"""Timezone utilities and human-like delay helpers.

Provides timezone constants and helpers for JST (Asia/Tokyo, UTC+9)
and CST (Asia/Shanghai, UTC+8), plus common timing operations.
"""

from __future__ import annotations

import asyncio
import random
from datetime import datetime, timedelta, timezone

# JST is UTC+9 (Japan Standard Time)
JST = timezone(timedelta(hours=9))

# CST is UTC+8 (China Standard Time)
CST = timezone(timedelta(hours=8))


def now_jst() -> datetime:
    """Return the current time in JST (Asia/Tokyo, UTC+9)."""
    return datetime.now(tz=JST)


def now_cst() -> datetime:
    """Return the current time in CST (Asia/Shanghai, UTC+8)."""
    return datetime.now(tz=CST)


def is_active_hours(
    start_hour: int = 8,
    end_hour: int = 23,
    tz: timezone = JST,
) -> bool:
    """Check whether the current hour falls within active hours.

    Parameters
    ----------
    start_hour:
        Inclusive start of the active window (0-23).
    end_hour:
        Inclusive end of the active window (0-23).
    tz:
        Timezone for the check.  Defaults to JST.

    Returns
    -------
    bool
        ``True`` when ``start_hour <= current_hour <= end_hour``.
    """
    current_hour = datetime.now(tz=tz).hour
    return start_hour <= current_hour <= end_hour


async def random_delay(min_seconds: float, max_seconds: float) -> float:
    """Sleep for a random duration between *min_seconds* and *max_seconds*.

    Returns the actual number of seconds slept.
    """
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)
    return delay


def parse_post_timestamp(timestamp_str: str) -> datetime:
    """Parse a social platform timestamp string into a timezone-aware datetime.

    Supports ISO-8601 and common alternative formats used by X and
    other platforms.  The parsed result is returned in UTC.

    Falls back to common alternative formats when the primary format
    does not match.
    """
    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%a %b %d %H:%M:%S %z %Y",  # e.g. "Wed Oct 10 20:19:24 +0000 2018"
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    raise ValueError(f"Unable to parse timestamp: {timestamp_str!r}")


def post_age_hours(post_time: datetime) -> float:
    """Return the age of a post in hours relative to the current UTC time."""
    now_utc = datetime.now(tz=timezone.utc)
    delta = now_utc - post_time.astimezone(timezone.utc)
    return delta.total_seconds() / 3600.0
