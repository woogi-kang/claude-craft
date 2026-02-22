"""Tests for the configuration system."""

from __future__ import annotations

from pathlib import Path

from src.config import (
    AccountPoolConfig,
    BrowserConfig,
    ClassificationConfig,
    DaemonConfig,
    DatabaseConfig,
    DelaysConfig,
    DmConfig,
    LLMConfig,
    LoggingConfig,
    ReplyConfig,
    SearchConfig,
    Settings,
    load_settings,
)


class TestSubConfigs:
    """Test individual configuration section defaults."""

    def test_search_defaults(self) -> None:
        cfg = SearchConfig()
        assert cfg.keywords == []
        assert cfg.max_post_age_hours == 24

    def test_classification_defaults(self) -> None:
        cfg = ClassificationConfig()
        assert cfg.confidence_threshold == 0.7
        assert len(cfg.categories) == 5
        assert "hospital" in cfg.categories

    def test_reply_defaults(self) -> None:
        cfg = ReplyConfig()
        assert cfg.enabled is False
        assert cfg.daily_limit == 20
        assert cfg.min_interval_minutes == 15
        assert cfg.max_interval_minutes == 20

    def test_dm_defaults(self) -> None:
        cfg = DmConfig()
        assert cfg.enabled is False
        assert cfg.daily_limit == 15
        assert cfg.min_interval_minutes == 20
        assert cfg.max_interval_minutes == 40

    def test_browser_defaults(self) -> None:
        cfg = BrowserConfig()
        assert cfg.headless is True
        assert cfg.viewport_width == 1280
        assert cfg.viewport_height == 720

    def test_delays_defaults(self) -> None:
        cfg = DelaysConfig()
        assert cfg.search_min_seconds == 30
        assert cfg.search_max_seconds == 300

    def test_daemon_defaults(self) -> None:
        cfg = DaemonConfig()
        assert cfg.min_interval_hours == 2.0
        assert cfg.max_interval_hours == 4.0
        assert cfg.active_start_hour == 8
        assert cfg.active_end_hour == 23

    def test_logging_defaults(self) -> None:
        cfg = LoggingConfig()
        assert cfg.level == "INFO"
        assert cfg.max_bytes == 10_485_760

    def test_database_defaults(self) -> None:
        cfg = DatabaseConfig()
        assert cfg.url == "postgresql://localhost:5432/outreach"
        assert cfg.min_pool_size == 2
        assert cfg.max_pool_size == 10

    def test_account_pool_defaults(self) -> None:
        cfg = AccountPoolConfig()
        assert cfg.cooldown_minutes_crawl == 30
        assert cfg.cooldown_minutes_outreach == 60

    def test_llm_defaults(self) -> None:
        cfg = LLMConfig()
        assert cfg.provider == "codex"
        assert cfg.model == "gpt-5.1-codex-mini"


class TestSettings:
    """Test the root Settings class."""

    def test_default_secrets_are_empty(self) -> None:
        s = Settings()
        assert s.burner_x_username == ""
        assert s.gemini_api_key == ""

    def test_nested_configs_present(self) -> None:
        s = Settings()
        assert isinstance(s.search, SearchConfig)
        assert isinstance(s.classification, ClassificationConfig)
        assert isinstance(s.browser, BrowserConfig)
        assert isinstance(s.database, DatabaseConfig)
        assert isinstance(s.daemon, DaemonConfig)
        assert isinstance(s.llm, LLMConfig)


class TestLoadSettings:
    """Test loading settings from YAML files."""

    def test_load_from_yaml(self, tmp_path: Path) -> None:
        config = tmp_path / "config.yaml"
        config.write_text(
            """\
search:
  keywords:
    - "テスト"
  max_post_age_hours: 12
classification:
  confidence_threshold: 0.8
""",
            encoding="utf-8",
        )
        s = load_settings(config_path=config)
        assert s.search.keywords == ["テスト"]
        assert s.search.max_post_age_hours == 12
        assert s.classification.confidence_threshold == 0.8

    def test_load_nonexistent_yaml(self, tmp_path: Path) -> None:
        """When the YAML file does not exist, defaults should be used."""
        s = load_settings(config_path=tmp_path / "missing.yaml")
        assert s.search.max_post_age_hours == 24

    def test_load_empty_yaml(self, tmp_path: Path) -> None:
        config = tmp_path / "config.yaml"
        config.write_text("", encoding="utf-8")
        s = load_settings(config_path=config)
        assert isinstance(s.search, SearchConfig)
