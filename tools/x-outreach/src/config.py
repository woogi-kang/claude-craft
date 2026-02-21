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
    max_post_age_hours: int = 24


class ClassificationConfig(BaseModel):
    """Classification pipeline configuration (5-category)."""

    confidence_threshold: float = 0.7
    categories: list[str] = Field(
        default_factory=lambda: [
            "hospital",
            "price",
            "procedure",
            "complaint",
            "review",
        ]
    )


class CollectConfig(BaseModel):
    """Collect pipeline configuration."""

    max_follower_count: int = 10_000
    require_profile_pic: bool = True
    require_bio: bool = True


class ReplyConfig(BaseModel):
    """Reply pipeline configuration."""

    enabled: bool = False
    daily_limit: int = 50


class DmConfig(BaseModel):
    """DM pipeline configuration."""

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


class DaemonConfig(BaseModel):
    """Daemon loop configuration."""

    min_interval_hours: float = 2.0
    max_interval_hours: float = 4.0
    active_start_hour: int = 8  # JST
    active_end_hour: int = 23  # JST


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 10_485_760  # 10 MB
    backup_count: int = 5


class DatabaseConfig(BaseModel):
    """PostgreSQL database configuration."""

    url: str = "postgresql://localhost:5432/outreach"
    min_pool_size: int = 2
    max_pool_size: int = 10


class AccountPoolConfig(BaseModel):
    """Account pool configuration."""

    cooldown_minutes_crawl: int = 30
    cooldown_minutes_outreach: int = 60


class NurtureConfig(BaseModel):
    """Nurture (follow/like) pipeline configuration."""

    enabled: bool = False
    follow_daily_limit: int = 10
    like_daily_limit: int = 15
    follow_probability: float = 0.4
    like_probability: float = 0.6


class PostingConfig(BaseModel):
    """Original tweet posting configuration."""

    enabled: bool = False
    daily_limit: int = 2
    min_interval_hours: float = 4.0
    active_start_hour: int = 10  # JST, narrower than pipeline
    active_end_hour: int = 21  # JST


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    provider: str = "codex"
    model: str = "gpt-5.1-codex-mini"


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
    nandemo_x_username: str = ""
    nandemo_x_password: str = ""
    gemini_api_key: str = ""  # Kept for .env backward compat (GEMINI_API_KEY)
    database_url: str = ""

    @property
    def llm_api_key(self) -> str:
        """Alias for ``gemini_api_key``, used by non-Codex providers."""
        return self.gemini_api_key

    # --- Non-secret configuration sections ---
    search: SearchConfig = Field(default_factory=SearchConfig)
    classification: ClassificationConfig = Field(default_factory=ClassificationConfig)
    collect: CollectConfig = Field(default_factory=CollectConfig)
    reply: ReplyConfig = Field(default_factory=ReplyConfig)
    dm: DmConfig = Field(default_factory=DmConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    delays: DelaysConfig = Field(default_factory=DelaysConfig)
    daemon: DaemonConfig = Field(default_factory=DaemonConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    account_pool: AccountPoolConfig = Field(default_factory=AccountPoolConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    nurture: NurtureConfig = Field(default_factory=NurtureConfig)
    posting: PostingConfig = Field(default_factory=PostingConfig)


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
