"""International usability analyzer — evaluates UX readiness for foreign patients."""

import re

from bs4 import BeautifulSoup


# Language switcher patterns
_LANG_SWITCH_PATTERNS = [
    re.compile(r"lang(uage)?[-_]?(switch|select|toggle|chooser|picker)", re.I),
    re.compile(r"translate|translator|translation", re.I),
    re.compile(r"google[_-]?translate", re.I),
]

_LANG_SWITCH_LINK_RE = re.compile(r"/(en|ja|jp|zh|cn|vi|th|ru|ar)(/|$|\?)", re.I)

_FLAG_ICON_RE = re.compile(
    r"flag[-_]?(icon|img|image)|globe[-_]?icon|🌐|🇺🇸|🇯🇵|🇨🇳|🇬🇧|🇰🇷", re.I,
)

# International phone patterns
_INTL_PHONE_RE = re.compile(r"\+\d{1,3}[\s.-]?\(?\d")

# Timezone patterns
_TIMEZONE_RE = re.compile(r"\bKST\b|\bUTC\b|\bGMT\b|\bJST\b|\bCST\b|\bEST\b|\bPST\b|시간대|\btimezone\b|time\s*zone", re.I)

# Currency patterns
_CURRENCY_RE = re.compile(r"USD|JPY|CNY|EUR|GBP|\$\d|¥\d|€\d|£\d", re.I)

# Google Translate widget
_GOOGLE_TRANSLATE_RE = re.compile(
    r"google[-_]?translate|translate\.google|notranslate|gtranslate", re.I,
)

# Visa / immigration patterns
_VISA_RE = re.compile(r"비자|visa|입국|immigration|체류|residency|stay\s*permit", re.I)

# Travel support patterns
_TRAVEL_RE = re.compile(
    r"pickup|픽업|공항|airport|hotel|숙소|accommodation|lodging|shuttle|transfer|게스트하우스|guesthouse",
    re.I,
)

# International payment patterns
_PAYMENT_RE = re.compile(
    r"alipay|wechat\s*pay|unionpay|paypal|stripe|visa|mastercard|jcb|amex|american\s*express",
    re.I,
)
# Exclude "visa" when it appears in immigration context
_PAYMENT_VISA_RE = re.compile(r"visa\s*(card|결제|payment|pay|accepted|accepted)", re.I)

# Multilingual font patterns
_MULTILINGUAL_FONT_RE = re.compile(
    r"noto[\s+_-]*sans[\s+_-]*(jp|sc|tc|kr|cjk)|hiragino|meiryo|microsoft[\s+_-]*yahei|simsun|mingliu|malgun|source[\s+_-]*han",
    re.I,
)

# Non-Korean alt text detection
_NON_KO_ALT_RE = re.compile(r"[a-zA-Z]{4,}|[\u3040-\u309F]|[\u30A0-\u30FF]|[\u4E00-\u9FFF]")
_KO_ONLY_RE = re.compile(r"^[\uAC00-\uD7A3\u3131-\u3163\s\d.,!?~·\-_()]+$")


