"""Content generation via shared LLM client (Codex CLI default).

Generates personalised reply and DM content based on tweet classification,
intent categories, and treatment knowledge. All output is in natural
Japanese matching the @ask.nandemo voice.
"""

from __future__ import annotations

import re

from outreach_shared.ai.llm_client import LLMClient, create_llm_client
from outreach_shared.utils.logger import get_logger

from src.ai.prompts import (
    CASUAL_POST_SYSTEM_PROMPT,
    DM_SYSTEM_PROMPT,
    KNOWLEDGE_POST_SYSTEM_PROMPT,
    REPLY_SYSTEM_PROMPT,
)

logger = get_logger("content_gen")


def _build_reply_user_prompt(
    tweet_content: str,
    author_username: str,
    intent_type: str,
    treatment_context: str,
) -> str:
    """Build the user prompt for reply generation."""
    parts = [
        f"Tweet:\n<tweet>\n{tweet_content}\n</tweet>",
        f"Author: @{author_username}",
        f"Intent category: {intent_type}",
    ]
    if treatment_context:
        parts.append(f"\nRelevant treatment data:\n{treatment_context}")
    return "\n".join(parts)


def _build_dm_user_prompt(
    tweet_content: str,
    author_username: str,
    intent_type: str,
    reply_content: str,
    treatment_context: str,
    previous_dm: str,
) -> str:
    """Build the user prompt for DM generation."""
    parts = [
        f"Tweet they posted:\n<tweet>\n{tweet_content}\n</tweet>",
        f"Author: @{author_username}",
        f"Their concern category: {intent_type}",
    ]
    if reply_content:
        parts.append(f"Our reply to their tweet: {reply_content}")
    if treatment_context:
        parts.append(f"\nRelevant treatment data:\n{treatment_context}")
    if previous_dm:
        parts.append(f"\nPrevious DM sent (must differ by 30+ chars): {previous_dm}")
    return "\n".join(parts)


