"""Tests for account pool rotation and lifecycle."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from outreach_shared.account.pool import (
    DAILY_LIMITS,
    Account,
    AccountPool,
)


class TestAccountPool:
    """Test account pool rotation."""

    def _make_active_account(self, account_id: str = "a1", **kwargs) -> Account:
        return Account(
            account_id=account_id,
            platform=kwargs.get("platform", "x"),
            account_type=kwargs.get("account_type", "crawl"),
            status="active",
            maturity="active",
            **{k: v for k, v in kwargs.items() if k not in ("platform", "account_type")},
        )

    def test_add_and_get_available(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 0})
        acct = self._make_active_account()
        pool.add(acct)
        result = pool.get_available("x", "crawl")
        assert result is not None
        assert result.account_id == "a1"

    def test_get_available_returns_none_when_empty(self) -> None:
        pool = AccountPool()
        assert pool.get_available("x", "crawl") is None

    def test_get_available_respects_cooldown(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 60})
        acct = self._make_active_account()
        acct.last_used_at = datetime.now(tz=UTC)
        pool.add(acct)
        # Should be None because cooldown hasn't elapsed
        assert pool.get_available("x", "crawl") is None

    def test_get_available_after_cooldown(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 5})
        acct = self._make_active_account()
        acct.last_used_at = datetime.now(tz=UTC) - timedelta(minutes=10)
        pool.add(acct)
        assert pool.get_available("x", "crawl") is not None

    def test_get_available_selects_lru(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 0})
        a1 = self._make_active_account("a1")
        a1.last_used_at = datetime.now(tz=UTC) - timedelta(minutes=30)
        a2 = self._make_active_account("a2")
        a2.last_used_at = datetime.now(tz=UTC) - timedelta(minutes=60)
        pool.add(a1)
        pool.add(a2)
        result = pool.get_available("x", "crawl")
        assert result is not None
        assert result.account_id == "a2"  # older = selected first

    def test_get_available_filters_by_platform(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 0})
        pool.add(self._make_active_account("a1", platform="x"))
        pool.add(self._make_active_account("a2", platform="xhs"))
        result = pool.get_available("xhs", "crawl")
        assert result is not None
        assert result.account_id == "a2"

    def test_get_available_excludes_non_active(self) -> None:
        pool = AccountPool(cooldown_minutes={"crawl": 0})
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="nurturing",
            maturity="new",
        )
        pool.add(acct)
        assert pool.get_available("x", "crawl") is None


class TestMarkUsed:
    """Test action recording."""

    def test_mark_used_search(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        pool.mark_used("a1", "search")
        assert acct.daily_search_count == 1
        assert acct.last_used_at is not None

    def test_mark_used_comment(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="outreach",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        pool.mark_used("a1", "comment")
        assert acct.daily_comment_count == 1

    def test_mark_used_dm(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="outreach",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        pool.mark_used("a1", "dm")
        assert acct.daily_dm_count == 1

    def test_mark_used_nonexistent_is_noop(self) -> None:
        pool = AccountPool()
        pool.mark_used("nonexistent", "search")  # Should not raise


class TestDailyLimits:
    """Test daily limit enforcement."""

    def test_within_limit(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        assert pool.is_within_daily_limit("a1", "search") is True

    def test_at_limit(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
            daily_search_count=DAILY_LIMITS["active"]["search"],
        )
        pool.add(acct)
        assert pool.is_within_daily_limit("a1", "search") is False

    def test_new_account_no_dm_allowed(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="outreach",
            status="active",
            maturity="new",
        )
        pool.add(acct)
        assert pool.is_within_daily_limit("a1", "dm") is False

    def test_nonexistent_account(self) -> None:
        pool = AccountPool()
        assert pool.is_within_daily_limit("nope", "search") is False


class TestResetAndLifecycle:
    """Test daily reset and maturity lifecycle."""

    def test_reset_daily_counts(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
            daily_search_count=42,
            daily_comment_count=5,
            daily_dm_count=3,
        )
        pool.add(acct)
        pool.reset_daily_counts()
        assert acct.daily_search_count == 0
        assert acct.daily_comment_count == 0
        assert acct.daily_dm_count == 0

    def test_promote_new_to_nurturing(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="nurturing",
            maturity="new",
        )
        pool.add(acct)
        result = pool.promote("a1")
        assert result == "nurturing"
        assert acct.maturity == "nurturing"

    def test_promote_nurturing_to_active(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="nurturing",
            maturity="nurturing",
        )
        pool.add(acct)
        result = pool.promote("a1")
        assert result == "active"
        assert acct.status == "active"

    def test_promote_active_to_resting(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        result = pool.promote("a1")
        assert result == "resting"
        assert acct.status == "resting"

    def test_ban_account(self) -> None:
        pool = AccountPool()
        acct = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
        )
        pool.add(acct)
        pool.ban("a1")
        assert acct.status == "banned"
        assert acct.banned_at is not None

    def test_active_count(self) -> None:
        pool = AccountPool()
        a1 = Account(
            account_id="a1",
            platform="x",
            account_type="crawl",
            status="active",
            maturity="active",
        )
        a2 = Account(
            account_id="a2",
            platform="x",
            account_type="crawl",
            status="nurturing",
            maturity="new",
        )
        pool.add(a1)
        pool.add(a2)
        assert pool.active_count == 1
