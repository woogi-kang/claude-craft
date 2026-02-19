"""Message intent classifier using LLM."""

from __future__ import annotations

import json
from dataclasses import dataclass

from src.ai.prompts import CLASSIFIER_SYSTEM_PROMPT
from src.utils.logger import get_logger

logger = get_logger("classifier")


@dataclass
class ClassificationResult:
    """Result of message classification."""

    intent: str
    confidence: float
    suggested_llm: str | None
    rationale: str


class MessageClassifier:
    """Classify incoming messages using Claude API.

    Parameters
    ----------
    api_key:
        Anthropic API key.
    model:
        Model to use for classification.
    confidence_threshold:
        Minimum confidence to accept classification.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        confidence_threshold: float = 0.7,
    ) -> None:
        self._api_key = api_key
        self._model = model
        self._threshold = confidence_threshold
        self._client = None

    def _ensure_client(self):
        if self._client is None:
            from anthropic import Anthropic

            self._client = Anthropic(api_key=self._api_key)

    async def classify(self, message: str) -> ClassificationResult:
        """Classify a message's intent.

        Falls back to 'complex' with Claude suggestion if classification fails.

        Parameters
        ----------
        message:
            The user message to classify.

        Returns
        -------
        ClassificationResult
            Classification with intent, confidence, and suggested LLM.
        """
        try:
            self._ensure_client()

            response = self._client.messages.create(
                model=self._model,
                max_tokens=200,
                temperature=0.0,
                system=CLASSIFIER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": message}],
            )

            text = response.content[0].text if response.content else ""

            # Parse JSON response, handling potential markdown code block wrapping
            clean = text.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1] if "\n" in clean else clean[3:]
                clean = clean.rsplit("```", 1)[0]

            data = json.loads(clean)

            result = ClassificationResult(
                intent=data.get("intent", "complex"),
                confidence=float(data.get("confidence", 0.5)),
                suggested_llm=data.get("suggested_llm"),
                rationale=data.get("rationale", ""),
            )

            # If confidence below threshold, default to complex
            if result.confidence < self._threshold:
                logger.info(
                    "low_confidence_fallback",
                    confidence=result.confidence,
                    original_intent=result.intent,
                )
                result.intent = "complex"
                result.suggested_llm = "claude"

            logger.info(
                "classified",
                intent=result.intent,
                confidence=result.confidence,
                suggested_llm=result.suggested_llm,
            )
            return result

        except Exception as exc:
            logger.error("classification_error", error=str(exc))
            return ClassificationResult(
                intent="complex",
                confidence=0.5,
                suggested_llm="claude",
                rationale=f"Classification failed: {exc}",
            )
