"""Tests for all check modules — HTML fixture based."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from app.checks.base import Grade
from app.checks.canonical import check_canonical
from app.checks.errors import check_errors
from app.checks.geo_aeo import check_ai_search_mention, check_content_clarity
from app.checks.headings import check_headings
from app.checks.https_check import check_https
from app.checks.images import check_images
from app.checks.links import check_links
from app.checks.meta_tags import check_meta_tags
from app.checks.mobile import check_mobile
from app.checks.performance import check_performance
from app.checks.robots import check_robots
from app.checks.sitemap import check_sitemap
from app.checks.structured_data import (
    check_eeat_signals,
    check_faq_content,
    check_structured_data,
)
from app.checks.multilingual import (
    check_hreflang,
    check_multilingual_pages,
    check_overseas_channels,
)
from app.checks.url_structure import check_url_structure


# ── Meta Tags ──────────────────────────────────────────────────────────


class TestMetaTags:
    def test_pass_with_good_html(self, good_html):
        r = check_meta_tags(good_html, "https://example.com")
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_no_title_no_desc(self, bad_html):
        r = check_meta_tags(bad_html, "https://example.com")
        assert r.grade == Grade.FAIL
        assert r.score == 0.0

    def test_warn_missing_og(self):
        html = """<html><head>
        <title>Good Title Here Test</title>
        <meta name="description" content="A good description that is long enough.">
        </head><body></body></html>"""
        r = check_meta_tags(html, "https://example.com")
        assert r.grade == Grade.WARN
        assert "og:title" in r.issues[0]


# ── Headings ───────────────────────────────────────────────────────────


class TestHeadings:
    def test_pass_single_h1(self, good_html):
        r = check_headings(good_html)
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_no_h1(self, bad_html):
        r = check_headings(bad_html)
        assert r.grade == Grade.FAIL
        assert r.score == 0.0

    def test_warn_multiple_h1(self):
        html = "<html><body><h1>First</h1><h1>Second</h1></body></html>"
        r = check_headings(html)
        assert r.grade == Grade.WARN
        assert r.score == 0.5

    def test_warn_heading_skip(self):
        html = "<html><body><h1>Title</h1><h3>Skipped h2</h3></body></html>"
        r = check_headings(html)
        assert r.grade == Grade.WARN


# ── Images ─────────────────────────────────────────────────────────────


class TestImages:
    def test_pass_all_alt(self, good_html):
        r = check_images(good_html)
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_no_alt(self, bad_html):
        r = check_images(bad_html)
        # bad_html has 2 images with no alt
        assert r.grade == Grade.FAIL
        assert r.score == 0.0

    def test_pass_no_images(self):
        html = "<html><body><p>No images here</p></body></html>"
        r = check_images(html)
        assert r.grade == Grade.PASS
        assert r.score == 1.0


# ── Canonical ──────────────────────────────────────────────────────────


class TestCanonical:
    def test_pass_with_canonical(self, good_html):
        r = check_canonical(good_html, "https://example.com/")
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_no_canonical(self, bad_html):
        r = check_canonical(bad_html, "https://example.com")
        assert r.grade == Grade.FAIL
        assert r.score == 0.0

    def test_warn_different_domain(self):
        html = '<html><head><link rel="canonical" href="https://other.com/page"></head><body></body></html>'
        r = check_canonical(html, "https://example.com/page")
        assert r.grade == Grade.WARN


# ── URL Structure ──────────────────────────────────────────────────────


class TestUrlStructure:
    def test_pass_clean_urls(self):
        urls = [
            "https://example.com/",
            "https://example.com/services",
            "https://example.com/about",
        ]
        r = check_url_structure("https://example.com/", urls)
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_warn_deep_urls(self):
        # Need at least one good URL so problem_ratio <= 0.5
        urls = [
            "https://example.com/",
            "https://example.com/a/b/c/d/e/f",
        ]
        r = check_url_structure("https://example.com/", urls)
        assert r.grade == Grade.WARN

    def test_fail_all_deep(self):
        urls = ["https://example.com/a/b/c/d/e/f"]
        r = check_url_structure("https://example.com/", urls)
        assert r.grade == Grade.FAIL

    def test_warn_bad_patterns(self):
        # .php? URL triggers 2 bad patterns (query param + .php?), so we need
        # enough good URLs to keep problem_ratio <= 0.5
        urls = [
            "https://example.com/",
            "https://example.com/about",
            "https://example.com/services",
            "https://example.com/contact",
            "https://example.com/page.php?id=123",
        ]
        r = check_url_structure("https://example.com/", urls)
        assert r.grade == Grade.WARN


# ── Mobile ─────────────────────────────────────────────────────────────


class TestMobile:
    def test_pass_with_viewport(self, good_html):
        r = check_mobile(good_html)
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_no_viewport(self, bad_html):
        r = check_mobile(bad_html)
        assert r.grade == Grade.FAIL
        assert r.score == 0.0

    def test_warn_viewport_no_device_width(self):
        html = '<html><head><meta name="viewport" content="width=1024"></head><body></body></html>'
        r = check_mobile(html)
        assert r.grade == Grade.WARN


# ── Structured Data ────────────────────────────────────────────────────


class TestStructuredData:
    def test_warn_with_medical_schema(self, good_html):
        r = check_structured_data(good_html)
        # MedicalClinic (0.4) + JSON-LD exists (0.1) = 0.5 → WARN (threshold 0.6)
        assert r.score >= 0.5
        assert r.grade in (Grade.WARN, Grade.PASS)

    def test_pass_with_full_schema(self):
        html = """<html><head>
        <script type="application/ld+json">
        {"@context":"https://schema.org","@type":"MedicalClinic","name":"Test"}
        </script>
        <script type="application/ld+json">
        {"@context":"https://schema.org","@type":"WebSite","name":"Test"}
        </script>
        <script type="application/ld+json">
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[]}
        </script>
        </head><body></body></html>"""
        r = check_structured_data(html)
        # MedicalClinic(0.4) + WebSite(0.2) + BreadcrumbList(0.1) + JSON-LD(0.1) = 0.8
        assert r.grade == Grade.PASS
        assert r.score >= 0.6

    def test_fail_no_schema(self, bad_html):
        r = check_structured_data(bad_html)
        assert r.grade == Grade.FAIL
        assert r.score < 0.3


# ── FAQ Content ────────────────────────────────────────────────────────


class TestFaqContent:
    def test_pass_with_faq(self, good_html):
        r = check_faq_content(good_html)
        # good_html has FAQPage schema + FAQ content
        assert r.grade == Grade.PASS
        assert r.score >= 0.6

    def test_fail_no_faq(self, bad_html):
        r = check_faq_content(bad_html)
        assert r.grade == Grade.FAIL


# ── E-E-A-T Signals ───────────────────────────────────────────────────


class TestEeatSignals:
    def test_pass_with_signals(self, good_html):
        r = check_eeat_signals(good_html, "https://example.com")
        assert r.grade == Grade.PASS
        assert r.score >= 0.6

    def test_fail_no_signals(self, bad_html):
        r = check_eeat_signals(bad_html, "https://example.com")
        assert r.grade == Grade.FAIL
        assert r.score < 0.3


# ── Content Clarity ────────────────────────────────────────────────────


class TestContentClarity:
    def test_good_content(self, good_html):
        r = check_content_clarity(good_html)
        # good_html has paragraphs, lists, tables, headings, Q&A
        assert r.score >= 0.4

    def test_bad_content(self, bad_html):
        r = check_content_clarity(bad_html)
        assert r.score < 0.4


# ── Async checks (using respx) ────────────────────────────────────────


@pytest.mark.asyncio
class TestRobots:
    async def test_pass_good_robots(self):
        async with respx.mock:
            respx.get("https://example.com/robots.txt").mock(
                return_value=httpx.Response(
                    200,
                    text="User-Agent: *\nAllow: /\nSitemap: https://example.com/sitemap.xml\n",
                )
            )
            async with httpx.AsyncClient() as client:
                r = await check_robots(client, "https://example.com")
            assert r.grade == Grade.PASS
            assert r.score == 1.0

    async def test_fail_no_robots(self):
        async with respx.mock:
            respx.get("https://example.com/robots.txt").mock(
                return_value=httpx.Response(404)
            )
            async with httpx.AsyncClient() as client:
                r = await check_robots(client, "https://example.com")
            assert r.grade == Grade.FAIL

    async def test_fail_disallow_all(self):
        async with respx.mock:
            respx.get("https://example.com/robots.txt").mock(
                return_value=httpx.Response(
                    200, text="User-Agent: *\nDisallow: /\n"
                )
            )
            async with httpx.AsyncClient() as client:
                r = await check_robots(client, "https://example.com")
            assert r.grade == Grade.FAIL
            assert r.score == 0.0


@pytest.mark.asyncio
class TestSitemap:
    async def test_pass_valid_sitemap(self):
        sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://example.com/</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/about</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/1</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/2</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/3</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/4</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/5</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/6</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/7</loc><lastmod>2026-01-01</lastmod></url>
            <url><loc>https://example.com/8</loc><lastmod>2026-01-01</lastmod></url>
        </urlset>"""
        async with respx.mock:
            respx.get("https://example.com/sitemap.xml").mock(
                return_value=httpx.Response(200, text=sitemap_xml)
            )
            async with httpx.AsyncClient() as client:
                r = await check_sitemap(client, "https://example.com")
            assert r.grade == Grade.PASS
            assert r.score == 1.0

    async def test_fail_no_sitemap(self):
        async with respx.mock:
            respx.get("https://example.com/sitemap.xml").mock(
                return_value=httpx.Response(404)
            )
            async with httpx.AsyncClient() as client:
                r = await check_sitemap(client, "https://example.com")
            assert r.grade == Grade.FAIL


