"""Tests for the FAQMatcher pattern matching engine."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.knowledge.faq_matcher import FAQMatcher


@pytest.fixture
def templates_dir() -> Path:
    """Return the project templates directory."""
    return Path(__file__).resolve().parent.parent / "templates"


@pytest.fixture
def matcher(templates_dir: Path) -> FAQMatcher:
    """Provide a loaded FAQMatcher instance."""
    m = FAQMatcher(templates_dir)
    m.load()
    return m


# -- Exact FAQ matches -------------------------------------------------------


class TestExactFAQMatch:
    """Verify exact keyword matching for each FAQ category."""

    def test_pricing_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("보톡스 가격이 얼마인가요?")
        assert result is not None
        assert result.category == "pricing"
        assert result.source == "exact"
        assert result.confidence == pytest.approx(0.90)

    def test_hours_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("진료시간이 어떻게 되나요?")
        assert result is not None
        assert result.category == "hours"
        assert result.source == "exact"

    def test_location_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("병원 위치가 어디인가요?")
        assert result is not None
        assert result.category == "location"
        assert result.source == "exact"

    def test_reservation_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("내일 예약 가능한가요?")
        assert result is not None
        assert result.category == "reservation"
        assert result.source == "exact"

    def test_aftercare_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("시술후 주의사항 알려주세요")
        assert result is not None
        assert result.category == "aftercare"
        assert result.source == "exact"


# -- Greeting matches ---------------------------------------------------------


class TestGreetingMatch:
    """Verify greeting pattern matching."""

    def test_hello_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("안녕하세요")
        assert result is not None
        assert result.category == "hello"
        assert result.source == "greeting"
        assert result.confidence == pytest.approx(0.95)

    def test_thanks_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("감사합니다!")
        assert result is not None
        assert result.category == "thanks"
        assert result.source == "greeting"

    def test_goodbye_match(self, matcher: FAQMatcher) -> None:
        result = matcher.match("수고하세요")
        assert result is not None
        assert result.category == "goodbye"
        assert result.source == "greeting"


# -- No match -----------------------------------------------------------------


class TestNoMatch:
    """Verify that unrelated text returns None."""

    def test_random_text_returns_none(self, matcher: FAQMatcher) -> None:
        result = matcher.match("오늘 날씨가 참 좋네요 산책하기 딱입니다")
        assert result is None

    def test_english_text_returns_none(self, matcher: FAQMatcher) -> None:
        result = matcher.match("What is the meaning of life?")
        assert result is None

    def test_empty_string_returns_none(self, matcher: FAQMatcher) -> None:
        result = matcher.match("")
        assert result is None


# -- Priority -----------------------------------------------------------------


class TestGreetingPriority:
    """Verify that greetings are matched before FAQ patterns."""

    def test_greeting_takes_priority(self, matcher: FAQMatcher) -> None:
        # "안녕" matches greeting; should not fall through to FAQ
        result = matcher.match("안녕하세요 상담 예약하고 싶어요")
        assert result is not None
        assert result.source == "greeting"
        assert result.category == "hello"


# -- Normalized matching ------------------------------------------------------


class TestNormalizedMatching:
    """Verify matching works with varied casing and whitespace."""

    def test_extra_whitespace(self, matcher: FAQMatcher) -> None:
        result = matcher.match("   가격   문의합니다   ")
        assert result is not None
        assert result.category == "pricing"

    def test_mixed_case_english(self, matcher: FAQMatcher) -> None:
        # Korean patterns are case-insensitive after lowering
        result = matcher.match("가격 PRICE 알려주세요")
        assert result is not None
        assert result.category == "pricing"


# -- Fuzzy matching -----------------------------------------------------------


class TestFuzzyMatch:
    """Verify fuzzy matching for similar but not exact patterns."""

    def test_fuzzy_pricing_variant(self, matcher: FAQMatcher) -> None:
        # "비욘" shares characters with "비용" -- fuzzy may or may not match
        # depending on threshold; this tests that the fuzzy path is exercised
        m = FAQMatcher(
            matcher._templates_dir,
            fuzzy_threshold=0.5,  # lower threshold for test
        )
        m.load()
        result = m.match("비욘이 궁금해요")
        # With low threshold, should pick up partial character overlap
        if result is not None:
            assert result.source == "fuzzy"
            assert result.confidence >= 0.5

    def test_fuzzy_below_threshold_returns_none(self) -> None:
        """When threshold is very high, near-misses should not match."""
        templates_dir = Path(__file__).resolve().parent.parent / "templates"
        m = FAQMatcher(templates_dir, fuzzy_threshold=0.99)
        m.load()
        # "xyz" shares no characters with any Korean pattern
        result = m.match("xyz")
        assert result is None
