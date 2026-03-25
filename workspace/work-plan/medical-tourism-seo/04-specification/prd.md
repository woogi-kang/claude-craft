# PRD: MediScope - 의료관광 병원 홈페이지 AI 진단 플랫폼

> 프로젝트: medical-tourism-seo
> Phase: 04-Specification
> 작성일: 2026-03-25
> 버전: 1.0
> 상태: Draft

---

## 목차

1. [제품 개요](#1-제품-개요)
2. [MVP 범위 정의](#2-mvp-범위-정의)
3. [사용자 페르소나](#3-사용자-페르소나)
4. [사용자 시나리오 및 유저 플로우](#4-사용자-시나리오-및-유저-플로우)
5. [기능 명세](#5-기능-명세)
6. [데이터 모델](#6-데이터-모델)
7. [API 설계](#7-api-설계)
8. [기술 스택](#8-기술-스택)
9. [시스템 아키텍처](#9-시스템-아키텍처)
10. [LINE/WeChat 메시징 Admin 대시보드 스펙](#10-linewe-chat-메시징-admin-대시보드-스펙)
11. [MVP 우선순위 (MoSCoW)](#11-mvp-우선순위-moscow)
12. [12주 MVP 로드맵](#12-12주-mvp-로드맵)
13. [비기능 요구사항](#13-비기능-요구사항)
14. [성공 지표](#14-성공-지표)

---

## 1. 제품 개요

### 1.1 제품명

**MediScope** (가칭)
- 영문: MediScope - AI Hospital Website Diagnostic Platform
- 한글: 메디스코프 - AI 병원 홈페이지 진단 플랫폼

### 1.2 한 줄 설명

> 병원 홈페이지 URL을 입력하면 AI가 SEO/GEO/AEO를 종합 진단하여,
> 해외 환자가 검색으로 찾을 수 있는 상태인지 즉시 리포트를 제공하는 플랫폼.

### 1.3 가치 제안

```
Before: 병원의 뛰어난 의료 실력이 검색에서 보이지 않아
        해외 환자를 에이전시에 수수료(20~40%)를 주며 유치

After:  AI 진단으로 문제를 발견하고, SEO/GEO/AEO 최적화로
        구글/AI 검색에서 직접 노출되어 자체 유입 확보
```

### 1.4 비즈니스 컨텍스트 (Phase 3 요약)

| 항목 | 수치 |
|------|------|
| 타겟 시장 | 외국인 환자 유치 등록 의료기관 3,154개소 |
| SAM | 72억~346억원 |
| 종합 점수 | 8.0/10 (GO) |
| MVP 목표 | 3개월 내 첫 유료 고객 확보 |

### 1.5 성공 조건

1. 월 100회 이상 진단 실행 (Month 2)
2. 진단 -> 상담 전환율 5% 이상 (Month 3)
3. 3개 이상 유료 계약 체결 (Month 4)
4. MRR 150만원 이상 달성 (Month 6)

---

## 2. MVP 범위 정의

### 2.1 제품 단계 (Phase 구분)

```
Phase A: 진단 도구 MVP (Week 1-6)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
핵심 가치: "병원 홈페이지의 문제를 보여주는 것"
- 무료 진단 도구 (URL 입력 -> 리포트)
- 랜딩페이지 + 리드 수집
- 기본 관리자 대시보드

Phase B: 최적화 서비스 도구 (Week 7-10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
핵심 가치: "문제를 해결하는 것"
- 고객별 프로젝트 관리
- 최적화 작업 추적 대시보드
- Before/After 비교 리포트

Phase C: 구독 모니터링 (Week 11-12)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
핵심 가치: "지속적으로 관리하는 것"
- 주간/월간 자동 진단
- 순위 변동 알림
- 경쟁사 벤치마크 트래킹

Phase D: LINE/WeChat 대시보드 (Post-MVP, Month 4+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
핵심 가치: "해외 환자와 소통하는 것"
- LINE Messaging API 통합
- WeChat Official Account 통합
- 통합 메시지 대시보드
```

### 2.2 MVP 경계선

| 포함 (In Scope) | 제외 (Out of Scope) |
|-----------------|---------------------|
| 기술 SEO 진단 (robots.txt, sitemap, meta tags, 구조화 데이터, Core Web Vitals) | 홈페이지 리디자인/리빌드 |
| GEO/AEO 진단 (AI 검색 노출 여부, 구조화 데이터 의료 스키마) | 콘텐츠 작성 (블로그, SNS) |
| 다국어 지원 여부 진단 | 번역 서비스 |
| 경쟁사 벤치마크 (동일 진료과 상위 병원) | 광고 집행 (Google Ads, Meta Ads) |
| PDF 리포트 생성 | 오프라인 컨설팅 |
| 리드 수집 + 자동 이메일 | CRM 통합 (Salesforce, HubSpot) |
| 관리자 대시보드 (진단 이력, 리드 관리) | 환자 예약 시스템 |

---

## 3. 사용자 페르소나

### 3.1 Primary: 병원장/원장 (의사결정자)

```
이름: 김성우 원장 (45세)
직책: 강남 소재 피부과 원장
상황: 외국인 환자가 점점 늘어나는데, 경쟁 병원에 비해
      구글 검색에서 잘 안 나온다는 것을 느끼고 있음.
      네이버 블로그는 잘 되지만 구글/AI 검색은 무관심했음.

니즈:
- "내 병원이 구글에서 몇 등인지 알고 싶다"
- "경쟁 병원은 어떻게 하고 있는지 비교하고 싶다"
- "기술적으로 뭐가 문제인지 쉽게 이해하고 싶다"
- "얼마나 투자하면 효과가 있는지 ROI를 보고 싶다"

행동 패턴:
- 직접 검색보다는 리포트를 받아보는 것을 선호
- 동료 원장의 추천에 강하게 반응
- 비용보다 결과(환자 수 증가)에 관심

결제 의사: 월 50~100만원 구독 또는 500~1,500만원 프로젝트
```

### 3.2 Secondary: 병원 마케팅 담당자

```
이름: 박지현 (32세)
직책: 네트워크 성형외과 마케팅 팀장
상황: 원장님이 "외국인 환자 더 늘려"라고 지시.
      현재 에이전시에 월 200만원 지불 중인데 효과 불투명.
      홈페이지 개선은 웹에이전시가 담당하는데 SEO는 모름.

니즈:
- "현재 홈페이지 상태를 객관적으로 평가받고 싶다"
- "원장님에게 보여줄 수 있는 리포트가 필요하다"
- "에이전시 vs 자체 최적화 중 뭐가 나은지 비교하고 싶다"

행동 패턴:
- 구글링으로 정보 수집
- 무료 도구를 먼저 사용해보고 유료 전환 결정
- 상급자에게 보고용 자료가 필요

결제 의사: 직접 결제 권한 없음, 원장 승인 필요
```

### 3.3 Tertiary: 의료관광 에이전시 (B2B)

```
이름: 이준호 대표 (38세)
직책: 의료관광 에이전시 대표
상황: 파트너 병원 30개를 관리하며 해외 환자를 연결.
      병원 홈페이지가 부실하면 환자 이탈이 높아 고민.

니즈:
- "파트너 병원들의 홈페이지를 일괄 진단하고 싶다"
- "병원에게 개선 필요성을 설득할 근거가 필요하다"

잠재 가치: 에이전시 경유 소개로 다수 병원 확보 가능 (채널 파트너)
```

---

## 4. 사용자 시나리오 및 유저 플로우

### 4.1 Core Flow: 무료 진단 -> 리드 전환

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORE USER FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. LANDING                                                      │
│     ┌────────────────────────────────┐                          │
│     │  "당신의 병원, 외국인 환자가   │                          │
│     │   검색으로 찾을 수 있나요?"    │                          │
│     │                                │                          │
│     │  [병원 홈페이지 URL 입력]      │                          │
│     │  [무료 진단 시작 ->]           │                          │
│     └────────────────────────────────┘                          │
│                     │                                            │
│                     v                                            │
│  2. SCANNING (실시간 진행 표시)                                  │
│     ┌────────────────────────────────┐                          │
│     │  Scanning your hospital...     │                          │
│     │  ████████████░░░░ 75%          │                          │
│     │                                │                          │
│     │  [v] 기술 SEO 분석 완료        │                          │
│     │  [v] 모바일 최적화 확인        │                          │
│     │  [>] GEO/AEO 진단 중...        │                          │
│     │  [ ] 경쟁사 벤치마크           │                          │
│     └────────────────────────────────┘                          │
│                     │                                            │
│                     v                                            │
│  3. PREVIEW (일부 결과 공개)                                    │
│     ┌────────────────────────────────┐                          │
│     │  종합 점수: 38/100  [위험]     │                          │
│     │                                │                          │
│     │  기술 SEO:    ██░░░  32점      │                          │
│     │  GEO/AEO:     █░░░░  18점      │                          │
│     │  모바일:      ███░░  62점      │                          │
│     │  다국어:      ░░░░░   0점      │                          │
│     │  경쟁력:      █░░░░  22점      │                          │
│     │                                │                          │
│     │  상세 리포트를 받아보세요!     │                          │
│     │  [이메일] [병원명] [전화번호]  │                          │
│     │  [무료 리포트 받기 ->]         │                          │
│     └────────────────────────────────┘                          │
│                     │                                            │
│                     v                                            │
│  4. REPORT DELIVERY                                             │
│     - 이메일로 상세 PDF 리포트 발송                             │
│     - 3일 후 자동 팔로업 이메일                                  │
│     - 7일 후 "무료 상담" 제안 이메일                            │
│                     │                                            │
│                     v                                            │
│  5. CONSULTATION (영업 전환)                                    │
│     - 리포트 기반 30분 무료 상담                                │
│     - 경쟁사 대비 현황 브리핑                                   │
│     - 개선 제안서 + 견적서 전달                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Flow B: 관리자 대시보드

```
┌─────────────────────────────────────────────────────────────────┐
│                 ADMIN DASHBOARD FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LOGIN -> DASHBOARD HOME                                        │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  오늘의 요약                                           │      │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                │      │
│  │  │ 진단  │ │ 리드  │ │상담중│ │ 계약  │                │      │
│  │  │  23   │ │  8   │ │  3   │ │  1   │                │      │
│  │  └──────┘ └──────┘ └──────┘ └──────┘                │      │
│  │                                                       │      │
│  │  최근 진단 목록                                       │      │
│  │  ──────────────────────────────────                   │      │
│  │  강남피부과     38점  리드수집완료  2h ago            │      │
│  │  서울성형외과   52점  상담예약      5h ago            │      │
│  │  역삼치과       21점  미전환        1d ago            │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                  │
│  -> LEAD DETAIL                                                 │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  강남피부과 | 38/100점                                 │      │
│  │                                                       │      │
│  │  담당자: 박지현 / 02-xxx-xxxx                         │      │
│  │  이메일: park@gangnam-skin.kr                         │      │
│  │                                                       │      │
│  │  진단 상세:                                           │      │
│  │  - robots.txt 미설정                                  │      │
│  │  - sitemap.xml 없음                                   │      │
│  │  - 구조화 데이터 0개                                  │      │
│  │  - 다국어 페이지 없음 (hreflang 미설정)               │      │
│  │  - Lighthouse 성능 점수: 42                           │      │
│  │                                                       │      │
│  │  [리포트 재발송] [상담 메모 추가] [견적서 생성]       │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Flow C: 유료 고객 모니터링 대시보드

```
┌─────────────────────────────────────────────────────────────────┐
│              CLIENT MONITORING DASHBOARD                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  강남피부과 | 프로젝트 진행 중                                   │
│                                                                  │
│  점수 추이                                                       │
│  100┃                                         ★ 82              │
│     ┃                              ●───●──●──●                  │
│  50 ┃               ●──●──●──●──●                               │
│     ┃    ●──●──●──●                                             │
│   0 ┃ ●                                                         │
│     ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                   │
│     W1  W2  W3  W4  W5  W6  W7  W8  W9 W10 W11 W12             │
│                                                                  │
│  카테고리별 현황                                                 │
│  ┌─────────────┬────────┬────────┬────────┐                    │
│  │ 항목        │ Before │ Now    │ Target │                    │
│  ├─────────────┼────────┼────────┼────────┤                    │
│  │ 기술 SEO    │ 32     │ 78     │ 85     │                    │
│  │ GEO/AEO     │ 18     │ 65     │ 80     │                    │
│  │ 모바일      │ 62     │ 88     │ 90     │                    │
│  │ 다국어      │  0     │ 72     │ 80     │                    │
│  │ 경쟁력      │ 22     │ 71     │ 75     │                    │
│  └─────────────┴────────┴────────┴────────┘                    │
│                                                                  │
│  최근 변경사항                                                   │
│  - 03/20: sitemap.xml 생성 + 제출 완료                          │
│  - 03/18: 일본어 페이지 5개 추가 (hreflang 설정)               │
│  - 03/15: MedicalClinic 스키마 적용                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. 기능 명세

### 5.1 F1: 홈페이지 진단 엔진 (Core)

#### F1.1 기술 SEO 진단

| 진단 항목 | 체크 내용 | 점수 가중치 | 구현 방법 |
|-----------|----------|------------|----------|
| robots.txt | 존재 여부, 주요 봇 허용, 잘못된 차단 규칙 | 5% | HTTP GET + 파싱 |
| sitemap.xml | 존재 여부, URL 수, 최종 수정일, 유효성 | 5% | HTTP GET + XML 파싱 |
| Meta Tags | title, description 존재/길이/중복, og tags | 10% | HTML 파싱 (BeautifulSoup) |
| Heading 구조 | H1 존재/고유성, H2-H6 계층 구조 | 5% | HTML 파싱 |
| 이미지 ALT | ALT 태그 존재 비율, 파일명 의미성 | 5% | HTML 파싱 |
| 내부 링크 | 깨진 링크 비율, 앵커 텍스트 다양성 | 5% | 크롤링 (Playwright) |
| HTTPS | SSL 인증서 유효성, Mixed Content | 3% | HTTP 요청 |
| Canonical | canonical 태그 존재/정확성 | 3% | HTML 파싱 |
| URL 구조 | 깔끔한 URL, 깊이, 파라미터 | 4% | 크롤링 |
| 404/리다이렉트 | 4xx/5xx 에러, 리다이렉트 체인 | 5% | 크롤링 |

#### F1.2 Core Web Vitals / 성능

| 진단 항목 | 체크 내용 | 점수 가중치 | 구현 방법 |
|-----------|----------|------------|----------|
| LCP | Largest Contentful Paint (2.5s 이하 양호) | 5% | PageSpeed Insights API |
| FID/INP | Interaction to Next Paint | 3% | PageSpeed Insights API |
| CLS | Cumulative Layout Shift (0.1 이하 양호) | 3% | PageSpeed Insights API |
| 성능 점수 | Lighthouse Performance Score | 4% | PageSpeed Insights API |
| 모바일 반응형 | Viewport 설정, 터치 영역, 폰트 크기 | 5% | Lighthouse + Playwright |

#### F1.3 GEO/AEO 진단

| 진단 항목 | 체크 내용 | 점수 가중치 | 구현 방법 |
|-----------|----------|------------|----------|
| 구조화 데이터 | Schema.org 존재, MedicalClinic/Physician 타입 | 8% | JSON-LD 파싱 |
| FAQ 콘텐츠 | FAQ 섹션 존재, Q&A 구조화 데이터 | 3% | HTML 파싱 |
| 콘텐츠 명확성 | 주요 질문에 대한 직접적 답변 포함 여부 | 4% | LLM 분석 |
| AI 검색 언급 | ChatGPT/Gemini/Perplexity에서 병원명 검색 시 언급 여부 | 5% | LLM API 호출 |
| E-E-A-T 신호 | 전문성, 경험, 권위, 신뢰 관련 콘텐츠 | 5% | LLM 분석 |

#### F1.4 다국어/해외 환자 대응

| 진단 항목 | 체크 내용 | 점수 가중치 | 구현 방법 |
|-----------|----------|------------|----------|
| 다국어 페이지 | 영어/일본어/중국어 페이지 존재 여부 | 5% | 크롤링 + 언어 감지 |
| hreflang 태그 | 다국어 페이지간 hreflang 설정 | 3% | HTML 파싱 |
| 해외 채널 연동 | LINE, WeChat, WhatsApp 링크/위젯 | 2% | HTML 파싱 |
| 구글 비즈니스 프로필 | Google Business Profile 등록/최적화 | 4% | Google API (향후) |

### 5.2 F2: 리포트 생성

#### F2.1 실시간 프리뷰 리포트 (게이트 전)

- 종합 점수 (0-100)
- 카테고리별 점수 (5개 영역) 바 차트
- 등급 표시: A(80+), B(60-79), C(40-59), D(20-39), F(0-19)
- "상세 리포트를 받으려면 정보를 입력하세요" CTA

#### F2.2 상세 PDF 리포트 (게이트 후)

```
리포트 구조:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Executive Summary (1페이지)
   - 종합 점수 + 등급
   - 핵심 문제 Top 3
   - 예상 개선 효과

2. 카테고리별 상세 진단 (3-5페이지)
   - 각 항목별 Pass/Warn/Fail 상태
   - 스크린샷 포함 (문제 영역 하이라이트)
   - 개선 권고사항 (우선순위별)

3. 경쟁사 벤치마크 (1-2페이지)
   - 동일 진료과 상위 3개 병원과 비교
   - 레이더 차트로 시각화
   - "이 영역에서 뒤처지고 있습니다" 메시지

4. 개선 로드맵 (1페이지)
   - 즉시 개선 가능 (1주)
   - 단기 개선 (1개월)
   - 중기 개선 (3개월)
   - 예상 비용 범위

5. 부록
   - 전체 체크리스트 결과표
   - 기술 용어 설명
```

#### F2.3 리포트 생성 기술

| 요소 | 기술 | 비고 |
|------|------|------|
| PDF 생성 | Playwright (HTML -> PDF) 또는 @react-pdf/renderer | HTML 템플릿 기반 |
| 차트 | Chart.js (서버사이드 렌더링) | 바 차트, 레이더 차트 |
| 스크린샷 | Playwright screenshot API | 전체 페이지 + 특정 영역 |
| 저장 | Supabase Storage | S3 호환 |
| 전송 | Resend (이메일 API) | 트랜잭셔널 이메일 |

### 5.3 F3: 리드 수집 및 자동 이메일

#### F3.1 정보 수집 폼

| 필드 | 필수 | 타입 | 용도 |
|------|------|------|------|
| 이메일 | O | email | 리포트 발송 + 후속 이메일 |
| 병원명 | O | text | CRM + 영업 |
| 담당자명 | O | text | 개인화 소통 |
| 전화번호 | X | tel | 콜 아웃리치 |
| 진료과목 | X | select | 세그먼트 |

#### F3.2 자동 이메일 시퀀스

| 시점 | 이메일 | 내용 |
|------|--------|------|
| 즉시 | 리포트 발송 | PDF 첨부 + 주요 발견사항 요약 |
| +3일 | 팔로업 1 | "리포트 확인하셨나요?" + 핵심 문제 1개 강조 |
| +7일 | 팔로업 2 | "무료 30분 상담 예약하세요" + 캘린더 링크 |
| +14일 | 팔로업 3 | 성공 사례 공유 + "경쟁 병원은 이미 시작했습니다" |
| +30일 | 재진단 알림 | "한 달이 지났습니다. 다시 진단해보세요" |

### 5.4 F4: 관리자 대시보드

#### F4.1 대시보드 홈

| 위젯 | 데이터 | 비고 |
|------|--------|------|
| 진단 수 (오늘/주간/월간) | audit 테이블 COUNT | 트렌드 포함 |
| 리드 수 (신규/누적) | leads 테이블 COUNT | 전환율 포함 |
| 상담/계약 현황 | leads.status COUNT | 퍼널 시각화 |
| 최근 진단 목록 | audits ORDER BY created_at DESC | 클릭 -> 상세 |

#### F4.2 리드 관리

| 기능 | 설명 |
|------|------|
| 리드 목록 | 필터(상태, 진료과, 점수 범위), 정렬, 검색 |
| 리드 상세 | 진단 결과, 연락처, 상담 메모, 이메일 이력 |
| 상태 관리 | New -> Contacted -> Consulting -> Contracted -> Churned |
| 메모 추가 | 상담 내용, 요구사항, 다음 액션 기록 |
| 견적서 생성 | 템플릿 기반 견적서 PDF 생성 (향후) |

#### F4.3 프로젝트 관리 (Phase B)

| 기능 | 설명 |
|------|------|
| 프로젝트 목록 | 진행 중인 최적화 프로젝트 |
| 작업 체크리스트 | 최적화 항목별 완료 상태 |
| Before/After | 최적화 전후 점수 비교 |
| 타임라인 | 작업 히스토리 |

### 5.5 F5: 경쟁사 벤치마크

| 기능 | 설명 | 구현 |
|------|------|------|
| 동일 진료과 자동 매칭 | 진단 시 해당 진료과 상위 병원 3개 자동 선정 | 사전 크롤링 DB |
| 비교 레이더 차트 | 5개 카테고리 비교 시각화 | Chart.js |
| 순위 추정 | 해당 키워드 구글 검색 순위 추정 | Google Search Console API (향후) |
| 벤치마크 DB | 3,154개 등록 기관 사전 크롤링 결과 | 배치 크롤링 |

### 5.6 F6: 벌크 진단 (사전 크롤링)

| 기능 | 설명 | 용도 |
|------|------|------|
| 등록 기관 전수 크롤링 | 3,154개 기관 홈페이지 일괄 진단 | 벤치마크 DB + 콜드 아웃리치 |
| 스케줄링 | 월 1회 자동 재크롤링 | 데이터 최신화 |
| 순위 생성 | 진료과별 SEO 점수 순위 | 콘텐츠 마케팅 (공개 순위표) |
| 아웃리치 타겟 | 점수 하위 30% 병원 리스트 추출 | 영업 리드 |

---

## 6. 데이터 모델

### 6.1 ERD (Entity Relationship Diagram)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   hospitals  │     │    audits    │     │    leads     │
├──────────────┤     ├──────────────┤     ├──────────────┤
│ id (PK)      │<--->│ id (PK)      │     │ id (PK)      │
│ name         │     │ hospital_id  │---->│ audit_id     │
│ url          │     │ url          │     │ email        │
│ specialty    │     │ scores       │     │ name         │
│ region       │     │ details      │     │ hospital_name│
│ phone        │     │ report_url   │     │ phone        │
│ is_registered│     │ status       │     │ specialty    │
│ created_at   │     │ created_at   │     │ status       │
│ updated_at   │     │ updated_at   │     │ notes        │
└──────────────┘     └──────────────┘     │ emails_sent  │
                                          │ created_at   │
┌──────────────┐     ┌──────────────┐     │ updated_at   │
│  projects    │     │  audit_items │     └──────────────┘
├──────────────┤     ├──────────────┤
│ id (PK)      │     │ id (PK)      │     ┌──────────────┐
│ lead_id      │     │ audit_id     │     │ email_logs   │
│ hospital_id  │     │ category     │     ├──────────────┤
│ status       │     │ item_key     │     │ id (PK)      │
│ plan         │     │ status       │     │ lead_id      │
│ start_date   │     │ score        │     │ template     │
│ end_date     │     │ details      │     │ sent_at      │
│ created_at   │     │ suggestion   │     │ opened_at    │
│ updated_at   │     │ created_at   │     │ clicked_at   │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 6.2 주요 테이블 스키마

#### hospitals

```sql
CREATE TABLE hospitals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    specialty TEXT,                    -- dermatology, plastic_surgery, dental, etc.
    region TEXT,                       -- gangnam, seocho, etc.
    phone TEXT,
    is_registered BOOLEAN DEFAULT false,  -- 외국인 환자 유치 등록 기관 여부
    latest_score INTEGER,                 -- 최근 진단 점수 (캐시)
    latest_audit_id UUID,
    metadata JSONB,                       -- 추가 정보 (규모, 의료진 수 등)
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_hospitals_specialty ON hospitals(specialty);
CREATE INDEX idx_hospitals_region ON hospitals(region);
CREATE INDEX idx_hospitals_score ON hospitals(latest_score);
```

#### audits

```sql
CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID REFERENCES hospitals(id),
    url TEXT NOT NULL,
    status TEXT DEFAULT 'pending',        -- pending, scanning, completed, failed

    -- 종합 점수
    total_score INTEGER,                  -- 0-100
    grade TEXT,                           -- A, B, C, D, F

    -- 카테고리별 점수 (JSONB)
    scores JSONB NOT NULL DEFAULT '{}',
    -- {
    --   "technical_seo": 32,
    --   "performance": 45,
    --   "geo_aeo": 18,
    --   "multilingual": 0,
    --   "competitiveness": 22
    -- }

    -- 상세 결과 (JSONB)
    details JSONB NOT NULL DEFAULT '{}',
    -- {
    --   "robots_txt": { "exists": false, "issues": [...] },
    --   "sitemap": { "exists": true, "url_count": 12, "issues": [...] },
    --   ...
    -- }

    -- 경쟁사 벤치마크
    benchmark JSONB,
    -- {
    --   "competitors": [
    --     { "name": "XX피부과", "url": "...", "score": 78 },
    --     ...
    --   ]
    -- }

    -- 리포트
    report_url TEXT,                      -- Supabase Storage URL
    screenshots JSONB,                    -- 스크린샷 URL 목록

    -- 메타
    scan_duration_ms INTEGER,
    source TEXT DEFAULT 'web',            -- web, api, batch
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audits_hospital ON audits(hospital_id);
CREATE INDEX idx_audits_status ON audits(status);
CREATE INDEX idx_audits_created ON audits(created_at DESC);
```

#### leads

```sql
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_id UUID REFERENCES audits(id),

    -- 연락처
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    hospital_name TEXT,
    phone TEXT,
    specialty TEXT,

    -- 퍼널 상태
    status TEXT DEFAULT 'new',
    -- new -> contacted -> consulting -> proposal_sent
    -- -> contracted -> active -> churned

    -- 추적
    notes JSONB DEFAULT '[]',
    -- [{ "date": "...", "content": "상담 완료. SEO 관심 높음", "author": "admin" }]

    emails_sent INTEGER DEFAULT 0,
    last_email_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_email ON leads(email);
```

#### audit_items

```sql
CREATE TABLE audit_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_id UUID REFERENCES audits(id) ON DELETE CASCADE,

    category TEXT NOT NULL,               -- technical_seo, performance, geo_aeo, multilingual, competitiveness
    item_key TEXT NOT NULL,               -- robots_txt, sitemap, meta_title, etc.

    status TEXT NOT NULL,                 -- pass, warn, fail, info
    score REAL,                           -- 0.0 - 1.0 (해당 항목의 정규화 점수)
    weight REAL,                          -- 가중치 (0.0 - 1.0)

    details JSONB,                        -- 상세 결과 (항목별 다름)
    suggestion TEXT,                      -- 개선 권고사항
    priority TEXT,                        -- critical, high, medium, low

    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_items_audit ON audit_items(audit_id);
CREATE INDEX idx_audit_items_category ON audit_items(category);
```

### 6.3 Supabase RLS (Row Level Security) 정책

```sql
-- 관리자만 모든 데이터 접근 (초기 MVP는 단일 관리자)
ALTER TABLE hospitals ENABLE ROW LEVEL SECURITY;
ALTER TABLE audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- 공개 진단: 누구나 진단 생성 가능
CREATE POLICY "Anyone can create audit" ON audits
    FOR INSERT TO anon WITH CHECK (true);

-- 진단 결과 조회: 자신의 진단만
CREATE POLICY "Users can view own audit" ON audits
    FOR SELECT TO anon USING (id = current_setting('app.audit_id')::uuid);

-- 관리자: 전체 접근
CREATE POLICY "Admin full access" ON audits
    FOR ALL TO authenticated USING (
        auth.jwt() ->> 'role' = 'admin'
    );
```

---

## 7. API 설계

### 7.1 아키텍처 개요

```
Client (Next.js)     API Gateway (Next.js API Routes)     Worker (FastAPI)
     │                        │                                │
     │  POST /api/audits      │                                │
     │ ─────────────────────> │                                │
     │                        │  POST /worker/scan             │
     │                        │ ────────────────────────────> │
     │                        │                                │  크롤링
     │                        │                                │  분석
     │  GET /api/audits/:id   │                                │  점수 산출
     │ ─────────────────────> │  (Supabase Realtime)           │
     │  <── SSE/WebSocket ──  │  <── DB Update ───────────── │
     │                        │                                │
     │  POST /api/leads       │                                │
     │ ─────────────────────> │                                │
     │                        │  (이메일 발송)                  │
```

### 7.2 Public API (Next.js API Routes)

#### 진단 생성

```
POST /api/audits
Content-Type: application/json

Request:
{
    "url": "https://example-clinic.com",
    "specialty": "dermatology"        // optional
}

Response (202 Accepted):
{
    "id": "uuid",
    "status": "pending",
    "estimated_time_seconds": 60
}
```

#### 진단 결과 조회

```
GET /api/audits/:id

Response (200):
{
    "id": "uuid",
    "url": "https://example-clinic.com",
    "status": "completed",
    "total_score": 38,
    "grade": "D",
    "scores": {
        "technical_seo": 32,
        "performance": 45,
        "geo_aeo": 18,
        "multilingual": 0,
        "competitiveness": 22
    },
    "summary": {
        "critical_issues": 5,
        "warnings": 12,
        "passed": 8
    },
    "scan_duration_ms": 45000,
    "created_at": "2026-03-25T10:00:00Z"
}
```

#### 진단 상세 (게이트 후)

```
GET /api/audits/:id/details
Authorization: Bearer {lead_token}

Response (200):
{
    "items": [
        {
            "category": "technical_seo",
            "item_key": "robots_txt",
            "status": "fail",
            "score": 0,
            "suggestion": "robots.txt 파일이 존재하지 않습니다...",
            "priority": "critical"
        },
        ...
    ],
    "benchmark": {
        "competitors": [
            { "name": "XX피부과", "score": 78, "rank": 1 },
            { "name": "YY피부과", "score": 65, "rank": 2 },
            { "name": "ZZ피부과", "score": 52, "rank": 3 }
        ],
        "your_rank": 15,
        "total_in_category": 23
    },
    "report_url": "https://storage.../report.pdf"
}
```

#### 리드 생성 (정보 입력)

```
POST /api/leads
Content-Type: application/json

Request:
{
    "audit_id": "uuid",
    "email": "park@gangnam-skin.kr",
    "name": "박지현",
    "hospital_name": "강남피부과",
    "phone": "02-1234-5678",
    "specialty": "dermatology"
}

Response (201):
{
    "id": "uuid",
    "token": "jwt_token",      // 상세 리포트 접근용
    "report_url": "https://..."
}
```

### 7.3 Worker API (FastAPI)

#### 크롤링/분석 작업 실행

```
POST /worker/scan
Content-Type: application/json

Request:
{
    "audit_id": "uuid",
    "url": "https://example-clinic.com",
    "options": {
        "depth": 3,                    // 크롤링 깊이
        "max_pages": 50,               // 최대 페이지 수
        "check_geo": true,             // GEO/AEO 진단 포함
        "benchmark": true,             // 경쟁사 벤치마크 포함
        "screenshot": true             // 스크린샷 촬영
    }
}

Response (202 Accepted):
{
    "task_id": "uuid",
    "status": "queued"
}
```

#### 배치 크롤링

```
POST /worker/batch-scan
Content-Type: application/json

Request:
{
    "urls": [
        { "url": "https://clinic-a.com", "specialty": "dermatology" },
        { "url": "https://clinic-b.com", "specialty": "plastic_surgery" }
    ],
    "options": {
        "depth": 1,
        "check_geo": false,
        "screenshot": false
    }
}

Response (202 Accepted):
{
    "batch_id": "uuid",
    "total": 2,
    "status": "queued"
}
```

### 7.4 내부 API (Admin Only)

```
# 관리자 대시보드
GET    /api/admin/dashboard/stats       # 통계 요약
GET    /api/admin/leads                 # 리드 목록 (필터, 페이지네이션)
GET    /api/admin/leads/:id             # 리드 상세
PATCH  /api/admin/leads/:id             # 리드 상태 변경, 메모 추가
GET    /api/admin/audits                # 진단 이력
GET    /api/admin/audits/:id            # 진단 상세
POST   /api/admin/audits/:id/resend     # 리포트 재발송
GET    /api/admin/hospitals             # 병원 DB (벤치마크용)
POST   /api/admin/hospitals/import      # 병원 DB 일괄 임포트

# 프로젝트 관리 (Phase B)
GET    /api/admin/projects              # 프로젝트 목록
POST   /api/admin/projects              # 프로젝트 생성
GET    /api/admin/projects/:id          # 프로젝트 상세
PATCH  /api/admin/projects/:id          # 프로젝트 상태 업데이트

# 이메일 관리
GET    /api/admin/emails/logs           # 이메일 발송 이력
POST   /api/admin/emails/send           # 수동 이메일 발송
```

---

## 8. 기술 스택

### 8.1 스택 선정 원칙

| 원칙 | 설명 |
|------|------|
| 1인 운영 최적화 | 유지보수 비용 최소화, 서버리스/매니지드 서비스 우선 |
| 기존 역량 활용 | Next.js + FastAPI + Python 스택 |
| AI 에이전트 친화적 | 코드 자동 생성/수정이 용이한 구조 |
| 점진적 확장 | MVP에서 시작하여 기능 추가가 쉬운 아키텍처 |

### 8.2 기술 스택 상세

#### Frontend

| 기술 | 버전 | 용도 | 선정 이유 |
|------|------|------|----------|
| **Next.js** | 15+ | 웹 프레임워크 | App Router, Server Components, API Routes |
| **TypeScript** | 5.x | 타입 안전성 | 엄격 모드 |
| **Tailwind CSS** | 4.x | 스타일링 | 빠른 UI 개발 |
| **shadcn/ui** | latest | UI 컴포넌트 | 커스터마이즈 용이, 접근성 |
| **TanStack Query** | 5.x | 서버 상태 관리 | 캐싱, 리페치, SSE 연동 |
| **Zustand** | 5.x | 클라이언트 상태 | 경량, 직관적 |
| **Recharts** | 2.x | 차트 | React 네이티브, 반응형 |
| **Framer Motion** | 11.x | 애니메이션 | 스캔 진행 UI, 점수 카운트업 |

#### Backend (API Gateway)

| 기술 | 용도 | 선정 이유 |
|------|------|----------|
| **Next.js API Routes** | Public API + Admin API | 프론트엔드와 동일 배포 |
| **Supabase Client** | DB 접근 | RLS, Realtime, Auth 통합 |
| **Resend** | 이메일 발송 | 트랜잭셔널 이메일, React Email 템플릿 |
| **Vercel Cron** | 스케줄링 | 자동 이메일 시퀀스, 재진단 알림 |

#### Backend (Worker / 크롤링 엔진)

| 기술 | 용도 | 선정 이유 |
|------|------|----------|
| **FastAPI** | Worker API | 비동기 처리, 자동 문서화, Python 에코시스템 |
| **Playwright** | 브라우저 크롤링 | JS 렌더링, 스크린샷, 모바일 에뮬레이션 |
| **BeautifulSoup4** | HTML 파싱 | 경량, 빠른 파싱 |
| **httpx** | HTTP 클라이언트 | 비동기, HTTP/2 지원 |
| **Pydantic** | 데이터 검증 | FastAPI 네이티브, 타입 안전 |
| **Celery** 또는 **arq** | 작업 큐 | 비동기 크롤링 작업 관리 |
| **Redis** | 큐 브로커 + 캐시 | Celery/arq 브로커, 진단 결과 캐싱 |

#### AI/LLM

| 기술 | 용도 | 선정 이유 |
|------|------|----------|
| **Google Gemini Flash** | 콘텐츠 분석, GEO 진단 | 빠르고 저렴, 한국어 우수 |
| **OpenAI GPT-4o-mini** | AI 검색 언급 확인, 보조 분석 | 정확도, 구조화 출력 |
| **Google PageSpeed Insights API** | 성능 분석 | 무료, Lighthouse 통합 |

#### 인프라 / 서비스

| 기술 | 용도 | 비용 (월) |
|------|------|----------|
| **Vercel** (Pro) | Next.js 호스팅, Edge Functions | ~$20 |
| **Supabase** (Pro) | PostgreSQL, Auth, Storage, Realtime | ~$25 |
| **Railway** 또는 **Fly.io** | FastAPI Worker 호스팅 | ~$10-20 |
| **Upstash Redis** | 작업 큐 브로커, 캐시, Rate Limit | ~$10 |
| **Resend** | 트랜잭셔널 이메일 | ~$20 (5K emails) |
| **Vercel Analytics** | 웹 분석 | 무료 |
| **Sentry** | 에러 모니터링 | 무료 (Dev) |
| **합계** | | **~$85-95/월 (~12만원)** |

### 8.3 모노레포 구조

```
mediscope/
├── apps/
│   ├── web/                          # Next.js (Vercel)
│   │   ├── app/
│   │   │   ├── (public)/             # 공개 페이지
│   │   │   │   ├── page.tsx          # 랜딩 (진단 입력)
│   │   │   │   ├── scan/[id]/        # 진단 진행/결과
│   │   │   │   └── report/[id]/      # 상세 리포트 (게이트)
│   │   │   ├── (admin)/              # 관리자 대시보드
│   │   │   │   ├── dashboard/
│   │   │   │   ├── leads/
│   │   │   │   ├── audits/
│   │   │   │   └── projects/
│   │   │   └── api/                  # API Routes
│   │   │       ├── audits/
│   │   │       ├── leads/
│   │   │       └── admin/
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn/ui
│   │   │   ├── audit/                # 진단 관련 컴포넌트
│   │   │   ├── report/               # 리포트 관련 컴포넌트
│   │   │   └── admin/                # 관리자 컴포넌트
│   │   ├── lib/
│   │   │   ├── supabase/
│   │   │   ├── email/
│   │   │   └── utils/
│   │   └── package.json
│   │
│   └── worker/                       # FastAPI (Railway/Fly.io)
│       ├── app/
│       │   ├── main.py               # FastAPI app
│       │   ├── api/
│       │   │   ├── scan.py           # 스캔 엔드포인트
│       │   │   └── batch.py          # 배치 크롤링
│       │   ├── scanner/
│       │   │   ├── technical.py      # 기술 SEO 분석
│       │   │   ├── performance.py    # 성능 분석 (PageSpeed API)
│       │   │   ├── geo_aeo.py        # GEO/AEO 분석
│       │   │   ├── multilingual.py   # 다국어 분석
│       │   │   ├── benchmark.py      # 경쟁사 벤치마크
│       │   │   └── scorer.py         # 종합 점수 산출
│       │   ├── crawler/
│       │   │   ├── browser.py        # Playwright 브라우저 관리
│       │   │   ├── parser.py         # HTML 파싱
│       │   │   └── screenshot.py     # 스크린샷
│       │   ├── report/
│       │   │   ├── generator.py      # PDF 생성
│       │   │   └── templates/        # HTML 템플릿
│       │   ├── tasks/
│       │   │   ├── worker.py         # Celery/arq worker
│       │   │   └── scheduler.py      # 스케줄링 작업
│       │   └── models/
│       │       ├── audit.py          # Pydantic 모델
│       │       └── score.py          # 점수 모델
│       ├── pyproject.toml
│       └── Dockerfile
│
├── packages/
│   └── shared/                       # 공유 타입, 상수
│       ├── types/
│       └── constants/
│
├── supabase/
│   ├── migrations/                   # DB 마이그레이션
│   └── seed.sql                      # 초기 데이터
│
├── turbo.json
└── package.json
```

---

## 9. 시스템 아키텍처

### 9.1 전체 아키텍처

```
                                 ┌──────────────────┐
                                 │   사용자 브라우저  │
                                 └────────┬─────────┘
                                          │
                                          v
                              ┌───────────────────────┐
                              │    Vercel (Next.js)    │
                              │  ┌─────────────────┐  │
                              │  │  Public Pages    │  │
                              │  │  (Landing, Scan, │  │
                              │  │   Report)        │  │
                              │  ├─────────────────┤  │
                              │  │  Admin Pages     │  │
                              │  │  (Dashboard,     │  │
                              │  │   Leads, Audits) │  │
                              │  ├─────────────────┤  │
                              │  │  API Routes      │  │
                              │  │  (/api/*)        │  │
                              │  └────────┬────────┘  │
                              └───────────┼───────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    v                     v                     v
          ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
          │    Supabase      │  │  Railway/Fly.io  │  │    Resend       │
          │  ┌────────────┐ │  │  ┌────────────┐  │  │                 │
          │  │ PostgreSQL  │ │  │  │  FastAPI    │  │  │  이메일 발송    │
          │  │ (DB)        │ │  │  │  Worker     │  │  │  (리포트,      │
          │  ├────────────┤ │  │  │            │  │  │   팔로업)       │
          │  │ Auth        │ │  │  │  Playwright │  │  │                 │
          │  ├────────────┤ │  │  │  크롤러     │  │  └─────────────────┘
          │  │ Storage     │ │  │  │            │  │
          │  │ (PDF, IMG)  │ │  │  │  LLM 분석  │  │
          │  ├────────────┤ │  │  └────────────┘  │
          │  │ Realtime    │ │  │        │         │
          │  │ (진행률)    │ │  │        v         │
          │  └────────────┘ │  │  ┌────────────┐  │
          └─────────────────┘  │  │   Redis     │  │
                               │  │  (Upstash)  │  │
                               │  │  작업 큐    │  │
                               │  └────────────┘  │
                               └──────────────────┘
                                        │
                          ┌─────────────┼─────────────┐
                          v             v             v
                   ┌───────────┐ ┌───────────┐ ┌───────────┐
                   │ PageSpeed │ │  Gemini   │ │  GPT-4o   │
                   │ API       │ │  Flash    │ │  mini     │
                   │ (Google)  │ │  (Google) │ │ (OpenAI)  │
                   └───────────┘ └───────────┘ └───────────┘
```

### 9.2 진단 프로세스 시퀀스

```
User          Next.js API       Redis Queue       FastAPI Worker       Supabase
 │                │                  │                   │                │
 │  POST /audit   │                  │                   │                │
 │ ──────────────>│                  │                   │                │
 │                │  INSERT audit    │                   │                │
 │                │ ──────────────────────────────────────────────────────>│
 │                │  ENQUEUE scan    │                   │                │
 │                │ ────────────────>│                   │                │
 │  audit_id      │                  │                   │                │
 │ <──────────────│                  │                   │                │
 │                │                  │  DEQUEUE          │                │
 │                │                  │ ────────────────>│                │
 │                │                  │                   │                │
 │  SSE subscribe │                  │     1. HTTP fetch (robots, sitemap)│
 │ ──────────────>│                  │     2. Playwright (full page)     │
 │                │                  │     3. PageSpeed API              │
 │                │                  │     4. LLM analysis               │
 │                │                  │     5. Score calculation           │
 │                │                  │     6. Screenshot                  │
 │                │                  │     7. PDF generation              │
 │                │                  │                   │                │
 │                │                  │  UPDATE audit     │                │
 │                │                  │  (진행률 20%)      │                │
 │                │                  │ ──────────────────────────────────>│
 │  SSE: 20%      │  Realtime        │                   │                │
 │ <──────────────│ <─────────────────────────────────────────────────────│
 │                │                  │                   │                │
 │                │                  │  ...반복...        │                │
 │                │                  │                   │                │
 │                │                  │  UPDATE audit     │                │
 │                │                  │  (완료, 점수)     │                │
 │                │                  │ ──────────────────────────────────>│
 │  SSE: complete │  Realtime        │                   │                │
 │ <──────────────│ <─────────────────────────────────────────────────────│
 │                │                  │                   │                │
```

### 9.3 Rate Limiting / Abuse 방지

```
진단 요청 제한:
- IP당: 5회/시간, 20회/일
- 동일 URL: 1회/24시간 (캐시 반환)
- 구현: Upstash Redis Rate Limiter (@upstash/ratelimit)

크롤링 예의:
- robots.txt 준수 (단, 진단 목적이므로 전체 사이트 크롤링은 아님)
- 크롤링 간격: 1초/요청
- User-Agent: MediScope Bot/1.0
- 동시 크롤링: 최대 5개 병렬
```

---

## 10. LINE/WeChat 채널 세팅 도구 (SEO 패키지 부가 서비스)

> Phase D (Post-MVP, Month 4+) - 첫 수익 발생 후 개발
> **참고**: LINE 연동은 이전 프로젝트에서 구현 완료 경험 보유 (LINE_MESSAGING.md, 260325_wechat_admin_chat.md)

### 10.1 포지셔닝: 독립 제품이 아닌 SEO 패키지의 부가 도구

> **핵심 관점**: LINE/WeChat은 MediScope의 주력 상품이 아니다.
> 경쟁 병원들이 이미 LINE/WeChat으로 해외 환자와 소통하고 있는 환경에서,
> 이를 갖추지 못한 병원에게 **공정한 경쟁 기회를 제공하는 도구**에 불과하다.

#### 비즈니스 구조

```
[MediScope가 하는 것]
1. 도구를 한번 만들어둠 (webhook 게이트웨이 + 관리 대시보드 + 번역 기능)
2. SEO 컨설팅 고객 병원에게 LINE/WeChat 세팅을 부가 서비스로 제공
3. 병원이 자기 LINE Official Account / WeChat Service Account를 발급
4. MediScope는 webhook 연결 + 대시보드 세팅만 해줌 (1~2일)

[MediScope가 하지 않는 것]
- 독립 메시징 제품으로 따로 판매 ✗
- 환자 데이터 직접 관리/소유 ✗
- 24/7 메시징 운영 책임 ✗
- 환자 유치/알선/소개 ✗
```

#### 왜 SEO 패키지에 포함되는가

MediScope 진단 25개 항목 중 **"해외 채널 링크 (LINE/WeChat)"** 항목이 있다.

```
진단 결과: "귀 병원은 LINE/WeChat이 없어 일본/중국 환자가 문의할 수 없습니다"
         "경쟁 병원 A, B, C는 모두 LINE 공식 계정을 운영 중입니다"
              ↓
MediScope: "SEO 최적화하면서 LINE도 세팅해드리겠습니다"
              ↓
검색에서 찾고 → 바로 문의하고 → 한국어로 소통 = 풀 퍼널 완결
```

기존 SEO 업체는 "트래픽 올려드리겠습니다"에서 끝나지만, MediScope는 **검색 노출 → 문의 전환**까지 책임지는 원스톱 서비스.

#### 가격 전략

| 항목 | 가격 | 형태 |
|------|------|------|
| LINE 1개 채널 세팅 | **패키지 포함** (SEO 프로젝트 500~1,500만원에 포함) | 1회성 |
| WeChat 추가 세팅 | +100~150만원 | 1회성 |
| 자동번역 기능 | +30~50만원/월 (API 실비 기반) | 월정액 |
| 의료 용어 사전 커스텀 | +100~200만원 | 1회성 |
| 대시보드 유지보수 | SEO 모니터링 구독에 포함 | 월정액 |

#### 법적 구조: 데이터 책임 분리

| 역할 | 주체 | 근거 |
|------|------|------|
| **개인정보처리자 (컨트롤러)** | 병원 | 자기 LINE/WeChat 계정 소유, 환자 대응 주체 |
| **수탁자 (프로세서)** | MediScope | webhook 경유, 번역 처리, 대시보드 제공 |
| **재위탁** | 번역 API (Gemini/DeepL) | MediScope → 번역 API 호출 시 재위탁 관계 |

필수 계약 문서:
- 개인정보 처리 위탁계약서 (병원 ↔ MediScope)
- 번역 기능 한계 및 면책 조항
- 재위탁(번역 API) 고지

#### 데이터 관리 정책

| 항목 | 정책 |
|------|------|
| 메시지 저장 | MediScope 서버에 암호화 저장, **30일 TTL** 후 자동 삭제 |
| 병원별 격리 | 멀티테넌트, 병원 A 관리자는 A 데이터만 접근 |
| 내보내기 | 병원이 원하면 대화 이력 CSV/JSON 내보내기 가능 |
| 접근 로그 | 관리자 접근/조회/발송 모든 이벤트 감사 로그 기록 |

#### 단계적 확대 로드맵

| Phase | 대상 | 시기 | 근거 |
|-------|------|------|------|
| D-1 | **LINE만** (일본/대만 시장) | 첫 수익 후 | 구현 경험 보유, 법적 복잡도 낮음 |
| D-2 | **WeChat 추가** (중국 시장) | D-1 검증 후 | Service Account 발급, PIPL 검토 완료 후 |
| D-3 | WhatsApp 추가 (동남아/중동) | 수요 확인 후 | 향후 |

#### BM 검증 결과 요약

| 평가 항목 | 독립 제품 (이전) | 부가 도구 (현재) |
|-----------|-----------------|-----------------|
| 시장 적합성 | 2/5 | **4/5** — SEO 풀 퍼널의 자연스러운 연장 |
| 기술 실행성 | 3/5 | **4/5** — 도구 한번 구축, 반복 활용 |
| 법적 리스크 | 1/5 | **3/5** — 책임 주체 병원으로 이동, 수탁자 의무만 |
| 경쟁 우위 | 1/5 | **4/5** — SEO+채널 번들은 명확한 차별화 |
| 수익 기여 | 1/5 | **4/5** — 패키지 가치 상승 + 번역 월정액 |
| **합계** | **8/25 (No-Go)** | **19/25 (조건부 Go)** |

### 10.2 자동 번역 시스템 (대시보드 내장 편의 기능)

> 병원 관리자가 외국어를 몰라도 해외 환자와 소통할 수 있게 하는 편의 기능.
> 의료 상담이 아닌 **초기 문의 대응** (비용, 예약, 일정)에 최적화.

#### 번역 워크플로우 (병원 관리자 확인 필수)

```
[수신] 환자 메시지 (외국어) → 자동 번역 → 원문 + 번역 동시 표시
[발송] 관리자 한국어 입력 → 번역 미리보기 → [수정 가능] → [발송 버튼]
       ※ 자동발송 아님 — 반드시 관리자가 확인 후 발송
```

#### 자동 삽입 면책 문구

모든 번역 발송 메시지 하단에 자동 삽입:
- 🇯🇵 `※このメッセージは自動翻訳です。正確な医療情報はご来院時にご確認ください。`
- 🇨🇳 `※此消息为自动翻译。准确的医疗信息请在就诊时确认。`
- 🇺🇸 `※This message is auto-translated. Please confirm medical details during your visit.`

#### 번역 기능 상세

| 기능 | 설명 | 우선순위 |
|------|------|---------|
| 수신 메시지 자동 번역 | 외국어 → 한국어 자동 표시 | Must |
| 발송 번역 미리보기 | 한국어 → 상대방 언어 미리보기 + 수정 가능 | Must |
| 면책 문구 자동 삽입 | 모든 번역 발송에 자동 삽입 | Must |
| 언어 자동 감지 | 첫 메시지에서 언어 판별 | Must |
| 의료 용어 사전 | 병원별 커스텀 시술명/진료과 번역 등록 | Should |
| 원문/번역 토글 | 원문↔번역 전환 표시 | Should |

#### 번역 비용

| 기술 | 메시지당 비용 | 월 예상 (500건 기준) |
|------|-------------|-------------------|
| Gemini Flash | ~$0.001 | ~$0.50 |
| DeepL API | ~$0.005 | ~$2.50 |
| Google Cloud Translation | ~$0.002 | ~$1.00 |

→ API 비용은 미미. 월정액(30~50만원)의 대부분이 마진.

### 10.3 LINE 연동 (구현 경험 기반)

> 이전 프로젝트에서 LINE Messaging API 양방향 채팅 시스템을 구현한 경험이 있으며,
> 아래는 검증된 아키텍처를 MediScope 멀티테넌트 구조에 맞게 확장한 설계다.

#### 검증된 아키텍처

**Inbound 흐름 (LINE 사용자 → Admin)**

```
LINE 사용자 메시지 전송
        ↓
LINE Platform → POST /webhook/line (FastAPI Worker)
        ↓
서명 검증 (HMAC-SHA256 + compare_digest) + Redis 중복 방지 (SET NX, TTL 1h)
        ↓
즉시 200 반환 + 백그라운드 태스크 (LINE은 ~20초 타임아웃)
        ↓
  ┌──────────────────────────────────────────┐
  │ LINE Profile API → displayName (Redis 캐시 24h) │
  │ 언어 감지 + 한국어 자동 번역 (Gemini Flash)       │
  │ DB 저장 (conversations + messages)              │
  │ Supabase Realtime → Admin 대시보드 실시간 알림    │
  └──────────────────────────────────────────┘
```

**Outbound 흐름 (Admin → LINE 사용자)**

```
Admin이 한국어로 메시지 입력 + 전송
        ↓
자동 번역: 한국어 → 대화 상대방 언어 (Gemini Flash)
        ↓
POST /api/conversations/{id}/reply (Next.js API Route)
        ↓
JWT 인증 + conversation status 검증
        ↓
LINE Push API (https://api.line.me/v2/bot/message/push)
        ↓
성공 시:
  ├── messages INSERT (direction='outbound', content=원문, translated_content=번역문)
  └── conversations 상태 자동 전환 (pending → in_progress)
```

#### 기술 요구사항 (검증 완료 항목 ✓)

| 항목 | 내용 | 상태 |
|------|------|------|
| LINE Messaging API | Official Account + Messaging API 채널 | ✓ 구현 경험 |
| Webhook 수신 | HMAC-SHA256 서명 검증 + Redis 멱등성 보장 | ✓ 구현 경험 |
| Push API 발송 | 텍스트/이미지/리치 메시지 발송 | ✓ 구현 경험 |
| Profile API | displayName + 프로필 이미지 (Redis 24h 캐시) | ✓ 구현 경험 |
| Rich Menu | 메뉴 카드 커스터마이즈 | 신규 개발 |
| LINE Login | 환자 식별 (향후) | 향후 |

#### 기능

| 기능 | 설명 | 우선순위 |
|------|------|---------|
| 메시지 수신/발송 | LINE 메시지 실시간 수신 + 관리자 답변 | Must |
| **실시간 자동 번역** | 수신: 외국어→한국어 / 발송: 한국어→상대방 언어 | Must |
| 자동 응답 | FAQ 기반 자동 답변 (다국어) | Should |
| 예약 알림 | 예약 확인/리마인더 발송 | Should |
| Rich Menu 관리 | 메뉴 카드 생성/수정 | Could |
| 환자 프로필 | LINE 사용자 정보 + 상담 이력 | Could |

#### LINE 비용

| 플랜 | 무료 메시지/월 | 추가 메시지 | 월비용 |
|------|-------------|-----------|--------|
| Communication | 200건 | 불가 | 무료 |
| Light | 5,000건 | 불가 | ~$50 |
| Standard | 30,000건 | ~$0.01/건 | ~$150 |

#### 구현 시 주의사항 (이전 경험 기반)

| 항목 | 내용 |
|------|------|
| Webhook 즉시 응답 | LINE은 ~20초 타임아웃. DB/번역/알림은 반드시 백그라운드 태스크로 분리 |
| 서명 검증 필수 | `compare_digest`로 타이밍 공격 방지, channel_secret 변경 시 양쪽 동기화 |
| 메시지 타입 처리 | text/image/video/audio/sticker/location/file 각각 별도 표시 텍스트 매핑 |
| 중복 방지 이중 보호 | Redis `SET NX` (webhookEventId) + DB `line_message_id` UNIQUE INDEX |
| Redis 장애 시 동작 | 중복 허용 (전달 누락보다 나음) — DB UNIQUE에서 최종 방어 |
| Admin 프록시 패턴 | 브라우저 → Next.js API Route → FastAPI Worker (CORS + 쿠키 정책) |

### 10.4 WeChat 연동 (구현 계획 수립 완료)

> LINE과 동일한 아키텍처를 재사용하되, WeChat 고유 제약에 대응.
> 상세 구현 계획: `260325_wechat_admin_chat.md`

#### LINE vs WeChat 핵심 차이 (구현 시 주의사항)

| 항목 | LINE | WeChat |
|------|------|--------|
| Webhook 포맷 | JSON | **XML** |
| 서명 검증 | HMAC-SHA256 (body) | **SHA1 (params)** + 선택적 AES 암호화 |
| 답장 방식 | Push API (시간 무제한) | **Customer Service API (48시간 제한)** |
| 48시간 초과 대응 | 불필요 | **Template Message로 재참여 유도** |
| 사용자 프로필 | displayName + pictureUrl | **nickname 비공개** (openid만) |
| access_token | 장기 Channel Access Token | **2시간마다 갱신 필요** |
| 텍스트 길이 | 5,000자 | **600자** |

#### 선행 조건: WeChat Service Account 해외 발급

| 항목 | 내용 |
|------|------|
| 계정 유형 | **Service Account (服务号)** 필수 — Subscription Account는 CS API 불가 |
| 신청 방식 | 한국 법인 직접 신청 (소유권 100% 본사) |
| 비용 | 연 $99 (WeChat 인증) + 에이전시 대행비 30~88만원 |
| 심사 기간 | 영업일 5~10일 |
| 필요 서류 | 영문 사업자등록증, 관리자 여권, 통신비 납부내역, 인증 신청서, 법인 은행계좌 |

> **중요**: 중국 에이전시 명의 차용(借用) 절대 금지 — 분쟁 시 계정+팔로워 전부 상실 위험

#### 48시간 Customer Service 창 관리

```
사용자 메시지 수신
        ↓
cs_window_expires_at = NOW() + 48시간 (DB 기록)
        ↓
Admin 답장 시:
  ├─ 창 열림 (48시간 내) → Customer Service API로 즉시 발송
  └─ 창 닫힘 (48시간 초과) → Template Message로 재참여 유도
                              "상담에 대한 답변이 준비되었습니다"
                              탭 → 웹서비스로 유도 → 새 메시지 → 창 다시 열림
```

#### Template Message 사전 등록 (WeChat 심사 필요)

| 템플릿 용도 | 내용 예시 | 심사 가능성 |
|-----------|---------|-----------|
| 상담 답변 알림 | "고객님의 상담에 대한 답변이 준비되었습니다" | 높음 |
| 예약 확인 | "시술 예약이 확정되었습니다" | 높음 |
| 가격 안내 | "요청하신 시술 견적이 준비되었습니다" | 높음 |

> 마케팅/광고성 템플릿은 심사 거절. "서비스 알림" 용도로만 신청.

#### 기능

| 기능 | 설명 | 우선순위 |
|------|------|---------|
| 메시지 수신/발송 | WeChat 메시지 수신 + CS API/Template 답장 | Must |
| **실시간 자동 번역** | 수신: 중국어→한국어 / 발송: 한국어→중국어 | Must |
| 48시간 창 관리 | 카운트다운 표시 + 만료 시 Template 자동 전환 | Must |
| access_token 자동 갱신 | 2시간마다 갱신, 만료 5분 전 선제 갱신 | Must |
| 자동 응답 | 키워드 기반 자동 답변 | Should |
| Template Message | 예약 확인, 결과 알림 | Should |
| 미니프로그램 | (향후) 예약/결제 미니앱 | Won't (MVP) |

#### LINE 코드 재사용율

| LINE 파일 | WeChat 대응 | 재사용율 |
|----------|------------|---------|
| Webhook 핸들러 | 서명/파싱 다름, 나머지 동일 | 60% |
| Push API 래퍼 | 엔드포인트/인증 다름 + 48h 분기 추가 | 70% |
| Admin CRUD | 테이블명만 다름 | 90% |
| Admin API 라우터 | 경로명만 다름 + 48h 응답 추가 | 90% |
| 채팅 UI 컴포넌트 | 48h 카운트다운 배너 추가 | 85% |
| API 프록시 라우트 | 경로만 다름 | 95% |

### 10.5 통합 대시보드 UI

```
┌─────────────────────────────────────────────────────────────────────┐
│  MediScope Messaging Dashboard                    [자동번역 ON 🟢]  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌────────────────────────────────────────────┐  │
│  │ 대화 목록     │  │  田中太郎 (LINE) 🇯🇵                       │  │
│  │              │  │                                            │  │
│  │ 🔴 田中太郎  │  │  14:30 田中:                               │  │
│  │   LINE|🇯🇵|2m │  │  ┌────────────────────────────────────┐   │  │
│  │              │  │  │ 鼻の整形について相談したいです。        │   │  │
│  │ ○ 王小明     │  │  │ 費用はいくらですか？                   │   │  │
│  │   WeChat|🇨🇳| │  │  │                                    │   │  │
│  │   1h        │  │  │ 🔄 코 성형에 대해 상담하고 싶습니다.   │   │  │
│  │              │  │  │    비용은 얼마인가요?                 │   │  │
│  │ ○ Sarah J.  │  │  └────────────────────────────────────┘   │  │
│  │   LINE|🇺🇸|3h│  │                                            │  │
│  │              │  │  14:32 관리자:                              │  │
│  │ 필터:        │  │  ┌────────────────────────────────────┐   │  │
│  │ [ALL]        │  │  │ 코 성형 비용은 200~400만원입니다.     │   │  │
│  │ [LINE]       │  │  │                                    │   │  │
│  │ [WeChat]     │  │  │ → 鼻整形の費用は200〜400万ウォンです。│   │  │
│  │              │  │  └────────────────────────────────────┘   │  │
│  │ 언어:        │  │                                            │  │
│  │ [ALL]        │  │  ┌──────────────────────────────────────┐ │  │
│  │ [🇯🇵 日本語] │  │  │ 한국어로 입력하세요...         [전송] │ │  │
│  │ [🇨🇳 中文]   │  │  │                                      │ │  │
│  │ [🇺🇸 English]│  │  │ 미리보기: (번역 결과가 여기 표시)     │ │  │
│  │              │  │  └──────────────────────────────────────┘ │  │
│  └──────────────┘  │                                            │  │
│                     │  [원문/번역 토글] [템플릿] [예약링크]      │  │
│                     └────────────────────────────────────────────┘  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  환자 정보                                                      │ │
│  │  이름: 田中太郎           언어: 🇯🇵 日本語 (자동 감지)          │ │
│  │  채널: LINE               첫 메시지: 2026-03-20                │ │
│  │  상담 이력: 3건           태그: [코성형] [상담중]              │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 10.6 LINE/WeChat 대시보드 기술 스택

| 기술 | 용도 |
|------|------|
| Next.js + Supabase Realtime | 실시간 메시지 UI (폴링 fallback 7초) |
| FastAPI + arq Worker | Webhook 수신 + Push 발송 + 번역 처리 |
| LINE Messaging API | LINE 연동 (✓ 검증 완료) |
| WeChat Official Account API | WeChat 연동 |
| Gemini Flash | 실시간 번역 + 언어 감지 + 자동 응답 |
| Redis (Upstash) | 중복 방지 + Profile 캐시 + 번역 캐시 |
| Supabase DB | 대화 이력, 환자 정보, 채널 설정 |
| Supabase Vault | 채널 시크릿/토큰 암호화 저장 |

### 10.7 LINE/WeChat 대시보드 데이터 모델 (추가)

```sql
-- 채널 연결 정보
CREATE TABLE messaging_channels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID REFERENCES hospitals(id),
    platform TEXT NOT NULL CHECK (platform IN ('line', 'wechat')),
    channel_id TEXT NOT NULL,         -- LINE Channel ID / WeChat AppID
    channel_secret TEXT NOT NULL,     -- Supabase Vault으로 암호화 저장
    access_token TEXT,                -- Supabase Vault으로 암호화 저장
    webhook_url TEXT,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    config JSONB,                     -- 플랫폼별 설정 (Rich Menu ID 등)
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 대화 (Conversation)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID REFERENCES messaging_channels(id),
    external_user_id TEXT NOT NULL,   -- LINE userId (U+32hex) / WeChat OpenID
    user_name TEXT,
    user_language TEXT,               -- 'ja', 'zh-CN', 'zh-TW', 'en', 'ko' (자동 감지)
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'resolved', 'archived')),
    tags TEXT[],
    last_message_at TIMESTAMPTZ,
    cs_window_expires_at TIMESTAMPTZ, -- WeChat 48시간 CS 창 만료 시각 (LINE은 NULL)
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 메시지 (원문 + 번역 동시 저장)
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    content TEXT NOT NULL,               -- 원문 (inbound: 외국어, outbound: 한국어)
    content_type TEXT DEFAULT 'text' CHECK (content_type IN ('text', 'image', 'video', 'audio', 'sticker', 'location', 'file')),
    original_language TEXT,              -- 감지된 원문 언어 코드
    translated_content TEXT,             -- 번역문 (inbound: 한국어, outbound: 상대방 언어)
    is_auto_reply BOOLEAN DEFAULT false,
    via_template BOOLEAN DEFAULT false,  -- WeChat: Template Message로 발송 여부 (48h 초과 시)
    platform_message_id TEXT,            -- LINE message ID / WeChat MsgId (중복 방지)
    sender_name TEXT,                    -- LINE displayName 또는 admin 이름
    metadata JSONB,                      -- 플랫폼별 추가 데이터
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 인덱스 (이전 구현 경험 기반 최적화)
CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
CREATE UNIQUE INDEX idx_messages_platform_dedup ON messages(platform_message_id) WHERE platform_message_id IS NOT NULL;
CREATE INDEX idx_conversations_channel ON conversations(channel_id, last_message_at DESC);
CREATE INDEX idx_conversations_status ON conversations(status) WHERE status IN ('pending', 'in_progress');

-- 의료 용어 사전 (번역 정확도 향상)
CREATE TABLE medical_terms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ko TEXT NOT NULL,                    -- 한국어 용어
    ja TEXT,                             -- 일본어
    zh_cn TEXT,                          -- 중국어 간체
    zh_tw TEXT,                          -- 중국어 번체
    en TEXT,                             -- 영어
    category TEXT,                       -- 'procedure', 'department', 'symptom'
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### 10.8 Redis 키 구조 (LINE/WeChat 공용)

| 키 패턴 | TTL | 용도 |
|---------|-----|------|
| `mediscope:msg:dedup:{webhookEventId}` | 1시간 | Webhook 이벤트 중복 방지 |
| `mediscope:msg:profile:{platform}:{userId}` | 24시간 | LINE/WeChat 프로필 캐시 |
| `mediscope:msg:translate:{hash}` | 7일 | 번역 결과 캐시 (동일 문장 반복 방지) |
| `mediscope:msg:lang:{userId}` | 30일 | 사용자 언어 감지 결과 캐시 |

---

## 11. MVP 우선순위 (MoSCoW)

### 11.1 Phase A: 진단 도구 MVP (Week 1-6)

#### Must Have (반드시 있어야 하는 것)

| ID | 기능 | 설명 | 예상 공수 |
|----|------|------|----------|
| M1 | URL 입력 + 진단 시작 | 단일 URL 입력, 진단 요청 생성 | 0.5일 |
| M2 | 기술 SEO 진단 (10개 항목) | robots.txt, sitemap, meta tags, heading, alt, links, HTTPS, canonical, URL, 4xx | 5일 |
| M3 | Core Web Vitals 진단 | PageSpeed Insights API 연동 (LCP, INP, CLS, 성능 점수) | 2일 |
| M4 | 종합 점수 산출 | 가중치 기반 0-100점, 등급(A-F) | 1일 |
| M5 | 실시간 진행 표시 | SSE/Realtime으로 진행률 표시 | 1.5일 |
| M6 | 프리뷰 결과 페이지 | 종합 점수 + 카테고리별 바 차트 | 2일 |
| M7 | 리드 수집 폼 | 이메일, 병원명, 담당자명 (게이트) | 1일 |
| M8 | 상세 리포트 페이지 | 항목별 Pass/Warn/Fail + 권고사항 | 3일 |
| M9 | PDF 리포트 생성 | HTML -> PDF 변환, Storage 저장 | 2일 |
| M10 | 리포트 이메일 발송 | 리드 정보 입력 후 자동 발송 | 1일 |
| M11 | 랜딩페이지 | 메인 히어로, 가치 제안, 사용법, FAQ | 2일 |
| M12 | Rate Limiting | IP/URL 기반 요청 제한 | 0.5일 |
| | **소계** | | **21.5일** |

#### Should Have (있으면 좋은 것)

| ID | 기능 | 설명 | 예상 공수 |
|----|------|------|----------|
| S1 | GEO/AEO 진단 (5개 항목) | 구조화 데이터, FAQ, 콘텐츠 명확성, AI 검색 언급, E-E-A-T | 4일 |
| S2 | 다국어 진단 (4개 항목) | 다국어 페이지, hreflang, 해외 채널, GBP | 2일 |
| S3 | 관리자 대시보드 (기본) | 통계 요약, 진단 목록, 리드 목록 | 3일 |
| S4 | 자동 이메일 시퀀스 | 3일/7일/14일 후 팔로업 (Vercel Cron) | 2일 |
| S5 | 스크린샷 포함 리포트 | 전체 페이지 + 문제 영역 스크린샷 | 1.5일 |
| | **소계** | | **12.5일** |

#### Could Have (가능하면 넣을 것)

| ID | 기능 | 설명 | 예상 공수 |
|----|------|------|----------|
| C1 | 경쟁사 벤치마크 | 동일 진료과 상위 3개 병원 비교 | 3일 |
| C2 | 벌크 진단 (배치) | 등록 기관 전수 크롤링 | 3일 |
| C3 | 관리자: 리드 상세 | 메모 추가, 상태 변경, 이메일 이력 | 2일 |
| C4 | 소셜 공유 카드 | 진단 결과 OG Image 동적 생성 | 1일 |
| C5 | 일본어/영어 랜딩페이지 | 해외 에이전시/병원 대상 | 2일 |
| | **소계** | | **11일** |

#### Won't Have (이번 MVP에서 안 할 것)

| ID | 기능 | 이유 |
|----|------|------|
| W1 | LINE/WeChat 채널 세팅 도구 | Phase D — SEO 패키지 부가 서비스로 제공 (독립 제품 아님, LINE 구현 경험 보유) |
| W2 | 홈페이지 리디자인/리빌드 기능 | 스코프 외 (별도 서비스) |
| W3 | 환자 예약 시스템 | 복잡도 높음, 별도 제품 |
| W4 | CRM 통합 (Salesforce, HubSpot) | 초기 불필요 |
| W5 | Google Ads / Meta Ads 연동 | 스코프 외 |
| W6 | 모바일 앱 | 웹 우선 |
| W7 | 다국어 관리자 UI | 1인 운영, 한국어 우선 |

### 11.2 Phase B: 최적화 서비스 도구 (Week 7-10)

| ID | 기능 | 우선순위 | 예상 공수 |
|----|------|---------|----------|
| B1 | 프로젝트 생성/관리 | Must | 2일 |
| B2 | 최적화 작업 체크리스트 | Must | 2일 |
| B3 | Before/After 비교 리포트 | Must | 2일 |
| B4 | 점수 추이 차트 | Should | 1일 |
| B5 | 클라이언트 공유 링크 | Should | 1일 |
| | **소계** | | **8일** |

### 11.3 Phase C: 구독 모니터링 (Week 11-12)

| ID | 기능 | 우선순위 | 예상 공수 |
|----|------|---------|----------|
| C-1 | 주간/월간 자동 재진단 | Must | 2일 |
| C-2 | 점수 변동 알림 (이메일) | Must | 1일 |
| C-3 | 경쟁사 순위 트래킹 | Should | 2일 |
| C-4 | 월간 리포트 자동 발송 | Should | 1.5일 |
| | **소계** | | **6.5일** |

---

## 12. 12주 MVP 로드맵

### 12.1 주차별 상세 계획

```
Week 1: 프로젝트 셋업 + 크롤링 엔진 기초
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-2]  모노레포 초기화 (Turborepo + Next.js + FastAPI)
           Supabase 프로젝트 생성, DB 스키마 마이그레이션
           Vercel + Railway 배포 파이프라인 구성
[Day 3-5]  Playwright 크롤러 기본 구조
           HTTP 요청 기반 분석 (robots.txt, sitemap, meta)
           단위 테스트 작성

Week 2: 기술 SEO 진단 엔진 완성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-3]  나머지 기술 SEO 항목 구현
           (heading, alt, links, HTTPS, canonical, URL, 4xx)
[Day 4-5]  PageSpeed Insights API 연동 (Core Web Vitals)
           종합 점수 산출 로직 (가중치 기반)

Week 3: GEO/AEO + 다국어 진단
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-3]  구조화 데이터 분석 (JSON-LD, MedicalClinic 스키마)
           LLM 기반 콘텐츠 분석 (E-E-A-T, 명확성)
[Day 4-5]  다국어 페이지 감지 + hreflang 검증
           해외 채널 링크 감지 (LINE, WeChat, WhatsApp)

Week 4: 프론트엔드 - 진단 UI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-2]  랜딩페이지 (히어로, URL 입력, 가치 제안)
[Day 3-4]  진단 진행 페이지 (실시간 프로그레스)
           Supabase Realtime 연동
[Day 5]    프리뷰 결과 페이지 (점수, 바 차트, 등급)

Week 5: 리포트 + 리드 수집
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-2]  리드 수집 폼 (게이트)
           상세 리포트 페이지 (항목별 Pass/Warn/Fail)
[Day 3-4]  PDF 리포트 생성 (HTML 템플릿 -> Playwright PDF)
           스크린샷 포함
[Day 5]    이메일 발송 (Resend + React Email 템플릿)

Week 6: 관리자 대시보드 + 이메일 자동화 + 런칭 준비
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Day 1-2]  관리자 대시보드 (통계, 진단 목록, 리드 목록)
           Supabase Auth (관리자 로그인)
[Day 3]    자동 이메일 시퀀스 (Vercel Cron)
[Day 4]    Rate Limiting, 에러 처리, 보안 점검
[Day 5]    QA, 버그 수정, 소프트 런칭

         ──────── Phase A 완료 (MVP v1.0) ────────

Week 7-8: 경쟁사 벤치마크 + 벌크 진단
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[W7 D1-3]  등록 기관 리스트 수집 + DB 임포트
           배치 크롤링 시스템 구축
[W7 D4-5]  경쟁사 벤치마크 기능 (레이더 차트)
[W8 D1-3]  벌크 진단 실행 (3,154개 기관)
[W8 D4-5]  콜드 아웃리치 타겟 리스트 추출
           아웃리치 이메일 템플릿 작성

Week 9-10: 프로젝트 관리 도구 (Phase B)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[W9 D1-3]  프로젝트 CRUD + 체크리스트
[W9 D4-5]  Before/After 비교 리포트
[W10 D1-2] 점수 추이 차트
[W10 D3-5] 클라이언트 공유 링크 + QA

         ──────── Phase B 완료 (v1.1) ────────

Week 11-12: 구독 모니터링 (Phase C) + 첫 고객 확보
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[W11 D1-3] 자동 재진단 시스템 (주간/월간)
[W11 D4-5] 점수 변동 알림 + 월간 리포트
[W12 D1-3] 경쟁사 순위 트래킹
[W12 D4-5] 최종 QA, 성능 최적화

         ──────── Phase C 완료 (v1.2) ────────
```

### 12.2 마일스톤 요약

| 마일스톤 | 시점 | 산출물 | 핵심 지표 |
|---------|------|--------|----------|
| M1: 크롤링 엔진 완성 | Week 3 | 25개 진단 항목 동작 | 1개 URL 60초 내 진단 |
| M2: MVP v1.0 런칭 | Week 6 | 진단 도구 + 리드 수집 + 관리자 | 첫 100회 진단 |
| M3: 벤치마크 DB 구축 | Week 8 | 3,154개 기관 진단 완료 | 아웃리치 리스트 확보 |
| M4: 프로젝트 관리 v1.1 | Week 10 | 유료 고객용 대시보드 | 첫 유료 계약 |
| M5: 모니터링 v1.2 | Week 12 | 구독 모니터링 서비스 | MRR 시작 |

### 12.3 주간 버퍼

각 Phase에 1일 정도의 버퍼를 포함. 예상치 못한 기술적 이슈, 외부 API 장애, LLM 프롬프트 튜닝 등에 대응.

---

## 13. 비기능 요구사항

### 13.1 성능

| 항목 | 목표 | 비고 |
|------|------|------|
| 진단 완료 시간 | 60초 이내 (기본), 120초 이내 (GEO 포함) | Playwright 최적화 |
| 랜딩페이지 로드 | LCP 2.5초 이내 | Next.js SSG |
| 관리자 대시보드 로드 | FCP 1.5초 이내 | Server Components |
| PDF 생성 | 10초 이내 | 템플릿 사전 준비 |
| 동시 진단 처리 | 10건 | Worker 스케일링 |

### 13.2 보안

| 항목 | 방법 |
|------|------|
| 관리자 인증 | Supabase Auth (이메일/비밀번호) + MFA(TOTP) 권장 |
| API 인증 | JWT (리드 토큰), API Key (관리자) |
| Worker API 인증 | API Key + Private Network (이중 보안) |
| 데이터 암호화 | HTTPS 전송, Supabase 저장소 암호화 |
| Rate Limiting | Upstash Redis (@upstash/ratelimit) — IP/URL 단위 |
| CORS | Vercel 도메인만 허용 |
| SSRF 방지 | 크롤링 URL 입력 시 내부 IP 대역 차단 (localhost, 10.x, 172.16-31.x, 169.254.x), HTTPS만 허용 |
| 입력 검증 | Pydantic(Worker) / Zod(Next.js)로 모든 사용자 입력 검증 |
| 민감정보 | 환경변수 (.env), Vercel Secrets |

### 13.3 법적 컴플라이언스

#### 13.3.1 서비스 범위 법적 정의

| 구분 | MediScope 서비스 | 법적 성격 | 리스크 |
|------|-----------------|-----------|--------|
| 기술적 SEO 최적화 | 사이트 구조, 속도, 스키마, 메타태그 | IT 기술 컨설팅 | **낮음** |
| 분석 리포트 제공 | SEO/GEO 점수, 개선 권고 | 경영 컨설팅 | **낮음** |
| 콘텐츠 가이드라인 제공 | "이런 내용을 추가하세요" 방향 제시 | 컨설팅 | **낮음** |
| 콘텐츠 직접 수정 | 시술 설명, 의료진 소개 작성 | **의료광고 대행** | **높음 — 스코프 외** |
| LINE/WeChat 세팅 | webhook 연결 + 대시보드 구성 | 기술 서비스 | **낮음** |

> **원칙**: MediScope는 **콘텐츠를 직접 작성/수정하지 않는다.**
> 의료 콘텐츠 수정이 필요한 경우 가이드라인만 제공하고, 실제 작성은 병원이 직접 수행.
> 의료광고 심의 의무는 광고주(병원)에게 있으며, 계약서에 명시.

#### 13.3.2 개인정보보호

**리드 수집 폼 필수 요소**:
- [ ] 개인정보 수집·이용 동의 체크박스 (필수)
- [ ] 수집 항목: 이메일, 병원명, 담당자명, 전화번호(선택)
- [ ] 수집 목적: 진단 리포트 발송, 서비스 안내
- [ ] 보유 기간: 2년 (또는 동의 철회 시까지)
- [ ] 개인정보처리방침 링크
- [ ] 마케팅 수신 동의 체크박스 (선택, 별도)

**크롤링 수집 데이터**:
- 병원 사업자 정보 (상호, 주소, 전화) → 개인정보 아님 → 동의 불필요
- 의료진 개인 이름/사진 → 진단 리포트에 미포함

#### 13.3.3 크롤링 정책

| 항목 | 정책 | 법적 근거 |
|------|------|-----------|
| robots.txt | **100% 준수** (예외 없음) | 정보통신망법 제48조 판례 |
| 요청 빈도 | 1도메인당 최소 3초 간격 | 서버 부하 방지, 업무방해 예방 |
| User-Agent | `MediScope-Bot/1.0 (+https://mediscope.kr/bot)` | 신원 공개 |
| 크롤링 깊이 | 최대 3depth, 페이지 200개 제한 | 합리적 범위 |
| 차단 대응 | 403/429 수신 시 즉시 중단, 재시도 안 함 | |
| 기술적 보호조치 | CAPTCHA, IP 차단 등 우회 금지 | 정보통신망법 제48조 |
| 크롤링 로그 | 전수 보관 (분쟁 시 증빙용) | |

#### 13.3.4 콜드 아웃리치 제한

| 방법 | 합법 여부 | 조건 |
|------|-----------|------|
| 동의 없는 이메일 발송 | **위법** | 정보통신망법 제50조 — 과태료 3천만원 |
| 동의 없는 문자/카카오톡 | **위법** | 동일 |
| 무료 진단 후 동의 받은 이메일 | **합법** | 리드 폼에서 마케팅 동의 수집 |
| 사업자 공개 전화번호로 전화 | **합법** (B2B 관용) | 수신 거부 시 즉시 중단 |
| 오프라인 (컨퍼런스, 방문) | **합법** | 정보통신망법 적용 대상 아님 |

> **MediScope 영업 전략**: 무료 진단 도구를 인바운드 퍼널로 활용하여 합법적 리드 확보.
> 벌크 진단(3,154개 기관) 결과를 직접 이메일하지 않고, 콘텐츠 마케팅 소재로만 활용.

#### 13.3.5 진단 리포트 면책

모든 리포트(무료/유료)에 아래 면책 문구 필수 삽입:

> "본 리포트는 웹사이트의 기술적 SEO/GEO 지표를 자동 분석한 것이며, 의료 서비스의 품질이나 안전성을 평가한 것이 아닙니다. 리포트의 점수와 권장 사항은 검색 엔진 최적화 관점의 기술적 분석이며, 의료광고 심의를 대체하지 않습니다. 검색 순위는 외부 요인에 의해 결정되므로 특정 결과를 보장하지 않습니다."

#### 13.3.6 외국인환자유치사업자 등록

| 서비스 범위 | 등록 필요 여부 |
|-------------|---------------|
| SEO/GEO 기술 컨설팅 | 불필요 (기술 서비스) |
| 콘텐츠 가이드라인 제공 | 불필요 (컨설팅) |
| LINE/WeChat webhook 세팅 | 불필요 (기술 서비스) |
| LINE/WeChat으로 환자 직접 중개 | **필요할 수 있음** |

> **조치**: Phase D (LINE/WeChat 세팅 서비스) 시작 전,
> 보건복지부/한국보건산업진흥원에 유권해석 요청하여 등록 필요 여부 확정.

### 13.4 가용성

| 항목 | 목표 |
|------|------|
| 가동률 | 99.5% (Vercel + Supabase SLA) |
| 장애 복구 | 자동 재시작 (Vercel/Railway) |
| 데이터 백업 | Supabase 일일 자동 백업 |
| 모니터링 | Sentry (에러), Vercel Analytics (트래픽) |

### 13.4 확장성

| 시기 | 동시 사용자 | 일일 진단 | 인프라 |
|------|-----------|----------|--------|
| 초기 (Month 1-3) | ~50 | ~30 | 기본 플랜 |
| 중기 (Month 4-6) | ~200 | ~100 | Worker 스케일업 |
| 후기 (Month 7-12) | ~500 | ~300 | Worker 복수 인스턴스 |

---

## 14. 성공 지표

### 14.1 Product Metrics

| 지표 | Month 2 | Month 3 | Month 6 | 측정 방법 |
|------|---------|---------|---------|----------|
| 월 진단 실행 수 | 100+ | 300+ | 1,000+ | DB COUNT |
| 진단 완료율 | 80%+ | 85%+ | 90%+ | completed / total |
| 리드 전환율 (진단 -> 정보 입력) | 20%+ | 25%+ | 30%+ | leads / audits |
| 상담 전환율 (리드 -> 상담) | 5%+ | 8%+ | 10%+ | consulting / leads |

### 14.2 Business Metrics

| 지표 | Month 3 | Month 6 | Month 12 | 측정 방법 |
|------|---------|---------|----------|----------|
| 유료 계약 수 | 3+ | 10+ | 25+ | contracts |
| 프로젝트 매출 (누적) | 1,500만원 | 5,000만원 | 1.5억원 | invoices |
| MRR | - | 150만원 | 500만원 | 구독 매출 |
| 고객 이탈률 | - | <10% | <8% | churned / active |

### 14.3 Technical Metrics

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 진단 정확도 | 수동 감사 대비 90%+ 일치 | 샘플 10개 수동 검증 |
| 시스템 가동률 | 99.5%+ | Vercel/Railway 모니터링 |
| 진단 평균 소요 시간 | 60초 이내 | DB 통계 |
| 에러율 | <2% | Sentry |

---

## 부록 A: 진단 항목 전체 체크리스트

> **상세 채점 기준**: `05-research/scoring-engine-reference.md` 참조
> 각 항목의 Pass/Warn/Fail 기준, GEO 측정 프로토콜, 의료관광 특화 보너스/감산 항목 포함

| # | 카테고리 | 항목 | 가중치 | Phase |
|---|---------|------|--------|-------|
| 1 | 기술 SEO | robots.txt 존재/설정 | 3% | A |
| 2 | 기술 SEO | sitemap.xml 존재/유효성 | 3% | A |
| 3 | 기술 SEO | Meta Title (존재/길이/고유성) | 5% | A |
| 4 | 기술 SEO | Meta Description (존재/길이) | 4% | A |
| 5 | 기술 SEO | Heading 구조 (H1 고유, 계층) | 4% | A |
| 6 | 기술 SEO | 이미지 ALT 태그 비율 | 4% | A |
| 7 | 기술 SEO | 내부 링크 / 깨진 링크 | 4% | A |
| 8 | 기술 SEO | HTTPS / SSL | 3% | A |
| 9 | 기술 SEO | Canonical 태그 | 2% | A |
| 10 | 기술 SEO | URL 구조 (깨끗한 URL) | 3% | A |
| 11 | 기술 SEO | HTTP 상태 (4xx/5xx) | 5% | A |
| | | **기술 SEO 소계** | **40%** | |
| 12 | 성능 | LCP (Largest Contentful Paint) | 4% | A |
| 13 | 성능 | INP (Interaction to Next Paint) | 2% | A |
| 14 | 성능 | CLS (Cumulative Layout Shift) | 2% | A |
| 15 | 성능 | Lighthouse 성능 점수 | 3% | A |
| 16 | 성능 | 모바일 반응형 (Viewport, 터치) | 4% | A |
| | | **성능 소계** | **15%** | |
| 17 | GEO/AEO | 구조화 데이터 (Schema.org + 의료 스키마) | 7% | A |
| 18 | GEO/AEO | FAQ 콘텐츠 + 구조화 데이터 | 3% | A |
| 19 | GEO/AEO | 콘텐츠 명확성 + Fact-Density (하이브리드) | 4% | A |
| 20 | GEO/AEO | **AI 검색 노출 — Share of Model** (4개 엔진) | 6% | A |
| 21 | GEO/AEO | E-E-A-T 신호 (프록시 체크리스트) | 5% | A |
| | | **GEO/AEO 소계** | **25%** | |
| 22 | 다국어 | 다국어 페이지 존재 (3개+ 언어) | 6% | A |
| 23 | 다국어 | hreflang 태그 (양방향 + x-default) | 4% | A |
| 24 | 다국어 | 해외 채널/결제 연동 (LINE/WeChat/예약) | 5% | A |
| | | **다국어 소계** | **15%** | |
| 25 | 의료관광 특화 | 가산/감산 보너스 (스키마/인증/B·A/다국어/위반) | ±5% | A |
| 26 | 경쟁력 | 경쟁사 대비 SoM + 상대 점수 | - | B |
| | | **합계** | **100% (±5%)** | |

**등급 체계**: A+(95-100) / A(85-94) / B(70-84) / C(55-69) / D(40-54) / F(0-39)
**진단 비용**: ~$2-3/회 (API 호출) | **소요 시간**: 3-5분 (병렬 처리)

---

## 부록 B: 기술 참고 자료

### API 문서
- [Google PageSpeed Insights API v5](https://developers.google.com/speed/docs/insights/v5/get-started)
- [LINE Messaging API](https://developers.line.biz/en/docs/messaging-api/getting-started/)
- [WeChat Official Account API](https://wechatwiki.com/wechat-resources/wechat-overseas-official-account-registration-fees/)
- [Supabase Documentation](https://supabase.com/docs)
- [Resend API](https://resend.com/docs)

### 아키텍처 참고
- [Next.js + FastAPI Monorepo Template](https://github.com/vintasoftware/nextjs-fastapi-template)
- [SEOptimer SEO Audit API](https://www.seoptimer.com/seo-api/)
- [Schema.org MedicalClinic](https://schema.org/MedicalClinic)

### GEO/AEO 참고
- [GEO Complete Guide 2026 - Enrich Labs](https://www.enrichlabs.ai/blog/generative-engine-optimization-geo-complete-guide-2026)
- [AEO/GEO Benchmarks Report 2026 - Conductor](https://www.conductor.com/academy/aeo-geo-benchmarks-report/)
- [frase.io - SEO + GEO Platform](https://www.frase.io/)
- [Otterly.ai - AI Search Monitoring](https://otterly.ai/)
- [Peec AI - AI Search Analytics](https://peec.ai/)
- [Profound - Multi-LLM Monitoring](https://profound.so/)
- [HubSpot AEO Grader](https://www.hubspot.com/aeo-grader)
- [Incremys - 2026 GEO Statistics](https://www.incremys.com/en/resources/blog/geo-statistics)

### MediScope 내부 레퍼런스
- `05-research/scoring-engine-reference.md` — 채점 엔진 상세 기준 (Pass/Warn/Fail, GEO 프로토콜, 의료관광 보너스)
- `05-research/geo-aeo-scoring-research.md` — NotebookLM 리서치 리포트 (기존 도구 비교, LLM별 노출 메커니즘)
- `docs/260325-mediscope-sales-report-strategy.md` — 영업용 PPT 리포트 전략 (3막 12슬라이드, 셀링 포인트, 게이팅)
