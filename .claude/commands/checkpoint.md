---
name: checkpoint
description: 이름 있는 체크포인트 생성/검증 — 작업 전후 상태 비교
allowed-tools: ["Bash", "Read", "Write", "Glob", "Grep", "AskUserQuestion"]
---

$ARGUMENTS

작업의 특정 시점을 체크포인트로 저장하고, 이전 체크포인트와 비교합니다.

## 서브커맨드

### create {name}
현재 상태를 체크포인트로 저장:
1. `git rev-parse HEAD` 로 현재 커밋 SHA 기록
2. `git diff --stat` 로 변경 파일 목록
3. 프로젝트 메트릭 수집 (가능한 경우):
   - 테스트 결과: `pytest --tb=no -q 2>/dev/null` 또는 `npx vitest run --reporter=dot 2>/dev/null`
   - 린트: `ruff check --statistics 2>/dev/null`
4. `.claude/checkpoints/{name}.json` 에 저장:
```json
{
  "name": "{name}",
  "timestamp": "ISO-8601",
  "git_sha": "abc123",
  "branch": "master",
  "dirty_files": ["file1.py", "file2.md"],
  "metrics": {
    "tests_passed": 42,
    "tests_failed": 0,
    "lint_errors": 0,
    "lint_warnings": 3
  }
}
```

### verify {name}
이전 체크포인트와 현재 상태를 비교:
1. `.claude/checkpoints/{name}.json` 로드
2. 현재 메트릭 수집
3. before/after 비교 출력:
```
=== Checkpoint: {name} ===
Created: {timestamp}
SHA then: {old} → now: {new}

Metric          Before    After    Delta
Tests passed    42        45       +3 ✅
Tests failed    0         0        =
Lint errors     0         0        =
Lint warnings   3         1        -2 ✅
Files changed   —         8        (since checkpoint)
```

### list
`.claude/checkpoints/` 의 모든 체크포인트 나열 (최신순)

### clear {name}
특정 체크포인트 삭제. `--all` 로 전체 삭제.

---

## EXECUTION DIRECTIVE

1. 인자를 파싱하여 서브커맨드와 이름을 추출합니다:
   - `create {name}` → 체크포인트 생성
   - `verify {name}` → 체크포인트 검증
   - `list` → 목록 출력
   - `clear {name}` 또는 `clear --all` → 삭제

2. **create** 실행:
   ```bash
   # Git 정보 수집
   git rev-parse HEAD
   git rev-parse --abbrev-ref HEAD
   git diff --name-only
   git diff --cached --name-only
   ```
   - 테스트/린트 도구를 자동 감지하여 메트릭 수집 시도
   - 결과를 JSON으로 `.claude/checkpoints/{name}.json` 에 저장
   - 저장 완료 메시지 출력: `✅ Checkpoint '{name}' created at {timestamp}`

3. **verify** 실행:
   - `.claude/checkpoints/{name}.json` 파일이 없으면 에러 메시지 출력
   - 현재 메트릭을 동일한 방법으로 수집
   - before/after 비교표를 출력
   - 각 메트릭의 delta를 계산하여 개선(✅)/악화(❌)/동일(=) 표시

4. **list** 실행:
   ```bash
   ls -t .claude/checkpoints/*.json 2>/dev/null
   ```
   - 각 파일의 name, timestamp, git_sha를 테이블로 출력
   - 체크포인트가 없으면 안내 메시지 출력

5. **clear** 실행:
   - `--all` 이면 AskUserQuestion으로 확인 후 전체 삭제
   - 특정 이름이면 해당 파일만 삭제
   - 삭제 완료 메시지 출력

6. 인자가 없으면 도움말 출력:
   ```
   사용법:
     /checkpoint create {name}   체크포인트 생성
     /checkpoint verify {name}   체크포인트 검증
     /checkpoint list            목록 보기
     /checkpoint clear {name}    삭제 (--all: 전체)
   ```

---

## 사용 예시

```
/checkpoint create before-refactor
# ... 작업 수행 ...
/checkpoint verify before-refactor
/checkpoint list
/checkpoint clear before-refactor
/checkpoint clear --all
```

---

Version: 1.0.0
Last Updated: 2026-03-16
Core: Named checkpoint creation and verification for work state comparison
