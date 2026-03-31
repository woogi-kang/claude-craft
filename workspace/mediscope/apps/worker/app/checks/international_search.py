"""International search engine visibility check."""

import logging
from urllib.parse import quote_plus, urlparse

import httpx

from ..checks.base import CheckResult, Grade
from ..config import settings

logger = logging.getLogger("checkyourhospital.checks.international_search")

_DISPLAY_NAME = "해외 검색엔진 노출"
_DESCRIPTION = "일본/대만/동남아 구글, 네이버, 바이두에서 병원이 검색되는지 확인합니다"
_RECOMMENDATION = (
    "타겟 국가 언어로 페이지를 만들고, Google Search Console에서 해당 국가 타겟팅을 설정하세요"
)

# Country configurations: (engine_key, country_code, language, search_category_template)
GOOGLE_COUNTRIES: list[dict] = [
    {
        "key": "google_jp",
        "gl": "jp",
        "hl": "ja",
        "label": "일본",
        "category_query": "韓国 {specialty} クリニック",
    },
    {
        "key": "google_tw",
        "gl": "tw",
        "hl": "zh-TW",
        "label": "대만",
        "category_query": "韓國 {specialty} 診所",
    },
    {
        "key": "google_sg",
        "gl": "sg",
        "hl": "en",
        "label": "싱가포르",
        "category_query": "{specialty} clinic in Korea",
    },
    {
        "key": "google_my",
        "gl": "my",
        "hl": "en",
        "label": "말레이시아",
        "category_query": "{specialty} clinic in Korea",
    },
    {
        "key": "google_th",
        "gl": "th",
        "hl": "th",
        "label": "태국",
        "category_query": "คลินิก {specialty} เกาหลี",
    },
    {
        "key": "google_vn",
        "gl": "vn",
        "hl": "vi",
        "label": "베트남",
        "category_query": "phẫu thuật {specialty} Hàn Quốc",
    },
]

GOOGLE_CSE_URL = "https://www.googleapis.com/customsearch/v1"
NAVER_SEARCH_URL = "https://openapi.naver.com/v1/search/webkw"
BAIDU_URL = "https://www.baidu.com/s"


def _rank_to_score(rank: int | None) -> float:
    """Convert search rank to 0.0-1.0 score."""
    if rank is None:
        return 0.0
    if rank <= 10:
        return 1.0
    if rank <= 30:
        return 0.7
    if rank <= 100:
        return 0.3
    return 0.0


def _find_rank(items: list[dict], url: str) -> int | None:
    """Find rank of target URL in search results."""
    domain = urlparse(url).netloc.lower().replace("www.", "")

    for i, item in enumerate(items, 1):
        link = item.get("link", "")
        item_domain = urlparse(link).netloc.lower().replace("www.", "")
        if domain == item_domain or domain in item_domain or item_domain in domain:
            return i
    return None


async def _search_google_cse(
    client: httpx.AsyncClient,
    query: str,
    gl: str,
    hl: str,
    url: str,
    *,
    start: int = 1,
) -> tuple[int | None, list[dict]]:
    """Search Google CSE and return (rank, raw_items)."""
    api_key = settings.pagespeed_api_key
    cse_id = settings.google_cse_id
    if not api_key or not cse_id:
        return None, []

    try:
        resp = await client.get(
            GOOGLE_CSE_URL,
            params={
                "key": api_key,
                "cx": cse_id,
                "q": query,
                "gl": gl,
                "hl": hl,
                "num": 10,
                "start": start,
            },
            timeout=15,
        )
        if resp.status_code != 200:
            logger.warning(f"Google CSE returned {resp.status_code} for gl={gl}")
            return None, []

        data = resp.json()
        items = data.get("items", [])
        rank = _find_rank(items, url)
        # Adjust rank for pagination
        if rank is not None:
            rank += start - 1
        return rank, items
    except Exception as e:
        logger.warning(f"Google CSE error (gl={gl}): {e}")
        return None, []


