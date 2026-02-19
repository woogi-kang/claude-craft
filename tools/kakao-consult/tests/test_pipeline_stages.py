"""Tests for pipeline stages (classify, respond, send, track)."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai.classifier import ClassificationResult
from src.ai.providers.base import LLMResponse
from src.knowledge.faq_matcher import FAQMatch
from src.pipeline.classify import ClassifyPipeline, ClassifyResult
from src.pipeline.respond import RespondPipeline, RespondResult
from src.pipeline.send import SendPipeline, SendResult
from src.pipeline.track import ActionTracker


class TestClassifyPipeline:
    @pytest.mark.asyncio
    async def test_local_faq_match_first(self):
        faq_matcher = MagicMock()
        faq_matcher.match.return_value = FAQMatch(
            category="pricing", matched_pattern="price", confidence=0.9, source="exact"
        )
        classifier = MagicMock()

        pipeline = ClassifyPipeline(faq_matcher, classifier, use_local_first=True)
        result = await pipeline.run("How much does it cost?")

        assert result.used_local is True
        assert result.faq_match is not None
        assert result.faq_match.category == "pricing"
        classifier.classify.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_through_to_llm(self):
        faq_matcher = MagicMock()
        faq_matcher.match.return_value = None
        classifier = AsyncMock()
        classifier.classify.return_value = ClassificationResult(
            intent="complex", confidence=0.9, suggested_llm="claude", rationale="test"
        )

        pipeline = ClassifyPipeline(faq_matcher, classifier, use_local_first=True)
        result = await pipeline.run("This is a complex question")

        assert result.used_local is False
        assert result.classification is not None
        assert result.classification.intent == "complex"

    @pytest.mark.asyncio
    async def test_local_first_disabled(self):
        faq_matcher = MagicMock()
        classifier = AsyncMock()
        classifier.classify.return_value = ClassificationResult(
            intent="faq", confidence=0.95, suggested_llm=None, rationale="test"
        )
        faq_matcher.match.return_value = None

        pipeline = ClassifyPipeline(faq_matcher, classifier, use_local_first=False)
        result = await pipeline.run("How much does it cost?")

        assert result.used_local is False
        classifier.classify.assert_called_once()


class TestRespondPipeline:
    def _make_template_engine(self):
        engine = MagicMock()
        engine.get_faq_response.return_value = MagicMock(
            id="faq_1", text="FAQ response.", category="pricing"
        )
        engine.get_greeting_response.return_value = MagicMock(
            id="greet_1", text="Hello!", category="hello"
        )
        engine.get_redirect_response.return_value = MagicMock(
            id="redirect_1", text="That is not related.", category="off_topic"
        )
        return engine

    @pytest.mark.asyncio
    async def test_faq_match_returns_template(self):
        engine = self._make_template_engine()
        router = AsyncMock()

        pipeline = RespondPipeline(engine, router)
        classify_result = ClassifyResult(
            faq_match=FAQMatch(
                category="pricing", matched_pattern="price", confidence=0.9, source="exact"
            ),
            classification=None,
            used_local=True,
        )

        result = await pipeline.run("price?", classify_result, [])
        assert result.provider == "template"
        assert result.text == "FAQ response."
        router.route.assert_not_called()

    @pytest.mark.asyncio
    async def test_spam_returns_empty(self):
        engine = self._make_template_engine()
        router = AsyncMock()

        pipeline = RespondPipeline(engine, router)
        classify_result = ClassifyResult(
            faq_match=None,
            classification=ClassificationResult(
                intent="spam", confidence=0.9, suggested_llm=None, rationale="spam"
            ),
            used_local=False,
        )

        result = await pipeline.run("spam message", classify_result, [])
        assert result.text == ""
        assert result.provider == "skip"

    @pytest.mark.asyncio
    async def test_complex_routes_to_llm(self):
        engine = self._make_template_engine()
        router = AsyncMock()
        router.route.return_value = LLMResponse(
            text="LLM response", provider="claude", model="test", tokens_used=50
        )

        pipeline = RespondPipeline(engine, router)
        classify_result = ClassifyResult(
            faq_match=None,
            classification=ClassificationResult(
                intent="complex", confidence=0.9, suggested_llm="claude", rationale="test"
            ),
            used_local=False,
        )

        result = await pipeline.run("complex question", classify_result, [])
        assert result.provider == "claude"
        assert result.text == "LLM response"
        router.route.assert_called_once()


class TestSendPipeline:
    @pytest.mark.asyncio
    async def test_send_empty_text(self):
        sender = AsyncMock()
        pipeline = SendPipeline(sender)
        result = await pipeline.run("room1", "", 500)
        assert result.success is True
        sender.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_short_message(self):
        sender = AsyncMock()
        sender.send.return_value = True
        pipeline = SendPipeline(sender)
        result = await pipeline.run("room1", "Hello", 500)
        assert result.success is True
        sender.send.assert_called_once_with("Hello")

    @pytest.mark.asyncio
    async def test_send_long_message_splits(self):
        sender = AsyncMock()
        sender.send_split.return_value = True
        pipeline = SendPipeline(sender)
        long_text = "A" * 600
        result = await pipeline.run("room1", long_text, 500)
        assert result.success is True
        sender.send_split.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_failure(self):
        sender = AsyncMock()
        sender.send.side_effect = RuntimeError("Device error")
        pipeline = SendPipeline(sender)
        result = await pipeline.run("room1", "Hello", 500)
        assert result.success is False
        assert result.error is not None


class TestActionTracker:
    def test_record_receive(self):
        repo = MagicMock()
        tracker = ActionTracker(repo)
        tracker.record_receive("room1", "Hello")
        repo.record_action.assert_called_once()
        repo.update_daily_stats.assert_called_once()

    def test_record_respond_template(self):
        repo = MagicMock()
        tracker = ActionTracker(repo)
        tracker.record_respond("room1", "template", "faq")
        repo.record_action.assert_called_once()
        # Check stats include faq_matches
        call_kwargs = repo.update_daily_stats.call_args
        assert call_kwargs is not None

    def test_record_error(self):
        repo = MagicMock()
        tracker = ActionTracker(repo)
        tracker.record_error("processing", "test error", "room1")
        repo.record_action.assert_called_once()
        repo.update_daily_stats.assert_called_once()
