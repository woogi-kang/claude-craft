"""Tests for the daemon loop."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from outreach_shared.daemon.loop import DaemonLoop


class TestDaemonLoop:
    """Test daemon loop behavior."""

    @pytest.mark.asyncio
    async def test_stop_immediately(self) -> None:
        call_count = 0

        async def cycle() -> None:
            nonlocal call_count
            call_count += 1

        daemon = DaemonLoop(
            cycle,
            min_interval_hours=0.001,
            max_interval_hours=0.001,
            active_hours=(0, 23),
            tz=UTC,
        )

        async def stop_after_delay() -> None:
            await asyncio.sleep(0.05)
            daemon.stop()

        await asyncio.gather(daemon.run(), stop_after_delay())
        assert call_count >= 1

    @pytest.mark.asyncio
    async def test_is_running_flag(self) -> None:
        async def cycle() -> None:
            pass

        daemon = DaemonLoop(
            cycle,
            min_interval_hours=0.001,
            max_interval_hours=0.001,
        )
        assert daemon.is_running is False

        async def check_and_stop() -> None:
            await asyncio.sleep(0.02)
            assert daemon.is_running is True
            daemon.stop()

        await asyncio.gather(daemon.run(), check_and_stop())
        assert daemon.is_running is False

    @pytest.mark.asyncio
    async def test_outside_active_hours_skips_cycle(self) -> None:
        call_count = 0

        async def cycle() -> None:
            nonlocal call_count
            call_count += 1

        # Set active hours to a window that's impossible right now
        # by using hour 25 as start (always outside)
        current_hour = datetime.now(tz=UTC).hour
        # Pick an hour range that definitely doesn't include current
        start = (current_hour + 2) % 24
        end = (current_hour + 3) % 24

        daemon = DaemonLoop(
            cycle,
            min_interval_hours=0.001,
            max_interval_hours=0.001,
            active_hours=(start, end),
            tz=UTC,
        )

        async def stop_soon() -> None:
            await asyncio.sleep(0.05)
            daemon.stop()

        await asyncio.gather(daemon.run(), stop_soon())
        assert call_count == 0  # Should not have run

    @pytest.mark.asyncio
    async def test_midnight_callback(self) -> None:
        midnight_called = False

        async def cycle() -> None:
            pass

        async def on_midnight() -> None:
            nonlocal midnight_called
            midnight_called = True

        daemon = DaemonLoop(
            cycle,
            min_interval_hours=0.000005,
            max_interval_hours=0.000005,
            active_hours=(0, 23),
            tz=UTC,
            on_midnight=on_midnight,
        )

        async def stop_soon() -> None:
            # Wait for run() to initialise _last_date, then override it
            await asyncio.sleep(0.01)
            daemon._last_date = "2020-01-01"
            await asyncio.sleep(0.1)
            daemon.stop()

        await asyncio.gather(daemon.run(), stop_soon())
        assert midnight_called is True

    @pytest.mark.asyncio
    async def test_cycle_error_does_not_crash(self) -> None:
        call_count = 0

        async def failing_cycle() -> None:
            nonlocal call_count
            call_count += 1
            msg = "boom"
            raise RuntimeError(msg)

        daemon = DaemonLoop(
            failing_cycle,
            min_interval_hours=0.001,
            max_interval_hours=0.001,
            active_hours=(0, 23),
            tz=UTC,
        )

        async def stop_soon() -> None:
            await asyncio.sleep(0.05)
            daemon.stop()

        await asyncio.gather(daemon.run(), stop_soon())
        assert call_count >= 1  # Error was caught, loop continued

    def test_next_interval_in_range(self) -> None:
        async def cycle() -> None:
            pass

        daemon = DaemonLoop(
            cycle,
            min_interval_hours=2.0,
            max_interval_hours=4.0,
        )
        for _ in range(100):
            interval = daemon._next_interval_seconds()
            assert 2.0 * 3600 <= interval <= 4.0 * 3600
