"""Content freshness analyzer — extract last-modified dates and score freshness."""

import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .multilingual_analyzer import _PAGE_TYPE_PATTERNS


# ── Page type classification (reuse patterns from multilingual_analyzer) ─────

_BLOG_NEWS_PATTERNS = [
    re.compile(r"(blog|news|공지|소식|칼럼|column|magazine|journal|게시판|notice)", re.I),
]
_EVENT_PATTERNS = [
    re.compile(r"(event|이벤트|프로모션|promotion|할인|discount|campaign|special)", re.I),
]


def _classify_freshness_page_type(url: str, title: str) -> str:
    """Classify page type for freshness analysis."""
    combined = url + " " + title

    # Check blog/news first (not in multilingual patterns)
    for p in _BLOG_NEWS_PATTERNS:
        if p.search(combined):
            return "blog"
    for p in _EVENT_PATTERNS:
        if p.search(combined):
            return "event"

    # Reuse multilingual patterns
    for page_type, patterns in _PAGE_TYPE_PATTERNS.items():
        if page_type == "main":
            continue
        for p in patterns:
            if p.search(combined):
                return page_type

    return "other"


# ── Date extraction ──────────────────────────────────────────────────────────

# Meta tag names/properties that contain dates
_DATE_META_NAMES = [
    "article:modified_time",
    "article:published_time",
    "og:updated_time",
    "last-modified",
    "date",
    "dcterms.modified",
    "dcterms.date",
]

