# LLM-Based Doctor Verification

Two-stage LLM verification pipeline for doctor extraction accuracy.

## Pipeline Position

```
DOM extraction -> codex_validator -> llm_verifier -> final result
                  (text-based)      (visual)
```

## Stage 1: Codex Validator (`codex_validator.py`)

Validates extracted `profile_raw` arrays via Codex CLI.

**Input**: Doctor list with name, role, profile_raw arrays
**Output**: Filtered doctors with cleaned profile_raw, branch tags

Responsibilities:
- Filter noise from profile_raw (marketing text, navigation, addresses)
- Validate Korean names (real person vs. brand/fragment)
- Detect credential cross-contamination (multiple people's credentials merged)
- Deduplicate identical credential lists
- Branch filtering for chain hospitals

**Invocation**: `codex exec --full-auto --skip-git-repo-check --ephemeral`

## Stage 2: LLM Verifier (`llm_verifier.py`)

Visual verification of doctor candidates using page screenshot.

**Input**: Doctor candidates + page screenshot path
**Output**: Filtered list (only explicitly rejected names removed)

Responsibilities:
- Confirm extracted names are visible on the page as doctor names
- Reject navigation text, UI labels, marketing copy
- Conservative strategy: unmentioned names are kept

**Invocation**: `codex exec -i <screenshot>`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| CLINIC_CODEX_MODEL | gpt-5.2 | Model for Codex CLI |
| CLINIC_CODEX_REASONING | xhigh | Reasoning effort level |
| CLINIC_CODEX_TIMEOUT | 120 | Timeout in seconds |
| CLINIC_CODEX_KEEP_DEBUG | (off) | Set to "1" to keep debug temp files |
| CLINIC_GEMINI_MODEL | gemini-3-flash-preview | Model for Gemini OCR |

## Prerequisites

Install the Codex CLI:
```bash
npm install -g @openai/codex
```

Set your API key:
```bash
export OPENAI_API_KEY=your-key-here
```

## Fallback Behavior

- Codex CLI not installed: Skips validation, returns empty list (OCR fallback attempted)
- Timeout: Returns empty list, logs warning
- Parse failure: Returns empty list
- LLM verifier failure: Returns all candidates unchanged (conservative)
