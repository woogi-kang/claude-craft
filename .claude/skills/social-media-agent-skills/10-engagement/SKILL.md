---
name: social-engagement
description: |
  소셜미디어 커뮤니티를 관리하고 참여를 유도합니다.

  활성화 조건:
  - "댓글 대응해줘"
  - "커뮤니티 관리"
  - "DM 답변 템플릿"
  - "부정적 댓글 대응"
  - "위기 대응"
---

# 10. Engagement: 커뮤니티 관리

## 개요

발행 후 오디언스와의 양방향 소통을 관리하여 참여율과 브랜드 충성도를 높입니다.

## 댓글 응답 가이드

### 응답 우선순위

```yaml
response_priority:
  immediate: # 1시간 이내
    - 질문/문의
    - 불만/컴플레인
    - 인플루언서/VIP
    - 잠재 위기 신호

  high: # 4시간 이내
    - 제품/서비스 관련 피드백
    - 상세한 의견/제안
    - 구매 의향 표현

  medium: # 24시간 이내
    - 긍정적 피드백
    - 일반적인 댓글
    - 이모지만 있는 댓글

  low: # 48시간 이내 또는 생략
    - 스팸성 댓글
    - 관련 없는 홍보
    - 단순 태그 (친구 태그)
```

### 댓글 유형별 응답 템플릿

```yaml
response_templates:
  positive_feedback:
    tone: "감사, 따뜻하게"
    examples:
      - "감사합니다! 도움이 됐다니 기뻐요 😊"
      - "좋게 봐주셔서 감사해요! 더 좋은 콘텐츠로 보답할게요"
      - "최고의 칭찬이에요 🙏 앞으로도 기대해주세요!"

  question:
    tone: "도움이 되게, 정확하게"
    examples:
      - "[답변]. 더 궁금하신 점 있으시면 언제든 물어봐 주세요!"
      - "좋은 질문이에요! [답변]. 도움이 됐으면 좋겠어요 😊"
      - "[답변]. 자세한 내용은 프로필 링크에서 확인해 보세요!"

  negative_feedback:
    tone: "공감, 해결 지향적"
    examples:
      - "불편을 드려 정말 죄송합니다. DM으로 자세히 말씀해 주시면 해결해 드릴게요."
      - "소중한 피드백 감사합니다. 개선에 참고하겠습니다!"
      - "이런 경험을 하셨군요. 저희가 어떻게 도와드릴 수 있을지 DM 주세요."

  suggestion:
    tone: "열린 자세, 감사"
    examples:
      - "좋은 아이디어예요! 팀에 공유해 볼게요 ✨"
      - "이런 제안 정말 감사해요. 검토해 보겠습니다!"

  spam_promotional:
    action: "무시 또는 삭제"
    exceptions: "관련성 있으면 간단히 반응"

  tagging_friends:
    action: "반응하거나 무시"
    optional: "재미있는 반응 추가 가능"
```

### 플랫폼별 응답 톤

```yaml
platform_response_tone:
  instagram:
    style: "친근하고 따뜻하게"
    emoji: "적극 활용"
    length: "1-2문장"

  linkedin:
    style: "전문적이지만 인간적"
    emoji: "최소한"
    length: "2-3문장, 상세하게"

  x:
    style: "간결하고 위트있게"
    emoji: "가끔"
    length: "1문장"

  threads:
    style: "친구처럼 캐주얼하게"
    emoji: "자유롭게"
    length: "대화체로 짧게"
```

## DM 관리

### DM 유형별 대응

```yaml
dm_management:
  inquiry:
    response_time: "24시간 이내"
    template: |
      안녕하세요! 문의 감사합니다 😊

      [질문에 대한 답변]

      더 궁금하신 점 있으시면 편하게 물어봐 주세요!

  collaboration_request:
    response_time: "48시간 이내"
    template: |
      안녕하세요! 협업 제안 감사합니다.

      저희 브랜드와의 협업에 관심 가져주셔서 감사해요.
      상세 내용을 [이메일]로 보내주시면 검토 후 연락드릴게요.

      감사합니다!

  complaint:
    response_time: "4시간 이내"
    template: |
      안녕하세요, 먼저 불편을 드려 정말 죄송합니다.

      말씀해 주신 내용 확인했습니다.
      [문제 해결 방안/담당자 연결 안내]

      빠르게 해결해 드리겠습니다.
      양해 부탁드립니다.

  spam:
    action: "무시 또는 차단"
```

## 부정적 상황 대응

### 부정적 댓글 대응 프레임워크

```yaml
negative_comment_framework:
  step_1_assess:
    questions:
      - "댓글이 사실에 기반한가?"
      - "우리 잘못이 있는가?"
      - "공개 대응이 필요한가?"
      - "확산 가능성은?"

  step_2_categorize:
    constructive_criticism:
      action: "감사 + 개선 약속"
      visibility: "공개 응답"

    legitimate_complaint:
      action: "사과 + 해결책 + DM 유도"
      visibility: "공개 사과 후 DM"

    misinformation:
      action: "정정 정보 제공"
      visibility: "공개 (정중하게)"

    trolling:
      action: "무시 또는 숨김"
      visibility: "대응 안 함"

    hate_speech:
      action: "삭제 + 차단 + 신고"
      visibility: "즉시 조치"

  step_3_respond:
    template: |
      1. 공감 표현
      2. 책임 인정 (해당시)
      3. 해결책 제시
      4. 후속 조치 안내

    example: |
      불편을 드려 정말 죄송합니다.
      말씀하신 부분 확인했고, 이런 경험을 하셨다니 저희도 안타깝습니다.
      바로 담당팀에 전달해서 [해결책]으로 조치하겠습니다.
      DM으로 연락처 남겨주시면 직접 연락드릴게요.
```

