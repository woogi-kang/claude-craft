"""Tests for outbound LLM prompt templates."""

from __future__ import annotations

from src.outbound.prompts import (
    AGENCY_IDENTITY,
    CONFIRMATION_PROMPT,
    DEFAULT_AGENCY_NAME,
    FOLLOWUP_PROMPT,
    GREETING_PROMPT,
    NEGOTIATION_PROMPT,
)


class TestAgencyIdentity:
    """Test agency identity template."""

    def test_format_with_agency_name(self) -> None:
        result = AGENCY_IDENTITY.format(agency_name="Test Agency")
        assert "Test Agency" in result

    def test_default_agency_name_is_set(self) -> None:
        assert DEFAULT_AGENCY_NAME
        assert isinstance(DEFAULT_AGENCY_NAME, str)
        assert len(DEFAULT_AGENCY_NAME) > 0


class TestGreetingPrompt:
    """Test greeting prompt template."""

    def test_format_with_all_variables(self) -> None:
        result = GREETING_PROMPT.format(
            agency_identity="We are Test Agency",
            clinic_name="Seoul Skin",
            procedure="Botox",
            preferred_dates="2026-03-01, 2026-03-02",
            preferred_time="morning",
            nationality="JP",
            notes="VIP patient",
        )
        assert "Seoul Skin" in result
        assert "Botox" in result
        assert "2026-03-01" in result
        assert "morning" in result
        assert "JP" in result
        assert "VIP patient" in result
        assert "Test Agency" in result

    def test_format_with_empty_notes(self) -> None:
        result = GREETING_PROMPT.format(
            agency_identity="Agency",
            clinic_name="Clinic",
            procedure="Laser",
            preferred_dates="any",
            preferred_time="any",
            nationality="JP",
            notes="",
        )
        assert "Clinic" in result
        assert "Laser" in result


class TestNegotiationPrompt:
    """Test negotiation prompt template."""

    def test_format_with_all_variables(self) -> None:
        result = NEGOTIATION_PROMPT.format(
            agency_identity="We are Test Agency",
            clinic_name="Gangnam Derm",
            procedure="Filler",
            preferred_dates="2026-04-01",
            preferred_time="afternoon",
            nationality="CN",
            notes="First visit",
            conversation_history="[us] Hello\n[clinic] Hi",
            latest_message="We have availability on April 1st",
        )
        assert "Gangnam Derm" in result
        assert "Filler" in result
        assert "2026-04-01" in result
        assert "afternoon" in result
        assert "CN" in result
        assert "First visit" in result
        assert "[us] Hello" in result
        assert "We have availability on April 1st" in result


class TestFollowupPrompt:
    """Test follow-up prompt template."""

    def test_format_with_all_variables(self) -> None:
        result = FOLLOWUP_PROMPT.format(
            agency_identity="We are Test Agency",
            clinic_name="Myeongdong Clinic",
            procedure="Botox",
            preferred_dates="2026-05-10",
        )
        assert "Myeongdong Clinic" in result
        assert "Botox" in result
        assert "2026-05-10" in result
        assert "Test Agency" in result


class TestConfirmationPrompt:
    """Test confirmation extraction prompt."""

    def test_format_with_history(self) -> None:
        result = CONFIRMATION_PROMPT.format(
            conversation_history="[us] Is April 1 ok?\n[clinic] Yes, 2pm confirmed."
        )
        assert "April 1" in result
        assert "2pm confirmed" in result
        # Should contain JSON template markers
        assert "confirmed_date" in result
        assert "confirmed_time" in result
