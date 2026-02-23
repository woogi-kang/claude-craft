"""Tests for account health monitoring and escalation."""

from __future__ import annotations

from pathlib import Path

from outreach_shared.account.health import HealthMonitor


class TestHealthMonitor:
    """Test escalation protocol."""

    def test_first_warning_continues(self) -> None:
        monitor = HealthMonitor()
        action = monitor.record_warning("a1", "rate_limit")
        assert action == "continue"

    def test_second_warning_pauses(self) -> None:
        monitor = HealthMonitor()
        monitor.record_warning("a1", "rate_limit")
        action = monitor.record_warning("a1", "captcha")
        assert action == "pause"

    def test_third_warning_bans(self) -> None:
        monitor = HealthMonitor()
        monitor.record_warning("a1", "rate_limit")
        monitor.record_warning("a1", "captcha")
        action = monitor.record_warning("a1", "restricted")
        assert action == "ban"

    def test_different_accounts_independent(self) -> None:
        monitor = HealthMonitor()
        monitor.record_warning("a1", "x")
        monitor.record_warning("a1", "x")
        action = monitor.record_warning("a2", "x")
        assert action == "continue"  # a2 is independent

    def test_warning_count(self) -> None:
        monitor = HealthMonitor()
        monitor.record_warning("a1", "x")
        monitor.record_warning("a1", "y")
        assert monitor.get_warning_count("a1") == 2
        assert monitor.get_warning_count("a2") == 0


class TestHaltFile:
    """Test halt file operations."""

    def test_is_halted_no_file(self, tmp_path: Path) -> None:
        monitor = HealthMonitor(halt_file=tmp_path / ".halt")
        assert monitor.is_halted() is False

    def test_write_and_check_halt(self, tmp_path: Path) -> None:
        halt_file = tmp_path / "data" / ".halt"
        monitor = HealthMonitor(halt_file=halt_file)
        monitor.write_halt("test emergency")
        assert monitor.is_halted() is True
        assert halt_file.exists()

    def test_clear_halt(self, tmp_path: Path) -> None:
        halt_file = tmp_path / ".halt"
        monitor = HealthMonitor(halt_file=halt_file)
        monitor.write_halt("test")
        assert monitor.clear_halt() is True
        assert monitor.is_halted() is False

    def test_clear_halt_no_file(self, tmp_path: Path) -> None:
        monitor = HealthMonitor(halt_file=tmp_path / ".halt")
        assert monitor.clear_halt() is False

    def test_is_halted_no_path_configured(self) -> None:
        monitor = HealthMonitor(halt_file=None)
        assert monitor.is_halted() is False
