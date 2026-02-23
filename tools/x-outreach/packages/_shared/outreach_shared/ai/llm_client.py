"""LLM client abstraction with Codex CLI, Gemini CLI, and SDK implementations.

Provides a unified protocol for LLM interactions, allowing the
outreach pipeline to switch between providers without code changes.
CLI-based clients (Codex, Gemini CLI) require no API keys.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from outreach_shared.utils.logger import get_logger

logger = get_logger("llm_client")


@dataclass
class LLMResponse:
    """Unified response from any LLM provider."""

    text: str
    model: str
    usage: dict[str, int] | None = None


class LLMClient(Protocol):
    """Protocol for LLM client implementations."""

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate a text completion.

        Parameters
        ----------
        prompt:
            The user prompt / message.
        system:
            Optional system instruction.
        temperature:
            Sampling temperature (0.0-1.0).
        max_tokens:
            Maximum tokens in the response.
        json_mode:
            When ``True``, instruct the model to return valid JSON.

        Returns
        -------
        LLMResponse
            The model's response with text and metadata.
        """
        ...


class GeminiClient:
    """Google Gemini LLM client using the ``google-genai`` SDK.

    Parameters
    ----------
    api_key:
        Gemini API key.
    model:
        Model identifier. Defaults to ``gemini-2.0-flash``.
    """

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "gemini-2.0-flash",
    ) -> None:
        from google import genai

        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate text using Gemini API."""
        from google.genai import types

        config: dict[str, Any] = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        if system:
            config["system_instruction"] = system
        if json_mode:
            config["response_mime_type"] = "application/json"

        generation_config = types.GenerateContentConfig(**config)

        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=generation_config,
        )

        text = response.text or ""
        usage = None
        if response.usage_metadata:
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count or 0,
                "completion_tokens": response.usage_metadata.candidates_token_count or 0,
                "total_tokens": response.usage_metadata.total_token_count or 0,
            }

        logger.debug(
            "gemini_response",
            model=self._model,
            tokens=usage.get("total_tokens") if usage else None,
        )

        return LLMResponse(text=text, model=self._model, usage=usage)


class ClaudeClient:
    """Anthropic Claude LLM client.

    Parameters
    ----------
    api_key:
        Anthropic API key.
    model:
        Model identifier. Defaults to ``claude-sonnet-4-20250514``.
    """

    def __init__(
        self,
        api_key: str,
        *,
        model: str = "claude-sonnet-4-20250514",
    ) -> None:
        import anthropic

        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate text using Claude API."""
        messages = [{"role": "user", "content": prompt}]

        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            kwargs["system"] = system

        response = await self._client.messages.create(**kwargs)

        text = ""
        for block in response.content:
            if block.type == "text":
                text += block.text

        usage = {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
        }

        logger.debug(
            "claude_response",
            model=self._model,
            tokens=usage["total_tokens"],
        )

        return LLMResponse(text=text, model=self._model, usage=usage)


