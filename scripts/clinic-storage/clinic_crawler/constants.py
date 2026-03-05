"""Constants for social channel detection, doctor extraction, and Korean name validation."""

import re

# ---------------------------------------------------------------------------
# Platform URL patterns for social channel detection
# ---------------------------------------------------------------------------
PLATFORM_PATTERNS = {
    "KakaoTalk": [
        r"pf\.kakao\.com/", r"open\.kakao\.com/o/",
        r"talk\.kakao\.com/", r"kakao\.com/channel/",
    ],
    "NaverTalk": [r"talk\.naver\.com/"],
    "NaverShortlink": [r"naver\.me/"],
    "Line": [r"line\.me/", r"lin\.ee/"],
    "WeChat": [r"u\.wechat\.com/", r"weixin\.qq\.com/"],
    "WhatsApp": [r"wa\.me/", r"api\.whatsapp\.com/"],
    "Telegram": [r"t\.me/[^/]+$"],
    "FacebookMessenger": [r"m\.me/"],
    "NaverBooking": [r"booking\.naver\.com/"],
    "NaverMap": [r"map\.naver\.com/", r"m\.place\.naver\.com/"],
    "Instagram": [r"instagram\.com/"],
    "YouTube": [r"youtube\.com/", r"youtu\.be/"],
    "NaverBlog": [r"blog\.naver\.com/"],
    "NaverCafe": [r"cafe\.naver\.com/"],
    "Facebook": [r"facebook\.com/(?!.*messenger)"],
}

PHONE_RE = re.compile(
    r"(?:0\d{1,2})[-.\s]?\d{3,4}[-.\s]?\d{4}|\+82[-.\s]?\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}"
)

TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term",
                   "utm_content", "ref", "fbclid", "gclid", "igshid"}

# ---------------------------------------------------------------------------
# Doctor menu labels
# ---------------------------------------------------------------------------
DOCTOR_PRIMARY = [
    "의료진", "의료진 소개", "의료진소개", "원장 소개", "원장소개",
    "전문의 소개", "전문의소개", "DOCTOR", "Doctor", "Our Doctors", "Medical Staff",
]
DOCTOR_SECONDARY = [
    "원장님", "대표원장", "의료팀", "진료진", "진료 안내",
    "클리닉 소개", "Staff", "Team", "About Us",
    "병원소개", "병원 소개", "About Umi", "About TheHill",
    "ABOUT Dr", "Dr.", "대표원장 소개",
]
DOCTOR_SUBMENU_PARENTS = [
    "병원 소개", "병원소개", "클리닉 소개", "소개", "병원 안내", "클리닉 안내",
    "About", "About Us", "병원소개/위치",
]
SUBMENU_PARENT_INTRO_RE = re.compile(r".{1,10}\s*소개$")

# ---------------------------------------------------------------------------
# Doctor role detection
# ---------------------------------------------------------------------------
# Canonical role pattern string - single source of truth for all regex usage
ROLE_PATTERN_STR = (
    "수석원장|교육원장|진료원장|총괄원장|대표원장|부원장|원장"
    "|지도전문의|전문의|의사|레지던트|인턴"
)
# Subset for name-role extraction (excludes 레지던트/인턴 which rarely appear inline)
ROLE_EXTRACT_STR = (
    "수석원장|교육원장|진료원장|총괄원장|대표원장|부원장|원장"
    "|지도전문의|전문의|의사"
)

ROLE_RE = re.compile(rf"^(.+?)\s+({ROLE_PATTERN_STR})$")

DOCTOR_ROLES_KEEP = {
    "원장", "대표원장", "부원장", "전문의", "의사", "레지던트", "인턴",
    "수석원장", "교육원장", "진료원장", "총괄원장", "지도전문의",
}
DOCTOR_ROLES_EXCLUDE = {"간호사", "간호조무사", "피부관리사", "상담사", "코디네이터", "스텝", "직원"}

