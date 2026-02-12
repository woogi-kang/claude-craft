"""Tests for constants and pattern integrity."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.constants import (
    DOCTOR_PRIMARY,
    DOCTOR_ROLES_EXCLUDE,
    DOCTOR_ROLES_KEEP,
    DOCTOR_SECONDARY,
    DOCTOR_SUBMENU_PARENTS,
    KOREAN_SURNAMES,
    PHONE_RE,
    PLATFORM_PATTERNS,
    ROLE_RE,
    TRACKING_PARAMS,
)
from storage_manager import VALID_PLATFORMS, VALID_STATUSES


class TestPlatformPatterns:
    def test_all_patterns_compile(self):
        for platform, patterns in PLATFORM_PATTERNS.items():
            for pat in patterns:
                compiled = re.compile(pat)
                assert compiled is not None, f"Failed to compile pattern for {platform}: {pat}"

    def test_expected_platforms_present(self):
        expected = {"KakaoTalk", "NaverTalk", "Instagram", "YouTube", "Facebook", "Line", "WhatsApp"}
        for p in expected:
            assert p in PLATFORM_PATTERNS, f"Missing platform: {p}"

    def test_no_empty_patterns(self):
        for platform, patterns in PLATFORM_PATTERNS.items():
            assert len(patterns) > 0, f"Empty patterns for {platform}"


class TestPhoneRegex:
    def test_matches_korean_landline(self):
        assert PHONE_RE.search("02-1234-5678")

    def test_matches_korean_mobile(self):
        assert PHONE_RE.search("010-1234-5678")

    def test_matches_international(self):
        assert PHONE_RE.search("+82-10-1234-5678")

    def test_matches_no_separator(self):
        assert PHONE_RE.search("01012345678")

    def test_no_match_short(self):
        assert PHONE_RE.search("010-123") is None


class TestTrackingParams:
    def test_contains_utm(self):
        for p in ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"]:
            assert p in TRACKING_PARAMS

    def test_contains_fbclid(self):
        assert "fbclid" in TRACKING_PARAMS

    def test_contains_gclid(self):
        assert "gclid" in TRACKING_PARAMS


class TestDoctorLabels:
    def test_primary_not_empty(self):
        assert len(DOCTOR_PRIMARY) > 0

    def test_secondary_not_empty(self):
        assert len(DOCTOR_SECONDARY) > 0

    def test_submenu_parents_not_empty(self):
        assert len(DOCTOR_SUBMENU_PARENTS) > 0

    def test_no_duplicates_in_primary(self):
        assert len(DOCTOR_PRIMARY) == len(set(DOCTOR_PRIMARY))

    def test_korean_labels_in_primary(self):
        assert "의료진" in DOCTOR_PRIMARY
        assert "원장 소개" in DOCTOR_PRIMARY


class TestDoctorRoles:
    def test_keep_contains_expected(self):
        for role in ["원장", "대표원장", "전문의", "의사"]:
            assert role in DOCTOR_ROLES_KEEP

    def test_exclude_contains_expected(self):
        for role in ["간호사", "상담사", "코디네이터"]:
            assert role in DOCTOR_ROLES_EXCLUDE

    def test_no_overlap(self):
        assert DOCTOR_ROLES_KEEP.isdisjoint(DOCTOR_ROLES_EXCLUDE)


class TestKoreanSurnames:
    def test_common_surnames_present(self):
        for s in "김이박최정강조윤장임":
            assert s in KOREAN_SURNAMES, f"Missing surname: {s}"

    def test_is_set_type(self):
        assert isinstance(KOREAN_SURNAMES, set)


class TestRoleRegex:
    def test_matches_name_role(self):
        m = ROLE_RE.match("박미래 원장")
        assert m is not None
        assert m.group(1) == "박미래"
        assert m.group(2) == "원장"

    def test_matches_name_전문의(self):
        m = ROLE_RE.match("김상우 전문의")
        assert m is not None
        assert m.group(2) == "전문의"

    def test_no_match_without_role(self):
        assert ROLE_RE.match("김상우") is None


class TestValidPlatforms:
    def test_contains_major_platforms(self):
        for p in ["KakaoTalk", "NaverTalk", "Instagram", "Phone"]:
            assert p in VALID_PLATFORMS


class TestValidStatuses:
    def test_contains_expected_statuses(self):
        for s in ["success", "partial", "failed", "archived", "requires_manual"]:
            assert s in VALID_STATUSES
