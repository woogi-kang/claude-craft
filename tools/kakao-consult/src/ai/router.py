"""Multi-LLM router for response generation."""

from __future__ import annotations

from src.ai.classifier import ClassificationResult
from src.ai.prompts import COMPLAINT_SYSTEM_PROMPT, CONSULTATION_SYSTEM_PROMPT
from src.ai.providers.base import LLMProvider, LLMResponse
from src.utils.logger import get_logger

logger = get_logger("router")


class LLMRouter:
    """Route messages to the optimal LLM provider.

    Parameters
    ----------
    providers:
        Dict mapping provider name to LLMProvider instance.
    default_provider:
        Name of the default provider to use.
    """

    def __init__(
        self,
        providers: dict[str, LLMProvider],
        default_provider: str = "claude",
    ) -> None:
        self._providers = providers
        self._default = default_provider
        self._fallback_order = ["claude", "openai", "ollama"]

    async def route(
        self,
        message: str,
        classification: ClassificationResult,
        conversation_history: list[dict[str, str]],
    ) -> LLMResponse:
        """Route to the best available LLM and generate response.

        Parameters
        ----------
        message:
            The user message requiring a response.
        classification:
            The classification result with suggested LLM.
        conversation_history:
            Previous conversation turns as role/content dicts.

        Returns
        -------
        LLMResponse
            Generated response from the selected provider.
        """
        # Select system prompt based on intent
        if classification.intent == "complaint":
            system_prompt = COMPLAINT_SYSTEM_PROMPT
        else:
            system_prompt = CONSULTATION_SYSTEM_PROMPT

        # Determine target provider from classification or default
        target = classification.suggested_llm or self._default

        # Map classifier suggestion names to provider keys
        provider_map = {"claude": "claude", "gpt4": "openai", "ollama": "ollama"}
        provider_key = provider_map.get(target, self._default)

        # Try target provider, then fallback chain
        tried: set[str] = set()
        for key in [provider_key] + self._fallback_order:
            if key in tried:
                continue
            tried.add(key)

            provider = self._providers.get(key)
            if provider is None or not provider.is_available:
                logger.warning("provider_unavailable", provider=key)
                continue

            try:
                response = await provider.generate(
                    message=message,
                    conversation_history=conversation_history,
                    system_prompt=system_prompt,
                )
                logger.info(
                    "routed",
                    provider=key,
                    intent=classification.intent,
                    tokens=response.tokens_used,
                )
                return response
            except Exception as exc:
                logger.error("provider_error", provider=key, error=str(exc))
                continue

        # All providers failed - return error message in Korean
        logger.error("all_providers_failed")
        return LLMResponse(
            text="죄송합니다, 잠시 후 다시 문의해주세요.",
            provider="fallback",
            model="none",
        )
