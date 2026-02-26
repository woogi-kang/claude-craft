"""Tests for storage_manager: save_result, export, migrations, validation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from storage_manager import (
    _escape_csv_formula,
    _normalize,
    _normalize_platform,
    _validate_channel,
    _validate_channel_url,
    export_csv,
    get_db,
    save_result,
)

# ============================================================================
# get_db
# ============================================================================

class TestGetDb:
    def test_creates_db_file(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = get_db(db_path)
        assert Path(db_path).exists()
        conn.close()

    def test_creates_parent_dirs(self, tmp_path):
        db_path = str(tmp_path / "sub" / "dir" / "test.db")
        conn = get_db(db_path)
        assert Path(db_path).exists()
        conn.close()

    def test_wal_mode_enabled(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = get_db(db_path)
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        assert mode == "wal"
        conn.close()

    def test_schema_tables_created(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = get_db(db_path)
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()]
        assert "hospitals" in tables
        assert "social_channels" in tables
        assert "doctors" in tables
        assert "crawl_errors" in tables
        conn.close()

    def test_schema_version_3(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        conn = get_db(db_path)
        # Check place_id column exists
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(hospitals)").fetchall()]
        assert "place_id" in cols
        assert "csv_no" in cols
        # Check doctors has profile_raw_json
        doc_cols = [r["name"] for r in conn.execute("PRAGMA table_info(doctors)").fetchall()]
        assert "profile_raw_json" in doc_cols
        assert "page_text" in doc_cols
        assert "source_url" in doc_cols
        assert "screenshot_path" in doc_cols
        conn.close()


# ============================================================================
# _normalize
# ============================================================================

class TestNormalize:
    def test_nfc_normalization(self):
        import unicodedata
        nfd = unicodedata.normalize("NFD", "가나다")
        result = _normalize(nfd)
        assert result == unicodedata.normalize("NFC", "가나다")

    def test_empty_string(self):
        assert _normalize("") == ""

    def test_none_returns_none(self):
        assert _normalize(None) is None

    def test_ascii_unchanged(self):
        assert _normalize("hello") == "hello"


# ============================================================================
# _escape_csv_formula
# ============================================================================

class TestEscapeCsvFormula:
    def test_escapes_equals(self):
        assert _escape_csv_formula("=SUM(A1)") == "'=SUM(A1)"

    def test_escapes_plus(self):
        assert _escape_csv_formula("+cmd|'/C calc'!A0") == "'+cmd|'/C calc'!A0"

    def test_escapes_minus(self):
        assert _escape_csv_formula("-1+1") == "'-1+1"

    def test_escapes_at(self):
        assert _escape_csv_formula("@import") == "'@import"

    def test_normal_string_unchanged(self):
        assert _escape_csv_formula("Hello World") == "Hello World"

    def test_empty_string_unchanged(self):
        assert _escape_csv_formula("") == ""

    def test_non_string_unchanged(self):
        assert _escape_csv_formula(123) == 123


# ============================================================================
# _validate_channel_url
# ============================================================================

class TestValidateChannelUrl:
    def test_valid_https(self):
        assert _validate_channel_url("https://pf.kakao.com/_test", "KakaoTalk") is True

    def test_valid_http(self):
        assert _validate_channel_url("http://example.com", "NaverBlog") is True

    def test_valid_phone(self):
        assert _validate_channel_url("tel:010-1234-5678", "Phone") is True

    def test_valid_phone_no_prefix(self):
        assert _validate_channel_url("010-1234-5678", "Phone") is True

    def test_valid_phone_international(self):
        assert _validate_channel_url("+821012345678", "Phone") is True

    def test_valid_phone_international_with_separator_after_code(self):
        assert _validate_channel_url("+82-10-1234-5678", "Phone") is True

    def test_invalid_phone(self):
        assert _validate_channel_url("not-a-phone", "Phone") is False

    def test_valid_sms(self):
        assert _validate_channel_url("sms:01012345678", "SMS") is True

    def test_invalid_sms(self):
        assert _validate_channel_url("https://example.com", "SMS") is False

    def test_empty_url(self):
        assert _validate_channel_url("", "KakaoTalk") is False

    def test_kakao_deep_link(self):
        assert _validate_channel_url("kakao://channel/chat", "KakaoTalk") is True


# ============================================================================
# _validate_channel
# ============================================================================

class TestValidateChannel:
    def test_valid_channel_passthrough(self):
        ch = {"platform": "KakaoTalk", "url": "https://pf.kakao.com/_test", "confidence": 0.9}
        result = _validate_channel(ch)
        assert result["confidence"] == 0.9

    def test_clamps_confidence_above_1(self):
        ch = {"platform": "KakaoTalk", "url": "https://pf.kakao.com/_test", "confidence": 1.5}
        result = _validate_channel(ch)
        assert result["confidence"] == 1.0

    def test_clamps_confidence_below_0(self):
        ch = {"platform": "KakaoTalk", "url": "https://pf.kakao.com/_test", "confidence": -0.5}
        result = _validate_channel(ch)
        assert result["confidence"] == 0.0


# ============================================================================
# _normalize_platform
# ============================================================================

class TestNormalizePlatform:
    def test_kakao_lowercase(self):
        assert _normalize_platform("kakao") == "KakaoTalk"

    def test_kakaotalk_lowercase(self):
        assert _normalize_platform("kakaotalk") == "KakaoTalk"

    def test_naver_blog(self):
        assert _normalize_platform("naver_blog") == "NaverBlog"

    def test_instagram(self):
        assert _normalize_platform("instagram") == "Instagram"

    def test_youtube(self):
        assert _normalize_platform("youtube") == "YouTube"

    def test_unknown_passthrough(self):
        assert _normalize_platform("UnknownPlatform") == "UnknownPlatform"

    def test_phone(self):
        assert _normalize_platform("phone") == "Phone"


# ============================================================================
# save_result
# ============================================================================

class TestSaveResult:
    def test_insert_new_hospital(self, temp_db, sample_crawl_result):
        data = sample_crawl_result(place_id="100", name="Test Clinic")
        save_result(temp_db, data)

        conn = get_db(temp_db)
        row = conn.execute("SELECT * FROM hospitals WHERE place_id='100'").fetchone()
        assert row is not None
        assert row["name"] == "Test Clinic"
        assert row["status"] == "success"
        conn.close()

    def test_upsert_existing_hospital(self, temp_db, sample_crawl_result):
        save_result(temp_db, sample_crawl_result(place_id="200", name="First"))
        save_result(temp_db, sample_crawl_result(place_id="200", name="Updated"))

        conn = get_db(temp_db)
        row = conn.execute("SELECT * FROM hospitals WHERE place_id='200'").fetchone()
        assert row["name"] == "Updated"
        conn.close()

    def test_skip_failed_overwrite_of_success(self, temp_db, sample_crawl_result):
        save_result(temp_db, sample_crawl_result(place_id="300", status="success"))
        save_result(temp_db, sample_crawl_result(place_id="300", status="failed"))

        conn = get_db(temp_db)
        row = conn.execute("SELECT * FROM hospitals WHERE place_id='300'").fetchone()
        assert row["status"] == "success"  # not overwritten
        conn.close()

    def test_saves_social_channels(self, temp_db, sample_crawl_result, sample_channel):
        data = sample_crawl_result(
            place_id="400",
            social_channels=[sample_channel(platform="KakaoTalk", url="https://pf.kakao.com/_test")],
        )
        save_result(temp_db, data)

        conn = get_db(temp_db)
        channels = conn.execute("SELECT * FROM social_channels WHERE place_id='400'").fetchall()
        assert len(channels) == 1
        assert channels[0]["platform"] == "KakaoTalk"
        conn.close()

    def test_saves_doctors(self, temp_db, sample_crawl_result, sample_doctor):
        data = sample_crawl_result(
            place_id="500",
            doctors=[sample_doctor(name="김상우", role="대표원장")],
        )
        save_result(temp_db, data)

        conn = get_db(temp_db)
        doctors = conn.execute("SELECT * FROM doctors WHERE place_id='500'").fetchall()
        assert len(doctors) == 1
        assert doctors[0]["name"] == "김상우"
        conn.close()

    def test_saves_profile_raw_json(self, temp_db, sample_crawl_result, sample_doctor):
        data = sample_crawl_result(
            place_id="501",
            doctors=[sample_doctor(
                name="박지연",
                profile_raw=["서울대학교 의과대학 졸업", "삼성서울병원 피부과 전공의"],
            )],
        )
        save_result(temp_db, data)

        conn = get_db(temp_db)
        doc = conn.execute("SELECT * FROM doctors WHERE place_id='501'").fetchone()
        import json
        profile = json.loads(doc["profile_raw_json"])
        assert len(profile) == 2
        assert "서울대학교" in profile[0]
        conn.close()

    def test_saves_errors_as_string(self, temp_db, sample_crawl_result):
        data = sample_crawl_result(place_id="600", errors=["Timeout occurred"])
        save_result(temp_db, data)

        conn = get_db(temp_db)
        errors = conn.execute("SELECT * FROM crawl_errors WHERE place_id='600'").fetchall()
        assert len(errors) == 1
        assert errors[0]["message"] == "Timeout occurred"
        conn.close()

    def test_saves_errors_as_dict(self, temp_db, sample_crawl_result):
        data = sample_crawl_result(
            place_id="700",
            errors=[{"type": "navigation", "message": "DNS failed", "step": "step1", "retryable": True}],
        )
        save_result(temp_db, data)

        conn = get_db(temp_db)
        errors = conn.execute("SELECT * FROM crawl_errors WHERE place_id='700'").fetchall()
        assert errors[0]["error_type"] == "navigation"
        assert errors[0]["retryable"] == 1
        conn.close()

    def test_replaces_channels_on_recrawl(self, temp_db, sample_crawl_result, sample_channel):
        save_result(temp_db, sample_crawl_result(
            place_id="800",
            social_channels=[sample_channel(platform="KakaoTalk")],
        ))
        save_result(temp_db, sample_crawl_result(
            place_id="800",
            social_channels=[sample_channel(platform="NaverTalk", url="https://talk.naver.com/ct/test")],
        ))

        conn = get_db(temp_db)
        channels = conn.execute("SELECT * FROM social_channels WHERE place_id='800'").fetchall()
        assert len(channels) == 1
        assert channels[0]["platform"] == "NaverTalk"
        conn.close()

    def test_replaces_doctors_on_recrawl(self, temp_db, sample_crawl_result, sample_doctor):
        save_result(temp_db, sample_crawl_result(
            place_id="900",
            doctors=[sample_doctor(name="김상우")],
        ))
        save_result(temp_db, sample_crawl_result(
            place_id="900",
            doctors=[sample_doctor(name="이지연")],
        ))

        conn = get_db(temp_db)
        doctors = conn.execute("SELECT * FROM doctors WHERE place_id='900'").fetchall()
        assert len(doctors) == 1
        assert doctors[0]["name"] == "이지연"
        conn.close()


# ============================================================================
# export_csv
# ============================================================================

class TestExportCsv:
    def test_produces_csv_files(self, temp_db, sample_crawl_result, sample_channel, sample_doctor, tmp_path):
        save_result(temp_db, sample_crawl_result(
            place_id="1000",
            social_channels=[sample_channel()],
            doctors=[sample_doctor()],
        ))
        output_dir = str(tmp_path / "exports")
        export_csv(temp_db, output_dir)

        assert (Path(output_dir) / "hospitals.csv").exists()
        assert (Path(output_dir) / "social_channels.csv").exists()
        assert (Path(output_dir) / "doctors.csv").exists()
