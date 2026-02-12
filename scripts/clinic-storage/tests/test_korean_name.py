"""Tests for Korean name validation: _is_plausible_korean_name."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.korean_name import is_plausible_korean_name as _is_plausible_korean_name


class TestIsPlausibleKoreanName:
    # -- Valid names --
    def test_two_char_name(self):
        assert _is_plausible_korean_name("김솔") is True

    def test_three_char_name(self):
        assert _is_plausible_korean_name("박미래") is True

    def test_four_char_name(self):
        assert _is_plausible_korean_name("김나라별") is True

    def test_common_name_kim(self):
        assert _is_plausible_korean_name("김상우") is True

    def test_common_name_lee(self):
        assert _is_plausible_korean_name("이지연") is True

    def test_common_name_park(self):
        assert _is_plausible_korean_name("박서준") is True

    def test_common_name_choi(self):
        assert _is_plausible_korean_name("최민지") is True

    def test_surname_jung(self):
        assert _is_plausible_korean_name("정하영") is True

    def test_surname_kang(self):
        assert _is_plausible_korean_name("강민호") is True

    # -- Invalid: length --
    def test_single_char_rejected(self):
        assert _is_plausible_korean_name("김") is False

    def test_five_char_rejected(self):
        assert _is_plausible_korean_name("김나라별하") is False

    def test_empty_string_rejected(self):
        assert _is_plausible_korean_name("") is False

    # -- Invalid: non-Korean characters --
    def test_english_rejected(self):
        assert _is_plausible_korean_name("Kim") is False

    def test_mixed_korean_english(self):
        assert _is_plausible_korean_name("김A호") is False

    def test_numbers_rejected(self):
        assert _is_plausible_korean_name("김1호") is False

    def test_jamo_rejected(self):
        # Jamo (incomplete syllables like ㅎ) should fail the 가-힣 range check
        assert _is_plausible_korean_name("김ㅎ호") is False

    # -- Invalid: unknown surname --
    def test_unknown_surname_rejected(self):
        # 빈 is not a common Korean surname
        assert _is_plausible_korean_name("빈서준") is False

    # -- Invalid: non-name patterns --
    def test_non_name_word_대표원(self):
        assert _is_plausible_korean_name("대표원") is False

    def test_non_name_word_원대표(self):
        assert _is_plausible_korean_name("원대표") is False

    def test_non_name_word_부대표(self):
        assert _is_plausible_korean_name("부대표") is False

    def test_non_name_word_병원장(self):
        assert _is_plausible_korean_name("병원장") is False

    # -- Invalid: verb/adjective suffixes --
    def test_suffix_있는(self):
        assert _is_plausible_korean_name("김있는") is False

    def test_suffix_없는(self):
        assert _is_plausible_korean_name("이없는") is False

    def test_suffix_하는(self):
        assert _is_plausible_korean_name("박하는") is False

    # -- Invalid: title/role given names --
    def test_given_대표(self):
        assert _is_plausible_korean_name("정대표") is False

    def test_given_원장(self):
        assert _is_plausible_korean_name("김원장") is False

    def test_given_소개(self):
        assert _is_plausible_korean_name("박소개") is False

    def test_given_안내(self):
        assert _is_plausible_korean_name("이안내") is False

    # -- None input --
    def test_none_rejected(self):
        assert _is_plausible_korean_name(None) is False