# ---------------------------------------------------------------------------
# Korean name validation - single source of truth for JS and Python
# ---------------------------------------------------------------------------

# Top ~85 Korean surnames covering 99.9%+ of population
KOREAN_SURNAMES = set(
    "김이박최정강조윤장임한오서신권황안송류전홍유고문양손배백허남심노하"
    "곽성차주우구민진지엄채원천방공현함변추도소석선설마길연위표명기반왕"
    "금옥육인맹제모탁국여어은편빈예봉경태피감복"
)

# Exact-match blocklist: full strings that are never valid names
NON_NAME_WORDS = {
    # Role/title words (2-char that look like names but are titles)
    "대표", "원장", "선생", "전담", "인사", "소속",
    # Role/title fragments (3+ char)
    "대표원", "원대표", "부대표", "병원장", "원장님", "선생님",
    # Medical/academic terms
    "의학", "진료", "진단", "보험", "안과", "여의사", "인증",
    "교육", "경력", "학력", "경험", "운영", "소개", "안내", "예약",
    # Common nouns/adjectives
    "대한", "멤버", "보유", "도입", "주요", "최신", "어떤", "최애",
    "주름", "기기", "노하우",
    # DOM text fragments (object+particle)
    "고객을", "한분한", "진료를", "상담을", "예약을", "문의를",
    "안내를", "소개를", "정보를", "치료를", "시술을", "관리를",
    "한번의", "한분의", "한눈에", "한걸음",
    # Brand names, clinic-specific words
    "유튜브", "안녕하", "고객", "차앤유", "원소개",
    "이벤트", "공지사", "문의하", "예약하", "진료시", "오시는",
    "이퓨어", "우아성", "박훤함", "마인피", "하나이",
    # Branch suffixes (강남점, 서울점, etc.)
    "강남점", "서울점", "부산점", "대전점", "인천점",
    "구로점", "잠실점", "홍대점", "명동점", "신사점",
    # Location names (2-char that pass surname check)
    "홍대", "노원", "목동", "잠실", "신촌", "합정", "마포",
    "성수", "건대", "이대", "원노원", "서초", "신사",
    "강남", "천호", "하남", "구리", "강서", "송파", "구로",
    "명동", "여의도", "인천",
    "연신내", "왕십리",
    # OCR/text noise
    "마취통", "장없이", "전화번",
    # Marketing/brand fragments
    "오랜", "성장한", "유픽", "지도", "신뢰", "오직",
    # UI labels, honorifics, misc fragments
    "전체", "원부", "강북삼", "고객님", "구분",
    "연세청", "연세청아", "원신사", "주시면", "구주", "지여",
    # Round 4: common words misidentified as names
    "이력", "이송", "한국", "공동", "위해", "전국",
    "방문", "한문", "전임", "전에", "오전", "안심",
    "민부", "문여", "한정", "선정",
    # Round 4: country/nation fragments from credential text
    "한민국",
    # Round 4: location names
    "홍제",
    # Round 5: university/institution name fragments
    "이화여", "이화여자",
    # Round 6: branch/district names that pass surname check
    "공덕", "마포공", "마포공덕", "한남", "구의",
    # Round 10: common words and UI labels
    "인사말",
    # Round 14: common word (advisor/consultant 顧問)
    "고문",
    # Round 15: pronoun, common word, clinic brand
    "제가", "경우", "연세아인",
    # Round 16+25+26: clinic brand, parsing artifacts (name+원장 concatenation)
    "제너리스", "임정민원", "김지영원", "김윤미원",
    # Round 26: clinic brand fragment (모던스탠다드 truncated)
    "모던스탠",
    # Round 17: section header, common word
    "인사글", "국내",
    # Round 18: marketing text, sentence fragments, honorific, bio header
    "안티에이", "정직함이", "한분한분", "주요약력",
    # Round 21: reservation text
    "예약제로",
    # Round 22: medical term (neck 頸部)
    "경부",
    # Round 24: schedule label (진료시 already blocked, 4-char version)
    "진료시간",
    # Round 27: legal term, role title
    "이용약관", "공동대표",
    # Round 29: military text fragment, clinic brand fragment
    "공군사", "공군사령", "오아로피",
    # Round 30: adjective, UI label
    "진정한", "전후사진",
    # Round 31: common words, credential header, marketing text
    "전세계", "명의", "고픈", "은옥건", "주요경력", "편한세상",
    # Round 31b: clinic name, medical procedure
    "옥건", "모발이식",
    # Round 33: credential fragment, parsing artifact (name+이전 concatenation)
    "주요약", "강현이전", "성균관",
    # Round 34: parsing artifact (원장+name), credential text
    "원이건", "공중보건",
    # Round 35: treatment categories, common word
    "여드름", "제모", "기타", "제언",
    # Round 36: pronoun/determiner
    "어느",
    # Round 37: credential/branch/location fragments
    "국립중앙", "강남뮤즈", "이대목동", "이대목", "남뮤즈", "김로데",
    # Round 38: treatment device, branch name fragment
    "복합광", "명동쁨",
    # Round 39: UI label (treatment consultation)
    "진료상담",
    # Round 40: editorial committee fragment, sentence fragment, location
    "편찬위", "진료보다", "위례중앙",
    # Round 43: text fragment (from "1인여성" or "본인여부")
    "인여",
    # Round 44: verb ending, district name, treatment fragment, parsing artifact
    "하는", "강서구", "진료로", "김병균원",
    # Round 45: clinic brand name
    "강남비비", "남비비",
    # Round 46: area fragment, connective ending
    "위동네", "하더라도",
    # Round 48: credential typo, district name
    "공증보건", "서초구",
    # Round 49: medical specialty, country/common word, adverb
    "이비인후", "인도", "정확히",
    # Round 50: treatment fragments, soundproof/food fragment, parsing artifact
    "모치료", "모전문", "방음식", "허선영원",
    # Round 51: role designation fragment, location fragment
    "정전담", "원명동",
    # Round 53: common word, time expression, location fragment
    "소통", "차마다", "원신촌",
    # Round 54: common word (designated/appointed 指定)
    "지정",
    # Round 56: clinic name fragment, common word, parsing artifact
    "연세고운", "여러", "원지도",
    # Round 57: adverb, district name
    "반드시", "송파구",
    # Round 58: marketing text conjugation, treatment device name, phrase fragments
    "정직하고", "피코", "기반으로", "태체크",
    # Round 58b: precision, verb conjugation (non-deterministic extraction)
    "정밀", "하였는데",
    # Round 59: parsing artifacts, particle-appended word
    "원전임", "전국은", "임상강",
    # Round 61: honorary title, phone label, disease/bottle, honorific plural
    "명예", "전화번호", "한병", "선생님들",
    # Round 62: branch name fragment (강남본점 truncated)
    "강남본",
    # Round 63: marketing slang, brand name
    "강남언니", "노즈랩",
    # Round 64: connective ending, brand fragment, terms truncation, parsing artifact
    "하고", "하우스", "이용약", "황상민이",
    # Round 65: common word (reliability 信賴性)
    "신뢰성",
    # Round 66: location name (강서구 화곡동)
    "강서화곡",
    # Round 67: station/area name
    "신논현",
    # Round 68: common word (provision), credential truncation
    "제공", "한국피",
    # Round 69: marketing text (beautiful world), truncated form
    "고운세상", "고운세",
    # Round 70: credential text (national exam), committee fragment
    "국가고시", "정책위",
    # Round 73: common word (subway 地下鐵)
    "지하철",
    # Round 74: credential truncation (하나이비인후과), clinic name truncation (우태하피부과)
    "하나이비", "우태하피",
    # Round 77: "female doctor + particle" fragment, schedule label
    "여의사가", "진료일",
    # Round 84: "primary doctor + particle", surgery fragment, medical term
    "주치의가", "이저수술", "마취통증",
    # Round 88: clinic name fragment (너와의원 강남→원강남), marketing adverb (safely)
    "원강남", "안전하게",
    # Round 93: credential fragment (인정전문의 → 인정 = "certified/recognized")
    "인정",
    # Round 95: navigation label (진료안내 = "consultation guide")
    "진료안내",
    # Round 99: credential text (우등졸업 = "graduated with honors")
    "우등졸업",
    # Round 100: parsing artifact (최혜진원 = "최혜진" + truncated "원장")
    "최혜진원",
    # Round 102: text fragment (은여 from page parsing noise)
    "은여",
    # Round 105: sentence truncation (김융입니 from "김융입니다")
    "김융입니",
    # Round 106: UI labels (sort order, visits filter, view all, navigation)
    "기본순", "전방문", "전체보기", "이동",
}

