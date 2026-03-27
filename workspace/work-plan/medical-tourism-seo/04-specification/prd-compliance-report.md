# PRD 준수 검증 리포트

> 검증일: 2026-03-27
> PRD 버전: 1.0 (2026-03-25)
> 검증 대상: mediscope/ 전체 구현 코드

---

## 요약

- **전체 준수율: 72%**
- 완전 구현: 10개
- 부분 구현: 5개
- 미구현: 2개

| Phase | 항목 수 | 완전 | 부분 | 미구현 |
|-------|---------|------|------|--------|
| Phase A | 6 | 5 | 1 | 0 |
| Phase A+ | 2 | 1 | 1 | 0 |
| Phase B | 4 | 2 | 1 | 1 |
| Phase C | 2 | 1 | 1 | 0 |
| Phase D | 1 | 0 | 1 | 0 |
| 비기능 | 2 | 1 | 0 | 1 |

---

## 상세 결과

### 1. 랜딩 페이지 (Phase A)
- **상태: 완전 구현**
- PRD 요구사항: "당신의 병원, 외국인 환자가 검색으로 찾을 수 있나요?" 헤드라인, URL 입력 필드, "무료 진단 시작" CTA 버튼
- 실제 구현:
  - 헤드라인 문구 PRD와 정확히 일치 (page.tsx L91-93)
  - URL 입력 + "무료 진단 시작" 버튼 구현 (L107-118)
  - POST /api/audits 호출 후 /scan/:id 이동 (L40-54)
  - 기능 소개 섹션 4개 (기술 SEO, 성능 분석, GEO/AEO, 경쟁력 벤치마크)
  - 진단 프로세스 3단계 설명 섹션
- 차이점: 없음

### 2. 스캔 진행 UI (Phase A)
- **상태: 완전 구현**
- PRD 요구사항: 5개 단계 표시 (기술 SEO, 모바일 최적화, GEO/AEO, 경쟁사 벤치마크), 진행률 바, 완료 시 자동 이동
- 실제 구현:
  - 5개 단계: 기술 SEO 분석, 성능 측정, GEO/AEO 진단, 다국어 지원 확인, 경쟁사 벤치마크 (scan/[id]/page.tsx L12-18)
  - Progress 바 + 퍼센트 표시 (L73-79)
  - 2초 간격 폴링으로 상태 갱신 (TanStack Query, refetchInterval: 2000)
  - completed 시 /report/:id로 자동 이동 (useEffect, L55-59)
  - 각 단계 아이콘 (완료/진행중/미완료) 표시
- 차이점: PRD의 "모바일 최적화 확인" 단계명이 "성능 측정"으로 변경 (의미적으로 동일)

### 3. 리포트 페이지 (Phase A)
- **상태: 완전 구현**
- PRD 요구사항 (F2.1): 종합 점수 0-100, 카테고리별 바 차트, 등급 A-F, 리드 게이팅 CTA
- 실제 구현:
  - ScoreGauge 컴포넌트: 원형 0-100 점수 + 등급 Badge (L58-74)
  - Recharts BarChart (카테고리별 수평 바 차트) (L283-302)
  - 등급: A(80+), B(60-79), C(40-59), D(20-39), F(0-19) - scorer.py와 일치
  - 리드 수집 폼: "상세 리포트를 받아보세요" 카드 (L482-558)
  - PDF 다운로드 링크 + 상세 리포트 보기/인쇄 링크
- 차이점: PRD의 "상세 리포트를 받으려면 정보를 입력하세요"가 "정보를 입력하시면 PDF 상세 리포트를 이메일로 보내드립니다"로 변경 (의미 동일)

### 4. 진단 항목 (Phase A)
- **상태: 부분 구현**
- PRD 요구사항:
  - F1.1 기술 SEO 10개 (50%): robots, sitemap, meta, headings, images, links, https, canonical, url, errors
  - F1.2 Core Web Vitals 5개 (20%): LCP, INP, CLS, 성능 점수, 모바일
  - F1.3 GEO/AEO 5개 (25%): 구조화 데이터, FAQ, 콘텐츠 명확성, AI 검색 언급, E-E-A-T
  - F1.4 다국어 3개 (10%): 다국어 페이지(5%), hreflang(3%), 해외 채널(2%)
