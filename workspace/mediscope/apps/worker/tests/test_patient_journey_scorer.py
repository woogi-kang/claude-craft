"""Tests for patient journey funnel scoring."""

from app.services.patient_journey_scorer import (
    JOURNEY_STAGES,
    calculate_journey_scores,
)


class TestJourneyStagesConfig:
    def test_stage_weights_sum_to_one(self):
        for stage_key, stage_def in JOURNEY_STAGES.items():
            total = sum(stage_def["checks"].values())
            assert abs(total - 1.0) < 0.001, (
                f"{stage_key} weights sum = {total}, expected 1.0"
            )

    def test_all_four_stages_defined(self):
        assert set(JOURNEY_STAGES.keys()) == {
            "discovery", "trust", "comparison", "booking",
        }

    def test_all_checks_reference_valid_scorer_keys(self):
        from app.services.scorer import WEIGHTS

        for stage_key, stage_def in JOURNEY_STAGES.items():
            for check_name in stage_def["checks"]:
                assert check_name in WEIGHTS, (
                    f"{stage_key}.{check_name} not in scorer WEIGHTS"
                )


def _make_category_scores(overrides: dict | None = None) -> dict:
    """Create a full category_scores dict with default score=50 for all checks."""
    from app.services.scorer import WEIGHTS

    scores = {}
    for name, weight in WEIGHTS.items():
        scores[name] = {
            "score": 50.0,
            "weight": weight,
            "grade": "warn",
            "fail_type": "site_issue",
            "display_name": name,
            "description": "",
            "recommendation": "",
            "issues": [],
            "details": {},
        }
    if overrides:
        for key, val in overrides.items():
            if key in scores:
                scores[key].update(val)
    return scores


class TestCalculateJourneyScores:
    def test_all_perfect_scores(self):
        scores = _make_category_scores({
            name: {"score": 100.0, "grade": "pass"}
            for name in [
                "sitemap", "robots_txt", "meta_tags", "headings", "url_structure",
                "international_search", "ai_search_mention", "eeat_signals", "https",
                "structured_data", "content_clarity", "errors_404", "canonical",
                "faq_content", "images_alt", "links", "performance_score",
                "multilingual_pages", "overseas_channels", "lcp", "inp", "cls",
                "hreflang",
            ]
        })
        result = calculate_journey_scores(scores)

        assert result["overall_journey_score"] == 100
        for stage in result["stages"].values():
            assert stage["score"] == 100
            assert stage["grade"] == "A"

    def test_all_zero_scores(self):
        scores = _make_category_scores({
            name: {"score": 0.0, "grade": "fail"}
            for name in [
                "sitemap", "robots_txt", "meta_tags", "headings", "url_structure",
                "international_search", "ai_search_mention", "eeat_signals", "https",
                "structured_data", "content_clarity", "errors_404", "canonical",
                "faq_content", "images_alt", "links", "performance_score",
                "multilingual_pages", "overseas_channels", "lcp", "inp", "cls",
                "hreflang",
            ]
        })
        result = calculate_journey_scores(scores)

        assert result["overall_journey_score"] == 0
        for stage in result["stages"].values():
            assert stage["score"] == 0
            assert stage["grade"] == "F"

    def test_weakest_and_strongest_stages(self):
        scores = _make_category_scores()
        # Make discovery checks high, comparison checks low
        for name in JOURNEY_STAGES["discovery"]["checks"]:
            scores[name]["score"] = 90.0
        for name in JOURNEY_STAGES["comparison"]["checks"]:
            scores[name]["score"] = 10.0

        result = calculate_journey_scores(scores)
        assert result["strongest_stage"] == "discovery"
        assert result["weakest_stage"] == "comparison"

    def test_narrative_generated(self):
        scores = _make_category_scores()
        result = calculate_journey_scores(scores)
        assert isinstance(result["narrative"], str)
        assert len(result["narrative"]) > 0

    def test_empty_category_scores(self):
        result = calculate_journey_scores({})
        assert result["overall_journey_score"] == 0
        # All stages exist but with score 0
        for stage in result["stages"].values():
            assert stage["score"] == 0
            assert stage["grade"] == "F"

    def test_system_limit_checks_excluded(self):
        scores = _make_category_scores()
        # Mark all discovery checks as system_limit
        for name in JOURNEY_STAGES["discovery"]["checks"]:
            scores[name]["fail_type"] = "system_limit"
            scores[name]["score"] = None

        result = calculate_journey_scores(scores)
        # Discovery stage should be 0 since no valid checks
        assert result["stages"]["discovery"]["score"] == 0

    def test_each_stage_has_required_fields(self):
        scores = _make_category_scores()
        result = calculate_journey_scores(scores)

        for stage_key, stage in result["stages"].items():
            assert "score" in stage
            assert "grade" in stage
            assert "display_name" in stage
            assert "icon" in stage
            assert "description" in stage
            assert "weakest_check" in stage
            assert "recommendation" in stage

    def test_grades_match_scores(self):
        scores = _make_category_scores()
        result = calculate_journey_scores(scores)

        from app.services.scorer import calculate_grade

        for stage in result["stages"].values():
            assert stage["grade"] == calculate_grade(stage["score"])

    def test_performance_score_shared_between_comparison_and_booking(self):
        """performance_score is used in both comparison and booking stages."""
        scores = _make_category_scores()
        scores["performance_score"]["score"] = 0.0

        result = calculate_journey_scores(scores)
        # Both comparison and booking should be affected
        assert result["stages"]["comparison"]["score"] < 50
        assert result["stages"]["booking"]["score"] < 50
