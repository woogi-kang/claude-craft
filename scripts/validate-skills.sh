#!/usr/bin/env bash
# validate-skills.sh — Check all SKILL.md files for YAML frontmatter
# Exit 0 if all valid, 1 if any missing

set -euo pipefail

SKILLS_DIR="${1:-$(dirname "$0")/../.claude/skills}"
SKILLS_DIR="$(cd "$SKILLS_DIR" && pwd)"

total=0
with_fm=0
without_fm=0
missing_files=()

while IFS= read -r -d '' file; do
  total=$((total + 1))
  first_line=$(head -1 "$file")
  if [ "$first_line" = "---" ]; then
    with_fm=$((with_fm + 1))
  else
    without_fm=$((without_fm + 1))
    missing_files+=("$file")
  fi
done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0)

echo "===== Skill Frontmatter Validation ====="
echo "Skills directory: $SKILLS_DIR"
echo ""
echo "Total SKILL.md files:        $total"
echo "With frontmatter:            $with_fm"
echo "Without frontmatter:         $without_fm"
echo ""

if [ "$without_fm" -eq 0 ]; then
  echo "All skills have frontmatter."
  exit 0
else
  echo "Files missing frontmatter:"
  for f in "${missing_files[@]}"; do
    echo "  $f"
  done
  exit 1
fi
