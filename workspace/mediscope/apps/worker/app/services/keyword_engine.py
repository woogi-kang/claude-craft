"""Keyword extraction and generation engine for competitor analysis.

Extracts procedure names from crawled pages and generates search keywords
with multilingual support and priority ranking.
"""

import re

from .procedure_completeness import PROCEDURE_KEYWORDS, PROCEDURE_LABELS, _extract_text

# Procedure popularity weights (estimated search volume)
PROCEDURE_POPULARITY: dict[str, int] = {
    "botox": 10,
    "filler": 9,
    "lifting": 8,
    "laser": 7,
    "potenza": 7,
    "hair_removal": 6,
    "whitening": 5,
    "acne": 5,
    "peel": 4,
    "scar": 3,
}

# Region name translations for multilingual keyword generation
REGION_TRANSLATIONS: dict[str, dict[str, str]] = {
    "홍대": {"en": "hongdae", "ja": "弘大", "zh": "弘大"},
    "홍대/마포": {"en": "hongdae", "ja": "弘大", "zh": "弘大"},
    "강남": {"en": "gangnam", "ja": "江南", "zh": "江南"},
    "강남/서초": {"en": "gangnam", "ja": "江南", "zh": "江南"},
    "명동": {"en": "myeongdong", "ja": "明洞", "zh": "明洞"},
    "명동/을지": {"en": "myeongdong", "ja": "明洞", "zh": "明洞"},
    "신촌": {"en": "sinchon", "ja": "新村", "zh": "新村"},
    "신촌/연남": {"en": "sinchon", "ja": "新村", "zh": "新村"},
    "압구정": {"en": "apgujeong", "ja": "狎鷗亭", "zh": "狎鸥亭"},
    "압구정/청담": {"en": "apgujeong", "ja": "狎鷗亭", "zh": "狎鸥亭"},
    "잠실": {"en": "jamsil", "ja": "蚕室", "zh": "蚕室"},
    "잠실/송파": {"en": "jamsil", "ja": "蚕室", "zh": "蚕室"},
    "건대": {"en": "kondae", "ja": "建大", "zh": "建大"},
    "건대/성수": {"en": "kondae", "ja": "建大", "zh": "建大"},
    "영등포": {"en": "yeongdeungpo", "ja": "永登浦", "zh": "永登浦"},
    "영등포/여의도": {"en": "yeongdeungpo", "ja": "永登浦", "zh": "永登浦"},
    "부산 서면": {"en": "seomyeon busan", "ja": "西面", "zh": "西面"},
    "부산 해운대": {"en": "haeundae busan", "ja": "海雲台", "zh": "海云台"},
    "대구 수성": {"en": "suseong daegu", "ja": "寿城", "zh": "寿城"},
    "제주": {"en": "jeju", "ja": "済州", "zh": "济州"},
}

# Procedure name translations for multilingual keywords
PROCEDURE_TRANSLATIONS: dict[str, dict[str, str]] = {
    "botox": {"en": "botox", "ja": "ボトックス", "zh": "肉毒"},
    "filler": {"en": "filler", "ja": "フィラー", "zh": "填充"},
    "lifting": {"en": "lifting", "ja": "リフティング", "zh": "提拉"},
    "laser": {"en": "laser", "ja": "レーザー", "zh": "激光"},
    "potenza": {"en": "potenza", "ja": "ポテンツァ", "zh": "热玛吉"},
    "hair_removal": {"en": "hair removal", "ja": "脱毛", "zh": "脱毛"},
    "whitening": {"en": "whitening", "ja": "美白", "zh": "美白"},
    "acne": {"en": "acne treatment", "ja": "ニキビ治療", "zh": "痤疮治疗"},
    "peel": {"en": "chemical peel", "ja": "ピーリング", "zh": "果酸换肤"},
    "scar": {"en": "scar treatment", "ja": "傷跡治療", "zh": "疤痕治疗"},
}

# Portal mapping by language
PORTAL_BY_LANGUAGE: dict[str, list[str]] = {
    "ko": ["naver", "google"],
    "en": ["google"],
    "ja": ["google", "yahoo_jp"],
    "zh": ["google", "baidu"],
}

# Precompiled patterns (reuse from procedure_completeness)
_PROCEDURE_PATTERNS: dict[str, re.Pattern] = {
    key: re.compile("|".join(re.escape(kw) for kw in keywords), re.I)
    for key, keywords in PROCEDURE_KEYWORDS.items()
}


def _extract_procedures_from_pages(pages: list[dict]) -> list[str]:
    """Extract unique procedure keys found across all crawled pages."""
    found: set[str] = set()
    for page in pages:
        url = page.get("url", "")
        html = page.get("html", "")
        title = page.get("title", "")
        text = _extract_text(html) if html else ""
        combined = f"{url} {title} {text}"
        for proc_key, pattern in _PROCEDURE_PATTERNS.items():
            if pattern.search(combined):
                found.add(proc_key)
    return sorted(found)


