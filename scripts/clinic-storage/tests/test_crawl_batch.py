"""Tests for crawl_batch: parse_hospital, filter_hospitals, load_csv."""

import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from crawl_batch import filter_hospitals, load_csv, parse_hospital
from storage_manager import get_db, save_result


# ===========================================================================
# parse_hospital
# ===========================================================================

class TestParseHospitalNewFormat:
    def test_new_format(self):
        row = {
            "naver_place_id": "123",
            "id": "1",
            "name": "Test",
            "website": "https://ex.com",
            "address": "서울시 강남구",
            "phone": "02-1234-5678",
        }
        result = parse_hospital(row)
        assert result["place_id"] == "123"
        assert result["csv_no"] == 1
        assert result["name"] == "Test"
        assert result["url"] == "https://ex.com"


class TestParseHospitalOldFormat:
    def test_old_format(self):
        row = {
            "place_id": "456",
            "csv_no": "2",
            "naver_name": "Test2",
            "homepage_url": "https://ex2.com",
        }
        result = parse_hospital(row)
        assert result["place_id"] == "456"
        assert result["csv_no"] == 2
        assert result["name"] == "Test2"
        assert result["url"] == "https://ex2.com"


class TestParseHospitalMissingUrl:
    def test_missing_url(self):
        row = {
            "naver_place_id": "789",
            "id": "3",
            "name": "No Website",
        }
        result = parse_hospital(row)
        assert result["url"] == ""


# ===========================================================================
# filter_hospitals
# ===========================================================================

@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary SQLite database with schema initialized."""
    db_path = str(tmp_path / "test_filter.db")
    conn = get_db(db_path)
    conn.close()
    return db_path


@pytest.fixture
def sample_hospitals():
    """Create sample hospital list for filtering tests."""
    return [
        {
            "naver_place_id": "100",
            "name": "Seoul Clinic",
            "website": "https://seoul-clinic.com",
            "naver_address": "서울시 강남구 역삼동",
        },
        {
            "naver_place_id": "200",
            "name": "Busan Clinic",
            "website": "https://busan-clinic.com",
            "naver_address": "부산시 해운대구",
        },
        {
            "naver_place_id": "300",
            "name": "Seoul No Website",
            "website": "",
            "naver_address": "서울시 서초구",
        },
        {
            "naver_place_id": "400",
            "name": "Gangnam Clinic",
            "website": "https://gangnam.com",
            "naver_address": "서울시 강남구 삼성동",
        },
    ]


class TestFilterByCity:
    def test_filter_by_city(self, sample_hospitals, temp_db):
        result = filter_hospitals(
            sample_hospitals,
            city="서울",
            homepage_only=False,
            skip_crawled=False,
            db_path=temp_db,
        )
        names = {h["name"] for h in result}
        assert "Seoul Clinic" in names
        assert "Seoul No Website" in names
        assert "Gangnam Clinic" in names
        assert "Busan Clinic" not in names


class TestFilterByPlaceIds:
    def test_filter_by_place_ids(self, sample_hospitals, temp_db):
        result = filter_hospitals(
            sample_hospitals,
            place_ids=["100", "400"],
            homepage_only=False,
            skip_crawled=False,
            db_path=temp_db,
        )
        pids = {h["naver_place_id"] for h in result}
        assert pids == {"100", "400"}


class TestFilterHomepageOnly:
    def test_homepage_only(self, sample_hospitals, temp_db):
        result = filter_hospitals(
            sample_hospitals,
            homepage_only=True,
            skip_crawled=False,
            db_path=temp_db,
        )
        # "Seoul No Website" has empty website, should be removed
        names = {h["name"] for h in result}
        assert "Seoul No Website" not in names
        assert len(result) == 3


class TestFilterSkipCrawled:
    def test_skip_crawled(self, sample_hospitals, temp_db):
        # Save one hospital as already crawled with success
        save_result(temp_db, {
            "place_id": "100",
            "name": "Seoul Clinic",
            "url": "https://seoul-clinic.com",
            "status": "success",
            "social_channels": [],
            "doctors": [],
            "errors": [],
        })
        result = filter_hospitals(
            sample_hospitals,
            homepage_only=False,
            skip_crawled=True,
            db_path=temp_db,
        )
        pids = {h["naver_place_id"] for h in result}
        assert "100" not in pids  # already crawled
        assert "200" in pids


# ===========================================================================
# load_csv
# ===========================================================================

class TestLoadCsv:
    def test_reads_csv(self, tmp_path):
        csv_path = tmp_path / "test.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["naver_place_id", "name", "website"])
            writer.writeheader()
            writer.writerow({"naver_place_id": "111", "name": "Clinic A", "website": "https://a.com"})
            writer.writerow({"naver_place_id": "222", "name": "Clinic B", "website": "https://b.com"})

        result = load_csv(str(csv_path))
        assert len(result) == 2
        assert result[0]["naver_place_id"] == "111"
        assert result[1]["name"] == "Clinic B"

    def test_handles_bom(self, tmp_path):
        csv_path = tmp_path / "bom_test.csv"
        # Write CSV with BOM prefix
        with open(csv_path, "wb") as f:
            f.write(b"\xef\xbb\xbf")  # UTF-8 BOM
            f.write("naver_place_id,name,website\n".encode("utf-8"))
            f.write("333,BOM Clinic,https://bom.com\n".encode("utf-8"))

        result = load_csv(str(csv_path))
        assert len(result) == 1
        # The key should not have BOM prefix thanks to utf-8-sig encoding
        assert "naver_place_id" in result[0]
        assert result[0]["naver_place_id"] == "333"
