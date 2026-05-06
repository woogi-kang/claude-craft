# AEO 가이드북 03: AEO 6계층 스택

[< 이전: 에이전트 패턴](260420-aeo-02-agent-patterns.md) | [목차](260420-aeo-00-index.md) | [다음: 토큰 최적화 >](260420-aeo-04-token-optimization.md)

---

## 개요

AEO는 6개 계층으로 구성된 스택이다. 아래에서 위로, 기반부터 사용자 경험까지 쌓아올린다.

```
┌──────────────────────────────────────┐
│  Layer 6: UX 브릿지                   │  "AI용 복사" 버튼
├──────────────────────────────────────┤
│  Layer 5: 토큰 수 표시                │  페이지별 토큰 카운트 공개
├──────────────────────────────────────┤
│  Layer 4: 콘텐츠 형식                 │  Markdown, 구조화, 노이즈 제거
├──────────────────────────────────────┤
│  Layer 3: 기능 신호 (skill.md)        │  "무엇을 할 수 있는가" 선언
├──────────────────────────────────────┤
│  Layer 2: 검색 (llms.txt)            │  AI용 사이트맵
├──────────────────────────────────────┤
│  Layer 1: 접근 제어 (robots.txt)      │  에이전트 출입문
└──────────────────────────────────────┘
```

---

## Layer 1: 접근 제어 — robots.txt

에이전트가 **가장 먼저 확인**하는 파일. 잘못 구성하면 에이전트를 완전히 차단한다.

### 흔한 실수

```
# 이렇게 하면 모든 AI 에이전트 차단!
User-agent: *
Disallow: /docs/
```

### 권장 설정

```
# === 검색/코딩 에이전트: 허용 ===
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-User
Allow: /

# === 학습 크롤러: 선택적 차단 ===
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CCBot
Disallow: /

# === 학습 옵트아웃 토큰 ===
User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

# === 일반 크롤러 ===
User-agent: *
Allow: /
Sitemap: https://example.com/sitemap.xml
```

### agent-permissions.json (신흥 표준)

`robots.txt`를 보완하는 새로운 파일. 자동화된 상호작용의 세부 규칙을 선언한다.

```json
{
  "version": "1.0",
  "permissions": {
    "automated_interaction": true,
    "rate_limits": {
      "requests_per_minute": 60,
      "requests_per_hour": 1000
    },
    "preferred_endpoints": {
      "documentation": "/docs/api/",
      "openapi_spec": "/api/v1/openapi.json",
      "llms_txt": "/llms.txt"
    },
    "allowed_actions": [
      "read_documentation",
      "test_api_sandbox",
      "download_sdk"
    ],
    "restricted_actions": [
      "create_account",
      "modify_data",
      "bulk_download"
    ]
  }
}
```

---

## Layer 2: 검색 — llms.txt

`yourdomain.com/llms.txt` — AI 에이전트를 위한 구조화된 사이트맵.

### llms.txt 표준 형식

```markdown
# 프로젝트명

> 프로젝트에 대한 한두 줄 요약

프로젝트 상세 설명 (선택)

## Getting Started

- [Quick Start Guide](/docs/quickstart): 5분 내 API 첫 호출 가능 (8K tokens)
- [Authentication](/docs/auth): OAuth 2.0 및 API 키 인증 패턴 (12K tokens)

## API Reference

- [Users API](/docs/api/users): 사용자 CRUD 엔드포인트 (15K tokens)
- [Events API](/docs/api/events): 이벤트 스트리밍 및 웹훅 (8K tokens)
- [Billing API](/docs/api/billing): 구독 및 결제 관리 (10K tokens)

## Concepts

- [Rate Limiting](/docs/concepts/rate-limits): 속도 제한 정책 (3K tokens)
- [Error Handling](/docs/concepts/errors): 에러 코드 및 재시도 전략 (5K tokens)

## SDKs

- [Python SDK](/docs/sdk/python): pip install 및 빠른 시작
- [Node.js SDK](/docs/sdk/node): npm install 및 TypeScript 지원

## Optional

- [Changelog](/changelog): 릴리즈 히스토리
- [Migration Guide v2→v3](/docs/migration): 마이그레이션 가이드
```

### 좋은 llms.txt의 특징

