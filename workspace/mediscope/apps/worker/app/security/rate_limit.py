"""Simple in-memory sliding window rate limiter."""

import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self._max = max_requests
        self._window = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.monotonic()
        timestamps = self._requests[key]

        # Evict expired
        self._requests[key] = [t for t in timestamps if now - t < self._window]

        if len(self._requests[key]) >= self._max:
            return False

        self._requests[key].append(now)
        return True

    def reset(self, key: str) -> None:
        self._requests.pop(key, None)
