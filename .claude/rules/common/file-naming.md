# File Naming Conventions

## 문서
- `docs/` 디렉토리: `YYMMDD-문서명.md` (예: `260316-liff-guide.md`)
- 자동 생성 파일 (카탈로그 등): 날짜 prefix 없음

## 코드
- 스킬 디렉토리: kebab-case (`app-store-screenshots`)
- 스킬 정의: `SKILL.md`
- 에이전트: `{domain}-agent.md` 또는 `{domain}-agent/{domain}-agent-unified.md`
- 커맨드: `command-name.md`

## 프로젝트 구조
- Single Source of Truth: `.claude/`
- 다른 환경 공유: symlink (`.agents/skills/` → `.claude/skills/`)
- 수정은 항상 원본(`.claude/`)에서
