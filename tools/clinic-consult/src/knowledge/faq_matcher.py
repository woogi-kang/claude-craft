"""FAQ pattern matcher with keyword and fuzzy Korean matching."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from src.utils.korean_text import normalize_korean
from src.utils.logger import get_logger

logger = get_logger("faq_matcher")


@dataclass
class FAQMatch:
    """Result of FAQ pattern matching."""

    category: str
    matched_pattern: str
    confidence: float
    source: str  # "exact", "fuzzy", "greeting"


class FAQMatcher:
    """Match incoming messages against FAQ patterns.

    Parameters
    ----------
    templates_dir:
        Directory containing template YAML files.
    fuzzy_threshold:
        Minimum similarity score for fuzzy matching (0.0-1.0).
    """

    def __init__(self, templates_dir: Path, fuzzy_threshold: float = 0.75) -> None:
        self._templates_dir = templates_dir
        self._fuzzy_threshold = fuzzy_threshold
        self._faq_patterns: dict[str, list[str]] = {}
        self._greeting_patterns: dict[str, list[str]] = {}

    def load(self) -> int:
        """Load patterns from YAML files. Returns total pattern count."""
        total = 0

        faq_path = self._templates_dir / "faq_templates.yaml"
        if faq_path.exists():
            with open(faq_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for cat, cat_data in data.get("categories", {}).items():
                patterns = cat_data.get("patterns", [])
                self._faq_patterns[cat] = patterns
                total += len(patterns)

        greeting_path = self._templates_dir / "greeting_templates.yaml"
        if greeting_path.exists():
            with open(greeting_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for cat, cat_data in data.get("greetings", {}).items():
                patterns = cat_data.get("patterns", [])
                self._greeting_patterns[cat] = patterns
                total += len(patterns)

        logger.info("faq_patterns_loaded", total=total)
        return total

    def match(self, message: str) -> FAQMatch | None:
        """Match message against all patterns.

        Tries exact keyword match first, then fuzzy matching.
        Returns None if no match found.
        """
        normalized = normalize_korean(message.lower())

        # Tier 1: Exact keyword match in greetings (higher priority)
        for cat, patterns in self._greeting_patterns.items():
            for pattern in patterns:
                if pattern in normalized:
                    return FAQMatch(
                        category=cat,
                        matched_pattern=pattern,
                        confidence=0.95,
                        source="greeting",
                    )

        # Tier 2: Exact keyword match in FAQ
        for cat, patterns in self._faq_patterns.items():
            for pattern in patterns:
                if pattern in normalized:
                    return FAQMatch(
                        category=cat,
                        matched_pattern=pattern,
                        confidence=0.90,
                        source="exact",
                    )

        # Tier 3: Fuzzy matching (character-overlap based)
        best_score = 0.0
        best_match: FAQMatch | None = None

        for cat, patterns in self._faq_patterns.items():
            for pattern in patterns:
                score = self._fuzzy_score(normalized, pattern)
                if score > best_score and score >= self._fuzzy_threshold:
                    best_score = score
                    best_match = FAQMatch(
                        category=cat,
                        matched_pattern=pattern,
                        confidence=score,
                        source="fuzzy",
                    )

        return best_match

    def _fuzzy_score(self, text: str, pattern: str) -> float:
        """Calculate fuzzy similarity between text and pattern.

        Uses character overlap ratio as a simple but effective metric
        for Korean text matching.
        """
        if not text or not pattern:
            return 0.0

        # Check if pattern characters appear in text (order-independent)
        pattern_chars = set(pattern)
        text_chars = set(text)

        if not pattern_chars:
            return 0.0

        overlap = len(pattern_chars & text_chars)
        score = overlap / len(pattern_chars)

        # Boost score if pattern appears as substring
        if pattern in text:
            score = max(score, 0.95)

        return score

    @property
    def faq_categories(self) -> list[str]:
        """Return list of loaded FAQ category names."""
        return list(self._faq_patterns.keys())
