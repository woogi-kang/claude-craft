#!/usr/bin/env python3
"""
Skill Catalog Generator

Scans all SKILL.md files under .claude/skills/ and generates a structured
markdown catalog at docs/skill-catalog.md.

Usage:
    python scripts/skill-catalog.py
"""

import os
import re
from datetime import date
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────────

SKILLS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "skills"
OUTPUT_FILE = Path(__file__).resolve().parent.parent / "docs" / "skill-catalog.md"

# Categories that map to emoji-prefixed directories
CATEGORY_DIRS = {
    "💻 개발": "💻 개발",
    "🎯 기획": "🎯 기획",
    "🎨 디자인": "🎨 디자인",
    "📝 콘텐츠": "📝 콘텐츠",
    "📣 마케팅": "📣 마케팅",
    "⚖️ 법무": "⚖️ 법무",
    "💰 재무": "💰 재무",
}

CATEGORY_ORDER = [
    "💻 개발",
    "🎯 기획",
    "🎨 디자인",
    "📝 콘텐츠",
    "📣 마케팅",
    "⚖️ 법무",
    "💰 재무",
    "Standalone",
]


# ── YAML Frontmatter Parser (stdlib only) ──────────────────────────────────

def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content. Returns a dict."""
    if not content.startswith("---"):
        return {}

    end = content.find("\n---", 3)
    if end == -1:
        return {}

    yaml_block = content[4:end]
    return _parse_yaml_simple(yaml_block)


def _parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for frontmatter fields we care about.

    Handles:
      - key: value (scalars)
      - key: "quoted value"
      - key: | (multiline literal — join lines)
      - nested mapping one level deep (e.g. metadata.version)
      - list items (- value)
    """
    result = {}
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip blank lines and comments
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        # Top-level key
        m = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if not m:
            i += 1
            continue

        key = m.group(1)
        value = m.group(2).strip()

        if value == "|":
            # Multiline literal block
            parts = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or lines[i].strip() == ""):
                parts.append(lines[i].strip())
                i += 1
            result[key] = " ".join(p for p in parts if p)
            continue

        if value == "" or value == ">":
            # Could be a nested mapping or list
            nested = {}
            items = []
            i += 1
            while i < len(lines):
                child = lines[i]
                if not child.startswith("  ") and child.strip():
                    break
                child_stripped = child.strip()
                if not child_stripped:
                    i += 1
                    continue
                # List item
                if child_stripped.startswith("- "):
                    items.append(_unquote(child_stripped[2:].strip()))
                    i += 1
                    continue
                # Nested key: value
                nm = re.match(r"^\s+([\w-]+)\s*:\s*(.*)", child)
                if nm:
                    nested[nm.group(1)] = _unquote(nm.group(2).strip())
                i += 1

            if items:
                result[key] = items
            elif nested:
                result[key] = nested
            continue

        result[key] = _unquote(value)
        i += 1

    return result


def _unquote(s: str) -> str:
    """Remove surrounding quotes from a string."""
    if len(s) >= 2:
        if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
            return s[1:-1]
    return s


# ── Skill Extraction ──────────────────────────────────────────────────────

