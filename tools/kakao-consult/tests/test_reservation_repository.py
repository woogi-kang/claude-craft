"""Tests for reservation repository."""

from __future__ import annotations

import pytest

from src.reservation.repository import ReservationRepository, VALID_TRANSITIONS


class TestInitDb:
    """Test database initialisation."""

    def test_creates_tables(self, tmp_reservation_repo: ReservationRepository) -> None:
        conn = tmp_reservation_repo._get_conn()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {row["name"] for row in cursor.fetchall()}
        assert "reservations" in tables
        assert "reservation_messages" in tables

    def test_idempotent_init(self, tmp_reservation_repo: ReservationRepository) -> None:
        """Calling init_db twice should not raise."""
        tmp_reservation_repo.init_db()


class TestCreateReservation:
    """Test reservation creation."""

    def test_returns_valid_id(self, tmp_reservation_repo: ReservationRepository) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Test Clinic",
            patient_name="Tanaka",
            procedure_name="Botox",
        )
        assert rid > 0

    def test_multiple_reservations_get_unique_ids(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid1 = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Clinic A",
            patient_name="Tanaka",
            procedure_name="Botox",
        )
        rid2 = tmp_reservation_repo.create_reservation(
            request_id="REQ-002",
            clinic_name="Clinic B",
            patient_name="Sato",
            procedure_name="Filler",
        )
        assert rid1 != rid2


class TestGetReservation:
    """Test fetching reservations."""

    def test_returns_correct_data(self, tmp_reservation_repo: ReservationRepository) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Seoul Derm",
            patient_name="Tanaka",
            procedure_name="Laser",
            patient_nationality="JP",
        )
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["clinic_name"] == "Seoul Derm"
        assert row["patient_name"] == "Tanaka"
        assert row["procedure_name"] == "Laser"
        assert row["patient_nationality"] == "JP"
        assert row["status"] == "created"

    def test_returns_none_for_missing(self, tmp_reservation_repo: ReservationRepository) -> None:
        assert tmp_reservation_repo.get_reservation(9999) is None


class TestGetByRequestId:
    """Test lookup by request_id."""

    def test_returns_match(self, tmp_reservation_repo: ReservationRepository) -> None:
        tmp_reservation_repo.create_reservation(
            request_id="REQ-XYZ",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )
        row = tmp_reservation_repo.get_by_request_id("REQ-XYZ")
        assert row is not None
        assert row["request_id"] == "REQ-XYZ"

    def test_returns_none_for_missing(self, tmp_reservation_repo: ReservationRepository) -> None:
        assert tmp_reservation_repo.get_by_request_id("NOPE") is None


class TestUpdateReservation:
    """Test reservation updates and validation."""

    def test_rejects_invalid_column(self, tmp_reservation_repo: ReservationRepository) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )
        with pytest.raises(ValueError, match="Invalid column names"):
            tmp_reservation_repo.update_reservation(rid, evil_column="hack")

    def test_rejects_invalid_status(self, tmp_reservation_repo: ReservationRepository) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )
        with pytest.raises(ValueError, match="Invalid status"):
            tmp_reservation_repo.update_reservation(rid, status="nonexistent_status")

    def test_returns_false_for_empty_kwargs(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )
        assert tmp_reservation_repo.update_reservation(rid) is False

    def test_updates_valid_fields(self, tmp_reservation_repo: ReservationRepository) -> None:
        rid = tmp_reservation_repo.create_reservation(
            request_id="REQ-001",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )
        updated = tmp_reservation_repo.update_reservation(rid, notes="VIP patient")
        assert updated is True
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["notes"] == "VIP patient"


