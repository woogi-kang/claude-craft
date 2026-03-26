"""Tests for PDF report generator."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.pdf_generator import (
    CATEGORY_LABELS,
    generate_pdf,
    render_report_html,
)

SAMPLE_AUDIT_DATA = {
    "url": "https://example-hospital.com",
    "total_score": 72,
    "grade": "B",
    "category_scores": {
        "robots_txt": {"score": 100, "grade": "pass", "issues": [], "weight": 0.05},
        "sitemap": {"score": 80, "grade": "pass", "issues": [], "weight": 0.05},
        "meta_tags": {"score": 60, "grade": "warn", "issues": ["title 태그 최적화 필요"], "weight": 0.10},
        "headings": {"score": 40, "grade": "warn", "issues": ["h1 태그 누락"], "weight": 0.05},
        "images_alt": {"score": 20, "grade": "fail", "issues": ["ALT 텍스트 누락"], "weight": 0.05},
        "https": {"score": 100, "grade": "pass", "issues": [], "weight": 0.03},
    },
}


class TestRenderReportHtml:
    def test_returns_html_string(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "<!DOCTYPE html>" in html
        assert "CheckYourHospital" in html

    def test_contains_url(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "https://example-hospital.com" in html

    def test_contains_score_and_grade(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "72" in html
        assert "등급: B" in html

    def test_contains_category_labels(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "Robots.txt" in html
        assert "Meta Tags" in html
        assert "이미지 ALT" in html

    def test_contains_pass_warn_fail_badges(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "통과" in html
        assert "주의" in html
        assert "실패" in html

    def test_contains_top_issues(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "ALT 텍스트 누락" in html

    def test_contains_recommendations(self):
        html = render_report_html(SAMPLE_AUDIT_DATA)
        assert "개선 권고사항" in html
        assert "긴급" in html  # fail items show as 긴급

    def test_empty_scores(self):
        data = {"url": "https://test.com", "total_score": 0, "grade": "F", "category_scores": {}}
        html = render_report_html(data)
        assert "<!DOCTYPE html>" in html
        assert "0" in html


@pytest.mark.asyncio
class TestHtmlToPdf:
    async def test_html_to_pdf_returns_bytes(self):
        """Test Playwright PDF generation with a minimal HTML string."""
        from app.services.pdf_generator import html_to_pdf

        html = "<html><body><h1>Test</h1></body></html>"
        pdf_bytes = await html_to_pdf(html)
        assert isinstance(pdf_bytes, bytes)
        assert len(pdf_bytes) > 0
        # PDF files start with %PDF
        assert pdf_bytes[:4] == b"%PDF"


@pytest.mark.asyncio
class TestGeneratePdf:
    async def test_generate_pdf_full_pipeline(self):
        """Test the full pipeline with mocked Supabase."""
        mock_storage = MagicMock()
        mock_storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://storage.example.com/reports/test-id.pdf"

        mock_client = MagicMock()
        mock_client.storage = mock_storage
        mock_client.table.return_value = mock_client
        mock_client.update.return_value = mock_client
        mock_client.eq.return_value = mock_client
        mock_client.execute.return_value = MagicMock(data=None)

        with patch("app.services.pdf_generator.get_supabase_client", return_value=mock_client):
            url = await generate_pdf("test-audit-id", SAMPLE_AUDIT_DATA)

        assert url == "https://storage.example.com/reports/test-id.pdf"
        mock_storage.from_.assert_called_with("reports")
        mock_storage.upload.assert_called_once()
        # Verify the audit report_url was updated
        mock_client.table.assert_any_call("audits")
