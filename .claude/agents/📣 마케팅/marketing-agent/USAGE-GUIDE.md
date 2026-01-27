# Marketing Agent 사용 가이드

## Phase 비교표

| Phase | 목적 | Skills | 산출물 | 소요 시간 |
|-------|------|--------|--------|----------|
| **Phase 0** | Context Intake | context-intake | 브랜드/제품 컨텍스트 문서 | 5-10분 |
| **Phase 1** | 전략 수립 | research, persona, positioning, strategy | 3C 분석, 페르소나 3종, STP 전략, 마케팅 로드맵 | 20-30분 |
| **Phase 2** | 캠페인 기획 | campaign, funnel, journey | SMART 목표, AARRR 퍼널, 고객 여정 맵 | 15-20분 |
| **Phase 3** | 콘텐츠 제작 | copy, landing, email, ads | 헤드라인 10개+, LP 카피, 이메일 시퀀스 5-7통, 광고 카피 | 30-40분 |
| **Phase 4** | 최적화 & 분석 | ab-testing, analytics, review | A/B 테스트 설계, KPI 대시보드, 최종 리뷰 | 15-20분 |

## 사용 시나리오

### 시나리오 1: SaaS 제품 런칭 (Full Process)

```
사용자: "개발자용 API 모니터링 툴 마케팅해줘. 월 $29, 경쟁사는 Datadog. 초기 100명 모으고 싶어."

실행 흐름:
Phase 0 → Context: 제품 특성, 기술 스택, 타겟 개발자 유형 수집
Phase 1 → Research: Datadog 가격/기능 비교
         Persona: "스타트업 백엔드 개발자", "DevOps 엔지니어"
         Positioning: "Datadog의 10% 가격으로 핵심 기능만"
         Strategy: Product Hunt + 개발자 커뮤니티 전략
Phase 2 → Campaign: 런칭 캠페인 기획
         Funnel: 무료체험 → 유료전환 퍼널
Phase 3 → Copy: 헤드라인 10개, 가치 제안
         Landing: 전체 LP 카피 + 구조
         Email: 온보딩 시퀀스 5통
         Ads: Google Ads 키워드 + 광고문구
Phase 4 → A/B Test: "무료체험 vs 데모신청" 테스트 설계
         Analytics: 핵심 KPI 정의
         Review: 전체 검토
```

### 시나리오 2: 이커머스 전환율 개선 (Partial)

```
사용자: "친환경 텀블러 판매. 3만원대. 장바구니 이탈률 70% 개선하고 싶어."

실행 흐름:
Phase 0 → Context: 제품 특성, 현재 이탈 지점, 고객 피드백
Phase 1 → Research: 이커머스 이탈 원인 분석 (일부만)
Phase 2 → Funnel: 이탈 지점 진단, 개선 우선순위
Phase 3 → Copy: 긴급성 유발 문구, 신뢰 요소
         Email: 장바구니 리마인더 시퀀스 3통
         Ads: 리타게팅 광고 카피
Phase 4 → A/B Test: "무료배송 vs 10% 할인" 테스트
         Analytics: 전환율 추적 KPI
```

### 시나리오 3: B2B 리드 생성

```
사용자: "HR 솔루션 회사. 100인 이상 기업 인사팀장 타겟. 데모 신청 늘리고 싶어."

실행 흐름:
Phase 0 → Context: 솔루션 특성, 현재 리드 소스, ICP
Phase 1 → Persona: "과로하는 인사팀장 김부장"
         Positioning: 경쟁사 대비 차별점
Phase 2 → Campaign: 리드마그넷 + 너처링 전략
         Journey: 콘텐츠 다운로드 → 데모 신청 여정
Phase 3 → Landing: 리드마그넷용 LP + 데모 LP
         Email: 리드 너처링 시퀀스 7통
         Ads: LinkedIn 광고 카피
Phase 4 → Analytics: CPL, 데모 전환율 KPI
```

### 시나리오 4: 특정 단계만 실행

```
사용자: "광고 카피만 10개 뽑아줘"

실행 흐름:
Phase 0 → Context: 제품/타겟 빠르게 확인
Phase 3 → Copy: AIDA/PAS 기반 카피 10개 (프레임워크별 분류 제공)
```

## 명령어 가이드

