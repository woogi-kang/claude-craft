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

# Doctor menu labels
DOCTOR_PRIMARY = [
    "의료진", "의료진 소개", "의료진소개", "원장 소개", "원장소개",
    "전문의 소개", "전문의소개", "DOCTOR", "Doctor", "Our Doctors", "Medical Staff",
]
DOCTOR_SECONDARY = [
    "원장님", "대표원장", "의료팀", "진료진", "진료 안내",
    "클리닉 소개", "Staff", "Team", "About Us",
    "병원소개", "병원 소개", "About Umi", "About TheHill",
]
DOCTOR_SUBMENU_PARENTS = [
    "병원 소개", "병원소개", "클리닉 소개", "소개", "병원 안내", "클리닉 안내",
    "About", "About Us", "병원소개/위치",
]
# Regex pattern: "{hospital_name_fragment} 소개" as submenu parent
SUBMENU_PARENT_INTRO_RE = re.compile(r".{1,10}\s*소개$")

DOCTOR_ROLES_KEEP = {"원장", "대표원장", "부원장", "전문의", "의사", "레지던트", "인턴"}
DOCTOR_ROLES_EXCLUDE = {"간호사", "간호조무사", "피부관리사", "상담사", "코디네이터", "스텝", "직원"}

# Korean name validation - top ~60 surnames covering 99%+ of population
KOREAN_SURNAMES = set("김이박최정강조윤장임한오서신권황안송류전홍고문양손배백허유남노하곡성차주우방공민변탁도진지엄채원천구현은봉추위석선설마길연")
# Common verb/adjective endings that get misidentified as given names
NON_NAME_SUFFIXES = {
    "싶은", "있는", "없는", "않는", "되는", "하는", "같은", "때문", "부터",
    "에서", "으로", "까지", "에게", "한다", "된다", "니다", "입니", "세요",
    "해서", "해야", "라고", "아서", "어서", "이라", "라는", "하고", "지만",
}
NON_NAME_WORDS = {"대표원", "원대표", "부대표", "병원장"}
# Title/role suffixes that are NOT given names (e.g. 정대표 = 정 + 대표)
NON_NAME_GIVEN = {"대표", "원장", "부장", "과장", "실장", "팀장", "소개", "안내"}

ROLE_RE = re.compile(r"^(.+?)\s+(원장|대표원장|부원장|전문의|의사|레지던트|인턴)$")
