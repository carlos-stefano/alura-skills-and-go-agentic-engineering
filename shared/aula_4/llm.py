"""Construção funcional dos modelos usados pelos agentes.

Cada função devolve um ``Runnable`` com saída estruturada. Os modelos não guardam
estado: recebem mensagens e devolvem um contrato explícito.
"""

from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from .contracts import ActionProposal, InvestigationOutput, ReviewOutput, TriageOutput


def build_chat_model(settings: dict[str, Any]) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings["model_name"],
        temperature=settings["temperature"],
    )


def build_structured_agent(settings: dict[str, Any], schema: Any):
    return build_chat_model(settings).with_structured_output(schema, include_raw=True)


def build_agent_models(settings: dict[str, Any]) -> dict[str, Any]:
    """Cria os quatro agentes do workflow multiagente."""
    return {
        "triage": build_structured_agent(settings, TriageOutput),
        "investigation": build_structured_agent(settings, InvestigationOutput),
        "review": build_structured_agent(settings, ReviewOutput),
        "action_planner": build_structured_agent(settings, ActionProposal),
    }


def extract_usage_metadata(response: dict[str, Any]) -> dict[str, int]:
    raw = response.get("raw")
    usage = getattr(raw, "usage_metadata", None) or {}
    return {
        "input_tokens": int(usage.get("input_tokens", 0)),
        "output_tokens": int(usage.get("output_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
    }


def parsed_dict(response: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """Normaliza saídas estruturadas baseadas em TypedDict ou Pydantic."""
    parsed = response.get("parsed")
    error = response.get("parsing_error")
    if parsed is None:
        return None, str(error) if error else "structured_output_missing"
    if hasattr(parsed, "model_dump"):
        return parsed.model_dump(), None
    return dict(parsed), None
