"""API local que reutiliza o mesmo workflow multiagente da CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, HTTPException

from shared.aula_4.config import get_settings
from shared.aula_4.validation import validate_incident_input

from .workflow import run_workflow

PROJECT_DIR = Path(__file__).resolve().parents[1]

app = FastAPI(
    title="Multi-Agent Incident API",
    version="0.2.0",
    description="API didática para operacionalização de um workflow multiagente com LangGraph.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/incidents/investigate")
def investigate_incident(incident: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        valid_incident = validate_incident_input(incident)
        settings = get_settings(PROJECT_DIR / ".env")
        return run_workflow(valid_incident, settings, PROJECT_DIR / "data" / "knowledge")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Falha no workflow: {exc}") from exc