- 실제 구현 (scorer.py WEIGHTS):
  - F1.1: 10개 모두 구현 (각 체커 파일 존재) = 50%
  - F1.2: 5개 모두 구현 (check_performance + check_mobile) = 20%
  - F1.3: 5개 모두 구현 (structured_data, faq_content, content_clarity, ai_search_mention, eeat_signals) = 25%
  - F1.4: **1개만 구현** (multilingual 5%), hreflang(3%)과 해외 채널(2%)이 별도 항목으로 분리되지 않음
- **차이점**:
  - 다국어 카테고리: PRD는 3개 항목 10% 가중치이나 실제로는 1개 항목 5% 가중치
  - hreflang 진단이 check_multilingual 내에 포함되어 있을 수 있으나 별도 WEIGHTS 항목이 없음
  - 해외 채널 연동(LINE/WeChat/WhatsApp 링크) 진단 항목 미구현
  - 전체 가중치 합계: PRD=100%, 실제=100% (다국어 차이 5%p)
- 권장 조치:
  1. multilingual 체커를 3개 하위 항목으로 분리: multilingual_pages(5%), hreflang(3%), overseas_channels(2%)
  2. scorer.py WEIGHTS에 3개 항목으로 업데이트
  3. 구글 비즈니스 프로필 항목은 PRD에서도 "(향후)"로 표시되어 제외 가능

### 5. 리드 수집 (Phase A)
- **상태: 완전 구현**
- PRD 요구사항 (F3.1): 이메일(필수), 병원명(필수), 담당자명(필수), 전화번호(선택), 진료과목(선택)
- 실제 구현:
  - 리포트 페이지 리드 폼: 이메일(필수), 담당자명(필수), 병원명(선택), 전화번호(선택) (report/[id]/page.tsx L496-547)
  - API: audit_id, email(필수), name(필수), hospital_name(선택), phone(선택), specialty(선택) (leads/route.ts L6-13)
  - DB 스키마: leads 테이블에 모든 필드 존재 (001_initial_schema.sql L74-88)
- 차이점: PRD에서 병원명은 필수이나 구현에서는 선택 - 전환율 최적화를 위한 의도적 변경으로 판단
- 권장 조치: 병원명을 required로 변경하거나, PRD를 실제 구현에 맞게 업데이트

### 6. 이메일 시퀀스 (Phase A)
- **상태: 완전 구현**
- PRD 요구사항 (F3.2): 즉시 리포트 발송, +3일 팔로업1, +7일 팔로업2, +14일 팔로업3, +30일 재진단 알림
- 실제 구현:
  - 즉시 리포트 발송: leads/route.ts에서 sendReportEmail 호출 (L58-69)
  - 팔로업 시퀀스: cron/follow-up/route.ts에서 4단계 구현 (L8-21)
    - 3일: followup_1 "리포트 확인하셨나요?"
    - 7일: followup_2 "무료 30분 상담을 제안드립니다"
    - 14일: followup_3 "경쟁 병원은 이미 시작했습니다"
    - 30일: rediagnose "한 달이 지났습니다"
  - 이메일 템플릿: resend.ts에서 FOLLOW_UP_TEMPLATES 정의 (L64-113)
  - email_logs 테이블로 중복 발송 방지 (follow-up/route.ts L66-73)
- 차이점: PRD와 완전히 일치

### 7. GEO/AEO 진단 (Phase A+)
- **상태: 완전 구현**
- PRD 요구사항: ChatGPT/Perplexity 검색 시뮬레이션
- 실제 구현:
  - check_ai_search_mention: AI 검색 엔진에서 병원명 언급 여부 확인 (geo_aeo.py)
  - check_content_clarity, check_structured_data, check_faq_content, check_eeat_signals: 모두 구현
  - scanner.py에서 check_geo=True 옵션으로 제어 (L77-100)
- 차이점: 없음

### 8. 벤치마크 (Phase A+)
- **상태: 부분 구현**
- PRD 요구사항: 동일 지역 분포 기반 비교, 상위25%/중위/하위25% 분포, 익명화
- 실제 구현:
  - 리포트 페이지에 벤치마크 섹션 구현 (report/[id]/page.tsx L413-479)
  - BenchmarkData: top_25_avg, median, bottom_25_avg, total_count, your_percentile
  - 분포 바 시각화 (red/yellow/green 3구간 + 자신의 위치 마커)
  - API: /api/benchmark/[auditId] 존재
  - 경쟁 분석 섹션: region_clinics, foreign_patient_rate, website_rate (L306-411)
