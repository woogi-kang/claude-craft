"""Conversion element detection for medical tourism websites."""

import re

from bs4 import BeautifulSoup

from .base import CheckResult, Grade

# CTA keywords (Korean + English)
_CTA_KEYWORDS = re.compile(
    r"예약|상담|문의|접수|book|contact|reserve|appointment|consult|inquiry|schedule",
    re.I,
)

# Procedure page indicators
_PROCEDURE_KEYWORDS = re.compile(
    r"시술|치료|수술|레이저|보톡스|필러|리프팅|procedure|treatment|surgery|therapy",
    re.I,
)

# Messenger patterns
_MESSENGER_PATTERNS: dict[str, list[re.Pattern]] = {
    "kakao": [
        re.compile(r"kakao", re.I),
        re.compile(r"pf\.kakao\.com", re.I),
        re.compile(r"talk\.naver\.com", re.I),  # Kakao channel link variant
    ],
    "line": [
        re.compile(r"line\.me", re.I),
        re.compile(r"lin\.ee", re.I),
        re.compile(r"line-?add", re.I),
    ],
    "wechat": [
        re.compile(r"wechat|weixin|微信", re.I),
    ],
    "chat_widget": [
        re.compile(r"channel\.io", re.I),
        re.compile(r"zendesk", re.I),
        re.compile(r"intercom", re.I),
        re.compile(r"crisp\.chat", re.I),
        re.compile(r"tawk\.to", re.I),
        re.compile(r"livechat", re.I),
    ],
}

# Price keywords
_PRICE_KEYWORDS = re.compile(
    r"가격|price|비용|cost|요금|fee|料金|价格|費用|\d+\s*만\s*원|\d+,\d{3}원",
    re.I,
)

# Form language detection: non-Korean text patterns
_NON_KO_TEXT = re.compile(r"[a-zA-Z]{3,}|[\u3040-\u309F]|[\u4E00-\u9FFF]")


def _detect_cta_buttons(soup: BeautifulSoup) -> list[dict]:
    """Find CTA buttons/links with booking-related text."""
    ctas: list[dict] = []
    for el in soup.find_all(["a", "button"]):
        text = el.get_text(strip=True)
        href = str(el.get("href", ""))
        if _CTA_KEYWORDS.search(text) or _CTA_KEYWORDS.search(href):
            ctas.append({"text": text[:50], "tag": el.name, "href": href[:100]})
    return ctas


def _detect_phone_links(soup: BeautifulSoup) -> dict:
    """Detect phone numbers and whether they use tel: links."""
    tel_links = soup.find_all("a", href=re.compile(r"^tel:", re.I))
    phone_re = re.compile(r"0\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}")
    text = soup.get_text()
    phone_texts = phone_re.findall(text)
    return {
        "tel_links": len(tel_links),
        "phone_numbers_in_text": len(phone_texts),
        "clickable": len(tel_links) > 0,
    }


def _detect_messengers(soup: BeautifulSoup) -> dict[str, bool]:
    """Detect messenger widgets and links."""
    full_html = str(soup)
    found: dict[str, bool] = {}
    for name, patterns in _MESSENGER_PATTERNS.items():
        found[name] = any(p.search(full_html) for p in patterns)
    return found


def _analyze_forms(soup: BeautifulSoup) -> dict:
    """Analyze booking/contact forms."""
    forms = soup.find_all("form")
    if not forms:
        return {"exists": False, "field_count": 0, "multilingual": False}

    # Find the most likely booking form (smallest or first)
    best_form = min(forms, key=lambda f: len(f.find_all("input")))
    inputs = best_form.find_all(["input", "select", "textarea"])
    # Exclude hidden and submit inputs
    visible_inputs = [
        i for i in inputs
        if i.get("type", "text") not in ("hidden", "submit", "button")
    ]
    field_count = len(visible_inputs)

    # Check multilingual: look for non-Korean placeholders/labels
    form_text = best_form.get_text()
    placeholders = [str(i.get("placeholder", "")) for i in visible_inputs]
    labels = best_form.find_all("label")
    label_texts = [l.get_text(strip=True) for l in labels]
    all_form_text = " ".join(placeholders + label_texts + [form_text])
    multilingual = bool(_NON_KO_TEXT.search(all_form_text))

    return {
        "exists": True,
        "field_count": field_count,
        "multilingual": multilingual,
    }


