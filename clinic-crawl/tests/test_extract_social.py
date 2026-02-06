"""Tests for social link extraction helpers."""

from __future__ import annotations

from clinic_crawl.models.enums import ExtractionMethod
from clinic_crawl.scripts.extract_social import (
    build_social_channels,
    clean_social_url,
    detect_chat_widgets,
    detect_qr_images,
    parse_social_from_html,
)


class TestCleanSocialUrl:
    def test_strips_trailing_punctuation(self):
        assert clean_social_url("https://pf.kakao.com/abc;") == "https://pf.kakao.com/abc"

    def test_removes_tracking_params(self):
        assert clean_social_url("https://line.me/R/ti/p/abc?utm=1") == "https://line.me/R/ti/p/abc"

    def test_keeps_kakao_params(self):
        url = "https://pf.kakao.com/abc?ref=homepage"
        assert clean_social_url(url) == url

    def test_no_change_clean_url(self):
        url = "https://talk.naver.com/ct/test"
        assert clean_social_url(url) == url


class TestParseSocialFromHtml:
    def test_finds_kakao_link(self):
        html = '<a href="https://pf.kakao.com/test123">Chat</a>'
        links = parse_social_from_html(html, "https://clinic.com")
        assert len(links) == 1
        assert links[0].platform == "kakao"

    def test_finds_naver_talk(self):
        html = '<a href="https://talk.naver.com/ct/clinic">Talk</a>'
        links = parse_social_from_html(html, "https://clinic.com")
        assert len(links) == 1
        assert links[0].platform == "naver_talk"

    def test_deduplicates(self):
        html = """
        <a href="https://pf.kakao.com/test">Link1</a>
        <a href="https://pf.kakao.com/test">Link2</a>
        """
        links = parse_social_from_html(html, "https://clinic.com")
        assert len(links) == 1

    def test_resolves_relative_urls(self):
        html = '<a href="/go/kakao" data-url="https://pf.kakao.com/test">Chat</a>'
        links = parse_social_from_html(html, "https://clinic.com")
        assert any(link.platform == "kakao" for link in links)

    def test_no_matches_returns_empty(self):
        html = '<a href="https://example.com">Site</a>'
        links = parse_social_from_html(html, "https://clinic.com")
        assert links == []

    def test_confidence_dom_static(self):
        html = '<a href="https://pf.kakao.com/test">Chat</a>'
        links = parse_social_from_html(html, "https://clinic.com", ExtractionMethod.DOM_STATIC)
        assert links[0].confidence == 0.9

    def test_confidence_other_method(self):
        html = '<a href="https://pf.kakao.com/test">Chat</a>'
        links = parse_social_from_html(html, "https://clinic.com", ExtractionMethod.DOM_DYNAMIC)
        assert links[0].confidence == 0.85


class TestDetectChatWidgets:
    def test_kakao_channel_sdk(self):
        html = '<script src="https://developers.kakao.com/sdk/js/kakao.channel.js"></script>'
        assert detect_chat_widgets(html) is True

    def test_kakao_channel_chat(self):
        html = "<script>kakao.channel.chat</script>"
        assert detect_chat_widgets(html) is True

    def test_no_widget(self):
        html = "<div>Normal content</div>"
        assert detect_chat_widgets(html) is False


class TestDetectQrImages:
    def test_finds_qr_image(self):
        html = '<img src="/images/wechat-qr.png" alt="WeChat QR">'
        urls = detect_qr_images(html)
        assert len(urls) == 1
        assert urls[0] == "/images/wechat-qr.png"

    def test_no_qr_images(self):
        html = '<img src="/logo.png" alt="Logo">'
        urls = detect_qr_images(html)
        assert urls == []

    def test_korean_qr_keyword(self):
        html = '<img src="/qr.jpg" alt="큐알코드">'
        urls = detect_qr_images(html)
        assert len(urls) == 1


class TestBuildSocialChannels:
    def test_builds_channels(self):
        from clinic_crawl.models.social import SocialLink

        links = [
            SocialLink(
                platform="kakao",
                url="https://pf.kakao.com/a",
                extraction_method=ExtractionMethod.DOM_STATIC,
            ),
        ]
        channels = build_social_channels(links, chat_widget=True)
        assert channels.chat_widget_detected is True
        assert len(channels.links) == 1

    def test_deduplicates(self):
        from clinic_crawl.models.social import SocialLink

        links = [
            SocialLink(
                platform="kakao",
                url="https://pf.kakao.com/a",
                extraction_method=ExtractionMethod.DOM_STATIC,
                confidence=0.9,
            ),
            SocialLink(
                platform="kakao",
                url="https://pf.kakao.com/a",
                extraction_method=ExtractionMethod.PRESCAN_REGEX,
                confidence=0.7,
            ),
        ]
        channels = build_social_channels(links)
        assert len(channels.links) == 1
        assert channels.links[0].confidence == 0.9
