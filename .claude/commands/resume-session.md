---
description: "이전 세션을 로드하고 작업을 이어서 진행"
argument-hint: "[keyword]"
type: utility
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
---

# /resume-session - Resume Previous Work Session

이전 세션 파일을 로드하여 작업 컨텍스트를 복원합니다.

## 절차

### Step 1: 세션 파일 탐색

- `.claude/sessions/` 디렉토리에서 세션 파일 나열
- 인자로 키워드가 주어지면 파일명에서 매칭
- 사용자가 특정 세션을 지정하지 않으면 가장 최근 세션 선택

```bash
# 모든 세션 파일 나열 (최신순)
ls -t .claude/sessions/*.md 2>/dev/null

# 키워드 매칭 (인자가 있을 경우)
ls -t .claude/sessions/*{keyword}*.md 2>/dev/null
```

### Step 2: 세션 로드

- 세션 파일 읽기
- 현재 git 상태와 세션 저장 시점 비교

```bash
# 현재 git 상태
git status --porcelain

# 세션 이후 커밋 확인
git log --oneline --since="{session_date}"
```

### Step 3: 브리핑 출력

아래 형식으로 복원된 세션 정보를 출력합니다:

```
## 세션 복원: {topic}
저장 시점: {date}

### 이전 진행 상황
{완료한 작업 요약}

### 미완료 작업
{미완료/블로커 요약}

### 다음 단계
{다음 단계 목록}

### 현재 상태
- 변경 사항: {git status 요약}
- 세션 이후 커밋: {있으면 표시}
```

### Step 4: 작업 재개 확인

- AskUserQuestion:
  - Question: "다음 단계부터 시작할까요?"
  - Header: "Resume Session"
  - Options:
    - Label: "다음 단계 진행", Description: "세션의 다음 단계부터 이어서 작업합니다"
    - Label: "다른 작업", Description: "다른 작업을 먼저 하겠습니다"

---

## EXECUTION DIRECTIVE

1. 인자를 확인합니다:
   - 인자가 없으면: `.claude/sessions/` 에서 가장 최근 파일 선택
   - 인자가 있으면: 파일명에 해당 키워드가 포함된 세션 검색

2. 매칭되는 세션이 여러 개면 목록을 보여주고 AskUserQuestion으로 선택:
   - Question: "어떤 세션을 복원할까요?"
   - 각 세션을 옵션으로 제공 (파일명 + 날짜)

3. 세션이 없으면 안내 메시지 출력:
   - "저장된 세션이 없습니다. /save-session으로 먼저 세션을 저장해주세요."

4. 선택된 세션 파일을 읽고 내용을 파싱합니다.

5. 현재 git 상태를 수집합니다:
   ```bash
   git status --porcelain
   git log --oneline -5
   ```

6. 세션 저장 시점 이후 변경 사항을 확인합니다:
   ```bash
   git log --oneline --since="{session_datetime}"
   ```

7. 브리핑 형식으로 세션 정보를 출력합니다.

8. AskUserQuestion으로 다음 행동을 확인합니다:
   - "다음 단계 진행" → 세션의 다음 단계 항목부터 작업 시작
   - "다른 작업" → 사용자 지시를 기다림

---

## 사용 예시

```
/resume-session              # 가장 최근 세션
/resume-session auth         # 'auth' 키워드가 포함된 세션
```

---

Version: 1.0.0
Last Updated: 2026-03-16
Core: Session restore and work continuity
