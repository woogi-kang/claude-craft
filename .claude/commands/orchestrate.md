---
description: "병렬 워크트리 오케스트레이션 — 여러 Claude 인스턴스를 동시에 실행"
argument-hint: "[workers or --status/--cleanup session]"
type: utility
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
model: opus
---

## Pre-execution Context

!git branch --show-current
!git worktree list
!tmux ls 2>/dev/null || echo "No tmux sessions"

---

# /orchestrate - Parallel Worktree Orchestration

## Core Principle

사용자가 병렬로 처리할 작업들을 설명하면, 독립적인 git worktree와 tmux pane으로
여러 Claude 인스턴스를 동시에 실행합니다.

## Command Flow

```
START: Parse user input
  ↓
IF --status {session}: Show session status
IF --cleanup {session}: Cleanup session
ELSE:
  ↓
Decompose tasks into independent workers
  ↓
Generate plan.json
  ↓
Review plan with user (dry-run)
  ↓
Execute orchestration
```

## Step 1: Parse Input

사용자 입력 형태:
- 자유 텍스트: "백엔드 API, 프론트엔드 UI, 테스트를 병렬로 작업해줘"
- 구조화: "Backend: JWT API, Frontend: 로그인 UI, Tests: E2E"
- 상태 확인: "--status feature-auth"
- 정리: "--cleanup feature-auth"

## Step 2: Status/Cleanup (shortcut)

If `--status` or `--cleanup`:
```bash
# Find the plan file or reconstruct from .orchestration/
python3 scripts/orchestrate-worktrees.py plan.json --status
python3 scripts/orchestrate-worktrees.py plan.json --cleanup
```

## Step 3: Decompose Tasks

각 작업을 독립적인 워커로 분해:
- 파일 수정 범위가 겹치지 않도록 분리
- 각 워커에 명확한 목표 부여
- 워커 이름은 영어 권장 (브랜치명 생성에 사용)

## Step 4: Generate Plan

`.orchestration/` 디렉토리에 plan.json 생성:

```json
{
  "session": "feature-name",
  "base_ref": "main",
  "launcher": "claude --dangerously-skip-permissions -p '{task}' --cwd {worktree}",
  "workers": [
    { "name": "Backend", "task": "구체적인 작업 설명" },
    { "name": "Frontend", "task": "구체적인 작업 설명" }
  ]
}
```

## Step 5: Dry Run & Confirm

```bash
python3 scripts/orchestrate-worktrees.py plan.json
```

AskUserQuestion으로 확인:
- Question: "이 계획으로 실행할까요?"
- Options:
  - "실행" — 워크트리 생성 및 Claude 인스턴스 시작
  - "수정" — plan.json 수정 후 재확인
  - "취소" — 중단

## Step 6: Execute

```bash
python3 scripts/orchestrate-worktrees.py plan.json --execute
```

## Step 7: Post-execution Guide

실행 후 안내:
```markdown
## Orchestration Started

**Session**: {session}
**Workers**: {count}

### Commands
- Attach: `tmux attach -t orch-{session}`
- Status: `python3 scripts/orchestrate-worktrees.py plan.json --status`
- Cleanup: `python3 scripts/orchestrate-worktrees.py plan.json --cleanup`

### Tips
- 각 워커는 독립 브랜치에서 작업합니다
- 완료 후 `--cleanup`으로 정리하세요
- handoff.md에서 각 워커의 작업 결과를 확인하세요
```

---

## EXECUTION DIRECTIVE

1. Parse user input to determine mode (orchestrate / status / cleanup)

2. IF status or cleanup mode:
   - Find or reconstruct plan file
   - Run appropriate command
   - Show results
   - STOP

3. IF orchestrate mode:
   - Analyze user's task descriptions
   - Decompose into independent workers with non-overlapping scopes
   - Create plan.json in `.orchestration/` directory
   - Run dry-run: `python3 scripts/orchestrate-worktrees.py plan.json`
   - Ask user to confirm via AskUserQuestion
   - If confirmed, run: `python3 scripts/orchestrate-worktrees.py plan.json --execute`
   - Show post-execution guide with attach/status/cleanup commands

4. Key considerations:
   - Worker names should be English (for branch/slug generation)
   - Task descriptions can be Korean (UTF-8 safe)
   - Session names should be kebab-case English
   - base_ref defaults to current branch or "main"

---

Version: 1.0.0
Last Updated: 2026-03-16
Core: Parallel worktree orchestration via tmux
