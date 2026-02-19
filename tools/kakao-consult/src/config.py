"""Configuration system using pydantic-settings.

Loads settings from config.yaml and .env files. All secrets are loaded
exclusively from environment variables; config.yaml contains only
non-sensitive defaults.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------------------------
# Sub-models (nested configuration sections)
# ---------------------------------------------------------------------------


class EmulatorConfig(BaseModel):
    """LDPlayer Android emulator configuration."""

    ldplayer_path: str = "C:/LDPlayer/LDPlayer9"
    instance_name: str = "LDPlayer"
    serial: str = "127.0.0.1:5555"
    kakao_package: str = "com.kakao.talk"


class MonitorConfig(BaseModel):
    """KakaoTalk message monitoring configuration."""

    poll_interval_seconds: int = 5
    max_messages_per_poll: int = 10
    ignored_chatrooms: list[str] = Field(default_factory=list)


class ClassifierConfig(BaseModel):
    """Message classification configuration."""

    model: str = "claude-sonnet-4-20250514"
    confidence_threshold: float = 0.7
    use_local_first: bool = True

    @field_validator("confidence_threshold")
    @classmethod
    def validate_threshold(cls, v: float) -> float:
        if v < 0.0 or v > 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")
        return v


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    default_provider: str = "claude"
    claude_model: str = "claude-sonnet-4-20250514"
    openai_model: str = "gpt-4o"
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    max_tokens: int = 500
    temperature: float = 0.7


class TemplateConfig(BaseModel):
    """Response template configuration."""

    templates_dir: str = "templates"
    fuzzy_threshold: float = 0.75


class ResponseConfig(BaseModel):
    """Response delivery configuration."""

    max_response_length: int = 500
    typing_delay_per_char_ms: int = 80
    min_response_delay_seconds: float = 2.0
    max_response_delay_seconds: float = 8.0
    split_long_messages: bool = True


class RateLimitConfig(BaseModel):
    """Rate limiting configuration."""

    max_responses_per_hour: int = 30
    max_responses_per_day: int = 200
    min_interval_seconds: int = 10
    cooldown_after_errors: int = 60

    @field_validator("max_responses_per_hour")
    @classmethod
    def validate_hourly(cls, v: int) -> int:
        if v < 1 or v > 1000:
            raise ValueError("max_responses_per_hour must be between 1 and 1000")
        return v

    @field_validator("max_responses_per_day")
    @classmethod
    def validate_daily(cls, v: int) -> int:
        if v < 1 or v > 10000:
            raise ValueError("max_responses_per_day must be between 1 and 10000")
        return v


class DelaysConfig(BaseModel):
    """Human-like delay configuration."""

    read_min_seconds: float = 1.0
    read_max_seconds: float = 3.0
    type_min_delay_ms: int = 50
    type_max_delay_ms: int = 200
    between_messages_min: float = 2.0
    between_messages_max: float = 8.0


class SchedulingConfig(BaseModel):
    """Scheduler configuration."""

    active_start_hour: int = 9  # KST
    active_end_hour: int = 22  # KST
    weekend_enabled: bool = False

    @field_validator("active_start_hour", "active_end_hour")
    @classmethod
    def validate_hour(cls, v: int) -> int:
        if v < 0 or v > 23:
            raise ValueError("Hour must be between 0 and 23")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    log_dir: str = "logs"
    max_bytes: int = 10_485_760  # 10 MB
    backup_count: int = 5


class DatabaseConfig(BaseModel):
    """Database configuration."""

    path: str = "data/consult.db"


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
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # --- Non-secret configuration sections ---
    emulator: EmulatorConfig = Field(default_factory=EmulatorConfig)
    monitor: MonitorConfig = Field(default_factory=MonitorConfig)
    classifier: ClassifierConfig = Field(default_factory=ClassifierConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    template: TemplateConfig = Field(default_factory=TemplateConfig)
    response: ResponseConfig = Field(default_factory=ResponseConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
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
