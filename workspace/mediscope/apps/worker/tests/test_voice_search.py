"""Tests for voice search optimization analyzer."""

import pytest

from app.services.voice_search_analyzer import (
    QUESTION_PATTERNS,
    _check_featured_snippet_paragraphs,
    _count_long_tail_questions,
    _count_question_headings,
    _has_howto_schema,
    analyze_voice_search_readiness,
)
from bs4 import BeautifulSoup


# ── Question heading detection ───────────────────────────────────────


class TestQuestionHeadings:
    def test_question_mark(self):
        html = "<h2>보톡스 시술 후 주의사항은?</h2>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 1

    def test_english_question(self):
        html = "<h2>What is Botox?</h2><h3>How does it work?</h3>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 2

    def test_korean_question(self):
        html = "<h2>보톡스는 무엇인가</h2>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 1

    def test_japanese_question(self):
        html = "<h2>ボトックスとは</h2>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 1

    def test_non_question_heading(self):
        html = "<h2>보톡스 시술 안내</h2>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 0

    def test_only_h2_h3(self):
        html = "<h1>What is Botox?</h1><h4>How does it work?</h4>"
        soup = BeautifulSoup(html, "html.parser")
        result = _count_question_headings(soup)
        assert len(result) == 0


# ── Featured Snippet detection ───────────────────────────────────────


class TestFeaturedSnippet:
    def test_definition_paragraph(self):
        words = " ".join(["word"] * 45)
        html = f"<h2>What is Botox?</h2><p>Botox is a {words} treatment that works well.</p>"
        soup = BeautifulSoup(html, "html.parser")
        result = _check_featured_snippet_paragraphs(soup)
        assert len(result) >= 1

    def test_korean_definition(self):
        # Need 40-60 space-separated words for the word count check
        filler = " ".join(["좋은"] * 42)
        html = f"<h2>보톡스란?</h2><p>보톡스는 {filler} 시술입니다</p>"
        soup = BeautifulSoup(html, "html.parser")
        result = _check_featured_snippet_paragraphs(soup)
        assert len(result) >= 1

    def test_too_short_paragraph(self):
        html = "<h2>What is Botox?</h2><p>Botox is a treatment.</p>"
        soup = BeautifulSoup(html, "html.parser")
        result = _check_featured_snippet_paragraphs(soup)
        assert len(result) == 0

    def test_no_definition_form(self):
        words = " ".join(["word"] * 45)
        html = f"<h2>Botox Info</h2><p>We provide {words} services to our patients.</p>"
        soup = BeautifulSoup(html, "html.parser")
        result = _check_featured_snippet_paragraphs(soup)
        assert len(result) == 0


# ── HowTo Schema detection ──────────────────────────────────────────


class TestHowToSchema:
    def test_howto_present(self):
        items = [{"@type": "HowTo", "name": "Botox Procedure"}]
        assert _has_howto_schema(items) is True

    def test_howto_in_graph(self):
        items = [{"@graph": [{"@type": "HowTo", "name": "Steps"}]}]
        assert _has_howto_schema(items) is True

    def test_howto_absent(self):
        items = [{"@type": "FAQPage"}]
        assert _has_howto_schema(items) is False

    def test_empty_items(self):
        assert _has_howto_schema([]) is False


# ── Long-tail keyword detection ──────────────────────────────────────


class TestLongTailQuestions:
    def test_english_long_tail(self):
        html = "<p>How long does botox treatment last for patients?</p>"
        soup = BeautifulSoup(html, "html.parser")
        assert _count_long_tail_questions(soup) >= 1

    def test_short_question_excluded(self):
        html = "<p>What is botox?</p>"
        soup = BeautifulSoup(html, "html.parser")
        assert _count_long_tail_questions(soup) == 0

    def test_korean_long_tail(self):
        html = "<p>어떻게 하면 보톡스 시술을 안전하게 받을 수 있는지 알려주세요?</p>"
        soup = BeautifulSoup(html, "html.parser")
        assert _count_long_tail_questions(soup) >= 1


