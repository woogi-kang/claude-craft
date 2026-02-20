"""Anthropic Claude LLM provider."""

from __future__ import annotations

import time

import httpx

from src.ai.providers.base import LLMResponse
from src.utils.logger import get_logger

logger = get_logger("claude_provider")


class ClaudeProvider:
    """Claude API provider for response generation."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature
        self._client = None

    @property
    def name(self) -> str:
        return "claude"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    def _ensure_client(self):
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic

                self._client = AsyncAnthropic(
                    api_key=self._api_key,
                    timeout=httpx.Timeout(30.0, connect=10.0),
                )
            except ImportError:
                logger.error("anthropic_not_installed")
                raise

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse:
        """Generate a response using Claude API.

        Parameters
        ----------
        message:
            The user message to respond to.
        conversation_history:
            Previous conversation turns as role/content dicts.
        system_prompt:
            System prompt to guide Claude's behavior.

        Returns
        -------
        LLMResponse
            The generated response with metadata.
        """
        self._ensure_client()
        start = time.monotonic()

        # Build messages list from history + current message
        messages = []
        for entry in conversation_history:
            messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": message})

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            system=system_prompt,
            messages=messages,
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)
        text = response.content[0].text if response.content else ""
        tokens = response.usage.input_tokens + response.usage.output_tokens

        logger.info(
            "claude_response",
            model=self._model,
            tokens=tokens,
            latency_ms=elapsed_ms,
        )
        return LLMResponse(
            text=text,
            provider="claude",
            model=self._model,
            tokens_used=tokens,
            latency_ms=elapsed_ms,
        )
