"""Doctor information extraction helpers for agent-based deep crawl."""

from __future__ import annotations

import re
from urllib.parse import urljoin

from clinic_crawl.models.doctor import DoctorCredential, DoctorInfo
from clinic_crawl.models.enums import DoctorRole

# Menu label patterns for doctor pages (Korean and English)
DOCTOR_MENU_KEYWORDS = [
    "의료진",
    "원장",
    "전문의",
    "의료팀",
    "의사",
    "진료진",
    "대표원장",
    "원장님",
    "doctor",
    "staff",
    "team",
    "about",
    "의료진소개",
    "의료진 소개",
    "원장소개",
    "원장 소개",
    "전문의소개",
]

# Role detection patterns
ROLE_PATTERNS: list[tuple[str, DoctorRole]] = [
    (r"대표\s*원장", DoctorRole.DIRECTOR),
    (r"원장", DoctorRole.DIRECTOR),
    (r"전문의", DoctorRole.SPECIALIST),
    (r"전공의|레지던트", DoctorRole.RESIDENT),
    (r"간호사|간호", DoctorRole.NURSE),
    (r"(?:피부|성형)\s*(?:외)?과\s*전문의", DoctorRole.SPECIALIST),
]

# Credential extraction patterns
CREDENTIAL_PATTERNS = [
    (r"(피부(?:과|외과)?\s*전문의)", "전문의"),
    (r"(성형외과\s*전문의)", "전문의"),
    (r"(대한[^\s]+학회\s*(?:정회원|인증의|회원))", "학회"),
    (r"(미국[^\s]+(?:학회|Board)\s*(?:인증|Fellow))", "학회"),
    (r"(\w+대학교?\s*의과대학\s*(?:졸업)?)", "학력"),
    (r"(\w+대학교?\s*(?:의학)?대학원\s*(?:석사|박사|졸업)?)", "학력"),
    (r"(\w+병원\s*(?:인턴|레지던트|전공의|전임의|수련))", "경력"),
]


def detect_role(text: str) -> DoctorRole:
    """Detect doctor's role from surrounding text."""
    for pattern, role in ROLE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return role
    return DoctorRole.SPECIALIST


def extract_credentials(text: str) -> list[DoctorCredential]:
    """Extract credentials from a doctor's profile text."""
    credentials: list[DoctorCredential] = []
    seen: set[str] = set()

    for pattern, cred_type in CREDENTIAL_PATTERNS:
        for match in re.finditer(pattern, text):
            value = match.group(1).strip()
            if value not in seen:
                seen.add(value)
                credentials.append(
                    DoctorCredential(credential_type=cred_type, value=value)
                )

    return credentials


def extract_education(text: str) -> list[str]:
    """Extract education history from text."""
    education: list[str] = []
    # Split by newlines or bullet points
    lines = re.split(r"[\n\r]+|[·•\-]\s*", text)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Match education-related keywords
        if re.search(r"대학|대학원|졸업|학사|석사|박사|의학과|의과", line):
            education.append(line)
    return education


def extract_career(text: str) -> list[str]:
    """Extract career history from text."""
    career: list[str] = []
    lines = re.split(r"[\n\r]+|[·•\-]\s*", text)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Match career-related keywords
        if re.search(r"병원|클리닉|의원|센터|인턴|레지던트|전공의|전임의|수련|근무|재직", line):
            career.append(line)
    return career


def resolve_photo_url(src: str | None, base_url: str) -> str | None:
    """Resolve a photo URL relative to the base URL."""
    if not src:
        return None
    if src.startswith("data:"):
        return None  # Skip data URIs
    if src.startswith("http"):
        return src
    return urljoin(base_url, src)


def parse_doctor_section(
    html_section: str,
    base_url: str,
) -> DoctorInfo:
    """Parse a single doctor's HTML section into a DoctorInfo.

    This is a best-effort parser that looks for common patterns.
    The agent may need to refine this per-site.
    """
    # Try to find name (usually in a heading or strong tag)
    name = None
    name_match = re.search(
        r"<(?:h[1-6]|strong|b|span[^>]*class[^>]*name)[^>]*>([^<]{2,20})</",
        html_section,
        re.IGNORECASE,
    )
    if name_match:
        name = name_match.group(1).strip()

    # Find photo
    photo_url = None
    img_match = re.search(
        r'<img[^>]+(?:src|data-src)\s*=\s*["\']([^"\']+)["\']',
        html_section,
        re.IGNORECASE,
    )
    if img_match:
        photo_url = resolve_photo_url(img_match.group(1), base_url)

    # Extract text content for analysis
    text = re.sub(r"<[^>]+>", " ", html_section)
    text = re.sub(r"\s+", " ", text).strip()

    role = detect_role(text)
    credentials = extract_credentials(text)
    education = extract_education(text)
    career = extract_career(text)

    return DoctorInfo(
        name=name,
        role=role,
        photo_url=photo_url,
        credentials=credentials,
        education=education,
        career=career,
    )


def is_doctor_menu_link(text: str) -> bool:
    """Check if a menu link text likely leads to a doctor page."""
    text_lower = text.lower().strip()
    return any(kw.lower() in text_lower for kw in DOCTOR_MENU_KEYWORDS)
