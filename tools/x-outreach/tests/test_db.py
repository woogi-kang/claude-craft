"""Tests for database repository."""

from __future__ import annotations

from pathlib import Path

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
        assert "tweets" in tables
        assert "users" in tables
        assert "actions" in tables
        assert "daily_stats" in tables
        assert "config" in tables

    def test_idempotent_init(self, tmp_db: Repository) -> None:
        """Calling init_db twice should not raise."""
        tmp_db.init_db()  # Second call


class TestTweets:
    """Test tweet CRUD operations."""

    def test_insert_tweet(self, tmp_db: Repository) -> None:
        inserted = tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "test tweet",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        assert inserted is True

    def test_insert_duplicate_ignored(self, tmp_db: Repository) -> None:
        tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "first",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        inserted = tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "duplicate",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        assert inserted is False

    def test_get_tweets_by_status(self, tmp_db: Repository) -> None:
        tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "a",
                "author_username": "u1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
                "status": "collected",
            }
        )
        tmp_db.insert_tweet(
            {
                "tweet_id": "t2",
                "content": "b",
                "author_username": "u2",
                "tweet_timestamp": "2026-02-19T11:00:00Z",
                "status": "analyzed",
            }
        )
        collected = tmp_db.get_tweets_by_status("collected")
        assert len(collected) == 1
        assert collected[0]["tweet_id"] == "t1"

    def test_update_tweet_status(self, tmp_db: Repository) -> None:
        tmp_db.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "test",
                "author_username": "u1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
                "status": "collected",
            }
        )
        updated = tmp_db.update_tweet_status(
            "t1",
            status="analyzed",
            classification="needs_help",
            confidence=0.85,
        )
        assert updated is True
        tweet = tmp_db.get_tweet_by_id("t1")
        assert tweet is not None
        assert tweet["status"] == "analyzed"
        assert tweet["classification"] == "needs_help"
        assert tweet["confidence"] == 0.85

    def test_get_tweet_by_id(self, tmp_db: Repository) -> None:
        tmp_db.insert_tweet(
            {
                "tweet_id": "t42",
                "content": "hello",
                "author_username": "u1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        tweet = tmp_db.get_tweet_by_id("t42")
        assert tweet is not None
        assert tweet["content"] == "hello"

    def test_get_nonexistent_tweet(self, tmp_db: Repository) -> None:
        assert tmp_db.get_tweet_by_id("missing") is None


class TestUsers:
    """Test user CRUD operations."""

    def test_insert_user(self, tmp_db: Repository) -> None:
        inserted = tmp_db.insert_user(
            {"username": "alice", "display_name": "Alice", "follower_count": 100}
        )
        assert inserted is True

    def test_insert_duplicate_user(self, tmp_db: Repository) -> None:
        tmp_db.insert_user({"username": "alice"})
        inserted = tmp_db.insert_user({"username": "alice"})
        assert inserted is False

    def test_get_user(self, tmp_db: Repository) -> None:
        tmp_db.insert_user(
            {"username": "bob", "display_name": "Bob", "bio": "hello"}
        )
        user = tmp_db.get_user("bob")
        assert user is not None
        assert user["display_name"] == "Bob"

    def test_get_nonexistent_user(self, tmp_db: Repository) -> None:
        assert tmp_db.get_user("nobody") is None

    def test_update_user(self, tmp_db: Repository) -> None:
        tmp_db.insert_user({"username": "carol", "follower_count": 50})
        tmp_db.update_user("carol", follower_count=100, bio="updated")
        user = tmp_db.get_user("carol")
        assert user is not None
        assert user["follower_count"] == 100
        assert user["bio"] == "updated"

    def test_is_user_contacted_false(self, tmp_db: Repository) -> None:
        tmp_db.insert_user({"username": "dave", "contact_count": 0})
        assert tmp_db.is_user_contacted("dave") is False

    def test_is_user_contacted_true(self, tmp_db: Repository) -> None:
        tmp_db.insert_user({"username": "eve"})
        tmp_db.update_user("eve", contact_count=1)
        assert tmp_db.is_user_contacted("eve") is True

    def test_is_user_contacted_unknown(self, tmp_db: Repository) -> None:
        assert tmp_db.is_user_contacted("unknown") is False


class TestActions:
    """Test action recording."""

    def test_record_action(self, tmp_db: Repository) -> None:
        row_id = tmp_db.record_action(
            action_type="search",
            tweet_id=None,
            username=None,
            details="keyword=test, found=5",
            status="success",
        )
        assert row_id > 0

    def test_record_action_with_error(self, tmp_db: Repository) -> None:
        row_id = tmp_db.record_action(
            action_type="login",
            tweet_id=None,
            username="burner",
            details=None,
            status="error",
            error_message="Timeout",
        )
        assert row_id > 0


class TestDailyStats:
    """Test daily statistics tracking."""

    def test_get_nonexistent_stats(self, tmp_db: Repository) -> None:
        assert tmp_db.get_daily_stats("2026-01-01") is None

    def test_update_creates_row(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-19", tweets_searched=10)
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["tweets_searched"] == 10

    def test_update_increments(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats("2026-02-19", tweets_searched=5)
        tmp_db.update_daily_stats("2026-02-19", tweets_searched=3)
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["tweets_searched"] == 8

    def test_update_multiple_fields(self, tmp_db: Repository) -> None:
        tmp_db.update_daily_stats(
            "2026-02-19",
            tweets_collected=10,
            tweets_analyzed=8,
            errors=1,
        )
        stats = tmp_db.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["tweets_collected"] == 10
        assert stats["tweets_analyzed"] == 8
        assert stats["errors"] == 1
