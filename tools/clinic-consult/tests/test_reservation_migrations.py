"""Tests for reservation schema migration logic.

Covers _run_migrations() in ReservationRepository which handles:
- Renaming clinic_kakao_url -> clinic_contact_url
- Adding contact_platform column with default 'kakao'
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from src.reservation.repository import ReservationRepository


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_column_names(db_path: Path) -> set[str]:
    """Return the set of column names for the reservations table."""
    conn = sqlite3.connect(str(db_path))
    columns = {row[1] for row in conn.execute("PRAGMA table_info(reservations)").fetchall()}
    conn.close()
    return columns


def _create_old_schema_with_kakao_url(db_path: Path) -> None:
    """Create reservations table with the pre-migration schema.

    Has ``clinic_kakao_url`` instead of ``clinic_contact_url`` and no
    ``contact_platform`` column.  All other columns match the modern
    schema so that indexes can be created without error.
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id          TEXT    UNIQUE NOT NULL,
            clinic_id           INTEGER,
            clinic_name         TEXT    NOT NULL,
            clinic_kakao_url    TEXT,
            patient_name        TEXT    NOT NULL,
            patient_nationality TEXT    DEFAULT 'JP',
            patient_age         INTEGER,
            patient_gender      TEXT,
            patient_contact     TEXT,
            procedure_name      TEXT    NOT NULL,
            preferred_dates     TEXT,
            preferred_time      TEXT    DEFAULT 'any',
            notes               TEXT,
            status              TEXT    NOT NULL DEFAULT 'created',
            confirmed_date      TEXT,
            confirmed_time      TEXT,
            confirmed_price     TEXT,
            confirmed_doctor    TEXT,
            clinic_instructions TEXT,
            decline_reason      TEXT,
            turn_count          INTEGER DEFAULT 0,
            paused_reason       TEXT,
            error_message       TEXT,
            created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
            contacted_at        DATETIME,
            confirmed_at        DATETIME,
            completed_at        DATETIME,
            updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservation_messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id  INTEGER NOT NULL,
            direction       TEXT    NOT NULL,
            content         TEXT    NOT NULL,
            llm_provider    TEXT,
            extracted_json  TEXT,
            phase           TEXT,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        )
    """)
    conn.commit()
    conn.close()


def _create_partially_migrated_schema(db_path: Path) -> None:
    """Create reservations table that already has ``clinic_contact_url``
    but is missing ``contact_platform``.  All other columns match the
    modern schema so that indexes can be created without error.
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id                  INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id          TEXT    UNIQUE NOT NULL,
            clinic_id           INTEGER,
            clinic_name         TEXT    NOT NULL,
            clinic_contact_url  TEXT,
            patient_name        TEXT    NOT NULL,
            patient_nationality TEXT    DEFAULT 'JP',
            patient_age         INTEGER,
            patient_gender      TEXT,
            patient_contact     TEXT,
            procedure_name      TEXT    NOT NULL,
            preferred_dates     TEXT,
            preferred_time      TEXT    DEFAULT 'any',
            notes               TEXT,
            status              TEXT    NOT NULL DEFAULT 'created',
            confirmed_date      TEXT,
            confirmed_time      TEXT,
            confirmed_price     TEXT,
            confirmed_doctor    TEXT,
            clinic_instructions TEXT,
            decline_reason      TEXT,
            turn_count          INTEGER DEFAULT 0,
            paused_reason       TEXT,
            error_message       TEXT,
            created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
            contacted_at        DATETIME,
            confirmed_at        DATETIME,
            completed_at        DATETIME,
            updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservation_messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id  INTEGER NOT NULL,
            direction       TEXT    NOT NULL,
            content         TEXT    NOT NULL,
            llm_provider    TEXT,
            extracted_json  TEXT,
            phase           TEXT,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id)
        )
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Fixtures (local, no conftest dependency)
# ---------------------------------------------------------------------------

@pytest.fixture()
def db_path(tmp_path: Path) -> Path:
    """Return a temporary database file path."""
    return tmp_path / "reservations.db"


@pytest.fixture()
def fresh_repo(db_path: Path) -> ReservationRepository:
    """Provide a fresh ReservationRepository with init_db() called."""
    repo = ReservationRepository(db_path)
    repo.init_db()
    yield repo
    repo.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFreshDbHasNewColumns:
    """A freshly initialised database should contain the modern schema."""

    def test_clinic_contact_url_exists(self, fresh_repo: ReservationRepository, db_path: Path) -> None:
        columns = _get_column_names(db_path)
        assert "clinic_contact_url" in columns

    def test_contact_platform_exists(self, fresh_repo: ReservationRepository, db_path: Path) -> None:
        columns = _get_column_names(db_path)
        assert "contact_platform" in columns

    def test_old_kakao_url_absent(self, fresh_repo: ReservationRepository, db_path: Path) -> None:
        columns = _get_column_names(db_path)
        assert "clinic_kakao_url" not in columns


