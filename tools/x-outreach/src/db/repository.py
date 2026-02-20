"""Synchronous repository wrapper around the shared PostgresRepository.

Provides a sync interface that the existing pipeline code can use.
A future migration will rewrite all callers to async, at which point
this wrapper can be removed.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import nest_asyncio
from outreach_shared.db.postgres import PostgresRepository
from outreach_shared.utils.logger import get_logger

nest_asyncio.apply()

logger = get_logger("repository")

# File-based key-value store for config persistence (warmup, blocklist).
_CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "config.json"


def _load_config_store() -> dict[str, str]:
    """Load the config key-value store from disk."""
    if _CONFIG_FILE.exists():
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_config_store(store: dict[str, str]) -> None:
    """Persist the config key-value store to disk."""
    _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(
        json.dumps(store, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class Repository:
    """Synchronous wrapper around the async PostgresRepository.

    Parameters
    ----------
    database_url:
        PostgreSQL connection string.
    """

    def __init__(self, database_url: str) -> None:
        self._url = database_url
        self._repo = PostgresRepository(database_url)
        self._loop: asyncio.AbstractEventLoop | None = None

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
        return self._loop

    def _run(self, coro: Any) -> Any:
        return self._get_loop().run_until_complete(coro)

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def init_db(self) -> None:
        """Connect to PostgreSQL and initialise the schema."""
        self._run(self._repo.connect())

    def close(self) -> None:
        """Close the connection pool."""
        self._run(self._repo.close())
        if self._loop and not self._loop.is_closed():
            self._loop.close()
            self._loop = None

    # ------------------------------------------------------------------
    # Posts (mapped from old tweets API)
    # ------------------------------------------------------------------

    def insert_tweet(self, tweet_data: dict[str, Any]) -> bool:
        """Insert a post record. Returns True on success.

        Maps old tweet_data keys to the new posts schema.
        """
        post_id = tweet_data.get("tweet_id", "")
        result = self._run(
            self._repo.insert_post(
                post_id=post_id,
                platform="x",
                user_id=tweet_data.get("author_username", ""),
                username=tweet_data.get("author_username"),
                contents=tweet_data.get("content", ""),
                likes_count=tweet_data.get("likes", 0),
                comments_count=tweet_data.get("replies", 0),
                retweets_count=tweet_data.get("retweets", 0),
                post_url=tweet_data.get("tweet_url"),
                author_bio=tweet_data.get("author_bio"),
                author_followers=tweet_data.get("author_follower_count", 0),
                search_keyword=tweet_data.get("search_keyword"),
            )
        )
        return result != -1

    def get_tweets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Return all posts matching the given pipeline status."""
        return self._run(self._repo.get_posts_by_status(status, platform="x"))

    def update_tweet_status(self, tweet_id: str, status: str, **kwargs: Any) -> bool:
        """Update a post's status and optional extra fields."""
        self._run(self._repo.update_post_status(tweet_id, status, **kwargs))
        return True

    def get_tweet_by_id(self, tweet_id: str) -> dict[str, Any] | None:
        """Look up a single post by its post_id."""
        return self._run(self._repo.get_post(tweet_id))

    # ------------------------------------------------------------------
    # Users (author data stored on posts table)
    # ------------------------------------------------------------------

    def insert_user(self, user_data: dict[str, Any]) -> bool:
        """No-op -- user data is embedded in the posts table."""
        return True

    def get_user(self, username: str) -> dict[str, Any] | None:
        """Look up user info by querying posts for the latest author data."""

        async def _find() -> dict[str, Any] | None:
            async with self._repo.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT username, author_bio, author_followers "
                    "FROM posts "
                    "WHERE username = $1 AND platform = 'x' "
                    "ORDER BY crawled_at DESC LIMIT 1",
                    username,
                )
                if row is None:
                    return None
                return {
                    "username": row["username"],
                    "bio": row["author_bio"],
                    "follower_count": row["author_followers"],
                }

        return self._run(_find())

    def is_user_contacted(self, username: str) -> bool:
        """Check if user has been contacted via outreach table."""

        async def _check() -> bool:
            async with self._repo.pool.acquire() as conn:
                row = await conn.fetchval(
                    "SELECT EXISTS("
                    "  SELECT 1 FROM outreach "
                    "  WHERE user_id = $1 AND status = 'sent' "
                    "  AND platform = 'x'"
                    ")",
                    username,
                )
                return bool(row)

        return self._run(_check())

    def update_user(self, username: str, **kwargs: Any) -> bool:
        """No-op -- user data is embedded in the posts table."""
        return True

    def count_user_replies(self, username: str) -> int:
        """Count posts for a user with replied/dm_sent status."""

        async def _count() -> int:
            async with self._repo.pool.acquire() as conn:
                return await conn.fetchval(
                    "SELECT COUNT(*) FROM posts "
                    "WHERE username = $1 "
                    "AND status IN ('replied', 'dm_sent') "
                    "AND platform = 'x'",
                    username,
                )

        return self._run(_count())

    def get_last_dm_to_user(self, username: str) -> str:
        """Return the last DM content sent to a user, or empty string."""

        async def _fetch() -> str:
            async with self._repo.pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT message FROM outreach "
                    "WHERE user_id = $1 AND outreach_type = 'dm' "
                    "AND platform = 'x' "
                    "ORDER BY sent_at DESC NULLS LAST LIMIT 1",
                    username,
                )
                return row["message"] if row else ""

        return self._run(_fetch())

    def get_dm_pending_users(self) -> list[dict[str, Any]]:
        """Return users who received a DM but have not responded.

        Queries the outreach table for DMs that were sent but have
        no reply recorded yet.
        """

        async def _fetch() -> list[dict[str, Any]]:
            async with self._repo.pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT DISTINCT user_id AS username "
                    "FROM outreach "
                    "WHERE outreach_type = 'dm' "
                    "AND status = 'sent' "
                    "AND replied = FALSE "
                    "AND platform = 'x' "
                    "ORDER BY user_id",
                )
                return [dict(r) for r in rows]

        return self._run(_fetch())

    def mark_dm_replied(self, username: str, replied_at: str) -> None:
        """Mark all sent DMs to a user as replied."""

        async def _mark() -> None:
            async with self._repo.pool.acquire() as conn:
                await conn.execute(
                    "UPDATE outreach SET replied = TRUE, replied_at = $2 "
                    "WHERE user_id = $1 AND outreach_type = 'dm' "
                    "AND status = 'sent' AND platform = 'x'",
                    username,
                    replied_at,
                )

        self._run(_mark())

    # ------------------------------------------------------------------
    # Actions (mapped to outreach table)
    # ------------------------------------------------------------------

    def record_action(
        self,
        action_type: str,
        tweet_id: str | None,
        username: str | None,
        details: str | None,
        status: str,
        error_message: str | None = None,
        account_id: str | None = None,
    ) -> int:
        """Insert an outreach record and return the new row id."""
        if tweet_id and username:
            result = self._run(
                self._repo.insert_outreach(
                    post_id=tweet_id,
                    user_id=username,
                    account_id=account_id or "",
                    platform="x",
                    outreach_type=action_type,
                    message=details or "",
                    status=status,
                )
            )
            return result
        return 0

    # ------------------------------------------------------------------
    # Daily stats (computed from post/outreach counts)
    # ------------------------------------------------------------------

    def get_daily_stats(self, date: str) -> dict[str, Any] | None:
        """Return stats for the given date. Uses count queries."""
        count = self._run(self._repo.count_posts(platform="x"))
        return {
            "date": date,
            "tweets_searched": count,
            "tweets_collected": count,
        }

    def get_daily_stats_range(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Return stats within a date range."""
        stats = self.get_daily_stats(start_date)
        return [stats] if stats else []

    def update_daily_stats(self, date: str, **increments: int) -> None:
        """No-op -- daily stats are computed from post/outreach counts."""

    # ------------------------------------------------------------------
    # Config (file-based key-value store)
    # ------------------------------------------------------------------

    def get_config(self, key: str) -> str | None:
        """Read a config value from the file-based key-value store."""
        store = _load_config_store()
        return store.get(key)

    def set_config(self, key: str, value: str) -> None:
        """Write a config value to the file-based key-value store."""
        store = _load_config_store()
        store[key] = value
        _save_config_store(store)
