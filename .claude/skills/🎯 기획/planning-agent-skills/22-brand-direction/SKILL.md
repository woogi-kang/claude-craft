---
name: plan-brand-direction
description: |
  브랜딩 방향을 정의하는 스킬.
  브랜드 톤앤매너, 키워드, 성격을 설정합니다.
triggers:
  - "브랜드 방향"
  - "브랜딩"
  - "톤앤매너"
  - "브랜드 가이드"
input:
  - target-user.md 결과
  - value-proposition.md 결과
output:
  - 06-design/brand-direction.md
---

# Brand Direction Skill

브랜드의 성격, 톤앤매너, 시각적 방향을 정의합니다.

## 출력 템플릿

```markdown
# {Project Name} - 브랜드 방향

## 1. 브랜드 에센스

### 브랜드 미션

> **"{brand_mission}"**

### 브랜드 비전

> **"{brand_vision}"**

### 핵심 가치

| 가치 | 의미 | 표현 |
|------|------|------|
| {value_1} | {meaning} | {expression} |
| {value_2} | {meaning} | {expression} |
| {value_3} | {meaning} | {expression} |

---

## 2. 브랜드 퍼스낼리티

### 브랜드 성격

> **{brand_name}은(는) {personality_summary}.**

### 성격 키워드

| 키워드 | 설명 | 강도 |
|--------|------|------|
| {keyword_1} | {description} | ⭐⭐⭐⭐⭐ |
| {keyword_2} | {description} | ⭐⭐⭐⭐ |
| {keyword_3} | {description} | ⭐⭐⭐ |

### 성격 스펙트럼

```
친근함 ●────────────○ 권위적
혁신적 ●────────────○ 전통적
캐주얼 ●────────────○ 포멀
대담함 ●────────────○ 절제됨
유머러스 ●────────────○ 진지함
```

### Brand Archetype

| Archetype | 설명 | 적합도 |
|-----------|------|--------|
| {archetype_1} | {description} | ⭐⭐⭐⭐⭐ |
| {archetype_2} | {description} | ⭐⭐⭐ |

---

## 3. 톤앤매너

### Voice

> **{brand_name}의 목소리는 {voice_description}.**

| 특성 | Do ✅ | Don't ❌ |
|------|-------|---------|
| {trait_1} | {do_1} | {dont_1} |
| {trait_2} | {do_2} | {dont_2} |
| {trait_3} | {do_3} | {dont_3} |

### Tone 가이드

| 상황 | 톤 | 예시 |
|------|-----|------|
| 환영 | {tone} | "{example}" |
| 성공 | {tone} | "{example}" |
| 에러 | {tone} | "{example}" |
| 안내 | {tone} | "{example}" |

### 카피라이팅 원칙

1. **{principle_1}**: {description}
2. **{principle_2}**: {description}
3. **{principle_3}**: {description}

### 예시 카피

**Headline**
- ✅ "{good_example}"
- ❌ "{bad_example}"

**CTA**
- ✅ "{good_cta}"
- ❌ "{bad_cta}"

**에러 메시지**
- ✅ "{good_error}"
- ❌ "{bad_error}"

---

## 4. 시각적 방향

### 무드보드 키워드

```
{keyword_1} | {keyword_2} | {keyword_3} | {keyword_4}
```

### 색상 방향

| 역할 | 색상 계열 | 느낌 |
|------|----------|------|
| Primary | {color_family} | {feeling} |
| Secondary | {color_family} | {feeling} |
| Accent | {color_family} | {feeling} |
| Neutral | {color_family} | {feeling} |

### 타이포그래피 방향

| 용도 | 스타일 | 예시 |
|------|--------|------|
| 헤드라인 | {style} | {font_example} |
| 본문 | {style} | {font_example} |
| 강조 | {style} | {font_example} |

### 이미지 스타일

| 요소 | 스타일 | 예시 |
|------|--------|------|
| 사진 | {style} | {description} |
| 일러스트 | {style} | {description} |
| 아이콘 | {style} | {description} |

---

## 5. 브랜드 경쟁 포지션

### 경쟁사 대비 포지셔닝

```
            혁신적
               │
       {Comp_A}│{Us}
    ─────────────────────
       {Comp_B}│{Comp_C}
               │
            전통적

           접근성 ← → 프리미엄
