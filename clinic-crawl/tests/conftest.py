"""Shared fixtures for clinic-crawl tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from clinic_crawl.config import ClinicCrawlConfig, StorageConfig
from clinic_crawl.storage import ClinicStorageManager


@pytest.fixture
def tmp_config(tmp_path: Path) -> ClinicCrawlConfig:
    """Config pointing to a temporary database."""
    return ClinicCrawlConfig(
        storage=StorageConfig(db_path=tmp_path / "test.db"),
    )


@pytest.fixture
async def storage(tmp_config: ClinicCrawlConfig) -> ClinicStorageManager:
    """Initialized storage manager backed by a temp database."""
    async with ClinicStorageManager(tmp_config) as mgr:
        yield mgr
