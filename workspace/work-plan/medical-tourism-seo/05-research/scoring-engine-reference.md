# MediScope 채점 엔진 레퍼런스

> SEO/GEO/AEO 진단 항목별 채점 기준, 측정 방법론, 의료관광 특화 전략의 기술 레퍼런스.
> PRD 섹션 "부록 A: 진단 항목 전체 체크리스트"의 상세 구현 가이드.

---

## 1. 가중치 체계 (100점 만점)

| 카테고리 | 가중치 | 항목 수 | 근거 |
|----------|--------|---------|------|
| 기술 SEO | **40%** | 11개 | 기본 위생 요소. 없으면 GEO도 무의미 |
| 성능 (Core Web Vitals) | **15%** | 5개 | Google 랭킹 시그널이나 의료관광에서는 콘텐츠/신뢰가 더 중요 |
| GEO/AEO (AI 검색 최적화) | **25%** | 5개 | AI 검색 시대 핵심. "나타날지 말지"를 결정 |
| 다국어/해외 접근성 | **15%** | 3개 | 의료관광의 본질적 요소 |
| 의료관광 특화 | **±5%** | 보너스 | 가산/감산 항목 |

---

## 2. 기술 SEO (40%)

### 2.1 robots.txt (3%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 존재 + Sitemap 디렉티브 포함 + 주요 페이지 크롤링 허용 + 불필요 리소스만 차단 |
| Warn | 50% | 존재하지만: Sitemap 참조 없음 / 과도한 Disallow(5개+) / 다국어 경로 차단 |
| Fail | 0% | 미존재 / `Disallow: /` 전체 차단 / 200이 아닌 상태 반환 |

**측정**: `{domain}/robots.txt` HTTP GET → 파싱
**의료관광 추가**: `/en/`, `/ja/`, `/zh/` 등 다국어 경로 차단 시 Warn 강제

### 2.2 sitemap.xml (3%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 존재 + XML 유효 + URL 50개+ + lastmod 포함 + 다국어 URL 포함 + robots.txt에서 참조 |
| Warn | 50% | 존재하지만: lastmod 누락 / URL 10개 미만 / 다국어 미포함 |
| Fail | 0% | 미존재 / XML 파싱 실패 / 빈 sitemap |

**측정**: robots.txt Sitemap 디렉티브 → XML 파싱 → URL 수/lastmod 존재율

### 2.3 Meta Title (5%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 90%+ 페이지: title 존재 + 30-60자(한국어 15-30자) + 페이지별 고유 + 핵심 키워드 |
| Warn | 50% | 존재율 70-89% / 길이 초과 20%+ / 중복 존재 |
| Fail | 0% | 존재율 70% 미만 / 50%+ 동일 title |

### 2.4 Meta Description (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 90%+ 페이지: 존재 + 70-155자(한국어 35-77자) + 고유 + CTA 포함 |
| Warn | 50% | 존재율 70-89% / 길이 부적절 20%+ / 중복 |
| Fail | 0% | 존재율 70% 미만 / 50%+ 중복 |

### 2.5 Heading 구조 (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | H1 정확히 1개 + H1→H2→H3 계층 준수 + 키워드 자연 포함 |
| Warn | 50% | H1 복수 / 계층 건너뜀(H1→H3) / H 태그 과다(H1 3개+) |
| Fail | 0% | H1 누락 50%+ / Heading 전무 |

### 2.6 이미지 ALT 태그 (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | ALT 존재율 90%+ + 의미 있는 설명 + 의료 이미지에 시술명 포함 |
| Warn | 50% | 존재율 60-89% / 파일명 반복(IMG_001.jpg) 20%+ |
| Fail | 0% | 존재율 60% 미만 / Before/After 사진에 ALT 전무 |

**의료관광 특화**: B/A 사진 ALT에 시술명/부위 포함 필수

### 2.7 내부 링크 / 깨진 링크 (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 깨진 링크 0개 + 고아 페이지 0개 + 평균 내부 링크 3개+/페이지 |
| Warn | 50% | 깨진 링크 1-5개 / 고아 페이지 존재 / 내부 링크 빈약 |
| Fail | 0% | 깨진 링크 6개+ / 주요 페이지(시술, 예약)에서 404 |

