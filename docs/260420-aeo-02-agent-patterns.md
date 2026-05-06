# AEO 가이드북 02: AI 에이전트 유형과 행동 패턴

[< 이전: 개요](260420-aeo-01-overview.md) | [목차](260420-aeo-00-index.md) | [다음: AEO 스택 >](260420-aeo-03-aeo-stack.md)

---

## AI 에이전트의 5가지 분류

"AI 봇"을 하나의 범주로 취급하는 것은 잘못이다. 기능적으로 구분되는 **5가지 범주**가 존재하며, 각각 다른 규칙과 결과를 초래한다.

---

### 1. 학습용 크롤러 (Training Crawlers)

LLM 모델 훈련 데이터 수집 목적. 대규모 콘텐츠를 주기적으로 크롤링한다.

| 봇 | 운영사 | robots.txt 준수 | IP 범위 공개 |
|----|--------|:-:|:-:|
| GPTBot | OpenAI | O | O (`/gptbot.json`) |
| ClaudeBot | Anthropic | O | X |
| Amazonbot | Amazon | O | O |
| Meta-ExternalAgent | Meta | O | O |
| CCBot | Common Crawl | O | O |

**대응 전략:**
- 학습에 콘텐츠 사용을 원치 않으면 `robots.txt`에서 명시적 차단
- `Google-Extended`, `Applebot-Extended`는 학습 옵트아웃 전용 토큰 (실제 크롤러가 아님)

```
# robots.txt — 학습 크롤러 차단 예시
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CCBot
Disallow: /
```

---

### 2. 검색/검색 크롤러 (Search & Retrieval)

AI 검색 서비스(Perplexity, ChatGPT 검색 등)의 실시간 색인 구축 목적.

| 봇 | 운영사 | robots.txt | IP 공개 | 비고 |
|----|--------|:-:|:-:|------|
| OAI-SearchBot | OpenAI | O | O | ChatGPT 검색 |
| Claude-SearchBot | Anthropic | O | X | Claude 검색 |
| PerplexityBot | Perplexity | 공표 O / 실제 X | O | 준수 불일치 보고 |
| Bingbot | Microsoft | O | O | Copilot 검색 |

**대응 전략:**
- 일반적으로 **허용 권장** — AI 검색에 노출되면 트래픽 증가
- PerplexityBot은 실제 준수 여부 모니터링 필요

---

### 3. 사용자 트리거 페처 (User-Triggered Fetchers)

사용자가 "이 URL을 읽어줘"라고 명시적으로 요청할 때 동작하는 에이전트.

| 봇 | 운영사 | robots.txt 준수 | 특이사항 |
|----|--------|:-:|----------|
| ChatGPT-User | OpenAI | O | 표준 준수 |
| Claude-User | Anthropic | O | 표준 준수 |
| Google-Agent | Google | **X** | "사용자 요청이므로 무시" |
| Perplexity-User | Perplexity | 공표 O / 실제 불일치 | 보고 있음 |

**핵심 발견:** Google-Agent는 사용자 요청을 근거로 robots.txt 규칙을 명시적으로 무시한다. 이는 서버 측 접근 제어가 필요함을 의미한다.

---

### 4. 코딩 에이전트 (Coding Agents)

개발자 IDE에서 문서를 직접 가져오는 에이전트. **AEO의 주요 대상**이다.

| 에이전트 | HTTP 런타임 | 프리페치 동작 | User-Agent 서명 |
|---------|-----------|-----------|----------------|
| Claude Code | Node.js/Axios | On-demand GET | `axios/1.8.4` |
| Cline | curl | GET + OpenAPI 스캔 | `curl/8.4.0` |
| Cursor | Node.js/got | HEAD 프로브 → GET | `got (sindresorhus)` |
| Aider | Headless Chromium | On-demand GET | Mozilla/Safari UA |

