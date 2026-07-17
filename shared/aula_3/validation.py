from jsonschema import Draft202012Validator


ANALYSIS_SCHEMA = {
    "type": "object",
    "required": [
        "incident_id",
        "classification",
        "summary",
        "hypotheses",
        "evidence_ids",
        "recommended_actions",
        "confidence",
        "requires_human_review",
    ],
    "properties": {
        "incident_id": {"type": "string", "minLength": 1},
        "classification": {"type": "string", "minLength": 1},
        "summary": {"type": "string", "minLength": 1},
        "hypotheses": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "evidence_ids": {
            "type": "array",
            "items": {"type": "string", "pattern": "^project:"},
        },
        "recommended_actions": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "requires_human_review": {"type": "boolean"},
    },
    "additionalProperties": False,
}


def validate_schema(payload, schema=ANALYSIS_SCHEMA):
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )

    return {
        "valid": not errors,
        "errors": [
            {
                "path": ".".join(map(str, error.absolute_path)) or "<root>",
                "message": error.message,
            }
            for error in errors
        ],
    }


def validate_evidence(payload, valid_evidence_ids):
    cited = set(payload.get("evidence_ids", []))
    invalid = sorted(cited - set(valid_evidence_ids))

    return {
        "valid": not invalid,
        "invalid_evidence_ids": invalid,
        "cited_count": len(cited),
    }


def validate_safety(payload, low_confidence_threshold=0.60):
    errors = []

    if payload.get("confidence", 0) < low_confidence_threshold:
        if not payload.get("requires_human_review", False):
            errors.append("Baixa confiança sem revisão humana.")

    if not payload.get("evidence_ids"):
        if not payload.get("requires_human_review", False):
            errors.append("Análise sem evidências não foi escalada.")

    high_impact_terms = (
        "apagar", "deletar", "rotacionar credencial", "executar em produção",
        "reiniciar produção", "alterar firewall",
    )
    actions_text = " ".join(payload.get("recommended_actions", [])).lower()

    if any(term in actions_text for term in high_impact_terms):
        if not payload.get("requires_human_review", False):
            errors.append("Ação de alto impacto sem revisão humana.")

    return {"valid": not errors, "errors": errors}


def evaluate_analysis(payload, valid_evidence_ids):
    schema = validate_schema(payload)

    if not schema["valid"]:
        return {
            "schema": schema,
            "evidence": {"valid": False, "invalid_evidence_ids": []},
            "safety": {"valid": False, "errors": ["Não avaliado: schema inválido."]},
            "accepted": False,
        }

    evidence = validate_evidence(payload, valid_evidence_ids)
    safety = validate_safety(payload)

    return {
        "schema": schema,
        "evidence": evidence,
        "safety": safety,
        "accepted": schema["valid"] and evidence["valid"] and safety["valid"],
    }


def decide_next_action(evaluation, attempt_number, max_attempts):
    if evaluation["accepted"]:
        return "accept"
    if attempt_number >= max_attempts:
        return "human_review"
    if not evaluation["schema"]["valid"]:
        return "retry_format"
    if not evaluation["evidence"]["valid"]:
        return "retry_with_evidence_feedback"
    return "human_review"
