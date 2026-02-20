"""Tweet classifier using Gemini API via shared LLM client.

Classifies tweets into 5 intent categories (hospital / price / procedure /
complaint / review) with a keyword pre-filter and LLM decision.
Low-confidence classifications are automatically rejected.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from outreach_shared.ai.llm_client import LLMClient, create_llm_client
from outreach_shared.utils.logger import get_logger

from src.ai.keywords import KeywordMatch, match_category
from src.ai.prompts import build_classification_system_prompt, build_classification_user_prompt

logger = get_logger("classifier")

# Valid intent categories
VALID_INTENTS = frozenset({"hospital", "price", "procedure", "complaint", "review"})


@dataclass
class ClassificationResult:
    """Result of classifying a single tweet."""

    intent_type: str  # hospital/price/procedure/complaint/review
    confidence: float  # 0.0 - 1.0
    rationale: str
    llm_decision: bool  # True if outreach is recommended
    keyword_intent: str | None = None  # Category from keyword pre-filter

    @property
    def is_actionable(self) -> bool:
        """Return ``True`` if this classification warrants outreach."""
        return self.llm_decision

    # Backward compatibility aliases
    @property
    def classification(self) -> str:
        return self.intent_type

    @property
    def template_category(self) -> str | None:
        return self.intent_type if self.llm_decision else None


class TweetClassifier:
    """Classify tweets using keyword pre-filter + Gemini LLM.

    Parameters
    ----------
    api_key:
        Gemini API key.
    model:
        LLM model identifier.
    confidence_threshold:
        Minimum confidence to accept an LLM classification.
    domain_context:
        Treatment knowledge context string to embed in the system prompt.
    provider:
        LLM provider name (default: ``"gemini"``).
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gemini-2.0-flash",
        confidence_threshold: float = 0.7,
        domain_context: str = "",
        provider: str = "gemini",
    ) -> None:
        self._llm: LLMClient = create_llm_client(provider, api_key, model=model)
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

        First applies keyword pre-filter. If no keyword match, calls the
        LLM.  Low-confidence LLM results are rejected.
        """
        # Step 1: Keyword pre-filter
        kw_match = match_category(tweet_content)

        if kw_match.excluded:
            logger.info(
                "keyword_excluded",
                username=author_username,
                keyword=kw_match.keyword,
            )
            return ClassificationResult(
                intent_type="review",
                confidence=1.0,
                rationale=f"Excluded by keyword filter: {kw_match.keyword}",
                llm_decision=False,
                keyword_intent=None,
            )

        # Step 2: LLM classification
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
            response = await self._llm.generate(
                user_prompt,
                system=self._system_prompt,
                temperature=0.3,
                max_tokens=300,
                json_mode=True,
            )

            result = self._parse_response(response.text, kw_match)

            # Enforce confidence threshold
            if result.confidence < self._confidence_threshold:
                logger.info(
                    "classification_low_confidence",
                    tweet_snippet=tweet_content[:50],
                    original=result.intent_type,
                    confidence=result.confidence,
                )
                result = ClassificationResult(
                    intent_type=result.intent_type,
                    confidence=result.confidence,
                    rationale=f"Low confidence ({result.confidence:.2f}). {result.rationale}",
                    llm_decision=False,
                    keyword_intent=kw_match.category if kw_match.matched else None,
                )

            logger.info(
                "classification_done",
                username=author_username,
                intent=result.intent_type,
                confidence=result.confidence,
                llm_decision=result.llm_decision,
                keyword_intent=result.keyword_intent,
            )
            return result

        except Exception as exc:
            logger.error(
                "classification_error",
                error=str(exc)[:200],
                username=author_username,
            )
            return ClassificationResult(
                intent_type=kw_match.category or "review",
                confidence=0.0,
                rationale=f"Classification error: {exc}",
                llm_decision=False,
                keyword_intent=kw_match.category if kw_match.matched else None,
            )

    def _parse_response(
        self,
        raw_text: str,
        kw_match: KeywordMatch,
    ) -> ClassificationResult:
        """Parse the JSON response from the LLM.

        Handles potential markdown wrapping and malformed JSON gracefully.
        """
        text = raw_text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("classification_parse_error", raw=raw_text[:200])
            return ClassificationResult(
                intent_type=kw_match.category or "review",
                confidence=0.0,
                rationale=f"Failed to parse response: {raw_text[:100]}",
                llm_decision=False,
                keyword_intent=kw_match.category if kw_match.matched else None,
            )

        intent_type = data.get("intent_type", "review")
        if intent_type not in VALID_INTENTS:
            intent_type = "review"

        confidence = float(data.get("confidence", 0.0))
        confidence = max(0.0, min(1.0, confidence))

        llm_decision = bool(data.get("llm_decision", False))

        return ClassificationResult(
            intent_type=intent_type,
            confidence=confidence,
            rationale=data.get("rationale", ""),
            llm_decision=llm_decision,
            keyword_intent=kw_match.category if kw_match.matched else None,
        )
