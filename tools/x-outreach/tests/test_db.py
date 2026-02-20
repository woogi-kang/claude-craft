"""Tests for the PostgreSQL repository wrapper.

These tests verify the Repository wrapper's interface using mocked
PostgresRepository, since actual PostgreSQL requires testcontainers.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.db.repository import Repository


@pytest.fixture
def mock_repo() -> Repository:
    """Create a Repository with a mocked PostgresRepository backend."""
    with patch("src.db.repository.PostgresRepository") as mock_pg_cls:
        mock_pg = mock_pg_cls.return_value
        mock_pg.connect = AsyncMock()
        mock_pg.close = AsyncMock()
        mock_pg.insert_post = AsyncMock(return_value=1)
        mock_pg.get_posts_by_status = AsyncMock(return_value=[])
        mock_pg.update_post_status = AsyncMock()
        mock_pg.get_post = AsyncMock(return_value=None)
        mock_pg.insert_outreach = AsyncMock(return_value=1)
        mock_pg.get_pending_outreach = AsyncMock(return_value=[])
        mock_pg.count_posts = AsyncMock(return_value=0)

        repo = Repository("postgresql://localhost:5432/test")
        yield repo
        # Ensure event loop is cleaned up
        if repo._loop and not repo._loop.is_closed():
            repo._loop.close()


class TestInitDb:
    """Test database initialisation."""

    def test_init_calls_connect(self, mock_repo: Repository) -> None:
        mock_repo.init_db()
        mock_repo._repo.connect.assert_called_once()

    def test_close_calls_close(self, mock_repo: Repository) -> None:
        mock_repo.init_db()
        mock_repo.close()
        mock_repo._repo.close.assert_called_once()


class TestTweets:
    """Test tweet CRUD operations."""

    def test_insert_tweet(self, mock_repo: Repository) -> None:
        mock_repo._repo.insert_post = AsyncMock(return_value=1)
        inserted = mock_repo.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "test tweet",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        assert inserted is True
        mock_repo._repo.insert_post.assert_called_once()

    def test_insert_duplicate_returns_false(self, mock_repo: Repository) -> None:
        mock_repo._repo.insert_post = AsyncMock(return_value=-1)
        inserted = mock_repo.insert_tweet(
            {
                "tweet_id": "t1",
                "content": "duplicate",
                "author_username": "user1",
                "tweet_timestamp": "2026-02-19T10:00:00Z",
            }
        )
        assert inserted is False

    def test_get_tweets_by_status(self, mock_repo: Repository) -> None:
        expected = [{"post_id": "t1", "contents": "a", "status": "collected"}]
        mock_repo._repo.get_posts_by_status = AsyncMock(return_value=expected)
        result = mock_repo.get_tweets_by_status("collected")
        assert len(result) == 1
        assert result[0]["post_id"] == "t1"

    def test_update_tweet_status(self, mock_repo: Repository) -> None:
        mock_repo._repo.update_post_status = AsyncMock()
        updated = mock_repo.update_tweet_status(
            "t1",
            status="analyzed",
            intent_type="hospital",
            llm_decision=True,
        )
        assert updated is True
        mock_repo._repo.update_post_status.assert_called_once_with(
            "t1",
            "analyzed",
            intent_type="hospital",
            llm_decision=True,
        )

    def test_get_tweet_by_id(self, mock_repo: Repository) -> None:
        expected = {"post_id": "t42", "contents": "hello"}
        mock_repo._repo.get_post = AsyncMock(return_value=expected)
        tweet = mock_repo.get_tweet_by_id("t42")
        assert tweet is not None
        assert tweet["contents"] == "hello"

    def test_get_nonexistent_tweet(self, mock_repo: Repository) -> None:
        mock_repo._repo.get_post = AsyncMock(return_value=None)
        assert mock_repo.get_tweet_by_id("missing") is None


class TestUsers:
    """Test user operations (mostly no-ops in PostgreSQL migration)."""

    def test_insert_user_returns_true(self, mock_repo: Repository) -> None:
        assert mock_repo.insert_user({"username": "alice"}) is True

    def test_update_user_returns_true(self, mock_repo: Repository) -> None:
        assert mock_repo.update_user("carol", follower_count=100) is True


class TestActions:
    """Test action recording via outreach table."""

    def test_record_action(self, mock_repo: Repository) -> None:
        mock_repo._repo.insert_outreach = AsyncMock(return_value=1)
        row_id = mock_repo.record_action(
            action_type="search",
            tweet_id="t1",
            username="user1",
            details="keyword=test, found=5",
            status="success",
        )
        assert row_id == 1

    def test_record_action_no_tweet_returns_zero(self, mock_repo: Repository) -> None:
        row_id = mock_repo.record_action(
            action_type="search",
            tweet_id=None,
            username=None,
            details="test",
            status="success",
        )
        assert row_id == 0


class TestDailyStats:
    """Test daily statistics (computed from counts in PostgreSQL)."""

    def test_get_daily_stats(self, mock_repo: Repository) -> None:
        mock_repo._repo.count_posts = AsyncMock(return_value=42)
        stats = mock_repo.get_daily_stats("2026-02-19")
        assert stats is not None
        assert stats["date"] == "2026-02-19"
        assert stats["tweets_searched"] == 42

    def test_update_daily_stats_is_noop(self, mock_repo: Repository) -> None:
        # Should not raise
        mock_repo.update_daily_stats("2026-02-19", tweets_searched=10)


class TestConfig:
    """Test config methods (stubs in PostgreSQL migration)."""

    def test_get_config_returns_none(self, mock_repo: Repository) -> None:
        assert mock_repo.get_config("any_key") is None

    def test_set_config_is_noop(self, mock_repo: Repository) -> None:
        # Should not raise
        mock_repo.set_config("key", "value")
