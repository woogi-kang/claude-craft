"""Tests for international search engine visibility check."""

from unittest.mock import patch

import httpx
import pytest
import respx

from app.checks.base import Grade
from app.checks.international_search import (
    _find_rank,
    _rank_to_score,
    check_international_search,
)


# ── Helpers ───────────────────────────────────────────────────────────


class TestRankToScore:
    def test_none_returns_zero(self):
        assert _rank_to_score(None) == 0.0

    def test_top_10(self):
        assert _rank_to_score(1) == 1.0
        assert _rank_to_score(10) == 1.0

    def test_top_30(self):
        assert _rank_to_score(11) == 0.7
        assert _rank_to_score(30) == 0.7

    def test_top_100(self):
        assert _rank_to_score(31) == 0.3
        assert _rank_to_score(100) == 0.3

    def test_beyond_100(self):
        assert _rank_to_score(101) == 0.0


class TestFindRank:
    def test_found_exact_domain(self):
        items = [
            {"link": "https://other.com/page"},
            {"link": "https://example.com/about"},
            {"link": "https://another.com/page"},
        ]
        assert _find_rank(items, "https://example.com") == 2

    def test_found_with_www(self):
        items = [
            {"link": "https://www.example.com/page"},
        ]
        assert _find_rank(items, "https://example.com") == 1

    def test_not_found(self):
        items = [
            {"link": "https://other.com/page"},
            {"link": "https://another.com/page"},
        ]
        assert _find_rank(items, "https://example.com") is None

    def test_empty_items(self):
        assert _find_rank([], "https://example.com") is None


# ── Google CSE ────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestGoogleCSE:
    async def test_google_cse_found_rank_3(self):
        """Google CSE returns target site at rank 3."""
        cse_response = {
            "items": [
                {"link": "https://other1.com/page", "title": "Other 1"},
                {"link": "https://other2.com/page", "title": "Other 2"},
                {"link": "https://example.com/en/dermatology", "title": "Example Clinic"},
                {"link": "https://other3.com/page", "title": "Other 3"},
            ]
        }
        with (
            patch("app.checks.international_search.settings") as mock_settings,
        ):
            mock_settings.pagespeed_api_key = "test-key"
            mock_settings.google_cse_id = "test-cse-id"
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""

            async with respx.mock:
                respx.get("https://www.googleapis.com/customsearch/v1").mock(
                    return_value=httpx.Response(200, json=cse_response)
                )
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text="<html><body></body></html>")
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                        specialty="피부과",
                    )

        assert r.name == "international_search"
        assert r.details["engines_checked"] > 0
        # At least one google engine found it
        found_any = any(
            v.get("rank") is not None
            for k, v in r.details["results"].items()
            if k.startswith("google_")
        )
        assert found_any

    async def test_google_cse_not_found(self):
        """Google CSE returns no matching results."""
        cse_response = {
            "items": [
                {"link": "https://other1.com/page", "title": "Other 1"},
                {"link": "https://other2.com/page", "title": "Other 2"},
            ]
        }
        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = "test-key"
            mock_settings.google_cse_id = "test-cse-id"
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""

            async with respx.mock:
                respx.get("https://www.googleapis.com/customsearch/v1").mock(
                    return_value=httpx.Response(200, json=cse_response)
                )
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text="<html><body></body></html>")
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        assert r.score == 0.0
        assert len(r.issues) > 0


# ── Naver ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestNaver:
    async def test_naver_found(self):
        """Naver API returns target site."""
        naver_response = {
            "items": [
                {"title": "Other", "link": "https://other.com"},
                {"title": "강남피부과", "link": "https://example.com/"},
            ]
        }
        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = ""
            mock_settings.google_cse_id = ""
            mock_settings.naver_client_id = "test-id"
            mock_settings.naver_client_secret = "test-secret"

            async with respx.mock:
                respx.get("https://openapi.naver.com/v1/search/webkw").mock(
                    return_value=httpx.Response(200, json=naver_response)
                )
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text="<html><body></body></html>")
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        naver = r.details["results"]["naver"]
        assert naver["rank"] == 2
        assert naver["score"] == 1.0

    async def test_naver_api_error(self):
        """Naver API returns error status."""
        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = ""
            mock_settings.google_cse_id = ""
            mock_settings.naver_client_id = "test-id"
            mock_settings.naver_client_secret = "test-secret"

            async with respx.mock:
                respx.get("https://openapi.naver.com/v1/search/webkw").mock(
                    return_value=httpx.Response(500)
                )
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text="<html><body></body></html>")
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        naver = r.details["results"]["naver"]
        assert naver.get("error") == "api_error"