@pytest.mark.asyncio
class TestHttps:
    async def test_pass_https(self):
        async with respx.mock:
            respx.get("http://example.com/").mock(
                return_value=httpx.Response(301, headers={"location": "https://example.com/"})
            )
            respx.get("https://example.com/").mock(
                return_value=httpx.Response(200, text="<html></html>")
            )
            async with httpx.AsyncClient() as client:
                r = await check_https(client, "https://example.com/")
            assert r.grade == Grade.PASS
            assert r.score == 1.0

    async def test_fail_http_only(self):
        async with respx.mock:
            respx.get("https://example.com/").mock(side_effect=httpx.ConnectError("no ssl"))
            respx.get("http://example.com/").mock(
                return_value=httpx.Response(200, text="<html></html>")
            )
            async with httpx.AsyncClient() as client:
                r = await check_https(client, "http://example.com/")
            assert r.grade == Grade.FAIL


@pytest.mark.asyncio
class TestLinks:
    async def test_pass_no_broken(self):
        html = """<html><body>
        <a href="/about">About</a>
        <a href="/services">Services</a>
        <a href="/contact">Contact</a>
        </body></html>"""
        async with respx.mock:
            respx.head("https://example.com/about").mock(return_value=httpx.Response(200))
            respx.head("https://example.com/services").mock(return_value=httpx.Response(200))
            respx.head("https://example.com/contact").mock(return_value=httpx.Response(200))
            async with httpx.AsyncClient() as client:
                r = await check_links(client, html, "https://example.com")
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    async def test_warn_broken_link(self):
        html = """<html><body>
        <a href="/about">About</a>
        <a href="/missing">Missing</a>
        <a href="/services">Services</a>
        </body></html>"""
        async with respx.mock:
            respx.head("https://example.com/about").mock(return_value=httpx.Response(200))
            respx.head("https://example.com/missing").mock(return_value=httpx.Response(404))
            respx.head("https://example.com/services").mock(return_value=httpx.Response(200))
            async with httpx.AsyncClient() as client:
                r = await check_links(client, html, "https://example.com")
        assert r.grade == Grade.WARN