class TestMigrationRenamesKakaoUrl:
    """Starting from the old schema that has ``clinic_kakao_url``,
    init_db() should rename it to ``clinic_contact_url`` and add
    ``contact_platform``.
    """

    def test_old_column_removed(self, db_path: Path) -> None:
        _create_old_schema_with_kakao_url(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        columns = _get_column_names(db_path)
        repo.close()
        assert "clinic_kakao_url" not in columns

    def test_new_contact_url_column_present(self, db_path: Path) -> None:
        _create_old_schema_with_kakao_url(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        columns = _get_column_names(db_path)
        repo.close()
        assert "clinic_contact_url" in columns

    def test_contact_platform_added(self, db_path: Path) -> None:
        _create_old_schema_with_kakao_url(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        columns = _get_column_names(db_path)
        repo.close()
        assert "contact_platform" in columns


class TestMigrationAddsContactPlatform:
    """When ``clinic_contact_url`` already exists but ``contact_platform``
    does not, init_db() should add the missing column.
    """

    def test_contact_platform_added(self, db_path: Path) -> None:
        _create_partially_migrated_schema(db_path)
        # Verify the partially-migrated state before running migrations
        columns_before = _get_column_names(db_path)
        assert "clinic_contact_url" in columns_before
        assert "contact_platform" not in columns_before

        repo = ReservationRepository(db_path)
        repo.init_db()
        columns_after = _get_column_names(db_path)
        repo.close()
        assert "contact_platform" in columns_after

    def test_existing_columns_preserved(self, db_path: Path) -> None:
        _create_partially_migrated_schema(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        columns = _get_column_names(db_path)
        repo.close()
        assert "clinic_contact_url" in columns
        assert "request_id" in columns
        assert "clinic_name" in columns


class TestMigrationIdempotent:
    """Calling init_db() multiple times must not raise."""

    def test_double_init_no_error(self, db_path: Path) -> None:
        repo = ReservationRepository(db_path)
        repo.init_db()
        repo.init_db()
        repo.close()

    def test_triple_init_no_error(self, db_path: Path) -> None:
        repo = ReservationRepository(db_path)
        repo.init_db()
        repo.init_db()
        repo.init_db()
        repo.close()

    def test_idempotent_on_old_schema(self, db_path: Path) -> None:
        """Migrate an old schema, then call init_db() again."""
        _create_old_schema_with_kakao_url(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        repo.init_db()  # second call after migration
        columns = _get_column_names(db_path)
        repo.close()
        assert "clinic_contact_url" in columns
        assert "contact_platform" in columns
        assert "clinic_kakao_url" not in columns


class TestCreateWithPlatform:
    """Creating a reservation with an explicit contact_platform persists it."""

    def test_line_platform_persists(self, fresh_repo: ReservationRepository) -> None:
        rid = fresh_repo.create_reservation(
            request_id="REQ-LINE-001",
            clinic_name="Line Clinic",
            patient_name="Yamada",
            procedure_name="Botox",
            contact_platform="line",
        )
        row = fresh_repo.get_reservation(rid)
        assert row is not None
        assert row["contact_platform"] == "line"

    def test_instagram_platform_persists(self, fresh_repo: ReservationRepository) -> None:
        rid = fresh_repo.create_reservation(
            request_id="REQ-IG-001",
            clinic_name="IG Clinic",
            patient_name="Kim",
            procedure_name="Filler",
            contact_platform="instagram",
        )
        row = fresh_repo.get_reservation(rid)
        assert row is not None
        assert row["contact_platform"] == "instagram"


class TestCreateDefaultPlatform:
    """A reservation created without specifying contact_platform defaults to 'kakao'."""

    def test_default_is_kakao(self, fresh_repo: ReservationRepository) -> None:
        rid = fresh_repo.create_reservation(
            request_id="REQ-DEFAULT-001",
            clinic_name="Default Clinic",
            patient_name="Tanaka",
            procedure_name="Laser",
        )
        row = fresh_repo.get_reservation(rid)
        assert row is not None
        assert row["contact_platform"] == "kakao"

    def test_default_on_migrated_db(self, db_path: Path) -> None:
        """Even after migration from old schema, the default should be 'kakao'."""
        _create_old_schema_with_kakao_url(db_path)
        repo = ReservationRepository(db_path)
        repo.init_db()
        rid = repo.create_reservation(
            request_id="REQ-MIG-DEFAULT",
            clinic_name="Migrated Clinic",
            patient_name="Sato",
            procedure_name="Peel",
        )
        row = repo.get_reservation(rid)
        repo.close()
        assert row is not None
        assert row["contact_platform"] == "kakao"
