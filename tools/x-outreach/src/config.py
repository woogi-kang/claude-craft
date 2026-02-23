"""Configuration system using pydantic-settings.

Loads settings from config.yaml and .env files. All secrets are loaded
exclusively from environment variables; config.yaml contains only
non-sensitive defaults.
"""

from __future__ import annotations

import re
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
    block_media_resources: bool = False
    blocked_resource_types: list[str] = Field(
        default_factory=lambda: ["image", "media", "font"]
    )
    log_network_usage: bool = False


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

    require_profile_pic: bool = True
    require_bio: bool = True


class ReplyConfig(BaseModel):
    """Reply pipeline configuration."""

    enabled: bool = False
    daily_limit: int = 20
    min_interval_minutes: int = 15
    max_interval_minutes: int = 20


class DmConfig(BaseModel):
    """DM pipeline configuration."""

    enabled: bool = False
    daily_limit: int = 15
    min_interval_minutes: int = 20
    max_interval_minutes: int = 40


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
    fallback_provider: str = "gemini_cli"
    fallback_model: str = "gemini-3-flash-preview"


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
    gemini_api_key: str = ""  # Kept for .env backward compat (GEMINI_API_KEY)
    database_url: str = ""
    x_dm_encryption_passcode: str = ""  # 4-digit PIN for X DM encryption

    # Per-persona account credentials
    master_a_username: str = ""
    master_a_password: str = ""
    master_b_username: str = ""
    master_b_password: str = ""
    master_c_username: str = ""
    master_c_password: str = ""
    master_d_username: str = ""
    master_d_password: str = ""
    master_e_username: str = ""
    master_e_password: str = ""

    # Oxylabs Residential proxy (per-persona account mapping)
    oxylabs_proxy_server: str = "pr.oxylabs.io:7777"
    oxylabs_proxy_country: str = "JP"
    oxylabs_proxy_city: str = "tokyo"
    oxylabs_master_a_proxy_username: str = ""
    oxylabs_master_a_proxy_password: str = ""
    oxylabs_master_a_proxy_country: str = ""
    oxylabs_master_a_proxy_city: str = ""
    oxylabs_master_b_proxy_username: str = ""
    oxylabs_master_b_proxy_password: str = ""
    oxylabs_master_b_proxy_country: str = ""
    oxylabs_master_b_proxy_city: str = ""
    oxylabs_master_c_proxy_username: str = ""
    oxylabs_master_c_proxy_password: str = ""
    oxylabs_master_c_proxy_country: str = ""
    oxylabs_master_c_proxy_city: str = ""
    oxylabs_master_d_proxy_username: str = ""
    oxylabs_master_d_proxy_password: str = ""
    oxylabs_master_d_proxy_country: str = ""
    oxylabs_master_d_proxy_city: str = ""
    oxylabs_master_e_proxy_username: str = ""
    oxylabs_master_e_proxy_password: str = ""
    oxylabs_master_e_proxy_country: str = ""
    oxylabs_master_e_proxy_city: str = ""

    @property
    def llm_api_key(self) -> str:
        """Return the active LLM API key based on provider config."""
        return self.gemini_api_key

    @property
    def dm_passcode_digits(self) -> list[str] | None:
        """Return the passcode as individual digit strings, or None if unset."""
        code = self.x_dm_encryption_passcode.strip()
        if not code:
            return None
        if len(code) != 4 or not code.isdigit():
            raise ValueError(f"X_DM_ENCRYPTION_PASSCODE must be exactly 4 digits, got: '{code}'")
        return list(code)

    def get_account_credentials(self, account_id: str) -> tuple[str, str]:
        """Return (username, password) for the given account_id.

        Maps account_id (e.g. ``"master_a"``) to the corresponding
        ``MASTER_A_USERNAME`` / ``MASTER_A_PASSWORD`` environment variables.

        Returns empty strings if the account_id is not recognized.
        """
        cred_map: dict[str, tuple[str, str]] = {
            "master_a": (self.master_a_username, self.master_a_password),
            "master_b": (self.master_b_username, self.master_b_password),
            "master_c": (self.master_c_username, self.master_c_password),
            "master_d": (self.master_d_username, self.master_d_password),
            "master_e": (self.master_e_username, self.master_e_password),
        }
        return cred_map.get(account_id, ("", ""))

    def get_account_proxy(self, account_id: str) -> dict[str, str] | None:
        """Return Playwright proxy settings for a specific account.

        Supports per-account Oxylabs credentials for:
        - ``master_a`` .. ``master_e``
        """
        proxy_map: dict[str, tuple[str, str, str, str]] = {
            "master_a": (
                self.oxylabs_master_a_proxy_username,
                self.oxylabs_master_a_proxy_password,
                self.oxylabs_master_a_proxy_country,
                self.oxylabs_master_a_proxy_city,
            ),
            "master_b": (
                self.oxylabs_master_b_proxy_username,
                self.oxylabs_master_b_proxy_password,
                self.oxylabs_master_b_proxy_country,
                self.oxylabs_master_b_proxy_city,
            ),
            "master_c": (
                self.oxylabs_master_c_proxy_username,
                self.oxylabs_master_c_proxy_password,
                self.oxylabs_master_c_proxy_country,
                self.oxylabs_master_c_proxy_city,
            ),
            "master_d": (
                self.oxylabs_master_d_proxy_username,
                self.oxylabs_master_d_proxy_password,
                self.oxylabs_master_d_proxy_country,
                self.oxylabs_master_d_proxy_city,
            ),
            "master_e": (
                self.oxylabs_master_e_proxy_username,
                self.oxylabs_master_e_proxy_password,
                self.oxylabs_master_e_proxy_country,
                self.oxylabs_master_e_proxy_city,
            ),
        }
        creds = proxy_map.get(account_id)
        if creds is None:
            return None

        base_username, raw_password, account_country, account_city = creds
        base_username = base_username.strip()
        password = raw_password.strip()
        if not base_username or not password:
            return None

        country = account_country.strip() or self.oxylabs_proxy_country
        city = account_city.strip() or self.oxylabs_proxy_city
        username = self._apply_oxylabs_geo_targeting(
            base_username,
            country=country,
            city=city,
        )
        server = self._normalize_proxy_server(self.oxylabs_proxy_server)
        return {
            "server": server,
            "username": username,
            "password": password,
        }

    @staticmethod
    def _normalize_proxy_server(server: str) -> str:
        """Normalize proxy server to a Playwright-compatible URI."""
        cleaned = server.strip() or "pr.oxylabs.io:7777"
        if "://" in cleaned:
            return cleaned
        return f"http://{cleaned}"

    @staticmethod
    def _apply_oxylabs_geo_targeting(
        username: str,
        *,
        country: str,
        city: str,
    ) -> str:
        """Apply/replace ``cc`` and ``city`` targeting in Oxylabs username."""
        targeted = re.sub(r"-cc-[A-Za-z]{2}", "", username)
        targeted = re.sub(r"-city-[A-Za-z0-9_]+", "", targeted)

        cc = country.strip().upper()
        if cc:
            targeted = f"{targeted}-cc-{cc}"

        city_slug = city.strip().lower().replace(" ", "-")
        if city_slug:
            targeted = f"{targeted}-city-{city_slug}"

        return targeted

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