### 2.8 HTTPS / SSL (3%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 전체 HTTPS + 유효 SSL + HTTP→HTTPS 301 + HSTS + Mixed Content 없음 |
| Warn | 50% | HTTPS이지만: Mixed Content / HSTS 미설정 / 인증서 만료 30일 이내 |
| Fail | 0% | HTTP / 만료 SSL / 자체 서명 |

### 2.9 Canonical 태그 (2%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 모든 페이지 canonical 존재 + 자기 참조 + 다국어 간 올바른 설정 |
| Warn | 50% | 존재율 70%+ 이지만 일부 잘못된 참조 |
| Fail | 0% | 50%+ 누락 / 모든 페이지가 홈으로 canonical |

### 2.10 URL 구조 (3%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 깨끗한 슬러그 + 3depth 이내 + 소문자 + 의미 있는 경로 + 언어 코드 prefix |
| Warn | 50% | 쿼리 파라미터 일부 / 4depth+ / 대소문자 혼용 |
| Fail | 0% | 전체 쿼리 기반 / 해시뱅 / 5depth+ 다수 |

### 2.11 HTTP 상태 코드 (5%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 4xx/5xx 0개 + 리다이렉트 체인 2회 이내 + 커스텀 404 페이지 |
| Warn | 50% | 4xx 1-3개 / 리다이렉트 체인 3회+ / 5xx 간헐적 |
| Fail | 0% | 4xx 4개+ / 5xx 상시 / 주요 페이지 접근 불가 |

---

## 3. 성능 - Core Web Vitals (15%)

### 3.1 LCP (4%)

| 등급 | 점수 | 기준 |
|------|------|------|
| Pass | 100% | ≤ 2.5초 (Good) |
| Warn | 50% | 2.5~4.0초 (Needs Improvement) |
| Fail | 0% | > 4.0초 (Poor) |

### 3.2 INP (2%)

| 등급 | 점수 | 기준 |
|------|------|------|
| Pass | 100% | ≤ 200ms |
| Warn | 50% | 200~500ms |
| Fail | 0% | > 500ms |

### 3.3 CLS (2%)

| 등급 | 점수 | 기준 |
|------|------|------|
| Pass | 100% | ≤ 0.1 |
| Warn | 50% | 0.1~0.25 |
| Fail | 0% | > 0.25 |

### 3.4 Lighthouse 성능 점수 (3%)

| 등급 | 점수 | 기준 |
|------|------|------|
| Pass | 100% | Score ≥ 90 |
| Warn | 50% | 50 ≤ Score < 90 |
| Fail | 0% | Score < 50 |

### 3.5 모바일 반응형 (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | viewport 존재 + 가로 스크롤 없음 + 터치 타겟 48px+ + font-size ≥ 16px |
| Warn | 50% | viewport 있지만 일부 오버플로우 / 터치 타겟 작음 |
| Fail | 0% | viewport 미설정 / 데스크톱 전용 |

**측정**: Google PageSpeed Insights API (모바일 + 데스크톱)

---

## 4. GEO/AEO - AI 검색 최적화 (25%)

> "전통적인 SEO는 당신이 어디에 나타나는지를 결정하지만,
> GEO는 당신이 나타날지 말지를 결정합니다."

### 4.1 구조화 데이터 - Schema.org (7%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | JSON-LD + 3종+ 스키마 타입 + Validator 에러 0 + **의료 스키마 1종+** |
| Warn | 50% | 존재하지만: 1-2종만 / Validator 경고 / 의료 스키마 미사용 / Microdata |
| Fail | 0% | 구조화 데이터 전무 / Validator 에러 |

**의료관광 권장 스키마** (7점 세부 채점):

| 세부 항목 | 배점 |
|-----------|------|
| JSON-LD 형식 사용 | 1점 |
| Organization/LocalBusiness 존재 | 1점 |
| **MedicalClinic 또는 Hospital** | 1점 |
| **Physician** (의료진 정보) | 1점 |
| **MedicalProcedure** (시술 정보) | 1점 |
| FAQPage / BreadcrumbList | 1점 |
| Validator 에러 없음 + Rich Results 적격 | 1점 |