| 원칙 | 설명 |
|------|------|
| **작업 중심 조직** | 제품 계층이 아닌, 개발자 작업 흐름 기준 배열 |
| **페이지 설명 포함** | 각 링크에 "무엇을 포함하는지" 기술 |
| **토큰 수 명시** | 에이전트가 컨텍스트 예산 판단 가능 |
| **자체 크기 제한** | llms.txt 자체가 < 5,000 토큰 |
| **Optional 섹션** | 맥락 부족 시 생략 가능한 보충 정보 분리 |

### llms.txt 변형 파일

| 파일 | 용도 |
|------|------|
| `llms.txt` | 경량 인덱스 (링크 + 설명) |
| `llms-full.txt` | 전체 문서 내용을 하나로 합친 버전 |
| `llms-ctx.txt` | URL 없이 컨텍스트만 포함한 버전 |

### 현실적 주의사항

> 2026년 4월 현재, Google의 John Mueller는 "현재 AI 시스템이 llms.txt를 사용하지 않는다"고 명시적으로 언급했다.

그러나:
- Cursor, Claude Code 등 코딩 에이전트는 llms.txt를 활용
- Context7 등 MCP 서버가 llms.txt 기반으로 문서 제공
- "상징적 제스처이지 운영상 제어가 아니다"라는 평가도 존재
- 비용 대비 효과가 높으므로 도입 권장

---

## Layer 3: 기능 신호 — skill.md

`skill.md`는 "찾는 위치"가 아닌 **"할 수 있는 것"**을 선언하는 파일이다.

### skill.md 구조

```yaml
---
name: auth-service
description: 사용자 인증, OAuth 2.0 흐름, 세션 관리
version: 2.1.0
---

## 성취 가능한 것 (Capabilities)

- OAuth 2.0 인증 (authorization code, client credentials, PKCE)
- JWT 토큰 발급 및 검증
- 사용자 세션 및 새로고침 토큰 로테이션
- SSO 제공자 통합 (SAML, OIDC)

## 필수 입력 (Required Inputs)

- Client ID / Client Secret
- Redirect URI (사전 등록 필요)
- 요청된 범위 (scopes)

## 제약사항 (Constraints)

- 속도 제한: 분당 1,000 토큰 요청
- 토큰 만료: access 1시간, refresh 30일
- 공개 클라이언트에 PKCE 필수
- 최소 TLS 1.2

## 문서 링크

- [인증 가이드](/docs/auth): 전체 흐름 설명 (12K tokens)
- [OAuth 레퍼런스](/docs/api/oauth): 엔드포인트 상세 (8K tokens)
- [에러 코드](/docs/auth/errors): 인증 에러 목록 (3K tokens)
```

### skill.md vs 기존 문서

| 기존 API 문서 | skill.md |
|-------------|----------|
| "POST /oauth/token 엔드포인트" | "OAuth 2.0 토큰 발급 가능" |
| 엔드포인트별 나열 | 기능별 그룹핑 |
| 호출 방법 상세 | 무엇이 가능한지 요약 |
| 500줄 이상 가능 | 50줄 이내 권장 |

---

## Layer 4: 콘텐츠 형식

에이전트가 실제로 소비하는 콘텐츠의 형식 최적화.

### Markdown 제공 방식

```
# 방법 1: URL에 .md 확장자 추가
https://docs.example.com/api/users        → HTML
https://docs.example.com/api/users.md     → Markdown

# 방법 2: 쿼리 매개변수
https://docs.example.com/api/users?format=md

# 방법 3: Accept 헤더
Accept: text/markdown
```

### 구조화 원칙

**1. 결과 먼저 (Answer First)**
```markdown
## 사용자 생성

사용자를 생성하려면 POST /api/users에 name과 email을 보냅니다.

\```bash
curl -X POST https://api.example.com/users \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "Kim", "email": "kim@example.com"}'
\```

### 매개변수

| 이름 | 타입 | 필수 | 설명 |
|------|------|:----:|------|
| name | string | O | 사용자 이름 |
| email | string | O | 이메일 주소 |
| role | string | X | 기본값: "member" |
```

**2. 일관된 제목 계층**
```
H1: 페이지 제목 (하나만)
  H2: 주요 섹션
    H3: 하위 주제
      H4: 세부 사항 (드물게)
```

**3. 네비게이션 노이즈 제거**

