"""Tests for the persona loading and validation module."""

from __future__ import annotations

import pytest

from src.persona import (
    PersonaContext,
    StyleLexicon,
    build_persona_system_prompt,
    load_persona,
    sample_keywords,
    validate_persona_content,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def persona_price() -> PersonaContext:
    """Load the p01_price persona for master_a."""
    ctx = load_persona("master_a")
    assert ctx is not None
    return ctx


@pytest.fixture
def persona_beginner() -> PersonaContext:
    """Load the p02_beginner_guide persona for master_b."""
    ctx = load_persona("master_b")
    assert ctx is not None
    return ctx


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


class TestLoadPersona:
    """Test persona loading from YAML/MD files."""

    def test_load_valid_account(self) -> None:
        ctx = load_persona("master_a")
        assert ctx is not None
        assert ctx.account_id == "master_a"
        assert ctx.persona_id == "p01_price"

    def test_load_all_five_accounts(self) -> None:
        expected = {
            "master_a": "p01_price",
            "master_b": "p02_beginner_guide",
            "master_c": "p03_procedure_explainer",
            "master_d": "p04_risk_care",
            "master_e": "p05_lifestyle",
        }
        for account_id, persona_id in expected.items():
            ctx = load_persona(account_id)
            assert ctx is not None, f"Failed to load {account_id}"
            assert ctx.persona_id == persona_id

    def test_load_unknown_account_returns_none(self) -> None:
        assert load_persona("nonexistent_account") is None

    def test_persona_md_not_empty(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.persona_md) > 0
        assert "p01_price" in persona_price.persona_md.lower() or "Price" in persona_price.persona_md

    def test_base_policy_loaded(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.base_policy) > 0
        assert "Non-Negotiable" in persona_price.base_policy or "Policy" in persona_price.base_policy

    def test_style_lexicon_loaded(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.style.preferred_endings) > 0
        assert len(persona_price.style.preferred_tokens) > 0
        assert len(persona_price.style.banned_tokens) > 0

    def test_shared_banned_patterns_loaded(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.shared_banned_patterns) > 0
        assert "100%" in persona_price.shared_banned_patterns

    def test_keywords_loaded(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.keywords_primary) > 0
        assert len(persona_price.keywords_secondary) > 0

    def test_global_fallback_keywords_loaded(self, persona_price: PersonaContext) -> None:
        assert len(persona_price.global_fallback_keywords) > 0

    def test_stage_overrides_loaded(self, persona_price: PersonaContext) -> None:
        assert "reply" in persona_price.stage_overrides
        assert persona_price.stage_overrides["reply"]["max_chars"] == 260

    def test_persona_context_is_immutable(self, persona_price: PersonaContext) -> None:
        with pytest.raises(AttributeError):
            persona_price.persona_id = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Keyword sampling
# ---------------------------------------------------------------------------


class TestSampleKeywords:
    """Test keyword sampling logic."""

    def test_returns_list(self, persona_price: PersonaContext) -> None:
        kws = sample_keywords(persona_price)
        assert isinstance(kws, list)

    def test_respects_count(self, persona_price: PersonaContext) -> None:
        kws = sample_keywords(persona_price, count=6)
        assert len(kws) <= 6

    def test_default_count_is_8(self, persona_price: PersonaContext) -> None:
        kws = sample_keywords(persona_price)
        assert len(kws) <= 8

    def test_includes_primary_keywords(self, persona_price: PersonaContext) -> None:
        """At least some primary keywords should be included."""
        kws = sample_keywords(persona_price, count=8)
        primary_set = set(persona_price.keywords_primary)
        assert any(kw in primary_set for kw in kws)

    def test_no_duplicates(self, persona_price: PersonaContext) -> None:
        kws = sample_keywords(persona_price, count=8)
        assert len(kws) == len(set(kws))

    def test_small_count(self, persona_price: PersonaContext) -> None:
        kws = sample_keywords(persona_price, count=2)
        assert len(kws) <= 2


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------


class TestBuildPersonaSystemPrompt:
    """Test system prompt construction with persona layers."""

    def test_contains_base_policy(self, persona_price: PersonaContext) -> None:
        prompt = build_persona_system_prompt("Stage prompt here.", persona_price)
        # base_policy content should appear before everything else
        assert persona_price.base_policy[:50] in prompt

    def test_contains_persona_md(self, persona_price: PersonaContext) -> None:
        prompt = build_persona_system_prompt("Stage prompt here.", persona_price)
        assert "p01_price" in prompt.lower() or "Price" in prompt

    def test_contains_style_rules(self, persona_price: PersonaContext) -> None:
        prompt = build_persona_system_prompt("Stage prompt here.", persona_price)
        assert "Style Rules" in prompt
        assert "Preferred sentence endings" in prompt
        assert "BANNED" in prompt

    def test_contains_stage_prompt(self, persona_price: PersonaContext) -> None:
        stage_prompt = "You are a Korean dermatology specialist."
        prompt = build_persona_system_prompt(stage_prompt, persona_price)
        assert stage_prompt in prompt

    def test_layering_order(self, persona_price: PersonaContext) -> None:
        """base_policy -> persona_md -> style -> stage prompt."""
        prompt = build_persona_system_prompt("STAGE_MARKER", persona_price)
        policy_pos = prompt.find("Base Persona Policy")
        style_pos = prompt.find("Style Rules")
        stage_pos = prompt.find("STAGE_MARKER")
        assert policy_pos < style_pos < stage_pos

    def test_banned_tokens_include_shared(self, persona_price: PersonaContext) -> None:
        prompt = build_persona_system_prompt("test", persona_price)
        assert "100%" in prompt
        assert "激安" in prompt  # p01_price specific banned token


# ---------------------------------------------------------------------------
# Content validation
# ---------------------------------------------------------------------------


class TestValidatePersonaContent:
    """Test post-generation content validation."""

    def test_clean_text_passes(self, persona_price: PersonaContext) -> None:
        text = "韓国の皮膚科の価格帯を比較してみたよ"
        valid, violations = validate_persona_content(text, persona_price, "reply")
        assert valid is True
        assert violations == []

    def test_catches_persona_banned_token(self, persona_price: PersonaContext) -> None:
        text = "この施術は激安だから行くべき"
        valid, violations = validate_persona_content(text, persona_price, "reply")
        assert valid is False
        assert any("激安" in v for v in violations)

    def test_catches_shared_banned_pattern(self, persona_price: PersonaContext) -> None:
        text = "100%効果があるよ"
        valid, violations = validate_persona_content(text, persona_price, "reply")
        assert valid is False
        assert any("100%" in v for v in violations)

    def test_catches_char_limit_reply(self, persona_price: PersonaContext) -> None:
        # stage_overrides.reply.max_chars = 260
        # 150 CJK chars = 300 weighted > 260
        long_text = "あ" * 150
        valid, violations = validate_persona_content(long_text, persona_price, "reply")
        assert valid is False
        assert any("char_limit" in v for v in violations)

    def test_within_char_limit_passes(self, persona_price: PersonaContext) -> None:
        # 50 CJK chars = 100 weighted < 260
        text = "あ" * 50
        valid, violations = validate_persona_content(text, persona_price, "reply")
        assert valid is True

    def test_dm_char_limit(self, persona_price: PersonaContext) -> None:
        # stage_overrides.dm.max_chars = 480
        long_text = "い" * 250  # 500 weighted > 480
        valid, violations = validate_persona_content(long_text, persona_price, "dm")
        assert valid is False
        assert any("char_limit" in v for v in violations)

    def test_unknown_stage_no_char_check(self, persona_price: PersonaContext) -> None:
        text = "あ" * 200  # 400 weighted, but stage 'nurture' has no override
        valid, violations = validate_persona_content(text, persona_price, "nurture")
        assert valid is True

    def test_multiple_violations(self, persona_price: PersonaContext) -> None:
        # Both banned token AND over char limit
        long_banned = "激安" + "あ" * 150
        valid, violations = validate_persona_content(long_banned, persona_price, "reply")
        assert valid is False
        assert len(violations) >= 2

    def test_beginner_persona_banned_tokens(self, persona_beginner: PersonaContext) -> None:
        text = "自己責任で行ってね"
        valid, violations = validate_persona_content(text, persona_beginner, "reply")
        assert valid is False
        assert any("自己責任" in v for v in violations)
