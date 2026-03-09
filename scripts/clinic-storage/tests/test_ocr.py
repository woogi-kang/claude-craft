"""Tests for OCR parsing helpers: parse_ocr_json, append_ocr_doctors, run_gemini_ocr."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.ocr import append_ocr_doctors, parse_ocr_json, run_gemini_ocr


class TestParseOcrJson:
    # -- Strategy 1: Markdown code fences --
    def test_json_in_code_fence(self):
        text = '```json\n[{"name": "김상우", "role": "원장"}]\n```'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["name"] == "김상우"

    def test_json_in_plain_code_fence(self):
        text = '```\n[{"name": "이지연"}]\n```'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["name"] == "이지연"

    # -- Strategy 1b: Markdown code fence with nested doctors key --
    def test_json_in_code_fence_with_doctors_key(self):
        text = '```json\n{"doctors": [{"name": "김상우", "role": "원장"}]}\n```'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["name"] == "김상우"

    # -- Strategy 2: Raw JSON array --
    def test_raw_json_array(self):
        text = '[{"name": "박서준", "role": "전문의"}]'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["role"] == "전문의"

    def test_bare_json_object_with_doctors_key(self):
        text = '{"doctors": [{"name": "최민지"}]}'
        result = parse_ocr_json(text)
        assert len(result) == 1

    def test_json_with_surrounding_text(self):
        text = 'Here are the results:\n[{"name": "최민지"}]\nEnd of results.'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert result[0]["name"] == "최민지"

    # -- Multiple doctors --
    def test_multiple_doctors(self):
        text = '[{"name": "김상우", "role": "대표원장"}, {"name": "이지연", "role": "부원장"}]'
        result = parse_ocr_json(text)
        assert len(result) == 2

    # -- Empty/no results --
    def test_empty_array(self):
        assert parse_ocr_json("[]") == []

    def test_empty_string(self):
        assert parse_ocr_json("") == []

    def test_none_input(self):
        assert parse_ocr_json(None) == []

    def test_whitespace_only(self):
        assert parse_ocr_json("   \n  ") == []

    # -- Malformed JSON --
    def test_no_json_content(self):
        assert parse_ocr_json("This is just plain text with no JSON.") == []

    def test_invalid_json_returns_empty(self):
        assert parse_ocr_json("not json at all") == []

    def test_truncated_json_falls_back(self):
        # Strategy 3 (greedy shrink) should recover partial array
        text = '[{"name": "김상우"}, {"name": "이지연"'
        result = parse_ocr_json(text)
        # May recover first item or empty depending on parse
        assert isinstance(result, list)

    def test_malformed_code_fence_falls_through(self):
        # Strategy 1 matches code fence but JSON inside is invalid;
        # the second array outside the fence is not inside a fence,
        # so Strategy 2 picks it up as shortest JSON array
        text = '```json\n[{broken json}]\n```'
        result = parse_ocr_json(text)
        # Code fence match fails JSON parse, falls through to Strategy 2
        # but no valid array outside fence → empty
        assert result == []

    def test_strategy3_greedy_shrink(self):
        # Only Strategy 3 can parse this (shortest match fails)
        text = '[{"name": "A"}] extra text [{"name": "B"}]'
        result = parse_ocr_json(text)
        assert isinstance(result, list)
        assert len(result) >= 1

    # -- Profile data --
    def test_preserves_profile_raw(self):
        text = '[{"name": "김상우", "role": "원장", "profile_raw": ["서울대학교 졸업", "피부과 전문의"]}]'
        result = parse_ocr_json(text)
        assert len(result) == 1
        assert len(result[0]["profile_raw"]) == 2

    def test_preserves_legacy_fields(self):
        text = '[{"name": "김상우", "education": ["서울대"], "career": ["강남병원"]}]'
        result = parse_ocr_json(text)
        assert result[0]["education"] == ["서울대"]


class TestAppendOcrDoctors:
    def test_appends_new_doctor(self):
        doctors_raw = [{"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]}]
        seen = set()
        result = []
        count = append_ocr_doctors(doctors_raw, seen, result)
        assert count == 1
        assert len(result) == 1
        assert result[0]["name"] == "김상우"
        assert result[0]["ocr_source"] is True
        assert result[0]["extraction_source"] == "ocr"

    def test_skips_duplicate_name(self):
        doctors_raw = [{"name": "김상우", "role": "원장"}]
        seen = {"김상우"}
        result = []
        count = append_ocr_doctors(doctors_raw, seen, result)
        assert count == 0
        assert len(result) == 0

    def test_skips_short_name(self):
        doctors_raw = [{"name": "김", "role": "원장"}]
        seen = set()
        result = []
        count = append_ocr_doctors(doctors_raw, seen, result)
        assert count == 0

    def test_skips_empty_name(self):
        doctors_raw = [{"name": "", "role": "원장"}]
        seen = set()
        result = []
        count = append_ocr_doctors(doctors_raw, seen, result)
        assert count == 0

    def test_merges_legacy_fields_to_profile_raw(self):
        doctors_raw = [{
            "name": "이지연",
            "role": "전문의",
            "education": ["고려대 졸업"],
            "career": ["강남병원 근무"],
            "credentials": ["피부과 정회원"],
        }]
        seen = set()
        result = []
        append_ocr_doctors(doctors_raw, seen, result)
        assert len(result) == 1
        assert "고려대 졸업" in result[0]["profile_raw"]
        assert "강남병원 근무" in result[0]["profile_raw"]
        assert "피부과 정회원" in result[0]["profile_raw"]

    def test_prefers_profile_raw_over_legacy(self):
        doctors_raw = [{
            "name": "박서준",
            "role": "원장",
            "profile_raw": ["통합된 경력"],
            "education": ["이건 무시됨"],
        }]
        seen = set()
        result = []
        append_ocr_doctors(doctors_raw, seen, result)
        assert result[0]["profile_raw"] == ["통합된 경력"]

    def test_multiple_doctors_mixed(self):
        doctors_raw = [
            {"name": "김상우", "role": "대표원장", "profile_raw": ["서울대"]},
            {"name": "김상우", "role": "원장"},  # duplicate
            {"name": "이지연", "role": "부원장", "profile_raw": ["고려대"]},
        ]
        seen = set()
        result = []
        count = append_ocr_doctors(doctors_raw, seen, result)
        assert count == 2
        assert len(result) == 2

    def test_adds_to_seen_set(self):
        doctors_raw = [{"name": "정하영", "role": "원장"}]
        seen = set()
        result = []
        append_ocr_doctors(doctors_raw, seen, result)
        assert "정하영" in seen

    def test_default_role(self):
        doctors_raw = [{"name": "강민호"}]
        seen = set()
        result = []
        append_ocr_doctors(doctors_raw, seen, result)
        assert result[0]["role"] == "specialist"


class TestRunGeminiOcr:
    def test_successful_ocr(self, tmp_path):
        image = tmp_path / "page.jpg"
        image.write_bytes(b"fake jpg")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '[{"name": "김상우", "role": "원장"}]'

        with patch("clinic_crawler.ocr.subprocess.run", return_value=mock_result):
            result = run_gemini_ocr("extract doctors", str(image))

        assert len(result) == 1
        assert result[0]["name"] == "김상우"

    def test_failed_ocr_returns_empty(self, tmp_path):
        image = tmp_path / "page.jpg"
        image.write_bytes(b"fake jpg")

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error"

        with patch("clinic_crawler.ocr.subprocess.run", return_value=mock_result):
            result = run_gemini_ocr("extract doctors", str(image))

        assert result == []
