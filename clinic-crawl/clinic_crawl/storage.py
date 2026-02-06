"""SQLite async storage with phase tracking for clinic crawl pipeline."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aiosqlite

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.enums import CrawlCategory, CrawlPhase, ExtractionMethod
from clinic_crawl.models.hospital import HospitalCrawlResult

logger = logging.getLogger(__name__)

_CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS crawl_progress (
    hospital_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phase TEXT NOT NULL DEFAULT 'pending',
    category TEXT,
    chain_domain TEXT,
    error_message TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS social_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    extraction_method TEXT NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES crawl_progress(hospital_no),
    UNIQUE(hospital_no, platform, url)
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    name TEXT,
    role TEXT NOT NULL DEFAULT 'specialist',
    photo_url TEXT,
    credentials_json TEXT,
    education_json TEXT,
    career_json TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES crawl_progress(hospital_no)
);

CREATE TABLE IF NOT EXISTS hospital_results (
    hospital_no INTEGER PRIMARY KEY,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES crawl_progress(hospital_no)
);

CREATE TABLE IF NOT EXISTS chain_patterns (
    domain TEXT PRIMARY KEY,
    selectors_json TEXT NOT NULL,
    sample_hospital_no INTEGER,
    verified_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_progress_phase ON crawl_progress(phase);
CREATE INDEX IF NOT EXISTS idx_progress_category ON crawl_progress(category);
CREATE INDEX IF NOT EXISTS idx_progress_chain ON crawl_progress(chain_domain);
CREATE INDEX IF NOT EXISTS idx_social_hospital ON social_links(hospital_no);
CREATE INDEX IF NOT EXISTS idx_doctors_hospital ON doctors(hospital_no);
"""