@pytest.mark.asyncio
class TestErrors:
    async def test_pass_no_errors(self):
        urls = ["https://example.com/", "https://example.com/about"]
        async with respx.mock:
            respx.get("https://example.com/").mock(return_value=httpx.Response(200))
            respx.get("https://example.com/about").mock(return_value=httpx.Response(200))
            async with httpx.AsyncClient() as client:
                r = await check_errors(client, urls)
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    async def test_warn_some_errors(self):
        urls = ["https://example.com/missing"]
        async with respx.mock:
            respx.get("https://example.com/missing").mock(return_value=httpx.Response(404))
            async with httpx.AsyncClient() as client:
                r = await check_errors(client, urls)
        assert r.grade == Grade.WARN


@pytest.mark.asyncio
class TestPerformance:
    async def test_pass_good_performance(self):
        psi_response = {
            "lighthouseResult": {
                "audits": {
                    "largest-contentful-paint": {"numericValue": 1500},
                    "interaction-to-next-paint": {"numericValue": 100},
                    "cumulative-layout-shift": {"numericValue": 0.05},
                },
                "categories": {
                    "performance": {"score": 0.95},
                },
            }
        }
        async with respx.mock:
            respx.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed").mock(
                return_value=httpx.Response(200, json=psi_response)
            )
            async with httpx.AsyncClient() as client:
                results = await check_performance(client, "https://example.com")
        assert len(results) == 4
        names = {r.name for r in results}
        assert names == {"lcp", "inp", "cls", "performance_score"}
        for r in results:
            assert r.grade == Grade.PASS

    async def test_fallback_on_api_failure(self):
        async with respx.mock:
            respx.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed").mock(
                return_value=httpx.Response(500)
            )
            async with httpx.AsyncClient() as client:
                results = await check_performance(client, "https://example.com")
        assert len(results) == 4
        for r in results:
            assert r.grade == Grade.WARN