def _detect_price(soup: BeautifulSoup) -> bool:
    """Check if price information is visible."""
    text = soup.get_text()
    return bool(_PRICE_KEYWORDS.search(text))


def check_conversion_elements(pages: list[dict]) -> CheckResult:
    """
    Analyze crawled pages for booking/conversion elements.

    Args:
        pages: List of dicts with keys: url, html, status_code

    Returns:
        CheckResult with conversion element analysis.
    """
    if not pages:
        return CheckResult(
            name="conversion_elements",
            score=0.0,
            grade=Grade.FAIL,
            display_name="예약 전환 요소",
            description="웹사이트의 예약/전환 요소(CTA, 전화, 메신저, 폼)를 분석합니다",
            recommendation="예약 버튼, 전화번호 tel: 링크, 메신저 위젯을 추가하세요",
            issues=["분석할 페이지가 없습니다"],
        )

    main_html = pages[0]["html"]
    main_soup = BeautifulSoup(main_html, "html.parser")

    # 1. CTA detection on main page
    main_ctas = _detect_cta_buttons(main_soup)
    cta_main = len(main_ctas) > 0

    # 2. CTA on procedure pages
    procedure_pages_total = 0
    procedure_pages_with_cta = 0
    for page in pages[1:]:
        url = page.get("url", "")
        page_soup = BeautifulSoup(page["html"], "html.parser")
        title_text = page_soup.title.string if page_soup.title else ""
        body_text = page_soup.get_text()[:500]
        if _PROCEDURE_KEYWORDS.search(url) or _PROCEDURE_KEYWORDS.search(title_text or "") or _PROCEDURE_KEYWORDS.search(body_text):
            procedure_pages_total += 1
            if _detect_cta_buttons(page_soup):
                procedure_pages_with_cta += 1

    # 3. Phone detection
    phone_info = _detect_phone_links(main_soup)

    # 4. Messenger detection
    messengers = _detect_messengers(main_soup)

    # 5. Form analysis
    form_info = _analyze_forms(main_soup)

    # 6. Price visibility (check all pages)
    price_visible = any(
        _detect_price(BeautifulSoup(p["html"], "html.parser")) for p in pages
    )

    # === Scoring ===
    score = 0

    # CTA main page: 20 points
    if cta_main:
        score += 20

    # CTA procedure pages (50%+ coverage): 15 points
    if procedure_pages_total > 0:
        cta_coverage = procedure_pages_with_cta / procedure_pages_total
        if cta_coverage >= 0.5:
            score += 15
    elif cta_main:
        # No procedure pages detected but main has CTA, give partial credit
        score += 8

    # Phone tel: link: 10 points
    if phone_info["clickable"]:
        score += 10

    # Messenger: 15 points + bonus
    messenger_count = sum(1 for v in messengers.values() if v)
    if messenger_count >= 1:
        score += 15
    # LINE/WeChat bonus: +5
    if messengers.get("line") or messengers.get("wechat"):
        score += 5

    # Form: 15 points + bonus
    if form_info["exists"]:
        score += 15
        if form_info["field_count"] <= 5:
            score += 5

    # Price visible: 10 points
    if price_visible:
        score += 10

    # Form multilingual: 10 points
    if form_info.get("multilingual"):
        score += 10

    # Cap at 100
    score = min(score, 100)

    # Normalize to 0.0-1.0
    normalized_score = score / 100.0

    # Build elements found/missing
    elements_found: list[str] = []
    elements_missing: list[str] = []

    for label, present in [
        ("cta_main", cta_main),
        ("phone_clickable", phone_info["clickable"]),
        ("kakao", messengers.get("kakao", False)),
        ("line", messengers.get("line", False)),
        ("wechat", messengers.get("wechat", False)),
        ("chat_widget", messengers.get("chat_widget", False)),
        ("form", form_info["exists"]),
        ("form_multilingual", form_info.get("multilingual", False)),
        ("price", price_visible),
    ]:
        if present:
            elements_found.append(label)
        else:
            elements_missing.append(label)

    # Grade
    if normalized_score >= 0.8:
        grade = Grade.PASS
    elif normalized_score >= 0.4:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    # Issues
    issues: list[str] = []
    if not cta_main:
        issues.append("메인 페이지에 예약/상담 CTA 버튼이 없습니다")
    if not phone_info["clickable"]:
        issues.append("전화번호가 클릭 가능한 tel: 링크로 되어있지 않습니다")
    if messenger_count == 0:
        issues.append("메신저 위젯(카카오, LINE, WeChat 등)이 없습니다")
    if not form_info["exists"]:
        issues.append("예약/문의 폼이 없습니다")
    elif form_info["field_count"] > 5:
        issues.append(f"폼 입력 필드가 {form_info['field_count']}개로 많습니다 (5개 이하 권장)")
    if not price_visible:
        issues.append("가격/비용 정보가 표시되지 않습니다")
    if not form_info.get("multilingual"):
        issues.append("예약 폼이 다국어를 지원하지 않습니다")

    # Recommendation
    if normalized_score >= 0.8:
        recommendation = "전환 요소가 잘 갖춰져 있습니다. LINE/WeChat 추가로 해외 환자 전환율을 높이세요"
    elif normalized_score >= 0.4:
        recommendation = "기본 전환 요소는 있으나, 누락된 요소를 추가하여 전환율을 개선하세요"
    else:
        recommendation = "예약 CTA 버튼, 전화번호 tel: 링크, 메신저 위젯을 우선 추가하세요"

    return CheckResult(
        name="conversion_elements",
        score=normalized_score,
        grade=grade,
        display_name="예약 전환 요소",
        description="웹사이트의 예약/전환 요소(CTA, 전화, 메신저, 폼)를 분석합니다",
        recommendation=recommendation,
        issues=issues,
        details={
            "cta_main": cta_main,
            "cta_main_buttons": main_ctas[:5],
            "cta_procedure_pages": {
                "total": procedure_pages_total,
                "with_cta": procedure_pages_with_cta,
            },
            "phone_clickable": phone_info["clickable"],
            "phone_tel_links": phone_info["tel_links"],
            "phone_numbers_in_text": phone_info["phone_numbers_in_text"],
            "messengers": messengers,
            "form_exists": form_info["exists"],
            "form_fields": form_info.get("field_count", 0),
            "form_multilingual": form_info.get("multilingual", False),
            "price_visible": price_visible,
            "elements_found": elements_found,
            "elements_missing": elements_missing,
            "score_breakdown": {
                "cta_main": 20 if cta_main else 0,
                "cta_procedures": 15 if (procedure_pages_total > 0 and procedure_pages_with_cta / max(procedure_pages_total, 1) >= 0.5) else (8 if cta_main and procedure_pages_total == 0 else 0),
                "phone": 10 if phone_info["clickable"] else 0,
                "messenger": 15 if messenger_count >= 1 else 0,
                "messenger_intl_bonus": 5 if (messengers.get("line") or messengers.get("wechat")) else 0,
                "form": 15 if form_info["exists"] else 0,
                "form_simple_bonus": 5 if (form_info["exists"] and form_info.get("field_count", 99) <= 5) else 0,
                "price": 10 if price_visible else 0,
                "form_multilingual": 10 if form_info.get("multilingual") else 0,
            },
        },
    )
