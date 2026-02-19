"""OpenAI GPT LLM provider."""

from __future__ import annotations

import time

from src.ai.providers.base import LLMResponse
from src.utils.logger import get_logger

logger = get_logger("openai_provider")


class OpenAIProvider:
    """OpenAI API provider for response generation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
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
        return "openai"

    @property
    def is_available(self) -> bool:
        return bool(self._api_key)

    def _ensure_client(self):
        if self._client is None:
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=self._api_key)
            except ImportError:
                logger.error("openai_not_installed")
                raise

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse:
        """Generate a response using OpenAI API.

        Parameters
        ----------
        message:
            The user message to respond to.
        conversation_history:
            Previous conversation turns as role/content dicts.
        system_prompt:
            System prompt to guide GPT's behavior.

        Returns
        -------
        LLMResponse
            The generated response with metadata.
        """
        self._ensure_client()
        start = time.monotonic()

        # Build messages: system prompt first, then history, then user message
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]
        for entry in conversation_history:
            messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": message})

        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            messages=messages,
        )

        elapsed_ms = int((time.monotonic() - start) * 1000)

        choice = response.choices[0] if response.choices else None
        text = choice.message.content if choice and choice.message else ""
        tokens = 0
        if response.usage:
            tokens = (response.usage.prompt_tokens or 0) + (
                response.usage.completion_tokens or 0
            )

        logger.info(
            "openai_response",
            model=self._model,
            tokens=tokens,
            latency_ms=elapsed_ms,
        )
        return LLMResponse(
            text=text or "",
            provider="openai",
            model=self._model,
            tokens_used=tokens,
            latency_ms=elapsed_ms,
        )
