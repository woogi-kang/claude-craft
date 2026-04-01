"""Tests for SERP checker service."""

import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.services.serp_checker import (
    _build_competitors,
    _build_summary,
    _collect_competitors,
    _extract_domain,
    _find_rank,
    check_keyword_rankings,
)

HOSPITAL_URL = "https://hongdae.doctorpetit.com"


def _make_response(status_code: int, json_data: dict) -> httpx.Response:
    """Create an httpx.Response with a request object set (needed for raise_for_status)."""
    resp = httpx.Response(
        status_code,
        json=json_data,
        request=httpx.Request("GET", "https://test.example.com"),
    )
    return resp
KEYWORDS = [
    {"keyword": "홍대 보톡스", "language": "ko"},
    {"keyword": "홍대 피부과", "language": "ko"},
    {"keyword": "홍대 포텐자", "language": "ko"},
]


# ---------------------------------------------------------------------------
# _find_rank / _extract_domain
# ---------------------------------------------------------------------------

class TestFindRank:
    def test_exact_domain_match(self):
        results = [
            {"link": "https://b-skin.com/page"},
            {"link": "https://hongdae.doctorpetit.com/botox"},
            {"link": "https://c-clinic.kr/page"},
        ]
        assert _find_rank(results, HOSPITAL_URL) == 2

    def test_subdomain_match(self):
        results = [
            {"link": "https://other.com"},
            {"link": "https://www.doctorpetit.com/hongdae"},
        ]
        # "doctorpetit.com" is in "hongdae.doctorpetit.com"
        assert _find_rank(results, HOSPITAL_URL) == 2

    def test_no_match_returns_none(self):
        results = [
            {"link": "https://b-skin.com"},
            {"link": "https://c-clinic.kr"},
        ]
        assert _find_rank(results, HOSPITAL_URL) is None

    def test_empty_results(self):
        assert _find_rank([], HOSPITAL_URL) is None

    def test_www_stripped(self):
        results = [{"link": "https://www.hongdae.doctorpetit.com/page"}]
        assert _find_rank(results, HOSPITAL_URL) == 1


class TestExtractDomain:
    def test_basic(self):
        assert _extract_domain("https://www.example.com/path") == "example.com"

    def test_no_www(self):
        assert _extract_domain("https://example.com") == "example.com"

    def test_empty(self):
        assert _extract_domain("") == ""

    def test_invalid(self):
        assert _extract_domain("not-a-url") == ""


# ---------------------------------------------------------------------------
# Competitor collection
# ---------------------------------------------------------------------------

class TestCollectCompetitors:
    def test_collects_non_hospital_domains(self):
        results = [
            {"link": "https://b-skin.com/page", "title": "B피부과"},
            {"link": "https://hongdae.doctorpetit.com/botox", "title": "닥터쁘띠"},
            {"link": "https://c-clinic.kr/page", "title": "C클리닉"},
            {"link": "https://b-skin.com/other", "title": "B피부과 - 기타"},
        ]
        counts: dict = {}
        from collections import defaultdict

        counts = defaultdict(lambda: {"appearances": 0, "ranks": [], "name": ""})
        _collect_competitors(results, HOSPITAL_URL, counts)

        assert counts["b-skin.com"]["appearances"] == 2
        assert counts["c-clinic.kr"]["appearances"] == 1
        assert "hongdae.doctorpetit.com" not in counts

    def test_build_competitors_sorted(self):
        counts = {
            "a.com": {"appearances": 2, "ranks": [3, 5], "name": "A"},
            "b.com": {"appearances": 5, "ranks": [1, 2, 3, 4, 5], "name": "B"},
            "c.com": {"appearances": 2, "ranks": [1, 2], "name": "C"},
        }
        result = _build_competitors(counts)
        assert result[0]["domain"] == "b.com"
        assert result[0]["avg_rank"] == 3.0
        # Same appearances → sorted by avg_rank ascending
        assert result[1]["domain"] == "c.com"
        assert result[2]["domain"] == "a.com"


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

class TestBuildSummary:
    def test_with_ranks(self):
        results = [
            {"keyword": "kw1", "language": "ko", "naver": {"rank": 5}, "google": {"rank": 10}},
            {"keyword": "kw2", "language": "ko", "naver": {"rank": 15}, "google": {"rank": None}},
        ]
        summary = _build_summary(results)
        assert summary["naver_avg_rank"] == 10.0
        assert summary["google_avg_rank"] == 10.0
        assert summary["keywords_found_naver"] == 2
        assert summary["keywords_found_google"] == 1
        assert summary["keywords_total"] == 2
        assert summary["best_keyword"]["rank"] == 5
        assert summary["worst_keyword"]["rank"] == 15

    def test_all_none_ranks(self):
        results = [
            {"keyword": "kw1", "language": "ko", "naver": {"rank": None}, "google": {"rank": None}},
        ]
        summary = _build_summary(results)
        assert summary["naver_avg_rank"] is None
        assert summary["google_avg_rank"] is None
        assert summary["best_keyword"] is None
        assert summary["worst_keyword"]["rank"] is None

    def test_empty_results(self):
        summary = _build_summary([])
        assert summary["keywords_total"] == 0
        assert summary["best_keyword"] is None
        assert summary["worst_keyword"] is None