async def _check_google_country(
    client: httpx.AsyncClient,
    url: str,
    hospital_name: str,
    specialty: str,
    country: dict,
) -> dict:
    """Check visibility in one Google country variant."""
    api_key = settings.pagespeed_api_key
    cse_id = settings.google_cse_id
    if not api_key or not cse_id:
        return {"rank": None, "score": 0.0, "query": "", "skipped": True}

    # Try direct search first
    query = hospital_name
    rank, _ = await _search_google_cse(
        client, query, country["gl"], country["hl"], url
    )

    best_rank = rank
    best_query = query

    # If not found in top 10, try category search
    if rank is None or rank > 10:
        if specialty:
            cat_query = country["category_query"].format(specialty=specialty)
            cat_rank, _ = await _search_google_cse(
                client, cat_query, country["gl"], country["hl"], url
            )
            if cat_rank is not None and (best_rank is None or cat_rank < best_rank):
                best_rank = cat_rank
                best_query = cat_query

    return {
        "rank": best_rank,
        "score": _rank_to_score(best_rank),
        "query": best_query,
    }


async def _check_naver(
    client: httpx.AsyncClient,
    url: str,
    hospital_name: str,
) -> dict:
    """Check visibility in Naver search."""
    client_id = settings.naver_client_id
    client_secret = settings.naver_client_secret
    if not client_id or not client_secret:
        return {"rank": None, "score": 0.0, "query": "", "skipped": True}

    query = hospital_name
    try:
        resp = await client.get(
            NAVER_SEARCH_URL,
            params={"query": query, "display": 10},
            headers={
                "X-Naver-Client-Id": client_id,
                "X-Naver-Client-Secret": client_secret,
            },
            timeout=15,
        )
        if resp.status_code != 200:
            logger.warning(f"Naver API returned {resp.status_code}")
            return {"rank": None, "score": 0.0, "query": query, "error": "api_error"}

        data = resp.json()
        items = data.get("items", [])
        domain = urlparse(url).netloc.lower().replace("www.", "")

        rank = None
        for i, item in enumerate(items, 1):
            link = item.get("link", "")
            item_domain = urlparse(link).netloc.lower().replace("www.", "")
            if domain == item_domain or domain in item_domain or item_domain in domain:
                rank = i
                break

        return {
            "rank": rank,
            "score": _rank_to_score(rank),
            "query": query,
        }
    except Exception as e:
        logger.warning(f"Naver search error: {e}")
        return {"rank": None, "score": 0.0, "query": query, "error": str(e)}


async def _check_baidu(
    client: httpx.AsyncClient,
    url: str,
    hospital_name: str,
) -> dict:
    """Check visibility in Baidu search (best-effort scraping)."""
    query = hospital_name
    try:
        resp = await client.get(
            BAIDU_URL,
            params={"wd": query},
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
            timeout=15,
        )
        if resp.status_code != 200:
            return {
                "rank": None,
                "score": 0.0,
                "query": query,
                "error": f"status_{resp.status_code}",
            }

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(resp.text, "html.parser")
        domain = urlparse(url).netloc.lower().replace("www.", "")

        # Baidu search results are in div.result elements
        results = soup.select("div.result, div.c-container")
        rank = None
        for i, result in enumerate(results[:10], 1):
            # Check links within the result
            links = result.find_all("a", href=True)
            for link in links:
                href = link.get("href", "")
                link_text = link.get_text(strip=True).lower()
                # Baidu often uses redirect URLs, so also check text
                link_domain = urlparse(href).netloc.lower().replace("www.", "")
                if (
                    domain in link_domain
                    or link_domain in domain
                    or domain in link_text
                    or domain in href
                ):
                    rank = i
                    break
            if rank is not None:
                break

        return {
            "rank": rank,
            "score": _rank_to_score(rank),
            "query": query,
        }
    except Exception as e:
        logger.warning(f"Baidu search error: {e}")
        return {
            "rank": None,
            "score": 0.0,
            "query": query,
            "error": str(e),
        }


