"""GEO/AEO checks: AI search engine mention detection."""

import logging
import re

import httpx

from ..checks.base import CheckResult, Grade
from ..config import settings

logger = logging.getLogger("mediscope.checks.geo_aeo")

# --- ai_search_mention ---
_AI_DISPLAY_NAME = "AI 검색 노출"
_AI_DESCRIPTION = "Gemini, ChatGPT, Perplexity 등 AI 검색에서 병원이 언급되는지 확인합니다"
_AI_RECOMMENDATION = (
    "홈페이지에 시술별 상세 설명, FAQ, 환자 후기를 충실히 작성하세요. "
    "AI가 참고할 수 있는 근거를 제공합니다"
)

# Weighted average weights per engine (sum to 1.0 when all present)
_ENGINE_WEIGHTS = {
    "gemini": 0.4,
    "perplexity": 0.3,
    "chatgpt": 0.3,
}

# --- content_clarity ---
_CC_DISPLAY_NAME = "콘텐츠 명확성"
_CC_DESCRIPTION = "페이지 내용이 AI와 검색엔진이 이해하기 좋은 구조인지 확인합니다"
_CC_RECOMMENDATION = (
    "Q&A 형식의 콘텐츠, 목록형 정리, 충분한 분량(300단어 이상)의 상세 설명을 추가하세요"
)


def _build_queries(hospital_name: str, specialty: str = "", region: str = "") -> list[str]:
    """Build search queries from hospital info."""
    queries = []
    if hospital_name:
        queries.append(hospital_name)
    if hospital_name and region:
        queries.append(f"{region} {specialty} 추천".strip())
        queries.append(f"best {specialty} clinic in {region}".strip())
    if hospital_name and specialty:
        queries.append(f"{hospital_name} {specialty}")
    return [q for q in queries if q]


def _check_mention(text: str, hospital_name: str, url: str) -> float:
    """Check if hospital is mentioned in AI response text.

    Returns 1.0 (full mention), 0.5 (partial), 0.0 (none).
    """
    if not text:
        return 0.0

    text_lower = text.lower()
    name_lower = hospital_name.lower()

    from urllib.parse import urlparse

    domain = urlparse(url).netloc.lower()

    # Full mention: name or domain found
    if name_lower in text_lower or domain in text_lower:
        return 1.0

    # Partial mention: URL path or partial name match
    name_parts = [p for p in re.split(r"[\s·\-]+", name_lower) if len(p) > 1]
    matched = sum(1 for part in name_parts if part in text_lower)
    if name_parts and matched / len(name_parts) >= 0.5:
        return 0.5

    return 0.0


async def _query_gemini(
    client: httpx.AsyncClient, query: str
) -> str | None:
    """Query Gemini API (REST) if key is available."""
    api_key = settings.gemini_api_key
    if not api_key:
        return None

    try:
        resp = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            params={"key": api_key},
            json={
                "contents": [{"parts": [{"text": query}]}],
                "generationConfig": {"maxOutputTokens": 512},
            },
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                return "".join(p.get("text", "") for p in parts)
    except Exception as e:
        logger.warning(f"Gemini API error: {e}")
    return None


async def _query_perplexity(
    client: httpx.AsyncClient, query: str
) -> str | None:
    """Query Perplexity API if key is available."""
    api_key = settings.perplexity_api_key
    if not api_key:
        return None

    try:
        resp = await client.post(
            "https://api.perplexity.ai/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 512,
            },
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        logger.warning(f"Perplexity API error: {e}")
    return None


async def _query_engine(
    client: httpx.AsyncClient,
    engine: str,
    queries: list[str],
    hospital_name: str,
    url: str,
) -> dict:
    """Query a single AI engine and return per-engine result dict."""
    query_fn = {"gemini": _query_gemini, "perplexity": _query_perplexity}.get(engine)
    if query_fn is None:
        return {"mentioned": None, "reason": "not_implemented"}

    scores: list[float] = []
    matched_queries: list[str] = []
    context_snippet: str = ""

    for query in queries[:2]:
        response_text = await query_fn(client, query)
        if response_text is not None:
            score = _check_mention(response_text, hospital_name, url)
            scores.append(score)
            matched_queries.append(query)
            if score > 0 and not context_snippet:
                context_snippet = response_text[:200]

    if not scores:
        return {"mentioned": None, "reason": "no_api_key", "queries": matched_queries}

    best = max(scores)
    result: dict = {
        "mentioned": best > 0,
        "score": round(best, 2),
        "queries": matched_queries,
    }
    if context_snippet:
        result["context"] = context_snippet
    return result


