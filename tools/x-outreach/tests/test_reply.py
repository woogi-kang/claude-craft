"""Tests for the reply pipeline (tweet replies via Playwright)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai.content_gen import ContentGenerationError
from src.pipeline.reply import (
    ReplyPipeline,
    ReplyRateLimitError,
    ReplyResult,
    _build_treatment_context,
    _post_reply_via_playwright,
)

# =========================================================================
# ReplyResult
# =========================================================================


class TestReplyResult:
    """Test ReplyResult dataclass defaults."""

    def test_defaults(self) -> None:
        result = ReplyResult()
        assert result.total_candidates == 0
        assert result.replies_sent == 0
        assert result.skipped_quiet_hours == 0
        assert result.skipped_daily_limit == 0
        assert result.skipped_max_thread == 0
        assert result.skipped_interval == 0
        assert result.errors == 0
        assert result.emergency_halt is False
        assert result.error_details == []


# =========================================================================
# Helpers
# =========================================================================


def _make_repo(
    tweets: list[dict] | None = None,
    thread_count: int = 0,
) -> MagicMock:
    """Build a mock repository with configurable behaviour."""
    repo = MagicMock()
    repo.get_tweets_by_status.return_value = tweets or []
    repo.count_user_replies.return_value = thread_count
    repo.update_tweet_status.return_value = True
    return repo


def _make_tracker() -> MagicMock:
    """Build a mock action tracker."""
    return MagicMock()


def _make_settings(
    start_hour: int = 8,
    end_hour: int = 23,
) -> MagicMock:
    """Build a mock Settings with daemon active hours."""
    settings = MagicMock()
    settings.daemon.active_start_hour = start_hour
    settings.daemon.active_end_hour = end_hour
    return settings


def _make_content_gen(reply_text: str = "テストリプライ") -> MagicMock:
    """Build a mock ContentGenerator."""
    gen = MagicMock()
    gen.generate_reply = AsyncMock(return_value=reply_text)
    return gen


def _analyzed_tweet(
    tweet_id: str = "t1",
    username: str = "user_a",
    llm_decision: bool = True,
    intent_type: str = "hospital",
    contents: str = "test tweet",
) -> dict:
    """Create a minimal analyzed tweet dict."""
    return {
        "post_id": tweet_id,
        "username": username,
        "llm_decision": llm_decision,
        "intent_type": intent_type,
        "contents": contents,
        "post_url": f"https://x.com/{username}/status/{tweet_id}",
    }


# =========================================================================
# ReplyPipeline
# =========================================================================


class TestReplyPipeline:
    """Test ReplyPipeline with mocked dependencies."""

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=False)
    async def test_skips_quiet_hours(self, _mock_hours: MagicMock) -> None:
        """When is_active_hours returns False the pipeline returns early."""
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        repo = _make_repo()
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        # Returns early -- no candidates fetched, no skipped_quiet_hours counter
        assert result.replies_sent == 0
        assert result.total_candidates == 0
        repo.get_tweets_by_status.assert_not_called()

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    async def test_no_candidates(self, _mock_hours: MagicMock) -> None:
        """Empty tweet list results in total_candidates=0."""
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=[])
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        assert result.total_candidates == 0
        assert result.replies_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    async def test_filters_non_actionable(self, _mock_hours: MagicMock) -> None:
        """Tweets with llm_decision=False are filtered out."""
        tweets = [_analyzed_tweet(llm_decision=False)]
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=tweets)
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        assert result.total_candidates == 0
        assert result.replies_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._post_reply_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_reply_success(
        self,
        _mock_ctx: MagicMock,
        mock_post: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """Happy path: content generated, playwright posts, DB updated, tracker called."""
        mock_post.return_value = True
        reply_text = "テストリプライ"
        content_gen = _make_content_gen(reply_text)
        tweets = [_analyzed_tweet()]
        pipeline = ReplyPipeline(
            content_gen=content_gen,
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=tweets)
        tracker = _make_tracker()
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, tracker, _make_settings())

        assert result.replies_sent == 1
        assert result.errors == 0
        assert result.total_candidates == 1
        mock_post.assert_called_once_with(ctx, "https://x.com/user_a/status/t1", reply_text)
        tracker.record_reply.assert_called_once_with("t1", "user_a", persona_id=None)
        repo.update_tweet_status.assert_called_once()

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_skips_daily_limit(
        self,
        _mock_ctx: MagicMock,
        _mock_hours: MagicMock,
    ) -> None:
        """SlidingWindowLimiter(max_actions=0) causes daily limit skip."""
        from outreach_shared.utils.rate_limiter import SlidingWindowLimiter

        limiter = SlidingWindowLimiter(max_actions=0, window_seconds=86_400.0)
        tweets = [_analyzed_tweet()]
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            daily_limiter=limiter,
        )
        repo = _make_repo(tweets=tweets)
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        assert result.skipped_daily_limit == 1
        assert result.replies_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_skips_max_thread(
        self,
        _mock_ctx: MagicMock,
        _mock_hours: MagicMock,
    ) -> None:
        """When count_user_replies >= max_thread_replies, the tweet is skipped."""
        tweets = [_analyzed_tweet()]
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            max_thread_replies=3,
        )
        repo = _make_repo(tweets=tweets, thread_count=3)
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        assert result.skipped_max_thread == 1
        assert result.replies_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_content_generation_error(
        self,
        _mock_ctx: MagicMock,
        _mock_hours: MagicMock,
    ) -> None:
        """ContentGenerationError increments errors and continues."""
        gen = MagicMock()
        gen.generate_reply = AsyncMock(side_effect=ContentGenerationError("API down"))
        tweets = [_analyzed_tweet()]
        pipeline = ReplyPipeline(
            content_gen=gen,
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=tweets)
        tracker = _make_tracker()
        result = await pipeline.run(repo, MagicMock(), tracker, _make_settings())
        assert result.errors == 1
        assert result.replies_sent == 0
        tracker.record_error.assert_called_once()

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._post_reply_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_emergency_halt_on_rate_limit(
        self,
        _mock_ctx: MagicMock,
        mock_post: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """ReplyRateLimitError sets emergency_halt=True and breaks the loop."""
        mock_post.side_effect = ReplyRateLimitError("restricted")
        tweets = [
            _analyzed_tweet(tweet_id="t1"),
            _analyzed_tweet(tweet_id="t2", username="user_b"),
        ]
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=tweets)
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())
        assert result.emergency_halt is True
        assert result.errors == 1
        # Should stop after first tweet (not process second candidate)
        assert mock_post.call_count == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.is_active_hours", return_value=True)
    @patch("src.pipeline.reply._post_reply_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.reply._build_treatment_context", return_value="")
    async def test_playwright_failure(
        self,
        _mock_ctx: MagicMock,
        mock_post: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """A generic exception from Playwright increments errors and continues."""
        mock_post.side_effect = RuntimeError("browser crashed")
        tweets = [_analyzed_tweet()]
        pipeline = ReplyPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        repo = _make_repo(tweets=tweets)
        tracker = _make_tracker()
        result = await pipeline.run(repo, MagicMock(), tracker, _make_settings())
        assert result.errors == 1
        assert result.replies_sent == 0
        tracker.record_error.assert_called_once()


# =========================================================================
# _build_treatment_context
# =========================================================================


class TestBuildTreatmentContext:
    """Test treatment context builder."""

    def test_with_matching_treatment(self) -> None:
        """Tweet containing a known Japanese term returns context string."""
        kb = MagicMock()
        info = MagicMock()
        info.korean_name = "보톡스"
        info.average_price = "3만원~25만원"
        info.downtime = "없음"
        info.duration = "3-6개월"
        kb.lookup_by_japanese.return_value = info

        with patch(
            "src.knowledge.treatments.JAPANESE_TO_KOREAN",
            {"ボトックス": "보톡스"},
        ):
            result = _build_treatment_context("ボトックスを打ちたい", kb)

        assert "ボトックス" in result
        assert "보톡스" in result
        assert "3만원~25만원" in result
        kb.lookup_by_japanese.assert_called_once_with("ボトックス")

    def test_no_matching_treatment(self) -> None:
        """Tweet without known treatment terms returns empty string."""
        kb = MagicMock()
        kb.lookup_by_japanese.return_value = None

        with patch(
            "src.knowledge.treatments.JAPANESE_TO_KOREAN",
            {"ボトックス": "보톡스"},
        ):
            result = _build_treatment_context("韓国旅行楽しかった", kb)

        assert result == ""
        kb.lookup_by_japanese.assert_not_called()


# =========================================================================
# _post_reply_via_playwright
# =========================================================================


class TestPostReplyViaPlaywright:
    """Test the Playwright reply helper."""

    @pytest.mark.asyncio
    async def test_no_url_returns_false(self) -> None:
        """Empty tweet_url returns False immediately."""
        ctx = MagicMock()
        result = await _post_reply_via_playwright(ctx, "", "reply text")
        assert result is False

    @pytest.mark.asyncio
    @patch("src.pipeline.reply.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.reply.random_mouse_move", new_callable=AsyncMock)
    @patch("src.pipeline.reply.detect_restriction", return_value=True)
    async def test_rate_limit_detected_raises(
        self,
        _mock_detect: MagicMock,
        _mock_mouse: AsyncMock,
        _mock_pause: AsyncMock,
    ) -> None:
        """When detect_restriction returns True, ReplyRateLimitError is raised."""
        page = AsyncMock()
        page.content = AsyncMock(return_value="rate limit page content")
        ctx = MagicMock()
        ctx.pages = [page]

        with pytest.raises(ReplyRateLimitError):
            await _post_reply_via_playwright(ctx, "https://x.com/user/status/123", "reply text")
