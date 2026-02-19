"""Reply pipeline -- post replies to classified tweets via X API.

Uses tweepy with X API v2 Free tier to reply to tweets classified as
``needs_help`` or ``seeking_info`` with sufficient confidence. Enforces
rate limits (17 writes/15 min, 1500/month) and quiet hours (23:00-08:00 JST).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import tweepy

from src.ai.content_gen import ContentGenerator, ContentGenerationError
from src.config import Settings
from src.db.repository import Repository
from src.knowledge.templates import TemplateSelector
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.track import ActionTracker
from src.utils.logger import get_logger
from src.utils.rate_limiter import MonthlyBudgetTracker, TokenBucketLimiter
from src.utils.time_utils import is_active_hours

logger = get_logger("reply")

# X API Free tier limits
_X_API_WRITES_PER_15MIN = 17
_X_API_MONTHLY_LIMIT = 1500
_CONSERVATION_THRESHOLD = 1200  # 80% of monthly limit


@dataclass
class ReplyResult:
    """Summary of a reply pipeline run."""

    total_candidates: int = 0
    replies_sent: int = 0
    skipped_quiet_hours: int = 0
    skipped_rate_limit: int = 0
    skipped_conservation: int = 0
    skipped_category_f: int = 0
    skipped_low_confidence: int = 0
    skipped_max_thread: int = 0
    errors: int = 0
    error_details: list[str] = field(default_factory=list)


class ReplyPipeline:
    """Post replies to classified tweets via X API Free tier.

    Parameters
    ----------
    content_gen:
        Content generator for creating reply text.
    knowledge_base:
        Treatment knowledge base for context enrichment.
    template_selector:
        Template selector for rotation tracking.
    api_rate_limiter:
        Token bucket limiter for 17 writes/15 min.
    monthly_budget:
        Monthly budget tracker for 1500 tweets/month.
    max_thread_replies:
        Maximum replies per conversation thread.
    """

    def __init__(
        self,
        content_gen: ContentGenerator,
        knowledge_base: TreatmentKnowledgeBase,
        template_selector: TemplateSelector | None = None,
        api_rate_limiter: TokenBucketLimiter | None = None,
        monthly_budget: MonthlyBudgetTracker | None = None,
        max_thread_replies: int = 3,
    ) -> None:
        self._content_gen = content_gen
        self._kb = knowledge_base
        self._template_selector = template_selector or TemplateSelector()
        self._api_limiter = api_rate_limiter or TokenBucketLimiter(
            max_tokens=_X_API_WRITES_PER_15MIN,
            refill_seconds=900,  # 15 minutes
        )
        self._monthly_budget = monthly_budget or MonthlyBudgetTracker(
            monthly_limit=_X_API_MONTHLY_LIMIT,
        )
        self._max_thread_replies = max_thread_replies

    async def run(
        self,
        repository: Repository,
        tracker: ActionTracker,
        settings: Settings,
    ) -> ReplyResult:
        """Process all 'analyzed' tweets that are actionable.

        Applies the following filters before replying:
        - R4.1: Only needs_help and seeking_info with confidence >= 0.7
        - R4.4: Conservation mode at 80% monthly limit
        - R4.5: Max 3 replies per conversation thread
        - R4.6: No replies between 23:00-08:00 JST

        Parameters
        ----------
        repository:
            Database repository for tweet lookup and updates.
        tracker:
            Action tracker for audit logging.
        settings:
            Application settings with API credentials.

        Returns
        -------
        ReplyResult
            Aggregate statistics for the run.
        """
        result = ReplyResult()

        # R4.6: Check quiet hours
        if not is_active_hours(start_hour=8, end_hour=22):
            logger.info("reply_quiet_hours")
            return result

        tweets = repository.get_tweets_by_status("analyzed")
        if not tweets:
            logger.info("reply_no_candidates")
            return result

        # Filter to actionable tweets
        candidates = [
            t for t in tweets
            if t.get("classification") in ("needs_help", "seeking_info")
            and (t.get("confidence") or 0.0) >= 0.7
        ]
        result.total_candidates = len(candidates)

        if not candidates:
            logger.info("reply_no_actionable_tweets")
            return result

        # Build tweepy client
        client = _build_tweepy_client(settings)

        logger.info("reply_start", candidates=len(candidates))

        for tweet in candidates:
            tweet_id = tweet["tweet_id"]
            username = tweet["author_username"]
            classification = tweet["classification"]
            template_category = tweet.get("template_category", "B")
            confidence = tweet.get("confidence", 0.0)

            # R4.1: Confidence check (redundant but explicit)
            if confidence < 0.7:
                result.skipped_low_confidence += 1
                continue

            # Skip category F (clinic accounts)
            if template_category == "F":
                result.skipped_category_f += 1
                repository.update_tweet_status(
                    tweet_id, status="skipped", dm_skip_reason="category_f"
                )
                continue

            # R4.6: Re-check quiet hours (loop may span midnight)
            if not is_active_hours(start_hour=8, end_hour=22):
                result.skipped_quiet_hours += 1
                break

            # R4.4: Conservation mode
            if self._monthly_budget.used >= _CONSERVATION_THRESHOLD:
                if classification != "needs_help":
                    result.skipped_conservation += 1
                    logger.info(
                        "reply_conservation_skip",
                        tweet_id=tweet_id,
                        classification=classification,
                    )
                    continue

            # Check monthly budget
            if not self._monthly_budget.can_use():
                result.skipped_rate_limit += 1
                logger.warning("reply_monthly_budget_exhausted")
                break

            # R4.5: Thread reply limit
            thread_count = _count_thread_replies(repository, username)
            if thread_count >= self._max_thread_replies:
                result.skipped_max_thread += 1
                logger.info(
                    "reply_thread_limit",
                    tweet_id=tweet_id,
                    username=username,
                    thread_count=thread_count,
                )
                continue

            # Wait for API rate limit token
            await self._api_limiter.acquire()

            # Build treatment context
            treatment_ctx = _build_treatment_context(
                tweet["content"], self._kb
            )

            # Generate reply content
            try:
                reply_text = await self._content_gen.generate_reply(
                    tweet_content=tweet["content"],
                    author_username=username,
                    template_category=template_category,
                    classification=classification,
                    treatment_context=treatment_ctx,
                )
            except ContentGenerationError as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: content_gen: {exc}")
                tracker.record_error("reply_content_gen", str(exc))
                continue

            # Post reply via X API
            try:
                response = client.create_tweet(
                    text=reply_text,
                    in_reply_to_tweet_id=tweet_id,
                )
                reply_tweet_id = (
                    response.data["id"] if response.data else None
                )
                self._monthly_budget.use()

                # R4.7: Update tweet record
                repository.update_tweet_status(
                    tweet_id,
                    status="replied",
                    reply_content=reply_text,
                    reply_tweet_id=reply_tweet_id,
                    reply_timestamp=datetime.utcnow().isoformat(),
                )
                tracker.record_reply(tweet_id, username)
                result.replies_sent += 1

                logger.info(
                    "reply_sent",
                    tweet_id=tweet_id,
                    username=username,
                    reply_id=reply_tweet_id,
                    monthly_used=self._monthly_budget.used,
                )

            except tweepy.TooManyRequests:
                result.skipped_rate_limit += 1
                logger.warning("reply_rate_limited", tweet_id=tweet_id)
                break

            except tweepy.Forbidden as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: forbidden: {exc}")
                logger.error(
                    "reply_forbidden", tweet_id=tweet_id, error=str(exc)
                )
                # Emergency halt: possible account restriction
                logger.warning("reply_emergency_halt", reason="forbidden_error")
                break

            except Exception as exc:
                result.errors += 1
                result.error_details.append(f"{tweet_id}: {exc}")
                tracker.record_error("reply_post", str(exc))
                logger.error(
                    "reply_error", tweet_id=tweet_id, error=str(exc)
                )

        logger.info(
            "reply_complete",
            sent=result.replies_sent,
            candidates=result.total_candidates,
            errors=result.errors,
        )
        return result


def _build_tweepy_client(settings: Settings) -> tweepy.Client:
    """Create a tweepy Client with X API v2 credentials.

    Parameters
    ----------
    settings:
        Application settings containing API keys.

    Returns
    -------
    tweepy.Client
        Authenticated tweepy client.
    """
    return tweepy.Client(
        consumer_key=settings.x_api_key,
        consumer_secret=settings.x_api_secret,
        access_token=settings.x_access_token,
        access_token_secret=settings.x_access_token_secret,
    )


def _count_thread_replies(repository: Repository, username: str) -> int:
    """Count how many replies we have already sent to this user.

    Parameters
    ----------
    repository:
        Database repository.
    username:
        The target user's username.

    Returns
    -------
    int
        Number of existing replies to this user.
    """
    conn = repository._get_conn()
    cursor = conn.execute(
        "SELECT COUNT(*) as cnt FROM tweets "
        "WHERE author_username = ? AND status IN ('replied', 'dm_sent')",
        (username,),
    )
    row = cursor.fetchone()
    return row["cnt"] if row else 0


def _build_treatment_context(
    tweet_content: str, kb: TreatmentKnowledgeBase
) -> str:
    """Extract treatment context from tweet content using the knowledge base.

    Scans the tweet for known Japanese treatment terms and builds a
    context string with Korean equivalents and pricing data.

    Parameters
    ----------
    tweet_content:
        The tweet text to scan.
    kb:
        Treatment knowledge base.

    Returns
    -------
    str
        Treatment context string, or empty string if no matches.
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
