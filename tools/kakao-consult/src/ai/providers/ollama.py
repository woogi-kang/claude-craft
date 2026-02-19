"""Local Ollama LLM provider using httpx."""

from __future__ import annotations

import time

import httpx

from src.ai.providers.base import LLMResponse
from src.utils.logger import get_logger

logger = get_logger("ollama_provider")


class OllamaProvider:
    """Ollama local LLM provider for response generation.

    Communicates with a local Ollama server via its HTTP API.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def is_available(self) -> bool:
        """Check if the Ollama server is reachable."""
        try:
            resp = httpx.get(f"{self._base_url}/api/tags", timeout=3.0)
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError):
            return False

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse:
        """Generate a response using local Ollama server.

        Parameters
        ----------
        message:
            The user message to respond to.
        conversation_history:
            Previous conversation turns as role/content dicts.
        system_prompt:
            System prompt to guide model behavior.

        Returns
        -------
        LLMResponse
            The generated response with metadata.
        """
        start = time.monotonic()

        # Build messages list for Ollama chat API
        messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]
        for entry in conversation_history:
            messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": message})

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{self._base_url}/api/chat",
                    json={
                        "model": self._model,
                        "messages": messages,
                        "stream": False,
                        "options": {
                            "temperature": self._temperature,
                            "num_predict": self._max_tokens,
                        },
                    },
                )
                resp.raise_for_status()
                data = resp.json()

            elapsed_ms = int((time.monotonic() - start) * 1000)
            text = data.get("message", {}).get("content", "")
            tokens = data.get("eval_count", 0) + data.get("prompt_eval_count", 0)

            logger.info(
                "ollama_response",
                model=self._model,
                tokens=tokens,
                latency_ms=elapsed_ms,
            )
            return LLMResponse(
                text=text,
                provider="ollama",
                model=self._model,
                tokens_used=tokens,
                latency_ms=elapsed_ms,
            )

        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            logger.error("ollama_connection_error", error=str(exc))
            return LLMResponse(
                text="Ollama server is not available. Please try again later.",
                provider="ollama",
                model=self._model,
                tokens_used=0,
                latency_ms=elapsed_ms,
            )
        except httpx.HTTPStatusError as exc:
            elapsed_ms = int((time.monotonic() - start) * 1000)
            logger.error(
                "ollama_http_error",
                status_code=exc.response.status_code,
                error=str(exc),
            )
            return LLMResponse(
                text="Ollama request failed. Please check the model configuration.",
                provider="ollama",
                model=self._model,
                tokens_used=0,
                latency_ms=elapsed_ms,
            )
