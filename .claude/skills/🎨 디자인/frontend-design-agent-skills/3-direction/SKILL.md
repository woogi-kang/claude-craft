---
name: fd-direction
description: |
  12가지 미적 방향(Aesthetic Direction) 템플릿을 기반으로 프로젝트의 디자인 방향을 결정합니다.
  컨텍스트와 인스피레이션을 바탕으로 최적의 스타일을 선택하고 조합합니다.
triggers:
  - "미적 방향"
  - "디자인 방향"
  - "스타일"
  - "에스테틱"
  - "aesthetic"
  - "direction"
input:
  - 프로젝트 컨텍스트 (1-context 결과물)
  - 인스피레이션/무드보드 (2-inspiration 결과물, 선택)
output:
  - workspace/work-design/{project}/direction/aesthetic-direction.md
  - workspace/work-design/{project}/direction/decision-rationale.md
---

# Aesthetic Direction Skill

디자인의 성공은 **일관된 미적 방향**에서 시작됩니다.
이 스킬은 12가지 검증된 미적 방향 중 프로젝트에 최적화된 스타일을 선택하고 조합하는 것을 돕습니다.

## 왜 중요한가?

```
미적 방향 없이 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"그냥 예쁘게" → 일관성 없는 혼란

미적 방향 기반 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
명확한 Direction → 일관된 시스템 → 통일감 있는 결과물
```

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| 프로젝트 컨텍스트 | Y | 1-context 스킬 결과물 |
| 인스피레이션 | N | 2-inspiration 스킬 결과물 |
| 선호 스타일 힌트 | N | 사용자가 언급한 스타일 키워드 |

---

## 12 Aesthetic Directions

### 1. Barely-There Minimal

```yaml
name: "Barely-There Minimal"
korean: "거의 없는 미니멀"
tagline: "존재감을 지우는 극단적 절제"

description: |
  콘텐츠만 남기고 모든 장식을 제거합니다.
  UI는 배경으로 물러나고, 콘텐츠가 말합니다.
  Apple, Notion의 극한 미니멀리즘.

visual_characteristics:
  colors: "모노톤 (검정/흰색/회색), 단일 액센트"
  typography: "가변 산세리프, 극단적 크기 대비"
  spacing: "과감한 여백, 호흡하는 레이아웃"
  shapes: "직선, 최소 border-radius (0-4px)"
  imagery: "거의 없음, 있다면 흑백"
  effects: "그림자 없음, 경계선 최소화"

interaction:
  hover: "미묘한 색상 변화"
  transitions: "느리고 우아함 (300-500ms)"
  feedback: "최소한의 상태 표시"

best_for:
  - "고급 포트폴리오"
  - "디자인 에이전시"
  - "럭셔리 브랜드"
  - "콘텐츠 중심 사이트"

avoid_for:
  - "게이미피케이션 앱"
  - "어린이 대상"
  - "정보 과밀 대시보드"

references:
  - { name: "Apple", url: "apple.com" }
  - { name: "Notion", url: "notion.so" }
  - { name: "Aesop", url: "aesop.com" }

tailwind_hints:
  - "bg-white text-black"
  - "font-light tracking-tight"
  - "py-24 md:py-40"
  - "border-transparent hover:border-black"
```

---

### 2. Soft Maximalism

```yaml
name: "Soft Maximalism"
korean: "부드러운 맥시멀리즘"
tagline: "풍성하지만 우아한 레이어링"

description: |
  다양한 요소를 사용하지만 조화롭게 배치합니다.
  색상, 텍스처, 레이어가 풍부하지만 혼란스럽지 않습니다.
  Airbnb의 따뜻함과 풍성함.

visual_characteristics:
  colors: "따뜻한 중성색 기반 + 다양한 톤"
  typography: "혼합 (세리프 헤딩 + 산세리프 본문)"
  spacing: "적당한 여백, 그룹핑으로 정리"
  shapes: "다양한 radius (8-24px)"
  imagery: "풍부한 사진, 일러스트 혼용"
  effects: "부드러운 그림자, 미묘한 그라데이션"

interaction:
  hover: "확대, 색상 전환"
  transitions: "자연스럽고 탄성 있음"
  feedback: "친근한 마이크로인터랙션"

best_for:
  - "라이프스타일 브랜드"
  - "여행/숙박"
  - "음식/레스토랑"
  - "이커머스 (패션, 인테리어)"

avoid_for:
  - "테크/개발자 도구"
  - "B2B SaaS"
  - "금융/핀테크"

references:
  - { name: "Airbnb", url: "airbnb.com" }
  - { name: "Pinterest", url: "pinterest.com" }
  - { name: "Anthropologie", url: "anthropologie.com" }

tailwind_hints:
  - "bg-amber-50 text-stone-800"
  - "font-serif + font-sans"
  - "rounded-2xl shadow-lg"
  - "hover:scale-105 transition-transform"
```

---

### 3. Anti-Design Chaos

```yaml
name: "Anti-Design Chaos"
korean: "안티-디자인 카오스"
tagline: "규칙을 깨는 의도적 불협화음"

description: |
  전통적 디자인 원칙을 의도적으로 위반합니다.
  비대칭, 충돌하는 요소, 예측 불가능한 레이아웃.
  Balenciaga, 브루탈리즘의 극단.

visual_characteristics:
  colors: "충돌하는 색상, 네온, 비비드"
  typography: "다양한 크기/폰트 혼용, 회전, 겹침"
  spacing: "불규칙, 의도적 불균형"
  shapes: "비대칭, 찌그러진 형태"
  imagery: "콜라주, 글리치, 노이즈"
  effects: "과한 그림자, 이상한 블렌드 모드"

interaction:
  hover: "과격한 변형"
  transitions: "불규칙하거나 없음"
  feedback: "예상 밖의 반응"

best_for:
  - "패션/하이엔드 브랜드"
  - "음악/엔터테인먼트"
  - "아트 갤러리"
  - "실험적 프로젝트"

avoid_for:
  - "기업 사이트"
  - "헬스케어"
  - "교육"
  - "접근성 중요 프로젝트"

references:
  - { name: "Balenciaga", url: "balenciaga.com" }
  - { name: "Bloomberg Businessweek", url: "businessweek.com" }

tailwind_hints:
  - "rotate-3 -translate-x-2"
  - "mix-blend-multiply"
  - "text-[200px] leading-none"
  - "absolute -top-10 -left-5"
```

---

### 4. Liquid Glass

```yaml
name: "Liquid Glass"
korean: "리퀴드 글래스"
tagline: "투명하고 흐르는 글래스모피즘"

description: |
  반투명 유리 효과와 부드러운 블러가 특징입니다.
  iOS의 글래스모피즘을 웹에 적용.
  고급스럽고 현대적인 느낌.

visual_characteristics:
  colors: "그라데이션 배경 + 반투명 레이어"
  typography: "산세리프, 적당한 굵기"
  spacing: "여유로운 패딩"
  shapes: "둥근 모서리 (16-32px)"
  imagery: "추상적 그라데이션, 블러 배경"
  effects: "backdrop-blur, 미묘한 테두리"

interaction:
  hover: "불투명도 변화, 글로우"
  transitions: "부드럽고 연속적"
  feedback: "리플 효과, 광택"

best_for:
  - "금융/핀테크 앱"
  - "대시보드"
  - "iOS/macOS 스타일"
  - "SaaS 인터페이스"

avoid_for:
  - "저사양 기기 타겟"
  - "콘텐츠 밀집 사이트"
  - "접근성 최우선 프로젝트"

references:
  - { name: "Linear", url: "linear.app" }
  - { name: "Clerk", url: "clerk.com" }
  - { name: "Apple Music", url: "music.apple.com" }

tailwind_hints:
  - "bg-white/10 backdrop-blur-xl"
  - "border border-white/20"
  - "rounded-3xl"
  - "shadow-2xl shadow-black/5"
```

---

### 5. Editorial Magazine

```yaml
name: "Editorial Magazine"
korean: "에디토리얼 매거진"
tagline: "인쇄물의 품격을 웹으로"

description: |
  고급 잡지의 레이아웃과 타이포그래피를 웹에 적용합니다.
  세리프 폰트, 컬럼 그리드, 큰 이미지.
  Vogue, NYT 매거진의 우아함.

visual_characteristics:
  colors: "클래식 (검정, 흰색, 단일 액센트)"
  typography: "세리프 헤딩, 다양한 크기 대비"
  spacing: "텍스트 블록 기반, 컬럼 구조"
  shapes: "직선적, 최소 radius"
  imagery: "대형 고품질 사진, 크롭"
  effects: "거의 없음, 순수한 타이포"

interaction:
  hover: "밑줄, 색상 전환"
  transitions: "미묘하고 우아함"
  feedback: "텍스트 기반"

best_for:
  - "미디어/뉴스"
  - "블로그/콘텐츠 플랫폼"
  - "럭셔리 브랜드"
  - "포트폴리오"

avoid_for:
  - "데이터 중심 앱"
  - "게이미피케이션"
  - "복잡한 인터랙션"

references:
  - { name: "The New York Times", url: "nytimes.com" }
  - { name: "Stripe Press", url: "press.stripe.com" }
  - { name: "Hodinkee", url: "hodinkee.com" }

tailwind_hints:
  - "font-serif text-4xl leading-tight"
  - "grid grid-cols-12 gap-6"
  - "prose prose-lg"
  - "border-b border-black"
```

---

### 6. Retro-Futuristic

```yaml
name: "Retro-Futuristic"
korean: "레트로-퓨처리스틱"
tagline: "과거가 상상한 미래"

description: |
  80-90년대 SF의 미래 비전을 현대적으로 해석합니다.
  네온, 그리드, 신스웨이브, 사이버펑크.
  Blade Runner, Tron의 미학.

visual_characteristics:
  colors: "어두운 배경 + 네온 (핑크, 시안, 퍼플)"
  typography: "기하학적 산세리프, 글로우 효과"
  spacing: "그리드 기반, 기하학적"
  shapes: "직선, 기하학, 그리드 패턴"
  imagery: "3D 그리드, 네온, 홀로그램"
  effects: "글로우, 스캔라인, 그라데이션"

interaction:
  hover: "글로우 강화, 스케일"
  transitions: "빠르고 기계적"
  feedback: "빛 효과"

best_for:
  - "게임/엔터테인먼트"
  - "크립토/Web3"
  - "음악/DJ"
  - "테크 이벤트"

avoid_for:
  - "헬스케어"
  - "어린이/교육"
  - "기업/금융"

references:
  - { name: "Poolsuite", url: "poolsuite.net" }
  - { name: "Daft Punk", url: "daftpunk.com" }

tailwind_hints:
  - "bg-slate-950 text-cyan-400"
  - "shadow-[0_0_20px_rgba(0,255,255,0.5)]"
  - "font-mono tracking-widest"
  - "border border-cyan-500/50"
```

---

### 7. Organic Natural

