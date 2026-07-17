"""Contratos de dados da Aula 4.

Os contratos usam ``TypedDict`` apenas para tipagem e saídas estruturadas. Não há
classes de serviço nem objetos com estado interno: toda a aplicação é composta por
funções que recebem e devolvem dicionários.
"""

from __future__ import annotations

from typing import Any, Literal, NotRequired, TypedDict


class IncidentInput(TypedDict):
    incident_id: str
    title: str
    description: str
    severity: Literal["low", "medium", "high", "critical"]
    source: str


class TriageOutput(TypedDict):
    classification: str
    selected_tools: list[Literal["search_runbooks", "search_logs", "search_history"]]
    search_queries: list[str]
    rationale: str
    priority: Literal["low", "medium", "high", "critical"]


class InvestigationOutput(TypedDict):
    summary: str
    classification: str
    hypotheses: list[str]
    evidence_ids: list[str]
    recommended_actions: list[str]
    confidence: float
    requires_human_review: bool
    review_reason: str | None


class ReviewOutput(TypedDict):
    decision: Literal["approved", "revise", "human_review"]
    evidence_alignment: Literal["strong", "partial", "weak"]
    issues: list[str]
    feedback_to_investigator: str
    requires_additional_evidence: bool
    additional_search_queries: list[str]


class ActionProposal(TypedDict):
    action_name: str
    risk_level: Literal["low", "medium", "high"]
    reversible: bool
    parameters: dict[str, Any]
    justification: str
    requires_approval_recommendation: bool


class WorkflowState(TypedDict):
    run_id: str
    incident: IncidentInput
    triage: NotRequired[TriageOutput]
    selected_tools: list[str]
    search_queries: list[str]
    retrieved_evidence: list[dict[str, Any]]
    investigation: NotRequired[InvestigationOutput]
    deterministic_validation: NotRequired[dict[str, Any]]
    review: NotRequired[ReviewOutput]
    proposed_action: NotRequired[dict[str, Any]]
    approval_status: NotRequired[Literal["not_required", "pending", "approved", "rejected"]]
    execution_result: NotRequired[dict[str, Any]]
    retry_count: int
    status: str
    errors: list[str]
    metrics: dict[str, Any]
    events: list[dict[str, Any]]
