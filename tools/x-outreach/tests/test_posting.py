"""Tests for the posting pipeline (casual tweets)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai.content_gen import ContentGenerationError
from src.pipeline.posting import (
    PostingPipeline,
    PostingRateLimitError,
    PostingResult,
    posting_probability,
)


# =========================================================================
# PostingResult
# =========================================================================


class TestPostingResult:
    """Test PostingResult dataclass defaults."""

    def test_defaults(self) -> None:
        result = PostingResult()
        assert result.posts_published == 0
        assert result.skipped_quiet_hours == 0
        assert result.skipped_daily_limit == 0
        assert result.skipped_cooldown == 0
        assert result.errors == 0
        assert result.emergency_halt is False
        assert result.error_details == []


# =========================================================================
# posting_probability
# =========================================================================


class TestPostingProbability:
    def test_basic_probability(self) -> None:
        settings = MagicMock()
        settings.posting.active_start_hour = 10
        settings.posting.active_end_hour = 21
        settings.posting.daily_limit = 2
        settings.daemon.min_interval_hours = 1.0
        settings.daemon.max_interval_hours = 2.0
        # active_hours=11, avg_interval=1.5, expected_cycles=~7.3
        prob = posting_probability(settings)
        assert 0.2 < prob < 0.4

    def test_zero_active_hours(self) -> None:
        settings = MagicMock()
        settings.posting.active_start_hour = 10
        settings.posting.active_end_hour = 10
        settings.posting.daily_limit = 2
        settings.daemon.min_interval_hours = 1.0
        settings.daemon.max_interval_hours = 2.0
        assert posting_probability(settings) == 0.0

    def test_capped_at_one(self) -> None:
        settings = MagicMock()
        settings.posting.active_start_hour = 10
        settings.posting.active_end_hour = 11
        settings.posting.daily_limit = 100
        settings.daemon.min_interval_hours = 1.0
        settings.daemon.max_interval_hours = 2.0
        assert posting_probability(settings) == 1.0


# =========================================================================
# PostingPipeline
# =========================================================================


def _make_repo(last_post_time: str | None = None) -> MagicMock:
    repo = MagicMock()
    repo.get_config.return_value = last_post_time
    return repo


def _make_tracker() -> MagicMock:
    return MagicMock()


def _make_settings(
    start_hour: int = 10,
    end_hour: int = 21,
) -> MagicMock:
    settings = MagicMock()
    settings.posting.active_start_hour = start_hour
    settings.posting.active_end_hour = end_hour
    return settings


def _make_content_gen(text: str = "今日はいい天気だな") -> MagicMock:
    gen = MagicMock()
    gen.generate_casual_post = AsyncMock(return_value=text)
    return gen


class TestPostingPipeline:
    """Test PostingPipeline with mocked dependencies."""

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=False)
    async def test_skips_quiet_hours(self, _mock_hours: MagicMock) -> None:
        pipeline = PostingPipeline(content_gen=_make_content_gen())
        result = await pipeline.run(
            _make_repo(), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.skipped_quiet_hours == 1
        assert result.posts_published == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    async def test_skips_daily_limit(self, _mock_hours: MagicMock) -> None:
        from outreach_shared.utils.rate_limiter import SlidingWindowLimiter

        limiter = SlidingWindowLimiter(max_actions=0, window_seconds=86_400.0)
        pipeline = PostingPipeline(
            content_gen=_make_content_gen(), daily_limiter=limiter
        )
        result = await pipeline.run(
            _make_repo(), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.skipped_daily_limit == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    async def test_skips_cooldown(self, _mock_hours: MagicMock) -> None:
        # Last post was 1 hour ago, min interval is 4 hours
        recent = (datetime.now(tz=UTC) - timedelta(hours=1)).isoformat()
        pipeline = PostingPipeline(
            content_gen=_make_content_gen(), min_interval_hours=4.0
        )
        result = await pipeline.run(
            _make_repo(last_post_time=recent),
            MagicMock(),
            _make_tracker(),
            _make_settings(),
        )
        assert result.skipped_cooldown == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    @patch("src.pipeline.posting._post_tweet_via_playwright", new_callable=AsyncMock)
    async def test_publish_success(
        self, mock_post: AsyncMock, _mock_hours: MagicMock
    ) -> None:
        mock_post.return_value = True
        content_gen = _make_content_gen("電車混みすぎ")
        pipeline = PostingPipeline(content_gen=content_gen, min_interval_hours=0.0)
        repo = _make_repo(last_post_time=None)
        tracker = _make_tracker()
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, tracker, _make_settings())

        assert result.posts_published == 1
        assert result.errors == 0
        tracker.record_post.assert_called_once()
        repo.set_config.assert_called_once()
        mock_post.assert_called_once_with(ctx, "電車混みすぎ")

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    async def test_content_generation_error(self, _mock_hours: MagicMock) -> None:
        gen = MagicMock()
        gen.generate_casual_post = AsyncMock(
            side_effect=ContentGenerationError("API down")
        )
        pipeline = PostingPipeline(content_gen=gen, min_interval_hours=0.0)
        result = await pipeline.run(
            _make_repo(), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.errors == 1
        assert result.posts_published == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    @patch("src.pipeline.posting._post_tweet_via_playwright", new_callable=AsyncMock)
    async def test_emergency_halt_on_rate_limit(
        self, mock_post: AsyncMock, _mock_hours: MagicMock
    ) -> None:
        mock_post.side_effect = PostingRateLimitError("restricted")
        pipeline = PostingPipeline(
            content_gen=_make_content_gen(), min_interval_hours=0.0
        )
        result = await pipeline.run(
            _make_repo(), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.emergency_halt is True
        assert result.errors == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    async def test_empty_content_is_error(self, _mock_hours: MagicMock) -> None:
        gen = MagicMock()
        gen.generate_casual_post = AsyncMock(return_value="")
        pipeline = PostingPipeline(content_gen=gen, min_interval_hours=0.0)
        result = await pipeline.run(
            _make_repo(), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.errors == 1
        assert result.posts_published == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.posting.is_active_hours", return_value=True)
    @patch("src.pipeline.posting._post_tweet_via_playwright", new_callable=AsyncMock)
    async def test_old_post_time_allows_posting(
        self, mock_post: AsyncMock, _mock_hours: MagicMock
    ) -> None:
        mock_post.return_value = True
        old_time = (datetime.now(tz=UTC) - timedelta(hours=10)).isoformat()
        pipeline = PostingPipeline(
            content_gen=_make_content_gen(), min_interval_hours=4.0
        )
        result = await pipeline.run(
            _make_repo(last_post_time=old_time),
            MagicMock(),
            _make_tracker(),
            _make_settings(),
        )
        assert result.posts_published == 1
