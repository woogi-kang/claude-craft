"""Tests for prescan HTML extraction functions."""

from __future__ import annotations

from clinic_crawl.models.enums import SocialPlatform
from clinic_crawl.scripts.prescan import (
    detect_platform,
    extract_doctor_pages_from_html,
    extract_social_from_html,
)


class TestExtractSocialFromHtml:
    def test_kakao_pf(self):
        html = '<a href="https://pf.kakao.com/xAbCdE">카카오톡 상담</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.KAKAO
        assert "pf.kakao.com" in result[0][1]

    def test_kakao_open(self):
        html = '<a href="https://open.kakao.com/o/gAbCdE">오픈채팅</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.KAKAO

    def test_naver_talk(self):
        html = '<a href="https://talk.naver.com/ct/abc123">네이버톡톡</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.NAVER_TALK

    def test_naver_me(self):
        html = '<a href="https://naver.me/xAbC123">바로가기</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.NAVER_TALK

    def test_line(self):
        html = '<a href="https://line.me/R/ti/p/@clinic">라인</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.LINE

    def test_line_short(self):
        html = '<a href="https://lin.ee/AbCdEf">라인</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.LINE

    def test_whatsapp(self):
        html = '<a href="https://wa.me/821012345678">WhatsApp</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.WHATSAPP

    def test_telegram(self):
        html = '<a href="https://t.me/clinic_bot">텔레그램</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.TELEGRAM

    def test_facebook_messenger(self):
        html = '<a href="https://m.me/clinic.page">메신저</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.FACEBOOK_MESSENGER

    def test_wechat(self):
        html = '<a href="https://u.wechat.com/abc123">위챗</a>'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert result[0][0] == SocialPlatform.WECHAT

    def test_multiple_platforms(self):
        html = """
        <a href="https://pf.kakao.com/xTest">카카오</a>
        <a href="https://talk.naver.com/ct/test">네이버</a>
        <a href="https://t.me/test_bot">텔레그램</a>
        """
        result = extract_social_from_html(html)
        platforms = {r[0] for r in result}
        assert SocialPlatform.KAKAO in platforms
        assert SocialPlatform.NAVER_TALK in platforms
        assert SocialPlatform.TELEGRAM in platforms

    def test_deduplicates_same_url(self):
        html = """
        <a href="https://pf.kakao.com/xTest">상담1</a>
        <a href="https://pf.kakao.com/xTest">상담2</a>
        """
        result = extract_social_from_html(html)
        assert len(result) == 1

    def test_no_matches(self):
        html = "<html><body><p>No social links here</p></body></html>"
        result = extract_social_from_html(html)
        assert result == []

    def test_strips_trailing_punctuation(self):
        html = 'href="https://pf.kakao.com/xTest").'
        result = extract_social_from_html(html)
        assert len(result) == 1
        assert not result[0][1].endswith(")")


class TestExtractDoctorPagesFromHtml:
    def test_doctor_href(self):
        html = '<a href="/doctor/intro">의료진 소개</a>'
        result = extract_doctor_pages_from_html(html)
        assert "/doctor/intro" in result

    def test_korean_keyword(self):
        html = '<a href="/page/의료진소개">의료진</a>'
        result = extract_doctor_pages_from_html(html)
        assert "/page/의료진소개" in result

    def test_staff_keyword(self):
        html = '<a href="/about/staff">Staff</a>'
        result = extract_doctor_pages_from_html(html)
        assert "/about/staff" in result

    def test_ignores_hash_links(self):
        html = '<a href="#doctor-section">Jump</a>'
        result = extract_doctor_pages_from_html(html)
        assert result == []

    def test_deduplicates(self):
        html = """
        <a href="/doctor">의료진</a>
        <a href="/doctor">의료진 소개</a>
        """
        result = extract_doctor_pages_from_html(html)
        assert len(result) == 1


class TestDetectPlatform:
    def test_imweb_in_html(self):
        assert detect_platform("<html>imweb site builder</html>", None) == "imweb"

    def test_imweb_in_server(self):
        assert detect_platform("<html></html>", "imweb") == "imweb"

    def test_wordpress(self):
        assert detect_platform("<html>wp-content/themes</html>", None) == "wordpress"

    def test_nextjs(self):
        assert detect_platform('<div id="__next"></div>', None) == "nextjs"

    def test_modoo(self):
        assert detect_platform("<html>modoo platform</html>", None) == "modoo"

    def test_wix(self):
        assert detect_platform("<html>wixsite content</html>", None) == "wix"

    def test_unknown(self):
        assert detect_platform("<html><body>generic</body></html>", None) is None

    def test_only_checks_first_5000_chars(self):
        html = "x" * 6000 + "imweb"
        assert detect_platform(html, None) is None