### 4.2 FAQ 콘텐츠 + 구조화 데이터 (3%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | FAQ 섹션 존재 + FAQPage 스키마 + Q&A 5개+ + 다국어 FAQ |
| Warn | 50% | FAQ 존재하지만: 스키마 미적용 / 3개 미만 / 단일 언어 |
| Fail | 0% | FAQ 전무 |

**AEO 최적화 구조** (AI가 답변으로 선택되는 조건):
- 역피라미드: 질문(H2) 바로 다음에 40~60단어 직접 답변
- `<li>`, `<table>` 태그로 기계 판독성 확보
- 의료관광 FAQ 필수 주제: 비용, 시술 과정, 회복 기간, 비자/입국, 통역, 사후 관리

### 4.3 콘텐츠 명확성 + Fact-Density (4%)

> AI는 "검증 가능한 통계와 인용이 있는 출처"를 압도적으로 선호.
> Fact-density가 높은 콘텐츠는 AI 인용률이 30~40% 상승.

**측정 방법 (하이브리드: 규칙 기반 + LLM)**

**규칙 기반 (50%)**:

| 세부 항목 | 배점 | 측정 |
|-----------|------|------|
| 페이지당 평균 단어 수 ≥ 300 | 0.5점 | 텍스트 추출 → 단어 수 |
| 검증 가능한 수치/통계 포함 | 0.5점 | 숫자 패턴 + "%" / "건" / "명" 등 매칭 |
| 리스트/테이블 사용 (스캔 가능성) | 0.5점 | `<li>`, `<table>` 태그 존재 |
| 이미지/비디오 포함 (멀티미디어) | 0.25점 | `<img>`, `<video>`, `<iframe>` 존재 |
| CTA 버튼/링크 존재 | 0.25점 | 예약/문의 링크 패턴 매칭 |

**LLM 기반 (50%)** — 구조화된 루브릭:

```
평가 기준 (각 1-5점, 온도 0, 3회 평균):
1. 정보 완전성: 시술명, 과정, 회복 기간, 비용 범위, 부작용 정보
2. 의료 정확성 신호: 의학적 근거 인용, 전문 용어 적절 사용, 면책 조항
3. 외국 환자 관점: 비자, 교통, 숙소, 통역, 사후 관리 정보
4. 행동 유도 명확성: CTA 명확성 (상담 예약, 문의)
5. 가독성: 문장 명확성, 전문 용어 설명, 스캔 가능 구조
```

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 규칙 기반 1.5/2점+ AND LLM 평균 4.0/5.0+ |
| Warn | 50% | 규칙 1.0-1.4 OR LLM 3.0-3.9 |
| Fail | 0% | 규칙 1.0 미만 OR LLM 3.0 미만 |

**재현성 보장**:
- 온도 0 + 3회 반복 → 분산 ≤ 0.5이면 유효
- 프롬프트 버전 관리 (v1, v2...)
- 10개 기준 사이트로 캘리브레이션 (아래 캘리브레이션 프로세스 참조)
- **LLM 모델 버전 고정** (예: gpt-4o-2024-08-06, gemini-1.5-flash-002)
  - 모델 업데이트 시 반드시 캘리브레이션 재실행 후 배포
  - 리포트에 사용된 LLM 모델 버전 명시

**캘리브레이션 프로세스**:
```
1. 기준 사이트 10개 선정 (진료과/규모/점수 분포 다양하게)
   - A등급 2개, B등급 2개, C등급 3개, D-F등급 3개
2. 전문가(SEO 전문가 또는 개발자) 수동 평가 → ground truth 점수
3. 자동 진단 실행 → ground truth와 비교
4. MAE(평균 절대 오차) ≤ 10점이면 유효
5. 가중치 조정 시 전체 기준 사이트에 대한 회귀 테스트 자동 실행
6. 월 1회 캘리브레이션 결과 기록 → 점수 일관성 추적
```

### 4.4 AI 검색 노출 여부 — Share of Model (6%)

> MediScope의 가장 강력한 차별화 기능.

**측정 프로토콜**:

