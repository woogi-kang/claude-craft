"""SERP checker: check keyword rankings on Naver and Google."""

import logging
from collections import defaultdict
from datetime import datetime, timedelta
from urllib.parse import urlparse

import httpx

from ..config import settings
from ..db.supabase import get_supabase_client

logger = logging.getLogger("checkyourhospital.serp_checker")

_CACHE_TTL_DAYS = 7
_NAVER_SEARCH_URL = "https://openapi.naver.com/v1/search/webkeyword.json"
_SERPER_SEARCH_URL = "https://google.serper.dev/search"


async def check_keyword_rankings(
    hospital_url: str,
    keywords: list[dict],
) -> dict:
    """Check keyword rankings on Naver/Google for the given hospital URL.

    Args:
        hospital_url: Hospital website URL.
        keywords: List of keyword dicts from keyword_engine, each with at least
                  "keyword" and "language" keys.

    Returns:
        Dict with results, summary, and competitors_in_serp.
    """
    has_naver = bool(settings.naver_client_id and settings.naver_client_secret)
    has_google = bool(settings.serper_api_key)

    results: list[dict] = []
    competitor_counts: dict[str, dict] = defaultdict(
        lambda: {"appearances": 0, "ranks": [], "name": ""}
    )

    async with httpx.AsyncClient(timeout=15) as client:
        for kw_entry in keywords:
            keyword = kw_entry.get("keyword", "")
            language = kw_entry.get("language", "ko")
            if not keyword:
                continue

            entry: dict = {
                "keyword": keyword,
                "language": language,
                "naver": {"rank": None, "cached": False},
                "google": {"rank": None, "cached": False},
            }

            # --- Naver ---
            if has_naver:
                naver_results, cached = await _get_or_fetch(
                    client, keyword, "naver", _search_naver
                )
                entry["naver"]["cached"] = cached
                if naver_results is not None:
                    entry["naver"]["rank"] = _find_rank(naver_results, hospital_url)
                    _collect_competitors(
                        naver_results, hospital_url, competitor_counts
                    )

            # --- Google ---
            if has_google:
                google_results, cached = await _get_or_fetch(
                    client, keyword, "google", _search_google
                )
                entry["google"]["cached"] = cached
                if google_results is not None:
                    entry["google"]["rank"] = _find_rank(google_results, hospital_url)
                    _collect_competitors(
                        google_results, hospital_url, competitor_counts
                    )

            results.append(entry)

    summary = _build_summary(results)
    competitors = _build_competitors(competitor_counts)

    return {
        "hospital_url": hospital_url,
        "results": results,
        "summary": summary,
        "competitors_in_serp": competitors,
    }


# ---------------------------------------------------------------------------
# Search API helpers
# ---------------------------------------------------------------------------

async def _search_naver(client: httpx.AsyncClient, keyword: str) -> list[dict] | None:
    """Call Naver Search API and return list of {title, link, description}."""
    try:
        resp = await client.get(
            _NAVER_SEARCH_URL,
            params={"query": keyword, "display": 50, "start": 1},
            headers={
                "X-Naver-Client-Id": settings.naver_client_id,
                "X-Naver-Client-Secret": settings.naver_client_secret,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {"title": item.get("title", ""), "link": item.get("link", "")}
            for item in data.get("items", [])
        ]
    except Exception as e:
        logger.warning("Naver search failed for '%s': %s", keyword, e)
        return None


async def _search_google(client: httpx.AsyncClient, keyword: str) -> list[dict] | None:
    """Call Serper.dev API and return list of {title, link, position}."""
    try:
        resp = await client.post(
            _SERPER_SEARCH_URL,
            json={"q": keyword, "gl": "kr", "hl": "ko", "num": 50},
            headers={"X-API-KEY": settings.serper_api_key},
        )
        resp.raise_for_status()
        data = resp.json()
        return [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "position": item.get("position", i + 1),
            }
            for i, item in enumerate(data.get("organic", []))
        ]
    except Exception as e:
        logger.warning("Google search failed for '%s': %s", keyword, e)
        return None


# ---------------------------------------------------------------------------
# Rank extraction
# ---------------------------------------------------------------------------

def _find_rank(results: list[dict], hospital_url: str) -> int | None:
    """Find the rank of hospital_url's domain in search results."""
    target_domain = _extract_domain(hospital_url)
    for i, item in enumerate(results, 1):
        item_domain = _extract_domain(item.get("link", ""))
        if target_domain in item_domain or item_domain in target_domain:
            return i
    return None