def _check_lang_switcher(main_soup: BeautifulSoup) -> dict:
    """Check for language switcher accessibility in navigation."""
    full_html = str(main_soup)

    # Check nav area first
    nav = main_soup.find("nav") or main_soup.find("header")
    nav_html = str(nav) if nav else ""

    # 1. Direct pattern match in nav
    in_nav = False
    for pattern in _LANG_SWITCH_PATTERNS:
        if pattern.search(nav_html):
            in_nav = True
            break

    # 2. Language links in nav (/en, /ja, /zh)
    if not in_nav and nav:
        for a in nav.find_all("a", href=True):
            if _LANG_SWITCH_LINK_RE.search(str(a.get("href", ""))):
                in_nav = True
                break

    # 3. Flag/globe icons in nav
    if not in_nav and nav:
        if _FLAG_ICON_RE.search(nav_html):
            in_nav = True

    # 4. Select element with language options in nav
    if not in_nav and nav:
        for select in nav.find_all("select"):
            select_str = str(select)
            if any(
                kw in select_str.lower()
                for kw in ["lang", "language", "en", "ja", "zh", "english", "japanese", "chinese"]
            ):
                in_nav = True
                break

    # Check anywhere on page (deeper access)
    anywhere = False
    if not in_nav:
        for pattern in _LANG_SWITCH_PATTERNS:
            if pattern.search(full_html):
                anywhere = True
                break
        if not anywhere:
            for a in main_soup.find_all("a", href=True):
                if _LANG_SWITCH_LINK_RE.search(str(a.get("href", ""))):
                    anywhere = True
                    break
        if not anywhere and _FLAG_ICON_RE.search(full_html):
            anywhere = True

    if in_nav:
        return {"status": "pass", "detail": "네비게이션에 언어 전환 요소 있음"}
    if anywhere:
        return {"status": "warn", "detail": "언어 전환 요소가 있으나 네비게이션 1단계 접근이 아님"}
    return {"status": "fail", "detail": "언어 전환 버튼 없음"}


def _check_intl_phone(pages: list[dict]) -> dict:
    """Check for international phone number format (+82 etc.)."""
    for page in pages:
        html = page.get("html", "")
        if _INTL_PHONE_RE.search(html):
            return {"status": "pass", "detail": "국제 전화번호 형식(국가코드 포함) 발견"}
    # Check if any phone exists at all
    phone_re = re.compile(r"0\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}")
    for page in pages:
        if phone_re.search(page.get("html", "")):
            return {"status": "warn", "detail": "국내 전화번호만 있음, +82 국가코드 미포함"}
    return {"status": "fail", "detail": "전화번호 없음"}


def _check_timezone(pages: list[dict]) -> dict:
    """Check for timezone display."""
    for page in pages:
        if _TIMEZONE_RE.search(page.get("html", "")):
            return {"status": "pass", "detail": "시간대 정보 표시됨"}
    return {"status": "fail", "detail": "시간대 미표시 (영업시간에 KST/UTC 등 없음)"}


def _check_currency(pages: list[dict]) -> dict:
    """Check for multi-currency display."""
    for page in pages:
        if _CURRENCY_RE.search(page.get("html", "")):
            return {"status": "pass", "detail": "해외 통화 표시 발견 (USD/JPY/CNY 등)"}
    return {"status": "fail", "detail": "원(₩)만 표기, 해외 통화 미표시"}


def _check_google_translate(pages: list[dict]) -> dict:
    """Check for Google Translate widget."""
    for page in pages:
        if _GOOGLE_TRANSLATE_RE.search(page.get("html", "")):
            return {"status": "pass", "detail": "Google 번역 위젯 발견"}
    return {"status": "fail", "detail": "번역 위젯 없음"}


def _check_visa_info(pages: list[dict]) -> dict:
    """Check for visa/immigration information."""
    for page in pages:
        soup = BeautifulSoup(page.get("html", ""), "html.parser")
        text = soup.get_text()
        if _VISA_RE.search(text):
            return {"status": "pass", "detail": "비자/입국 관련 정보 발견"}
    return {"status": "fail", "detail": "비자/입국 정보 없음"}


def _check_travel_support(pages: list[dict]) -> dict:
    """Check for travel support (airport pickup, hotel, etc.)."""
    for page in pages:
        soup = BeautifulSoup(page.get("html", ""), "html.parser")
        text = soup.get_text()
        if _TRAVEL_RE.search(text):
            return {"status": "pass", "detail": "공항 픽업/숙소 안내 정보 발견"}
    return {"status": "fail", "detail": "픽업/숙소 안내 없음"}


