---
name: goal-prep-pack
description: "Turn a PRD, long-running task, launch plan, or autonomous implementation request into a local execution prep pack: VALIDATION.md, RECOVERY.md, PLAN.md, PROGRESS.md, and a command-ready goal summary. Use this before long/autonomous work, multi-agent implementation, or any task where rollback, success criteria, or progress continuity matter."
license: MIT
metadata:
  category: "Standalone"
  version: "0.1.0"
  tags: "execution-contract, prd, planning, recovery, progress, autonomous-work"
---

# Goal Prep Pack

Use this skill to convert a PRD or broad objective into a durable execution package before implementation starts.

## When to Use

- The task spans multiple files, agents, or sessions.
- The user asks for autonomous/long-running work.
- The work has rollback, data, deployment, finance, privacy, or external-send risk.
- A PRD or planning doc exists and needs to become executable.

For small one-file changes, use the lightweight `execution-contract.md` fields instead of creating files.

## Output Directory

Create a repo-local directory:

```text
.claude/goals/{yyMMdd}-{goal-slug}/
```

Write these files:

```text
VALIDATION.md
RECOVERY.md
PLAN.md
PROGRESS.md
goal-command.md
```

## File Contracts

### VALIDATION.md

- Outcome
- In scope
- Out of scope
- Success criteria as observable checks
- Verification commands or browser/device flows
- Required evidence
- Hard fail conditions

### RECOVERY.md

- Files/systems likely to change
- Backup or rollback path
- Data/prod/secrets boundary
- What to do after partial completion
- What must never be reverted automatically

### PLAN.md

- Phases with dependencies
- Owner/agent/skill route for each phase
- Expected artifacts
- Context packs or source docs needed
- Approval gates

### PROGRESS.md

Prepend updates, newest first:

```markdown
## YYYY-MM-DD HH:mm KST
- State: planned|running|blocked|complete
- Done:
- Evidence:
- Next:
```

### goal-command.md

Keep this short enough to paste into a goal or worker prompt:

- objective
- scope lock
- stop condition
- verification
- approval boundary
- links to the four prep files

## Protected Clauses

Every prep pack must include:

- Stop after three repeated failures on the same blocker.
- Do not deploy, mutate production, send external messages, or expose secrets without explicit approval.
- Keep changes tied to the requested scope.
- Update `PROGRESS.md` after each meaningful phase.
- Prefer focused verification over broad, noisy gates unless the blast radius requires broad gates.
