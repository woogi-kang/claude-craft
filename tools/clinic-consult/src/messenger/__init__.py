"""Platform-agnostic messenger abstraction layer."""

from __future__ import annotations


def normalize_platform(platform: str) -> str:
    """Normalize a platform name to its canonical key.

    Handles case-insensitivity and aliases:

    - ``"kakao"``, ``"KakaoTalk"``, ``"kakaotalk"`` -> ``"kakao"``
    - ``"line"``, ``"Line"`` -> ``"line"``
    """
    key = platform.lower().strip()
    if key in ("kakao", "kakaotalk"):
        return "kakao"
    return key
