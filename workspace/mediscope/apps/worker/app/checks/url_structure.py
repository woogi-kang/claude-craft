"""URL structure check (weight: 4%)."""

import re
from urllib.parse import urlparse

from .base import CheckResult, Grade


def check_url_structure(url: str, crawled_urls: list[str] | None = None) -> CheckResult:
    issues: list[str] = []
    urls_to_check = crawled_urls or [url]
    details: dict = {"urls_checked": len(urls_to_check)}

    bad_patterns = 0
    deep_urls = 0

    for u in urls_to_check:
        parsed = urlparse(u)
        path = parsed.path

        # Check depth (more than 4 levels)
        depth = len([p for p in path.split("/") if p])
        if depth > 4:
            deep_urls += 1

        # Check for query parameters in main content URLs
        if parsed.query and not any(
            skip in parsed.query for skip in ["utm_", "fbclid", "gclid"]
        ):
            bad_patterns += 1

        # Check for non-clean URLs
        if re.search(r"\.(php|asp|aspx|jsp)\?", u):
            bad_patterns += 1

        # Check for IDs in URL
        if re.search(r"/\d{5,}(/|$)", path):
            bad_patterns += 1

    details["deep_urls"] = deep_urls
    details["bad_patterns"] = bad_patterns

    if deep_urls > 0:
        issues.append(f"URL 깊이가 4단계를 초과하는 URL이 {deep_urls}개 있습니다")

    if bad_patterns > 0:
        issues.append(f"깔끔하지 않은 URL 패턴이 {bad_patterns}개 있습니다")

    total = len(urls_to_check)
    problem_ratio = (deep_urls + bad_patterns) / max(total, 1)

    if problem_ratio > 0.5:
        return CheckResult(
            name="url_structure", score=0.0, grade=Grade.FAIL, details=details, issues=issues
        )

    if issues:
        return CheckResult(
            name="url_structure", score=0.5, grade=Grade.WARN, details=details, issues=issues
        )

    return CheckResult(name="url_structure", score=1.0, grade=Grade.PASS, details=details)
