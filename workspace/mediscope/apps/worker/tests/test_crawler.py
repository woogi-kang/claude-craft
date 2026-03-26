"""Tests for the Crawler service."""

from unittest.mock import patch

import pytest

from app.security.ssrf import SSRFError
from app.services.crawler import Crawler


class TestCrawlerInit:
    def test_default_limits(self):
        c = Crawler()
        assert c.max_pages == 50
        assert c.max_depth == 3

    def test_custom_limits(self):
        c = Crawler(max_pages=10, max_depth=1)
        assert c.max_pages == 10
        assert c.max_depth == 1


class TestCrawlerValidation:
    def test_ssrf_blocked_url(self):
        c = Crawler()
        with patch(
            "app.security.ssrf.socket.getaddrinfo",
            return_value=[(2, 1, 6, "", ("127.0.0.1", 443))],
        ):
            with pytest.raises(SSRFError):
                import asyncio
                asyncio.get_event_loop().run_until_complete(
                    c.crawl("https://localhost/")
                )

    def test_ssrf_allowed_url(self):
        """Validates that public URLs pass SSRF check (crawl itself will fail without network)."""
        c = Crawler(max_pages=1, max_depth=0)
        with patch(
            "app.security.ssrf.socket.getaddrinfo",
            return_value=[(2, 1, 6, "", ("93.184.216.34", 443))],
        ):
            # The crawl will proceed past SSRF validation.
            # It will fail on actual HTTP request, but that's OK —
            # we just verify SSRF validation passes.
            import asyncio
            results = asyncio.get_event_loop().run_until_complete(
                c.crawl("https://example.com/")
            )
            # httpx will fail since we're not mocking the HTTP layer,
            # so results should be empty (no pages fetched)
            assert isinstance(results, list)
