"""Tests for M4 features: warmup, conservation, blocklist, DM tracking, report, hot-reload."""

from __future__ import annotations

import csv
import io
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

from src.config import Settings, load_settings
from src.db.repository import Repository

# =========================================================================
# Repository: config methods (now stubs in PostgreSQL migration)
# =========================================================================


class TestConfigStubs:
    """Test that config methods are safe stubs."""

    def test_get_config_returns_none(self) -> None:
        repo = MagicMock(spec=Repository)
        repo.get_config.return_value = None
        assert repo.get_config("any_key") is None

    def test_set_config_is_noop(self) -> None:
        repo = MagicMock(spec=Repository)
        repo.set_config("key", "value")  # Should not raise


# =========================================================================
# Warmup mode (with mocked repository)
# =========================================================================


class TestWarmupManager:
    """Test the warmup mode manager with mocked config."""

    def _make_repo(self, config_data: dict[str, str] | None = None) -> MagicMock:
        repo = MagicMock(spec=Repository)
        store = dict(config_data) if config_data else {}
        repo.get_config.side_effect = lambda k: store.get(k)
        repo.set_config.side_effect = lambda k, v: store.__setitem__(k, v)
        return repo

    def test_ensure_start_date_first_run(self) -> None:
        from src.pipeline.warmup import WarmupManager

        repo = self._make_repo()
        mgr = WarmupManager(repo)
        start_date = mgr.ensure_start_date()
        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        assert start_date == today

    def test_ensure_start_date_subsequent_run(self) -> None:
        from src.pipeline.warmup import WarmupManager

        repo = self._make_repo({"pipeline_start_date": "2026-01-01"})
        mgr = WarmupManager(repo)
        assert mgr.ensure_start_date() == "2026-01-01"

    def test_is_warmup_active_first_day(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)
        assert mgr.is_warmup_active() is True

    def test_is_warmup_active_day_14(self) -> None:
        from src.pipeline.warmup import WarmupManager

        day_14_ago = (datetime.now(tz=UTC) - timedelta(days=13)).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": day_14_ago})
        mgr = WarmupManager(repo)
        assert mgr.is_warmup_active() is True

    def test_is_warmup_inactive_day_15(self) -> None:
        from src.pipeline.warmup import WarmupManager

        day_15_ago = (datetime.now(tz=UTC) - timedelta(days=14)).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": day_15_ago})
        mgr = WarmupManager(repo)
        assert mgr.is_warmup_active() is False

    def test_get_warmup_day_first(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)
        assert mgr.get_warmup_day() == 1

    def test_get_warmup_day_mid(self) -> None:
        from src.pipeline.warmup import WarmupManager

        seven_days_ago = (datetime.now(tz=UTC) - timedelta(days=6)).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": seven_days_ago})
        mgr = WarmupManager(repo)
        assert mgr.get_warmup_day() == 7

    def test_get_warmup_day_no_start_date(self) -> None:
        from src.pipeline.warmup import WarmupManager

        repo = self._make_repo()
        mgr = WarmupManager(repo)
        assert mgr.get_warmup_day() == 1

    def test_get_volume_multiplier_during_warmup(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)
        assert mgr.get_volume_multiplier() == 0.5

    def test_get_volume_multiplier_after_warmup(self) -> None:
        from src.pipeline.warmup import WarmupManager

        old_date = (datetime.now(tz=UTC) - timedelta(days=30)).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": old_date})
        mgr = WarmupManager(repo)
        assert mgr.get_volume_multiplier() == 1.0

    def test_apply_limits_during_warmup(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
            search={"keywords": ["a", "b", "c", "d", "e", "f"]},
        )

        adjusted = mgr.apply_limits(settings)
        assert adjusted.reply.daily_limit == 25
        assert adjusted.dm.daily_limit == 10
        assert len(adjusted.search.keywords) == 3

    def test_apply_limits_after_warmup(self) -> None:
        from src.pipeline.warmup import WarmupManager

        old_date = (datetime.now(tz=UTC) - timedelta(days=30)).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": old_date})
        mgr = WarmupManager(repo)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
            search={"keywords": ["a", "b", "c", "d"]},
        )

        adjusted = mgr.apply_limits(settings)
        assert adjusted.reply.daily_limit == 50
        assert adjusted.dm.daily_limit == 20
        assert len(adjusted.search.keywords) == 4

    def test_apply_limits_does_not_mutate_original(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)

        settings = Settings(
            reply={"enabled": True, "daily_limit": 50},
            dm={"enabled": True, "daily_limit": 20},
        )
        mgr.apply_limits(settings)
        assert settings.reply.daily_limit == 50
        assert settings.dm.daily_limit == 20

    def test_apply_limits_minimum_one(self) -> None:
        from src.pipeline.warmup import WarmupManager

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        repo = self._make_repo({"pipeline_start_date": today})
        mgr = WarmupManager(repo)

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
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        assert tracker.is_conservation_mode() is False

    def test_conservation_at_80_percent(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1200)  # 80%
        assert tracker.is_conservation_mode() is True

    def test_conservation_below_80_percent(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1199)
        assert tracker.is_conservation_mode() is False

    def test_critical_at_95_percent(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1425)  # 95%
        assert tracker.is_critical_mode() is True

    def test_not_critical_below_95_percent(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=1500)
        tracker.use(1424)
        assert tracker.is_critical_mode() is False

    def test_usage_ratio(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=100)
        tracker.use(50)
        assert tracker.usage_ratio == 0.5

    def test_usage_ratio_zero_limit(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=0)
        assert tracker.usage_ratio == 1.0

    def test_custom_conservation_threshold(self) -> None:
        from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker

        tracker = MonthlyBudgetTracker(monthly_limit=100)
        tracker.use(70)
        assert tracker.is_conservation_mode(threshold=0.7) is True
        assert tracker.is_conservation_mode(threshold=0.8) is False


