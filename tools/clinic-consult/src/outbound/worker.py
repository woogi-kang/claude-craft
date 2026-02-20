"""Background worker that processes outbound reservations.

Periodically polls for active reservations and drives them through
the conversation state machine: open chat -> send greeting -> wait
for response -> negotiate -> confirm/decline.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from src.clinic.lookup import ClinicLookup
from src.clinic.models import ClinicInfo
from src.outbound.contact import ClinicContactor
from src.outbound.conversation import ConversationManager
from src.reservation.repository import ReservationRepository
from src.utils.logger import get_logger

logger = get_logger("worker")


class ReservationWorker:
    """Background loop that processes reservations through the state machine.

    Parameters
    ----------
    repo:
        Reservation persistence layer.
    conversation:
        LLM-driven conversation manager.
    contactor:
        Messenger deep-link opener (None for dry-run mode).
    clinic_lookup:
        Clinic database for resolving messenger channel URLs.
    poll_interval:
        Seconds between polling cycles.
    greeting_timeout_hours:
        Hours to wait for a clinic response before sending follow-up.
    max_followups:
        Maximum follow-up nudges before timing out.
    """

    def __init__(
        self,
        repo: ReservationRepository,
        conversation: ConversationManager,
        contactor: ClinicContactor | None,
        clinic_lookup: ClinicLookup,
        *,
        platform: str = "kakao",
        poll_interval: float = 30.0,
        greeting_timeout_hours: int = 2,
        max_followups: int = 2,
    ) -> None:
        self._repo = repo
        self._conversation = conversation
        self._contactor = contactor
        self._clinic_lookup = clinic_lookup
        self._platform = platform
        self._poll_interval = poll_interval
        self._greeting_timeout_hours = greeting_timeout_hours
        self._max_followups = max_followups
        self._running = False

    async def run(self) -> None:
        """Main worker loop. Runs until cancelled."""
        self._running = True
        logger.info("worker_started", poll_interval=self._poll_interval)

        while self._running:
            try:
                await self._process_cycle()
            except Exception as exc:
                logger.error("worker_cycle_error", error=str(exc))

            await asyncio.sleep(self._poll_interval)

        logger.info("worker_stopped")

    def stop(self) -> None:
        """Signal the worker to stop after the current cycle."""
        self._running = False

    async def _process_cycle(self) -> None:
        """One processing cycle: handle all active reservations."""
        active = self._repo.list_active()
        if not active:
            return

        logger.debug("processing_cycle", count=len(active))

        for reservation in active:
            try:
                await self._process_reservation(reservation)
            except Exception as exc:
                logger.error(
                    "reservation_processing_error",
                    reservation_id=reservation["id"],
                    error=str(exc),
                )
                self._repo.update_reservation(
                    reservation["id"],
                    status="failed",
                    error_message=f"Worker error: {str(exc)[:200]}",
                )

    async def _process_reservation(self, reservation: dict[str, Any]) -> None:
        """Route a single reservation based on its current status."""
        status = reservation["status"]
        rid = reservation["id"]

        if status == "created":
            await self._handle_created(reservation)
        elif status == "contacting":
            await self._handle_contacting(reservation)
        elif status == "greeting_sent":
            await self._handle_greeting_sent(reservation)
        elif status == "negotiating":
            await self._handle_negotiating(reservation)
        else:
            logger.debug("skipping_status", reservation_id=rid, status=status)

    # ------------------------------------------------------------------
    # Status handlers
    # ------------------------------------------------------------------

    async def _handle_created(self, reservation: dict[str, Any]) -> None:
        """Transition CREATED -> CONTACTING: resolve clinic and open chat."""
        rid = reservation["id"]
        platform = reservation.get("contact_platform") or self._platform
        contact_url = reservation.get("clinic_contact_url")

        if not contact_url:
            # Try to resolve from clinic lookup
            clinic_id = reservation.get("clinic_id")
            if clinic_id:
                clinic = self._clinic_lookup.find_by_id(clinic_id)
                if clinic:
                    contact_url = clinic.get_contact_url(platform)
                    if contact_url:
                        self._repo.update_reservation(
                            rid,
                            clinic_contact_url=contact_url,
                            contact_platform=platform,
                        )

        if not contact_url:
            logger.warning(
                "no_contact_url", reservation_id=rid, platform=platform,
            )
            self._repo.update_reservation(
                rid,
                status="failed",
                error_message=f"No {platform} channel URL available",
            )
            return

        self._repo.update_reservation(rid, status="contacting")
        logger.info("reservation_contacting", reservation_id=rid, platform=platform)

    async def _handle_contacting(self, reservation: dict[str, Any]) -> None:
        """Transition CONTACTING -> GREETING_SENT: open chat and send greeting."""
        rid = reservation["id"]

        # Open messenger chat (skip in dry-run mode)
        if self._contactor:
            clinic = self._resolve_clinic(reservation)
            if not clinic:
                self._repo.update_reservation(
                    rid,
                    status="failed",
                    error_message="Could not resolve clinic info",
                )
                return

            opened = await self._contactor.open_clinic_chat(clinic)
            if not opened:
                self._repo.update_reservation(
                    rid,
                    status="failed",
                    error_message=f"Failed to open {self._platform} chat",
                )
                return

        # Generate and record greeting
        greeting = await self._conversation.generate_greeting(reservation)
        logger.info(
            "greeting_sent",
            reservation_id=rid,
            greeting_len=len(greeting),
        )

    async def _handle_greeting_sent(self, reservation: dict[str, Any]) -> None:
        """Check for clinic response after greeting. Send follow-up if timed out."""
        rid = reservation["id"]
        contacted_at = reservation.get("contacted_at")

        if not contacted_at:
            return

        hours_elapsed = self._hours_since(contacted_at)

        # Check if there's a new incoming message (would be detected externally)
        last_incoming = self._repo.get_last_incoming(rid)
        if last_incoming:
            # There's a clinic response - process it
            result = await self._conversation.process_clinic_response(
                rid, last_incoming["content"],
            )
            logger.info(
                "clinic_response_processed",
                reservation_id=rid,
                new_status=result.new_status,
            )
            return

        # No response yet - check timeout
        followup_count = (reservation.get("turn_count", 1)) - 1
        if hours_elapsed >= self._greeting_timeout_hours:
            if followup_count < self._max_followups:
                followup = await self._conversation.generate_followup(reservation)
                logger.info("followup_sent", reservation_id=rid, attempt=followup_count + 1)
            else:
                self._repo.update_reservation(
                    rid,
                    status="timed_out",
                    error_message="No response after follow-ups",
                )
                logger.info("reservation_timed_out", reservation_id=rid)

    async def _handle_negotiating(self, reservation: dict[str, Any]) -> None:
        """Process new incoming messages during negotiation."""
        rid = reservation["id"]

        last_incoming = self._repo.get_last_incoming(rid)
        if not last_incoming:
            return

        # Check if we already replied to this message
        messages = self._repo.get_messages(rid)
        if messages and messages[-1]["direction"] == "outgoing":
            # Already replied, waiting for next clinic response
            return

        result = await self._conversation.process_clinic_response(
            rid, last_incoming["content"],
        )
        logger.info(
            "negotiation_turn",
            reservation_id=rid,
            new_status=result.new_status,
            needs_human=result.needs_human,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _resolve_clinic(self, reservation: dict[str, Any]) -> ClinicInfo | None:
        """Resolve a ClinicInfo for the reservation."""
        clinic_id = reservation.get("clinic_id")
        if clinic_id:
            return self._clinic_lookup.find_by_id(clinic_id)

        clinics = self._clinic_lookup.find_by_name(reservation["clinic_name"])
        return clinics[0] if clinics else None

    @staticmethod
    def _hours_since(iso_timestamp: str) -> float:
        """Calculate hours elapsed since an ISO timestamp."""
        try:
            dt = datetime.fromisoformat(iso_timestamp)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            delta = datetime.now(timezone.utc) - dt
            return delta.total_seconds() / 3600.0
        except (ValueError, TypeError):
            return 0.0
