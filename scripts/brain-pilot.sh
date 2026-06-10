#!/usr/bin/env bash
# brain-pilot.sh - GBrain Phase 3 pilot metrics logger and report generator.

set -euo pipefail

BRAIN_REPO="${BRAIN_REPO:-$HOME/brain-craft}"
PILOT_EVENTS="${PILOT_EVENTS:-$BRAIN_REPO/metrics/gbrain-pilot-events.tsv}"

usage() {
  cat <<'EOF'
Usage: scripts/brain-pilot.sh <command> [args]

Commands:
  init
      Create the pilot metrics file if missing.
  log <event_type> <outcome> <minutes_saved> <citations> <note>
      Append one pilot event.
  report
      Print a Markdown pilot metrics report.

Event types:
  lookup, context, capture, resume, quality, miss

Outcomes:
  useful, neutral, miss, done, blocked

Examples:
  scripts/brain-pilot.sh init
  scripts/brain-pilot.sh log lookup useful 10 decisions/260610-gbrain-phase1-harness-wiring "Recovered Phase 1 decision"
  scripts/brain-pilot.sh report
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

require_brain_repo() {
  [ -d "$BRAIN_REPO/.git" ] || die "brain repo not found or not a git repo: $BRAIN_REPO"
}

sanitize_field() {
  printf '%s' "$1" | tr '\t\n\r' '   ' | sed 's/[[:space:]][[:space:]]*/ /g; s/^ //; s/ $//'
}

init_pilot() {
  require_brain_repo
  mkdir -p "$(dirname "$PILOT_EVENTS")"

  if [ ! -f "$PILOT_EVENTS" ]; then
    printf 'date_iso\tevent_type\toutcome\tminutes_saved\tcitations\tnote\n' > "$PILOT_EVENTS"
  fi

  printf 'pilot metrics: %s\n' "$PILOT_EVENTS"
}

log_event() {
  require_brain_repo
  [ "$#" -ge 5 ] || die "usage: log <event_type> <outcome> <minutes_saved> <citations> <note>"

  local event_type="$1"
  local outcome="$2"
  local minutes_saved="$3"
  local citations="$4"
  shift 4
  local note="$*"

  case "$event_type" in
    lookup|context|capture|resume|quality|miss) ;;
    *) die "unknown event_type: $event_type" ;;
  esac

  case "$outcome" in
    useful|neutral|miss|done|blocked) ;;
    *) die "unknown outcome: $outcome" ;;
  esac

  [[ "$minutes_saved" =~ ^-?[0-9]+$ ]] || die "minutes_saved must be an integer"

  init_pilot >/dev/null
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
    "$(sanitize_field "$event_type")" \
    "$(sanitize_field "$outcome")" \
    "$minutes_saved" \
    "$(sanitize_field "$citations")" \
    "$(sanitize_field "$note")" >> "$PILOT_EVENTS"

  printf 'pilot event logged: %s %s %s\n' "$event_type" "$outcome" "$minutes_saved"
}

report_pilot() {
  require_brain_repo
  [ -f "$PILOT_EVENTS" ] || die "pilot metrics file not found; run init first"

  awk -F '\t' -v metrics_file="$PILOT_EVENTS" '
    NR == 1 { next }
    {
      total++
      type[$2]++
      outcome[$3]++
      minutes += $4
      if ($5 != "" && $5 != "-") cited++
      if ($3 == "useful") useful++
      if ($3 == "miss") misses++
      if ($2 == "capture") captures++
      if ($2 == "resume") resumes++
    }
    END {
      useful_rate = total ? useful * 100 / total : 0
      citation_rate = total ? cited * 100 / total : 0
      printf "# GBrain Phase 3 Pilot Metrics\n\n"
      printf "Metrics file: `%s`\n\n", metrics_file
      printf "## Summary\n\n"
      printf "- Total events: %d\n", total
      printf "- Useful events: %d (%.0f%%)\n", useful, useful_rate
      printf "- Misses: %d\n", misses
      printf "- Capture events: %d\n", captures
      printf "- Resume events: %d\n", resumes
      printf "- Cited events: %d (%.0f%%)\n", cited, citation_rate
      printf "- Estimated minutes saved: %d\n\n", minutes
      printf "## Event Types\n\n"
      for (key in type) {
        printf "- %s: %d\n", key, type[key]
      }
      printf "\n## Outcomes\n\n"
      for (key in outcome) {
        printf "- %s: %d\n", key, outcome[key]
      }
      printf "\n## Go / No-Go Readout\n\n"
      if (total < 10) {
        printf "- Status: collecting data\n"
        printf "- Reason: fewer than 10 events logged.\n"
      } else if (useful_rate >= 50 && misses <= useful && citation_rate >= 50) {
        printf "- Status: go\n"
        printf "- Reason: useful rate and citation rate meet the pilot bar.\n"
      } else {
        printf "- Status: change\n"
        printf "- Reason: usefulness, misses, or citation rate need improvement before expansion.\n"
      }
      printf "\n## Required 30-Day Review Questions\n\n"
      printf "- Did context recovery time drop by at least 50%%?\n"
      printf "- Did the user repeat less project context?\n"
      printf "- Were at least 5 follow-up tasks materially helped by memory?\n"
      printf "- Were search misses caused by no embeddings, bad capture quality, or wrong trigger rules?\n"
      printf "- Keep, change, or drop the current setup?\n"
    }
  ' "$PILOT_EVENTS"
}

main() {
  local command="${1:-}"

  case "$command" in
    init)
      shift
      [ "$#" -eq 0 ] || die "init takes no arguments"
      init_pilot
      ;;
    log)
      shift
      log_event "$@"
      ;;
    report)
      shift
      [ "$#" -eq 0 ] || die "report takes no arguments"
      report_pilot
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      usage >&2
      die "unknown command: $command"
      ;;
  esac
}

main "$@"
