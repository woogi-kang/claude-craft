"""Classify pipeline stage -- determine message intent."""

from __future__ import annotations

from dataclasses import dataclass

from src.ai.classifier import ClassificationResult, MessageClassifier
from src.knowledge.faq_matcher import FAQMatch, FAQMatcher
from src.utils.logger import get_logger

logger = get_logger("pipeline.classify")


@dataclass
class ClassifyResult:
    """Result from the classify stage."""

    faq_match: FAQMatch | None
    classification: ClassificationResult | None
    used_local: bool  # True if FAQ matcher handled it


class ClassifyPipeline:
    """Classify message intent using local FAQ match first, then LLM.

    Parameters
    ----------
    faq_matcher:
        Local FAQ pattern matcher.
    classifier:
        LLM-based message classifier.
    use_local_first:
        Try local FAQ match before LLM classification.
    """

    def __init__(
        self,
        faq_matcher: FAQMatcher,
        classifier: MessageClassifier,
        use_local_first: bool = True,
    ) -> None:
        self._faq = faq_matcher
        self._classifier = classifier
        self._local_first = use_local_first

    async def run(self, message_text: str) -> ClassifyResult:
        """Classify a single message."""

        # Try local FAQ match first
        if self._local_first:
            faq_match = self._faq.match(message_text)
            if faq_match:
                logger.info(
                    "faq_matched",
                    category=faq_match.category,
                    confidence=faq_match.confidence,
                    source=faq_match.source,
                )
                return ClassifyResult(
                    faq_match=faq_match, classification=None, used_local=True
                )

        # Fall through to LLM classification
        classification = await self._classifier.classify(message_text)

        # Check if LLM identified it as FAQ
        faq_match = None
        if classification.intent == "faq":
            faq_match = self._faq.match(message_text)

        return ClassifyResult(
            faq_match=faq_match, classification=classification, used_local=False
        )