# ── Baidu ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestBaidu:
    async def test_baidu_found_in_results(self):
        """Baidu HTML contains target domain in results."""
        baidu_html = """<html><body>
        <div class="result c-container">
            <a href="https://other.com/page">Other</a>
        </div>
        <div class="result c-container">
            <a href="https://example.com/clinic">강남피부과</a>
        </div>
        </body></html>"""

        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = ""
            mock_settings.google_cse_id = ""
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""

            async with respx.mock:
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text=baidu_html)
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        baidu = r.details["results"]["baidu"]
        assert baidu["rank"] == 2
        assert baidu["score"] == 1.0

    async def test_baidu_blocked(self):
        """Baidu returns non-200 status (blocked)."""
        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = ""
            mock_settings.google_cse_id = ""
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""

            async with respx.mock:
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(403)
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        baidu = r.details["results"]["baidu"]
        assert baidu.get("error") == "status_403"


# ── Graceful skip ─────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestGracefulSkip:
    async def test_no_hospital_name(self):
        """Should skip when hospital_name is empty."""
        async with httpx.AsyncClient() as client:
            r = await check_international_search(client, "https://example.com")
        assert r.grade == Grade.FAIL
        assert r.details.get("skipped") is True

    async def test_no_api_keys(self):
        """Should gracefully report when no API keys are configured."""
        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = ""
            mock_settings.google_cse_id = ""
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""

            async with respx.mock:
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(403)
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                    )

        assert r.grade == Grade.FAIL
        assert r.details.get("skipped") is True
        assert r.details["engines_checked"] == 0


# ── Integration (all engines mocked) ─────────────────────────────────


@pytest.mark.asyncio
class TestIntegration:
    async def test_full_scan_all_engines(self):
        """All engines configured and returning results."""
        cse_response_found = {
            "items": [
                {"link": "https://other.com/1", "title": "O1"},
                {"link": "https://other.com/2", "title": "O2"},
                {"link": "https://other.com/3", "title": "O3"},
                {"link": "https://other.com/4", "title": "O4"},
                {"link": "https://other.com/5", "title": "O5"},
                {"link": "https://other.com/6", "title": "O6"},
                {"link": "https://other.com/7", "title": "O7"},
                {"link": "https://example.com/clinic", "title": "강남피부과"},
                {"link": "https://other.com/9", "title": "O9"},
                {"link": "https://other.com/10", "title": "O10"},
            ]
        }
        naver_response = {
            "items": [
                {"title": "강남피부과", "link": "https://example.com/"},
            ]
        }
        baidu_html = """<html><body>
        <div class="result c-container">
            <a href="https://example.com/">강남피부과</a>
        </div>
        </body></html>"""

        with patch("app.checks.international_search.settings") as mock_settings:
            mock_settings.pagespeed_api_key = "test-key"
            mock_settings.google_cse_id = "test-cse-id"
            mock_settings.naver_client_id = "test-id"
            mock_settings.naver_client_secret = "test-secret"

            async with respx.mock:
                respx.get("https://www.googleapis.com/customsearch/v1").mock(
                    return_value=httpx.Response(200, json=cse_response_found)
                )
                respx.get("https://openapi.naver.com/v1/search/webkw").mock(
                    return_value=httpx.Response(200, json=naver_response)
                )
                respx.get("https://www.baidu.com/s").mock(
                    return_value=httpx.Response(200, text=baidu_html)
                )

                async with httpx.AsyncClient() as client:
                    r = await check_international_search(
                        client,
                        "https://example.com",
                        hospital_name="강남피부과",
                        specialty="피부과",
                        region="강남",
                    )

        assert r.name == "international_search"
        assert r.score > 0.0
        assert r.details["engines_checked"] == 8
        assert r.details["engines_available"] == 8

        # All engines should have results
        for key in ["google_jp", "google_tw", "google_sg", "google_my",
                     "google_th", "google_vn", "naver", "baidu"]:
            assert key in r.details["results"]

        # Naver found at rank 1
        assert r.details["results"]["naver"]["rank"] == 1
        assert r.details["results"]["naver"]["score"] == 1.0

        # Baidu found at rank 1
        assert r.details["results"]["baidu"]["rank"] == 1

        # Google found at rank 8 (top 10)
        for country_key in ["google_jp", "google_tw", "google_sg",
                            "google_my", "google_th", "google_vn"]:
            assert r.details["results"][country_key]["rank"] == 8
            assert r.details["results"][country_key]["score"] == 1.0

        # Summary present
        assert "summary" in r.details
        assert r.grade == Grade.PASS
