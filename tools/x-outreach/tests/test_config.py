"""Tests for the configuration system."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.config import (
    AnalyzeConfig,
    BrowserConfig,
    CollectConfig,
    DatabaseConfig,
    DelaysConfig,
    DmConfig,
    LoggingConfig,
    ReplyConfig,
    SchedulingConfig,
    SearchConfig,
    Settings,
    load_settings,
)


class TestSubConfigs:
    """Test individual configuration section defaults."""

    def test_search_defaults(self) -> None:
        cfg = SearchConfig()
        assert cfg.keywords == []
        assert cfg.max_tweet_age_hours == 24

    def test_collect_defaults(self) -> None:
        cfg = CollectConfig()
        assert cfg.max_follower_count == 10_000
        assert cfg.require_profile_pic is True
        assert cfg.require_bio is True

    def test_analyze_defaults(self) -> None:
        cfg = AnalyzeConfig()
        assert cfg.confidence_threshold == 0.7
        assert cfg.model == "claude-sonnet-4-20250514"

    def test_reply_defaults(self) -> None:
        cfg = ReplyConfig()
        assert cfg.enabled is False
        assert cfg.daily_limit == 50

    def test_dm_defaults(self) -> None:
        cfg = DmConfig()
        assert cfg.enabled is False
        assert cfg.daily_limit == 20
        assert cfg.min_interval_minutes == 25

    def test_browser_defaults(self) -> None:
        cfg = BrowserConfig()
        assert cfg.headless is True
        assert cfg.viewport_width == 1280
        assert cfg.viewport_height == 720

    def test_delays_defaults(self) -> None:
        cfg = DelaysConfig()
        assert cfg.search_min_seconds == 30
        assert cfg.search_max_seconds == 300

    def test_scheduling_defaults(self) -> None:
        cfg = SchedulingConfig()
        assert cfg.interval_hours == 2
        assert cfg.active_start_hour == 8
        assert cfg.active_end_hour == 23

    def test_logging_defaults(self) -> None:
        cfg = LoggingConfig()
        assert cfg.level == "INFO"
        assert cfg.max_bytes == 10_485_760

    def test_database_defaults(self) -> None:
        cfg = DatabaseConfig()
        assert cfg.path == "data/outreach.db"


class TestSettings:
    """Test the root Settings class."""

    def test_default_secrets_are_empty(self) -> None:
        s = Settings()
        assert s.burner_x_username == ""
        assert s.anthropic_api_key == ""

    def test_nested_configs_present(self) -> None:
        s = Settings()
        assert isinstance(s.search, SearchConfig)
        assert isinstance(s.collect, CollectConfig)
        assert isinstance(s.analyze, AnalyzeConfig)
        assert isinstance(s.browser, BrowserConfig)
        assert isinstance(s.database, DatabaseConfig)


class TestLoadSettings:
    """Test loading settings from YAML files."""

    def test_load_from_yaml(self, tmp_path: Path) -> None:
        config = tmp_path / "config.yaml"
        config.write_text(
            """\
search:
  keywords:
    - "テスト"
  max_tweet_age_hours: 12
collect:
  max_follower_count: 5000
""",
            encoding="utf-8",
        )
        s = load_settings(config_path=config)
        assert s.search.keywords == ["テスト"]
        assert s.search.max_tweet_age_hours == 12
        assert s.collect.max_follower_count == 5000

    def test_load_nonexistent_yaml(self, tmp_path: Path) -> None:
        """When the YAML file does not exist, defaults should be used."""
        s = load_settings(config_path=tmp_path / "missing.yaml")
        assert s.search.max_tweet_age_hours == 24

    def test_load_empty_yaml(self, tmp_path: Path) -> None:
        config = tmp_path / "config.yaml"
        config.write_text("", encoding="utf-8")
        s = load_settings(config_path=config)
        assert isinstance(s.search, SearchConfig)
