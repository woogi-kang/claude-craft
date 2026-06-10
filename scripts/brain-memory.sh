#!/usr/bin/env bash
# brain-memory.sh - Claude Craft wrapper for the local GBrain memory engine.

set -euo pipefail

GBRAIN_BIN="${GBRAIN_BIN:-$HOME/.bun/bin/gbrain}"
BRAIN_REPO="${BRAIN_REPO:-$HOME/brain-craft}"
BRAIN_SOURCE="${BRAIN_SOURCE:-brain-craft}"
DEFAULT_TIMEOUT_SECONDS="${BRAIN_TIMEOUT_SECONDS:-30}"

usage() {
  cat <<'EOF'
Usage: scripts/brain-memory.sh <command> [args]

Commands:
  status                         Show GBrain identity, stats, sources, and search mode
  search <query>                 Search long-term memory
  get <slug>                     Read a memory page
  sync                           Commit-safe sync of brain-craft into GBrain
  secret-scan                    Scan brain-craft for likely secrets
  capture <type> <slug> <title>  Create a typed memory page from stdin, commit, sync
  capture-decision <slug> <title>
                                 Create decisions/<slug>.md from stdin, commit, sync

Environment:
  GBRAIN_BIN=/path/to/gbrain     Default: $HOME/.bun/bin/gbrain
  BRAIN_REPO=/path/to/brain      Default: $HOME/brain-craft
  BRAIN_SOURCE=source-id         Default: brain-craft
  BRAIN_TIMEOUT_SECONDS=30       Command timeout for status/search/get
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_gbrain() {
  [ -x "$GBRAIN_BIN" ] || die "gbrain not found or not executable: $GBRAIN_BIN"
}

require_brain_repo() {
  [ -d "$BRAIN_REPO/.git" ] || die "brain repo not found or not a git repo: $BRAIN_REPO"
}

require_clean_brain_repo() {
  local status
  status="$(git -C "$BRAIN_REPO" status --porcelain)"
  if [ -n "$status" ]; then
    printf '%s\n' "$status" >&2
    die "brain repo has uncommitted changes; commit intentionally before continuing"
  fi
}

kill_process_tree() {
  local root="$1"
  local signal="${2:-TERM}"
  local child

  while IFS= read -r child; do
    [ -n "$child" ] && kill_process_tree "$child" "$signal"
  done < <(pgrep -P "$root" 2>/dev/null || true)

  kill "-$signal" "$root" 2>/dev/null || true
}

run_timeout() {
  local seconds="$1"
  shift

  "$@" &
  local pid=$!

  (
    sleep "$seconds"
    if kill -0 "$pid" 2>/dev/null; then
      printf 'error: command timed out after %ss: %s\n' "$seconds" "$*" >&2
      kill_process_tree "$pid" TERM
      sleep 1
      if kill -0 "$pid" 2>/dev/null; then
        kill_process_tree "$pid" KILL
      fi
    fi
  ) &
  local watcher=$!

  local status=0
  wait "$pid" || status=$?
  kill "$watcher" 2>/dev/null || true
  wait "$watcher" 2>/dev/null || true
  return "$status"
}

secret_scan() {
  require_brain_repo

  local hits
  hits="$(
    rg -n \
      '(sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|gbrain_[A-Za-z0-9_-]{16,}|api[_-]?key\s*[:=]\s*["'\'']?[A-Za-z0-9_-]{16,}|secret\s*[:=]\s*["'\'']?[A-Za-z0-9_-]{16,}|password\s*[:=]\s*["'\'']?[^"'\''[:space:]]{12,}|BEGIN (RSA|OPENSSH|PRIVATE) KEY)' \
      "$BRAIN_REPO" \
      | rg -v 'api_key="\\.\\.\\."|api_key="\\.\\.\\."|process\\.env\\.|example|placeholder' \
      || true
  )"

  if [ -n "$hits" ]; then
    printf '%s\n' "$hits" >&2
    die "possible secret(s) found in $BRAIN_REPO; refusing to continue"
  fi

  printf 'secret-scan: ok\n'
}

status() {
  require_gbrain
  printf '== gbrain ==\n'
  "$GBRAIN_BIN" --version
  printf '\n== identity ==\n'
  run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" call get_brain_identity '{}'
  printf '\n== stats ==\n'
  run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" stats
  printf '\n== sources ==\n'
  run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" sources list
  printf '\n== search mode ==\n'
  run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" search modes
}

search_memory() {
  require_gbrain
  [ "$#" -gt 0 ] || die "missing search query"

  local output
  local status=0
  output="$(run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" search "$*" 2>&1)" || status=$?
  printf '%s\n' "$output"

  if [ "$status" -ne 0 ]; then
    return "$status"
  fi

  if [ "$output" = "No results." ]; then
    printf 'hint: Phase 0 has embeddings disabled; retry with exact Korean terms, source title words, or slug fragments.\n'
  fi
}

