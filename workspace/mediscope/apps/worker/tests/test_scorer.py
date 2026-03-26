"""Tests for app.services.scorer — score calculation logic."""

from app.checks.base import CheckResult, Grade
from app.services.scorer import WEIGHTS, calculate_grade, calculate_score


class TestWeights:
    def test_weights_sum_is_095(self):
        total = sum(WEIGHTS.values())
        assert abs(total - 0.95) < 0.001, f"WEIGHTS sum = {total}, expected 0.95"

    def test_weights_has_20_items(self):
        assert len(WEIGHTS) == 20


class TestCalculateGrade:
    def test_grade_a(self):
        assert calculate_grade(80) == "A"
        assert calculate_grade(100) == "A"
        assert calculate_grade(95) == "A"

    def test_grade_b(self):
        assert calculate_grade(60) == "B"
        assert calculate_grade(79.9) == "B"

    def test_grade_c(self):
        assert calculate_grade(40) == "C"
        assert calculate_grade(59.9) == "C"

    def test_grade_d(self):
        assert calculate_grade(20) == "D"
        assert calculate_grade(39.9) == "D"

    def test_grade_f(self):
        assert calculate_grade(0) == "F"
        assert calculate_grade(19.9) == "F"


class TestCalculateScore:
    def test_empty_results(self):
        result = calculate_score([])
        assert result["total_score"] == 0
        assert result["grade"] == "F"
        assert result["items_checked"] == 0

    def test_all_perfect(self):
        results = [
            CheckResult(name=name, score=1.0, grade=Grade.PASS)
            for name in WEIGHTS
        ]
        result = calculate_score(results)
        assert result["total_score"] == 100
        assert result["grade"] == "A"
        assert result["items_checked"] == 20

    def test_all_zero(self):
        results = [
            CheckResult(name=name, score=0.0, grade=Grade.FAIL)
            for name in WEIGHTS
        ]
        result = calculate_score(results)
        assert result["total_score"] == 0
        assert result["grade"] == "F"

    def test_mixed_scores(self):
        results = [
            CheckResult(name="meta_tags", score=1.0, grade=Grade.PASS),
            CheckResult(name="headings", score=0.5, grade=Grade.WARN),
            CheckResult(name="images_alt", score=0.0, grade=Grade.FAIL),
        ]
        result = calculate_score(results)
        assert 0 < result["total_score"] < 100
        assert result["items_checked"] == 3

    def test_category_scores_present(self):
        results = [
            CheckResult(
                name="meta_tags", score=1.0, grade=Grade.PASS,
                details={"title": "Test"}, issues=[],
            ),
        ]
        result = calculate_score(results)
        assert "meta_tags" in result["category_scores"]
        cs = result["category_scores"]["meta_tags"]
        assert cs["score"] == 100.0
        assert cs["grade"] == "pass"
        assert cs["weight"] == 0.10

    def test_missing_checks_marked_skip(self):
        result = calculate_score([])
        for name in WEIGHTS:
            assert result["category_scores"][name]["grade"] == "skip"

    def test_partial_results_normalize(self):
        # Only one check with score 1.0 — should normalize to 100
        results = [
            CheckResult(name="robots_txt", score=1.0, grade=Grade.PASS),
        ]
        result = calculate_score(results)
        assert result["total_score"] == 100
        assert result["items_checked"] == 1
