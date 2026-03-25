"""Canonical tag check (weight: 3%)."""

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .base import CheckResult, Grade


def check_canonical(html: str, url: str) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    issues: list[str] = []

    canonical = soup.find("link", rel="canonical")
    details: dict = {"has_canonical": canonical is not None}

    if not canonical:
        issues.append("canonical 태그가 없습니다")
        return CheckResult(
            name="canonical", score=0.0, grade=Grade.FAIL, details=details, issues=issues
        )

    href = canonical.get("href", "")
    if isinstance(href, list):
        href = href[0] if href else ""
    details["canonical_url"] = href

    if not href:
        issues.append("canonical 태그에 href가 없습니다")
        return CheckResult(
            name="canonical", score=0.0, grade=Grade.FAIL, details=details, issues=issues
        )

    # Check if canonical points to itself (good) or elsewhere
    parsed_url = urlparse(url)
    parsed_canonical = urlparse(href)

    if parsed_canonical.netloc and parsed_canonical.netloc != parsed_url.netloc:
        issues.append(f"canonical이 다른 도메인을 가리킵니다: {href}")

    if issues:
        return CheckResult(
            name="canonical", score=0.5, grade=Grade.WARN, details=details, issues=issues
        )

    return CheckResult(name="canonical", score=1.0, grade=Grade.PASS, details=details)
