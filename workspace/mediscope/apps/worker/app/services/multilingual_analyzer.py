"""Multilingual readiness analyzer — deep analysis of crawled pages for language coverage."""

import re
import unicodedata
from collections import defaultdict
from urllib.parse import urlparse

from bs4 import BeautifulSoup


# Language detection via URL path patterns
_LANG_PATH_RE = re.compile(
    r"/(en|ja|jp|zh|zh-cn|zh-tw|cn|vi|th|ru|ar|ko)(/|$)", re.I,
)

# Character range helpers
_HANGUL_RE = re.compile(r"[\uAC00-\uD7A3\u3131-\u3163\u1100-\u11FF]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_HIRAGANA_RE = re.compile(r"[\u3040-\u309F]")
_KATAKANA_RE = re.compile(r"[\u30A0-\u30FF]")
_CJK_RE = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF]")

# Page type classification patterns
_PAGE_TYPE_PATTERNS: dict[str, list[re.Pattern]] = {
    "main": [re.compile(r"^https?://[^/]+/?$")],
    "procedure": [
        re.compile(r"(시술|치료|treatment|procedure|surgery|laser|filler|botox|리프팅|필러|보톡스)", re.I),
    ],
    "doctor": [
        re.compile(r"(의사|doctor|의료진|원장|staff|team|physician|dr\.)", re.I),
    ],
    "price": [
        re.compile(r"(가격|price|비용|cost|fee|pricing|요금)", re.I),
    ],
    "booking": [
        re.compile(r"(예약|book|상담|contact|consult|appointment|문의|reserve)", re.I),
    ],
    "review": [
        re.compile(r"(후기|review|before.?after|사례|testimonial|결과)", re.I),
    ],
}

# Language code normalization
_LANG_NORM: dict[str, str] = {
    "jp": "ja",
    "cn": "zh",
    "zh-cn": "zh",
    "zh-tw": "zh",
    "zh-hans": "zh",
    "zh-hant": "zh",
}

_LANG_LABELS: dict[str, str] = {
    "ko": "한국어",
    "en": "English",
    "ja": "日本語",
    "zh": "中文",
}

_LANG_FLAGS: dict[str, str] = {
    "ko": "🇰🇷",
    "en": "🇺🇸",
    "ja": "🇯🇵",
    "zh": "🇨🇳",
}

TARGET_LANGUAGES = ["ko", "en", "ja", "zh"]


def _normalize_lang(code: str) -> str:
    """Normalize language code to 2-letter form."""
    code = code.lower().strip().split("-")[0] if "-" not in code[:3] else code.lower().strip()
    return _LANG_NORM.get(code, code.split("-")[0])


def _detect_lang_from_url(url: str) -> str | None:
    """Detect language from URL path pattern."""
    m = _LANG_PATH_RE.search(urlparse(url).path)
    if m:
        return _normalize_lang(m.group(1))
    # Subdomain detection: en.example.com, ja.example.com
    host = urlparse(url).hostname or ""
    parts = host.split(".")
    if len(parts) >= 3 and parts[0] in ("en", "ja", "jp", "zh", "cn", "ko"):
        return _normalize_lang(parts[0])
    return None


def _detect_lang_from_content(html: str) -> str:
    """Detect primary language from HTML content using character frequency analysis."""
    soup = BeautifulSoup(html, "html.parser")
    # Remove script/style
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)

    if not text:
        return "ko"  # default

    hangul = len(_HANGUL_RE.findall(text))
    latin = len(_LATIN_RE.findall(text))
    hiragana = len(_HIRAGANA_RE.findall(text))
    katakana = len(_KATAKANA_RE.findall(text))
    cjk = len(_CJK_RE.findall(text))

    japanese = hiragana + katakana
    total = hangul + latin + japanese + cjk
    if total == 0:
        return "ko"

    # Japanese: hiragana/katakana are definitive
    if japanese > 0 and japanese / total > 0.05:
        return "ja"
    # Korean
    if hangul > 0 and hangul / total > 0.2:
        return "ko"
    # Chinese: CJK without Japanese kana and without Korean
    if cjk > 0 and hangul == 0 and japanese == 0 and cjk / total > 0.2:
        return "zh"
    # English / Latin-dominant
    if latin > 0 and latin / total > 0.5:
        return "en"

    return "ko"


