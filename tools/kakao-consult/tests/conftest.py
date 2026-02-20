"""Shared fixtures for the kakao-consult test suite."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.db.repository import Repository


@pytest.fixture
def tmp_db(tmp_path: Path) -> Repository:
    """Provide a fresh in-memory-style SQLite repository."""
    db_path = tmp_path / "test.db"
    repo = Repository(db_path)
    repo.init_db()
    yield repo
    repo.close()


@pytest.fixture
def tmp_reservation_repo(tmp_path: Path):
    """Provide a fresh SQLite ReservationRepository."""
    from src.reservation.repository import ReservationRepository

    repo = ReservationRepository(tmp_path / "test_reservations.db")
    repo.init_db()
    yield repo
    repo.close()


@pytest.fixture
def sample_messages() -> list[dict]:
    """Provide a batch of sample message dicts for testing."""
    return [
        {
            "chatroom_id": "room_001",
            "direction": "incoming",
            "content": "How much is botox?",
            "classification": "faq",
            "confidence": 0.95,
        },
        {
            "chatroom_id": "room_001",
            "direction": "outgoing",
            "content": "Botox starts from 30,000 KRW.",
            "llm_provider": "claude",
            "response_time_ms": 350,
        },
        {
            "chatroom_id": "room_002",
            "direction": "incoming",
            "content": "Hello!",
            "classification": "greeting",
            "confidence": 0.99,
        },
        {
            "chatroom_id": "room_002",
            "direction": "outgoing",
            "content": "Welcome! How can I help you?",
            "template_id": "greeting_default",
            "response_time_ms": 50,
        },
        {
            "chatroom_id": "room_003",
            "direction": "incoming",
            "content": "I want to file a complaint about my last visit.",
            "classification": "complaint",
            "confidence": 0.88,
        },
    ]
