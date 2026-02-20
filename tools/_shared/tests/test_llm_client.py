"""Tests for LLM client abstraction.

Uses mocks to avoid real API calls.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from outreach_shared.ai.llm_client import (
    ClaudeClient,
    GeminiClient,
    LLMResponse,
    create_llm_client,
)


class TestLLMResponse:
    """Test the LLMResponse dataclass."""

    def test_basic_response(self) -> None:
        r = LLMResponse(text="hello", model="test-model")
        assert r.text == "hello"
        assert r.model == "test-model"
        assert r.usage is None

    def test_response_with_usage(self) -> None:
        usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        r = LLMResponse(text="hi", model="m", usage=usage)
        assert r.usage is not None
        assert r.usage["total_tokens"] == 30


class TestGeminiClient:
    """Test GeminiClient with mocked google-genai SDK."""

    @pytest.mark.asyncio
    async def test_generate_basic(self) -> None:
        mock_response = MagicMock()
        mock_response.text = "Generated text"
        mock_response.usage_metadata = MagicMock()
        mock_response.usage_metadata.prompt_token_count = 5
        mock_response.usage_metadata.candidates_token_count = 10
        mock_response.usage_metadata.total_token_count = 15

        mock_aio_models = MagicMock()
        mock_aio_models.generate_content = AsyncMock(return_value=mock_response)

        mock_aio = MagicMock()
        mock_aio.models = mock_aio_models

        mock_genai_client = MagicMock()
        mock_genai_client.aio = mock_aio

        with patch("outreach_shared.ai.llm_client.GeminiClient.__init__", return_value=None):
            client = GeminiClient.__new__(GeminiClient)
            client._client = mock_genai_client
            client._model = "gemini-2.0-flash"

        result = await client.generate("Hello", system="Be helpful")
        assert result.text == "Generated text"
        assert result.model == "gemini-2.0-flash"
        assert result.usage is not None
        assert result.usage["total_tokens"] == 15

    @pytest.mark.asyncio
    async def test_generate_json_mode(self) -> None:
        mock_response = MagicMock()
        mock_response.text = '{"key": "value"}'
        mock_response.usage_metadata = None

        mock_aio_models = MagicMock()
        mock_aio_models.generate_content = AsyncMock(return_value=mock_response)

        mock_aio = MagicMock()
        mock_aio.models = mock_aio_models

        mock_genai_client = MagicMock()
        mock_genai_client.aio = mock_aio

        with patch("outreach_shared.ai.llm_client.GeminiClient.__init__", return_value=None):
            client = GeminiClient.__new__(GeminiClient)
            client._client = mock_genai_client
            client._model = "gemini-2.0-flash"

        result = await client.generate("Give JSON", json_mode=True)
        assert result.text == '{"key": "value"}'
        assert result.usage is None

    @pytest.mark.asyncio
    async def test_generate_empty_response(self) -> None:
        mock_response = MagicMock()
        mock_response.text = None
        mock_response.usage_metadata = None

        mock_aio_models = MagicMock()
        mock_aio_models.generate_content = AsyncMock(return_value=mock_response)

        mock_aio = MagicMock()
        mock_aio.models = mock_aio_models

        mock_genai_client = MagicMock()
        mock_genai_client.aio = mock_aio

        with patch("outreach_shared.ai.llm_client.GeminiClient.__init__", return_value=None):
            client = GeminiClient.__new__(GeminiClient)
            client._client = mock_genai_client
            client._model = "gemini-2.0-flash"

        result = await client.generate("Hello")
        assert result.text == ""


class TestClaudeClient:
    """Test ClaudeClient with mocked anthropic SDK."""

    @pytest.mark.asyncio
    async def test_generate_basic(self) -> None:
        mock_block = MagicMock()
        mock_block.type = "text"
        mock_block.text = "Claude response"

        mock_usage = MagicMock()
        mock_usage.input_tokens = 10
        mock_usage.output_tokens = 20

        mock_response = MagicMock()
        mock_response.content = [mock_block]
        mock_response.usage = mock_usage

        mock_messages = MagicMock()
        mock_messages.create = AsyncMock(return_value=mock_response)

        mock_anthropic = MagicMock()
        mock_anthropic.messages = mock_messages

        with patch("outreach_shared.ai.llm_client.ClaudeClient.__init__", return_value=None):
            client = ClaudeClient.__new__(ClaudeClient)
            client._client = mock_anthropic
            client._model = "claude-sonnet-4-20250514"

        result = await client.generate("Hello", system="Be nice")
        assert result.text == "Claude response"
        assert result.model == "claude-sonnet-4-20250514"
        assert result.usage is not None
        assert result.usage["total_tokens"] == 30


class TestCreateLLMClient:
    """Test the factory function."""

    def test_create_gemini_client(self) -> None:
        with patch("outreach_shared.ai.llm_client.GeminiClient.__init__", return_value=None):
            client = create_llm_client("gemini", "fake-key")
        assert isinstance(client, GeminiClient)

    def test_create_claude_client(self) -> None:
        with patch("outreach_shared.ai.llm_client.ClaudeClient.__init__", return_value=None):
            client = create_llm_client("claude", "fake-key")
        assert isinstance(client, ClaudeClient)

    def test_create_gemini_with_model(self) -> None:
        with patch("outreach_shared.ai.llm_client.GeminiClient.__init__", return_value=None):
            client = create_llm_client("gemini", "fake-key", model="gemini-2.0-pro")
        assert isinstance(client, GeminiClient)

    def test_unknown_provider_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            create_llm_client("openai", "fake-key")
