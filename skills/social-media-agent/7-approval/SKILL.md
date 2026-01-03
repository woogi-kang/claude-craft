---
name: social-approval
description: |
  소셜미디어 콘텐츠의 승인 워크플로우를 관리합니다.

  활성화 조건:
  - "콘텐츠 승인해줘"
  - "승인 요청"
  - "리뷰 요청"
  - "최종 확인"
---

# 7. Approval: 승인 워크플로우

## 개요

콘텐츠 발행 전 체계적인 승인 프로세스로 품질과 일관성을 보장합니다.

## 승인 워크플로우 유형

### 1. 단순 워크플로우 (소규모 팀)

```
작성자 → 승인자 → 발행
```

```yaml
simple_workflow:
  suitable_for: "1-3명 팀, 개인 브랜드"

  steps:
    1_draft:
      actor: "콘텐츠 작성자"
      action: "콘텐츠 작성 완료"
      output: "초안"

    2_review:
      actor: "승인자 (팀장/본인)"
      action: "검토 및 피드백"
      output: "승인/수정 요청"

    3_publish:
      actor: "작성자"
      action: "발행"
```

### 2. 표준 워크플로우 (중간 규모)

```
작성자 → 편집자 → 승인자 → 발행
```

```yaml
standard_workflow:
  suitable_for: "4-10명 팀, 중소기업"

  steps:
    1_draft:
      actor: "콘텐츠 작성자"
      action: "초안 작성"
      checklist:
        - 콘텐츠 작성 완료
        - 비주얼 첨부
        - 해시태그 준비

    2_edit:
      actor: "편집자/리뷰어"
      action: "품질 검토"
      checklist:
        - 맞춤법/문법
        - 브랜드 톤 일치
        - 팩트 체크

    3_approve:
      actor: "승인자 (매니저)"
      action: "최종 승인"
      checklist:
        - 전략 적합성
        - 타이밍 적절성
        - 리스크 검토

    4_schedule:
      actor: "작성자/스케줄러"
      action: "발행 예약"
```

### 3. 기업 워크플로우 (대규모)

```
작성자 → 편집자 → 법무팀 → 부서장 → 최종 승인자 → 발행
```

```yaml
enterprise_workflow:
  suitable_for: "대기업, 규제 산업"

  steps:
    1_draft:
      actor: "콘텐츠 작성자"
      sla: "D-5"

    2_creative_review:
      actor: "크리에이티브 팀"
      sla: "D-4"
      focus: "비주얼, 브랜드 일관성"

    3_copy_review:
      actor: "카피라이터/편집자"
      sla: "D-3"
      focus: "텍스트 품질, 메시지"

    4_legal_review:
      actor: "법무/컴플라이언스 팀"
      sla: "D-2"
      focus: "법적 리스크, 규정 준수"

    5_manager_approval:
      actor: "부서 매니저"
      sla: "D-1"
      focus: "전략 적합성"

    6_final_approval:
      actor: "최종 승인자"
      sla: "D-0"
      focus: "최종 확인"

    7_publish:
      actor: "소셜미디어 매니저"
```

## 역할별 체크리스트

### 작성자 (Creator)

```yaml
creator_checklist:
  before_submission:
    content:
      - [ ] 캡션/텍스트 작성 완료
      - [ ] 맞춤법 검사 완료
      - [ ] CTA 포함

    visual:
      - [ ] 이미지/영상 첨부
      - [ ] 올바른 사이즈/비율
      - [ ] 브랜드 가이드 준수

    metadata:
      - [ ] 해시태그 준비
      - [ ] 태그/멘션 확인
      - [ ] 링크 테스트

    documentation:
      - [ ] 승인 요청 메모 작성
      - [ ] 발행 희망 일시 명시
```

### 편집자 (Editor)

```yaml
editor_checklist:
  review_items:
    text_quality:
      - [ ] 맞춤법/문법 오류 없음
      - [ ] 문장 가독성 양호
      - [ ] 톤앤매너 일관성

    brand_alignment:
      - [ ] 브랜드 보이스 준수
      - [ ] 메시지 일관성
      - [ ] 비주얼 가이드 준수

    accuracy:
      - [ ] 팩트 검증 완료
      - [ ] 링크 작동 확인
      - [ ] 날짜/숫자 정확성
```

### 법무팀 (Legal)

```yaml
legal_checklist:
  review_items:
    disclosure:
      - [ ] 광고 표시 적절
      - [ ] 제휴/협찬 고지

    copyright:
      - [ ] 이미지 라이선스 확인
      - [ ] 음악/영상 권리 확보
      - [ ] 인용 출처 명시

    compliance:
      - [ ] 산업 규정 준수
      - [ ] 개인정보 보호
      - [ ] 경쟁법 준수
```

### 승인자 (Approver)

