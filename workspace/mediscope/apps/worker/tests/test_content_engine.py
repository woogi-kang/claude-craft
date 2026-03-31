"""Tests for content engine — template fallback, SEO scoring, compliance filtering."""

import os
from unittest.mock import MagicMock, patch

import pytest

# Set env vars before importing app modules
os.environ.setdefault("WORKER_API_KEY", "test-key")
os.environ.setdefault("SUPABASE_URL", "")
os.environ.setdefault("SUPABASE_SECRET_KEY", "")

from app.services.content_engine import (
    ContentLanguage,
    ContentType,
    calculate_seo_score,
    filter_compliance,
    generate_content,
    get_supported_content_types,
    get_supported_languages,
)
from app.services.procedure_data import ProcedureData

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_procedure() -> ProcedureData:
    return ProcedureData(
        name="포텐자",
        name_en="Potenza",
        category="리프팅/타이트닝",
        principle="RF 마이크로니들을 이용한 피부 재생 시술",
        mechanism_detail="고주파 에너지를 피부 진피층에 전달하여 콜라겐 생성을 촉진합니다.",
        method="마취 크림 도포 후 RF 마이크로니들로 시술 부위를 치료합니다.",
        duration="30-60분",
        side_effects="일시적 붉어짐, 부종, 가벼운 통증이 있을 수 있습니다.",
        pain_level="3",
        pain_description="마취 크림 적용 시 통증은 미미합니다.",
        downtime="1-3일",
        post_care="시술 후 24시간 세안 자제, 자외선 차단제 필수 사용",
        average_price="30-50만원",
        target="모공, 흉터, 주름 개선이 필요한 분",
        effect="피부 탄력 개선, 모공 축소, 흉터 개선",
        advantage="기존 RF 시술 대비 정밀한 깊이 조절 가능",
        not_recommended="임산부, 켈로이드 체질, 피부 염증이 있는 분",
        summary="포텐자는 RF 마이크로니들 기반의 피부 재생 시술입니다.",
        price_by_country={
            "us": {"currency": "USD", "price": 800, "price_unit": "per session"},
            "jp": {"currency": "JPY", "price": 80000, "price_unit": "1回"},
            "kr": {"currency": "KRW", "price": 400000, "price_unit": "1회"},
        },
        translations={
            "en": {
                "translated_name": "Potenza RF Microneedling",
                "principle": "RF microneedling skin regeneration treatment",
            },
            "ja": {
                "translated_name": "ポテンザ",
                "principle": "RFマイクロニードルによる肌再生施術",
            },
        },
    )


# ---------------------------------------------------------------------------
# SEO Score tests
# ---------------------------------------------------------------------------

class TestSEOScore:
    def test_perfect_content_scores_high(self):
        content = """
<h2>포텐자 시술 완벽 가이드</h2>
<p>포텐자 시술에 대해 알아보겠습니다. 포텐자는 RF 마이크로니들을 이용한 시술입니다.</p>
<h2>시술 과정</h2>
<p>포텐자 시술은 마취 후 진행됩니다.</p>
<h3>1단계: 상담</h3>
<p>전문의와 상담합니다.</p>
<h3>2단계: 시술</h3>
<p>포텐자 시술을 진행합니다.</p>
<h2>부작용</h2>
<p>일시적 붉어짐이 있을 수 있습니다.</p>
<h2>FAQ</h2>
<p>자주 묻는 질문</p>
<a href="/about">의료진 소개</a>
<a href="/services">시술 안내</a>
<a href="/contact">상담 예약</a>
""" + ("포텐자 피부 재생 시술 " * 100)  # Pad for word count

        score = calculate_seo_score(
            content=content,
            title="포텐자 시술 완벽 가이드 - 강남 A피부과",
            meta_description=(
                "포텐자 RF 마이크로니들 시술 가이드. 원리, 과정, 비용, 부작용 안내. "
                "강남 A피부과에서 전문의 상담 후 시술을 결정하세요."
            ),
            target_keywords=["포텐자", "피부 재생"],
        )
        assert score >= 70

    def test_empty_content_scores_low(self):
        score = calculate_seo_score(
            content="", title="", meta_description="", target_keywords=["test"]
        )
        assert score < 30

    def test_title_length_scoring(self):
        title = "좋은 타이틀 길이 30자 이상 60자 이하입니다 완벽합니다 예시 텍스트"
        good = calculate_seo_score("x" * 2000, title, "", [])
        bad = calculate_seo_score("x" * 2000, "짧", "", [])
        assert good > bad

    def test_no_keywords_gives_partial_credit(self):
        score = calculate_seo_score("x" * 2000, "Title Here", "desc", None)
        assert score > 0

    def test_faq_section_detected(self):
        with_faq = calculate_seo_score(
            "<h2>FAQ</h2><p>자주 묻는 질문</p>" + "x" * 2000, "Title", "Desc", []
        )
        without_faq = calculate_seo_score("x" * 2000, "Title", "Desc", [])
        assert with_faq > without_faq


