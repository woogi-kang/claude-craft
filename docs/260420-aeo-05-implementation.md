# AEO 가이드북 05: 실전 구현 가이드

[< 이전: 토큰 최적화](260420-aeo-04-token-optimization.md) | [목차](260420-aeo-00-index.md)

---

## AGENTS.md 작성 가이드

### AGENTS.md란

코드 저장소에 배치하는 AI 코딩 에이전트의 진입점 파일. README.md가 인간을 위한 것이라면, AGENTS.md는 에이전트를 위한 것이다.

### 핵심 원칙: "발견 불가능한 정보만 작성"

> "살아있는 코드베이스 악취 목록으로 생각하라. 영구적 설정이 아니라."

에이전트는 디렉토리 나열과 README로 대부분의 정보를 발견한다. AGENTS.md에는 **코드에서 읽을 수 없는 것**만 넣는다.

### 포함해야 할 것

```markdown
# AGENTS.md

- `uv` 사용 (pip이 아닌 uv로 패키지 관리)
- 테스트 실행 시 반드시 `--no-cache` 플래그 필요
- auth 모듈은 커스텀 미들웨어 패턴 사용 (표준 Express 미들웨어 아님)
- legacy/ 디렉토리는 절대 삭제 금지 (3개 프로덕션 모듈이 임포트)
- 환경변수는 .env.example 참조 (실제 .env는 gitignore)
- CI에서 lint 실패 시 빌드 차단됨
- DB 마이그레이션은 반드시 down 마이그레이션 포함해야 함

## API 문서
- OpenAPI 스펙: /api/v1/openapi.json
- 인증 가이드: /docs/auth.md

## 개발 환경
- 샌드박스: https://sandbox.example.com
- 테스트 계정: test@example.com / (시크릿 관리자 참조)

## 속도 제한
- API: 분당 100 요청
- 웹훅: 초당 10 이벤트
```

### 포함하지 말아야 할 것

| 제외 항목 | 이유 |
|----------|------|
| 디렉토리 구조 | `ls`로 발견 가능 |
| 기술 스택 설명 | `package.json` / `pyproject.toml`로 발견 가능 |
| 모듈별 설명 | README나 코드에서 읽을 수 있음 |
| 코딩 컨벤션 | `.eslintrc`, `ruff.toml` 등에서 파악 가능 |
| 기본적인 git 워크플로우 | 표준 관행 |

### 성능 연구 결과

| 유형 | 성공률 변화 | 비용 변화 | 판정 |
|------|:----------:|:---------:|:----:|
| AGENTS.md 없음 (기준) | — | — | — |
| 개발자 직접 작성 | +4% | +19% | 권장 |
| LLM 자동 생성 | -2~3% | +20%+ | 비권장 |
| `/init` 명령어 생성 | -2~3% | +20%+ | 비권장 |

> **자동 생성된 AGENTS.md는 에이전트 성능을 저하시킨다.** 코드에서 이미 발견할 수 있는 정보를 복제하므로 노이즈만 증가.

### 유지보수 전략

1. **빈 파일로 시작** — 필요할 때만 추가
2. **6개월마다 감사** — 오래된 정보 제거
3. **계층적 배치 고려** — 루트가 아닌 관련 디렉토리에도 배치 가능
4. **자동화된 검증** — CI에서 AGENTS.md 내용의 정확성 검증

---

## agentic-seo 감사 도구

### 설치 및 기본 사용

```bash
# 로컬 프로젝트 감사
npx agentic-seo

# 특정 디렉토리
npx agentic-seo ./my-docs-site

# 라이브 URL 감사
npx agentic-seo --url https://docs.example.com

# 스캐폴딩 (필요한 파일 자동 생성)
npx agentic-seo init
```

### 감사 항목 (100점 만점)

```
┌────────────────────────────────────────────────┐
│           agentic-seo 점수 체계                  │
├──────────────────────┬─────────┬───────────────┤
│ 카테고리              │ 배점    │ 검사 항목      │
├──────────────────────┼─────────┼───────────────┤
│ 검색 발견성           │ 25점    │               │
│   robots.txt         │  10점   │ AI 차단 여부   │
│   llms.txt           │  10점   │ 인덱스 존재    │
│   AGENTS.md          │   5점   │ 프로젝트 컨텍스트│
├──────────────────────┼─────────┼───────────────┤
│ 콘텐츠 구조           │ 25점    │               │
│   구조 평가           │  15점   │ 제목계층/코드예제│
│   Markdown 가용성     │  10점   │ .md 버전 존재  │
├──────────────────────┼─────────┼───────────────┤
│ 토큰 경제성           │ 25점    │               │
│   토큰 예산           │  15점   │ 페이지당 제한   │
│   메타 태그           │  10점   │ AI 메타데이터   │
├──────────────────────┼─────────┼───────────────┤
│ 기능 신호             │ 15점    │               │
│   skill.md           │  10점   │ 기능 설명서    │
│   에이전트 권한        │   5점   │ 접근 규칙     │
├──────────────────────┼─────────┼───────────────┤
│ UX 브릿지             │ 10점    │               │
│   AI용 복사           │  10점   │ 복사 버튼     │
└──────────────────────┴─────────┴───────────────┘
```

