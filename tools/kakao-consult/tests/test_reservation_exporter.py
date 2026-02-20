"""Tests for reservation CSV exporter."""

from __future__ import annotations

import csv
from pathlib import Path

from src.reservation.exporter import ReservationExporter


class TestShouldExport:
    """Test terminal status detection."""

    def test_confirmed_is_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("confirmed") is True

    def test_declined_is_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("declined") is True

    def test_completed_is_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("completed") is True

    def test_failed_is_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("failed") is True

    def test_created_is_not_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("created") is False

    def test_negotiating_is_not_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("negotiating") is False

    def test_contacting_is_not_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("contacting") is False

    def test_paused_for_human_is_not_terminal(self) -> None:
        exporter = ReservationExporter("/tmp/unused")
        assert exporter.should_export("paused_for_human") is False


class TestExportReservation:
    """Test single reservation export."""

    def test_creates_csv_file(self, tmp_path: Path) -> None:
        exporter = ReservationExporter(tmp_path / "exports")
        reservation = {
            "request_id": "REQ-001",
            "clinic_name": "Seoul Derm",
            "patient_name": "Tanaka",
            "patient_nationality": "JP",
            "procedure_name": "Botox",
            "status": "confirmed",
        }
        exporter.export_reservation(reservation)

        assert exporter.csv_path.exists()
        with open(exporter.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["request_id"] == "REQ-001"
        assert rows[0]["clinic_name"] == "Seoul Derm"

    def test_appends_to_existing(self, tmp_path: Path) -> None:
        exporter = ReservationExporter(tmp_path / "exports")
        res1 = {
            "request_id": "REQ-001",
            "clinic_name": "A",
            "patient_name": "P",
            "procedure_name": "Botox",
            "status": "confirmed",
        }
        res2 = {
            "request_id": "REQ-002",
            "clinic_name": "B",
            "patient_name": "Q",
            "procedure_name": "Filler",
            "status": "declined",
        }
        exporter.export_reservation(res1)
        exporter.export_reservation(res2)

        with open(exporter.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["request_id"] == "REQ-001"
        assert rows[1]["request_id"] == "REQ-002"


class TestExportAll:
    """Test full export."""

    def test_export_all_creates_file(self, tmp_path: Path) -> None:
        exporter = ReservationExporter(tmp_path / "exports")
        reservations = [
            {"request_id": "REQ-001", "clinic_name": "A", "status": "confirmed"},
            {"request_id": "REQ-002", "clinic_name": "B", "status": "declined"},
            {"request_id": "REQ-003", "clinic_name": "C", "status": "completed"},
        ]
        path = exporter.export_all(reservations)
        assert path.exists()

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 3

    def test_export_all_overwrites(self, tmp_path: Path) -> None:
        exporter = ReservationExporter(tmp_path / "exports")
        exporter.export_all([{"request_id": "OLD", "status": "confirmed"}])
        exporter.export_all([{"request_id": "NEW", "status": "declined"}])

        with open(exporter.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["request_id"] == "NEW"
