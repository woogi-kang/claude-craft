"""Tests for keyword_engine service."""

import pytest

from app.services.keyword_engine import (
    PROCEDURE_POPULARITY,
    PROCEDURE_TRANSLATIONS,
    REGION_TRANSLATIONS,
    _extract_procedures_from_pages,
    _generate_base_keywords,
    _generate_ko_keywords,
    _generate_multilingual_keywords,
    _short_region,
    extract_and_generate_keywords,
)


def _make_page(url: str = "https://example.com", title: str = "", html: str = "") -> dict:
    return {"url": url, "html": html, "title": title}


# ---------------------------------------------------------------------------
# Procedure extraction
# ---------------------------------------------------------------------------

class TestExtractProcedures:
    def test_extract_korean_procedure(self):
        pages = [_make_page(html="<p>보톡스 시술 안내</p>")]
        assert "botox" in _extract_procedures_from_pages(pages)

    def test_extract_english_procedure(self):
        pages = [_make_page(html="<p>Our botox treatment</p>")]
        assert "botox" in _extract_procedures_from_pages(pages)

    def test_extract_japanese_procedure(self):
        pages = [_make_page(html="<p>ボトックス治療のご案内</p>")]
        assert "botox" in _extract_procedures_from_pages(pages)

    def test_extract_chinese_procedure(self):
        pages = [_make_page(html="<p>肉毒杆菌注射</p>")]
        assert "botox" in _extract_procedures_from_pages(pages)

    def test_extract_multiple_procedures(self):
        pages = [_make_page(html="<p>보톡스와 필러 시술</p>")]
        found = _extract_procedures_from_pages(pages)
        assert "botox" in found
        assert "filler" in found

    def test_extract_from_url(self):
        pages = [_make_page(url="https://clinic.com/potenza-treatment")]
        assert "potenza" in _extract_procedures_from_pages(pages)

    def test_extract_from_title(self):
        pages = [_make_page(title="리프팅 전문 클리닉")]
        assert "lifting" in _extract_procedures_from_pages(pages)

    def test_no_procedures_found(self):
        pages = [_make_page(html="<p>일반 의원 소개</p>")]
        assert _extract_procedures_from_pages(pages) == []

    def test_empty_pages(self):
        assert _extract_procedures_from_pages([]) == []

    def test_across_multiple_pages(self):
        pages = [
            _make_page(html="<p>보톡스 안내</p>"),
            _make_page(html="<p>레이저 치료</p>"),
        ]
        found = _extract_procedures_from_pages(pages)
        assert "botox" in found
        assert "laser" in found


# ---------------------------------------------------------------------------
# Korean keyword generation
# ---------------------------------------------------------------------------

class TestKoreanKeywords:
    def test_generates_four_patterns(self):
        keywords = _generate_ko_keywords("홍대/마포", "botox", "보톡스")
        texts = [k["keyword"] for k in keywords]
        assert "홍대 보톡스" in texts
        assert "보톡스 홍대" in texts
        assert "홍대 보톡스 가격" in texts
        assert "홍대 보톡스 잘하는곳" in texts

    def test_all_korean_language(self):
        keywords = _generate_ko_keywords("강남/서초", "filler", "필러")
        assert all(k["language"] == "ko" for k in keywords)

    def test_portals_include_naver(self):
        keywords = _generate_ko_keywords("명동", "laser", "레이저")
        assert all("naver" in k["portals"] for k in keywords)

    def test_priority_follows_popularity(self):
        botox_kw = _generate_ko_keywords("홍대", "botox", "보톡스")
        scar_kw = _generate_ko_keywords("홍대", "scar", "흉터")
        # First keyword of each (region+procedure) should reflect popularity
        assert botox_kw[0]["priority"] > scar_kw[0]["priority"]


# ---------------------------------------------------------------------------
# Multilingual keyword generation
# ---------------------------------------------------------------------------

class TestMultilingualKeywords:
    def test_generates_en_ja_zh(self):
        keywords = _generate_multilingual_keywords("홍대", "botox")
        langs = {k["language"] for k in keywords}
        assert {"en", "ja", "zh"} == langs

    def test_english_keyword_content(self):
        keywords = _generate_multilingual_keywords("홍대", "botox")
        en_kw = [k for k in keywords if k["language"] == "en"][0]
        assert en_kw["keyword"] == "hongdae botox"

    def test_japanese_keyword_content(self):
        keywords = _generate_multilingual_keywords("홍대", "botox")
        ja_kw = [k for k in keywords if k["language"] == "ja"][0]
        assert ja_kw["keyword"] == "弘大 ボトックス"

    def test_chinese_keyword_content(self):
        keywords = _generate_multilingual_keywords("홍대", "botox")
        zh_kw = [k for k in keywords if k["language"] == "zh"][0]
        assert zh_kw["keyword"] == "弘大 肉毒"

    def test_region_with_slash_lookup(self):
        keywords = _generate_multilingual_keywords("홍대/마포", "filler")
        en_kw = [k for k in keywords if k["language"] == "en"][0]
        assert "hongdae" in en_kw["keyword"]

    def test_unknown_region_returns_empty(self):
        keywords = _generate_multilingual_keywords("알수없는지역", "botox")
        assert keywords == []

    def test_portals_vary_by_language(self):
        keywords = _generate_multilingual_keywords("강남", "botox")
        ja_kw = [k for k in keywords if k["language"] == "ja"][0]
        assert "yahoo_jp" in ja_kw["portals"]
        zh_kw = [k for k in keywords if k["language"] == "zh"][0]
        assert "baidu" in zh_kw["portals"]


