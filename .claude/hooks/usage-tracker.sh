#!/bin/bash
# Claude Code Hook: Usage Tracker
# Logs Agent/Skill tool invocations to .claude/logs/usage.jsonl
#
# Triggered by PostToolUse events (configured in settings.json)
# Reads JSON from stdin per Claude Code hooks spec

set -e

INPUT=$(cat)

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')

LOG_DIR="$(cd "$(dirname "$0")/.." && pwd)/logs"
LOG_FILE="$LOG_DIR/usage.jsonl"
mkdir -p "$LOG_DIR"

case "$TOOL_NAME" in
  Agent)
    NAME=$(echo "$INPUT" | jq -r '.tool_input.description // .tool_input.subagent_type // "unknown"')
    TYPE=$(echo "$INPUT" | jq -r '.tool_input.subagent_type // "general-purpose"')
    jq -n \
      --arg ts "$TIMESTAMP" \
      --arg sid "$SESSION_ID" \
      --arg tool "agent" \
      --arg name "$NAME" \
      --arg subtype "$TYPE" \
      '{timestamp:$ts, session_id:$sid, tool:$tool, name:$name, subagent_type:$subtype}' \
      >> "$LOG_FILE"
    ;;
  Skill)
    NAME=$(echo "$INPUT" | jq -r '.tool_input.skill // "unknown"')
    ARGS=$(echo "$INPUT" | jq -r '.tool_input.args // ""')
    jq -n \
      --arg ts "$TIMESTAMP" \
      --arg sid "$SESSION_ID" \
      --arg tool "skill" \
      --arg name "$NAME" \
      --arg args "$ARGS" \
      '{timestamp:$ts, session_id:$sid, tool:$tool, name:$name, args:$args}' \
      >> "$LOG_FILE"
    ;;
esac

exit 0
