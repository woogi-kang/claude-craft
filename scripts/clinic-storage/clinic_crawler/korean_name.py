"""Korean name validation for doctor extraction."""

from clinic_crawler.constants import (
    KOREAN_SURNAMES,
    NON_NAME_GIVEN,
    NON_NAME_SUFFIXES,
    NON_NAME_WORDS,
)

# Korean particles that never end a person's name
# Only include particles that are essentially impossible as name endings
# Excluded: 은(가은,하은), 서(민서,예서), 이, 가, 도, 의 — valid in real names
_TRAILING_PARTICLES = set("을를는며")


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
    # 3+ char names ending with a particle are almost certainly not names
    # (e.g. "고객을", "진료를", "한분한" is caught by NON_NAME_WORDS)
    if len(name) >= 3 and name[-1] in _TRAILING_PARTICLES:
        return False
    # Branch names ending in 점/본점 (e.g. 강남점, 강남본점, 서울점)
    if name.endswith("점"):
        return False
    return True