```
Step 1: 대상 병원 주력 시술 추출 (크롤링 기반, 상위 3개)
Step 2: 시술별 질문 생성 (한국어 2 + 영어 2 + 병원명 직접 1 = 5개)
Step 3: 4개 AI 엔진에 질문 (temperature=0)
Step 4: 응답에서 병원명/URL 매칭 (정확 + 퍼지)
Step 5: 3회 반복 → 2/3+ 일치하면 "언급"으로 확정
Step 6: 언급 맥락 분석 (긍정/중립/부정)
```

**AI 엔진별 측정 방법**:

> **MVP 전략 (리뷰 반영)**: 4개 엔진 동시 측정은 비용/rate limit 이슈.
> MVP에서는 **2개 엔진(ChatGPT + Perplexity)**으로 시작, 안정화 후 확장.

| AI 엔진 | API | 측정 방식 | 인용 특성 | MVP 포함 |
|---------|-----|----------|----------|---------|
| **ChatGPT** | OpenAI API (GPT-4o, **버전 고정**) | 응답 텍스트에서 병원명 매칭 | 간접 인용, 출처 링크 때때로 | **O** |
| **Perplexity** | pplx-api | 응답 + **명시적 출처 링크** 추출 | 가장 추적 용이, 출처 URL 직접 제공 | **O** |
| **Google Gemini** | Gemini API | 응답 + Grounding Sources 분석 | Google Search 기반, AI Overview 대리 지표 | v1.2+ |
| **Google AI Overview** | SerpAPI / Custom Scraper | 검색 결과의 AI Overview 스니펫 분석 | 출처 카드 형태 | v1.2+ |

> **대안 엔진**: Perplexity API 가격/안정성 변동 시 Brave Search API 또는 You.com API로 교체 가능하도록 설계.
> 엔진 수를 2-4개로 유연하게 설정 가능한 플러그인 구조 권장.

**채점 (MVP: 6점 만점, 2개 엔진 기준으로 정규화)**:

| 세부 항목 | 배점 | 판정 |
|-----------|------|------|
| ChatGPT 언급 | 3.0점 | 직접 언급(3.0) / 간접(1.5) / 미언급(0) |
| Perplexity 언급 | 3.0점 | 직접 언급 + 출처 링크(3.0) / 언급만(2.0) / 미언급(0) |

> v1.2 이후 4개 엔진 확장 시 각 1.5점으로 재분배.

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 2개 엔진 모두 직접 언급 |
| Warn | 50% | 1개에서만 언급 / 또는 간접 언급만 |
| Fail | 0% | 어떤 엔진에서도 미언급 |

**신규 병원 대응**: LLM 학습 데이터에 포함되지 않은 신규 병원은 AI 검색 언급이 0점이 될 수 있음.
이 경우 "측정 불가 (학습 데이터 미포함 추정)"로 표시하고, 나머지 항목으로 점수를 **정규화** (6% 가중치를 다른 항목에 재분배).

**비용**: 진단 1회당 ~$0.50-1.00 (MVP 2개 엔진, API 호출 30회)
**시간**: 1-2분 (병렬 처리)

**재현성 대응**:
- 고정 프롬프트 세트 + temperature 0
- **LLM 모델 버전 고정** (모델 업데이트 시 캘리브레이션 재실행)
- 3회 반복 → 2/3 합의
- 측정 시점 + 사용 모델 버전을 리포트에 명시
- "스냅샷 기반 평가이며, AI 모델 업데이트에 따라 변동 가능"임을 면책

### 4.5 E-E-A-T 신호 (5%)

**자동 측정 가능한 프록시 신호 체크리스트** (5점 만점):

