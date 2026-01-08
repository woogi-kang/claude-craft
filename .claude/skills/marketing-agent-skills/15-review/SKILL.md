---
name: mkt-review
description: |
  마케팅 자료 종합 검토 및 품질 체크.
  브랜드 일관성, 메시지 정확성, 실행 준비도를 확인합니다.
triggers:
  - "마케팅 검토"
  - "리뷰"
  - "품질 체크"
  - "최종 확인"
input:
  - 마케팅 산출물 전체
output:
  - reports/review-report.md
---

# Review Skill

마케팅 자료의 최종 품질을 검토합니다.

## 검토 영역

### 1. 브랜드 일관성

```yaml
brand_consistency:
  voice_tone:
    - 톤앤매너 일관성
    - 브랜드 가이드 준수
    - 금지 표현 사용 여부

  visual:
    - 컬러 일관성
    - 폰트 일관성
    - 로고 사용 규정

  messaging:
    - 핵심 메시지 일관성
    - 가치 제안 통일
    - 태그라인 정확성
```

### 2. 콘텐츠 품질

```yaml
content_quality:
  accuracy:
    - 팩트 정확성
    - 숫자/통계 검증
    - 출처 명시

  clarity:
    - 메시지 명확성
    - 타겟 언어 사용
    - 전문 용어 적절성

  persuasion:
    - CTA 명확성
    - 혜택 중심 표현
    - 긴급성/희소성 적절성
```

### 3. 기술 검토

```yaml
technical_review:
  links:
    - 모든 링크 작동
    - UTM 파라미터 설정
    - 랜딩페이지 연결

  tracking:
    - GA 설정
    - 픽셀 설치
    - 전환 추적

  format:
    - 규격 준수
    - 파일 형식 적절
    - 용량 최적화
```

### 4. 법적/컴플라이언스

```yaml
legal_compliance:
  copyright:
    - 이미지 저작권
    - 폰트 라이선스
    - 음악 권리

  regulations:
    - 광고 규정 준수
    - 개인정보 보호
    - 산업별 규제

  claims:
    - 과장 광고 여부
    - 비교 광고 적절성
    - 보증/증거
```

## 검토 체크리스트

### 전략 문서

```
□ 목표가 SMART 기준 충족
□ 타겟이 명확하게 정의됨
□ 포지셔닝이 차별화됨
□ 채널 선택이 타겟에 적합
□ 예산 배분이 합리적
□ KPI가 측정 가능
□ 타임라인이 현실적
```

### 카피 & 콘텐츠

```
□ 헤드라인이 가치 제안 명확
□ CTA가 행동 지향적
□ 혜택 중심 표현 (기능 X)
□ 타겟 언어 사용
□ 오탈자 없음
□ 문법 정확
□ 톤앤매너 일관성
□ 금지 표현 미사용
```

### 랜딩페이지

```
□ 3초 내 가치 제안 파악
□ 단일 CTA에 집중
□ Social Proof 포함
□ 폼 필드 최소화
□ 모바일 반응형
□ 로딩 3초 이하
□ 트래킹 코드 설치
□ Thank You 페이지 설정
```

### 이메일

```
□ 제목줄 40자 이하
□ 프리뷰 텍스트 설정
□ 개인화 변수 정확
□ CTA 버튼 명확
□ 모바일 최적화
□ 수신거부 링크 포함
□ 발신자 정보 정확
□ A/B 테스트 준비
```

### 광고

```
□ 규격 준수
□ 텍스트 비율 적절 (Meta)
□ 랜딩페이지 일치
□ 타겟팅 설정 완료
□ 예산 설정 완료
□ 일정 설정 완료
□ 트래킹 연결
```

## 워크플로우

```
1. 검토 대상 수집
      │
      ▼
2. 체크리스트 기반 검토
      │
      ▼
3. 이슈 분류 (Critical/Major/Minor)
      │
      ▼
4. 수정 사항 정리
      │
      ▼
5. 검토 리포트 작성
      │
      ▼
6. 문서 저장
   → workspace/work-marketing/reports/review-report.md
```

## 출력 템플릿