def _check_payment_methods(pages: list[dict]) -> dict:
    """Check for international payment methods."""
    found_methods: list[str] = []
    for page in pages:
        html = page.get("html", "")
        for method in ["alipay", "wechat pay", "unionpay", "paypal", "jcb"]:
            if method in html.lower() and method not in found_methods:
                found_methods.append(method)
        # "visa" as payment (not immigration)
        if _PAYMENT_VISA_RE.search(html) and "visa" not in found_methods:
            found_methods.append("visa")
        if re.search(r"mastercard", html, re.I) and "mastercard" not in found_methods:
            found_methods.append("mastercard")

    if len(found_methods) >= 2:
        return {
            "status": "pass",
            "detail": f"해외 결제수단 발견: {', '.join(found_methods)}",
        }
    if len(found_methods) == 1:
        return {
            "status": "warn",
            "detail": f"{found_methods[0]}만 발견, 추가 결제수단 권장",
        }
    return {"status": "fail", "detail": "해외 결제수단(Alipay, WeChat Pay, PayPal 등) 없음"}


def _check_multilingual_fonts(pages: list[dict]) -> dict:
    """Check for multilingual font support."""
    for page in pages:
        html = page.get("html", "")
        if _MULTILINGUAL_FONT_RE.search(html):
            return {"status": "pass", "detail": "중문/일문 전용 웹폰트 포함"}
    # Check for generic CJK font in CSS
    for page in pages:
        soup = BeautifulSoup(page.get("html", ""), "html.parser")
        styles = soup.find_all("style")
        for style in styles:
            if style.string and _MULTILINGUAL_FONT_RE.search(style.string):
                return {"status": "pass", "detail": "CSS에 다국어 폰트 지정됨"}
    return {"status": "warn", "detail": "중문/일문 전용 폰트 미지정"}


def _check_alt_multilingual(pages: list[dict]) -> dict:
    """Check for multilingual image alt text."""
    total_with_alt = 0
    non_ko_alt_count = 0

    for page in pages:
        soup = BeautifulSoup(page.get("html", ""), "html.parser")
        for img in soup.find_all("img", alt=True):
            alt = img["alt"].strip()
            if not alt:
                continue
            total_with_alt += 1
            if not _KO_ONLY_RE.match(alt) and _NON_KO_ALT_RE.search(alt):
                non_ko_alt_count += 1

    if total_with_alt == 0:
        return {"status": "fail", "detail": "이미지 alt 텍스트 없음"}
    if non_ko_alt_count > 0:
        ratio = round(non_ko_alt_count / total_with_alt * 100)
        return {
            "status": "pass" if ratio >= 30 else "warn",
            "detail": f"다국어 alt 텍스트 {non_ko_alt_count}/{total_with_alt}개 ({ratio}%)",
        }
    return {"status": "fail", "detail": "이미지 alt 텍스트가 한국어만 사용"}


# Check configs for scoring and recommendations
_CHECK_CONFIGS: list[dict] = [
    {
        "key": "lang_switcher",
        "label": "언어 전환 버튼",
        "weight": 15,
        "rec_high": "메인 네비게이션에 언어 전환 버튼 추가 (국기 아이콘 권장)",
    },
    {
        "key": "intl_phone",
        "label": "국제 전화번호",
        "weight": 10,
        "rec_high": "전화번호에 +82 국가코드를 추가하세요",
    },
    {
        "key": "timezone",
        "label": "시간대 표시",
        "weight": 8,
        "rec_high": "영업시간에 KST(한국 표준시) 표기를 추가하세요",
    },
    {
        "key": "currency",
        "label": "다중 통화 표시",
        "weight": 8,
        "rec_high": "시술 가격에 USD/JPY/CNY 환산 금액을 병기하세요",
    },
    {
        "key": "google_translate",
        "label": "번역 위젯",
        "weight": 7,
        "rec_high": "Google Translate 위젯을 설치하여 자동 번역을 지원하세요",
    },
    {
        "key": "visa_info",
        "label": "비자/입국 안내",
        "weight": 12,
        "rec_high": "의료관광 비자(C-3-3) 안내 페이지를 추가하세요",
    },
    {
        "key": "travel_support",
        "label": "공항 픽업/숙소",
        "weight": 12,
        "rec_high": "공항 픽업 서비스와 제휴 숙소 안내를 추가하세요",
    },
    {
        "key": "payment_methods",
        "label": "해외 결제수단",
        "weight": 10,
        "rec_high": "Alipay, WeChat Pay, PayPal 등 해외 결제수단을 추가하세요",
    },
    {
        "key": "multilingual_fonts",
        "label": "다국어 폰트",
        "weight": 8,
        "rec_high": "Noto Sans JP/SC 등 CJK 웹폰트를 추가하여 가독성을 개선하세요",
    },
    {
        "key": "alt_multilingual",
        "label": "이미지 alt 다국어",
        "weight": 10,
        "rec_high": "주요 이미지의 alt 텍스트를 영어/일본어/중국어로 제공하세요",
    },
]


