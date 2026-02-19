"""Respond pipeline stage -- generate response text."""

from __future__ import annotations

from dataclasses import dataclass

from src.ai.classifier import ClassificationResult
from src.ai.router import LLMRouter
from src.knowledge.templates import TemplateEngine
from src.pipeline.classify import ClassifyResult
from src.utils.logger import get_logger

logger = get_logger("pipeline.respond")


@dataclass
class RespondResult:
    """Result from the respond stage."""

    text: str
    provider: str  # "template", "claude", "openai", "ollama", "fallback"
    template_id: str | None = None
    classification: str | None = None
    confidence: float | None = None


class RespondPipeline:
    """Generate response based on classification result.

    Parameters
    ----------
    template_engine:
        Template engine for FAQ/greeting responses.
    llm_router:
        Multi-LLM router for complex responses.
    """

    def __init__(self, template_engine: TemplateEngine, llm_router: LLMRouter) -> None:
        self._templates = template_engine
        self._router = llm_router

    async def run(
        self,
        message_text: str,
        classify_result: ClassifyResult,
        conversation_history: list[dict[str, str]],
    ) -> RespondResult:
        """Generate a response for the classified message."""

        # Case 1: FAQ match -> use template
        if classify_result.faq_match:
            match = classify_result.faq_match

            if match.source == "greeting":
                template = self._templates.get_greeting_response(match.category)
            else:
                template = self._templates.get_faq_response(match.category)

            if template:
                logger.info(
                    "template_response",
                    category=match.category,
                    template_id=template.id,
                )
                return RespondResult(
                    text=template.text,
                    provider="template",
                    template_id=template.id,
                    classification="faq",
                    confidence=match.confidence,
                )

        # Case 2: Classification available -> route to LLM or template
        if classify_result.classification:
            cls = classify_result.classification

            # Off-topic -> redirect template
            if cls.intent == "off_topic":
                template = self._templates.get_redirect_response()
                if template:
                    return RespondResult(
                        text=template.text,
                        provider="template",
                        template_id=template.id,
                        classification="off_topic",
                        confidence=cls.confidence,
                    )

            # Greeting -> greeting template
            if cls.intent == "greeting":
                template = self._templates.get_greeting_response("hello")
                if template:
                    return RespondResult(
                        text=template.text,
                        provider="template",
                        template_id=template.id,
                        classification="greeting",
                        confidence=cls.confidence,
                    )

            # Spam -> skip (return empty)
            if cls.intent == "spam":
                logger.info("spam_skipped")
                return RespondResult(
                    text="",
                    provider="skip",
                    classification="spam",
                    confidence=cls.confidence,
                )

            # Complex / complaint -> route to LLM
            llm_response = await self._router.route(
                message=message_text,
                classification=cls,
                conversation_history=conversation_history,
            )

            return RespondResult(
                text=llm_response.text,
                provider=llm_response.provider,
                classification=cls.intent,
                confidence=cls.confidence,
            )

        # Fallback: no classification, no FAQ match
        logger.warning("no_classification_fallback")
        return RespondResult(
            text="\uac10\uc0ac\ud569\ub2c8\ub2e4. \ub2f4\ub2f9\uc790\uac00 \uace7 \ub2f5\ubcc0\ub4dc\ub9ac\uaca0\uc2b5\ub2c8\ub2e4.",
            provider="fallback",
        )
