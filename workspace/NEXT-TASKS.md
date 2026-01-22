# 다음 작업 목록

> 작성일: 2026-01-16
> 작성자: Alfred
> 브랜치: `feature/planning-agent`

---

## 📊 현재 상태 요약

### 완료된 작업 (2026-01-16)

| 작업 | 상태 | 비고 |
|------|------|------|
| 멀티-LLM 리뷰 시스템 구축 | ✅ 완료 | Claude + Gemini 앙상블 |
| 3개 문서 컨센서스 리뷰 | ✅ 완료 | PRD, IA, UX Strategy |
| 리뷰 피드백 적용 (v1.1) | ✅ 완료 | P0 Critical 이슈 해결 |
| workspace 전체 Git 추가 | ✅ 완료 | 49개 파일 커밋 |

### 컨센서스 점수 현황

| 문서 | 점수 | P0 해결 | P1 해결 |
|------|------|---------|---------|
| PRD | 5.5/10 → 개선됨 | ✅ | ⚠️ 일부 |
| Information Architecture | 7.25/10 → 개선됨 | ✅ | ✅ |
| UX Strategy | 7.0/10 → 개선됨 | ✅ | ✅ |

---

## 🎯 내일 작업 (우선순위순)

### P0: 즉시 필요 (개발 착수 전 필수)

#### 1. PRD 재검토 요청
```bash
# 수정된 PRD를 다시 멀티-LLM 리뷰하여 점수 개선 확인
# 목표: 7.0/10 이상
```

**체크리스트**:
- [ ] 비즈니스 메트릭 정합성 재확인
- [ ] MVP 8주 일정 세부 검토
- [ ] 인수 조건 완성도 확인

#### 2. 사용자 여정(User Journey) 정의
- **위치**: `testcraft/04-specification/` 또는 `06-design/`
- **내용**: Primary 페르소나(QA 엔지니어)의 일주일 시나리오
- **예시**:
  ```
  Day 1: 신규 기획서 수령 → TestCraft 로그인 → PDF 업로드
  Day 2: 생성된 TC 검토 → 수정/보완
  Day 3: Excel Export → 테스트 실행
  ```

#### 3. 핵심 기술 POC 계획서 작성
- **목적**: PDF 파싱 + AI TC 생성 품질 검증
- **예상 위치**: `testcraft/04-specification/poc-plan.md`
- **포함 내용**:
  - 테스트할 PDF 샘플 (3-5종)
  - 평가 기준 (정확도, 완성도, 엣지케이스 수)
  - 성공 기준 (80% 이상 유효 TC)

---

### P1: Sprint 0 (MVP 시작 전)

#### 4. 나머지 문서 멀티-LLM 리뷰
아직 리뷰하지 않은 문서들:
- [ ] `feature-spec.md` - 기능 명세
- [ ] `user-flow.md` - 사용자 흐름
- [ ] `wireframe-guide.md` - 와이어프레임
- [ ] `data-strategy.md` - 데이터 전략

#### 5. 용어 사전 정리
- **위치**: `testcraft/04-specification/glossary.md` (신규)
- **내용**:
  | 용어 | 정의 | 사용 컨텍스트 |
  |------|------|---------------|
  | TC | Test Case, 테스트케이스 | 전체 |
  | PRD | Product Requirements Document | 입력 문서 |
  | 엣지케이스 | 경계 조건 테스트 시나리오 | TC 유형 |

#### 6. 경쟁사 분석 보강
- **위치**: `testcraft/02-research/competitor-analysis.md`
- **추가 내용**:
  - 현재 경쟁 환경 (AI TC 생성 도구)
  - 차별화 포인트 정리
  - 위협 요소 분석

---

### P2: MVP 개발 중

#### 7. Should Have 기능 인수 조건 작성
- F-010 ~ F-017 기능에 Given-When-Then 형식 추가

#### 8. 반응형 전략 상세화
- `ux-strategy.md`에 디바이스별 세부 행동 정의 추가

#### 9. API 문서 초안
- 백엔드 개발 시작 전 API 명세 작성

---

## 🔄 Planning Agent 브랜치 상태

```
현재 브랜치: feature/planning-agent
원격 동기화: ✅ 완료 (origin/feature/planning-agent)

최근 커밋:
- 03968e5 feat(workspace): 프로젝트 기획 문서 전체 추가
- 5ff4752 docs(testcraft): 멀티-LLM 리뷰 피드백 반영 (v1.0 → v1.1)
- 90148e0 feat(reviews): 멀티-LLM 컨센서스 리포트 3종 추가
```

### PR 생성 고려
- `feature/planning-agent` → `master` PR 생성 검토
- 포함 내용: Planning Agent 정의, 37개 스킬, 멀티-LLM 리뷰 시스템

---

## 📁 주요 파일 위치

```
workspace/work-plan/testcraft/
├── 01-discovery/          # 아이디어, 타겟 사용자, 가치 제안
├── 02-research/           # 시장/경쟁사/사용자 조사
├── 03-validation/         # 비즈니스 모델, MVP 정의, 가격
├── 04-specification/      # PRD, IA, 기능명세, 사용자흐름 ⭐
├── 05-estimation/         # 공수, 기술스택, 팀구성
├── 06-design/             # UX 전략, 브랜드 ⭐
├── 07-execution/          # 로드맵, KPI, 리스크
├── 08-launch/             # GTM, 성장전략
└── _synthesis/            # 각 단계별 종합 문서

.moai/reports/reviews/
├── consensus-prd.md                    # PRD 컨센서스 (5.5/10)
├── consensus-information-architecture.md # IA 컨센서스 (7.25/10)
└── consensus-ux-strategy.md            # UX 컨센서스 (7.0/10)
```

---

## 💡 권장 시작 순서 (내일 아침)

```
1. [5분] 이 문서 읽고 컨텍스트 파악
2. [30분] PRD 재검토 리뷰 실행
3. [1시간] 사용자 여정 문서 작성
4. [1시간] POC 계획서 작성
5. [30분] 용어 사전 초안 작성
```

예상 소요: **약 3시간**

---

## 🚀 빠른 시작 명령어

```bash
# 프로젝트 디렉토리로 이동
cd /Users/woogi/Development/claude-craft

# 브랜치 확인
git branch

# PRD 파일 열기
open workspace/work-plan/testcraft/04-specification/prd.md

# 컨센서스 리포트 확인
open .moai/reports/reviews/
```

---

*이 문서는 Alfred가 2026-01-16 세션 종료 시 자동 생성했습니다.*
