"""Send pipeline stage -- deliver response via messenger."""

from __future__ import annotations

from dataclasses import dataclass

from src.device.sender import MessageSender
from src.utils.logger import get_logger

logger = get_logger("pipeline.send")


@dataclass
class SendResult:
    """Result from the send stage."""

    success: bool
    chatroom_id: str
    response_text: str
    error: str | None = None


class SendPipeline:
    """Send response message to a messenger chatroom."""

    def __init__(self, sender: MessageSender) -> None:
        self._sender = sender

    async def run(self, chatroom_id: str, text: str, max_length: int = 500) -> SendResult:
        """Send response text to the chatroom.

        Splits long messages if needed.
        """
        if not text:
            return SendResult(success=True, chatroom_id=chatroom_id, response_text="")

        try:
            if len(text) > max_length:
                success = await self._sender.send_split(text, max_length)
            else:
                success = await self._sender.send(text)

            if success:
                logger.info("message_sent", chatroom=chatroom_id, length=len(text))
            else:
                logger.warning("send_failed", chatroom=chatroom_id)

            return SendResult(
                success=success, chatroom_id=chatroom_id, response_text=text
            )
        except Exception as exc:
            logger.error("send_error", chatroom=chatroom_id, error=str(exc))
            return SendResult(
                success=False,
                chatroom_id=chatroom_id,
                response_text=text,
                error=str(exc),
            )
