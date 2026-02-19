"""Rate limiting utilities for X API and DM operations.

Provides three complementary limiters:

* ``TokenBucketLimiter`` -- classic token-bucket for short-burst limits
  (e.g. 17 writes per 15 minutes on the X API).
* ``SlidingWindowLimiter`` -- sliding-window counter for daily caps
  (e.g. max 20-30 DMs per day).
* ``MonthlyBudgetTracker`` -- simple counter for monthly API tweet
  budgets (e.g. 1 500 tweets/month on free tier).

All limiters are async-compatible and safe for single-process use.
"""

from __future__ import annotations

import asyncio
import time
from collections import deque
from datetime import datetime, timezone


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
    """Sliding-window rate limiter for daily action caps.

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


class MonthlyBudgetTracker:
    """Simple counter for monthly API tweet usage budgets.

    Parameters
    ----------
    monthly_limit:
        Maximum tweets allowed per calendar month.
    """

    def __init__(self, monthly_limit: int = 1500) -> None:
        self.monthly_limit = monthly_limit
        self._used: int = 0
        self._month: int = datetime.now(tz=timezone.utc).month

    def _maybe_reset(self) -> None:
        current_month = datetime.now(tz=timezone.utc).month
        if current_month != self._month:
            self._month = current_month
            self._used = 0

    def can_use(self, count: int = 1) -> bool:
        """Return ``True`` if *count* tweets can be consumed."""
        self._maybe_reset()
        return self._used + count <= self.monthly_limit

    def use(self, count: int = 1) -> None:
        """Record usage of *count* tweets."""
        self._maybe_reset()
        self._used += count

    @property
    def remaining(self) -> int:
        """Number of tweets remaining in the current month."""
        self._maybe_reset()
        return max(0, self.monthly_limit - self._used)

    @property
    def used(self) -> int:
        """Number of tweets used in the current month."""
        self._maybe_reset()
        return self._used

    @property
    def usage_ratio(self) -> float:
        """Return the fraction of the monthly budget consumed (0.0--1.0)."""
        self._maybe_reset()
        if self.monthly_limit == 0:
            return 1.0
        return self._used / self.monthly_limit

    def is_conservation_mode(self, threshold: float = 0.8) -> bool:
        """Return ``True`` when monthly usage has reached *threshold*.

        Parameters
        ----------
        threshold:
            Fraction of the monthly limit at which conservation mode
            activates.  Defaults to 0.80 (80%).
        """
        return self.usage_ratio >= threshold

    def is_critical_mode(self, threshold: float = 0.95) -> bool:
        """Return ``True`` when monthly usage has reached *threshold*.

        At this level, API-based replies should be stopped entirely
        while Playwright-based DMs can continue.

        Parameters
        ----------
        threshold:
            Fraction of the monthly limit at which critical mode
            activates.  Defaults to 0.95 (95%).
        """
        return self.usage_ratio >= threshold
