"""Posting pipeline -- publish casual tweets via Playwright.

Generates and publishes original casual tweets from the @ask.nandemo
account to build a natural activity profile.  Runs independently from
the main outreach pipeline, gated by a probability check per daemon
cycle.

Content is explicitly non-professional: daily life, food, weather,
Tokyo observations -- never dermatology or beauty topics.
"""

from __future__ import annotations

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
from src.pipeline.track import ActionTracker
from src.platform.selectors import (
    COMPOSE_SUBMIT_BUTTON,
    COMPOSE_TEXT_INPUT,
    COMPOSE_TWEET_BUTTON,
    detect_restriction,
)

logger = get_logger("posting")


@dataclass
class PostingResult:
    """Summary of a posting pipeline run."""

    posts_published: int = 0
    skipped_quiet_hours: int = 0
    skipped_daily_limit: int = 0
    skipped_cooldown: int = 0
    errors: int = 0
    emergency_halt: bool = False
    error_details: list[str] = field(default_factory=list)


class PostingPipeline:
    """Publish casual tweets to build natural account activity.

    Parameters
    ----------
    content_gen:
        Content generator for creating casual tweet text.
    daily_limiter:
        Sliding-window limiter for daily post cap.
    min_interval_hours:
        Minimum hours between posts.
    """

    def __init__(
        self,
        content_gen: ContentGenerator,
        *,
        daily_limiter: SlidingWindowLimiter | None = None,
        min_interval_hours: float = 4.0,
    ) -> None:
        self._content_gen = content_gen
        self._daily_limiter = daily_limiter or SlidingWindowLimiter(
            max_actions=2, window_seconds=86_400.0
        )
        self._min_interval_hours = min_interval_hours
        self._last_post_time: datetime | None = None

    async def run(
        self,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
    ) -> PostingResult:
        """Publish one casual tweet if all conditions are met.

        Conditions checked:
        - Within active hours (narrower window: 10-21 JST)
        - Daily limit not reached
        - Minimum interval since last post elapsed

        Parameters
        ----------
        repository:
            Database repository (for config persistence).
        context:
            Authenticated Playwright browser context.
        tracker:
            Action tracker for audit logging.
        settings:
            Application settings.

        Returns
        -------
        PostingResult
            Statistics for this posting attempt.
        """
        result = PostingResult()

        # Narrower active hours for posting
        start_hour = settings.posting.active_start_hour
        end_hour = settings.posting.active_end_hour
        if not is_active_hours(start_hour=start_hour, end_hour=end_hour):
            result.skipped_quiet_hours += 1
            logger.info("posting_quiet_hours")
            return result

        # Daily limit
        if not self._daily_limiter.can_act():
            result.skipped_daily_limit += 1
            logger.info("posting_daily_limit_reached")
            return result

        # Minimum interval cooldown
        last_post_str = repository.get_config("last_post_time")
        if last_post_str:
            try:
                last_post_dt = datetime.fromisoformat(last_post_str)
                elapsed_hours = (datetime.now(tz=UTC) - last_post_dt).total_seconds() / 3600
                if elapsed_hours < self._min_interval_hours:
                    result.skipped_cooldown += 1
                    logger.info(
                        "posting_cooldown",
                        elapsed_hours=f"{elapsed_hours:.1f}",
                        min_hours=self._min_interval_hours,
                    )
                    return result
            except (ValueError, TypeError):
                pass  # Invalid stored time, proceed

        # Generate casual content
        try:
            tweet_text = await self._content_gen.generate_casual_post()
        except ContentGenerationError as exc:
            result.errors += 1
            result.error_details.append(f"content_gen: {exc}")
            tracker.record_error("posting_content_gen", str(exc))
            return result

        if not tweet_text:
            result.errors += 1
            result.error_details.append("content_gen: empty result")
            return result

        # Post via Playwright
        try:
            success = await _post_tweet_via_playwright(context, tweet_text)
        except PostingRateLimitError:
            result.emergency_halt = True
            result.errors += 1
            result.error_details.append("posting_rate_limit")
            tracker.record_error("posting_emergency", "Rate limit detected")
            logger.warning("posting_emergency_halt")
            return result
        except Exception as exc:
            result.errors += 1
            result.error_details.append(f"playwright: {exc}")
            tracker.record_error("posting", str(exc))
            logger.error("posting_error", error=str(exc))
            return result

        if success:
            self._daily_limiter.record()
            repository.set_config("last_post_time", datetime.now(tz=UTC).isoformat())
            tracker.record_post(len(tweet_text))
            result.posts_published += 1
            logger.info(
                "posting_published",
                length=len(tweet_text),
                content=tweet_text[:50],
            )

        return result


async def _post_tweet_via_playwright(
    context: BrowserContext,
    tweet_text: str,
) -> bool:
    """Compose and publish a tweet via Playwright.

    Parameters
    ----------
    context:
        Authenticated Playwright browser context.
    tweet_text:
        Text content for the tweet.

    Returns
    -------
    bool
        ``True`` if the tweet was posted successfully.

    Raises
    ------
    PostingRateLimitError
        When X rate-limits or restricts the account.
    """
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        # Navigate to home
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
        await random_pause(3.0, 5.5)

        # Check for restriction
        page_content = await page.content()
        if detect_restriction(page_content):
            raise PostingRateLimitError("Account restricted")

        # Click compose button
        compose_btn = await page.wait_for_selector(COMPOSE_TWEET_BUTTON, timeout=10_000)
        if compose_btn is None:
            logger.warning("posting_compose_btn_not_found")
            return False

        await random_mouse_move(page)
        await compose_btn.click()
        await random_pause(2.0, 4.0)

        # Type into compose area
        text_input = await page.wait_for_selector(COMPOSE_TEXT_INPUT, timeout=10_000)
        if text_input is None:
            logger.warning("posting_text_input_not_found")
            return False

        await text_input.click()
        await random_pause(0.5, 1.2)

        # Type character by character with human-like delays
        for char in tweet_text:
            delay_ms = random.randint(65, 273)
            await page.keyboard.type(char, delay=delay_ms)
            if random.random() < 0.08:
                await asyncio.sleep(random.uniform(0.9, 2.6))

        await random_pause(1.0, 2.5)

        # Click the post button (wait for it to become available after typing)
        submit_btn = await page.wait_for_selector(COMPOSE_SUBMIT_BUTTON, timeout=10_000)
        if submit_btn is None:
            logger.warning("posting_submit_btn_not_found")
            return False

        await random_mouse_move(page)
        await random_pause(0.7, 1.4)
        await submit_btn.click()
        await random_pause(4.0, 7.0)

        # Check for restriction after posting
        page_content = await page.content()
        if detect_restriction(page_content):
            raise PostingRateLimitError("Restriction detected after post attempt")

        logger.info("posting_playwright_sent")
        return True

    except PostingRateLimitError:
        raise
    except Exception as exc:
        logger.error("posting_playwright_error", error=str(exc))
        raise


def posting_probability(settings: Settings) -> float:
    """Compute probability of posting in a given daemon cycle.

    Over many cycles, this probability produces approximately
    ``daily_limit`` posts per day within the active posting window.
    """
    active_hours = settings.posting.active_end_hour - settings.posting.active_start_hour
    if active_hours <= 0:
        return 0.0
    avg_interval = (settings.daemon.min_interval_hours + settings.daemon.max_interval_hours) / 2
    if avg_interval <= 0:
        return 0.0
    expected_cycles = active_hours / avg_interval
    return min(1.0, settings.posting.daily_limit / expected_cycles)


class PostingRateLimitError(Exception):
    """Raised when X rate-limits or restricts the account during posting."""