### 등급 기준

| 등급 | 점수 | 의미 |
|:----:|:-----:|------|
| A | 90-100 | 우수한 에이전트 준비 상태 |
| B | 75-89 | 양호 — 몇 가지 개선 필요 |
| C | 60-74 | 기능적이나 상당한 개선 필요 |
| D | 40-59 | 격차가 큼 |
| F | 0-39 | 최적화 미흡 |

### 프로그래밍 API

```javascript
import { audit } from 'agentic-seo';

const report = await audit('./my-site');

console.log(report.grade);       // 'B'
console.log(report.percentage);  // 82
console.log(report.findings);    // 상세 검사 결과
```

### 지원 프레임워크

Next.js, Docusaurus, 11ty, Astro, Hugo, Jekyll, Gatsby, VitePress, MkDocs, Sphinx, Vite

---

## 단계별 구현 로드맵

### Phase 1: 즉시 (10분)

**robots.txt 감사**

```bash
# 현재 robots.txt 확인
curl https://yourdomain.com/robots.txt

# AI 에이전트 관련 규칙 점검:
# 1. 광범위한 Disallow가 AI 에이전트를 차단하지 않는지
# 2. 필요한 학습 크롤러만 선택적 차단
# 3. 검색/코딩 에이전트는 허용
```

### Phase 2: 몇 시간

**llms.txt 작성 및 배포**

1. 핵심 문서 페이지 목록 작성
2. 각 페이지에 한 줄 설명 추가
3. 작업 흐름 기준으로 섹션 구성 (Quick Start → API → Concepts)
4. 토큰 수 측정 및 표기
5. `yourdomain.com/llms.txt`에 배포

### Phase 3: 주말 프로젝트

**토큰 수 측정 및 표시**

```bash
# 전체 문서 사이트 토큰 측정 스크립트
#!/bin/bash
for file in docs/**/*.md; do
  tokens=$(python3 -c "
import tiktoken
enc = tiktoken.encoding_for_model('gpt-4o')
with open('$file') as f:
    print(len(enc.encode(f.read())))
  ")
  echo "$file: ${tokens} tokens"
done
```

### Phase 4: 시작 단계

**상위 3개 API의 skill.md 작성**

가장 많이 사용되는 API 3개를 선정하여 skill.md 작성:
1. 성취 가능한 것 (Capabilities)
2. 필수 입력 (Required Inputs)
3. 제약사항 (Constraints)
4. 문서 링크 (토큰 수 포함)

### Phase 5: 낮은 노력

**"AI용 복사" 버튼 추가**

문서 사이트의 각 페이지에 버튼 추가. 클릭 시 본문만 깨끗한 Markdown으로 클립보드에 복사.

### Phase 6: 지속적

**AI 트래픽 모니터링 설정**

```javascript
// Google Analytics 4에서 AI 트래픽 분리
const AI_REFERRERS = [
  'labs.perplexity.ai',
  'chatgpt.com',
  'platform.openai.com',
  'claude.ai',
  'copilot.microsoft.com',
  'gemini.google.com'
];

// 서버 로그에서 코딩 에이전트 식별
const AGENT_SIGNATURES = [
  'axios/1.8.4',     // Claude Code
  'curl/8.4.0',      // Cline
  'got',             // Cursor
  'colly',           // 자동화 크롤러
];
```

---

## 전체 AEO 감사 체크리스트

### 검색 가능성
- [ ] 루트에 `llms.txt` 존재
- [ ] `robots.txt`가 AI 에이전트를 무의식적으로 차단하지 않음
- [ ] `agent-permissions.json` 정의 (선택적)
- [ ] 코드 저장소에 `AGENTS.md` (발견 불가능한 정보만)

### 콘텐츠 구조
- [ ] 문서가 깨끗한 Markdown으로 사용 가능
- [ ] 각 페이지 첫 200단어가 "이것은 무엇이고 어떻게 시작하는가" 답변
- [ ] 제목 계층 일관성 (H1 → H2 → H3)
- [ ] 코드 예시가 설명 직후 배치
- [ ] 매개변수 참고가 산문이 아닌 표 형식

### 토큰 경제학
- [ ] 페이지당 토큰 수 추적
- [ ] 단일 페이지 <= 30,000 토큰
- [ ] `llms.txt`에 주요 페이지 토큰 수 표시
- [ ] 토큰 수가 메타데이터로 공개

