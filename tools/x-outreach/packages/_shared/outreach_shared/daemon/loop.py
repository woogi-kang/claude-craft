"""24-hour daemon loop with variable cycle intervals.

Replaces APScheduler with a simple asyncio loop that:
- Runs cycles every 2-4 hours (randomised)
- Respects active hours configuration
- Handles SIGTERM/SIGINT for graceful shutdown
- Resets daily counters at midnight
"""

from __future__ import annotations

import asyncio
import random
import signal
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime, timezone
from typing import Any

from outreach_shared.utils.logger import get_logger

logger = get_logger("daemon")


class DaemonLoop:
    """Async daemon loop with variable-interval cycle execution.

    Parameters
    ----------
    run_cycle:
        Async callable executed each cycle.  Receives no arguments.
    min_interval_hours:
        Minimum hours between cycles.
    max_interval_hours:
        Maximum hours between cycles.
    active_hours:
        Tuple of (start_hour, end_hour) in the configured timezone.
        Cycles are skipped outside these hours.
    tz:
        Timezone for active-hours checking.
    on_midnight:
        Optional async callback called when the date changes
        (for daily counter resets).
    """

    def __init__(
        self,
        run_cycle: Callable[[], Coroutine[Any, Any, None]],
        *,
        min_interval_hours: float = 2.0,
        max_interval_hours: float = 4.0,
        active_hours: tuple[int, int] = (8, 23),
        tz: timezone = UTC,
        on_midnight: Callable[[], Coroutine[Any, Any, None]] | None = None,
    ) -> None:
        self._run_cycle = run_cycle
        self._min_interval = min_interval_hours
        self._max_interval = max_interval_hours
        self._active_start, self._active_end = active_hours
        self._tz = tz
        self._on_midnight = on_midnight
        self._running = False
        self._last_date: str | None = None

    def _is_active_hour(self) -> bool:
        """Check if current hour is within active window."""
        current_hour = datetime.now(tz=self._tz).hour
        return self._active_start <= current_hour <= self._active_end

    def _next_interval_seconds(self) -> float:
        """Generate a random interval between min and max hours."""
        hours = random.uniform(self._min_interval, self._max_interval)
        return hours * 3600

    async def _check_midnight(self) -> None:
        """Call on_midnight callback if the date has changed."""
        today = datetime.now(tz=self._tz).strftime("%Y-%m-%d")
        if self._last_date is not None and today != self._last_date:
            if self._on_midnight:
                logger.info("midnight_reset", new_date=today)
                await self._on_midnight()
        self._last_date = today

    async def run(self) -> None:
        """Start the daemon loop. Blocks until stopped."""
        self._running = True
        self._last_date = datetime.now(tz=self._tz).strftime("%Y-%m-%d")

        # Install signal handlers
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, self._handle_signal, sig)

        logger.info(
            "daemon_started",
            interval=f"{self._min_interval}-{self._max_interval}h",
            active_hours=f"{self._active_start}:00-{self._active_end}:00",
        )

        while self._running:
            await self._check_midnight()

            if self._is_active_hour():
                try:
                    logger.info("cycle_start")
                    await self._run_cycle()
                    logger.info("cycle_complete")
                except Exception as exc:
                    logger.error("cycle_error", error=str(exc))
            else:
                logger.debug("outside_active_hours", skipping=True)

            # Sleep until next cycle
            interval = self._next_interval_seconds()
            logger.info(
                "next_cycle",
                wait_minutes=round(interval / 60, 1),
            )
            try:
                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break

        logger.info("daemon_stopped")

    def stop(self) -> None:
        """Signal the daemon to stop after the current cycle."""
        self._running = False
        logger.info("daemon_stop_requested")

    def _handle_signal(self, sig: signal.Signals) -> None:
        """Handle OS signals for graceful shutdown."""
        logger.info("signal_received", signal=sig.name)
        self.stop()

    @property
    def is_running(self) -> bool:
        """Whether the daemon loop is currently running."""
        return self._running
