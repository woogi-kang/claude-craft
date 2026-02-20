"""Clinic lookup from the hospitals.db database.

This module provides read-only access to the crawled clinic data,
including KakaoTalk channel URLs and doctor information.
"""

from __future__ import annotations

import json
import sqlite3
import unicodedata
from pathlib import Path
from typing import Any

from src.clinic.models import ClinicInfo, DoctorInfo

# Default path to the hospitals database (read-only)
# lookup.py -> clinic -> src -> kakao-consult -> tools -> claude-craft
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

    def search(self, query: str, limit: int = 20) -> list[ClinicInfo]:
        """Search clinics by name for autocomplete suggestions.

        Returns clinics with KakaoTalk channels prioritized.
        """
        conn = self._get_conn()
        normalized = _normalize(query)
        cursor = conn.execute(
            """SELECT h.*, sc.url as kakao_url
               FROM hospitals h
               LEFT JOIN social_channels sc
                 ON h.hospital_no = sc.hospital_no AND sc.platform = 'KakaoTalk'
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

    def list_with_kakao(self, limit: int = 100, offset: int = 0) -> list[ClinicInfo]:
        """List clinics that have KakaoTalk channels."""
        conn = self._get_conn()
        cursor = conn.execute(
            """SELECT DISTINCT h.*
               FROM hospitals h
               INNER JOIN social_channels sc
                 ON h.hospital_no = sc.hospital_no AND sc.platform = 'KakaoTalk'
               ORDER BY h.name
               LIMIT ? OFFSET ?""",
            (limit, offset),
        )
        return [self._build_clinic_info(dict(row)) for row in cursor.fetchall()]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_clinic_info(self, hospital: dict[str, Any]) -> ClinicInfo:
        """Build a ClinicInfo from a hospital row + related data."""
        conn = self._get_conn()
        hno = hospital["hospital_no"]

        # Get KakaoTalk URL
        kakao_url = self._get_kakao_url(hno)

        # Get doctors
        doctors = self._get_doctors(hno)

        return ClinicInfo(
            hospital_no=hno,
            name=hospital.get("name", ""),
            kakao_url=kakao_url,
            phone=hospital.get("phone"),
            address=hospital.get("address"),
            website=hospital.get("final_url") or hospital.get("url"),
            doctors=doctors,
        )

    def _get_kakao_url(self, hospital_no: int) -> str | None:
        """Get the best KakaoTalk URL for a clinic."""
        conn = self._get_conn()
        cursor = conn.execute(
            """SELECT url FROM social_channels
               WHERE hospital_no = ? AND platform = 'KakaoTalk'
               ORDER BY
                 CASE WHEN url LIKE '%/chat' THEN 0 ELSE 1 END,
                 confidence DESC
               LIMIT 1""",
            (hospital_no,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        url = row["url"]
        # Filter out malformed URLs
        if not url or "pf.kakao.com" not in url:
            return None
        return url

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
