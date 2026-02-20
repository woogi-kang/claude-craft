"""Tests for the content generation module."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.ai.content_gen import (
    ContentGenerationError,
    ContentGenerator,
    _strip_urls,
    dm_uniqueness_check,
)


class TestStripUrls:
    """Test URL stripping from DM content."""

    def test_removes_http(self) -> None:
        assert _strip_urls("check http://example.com now") == "check  now"

    def test_removes_https(self) -> None:
        assert _strip_urls("see https://example.com/path") == "see"

    def test_no_urls_unchanged(self) -> None:
        text = "こんにちは！元気？"
        assert _strip_urls(text) == text

    def test_multiple_urls(self) -> None:
        text = "visit https://a.com and http://b.com please"
        assert _strip_urls(text) == "visit  and  please"


class TestDmUniquenessCheck:
    """Test DM uniqueness verification."""

    def test_no_previous_always_passes(self) -> None:
        assert dm_uniqueness_check("any text", "") is True

    def test_identical_fails(self) -> None:
        text = "短いテキスト"
        assert dm_uniqueness_check(text, text) is False

    def test_sufficiently_different_passes(self) -> None:
        prev = "前のメッセージはこちらです。韓国の皮膚科について。"
        new = (
            "全く違う新しいメッセージを送ります。"
            "ボトックスの料金比較データをまとめました。参考にしてください。"
        )
        assert dm_uniqueness_check(new, prev) is True

    def test_slightly_different_fails(self) -> None:
        prev = "こんにちは、韓国の皮膚科について調べています"
        new = "こんにちは、韓国の皮膚科について調べてます"
        assert dm_uniqueness_check(new, prev) is False


class TestContentGenerator:
    """Test ContentGenerator with mocked LLM."""

    @pytest.fixture
    def generator(self):
        with patch("src.ai.content_gen.create_llm_client") as mock_create:
            mock_client = AsyncMock()
            mock_create.return_value = mock_client
            g = ContentGenerator(
                api_key="test-key",
                model="test-model",
            )
            g._mock_client = mock_client
            return g

    @pytest.mark.asyncio
    async def test_generate_reply(self, generator) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(
                text="いい情報ですね！参考になります",
                model="test",
            )
        )
        result = await generator.generate_reply(
            tweet_content="ボトックス打ってきた",
            author_username="user_a",
            template_category="procedure",
        )
        assert len(result) <= 280
        assert "参考" in result

    @pytest.mark.asyncio
    async def test_reply_truncated_at_280(self, generator) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        long_text = "あ" * 300
        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(text=long_text, model="test")
        )
        result = await generator.generate_reply(
            tweet_content="test",
            author_username="user_b",
            template_category="hospital",
        )
        assert len(result) == 280
        assert result.endswith("...")

    @pytest.mark.asyncio
    async def test_generate_dm(self, generator) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(
                text="こんにちは！投稿見ました。韓国の皮膚科について調べてます",
                model="test",
            )
        )
        result = await generator.generate_dm(
            tweet_content="韓国の皮膚科行きたい",
            author_username="user_c",
            template_category="hospital",
        )
        assert len(result) <= 500

    @pytest.mark.asyncio
    async def test_dm_truncated_at_500(self, generator) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        long_text = "い" * 600
        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(text=long_text, model="test")
        )
        result = await generator.generate_dm(
            tweet_content="test",
            author_username="user_d",
            template_category="review",
        )
        assert len(result) == 500
        assert result.endswith("...")

    @pytest.mark.asyncio
    async def test_dm_urls_stripped(self, generator) -> None:
        from outreach_shared.ai.llm_client import LLMResponse

        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(
                text="こちらをチェック https://evil.com してね",
                model="test",
            )
        )
        result = await generator.generate_dm(
            tweet_content="test",
            author_username="user_e",
            template_category="price",
        )
        assert "https://" not in result

    @pytest.mark.asyncio
    async def test_reply_error_raises(self, generator) -> None:
        generator._mock_client.generate = AsyncMock(side_effect=RuntimeError("API error"))
        with pytest.raises(ContentGenerationError, match="Failed to generate reply"):
            await generator.generate_reply(
                tweet_content="test",
                author_username="user_f",
                template_category="hospital",
            )

    @pytest.mark.asyncio
    async def test_dm_error_raises(self, generator) -> None:
        generator._mock_client.generate = AsyncMock(side_effect=RuntimeError("API error"))
        with pytest.raises(ContentGenerationError, match="Failed to generate DM"):
            await generator.generate_dm(
                tweet_content="test",
                author_username="user_g",
                template_category="review",
            )

    @pytest.mark.asyncio
    async def test_backward_compat_classification_param(self, generator) -> None:
        """The classification param is accepted but unused."""
        from outreach_shared.ai.llm_client import LLMResponse

        generator._mock_client.generate = AsyncMock(
            return_value=LLMResponse(text="テスト", model="test")
        )
        result = await generator.generate_reply(
            tweet_content="test",
            author_username="user_h",
            template_category="review",
            classification="needs_help",
        )
        assert result == "テスト"
