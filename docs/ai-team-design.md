# Claude-Craft 기반 AI Team 설계안 (v0.1)

## 목적
- claude-craft에 이미 존재하는 에이전트/스킬 자산을 조합해
  **실제 업무를 병렬 처리하는 AI 팀 운영체계**를 만든다.
- 목표: 기획 → 개발 → 검수 → 배포/홍보까지 리드타임 단축.

---

## 1) 팀 구조 (권장 6인)

## A. Orchestrator (팀 리더)
- 후보: `moai/manager-project.md`, `moai/manager-strategy.md`
- 책임:
  - 업무 분해 (task decomposition)
  - 담당 에이전트 할당
  - 최종 산출물 통합/우선순위 결정
- 입출력:
  - 입력: 사용자 목표/제약/마감
  - 출력: 실행 플랜, 담당자별 작업 지시

## B. PM/Spec
- 후보: `🎯 기획/planning-agent/planning-agent-unified.md`, `moai/manager-spec.md`
- 책임:
  - 요구사항 명세(PRD, feature spec)
  - KPI/검증 기준 정의
  - 범위 통제(MVP 우선순위)
- 출력:
  - PRD, 사용자 시나리오, acceptance criteria

## C. Frontend Engineer
- 후보: `💻 개발/nextjs-expert-agent.md`
- 보조 스킬: `nextjs-expert-agent-skills/*`, `moai-library-shadcn`
- 책임:
  - 랜딩/웹 UI 구현
  - 접근성/반응형/성능 개선
- 출력:
  - 컴포넌트, 페이지, UI 테스트 결과

## D. Backend Engineer
- 후보: `💻 개발/fastapi-expert-agent.md`
- 보조 스킬: `fastapi-expert-agent-skills/*`
- 책임:
  - API/DB/인증/작업 큐 구현
  - 관측성/보안/테스트 셋업
- 출력:
  - API 스펙, 마이그레이션, 테스트 리포트

## E. Growth & Content
- 후보: `📣 마케팅/marketing-agent/marketing-agent-unified.md`, `📣 마케팅/seo-orchestrator-agent.md`, `📝 콘텐츠/social-media-agent.md`, `📝 콘텐츠/tech-blog-agent.md`
- 책임:
  - 콘텐츠 캘린더(예: 100일 플랜)
  - 채널별 카피 변환(랜딩/X/블로그)
  - 퍼널 실험(A/B 테스트)
- 출력:
  - 카피 자산, 발행 일정, KPI 대시보드 초안

## F. Reviewer (QA + Security + Content)
- 후보: `🔍 리뷰/review-code.md`, `review-architecture.md`, `review-security.md`, `review-content.md`
- 책임:
  - 코드/문서 품질 게이트
  - 정책/보안/논리성 검증
  - 릴리즈 승인/보류 판단
- 출력:
  - 리뷰 리포트(critical/major/minor), 수정 요청 목록

---

## 2) 운영 방식 (핸드오프 규칙)

1. **Orchestrator가 티켓 생성**
   - 티켓 ID, 목표, 마감, 의사결정 포인트 포함
2. **PM/Spec이 명세 고정**
   - 범위/완료조건 확정 전 개발 착수 금지
3. **FE/BE 병렬 구현**
   - 인터페이스 계약(API schema) 먼저 합의
4. **Growth 팀이 병행 준비**
   - 릴리즈 카피/랜딩/채널 플랜 사전 제작
5. **Reviewer 게이트 통과 후 merge**
   - Critical 0개가 기본 조건
6. **Orchestrator가 최종 요약/다음 액션 확정**

---

## 3) RACI 요약

| 업무 | Orchestrator | PM/Spec | FE | BE | Growth | Reviewer |
|---|---|---|---|---|---|---|
| 요구사항 정의 | A | R | C | C | C | C |
| UI 구현 | C | C | R | C | C | C |
| API/DB 구현 | C | C | C | R | C | C |
| 마케팅 카피/캘린더 | C | C | C | C | R | C |
| 품질/보안 검수 | C | C | C | C | C | R |
| 최종 출시 승인 | A | C | C | C | C | R |

(A: Accountable, R: Responsible, C: Consulted)

---

## 4) 스프린트 템플릿 (주간)

- 월: 목표 확정 + 티켓 분배
- 화~수: 구현/콘텐츠 병렬 생산
- 목: 리뷰/수정
- 금: 통합/배포/회고

산출물 기본 세트:
- `/docs/specs/*` (명세)
- `/docs/reviews/*` (리뷰 리포트)
- `/docs/growth/*` (카피/캘린더)
- 코드 PR + 릴리즈 노트

---

## 5) 초기 도입 순서 (2주)

### Week 1 (핵심 3인)
- Orchestrator + PM/Spec + FE/BE(겸)
- 목표: 명세 기반 개발 루프 정착

### Week 2 (확장 6인)
- Growth, Reviewer 추가
- 목표: 품질 게이트 + 콘텐츠 동시 운영

---

## 6) 리스크 및 대응

- 리스크: 역할 중복으로 책임 불명확
  - 대응: 티켓마다 단일 Owner 지정
- 리스크: 컨텍스트 과부하로 품질 저하
  - 대응: 에이전트별 입력 포맷 템플릿화
- 리스크: 리뷰 병목
  - 대응: Critical 우선 리뷰 규칙 적용

---

## 7) 성공 지표

- 기획→배포 리드타임 30% 단축
- 리뷰에서 Critical 발견률 감소(초기 대비)
- 콘텐츠 발행 준수율 90%+
- 릴리즈 후 회귀 이슈 감소

---

## 8) 다음 액션

1. 실제 프로젝트 기준으로 6개 역할에 담당 에이전트 매핑 확정
2. 티켓 템플릿(입력/출력 형식) 문서화
3. 주간 운영 리듬(월~금) 파일로 고정
4. 첫 스프린트 파일럿 실행 후 회고
