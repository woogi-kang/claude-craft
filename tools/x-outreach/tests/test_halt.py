"""Tests for emergency halt and daemon halt wiring."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.pipeline.halt import HaltManager, get_volume_multiplier, mark_resumed


class TestHaltManager:
    """Test HaltManager state management."""

    def test_not_halted_initially(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        assert mgr.is_halted() is False
        assert mgr.get_halt_info() is None

    def test_trigger_halt_creates_file(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        mgr.trigger_halt("test reason", source="test_source")
        assert mgr.is_halted() is True
        info = mgr.get_halt_info()
        assert info is not None
        assert info["reason"] == "test reason"
        assert info["source"] == "test_source"

    def test_resume_clears_halt(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        mgr.trigger_halt("test")
        assert mgr.is_halted() is True
        assert mgr.resume() is True
        assert mgr.is_halted() is False

    def test_resume_when_not_halted(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        assert mgr.resume() is False

    def test_is_restriction_error_403(self) -> None:
        assert HaltManager.is_restriction_error(403, "account suspended") is True
        assert HaltManager.is_restriction_error(403, "temporarily limited") is True
        assert HaltManager.is_restriction_error(403, "") is True  # empty body suspicious

    def test_is_restriction_error_429(self) -> None:
        assert HaltManager.is_restriction_error(429, "too many requests") is True
        assert HaltManager.is_restriction_error(429, "rate limit exceeded") is True

    def test_is_restriction_error_normal(self) -> None:
        assert HaltManager.is_restriction_error(200, "ok") is False
        assert HaltManager.is_restriction_error(404, "not found") is False

    def test_is_blocked_page(self) -> None:
        assert HaltManager.is_blocked_page("Something went wrong. Try again.") is True
        assert HaltManager.is_blocked_page("Your account has been locked") is True
        assert HaltManager.is_blocked_page("Normal timeline content") is False


class TestVolumeMultiplier:
    """Test conservation mode volume multiplier."""

    def test_normal_returns_1(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        assert get_volume_multiplier(mgr) == 1.0

    def test_after_resume_returns_half(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        mgr.trigger_halt("test")
        mgr.resume()
        mark_resumed(mgr)
        assert get_volume_multiplier(mgr) == 0.5

    def test_second_cycle_returns_full(self, tmp_path: Path) -> None:
        mgr = HaltManager(halt_path=tmp_path / ".halt")
        mgr.trigger_halt("test")
        mgr.resume()
        mark_resumed(mgr)
        get_volume_multiplier(mgr)  # consumes marker
        assert get_volume_multiplier(mgr) == 1.0


class TestCheckEmergencyHalt:
    """Test _check_emergency_halt from daemon module."""

    @dataclass
    class _FakeReplyResult:
        emergency_halt: bool = False

    @dataclass
    class _FakeDmResult:
        emergency_halt: bool = False

    @dataclass
    class _FakeNurtureResult:
        emergency_halt: bool = False

    @dataclass
    class _FakePostingResult:
        emergency_halt: bool = False

    @dataclass
    class _FakePipelineResult:
        reply: object = None
        dm: object = None
        nurture: object = None
        posting: object = None

    def test_no_halt_when_all_ok(self, tmp_path: Path) -> None:
        from src.daemon import _check_emergency_halt

        mgr = HaltManager(halt_path=tmp_path / ".halt")
        result = self._FakePipelineResult(
            reply=self._FakeReplyResult(emergency_halt=False),
        )
        _check_emergency_halt(result, mgr)
        assert mgr.is_halted() is False

    def test_halt_on_reply_emergency(self, tmp_path: Path) -> None:
        from src.daemon import _check_emergency_halt

        mgr = HaltManager(halt_path=tmp_path / ".halt")
        result = self._FakePipelineResult(
            reply=self._FakeReplyResult(emergency_halt=True),
        )
        _check_emergency_halt(result, mgr)
        assert mgr.is_halted() is True
        info = mgr.get_halt_info()
        assert "Reply" in info["reason"]

    def test_halt_on_dm_emergency(self, tmp_path: Path) -> None:
        from src.daemon import _check_emergency_halt

        mgr = HaltManager(halt_path=tmp_path / ".halt")
        result = self._FakePipelineResult(
            dm=self._FakeDmResult(emergency_halt=True),
        )
        _check_emergency_halt(result, mgr)
        assert mgr.is_halted() is True

    def test_halt_on_multiple_emergencies(self, tmp_path: Path) -> None:
        from src.daemon import _check_emergency_halt

        mgr = HaltManager(halt_path=tmp_path / ".halt")
        result = self._FakePipelineResult(
            reply=self._FakeReplyResult(emergency_halt=True),
            nurture=self._FakeNurtureResult(emergency_halt=True),
        )
        _check_emergency_halt(result, mgr)
        assert mgr.is_halted() is True
        info = mgr.get_halt_info()
        assert "Reply" in info["reason"]
        assert "Nurture" in info["reason"]

    def test_no_halt_with_none_results(self, tmp_path: Path) -> None:
        from src.daemon import _check_emergency_halt

        mgr = HaltManager(halt_path=tmp_path / ".halt")
        result = self._FakePipelineResult()  # all None
        _check_emergency_halt(result, mgr)
        assert mgr.is_halted() is False