class ContentGenerator:
    """Generate reply and DM content using a configurable LLM provider.

    Parameters
    ----------
    api_key:
        API key (unused for Codex provider).
    model:
        LLM model identifier.
    provider:
        LLM provider name (default: ``"codex"``).
    """

    def __init__(
        self,
        *,
        api_key: str = "",
        model: str = "gpt-5.1-codex-mini",
        provider: str = "codex",
    ) -> None:
        self._llm: LLMClient = create_llm_client(provider, api_key, model=model)

    async def generate_reply(
        self,
        tweet_content: str,
        author_username: str,
        template_category: str,
        classification: str = "",
        treatment_context: str = "",
    ) -> str:
        """Generate a natural Japanese reply based on tweet context.

        Parameters
        ----------
        tweet_content:
            The original tweet text.
        author_username:
            The tweet author's username.
        template_category:
            Intent category (hospital/price/procedure/complaint/review).
        classification:
            Unused, kept for backward compatibility.
        treatment_context:
            Optional treatment data for context enrichment.

        Returns
        -------
        str
            Generated reply text (under 280 characters).

        Raises
        ------
        ContentGenerationError
            When LLM API call fails.
        """
        user_prompt = _build_reply_user_prompt(
            tweet_content=tweet_content,
            author_username=author_username,
            intent_type=template_category,
            treatment_context=treatment_context,
        )

        try:
            response = await self._llm.generate(
                user_prompt,
                system=REPLY_SYSTEM_PROMPT,
                temperature=0.8,
                max_tokens=200,
            )
            reply_text = response.text.strip()
            reply_text = _sanitize_llm_output(reply_text)

            # Enforce 280 character limit
            if len(reply_text) > 280:
                reply_text = reply_text[:277] + "..."

            # Strip any URLs that may have been generated
            reply_text = _strip_urls(reply_text)

            logger.info(
                "reply_generated",
                username=author_username,
                category=template_category,
                length=len(reply_text),
            )
            return reply_text

        except Exception as exc:
            logger.error(
                "reply_generation_error",
                username=author_username,
                error=str(exc)[:200],
            )
            raise ContentGenerationError(f"Failed to generate reply: {exc}") from exc

    async def generate_dm(
        self,
        tweet_content: str,
        author_username: str,
        template_category: str,
        classification: str = "",
        reply_content: str = "",
        treatment_context: str = "",
        previous_dm: str = "",
    ) -> str:
        """Generate a personalized Japanese DM.

        Parameters
        ----------
        tweet_content:
            The original tweet text.
        author_username:
            The tweet author's username.
        template_category:
            Intent category (hospital/price/procedure/complaint/review).
        classification:
            Unused, kept for backward compatibility.
        reply_content:
            The reply already sent to this tweet (for context).
        treatment_context:
            Optional treatment data for context enrichment.
        previous_dm:
            The previous DM sent (new DM must differ by 30+ chars).

        Returns
        -------
        str
            Generated DM text (under 500 characters, no links).

        Raises
        ------
        ContentGenerationError
            When LLM API call fails.
        """
        user_prompt = _build_dm_user_prompt(
            tweet_content=tweet_content,
            author_username=author_username,
            intent_type=template_category,
            reply_content=reply_content,
            treatment_context=treatment_context,
            previous_dm=previous_dm,
        )

        try:
            response = await self._llm.generate(
                user_prompt,
                system=DM_SYSTEM_PROMPT,
                temperature=0.8,
                max_tokens=400,
            )
            dm_text = response.text.strip()
            dm_text = _sanitize_llm_output(dm_text)

            # Enforce 500 character limit
            if len(dm_text) > 500:
                dm_text = dm_text[:497] + "..."

            # Strip any URLs that may have been generated
            dm_text = _strip_urls(dm_text)

            logger.info(
                "dm_generated",
                username=author_username,
                category=template_category,
                length=len(dm_text),
            )
            return dm_text

        except Exception as exc:
            logger.error(
                "dm_generation_error",
                username=author_username,
                error=str(exc)[:200],
            )
            raise ContentGenerationError(f"Failed to generate DM: {exc}") from exc

    async def generate_casual_post(self) -> str:
        """Generate a casual daily tweet for the @ask.nandemo account.

        Content is casual and personal -- explicitly NOT about dermatology.
        Topics include daily life, food, weather, Tokyo observations, etc.

        Returns
        -------
        str
            Generated tweet text (under 140 characters).

        Raises
        ------
        ContentGenerationError
            When LLM API call fails.
        """
        try:
            response = await self._llm.generate(
                "Generate one casual tweet.",
                system=CASUAL_POST_SYSTEM_PROMPT,
                temperature=0.95,
                max_tokens=100,
            )
            post_text = response.text.strip()
            post_text = _sanitize_llm_output(post_text)

            # Enforce 280 character hard limit
            if len(post_text) > 280:
                post_text = post_text[:277] + "..."

            # Strip any URLs that may have been generated
            post_text = _strip_urls(post_text)

            logger.info("casual_post_generated", length=len(post_text))
            return post_text

        except Exception as exc:
            logger.error("casual_post_generation_error", error=str(exc)[:200])
            raise ContentGenerationError(f"Failed to generate casual post: {exc}") from exc

    async def generate_knowledge_post(self, treatment_context: str) -> str:
        """Generate a Korean dermatology knowledge tweet.

        Uses treatment data to create an informative post that positions
        @ask.nandemo as a knowledgeable resource.

        Parameters
        ----------
        treatment_context:
            Treatment data snippet (procedure names, price ranges, etc.)
            to ground the post in real data.

        Returns
        -------
        str
            Generated tweet text (under 240 characters).

        Raises
        ------
        ContentGenerationError
            When LLM API call fails.
        """
        user_prompt = (
            f"Generate one informative tweet.\n\nAvailable treatment data:\n{treatment_context}"
        )

        try:
            response = await self._llm.generate(
                user_prompt,
                system=KNOWLEDGE_POST_SYSTEM_PROMPT,
                temperature=0.9,
                max_tokens=150,
            )
            post_text = response.text.strip()
            post_text = _sanitize_llm_output(post_text)

            if len(post_text) > 280:
                post_text = post_text[:277] + "..."

            post_text = _strip_urls(post_text)

            logger.info("knowledge_post_generated", length=len(post_text))
            return post_text

        except Exception as exc:
            logger.error("knowledge_post_generation_error", error=str(exc)[:200])
            raise ContentGenerationError(f"Failed to generate knowledge post: {exc}") from exc


class ContentGenerationError(Exception):
    """Raised when content generation via LLM API fails."""


def _strip_urls(text: str) -> str:
    """Remove any URLs from the text as a safety measure.

    DMs must not contain links.
    """
    return re.sub(r"https?://\S+", "", text).strip()


def _sanitize_llm_output(text: str) -> str:
    """Remove dangerous patterns from LLM-generated text before posting.

    Strips email addresses, @mentions, and phone number patterns that
    the LLM might hallucinate despite system prompt instructions.

    Order matters: email regex runs first so that the ``@`` anchor is
    intact; then @mentions are stripped.
    """
    # Strip zero-width characters that could bypass filters
    text = re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]", "", text)
    # Strip email addresses (MUST run before @mention removal)
    text = re.sub(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b", "", text)
    # Strip @mentions (e.g. @username)
    text = re.sub(r"@\w+", "", text)
    # Strip phone number patterns (international, local, and Korean fixed-line)
    text = re.sub(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}",
        "",
        text,
    )
    # Collapse multiple spaces left by removals
    text = re.sub(r"  +", " ", text).strip()
    return text


def dm_uniqueness_check(new_dm: str, previous_dm: str) -> bool:
    """Verify that the new DM differs from the previous by 30+ characters.

    Uses character-level set difference to measure uniqueness.

    Parameters
    ----------
    new_dm:
        The newly generated DM text.
    previous_dm:
        The previously sent DM text.

    Returns
    -------
    bool
        ``True`` if the new DM has at least 30 characters not in the previous.
    """
    if not previous_dm:
        return True

    unique_chars = 0
    prev_chars = list(previous_dm)
    for char in new_dm:
        if char in prev_chars:
            prev_chars.remove(char)
        else:
            unique_chars += 1

    return unique_chars >= 30
