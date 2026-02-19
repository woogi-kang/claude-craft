"""Database schema definitions for SQLite tables.

All table creation SQL is centralised here so that ``repository.init_db``
can bootstrap the database from a single source of truth.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Table creation DDL
# ---------------------------------------------------------------------------

TWEETS_TABLE = """\
CREATE TABLE IF NOT EXISTS tweets (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id                TEXT    UNIQUE NOT NULL,
    content                 TEXT    NOT NULL,
    author_username         TEXT    NOT NULL,
    author_display_name     TEXT,
    author_follower_count   INTEGER,
    author_following_count  INTEGER,
    author_bio              TEXT,
    tweet_timestamp         DATETIME NOT NULL,
    likes                   INTEGER DEFAULT 0,
    retweets                INTEGER DEFAULT 0,
    replies                 INTEGER DEFAULT 0,
    tweet_url               TEXT,
    search_keyword          TEXT,
    status                  TEXT    NOT NULL DEFAULT 'collected',
    classification          TEXT,
    confidence              REAL,
    classification_rationale TEXT,
    template_category       TEXT,
    reply_content           TEXT,
    reply_tweet_id          TEXT,
    reply_timestamp         DATETIME,
    dm_content              TEXT,
    dm_template_used        TEXT,
    dm_timestamp            DATETIME,
    dm_skip_reason          TEXT,
    created_at              DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at              DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

USERS_TABLE = """\
CREATE TABLE IF NOT EXISTS users (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    username              TEXT    UNIQUE NOT NULL,
    display_name          TEXT,
    follower_count        INTEGER,
    following_count       INTEGER,
    bio                   TEXT,
    is_blocked            INTEGER DEFAULT 0,
    first_seen            DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_contacted        DATETIME,
    contact_count         INTEGER DEFAULT 0,
    dm_open               INTEGER DEFAULT 1,
    dm_response_received  INTEGER DEFAULT 0,
    dm_response_at        DATETIME,
    created_at            DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

ACTIONS_TABLE = """\
CREATE TABLE IF NOT EXISTS actions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type   TEXT NOT NULL,
    tweet_id      TEXT,
    username      TEXT,
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
    tweets_searched     INTEGER DEFAULT 0,
    tweets_collected    INTEGER DEFAULT 0,
    tweets_analyzed     INTEGER DEFAULT 0,
    tweets_needs_help   INTEGER DEFAULT 0,
    tweets_seeking_info INTEGER DEFAULT 0,
    tweets_irrelevant   INTEGER DEFAULT 0,
    replies_sent        INTEGER DEFAULT 0,
    dms_sent            INTEGER DEFAULT 0,
    dms_skipped         INTEGER DEFAULT 0,
    dm_responses        INTEGER DEFAULT 0,
    errors              INTEGER DEFAULT 0,
    api_tweets_used     INTEGER DEFAULT 0,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

CONFIG_TABLE = """\
CREATE TABLE IF NOT EXISTS config (
    key        TEXT PRIMARY KEY,
    value      TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

ALL_TABLES: list[str] = [
    TWEETS_TABLE,
    USERS_TABLE,
    ACTIONS_TABLE,
    DAILY_STATS_TABLE,
    CONFIG_TABLE,
]

# ---------------------------------------------------------------------------
# Indexes for common query patterns
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Migrations for existing databases (ALTER TABLE with error handling)
# ---------------------------------------------------------------------------

MIGRATIONS: list[str] = [
    # M4: Add dm_responses column to daily_stats
    "ALTER TABLE daily_stats ADD COLUMN dm_responses INTEGER DEFAULT 0;",
    # M4: Add dm_response_received and dm_response_at columns to users
    "ALTER TABLE users ADD COLUMN dm_response_received INTEGER DEFAULT 0;",
    "ALTER TABLE users ADD COLUMN dm_response_at DATETIME;",
]

# ---------------------------------------------------------------------------
# Indexes for common query patterns
# ---------------------------------------------------------------------------

INDEXES: list[str] = [
    "CREATE INDEX IF NOT EXISTS idx_tweets_status ON tweets(status);",
    "CREATE INDEX IF NOT EXISTS idx_tweets_author ON tweets(author_username);",
    "CREATE INDEX IF NOT EXISTS idx_tweets_timestamp ON tweets(tweet_timestamp);",
    "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
    "CREATE INDEX IF NOT EXISTS idx_actions_type ON actions(action_type);",
    "CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(date);",
]
