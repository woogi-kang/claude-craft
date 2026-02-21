"""Reply pipeline -- post replies to classified tweets via Playwright.

Uses Playwright browser automation to reply to tweets classified with
``llm_decision=True``.  Enforces rate limits (daily cap, min interval)
and quiet hours (23:00-08:00 JST).
"""

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass, field
from datetime import UTC, datetime

from outreach_shared.browser.human_sim import random_mouse_move, random_pause
from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.rate_limiter import SlidingWindowLimiter
from outreach_shared.utils.time_utils import is_active_hours
from playwright.async_api import BrowserContext

from src.ai.content_gen import ContentGenerationError, ContentGenerator
from src.config import Settings
from src.db.repository import Repository
from src.knowledge.templates import TemplateSelector
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.track import ActionTracker
from src.platform.selectors import (
    REPLY_BUTTON,
    REPLY_SUBMIT_BUTTON,
    REPLY_TEXT_INPUT,
    detect_restriction,
)

logger = get_logger("reply")


@dataclass
class ReplyResult:
    """Summary of a reply pipeline run."""

    total_candidates: int = 0
    replies_sent: int = 0
    skipped_quiet_hours: int = 0
    skipped_daily_limit: int = 0
    skipped_max_thread: int = 0
    skipped_interval: int = 0
    errors: int = 0
    emergency_halt: bool = False
    error_details: list[str] = field(default_factory=list)


class ReplyPipeline:
    """Post replies to classified tweets via Playwright browser automation.

    Parameters
    ----------
    content_gen:
        Content generator for creating reply text.
    knowledge_base:
        Treatment knowledge base for context enrichment.
    template_selector:
        Template selector for rotation tracking.
    daily_limiter:
        Sliding window limiter for daily reply cap.
    min_interval_minutes:
        Minimum minutes between replies.
    max_thread_replies:
        Maximum replies per conversation thread.
    """

    def __init__(
        self,
        content_gen: ContentGenerator,
        knowledge_base: TreatmentKnowledgeBase,
        template_selector: TemplateSelector | None = None,
        daily_limiter: SlidingWindowLimiter | None = None,
        min_interval_minutes: int = 20,
        max_thread_replies: int = 3,
    ) -> None:
        self._content_gen = content_gen
        self._kb = knowledge_base
        self._template_selector = template_selector or TemplateSelector()
        self._daily_limiter = daily_limiter or SlidingWindowLimiter(
            max_actions=50, window_seconds=86_400.0
        )
        self._min_interval_minutes = min_interval_minutes
        self._max_thread_replies = max_thread_replies
        self._last_reply_time: datetime | None = None

    async def run(
        self,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
    ) -> ReplyResult:
        """Process all 'analyzed' tweets with llm_decision=True.

        Applies the following filters before replying:
        - Only tweets with llm_decision=True
        - Daily reply limit
        - Max replies per user thread
        - No replies between 23:00-08:00 JST
        - Min interval between replies

        Parameters
        ----------
        repository:
            Database repository for tweet lookup and updates.
        context:
            Authenticated Playwright browser context.
        tracker:
            Action tracker for audit logging.
        settings:
            Application settings.

        Returns
        -------
        ReplyResult
            Aggregate statistics for the run.
        """
        result = ReplyResult()

        if not is_active_hours(start_hour=8, end_hour=22):
            logger.info("reply_quiet_hours")
            return result

        tweets = repository.get_tweets_by_status("analyzed")
        if not tweets:
            logger.info("reply_no_candidates")
            return result

        # Filter to actionable tweets (llm_decision=True)
        candidates = [t for t in tweets if t.get("llm_decision") is True]
        result.total_candidates = len(candidates)

        if not candidates:
            logger.info("reply_no_actionable_tweets")
            return result

        logger.info("reply_start", candidates=len(candidates))

        for tweet in candidates:
            tweet_id = tweet["post_id"]
            username = tweet.get("username", "")
            intent_type = tweet.get("intent_type", "review")
            tweet_url = tweet.get("post_url", "")

            # Re-check quiet hours (loop may span midnight)
            if not is_active_hours(start_hour=8, end_hour=22):
                result.skipped_quiet_hours += 1
                break

            # Daily limit check
            if not self._daily_limiter.can_act():
                result.skipped_daily_limit += 1
                logger.info("reply_daily_limit_reached")
                break

            # Thread reply limit
            thread_count = repository.count_user_replies(username)
            if thread_count >= self._max_thread_replies:
                result.skipped_max_thread += 1
                logger.info(
                    "reply_thread_limit",
                    tweet_id=tweet_id,
                    username=username,
                    thread_count=thread_count,
                )
                continue

            # Min interval between replies
            if self._last_reply_time is not None:
                elapsed = (datetime.now(tz=UTC) - self._last_reply_time).total_seconds()
                min_secs = self._min_interval_minutes * 60
                if elapsed < min_secs:
                    wait_time = min_secs - elapsed
                    logger.info("reply_interval_wait", wait_seconds=int(wait_time))
                    await asyncio.sleep(wait_time)

            # Build treatment context
            treatment_ctx = _build_treatment_context(tweet.get("contents", ""), self._kb)

            # Generate reply content
            try:
                reply_text = await self._content_gen.generate_reply(
                    tweet_content=tweet.get("contents", ""),
                    author_username=username,
                    template_category=intent_type,
                    treatment_context=treatment_ctx,
                )
            except ContentGenerationError as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: content_gen: {exc}")
                tracker.record_error("reply_content_gen", str(exc))
                continue

            # Post reply via Playwright
            try:
                success = await _post_reply_via_playwright(context, tweet_url, reply_text)
            except ReplyRateLimitError:
                result.emergency_halt = True
                result.errors += 1
                result.error_details.append(f"{tweet_id}: rate_limit_emergency_halt")
                tracker.record_error("reply_emergency", "Rate limit detected, halting")
                logger.warning("reply_emergency_halt", tweet_id=tweet_id)
                break
            except Exception as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: {exc}")
                tracker.record_error("reply_post", str(exc))
                logger.error("reply_error", tweet_id=tweet_id, error=str(exc))
                continue

            if success:
                self._daily_limiter.record()
                self._last_reply_time = datetime.now(tz=UTC)

                repository.update_tweet_status(
                    tweet_id,
                    status="replied",
                    reply_content=reply_text,
                    reply_timestamp=datetime.now(tz=UTC).isoformat(),
                )
                tracker.record_reply(tweet_id, username)
                result.replies_sent += 1

                logger.info(
                    "reply_sent",
                    tweet_id=tweet_id,
                    username=username,
                    daily_used=self._daily_limiter.actions_used,
                )

        logger.info(
            "reply_complete",
            sent=result.replies_sent,
            candidates=result.total_candidates,
            errors=result.errors,
        )
        return result


