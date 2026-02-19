"""SQLite repository with parameterised queries.

Every public function in this module uses parameterised SQL to prevent
injection.  The module is synchronous -- SQLite does not benefit from
async I/O given its file-level locking.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.db.models import ALL_TABLES, INDEXES, MIGRATIONS


class Repository:
    """Thin wrapper around an SQLite connection.

    Parameters
    ----------
    db_path:
        Filesystem path to the SQLite database file.  Parent directories
        are created automatically.
    """

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self._db_path),
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL;")
            self._conn.execute("PRAGMA foreign_keys=ON;")
        return self._conn

    def close(self) -> None:
        """Close the underlying database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------
    # Schema bootstrap
    # ------------------------------------------------------------------

    def init_db(self) -> None:
        """Create all tables and indexes if they do not exist.

        Also runs schema migrations for existing databases (ALTER TABLE
        statements that may already have been applied are silently ignored).
        """
        conn = self._get_conn()
        for ddl in ALL_TABLES:
            conn.execute(ddl)
        for idx in INDEXES:
            conn.execute(idx)
        # Run migrations for existing databases
        for migration in MIGRATIONS:
            try:
                conn.execute(migration)
            except sqlite3.OperationalError:
                pass  # Column already exists
        conn.commit()

    # ------------------------------------------------------------------
    # Tweets
    # ------------------------------------------------------------------

    def insert_tweet(self, tweet_data: dict[str, Any]) -> bool:
        """Insert a tweet record.  Returns ``True`` on success.

        Silently skips duplicates (based on ``tweet_id`` UNIQUE constraint).
        """
        conn = self._get_conn()
        columns = ", ".join(tweet_data.keys())
        placeholders = ", ".join(["?"] * len(tweet_data))
        sql = f"INSERT OR IGNORE INTO tweets ({columns}) VALUES ({placeholders})"
        cursor = conn.execute(sql, list(tweet_data.values()))
        conn.commit()
        return cursor.rowcount > 0

    def get_tweets_by_status(self, status: str) -> list[dict[str, Any]]:
        """Return all tweets matching the given pipeline *status*."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM tweets WHERE status = ? ORDER BY tweet_timestamp DESC",
            (status,),
        )
        return [dict(row) for row in cursor.fetchall()]

    def update_tweet_status(
        self, tweet_id: str, status: str, **kwargs: Any
    ) -> bool:
        """Update a tweet's status and optional extra fields.

        Parameters
        ----------
        tweet_id:
            The unique tweet identifier (``tweet_id`` column, not the
            auto-increment ``id``).
        status:
            New pipeline status value.
        **kwargs:
            Additional column=value pairs to update.

        Returns
        -------
        bool
            ``True`` if a row was updated.
        """
        conn = self._get_conn()
        fields = {"status": status, "updated_at": datetime.now(timezone.utc).isoformat(), **kwargs}
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [tweet_id]
        cursor = conn.execute(
            f"UPDATE tweets SET {set_clause} WHERE tweet_id = ?",
            values,
        )
        conn.commit()
        return cursor.rowcount > 0

    def get_tweet_by_id(self, tweet_id: str) -> dict[str, Any] | None:
        """Look up a single tweet by its ``tweet_id``."""
        conn = self._get_conn()
        cursor = conn.execute("SELECT * FROM tweets WHERE tweet_id = ?", (tweet_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def insert_user(self, user_data: dict[str, Any]) -> bool:
        """Insert a user record.  Skips duplicates on ``username``."""
        conn = self._get_conn()
        columns = ", ".join(user_data.keys())
        placeholders = ", ".join(["?"] * len(user_data))
        sql = f"INSERT OR IGNORE INTO users ({columns}) VALUES ({placeholders})"
        cursor = conn.execute(sql, list(user_data.values()))
        conn.commit()
        return cursor.rowcount > 0

    def get_user(self, username: str) -> dict[str, Any] | None:
        """Look up a user by ``username``."""
        conn = self._get_conn()
        cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_user(self, username: str, **kwargs: Any) -> bool:
        """Update arbitrary fields on a user row."""
        if not kwargs:
            return False
        conn = self._get_conn()
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [username]
        cursor = conn.execute(
            f"UPDATE users SET {set_clause} WHERE username = ?",
            values,
        )
        conn.commit()
        return cursor.rowcount > 0

    def is_user_contacted(self, username: str) -> bool:
        """Return ``True`` if the user has been contacted before."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT contact_count FROM users WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        return row["contact_count"] > 0

    # ------------------------------------------------------------------
    # Actions (audit log)
    # ------------------------------------------------------------------

    def record_action(
        self,
        action_type: str,
        tweet_id: str | None,
        username: str | None,
        details: str | None,
        status: str,
        error_message: str | None = None,
    ) -> int:
        """Insert an action record and return the new row id."""
        conn = self._get_conn()
        cursor = conn.execute(
            """INSERT INTO actions
               (action_type, tweet_id, username, details, status, error_message)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (action_type, tweet_id, username, details, status, error_message),
        )
        conn.commit()
        return cursor.lastrowid or 0

    # ------------------------------------------------------------------
    # Daily stats
    # ------------------------------------------------------------------

    def get_daily_stats(self, date: str) -> dict[str, Any] | None:
        """Return stats row for the given *date* (``YYYY-MM-DD``)."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM daily_stats WHERE date = ?", (date,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_daily_stats_range(
        self, start_date: str, end_date: str
    ) -> list[dict[str, Any]]:
        """Return all daily_stats rows within a date range (inclusive).

        Parameters
        ----------
        start_date:
            Start date as ``YYYY-MM-DD`` (inclusive).
        end_date:
            End date as ``YYYY-MM-DD`` (inclusive).

        Returns
        -------
        list[dict[str, Any]]
            List of stats rows ordered by date ascending.
        """
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM daily_stats WHERE date >= ? AND date <= ? ORDER BY date ASC",
            (start_date, end_date),
        )
        return [dict(row) for row in cursor.fetchall()]

    def update_daily_stats(self, date: str, **increments: int) -> None:
        """Upsert daily stats, incrementing the given counters.

        If no row exists for *date*, one is created first.  Each kwarg
        key must match a column name and its value is *added* to the
        current value.
        """
        conn = self._get_conn()

        # Ensure row exists
        conn.execute(
            "INSERT OR IGNORE INTO daily_stats (date) VALUES (?)",
            (date,),
        )

        if increments:
            set_parts = [f"{k} = {k} + ?" for k in increments]
            set_clause = ", ".join(set_parts)
            values = list(increments.values()) + [date]
            conn.execute(
                f"UPDATE daily_stats SET {set_clause} WHERE date = ?",
                values,
            )

        conn.commit()

    # ------------------------------------------------------------------
    # Config (key-value store)
    # ------------------------------------------------------------------

    def get_config(self, key: str) -> str | None:
        """Retrieve a configuration value by key.

        Returns
        -------
        str | None
            The stored value, or ``None`` if the key does not exist.
        """
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT value FROM config WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row["value"] if row else None

    def set_config(self, key: str, value: str) -> None:
        """Insert or update a configuration value.

        Parameters
        ----------
        key:
            Configuration key.
        value:
            Configuration value (stored as text).
        """
        conn = self._get_conn()
        conn.execute(
            "INSERT INTO config (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP",
            (key, value),
        )
        conn.commit()
