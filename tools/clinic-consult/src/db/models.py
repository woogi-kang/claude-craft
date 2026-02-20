"""Database schema definitions for SQLite tables.

All table creation SQL is centralised here so that ``repository.init_db``
can bootstrap the database from a single source of truth.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Table creation DDL
# ---------------------------------------------------------------------------

CONVERSATIONS_TABLE = """\
CREATE TABLE IF NOT EXISTS conversations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chatroom_id     TEXT    UNIQUE NOT NULL,
    chatroom_name   TEXT,
    sender_name     TEXT,
    status          TEXT    NOT NULL DEFAULT 'active',
    message_count   INTEGER DEFAULT 0,
    last_message_at DATETIME,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

MESSAGES_TABLE = """\
CREATE TABLE IF NOT EXISTS messages (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    chatroom_id      TEXT    NOT NULL,
    direction        TEXT    NOT NULL,
    content          TEXT    NOT NULL,
    classification   TEXT,
    confidence       REAL,
    llm_provider     TEXT,
    template_id      TEXT,
    response_time_ms INTEGER,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chatroom_id) REFERENCES conversations(chatroom_id)
);
"""

ACTIONS_TABLE = """\
CREATE TABLE IF NOT EXISTS actions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type   TEXT NOT NULL,
    chatroom_id   TEXT,
    details       TEXT,
    status        TEXT NOT NULL,
    error_message TEXT,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

DAILY_STATS_TABLE = """\
CREATE TABLE IF NOT EXISTS daily_stats (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    date                TEXT    UNIQUE NOT NULL,
    messages_received   INTEGER DEFAULT 0,
    messages_responded  INTEGER DEFAULT 0,
    faq_matches         INTEGER DEFAULT 0,
    llm_responses       INTEGER DEFAULT 0,
    claude_calls        INTEGER DEFAULT 0,
    gpt4_calls          INTEGER DEFAULT 0,
    ollama_calls        INTEGER DEFAULT 0,
    template_responses  INTEGER DEFAULT 0,
    errors              INTEGER DEFAULT 0,
    avg_response_time_ms REAL   DEFAULT 0,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

BLOCKED_USERS_TABLE = """\
CREATE TABLE IF NOT EXISTS blocked_users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_name TEXT    UNIQUE NOT NULL,
    reason      TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

ALL_TABLES: list[str] = [
    CONVERSATIONS_TABLE,
    MESSAGES_TABLE,
    ACTIONS_TABLE,
    DAILY_STATS_TABLE,
    BLOCKED_USERS_TABLE,
]

# ---------------------------------------------------------------------------
# Indexes for common query patterns
# ---------------------------------------------------------------------------

INDEXES: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_messages_chatroom ON messages(chatroom_id);",
    "CREATE INDEX IF NOT EXISTS idx_messages_direction ON messages(direction);",
    "CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(date);",
    "CREATE INDEX IF NOT EXISTS idx_blocked_users_name ON blocked_users(sender_name);",
    "CREATE INDEX IF NOT EXISTS idx_actions_type ON actions(action_type);",
]
