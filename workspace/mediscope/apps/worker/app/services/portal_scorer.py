"""Portal-specific SEO scorer: remap 21 checks into per-portal scores."""

PORTAL_CHECK_MAP: dict[str, dict] = {
    "google": {
        "label": "Google",
        "checks": [
            "sitemap", "robots_txt", "structured_data", "performance_score",
            "lcp", "inp", "cls", "https", "canonical", "meta_tags", "images_alt",
        ],
        "weights": {
            "sitemap": 0.12, "robots_txt": 0.10, "structured_data": 0.15,
            "performance_score": 0.12, "lcp": 0.08, "inp": 0.05, "cls": 0.05,
            "https": 0.10, "canonical": 0.08, "meta_tags": 0.10, "images_alt": 0.05,
        },
    },
    "naver": {
        "label": "Naver",
        "checks": ["meta_tags", "headings", "sitemap", "robots_txt", "links", "images_alt"],
        "weights": {
            "meta_tags": 0.25, "headings": 0.15, "sitemap": 0.20,
            "robots_txt": 0.15, "links": 0.15, "images_alt": 0.10,
        },
    },
    "baidu": {
        "label": "Baidu",
        "checks": ["multilingual_pages", "https", "performance_score", "meta_tags", "sitemap"],
        "weights": {
            "multilingual_pages": 0.35, "https": 0.15, "performance_score": 0.20,
            "meta_tags": 0.15, "sitemap": 0.15,
        },
    },
    "yahoo_jp": {
        "label": "Yahoo JP",
        "checks": ["multilingual_pages", "hreflang", "meta_tags", "performance_score", "https"],
        "weights": {
            "multilingual_pages": 0.30, "hreflang": 0.25, "meta_tags": 0.20,
            "performance_score": 0.15, "https": 0.10,
        },
    },
    "ai_search": {
        "label": "AI 검색",
        "checks": [
            "ai_search_mention", "content_clarity", "structured_data",
            "faq_content", "eeat_signals",
        ],
        "weights": {
            "ai_search_mention": 0.30, "content_clarity": 0.20,
            "structured_data": 0.20, "faq_content": 0.15, "eeat_signals": 0.15,
        },
    },
}

SKIP_FAIL_TYPES = {"system_limit", "api_error", "not_applicable"}


def _calculate_grade(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    if score >= 20:
        return "D"
    return "F"


def _top_issues(portal_checks: list[str], category_scores: dict, limit: int = 2) -> list[str]:
    """Return top N issues for a portal sorted by impact (weight * deficit)."""
    issues: list[tuple[float, str]] = []
    for check_name in portal_checks:
        item = category_scores.get(check_name)
        if not item:
            continue
        if item.get("fail_type") in SKIP_FAIL_TYPES:
            continue
        score = item.get("score")
        if score is None or score >= 80:
            continue
        display = item.get("display_name") or check_name
        recommendation = item.get("recommendation", "")
        weight = item.get("weight", 0)
        impact = weight * (100 - score)
        text = f"{display}: {recommendation}" if recommendation else display
        issues.append((impact, text))
    issues.sort(key=lambda x: -x[0])
    return [text for _, text in issues[:limit]]


def calculate_portal_scores(category_scores: dict) -> dict:
    """Calculate per-portal scores from category_scores.

    Returns dict keyed by portal name, each with:
        - score: 0-100
        - grade: A/B/C/D/F
        - label: display name
        - issues: top issue strings
        - checks_measured: number of checks with valid scores
        - checks_total: total checks for this portal
    """
    result: dict[str, dict] = {}

    for portal_key, portal_def in PORTAL_CHECK_MAP.items():
        checks = portal_def["checks"]
        weights = portal_def["weights"]

        weighted_sum = 0.0
        weight_sum = 0.0
        measured = 0

        for check_name in checks:
            item = category_scores.get(check_name)
            if not item:
                continue
            if item.get("fail_type") in SKIP_FAIL_TYPES:
                continue
            score = item.get("score")
            if score is None:
                continue
            measured += 1
            w = weights.get(check_name, 0)
            weighted_sum += (score / 100) * w
            weight_sum += w

        if weight_sum > 0:
            portal_score = round((weighted_sum / weight_sum) * 100)
        else:
            portal_score = 0

        portal_score = max(0, min(100, portal_score))

        result[portal_key] = {
            "score": portal_score,
            "grade": _calculate_grade(portal_score),
            "label": portal_def["label"],
            "issues": _top_issues(checks, category_scores),
            "checks_measured": measured,
            "checks_total": len(checks),
        }

    return result
