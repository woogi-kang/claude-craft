"""Tests for the configuration system."""

from __future__ import annotations

from pathlib import Path

import pytest

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
        assert cfg.block_media_resources is False
        assert cfg.blocked_resource_types == ["image", "media", "font"]
        assert cfg.log_network_usage is False

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
        assert cfg.fallback_provider == "gemini_cli"
        assert cfg.fallback_model == "gemini-3-flash-preview"


class TestSettings:
    """Test the root Settings class."""

    def test_default_secrets_are_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("DATABASE_URL", raising=False)
        monkeypatch.delenv("X_DM_ENCRYPTION_PASSCODE", raising=False)
        monkeypatch.delenv("OXYLABS_PROXY_SERVER", raising=False)
        monkeypatch.delenv("OXYLABS_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_PROXY_CITY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_A_PROXY_USERNAME", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_A_PROXY_PASSWORD", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_A_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_A_PROXY_CITY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_B_PROXY_USERNAME", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_B_PROXY_PASSWORD", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_B_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_B_PROXY_CITY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_C_PROXY_USERNAME", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_C_PROXY_PASSWORD", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_C_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_C_PROXY_CITY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_D_PROXY_USERNAME", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_D_PROXY_PASSWORD", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_D_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_D_PROXY_CITY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_E_PROXY_USERNAME", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_E_PROXY_PASSWORD", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_E_PROXY_COUNTRY", raising=False)
        monkeypatch.delenv("OXYLABS_MASTER_E_PROXY_CITY", raising=False)
        for suffix in ["A", "B", "C", "D", "E"]:
            monkeypatch.delenv(f"MASTER_{suffix}_USERNAME", raising=False)
            monkeypatch.delenv(f"MASTER_{suffix}_PASSWORD", raising=False)
        s = Settings(_env_file=None)
        assert s.gemini_api_key == ""
        assert s.master_a_username == ""
        assert s.oxylabs_master_a_proxy_username == ""
        assert s.oxylabs_master_a_proxy_password == ""
        assert s.oxylabs_master_b_proxy_username == ""
        assert s.oxylabs_master_b_proxy_password == ""

    def test_nested_configs_present(self) -> None:
        s = Settings()
        assert isinstance(s.search, SearchConfig)
        assert isinstance(s.classification, ClassificationConfig)
        assert isinstance(s.browser, BrowserConfig)
        assert isinstance(s.database, DatabaseConfig)
        assert isinstance(s.daemon, DaemonConfig)
        assert isinstance(s.llm, LLMConfig)

    def test_get_account_proxy_master_a_applies_jp_tokyo(self) -> None:
        s = Settings(
            _env_file=None,
            oxylabs_proxy_server="pr.oxylabs.io:7777",
            oxylabs_master_a_proxy_username="customer-master_a_NcA0m-cc-US",
            oxylabs_master_a_proxy_password="secret",
            oxylabs_proxy_country="JP",
            oxylabs_proxy_city="tokyo",
        )

        proxy = s.get_account_proxy("master_a")
        assert proxy is not None
        assert proxy["server"] == "http://pr.oxylabs.io:7777"
        assert proxy["username"] == "customer-master_a_NcA0m-cc-JP-city-tokyo"
        assert proxy["password"] == "secret"

    def test_get_account_proxy_per_account_mapping(self) -> None:
        s = Settings(
            _env_file=None,
            oxylabs_master_b_proxy_username="customer-master_b_x",
            oxylabs_master_b_proxy_password="pw-b",
        )
        proxy_b = s.get_account_proxy("master_b")
        assert proxy_b is not None
        assert proxy_b["username"] == "customer-master_b_x-cc-JP-city-tokyo"
        assert proxy_b["password"] == "pw-b"

    def test_get_account_proxy_account_geo_override(self) -> None:
        s = Settings(
            _env_file=None,
            oxylabs_proxy_country="JP",
            oxylabs_proxy_city="tokyo",
            oxylabs_master_d_proxy_username="customer-master_b_x",
            oxylabs_master_d_proxy_password="pw-d",
            oxylabs_master_d_proxy_city="osaka",
        )
        proxy_d = s.get_account_proxy("master_d")
        assert proxy_d is not None
        assert proxy_d["username"] == "customer-master_b_x-cc-JP-city-osaka"

    def test_get_account_proxy_non_master_or_missing_secret(self) -> None:
        s = Settings(_env_file=None)
        assert s.get_account_proxy("master_a") is None
        assert s.get_account_proxy("master_b") is None


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
  block_media_resources: true
  blocked_resource_types: ["image", "media"]
  log_network_usage: true
classification:
  confidence_threshold: 0.8
""",
            encoding="utf-8",
        )
        s = load_settings(config_path=config)
        assert s.search.keywords == ["テスト"]
        assert s.search.max_post_age_hours == 12
        assert s.search.block_media_resources is True
        assert s.search.blocked_resource_types == ["image", "media"]
        assert s.search.log_network_usage is True
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