# Suffix blocklist: given-name parts (name[1:]) that are verb/adjective endings
NON_NAME_SUFFIXES = {
    # Verb/adjective endings
    "싶은", "있는", "없는", "않는", "되는", "하는", "같은",
    "한다", "된다", "니다", "입니", "세요", "적은",
    # Connective endings / comparison particle
    "때문", "부터", "에서", "으로", "까지", "에게",
    "해서", "해야", "라고", "아서", "어서", "이라", "라는", "하고", "지만",
    "보다", "더라도", "였는데",
    # Noun suffixes (particle fragments from DOM text)
    "객을", "분한", "료진", "원을", "문의", "내용", "상담", "예약", "진료",
    "비용", "안내", "소개", "정보", "후기", "리뷰", "사진", "영상",
    # Marketing text fragments
    "나뿐인",
    # OCR/noise/honorific suffixes
    "없이", "취통", "시면", "객님", "북삼",
    # Kinship terms (never valid given names)
    "언니",
    # Adjective/negative endings
    "많은", "아닌",
}

# Given-name blocklist: name[1:] that are titles/roles (e.g. 정대표 = 정+대표)
NON_NAME_GIVEN = {
    # Job titles
    "대표", "원장", "부장", "과장", "실장", "팀장",
    # UI/nav labels
    "소개", "안내", "의원",
    # Compound role fragments (e.g. "원수석" from "수석원장" boundary)
    "수석", "교육", "미국", "진료", "총괄", "연구", "센터",
    # Location names from career text
    "서초", "신사",
    # Medical institution terms
    "본원",
    # Common words as given names
    "오직",
    # Medical procedure term (시술 = procedure/treatment)
    "시술",
}

