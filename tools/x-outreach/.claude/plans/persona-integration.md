# Persona Integration Plan

## Context

The x-outreach pipeline currently operates with a single generic voice for all content (reply/DM/posting). The `personas/` directory defines 5 specialized personas with distinct voices, keywords, and style rules, but none of this is wired into the pipeline code. This plan integrates the persona system so each account produces content matching its assigned persona voice.

User requirement: account maps directly to persona (no indirection via keyword_profile).

## Architecture: Single New Module + Minimal Injection

One new file `src/persona.py` handles all persona logic. Existing files receive an optional `persona` parameter -- when `None`, behavior is identical to current (full backward compat).

---

## Changes by File

### 1. NEW: `src/persona.py` -- Core persona module

**Data classes:**
- `StyleLexicon(preferred_endings, preferred_tokens, banned_tokens)` -- frozen dataclass
- `PersonaContext(account_id, persona_id, persona_md, base_policy, style, shared_banned_patterns, keywords_primary, keywords_secondary, global_fallback_keywords, stage_overrides)` -- frozen dataclass

**Functions:**
- `load_persona(account_id, personas_dir?) -> PersonaContext | None` -- reads accounts.yaml, persona MD, base_policy.md, style_lexicon.yaml, keyword_matrix.yaml; returns None if account not found
- `sample_keywords(persona, count=8) -> list[str]` -- 4-6 primary + 1-2 secondary + global fallback per README section 6
- `build_persona_system_prompt(base_prompt, persona) -> str` -- layers: base_policy + persona_md + style rules + original stage prompt
- `validate_persona_content(text, persona, stage) -> tuple[bool, list[str]]` -- checks banned tokens (shared + persona-specific), stage char limits

### 2. MODIFY: `src/ai/content_gen.py`

- Add `persona: PersonaContext | None = None` parameter to `generate_reply()`, `generate_dm()`, `generate_casual_post()`, `generate_knowledge_post()`
- When persona is set: use `build_persona_system_prompt()` instead of hardcoded prompt, use stage_overrides for truncation limit, run `validate_persona_content()` after generation with warning log on violations
- When persona is None: exact current behavior (backward compat)

### 3. MODIFY: `src/main.py` -- PipelineRunner

- Add `account_id: str | None = None` to `run_once()` signature
- At top: `persona = load_persona(account_id)` if account_id provided
- Search keywords: `sample_keywords(persona)` if persona else `settings.search.keywords`
- Pass `persona=persona` to ReplyPipeline, DmPipeline, PostingPipeline constructors
- Pass `persona=persona` to ContentGenerator (via pipelines, not constructor)

### 4. MODIFY: `src/pipeline/reply.py` -- ReplyPipeline

- Add `persona: PersonaContext | None = None` to `__init__()`, store as `self._persona`
- Pass `persona=self._persona` to `content_gen.generate_reply()` call
- Log persona_id on reply_sent

### 5. MODIFY: `src/pipeline/dm.py` -- DmPipeline

- Same pattern: add `persona` to `__init__()`, pass to `content_gen.generate_dm()`

### 6. MODIFY: `src/pipeline/posting.py` -- PostingPipeline

- Same pattern: add `persona` to `__init__()`, pass to `generate_casual_post()` and `generate_knowledge_post()`

### 7. MODIFY: `src/pipeline/track.py` -- ActionTracker

- Add optional `persona_id: str | None = None` to `record_reply()`, `record_dm()`, `record_post()`
- Include persona_id in details string for database recording

### 8. MODIFY: `src/db/repository.py`

- `record_nurture_action()`: change hardcoded `account_id="master"` to parameterized with default

### 9. MODIFY: `src/daemon.py`

- Minimal: pass `account_id` to `runner.run_once()` (default None for backward compat, configurable for single-persona operation)

### 10. NEW: `tests/test_persona.py`

Tests for persona loading, keyword sampling, prompt building, content validation:
- `test_load_persona_valid` / `test_load_persona_unknown_returns_none`
- `test_sample_keywords_count_and_composition`
- `test_build_prompt_layering_order`
- `test_validate_catches_banned_tokens` / `test_validate_catches_shared_banned`
- `test_validate_respects_stage_char_limits`
- `test_backward_compat_none_persona`

### 11. MODIFY: `tests/test_content_gen.py`

Add tests for persona-aware generation:
- `test_generate_reply_with_persona`
- `test_generate_dm_with_persona`

---

## Implementation Order

1. Create `src/persona.py` (self-contained, no dependencies on changes elsewhere)
2. Create `tests/test_persona.py` and verify
3. Modify `src/ai/content_gen.py` (add persona parameter)
4. Modify pipeline files (reply.py, dm.py, posting.py)
5. Modify `src/main.py` (wire account_id -> persona -> keywords/pipelines)
6. Modify `src/pipeline/track.py` and `src/db/repository.py` (tracking)
7. Modify `src/daemon.py` (minimal)
8. Update/add tests for modified files
9. Run full test suite to verify backward compatibility

## Verification

1. `pytest tools/x-outreach/tests/` -- all existing + new tests pass
2. Manual: `python -m src.main run --account-id master_a` -- verify persona-specific keywords and voice in generated content
3. Check logs for `persona_loaded`, `persona_id=p01_price` entries
