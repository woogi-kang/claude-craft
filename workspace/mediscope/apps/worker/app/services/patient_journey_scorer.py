"""Patient journey funnel scorer: maps 24 check items to 4 patient journey stages."""

from .scorer import calculate_grade

# Check name → journey stage mapping with per-stage weights (must sum to 1.0 per stage)
JOURNEY_STAGES: dict[str, dict] = {
    "discovery": {
        "display_name": "발견",
        "icon": "search",
        "description": "검색 엔진에서 병원을 찾을 수 있는가?",
        "checks": {
            "sitemap": 0.15,
            "robots_txt": 0.15,
            "meta_tags": 0.20,
            "headings": 0.10,
            "url_structure": 0.10,
            "international_search": 0.15,
            "ai_search_mention": 0.15,
        },
    },
    "trust": {
        "display_name": "신뢰",
        "icon": "shield",
        "description": "병원을 신뢰할 수 있는가?",
        "checks": {
            "eeat_signals": 0.25,
            "https": 0.15,
            "structured_data": 0.20,
            "content_clarity": 0.20,
            "errors_404": 0.10,
            "canonical": 0.10,
        },
    },
    "comparison": {
        "display_name": "비교",
        "icon": "scale",
        "description": "경쟁 병원과 비교할 정보가 충분한가?",
        "checks": {
            "faq_content": 0.20,
            "images_alt": 0.15,
            "links": 0.15,
            "performance_score": 0.15,
            "multilingual_pages": 0.20,
            "overseas_channels": 0.15,
        },
    },
    "booking": {
        "display_name": "예약",
        "icon": "calendar",
        "description": "예약/상담으로 전환되는가?",
        "checks": {
            "lcp": 0.20,
            "inp": 0.20,
            "cls": 0.15,
            "hreflang": 0.25,
            "performance_score": 0.20,
        },
    },
}

STAGE_RECOMMENDATIONS: dict[str, dict[str, str]] = {
    "discovery": {
        "high": "검색 노출 기본기가 잘 갖춰져 있습니다.",
        "mid": "검색엔진이 사이트를 제대로 인식하지 못하는 항목이 있습니다. 기본 SEO 설정을 점검하세요.",
        "low": "검색엔진에서 병원을 찾기 어려운 상태입니다. sitemap, robots.txt, meta tags부터 시급히 개선하세요.",
    },
    "trust": {
        "high": "환자가 신뢰할 수 있는 사이트로 잘 구성되어 있습니다.",
        "mid": "신뢰도를 높일 수 있는 요소가 부족합니다. HTTPS, 구조화 데이터, E-E-A-T 신호를 보강하세요.",
        "low": "환자가 사이트를 신뢰하기 어려운 상태입니다. 보안(HTTPS)과 전문성 표시를 즉시 개선하세요.",
    },
    "comparison": {
        "high": "경쟁 병원과 비교 시 충분한 정보를 제공하고 있습니다.",
        "mid": "비교 검토 단계에서 환자를 잃을 수 있습니다. FAQ, 이미지, 다국어 페이지를 보강하세요.",
        "low": "경쟁 병원 대비 정보가 크게 부족합니다. 콘텐츠와 다국어 지원을 시급히 확충하세요.",
    },
    "booking": {
        "high": "예약 전환에 필요한 기술적 요소가 잘 갖춰져 있습니다.",
        "mid": "페이지 속도나 다국어 설정이 예약 전환을 방해할 수 있습니다. 성능 최적화를 진행하세요.",
        "low": "느린 로딩과 부족한 다국어 설정으로 예약 전환이 어렵습니다. LCP, INP, hreflang을 즉시 개선하세요.",
    },
}


def _get_recommendation(stage_key: str, score: float) -> str:
    recs = STAGE_RECOMMENDATIONS[stage_key]
    if score >= 70:
        return recs["high"]
    if score >= 40:
        return recs["mid"]
    return recs["low"]


def calculate_journey_scores(category_scores: dict) -> dict:
    """Calculate patient journey funnel scores from category_scores.

    Args:
        category_scores: category_scores dict from scorer.calculate_score()

    Returns:
        Dict with stages, weakest/strongest stage, overall score, and narrative.
    """
    stages: dict[str, dict] = {}
    stage_scores: dict[str, float] = {}

    for stage_key, stage_def in JOURNEY_STAGES.items():
        checks = stage_def["checks"]
        weighted_sum = 0.0
        weight_sum = 0.0
        weakest_check = None
        weakest_score = 101.0

        for check_name, check_weight in checks.items():
            cat = category_scores.get(check_name)
            if not cat:
                continue
            # Skip system_limit / api_error / not_applicable
            if cat.get("fail_type") in ("system_limit", "api_error", "not_applicable"):
                continue
            item_score = cat.get("score")
            if item_score is None:
                continue

            weighted_sum += item_score * check_weight
            weight_sum += check_weight

            if item_score < weakest_score:
                weakest_score = item_score
                weakest_check = check_name

        score = round(weighted_sum / weight_sum) if weight_sum > 0 else 0
        score = max(0, min(100, score))
        grade = calculate_grade(score)

        stages[stage_key] = {
            "score": score,
            "grade": grade,
            "display_name": stage_def["display_name"],
            "icon": stage_def["icon"],
            "description": stage_def["description"],
            "weakest_check": weakest_check,
            "recommendation": _get_recommendation(stage_key, score),
        }
        stage_scores[stage_key] = score

    if not stage_scores:
        return {
            "stages": stages,
            "weakest_stage": None,
            "strongest_stage": None,
            "overall_journey_score": 0,
            "narrative": "측정된 데이터가 없습니다.",
        }

    weakest_stage = min(stage_scores, key=stage_scores.get)  # type: ignore[arg-type]
    strongest_stage = max(stage_scores, key=stage_scores.get)  # type: ignore[arg-type]
    overall = round(sum(stage_scores.values()) / len(stage_scores))

    # Build narrative
    strongest_name = JOURNEY_STAGES[strongest_stage]["display_name"]
    weakest_name = JOURNEY_STAGES[weakest_stage]["display_name"]
    if stage_scores[strongest_stage] == stage_scores[weakest_stage]:
        narrative = f"모든 단계가 동일한 수준({overall}점)입니다."
    else:
        narrative = (
            f"'{strongest_name}' 단계는 양호하나, "
            f"'{weakest_name}' 단계가 가장 취약하여 집중 개선이 필요합니다."
        )

    return {
        "stages": stages,
        "weakest_stage": weakest_stage,
        "strongest_stage": strongest_stage,
        "overall_journey_score": overall,
        "narrative": narrative,
    }
