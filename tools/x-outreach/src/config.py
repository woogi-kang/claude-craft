"""Configuration system using pydantic-settings.

Loads settings from config.yaml and .env files. All secrets are loaded
exclusively from environment variables; config.yaml contains only
non-sensitive defaults.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# Sub-models (nested configuration sections)
# ---------------------------------------------------------------------------


class SearchConfig(BaseModel):
    """Search pipeline configuration."""

    keywords: list[str] = Field(default_factory=list)
    max_tweet_age_hours: int = 24


class CollectConfig(BaseModel):
    """Collect pipeline configuration."""

    max_follower_count: int = 10_000
    require_profile_pic: bool = True
    require_bio: bool = True


class AnalyzeConfig(BaseModel):
    """Analyze pipeline configuration."""

    confidence_threshold: float = 0.7
    model: str = "claude-sonnet-4-20250514"


class ReplyConfig(BaseModel):
    """Reply pipeline configuration (M2 stub)."""

    enabled: bool = False
    daily_limit: int = 50


class DmConfig(BaseModel):
    """DM pipeline configuration (M2 stub)."""

    enabled: bool = False
    daily_limit: int = 20
    min_interval_minutes: int = 25


class BrowserConfig(BaseModel):
    """Browser / Playwright configuration."""

    headless: bool = True
    viewport_width: int = 1280
    viewport_height: int = 720


class DelaysConfig(BaseModel):
    """Human-like delay configuration."""

    search_min_seconds: int = 30
    search_max_seconds: int = 300
    action_min_seconds: int = 5
    action_max_seconds: int = 30


class SchedulingConfig(BaseModel):
    """Scheduler configuration."""

    interval_hours: int = 2
    active_start_hour: int = 8  # JST
    active_end_hour: int = 23  # JST


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 10_485_760  # 10 MB
    backup_count: int = 5


class DatabaseConfig(BaseModel):
    """Database configuration."""

    path: str = "data/outreach.db"


# ---------------------------------------------------------------------------
# Root settings
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_yaml_config(path: Path) -> dict[str, Any]:
    """Load configuration from a YAML file.

    Returns an empty dict if the file does not exist.
    """
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


class Settings(BaseSettings):
    """Root application settings.

    Values are resolved in the following priority order (highest wins):
    1. Environment variables
    2. .env file
    3. config.yaml
    4. Field defaults
    """

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Secrets (loaded from .env only) ---
    burner_x_username: str = ""
    burner_x_password: str = ""
    x_api_key: str = ""
    x_api_secret: str = ""
    x_access_token: str = ""
    x_access_token_secret: str = ""
    nandemo_x_username: str = ""
    nandemo_x_password: str = ""
    anthropic_api_key: str = ""

    # --- Non-secret configuration sections ---
    search: SearchConfig = Field(default_factory=SearchConfig)
    collect: CollectConfig = Field(default_factory=CollectConfig)
    analyze: AnalyzeConfig = Field(default_factory=AnalyzeConfig)
    reply: ReplyConfig = Field(default_factory=ReplyConfig)
    dm: DmConfig = Field(default_factory=DmConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    delays: DelaysConfig = Field(default_factory=DelaysConfig)
    scheduling: SchedulingConfig = Field(default_factory=SchedulingConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)


def load_settings(config_path: Path | None = None) -> Settings:
    """Build a ``Settings`` instance by merging YAML config with env vars.

    Parameters
    ----------
    config_path:
        Path to ``config.yaml``. Defaults to ``<project_root>/config.yaml``.
    """
    if config_path is None:
        config_path = PROJECT_ROOT / "config.yaml"

    yaml_data = _load_yaml_config(config_path)
    return Settings(**yaml_data)
