"""Message monitor -- polls messenger chat list for new unread messages."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.messenger.selectors import KAKAO, MessengerSelectors
from src.utils.logger import get_logger

logger = get_logger("monitor")


@dataclass
class NewMessage:
    """A newly detected incoming message."""

    sender: str
    text: str
    chatroom_id: str
    chatroom_name: str
    timestamp: float = field(default_factory=time.time)


class MessageMonitor:
    """Poll a messenger's chat list for unread messages.

    Parameters
    ----------
    device:
        Connected uiautomator2 device instance.
    ignored_chatrooms:
        Chatroom names to skip (e.g. official channels).
    selectors:
        UI selectors for the target messenger. Defaults to KakaoTalk.
    """

    def __init__(
        self,
        device: object,
        ignored_chatrooms: list[str] | None = None,
        max_seen: int = 500,
        selectors: MessengerSelectors | None = None,
    ) -> None:
        self._device = device
        self._ignored: set[str] = set(ignored_chatrooms or [])
        self._seen_messages: dict[str, str] = {}  # chatroom_id -> last seen text hash
        self._max_seen = max_seen
        self._selectors = selectors or KAKAO

    def poll(self) -> list[NewMessage]:
        """Check for new unread messages in the chat list.

        Returns list of NewMessage for each chatroom with unread badge.
        The monitor must be on the chat list screen.
        """
        messages: list[NewMessage] = []

        try:
            # Find chat items with unread badges
            badge_elements = self._device.resourceId(self._selectors.chat_item_badge)  # type: ignore[attr-defined]

            if not badge_elements.exists:
                return messages

            count = badge_elements.count
            for i in range(min(count, 10)):  # Max 10 per poll
                try:
                    badge = badge_elements[i]
                    parent = badge.parent()

                    # Extract chatroom info
                    title_el = parent.child(resourceId=self._selectors.chat_item_title)
                    msg_el = parent.child(resourceId=self._selectors.chat_item_message)

                    if not title_el.exists or not msg_el.exists:
                        continue

                    chatroom_name = title_el.get_text() or ""
                    preview_text = msg_el.get_text() or ""

                    # Skip ignored chatrooms
                    if chatroom_name in self._ignored:
                        continue

                    # Use chatroom name as ID (simplified)
                    chatroom_id = chatroom_name

                    # Check if this is a new message
                    msg_hash = f"{chatroom_id}:{preview_text}"
                    if self._seen_messages.get(chatroom_id) == msg_hash:
                        continue

                    self._seen_messages[chatroom_id] = msg_hash

                    # Evict oldest entries if cache too large
                    if len(self._seen_messages) > self._max_seen:
                        # Remove oldest half
                        keys = list(self._seen_messages.keys())
                        for old_key in keys[:len(keys) // 2]:
                            del self._seen_messages[old_key]

                    messages.append(
                        NewMessage(
                            sender=chatroom_name,  # Will be refined when entering room
                            text=preview_text,
                            chatroom_id=chatroom_id,
                            chatroom_name=chatroom_name,
                        )
                    )

                except Exception as exc:
                    logger.warning("monitor_item_error", index=i, error=str(exc))
                    continue

        except Exception as exc:
            logger.error("monitor_poll_error", error=str(exc))

        if messages:
            logger.info("new_messages_detected", count=len(messages))

        return messages

    def reset_seen(self, chatroom_id: str) -> None:
        """Clear the seen state for a chatroom."""
        self._seen_messages.pop(chatroom_id, None)
