"""Account health monitoring and escalation protocol.

Detects warning signals (rate limits, CAPTCHAs, restrictions) and
triggers escalation actions: pause, rest, or ban.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from outreach_shared.utils.logger import get_logger

logger = get_logger("account_health")


class HealthMonitor:
    """Monitor account health and trigger escalation.

    Escalation levels:
    1. Warning: log and continue (1st occurrence)
    2. Pause: rest account for cooldown_hours (2nd within window)
    3. Ban: mark account as banned (3rd within window)

    Parameters
    ----------
    warning_window_hours:
        Time window for counting warnings before escalating.
    cooldown_hours:
        Hours to rest an account after pause escalation.
    halt_file:
        Path to the halt file for emergency stops.
    """

    def __init__(
        self,
        *,
        warning_window_hours: int = 24,
        cooldown_hours: int = 4,
        halt_file: Path | None = None,
    ) -> None:
        self._warning_window_hours = warning_window_hours
        self._cooldown_hours = cooldown_hours
        self._halt_file = halt_file
        # Track warnings: account_id -> list of timestamps
        self._warnings: dict[str, list[datetime]] = {}

    def record_warning(
        self,
        account_id: str,
        reason: str,
    ) -> str:
        """Record a warning signal and return the escalation action.

        Returns
        -------
        str
            One of ``"continue"``, ``"pause"``, ``"ban"``.
        """
        now = datetime.now(tz=UTC)

        if account_id not in self._warnings:
            self._warnings[account_id] = []

        # Prune old warnings outside the window
        cutoff = now.timestamp() - (self._warning_window_hours * 3600)
        self._warnings[account_id] = [
            w for w in self._warnings[account_id] if w.timestamp() > cutoff
        ]

        self._warnings[account_id].append(now)
        count = len(self._warnings[account_id])

        if count >= 3:
            logger.error(
                "escalation_ban",
                account_id=account_id,
                reason=reason,
                warning_count=count,
            )
            return "ban"

        if count >= 2:
            logger.warning(
                "escalation_pause",
                account_id=account_id,
                reason=reason,
                cooldown_hours=self._cooldown_hours,
            )
            return "pause"

        logger.info(
            "escalation_warning",
            account_id=account_id,
            reason=reason,
        )
        return "continue"

    def is_halted(self) -> bool:
        """Check if the emergency halt file exists."""
        if self._halt_file is None:
            return False
        return self._halt_file.exists()

    def write_halt(self, reason: str) -> None:
        """Write an emergency halt file to stop all operations."""
        if self._halt_file is None:
            return
        self._halt_file.parent.mkdir(parents=True, exist_ok=True)
        halt_data = {
            "halted_at": datetime.now(tz=UTC).isoformat(),
            "reason": reason,
        }
        self._halt_file.write_text(json.dumps(halt_data), encoding="utf-8")
        logger.error("emergency_halt", reason=reason)

    def clear_halt(self) -> bool:
        """Remove the halt file to resume operations.

        Returns ``True`` if a halt file was removed.
        """
        if self._halt_file is None or not self._halt_file.exists():
            return False
        self._halt_file.unlink()
        logger.info("halt_cleared")
        return True

    def get_warning_count(self, account_id: str) -> int:
        """Return the current warning count for an account."""
        now = datetime.now(tz=UTC)
        cutoff = now.timestamp() - (self._warning_window_hours * 3600)
        warnings = self._warnings.get(account_id, [])
        return len([w for w in warnings if w.timestamp() > cutoff])
