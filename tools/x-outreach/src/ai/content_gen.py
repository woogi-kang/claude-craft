"""Content generation via shared LLM client (Codex CLI default).

Generates personalised reply and DM content based on tweet classification,
intent categories, and treatment knowledge. All output is in natural
Japanese matching the master account voice. Supports optional persona
context for account-specific voice and style.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from outreach_shared.ai.llm_client import LLMClient, create_llm_client

if TYPE_CHECKING:
    from src.persona import PersonaContext

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
        persona: PersonaContext | None = None,
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
        persona:
            Optional persona context for account-specific voice.

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

        system_prompt = REPLY_SYSTEM_PROMPT
        max_chars = 280
        if persona is not None:
            from src.persona import build_persona_system_prompt

            system_prompt = build_persona_system_prompt(REPLY_SYSTEM_PROMPT, persona)
            max_chars = persona.stage_overrides.get("reply", {}).get("max_chars", 280)

        try:
            response = await self._llm.generate(
                user_prompt,
                system=system_prompt,
                temperature=0.8,
                max_tokens=200,
            )
            reply_text = response.text.strip()
            reply_text = _sanitize_llm_output(reply_text)

            # Enforce X's weighted character limit (CJK = 2 each)
            reply_text = _x_truncate(reply_text, max_chars)

            # Strip any URLs that may have been generated
            reply_text = _strip_urls(reply_text)

            if not _check_persona_violations(reply_text, persona, "reply"):
                raise ContentGenerationError("Persona validation failed for reply")

            logger.info(
                "reply_generated",
                username=author_username,
                category=template_category,
                length=x_weighted_len(reply_text),
                persona_id=persona.persona_id if persona else None,
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
        persona: PersonaContext | None = None,
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
        persona:
            Optional persona context for account-specific voice.

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

        system_prompt = DM_SYSTEM_PROMPT
        max_chars = 500
        if persona is not None:
            from src.persona import build_persona_system_prompt

            system_prompt = build_persona_system_prompt(DM_SYSTEM_PROMPT, persona)
            max_chars = persona.stage_overrides.get("dm", {}).get("max_chars", 500)

        try:
            response = await self._llm.generate(
                user_prompt,
                system=system_prompt,
                temperature=0.8,
                max_tokens=400,
            )
            dm_text = response.text.strip()
            dm_text = _sanitize_llm_output(dm_text)

            # Enforce X's weighted character limit (CJK = 2 each)
            dm_text = _x_truncate(dm_text, max_chars)

            # Strip any URLs that may have been generated
            dm_text = _strip_urls(dm_text)

            if not _check_persona_violations(dm_text, persona, "dm"):
                raise ContentGenerationError("Persona validation failed for DM")

            logger.info(
                "dm_generated",
                username=author_username,
                category=template_category,
                length=x_weighted_len(dm_text),
                persona_id=persona.persona_id if persona else None,
            )
            return dm_text

        except Exception as exc:
            logger.error(
                "dm_generation_error",
                username=author_username,
                error=str(exc)[:200],
            )
            raise ContentGenerationError(f"Failed to generate DM: {exc}") from exc

    async def generate_casual_post(
        self,
        persona: PersonaContext | None = None,
    ) -> str:
        """Generate a casual daily tweet for the master account.

        Content is casual and personal -- explicitly NOT about dermatology.
        Topics include daily life, food, weather, Tokyo observations, etc.

        Parameters
        ----------
        persona:
            Optional persona context for account-specific voice.

        Returns
        -------
        str
            Generated tweet text (under 140 characters).

        Raises
        ------
        ContentGenerationError
            When LLM API call fails.
        """
        system_prompt = CASUAL_POST_SYSTEM_PROMPT
        max_chars = 280
        if persona is not None:
            from src.persona import build_persona_system_prompt

            system_prompt = build_persona_system_prompt(CASUAL_POST_SYSTEM_PROMPT, persona)
            max_chars = persona.stage_overrides.get("post", {}).get("max_chars", 280)

        try:
            response = await self._llm.generate(
                "Generate one casual tweet.",
                system=system_prompt,
                temperature=0.95,
                max_tokens=100,
            )
            post_text = response.text.strip()
            post_text = _sanitize_llm_output(post_text)

            post_text = _x_truncate(post_text, max_chars)

            post_text = _strip_urls(post_text)

            if not _check_persona_violations(post_text, persona, "post"):
                raise ContentGenerationError("Persona validation failed for casual post")

            logger.info(
                "casual_post_generated",
                length=x_weighted_len(post_text),
                persona_id=persona.persona_id if persona else None,
            )
            return post_text

        except Exception as exc:
            logger.error("casual_post_generation_error", error=str(exc)[:200])
            raise ContentGenerationError(f"Failed to generate casual post: {exc}") from exc

    async def generate_knowledge_post(
        self,
        treatment_context: str,
        persona: PersonaContext | None = None,
    ) -> str:
        """Generate a Korean dermatology knowledge tweet.

        Uses treatment data to create an informative post that positions
        the master account as a knowledgeable resource.

        Parameters
        ----------
        treatment_context:
            Treatment data snippet (procedure names, price ranges, etc.)
            to ground the post in real data.
        persona:
            Optional persona context for account-specific voice.

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

        system_prompt = KNOWLEDGE_POST_SYSTEM_PROMPT
        max_chars = 280
        if persona is not None:
            from src.persona import build_persona_system_prompt

            system_prompt = build_persona_system_prompt(KNOWLEDGE_POST_SYSTEM_PROMPT, persona)
            max_chars = persona.stage_overrides.get("post", {}).get("max_chars", 280)

        try:
            response = await self._llm.generate(
                user_prompt,
                system=system_prompt,
                temperature=0.9,
                max_tokens=150,
            )
            post_text = response.text.strip()
            post_text = _sanitize_llm_output(post_text)

            post_text = _x_truncate(post_text, max_chars)

            post_text = _strip_urls(post_text)

            if not _check_persona_violations(post_text, persona, "post"):
                raise ContentGenerationError("Persona validation failed for knowledge post")

            logger.info(
                "knowledge_post_generated",
                length=x_weighted_len(post_text),
                persona_id=persona.persona_id if persona else None,
            )
            return post_text

        except Exception as exc:
            logger.error("knowledge_post_generation_error", error=str(exc)[:200])
            raise ContentGenerationError(f"Failed to generate knowledge post: {exc}") from exc


