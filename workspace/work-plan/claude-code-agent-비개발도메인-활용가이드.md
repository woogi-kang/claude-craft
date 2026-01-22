# Claude Code Agent 비개발 도메인 활용 가이드

> 코딩을 넘어선 "범용 자동화 도구"로서의 Claude Code 활용법

---

## 핵심 통찰

> "Claude Code는 코딩 도구가 아니다. 컴퓨터로 타이핑해서 할 수 있는 모든 것을 자동화할 수 있는 **범용 에이전트**다."
> — Simon Willison

> "Claude Code는 지식 노동자다. 스프레드시트 정리, 상세한 리서치 리포트 작성, 기사 작성 등을 수행한다."
> — Transformer News

---

## 목차

1. [마케팅 & 광고](#1-마케팅--광고)
2. [법률 & 계약](#2-법률--계약)
3. [금융 & 회계](#3-금융--회계)
4. [연구 & 학술](#4-연구--학술)
5. [HR & 채용](#5-hr--채용)
6. [고객 서비스](#6-고객-서비스)
7. [부동산](#7-부동산)
8. [헬스케어](#8-헬스케어)
9. [교육](#9-교육)
10. [저널리즘 & 글쓰기](#10-저널리즘--글쓰기)
11. [세일즈 & CRM](#11-세일즈--crm)
12. [공급망 & 물류](#12-공급망--물류)
13. [팟캐스트 & 오디오](#13-팟캐스트--오디오)
14. [여행 계획](#14-여행-계획)
15. [프로젝트 관리](#15-프로젝트-관리)
16. [개인 비서 & 라이프 자동화](#16-개인-비서--라이프-자동화)
17. [데이터 시각화 & 리포팅](#17-데이터-시각화--리포팅)
18. [이메일 관리](#18-이메일-관리)
19. [소셜 미디어 관리](#19-소셜-미디어-관리)
20. [이커머스](#20-이커머스)

---

## 1. 마케팅 & 광고

### 실제 사례: Advolve

**출처**: [Advolve automates digital marketing with Claude](https://www.claude.com/customers/advolve)

Advolve는 Claude를 AI 플랫폼의 중앙 오케스트레이터로 사용하여 수백만 달러 광고 예산을 자동 관리합니다.

**워크플로우:**
1. 정적 크리에이티브 에셋 생성
2. 카피라이팅
3. 각 에셋 레이어(배경, 아트, 폰트, 카피) 평가
4. 과거 성공 광고 데이터 기반 최적화

### 광고 카피 자동 생성

**출처**: [Anthropic - How teams use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)

```
CSV 파일 (기존 광고 + 성과 지표)
    ↓
저성과 광고 식별
    ↓
두 개의 서브에이전트:
  - 헤드라인 에이전트 (30자 제한)
  - 설명 에이전트 (90자 제한)
    ↓
수백 개 새 변형 생성 (수 분 내)
```

**결과**: 수 시간 → 수 분

### 콘텐츠 마케팅 자동화

**출처**: [Claude Code for Content Marketers](https://www.animalz.co/blog/claude-code)

| 도구 | 기능 |
|------|------|
| 인터랙티브 프레젠테이션 생성기 | 프레젠테이션 자동 생성 |
| 인터뷰 트랜스크립트 분석기 | ICP 기반 테마 추출 |
| 콘텐츠 라이브러리 감사자 | 블로그 분석 |
| 스타일 가이드 생성기 | 15+ 기사 분석 → 편집 가이드 |

### 성과 지표

- **시간 절약**: 75% (8시간 → 2시간)
- **비용 절감**: 70%
- **월 절감액**: 클라이언트당 $150

---

## 2. 법률 & 계약

### 실제 사례: Harvey AI

**출처**: [Harvey transforms legal work with Claude](https://www.claude.com/customers/harvey)

Harvey는 법률 사무소와 Fortune 500 기업의 계약 분석, 실사, 소송을 Claude 기반으로 혁신합니다.

### Anthropic 법무팀 활용 사례

**출처**: [How Anthropic uses Claude in Legal](https://claude.com/blog/how-anthropic-uses-claude-legal)

- **마케팅 콘텐츠 검토**: 코딩 없이 자동화
- **계약서 레드라이닝**: Google Docs/Office 365 통합
- **실시간 편집 제안**: Google Docs 내 코멘트로 표시

### 계약 검토 성과

| 지표 | Before | After |
|------|--------|-------|
| 계약당 검토 시간 | 4시간 | 55분 |
| 월간 처리량 | 기준 | +300% |
| 턴어라운드 | 2-3일 | 24시간 |

### 주요 기능

- 위험 조항 플래그
- 긴 계약서 요약
- 버전 간 불일치 탐지
- 메타데이터 추출 (당사자, 날짜, 조건)

### 주의사항

> "AI 도구는 변호사 전문성을 **보완**하는 것이지 **대체**하는 것이 아닙니다. 모든 출력은 자격 있는 변호사가 검토해야 합니다."

---

## 3. 금융 & 회계

### Claude 금융 서비스 진출

**출처**: [Advancing Claude for Financial Services](https://www.anthropic.com/news/advancing-claude-for-financial-services)

**금융 전용 Skills:**
- 유사 기업 분석 (밸류에이션 멀티플)
- DCF 모델 (예측 + 민감도 테이블)
- 실사 데이터 팩
- 기업 프로필/티저
- 실적 분석
- 커버리지 개시 보고서

### Excel 통합

**출처**: [Claude for Excel](https://claude.com/claude-in-excel)

- Excel 사이드바에서 직접 Claude 작업
- 워크북 읽기/분석/수정/생성
- 자동 헤더 감지 & 데이터 프로파일링
- 50MB (Pro) / 1GB (Enterprise) 파일 지원

### 실제 활용 사례

**$50k 부동산 리노베이션 분석:**
- 완전한 임대 부동산 분석
- 3개 시나리오 예측
- 5년 현금흐름 모델링
- 다중 기간 ROI 계산
- 핵심 변수 민감도 분석

### 벤치마크 성과

**Financial Modeling World Cup:**
- Claude Opus 4: 7개 레벨 중 5개 통과
- 복잡한 Excel 작업 83% 정확도

---

## 4. 연구 & 학술

### 문헌 리뷰 자동화

**출처**: [Claude for Researchers](https://claude-ai.chat/use-cases/researchers/)

**기능:**
- 복잡한 논문 요약
- 연구 간 결과 비교
- 인용 추출 및 교차 참조
- 구조화된 연구 노트 생성

### 실험 사례

한 연구자가 PDF 파일들을 Claude에 업로드하여 문헌 리뷰 합성:
- **소요 시간**: 5개 채팅, 1일
- **결과**: 일관된 문헌 리뷰 섹션 완성

### claude-scientific-writer

**출처**: [GitHub - claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer)

**생성 가능 문서:**
- 출판 준비 과학 논문
- 보고서
- 포스터
- 연구비 제안서
- 문헌 리뷰

**특징:**
- 실시간 문헌 검색
- 검증된 인용
- PubMed, arXiv, bioRxiv, Semantic Scholar 통합

### 워크플로우 팁

```
Zotero/Obsidian + Claude API 통합
    ↓
PDF 스캔 자동화
    ↓
노트 정리 자동화
    ↓
참조 조직화 자동화
```

---

## 5. HR & 채용

### 이력서 스크리닝

**출처**: [Claude for HR Teams](https://claude-ai.chat/use-cases/hr-teams/)

**성과:**
- 행정 스크리닝 시간 **50% 절감**
- 대량 CV/커버레터 처리 → 순위 목록 생성
- 구조화된 요약 및 명확한 추천 (면접/탤런트풀/거절)

### Anthropic HR팀 활용

- 직무 기술서 작성
- 인터뷰 질문 개발
- 후보자 커뮤니케이션 초안
- 채용 메트릭 분석
- 인터뷰 전사

### Skillfully 사례

**출처**: [Skillfully uses Claude](https://claude.com/customers/skillfully)

기존 이력서 대신 AI 기반 시뮬레이션으로 후보자 실제 능력 평가:
- **전환율**: 10배 향상
- **채용 사이클**: 50% 단축
- **채용 비용**: 70% 감소

### AI 에이전트 팀 구축 사례

**출처**: [Medium - AI Agents for Job Search](https://medium.com/@cheemabyren/i-built-a-team-of-ai-agents-to-find-me-a-job-heres-what-happened-ad19566fc193)

4개 전문 AI 에이전트 = 소형 채용 리서치 회사
- 24/7 작동
- 피로 없음
- **비용**: API 크레딧 약 $2

---

## 6. 고객 서비스

### HappyFox 사례

**출처**: [HappyFox uses Claude in Amazon Bedrock](https://aws.amazon.com/solutions/case-studies/happyfox/)

- **자동 티켓 해결**: +40%
- **에이전트 생산성**: +30%
- AI Agent Copilot이 티켓 전체 분석

### 티켓 자동 분류

**출처**: [Automated Ticket Triage with Claude](https://thomas-wiegold.com/blog/ai-automated-ticket-triage-system-small-business/)

```
새 티켓 (status="new")
    ↓
트리거 → Claude Haiku 전송
    ↓
구조화된 JSON 응답 반환
    ↓
자동 카테고리 할당
```

**비용**: 티켓당 $0.01-0.05
**절감**: 월 1,000 티켓 → 연간 수천 달러

### 고객 지원 에이전트 구축

**출처**: [Customer support agent - Claude Docs](https://platform.claude.com/docs/en/about-claude/use-case-guides/customer-support-chat)

**Tool Use 활용:**
- 고객 정보 조회
- 주문 상세 검색
- 고객 대신 주문 취소

---

## 7. 부동산

### AppFolio 사례

**출처**: [AppFolio uses Claude](https://claude.com/customers/appfolio)

부동산 관리 고객을 위한 AI 지원 응답 및 작업 자동화:
- **주당 시간 절약**: 11시간 (커뮤니케이션만)
- **메시지당 절약**: 26초

### 부동산 분석 Skills

**활용 사례:**
- 부동산 시장 데이터 분석
- 복잡한 보고서 간소화
- 투자 잠재력 평가
- 트렌드 파악 및 인사이트 공유

### CRE Agents

상업용 부동산 전용 "디지털 동료":
- 인수
- 개발
- 자산 관리
- 중개

---

## 8. 헬스케어

### 주의사항

> **면책조항**: Claude는 전문 의료 조언, 진단, 치료를 **대체하지 않습니다**. 의료 상태에 관한 질문은 항상 자격 있는 의료 제공자와 상담하세요.

### Novo Nordisk - NovoScribe

**출처**: [Building AI agents in healthcare](https://www.claude.com/blog/building-ai-agents-in-healthcare-and-life-sciences)

Claude Code와 MongoDB Atlas로 구축:
- 규제 문서 처리 자동화
- 임상 연구 보고서 (최대 300페이지) 자동 생성
- 규제 준수 표준 유지
- **기존**: 연간 2.3개 보고서 → **현재**: 수 분 내 생성

### 진단 성능 연구

**출처**: [Diagnostic Performance of Claude 3](https://www.medrxiv.org/content/10.1101/2024.04.11.24305622v1)

도쿄대학교 연구:
- 임상 기록 + 키 이미지 제공시 진단 정확도 유의미하게 향상
- **HIPAA 준수율**: 99.1% (방사선 보고서 생성시)

### 헬스케어 에이전트 아키텍처

```
5개 시스템 데이터 통합
    ↓
환자 바이탈 모니터링
    ↓
우려 패턴 인식
    ↓
최신 가이드라인 기반 권장사항 초안
    ↓
적합한 임상의에게 승인 요청 라우팅
```

---

## 9. 교육

### Learning Mode (소크라테스식 튜터)

**출처**: [Claude AI's Learning Style](https://medium.com/@CherryZhouTech/claude-ais-learning-style-transform-ai-into-a-socratic-tutor-d4e48f2c9249)

Claude가 답을 직접 주는 대신 질문을 통해 학습 유도:
- AI 생성 솔루션 의존도 감소
- 안내식 탐구를 통한 깊은 이해 촉진

### 교육 솔루션

**출처**: [Claude for Education](https://claude.com/solutions/education)

> "모든 분야 학생들에게 코딩 리터러시가 필요합니다. Claude Code는 확장된 도제 제도처럼 작동하여 전문 프로그래머의 사고 과정을 보여줍니다."

### 교사 활용

- Learning Mode로 동적/인터랙티브 학습 자료 제작
- 소크라테스 방법론 프롬프트 설계
- 학생 독립적 주제 탐색 지원 도구

### 공식 교육 과정

| 과정 | 제공자 |
|------|--------|
| Claude Code: Agentic Coding | DeepLearning.AI + Anthropic |
| Claude Code in Action | Anthropic Skilljar |
| Software Engineering with Claude Code | Coursera (Vanderbilt) |
| Claude Code for Everyone | DAIR.AI |

---

## 10. 저널리즘 & 글쓰기

### 글쓰기 시스템 구축

**출처**: [How I Built My Personal AI Writing Agent](https://medium.com/@pa_sherman/how-i-built-my-personal-ai-writing-agent-with-claude-code-and-you-can-too-4f3ae29019d2)

**결과:**
- **기존**: 기사 23시간
- **현재**: 5시간 (더 나은 일관성과 품질)

### Claude-Journalist

**출처**: [Claude-Journalist AI Agent](https://digialps.com/claude-journalist-an-ai-journalist-agent-to-write-well-researched-articles-on-any-topic-using-claude-3/)

Matt Shumer가 개발한 AI 저널리스트 에이전트:
1. 웹 검색 API로 관련 정보 수집
2. 콘텐츠 분석
3. 주요 미디어 수준의 기사 생성
4. Claude 3가 초안 검토 및 개선 제안

### 뉴스룸 활용

**출처**: [Claude, Editor](https://structureofnews.wordpress.com/2025/10/27/claude-editor/)

LLM의 언어 능력에 집중하면:
- 출력 개선
- 역량 확장
- 제품 리메이크

질문: "기자들이 더 나은 기사를 쓰도록 돕는 머신 에디터를 만들 수 있을까?"

### 커스텀 명령어 예시

```markdown
# /quick-edit
뉴스레터 콘텐츠 작업시
긴 지시문 없이 바로 실행
```

---

## 11. 세일즈 & CRM

### CRM 통합

**출처**: [Using Claude with your CRM](https://www.close.com/blog/claude-crm-how-to)

**기능:**
- 리드, 활동, 기회 데이터 온디맨드 조회
- 커스텀 리포트/시각화 생성
- 실시간 레코드 업데이트
- 독립적 웹 리서치로 새 리드 생성
- CRM 정리 (감사, 리드 클린업, 상태 업데이트)

### 리드 생성 자동화

```
ICP 기준 매칭 기업 찾기
    ↓
웹사이트, 대표전화, 의사결정자 연락처 캡처
    ↓
적합 이유 요약과 함께 CRM에 리드 생성
```

### Salesforce 파트너십

**출처**: [Anthropic Salesforce Partnership](https://www.anthropic.com/news/salesforce-anthropic-expanded-partnership)

Claude가 Salesforce Agentforce 플랫폼의 선호 모델:
- 클라이언트 포트폴리오 요약
- 새 요구사항 플래그
- 고객 아웃리치 자동화
- CRM 인사이트 + 산업 업데이트 결합

---

## 12. 공급망 & 물류

### Smart Warehouse MCP Agent

**출처**: [GitHub - claude-mcp-agent-for-supply-chain](https://github.com/Ayancodes2003/claude-mcp-agent-for-supply-chain)

**구성 에이전트:**
- InventoryManager
- AGVPlanner (자동 가이드 차량)
- RestockAgent
- Coordinator

**기능:**
- 재고 추적
- AGV 이동
- 주문 처리
- Claude 의사결정 via FastAPI

### 실제 성과

| 기업 | 결과 |
|------|------|
| 소매 체인 | 과잉재고 20% 감소 |
| 자동차 제조사 | 리드타임 25% 단축 |
| 제약회사 | 재고 회전율 30% 개선 |

---

## 13. 팟캐스트 & 오디오

### 자율 팟캐스트 제작

**출처**: [Autonomous Podcast Production Agent](https://www.codersarts.com/post/autonomous-podcast-production-agent-ai-driven-audio-content-creation)

**기능:**
- 트렌딩 토픽 리서치
- 청중 맞춤 스크립트 작성
- 동적 호스트/게스트 음성 생성
- 배경 소음 제거
- 오디오 레벨 밸런싱
- 음악/효과 삽입
- 메타데이터 최적화 + 멀티플랫폼 발행

### n8n 워크플로우

```
토픽 입력
    ↓
GPT-5 + Claude Sonnet
    ↓
완전한 팟캐스트 에피소드 인트로 + 오디오 파일
```

### Voice MCP 서버

**출처**: [voice-mcp](https://lobehub.com/mcp/mbailey-voice-mcp)

- Claude와 음성 대화
- 실시간 저지연 음성 인터랙션
- OpenAI API 키 + 마이크/스피커만 필요

---

## 14. 여행 계획

### Travel Planner Skill

**출처**: [travel-planner Agent Skill](https://claude-plugins.dev/skills/@ailabs-393/ai-labs-claude-skills/travel-planner)

**최초 사용시 수집 정보:**
- 예산 레벨
- 여행 스타일
- 관심사
- 식이 제한

**생성 결과:**
- 일별 상세 일정
- 예산 분석
- 패킹 체크리스트
- 문화적 Do's & Don'ts
- 지역별 스케줄

### MCP 통한 예약

**출처**: [Booking Flights and Hotels with Claude and Node.js](https://medium.com/@royalsanga24/practical-ways-to-use-mcp-booking-flights-and-hotels-with-claude-and-node-js-1f9c0e01db89)

```
Claude Desktop (MCP 호스트)
    ↓
Node.js 서버 시작
    ↓
JSON-RPC 연결
    ↓
search_flights / search_hotels 호출
```

### 실제 활용

- 캘린더 검토
- 티켓 가용성 브라우징
- 스케줄 맞는 날짜 선택
- 소셜 미디어에서 레스토랑 추천 추출

---

## 15. 프로젝트 관리

### CCPM (Claude Code Project Manager)

**출처**: [GitHub - automazeio/ccpm](https://github.com/automazeio/ccpm)

**특징:**
- GitHub Issues + Git worktrees 사용
- `parallel: true` 태스크는 충돌 없이 동시 개발
- 완전한 감사 추적: PRD → Epic → Task → Issue → Code → Commit

### AI 개발팀 구축

**출처**: [How I Built an AI Development Team](https://medium.com/@mohammedhjabreel/how-i-built-an-ai-development-team-on-top-of-claude-code-ce0b49c78eb1)

```
프로젝트 매니저 (태스크 생성 + 전문가 호출)
    ↓
전문가들 병렬 작업:
  - 백엔드
  - 데이터베이스
  - 프론트엔드
  - QA
    ↓
프로젝트 매니저가 모니터링 + 완료 보고
```

### APM (Agentic Project Management)

**출처**: [GitHub - claude-code-agentic-project-management](https://github.com/Malgenec/claude-code-agentic-project-management)

- Manager Agent + Implementation Agent
- Memory Banks
- Handover Protocols
- 자동 프로젝트 로딩
- 슬래시 명령어 통합
- 멀티 인스턴스 조정

---

## 16. 개인 비서 & 라이프 자동화

### Claude Code를 개인 비서로

**출처**: [How to Turn Claude Code Into Your Personal AI Assistant](https://www.theneuron.ai/explainer-articles/how-to-turn-claude-code-into-your-personal-ai-assistant)

**핵심 인사이트:**
> "Claude Code를 코딩 AI가 아닌, 컴퓨터의 모든 파일을 읽고 분석하고, 명령을 실행하고, 파일시스템에 직접 쓸 수 있는 **브릴리언트 어시스턴트**로 생각하라."

### 설정 프롬프트

```
"당신은 나의 개인 비서이자 비서실장입니다.
마크다운 파일을 사용해 스스로 정리하세요."
```

### Life OS 자동화

**출처**: [Claude Code Life OS](https://cc.deeptoai.com/docs/en/community-tips/claude-code-life-os)

**자동화 가능 영역:**
- 목표 추적
- 생각 저널링
- 콘텐츠 리서치
- 노트 분석
- 정보 큐레이션

### 17가지 코드 없이 자동화하는 방법

**출처**: [17 Ways to Automate Your Life Without Code](https://medium.com/@ferreradaniel/17-ways-to-automate-your-life-without-code-how-claude-code-runs-the-show-6f8526c2cea4)

**시간 절약 예시:**
- 디지털 라이프 정리: 수동 3시간 → Claude 7분

### 커스텀 명령어

```markdown
# /daily-journal
복잡한 워크플로우를 한 줄로 실행
```

---

## 17. 데이터 시각화 & 리포팅

### Claude Code Analytics Dashboard

**출처**: [Analytics - Claude Code Docs](https://code.claude.com/docs/en/analytics)

**사용 가능 메트릭:**
- Claude가 작성하고 사용자가 승인한 총 코드 라인
- 일별 활성 사용자/세션
- 총 지출 금액

### Analytics API

**출처**: [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api)

**활용 사례:**
- 경영진 대시보드
- AI 도구 비교
- 개발자 생산성 분석
- 비용 추적 및 할당
- 채택 모니터링
- ROI 정당화

### Analysis Tool

**출처**: [Introducing the analysis tool](https://claude.com/blog/analysis-tool)

Claude가 claude.ai에서 직접 JavaScript 코드 작성/실행:
- 정밀 데이터 분석
- 실시간 인사이트
- 수학적으로 정확한 결과

---

## 18. 이메일 관리

### Harper Reed의 이메일 자동화

**출처**: [Getting Claude Code to do my emails](https://harper.blog/2025/12/03/claude-code-email-productivity-mcp-agents/)

**특징:**
- Pipedream MCP 서버 사용
- 에이전트는 직접 전송 불가, 초안만 작성
- 매 이메일 약간씩 수정 (점점 적게)
- 기존에 무시했을 이메일도 처리 가능

### 이메일 에이전트 아키텍처

**출처**: [Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)

**Search Subagent 패턴:**
- 병렬로 여러 검색 쿼리 실행
- 전체 이메일 스레드 대신 관련 발췌만 반환
- MCP로 외부 서비스 통합

### MCP 서버 통합

| MCP | 기능 |
|-----|------|
| Gmail MCP | 포괄적 이메일 자동화 (초안 생성, 전송 포함) |
| Outlook MCP | 메시지 읽기/관리, 답장, 전송, 첨부파일 다운로드 |

---

## 19. 소셜 미디어 관리

### Social-Strategist 서브에이전트

**출처**: [Claude Code Subagents for Digital Marketing](https://www.digitalapplied.com/blog/claude-code-subagents-digital-marketing-guide)

**기능:**
- 브랜드 가이드라인 읽기
- 고성과 포스트 분석 (참여율)
- 콘텐츠 테마 생성
- 해시태그 전략 제안
- 청중 활동 패턴 기반 포스팅 스케줄 제안
- 포스트 카피 변형 생성 (짧은/긴)
- CTA 추천

**결과**: 구조화된 캘린더 CSV, 1시간 내 완료

### MCP 통합

**Crosspost MCP:**
- 다중 소셜 네트워크 포스팅
- 무한 스크롤 없이 소셜 미디어 관리

**Simplified MCP:**
- 네이티브 소셜 미디어 관리
- Claude Desktop에서 리서치 → Simplified Calendar에 스케줄 → 발행

### n8n 워크플로우

```
WordPress 게시물
    ↓
Claude "Social Media Manager" 노드
    ↓
플랫폼 최적화 캡션:
  - Twitter/X: 간결, 해시태그 풍부
  - Facebook/LinkedIn: 전문적, CTA 포함
  - Instagram: 비주얼 중심, 이모지/해시태그
    ↓
Postiz (스케줄러) → 발행
```

---

## 20. 이커머스

### 제품 관리 자동화

**출처**: [Claude AI for Ecommerce](https://designmusketeer.com/print-on-demand/claude-ai-for-ecommerce/)

**기능:**
- 제품 타이틀/설명/태그 개선
- 수요 신호 추적
- 경쟁 환경 변화 모니터링
- 데이터 기반 가격 조정 추천
- 재고 수준 추적
- 수요 예측
- 공급업체 이슈 식별
- 재주문 수준 최적화 제안

### Claude Code 에이전트 기능

- 코드에서 수익 기회 발견
- 가격 티어 및 결제 흐름 구현
- 경쟁사 분석 자동화
- 가격 비교표 생성
- 기능 비교표 생성

---

## 핵심 원칙 요약

### 1. Claude Code는 "코딩 도구"가 아니다

컴퓨터로 할 수 있는 **모든 것**을 자동화하는 범용 에이전트입니다.

### 2. MCP 통합이 핵심

Gmail, Notion, Figma, CRM, 소셜 미디어 등 외부 서비스와 연결하여 능력 확장

### 3. 서브에이전트로 전문화

각 도메인에 특화된 서브에이전트 구축:
- 마케팅 전문가
- 법률 검토자
- 금융 분석가
- HR 스크리너

### 4. Skills로 반복 작업 자동화

자주 하는 작업을 Skill로 만들어 한 줄 명령으로 실행

### 5. 인간 전문가의 보완재

모든 도메인에서 AI는 인간 전문성을 **대체**가 아닌 **보완**

### 6. 시간 절약 = 실질적 ROI

| 도메인 | 절감 |
|--------|------|
| 마케팅 | 75% (8h→2h) |
| 계약 검토 | 80% (4h→55m) |
| HR 스크리닝 | 50% |
| 고객 티켓 | 40% 자동 해결 |
| 이메일 | 디지털 정리 3h→7m |

---

## 시작하기

1. **Claude Code 설치**: [code.claude.com](https://code.claude.com)
2. **MCP 서버 연결**: 필요한 외부 서비스 연결
3. **CLAUDE.md 작성**: 도메인 특화 지침 설정
4. **Skills/서브에이전트 구축**: 반복 작업 자동화
5. **커스텀 명령어 생성**: `/daily-report`, `/analyze-leads` 등

---

*이 가이드는 2026년 1월 기준 웹 리서치를 바탕으로 작성되었습니다.*
