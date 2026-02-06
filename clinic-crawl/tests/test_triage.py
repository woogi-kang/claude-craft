"""Tests for URL classification and chain hospital detection."""

from __future__ import annotations

from clinic_crawl.models.csv_row import SkinClinicRow
from clinic_crawl.models.enums import CrawlCategory
from clinic_crawl.scripts.triage import classify_url, extract_domain, find_chain_hospitals


class TestClassifyUrl:
    def test_none_url(self):
        assert classify_url(None) == CrawlCategory.NO_URL

    def test_empty_url(self):
        assert classify_url("") == CrawlCategory.NO_URL

    def test_naver_blog(self):
        assert classify_url("https://blog.naver.com/test") == CrawlCategory.BLOG_NAVER

    def test_kakao_channel(self):
        assert classify_url("https://pf.kakao.com/test") == CrawlCategory.KAKAO_CHANNEL

    def test_instagram(self):
        assert classify_url("https://www.instagram.com/clinic") == CrawlCategory.INSTAGRAM

    def test_youtube(self):
        assert classify_url("https://youtube.com/channel/test") == CrawlCategory.YOUTUBE

    def test_youtube_short(self):
        assert classify_url("https://youtu.be/abc123") == CrawlCategory.YOUTUBE

    def test_imweb(self):
        assert classify_url("https://clinic.imweb.me") == CrawlCategory.IMWEB

    def test_mobidoc(self):
        assert classify_url("https://clinic.mobidoc.co.kr") == CrawlCategory.MOBIDOC

    def test_google_sites(self):
        assert classify_url("https://sites.google.com/view/clinic") == CrawlCategory.GOOGLE_SITES

    def test_custom_domain(self):
        assert classify_url("https://myclinic.co.kr") == CrawlCategory.CUSTOM_DOMAIN

    def test_case_insensitive(self):
        assert classify_url("https://BLOG.NAVER.COM/test") == CrawlCategory.BLOG_NAVER


class TestExtractDomain:
    def test_simple_domain(self):
        assert extract_domain("https://example.com/path") == "example.com"

    def test_subdomain(self):
        assert extract_domain("https://www.example.com") == "example.com"

    def test_korean_domain(self):
        assert extract_domain("https://clinic.co.kr") == "clinic.co.kr"

    def test_invalid_url(self):
        assert extract_domain("not-a-url") is None

    def test_empty(self):
        assert extract_domain("") is None


def _make_row(no: int, homepage: str | None = None) -> SkinClinicRow:
    data = {"NO": no, "병원/약국명": f"Hospital {no}", "병원/약국구분": "피부과"}
    if homepage:
        data["홈페이지"] = homepage
    return SkinClinicRow.model_validate(data)


class TestFindChainHospitals:
    def test_identifies_chains(self):
        rows = [
            _make_row(1, "https://branch1.skinclinic.com"),
            _make_row(2, "https://branch2.skinclinic.com"),
            _make_row(3, "https://branch3.skinclinic.com"),
        ]
        chains = find_chain_hospitals(rows, threshold=3)
        assert "skinclinic.com" in chains
        assert sorted(chains["skinclinic.com"]) == [1, 2, 3]

    def test_below_threshold(self):
        rows = [
            _make_row(1, "https://a.clinic.com"),
            _make_row(2, "https://b.clinic.com"),
        ]
        chains = find_chain_hospitals(rows, threshold=3)
        assert len(chains) == 0

    def test_multiple_chains(self):
        rows = [
            _make_row(1, "https://a.chain1.com"),
            _make_row(2, "https://b.chain1.com"),
            _make_row(3, "https://c.chain1.com"),
            _make_row(4, "https://a.chain2.com"),
            _make_row(5, "https://b.chain2.com"),
            _make_row(6, "https://c.chain2.com"),
        ]
        chains = find_chain_hospitals(rows, threshold=3)
        assert len(chains) == 2

    def test_no_urls(self):
        rows = [_make_row(1), _make_row(2), _make_row(3)]
        chains = find_chain_hospitals(rows, threshold=3)
        assert len(chains) == 0
