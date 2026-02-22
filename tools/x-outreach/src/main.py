"""Pipeline orchestrator -- wire all stages together.

Provides ``PipelineRunner`` which executes the full
Search -> Collect -> Analyze -> Reply -> DM cycle, and a CLI entry
point with subcommands: run, daemon, status, setup, halt.
"""

from __future__ import annotations

import argparse
import asyncio
import random
import sys
from dataclasses import dataclass

from outreach_shared.utils.logger import get_logger, setup_logging
from outreach_shared.utils.rate_limiter import SlidingWindowLimiter
from playwright.async_api import BrowserContext, async_playwright

from src.ai.classifier import TweetClassifier
from src.ai.content_gen import ContentGenerator
from src.browser.session import SessionManager
from src.config import Settings, load_settings
from src.db.repository import Repository
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.analyze import AnalyzePipeline, AnalyzeResult
from src.pipeline.collect import CollectPipeline, CollectResult
from src.pipeline.dm import DmPipeline, DmResult
from src.pipeline.nurture import NurturePipeline, NurtureResult
from src.pipeline.posting import PostingPipeline, PostingResult, posting_probability
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
    nurture: NurtureResult | None = None
    reply: ReplyResult | None = None
    dm: DmResult | None = None
    posting: PostingResult | None = None
    success: bool = False
    error: str | None = None


