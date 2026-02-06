"""Configuration for clinic crawl pipeline using pydantic-settings."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class PrescanConfig(BaseSettings):
    """HTTP prescan settings."""

    timeout_seconds: float = 10.0
    max_concurrent: int = 50
    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    max_retries: int = 2


class TriageConfig(BaseSettings):
    """URL triage settings."""

    chain_threshold: int = 3  # minimum branches to classify as chain
    known_platforms: list[str] = Field(
        default_factory=lambda: ["imweb", "mobidoc", "modoo", "wixsite", "google_sites"]
    )


class StorageConfig(BaseSettings):
    """Storage settings."""

    db_path: Path = Path(__file__).resolve().parent.parent / "data" / "crawl.db"
    batch_size: int = 100


class ClinicCrawlConfig(BaseSettings):
    """Root configuration for the clinic crawl pipeline."""

    csv_path: Path = Path(__file__).resolve().parent.parent.parent / "samples" / "skin_clinics.csv"
    prescan: PrescanConfig = Field(default_factory=PrescanConfig)
    triage: TriageConfig = Field(default_factory=TriageConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
