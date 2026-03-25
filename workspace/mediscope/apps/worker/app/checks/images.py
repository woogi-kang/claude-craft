"""Image ALT tag check (weight: 5%)."""

from bs4 import BeautifulSoup

from .base import CheckResult, Grade


def check_images(html: str) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    images = soup.find_all("img")
    total = len(images)

    if total == 0:
        return CheckResult(
            name="images_alt",
            score=1.0,
            grade=Grade.PASS,
            details={"total_images": 0, "with_alt": 0},
        )

    with_alt = 0
    generic_alt = 0
    issues: list[str] = []

    for img in images:
        alt = img.get("alt")
        if alt and str(alt).strip():
            with_alt += 1
            # Check for generic/meaningless alt
            alt_lower = str(alt).strip().lower()
            if alt_lower in ("image", "img", "photo", "picture", "사진", "이미지"):
                generic_alt += 1
        # Check for generic filenames
        src = img.get("src", "")
        if isinstance(src, str) and any(p in src.lower() for p in ["img_", "dsc_", "screenshot"]):
            issues.append(f"의미 없는 파일명: {src[:60]}")

    alt_ratio = with_alt / total
    details = {
        "total_images": total,
        "with_alt": with_alt,
        "alt_ratio": round(alt_ratio, 2),
        "generic_alt_count": generic_alt,
    }

    if alt_ratio < 0.6:
        issues.insert(0, f"ALT 태그 존재율이 낮습니다 ({alt_ratio:.0%})")
        return CheckResult(name="images_alt", score=0.0, grade=Grade.FAIL, details=details, issues=issues)

    if alt_ratio < 0.9 or generic_alt > total * 0.2:
        if alt_ratio < 0.9:
            issues.insert(0, f"ALT 태그 존재율: {alt_ratio:.0%} (90% 이상 권장)")
        return CheckResult(name="images_alt", score=0.5, grade=Grade.WARN, details=details, issues=issues)

    return CheckResult(name="images_alt", score=1.0, grade=Grade.PASS, details=details)