### 위기 대응 프로토콜

```yaml
crisis_protocol:
  trigger_signals:
    - "부정적 멘션 급증"
    - "언론 문의"
    - "인플루언서 비판"
    - "바이럴 비판 콘텐츠"
    - "내부 고발/유출"

  immediate_actions:
    1: "발행 예정 콘텐츠 일시 중단"
    2: "상황 파악 (누가, 무엇을, 왜)"
    3: "내부 보고 (PR/경영진)"
    4: "대응 메시지 준비"
    5: "모니터링 강화"

  response_guidelines:
    speed: "1시간 이내 초기 대응"
    tone: "진정성, 공감, 책임감"
    consistency: "모든 채널 동일 메시지"

    do:
      - "사실 인정 (확인된 경우)"
      - "진심어린 사과"
      - "구체적 해결책 제시"
      - "후속 조치 약속"

    dont:
      - "변명하거나 책임 회피"
      - "감정적 대응"
      - "댓글 삭제 (증거 인멸로 보임)"
      - "무대응 (상황 악화)"

  template: |
    [상황]에 대해 진심으로 사과드립니다.

    현재 상황을 파악 중이며,
    [구체적 조치]를 진행하고 있습니다.

    추가 업데이트는 [시점]에 공유드리겠습니다.

    불편을 드려 죄송합니다.
```

## 적극적 참여 전략

### 아웃바운드 참여

```yaml
outbound_engagement:
  purpose: "커뮤니티 구축, 도달률 증가, 관계 형성"

  daily_routine:
    - "팔로워 새 포스트에 의미 있는 댓글 5-10개"
    - "관련 해시태그 포스트에 참여"
    - "업계 인플루언서 포스트에 반응"
    - "멘션된 포스트에 감사 표현"

  quality_comments:
    good:
      - "구체적인 의견/생각 공유"
      - "추가 인사이트 제공"
      - "진심어린 질문"

    bad:
      - "이모지만 (👍, ❤️)"
      - "일반적인 칭찬 ("좋아요!")"
      - "자기 홍보"

  example:
    instead_of: "좋은 글이네요!"
    better: |
      이 부분 정말 공감돼요!
      저도 비슷한 경험이 있는데,
      [관련 인사이트 추가]
      덕분에 새로운 관점을 얻었어요 🙏
```

### 참여 유도 전략

```yaml
engagement_tactics:
  questions:
    - "여러분은 어떻게 생각하세요?"
    - "비슷한 경험 있으신 분?"
    - "A vs B, 뭐가 더 좋아요?"

  polls:
    - "투표해주세요!"
    - "결과 공유할게요"

  challenges:
    - "오늘 도전해보세요"
    - "결과 공유해주세요"

  user_generated:
    - "여러분의 이야기를 들려주세요"
    - "태그하면 리포스트할게요"

  exclusivity:
    - "팔로워만을 위한 팁"
    - "DM 주시면 공유해드릴게요"
```

## 커뮤니티 가이드라인

```yaml
community_guidelines:
  values:
    - "상호 존중"
    - "건설적인 대화"
    - "다양성 존중"
    - "정확한 정보"

  prohibited:
    - "혐오 발언"
    - "스팸/홍보"
    - "개인정보 노출"
    - "허위 정보"

  moderation:
    warning: "가이드라인 위반 시 경고"
    hide: "반복 위반 시 댓글 숨김"
    block: "심각한 위반 시 차단"
    report: "불법 콘텐츠 신고"
```

## 모니터링 도구

```yaml
monitoring_tools:
  free:
    - "각 플랫폼 알림"
    - "Google Alerts"

  paid:
    - name: "Hootsuite"
      features: ["통합 인박스", "팀 할당"]

    - name: "Sprout Social"
      features: ["소셜 리스닝", "감성 분석"]

    - name: "Brandwatch"
      features: ["멘션 모니터링", "위기 감지"]
```

## 출력 형식

```yaml
engagement_output:
  period: "2025-01-04"

  summary:
    comments_received: 45
    comments_responded: 40
    response_rate: "89%"
    avg_response_time: "2시간"

  sentiment:
    positive: 70%
    neutral: 25%
    negative: 5%

  notable_interactions:
    - type: "인플루언서 멘션"
      account: "@influencer"
      action: "감사 댓글 + DM"

    - type: "고객 불만"
      issue: "[이슈]"
      action: "공개 사과 + DM 해결"

  action_items:
    - "FAQ 업데이트 필요 (같은 질문 반복)"
    - "인플루언서 협업 가능성 탐색"
```

## 다음 단계

커뮤니티 관리 진행 중/후:
1. → `11-analytics`: 참여율 분석
2. → `1-research`: 오디언스 인사이트 수집
3. → `4-content`: 피드백 기반 콘텐츠 기획
