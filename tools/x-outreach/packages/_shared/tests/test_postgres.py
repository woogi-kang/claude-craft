"""Tests for PostgresRepository.

These tests require a running PostgreSQL instance. They are skipped
automatically when PostgreSQL is not available. Set DATABASE_URL env
var or run with testcontainers (requires Docker).
"""

from __future__ import annotations

import asyncio
import os

import asyncpg
import pytest

from outreach_shared.db.postgres import PostgresRepository


def _get_dsn() -> str | None:
    """Return a test PostgreSQL DSN or None."""
    return os.environ.get("DATABASE_URL") or os.environ.get("TEST_DATABASE_URL")


def _can_connect(dsn: str) -> bool:
    """Check if we can actually connect to the database."""
    try:
        loop = asyncio.new_event_loop()
        conn = loop.run_until_complete(asyncpg.connect(dsn))
        loop.run_until_complete(conn.close())
        loop.close()
        return True
    except Exception:
        return False


_dsn = _get_dsn()
_skip_reason = "No PostgreSQL available (set DATABASE_URL or TEST_DATABASE_URL)"
_pg_available = _dsn is not None and _can_connect(_dsn) if _dsn else False

pytestmark = pytest.mark.skipif(not _pg_available, reason=_skip_reason)


@pytest.fixture
async def repo() -> PostgresRepository:
    """Create a repo with clean tables for each test."""
    assert _dsn is not None
    r = PostgresRepository(_dsn, min_pool_size=1, max_pool_size=2)
    await r.connect()
    # Clean tables before each test
    async with r.pool.acquire() as conn:
        await conn.execute("DELETE FROM outreach")
        await conn.execute("DELETE FROM posts")
        await conn.execute("DELETE FROM accounts")
    yield r  # type: ignore[misc]
    await r.close()


class TestPostsCRUD:
    """Test posts table operations."""

    @pytest.mark.asyncio
    async def test_insert_and_get(self, repo: PostgresRepository) -> None:
        pid = await repo.insert_post(
            post_id="test_1",
            platform="x",
            user_id="user_1",
            contents="Looking for skin clinic in Tokyo",
            username="testuser",
        )
        assert pid > 0

        post = await repo.get_post("test_1")
        assert post is not None
        assert post["platform"] == "x"
        assert post["contents"] == "Looking for skin clinic in Tokyo"
        assert post["status"] == "collected"

    @pytest.mark.asyncio
    async def test_insert_duplicate_returns_neg1(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="dup_1", platform="x", user_id="u1", contents="hello")
        result = await repo.insert_post(
            post_id="dup_1", platform="x", user_id="u1", contents="hello again"
        )
        assert result == -1

    @pytest.mark.asyncio
    async def test_update_status(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="s_1", platform="x", user_id="u1", contents="test")
        await repo.update_post_status("s_1", "curated", intent_type="hospital")
        post = await repo.get_post("s_1")
        assert post is not None
        assert post["status"] == "curated"
        assert post["intent_type"] == "hospital"

    @pytest.mark.asyncio
    async def test_get_by_status(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="a1", platform="x", user_id="u1", contents="c1")
        await repo.insert_post(post_id="a2", platform="xhs", user_id="u2", contents="c2")
        await repo.update_post_status("a2", "curated")

        collected = await repo.get_posts_by_status("collected")
        assert len(collected) == 1
        assert collected[0]["post_id"] == "a1"

    @pytest.mark.asyncio
    async def test_get_by_status_with_platform_filter(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="p1", platform="x", user_id="u1", contents="c1")
        await repo.insert_post(post_id="p2", platform="xhs", user_id="u2", contents="c2")

        x_posts = await repo.get_posts_by_status("collected", platform="x")
        assert len(x_posts) == 1
        assert x_posts[0]["platform"] == "x"

    @pytest.mark.asyncio
    async def test_count_posts(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="c1", platform="x", user_id="u1", contents="c1")
        await repo.insert_post(post_id="c2", platform="x", user_id="u2", contents="c2")
        count = await repo.count_posts(platform="x")
        assert count == 2