### 전체 프로세스 실행
```
"[제품]에 대한 마케팅 전략 세워줘"
"[목표]를 위한 마케팅 캠페인 기획해줘"
"[제품] 런칭 마케팅 전체 해줘"
```

### 특정 Skill 호출
```
/mkt-context        # 컨텍스트 수집
/mkt-research       # 시장 리서치
/mkt-persona        # 페르소나 생성
/mkt-positioning    # 포지셔닝 전략
/mkt-strategy       # 마케팅 전략
/mkt-campaign       # 캠페인 기획
/mkt-funnel         # 퍼널 설계
/mkt-journey        # 고객 여정
/mkt-copy           # 카피라이팅
/mkt-landing        # 랜딩페이지
/mkt-email          # 이메일 시퀀스
/mkt-ads            # 광고 크리에이티브
/mkt-abtest         # A/B 테스트
/mkt-analytics      # KPI & 분석
/mkt-review         # 검토
```

### 파이프라인 제어
```
"전략까지만 해줘"           # Phase 0-1만 실행
"콘텐츠 제작부터 해줘"       # Phase 3부터 실행
"카피만 다시 뽑아줘"         # 특정 스킬 재실행
"피드백 반영해서 수정해줘"    # 피드백 루프
```

## 퀄리티 향상 전략

```
레벨 1: 기본 → Generic한 결과물
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"마케팅해줘"

레벨 2: 컨텍스트 추가 → 훨씬 나은 결과물
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context Intake 스킬로 브랜드/제품/타겟 정보 수집

레벨 3: 피드백 루프 → 시니어 마케터에 근접
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1차 결과 → "2번 방향이 좋아" → 2차 결과 → 최종
```

### 피드백 예시
- "이 중 3번이 가장 좋아. 이 방향으로 5개 더 만들어줘"
- "우리 타겟은 더 전문적인 톤을 선호해"
- "경쟁사 A보다는 B를 더 의식해서 써줘"
- "CTA를 더 긴급하게 바꿔줘"

## 산출물 구조

```
workspace/work-marketing/
└── {project-name}/
    ├── context/
    │   └── {project}-context.md
    ├── research/
    │   └── {project}-3c-analysis.md
    ├── personas/
    │   └── {project}-personas.md
    ├── strategy/
    │   ├── {project}-positioning.md
    │   ├── {project}-strategy.md
    │   └── {project}-prelaunch.md
    ├── copy/
    │   └── {project}-copy.md
    ├── landing-pages/
    │   └── {page-name}/
    │       ├── structure.md
    │       ├── copy.md
    │       └── cro-checklist.md
    ├── email-sequences/
    │   └── {sequence-name}.md
    ├── ads/
    │   ├── google-ads.md
    │   ├── meta-ads.md
    │   └── linkedin-ads.md
    ├── ab-tests/
    │   └── {test-name}.md
    └── reports/
        ├── kpi-dashboard.md
        └── review-report.md
```

## 문제 해결

| 문제 | 원인 | 해결 방법 |
|-----|------|----------|
| 결과물이 generic함 | 컨텍스트 부족 | Context Intake 충실히 |
| 브랜드 톤 안 맞음 | 톤 정보 없음 | 기존 카피 예시 제공 |
| 타겟 언어 어색 | 실제 고객 언어 부재 | 고객 리뷰/피드백 공유 |
| 창의성 부족 | AI 한계 | 방향 제시 후 변형 요청 |
| 데이터 부정확 | 실시간 데이터 없음 | 외부 리서치 보완 |

## 자동화 범위

### 에이전트가 하는 것 (자동화)
- 시장/경쟁사 리서치 & 분석
- 페르소나 생성
- 전략 문서 작성
- 모든 종류의 카피라이팅
- 이메일 시퀀스 설계 & 작성
- 랜딩페이지 구조 & 카피
- A/B 테스트 가설 & 설계
- KPI 정의 & 리포트 템플릿
- 광고 카피 (Google, Meta, LinkedIn)

### 사용자가 하는 것 (수동)
- 실제 광고 플랫폼에 광고 등록
- 이메일 툴에 시퀀스 세팅
- 랜딩페이지 실제 구현/코딩
- A/B 테스트 실행 & 결과 수집
- 예산 집행 결정
- 최종 승인 & 퍼블리시