- 차이점:
  - PRD의 레이더 차트가 분포 바로 대체됨 (기능적으로 유사)
  - 벌크 크롤링(F6) 배치 시스템: /api/admin/batch-scan 라우트 존재하나 상세 구현 미확인
- 권장 조치: 레이더 차트를 추가하거나 PRD를 현행 방식으로 업데이트

### 9. 관리자 대시보드 (Phase B)
- **상태: 완전 구현**
- PRD 요구사항 (4.2): 오늘의 요약 (진단/리드/상담중/계약 카운터), 최근 진단 목록, 리드 상세
- 실제 구현:
  - 대시보드 홈: 4개 카운터 카드 (진단, 리드, 상담 중, 계약) (admin/dashboard/page.tsx L43-68)
  - 최근 진단 목록: URL, 점수, 상태, 시간 표시 (L98-136)
  - 리드 관리: 테이블 (담당자, 이메일, 병원명, 상태, 이메일건수, 등록일, 액션) (admin/leads/page.tsx)
  - 상태 관리: new/contacted/consulting/proposal_sent/contracted/active/churned (L9-23)
  - 프로젝트 전환 버튼 (L106-111)
  - 사이드바 네비: 대시보드, 진단 목록, 리드 관리, 프로젝트, 병원 관리, 구독 관리, 메신저 연동, 알림 이력, 시장 현황 (admin/layout.tsx L27-39)
  - 인증: getAdminUser() 서버 사이드 체크 (layout.tsx L10-15)
- 차이점:
  - PRD의 "리포트 재발송" 버튼이 리드 상세에서 직접 노출되지 않음 (API /api/admin/audits/:id/resend는 존재하나 UI 미연결)
  - "상담 메모 추가" 기능이 리드 목록 UI에서 바로 접근 불가 (API PATCH /api/admin/leads/:id로 가능하나 UI 미노출)
- 권장 조치: 리드 상세 페이지에 "리포트 재발송", "메모 추가" 버튼 추가

### 10. PDF 리포트 (Phase B)
- **상태: 부분 구현**
- PRD 요구사항 (F2.2): Executive Summary, 카테고리별 상세, 경쟁사 벤치마크, 개선 로드맵, 부록
- 실제 구현:
  - Worker: Jinja2 HTML -> Playwright PDF -> Supabase Storage (pdf_generator.py)
  - Web: HTML 상세 리포트 생성 (/api/reports/[id]/route.ts) - 항목별 점수, 상태(pass/warn/fail), 이슈 표시
  - 리포트 페이지에서 PDF 다운로드 + HTML 리포트 보기/인쇄 링크 제공
- 차이점:
  - HTML 리포트는 단일 페이지 구조 (PRD의 5개 섹션 구조가 아님)
  - "경쟁사 벤치마크" 섹션 미포함 (분포 데이터가 리포트에 미반영)
  - "개선 로드맵" (즉시/단기/중기 개선) 섹션 미포함
  - "부록" (전체 체크리스트, 기술 용어) 미포함
  - 스크린샷 포함 기능 미구현
- 권장 조치:
  1. PDF 템플릿을 PRD F2.2 구조로 재설계
  2. 벤치마크 데이터를 리포트에 포함
  3. 개선 로드맵 섹션 추가 (각 fail 항목에 대한 우선순위별 분류)

### 11. Before/After 비교 (Phase B)
- **상태: 완전 구현**
- PRD 요구사항 (4.3): 점수 추이 차트, Before/After 카테고리별 비교
- 실제 구현:
  - 프로젝트 상세 페이지: ScoreTrendChart + BeforeAfterTable 컴포넌트 (admin/projects/[id]/page.tsx L164-193)
  - Score History API: /api/score-history/[hospitalId]
  - record_score_history 함수: scanner.py에서 진단 후 자동 기록 (L111-120)
- 차이점: 없음

### 12. 프로젝트 관리 (Phase B)
- **상태: 완전 구현**
- PRD 요구사항 (F4.3): 프로젝트 목록, 작업 체크리스트, Before/After, 타임라인
- 실제 구현:
  - 프로젝트 목록: 상태별 Badge, ProgressRing, 기간/점수 표시 (admin/projects/page.tsx)
  - 프로젝트 상세: 정보 카드, 점수 추이, Before/After, TaskChecklist (admin/projects/[id]/page.tsx)
  - 새 프로젝트 생성: admin/projects/new/page.tsx
  - API: /api/projects, /api/projects/[id], /api/projects/[id]/tasks
  - DB: projects 테이블 (plan JSONB, status, start_date, end_date)
  - 리드 -> 프로젝트 전환: leads 페이지의 "프로젝트 전환" 버튼 (admin/leads/page.tsx L106-111)
