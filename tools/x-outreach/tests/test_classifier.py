"""Tests for the 5-category tweet classifier."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from src.ai.classifier import VALID_INTENTS, ClassificationResult, TweetClassifier


class TestClassificationResult:
    """Test the ClassificationResult dataclass."""

    def test_actionable_when_llm_decision_true(self) -> None:
        r = ClassificationResult(
            intent_type="hospital",
            confidence=0.9,
            rationale="Genuine user",
            llm_decision=True,
        )
        assert r.is_actionable

    def test_not_actionable_when_llm_decision_false(self) -> None:
        r = ClassificationResult(
            intent_type="hospital",
            confidence=0.9,
            rationale="Marketing account",
            llm_decision=False,
        )
        assert not r.is_actionable

    def test_backward_compat_classification(self) -> None:
        r = ClassificationResult(
            intent_type="price",
            confidence=0.8,
            rationale="",
            llm_decision=True,
        )
        assert r.classification == "price"

    def test_backward_compat_template_category(self) -> None:
        r = ClassificationResult(
            intent_type="procedure",
            confidence=0.8,
            rationale="",
            llm_decision=True,
        )
        assert r.template_category == "procedure"

    def test_template_category_none_when_rejected(self) -> None:
        r = ClassificationResult(
            intent_type="procedure",
            confidence=0.8,
            rationale="",
            llm_decision=False,
        )
        assert r.template_category is None

    def test_keyword_intent_stored(self) -> None:
        r = ClassificationResult(
            intent_type="price",
            confidence=0.9,
            rationale="",
            llm_decision=True,
            keyword_intent="price",
        )
        assert r.keyword_intent == "price"


class TestValidIntents:
    """Test intent category constants."""

    def test_five_categories(self) -> None:
        assert len(VALID_INTENTS) == 5

    def test_expected_categories(self) -> None:
        assert VALID_INTENTS == {"hospital", "price", "procedure", "complaint", "review"}


class TestTweetClassifier:
    """Test the TweetClassifier with mocked LLM."""

    @pytest.fixture
    def mock_llm_response(self):
        """Create a mock LLM response factory."""

        def _make(data: dict):
            from outreach_shared.ai.llm_client import LLMResponse

            return LLMResponse(text=json.dumps(data), model="test")

        return _make

    @pytest.fixture
    def classifier(self):
        """Create a classifier with mocked LLM client."""
        with patch("src.ai.classifier.create_llm_client") as mock_create:
            mock_client = AsyncMock()
            mock_create.return_value = mock_client
            c = TweetClassifier(
                api_key="test-key",
                model="test-model",
                confidence_threshold=0.7,
                domain_context="test context",
            )
            c._mock_client = mock_client
            return c

    @pytest.mark.asyncio
    async def test_exclude_keyword_skips_llm(self, classifier) -> None:
        """Tweets with exclude keywords should not call the LLM."""
        result = await classifier.classify(
            tweet_content="キャンペーン実施中！ボトックス50%OFF",
            author_username="clinic_bot",
        )
        assert not result.is_actionable
        assert not result.llm_decision
        # LLM should not have been called
        classifier._mock_client.generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_llm_classification_hospital(self, classifier, mock_llm_response) -> None:
        classifier._mock_client.generate = AsyncMock(
            return_value=mock_llm_response(
                {
                    "intent_type": "hospital",
                    "confidence": 0.9,
                    "llm_decision": True,
                    "rationale": "User asking for clinic recommendation",
                }
            )
        )
        result = await classifier.classify(
            tweet_content="韓国の皮膚科どこがいい？",
            author_username="user_a",
            author_bio="東京在住",
            follower_count=200,
        )
        assert result.intent_type == "hospital"
        assert result.confidence == 0.9
        assert result.llm_decision is True
        assert result.is_actionable

    @pytest.mark.asyncio
    async def test_low_confidence_rejected(self, classifier, mock_llm_response) -> None:
        classifier._mock_client.generate = AsyncMock(
            return_value=mock_llm_response(
                {
                    "intent_type": "price",
                    "confidence": 0.4,
                    "llm_decision": True,
                    "rationale": "Ambiguous",
                }
            )
        )
        result = await classifier.classify(
            tweet_content="何か安いもの探してる",
            author_username="user_b",
        )
        assert result.confidence == 0.4
        assert not result.llm_decision
        assert not result.is_actionable

    @pytest.mark.asyncio
    async def test_invalid_intent_defaults_to_review(self, classifier, mock_llm_response) -> None:
        classifier._mock_client.generate = AsyncMock(
            return_value=mock_llm_response(
                {
                    "intent_type": "unknown_category",
                    "confidence": 0.9,
                    "llm_decision": True,
                    "rationale": "test",
                }
            )
        )
        result = await classifier.classify(
            tweet_content="テスト",
            author_username="user_c",
        )
        assert result.intent_type == "review"

    @pytest.mark.asyncio
    async def test_malformed_json_handled(self, classifier) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        classifier._mock_client.generate = AsyncMock(
            return_value=LLMResponse(text="not valid json{{{", model="test")
        )
        result = await classifier.classify(
            tweet_content="テスト",
            author_username="user_d",
        )
        assert not result.is_actionable
        assert result.confidence == 0.0

    @pytest.mark.asyncio
    async def test_llm_error_handled(self, classifier) -> None:
        classifier._mock_client.generate = AsyncMock(side_effect=RuntimeError("API down"))
        result = await classifier.classify(
            tweet_content="ボトックス打ちたい",
            author_username="user_e",
        )
        assert not result.is_actionable
        assert result.confidence == 0.0
        assert "API down" in result.rationale

    @pytest.mark.asyncio
    async def test_keyword_intent_passed_through(self, classifier, mock_llm_response) -> None:
        """When keyword pre-filter matches, the keyword_intent should be set."""
        classifier._mock_client.generate = AsyncMock(
            return_value=mock_llm_response(
                {
                    "intent_type": "procedure",
                    "confidence": 0.85,
                    "llm_decision": True,
                    "rationale": "Procedure experience",
                }
            )
        )
        result = await classifier.classify(
            tweet_content="ボトックス打ってきた！めっちゃ良かった",
            author_username="user_f",
        )
        assert result.intent_type == "procedure"
        assert result.keyword_intent == "procedure"

    @pytest.mark.asyncio
    async def test_markdown_wrapped_json_parsed(self, classifier) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        json_text = json.dumps(
            {
                "intent_type": "complaint",
                "confidence": 0.8,
                "llm_decision": True,
                "rationale": "Negative experience",
            }
        )
        wrapped = f"```json\n{json_text}\n```"
        classifier._mock_client.generate = AsyncMock(
            return_value=LLMResponse(text=wrapped, model="test")
        )
        result = await classifier.classify(
            tweet_content="施術失敗した…",
            author_username="user_g",
        )
        assert result.intent_type == "complaint"
        assert result.llm_decision is True

    @pytest.mark.asyncio
    async def test_confidence_clamped(self, classifier, mock_llm_response) -> None:
        classifier._mock_client.generate = AsyncMock(
            return_value=mock_llm_response(
                {
                    "intent_type": "review",
                    "confidence": 1.5,
                    "llm_decision": True,
                    "rationale": "test",
                }
            )
        )
        result = await classifier.classify(
            tweet_content="行ってきた",
            author_username="user_h",
        )
        assert result.confidence == 1.0