| 카테고리 | 신호 | 측정 방법 | 배점 |
|----------|------|-----------|------|
| **Experience** | 시술 후기/사례 페이지 | URL/콘텐츠 패턴 (review, 후기, 사례) | 0.5 |
| **Experience** | Before/After 갤러리 | 이미지 페이지 탐지 | 0.5 |
| **Expertise** | 의료진 소개 (이름, 전공, 약력) | /doctor URL + 면허/학력 콘텐츠 | 1.0 |
| **Expertise** | Physician 스키마 | JSON-LD 파싱 | 0.5 |
| **Authority** | 의료기관 인증 (JCI, 보건복지부) | 인증 키워드/이미지 탐지 | 0.5 |
| **Trust** | 개인정보처리방침 존재 | /privacy URL 탐지 | 0.5 |
| **Trust** | 연락처 정보 (주소, 전화, 이메일) | 구조화 데이터 또는 footer 분석 | 0.5 |
| **Trust** | HTTPS (항목 2.8과 연동) | | 0.5 |

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 4.0점+ |
| Warn | 50% | 2.5-3.9점 |
| Fail | 0% | 2.5점 미만 |

---

## 5. 다국어/해외 접근성 (15%)

### 5.1 다국어 페이지 존재 (6%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 3개+ 언어 + 주요 페이지 모두 번역 + 자연스러운 번역 |
| Warn | 50% | 2개 언어 / 일부만 번역 / 기계번역 흔적 |
| Fail | 0% | 단일 언어 / 언어 전환 없음 |

**의료관광 핵심 언어**: 영어(필수), 일본어, 중국어(간/번체), 베트남어, 러시아어

### 5.2 hreflang 태그 (4%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 모든 다국어 페이지 hreflang + 양방향(reciprocal) + x-default |
| Warn | 50% | 존재하지만 양방향 미완성 / x-default 누락 |
| Fail | 0% | 전무 / 전부 잘못된 설정 |

### 5.3 해외 채널/결제 연동 (5%)

| 등급 | 점수 | 조건 |
|------|------|------|
| Pass | 100% | 해외 메신저 2개+(LINE/WhatsApp/WeChat) + 해외 결제 안내 + 다국어 예약 폼 |
| Warn | 50% | 메신저 1개 / 결제 안내 불명확 / 예약 폼 한국어만 |
| Fail | 0% | 해외 소통 채널 전무 / 한국 전화번호만 |

---

## 6. 의료관광 특화 보너스 (±5%)

### 6.1 가산 항목 (최대 +5점)

| 항목 | 가산 | 조건 | 측정 |
|------|------|------|------|
| 의료 스키마 심화 | +1.5 | MedicalClinic + MedicalProcedure + Physician 3종 모두 | JSON-LD |
| 의료관광 인증 마크 | +1.0 | JCI / 보건복지부 외국인환자유치기관 인증 표시 | 텍스트/이미지 패턴 |
| B/A 사진 SEO 최적화 | +0.5 | 시술명 ALT + ImageObject 구조화 데이터 | img alt + JSON-LD |
| 다국어 시술 상세 | +1.0 | 주력 시술 3개+가 3개 언어+로 제공 | 크롤링 패턴 |
| 해외 환자 전용 페이지 | +1.0 | International Patient 랜딩 + 공항 픽업/숙소/통역 안내 | URL/콘텐츠 패턴 |

### 6.2 감산 항목 (최대 -5점)

| 항목 | 감산 | 조건 | 측정 |
|------|------|------|------|
| 의료법 위반 우려 표현 | -2.0 | "최고", "100% 성공률", "부작용 없음" | LLM 텍스트 분석 |
| 시술 가격 미표시 | -1.0 | 주력 시술 가격 범위 완전 비공개 | 가격 키워드 탐지 |
| 의료진 정보 불투명 | -1.0 | 의료진 소개 없음 / 이름/면허 미표시 | /doctor 분석 |
| 후기 조작 의심 | -1.0 | 모든 후기 5점/동일 패턴/날짜 집중 | LLM 패턴 분석 |

---

## 7. 등급 체계

| 등급 | 점수 | 의미 | 리포트 색상 |
|------|------|------|-----------|
| **A+** | 95-100 | 업계 최상위. AI 검색 시대에 완벽히 준비됨 | 🟢 #22C55E |
| **A** | 85-94 | 우수. 소수 항목만 개선 필요 | 🟢 #22C55E |
| **B** | 70-84 | 양호. 주요 개선 포인트 존재 | 🔵 #3B82F6 |
| **C** | 55-69 | 보통. 기본 SEO 미비 다수 | 🟡 #EAB308 |
| **D** | 40-54 | 미흡. 즉각적 개선 필요 | 🟠 #F97316 |
| **F** | 0-39 | 심각. 웹사이트 근본적 재설계 권장 | 🔴 #EF4444 |

