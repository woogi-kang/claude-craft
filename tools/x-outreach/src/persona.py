"""Persona system -- load, sample keywords, build prompts, validate.

Reads persona definitions from the ``personas/`` directory and provides
helpers for keyword sampling, system prompt construction, and
post-generation content validation.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from outreach_shared.utils.logger import get_logger

logger = get_logger("persona")

_PERSONAS_DIR = Path(__file__).resolve().parent.parent / "personas"


@dataclass(frozen=True)
class StyleLexicon:
    """Per-persona style rules from style_lexicon.yaml."""

    preferred_endings: tuple[str, ...]
    preferred_tokens: tuple[str, ...]
    banned_tokens: tuple[str, ...]


@dataclass(frozen=True)
class PersonaContext:
    """Immutable persona configuration resolved for a single account."""

    account_id: str
    persona_id: str
    persona_md: str
    base_policy: str
    style: StyleLexicon
    shared_banned_patterns: tuple[str, ...]
    keywords_primary: tuple[str, ...]
    keywords_secondary: tuple[str, ...]
    global_fallback_keywords: tuple[str, ...]
    stage_overrides: dict[str, dict[str, int]]


def load_persona(
    account_id: str,
    personas_dir: Path | None = None,
) -> PersonaContext | None:
    """Load persona context for *account_id*.

    Returns ``None`` when *account_id* is not found in ``accounts.yaml``
    or when a required file is missing.

    Parameters
    ----------
    account_id:
        The account identifier (e.g. ``"master_a"``).
    personas_dir:
        Override for the personas directory path.
    """
    pdir = personas_dir or _PERSONAS_DIR

    # --- accounts.yaml ---
    accounts_path = pdir / "accounts.yaml"
    if not accounts_path.exists():
        logger.warning("persona_accounts_yaml_missing", path=str(accounts_path))
        return None

    accounts_data = _load_yaml(accounts_path)
    mappings: list[dict[str, Any]] = accounts_data.get("mappings", [])
    mapping = _find_mapping(mappings, account_id)
    if mapping is None:
        logger.info("persona_account_not_found", account_id=account_id)
        return None

    persona_id: str = mapping["persona_id"]
    keyword_profile: str = mapping.get("keyword_profile", persona_id)
    stage_overrides: dict[str, dict[str, int]] = accounts_data.get("stage_overrides", {})
    global_fallback: list[str] = accounts_data.get("global_fallback_keywords", [])

    # --- persona MD file ---
    persona_md_path = _resolve_persona_md(pdir, persona_id)
    if persona_md_path is None or not persona_md_path.exists():
        logger.warning("persona_md_missing", persona_id=persona_id)
        return None
    persona_md = persona_md_path.read_text(encoding="utf-8")

    # --- base_policy.md ---
    base_policy_path = pdir / "base_policy.md"
    base_policy = ""
    if base_policy_path.exists():
        base_policy = base_policy_path.read_text(encoding="utf-8")

    # --- style_lexicon.yaml ---
    style_data = _load_yaml(pdir / "style_lexicon.yaml")
    shared_banned = style_data.get("shared_banned_patterns", [])
    persona_style_raw = style_data.get("personas", {}).get(persona_id, {})
    style = StyleLexicon(
        preferred_endings=tuple(persona_style_raw.get("preferred_endings", [])),
        preferred_tokens=tuple(persona_style_raw.get("preferred_tokens", [])),
        banned_tokens=tuple(persona_style_raw.get("banned_tokens", [])),
    )

    # --- keyword_matrix.yaml ---
    kw_data = _load_yaml(pdir / "keyword_matrix.yaml")
    profile = kw_data.get("profiles", {}).get(keyword_profile, {})
    primary_kws = [e["keyword"] for e in profile.get("primary", []) if e.get("keyword")]
    secondary_kws = [e["keyword"] for e in profile.get("secondary", []) if e.get("keyword")]

    ctx = PersonaContext(
        account_id=account_id,
        persona_id=persona_id,
        persona_md=persona_md,
        base_policy=base_policy,
        style=style,
        shared_banned_patterns=tuple(shared_banned),
        keywords_primary=tuple(primary_kws),
        keywords_secondary=tuple(secondary_kws),
        global_fallback_keywords=tuple(global_fallback),
        stage_overrides=stage_overrides,
    )
    logger.info("persona_loaded", account_id=account_id, persona_id=persona_id)
    return ctx


# ---------------------------------------------------------------------------
# Keyword sampling
# ---------------------------------------------------------------------------


def sample_keywords(persona: PersonaContext, count: int = 8) -> list[str]:
    """Sample search keywords for a persona run.

    Algorithm (per ``personas/README.md`` section 6):
    - 4-6 keywords from ``primary``
    - 1-2 keywords from ``secondary``
    - If total < *count*, pad from ``global_fallback_keywords``

    Parameters
    ----------
    persona:
        Loaded persona context.
    count:
        Target number of keywords.
    """
    primary = list(persona.keywords_primary)
    secondary = list(persona.keywords_secondary)
    fallback = list(persona.global_fallback_keywords)

    random.shuffle(primary)
    random.shuffle(secondary)
    random.shuffle(fallback)

    # Take 4-6 primary (capped by availability)
    n_primary = min(random.randint(4, 6), len(primary))
    selected = primary[:n_primary]

    # Take 1-2 secondary
    n_secondary = min(random.randint(1, 2), len(secondary))
    selected.extend(secondary[:n_secondary])

    # Pad from fallback if needed (deduplicated)
    if len(selected) < count:
        existing = set(selected)
        for kw in fallback:
            if kw not in existing:
                selected.append(kw)
                existing.add(kw)
            if len(selected) >= count:
                break

    return selected[:count]


# ---------------------------------------------------------------------------
# Prompt building
# ---------------------------------------------------------------------------


def build_persona_system_prompt(base_stage_prompt: str, persona: PersonaContext) -> str:
    """Build a layered system prompt with persona context.

    Layering order (per ``personas/README.md`` section 5):
    1. Base safety policy
    2. Persona profile (MD content)
    3. Style lexicon rules
    4. Original stage prompt (reply/DM/post)

    Parameters
    ----------
    base_stage_prompt:
        The original hardcoded system prompt (e.g. ``REPLY_SYSTEM_PROMPT``).
    persona:
        Loaded persona context.
    """
    style_section = (
        f"## Style Rules for {persona.persona_id}\n"
        f"- Preferred sentence endings: {', '.join(persona.style.preferred_endings)}\n"
        f"- Preferred vocabulary: {', '.join(persona.style.preferred_tokens)}\n"
        f"- BANNED words/phrases (NEVER use): "
        f"{', '.join(list(persona.style.banned_tokens) + list(persona.shared_banned_patterns))}\n"
    )

    return (
        f"{persona.base_policy}\n\n"
        f"{persona.persona_md}\n\n"
        f"{style_section}\n\n"
        f"{base_stage_prompt}"
    )


# ---------------------------------------------------------------------------
# Content validation
# ---------------------------------------------------------------------------


def validate_persona_content(
    text: str,
    persona: PersonaContext,
    stage: str,
) -> tuple[bool, list[str]]:
    """Validate generated text against persona rules.

    Checks:
    - Banned tokens (per-persona + shared)
    - Character length from ``stage_overrides``

    Parameters
    ----------
    text:
        The generated content.
    persona:
        Loaded persona context.
    stage:
        Pipeline stage: ``"reply"``, ``"dm"``, or ``"post"``.

    Returns
    -------
    tuple[bool, list[str]]
        ``(is_valid, list_of_violations)``
    """
    from src.ai.content_gen import x_weighted_len

    violations: list[str] = []

    # Check banned tokens
    all_banned = list(persona.style.banned_tokens) + list(persona.shared_banned_patterns)
    for token in all_banned:
        if token in text:
            violations.append(f"banned_token: {token}")

    # Check stage char limit
    overrides = persona.stage_overrides.get(stage, {})
    max_chars = overrides.get("max_chars")
    if max_chars is not None:
        actual = x_weighted_len(text)
        if actual > max_chars:
            violations.append(f"char_limit: {actual}/{max_chars}")

    return (len(violations) == 0, violations)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file, returning empty dict on missing or invalid files."""
    if not path.exists():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except (yaml.YAMLError, OSError) as exc:
        logger.warning("yaml_load_error", path=str(path), error=str(exc)[:200])
        return {}
    return data if isinstance(data, dict) else {}


def _find_mapping(
    mappings: list[dict[str, Any]],
    account_id: str,
) -> dict[str, Any] | None:
    """Find the mapping entry for *account_id*."""
    for m in mappings:
        if m.get("account_id") == account_id:
            return m
    return None


def _resolve_persona_md(personas_dir: Path, persona_id: str) -> Path | None:
    """Find the MD file for *persona_id*.

    Tries two naming patterns:
    - ``p01_price.md`` (persona_id as-is)
    - ``p01_*.md`` (prefix match for the numeric part)
    """
    # Direct match: persona_id as filename
    direct = personas_dir / f"{persona_id}.md"
    if direct.exists():
        return direct

    # Prefix match: extract the pXX prefix
    parts = persona_id.split("_", 1)
    if len(parts) >= 1:
        prefix = parts[0]
        for p in personas_dir.glob(f"{prefix}_*.md"):
            return p

    return None