async def check_ai_search_mention(
    client: httpx.AsyncClient,
    url: str,
    hospital_name: str,
    specialty: str = "",
    region: str = "",
) -> CheckResult:
    """Check if the hospital is mentioned in AI search engines."""
    if not hospital_name:
        return CheckResult(
            name="ai_search_mention",
            score=0.0,
            grade=Grade.FAIL,
            fail_type="system_limit",
            display_name=_AI_DISPLAY_NAME,
            description=_AI_DESCRIPTION,
            recommendation=_AI_RECOMMENDATION,
            issues=["병원명 정보가 없어 AI 검색 체크를 수행할 수 없습니다"],
            details={"skipped": True},
        )

    queries = _build_queries(hospital_name, specialty, region)
    if not queries:
        return CheckResult(
            name="ai_search_mention",
            score=0.0,
            grade=Grade.FAIL,
            fail_type="system_limit",
            display_name=_AI_DISPLAY_NAME,
            description=_AI_DESCRIPTION,
            recommendation=_AI_RECOMMENDATION,
            issues=["검색 쿼리를 생성할 수 없습니다"],
        )

    # Query engines in priority order: Gemini → Perplexity → ChatGPT
    engines_checked: list[str] = []
    engine_results: dict[str, dict] = {}

    for engine in ("gemini", "perplexity", "chatgpt"):
        result = await _query_engine(client, engine, queries, hospital_name, url)
        engine_results[engine] = result
        if result.get("mentioned") is not None:
            engines_checked.append(engine)

    if not engines_checked:
        return CheckResult(
            name="ai_search_mention",
            score=0.0,
            grade=Grade.FAIL,
            fail_type="system_limit",
            display_name=_AI_DISPLAY_NAME,
            description=_AI_DESCRIPTION,
            recommendation=_AI_RECOMMENDATION,
            issues=[
                "AI 검색 API를 사용할 수 없습니다 "
                "(GEMINI_API_KEY 또는 PERPLEXITY_API_KEY 필요)"
            ],
            details={"skipped": True, "reason": "no_api_key"},
        )

    # Weighted average — only engines that were actually checked
    total_weight = sum(_ENGINE_WEIGHTS.get(e, 0) for e in engines_checked)
    weighted_score = sum(
        engine_results[e].get("score", 0.0) * _ENGINE_WEIGHTS.get(e, 0)
        for e in engines_checked
    )
    avg_score = weighted_score / total_weight if total_weight > 0 else 0.0

    if avg_score >= 0.8:
        grade = Grade.PASS
        issues = []
    elif avg_score >= 0.3:
        grade = Grade.WARN
        issues = ["AI 검색에서 부분적으로만 언급됩니다"]
    else:
        grade = Grade.FAIL
        issues = ["AI 검색 결과에서 병원이 언급되지 않습니다"]

    return CheckResult(
        name="ai_search_mention",
        score=round(avg_score, 2),
        grade=grade,
        display_name=_AI_DISPLAY_NAME,
        description=_AI_DESCRIPTION,
        recommendation=_AI_RECOMMENDATION,
        issues=issues,
        details={
            "engines_checked": engines_checked,
            "queries_used": queries[:2],
            **engine_results,
        },
    )


def check_content_clarity(html: str) -> CheckResult:
    """Check content clarity signals for AI engines."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    score = 0.0
    issues: list[str] = []
    details: dict = {}

    # Check for clear, structured content sections
    paragraphs = soup.find_all("p")
    word_count = sum(len(p.get_text(strip=True).split()) for p in paragraphs)
    details["word_count"] = word_count

    if word_count >= 300:
        score += 0.3
    elif word_count >= 100:
        score += 0.15
    else:
        issues.append("콘텐츠가 너무 짧습니다 (300단어 이상 권장)")

    # Check for lists (AI engines favor structured info)
    lists = soup.find_all(["ul", "ol"])
    details["list_count"] = len(lists)
    if lists:
        score += 0.2
    else:
        issues.append("목록 형태의 구조화된 콘텐츠가 없습니다")

    # Check for tables
    tables = soup.find_all("table")
    details["table_count"] = len(tables)
    if tables:
        score += 0.1

    # Check for clear headings with descriptive text
    headings = soup.find_all(["h1", "h2", "h3"])
    descriptive_headings = [
        h for h in headings if len(h.get_text(strip=True)) > 3
    ]
    details["heading_count"] = len(descriptive_headings)
    if len(descriptive_headings) >= 3:
        score += 0.2
    elif descriptive_headings:
        score += 0.1
    else:
        issues.append("설명적인 소제목이 부족합니다")

    # Check for Q&A style content (natural language queries)
    qa_patterns = re.compile(r"(무엇|어떻게|왜|언제|어디|how|what|why|when|where)\s*[?？]", re.I)
    text = soup.get_text()
    qa_matches = qa_patterns.findall(text)
    details["qa_pattern_count"] = len(qa_matches)
    if qa_matches:
        score += 0.2
    else:
        issues.append("Q&A 형식의 콘텐츠가 없습니다 (AI 검색에서 인용 확률 증가)")

    score = min(1.0, score)

    if score >= 0.7:
        grade = Grade.PASS
    elif score >= 0.4:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="content_clarity",
        score=round(score, 2),
        grade=grade,
        display_name=_CC_DISPLAY_NAME,
        description=_CC_DESCRIPTION,
        recommendation=_CC_RECOMMENDATION,
        issues=issues,
        details=details,
    )
