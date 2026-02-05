"""
Crawler configuration with Pydantic BaseSettings.

Supports environment variable overrides with CRAWL_ prefix.
Example: CRAWL_BROWSER__HEADLESS=true
"""

from __future__ import annotations

import random
from pathlib import Path
from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

MOBILE_USER_AGENTS = [
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.4.1 Mobile/15E148 Safari/604.1"
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/16.6 Mobile/15E148 Safari/604.1"
    ),
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.2 Mobile/15E148 Safari/604.1"
    ),
]


class BrowserConfig(BaseSettings):
    """Playwright browser settings."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_BROWSER__")

    headless: bool = Field(
        default=False,
        description="Must be False to avoid Naver IP bans",
    )
    channel: str = Field(
        default="chrome",
        description="Use installed Chrome for realistic fingerprint",
    )
    viewport_width_min: int = 375
    viewport_width_max: int = 430
    viewport_height_min: int = 667
    viewport_height_max: int = 932
    user_agent: str = Field(
        default_factory=lambda: random.choice(MOBILE_USER_AGENTS),
        description="Randomized mobile Safari user agent",
    )
    session_dir: Path = Path("crawl/output/.browser_session")
    timeout_ms: int = 30000

    @model_validator(mode="after")
    def validate_viewport_ranges(self) -> Self:
        if self.viewport_width_min > self.viewport_width_max:
            raise ValueError("viewport_width_min must be <= viewport_width_max")
        if self.viewport_height_min > self.viewport_height_max:
            raise ValueError("viewport_height_min must be <= viewport_height_max")
        return self


class DelayConfig(BaseSettings):
    """Human-like delay settings (in seconds)."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_DELAYS__")

    page_load_min: float = 2.0
    page_load_max: float = 5.0
    action_min: float = 0.5
    action_max: float = 2.0
    between_places_min: float = 3.0
    between_places_max: float = 8.0
    typing_min_ms: int = 50
    typing_max_ms: int = 200
    rate_limit_seconds: float = 3.0

    @model_validator(mode="after")
    def validate_delay_ranges(self) -> Self:
        for prefix in ("page_load", "action", "between_places"):
            min_val = getattr(self, f"{prefix}_min")
            max_val = getattr(self, f"{prefix}_max")
            if min_val > max_val:
                raise ValueError(f"{prefix}_min must be <= {prefix}_max")
        if self.typing_min_ms > self.typing_max_ms:
            raise ValueError("typing_min_ms must be <= typing_max_ms")
        return self


class StorageConfig(BaseSettings):
    """Storage paths and settings."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_STORAGE__")

    output_dir: Path = Path("crawl/output")
    db_path: Path = Path("crawl/output/naver_places.db")
    screenshot_dir: Path = Path("crawl/output/screenshots")


class RetryConfig(BaseSettings):
    """Retry and error handling settings."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_RETRY__")

    max_retries: int = 3
    base_delay: float = 5.0
    max_delay: float = 60.0
    cooldown_on_ban_min: float = 300.0
    cooldown_on_ban_max: float = 600.0
    max_consecutive_bans: int = 3

    @model_validator(mode="after")
    def validate_cooldown_range(self) -> Self:
        if self.cooldown_on_ban_min > self.cooldown_on_ban_max:
            raise ValueError("cooldown_on_ban_min must be <= cooldown_on_ban_max")
        return self


class PhotoConfig(BaseSettings):
    """Photo download settings."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_PHOTOS__")

    max_concurrent_downloads: int = 3
    download_timeout_seconds: int = 30
    exclude_video: bool = True
    max_photos_per_place: int = 500
    max_scroll_attempts: int = 50


class CrawlerConfig(BaseSettings):
    """Top-level crawler configuration."""

    model_config = SettingsConfigDict(env_prefix="CRAWL_")

    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    delays: DelayConfig = Field(default_factory=DelayConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    photos: PhotoConfig = Field(default_factory=PhotoConfig)
    delay_multiplier: float = Field(
        default=1.0,
        gt=0.0,
        description="Multiply all delays (>1 = slower, safer)",
    )
    max_places: int | None = Field(
        default=None,
        description="Limit number of places to crawl",
    )
