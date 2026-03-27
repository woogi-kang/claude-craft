"""Structured data checks: Schema.org, FAQ, E-E-A-T signals."""

import json
import re

from bs4 import BeautifulSoup

from ..checks.base import CheckResult, Grade

# --- structured_data ---
_SD_DISPLAY_NAME = "검색 강화 데이터"
_SD_DESCRIPTION = "구글에 병원 정보(진료시간, 위치, 전화번호 등)를 구조화된 형태로 제공합니다"
_SD_RECOMMENDATION = (
    '웹 개발자에게 "Schema.org의 MedicalClinic 타입 JSON-LD를 추가해달라"고 요청하세요'
)

# --- faq_content ---
_FAQ_DISPLAY_NAME = "자주 묻는 질문 (FAQ)"
_FAQ_DESCRIPTION = "FAQ 콘텐츠와 구조화 데이터가 있는지 확인합니다"
_FAQ_RECOMMENDATION = (
    "환자들이 자주 묻는 질문 10-20개를 정리하여 FAQ 페이지를 만들고, FAQPage 스키마를 추가하세요"
)

# --- eeat_signals ---
_EEAT_DISPLAY_NAME = "전문성/신뢰도 표시"
_EEAT_DESCRIPTION = (
    "의사 프로필, 자격 정보, 환자 후기 등 전문성을 보여주는 콘텐츠가 있는지 확인합니다"
)
_EEAT_RECOMMENDATION = (
    "의사 경력/학력/전문의 자격, 환자 후기, 시술 전후 사진을 홈페이지에 게시하세요"
)


