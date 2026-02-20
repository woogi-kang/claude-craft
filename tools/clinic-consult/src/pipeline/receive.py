"""Receive pipeline stage -- detect and collect new messages."""

from __future__ import annotations

from dataclasses import dataclass

from src.device.monitor import MessageMonitor, NewMessage
from src.utils.logger import get_logger

logger = get_logger("pipeline.receive")


@dataclass
class ReceiveResult:
    """Result from the receive stage."""

    messages: list[NewMessage]
    total_detected: int


class ReceivePipeline:
    """Detect new messages from the active messenger."""

    def __init__(self, monitor: MessageMonitor) -> None:
        self._monitor = monitor

    def run(self) -> ReceiveResult:
        """Poll for new messages."""
        messages = self._monitor.poll()
        logger.info("receive_done", count=len(messages))
        return ReceiveResult(messages=messages, total_detected=len(messages))
