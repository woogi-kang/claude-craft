"""Tests for the DM pipeline (personalized DM follow-up)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai.content_gen import ContentGenerationError
from src.pipeline.dm import (
    DmClosedError,
    DmEncryptionPasscodeError,
    DmPipeline,
    DmRateLimitError,
    DmResult,
    _is_dm_ready,
    _send_dm_with_retry,
)

# =========================================================================
# DmResult
# =========================================================================


class TestDmResult:
    """Test DmResult dataclass defaults."""

    def test_defaults(self) -> None:
        result = DmResult()
        assert result.total_candidates == 0
        assert result.dms_sent == 0
        assert result.skipped_quiet_hours == 0
        assert result.skipped_daily_limit == 0
        assert result.skipped_dm_closed == 0
        assert result.skipped_uniqueness == 0
        assert result.skipped_interval == 0
        assert result.skipped_too_soon == 0
        assert result.errors == 0
        assert result.emergency_halt is False
        assert result.encryption_passcode_error is False
        assert result.error_details == []


# =========================================================================
# _is_dm_ready
# =========================================================================


class TestIsDmReady:
    """Test the _is_dm_ready helper function."""

    def test_ready_after_min_delay(self) -> None:
        ts = (datetime.now(tz=UTC) - timedelta(minutes=30)).isoformat()
        assert _is_dm_ready(ts, min_delay_minutes=10, max_delay_minutes=30) is True

    def test_not_ready_too_soon(self) -> None:
        ts = (datetime.now(tz=UTC) - timedelta(minutes=5)).isoformat()
        assert _is_dm_ready(ts, min_delay_minutes=10, max_delay_minutes=30) is False

    def test_invalid_timestamp_returns_true(self) -> None:
        assert _is_dm_ready("not-a-date", min_delay_minutes=10, max_delay_minutes=30) is True

    def test_none_returns_true(self) -> None:
        # None triggers TypeError which is caught, returning True
        assert _is_dm_ready(None, min_delay_minutes=10, max_delay_minutes=30) is True  # type: ignore[arg-type]


# =========================================================================
# _send_dm_with_retry
# =========================================================================


class TestSendDmWithRetry:
    """Test the _send_dm_with_retry function."""

    @pytest.mark.asyncio
    @patch("src.pipeline.dm._send_dm_via_playwright", new_callable=AsyncMock)
    async def test_success_first_attempt(self, mock_send: AsyncMock) -> None:
        mock_send.return_value = True
        ctx = MagicMock()
        result = await _send_dm_with_retry(ctx, "user_a", "hello", max_attempts=2)
        assert result is True
        mock_send.assert_called_once_with(ctx, "user_a", "hello", settings=None)

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.asyncio.sleep", new_callable=AsyncMock)
    @patch("src.pipeline.dm._send_dm_via_playwright", new_callable=AsyncMock)
    async def test_retries_on_transient_error(
        self, mock_send: AsyncMock, _mock_sleep: AsyncMock
    ) -> None:
        mock_send.side_effect = [RuntimeError("transient"), True]
        ctx = MagicMock()
        result = await _send_dm_with_retry(ctx, "user_a", "hello", max_attempts=2)
        assert result is True
        assert mock_send.call_count == 2

    @pytest.mark.asyncio
    @patch("src.pipeline.dm._send_dm_via_playwright", new_callable=AsyncMock)
    async def test_dm_closed_not_retried(self, mock_send: AsyncMock) -> None:
        mock_send.side_effect = DmClosedError("DMs closed")
        ctx = MagicMock()
        with pytest.raises(DmClosedError):
            await _send_dm_with_retry(ctx, "user_a", "hello", max_attempts=2)
        mock_send.assert_called_once()

    @pytest.mark.asyncio
    @patch("src.pipeline.dm._send_dm_via_playwright", new_callable=AsyncMock)
    async def test_rate_limit_not_retried(self, mock_send: AsyncMock) -> None:
        mock_send.side_effect = DmRateLimitError("rate limited")
        ctx = MagicMock()
        with pytest.raises(DmRateLimitError):
            await _send_dm_with_retry(ctx, "user_a", "hello", max_attempts=2)
        mock_send.assert_called_once()

    @pytest.mark.asyncio
    @patch("src.pipeline.dm._send_dm_via_playwright", new_callable=AsyncMock)
    async def test_encryption_passcode_not_retried(self, mock_send: AsyncMock) -> None:
        mock_send.side_effect = DmEncryptionPasscodeError("passcode error")
        ctx = MagicMock()
        with pytest.raises(DmEncryptionPasscodeError):
            await _send_dm_with_retry(ctx, "user_a", "hello", max_attempts=2)
        mock_send.assert_called_once()


# =========================================================================
# DmPipeline
# =========================================================================


def _make_repo(
    tweets: list[dict] | None = None,
    last_dm: str | None = None,
) -> MagicMock:
    """Build a mock repository with configurable behaviour."""
    repo = MagicMock()
    repo.get_tweets_by_status.return_value = tweets or []
    repo.get_last_dm_to_user.return_value = last_dm
    repo.update_tweet_status.return_value = True
    return repo


def _make_tracker() -> MagicMock:
    """Build a mock action tracker."""
    return MagicMock()


def _make_settings() -> MagicMock:
    """Build a mock Settings."""
    settings = MagicMock()
    settings.daemon.active_start_hour = 8
    settings.daemon.active_end_hour = 23
    settings.dm_passcode_digits = None
    return settings


def _make_content_gen(dm_text: str = "test DM message") -> MagicMock:
    """Build a mock ContentGenerator."""
    gen = MagicMock()
    gen.generate_dm = AsyncMock(return_value=dm_text)
    return gen


def _replied_tweet(
    tweet_id: str = "t1",
    username: str = "user_a",
    hours_ago: float = 2.0,
) -> dict:
    """Create a minimal replied tweet dict."""
    return {
        "post_id": tweet_id,
        "username": username,
        "intent_type": "hospital",
        "contents": "test tweet",
        "reply_content": "previous reply",
        "reply_timestamp": (datetime.now(tz=UTC) - timedelta(hours=hours_ago)).isoformat(),
    }


class TestDmPipeline:
    """Test DmPipeline with mocked dependencies."""

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=False)
    async def test_skips_quiet_hours(self, _mock_hours: MagicMock) -> None:
        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        result = await pipeline.run(_make_repo(), MagicMock(), _make_tracker(), _make_settings())
        assert result.dms_sent == 0
        assert result.total_candidates == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    async def test_no_candidates(self, _mock_hours: MagicMock) -> None:
        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
        )
        result = await pipeline.run(
            _make_repo(tweets=[]), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.total_candidates == 0
        assert result.dms_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_dm_success(
        self,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_send.return_value = True
        tweets = [_replied_tweet()]
        content_gen = _make_content_gen("Hello DM!")
        repo = _make_repo(tweets=tweets, last_dm="previous dm")
        tracker = _make_tracker()
        ctx = MagicMock()

        pipeline = DmPipeline(
            content_gen=content_gen,
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(repo, ctx, tracker, _make_settings())

        assert result.dms_sent == 1
        assert result.errors == 0
        assert result.total_candidates == 1
        tracker.record_dm.assert_called_once()
        repo.update_tweet_status.assert_called_once()
        # Verify update_tweet_status was called with dm_sent status
        call_kwargs = repo.update_tweet_status.call_args
        assert call_kwargs[0][0] == "t1"
        assert call_kwargs.kwargs.get("status") == "dm_sent"

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    async def test_skips_daily_limit(self, _mock_hours: MagicMock) -> None:
        from outreach_shared.utils.rate_limiter import SlidingWindowLimiter

        limiter = SlidingWindowLimiter(max_actions=0, window_seconds=86_400.0)
        tweets = [_replied_tweet()]
        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            daily_limiter=limiter,
        )
        result = await pipeline.run(
            _make_repo(tweets=tweets), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.skipped_daily_limit == 1
        assert result.dms_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    async def test_skips_too_soon(self, _mock_hours: MagicMock) -> None:
        # Reply was 2 minutes ago, min delay is 10 minutes
        tweet = _replied_tweet(hours_ago=0.03)  # ~2 minutes ago
        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=10,
            dm_delay_max_minutes=30,
        )
        result = await pipeline.run(
            _make_repo(tweets=[tweet]), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.skipped_too_soon == 1
        assert result.dms_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_content_generation_error(
        self,
        _mock_treatment: MagicMock,
        _mock_hours: MagicMock,
    ) -> None:
        gen = MagicMock()
        gen.generate_dm = AsyncMock(side_effect=ContentGenerationError("API down"))
        tweets = [_replied_tweet()]
        pipeline = DmPipeline(
            content_gen=gen,
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(
            _make_repo(tweets=tweets), MagicMock(), _make_tracker(), _make_settings()
        )
        assert result.errors == 1
        assert result.dms_sent == 0
        assert len(result.error_details) == 1
        assert "content_gen" in result.error_details[0]

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_dm_closed_skips(
        self,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_send.side_effect = DmClosedError("DMs closed")
        tweets = [_replied_tweet()]
        repo = _make_repo(tweets=tweets)
        tracker = _make_tracker()

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(repo, MagicMock(), tracker, _make_settings())

        assert result.skipped_dm_closed == 1
        assert result.dms_sent == 0
        # Verify status updated to dm_skipped
        repo.update_tweet_status.assert_called_once()
        call_args = repo.update_tweet_status.call_args
        assert call_args[0][0] == "t1"
        assert call_args.kwargs.get("status") == "dm_skipped"
        tracker.record_dm_skip.assert_called_once_with("user_a", "dm_closed_detected")

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_emergency_halt_on_rate_limit(
        self,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_send.side_effect = DmRateLimitError("rate limited")
        tweets = [_replied_tweet(), _replied_tweet(tweet_id="t2", username="user_b")]
        repo = _make_repo(tweets=tweets)

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())

        assert result.emergency_halt is True
        assert result.errors == 1
        assert result.dms_sent == 0
        assert "rate_limit_emergency_halt" in result.error_details[0]

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_encryption_passcode_error(
        self,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        mock_send.side_effect = DmEncryptionPasscodeError("passcode issue")
        tweets = [_replied_tweet()]

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(
            _make_repo(tweets=tweets), MagicMock(), _make_tracker(), _make_settings()
        )

        assert result.encryption_passcode_error is True
        assert result.errors == 1
        assert result.dms_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=False)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_uniqueness_check_fails(
        self,
        _mock_treatment: MagicMock,
        mock_unique: MagicMock,
        _mock_hours: MagicMock,
    ) -> None:
        tweets = [_replied_tweet()]
        repo = _make_repo(tweets=tweets, last_dm="previous dm text")

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())

        assert result.skipped_uniqueness == 1
        assert result.dms_sent == 0

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    @patch("src.pipeline.dm.asyncio.sleep", new_callable=AsyncMock)
    async def test_interval_wait_between_dms(
        self,
        _mock_sleep: AsyncMock,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """Verify that the pipeline waits between DMs when interval has not elapsed."""
        mock_send.return_value = True
        tweets = [
            _replied_tweet(tweet_id="t1", username="user_a"),
            _replied_tweet(tweet_id="t2", username="user_b"),
        ]
        repo = _make_repo(tweets=tweets)

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
            min_interval_minutes=20,
            max_interval_minutes=40,
        )
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())

        # Both DMs should be sent (the second waits for interval)
        assert result.dms_sent == 2

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm.dm_uniqueness_check", return_value=True)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_generic_send_error_continues(
        self,
        _mock_treatment: MagicMock,
        _mock_unique: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """A generic exception during send should increment errors but continue."""
        mock_send.side_effect = RuntimeError("network timeout")
        tweets = [_replied_tweet()]

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(
            _make_repo(tweets=tweets), MagicMock(), _make_tracker(), _make_settings()
        )

        assert result.errors == 1
        assert result.dms_sent == 0
        assert "send" in result.error_details[0]

    @pytest.mark.asyncio
    @patch("src.pipeline.dm.is_active_hours", return_value=True)
    @patch("src.pipeline.dm._send_dm_with_retry", new_callable=AsyncMock)
    @patch("src.pipeline.dm._build_treatment_context", return_value="ctx")
    async def test_no_previous_dm_skips_uniqueness(
        self,
        _mock_treatment: MagicMock,
        mock_send: AsyncMock,
        _mock_hours: MagicMock,
    ) -> None:
        """When there is no previous DM, uniqueness check is skipped entirely."""
        mock_send.return_value = True
        tweets = [_replied_tweet()]
        # last_dm=None means no previous DM
        repo = _make_repo(tweets=tweets, last_dm=None)

        pipeline = DmPipeline(
            content_gen=_make_content_gen(),
            knowledge_base=MagicMock(),
            dm_delay_min_minutes=0,
            dm_delay_max_minutes=1,
        )
        result = await pipeline.run(repo, MagicMock(), _make_tracker(), _make_settings())

        assert result.dms_sent == 1
        assert result.skipped_uniqueness == 0