async def _post_reply_via_playwright(
    context: BrowserContext,
    tweet_url: str,
    reply_text: str,
) -> bool:
    """Post a reply to a tweet via Playwright browser automation.

    Parameters
    ----------
    context:
        Authenticated Playwright browser context.
    tweet_url:
        Full URL of the tweet to reply to.
    reply_text:
        Text content for the reply.

    Returns
    -------
    bool
        ``True`` if the reply was posted successfully.

    Raises
    ------
    ReplyRateLimitError
        When X rate-limits or restricts the account.
    """
    if not tweet_url:
        logger.warning("reply_no_url")
        return False

    page = context.pages[0] if context.pages else await context.new_page()

    try:
        # Navigate to the tweet
        await page.goto(tweet_url, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(3.0, 5.5)

        # Check for rate limit / restriction
        page_content = await page.content()
        if detect_restriction(page_content):
            raise ReplyRateLimitError("Account rate-limited or restricted")

        # Click the reply button on the tweet
        reply_btn = await page.wait_for_selector(REPLY_BUTTON, timeout=10_000)
        if reply_btn is None:
            logger.warning("reply_button_not_found", url=tweet_url)
            return False

        await random_mouse_move(page)
        await reply_btn.click()
        await random_pause(2.0, 4.0)

        # Type reply text
        reply_input = await page.wait_for_selector(REPLY_TEXT_INPUT, timeout=10_000)
        if reply_input is None:
            logger.warning("reply_input_not_found", url=tweet_url)
            return False

        await reply_input.click()
        await random_pause(0.5, 1.2)

        # Type character by character with human-like delays
        for char in reply_text:
            delay_ms = random.randint(65, 273)
            await page.keyboard.type(char, delay=delay_ms)
            if random.random() < 0.08:
                await asyncio.sleep(random.uniform(0.9, 2.6))

        await random_pause(0.7, 2.0)

        # Click the reply submit button
        submit_btn = await page.query_selector(REPLY_SUBMIT_BUTTON)
        if submit_btn:
            await random_mouse_move(page)
            await random_pause(0.7, 1.4)
            await submit_btn.click()
            await random_pause(4.0, 7.0)

        # Check for restriction after posting
        page_content = await page.content()
        if detect_restriction(page_content):
            raise ReplyRateLimitError("Restriction detected after reply attempt")

        logger.info("reply_playwright_sent", url=tweet_url)
        return True

    except ReplyRateLimitError:
        raise
    except Exception as exc:
        logger.error("reply_playwright_error", url=tweet_url, error=str(exc))
        raise


def _build_treatment_context(tweet_content: str, kb: TreatmentKnowledgeBase) -> str:
    """Extract treatment context from tweet content using the knowledge base.

    Scans the tweet for known Japanese treatment terms and builds a
    context string with Korean equivalents and pricing data.
    """
    from src.knowledge.treatments import JAPANESE_TO_KOREAN

    matches: list[str] = []
    for jp_name in JAPANESE_TO_KOREAN:
        if jp_name in tweet_content:
            info = kb.lookup_by_japanese(jp_name)
            if info:
                parts = [f"- {jp_name} ({info.korean_name})"]
                if info.average_price:
                    parts.append(f"  Price range: {info.average_price}")
                if info.downtime:
                    parts.append(f"  Downtime: {info.downtime}")
                if info.duration:
                    parts.append(f"  Duration: {info.duration}")
                matches.append("\n".join(parts))

    return "\n".join(matches) if matches else ""


class ReplyRateLimitError(Exception):
    """Raised when X rate-limits or restricts the account during reply."""
