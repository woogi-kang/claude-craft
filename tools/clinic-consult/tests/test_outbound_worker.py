"""Tests for outbound reservation worker and clinic contactor."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.clinic.models import ClinicInfo
from src.outbound.contact import ClinicContactor
from src.outbound.worker import ReservationWorker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_worker(**overrides) -> ReservationWorker:
    """Create a ReservationWorker with all-mock dependencies."""
    defaults = {
        "repo": MagicMock(),
        "conversation": MagicMock(),
        "contactor": MagicMock(),
        "clinic_lookup": MagicMock(),
    }
    defaults.update(overrides)
    return ReservationWorker(**defaults)


def _make_clinic(
    hospital_no: int = 1,
    name: str = "Test Clinic",
    contact_urls: dict[str, str] | None = None,
) -> ClinicInfo:
    """Create a ClinicInfo with optional contact URLs."""
    return ClinicInfo(
        hospital_no=hospital_no,
        name=name,
        contact_urls=contact_urls or {},
    )


# ---------------------------------------------------------------------------
# ReservationWorker construction
# ---------------------------------------------------------------------------

class TestWorkerConstruction:
    """Verify constructor default values and parameter injection."""

    def test_defaults(self) -> None:
        worker = _make_worker()
        assert worker._platform == "kakao"
        assert worker._poll_interval == 30.0
        assert worker._greeting_timeout_hours == 2
        assert worker._max_followups == 2
        assert worker._running is False

    def test_custom_platform(self) -> None:
        worker = _make_worker(platform="line")
        assert worker._platform == "line"

    def test_custom_poll_interval(self) -> None:
        worker = _make_worker(poll_interval=5.0)
        assert worker._poll_interval == 5.0

    def test_custom_greeting_timeout(self) -> None:
        worker = _make_worker(greeting_timeout_hours=4)
        assert worker._greeting_timeout_hours == 4

    def test_custom_max_followups(self) -> None:
        worker = _make_worker(max_followups=5)
        assert worker._max_followups == 5

    def test_none_contactor_accepted(self) -> None:
        worker = _make_worker(contactor=None)
        assert worker._contactor is None


# ---------------------------------------------------------------------------
# Worker stop signal
# ---------------------------------------------------------------------------

class TestWorkerStopSignal:
    """Test that stop() signals the worker loop to exit."""

    def test_stop_sets_running_false(self) -> None:
        worker = _make_worker()
        worker._running = True
        worker.stop()
        assert worker._running is False

    def test_stop_idempotent(self) -> None:
        worker = _make_worker()
        worker.stop()
        worker.stop()
        assert worker._running is False


# ---------------------------------------------------------------------------
# _hours_since static method
# ---------------------------------------------------------------------------

class TestHoursSince:
    """Test the static helper that computes elapsed hours from ISO timestamp."""

    def test_valid_iso_timestamp(self) -> None:
        # Use a timestamp 2 hours ago
        two_hours_ago = datetime.now(timezone.utc).replace(microsecond=0)
        from datetime import timedelta

        two_hours_ago -= timedelta(hours=2)
        result = ReservationWorker._hours_since(two_hours_ago.isoformat())
        assert 1.9 <= result <= 2.1

    def test_none_returns_zero(self) -> None:
        result = ReservationWorker._hours_since(None)  # type: ignore[arg-type]
        assert result == 0.0

    def test_invalid_string_returns_zero(self) -> None:
        result = ReservationWorker._hours_since("not-a-date")
        assert result == 0.0

    def test_empty_string_returns_zero(self) -> None:
        result = ReservationWorker._hours_since("")
        assert result == 0.0

    def test_timezone_aware_timestamp(self) -> None:
        from datetime import timedelta

        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        result = ReservationWorker._hours_since(one_hour_ago.isoformat())
        assert 0.9 <= result <= 1.1

    def test_naive_timestamp_treated_as_utc(self) -> None:
        from datetime import timedelta

        one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
        naive_str = one_hour_ago.replace(tzinfo=None).isoformat()
        result = ReservationWorker._hours_since(naive_str)
        assert 0.9 <= result <= 1.1

    def test_future_timestamp_returns_negative(self) -> None:
        from datetime import timedelta

        future = datetime.now(timezone.utc) + timedelta(hours=3)
        result = ReservationWorker._hours_since(future.isoformat())
        assert result < 0


# ---------------------------------------------------------------------------
# _handle_created - no contact URL
# ---------------------------------------------------------------------------

class TestHandleCreatedNoUrl:
    """Test _handle_created when no contact URL can be resolved."""

    async def test_no_url_no_clinic_id_marks_failed(self) -> None:
        repo = MagicMock()
        clinic_lookup = MagicMock()
        worker = _make_worker(repo=repo, clinic_lookup=clinic_lookup)

        reservation = {
            "id": 1,
            "status": "created",
            "contact_platform": None,
            "clinic_contact_url": None,
            "clinic_id": None,
        }

        await worker._handle_created(reservation)

        repo.update_reservation.assert_called_once_with(
            1,
            status="failed",
            error_message="No kakao channel URL available",
        )

    async def test_no_url_clinic_id_but_lookup_returns_none(self) -> None:
        repo = MagicMock()
        clinic_lookup = MagicMock()
        clinic_lookup.find_by_id.return_value = None
        worker = _make_worker(repo=repo, clinic_lookup=clinic_lookup)

        reservation = {
            "id": 2,
            "status": "created",
            "contact_platform": None,
            "clinic_contact_url": None,
            "clinic_id": 99,
        }

        await worker._handle_created(reservation)

        clinic_lookup.find_by_id.assert_called_once_with(99)
        repo.update_reservation.assert_called_once_with(
            2,
            status="failed",
            error_message="No kakao channel URL available",
        )

    async def test_no_url_clinic_found_but_no_platform_url(self) -> None:
        repo = MagicMock()
        clinic_lookup = MagicMock()
        clinic = _make_clinic(contact_urls={"line": "https://line.me/R/ti/p/@test"})
        clinic_lookup.find_by_id.return_value = clinic
        worker = _make_worker(repo=repo, clinic_lookup=clinic_lookup)

        reservation = {
            "id": 3,
            "status": "created",
            "contact_platform": None,
            "clinic_contact_url": None,
            "clinic_id": 1,
        }

        await worker._handle_created(reservation)

        repo.update_reservation.assert_called_once_with(
            3,
            status="failed",
            error_message="No kakao channel URL available",
        )


# ---------------------------------------------------------------------------
# _handle_created - with contact URL
# ---------------------------------------------------------------------------

class TestHandleCreatedWithUrl:
    """Test _handle_created transitions to contacting when URL exists."""

    async def test_existing_url_transitions_to_contacting(self) -> None:
        repo = MagicMock()
        worker = _make_worker(repo=repo)

        reservation = {
            "id": 10,
            "status": "created",
            "contact_platform": "kakao",
            "clinic_contact_url": "https://pf.kakao.com/_abcdef",
            "clinic_id": None,
        }

        await worker._handle_created(reservation)

        repo.update_reservation.assert_called_once_with(10, status="contacting")

    async def test_url_resolved_from_lookup_transitions_to_contacting(self) -> None:
        repo = MagicMock()
        clinic_lookup = MagicMock()
        clinic = _make_clinic(
            contact_urls={"kakao": "https://pf.kakao.com/_resolved"},
        )
        clinic_lookup.find_by_id.return_value = clinic
        worker = _make_worker(repo=repo, clinic_lookup=clinic_lookup)

        reservation = {
            "id": 11,
            "status": "created",
            "contact_platform": None,
            "clinic_contact_url": None,
            "clinic_id": 1,
        }

        await worker._handle_created(reservation)

        # First call saves the resolved URL, second call transitions status
        calls = repo.update_reservation.call_args_list
        assert len(calls) == 2
        assert calls[0] == (
            (11,),
            {
                "clinic_contact_url": "https://pf.kakao.com/_resolved",
                "contact_platform": "kakao",
            },
        )
        assert calls[1] == ((11,), {"status": "contacting"})

    async def test_respects_contact_platform_override(self) -> None:
        repo = MagicMock()
        worker = _make_worker(repo=repo, platform="kakao")

        reservation = {
            "id": 12,
            "status": "created",
            "contact_platform": "line",
            "clinic_contact_url": "https://line.me/R/ti/p/@test",
            "clinic_id": None,
        }

        await worker._handle_created(reservation)

        repo.update_reservation.assert_called_once_with(12, status="contacting")


# ---------------------------------------------------------------------------
# ClinicContactor platform property
# ---------------------------------------------------------------------------

class TestContactorPlatformProperty:
    """Verify the .platform property returns the configured platform."""

    def test_default_platform(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        contactor = ClinicContactor(device, navigator)
        assert contactor.platform == "kakao"

    def test_custom_platform(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        contactor = ClinicContactor(device, navigator, platform="line")
        assert contactor.platform == "line"


# ---------------------------------------------------------------------------
# ClinicContactor - no contact URL for platform
# ---------------------------------------------------------------------------

class TestContactorNoContactUrl:
    """Test open_clinic_chat returns False when clinic has no URL for platform."""

    async def test_no_url_returns_false(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        contactor = ClinicContactor(device, navigator, platform="kakao")

        clinic = _make_clinic(contact_urls={})

        result = await contactor.open_clinic_chat(clinic)

        assert result is False
        # Navigator should not have been called since we exit early
        navigator.ensure_foreground.assert_not_called()

    async def test_wrong_platform_returns_false(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        contactor = ClinicContactor(device, navigator, platform="line")

        clinic = _make_clinic(
            contact_urls={"kakao": "https://pf.kakao.com/_abcdef"},
        )

        result = await contactor.open_clinic_chat(clinic)

        assert result is False


# ---------------------------------------------------------------------------
# ClinicContactor - return_to_chat_list
# ---------------------------------------------------------------------------

class TestContactorReturnToChatList:
    """Test that return_to_chat_list delegates to navigator."""

    async def test_delegates_to_navigator(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        navigator.go_to_chat_list.return_value = True
        contactor = ClinicContactor(device, navigator)

        result = await contactor.return_to_chat_list()

        assert result is True
        navigator.go_to_chat_list.assert_called_once()

    async def test_returns_navigator_false(self) -> None:
        device = MagicMock()
        navigator = MagicMock()
        navigator.go_to_chat_list.return_value = False
        contactor = ClinicContactor(device, navigator)

        result = await contactor.return_to_chat_list()

        assert result is False
        navigator.go_to_chat_list.assert_called_once()
