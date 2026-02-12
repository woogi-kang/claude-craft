"""Korean name validation for doctor extraction."""

from clinic_crawler.constants import (
    KOREAN_SURNAMES,
    NON_NAME_GIVEN,
    NON_NAME_SUFFIXES,
    NON_NAME_WORDS,
)


def is_plausible_korean_name(name: str) -> bool:
    """Check if a string is plausibly a Korean person's name."""
    if not name or len(name) < 2 or len(name) > 4:
        return False
    # All characters should be Korean syllables (가-힣)
    if not all('\uac00' <= c <= '\ud7a3' for c in name):
        return False
    # First character should be a known surname
    if name[0] not in KOREAN_SURNAMES:
        return False
    # Exclude common non-name patterns
    if name in NON_NAME_WORDS:
        return False
    if name[1:] in NON_NAME_SUFFIXES:
        return False
    if name[1:] in NON_NAME_GIVEN:
        return False
    return True
