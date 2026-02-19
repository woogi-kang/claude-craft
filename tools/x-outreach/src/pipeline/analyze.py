"""Analyze pipeline -- classify collected tweets via Claude.

Processes all tweets with status ``collected``, calls the AI classifier,
and updates each tweet with its classification result.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.ai.classifier import TweetClassifier
from src.db.repository import Repository
from src.utils.logger import get_logger

logger = get_logger("analyze")


@dataclass
class AnalyzeResult:
    """Summary of the analyze pipeline run."""

    total_processed: int = 0
    needs_help: int = 0
    seeking_info: int = 0
    irrelevant: int = 0
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
        - ``classification`` (needs_help / seeking_info / irrelevant)
        - ``confidence`` score
        - ``classification_rationale``
        - ``template_category`` (A-G)
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
                    tweet_content=tweet["content"],
                    author_username=tweet["author_username"],
                    author_bio=tweet.get("author_bio", ""),
                    follower_count=tweet.get("author_follower_count", 0),
                    following_count=tweet.get("author_following_count", 0),
                    likes=tweet.get("likes", 0),
                    retweets=tweet.get("retweets", 0),
                    replies=tweet.get("replies", 0),
                )

                repository.update_tweet_status(
                    tweet["tweet_id"],
                    status="analyzed",
                    classification=classification.classification,
                    confidence=classification.confidence,
                    classification_rationale=classification.rationale,
                    template_category=classification.template_category,
                )

                result.total_processed += 1
                if classification.classification == "needs_help":
                    result.needs_help += 1
                elif classification.classification == "seeking_info":
                    result.seeking_info += 1
                else:
                    result.irrelevant += 1

            except Exception as exc:
                result.errors += 1
                logger.error(
                    "analyze_tweet_error",
                    tweet_id=tweet["tweet_id"],
                    error=str(exc),
                )

        logger.info(
            "analyze_complete",
            total=result.total_processed,
            needs_help=result.needs_help,
            seeking_info=result.seeking_info,
            irrelevant=result.irrelevant,
            errors=result.errors,
        )
        return result
