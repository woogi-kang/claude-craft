# PRD v2.0 — Gemini 기반 UI/UX 서베이 자가진화 분석 플랫폼

| 항목 | 내용 |
|------|------|
| **문서 버전** | 2.0 |
| **작성일** | 2026-05-18 |
| **상태** | Draft (검토 대기) |
| **전 버전 차이** | 실제 RAW DATA (2025 2분기 3,295건) 분석 기반 재작성 + Self-Evolving 루프 추가 |
| **데이터 출처** | `UI_UX 서베이 결과 정기 보고 (2분기_2025_4_5_6월).xlsx` |

---

## 0. 변경 이력 (v1 → v2)

| 항목 | v1 (기획안) | v2 (본 문서) |
|------|-------------|--------------|
| 데이터 스키마 | 미정의 | 8컬럼 확정 (CATEGORY/CHANNEL/CHOICE_ANSWER/SHORT_ANSWER 등) |
| Stage 분류 | 3개 (booking/check-in/ancillary) | **7개 enum** (CATEGORY 값 그대로) |
| AI 분석 흐름 | 1회성 분석 | **Self-Evolving 4단계 루프** |
| Quality Gate | 없음 | **3-Tier 게이트** (Regex/Context/AI) |
| 백로그 처리 | 없음 | **981건 매칭 + 중복 제거** |
| 검증 체계 | 없음 | **Gold Dataset 100건 + Drift Alert** |
| Batch 주기 | 매일 | **주간(권장) 또는 월간** |
| 다국어 | 미정 | **한/영 분리 처리** |

---

## 1. 개요

### 1.1 배경
- 2분기(2025.4~6) 기준 **3,295건의 UI/UX 서베이 응답**이 누적되었으나, 사람이 수동으로 읽고 정리하는 데 평균 **3주 소요**.
- 기존 분석 시트(`gemini`, `IBE_KWD`)는 1회성 키워드 추출 수준이며, **반복 학습/개선 메커니즘 없음**.
- 누적된 **개선 백로그 981건**과 신규 제안 간 중복 제거 프로세스가 없어 동일 이슈가 반복 제기됨.

### 1.2 비전
> **"매 배치마다 더 똑똑해지는 자가진화 UX 인사이트 시스템"**
>
> 노이즈가 섞인 정성 데이터에서 Gemini와 자체 회고 루프로 분류·우선순위·제안 품질을 지속 개선하고, 휴먼 의사결정자가 신뢰할 수 있는 단일 대시보드를 제공한다.

### 1.3 범위 (In / Out)

| In Scope | Out of Scope |
|----------|--------------|
| IBE Flow + CHECK-IN RAW 데이터 분석 | 부가서비스(Ancillary) 별도 RAW (현재 시트 없음) |
| 한국어/영어 응답 | 일본어/중국어 (Phase 2) |
| 관리자용 인사이트 대시보드 | 외부 공개 대시보드 |
| Self-Evolving 분석 루프 | 모델 파인튜닝 (LoRA, RLHF) |
| 기존 Backlog 매칭 | Jira/Notion 자동 티켓 생성 (Phase 2) |

---

## 2. 문제 정의 & 목표

### 2.1 문제 (As-is)

| 문제 | 영향 |
|------|------|
| 정성 데이터 수동 분석에 분기당 3주 소요 | 의사결정 지연 → 개선 사이클 둔화 |
| 트래시 응답(7~12%) 필터 없음 | 분석가가 잡음 속에서 신호 탐색 |
| 우선순위가 분석가 주관에 의존 | 일관성 부족, 인수인계 어려움 |
| 백로그(981건)와 신규 제안 중복 | 동일 이슈 반복 논의, 리소스 낭비 |
| AI 분석 품질을 측정/개선할 메커니즘 없음 | 시간이 지나도 정확도 정체 |

### 2.2 목표 (To-be)

| 목표 | 측정 지표 | 목표값 |
|------|----------|--------|
| 분석 시간 단축 | 수동 분석 시간 대비 | **90% ↓** |
| 분류 정확도 | Gold Set 100건 기준 macro-F1 | **0.80+** (3개월 내) |
| 백로그 중복 제거 | 신규 제안 중 백로그 매칭률 | **30%+ 매칭** |
| 트래시 필터링 정확도 | Quality Gate Precision/Recall | **P=0.95, R=0.90** |
| 의사결정 채택률 | AI 제안 → 실제 Backlog 등재율 | **40%+** |

