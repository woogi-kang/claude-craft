"""Content generation using Claude API.

Generates personalised reply and DM content based on tweet classification,
template categories, and treatment knowledge. All output is in natural
Japanese matching the @ask.nandemo voice.
"""

from __future__ import annotations

import anthropic

from src.utils.logger import get_logger

logger = get_logger("content_gen")


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

REPLY_SYSTEM_PROMPT = """\
You are @ask.nandemo, a neutral data-driven resource about Korean dermatology.
Generate a helpful reply in natural Japanese to this tweet.

Voice guide:
- Casual Japanese (plain form base: da-yo, da-ne, kana)
- Occasionally use desu/masu for softening
- Warm but not overly friendly
- Data-driven: include specific numbers when possible
- Never sound like a clinic marketing account
- Keep under 280 characters

Respond with ONLY the reply text. No explanation, no quotes, no prefix."""

DM_SYSTEM_PROMPT = """\
You are @ask.nandemo. Generate a personalized DM in natural Japanese.

Rules:
- Start with a warm greeting referencing their tweet
- Show understanding of their specific concern
- Offer to help with specific knowledge
- DO NOT include any links or URLs
- Keep under 500 characters
- Use casual but respectful Japanese

Respond with ONLY the DM text. No explanation, no quotes, no prefix."""


def _build_reply_user_prompt(
    tweet_content: str,
    author_username: str,
    template_category: str,
    classification: str,
    treatment_context: str,
) -> str:
    """Build the user prompt for reply generation."""
    parts = [
        f"Tweet: {tweet_content}",
        f"Author: @{author_username}",
        f"Classification: {classification}",
        f"Template category: {template_category}",
    ]
    if treatment_context:
        parts.append(f"\nRelevant treatment data:\n{treatment_context}")
    return "\n".join(parts)


def _build_dm_user_prompt(
    tweet_content: str,
    author_username: str,
    template_category: str,
    classification: str,
    reply_content: str,
    treatment_context: str,
    previous_dm: str,
) -> str:
    """Build the user prompt for DM generation."""
    parts = [
        f"Tweet they posted: {tweet_content}",
        f"Author: @{author_username}",
        f"Their concern category: {template_category}",
        f"Classification: {classification}",
    ]
    if reply_content:
        parts.append(f"Our reply to their tweet: {reply_content}")
    if treatment_context:
        parts.append(f"\nRelevant treatment data:\n{treatment_context}")
    if previous_dm:
        parts.append(
            f"\nPrevious DM sent (must differ by 30+ chars): {previous_dm}"
        )
    return "\n".join(parts)


class ContentGenerator:
    """Generate reply and DM content using Claude API.

    Parameters
    ----------
    api_key:
        Anthropic API key.
    model:
        Claude model identifier.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def generate_reply(
        self,
        tweet_content: str,
        author_username: str,
        template_category: str,
        classification: str,
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
            Classification template category (A-G).
        classification:
            Tweet classification (needs_help / seeking_info).
        treatment_context:
            Optional treatment data for context enrichment.

        Returns
        -------
        str
            Generated reply text (under 280 characters).

        Raises
        ------
        ContentGenerationError
            When Claude API call fails.
        """
        user_prompt = _build_reply_user_prompt(
            tweet_content=tweet_content,
            author_username=author_username,
            template_category=template_category,
            classification=classification,
            treatment_context=treatment_context,
        )

        try:
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=200,
                system=REPLY_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            reply_text = response.content[0].text.strip()

            # Enforce 280 character limit
            if len(reply_text) > 280:
                reply_text = reply_text[:277] + "..."

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
                error=str(exc),
            )
            raise ContentGenerationError(
                f"Failed to generate reply: {exc}"
            ) from exc

    async def generate_dm(
        self,
        tweet_content: str,
        author_username: str,
        template_category: str,
        classification: str,
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
            DM template category (A-E).
        classification:
            Tweet classification.
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
            When Claude API call fails.
        """
        user_prompt = _build_dm_user_prompt(
            tweet_content=tweet_content,
            author_username=author_username,
            template_category=template_category,
            classification=classification,
            reply_content=reply_content,
            treatment_context=treatment_context,
            previous_dm=previous_dm,
        )

        try:
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=400,
                system=DM_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )
            dm_text = response.content[0].text.strip()

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
                error=str(exc),
            )
            raise ContentGenerationError(
                f"Failed to generate DM: {exc}"
            ) from exc


class ContentGenerationError(Exception):
    """Raised when content generation via Claude API fails."""


def _strip_urls(text: str) -> str:
    """Remove any URLs from the text as a safety measure.

    DMs must not contain links per R5.8.
    """
    import re

    return re.sub(r"https?://\S+", "", text).strip()


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

    # Count characters in new_dm that are not at the same position in previous
    # Use a simple approach: find the longest common substring deficit
    unique_chars = 0
    prev_chars = list(previous_dm)
    for char in new_dm:
        if char in prev_chars:
            prev_chars.remove(char)
        else:
            unique_chars += 1

    return unique_chars >= 30