class ClinicStorageManager:
    """Manages SQLite storage for the clinic crawl pipeline."""

    def __init__(self, config: ClinicCrawlConfig) -> None:
        self._config = config
        self._db_path = config.storage.db_path
        self._db: aiosqlite.Connection | None = None
        self._in_batch = False

    async def __aenter__(self) -> ClinicStorageManager:
        await self.initialize()
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.close()

    def _ensure_db(self) -> aiosqlite.Connection:
        if self._db is None:
            msg = "StorageManager not initialized. Use async context manager."
            raise RuntimeError(msg)
        return self._db

    async def _maybe_commit(self) -> None:
        """Commit unless inside a batch context."""
        if not self._in_batch:
            db = self._ensure_db()
            await db.commit()

    @asynccontextmanager
    async def batch(self) -> AsyncIterator[None]:
        """Batch multiple writes into a single transaction.

        Usage::

            async with storage.batch():
                for item in items:
                    await storage.save_social_link(...)
            # Single commit happens here
        """
        db = self._ensure_db()
        self._in_batch = True
        try:
            yield
            await db.commit()
        except BaseException:
            await db.rollback()
            raise
        finally:
            self._in_batch = False

    async def initialize(self) -> None:
        """Create database and tables."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db = await aiosqlite.connect(str(self._db_path))
        self._db.row_factory = aiosqlite.Row
        await self._db.execute("PRAGMA journal_mode=WAL")
        await self._db.execute("PRAGMA busy_timeout=5000")
        await self._db.executescript(_CREATE_TABLES)
        await self._db.commit()
        logger.info("Storage initialized: %s", self._db_path)

    async def close(self) -> None:
        """Close database connection."""
        if self._db:
            await self._db.close()
            self._db = None

    # --- Progress tracking ---

    async def upsert_hospital(
        self,
        hospital_no: int,
        name: str,
        phase: CrawlPhase = CrawlPhase.PENDING,
        category: CrawlCategory | None = None,
        chain_domain: str | None = None,
    ) -> None:
        """Insert or update a hospital's progress record."""
        db = self._ensure_db()
        await db.execute(
            """
            INSERT INTO crawl_progress (hospital_no, name, phase, category, chain_domain)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(hospital_no) DO UPDATE SET
                phase = excluded.phase,
                category = COALESCE(excluded.category, crawl_progress.category),
                chain_domain = COALESCE(excluded.chain_domain, crawl_progress.chain_domain),
                updated_at = datetime('now')
            """,
            (hospital_no, name, phase.value, category.value if category else None, chain_domain),
        )
        await self._maybe_commit()

    async def update_phase(
        self,
        hospital_no: int,
        phase: CrawlPhase,
        error_message: str | None = None,
    ) -> None:
        """Update a hospital's crawl phase."""
        db = self._ensure_db()
        await db.execute(
            """
            UPDATE crawl_progress
            SET phase = ?, error_message = ?, updated_at = datetime('now')
            WHERE hospital_no = ?
            """,
            (phase.value, error_message, hospital_no),
        )
        await self._maybe_commit()

    async def get_hospitals_by_phase(self, phase: CrawlPhase) -> list[dict]:
        """Get all hospitals in a given phase."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT * FROM crawl_progress WHERE phase = ?",
            (phase.value,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def get_phase_counts(self) -> dict[str, int]:
        """Get count of hospitals in each phase."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT phase, COUNT(*) as cnt FROM crawl_progress GROUP BY phase"
        )
        rows = await cursor.fetchall()
        return {row["phase"]: row["cnt"] for row in rows}

    # --- Social links ---

    async def save_social_link(
        self,
        hospital_no: int,
        platform: str,
        url: str,
        extraction_method: ExtractionMethod,
        confidence: float = 1.0,
    ) -> None:
        """Save a social link, ignoring duplicates."""
        db = self._ensure_db()
        await db.execute(
            """
            INSERT OR IGNORE INTO social_links
                (hospital_no, platform, url, extraction_method, confidence)
            VALUES (?, ?, ?, ?, ?)
            """,
            (hospital_no, platform, url, extraction_method.value, confidence),
        )
        await self._maybe_commit()

    async def get_social_links(self, hospital_no: int) -> list[dict]:
        """Get all social links for a hospital."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT * FROM social_links WHERE hospital_no = ?",
            (hospital_no,),
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    # --- Doctors ---

    async def save_doctor(
        self,
        hospital_no: int,
        name: str | None,
        role: str,
        photo_url: str | None = None,
        credentials: list[dict] | None = None,
        education: list[str] | None = None,
        career: list[str] | None = None,
    ) -> None:
        """Save a doctor record."""
        db = self._ensure_db()
        await db.execute(
            """
            INSERT INTO doctors
                (hospital_no, name, role, photo_url, credentials_json, education_json, career_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                hospital_no,
                name,
                role,
                photo_url,
                json.dumps(credentials or [], ensure_ascii=False),
                json.dumps(education or [], ensure_ascii=False),
                json.dumps(career or [], ensure_ascii=False),
            ),
        )
        await self._maybe_commit()

    # --- Full results ---

    async def save_result(self, result: HospitalCrawlResult) -> None:
        """Save full crawl result as JSON."""
        db = self._ensure_db()
        await db.execute(
            """
            INSERT INTO hospital_results (hospital_no, result_json)
            VALUES (?, ?)
            ON CONFLICT(hospital_no) DO UPDATE SET
                result_json = excluded.result_json,
                created_at = datetime('now')
            """,
            (result.hospital_no, result.model_dump_json()),
        )
        await self._maybe_commit()

    # --- Chain patterns ---

    async def save_chain_pattern(
        self,
        domain: str,
        selectors: dict,
        sample_hospital_no: int,
    ) -> None:
        """Save or update chain pattern selectors."""
        db = self._ensure_db()
        await db.execute(
            """
            INSERT INTO chain_patterns (domain, selectors_json, sample_hospital_no)
            VALUES (?, ?, ?)
            ON CONFLICT(domain) DO UPDATE SET
                selectors_json = excluded.selectors_json,
                updated_at = datetime('now')
            """,
            (domain, json.dumps(selectors, ensure_ascii=False), sample_hospital_no),
        )
        await self._maybe_commit()

    async def get_chain_pattern(self, domain: str) -> dict | None:
        """Get chain pattern selectors for a domain."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT selectors_json FROM chain_patterns WHERE domain = ?",
            (domain,),
        )
        row = await cursor.fetchone()
        if row:
            return json.loads(row["selectors_json"])
        return None

    # --- Report queries ---

    async def get_category_counts(self) -> dict[str, int]:
        """Get count of hospitals in each category."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT category, COUNT(*) as cnt FROM crawl_progress"
            " GROUP BY category ORDER BY cnt DESC"
        )
        return {row["category"]: row["cnt"] for row in await cursor.fetchall()}

    async def get_social_platform_counts(self) -> dict[str, int]:
        """Get count of social links per platform."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT platform, COUNT(*) as cnt FROM social_links GROUP BY platform ORDER BY cnt DESC"
        )
        return {row["platform"]: row["cnt"] for row in await cursor.fetchall()}

    async def get_hospitals_with_social_count(self) -> int:
        """Get count of hospitals that have at least one social link."""
        db = self._ensure_db()
        cursor = await db.execute("SELECT COUNT(DISTINCT hospital_no) as cnt FROM social_links")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0

    async def get_doctor_stats(self) -> tuple[int, int]:
        """Return (hospitals_with_doctors, total_doctors)."""
        db = self._ensure_db()
        cursor = await db.execute("SELECT COUNT(DISTINCT hospital_no) as cnt FROM doctors")
        row = await cursor.fetchone()
        hospitals = row["cnt"] if row else 0

        cursor = await db.execute("SELECT COUNT(*) as cnt FROM doctors")
        row = await cursor.fetchone()
        total = row["cnt"] if row else 0
        return hospitals, total

    async def get_chain_domain_count(self) -> int:
        """Get count of known chain domains."""
        db = self._ensure_db()
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM chain_patterns")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0

    async def get_top_chains(self, limit: int = 10) -> dict[str, int]:
        """Get top chain domains by hospital count."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT chain_domain, COUNT(*) as cnt FROM crawl_progress "
            "WHERE chain_domain IS NOT NULL GROUP BY chain_domain "
            "ORDER BY cnt DESC LIMIT ?",
            (limit,),
        )
        return {row["chain_domain"]: row["cnt"] for row in await cursor.fetchall()}

    async def get_extraction_method_counts(self) -> dict[str, int]:
        """Get count of social links per extraction method."""
        db = self._ensure_db()
        cursor = await db.execute(
            "SELECT extraction_method, COUNT(*) as cnt FROM social_links"
            " GROUP BY extraction_method ORDER BY cnt DESC"
        )
        return {row["extraction_method"]: row["cnt"] for row in await cursor.fetchall()}

    async def get_total_hospitals(self) -> int:
        """Get total number of hospitals."""
        db = self._ensure_db()
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM crawl_progress")
        row = await cursor.fetchone()
        return row["cnt"] if row else 0

    async def recover_interrupted(self) -> int:
        """Reset in-progress items to previous phase on startup."""
        db = self._ensure_db()
        cursor = await db.execute(
            """
            UPDATE crawl_progress
            SET phase = 'prescan_done', error_message = NULL, updated_at = datetime('now')
            WHERE phase = 'failed'
            """
        )
        await self._maybe_commit()
        count = cursor.rowcount or 0
        if count:
            logger.info("Recovered %d failed items back to prescan_done", count)
        return count
