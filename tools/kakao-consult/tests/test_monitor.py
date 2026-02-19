"""Tests for the MessageMonitor."""
from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock

from src.kakao.monitor import MessageMonitor, NewMessage


class _FakeElement:
    """Minimal mock for uiautomator2 UI elements."""

    def __init__(self, text: str = "", exists: bool = True):
        self._text = text
        self._exists = exists

    @property
    def exists(self):
        return self._exists

    def get_text(self):
        return self._text


def _make_badge_parent(title: str, message: str):
    """Create a mock badge parent with title and message children."""
    parent = MagicMock()
    parent.child.side_effect = lambda resourceId: {
        "com.kakao.talk:id/title": _FakeElement(title),
        "com.kakao.talk:id/message": _FakeElement(message),
    }.get(resourceId, _FakeElement(exists=False))
    return parent


class TestMessageMonitor:
    def test_poll_no_badges(self):
        device = MagicMock()
        badges = MagicMock()
        badges.exists = False
        device.resourceId.return_value = badges

        monitor = MessageMonitor(device)
        messages = monitor.poll()
        assert messages == []

    def test_poll_detects_new_message(self):
        device = MagicMock()
        parent = _make_badge_parent("Alice", "Hello!")
        badge = MagicMock()
        badge.parent.return_value = parent

        badges = MagicMock()
        badges.exists = True
        badges.count = 1
        badges.__getitem__ = MagicMock(return_value=badge)
        device.resourceId.return_value = badges

        monitor = MessageMonitor(device)
        messages = monitor.poll()

        assert len(messages) == 1
        assert messages[0].chatroom_name == "Alice"
        assert messages[0].text == "Hello!"

    def test_poll_skips_ignored_chatrooms(self):
        device = MagicMock()
        parent = _make_badge_parent("IgnoredRoom", "msg")
        badge = MagicMock()
        badge.parent.return_value = parent

        badges = MagicMock()
        badges.exists = True
        badges.count = 1
        badges.__getitem__ = MagicMock(return_value=badge)
        device.resourceId.return_value = badges

        monitor = MessageMonitor(device, ignored_chatrooms=["IgnoredRoom"])
        messages = monitor.poll()
        assert messages == []

    def test_poll_dedup_same_message(self):
        device = MagicMock()
        parent = _make_badge_parent("Alice", "Same text")
        badge = MagicMock()
        badge.parent.return_value = parent

        badges = MagicMock()
        badges.exists = True
        badges.count = 1
        badges.__getitem__ = MagicMock(return_value=badge)
        device.resourceId.return_value = badges

        monitor = MessageMonitor(device)
        first = monitor.poll()
        second = monitor.poll()

        assert len(first) == 1
        assert len(second) == 0  # Same message, deduped

    def test_poll_detects_new_after_different_text(self):
        device = MagicMock()

        def make_badges(text):
            parent = _make_badge_parent("Alice", text)
            badge = MagicMock()
            badge.parent.return_value = parent
            badges = MagicMock()
            badges.exists = True
            badges.count = 1
            badges.__getitem__ = MagicMock(return_value=badge)
            return badges

        device.resourceId.return_value = make_badges("First message")
        monitor = MessageMonitor(device)
        first = monitor.poll()
        assert len(first) == 1

        device.resourceId.return_value = make_badges("Second message")
        second = monitor.poll()
        assert len(second) == 1

    def test_reset_seen(self):
        monitor = MessageMonitor(MagicMock())
        monitor._seen_messages["room1"] = "hash1"
        monitor.reset_seen("room1")
        assert "room1" not in monitor._seen_messages

    def test_seen_messages_eviction(self):
        monitor = MessageMonitor(MagicMock(), max_seen=5)
        for i in range(10):
            monitor._seen_messages[f"room_{i}"] = f"hash_{i}"
        # Trigger eviction check manually
        if len(monitor._seen_messages) > monitor._max_seen:
            keys = list(monitor._seen_messages.keys())
            for old_key in keys[: len(keys) // 2]:
                del monitor._seen_messages[old_key]
        assert len(monitor._seen_messages) <= 10  # Some evicted
