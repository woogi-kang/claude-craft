"""Scheduler utilities for the polling loop."""

from __future__ import annotations

from src.utils.logger import get_logger

logger = get_logger("scheduler")


def log_scheduler_event(event_type: str, **kwargs) -> None:
    """Log a scheduler event."""
    logger.info(f"scheduler_{event_type}", **kwargs)
