"""Tests for content freshness analyzer."""

from datetime import date

import pytest

from app.services.content_freshness_analyzer import (
    _classify_freshness_page_type,
    _extract_date_from_meta,
    _extract_date_from_text,
    _freshness_rating,
    analyze_content_freshness,
    extract_page_date,
)

TODAY = date(2026, 3, 31)


# ── Date extraction from meta tags ──────────────────────────────────────────


class TestExtractDateFromMeta:
    def test_article_modified_time(self):
        html = '<html><head><meta property="article:modified_time" content="2026-01-15T10:30:00Z"></head><body></body></html>'
        assert _extract_date_from_meta(html) == date(2026, 1, 15)

    def test_article_published_time(self):
        html = '<html><head><meta property="article:published_time" content="2025-06-20"></head><body></body></html>'
        assert _extract_date_from_meta(html) == date(2025, 6, 20)

    def test_og_updated_time(self):
        html = '<html><head><meta property="og:updated_time" content="2025-12-01T08:00:00+09:00"></head><body></body></html>'
        assert _extract_date_from_meta(html) == date(2025, 12, 1)

    def test_last_modified_meta_name(self):
        html = '<html><head><meta name="last-modified" content="2024-03-10"></head><body></body></html>'
        assert _extract_date_from_meta(html) == date(2024, 3, 10)

    def test_time_tag_datetime(self):
        html = '<html><head></head><body><time datetime="2025-11-20">Nov 20</time></body></html>'
        assert _extract_date_from_meta(html) == date(2025, 11, 20)

    def test_no_date_meta(self):
        html = "<html><head><title>No date</title></head><body></body></html>"
        assert _extract_date_from_meta(html) is None


# ── Date extraction from text ───────────────────────────────────────────────


class TestExtractDateFromText:
    def test_korean_date_format(self):
        html = "<html><body><p>작성일: 2025년 8월 15일</p></body></html>"
        assert _extract_date_from_text(html) == date(2025, 8, 15)

    def test_iso_date_format(self):
        html = "<html><body><p>Published: 2025-10-01</p></body></html>"
        assert _extract_date_from_text(html) == date(2025, 10, 1)

    def test_dot_date_format(self):
        html = "<html><body><p>등록일: 2024.03.15</p></body></html>"
        assert _extract_date_from_text(html) == date(2024, 3, 15)

    def test_english_date_format(self):
        html = "<html><body><p>March 15, 2025</p></body></html>"
        assert _extract_date_from_text(html) == date(2025, 3, 15)

    def test_english_abbreviated_month(self):
        html = "<html><body><p>Jan 5, 2026</p></body></html>"
        assert _extract_date_from_text(html) == date(2026, 1, 5)

    def test_update_context_preferred(self):
        html = "<html><body><p>게시일: 2024-01-01</p><p>최종 수정: 2025-06-15</p></body></html>"
        assert _extract_date_from_text(html) == date(2025, 6, 15)

    def test_updated_prefix(self):
        html = "<html><body><p>Updated: 2026-02-10</p></body></html>"
        assert _extract_date_from_text(html) == date(2026, 2, 10)

    def test_no_date_found(self):
        html = "<html><body><p>날짜 정보가 없는 페이지입니다</p></body></html>"
        assert _extract_date_from_text(html) is None

    def test_year_month_only(self):
        html = "<html><body><p>2025년 3월</p></body></html>"
        assert _extract_date_from_text(html) == date(2025, 3, 1)

    def test_slash_date_format(self):
        html = "<html><body><p>2024/12/25</p></body></html>"
        assert _extract_date_from_text(html) == date(2024, 12, 25)


# ── Page type classification ───────────────────────────────────────────────


class TestClassifyFreshnessPageType:
    def test_blog_page(self):
        assert _classify_freshness_page_type("https://example.com/blog/post1", "블로그 글") == "blog"

    def test_news_page(self):
        assert _classify_freshness_page_type("https://example.com/news/latest", "최신 소식") == "blog"

    def test_event_page(self):
        assert _classify_freshness_page_type("https://example.com/event/spring", "봄 이벤트") == "event"

    def test_promotion_page(self):
        assert _classify_freshness_page_type("https://example.com/promo", "프로모션 할인") == "event"

    def test_procedure_page(self):
        assert _classify_freshness_page_type("https://example.com/treatment", "레이저 시술 안내") == "procedure"

    def test_doctor_page(self):
        assert _classify_freshness_page_type("https://example.com/staff", "의료진 소개") == "doctor"

    def test_other_page(self):
        assert _classify_freshness_page_type("https://example.com/location", "오시는 길") == "other"


