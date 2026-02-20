"""Analyze pipeline -- classify collected tweets via LLM.

Processes all tweets with status ``collected``, calls the AI classifier,
and updates each tweet with its classification result.  Uses the 5-category
intent system (hospital/price/procedure/complaint/review) with keyword
pre-filtering and llm_decision boolean.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from outreach_shared.utils.logger import get_logger

from src.ai.classifier import TweetClassifier
from src.db.repository import Repository

logger = get_logger("analyze")


@dataclass
class AnalyzeResult:
    """Summary of the analyze pipeline run."""

    total_processed: int = 0
    approved: int = 0
    rejected: int = 0
    by_intent: dict[str, int] = field(default_factory=dict)
    errors: int = 0


class AnalyzePipeline:
    """Classify collected tweets using the AI classifier.

    Parameters
    ----------
    classifier:
        A configured ``TweetClassifier`` instance.
    """

    def __init__(self, classifier: TweetClassifier) -> None:
        self._classifier = classifier

    async def run(self, repository: Repository) -> AnalyzeResult:
        """Process all ``collected`` tweets through classification.

        Each tweet is classified and updated in-place with:
        - ``intent_type`` (hospital/price/procedure/complaint/review)
        - ``llm_decision`` (True = actionable)
        - ``keyword_intent`` (from keyword pre-filter, may be None)
        - ``llm_rationale`` (explanation text)
        - ``status`` set to ``analyzed``

        Returns
        -------
        AnalyzeResult
            Aggregate statistics for the run.
        """
        result = AnalyzeResult()
        tweets = repository.get_tweets_by_status("collected")

        if not tweets:
            logger.info("analyze_no_tweets")
            return result

        logger.info("analyze_start", count=len(tweets))

        for tweet in tweets:
            try:
                classification = await self._classifier.classify(
                    tweet_content=tweet.get("contents", ""),
                    author_username=tweet.get("username", ""),
                    author_bio=tweet.get("author_bio", ""),
                    follower_count=tweet.get("author_followers", 0),
                    following_count=0,
                    likes=tweet.get("likes_count", 0),
                    retweets=tweet.get("retweets_count", 0),
                    replies=tweet.get("comments_count", 0),
                )

                repository.update_tweet_status(
                    tweet["post_id"],
                    status="analyzed",
                    intent_type=classification.intent_type,
                    llm_decision=classification.llm_decision,
                    keyword_intent=classification.keyword_intent,
                    llm_rationale=classification.rationale,
                )

                result.total_processed += 1
                intent = classification.intent_type
                result.by_intent[intent] = result.by_intent.get(intent, 0) + 1

                if classification.llm_decision:
                    result.approved += 1
                else:
                    result.rejected += 1

            except Exception as exc:
                result.errors += 1
                logger.error(
                    "analyze_tweet_error",
                    tweet_id=tweet.get("post_id", "unknown"),
                    error=str(exc),
                )

        logger.info(
            "analyze_complete",
            total=result.total_processed,
            approved=result.approved,
            rejected=result.rejected,
            by_intent=result.by_intent,
            errors=result.errors,
        )
        return result