# Regex patterns for date extraction from text
_DATE_PATTERNS_YMD = [
    # ISO / standard: 2024-03-15, 2024.03.15, 2024/03/15
    re.compile(r"(\d{4})[-./](\d{1,2})[-./](\d{1,2})"),
    # Korean: 2024년 3월 15일
    re.compile(r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일"),
]

_DATE_PATTERNS_YM = [
    # 2024-03, 2024.03, 2024/03
    re.compile(r"(\d{4})[-./](\d{1,2})(?!\s*[-./]\d)"),
    # 2024년 3월 (without 일)
    re.compile(r"(\d{4})\s*년\s*(\d{1,2})\s*월(?!\s*\d)"),
]

_DATE_PATTERNS_ENGLISH = [
    # March 15, 2024 / Mar 15, 2024
    re.compile(
        r"(January|February|March|April|May|June|July|August|September|October|November|December"
        r"|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})",
        re.I,
    ),
]

_MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Contextual prefixes that indicate a modification/update date
_UPDATE_CONTEXT_RE = re.compile(
    r"(Updated|Modified|수정|업데이트|更新|최종\s*수정|Last\s*(?:updated|modified))",
    re.I,
)


def _parse_date_safe(year: int, month: int, day: int = 1) -> date | None:
    """Parse date components safely, returning None for invalid dates."""
    try:
        if year < 2000 or year > 2030:
            return None
        return date(year, month, min(day, 28) if month == 2 else day)
    except (ValueError, OverflowError):
        return None


def _extract_date_from_meta(html: str) -> date | None:
    """Extract date from HTML meta tags."""
    soup = BeautifulSoup(html, "html.parser")
    for meta_name in _DATE_META_NAMES:
        # Check property attribute
        tag = soup.find("meta", attrs={"property": meta_name})
        if not tag:
            tag = soup.find("meta", attrs={"name": meta_name})
        if tag:
            content = tag.get("content", "")
            if content:
                d = _parse_iso_or_date_string(content)
                if d:
                    return d

    # Check <time> tags with datetime attribute
    for time_tag in soup.find_all("time", attrs={"datetime": True}):
        d = _parse_iso_or_date_string(time_tag["datetime"])
        if d:
            return d

    return None


def _parse_iso_or_date_string(s: str) -> date | None:
    """Parse an ISO 8601 datetime or simple date string."""
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(s[:19] if "T" in s else s[:10], fmt.split("T")[0] if "T" not in s else fmt).date()
        except ValueError:
            continue

    # Try simpler parsing
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(s[:10], fmt).date()
        except ValueError:
            continue
    return None


def _extract_date_from_text(html: str) -> date | None:
    """Extract the most relevant date from page text content."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)

    if not text:
        return None

    found_dates: list[tuple[date, bool]] = []  # (date, is_update_context)

    # English month patterns
    for p in _DATE_PATTERNS_ENGLISH:
        for m in p.finditer(text):
            month_name = m.group(1).lower()
            day = int(m.group(2))
            year = int(m.group(3))
            month = _MONTH_MAP.get(month_name)
            if month:
                d = _parse_date_safe(year, month, day)
                if d:
                    # Check if preceded by update context
                    start = max(0, m.start() - 50)
                    context = text[start:m.start()]
                    is_update = bool(_UPDATE_CONTEXT_RE.search(context))
                    found_dates.append((d, is_update))

    # Y-M-D patterns
    for p in _DATE_PATTERNS_YMD:
        for m in p.finditer(text):
            year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))
            d = _parse_date_safe(year, month, day)
            if d:
                start = max(0, m.start() - 50)
                context = text[start:m.start()]
                is_update = bool(_UPDATE_CONTEXT_RE.search(context))
                found_dates.append((d, is_update))

    # Y-M patterns (less precise)
    for p in _DATE_PATTERNS_YM:
        for m in p.finditer(text):
            year, month = int(m.group(1)), int(m.group(2))
            d = _parse_date_safe(year, month, 1)
            if d:
                start = max(0, m.start() - 50)
                context = text[start:m.start()]
                is_update = bool(_UPDATE_CONTEXT_RE.search(context))
                found_dates.append((d, is_update))

    if not found_dates:
        return None

    # Prefer dates with update context, then most recent
    update_dates = [d for d, is_update in found_dates if is_update]
    if update_dates:
        return max(update_dates)

    return max(d for d, _ in found_dates)


def extract_page_date(page: dict) -> date | None:
    """Extract the most relevant date from a page.

    Priority:
    1. Meta tags (article:modified_time, etc.)
    2. Text content date patterns
    """
    html = page.get("html", "")
    if not html:
        return None

    # 1. Meta tags
    d = _extract_date_from_meta(html)
    if d:
        return d

    # 2. Text content
    return _extract_date_from_text(html)


# ── Freshness scoring ────────────────────────────────────────────────────────

def _freshness_rating(d: date | None, today: date) -> str:
    """Classify freshness: good (6mo), moderate (12mo), stale (12mo+), unknown."""
    if d is None:
        return "unknown"
    delta = (today - d).days
    if delta <= 180:
        return "good"
    if delta <= 365:
        return "moderate"
    return "stale"


def _type_freshness_label(newest: date | None, today: date) -> str:
    """Get freshness label for a page type group."""
    return _freshness_rating(newest, today)


def _calculate_freshness_score(
    pages_with_date: int,
    total_pages: int,
    rating_counts: dict[str, int],
) -> int:
    """Calculate overall freshness score 0-100."""
    if total_pages == 0:
        return 0

    # Weight: good=100, moderate=60, stale=20, unknown=30
    weights = {"good": 100, "moderate": 60, "stale": 20, "unknown": 30}
    weighted_sum = sum(rating_counts.get(r, 0) * weights[r] for r in weights)
    return round(weighted_sum / total_pages)


def _extract_title(html: str) -> str:
    """Extract page title from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    return title.get_text(strip=True) if title else ""


# ── Recommendations ──────────────────────────────────────────────────────────

_TYPE_LABELS = {
    "blog": "블로그/뉴스",
    "procedure": "시술 소개",
    "doctor": "의사 소개",
    "price": "가격/비용",
    "booking": "예약/상담",
    "review": "후기/리뷰",
    "event": "이벤트/프로모션",
    "main": "메인 페이지",
    "other": "기타",
}


def _generate_recommendations(
    by_type: dict[str, dict],
    rating_counts: dict[str, int],
    total_pages: int,
    today: date,
) -> list[dict]:
    """Generate actionable freshness recommendations."""
    recs: list[dict] = []

    # Stale procedure/doctor pages are high priority
    for ptype in ["procedure", "doctor", "price"]:
        info = by_type.get(ptype)
        if info and info["freshness"] == "stale" and info["newest"]:
            newest = date.fromisoformat(info["newest"])
            months = (today - newest).days // 30
            label = _TYPE_LABELS.get(ptype, ptype)
            recs.append({
                "priority": "high",
                "message": f"{label} 페이지가 {months}개월 이상 업데이트되지 않았습니다. 최신 정보로 갱신하세요.",
            })

    # Blog/news freshness
    blog_info = by_type.get("blog")
    if blog_info and blog_info["count"] > 0 and blog_info["freshness"] in ("stale", "moderate"):
        recs.append({
            "priority": "medium",
            "message": "블로그/뉴스 콘텐츠가 오래되었습니다. 정기적인 콘텐츠 발행으로 검색 엔진 신뢰도를 높이세요.",
        })

    # Event pages that are stale
    event_info = by_type.get("event")
    if event_info and event_info["freshness"] == "stale":
        recs.append({
            "priority": "high",
            "message": "만료된 이벤트/프로모션 페이지가 있습니다. 종료된 이벤트를 제거하거나 업데이트하세요.",
        })

    # High unknown ratio
    unknown_ratio = rating_counts.get("unknown", 0) / total_pages if total_pages > 0 else 0
    if unknown_ratio > 0.5:
        recs.append({
            "priority": "medium",
            "message": "페이지의 50% 이상에서 날짜를 확인할 수 없습니다. 콘텐츠에 게시일/수정일을 명시하면 SEO에 도움됩니다.",
        })

    # Overall stale content
    stale_ratio = rating_counts.get("stale", 0) / total_pages if total_pages > 0 else 0
    if stale_ratio > 0.4:
        recs.append({
            "priority": "high",
            "message": "전체 페이지의 40% 이상이 1년 넘게 업데이트되지 않았습니다. 콘텐츠 갱신 계획을 수립하세요.",
        })

    return recs


# ── Main analysis function ───────────────────────────────────────────────────

def analyze_content_freshness(pages: list[dict], today: date | None = None) -> dict:
    """Analyze content freshness from crawled pages.

    Args:
        pages: List of crawled page dicts with keys: url, html, status_code
        today: Override for current date (for testing)

    Returns:
        Analysis result with freshness scores, type breakdown, ratings, recommendations.
    """
    if today is None:
        today = date.today()

    if not pages:
        return {
            "overall_freshness_score": 0,
            "total_pages": 0,
            "pages_with_date": 0,
            "recent_6months": 0,
            "by_type": {},
            "freshness_rating": {"good": 0, "moderate": 0, "stale": 0, "unknown": 0},
            "recommendations": [],
        }

    # Process each page
    type_pages: dict[str, list[dict]] = defaultdict(list)

    for page in pages:
        url = page.get("url", "")
        html = page.get("html", "")
        title = page.get("title", "") or _extract_title(html)

        page_type = _classify_freshness_page_type(url, title)
        page_date = extract_page_date(page)

        type_pages[page_type].append({
            "url": url,
            "title": title,
            "date": page_date,
            "rating": _freshness_rating(page_date, today),
        })

    # Aggregate by type
    by_type: dict[str, dict] = {}
    total_pages = len(pages)
    pages_with_date = 0
    recent_6months = 0
    rating_counts: dict[str, int] = {"good": 0, "moderate": 0, "stale": 0, "unknown": 0}

    for ptype, plist in type_pages.items():
        dates = [p["date"] for p in plist if p["date"] is not None]
        newest = max(dates) if dates else None
        by_type[ptype] = {
            "count": len(plist),
            "newest": newest.isoformat() if newest else None,
            "freshness": _type_freshness_label(newest, today),
            "pages_with_date": len(dates),
        }
        pages_with_date += len(dates)
        for p in plist:
            rating = p["rating"]
            rating_counts[rating] += 1
            if rating == "good":
                recent_6months += 1

    overall_score = _calculate_freshness_score(pages_with_date, total_pages, rating_counts)
    recommendations = _generate_recommendations(by_type, rating_counts, total_pages, today)

    return {
        "overall_freshness_score": overall_score,
        "total_pages": total_pages,
        "pages_with_date": pages_with_date,
        "recent_6months": recent_6months,
        "by_type": by_type,
        "freshness_rating": rating_counts,
        "recommendations": recommendations,
    }
