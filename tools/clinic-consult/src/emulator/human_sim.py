"""Human-like interaction simulation for Android emulator.

Provides realistic delays and input patterns to mimic natural human
behaviour when interacting with messenger apps through uiautomator2.
"""

from __future__ import annotations

import asyncio
import logging
import random

logger = logging.getLogger(__name__)


async def random_delay(min_s: float, max_s: float) -> None:
    """Sleep for a random duration between *min_s* and *max_s* seconds."""
    duration = random.uniform(min_s, max_s)
    await asyncio.sleep(duration)


async def human_type(
    device: object,
    text: str,
    min_delay_ms: int = 50,
    max_delay_ms: int = 200,
) -> None:
    """Type *text* into the device with human-like inter-keystroke delays.

    Uses ``device.send_keys()`` to input the full text (uiautomator2
    handles Korean IME internally), preceded by a character-level delay
    simulation that matches natural typing rhythm.

    Parameters
    ----------
    device:
        A ``uiautomator2.Device`` instance.
    text:
        The text string to type.
    min_delay_ms:
        Minimum delay between keystrokes in milliseconds.
    max_delay_ms:
        Maximum delay between keystrokes in milliseconds.
    """
    # Simulate per-character typing delay
    for char in text:
        delay_s = random.randint(min_delay_ms, max_delay_ms) / 1000.0
        await asyncio.sleep(delay_s)

    # Actually send the full text via uiautomator2
    device.send_keys(text)  # type: ignore[attr-defined]
    logger.debug("Typed %d characters", len(text))


def human_tap_with_jitter(
    device: object,
    x: int,
    y: int,
    jitter: int = 3,
) -> None:
    """Tap a screen coordinate with a small random offset.

    Adds a random pixel offset to both *x* and *y* to avoid
    perfectly robotic taps.

    Parameters
    ----------
    device:
        A ``uiautomator2.Device`` instance.
    x:
        Target X coordinate.
    y:
        Target Y coordinate.
    jitter:
        Maximum pixel offset applied in each direction.
    """
    offset_x = random.randint(-jitter, jitter)
    offset_y = random.randint(-jitter, jitter)
    tap_x = x + offset_x
    tap_y = y + offset_y
    device.click(tap_x, tap_y)  # type: ignore[attr-defined]
    logger.debug("Tapped (%d, %d) with jitter -> (%d, %d)", x, y, tap_x, tap_y)


async def reading_delay(
    text: str,
    min_s: float = 1.0,
    max_s: float = 3.0,
) -> None:
    """Simulate time spent reading a message before responding.

    Longer messages produce a longer delay, bounded by *min_s* and a
    length-based maximum.

    Parameters
    ----------
    text:
        The message text being "read".
    min_s:
        Minimum reading delay in seconds.
    max_s:
        Base maximum delay in seconds (scaled up for longer texts).
    """
    # Roughly ~200 chars/min reading speed -> ~0.3 s per character,
    # but capped to keep interactions snappy.
    length_factor = len(text) * 0.02  # 20 ms per character
    upper = max(min_s, min(max_s + length_factor, max_s * 3))
    duration = random.uniform(min_s, upper)
    await asyncio.sleep(duration)
    logger.debug("Reading delay %.2f s for %d-char message", duration, len(text))
