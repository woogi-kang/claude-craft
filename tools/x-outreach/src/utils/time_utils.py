"""JST time utilities and human-like delay helpers.

All datetime-aware operations use Asia/Tokyo (JST, UTC+9) as the
canonical timezone for active-hours checks and tweet timestamp parsing.
"""

from __future__ import annotations

import asyncio
import random
from datetime import datetime, timezone, timedelta

# JST is UTC+9 -- defined as a fixed offset to avoid third-party deps.
JST = timezone(timedelta(hours=9))


def now_jst() -> datetime:
    """Return the current time in JST (Asia/Tokyo, UTC+9)."""
    return datetime.now(tz=JST)


def is_active_hours(start_hour: int = 8, end_hour: int = 23) -> bool:
    """Check whether the current JST hour falls within active hours.

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
    current_hour = now_jst().hour
    return start_hour <= current_hour <= end_hour


async def random_delay(min_seconds: float, max_seconds: float) -> float:
    """Sleep for a random duration between *min_seconds* and *max_seconds*.

    Returns the actual number of seconds slept.
    """
    delay = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(delay)
    return delay


def parse_tweet_timestamp(timestamp_str: str) -> datetime:
    """Parse an X (Twitter) timestamp string into a timezone-aware datetime.

    X uses the ISO-8601 format ``YYYY-MM-DDTHH:MM:SS.000Z`` in its API
    responses.  The parsed result is returned in UTC.

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

    raise ValueError(f"Unable to parse tweet timestamp: {timestamp_str!r}")


def tweet_age_hours(tweet_time: datetime) -> float:
    """Return the age of a tweet in hours relative to the current UTC time."""
    now_utc = datetime.now(tz=timezone.utc)
    delta = now_utc - tweet_time.astimezone(timezone.utc)
    return delta.total_seconds() / 3600.0