def _short_region(region_name: str) -> str:
    """Get the short display form of a region (before '/')."""
    return region_name.split("/")[0]


def _generate_ko_keywords(region: str, procedure: str, proc_label: str) -> list[dict]:
    """Generate Korean keyword combinations for a region+procedure pair."""
    base_priority = PROCEDURE_POPULARITY.get(procedure, 1)
    portals = PORTAL_BY_LANGUAGE["ko"]
    short = _short_region(region)

    return [
        {
            "keyword": f"{short} {proc_label}",
            "language": "ko",
            "procedure": procedure,
            "priority": base_priority,
            "portals": portals,
        },
        {
            "keyword": f"{proc_label} {short}",
            "language": "ko",
            "procedure": procedure,
            "priority": base_priority - 1,
            "portals": portals,
        },
        {
            "keyword": f"{short} {proc_label} 가격",
            "language": "ko",
            "procedure": procedure,
            "priority": base_priority - 1,
            "portals": portals,
        },
        {
            "keyword": f"{short} {proc_label} 잘하는곳",
            "language": "ko",
            "procedure": procedure,
            "priority": base_priority - 2,
            "portals": portals,
        },
    ]


def _generate_multilingual_keywords(
    region: str, procedure: str,
) -> list[dict]:
    """Generate EN/JA/ZH keywords for a region+procedure pair."""
    keywords: list[dict] = []
    base_priority = PROCEDURE_POPULARITY.get(procedure, 1)
    region_trans = REGION_TRANSLATIONS.get(region) or REGION_TRANSLATIONS.get(
        _short_region(region)
    )
    proc_trans = PROCEDURE_TRANSLATIONS.get(procedure)

    if not region_trans or not proc_trans:
        return keywords

    for lang in ("en", "ja", "zh"):
        r = region_trans.get(lang)
        p = proc_trans.get(lang)
        if not r or not p:
            continue
        portals = PORTAL_BY_LANGUAGE.get(lang, ["google"])
        # Reduce priority for non-Korean keywords
        priority = max(1, base_priority - 3)
        keywords.append({
            "keyword": f"{r} {p}",
            "language": lang,
            "procedure": procedure,
            "priority": priority,
            "portals": portals,
        })

    return keywords


def _generate_base_keywords(region: str) -> list[dict]:
    """Generate base region keywords (no specific procedure)."""
    short = _short_region(region)
    portals = PORTAL_BY_LANGUAGE["ko"]
    return [
        {
            "keyword": f"{short} 피부과",
            "language": "ko",
            "procedure": None,
            "priority": 8,
            "portals": portals,
        },
        {
            "keyword": f"{short} 피부과 추천",
            "language": "ko",
            "procedure": None,
            "priority": 7,
            "portals": portals,
        },
    ]


def extract_and_generate_keywords(
    pages: list[dict],
    region_name: str,
    hospital_name: str | None = None,
) -> dict:
    """Extract procedure names from crawled pages and generate search keywords.

    Steps:
        1. Extract procedures using PROCEDURE_KEYWORDS patterns
        2. Generate Korean keyword combinations (region+procedure)
        3. Generate multilingual keywords (EN/JA/ZH)
        4. Sort by priority and select top 10

    Args:
        pages: List of crawled page dicts with keys: url, html, (title optional)
        region_name: Region name (e.g., "홍대", "강남/서초")
        hospital_name: Optional hospital name for branded keywords

    Returns:
        Dict with procedures_found, keywords (top 10), total_generated count.
    """
    if not pages or not region_name:
        return {
            "region": region_name or "",
            "procedures_found": [],
            "keywords": [],
            "total_generated": 0,
            "selected": 0,
        }

    # Step 1: Extract procedures
    procedures_found = _extract_procedures_from_pages(pages)

    # Step 2-3: Generate all keywords
    all_keywords: list[dict] = []

    # Base region keywords
    all_keywords.extend(_generate_base_keywords(region_name))

    for proc in procedures_found:
        proc_label = PROCEDURE_LABELS.get(proc, proc)

        # Korean keyword combinations
        all_keywords.extend(_generate_ko_keywords(region_name, proc, proc_label))

        # Multilingual keywords
        all_keywords.extend(_generate_multilingual_keywords(region_name, proc))

    # Step 4: Deduplicate by keyword text
    seen: set[str] = set()
    unique_keywords: list[dict] = []
    for kw in all_keywords:
        if kw["keyword"] not in seen:
            seen.add(kw["keyword"])
            unique_keywords.append(kw)

    total_generated = len(unique_keywords)

    # Sort by priority (descending), then by language (ko first)
    lang_order = {"ko": 0, "en": 1, "ja": 2, "zh": 3}
    unique_keywords.sort(
        key=lambda k: (-k["priority"], lang_order.get(k["language"], 9))
    )

    # Select top 10
    selected = unique_keywords[:10]

    return {
        "region": region_name,
        "procedures_found": procedures_found,
        "keywords": selected,
        "total_generated": total_generated,
        "selected": len(selected),
    }
