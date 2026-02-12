"""Shared test fixtures for clinic crawler tests."""

import sys
from pathlib import Path

import pytest

# Ensure scripts/clinic-storage is on sys.path so we can import the flat modules
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_db(tmp_path):
    """Create a temporary SQLite database with schema initialized."""
    db_path = str(tmp_path / "test.db")
    from storage_manager import get_db

    conn = get_db(db_path)
    conn.close()
    return db_path


@pytest.fixture
def sample_crawl_result():
    """Factory for sample crawl result dicts."""

    def _make(hospital_no=1, name="Test Hospital", status="success", **overrides):
        base = {
            "hospital_no": hospital_no,
            "name": name,
            "url": "https://example.com",
            "final_url": "",
            "status": status,
            "cms_platform": "",
            "schema_version": "2.0.0",
            "social_channels": [],
            "doctors": [],
            "errors": [],
            "doctor_page_exists": None,
        }
        base.update(overrides)
        return base

    return _make


@pytest.fixture
def sample_doctor():
    """Factory for sample doctor dicts."""

    def _make(name="김상우", role="대표원장", **overrides):
        base = {
            "name": name,
            "name_english": "",
            "role": role,
            "photo_url": "",
            "education": [],
            "career": [],
            "credentials": [],
            "branch": "",
            "branches": [],
            "extraction_source": "dom",
            "ocr_source": False,
        }
        base.update(overrides)
        return base

    return _make


@pytest.fixture
def sample_channel():
    """Factory for sample social channel dicts."""

    def _make(platform="KakaoTalk", url="https://pf.kakao.com/_test", **overrides):
        base = {
            "platform": platform,
            "url": url,
            "extraction_method": "dom_static",
            "confidence": 1.0,
            "status": "active",
        }
        base.update(overrides)
        return base

    return _make