class TestStateTransitions:
    """Test the state machine transition enforcement."""

    def _make_reservation(
        self, repo: ReservationRepository, request_id: str = "REQ-T"
    ) -> int:
        return repo.create_reservation(
            request_id=request_id,
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )

    def test_created_to_contacting_allowed(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="contacting")
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["status"] == "contacting"

    def test_created_to_confirmed_rejected(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        with pytest.raises(ValueError, match="Invalid transition"):
            tmp_reservation_repo.update_reservation(rid, status="confirmed")

    def test_confirmed_to_completed_allowed(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        # Walk through valid path: created -> contacting -> greeting_sent -> negotiating -> confirmed
        tmp_reservation_repo.update_reservation(rid, status="contacting")
        tmp_reservation_repo.update_reservation(rid, status="greeting_sent")
        tmp_reservation_repo.update_reservation(rid, status="negotiating")
        tmp_reservation_repo.update_reservation(rid, status="confirmed")
        tmp_reservation_repo.update_reservation(rid, status="completed")
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["status"] == "completed"

    def test_completed_is_terminal(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="contacting")
        tmp_reservation_repo.update_reservation(rid, status="greeting_sent")
        tmp_reservation_repo.update_reservation(rid, status="negotiating")
        tmp_reservation_repo.update_reservation(rid, status="confirmed")
        tmp_reservation_repo.update_reservation(rid, status="completed")
        with pytest.raises(ValueError, match="Invalid transition"):
            tmp_reservation_repo.update_reservation(rid, status="contacting")

    def test_negotiating_to_paused_for_human_allowed(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="contacting")
        tmp_reservation_repo.update_reservation(rid, status="greeting_sent")
        tmp_reservation_repo.update_reservation(rid, status="negotiating")
        tmp_reservation_repo.update_reservation(rid, status="paused_for_human")
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["status"] == "paused_for_human"

    def test_declined_is_terminal(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="contacting")
        tmp_reservation_repo.update_reservation(rid, status="greeting_sent")
        tmp_reservation_repo.update_reservation(rid, status="negotiating")
        tmp_reservation_repo.update_reservation(rid, status="declined")
        with pytest.raises(ValueError, match="Invalid transition"):
            tmp_reservation_repo.update_reservation(rid, status="negotiating")

    def test_failed_is_terminal(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="failed")
        with pytest.raises(ValueError, match="Invalid transition"):
            tmp_reservation_repo.update_reservation(rid, status="created")

    def test_same_status_noop(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        """Setting the same status should succeed (no-op transition)."""
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.update_reservation(rid, status="created")
        row = tmp_reservation_repo.get_reservation(rid)
        assert row is not None
        assert row["status"] == "created"


class TestListReservations:
    """Test listing reservations with and without filters."""

    def _seed(self, repo: ReservationRepository) -> None:
        repo.create_reservation(
            request_id="REQ-A", clinic_name="A", patient_name="P", procedure_name="Botox"
        )
        rid2 = repo.create_reservation(
            request_id="REQ-B", clinic_name="B", patient_name="P", procedure_name="Filler"
        )
        repo.update_reservation(rid2, status="contacting")

    def test_list_all(self, tmp_reservation_repo: ReservationRepository) -> None:
        self._seed(tmp_reservation_repo)
        rows = tmp_reservation_repo.list_reservations()
        assert len(rows) == 2

    def test_list_with_status_filter(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        self._seed(tmp_reservation_repo)
        rows = tmp_reservation_repo.list_reservations(status="created")
        assert len(rows) == 1
        assert rows[0]["clinic_name"] == "A"

    def test_list_empty(self, tmp_reservation_repo: ReservationRepository) -> None:
        rows = tmp_reservation_repo.list_reservations()
        assert rows == []


class TestListActive:
    """Test listing active reservations."""

    def test_returns_active_statuses(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid1 = tmp_reservation_repo.create_reservation(
            request_id="REQ-1", clinic_name="A", patient_name="P", procedure_name="B"
        )
        rid2 = tmp_reservation_repo.create_reservation(
            request_id="REQ-2", clinic_name="B", patient_name="P", procedure_name="F"
        )
        rid3 = tmp_reservation_repo.create_reservation(
            request_id="REQ-3", clinic_name="C", patient_name="P", procedure_name="L"
        )
        # Move rid2 to contacting (active) and rid3 to failed (not active)
        tmp_reservation_repo.update_reservation(rid2, status="contacting")
        tmp_reservation_repo.update_reservation(rid3, status="failed")

        active = tmp_reservation_repo.list_active()
        active_ids = {r["id"] for r in active}
        assert rid1 in active_ids  # created is active
        assert rid2 in active_ids  # contacting is active
        assert rid3 not in active_ids  # failed is not active


class TestListPaused:
    """Test listing paused reservations."""

    def test_returns_paused_only(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid1 = tmp_reservation_repo.create_reservation(
            request_id="REQ-1", clinic_name="A", patient_name="P", procedure_name="B"
        )
        rid2 = tmp_reservation_repo.create_reservation(
            request_id="REQ-2", clinic_name="B", patient_name="P", procedure_name="F"
        )
        # Move rid2 to paused_for_human via valid path
        tmp_reservation_repo.update_reservation(rid2, status="contacting")
        tmp_reservation_repo.update_reservation(rid2, status="greeting_sent")
        tmp_reservation_repo.update_reservation(rid2, status="paused_for_human")

        paused = tmp_reservation_repo.list_paused()
        assert len(paused) == 1
        assert paused[0]["id"] == rid2

    def test_returns_empty_when_none_paused(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        tmp_reservation_repo.create_reservation(
            request_id="REQ-1", clinic_name="A", patient_name="P", procedure_name="B"
        )
        assert tmp_reservation_repo.list_paused() == []


class TestMessages:
    """Test reservation message operations."""

    def _make_reservation(self, repo: ReservationRepository) -> int:
        return repo.create_reservation(
            request_id="REQ-MSG",
            clinic_name="Clinic",
            patient_name="Pat",
            procedure_name="Botox",
        )

    def test_add_message_returns_id(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        mid = tmp_reservation_repo.add_message(rid, "outgoing", "Hello clinic!")
        assert mid > 0

    def test_get_messages_ordered(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.add_message(rid, "outgoing", "First")
        tmp_reservation_repo.add_message(rid, "incoming", "Second")
        tmp_reservation_repo.add_message(rid, "outgoing", "Third")

        msgs = tmp_reservation_repo.get_messages(rid)
        assert len(msgs) == 3
        assert msgs[0]["content"] == "First"
        assert msgs[1]["content"] == "Second"
        assert msgs[2]["content"] == "Third"

    def test_get_messages_empty(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        assert tmp_reservation_repo.get_messages(rid) == []

    def test_get_last_incoming(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.add_message(rid, "incoming", "First incoming")
        tmp_reservation_repo.add_message(rid, "outgoing", "Reply")
        tmp_reservation_repo.add_message(rid, "incoming", "Second incoming")

        last = tmp_reservation_repo.get_last_incoming(rid)
        assert last is not None
        assert last["content"] == "Second incoming"
        assert last["direction"] == "incoming"

    def test_get_last_incoming_none(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        tmp_reservation_repo.add_message(rid, "outgoing", "Only outgoing")
        assert tmp_reservation_repo.get_last_incoming(rid) is None

    def test_message_count(
        self, tmp_reservation_repo: ReservationRepository
    ) -> None:
        rid = self._make_reservation(tmp_reservation_repo)
        assert tmp_reservation_repo.message_count(rid) == 0

        tmp_reservation_repo.add_message(rid, "outgoing", "A")
        tmp_reservation_repo.add_message(rid, "incoming", "B")
        assert tmp_reservation_repo.message_count(rid) == 2
