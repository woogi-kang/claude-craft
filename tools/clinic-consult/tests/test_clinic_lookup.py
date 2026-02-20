"""Tests for ClinicLookup against an in-memory SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from src.clinic.lookup import ClinicLookup, _normalize, _parse_json_list


# ------------------------------------------------------------------
# Fixtures (local, no conftest)
# ------------------------------------------------------------------

_SCHEMA = """\
CREATE TABLE hospitals (
    hospital_no INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT,
    address TEXT,
    url TEXT,
    final_url TEXT
);

CREATE TABLE social_channels (
    id INTEGER PRIMARY KEY,
    hospital_no INTEGER,
    platform TEXT,
    url TEXT,
    confidence REAL
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    hospital_no INTEGER,
    name TEXT,
    name_english TEXT,
    role TEXT,
    education_json TEXT,
    career_json TEXT,
    credentials_json TEXT
);
"""


def _seed(conn: sqlite3.Connection) -> None:
    """Insert seed data into the test database."""
    conn.executemany(
        "INSERT INTO hospitals (hospital_no, name, phone, address, url, final_url) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1, "Seoul Skin Clinic", "02-1234-5678", "Seoul Gangnam-gu",
             "http://seoulsk.kr", "https://seoulsk.kr"),
            (2, "Gangnam Derm", "02-9999-8888", "Seoul Gangnam-gu 2",
             "http://gangnamderm.kr", "https://gangnamderm.kr"),
            (3, "Both Platform Clinic", "02-5555-6666", "Seoul Seocho-gu",
             "http://both.kr", "https://both.kr"),
            (4, "No Channel Clinic", "02-0000-1111", "Seoul Mapo-gu",
             "http://nochannel.kr", "https://nochannel.kr"),
        ],
    )

    conn.executemany(
        "INSERT INTO social_channels (id, hospital_no, platform, url, confidence) "
        "VALUES (?, ?, ?, ?, ?)",
        [
            (1, 1, "KakaoTalk", "https://pf.kakao.com/_abc", 0.95),
            (2, 2, "Line", "https://line.me/R/ti/p/@gangnam", 0.90),
            (3, 3, "KakaoTalk", "https://pf.kakao.com/_both", 0.85),
            (4, 3, "Line", "https://line.me/R/ti/p/@both", 0.80),
        ],
    )

    conn.executemany(
        "INSERT INTO doctors (id, hospital_no, name, name_english, role, "
        "education_json, career_json, credentials_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (1, 1, "Kim", "Kim", "director", '["Seoul Univ"]', '["10yr"]', '["Board"]'),
        ],
    )

    conn.commit()


@pytest.fixture()
def db_path(tmp_path: Path) -> Path:
    """Create a temporary SQLite database with schema and seed data."""
    path = tmp_path / "hospitals_test.db"
    conn = sqlite3.connect(str(path))
    conn.executescript(_SCHEMA)
    _seed(conn)
    conn.close()
    return path


@pytest.fixture()
def lookup(db_path: Path) -> ClinicLookup:
    """Create a ClinicLookup backed by the test database."""
    lk = ClinicLookup(db_path=db_path)
    yield lk  # type: ignore[misc]
    lk.close()


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------


class TestNormalize:
    """Test the _normalize helper function."""

    def test_strips_whitespace(self) -> None:
        assert _normalize("  hello  ") == "hello"

    def test_nfc_normalization(self) -> None:
        # Korean NFD decomposed form should become NFC
        nfd = "\u1100\u1161\u1102\u1161"  # decomposed "가나"
        result = _normalize(nfd)
        assert result == "\uAC00\uB098"  # NFC "가나"

    def test_empty_string(self) -> None:
        assert _normalize("") == ""

    def test_already_normalized(self) -> None:
        assert _normalize("Seoul Skin Clinic") == "Seoul Skin Clinic"


class TestParseJsonList:
    """Test the _parse_json_list helper function."""

    def test_valid_json_array(self) -> None:
        assert _parse_json_list('["a", "b", "c"]') == ["a", "b", "c"]

    def test_empty_string(self) -> None:
        assert _parse_json_list("") == []

    def test_none_input(self) -> None:
        assert _parse_json_list(None) == []

    def test_invalid_json(self) -> None:
        assert _parse_json_list("not json at all") == []

    def test_non_array_json(self) -> None:
        # Valid JSON but not a list should return empty
        assert _parse_json_list('{"key": "value"}') == []

    def test_mixed_types_coerced_to_str(self) -> None:
        assert _parse_json_list('[1, "two", 3]') == ["1", "two", "3"]

    def test_null_items_filtered(self) -> None:
        # Items that are falsy (null -> None) should be filtered
        assert _parse_json_list('[null, "a", null]') == ["a"]

    def test_empty_array(self) -> None:
        assert _parse_json_list("[]") == []


# ------------------------------------------------------------------
# ClinicLookup.find_by_name
# ------------------------------------------------------------------


class TestFindByName:
    """Test find_by_name exact and partial matching."""

    def test_exact_match(self, lookup: ClinicLookup) -> None:
        results = lookup.find_by_name("Seoul Skin Clinic")
        assert len(results) == 1
        assert results[0].hospital_no == 1
        assert results[0].name == "Seoul Skin Clinic"

    def test_partial_match(self, lookup: ClinicLookup) -> None:
        # "Skin" should match "Seoul Skin Clinic" via LIKE
        results = lookup.find_by_name("Skin")
        assert len(results) == 1
        assert results[0].hospital_no == 1

    def test_partial_match_multiple(self, lookup: ClinicLookup) -> None:
        # "Clinic" appears in multiple hospital names
        results = lookup.find_by_name("Clinic")
        names = {r.name for r in results}
        assert "Seoul Skin Clinic" in names
        assert "Both Platform Clinic" in names
        assert "No Channel Clinic" in names

    def test_no_match(self, lookup: ClinicLookup) -> None:
        results = lookup.find_by_name("Nonexistent Hospital")
        assert results == []

    def test_exact_match_takes_priority(self, lookup: ClinicLookup) -> None:
        # When exact match exists, partial match should not run
        results = lookup.find_by_name("Gangnam Derm")
        assert len(results) == 1
        assert results[0].hospital_no == 2


# ------------------------------------------------------------------
# ClinicLookup.find_by_id
# ------------------------------------------------------------------


class TestFindById:
    """Test find_by_id with existing and missing hospitals."""

    def test_existing_hospital(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        assert clinic.hospital_no == 1
        assert clinic.name == "Seoul Skin Clinic"

    def test_missing_hospital(self, lookup: ClinicLookup) -> None:
        assert lookup.find_by_id(9999) is None

    def test_contact_urls_populated(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        assert "kakao" in clinic.contact_urls
        assert clinic.contact_urls["kakao"] == "https://pf.kakao.com/_abc"

    def test_line_contact_url(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(2)
        assert clinic is not None
        assert "line" in clinic.contact_urls
        assert clinic.contact_urls["line"] == "https://line.me/R/ti/p/@gangnam"

    def test_both_platforms(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(3)
        assert clinic is not None
        assert "kakao" in clinic.contact_urls
        assert "line" in clinic.contact_urls

    def test_no_channels(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(4)
        assert clinic is not None
        assert clinic.contact_urls == {}

    def test_phone_and_address(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        assert clinic.phone == "02-1234-5678"
        assert clinic.address == "Seoul Gangnam-gu"

    def test_website_uses_final_url(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        assert clinic.website == "https://seoulsk.kr"


# ------------------------------------------------------------------
# ClinicLookup.search
# ------------------------------------------------------------------


class TestSearch:
    """Test the search method with ranking and platform filtering."""

    def test_search_by_name(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Seoul")
        assert len(results) >= 1
        assert any(r.hospital_no == 1 for r in results)

    def test_search_prioritizes_messenger_channels(self, lookup: ClinicLookup) -> None:
        # "Clinic" matches hospitals 1, 3, 4.
        # Hospital 1 has kakao, hospital 3 has both, hospital 4 has none.
        # Clinics with channels should appear before those without.
        results = lookup.search("Clinic")
        has_channel = [r for r in results if r.contact_urls]
        no_channel = [r for r in results if not r.contact_urls]
        if has_channel and no_channel:
            # All clinics with channels should appear before those without
            last_channel_idx = max(
                results.index(r) for r in has_channel
            )
            first_no_channel_idx = min(
                results.index(r) for r in no_channel
            )
            assert last_channel_idx < first_no_channel_idx

    def test_search_with_kakao_platform_filter(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Clinic", platform="kakao")
        # Only hospitals with KakaoTalk should be returned
        hospital_nos = {r.hospital_no for r in results}
        assert 1 in hospital_nos  # Seoul Skin Clinic has kakao
        assert 3 in hospital_nos  # Both Platform Clinic has kakao
        assert 4 not in hospital_nos  # No Channel Clinic

    def test_search_with_line_platform_filter(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Clinic", platform="line")
        hospital_nos = {r.hospital_no for r in results}
        assert 3 in hospital_nos  # Both Platform Clinic has line
        assert 1 not in hospital_nos  # Seoul Skin Clinic has kakao only

    def test_search_limit(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Clinic", limit=1)
        assert len(results) <= 1

    def test_search_no_match(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Nonexistent")
        assert results == []

    def test_search_deduplicates(self, lookup: ClinicLookup) -> None:
        # Hospital 3 has two social channels; it should appear only once
        results = lookup.search("Both Platform")
        hospital_nos = [r.hospital_no for r in results]
        assert hospital_nos.count(3) == 1


# ------------------------------------------------------------------
# ClinicLookup.list_with_platform
# ------------------------------------------------------------------


class TestListWithPlatform:
    """Test listing clinics by platform."""

    def test_list_kakao_clinics(self, lookup: ClinicLookup) -> None:
        results = lookup.list_with_platform("kakao")
        hospital_nos = {r.hospital_no for r in results}
        assert 1 in hospital_nos  # Seoul Skin Clinic
        assert 3 in hospital_nos  # Both Platform Clinic
        assert 2 not in hospital_nos  # Gangnam Derm (line only)
        assert 4 not in hospital_nos  # No Channel Clinic

    def test_list_line_clinics(self, lookup: ClinicLookup) -> None:
        results = lookup.list_with_platform("line")
        hospital_nos = {r.hospital_no for r in results}
        assert 2 in hospital_nos  # Gangnam Derm
        assert 3 in hospital_nos  # Both Platform Clinic
        assert 1 not in hospital_nos  # Seoul Skin Clinic (kakao only)

    def test_list_with_limit(self, lookup: ClinicLookup) -> None:
        results = lookup.list_with_platform("kakao", limit=1)
        assert len(results) == 1

    def test_list_with_offset(self, lookup: ClinicLookup) -> None:
        all_results = lookup.list_with_platform("kakao")
        offset_results = lookup.list_with_platform("kakao", offset=1)
        if len(all_results) > 1:
            assert len(offset_results) == len(all_results) - 1

    def test_list_unknown_platform_empty(self, lookup: ClinicLookup) -> None:
        results = lookup.list_with_platform("wechat")
        assert results == []


# ------------------------------------------------------------------
# ClinicLookup.list_with_kakao (backward compat alias)
# ------------------------------------------------------------------


class TestListWithKakao:
    """Test backward-compatible list_with_kakao alias."""

    def test_returns_same_as_list_with_platform_kakao(self, lookup: ClinicLookup) -> None:
        kakao_results = lookup.list_with_platform("kakao")
        alias_results = lookup.list_with_kakao()
        assert len(kakao_results) == len(alias_results)
        kakao_nos = {r.hospital_no for r in kakao_results}
        alias_nos = {r.hospital_no for r in alias_results}
        assert kakao_nos == alias_nos

    def test_limit_forwarded(self, lookup: ClinicLookup) -> None:
        results = lookup.list_with_kakao(limit=1)
        assert len(results) <= 1

    def test_offset_forwarded(self, lookup: ClinicLookup) -> None:
        all_results = lookup.list_with_kakao()
        offset_results = lookup.list_with_kakao(offset=1)
        if len(all_results) > 1:
            assert len(offset_results) == len(all_results) - 1


# ------------------------------------------------------------------
# Static methods
# ------------------------------------------------------------------


class TestPlatformToKey:
    """Test _platform_to_key static method."""

    def test_kakaotalk_to_kakao(self) -> None:
        assert ClinicLookup._platform_to_key("KakaoTalk") == "kakao"

    def test_line_to_line(self) -> None:
        assert ClinicLookup._platform_to_key("Line") == "line"

    def test_unknown_returns_none(self) -> None:
        assert ClinicLookup._platform_to_key("WeChat") is None

    def test_case_sensitive(self) -> None:
        # "kakaotalk" (lowercase) is not in the mapping
        assert ClinicLookup._platform_to_key("kakaotalk") is None


class TestResolvePlatformName:
    """Test _resolve_platform_name static method."""

    def test_kakao_to_kakaotalk(self) -> None:
        assert ClinicLookup._resolve_platform_name("kakao") == "KakaoTalk"

    def test_line_to_line(self) -> None:
        assert ClinicLookup._resolve_platform_name("line") == "Line"

    def test_case_insensitive(self) -> None:
        assert ClinicLookup._resolve_platform_name("KAKAO") == "KakaoTalk"
        assert ClinicLookup._resolve_platform_name("LINE") == "Line"

    def test_unknown_returns_original(self) -> None:
        assert ClinicLookup._resolve_platform_name("wechat") == "wechat"


# ------------------------------------------------------------------
# Doctor loading
# ------------------------------------------------------------------


class TestDoctorLoading:
    """Test that find_by_id returns ClinicInfo with doctors populated."""

    def test_doctor_populated(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        assert len(clinic.doctors) == 1

    def test_doctor_fields(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(1)
        assert clinic is not None
        doc = clinic.doctors[0]
        assert doc.name == "Kim"
        assert doc.name_english == "Kim"
        assert doc.role == "director"
        assert doc.education == ["Seoul Univ"]
        assert doc.career == ["10yr"]
        assert doc.credentials == ["Board"]

    def test_no_doctors(self, lookup: ClinicLookup) -> None:
        clinic = lookup.find_by_id(2)
        assert clinic is not None
        assert clinic.doctors == []

    def test_doctors_from_find_by_name(self, lookup: ClinicLookup) -> None:
        results = lookup.find_by_name("Seoul Skin Clinic")
        assert len(results) == 1
        assert len(results[0].doctors) == 1
        assert results[0].doctors[0].name == "Kim"

    def test_doctors_from_search(self, lookup: ClinicLookup) -> None:
        results = lookup.search("Seoul Skin")
        assert len(results) >= 1
        seoul = next(r for r in results if r.hospital_no == 1)
        assert len(seoul.doctors) == 1
        assert seoul.doctors[0].name == "Kim"