```markdown
# {Project Name} Marketing Review Report

## Review Summary

| 항목 | 내용 |
|------|------|
| 검토 대상 | {scope} |
| 검토자 | {reviewer} |
| 검토 날짜 | {date} |
| 전체 상태 | 🟢 Ready / 🟡 Minor Issues / 🔴 Major Issues |

### Overall Score

| 영역 | 점수 | 상태 |
|------|------|------|
| 브랜드 일관성 | {score}/10 | {status} |
| 콘텐츠 품질 | {score}/10 | {status} |
| 기술 검토 | {score}/10 | {status} |
| 컴플라이언스 | {score}/10 | {status} |
| **총점** | **{total}/40** | **{status}** |

---

## Issue Summary

| 심각도 | 개수 | 상태 |
|--------|------|------|
| 🔴 Critical | {count} | 필수 수정 |
| 🟠 Major | {count} | 권장 수정 |
| 🟡 Minor | {count} | 선택 수정 |

---

## Detailed Review

### 1. 브랜드 일관성

#### ✅ Pass

- {pass_item_1}
- {pass_item_2}

#### ❌ Issues

| ID | 심각도 | 항목 | 이슈 | 권고 |
|----|--------|------|------|------|
| B01 | 🔴 | {item} | {issue} | {recommendation} |
| B02 | 🟡 | {item} | {issue} | {recommendation} |

---

### 2. 콘텐츠 품질

#### ✅ Pass

- {pass_item_1}
- {pass_item_2}

#### ❌ Issues

| ID | 심각도 | 항목 | 이슈 | 권고 |
|----|--------|------|------|------|
| C01 | 🟠 | {item} | {issue} | {recommendation} |
| C02 | 🟡 | {item} | {issue} | {recommendation} |

---

### 3. 기술 검토

#### ✅ Pass

- {pass_item_1}
- {pass_item_2}

#### ❌ Issues

| ID | 심각도 | 항목 | 이슈 | 권고 |
|----|--------|------|------|------|
| T01 | 🔴 | {item} | {issue} | {recommendation} |

---

### 4. 컴플라이언스

#### ✅ Pass

- {pass_item_1}
- {pass_item_2}

#### ❌ Issues

| ID | 심각도 | 항목 | 이슈 | 권고 |
|----|--------|------|------|------|
| L01 | 🔴 | {item} | {issue} | {recommendation} |

---

## Asset-by-Asset Review

### Landing Page

| 체크 항목 | 상태 | 비고 |
|----------|------|------|
| 헤드라인 명확 | ✅/❌ | {note} |
| CTA 눈에 띔 | ✅/❌ | {note} |
| 모바일 최적화 | ✅/❌ | {note} |
| 로딩 속도 | ✅/❌ | {note} |
| 트래킹 설정 | ✅/❌ | {note} |

### Email Sequence

| 이메일 | 제목줄 | 본문 | CTA | 기술 |
|--------|--------|------|-----|------|
| Email 1 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Email 2 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| ... | ... | ... | ... | ... |

### Ads

| 광고 | 카피 | 규격 | 랜딩 연결 | 트래킹 |
|------|------|------|----------|--------|
| Google Ad 1 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| Meta Ad 1 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

---

## Action Items

### 🔴 Critical (필수 - 런칭 전 해결)

| # | 이슈 ID | 항목 | 담당 | 마감 |
|---|---------|------|------|------|
| 1 | {id} | {item} | {owner} | {deadline} |
| 2 | {id} | {item} | {owner} | {deadline} |

### 🟠 Major (권장 - 가능하면 해결)

| # | 이슈 ID | 항목 | 담당 | 마감 |
|---|---------|------|------|------|
| 1 | {id} | {item} | {owner} | {deadline} |

### 🟡 Minor (선택 - 시간 되면 해결)

| # | 이슈 ID | 항목 | 담당 | 마감 |
|---|---------|------|------|------|
| 1 | {id} | {item} | {owner} | {deadline} |

---

## Sign-off

### 런칭 승인

- [ ] Critical 이슈 모두 해결
- [ ] Major 이슈 해결 또는 승인된 예외
- [ ] 팀 리뷰 완료
- [ ] 최종 승인

### 승인자

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| 마케팅 | {name} | ⬜ | {date} |
| 법무 | {name} | ⬜ | {date} |
| 경영진 | {name} | ⬜ | {date} |

---

## Notes

{additional_notes}

---

*Review Version: {version}*
*Created: {date}*
*Last Updated: {update_date}*
```

## 이슈 심각도 정의

| 심각도 | 정의 | 예시 |
|--------|------|------|
| 🔴 Critical | 런칭 불가, 법적 리스크, 브랜드 손상 | 잘못된 가격, 저작권 침해, 링크 오류 |
| 🟠 Major | 성과 저하 예상, 사용자 경험 저하 | CTA 불명확, 모바일 깨짐, 오탈자 |
| 🟡 Minor | 개선 권장, 성과에 큰 영향 없음 | 여백 불균형, 미세 디자인 |

## 다음 단계

검토 완료 후:

1. **모든 Critical 해결** → 런칭 승인
2. **Major 검토** → 수정 또는 예외 승인
3. **Minor 정리** → 백로그 등록

---

*런칭 전 검토는 실수를 예방하는 마지막 방어선입니다.*
*한 번 나간 것은 되돌리기 어렵습니다.*
