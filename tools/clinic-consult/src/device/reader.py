"""Read message content from within a messenger chatroom.

Uses uiautomator2 selectors to extract the last N messages from the
currently open chatroom, including sender names and message text.
Works with any messenger supported by :class:`MessengerSelectors`.
"""

from __future__ import annotations

from src.messenger.selectors import KAKAO, MessengerSelectors
from src.utils.logger import get_logger

logger = get_logger("reader")


class MessageReader:
    """Extract messages from the currently open chatroom.

    Parameters
    ----------
    device:
        Connected uiautomator2 device instance.
    selectors:
        UI selectors for the target messenger. Defaults to KakaoTalk.
    """

    def __init__(
        self,
        device: object,
        selectors: MessengerSelectors | None = None,
    ) -> None:
        self._device = device
        self._selectors = selectors or KAKAO

    def read_messages(self, count: int = 5) -> list[dict[str, str | bool | None]]:
        """Read the last *count* messages from the current chatroom.

        Returns a list of dicts, each with keys:
        - ``sender`` (str | None): Display name of the sender, or ``None``
          for messages without a visible sender (consecutive own messages).
        - ``text`` (str): The message body.
        - ``is_incoming`` (bool): ``True`` if the message was sent by
          another user (has a sender label), ``False`` otherwise.

        Parameters
        ----------
        count:
            Maximum number of messages to retrieve (from the bottom of
            the chat scroll).

        Returns
        -------
        list[dict[str, str | bool | None]]
            Messages ordered from oldest to newest.
        """
        messages: list[dict[str, str | bool | None]] = []

        try:
            text_elements = self._device.resourceId(self._selectors.message_text)  # type: ignore[attr-defined]

            if not text_elements.exists:
                logger.debug("read_no_messages_found")
                return messages

            total = text_elements.count
            start_index = max(0, total - count)

            for i in range(start_index, total):
                try:
                    msg_el = text_elements[i]
                    text = msg_el.get_text() or ""

                    if not text:
                        continue

                    # Try to find the sender label near this message element.
                    # Incoming messages have a profile_name sibling;
                    # outgoing messages do not.
                    sender: str | None = None
                    is_incoming = False

                    try:
                        parent = msg_el.parent()
                        sender_el = parent.child(resourceId=self._selectors.message_sender)
                        if sender_el.exists:
                            sender = sender_el.get_text() or None
                            is_incoming = True
                    except Exception:
                        # No sender element found -- treat as outgoing
                        pass

                    messages.append(
                        {
                            "sender": sender,
                            "text": text,
                            "is_incoming": is_incoming,
                        }
                    )

                except Exception as exc:
                    logger.warning("read_message_error", index=i, error=str(exc))
                    continue

        except Exception as exc:
            logger.error("read_messages_error", error=str(exc))

        logger.debug("read_messages_count", count=len(messages))
        return messages

    def get_chatroom_title(self) -> str:
        """Read the current chatroom title from the toolbar.

        Returns
        -------
        str
            The chatroom title, or an empty string if not found.
        """
        try:
            title_el = self._device.resourceId(self._selectors.chatroom_title)  # type: ignore[attr-defined]
            if title_el.exists:
                return title_el.get_text() or ""
        except Exception as exc:
            logger.warning("read_chatroom_title_error", error=str(exc))

        return ""