def _detect_lang_from_html_tag(html: str) -> str | None:
    """Detect language from <html lang='...'> attribute."""
    soup = BeautifulSoup(html, "html.parser")
    html_tag = soup.find("html")
    if html_tag:
        lang = (html_tag.get("lang") or "").strip()
        if lang:
            return _normalize_lang(lang)
    return None


def _classify_page_type(url: str, html: str) -> str:
    """Classify page into a type based on URL and content keywords."""
    # Check main page first (URL-only check)
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    # Main page: root, or language root like /en, /ja
    if not path or _LANG_PATH_RE.fullmatch(path + "/"):
        return "main"

    combined = url + " " + _extract_title(html)

    for page_type, patterns in _PAGE_TYPE_PATTERNS.items():
        if page_type == "main":
            continue
        for pattern in patterns:
            if pattern.search(combined):
                return page_type

    return "other"


def _extract_title(html: str) -> str:
    """Extract page title from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title")
    return title.get_text(strip=True) if title else ""


def _extract_hreflang_tags(html: str) -> list[dict]:
    """Extract hreflang link tags from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    tags = soup.find_all("link", attrs={"rel": "alternate", "hreflang": True})
    results = []
    for tag in tags:
        hreflang = tag.get("hreflang", "")
        href = tag.get("href", "")
        if hreflang and href:
            results.append({
                "lang": _normalize_lang(hreflang),
                "hreflang": hreflang,
                "href": href,
            })
    return results


def analyze_multilingual_readiness(pages: list[dict]) -> dict:
    """Analyze multilingual readiness from crawled pages.

    Args:
        pages: List of crawled page dicts with keys: url, html, status_code, (title optional)

    Returns:
        Analysis result with languages, page_types, matrix, readiness_scores, etc.
    """
    if not pages:
        return {
            "languages": {},
            "page_types": {},
            "matrix": {},
            "readiness_scores": {lang: 0 for lang in TARGET_LANGUAGES},
            "overall_score": 0,
            "hreflang_tags": [],
            "recommendations": [],
        }

    # Group pages by detected language
    lang_pages: dict[str, list[dict]] = defaultdict(list)
    page_type_lang: dict[str, set[str]] = defaultdict(set)  # page_type -> set of langs
    all_hreflang: list[dict] = []
    page_details: list[dict] = []

    for page in pages:
        url = page.get("url", "")
        html = page.get("html", "")

        # Detect language (priority: URL > html tag > content analysis)
        lang = _detect_lang_from_url(url)
        if not lang:
            lang = _detect_lang_from_html_tag(html)
        if not lang:
            lang = _detect_lang_from_content(html)

        lang = _normalize_lang(lang)
        page_type = _classify_page_type(url, html)
        title = page.get("title", "") or _extract_title(html)

        lang_pages[lang].append({"url": url, "title": title, "page_type": page_type})
        page_type_lang[page_type].add(lang)

        # Collect hreflang from main page
        hreflang_tags = _extract_hreflang_tags(html)
        if hreflang_tags:
            all_hreflang.extend(hreflang_tags)

        page_details.append({
            "url": url,
            "title": title,
            "lang": lang,
            "page_type": page_type,
        })

    # Deduplicate hreflang
    seen_hreflang: set[str] = set()
    unique_hreflang: list[dict] = []
    for tag in all_hreflang:
        key = f"{tag['hreflang']}:{tag['href']}"
        if key not in seen_hreflang:
            seen_hreflang.add(key)
            unique_hreflang.append(tag)

    # Build language info
    languages: dict[str, dict] = {}
    for lang in TARGET_LANGUAGES:
        pages_for_lang = lang_pages.get(lang, [])
        languages[lang] = {
            "code": lang,
            "label": _LANG_LABELS.get(lang, lang),
            "flag": _LANG_FLAGS.get(lang, ""),
            "page_count": len(pages_for_lang),
            "pages": pages_for_lang,
        }

    # Build page type info
    all_page_types = sorted(set(
        pt for pt in page_type_lang.keys() if pt != "other"
    ))
    if not all_page_types:
        all_page_types = ["main"]

    page_types: dict[str, dict] = {}
    for pt in all_page_types:
        page_types[pt] = {
            "name": pt,
            "languages": sorted(page_type_lang.get(pt, set())),
        }

    # Build matrix: page_type × language → bool
    matrix: dict[str, dict[str, bool]] = {}
    for pt in all_page_types:
        matrix[pt] = {}
        for lang in TARGET_LANGUAGES:
            matrix[pt][lang] = lang in page_type_lang.get(pt, set())

    # Calculate readiness scores per language
    readiness_scores: dict[str, int] = {}
    for lang in TARGET_LANGUAGES:
        if not all_page_types:
            readiness_scores[lang] = 0
            continue
        covered = sum(1 for pt in all_page_types if matrix.get(pt, {}).get(lang, False))
        readiness_scores[lang] = round(covered / len(all_page_types) * 100)

    # Overall score = average of non-Korean languages
    non_ko_scores = [readiness_scores[lang] for lang in TARGET_LANGUAGES if lang != "ko"]
    overall_score = round(sum(non_ko_scores) / len(non_ko_scores)) if non_ko_scores else 0

    # Generate recommendations
    recommendations = _generate_recommendations(
        languages, matrix, all_page_types, readiness_scores, unique_hreflang,
    )

    return {
        "languages": languages,
        "page_types": page_types,
        "matrix": matrix,
        "readiness_scores": readiness_scores,
        "overall_score": overall_score,
        "hreflang_tags": unique_hreflang,
        "recommendations": recommendations,
        "page_details": page_details,
    }


