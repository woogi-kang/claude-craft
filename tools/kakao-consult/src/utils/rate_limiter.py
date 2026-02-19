"""Rate limiting utilities for KakaoTalk consultation bot.

Provides four complementary limiters:

* ``TokenBucketLimiter`` -- classic token-bucket for short-burst limits
  (e.g. 30 responses per hour).
* ``SlidingWindowLimiter`` -- sliding-window counter for daily caps
  (e.g. max 200 responses per day).
* ``PerUserCooldown`` -- per-chatroom cooldown to avoid spamming
  individual conversations.
* ``CompositeRateLimiter`` -- combines all three into a single
  check-and-record interface.

All limiters are async-compatible and safe for single-process use.
"""

from __future__ import annotations

import asyncio
import time
from collections import deque


class TokenBucketLimiter:
    """Token-bucket rate limiter.

    Parameters
    ----------
    max_tokens:
        Maximum number of tokens in the bucket.
    refill_seconds:
        Time window (in seconds) over which all tokens are refilled.
    """

    def __init__(self, max_tokens: int, refill_seconds: float) -> None:
        self.max_tokens = max_tokens
        self.refill_seconds = refill_seconds
        self._tokens = float(max_tokens)
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill
        added = elapsed * (self.max_tokens / self.refill_seconds)
        self._tokens = min(self.max_tokens, self._tokens + added)
        self._last_refill = now

    async def acquire(self) -> None:
        """Wait until a token is available, then consume it."""
        while True:
            async with self._lock:
                self._refill()
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
            # Back off briefly before retrying
            await asyncio.sleep(0.5)

    @property
    def available_tokens(self) -> float:
        """Current (approximate) number of available tokens."""
        self._refill()
        return self._tokens


class SlidingWindowLimiter:
    """Sliding-window rate limiter for action caps.

    Parameters
    ----------
    max_actions:
        Maximum allowed actions within the window.
    window_seconds:
        Length of the sliding window in seconds.  Defaults to 86 400
        (24 hours).
    """

    def __init__(
        self, max_actions: int, window_seconds: float = 86_400.0
    ) -> None:
        self.max_actions = max_actions
        self.window_seconds = window_seconds
        self._timestamps: deque[float] = deque()

    def _prune(self) -> None:
        cutoff = time.monotonic() - self.window_seconds
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def can_act(self) -> bool:
        """Return ``True`` if an action is allowed right now."""
        self._prune()
        return len(self._timestamps) < self.max_actions

    def record(self) -> None:
        """Record that an action was performed at the current time."""
        self._timestamps.append(time.monotonic())

    @property
    def remaining(self) -> int:
        """Number of actions still allowed in the current window."""
        self._prune()
        return max(0, self.max_actions - len(self._timestamps))

    @property
    def actions_used(self) -> int:
        """Number of actions used in the current window."""
        self._prune()
        return len(self._timestamps)


class PerUserCooldown:
    """Per-chatroom cooldown to prevent spamming individual conversations.

    Tracks the last response time per ``chatroom_id`` and enforces a
    minimum interval between consecutive responses to the same chatroom.

    Parameters
    ----------
    min_interval_seconds:
        Minimum number of seconds between responses to the same chatroom.
    """

    def __init__(self, min_interval_seconds: int = 10) -> None:
        self.min_interval_seconds = min_interval_seconds
        self._cooldowns: dict[str, float] = {}

    def can_respond(self, chatroom_id: str) -> bool:
        """Return ``True`` if enough time has elapsed since the last
        response to *chatroom_id*.
        """
        last = self._cooldowns.get(chatroom_id)
        if last is None:
            return True
        return (time.monotonic() - last) >= self.min_interval_seconds

    def record_response(self, chatroom_id: str) -> None:
        """Record that a response was sent to *chatroom_id* right now."""
        self._cooldowns[chatroom_id] = time.monotonic()


class CompositeRateLimiter:
    """Combines hourly, daily, and per-user limiters into a single interface.

    Parameters
    ----------
    hourly_limit:
        Maximum responses per hour (token-bucket).
    daily_limit:
        Maximum responses per day (sliding-window).
    min_interval_seconds:
        Minimum seconds between responses to the same chatroom.
    """

    def __init__(
        self,
        hourly_limit: int = 30,
        daily_limit: int = 200,
        min_interval_seconds: int = 10,
    ) -> None:
        self._hourly = TokenBucketLimiter(hourly_limit, 3600)
        self._daily = SlidingWindowLimiter(daily_limit, 86_400)
        self._per_user = PerUserCooldown(min_interval_seconds)

    async def can_respond(self, chatroom_id: str) -> bool:
        """Return ``True`` if all limiters allow a response to *chatroom_id*."""
        if not self._per_user.can_respond(chatroom_id):
            return False
        if not self._daily.can_act():
            return False
        if self._hourly.available_tokens < 1.0:
            return False
        return True

    async def record_response(self, chatroom_id: str) -> None:
        """Record a response in all limiters and consume an hourly token."""
        await self._hourly.acquire()
        self._daily.record()
        self._per_user.record_response(chatroom_id)

    @property
    def remaining_daily(self) -> int:
        """Number of responses still allowed today."""
        return self._daily.remaining

    @property
    def remaining_hourly(self) -> float:
        """Approximate number of responses still allowed this hour."""
        return self._hourly.available_tokens
