"""Tests for Korean text utilities."""
from __future__ import annotations

from src.utils.korean_text import contains_korean, normalize_korean, truncate_message


class TestNormalizeKorean:
    def test_normalizes_nfc(self):
        # Decomposed form -> composed form
        result = normalize_korean("\ud55c\uae00")
        assert result == "\ud55c\uae00"

    def test_empty_string(self):
        assert normalize_korean("") == ""

    def test_ascii_passthrough(self):
        assert normalize_korean("hello") == "hello"


class TestContainsKorean:
    def test_korean_text(self):
        assert contains_korean("\uc548\ub155\ud558\uc138\uc694") is True

    def test_english_text(self):
        assert contains_korean("hello") is False

    def test_mixed_text(self):
        assert contains_korean("hello \uc548\ub155") is True

    def test_empty(self):
        assert contains_korean("") is False


class TestTruncateMessage:
    def test_short_message(self):
        assert truncate_message("Hi", 100) == "Hi"

    def test_long_message(self):
        result = truncate_message("A" * 200, 100)
        assert len(result) <= 103  # 100 + "..."
        assert result.endswith("...")
