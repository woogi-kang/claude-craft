"""Tests for CLI entry point."""

from __future__ import annotations

import sys

import pytest

from clinic_crawl.__main__ import main


class TestCli:
    def test_no_command_exits(self, monkeypatch):
        """No subcommand prints help and exits."""
        monkeypatch.setattr(sys, "argv", ["clinic-crawl"])
        with pytest.raises(SystemExit, match="1"):
            main()

    def test_help_flag(self, monkeypatch):
        """--help prints usage and exits."""
        monkeypatch.setattr(sys, "argv", ["clinic-crawl", "--help"])
        with pytest.raises(SystemExit, match="0"):
            main()

    def test_verbose_no_command_exits(self, monkeypatch):
        """Verbose flag without subcommand still exits."""
        monkeypatch.setattr(sys, "argv", ["clinic-crawl", "-v"])
        with pytest.raises(SystemExit, match="1"):
            main()
