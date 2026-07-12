"""Ferramentas locais e determinísticas de recuperação para os agentes.

O agente decide quais ferramentas e consultas usar. O código executa apenas as
ferramentas explicitamente disponíveis, preservando controle e auditabilidade.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


AVAILABLE_TOOLS = {
    "search_runbooks": "Busca procedimentos e runbooks técnicos.",
    "search_logs": "Busca logs sintéticos relacionados ao incidente.",
    "search_history": "Busca incidentes anteriores e respectivas resoluções.",
}


def load_json_documents(directory: str | Path) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for path in sorted(Path(directory).glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["_source_path"] = str(path)
        documents.append(payload)
    return documents


def keyword_score(query: str, text: str) -> float:
    query_terms = {term.lower().strip(".,:;()[]") for term in query.split() if len(term) > 2}
    text_terms = {term.lower().strip(".,:;()[]") for term in text.split()}
    if not query_terms:
        return 0.0
    return len(query_terms & text_terms) / len(query_terms)


def tool_source_type(tool_name: str) -> str:
    return {
        "search_runbooks": "runbook",
        "search_logs": "log",
        "search_history": "history",
    }[tool_name]


def search_documents(
    query: str,
    documents: list[dict[str, Any]],
    source_type: str,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    candidates = [item for item in documents if item.get("source_type") == source_type]
    scored: list[tuple[float, dict[str, Any]]] = []
    for document in candidates:
        searchable_text = " ".join(
            str(document.get(field, ""))
            for field in ("title", "symptoms", "content", "resolution", "service")
        )
        scored.append((keyword_score(query, searchable_text), document))

    ranked = sorted(scored, key=lambda item: item[0], reverse=True)
    return [
        {
            "evidence_id": document.get("id", f"doc_{index}"),
            "source_type": source_type,
            "content": document.get("content") or document.get("resolution") or str(document),
            "relevance_reason": f"ferramenta={source_type}; consulta={query}; pontuação={score:.3f}",
        }
        for index, (score, document) in enumerate(ranked[:top_k], start=1)
        if score > 0
    ]


def execute_selected_tools(
    selected_tools: list[str],
    search_queries: list[str],
    documents: list[dict[str, Any]],
    top_k_per_query: int = 2,
) -> list[dict[str, Any]]:
    """Executa somente ferramentas conhecidas e remove evidências duplicadas."""
    collected: dict[str, dict[str, Any]] = {}
    safe_tools = [tool for tool in selected_tools if tool in AVAILABLE_TOOLS]

    for tool_name in safe_tools:
        source_type = tool_source_type(tool_name)
        for query in search_queries:
            for evidence in search_documents(query, documents, source_type, top_k_per_query):
                collected[evidence["evidence_id"]] = evidence

    return list(collected.values())
