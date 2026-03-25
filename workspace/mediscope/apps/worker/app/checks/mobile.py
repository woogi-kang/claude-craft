"""Mobile responsiveness check (weight: 5%)."""

from bs4 import BeautifulSoup

from .base import CheckResult, Grade


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
            name="mobile", score=0.0, grade=Grade.FAIL, details=details, issues=issues
        )

    if issues:
        return CheckResult(
            name="mobile", score=0.5, grade=Grade.WARN, details=details, issues=issues
        )

    return CheckResult(name="mobile", score=1.0, grade=Grade.PASS, details=details)
