"""Async PostgreSQL repository using asyncpg.

Provides CRUD operations for the unified outreach schema (posts,
accounts, outreach tables) with connection pooling.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import asyncpg

from outreach_shared.db.models import ALL_DDL
from outreach_shared.utils.logger import get_logger

logger = get_logger("postgres")


class PostgresRepository:
    """Async PostgreSQL repository with connection pooling.

    Parameters
    ----------
    dsn:
        PostgreSQL connection string
        (e.g. ``postgresql://user:pass@localhost:5432/outreach``).
    min_pool_size:
        Minimum number of connections in the pool.
    max_pool_size:
        Maximum number of connections in the pool.
    """

    def __init__(
        self,
        dsn: str,
        *,
        min_pool_size: int = 2,
        max_pool_size: int = 10,
    ) -> None:
        self._dsn = dsn
        self._min_pool_size = min_pool_size
        self._max_pool_size = max_pool_size
        self._pool: asyncpg.Pool | None = None  # type: ignore[type-arg]

    async def connect(self) -> None:
        """Create the connection pool and initialise the schema."""
        self._pool = await asyncpg.create_pool(
            self._dsn,
            min_size=self._min_pool_size,
            max_size=self._max_pool_size,
        )
        await self._init_schema()
        # Log only host/port/db, never credentials
        try:
            safe_dsn = self._dsn.split("@")[-1]
        except (AttributeError, IndexError):
            safe_dsn = "***"
        logger.info("postgres_connected", dsn=safe_dsn)

    async def close(self) -> None:
        """Close all connections in the pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("postgres_disconnected")

    async def _init_schema(self) -> None:
        """Create tables and indexes if they do not exist."""
        assert self._pool is not None
        async with self._pool.acquire() as conn:
            for ddl in ALL_DDL:
                await conn.execute(ddl)

    @property
    def pool(self) -> asyncpg.Pool:  # type: ignore[type-arg]
        """Return the connection pool, raising if not connected."""
        if self._pool is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        return self._pool

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    async def insert_post(
        self,
        *,
        post_id: str,
        platform: str,
        user_id: str,
        contents: str,
        username: str | None = None,
        intent_type: str | None = None,
        keyword_intent: str | None = None,
        likes_count: int = 0,
        comments_count: int = 0,
        retweets_count: int = 0,
        post_url: str | None = None,
        author_bio: str | None = None,
        author_followers: int = 0,
        search_keyword: str | None = None,
        post_created_at: datetime | None = None,
    ) -> int:
        """Insert a new post and return its serial id.

        If a post with the same ``post_id`` already exists, the insert
        is skipped and ``-1`` is returned.
        """
        sql = """\
            INSERT INTO posts (
                post_id, platform, user_id, username, contents,
                intent_type, keyword_intent,
                likes_count, comments_count, retweets_count,
                post_url, author_bio, author_followers,
                search_keyword, post_created_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)
            ON CONFLICT (post_id) DO NOTHING
            RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                sql,
                post_id,
                platform,
                user_id,
                username,
                contents,
                intent_type,
                keyword_intent,
                likes_count,
                comments_count,
                retweets_count,
                post_url,
                author_bio,
                author_followers,
                search_keyword,
                post_created_at,
            )
        return row["id"] if row else -1

    # Column allowlists for dynamic UPDATE queries (prevents SQL injection)
    _POSTS_ALLOWED_COLUMNS = frozenset(
        {
            "status",
            "intent_type",
            "keyword_intent",
            "llm_decision",
            "llm_rationale",
            "post_url",
            "author_bio",
            "author_followers",
            "likes_count",
            "comments_count",
            "retweets_count",
            "search_keyword",
            "post_created_at",
        }
    )
    _ACCOUNTS_ALLOWED_COLUMNS = frozenset(
        {
            "status",
            "maturity",
            "username",
            "proxy_ip",
            "daily_comment_count",
            "daily_dm_count",
            "daily_search_count",
            "last_warning_at",
            "last_used_at",
            "session_data_dir",
            "banned_at",
        }
    )
    _OUTREACH_ALLOWED_COLUMNS = frozenset(
        {
            "status",
            "error_message",
            "replied",
            "sent_at",
            "replied_at",
        }
    )

    async def update_post_status(
        self,
        post_id: str,
        status: str,
        **extra: Any,
    ) -> None:
        """Update the status of a post, with optional extra fields."""
        sets = ["status = $2"]
        vals: list[Any] = [post_id, status]
        idx = 3
        for col, val in extra.items():
            if col not in self._POSTS_ALLOWED_COLUMNS:
                raise ValueError(f"Disallowed column name: {col!r}")
            sets.append(f"{col} = ${idx}")
            vals.append(val)
            idx += 1
        sql = f"UPDATE posts SET {', '.join(sets)} WHERE post_id = $1"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, *vals)

    async def get_posts_by_status(
        self,
        status: str,
        platform: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Return posts matching the given status."""
        if platform:
            sql = (
                "SELECT * FROM posts WHERE status = $1 AND platform = $2 "
                "ORDER BY crawled_at LIMIT $3"
            )
            args: tuple[Any, ...] = (status, platform, limit)
        else:
            sql = "SELECT * FROM posts WHERE status = $1 ORDER BY crawled_at LIMIT $2"
            args = (status, limit)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]

    async def get_post(self, post_id: str) -> dict[str, Any] | None:
        """Return a single post by its post_id."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM posts WHERE post_id = $1", post_id)
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    async def insert_account(
        self,
        *,
        account_id: str,
        platform: str,
        account_type: str,
        username: str | None = None,
        proxy_ip: str | None = None,
        session_data_dir: str | None = None,
    ) -> None:
        """Insert or update an account."""
        sql = """\
            INSERT INTO accounts (
                account_id, platform, account_type, username,
                proxy_ip, session_data_dir
            ) VALUES ($1,$2,$3,$4,$5,$6)
            ON CONFLICT (account_id) DO UPDATE SET
                username = EXCLUDED.username,
                proxy_ip = EXCLUDED.proxy_ip,
                session_data_dir = EXCLUDED.session_data_dir
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                sql,
                account_id,
                platform,
                account_type,
                username,
                proxy_ip,
                session_data_dir,
            )

    async def get_available_account(
        self,
        platform: str,
        account_type: str,
    ) -> dict[str, Any] | None:
        """Return the least-recently-used active account for the given role."""
        sql = """\
            SELECT * FROM accounts
            WHERE platform = $1
              AND account_type = $2
              AND status = 'active'
            ORDER BY last_used_at ASC NULLS FIRST
            LIMIT 1
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(sql, platform, account_type)
        return dict(row) if row else None

    async def update_account(
        self,
        account_id: str,
        **fields: Any,
    ) -> None:
        """Update arbitrary fields on an account."""
        if not fields:
            return
        sets = []
        vals: list[Any] = [account_id]
        idx = 2
        for col, val in fields.items():
            if col not in self._ACCOUNTS_ALLOWED_COLUMNS:
                raise ValueError(f"Disallowed column name: {col!r}")
            sets.append(f"{col} = ${idx}")
            vals.append(val)
            idx += 1
        sql = f"UPDATE accounts SET {', '.join(sets)} WHERE account_id = $1"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, *vals)

    async def touch_account(self, account_id: str) -> None:
        """Update last_used_at to the current time."""
        now = datetime.now(tz=UTC)
        await self.update_account(account_id, last_used_at=now)

    async def get_accounts(
        self,
        platform: str | None = None,
        account_type: str | None = None,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """List accounts with optional filters."""
        conditions = []
        vals: list[Any] = []
        idx = 1
        if platform:
            conditions.append(f"platform = ${idx}")
            vals.append(platform)
            idx += 1
        if account_type:
            conditions.append(f"account_type = ${idx}")
            vals.append(account_type)
            idx += 1
        if status:
            conditions.append(f"status = ${idx}")
            vals.append(status)
            idx += 1

        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT * FROM accounts{where} ORDER BY created_at"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *vals)
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Outreach
    # ------------------------------------------------------------------

    async def insert_outreach(
        self,
        *,
        post_id: str,
        user_id: str,
        account_id: str,
        platform: str,
        outreach_type: str,
        message: str,
        scheduled_at: datetime | None = None,
    ) -> int:
        """Queue a new outreach action and return its id."""
        sql = """\
            INSERT INTO outreach (
                post_id, user_id, account_id, platform,
                outreach_type, message, scheduled_at
            ) VALUES ($1,$2,$3,$4,$5,$6,$7)
            RETURNING id
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                sql,
                post_id,
                user_id,
                account_id,
                platform,
                outreach_type,
                message,
                scheduled_at,
            )
        return row["id"]  # type: ignore[index]

    async def update_outreach_status(
        self,
        outreach_id: int,
        status: str,
        **extra: Any,
    ) -> None:
        """Update outreach status with optional extra fields."""
        sets = ["status = $2"]
        vals: list[Any] = [outreach_id, status]
        idx = 3
        for col, val in extra.items():
            if col not in self._OUTREACH_ALLOWED_COLUMNS:
                raise ValueError(f"Disallowed column name: {col!r}")
            sets.append(f"{col} = ${idx}")
            vals.append(val)
            idx += 1
        sql = f"UPDATE outreach SET {', '.join(sets)} WHERE id = $1"
        async with self.pool.acquire() as conn:
            await conn.execute(sql, *vals)

    async def get_pending_outreach(
        self,
        platform: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Return pending outreach actions ordered by schedule time."""
        if platform:
            sql = (
                "SELECT * FROM outreach WHERE status = 'pending' "
                "AND platform = $1 ORDER BY scheduled_at NULLS FIRST LIMIT $2"
            )
            args: tuple[Any, ...] = (platform, limit)
        else:
            sql = (
                "SELECT * FROM outreach WHERE status = 'pending' "
                "ORDER BY scheduled_at NULLS FIRST LIMIT $1"
            )
            args = (limit,)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *args)
        return [dict(r) for r in rows]

    async def get_outreach_for_post(self, post_id: str) -> list[dict[str, Any]]:
        """Return all outreach actions for a given post."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM outreach WHERE post_id = $1 ORDER BY created_at",
                post_id,
            )
        return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Stats helpers
    # ------------------------------------------------------------------

    async def count_posts(
        self,
        platform: str | None = None,
        status: str | None = None,
    ) -> int:
        """Count posts with optional filters."""
        conditions = []
        vals: list[Any] = []
        idx = 1
        if platform:
            conditions.append(f"platform = ${idx}")
            vals.append(platform)
            idx += 1
        if status:
            conditions.append(f"status = ${idx}")
            vals.append(status)
            idx += 1
        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT COUNT(*) FROM posts{where}"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(sql, *vals)  # type: ignore[return-value]

    async def count_outreach(
        self,
        platform: str | None = None,
        status: str | None = None,
    ) -> int:
        """Count outreach actions with optional filters."""
        conditions = []
        vals: list[Any] = []
        idx = 1
        if platform:
            conditions.append(f"platform = ${idx}")
            vals.append(platform)
            idx += 1
        if status:
            conditions.append(f"status = ${idx}")
            vals.append(status)
            idx += 1
        where = f" WHERE {' AND '.join(conditions)}" if conditions else ""
        sql = f"SELECT COUNT(*) FROM outreach{where}"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(sql, *vals)  # type: ignore[return-value]
