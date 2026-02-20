"""Tests for the MessageClassifier with mocked Anthropic client."""

from __future__ import annotations

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai.classifier import ClassificationResult, MessageClassifier


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@dataclass
class _FakeTextBlock:
    text: str


@dataclass
class _FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class _FakeResponse:
    content: list[_FakeTextBlock]
    usage: _FakeUsage


def _make_classifier(
    threshold: float = 0.7,
    json_text: str | None = None,
    side_effect: Exception | None = None,
) -> MessageClassifier:
    """Create a MessageClassifier with an injected mock client.

    Parameters
    ----------
    threshold:
        Confidence threshold for classification.
    json_text:
        JSON text the mock Anthropic client should return.
    side_effect:
        Exception the mock client should raise instead of returning.
    """
    classifier = MessageClassifier(
        api_key="test-key",
        model="claude-sonnet-4-20250514",
        confidence_threshold=threshold,
    )

    mock_client = MagicMock()
    mock_client.messages.create = AsyncMock()
    if side_effect is not None:
        mock_client.messages.create.side_effect = side_effect
    elif json_text is not None:
        mock_client.messages.create.return_value = _FakeResponse(
            content=[_FakeTextBlock(text=json_text)],
            usage=_FakeUsage(input_tokens=50, output_tokens=30),
        )

    # Inject mock directly, bypassing lazy _ensure_client() import
    classifier._client = mock_client
    return classifier


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_classify_faq():
    """FAQ messages should be classified with null suggested_llm."""
    classifier = _make_classifier(
        json_text=(
            '{"intent": "faq", "confidence": 0.95, '
            '"suggested_llm": null, "rationale": "pricing question"}'
        ),
    )

    result = await classifier.classify("How much is botox?")

    assert isinstance(result, ClassificationResult)
    assert result.intent == "faq"
    assert result.confidence == 0.95
    assert result.suggested_llm is None
    assert result.rationale == "pricing question"


@pytest.mark.asyncio
async def test_classify_complex():
    """Complex messages should suggest Claude as the LLM."""
    classifier = _make_classifier(
        json_text=(
            '{"intent": "complex", "confidence": 0.88, '
            '"suggested_llm": "claude", "rationale": "medical question"}'
        ),
    )

    result = await classifier.classify("What are the side effects of retinol?")

    assert result.intent == "complex"
    assert result.confidence == 0.88
    assert result.suggested_llm == "claude"


@pytest.mark.asyncio
async def test_classify_with_markdown_code_block():
    """Classifier should handle markdown-wrapped JSON responses."""
    classifier = _make_classifier(
        json_text=(
            '```json\n{"intent": "greeting", "confidence": 0.99, '
            '"suggested_llm": null, "rationale": "hello"}\n```'
        ),
    )

    result = await classifier.classify("Hello!")

    assert result.intent == "greeting"
    assert result.confidence == 0.99


@pytest.mark.asyncio
async def test_low_confidence_fallback():
    """Below-threshold confidence should fall back to complex/claude."""
    classifier = _make_classifier(
        threshold=0.7,
        json_text=(
            '{"intent": "faq", "confidence": 0.4, '
            '"suggested_llm": null, "rationale": "unclear"}'
        ),
    )

    result = await classifier.classify("umm maybe botox?")

    assert result.intent == "complex"
    assert result.suggested_llm == "claude"
    assert result.confidence == 0.4


@pytest.mark.asyncio
async def test_classification_error_fallback():
    """On exception, classifier should return safe complex/claude default."""
    classifier = _make_classifier(side_effect=RuntimeError("API down"))

    result = await classifier.classify("anything")

    assert result.intent == "complex"
    assert result.confidence == 0.5
    assert result.suggested_llm == "claude"
    assert "Classification failed" in result.rationale