def _generate_recommendations(
    languages: dict,
    matrix: dict,
    page_types: list[str],
    scores: dict,
    hreflang_tags: list[dict],
) -> list[dict]:
    """Generate actionable recommendations."""
    recs: list[dict] = []

    # Missing language pages
    for lang in ["en", "ja", "zh"]:
        if scores.get(lang, 0) == 0:
            label = _LANG_LABELS.get(lang, lang)
            flag = _LANG_FLAGS.get(lang, "")
            traffic_estimates = {"en": 35, "ja": 23, "zh": 18}
            est = traffic_estimates.get(lang, 15)
            recs.append({
                "priority": "high",
                "category": "missing_language",
                "lang": lang,
                "message": f"{flag} {label} 페이지가 없습니다. 추가 시 예상 해외 트래픽: +{est}%",
            })

    # Partial language coverage
    for lang in ["en", "ja", "zh"]:
        score = scores.get(lang, 0)
        if 0 < score < 100:
            label = _LANG_LABELS.get(lang, lang)
            flag = _LANG_FLAGS.get(lang, "")
            missing_types = [
                pt for pt in page_types
                if not matrix.get(pt, {}).get(lang, False)
            ]
            if missing_types:
                type_names = ", ".join(missing_types)
                recs.append({
                    "priority": "medium",
                    "category": "partial_coverage",
                    "lang": lang,
                    "message": f"{flag} {label}: {type_names} 페이지 번역이 필요합니다",
                })

    # Missing hreflang tags
    if not hreflang_tags:
        detected_langs = [lang for lang in TARGET_LANGUAGES if languages.get(lang, {}).get("page_count", 0) > 0]
        if len(detected_langs) > 1:
            recs.append({
                "priority": "medium",
                "category": "missing_hreflang",
                "message": "다국어 페이지가 있지만 hreflang 태그가 없습니다. 검색엔진에 언어별 페이지를 알려주세요.",
            })

    # Priority page types to translate
    priority_types = ["procedure", "booking", "price"]
    for pt in priority_types:
        if pt in page_types:
            for lang in ["en", "ja", "zh"]:
                if not matrix.get(pt, {}).get(lang, False) and scores.get(lang, 0) > 0:
                    label = _LANG_LABELS.get(lang, lang)
                    recs.append({
                        "priority": "high",
                        "category": "priority_translation",
                        "lang": lang,
                        "message": f"{pt} 페이지의 {label} 번역이 우선적으로 필요합니다 (전환율에 직접 영향)",
                    })

    return recs