# ---------------------------------------------------------------------------
# Naver API mock
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSearchNaver:
    async def test_naver_api_success(self):
        naver_response = {
            "items": [
                {"title": "B피부과", "link": "https://b-skin.com"},
                {"title": "닥터쁘띠 홍대", "link": "https://hongdae.doctorpetit.com/botox"},
            ]
        }

        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = "test-id"
            mock_settings.naver_client_secret = "test-secret"
            mock_settings.serper_api_key = ""

            with patch("app.services.serp_checker.get_supabase_client", return_value=None):
                mock_resp = _make_response(200, naver_response)

                with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
                    result = await check_keyword_rankings(
                        HOSPITAL_URL,
                        [{"keyword": "홍대 보톡스", "language": "ko"}],
                    )

        assert len(result["results"]) == 1
        assert result["results"][0]["naver"]["rank"] == 2
        assert result["results"][0]["google"]["rank"] is None

    async def test_naver_api_failure_graceful(self):
        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = "test-id"
            mock_settings.naver_client_secret = "test-secret"
            mock_settings.serper_api_key = ""

            with patch("app.services.serp_checker.get_supabase_client", return_value=None):
                with patch(
                    "httpx.AsyncClient.get",
                    new_callable=AsyncMock,
                    side_effect=httpx.HTTPStatusError(
                        "500", request=MagicMock(), response=MagicMock(status_code=500)
                    ),
                ):
                    result = await check_keyword_rankings(
                        HOSPITAL_URL,
                        [{"keyword": "홍대 보톡스", "language": "ko"}],
                    )

        assert result["results"][0]["naver"]["rank"] is None


# ---------------------------------------------------------------------------
# Serper (Google) API mock
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSearchGoogle:
    async def test_serper_api_success(self):
        serper_response = {
            "organic": [
                {"title": "C클리닉", "link": "https://c-clinic.kr", "position": 1},
                {"title": "닥터쁘띠", "link": "https://hongdae.doctorpetit.com", "position": 2},
            ]
        }

        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""
            mock_settings.serper_api_key = "test-serper-key"

            with patch("app.services.serp_checker.get_supabase_client", return_value=None):
                mock_resp = _make_response(200, serper_response)

                with patch("httpx.AsyncClient.post", new_callable=AsyncMock, return_value=mock_resp):
                    result = await check_keyword_rankings(
                        HOSPITAL_URL,
                        [{"keyword": "홍대 피부과", "language": "ko"}],
                    )

        assert result["results"][0]["google"]["rank"] == 2
        assert result["results"][0]["naver"]["rank"] is None


# ---------------------------------------------------------------------------
# Graceful degradation — no API keys
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestGracefulDegradation:
    async def test_no_api_keys_returns_empty(self):
        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = ""
            mock_settings.naver_client_secret = ""
            mock_settings.serper_api_key = ""

            result = await check_keyword_rankings(HOSPITAL_URL, KEYWORDS)

        assert len(result["results"]) == 3
        for r in result["results"]:
            assert r["naver"]["rank"] is None
            assert r["google"]["rank"] is None

    async def test_empty_keywords(self):
        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = "id"
            mock_settings.naver_client_secret = "secret"
            mock_settings.serper_api_key = ""

            result = await check_keyword_rankings(HOSPITAL_URL, [])

        assert result["results"] == []
        assert result["summary"]["keywords_total"] == 0


# ---------------------------------------------------------------------------
# Cache hit / miss
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestCache:
    async def test_cache_hit_skips_api_call(self):
        cached_results = [
            {"title": "Cached B피부과", "link": "https://b-skin.com"},
            {"title": "Cached 닥터쁘띠", "link": "https://hongdae.doctorpetit.com"},
        ]

        mock_sb = MagicMock()
        mock_sb.table.return_value = mock_sb
        mock_sb.select.return_value = mock_sb
        mock_sb.eq.return_value = mock_sb
        mock_sb.gte.return_value = mock_sb
        mock_sb.single.return_value = mock_sb
        mock_sb.execute.return_value = MagicMock(data={"results": cached_results})

        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = "id"
            mock_settings.naver_client_secret = "secret"
            mock_settings.serper_api_key = ""

            with patch("app.services.serp_checker.get_supabase_client", return_value=mock_sb):
                with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
                    result = await check_keyword_rankings(
                        HOSPITAL_URL,
                        [{"keyword": "홍대 보톡스", "language": "ko"}],
                    )
                    # API should NOT have been called since cache hit
                    mock_get.assert_not_called()

        assert result["results"][0]["naver"]["cached"] is True
        assert result["results"][0]["naver"]["rank"] == 2

    async def test_cache_miss_calls_api(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value = mock_sb
        mock_sb.select.return_value = mock_sb
        mock_sb.eq.return_value = mock_sb
        mock_sb.gte.return_value = mock_sb
        mock_sb.single.return_value = mock_sb
        mock_sb.upsert.return_value = mock_sb
        # Cache miss
        mock_sb.execute.return_value = MagicMock(data=None)

        naver_response = {
            "items": [
                {"title": "닥터쁘띠", "link": "https://hongdae.doctorpetit.com"},
            ]
        }

        with patch("app.services.serp_checker.settings") as mock_settings:
            mock_settings.naver_client_id = "id"
            mock_settings.naver_client_secret = "secret"
            mock_settings.serper_api_key = ""

            with patch("app.services.serp_checker.get_supabase_client", return_value=mock_sb):
                mock_resp = _make_response(200, naver_response)
                with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
                    result = await check_keyword_rankings(
                        HOSPITAL_URL,
                        [{"keyword": "홍대 보톡스", "language": "ko"}],
                    )

        assert result["results"][0]["naver"]["cached"] is False
        assert result["results"][0]["naver"]["rank"] == 1
