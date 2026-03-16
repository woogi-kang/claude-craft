#!/bin/bash
# Claude Code Hook: Quality Gate
# Auto-runs linters/formatters on edited files
# Triggered by PostToolUse for Edit|Write tools

set -e
INPUT=$(cat)

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
[ -z "$FILE" ] && exit 0
[ ! -f "$FILE" ] && exit 0

# Skip generated/vendored paths
case "$FILE" in
  */node_modules/*|*/.venv/*|*/dist/*|*/build/*|*/__pycache__/*) exit 0 ;;
esac

LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/quality-gate.log"

EXT="${FILE##*.}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

case "$EXT" in
  py)
    if command -v ruff &>/dev/null; then
      ruff check --fix --quiet "$FILE" 2>>"$LOG" || true
      ruff format --quiet "$FILE" 2>>"$LOG" || true
      echo "$TIMESTAMP [py] ruff: $FILE" >> "$LOG"
    fi
    ;;
  ts|tsx|js|jsx)
    if command -v npx &>/dev/null && [ -f "$(dirname "$FILE")/node_modules/.bin/biome" ] 2>/dev/null || npx biome --version &>/dev/null 2>&1; then
      npx biome check --write "$FILE" 2>>"$LOG" || true
      echo "$TIMESTAMP [js/ts] biome: $FILE" >> "$LOG"
    elif command -v npx &>/dev/null; then
      npx prettier --write "$FILE" 2>>"$LOG" || true
      echo "$TIMESTAMP [js/ts] prettier: $FILE" >> "$LOG"
    fi
    ;;
  sh|bash)
    if command -v shellcheck &>/dev/null; then
      shellcheck "$FILE" 2>>"$LOG" || true
      echo "$TIMESTAMP [sh] shellcheck: $FILE" >> "$LOG"
    fi
    ;;
esac

exit 0
