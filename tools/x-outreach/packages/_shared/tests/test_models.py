"""Tests for the DDL model definitions."""

from __future__ import annotations

from outreach_shared.db.models import ACCOUNTS_DDL, ALL_DDL, INDEXES_DDL, OUTREACH_DDL, POSTS_DDL


class TestDDL:
    """Verify DDL strings are well-formed."""

    def test_posts_ddl_has_required_columns(self) -> None:
        assert "post_id" in POSTS_DDL
        assert "platform" in POSTS_DDL
        assert "user_id" in POSTS_DDL
        assert "contents" in POSTS_DDL
        assert "intent_type" in POSTS_DDL
        assert "keyword_intent" in POSTS_DDL
        assert "llm_decision" in POSTS_DDL
        assert "status" in POSTS_DDL

    def test_accounts_ddl_has_required_columns(self) -> None:
        assert "account_id" in ACCOUNTS_DDL
        assert "platform" in ACCOUNTS_DDL
        assert "account_type" in ACCOUNTS_DDL
        assert "maturity" in ACCOUNTS_DDL
        assert "daily_comment_count" in ACCOUNTS_DDL
        assert "session_data_dir" in ACCOUNTS_DDL

    def test_outreach_ddl_has_required_columns(self) -> None:
        assert "post_id" in OUTREACH_DDL
        assert "user_id" in OUTREACH_DDL
        assert "account_id" in OUTREACH_DDL
        assert "outreach_type" in OUTREACH_DDL
        assert "message" in OUTREACH_DDL
        assert "status" in OUTREACH_DDL

    def test_outreach_references_posts(self) -> None:
        assert "REFERENCES posts(post_id)" in OUTREACH_DDL

    def test_outreach_references_accounts(self) -> None:
        assert "REFERENCES accounts(account_id)" in OUTREACH_DDL

    def test_indexes_cover_key_columns(self) -> None:
        assert "idx_posts_status" in INDEXES_DDL
        assert "idx_posts_platform" in INDEXES_DDL
        assert "idx_outreach_status" in INDEXES_DDL
        assert "idx_accounts_status" in INDEXES_DDL
        assert "idx_accounts_maturity" in INDEXES_DDL

    def test_all_ddl_order(self) -> None:
        # Accounts must come before posts/outreach due to FK references
        assert ALL_DDL[0] is ACCOUNTS_DDL
        assert ALL_DDL[1] is POSTS_DDL
        assert ALL_DDL[2] is OUTREACH_DDL
        assert ALL_DDL[3] is INDEXES_DDL

    def test_all_ddl_are_create_if_not_exists(self) -> None:
        for ddl in [POSTS_DDL, ACCOUNTS_DDL, OUTREACH_DDL]:
            assert "IF NOT EXISTS" in ddl

    def test_indexes_are_create_if_not_exists(self) -> None:
        for line in INDEXES_DDL.strip().split("\n"):
            if line.strip():
                assert "IF NOT EXISTS" in line
