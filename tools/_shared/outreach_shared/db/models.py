"""Unified PostgreSQL DDL for the outreach platform.

Defines three core tables shared across X and XHS pipelines:
- posts: crawled content from any platform
- accounts: account pool with maturity lifecycle
- outreach: outreach actions (reply, comment, DM)
"""

from __future__ import annotations

POSTS_DDL = """\
CREATE TABLE IF NOT EXISTS posts (
    id              SERIAL PRIMARY KEY,
    post_id         TEXT UNIQUE NOT NULL,
    platform        TEXT NOT NULL,
    user_id         TEXT NOT NULL,
    username        TEXT,
    contents        TEXT NOT NULL,
    intent_type     TEXT,
    keyword_intent  TEXT,
    llm_decision    BOOLEAN DEFAULT NULL,
    llm_rationale   TEXT,
    likes_count     INTEGER DEFAULT 0,
    comments_count  INTEGER DEFAULT 0,
    retweets_count  INTEGER DEFAULT 0,
    post_url        TEXT,
    author_bio      TEXT,
    author_followers INTEGER DEFAULT 0,
    search_keyword  TEXT,
    status          TEXT NOT NULL DEFAULT 'collected',
    crawled_at      TIMESTAMPTZ DEFAULT NOW(),
    post_created_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
"""

ACCOUNTS_DDL = """\
CREATE TABLE IF NOT EXISTS accounts (
    account_id      TEXT PRIMARY KEY,
    platform        TEXT NOT NULL,
    account_type    TEXT NOT NULL,
    username        TEXT,
    proxy_ip        TEXT,
    status          TEXT NOT NULL DEFAULT 'nurturing',
    maturity        TEXT NOT NULL DEFAULT 'new',
    daily_comment_count INTEGER DEFAULT 0,
    daily_dm_count  INTEGER DEFAULT 0,
    daily_search_count INTEGER DEFAULT 0,
    last_warning_at TIMESTAMPTZ,
    last_used_at    TIMESTAMPTZ,
    session_data_dir TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    banned_at       TIMESTAMPTZ
);
"""

OUTREACH_DDL = """\
CREATE TABLE IF NOT EXISTS outreach (
    id              SERIAL PRIMARY KEY,
    post_id         TEXT REFERENCES posts(post_id),
    user_id         TEXT NOT NULL,
    account_id      TEXT REFERENCES accounts(account_id),
    platform        TEXT NOT NULL,
    outreach_type   TEXT NOT NULL,
    message         TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'pending',
    error_message   TEXT,
    replied         BOOLEAN DEFAULT FALSE,
    scheduled_at    TIMESTAMPTZ,
    sent_at         TIMESTAMPTZ,
    replied_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
"""

INDEXES_DDL = """\
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_post_id ON posts(post_id);
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_crawled_at ON posts(crawled_at);
CREATE INDEX IF NOT EXISTS idx_outreach_status ON outreach(status);
CREATE INDEX IF NOT EXISTS idx_outreach_post_id ON outreach(post_id);
CREATE INDEX IF NOT EXISTS idx_outreach_account_id ON outreach(account_id);
CREATE INDEX IF NOT EXISTS idx_outreach_platform ON outreach(platform);
CREATE INDEX IF NOT EXISTS idx_accounts_platform ON accounts(platform);
CREATE INDEX IF NOT EXISTS idx_accounts_status ON accounts(status);
CREATE INDEX IF NOT EXISTS idx_accounts_maturity ON accounts(maturity);
"""

ALL_DDL = [ACCOUNTS_DDL, POSTS_DDL, OUTREACH_DDL, INDEXES_DDL]
