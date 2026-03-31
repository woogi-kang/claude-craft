"""Tests for image generator service."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.image_generator import (
    ImageType,
    IMAGE_TYPE_DEFAULTS,
    TEMPLATE_FILES,
    list_templates,
    render_image_html,
)


# --- Sample data fixtures ---

SAMPLE_INFOGRAPHIC_DATA = {
    "clinic_name": "미소클리닉",
    "steps": [
        {"title": "상담", "duration": "15분", "description": "전문의와 1:1 상담", "icon": "🩺"},
        {"title": "마취", "duration": "10분", "description": "국소 마취 적용", "icon": "💉"},
        {"title": "시술", "duration": "30분", "description": "레이저 시술 진행", "icon": "✨"},
        {"title": "관리", "duration": "15분", "description": "시술 후 쿨링 및 관리", "icon": "❄️"},
    ],
    "total_duration": "약 70분",
    "downtime": "3-5일",
    "side_effects": "경미한 홍조",
}

SAMPLE_SNS_DATA = {
    "category": "피부 시술",
    "description": "마이크로 니들링 기반 피부 재생 시술로, 콜라겐 생성을 촉진합니다.",
    "duration": "30분",
    "downtime": "3-5일",
    "pain_level": 2,
    "clinic_name": "미소클리닉",
    "website": "www.example.com",
}

SAMPLE_COMPARISON_DATA = {
    "prices": [
        {"country": "한국", "country_flag": "🇰🇷", "price": 300, "price_formatted": "$300", "highlight": True},
        {"country": "일본", "country_flag": "🇯🇵", "price": 500, "price_formatted": "$500"},
        {"country": "미국", "country_flag": "🇺🇸", "price": 800, "price_formatted": "$800"},
        {"country": "중국", "country_flag": "🇨🇳", "price": 450, "price_formatted": "$450"},
    ],
    "summary": "한국이 일본 대비 40% 저렴합니다",
    "source": "2024년 평균 시술 가격 기준",
}

SAMPLE_BANNER_DATA = {
    "tag": "Medical Tourism",
    "headline": "韓国でポテンツァ — 日本の60%の費用で",
    "subheadline": "東京から2時間。最新の医療技術を手頃な価格で。",
    "cta": "今すぐ相談する",
    "price": "¥35,000~",
    "original_price": "¥60,000",
}

SAMPLE_SUMMARY_DATA = {
    "pain_level": 2,
    "pain_description": "경미한 따끔거림",
    "duration": "30분",
    "duration_detail": "마취 포함",
    "downtime": "3-5일",
    "downtime_detail": "일상생활 가능",
    "price_range": "30-50만원",
    "price_detail": "부위/횟수에 따라 상이",
    "note": "※ 개인 차이가 있을 수 있습니다",
}


class TestRenderImageHtml:
    """Test HTML template rendering with Jinja2."""

    def test_infographic_renders(self):
        html = render_image_html(ImageType.INFOGRAPHIC, "포텐자", SAMPLE_INFOGRAPHIC_DATA)
        assert "<!DOCTYPE html>" in html
        assert "포텐자" in html
        assert "상담" in html
        assert "마취" in html
        assert "시술" in html
        assert "관리" in html

    def test_sns_card_renders(self):
        html = render_image_html(ImageType.SNS_CARD, "포텐자", SAMPLE_SNS_DATA)
        assert "<!DOCTYPE html>" in html
        assert "포텐자" in html
        assert "이란?" in html
        assert "30분" in html
        assert "●●○○○" in html

    def test_comparison_chart_renders(self):
        html = render_image_html(ImageType.COMPARISON_CHART, "포텐자", SAMPLE_COMPARISON_DATA)
        assert "<!DOCTYPE html>" in html
        assert "포텐자" in html
        assert "한국" in html
        assert "$300" in html
        assert "40% 저렴" in html

    def test_banner_renders(self):
        html = render_image_html(ImageType.BANNER, "ポテンツァ", SAMPLE_BANNER_DATA, language="ja")
        assert "<!DOCTYPE html>" in html
        assert "ポテンツァ" in html
        assert "¥35,000~" in html
        assert "今すぐ相談する" in html

    def test_procedure_summary_renders(self):
        html = render_image_html(ImageType.PROCEDURE_SUMMARY, "포텐자", SAMPLE_SUMMARY_DATA)
        assert "<!DOCTYPE html>" in html
        assert "포텐자" in html
        assert "30분" in html
        assert "30-50만원" in html

    def test_multilingual_korean(self):
        html = render_image_html(ImageType.SNS_CARD, "포텐자", SAMPLE_SNS_DATA, language="ko")
        assert "시술 시간" in html
        assert "다운타임" in html

    def test_multilingual_japanese(self):
        html = render_image_html(ImageType.SNS_CARD, "ポテンツァ", SAMPLE_SNS_DATA, language="ja")
        assert "施術時間" in html
        assert "ダウンタイム" in html

    def test_multilingual_chinese(self):
        html = render_image_html(ImageType.SNS_CARD, "射频微针", SAMPLE_SNS_DATA, language="zh")
        assert "手术时间" in html
        assert "恢复期" in html

    def test_multilingual_english(self):
        html = render_image_html(ImageType.SNS_CARD, "Potenza", SAMPLE_SNS_DATA, language="en")
        assert "Duration" in html
        assert "Downtime" in html

    def test_empty_data(self):
        html = render_image_html(ImageType.SNS_CARD, "Test", {})
        assert "<!DOCTYPE html>" in html
        assert "Test" in html

    def test_comparison_empty_prices(self):
        html = render_image_html(ImageType.COMPARISON_CHART, "Test", {"prices": []})
        assert "<!DOCTYPE html>" in html


class TestImageTypeDefaults:
    """Test image type configuration."""

    def test_all_types_have_defaults(self):
        for img_type in ImageType:
            assert img_type in IMAGE_TYPE_DEFAULTS

    def test_all_types_have_templates(self):
        for img_type in ImageType:
            assert img_type in TEMPLATE_FILES

    def test_infographic_size(self):
        assert IMAGE_TYPE_DEFAULTS[ImageType.INFOGRAPHIC] == (1080, 1350)

    def test_sns_card_size(self):
        assert IMAGE_TYPE_DEFAULTS[ImageType.SNS_CARD] == (1080, 1080)

    def test_banner_size(self):
        assert IMAGE_TYPE_DEFAULTS[ImageType.BANNER] == (1200, 630)


class TestListTemplates:
    def test_returns_all_types(self):
        templates = list_templates()
        assert len(templates) == len(ImageType)

    def test_template_structure(self):
        templates = list_templates()
        for t in templates:
            assert "type" in t
            assert "name" in t
            assert "default_width" in t
            assert "default_height" in t


@pytest.mark.slow
@pytest.mark.asyncio
class TestImageGeneration:
    """Integration tests requiring Playwright."""

    async def test_generate_infographic(self):
        from app.services.image_generator import generate_image

        png = await generate_image(
            ImageType.INFOGRAPHIC, "포텐자", SAMPLE_INFOGRAPHIC_DATA
        )
        assert isinstance(png, bytes)
        assert len(png) > 0
        # PNG magic bytes
        assert png[:4] == b"\x89PNG"

    async def test_generate_sns_card(self):
        from app.services.image_generator import generate_image

        png = await generate_image(
            ImageType.SNS_CARD, "포텐자", SAMPLE_SNS_DATA
        )
        assert isinstance(png, bytes)
        assert png[:4] == b"\x89PNG"

    async def test_generate_with_custom_size(self):
        from app.services.image_generator import generate_image

        png = await generate_image(
            ImageType.SNS_CARD, "Test", SAMPLE_SNS_DATA, width=500, height=500
        )
        assert isinstance(png, bytes)
        assert png[:4] == b"\x89PNG"


@pytest.mark.asyncio
class TestImageApi:
    """Test image API endpoints."""

    async def test_get_templates(self, test_client, auth_headers):
        resp = await test_client.get("/worker/content/image/templates", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "templates" in data
        assert len(data["templates"]) == len(ImageType)

    async def test_generate_image_returns_png(self, test_client, auth_headers):
        with patch("app.services.image_generator.html_to_screenshot") as mock_screenshot:
            mock_screenshot.return_value = b"\x89PNG\r\n\x1a\nfakedata"
            resp = await test_client.post(
                "/worker/content/image",
                json={
                    "image_type": "sns_card",
                    "procedure_name": "포텐자",
                    "data": SAMPLE_SNS_DATA,
                },
                headers=auth_headers,
            )
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "image/png"
        assert resp.content[:4] == b"\x89PNG"

    async def test_generate_image_upload(self, test_client, auth_headers):
        mock_storage = MagicMock()
        mock_storage.from_.return_value = mock_storage
        mock_storage.upload.return_value = None
        mock_storage.get_public_url.return_value = "https://storage.example.com/img.png"

        mock_client = MagicMock()
        mock_client.storage = mock_storage

        with (
            patch("app.services.image_generator.html_to_screenshot") as mock_screenshot,
            patch("app.services.image_generator.get_supabase_client", return_value=mock_client),
        ):
            mock_screenshot.return_value = b"\x89PNG\r\n\x1a\nfakedata"
            resp = await test_client.post(
                "/worker/content/image",
                json={
                    "image_type": "banner",
                    "procedure_name": "포텐자",
                    "data": SAMPLE_BANNER_DATA,
                    "language": "ja",
                    "upload": True,
                },
                headers=auth_headers,
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["url"] == "https://storage.example.com/img.png"
        assert "filename" in data

    async def test_generate_image_no_auth(self, test_client):
        resp = await test_client.post(
            "/worker/content/image",
            json={"image_type": "sns_card", "procedure_name": "Test", "data": {}},
        )
        assert resp.status_code == 401

    async def test_invalid_image_type(self, test_client, auth_headers):
        resp = await test_client.post(
            "/worker/content/image",
            json={"image_type": "invalid_type", "procedure_name": "Test", "data": {}},
            headers=auth_headers,
        )
        assert resp.status_code == 422
