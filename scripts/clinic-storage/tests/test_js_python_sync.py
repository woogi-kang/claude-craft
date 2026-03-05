"""Tests to verify JS and Python name-validation constants stay in sync."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from clinic_crawler.constants import (
    KOREAN_SURNAMES,
    NON_NAME_GIVEN,
    NON_NAME_WORDS,
    ROLE_EXTRACT_STR,
    ROLE_PATTERN_STR,
)
from clinic_crawler.js_snippets import JS_EXTRACT_DOCTORS


class TestJsPythonSync:
    def test_surnames_present_in_js(self):
        for ch in KOREAN_SURNAMES:
            assert ch in JS_EXTRACT_DOCTORS, f"Surname '{ch}' missing from JS"

    def test_non_name_words_present_in_js(self):
        for word in NON_NAME_WORDS:
            assert word in JS_EXTRACT_DOCTORS, f"NON_NAME_WORDS '{word}' missing from JS"

    def test_non_name_given_present_in_js(self):
        for word in NON_NAME_GIVEN:
            assert word in JS_EXTRACT_DOCTORS, f"NON_NAME_GIVEN '{word}' missing from JS"

    def test_role_pattern_in_js(self):
        assert ROLE_PATTERN_STR in JS_EXTRACT_DOCTORS

    def test_role_extract_in_js(self):
        assert ROLE_EXTRACT_STR in JS_EXTRACT_DOCTORS

    def test_no_unresolved_placeholders(self):
        assert "{{" not in JS_EXTRACT_DOCTORS
        assert "}}" not in JS_EXTRACT_DOCTORS

    def test_compound_roles_in_role_pattern(self):
        for role in ["수석원장", "교육원장", "진료원장", "총괄원장", "지도전문의"]:
            assert role in ROLE_PATTERN_STR, f"Compound role '{role}' missing from ROLE_PATTERN_STR"

    def test_role_extract_subset_of_pattern(self):
        extract_roles = set(ROLE_EXTRACT_STR.split("|"))
        pattern_roles = set(ROLE_PATTERN_STR.split("|"))
        assert extract_roles <= pattern_roles, (
            f"ROLE_EXTRACT has roles not in ROLE_PATTERN: {extract_roles - pattern_roles}"
        )
