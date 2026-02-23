"""Live stage-by-stage test -- run each pipeline feature once with 5 min gaps.

Usage:
    .venv/bin/python test_stages_live.py [stage]

Stages: nurture, reply, dm, posting, all (default)
"""

from __future__ import annotations

import asyncio
import sys

from outreach_shared.utils.logger import get_logger, setup_logging
from outreach_shared.utils.rate_limiter import SlidingWindowLimiter
from playwright.async_api import async_playwright

from src.ai.content_gen import ContentGenerator
from src.browser.session import SessionManager
from src.config import load_settings
from src.db.repository import Repository
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.dm import DmPipeline
from src.pipeline.nurture import NurturePipeline
from src.pipeline.posting import PostingPipeline
from src.pipeline.reply import ReplyPipeline
from src.pipeline.track import ActionTracker
from src.platform.login import check_session_health, login

logger = get_logger("live_test")

WAIT_BETWEEN_STAGES = 5 * 60  # 5 minutes


def _banner(title: str) -> None:
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  {title}")
    print(f"{sep}\n")


async def run_stages(stages: list[str]) -> None:
    settings = load_settings()
    setup_logging(level="DEBUG", log_dir=settings.logging.log_dir)

    db_url = settings.database_url or settings.database.url
    repo = Repository(db_url)
    repo.init_db()

    kb = TreatmentKnowledgeBase()
    kb.load()

    tracker = ActionTracker(repo)

    async with async_playwright() as pw:
        session_mgr = SessionManager(
            pw,
            headless=settings.browser.headless,
            viewport_width=settings.browser.viewport_width,
            viewport_height=settings.browser.viewport_height,
        )
        try:
            context = await session_mgr.get_session("burner")

            healthy = await check_session_health(context)
            if not healthy:
                logger.info("session_expired_relogin")
                await login(context, settings.burner_x_username, settings.burner_x_password)

            content_gen = ContentGenerator(
                api_key=settings.llm_api_key,
                model=settings.llm.model,
                provider=settings.llm.provider,
            )

            results = {}

            for i, stage in enumerate(stages):
                if i > 0:
                    _banner(f"Waiting {WAIT_BETWEEN_STAGES // 60} min before next stage...")
                    await asyncio.sleep(WAIT_BETWEEN_STAGES)

                if stage == "nurture":
                    _banner("STAGE: NURTURE (like/follow)")
                    pipeline = NurturePipeline(
                        follow_daily_limiter=SlidingWindowLimiter(
                            max_actions=5, window_seconds=86400
                        ),
                        like_daily_limiter=SlidingWindowLimiter(
                            max_actions=10, window_seconds=86400
                        ),
                        follow_probability=0.5,
                        like_probability=0.8,
                    )
                    result = await pipeline.run(repo, context, tracker, settings)
                    results["nurture"] = {
                        "follows": result.follows_sent,
                        "likes": result.likes_sent,
                        "already_followed": result.already_followed,
                        "already_liked": result.already_liked,
                        "errors": result.errors,
                        "emergency_halt": result.emergency_halt,
                    }
                    print(f"\n  Result: {results['nurture']}")

                elif stage == "reply":
                    _banner("STAGE: REPLY")
                    pipeline = ReplyPipeline(
                        content_gen=content_gen,
                        knowledge_base=kb,
                        daily_limiter=SlidingWindowLimiter(max_actions=5, window_seconds=86400),
                        min_interval_minutes=0,  # no wait for testing
                        max_interval_minutes=0,
                        max_thread_replies=3,
                    )
                    result = await pipeline.run(repo, context, tracker, settings)
                    results["reply"] = {
                        "candidates": result.total_candidates,
                        "sent": result.replies_sent,
                        "skipped_daily": result.skipped_daily_limit,
                        "skipped_thread": result.skipped_max_thread,
                        "errors": result.errors,
                        "emergency_halt": result.emergency_halt,
                    }
                    print(f"\n  Result: {results['reply']}")

                elif stage == "dm":
                    _banner("STAGE: DM")
                    pipeline = DmPipeline(
                        content_gen=content_gen,
                        knowledge_base=kb,
                        daily_limiter=SlidingWindowLimiter(max_actions=5, window_seconds=86400),
                        min_interval_minutes=0,  # no wait for testing
                        max_interval_minutes=0,
                        dm_delay_min_minutes=0,  # no delay after reply
                        dm_delay_max_minutes=0,
                    )
                    result = await pipeline.run(repo, context, tracker, settings)
                    results["dm"] = {
                        "candidates": result.total_candidates,
                        "sent": result.dms_sent,
                        "skipped_daily": result.skipped_daily_limit,
                        "skipped_closed": result.skipped_dm_closed,
                        "skipped_uniqueness": result.skipped_uniqueness,
                        "skipped_too_soon": result.skipped_too_soon,
                        "errors": result.errors,
                        "emergency_halt": result.emergency_halt,
                        "passcode_error": result.encryption_passcode_error,
                    }
                    print(f"\n  Result: {results['dm']}")

                elif stage == "posting":
                    _banner("STAGE: POSTING (casual tweet)")
                    pipeline = PostingPipeline(
                        content_gen=content_gen,
                        knowledge_base=kb,
                        daily_limiter=SlidingWindowLimiter(max_actions=3, window_seconds=86400),
                        min_interval_hours=0.0,  # no cooldown for testing
                    )
                    result = await pipeline.run(repo, context, tracker, settings)
                    results["posting"] = {
                        "published": result.posts_published,
                        "skipped_quiet": result.skipped_quiet_hours,
                        "skipped_daily": result.skipped_daily_limit,
                        "skipped_cooldown": result.skipped_cooldown,
                        "errors": result.errors,
                        "emergency_halt": result.emergency_halt,
                    }
                    print(f"\n  Result: {results['posting']}")

            # Final summary
            _banner("FINAL SUMMARY")
            for name, res in results.items():
                print(f"  {name}: {res}")

        finally:
            await session_mgr.close_all()


if __name__ == "__main__":
    stage_arg = sys.argv[1] if len(sys.argv) > 1 else "all"

    if stage_arg == "all":
        stages = ["nurture", "reply", "dm", "posting"]
    else:
        stages = [s.strip() for s in stage_arg.split(",")]

    print(f"Running stages: {stages}")
    print(f"Wait between stages: {WAIT_BETWEEN_STAGES // 60} min")
    asyncio.run(run_stages(stages))
