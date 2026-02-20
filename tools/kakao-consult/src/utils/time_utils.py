"""KST time utilities and human-like delay helpers.

All datetime-aware operations use Asia/Seoul (KST, UTC+9) as the
canonical timezone for active-hours checks and scheduling.
"""

from __future__ import annotations

import asyncio
import random
from datetime import datetime, timezone, timedelta

# KST is UTC+9 -- defined as a fixed offset to avoid third-party deps.
KST = timezone(timedelta(hours=9))


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def now_kst() -> datetime:
    """Return the current time in KST (Asia/Seoul, UTC+9)."""
    return datetime.now(tz=KST)


def today_kst() -> str:
    """Return today's date in KST as a ``YYYY-MM-DD`` string."""
    return now_kst().strftime("%Y-%m-%d")


def is_active_hours(start_hour: int = 9, end_hour: int = 22) -> bool:
    """Check whether the current KST hour falls within active hours.

    Parameters
    ----------
    start_hour:
        Inclusive start of the active window (0-23).
    end_hour:
        Inclusive end of the active window (0-23).

    Returns
    -------
    bool
        ``True`` when ``start_hour <= current_hour <= end_hour``.
    """
    current_hour = now_kst().hour
    return start_hour <= current_hour <= end_hour


async def random_delay(min_seconds: float, max_seconds: float) -> float:
    """Sleep for a random duration between *min_seconds* and *max_seconds*.

    Returns the actual number of seconds slept.
    """
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)
    return delay
