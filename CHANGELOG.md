# Changelog

이 프로젝트의 모든 주요 변경사항을 기록합니다.
형식: [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)

---

## [1.0.0] - 2026-03-16

초기 안정 릴리스. 멀티 도메인 에이전트/스킬 워크스페이스 구축 완료.

### Added

**에이전트 (8개 카테고리)**
- 💻 개발: FastAPI, Flutter, Next.js, Figma 변환, 크롤러, TDD 에이전트
- 🎯 기획: 디스커버리, 전략, 실행, GTM, 데이터 분석 (75개 기획 스킬 통합)
- 🎨 디자인: UI/UX Pro Max, 디자인 시스템, 브랜드, 배너, 소셜 포토
- 📝 콘텐츠: PPT, 소셜 미디어, 기술 블로그, 이모티콘, NotebookLM
- 📣 마케팅: 마케팅 전략, SEO, X 아웃리치
- ⚖️ 법무: 계약 검토, 법인 운영
- 💰 재무: 결제 자동화, 재무 보고
- 🔍 리뷰: 코드/아키텍처/보안/콘텐츠/디자인 멀티-LLM 앙상블 리뷰

**스킬 (313+)**
- 카테고리별 에이전트 전용 스킬 (FastAPI 37개, Flutter, Next.js 등)
- 기획 스킬 84개 (pm-skills 통합)
- 독립 스킬 16개 (design, brand, social-content, ui-ux-pro-max 등)

**슬래시 커맨드 (4개)**
- `/commit`: 스마트 멀티 커밋 (논리적 그루핑, 브랜치 보호)
- `/review`: 멀티-LLM 리뷰 (Claude + Gemini + Codex 합의 도출)
- `/today`: 데일리 브리핑 (Dev/Biz/Content 카테고리)
- `/financial-report`: 월간 재무 보고 자동화

**프로덕션 도구 (3개)**
- `clinic-consult`: 외국인 환자 피부과 예약 봇 (카카오톡/LINE, LLM 폴백 체인)
- `x-outreach`: X 자동 아웃리치 파이프라인 (5 페르소나, Playwright)
- `_shared`: 아웃리치 공유 라이브러리 (LLM, 브라우저, DB, 데몬)

**멀티 환경 지원**
- Claude Code, Gemini CLI, Codex CLI, OpenCode 공용 설정
- `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` symlink 체계
- `.agents/skills/` → `.claude/skills/` symlink으로 스킬 공유

**인프라**
- 라이프사이클 훅: `post-write-hook.sh`, `sync-docs.sh`
- 스킬 검증: `scripts/validate-skills.sh`
- 카탈로그 생성: `scripts/skill-catalog.py`

### Improved

**문서화**
- 스킬 템플릿 표준화 (`.claude/skills/_template/SKILL.md`)
- 기여 가이드 (`docs/CONTRIBUTING.md`)
- 프로덕션 도구 런북 (`tools/clinic-consult/RUNBOOK.md`, `tools/x-outreach/RUNBOOK.md`)
- YAML 프론트매터 표준: `name`, `description`, `metadata` (category, version, tags, author)

**컨벤션**
- 파일 네이밍: kebab-case 디렉토리, `SKILL.md` 고정, `YYMMDD-` docs prefix
- 에이전트 네이밍: `{domain}-agent.md` 또는 `{domain}/{domain}-unified.md`
- 커맨드 네이밍: `command-name.md`
