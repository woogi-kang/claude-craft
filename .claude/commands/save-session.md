---
description: "현재 작업 세션을 구조화하여 저장"
type: utility
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

## Pre-execution Context

!git status --porcelain
!git diff --stat
!git log -5 --oneline

---

# /save-session - Save Current Work Session

현재 작업 세션의 진행 상황을 구조화하여 `.claude/sessions/` 에 저장합니다.

## 절차

### Step 1: 현재 상태 수집

```bash
# 변경된 파일 목록
git status

# 변경 규모
git diff --stat

# 최근 커밋
git log --oneline -5
```

### Step 2: 세션 파일 생성

- 파일명: `.claude/sessions/{YYMMDD}-{HHmm}-{topic}.md`
- topic은 현재 작업 주제를 2-3단어로 요약
- AskUserQuestion으로 topic 확인:
  - Question: "세션 주제를 2-3단어로 입력해주세요 (예: auth-api, ui-refactor)"
  - Header: "Session Topic"

### Step 3: 세션 파일 구조

아래 템플릿으로 세션 파일을 생성합니다:

```markdown
# Session: {topic}

## 날짜
{YYYY-MM-DD HH:mm}

## 목표
현재 세션에서 달성하려던 것

## 완료한 작업
- [ ] 또는 [x] 체크리스트 형태

## 변경된 파일
- file1.py — 변경 설명
- file2.md — 변경 설명

## 미완료/블로커
- 아직 끝나지 않은 작업
- 막힌 부분과 이유

## 다음 단계
1. 다음에 이어서 할 작업
2. 우선순위순으로 정리

## 컨텍스트
이 세션을 이어받을 때 알아야 할 핵심 정보.
기술적 결정, 발견한 이슈, 시도한 접근법과 결과 등.
```

### Step 4: 사용자 확인

- 생성된 세션 파일을 보여주고 수정할 부분 확인
- AskUserQuestion:
  - Question: "세션 파일을 확인해주세요. 수정할 부분이 있나요?"
  - Header: "Session Review"
  - Options:
    - Label: "저장 완료", Description: "이대로 저장합니다"
    - Label: "수정 필요", Description: "수정할 내용을 알려주세요"

---

## EXECUTION DIRECTIVE

1. 현재 상태를 수집합니다:
   ```bash
   git status --porcelain
   git diff --stat
   git log --oneline -5
   ```

2. 대화 컨텍스트를 분석하여 세션 내용을 파악합니다:
   - 이번 세션의 목표
   - 완료한 작업과 미완료 작업
   - 변경된 파일과 각각의 변경 내용
   - 블로커나 이슈
   - 다음 단계

3. AskUserQuestion으로 세션 topic을 확인합니다.

4. `.claude/sessions/{YYMMDD}-{HHmm}-{topic}.md` 파일을 생성합니다.
   - 날짜/시간은 현재 시점 기준
   - 변경된 파일 목록은 git status에서 가져옴
   - 목표, 완료 작업, 미완료, 다음 단계는 대화 컨텍스트에서 추출

5. 생성된 파일 내용을 사용자에게 보여주고 확인을 받습니다.

6. 수정 요청이 있으면 반영 후 최종 저장합니다.

---

## 사용 예시

```
/save-session
```

---

Version: 1.0.0
Last Updated: 2026-03-16
Core: Structured session save for work continuity
