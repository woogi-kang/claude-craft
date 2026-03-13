# Claude Craft Directive

이 저장소는 더 이상 `moai` 오케스트레이션을 사용하지 않습니다.

## 현재 구성

- 도메인 에이전트와 스킬은 `.claude/agents/`, `.claude/skills/` 아래에 유지합니다.
- 커스텀 커맨드와 일반 훅은 `.claude/commands/`, `.claude/hooks/` 아래에 유지합니다.
- 상태줄은 `.claude/statusline.py`를 사용합니다.

## 제거된 구성

- `moai` core agents / skills / hooks / rules / output styles
- `.moai/` 설정, 메모리, spec 산출물
- `/moai` 기반 워크플로우 전제

## 작업 원칙

- `moai` 전용 워크플로우를 가정하지 말고 직접 도구 호출이나 남아 있는 도메인 자산을 사용합니다.
- 사용자 응답은 현재 대화 언어를 따릅니다.
- 서로 독립적인 조회 작업은 병렬 실행을 우선합니다.
