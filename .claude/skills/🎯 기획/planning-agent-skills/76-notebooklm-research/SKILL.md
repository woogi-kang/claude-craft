---
name: notebooklm-research
description: "NotebookLM 딥 리서치 — 시장/경쟁사 소스 수집 및 인덱싱으로 Phase 2 리서치 강화"
---

# NotebookLM Deep Research Setup

## Purpose
Planning-agent Phase 2(Research) 시작 전, NotebookLM을 활용해 시장/경쟁사 관련 소스를 대량 수집하고 인덱싱한다. 후속 스킬(market-research, competitor-analysis)이 수집된 소스를 기반으로 깊이 있는 분석을 수행할 수 있도록 준비한다.

## When to Use
- 사용자가 `--deep` 플래그를 지정한 경우
- 사용자가 "깊이 있는 리서치", "NotebookLM 활용", "딥 리서치" 등을 요청한 경우
- 사용자가 명시적으로 빠른 리서치를 원하면 **스킵** (기존 WebSearch만 사용)

## Prerequisites
- `notebooklm` CLI 설치 및 인증 완료
- 인증 확인: `notebooklm status`

## Instructions

You are a research coordinator who sets up deep research infrastructure using NotebookLM before market and competitive analysis begins.

### Input
- **$ARGUMENTS**: 프로젝트명 또는 서비스 아이디어 설명
- **$MARKET_KEYWORDS**: 시장 관련 검색 키워드 (없으면 아이디어에서 추출)
- **$COMPETITOR_KEYWORDS**: 경쟁사 관련 검색 키워드 (없으면 아이디어에서 추출)
- **$USER_SOURCES**: 사용자 제공 URL/파일 목록 (선택)

### Execution Steps

#### Step 1: 인증 확인
```bash
notebooklm status
```
인증 실패 시 사용자에게 `notebooklm login` 실행을 요청하고 중단한다.

#### Step 2: 노트북 생성
```bash
notebooklm create "Research: {project-name}" --json
```
→ `notebook_id`를 기록한다.

#### Step 3: 키워드 추출
아이디어에서 리서치 키워드를 2~4개 추출한다:

- **시장 키워드**: "{시장/산업} 시장 규모 트렌드 성장률 2024 2025"
- **경쟁사 키워드**: "{서비스 카테고리} competitor analysis alternatives"
- **사용자 제공 키워드**: $MARKET_KEYWORDS, $COMPETITOR_KEYWORDS가 있으면 우선 사용

#### Step 4: 딥 리서치 실행 (비동기)
```bash
# 시장 리서치
notebooklm source add-research "{시장 키워드}" --mode deep --no-wait

# 경쟁사 리서치
notebooklm source add-research "{경쟁사 키워드}" --mode deep --no-wait
```

#### Step 5: 사용자 제공 소스 추가
사용자가 URL, PDF 등을 제공한 경우:
```bash
notebooklm source add "{url_or_file}" --json
```

#### Step 6: 리서치 완료 대기
백그라운드 에이전트로 대기하여 메인 대화를 차단하지 않는다:

```
Agent(
  prompt="Wait for research in notebook {notebook_id} to complete and import sources.
          Use: notebooklm research wait -n {notebook_id} --import-all --timeout 600
          Then: notebooklm source list --notebook {notebook_id} --json
          Report: 임포트된 소스 수, 주요 소스 제목 목록",
  subagent_type="general-purpose",
  run_in_background=true
)
```

대기하는 동안 기존 WebSearch 기반으로 market-research, competitor-analysis를 먼저 실행할 수 있다.

#### Step 7: 리서치 컨텍스트 전달
리서치 완료 후 후속 스킬에 전달할 정보:

```
NOTEBOOKLM_CONTEXT:
  notebook_id: {notebook_id}
  source_count: {수집된 소스 수}
  sources: [{소스 제목 목록}]
  status: ready
```

### Output

`workspace/work-plan/{project-name}/02-research/` 폴더에:

**notebooklm-research-setup.md**

```markdown
# NotebookLM Research Setup

## Notebook
- **ID**: {notebook_id}
- **Title**: Research: {project-name}
- **Created**: {timestamp}

## Research Queries
| Query | Mode | Sources Imported |
|-------|------|-----------------|
| {시장 키워드} | deep | {count} |
| {경쟁사 키워드} | deep | {count} |

## Sources
| # | Title | Type | Status |
|---|-------|------|--------|
| 1 | ... | web | ready |
| 2 | ... | web | ready |
| ... | | | |

## Usage for Subsequent Skills
후속 스킬에서 아래 명령으로 소스 활용:
- `notebooklm ask "질문" --notebook {notebook_id}`
- `notebooklm generate report --notebook {notebook_id}`
```

## Fallback
NotebookLM 인증 실패 또는 리서치 타임아웃 시:
- 사용자에게 알림
- 기존 WebSearch 기반 리서치로 폴백
- Phase 2 진행을 차단하지 않는다
