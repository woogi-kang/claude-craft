# Finance Context

재무 운영을 위한 AI 에이전트 컨텍스트 문서입니다.

## 회사 정보

| 항목 | 값 |
|------|-----|
| 회사명 | Solo Unicorn Corp |
| 사업자번호 | 000-00-00000 |
| 결산월 | 12월 |
| 회계연도 | 1월 1일 ~ 12월 31일 |

## 핵심 에이전트

```
finance-orchestrator-agent
├── receipt-ocr-gemini     # Gemini CLI OCR (무료)
├── expense-classifier     # 비용 분류 (Claude)
├── tax-invoice-popbill    # 세금계산서 (팝빌 API)
├── financial-statement    # 재무제표 생성
├── budget-analyzer        # 예산 분석
├── cash-flow-tracker      # 현금흐름 추적
└── tax-calendar           # 세무 일정 관리
```

## 파일 구조

```
operations/finance/
├── receipts/              # 영수증 (이미지 + OCR JSON)
│   └── YYYY-MM/
├── invoices/              # 세금계산서
│   └── YYYY-MM/
│       ├── sales/         # 매출
│       └── purchase/      # 매입
├── statements/            # 재무제표
│   └── YYYY-MM/
├── ledger.json            # 원장
├── budget.json            # 예산
└── FINANCE.md             # 이 파일
```

## 주요 명령어

| 명령어 | 설명 |
|--------|------|
| `/financial-report [YYYY-MM]` | 월간 재무 리포트 생성 |
| `./scripts/smart-ai.sh ocr <image>` | 영수증 OCR (Gemini) |
| `./scripts/smart-ai.sh classify <json>` | 비용 분류 |

## 비용 분류 체계

| 카테고리 | 코드 | 예산 비율 | 키워드 |
|----------|------|----------|--------|
| 인건비 | LABOR | 48% | 급여, 4대보험, 외주비 |
| 서버/인프라 | INFRA | 18% | AWS, GCP, Firebase |
| 마케팅 | MARKETING | 24% | 광고, 프로모션 |
| 소프트웨어 | SOFTWARE | 6% | 구독, SaaS |
| 사무실/운영 | OFFICE | 3.6% | 임대료, 통신비 |
| 기타 | ETC | 0.4% | 예비비 |

## 멀티 LLM 전략

| 작업 | 모델 | 비용 |
|------|------|------|
| 영수증 OCR | Gemini CLI | 무료 (1,000건/일) |
| 복잡한 문서 | Claude Vision | API 과금 |
| 비용 분류 | Claude Haiku | 저비용 |
| 재무 분석 | Claude Sonnet | 중간 |
| 전략 조언 | Claude Opus | 고급 |

**월 비용 예상** (1,000건 기준):
- 외부 OCR 서비스: $50-500
- 멀티 LLM 방식: ~$5
- **절감률: 90-99%**

## 연동 서비스

| 서비스 | 용도 | API |
|--------|------|-----|
| 팝빌 | 세금계산서 | popbill.com |
| 홈택스 | 원천세 신고 | hometax.go.kr |
| flex | 급여/4대보험 | flex.team |

## 세무 일정 (월간)

- **10일**: 원천세 신고/납부
- **25일**: 부가세 신고 (분기별)

## 알림 설정

| 이벤트 | 채널 | 임계값 |
|--------|------|--------|
| 예산 경고 | Slack #finance | 80% |
| 예산 초과 | Slack #finance | 100% |
| 런웨이 경고 | Slack #finance | 6개월 |
| 세무 D-7 | Slack #finance | 7일 전 |

## Quick Actions

```bash
# 영수증 일괄 처리
./scripts/smart-ai.sh ocr-batch ./receipts/2026-01

# 월간 리포트 생성
claude "/financial-report 2026-01"

# 예산 확인
./scripts/smart-ai.sh finance 2026-01
```

---

Version: 1.0.0
Last Updated: 2026-01-27