# ---------------------------------------------------------------------------
# Compliance filter tests
# ---------------------------------------------------------------------------

class TestComplianceFilter:
    def test_removes_exaggeration(self):
        content = "이 시술은 최고의 효과를 보장합니다."
        filtered, warnings = filter_compliance(content, "ko")
        assert "최고" not in filtered
        assert "보장" not in filtered
        assert len(warnings) >= 2

    def test_removes_discount_claims(self):
        content = "무료 시술 이벤트! 70% 할인 진행중"
        filtered, warnings = filter_compliance(content, "ko")
        assert "무료 시술" not in filtered
        assert len(warnings) >= 1

    def test_inserts_required_disclaimer(self):
        content = "포텐자 시술 소개입니다."
        filtered, warnings = filter_compliance(content, "ko")
        assert "개인에 따라 결과가 다를 수 있습니다" in filtered
        assert any("필수 고지문" in w for w in warnings)

    def test_skips_disclaimer_if_present(self):
        content = "포텐자 시술 소개입니다. 개인에 따라 결과가 다를 수 있습니다."
        filtered, warnings = filter_compliance(content, "ko")
        assert not any("필수 고지문" in w for w in warnings)

    def test_no_filtering_for_english(self):
        content = "This is the best treatment with 100% guarantee."
        filtered, warnings = filter_compliance(content, "en")
        assert filtered == content
        assert warnings == []

    def test_comparison_expressions_removed(self):
        content = "가장 효과적인 시술입니다. 업계 최초 도입."
        filtered, warnings = filter_compliance(content, "ko")
        assert "업계 최초" not in filtered


# ---------------------------------------------------------------------------
# Fallback content generation tests
# ---------------------------------------------------------------------------

class TestFallbackGeneration:
    @patch("app.services.content_engine.get_procedure_data")
    async def test_blog_post_generation(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="포텐자",
            hospital_name="테스트피부과",
            hospital_region="강남",
            target_keywords=["포텐자", "RF 마이크로니들"],
        )

        assert result["content_type"] == "blog_post"
        assert result["language"] == "ko"
        assert "포텐자" in result["title"]
        assert len(result["content"]) > 500
        assert result["seo_score"] > 0
        assert result["word_count"] > 0
        assert result["schema_markup"]
        assert result["generated_at"]

    @patch("app.services.content_engine.get_procedure_data")
    async def test_faq_generation(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.FAQ,
            procedure_name="포텐자",
        )

        assert result["content_type"] == "faq"
        assert "Q." in result["content"]
        assert "A." in result["content"]
        # FAQ should have schema.org markup in content
        assert "FAQPage" in result["content"]

    @patch("app.services.content_engine.get_procedure_data")
    async def test_procedure_page_generation(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.PROCEDURE_PAGE,
            procedure_name="포텐자",
            target_language=ContentLanguage.EN,
        )

        assert result["content_type"] == "procedure_page"
        assert result["language"] == "en"
        # Should use English translation
        assert "Potenza" in result["content"] or "포텐자" in result["content"]

    @patch("app.services.content_engine.get_procedure_data")
    async def test_sns_set_generation(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.SNS_SET,
            procedure_name="포텐자",
        )

        assert result["content_type"] == "sns_set"
        # Should have Instagram, Naver Blog, Xiaohongshu
        content = result["content"]
        assert "인스타그램" in content
        assert "네이버" in content
        assert "小红书" in content

    @patch("app.services.content_engine.get_procedure_data")
    async def test_medical_guide_generation(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.MEDICAL_GUIDE,
            procedure_name="포텐자",
            target_language=ContentLanguage.EN,
        )

        assert result["content_type"] == "medical_guide"
        assert "Korea" in result["content"]
        assert "Timeline" in result["content"] or "timeline" in result["content"].lower()

    @patch("app.services.content_engine.get_procedure_data")
    async def test_generation_with_no_db_data(self, mock_get_proc):
        mock_get_proc.return_value = None

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="레이저토닝",
        )

        assert result["content_type"] == "blog_post"
        assert "레이저토닝" in result["content"]
        assert result["source_data"]["procedure"] == "레이저토닝"


# ---------------------------------------------------------------------------
# Content type structure tests
# ---------------------------------------------------------------------------

class TestContentStructure:
    @patch("app.services.content_engine.get_procedure_data")
    async def test_response_has_all_fields(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="포텐자",
        )

        required_fields = [
            "content_type", "title", "content", "meta_title",
            "meta_description", "seo_score", "word_count", "language",
            "schema_markup", "compliance_warnings", "generated_at",
            "source_data",
        ]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"

    @patch("app.services.content_engine.get_procedure_data")
    async def test_meta_title_length_limit(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="포텐자",
            hospital_name="아주긴이름의피부과병원이름입니다정말긴이름",
        )

        assert len(result["meta_title"]) <= 60

    @patch("app.services.content_engine.get_procedure_data")
    async def test_meta_description_length(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="포텐자",
        )

        assert len(result["meta_description"]) <= 160


