"""Leitura e validação funcional das configurações da Aula 4."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def load_environment(env_file: str | Path | None = None) -> None:
    """Carrega variáveis de ambiente sem sobrescrever valores já definidos."""
    if env_file:
        load_dotenv(dotenv_path=env_file, override=False)
    else:
        load_dotenv(override=False)


def get_settings(env_file: str | Path | None = None) -> dict[str, Any]:
    """Retorna configurações validadas como um dicionário simples."""
    load_environment(env_file)

    settings = {
        "model_name": os.getenv("MODEL_NAME", "gpt-4.1-mini"),
        "temperature": float(os.getenv("MODEL_TEMPERATURE", "0")),
        "max_retries": int(os.getenv("MAX_RETRIES", "1")),
        "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
        "log_dir": os.getenv("LOG_DIR", "data/runtime_logs"),
        "token_price_input_per_million": float(
            os.getenv("TOKEN_PRICE_INPUT_PER_MILLION", "0")
        ),
        "token_price_output_per_million": float(
            os.getenv("TOKEN_PRICE_OUTPUT_PER_MILLION", "0")
        ),
        "require_human_approval": os.getenv(
            "REQUIRE_HUMAN_APPROVAL", "true"
        ).lower() in {"1", "true", "yes", "y"},
    }

    errors: list[str] = []
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY não foi encontrada no ambiente.")
    if settings["temperature"] < 0:
        errors.append("MODEL_TEMPERATURE não pode ser negativa.")
    if settings["max_retries"] < 0:
        errors.append("MAX_RETRIES não pode ser negativo.")

    if errors:
        raise ValueError("Configuração inválida: " + " | ".join(errors))

    return settings
