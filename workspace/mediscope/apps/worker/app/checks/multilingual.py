"""Multilingual / overseas patient readiness checks (3 separate checks)."""

import re
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from .base import CheckResult, Grade

# URL patterns indicating a specific language version
_LANG_PATH_RE = re.compile(
    r"/(en|ja|zh|zh-cn|zh-tw|vi|th|ru|ar|en-us|en-gb|ja-jp|zh-hans|zh-hant)"
    r"(/|$)",
    re.I,
)
_LANG_QUERY_RE = re.compile(r"lang=(en|ja|zh|vi|th|ru|ar)", re.I)

# --- multilingual_pages ---
_ML_DISPLAY_NAME = "외국어 페이지"
_ML_DESCRIPTION = "영어, 일본어, 중국어 등 외국어로 된 페이지가 있는지 확인합니다"
_ML_RECOMMENDATION = (
    "주요 타겟 국가 언어(영어, 일본어, 중국어)로 핵심 페이지(시술 소개, 가격, 오시는 길)를 번역하세요"
)

# --- hreflang ---
_HL_DISPLAY_NAME = "다국어 페이지 연결 표시"
_HL_DESCRIPTION = (
    '검색엔진에 "이 페이지는 한국어 버전이고, 영어 버전은 여기 있습니다"를 알려줍니다'
)
_HL_RECOMMENDATION = (
    '웹 개발자에게 "각 언어별 페이지에 hreflang 태그를 추가해달라"고 요청하세요'
)

# --- overseas_channels ---
_OC_DISPLAY_NAME = "해외 메신저 연결"
_OC_DESCRIPTION = "LINE, WeChat, WhatsApp 등 해외 메신저 채널이 있는지 확인합니다"
_OC_RECOMMENDATION = (
    "타겟 국가에 맞는 메신저(일본: LINE, 중국: WeChat, 동남아: WhatsApp) 공식 계정을 만들고 홈페이지에 링크하세요"
)


def check_multilingual_pages(
    main_html: str, crawled_urls: list[str],
) -> CheckResult:
    """Check for multi-language page availability."""
    soup = BeautifulSoup(main_html, "html.parser")
    detected: set[str] = set()

    # Check <html lang="...">
    html_tag = soup.find("html")
    if html_tag:
        html_lang = (html_tag.get("lang") or "").strip().lower()
        if html_lang:
            detected.add(html_lang.split("-")[0])

    # Check <meta http-equiv="content-language">
    meta_lang = soup.find("meta", attrs={"http-equiv": re.compile(r"content-language", re.I)})
    if meta_lang:
        content = (meta_lang.get("content") or "").strip().lower()
        if content:
            detected.add(content.split("-")[0])

    # Check crawled URLs for language path segments and query params
    for url in crawled_urls:
        m = _LANG_PATH_RE.search(url)
        if m:
            detected.add(m.group(1).lower().split("-")[0])
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        for val in qs.get("lang", []):
            detected.add(val.lower().split("-")[0])

    non_korean = detected - {"ko"}
    lang_count = len(non_korean)

    if lang_count >= 3:
        score = 1.0
    elif lang_count == 2:
        score = 0.7
    elif lang_count == 1:
        score = 0.4
    else:
        score = 0.0

    issues: list[str] = []
    if score == 0.0:
        issues.append("외국어 페이지가 감지되지 않았습니다")

    if score >= 0.8:
        grade = Grade.PASS
    elif score >= 0.4:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="multilingual_pages",
        score=score,
        grade=grade,
        display_name=_ML_DISPLAY_NAME,
        description=_ML_DESCRIPTION,
        recommendation=_ML_RECOMMENDATION,
        issues=issues,
        details={
            "detected_languages": sorted(detected),
        },
    )


def check_hreflang(main_html: str) -> CheckResult:
    """Check <link rel="alternate" hreflang="..."> tags."""
    soup = BeautifulSoup(main_html, "html.parser")
    tags = soup.find_all("link", attrs={"rel": "alternate", "hreflang": True})
    langs = [tag["hreflang"] for tag in tags if tag.get("hreflang")]
    count = len(langs)

    if count >= 2:
        score = 1.0
    elif count == 1:
        score = 0.5
    else:
        score = 0.0

    issues: list[str] = []
    if score == 0.0:
        issues.append("hreflang 태그가 없습니다")

    if score >= 0.8:
        grade = Grade.PASS
    elif score >= 0.5:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="hreflang",
        score=score,
        grade=grade,
        display_name=_HL_DISPLAY_NAME,
        description=_HL_DESCRIPTION,
        recommendation=_HL_RECOMMENDATION,
        issues=issues,
        details={
            "hreflang_tags": langs,
        },
    )


def check_overseas_channels(main_html: str) -> CheckResult:
    """Detect overseas messaging channel links (LINE, WeChat, WhatsApp)."""
    soup = BeautifulSoup(main_html, "html.parser")
    channels: set[str] = set()
    text = soup.get_text()

    for a in soup.find_all("a", href=True):
        href = str(a["href"]).lower()
        if "line.me" in href or "lin.ee" in href:
            channels.add("LINE")
        if "weixin.qq.com" in href:
            channels.add("WeChat")
        if "wa.me" in href or "whatsapp.com" in href:
            channels.add("WhatsApp")

    # WeChat text detection
    if "WeChat" not in channels and re.search(r"(WeChat|微信)", text):
        channels.add("WeChat")

    found = sorted(channels)
    count = len(found)
    if count >= 2:
        score = 1.0
    elif count == 1:
        score = 0.5
    else:
        score = 0.0

    issues: list[str] = []
    if score == 0.0:
        issues.append("해외 환자용 메신저 채널이 없습니다 (LINE/WeChat/WhatsApp)")

    if score >= 0.8:
        grade = Grade.PASS
    elif score >= 0.5:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="overseas_channels",
        score=score,
        grade=grade,
        display_name=_OC_DISPLAY_NAME,
        description=_OC_DESCRIPTION,
        recommendation=_OC_RECOMMENDATION,
        issues=issues,
        details={
            "overseas_channels": found,
        },
    )