**점수 공식**:
```
최종 점수 = Σ(항목 점수 × 항목 가중치) + 의료관광 보너스
범위: 0 ~ 105 → 표시는 min(점수, 100)
```

---

## 8. 리포트 범위 (무료 vs 유료)

### 8.1 무료 프리뷰 (게이팅 전)

| 포함 | 비포함 (유료 유도) |
|------|-------------------|
| 종합 점수 + A-F 등급 | 개별 항목 Pass/Warn/Fail 상세 |
| 카테고리별 등급 (점수 미공개) | 구체적 수정 방법 |
| 상위 3개 문제 (제목 + 1줄 설명) | AI 검색 언급 맥락/내용 |
| AI 검색 노출 여부 (Y/N만) | E-E-A-T 세부 분석 |
| Lighthouse 성능 점수 | 의료관광 특화 가산/감산 내역 |

### 8.2 유료 상세 리포트

| 섹션 | 내용 |
|------|------|
| Executive Summary | 종합 점수 + 핵심 발견 3가지 + 예상 개선 효과 |
| 항목별 상세 | 25개 전 항목 Pass/Warn/Fail + 근거 + 스크린샷 |
| AI 검색 상세 | 4개 엔진별 언급 여부 + 맥락 + SoM(Share of Model) |
| 우선순위 액션 플랜 | 긴급(1주) / 중요(1개월) / 개선(3개월) + 난이도 |
| 경쟁사 벤치마크 | 동일 진료과 상위 병원 대비 비교 (Phase B) |
| 기술 부록 | 크롤링 로그, 측정 시점/조건, LLM 원문 응답 |

### 8.3 리포트 금지 내용 (의료법)

| 금지 | 대안 |
|------|------|
| 시술 효과/성공률 평가 | "시술 정보 페이지 존재 여부"만 체크 |
| 병원 간 시술 품질 비교 | SEO 지표 기반 비교만 |
| 의료진 실력/평판 평가 | "의료진 정보 공개 수준"만 체크 |
| 시술 가격 적정성 | "가격 정보 공개 여부"만 체크 |

**리포트 필수 면책**:
> "본 리포트는 웹사이트의 기술적 SEO/GEO 지표를 자동 분석한 것이며,
> 의료 서비스의 품질이나 안전성을 평가한 것이 아닙니다.
> AI 검색 노출 측정은 측정 시점의 스냅샷이며, AI 모델 업데이트에 따라 변동 가능합니다.
> 의료법 위반 여부 탐지는 주의가 필요한 표현을 안내하는 것이며, 법률 자문이 아닙니다."

**벤치마크 표현 원칙 (의료법 준수)**:
- 경쟁 병원 실명/URL 직접 노출 금지
- "XX피부과는 78점" 같은 실명 비교 금지
- 허용: "동일 진료과 상위 25%/중위/하위 25%" 분포 기반 비교
- 허용: "귀원은 동일 진료과 내 상위 65% 위치"

---

## 9. 진단 파이프라인 아키텍처

### 9.1 4-Phase 병렬 파이프라인

```
진단 요청 (URL 입력)
    │
    ├──[Phase 1] Lighthouse (30초) ─── 성능 + 기본 SEO 13개 항목
    │                                  Chromium headless 실행
    │
    ├──[Phase 2] httpx 크롤링 (10초) ── robots.txt, sitemap, 구조화 데이터, 다국어
    │                                  경량 HTTP 요청, Playwright 불필요
    │
    ├──[Phase 3] Playwright (30초) ─── 스크린샷, JS 렌더링 후 콘텐츠 추출
    │                                  Phase 1의 Chromium 종료 후 실행 (메모리)
    │
    └──[Phase 4] LLM API (20초) ───── 콘텐츠 분석, AI 검색 시뮬레이션, E-E-A-T
                                      Phase 2/3 결과를 입력으로 사용
    │
    ▼
점수 합산 → 등급 산출 → 리포트 생성
```

