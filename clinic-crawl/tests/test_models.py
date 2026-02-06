"""Tests for Pydantic models."""

from __future__ import annotations

import pytest

from clinic_crawl.models.csv_row import SkinClinicRow
from clinic_crawl.models.doctor import DoctorCredential, DoctorInfo, DoctorPage
from clinic_crawl.models.enums import (
    CrawlCategory,
    CrawlPhase,
    DoctorRole,
    ExtractionMethod,
    SocialPlatform,
)
from clinic_crawl.models.social import SocialChannels, SocialLink


class TestSkinClinicRow:
    def _make_row(self, **overrides) -> SkinClinicRow:
        defaults = {
            "NO": 1,
            "병원/약국명": "테스트피부과",
            "병원/약국구분": "피부과",
        }
        defaults.update(overrides)
        return SkinClinicRow.model_validate(defaults)

    def test_basic_creation(self):
        row = self._make_row()
        assert row.no == 1
        assert row.name == "테스트피부과"

    def test_clean_url_adds_https(self):
        row = self._make_row(홈페이지="example.com")
        assert row.homepage == "https://example.com"

    def test_clean_url_preserves_https(self):
        row = self._make_row(홈페이지="https://example.com")
        assert row.homepage == "https://example.com"

    def test_clean_url_preserves_http(self):
        row = self._make_row(홈페이지="http://example.com")
        assert row.homepage == "http://example.com"

    def test_clean_url_strips_whitespace(self):
        row = self._make_row(홈페이지="  example.com  ")
        assert row.homepage == "https://example.com"

    def test_clean_url_rejects_garbage_dash(self):
        row = self._make_row(홈페이지="-")
        assert row.homepage is None

    def test_clean_url_rejects_garbage_korean(self):
        row = self._make_row(홈페이지="없음")
        assert row.homepage is None

    def test_clean_url_rejects_empty_protocol(self):
        row = self._make_row(홈페이지="http://")
        assert row.homepage is None

    def test_clean_url_removes_bom(self):
        row = self._make_row(홈페이지="\ufeffexample.com")
        assert row.homepage == "https://example.com"

    def test_clean_url_removes_zero_width(self):
        row = self._make_row(홈페이지="exam\u200bple.com")
        assert row.homepage == "https://example.com"

    def test_clean_url_none(self):
        row = self._make_row()
        assert row.homepage is None

    def test_urls_deduplicates(self):
        row = self._make_row(
            홈페이지="https://example.com",
            naver_website="https://example.com",
        )
        assert row.urls == ["https://example.com"]

    def test_urls_multiple(self):
        row = self._make_row(
            홈페이지="https://a.com",
            naver_website="https://b.com",
        )
        assert row.urls == ["https://a.com", "https://b.com"]

    def test_urls_empty_when_no_urls(self):
        row = self._make_row()
        assert row.urls == []


class TestSocialLink:
    def test_frozen(self):
        link = SocialLink(
            platform=SocialPlatform.KAKAO,
            url="https://pf.kakao.com/test",
            extraction_method=ExtractionMethod.PRESCAN_REGEX,
        )
        with pytest.raises(Exception):
            link.url = "changed"

    def test_confidence_default(self):
        link = SocialLink(
            platform=SocialPlatform.KAKAO,
            url="https://pf.kakao.com/test",
            extraction_method=ExtractionMethod.PRESCAN_REGEX,
        )
        assert link.confidence == 1.0

    def test_confidence_bounds(self):
        with pytest.raises(Exception):
            SocialLink(
                platform=SocialPlatform.KAKAO,
                url="https://pf.kakao.com/test",
                extraction_method=ExtractionMethod.PRESCAN_REGEX,
                confidence=1.5,
            )


class TestSocialChannels:
    def _make_link(
        self, platform: SocialPlatform, url: str, confidence: float = 1.0
    ) -> SocialLink:
        return SocialLink(
            platform=platform,
            url=url,
            extraction_method=ExtractionMethod.PRESCAN_REGEX,
            confidence=confidence,
        )

    def test_platforms_found(self):
        channels = SocialChannels(
            links=[
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a"),
                self._make_link(SocialPlatform.LINE, "https://line.me/b"),
            ]
        )
        assert channels.platforms_found == {SocialPlatform.KAKAO, SocialPlatform.LINE}

    def test_has_kakao_true(self):
        channels = SocialChannels(
            links=[self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a")]
        )
        assert channels.has_kakao is True

    def test_has_kakao_false(self):
        channels = SocialChannels(
            links=[self._make_link(SocialPlatform.LINE, "https://line.me/a")]
        )
        assert channels.has_kakao is False

    def test_deduplicated_keeps_highest_confidence(self):
        channels = SocialChannels(
            links=[
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a", 0.5),
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a", 0.9),
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a", 0.7),
            ]
        )
        deduped = channels.deduplicated()
        assert len(deduped.links) == 1
        assert deduped.links[0].confidence == 0.9

    def test_deduplicated_preserves_different_urls(self):
        channels = SocialChannels(
            links=[
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a"),
                self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/b"),
            ]
        )
        deduped = channels.deduplicated()
        assert len(deduped.links) == 2

    def test_deduplicated_preserves_metadata(self):
        channels = SocialChannels(
            links=[self._make_link(SocialPlatform.KAKAO, "https://pf.kakao.com/a")],
            chat_widget_detected=True,
            qr_image_urls=["https://example.com/qr.png"],
        )
        deduped = channels.deduplicated()
        assert deduped.chat_widget_detected is True
        assert deduped.qr_image_urls == ["https://example.com/qr.png"]


class TestDoctorModels:
    def test_credential_frozen(self):
        cred = DoctorCredential(credential_type="전문의", value="피부과전문의")
        with pytest.raises(Exception):
            cred.value = "changed"

    def test_doctor_info_defaults(self):
        doc = DoctorInfo()
        assert doc.name is None
        assert doc.role == DoctorRole.SPECIALIST
        assert doc.credentials == []
        assert doc.education == []

    def test_doctor_page_count(self):
        page = DoctorPage(
            doctors=[DoctorInfo(name="Dr A"), DoctorInfo(name="Dr B")]
        )
        assert page.doctor_count == 2

    def test_doctor_page_has_photos(self):
        page = DoctorPage(
            doctors=[DoctorInfo(name="Dr A", photo_url="https://example.com/a.jpg")]
        )
        assert page.has_photos is True

    def test_doctor_page_no_photos(self):
        page = DoctorPage(doctors=[DoctorInfo(name="Dr A")])
        assert page.has_photos is False


class TestEnums:
    def test_crawl_category_values(self):
        assert CrawlCategory.CUSTOM_DOMAIN == "custom_domain"
        assert CrawlCategory.NO_URL == "no_url"

    def test_crawl_phase_values(self):
        assert CrawlPhase.PENDING == "pending"
        assert CrawlPhase.VALIDATED == "validated"

    def test_social_platform_values(self):
        assert SocialPlatform.KAKAO == "kakao"
        assert SocialPlatform.NAVER_TALK == "naver_talk"

    def test_extraction_method_values(self):
        assert ExtractionMethod.PRESCAN_REGEX == "prescan_regex"
        assert ExtractionMethod.QR_DECODE == "qr_decode"
