"""Tests for src/utils/rate_limiter.py."""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest

from src.utils.rate_limiter import (
    CompositeRateLimiter,
    PerUserCooldown,
    SlidingWindowLimiter,
    TokenBucketLimiter,
)


# ---------------------------------------------------------------------------
# TokenBucketLimiter
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_token_bucket_acquire() -> None:
    """TokenBucketLimiter allows acquiring up to max_tokens immediately."""
    limiter = TokenBucketLimiter(max_tokens=3, refill_seconds=3600)

    # Should be able to acquire 3 tokens without blocking
    for _ in range(3):
        await limiter.acquire()

    # After consuming all tokens, available should be near 0
    assert limiter.available_tokens < 1.0


# ---------------------------------------------------------------------------
# SlidingWindowLimiter
# ---------------------------------------------------------------------------


def test_sliding_window_limit() -> None:
    """SlidingWindowLimiter blocks after max_actions are recorded."""
    limiter = SlidingWindowLimiter(max_actions=3, window_seconds=3600)

    for _ in range(3):
        assert limiter.can_act() is True
        limiter.record()

    # 4th action should be blocked
    assert limiter.can_act() is False


def test_sliding_window_remaining() -> None:
    """SlidingWindowLimiter.remaining decreases as actions are recorded."""
    limiter = SlidingWindowLimiter(max_actions=5, window_seconds=3600)

    assert limiter.remaining == 5

    limiter.record()
    assert limiter.remaining == 4

    limiter.record()
    limiter.record()
    assert limiter.remaining == 2


# ---------------------------------------------------------------------------
# PerUserCooldown
# ---------------------------------------------------------------------------


def test_per_user_cooldown_blocks_same_user() -> None:
    """PerUserCooldown blocks the same chatroom within the cooldown interval."""
    cooldown = PerUserCooldown(min_interval_seconds=10)

    chatroom = "room_abc"

    # First response is always allowed
    assert cooldown.can_respond(chatroom) is True
    cooldown.record_response(chatroom)

    # Immediately after, same chatroom is blocked
    assert cooldown.can_respond(chatroom) is False


def test_per_user_cooldown_different_users() -> None:
    """PerUserCooldown allows different chatrooms independently."""
    cooldown = PerUserCooldown(min_interval_seconds=10)

    room_a = "room_a"
    room_b = "room_b"

    cooldown.record_response(room_a)

    # room_a is blocked, but room_b is still allowed
    assert cooldown.can_respond(room_a) is False
    assert cooldown.can_respond(room_b) is True


def test_per_user_cooldown_expires() -> None:
    """PerUserCooldown allows responding after the interval elapses."""
    cooldown = PerUserCooldown(min_interval_seconds=5)

    chatroom = "room_x"
    cooldown.record_response(chatroom)
    assert cooldown.can_respond(chatroom) is False

    # Fast-forward time past the cooldown
    with patch.object(time, "monotonic", return_value=time.monotonic() + 6):
        assert cooldown.can_respond(chatroom) is True


# ---------------------------------------------------------------------------
# CompositeRateLimiter
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_composite_rate_limiter_daily_limit() -> None:
    """CompositeRateLimiter respects the daily sliding-window limit."""
    limiter = CompositeRateLimiter(
        hourly_limit=100,
        daily_limit=3,
        min_interval_seconds=0,
    )

    for i in range(3):
        chatroom = f"room_{i}"
        assert await limiter.can_respond(chatroom) is True
        await limiter.record_response(chatroom)

    # Daily limit exhausted
    assert limiter.remaining_daily == 0
    assert await limiter.can_respond("room_new") is False


@pytest.mark.asyncio
async def test_composite_rate_limiter_per_user() -> None:
    """CompositeRateLimiter respects the per-user cooldown."""
    limiter = CompositeRateLimiter(
        hourly_limit=100,
        daily_limit=100,
        min_interval_seconds=10,
    )

    chatroom = "room_1"

    assert await limiter.can_respond(chatroom) is True
    await limiter.record_response(chatroom)

    # Same chatroom should be blocked by per-user cooldown
    assert await limiter.can_respond(chatroom) is False

    # Different chatroom should still be allowed
    assert await limiter.can_respond("room_2") is True