# ---------------------------------------------------------------------------
# Base keywords
# ---------------------------------------------------------------------------

class TestBaseKeywords:
    def test_generates_dermatology_keywords(self):
        keywords = _generate_base_keywords("홍대/마포")
        texts = [k["keyword"] for k in keywords]
        assert "홍대 피부과" in texts
        assert "홍대 피부과 추천" in texts

    def test_no_procedure_field(self):
        keywords = _generate_base_keywords("강남")
        assert all(k["procedure"] is None for k in keywords)


# ---------------------------------------------------------------------------
# Short region helper
# ---------------------------------------------------------------------------

class TestShortRegion:
    def test_with_slash(self):
        assert _short_region("홍대/마포") == "홍대"

    def test_without_slash(self):
        assert _short_region("명동") == "명동"

    def test_space_region(self):
        assert _short_region("부산 서면") == "부산 서면"


# ---------------------------------------------------------------------------
# Full integration: extract_and_generate_keywords
# ---------------------------------------------------------------------------

class TestExtractAndGenerateKeywords:
    def test_basic_flow(self):
        pages = [_make_page(html="<p>보톡스와 필러 시술 안내</p>")]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        assert result["region"] == "홍대"
        assert "botox" in result["procedures_found"]
        assert "filler" in result["procedures_found"]
        assert len(result["keywords"]) <= 10
        assert result["total_generated"] > 0
        assert result["selected"] == len(result["keywords"])

    def test_empty_pages(self):
        result = extract_and_generate_keywords([], region_name="홍대")
        assert result["procedures_found"] == []
        assert result["keywords"] == []
        assert result["total_generated"] == 0

    def test_empty_region(self):
        pages = [_make_page(html="<p>보톡스</p>")]
        result = extract_and_generate_keywords(pages, region_name="")
        assert result["keywords"] == []

    def test_priority_sorting(self):
        pages = [_make_page(html="<p>보톡스 흉터 치료</p>")]
        result = extract_and_generate_keywords(pages, region_name="강남")
        keywords = result["keywords"]
        # Keywords should be sorted by priority descending
        priorities = [k["priority"] for k in keywords]
        assert priorities == sorted(priorities, reverse=True)

    def test_top_10_selection(self):
        # Many procedures should generate more than 10 keywords total
        html = "<p>보톡스 필러 리프팅 레이저 포텐자 제모 미백 여드름 필링 흉터</p>"
        pages = [_make_page(html=html)]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        assert result["selected"] <= 10
        assert result["total_generated"] > 10

    def test_no_duplicate_keywords(self):
        pages = [
            _make_page(html="<p>보톡스 시술</p>"),
            _make_page(html="<p>보톡스 가격</p>"),
        ]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        keyword_texts = [k["keyword"] for k in result["keywords"]]
        assert len(keyword_texts) == len(set(keyword_texts))

    def test_keyword_structure(self):
        pages = [_make_page(html="<p>보톡스</p>")]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        kw = result["keywords"][0]
        assert "keyword" in kw
        assert "language" in kw
        assert "procedure" in kw
        assert "priority" in kw
        assert "portals" in kw

    def test_includes_base_keywords(self):
        pages = [_make_page(html="<p>보톡스</p>")]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        keyword_texts = [k["keyword"] for k in result["keywords"]]
        assert "홍대 피부과" in keyword_texts

    def test_korean_keywords_prioritized_over_foreign(self):
        pages = [_make_page(html="<p>보톡스</p>")]
        result = extract_and_generate_keywords(pages, region_name="홍대")
        keywords = result["keywords"]
        # Korean keywords should appear before foreign ones at same priority tier
        ko_indices = [i for i, k in enumerate(keywords) if k["language"] == "ko"]
        non_ko_indices = [i for i, k in enumerate(keywords) if k["language"] != "ko"]
        if ko_indices and non_ko_indices:
            assert min(ko_indices) < min(non_ko_indices)