def _extract_json_ld(html: str) -> list[dict]:
    """Extract all JSON-LD structured data from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
        except (json.JSONDecodeError, TypeError):
            continue
    return results


def _get_types(json_ld_items: list[dict]) -> set[str]:
    """Get all @type values from JSON-LD items (including nested @graph)."""
    types: set[str] = set()
    for item in json_ld_items:
        if "@type" in item:
            t = item["@type"]
            if isinstance(t, list):
                types.update(t)
            else:
                types.add(t)
        # Handle @graph pattern
        if "@graph" in item and isinstance(item["@graph"], list):
            for node in item["@graph"]:
                if "@type" in node:
                    t = node["@type"]
                    if isinstance(t, list):
                        types.update(t)
                    else:
                        types.add(t)
    return types


def check_structured_data(html: str) -> CheckResult:
    """Check for medical-relevant Schema.org structured data."""
    json_ld = _extract_json_ld(html)
    types = _get_types(json_ld)

    score = 0.0
    issues: list[str] = []
    found_schemas: list[str] = []

    # Medical-specific schemas
    medical_types = {"MedicalClinic", "Physician", "MedicalProcedure", "Hospital",
                     "MedicalOrganization", "Dentist"}
    found_medical = medical_types & types
    if found_medical:
        score += 0.4
        found_schemas.extend(sorted(found_medical))
    else:
        issues.append("의료 관련 Schema.org가 없습니다 (MedicalClinic, Physician 등)")

    # General business schemas
    business_types = {"LocalBusiness", "Organization", "WebSite", "WebPage"}
    found_business = business_types & types
    if found_business:
        score += 0.2
        found_schemas.extend(sorted(found_business))
    elif not found_medical:
        issues.append("기본 비즈니스 Schema.org도 없습니다")

    # Breadcrumb
    if "BreadcrumbList" in types:
        score += 0.1
        found_schemas.append("BreadcrumbList")

    # Any JSON-LD at all
    if json_ld:
        score += 0.1
    else:
        issues.append("JSON-LD 구조화 데이터가 전혀 없습니다")

    # Check microdata/RDFa as fallback
    soup = BeautifulSoup(html, "html.parser")
    microdata = soup.find_all(attrs={"itemtype": True})
    if microdata and not json_ld:
        score += 0.2
        found_schemas.append("microdata")

    score = min(1.0, score)

    if score >= 0.6:
        grade = Grade.PASS
    elif score >= 0.3:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="structured_data",
        score=round(score, 2),
        grade=grade,
        display_name=_SD_DISPLAY_NAME,
        description=_SD_DESCRIPTION,
        recommendation=_SD_RECOMMENDATION,
        issues=issues,
        details={
            "json_ld_count": len(json_ld),
            "schema_types": sorted(types),
            "found_schemas": found_schemas,
        },
    )


def check_faq_content(html: str) -> CheckResult:
    """Check for FAQ structured data and content."""
    json_ld = _extract_json_ld(html)
    types = _get_types(json_ld)
    soup = BeautifulSoup(html, "html.parser")

    score = 0.0
    issues: list[str] = []
    details: dict = {}

    # FAQPage schema
    has_faq_schema = "FAQPage" in types
    details["has_faq_schema"] = has_faq_schema
    if has_faq_schema:
        score += 0.5
    else:
        issues.append("FAQPage 구조화 데이터가 없습니다")

    # FAQ-like HTML content (even without schema)
    faq_indicators = soup.find_all(
        ["details", "summary", "dt", "dd"]
    )
    accordion_elements = soup.find_all(
        attrs={"class": re.compile(r"(faq|accordion|question|answer)", re.I)}
    )
    faq_headings = [
        h for h in soup.find_all(["h1", "h2", "h3", "h4"])
        if re.search(r"(FAQ|자주\s*묻는|질문|Q&A|문의)", h.get_text(), re.I)
    ]

    faq_content_found = bool(faq_indicators or accordion_elements or faq_headings)
    details["has_faq_content"] = faq_content_found

    if faq_content_found:
        score += 0.3
    else:
        issues.append("FAQ 형식의 콘텐츠가 없습니다")

    # Question-answer pairs in content
    qa_pattern = re.compile(r"(Q\.|질문|Question)\s*[:：]", re.I)
    text = soup.get_text()
    qa_count = len(qa_pattern.findall(text))
    details["qa_pair_count"] = qa_count
    if qa_count >= 3:
        score += 0.2
    elif qa_count >= 1:
        score += 0.1

    score = min(1.0, score)

    if score >= 0.6:
        grade = Grade.PASS
    elif score >= 0.3:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="faq_content",
        score=round(score, 2),
        grade=grade,
        display_name=_FAQ_DISPLAY_NAME,
        description=_FAQ_DESCRIPTION,
        recommendation=_FAQ_RECOMMENDATION,
        issues=issues,
        details=details,
    )


def check_eeat_signals(html: str, url: str) -> CheckResult:
    """Check E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()

    score = 0.0
    issues: list[str] = []
    details: dict = {}

    # Author/Doctor profiles
    author_patterns = re.compile(
        r"(의사|원장|대표원장|전문의|교수|박사|dr\.|doctor|physician|specialist)", re.I
    )
    author_matches = author_patterns.findall(text)
    details["author_signal_count"] = len(author_matches)
    if author_matches:
        score += 0.25
    else:
        issues.append("의사/전문의 프로필 정보가 없습니다")

    # Credentials & qualifications
    credential_patterns = re.compile(
        r"(자격증|면허|인증|학력|경력|수련|전공|board.?certified|fellowship|residency)", re.I
    )
    credential_matches = credential_patterns.findall(text)
    details["credential_signal_count"] = len(credential_matches)
    if credential_matches:
        score += 0.2
    else:
        issues.append("자격/경력 정보가 없습니다")

    # Contact & trust signals
    contact_patterns = re.compile(
        r"(전화|연락처|주소|찾아오시는|오시는\s*길|contact|address|phone|tel)", re.I
    )
    contact_matches = contact_patterns.findall(text)
    details["contact_signal_count"] = len(contact_matches)
    if contact_matches:
        score += 0.15

    # Reviews/testimonials
    review_patterns = re.compile(
        r"(후기|리뷰|환자\s*경험|치료\s*사례|review|testimonial|before.?after)", re.I
    )
    review_matches = review_patterns.findall(text)
    details["review_signal_count"] = len(review_matches)
    if review_matches:
        score += 0.15

    # About/team page links
    links = soup.find_all("a", href=True)
    about_links = [
        a for a in links
        if re.search(r"(about|team|doctor|의료진|소개|원장)", a.get("href", ""), re.I)
        or re.search(r"(소개|의료진|원장|팀|about|team|doctor)", a.get_text(), re.I)
    ]
    details["about_link_count"] = len(about_links)
    if about_links:
        score += 0.15
    else:
        issues.append("의료진/소개 페이지 링크가 없습니다")

    # Schema.org Person/Physician
    json_ld = _extract_json_ld(html)
    types = _get_types(json_ld)
    if {"Person", "Physician"} & types:
        score += 0.1
        details["has_person_schema"] = True

    score = min(1.0, score)

    if score >= 0.6:
        grade = Grade.PASS
    elif score >= 0.3:
        grade = Grade.WARN
    else:
        grade = Grade.FAIL

    return CheckResult(
        name="eeat_signals",
        score=round(score, 2),
        grade=grade,
        display_name=_EEAT_DISPLAY_NAME,
        description=_EEAT_DESCRIPTION,
        recommendation=_EEAT_RECOMMENDATION,
        issues=issues,
        details=details,
    )
