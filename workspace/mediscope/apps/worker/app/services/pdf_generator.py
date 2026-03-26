"""PDF report generator: Jinja2 HTML → Playwright PDF → Supabase Storage."""

import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from ..config import settings
from ..db.supabase import get_supabase_client

logger = logging.getLogger("mediscope.pdf")

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=True,
)


def _grade_color(grade: str) -> str:
    return {
        "A": "#166534",
        "B": "#1e40af",
        "C": "#854d0e",
    }.get(grade, "#991b1b")


def _grade_bg(grade: str) -> str:
    return {
        "A": "#dcfce7",
        "B": "#dbeafe",
        "C": "#fef9c3",
    }.get(grade, "#fee2e2")


def _badge_label(grade: str) -> str:
    return {"pass": "통과", "warn": "주의", "fail": "실패"}.get(grade, grade)


def _bar_color(grade: str) -> str:
    return {"pass": "#22c55e", "warn": "#eab308", "fail": "#ef4444"}.get(grade, "#94a3b8")


CATEGORY_LABELS: dict[str, str] = {
    "robots_txt": "Robots.txt",
    "sitemap": "Sitemap",
    "meta_tags": "Meta Tags",
    "headings": "Heading 구조",
    "images_alt": "이미지 ALT",
    "links": "내부 링크",
    "https": "HTTPS",
    "canonical": "Canonical",
    "url_structure": "URL 구조",
    "errors_404": "404/리다이렉트",
    "lcp": "LCP",
    "inp": "INP",
    "cls": "CLS",
    "performance_score": "성능 점수",
    "mobile": "모바일 반응형",
    "structured_data": "구조화 데이터",
    "faq_content": "FAQ 콘텐츠",
    "ai_search_mention": "AI 검색 노출",
    "eeat_signals": "E-E-A-T 신호",
    "content_clarity": "콘텐츠 명확성",
    "geo_aeo": "GEO/AEO",
    "multilingual": "다국어 지원",
    "competitiveness": "경쟁력",
}


def render_report_html(audit_data: dict) -> str:
    """Render audit data into an HTML string using Jinja2 template."""
    scores = audit_data.get("category_scores", audit_data.get("scores", {}))

    items = []
    for key, val in scores.items():
        if isinstance(val, dict):
            score = val.get("score", 0) or 0
            grade = val.get("grade", "skip")
            issues = val.get("issues", [])
        else:
            score = val if isinstance(val, (int, float)) else 0
            grade = "pass" if score >= 80 else "warn" if score >= 40 else "fail"
            issues = []
        items.append({
            "key": key,
            "label": CATEGORY_LABELS.get(key, key),
            "score": round(score) if score is not None else 0,
            "grade": grade,
            "grade_label": _badge_label(grade),
            "bar_color": _bar_color(grade),
            "first_issue": issues[0] if issues else "—",
        })

    pass_count = sum(1 for i in items if i["grade"] == "pass")
    warn_count = sum(1 for i in items if i["grade"] == "warn")
    fail_count = sum(1 for i in items if i["grade"] == "fail")

    total_score = audit_data.get("total_score", 0) or 0
    grade = audit_data.get("grade", "F")

    # Top 3 issues: pick fail items first, then warn items
    top_issues = []
    for i in items:
        if i["grade"] == "fail" and i["first_issue"] != "—":
            top_issues.append({"label": i["label"], "issue": i["first_issue"]})
    for i in items:
        if i["grade"] == "warn" and i["first_issue"] != "—":
            top_issues.append({"label": i["label"], "issue": i["first_issue"]})
    top_issues = top_issues[:3]

    # Recommendations sorted by priority (fail first)
    priority_order = {"fail": 0, "warn": 1, "pass": 2, "skip": 3}
    recommendations = sorted(
        [i for i in items if i["grade"] in ("fail", "warn")],
        key=lambda x: priority_order.get(x["grade"], 99),
    )

    now = datetime.now()
    report_date = f"{now.year}년 {now.month}월 {now.day}일"

    template = _jinja_env.get_template("report.html")
    return template.render(
        url=audit_data.get("url", ""),
        report_date=report_date,
        total_score=total_score,
        grade=grade,
        grade_color=_grade_color(grade),
        grade_bg=_grade_bg(grade),
        items=items,
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
        top_issues=top_issues,
        recommendations=recommendations,
    )


async def html_to_pdf(html: str) -> bytes:
    """Convert HTML string to PDF bytes using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html, wait_until="networkidle")
        pdf_bytes = await page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "10mm", "right": "10mm", "bottom": "10mm", "left": "10mm"},
        )
        await browser.close()
    return pdf_bytes


def upload_to_storage(audit_id: str, pdf_bytes: bytes) -> str:
    """Upload PDF to Supabase Storage and return public URL."""
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase client not configured")

    bucket = settings.supabase_storage_bucket
    file_path = f"{audit_id}.pdf"

    # Upload (upsert to overwrite if re-generated)
    client.storage.from_(bucket).upload(
        file_path,
        pdf_bytes,
        file_options={"content-type": "application/pdf", "upsert": "true"},
    )

    # Get public URL
    public_url = client.storage.from_(bucket).get_public_url(file_path)
    return public_url


def update_audit_report_url(audit_id: str, url: str) -> None:
    """Update audits.report_url with the generated PDF URL."""
    client = get_supabase_client()
    if client is None:
        return
    client.table("audits").update({"report_url": url}).eq("id", audit_id).execute()


async def generate_pdf(audit_id: str, audit_data: dict) -> str:
    """Generate PDF report: render HTML → convert to PDF → upload → update DB.

    Returns the public URL of the generated PDF.
    """
    logger.info(f"Generating PDF for audit_id={audit_id}")

    # 1. Render HTML from audit data
    html = render_report_html(audit_data)

    # 2. Convert HTML to PDF via Playwright
    pdf_bytes = await html_to_pdf(html)
    logger.info(f"PDF generated: {len(pdf_bytes)} bytes")

    # 3. Upload to Supabase Storage
    pdf_url = upload_to_storage(audit_id, pdf_bytes)

    # 4. Update audits.report_url
    update_audit_report_url(audit_id, pdf_url)

    logger.info(f"PDF uploaded: {pdf_url}")
    return pdf_url
