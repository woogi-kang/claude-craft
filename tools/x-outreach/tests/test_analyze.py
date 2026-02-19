"""Tests for the analyze pipeline and classifier."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai.classifier import ClassificationResult, TweetClassifier
from src.db.repository import Repository
from src.pipeline.analyze import AnalyzePipeline


class TestClassificationResult:
    """Test the ClassificationResult dataclass."""

    def test_is_actionable_needs_help(self) -> None:
        r = ClassificationResult(
            classification="needs_help",
            confidence=0.9,
            rationale="test",
            template_category="D",
        )
        assert r.is_actionable is True

    def test_is_actionable_seeking_info(self) -> None:
        r = ClassificationResult(
            classification="seeking_info",
            confidence=0.8,
            rationale="test",
            template_category="B",
        )
        assert r.is_actionable is True

    def test_is_actionable_irrelevant(self) -> None:
        r = ClassificationResult(
            classification="irrelevant",
            confidence=0.95,
            rationale="test",
            template_category=None,
        )
        assert r.is_actionable is False


class TestTweetClassifierParsing:
    """Test the classifier's response parsing."""

    def _make_classifier(self) -> TweetClassifier:
        return TweetClassifier(
            api_key="test-key",
            model="test-model",
            confidence_threshold=0.7,
        )

    def test_parse_valid_json(self) -> None:
        clf = self._make_classifier()
        result = clf._parse_response(
            json.dumps(
                {
                    "classification": "needs_help",
                    "confidence": 0.85,
                    "rationale": "User reports bad experience",
                    "template_category": "D",
                }
            )
        )
        assert result.classification == "needs_help"
        assert result.confidence == 0.85
        assert result.template_category == "D"

    def test_parse_with_markdown_fences(self) -> None:
        clf = self._make_classifier()
        raw = '```json\n{"classification":"seeking_info","confidence":0.9,"rationale":"Asking","template_category":"B"}\n```'
        result = clf._parse_response(raw)
        assert result.classification == "seeking_info"
        assert result.confidence == 0.9

    def test_parse_invalid_json(self) -> None:
        clf = self._make_classifier()
        result = clf._parse_response("not json at all")
        assert result.classification == "irrelevant"
        assert result.confidence == 0.0

    def test_parse_unknown_classification(self) -> None:
        clf = self._make_classifier()
        result = clf._parse_response(
            json.dumps(
                {
                    "classification": "unknown_category",
                    "confidence": 0.5,
                    "rationale": "",
                    "template_category": None,
                }
            )
        )
        assert result.classification == "irrelevant"

    def test_parse_clamps_confidence(self) -> None:
        clf = self._make_classifier()
        result = clf._parse_response(
            json.dumps(
                {
                    "classification": "needs_help",
                    "confidence": 1.5,
                    "rationale": "",
                    "template_category": "A",
                }
            )
        )
        assert result.confidence == 1.0


class TestTweetClassifierClassify:
    """Test the classifier's classify method with mocked API."""

    @pytest.mark.asyncio
    async def test_classify_success(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = json.dumps(
            {
                "classification": "seeking_info",
                "confidence": 0.85,
                "rationale": "User asking for recommendations",
                "template_category": "B",
            }
        )
        mock_response.content = [mock_content]

        clf._client = AsyncMock()
        clf._client.messages.create = AsyncMock(return_value=mock_response)

        result = await clf.classify(
            tweet_content="韓国のクリニックおすすめある？",
            author_username="test_user",
        )

        assert result.classification == "seeking_info"
        assert result.confidence == 0.85

    @pytest.mark.asyncio
    async def test_classify_low_confidence_forced_irrelevant(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        mock_response = MagicMock()
        mock_content = MagicMock()
        mock_content.text = json.dumps(
            {
                "classification": "seeking_info",
                "confidence": 0.5,
                "rationale": "Ambiguous content",
                "template_category": "B",
            }
        )
        mock_response.content = [mock_content]

        clf._client = AsyncMock()
        clf._client.messages.create = AsyncMock(return_value=mock_response)

        result = await clf.classify(
            tweet_content="韓国いいよね",
            author_username="test_user",
        )

        assert result.classification == "irrelevant"
        assert result.confidence == 0.5

    @pytest.mark.asyncio
    async def test_classify_api_error(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        clf._client = AsyncMock()
        clf._client.messages.create = AsyncMock(side_effect=Exception("API error"))

        result = await clf.classify(
            tweet_content="test",
            author_username="test_user",
        )

        assert result.classification == "irrelevant"
        assert result.confidence == 0.0


class TestAnalyzePipeline:
    """Test the analyze pipeline with mocked classifier."""

    @pytest.mark.asyncio
    async def test_analyze_processes_collected_tweets(
        self, tmp_db: Repository
    ) -> None:
        # Insert test tweets
        tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "韓国のクリニックどこがいい？",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
                "status": "collected",
            }
        )
        tmp_db.insert_tweet(
            {
                "tweet_id": "t2",
                "content": "ボトックス失敗した…",
                "author_username": "user2",
                "tweet_timestamp": "2026-02-19T11:00:00Z",
                "status": "collected",
            }
        )

        mock_classifier = AsyncMock(spec=TweetClassifier)
        mock_classifier.classify = AsyncMock(
            side_effect=[
                ClassificationResult(
                    classification="seeking_info",
                    confidence=0.9,
                    rationale="Asking for recommendations",
                    template_category="B",
                ),
                ClassificationResult(
                    classification="needs_help",
                    confidence=0.85,
                    rationale="Bad experience reported",
                    template_category="D",
                ),
            ]
        )

        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(tmp_db)

        assert result.total_processed == 2
        assert result.seeking_info == 1
        assert result.needs_help == 1
        assert result.irrelevant == 0
        assert result.errors == 0

        # Verify DB was updated
        # Tweets are processed in DESC timestamp order: t2 (11:00) first, t1 (10:00) second.
        # So t2 gets "seeking_info" and t1 gets "needs_help".
        t1 = tmp_db.get_tweet_by_id("t1")
        assert t1 is not None
        assert t1["status"] == "analyzed"
        assert t1["classification"] == "needs_help"

        t2 = tmp_db.get_tweet_by_id("t2")
        assert t2 is not None
        assert t2["status"] == "analyzed"
        assert t2["classification"] == "seeking_info"

    @pytest.mark.asyncio
    async def test_analyze_no_tweets(self, tmp_db: Repository) -> None:
        mock_classifier = AsyncMock(spec=TweetClassifier)
        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(tmp_db)
        assert result.total_processed == 0

    @pytest.mark.asyncio
    async def test_analyze_handles_classifier_error(
        self, tmp_db: Repository
    ) -> None:
        tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "test",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
                "status": "collected",
            }
        )

        mock_classifier = AsyncMock(spec=TweetClassifier)
        mock_classifier.classify = AsyncMock(side_effect=Exception("API down"))

        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(tmp_db)

        assert result.errors == 1
        assert result.total_processed == 0