get_page() {
  require_gbrain
  [ "$#" -eq 1 ] || die "usage: get <slug>"
  run_timeout "$DEFAULT_TIMEOUT_SECONDS" "$GBRAIN_BIN" get "$1"
}

sync_memory() {
  require_gbrain
  require_brain_repo
  secret_scan >/dev/null
  require_clean_brain_repo

  "$GBRAIN_BIN" sync \
    --source "$BRAIN_SOURCE" \
    --repo "$BRAIN_REPO" \
    --no-embed \
    --no-pull \
    --yes
  "$GBRAIN_BIN" extract all --source db
}

capture_memory() {
  require_brain_repo
  require_clean_brain_repo
  [ "$#" -ge 3 ] || die "usage: capture <type> <slug> <title> < stdin"

  local type="$1"
  local slug="$2"
  shift 2
  local title="$*"
  local directory
  local heading

  case "$type" in
    decision|decisions)
      directory="decisions"
      heading="Decision"
      [[ "$slug" =~ ^[0-9]{6}-[a-z0-9][a-z0-9-]*$ ]] || die "decision slug must look like YYMMDD-kebab-title"
      ;;
    project|projects)
      directory="projects"
      heading="Project"
      [[ "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "project slug must be kebab-case"
      ;;
    idea|ideas)
      directory="ideas"
      heading="Idea"
      [[ "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "idea slug must be kebab-case"
      ;;
    pattern|patterns)
      directory="patterns"
      heading="Pattern"
      [[ "$slug" =~ ^[a-z0-9][a-z0-9-]*$ ]] || die "pattern slug must be kebab-case"
      ;;
    session|sessions)
      directory="sessions"
      heading="Session"
      [[ "$slug" =~ ^[0-9]{6}-[a-z0-9][a-z0-9-]*$ ]] || die "session slug must look like YYMMDD-kebab-title"
      ;;
    *)
      die "unknown memory type: $type"
      ;;
  esac

  local file="$BRAIN_REPO/$directory/$slug.md"
  [ ! -e "$file" ] || die "file already exists: $file"

  local body
  body="$(cat)"
  [ -n "$body" ] || die "stdin body is empty"

  mkdir -p "$BRAIN_REPO/$directory"

  {
    printf '# %s: %s\n\n' "$heading" "$title"
    printf '## Summary\n\n'
    printf '%s\n\n' "$body"
    case "$directory" in
      decisions)
        printf '## Context\n\n'
        printf '## Decision\n\n'
        printf '## Alternatives Considered\n\n'
        printf '## Why Now\n\n'
        printf '## Impact\n\n'
        ;;
      projects)
        printf '## Current Status\n\n'
        printf '## Key Decisions\n\n'
        printf '## Open Questions\n\n'
        printf '## Next Actions\n\n'
        ;;
      ideas)
        printf '## Problem\n\n'
        printf '## Hypothesis\n\n'
        printf '## Evidence\n\n'
        printf '## Next Test\n\n'
        ;;
      patterns)
        printf '## Trigger\n\n'
        printf '## Workflow\n\n'
        printf '## Quality Bar\n\n'
        printf '## Failure Modes\n\n'
        ;;
      sessions)
        printf '## Completed\n\n'
        printf '## Decisions\n\n'
        printf '## Open Questions\n\n'
        printf '## Next Actions\n\n'
        ;;
    esac
    printf '## Related\n\n'
    printf '## Timeline\n\n'
  } > "$file"

  secret_scan >/dev/null
  git -C "$BRAIN_REPO" add "$file"
  git -C "$BRAIN_REPO" commit -m "docs: capture ${directory%?} ${slug#??????-}"
  sync_memory
  printf 'Memory saved:\n- %s/%s\n' "$directory" "$slug"
}

capture_decision() {
  [ "$#" -ge 2 ] || die "usage: capture-decision <slug> <title> < stdin"

  local slug="$1"
  shift
  local title="$*"
  capture_memory decision "$slug" "$title"
}

main() {
  local command="${1:-}"
  case "$command" in
    status)
      shift
      [ "$#" -eq 0 ] || die "status takes no arguments"
      status
      ;;
    search)
      shift
      search_memory "$@"
      ;;
    get)
      shift
      get_page "$@"
      ;;
    sync)
      shift
      [ "$#" -eq 0 ] || die "sync takes no arguments"
      sync_memory
      ;;
    secret-scan)
      shift
      [ "$#" -eq 0 ] || die "secret-scan takes no arguments"
      secret_scan
      ;;
    capture)
      shift
      capture_memory "$@"
      ;;
    capture-decision)
      shift
      capture_decision "$@"
      ;;
    -h|--help|help|'')
      usage
      ;;
    *)
      usage >&2
      die "unknown command: $command"
      ;;
  esac
}

main "$@"