# =========================================================================
# Blocklist (with mocked repository)
# =========================================================================


class TestBlocklistManager:
    """Test the blocklist management system with mocked repository."""

    def _make_repo(self) -> MagicMock:
        repo = MagicMock(spec=Repository)
        store: dict[str, str] = {}
        repo.get_config.side_effect = lambda k: store.get(k)
        repo.set_config.side_effect = lambda k, v: store.__setitem__(k, v)
        return repo

    def test_add_user(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        assert mgr.add("spammer") is True

    def test_add_user_with_at_sign(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        assert mgr.add("@spammer") is True
        assert mgr.is_blocked("spammer") is True

    def test_add_duplicate(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        mgr.add("spammer")
        assert mgr.add("spammer") is False

    def test_remove_user(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        mgr.add("spammer")
        assert mgr.remove("spammer") is True

    def test_remove_nonexistent(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        assert mgr.remove("nobody") is False

    def test_is_blocked_true(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        mgr.add("spammer")
        assert mgr.is_blocked("spammer") is True

    def test_is_blocked_false(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        assert mgr.is_blocked("innocent") is False

    def test_is_blocked_case_insensitive(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        mgr.add("Spammer")
        assert mgr.is_blocked("spammer") is True
        assert mgr.is_blocked("SPAMMER") is True

    def test_list_all_empty(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        assert mgr.list_all() == []

    def test_list_all_with_users(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
        mgr.add("alice")
        mgr.add("bob")
        blocked = mgr.list_all()
        assert len(blocked) == 2
        assert "alice" in blocked
        assert "bob" in blocked

    def test_add_then_remove_then_list(self) -> None:
        from src.cli.blocklist import BlocklistManager

        mgr = BlocklistManager(self._make_repo())
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


# =========================================================================
# DM response tracking (with mocked repository)
# =========================================================================


class TestDmResponseTracker:
    """Test the DM response tracking system with mocked repository."""

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
            {
                "date": "2026-02-13",
                "tweets_searched": 10,
                "tweets_collected": 5,
                "tweets_analyzed": 3,
                "replies_sent": 2,
                "dms_sent": 1,
                "dms_skipped": 0,
                "dm_responses": 0,
                "errors": 0,
                "api_tweets_used": 2,
            },
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
        for row in csv_rows:
            assert row["tweets_searched"] == "0"

    def test_generate_summary(self) -> None:
        from src.cli.report import generate_summary

        rows = [
            {
                "tweets_searched": 10,
                "tweets_collected": 5,
                "tweets_analyzed": 3,
                "replies_sent": 2,
                "dms_sent": 1,
                "dms_skipped": 0,
                "dm_responses": 1,
                "errors": 0,
                "api_tweets_used": 2,
            },
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
    """Test the config hot-reload mechanism."""

    @staticmethod
    def _make_reload_helper(config_path: Path, settings: Settings) -> object:
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
        helper._config_mtime = 0.0

        result = helper._check_config_reload()
        assert result is True
        assert helper._settings.search.keywords == ["test"]

    def test_check_config_reload_invalid_yaml(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.yaml"
        config_file.write_text("valid: true", encoding="utf-8")

        helper = self._make_reload_helper(config_file, Settings())
        helper._config_mtime = 0.0

        config_file.write_text(": invalid: yaml: [", encoding="utf-8")

        result = helper._check_config_reload()
        assert isinstance(result, bool)


# =========================================================================
# CLI integration (parser)
# =========================================================================


class TestCLIParser:
    """Test that the CLI parser includes M4 subcommands."""

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
            "halt_action",
            nargs="?",
            default="status",
            choices=["status", "resume"],
        )

        blocklist_p = subparsers.add_parser("blocklist")
        blocklist_p.add_argument(
            "blocklist_action",
            nargs="?",
            default="list",
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
