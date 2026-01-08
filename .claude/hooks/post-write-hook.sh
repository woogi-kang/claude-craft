#!/bin/bash

# Post-Write Hook for Claude Code
# Triggers documentation sync when agent/skill files are modified
#
# Usage: Called automatically by Claude Code after Write/Edit operations
# Input: $1 = file path that was modified

# Exit silently if no file path provided
if [ -z "${1:-}" ]; then
    exit 0
fi

FILE_PATH="$1"

# Get script directory (macOS/Linux compatible)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if the modified file is in .claude/agents/ or .claude/skills/ directory
# This supports both ~/.claude/ and project/.claude/ structures
if [[ "$FILE_PATH" == *"/.claude/agents/"* ]] || [[ "$FILE_PATH" == *"/.claude/skills/"* ]] || \
   [[ "$FILE_PATH" == *"/agents/"* ]] || [[ "$FILE_PATH" == *"/skills/"* ]]; then
    # Check if it's an AGENT.md or SKILL.md file
    if [[ "$FILE_PATH" == *"AGENT.md" ]] || [[ "$FILE_PATH" == *"SKILL.md" ]]; then
        # Run sync-docs in background to not block Claude Code
        bash "$SCRIPT_DIR/sync-docs.sh" >> /tmp/claude-craft-sync.log 2>&1 &
    fi
fi