# ── Full analysis ────────────────────────────────────────────────────


class TestAnalyzeVoiceSearchReadiness:
    def test_empty_pages(self):
        result = analyze_voice_search_readiness([], {})
        assert result["overall_score"] == 0
        assert result["checks"] == {}
        assert result["pass_count"] == 0
        assert result["total_checks"] == 8
        assert result["recommendations"] == []

    def test_minimal_page(self):
        html = "<html><body><p>Simple page content</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_voice_search_readiness(pages, {})
        assert result["total_checks"] == 8
        assert result["overall_score"] >= 0
        assert len(result["checks"]) == 8
        # With no optimization, score should be low
        assert result["pass_count"] <= 3

    def test_well_optimized_page(self):
        html = """<html><head>
        <script type="application/ld+json">
        [{"@type": "FAQPage", "mainEntity": []},
         {"@type": "LocalBusiness", "name": "Test Clinic"},
         {"@type": "HowTo", "name": "Botox Steps"}]
        </script>
        </head><body>
        <h2>What is Botox treatment?</h2>
        <p>""" + " ".join(["Botox is a cosmetic"] + ["treatment that"] * 18 + ["works well."]) + """</p>
        <h2>How does filler work for patients?</h2>
        <p>""" + " ".join(["Filler is a"] + ["procedure that"] * 18 + ["helps patients."]) + """</p>
        <h3>Why should you choose our clinic?</h3>
        <h3>When is the best time for treatment?</h3>
        <h3>Where can I find the best dermatologist?</h3>
        <p>How long does botox treatment last for patients? Many patients ask this question.</p>
        <p>What are the best ways to prepare for filler injections at home?</p>
        <p>Where can I find a good cosmetic dermatologist near my location?</p>
        </body></html>"""
        pages = [{"url": "https://example.com", "html": html}]
        category_scores = {
            "faq_content": {"details": {"has_faq_schema": True}},
            "structured_data": {"details": {"schema_types": ["LocalBusiness"]}},
            "lcp": {"score": 80, "details": {"lcp_ms": 1500}},
            "mobile": {"score": 90},
        }
        result = analyze_voice_search_readiness(pages, category_scores)
        assert result["overall_score"] >= 50
        assert result["pass_count"] >= 4

    def test_recommendations_priority_sorted(self):
        html = "<html><body><p>Simple page</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_voice_search_readiness(pages, {})
        priorities = [r["priority"] for r in result["recommendations"]]
        # High priority should come before medium
        high_indices = [i for i, p in enumerate(priorities) if p == "high"]
        medium_indices = [i for i, p in enumerate(priorities) if p == "medium"]
        if high_indices and medium_indices:
            assert max(high_indices) < min(medium_indices)

    def test_category_scores_integration(self):
        html = "<html><body><p>Test page</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        # Pass mobile and speed checks via category_scores
        category_scores = {
            "mobile": {"score": 90},
            "lcp": {"score": 80, "details": {"lcp_ms": 2000}},
        }
        result = analyze_voice_search_readiness(pages, category_scores)
        assert result["checks"]["mobile"]["status"] == "pass"
        assert result["checks"]["page_speed"]["status"] == "pass"

    def test_multi_page_aggregation(self):
        page1 = """<html><body>
        <h2>What is Botox?</h2>
        <h3>How does it work?</h3>
        </body></html>"""

        page2 = """<html><body>
        <h2>When should I get filler?</h2>
        <h3>Why choose our clinic?</h3>
        <h3>Where is the clinic located?</h3>
        </body></html>"""

        pages = [
            {"url": "https://example.com", "html": page1},
            {"url": "https://example.com/filler", "html": page2},
        ]
        result = analyze_voice_search_readiness(pages, {})
        assert result["checks"]["question_headings"]["count"] == 5
        assert result["checks"]["question_headings"]["status"] == "pass"
