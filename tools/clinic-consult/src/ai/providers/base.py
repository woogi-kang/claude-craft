"""Abstract LLM provider protocol and shared LLM utilities."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    text: str
    provider: str
    model: str
    tokens_used: int = 0
    latency_ms: int = 0


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM provider implementations."""

    @property
    def name(self) -> str: ...

    @property
    def is_available(self) -> bool: ...

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse: ...


_logger = logging.getLogger("llm_fallback")

_DEFAULT_FALLBACK_ORDER = ["claude", "openai", "ollama"]


async def call_llm_with_fallback(
    providers: dict[str, LLMProvider],
    message: str,
    system_prompt: str,
    *,
    default_provider: str = "claude",
    conversation_history: list[dict[str, str]] | None = None,
    fallback_order: list[str] | None = None,
    error_text: str = "죄송합니다, 시스템 오류가 발생했습니다.",
) -> LLMResponse:
    """Call an LLM with automatic fallback chain.

    Tries the default provider first, then falls back through the
    ordered list until one succeeds.
    """
    history = conversation_history or []
    order = fallback_order or _DEFAULT_FALLBACK_ORDER
    tried: set[str] = set()

    for key in [default_provider] + order:
        if key in tried:
            continue
        tried.add(key)

        provider = providers.get(key)
        if provider is None or not provider.is_available:
            continue

        try:
            return await provider.generate(
                message=message,
                conversation_history=history,
                system_prompt=system_prompt,
            )
        except Exception as exc:
            _logger.error("provider_error: %s - %s", key, exc)
            continue

    return LLMResponse(
        text=error_text,
        provider="fallback",
        model="none",
    )