```

### 차별화 포인트

| 경쟁사 | 그들의 브랜드 | 우리의 차별점 |
|--------|-------------|--------------|
| {comp_1} | {their_brand} | {our_diff} |
| {comp_2} | {their_brand} | {our_diff} |

---

## 6. 브랜드 표현

### 네이밍 가이드

| 요소 | 이름 | 발음 | 의미 |
|------|------|------|------|
| 서비스명 | {name} | {pronunciation} | {meaning} |
| 태그라인 | {tagline} | - | {meaning} |

### 로고 방향

| 요소 | 방향 | 예시/레퍼런스 |
|------|------|-------------|
| 형태 | {shape} | {reference} |
| 스타일 | {style} | {reference} |
| 느낌 | {feeling} | {reference} |

### 브랜드 요소

| 요소 | 설명 | 활용 |
|------|------|------|
| 마스코트 | {description} | {usage} |
| 패턴 | {description} | {usage} |
| 모션 | {description} | {usage} |

---

## 7. 브랜드 적용

### 터치포인트별 적용

| 터치포인트 | 브랜드 요소 | 주의사항 |
|-----------|-----------|---------|
| 웹사이트 | 로고, 색상, 톤 | {note} |
| 앱 | 아이콘, 마이크로카피 | {note} |
| 이메일 | 로고, 서명 | {note} |
| 소셜미디어 | 프로필, 콘텐츠 톤 | {note} |

### 일관성 체크리스트

- [ ] 로고 사용 가이드 준수
- [ ] 색상 팔레트 준수
- [ ] 톤앤매너 일관성
- [ ] 타이포그래피 일관성

---

## 8. 브랜드 금지사항

### Don'ts

| 금지 | 이유 | 대안 |
|------|------|------|
| {dont_1} | {reason} | {alternative} |
| {dont_2} | {reason} | {alternative} |
| {dont_3} | {reason} | {alternative} |

### 피해야 할 표현

- ❌ "{avoid_1}"
- ❌ "{avoid_2}"
- ❌ "{avoid_3}"

---

## 9. 레퍼런스

### 영감받은 브랜드

| 브랜드 | 참고 요소 | 적용 방법 |
|--------|----------|----------|
| {brand_1} | {element} | {application} |
| {brand_2} | {element} | {application} |
| {brand_3} | {element} | {application} |

### 무드보드 이미지

(디자이너와 공유할 레퍼런스 이미지 목록)

---

## 10. 다음 단계

### 브랜드 개발 로드맵

| 단계 | 산출물 | 담당 |
|------|--------|------|
| 1 | 로고 디자인 | 디자이너 |
| 2 | 색상 팔레트 확정 | 디자이너 |
| 3 | 타이포그래피 확정 | 디자이너 |
| 4 | 브랜드 가이드라인 | 디자이너 |
| 5 | 적용 및 검증 | 전체 |

### 디자이너 전달 사항

**핵심 요청**
1. {request_1}
2. {request_2}
3. {request_3}

**참고 자료**
- 이 문서
- target-user.md
- value-proposition.md

---

*다음 단계: Roadmap → Risk Management*
```

## 퀄리티 체크리스트

```
□ 브랜드 미션/비전이 명확한가?
□ 퍼스낼리티가 구체적인가?
□ 톤앤매너 예시가 있는가?
□ 시각적 방향이 정의되었는가?
□ 경쟁사 대비 포지셔닝이 있는가?
□ 금지사항이 명시되었는가?
□ 레퍼런스가 제공되었는가?
```

## 다음 스킬 연결

Brand Direction 완료 후:

1. **로드맵** → Roadmap Skill
2. **실제 디자인** → Frontend Design Agent 연계
3. **브랜드 가이드** → 디자이너 작업

---

*브랜드는 로고가 아니라 약속입니다. 일관되게 지키세요.*
