"""Emergency halt protocol for pipeline protection.

Detects account restriction signals from X API errors and Playwright
blocked pages, writes a halt file to stop all scheduled runs, and
provides a resume mechanism with reduced volume.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.utils.logger import get_logger

logger = get_logger("halt")

# Default halt file location relative to project root
_DEFAULT_HALT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / ".halt"


class HaltManager:
    """Manage emergency halt state for the pipeline.

    Parameters
    ----------
    halt_path:
        Path to the halt sentinel file.  When this file exists the
        scheduler must skip pipeline runs.
    """

    def __init__(self, halt_path: Path | None = None) -> None:
        self._halt_path = halt_path or _DEFAULT_HALT_PATH

    @property
    def halt_path(self) -> Path:
        """Return the path to the halt file."""
        return self._halt_path

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def is_halted(self) -> bool:
        """Return ``True`` if the halt file exists."""
        return self._halt_path.exists()

    def get_halt_info(self) -> dict[str, str] | None:
        """Read and return halt metadata, or ``None`` if not halted."""
        if not self._halt_path.exists():
            return None
        try:
            data = json.loads(self._halt_path.read_text(encoding="utf-8"))
            return data
        except (json.JSONDecodeError, OSError):
            return {"reason": "unknown", "timestamp": "unknown"}

    # ------------------------------------------------------------------
    # Halt triggers
    # ------------------------------------------------------------------

    def trigger_halt(self, reason: str, *, source: str = "unknown") -> None:
        """Create the halt file and log the event.

        Parameters
        ----------
        reason:
            Human-readable description of why the halt was triggered.
        source:
            The component that detected the issue (e.g. ``"api"``,
            ``"playwright"``).
        """
        self._halt_path.parent.mkdir(parents=True, exist_ok=True)

        halt_data = {
            "reason": reason,
            "source": source,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "resumed": False,
        }
        self._halt_path.write_text(
            json.dumps(halt_data, indent=2),
            encoding="utf-8",
        )
        logger.error(
            "emergency_halt_triggered",
            reason=reason,
            source=source,
            halt_path=str(self._halt_path),
        )

    def resume(self) -> bool:
        """Clear the halt file so the scheduler can run again.

        Returns
        -------
        bool
            ``True`` if a halt file was removed, ``False`` if not halted.
        """
        if not self._halt_path.exists():
            return False

        self._halt_path.unlink()
        logger.info("halt_cleared", halt_path=str(self._halt_path))
        return True

    # ------------------------------------------------------------------
    # Signal detection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def is_restriction_error(status_code: int, body: str = "") -> bool:
        """Detect X API restriction signals from HTTP responses.

        Parameters
        ----------
        status_code:
            HTTP status code from the API response.
        body:
            Response body text (optional) for deeper signal matching.

        Returns
        -------
        bool
            ``True`` if the response indicates an account restriction.
        """
        # Hard restriction signals
        if status_code == 403:
            restriction_phrases = [
                "suspended",
                "restricted",
                "locked",
                "temporarily limited",
                "account is temporarily",
            ]
            body_lower = body.lower()
            for phrase in restriction_phrases:
                if phrase in body_lower:
                    return True
            # A 403 without a body is also suspicious enough to halt
            if not body.strip():
                return True

        # Rate limiting with specific long-backoff signals
        if status_code == 429:
            body_lower = body.lower()
            if any(
                phrase in body_lower
                for phrase in ["too many requests", "rate limit"]
            ):
                return True

        return False

    @staticmethod
    def is_blocked_page(page_content: str) -> bool:
        """Detect Playwright blocked/challenge pages.

        Parameters
        ----------
        page_content:
            HTML content or visible text of the loaded page.

        Returns
        -------
        bool
            ``True`` if the page content suggests a block or challenge.
        """
        block_signals = [
            "something went wrong",
            "account suspended",
            "your account has been locked",
            "verify your identity",
            "unusual login activity",
            "caution: this account is temporarily limited",
        ]
        content_lower = page_content.lower()
        return any(signal in content_lower for signal in block_signals)


# ---------------------------------------------------------------------------
# Conservation mode helpers
# ---------------------------------------------------------------------------


def get_volume_multiplier(halt_manager: HaltManager) -> float:
    """Return a volume multiplier based on recent halt history.

    After a resume, the pipeline should run at 50% volume for the first
    cycle.  This is tracked via the halt file metadata.

    Parameters
    ----------
    halt_manager:
        The halt manager to check state against.

    Returns
    -------
    float
        ``1.0`` for normal operation, ``0.5`` after a recent resume.
    """
    # If the halt file existed recently (within the last resume cycle),
    # the resume command writes a marker.  We use a simple approach:
    # if the halt file does not exist but a .halt.resumed marker does,
    # return 0.5.
    resumed_path = halt_manager.halt_path.parent / ".halt.resumed"
    if resumed_path.exists():
        # Consume the marker so the next cycle runs at full volume
        resumed_path.unlink(missing_ok=True)
        logger.info("running_at_reduced_volume", multiplier=0.5)
        return 0.5
    return 1.0


def mark_resumed(halt_manager: HaltManager) -> None:
    """Write a resume marker for volume reduction on next cycle.

    Called by the ``resume`` CLI command after clearing the halt file.
    """
    resumed_path = halt_manager.halt_path.parent / ".halt.resumed"
    resumed_path.parent.mkdir(parents=True, exist_ok=True)
    resumed_path.write_text(
        json.dumps({"resumed_at": datetime.now(timezone.utc).isoformat()}),
        encoding="utf-8",
    )