Markdown 버전에서 제외해야 할 요소:
- 사이드바 네비게이션
- 이동경로 (breadcrumbs)
- 바닥글 (footer)
- 쿠키 배너
- 프로모션 배너
- "이 페이지가 도움이 되었나요?" 위젯

**4. 첫 500 토큰의 중요성**

첫 500 토큰이 반드시 답변해야 하는 두 가지 질문:
1. **이것은 무엇인가?** (What)
2. **어떻게 시작하는가?** (How to start)

---

## Layer 5: 토큰 수 표시

문서 페이지와 llms.txt 인덱스에 **토큰 수를 공개**하여 에이전트가 사전 판단 가능하게 한다.

### 표시 방법

```markdown
<!-- 문서 페이지 상단 메타 -->
---
title: Users API Reference
tokens: 15,200
last_updated: 2026-04-15
---

<!-- llms.txt 내 표시 -->
- [Users API](/docs/api/users): 사용자 CRUD (15K tokens)
```

### 에이전트의 의사결정

```
8K tokens   → "전체 포함 가능, 로드하자"
25K tokens  → "큰 편이지만 핵심 부분이면 포함"
150K tokens → "관련 섹션만 추출해야 함"
```

→ 토큰 수 공개가 없으면, 에이전트는 **전체를 다운로드한 후** 초과를 발견하고 잘라내거나 폐기한다.

---

## Layer 6: UX 브릿지 — "AI용 복사" 버튼

IDE 내 AI 어시스턴트(Copilot, Cursor)를 사용하는 개발자가 문서 내용을 깨끗한 Markdown으로 복사할 수 있는 버튼.

### 구현 예시

```html
<button onclick="copyForAI()" title="AI 어시스턴트에 붙여넣기용">
  AI용 복사
</button>

<script>
function copyForAI() {
  // 네비게이션, 사이드바 제외한 본문만 Markdown으로 변환
  const content = document.querySelector('.docs-content');
  const markdown = htmlToMarkdown(content);
  navigator.clipboard.writeText(markdown);
}
</script>
```

### 왜 중요한가

- 개발자가 문서를 읽다가 AI에게 "이걸 기반으로 구현해줘"라고 하는 워크플로우 지원
- HTML 복사 시 네비게이션, CSS 클래스 등 노이즈 포함 → 토큰 낭비
- 깨끗한 Markdown → 에이전트가 정확하게 이해

---

## 계층별 우선순위와 난이도

| 계층 | 영향력 | 난이도 | 권장 순서 |
|------|:------:|:------:|:---------:|
| Layer 1: robots.txt | 높음 (차단 방지) | 10분 | 1 |
| Layer 2: llms.txt | 높음 (발견성) | 몇 시간 | 2 |
| Layer 5: 토큰 수 | 높음 (판단 지원) | 주말 | 3 |
| Layer 3: skill.md | 중간 (기능 신호) | 반나절 | 4 |
| Layer 6: AI 복사 | 낮은 노력/높은 신호 | 1시간 | 5 |
| Layer 4: 콘텐츠 | 높음 (지속적) | 지속적 | 6 (지속) |

---

## 관련 프로토콜 및 표준

### MCP (Model Context Protocol)

Anthropic이 도입한 프로토콜로, AI 모델이 외부 서비스/도구와 연결하는 표준화된 방식. AEO의 Layer 3 (skill.md)과 유사한 "기능 선언" 개념을 프로그래밍 레벨에서 구현.

### A2A (Agent-to-Agent Protocol)

에이전트 간 발견 및 통신 표준. 각 에이전트가 `/.well-known/agent-card.json`에 자신의 이름, 기능, 엔드포인트를 공시.

### llms.txt와의 관계

| 표준 | 역할 | 수준 |
|------|------|------|
| robots.txt | 접근 제어 | 서버 |
| llms.txt | 콘텐츠 발견 | 문서 |
| skill.md | 기능 선언 | 서비스 |
| agent-permissions.json | 상호작용 규칙 | 서버 |
| agent-card.json (A2A) | 에이전트 신원 | 에이전트 |
| MCP | 도구 연결 | 런타임 |

[< 이전: 에이전트 패턴](260420-aeo-02-agent-patterns.md) | [목차](260420-aeo-00-index.md) | [다음: 토큰 최적화 >](260420-aeo-04-token-optimization.md)
