"""Load social URL patterns from the canonical JSON source."""

from __future__ import annotations

import json
import re
from pathlib import Path

from clinic_crawl.models.enums import SocialPlatform

_PATTERNS_DIR = Path(__file__).resolve().parent.parent / "patterns"


def _load_social_patterns() -> dict:
    path = _PATTERNS_DIR / "social_urls.json"
    with path.open() as f:
        return json.load(f)


_RAW = _load_social_patterns()

# Platform -> list of URL fragment strings (from JSON)
PLATFORM_URL_FRAGMENTS: dict[SocialPlatform, list[str]] = {
    SocialPlatform(key): data["patterns"]
    for key, data in _RAW.items()
    if isinstance(data, dict) and "patterns" in data
}

# Platform -> compiled regex that matches any of its URL patterns
PLATFORM_VALIDATORS: dict[SocialPlatform, re.Pattern[str]] = {
    platform: re.compile(
        r"https?://(?:" + "|".join(re.escape(p).replace(r"/", "/") for p in fragments) + ")",
        re.IGNORECASE,
    )
    for platform, fragments in PLATFORM_URL_FRAGMENTS.items()
}

# Flat list of (regex, platform) tuples for prescan HTML scanning
SOCIAL_SCAN_PATTERNS: list[tuple[re.Pattern[str], SocialPlatform]] = [
    (
        re.compile(
            r"https?://" + re.escape(fragment).replace(r"/", "/") + r"[^\s\"'<>)*,;]*",
            re.IGNORECASE,
        ),
        platform,
    )
    for platform, fragments in PLATFORM_URL_FRAGMENTS.items()
    for fragment in fragments
]

# Widget detection signatures
WIDGET_SIGNATURES: list[str] = []
for _data in _RAW.values():
    if isinstance(_data, dict) and "widget_signatures" in _data:
        WIDGET_SIGNATURES.extend(_data["widget_signatures"])


def identify_platform(url: str) -> SocialPlatform | None:
    """Identify which social platform a URL belongs to."""
    for platform, pattern in PLATFORM_VALIDATORS.items():
        if pattern.search(url):
            return platform
    return None
