---
name: multi-plan
description: 멀티 LLM 협업 기획 — Claude 오케스트레이션 + 전문가 LLM 분석
allowed-tools: ["Bash", "Read", "Write", "Glob", "Grep", "AskUserQuestion", "Agent"]
---

$ARGUMENTS

여러 LLM을 활용한 협업 기획을 수행합니다. Claude가 오케스트레이터, 다른 LLM이 전문가 역할.

## 원칙
- **기획만, 구현 없음** — 코드 작성 금지
- **모든 결정에 근거 필요** — 트레이드오프 명시
- **사용자 승인 후 다음 단계** — 각 단계 끝에서 확인

## 절차

### Phase 1: 요구사항 정리
사용자의 요청(`$ARGUMENTS`)을 분석하여 명확한 목표와 범위 정의:
- 무엇을 만들/변경할 것인지
- 제약 조건 (기술 스택, 시간, 호환성)
- 성공 기준

### Phase 2: 컨텍스트 수집
관련 코드/문서를 읽어 현재 상태 파악:
- 프로젝트 구조 탐색
- 기존 패턴/컨벤션 확인
- 의존성 확인

### Phase 3: 전문가 분석 (병렬)
Gemini CLI와 Codex CLI를 활용하여 독립적 분석 수행:

```bash
# Backend/시스템 분석 (Codex)
echo "{분석 프롬프트}" | codex -q --model codex-mini 2>/dev/null || echo "Codex unavailable"

# Frontend/UX 분석 (Gemini)
echo "{분석 프롬프트}" | gemini -p 2>/dev/null || echo "Gemini unavailable"
```

사용 불가한 LLM은 건너뛰고 Claude가 해당 역할도 수행.

### Phase 4: 종합 및 계획 수립
전문가 분석 결과를 종합하여 구조화된 계획 작성:

```markdown
# Plan: {제목}

## 목표
{한 문장}

## 아키텍처 결정
| 결정 | 선택 | 근거 | 대안 |
|------|------|------|------|
| ... | ... | ... | ... |

## 작업 분해
1. [ ] {작업 1} — {예상 범위}
2. [ ] {작업 2} — {예상 범위}
...

## 리스크
- {리스크 1}: {완화 방안}

## 의존성
{작업간 의존성 그래프}

## 전문가 의견
- **Codex**: {요약}
- **Gemini**: {요약}
- **합의**: {공통점}
- **이견**: {차이점과 Claude의 판단}
```

### Phase 5: 저장
`.claude/plans/{YYMMDD}-{topic}.md` 에 저장.

## 사용 예시
```
/multi-plan JWT 인증 시스템을 OAuth2로 마이그레이션
/multi-plan 실시간 알림 시스템 설계
```
