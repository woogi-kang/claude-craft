#!/usr/bin/env python3
"""fix-frontmatter.py — Auto-add YAML frontmatter to SKILL.md files that lack it.

Usage:
    python3 scripts/fix-frontmatter.py              # apply fixes
    python3 scripts/fix-frontmatter.py --dry-run    # preview only
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Category mapping: top-level directory emoji prefix → category label
CATEGORY_MAP = {
    "💻 개발": "💻 개발",
    "🎯 기획": "🎯 기획",
    "🎨 디자인": "🎨 디자인",
    "📝 콘텐츠": "📝 콘텐츠",
    "📣 마케팅": "📣 마케팅",
    "⚖️ 법무": "⚖️ 법무",
    "💰 재무": "💰 재무",
    "🔍 리뷰": "🔍 리뷰",
}


def detect_category(skill_path: Path, skills_root: Path) -> str:
    """Determine category from the directory path relative to skills root."""
    try:
        rel = skill_path.parent.relative_to(skills_root)
    except ValueError:
        return "standalone"
    parts = rel.parts
    if not parts:
        return "standalone"
    top_dir = parts[0]
    return CATEGORY_MAP.get(top_dir, "standalone")


def to_kebab(name: str) -> str:
    """Convert a directory name to kebab-case, stripping leading numbers."""
    # Remove leading number prefix like "4-", "16-", "S8-"
    cleaned = re.sub(r"^[sS]?\d+-", "", name)
    if not cleaned:
        cleaned = name
    # Replace underscores and spaces with hyphens, lowercase
    kebab = re.sub(r"[_\s]+", "-", cleaned).lower()
    # Remove any characters that aren't alphanumeric or hyphens
    kebab = re.sub(r"[^a-z0-9-]", "", kebab)
    # Collapse multiple hyphens
    kebab = re.sub(r"-{2,}", "-", kebab).strip("-")
    return kebab or "unnamed-skill"


def extract_title(content: str) -> str:
    """Extract the title from the first '# ' heading."""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_description(content: str) -> str:
    """Extract description from the first paragraph after the heading.

    Returns up to 2 lines of text, cleaned up for YAML block scalar.
    """
    lines = content.splitlines()
    found_heading = False
    desc_lines = []
    for line in lines:
        stripped = line.strip()
        if not found_heading:
            if stripped.startswith("# "):
                found_heading = True
            continue
        # Skip blank lines right after heading
        if not stripped and not desc_lines:
            continue
        # Stop at next heading, horizontal rule, or blank line after collecting
        if stripped.startswith("#") or stripped.startswith("---"):
            break
        if not stripped and desc_lines:
            break
        desc_lines.append(stripped)
        if len(desc_lines) >= 2:
            break

    return "\n".join(desc_lines) if desc_lines else "Skill description."


def build_frontmatter(name: str, description: str, category: str) -> str:
    """Build the YAML frontmatter block."""
    # Indent description lines for YAML block scalar
    desc_lines = description.splitlines()
    if len(desc_lines) == 1:
        desc_block = f"  {desc_lines[0]}"
    else:
        desc_block = "\n".join(f"  {l}" for l in desc_lines)

    return (
        f"---\n"
        f"name: {name}\n"
        f"description: |\n"
        f"{desc_block}\n"
        f"metadata:\n"
        f"  category: \"{category}\"\n"
        f"  version: \"1.0.0\"\n"
        f"---\n"
    )


def process_file(
    skill_path: Path, skills_root: Path, dry_run: bool
) -> bool:
    """Process a single SKILL.md file. Returns True if it was (or would be) fixed."""
    content = skill_path.read_text(encoding="utf-8")

    # Skip if already has frontmatter
    if content.startswith("---"):
        return False

    # Extract info
    title = extract_title(content)
    description = extract_description(content)
    category = detect_category(skill_path, skills_root)

    # Determine the skill directory name (parent of SKILL.md)
    dir_name = skill_path.parent.name
    name = to_kebab(dir_name)

    frontmatter = build_frontmatter(name, description, category)

    if dry_run:
        rel = skill_path.relative_to(skills_root)
        print(f"  [DRY-RUN] {rel}")
        print(f"    name: {name}")
        print(f"    category: {category}")
        print(f"    description: {description[:80]}{'...' if len(description) > 80 else ''}")
        print()
    else:
        new_content = frontmatter + content
        skill_path.write_text(new_content, encoding="utf-8")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add YAML frontmatter to SKILL.md files that lack it."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files.",
    )
    parser.add_argument(
        "--skills-dir",
        type=str,
        default=None,
        help="Path to skills directory (default: .claude/skills/ relative to script).",
    )
    args = parser.parse_args()

    if args.skills_dir:
        skills_root = Path(args.skills_dir).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        skills_root = script_dir.parent / ".claude" / "skills"
        skills_root = skills_root.resolve()

    if not skills_root.is_dir():
        print(f"Error: Skills directory not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    # Find all SKILL.md files
    all_skills = sorted(skills_root.rglob("SKILL.md"))
    total = len(all_skills)
    fixed = 0
    skipped = 0

    mode = "DRY-RUN" if args.dry_run else "FIX"
    print(f"===== Skill Frontmatter {mode} =====")
    print(f"Skills directory: {skills_root}")
    print(f"Total SKILL.md files: {total}")
    print()

    for skill_path in all_skills:
        was_fixed = process_file(skill_path, skills_root, args.dry_run)
        if was_fixed:
            fixed += 1
        else:
            skipped += 1

    print(f"===== Summary =====")
    print(f"Already had frontmatter (skipped): {skipped}")
    print(f"{'Would fix' if args.dry_run else 'Fixed'}:               {fixed}")
    print(f"Total:                             {total}")

    if fixed == 0:
        print("\nAll skills already have frontmatter. Nothing to do.")


if __name__ == "__main__":
    main()
