"""Abstract LLM provider protocol."""

from __future__ import annotations

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
