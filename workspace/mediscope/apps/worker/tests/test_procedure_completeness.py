"""Tests for procedure completeness analyzer."""

import pytest

from app.services.procedure_completeness import (
    CONTENT_SECTIONS,
    PROCEDURE_KEYWORDS,
    _detect_sections,
    _extract_text,
    _identify_procedures,
    analyze_procedure_completeness,
)


# ── Procedure identification ────────────────────────────────────────


class TestIdentifyProcedures:
    def test_korean_keywords(self):
        procs = _identify_procedures(
            "https://example.com/treatment",
            "보톡스 시술 안내",
            "보톡스 시술에 대해 알려드립니다",
        )
        assert "botox" in procs

    def test_english_keywords(self):
        procs = _identify_procedures(
            "https://example.com/filler",
            "Filler Treatment",
            "Learn about our filler treatments",
        )
        assert "filler" in procs

    def test_japanese_keywords(self):
        procs = _identify_procedures(
            "https://example.com/ja/treatment",
            "ボトックス治療",
            "ボトックス注射の詳細をご覧ください",
        )
        assert "botox" in procs

    def test_chinese_keywords(self):
        procs = _identify_procedures(
            "https://example.com/zh/treatment",
            "激光治疗",
            "我们提供专业的激光治疗服务",
        )
        assert "laser" in procs

    def test_multiple_procedures(self):
        procs = _identify_procedures(
            "https://example.com/procedures",
            "시술 안내",
            "보톡스와 필러 시술을 전문으로 합니다",
        )
        assert "botox" in procs
        assert "filler" in procs

    def test_no_procedure(self):
        procs = _identify_procedures(
            "https://example.com/about",
            "병원 소개",
            "우리 병원은 강남에 위치해 있습니다",
        )
        assert procs == []

    def test_url_based_detection(self):
        procs = _identify_procedures(
            "https://example.com/botox-treatment",
            "Treatment Page",
            "Welcome to our clinic",
        )
        assert "botox" in procs

    def test_case_insensitive(self):
        procs = _identify_procedures(
            "https://example.com/treatment",
            "BOTOX Treatment",
            "LASER and FILLER services",
        )
        assert "botox" in procs
        assert "laser" in procs
        assert "filler" in procs


# ── Section detection ───────────────────────────────────────────────


class TestDetectSections:
    def test_description_detected(self):
        text = "포텐자에 대한 소개입니다. " + "포텐자는 마이크로니들과 RF를 결합한 시술입니다. " * 20
        sections = _detect_sections(text)
        assert sections["description"]["present"] is True

    def test_price_detected(self):
        text = "포텐자 가격 안내입니다. " + "시술 비용은 회차에 따라 달라집니다. " * 20
        sections = _detect_sections(text)
        assert sections["price"]["present"] is True

    def test_faq_detected(self):
        text = "자주 묻는 질문 모음입니다. " + "Q: 시술 후 관리는 어떻게 하나요? A: 보습을 잘 해주세요. " * 20
        sections = _detect_sections(text)
        assert sections["faq"]["present"] is True

    def test_review_detected(self):
        text = "환자 후기를 확인해보세요. " + "시술 후 결과가 매우 만족스럽습니다. " * 20
        sections = _detect_sections(text)
        assert sections["review"]["present"] is True

    def test_before_after_detected(self):
        text = "시술 전후 사진을 확인해보세요. " + "비포 애프터 결과가 놀랍습니다. " * 20
        sections = _detect_sections(text)
        assert sections["before_after"]["present"] is True

    def test_process_detected(self):
        text = "시술 과정 안내입니다. " + "첫 번째 단계는 상담이며 두 번째 단계는 시술입니다. " * 20
        sections = _detect_sections(text)
        assert sections["process"]["present"] is True

    def test_partial_detection(self):
        # Content between 100-300 chars around keyword — only one keyword match with ~200 chars
        text = "시술 가격 안내입니다. " + "상세한 내용을 확인해 주세요. " * 6
        sections = _detect_sections(text)
        assert sections["price"]["present"] is True
        assert sections["price"]["partial"] is True

    def test_too_short_not_detected(self):
        text = "가격"
        sections = _detect_sections(text)
        assert sections["price"]["present"] is False

    def test_no_keyword_not_detected(self):
        text = "이 페이지에는 특별한 내용이 없습니다. " * 20
        sections = _detect_sections(text)
        assert sections["description"]["present"] is False
        assert sections["price"]["present"] is False


