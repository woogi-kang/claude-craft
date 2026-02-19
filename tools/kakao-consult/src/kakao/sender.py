"""Send messages in the current KakaoTalk chatroom.

Delivers text through the KakaoTalk input field with human-like
delays to avoid detection as automated input.
"""

from __future__ import annotations

from src.emulator import human_sim
from src.kakao import selectors
from src.utils.logger import get_logger

logger = get_logger("sender")


class MessageSender:
    """Type and send messages in the currently open KakaoTalk chatroom.

    Parameters
    ----------
    device:
        Connected uiautomator2 device instance.
    typing_delay_per_char_ms:
        Average delay in milliseconds between keystrokes.
    min_delay:
        Minimum "reading" delay in seconds before typing begins.
    max_delay:
        Maximum "reading" delay in seconds before typing begins.
    """

    def __init__(
        self,
        device: object,
        typing_delay_per_char_ms: int = 80,
        min_delay: float = 2.0,
        max_delay: float = 8.0,
    ) -> None:
        self._device = device
        self._typing_delay_per_char_ms = typing_delay_per_char_ms
        self._min_delay = min_delay
        self._max_delay = max_delay

    async def send(self, text: str) -> bool:
        """Send a single message in the current chatroom.

        Steps:
        1. Click the message input field.
        2. Simulate a human reading delay before typing.
        3. Type the text using ``device.send_keys()``.
        4. Click the send button.

        Parameters
        ----------
        text:
            The message text to send.

        Returns
        -------
        bool
            ``True`` if the message was sent successfully, ``False`` on error.
        """
        if not text.strip():
            logger.warning("send_empty_message")
            return False

        try:
            # 1. Focus the input field
            input_field = self._device.resourceId(selectors.MESSAGE_INPUT)  # type: ignore[attr-defined]
            if not input_field.exists:
                logger.error("send_input_not_found")
                return False

            input_field.click()

            # 2. Simulate reading delay (thinking time before reply)
            await human_sim.reading_delay(
                text,
                min_s=self._min_delay,
                max_s=self._max_delay,
            )

            # 3. Type the message with human-like delays
            await human_sim.human_type(
                self._device,
                text,
                min_delay_ms=max(30, self._typing_delay_per_char_ms - 30),
                max_delay_ms=self._typing_delay_per_char_ms + 50,
            )

            # 4. Tap the send button
            send_btn = self._device.resourceId(selectors.SEND_BUTTON)  # type: ignore[attr-defined]
            if not send_btn.exists:
                logger.error("send_button_not_found")
                return False

            send_btn.click()

            logger.info("message_sent", length=len(text))
            return True

        except Exception as exc:
            logger.error("send_message_error", error=str(exc))
            return False

    async def send_split(self, text: str, max_length: int = 500) -> bool:
        """Split a long message into chunks and send each with delay.

        Splits on newline boundaries when possible, otherwise at the
        ``max_length`` boundary.

        Parameters
        ----------
        text:
            The full message text to send.
        max_length:
            Maximum characters per individual message.

        Returns
        -------
        bool
            ``True`` if all chunks were sent successfully.
        """
        if len(text) <= max_length:
            return await self.send(text)

        chunks = self._split_text(text, max_length)
        logger.info("send_split_message", total_length=len(text), chunks=len(chunks))

        for i, chunk in enumerate(chunks):
            success = await self.send(chunk)
            if not success:
                logger.error("send_split_chunk_failed", chunk_index=i, total=len(chunks))
                return False

            # Small delay between consecutive chunks
            if i < len(chunks) - 1:
                await human_sim.random_delay(1.0, 3.0)

        return True

    @staticmethod
    def _split_text(text: str, max_length: int) -> list[str]:
        """Split text into chunks, preferring newline boundaries.

        Parameters
        ----------
        text:
            The text to split.
        max_length:
            Maximum length of each chunk.

        Returns
        -------
        list[str]
            Non-empty text chunks.
        """
        chunks: list[str] = []
        remaining = text

        while remaining:
            if len(remaining) <= max_length:
                chunks.append(remaining)
                break

            # Try to split at the last newline within the limit
            split_pos = remaining.rfind("\n", 0, max_length)

            if split_pos == -1:
                # No newline found; try splitting at the last space
                split_pos = remaining.rfind(" ", 0, max_length)

            if split_pos == -1:
                # No good break point; hard-split at max_length
                split_pos = max_length

            chunk = remaining[:split_pos].rstrip()
            if chunk:
                chunks.append(chunk)

            remaining = remaining[split_pos:].lstrip()

        return chunks
