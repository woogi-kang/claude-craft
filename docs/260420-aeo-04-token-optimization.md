# AEO 가이드북 04: 토큰 최적화 전략

[< 이전: AEO 스택](260420-aeo-03-aeo-stack.md) | [목차](260420-aeo-00-index.md) | [다음: 실전 구현 >](260420-aeo-05-implementation.md)

---

## 왜 토큰이 핵심 제약인가

AI 에이전트의 컨텍스트 윈도우는 유한하다. 문서가 이 윈도우를 초과하면 에이전트는 **침묵하는 실패**를 일으킨다.

### 실제 사례

Cisco Secure Firewall Management Center API 가이드:
- **193,217 토큰** (718,000자)
- 대부분 에이전트의 전체 컨텍스트 윈도우(100K~200K) 초과

### 에이전트의 반응 (토큰 초과 시)

| 반응 | 결과 |
|------|------|
| 침묵한 자르기 (Silent Truncation) | 문서 끝부분 손실, 에러 없음 |
| 완전 스킵 | 해당 문서를 아예 무시 |
| 청크 분할 시도 | 지연 증가, 오류 표면 확대 |
| 파라메트릭 지식 폴백 | 학습 데이터 기반 추론 → **할루시네이션** |

→ 개발자는 "왜 AI가 잘못된 API 호출을 생성하는지" 원인을 파악하기 극히 어렵다.

---

## 토큰 예산 가이드라인

### 페이지 유형별 목표

| 페이지 유형 | 토큰 목표 | 근거 |
|-----------|:---------:|------|
| 빠른 시작 (Quick Start) | < 15,000 | 에이전트의 첫 진입점, 빠른 파악 |
| 개별 API 참고 (Reference) | < 25,000 | 단일 엔드포인트/기능 상세 |
| 개념 가이드 (Concept) | < 20,000 | 배경 지식, 아키텍처 설명 |
| llms.txt 인덱스 | < 5,000 | 사이트맵 역할, 경량 유지 |
| skill.md | < 2,000 | 기능 요약, 최대한 간결 |

### 주요 LLM 컨텍스트 윈도우 (2026)

| 모델 | 컨텍스트 윈도우 | 실용적 한계 |
|------|:-----------:|:----------:|
| Claude Opus 4 | 200K | ~150K (시스템 프롬프트 등 제외) |
| GPT-4o | 128K | ~100K |
| Gemini 2.5 Pro | 1M | ~800K |
| Claude Sonnet 4 | 200K | ~150K |

> 컨텍스트 윈도우가 크더라도, 문서 + 코드 + 시스템 프롬프트 + 대화 히스토리가 함께 들어가므로 실용적 한계는 훨씬 작다.

---

## HTML vs Markdown: 90% 토큰 절감

### 비교 실험

동일한 API 문서 페이지:

| 형식 | 토큰 수 | 구성 |
|------|:-------:|------|
| HTML (원본) | ~10,000 | 네비게이션, CSS, 스크립트, 구조 마크업 포함 |
| Markdown (변환) | ~1,000 | 순수 콘텐츠만 |
| **절감률** | **~90%** | |

### 토큰을 낭비하는 HTML 요소

```html
<!-- 이 모든 것이 토큰을 소비하지만 에이전트에게 무가치 -->
<nav class="sidebar">...</nav>           <!-- 사이드바 네비게이션 -->
<ol class="breadcrumb">...</ol>          <!-- 이동경로 -->
<div class="cookie-banner">...</div>     <!-- 쿠키 배너 -->
<footer>...</footer>                     <!-- 바닥글 -->
<script>analytics.track(...);</script>   <!-- 분석 스크립트 -->
<style>.docs-nav { ... }</style>         <!-- CSS -->
<div class="feedback-widget">...</div>   <!-- 피드백 위젯 -->
```

### Markdown 제공 방법

**방법 1: URL 확장자**
```
/docs/api/users       → HTML (인간용)
/docs/api/users.md    → Markdown (에이전트용)
```

**방법 2: 빌드 시 자동 생성**
```bash
# VitePress/Docusaurus 등에서 빌드 시 .md 파일 동시 생성
# nbdev: 모든 페이지의 .md 버전 자동 생성 내장
```

**방법 3: 서버 사이드 변환**
```
Accept: text/markdown  →  서버가 Markdown 반환
Accept: text/html      →  서버가 HTML 반환
```

---

## API 문서 최적화 전략

### 1. OpenAPI 스펙 최적화

에이전트가 OpenAPI 스펙을 직접 소비한다. 명확하게 작성해야 할루시네이션을 방지한다.

**나쁜 예:**
```yaml
paths:
  /users:
    post:
      summary: Create user
      # 매개변수 설명 없음, 제약 없음
```