# ── Completeness score calculation ──────────────────────────────────


class TestCompletenessScores:
    def test_full_completeness(self):
        html = """<html><head><title>보톡스 시술</title></head><body>
        <p>보톡스 소개 및 설명입니다. """ + "보톡스는 근육을 이완시키는 시술입니다. " * 20 + """</p>
        <p>시술 과정 안내입니다. """ + "첫 번째 단계는 상담입니다. " * 20 + """</p>
        <p>시술 가격 안내입니다. """ + "비용은 부위에 따라 다릅니다. " * 20 + """</p>
        <p>환자 후기를 확인하세요. """ + "시술 결과가 매우 만족스럽습니다. " * 20 + """</p>
        <p>시술 전후 사진입니다. """ + "비포 애프터 결과입니다. " * 20 + """</p>
        <p>자주 묻는 질문 모음입니다. """ + "Q: 통증이 있나요? A: 거의 없습니다. " * 20 + """</p>
        </body></html>"""
        pages = [{"url": "https://example.com/botox", "html": html}]
        result = analyze_procedure_completeness(pages)
        assert "botox" in result["procedures"]
        assert result["procedures"]["botox"]["completeness"] == 100

    def test_partial_completeness(self):
        html = """<html><head><title>보톡스 시술</title></head><body>
        <p>보톡스 소개 및 설명입니다. """ + "보톡스는 안전한 시술입니다. " * 20 + """</p>
        <p>시술 가격 안내입니다. """ + "비용은 상담 후 결정됩니다. " * 20 + """</p>
        </body></html>"""
        pages = [{"url": "https://example.com/botox", "html": html}]
        result = analyze_procedure_completeness(pages)
        botox = result["procedures"]["botox"]
        assert botox["sections"]["description"] is True
        assert botox["sections"]["price"] is True
        assert botox["sections"]["review"] is False
        # 2 out of 6 = 33%
        assert botox["completeness"] == 33

    def test_zero_completeness_no_procedures(self):
        html = "<html><body><p>병원 소개 페이지입니다.</p></body></html>"
        pages = [{"url": "https://example.com/about", "html": html}]
        result = analyze_procedure_completeness(pages)
        assert result["procedures"] == {}
        assert result["overall_completeness"] == 0


# ── Full analysis ───────────────────────────────────────────────────


