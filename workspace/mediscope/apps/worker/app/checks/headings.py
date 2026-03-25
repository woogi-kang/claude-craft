"""Heading structure check (weight: 5%)."""

from bs4 import BeautifulSoup

from .base import CheckResult, Grade


def check_headings(html: str) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    issues: list[str] = []

    h1_tags = soup.find_all("h1")
    h1_count = len(h1_tags)
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))

    details = {"h1_count": h1_count, "h2_count": h2_count, "h3_count": h3_count}

    if h1_count == 0:
        issues.append("H1 태그가 없습니다")
        return CheckResult(name="headings", score=0.0, grade=Grade.FAIL, details=details, issues=issues)

    if h1_count > 1:
        issues.append(f"H1 태그가 {h1_count}개입니다 (1개 권장)")

    if h1_count >= 3:
        issues.append("H1 태그가 과다합니다 (3개 이상)")

    # Check hierarchy: H1 should come before H2
    all_headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    if len(all_headings) >= 2:
        levels = [int(h.name[1]) for h in all_headings]
        for i in range(1, len(levels)):
            if levels[i] - levels[i - 1] > 1:
                issues.append(f"헤딩 계층 건너뜀: H{levels[i-1]} → H{levels[i]}")
                break

    if issues:
        return CheckResult(name="headings", score=0.5, grade=Grade.WARN, details=details, issues=issues)

    return CheckResult(name="headings", score=1.0, grade=Grade.PASS, details=details)