@pytest.mark.asyncio
class TestAiSearchMention:
    async def test_fail_no_hospital_name(self):
        async with httpx.AsyncClient() as client:
            r = await check_ai_search_mention(client, "https://example.com", "")
        assert r.grade == Grade.FAIL
        assert r.details.get("skipped") is True

    async def test_fail_no_api_key(self):
        """Without perplexity_api_key, should return fail with skipped."""
        async with httpx.AsyncClient() as client:
            r = await check_ai_search_mention(
                client, "https://example.com", "TestHospital"
            )
        assert r.grade == Grade.FAIL
        assert "API" in r.issues[0]


# ── Multilingual Pages ────────────────────────────────────────────────


class TestMultilingualPages:
    def test_pass_multiple_languages(self):
        html = '<html lang="ko"><head></head><body></body></html>'
        urls = [
            "https://example.com/",
            "https://example.com/en/",
            "https://example.com/ja/about",
            "https://example.com/zh/services",
        ]
        r = check_multilingual_pages(html, urls)
        assert r.name == "multilingual_pages"
        assert r.grade == Grade.PASS
        assert r.score == 1.0

    def test_fail_korean_only(self):
        html = '<html lang="ko"><head></head><body></body></html>'
        urls = ["https://example.com/", "https://example.com/about"]
        r = check_multilingual_pages(html, urls)
        assert r.grade == Grade.FAIL
        assert r.score == 0.0
        assert len(r.issues) == 1

    def test_warn_one_language(self):
        html = '<html lang="ko"><head></head><body></body></html>'
        urls = ["https://example.com/", "https://example.com/en/"]
        r = check_multilingual_pages(html, urls)
        assert r.grade == Grade.WARN
        assert r.score == 0.4


# ── Hreflang ─────────────────────────────────────────────────────────


class TestHreflang:
    def test_pass_multiple_hreflang(self):
        html = """<html><head>
        <link rel="alternate" hreflang="ko" href="https://example.com/">
        <link rel="alternate" hreflang="en" href="https://example.com/en/">
        <link rel="alternate" hreflang="ja" href="https://example.com/ja/">
        </head><body></body></html>"""
        r = check_hreflang(html)
        assert r.name == "hreflang"
        assert r.grade == Grade.PASS
        assert r.score == 1.0
        assert "en" in r.details["hreflang_tags"]

    def test_fail_no_hreflang(self):
        html = "<html><head></head><body></body></html>"
        r = check_hreflang(html)
        assert r.grade == Grade.FAIL
        assert r.score == 0.0
        assert len(r.issues) == 1

    def test_warn_single_hreflang(self):
        html = """<html><head>
        <link rel="alternate" hreflang="ko" href="https://example.com/">
        </head><body></body></html>"""
        r = check_hreflang(html)
        assert r.grade == Grade.WARN
        assert r.score == 0.5


# ── Overseas Channels ────────────────────────────────────────────────


class TestOverseasChannels:
    def test_pass_multiple_channels(self):
        html = """<html><body>
        <a href="https://line.me/ti/p/@clinic">LINE 상담</a>
        <a href="https://wa.me/821012345678">WhatsApp</a>
        </body></html>"""
        r = check_overseas_channels(html)
        assert r.name == "overseas_channels"
        assert r.grade == Grade.PASS
        assert r.score == 1.0
        assert len(r.details["overseas_channels"]) >= 2

    def test_fail_no_channels(self):
        html = "<html><body><p>No channels</p></body></html>"
        r = check_overseas_channels(html)
        assert r.grade == Grade.FAIL
        assert r.score == 0.0
        assert len(r.issues) == 1

    def test_warn_single_channel(self):
        html = """<html><body>
        <a href="https://line.me/ti/p/@clinic">LINE</a>
        </body></html>"""
        r = check_overseas_channels(html)
        assert r.grade == Grade.WARN
        assert r.score == 0.5