```yaml
approver_checklist:
  final_review:
    strategic:
      - [ ] 마케팅 목표 부합
      - [ ] 타겟 오디언스 적합
      - [ ] 캠페인 일관성

    timing:
      - [ ] 발행 시점 적절
      - [ ] 민감 이슈 없음
      - [ ] 경쟁사 동향 고려

    risk:
      - [ ] 브랜드 리스크 없음
      - [ ] 논란 가능성 검토
      - [ ] 위기 대응 준비
```

## 승인 상태

```yaml
approval_status:
  draft:
    description: "작성 중"
    next_action: "제출"

  pending_review:
    description: "검토 대기"
    next_action: "리뷰어 배정"

  in_review:
    description: "검토 중"
    next_action: "피드백/승인"

  needs_revision:
    description: "수정 필요"
    next_action: "작성자 수정"
    feedback_required: true

  approved:
    description: "승인됨"
    next_action: "발행 예약"

  scheduled:
    description: "발행 예약됨"
    next_action: "자동 발행"

  published:
    description: "발행됨"
    next_action: "성과 모니터링"

  rejected:
    description: "반려됨"
    next_action: "재작성 또는 폐기"
    reason_required: true
```

## 긴급 발행 프로세스

```yaml
urgent_process:
  trigger:
    - 실시간 이슈 대응
    - 트렌딩 토픽 참여
    - 위기 상황 커뮤니케이션

  expedited_flow:
    1: "작성자 → 승인자 직접 연락"
    2: "구두/메시지로 빠른 승인"
    3: "발행 후 문서화"

  safeguards:
    - 긴급 승인 권한자 지정
    - 사후 검토 필수
    - 긴급 사용 로그 기록

  template: |
    [긴급 승인 요청]

    콘텐츠: [링크/내용]
    사유: [긴급 사유]
    발행 희망: [시간]
    승인 요청 대상: [@승인자]
```

## 피드백 가이드

### 효과적인 피드백 작성

```yaml
feedback_guidelines:
  structure:
    specific: "구체적인 위치/내용 명시"
    actionable: "수정 방향 제시"
    priority: "중요도 표시 (필수/권장)"

  examples:
    bad: "톤이 이상해요"
    good: |
      2번째 문단의 '~했다'를 '~했어요'로 변경 권장.
      전체적으로 캐주얼한 톤인데 이 부분만 딱딱합니다.
      [권장]

    bad: "이미지 바꿔주세요"
    good: |
      메인 이미지의 텍스트가 배경과 대비가 부족합니다.
      텍스트 색상을 흰색→검정으로 변경하거나,
      배경에 오버레이 추가해주세요.
      [필수]
```

### 피드백 템플릿

```yaml
feedback_template:
  content_id: "[콘텐츠 ID]"
  reviewer: "[리뷰어 이름]"
  date: "[날짜]"
  status: "needs_revision"

  feedback:
    - location: "캡션 1번째 문단"
      type: "text"
      priority: "required"
      current: "[현재 내용]"
      suggestion: "[수정 제안]"
      reason: "[이유]"

    - location: "3번째 슬라이드"
      type: "visual"
      priority: "recommended"
      issue: "[문제점]"
      suggestion: "[수정 제안]"

  overall_notes: |
    전체적으로 좋습니다. 위 2가지 수정 후 재제출 부탁드립니다.
```

## 승인 도구 추천

```yaml
approval_tools:
  social_management:
    - name: "Hootsuite"
      features: ["다단계 승인", "역할 권한", "히스토리"]

    - name: "Sprout Social"
      features: ["승인 워크플로우", "협업", "캘린더"]

    - name: "Planable"
      features: ["시각적 협업", "댓글", "버전 관리"]

  project_management:
    - name: "Asana"
      features: ["워크플로우 자동화", "의존성"]

    - name: "Monday.com"
      features: ["커스텀 상태", "자동화"]

    - name: "Notion"
      features: ["데이터베이스", "협업"]
```

## 승인 요청 템플릿

```yaml
approval_request:
  subject: "[승인 요청] [플랫폼] - [콘텐츠 제목] - [발행일]"

  body: |
    안녕하세요, [승인자]님

    아래 콘텐츠 승인 요청드립니다.

    ## 콘텐츠 정보
    - 플랫폼: [Instagram/LinkedIn/X/Threads]
    - 유형: [피드/릴스/스토리/캐러셀]
    - 발행 예정: [날짜 시간]

    ## 콘텐츠 링크
    [초안 링크]

    ## 첨부
    - 캡션: [텍스트]
    - 비주얼: [이미지/영상 링크]
    - 해시태그: [해시태그 목록]

    ## 체크리스트
    - [x] 맞춤법 검사 완료
    - [x] 브랜드 가이드 준수
    - [x] 팩트 체크 완료
    - [x] 법적 검토 완료 (해당시)

    ## 특이사항
    [특별히 검토 요청하는 부분이나 참고사항]

    승인 부탁드립니다.
    감사합니다.
```

## 다음 단계

승인 완료 후:
1. → `8-schedule`: 발행 예약
2. → 발행 후 `10-engagement`: 커뮤니티 관리
3. → `11-analytics`: 성과 분석