---

## 3. 페르소나

| Persona | 역할 | Pain Point | 기대 |
|---------|------|-----------|------|
| **UX 기획자 P1 (주 사용자)** | 분기 보고서 작성, 우선순위 결정 | 1,000+ 응답을 매월 직접 읽음 | 우선순위 자동화, 핵심 인사이트 한눈에 |
| **개발 PM P2** | Backlog 관리, 일정 조율 | 중복 제안 검토에 시간 낭비 | 신규 vs 기존 매칭 자동화 |
| **C-level P3** | 분기 보고 받음 | 상세 데이터 못 봄 | Overview 한 화면, 트렌드 |
| **데이터 관리자 P4** | Gold Set 관리, 시스템 운영 | 모델 품질 측정 어려움 | 정확도/Drift 대시보드 |

---

## 4. 데이터 (실측 기반)

### 4.1 데이터 규모 (2025 2분기 기준)

| 분류 | 4월 | 5월 | 6월 | 월평균 |
|------|----|----|----|--------|
| IBE Flow | 858 | 990 | 882 | **910** |
| CHECK-IN | 168 | 215 | 182 | **188** |
| **합계** | 1,026 | 1,205 | 1,064 | **1,098** |

→ Batch 주기: **주간 (약 275건/주)** 권장

### 4.2 RAW 스키마 (확정)

```sql
CREATE TABLE survey_raw (
  id              BIGSERIAL PRIMARY KEY,
  source_sheet    TEXT NOT NULL,
  category        TEXT NOT NULL,
  channel         TEXT NOT NULL,
  office_id       TEXT,
  choice_answer   TEXT NOT NULL,
  short_answer    TEXT,
  member_hash     TEXT,
  created_at      TIMESTAMPTZ NOT NULL,
  ingested_at     TIMESTAMPTZ DEFAULT NOW(),
  language        TEXT,
  UNIQUE(source_sheet, category, choice_answer, short_answer, created_at)
);

CREATE INDEX idx_survey_raw_category ON survey_raw(category, created_at);
CREATE INDEX idx_survey_raw_channel  ON survey_raw(channel);
```

### 4.3 Stage Enum (CATEGORY 값 그대로)

```
IBE Flow:    SELECT-FLIGHT | PAYMENT | PASSENGER-INFO | ASR
CHECK-IN:    CHKIN-SEAT | CHKIN-INFO | CHKIN-PAX
```

### 4.4 데이터 품질 (실측)

| 지표 | 값 |
|------|----|
| 빈 응답 | 0.1~0.3% |
| 트래시(≤5자) | 7~12% |
| 평균 길이 | 30~38자 |
| 100자+ 상세 응답 | 약 5% |
| 회원 반복 응답 | 0% (2분기) |

**트래시 시드 패턴 (Quality Gate L1용)**:
```
"없음", "없어요", "없습니다", "없다", ".", "..", "ㅡ", "ㅇㅇ",
"감사합니다", "아니요", "네", "굿"
```

**컨텍스트 결합 시 유효한 짧은 응답 (L2 통과)**:
```
"매진", "가격", "오류", "멈춤", "회원번호", "이메일" + CHOICE_ANSWER 결합
```

---

## 5. 시스템 아키텍처

### 5.1 전체 흐름