# Substring blocklist: reject name if any entry appears anywhere in it
NON_NAME_SUBSTRINGS = [
    "병원", "의원", "클리닉", "외과", "내과", "의과", "센터",
    "학회", "학교", "대학", "약국", "닥터", "학과", "피부",
    "점", "위원", "회원", "전문가", "구매", "상식", "활동",
    "협력", "총괄", "증서", "인후과", "의료", "연구",
    "서울", "인터", "채용", "공지", "조회", "철산",
    "미용", "홍보", "오늘", "강사", "소개", "마사", "필러", "고객", "방사선",
    "약력", "복지",
    # Round 55: Korean conjunction "and" (及) — never part of a name
    "및",
    # Round 66: credential text (International 國際)
    "국제",
    # Round 67: credential text (broadcasting 放送)
    "방송",
]

# Truncated word endings: 3-char names ending with these are likely fragments
TRUNCATED_ENDING_CHARS = set("의과에적대는여입")

# ---------------------------------------------------------------------------
# Detail page navigation
# ---------------------------------------------------------------------------
DETAIL_MORE_LABELS = [
    "더보기", "자세히보기", "자세히 보기", "상세보기", "상세 보기",
    "프로필 보기", "프로필보기", "View More", "View Detail", "More",
    "약력 보기", "경력 보기", "이력 보기",
]

# Screenshot persistence directory (relative to project root)
SCREENSHOT_DIR = "data/clinic-results/screenshots"