class TestAccountsCRUD:
    """Test accounts table operations."""

    @pytest.mark.asyncio
    async def test_insert_and_list(self, repo: PostgresRepository) -> None:
        await repo.insert_account(
            account_id="acc_1",
            platform="x",
            account_type="crawl",
            username="crawler1",
        )
        accounts = await repo.get_accounts(platform="x")
        assert len(accounts) == 1
        assert accounts[0]["account_type"] == "crawl"
        assert accounts[0]["maturity"] == "new"

    @pytest.mark.asyncio
    async def test_upsert_updates_fields(self, repo: PostgresRepository) -> None:
        await repo.insert_account(
            account_id="acc_2",
            platform="x",
            account_type="outreach",
            username="old_name",
        )
        await repo.insert_account(
            account_id="acc_2",
            platform="x",
            account_type="outreach",
            username="new_name",
        )
        accounts = await repo.get_accounts(platform="x")
        assert len(accounts) == 1
        assert accounts[0]["username"] == "new_name"

    @pytest.mark.asyncio
    async def test_get_available_account(self, repo: PostgresRepository) -> None:
        await repo.insert_account(account_id="avail_1", platform="x", account_type="outreach")
        await repo.update_account("avail_1", status="active")

        acct = await repo.get_available_account("x", "outreach")
        assert acct is not None
        assert acct["account_id"] == "avail_1"

    @pytest.mark.asyncio
    async def test_get_available_excludes_inactive(self, repo: PostgresRepository) -> None:
        await repo.insert_account(account_id="inact_1", platform="x", account_type="outreach")
        # Default status is 'nurturing', not 'active'
        acct = await repo.get_available_account("x", "outreach")
        assert acct is None

    @pytest.mark.asyncio
    async def test_touch_updates_last_used(self, repo: PostgresRepository) -> None:
        await repo.insert_account(account_id="touch_1", platform="x", account_type="crawl")
        await repo.touch_account("touch_1")
        accounts = await repo.get_accounts(platform="x")
        assert accounts[0]["last_used_at"] is not None


class TestOutreachCRUD:
    """Test outreach table operations."""

    @pytest.mark.asyncio
    async def test_insert_and_get_pending(self, repo: PostgresRepository) -> None:
        # Need a post and account first (FK constraints)
        await repo.insert_post(post_id="op_1", platform="x", user_id="u1", contents="help")
        await repo.insert_account(account_id="oa_1", platform="x", account_type="outreach")

        oid = await repo.insert_outreach(
            post_id="op_1",
            user_id="u1",
            account_id="oa_1",
            platform="x",
            outreach_type="reply",
            message="We can help!",
        )
        assert oid > 0

        pending = await repo.get_pending_outreach(platform="x")
        assert len(pending) == 1
        assert pending[0]["message"] == "We can help!"

    @pytest.mark.asyncio
    async def test_update_outreach_status(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="os_1", platform="x", user_id="u1", contents="c")
        await repo.insert_account(account_id="osa_1", platform="x", account_type="outreach")
        oid = await repo.insert_outreach(
            post_id="os_1",
            user_id="u1",
            account_id="osa_1",
            platform="x",
            outreach_type="dm",
            message="Hello!",
        )

        await repo.update_outreach_status(oid, "sent")
        pending = await repo.get_pending_outreach(platform="x")
        assert len(pending) == 0

    @pytest.mark.asyncio
    async def test_get_outreach_for_post(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="ofp_1", platform="x", user_id="u1", contents="c")
        await repo.insert_account(account_id="ofa_1", platform="x", account_type="outreach")
        await repo.insert_outreach(
            post_id="ofp_1",
            user_id="u1",
            account_id="ofa_1",
            platform="x",
            outreach_type="reply",
            message="msg1",
        )
        await repo.insert_outreach(
            post_id="ofp_1",
            user_id="u1",
            account_id="ofa_1",
            platform="x",
            outreach_type="dm",
            message="msg2",
        )

        actions = await repo.get_outreach_for_post("ofp_1")
        assert len(actions) == 2

    @pytest.mark.asyncio
    async def test_count_outreach(self, repo: PostgresRepository) -> None:
        await repo.insert_post(post_id="co_1", platform="x", user_id="u1", contents="c")
        await repo.insert_account(account_id="coa_1", platform="x", account_type="outreach")
        await repo.insert_outreach(
            post_id="co_1",
            user_id="u1",
            account_id="coa_1",
            platform="x",
            outreach_type="reply",
            message="m",
        )
        count = await repo.count_outreach(platform="x", status="pending")
        assert count == 1
