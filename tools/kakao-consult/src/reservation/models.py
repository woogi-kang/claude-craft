"""Database schema for reservations.

All reservation-related DDL is centralised here, following the same
pattern as ``db.models``.
"""

from __future__ import annotations

RESERVATIONS_TABLE = """\
CREATE TABLE IF NOT EXISTS reservations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id          TEXT    UNIQUE NOT NULL,
    clinic_id           INTEGER,
    clinic_name         TEXT    NOT NULL,
    clinic_kakao_url    TEXT,
    patient_name        TEXT    NOT NULL,
    patient_nationality TEXT    DEFAULT 'JP',
    patient_age         INTEGER,
    patient_gender      TEXT,
    patient_contact     TEXT,
    procedure_name      TEXT    NOT NULL,
    preferred_dates     TEXT,
    preferred_time      TEXT    DEFAULT 'any',
    notes               TEXT,
    status              TEXT    NOT NULL DEFAULT 'created',
    confirmed_date      TEXT,
    confirmed_time      TEXT,
    confirmed_price     TEXT,
    confirmed_doctor    TEXT,
    clinic_instructions TEXT,
    decline_reason      TEXT,
    turn_count          INTEGER DEFAULT 0,
    paused_reason       TEXT,
    error_message       TEXT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    contacted_at        DATETIME,
    confirmed_at        DATETIME,
    completed_at        DATETIME,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

RESERVATION_MESSAGES_TABLE = """\
CREATE TABLE IF NOT EXISTS reservation_messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_id  INTEGER NOT NULL,
    direction       TEXT    NOT NULL,
    content         TEXT    NOT NULL,
    llm_provider    TEXT,
    extracted_json  TEXT,
    phase           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(id)
);
"""

ALL_RESERVATION_TABLES: list[str] = [
    RESERVATIONS_TABLE,
    RESERVATION_MESSAGES_TABLE,
]

RESERVATION_INDEXES: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);",
    "CREATE INDEX IF NOT EXISTS idx_reservations_clinic ON reservations(clinic_id);",
    "CREATE INDEX IF NOT EXISTS idx_reservation_msgs_res ON reservation_messages(reservation_id);",
]

# Valid reservation statuses (state machine)
VALID_STATUSES = frozenset({
    "created",
    "contacting",
    "greeting_sent",
    "negotiating",
    "paused_for_human",
    "confirmed",
    "declined",
    "completed",
    "timed_out",
    "failed",
})
