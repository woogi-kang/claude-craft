"""Messenger UI automation layer.

Provides message monitoring, reading, sending, and navigation through
platform-agnostic uiautomator2 selectors. Supports KakaoTalk and LINE
via :class:`~src.messenger.selectors.MessengerSelectors` injection.
"""

from src.device.monitor import MessageMonitor, NewMessage
from src.device.navigator import Navigator
from src.device.reader import MessageReader
from src.device.sender import MessageSender

__all__ = [
    "MessageMonitor",
    "MessageReader",
    "MessageSender",
    "Navigator",
    "NewMessage",
]