**코딩 에이전트의 문서 소비 특성:**
- 1~2개의 HTTP 요청으로 멀티페이지 탐색을 압축
- 전체 페이지 수신 후 즉시 다음 행동으로 이동
- 클라이언트측 분석 이벤트(스크롤, 클릭, 체류시간) 모두 0
- JavaScript 렌더링 능력이 제한적 (Aider 제외)

---

### 5. 비선언/위장 트래픽 (Undeclared Traffic)

자신을 식별하지 않거나 다른 봇으로 위장하는 트래픽.

| 봇 | 운영사 | 식별 방법 | 문제점 |
|----|--------|-----------|--------|
| Bytespider | ByteDance | 역방향 DNS | 공식 문서 없음 |
| xAI Grok | xAI | IP 범위 분석 | 브라우저 UA 위장 |
| Copilot Actions | Microsoft | IP 범위 | 표준 Edge UA 사용 |

**대응 전략:**
- 서버 로그에서 비정상 패턴 모니터링
- IP 범위 기반 식별
- Web Bot Auth (IETF 초안) 채택 검토

---

## AI 추천 트래픽 모니터링

### Referrer 패턴

에이전트가 사이트로 보내는 트래픽의 주요 referrer:

```
labs.perplexity.ai/referral
chatgpt.com/(none)
chatgpt.com/organic
platform.openai.com/referral
claude.ai/referral
copilot.microsoft.com/referral
gemini.google.com/referral
```

### HTTP 서명 패턴

서버 로그에서 코딩 에이전트를 식별하는 User-Agent 문자열:

```
axios/1.8.4           → Claude Code
curl/8.4.0            → Cline
got (sindresorhus/got) → Cursor
colly                  → 자동화 크롤러
```

### 분석 설정 권장사항

1. 웹 분석 도구에서 AI referrer를 별도 채널로 분리
2. 서버 로그에서 위 HTTP 서명 패턴 모니터링
3. AI 대 인간 트래픽 비율의 기준선(baseline) 수립
4. 주간 리포트에 AI 트래픽 추세 포함

---

## Web Bot Auth — 신흥 신원 검증 표준

IETF 초안 프로토콜로, 봇이 Ed25519 키 쌍으로 HTTP 요청에 서명하고, `/.well-known/http-message-signatures-directory`에서 공개 키를 공시하는 방식이다.

### 지원 현황 (2026.04)

| 제공사 | 상태 | 비고 |
|--------|------|------|
| Google | 실험 단계 | `agent.bot.goog` identity |
| Cloudflare | 완전 구현 | 프로덕션 사용 가능 |
| Akamai | 지원 | CDN 레벨 검증 |
| Amazon Bedrock | 미리보기 | 제한적 사용 |

---

## 에이전트별 대응 전략 매트릭스

| 에이전트 유형 | 허용/차단 | 주요 대응 |
|-------------|----------|-----------|
| 학습 크롤러 | 정책에 따라 선택 | `robots.txt` + 옵트아웃 토큰 |
| 검색 크롤러 | 일반적으로 허용 | `llms.txt`로 구조화 안내 |
| 사용자 페처 | 허용 (차단 어려움) | 서버 측 접근 제어 |
| 코딩 에이전트 | **적극 지원** | AEO 전체 스택 적용 |
| 위장 트래픽 | 서버 측 차단 | IP/행동 패턴 분석 |

---

## 핵심 시사점

1. **"AI 봇" 일괄 차단은 비생산적** — 유형별 세분화된 정책 필요
2. **코딩 에이전트가 AEO의 핵심 대상** — IDE에서 직접 문서를 소비
3. **robots.txt만으로는 불충분** — 일부 에이전트는 준수하지 않음
4. **서버 로그 모니터링 필수** — 에이전트 트래픽은 분석 도구에 안 잡힘
5. **Web Bot Auth 주시** — 신원 검증의 미래 표준

[< 이전: 개요](260420-aeo-01-overview.md) | [목차](260420-aeo-00-index.md) | [다음: AEO 스택 >](260420-aeo-03-aeo-stack.md)
