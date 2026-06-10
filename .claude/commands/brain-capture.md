---
name: brain-capture
description: 결정, 가정, 실패 접근, 반복 패턴을 brain-craft에 저장하고 GBrain에 동기화
allowed-tools: ["Bash", "Read", "Write", "Grep"]
---

$ARGUMENTS

현재 작업에서 장기 기억으로 남길 내용을 `/Users/woogi/brain-craft`에 저장합니다.

## 저장 대상

- 제품/기술/운영 결정
- 중요한 가정과 근거
- 거절한 대안과 이유
- 실패한 접근과 재시도 금지 사항
- 반복 가능한 업무 패턴
- 프로젝트 재개에 필요한 다음 액션

## 저장 금지

- API key, token, credential, password, private env
- 일회성 로그
- 원본 소스 코드 전체
- 사용자 응답 스타일 같은 agent 운영 선호

## 파일 위치

| 유형 | 경로 |
| --- | --- |
| 결정 | `/Users/woogi/brain-craft/decisions/{YYMMDD}-{slug}.md` |
| 프로젝트 맥락 | `/Users/woogi/brain-craft/projects/{slug}.md` |
| 아이디어 | `/Users/woogi/brain-craft/ideas/{slug}.md` |
| 반복 패턴 | `/Users/woogi/brain-craft/patterns/{slug}.md` |
| 세션 요약 | `/Users/woogi/brain-craft/sessions/{YYMMDD}-{slug}.md` |

## Decision Template

```markdown
# Decision: {title}

## Summary

## Context

## Decision

## Alternatives Considered

## Why Now

## Impact

## Related

## Timeline
```

## 동기화

가능하면 wrapper로 저장합니다.

```bash
scripts/brain-memory.sh capture decision "YYMMDD-kebab-title" "Title" < body.md
scripts/brain-memory.sh capture project "project-slug" "Title" < body.md
scripts/brain-memory.sh capture idea "idea-slug" "Title" < body.md
scripts/brain-memory.sh capture pattern "pattern-slug" "Title" < body.md
scripts/brain-memory.sh capture session "YYMMDD-session-slug" "Title" < body.md
```

wrapper는 secret scan, git commit, GBrain sync, extract 갱신을 한 번에 수행합니다. 실제 secret 값이 발견되거나 `/Users/woogi/brain-craft`에 커밋되지 않은 변경이 있으면 중단합니다.

수동 저장이 필요한 경우에도 먼저 확인합니다.

```bash
scripts/brain-memory.sh secret-scan
scripts/brain-memory.sh sync
```

## 출력

```text
Memory saved:
- decisions/...
Skipped:
- ...
Synced:
- pages: N
```
