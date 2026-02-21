"""Warmup mode for gradual pipeline ramp-up.

During the first 14 days of pipeline operation, all volume limits are
reduced by 50% to avoid triggering X's anti-automation systems on a
new account.  The pipeline start date is persisted in the config
store so it survives restarts.
"""

from __future__ import annotations

from datetime import UTC, datetime

from outreach_shared.utils.logger import get_logger

from src.config import Settings
from src.db.repository import Repository

logger = get_logger("warmup")

# Number of days for the warmup period
_WARMUP_DAYS = 14

# Config table key for the pipeline start date
_CONFIG_KEY_START_DATE = "pipeline_start_date"


class WarmupManager:
    """Manage the warmup period for a newly deployed pipeline.

    Parameters
    ----------
    repository:
        Database repository for reading/writing config state.
    warmup_days:
        Length of the warmup period in days.  Defaults to 14.
    """

    def __init__(
        self,
        repository: Repository,
        warmup_days: int = _WARMUP_DAYS,
    ) -> None:
        self._repo = repository
        self._warmup_days = warmup_days

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ensure_start_date(self) -> str:
        """Record the pipeline start date if not already set.

        On the very first run this writes the current UTC date to the
        ``config`` table.  Subsequent calls return the stored value.

        Returns
        -------
        str
            The pipeline start date as ``YYYY-MM-DD``.
        """
        existing = self._repo.get_config(_CONFIG_KEY_START_DATE)
        if existing is not None:
            return existing

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        self._repo.set_config(_CONFIG_KEY_START_DATE, today)
        logger.info("warmup_start_date_recorded", start_date=today)
        return today

    def is_warmup_active(self) -> bool:
        """Return ``True`` if the pipeline is within the warmup period."""
        return self.get_warmup_day() <= self._warmup_days

    def get_warmup_day(self) -> int:
        """Return the current warmup day (1-based).

        Day 1 is the pipeline start date.  Returns a value greater than
        ``warmup_days`` once the warmup period has elapsed.
        """
        start_str = self._repo.get_config(_CONFIG_KEY_START_DATE)
        if start_str is None:
            # No start date recorded yet; first run.
            return 1

        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=UTC)
        except ValueError:
            return 1

        now = datetime.now(tz=UTC)
        delta_days = (now - start_date).days
        return max(1, delta_days + 1)

    def get_volume_multiplier(self) -> float:
        """Return the volume multiplier for the current warmup state.

        Returns
        -------
        float
            ``0.5`` during warmup, ``1.0`` after.
        """
        if self.is_warmup_active():
            return 0.5
        return 1.0

    def apply_limits(self, settings: Settings) -> Settings:
        """Return a copy of *settings* with halved limits during warmup.

        The following limits are affected:

        * ``reply.daily_limit`` -- halved
        * ``dm.daily_limit`` -- halved
        * ``nurture.follow_daily_limit`` -- halved
        * ``nurture.like_daily_limit`` -- halved
        * ``posting.daily_limit`` -- halved
        * ``search.keywords`` -- only the first half of keywords

        Parameters
        ----------
        settings:
            The original application settings.

        Returns
        -------
        Settings
            A deep copy with adjusted limits.  If warmup is not
            active, the original settings are returned unchanged.
        """
        if not self.is_warmup_active():
            return settings

        # Create a deep copy to avoid mutating the original
        adjusted = settings.model_copy(deep=True)

        # Halve daily limits
        adjusted.reply.daily_limit = max(1, settings.reply.daily_limit // 2)
        adjusted.dm.daily_limit = max(1, settings.dm.daily_limit // 2)
        adjusted.nurture.follow_daily_limit = max(1, settings.nurture.follow_daily_limit // 2)
        adjusted.nurture.like_daily_limit = max(1, settings.nurture.like_daily_limit // 2)
        adjusted.posting.daily_limit = max(1, settings.posting.daily_limit // 2)

        # Use only the first half of keywords
        keywords = settings.search.keywords
        half = max(1, len(keywords) // 2)
        adjusted.search.keywords = keywords[:half]

        warmup_day = self.get_warmup_day()
        logger.info(
            "warmup_limits_applied",
            day=warmup_day,
            reply_limit=adjusted.reply.daily_limit,
            dm_limit=adjusted.dm.daily_limit,
            follow_limit=adjusted.nurture.follow_daily_limit,
            like_limit=adjusted.nurture.like_daily_limit,
            posting_limit=adjusted.posting.daily_limit,
            keyword_count=len(adjusted.search.keywords),
        )

        return adjusted
