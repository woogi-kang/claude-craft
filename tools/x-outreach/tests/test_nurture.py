"""Tests for the nurture pipeline (follow/like)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.pipeline.nurture import (
    FollowOutcome,
    LikeOutcome,
    NurturePipeline,
    NurtureRateLimitError,
    NurtureResult,
)

# =========================================================================
# NurtureResult
# =========================================================================


class TestNurtureResult:
    """Test NurtureResult dataclass defaults."""

    def test_defaults(self) -> None:
        result = NurtureResult()
        assert result.total_candidates == 0
        assert result.follows_sent == 0
        assert result.likes_sent == 0
        assert result.already_followed == 0
        assert result.already_liked == 0
        assert result.errors == 0
        assert result.emergency_halt is False
        assert result.error_details == []


# =========================================================================
# Enums
# =========================================================================


class TestOutcomeEnums:
    def test_follow_outcome_values(self) -> None:
        assert FollowOutcome.SUCCESS.value == "success"
        assert FollowOutcome.ALREADY_FOLLOWING.value == "already_following"
        assert FollowOutcome.ERROR.value == "error"

    def test_like_outcome_values(self) -> None:
        assert LikeOutcome.SUCCESS.value == "success"
        assert LikeOutcome.ALREADY_LIKED.value == "already_liked"
        assert LikeOutcome.ERROR.value == "error"


# =========================================================================
# NurturePipeline
# =========================================================================


def _make_repo(
    tweets: list[dict] | None = None,
    followed_users: set[str] | None = None,
    liked_tweets: set[str] | None = None,
) -> MagicMock:
    """Build a mock repository with configurable behaviour."""
    repo = MagicMock()
    repo.get_tweets_by_status.return_value = tweets or []
    followed = followed_users or set()
    liked = liked_tweets or set()
    repo.is_user_followed.side_effect = lambda u: u in followed
    repo.is_tweet_liked.side_effect = lambda t: t in liked
    repo.record_nurture_action.return_value = 1
    return repo


def _make_tracker() -> MagicMock:
    """Build a mock action tracker."""
    tracker = MagicMock()
    return tracker


def _make_settings() -> MagicMock:
    """Build a mock Settings with delays."""
    settings = MagicMock()
    settings.delays.action_min_seconds = 0.01
    settings.delays.action_max_seconds = 0.02
    return settings


def _analyzed_tweet(
    tweet_id: str = "t1",
    username: str = "user_a",
    llm_decision: bool = True,
) -> dict:
    """Create a minimal analyzed tweet dict."""
    return {
        "post_id": tweet_id,
        "username": username,
        "llm_decision": llm_decision,
        "intent_type": "hospital",
        "contents": "test tweet",
        "post_url": f"https://x.com/{username}/status/{tweet_id}",
    }


class TestNurturePipeline:
    """Test NurturePipeline with mocked dependencies."""

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=False)
    async def test_skips_quiet_hours(self, _mock_hours: MagicMock) -> None:
        pipeline = NurturePipeline()
        repo = _make_repo()
        ctx = MagicMock()
        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())
        assert result.total_candidates == 0
        repo.get_tweets_by_status.assert_not_called()

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    async def test_no_candidates(self, _mock_hours: MagicMock) -> None:
        pipeline = NurturePipeline()
        repo = _make_repo(tweets=[])
        ctx = MagicMock()
        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())
        assert result.total_candidates == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    async def test_filters_non_actionable(self, _mock_hours: MagicMock) -> None:
        tweets = [_analyzed_tweet(llm_decision=False)]
        pipeline = NurturePipeline()
        repo = _make_repo(tweets=tweets)
        ctx = MagicMock()
        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())
        assert result.total_candidates == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture._follow_user_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.nurture._like_tweet_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_follow_and_like_success(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        mock_like: AsyncMock,
        mock_follow: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_follow.return_value = FollowOutcome.SUCCESS
        mock_like.return_value = LikeOutcome.SUCCESS

        tweets = [_analyzed_tweet()]
        pipeline = NurturePipeline(follow_probability=0.5, like_probability=0.5)
        repo = _make_repo(tweets=tweets)
        tracker = _make_tracker()
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, tracker, _make_settings())

        assert result.follows_sent == 1
        assert result.likes_sent == 1
        assert result.errors == 0
        tracker.record_follow.assert_called_once()
        tracker.record_like.assert_called_once()
        repo.record_nurture_action.assert_any_call("follow", "t1", "user_a")
        repo.record_nurture_action.assert_any_call("like", "t1", "user_a")

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_skips_already_followed(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        tweets = [_analyzed_tweet()]
        pipeline = NurturePipeline(follow_probability=1.0, like_probability=0.0)
        repo = _make_repo(tweets=tweets, followed_users={"user_a"})
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())

        assert result.follows_sent == 0
        assert result.already_followed == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_skips_already_liked(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        tweets = [_analyzed_tweet()]
        pipeline = NurturePipeline(follow_probability=0.0, like_probability=1.0)
        repo = _make_repo(tweets=tweets, liked_tweets={"t1"})
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())

        assert result.likes_sent == 0
        assert result.already_liked == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture._follow_user_via_playwright", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_emergency_halt_on_rate_limit(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        mock_follow: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_follow.side_effect = NurtureRateLimitError("restricted")

        tweets = [_analyzed_tweet(), _analyzed_tweet(tweet_id="t2", username="user_b")]
        pipeline = NurturePipeline(follow_probability=1.0, like_probability=0.0)
        repo = _make_repo(tweets=tweets)
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())

        assert result.emergency_halt is True
        assert result.errors == 1
        # Should stop after first error (not process second candidate)
        assert result.follows_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_daily_limit_follow(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        from outreach_shared.utils.rate_limiter import SlidingWindowLimiter

        limiter = SlidingWindowLimiter(max_actions=0, window_seconds=86_400.0)
        tweets = [_analyzed_tweet()]
        pipeline = NurturePipeline(
            follow_daily_limiter=limiter,
            follow_probability=1.0,
            like_probability=0.0,
        )
        repo = _make_repo(tweets=tweets)
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())

        assert result.follows_sent == 0
        assert result.skipped_daily_limit_follow == 1

    @pytest.mark.asyncio
    @patch("src.pipeline.nurture.is_active_hours", return_value=True)
    @patch("src.pipeline.nurture.human_scroll", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random_pause", new_callable=AsyncMock)
    @patch("src.pipeline.nurture.random.random", return_value=0.1)
    @patch("src.pipeline.nurture.random.shuffle")
    async def test_daily_limit_like(
        self,
        mock_shuffle: MagicMock,
        _mock_rand: MagicMock,
        _mock_pause: AsyncMock,
        _mock_scroll: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        from outreach_shared.utils.rate_limiter import SlidingWindowLimiter

        limiter = SlidingWindowLimiter(max_actions=0, window_seconds=86_400.0)
        tweets = [_analyzed_tweet()]
        pipeline = NurturePipeline(
            like_daily_limiter=limiter,
            follow_probability=0.0,
            like_probability=1.0,
        )
        repo = _make_repo(tweets=tweets)
        ctx = MagicMock()

        result = await pipeline.run(repo, ctx, _make_tracker(), _make_settings())

        assert result.likes_sent == 0
        assert result.skipped_daily_limit_like == 1