class CodexClient:
    """OpenAI Codex CLI client using subprocess.

    Calls ``codex exec`` as a subprocess, allowing use of ChatGPT
    account authentication without an API key.

    Parameters
    ----------
    model:
        Model to pass to codex CLI. ``None`` uses the default.
    """

    def __init__(
        self,
        api_key: str = "",
        *,
        model: str | None = None,
    ) -> None:
        self._model = model if model else "codex-default"

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate text using Codex CLI subprocess."""
        import asyncio

        full_prompt = ""
        if system:
            full_prompt += f"[System Instructions]\n{system}\n\n"
        full_prompt += f"[User Request]\n{prompt}"
        if json_mode:
            full_prompt += "\n\nRespond ONLY with valid JSON, no markdown."
        full_prompt += (
            "\n\nRespond directly with the requested content only."
            " No explanations, no code blocks, no markdown formatting."
        )

        cmd = ["codex", "exec", "-c", 'model_reasoning_effort="high"']
        if self._model and self._model != "codex-default":
            cmd.extend(["-m", self._model])
        cmd.append("-")

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate(full_prompt.encode("utf-8"))

        text = stdout.decode("utf-8").strip()

        # codex exec prints metadata lines at the end, extract just the content
        # Remove trailing "tokens used\nN,NNN\n..." if present
        lines = text.split("\n")
        clean_lines: list[str] = []
        for i, line in enumerate(lines):
            if line.strip() == "tokens used" and i < len(lines) - 1:
                break
            clean_lines.append(line)
        text = "\n".join(clean_lines).strip()

        if proc.returncode != 0 and not text:
            error_msg = stderr.decode("utf-8").strip()
            logger.error("codex_error", error=error_msg[:200])
            raise RuntimeError(f"Codex CLI failed: {error_msg[:200]}")

        logger.debug("codex_response", model=self._model, length=len(text))

        return LLMResponse(text=text, model=self._model)


class GeminiCLIClient:
    """Google Gemini CLI client using subprocess.

    Calls the ``gemini`` CLI as a subprocess, allowing use without
    an API key (uses local Gemini CLI authentication).

    Parameters
    ----------
    model:
        Model to pass to gemini CLI. ``None`` or empty uses the CLI default.
    """

    def __init__(
        self,
        api_key: str = "",
        *,
        model: str | None = None,
    ) -> None:
        self._model = model if model else "gemini-cli-default"

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Generate text using Gemini CLI subprocess."""
        import asyncio

        full_prompt = ""
        if system:
            full_prompt += f"[System Instructions]\n{system}\n\n"
        full_prompt += f"[User Request]\n{prompt}"
        if json_mode:
            full_prompt += "\n\nRespond ONLY with valid JSON, no markdown."
        full_prompt += (
            "\n\nRespond directly with the requested content only."
            " No explanations, no code blocks, no markdown formatting."
        )

        cmd = ["gemini"]
        if self._model and self._model != "gemini-cli-default":
            cmd.extend(["-m", self._model])
        cmd.append("--yolo")

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate(full_prompt.encode("utf-8"))

        text = stdout.decode("utf-8").strip()

        if proc.returncode != 0 and not text:
            error_msg = stderr.decode("utf-8").strip()
            logger.error("gemini_cli_error", error=error_msg[:200])
            raise RuntimeError(f"Gemini CLI failed: {error_msg[:200]}")

        logger.debug("gemini_cli_response", model=self._model, length=len(text))

        return LLMResponse(text=text, model=self._model)


class FallbackLLMClient:
    """Wrapper that tries a primary client and falls back on error.

    Parameters
    ----------
    primary:
        The primary LLM client to try first.
    fallback:
        The fallback client to use when the primary fails.
    """

    def __init__(self, primary: LLMClient, fallback: LLMClient) -> None:
        self._primary = primary
        self._fallback = fallback

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        json_mode: bool = False,
    ) -> LLMResponse:
        """Try primary client, fall back on error."""
        try:
            return await self._primary.generate(
                prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode,
            )
        except Exception as exc:
            logger.warning(
                "primary_llm_failed_fallback",
                error=str(exc)[:200],
            )
            return await self._fallback.generate(
                prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                json_mode=json_mode,
            )


def create_llm_client(
    provider: str,
    api_key: str,
    *,
    model: str | None = None,
) -> LLMClient:
    """Factory function to create an LLM client.

    Parameters
    ----------
    provider:
        One of ``"codex"``, ``"gemini_cli"``, ``"gemini"``, or ``"claude"``.
    api_key:
        API key for the provider (unused for CLI-based providers).
    model:
        Optional model override. Uses provider default if ``None``.

    Returns
    -------
    LLMClient
        A configured client instance.
    """
    if provider == "codex":
        kwargs: dict[str, Any] = {}
        if model:
            kwargs["model"] = model
        return CodexClient(**kwargs)
    if provider == "gemini_cli":
        kwargs = {}
        if model:
            kwargs["model"] = model
        return GeminiCLIClient(**kwargs)
    if provider == "gemini":
        kwargs = {"api_key": api_key}
        if model:
            kwargs["model"] = model
        return GeminiClient(**kwargs)
    if provider == "claude":
        kwargs = {"api_key": api_key}
        if model:
            kwargs["model"] = model
        return ClaudeClient(**kwargs)
    msg = f"Unknown LLM provider: {provider!r}. Use 'codex', 'gemini_cli', 'gemini', or 'claude'."
    raise ValueError(msg)


def create_llm_client_with_fallback(
    provider: str,
    fallback_provider: str,
    api_key: str = "",
    *,
    model: str | None = None,
    fallback_model: str | None = None,
) -> LLMClient:
    """Create an LLM client with automatic fallback.

    Parameters
    ----------
    provider:
        Primary provider name.
    fallback_provider:
        Fallback provider name (used when primary fails).
    api_key:
        API key (unused for CLI providers).
    model:
        Optional model override for primary provider.
    fallback_model:
        Optional model override for fallback provider.

    Returns
    -------
    LLMClient
        A FallbackLLMClient wrapping primary and fallback clients.
    """
    primary = create_llm_client(provider, api_key, model=model)
    fallback = create_llm_client(fallback_provider, api_key, model=fallback_model)
    return FallbackLLMClient(primary, fallback)
