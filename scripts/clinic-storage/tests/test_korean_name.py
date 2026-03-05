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
        # 럭 is not a Korean surname
        assert _is_plausible_korean_name("럭서준") is False

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

    # -- Substring blocklist (ported from JS) --
    def test_substring_병원(self):
        assert _is_plausible_korean_name("김병원") is False

    def test_substring_클리닉(self):
        assert _is_plausible_korean_name("김클리닉") is False

    def test_substring_의원(self):
        assert _is_plausible_korean_name("김의원") is False

    def test_substring_피부(self):
        assert _is_plausible_korean_name("김피부") is False

    def test_substring_필러(self):
        assert _is_plausible_korean_name("마필러") is False

    # -- Truncated word endings (ported from JS) --
    def test_truncated_의(self):
        # "경희의" from "경희의료원"
        assert _is_plausible_korean_name("경희의") is False

    def test_truncated_대(self):
        # "연세대" from "연세대학교"
        assert _is_plausible_korean_name("연세대") is False

    def test_truncated_과(self):
        assert _is_plausible_korean_name("김외과") is False

    # -- Role prefix (ported from JS) --
    def test_role_prefix_원장(self):
        assert _is_plausible_korean_name("원장유") is False

    def test_role_prefix_전문(self):
        assert _is_plausible_korean_name("전문김") is False

    # -- Valid names not caught by new rules --
    def test_valid_name_김서연(self):
        assert _is_plausible_korean_name("김서연") is True

    def test_valid_name_이하은(self):
        assert _is_plausible_korean_name("이하은") is True

    # -- Round 4: common words misidentified as names --
    def test_word_이력(self):
        assert _is_plausible_korean_name("이력") is False

    def test_word_이송(self):
        assert _is_plausible_korean_name("이송") is False

    def test_word_한국(self):
        assert _is_plausible_korean_name("한국") is False

    def test_word_공동(self):
        assert _is_plausible_korean_name("공동") is False

    def test_word_위해(self):
        assert _is_plausible_korean_name("위해") is False

    def test_word_전국(self):
        assert _is_plausible_korean_name("전국") is False

    def test_word_방문(self):
        assert _is_plausible_korean_name("방문") is False

    def test_word_한문(self):
        assert _is_plausible_korean_name("한문") is False

    def test_word_전임(self):
        assert _is_plausible_korean_name("전임") is False

    def test_word_전에(self):
        assert _is_plausible_korean_name("전에") is False

    def test_word_오전(self):
        assert _is_plausible_korean_name("오전") is False

    def test_word_안심(self):
        assert _is_plausible_korean_name("안심") is False

    def test_word_민부(self):
        assert _is_plausible_korean_name("민부") is False

    def test_word_문여(self):
        assert _is_plausible_korean_name("문여") is False

    def test_word_한정(self):
        assert _is_plausible_korean_name("한정") is False

    def test_word_선정(self):
        assert _is_plausible_korean_name("선정") is False

    def test_country_한민국(self):
        assert _is_plausible_korean_name("한민국") is False

    def test_location_홍제(self):
        assert _is_plausible_korean_name("홍제") is False

    # -- Round 5: university/institution fragments --
    def test_institution_이화여자(self):
        assert _is_plausible_korean_name("이화여자") is False

    def test_institution_이화여(self):
        assert _is_plausible_korean_name("이화여") is False

    # -- Round 6: branch/district names --
    def test_location_공덕(self):
        assert _is_plausible_korean_name("공덕") is False

    def test_location_마포공덕(self):
        assert _is_plausible_korean_name("마포공덕") is False

    def test_location_마포공(self):
        assert _is_plausible_korean_name("마포공") is False

    # -- Round 10: location names, UI labels, truncated endings --
    def test_location_명동(self):
        assert _is_plausible_korean_name("명동") is False

    def test_location_여의도(self):
        assert _is_plausible_korean_name("여의도") is False

    def test_word_인사말(self):
        assert _is_plausible_korean_name("인사말") is False

    def test_word_고문(self):
        # 고문 = advisor/consultant (顧問), not a person name
        assert _is_plausible_korean_name("고문") is False

    def test_pronoun_제가(self):
        # 제가 = "I" (first person pronoun)
        assert _is_plausible_korean_name("제가") is False

    def test_word_경우(self):
        # 경우 = case/situation, not a person name
        assert _is_plausible_korean_name("경우") is False

    def test_brand_연세아인(self):
        # 연세아인 = clinic brand name
        assert _is_plausible_korean_name("연세아인") is False

    def test_brand_제너리스(self):
        # 제너리스 = clinic brand name (transliteration of "Generis")
        assert _is_plausible_korean_name("제너리스") is False

    def test_parse_artifact_임정민원(self):
        # 임정민원 = parsing artifact from "임정민 원장"
        assert _is_plausible_korean_name("임정민원") is False

    def test_word_인사글(self):
        # 인사글 = greeting message (section header)
        assert _is_plausible_korean_name("인사글") is False

    def test_word_국내(self):
        # 국내 = domestic/within the country
        assert _is_plausible_korean_name("국내") is False

    def test_marketing_안티에이(self):
        # 안티에이 = anti-aging marketing text
        assert _is_plausible_korean_name("안티에이") is False

    def test_fragment_정직함이(self):
        # 정직함이 = "honesty is..." sentence fragment
        assert _is_plausible_korean_name("정직함이") is False

    def test_honorific_한분한분(self):
        # 한분한분 = "each and every person"
        assert _is_plausible_korean_name("한분한분") is False

    def test_bio_주요약력(self):
        # 주요약력 = "main career history"
        assert _is_plausible_korean_name("주요약력") is False

    def test_substring_약력(self):
        # 약력 should be caught by substring blocklist
        assert _is_plausible_korean_name("김약력") is False

    def test_given_본원(self):
        # 본원 = "this clinic/main branch", not a given name
        assert _is_plausible_korean_name("남본원") is False

    def test_marketing_예약제로(self):
        # 예약제로 = "reservation zero" marketing text
        assert _is_plausible_korean_name("예약제로") is False

    def test_given_오직(self):
        # 기오직 = surname 기 + 오직 (word "only")
        assert _is_plausible_korean_name("기오직") is False

    def test_substring_복지(self):
        # 복지 = welfare, caught by substring blocklist
        assert _is_plausible_korean_name("제주복지") is False

    def test_medical_경부(self):
        # 경부 = neck (頸部), medical term
        assert _is_plausible_korean_name("경부") is False

    def test_brand_연세청아(self):
        # 연세청아 = clinic brand name (from 연세청아린의원)
        assert _is_plausible_korean_name("연세청아") is False

    def test_label_진료시간(self):
        # 진료시간 = "consultation hours" schedule label
        assert _is_plausible_korean_name("진료시간") is False

    def test_truncated_입_4char(self):
        # "서성훈입" from "서성훈입니다"
        assert _is_plausible_korean_name("서성훈입") is False

    def test_parse_artifact_김지영원(self):
        # 김지영원 = parsing artifact from "김지영 원장"
        assert _is_plausible_korean_name("김지영원") is False

    def test_parse_artifact_김윤미원(self):
        # 김윤미원 = parsing artifact from "김윤미 원장"
        assert _is_plausible_korean_name("김윤미원") is False

    def test_brand_모던스탠(self):
        # 모던스탠 = clinic brand fragment from "모던스탠다드의원"
        assert _is_plausible_korean_name("모던스탠") is False

    def test_legal_이용약관(self):
        # 이용약관 = "Terms of Use" legal text
        assert _is_plausible_korean_name("이용약관") is False

    def test_role_공동대표(self):
        # 공동대표 = "co-representative" role title
        assert _is_plausible_korean_name("공동대표") is False

    def test_military_공군사(self):
        # 공군사 = military text fragment from "공군사령부"
        assert _is_plausible_korean_name("공군사") is False

    def test_military_공군사령(self):
        # 공군사령 = "Air Force Command" military text
        assert _is_plausible_korean_name("공군사령") is False

    def test_brand_오아로피(self):
        # 오아로피 = clinic brand fragment from "오아로피부과"
        assert _is_plausible_korean_name("오아로피") is False

    def test_adjective_진정한(self):
        # 진정한 = "genuine/true" adjective
        assert _is_plausible_korean_name("진정한") is False

    def test_label_전후사진(self):
        # 전후사진 = "before/after photos" UI label
        assert _is_plausible_korean_name("전후사진") is False

    def test_word_전세계(self):
        # 전세계 = "worldwide" common word
        assert _is_plausible_korean_name("전세계") is False

    def test_word_명의(self):
        # 명의 = "famous doctor" noun
        assert _is_plausible_korean_name("명의") is False

    def test_verb_고픈(self):
        # 고픈 = "wanting to" verb ending
        assert _is_plausible_korean_name("고픈") is False

    def test_noise_은옥건(self):
        # 은옥건 = parsing artifact from clinic name "옥건"
        assert _is_plausible_korean_name("은옥건") is False

    def test_credential_주요경력(self):
        # 주요경력 = "main career history" credential header
        assert _is_plausible_korean_name("주요경력") is False

    def test_marketing_편한세상(self):
        # 편한세상 = "comfortable world" marketing text
        assert _is_plausible_korean_name("편한세상") is False

    def test_brand_옥건(self):
        # 옥건 = clinic brand name (옥건헤어라인의원)
        assert _is_plausible_korean_name("옥건") is False

    def test_procedure_모발이식(self):
        # 모발이식 = "hair transplant" medical procedure
        assert _is_plausible_korean_name("모발이식") is False

    def test_credential_주요약(self):
        # 주요약 = truncated from "주요약력" credential header
        assert _is_plausible_korean_name("주요약") is False

    def test_parse_artifact_강현이전(self):
        # 강현이전 = parsing artifact from "강현이 이전" (name + "before")
        assert _is_plausible_korean_name("강현이전") is False

    def test_institution_성균관(self):
        # 성균관 = Sungkyunkwan (university name)
        assert _is_plausible_korean_name("성균관") is False

    def test_parse_artifact_원이건(self):
        # 원이건 = parsing artifact from "원장 이건"
        assert _is_plausible_korean_name("원이건") is False

    def test_credential_공중보건(self):
        # 공중보건 = "public health" credential text
        assert _is_plausible_korean_name("공중보건") is False

    def test_treatment_여드름(self):
        # 여드름 = "acne" treatment category
        assert _is_plausible_korean_name("여드름") is False

    def test_treatment_제모(self):
        # 제모 = "hair removal" treatment category
        assert _is_plausible_korean_name("제모") is False

    def test_label_기타(self):
        # 기타 = "other" UI label
        assert _is_plausible_korean_name("기타") is False

    def test_word_제언(self):
        # 제언 = "proposal/suggestion" common word
        assert _is_plausible_korean_name("제언") is False

    def test_pronoun_어느(self):
        # 어느 = "which/some" pronoun/determiner
        assert _is_plausible_korean_name("어느") is False

    def test_credential_국립중앙(self):
        # 국립중앙 = "National Central" from credential text
        assert _is_plausible_korean_name("국립중앙") is False

    def test_branch_강남뮤즈(self):
        # 강남뮤즈 = "Gangnam Muse" branch name
        assert _is_plausible_korean_name("강남뮤즈") is False

    def test_location_이대목동(self):
        # 이대목동 = "Ewha Mokdong" hospital/location
        assert _is_plausible_korean_name("이대목동") is False

    def test_device_복합광(self):
        # 복합광 = "compound light" treatment device name
        assert _is_plausible_korean_name("복합광") is False

    def test_branch_명동쁨(self):
        # 명동쁨 = branch name fragment
        assert _is_plausible_korean_name("명동쁨") is False

    # -- Round 39: UI label --
    def test_label_진료상담(self):
        # 진료상담 = "treatment consultation" UI label
        assert _is_plausible_korean_name("진료상담") is False

    # -- Round 40: editorial committee, sentence fragment, suffix --
    def test_committee_편찬위(self):
        # 편찬위 = "editorial committee" (편찬위원회 truncated)
        assert _is_plausible_korean_name("편찬위") is False

    def test_fragment_진료보다(self):
        # 진료보다 = "more than treatment" sentence fragment
        assert _is_plausible_korean_name("진료보다") is False

    def test_suffix_보다(self):
        # 보다 = comparison particle; name[1:] = "보다" should be rejected
        assert _is_plausible_korean_name("김보다") is False

    def test_location_위례중앙(self):
        # 위례중앙 = "Wirye Central" location/station name
        assert _is_plausible_korean_name("위례중앙") is False

    # -- Round 43: text fragment --
    def test_fragment_인여(self):
        # 인여 = fragment from "1인여성" or "본인여부"
        assert _is_plausible_korean_name("인여") is False

    # -- Round 44: verb ending, district, fragment, parsing artifact --
    def test_verb_하는(self):
        # 하는 = verb ending "doing" (2-char edge case)
        assert _is_plausible_korean_name("하는") is False

    def test_district_강서구(self):
        # 강서구 = "Gangseo-gu" Seoul district name
        assert _is_plausible_korean_name("강서구") is False

    def test_fragment_진료로(self):
        # 진료로 = "to treatment" or "treatment road"
        assert _is_plausible_korean_name("진료로") is False

    def test_artifact_김병균원(self):
        # 김병균원 = parsing artifact (name+원 from "김병균 원장")
        assert _is_plausible_korean_name("김병균원") is False

    # -- Round 45: clinic brand --
    def test_brand_강남비비(self):
        # 강남비비 = clinic brand name "Gangnam BB"
        assert _is_plausible_korean_name("강남비비") is False

    def test_brand_남비비(self):
        # 남비비 = clinic brand fragment
        assert _is_plausible_korean_name("남비비") is False

    # -- Round 46: area fragment, connective ending, suffix --
    def test_fragment_위동네(self):
        # 위동네 = "upper neighborhood" area fragment
        assert _is_plausible_korean_name("위동네") is False

    def test_ending_하더라도(self):
        # 하더라도 = connective ending "even if"
        assert _is_plausible_korean_name("하더라도") is False

    def test_suffix_더라도(self):
        # 더라도 = connective suffix; name[1:] should be rejected
        assert _is_plausible_korean_name("김더라도") is False

    # -- Round 48: credential typo, district name --
    def test_credential_공증보건(self):
        # 공증보건 = typo of 공중보건 "public health"
        assert _is_plausible_korean_name("공증보건") is False

    def test_district_서초구(self):
        # 서초구 = "Seocho-gu" Seoul district name
        assert _is_plausible_korean_name("서초구") is False

    # -- Round 49: medical specialty, common word, adverb --
    def test_medical_이비인후(self):
        # 이비인후 = otolaryngology (ENT) medical specialty
        assert _is_plausible_korean_name("이비인후") is False

    def test_word_인도(self):
        # 인도 = "India" or "guidance"
        assert _is_plausible_korean_name("인도") is False

    def test_adverb_정확히(self):
        # 정확히 = "exactly/precisely" adverb
        assert _is_plausible_korean_name("정확히") is False

    # -- Round 50: treatment fragments, food fragment, parsing artifact --
    def test_fragment_모치료(self):
        # 모치료 = "hair treatment" fragment
        assert _is_plausible_korean_name("모치료") is False

    def test_fragment_모전문(self):
        # 모전문 = "hair specialist" fragment
        assert _is_plausible_korean_name("모전문") is False

    def test_fragment_방음식(self):
        # 방음식 = "soundproof food" or DOM fragment
        assert _is_plausible_korean_name("방음식") is False

    def test_artifact_허선영원(self):
        # 허선영원 = parsing artifact (name+원 from "허선영 원장")
        assert _is_plausible_korean_name("허선영원") is False

    # -- Round 51: role designation, location fragment --
    def test_fragment_정전담(self):
        # 정전담 = "designated" role fragment
        assert _is_plausible_korean_name("정전담") is False

    def test_fragment_원명동(self):
        # 원명동 = clinic + location "Myeongdong" fragment
        assert _is_plausible_korean_name("원명동") is False

    # -- Round 53: common word, time expression, location fragment --
    def test_word_소통(self):
        # 소통 = "communication" common word
        assert _is_plausible_korean_name("소통") is False

    def test_fragment_차마다(self):
        # 차마다 = "every car/time" expression
        assert _is_plausible_korean_name("차마다") is False

    def test_fragment_원신촌(self):
        # 원신촌 = clinic + "Sinchon" location fragment
        assert _is_plausible_korean_name("원신촌") is False

    # -- Round 54: common word (designated/appointed) --
    def test_word_지정(self):
        # 지정 = "designated/appointed" (指定), from "1대1 지정 원장제"
        assert _is_plausible_korean_name("지정") is False

    # -- Round 55: conjunction parsing artifact --
    def test_artifact_기및주(self):
        # 기및주 = "기본술기 및 주의사항" parsing artifact (및 = "and")
        assert _is_plausible_korean_name("기및주") is False

    # -- Round 56: clinic name, common word, parsing artifact --
    def test_clinic_연세고운(self):
        # 연세고운 = clinic name fragment "연세고운피부과"
        assert _is_plausible_korean_name("연세고운") is False

    def test_word_여러(self):
        # 여러 = "several/various" common word
        assert _is_plausible_korean_name("여러") is False

    def test_artifact_원지도(self):
        # 원지도 = 원(장) + 지도(전문의) parsing artifact
        assert _is_plausible_korean_name("원지도") is False

    # -- Round 57: adverb, district name --
    def test_adverb_반드시(self):
        # 반드시 = "certainly/necessarily" adverb
        assert _is_plausible_korean_name("반드시") is False

    def test_district_송파구(self):
        # 송파구 = Songpa-gu district name
        assert _is_plausible_korean_name("송파구") is False

    # -- Round 58: marketing text, treatment device --
    def test_marketing_정직하고(self):
        # 정직하고 = "being honest and" marketing text conjugation
        assert _is_plausible_korean_name("정직하고") is False

    def test_device_피코(self):
        # 피코 = "Pico" laser treatment device name
        assert _is_plausible_korean_name("피코") is False

    def test_phrase_기반으로(self):
        # 기반으로 = "based on" common phrase fragment
        assert _is_plausible_korean_name("기반으로") is False

    def test_fragment_태체크(self):
        # 태체크 = "check" fragment from DOM text
        assert _is_plausible_korean_name("태체크") is False

    def test_word_정밀(self):
        # 정밀 = "precision/precise" common word
        assert _is_plausible_korean_name("정밀") is False

    def test_verb_하였는데(self):
        # 하였는데 = "had done, but" verb conjugation
        assert _is_plausible_korean_name("하였는데") is False

    # -- Round 59: parsing artifacts, particle-appended word --
    def test_artifact_원전임(self):
        # 원전임 = 원(장) + 전임 parsing artifact
        assert _is_plausible_korean_name("원전임") is False

    def test_particle_전국은(self):
        # 전국은 = "nationwide" + topic particle 은
        assert _is_plausible_korean_name("전국은") is False

    def test_fragment_임상강(self):
        # 임상강 = "clinical instructor" (임상강사) fragment
        assert _is_plausible_korean_name("임상강") is False

    # -- Round 61: honorary title, phone label, disease, honorific plural --
    def test_word_명예(self):
        # 명예 = "honorary" title word
        assert _is_plausible_korean_name("명예") is False

    def test_label_전화번호(self):
        # 전화번호 = "phone number" UI label
        assert _is_plausible_korean_name("전화번호") is False

    def test_word_한병(self):
        # 한병 = "one bottle" or "Korean disease" common word
        assert _is_plausible_korean_name("한병") is False

    def test_honorific_선생님들(self):
        # 선생님들 = "teachers/doctors" honorific plural
        assert _is_plausible_korean_name("선생님들") is False

    # -- Round 62: branch name fragment --
    def test_branch_강남본(self):
        # 강남본 = "강남본점" (Gangnam main branch) truncated
        assert _is_plausible_korean_name("강남본") is False

    # -- Round 63: marketing slang, brand name, kinship suffix --
    def test_slang_강남언니(self):
        # 강남언니 = "Gangnam unni" marketing slang, not a doctor name
        assert _is_plausible_korean_name("강남언니") is False

    def test_brand_노즈랩(self):
        # 노즈랩 = "Nose Lab" brand name
        assert _is_plausible_korean_name("노즈랩") is False

    def test_suffix_언니(self):
        # X언니 pattern: 김언니 = "Kim unni" kinship term, not a name
        assert _is_plausible_korean_name("김언니") is False

    # -- Round 64: connective, brand, terms, parsing artifact, adjective/negative suffixes --
    def test_connective_하고(self):
        # 하고 = "and" connective ending
        assert _is_plausible_korean_name("하고") is False

    def test_brand_하우스(self):
        # 하우스 = "house" from clinic name (힐하우스)
        assert _is_plausible_korean_name("하우스") is False

    def test_terms_이용약(self):
        # 이용약 = truncated from "이용약관" (terms of use)
        assert _is_plausible_korean_name("이용약") is False

    def test_artifact_황상민이(self):
        # 황상민이 = name "황상민" + subject particle 이
        assert _is_plausible_korean_name("황상민이") is False

    def test_suffix_많은(self):
        # 이많은 = surname 이 + "많은" (many) adjective
        assert _is_plausible_korean_name("이많은") is False

    def test_suffix_아닌(self):
        # 이아닌 = surname 이 + "아닌" (not being) negative adjective
        assert _is_plausible_korean_name("이아닌") is False

    # -- Round 65: common word --
    def test_word_신뢰성(self):
        # 신뢰성 = "reliability" (信賴性) common word
        assert _is_plausible_korean_name("신뢰성") is False

    # -- Round 66: location name, credential substring --
    def test_location_강서화곡(self):
        # 강서화곡 = 강서구 화곡동 location name
        assert _is_plausible_korean_name("강서화곡") is False

    def test_substring_국제(self):
        # 국제인명 = "International Who's Who" credential text
        assert _is_plausible_korean_name("국제인명") is False

    # -- Round 67: station name, credential substring --
    def test_station_신논현(self):
        # 신논현 = Sinnonhyeon station/area name
        assert _is_plausible_korean_name("신논현") is False

    def test_substring_방송(self):
        # 방송출연 = "TV appearance" credential text (방송 substring)
        assert _is_plausible_korean_name("방송출연") is False

    # -- Round 68: common word, credential truncation --
    def test_word_제공(self):
        # 제공 = "provision/provided" (提供) common word
        assert _is_plausible_korean_name("제공") is False

    def test_credential_한국피(self):
        # 한국피 = truncated from "한국피부과학회" (Korean Dermatology Society)
        assert _is_plausible_korean_name("한국피") is False

    # -- Round 69: marketing text --
    def test_marketing_고운세상(self):
        # 고운세상 = "beautiful world" marketing text
        assert _is_plausible_korean_name("고운세상") is False

    def test_marketing_고운세(self):
        # 고운세 = truncated from "고운세상" marketing text
        assert _is_plausible_korean_name("고운세") is False

    # -- Round 70: credential text, committee fragment --
    def test_credential_국가고시(self):
        # 국가고시 = "national exam" (國家考試) credential text
        assert _is_plausible_korean_name("국가고시") is False

    def test_committee_정책위(self):
        # 정책위 = "policy committee" (정책위원회) truncated
        assert _is_plausible_korean_name("정책위") is False

    # -- Round 73: common word --
    def test_word_지하철(self):
        # 지하철 = "subway" (地下鐵) common word
        assert _is_plausible_korean_name("지하철") is False

    def test_credential_하나이비(self):
        # 하나이비 = truncation of "하나이비인후과병원" (hospital name in credentials)
        assert _is_plausible_korean_name("하나이비") is False

    def test_clinic_우태하피(self):
        # 우태하피 = truncation of "우태하피부과" (clinic's own name)
        assert _is_plausible_korean_name("우태하피") is False

    def test_given_서시술(self):
        # 서시술 = 서(surname) + 시술(procedure) — medical term as given name
        assert _is_plausible_korean_name("서시술") is False

    def test_location_인천(self):
        # 인천 = Incheon city name (인 is a valid surname)
        assert _is_plausible_korean_name("인천") is False

    def test_word_여의사가(self):
        # 여의사가 = "female doctor + subject particle" fragment
        assert _is_plausible_korean_name("여의사가") is False

    def test_word_진료일(self):
        # 진료일 = "consultation day" (schedule label)
        assert _is_plausible_korean_name("진료일") is False

    def test_word_주치의가(self):
        # 주치의가 = "primary doctor + subject particle" fragment
        assert _is_plausible_korean_name("주치의가") is False

    def test_word_이저수술(self):
        # 이저수술 = surgery text fragment (레이저수술 truncated)
        assert _is_plausible_korean_name("이저수술") is False

    def test_word_마취통증(self):
        # 마취통증 = "anesthesia pain" medical term
        assert _is_plausible_korean_name("마취통증") is False

    # -- Round 88: clinic name fragment, marketing adverb --
    def test_fragment_원강남(self):
        # 원강남 = clinic name fragment (너와의원 강남 → 원+강남)
        assert _is_plausible_korean_name("원강남") is False

    def test_word_안전하게(self):
        # 안전하게 = "safely" marketing adverb
        assert _is_plausible_korean_name("안전하게") is False

    # -- Round 93: credential fragment --
    def test_credential_인정(self):
        # 인정 = "certified/recognized" from "인정전문의" (board-certified specialist)
        assert _is_plausible_korean_name("인정") is False

    # -- Round 95: navigation label --
    def test_nav_진료안내(self):
        # 진료안내 = "consultation guide" navigation menu label
        assert _is_plausible_korean_name("진료안내") is False

    # -- Round 99: credential text --
    def test_credential_우등졸업(self):
        # 우등졸업 = "graduated with honors" credential fragment
        assert _is_plausible_korean_name("우등졸업") is False

    # -- Round 100: parsing artifact --
    def test_artifact_최혜진원(self):
        # 최혜진원 = "최혜진" + truncated "원장" parsing artifact
        assert _is_plausible_korean_name("최혜진원") is False

    # -- Round 102: text fragment --
    def test_fragment_은여(self):
        # 은여 = page parsing noise fragment
        assert _is_plausible_korean_name("은여") is False

    # -- Round 105: sentence truncation --
    def test_truncation_김융입니(self):
        # 김융입니 = truncated from "김융입니다" (I am Kim Yung)
        assert _is_plausible_korean_name("김융입니") is False

    # -- Round 106: UI labels --
    def test_ui_기본순(self):
        # 기본순 = "default sort order" UI label
        assert _is_plausible_korean_name("기본순") is False

    def test_ui_전방문(self):
        # 전방문 = "all visits" / "previous visit" UI label
        assert _is_plausible_korean_name("전방문") is False

    def test_ui_전체보기(self):
        # 전체보기 = "view all" UI label
        assert _is_plausible_korean_name("전체보기") is False

    def test_ui_이동(self):
        # 이동 = "move/navigate" UI label
        assert _is_plausible_korean_name("이동") is False

    # -- None input --
    def test_none_rejected(self):
        assert _is_plausible_korean_name(None) is False
