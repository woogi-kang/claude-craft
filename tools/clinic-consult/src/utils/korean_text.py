"""Korean text processing utilities.

Provides normalisation, detection, and truncation helpers for Korean
(Hangul) text used in messenger message handling.
"""

from __future__ import annotations

import unicodedata


def normalize_korean(text: str) -> str:
    """Normalize Korean text to NFC form and strip whitespace.

    NFC (Canonical Decomposition followed by Canonical Composition) ensures
    that precomposed Hangul syllables are used consistently.

    Parameters
    ----------
    text:
        Raw input string, potentially containing decomposed Hangul.

    Returns
    -------
    str
        NFC-normalized and stripped string.
    """
    return unicodedata.normalize("NFC", text).strip()


def contains_korean(text: str) -> bool:
    """Check whether *text* contains at least one Hangul character.

    Covers the main Unicode blocks for Korean:
    - Hangul Syllables (U+AC00 .. U+D7A3)
    - Hangul Jamo (U+1100 .. U+11FF)
    - Hangul Compatibility Jamo (U+3130 .. U+318F)
    - Hangul Jamo Extended-A (U+A960 .. U+A97F)
    - Hangul Jamo Extended-B (U+D7B0 .. U+D7FF)

    Returns
    -------
    bool
        ``True`` if at least one Hangul character is found.
    """
    for ch in text:
        cp = ord(ch)
        if (
            0xAC00 <= cp <= 0xD7A3      # Hangul Syllables
            or 0x1100 <= cp <= 0x11FF    # Hangul Jamo
            or 0x3130 <= cp <= 0x318F    # Hangul Compatibility Jamo
            or 0xA960 <= cp <= 0xA97F    # Hangul Jamo Extended-A
            or 0xD7B0 <= cp <= 0xD7FF    # Hangul Jamo Extended-B
        ):
            return True
    return False


def truncate_message(text: str, max_length: int = 500) -> str:
    """Truncate *text* at a word boundary, respecting Korean characters.

    If the text is already within *max_length*, it is returned unchanged.
    Otherwise the text is cut at the last whitespace boundary before the
    limit, and an ellipsis marker (``...``) is appended.

    Parameters
    ----------
    text:
        The message text to truncate.
    max_length:
        Maximum allowed character length (including the ellipsis).

    Returns
    -------
    str
        The original text or a truncated version with ``...`` appended.
    """
    if len(text) <= max_length:
        return text

    # Reserve space for the ellipsis marker
    cut = max_length - 3
    if cut <= 0:
        return text[:max_length]

    # Try to find a word boundary (whitespace) to cut at
    truncated = text[:cut]
    last_space = truncated.rfind(" ")

    if last_space > 0:
        truncated = truncated[:last_space]

    return truncated.rstrip() + "..."
