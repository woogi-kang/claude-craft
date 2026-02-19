"""Pipeline orchestrator -- wire all stages together.

Provides ``PipelineRunner`` which executes the full
Search -> Collect -> Analyze cycle, and a CLI entry point
for single runs and dry-run simulations.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from dataclasses import dataclass

from playwright.async_api import async_playwright

from src.ai.classifier import TweetClassifier
from src.config import Settings, load_settings
from src.db.repository import Repository
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.analyze import AnalyzePipeline, AnalyzeResult
from src.pipeline.collect import CollectPipeline, CollectResult
from src.pipeline.search import SearchPipeline
from src.pipeline.track import ActionTracker
from src.browser.session import SessionManager
from src.utils.logger import get_logger, setup_logging

logger = get_logger("main")


@dataclass
class PipelineRunResult:
    """Aggregated result from a full pipeline run."""

    search_count: int = 0
    collect: CollectResult | None = None
    analyze: AnalyzeResult | None = None
    success: bool = False
    error: str | None = None


class PipelineRunner:
    """Orchestrate the Search -> Collect -> Analyze pipeline.

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
                    max_tweet_age_hours=self._settings.search.max_tweet_age_hours,
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
                        healthy = await session_mgr.check_session_health(context)
                        if not healthy:
                            logger.info("session_expired_relogin")
                            logged_in = await session_mgr.login(
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
                api_key=self._settings.anthropic_api_key,
                model=self._settings.analyze.model,
                confidence_threshold=self._settings.analyze.confidence_threshold,
                domain_context=self._kb.get_classification_context(),
            )
            analyze_pipeline = AnalyzePipeline(classifier)
            analyze_result = await analyze_pipeline.run(self._repo)
            result.analyze = analyze_result

            # Track individual classifications
            analyzed_tweets = self._repo.get_tweets_by_status("analyzed")
            for tweet in analyzed_tweets:
                if tweet.get("classification"):
                    self._tracker.record_analyze(
                        tweet["tweet_id"],
                        tweet["classification"],
                        tweet.get("confidence", 0.0),
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
    """
    errors: list[str] = []

    if not settings.anthropic_api_key:
        errors.append("ANTHROPIC_API_KEY is not set")

    if not settings.burner_x_username:
        errors.append("BURNER_X_USERNAME is not set")

    if not settings.burner_x_password:
        errors.append("BURNER_X_PASSWORD is not set")

    return errors


async def _async_main(args: argparse.Namespace) -> int:
    """Async entry point."""
    settings = load_settings()

    # Setup logging
    setup_logging(
        level=settings.logging.level,
        log_dir=settings.logging.log_dir,
    )
    logger.info("pipeline_starting", mode="dry_run" if args.dry_run else "live")

    # Startup verification
    if not args.dry_run:
        errors = _verify_startup(settings)
        if errors:
            for err in errors:
                logger.error("startup_check_failed", error=err)
            return 1

    # Initialize database
    repo = Repository(settings.database.path)
    repo.init_db()

    # Load knowledge base
    kb = TreatmentKnowledgeBase()
    loaded = kb.load()
    logger.info("knowledge_base_loaded", procedures=loaded)

    # Run pipeline
    runner = PipelineRunner(settings, repo, kb)
    result = await runner.run_once(dry_run=args.dry_run)

    if result.success:
        logger.info(
            "pipeline_complete",
            searched=result.search_count,
            collected=result.collect.stored if result.collect else 0,
            analyzed=result.analyze.total_processed if result.analyze else 0,
        )
        return 0

    logger.error("pipeline_failed", error=result.error)
    return 1


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="X Outreach Pipeline for @ask.nandemo",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        default=True,
        help="Run the pipeline once (default behaviour)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Skip browser search; only analyze already-collected tweets",
    )
    args = parser.parse_args()

    exit_code = asyncio.run(_async_main(args))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