def analyze_international_usability(
    pages: list[dict],
    multilingual_readiness: dict,
) -> dict:
    """Analyze website UX readiness for foreign patients.

    Args:
        pages: Crawled page list with keys: url, html, status_code
        multilingual_readiness: Multilingual readiness result (already computed)

    Returns:
        Analysis result with overall_score, checks, counts, and recommendations.
    """
    if not pages:
        checks = {cfg["key"]: {"status": "fail", "detail": "분석할 페이지 없음"} for cfg in _CHECK_CONFIGS}
        return {
            "overall_score": 0,
            "checks": checks,
            "pass_count": 0,
            "warn_count": 0,
            "fail_count": len(_CHECK_CONFIGS),
            "recommendations": [],
        }

    main_soup = BeautifulSoup(pages[0].get("html", ""), "html.parser")

    # Run all checks
    checks: dict[str, dict] = {
        "lang_switcher": _check_lang_switcher(main_soup),
        "intl_phone": _check_intl_phone(pages),
        "timezone": _check_timezone(pages),
        "currency": _check_currency(pages),
        "google_translate": _check_google_translate(pages),
        "visa_info": _check_visa_info(pages),
        "travel_support": _check_travel_support(pages),
        "payment_methods": _check_payment_methods(pages),
        "multilingual_fonts": _check_multilingual_fonts(pages),
        "alt_multilingual": _check_alt_multilingual(pages),
    }

    # Calculate score
    total_weight = sum(cfg["weight"] for cfg in _CHECK_CONFIGS)
    earned = 0
    pass_count = 0
    warn_count = 0
    fail_count = 0

    for cfg in _CHECK_CONFIGS:
        status = checks[cfg["key"]]["status"]
        if status == "pass":
            earned += cfg["weight"]
            pass_count += 1
        elif status == "warn":
            earned += cfg["weight"] * 0.5
            warn_count += 1
        else:
            fail_count += 1

    overall_score = round(earned / total_weight * 100) if total_weight > 0 else 0

    # Boost/penalize based on multilingual readiness
    ml_score = multilingual_readiness.get("overall_score", 0)
    if ml_score >= 50:
        overall_score = min(100, overall_score + 5)
    elif ml_score == 0 and overall_score > 20:
        overall_score = max(0, overall_score - 5)

    # Generate recommendations
    recommendations: list[dict] = []
    for cfg in _CHECK_CONFIGS:
        status = checks[cfg["key"]]["status"]
        if status == "fail":
            recommendations.append({
                "priority": "high",
                "check": cfg["key"],
                "message": cfg["rec_high"],
            })
        elif status == "warn":
            recommendations.append({
                "priority": "medium",
                "check": cfg["key"],
                "message": cfg["rec_high"],
            })

    # Sort: high priority first
    recommendations.sort(key=lambda r: 0 if r["priority"] == "high" else 1)

    return {
        "overall_score": overall_score,
        "checks": checks,
        "pass_count": pass_count,
        "warn_count": warn_count,
        "fail_count": fail_count,
        "recommendations": recommendations,
    }
