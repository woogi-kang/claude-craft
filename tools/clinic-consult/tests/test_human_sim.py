"""Tests for human simulation utilities."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from src.emulator.human_sim import human_tap_with_jitter, human_type, random_delay, reading_delay


@pytest.mark.asyncio
async def test_random_delay_range():
    """random_delay should complete within reasonable bounds."""
    await random_delay(0.01, 0.02)  # Just ensure it doesn't error


@pytest.mark.asyncio
async def test_human_type_calls_send_keys():
    device = MagicMock()
    await human_type(device, "Hi", min_delay_ms=1, max_delay_ms=2)
    device.send_keys.assert_called_once_with("Hi")


def test_human_tap_with_jitter():
    device = MagicMock()
    human_tap_with_jitter(device, 100, 200, jitter=5)
    device.click.assert_called_once()
    args = device.click.call_args[0]
    assert 95 <= args[0] <= 105
    assert 195 <= args[1] <= 205


@pytest.mark.asyncio
async def test_reading_delay_short_text():
    await reading_delay("Hi", min_s=0.01, max_s=0.02)


@pytest.mark.asyncio
async def test_reading_delay_long_text():
    await reading_delay("A" * 500, min_s=0.01, max_s=0.02)
