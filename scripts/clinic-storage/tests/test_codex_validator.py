"""Tests for clinic_crawler.codex_validator: validate_doctors via Codex CLI."""

import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.codex_validator import validate_doctors


class TestEmptyInput:
    def test_empty_input_returns_empty(self):
        result, any_valid = validate_doctors([], "123")
        assert result == []
        assert any_valid is False


class TestAllEmptyProfileRaw:
    def test_all_empty_profile_raw_skips_codex(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": []},
            {"name": "이지연", "role": "부원장", "profile_raw": []},
        ]
        with patch("clinic_crawler.codex_validator.subprocess.run") as mock_run:
            result, any_valid = validate_doctors(doctors, "123")
            mock_run.assert_not_called()
        assert result == doctors
        assert any_valid is False


class TestSuccessfulValidation:
    def test_successful_validation(self, tmp_path):
        doctors = [
            {"name": "김상우", "role": "대표원장", "profile_raw": ["서울대 졸업", "피부과 전문의"]},
            {"name": "이지연", "role": "부원장", "profile_raw": ["고려대 졸업"]},
        ]
        codex_output = [
            {"name": "김상우", "valid_items": ["서울대 졸업", "피부과 전문의"], "is_valid": True},
            {"name": "이지연", "valid_items": [], "is_valid": False},
        ]

        def fake_run(cmd, **kwargs):
            # Write codex output file
            # Find the output path from the prompt text
            prompt = cmd[-1]
            # Extract output_path from prompt
            for line in prompt.split("\n"):
                if "codex_out_" in line:
                    # Parse the output path
                    import re
                    m = re.search(r"(/tmp/codex_out_\S+\.json)", line)
                    if m:
                        out_path = m.group(1)
                        with open(out_path, "w") as f:
                            json.dump(codex_output, f)
                        break
            else:
                # Fallback: find the input path and derive output path
                for line2 in prompt.split("\n"):
                    import re
                    m = re.search(r"(/tmp/codex_in_\S+\.json)", line2)
                    if m:
                        out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                        with open(out_path, "w") as f:
                            json.dump(codex_output, f)
                        break

            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            mock_result.stdout = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            filtered, any_valid = validate_doctors(doctors, "test_place")

        assert any_valid is True
        # Kim should be kept (is_valid=True), Lee rejected but recovered
        # (valid Korean name + medical role)
        valid_names = {d["name"] for d in filtered}
        assert "김상우" in valid_names


