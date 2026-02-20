"""CSV export for reservation results.

Auto-exports reservation data when status changes to a terminal state
(confirmed, declined, completed, failed).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


_EXPORT_COLUMNS = [
    "request_id",
    "clinic_name",
    "clinic_contact_url",
    "contact_platform",
    "patient_name",
    "patient_nationality",
    "patient_age",
    "patient_gender",
    "patient_contact",
    "procedure_name",
    "status",
    "confirmed_date",
    "confirmed_time",
    "confirmed_price",
    "confirmed_doctor",
    "clinic_instructions",
    "decline_reason",
    "notes",
    "turn_count",
    "created_at",
    "completed_at",
]

_TERMINAL_STATUSES = frozenset({"confirmed", "declined", "completed", "failed"})


class ReservationExporter:
    """Exports reservation data to CSV."""

    def __init__(self, export_dir: str | Path) -> None:
        self._export_dir = Path(export_dir)
        self._export_dir.mkdir(parents=True, exist_ok=True)
        self._csv_path = self._export_dir / "reservations.csv"

    @property
    def csv_path(self) -> Path:
        return self._csv_path

    def should_export(self, status: str) -> bool:
        """Check if the status warrants a CSV export."""
        return status in _TERMINAL_STATUSES

    def export_reservation(self, reservation: dict[str, Any]) -> None:
        """Append a single reservation to the CSV file."""
        file_exists = self._csv_path.exists()
        with open(self._csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_EXPORT_COLUMNS)
            if not file_exists:
                writer.writeheader()
            row = {col: reservation.get(col, "") for col in _EXPORT_COLUMNS}
            writer.writerow(row)

    def export_all(self, reservations: list[dict[str, Any]]) -> Path:
        """Export all reservations to CSV (overwrites existing file)."""
        with open(self._csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=_EXPORT_COLUMNS)
            writer.writeheader()
            for res in reservations:
                row = {col: res.get(col, "") for col in _EXPORT_COLUMNS}
                writer.writerow(row)
        return self._csv_path
