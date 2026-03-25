# Phase 4 Specification - Synthesis

> 프로젝트: medical-tourism-seo (MediScope)
> 작성일: 2026-03-25
> 상태: 완료

---

## Executive Summary

"MediScope" - AI 병원 홈페이지 진단 플랫폼의 PRD 및 기능명세서를 완성했다. Phase 3 검증 결과(GO, 8.0/10)를 기반으로, 12주 MVP 로드맵에 따라 4개 Phase(A-D)로 나누어 점진적으로 기능을 확장하는 구조다.

---

## Key Decisions

### 제품 구조

| 결정 | 내용 | 근거 |
|------|------|------|
| 제품명 | MediScope (메디스코프) | 의료(Medi) + 진단(Scope), 직관적 |
| 핵심 전략 | 무료 진단 -> 리드 수집 -> 유료 전환 | Phase 3 검증: 영업 허들 낮추기 |
| 게이트 위치 | 프리뷰(무료) / 상세(정보 입력) | 진단 결과로 호기심 유발 후 전환 |
| 리포트 형식 | 웹 + PDF 이중 제공 | 웹은 즉시 확인, PDF는 보고용 |

### 기술 아키텍처

| 결정 | 내용 | 근거 |
|------|------|------|
| 아키텍처 | Next.js (프론트+API) + FastAPI (Worker) 분리 | CPU 집약적 크롤링 분리, 독립 스케일링 |
| DB | Supabase (PostgreSQL) | Auth, Storage, Realtime 통합 |
| 작업 큐 | Redis (Upstash) + arq/Celery | 비동기 크롤링 처리 |
| LLM | Gemini Flash (주) + GPT-4o-mini (보조) | 비용 효율 + 정확도 |
| 배포 | Vercel + Railway | 서버리스 + 컨테이너 조합 |
| 월 인프라 비용 | ~12만원 ($85-95) | 1인 창업에 적합한 비용 |

### MVP 스코프

| 결정 | 내용 | 근거 |
|------|------|------|
| 진단 항목 수 | 25개 (5개 카테고리) | 포괄적이면서도 관리 가능한 범위 |
| Phase A (Week 1-6) | 진단 + 리포트 + 리드 수집 | 핵심 가치 검증 |
| Phase B (Week 7-10) | 프로젝트 관리 + 벤치마크 | 유료 전환 도구 |
| Phase C (Week 11-12) | 구독 모니터링 | MRR 시작 |
| Phase D (Post-MVP) | LINE/WeChat 대시보드 | 첫 수익 후 |

---

## 산출물 목록

| 문서 | 경로 | 포함 내용 |
|------|------|----------|
| PRD (통합) | `04-specification/prd.md` | 전 14개 섹션 포함 |

### PRD 포함 내용 체크리스트

| 섹션 | 상태 | 핵심 내용 |
|------|------|----------|
| 제품 개요 | O | 제품명, 가치 제안, 비즈니스 컨텍스트 |
| MVP 범위 | O | Phase A-D 정의, In/Out 스코프 |
| 페르소나 | O | 3개 페르소나 (원장, 마케터, 에이전시) |
| 유저 플로우 | O | Core Flow, Admin Flow, Monitoring Flow |
| 기능 명세 | O | F1-F6, 25개 진단 항목 상세 |
| 데이터 모델 | O | ERD, 6개 테이블 스키마, RLS |
| API 설계 | O | Public/Worker/Admin API 엔드포인트 |
| 기술 스택 | O | Frontend/Backend/AI/인프라 상세 |
| 시스템 아키텍처 | O | 전체 아키텍처, 시퀀스 다이어그램 |
| LINE/WeChat 스펙 | O | 연동 요구사항, 데이터 모델, UI 목업 |
| MoSCoW 우선순위 | O | Must/Should/Could/Won't 분류 |
| 12주 로드맵 | O | 주차별 상세 계획, 5개 마일스톤 |
| 비기능 요구사항 | O | 성능, 보안, 가용성, 확장성 |
| 성공 지표 | O | Product/Business/Technical 지표 |

---

## Risk & Open Questions

### 해결된 질문

1. 기술 스택 선정 -> Next.js + FastAPI + Supabase 확정
2. 진단 항목 범위 -> 25개 항목, 5개 카테고리
3. 리포트 게이트 전략 -> 프리뷰(무료) + 상세(정보 입력)
4. 월 인프라 비용 -> ~12만원

### 미결 질문 (개발 중 결정)

1. 크롤링 동시성 최적화 (Playwright 인스턴스 풀 사이즈)
2. LLM 프롬프트 튜닝 (GEO/AEO 진단 정확도)
3. PDF 리포트 디자인 (템플릿 상세 레이아웃)
4. 콜드 아웃리치 이메일 법적 검토 (수신 동의 없는 발송)

---

## Next Steps

| 순서 | 액션 | 비고 |
|------|------|------|
| 1 | Phase 5 (Estimation) | 공수 재검증, 비용 상세 산출 |
| 2 | Phase 6 (Design) | 랜딩페이지/대시보드 와이어프레임 |
| 3 | 개발 시작 | Week 1: 모노레포 셋업 + 크롤링 엔진 |
