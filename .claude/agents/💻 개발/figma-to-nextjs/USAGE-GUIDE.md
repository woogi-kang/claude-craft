---
name: "Figma to Next.js Usage Guide"
---

# Figma → Next.js Converter Usage Guide

> 모듈형(B)과 풀스택(C) 버전 사용 가이드

---

## 버전 비교

| 특성 | 모듈형 (B) | 풀스택 (C) |
|------|-----------|-----------|
| 구조 | 8개 독립 Phase 파일 | 단일 통합 에이전트 |
| 유연성 | Phase별 개별 실행 가능 | 전체 파이프라인 자동화 |
| 학습 곡선 | 낮음 (단계별 이해) | 중간 (전체 흐름 이해 필요) |
| 커스터마이징 | Phase 파일 직접 수정 | Skills/Templates 수정 |
| 권장 사용 | 학습, 디버깅, 부분 변환 | 전체 프로젝트 변환 |

---

## 사전 준비

### 1. Figma MCP 연결 확인

```bash
# Claude Code에서 Figma MCP 도구 호출
# (bash 명령어가 아닌 MCP 도구입니다)
whoami
```

성공 응답 예시:
```json
{
  "id": "12345",
  "name": "Your Name",
  "email": "your@email.com"
}
```

### 2. Next.js 프로젝트 준비

```bash
# 새 프로젝트 생성 (없는 경우)
npx create-next-app@latest my-app --typescript --tailwind --app

# shadcn/ui 초기화
cd my-app
npx shadcn@latest init

# 필수 컴포넌트 설치
npx shadcn@latest add button card input
```

### 3. Figma URL 준비

```
형식: https://www.figma.com/design/[FILE_KEY]/[FILE_NAME]?node-id=[NODE_ID]

예시: https://www.figma.com/design/ABC123/Landing-Page?node-id=123-456
```

---

## 모듈형 (B) 사용법

### 위치

```
.claude/agents/figma-to-nextjs/modular/
├── figma-to-nextjs.md          # 메인 에이전트
└── phases/
    ├── phase-0-project-scan.md
    ├── phase-1-design-scan.md
    ├── phase-2-token-extract.md
    ├── phase-3-component-mapping.md
    ├── phase-4-code-generate.md
    ├── phase-5-asset-process.md
    ├── phase-6-pixel-perfect.md
    └── phase-7-responsive.md
```

### 전체 실행

```
@figma-to-nextjs [FIGMA_URL]

예시:
@figma-to-nextjs https://www.figma.com/design/ABC123/Landing-Page?node-id=123-456
```

### Phase별 개별 실행

```
# Phase 0: 프로젝트 스캔
프로젝트 구조를 분석해줘. phases/phase-0-project-scan.md 참조

# Phase 1: 디자인 스캔
Figma 디자인을 분석해줘: [FIGMA_URL]
phases/phase-1-design-scan.md 참조

# Phase 2: 토큰 추출
디자인 토큰을 추출해줘
phases/phase-2-token-extract.md 참조

# Phase 3: 컴포넌트 매핑
컴포넌트 매핑을 확인해줘
phases/phase-3-component-mapping.md 참조

# Phase 4: 코드 생성
컴포넌트 코드를 생성해줘
phases/phase-4-code-generate.md 참조

# Phase 5: 에셋 처리
이미지와 아이콘을 처리해줘
phases/phase-5-asset-process.md 참조

# Phase 6: Pixel-Perfect 검증
Figma와 1:1 비교 검증해줘
phases/phase-6-pixel-perfect.md 참조

# Phase 7: 반응형 검증
반응형 레이아웃을 검증해줘
phases/phase-7-responsive.md 참조
```

### 장점

- 각 Phase를 독립적으로 실행 가능
- 문제 발생 시 해당 Phase만 재실행
- Phase 파일을 직접 수정하여 커스터마이징
- 학습 및 디버깅에 적합

---

## 풀스택 (C) 사용법

### 위치

```
.claude/agents/figma-to-nextjs/fullstack/
├── figma-to-nextjs-pro.md      # 메인 에이전트
├── skills/
│   ├── figma-tokens.md         # 토큰 추출 스킬
│   ├── tailwind-mapping.md     # Tailwind 매핑 스킬
│   └── shadcn-patterns.md      # shadcn 패턴 스킬
└── templates/
    └── component.tsx.template  # 컴포넌트 템플릿
```

### 전체 변환

```
@figma-to-nextjs-pro convert [FIGMA_URL]

예시:
@figma-to-nextjs-pro convert https://www.figma.com/design/ABC123/Landing-Page?node-id=123-456
```

### Phase별 실행

