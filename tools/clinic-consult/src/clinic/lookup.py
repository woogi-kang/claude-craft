"""Clinic lookup from the hospitals.db database.

This module provides read-only access to the crawled clinic data,
including messenger channel URLs (KakaoTalk, LINE) and doctor information.
"""

from __future__ import annotations

import json
import sqlite3
import unicodedata
from pathlib import Path
from typing import Any

from src.clinic.models import ClinicInfo, DoctorInfo

# Default path to the hospitals database (read-only)
# lookup.py -> clinic -> src -> clinic-consult -> tools -> claude-craft
_CLAUDE_CRAFT_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_DB_PATH = _CLAUDE_CRAFT_ROOT / "data" / "clinic-results" / "hospitals.db"


def _normalize(text: str) -> str:
    """NFC-normalize and strip whitespace for Korean text matching."""
    return unicodedata.normalize("NFC", text).strip()


def _parse_json_list(raw: str | None) -> list[str]:
    """Safely parse a JSON array string into a list of strings."""
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(item) for item in data if item]
    except (json.JSONDecodeError, TypeError):
        pass
    return []


class ClinicLookup:
    """Read-only lookup against the crawled hospitals database."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = Path(db_path) if db_path else _DEFAULT_DB_PATH
        self._conn: sqlite3.Connection | None = None

    def _get_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(
                str(self._db_path),
                detect_types=sqlite3.PARSE_DECLTYPES,
            )
            self._conn.row_factory = sqlite3.Row
            # Read-only: no WAL needed
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # ------------------------------------------------------------------
    # Lookup methods
    # ------------------------------------------------------------------

    def find_by_name(self, name: str) -> list[ClinicInfo]:
        """Search clinics by name (exact or partial match).

        Returns a list of matching clinics, ordered by relevance
        (exact match first, then partial matches).
        """
        conn = self._get_conn()
        normalized = _normalize(name)

        # Exact match first
        cursor = conn.execute(
            "SELECT * FROM hospitals WHERE name = ?",
            (normalized,),
        )
        rows = cursor.fetchall()

        # Partial match if no exact match
        if not rows:
            cursor = conn.execute(
                "SELECT * FROM hospitals WHERE name LIKE ?",
                (f"%{normalized}%",),
            )
            rows = cursor.fetchall()

        return [self._build_clinic_info(dict(row)) for row in rows]

    def find_by_id(self, hospital_no: int) -> ClinicInfo | None:
        """Look up a clinic by its hospital_no."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM hospitals WHERE hospital_no = ?",
            (hospital_no,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self._build_clinic_info(dict(row))

    def search(
        self, query: str, limit: int = 20, platform: str | None = None,
    ) -> list[ClinicInfo]:
        """Search clinics by name for autocomplete suggestions.

        Clinics with a matching messenger channel are prioritized.
        If *platform* is given, only clinics with that platform are returned.
        """
        conn = self._get_conn()
        normalized = _normalize(query)
        platform_filter = self._resolve_platform_name(platform) if platform else None

        if platform_filter:
            cursor = conn.execute(
                """SELECT h.*, sc.url as channel_url
                   FROM hospitals h
                   INNER JOIN social_channels sc
                     ON h.hospital_no = sc.hospital_no AND sc.platform = ?
                   WHERE h.name LIKE ?
                   ORDER BY
                     CASE WHEN h.name = ? THEN 0 ELSE 1 END,
                     h.name
                   LIMIT ?""",
                (platform_filter, f"%{normalized}%", normalized, limit),
            )
        else:
            cursor = conn.execute(
                """SELECT h.*, sc.url as channel_url
                   FROM hospitals h
                   LEFT JOIN social_channels sc
                     ON h.hospital_no = sc.hospital_no
                       AND sc.platform IN ('KakaoTalk', 'Line')
                   WHERE h.name LIKE ?
                   ORDER BY
                     CASE WHEN sc.url IS NOT NULL THEN 0 ELSE 1 END,
                     CASE WHEN h.name = ? THEN 0 ELSE 1 END,
                     h.name
                   LIMIT ?""",
                (f"%{normalized}%", normalized, limit),
            )
        results: list[ClinicInfo] = []
        seen: set[int] = set()
        for row in cursor.fetchall():
            row_dict = dict(row)
            hno = row_dict["hospital_no"]
            if hno in seen:
                continue
            seen.add(hno)
            results.append(self._build_clinic_info(row_dict))
        return results

    def list_with_platform(
        self, platform: str = "kakao", limit: int = 100, offset: int = 0,
    ) -> list[ClinicInfo]:
        """List clinics that have a channel for the given platform."""
        conn = self._get_conn()
        platform_name = self._resolve_platform_name(platform)
        cursor = conn.execute(
            """SELECT DISTINCT h.*
               FROM hospitals h
               INNER JOIN social_channels sc
                 ON h.hospital_no = sc.hospital_no AND sc.platform = ?
               ORDER BY h.name
               LIMIT ? OFFSET ?""",
            (platform_name, limit, offset),
        )
        return [self._build_clinic_info(dict(row)) for row in cursor.fetchall()]

    def list_with_kakao(self, limit: int = 100, offset: int = 0) -> list[ClinicInfo]:
        """List clinics that have KakaoTalk channels (backward compat)."""
        return self.list_with_platform("kakao", limit, offset)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_clinic_info(self, hospital: dict[str, Any]) -> ClinicInfo:
        """Build a ClinicInfo from a hospital row + related data."""
        hno = hospital["hospital_no"]

        # Get all messenger URLs
        contact_urls = self._get_contact_urls(hno)

        # Get doctors
        doctors = self._get_doctors(hno)

        return ClinicInfo(
            hospital_no=hno,
            name=hospital.get("name", ""),
            contact_urls=contact_urls,
            phone=hospital.get("phone"),
            address=hospital.get("address"),
            website=hospital.get("final_url") or hospital.get("url"),
            doctors=doctors,
        )

    def _get_contact_urls(self, hospital_no: int) -> dict[str, str]:
        """Get all messenger URLs for a clinic, keyed by platform."""
        conn = self._get_conn()
        cursor = conn.execute(
            """SELECT platform, url FROM social_channels
               WHERE hospital_no = ?
                 AND platform IN ('KakaoTalk', 'Line')
               ORDER BY confidence DESC""",
            (hospital_no,),
        )
        urls: dict[str, str] = {}
        for row in cursor.fetchall():
            platform = row["platform"]
            url = row["url"]
            if not url:
                continue
            key = self._platform_to_key(platform)
            if key and key not in urls:
                if key == "kakao" and "pf.kakao.com" not in url:
                    continue
                urls[key] = url
        return urls

    @staticmethod
    def _platform_to_key(platform: str) -> str | None:
        """Convert DB platform name to internal key."""
        mapping = {"KakaoTalk": "kakao", "Line": "line"}
        return mapping.get(platform)

    @staticmethod
    def _resolve_platform_name(platform: str) -> str:
        """Convert internal key to DB platform name."""
        from src.messenger import normalize_platform

        mapping = {"kakao": "KakaoTalk", "line": "Line"}
        return mapping.get(normalize_platform(platform), platform)

    def _get_doctors(self, hospital_no: int) -> list[DoctorInfo]:
        """Get doctor records for a clinic."""
        conn = self._get_conn()
        cursor = conn.execute(
            "SELECT * FROM doctors WHERE hospital_no = ? ORDER BY id",
            (hospital_no,),
        )
        return [
            DoctorInfo(
                name=row["name"] or "",
                name_english=row["name_english"],
                role=row["role"] or "specialist",
                education=_parse_json_list(row["education_json"]),
                career=_parse_json_list(row["career_json"]),
                credentials=_parse_json_list(row["credentials_json"]),
            )
            for row in cursor.fetchall()
        ]