async def check_international_search(
    client: httpx.AsyncClient,
    url: str,
    hospital_name: str = "",
    specialty: str = "",
    region: str = "",
) -> CheckResult:
    """Check hospital visibility in international search engines."""
    if not hospital_name:
        return CheckResult(
            name="international_search",
            score=0.0,
            grade=Grade.FAIL,
            fail_type="system_limit",
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["병원명 정보가 없어 국제 검색 체크를 수행할 수 없습니다"],
            details={"skipped": True},
        )

    results: dict[str, dict] = {}
    engines_available = 8  # Total possible engines
    engines_checked = 0

    # Google country searches
    has_google_keys = bool(settings.pagespeed_api_key and settings.google_cse_id)
    if has_google_keys:
        for country in GOOGLE_COUNTRIES:
            result = await _check_google_country(
                client, url, hospital_name, specialty, country
            )
            results[country["key"]] = result
            if not result.get("skipped"):
                engines_checked += 1
    else:
        for country in GOOGLE_COUNTRIES:
            results[country["key"]] = {
                "rank": None,
                "score": 0.0,
                "query": "",
                "skipped": True,
            }

    # Naver
    naver_result = await _check_naver(client, url, hospital_name)
    results["naver"] = naver_result
    if not naver_result.get("skipped"):
        engines_checked += 1

    # Baidu (best-effort)
    baidu_result = await _check_baidu(client, url, hospital_name)
    results["baidu"] = baidu_result
    if not baidu_result.get("skipped") and not baidu_result.get("error"):
        engines_checked += 1

    # Calculate average score from checked engines only
    checked_scores = [
        r["score"]
        for r in results.values()
        if not r.get("skipped") and "error" not in r
    ]

    if not checked_scores:
        return CheckResult(
            name="international_search",
            score=0.0,
            grade=Grade.FAIL,
            fail_type="system_limit",
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["사용 가능한 검색 API가 없습니다 (GOOGLE_CSE_ID, NAVER_CLIENT_ID 설정 필요)"],
            details={
                "skipped": True,
                "engines_checked": 0,
                "engines_available": engines_available,
                "results": results,
            },
        )

    avg_score = sum(checked_scores) / len(checked_scores)

    # Check for API errors in individual engines
    has_api_errors = any(r.get("error") for r in results.values())

    # Generate issues
    issues: list[str] = []
    not_found_engines: list[str] = []
    for key, r in results.items():
        if r.get("skipped"):
            continue
        if r.get("error"):
            continue
        if r["rank"] is None:
            label = key.replace("google_", "Google ").replace("_", " ").title()
            not_found_engines.append(label)

    if not_found_engines:
        engine_list = ", ".join(not_found_engines)
        issues.append(
            f"{engine_list}에서 노출되지 않습니다. 해당 언어 페이지 추가를 권장합니다."
        )

    # Determine grade
    if avg_score >= 0.7:
        grade = Grade.PASS
    elif avg_score >= 0.3:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    # Determine fail_type based on API errors
    fail_type = "site_issue"
    if has_api_errors:
        fail_type = "api_error"

    # Summary
    found_count = sum(
        1
        for r in results.values()
        if not r.get("skipped") and not r.get("error") and r["rank"] is not None
    )
    summary = f"{engines_available}개 검색엔진 중 {engines_checked}개 체크, {found_count}개에서 노출 확인"

    return CheckResult(
        name="international_search",
        score=round(avg_score, 2),
        grade=grade,
        fail_type=fail_type,
        display_name=_DISPLAY_NAME,
        description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        issues=issues,
        details={
            "engines_checked": engines_checked,
            "engines_available": engines_available,
            "results": results,
            "summary": summary,
        },
    )
