"""Tests for tech stack detector."""

import pytest

from app.services.tech_stack_detector import (
    ALL_CATEGORIES,
    TECH_SIGNATURES,
    _match_tech,
    detect_tech_stack,
)


# ── Pattern matching ───────────────────────────────────────────────────────


class TestMatchTech:
    def test_google_analytics_gtag(self):
        html = '<script>gtag("config", "G-XXXXXX")</script>'
        assert _match_tech(html, "google_analytics", TECH_SIGNATURES["google_analytics"])

    def test_google_analytics_tag_manager(self):
        html = '<script src="https://www.googletagmanager.com/gtag/js"></script>'
        assert _match_tech(html, "google_analytics", TECH_SIGNATURES["google_analytics"])

    def test_facebook_pixel(self):
        html = "<script>fbq('init', '123456');</script>"
        assert _match_tech(html, "facebook_pixel", TECH_SIGNATURES["facebook_pixel"])

    def test_channel_io(self):
        html = '<script src="https://cdn.channel.io/plugin/ch-plugin-web.js"></script>'
        assert _match_tech(html, "channel_io", TECH_SIGNATURES["channel_io"])

    def test_wordpress(self):
        html = '<link rel="stylesheet" href="/wp-content/themes/flavor/style.css">'
        assert _match_tech(html, "wordpress", TECH_SIGNATURES["wordpress"])

    def test_cloudflare(self):
        html = '<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.js"></script>'
        assert _match_tech(html, "cloudflare", TECH_SIGNATURES["cloudflare"])

    def test_schema_org(self):
        html = '<script type="application/ld+json">{"@context":"https://schema.org"}</script>'
        assert _match_tech(html, "schema_org", TECH_SIGNATURES["schema_org"])

    def test_naver_analytics(self):
        html = "<script>var _nasa={}; wcs_add['wa']='abc123';</script>"
        assert _match_tech(html, "naver_analytics", TECH_SIGNATURES["naver_analytics"])

    def test_naver_booking(self):
        html = '<a href="https://booking.naver.com/booking/13/bizes/12345">예약</a>'
        assert _match_tech(html, "naver_booking", TECH_SIGNATURES["naver_booking"])

    def test_no_match(self):
        html = "<html><body><p>Hello world</p></body></html>"
        assert not _match_tech(html, "google_analytics", TECH_SIGNATURES["google_analytics"])

    def test_case_insensitive(self):
        html = "<script>CHANNELIO.init()</script>"
        # ChannelIO pattern should match case-insensitively
        assert _match_tech(html, "channel_io", TECH_SIGNATURES["channel_io"])


# ── Full detection ─────────────────────────────────────────────────────────


class TestDetectTechStack:
    def test_empty_pages(self):
        result = detect_tech_stack([])
        assert result["total_detected"] == 0
        assert result["detected"] == {}
        for cat in ALL_CATEGORIES:
            assert cat in result["by_category"]
            assert result["by_category"][cat] == []

    def test_single_page_multiple_techs(self):
        html = """
        <html>
        <head>
            <script src="https://www.googletagmanager.com/gtag/js?id=G-ABC123"></script>
            <script>fbq('init', '999');</script>
            <script type="application/ld+json">{"@context":"https://schema.org"}</script>
        </head>
        <body><p>Test</p></body>
        </html>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = detect_tech_stack(pages)

        assert result["total_detected"] >= 3
        assert "google_analytics" in result["detected"]
        assert "facebook_pixel" in result["detected"]
        assert "schema_org" in result["detected"]
        assert "Google Analytics" in result["by_category"]["analytics"]
        assert "Facebook Pixel" in result["by_category"]["ads"]
        assert "구조화 데이터" in result["by_category"]["seo"]

    def test_multiple_pages_aggregate(self):
        page1 = {"url": "https://example.com", "html": '<script>gtag("config")</script>'}
        page2 = {"url": "https://example.com/about", "html": '<script src="https://cdn.channel.io/plugin.js"></script>'}
        result = detect_tech_stack([page1, page2])

        assert "google_analytics" in result["detected"]
        assert "channel_io" in result["detected"]
        assert result["detected"]["google_analytics"]["found_on"] == ["https://example.com"]
        assert result["detected"]["channel_io"]["found_on"] == ["https://example.com/about"]

    def test_found_on_dedup(self):
        html = '<script>gtag("config"); gtag("event")</script>'
        pages = [{"url": "https://example.com", "html": html}]
        result = detect_tech_stack(pages)
        assert len(result["detected"]["google_analytics"]["found_on"]) == 1

    def test_missing_recommended_complete(self):
        """When no tech is detected, all recommended items should be missing."""
        pages = [{"url": "https://example.com", "html": "<html><body>plain</body></html>"}]
        result = detect_tech_stack(pages)
        assert len(result["missing_recommended"]) >= 5

    def test_missing_recommended_partial(self):
        """When analytics is detected, it should not be in missing list."""
        html = '<script src="https://www.googletagmanager.com/gtag/js"></script>'
        pages = [{"url": "https://example.com", "html": html}]
        result = detect_tech_stack(pages)

        missing_techs = [m["tech"] for m in result["missing_recommended"]]
        assert "Google Analytics" not in missing_techs

    def test_recommendations_for_missing_analytics(self):
        pages = [{"url": "https://example.com", "html": "<html><body>no tech</body></html>"}]
        result = detect_tech_stack(pages)
        assert any("분석 도구" in r["message"] for r in result["recommendations"])

    def test_recommendations_for_missing_schema(self):
        pages = [{"url": "https://example.com", "html": "<html><body>no tech</body></html>"}]
        result = detect_tech_stack(pages)
        assert any("구조화 데이터" in r["message"] for r in result["recommendations"])

    def test_no_recommendations_when_all_present(self):
        html = """
        <script src="https://www.googletagmanager.com/gtag/js"></script>
        <script>fbq('init');</script>
        <script src="https://cdn.channel.io/plugin.js"></script>
        <link href="/wp-content/themes/flavor/style.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/x.js"></script>
        <a href="https://booking.naver.com/booking/13/bizes/1">예약</a>
        <script type="application/ld+json">{"@context":"https://schema.org"}</script>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = detect_tech_stack(pages)
        assert result["recommendations"] == []
        assert result["missing_recommended"] == []

    def test_by_category_structure(self):
        result = detect_tech_stack([{"url": "https://example.com", "html": "<html></html>"}])
        for cat in ALL_CATEGORIES:
            assert cat in result["by_category"]
            assert isinstance(result["by_category"][cat], list)

    def test_korean_platform_detection(self):
        html = """
        <script>var _nasa={}; wcs_add['wa']='s_abc';</script>
        <a href="https://booking.naver.com/booking/13">예약</a>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = detect_tech_stack(pages)
        assert "naver_analytics" in result["detected"]
        assert "naver_booking" in result["detected"]
        assert "네이버 애널리틱스" in result["by_category"]["analytics"]
        assert "네이버 예약" in result["by_category"]["booking"]