### 기능 신호
- [ ] `skill.md`가 "하는 것" 설명 (호출 방법이 아님)
- [ ] 기능, 필수 입력, 제약, 문서 링크 포함
- [ ] MCP 서버 사용 가능 여부 표시

### 분석
- [ ] AI 추천 출처를 웹 분석에서 분리
- [ ] 서버 로그에서 AI 에이전트 HTTP 서명 모니터링
- [ ] AI 대 인간 트래픽 기준선 설정

### UX 브릿지
- [ ] 문서 페이지에 "AI용 복사" 버튼
- [ ] URL 규칙을 통해 Markdown 접근 가능

---

## llms.txt 구현 도구 모음

### 공식/커뮤니티 도구

| 도구 | 용도 | 기술 |
|------|------|------|
| `llms_txt2ctx` | CLI/Python 파서 | Python |
| VitePress 플러그인 | VitePress 자동 생성 | JavaScript |
| Docusaurus 플러그인 | Docusaurus 통합 | JavaScript |
| Drupal LLM Support | Drupal 10.3+ | PHP |
| `llms-txt-php` | PHP 라이브러리 | PHP |
| VS Code PagePilot | 외부 컨텍스트 로딩 | VS Code Extension |
| nbdev | 모든 페이지 .md 자동 생성 | Python |

### llms.txt 디렉토리

- [llmstxt.site](https://llmstxt.site) — llms.txt 채택 사이트 목록
- [directory.llmstxt.cloud](https://directory.llmstxt.cloud) — 커뮤니티 디렉토리

---

## 워크플로우 체인: AEO + MCP

AEO와 MCP(Model Context Protocol)를 결합하면 더 강력한 에이전트 통합이 가능하다.

```
1. 에이전트가 llms.txt로 문서 발견
2. skill.md로 기능 파악
3. MCP 서버를 통해 실시간 API 호출
4. 결과를 코드에 통합
```

### Context7 예시

Context7 같은 MCP 서버가 llms.txt를 기반으로 문서를 제공:

```
# 에이전트 워크플로우
1. resolve-library-id("stripe") → 라이브러리 식별
2. get-library-docs("stripe", "payment intents") → 관련 문서만 검색
3. 토큰 효율적인 컨텍스트로 코드 생성
```

---

## 자주 묻는 질문

### Q: llms.txt는 정말 효과가 있나?

Google의 John Mueller는 "현재 AI 시스템이 llms.txt를 사용하지 않는다"고 했지만, Cursor와 Claude Code 같은 코딩 에이전트는 활용한다. 비용 대비 효과가 높으므로 도입 권장.

### Q: AGENTS.md vs CLAUDE.md vs .cursorrules?

| 파일 | 대상 | 범위 |
|------|------|------|
| AGENTS.md | 모든 AI 에이전트 | 범용 |
| CLAUDE.md | Claude Code 전용 | Claude 특화 |
| .cursorrules | Cursor 전용 | Cursor 특화 |

프로젝트의 도구 에코시스템에 따라 선택. 여러 도구를 사용한다면 AGENTS.md + 특화 파일 병행.

### Q: SEO가 이미 잘 되어 있으면 AEO는 불필요한가?

아니다. SEO와 AEO는 다른 문제를 해결한다:
- SEO: 검색 결과에 노출 → 인간이 클릭
- AEO: 에이전트 컨텍스트에 로드 → 에이전트가 활용

HTML 구조가 아무리 좋아도 토큰 비효율, Markdown 미제공, llms.txt 부재 등은 에이전트를 막는다.

### Q: 어디서부터 시작해야 하나?

1. `npx agentic-seo` 실행 → 현재 점수 확인
2. robots.txt 감사 (10분)
3. llms.txt 작성 (몇 시간)
4. 토큰 수 측정 (주말)

---

## 참고 자료

- [Addy Osmani — Agentic Engine Optimization](https://addyosmani.com/blog/agentic-engine-optimization/)
- [llms.txt 공식 표준](https://llmstxt.org/)
- [agentic-seo GitHub](https://github.com/addyosmani/agentic-seo)
- [Fern — Prepare APIs for AI Agents](https://buildwithfern.com/post/prepare-apis-documentation-ai-agent-consumption)
- [No Hacks — AI User Agent Landscape 2026](https://nohacks.co/blog/ai-user-agents-landscape-2026)
- [Search Engine Land — AEO](https://searchengineland.com/agentic-engine-optimization-google-ai-director-474358)
- [Chrome DevTools — Efficient Token Usage](https://developer.chrome.com/blog/designing-devtools-efficient-token-usage)
- [SmartScope — AGENTS.md Optimization](https://smartscope.blog/en/generative-ai/claude/agents-md-token-optimization-guide-2026/)

[< 이전: 토큰 최적화](260420-aeo-04-token-optimization.md) | [목차](260420-aeo-00-index.md)
