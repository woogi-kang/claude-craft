"""Tests for GEO/AEO AI search mention checks."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.checks.geo_aeo import (
    _build_queries,
    _check_mention,
    _query_gemini,
    _query_perplexity,
    check_ai_search_mention,
    check_content_clarity,
)


# --- _build_queries ---


def test_build_queries_basic():
    queries = _build_queries("미소클리닉")
    assert "미소클리닉" in queries


def test_build_queries_with_region_specialty():
    queries = _build_queries("미소클리닉", specialty="피부과", region="강남")
    assert any("강남" in q for q in queries)
    assert any("피부과" in q for q in queries)


def test_build_queries_empty_name():
    queries = _build_queries("")
    assert queries == []


# --- _check_mention ---


def test_check_mention_full_name():
    score = _check_mention(
        "미소클리닉은 강남에서 추천하는 피부과입니다.",
        "미소클리닉",
        "https://misoclinic.com",
    )
    assert score == 1.0


def test_check_mention_domain():
    score = _check_mention(
        "misoclinic.com에서 확인하세요.",
        "다른이름",
        "https://misoclinic.com",
    )
    assert score == 1.0


def test_check_mention_partial():
    score = _check_mention(
        "미소 피부과에서 시술받으세요.",
        "미소클리닉 피부과",
        "https://misoclinic.com",
    )
    assert score == 0.5


def test_check_mention_none():
    score = _check_mention(
        "강남에 좋은 병원이 많습니다.",
        "미소클리닉",
        "https://misoclinic.com",
    )
    assert score == 0.0


def test_check_mention_empty_text():
    score = _check_mention("", "미소클리닉", "https://misoclinic.com")
    assert score == 0.0


# --- _query_gemini ---


@pytest.mark.asyncio
async def test_query_gemini_success():
    mock_response = httpx.Response(
        200,
        json={
            "candidates": [
                {"content": {"parts": [{"text": "미소클리닉을 추천합니다."}]}}
            ]
        },
    )

    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(return_value=mock_response)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = "test-key"
        result = await _query_gemini(client, "강남 피부과 추천")

    assert result == "미소클리닉을 추천합니다."


@pytest.mark.asyncio
async def test_query_gemini_no_api_key():
    client = AsyncMock(spec=httpx.AsyncClient)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = ""
        result = await _query_gemini(client, "강남 피부과 추천")

    assert result is None


@pytest.mark.asyncio
async def test_query_gemini_api_error():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(side_effect=httpx.ConnectError("timeout"))

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = "test-key"
        result = await _query_gemini(client, "강남 피부과 추천")

    assert result is None


# --- _query_perplexity ---


@pytest.mark.asyncio
async def test_query_perplexity_success():
    mock_response = httpx.Response(
        200,
        json={
            "choices": [
                {"message": {"content": "미소클리닉은 강남 최고의 피부과입니다."}}
            ]
        },
    )

    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(return_value=mock_response)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.perplexity_api_key = "test-key"
        result = await _query_perplexity(client, "강남 피부과 추천")

    assert "미소클리닉" in result


@pytest.mark.asyncio
async def test_query_perplexity_no_api_key():
    client = AsyncMock(spec=httpx.AsyncClient)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.perplexity_api_key = ""
        result = await _query_perplexity(client, "강남 피부과 추천")

    assert result is None


# --- check_ai_search_mention (integration) ---


@pytest.mark.asyncio
async def test_ai_search_no_hospital_name():
    client = AsyncMock(spec=httpx.AsyncClient)
    result = await check_ai_search_mention(client, "https://example.com", "")
    assert result.name == "ai_search_mention"
    assert result.fail_type == "system_limit"
    assert result.score == 0.0


@pytest.mark.asyncio
async def test_ai_search_no_api_keys():
    client = AsyncMock(spec=httpx.AsyncClient)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = ""
        mock_settings.perplexity_api_key = ""
        result = await check_ai_search_mention(
            client, "https://misoclinic.com", "미소클리닉"
        )

    assert result.fail_type == "system_limit"
    assert result.details.get("skipped") is True


@pytest.mark.asyncio
async def test_ai_search_gemini_only():
    """Gemini available, Perplexity not — should still score."""
    gemini_response = httpx.Response(
        200,
        json={
            "candidates": [
                {"content": {"parts": [{"text": "미소클리닉은 강남 추천 피부과입니다."}]}}
            ]
        },
    )

    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(return_value=gemini_response)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = "test-key"
        mock_settings.perplexity_api_key = ""
        result = await check_ai_search_mention(
            client, "https://misoclinic.com", "미소클리닉", "피부과", "강남"
        )

    assert result.score > 0
    assert "gemini" in result.details.get("engines_checked", [])
    assert result.fail_type == "site_issue"


@pytest.mark.asyncio
async def test_ai_search_both_engines():
    """Both Gemini and Perplexity available."""

    async def mock_post(url, **kwargs):
        if "generativelanguage" in url:
            return httpx.Response(
                200,
                json={
                    "candidates": [
                        {"content": {"parts": [{"text": "미소클리닉을 추천합니다."}]}}
                    ]
                },
            )
        if "perplexity" in url:
            return httpx.Response(
                200,
                json={
                    "choices": [
                        {"message": {"content": "강남에 좋은 병원이 많습니다."}}
                    ]
                },
            )
        return httpx.Response(404)

    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(side_effect=mock_post)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = "test-key"
        mock_settings.perplexity_api_key = "test-key"
        result = await check_ai_search_mention(
            client, "https://misoclinic.com", "미소클리닉", "피부과", "강남"
        )

    engines = result.details.get("engines_checked", [])
    assert "gemini" in engines
    assert "perplexity" in engines
    # Gemini mentions hospital (score 1.0, weight 0.4)
    # Perplexity doesn't mention (score 0.0, weight 0.3)
    # Weighted: 0.4*1.0 / (0.4+0.3) ≈ 0.57
    assert 0.3 <= result.score <= 0.8


@pytest.mark.asyncio
async def test_ai_search_details_structure():
    """Verify details dict has expected multi-engine structure."""
    gemini_response = httpx.Response(
        200,
        json={
            "candidates": [
                {"content": {"parts": [{"text": "미소클리닉은 좋은 병원입니다."}]}}
            ]
        },
    )

    client = AsyncMock(spec=httpx.AsyncClient)
    client.post = AsyncMock(return_value=gemini_response)

    with patch("app.checks.geo_aeo.settings") as mock_settings:
        mock_settings.gemini_api_key = "test-key"
        mock_settings.perplexity_api_key = ""
        result = await check_ai_search_mention(
            client, "https://misoclinic.com", "미소클리닉"
        )

    details = result.details
    assert "engines_checked" in details
    assert "gemini" in details
    assert "perplexity" in details
    assert "chatgpt" in details
    # Gemini should have mention data
    assert details["gemini"]["mentioned"] is True
    # Perplexity should indicate no API key
    assert details["perplexity"]["reason"] == "no_api_key"
    # ChatGPT not implemented
    assert details["chatgpt"]["reason"] == "not_implemented"


# --- content_clarity ---


def test_content_clarity_good(good_html):
    result = check_content_clarity(good_html)
    assert result.name == "content_clarity"
    assert result.score >= 0.5


def test_content_clarity_bad(bad_html):
    result = check_content_clarity(bad_html)
    assert result.name == "content_clarity"
    assert result.score < 0.3
