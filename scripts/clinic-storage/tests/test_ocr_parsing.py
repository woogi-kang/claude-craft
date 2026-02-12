"""Tests for OCR parsing helpers: parse_ocr_json, append_ocr_doctors.

Tests import directly from the clinic_crawler.ocr module.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from clinic_crawler.ocr import append_ocr_doctors as _append_ocr_doctors
from clinic_crawler.ocr import parse_ocr_json as _parse_ocr_json

# ============================================================================
# _parse_ocr_json
# ============================================================================

class TestParseOcrJson:
    def test_json_in_code_fence(self):
        text = '```json\n{"doctors": [{"name": "김상우", "role": "원장"}]}\n```'
        result = _parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["name"] == "김상우"

    def test_json_in_fence_without_lang(self):
        text = '```\n[{"name": "이지연", "role": "전문의"}]\n```'
        result = _parse_ocr_json(text)
        assert len(result) == 1

    def test_bare_json_array(self):
        text = '[{"name": "박미래", "role": "원장"}]'
        result = _parse_ocr_json(text)
        assert len(result) == 1

    def test_bare_json_object_with_doctors(self):
        text = '{"doctors": [{"name": "최민지"}]}'
        result = _parse_ocr_json(text)
        assert len(result) == 1

    def test_json_with_surrounding_text(self):
        text = 'Here are the results:\n```json\n[{"name": "김솔"}]\n```\nDone!'
        result = _parse_ocr_json(text)
        assert len(result) == 1

    def test_empty_string(self):
        assert _parse_ocr_json("") == []

    def test_none_input(self):
        assert _parse_ocr_json(None) == []

    def test_no_json_content(self):
        assert _parse_ocr_json("This is just plain text with no JSON.") == []

    def test_malformed_json(self):
        assert _parse_ocr_json('```json\n{invalid json}\n```') == []

    def test_multiple_doctors(self):
        text = '[{"name": "김상우"}, {"name": "이지연"}, {"name": "박미래"}]'
        result = _parse_ocr_json(text)
        assert len(result) == 3


# ============================================================================
# _append_ocr_doctors
# ============================================================================

class TestAppendOcrDoctors:
    def test_appends_valid_doctor(self):
        seen = set()
        result = []
        added = _append_ocr_doctors([{"name": "김상우", "role": "원장"}], seen, result)
        assert added == 1
        assert result[0]["name"] == "김상우"
        assert result[0]["ocr_source"] is True
        assert result[0]["extraction_source"] == "ocr"

    def test_deduplicates_by_name(self):
        seen = {"김상우"}
        result = []
        added = _append_ocr_doctors([{"name": "김상우", "role": "원장"}], seen, result)
        assert added == 0
        assert len(result) == 0

    def test_skips_short_name(self):
        seen = set()
        result = []
        added = _append_ocr_doctors([{"name": "김"}], seen, result)
        assert added == 0

    def test_skips_empty_name(self):
        seen = set()
        result = []
        added = _append_ocr_doctors([{"name": ""}], seen, result)
        assert added == 0

    def test_multiple_doctors_with_dedup(self):
        seen = set()
        result = []
        doctors = [
            {"name": "김상우", "role": "원장"},
            {"name": "이지연", "role": "전문의"},
            {"name": "김상우", "role": "원장"},  # duplicate
        ]
        added = _append_ocr_doctors(doctors, seen, result)
        assert added == 2
        assert len(result) == 2

    def test_preserves_education_career(self):
        seen = set()
        result = []
        _append_ocr_doctors([{
            "name": "김상우",
            "education": ["서울대학교 의학과"],
            "career": ["강남피부과 근무"],
            "credentials": ["대한피부과학회 정회원"],
        }], seen, result)
        assert result[0]["education"] == ["서울대학교 의학과"]
        assert result[0]["career"] == ["강남피부과 근무"]
        assert result[0]["credentials"] == ["대한피부과학회 정회원"]