class TestNameBasedFallback:
    def test_name_based_fallback_on_length_mismatch(self, tmp_path):
        doctors = [
            {"name": "김상우", "role": "대표원장", "profile_raw": ["서울대 졸업"]},
            {"name": "이지연", "role": "부원장", "profile_raw": ["고려대 졸업"]},
            {"name": "박서준", "role": "전문의", "profile_raw": ["연세대 졸업"]},
        ]
        # Codex returns fewer items than input (length mismatch)
        codex_output = [
            {"name": "김상우", "valid_items": ["서울대 졸업"], "is_valid": True},
            {"name": "박서준", "valid_items": ["연세대 졸업"], "is_valid": True},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump(codex_output, f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            filtered, any_valid = validate_doctors(doctors, "test_place")

        assert any_valid is True
        names = {d["name"] for d in filtered}
        assert "김상우" in names
        assert "박서준" in names


class TestRecoveryOfValidKoreanName:
    def test_recovery_of_valid_korean_name_rejected(self, tmp_path):
        doctors = [
            {"name": "정진이", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        codex_output = [
            {"name": "정진이", "valid_items": [], "is_valid": False},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump(codex_output, f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            filtered, any_valid = validate_doctors(doctors, "test_place")

        # Should be recovered: valid Korean name + medical role (원장)
        assert any_valid is True
        assert len(filtered) == 1
        assert filtered[0]["name"] == "정진이"
        # profile_raw should be emptied on recovery
        assert filtered[0]["profile_raw"] == []


class TestTimeoutReturnsEmpty:
    def test_timeout_returns_empty(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        with patch(
            "clinic_crawler.codex_validator.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="codex", timeout=120),
        ):
            result, any_valid = validate_doctors(doctors, "123")
        assert result == []
        assert any_valid is False


class TestErrorReturncodeReturnsEmpty:
    def test_error_returncode_returns_empty(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Some error"
        with patch("clinic_crawler.codex_validator.subprocess.run", return_value=mock_result):
            result, any_valid = validate_doctors(doctors, "123")
        assert result == []
        assert any_valid is False


class TestOutputFileNotFound:
    def test_output_file_not_found(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""
        # Do not create the output file, so it won't be found
        with patch("clinic_crawler.codex_validator.subprocess.run", return_value=mock_result):
            result, any_valid = validate_doctors(doctors, "123")
        assert result == []
        assert any_valid is False


class TestNonListJson:
    def test_non_list_json(self, tmp_path):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump({"error": "not a list"}, f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            result, any_valid = validate_doctors(doctors, "123")
        assert result == []
        assert any_valid is False


class TestBranchPropagated:
    def test_branch_propagated(self, tmp_path):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"], "branch": ""},
        ]
        codex_output = [
            {"name": "김상우", "valid_items": ["서울대 졸업"], "is_valid": True, "branch": "강남점"},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump(codex_output, f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            filtered, any_valid = validate_doctors(doctors, "test_place")

        assert any_valid is True
        assert filtered[0]["branch"] == "강남점"


class TestGenericException:
    def test_generic_exception_returns_empty(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        with patch(
            "clinic_crawler.codex_validator.subprocess.run",
            side_effect=RuntimeError("unexpected error"),
        ):
            result, any_valid = validate_doctors(doctors, "123")
        assert result == []
        assert any_valid is False


class TestKeepDebugFiles:
    def test_keep_debug_files_when_env_set(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump([{"name": "김상우", "valid_items": [], "is_valid": True}], f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch.dict(os.environ, {"CLINIC_CODEX_KEEP_DEBUG": "1"}):
            with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
                validate_doctors(doctors, "debug_test")

        # Debug files should exist
        debug_in = Path("/tmp/codex_debug_in_debug_test.json")
        debug_out = Path("/tmp/codex_debug_out_debug_test.json")
        try:
            assert debug_in.exists() or debug_out.exists()
        finally:
            debug_in.unlink(missing_ok=True)
            debug_out.unlink(missing_ok=True)


class TestNameBasedFallbackWithBranch:
    def test_branch_in_name_based_fallback(self, tmp_path):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        # Return 2 items for 1 doctor (length mismatch) → name-based lookup
        codex_output = [
            {"name": "김상우", "valid_items": ["서울대 졸업"], "is_valid": True, "branch": "강남점"},
            {"name": "extra", "valid_items": [], "is_valid": False},
        ]

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                with open(out_path, "w") as f:
                    json.dump(codex_output, f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
            filtered, any_valid = validate_doctors(doctors, "test_place")

        assert any_valid is True
        assert filtered[0]["branch"] == "강남점"


class TestTempFilesCleaned:
    def test_temp_files_cleaned_in_production(self):
        doctors = [
            {"name": "김상우", "role": "원장", "profile_raw": ["서울대 졸업"]},
        ]
        created_files = []

        def fake_run(cmd, **kwargs):
            prompt = cmd[-1]
            import re
            m = re.search(r"(/tmp/codex_in_\S+\.json)", prompt)
            if m:
                created_files.append(m.group(1))
                out_path = m.group(1).replace("codex_in_", "codex_out_", 1)
                created_files.append(out_path)
                with open(out_path, "w") as f:
                    json.dump([{"name": "김상우", "valid_items": [], "is_valid": True}], f)
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stderr = ""
            return mock_result

        # Ensure CLINIC_CODEX_KEEP_DEBUG is not set
        env = os.environ.copy()
        env.pop("CLINIC_CODEX_KEEP_DEBUG", None)
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("CLINIC_CODEX_KEEP_DEBUG", None)
            with patch("clinic_crawler.codex_validator.subprocess.run", side_effect=fake_run):
                validate_doctors(doctors, "cleanup_test")

        # After call, temp files should be cleaned up
        for fp in created_files:
            assert not Path(fp).exists(), f"Temp file should be cleaned: {fp}"
