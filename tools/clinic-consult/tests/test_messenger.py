"""Tests for the messenger abstraction layer (selectors + deep links)."""

from __future__ import annotations

import pytest

from src.messenger import normalize_platform
from src.messenger.deep_link import (
    build_chat_url,
    validate_channel_url,
)
from src.messenger.selectors import (
    KAKAO,
    LINE,
    MessengerSelectors,
    get_selectors,
)


# -----------------------------------------------------------------------
# normalize_platform
# -----------------------------------------------------------------------


class TestNormalizePlatform:
    """Test the centralized platform normalization."""

    def test_kakao_lowercase(self) -> None:
        assert normalize_platform("kakao") == "kakao"

    def test_kakaotalk_alias(self) -> None:
        assert normalize_platform("kakaotalk") == "kakao"

    def test_kakao_uppercase(self) -> None:
        assert normalize_platform("KAKAO") == "kakao"

    def test_kakaotalk_mixed_case(self) -> None:
        assert normalize_platform("KakaoTalk") == "kakao"

    def test_line_lowercase(self) -> None:
        assert normalize_platform("line") == "line"

    def test_line_uppercase(self) -> None:
        assert normalize_platform("LINE") == "line"

    def test_whitespace_stripped(self) -> None:
        assert normalize_platform("  kakao  ") == "kakao"

    def test_unknown_passthrough(self) -> None:
        assert normalize_platform("wechat") == "wechat"


# -----------------------------------------------------------------------
# Selectors
# -----------------------------------------------------------------------


class TestMessengerSelectors:
    """Test MessengerSelectors dataclass and factory."""

    def test_kakao_instance_exists(self) -> None:
        assert KAKAO.package == "com.kakao.talk"
        assert "kakao" in KAKAO.chat_list_tab.lower()

    def test_line_instance_exists(self) -> None:
        assert LINE.package == "jp.naver.line.android"
        assert "line" in LINE.chat_list_tab.lower()

    def test_frozen(self) -> None:
        import dataclasses

        with pytest.raises(dataclasses.FrozenInstanceError):
            KAKAO.package = "changed"  # type: ignore[misc]

    def test_get_selectors_kakao(self) -> None:
        sel = get_selectors("kakao")
        assert sel is KAKAO

    def test_get_selectors_kakaotalk_alias(self) -> None:
        sel = get_selectors("kakaotalk")
        assert sel is KAKAO

    def test_get_selectors_line(self) -> None:
        sel = get_selectors("line")
        assert sel is LINE

    def test_get_selectors_case_insensitive(self) -> None:
        assert get_selectors("KAKAO") is KAKAO
        assert get_selectors("Line") is LINE

    def test_get_selectors_unsupported_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported"):
            get_selectors("wechat")

    def test_all_fields_populated_kakao(self) -> None:
        for field_name in MessengerSelectors.__dataclass_fields__:
            val = getattr(KAKAO, field_name)
            assert val, f"KAKAO.{field_name} is empty"

    def test_all_fields_populated_line(self) -> None:
        for field_name in MessengerSelectors.__dataclass_fields__:
            val = getattr(LINE, field_name)
            assert val, f"LINE.{field_name} is empty"


# -----------------------------------------------------------------------
# Deep Links - KakaoTalk
# -----------------------------------------------------------------------


class TestKakaoChatUrl:
    """Test KakaoTalk deep link URL construction."""

    def test_basic_url(self) -> None:
        url = build_chat_url("kakao", "https://pf.kakao.com/_abcdef")
        assert url == "https://pf.kakao.com/_abcdef/chat"

    def test_already_has_chat_suffix(self) -> None:
        url = build_chat_url("kakao", "https://pf.kakao.com/_abcdef/chat")
        assert url == "https://pf.kakao.com/_abcdef/chat"

    def test_trailing_slash(self) -> None:
        url = build_chat_url("kakao", "https://pf.kakao.com/_abcdef/")
        assert url == "https://pf.kakao.com/_abcdef/chat"

    def test_fragment_stripped(self) -> None:
        url = build_chat_url("kakao", "https://pf.kakao.com/_abcdef#section")
        assert url == "https://pf.kakao.com/_abcdef/chat"

    def test_non_kakao_url_returns_none(self) -> None:
        url = build_chat_url("kakao", "https://example.com/something")
        assert url is None

    def test_empty_url_returns_none(self) -> None:
        url = build_chat_url("kakao", "")
        assert url is None

    def test_kakaotalk_alias(self) -> None:
        url = build_chat_url("kakaotalk", "https://pf.kakao.com/_test")
        assert url == "https://pf.kakao.com/_test/chat"