class PipelineRunner:
    """Orchestrate the Search -> Collect -> Analyze -> Nurture -> Reply -> DM -> Posting pipeline.

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

        # Persistent limiters -- must survive across run_once() calls so
        # that daily caps are actually enforced during daemon operation.
        self._follow_limiter = SlidingWindowLimiter(
            max_actions=settings.nurture.follow_daily_limit,
            window_seconds=86_400.0,
        )
        self._like_limiter = SlidingWindowLimiter(
            max_actions=settings.nurture.like_daily_limit,
            window_seconds=86_400.0,
        )
        self._reply_limiter = SlidingWindowLimiter(
            max_actions=settings.reply.daily_limit,
            window_seconds=86_400.0,
        )
        self._dm_limiter = SlidingWindowLimiter(
            max_actions=settings.dm.daily_limit,
            window_seconds=86_400.0,
        )
        self._posting_limiter = SlidingWindowLimiter(
            max_actions=settings.posting.daily_limit,
            window_seconds=86_400.0,
        )

    async def run_once(
        self,
        *,
        dry_run: bool = False,
        context: BrowserContext | None = None,
    ) -> PipelineRunResult:
        """Execute a single Search -> Collect -> Analyze -> Nurture -> Reply -> DM -> Posting cycle.

        Parameters
        ----------
        dry_run:
            When ``True``, skip browser-based search and use any
            already-collected tweets for analysis only.
        context:
            Pre-existing browser context to reuse. When provided the
            pipeline will NOT open or close its own browser -- the
            caller is responsible for lifecycle management.

        Returns
        -------
        PipelineRunResult
            Aggregated statistics from all pipeline stages.
        """
        result = PipelineRunResult()

        try:
            # --- Ensure session is healthy ---
            if context is not None:
                healthy = await check_session_health(context)
                if not healthy:
                    logger.info("session_expired_relogin")
                    logged_in = await login(
                        context,
                        self._settings.burner_x_username,
                        self._settings.burner_x_password,
                    )
                    if not logged_in:
                        result.error = "Failed to login"
                        self._tracker.record_error("login", result.error)
                        return result

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

                if context is not None:
                    # Use the shared browser context
                    raw_tweets = await search_pipeline.run(
                        self._settings.search.keywords,
                        context,
                    )
                    result.search_count = len(raw_tweets)

                    for kw in self._settings.search.keywords:
                        kw_tweets = [t for t in raw_tweets if t.search_keyword == kw]
                        self._tracker.record_search(kw, len(kw_tweets))

                    collect_result = collect_pipeline.run(raw_tweets, self._repo)
                    result.collect = collect_result
                    self._tracker.record_collect(
                        collect_result.stored,
                        collect_result.total_input - collect_result.stored,
                    )
                else:
                    # One-shot mode: open browser just for this run
                    async with async_playwright() as pw:
                        session_mgr = SessionManager(
                            pw,
                            headless=self._settings.browser.headless,
                            viewport_width=self._settings.browser.viewport_width,
                            viewport_height=self._settings.browser.viewport_height,
                        )
                        try:
                            ctx = await session_mgr.get_session("burner")
                            healthy = await check_session_health(ctx)
                            if not healthy:
                                logged_in = await login(
                                    ctx,
                                    self._settings.burner_x_username,
                                    self._settings.burner_x_password,
                                )
                                if not logged_in:
                                    result.error = "Failed to login"
                                    self._tracker.record_error("login", result.error)
                                    return result

                            raw_tweets = await search_pipeline.run(
                                self._settings.search.keywords,
                                ctx,
                            )
                            result.search_count = len(raw_tweets)

                            for kw in self._settings.search.keywords:
                                kw_tweets = [t for t in raw_tweets if t.search_keyword == kw]
                                self._tracker.record_search(kw, len(kw_tweets))

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
                api_key=self._settings.llm_api_key,
                model=self._settings.llm.model,
                confidence_threshold=(self._settings.classification.confidence_threshold),
                domain_context=self._kb.get_classification_context(),
                provider=self._settings.llm.provider,
            )
            analyze_pipeline = AnalyzePipeline(classifier)
            analyze_result = await analyze_pipeline.run(self._repo)
            result.analyze = analyze_result

            # --- Nurture: follow/like (if enabled) ---
            if self._settings.nurture.enabled and context is not None:
                nurture_pipeline = NurturePipeline(
                    follow_daily_limiter=self._follow_limiter,
                    like_daily_limiter=self._like_limiter,
                    follow_probability=self._settings.nurture.follow_probability,
                    like_probability=self._settings.nurture.like_probability,
                )
                nurture_result = await nurture_pipeline.run(
                    repository=self._repo,
                    context=context,
                    tracker=self._tracker,
                    settings=self._settings,
                )
                result.nurture = nurture_result
                logger.info(
                    "nurture_stage_done",
                    follows=nurture_result.follows_sent,
                    likes=nurture_result.likes_sent,
                    errors=nurture_result.errors,
                )

            # --- Reply (if enabled) ---
            reply_ctx = context  # reuse same browser
            if self._settings.reply.enabled and reply_ctx is not None:
                content_gen = ContentGenerator(
                    api_key=self._settings.llm_api_key,
                    model=self._settings.llm.model,
                    provider=self._settings.llm.provider,
                )
                reply_pipeline = ReplyPipeline(
                    content_gen=content_gen,
                    knowledge_base=self._kb,
                    daily_limiter=self._reply_limiter,
                    min_interval_minutes=self._settings.reply.min_interval_minutes,
                    max_interval_minutes=self._settings.reply.max_interval_minutes,
                )
                reply_result = await reply_pipeline.run(
                    repository=self._repo,
                    context=reply_ctx,
                    tracker=self._tracker,
                    settings=self._settings,
                )
                result.reply = reply_result
                logger.info(
                    "reply_stage_done",
                    sent=reply_result.replies_sent,
                    errors=reply_result.errors,
                )

            # --- DM (if enabled) ---
            dm_ctx = context  # reuse same browser
            if self._settings.dm.enabled and dm_ctx is not None:
                if not self._settings.reply.enabled:
                    content_gen = ContentGenerator(
                        api_key=self._settings.llm_api_key,
                        model=self._settings.llm.model,
                        provider=self._settings.llm.provider,
                    )
                dm_pipeline = DmPipeline(
                    content_gen=content_gen,
                    knowledge_base=self._kb,
                    daily_limiter=self._dm_limiter,
                    min_interval_minutes=self._settings.dm.min_interval_minutes,
                    max_interval_minutes=self._settings.dm.max_interval_minutes,
                )
                dm_result = await dm_pipeline.run(
                    repository=self._repo,
                    context=dm_ctx,
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

            # --- Posting: casual tweet (if enabled, probability-gated) ---
            if self._settings.posting.enabled and context is not None:
                prob = posting_probability(self._settings)
                if random.random() < prob:
                    content_gen = ContentGenerator(
                        api_key=self._settings.llm_api_key,
                        model=self._settings.llm.model,
                        provider=self._settings.llm.provider,
                    )
                    posting_pipeline = PostingPipeline(
                        content_gen=content_gen,
                        knowledge_base=self._kb,
                        daily_limiter=self._posting_limiter,
                        min_interval_hours=self._settings.posting.min_interval_hours,
                    )
                    posting_result = await posting_pipeline.run(
                        repository=self._repo,
                        context=context,
                        tracker=self._tracker,
                        settings=self._settings,
                    )
                    result.posting = posting_result
                    logger.info(
                        "posting_stage_done",
                        published=posting_result.posts_published,
                        errors=posting_result.errors,
                    )

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
    Credential checks are skipped when a persistent browser session
    already exists on disk (manual login flow).
    """
    from pathlib import Path

    errors: list[str] = []

    # API key only required for non-codex providers
    if settings.llm.provider != "codex" and not settings.llm_api_key:
        errors.append("LLM API key is not set (GEMINI_API_KEY in .env)")

    # Skip credential checks if a saved session exists
    session_dir = Path(__file__).resolve().parent.parent / "data" / "sessions" / "nandemo"
    has_session = (session_dir / "Default" / "Cookies").exists()

    if not has_session:
        if not settings.burner_x_username:
            errors.append("BURNER_X_USERNAME is not set")
        if not settings.burner_x_password:
            errors.append("BURNER_X_PASSWORD is not set")

        needs_nandemo = settings.dm.enabled or settings.nurture.enabled or settings.posting.enabled
        if needs_nandemo:
            if not settings.nandemo_x_username:
                errors.append("NANDEMO_X_USERNAME is not set (required for DM/nurture/posting)")
            if not settings.nandemo_x_password:
                errors.append("NANDEMO_X_PASSWORD is not set (required for DM/nurture/posting)")

    return errors


async def _async_run(args: argparse.Namespace) -> int:
    """Async entry point for the ``run`` subcommand.

    Opens a single browser session and keeps it alive for the entire
    Search -> Collect -> Analyze -> Reply -> DM cycle.
    """
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

    runner = PipelineRunner(settings, repo, kb)

    if dry_run:
        result = await runner.run_once(dry_run=True)
    else:
        # Single browser session for the entire pipeline
        async with async_playwright() as pw:
            session_mgr = SessionManager(
                pw,
                headless=settings.browser.headless,
                viewport_width=settings.browser.viewport_width,
                viewport_height=settings.browser.viewport_height,
            )
            try:
                context = await session_mgr.get_session("burner")
                result = await runner.run_once(context=context)
            finally:
                await session_mgr.close_all()

    if result.success:
        logger.info(
            "pipeline_complete",
            searched=result.search_count,
            collected=result.collect.stored if result.collect else 0,
            analyzed=result.analyze.total_processed if result.analyze else 0,
            follows=result.nurture.follows_sent if result.nurture else 0,
            likes=result.nurture.likes_sent if result.nurture else 0,
            replied=result.reply.replies_sent if result.reply else 0,
            dms_sent=result.dm.dms_sent if result.dm else 0,
            posted=result.posting.posts_published if result.posting else 0,
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
