"""
Dual storage manager: JSON files + SQLite for resume support.

JSON files store full hospital data per place.
SQLite tracks crawl progress for resume capability.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Optional

import aiosqlite

from crawl.config import CrawlerConfig
from crawl.hospital_schema import NaverHospitalPlace

logger = logging.getLogger(__name__)

_CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS crawl_progress (
    search_name TEXT PRIMARY KEY,
    place_id TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS hospitals (
    place_id TEXT PRIMARY KEY,
    search_name TEXT NOT NULL,
    name TEXT NOT NULL,
    category TEXT,
    road_address TEXT,
    phone TEXT,
    photo_count INTEGER NOT NULL DEFAULT 0,
    data_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_progress_status ON crawl_progress(status);
CREATE INDEX IF NOT EXISTS idx_hospitals_search ON hospitals(search_name);
"""


class StorageManager:
    """Manages JSON output and SQLite progress tracking."""

    def __init__(self, config: CrawlerConfig) -> None:
        self._config = config
        self._output_dir = config.storage.output_dir
        self._db_path = config.storage.db_path
        self._json_dir = self._output_dir / "hospitals"
        self._db: Optional[aiosqlite.Connection] = None

    async def __aenter__(self) -> StorageManager:
        await self.initialize()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()

    def _ensure_db(self) -> aiosqlite.Connection:
        if self._db is None:
            raise RuntimeError(
                "StorageManager not initialized. Call initialize() first."
            )
        return self._db

    async def initialize(self) -> None:
        """Create directories and database tables."""
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._json_dir.mkdir(parents=True, exist_ok=True)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        self._db = await aiosqlite.connect(str(self._db_path))
        self._db.row_factory = aiosqlite.Row
        await self._db.execute("PRAGMA journal_mode=WAL")
        await self._db.execute("PRAGMA busy_timeout=5000")
        await self._db.executescript(_CREATE_TABLES)
        await self._db.commit()

        logger.info(
            "StorageManager initialized: db=%s, output=%s",
            self._db_path,
            self._output_dir,
        )

    async def recover_interrupted(self) -> int:
        """Reset in_progress items to pending on startup."""
        db = self._ensure_db()
        cursor = await db.execute(
            "UPDATE crawl_progress SET status = 'pending' "
            "WHERE status = 'in_progress'"
        )
        await db.commit()
        count = cursor.rowcount
        if count > 0:
            logger.info("Recovered %d interrupted hospitals to pending", count)
        return count

    async def register_hospitals(self, names: list[str]) -> int:
        """Register hospital names from CSV. Returns count of newly added."""
        db = self._ensure_db()

        cursor = await db.execute("SELECT COUNT(*) FROM crawl_progress")
        row = await cursor.fetchone()
        before = row[0] if row else 0

        await db.executemany(
            "INSERT OR IGNORE INTO crawl_progress (search_name, status) "
            "VALUES (?, 'pending')",
            [(name,) for name in names],
        )
        await db.commit()

        cursor = await db.execute("SELECT COUNT(*) FROM crawl_progress")
        row = await cursor.fetchone()
        after = row[0] if row else 0
        return after - before

    async def get_pending_hospitals(self) -> list[str]:
        """Return hospital names not yet crawled (including interrupted)."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT search_name FROM crawl_progress "
            "WHERE status IN ('pending', 'failed', 'in_progress') "
            "ORDER BY rowid"
        )
        rows = await cursor.fetchall()
        return [row["search_name"] for row in rows]

    async def is_place_crawled(self, place_id: str) -> bool:
        """Check if a place ID has already been successfully crawled."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT 1 FROM hospitals WHERE place_id = ?", (place_id,)
        )
        return await cursor.fetchone() is not None

    async def mark_in_progress(self, search_name: str) -> None:
        """Mark a hospital as currently being crawled."""
        db = self._ensure_db()
        await db.execute(
            "UPDATE crawl_progress SET status = 'in_progress', "
            "updated_at = datetime('now') WHERE search_name = ?",
            (search_name,),
        )
        await db.commit()

    async def save_hospital(
        self,
        hospital: NaverHospitalPlace,
        search_name: str,
    ) -> Path:
        """Save hospital data to SQLite first, then JSON file."""
        db = self._ensure_db()

        data = hospital.model_dump(mode="json")
        json_content = json.dumps(data, ensure_ascii=False, indent=2)

        safe_name = "".join(
            c if c.isalnum() or c in ("-", "_") else "_"
            for c in search_name
        ).strip("_") or "unnamed"
        name_hash = hashlib.md5(search_name.encode()).hexdigest()[:8]
        json_path = self._json_dir / f"{hospital.id}_{safe_name}_{name_hash}.json"

        # SQLite first (rollback-safe)
        try:
            await db.execute(
                "INSERT OR REPLACE INTO hospitals "
                "(place_id, search_name, name, category, road_address, "
                "phone, photo_count, data_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    hospital.id,
                    search_name,
                    hospital.name,
                    hospital.category,
                    hospital.road_address,
                    hospital.phone,
                    hospital.photo_count,
                    json.dumps(data, ensure_ascii=False),
                ),
            )
            await db.execute(
                "UPDATE crawl_progress SET place_id = ?, status = 'completed', "
                "updated_at = datetime('now') WHERE search_name = ?",
                (hospital.id, search_name),
            )
            await db.commit()
        except Exception:
            await db.rollback()
            raise

        # JSON file second (best-effort, DB is source of truth)
        json_path.write_text(json_content, encoding="utf-8")

        logger.info(
            "Saved hospital: place_id=%s, name=%s, photos=%d",
            hospital.id,
            hospital.name,
            hospital.photo_count,
        )
        return json_path

    async def mark_completed_duplicate(
        self, search_name: str, place_id: str
    ) -> None:
        """Mark a hospital as completed (duplicate of already-crawled place)."""
        db = self._ensure_db()
        await db.execute(
            "UPDATE crawl_progress SET place_id = ?, status = 'completed', "
            "error_message = 'duplicate', updated_at = datetime('now') "
            "WHERE search_name = ?",
            (place_id, search_name),
        )
        await db.commit()

    async def mark_failed(self, search_name: str, error: str) -> None:
        """Mark a hospital as failed with error message."""
        db = self._ensure_db()
        # Truncate error message to prevent DB bloat
        truncated = error[:2000] if len(error) > 2000 else error
        await db.execute(
            "UPDATE crawl_progress SET status = 'failed', error_message = ?, "
            "updated_at = datetime('now') WHERE search_name = ?",
            (truncated, search_name),
        )
        await db.commit()
        logger.warning("Hospital failed: search_name=%s, error=%s", search_name, error)

    async def get_summary(self) -> dict:
        """Return crawl progress summary."""
        db = self._ensure_db()

        summary = {}
        for status in ("pending", "in_progress", "completed", "failed"):
            cursor = await db.execute(
                "SELECT COUNT(*) as cnt FROM crawl_progress WHERE status = ?",
                (status,),
            )
            row = await cursor.fetchone()
            summary[status] = row["cnt"] if row else 0

        summary["total"] = sum(summary.values())

        cursor = await db.execute(
            "SELECT COALESCE(SUM(photo_count), 0) as total_photos FROM hospitals"
        )
        row = await cursor.fetchone()
        summary["total_photos"] = row["total_photos"] if row else 0

        return summary

    async def close(self) -> None:
        """Close database connection."""
        if self._db:
            try:
                await self._db.close()
            except Exception:
                logger.exception("Failed to close database")
            finally:
                self._db = None