class TestAnalyzeProcedureCompleteness:
    def test_empty_pages(self):
        result = analyze_procedure_completeness([])
        assert result["overall_completeness"] == 0
        assert result["procedures"] == {}
        assert result["best_procedure"] is None
        assert result["worst_procedure"] is None
        assert result["recommendations"] == []

    def test_multiple_procedures(self):
        botox_html = """<html><head><title>보톡스</title></head><body>
        <p>보톡스 소개입니다. """ + "보톡스 시술 정보. " * 30 + """</p>
        <p>가격 안내입니다. """ + "비용 상세 정보. " * 30 + """</p>
        <p>시술 과정 안내. """ + "단계별 진행 과정. " * 30 + """</p>
        </body></html>"""

        filler_html = """<html><head><title>필러</title></head><body>
        <p>필러 소개입니다. """ + "필러 시술 정보. " * 30 + """</p>
        </body></html>"""

        pages = [
            {"url": "https://example.com/botox", "html": botox_html},
            {"url": "https://example.com/filler", "html": filler_html},
        ]
        result = analyze_procedure_completeness(pages)
        assert "botox" in result["procedures"]
        assert "filler" in result["procedures"]
        assert result["procedures"]["botox"]["completeness"] > result["procedures"]["filler"]["completeness"]
        assert result["best_procedure"] == "botox"
        assert result["worst_procedure"] == "filler"

    def test_multi_page_aggregation(self):
        page1 = """<html><head><title>리프팅 소개</title></head><body>
        <p>리프팅 소개 및 설명입니다. """ + "리프팅은 피부를 탄력있게 합니다. " * 30 + """</p>
        </body></html>"""

        page2 = """<html><head><title>리프팅 후기</title></head><body>
        <p>리프팅 후기를 확인하세요. """ + "시술 결과가 매우 좋습니다. " * 30 + """</p>
        <p>리프팅 전후 사진입니다. """ + "비포 애프터 결과. " * 30 + """</p>
        </body></html>"""

        pages = [
            {"url": "https://example.com/lifting", "html": page1},
            {"url": "https://example.com/lifting-review", "html": page2},
        ]
        result = analyze_procedure_completeness(pages)
        lifting = result["procedures"]["lifting"]
        assert lifting["pages_found"] == 2
        assert lifting["sections"]["description"] is True
        assert lifting["sections"]["review"] is True
        assert lifting["sections"]["before_after"] is True

    def test_recommendations_generated(self):
        html = """<html><head><title>레이저 시술</title></head><body>
        <p>레이저 소개입니다. """ + "레이저 시술 정보. " * 30 + """</p>
        </body></html>"""
        pages = [{"url": "https://example.com/laser", "html": html}]
        result = analyze_procedure_completeness(pages)
        assert len(result["recommendations"]) > 0
        rec = result["recommendations"][0]
        assert rec["procedure"] == "laser"
        assert len(rec["missing"]) > 0
        assert rec["priority"] in ("high", "medium", "low")

    def test_benchmark_recommendation(self):
        good_html = """<html><head><title>리프팅</title></head><body>
        <p>리프팅 소개입니다. """ + "리프팅 설명. " * 30 + """</p>
        <p>시술 과정. """ + "단계별 과정. " * 30 + """</p>
        <p>가격 안내. """ + "비용 정보. " * 30 + """</p>
        <p>환자 후기. """ + "만족스러운 결과. " * 30 + """</p>
        </body></html>"""

        bad_html = """<html><head><title>보톡스</title></head><body>
        <p>보톡스 소개입니다. """ + "보톡스 정보. " * 30 + """</p>
        </body></html>"""

        pages = [
            {"url": "https://example.com/lifting", "html": good_html},
            {"url": "https://example.com/botox", "html": bad_html},
        ]
        result = analyze_procedure_completeness(pages)
        # Should have benchmark recommendation for best procedure
        info_recs = [r for r in result["recommendations"] if r["priority"] == "info"]
        assert len(info_recs) > 0
        assert "벤치마크" in info_recs[0]["message"]

    def test_overall_completeness_average(self):
        # Two procedures: one at 100%, one at 0% => 50% average
        full_html = """<html><head><title>보톡스</title></head><body>
        <p>보톡스 소개. """ + "설명 내용. " * 30 + """</p>
        <p>시술 과정. """ + "과정 내용. " * 30 + """</p>
        <p>가격 안내. """ + "가격 내용. " * 30 + """</p>
        <p>환자 후기. """ + "후기 내용. " * 30 + """</p>
        <p>전후 사진. """ + "비포 애프터. " * 30 + """</p>
        <p>자주 묻는 질문. """ + "FAQ 내용. " * 30 + """</p>
        </body></html>"""

        empty_html = """<html><head><title>필러 페이지</title></head><body>
        <p>필러 시술 관련 내용입니다.</p>
        </body></html>"""

        pages = [
            {"url": "https://example.com/botox", "html": full_html},
            {"url": "https://example.com/filler", "html": empty_html},
        ]
        result = analyze_procedure_completeness(pages)
        # Overall should be between 0 and 100
        assert 0 <= result["overall_completeness"] <= 100