```yaml
name: "Organic Natural"
korean: "오가닉 내추럴"
tagline: "자연에서 온 부드러운 형태"

description: |
  자연에서 영감받은 유기적 곡선과 색상입니다.
  불규칙한 blob, 식물적 이미지, 흙빛 톤.
  웰니스, 지속가능성의 미학.

visual_characteristics:
  colors: "어스 톤 (베이지, 올리브, 테라코타)"
  typography: "인간적인 산세리프, 손글씨 액센트"
  spacing: "여유로운, 비대칭 밸런스"
  shapes: "불규칙 blob, 유기적 곡선"
  imagery: "자연 사진, 질감, 식물"
  effects: "텍스처, 종이 질감, 노이즈"

interaction:
  hover: "부드러운 변형"
  transitions: "천천히, 자연스럽게"
  feedback: "파동, 성장 애니메이션"

best_for:
  - "웰니스/뷰티"
  - "오가닉 제품"
  - "ESG/지속가능성"
  - "요가/명상 앱"

avoid_for:
  - "테크/AI"
  - "금융/핀테크"
  - "B2B SaaS"

references:
  - { name: "Headspace", url: "headspace.com" }
  - { name: "Patagonia", url: "patagonia.com" }
  - { name: "The Ordinary", url: "theordinary.com" }

tailwind_hints:
  - "bg-stone-100 text-stone-800"
  - "rounded-[40%_60%_70%_30%/40%_50%_60%_50%]"
  - "font-normal tracking-normal"
  - "opacity-90 hover:opacity-100"
```

---

### 8. Luxury Refined

```yaml
name: "Luxury Refined"
korean: "럭셔리 리파인드"
tagline: "절제된 고급스러움"

description: |
  최소한의 요소로 최대의 고급스러움을 표현합니다.
  검정, 금, 세리프, 넓은 여백.
  Chanel, Rolex의 우아함.

visual_characteristics:
  colors: "검정, 흰색, 금/크림 액센트"
  typography: "우아한 세리프, 넓은 자간"
  spacing: "과감한 여백"
  shapes: "정제된 직선, 최소 radius"
  imagery: "고급 제품 사진, 흑백"
  effects: "미묘한 그라데이션, 금속 질감"

interaction:
  hover: "우아한 페이드"
  transitions: "느리고 품격 있게"
  feedback: "최소한, 정제된"

best_for:
  - "럭셔리 브랜드"
  - "호텔/리조트"
  - "주얼리/시계"
  - "프리미엄 서비스"

avoid_for:
  - "스타트업/테크"
  - "젊은 타겟"
  - "가격 민감 시장"

references:
  - { name: "Rolex", url: "rolex.com" }
  - { name: "Bottega Veneta", url: "bottegaveneta.com" }
  - { name: "Aman Resorts", url: "aman.com" }

tailwind_hints:
  - "bg-black text-white"
  - "font-serif tracking-[0.3em] uppercase"
  - "py-32"
  - "border-b border-gold/20"
```

---

### 9. Tech Documentation

```yaml
name: "Tech Documentation"
korean: "테크 도큐멘테이션"
tagline: "개발자를 위한 명확한 정보 전달"

description: |
  문서화 우선, 기능 중심의 인터페이스입니다.
  코드 블록, 사이드바, 검색 강조.
  Stripe Docs, Vercel의 개발자 경험.

visual_characteristics:
  colors: "다크 모드 기본, 구문 강조 색상"
  typography: "모노스페이스 + 클린 산세리프"
  spacing: "정보 밀도 높음, 그리드 정렬"
  shapes: "직선적, 작은 radius"
  imagery: "다이어그램, 코드, 스키마"
  effects: "코드 하이라이트, 호버 팁"

interaction:
  hover: "빠른 피드백"
  transitions: "즉각적"
  feedback: "복사, 토글, 상태 표시"

best_for:
  - "개발자 도구"
  - "API/SDK 문서"
  - "오픈소스 프로젝트"
  - "테크 블로그"

avoid_for:
  - "일반 소비자"
  - "감성적 브랜딩"
  - "크리에이티브 분야"

references:
  - { name: "Stripe Docs", url: "stripe.com/docs" }
  - { name: "Vercel Docs", url: "vercel.com/docs" }
  - { name: "Tailwind CSS", url: "tailwindcss.com" }

tailwind_hints:
  - "bg-slate-900 text-slate-100"
  - "font-mono text-sm"
  - "prose-pre:bg-slate-800"
  - "sticky top-0"
```

---

### 10. Brutalist Raw

```yaml
name: "Brutalist Raw"
korean: "브루탈리스트 로우"
tagline: "꾸미지 않은 원시적 힘"

description: |
  디자인 장식을 거부하고 기능에 집중합니다.
  시스템 폰트, 기본 HTML, 의도적 투박함.
  90년대 웹의 순수함을 현대적으로.

visual_characteristics:
  colors: "검정, 흰색, 원색 (필요시)"
  typography: "시스템 폰트, 기본 스타일"
  spacing: "기능적 최소"
  shapes: "없음, 직선 경계"
  imagery: "최소, 있다면 원본 그대로"
  effects: "없음"

interaction:
  hover: "밑줄, 색상 반전"
  transitions: "없거나 최소"
  feedback: "기본 브라우저 피드백"

best_for:
  - "실험적 프로젝트"
  - "아티스트/디자이너"
  - "스타트업 초기"
  - "속도 최우선"

avoid_for:
  - "기업 브랜딩"
  - "럭셔리"
  - "신뢰가 중요한 분야"

references:
  - { name: "Craigslist", url: "craigslist.org" }
  - { name: "Berkshire Hathaway", url: "berkshirehathaway.com" }
  - { name: "Hacker News", url: "news.ycombinator.com" }

tailwind_hints:
  - "font-mono text-black bg-white"
  - "border border-black"
  - "p-2"
  - "hover:bg-black hover:text-white"
```

---

### 11. Playful Rounded

```yaml
name: "Playful Rounded"
korean: "플레이풀 라운디드"
tagline: "친근하고 접근하기 쉬운"

description: |
  둥근 모서리, 밝은 색상, 친근한 일러스트.
  Duolingo, Notion의 접근성.
  부담 없이 사용할 수 있는 인터페이스.

visual_characteristics:
  colors: "밝고 부드러운 색상, 파스텔"
  typography: "둥근 산세리프, 친근한"
  spacing: "넉넉하고 숨쉬는"
  shapes: "큰 border-radius (16-32px), pill"
  imagery: "친근한 일러스트, 이모지"
  effects: "부드러운 그림자, 바운스"

interaction:
  hover: "스케일 업, 바운스"
  transitions: "탄성 있고 재미있음"
  feedback: "이모지, 애니메이션"

best_for:
  - "교육 플랫폼"
  - "생산성 도구"
  - "소비자 앱"
  - "젊은 타겟"

avoid_for:
  - "금융/보험"
  - "럭셔리"
  - "시니어 타겟"

references:
  - { name: "Duolingo", url: "duolingo.com" }
  - { name: "Notion", url: "notion.so" }
  - { name: "Linear", url: "linear.app" }

tailwind_hints:
  - "bg-violet-50 text-violet-900"
  - "rounded-2xl"
  - "shadow-xl shadow-violet-500/10"
  - "hover:scale-105 transition-transform"
```

---

### 12. Grade-School Bold

```yaml
name: "Grade-School Bold"
korean: "그레이드 스쿨 볼드"
tagline: "어린이처럼 대담하고 자유롭게"

description: |
  크레용, 손글씨, 불규칙한 형태의 즐거움.
  어린이 교육이나 창의적 브랜드에 적합.
  규칙을 깨지만 Anti-Design보다 친근함.

visual_characteristics:
  colors: "원색, 크레용 색상, 비비드"
  typography: "손글씨, 기울어진, 다양한 크기"
  spacing: "불규칙하지만 의도적"
  shapes: "손으로 그린 듯한 불규칙"
  imagery: "일러스트, 손그림 스타일"
  effects: "종이 질감, 크레용 텍스처"

interaction:
  hover: "흔들림, 회전"
  transitions: "예측 불가, 재미있음"
  feedback: "과장된 애니메이션"

best_for:
  - "어린이 교육"
  - "창의적 도구"
  - "게임"
  - "재미있는 브랜드"

avoid_for:
  - "기업/B2B"
  - "금융/의료"
  - "전문 서비스"

references:
  - { name: "Yoast", url: "yoast.com" }
  - { name: "MailChimp (old)", url: "-" }

tailwind_hints:
  - "rotate-[-2deg]"
  - "font-comic bg-yellow-300"
  - "border-4 border-black"
  - "hover:rotate-2 transition-transform"
```

---

## Decision Matrix

### 산업/타입별 추천

| 산업/타입 | 1순위 | 2순위 | 피해야 할 것 |
|----------|-------|-------|-------------|
| **SaaS/B2B** | Tech Docs, Minimal | Liquid Glass | Anti-Design, Grade-School |
| **이커머스 (패션)** | Soft Max, Luxury | Editorial | Brutalist, Tech Docs |
| **이커머스 (테크)** | Minimal, Liquid | Tech Docs | Organic, Luxury |
| **핀테크** | Liquid Glass, Minimal | Tech Docs | Anti-Design, Playful |
| **헬스케어** | Organic, Minimal | Soft Max | Anti-Design, Retro-Future |
| **에듀테크** | Playful, Grade-School | Soft Max | Luxury, Anti-Design |
| **Web3/크립토** | Retro-Future, Liquid | Anti-Design | Organic, Luxury |
| **에이전시** | Anti-Design, Minimal | Editorial | Brutalist, Grade-School |
| **포트폴리오** | Minimal, Editorial | Anti-Design | Playful, Grade-School |
| **미디어/블로그** | Editorial, Minimal | Soft Max | Anti-Design, Retro-Future |
| **웰니스** | Organic, Soft Max | Playful | Tech Docs, Brutalist |
| **럭셔리** | Luxury, Minimal | Editorial | Playful, Brutalist |

### 브랜드 톤별 추천

| 브랜드 톤 | 추천 Direction |
|----------|---------------|
| 전문적/신뢰감 | Minimal, Liquid Glass, Tech Docs |
| 친근한/접근성 | Playful, Soft Max, Organic |
| 혁신적/미래지향 | Retro-Future, Liquid Glass |
| 고급스러운 | Luxury, Editorial, Minimal |
| 재미있는/젊은 | Playful, Grade-School, Anti-Design |
| 자연적/지속가능 | Organic, Soft Max |
| 대담한/도전적 | Anti-Design, Brutalist |
| 클래식/우아한 | Editorial, Luxury |

### 사용자 기술 친숙도별 추천

| 기술 친숙도 | 추천 | 피해야 할 것 |
|------------|------|-------------|
| 높음 (개발자) | Tech Docs, Brutalist, Minimal | Grade-School, Soft Max |
| 중간 (일반 성인) | Liquid Glass, Minimal, Soft Max | Brutalist, Anti-Design |
| 낮음/시니어 | Playful, Soft Max, Minimal | Anti-Design, Tech Docs |
| 어린이 | Grade-School, Playful | Minimal, Luxury |

---

## Combination Strategies

### 유효한 조합

