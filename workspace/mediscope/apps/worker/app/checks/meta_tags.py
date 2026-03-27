"""Meta tags check — title + description (weight: 10%)."""

from bs4 import BeautifulSoup, Tag

from .base import CheckResult, Grade

_DISPLAY_NAME = "검색 결과 미리보기"
_DESCRIPTION = "검색 결과에 보이는 제목과 설명문입니다"
_RECOMMENDATION = (
    '웹 개발자에게 "title 태그에 병원명+진료과목, description에 핵심 강점을 넣어달라"고 요청하세요'
)


def check_meta_tags(html: str, url: str) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    issues: list[str] = []
    details: dict = {}

    # Title
    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else ""
    details["title"] = title_text
    details["title_length"] = len(title_text)

    if not title_text:
        issues.append("title 태그가 없습니다")
    elif len(title_text) > 60:
        issues.append(f"title이 너무 깁니다 ({len(title_text)}자, 권장 60자 이하)")
    elif len(title_text) < 10:
        issues.append(f"title이 너무 짧습니다 ({len(title_text)}자)")

    # Description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc_text = ""
    if isinstance(desc_tag, Tag):
        desc_text = desc_tag.get("content", "") or ""
        if isinstance(desc_text, list):
            desc_text = desc_text[0] if desc_text else ""
    details["description"] = desc_text
    details["description_length"] = len(desc_text)

    if not desc_text:
        issues.append("meta description이 없습니다")
    elif len(desc_text) > 160:
        issues.append(f"description이 너무 깁니다 ({len(desc_text)}자, 권장 160자 이하)")

    # OG tags
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    og_image = soup.find("meta", property="og:image")
    details["has_og_title"] = og_title is not None
    details["has_og_description"] = og_desc is not None
    details["has_og_image"] = og_image is not None

    if not og_title:
        issues.append("og:title이 없습니다")

    # Score
    if not title_text and not desc_text:
        return CheckResult(
            name="meta_tags", score=0.0, grade=Grade.FAIL,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    if issues:
        return CheckResult(
            name="meta_tags", score=0.5, grade=Grade.WARN,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    return CheckResult(
        name="meta_tags", score=1.0, grade=Grade.PASS,
        display_name=_DISPLAY_NAME, description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        details=details,
    )