```
┌─────────────────────────────────────────────────────────────┐
│  Data Source                                                  │
│   • Excel(주기 업로드) → S3/GCS                              │
│   • (Future) DB 직결                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ ETL (매일 자정 KST)
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  PostgreSQL (Source of Truth)                                 │
│   survey_raw / survey_analysis / calibration_notes /          │
│   gold_dataset / backlog / clusters                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ Weekly Batch (월요일 02:00 KST)
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  Analysis Pipeline (Python + Cloud Run Jobs)                  │
│  ┌────────┐  ┌─────────┐  ┌────────┐  ┌──────────┐         │
│  │Quality │→ │ Context │→ │ Gemini │→ │  Self-   │         │
│  │ Gate   │  │ Loader  │  │Analyze │  │Reflection│         │
│  └────────┘  └─────────┘  └────────┘  └──────────┘         │
│                                                                │
│  • Vertex AI Gemini 2.x (gemini-2.5-pro)                     │
│  • Function Calling (Tools)                                   │
│  • Guardrails (룰 기반)                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│  Dashboard (Next.js 15 + shadcn/ui + Recharts)               │
│   A: Overview | B: AI 심층 분석 | C: Action Plan |           │
│   D: 모델 품질 (P4 페르소나)                                  │
└─────────────────────────────────────────────────────────────┘
                       ↑
                       │ Slack Webhook (Drift Alert)
                       │ Email (주간 리포트)
```

### 5.2 기술 스택

| 영역 | 스택 | 비고 |
|------|------|------|
| AI | Vertex AI Gemini 2.5 Pro | Function Calling 필수 |
| ETL/배치 | Python 3.13 + Cloud Run Jobs | Cloud Scheduler 트리거 |
| DB | PostgreSQL 16 + pgvector | Backlog 임베딩용 |
| Backend | FastAPI | 대시보드 API |
| Frontend | Next.js 15 + shadcn/ui + Recharts | App Router |
| 알림 | Slack Webhook, SendGrid | Drift/Weekly Report |
| 모니터링 | Cloud Logging + Sentry | |

---

## 6. AI 분석 엔진 상세

### 6.1 4단계 Self-Evolving 루프

```
Step 1. Quality Gate        → 트래시 필터링 (3-Tier)
Step 2. Context Loader      → 직전 N배치 calibration 주입
Step 3. Gemini Analysis     → 분류 + 감성 + 제안
Step 4. Self-Reflection     → 다음 배치용 calibration 생성
```

### 6.2 분석 출력 스키마

```typescript
interface SurveyAnalysis {
  survey_id: string;
  batch_id: string;
  language: 'ko' | 'en';

  quality: {
    is_analyzable: boolean;
    trash_reason?: 'too_short' | 'no_meaning' | 'off_topic' | 'abusive' | null;
    gate_level: 'L1_regex' | 'L2_context' | 'L3_gemini';
  };

  classification: {
    stage: 'SELECT-FLIGHT' | 'PAYMENT' | 'PASSENGER-INFO' | 'ASR'
         | 'CHKIN-SEAT' | 'CHKIN-INFO' | 'CHKIN-PAX';
    sub_step: string;
    root_cause: 'system_error' | 'info_lack' | 'ui_complexity'
              | 'price_complaint' | 'other';
    cluster_id: string;
    cluster_label: string;
    confidence: number;
  };

  sentiment: {
    score: number;
    primary_emotion: 'frustration' | 'confusion' | 'disappointment'
                   | 'anger' | 'neutral' | 'satisfaction';
    intensity: 'low' | 'mid' | 'high';
    confidence: number;
  };

  ai_suggestion: {
    priority: 'P0' | 'P1' | 'P2' | 'P3';
    action: string;
    rationale: string;
    backlog_ref?: {
      backlog_id: string;
      similarity: number;
      suggested_action: 'priority_up' | 'merge' | 'reopen';
    };
    confidence: number;
  };

  meta: {
    analyzed_at: string;
    model_version: string;
    calibration_version: string;
    needs_human_review: boolean;
  };
}
```

### 6.3 Quality Gate (3-Tier)

```python
class QualityGate:
    TRASH_REGEX = re.compile(
        r'^\s*('
        r'없[음다]요?\.?|없습니다\.?|'
        r'[.ㅡㅇ]+|'
        r'감사합니다\.?|아니요\.?|네\.?|굿\.?'
        r')\s*$'
    )

    CONTEXT_VALID_TOKENS = {
        'SELECT-FLIGHT':  {'매진', '가격', '시간', '날짜'},
        'PAYMENT':        {'오류', '카드', '쿠폰', '결제', '에러'},
        'PASSENGER-INFO': {'회원번호', '이름', '생년월일', '여권'},
        'CHKIN-SEAT':     {'좌석', '창가', '통로'},
    }

    def check(self, row):
        text = (row.short_answer or '').strip()
        if not text or self.TRASH_REGEX.match(text):
            return QualityResult(False, 'too_short', 'L1_regex')
        if len(text) <= 5:
            valid = self.CONTEXT_VALID_TOKENS.get(row.category, set())
            if text in valid:
                return QualityResult(True, None, 'L2_context')
            return QualityResult(False, 'no_meaning', 'L2_context')
        if 6 <= len(text) <= 15:
            return self._gemini_gate(row)
        return QualityResult(True, None, 'L3_pass')
```

