"""Contagem aproximada de tokens para textos e mensagens."""

from __future__ import annotations

from typing import Any

import tiktoken


def get_encoder(model_name: str):
    try:
        return tiktoken.encoding_for_model(model_name)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")


def count_text_tokens(text: str, model_name: str) -> int:
    return len(get_encoder(model_name).encode(text))


def count_payload_tokens(payload: Any, model_name: str) -> int:
    return count_text_tokens(str(payload), model_name)