```yaml
valid_combinations:
  minimal_plus_liquid:
    primary: "Barely-There Minimal"
    secondary: "Liquid Glass"
    how: "레이아웃은 미니멀, 카드/모달만 글래스"
    example: "Linear, Raycast"

  editorial_plus_luxury:
    primary: "Editorial Magazine"
    secondary: "Luxury Refined"
    how: "타이포는 에디토리얼, 컬러/여백은 럭셔리"
    example: "Hodinkee, Stripe Press"

  organic_plus_soft_max:
    primary: "Organic Natural"
    secondary: "Soft Maximalism"
    how: "형태는 오가닉, 레이어링은 소프트"
    example: "Headspace"

  tech_docs_plus_minimal:
    primary: "Tech Documentation"
    secondary: "Barely-There Minimal"
    how: "문서 구조는 Tech, 여백/청결함은 미니멀"
    example: "Stripe Docs"

  playful_plus_liquid:
    primary: "Playful Rounded"
    secondary: "Liquid Glass"
    how: "둥근 형태에 글래스 효과"
    example: "Clerk, Notion"
```

### 피해야 할 조합

```yaml
avoid_combinations:
  - ["Brutalist Raw", "Luxury Refined"]        # 철학 충돌
  - ["Anti-Design Chaos", "Tech Documentation"]  # 가독성 저하
  - ["Grade-School Bold", "Luxury Refined"]      # 타겟 충돌
  - ["Retro-Futuristic", "Organic Natural"]     # 미학 충돌
```

---

## Workflow

```
1. 컨텍스트 로드
   ├── context/project-context.md
   └── inspiration/mood-board.md (있다면)
        │
        ▼
2. 핵심 요소 추출
   ├── 산업군
   ├── 타겟 사용자
   ├── 브랜드 톤
   └── 우선순위 (전환 vs 미적 vs 사용성)
        │
        ▼
3. Decision Matrix 적용
   └── 산업별 + 톤별 + 사용자별 교차 분석
        │
        ▼
4. 1-3개 후보 Direction 선정
        │
        ▼
5. 각 후보에 대해 적합성 평가
   ├── 브랜드 적합성 (0-10)
   ├── 타겟 적합성 (0-10)
   ├── 기술 실현 가능성 (0-10)
   └── 차별화 점수 (0-10)
        │
        ▼
6. 최종 Direction 결정
   └── 단일 또는 조합
        │
        ▼
7. 상세 적용 가이드 생성
        │
        ▼
8. 문서화 및 저장
   ├── aesthetic-direction.md
   └── decision-rationale.md
```

## Output

### 출력 디렉토리 구조

```
workspace/work-design/{project}/
├── context/
│   └── project-context.md
├── inspiration/
│   ├── mood-board.md
│   └── trend-analysis.md
└── direction/
    ├── aesthetic-direction.md     # 선택된 방향
    └── decision-rationale.md      # 결정 근거
```

### Aesthetic Direction 출력 템플릿

```markdown
# {Project Name} Aesthetic Direction

> 결정일: {date}
> 기반 컨텍스트: context/project-context.md

## 선택된 Direction

### Primary Direction
**{Direction Name}** - {Korean Name}

> {Tagline}

### Secondary Direction (해당시)
**{Direction Name}** - 적용 영역: {where_to_apply}

---

## 적용 가이드

### Colors

| 역할 | 값 | 적용 위치 |
|------|-----|----------|
| Background | {hex} | 전체 배경 |
| Foreground | {hex} | 텍스트 |
| Primary | {hex} | CTA, 강조 |
| Secondary | {hex} | 보조 요소 |
| Muted | {hex} | 비활성 상태 |

### Typography

| 역할 | 폰트 | 크기 | 무게 |
|------|------|------|------|
| Heading | {font} | {size} | {weight} |
| Body | {font} | {size} | {weight} |
| Caption | {font} | {size} | {weight} |

### Spacing

| 토큰 | 값 | 용도 |
|------|-----|------|
| xs | {value} | 내부 패딩 |
| sm | {value} | 요소 간격 |
| md | {value} | 섹션 내 |
| lg | {value} | 섹션 간 |
| xl | {value} | 히어로/대형 |

### Shapes

| 요소 | Border Radius | 참고 |
|------|---------------|------|
| Buttons | {value} | {note} |
| Cards | {value} | {note} |
| Inputs | {value} | {note} |
| Modals | {value} | {note} |

### Effects

| 효과 | CSS/Tailwind | 적용 위치 |
|------|-------------|----------|
| Shadow | {value} | 카드, 모달 |
| Blur | {value} | 글래스 요소 |
| Gradient | {value} | 배경 |

### Motion

| 타입 | Duration | Easing | 용도 |
|------|----------|--------|------|
| Hover | {ms} | {easing} | 버튼, 링크 |
| Enter | {ms} | {easing} | 모달, 토스트 |
| Page | {ms} | {easing} | 라우트 전환 |

---

## Tailwind 구성 힌트

\`\`\`javascript
// tailwind.config.js 참조 값
const theme = {
  colors: {
    background: "{hex}",
    foreground: "{hex}",
    primary: "{hex}",
    // ...
  },
  borderRadius: {
    sm: "{value}",
    md: "{value}",
    lg: "{value}",
  },
  // ...
}
\`\`\`

---

## 레퍼런스 사이트

| 사이트 | 참고 포인트 |
|--------|------------|
| {ref_1} | {what_to_learn} |
| {ref_2} | {what_to_learn} |

---

## 주의사항

- {caution_1}
- {caution_2}

---

*다음 단계: 4-typography (타이포그래피 시스템)*
```

### Decision Rationale 출력 템플릿

```markdown
# {Project Name} Direction Decision Rationale

> 결정일: {date}

## 핵심 요소 요약

| 요소 | 값 |
|------|-----|
| 산업군 | {industry} |
| 프로젝트 유형 | {type} |
| 타겟 사용자 | {target} |
| 브랜드 톤 | {tone_1}, {tone_2}, {tone_3} |
| 우선순위 | {priority} |

## 후보 Direction 평가

| Direction | 브랜드 적합 | 타겟 적합 | 기술 실현 | 차별화 | 총점 |
|-----------|------------|----------|----------|--------|------|
| {dir_1} | {score}/10 | {score}/10 | {score}/10 | {score}/10 | {total}/40 |
| {dir_2} | {score}/10 | {score}/10 | {score}/10 | {score}/10 | {total}/40 |
| {dir_3} | {score}/10 | {score}/10 | {score}/10 | {score}/10 | {total}/40 |

## 선택 이유

### 왜 {Chosen Direction}인가?

{detailed_reasoning}

### 왜 다른 것은 아닌가?

| Direction | 제외 이유 |
|-----------|----------|
| {rejected_1} | {reason} |
| {rejected_2} | {reason} |

## 조합 전략 (해당시)

{combination_strategy}

## 리스크 & 대응

| 리스크 | 대응 방안 |
|--------|----------|
| {risk_1} | {mitigation} |
| {risk_2} | {mitigation} |

---

*이 문서는 디자인 의사결정의 근거로 보존됩니다.*
```

## 퀄리티 체크리스트

```
□ 컨텍스트 기반 Decision Matrix 적용
□ 최소 2개 이상 후보 평가
□ 각 후보 점수화 (4개 기준)
□ 선택 이유 명확
□ 제외 이유 기록
□ 조합 전략 (해당시) 정의
□ 적용 가이드 상세 (Color, Type, Spacing, Shape, Motion)
□ Tailwind 힌트 포함
□ 리스크 & 대응 정리
```

## 다음 스킬 연결

Direction 결정 완료 후:

| 다음 스킬 | 조건 |
|-----------|------|
| **4-typography** | 타이포그래피 시스템 구축 (권장) |
| **5-color** | 컬러 시스템 정의 |
| **6-spacing** | 스페이싱 토큰 정의 |

---

*명확한 Direction은 수백 번의 의사결정을 단순화합니다. 처음에 잘 정하세요.*

---

## Template Quick Start 코드

각 Aesthetic Direction을 즉시 시작할 수 있는 Hero 컴포넌트 예제입니다.
모든 예제는 Next.js 15+ App Router, Tailwind CSS v4, Framer Motion을 기준으로 작성되었습니다.

### 사전 설정

```bash
# 폰트 설치 (Google Fonts 또는 next/font)
npm install @fontsource/satoshi @fontsource/clash-display @fontsource/basement-grotesque
npm install framer-motion
```

```typescript
// tailwind.config.ts - 폰트 확장 예시
import type { Config } from 'tailwindcss'

export default {
  theme: {
    extend: {
      fontFamily: {
        satoshi: ['Satoshi', 'sans-serif'],
        clash: ['Clash Display', 'sans-serif'],
        basement: ['Basement Grotesque', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        serif: ['GT Sectra', 'Georgia', 'serif'],
        display: ['Orbitron', 'sans-serif'],
        cormorant: ['Cormorant Garamond', 'serif'],
        didot: ['Didot', 'Playfair Display', 'serif'],
        nunito: ['Nunito', 'sans-serif'],
        albert: ['Albert Sans', 'sans-serif'],
      },
    },
  },
} satisfies Config
```

---

### 1. Barely-There Minimal

```tsx
// components/hero/BarelyThereMinimalHero.tsx
'use client'

import { motion } from 'framer-motion'

export function BarelyThereMinimalHero() {
  return (
    <section className="min-h-screen bg-white flex items-center justify-center px-6">
      <div className="max-w-4xl w-full">
        {/* Ultra minimal navigation */}
        <motion.nav
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="fixed top-0 left-0 right-0 flex justify-between items-center px-8 py-6"
        >
          <span className="font-satoshi text-sm tracking-tight text-black">
            Studio
          </span>
          <button className="font-satoshi text-sm text-black/60 hover:text-black transition-colors duration-300">
            Menu
          </button>
        </motion.nav>

        {/* Hero content - extreme whitespace */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="space-y-16"
        >
          {/* Tagline - whisper quiet */}
          <p className="font-satoshi text-sm tracking-wide text-black/40 uppercase">
            Design Studio
          </p>

          {/* Main headline - dramatic size contrast */}
          <h1 className="font-satoshi text-[clamp(3rem,12vw,8rem)] font-light leading-[0.9] tracking-tight text-black">
            Less is
            <br />
            <span className="text-black/20">everything.</span>
          </h1>

          {/* Single accent link */}
          <motion.a
            href="#work"
            className="inline-flex items-center gap-3 font-satoshi text-sm text-black group"
            whileHover={{ x: 4 }}
            transition={{ duration: 0.3 }}
          >
            <span className="border-b border-transparent group-hover:border-black transition-all duration-300">
              View selected work
            </span>
            <span className="text-black/40 group-hover:text-black transition-colors duration-300">
              →
            </span>
          </motion.a>
        </motion.div>

        {/* Bottom detail - single accent color */}
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ duration: 1.2, delay: 0.8 }}
          className="fixed bottom-8 left-8 right-8 h-px bg-black/10 origin-left"
        />
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-satoshi` - 가변 산세리프의 극단적 가벼움
- `text-black/20`, `text-black/40` - 투명도로 시각적 계층
- `leading-[0.9]` - 타이트한 라인하이트
- 단일 액센트: hover 시 border만 나타남
- 애니메이션: 300-500ms의 느리고 우아한 전환

