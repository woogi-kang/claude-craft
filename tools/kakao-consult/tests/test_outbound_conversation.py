"""Tests for outbound conversation manager."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.ai.providers.base import LLMResponse
from src.outbound.conversation import ConversationManager, TurnResult
from src.reservation.exporter import ReservationExporter
from src.reservation.repository import ReservationRepository


# ---------------------------------------------------------------------------
# Mock LLM provider
# ---------------------------------------------------------------------------

class MockProvider:
    """Minimal LLM provider for testing."""

    name = "mock"
    is_available = True

    def __init__(self, response_text: str = "mock response") -> None:
        self._text = response_text
        self.call_count = 0

    async def generate(
        self,
        message: str,
        conversation_history: list[dict[str, str]],
        system_prompt: str,
    ) -> LLMResponse:
        self.call_count += 1
        return LLMResponse(text=self._text, provider="mock", model="mock-1")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_repo(tmp_path: Path) -> ReservationRepository:
    repo = ReservationRepository(tmp_path / "conv_test.db")
    repo.init_db()
    return repo


def _make_exporter(tmp_path: Path) -> ReservationExporter:
    return ReservationExporter(tmp_path / "exports")


def _make_reservation(repo: ReservationRepository, status: str = "greeting_sent") -> int:
    rid = repo.create_reservation(
        request_id="REQ-CONV-001",
        clinic_name="Test Clinic",
        patient_name="Tanaka",
        procedure_name="Botox",
        preferred_dates=["2026-04-01"],
    )
    if status != "created":
        # Walk through the valid path
        transitions = {
            "contacting": ["contacting"],
            "greeting_sent": ["contacting", "greeting_sent"],
            "negotiating": ["contacting", "greeting_sent", "negotiating"],
            "paused_for_human": ["contacting", "greeting_sent", "paused_for_human"],
        }
        for s in transitions.get(status, []):
            repo.update_reservation(rid, status=s)
    return rid


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestConversationManagerInit:
    """Test ConversationManager construction."""

    def test_accepts_all_params(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)
        provider = MockProvider()

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
            agency_name="Custom Agency",
        )
        assert mgr is not None
        # Verify agency name was injected
        assert "Custom Agency" in mgr._agency_identity
        repo.close()


class TestGenerateGreeting:
    """Test greeting generation."""

    async def test_calls_llm_and_records_message(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)
        provider = MockProvider(response_text="Hello clinic, this is a test greeting.")

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
        )

        rid = repo.create_reservation(
            request_id="REQ-G1",
            clinic_name="Gangnam Clinic",
            patient_name="Tanaka",
            procedure_name="Botox",
            preferred_dates=["2026-03-01"],
        )
        # Advance to contacting so greeting_sent transition is valid
        repo.update_reservation(rid, status="contacting")
        reservation = repo.get_reservation(rid)
        greeting = await mgr.generate_greeting(reservation)

        assert greeting == "Hello clinic, this is a test greeting."
        assert provider.call_count == 1

        # Verify message was recorded
        messages = repo.get_messages(rid)
        assert len(messages) == 1
        assert messages[0]["direction"] == "outgoing"
        assert messages[0]["content"] == greeting

        # Verify status was updated
        updated = repo.get_reservation(rid)
        assert updated["status"] == "greeting_sent"

        repo.close()


class TestProcessClinicResponse:
    """Test clinic response processing."""

    async def test_confirmed_state(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)

        negotiation_response = json.dumps({
            "reply_text": "Thank you for confirming!",
            "extracted_info": {"confirmed": True, "available_dates": ["2026-04-01"]},
            "needs_human": False,
            "human_reason": None,
            "conversation_phase": "confirmed",
        })
        # Confirmation extraction response
        confirmation_response = json.dumps({
            "confirmed_date": "2026-04-01",
            "confirmed_time": "14:00",
            "procedure": "Botox",
            "price": "50000",
        })

        call_idx = 0

        class MultiResponseProvider:
            name = "mock"
            is_available = True

            async def generate(self, message, conversation_history, system_prompt):
                nonlocal call_idx
                call_idx += 1
                if call_idx == 1:
                    return LLMResponse(text=negotiation_response, provider="mock", model="m")
                return LLMResponse(text=confirmation_response, provider="mock", model="m")

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": MultiResponseProvider()},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="negotiating")
        result = await mgr.process_clinic_response(rid, "Yes, April 1 at 2pm is confirmed.")

        assert result.new_status == "confirmed"
        assert result.needs_human is False

        updated = repo.get_reservation(rid)
        assert updated["status"] == "confirmed"

        repo.close()

    async def test_declined_state(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)

        response = json.dumps({
            "reply_text": "We understand, thank you.",
            "extracted_info": {"declined": True, "decline_reason": "Fully booked"},
            "needs_human": False,
            "human_reason": None,
            "conversation_phase": "declined",
        })
        provider = MockProvider(response_text=response)

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="negotiating")
        result = await mgr.process_clinic_response(rid, "Sorry, fully booked.")

        assert result.new_status == "declined"
        updated = repo.get_reservation(rid)
        assert updated["status"] == "declined"

        repo.close()

    async def test_needs_human_escalation(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)

        response = json.dumps({
            "reply_text": None,
            "extracted_info": {},
            "needs_human": True,
            "human_reason": "payment",
            "conversation_phase": "negotiating",
        })
        provider = MockProvider(response_text=response)

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="negotiating")
        result = await mgr.process_clinic_response(rid, "Please pay deposit first.")

        assert result.needs_human is True
        assert result.human_reason == "payment"
        assert result.new_status == "paused_for_human"

        repo.close()

    async def test_max_turn_limit(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)
        provider = MockProvider()

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="negotiating")
        # Set turn_count to 15 (the max)
        repo.update_reservation(rid, turn_count=15)

        result = await mgr.process_clinic_response(rid, "Another message")

        assert result.needs_human is True
        assert result.human_reason == "max_turns_exceeded"
        assert result.new_status == "paused_for_human"

        repo.close()

    async def test_negotiating_continues(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)

        response = json.dumps({
            "reply_text": "Can we try next week?",
            "extracted_info": {"confirmed": False, "declined": False},
            "needs_human": False,
            "human_reason": None,
            "conversation_phase": "negotiating",
        })
        provider = MockProvider(response_text=response)

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": provider},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="negotiating")
        result = await mgr.process_clinic_response(rid, "Let me check the schedule.")

        assert result.new_status == "negotiating"
        assert result.reply_text == "Can we try next week?"

        repo.close()


class TestParseNegotiationResponse:
    """Test JSON parsing of LLM negotiation responses."""

    def _make_manager(self, tmp_path: Path) -> ConversationManager:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)
        return ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": MockProvider()},
            default_provider="mock",
        )

    def test_valid_json(self, tmp_path: Path) -> None:
        mgr = self._make_manager(tmp_path)
        data = {
            "reply_text": "Thanks",
            "extracted_info": {"confirmed": False},
            "needs_human": False,
            "human_reason": None,
            "conversation_phase": "negotiating",
        }
        result = mgr._parse_negotiation_response(json.dumps(data))
        assert result["reply_text"] == "Thanks"
        assert result["needs_human"] is False

    def test_markdown_fenced_json(self, tmp_path: Path) -> None:
        mgr = self._make_manager(tmp_path)
        fenced = '```json\n{"reply_text": "Hi", "needs_human": false}\n```'
        result = mgr._parse_negotiation_response(fenced)
        assert result["reply_text"] == "Hi"
        assert result["needs_human"] is False

    def test_invalid_json_returns_needs_human(self, tmp_path: Path) -> None:
        mgr = self._make_manager(tmp_path)
        result = mgr._parse_negotiation_response("This is not valid JSON at all")
        assert result["needs_human"] is True
        assert result["human_reason"] == "parse_failure"
        assert result["reply_text"] is None


class TestInjectStaffMessage:
    """Test staff message injection."""

    def test_records_message_and_updates_status(self, tmp_path: Path) -> None:
        repo = _make_repo(tmp_path)
        exporter = _make_exporter(tmp_path)

        mgr = ConversationManager(
            repo=repo,
            exporter=exporter,
            providers={"mock": MockProvider()},
            default_provider="mock",
        )

        rid = _make_reservation(repo, status="paused_for_human")
        mgr.inject_staff_message(rid, "Staff here, we can help.")

        messages = repo.get_messages(rid)
        staff_msgs = [m for m in messages if m["llm_provider"] == "staff"]
        assert len(staff_msgs) == 1
        assert staff_msgs[0]["content"] == "Staff here, we can help."
        assert staff_msgs[0]["direction"] == "outgoing"

        updated = repo.get_reservation(rid)
        assert updated["status"] == "negotiating"

        repo.close()
