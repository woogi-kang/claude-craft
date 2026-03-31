"""Tests for portal_scorer module."""

import pytest

from app.services.portal_scorer import (
    PORTAL_CHECK_MAP,
    calculate_portal_scores,
)


def _make_category_scores(**overrides: float) -> dict:
    """Create a minimal category_scores dict with given check scores (0-100)."""
    base = {}
    for name, score in overrides.items():
        base[name] = {
            "score": score,
            "weight": 0.05,
            "grade": "pass" if score >= 80 else "warn" if score >= 40 else "fail",
            "fail_type": "site_issue",
            "display_name": name,
            "description": "",
            "recommendation": f"Improve {name}",
            "issues": [] if score >= 80 else [f"{name} needs work"],
            "details": {},
        }
    return base


class TestCalculatePortalScores:
    def test_returns_all_portals(self):
        scores = _make_category_scores(meta_tags=80, sitemap=60, robots_txt=70)
        result = calculate_portal_scores(scores)
        assert set(result.keys()) == set(PORTAL_CHECK_MAP.keys())

    def test_perfect_scores(self):
        all_checks = set()
        for portal in PORTAL_CHECK_MAP.values():
            all_checks.update(portal["checks"])
        scores = _make_category_scores(**{c: 100 for c in all_checks})
        result = calculate_portal_scores(scores)
        for portal_key, portal_data in result.items():
            assert portal_data["score"] == 100, f"{portal_key} should be 100"
            assert portal_data["grade"] == "A"

    def test_zero_scores(self):
        all_checks = set()
        for portal in PORTAL_CHECK_MAP.values():
            all_checks.update(portal["checks"])
        scores = _make_category_scores(**{c: 0 for c in all_checks})
        result = calculate_portal_scores(scores)
        for portal_key, portal_data in result.items():
            assert portal_data["score"] == 0, f"{portal_key} should be 0"
            assert portal_data["grade"] == "F"

    def test_missing_checks_handled(self):
        """Portals with no matching checks should score 0."""
        result = calculate_portal_scores({})
        for portal_data in result.values():
            assert portal_data["score"] == 0
            assert portal_data["grade"] == "F"

    def test_skips_system_limit(self):
        scores = _make_category_scores(meta_tags=100)
        scores["meta_tags"]["fail_type"] = "system_limit"
        result = calculate_portal_scores(scores)
        # naver relies heavily on meta_tags; should get 0 if only check is skipped
        assert result["naver"]["checks_measured"] == 0

    def test_skips_api_error(self):
        scores = _make_category_scores(ai_search_mention=50)
        scores["ai_search_mention"]["fail_type"] = "api_error"
        result = calculate_portal_scores(scores)
        assert result["ai_search"]["checks_measured"] == 0

    def test_grade_boundaries(self):
        for score_val, expected_grade in [(80, "A"), (79, "B"), (60, "B"), (59, "C"), (40, "C"), (39, "D"), (20, "D"), (19, "F"), (0, "F")]:
            scores = _make_category_scores(
                sitemap=score_val, robots_txt=score_val, structured_data=score_val,
                performance_score=score_val, lcp=score_val, inp=score_val,
                cls=score_val, https=score_val, canonical=score_val,
                meta_tags=score_val, images_alt=score_val,
            )
            result = calculate_portal_scores(scores)
            assert result["google"]["grade"] == expected_grade, (
                f"Score {score_val} should give grade {expected_grade}, got {result['google']['grade']}"
            )

    def test_issues_returned(self):
        scores = _make_category_scores(meta_tags=30, sitemap=20, robots_txt=90)
        result = calculate_portal_scores(scores)
        # naver has meta_tags and sitemap as low-scoring checks
        assert len(result["naver"]["issues"]) > 0
        assert len(result["naver"]["issues"]) <= 2

    def test_no_issues_for_perfect_portal(self):
        scores = _make_category_scores(
            meta_tags=100, headings=100, sitemap=100,
            robots_txt=100, links=100, images_alt=100,
        )
        result = calculate_portal_scores(scores)
        assert result["naver"]["issues"] == []

    def test_portal_structure(self):
        scores = _make_category_scores(meta_tags=70)
        result = calculate_portal_scores(scores)
        for portal_data in result.values():
            assert "score" in portal_data
            assert "grade" in portal_data
            assert "label" in portal_data
            assert "issues" in portal_data
            assert "checks_measured" in portal_data
            assert "checks_total" in portal_data
            assert isinstance(portal_data["score"], int)
            assert isinstance(portal_data["issues"], list)

    def test_weights_sum_to_one(self):
        for portal_key, portal_def in PORTAL_CHECK_MAP.items():
            total = sum(portal_def["weights"].values())
            assert abs(total - 1.0) < 0.01, (
                f"{portal_key} weights sum to {total}, expected ~1.0"
            )