---

### 2. Soft Maximalism

```tsx
// components/hero/SoftMaximalismHero.tsx
'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'

export function SoftMaximalismHero() {
  return (
    <section className="min-h-screen bg-amber-50 overflow-hidden">
      {/* Layered background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          initial={{ scale: 1.1, opacity: 0 }}
          animate={{ scale: 1, opacity: 0.6 }}
          transition={{ duration: 1.2 }}
          className="absolute -top-20 -right-20 w-[500px] h-[500px] rounded-full bg-gradient-to-br from-rose-200 to-orange-100 blur-3xl"
        />
        <motion.div
          initial={{ scale: 1.1, opacity: 0 }}
          animate={{ scale: 1, opacity: 0.4 }}
          transition={{ duration: 1.2, delay: 0.2 }}
          className="absolute -bottom-40 -left-20 w-[600px] h-[600px] rounded-full bg-gradient-to-tr from-amber-200 to-yellow-100 blur-3xl"
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-24">
        {/* Navigation with mixed typography */}
        <nav className="flex justify-between items-center mb-20">
          <span className="font-serif text-2xl text-stone-800 italic">
            Maison
          </span>
          <div className="flex gap-8">
            {['Discover', 'Stories', 'About'].map((item) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                className="font-sans text-sm text-stone-600 hover:text-stone-900 transition-colors"
                whileHover={{ y: -2 }}
              >
                {item}
              </motion.a>
            ))}
          </div>
        </nav>

        {/* Hero grid - rich layering */}
        <div className="grid grid-cols-12 gap-6 items-center">
          {/* Text content */}
          <div className="col-span-12 lg:col-span-5 space-y-8">
            <motion.span
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-block font-sans text-xs uppercase tracking-widest text-amber-700 bg-amber-100 px-4 py-2 rounded-full"
            >
              New Collection
            </motion.span>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="font-serif text-5xl lg:text-6xl text-stone-800 leading-tight"
            >
              Curated living,
              <br />
              <span className="text-amber-700">thoughtfully made.</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="font-sans text-lg text-stone-600 max-w-md"
            >
              Discover handcrafted pieces that bring warmth and character to every corner of your home.
            </motion.p>

            <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="font-sans text-sm bg-stone-800 text-white px-8 py-4 rounded-2xl hover:bg-stone-900 transition-colors shadow-lg shadow-stone-800/20"
            >
              Explore Collection
            </motion.button>
          </div>

          {/* Image stack - layered cards */}
          <div className="col-span-12 lg:col-span-7 relative h-[500px]">
            <motion.div
              initial={{ opacity: 0, y: 40, rotate: -3 }}
              animate={{ opacity: 1, y: 0, rotate: -3 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="absolute top-10 left-10 w-[280px] h-[350px] rounded-3xl bg-gradient-to-br from-rose-100 to-rose-200 shadow-2xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-[url('/texture-linen.png')] opacity-30" />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 40, rotate: 2 }}
              animate={{ opacity: 1, y: 0, rotate: 2 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="absolute top-0 right-10 w-[320px] h-[400px] rounded-3xl bg-gradient-to-br from-amber-100 to-orange-100 shadow-2xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-[url('/texture-paper.png')] opacity-20" />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
              className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[250px] h-[300px] rounded-3xl bg-gradient-to-br from-stone-100 to-stone-200 shadow-2xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-[url('/texture-fabric.png')] opacity-25" />
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-serif` + `font-sans` 혼용 - 헤딩은 세리프, 본문은 산세리프
- `bg-amber-50` - 따뜻한 중성색 기반
- `rounded-2xl`, `rounded-3xl` - 다양한 라운드
- `shadow-2xl` - 부드러운 그림자
- 레이어드 카드: 회전과 겹침으로 풍성함

---

### 3. Anti-Design Chaos

```tsx
// components/hero/AntiDesignChaosHero.tsx
'use client'

import { motion, useMotionValue, useTransform } from 'framer-motion'
import { useEffect } from 'react'

export function AntiDesignChaosHero() {
  const mouseX = useMotionValue(0)
  const mouseY = useMotionValue(0)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX)
      mouseY.set(e.clientY)
    }
    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [mouseX, mouseY])

  const rotateX = useTransform(mouseY, [0, window.innerHeight], [5, -5])
  const rotateY = useTransform(mouseX, [0, window.innerWidth], [-5, 5])

  return (
    <section className="min-h-screen bg-black overflow-hidden relative">
      {/* Noise overlay */}
      <div
        className="absolute inset-0 opacity-30 pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Chaotic overlapping elements */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="absolute top-10 left-10 text-[200px] font-basement font-black text-lime-400 leading-none mix-blend-difference select-none"
        style={{ rotate: rotateX }}
      >
        BREAK
      </motion.div>

      <motion.div
        initial={{ opacity: 0, x: 100 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.2, delay: 0.1 }}
        className="absolute top-40 -right-20 text-[180px] font-basement font-black text-fuchsia-500 leading-none -rotate-12 mix-blend-screen select-none"
      >
        RULES
      </motion.div>

      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.3, delay: 0.2 }}
        className="absolute bottom-20 left-20 w-[300px] h-[300px] border-8 border-cyan-400 rotate-45"
      />

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.1, delay: 0.3 }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          className="w-[400px] h-[400px] border-4 border-dashed border-yellow-400 rounded-full"
        />
      </motion.div>

      {/* Main chaotic content */}
      <div className="relative z-10 min-h-screen flex flex-col justify-center px-8">
        <motion.div
          initial={{ y: 100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.4 }}
          className="relative"
          style={{ rotateX, rotateY, transformPerspective: 1000 }}
        >
          {/* Overlapping, clashing typography */}
          <h1 className="relative">
            <span className="block font-basement text-[clamp(4rem,20vw,14rem)] font-black text-white leading-none tracking-tighter">
              ANTI
            </span>
            <span className="absolute -top-8 left-40 font-basement text-[clamp(3rem,15vw,10rem)] font-black text-transparent leading-none tracking-tighter" style={{ WebkitTextStroke: '2px #ff00ff' }}>
              DESIGN
            </span>
            <span className="block font-basement text-[clamp(2rem,10vw,7rem)] font-black text-lime-400 leading-none -rotate-3 -ml-4">
              IS THE NEW
            </span>
            <span className="block font-basement text-[clamp(4rem,18vw,12rem)] font-black leading-none bg-gradient-to-r from-cyan-400 via-fuchsia-500 to-yellow-400 bg-clip-text text-transparent rotate-1">
              DESIGN
            </span>
          </h1>
        </motion.div>

        {/* Glitchy button */}
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          whileHover={{ scale: 1.1, rotate: Math.random() * 10 - 5 }}
          whileTap={{ scale: 0.9 }}
          className="mt-12 self-start font-basement text-xl uppercase bg-white text-black px-8 py-4 border-4 border-black shadow-[8px_8px_0px_#ff00ff] hover:shadow-[12px_12px_0px_#00ffff] transition-all"
        >
          Enter Chaos →
        </motion.button>
      </div>

      {/* Random floating elements */}
      {[...Array(5)].map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, scale: 0 }}
          animate={{
            opacity: [0, 1, 0],
            scale: [0, 1, 0],
            x: [0, Math.random() * 200 - 100],
            y: [0, Math.random() * 200 - 100],
          }}
          transition={{
            duration: 3,
            delay: i * 0.5,
            repeat: Infinity,
            repeatDelay: 2,
          }}
          className="absolute w-20 h-20"
          style={{
            top: `${20 + i * 15}%`,
            left: `${10 + i * 20}%`,
            backgroundColor: ['#ff00ff', '#00ffff', '#ffff00', '#ff0000', '#00ff00'][i],
          }}
        />
      ))}
    </section>
  )
}
```

**핵심 특징:**
- `font-basement` - Basement Grotesque의 극단적 굵기
- `mix-blend-difference`, `mix-blend-screen` - 이상한 블렌드 모드
- `-rotate-12`, `rotate-45` - 회전하는 요소들
- 네온 색상: `lime-400`, `fuchsia-500`, `cyan-400`, `yellow-400`
- 노이즈 오버레이 SVG 패턴
- 예측 불가능한 마우스 반응

---

### 4. Liquid Glass

```tsx
// components/hero/LiquidGlassHero.tsx
'use client'

import { motion } from 'framer-motion'

export function LiquidGlassHero() {
  return (
    <section className="min-h-screen relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
        <motion.div
          animate={{
            scale: [1, 1.2, 1],
            x: [0, 100, 0],
            y: [0, -50, 0],
          }}
          transition={{ duration: 20, repeat: Infinity, ease: 'easeInOut' }}
          className="absolute top-0 left-0 w-[800px] h-[800px] rounded-full bg-gradient-to-r from-blue-500/40 to-cyan-500/40 blur-[100px]"
        />
        <motion.div
          animate={{
            scale: [1.2, 1, 1.2],
            x: [0, -100, 0],
            y: [0, 100, 0],
          }}
          transition={{ duration: 25, repeat: Infinity, ease: 'easeInOut' }}
          className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full bg-gradient-to-r from-pink-500/40 to-orange-500/40 blur-[100px]"
        />
        <motion.div
          animate={{
            scale: [1, 1.3, 1],
            rotate: [0, 180, 360],
          }}
          transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full bg-gradient-to-r from-violet-500/30 to-fuchsia-500/30 blur-[80px]"
        />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-20 min-h-screen flex items-center">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <h1 className="font-sans text-5xl lg:text-7xl font-semibold text-white leading-tight tracking-tight">
              Build the future
              <br />
              <span className="text-white/60">with clarity.</span>
            </h1>
            <p className="text-lg text-white/70 max-w-md font-light">
              A new way to design, develop, and ship products. Transparent, intuitive, and beautifully fast.
            </p>
            <div className="flex gap-4">
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 bg-white text-slate-900 font-medium rounded-2xl hover:bg-white/90 transition-colors"
              >
                Get Started
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-medium rounded-2xl border border-white/20 hover:bg-white/20 transition-colors"
              >
                Learn More
              </motion.button>
            </div>
          </motion.div>

          {/* Glass cards */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative"
          >
            {/* Main glass card */}
            <div className="relative bg-white/10 backdrop-blur-2xl rounded-3xl border border-white/20 p-8 shadow-2xl">
              {/* Inner glow */}
              <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-white/5 to-transparent pointer-events-none" />

              <div className="relative space-y-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center">
                    <span className="text-white text-xl">✦</span>
                  </div>
                  <div>
                    <h3 className="font-medium text-white">Dashboard</h3>
                    <p className="text-sm text-white/50">Real-time analytics</p>
                  </div>
                </div>

                {/* Glass stat cards */}
                <div className="grid grid-cols-2 gap-4">
                  {[
                    { label: 'Users', value: '24.5K', change: '+12%' },
                    { label: 'Revenue', value: '$84K', change: '+23%' },
                  ].map((stat) => (
                    <motion.div
                      key={stat.label}
                      whileHover={{ scale: 1.02, y: -2 }}
                      className="bg-white/5 backdrop-blur-xl rounded-2xl p-4 border border-white/10"
                    >
                      <p className="text-sm text-white/50">{stat.label}</p>
                      <p className="text-2xl font-semibold text-white mt-1">{stat.value}</p>
                      <p className="text-sm text-emerald-400 mt-1">{stat.change}</p>
                    </motion.div>
                  ))}
                </div>

                {/* Progress bar */}
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-white/50">Progress</span>
                    <span className="text-white">78%</span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: '78%' }}
                      transition={{ duration: 1.5, delay: 0.5, ease: 'easeOut' }}
                      className="h-full bg-gradient-to-r from-violet-500 to-fuchsia-500 rounded-full"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Floating smaller glass elements */}
            <motion.div
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute -top-6 -right-6 w-20 h-20 bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 flex items-center justify-center"
            >
              <span className="text-2xl">📊</span>
            </motion.div>
            <motion.div
              animate={{ y: [0, 10, 0] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute -bottom-4 -left-4 w-16 h-16 bg-white/10 backdrop-blur-xl rounded-xl border border-white/20 flex items-center justify-center"
            >
              <span className="text-xl">⚡</span>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `backdrop-blur-2xl` - 글래스모피즘의 핵심
- `bg-white/10`, `border-white/20` - 반투명 레이어
- `rounded-3xl` - 큰 border-radius
- 그라데이션 배경: `from-indigo-900 via-purple-900 to-pink-800`
- 부드럽게 움직이는 블러 blob들
- Inner glow: `bg-gradient-to-br from-white/5`

---

### 5. Editorial Magazine

```tsx
// components/hero/EditorialMagazineHero.tsx
'use client'