class ContentGenerationError(Exception):
    """Raised when content generation via LLM API fails."""


def x_weighted_len(text: str) -> int:
    """Return X's weighted character count.

    X counts CJK ideographs, kana, full-width characters, and certain
    Unicode ranges as 2 characters each.  Latin/ASCII counts as 1.
    """
    count = 0
    for ch in text:
        cp = ord(ch)
        # CJK Unified Ideographs, CJK Extension A/B, Kangxi Radicals,
        # Katakana, Hiragana, Full-width forms, Hangul, CJK Symbols
        if (
            0x1100 <= cp <= 0x11FF  # Hangul Jamo
            or 0x2E80 <= cp <= 0x9FFF  # CJK Radicals through CJK Unified
            or 0x3000 <= cp <= 0x303F  # CJK Symbols & Punctuation
            or 0x3040 <= cp <= 0x309F  # Hiragana
            or 0x30A0 <= cp <= 0x30FF  # Katakana
            or 0x3100 <= cp <= 0x312F  # Bopomofo
            or 0x3130 <= cp <= 0x318F  # Hangul Compatibility Jamo
            or 0xA960 <= cp <= 0xA97F  # Hangul Jamo Extended-A
            or 0xAC00 <= cp <= 0xD7FF  # Hangul Syllables & Jamo Ext-B
            or 0xF900 <= cp <= 0xFAFF  # CJK Compatibility Ideographs
            or 0xFE30 <= cp <= 0xFE4F  # CJK Compatibility Forms
            or 0xFF01 <= cp <= 0xFF60  # Full-width ASCII variants
            or 0xFFE0 <= cp <= 0xFFE6  # Full-width signs
            or 0x20000 <= cp <= 0x2FA1F  # CJK Extension B+ & Compat Supp
        ):
            count += 2
        else:
            count += 1
    return count


def _x_truncate(text: str, limit: int) -> str:
    """Truncate text to fit within X's weighted character limit."""
    if x_weighted_len(text) <= limit:
        return text
    # Walk forward and cut at the last position within budget
    wt = 0
    cut = 0
    for i, ch in enumerate(text):
        cp = ord(ch)
        w = (
            2
            if (
                0x1100 <= cp <= 0x11FF
                or 0x2E80 <= cp <= 0x9FFF
                or 0x3000 <= cp <= 0x303F
                or 0x3040 <= cp <= 0x309F
                or 0x30A0 <= cp <= 0x30FF
                or 0x3100 <= cp <= 0x312F
                or 0x3130 <= cp <= 0x318F
                or 0xA960 <= cp <= 0xA97F
                or 0xAC00 <= cp <= 0xD7FF
                or 0xF900 <= cp <= 0xFAFF
                or 0xFE30 <= cp <= 0xFE4F
                or 0xFF01 <= cp <= 0xFF60
                or 0xFFE0 <= cp <= 0xFFE6
                or 0x20000 <= cp <= 0x2FA1F
            )
            else 1
        )
        if wt + w > limit - 3:  # reserve 3 for "..."
            break
        wt += w
        cut = i + 1
    return text[:cut] + "..."


def _strip_urls(text: str) -> str:
    """Remove any URLs from the text as a safety measure.

    DMs must not contain links.
    """
    # Full URLs
    text = re.sub(r"https?://\S+", "", text)
    # Bare domain references like (sciencedaily.com) or example.org/path
    text = re.sub(r"\(?[a-zA-Z0-9-]+\.[a-z]{2,}(?:\.[a-z]{2,})?(?:/\S*)?\)?", "", text)
    return text.strip()


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


def _check_persona_violations(
    text: str,
    persona: PersonaContext | None,
    stage: str,
) -> bool:
    """Check generated text against persona rules.

    Returns ``True`` if text passes validation (or persona is None).
    Returns ``False`` and logs a warning on violation.
    """
    if persona is None:
        return True
    from src.persona import validate_persona_content

    valid, violations = validate_persona_content(text, persona, stage)
    if not valid:
        logger.warning(
            "persona_content_violation",
            persona_id=persona.persona_id,
            stage=stage,
            violations=violations,
        )
        return False
    return True