```
@figma-to-nextjs-pro phase:0 scan          # 프로젝트 스캔
@figma-to-nextjs-pro phase:1 analyze       # 디자인 분석
@figma-to-nextjs-pro phase:2 tokens        # 토큰 추출
@figma-to-nextjs-pro phase:3 map           # 컴포넌트 매핑
@figma-to-nextjs-pro phase:4 generate      # 코드 생성
@figma-to-nextjs-pro phase:5 assets        # 에셋 처리
@figma-to-nextjs-pro phase:6 verify        # 검증
@figma-to-nextjs-pro phase:7 responsive    # 반응형
```

### Skills 활용

```
# 토큰 추출 스킬 단독 사용
skills/figma-tokens.md 참조하여 디자인 토큰을 추출해줘

# Tailwind 매핑 스킬 단독 사용
skills/tailwind-mapping.md 참조하여 Figma 값을 Tailwind로 변환해줘

# shadcn 패턴 스킬 단독 사용
skills/shadcn-patterns.md 참조하여 컴포넌트 패턴을 적용해줘
```

### 장점

- 전체 파이프라인 자동화
- Skills 시스템으로 재사용 가능한 지식
- 템플릿 기반 일관된 코드 생성
- 대규모 프로젝트 변환에 적합

---

## Rate Limit 관리

### 플랜별 제한

| 플랜 | 제한 |
|------|------|
| Starter | 6 calls/month |
| Professional | 높은 제한 |
| Organization | 높은 제한 |
| Enterprise | 높은 제한 |

### 토큰 절약 전략

```typescript
// MUST: 항상 get_metadata 먼저 호출 (80% 토큰 절약)
const metadata = await get_metadata({ fileKey, nodeId });

// 필요한 노드만 선택 후 get_design_context 호출
const targetNodes = selectRelevantNodes(metadata);
for (const node of targetNodes) {
  await get_design_context({ fileKey, nodeId: node.id });
}
```

### Rate Limit 도달 시

1. 작업 일시 중지
2. 에러 메시지에서 대기 시간 확인
3. 캐시된 데이터로 작업 계속
4. 제한 해제 후 재시도

---

## 문제 해결

### Figma 연결 실패

```
1. MCP 설정 확인 (.mcp.json)
2. Figma 토큰 유효성 확인
3. whoami 호출로 연결 테스트
```

### 토큰 추출 실패

```
1. 파일 접근 권한 확인
2. 노드 ID 유효성 검증
3. get_metadata로 구조 재확인
```

### 컴포넌트 생성 오류

```
1. TypeScript 오류: strict 모드 확인
2. Import 오류: 경로 별칭 확인 (@/)
3. Tailwind 오류: 설정 파일 확인
```

### Pixel-Perfect 불일치

```
1. 간격: Figma px → Tailwind 매핑 테이블 확인
2. 색상: CSS 변수 정확성 확인
3. 폰트: 웹폰트 로드 확인
```

---

## 권장 워크플로우

### 처음 사용자

1. **모듈형 (B)** 로 시작
2. Phase 0-2 실행하여 프로젝트/디자인 분석
3. Phase 3-4에서 컴포넌트 생성 학습
4. Phase 5-7에서 검증 방법 이해
5. 익숙해지면 풀스택 (C)로 전환

### 숙련 사용자

1. **풀스택 (C)** 로 전체 변환
2. Skills 커스터마이징
3. Templates 확장
4. 자동화 파이프라인 구축

### 대규모 프로젝트

1. 풀스택 (C) 사용
2. 페이지별로 분할 변환
3. 공통 컴포넌트 먼저 변환
4. 페이지별 섹션 순차 변환
5. 최종 통합 검증

---

## 출력 구조

```
src/
├── components/
│   ├── ui/                     # shadcn/ui 컴포넌트
│   ├── layout/                 # 레이아웃 (Header, Footer, Nav)
│   ├── sections/               # 페이지 섹션
│   └── [feature]/              # 기능별 컴포넌트
│
├── styles/
│   └── variables.css           # Figma 토큰 CSS 변수
│
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
│
└── public/
    ├── images/                 # 이미지 에셋
    ├── icons/                  # SVG 아이콘
    └── logos/                  # 로고 파일
```

---

## 체크리스트

### 변환 전

- [ ] Figma MCP 연결 확인
- [ ] Next.js 프로젝트 준비
- [ ] shadcn/ui 초기화
- [ ] Figma URL 준비

### 변환 중

- [ ] Rate Limit 모니터링
- [ ] 토큰 추출 확인
- [ ] 컴포넌트 생성 확인
- [ ] 에셋 처리 확인

### 변환 후

- [ ] TypeScript 오류 없음
- [ ] 빌드 성공
- [ ] Pixel-Perfect 검증 (95%+)
- [ ] 반응형 검증 완료

---

## 버전 정보

- Agent Version: 1.0.0
- Figma MCP API: 2025.1
- Next.js Target: 15.x
- Tailwind Target: 4.x
- shadcn/ui: Latest
