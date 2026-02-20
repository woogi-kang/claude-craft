"""Account pool rotation with maturity lifecycle.

Manages crawl and outreach account pools with:
- Round-robin rotation with least-recently-used selection
- Maturity lifecycle (new -> nurturing -> active -> resting -> banned)
- Daily action counter resets
- Cooldown enforcement between uses
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from outreach_shared.utils.logger import get_logger

logger = get_logger("account_pool")


@dataclass
class Account:
    """In-memory representation of an outreach account."""

    account_id: str
    platform: str
    account_type: str  # "crawl" or "outreach"
    username: str | None = None
    proxy_ip: str | None = None
    status: str = "nurturing"
    maturity: str = "new"
    daily_comment_count: int = 0
    daily_dm_count: int = 0
    daily_search_count: int = 0
    last_warning_at: datetime | None = None
    last_used_at: datetime | None = None
    session_data_dir: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    banned_at: datetime | None = None


# Maturity lifecycle transitions
MATURITY_TRANSITIONS = {
    "new": "nurturing",
    "nurturing": "active",
    "active": "resting",
    "resting": "active",
}

# Daily limits by maturity level
DAILY_LIMITS = {
    "new": {"search": 5, "comment": 0, "dm": 0},
    "nurturing": {"search": 15, "comment": 3, "dm": 0},
    "active": {"search": 50, "comment": 10, "dm": 5},
    "resting": {"search": 0, "comment": 0, "dm": 0},
}

# Cooldown between uses (minutes)
COOLDOWN_MINUTES = {
    "crawl": 5,
    "outreach": 20,
}


class AccountPool:
    """Manage a pool of accounts with rotation and lifecycle.

    Parameters
    ----------
    cooldown_minutes:
        Override default cooldown between uses per account type.
    """

    def __init__(
        self,
        cooldown_minutes: dict[str, int] | None = None,
    ) -> None:
        self._accounts: dict[str, Account] = {}
        self._cooldowns = cooldown_minutes or dict(COOLDOWN_MINUTES)

    def add(self, account: Account) -> None:
        """Register an account in the pool."""
        self._accounts[account.account_id] = account
        logger.info(
            "account_added",
            account_id=account.account_id,
            account_type=account.account_type,
            maturity=account.maturity,
        )

    def get_available(
        self,
        platform: str,
        account_type: str,
    ) -> Account | None:
        """Return the least-recently-used active account that is off cooldown.

        Returns ``None`` when no suitable account is available.
        """
        now = datetime.now(tz=UTC)
        cooldown = timedelta(minutes=self._cooldowns.get(account_type, 10))

        candidates = [
            a
            for a in self._accounts.values()
            if a.platform == platform
            and a.account_type == account_type
            and a.status == "active"
            and (a.last_used_at is None or now - a.last_used_at >= cooldown)
        ]

        if not candidates:
            return None

        # Sort by last_used_at ascending (None first)
        candidates.sort(key=lambda a: a.last_used_at or datetime.min.replace(tzinfo=UTC))
        return candidates[0]

    def mark_used(self, account_id: str, action: str = "search") -> None:
        """Record that an account was used for an action.

        Parameters
        ----------
        account_id:
            The account to update.
        action:
            One of ``"search"``, ``"comment"``, ``"dm"``.
        """
        acct = self._accounts.get(account_id)
        if acct is None:
            return

        acct.last_used_at = datetime.now(tz=UTC)
        if action == "search":
            acct.daily_search_count += 1
        elif action == "comment":
            acct.daily_comment_count += 1
        elif action == "dm":
            acct.daily_dm_count += 1

    def is_within_daily_limit(self, account_id: str, action: str) -> bool:
        """Check if an account is within its daily limit for an action."""
        acct = self._accounts.get(account_id)
        if acct is None:
            return False

        limits = DAILY_LIMITS.get(acct.maturity, DAILY_LIMITS["new"])

        if action == "search":
            return acct.daily_search_count < limits["search"]
        if action == "comment":
            return acct.daily_comment_count < limits["comment"]
        if action == "dm":
            return acct.daily_dm_count < limits["dm"]
        return False

    def reset_daily_counts(self) -> None:
        """Reset all daily counters (call at midnight)."""
        for acct in self._accounts.values():
            acct.daily_search_count = 0
            acct.daily_comment_count = 0
            acct.daily_dm_count = 0
        logger.info("daily_counts_reset", count=len(self._accounts))

    def promote(self, account_id: str) -> str | None:
        """Advance an account to the next maturity stage.

        Returns the new maturity or ``None`` if no transition available.
        """
        acct = self._accounts.get(account_id)
        if acct is None:
            return None

        next_maturity = MATURITY_TRANSITIONS.get(acct.maturity)
        if next_maturity is None:
            return None

        old = acct.maturity
        acct.maturity = next_maturity
        if next_maturity == "active":
            acct.status = "active"
        elif next_maturity == "resting":
            acct.status = "resting"

        logger.info(
            "account_promoted",
            account_id=account_id,
            from_maturity=old,
            to_maturity=next_maturity,
        )
        return next_maturity

    def ban(self, account_id: str) -> None:
        """Mark an account as banned."""
        acct = self._accounts.get(account_id)
        if acct is None:
            return
        acct.status = "banned"
        acct.banned_at = datetime.now(tz=UTC)
        logger.warning("account_banned", account_id=account_id)

    def get_all(self, platform: str | None = None) -> list[Account]:
        """List all accounts, optionally filtered by platform."""
        accounts = list(self._accounts.values())
        if platform:
            accounts = [a for a in accounts if a.platform == platform]
        return accounts

    @property
    def active_count(self) -> int:
        """Number of accounts with status 'active'."""
        return sum(1 for a in self._accounts.values() if a.status == "active")
