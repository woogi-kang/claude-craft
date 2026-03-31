"""Procedure completeness analyzer — checks content coverage per procedure type."""

import re
from collections import defaultdict

from bs4 import BeautifulSoup


# Procedure identification keywords (multilingual)
PROCEDURE_KEYWORDS: dict[str, list[str]] = {
    "potenza": ["포텐자", "potenza", "ポテンツァ"],
    "botox": ["보톡스", "botox", "ボトックス", "肉毒"],
    "filler": ["필러", "filler", "フィラー", "填充"],
    "lifting": ["리프팅", "lifting", "リフティング", "提拉"],
    "laser": ["레이저", "laser", "レーザー", "激光"],
    "peel": ["필링", "peel", "ピーリング"],
    "hair_removal": ["제모", "hair removal", "脱毛"],
    "whitening": ["미백", "whitening", "美白"],
    "acne": ["여드름", "acne", "ニキビ", "痤疮"],
    "scar": ["흉터", "scar", "傷跡"],
}

# Content section detection keywords
CONTENT_SECTIONS: dict[str, list[str]] = {
    "description": ["소개", "이란", "what is", "about", "とは"],
    "process": ["과정", "절차", "순서", "step", "process", "流れ", "procedure"],
    "price": ["가격", "비용", "price", "cost", "fee", "料金", "价格"],
    "review": ["후기", "리뷰", "review", "testimonial", "口コミ", "评价"],
    "before_after": ["전후", "비포", "before", "after", "ビフォー", "前后"],
    "faq": ["자주", "질문", "FAQ", "Q&A", "よくある"],
}

SECTION_LABELS: dict[str, str] = {
    "description": "설명",
    "process": "과정",
    "price": "가격",
    "review": "후기",
    "before_after": "전후사진",
    "faq": "FAQ",
}

PROCEDURE_LABELS: dict[str, str] = {
    "potenza": "포텐자",
    "botox": "보톡스",
    "filler": "필러",
    "lifting": "리프팅",
    "laser": "레이저",
    "peel": "필링",
    "hair_removal": "제모",
    "whitening": "미백",
    "acne": "여드름",
    "scar": "흉터",
}

# Precompiled patterns for procedure detection
_PROCEDURE_PATTERNS: dict[str, re.Pattern] = {
    key: re.compile("|".join(re.escape(kw) for kw in keywords), re.I)
    for key, keywords in PROCEDURE_KEYWORDS.items()
}

# Precompiled patterns for section detection
_SECTION_PATTERNS: dict[str, re.Pattern] = {
    key: re.compile("|".join(re.escape(kw) for kw in keywords), re.I)
    for key, keywords in CONTENT_SECTIONS.items()
}