**실행 순서**: Phase 1+2 병렬 → Phase 3 (Chromium 메모리 확보 후) → Phase 4 (크롤링 결과 기반)
**총 소요 시간**: ~60초 (병렬 처리)

### 9.2 Lighthouse 오픈소스 활용

> GitHub: [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse)
> PSI API 대비 장점: 무제한 실행, 커스텀 가능, 우리 Worker에서 직접 실행

**Lighthouse vs PageSpeed Insights API**:

| | PSI API | Lighthouse 직접 실행 |
|---|---------|-------------------|
| 비용 | 무료 (일일 쿼터) | 완전 무료, 무제한 |
| Rate Limit | 분당 ~25회 | **없음** |
| 커스텀 | 불가 | 카테고리/감사 항목 선택 가능 |
| 실행 환경 | Google 서버 | 우리 Worker에서 직접 |
| 출력 | JSON (제한적) | JSON/HTML/CSV 풀 리포트 |

**실행 방법 (FastAPI Worker에서)**:

```python
# Worker에서 CLI subprocess로 실행
import subprocess, json

async def run_lighthouse(url: str) -> dict:
    result = subprocess.run(
        ["npx", "lighthouse", url,
         "--output=json",
         "--chrome-flags=--headless --no-sandbox",
         "--only-categories=performance,seo,accessibility,best-practices",
         "--quiet"],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout)
```

```javascript
// 또는 Node.js 모듈로 직접 실행
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
const result = await lighthouse(url, {
  port: chrome.port,
  onlyCategories: ['performance', 'seo', 'accessibility', 'best-practices'],
});
// result.lhr → 전체 JSON 리포트
await chrome.kill();
```

### 9.3 Lighthouse → MediScope 항목 매핑

Lighthouse가 **25개 중 13개를 직접 커버**:

| MediScope 항목 | Lighthouse audit key | 값 타입 |
|---------------|---------------------|--------|
| LCP (4%) | `largest-contentful-paint` | ms → Pass/Warn/Fail |
| INP (2%) | `total-blocking-time` (프록시) | ms |
| CLS (2%) | `cumulative-layout-shift` | 점수 |
| Lighthouse 점수 (3%) | `categories.performance.score` | 0-1 (×100) |
| 모바일 반응형 (4%) | `viewport` + `tap-targets` + `font-size` | pass/fail |
| HTTPS (3%) | `is-on-https` | boolean |
| Meta Title (5%) | `document-title` | pass/fail |
| Meta Description (4%) | `meta-description` | pass/fail |
| hreflang (4%) | `hreflang` | pass/fail |
| 이미지 ALT (4%) | `image-alt` | pass/fail |
| 깨진 링크 (4%) | `link-text` + `crawlable-anchors` | 부분 커버 |
| Canonical (2%) | `canonical` | pass/fail |
| HTTP 상태 (5%) | `http-status-code` | pass/fail |

**나머지 12개 항목의 측정 도구**:

| 항목 | 측정 도구 | Phase |
|------|----------|-------|
| robots.txt (3%) | httpx GET | 2 |
| sitemap.xml (3%) | httpx GET + XML 파싱 | 2 |
| Heading 구조 (4%) | BeautifulSoup HTML 파싱 | 2 |
| 내부 링크 상세 (4%) | Playwright 크롤링 | 3 |
| URL 구조 (3%) | 크롤링 URL 패턴 분석 | 2 |
| 구조화 데이터 (7%) | JSON-LD 추출 + Schema.org Validator | 2 |
| FAQ + 스키마 (3%) | HTML 패턴 + JSON-LD | 2 |
| 콘텐츠 명확성 (4%) | LLM 분석 (Gemini Flash) | 4 |
| AI 검색 노출 (6%) | 4개 LLM API 시뮬레이션 | 4 |
| E-E-A-T (5%) | 프록시 신호 크롤링 + LLM | 2+4 |
| 다국어 페이지 (6%) | hreflang + URL 패턴 + LLM 번역 품질 | 2+4 |
| 해외 채널 (5%) | 외부 링크 매칭 (line.me, wa.me 등) | 2 |

### 9.4 Chromium 메모리 관리

