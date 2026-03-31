"""Tests for medical advertising compliance checker."""

from app.services.medical_compliance import check_medical_compliance


def _make_page(html: str, url: str = "https://example.com") -> dict:
    return {"url": url, "html": html}


def _wrap_html(body: str, lang: str = "ko") -> str:
    return f'<html lang="{lang}"><head><title>Test</title></head><body>{body}</body></html>'


def _kr_body(text: str) -> str:
    """Wrap text with enough Korean characters for language detection."""
    return f"<p>안녕하세요 피부과 전문 병원입니다. {text}</p>"


def _jp_body(text: str) -> str:
    """Wrap text with enough Japanese characters for language detection."""
    return f"<p>こんにちは。美容皮膚科クリニックです。{text}</p>"


class TestKoreanExaggeration:
    def test_detects_best(self):
        html = _wrap_html(_kr_body("최고의 시술을 제공합니다"))
        result = check_medical_compliance([_make_page(html)])
        assert result["by_country"]["kr"]["violations"] > 0
        rules = [v["rule"] for v in result["violations"]]
        assert "kr_exaggeration" in rules

    def test_detects_guarantee(self):
        html = _wrap_html(_kr_body("효과를 보장합니다"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_exaggeration" for v in result["violations"])

    def test_detects_perfect(self):
        html = _wrap_html(_kr_body("완벽한 피부를 만들어 드립니다"))
        result = check_medical_compliance([_make_page(html)])
        assert result["by_country"]["kr"]["violations"] > 0

    def test_detects_100_percent(self):
        html = _wrap_html(_kr_body("만족도 100% 시술입니다"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_exaggeration" for v in result["violations"])

    def test_clean_page_no_violation(self):
        html = _wrap_html(_kr_body("숙련된 의료진이 정성껏 시술합니다"))
        result = check_medical_compliance([_make_page(html)])
        kr_exag = [v for v in result["violations"] if v["rule"] == "kr_exaggeration"]
        assert len(kr_exag) == 0


class TestKoreanComparison:
    def test_detects_superlative(self):
        html = _wrap_html(_kr_body("가장 안전한 시술 방법"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_comparison" for v in result["violations"])

    def test_detects_first(self):
        html = _wrap_html(_kr_body("최초의 레이저 기술"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_comparison" for v in result["violations"])


class TestKoreanDiscount:
    def test_detects_free_procedure(self):
        html = _wrap_html(_kr_body("무료 시술 이벤트 진행중"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_discount" for v in result["violations"])

    def test_detects_heavy_discount(self):
        html = _wrap_html(_kr_body("보톡스 50% 할인"))
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "kr_discount" for v in result["violations"])

    def test_small_discount_ok(self):
        html = _wrap_html(_kr_body("10% 할인 이벤트"))
        result = check_medical_compliance([_make_page(html)])
        kr_disc = [v for v in result["violations"] if v["rule"] == "kr_discount"]
        assert len(kr_disc) == 0


class TestKoreanSideEffects:
    def test_procedure_page_without_disclosure(self):
        html = _wrap_html(_kr_body("보톡스 시술 안내"))
        result = check_medical_compliance([
            _make_page(html, url="https://example.com/botox-treatment"),
        ])
        assert any(v["rule"] == "kr_no_side_effects" for v in result["violations"])

    def test_procedure_page_with_disclosure(self):
        html = _wrap_html(_kr_body("보톡스 시술 안내. 부작용: 멍, 붓기가 발생할 수 있으며 개인 차이가 있습니다"))
        result = check_medical_compliance([
            _make_page(html, url="https://example.com/botox-treatment"),
        ])
        no_side = [v for v in result["violations"] if v["rule"] == "kr_no_side_effects"]
        assert len(no_side) == 0
        assert any(c["rule"] == "kr_side_effects_disclosed" for c in result["compliant_items"])

    def test_non_procedure_page_no_check(self):
        html = _wrap_html(_kr_body("병원 소개 페이지입니다"))
        result = check_medical_compliance([
            _make_page(html, url="https://example.com/about"),
        ])
        no_side = [v for v in result["violations"] if v["rule"] == "kr_no_side_effects"]
        assert len(no_side) == 0


class TestJapaneseViolations:
    def test_detects_testimonial(self):
        html = _wrap_html(_jp_body("体験談をご紹介します"), lang="ja")
        result = check_medical_compliance([_make_page(html)])
        assert any(v["rule"] == "jp_testimonial" for v in result["violations"])

    def test_detects_comparison(self):
        html = _wrap_html(_jp_body("日本一の美容クリニック"), lang="ja")
        result = check_medical_compliance([_make_page(html)])
        assert any(w["rule"] == "jp_comparison" for w in result["warnings"])

    def test_clean_jp_page(self):
        html = _wrap_html(_jp_body("経験豊富な医師が丁寧に施術いたします"), lang="ja")
        result = check_medical_compliance([_make_page(html)])
        jp_issues = [v for v in result["violations"] if v["rule"].startswith("jp_")]
        assert len(jp_issues) == 0


class TestGlobalCompliance:
    def test_no_privacy_policy(self):
        html = _wrap_html(_kr_body("병원 홈페이지"))
        result = check_medical_compliance([_make_page(html)])
        assert any(
            v["rule"] == "global_privacy"
            for v in result["violations"]
        )

    def test_privacy_policy_found(self):
        html = _wrap_html(_kr_body("개인정보 처리방침에 따라 운영합니다"))
        result = check_medical_compliance([_make_page(html)])
        privacy_violations = [v for v in result["violations"] if v["rule"] == "global_privacy"]
        assert len(privacy_violations) == 0

    def test_multilingual_privacy(self):
        pages = [
            _make_page(_wrap_html(_kr_body("개인정보 처리방침"))),
            _make_page(_wrap_html(_jp_body("プライバシーポリシー"), lang="ja")),
        ]
        result = check_medical_compliance(pages)
        assert any(c["rule"] == "global_privacy" for c in result["compliant_items"])


class TestScoring:
    def test_perfect_score(self):
        html = _wrap_html(_kr_body(
            "숙련된 의료진이 시술합니다. 개인정보 처리방침을 준수합니다."
        ))
        result = check_medical_compliance([_make_page(html)])
        assert result["overall_score"] >= 80

    def test_low_score_many_violations(self):
        html = _wrap_html(_kr_body(
            "최고의 시술! 100% 보장! 완벽한 결과! 무료 시술 이벤트! "
            "가장 안전한 최초의 독보적인 업계 최초 기술!"
        ))
        result = check_medical_compliance([_make_page(html)])
        assert result["overall_score"] < 70

    def test_empty_pages(self):
        result = check_medical_compliance([])
        assert result["overall_score"] == 0
        assert result["violations"] == []

    def test_country_scores_independent(self):
        pages = [
            _make_page(_wrap_html(_kr_body("최고의 시술"))),
            _make_page(_wrap_html(_jp_body("経験豊富な医師"), lang="ja")),
        ]
        result = check_medical_compliance(pages)
        assert result["by_country"]["kr"]["violations"] > 0
        assert result["by_country"]["jp"]["violations"] == 0


class TestRecommendations:
    def test_generates_recommendations(self):
        html = _wrap_html(_kr_body("최고의 시술! 무료 상담!"))
        result = check_medical_compliance([_make_page(html)])
        assert len(result["recommendations"]) > 0
        priorities = [r["priority"] for r in result["recommendations"]]
        assert "high" in priorities

    def test_no_recommendations_for_clean_page(self):
        html = _wrap_html(_kr_body("숙련된 의료진. 개인정보 처리방침 준수"))
        result = check_medical_compliance([_make_page(html)])
        # May have minor warnings but no high-priority recommendations
        high_recs = [r for r in result["recommendations"] if r["priority"] == "high"]
        assert len(high_recs) == 0


class TestViolationMetadata:
    def test_violation_has_law_reference(self):
        html = _wrap_html(_kr_body("최고의 시술"))
        result = check_medical_compliance([_make_page(html)])
        for v in result["violations"]:
            assert "law" in v
            assert len(v["law"]) > 0

    def test_violation_has_url(self):
        url = "https://example.com/treatment"
        html = _wrap_html(_kr_body("최고의 시술"))
        result = check_medical_compliance([_make_page(html, url=url)])
        for v in result["violations"]:
            assert v["url"] == url

    def test_violation_has_context_text(self):
        html = _wrap_html(_kr_body("이것은 최고의 시술입니다"))
        result = check_medical_compliance([_make_page(html)])
        assert any("최고" in v["text"] for v in result["violations"])
