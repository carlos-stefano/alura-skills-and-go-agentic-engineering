"""Referência conceitual de uma alternativa com agente único.

Este módulo não substitui o workflow principal. Ele existe para o exercício de
comparação arquitetural: um único agente recebe incidente, ferramentas disponíveis e
evidências recuperadas. A implementação é deliberadamente compacta para evidenciar
que multiagentes não são automaticamente superiores.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from shared.aula_4.llm import build_structured_agent, parsed_dict
from shared.aula_4.contracts import InvestigationOutput
from shared.aula_4.retrieval import execute_selected_tools, load_json_documents


def run_single_agent_baseline(
    incident: dict[str, Any],
    settings: dict[str, Any],
    knowledge_dir: str | Path,
) -> dict[str, Any]:
    documents = load_json_documents(knowledge_dir)
    evidence = execute_selected_tools(
        ["search_runbooks", "search_logs", "search_history"],
        [f"{incident['title']} {incident['description']}"],
        documents,
        top_k_per_query=2,
    )
    model = build_structured_agent(settings, InvestigationOutput)
    response = model.invoke(
        [
            SystemMessage(content="Analise o incidente usando somente as evidências fornecidas."),
            HumanMessage(content=json.dumps({"incident": incident, "evidence": evidence}, ensure_ascii=False)),
        ]
    )
    parsed, error = parsed_dict(response)
    return {"investigation": parsed, "error": error, "evidence": evidence}
