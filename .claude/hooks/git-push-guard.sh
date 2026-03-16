#!/bin/bash
# Claude Code Hook: Git Push Guard
# Warns before git push to remote (PreToolUse for Bash)

INPUT=$(cat) || exit 0

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null) || exit 0
[ -z "$COMMAND" ] && exit 0

# Only intercept git push commands
case "$COMMAND" in
  *"git push"*) ;;
  *) exit 0 ;;
esac

# Check for force push (extra dangerous)
case "$COMMAND" in
  *"--force"*|*" -f "*|*" -f")
    echo '{"decision":"block","reason":"Force push detected. This is destructive and may overwrite remote history. Please confirm with the user first."}'
    exit 0
    ;;
esac

# Allow normal push but log it
LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/logs"
mkdir -p "$LOG_DIR"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") git-push: $COMMAND" >> "$LOG_DIR/git-push.log"

exit 0
