"""Workflow multiagente de investigação de incidentes com LangGraph.

O grafo possui quatro agentes reais, todos chamados por LLM:

1. triagem: classifica o incidente e escolhe ferramentas/consultas;
2. investigação: formula hipóteses com base nas evidências recuperadas;
3. revisão: critica a investigação e decide aprovar, revisar ou escalar;
4. planejamento de ação: propõe uma ação estruturada.

As ferramentas, validações, políticas de segurança, métricas e rotas continuam
sendo determinísticas. Essa divisão evita delegar ao modelo decisões que devem ser
previsíveis e auditáveis.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from shared.aula_4.config import get_settings
from shared.aula_4.langgraph_helpers import (
    build_initial_state,
    create_graph,
    graph_constants,
    merge_step_metrics,
)
from shared.aula_4.llm import build_agent_models, extract_usage_metadata, parsed_dict
from shared.aula_4.observability import append_event, estimate_cost_usd, persist_run
from shared.aula_4.retrieval import AVAILABLE_TOOLS, execute_selected_tools, load_json_documents
from shared.aula_4.validation import (
    validate_action_policy,
    validate_incident_input,
    validate_investigation,
)

PROJECT_DIR = Path(__file__).resolve().parents[1]


def add_agent_metrics(
    state: dict[str, Any],
    step_name: str,
    elapsed_ms: float,
    usage: dict[str, int],
) -> dict[str, Any]:
    metrics = merge_step_metrics(state, step_name, elapsed_ms, usage)
    previous = state.get("metrics", {})
    return {
        **metrics,
        "input_tokens": previous.get("input_tokens", 0) + usage["input_tokens"],
        "output_tokens": previous.get("output_tokens", 0) + usage["output_tokens"],
        "total_tokens": previous.get("total_tokens", 0) + usage["total_tokens"],
    }


def invoke_structured_agent(
    model: Any,
    system_prompt: str,
    payload: dict[str, Any],
) -> tuple[dict[str, Any] | None, str | None, dict[str, int]]:
    response = model.invoke(
        [
            SystemMessage(content=system_prompt.strip()),
            HumanMessage(content=json.dumps(payload, ensure_ascii=False, indent=2)),
        ]
    )
    parsed, parsing_error = parsed_dict(response)
    return parsed, parsing_error, extract_usage_metadata(response)


def triage_node(state: dict[str, Any], models: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    prompt = """
Você é o agente de triagem de incidentes técnicos.
Classifique o incidente e escolha somente as ferramentas necessárias entre as opções fornecidas.
Gere de uma a três consultas de busca específicas. Não alegue ter consultado evidências ainda.
Evite selecionar todas as ferramentas por padrão: cada escolha deve ser justificada pelo incidente.
"""
    payload = {
        "incident": state["incident"],
        "available_tools": [
            {"name": name, "description": description}
            for name, description in AVAILABLE_TOOLS.items()
        ],
    }
    parsed, error, usage = invoke_structured_agent(models["triage"], prompt, payload)
    elapsed_ms = (time.perf_counter() - started) * 1000

    triage = parsed or {
        "classification": "triage_error",
        "selected_tools": [],
        "search_queries": [],
        "rationale": error or "Falha na saída estruturada da triagem.",
        "priority": state["incident"]["severity"],
    }
    safe_tools = [tool for tool in triage.get("selected_tools", []) if tool in AVAILABLE_TOOLS]
    queries = [query.strip() for query in triage.get("search_queries", []) if query.strip()]

    return {
        "triage": triage,
        "selected_tools": safe_tools,
        "search_queries": queries,
        "status": "triaged" if safe_tools and queries else "triage_incomplete",
        "metrics": add_agent_metrics(state, "triage_agent", elapsed_ms, usage),
        "events": append_event(
            state,
            "agent_completed",
            "triage_agent",
            {"selected_tools": safe_tools, "search_queries": queries, "error": error},
        ),
    }


def retrieve_node(state: dict[str, Any], knowledge_dir: str | Path) -> dict[str, Any]:
    started = time.perf_counter()
    documents = load_json_documents(knowledge_dir)
    evidence = execute_selected_tools(
        state.get("selected_tools", []),
        state.get("search_queries", []),
        documents,
        top_k_per_query=2,
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    return {
        "retrieved_evidence": evidence,
        "status": "evidence_retrieved" if evidence else "evidence_not_found",
        "metrics": merge_step_metrics(
            state,
            "execute_tools",
            elapsed_ms,
            {"documents": len(evidence), "tools": state.get("selected_tools", [])},
        ),
        "events": append_event(
            state,
            "tools_completed",
            "execute_tools",
            {
                "tools": state.get("selected_tools", []),
                "queries": state.get("search_queries", []),
                "evidence_ids": [item["evidence_id"] for item in evidence],
            },
        ),
    }


def investigate_node(state: dict[str, Any], models: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    prompt = """
Você é o agente investigador.
Use somente as evidências fornecidas e cite seus identificadores em evidence_ids.
Não invente causas, logs, documentos ou resultados de ferramentas.
Considere o feedback do revisor e os erros determinísticos de tentativas anteriores.
Quando as evidências forem insuficientes ou conflitantes, reduza a confiança e sinalize revisão humana.
"""
    payload = {
        "incident": state["incident"],
        "triage": state.get("triage"),
        "evidence": state.get("retrieved_evidence", []),
        "retry_count": state["retry_count"],
        "review_feedback": state.get("review", {}).get("feedback_to_investigator"),
        "previous_validation_errors": state.get("deterministic_validation", {}).get("errors", []),
    }
    parsed, error, usage = invoke_structured_agent(models["investigation"], prompt, payload)
    elapsed_ms = (time.perf_counter() - started) * 1000

    investigation = parsed or {
        "summary": "A resposta do investigador não respeitou o contrato esperado.",
        "classification": "invalid_output",
        "hypotheses": [],
        "evidence_ids": [],
        "recommended_actions": [],
        "confidence": 0.0,
        "requires_human_review": True,
        "review_reason": error,
    }
    return {
        "investigation": investigation,
        "status": "investigated",
        "metrics": add_agent_metrics(state, "investigation_agent", elapsed_ms, usage),
        "events": append_event(
            state,
            "agent_completed",
            "investigation_agent",
            {"classification": investigation.get("classification"), "error": error},
        ),
    }


def validate_node(state: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    evidence_ids = {item["evidence_id"] for item in state.get("retrieved_evidence", [])}
    validation = validate_investigation(state["investigation"], evidence_ids)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {
        "deterministic_validation": validation,
        "status": "validated" if validation["is_valid"] else "validation_failed",
        "metrics": merge_step_metrics(state, "deterministic_validation", elapsed_ms),
        "events": append_event(
            state,
            "validation_completed",
            "deterministic_validation",
            {"is_valid": validation["is_valid"], "errors": validation["errors"]},
        ),
    }


def route_after_validation(state: dict[str, Any], max_retries: int) -> str:
    if state["deterministic_validation"]["is_valid"]:
        return "review"
    if state["retry_count"] < max_retries:
        return "retry"
    return "human_review"


def review_node(state: dict[str, Any], models: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    prompt = """
Você é o agente revisor independente.
Avalie se a investigação é sustentada pelas evidências, se há contradições e se a confiança é adequada.
Não produza um novo diagnóstico. Decida entre approved, revise e human_review.
Use revise somente quando feedback ou novas buscas puderem melhorar a resposta dentro de uma nova tentativa.
"""
    payload = {
        "incident": state["incident"],
        "evidence": state.get("retrieved_evidence", []),
        "investigation": state["investigation"],
        "deterministic_validation": state["deterministic_validation"],
        "retry_count": state["retry_count"],
    }
    parsed, error, usage = invoke_structured_agent(models["review"], prompt, payload)
    elapsed_ms = (time.perf_counter() - started) * 1000

    review = parsed or {
        "decision": "human_review",
        "evidence_alignment": "weak",
        "issues": [error or "Falha na saída estruturada do revisor."],
        "feedback_to_investigator": "Encaminhar para revisão humana.",
        "requires_additional_evidence": False,
        "additional_search_queries": [],
    }
    return {
        "review": review,
        "status": f"review_{review['decision']}",
        "metrics": add_agent_metrics(state, "review_agent", elapsed_ms, usage),
        "events": append_event(
            state,
            "agent_completed",
            "review_agent",
            {"decision": review["decision"], "issues": review.get("issues", []), "error": error},
        ),
    }


def route_after_review(state: dict[str, Any], max_retries: int) -> str:
    decision = state["review"]["decision"]
    if decision == "approved":
        return "plan_action"
    if decision == "revise" and state["retry_count"] < max_retries:
        return "retry"
    return "human_review"


def retry_node(state: dict[str, Any]) -> dict[str, Any]:
    additional_queries = state.get("review", {}).get("additional_search_queries", [])
    queries = list(dict.fromkeys([*state.get("search_queries", []), *additional_queries]))
    return {
        "retry_count": state["retry_count"] + 1,
        "search_queries": queries,
        "status": "retrying",
        "events": append_event(
            state,
            "retry_scheduled",
            "retry",
            {"retry_count": state["retry_count"] + 1, "search_queries": queries},
        ),
    }


def action_planner_node(state: dict[str, Any], models: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    prompt = """
Você é o agente planejador de ação.
Proponha no máximo uma ação coerente com a investigação aprovada.
Não execute ações. Expresse risco, reversibilidade, parâmetros e justificativa.
Prefira request_manual_investigation quando não houver base suficiente para uma ação técnica concreta.
"""
    payload = {
        "incident": state["incident"],
        "investigation": state["investigation"],
        "review": state["review"],
        "allowed_action_examples": [
            "request_manual_investigation",
            "reprocess_pipeline",
            "rotate_credential",
            "collect_additional_metrics",
        ],
    }
    parsed, error, usage = invoke_structured_agent(models["action_planner"], prompt, payload)
    elapsed_ms = (time.perf_counter() - started) * 1000

    proposal = parsed or {
        "action_name": "request_manual_investigation",
        "risk_level": "low",
        "reversible": True,
        "parameters": {"incident_id": state["incident"]["incident_id"]},
        "justification": error or "Falha na saída estruturada do planejador.",
        "requires_approval_recommendation": True,
    }
    policy = validate_action_policy(proposal)
    approval_status = "pending" if policy["requires_approval"] else "not_required"

    return {
        "proposed_action": {**proposal, "policy": policy},
        "approval_status": approval_status,
        "status": "action_proposed",
        "metrics": add_agent_metrics(state, "action_planner_agent", elapsed_ms, usage),
        "events": append_event(
            state,
            "agent_completed",
            "action_planner_agent",
            {"action": proposal["action_name"], "policy": policy, "error": error},
        ),
    }


def route_after_action(state: dict[str, Any]) -> str:
    policy = state["proposed_action"]["policy"]
    if not policy["is_allowed"] or policy["requires_approval"]:
        return "human_review"
    return "simulate_action"


def simulate_action_node(state: dict[str, Any]) -> dict[str, Any]:
    action = state["proposed_action"]
    result = {
        "executed": False,
        "simulation": True,
        "action_name": action["action_name"],
        "message": "A ação foi apenas simulada. Nenhum sistema externo foi alterado.",
    }
    return {
        "execution_result": result,
        "status": "completed",
        "events": append_event(state, "action_simulated", "simulate_action", result),
    }


def human_review_node(state: dict[str, Any]) -> dict[str, Any]:
    reasons = [
        state.get("investigation", {}).get("review_reason"),
        *state.get("deterministic_validation", {}).get("errors", []),
        *state.get("review", {}).get("issues", []),
        *state.get("proposed_action", {}).get("policy", {}).get("errors", []),
    ]
    reason = "; ".join(str(item) for item in reasons if item) or "Ação ou análise requer revisão humana."
    return {
        "approval_status": "pending",
        "status": "human_review_required",
        "execution_result": {
            "executed": False,
            "simulation": True,
            "message": "Execução interrompida para revisão humana.",
            "reason": reason,
        },
        "events": append_event(state, "human_review_required", "human_review", {"reason": reason}),
    }


def finalize_node(state: dict[str, Any], settings: dict[str, Any]) -> dict[str, Any]:
    steps = state.get("metrics", {}).get("steps", {})
    total_latency = sum(step.get("latency_ms", 0) for step in steps.values())
    metrics = {**state.get("metrics", {}), "total_latency_ms": round(total_latency, 2)}
    metrics["estimated_cost_usd"] = estimate_cost_usd(
        metrics.get("input_tokens", 0),
        metrics.get("output_tokens", 0),
        settings["token_price_input_per_million"],
        settings["token_price_output_per_million"],
    )
    final_record = {
        **state,
        "metrics": metrics,
        "events": append_event(state, "workflow_finished", "finalize", {"status": state["status"]}),
    }
    log_dir = Path(settings["log_dir"])
    if not log_dir.is_absolute():
        log_dir = PROJECT_DIR / log_dir
    output_path = persist_run(final_record, log_dir)
    return {
        "metrics": metrics,
        "events": final_record["events"],
        "execution_result": {**state.get("execution_result", {}), "run_record_path": str(output_path)},
    }


def build_workflow(settings: dict[str, Any], knowledge_dir: str | Path):
    models = build_agent_models(settings)
    graph = create_graph()
    START, END = graph_constants()

    graph.add_node("triage", lambda state: triage_node(state, models))
    graph.add_node("execute_tools", lambda state: retrieve_node(state, knowledge_dir))
    graph.add_node("investigate", lambda state: investigate_node(state, models))
    graph.add_node("validate", validate_node)
    graph.add_node("review", lambda state: review_node(state, models))
    graph.add_node("retry", retry_node)
    graph.add_node("plan_action", lambda state: action_planner_node(state, models))
    graph.add_node("simulate_action", simulate_action_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("finalize", lambda state: finalize_node(state, settings))

    graph.add_edge(START, "triage")
    graph.add_edge("triage", "execute_tools")
    graph.add_edge("execute_tools", "investigate")
    graph.add_edge("investigate", "validate")
    graph.add_conditional_edges(
        "validate",
        lambda state: route_after_validation(state, settings["max_retries"]),
        {"review": "review", "retry": "retry", "human_review": "human_review"},
    )
    graph.add_conditional_edges(
        "review",
        lambda state: route_after_review(state, settings["max_retries"]),
        {"plan_action": "plan_action", "retry": "retry", "human_review": "human_review"},
    )
    graph.add_edge("retry", "execute_tools")
    graph.add_conditional_edges(
        "plan_action",
        route_after_action,
        {"simulate_action": "simulate_action", "human_review": "human_review"},
    )
    graph.add_edge("simulate_action", "finalize")
    graph.add_edge("human_review", "finalize")
    graph.add_edge("finalize", END)
    return graph.compile()


def run_workflow(
    incident: dict[str, Any],
    settings: dict[str, Any] | None = None,
    knowledge_dir: str | Path = PROJECT_DIR / "data" / "knowledge",
) -> dict[str, Any]:
    active_settings = settings or get_settings()
    valid_incident = validate_incident_input(incident)
    workflow = build_workflow(active_settings, knowledge_dir)
    return workflow.invoke(build_initial_state(valid_incident))
