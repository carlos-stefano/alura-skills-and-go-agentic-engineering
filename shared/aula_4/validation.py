"""Validações determinísticas e políticas independentes dos agentes."""

from __future__ import annotations

from typing import Any


REQUIRED_INCIDENT_FIELDS = {"incident_id", "title", "description", "severity", "source"}
ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}


def validate_incident_input(payload: dict[str, Any]) -> dict[str, Any]:
    errors = [f"missing_field:{field}" for field in sorted(REQUIRED_INCIDENT_FIELDS - payload.keys())]
    if payload.get("severity") not in ALLOWED_SEVERITIES:
        errors.append("invalid_severity")
    if len(str(payload.get("title", ""))) < 3:
        errors.append("title_too_short")
    if len(str(payload.get("description", ""))) < 10:
        errors.append("description_too_short")
    if errors:
        raise ValueError("Incidente inválido: " + " | ".join(errors))
    return {field: payload[field] for field in REQUIRED_INCIDENT_FIELDS}


def validate_investigation(payload: dict[str, Any], evidence_ids: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    required = {
        "summary", "classification", "hypotheses", "evidence_ids",
        "recommended_actions", "confidence", "requires_human_review", "review_reason",
    }
    missing = sorted(required - payload.keys())
    errors.extend(f"missing_field:{field}" for field in missing)

    unknown_evidence = sorted(set(payload.get("evidence_ids", [])) - evidence_ids)
    if unknown_evidence:
        errors.append(f"unknown_evidence_ids:{unknown_evidence}")

    confidence = payload.get("confidence", 0)
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append("invalid_confidence")
    if confidence >= 0.75 and not payload.get("evidence_ids"):
        errors.append("high_confidence_without_evidence")
    if not payload.get("hypotheses"):
        errors.append("missing_hypotheses")

    return {"is_valid": not errors, "errors": errors, "parsed": payload if not errors else None}


def validate_action_policy(action: dict[str, Any]) -> dict[str, Any]:
    required = {"action_name", "risk_level", "reversible", "parameters", "justification"}
    missing = sorted(required - action.keys())
    if missing:
        return {
            "is_allowed": False,
            "requires_approval": True,
            "errors": [f"missing_field:{field}" for field in missing],
        }

    forbidden_actions = {"delete_database", "disable_security", "expose_secret"}
    if action["action_name"] in forbidden_actions:
        return {"is_allowed": False, "requires_approval": True, "errors": ["forbidden_action"]}

    if action.get("risk_level") not in {"low", "medium", "high"}:
        return {"is_allowed": False, "requires_approval": True, "errors": ["invalid_risk_level"]}

    requires_approval = (
        action["risk_level"] in {"medium", "high"}
        or not bool(action["reversible"])
        or bool(action.get("requires_approval_recommendation"))
    )
    return {"is_allowed": True, "requires_approval": requires_approval, "errors": []}
