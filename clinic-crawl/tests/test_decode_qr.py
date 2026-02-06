"""Tests for QR code decoding utilities."""

from __future__ import annotations

from clinic_crawl.scripts.decode_qr import decode_qr_from_bytes, qr_text_to_social_link


class TestDecodeQrFromBytes:
    def test_invalid_image_returns_empty(self):
        result = decode_qr_from_bytes(b"not an image")
        assert result == []

    def test_empty_bytes_returns_empty(self):
        result = decode_qr_from_bytes(b"")
        assert result == []


class TestQrTextToSocialLink:
    def test_kakao_url(self):
        link = qr_text_to_social_link("https://pf.kakao.com/test123")
        assert link is not None
        assert link.platform == "kakao"
        assert link.extraction_method == "qr_decode"
        assert link.confidence == 0.95

    def test_wechat_url(self):
        link = qr_text_to_social_link("https://wechat.com/test")
        assert link is not None
        assert link.platform == "wechat"

    def test_non_http_returns_none(self):
        assert qr_text_to_social_link("just plain text") is None

    def test_non_social_url_returns_none(self):
        assert qr_text_to_social_link("https://example.com") is None

    def test_strips_whitespace(self):
        link = qr_text_to_social_link("  https://pf.kakao.com/test  ")
        assert link is not None
        assert link.platform == "kakao"

    def test_line_url(self):
        link = qr_text_to_social_link("https://line.me/R/ti/p/test")
        assert link is not None
        assert link.platform == "line"

    def test_weixin_keyword(self):
        link = qr_text_to_social_link("https://weixin.qq.com/r/abc")
        assert link is not None
        assert link.platform == "wechat"
