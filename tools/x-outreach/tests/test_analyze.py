"""Tests for the analyze pipeline and classifier."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai.classifier import ClassificationResult, TweetClassifier
from src.ai.keywords import KeywordMatch
from src.pipeline.analyze import AnalyzePipeline


class TestClassificationResult:
    """Test the ClassificationResult dataclass."""

    def test_is_actionable_approved(self) -> None:
        r = ClassificationResult(
            intent_type="hospital",
            confidence=0.9,
            rationale="test",
            llm_decision=True,
        )
        assert r.is_actionable is True

    def test_is_actionable_rejected(self) -> None:
        r = ClassificationResult(
            intent_type="review",
            confidence=0.8,
            rationale="test",
            llm_decision=False,
        )
        assert r.is_actionable is False

    def test_backward_compat_classification(self) -> None:
        r = ClassificationResult(
            intent_type="price",
            confidence=0.85,
            rationale="test",
            llm_decision=True,
        )
        assert r.classification == "price"

    def test_backward_compat_template_category_approved(self) -> None:
        r = ClassificationResult(
            intent_type="procedure",
            confidence=0.85,
            rationale="test",
            llm_decision=True,
        )
        assert r.template_category == "procedure"

    def test_backward_compat_template_category_rejected(self) -> None:
        r = ClassificationResult(
            intent_type="complaint",
            confidence=0.85,
            rationale="test",
            llm_decision=False,
        )
        assert r.template_category is None

    def test_keyword_intent_stored(self) -> None:
        r = ClassificationResult(
            intent_type="hospital",
            confidence=0.9,
            rationale="test",
            llm_decision=True,
            keyword_intent="hospital",
        )
        assert r.keyword_intent == "hospital"


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
        kw_match = KeywordMatch(matched=False)
        result = clf._parse_response(
            json.dumps(
                {
                    "intent_type": "hospital",
                    "confidence": 0.85,
                    "rationale": "User looking for clinic",
                    "llm_decision": True,
                }
            ),
            kw_match,
        )
        assert result.intent_type == "hospital"
        assert result.confidence == 0.85
        assert result.llm_decision is True

    def test_parse_with_markdown_fences(self) -> None:
        clf = self._make_classifier()
        kw_match = KeywordMatch(matched=False)
        raw = (
            '```json\n{"intent_type":"price","confidence":0.9,'
            '"rationale":"Asking cost","llm_decision":true}\n```'
        )
        result = clf._parse_response(raw, kw_match)
        assert result.intent_type == "price"
        assert result.confidence == 0.9

    def test_parse_invalid_json(self) -> None:
        clf = self._make_classifier()
        kw_match = KeywordMatch(matched=False)
        result = clf._parse_response("not json at all", kw_match)
        assert result.intent_type == "review"  # default fallback
        assert result.confidence == 0.0
        assert result.llm_decision is False

    def test_parse_unknown_intent_type(self) -> None:
        clf = self._make_classifier()
        kw_match = KeywordMatch(matched=False)
        result = clf._parse_response(
            json.dumps(
                {
                    "intent_type": "unknown_category",
                    "confidence": 0.5,
                    "rationale": "",
                    "llm_decision": False,
                }
            ),
            kw_match,
        )
        assert result.intent_type == "review"  # invalid types fall back to review

    def test_parse_clamps_confidence(self) -> None:
        clf = self._make_classifier()
        kw_match = KeywordMatch(matched=False)
        result = clf._parse_response(
            json.dumps(
                {
                    "intent_type": "hospital",
                    "confidence": 1.5,
                    "rationale": "",
                    "llm_decision": True,
                }
            ),
            kw_match,
        )
        assert result.confidence == 1.0

    def test_parse_preserves_keyword_intent(self) -> None:
        clf = self._make_classifier()
        kw_match = KeywordMatch(matched=True, category="procedure", keyword="ボトックス")
        result = clf._parse_response(
            json.dumps(
                {
                    "intent_type": "procedure",
                    "confidence": 0.9,
                    "rationale": "Procedure discussion",
                    "llm_decision": True,
                }
            ),
            kw_match,
        )
        assert result.keyword_intent == "procedure"


class TestTweetClassifierClassify:
    """Test the classifier's classify method with mocked LLM."""

    @pytest.mark.asyncio
    async def test_classify_success(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        mock_response = MagicMock()
        mock_response.text = json.dumps(
            {
                "intent_type": "hospital",
                "confidence": 0.85,
                "rationale": "User asking for recommendations",
                "llm_decision": True,
            }
        )

        clf._llm = AsyncMock()
        clf._llm.generate = AsyncMock(return_value=mock_response)

        result = await clf.classify(
            tweet_content="韓国のクリニックおすすめある？",
            author_username="test_user",
        )

        assert result.intent_type == "hospital"
        assert result.confidence == 0.85
        assert result.llm_decision is True

    @pytest.mark.asyncio
    async def test_classify_low_confidence_rejects(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        mock_response = MagicMock()
        mock_response.text = json.dumps(
            {
                "intent_type": "price",
                "confidence": 0.5,
                "rationale": "Ambiguous content",
                "llm_decision": True,
            }
        )

        clf._llm = AsyncMock()
        clf._llm.generate = AsyncMock(return_value=mock_response)

        result = await clf.classify(
            tweet_content="韓国いいよね",
            author_username="test_user",
        )

        # Low confidence forces llm_decision=False
        assert result.llm_decision is False
        assert result.confidence == 0.5

    @pytest.mark.asyncio
    async def test_classify_api_error(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        clf._llm = AsyncMock()
        clf._llm.generate = AsyncMock(side_effect=Exception("API error"))

        result = await clf.classify(
            tweet_content="test",
            author_username="test_user",
        )

        assert result.llm_decision is False
        assert result.confidence == 0.0

    @pytest.mark.asyncio
    async def test_classify_excluded_keyword(self) -> None:
        clf = TweetClassifier(
            api_key="test",
            model="test",
            confidence_threshold=0.7,
        )

        clf._llm = AsyncMock()

        result = await clf.classify(
            tweet_content="キャンペーン実施中！ボトックス50%OFF",
            author_username="clinic_account",
        )

        assert result.llm_decision is False
        assert result.confidence == 1.0
        # LLM should NOT have been called
        clf._llm.generate.assert_not_called()


class TestAnalyzePipeline:
    """Test the analyze pipeline with mocked classifier and repository."""

    @pytest.mark.asyncio
    async def test_analyze_processes_collected_tweets(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_tweets_by_status.return_value = [
            {
                "post_id": "t1",
                "contents": "韓国のクリニックどこがいい？",
                "username": "user1",
                "author_bio": "",
                "author_followers": 100,
                "likes_count": 2,
                "retweets_count": 0,
                "comments_count": 1,
            },
            {
                "post_id": "t2",
                "contents": "ボトックス失敗した…",
                "username": "user2",
                "author_bio": "",
                "author_followers": 200,
                "likes_count": 5,
                "retweets_count": 1,
                "comments_count": 3,
            },
        ]

        mock_classifier = AsyncMock(spec=TweetClassifier)
        mock_classifier.classify = AsyncMock(
            side_effect=[
                ClassificationResult(
                    intent_type="hospital",
                    confidence=0.9,
                    rationale="Asking for recommendations",
                    llm_decision=True,
                ),
                ClassificationResult(
                    intent_type="complaint",
                    confidence=0.85,
                    rationale="Bad experience reported",
                    llm_decision=True,
                ),
            ]
        )

        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(mock_repo)

        assert result.total_processed == 2
        assert result.approved == 2
        assert result.rejected == 0
        assert result.errors == 0
        assert result.by_intent == {"hospital": 1, "complaint": 1}

        # Verify DB updates were called
        assert mock_repo.update_tweet_status.call_count == 2

    @pytest.mark.asyncio
    async def test_analyze_mixed_decisions(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_tweets_by_status.return_value = [
            {
                "post_id": "t1",
                "contents": "クリニックおすすめ？",
                "username": "user1",
                "author_bio": "",
                "author_followers": 50,
                "likes_count": 0,
                "retweets_count": 0,
                "comments_count": 0,
            },
            {
                "post_id": "t2",
                "contents": "random tweet",
                "username": "user2",
                "author_bio": "",
                "author_followers": 50000,
                "likes_count": 100,
                "retweets_count": 50,
                "comments_count": 30,
            },
        ]

        mock_classifier = AsyncMock(spec=TweetClassifier)
        mock_classifier.classify = AsyncMock(
            side_effect=[
                ClassificationResult(
                    intent_type="hospital",
                    confidence=0.9,
                    rationale="Genuine question",
                    llm_decision=True,
                ),
                ClassificationResult(
                    intent_type="review",
                    confidence=0.6,
                    rationale="Influencer account",
                    llm_decision=False,
                ),
            ]
        )

        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(mock_repo)

        assert result.total_processed == 2
        assert result.approved == 1
        assert result.rejected == 1

    @pytest.mark.asyncio
    async def test_analyze_no_tweets(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_tweets_by_status.return_value = []

        mock_classifier = AsyncMock(spec=TweetClassifier)
        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(mock_repo)
        assert result.total_processed == 0

    @pytest.mark.asyncio
    async def test_analyze_handles_classifier_error(self) -> None:
        mock_repo = MagicMock()
        mock_repo.get_tweets_by_status.return_value = [
            {
                "post_id": "t1",
                "contents": "test",
                "username": "user1",
                "author_bio": "",
                "author_followers": 0,
                "likes_count": 0,
                "retweets_count": 0,
                "comments_count": 0,
            },
        ]

        mock_classifier = AsyncMock(spec=TweetClassifier)
        mock_classifier.classify = AsyncMock(side_effect=Exception("API down"))

        pipeline = AnalyzePipeline(mock_classifier)
        result = await pipeline.run(mock_repo)

        assert result.errors == 1
        assert result.total_processed == 0
