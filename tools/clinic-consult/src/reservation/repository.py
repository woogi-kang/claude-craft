"""Reservation repository with parameterised queries.

Follows the same patterns as ``db.repository`` -- synchronous SQLite
with parameterised queries and column-name whitelisting.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from src.reservation.models import (
    ALL_RESERVATION_TABLES,
    RESERVATION_INDEXES,
    VALID_STATUSES,
)

# Valid state transitions: current_status -> set of allowed next statuses
VALID_TRANSITIONS: dict[str, frozenset[str]] = {
    "created": frozenset({"contacting", "failed"}),
    "contacting": frozenset({"greeting_sent", "failed"}),
    "greeting_sent": frozenset({"negotiating", "paused_for_human", "timed_out", "failed"}),
    "negotiating": frozenset({
        "confirmed", "declined", "paused_for_human", "timed_out", "failed",
    }),
    "paused_for_human": frozenset({"negotiating", "confirmed", "declined", "failed"}),
    "confirmed": frozenset({"completed", "failed"}),
    "declined": frozenset(),
    "completed": frozenset(),
    "timed_out": frozenset({"contacting", "failed"}),
    "failed": frozenset(),
}

from src.utils.time_utils import utc_now_iso


_RESERVATION_UPDATE_COLUMNS = frozenset({
    "clinic_id", "clinic_name", "clinic_contact_url", "contact_platform",
    "patient_name", "patient_nationality", "patient_age", "patient_gender",
    "patient_contact",
    "procedure_name", "preferred_dates", "preferred_time", "notes",
    "status", "confirmed_date", "confirmed_time", "confirmed_price",
    "confirmed_doctor", "clinic_instructions", "decline_reason",
    "turn_count", "paused_reason", "error_message",
    "contacted_at", "confirmed_at", "completed_at", "updated_at",
})



class ReservationRepository:
    """CRUD operations for reservations and reservation messages."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None

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
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def init_db(self) -> None:
        """Create reservation tables, indexes, and run migrations."""
        conn = self._get_conn()
        for ddl in ALL_RESERVATION_TABLES:
            conn.execute(ddl)
        for idx in RESERVATION_INDEXES:
            conn.execute(idx)
        self._run_migrations(conn)
        conn.commit()

    def _run_migrations(self, conn: sqlite3.Connection) -> None:
        """Apply schema migrations for existing databases."""
        from src.reservation.models import (
            MIGRATION_ADD_CONTACT_PLATFORM,
            MIGRATION_RENAME_KAKAO_URL,
        )

        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(reservations)").fetchall()
        }
        # Migration: rename clinic_kakao_url -> clinic_contact_url
        if "clinic_kakao_url" in columns and "clinic_contact_url" not in columns:
            conn.execute(MIGRATION_RENAME_KAKAO_URL)
        # Migration: add contact_platform column
        if "contact_platform" not in columns:
            conn.execute(MIGRATION_ADD_CONTACT_PLATFORM)
        # Migration: add patient_age and patient_gender columns
        if "patient_age" not in columns:
            conn.execute("ALTER TABLE reservations ADD COLUMN patient_age INTEGER")
        if "patient_gender" not in columns:
            conn.execute("ALTER TABLE reservations ADD COLUMN patient_gender TEXT")

    # ------------------------------------------------------------------
    # Reservations
    # ------------------------------------------------------------------

    def create_reservation(
        self,
        request_id: str,
        clinic_name: str,
        patient_name: str,
        procedure_name: str,
        *,
        clinic_id: int | None = None,
        clinic_contact_url: str | None = None,
        contact_platform: str = "kakao",
        patient_nationality: str = "JP",
        patient_age: int | None = None,
        patient_gender: str | None = None,
        patient_contact: str | None = None,
        preferred_dates: list[str] | None = None,
        preferred_time: str = "any",
        notes: str | None = None,
    ) -> int:
        """Create a new reservation. Returns the reservation id."""
        conn = self._get_conn()
        now = utc_now_iso()
        dates_json = json.dumps(preferred_dates) if preferred_dates else None
        cursor = conn.execute(
            """INSERT INTO reservations
               (request_id, clinic_id, clinic_name, clinic_contact_url,
                contact_platform,
                patient_name, patient_nationality, patient_age, patient_gender,
                patient_contact,
                procedure_name, preferred_dates, preferred_time, notes,
                status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'created', ?, ?)""",
            (request_id, clinic_id, clinic_name, clinic_contact_url,
             contact_platform,
             patient_name, patient_nationality, patient_age, patient_gender,
             patient_contact,
             procedure_name, dates_json, preferred_time, notes,
             now, now),
        )
        conn.commit()
        return cursor.lastrowid or 0

    def get_reservation(self, reservation_id: int) -> dict[str, Any] | None:
        """Get a reservation by id."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM reservations WHERE id = ?",
            (reservation_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_request_id(self, request_id: str) -> dict[str, Any] | None:
        """Get a reservation by request_id."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM reservations WHERE request_id = ?",
            (request_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_reservation(self, reservation_id: int, **kwargs: Any) -> bool:
        """Update reservation fields. Returns True if updated.

        Raises ValueError on invalid columns or illegal state transitions.
        """
        if not kwargs:
            return False
        invalid = set(kwargs.keys()) - _RESERVATION_UPDATE_COLUMNS
        if invalid:
            raise ValueError(f"Invalid column names: {invalid}")
        if "status" in kwargs:
            new_status = kwargs["status"]
            if new_status not in VALID_STATUSES:
                raise ValueError(f"Invalid status: {new_status}")
            # Enforce state machine transitions
            current = self.get_reservation(reservation_id)
            if current:
                cur_status = current["status"]
                allowed = VALID_TRANSITIONS.get(cur_status, frozenset())
                if new_status != cur_status and new_status not in allowed:
                    raise ValueError(
                        f"Invalid transition: {cur_status} -> {new_status}. "
                        f"Allowed: {sorted(allowed)}"
                    )

        conn = self._get_conn()
        kwargs["updated_at"] = utc_now_iso()
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values()) + [reservation_id]
        cursor = conn.execute(
            f"UPDATE reservations SET {set_clause} WHERE id = ?",
            values,
        )
        conn.commit()
        return cursor.rowcount > 0

    def list_reservations(
        self,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List reservations, optionally filtered by status."""
        conn = self._get_conn()
        if status:
            cursor = conn.execute(
                "SELECT * FROM reservations WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM reservations ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
        return [dict(row) for row in cursor.fetchall()]

    def list_active(self) -> list[dict[str, Any]]:
        """List reservations in active processing states."""
        conn = self._get_conn()
        active_statuses = ("created", "contacting", "greeting_sent", "negotiating")
        placeholders = ", ".join(["?"] * len(active_statuses))
        cursor = conn.execute(
            f"SELECT * FROM reservations WHERE status IN ({placeholders}) ORDER BY created_at ASC",
            active_statuses,
        )
        return [dict(row) for row in cursor.fetchall()]

    def list_paused(self) -> list[dict[str, Any]]:
        """List reservations waiting for human intervention."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM reservations WHERE status = 'paused_for_human' ORDER BY updated_at ASC",
        )
        return [dict(row) for row in cursor.fetchall()]

    # ------------------------------------------------------------------
    # Reservation messages
    # ------------------------------------------------------------------

    def add_message(
        self,
        reservation_id: int,
        direction: str,
        content: str,
        *,
        llm_provider: str | None = None,
        extracted_json: str | None = None,
        phase: str | None = None,
    ) -> int:
        """Record a conversation message. Returns the message id."""
        conn = self._get_conn()
        cursor = conn.execute(
            """INSERT INTO reservation_messages
               (reservation_id, direction, content, llm_provider, extracted_json, phase)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (reservation_id, direction, content, llm_provider, extracted_json, phase),
        )
        conn.commit()
        return cursor.lastrowid or 0

    def get_messages(
        self,
        reservation_id: int,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get conversation messages for a reservation, oldest first."""
        conn = self._get_conn()
        cursor = conn.execute(
            """SELECT * FROM reservation_messages
               WHERE reservation_id = ?
               ORDER BY id ASC LIMIT ?""",
            (reservation_id, limit),
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_last_incoming(self, reservation_id: int) -> dict[str, Any] | None:
        """Get the most recent incoming message for a reservation."""
        conn = self._get_conn()
        cursor = conn.execute(
            """SELECT * FROM reservation_messages
               WHERE reservation_id = ? AND direction = 'incoming'
               ORDER BY id DESC LIMIT 1""",
            (reservation_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def message_count(self, reservation_id: int) -> int:
        """Count total messages for a reservation."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT COUNT(*) FROM reservation_messages WHERE reservation_id = ?",
            (reservation_id,),
        )
        return cursor.fetchone()[0]
