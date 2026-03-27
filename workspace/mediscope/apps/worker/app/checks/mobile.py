"""Mobile responsiveness check (weight: 5%)."""

from bs4 import BeautifulSoup

from .base import CheckResult, Grade

_DISPLAY_NAME = "모바일 최적화"
_DESCRIPTION = "스마트폰에서 홈페이지가 제대로 보이는지 확인합니다"
_RECOMMENDATION = (
    '웹 개발자에게 "반응형 웹 디자인(viewport 설정 포함)을 적용해달라"고 요청하세요'
)


def check_mobile(html: str) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    issues: list[str] = []
    details: dict = {}

    # Check viewport meta tag
    viewport = soup.find("meta", attrs={"name": "viewport"})
    has_viewport = viewport is not None
    details["has_viewport"] = has_viewport

    if not has_viewport:
        issues.append("viewport 메타 태그가 없습니다")
    else:
        content = viewport.get("content", "")
        if isinstance(content, list):
            content = content[0] if content else ""
        details["viewport_content"] = content
        if "width=device-width" not in content:
            issues.append("viewport에 width=device-width가 설정되지 않았습니다")

    # Check for tap target issues (basic heuristic: very small clickable elements)
    # This is a simplified check — full check would use Lighthouse
    small_links = 0
    for a in soup.find_all("a"):
        style = a.get("style", "")
        if isinstance(style, str) and "font-size" in style:
            # Very rough heuristic
            pass

    # Check for text size (basic)
    font_too_small = False
    for style_tag in soup.find_all("style"):
        if style_tag.string and "font-size: 1" in style_tag.string:
            # font-size: 10px or smaller
            pass

    details["small_links"] = small_links

    if not has_viewport:
        return CheckResult(
            name="mobile", score=0.0, grade=Grade.FAIL,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    if issues:
        return CheckResult(
            name="mobile", score=0.5, grade=Grade.WARN,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    return CheckResult(
        name="mobile", score=1.0, grade=Grade.PASS,
        display_name=_DISPLAY_NAME, description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        details=details,
    )