### 6.4 Tool 정의 (Function Calling)

| Tool | 호출 시점 | 응답 크기 |
|------|----------|----------|
| `get_calibration_notes(window=4)` | 배치 시작 1회 | ≤ 2KB |
| `get_gold_dataset_metrics()` | 배치 시작 1회 | ≤ 1KB |
| `get_recent_clusters(stage)` | stage당 1회 | ≤ 2KB |
| `search_existing_backlog(action, stage)` | 제안 생성 시마다 | ≤ 1KB |
| `get_seed_anchors()` | 첫 배치만 | ≤ 1KB |

→ **총 context 예산: 배치당 8KB 이내**

### 6.5 System Instruction (요약)

```text
당신은 항공 서비스 UI/UX 정성 피드백 분석가입니다.

[원칙]
1. CATEGORY와 CHOICE_ANSWER는 사용자가 직접 선택한 ground truth.
   stage/sub_step에 그대로 사용. 절대 재추론 금지.
2. SHORT_ANSWER만 분석 대상. root_cause, cluster, suggestion에 집중.
3. 모든 출력에 confidence(0~1) 필수. 추측 30%↑이면 0.5 이하.
4. calibration_notes의 deprecated_labels 사용 금지.
5. 제안 생성 전 search_existing_backlog 필수 호출. 중복 시 backlog_ref 사용.
6. JSON 외 텍스트 출력 금지.

[제약]
- PII (이름/전화/이메일) 출력 금지
- root_cause enum 5개 외 값 생성 금지
- 한 응답에 복수 이슈가 있으면 가장 강한 1건만 분류
```

### 6.6 Priority 산정 공식

```python
def assign_priority(survey, cluster_size_7d, has_backlog_dup, sentiment):
    if has_backlog_dup:
        return None
    revenue_critical = survey.stage in {'PAYMENT', 'SELECT-FLIGHT'}
    severe = (sentiment.intensity == 'high'
              and survey.root_cause == 'system_error')
    if severe and revenue_critical:                    return 'P0'
    if revenue_critical and cluster_size_7d >= 5:      return 'P1'
    if cluster_size_7d >= 5:                           return 'P2'
    if revenue_critical:                               return 'P2'
    return 'P3'
```

---

## 7. Self-Reflection 메커니즘

### 7.1 매 배치 종료 후 실행

```text
[입력]
- 이번 배치 결과 (N건)
- Gold Set 자체 평가 (accuracy, F1, MAE)
- 이전 4주 calibration_notes

[출력 (JSON)]
{
  "batch_id": "2026W20",
  "summary": "ui_complexity 라벨이 frustration 흡수 경향. 차주 분리 필요.",
  "metrics": { "gold_macro_f1": 0.78, "drift_score": 0.12 },
  "new_rules": [ ... ],
  "deprecated_labels": ["ui_slow"],
  "drift_warnings": [ ... ]
}
```

### 7.2 Hard Guardrails

```python
GUARDRAILS = {
    "max_new_rules_per_batch": 3,
    "calibration_window_weeks": 4,
    "calibration_ttl_weeks": 8,
    "min_confidence_for_action": 0.7,
    "human_review_sample_rate": 0.05,
    "human_review_low_conf_threshold": 0.6,
    "gold_set_size": 100,
    "drift_alert_threshold": 0.15,
    "max_gemini_calls_per_batch": 400,
}
```

---

## 8. 기능 요구사항 (FR)

