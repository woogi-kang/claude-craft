"""Daemon entry point using the shared DaemonLoop.

Keeps a single persistent browser session alive and runs the pipeline
at variable 1-2 hour intervals. The browser is only opened once at
startup and closed on shutdown.
"""

from __future__ import annotations

from datetime import timedelta, timezone

from outreach_shared.daemon.loop import DaemonLoop
from outreach_shared.utils.logger import get_logger
from playwright.async_api import async_playwright

from src.browser.session import SessionManager
from src.config import Settings, load_settings
from src.pipeline.halt import HaltManager, get_volume_multiplier

logger = get_logger("daemon")

# Japan Standard Time (UTC+9)
_JST = timezone(timedelta(hours=9))


def create_daemon(
    settings: Settings,
    run_cycle: object,
    halt_manager: HaltManager | None = None,
) -> DaemonLoop:
    """Build a DaemonLoop wired to the pipeline runner.

    Parameters
    ----------
    settings:
        Application settings with daemon configuration.
    run_cycle:
        Async callable that executes one pipeline cycle.
    halt_manager:
        Emergency halt manager.

    Returns
    -------
    DaemonLoop
        Configured daemon loop ready to start.
    """
    halt_mgr = halt_manager or HaltManager()
    cfg = settings.daemon

    async def _guarded_cycle() -> None:
        """Run one pipeline cycle with halt and conservation checks."""
        if halt_mgr.is_halted():
            halt_info = halt_mgr.get_halt_info()
            reason = halt_info.get("reason", "unknown") if halt_info else "unknown"
            logger.warning("pipeline_skipped_halted", reason=reason)
            return

        multiplier = get_volume_multiplier(halt_mgr)
        if multiplier < 1.0:
            logger.info("conservation_mode_active", multiplier=multiplier)

        logger.info("pipeline_run_starting")
        await run_cycle()

    return DaemonLoop(
        run_cycle=_guarded_cycle,
        min_interval_hours=cfg.min_interval_hours,
        max_interval_hours=cfg.max_interval_hours,
        active_hours=(cfg.active_start_hour, cfg.active_end_hour),
        tz=_JST,
    )


async def run_daemon(settings: Settings | None = None) -> None:
    """Start the daemon with a persistent browser session.

    Opens one browser at startup and keeps it alive across all cycles.
    The browser is only closed on SIGTERM/SIGINT shutdown.

    Parameters
    ----------
    settings:
        Application settings. Loaded from config if not provided.
    """
    if settings is None:
        settings = load_settings()

    from outreach_shared.utils.logger import setup_logging

    setup_logging(level=settings.logging.level, log_dir=settings.logging.log_dir)

    from src.db.repository import Repository
    from src.knowledge.treatments import TreatmentKnowledgeBase
    from src.main import PipelineRunner

    db_url = settings.database_url or settings.database.url
    repo = Repository(db_url)
    repo.init_db()

    kb = TreatmentKnowledgeBase()
    kb.load()

    runner = PipelineRunner(settings, repo, kb)

    # Single persistent browser for the entire daemon lifetime
    async with async_playwright() as pw:
        session_mgr = SessionManager(
            pw,
            headless=settings.browser.headless,
            viewport_width=settings.browser.viewport_width,
            viewport_height=settings.browser.viewport_height,
        )
        context = await session_mgr.get_session("nandemo")
        logger.info("persistent_browser_started")

        halt_mgr = HaltManager()

        async def _cycle() -> None:
            result = await runner.run_once(context=context)
            if result.success:
                logger.info(
                    "pipeline_run_complete",
                    searched=result.search_count,
                    collected=result.collect.stored if result.collect else 0,
                    analyzed=(result.analyze.total_processed if result.analyze else 0),
                    follows=result.nurture.follows_sent if result.nurture else 0,
                    likes=result.nurture.likes_sent if result.nurture else 0,
                    replied=result.reply.replies_sent if result.reply else 0,
                    dms_sent=result.dm.dms_sent if result.dm else 0,
                    posted=result.posting.posts_published if result.posting else 0,
                )
            else:
                logger.error("pipeline_run_failed", error=result.error)

            # Persist emergency halt so the daemon stops on the next cycle
            _check_emergency_halt(result, halt_mgr)
        daemon = create_daemon(settings, _cycle, halt_mgr)

        logger.info("daemon_starting")
        try:
            await daemon.run()
        finally:
            await session_mgr.close_all()
            logger.info("persistent_browser_closed")


def _check_emergency_halt(
    result: object,
    halt_mgr: HaltManager,
) -> None:
    """Inspect pipeline result for emergency halt flags and persist halt state.

    Checks reply, DM, nurture, and posting result objects for
    ``emergency_halt=True`` and triggers HaltManager so the daemon
    skips subsequent cycles until manually resumed.
    """
    halt_sources: list[tuple[str, str]] = []

    if getattr(result, "reply", None) and getattr(result.reply, "emergency_halt", False):
        halt_sources.append(("Reply rate limit detected", "reply_pipeline"))
    if getattr(result, "dm", None) and getattr(result.dm, "emergency_halt", False):
        halt_sources.append(("DM rate limit detected", "dm_pipeline"))
    if getattr(result, "nurture", None) and getattr(result.nurture, "emergency_halt", False):
        halt_sources.append(("Nurture rate limit detected", "nurture_pipeline"))
    if getattr(result, "posting", None) and getattr(result.posting, "emergency_halt", False):
        halt_sources.append(("Posting rate limit detected", "posting_pipeline"))

    if halt_sources:
        reason = "; ".join(r for r, _ in halt_sources)
        source = ", ".join(s for _, s in halt_sources)
        halt_mgr.trigger_halt(reason, source=source)
