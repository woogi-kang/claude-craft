"""Nurture pipeline -- follow users and like tweets via Playwright.

Interleaves follow and like actions randomly among analyzed leads
(``llm_decision=True``).  Each action is independently gated by a
probability coin-flip, a per-type daily cap, and DB deduplication.

These actions do **not** advance the post status -- they are non-destructive
side-effects that run between the Analyze and Reply stages.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum

from outreach_shared.browser.human_sim import human_scroll, random_mouse_move, random_pause
from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.rate_limiter import SlidingWindowLimiter
from outreach_shared.utils.time_utils import is_active_hours
from playwright.async_api import BrowserContext

from src.config import Settings
from src.db.repository import Repository
from src.pipeline.track import ActionTracker
from src.platform.selectors import (
    LIKE_BUTTON,
    PROFILE_FOLLOW_BUTTON,
    PROFILE_UNFOLLOW_BUTTON,
    UNLIKE_BUTTON,
    detect_restriction,
)

logger = get_logger("nurture")


# ---------------------------------------------------------------------------
# Outcome enums
# ---------------------------------------------------------------------------


class FollowOutcome(Enum):
    SUCCESS = "success"
    ALREADY_FOLLOWING = "already_following"
    ERROR = "error"


class LikeOutcome(Enum):
    SUCCESS = "success"
    ALREADY_LIKED = "already_liked"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------


@dataclass
class NurtureResult:
    """Summary of a nurture pipeline run."""

    total_candidates: int = 0
    follows_sent: int = 0
    likes_sent: int = 0
    already_followed: int = 0
    already_liked: int = 0
    skipped_quiet_hours: int = 0
    skipped_daily_limit_follow: int = 0
    skipped_daily_limit_like: int = 0
    errors: int = 0
    emergency_halt: bool = False
    error_details: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


class NurturePipeline:
    """Follow users and like tweets for analyzed leads.

    Parameters
    ----------
    follow_daily_limiter:
        Sliding-window limiter for daily follow cap.
    like_daily_limiter:
        Sliding-window limiter for daily like cap.
    follow_probability:
        Probability (0-1) of attempting a follow per candidate.
    like_probability:
        Probability (0-1) of attempting a like per candidate.
    """

    def __init__(
        self,
        *,
        follow_daily_limiter: SlidingWindowLimiter | None = None,
        like_daily_limiter: SlidingWindowLimiter | None = None,
        follow_probability: float = 0.4,
        like_probability: float = 0.6,
    ) -> None:
        self._follow_limiter = follow_daily_limiter or SlidingWindowLimiter(
            max_actions=10, window_seconds=86_400.0
        )
        self._like_limiter = like_daily_limiter or SlidingWindowLimiter(
            max_actions=15, window_seconds=86_400.0
        )
        self._follow_prob = follow_probability
        self._like_prob = like_probability

    async def run(
        self,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
    ) -> NurtureResult:
        """Process analyzed leads with random follow/like actions.

        Parameters
        ----------
        repository:
            Database repository for deduplication checks.
        context:
            Authenticated Playwright browser context.
        tracker:
            Action tracker for audit logging.
        settings:
            Application settings (for delay configuration).

        Returns
        -------
        NurtureResult
            Aggregate statistics for the run.
        """
        result = NurtureResult()

        if not is_active_hours(
            start_hour=settings.daemon.active_start_hour,
            end_hour=settings.daemon.active_end_hour,
        ):
            logger.info("nurture_quiet_hours")
            return result

        tweets = repository.get_tweets_by_status("analyzed")
        if not tweets:
            logger.info("nurture_no_candidates")
            return result

        candidates = [t for t in tweets if t.get("llm_decision") is True]
        result.total_candidates = len(candidates)

        if not candidates:
            logger.info("nurture_no_actionable_tweets")
            return result

        # Randomize order for natural-looking behavior
        random.shuffle(candidates)

        logger.info("nurture_start", candidates=len(candidates))

        for tweet in candidates:
            tweet_id = tweet["post_id"]
            username = tweet.get("username", "")

            # Re-check quiet hours
            if not is_active_hours(
                start_hour=settings.daemon.active_start_hour,
                end_hour=settings.daemon.active_end_hour,
            ):
                result.skipped_quiet_hours += 1
                break

            # Build action list per candidate via coin-flip
            actions: list[str] = []
            if random.random() < self._follow_prob:
                actions.append("follow")
            if random.random() < self._like_prob:
                actions.append("like")

            # Randomize action order within candidate
            random.shuffle(actions)

            for action in actions:
                # Idle browsing before each action for natural behavior
                page = context.pages[0] if context.pages else await context.new_page()
                await human_scroll(page, direction="down")
                await random_pause(2.0, 5.0)

                if action == "follow":
                    await self._do_follow(
                        result,
                        repository,
                        context,
                        tracker,
                        settings,
                        tweet_id,
                        username,
                    )
                elif action == "like":
                    await self._do_like(
                        result,
                        repository,
                        context,
                        tracker,
                        settings,
                        tweet_id,
                        username,
                    )

                if result.emergency_halt:
                    break

            if result.emergency_halt:
                break

        logger.info(
            "nurture_complete",
            follows=result.follows_sent,
            likes=result.likes_sent,
            errors=result.errors,
        )
        return result

    async def _do_follow(
        self,
        result: NurtureResult,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
        tweet_id: str,
        username: str,
    ) -> None:
        """Attempt to follow a user with all safety checks."""
        # Daily limit
        if not self._follow_limiter.can_act():
            result.skipped_daily_limit_follow += 1
            return

        # DB deduplication
        if repository.is_user_followed(username):
            result.already_followed += 1
            return

        try:
            outcome = await _follow_user_via_playwright(context, username)
        except NurtureRateLimitError:
            result.emergency_halt = True
            result.errors += 1
            result.error_details.append(f"{username}: follow_rate_limit")
            tracker.record_error("nurture_follow", "Rate limit detected")
            logger.warning("nurture_emergency_halt", action="follow", username=username)
            return
        except Exception as exc:
            result.errors += 1
            result.error_details.append(f"{username}: follow: {exc}")
            tracker.record_error("nurture_follow", str(exc))
            logger.error("nurture_follow_error", username=username, error=str(exc))
            return

        if outcome == FollowOutcome.SUCCESS:
            self._follow_limiter.record()
            repository.record_nurture_action("follow", tweet_id, username)
            tracker.record_follow(tweet_id, username)
            result.follows_sent += 1
            logger.info("nurture_followed", username=username)
        elif outcome == FollowOutcome.ALREADY_FOLLOWING:
            result.already_followed += 1

        # Human-like delay between actions
        await random_pause(
            settings.delays.action_min_seconds,
            settings.delays.action_max_seconds,
        )

    async def _do_like(
        self,
        result: NurtureResult,
        repository: Repository,
        context: BrowserContext,
        tracker: ActionTracker,
        settings: Settings,
        tweet_id: str,
        username: str,
    ) -> None:
        """Attempt to like a tweet with all safety checks."""
        # Daily limit
        if not self._like_limiter.can_act():
            result.skipped_daily_limit_like += 1
            return

        # DB deduplication
        if repository.is_tweet_liked(tweet_id):
            result.already_liked += 1
            return

        tweet_url = f"https://x.com/{username}/status/{tweet_id}"

        try:
            outcome = await _like_tweet_via_playwright(context, tweet_url)
        except NurtureRateLimitError:
            result.emergency_halt = True
            result.errors += 1
            result.error_details.append(f"{tweet_id}: like_rate_limit")
            tracker.record_error("nurture_like", "Rate limit detected")
            logger.warning("nurture_emergency_halt", action="like", tweet_id=tweet_id)
            return
        except Exception as exc:
            result.errors += 1
            result.error_details.append(f"{tweet_id}: like: {exc}")
            tracker.record_error("nurture_like", str(exc))
            logger.error("nurture_like_error", tweet_id=tweet_id, error=str(exc))
            return

        if outcome == LikeOutcome.SUCCESS:
            self._like_limiter.record()
            repository.record_nurture_action("like", tweet_id, username)
            tracker.record_like(tweet_id, username)
            result.likes_sent += 1
            logger.info("nurture_liked", tweet_id=tweet_id)
        elif outcome == LikeOutcome.ALREADY_LIKED:
            result.already_liked += 1

        # Human-like delay between actions
        await random_pause(
            settings.delays.action_min_seconds,
            settings.delays.action_max_seconds,
        )


# ---------------------------------------------------------------------------
# Playwright automation helpers
# ---------------------------------------------------------------------------


async def _follow_user_via_playwright(
    context: BrowserContext,
    username: str,
) -> FollowOutcome:
    """Navigate to a user's profile and click Follow.

    Parameters
    ----------
    context:
        Authenticated Playwright browser context.
    username:
        X username to follow (without ``@``).

    Returns
    -------
    FollowOutcome
        Result of the follow attempt.

    Raises
    ------
    NurtureRateLimitError
        When X rate-limits or restricts the account.
    """
    profile_url = f"https://x.com/{username}"
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        await page.goto(profile_url, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(3.0, 5.5)

        # Check for restriction
        page_content = await page.content()
        if detect_restriction(page_content):
            raise NurtureRateLimitError("Account restricted during follow")

        # Check if already following (unfollow button present)
        unfollow_btn = await page.query_selector(PROFILE_UNFOLLOW_BUTTON)
        if unfollow_btn:
            logger.info("nurture_already_following", username=username)
            return FollowOutcome.ALREADY_FOLLOWING

        # Find and click Follow button
        follow_btn = await page.wait_for_selector(PROFILE_FOLLOW_BUTTON, timeout=10_000)
        if follow_btn is None:
            logger.warning("nurture_follow_btn_not_found", username=username)
            return FollowOutcome.ERROR

        await random_mouse_move(page)
        await follow_btn.click()
        await random_pause(2.0, 4.0)

        # Verify follow succeeded (unfollow button should appear)
        unfollow_check = await page.query_selector(PROFILE_UNFOLLOW_BUTTON)
        if unfollow_check:
            return FollowOutcome.SUCCESS

        # Button may not have changed yet -- still count as success
        return FollowOutcome.SUCCESS

    except NurtureRateLimitError:
        raise
    except Exception as exc:
        logger.error("follow_playwright_error", username=username, error=str(exc))
        raise


async def _like_tweet_via_playwright(
    context: BrowserContext,
    tweet_url: str,
) -> LikeOutcome:
    """Navigate to a tweet and click Like.

    Parameters
    ----------
    context:
        Authenticated Playwright browser context.
    tweet_url:
        Full URL of the tweet to like.

    Returns
    -------
    LikeOutcome
        Result of the like attempt.

    Raises
    ------
    NurtureRateLimitError
        When X rate-limits or restricts the account.
    """
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        await page.goto(tweet_url, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(2.0, 4.5)

        # Check for restriction
        page_content = await page.content()
        if detect_restriction(page_content):
            raise NurtureRateLimitError("Account restricted during like")

        # Check if already liked (unlike button present)
        unlike_btn = await page.query_selector(UNLIKE_BUTTON)
        if unlike_btn:
            logger.info("nurture_already_liked", url=tweet_url)
            return LikeOutcome.ALREADY_LIKED

        # Find and click Like button
        like_btn = await page.wait_for_selector(LIKE_BUTTON, timeout=10_000)
        if like_btn is None:
            logger.warning("nurture_like_btn_not_found", url=tweet_url)
            return LikeOutcome.ERROR

        await random_mouse_move(page)
        await like_btn.click()
        await random_pause(1.5, 3.0)

        # Verify: unlike button should now be present
        unlike_check = await page.query_selector(UNLIKE_BUTTON)
        if unlike_check:
            return LikeOutcome.SUCCESS

        return LikeOutcome.SUCCESS

    except NurtureRateLimitError:
        raise
    except Exception as exc:
        logger.error("like_playwright_error", url=tweet_url, error=str(exc))
        raise


class NurtureRateLimitError(Exception):
    """Raised when X rate-limits or restricts the account during nurture."""