def _extract_domain(url: str) -> str:
    """Extract lowercase domain without www. prefix."""
    try:
        return urlparse(url).netloc.lower().replace("www.", "")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Competitor collection
# ---------------------------------------------------------------------------

def _collect_competitors(
    results: list[dict],
    hospital_url: str,
    counts: dict[str, dict],
) -> None:
    """Accumulate competitor domain appearances from search results."""
    target_domain = _extract_domain(hospital_url)
    for i, item in enumerate(results, 1):
        domain = _extract_domain(item.get("link", ""))
        if not domain or domain == target_domain:
            continue
        if target_domain in domain or domain in target_domain:
            continue
        counts[domain]["appearances"] += 1
        counts[domain]["ranks"].append(i)
        if not counts[domain]["name"]:
            counts[domain]["name"] = item.get("title", domain)


def _build_competitors(counts: dict[str, dict]) -> list[dict]:
    """Build sorted competitor list from accumulated counts."""
    competitors = []
    for domain, info in counts.items():
        if info["appearances"] < 1:
            continue
        avg_rank = sum(info["ranks"]) / len(info["ranks"]) if info["ranks"] else 0
        competitors.append({
            "domain": domain,
            "name": info["name"],
            "appearances": info["appearances"],
            "avg_rank": round(avg_rank, 1),
        })
    competitors.sort(key=lambda c: (-c["appearances"], c["avg_rank"]))
    return competitors[:20]


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def _build_summary(results: list[dict]) -> dict:
    """Build summary statistics from keyword ranking results."""
    naver_ranks = [r["naver"]["rank"] for r in results if r["naver"]["rank"] is not None]
    google_ranks = [r["google"]["rank"] for r in results if r["google"]["rank"] is not None]

    best_keyword = None
    worst_keyword = None
    best_rank = float("inf")
    worst_rank = 0

    for r in results:
        for portal in ("naver", "google"):
            rank = r[portal]["rank"]
            if rank is not None and rank < best_rank:
                best_rank = rank
                best_keyword = {"keyword": r["keyword"], "portal": portal, "rank": rank}
            if rank is not None and rank > worst_rank:
                worst_rank = rank
                worst_keyword = {"keyword": r["keyword"], "portal": portal, "rank": rank}

    # If no ranks found, pick first keyword as worst with null rank
    if worst_keyword is None and results:
        worst_keyword = {
            "keyword": results[0]["keyword"],
            "portal": "naver",
            "rank": None,
        }

    return {
        "naver_avg_rank": round(sum(naver_ranks) / len(naver_ranks), 1) if naver_ranks else None,
        "google_avg_rank": round(sum(google_ranks) / len(google_ranks), 1) if google_ranks else None,
        "keywords_found_naver": len(naver_ranks),
        "keywords_found_google": len(google_ranks),
        "keywords_total": len(results),
        "best_keyword": best_keyword,
        "worst_keyword": worst_keyword,
    }


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

async def _get_or_fetch(
    client: httpx.AsyncClient,
    keyword: str,
    portal: str,
    fetch_fn,
) -> tuple[list[dict] | None, bool]:
    """Return (results, cached). Try cache first, then fetch and save."""
    cached = await _get_cached(keyword, portal)
    if cached is not None:
        return cached, True

    results = await fetch_fn(client, keyword)
    if results is not None:
        await _save_cache(keyword, portal, results)
    return results, False


async def _get_cached(keyword: str, portal: str) -> list[dict] | None:
    """Get cached SERP results if not expired (7-day TTL)."""
    try:
        sb = get_supabase_client()
        if sb is None:
            return None
        result = (
            sb.table("serp_cache")
            .select("results")
            .eq("keyword", keyword)
            .eq("portal", portal)
            .gte("expires_at", datetime.now().isoformat())
            .single()
            .execute()
        )
        if result.data:
            return result.data["results"]
    except Exception:
        pass
    return None


async def _save_cache(keyword: str, portal: str, results: list[dict]) -> None:
    """Upsert SERP results into cache with 7-day TTL."""
    try:
        sb = get_supabase_client()
        if sb is None:
            return
        now = datetime.now()
        sb.table("serp_cache").upsert(
            {
                "keyword": keyword,
                "portal": portal,
                "results": results,
                "checked_at": now.isoformat(),
                "expires_at": (now + timedelta(days=_CACHE_TTL_DAYS)).isoformat(),
            },
            on_conflict="keyword,portal",
        ).execute()
    except Exception as e:
        logger.warning("Failed to save SERP cache: %s", e)
