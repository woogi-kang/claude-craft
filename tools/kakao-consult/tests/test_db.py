"""Tests for database repository."""

from __future__ import annotations

import pytest

from src.db.repository import Repository


class TestInitDb:
    """Test database initialisation."""

    def test_creates_tables(self, tmp_db: Repository) -> None:
        conn = tmp_db._get_conn()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {row["name"] for row in cursor.fetchall()}
        assert "conversations" in tables
        assert "messages" in tables
        assert "actions" in tables
        assert "daily_stats" in tables
        assert "blocked_users" in tables

    def test_idempotent_init(self, tmp_db: Repository) -> None:
        """Calling init_db twice should not raise."""
        tmp_db.init_db()  # Second call


class TestConversations:
    """Test conversation CRUD operations."""

    def test_upsert_inserts_new(self, tmp_db: Repository) -> None:
        inserted = tmp_db.upsert_conversation(
            chatroom_id="room_001",
            chatroom_name="Test Room",
            sender_name="Alice",
        )
        assert inserted is True

        conv = tmp_db.get_conversation("room_001")
        assert conv is not None
        assert conv["chatroom_name"] == "Test Room"
        assert conv["sender_name"] == "Alice"
        assert conv["status"] == "active"

    def test_upsert_updates_existing(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(
            chatroom_id="room_001",
            chatroom_name="Old Name",
            sender_name="Alice",
        )
        inserted = tmp_db.upsert_conversation(
            chatroom_id="room_001",
            chatroom_name="New Name",
        )
        assert inserted is False

        conv = tmp_db.get_conversation("room_001")
        assert conv is not None
        assert conv["chatroom_name"] == "New Name"
        # sender_name should remain unchanged (None was not passed)
        assert conv["sender_name"] == "Alice"

    def test_get_conversation_not_found(self, tmp_db: Repository) -> None:
        assert tmp_db.get_conversation("nonexistent") is None

    def test_update_conversation(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        updated = tmp_db.update_conversation(
            "room_001", status="paused", message_count=5
        )
        assert updated is True

        conv = tmp_db.get_conversation("room_001")
        assert conv is not None
        assert conv["status"] == "paused"
        assert conv["message_count"] == 5

    def test_update_conversation_empty_kwargs(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        assert tmp_db.update_conversation("room_001") is False


class TestMessages:
    """Test message CRUD operations."""

    def test_insert_message(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        row_id = tmp_db.insert_message(
            chatroom_id="room_001",
            direction="incoming",
            content="Hello!",
            classification="greeting",
            confidence=0.99,
        )
        assert row_id > 0

    def test_get_conversation_history(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        tmp_db.insert_message("room_001", "incoming", "First")
        tmp_db.insert_message("room_001", "outgoing", "Second")
        tmp_db.insert_message("room_001", "incoming", "Third")

        history = tmp_db.get_conversation_history("room_001", limit=2)
        assert len(history) == 2
        # Most recent first
        assert history[0]["content"] == "Third"
        assert history[1]["content"] == "Second"

    def test_get_conversation_history_empty(self, tmp_db: Repository) -> None:
        history = tmp_db.get_conversation_history("room_empty")
        assert history == []

    def test_get_last_message(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        tmp_db.insert_message("room_001", "incoming", "First")
        tmp_db.insert_message("room_001", "outgoing", "Last reply")

        last = tmp_db.get_last_message("room_001")
        assert last is not None
        assert last["content"] == "Last reply"
        assert last["direction"] == "outgoing"

    def test_get_last_message_empty(self, tmp_db: Repository) -> None:
        assert tmp_db.get_last_message("room_empty") is None


class TestActions:
    """Test action recording."""

    def test_record_action(self, tmp_db: Repository) -> None:
        row_id = tmp_db.record_action(
            action_type="auto_reply",
            chatroom_id="room_001",
            details="faq match: botox_price",
            status="success",
        )
        assert row_id > 0

    def test_record_action_with_error(self, tmp_db: Repository) -> None:
        row_id = tmp_db.record_action(
            action_type="llm_call",
            chatroom_id="room_002",
            details=None,
            status="error",
            error_message="API timeout",
        )
        assert row_id > 0


class TestDailyStats:
    """Test daily statistics tracking."""

    def test_get_nonexistent_stats(self, tmp_db: Repository) -> None:
        assert tmp_db.get_daily_stats("2026-01-01") is None

    def test_update_creates_row(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-19", messages_received=10)
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["messages_received"] == 10

    def test_update_increments(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-19", messages_received=5)
        tmp_db.update_daily_stats("2026-02-19", messages_received=3)
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["messages_received"] == 8

    def test_update_multiple_fields(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats(
            "2026-02-19",
            messages_received=10,
            messages_responded=8,
            faq_matches=5,
            claude_calls=3,
            errors=1,
        )
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["messages_received"] == 10
        assert stats["messages_responded"] == 8
        assert stats["faq_matches"] == 5
        assert stats["claude_calls"] == 3
        assert stats["errors"] == 1


class TestBlockedUsers:
    """Test blocked-user management."""

    def test_block_user(self, tmp_db: Repository) -> None:
        blocked = tmp_db.block_user("spammer", reason="repeated spam")
        assert blocked is True

    def test_block_user_duplicate(self, tmp_db: Repository) -> None:
        tmp_db.block_user("spammer", reason="spam")
        blocked = tmp_db.block_user("spammer", reason="spam again")
        assert blocked is False

    def test_is_user_blocked_true(self, tmp_db: Repository) -> None:
        tmp_db.block_user("spammer")
        assert tmp_db.is_user_blocked("spammer") is True

    def test_is_user_blocked_false(self, tmp_db: Repository) -> None:
        assert tmp_db.is_user_blocked("normal_user") is False


class TestColumnValidation:
    """Test that invalid column names are rejected."""

    def test_update_conversation_rejects_invalid_column(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        with pytest.raises(ValueError, match="Invalid column names"):
            tmp_db.update_conversation("room_001", evil_column="hack")

    def test_insert_message_rejects_invalid_column(self, tmp_db: Repository) -> None:
        tmp_db.upsert_conversation(chatroom_id="room_001")
        with pytest.raises(ValueError, match="Invalid column names"):
            tmp_db.insert_message("room_001", "incoming", "Hello", evil="hack")

    def test_update_daily_stats_rejects_invalid_column(self, tmp_db: Repository) -> None:
        with pytest.raises(ValueError, match="Invalid column names"):
            tmp_db.update_daily_stats("2026-02-19", evil_column=1)
