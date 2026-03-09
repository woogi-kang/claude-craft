"""Tests for clinic_crawler.llm_verifier: _parse_verification, verify_doctors_with_llm."""

import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.llm_verifier import _parse_verification, verify_doctors_with_llm


# ===========================================================================
# _parse_verification
# ===========================================================================

class TestParseVerificationMarkdownFence:
    def test_markdown_fence(self):
        text = '```json\n[{"name": "김상우", "is_valid": true, "reason": "doctor"}]\n```'
        result = _parse_verification(text)
        assert len(result) == 1
        assert result[0]["name"] == "김상우"
        assert result[0]["is_valid"] is True


class TestParseVerificationRawJsonArray:
    def test_raw_json_array(self):
        text = '[{"name": "김상우", "is_valid": true, "reason": "doctor"}]'
        result = _parse_verification(text)
        assert len(result) == 1
        assert result[0]["name"] == "김상우"


class TestParseVerificationIndividualObjects:
    def test_individual_objects(self):
        text = (
            'Here are the results:\n'
            '{"name": "김상우", "is_valid": true, "reason": "doctor"}\n'
            '{"name": "이지연", "is_valid": false, "reason": "nav text"}\n'
        )
        result = _parse_verification(text)
        assert len(result) == 2
        names = {r["name"] for r in result}
        assert "김상우" in names
        assert "이지연" in names


class TestParseVerificationEmptyString:
    def test_empty_string(self):
        assert _parse_verification("") == []


class TestParseVerificationMalformedJson:
    def test_malformed_json(self):
        assert _parse_verification("this is not json at all {{{") == []


# ===========================================================================
# verify_doctors_with_llm
# ===========================================================================

class TestVerifyEmptyCandidates:
    def test_empty_candidates(self):
        result = verify_doctors_with_llm([], "/some/screenshot.png", "123")
        assert result == []


class TestVerifyNoScreenshot:
    def test_no_screenshot_returns_all(self):
        candidates = [
            {"name": "김상우", "role": "원장"},
            {"name": "이지연", "role": "부원장"},
        ]
        result = verify_doctors_with_llm(candidates, None, "123")
        assert result == candidates


class TestVerifyScreenshotNotExists:
    def test_screenshot_not_exists_returns_all(self):
        candidates = [
            {"name": "김상우", "role": "원장"},
        ]
        result = verify_doctors_with_llm(candidates, "/nonexistent/path.png", "123")
        assert result == candidates


class TestVerifySuccessfulRejection:
    def test_successful_rejection(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [
            {"name": "김상우", "role": "원장"},
            {"name": "전체", "role": ""},
        ]
        llm_output = json.dumps([
            {"name": "김상우", "is_valid": True, "reason": "real doctor"},
            {"name": "전체", "is_valid": False, "reason": "UI label"},
        ])

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = llm_output
        mock_result.stderr = ""

        with patch("clinic_crawler.llm_verifier.subprocess.run", return_value=mock_result):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        assert len(filtered) == 1
        assert filtered[0]["name"] == "김상우"


class TestVerifyUnmentionedKept:
    def test_unmentioned_kept(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [
            {"name": "김상우", "role": "원장"},
            {"name": "이지연", "role": "부원장"},
            {"name": "박서준", "role": "전문의"},
        ]
        # LLM only mentions two of three candidates
        llm_output = json.dumps([
            {"name": "김상우", "is_valid": True, "reason": "real doctor"},
            {"name": "이지연", "is_valid": True, "reason": "real doctor"},
        ])

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = llm_output
        mock_result.stderr = ""

        with patch("clinic_crawler.llm_verifier.subprocess.run", return_value=mock_result):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        # All three should be kept (unmentioned candidates are kept conservatively)
        assert len(filtered) == 3
        names = {d["name"] for d in filtered}
        assert "박서준" in names


class TestVerifyCodexError:
    def test_codex_error_returns_all(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [
            {"name": "김상우", "role": "원장"},
        ]

        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error occurred"

        with patch("clinic_crawler.llm_verifier.subprocess.run", return_value=mock_result):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        assert filtered == candidates


class TestVerifyParseFailed:
    def test_parse_failed_returns_all(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [{"name": "김상우", "role": "원장"}]

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "no json here at all"
        mock_result.stderr = ""

        with patch("clinic_crawler.llm_verifier.subprocess.run", return_value=mock_result):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        assert filtered == candidates


class TestVerifyGenericException:
    def test_generic_exception_returns_all(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [{"name": "김상우", "role": "원장"}]

        with patch(
            "clinic_crawler.llm_verifier.subprocess.run",
            side_effect=RuntimeError("unexpected"),
        ):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        assert filtered == candidates


class TestVerifyTimeout:
    def test_timeout_returns_all(self, tmp_path):
        screenshot = tmp_path / "page.png"
        screenshot.write_bytes(b"fake png data")

        candidates = [
            {"name": "김상우", "role": "원장"},
            {"name": "이지연", "role": "부원장"},
        ]

        with patch(
            "clinic_crawler.llm_verifier.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="codex", timeout=120),
        ):
            filtered = verify_doctors_with_llm(candidates, str(screenshot), "123")

        assert filtered == candidates
