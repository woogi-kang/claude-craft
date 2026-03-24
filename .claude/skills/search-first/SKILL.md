---
name: search-first
description: "구현 전 기존 솔루션 탐색 — 패키지, MCP 서버, 스킬, GitHub 우선 검색"
metadata:
  category: "standalone"
  version: "1.0.0"
  tags: "research, discovery, reuse, efficiency"
  author: "woogi"
---

# Search First

새 코드를 작성하기 전에 기존 솔루션을 탐색하는 체계적 프로세스.

## 왜 필요한가

- 이미 존재하는 솔루션을 재구현하면 시간 낭비
- 검증된 라이브러리가 직접 구현보다 안정적
- 기존 스킬/에이전트로 해결 가능할 수 있음

## 탐색 순서

### 1. 내부 자산 확인
```bash
# 기존 스킬에서 관련 기능 검색
grep -r "keyword" .claude/skills/*/SKILL.md

# 에이전트에서 관련 기능 검색
grep -r "keyword" .claude/agents/

# 스킬 카탈로그 확인
cat docs/skill-catalog.md | grep "keyword"
```

### 2. 패키지 레지스트리 확인
| 스택 | 레지스트리 | 확인 방법 |
|------|-----------|----------|
| Python | PyPI | pypi.org 검색 또는 `pip index versions <package>` |
| Node.js | npm | `npm search` 또는 npmjs.com 검색 |
| Flutter | pub.dev | pub.dev 검색 |

### 3. MCP 서버 확인
- Context7으로 관련 라이브러리 문서 조회
- 기존 MCP 서버에서 해당 기능 제공하는지 확인

### 4. GitHub/오픈소스 확인
- GitHub에서 유사 구현 검색
- 스타 수, 유지보수 상태, 라이선스 확인

## 의사결정 매트릭스

| 판정 | 조건 | 행동 |
|------|------|------|
| **Adopt** | 정확히 맞는 라이브러리 존재 | 설치하고 사용 |
| **Extend** | 80% 맞는 라이브러리 존재 | 래퍼/어댑터 작성 |
| **Compose** | 여러 작은 라이브러리 조합 가능 | 조합하여 사용 |
| **Build** | 적합한 기존 솔루션 없음 | 직접 구현 |

## 적용 시점

다음 상황에서 이 스킬을 활성화:
- 새 기능 구현 시작 전
- "이런 기능이 필요한데" 라는 요청
- 외부 API 연동 전
- 복잡한 알고리즘 구현 전

## 예외 (탐색 건너뛰기)

- 프로젝트 고유 비즈니스 로직
- 보안상 외부 의존성 금지된 경우
- 기존 코드 리팩토링
- 단순 유틸리티 함수 (3줄 이하)