def _extract_text(html: str) -> str:
    """Extract visible text from HTML, removing scripts and styles."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def _identify_procedures(url: str, title: str, text: str) -> list[str]:
    """Identify which procedures are referenced in the page."""
    combined = f"{url} {title} {text}"
    found = []
    for proc_key, pattern in _PROCEDURE_PATTERNS.items():
        if pattern.search(combined):
            found.append(proc_key)
    return found


def _detect_sections(text: str) -> dict[str, dict]:
    """Detect which content sections are present and estimate their content length.

    Returns:
        Dict mapping section key to {"present": bool, "partial": bool, "char_count": int}
    """
    results: dict[str, dict] = {}

    for section_key, pattern in _SECTION_PATTERNS.items():
        matches = list(pattern.finditer(text))
        if not matches:
            results[section_key] = {"present": False, "partial": False, "char_count": 0}
            continue

        # Estimate content around the keyword: take 500 chars after each match
        total_chars = 0
        for m in matches:
            start = m.start()
            end = min(start + 500, len(text))
            snippet = text[start:end]
            total_chars += len(snippet)

        if total_chars >= 300:
            results[section_key] = {"present": True, "partial": False, "char_count": total_chars}
        elif total_chars >= 100:
            results[section_key] = {"present": True, "partial": True, "char_count": total_chars}
        else:
            results[section_key] = {"present": False, "partial": False, "char_count": total_chars}

    return results


def analyze_procedure_completeness(pages: list[dict]) -> dict:
    """Analyze procedure content completeness across crawled pages.

    Args:
        pages: List of crawled page dicts with keys: url, html, (title optional)

    Returns:
        Analysis result with procedures, overall completeness, recommendations, etc.
    """
    if not pages:
        return {
            "procedures": {},
            "overall_completeness": 0,
            "best_procedure": None,
            "worst_procedure": None,
            "recommendations": [],
        }

    # Aggregate data per procedure across all pages
    proc_data: dict[str, dict] = defaultdict(lambda: {
        "pages_found": 0,
        "content_length": 0,
        "sections": {s: {"present": False, "partial": False, "char_count": 0} for s in CONTENT_SECTIONS},
    })

    for page in pages:
        url = page.get("url", "")
        html = page.get("html", "")
        title = page.get("title", "")

        text = _extract_text(html)
        if not title:
            soup = BeautifulSoup(html, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else ""

        procedures = _identify_procedures(url, title, text)
        if not procedures:
            continue

        sections = _detect_sections(text)

        for proc in procedures:
            proc_data[proc]["pages_found"] += 1
            proc_data[proc]["content_length"] += len(text)

            # Merge section data (keep the "best" detection across pages)
            for section_key, section_info in sections.items():
                existing = proc_data[proc]["sections"][section_key]
                if section_info["present"] and not existing["present"]:
                    existing["present"] = True
                    existing["partial"] = section_info["partial"]
                if section_info["char_count"] > existing["char_count"]:
                    existing["char_count"] = section_info["char_count"]
                # Upgrade from partial to full if better data found
                if existing["partial"] and section_info["present"] and not section_info["partial"]:
                    existing["partial"] = False

    if not proc_data:
        return {
            "procedures": {},
            "overall_completeness": 0,
            "best_procedure": None,
            "worst_procedure": None,
            "recommendations": [],
        }

    # Build final procedure results
    procedures: dict[str, dict] = {}
    total_sections = len(CONTENT_SECTIONS)

    for proc_key, data in proc_data.items():
        section_bools: dict[str, bool] = {}
        partial_sections: list[str] = []

        for s_key in CONTENT_SECTIONS:
            s_info = data["sections"][s_key]
            section_bools[s_key] = s_info["present"]
            if s_info["partial"]:
                partial_sections.append(s_key)

        present_count = sum(1 for v in section_bools.values() if v)
        completeness = round(present_count / total_sections * 100)

        procedures[proc_key] = {
            "name": PROCEDURE_LABELS.get(proc_key, proc_key),
            "pages_found": data["pages_found"],
            "sections": section_bools,
            "partial_sections": partial_sections,
            "completeness": completeness,
            "content_length": data["content_length"],
        }

    # Overall stats
    completeness_values = [p["completeness"] for p in procedures.values()]
    overall_completeness = round(sum(completeness_values) / len(completeness_values))

    sorted_procs = sorted(procedures.items(), key=lambda x: x[1]["completeness"])
    worst_procedure = sorted_procs[0][0] if sorted_procs else None
    best_procedure = sorted_procs[-1][0] if sorted_procs else None

    # Generate recommendations
    recommendations = _generate_recommendations(procedures, best_procedure)

    return {
        "procedures": procedures,
        "overall_completeness": overall_completeness,
        "best_procedure": best_procedure,
        "worst_procedure": worst_procedure,
        "recommendations": recommendations,
    }


def _generate_recommendations(
    procedures: dict[str, dict],
    best_procedure: str | None,
) -> list[dict]:
    """Generate actionable recommendations for improving procedure content."""
    recs: list[dict] = []

    for proc_key, proc in sorted(procedures.items(), key=lambda x: x[1]["completeness"]):
        missing = [
            SECTION_LABELS.get(s, s)
            for s, present in proc["sections"].items()
            if not present
        ]
        if not missing:
            continue

        completeness = proc["completeness"]
        if completeness < 33:
            priority = "high"
        elif completeness < 67:
            priority = "medium"
        else:
            priority = "low"

        recs.append({
            "procedure": proc_key,
            "procedure_name": proc["name"],
            "missing": missing,
            "priority": priority,
            "message": f"{proc['name']} 페이지에 {', '.join(missing)} 콘텐츠가 필요합니다",
        })

    # Benchmark recommendation
    if best_procedure and len(procedures) > 1:
        best_name = procedures[best_procedure]["name"]
        best_score = procedures[best_procedure]["completeness"]
        if best_score > 50:
            recs.append({
                "procedure": best_procedure,
                "procedure_name": best_name,
                "missing": [],
                "priority": "info",
                "message": f"{best_name} 페이지를 벤치마크로 삼아 다른 시술 페이지도 보강하세요 (완성도 {best_score}%)",
            })

    return recs
