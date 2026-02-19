"""Tweet classifier using Claude API.

Classifies tweets into needs_help / seeking_info / irrelevant with a
confidence score and rationale.  Low-confidence classifications are
automatically forced to ``irrelevant``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

import anthropic

from src.ai.prompts import build_classification_system_prompt, build_classification_user_prompt
from src.utils.logger import get_logger

logger = get_logger("classifier")


@dataclass
class ClassificationResult:
    """Result of classifying a single tweet."""

    classification: str  # "needs_help" | "seeking_info" | "irrelevant"
    confidence: float  # 0.0 - 1.0
    rationale: str
    template_category: str | None  # A-G or None

    @property
    def is_actionable(self) -> bool:
        """Return ``True`` if this classification warrants outreach."""
        return self.classification in ("needs_help", "seeking_info")


class TweetClassifier:
    """Classify tweets using Claude via the Anthropic SDK.

    Parameters
    ----------
    api_key:
        Anthropic API key.
    model:
        Claude model identifier.
    confidence_threshold:
        Minimum confidence to accept a non-irrelevant classification.
    domain_context:
        Treatment knowledge context string to embed in the system prompt.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        confidence_threshold: float = 0.7,
        domain_context: str = "",
    ) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model
        self._confidence_threshold = confidence_threshold
        self._system_prompt = build_classification_system_prompt(domain_context)

    async def classify(
        self,
        tweet_content: str,
        author_username: str,
        author_bio: str = "",
        follower_count: int = 0,
        following_count: int = 0,
        likes: int = 0,
        retweets: int = 0,
        replies: int = 0,
    ) -> ClassificationResult:
        """Classify a single tweet.

        If the model returns confidence below the threshold, the
        classification is forced to ``irrelevant`` regardless of the
        model's choice.
        """
        user_prompt = build_classification_user_prompt(
            tweet_content=tweet_content,
            author_username=author_username,
            author_bio=author_bio,
            follower_count=follower_count,
            following_count=following_count,
            likes=likes,
            retweets=retweets,
            replies=replies,
        )

        try:
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=300,
                system=self._system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            raw_text = response.content[0].text.strip()
            result = self._parse_response(raw_text)

            # Enforce confidence threshold
            if result.confidence < self._confidence_threshold:
                logger.info(
                    "classification_low_confidence",
                    tweet_content=tweet_content[:80],
                    original=result.classification,
                    confidence=result.confidence,
                )
                result = ClassificationResult(
                    classification="irrelevant",
                    confidence=result.confidence,
                    rationale=f"Low confidence ({result.confidence:.2f}). Original: {result.classification}",
                    template_category=None,
                )

            logger.info(
                "classification_done",
                username=author_username,
                classification=result.classification,
                confidence=result.confidence,
                template=result.template_category,
            )
            return result

        except Exception as exc:
            logger.error("classification_error", error=str(exc), username=author_username)
            return ClassificationResult(
                classification="irrelevant",
                confidence=0.0,
                rationale=f"Classification error: {exc}",
                template_category=None,
            )

    def _parse_response(self, raw_text: str) -> ClassificationResult:
        """Parse the JSON response from Claude.

        Handles potential markdown wrapping and malformed JSON gracefully.
        """
        # Strip markdown code fences if present
        text = raw_text
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first and last lines (fences)
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("classification_parse_error", raw=raw_text[:200])
            return ClassificationResult(
                classification="irrelevant",
                confidence=0.0,
                rationale=f"Failed to parse response: {raw_text[:100]}",
                template_category=None,
            )

        classification = data.get("classification", "irrelevant")
        if classification not in ("needs_help", "seeking_info", "irrelevant"):
            classification = "irrelevant"

        confidence = float(data.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))

        return ClassificationResult(
            classification=classification,
            confidence=confidence,
            rationale=data.get("rationale", ""),
            template_category=data.get("template_category"),
        )