**좋은 예:**
```yaml
paths:
  /users:
    post:
      summary: 새 사용자 생성
      description: |
        이메일 기반으로 새 사용자를 생성합니다.
        이메일은 시스템 내에서 고유해야 합니다.
      parameters:
        - name: name
          in: body
          required: true
          schema:
            type: string
            minLength: 1
            maxLength: 100
          description: 사용자 표시 이름
        - name: email
          in: body
          required: true
          schema:
            type: string
            format: email
          description: 고유 이메일 주소
      responses:
        201:
          description: 사용자 생성 성공
        409:
          description: 이메일 중복
          content:
            application/json:
              schema:
                properties:
                  error:
                    example: "Email already registered"
```

### 2. 에러 메시지 명확성

```
# 에이전트가 복구할 수 없는 에러
400 Bad Request

# 에이전트가 프로그래밍 방식으로 수정 가능한 에러
400 Missing required field: customer_id (string, format: uuid)
```

### 3. 인증 방식 선택

| 방식 | 에이전트 친화도 | 이유 |
|------|:-:|------|
| API 키 | O | 헤더에 추가하면 끝 |
| 서비스 계정 | O | 자동화에 적합 |
| OAuth (인터랙티브) | X | 에이전트는 브라우저 리다이렉트 불가 |
| 세션 쿠키 | X | 상태 유지 어려움 |

### 4. 언어별 필터링

에이전트가 Python 작업 중이면 Python 예제만 제공하면 된다. 모든 언어의 예제를 로드하면 토큰 낭비.

```markdown
<!-- 에이전트 친화적: 언어별 분리 -->
## Python SDK

\```python
import example_sdk
client = example_sdk.Client(api_key="...")
user = client.users.create(name="Kim", email="kim@example.com")
\```

## Node.js SDK (별도 페이지)
...
```

---

## 의미론적 검색 (RAG) 도입

단순 키워드 매칭 대신 **검색 증강 생성(RAG)**을 도입하면 토큰 오버헤드를 극적으로 줄일 수 있다.

### 기존 방식 vs RAG

| 기존 | RAG |
|------|-----|
| 전체 문서 로드 (50K+ 토큰) | 관련 3~5개 구절만 추출 (~5K 토큰) |
| 에이전트가 관련 부분 직접 탐색 | 의미 기반으로 가장 관련 높은 컨텍스트 제공 |
| 토큰 윈도우 초과 위험 | 90% 토큰 절감 |

### 구현 방법

1. **문서를 청크로 분할** (500~1000 토큰 단위)
2. **임베딩 생성** (OpenAI, Cohere 등)
3. **벡터 DB에 저장** (Pinecone, Weaviate, Chroma 등)
4. **에이전트 질의 시 의미 검색** → 상위 3~5개 청크만 반환

---

## 토큰 측정 도구

### CLI 도구

```bash
# tiktoken (OpenAI 토크나이저)
pip install tiktoken
python -c "
import tiktoken
enc = tiktoken.encoding_for_model('gpt-4o')
with open('docs/api-reference.md') as f:
    tokens = enc.encode(f.read())
print(f'Tokens: {len(tokens):,}')
"

# gpt-tokenizer (JavaScript)
npx gpt-tokenizer count ./docs/api-reference.md
```

### agentic-seo 도구

```bash
# 전체 사이트의 토큰 수 감사
npx agentic-seo --url https://docs.example.com
# → 페이지별 토큰 카운트 포함된 보고서 생성
```

---

## 토큰 최적화 체크리스트

- [ ] 모든 문서 페이지의 토큰 수 측정 완료
- [ ] 단일 페이지 <= 30,000 토큰 (예외 시 청킹 전략 필요)
- [ ] 빠른 시작 페이지 < 15,000 토큰
- [ ] HTML 대신 Markdown 버전 제공
- [ ] llms.txt에 주요 페이지 토큰 수 표시
- [ ] 네비게이션/바닥글/사이드바 노이즈 제거 (Markdown 버전)
- [ ] 코드 예시가 불필요하게 길지 않은지 검토
- [ ] 매개변수 참고가 산문이 아닌 표 형식
- [ ] 에러 메시지가 구체적이고 행동 가능
- [ ] 인증 문서가 프로그래밍 방식 접근을 지원

---

## 핵심 원칙

1. **측정하지 않으면 최적화할 수 없다** — 모든 페이지의 토큰 수를 알아야 한다
2. **Markdown은 필수** — HTML 대비 90% 절감
3. **결과 먼저** — 첫 500 토큰이 핵심 정보를 전달해야 한다
4. **에이전트 컨텍스트는 공유 자원** — 문서는 코드, 프롬프트와 공간을 나눠 쓴다
5. **RAG는 장기 해결책** — 대규모 문서를 다루려면 의미 검색 필수

[< 이전: AEO 스택](260420-aeo-03-aeo-stack.md) | [목차](260420-aeo-00-index.md) | [다음: 실전 구현 >](260420-aeo-05-implementation.md)
