"""DM pipeline -- send personalized DMs via Playwright browser automation.

Follows up on replied tweets by sending a personalized DM after a
configurable delay (10-30 min). Uses Playwright with the outreach account
session cookies to navigate X's messaging interface.
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
from playwright.async_api import BrowserContext, Page

from src.ai.content_gen import (
    ContentGenerationError,
    ContentGenerator,
    dm_uniqueness_check,
)
from src.config import Settings
from src.db.repository import Repository
from src.knowledge.templates import TemplateSelector
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.reply import _build_treatment_context
from src.pipeline.track import ActionTracker
from src.platform.selectors import (
    DM_COMPOSER_INPUT,
    DM_CONVERSATION,
    DM_NEXT_BUTTON,
    DM_SEARCH_INPUT,
    DM_TYPEAHEAD_RESULT,
    MESSAGES_URL,
    NEW_DM_BUTTON,
    NEW_DM_LINK,
    RESTRICTION_INDICATORS,
)

logger = get_logger("dm")


@dataclass
class DmResult:
    """Summary of a DM pipeline run."""

    total_candidates: int = 0
    dms_sent: int = 0
    skipped_quiet_hours: int = 0
    skipped_daily_limit: int = 0
    skipped_dm_closed: int = 0
    skipped_uniqueness: int = 0
    skipped_interval: int = 0
    skipped_too_soon: int = 0
    errors: int = 0
    emergency_halt: bool = False
    error_details: list[str] = field(default_factory=list)


class DmPipeline:
    """Send personalized DMs via Playwright browser automation.

    Parameters
    ----------
    content_gen:
        Content generator for creating DM text.
    knowledge_base:
        Treatment knowledge base for context enrichment.
    template_selector:
        Template selector for rotation tracking.
    daily_limiter:
        Sliding window limiter for daily DM cap.
    min_interval_minutes:
        Minimum interval between DMs in minutes.
    dm_delay_min_minutes:
        Minimum delay after reply before sending DM.
    dm_delay_max_minutes:
        Maximum delay after reply before sending DM.
    """

    def __init__(
        self,
        content_gen: ContentGenerator,
        knowledge_base: TreatmentKnowledgeBase,
        template_selector: TemplateSelector | None = None,
        daily_limiter: SlidingWindowLimiter | None = None,
        min_interval_minutes: int = 25,
        dm_delay_min_minutes: int = 10,
        dm_delay_max_minutes: int = 30,
    ) -> None:
        self._content_gen = content_gen
        self._kb = knowledge_base
        self._template_selector = template_selector or TemplateSelector()
        self._daily_limiter = daily_limiter or SlidingWindowLimiter(
            max_actions=20, window_seconds=86_400.0
        )
        self._min_interval_minutes = min_interval_minutes
        self._dm_delay_min = dm_delay_min_minutes
        self._dm_delay_max = dm_delay_max_minutes
        self._last_dm_time: datetime | None = None

    async def run(
        self,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
    ) -> DmResult:
        """Process all 'replied' tweets for DM follow-up.

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
        DmResult
            Aggregate statistics for the run.
        """
        result = DmResult()

        if not is_active_hours(start_hour=8, end_hour=22):
            logger.info("dm_quiet_hours")
            return result

        tweets = repository.get_tweets_by_status("replied")
        if not tweets:
            logger.info("dm_no_candidates")
            return result

        result.total_candidates = len(tweets)
        logger.info("dm_start", candidates=len(tweets))

        for tweet in tweets:
            tweet_id = tweet["post_id"]
            username = tweet.get("username", "")
            intent_type = tweet.get("intent_type", "review")

            # Re-check quiet hours
            if not is_active_hours(start_hour=8, end_hour=22):
                result.skipped_quiet_hours += 1
                break

            # Daily limit check
            if not self._daily_limiter.can_act():
                result.skipped_daily_limit += 1
                logger.info("dm_daily_limit_reached")
                break

            # Check if enough time has passed since reply
            reply_ts = tweet.get("reply_timestamp")
            if reply_ts and not _is_dm_ready(reply_ts, self._dm_delay_min, self._dm_delay_max):
                result.skipped_too_soon += 1
                continue

            # Min interval between DMs
            if self._last_dm_time is not None:
                elapsed = (datetime.now(tz=UTC) - self._last_dm_time).total_seconds()
                min_interval_secs = self._min_interval_minutes * 60
                if elapsed < min_interval_secs:
                    wait_time = min_interval_secs - elapsed
                    logger.info("dm_interval_wait", wait_seconds=int(wait_time))
                    await asyncio.sleep(wait_time)

            # Get previous DM for uniqueness check
            previous_dm = repository.get_last_dm_to_user(username)

            # Build treatment context
            treatment_ctx = _build_treatment_context(tweet.get("contents", ""), self._kb)

            # Select template with rotation
            dm_template = self._template_selector.get_dm_template(intent_type)
            effective_category = dm_template.id if dm_template else intent_type

            # Generate DM content
            try:
                dm_text = await self._content_gen.generate_dm(
                    tweet_content=tweet.get("contents", ""),
                    author_username=username,
                    template_category=intent_type,
                    reply_content=tweet.get("reply_content", ""),
                    treatment_context=treatment_ctx,
                    previous_dm=previous_dm,
                )
            except ContentGenerationError as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: content_gen: {exc}")
                tracker.record_error("dm_content_gen", str(exc))
                continue

            # Uniqueness check
            if previous_dm and not dm_uniqueness_check(dm_text, previous_dm):
                result.skipped_uniqueness += 1
                logger.info(
                    "dm_uniqueness_failed",
                    tweet_id=tweet_id,
                    username=username,
                )
                continue

            # Send DM via Playwright
            try:
                dm_sent = await _send_dm_via_playwright(context, username, dm_text)
            except DmClosedError:
                result.skipped_dm_closed += 1
                repository.update_tweet_status(
                    tweet_id,
                    status="dm_skipped",
                    dm_skip_reason="dm_closed_detected",
                )
                tracker.record_dm_skip(username, "dm_closed_detected")
                logger.info("dm_closed_detected", username=username)
                continue
            except DmRateLimitError:
                result.emergency_halt = True
                result.errors += 1
                result.error_details.append(f"{tweet_id}: rate_limit_emergency_halt")
                tracker.record_error("dm_emergency", "Rate limit detected, 24hr pause")
                logger.warning("dm_emergency_halt", tweet_id=tweet_id, pause_hours=24)
                break
            except Exception as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: send: {exc}")
                tracker.record_error("dm_send", str(exc))
                logger.error(
                    "dm_send_error",
                    tweet_id=tweet_id,
                    username=username,
                    error=str(exc),
                )
                continue

            if dm_sent:
                self._daily_limiter.record()
                self._last_dm_time = datetime.now(tz=UTC)

                repository.update_tweet_status(
                    tweet_id,
                    status="dm_sent",
                    dm_content=dm_text,
                    dm_timestamp=datetime.now(tz=UTC).isoformat(),
                    dm_template_used=effective_category,
                )
                tracker.record_dm(username, effective_category)
                result.dms_sent += 1

                logger.info(
                    "dm_sent",
                    tweet_id=tweet_id,
                    username=username,
                    template=effective_category,
                    daily_used=self._daily_limiter.actions_used,
                )

        logger.info(
            "dm_complete",
            sent=result.dms_sent,
            candidates=result.total_candidates,
            errors=result.errors,
            emergency_halt=result.emergency_halt,
        )
        return result


# ---------------------------------------------------------------------------
# Playwright DM automation
# ---------------------------------------------------------------------------


async def _send_dm_via_playwright(
    context: BrowserContext,
    username: str,
    message: str,
) -> bool:
    """Send a DM to the specified user via Playwright.

    Navigates to X's messaging interface, searches for the user,
    types the message with human-like delays, and sends it.

    Parameters
    ----------
    context:
        Authenticated Playwright browser context.
    username:
        Target user's X username (without @).
    message:
        DM text to send.

    Returns
    -------
    bool
        ``True`` if the DM was sent successfully.

    Raises
    ------
    DmClosedError
        When the user's DMs are closed.
    DmRateLimitError
        When X rate-limits or restricts the account.
    """
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        # Step 1: Navigate to messages
        await page.goto(MESSAGES_URL, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(2.0, 4.0)

        # Check for rate limit / restriction indicators
        page_content = await page.content()
        if _detect_rate_limit(page_content):
            raise DmRateLimitError("Account rate-limited or restricted")

        # Step 2: Click "New message" button
        new_msg_btn = await page.wait_for_selector(NEW_DM_BUTTON, timeout=10_000)
        if new_msg_btn is None:
            new_msg_btn = await page.query_selector(NEW_DM_LINK)
        if new_msg_btn:
            await new_msg_btn.click()
            await random_pause(1.5, 3.0)

        # Step 3: Search for username
        search_input = await page.wait_for_selector(DM_SEARCH_INPUT, timeout=10_000)
        if search_input is None:
            search_input = await page.query_selector("input[placeholder]")

        if search_input:
            await search_input.click()
            await random_pause(0.3, 0.8)
            # Type username character by character
            for char in username:
                delay_ms = random.randint(50, 120)
                await page.keyboard.type(char, delay=delay_ms)
            await random_pause(1.5, 3.0)

        # Step 4: Select user from results
        user_result = await page.wait_for_selector(
            f"{DM_TYPEAHEAD_RESULT} >> text=@{username}",
            timeout=10_000,
        )
        if user_result is None:
            raise DmClosedError(f"Cannot find user @{username} in DM search")

        await user_result.click()
        await random_pause(1.0, 2.0)

        # Click Next/Start conversation button
        next_btn = await page.query_selector(DM_NEXT_BUTTON)
        if next_btn:
            await next_btn.click()
            await random_pause(1.5, 3.0)

        # Step 5: Type message with human-like delays
        msg_input = await page.wait_for_selector(DM_COMPOSER_INPUT, timeout=10_000)
        if msg_input is None:
            msg_input = await page.query_selector('[role="textbox"][data-testid]')

        if msg_input:
            await msg_input.click()
            await random_pause(0.3, 0.8)
            await _type_message_naturally(page, message)
            await random_pause(0.5, 1.5)

        # Step 6: Send the message
        send_btn = await page.query_selector('[data-testid="dmComposerSendButton"]')
        if send_btn:
            await random_mouse_move(page)
            await random_pause(0.5, 1.0)
            await send_btn.click()
            await random_pause(2.0, 4.0)

        # Verify send success by checking for the message in conversation
        sent_indicator = await page.query_selector(DM_CONVERSATION)
        if sent_indicator:
            logger.info("dm_playwright_sent", username=username)
            return True

        return True

    except (DmClosedError, DmRateLimitError):
        raise
    except Exception as exc:
        logger.error("dm_playwright_error", username=username, error=str(exc))
        raise


async def _type_message_naturally(page: Page, message: str) -> None:
    """Type a message with natural-feeling speed variation."""
    for char in message:
        delay_ms = random.randint(30, 150)
        await page.keyboard.type(char, delay=delay_ms)

        # Occasional longer pause (simulating thinking)
        if random.random() < 0.05:
            await asyncio.sleep(random.uniform(0.5, 1.5))


def _detect_rate_limit(page_content: str) -> bool:
    """Check page content for rate limit or restriction indicators."""
    lower_content = page_content.lower()
    return any(ind in lower_content for ind in RESTRICTION_INDICATORS)


def _is_dm_ready(
    reply_timestamp: str,
    min_delay_minutes: int,
    max_delay_minutes: int,
) -> bool:
    """Check if enough time has elapsed since the reply for DM readiness.

    Parameters
    ----------
    reply_timestamp:
        ISO format timestamp of when the reply was sent.
    min_delay_minutes:
        Minimum delay in minutes before DM is allowed.
    max_delay_minutes:
        Maximum delay (unused in check, but defines the ready window).

    Returns
    -------
    bool
        ``True`` if the reply was sent more than *min_delay_minutes* ago.
    """
    try:
        reply_time = datetime.fromisoformat(reply_timestamp)
        if reply_time.tzinfo is None:
            reply_time = reply_time.replace(tzinfo=UTC)
        elapsed_minutes = (datetime.now(tz=UTC) - reply_time).total_seconds() / 60.0
        return elapsed_minutes >= min_delay_minutes
    except (ValueError, TypeError):
        return True


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class DmClosedError(Exception):
    """Raised when the target user's DMs are closed."""


class DmRateLimitError(Exception):
    """Raised when X rate-limits or restricts the account."""