# -----------------------------------------------------------------------
# Deep Links - LINE
# -----------------------------------------------------------------------


class TestLineChatUrl:
    """Test LINE deep link URL construction."""

    def test_direct_deep_link(self) -> None:
        url = build_chat_url("line", "https://line.me/R/ti/p/@clinic123")
        assert url == "https://line.me/R/ti/p/@clinic123"

    def test_short_url(self) -> None:
        url = build_chat_url("line", "https://lin.ee/abc123")
        assert url == "https://lin.ee/abc123"

    def test_page_line_me_format(self) -> None:
        url = build_chat_url("line", "https://page.line.me/clinic123")
        assert url == "https://line.me/R/ti/p/@clinic123"

    def test_page_line_me_with_at_prefix(self) -> None:
        url = build_chat_url("line", "https://page.line.me/@clinic123")
        assert url == "https://line.me/R/ti/p/@clinic123"

    def test_bare_at_id(self) -> None:
        url = build_chat_url("line", "@clinic123")
        assert url == "https://line.me/R/ti/p/@clinic123"

    def test_other_line_me_url(self) -> None:
        url = build_chat_url("line", "https://line.me/some/other/path")
        assert url == "https://line.me/some/other/path"

    def test_empty_url_returns_none(self) -> None:
        url = build_chat_url("line", "")
        assert url is None

    def test_non_line_url_returns_none(self) -> None:
        url = build_chat_url("line", "https://example.com/foo")
        assert url is None


# -----------------------------------------------------------------------
# Deep Links - Unsupported
# -----------------------------------------------------------------------


class TestUnsupportedPlatform:
    """Test unsupported platform handling."""

    def test_unsupported_returns_none(self) -> None:
        url = build_chat_url("wechat", "https://example.com")
        assert url is None


# -----------------------------------------------------------------------
# URL Validation
# -----------------------------------------------------------------------


class TestValidateChannelUrl:
    """Test channel URL validation."""

    def test_kakao_valid(self) -> None:
        assert validate_channel_url("kakao", "https://pf.kakao.com/_abc") is True

    def test_kakao_invalid(self) -> None:
        assert validate_channel_url("kakao", "https://example.com") is False

    def test_line_valid_line_me(self) -> None:
        assert validate_channel_url("line", "https://line.me/R/ti/p/@test") is True

    def test_line_valid_lin_ee(self) -> None:
        assert validate_channel_url("line", "https://lin.ee/abc") is True

    def test_line_valid_page(self) -> None:
        assert validate_channel_url("line", "https://page.line.me/test") is True

    def test_line_valid_bare_at(self) -> None:
        assert validate_channel_url("line", "@test") is True

    def test_line_invalid(self) -> None:
        assert validate_channel_url("line", "https://example.com") is False

    def test_empty_url(self) -> None:
        assert validate_channel_url("kakao", "") is False

    def test_unsupported_platform(self) -> None:
        assert validate_channel_url("wechat", "https://example.com") is False

    # --- Domain spoofing tests (P0-2 security fix) ---

    def test_kakao_rejects_spoofed_domain_in_path(self) -> None:
        assert validate_channel_url("kakao", "https://evil.com/pf.kakao.com/_abc") is False

    def test_kakao_rejects_spoofed_subdomain(self) -> None:
        assert validate_channel_url("kakao", "https://pf.kakao.com.evil.com/_abc") is False

    def test_line_rejects_spoofed_domain_in_path(self) -> None:
        assert validate_channel_url("line", "https://evil.com/line.me/R/ti/p/@test") is False

    def test_line_rejects_spoofed_subdomain(self) -> None:
        assert validate_channel_url("line", "https://line.me.evil.com/R/ti/p/@test") is False


class TestBuildChatUrlSpoofing:
    """Ensure build_chat_url rejects domain-spoofed URLs."""

    def test_kakao_spoofed_path(self) -> None:
        assert build_chat_url("kakao", "https://evil.com/pf.kakao.com/_abc") is None

    def test_kakao_spoofed_subdomain(self) -> None:
        assert build_chat_url("kakao", "https://pf.kakao.com.evil.com/_abc") is None

    def test_line_spoofed_path(self) -> None:
        assert build_chat_url("line", "https://evil.com/line.me/R/ti/p/@test") is None

    def test_line_spoofed_page_subdomain(self) -> None:
        assert build_chat_url("line", "https://page.line.me.evil.com/clinic") is None
