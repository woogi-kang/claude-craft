# Claude Craft

AI 에이전트와 스킬을 체계적으로 관리하는 멀티 도메인 워크스페이스.
Claude Code, Gemini CLI, Codex CLI, OpenCode에서 동일한 에이전트/스킬 자산을 공유합니다.

## 프로젝트 구조

```
.claude/agents/    # 도메인 에이전트 정의
.claude/skills/    # 스킬 원본 (Single Source of Truth)
.claude/commands/  # 슬래시 커맨드 (commit, review, today, financial-report)
.claude/hooks/     # 라이프사이클 훅
.agents/skills/    # → .claude/skills/ symlink (Gemini, Codex, OpenCode 공용)
data/              # 비즈니스 데이터 (피부과, 시장조사)
tools/             # 운영 도구 (clinic-consult, x-outreach)
scripts/           # 유틸리티 스크립트
work-social/       # 소셜 미디어 전략/초안
```

## 도메인 에이전트 (8개 카테고리)

| 카테고리 | 영역 |
|----------|------|
| 💻 개발 | FastAPI, Flutter, Next.js, Figma 변환, 크롤러, TDD |
| 🎯 기획 | 디스커버리, 전략, 실행, GTM, 데이터 분석 (75개 스킬) |
| 🎨 디자인 | 프론트엔드 UI/UX 디자인 시스템 |
| 📝 콘텐츠 | PPT, 소셜 미디어, 기술 블로그, 이모티콘 |
| 📣 마케팅 | 마케팅 전략, SEO, X 아웃리치 |
| ⚖️ 법무 | 계약 검토, 법인 운영 |
| 💰 재무 | 결제 자동화, 재무 보고 |
| 🔍 리뷰 | 코드/아키텍처/보안/콘텐츠/디자인 멀티 리뷰 |

## 멀티 환경 지원

이 파일은 symlink로 각 도구에 공유됩니다:
- `CLAUDE.md` — Claude Code
- `GEMINI.md` → `CLAUDE.md` — Gemini CLI
- `AGENTS.md` → `CLAUDE.md` — Codex CLI, OpenCode

스킬 역시 `.agents/skills/` → `.claude/skills/` symlink로 공유됩니다.
수정은 항상 원본(`.claude/`)에서 하고, 다른 환경은 자동 반영됩니다.

## 작업 원칙

- 사용자 응답은 현재 대화 언어를 따릅니다.

## Rules

프로젝트 규칙은 `.claude/rules/`에 모듈형으로 관리됩니다:

```
.claude/rules/
├── common/          # 공통 규칙
│   ├── coding-style.md
│   ├── git-workflow.md
│   ├── agent-orchestration.md
│   ├── testing.md
│   └── file-naming.md
├── python/          # Python 전용
│   └── coding-style.md
└── typescript/      # TypeScript 전용
    └── coding-style.md
```

상세 규칙은 각 파일을 참조하세요.
