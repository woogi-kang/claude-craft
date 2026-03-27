"""Tests for app.services.scorer — score calculation logic."""

from app.checks.base import CheckResult, Grade
from app.services.scorer import WEIGHTS, calculate_grade, calculate_score


class TestWeights:
    def test_weights_sum_is_100(self):
        total = sum(WEIGHTS.values())
        assert abs(total - 1.0) < 0.001, f"WEIGHTS sum = {total}, expected 1.0"

    def test_weights_has_24_items(self):
        assert len(WEIGHTS) == 24


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
        assert result["items_checked"] == 24

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

    def test_system_limit_excluded_from_weight(self):
        """system_limit items should be excluded from weighted score calculation."""
        results = [
            CheckResult(name="robots_txt", score=1.0, grade=Grade.PASS),
            CheckResult(name="sitemap", score=1.0, grade=Grade.PASS),
            CheckResult(
                name="ai_search_mention", score=0.0, grade=Grade.FAIL,
                fail_type="system_limit",
                issues=["병원명 정보가 없어 AI 검색 체크를 수행할 수 없습니다"],
            ),
            CheckResult(
                name="international_search", score=0.0, grade=Grade.FAIL,
                fail_type="system_limit",
                issues=["병원명 정보가 없어 국제 검색 체크를 수행할 수 없습니다"],
            ),
        ]
        result = calculate_score(results)
        # Only robots_txt and sitemap should count (both perfect)
        assert result["total_score"] == 100
        assert result["items_checked"] == 2
        # system_limit items should have score=None in category_scores
        assert result["category_scores"]["ai_search_mention"]["score"] is None
        assert result["category_scores"]["ai_search_mention"]["fail_type"] == "system_limit"
        assert result["category_scores"]["international_search"]["score"] is None

    def test_api_error_excluded_from_weight(self):
        """api_error items should be excluded from weighted score calculation."""
        results = [
            CheckResult(name="robots_txt", score=1.0, grade=Grade.PASS),
            CheckResult(
                name="lcp", score=0.5, grade=Grade.WARN,
                fail_type="api_error",
                issues=["PageSpeed API 호출 실패"],
            ),
        ]
        result = calculate_score(results)
        # Only robots_txt should count
        assert result["total_score"] == 100
        assert result["items_checked"] == 1
        assert result["category_scores"]["lcp"]["score"] is None
        assert result["category_scores"]["lcp"]["fail_type"] == "api_error"

    def test_display_name_in_category_scores(self):
        """display_name, description, recommendation should appear in category_scores."""
        results = [
            CheckResult(
                name="robots_txt", score=1.0, grade=Grade.PASS,
                display_name="검색엔진 접근 허용",
                description="구글/네이버가 홈페이지를 읽어도 되는지 알려주는 설정 파일입니다",
                recommendation="웹 개발자에게 robots.txt 파일을 생성하고 검색엔진 접근을 허용해달라고 요청하세요",
            ),
        ]
        result = calculate_score(results)
        cs = result["category_scores"]["robots_txt"]
        assert cs["display_name"] == "검색엔진 접근 허용"
        assert cs["description"] != ""
        assert cs["recommendation"] != ""
        assert cs["fail_type"] == "site_issue"
