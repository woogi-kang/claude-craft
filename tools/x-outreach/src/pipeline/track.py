"""Action tracking and daily statistics.

Records all pipeline actions to the ``actions`` table and maintains
running totals in ``daily_stats`` for observability.
"""

from __future__ import annotations

from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.time_utils import now_jst

from src.db.repository import Repository

logger = get_logger("track")


class ActionTracker:
    """Record pipeline actions and update daily statistics.

    Parameters
    ----------
    repository:
        Database repository for persistence.
    """

    def __init__(self, repository: Repository) -> None:
        self._repo = repository

    def _today(self) -> str:
        """Return today's date in JST as ``YYYY-MM-DD``."""
        return now_jst().strftime("%Y-%m-%d")

    # ------------------------------------------------------------------
    # Action recording
    # ------------------------------------------------------------------

    def record_search(self, keyword: str, found_count: int) -> None:
        """Record a search action."""
        self._repo.record_action(
            action_type="search",
            tweet_id=None,
            username=None,
            details=f"keyword={keyword}, found={found_count}",
            status="success",
        )
        self._repo.update_daily_stats(self._today(), tweets_searched=found_count)

    def record_collect(self, stored: int, rejected: int) -> None:
        """Record the outcome of the collect phase."""
        self._repo.record_action(
            action_type="collect",
            tweet_id=None,
            username=None,
            details=f"stored={stored}, rejected={rejected}",
            status="success",
        )
        self._repo.update_daily_stats(self._today(), tweets_collected=stored)

    def record_analyze(
        self,
        tweet_id: str,
        classification: str,
        confidence: float,
    ) -> None:
        """Record a single tweet classification."""
        self._repo.record_action(
            action_type="analyze",
            tweet_id=tweet_id,
            username=None,
            details=f"classification={classification}, confidence={confidence:.2f}",
            status="success",
        )
        stat_key = f"tweets_{classification}"
        self._repo.update_daily_stats(self._today(), tweets_analyzed=1, **{stat_key: 1})

    def record_reply(self, tweet_id: str, username: str) -> None:
        """Record a reply action."""
        self._repo.record_action(
            action_type="reply",
            tweet_id=tweet_id,
            username=username,
            details=None,
            status="success",
        )
        self._repo.update_daily_stats(self._today(), replies_sent=1)

    def record_dm(self, username: str, template_used: str) -> None:
        """Record a DM action."""
        self._repo.record_action(
            action_type="dm",
            tweet_id=None,
            username=username,
            details=f"template={template_used}",
            status="success",
        )
        self._repo.update_daily_stats(self._today(), dms_sent=1)

    def record_dm_skip(self, username: str, reason: str) -> None:
        """Record a skipped DM."""
        self._repo.record_action(
            action_type="dm_skip",
            tweet_id=None,
            username=username,
            details=f"reason={reason}",
            status="skipped",
        )
        self._repo.update_daily_stats(self._today(), dms_skipped=1)

    def record_follow(self, tweet_id: str, username: str) -> None:
        """Record a follow action (daily stats only).

        The outreach table insert is handled by
        ``Repository.record_nurture_action`` to avoid double INSERT.
        """
        self._repo.update_daily_stats(self._today(), follows_sent=1)

    def record_like(self, tweet_id: str, username: str) -> None:
        """Record a like action (daily stats only).

        The outreach table insert is handled by
        ``Repository.record_nurture_action`` to avoid double INSERT.
        """
        self._repo.update_daily_stats(self._today(), likes_sent=1)

    def record_post(self, content_length: int) -> None:
        """Record an original post action."""
        self._repo.record_action(
            action_type="post",
            tweet_id=None,
            username=None,
            details=f"content_length={content_length}",
            status="success",
        )
        self._repo.update_daily_stats(self._today(), posts_published=1)

    def record_error(self, action_type: str, error_message: str) -> None:
        """Record an error that occurred during pipeline execution."""
        self._repo.record_action(
            action_type=action_type,
            tweet_id=None,
            username=None,
            details=None,
            status="error",
            error_message=error_message,
        )
        self._repo.update_daily_stats(self._today(), errors=1)

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------

    def get_today_summary(self) -> dict[str, int]:
        """Return today's stats as a dictionary."""
        stats = self._repo.get_daily_stats(self._today())
        if stats is None:
            return {}
        # Exclude non-metric keys
        return {
            k: v
            for k, v in stats.items()
            if k not in ("id", "date", "created_at") and isinstance(v, int)
        }

    def log_summary(self) -> None:
        """Log today's summary to structlog."""
        summary = self.get_today_summary()
        if summary:
            logger.info("daily_summary", **summary)
        else:
            logger.info("daily_summary", message="no stats recorded today")