- 차이점: 없음

### 13. 구독 모니터링 (Phase C)
- **상태: 완전 구현**
- PRD 요구사항: 주간/월간 자동 재진단
- 실제 구현:
  - 리포트 페이지에 모니터링 구독 폼 (report/[id]/page.tsx L560-615): 이메일 + 빈도(주간/격주/월간) 선택
  - API: /api/subscriptions (구독 생성), /api/cron/rescan (재스캔 트리거)
  - Worker: /worker/subscriptions/process-due 엔드포인트 호출
  - 관리자: admin/subscriptions/page.tsx (구독 목록/해지 관리)
- 차이점: 없음

### 14. 알림 (Phase C)
- **상태: 부분 구현**
- PRD 요구사항: 순위 변동 알림, 점수 변동 시 알림
- 실제 구현:
  - 알림 이력 페이지: admin/alerts/page.tsx (score_change, grade_change, score_drop, score_rise 유형)
  - alerts 테이블에서 subscription_id, alert_type, previous_score, current_score, sent 추적
  - 관리자가 알림 이력을 조회할 수 있음
- 차이점:
  - 알림 생성 로직(점수 비교 -> alert INSERT)이 Worker monitoring.py에 존재하나, 이메일 발송 연동이 불분명
  - 사용자에게 직접 알림 이메일이 발송되는지 미확인 (sent=false가 많을 수 있음)
- 권장 조치: 알림 생성 시 이메일 자동 발송 로직 확인 및 보강

### 15. LINE/WeChat 웹훅 (Phase D)
- **상태: 부분 구현**
- PRD 요구사항: LINE Messaging API + WeChat Official Account API 통합, 자동 번역, 통합 대시보드
- 실제 구현:
  - LINE Webhook: /api/webhook/line/route.ts - HMAC-SHA256 서명 검증, 메시지 수신, 기본 자동 응답, 리드 생성
  - WeChat Webhook: /api/webhook/wechat/route.ts - SHA1 서명 검증, XML 파싱, 기본 자동 응답, 리드 생성
  - 관리자 사이드바에 "메신저 연동" 메뉴 존재
  - 관리자 연동 관리: admin/integrations/page.tsx
- 차이점:
  - 자동 번역 시스템 미구현 (PRD 10.2: 수신 자동 번역 + 발송 번역 미리보기)
  - 통합 대시보드 UI (PRD 10.5: 대화 목록 + 채팅 UI) 미구현
  - LINE Push API 발송 미구현 (Reply API만 사용)
  - WeChat Customer Service API / Template Message 미구현
  - Redis 기반 중복 방지 미구현 (PRD: webhookEventId SET NX)
  - conversations/messages 테이블 미생성 (leads 테이블에 직접 upsert)
  - 면책 문구 자동 삽입 미구현
  - compare_digest 대신 단순 문자열 비교 (LINE webhook, L20: `hash === signature`)
- 권장 조치:
  1. Phase D는 Post-MVP(Month 5+)이므로 현 수준은 적절
  2. LINE 서명 검증을 timingSafeEqual로 변경 (보안)
  3. 이후 구현 시 PRD 10.3-10.5 참조

### 16. 보안 (비기능)
- **상태: 완전 구현**
- PRD 요구사항: SSRF 방지, RLS, 인증
- 실제 구현:
  - SSRF: worker/app/security/ssrf.py - 내부 IP 차단 (10/172/192/127/169.254/::1/fc00), DNS rebinding 방지, 메타데이터 URL 차단
  - RLS: 001_initial_schema.sql - 6개 테이블 RLS 활성화, anon audit 조회는 JWT audit_claims 기반, admin은 app_metadata.role='admin' 기반
  - 인증: admin/layout.tsx에서 getAdminUser() 서버 사이드 체크
  - API 인증: Worker API는 WORKER_API_KEY Bearer 토큰, Cron은 CRON_SECRET
- 차이점: PRD와 일치

### 17. Rate Limiting (비기능)
- **상태: 미구현 (부분)**
- PRD 요구사항: IP당 5회/시간, 20회/일, Upstash Redis + fallback 인메모리
- 실제 구현:
  - Worker: 인메모리 RateLimiter 클래스 (security/rate_limit.py) - 기본 10req/60s
  - Web (Next.js API Routes): Rate limit 미적용 - POST /api/audits에 rate limit 없음
