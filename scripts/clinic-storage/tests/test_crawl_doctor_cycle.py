"""Tests for crawl_doctor_cycle.assess_quality function."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from crawl_doctor_cycle import assess_quality
from storage_manager import get_db, save_result


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary SQLite database with schema initialized."""
    db_path = str(tmp_path / "test_cycle.db")
    conn = get_db(db_path)
    conn.close()
    return db_path


def _save(db_path, place_id, status="success", doctors=None, social_channels=None, errors=None):
    """Helper to save a hospital result."""
    data = {
        "place_id": place_id,
        "name": "Test Hospital",
        "url": "https://example.com",
        "status": status,
        "social_channels": social_channels or [],
        "doctors": doctors or [],
        "errors": errors or [],
    }
    save_result(db_path, data)


class TestAssessQualityGood:
    def test_good_hospital(self, temp_db):
        """Hospital with status=success, 2 doctors with 2+ credentials -> good."""
        _save(temp_db, "good1", status="success", doctors=[
            {"name": "김상우", "role": "대표원장", "profile_raw": ["서울대 졸업", "피부과 전문의"]},
            {"name": "이지연", "role": "부원장", "profile_raw": ["고려대 졸업"]},
        ])
        result = assess_quality(temp_db, ["good1"])
        assert "good1" in result["good"]
        assert "good1" not in result["suspicious"]
        assert "good1" not in result["failed"]


class TestAssessQualitySuspiciousNoDoctors:
    def test_suspicious_no_doctors(self, temp_db):
        """Hospital with status=success, 0 doctors -> suspicious."""
        _save(temp_db, "susp1", status="success", doctors=[])
        result = assess_quality(temp_db, ["susp1"])
        assert "susp1" in result["suspicious"]
        assert "susp1" not in result["good"]
        assert "susp1" not in result["failed"]


class TestAssessQualitySuspiciousNoCredentials:
    def test_suspicious_no_credentials(self, temp_db):
        """Hospital with status=success, 1 doctor with empty profile_raw -> suspicious."""
        _save(temp_db, "susp2", status="success", doctors=[
            {"name": "김상우", "role": "원장", "profile_raw": []},
        ])
        result = assess_quality(temp_db, ["susp2"])
        assert "susp2" in result["suspicious"]
        assert "susp2" not in result["good"]


class TestAssessQualityFailed:
    def test_failed_hospital(self, temp_db):
        """Hospital with status=robots_blocked -> failed."""
        _save(temp_db, "fail1", status="robots_blocked")
        result = assess_quality(temp_db, ["fail1"])
        assert "fail1" in result["failed"]
        assert "fail1" not in result["good"]
        assert "fail1" not in result["suspicious"]


class TestAssessQualityNotInDb:
    def test_hospital_not_in_db(self, temp_db):
        """place_id not in DB -> failed."""
        result = assess_quality(temp_db, ["nonexistent999"])
        assert "nonexistent999" in result["failed"]
        assert "nonexistent999" not in result["good"]
        assert "nonexistent999" not in result["suspicious"]
