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

from src.db.models import ALL_TABLES, INDEXES


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
        """Create all tables and indexes if they do not exist."""
        conn = self._get_conn()
        for ddl in ALL_TABLES:
            conn.execute(ddl)
        for idx in INDEXES:
            conn.execute(idx)
        conn.commit()

    # ------------------------------------------------------------------
    # Conversations
    # ------------------------------------------------------------------

    def upsert_conversation(
        self,
        chatroom_id: str,
        chatroom_name: str | None = None,
        sender_name: str | None = None,
    ) -> bool:
        """Insert or update a conversation record.

        Returns ``True`` if a new row was inserted, ``False`` if an
        existing row was updated.
        """
        conn = self._get_conn()
        now = datetime.now(timezone.utc).isoformat()

        # Try insert first
        cursor = conn.execute(
            """INSERT OR IGNORE INTO conversations
               (chatroom_id, chatroom_name, sender_name, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?)""",
            (chatroom_id, chatroom_name, sender_name, now, now),
        )
        inserted = cursor.rowcount > 0

        if not inserted:
            # Row already exists -- update mutable fields
            fields: dict[str, Any] = {"updated_at": now}
            if chatroom_name is not None:
                fields["chatroom_name"] = chatroom_name
            if sender_name is not None:
                fields["sender_name"] = sender_name
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            values = list(fields.values()) + [chatroom_id]
            conn.execute(
                f"UPDATE conversations SET {set_clause} WHERE chatroom_id = ?",
                values,
            )

        conn.commit()
        return inserted

    def get_conversation(self, chatroom_id: str) -> dict[str, Any] | None:
        """Look up a conversation by ``chatroom_id``."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM conversations WHERE chatroom_id = ?",
            (chatroom_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_conversation(self, chatroom_id: str, **kwargs: Any) -> bool:
        """Update arbitrary fields on a conversation row.

        Returns ``True`` if a row was updated.
        """
        if not kwargs:
            return False
        conn = self._get_conn()
        kwargs["updated_at"] = datetime.now(timezone.utc).isoformat()
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [chatroom_id]
        cursor = conn.execute(
            f"UPDATE conversations SET {set_clause} WHERE chatroom_id = ?",
            values,
        )
        conn.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    def insert_message(
        self,
        chatroom_id: str,
        direction: str,
        content: str,
        **kwargs: Any,
    ) -> int:
        """Insert a message record and return the new row id.

        Parameters
        ----------
        chatroom_id:
            The chatroom this message belongs to.
        direction:
            ``'incoming'`` or ``'outgoing'``.
        content:
            Message text.
        **kwargs:
            Optional columns: classification, confidence, llm_provider,
            template_id, response_time_ms.
        """
        conn = self._get_conn()
        fields = {
            "chatroom_id": chatroom_id,
            "direction": direction,
            "content": content,
            **kwargs,
        }
        columns = ", ".join(fields.keys())
        placeholders = ", ".join(["?"] * len(fields))
        cursor = conn.execute(
            f"INSERT INTO messages ({columns}) VALUES ({placeholders})",
            list(fields.values()),
        )
        conn.commit()
        return cursor.lastrowid or 0

    def get_conversation_history(
        self, chatroom_id: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        """Return the most recent messages for a chatroom.

        Results are ordered most-recent first.
        """
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM messages WHERE chatroom_id = ? ORDER BY id DESC LIMIT ?",
            (chatroom_id, limit),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_last_message(self, chatroom_id: str) -> dict[str, Any] | None:
        """Return the single most recent message for a chatroom."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM messages WHERE chatroom_id = ? ORDER BY id DESC LIMIT 1",
            (chatroom_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    # ------------------------------------------------------------------
    # Actions (audit log)
    # ------------------------------------------------------------------

    def record_action(
        self,
        action_type: str,
        chatroom_id: str | None,
        details: str | None,
        status: str,
        error_message: str | None = None,
    ) -> int:
        """Insert an action record and return the new row id."""
        conn = self._get_conn()
        cursor = conn.execute(
            """INSERT INTO actions
               (action_type, chatroom_id, details, status, error_message)
               VALUES (?, ?, ?, ?, ?)""",
            (action_type, chatroom_id, details, status, error_message),
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
    # Blocked users
    # ------------------------------------------------------------------

    def is_user_blocked(self, sender_name: str) -> bool:
        """Return ``True`` if the sender is in the blocked-users list."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT 1 FROM blocked_users WHERE sender_name = ?",
            (sender_name,),
        )
        return cursor.fetchone() is not None

    def block_user(self, sender_name: str, reason: str | None = None) -> bool:
        """Add a sender to the blocked-users list.

        Returns ``True`` if the user was newly blocked, ``False`` if
        they were already blocked.
        """
        conn = self._get_conn()
        cursor = conn.execute(
            "INSERT OR IGNORE INTO blocked_users (sender_name, reason) VALUES (?, ?)",
            (sender_name, reason),
        )
        conn.commit()
        return cursor.rowcount > 0