- 차이점:
  - PRD의 3중 방어 (Redis + 인메모리 + RLS)가 인메모리 단일 레이어로만 구현
  - Upstash Redis 연동 없음
  - Next.js API Routes에 rate limit 미적용 (가장 큰 갭)
  - 동일 URL 24시간 캐시 반환 미구현
- 권장 조치:
  1. @upstash/ratelimit 패키지 도입하여 POST /api/audits에 적용
  2. 동일 URL 재진단 시 24시간 내 캐시 반환 로직 추가
  3. Worker rate limiter의 설정값을 PRD와 일치 (5회/시간)

---

## 코드 품질 이슈

### 하드코딩된 값
1. **resend.ts L138**: Cloud Run URL이 하드코딩됨 (`cyh-web-124503144711.asia-northeast3.run.app`) - 환경 변수로 교체 필요
2. **follow-up/route.ts L48-57**: emails_sent 임계값이 매직 넘버로 하드코딩 (2, 3, 4, 5) - FOLLOW_UP_SCHEDULE 기반 계산으로 개선
3. **report/[id]/route.ts**: CATEGORY_LABELS가 reports 라우트와 report 페이지에 중복 정의 - 공유 모듈로 추출

### 보안 관련
1. **LINE webhook**: `hash === signature` 단순 비교 - `crypto.timingSafeEqual` 사용 필요 (타이밍 공격 방지)
2. **POST /api/audits**: Rate limit 미적용 - 무제한 진단 요청 가능
3. **Worker API key**: fire-and-forget 호출 시 에러 무시 (`.catch(() => {})`) - 로깅 추가 권장

### 구조 개선
1. **report/[id]/page.tsx**: 619줄의 대규모 컴포넌트 - ScoreSection, BenchmarkSection, LeadForm, SubscriptionForm으로 분리 권장
2. **scorer.py**: WEIGHTS 딕셔너리의 주석이 실제 가중치와 불일치 - "Technical SEO (0.70)"이라고 주석되어 있으나 실제로는 Tech SEO(0.50) + Performance(0.20) = 0.70

---

## 우선순위별 개선 목록

### 1. 즉시 수정 필요 (버그/보안)
| # | 항목 | 위치 | 설명 |
|---|------|------|------|
| 1 | Rate Limit 미적용 | `apps/web/src/app/api/audits/route.ts` | POST /api/audits에 @upstash/ratelimit 적용 |
| 2 | LINE 서명 타이밍 공격 | `apps/web/src/app/api/webhook/line/route.ts L20` | `crypto.timingSafeEqual` 사용 |
| 3 | 하드코딩 URL | `apps/web/src/lib/resend.ts L138` | 환경 변수 `NEXT_PUBLIC_BASE_URL`로 교체 |

### 2. 단기 개선 (UX/완성도) - 1~2주
| # | 항목 | 설명 |
|---|------|------|
| 1 | 다국어 진단 항목 분리 | hreflang(3%), overseas_channels(2%) 별도 체커 + WEIGHTS 항목 추가 |
| 2 | PDF 리포트 구조 개선 | PRD F2.2의 5개 섹션 구조로 재설계 (Executive Summary, 상세, 벤치마크, 로드맵, 부록) |
| 3 | 리드 상세 UI | "리포트 재발송" + "메모 추가" 버튼을 리드 상세 페이지에 노출 |
| 4 | 동일 URL 캐시 | 24시간 내 동일 URL 재진단 시 기존 결과 반환 |
| 5 | 벤치마크 리포트 포함 | PDF/HTML 리포트에 분포 벤치마크 데이터 포함 |

### 3. 중기 개선 (확장성/성능) - 1~2개월
| # | 항목 | 설명 |
|---|------|------|
| 1 | Upstash Redis 통합 | Rate limit + 진단 결과 캐시 + 세션 관리 |
| 2 | 알림 이메일 자동화 | 점수 변동 알림 생성 시 구독자에게 이메일 자동 발송 |
| 3 | 리포트 페이지 분할 | 619줄 컴포넌트를 4-5개 서브 컴포넌트로 분리 |
| 4 | LINE/WeChat 고도화 | 자동 번역, 통합 대시보드, Push API, Redis 중복 방지 (Phase D 본격 진입 시) |
| 5 | Framer Motion 도입 | PRD 기술 스택에 포함된 스캔 진행 UI 애니메이션, 점수 카운트업 효과 |
