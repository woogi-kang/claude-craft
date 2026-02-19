"""Action tracking and daily statistics."""

from __future__ import annotations

from src.db.repository import Repository
from src.utils.logger import get_logger
from src.utils.time_utils import today_kst

logger = get_logger("pipeline.track")


class ActionTracker:
    """Track pipeline actions and aggregate daily statistics."""

    def __init__(self, repository: Repository) -> None:
        self._repo = repository

    def record_receive(self, chatroom_id: str, message_text: str) -> None:
        self._repo.record_action("receive", chatroom_id, message_text, "success")
        self._repo.update_daily_stats(today_kst(), messages_received=1)

    def record_respond(
        self,
        chatroom_id: str,
        provider: str,
        classification: str | None = None,
    ) -> None:
        details = f"provider={provider}"
        if classification:
            details += f", classification={classification}"
        self._repo.record_action("respond", chatroom_id, details, "success")

        stats: dict[str, int] = {"messages_responded": 1}
        if provider == "template":
            stats["template_responses"] = 1
            if classification == "faq":
                stats["faq_matches"] = 1
        else:
            stats["llm_responses"] = 1
            if provider == "claude":
                stats["claude_calls"] = 1
            elif provider in ("openai", "gpt4"):
                stats["gpt4_calls"] = 1
            elif provider == "ollama":
                stats["ollama_calls"] = 1

        self._repo.update_daily_stats(today_kst(), **stats)

    def record_error(
        self,
        action_type: str,
        error_message: str,
        chatroom_id: str | None = None,
    ) -> None:
        self._repo.record_action(action_type, chatroom_id, None, "error", error_message)
        self._repo.update_daily_stats(today_kst(), errors=1)

    def log_summary(self) -> None:
        stats = self._repo.get_daily_stats(today_kst())
        if stats:
            logger.info(
                "daily_summary",
                received=stats.get("messages_received", 0),
                responded=stats.get("messages_responded", 0),
                faq=stats.get("faq_matches", 0),
                llm=stats.get("llm_responses", 0),
                errors=stats.get("errors", 0),
            )