Lighthouse와 Playwright 모두 Chromium을 사용하므로 동시 실행 시 메모리 충돌 주의:

```
[권장 실행 순서]
1. Lighthouse 실행 (자체 Chrome 인스턴스) → 완료 후 kill
2. Playwright 실행 (별도 Chromium) → 완료 후 close
→ 동시에 뜨지 않으므로 메모리 ~500MB로 충분

[대안: Lighthouse + Playwright 동시 실행]
→ 메모리 ~1.2GB 필요
→ Railway Pro ($25-30/월) 이상
```

### 9.5 진단 1회 리소스

**표준 진단 (25개 항목)**:

| 항목 | 수량 | 비용 | Phase |
|------|------|------|-------|
| Lighthouse 실행 | 1회 (모바일 기준) | 무료 | 1 |
| httpx 크롤링 | 50-200 페이지 | 무료 | 2 |
| Playwright 스크린샷 | 3-5장 (홈/시술/의료진) | 무료 | 3 |
| LLM 콘텐츠 분석 | ~30회 | ~$0.30 | 4 |
| AI 검색 시뮬레이션 (MVP 2엔진) | ~30회 (2엔진 × 5질문 × 3회) | ~$0.50 | 4 |
| **진단 1회 총 비용** | | **~$1-1.5** (MVP) | |
| **소요 시간** | | **~60-120초** (병렬) | |

> v1.2 이후 4개 엔진 확장 시: AI 시뮬레이션 60회, 비용 ~$2-3/건

**경량 벌크 크롤링 (벤치마크 DB용)**:

| 항목 | 수량 | 비용 | 포함 |
|------|------|------|------|
| httpx 크롤링 | 10-30 페이지 | 무료 | O |
| BeautifulSoup 파싱 | 기술 SEO 11개 항목 | 무료 | O |
| Lighthouse | 제외 | - | X |
| Playwright | 제외 | - | X |
| LLM 분석 | 제외 | - | X |
| **벌크 1건 비용** | | **~$0** | |
| **500건 총 비용** | | **~$0 (서버 비용만)** | |
| **500건 소요 시간** | | **~4-8시간** (1건당 30초, 순차) | |

---

## 10. 벤치마크 도구 레퍼런스

| 도구 | 채점 방식 | MediScope 차용 |
|------|----------|---------------|
| **HubSpot AEO Grader** | 100점, 5차원 (감정40/존재20/인지20/점유10/경쟁10) | 다차원 복합 점수 체계 |
| **SEOptimer** | A-F 등급, 6개 카테고리 | 등급 체계, Pass/Warn/Fail |
| **Ahrefs Site Audit** | Health Score 0-100%, Error/Warning/Notice | 이슈 분류 체계 |
| **frase.io** | SEO+GEO 통합, AI Citation 추적 | GEO 통합 진단 컨셉 |
| **Otterly.ai** | 실시간 AI 응답 모니터링 | 멀티 LLM 모니터링 |
| **Peec AI** | 가시성/포지션/감성 3축 | SoM + 감성 분석 |
| **Profound** | 8개+ LLM 동시 모니터링 | 광범위 플랫폼 커버리지 |
| **Bluefish** | AI Brand Vault, 호감도/정서/안전성 | 의료 브랜드 안전성 |

---

## 참고 문헌

- [Enrich Labs - GEO Complete Guide 2026](https://www.enrichlabs.ai/blog/generative-engine-optimization-geo-complete-guide-2026)
- [Conductor - AEO/GEO Benchmarks Report 2026](https://www.conductor.com/academy/aeo-geo-benchmarks-report/)
- [Incremys - 2026 GEO Statistics](https://www.incremys.com/en/resources/blog/geo-statistics)
- [frase.io - GEO Optimization](https://www.frase.io/blog/geo-optimization/)
- [HubSpot AEO Grader](https://www.hubspot.com/aeo-grader)
- [Otterly.ai - AI Search Monitoring](https://otterly.ai/)
- [Peec AI - AI Search Analytics](https://peec.ai/)
- [Profound - LLM Monitoring](https://profound.so/)
- NotebookLM Deep Research (2026-03-25)
