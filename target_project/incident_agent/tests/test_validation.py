from shared.aula_4.validation import (
    validate_action_policy,
    validate_incident_input,
    validate_investigation,
)


def test_valid_investigation_with_known_evidence():
    payload = {
        "summary": "Falha relacionada ao timeout.",
        "classification": "pipeline_failure",
        "hypotheses": ["Saturação temporária da origem."],
        "evidence_ids": ["RB-001"],
        "recommended_actions": ["Validar escrita parcial antes de reprocessar."],
        "confidence": 0.7,
        "requires_human_review": True,
        "review_reason": "Ação requer aprovação.",
    }
    assert validate_investigation(payload, {"RB-001"})["is_valid"] is True


def test_unknown_evidence_is_rejected():
    payload = {
        "summary": "Resumo.",
        "classification": "unknown",
        "hypotheses": ["Hipótese."],
        "evidence_ids": ["INVENTED"],
        "recommended_actions": [],
        "confidence": 0.8,
        "requires_human_review": False,
        "review_reason": None,
    }
    result = validate_investigation(payload, {"RB-001"})
    assert result["is_valid"] is False
    assert any("unknown_evidence_ids" in error for error in result["errors"])


def test_medium_risk_action_requires_approval():
    result = validate_action_policy(
        {
            "action_name": "reprocess_pipeline",
            "risk_level": "medium",
            "reversible": True,
            "parameters": {},
            "justification": "Teste.",
            "requires_approval_recommendation": False,
        }
    )
    assert result["is_allowed"] is True
    assert result["requires_approval"] is True


def test_incident_validation_is_functional():
    incident = validate_incident_input(
        {
            "incident_id": "INC-1",
            "title": "Falha de teste",
            "description": "Descrição suficientemente detalhada.",
            "severity": "low",
            "source": "manual",
        }
    )
    assert incident["incident_id"] == "INC-1"
