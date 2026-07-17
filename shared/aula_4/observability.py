"""Funções pequenas para eventos, tempos, métricas e persistência local."""

from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_run_id(prefix: str = "run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def build_event(
    run_id: str,
    event_type: str,
    step: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "timestamp": utc_now_iso(),
        "event_type": event_type,
        "step": step,
        "payload": payload or {},
    }


def append_event(
    state: dict[str, Any],
    event_type: str,
    step: str,
    payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    return [
        *state.get("events", []),
        build_event(state["run_id"], event_type, step, payload),
    ]


def timed_call(function: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
    started = time.perf_counter()
    result = function(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return result, elapsed_ms


def estimate_cost_usd(
    input_tokens: int,
    output_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> float:
    input_cost = input_tokens / 1_000_000 * input_price_per_million
    output_cost = output_tokens / 1_000_000 * output_price_per_million
    return round(input_cost + output_cost, 8)


def persist_run(run_record: dict[str, Any], log_dir: str | Path) -> Path:
    directory = Path(log_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / f"{run_record['run_id']}.json"
    output_path.write_text(
        json.dumps(run_record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def summarize_runs(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {
            "total_runs": 0,
            "success_rate": 0.0,
            "human_review_rate": 0.0,
            "average_latency_ms": 0.0,
            "average_total_tokens": 0.0,
        }

    total = len(records)
    successes = sum(record.get("status") == "completed" for record in records)
    reviews = sum(record.get("status") == "human_review_required" for record in records)
    latencies = [record.get("metrics", {}).get("total_latency_ms", 0) for record in records]
    tokens = [record.get("metrics", {}).get("total_tokens", 0) for record in records]

    return {
        "total_runs": total,
        "success_rate": round(successes / total, 4),
        "human_review_rate": round(reviews / total, 4),
        "average_latency_ms": round(sum(latencies) / total, 2),
        "average_total_tokens": round(sum(tokens) / total, 2),
    }
