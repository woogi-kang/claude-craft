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
        issues=issues,
        details={
            "overseas_channels": found,
        },
    )