import { motion } from 'framer-motion'

export function EditorialMagazineHero() {
  return (
    <section className="min-h-screen bg-[#FAFAFA]">
      {/* Editorial header */}
      <header className="border-b border-black">
        <div className="max-w-7xl mx-auto px-8 py-6 flex justify-between items-center">
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="font-serif text-2xl italic tracking-tight"
          >
            The Chronicle
          </motion.span>
          <nav className="hidden md:flex gap-8">
            {['Culture', 'Design', 'Technology', 'Opinion'].map((item, i) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="font-serif text-sm uppercase tracking-widest hover:underline underline-offset-4"
              >
                {item}
              </motion.a>
            ))}
          </nav>
          <span className="font-serif text-sm text-black/50">
            Issue 47 — Winter 2025
          </span>
        </div>
      </header>

      {/* Hero article */}
      <div className="max-w-7xl mx-auto px-8 py-16">
        <div className="grid grid-cols-12 gap-8">
          {/* Left column - metadata */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="col-span-12 md:col-span-2 space-y-8"
          >
            <div className="space-y-2">
              <p className="font-serif text-xs uppercase tracking-widest text-black/50">Category</p>
              <p className="font-serif text-sm">Design Essay</p>
            </div>
            <div className="space-y-2">
              <p className="font-serif text-xs uppercase tracking-widest text-black/50">Read Time</p>
              <p className="font-serif text-sm">12 min</p>
            </div>
            <div className="space-y-2">
              <p className="font-serif text-xs uppercase tracking-widest text-black/50">Author</p>
              <p className="font-serif text-sm italic">Elena Vásquez</p>
            </div>
          </motion.div>

          {/* Center - main headline */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="col-span-12 md:col-span-8 space-y-12"
          >
            <h1 className="font-serif text-[clamp(2.5rem,8vw,6rem)] leading-[1.05] tracking-tight">
              The Quiet Revolution
              <br />
              <span className="italic">of Thoughtful Design</span>
            </h1>

            <div className="w-full h-px bg-black" />

            <p className="font-serif text-xl leading-relaxed text-black/70 max-w-2xl">
              In an age of constant noise, the most radical act may be creating
              space for contemplation. A meditation on restraint, intention,
              and the enduring power of less.
            </p>

            {/* Pull quote */}
            <blockquote className="border-l-2 border-black pl-8 py-4">
              <p className="font-serif text-3xl italic leading-snug">
                "Design is not about making things beautiful.
                It's about making things understood."
              </p>
            </blockquote>

            {/* Article start */}
            <div className="columns-2 gap-8 font-serif text-lg leading-loose text-black/80">
              <p className="first-letter:text-7xl first-letter:font-normal first-letter:float-left first-letter:mr-3 first-letter:mt-1">
                There exists a peculiar tension at the heart of contemporary design practice.
                On one hand, we are besieged by tools that promise infinite possibility—
                an endless array of gradients, shadows, and effects at our fingertips.
              </p>
              <p className="mt-6">
                On the other, the most celebrated work of our era tends toward reduction,
                toward the deliberate removal of ornament in favor of clarity.
                This is not minimalism for its own sake, but rather a profound respect
                for the viewer's attention.
              </p>
            </div>
          </motion.div>

          {/* Right column - visual element */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="col-span-12 md:col-span-2 flex flex-col items-end"
          >
            <div className="w-full aspect-[3/4] bg-black" />
            <p className="font-serif text-xs mt-3 text-right text-black/50 italic">
              Photo: Marcus Chen
            </p>
          </motion.div>
        </div>
      </div>

      {/* Bottom rule */}
      <div className="max-w-7xl mx-auto px-8">
        <motion.div
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{ delay: 0.8, duration: 1 }}
          className="w-full h-px bg-black origin-left"
        />
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-serif` - GT Sectra/Editorial New 스타일
- `columns-2` - 인쇄 매거진 스타일 컬럼
- `first-letter:text-7xl` - 드롭캡
- `tracking-widest uppercase` - 레이블 타이포그래피
- `border-l-2 border-black` - 풀 인용구 스타일
- 12컬럼 그리드: `grid-cols-12`
- 클래식 컬러: 검정/흰색만 사용

---

### 6. Retro-Futuristic

```tsx
// components/hero/RetroFuturisticHero.tsx
'use client'

import { motion } from 'framer-motion'

export function RetroFuturisticHero() {
  return (
    <section className="min-h-screen bg-slate-950 overflow-hidden relative">
      {/* Scanlines overlay */}
      <div
        className="absolute inset-0 pointer-events-none z-20"
        style={{
          background: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.3) 2px, rgba(0,0,0,0.3) 4px)',
        }}
      />

      {/* Perspective grid floor */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          background: `
            linear-gradient(to bottom, transparent 0%, rgba(0,255,255,0.1) 100%),
            repeating-linear-gradient(90deg, transparent, transparent 99px, rgba(0,255,255,0.3) 99px, rgba(0,255,255,0.3) 100px),
            repeating-linear-gradient(0deg, transparent, transparent 99px, rgba(0,255,255,0.3) 99px, rgba(0,255,255,0.3) 100px)
          `,
          transform: 'perspective(500px) rotateX(60deg)',
          transformOrigin: 'center top',
        }}
      />

      {/* Neon sun/moon */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 1, delay: 0.5 }}
        className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2"
      >
        <div className="w-[300px] h-[300px] rounded-full bg-gradient-to-b from-fuchsia-500 via-orange-500 to-cyan-500 blur-sm" />
        <div className="absolute inset-4 rounded-full bg-slate-950" />
        {/* Horizontal lines through sun */}
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute left-0 right-0 h-4 bg-slate-950"
            style={{ top: `${20 + i * 12}%` }}
          />
        ))}
      </motion.div>

      {/* Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-8 min-h-screen flex flex-col justify-center">
        {/* Glowing title */}
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-4"
        >
          <motion.p
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="font-mono text-cyan-400 text-sm tracking-[0.5em] uppercase"
          >
            System Online // 2084
          </motion.p>

          <h1 className="relative">
            <span
              className="block font-display text-[clamp(3rem,12vw,10rem)] font-bold tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-fuchsia-500 to-cyan-400"
              style={{
                textShadow: '0 0 40px rgba(0,255,255,0.5), 0 0 80px rgba(255,0,255,0.3)',
              }}
            >
              NEON
            </span>
            <span
              className="block font-display text-[clamp(3rem,12vw,10rem)] font-bold tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-fuchsia-500 via-orange-500 to-fuchsia-500 -mt-4"
              style={{
                textShadow: '0 0 40px rgba(255,0,255,0.5), 0 0 80px rgba(255,165,0,0.3)',
              }}
            >
              DREAMS
            </span>
          </h1>

          <p className="font-mono text-lg text-cyan-300/70 max-w-lg leading-relaxed">
            Enter the digital frontier. Where reality bends and imagination becomes interface.
          </p>
        </motion.div>

        {/* Neon buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex gap-6 mt-12"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative px-8 py-4 font-mono text-sm uppercase tracking-widest text-cyan-400 border border-cyan-400 overflow-hidden group"
            style={{
              boxShadow: '0 0 20px rgba(0,255,255,0.3), inset 0 0 20px rgba(0,255,255,0.1)',
            }}
          >
            <span className="relative z-10">Initialize</span>
            <motion.div
              className="absolute inset-0 bg-cyan-400"
              initial={{ x: '-100%' }}
              whileHover={{ x: 0 }}
              transition={{ duration: 0.3 }}
              style={{ mixBlendMode: 'overlay' }}
            />
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 font-mono text-sm uppercase tracking-widest text-fuchsia-400 border border-fuchsia-400/50 hover:border-fuchsia-400"
            style={{
              boxShadow: '0 0 15px rgba(255,0,255,0.2)',
            }}
          >
            Explore Grid
          </motion.button>
        </motion.div>

        {/* Bottom stats */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="absolute bottom-8 left-8 right-8 flex justify-between font-mono text-xs text-cyan-400/50"
        >
          <span>LAT: 34.0522° N</span>
          <span className="animate-pulse">● CONNECTED</span>
          <span>LONG: 118.2437° W</span>
        </motion.div>
      </div>

      {/* Floating geometric elements */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
        className="absolute top-20 right-20 w-24 h-24 border border-fuchsia-500/50"
        style={{ boxShadow: '0 0 20px rgba(255,0,255,0.3)' }}
      />
      <motion.div
        animate={{ rotate: -360 }}
        transition={{ duration: 25, repeat: Infinity, ease: 'linear' }}
        className="absolute bottom-40 left-20 w-16 h-16 border border-cyan-400/50"
        style={{ boxShadow: '0 0 15px rgba(0,255,255,0.3)' }}
      />
    </section>
  )
}
```

**핵심 특징:**
- `font-display` (Orbitron) + `font-mono` (VT323) - 80s SF 타이포
- 네온 그라데이션: `from-cyan-400 via-fuchsia-500`
- `textShadow` 글로우 효과
- 스캔라인 오버레이: `repeating-linear-gradient`
- 원근 그리드: `perspective` + `rotateX`
- 기하학적 회전 요소들
- 네온 색상: cyan, fuchsia, orange

---

### 7. Organic Natural

```tsx
// components/hero/OrganicNaturalHero.tsx
'use client'

import { motion } from 'framer-motion'

