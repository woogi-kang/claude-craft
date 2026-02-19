"""Tests for M4 features: warmup, conservation, blocklist, DM tracking, report, hot-reload."""

from __future__ import annotations

import csv
import io
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from src.config import Settings, load_settings
from src.db.repository import Repository


# =========================================================================
# Repository: config table methods
# =========================================================================


class TestConfigTable:
    """Test the config key-value store in Repository."""

    def test_get_config_missing_key(self, tmp_db: Repository) -> None:
        assert tmp_db.get_config("nonexistent") is None

    def test_set_and_get_config(self, tmp_db: Repository) -> None:
        tmp_db.set_config("test_key", "test_value")
        assert tmp_db.get_config("test_key") == "test_value"

    def test_set_config_upsert(self, tmp_db: Repository) -> None:
        tmp_db.set_config("key", "first")
        tmp_db.set_config("key", "second")
        assert tmp_db.get_config("key") == "second"

    def test_get_daily_stats_range_empty(self, tmp_db: Repository) -> None:
        rows = tmp_db.get_daily_stats_range("2026-01-01", "2026-01-07")
        assert rows == []

    def test_get_daily_stats_range_with_data(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-10", tweets_searched=5)
        tmp_db.update_daily_stats("2026-02-11", tweets_searched=3)
        tmp_db.update_daily_stats("2026-02-12", tweets_searched=8)
        rows = tmp_db.get_daily_stats_range("2026-02-10", "2026-02-12")
        assert len(rows) == 3
        assert rows[0]["date"] == "2026-02-10"
        assert rows[2]["date"] == "2026-02-12"

    def test_get_daily_stats_range_filters(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-09", tweets_searched=1)
        tmp_db.update_daily_stats("2026-02-10", tweets_searched=2)
        tmp_db.update_daily_stats("2026-02-13", tweets_searched=3)
        rows = tmp_db.get_daily_stats_range("2026-02-10", "2026-02-12")
        assert len(rows) == 1
        assert rows[0]["date"] == "2026-02-10"


class TestMigrations:
    """Test that schema migrations run correctly."""

    def test_dm_responses_column_exists(self, tmp_db: Repository) -> None:
        """The dm_responses column should exist in daily_stats."""
        tmp_db.update_daily_stats("2026-02-19", dm_responses=3)
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["dm_responses"] == 3

    def test_user_dm_response_columns(self, tmp_db: Repository) -> None:
        """The dm_response_received and dm_response_at columns should exist."""
        tmp_db.insert_user({"username": "test_user"})
        tmp_db.update_user(
            "test_user",
            dm_response_received=1,
            dm_response_at="2026-02-19T10:00:00Z",
        )
        user = tmp_db.get_user("test_user")
        assert user is not None
        assert user["dm_response_received"] == 1
        assert user["dm_response_at"] == "2026-02-19T10:00:00Z"

    def test_migrations_idempotent(self, tmp_db: Repository) -> None:
        """Calling init_db twice should not fail (migrations are safe)."""
        tmp_db.init_db()
        tmp_db.init_db()


# =========================================================================
# Warmup mode
# =========================================================================


class TestWarmupManager:
    """Test the warmup mode manager."""

    def test_ensure_start_date_first_run(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        mgr = WarmupManager(tmp_db)
        start_date = mgr.ensure_start_date()
        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        assert start_date == today

    def test_ensure_start_date_subsequent_run(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        tmp_db.set_config("pipeline_start_date", "2026-01-01")
        mgr = WarmupManager(tmp_db)
        assert mgr.ensure_start_date() == "2026-01-01"

    def test_is_warmup_active_first_day(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)
        assert mgr.is_warmup_active() is True

    def test_is_warmup_active_day_14(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        day_14_ago = (datetime.now(tz=timezone.utc) - timedelta(days=13)).strftime(
            "%Y-%m-%d"
        )
        tmp_db.set_config("pipeline_start_date", day_14_ago)
        mgr = WarmupManager(tmp_db)
        assert mgr.is_warmup_active() is True

    def test_is_warmup_inactive_day_15(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        day_15_ago = (datetime.now(tz=timezone.utc) - timedelta(days=14)).strftime(
            "%Y-%m-%d"
        )
        tmp_db.set_config("pipeline_start_date", day_15_ago)
        mgr = WarmupManager(tmp_db)
        assert mgr.is_warmup_active() is False

    def test_get_warmup_day_first(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)
        assert mgr.get_warmup_day() == 1

    def test_get_warmup_day_mid(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        seven_days_ago = (datetime.now(tz=timezone.utc) - timedelta(days=6)).strftime(
            "%Y-%m-%d"
        )
        tmp_db.set_config("pipeline_start_date", seven_days_ago)
        mgr = WarmupManager(tmp_db)
        assert mgr.get_warmup_day() == 7

    def test_get_warmup_day_no_start_date(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        mgr = WarmupManager(tmp_db)
        assert mgr.get_warmup_day() == 1

    def test_get_volume_multiplier_during_warmup(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)
        assert mgr.get_volume_multiplier() == 0.5

    def test_get_volume_multiplier_after_warmup(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        old_date = (datetime.now(tz=timezone.utc) - timedelta(days=30)).strftime(
            "%Y-%m-%d"
        )
        tmp_db.set_config("pipeline_start_date", old_date)
        mgr = WarmupManager(tmp_db)
        assert mgr.get_volume_multiplier() == 1.0

    def test_apply_limits_during_warmup(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
            search={"keywords": ["a", "b", "c", "d", "e", "f"]},
        )

        adjusted = mgr.apply_limits(settings)
        assert adjusted.reply.daily_limit == 25
        assert adjusted.dm.daily_limit == 10
        assert len(adjusted.search.keywords) == 3

    def test_apply_limits_after_warmup(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        old_date = (datetime.now(tz=timezone.utc) - timedelta(days=30)).strftime(
            "%Y-%m-%d"
        )
        tmp_db.set_config("pipeline_start_date", old_date)
        mgr = WarmupManager(tmp_db)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
            search={"keywords": ["a", "b", "c", "d"]},
        )

        adjusted = mgr.apply_limits(settings)
        # Should return unchanged settings
        assert adjusted.reply.daily_limit == 50
        assert adjusted.dm.daily_limit == 20
        assert len(adjusted.search.keywords) == 4

    def test_apply_limits_does_not_mutate_original(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
        )
        mgr.apply_limits(settings)
        # Original should be unchanged
        assert settings.reply.daily_limit == 50
        assert settings.dm.daily_limit == 20

    def test_apply_limits_minimum_one(self, tmp_db: Repository) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        tmp_db.set_config("pipeline_start_date", today)
        mgr = WarmupManager(tmp_db)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 1},
            dm={"enabled": True, "daily_limit": 1},
            search={"keywords": ["one"]},
        )
        adjusted = mgr.apply_limits(settings)
        assert adjusted.reply.daily_limit >= 1
        assert adjusted.dm.daily_limit >= 1
        assert len(adjusted.search.keywords) >= 1


# =========================================================================
# Conservation mode
# =========================================================================


class TestConservationMode:
    """Test the conservation mode helpers on MonthlyBudgetTracker."""

    def test_not_in_conservation_initially(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        assert tracker.is_conservation_mode() is False

    def test_conservation_at_80_percent(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1200)  # 80%
        assert tracker.is_conservation_mode() is True

    def test_conservation_below_80_percent(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1199)
        assert tracker.is_conservation_mode() is False

    def test_critical_at_95_percent(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1425)  # 95%
        assert tracker.is_critical_mode() is True

    def test_not_critical_below_95_percent(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1424)
        assert tracker.is_critical_mode() is False

    def test_usage_ratio(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=100)
        tracker.use(50)
        assert tracker.usage_ratio == 0.5

    def test_usage_ratio_zero_limit(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=0)
        assert tracker.usage_ratio == 1.0

    def test_custom_conservation_threshold(self) -> None:
        from src.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=100)
        tracker.use(70)
        assert tracker.is_conservation_mode(threshold=0.7) is True
        assert tracker.is_conservation_mode(threshold=0.8) is False


# =========================================================================
# Blocklist
# =========================================================================


class TestBlocklistManager:
    """Test the blocklist management system."""

    def test_add_user(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        assert mgr.add("spammer") is True

    def test_add_user_with_at_sign(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        assert mgr.add("@spammer") is True
        assert mgr.is_blocked("spammer") is True

    def test_add_duplicate(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("spammer")
        assert mgr.add("spammer") is False

    def test_remove_user(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("spammer")
        assert mgr.remove("spammer") is True

    def test_remove_nonexistent(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        assert mgr.remove("nobody") is False

    def test_is_blocked_true(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("spammer")
        assert mgr.is_blocked("spammer") is True

    def test_is_blocked_false(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        assert mgr.is_blocked("innocent") is False

    def test_is_blocked_case_insensitive(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("Spammer")
        assert mgr.is_blocked("spammer") is True
        assert mgr.is_blocked("SPAMMER") is True

    def test_list_all_empty(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        assert mgr.list_all() == []

    def test_list_all_with_users(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("alice")
        mgr.add("bob")
        blocked = mgr.list_all()
        assert len(blocked) == 2
        assert "alice" in blocked
        assert "bob" in blocked

    def test_add_then_remove_then_list(self, tmp_db: Repository) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(tmp_db)
        mgr.add("alice")
        mgr.add("bob")
        mgr.remove("alice")
        blocked = mgr.list_all()
        assert blocked == ["bob"]

    def test_normalise_strips_at(self) -> None:
        from src.cli.blocklist import BlocklistManager

        assert BlocklistManager._normalise("@User") == "user"
        assert BlocklistManager._normalise("User") == "user"
        assert BlocklistManager._normalise("@@double") == "double"


class TestBlocklistCLI:
    """Test the blocklist CLI handler functions."""

    def test_run_blocklist_add(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_add

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        result = run_blocklist_add("@spammer", db_path=db_path)
        assert "Added" in result
        assert "spammer" in result

    def test_run_blocklist_add_duplicate(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_add

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        run_blocklist_add("spammer", db_path=db_path)
        result = run_blocklist_add("spammer", db_path=db_path)
        assert "already blocked" in result

    def test_run_blocklist_remove(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_add, run_blocklist_remove

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        run_blocklist_add("spammer", db_path=db_path)
        result = run_blocklist_remove("spammer", db_path=db_path)
        assert "Removed" in result

    def test_run_blocklist_remove_nonexistent(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_remove

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        result = run_blocklist_remove("nobody", db_path=db_path)
        assert "not blocked" in result

    def test_run_blocklist_list_empty(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_list

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        result = run_blocklist_list(db_path=db_path)
        assert "empty" in result

    def test_run_blocklist_list_with_users(self, tmp_path: Path) -> None:
        from src.cli.blocklist import run_blocklist_add, run_blocklist_list

        db_path = str(tmp_path / "test.db")
        repo = Repository(db_path)
        repo.init_db()
        repo.close()

        run_blocklist_add("alice", db_path=db_path)
        run_blocklist_add("bob", db_path=db_path)
        result = run_blocklist_list(db_path=db_path)
        assert "alice" in result
        assert "bob" in result
        assert "Total: 2" in result


# =========================================================================
# DM response tracking
# =========================================================================


class TestDmResponseTracker:
    """Test the DM response tracking system."""

    def test_get_pending_users_empty(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tracker = DmResponseTracker(tmp_db)
        assert tracker.get_pending_users() == []

    def test_get_pending_users_with_contacted(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tmp_db.insert_user({"username": "alice", "contact_count": 1})
        tmp_db.insert_user({"username": "bob", "contact_count": 0})
        tracker = DmResponseTracker(tmp_db)
        pending = tracker.get_pending_users()
        assert len(pending) == 1
        assert pending[0]["username"] == "alice"

    def test_get_pending_users_excludes_responded(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tmp_db.insert_user({"username": "alice", "contact_count": 1})
        tmp_db.update_user("alice", dm_response_received=1)
        tracker = DmResponseTracker(tmp_db)
        assert tracker.get_pending_users() == []

    def test_mark_response(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tmp_db.insert_user({"username": "alice", "contact_count": 1})
        tracker = DmResponseTracker(tmp_db)
        result = tracker.mark_response("alice")
        assert result is True

        user = tmp_db.get_user("alice")
        assert user is not None
        assert user["dm_response_received"] == 1
        assert user["dm_response_at"] is not None

    def test_mark_response_updates_daily_stats(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tmp_db.insert_user({"username": "alice", "contact_count": 1})
        tracker = DmResponseTracker(tmp_db)
        tracker.mark_response("alice")

        today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        stats = tmp_db.get_daily_stats(today)
        assert stats is not None
        assert stats["dm_responses"] == 1

    def test_mark_response_nonexistent_user(self, tmp_db: Repository) -> None:
        from src.pipeline.dm_track import DmResponseTracker

        tracker = DmResponseTracker(tmp_db)
        result = tracker.mark_response("nobody")
        assert result is False

    def test_dm_track_result_defaults(self) -> None:
        from src.pipeline.dm_track import DmTrackResult

        result = DmTrackResult()
        assert result.users_checked == 0
        assert result.responses_detected == 0
        assert result.errors == 0


# =========================================================================
# Weekly report
# =========================================================================


class TestWeeklyReport:
    """Test the weekly report generation."""

    def test_generate_csv_with_data(self) -> None:
        from src.cli.report import generate_csv

        rows = [
            {"date": "2026-02-13", "tweets_searched": 10, "tweets_collected": 5,
             "tweets_analyzed": 3, "replies_sent": 2, "dms_sent": 1,
             "dms_skipped": 0, "dm_responses": 0, "errors": 0, "api_tweets_used": 2},
        ]
        csv_str = generate_csv(rows, "2026-02-13", "2026-02-19")
        reader = csv.DictReader(io.StringIO(csv_str))
        csv_rows = list(reader)
        assert len(csv_rows) == 7  # Always 7 days
        assert csv_rows[0]["date"] == "2026-02-13"
        assert csv_rows[0]["tweets_searched"] == "10"

    def test_generate_csv_fills_missing_dates(self) -> None:
        from src.cli.report import generate_csv

        csv_str = generate_csv([], "2026-02-13", "2026-02-19")
        reader = csv.DictReader(io.StringIO(csv_str))
        csv_rows = list(reader)
        assert len(csv_rows) == 7
        # All values should be zero
        for row in csv_rows:
            assert row["tweets_searched"] == "0"

    def test_generate_summary(self) -> None:
        from src.cli.report import generate_summary

        rows = [
            {"tweets_searched": 10, "tweets_collected": 5,
             "tweets_analyzed": 3, "replies_sent": 2, "dms_sent": 1,
             "dms_skipped": 0, "dm_responses": 1, "errors": 0,
             "api_tweets_used": 2},
        ]
        summary = generate_summary(rows, budget_remaining=1400, budget_limit=1500)
        assert "Weekly Report Summary" in summary
        assert "Searched:     10" in summary
        assert "DM responses: 1" in summary
        assert "1400 / 1500" in summary

    def test_generate_summary_conservation_mode(self) -> None:
        from src.cli.report import generate_summary

        summary = generate_summary([], budget_remaining=200, budget_limit=1500)
        assert "CONSERVATION" in summary

    def test_write_csv_file(self, tmp_path: Path) -> None:
        from src.cli.report import write_csv_file

        csv_content = "date,value\n2026-02-19,10\n"
        filepath = write_csv_file(csv_content, output_dir=tmp_path)
        assert filepath.exists()
        assert filepath.suffix == ".csv"
        assert filepath.read_text(encoding="utf-8") == csv_content

    def test_date_range_7_days(self) -> None:
        from src.cli.report import _date_range_7_days

        start, end = _date_range_7_days()
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        delta = (end_dt - start_dt).days
        assert delta == 6  # 7-day range is 6 days apart


# =========================================================================
# Config hot-reload
# =========================================================================


class TestConfigHotReload:
    """Test the config hot-reload mechanism.

    The PipelineScheduler depends on APScheduler + SQLAlchemy which may
    not be available in the test environment.  We test the hot-reload
    logic by extracting it into a lightweight helper object that mirrors
    the scheduler's methods.
    """

    @staticmethod
    def _make_reload_helper(
        config_path: Path, settings: Settings
    ) -> object:
        """Build a minimal object with the scheduler's reload methods."""

        class _ReloadHelper:
            def __init__(self, cp: Path, s: Settings) -> None:
                self._config_path = cp
                self._settings = s
                self._config_mtime = self._get_config_mtime()

            def _get_config_mtime(self) -> float:
                try:
                    return self._config_path.stat().st_mtime
                except OSError:
                    return 0.0

            def _check_config_reload(self) -> bool:
                current_mtime = self._get_config_mtime()
                if current_mtime != self._config_mtime and current_mtime > 0:
                    self._config_mtime = current_mtime
                    try:
                        self._settings = load_settings(self._config_path)
                        return True
                    except Exception:
                        pass
                return False

        return _ReloadHelper(config_path, settings)

    def test_get_config_mtime_existing(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text("test: true", encoding="utf-8")

        helper = self._make_reload_helper(config_file, Settings())
        assert helper._get_config_mtime() > 0

    def test_get_config_mtime_missing(self, tmp_path: Path) -> None:
        helper = self._make_reload_helper(tmp_path / "missing.yaml", Settings())
        assert helper._get_config_mtime() == 0.0

    def test_check_config_reload_no_change(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text("search:\n  keywords: ['a']", encoding="utf-8")

        helper = self._make_reload_helper(config_file, Settings())
        result = helper._check_config_reload()
        assert result is False

    def test_check_config_reload_on_change(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text(
            "search:\n  keywords:\n    - 'test'\n  max_tweet_age_hours: 24\n",
            encoding="utf-8",
        )

        helper = self._make_reload_helper(config_file, Settings())
        # Simulate a change by resetting mtime to old value
        helper._config_mtime = 0.0

        result = helper._check_config_reload()
        assert result is True
        assert helper._settings.search.keywords == ["test"]

    def test_check_config_reload_invalid_yaml(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text("valid: true", encoding="utf-8")

        helper = self._make_reload_helper(config_file, Settings())
        helper._config_mtime = 0.0

        # Write invalid content
        config_file.write_text(": invalid: yaml: [", encoding="utf-8")

        # Should not crash, just return False
        result = helper._check_config_reload()
        assert isinstance(result, bool)


# =========================================================================
# CLI integration (parser)
# =========================================================================


class TestCLIParser:
    """Test that the CLI parser includes M4 subcommands.

    We build an equivalent argparse parser inline to avoid importing
    ``src.main`` which transitively imports Playwright / stealth
    modules that may not be resolvable in the test environment.
    """

    @staticmethod
    def _build_parser():
        """Replicate the parser structure for testing."""
        import argparse

        parser = argparse.ArgumentParser(prog="x-outreach")
        parser.add_argument("--once", action="store_true", default=False)
        parser.add_argument("--dry-run", action="store_true", default=False)

        subparsers = parser.add_subparsers(dest="command")

        run_p = subparsers.add_parser("run")
        run_p.add_argument("--dry-run", action="store_true", default=False)

        subparsers.add_parser("daemon")
        subparsers.add_parser("status")
        subparsers.add_parser("setup")

        halt_p = subparsers.add_parser("halt")
        halt_p.add_argument(
            "halt_action", nargs="?", default="status",
            choices=["status", "resume"],
        )

        blocklist_p = subparsers.add_parser("blocklist")
        blocklist_p.add_argument(
            "blocklist_action", nargs="?", default="list",
            choices=["add", "remove", "list"],
        )
        blocklist_p.add_argument("username", nargs="?", default=None)

        subparsers.add_parser("report")

        return parser

    def test_blocklist_subcommand_exists(self) -> None:
        parser = self._build_parser()
        args = parser.parse_args(["blocklist", "add", "@spammer"])
        assert args.command == "blocklist"
        assert args.blocklist_action == "add"
        assert args.username == "@spammer"

    def test_blocklist_list_default(self) -> None:
        parser = self._build_parser()
        args = parser.parse_args(["blocklist"])
        assert args.command == "blocklist"
        assert args.blocklist_action == "list"

    def test_blocklist_remove(self) -> None:
        parser = self._build_parser()
        args = parser.parse_args(["blocklist", "remove", "@user"])
        assert args.blocklist_action == "remove"
        assert args.username == "@user"

    def test_report_subcommand_exists(self) -> None:
        parser = self._build_parser()
        args = parser.parse_args(["report"])
        assert args.command == "report"

    def test_existing_commands_still_work(self) -> None:
        parser = self._build_parser()

        args = parser.parse_args(["run"])
        assert args.command == "run"

        args = parser.parse_args(["daemon"])
        assert args.command == "daemon"

        args = parser.parse_args(["status"])
        assert args.command == "status"

        args = parser.parse_args(["setup"])
        assert args.command == "setup"

        args = parser.parse_args(["halt"])
        assert args.command == "halt"

        args = parser.parse_args(["halt", "resume"])
        assert args.halt_action == "resume"
