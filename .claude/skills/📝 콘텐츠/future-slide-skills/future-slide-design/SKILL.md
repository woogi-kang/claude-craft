---
name: future-slide-design
description: "Future Slide HTML 덱의 폰트, 컬러, 레이아웃 밀도, 한국어 줄바꿈, 이미지 사용 원칙을 정하는 디자인 가드레일."
argument-hint: "[deck-context]"
metadata:
  category: "📝 콘텐츠"
  version: "0.1.0"
  tags: "presentation, typography, korean, future-slide, design-system"
  author: "woogi"
---

# Future Slide Design

Future Slide 덱을 만들기 전에 적용하는 디자인 가드레일입니다.

## 기본 원칙

- Future Slide template의 locked layout을 유지합니다.
- 하나의 덱에는 하나의 accent color만 사용합니다.
- 장식용 gradient, shadow, glass, rounded-card 남발은 피합니다.
- 정보형 덱은 차분하고 밀도 있게, 브랜드/제품 덱은 이미지 slot을 더 적극적으로 사용합니다.

## 한국어 타이포그래피

기본 선택:
- 제목/본문: `SUIT`, `Pretendard`, `Noto Sans KR`
- 영문 보조: `Inter`
- 코드/숫자 보조: `JetBrains Mono`, 단 표/라벨에만 제한적으로 사용

규칙:
- 한국어 display heading은 의미 단위로 `<br>`을 명시합니다.
- `word-break: break-all`, `overflow-wrap:anywhere`로 한국어 제목을 억지로 맞추지 않습니다.
- 본문은 2-4줄 단위로 짧게 나누고, 한 줄에 너무 긴 복합명사를 넣지 않습니다.
- 숫자와 `%` 표기는 letter spacing을 넓히지 않습니다.
- 작은 라벨은 mono를 써도 되지만, 긴 한국어 문장에는 mono를 쓰지 않습니다.

## Layout 밀도

- 7-8장 덱은 최소 6개 이상의 Sxx layout을 사용합니다.
- S03/S09/S10 같은 statement layout은 핵심 전환점에만 사용합니다.
- 표/카드/매트릭스는 S04/S15/S16/S19/S20 안에서 처리합니다.
- 긴 본문을 한 슬라이드에 밀어 넣지 말고 S16 brief, S19 cards, S20 ledger로 분산합니다.

## 이미지 사용

- 전체 슬라이드를 이미지로 만들지 않습니다. 텍스트는 HTML 레이어에 둡니다.
- 생성 이미지는 텍스트 없는 hero visual, diagram base, icon, texture, object illustration로 제한합니다.
- S22는 21:9 hero, S15/S16은 21:9 또는 16:10 slot을 우선 사용합니다.
- 이미지 prompt에는 "no text, no letters, no numbers, no UI labels"를 기본으로 넣습니다.
- 이미지 파일마다 alt text와 `data-image-slot`을 기록합니다.

## 기존 디자인 시스템과의 관계

필요하면 기존 PPT 디자인 시스템을 먼저 참고합니다.

```text
.claude/skills/📝 콘텐츠/presentation-agent-skills/5-design-system/
.claude/skills/design-system/data/slide-typography.csv
.claude/skills/design-system/data/slide-layouts.csv
```

Future Slide는 HTML locked layout을 우선하되, 브랜드 색상/폰트/톤은 기존 디자인 시스템의 결정을 재사용합니다.