export function OrganicNaturalHero() {
  return (
    <section className="min-h-screen bg-stone-100 relative overflow-hidden">
      {/* Paper texture overlay */}
      <div
        className="absolute inset-0 opacity-50 pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Organic blob shapes */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.4 }}
        transition={{ duration: 1.5, ease: 'easeOut' }}
        className="absolute -top-40 -right-40 w-[600px] h-[600px] bg-gradient-to-br from-amber-200 to-orange-200"
        style={{
          borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%',
        }}
      />
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 0.3 }}
        transition={{ duration: 1.5, delay: 0.3, ease: 'easeOut' }}
        className="absolute -bottom-20 -left-20 w-[500px] h-[500px] bg-gradient-to-tr from-stone-300 to-stone-200"
        style={{
          borderRadius: '30% 70% 70% 30% / 30% 30% 70% 70%',
        }}
      />
      <motion.div
        animate={{
          borderRadius: [
            '60% 40% 30% 70% / 60% 30% 70% 40%',
            '30% 60% 70% 40% / 50% 60% 30% 60%',
            '60% 40% 30% 70% / 60% 30% 70% 40%',
          ],
        }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-gradient-to-br from-sage-200 to-olive-200 opacity-30"
        style={{
          background: 'linear-gradient(135deg, #C5D5C5 0%, #B5C4A8 100%)',
        }}
      />

      <div className="relative z-10 max-w-6xl mx-auto px-8 py-24 min-h-screen flex items-center">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Content */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, ease: 'easeOut' }}
            className="space-y-8"
          >
            <span
              className="inline-block text-sm tracking-wide text-stone-500"
              style={{ fontFamily: "'Cormorant Garamond', serif" }}
            >
              Rooted in Nature
            </span>

            <h1
              className="text-5xl lg:text-7xl text-stone-800 leading-[1.1]"
              style={{ fontFamily: "'Cormorant Garamond', serif" }}
            >
              Breathe.
              <br />
              <span className="italic text-stone-600">Ground.</span>
              <br />
              <span className="text-olive-700" style={{ color: '#6B7A5B' }}>Flourish.</span>
            </h1>

            <p
              className="text-lg text-stone-600 max-w-md leading-relaxed"
              style={{ fontFamily: "'Lora', serif" }}
            >
              Reconnect with your inner calm through mindful practices
              inspired by the wisdom of the natural world.
            </p>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="px-8 py-4 bg-stone-800 text-stone-100 rounded-full text-sm tracking-wide hover:bg-stone-700 transition-colors"
              style={{ fontFamily: "'Lora', serif" }}
            >
              Begin Your Journey
            </motion.button>

            {/* Organic decorative elements */}
            <div className="flex items-center gap-6 pt-8">
              <svg viewBox="0 0 100 100" className="w-12 h-12 text-stone-400">
                <path
                  fill="currentColor"
                  d="M50 0C30 20 20 50 50 80C80 50 70 20 50 0Z"
                  opacity="0.6"
                />
              </svg>
              <span className="text-xs text-stone-400 tracking-widest uppercase">
                Est. 2024 · Sustainable Wellness
              </span>
            </div>
          </motion.div>

          {/* Visual element - organic card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, rotate: 3 }}
            animate={{ opacity: 1, scale: 1, rotate: 3 }}
            transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
            className="relative"
          >
            <div
              className="aspect-[4/5] bg-gradient-to-br from-stone-200 to-stone-300 p-8 flex flex-col justify-end"
              style={{
                borderRadius: '40% 60% 70% 30% / 40% 50% 60% 50%',
              }}
            >
              {/* Texture overlay */}
              <div
                className="absolute inset-0 opacity-20"
                style={{
                  borderRadius: 'inherit',
                  backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0C45 15 60 30 45 45C30 60 15 45 0 30C15 15 30 0 30 0Z' fill='%23000' fill-opacity='0.03'/%3E%3C/svg%3E")`,
                }}
              />
              <div className="relative">
                <p
                  className="text-2xl text-stone-700 italic"
                  style={{ fontFamily: "'Cormorant Garamond', serif" }}
                >
                  "Nature does not hurry, yet everything is accomplished."
                </p>
                <p className="mt-4 text-sm text-stone-500">— Lao Tzu</p>
              </div>
            </div>

            {/* Floating leaf accent */}
            <motion.div
              animate={{ y: [0, -10, 0], rotate: [0, 5, 0] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute -top-8 -right-4 text-5xl"
            >
              🍃
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-family: 'Cormorant Garamond'` + `'Lora'` - 유기적 세리프
- 어스톤: `stone-100`, `stone-800`, olive, sage
- 불규칙 blob: `borderRadius: '60% 40% 30% 70%'`
- 페이퍼 텍스처 노이즈 오버레이
- 유기적 형태 애니메이션
- 느린 전환: `duration: 1.5`

---

### 8. Luxury Refined

```tsx
// components/hero/LuxuryRefinedHero.tsx
'use client'

import { motion } from 'framer-motion'

export function LuxuryRefinedHero() {
  return (
    <section className="min-h-screen bg-black text-white overflow-hidden">
      {/* Subtle gold gradient accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-amber-900/10" />

      {/* Navigation */}
      <motion.nav
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.5 }}
        className="absolute top-0 left-0 right-0 flex justify-between items-center px-12 py-8 z-20"
      >
        <span
          className="text-xs tracking-[0.4em] uppercase"
          style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
        >
          Maison
        </span>
        <div className="flex gap-12">
          {['Collection', 'Atelier', 'Heritage'].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="text-xs tracking-[0.3em] uppercase text-white/60 hover:text-white transition-colors duration-500"
              style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
            >
              {item}
            </a>
          ))}
        </div>
      </motion.nav>

      <div className="relative z-10 max-w-7xl mx-auto px-12 min-h-screen flex items-center">
        <div className="grid grid-cols-12 gap-8 w-full items-center">
          {/* Left - Large typography */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 1.2, delay: 0.3 }}
            className="col-span-12 lg:col-span-7 space-y-12"
          >
            {/* Overline */}
            <div className="flex items-center gap-6">
              <div className="w-16 h-px bg-gradient-to-r from-amber-400 to-amber-600" />
              <span
                className="text-xs tracking-[0.5em] uppercase text-amber-400/80"
                style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
              >
                Autumn/Winter 2025
              </span>
            </div>

            {/* Main headline */}
            <h1
              className="text-[clamp(3rem,10vw,8rem)] leading-[0.95] tracking-tight"
              style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
            >
              <span className="block">Timeless</span>
              <span className="block italic font-light text-white/40">Elegance</span>
            </h1>

            {/* Refined body text */}
            <p
              className="text-lg text-white/50 max-w-md leading-relaxed tracking-wide"
              style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
            >
              Where craftsmanship meets vision.
              A collection of pieces designed to transcend seasons.
            </p>

            {/* Minimal CTA */}
            <motion.a
              href="#collection"
              whileHover={{ letterSpacing: '0.4em' }}
              transition={{ duration: 0.5 }}
              className="inline-flex items-center gap-4 group"
            >
              <span
                className="text-xs tracking-[0.3em] uppercase text-white/80 group-hover:text-white transition-colors duration-500"
                style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
              >
                Discover Collection
              </span>
              <motion.span
                className="w-12 h-px bg-white/40 group-hover:w-20 group-hover:bg-amber-400 transition-all duration-500"
              />
            </motion.a>
          </motion.div>

          {/* Right - Visual element */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1.5, delay: 0.6 }}
            className="col-span-12 lg:col-span-5"
          >
            <div className="relative aspect-[3/4]">
              {/* Gold border frame */}
              <div className="absolute inset-4 border border-amber-400/20" />
              {/* Image placeholder */}
              <div className="absolute inset-0 bg-gradient-to-br from-stone-900 to-black" />
              {/* Corner accents */}
              <div className="absolute top-0 left-0 w-8 h-8 border-t border-l border-amber-400/40" />
              <div className="absolute bottom-0 right-0 w-8 h-8 border-b border-r border-amber-400/40" />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Bottom details */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 1 }}
        className="absolute bottom-0 left-0 right-0 border-t border-white/10"
      >
        <div className="max-w-7xl mx-auto px-12 py-6 flex justify-between items-center">
          <span
            className="text-xs tracking-[0.3em] text-white/30"
            style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
          >
            Paris · Milan · New York
          </span>
          <span
            className="text-xs tracking-[0.3em] text-white/30"
            style={{ fontFamily: "'Didot', 'Playfair Display', serif" }}
          >
            Since 1892
          </span>
        </div>
      </motion.div>
    </section>
  )
}
```

**핵심 특징:**
- `font-family: 'Didot', 'Playfair Display'` - 우아한 세리프
- `tracking-[0.3em]` - 넓은 자간
- 검정 + 흰색 + 금색 (`amber-400`)
- `border-white/10` - 미묘한 구분선
- 과감한 여백: `py-32`, `space-y-12`
- 느린 전환: `duration: 0.5`, `duration: 1`

---

### 9. Tech Documentation

```tsx
// components/hero/TechDocumentationHero.tsx
'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'

