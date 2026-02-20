"""Tests for the LLMRouter with mock providers."""

from __future__ import annotations

import pytest

from src.ai.classifier import ClassificationResult
from src.ai.prompts import COMPLAINT_SYSTEM_PROMPT, CONSULTATION_SYSTEM_PROMPT
from src.ai.providers.base import LLMResponse
from src.ai.router import LLMRouter


# ---------------------------------------------------------------------------
# Mock provider
# ---------------------------------------------------------------------------

class MockProvider:
    """A configurable mock LLM provider for testing."""

    def __init__(
        self,
        name: str,
        available: bool = True,
        response_text: str = "mock response",
        should_raise: bool = False,
    ) -> None:
        self._name = name
        self._available = available
        self._response_text = response_text
        self._should_raise = should_raise
        self.generate_calls: list[dict] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_available(self) -> bool:
        return self._available

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse:
        if self._should_raise:
            raise RuntimeError(f"{self._name} provider error")

        self.generate_calls.append(
            {
                "message": message,
                "conversation_history": conversation_history,
                "system_prompt": system_prompt,
            }
        )
        return LLMResponse(
            text=self._response_text,
            provider=self._name,
            model=f"{self._name}-model",
            tokens_used=100,
            latency_ms=50,
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def classification_complex() -> ClassificationResult:
    return ClassificationResult(
        intent="complex",
        confidence=0.9,
        suggested_llm="claude",
        rationale="medical question",
    )


@pytest.fixture
def classification_complaint() -> ClassificationResult:
    return ClassificationResult(
        intent="complaint",
        confidence=0.85,
        suggested_llm="claude",
        rationale="upset customer",
    )


@pytest.fixture
def classification_general() -> ClassificationResult:
    return ClassificationResult(
        intent="complex",
        confidence=0.8,
        suggested_llm="gpt4",
        rationale="general consultation",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_route_to_suggested_provider(classification_general):
    """Router should use the provider suggested by the classifier."""
    openai_provider = MockProvider("openai", response_text="openai response")
    claude_provider = MockProvider("claude", response_text="claude response")

    router = LLMRouter(
        providers={"claude": claude_provider, "openai": openai_provider},
        default_provider="claude",
    )

    result = await router.route(
        message="Tell me about treatment options",
        classification=classification_general,
        conversation_history=[],
    )

    assert result.provider == "openai"
    assert result.text == "openai response"
    assert len(openai_provider.generate_calls) == 1
    assert len(claude_provider.generate_calls) == 0


@pytest.mark.asyncio
async def test_fallback_on_unavailable_provider(classification_general):
    """Router should fall back when the suggested provider is unavailable."""
    openai_provider = MockProvider("openai", available=False)
    claude_provider = MockProvider("claude", response_text="claude fallback")

    router = LLMRouter(
        providers={"claude": claude_provider, "openai": openai_provider},
        default_provider="claude",
    )

    result = await router.route(
        message="Tell me about treatment",
        classification=classification_general,
        conversation_history=[],
    )

    assert result.provider == "claude"
    assert result.text == "claude fallback"


@pytest.mark.asyncio
async def test_fallback_on_provider_error(classification_complex):
    """Router should try the next provider when one raises an exception."""
    claude_provider = MockProvider("claude", should_raise=True)
    openai_provider = MockProvider("openai", response_text="openai rescued")

    router = LLMRouter(
        providers={"claude": claude_provider, "openai": openai_provider},
        default_provider="claude",
    )

    result = await router.route(
        message="Detailed question",
        classification=classification_complex,
        conversation_history=[],
    )

    assert result.provider == "openai"
    assert result.text == "openai rescued"


@pytest.mark.asyncio
async def test_all_providers_failed():
    """When all providers fail, router returns a Korean fallback message."""
    claude_provider = MockProvider("claude", should_raise=True)
    openai_provider = MockProvider("openai", available=False)
    ollama_provider = MockProvider("ollama", should_raise=True)

    router = LLMRouter(
        providers={
            "claude": claude_provider,
            "openai": openai_provider,
            "ollama": ollama_provider,
        },
        default_provider="claude",
    )

    classification = ClassificationResult(
        intent="complex",
        confidence=0.9,
        suggested_llm="claude",
        rationale="test",
    )

    result = await router.route(
        message="Anything",
        classification=classification,
        conversation_history=[],
    )

    assert result.provider == "fallback"
    assert result.model == "none"
    assert "죄송합니다" in result.text


@pytest.mark.asyncio
async def test_complaint_uses_complaint_prompt(classification_complaint):
    """Complaint classification should use COMPLAINT_SYSTEM_PROMPT."""
    claude_provider = MockProvider("claude", response_text="empathetic response")

    router = LLMRouter(
        providers={"claude": claude_provider},
        default_provider="claude",
    )

    await router.route(
        message="I am very unhappy with the service",
        classification=classification_complaint,
        conversation_history=[],
    )

    assert len(claude_provider.generate_calls) == 1
    call = claude_provider.generate_calls[0]
    assert call["system_prompt"] == COMPLAINT_SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_non_complaint_uses_consultation_prompt(classification_complex):
    """Non-complaint intents should use CONSULTATION_SYSTEM_PROMPT."""
    claude_provider = MockProvider("claude", response_text="helpful response")

    router = LLMRouter(
        providers={"claude": claude_provider},
        default_provider="claude",
    )

    await router.route(
        message="What treatments do you offer?",
        classification=classification_complex,
        conversation_history=[],
    )

    assert len(claude_provider.generate_calls) == 1
    call = claude_provider.generate_calls[0]
    assert call["system_prompt"] == CONSULTATION_SYSTEM_PROMPT


@pytest.mark.asyncio
async def test_conversation_history_passed_through(classification_complex):
    """Router should pass conversation history to the provider."""
    claude_provider = MockProvider("claude")
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]

    router = LLMRouter(
        providers={"claude": claude_provider},
        default_provider="claude",
    )

    await router.route(
        message="Follow up question",
        classification=classification_complex,
        conversation_history=history,
    )

    call = claude_provider.generate_calls[0]
    assert call["conversation_history"] == history
    assert call["message"] == "Follow up question"


@pytest.mark.asyncio
async def test_null_suggested_llm_uses_default():
    """When suggested_llm is None, router should use the default provider."""
    claude_provider = MockProvider("claude", response_text="default response")

    router = LLMRouter(
        providers={"claude": claude_provider},
        default_provider="claude",
    )

    classification = ClassificationResult(
        intent="faq",
        confidence=0.95,
        suggested_llm=None,
        rationale="template answer",
    )

    result = await router.route(
        message="What are your hours?",
        classification=classification,
        conversation_history=[],
    )

    assert result.provider == "claude"
    assert result.text == "default response"