def extract_skill_info(filepath: Path, skills_root: Path) -> dict:
    """Extract metadata from a single SKILL.md file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    fm = parse_frontmatter(content)

    # Remove frontmatter from content for heading/paragraph extraction
    body = content
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            body = content[end + 4:].lstrip("\n")

    # Name: prefer frontmatter, then first heading
    name = fm.get("name", "")
    if not name:
        hm = re.search(r"^#\s+(.+)", body, re.MULTILINE)
        if hm:
            name = hm.group(1).strip()

    # Description: prefer frontmatter, then first paragraph after heading
    description = fm.get("description", "")
    if not description:
        # Find first non-empty line after the first heading
        lines = body.split("\n")
        found_heading = False
        for line in lines:
            stripped = line.strip()
            if not found_heading:
                if stripped.startswith("# "):
                    found_heading = True
                continue
            if stripped and not stripped.startswith("#") and not stripped.startswith("|") and not stripped.startswith("-"):
                description = stripped
                break

    # Truncate long descriptions
    if len(description) > 120:
        description = description[:117] + "..."

    # Version: frontmatter top-level or metadata.version
    version = fm.get("version", "")
    metadata = fm.get("metadata", {})
    if isinstance(metadata, dict) and not version:
        version = metadata.get("version", "")

    # Tags: frontmatter tags
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    # Relative path from skills root
    rel_path = filepath.parent.relative_to(skills_root)

    # Determine category from directory structure (emoji-prefixed dirs only)
    parts = rel_path.parts
    category = "Standalone"
    if parts:
        first_dir = parts[0]
        for cat_name in CATEGORY_DIRS:
            if first_dir == cat_name:
                category = cat_name
                break

    return {
        "name": name or rel_path.name,
        "description": description,
        "version": version,
        "tags": tags if isinstance(tags, list) else [],
        "category": category,
        "path": str(rel_path),
    }


def collect_skills(skills_root: Path) -> list:
    """Walk the skills directory and collect all SKILL.md entries."""
    skills = []
    for dirpath, _dirnames, filenames in os.walk(skills_root):
        for fname in filenames:
            if fname == "SKILL.md":
                filepath = Path(dirpath) / fname
                info = extract_skill_info(filepath, skills_root)
                if info:
                    skills.append(info)
    return skills


# ── Catalog Generation ─────────────────────────────────────────────────────

def generate_catalog(skills: list) -> str:
    """Generate the markdown catalog string."""
    # Group by category
    by_category: dict[str, list] = {}
    for s in skills:
        by_category.setdefault(s["category"], []).append(s)

    # Sort each group alphabetically by name
    for cat in by_category:
        by_category[cat].sort(key=lambda s: s["name"].lower())

    # Collect all tags
    tag_index: dict[str, list] = {}
    for s in skills:
        for tag in s["tags"]:
            tag_index.setdefault(tag, []).append(s["name"])

    # Category list for summary
    categories_present = [c for c in CATEGORY_ORDER if c in by_category]
    # Add any unexpected categories
    for c in sorted(by_category.keys()):
        if c not in categories_present:
            categories_present.append(c)

    total = len(skills)
    today = date.today().isoformat()

    lines = []
    lines.append("# Skill Catalog")
    lines.append("")
    lines.append(f"> Auto-generated by `scripts/skill-catalog.py` — do not edit manually.")
    lines.append(f"> Last updated: {today}")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append(f"- **Total skills:** {total}")
    lines.append(f"- **Categories:** {', '.join(categories_present)}")
    lines.append("")

    # By Category
    lines.append("## By Category")
    lines.append("")

    for cat in categories_present:
        group = by_category[cat]
        lines.append(f"### {cat} ({len(group)})")
        lines.append("")
        lines.append("| Skill | Description | Version | Path |")
        lines.append("|-------|-------------|---------|------|")
        for s in group:
            name = _escape_pipe(s["name"])
            desc = _escape_pipe(s["description"])
            ver = s["version"] or "—"
            path = _escape_pipe(s["path"])
            lines.append(f"| {name} | {desc} | {ver} | {path} |")
        lines.append("")

    # Tag Index
    if tag_index:
        lines.append("## Tag Index")
        lines.append("")
        lines.append("| Tag | Skills |")
        lines.append("|-----|--------|")
        for tag in sorted(tag_index.keys(), key=str.lower):
            skill_names = sorted(set(tag_index[tag]), key=str.lower)
            lines.append(f"| {tag} | {', '.join(skill_names)} |")
        lines.append("")

    # Regeneration
    lines.append("## Regeneration")
    lines.append("")
    lines.append("```bash")
    lines.append("python scripts/skill-catalog.py")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def _escape_pipe(s: str) -> str:
    """Escape pipe characters for markdown tables."""
    return s.replace("|", "\\|")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if not SKILLS_DIR.is_dir():
        print(f"Error: Skills directory not found: {SKILLS_DIR}")
        raise SystemExit(1)

    print(f"Scanning skills in {SKILLS_DIR} ...")
    skills = collect_skills(SKILLS_DIR)
    print(f"Found {len(skills)} skills.")

    catalog = generate_catalog(skills)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(catalog, encoding="utf-8")
    print(f"Catalog written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