export function TechDocumentationHero() {
  const [copied, setCopied] = useState(false)
  const installCommand = 'npm install @acme/sdk'

  const handleCopy = () => {
    navigator.clipboard.writeText(installCommand)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <section className="min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-sm border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-8">
            <span className="font-mono font-bold text-lg text-white">
              acme<span className="text-emerald-400">/</span>sdk
            </span>
            <nav className="hidden md:flex gap-6">
              {['Docs', 'API', 'Examples', 'Blog'].map((item) => (
                <a
                  key={item}
                  href={`#${item.toLowerCase()}`}
                  className="font-mono text-sm text-slate-400 hover:text-white transition-colors"
                >
                  {item}
                </a>
              ))}
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden sm:inline font-mono text-xs px-3 py-1 bg-emerald-400/10 text-emerald-400 rounded-full border border-emerald-400/20">
              v3.2.1
            </span>
            <a href="#github" className="font-mono text-sm text-slate-400 hover:text-white">
              GitHub →
            </a>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Left - Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs px-2 py-1 bg-amber-400/10 text-amber-400 rounded">
                  NEW
                </span>
                <span className="font-mono text-sm text-slate-400">
                  Now with TypeScript 5.0 support
                </span>
              </div>

              <h1 className="font-sans text-5xl lg:text-6xl font-bold text-white leading-tight">
                Build faster with
                <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
                  type-safe APIs
                </span>
              </h1>

              <p className="text-lg text-slate-400 max-w-lg leading-relaxed">
                A modern SDK for building robust applications.
                Full TypeScript support, zero dependencies, and blazingly fast.
              </p>
            </div>

            {/* Install command */}
            <div className="space-y-3">
              <span className="font-mono text-xs text-slate-500 uppercase tracking-wider">
                Quick Start
              </span>
              <motion.div
                whileHover={{ scale: 1.01 }}
                className="relative bg-slate-900 rounded-lg border border-slate-800 overflow-hidden group"
              >
                <div className="flex items-center justify-between p-4">
                  <code className="font-mono text-sm text-slate-300">
                    <span className="text-slate-500">$</span> {installCommand}
                  </code>
                  <button
                    onClick={handleCopy}
                    className="font-mono text-xs px-3 py-1.5 bg-slate-800 text-slate-400 rounded hover:text-white transition-colors"
                  >
                    {copied ? '✓ Copied' : 'Copy'}
                  </button>
                </div>
                <div className="h-0.5 bg-gradient-to-r from-emerald-400 to-cyan-400 scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
              </motion.div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6 pt-4">
              {[
                { value: '50K+', label: 'Downloads/week' },
                { value: '99.9%', label: 'Uptime' },
                { value: '<1ms', label: 'Latency' },
              ].map((stat) => (
                <div key={stat.label}>
                  <p className="font-mono text-2xl font-bold text-white">{stat.value}</p>
                  <p className="font-mono text-xs text-slate-500">{stat.label}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Right - Code block */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden"
          >
            {/* Code header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-slate-800 bg-slate-900/50">
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/70" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
                <div className="w-3 h-3 rounded-full bg-green-500/70" />
              </div>
              <span className="font-mono text-xs text-slate-500">example.ts</span>
            </div>

            {/* Code content */}
            <pre className="p-6 font-mono text-sm overflow-x-auto">
              <code>
                <span className="text-slate-500">{'// Initialize the SDK'}</span>
                {'\n'}
                <span className="text-purple-400">import</span>
                <span className="text-slate-300">{' { Acme } '}</span>
                <span className="text-purple-400">from</span>
                <span className="text-emerald-400">{" '@acme/sdk'"}</span>
                {'\n\n'}
                <span className="text-purple-400">const</span>
                <span className="text-slate-300">{' client = '}</span>
                <span className="text-purple-400">new</span>
                <span className="text-cyan-400">{' Acme'}</span>
                <span className="text-slate-300">{'({'}</span>
                {'\n'}
                <span className="text-slate-300">{'  apiKey: '}</span>
                <span className="text-emerald-400">{'process.env.ACME_KEY'}</span>
                <span className="text-slate-300">{','}</span>
                {'\n'}
                <span className="text-slate-300">{'})'}</span>
                {'\n\n'}
                <span className="text-slate-500">{'// Fetch data with full type safety'}</span>
                {'\n'}
                <span className="text-purple-400">const</span>
                <span className="text-slate-300">{' data = '}</span>
                <span className="text-purple-400">await</span>
                <span className="text-slate-300">{' client.'}</span>
                <span className="text-cyan-400">users</span>
                <span className="text-slate-300">{'.'}</span>
                <span className="text-cyan-400">list</span>
                <span className="text-slate-300">{'()'}</span>
                {'\n\n'}
                <span className="text-cyan-400">console</span>
                <span className="text-slate-300">{'.'}</span>
                <span className="text-cyan-400">log</span>
                <span className="text-slate-300">{'(data)'}</span>
                <span className="text-slate-500">{' // ✓ Fully typed!'}</span>
              </code>
            </pre>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-mono` (JetBrains Mono) - 모노스페이스 코드 폰트
- 다크 모드: `bg-slate-950`, `text-slate-100`
- 구문 강조 색상: `text-purple-400`, `text-emerald-400`, `text-cyan-400`
- 복사 기능이 있는 코드 블록
- `sticky top-0` - 고정 헤더
- `border-slate-800` - 미묘한 구분선

---

### 10. Brutalist Raw

```tsx
// components/hero/BrutalistRawHero.tsx
'use client'

import { motion } from 'framer-motion'

export function BrutalistRawHero() {
  return (
    <section className="min-h-screen bg-white">
      {/* No-frills header */}
      <header className="border-b-2 border-black">
        <div className="px-4 py-2 flex justify-between items-center">
          <span className="font-mono text-sm font-bold uppercase">
            BRUTALIST.CO
          </span>
          <nav className="flex gap-4">
            {['ABOUT', 'WORK', 'CONTACT'].map((item) => (
              <a
                key={item}
                href={`#${item.toLowerCase()}`}
                className="font-mono text-sm underline hover:no-underline hover:bg-black hover:text-white px-1"
              >
                {item}
              </a>
            ))}
          </nav>
        </div>
      </header>

      {/* Raw content */}
      <div className="p-4">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.1 }}
          className="space-y-4"
        >
          {/* No decoration headline */}
          <h1 className="font-mono text-[clamp(2rem,10vw,6rem)] font-bold uppercase leading-none tracking-tight">
            FUNCTION
            <br />
            OVER
            <br />
            FORM
          </h1>

          {/* Plain horizontal rule */}
          <hr className="border-t-2 border-black" />

          {/* Raw text block */}
          <div className="max-w-2xl">
            <p className="font-mono text-base leading-relaxed">
              This is a website. It has text and links.
              It loads fast because it has no unnecessary styling.
              Design trends come and go. Utility remains.
            </p>
          </div>

          {/* Basic list */}
          <ul className="font-mono text-sm space-y-1 pl-4">
            <li>• No gradients</li>
            <li>• No shadows</li>
            <li>• No animations</li>
            <li>• No rounded corners</li>
            <li>• Just content</li>
          </ul>

          {/* Raw buttons */}
          <div className="flex gap-2 pt-4">
            <motion.a
              href="#start"
              whileHover={{ backgroundColor: '#000', color: '#fff' }}
              transition={{ duration: 0 }}
              className="font-mono text-sm uppercase px-4 py-2 border-2 border-black bg-white text-black cursor-pointer"
            >
              START →
            </motion.a>
            <a
              href="#source"
              className="font-mono text-sm uppercase px-4 py-2 border-2 border-black bg-black text-white hover:bg-white hover:text-black"
            >
              VIEW SOURCE
            </a>
          </div>

          {/* Info table */}
          <table className="font-mono text-sm border-2 border-black mt-8">
            <tbody>
              <tr className="border-b-2 border-black">
                <td className="p-2 border-r-2 border-black font-bold">SIZE</td>
                <td className="p-2">2.4 KB</td>
              </tr>
              <tr className="border-b-2 border-black">
                <td className="p-2 border-r-2 border-black font-bold">LOAD TIME</td>
                <td className="p-2">0.1s</td>
              </tr>
              <tr>
                <td className="p-2 border-r-2 border-black font-bold">DEPENDENCIES</td>
                <td className="p-2">0</td>
              </tr>
            </tbody>
          </table>

          {/* Footer info */}
          <div className="pt-8 font-mono text-xs text-black/60">
            <p>Last updated: {new Date().toISOString().split('T')[0]}</p>
            <p>No cookies. No tracking. No JavaScript required.</p>
          </div>
        </motion.div>
      </div>

      {/* Counter at bottom */}
      <div className="fixed bottom-0 left-0 right-0 border-t-2 border-black bg-white">
        <div className="px-4 py-2 flex justify-between font-mono text-xs">
          <span>VISITORS: 12,847</span>
          <span>© 2025 BRUTALIST.CO</span>
        </div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-mono` - 시스템 모노스페이스 폰트
- `border-2 border-black` - 굵은 검정 테두리
- `bg-white text-black` - 순수 흑백
- 그림자 없음, 라운드 없음
- `transition: 0` - 애니메이션 거의 없음
- `<table>`, `<hr>` - 기본 HTML 요소
- `hover:bg-black hover:text-white` - 간단한 반전 호버

---

### 11. Playful Rounded

```tsx
// components/hero/PlayfulRoundedHero.tsx
'use client'

import { motion } from 'framer-motion'

export function PlayfulRoundedHero() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-violet-50 via-pink-50 to-amber-50 overflow-hidden">
      {/* Floating background elements */}
      <div className="absolute inset-0 overflow-hidden">
        {[
          { color: 'bg-violet-200', size: 'w-72 h-72', pos: 'top-10 -left-20', delay: 0 },
          { color: 'bg-pink-200', size: 'w-64 h-64', pos: 'top-40 right-10', delay: 0.5 },
          { color: 'bg-amber-200', size: 'w-56 h-56', pos: 'bottom-20 left-1/4', delay: 1 },
          { color: 'bg-cyan-200', size: 'w-48 h-48', pos: 'bottom-40 right-1/4', delay: 1.5 },
        ].map((blob, i) => (
          <motion.div
            key={i}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 0.5 }}
            transition={{ duration: 0.8, delay: blob.delay, ease: 'backOut' }}
            className={`absolute ${blob.size} ${blob.pos} ${blob.color} rounded-full blur-3xl`}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-16 min-h-screen flex flex-col">
        {/* Playful navigation */}
        <motion.nav
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="flex justify-between items-center"
        >
          <motion.span
            whileHover={{ scale: 1.05, rotate: -2 }}
            className="font-nunito text-2xl font-bold text-violet-600 cursor-pointer"
          >
            bubbly ✨
          </motion.span>
          <div className="flex gap-2">
            {['Features', 'Pricing', 'About'].map((item) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                whileHover={{ scale: 1.05, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="font-nunito text-sm px-4 py-2 rounded-full text-violet-700 hover:bg-white/50 transition-colors"
              >
                {item}
              </motion.a>
            ))}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="font-nunito text-sm px-6 py-2 bg-violet-500 text-white rounded-full shadow-lg shadow-violet-500/30 hover:bg-violet-600 transition-colors"
            >
              Get Started 🚀
            </motion.button>
          </div>
        </motion.nav>

        {/* Hero content */}
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center space-y-8 max-w-3xl">
            {/* Bouncy badge */}
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 10, delay: 0.3 }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-white/80 rounded-full shadow-md"
            >
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <span className="font-nunito text-sm text-violet-700">
                New: Dark mode is here! 🌙
              </span>
            </motion.div>

            {/* Main headline with bounce */}
            <motion.h1
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ type: 'spring', stiffness: 100, damping: 12, delay: 0.4 }}
              className="font-nunito text-5xl lg:text-7xl font-extrabold text-violet-900 leading-tight"
            >
              Make work feel
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-500 via-pink-500 to-amber-500">
                actually fun
              </span>
              {' '}
              <motion.span
                animate={{ rotate: [0, 14, -8, 14, -4, 10, 0] }}
                transition={{ duration: 2.5, repeat: Infinity, repeatDelay: 1 }}
                className="inline-block"
              >
                🎉
              </motion.span>
            </motion.h1>

            {/* Subtext */}
            <motion.p
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="font-nunito text-xl text-violet-700/80 max-w-xl mx-auto"
            >
              The productivity app that makes you smile.
              Simple, colorful, and designed to spark joy.
            </motion.p>

            {/* CTA buttons */}
            <motion.div
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <motion.button
                whileHover={{ scale: 1.05, y: -4 }}
                whileTap={{ scale: 0.95 }}
                className="font-nunito text-lg px-8 py-4 bg-gradient-to-r from-violet-500 to-pink-500 text-white rounded-2xl shadow-xl shadow-violet-500/30 hover:shadow-2xl transition-shadow"
              >
                Try for Free ✨
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05, y: -4 }}
                whileTap={{ scale: 0.95 }}
                className="font-nunito text-lg px-8 py-4 bg-white text-violet-700 rounded-2xl shadow-lg hover:shadow-xl transition-shadow"
              >
                Watch Demo 🎬
              </motion.button>
            </motion.div>

            {/* Social proof */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1 }}
              className="flex items-center justify-center gap-4 pt-8"
            >
              <div className="flex -space-x-3">
                {['😊', '🥳', '😎', '🤩', '💜'].map((emoji, i) => (
                  <motion.div
                    key={i}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 1 + i * 0.1, type: 'spring' }}
                    className="w-10 h-10 bg-white rounded-full shadow-md flex items-center justify-center text-lg"
                  >
                    {emoji}
                  </motion.div>
                ))}
              </div>
              <p className="font-nunito text-sm text-violet-700/80">
                <span className="font-bold">10,000+</span> happy users
              </p>
            </motion.div>
          </div>
        </div>

        {/* Bouncy scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, y: [0, 10, 0] }}
          transition={{
            opacity: { delay: 1.2 },
            y: { duration: 1.5, repeat: Infinity }
          }}
          className="text-center pb-8"
        >
          <span className="font-nunito text-sm text-violet-500">Scroll down ↓</span>
        </motion.div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-nunito` (Nunito/Quicksand) - 둥근 산세리프
- 파스텔 색상: `violet-50`, `pink-50`, `amber-50`
- `rounded-full`, `rounded-2xl` - 큰 border-radius
- `shadow-xl shadow-violet-500/30` - 컬러 그림자
- 이모지 사용: ✨ 🚀 🎉 🌙
- `type: 'spring'` - 탄성 있는 애니메이션
- `whileHover: { scale: 1.05, y: -4 }` - 바운스 호버

---

### 12. Grade-School Bold

```tsx
// components/hero/GradeSchoolBoldHero.tsx
'use client'

import { motion } from 'framer-motion'

export function GradeSchoolBoldHero() {
  return (
    <section className="min-h-screen bg-amber-100 overflow-hidden relative">
      {/* Paper texture */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='grain'%3E%3CfeTurbulence baseFrequency='0.8' type='fractalNoise'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23grain)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Crayon-like doodles */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ filter: 'url(#crayon)' }}>
        <defs>
          <filter id="crayon">
            <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="5" result="noise"/>
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="3" xChannelSelector="R" yChannelSelector="G"/>
          </filter>
        </defs>
        <motion.circle
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: 'spring' }}
          cx="15%" cy="20%" r="80"
          fill="none"
          stroke="#ef4444"
          strokeWidth="4"
          strokeDasharray="10,5"
        />
        <motion.path
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ delay: 0.8, duration: 1 }}
          d="M 80% 15% Q 85% 25% 75% 30%"
          fill="none"
          stroke="#3b82f6"
          strokeWidth="6"
          strokeLinecap="round"
        />
        <motion.rect
          initial={{ scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: -10 }}
          transition={{ delay: 1, type: 'spring' }}
          x="70%" y="60%" width="100" height="100"
          fill="none"
          stroke="#22c55e"
          strokeWidth="5"
        />
      </svg>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-12 min-h-screen flex flex-col">
        {/* Playful header */}
        <motion.header
          initial={{ y: -50, rotate: -3 }}
          animate={{ y: 0, rotate: -3 }}
          transition={{ type: 'spring', stiffness: 100 }}
          className="flex justify-between items-center"
        >
          <span
            className="text-3xl font-black text-blue-600 -rotate-3"
            style={{ fontFamily: "'Albert Sans', sans-serif" }}
          >
            LEARN!
          </span>
          <motion.div
            whileHover={{ scale: 1.1, rotate: 5 }}
            className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-none border-4 border-black shadow-[4px_4px_0px_#000]"
          >
            <span
              className="font-bold"
              style={{ fontFamily: "'Albert Sans', sans-serif" }}
            >
              SIGN UP!
            </span>
            <span className="text-xl">✏️</span>
          </motion.div>
        </motion.header>

        {/* Main content */}
        <div className="flex-1 flex items-center">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center w-full">
            {/* Text */}
            <motion.div
              initial={{ x: -100, opacity: 0, rotate: 2 }}
              animate={{ x: 0, opacity: 1, rotate: 2 }}
              transition={{ type: 'spring', stiffness: 80 }}
              className="space-y-6"
            >
              <motion.h1
                animate={{ rotate: [-1, 1, -1] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                className="text-6xl lg:text-8xl font-black leading-none"
                style={{ fontFamily: "'Albert Sans', sans-serif" }}
              >
                <span className="text-blue-600 block">LEARNING</span>
                <span className="text-red-500 block -rotate-2">IS</span>
                <span className="text-green-600 block rotate-1">AWESOME!</span>
              </motion.h1>

              <p
                className="text-xl text-gray-800 max-w-md leading-relaxed font-medium"
                style={{ fontFamily: "'Albert Sans', sans-serif" }}
              >
                Join 1 million kids making learning super fun!
                Games, puzzles, and surprises every day!
              </p>

              {/* Bold primary buttons */}
              <div className="flex flex-wrap gap-4">
                <motion.button
                  whileHover={{ scale: 1.05, rotate: -2 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-yellow-400 text-black font-black text-xl border-4 border-black shadow-[6px_6px_0px_#000] hover:shadow-[2px_2px_0px_#000] hover:translate-x-1 hover:translate-y-1 transition-all"
                  style={{ fontFamily: "'Albert Sans', sans-serif" }}
                >
                  START FREE! 🎮
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05, rotate: 2 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-white text-black font-black text-xl border-4 border-black shadow-[6px_6px_0px_#000]"
                  style={{ fontFamily: "'Albert Sans', sans-serif" }}
                >
                  FOR PARENTS 👨‍👩‍👧
                </motion.button>
              </div>

              {/* Stars rating */}
              <div className="flex items-center gap-2 pt-4">
                <div className="flex">
                  {[...Array(5)].map((_, i) => (
                    <motion.span
                      key={i}
                      initial={{ scale: 0, rotate: -180 }}
                      animate={{ scale: 1, rotate: 0 }}
                      transition={{ delay: 1.5 + i * 0.1, type: 'spring' }}
                      className="text-3xl"
                    >
                      ⭐
                    </motion.span>
                  ))}
                </div>
                <span
                  className="font-bold text-gray-700"
                  style={{ fontFamily: "'Albert Sans', sans-serif" }}
                >
                  Loved by kids & parents!
                </span>
              </div>
            </motion.div>

            {/* Visual element */}
            <motion.div
              initial={{ scale: 0, rotate: -10 }}
              animate={{ scale: 1, rotate: 5 }}
              transition={{ type: 'spring', stiffness: 60, delay: 0.3 }}
              className="relative"
            >
              <div className="aspect-square bg-cyan-400 border-8 border-black shadow-[12px_12px_0px_#000] p-8 rotate-3">
                {/* Simple illustration placeholder */}
                <div className="h-full bg-white border-4 border-black flex items-center justify-center">
                  <motion.div
                    animate={{
                      scale: [1, 1.1, 1],
                      rotate: [0, 5, -5, 0],
                    }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="text-8xl"
                  >
                    🎨
                  </motion.div>
                </div>
              </div>

              {/* Floating elements */}
              <motion.div
                animate={{ y: [-5, 5, -5], rotate: [0, 10, 0] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -top-8 -right-8 text-6xl"
              >
                📚
              </motion.div>
              <motion.div
                animate={{ y: [5, -5, 5], rotate: [0, -10, 0] }}
                transition={{ duration: 2.5, repeat: Infinity }}
                className="absolute -bottom-4 -left-4 text-5xl"
              >
                🚀
              </motion.div>
            </motion.div>
          </div>
        </div>

        {/* Bottom subjects */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1 }}
          className="flex flex-wrap gap-3 justify-center pb-8"
        >
          {[
            { emoji: '🔢', text: 'MATH', color: 'bg-blue-400' },
            { emoji: '📖', text: 'READING', color: 'bg-red-400' },
            { emoji: '🔬', text: 'SCIENCE', color: 'bg-green-400' },
            { emoji: '🎨', text: 'ART', color: 'bg-purple-400' },
            { emoji: '🎵', text: 'MUSIC', color: 'bg-pink-400' },
          ].map((subject, i) => (
            <motion.div
              key={subject.text}
              whileHover={{ scale: 1.1, rotate: Math.random() * 10 - 5 }}
              className={`${subject.color} px-4 py-2 border-4 border-black shadow-[4px_4px_0px_#000] flex items-center gap-2`}
            >
              <span className="text-2xl">{subject.emoji}</span>
              <span
                className="font-black text-black"
                style={{ fontFamily: "'Albert Sans', sans-serif" }}
              >
                {subject.text}
              </span>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
```

**핵심 특징:**
- `font-family: 'Albert Sans'` - 친근한 볼드 폰트
- 원색: `blue-600`, `red-500`, `green-600`, `yellow-400`
- `border-4 border-black` - 두꺼운 검정 테두리
- `shadow-[6px_6px_0px_#000]` - 거친 드롭 쉐도우
- `rotate-3`, `-rotate-2` - 기울어진 요소들
- 크레용 SVG 필터
- 이모지 과다 사용: 📚 🎮 🚀 ⭐
- 예측 불가능한 움직임

---

## 템플릿 사용 가이드

### 1. 폰트 설정

```bash
# next/font 사용 (권장)
npm install @next/font
```

```typescript
// app/layout.tsx
import { DM_Sans, DM_Serif_Display } from 'next/font/google'
import localFont from 'next/font/local'

const satoshi = localFont({
  src: '../fonts/Satoshi-Variable.woff2',
  variable: '--font-satoshi',
})

const clashDisplay = localFont({
  src: '../fonts/ClashDisplay-Variable.woff2',
  variable: '--font-clash',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${satoshi.variable} ${clashDisplay.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

### 2. Tailwind 설정

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      fontFamily: {
        satoshi: ['var(--font-satoshi)', 'sans-serif'],
        clash: ['var(--font-clash)', 'sans-serif'],
        // ... 다른 폰트들
      },
    },
  },
}
```

### 3. Framer Motion 설정

```bash
npm install framer-motion
```

```typescript
// app/providers.tsx
'use client'

import { LazyMotion, domAnimation } from 'framer-motion'

export function Providers({ children }) {
  return (
    <LazyMotion features={domAnimation}>
      {children}
    </LazyMotion>
  )
}
```

### 4. 템플릿 조합 예시

```tsx
// Minimal + Liquid Glass 조합
import { BarelyThereMinimalHero } from './BarelyThereMinimalHero'
import { LiquidGlassHero } from './LiquidGlassHero'

export function HybridHero() {
  return (
    <>
      {/* 전체 레이아웃은 Minimal */}
      <section className="min-h-screen bg-white">
        {/* 특정 카드만 Glass 효과 */}
        <div className="bg-white/10 backdrop-blur-xl rounded-3xl border border-white/20">
          {/* Glass card content */}
        </div>
      </section>
    </>
  )
}
```

---

*각 템플릿은 독립적으로 사용하거나 조합 전략에 따라 혼합할 수 있습니다.
Direction 결정 후 이 코드를 시작점으로 활용하세요.*
