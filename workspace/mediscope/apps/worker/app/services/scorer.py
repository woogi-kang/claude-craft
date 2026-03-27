"""Score calculator: weighted average → 0-100 score + grade."""

from ..checks.base import CheckResult

# 23 items with weights (must sum to ~1.0)
WEIGHTS: dict[str, float] = {
    # Technical SEO (0.50)
    "robots_txt": 0.05,
    "sitemap": 0.05,
    "meta_tags": 0.10,
    "headings": 0.05,
    "images_alt": 0.05,
    "links": 0.05,
    "https": 0.03,
    "canonical": 0.03,
    "url_structure": 0.04,
    "errors_404": 0.05,
    # Performance (0.20)
    "lcp": 0.05,
    "inp": 0.03,
    "cls": 0.03,
    "performance_score": 0.04,
    "mobile": 0.05,
    # GEO/AEO (0.25)
    "structured_data": 0.08,
    "faq_content": 0.03,
    "ai_search_mention": 0.05,
    "eeat_signals": 0.05,
    "content_clarity": 0.04,
    # Multilingual (0.05) — split into 3 sub-checks
    "multilingual_pages": 0.025,
    "hreflang": 0.015,
    "overseas_channels": 0.01,
}

# Total weight: 1.00


def calculate_grade(score: float) -> str:
    if score >= 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    if score >= 20:
        return "D"
    return "F"


def calculate_score(results: list[CheckResult]) -> dict:
    """Calculate weighted score from check results.

    Returns dict with:
        - total_score: 0-100
        - grade: A/B/C/D/F
        - category_scores: per-item breakdown
    """
    result_map = {r.name: r for r in results}

    weighted_sum = 0.0
    weight_sum = 0.0
    category_scores: dict[str, dict] = {}

    for name, weight in WEIGHTS.items():
        check = result_map.get(name)
        if check:
            item_score = check.score * 100  # Convert 0.0-1.0 to 0-100
            weighted_sum += check.score * weight
            weight_sum += weight
            category_scores[name] = {
                "score": round(item_score, 1),
                "weight": weight,
                "grade": check.grade.value,
                "issues": check.issues,
                "details": check.details,
            }
        else:
            category_scores[name] = {
                "score": None,
                "weight": weight,
                "grade": "skip",
                "issues": ["측정되지 않음"],
                "details": {},
            }

    # Normalize to 0-100 scale based on available weights
    if weight_sum > 0:
        total_score = round((weighted_sum / weight_sum) * 100, 1)
    else:
        total_score = 0.0

    # Clamp to 0-100
    total_score = max(0.0, min(100.0, total_score))

    return {
        "total_score": int(round(total_score)),
        "grade": calculate_grade(total_score),
        "items_checked": len([r for r in results if r.name in WEIGHTS]),
        "items_total": len(WEIGHTS),
        "category_scores": category_scores,
    }