# ---------------------------------------------------------------------------
# Multilingual tests
# ---------------------------------------------------------------------------

class TestMultilingual:
    @patch("app.services.content_engine.get_procedure_data")
    async def test_korean_content(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.BLOG_POST,
            procedure_name="포텐자",
            target_language=ContentLanguage.KO,
        )
        assert result["language"] == "ko"

    @patch("app.services.content_engine.get_procedure_data")
    async def test_english_content(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.PROCEDURE_PAGE,
            procedure_name="포텐자",
            target_language=ContentLanguage.EN,
        )
        assert result["language"] == "en"

    @patch("app.services.content_engine.get_procedure_data")
    async def test_japanese_content(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.PROCEDURE_PAGE,
            procedure_name="포텐자",
            target_language=ContentLanguage.JA,
        )
        assert result["language"] == "ja"

    @patch("app.services.content_engine.get_procedure_data")
    async def test_chinese_content(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        result = await generate_content(
            content_type=ContentType.PROCEDURE_PAGE,
            procedure_name="포텐자",
            target_language=ContentLanguage.ZH,
        )
        assert result["language"] == "zh"


# ---------------------------------------------------------------------------
# Prompt build tests
# ---------------------------------------------------------------------------

class TestPromptBuilding:
    def test_content_templates_exist_for_all_types(self):
        from app.services.content_engine import CONTENT_TEMPLATES

        for ct in ContentType:
            assert ct in CONTENT_TEMPLATES, f"Missing template for {ct}"
            assert "system" in CONTENT_TEMPLATES[ct]
            assert "user" in CONTENT_TEMPLATES[ct]

    def test_language_instructions_exist(self):
        from app.services.content_engine import LANGUAGE_INSTRUCTIONS

        for lang in ContentLanguage:
            assert lang.value in LANGUAGE_INSTRUCTIONS


# ---------------------------------------------------------------------------
# Supported types/languages tests
# ---------------------------------------------------------------------------

class TestSupportedOptions:
    def test_content_types_list(self):
        types = get_supported_content_types()
        assert len(types) == 5
        type_values = [t["type"] for t in types]
        assert "blog_post" in type_values
        assert "faq" in type_values
        assert "procedure_page" in type_values
        assert "sns_set" in type_values
        assert "medical_guide" in type_values

    def test_languages_list(self):
        langs = get_supported_languages()
        assert len(langs) == 4
        codes = [lang["code"] for lang in langs]
        assert "ko" in codes
        assert "en" in codes
        assert "ja" in codes
        assert "zh" in codes


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

@pytest.fixture
def _mock_playwright():
    """Mock playwright to avoid import errors from pdf_generator."""
    import sys
    import types

    mock_pw = types.ModuleType("playwright")
    mock_pw.async_api = types.ModuleType("playwright.async_api")
    mock_pw.async_api.async_playwright = MagicMock()
    sys.modules.setdefault("playwright", mock_pw)
    sys.modules.setdefault("playwright.async_api", mock_pw.async_api)
    yield
    # Don't remove — other tests may also import app.main


@pytest.mark.usefixtures("_mock_playwright")
class TestContentAPI:
    @patch("app.services.content_engine.get_procedure_data")
    async def test_generate_endpoint(self, mock_get_proc, sample_procedure):
        mock_get_proc.return_value = sample_procedure

        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/worker/content/generate",
                json={
                    "content_type": "blog_post",
                    "procedure_name": "포텐자",
                    "hospital_name": "테스트피부과",
                    "target_language": "ko",
                    "target_keywords": ["포텐자", "RF"],
                },
                headers={"Authorization": "Bearer test-key"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert data["content_type"] == "blog_post"
        assert "포텐자" in data["content"]

    async def test_templates_endpoint(self):
        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/worker/content/templates")

        assert resp.status_code == 200
        data = resp.json()
        assert "content_types" in data
        assert "languages" in data
        assert len(data["content_types"]) == 5
        assert len(data["languages"]) == 4

    @patch("app.services.procedure_data.get_supabase_client")
    async def test_procedures_endpoint(self, mock_sb):
        mock_sb.return_value = None  # No Supabase — returns empty

        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get(
                "/worker/content/procedures",
                headers={"Authorization": "Bearer test-key"},
            )

        assert resp.status_code == 200
        data = resp.json()
        assert "categories" in data

    async def test_generate_endpoint_auth_required(self):
        from httpx import ASGITransport, AsyncClient

        from app.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.post(
                "/worker/content/generate",
                json={"content_type": "blog_post", "procedure_name": "test"},
            )

        assert resp.status_code == 401
