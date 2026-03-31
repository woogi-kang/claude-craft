"""Tests for multilingual readiness analyzer."""

import pytest

from app.services.multilingual_analyzer import (
    TARGET_LANGUAGES,
    _classify_page_type,
    _detect_lang_from_content,
    _detect_lang_from_html_tag,
    _detect_lang_from_url,
    _normalize_lang,
    analyze_multilingual_readiness,
)


# ── Language normalization ───────────────────────────────────────────


class TestNormalizeLang:
    def test_basic_codes(self):
        assert _normalize_lang("ko") == "ko"
        assert _normalize_lang("en") == "en"
        assert _normalize_lang("ja") == "ja"

    def test_aliases(self):
        assert _normalize_lang("jp") == "ja"
        assert _normalize_lang("cn") == "zh"
        assert _normalize_lang("zh-cn") == "zh"
        assert _normalize_lang("zh-tw") == "zh"
        assert _normalize_lang("zh-hans") == "zh"

    def test_case_insensitive(self):
        assert _normalize_lang("EN") == "en"
        assert _normalize_lang("Ko") == "ko"


# ── URL language detection ───────────────────────────────────────────


class TestDetectLangFromUrl:
    def test_path_segment(self):
        assert _detect_lang_from_url("https://example.com/en/about") == "en"
        assert _detect_lang_from_url("https://example.com/ja/treatment") == "ja"
        assert _detect_lang_from_url("https://example.com/zh/price") == "zh"

    def test_jp_alias(self):
        assert _detect_lang_from_url("https://example.com/jp/info") == "ja"

    def test_subdomain(self):
        assert _detect_lang_from_url("https://en.example.com/about") == "en"
        assert _detect_lang_from_url("https://ja.example.com/") == "ja"

    def test_no_lang(self):
        assert _detect_lang_from_url("https://example.com/about") is None
        assert _detect_lang_from_url("https://example.com/") is None


# ── HTML tag language detection ──────────────────────────────────────


class TestDetectLangFromHtmlTag:
    def test_html_lang_ko(self):
        html = '<html lang="ko"><head></head><body></body></html>'
        assert _detect_lang_from_html_tag(html) == "ko"

    def test_html_lang_en(self):
        html = '<html lang="en-US"><head></head><body></body></html>'
        assert _detect_lang_from_html_tag(html) == "en"

    def test_html_lang_ja(self):
        html = '<html lang="ja"><head></head><body></body></html>'
        assert _detect_lang_from_html_tag(html) == "ja"

    def test_no_lang_attr(self):
        html = "<html><head></head><body></body></html>"
        assert _detect_lang_from_html_tag(html) is None


# ── Content language detection ───────────────────────────────────────


class TestDetectLangFromContent:
    def test_korean_content(self):
        html = "<html><body><p>안녕하세요 피부과 전문 클리닉입니다</p></body></html>"
        assert _detect_lang_from_content(html) == "ko"

    def test_english_content(self):
        html = "<html><body><p>Welcome to our dermatology clinic specializing in skin treatment</p></body></html>"
        assert _detect_lang_from_content(html) == "en"

    def test_japanese_content(self):
        html = "<html><body><p>ようこそ皮膚科クリニックへ。レーザー治療を専門としています。</p></body></html>"
        assert _detect_lang_from_content(html) == "ja"

    def test_chinese_content(self):
        html = "<html><body><p>欢迎来到皮肤科诊所提供专业激光治疗服务</p></body></html>"
        assert _detect_lang_from_content(html) == "zh"

    def test_empty_content(self):
        html = "<html><body></body></html>"
        assert _detect_lang_from_content(html) == "ko"


# ── Page type classification ─────────────────────────────────────────


class TestClassifyPageType:
    def test_main_page(self):
        assert _classify_page_type("https://example.com/", "<html></html>") == "main"
        assert _classify_page_type("https://example.com", "<html></html>") == "main"

    def test_procedure_page(self):
        html = "<html><head><title>레이저 시술 안내</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/treatment", html) == "procedure"

    def test_doctor_page(self):
        html = "<html><head><title>의료진 소개</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/doctor", html) == "doctor"

    def test_price_page(self):
        html = "<html><head><title>가격 안내</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/cost", html) == "price"

    def test_booking_page(self):
        html = "<html><head><title>상담 예약</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/reservation", html) == "booking"

    def test_review_page(self):
        html = "<html><head><title>환자 후기 모음</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/results", html) == "review"

    def test_other_page(self):
        html = "<html><head><title>오시는 길</title></head><body></body></html>"
        assert _classify_page_type("https://example.com/location", html) == "other"


