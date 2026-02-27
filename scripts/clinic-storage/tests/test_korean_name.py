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

    # -- Invalid: location names misidentified as person names --
    def test_location_홍대(self):
        assert _is_plausible_korean_name("홍대") is False

    def test_location_노원(self):
        assert _is_plausible_korean_name("노원") is False

    def test_location_성수(self):
        assert _is_plausible_korean_name("성수") is False

    def test_location_원노원(self):
        assert _is_plausible_korean_name("원노원") is False

    # -- Invalid: OCR/text noise --
    def test_noise_마취통(self):
        assert _is_plausible_korean_name("마취통") is False

    def test_noise_장없이(self):
        assert _is_plausible_korean_name("장없이") is False

    # -- Valid: real names that look like locations --
    def test_valid_name_성수진(self):
        assert _is_plausible_korean_name("성수진") is True

    def test_valid_name_홍대영(self):
        assert _is_plausible_korean_name("홍대영") is True

    # -- Round 2: compound role fragments as given names --
    def test_given_수석(self):
        assert _is_plausible_korean_name("원수석") is False

    def test_given_교육(self):
        assert _is_plausible_korean_name("원교육") is False

    def test_given_미국(self):
        assert _is_plausible_korean_name("원미국") is False

    def test_given_진료(self):
        assert _is_plausible_korean_name("장진료") is False

    def test_given_총괄(self):
        assert _is_plausible_korean_name("김총괄") is False

    def test_given_연구(self):
        assert _is_plausible_korean_name("이연구") is False

    def test_given_센터(self):
        assert _is_plausible_korean_name("박센터") is False

    # -- Round 2: marketing/brand/location false positives --
    def test_noise_오랜(self):
        assert _is_plausible_korean_name("오랜") is False

    def test_noise_성장한(self):
        assert _is_plausible_korean_name("성장한") is False

    def test_noise_유픽(self):
        assert _is_plausible_korean_name("유픽") is False

    def test_location_서초(self):
        assert _is_plausible_korean_name("서초") is False

    def test_noise_지도(self):
        assert _is_plausible_korean_name("지도") is False

    # -- Round 2: adjective suffix --
    def test_suffix_적은(self):
        assert _is_plausible_korean_name("이적은") is False

    # -- Round 3: verb forms, nouns, UI labels, honorifics --
    def test_verb_주시면(self):
        assert _is_plausible_korean_name("주시면") is False

    def test_noun_신뢰(self):
        assert _is_plausible_korean_name("신뢰") is False

    def test_label_전체(self):
        assert _is_plausible_korean_name("전체") is False

    def test_label_구분(self):
        assert _is_plausible_korean_name("구분") is False

    def test_adverb_오직(self):
        assert _is_plausible_korean_name("오직") is False

    def test_honorific_고객님(self):
        assert _is_plausible_korean_name("고객님") is False

    def test_career_원신사(self):
        assert _is_plausible_korean_name("원신사") is False

    def test_career_원부(self):
        assert _is_plausible_korean_name("원부") is False

    def test_hospital_강북삼(self):
        assert _is_plausible_korean_name("강북삼") is False

    def test_brand_연세청(self):
        assert _is_plausible_korean_name("연세청") is False

    def test_location_신사(self):
        assert _is_plausible_korean_name("신사") is False

    def test_noise_구주(self):
        assert _is_plausible_korean_name("구주") is False

    def test_noise_지여(self):
        assert _is_plausible_korean_name("지여") is False

    # -- Round 3: given-name blocklist for location names --
    def test_given_서초(self):
        assert _is_plausible_korean_name("원서초") is False

    def test_given_신사(self):
        assert _is_plausible_korean_name("장신사") is False

    # -- None input --
    def test_none_rejected(self):
        assert _is_plausible_korean_name(None) is False