# ── Freshness rating ────────────────────────────────────────────────────────


class TestFreshnessRating:
    def test_good_within_6_months(self):
        assert _freshness_rating(date(2026, 1, 1), TODAY) == "good"

    def test_moderate_6_to_12_months(self):
        assert _freshness_rating(date(2025, 6, 1), TODAY) == "moderate"

    def test_stale_over_12_months(self):
        assert _freshness_rating(date(2024, 1, 1), TODAY) == "stale"

    def test_unknown_no_date(self):
        assert _freshness_rating(None, TODAY) == "unknown"


# ── Full analysis ───────────────────────────────────────────────────────────


class TestAnalyzeContentFreshness:
    def test_empty_pages(self):
        result = analyze_content_freshness([], today=TODAY)
        assert result["overall_freshness_score"] == 0
        assert result["total_pages"] == 0

    def test_pages_with_dates(self):
        pages = [
            {
                "url": "https://example.com/blog/post1",
                "html": '<html><head><meta property="article:modified_time" content="2026-03-01"><title>블로그 최신글</title></head><body></body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/treatment/laser",
                "html": '<html><head><title>레이저 시술</title></head><body><p>Updated: 2025-01-10</p></body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["total_pages"] == 2
        assert result["pages_with_date"] == 2
        assert result["overall_freshness_score"] > 0
        assert "blog" in result["by_type"]
        assert "procedure" in result["by_type"]

    def test_freshness_rating_counts(self):
        pages = [
            {
                "url": "https://example.com/blog/new",
                "html": '<html><head><meta property="article:modified_time" content="2026-03-15"><title>최신 블로그</title></head><body></body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/treatment/old",
                "html": '<html><head><title>오래된 시술</title></head><body><p>2023-01-01</p></body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/about",
                "html": "<html><head><title>오시는 길</title></head><body>날짜 없음</body></html>",
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["freshness_rating"]["good"] == 1
        assert result["freshness_rating"]["stale"] == 1
        assert result["freshness_rating"]["unknown"] == 1

    def test_recommendations_for_stale_procedure(self):
        pages = [
            {
                "url": "https://example.com/treatment/laser",
                "html": '<html><head><title>레이저 시술</title></head><body><p>2024-06-01</p></body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert len(result["recommendations"]) > 0
        assert any("시술 소개" in r["message"] for r in result["recommendations"])

    def test_recommendations_for_stale_event(self):
        pages = [
            {
                "url": "https://example.com/event/summer",
                "html": '<html><head><title>여름 이벤트</title></head><body><p>2024-07-01</p></body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert any("이벤트" in r["message"] for r in result["recommendations"])

    def test_high_unknown_recommendation(self):
        pages = [
            {
                "url": f"https://example.com/page{i}",
                "html": f"<html><head><title>Page {i}</title></head><body>No date</body></html>",
                "status_code": 200,
            }
            for i in range(5)
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["freshness_rating"]["unknown"] == 5
        assert any("50%" in r["message"] for r in result["recommendations"])

    def test_recent_6months_count(self):
        pages = [
            {
                "url": "https://example.com/blog/a",
                "html": '<html><head><meta property="article:modified_time" content="2026-02-01"><title>Blog A</title></head><body></body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/blog/b",
                "html": '<html><head><meta property="article:modified_time" content="2026-03-20"><title>Blog B</title></head><body></body></html>',
                "status_code": 200,
            },
            {
                "url": "https://example.com/old",
                "html": '<html><head><title>Old page</title></head><body><p>2023-01-01</p></body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["recent_6months"] == 2

    def test_score_all_good(self):
        pages = [
            {
                "url": "https://example.com/page",
                "html": '<html><head><meta property="article:modified_time" content="2026-03-20"><title>Fresh</title></head><body></body></html>',
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["overall_freshness_score"] == 100

    def test_score_all_unknown(self):
        pages = [
            {
                "url": "https://example.com/page",
                "html": "<html><head><title>No date</title></head><body>content</body></html>",
                "status_code": 200,
            },
        ]
        result = analyze_content_freshness(pages, today=TODAY)
        assert result["overall_freshness_score"] == 30