| ID | 요구사항 | 우선순위 |
|----|---------|---------|
| FR-01 | RAW Excel → PostgreSQL 자동 적재 | P0 |
| FR-02 | PII 마스킹 (회원번호 SHA-256) | P0 |
| FR-03 | 3-Tier Quality Gate | P0 |
| FR-04 | Gemini 분석 (분류+감성+제안) | P0 |
| FR-05 | Backlog 임베딩 + Vector Search | P0 |
| FR-06 | Self-Reflection | P1 |
| FR-07 | Gold Dataset 자체 평가 | P1 |
| FR-08 | Drift Alert (Slack) | P1 |
| FR-09 | Human Review Queue UI | P1 |
| FR-10 | 4개 화면 대시보드 | P1 |
| FR-11 | PDF/Excel Export | P2 |
| FR-12 | 다국어 처리 (한/영 분리) | P2 |
| FR-13 | Backlog 자동 동기화 (Jira/Notion) | P3 |

## 9. 비기능 요구사항 (NFR)

| ID | 요구사항 | 측정값 |
|----|---------|--------|
| NFR-01 | 배치 처리 시간 | 300건 ≤ 30분 |
| NFR-02 | 대시보드 TTI | ≤ 2초 |
| NFR-03 | Gemini 호출 비용 | 월 ≤ $200 |
| NFR-04 | 배치 성공률 | ≥ 99% |
| NFR-05 | PII 보호 | 원본 회원번호 DB 저장 금지 |
| NFR-06 | 감사 로그 | Gemini I/O 7년 보관 |

---

## 10. 데이터 모델 (전체)

```sql
CREATE TABLE survey_analysis (
  survey_id            BIGINT PRIMARY KEY REFERENCES survey_raw(id),
  batch_id             TEXT NOT NULL,
  language             TEXT,
  is_analyzable        BOOLEAN NOT NULL,
  trash_reason         TEXT,
  gate_level           TEXT,
  stage                TEXT,
  sub_step             TEXT,
  root_cause           TEXT,
  cluster_id           TEXT,
  cluster_label        TEXT,
  classification_conf  REAL,
  sentiment_score      REAL,
  primary_emotion      TEXT,
  intensity            TEXT,
  sentiment_conf       REAL,
  priority             TEXT,
  action_text          TEXT,
  rationale            TEXT,
  backlog_ref_id       TEXT,
  backlog_similarity   REAL,
  suggestion_conf      REAL,
  needs_human_review   BOOLEAN,
  model_version        TEXT,
  calibration_version  TEXT,
  analyzed_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE clusters (
  cluster_id     TEXT PRIMARY KEY,
  stage          TEXT NOT NULL,
  label          TEXT NOT NULL,
  centroid       VECTOR(768),
  first_seen     TIMESTAMPTZ,
  last_seen      TIMESTAMPTZ,
  member_count   INT DEFAULT 0,
  status         TEXT DEFAULT 'active'
);

CREATE TABLE backlog (
  backlog_id     TEXT PRIMARY KEY,
  task           TEXT NOT NULL,
  stage          TEXT,
  status         TEXT,
  embedding      VECTOR(768),
  imported_at    TIMESTAMPTZ
);
CREATE INDEX idx_backlog_embedding ON backlog USING ivfflat (embedding);

CREATE TABLE calibration_notes (
  version           TEXT PRIMARY KEY,
  batch_id          TEXT NOT NULL,
  rules             JSONB,
  deprecated        JSONB,
  drift_warnings    JSONB,
  metrics           JSONB,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  expires_at        TIMESTAMPTZ
);

CREATE TABLE gold_dataset (
  id                  SERIAL PRIMARY KEY,
  short_answer        TEXT NOT NULL,
  category            TEXT NOT NULL,
  choice_answer       TEXT,
  language            TEXT,
  truth_root_cause    TEXT NOT NULL,
  truth_emotion       TEXT NOT NULL,
  truth_is_analyzable BOOLEAN NOT NULL,
  labeler             TEXT,
  labeled_at          TIMESTAMPTZ
);

CREATE TABLE review_queue (
  survey_id      BIGINT REFERENCES survey_raw(id),
  reason         TEXT,
  reviewer       TEXT,
  reviewed_at    TIMESTAMPTZ,
  decision       JSONB,
  PRIMARY KEY (survey_id)
);
```

---

## 11. 거버넌스 & 보안

