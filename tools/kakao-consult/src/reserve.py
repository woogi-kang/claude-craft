"""Entry point for the reservation system.

Starts the FastAPI web server and optionally runs the background
reservation worker that processes outbound conversations.

Usage:
    # Start web dashboard only
    python -m src.reserve

    # Start with background worker
    python -m src.reserve --worker

    # Process a single reservation (dry-run)
    python -m src.reserve --process REQ-20260220-001 --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import signal
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    parser = argparse.ArgumentParser(description="Kakao Reservation Bot")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Web server host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Web server port (default: 8000)"
    )
    parser.add_argument(
        "--worker", action="store_true", help="Run background reservation worker"
    )
    parser.add_argument(
        "--process", type=str, help="Process a specific reservation by request_id"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Skip actual KakaoTalk interaction"
    )
    args = parser.parse_args()

    if args.process:
        asyncio.run(_process_single(args.process, dry_run=args.dry_run))
        return

    if args.worker:
        asyncio.run(_run_worker_standalone(dry_run=args.dry_run))
        return

    _start_server(args.host, args.port)


def _start_server(host: str, port: int) -> None:
    """Start the FastAPI web server."""
    import uvicorn

    from src.web.app import create_app

    create_app()

    print(f"Starting reservation dashboard at http://{host}:{port}")
    print("Press Ctrl+C to stop")

    uvicorn.run(
        "src.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


def _build_worker(*, dry_run: bool = False):
    """Build a ReservationWorker with all dependencies wired up."""
    from src.ai.providers.base import LLMProvider
    from src.clinic.lookup import ClinicLookup
    from src.config import load_settings
    from src.outbound.conversation import ConversationManager
    from src.outbound.worker import ReservationWorker
    from src.reservation.exporter import ReservationExporter
    from src.reservation.repository import ReservationRepository

    settings = load_settings()

    db_path = PROJECT_ROOT / settings.database.path
    repo = ReservationRepository(db_path)
    repo.init_db()

    exports = PROJECT_ROOT / settings.reservation.export_dir
    exporter = ReservationExporter(exports)

    hospitals_db = PROJECT_ROOT / settings.reservation.hospitals_db
    clinic_lookup = ClinicLookup(hospitals_db)

    # Build LLM providers (import lazily to avoid missing API keys)
    providers: dict[str, LLMProvider] = {}
    try:
        from src.ai.providers.claude_provider import ClaudeProvider

        providers["claude"] = ClaudeProvider(
            api_key=settings.anthropic_api_key,
            model=settings.llm.claude_model,
            max_tokens=settings.llm.max_tokens,
        )
    except Exception:
        pass
    try:
        from src.ai.providers.openai_provider import OpenAIProvider

        providers["openai"] = OpenAIProvider(
            api_key=settings.openai_api_key,
            model=settings.llm.openai_model,
            max_tokens=settings.llm.max_tokens,
        )
    except Exception:
        pass

    conversation = ConversationManager(
        repo=repo,
        exporter=exporter,
        providers=providers,
        default_provider=settings.llm.default_provider,
        agency_name=settings.reservation.agency_name,
    )

    # In dry-run mode, contactor is None (no KakaoTalk interaction)
    contactor = None
    if not dry_run:
        try:
            import uiautomator2 as u2

            from src.kakao.navigator import KakaoNavigator
            from src.outbound.contact import ClinicContactor

            device = u2.connect(settings.emulator.serial)
            navigator = KakaoNavigator(device)
            contactor = ClinicContactor(
                device=device,
                navigator=navigator,
                serial=settings.emulator.serial,
            )
        except Exception as exc:
            print(f"Warning: Could not connect to emulator: {exc}")
            print("Running in dry-run mode (no KakaoTalk interaction)")

    worker = ReservationWorker(
        repo=repo,
        conversation=conversation,
        contactor=contactor,
        clinic_lookup=clinic_lookup,
        poll_interval=30.0,
        greeting_timeout_hours=settings.reservation.greeting_timeout_hours,
    )

    return worker


async def _run_worker_standalone(*, dry_run: bool = False) -> None:
    """Run the background worker as a standalone process."""
    worker = _build_worker(dry_run=dry_run)

    # Graceful shutdown on SIGINT/SIGTERM
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, worker.stop)

    mode = "DRY-RUN" if dry_run else "LIVE"
    print(f"Starting reservation worker [{mode}]...")
    print("Press Ctrl+C to stop")

    await worker.run()


async def _process_single(request_id: str, *, dry_run: bool = False) -> None:
    """Process a single reservation request."""
    from src.reservation.repository import ReservationRepository

    db_path = PROJECT_ROOT / "data" / "consult.db"
    repo = ReservationRepository(db_path)
    repo.init_db()

    reservation = repo.get_by_request_id(request_id)
    if not reservation:
        print(f"Reservation {request_id} not found")
        sys.exit(1)

    print(f"Reservation: {reservation['clinic_name']} / {reservation['procedure_name']}")
    print(f"Status: {reservation['status']}")
    print(f"Patient: {reservation['patient_name']} ({reservation['patient_nationality']})")

    if dry_run:
        print("[DRY RUN] Would contact clinic via KakaoTalk")
        print(f"  KakaoTalk URL: {reservation.get('clinic_kakao_url', 'N/A')}")
        return

    worker = _build_worker(dry_run=False)
    await worker._process_reservation(reservation)
    print("Processing complete.")


if __name__ == "__main__":
    main()
