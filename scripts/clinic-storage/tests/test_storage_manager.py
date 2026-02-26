"""Tests for storage_manager: DB operations, save, export, validation."""

import json
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from storage_manager import (
    VALID_PLATFORMS,
    VALID_STATUSES,
    _escape_csv_formula,
    _normalize,
    _validate_channel_url,
    get_db,
    save_result,
    show_stats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _temp_db() -> str:
    """Create a temporary DB path for testing."""
    f = tempfile.NamedTemporaryFile(suffix=".db", delete=False, prefix="test_clinic_")
    f.close()
    return f.name


def _sample_result(place_id: str = "99999999", **overrides) -> dict:
    """Build a minimal valid crawl result dict."""
    base = {
        "place_id": place_id,
        "name": "테스트의원",
        "url": "https://example.com",
        "status": "success",
        "social_channels": [],
        "doctors": [],
        "errors": [],
    }
    base.update(overrides)
    return base


# ===========================================================================
# Database initialization
# ===========================================================================

class TestGetDb:
    def test_creates_tables(self):
        db = _temp_db()
        conn = get_db(db)
        tables = [
            r[0] for r in
            conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        ]
        assert "hospitals" in tables
        assert "social_channels" in tables
        assert "doctors" in tables
        assert "crawl_errors" in tables
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_wal_mode_enabled(self):
        db = _temp_db()
        conn = get_db(db)
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal"
        conn.close()
        # Clean up WAL files too
        Path(db).unlink(missing_ok=True)
        Path(db + "-wal").unlink(missing_ok=True)
        Path(db + "-shm").unlink(missing_ok=True)

    def test_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            db = str(Path(tmpdir) / "sub" / "deep" / "test.db")
            conn = get_db(db)
            assert Path(db).exists()
            conn.close()


# ===========================================================================
# save_result
# ===========================================================================

class TestSaveResult:
    def test_saves_basic_hospital(self):
        db = _temp_db()
        save_result(db, _sample_result())
        conn = get_db(db)
        row = conn.execute("SELECT * FROM hospitals WHERE place_id = '99999999'").fetchone()
        assert row is not None
        assert row["name"] == "테스트의원"
        assert row["status"] == "success"
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_saves_social_channels(self):
        db = _temp_db()
        data = _sample_result(social_channels=[
            {"platform": "KakaoTalk", "url": "https://pf.kakao.com/_test", "extraction_method": "dom_static"},
            {"platform": "Phone", "url": "tel:01012345678", "extraction_method": "phone_text"},
        ])
        save_result(db, data)
        conn = get_db(db)
        channels = conn.execute(
            "SELECT * FROM social_channels WHERE place_id = '99999999'"
        ).fetchall()
        assert len(channels) == 2
        platforms = {ch["platform"] for ch in channels}
        assert "KakaoTalk" in platforms
        assert "Phone" in platforms
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_saves_doctors(self):
        db = _temp_db()
        data = _sample_result(doctors=[
            {"name": "김상우", "role": "대표원장", "profile_raw": ["서울대 졸업", "피부과 전문의"]},
            {"name": "이지연", "role": "부원장", "profile_raw": []},
        ])
        save_result(db, data)
        conn = get_db(db)
        docs = conn.execute(
            "SELECT * FROM doctors WHERE place_id = '99999999'"
        ).fetchall()
        assert len(docs) == 2
        # Check profile_raw is stored as JSON
        doc1 = [d for d in docs if d["name"] == "김상우"][0]
        profile = json.loads(doc1["profile_raw_json"])
        assert "서울대 졸업" in profile
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_saves_errors(self):
        db = _temp_db()
        data = _sample_result(
            status="failed",
            errors=[
                {"type": "timeout", "message": "Page timed out", "step": "navigate", "retryable": True},
                "Simple string error",
            ],
        )
        save_result(db, data)
        conn = get_db(db)
        errors = conn.execute(
            "SELECT * FROM crawl_errors WHERE place_id = '99999999'"
        ).fetchall()
        assert len(errors) == 2
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_upsert_updates_existing(self):
        db = _temp_db()
        save_result(db, _sample_result(status="partial"))
        save_result(db, _sample_result(status="success"))
        conn = get_db(db)
        row = conn.execute("SELECT status FROM hospitals WHERE place_id = '99999999'").fetchone()
        assert row["status"] == "success"
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_does_not_overwrite_success_with_empty_failure(self):
        db = _temp_db()
        # First: success with data
        save_result(db, _sample_result(
            status="success",
            doctors=[{"name": "김상우", "role": "원장"}],
            social_channels=[{"platform": "Phone", "url": "tel:01012345678"}],
        ))
        # Second: failed with no data
        save_result(db, _sample_result(status="failed"))
        conn = get_db(db)
        row = conn.execute("SELECT status FROM hospitals WHERE place_id = '99999999'").fetchone()
        assert row["status"] == "success"  # should NOT be overwritten
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_clears_old_channels_on_recrawl(self):
        db = _temp_db()
        save_result(db, _sample_result(social_channels=[
            {"platform": "KakaoTalk", "url": "https://pf.kakao.com/_old"},
        ]))
        save_result(db, _sample_result(social_channels=[
            {"platform": "Instagram", "url": "https://instagram.com/new"},
        ]))
        conn = get_db(db)
        channels = conn.execute(
            "SELECT platform FROM social_channels WHERE place_id = '99999999'"
        ).fetchall()
        assert len(channels) == 1
        assert channels[0]["platform"] == "Instagram"
        conn.close()
        Path(db).unlink(missing_ok=True)

    def test_saves_doctor_with_legacy_fields(self):
        db = _temp_db()
        data = _sample_result(doctors=[{
            "name": "박서준",
            "role": "전문의",
            "education": ["서울대 졸업"],
            "career": ["강남병원"],
            "credentials": ["피부과학회 정회원"],
        }])
        save_result(db, data)
        conn = get_db(db)
        doc = conn.execute("SELECT * FROM doctors WHERE place_id = '99999999'").fetchone()
        profile = json.loads(doc["profile_raw_json"])
        assert "서울대 졸업" in profile
        assert "강남병원" in profile
        assert "피부과학회 정회원" in profile
        conn.close()
        Path(db).unlink(missing_ok=True)


# ===========================================================================
# Validation helpers
# ===========================================================================

class TestNormalize:
    def test_nfc_normalization(self):
        # NFD decomposed Korean
        nfd = "\u1100\u1161\u11a8"  # 각 in NFD
        result = _normalize(nfd)
        assert result == "각"

    def test_empty_string(self):
        assert _normalize("") == ""

    def test_none_returns_none(self):
        assert _normalize(None) is None


class TestEscapeCsvFormula:
    def test_escapes_equals(self):
        assert _escape_csv_formula("=SUM(A1)") == "'=SUM(A1)"

    def test_escapes_plus(self):
        assert _escape_csv_formula("+1234") == "'+1234"

    def test_escapes_minus(self):
        assert _escape_csv_formula("-1234") == "'-1234"

    def test_escapes_at(self):
        assert _escape_csv_formula("@import") == "'@import"

    def test_no_escape_normal(self):
        assert _escape_csv_formula("normal text") == "normal text"

    def test_empty_string(self):
        assert _escape_csv_formula("") == ""


class TestValidateChannelUrl:
    def test_valid_kakao_url(self):
        assert _validate_channel_url("https://pf.kakao.com/_test", "KakaoTalk") is True

    def test_valid_phone(self):
        assert _validate_channel_url("tel:010-1234-5678", "Phone") is True

    def test_valid_phone_with_country(self):
        assert _validate_channel_url("tel:+82-10-1234-5678", "Phone") is True

    def test_invalid_phone(self):
        assert _validate_channel_url("tel:123", "Phone") is False

    def test_valid_sms(self):
        assert _validate_channel_url("sms:01012345678", "SMS") is True

    def test_empty_url(self):
        assert _validate_channel_url("", "KakaoTalk") is False

    def test_invalid_scheme(self):
        assert _validate_channel_url("ftp://example.com", "Instagram") is False


# ===========================================================================
# Constants validation
# ===========================================================================

class TestValidConstants:
    def test_valid_platforms_complete(self):
        expected = {"KakaoTalk", "NaverTalk", "Instagram", "YouTube",
                    "Phone", "SMS", "Line", "WhatsApp", "WeChat"}
        assert expected.issubset(VALID_PLATFORMS)

    def test_valid_statuses_complete(self):
        expected = {"success", "partial", "failed", "archived",
                    "requires_manual", "age_restricted", "robots_blocked"}
        assert expected.issubset(VALID_STATUSES)