# ── Full analysis ────────────────────────────────────────────────────


class TestAnalyzeMultilingualReadiness:
    def test_empty_pages(self):
        result = analyze_multilingual_readiness([])
        assert result["overall_score"] == 0
        assert result["readiness_scores"]["ko"] == 0

    def test_korean_only_site(self):
        pages = [
            {
                "url": "https://example.com/",
                "html": '<html lang="ko"><head><title>피부과</title></head><body>안녕하세요</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/treatment",
                "html": '<html lang="ko"><head><title>시술 안내</title></head><body>레이저 시술</body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_multilingual_readiness(pages)
        assert result["readiness_scores"]["ko"] == 100
        assert result["readiness_scores"]["en"] == 0
        assert result["overall_score"] == 0
        assert len(result["recommendations"]) > 0
        # Should recommend adding en, ja, zh
        rec_langs = [r.get("lang") for r in result["recommendations"]]
        assert "en" in rec_langs

    def test_bilingual_site(self):
        pages = [
            {
                "url": "https://example.com/",
                "html": '<html lang="ko"><head><title>피부과</title></head><body>안녕하세요</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/en/",
                "html": '<html lang="en"><head><title>Clinic</title></head><body>Welcome to our clinic</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/en/treatment",
                "html": '<html lang="en"><head><title>Treatment</title></head><body>Laser treatment info</body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_multilingual_readiness(pages)
        assert result["readiness_scores"]["ko"] > 0
        assert result["readiness_scores"]["en"] > 0
        assert result["overall_score"] > 0
        # Matrix should show ko and en for main
        assert result["matrix"]["main"]["ko"] is True
        assert result["matrix"]["main"]["en"] is True

    def test_multilingual_site(self):
        pages = [
            {
                "url": "https://example.com/",
                "html": '<html lang="ko"><head><title>피부과</title></head><body>안녕하세요</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/en/",
                "html": '<html lang="en"><head><title>Clinic</title></head><body>Welcome</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/ja/",
                "html": '<html lang="ja"><head><title>クリニック</title></head><body>ようこそ</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/zh/",
                "html": '<html lang="zh"><head><title>诊所</title></head><body>欢迎</body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_multilingual_readiness(pages)
        assert result["readiness_scores"]["en"] > 0
        assert result["readiness_scores"]["ja"] > 0
        assert result["readiness_scores"]["zh"] > 0
        assert result["overall_score"] > 0

    def test_hreflang_extraction(self):
        html = """<html lang="ko"><head>
        <link rel="alternate" hreflang="ko" href="https://example.com/" />
        <link rel="alternate" hreflang="en" href="https://example.com/en/" />
        <link rel="alternate" hreflang="ja" href="https://example.com/ja/" />
        <title>피부과</title>
        </head><body>안녕하세요</body></html>"""
        pages = [{"url": "https://example.com/", "html": html, "status_code": 200}]
        result = analyze_multilingual_readiness(pages)
        assert len(result["hreflang_tags"]) == 3
        hreflang_langs = [t["lang"] for t in result["hreflang_tags"]]
        assert "ko" in hreflang_langs
        assert "en" in hreflang_langs
        assert "ja" in hreflang_langs

    def test_matrix_structure(self):
        pages = [
            {
                "url": "https://example.com/",
                "html": '<html lang="ko"><head><title>피부과</title></head><body>안녕하세요</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/treatment",
                "html": '<html lang="ko"><head><title>레이저 시술</title></head><body>시술 안내</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/en/",
                "html": '<html lang="en"><head><title>Clinic</title></head><body>Welcome</body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_multilingual_readiness(pages)
        matrix = result["matrix"]
        # main page should exist in both ko and en
        assert "main" in matrix
        assert matrix["main"]["ko"] is True
        assert matrix["main"]["en"] is True
        # procedure should only exist in ko
        assert "procedure" in matrix
        assert matrix["procedure"]["ko"] is True
        assert matrix["procedure"]["en"] is False

    def test_recommendations_for_partial_coverage(self):
        pages = [
            {
                "url": "https://example.com/",
                "html": '<html lang="ko"><head><title>피부과</title></head><body>안녕하세요</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/treatment",
                "html": '<html lang="ko"><head><title>시술 안내</title></head><body>레이저</body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/en/",
                "html": '<html lang="en"><head><title>Clinic</title></head><body>Welcome</body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_multilingual_readiness(pages)
        # Should have partial coverage recommendation for English
        categories = [r["category"] for r in result["recommendations"]]
        assert "partial_coverage" in categories or "missing_language" in categories
