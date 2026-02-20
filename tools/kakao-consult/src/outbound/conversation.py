"""Conversation state machine for outbound reservation dialogs.

Manages the multi-turn conversation lifecycle with clinic staff,
using LLM to interpret responses and generate follow-up messages.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.ai.providers.base import LLMProvider, LLMResponse, call_llm_with_fallback
from src.outbound.prompts import (
    AGENCY_IDENTITY,
    CONFIRMATION_PROMPT,
    DEFAULT_AGENCY_NAME,
    FOLLOWUP_PROMPT,
    GREETING_PROMPT,
    NEGOTIATION_PROMPT,
)
from src.reservation.exporter import ReservationExporter
from src.reservation.repository import ReservationRepository
from src.utils.logger import get_logger
from src.utils.time_utils import utc_now_iso

logger = get_logger("conversation")

# Maximum conversation turns before forcing escalation
_MAX_TURNS = 15


@dataclass
class TurnResult:
    """Result of processing a single conversation turn."""

    reply_text: str | None = None
    new_status: str | None = None
    extracted_info: dict[str, Any] | None = None
    needs_human: bool = False
    human_reason: str | None = None


class ConversationManager:
    """Drives reservation conversations through the state machine.

    Parameters
    ----------
    repo:
        Reservation repository for persistence.
    exporter:
        CSV exporter for terminal states.
    providers:
        Dict of LLM provider name -> instance.
    default_provider:
        Which LLM to try first.
    """

    def __init__(
        self,
        repo: ReservationRepository,
        exporter: ReservationExporter,
        providers: dict[str, LLMProvider],
        default_provider: str = "claude",
        agency_name: str = DEFAULT_AGENCY_NAME,
    ) -> None:
        self._repo = repo
        self._exporter = exporter
        self._providers = providers
        self._default = default_provider
        self._fallback_order = ["claude", "openai", "ollama"]
        self._agency_identity = AGENCY_IDENTITY.format(agency_name=agency_name)

    # ------------------------------------------------------------------
    # Generate initial greeting
    # ------------------------------------------------------------------

    async def generate_greeting(self, reservation: dict[str, Any]) -> str:
        """Generate the initial inquiry message for a clinic."""
        preferred_dates = reservation.get("preferred_dates") or "[]"
        if isinstance(preferred_dates, str):
            try:
                preferred_dates = ", ".join(json.loads(preferred_dates))
            except json.JSONDecodeError:
                pass

        prompt = GREETING_PROMPT.format(
            agency_identity=self._agency_identity,
            clinic_name=reservation["clinic_name"],
            procedure=reservation["procedure_name"],
            preferred_dates=preferred_dates,
            preferred_time=reservation.get("preferred_time", "any"),
            nationality=reservation.get("patient_nationality", "JP"),
            notes=reservation.get("notes", ""),
        )

        response = await self._call_llm(prompt)
        greeting = response.text.strip()

        # Record the outgoing message
        self._repo.add_message(
            reservation_id=reservation["id"],
            direction="outgoing",
            content=greeting,
            llm_provider=response.provider,
            phase="greeting_sent",
        )

        # Update reservation status
        self._repo.update_reservation(
            reservation["id"],
            status="greeting_sent",
            contacted_at=utc_now_iso(),
            turn_count=1,
        )

        logger.info(
            "greeting_generated",
            reservation_id=reservation["id"],
            clinic=reservation["clinic_name"],
        )
        return greeting

    # ------------------------------------------------------------------
    # Process a clinic response (one conversation turn)
    # ------------------------------------------------------------------

    async def process_clinic_response(
        self,
        reservation_id: int,
        clinic_message: str,
    ) -> TurnResult:
        """Process a clinic's response and decide next action.

        Parameters
        ----------
        reservation_id:
            The reservation being negotiated.
        clinic_message:
            The clinic's latest message text.

        Returns
        -------
        TurnResult
            What to do next: reply, pause, or finalize.
        """
        reservation = self._repo.get_reservation(reservation_id)
        if not reservation:
            logger.error("reservation_not_found", id=reservation_id)
            return TurnResult(new_status="failed")

        # Record the incoming message
        self._repo.add_message(
            reservation_id=reservation_id,
            direction="incoming",
            content=clinic_message,
            phase=reservation["status"],
        )

        # Check turn limit
        turn_count = reservation.get("turn_count", 0) + 1
        if turn_count > _MAX_TURNS:
            logger.warning("max_turns_reached", reservation_id=reservation_id)
            self._repo.update_reservation(
                reservation_id,
                status="paused_for_human",
                paused_reason="max_turns_exceeded",
                turn_count=turn_count,
            )
            return TurnResult(
                needs_human=True,
                human_reason="max_turns_exceeded",
                new_status="paused_for_human",
            )

        # Build conversation history for LLM context
        messages = self._repo.get_messages(reservation_id)
        history_text = self._format_history(messages)

        preferred_dates = reservation.get("preferred_dates") or "[]"
        if isinstance(preferred_dates, str):
            try:
                preferred_dates = ", ".join(json.loads(preferred_dates))
            except json.JSONDecodeError:
                pass

        # Call LLM to interpret and respond
        prompt = NEGOTIATION_PROMPT.format(
            agency_identity=self._agency_identity,
            clinic_name=reservation["clinic_name"],
            procedure=reservation["procedure_name"],
            preferred_dates=preferred_dates,
            preferred_time=reservation.get("preferred_time", "any"),
            nationality=reservation.get("patient_nationality", "JP"),
            notes=reservation.get("notes", ""),
            conversation_history=history_text,
            latest_message=clinic_message,
        )

        response = await self._call_llm(prompt)
        parsed = self._parse_negotiation_response(response.text)

        # Handle parsed result
        result = TurnResult(
            reply_text=parsed.get("reply_text"),
            extracted_info=parsed.get("extracted_info"),
            needs_human=parsed.get("needs_human", False),
            human_reason=parsed.get("human_reason"),
        )

        # Record outgoing reply (if we have one and not pausing)
        if result.reply_text and not result.needs_human:
            self._repo.add_message(
                reservation_id=reservation_id,
                direction="outgoing",
                content=result.reply_text,
                llm_provider=response.provider,
                extracted_json=json.dumps(parsed.get("extracted_info"), ensure_ascii=False),
                phase=parsed.get("conversation_phase", "negotiating"),
            )

        # State transitions
        phase = parsed.get("conversation_phase", "negotiating")
        extracted = parsed.get("extracted_info", {})

        if result.needs_human:
            result.new_status = "paused_for_human"
            self._repo.update_reservation(
                reservation_id,
                status="paused_for_human",
                paused_reason=result.human_reason,
                turn_count=turn_count,
            )
        elif extracted.get("confirmed"):
            result.new_status = "confirmed"
            confirm_details = await self._extract_confirmation(reservation_id)
            self._repo.update_reservation(
                reservation_id,
                status="confirmed",
                confirmed_at=utc_now_iso(),
                turn_count=turn_count,
                **confirm_details,
            )
            self._export_if_terminal("confirmed", reservation_id)
        elif extracted.get("declined"):
            result.new_status = "declined"
            self._repo.update_reservation(
                reservation_id,
                status="declined",
                decline_reason=extracted.get("decline_reason", ""),
                completed_at=utc_now_iso(),
                turn_count=turn_count,
            )
            self._export_if_terminal("declined", reservation_id)
        else:
            result.new_status = "negotiating"
            self._repo.update_reservation(
                reservation_id,
                status="negotiating",
                turn_count=turn_count,
            )

        logger.info(
            "turn_processed",
            reservation_id=reservation_id,
            new_status=result.new_status,
            turn=turn_count,
        )
        return result

    # ------------------------------------------------------------------
    # Generate follow-up nudge
    # ------------------------------------------------------------------

    async def generate_followup(self, reservation: dict[str, Any]) -> str:
        """Generate a polite follow-up message for an unresponsive clinic."""
        preferred_dates = reservation.get("preferred_dates") or "[]"
        if isinstance(preferred_dates, str):
            try:
                preferred_dates = ", ".join(json.loads(preferred_dates))
            except json.JSONDecodeError:
                pass

        prompt = FOLLOWUP_PROMPT.format(
            agency_identity=self._agency_identity,
            clinic_name=reservation["clinic_name"],
            procedure=reservation["procedure_name"],
            preferred_dates=preferred_dates,
        )
        response = await self._call_llm(prompt)
        followup = response.text.strip()

        self._repo.add_message(
            reservation_id=reservation["id"],
            direction="outgoing",
            content=followup,
            llm_provider=response.provider,
            phase="followup",
        )

        turn_count = reservation.get("turn_count", 0) + 1
        self._repo.update_reservation(reservation["id"], turn_count=turn_count)

        return followup

    # ------------------------------------------------------------------
    # Staff resume (manual message injection)
    # ------------------------------------------------------------------

    def inject_staff_message(self, reservation_id: int, message: str) -> None:
        """Record a message manually composed by staff."""
        self._repo.add_message(
            reservation_id=reservation_id,
            direction="outgoing",
            content=message,
            llm_provider="staff",
            phase="negotiating",
        )
        self._repo.update_reservation(
            reservation_id,
            status="negotiating",
            paused_reason=None,
        )
        logger.info("staff_message_injected", reservation_id=reservation_id)

    def mark_completed(self, reservation_id: int) -> None:
        """Mark a confirmed reservation as completed."""
        self._repo.update_reservation(
            reservation_id,
            status="completed",
            completed_at=utc_now_iso(),
        )
        self._export_if_terminal("completed", reservation_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _call_llm(self, prompt: str) -> LLMResponse:
        """Call LLM with fallback chain."""
        return await call_llm_with_fallback(
            providers=self._providers,
            message=prompt,
            system_prompt="You are a professional Korean-language reservation coordinator.",
            default_provider=self._default,
            fallback_order=self._fallback_order,
        )

    async def _extract_confirmation(self, reservation_id: int) -> dict[str, Any]:
        """Extract confirmed booking details via LLM."""
        messages = self._repo.get_messages(reservation_id)
        history_text = self._format_history(messages)

        prompt = CONFIRMATION_PROMPT.format(conversation_history=history_text)
        response = await self._call_llm(prompt)

        try:
            data = json.loads(response.text)
            return {
                k: v
                for k, v in {
                    "confirmed_date": data.get("confirmed_date"),
                    "confirmed_time": data.get("confirmed_time"),
                    "confirmed_price": data.get("price"),
                    "confirmed_doctor": data.get("doctor_name"),
                    "clinic_instructions": data.get("clinic_instructions"),
                }.items()
                if v is not None
            }
        except (json.JSONDecodeError, AttributeError):
            logger.warning("confirmation_parse_failed", raw=response.text[:200])
            return {}

    def _format_history(self, messages: list[dict[str, Any]]) -> str:
        """Format message history for LLM context."""
        lines: list[str] = []
        for msg in messages:
            role = "우리" if msg["direction"] == "outgoing" else "병원"
            lines.append(f"[{role}] {msg['content']}")
        return "\n".join(lines)

    def _parse_negotiation_response(self, raw: str) -> dict[str, Any]:
        """Parse structured JSON from LLM negotiation response."""
        # Strip markdown code fences if present
        text = raw.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("negotiation_parse_failed", raw=raw[:300])
            return {
                "reply_text": None,
                "extracted_info": {},
                "needs_human": True,
                "human_reason": "parse_failure",
                "conversation_phase": "negotiating",
            }

    def _export_if_terminal(self, status: str, reservation_id: int) -> None:
        """Export to CSV if status is terminal."""
        if self._exporter.should_export(status):
            reservation = self._repo.get_reservation(reservation_id)
            if reservation:
                self._exporter.export_reservation(reservation)
