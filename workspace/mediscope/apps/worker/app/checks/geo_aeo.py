"""GEO/AEO checks: AI search engine mention detection."""

import logging
import re

import httpx

from ..checks.base import CheckResult, Grade
from ..config import settings

logger = logging.getLogger("mediscope.checks.geo_aeo")


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
            issues=["병원명 정보가 없어 AI 검색 체크를 수행할 수 없습니다"],
            details={"skipped": True},
        )

    queries = _build_queries(hospital_name, specialty, region)
    if not queries:
        return CheckResult(
            name="ai_search_mention",
            score=0.0,
            grade=Grade.FAIL,
            issues=["검색 쿼리를 생성할 수 없습니다"],
        )

    mention_scores: list[float] = []
    sources_checked: list[str] = []

    # Try Perplexity API
    for query in queries[:2]:  # Limit to 2 queries to save API calls
        response_text = await _query_perplexity(client, query)
        if response_text is not None:
            score = _check_mention(response_text, hospital_name, url)
            mention_scores.append(score)
            sources_checked.append(f"perplexity:{query}")

    if not mention_scores:
        # No API available — return skip result
        return CheckResult(
            name="ai_search_mention",
            score=0.0,
            grade=Grade.FAIL,
            issues=["AI 검색 API를 사용할 수 없습니다 (PERPLEXITY_API_KEY 필요)"],
            details={"skipped": True, "reason": "no_api_key"},
        )

    avg_score = sum(mention_scores) / len(mention_scores)

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
        issues=issues,
        details={
            "queries_used": queries[:2],
            "sources_checked": sources_checked,
            "mention_scores": mention_scores,
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
        issues=issues,
        details=details,
    )
