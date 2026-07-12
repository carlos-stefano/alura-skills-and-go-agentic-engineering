"""Pequenos adaptadores específicos de LangGraph.

A lógica de domínio não deve depender deste módulo. Ele existe apenas para encapsular
construção de estado inicial, compilação e renderização textual das rotas.
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from .contracts import WorkflowState
from .observability import new_run_id


def build_initial_state(incident: dict[str, Any]) -> WorkflowState:
    return {
        "run_id": new_run_id(),
        "incident": incident,
        "selected_tools": [],
        "search_queries": [],
        "retrieved_evidence": [],
        "retry_count": 0,
        "status": "created",
        "errors": [],
        "metrics": {
            "steps": {},
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "estimated_cost_usd": 0.0,
        },
        "events": [],
    }


def create_graph() -> StateGraph:
    return StateGraph(WorkflowState)


def graph_constants() -> tuple[str, str]:
    return START, END


def merge_step_metrics(
    state: dict[str, Any],
    step_name: str,
    elapsed_ms: float,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    previous = state.get("metrics", {})
    steps = {**previous.get("steps", {})}
    steps[step_name] = {"latency_ms": round(elapsed_ms, 2), **(extra or {})}
    return {**previous, "steps": steps}