| 영역 | 정책 |
|------|------|
| **PII** | 원본 회원번호 DB 저장 금지. SHA-256 해시만. 이름/전화/이메일 정규식 마스킹. |
| **개인정보 동의** | 나이/성별 페르소나 분석은 `consent_pii=true`만. |
| **AI 책임** | confidence<0.7 제안 자동 채택 금지. P0 제안은 휴먼 승인 필수. |
| **감사 로그** | Gemini I/O 7년 보관 (Cloud Logging) |
| **모델 버전** | model_version + calibration_version 기록 (재현 가능) |
| **Drift 대응** | 라벨 분포 ±15% 변동 시 Slack → 24시간 내 P4 검토 |

---

## 12. 마일스톤 & 로드맵

| Phase | 기간 | 산출물 |
|-------|------|--------|
| **Phase 0: 데이터 기반** | W1~W3 | PostgreSQL+ETL / PII 마스킹 / Gold 100건 라벨링 |
| **Phase 1: 분석 엔진 PoC** | W4~W6 | Quality Gate / Gemini 프롬프트+Tools / Backlog 임베딩 |
| **Phase 2: Self-Evolving 루프** | W7~W8 | Self-Reflection / Gold 자동 평가 / Guardrails |
| **Phase 3: 대시보드** | W9~W11 | 화면 A/B/C/D + Export |
| **Phase 4: 운영 준비** | W12~W13 | Drift Alert / Review Queue UI / Pilot |
| **Phase 5: GA** | W14 | 정식 운영 |

→ **총 14주 (약 3.5개월)**

---

## 13. 성공 기준 (KPI)

| KPI | 측정 시점 | 목표값 |
|-----|----------|--------|
| 분석 시간 단축률 | Phase 5 +1M | 90% ↓ |
| Gold Set Macro-F1 | Phase 5 +3M | 0.80+ |
| Trash Precision/Recall | Phase 2 종료 | P=0.95, R=0.90 |
| Backlog 매칭률 | Phase 5 +1M | 30%+ |
| AI 제안 채택률 | Phase 5 +3M | 40%+ |
| 사용자 NPS | Phase 5 +2M | +30 |
| 배치 성공률 | 상시 | 99%+ |

---

## 14. 리스크 & 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| Gemini 비용 폭증 | 운영비 부담 | 호출 상한 + L1/L2 사전 필터 |
| Feedback Drift | 라벨 표류 | Gold 100건 고정 + drift alert |
| Calibration 규칙 폭발 | context 비대화 | max_new_rules=3 + TTL 8주 |
| Gold Set 라벨러 편향 | 평가 왜곡 | 2명 라벨 + Cohen's κ ≥ 0.7 |
| Backlog 임베딩 품질 | 매칭 누락 | Top-5 recall 0.85+ 검증 |
| 영어 정확도 저하 | 다국어 누락 | Phase 2까지 한국어만 GA |
| 신규 CATEGORY | enum 깨짐 | unknown_category 폴백 + 알림 |

---

## 15. Open Questions

| # | 질문 | 옵션 | 권장 |
|---|------|------|------|
| Q1 | Batch 주기 | 주간 / 월간 | **주간** |
| Q2 | 데이터 소스 | Excel / DB | Phase 1: Excel → 5+: DB |
| Q3 | 페르소나 데이터 | 신규 수집 / 미사용 | Phase 2+ 신규 수집 |
| Q4 | 영어 응답 | Phase 1 / Phase 2+ | Phase 2+ |
| Q5 | Human Review 인력 | 전담 / 분담 | 분담 |
| Q6 | Slack 채널 | 신규 / 기존 | 신규 #ux-ai-alert |
| Q7 | Backlog 동기화 | 양방향 / 단방향 / 없음 | Phase 5+ 단방향 |

---

## 16. 참고 자료

- 이전 분석: `gemini` 시트 (calibration seed)
- 기존 백로그: `4. 개선 사항 Backlog ` (981건 임베딩 대상)
- 개선 계획 시트: `3.설문 분석 개선 계획`
- 키워드 추출: `IBE_KWD`, `CHKIN_KWD`
- v1 기획안: `[기획안] Gemini 기반 UI_UX 서베이 분석 (1).pdf`
- **대시보드 상세**: `260518-dashboard-design.md`
