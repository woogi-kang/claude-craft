"""Pipeline orchestrator -- wire all stages together.

Provides ``PipelineRunner`` which executes the full
Search -> Collect -> Analyze -> Reply -> DM cycle, and a CLI entry
point with subcommands: run, daemon, status, setup, halt.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import dataclass

from outreach_shared.utils.logger import get_logger, setup_logging
from playwright.async_api import async_playwright

from src.ai.classifier import TweetClassifier
from src.ai.content_gen import ContentGenerator
from src.browser.session import SessionManager
from src.config import Settings, load_settings
from src.db.repository import Repository
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.analyze import AnalyzePipeline, AnalyzeResult
from src.pipeline.collect import CollectPipeline, CollectResult
from src.pipeline.dm import DmPipeline, DmResult
from src.pipeline.reply import ReplyPipeline, ReplyResult
from src.pipeline.search import SearchPipeline
from src.pipeline.track import ActionTracker
from src.platform.login import check_session_health, login

logger = get_logger("main")


@dataclass
class PipelineRunResult:
    """Aggregated result from a full pipeline run."""

    search_count: int = 0
    collect: CollectResult | None = None
    analyze: AnalyzeResult | None = None
    reply: ReplyResult | None = None
    dm: DmResult | None = None
    success: bool = False
    error: str | None = None


class PipelineRunner:
    """Orchestrate the Search -> Collect -> Analyze -> Reply -> DM pipeline.

    Parameters
    ----------
    settings:
        Application settings.
    repository:
        Database repository.
    knowledge_base:
        Treatment knowledge base (pre-loaded).
    """

    def __init__(
        self,
        settings: Settings,
        repository: Repository,
        knowledge_base: TreatmentKnowledgeBase,
    ) -> None:
        self._settings = settings
        self._repo = repository
        self._kb = knowledge_base
        self._tracker = ActionTracker(repository)

    async def run_once(self, *, dry_run: bool = False) -> PipelineRunResult:
        """Execute a single Search -> Collect -> Analyze cycle.

        Parameters
        ----------
        dry_run:
            When ``True``, skip browser-based search and use any
            already-collected tweets for analysis only.

        Returns
        -------
        PipelineRunResult
            Aggregated statistics from all pipeline stages.
        """
        result = PipelineRunResult()

        try:
            # --- Search & Collect ---
            if not dry_run:
                search_pipeline = SearchPipeline(
                    min_delay=self._settings.delays.search_min_seconds,
                    max_delay=self._settings.delays.search_max_seconds,
                )
                collect_pipeline = CollectPipeline(
                    max_follower_count=self._settings.collect.max_follower_count,
                    require_profile_pic=self._settings.collect.require_profile_pic,
                    require_bio=self._settings.collect.require_bio,
                    max_tweet_age_hours=self._settings.search.max_post_age_hours,
                )

                async with async_playwright() as pw:
                    session_mgr = SessionManager(
                        pw,
                        headless=self._settings.browser.headless,
                        viewport_width=self._settings.browser.viewport_width,
                        viewport_height=self._settings.browser.viewport_height,
                    )

                    try:
                        context = await session_mgr.get_session("burner")

                        # Check session health and login if needed
                        healthy = await check_session_health(context)
                        if not healthy:
                            logger.info("session_expired_relogin")
                            logged_in = await login(
                                context,
                                self._settings.burner_x_username,
                                self._settings.burner_x_password,
                            )
                            if not logged_in:
                                result.error = "Failed to login to burner account"
                                self._tracker.record_error("login", result.error)
                                return result

                        # Search
                        raw_tweets = await search_pipeline.run(
                            self._settings.search.keywords,
                            context,
                        )
                        result.search_count = len(raw_tweets)

                        for kw in self._settings.search.keywords:
                            kw_tweets = [t for t in raw_tweets if t.search_keyword == kw]
                            self._tracker.record_search(kw, len(kw_tweets))

                        # Collect
                        collect_result = collect_pipeline.run(raw_tweets, self._repo)
                        result.collect = collect_result
                        self._tracker.record_collect(
                            collect_result.stored,
                            collect_result.total_input - collect_result.stored,
                        )

                    finally:
                        await session_mgr.close_all()

            else:
                logger.info("dry_run_skip_search")

            # --- Analyze ---
            classifier = TweetClassifier(
                api_key=self._settings.gemini_api_key,
                model=self._settings.llm.model,
                confidence_threshold=self._settings.classification.confidence_threshold,
                domain_context=self._kb.get_classification_context(),
            )
            analyze_pipeline = AnalyzePipeline(classifier)
            analyze_result = await analyze_pipeline.run(self._repo)
            result.analyze = analyze_result

            # --- Reply (if enabled) ---
            if self._settings.reply.enabled:
                content_gen = ContentGenerator(
                    api_key=self._settings.gemini_api_key,
                    model=self._settings.llm.model,
                    provider=self._settings.llm.provider,
                )

                async with async_playwright() as pw_reply:
                    session_mgr = SessionManager(
                        pw_reply,
                        headless=self._settings.browser.headless,
                        viewport_width=self._settings.browser.viewport_width,
                        viewport_height=self._settings.browser.viewport_height,
                    )
                    try:
                        context = await session_mgr.get_session("nandemo")
                        healthy = await check_session_health(context)
                        if not healthy:
                            logged_in = await login(
                                context,
                                self._settings.nandemo_x_username,
                                self._settings.nandemo_x_password,
                            )
                            if not logged_in:
                                result.error = "Failed to login for reply"
                                self._tracker.record_error("login", result.error)
                                return result

                        reply_pipeline = ReplyPipeline(
                            content_gen=content_gen,
                            knowledge_base=self._kb,
                        )
                        reply_result = await reply_pipeline.run(
                            repository=self._repo,
                            context=context,
                            tracker=self._tracker,
                            settings=self._settings,
                        )
                        result.reply = reply_result
                        logger.info(
                            "reply_stage_done",
                            sent=reply_result.replies_sent,
                            errors=reply_result.errors,
                        )
                    finally:
                        await session_mgr.close_all()

            # --- DM (if enabled) ---
            if self._settings.dm.enabled:
                if not self._settings.reply.enabled:
                    content_gen = ContentGenerator(
                        api_key=self._settings.gemini_api_key,
                        model=self._settings.llm.model,
                        provider=self._settings.llm.provider,
                    )

                async with async_playwright() as pw_dm:
                    dm_session_mgr = SessionManager(
                        pw_dm,
                        headless=self._settings.browser.headless,
                        viewport_width=self._settings.browser.viewport_width,
                        viewport_height=self._settings.browser.viewport_height,
                    )
                    try:
                        context = await dm_session_mgr.get_session("nandemo")
                        healthy = await check_session_health(context)
                        if not healthy:
                            logged_in = await login(
                                context,
                                self._settings.nandemo_x_username,
                                self._settings.nandemo_x_password,
                            )
                            if not logged_in:
                                result.error = "Failed to login for DM"
                                self._tracker.record_error("login", result.error)
                                return result

                        dm_pipeline = DmPipeline(
                            content_gen=content_gen,
                            knowledge_base=self._kb,
                            min_interval_minutes=self._settings.dm.min_interval_minutes,
                        )
                        dm_result = await dm_pipeline.run(
                            repository=self._repo,
                            context=context,
                            tracker=self._tracker,
                            settings=self._settings,
                        )
                        result.dm = dm_result
                        logger.info(
                            "dm_stage_done",
                            sent=dm_result.dms_sent,
                            errors=dm_result.errors,
                            emergency=dm_result.emergency_halt,
                        )
                    finally:
                        await dm_session_mgr.close_all()

            result.success = True
            self._tracker.log_summary()

        except Exception as exc:
            result.error = str(exc)
            self._tracker.record_error("pipeline", str(exc))
            logger.error("pipeline_error", error=str(exc))

        return result


def _verify_startup(settings: Settings) -> list[str]:
    """Verify that required resources are available.

    Returns a list of error messages (empty if all checks pass).
    """
    errors: list[str] = []

    if not settings.gemini_api_key:
        errors.append("GEMINI_API_KEY is not set")

    if not settings.burner_x_username:
        errors.append("BURNER_X_USERNAME is not set")

    if not settings.burner_x_password:
        errors.append("BURNER_X_PASSWORD is not set")

    # DM pipeline requires nandemo credentials
    if settings.dm.enabled:
        if not settings.nandemo_x_username:
            errors.append("NANDEMO_X_USERNAME is not set (required for DM)")
        if not settings.nandemo_x_password:
            errors.append("NANDEMO_X_PASSWORD is not set (required for DM)")

    return errors


async def _async_run(args: argparse.Namespace) -> int:
    """Async entry point for the ``run`` subcommand."""
    settings = load_settings()

    setup_logging(
        level=settings.logging.level,
        log_dir=settings.logging.log_dir,
    )
    dry_run = getattr(args, "dry_run", False)
    logger.info("pipeline_starting", mode="dry_run" if dry_run else "live")

    # Startup verification
    if not dry_run:
        errors = _verify_startup(settings)
        if errors:
            for err in errors:
                logger.error("startup_check_failed", error=err)
            return 1

    # Initialize database
    db_url = settings.database_url or settings.database.url
    repo = Repository(db_url)
    repo.init_db()

    # Load knowledge base
    kb = TreatmentKnowledgeBase()
    loaded = kb.load()
    logger.info("knowledge_base_loaded", procedures=loaded)

    # Run pipeline
    runner = PipelineRunner(settings, repo, kb)
    result = await runner.run_once(dry_run=dry_run)

    if result.success:
        logger.info(
            "pipeline_complete",
            searched=result.search_count,
            collected=result.collect.stored if result.collect else 0,
            analyzed=result.analyze.total_processed if result.analyze else 0,
            replied=result.reply.replies_sent if result.reply else 0,
            dms_sent=result.dm.dms_sent if result.dm else 0,
        )
        return 0

    logger.error("pipeline_failed", error=result.error)
    return 1


async def _async_daemon(args: argparse.Namespace) -> int:
    """Async entry point for the ``daemon`` subcommand."""
    from src.daemon import run_daemon

    settings = load_settings()

    setup_logging(
        level=settings.logging.level,
        log_dir=settings.logging.log_dir,
    )
    logger.info("daemon_starting")

    errors = _verify_startup(settings)
    if errors:
        for err in errors:
            logger.error("startup_check_failed", error=err)
        return 1

    await run_daemon(settings)
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    """Handle the ``run`` subcommand."""
    return asyncio.run(_async_run(args))


def _cmd_daemon(args: argparse.Namespace) -> int:
    """Handle the ``daemon`` subcommand."""
    return asyncio.run(_async_daemon(args))


def _cmd_status(args: argparse.Namespace) -> int:
    """Handle the ``status`` subcommand."""
    from src.cli.status import run_status

    settings = load_settings()
    output = run_status(settings)
    print(output)
    return 0


def _cmd_setup(args: argparse.Namespace) -> int:
    """Handle the ``setup`` subcommand."""
    from src.cli.setup import run_setup

    output, all_passed = run_setup()
    print(output)
    return 0 if all_passed else 1


def _cmd_halt(args: argparse.Namespace) -> int:
    """Handle the ``halt`` subcommand."""
    from src.pipeline.halt import HaltManager, mark_resumed

    halt_mgr = HaltManager()
    action = getattr(args, "halt_action", "status")

    if action == "resume":
        if halt_mgr.resume():
            mark_resumed(halt_mgr)
            print("Halt cleared. Next run will execute at 50% volume.")
        else:
            print("Pipeline is not halted.")
        return 0

    # Default: show halt status
    if halt_mgr.is_halted():
        info = halt_mgr.get_halt_info()
        print("HALTED")
        if info:
            print(f"  Reason:    {info.get('reason', 'unknown')}")
            print(f"  Source:    {info.get('source', 'unknown')}")
            print(f"  Timestamp: {info.get('timestamp', 'unknown')}")
        print("\nRun 'x-outreach halt resume' to clear.")
        return 1
    print("Pipeline is running normally (not halted).")
    return 0


def _cmd_blocklist(args: argparse.Namespace) -> int:
    """Handle the ``blocklist`` subcommand."""
    from src.cli.blocklist import (
        run_blocklist_add,
        run_blocklist_list,
        run_blocklist_remove,
    )

    settings = load_settings()
    db_url = settings.database_url or settings.database.url
    action = getattr(args, "blocklist_action", "list")

    if action == "add":
        username = getattr(args, "username", None)
        if not username:
            print("Error: username is required for 'blocklist add'.")
            return 1
        print(run_blocklist_add(username, db_url=db_url))
        return 0

    if action == "remove":
        username = getattr(args, "username", None)
        if not username:
            print("Error: username is required for 'blocklist remove'.")
            return 1
        print(run_blocklist_remove(username, db_url=db_url))
        return 0

    # Default: list
    print(run_blocklist_list(db_url=db_url))
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    """Handle the ``report`` subcommand."""
    from src.cli.report import run_report

    settings = load_settings()
    output = run_report(settings)
    print(output)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="x-outreach",
        description="X Outreach Pipeline for @ask.nandemo",
    )

    # Top-level flags for backward compatibility
    parser.add_argument(
        "--once",
        action="store_true",
        default=False,
        help="Run the pipeline once (backward-compat shortcut for 'run')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Skip browser search; only analyze already-collected tweets",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- run ---
    run_parser = subparsers.add_parser("run", help="Run the pipeline once")
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Skip browser search; only analyze already-collected tweets",
    )

    # --- daemon ---
    subparsers.add_parser("daemon", help="Start the daemon loop (24hr, variable 2-4hr cycles)")

    # --- status ---
    subparsers.add_parser("status", help="Show pipeline status and stats")

    # --- setup ---
    subparsers.add_parser("setup", help="Run first-time setup checks")

    # --- halt ---
    halt_parser = subparsers.add_parser("halt", help="Emergency halt management")
    halt_parser.add_argument(
        "halt_action",
        nargs="?",
        default="status",
        choices=["status", "resume"],
        help="Halt action: 'status' (default) or 'resume'",
    )

    # --- blocklist ---
    blocklist_parser = subparsers.add_parser("blocklist", help="User blocklist management")
    blocklist_parser.add_argument(
        "blocklist_action",
        nargs="?",
        default="list",
        choices=["add", "remove", "list"],
        help="Blocklist action: 'add', 'remove', or 'list' (default)",
    )
    blocklist_parser.add_argument(
        "username",
        nargs="?",
        default=None,
        help="Username to add or remove (e.g. @username)",
    )

    # --- report ---
    subparsers.add_parser("report", help="Generate weekly report")

    return parser


def main() -> None:
    """CLI entry point with subcommand routing."""
    parser = _build_parser()
    args = parser.parse_args()

    # Backward compatibility: --once or no command defaults to 'run'
    command = args.command
    if command is None:
        command = "run"

    dispatch = {
        "run": _cmd_run,
        "daemon": _cmd_daemon,
        "status": _cmd_status,
        "setup": _cmd_setup,
        "halt": _cmd_halt,
        "blocklist": _cmd_blocklist,
        "report": _cmd_report,
    }

    handler = dispatch.get(command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    exit_code = handler(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
