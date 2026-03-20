# ANTI-PATTERNS.md

피해야 할 디자인 안티패턴과 AI 슬롭 체크리스트

---

## 목차

1. [금지 폰트](#금지-폰트)
2. [금지 색상 조합](#금지-색상-조합)
3. [제네릭 패턴](#제네릭-패턴)
4. [AI 슬롭 체크리스트](#ai-슬롭-체크리스트)
5. [독창성 평가 방법](#독창성-평가-방법)
6. [흔한 실수들](#흔한-실수들)
7. [레드 플래그 패턴](#레드-플래그-패턴)

---

## 금지 폰트

### 절대 사용 금지 폰트

| 폰트 | 금지 이유 | 대안 |
|------|----------|------|
| **Comic Sans MS** | 비전문적, 아마추어적 느낌 | Quicksand, Baloo 2, Nunito |
| **Papyrus** | 클리셰, Avatar 밈 | Spectral, Cormorant, Lora |
| **Impact** | 밈/인터넷 클리셰 | Bebas Neue, Oswald, Anton |
| **Brush Script** | 시대에 뒤떨어짐, 저품질 | Dancing Script, Pacifico |
| **Curlz MT** | 전문성 부족 | Fredoka, Comfortaa |
| **Jokerman** | 진지한 프로젝트에 부적합 | Bangers, Bungee |
| **Chiller** | 저품질, 읽기 어려움 | Creepster, Nosifer |
| **Lucida Handwriting** | 가짜 필기체 느낌 | Caveat, Kalam |
| **Kristen ITC** | 아동용 같은 느낌 | Patrick Hand |
| **Bleeding Cowboys** | 과도하게 스타일화 | Special Elite |

### 주의가 필요한 폰트

| 폰트 | 문제점 | 사용 가능 상황 |
|------|--------|---------------|
| **Arial** | 너무 기본적, 개성 없음 | 시스템 폴백용으로만 |
| **Times New Roman** | 기본값 느낌, 게으름 | 학술 문서만 |
| **Helvetica** | 비용 문제, Arial과 혼동 | 라이선스 있을 때만 |
| **Lobster** | 과도한 사용으로 클리셰화 | 빈티지/레트로 한정 |
| **Raleway** | 너무 흔함 | 더 나은 대안 없을 때 |
| **Open Sans** | 너무 중립적, 무개성 | 폴백 용도 |
| **Montserrat** | 너무 흔해짐 | 브랜딩 프로젝트 피하기 |
| **Pacifico** | 과도한 사용 | 캐주얼 용도 한정 |

### 한글 폰트 주의사항

| 폰트 | 문제점 | 대안 |
|------|--------|------|
| **굴림/돋움** | 시스템 기본, 구시대적 | Pretendard, SUIT |
| **맑은 고딕** | 기본값 느낌 | Spoqa Han Sans Neo |
| **HY헤드라인** | 90년대 스타일 | Gmarket Sans |
| **궁서** | 과도한 장식, 가독성 낮음 | Nanum Myeongjo |
| **바탕체** | 화면용으로 부적합 | KoPub Batang |

---

## 금지 색상 조합

### 접근성 위반 조합

```css
/* AVOID: Low contrast combinations */
.bad-contrast-1 {
  background: oklch(90% 0.02 250);
  color: oklch(85% 0.02 250);  /* Ratio: ~1.3:1 - FAIL */
}

.bad-contrast-2 {
  background: oklch(50% 0.15 120);
  color: oklch(55% 0.12 120);  /* Ratio: ~1.2:1 - FAIL */
}

/* GOOD: High contrast alternatives */
.good-contrast-1 {
  background: oklch(95% 0.02 250);
  color: oklch(20% 0.02 250);  /* Ratio: ~10:1 - PASS */
}

.good-contrast-2 {
  background: oklch(50% 0.15 120);
  color: oklch(98% 0.01 120);  /* Ratio: ~5:1 - PASS */
}
```

### 시각적 불쾌함을 주는 조합

| 조합 | 문제점 | 대안 |
|------|--------|------|
| **빨강 + 초록 (같은 채도)** | 색맹 접근성 문제, 진동 효과 | 명도 차이 추가 |
| **파랑 + 빨강 (순색)** | 색 진동, 눈의 피로 | 채도 낮추기 |
| **노랑 + 보라 (순색)** | 과도한 대비 | 톤 조절 |
| **네온 핑크 + 네온 그린** | 90년대 클리셰 | 한 색만 강조 |
| **검정 + 갈색** | 칙칙함, 우울함 | 따뜻한 그레이 사용 |

### 클리셰 색상 조합

```tsx
// AVOID: Overused tech startup colors
const clicheTechPalette = {
  primary: '#6366F1',    // Indigo - too common
  secondary: '#8B5CF6',  // Purple gradient - everyone uses this
  accent: '#EC4899',     // Pink - Stripe/Vercel copy
};

// AVOID: Generic corporate blue
const boringCorporate = {
  primary: '#0066CC',    // Every bank ever
  secondary: '#003366',  // Navy - overdone
};

// AVOID: Startup template colors
const startupTemplate = {
  primary: '#667EEA',    // Purple-blue gradient start
  secondary: '#764BA2',  // Purple-blue gradient end
};
```

### 색상 조합 규칙

1. **60-30-10 법칙을 무시하지 말 것**
   - 60% 기본색, 30% 보조색, 10% 강조색

2. **5가지 이상 색상 사용 자제**
   - 대부분의 디자인은 3-4개 색상으로 충분

3. **무채색 없이 유채색만 사용 금지**
   - 항상 중립색(그레이)을 포함

---

## 제네릭 패턴

### 피해야 할 히어로 섹션 패턴

```tsx
// AVOID: Generic startup hero
function GenericHero() {
  return (
    <section className="bg-gradient-to-r from-purple-600 to-blue-600 min-h-screen flex items-center">
      <div className="container mx-auto text-center text-white">
        <h1 className="text-6xl font-bold">
          The Future of [X]
        </h1>
        <p className="text-xl mt-4 opacity-80">
          Revolutionizing the way you [verb] with AI-powered [noun]
        </p>
        <button className="mt-8 px-8 py-4 bg-white text-purple-600 rounded-full">
          Get Started Free
        </button>
      </div>
    </section>
  );
}

// BETTER: Unique approach
function UniqueHero() {
  return (
    <section className="min-h-screen relative overflow-hidden">
      {/* Custom visual element instead of gradient */}
      <div className="absolute inset-0 grid grid-cols-8 gap-px opacity-10">
        {/* Unique grid pattern */}
      </div>

      {/* Asymmetric layout */}
      <div className="container mx-auto grid lg:grid-cols-12 items-center min-h-screen">
        <div className="lg:col-span-7 lg:col-start-2">
          {/* Distinctive typography treatment */}
          <h1 className="text-7xl font-bold leading-none tracking-tighter">
            <span className="block">Ship</span>
            <span className="block text-primary">faster.</span>
          </h1>
        </div>
      </div>
    </section>
  );
}
```

### 피해야 할 카드 패턴

```tsx
// AVOID: Generic feature card
function GenericCard() {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 text-center">
      <div className="w-16 h-16 mx-auto mb-4 bg-purple-100 rounded-full flex items-center justify-center">
        <Icon className="w-8 h-8 text-purple-600" />
      </div>
      <h3 className="text-xl font-semibold mb-2">Feature Name</h3>
      <p className="text-gray-600">
        Lorem ipsum dolor sit amet consectetur adipiscing elit.
      </p>
    </div>
  );
}

// BETTER: Distinctive card
function UniqueCard() {
  return (
    <div className="group relative">
      {/* Unique border treatment */}
      <div className="absolute -inset-px bg-gradient-to-r from-primary/20 to-transparent rounded-2xl" />

      <div className="relative bg-card rounded-2xl p-8 h-full">
        {/* Icon in unusual position */}
        <div className="absolute -top-3 -right-3 w-12 h-12 bg-primary rounded-xl flex items-center justify-center shadow-lg">
          <Icon className="w-6 h-6 text-primary-foreground" />
        </div>

        <h3 className="text-xl font-semibold mb-4 pr-8">Feature Name</h3>
        <p className="text-muted-foreground leading-relaxed">
          Specific, meaningful description.
        </p>
      </div>
    </div>
  );
}
```

### 피해야 할 레이아웃 패턴

| 패턴 | 문제점 | 대안 |
|------|--------|------|
| **3열 등간격 그리드** | 모든 SaaS가 사용 | 비대칭 그리드, 벤토 |
| **중앙 정렬 모든 것** | 지루함, 긴장감 없음 | 비대칭 정렬 |
| **아이콘 + 제목 + 설명** | Feature 섹션 클리셰 | 색다른 정보 구조 |
| **좌우 지그재그 레이아웃** | About 페이지 클리셰 | 오버랩, 오프셋 |
| **원형 프로필 그리드** | Team 섹션 클리셰 | 비정형 레이아웃 |

---

## AI 슬롭 체크리스트

### AI 생성 콘텐츠 징후

#### 시각적 징후

- [ ] **과도한 대칭성**: 모든 요소가 완벽하게 대칭
- [ ] **예측 가능한 패턴**: 1-2-3 열, 반복적 구조
- [ ] **제네릭 일러스트레이션**: Undraw, Storyset 스타일의 벡터 이미지
- [ ] **스톡 이미지 느낌**: 비즈니스 사람들 악수, 다양성 체크박스
- [ ] **무한 그라데이션**: 보라-파랑 그라데이션 남용
- [ ] **과도한 둥근 모서리**: 모든 것이 rounded-full

#### 텍스트 징후

- [ ] **"AI-powered" 남발**: 모든 기능에 AI 붙이기
- [ ] **"Revolutionary" 사용**: 혁명적이라고 주장
- [ ] **"Seamlessly" 남용**: 원활하게 통합
- [ ] **"Cutting-edge"**: 최첨단 기술
- [ ] **빈 형용사**: "Powerful", "Robust", "Innovative"
- [ ] **과도한 약속**: "10x faster", "100% accurate"

### AI 슬롭 점수 매기기

```typescript
// lib/slop-detector.ts

interface SlopScore {
  visual: number;      // 0-100
  textual: number;     // 0-100
  overall: number;     // 0-100
  flags: string[];
}

const VISUAL_RED_FLAGS = [
  'purple-blue-gradient',
  'centered-everything',
  'symmetric-3-column',
  'rounded-full-overuse',
  'stock-illustration',
  'blob-shapes',
  'floating-elements-random',
];

const TEXTUAL_RED_FLAGS = [
  'AI-powered',
  'revolutionary',
  'seamlessly',
  'cutting-edge',
  'game-changing',
  'next-generation',
  'unlock',
  'leverage',
  'synergy',
];

export function detectSlop(content: {
  visualPatterns: string[];
  textContent: string;
}): SlopScore {
  const flags: string[] = [];

  // Check visual patterns
  const visualMatches = content.visualPatterns.filter(p =>
    VISUAL_RED_FLAGS.includes(p)
  );
  const visualScore = (visualMatches.length / VISUAL_RED_FLAGS.length) * 100;
  flags.push(...visualMatches.map(m => `Visual: ${m}`));

  // Check text content
  const lowerText = content.textContent.toLowerCase();
  const textMatches = TEXTUAL_RED_FLAGS.filter(flag =>
    lowerText.includes(flag.toLowerCase())
  );
  const textualScore = (textMatches.length / TEXTUAL_RED_FLAGS.length) * 100;
  flags.push(...textMatches.map(m => `Text: ${m}`));

  return {
    visual: Math.round(visualScore),
    textual: Math.round(textualScore),
    overall: Math.round((visualScore + textualScore) / 2),
    flags,
  };
}
```

### 안티 AI 슬롭 디자인 원칙

1. **의도적 불완전함**
   - 완벽한 대칭 피하기
   - 약간의 불규칙성 추가

2. **구체적 언어 사용**
   - "AI-powered" 대신 구체적 기능 설명
   - 숫자와 사례로 증명

3. **커스텀 비주얼**
   - 스톡 이미지 대신 맞춤 사진/일러스트
   - 브랜드 고유 그래픽 요소

4. **인간적 터치**
   - 손글씨 느낌 요소
   - 불완전한 선, 텍스처

---

## 독창성 평가 방법

### 독창성 체크리스트

```typescript
// lib/originality-checker.ts

interface OriginalityCheck {
  score: number;        // 0-100
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
}

const ORIGINALITY_CRITERIA = {
  typography: {
    weight: 20,
    checks: [
      { name: 'customFont', desc: '커스텀/희귀 폰트 사용', points: 5 },
      { name: 'uniquePairing', desc: '독특한 폰트 조합', points: 5 },
      { name: 'creativeHierarchy', desc: '창의적 위계 구조', points: 5 },
      { name: 'noDefaultFonts', desc: '기본 폰트 미사용', points: 5 },
    ],
  },
  color: {
    weight: 20,
    checks: [
      { name: 'uniquePalette', desc: '독특한 색상 팔레트', points: 5 },
      { name: 'noTemplateColors', desc: '템플릿 색상 미사용', points: 5 },
      { name: 'intentionalAccent', desc: '의도적 강조색 사용', points: 5 },
      { name: 'darkModeThought', desc: '다크모드 고려', points: 5 },
    ],
  },
  layout: {
    weight: 25,
    checks: [
      { name: 'asymmetricGrid', desc: '비대칭 그리드', points: 6 },
      { name: 'unusualSpacing', desc: '의도적 여백', points: 6 },
      { name: 'breakingGrid', desc: '그리드 브레이킹', points: 6 },
      { name: 'creativeOverlap', desc: '창의적 오버랩', points: 7 },
    ],
  },
  motion: {
    weight: 15,
    checks: [
      { name: 'customEasing', desc: '커스텀 이징', points: 4 },
      { name: 'meaningfulAnimation', desc: '의미 있는 애니메이션', points: 4 },
      { name: 'microInteractions', desc: '마이크로 인터랙션', points: 4 },
      { name: 'reducedMotionSupport', desc: '모션 감소 지원', points: 3 },
    ],
  },
  content: {
    weight: 20,
    checks: [
      { name: 'specificLanguage', desc: '구체적 언어', points: 5 },
      { name: 'noGenericPhrases', desc: '제네릭 문구 미사용', points: 5 },
      { name: 'realExamples', desc: '실제 사례/데이터', points: 5 },
      { name: 'brandVoice', desc: '고유한 브랜드 보이스', points: 5 },
    ],
  },
};

export function evaluateOriginality(
  responses: Record<string, boolean>
): OriginalityCheck {
  let totalScore = 0;
  const strengths: string[] = [];
  const weaknesses: string[] = [];

  for (const [category, config] of Object.entries(ORIGINALITY_CRITERIA)) {
    for (const check of config.checks) {
      if (responses[check.name]) {
        totalScore += check.points;
        strengths.push(check.desc);
      } else {
        weaknesses.push(check.desc);
      }
    }
  }

  return {
    score: totalScore,
    strengths,
    weaknesses,
    suggestions: generateSuggestions(weaknesses),
  };
}
```

### 경쟁사 분석 체크리스트

1. **폰트 차별화**
   - [ ] 경쟁사와 다른 폰트 패밀리 사용
   - [ ] 독특한 웨이트/스타일 조합
   - [ ] 커스텀 폰트 고려

2. **색상 차별화**
   - [ ] 업계 표준 색상 피하기
   - [ ] 독특한 강조색 선택
   - [ ] 경쟁사 색상 분석 완료

3. **레이아웃 차별화**
   - [ ] 경쟁사와 다른 구조
   - [ ] 독특한 정보 구조
   - [ ] 차별화된 네비게이션

4. **비주얼 차별화**
   - [ ] 커스텀 그래픽 요소
   - [ ] 브랜드 고유 일러스트레이션
   - [ ] 독특한 사진 스타일

---

## 흔한 실수들

### UI/UX 실수

#### 1. 모달 남용

```tsx
// BAD: Modal for everything
function ModalAbuse() {
  return (
    <>
      <button onClick={() => setShowSettings(true)}>Settings</button>
      <button onClick={() => setShowHelp(true)}>Help</button>
      <button onClick={() => setShowProfile(true)}>Profile</button>
      {/* 3 different modals for everything */}
    </>
  );
}

// GOOD: Use appropriate patterns
function ProperPatterns() {
  return (
    <>
      <Link href="/settings">Settings</Link> {/* Full page */}
      <Popover>Help content</Popover> {/* Popover for short info */}
      <Sheet>Profile details</Sheet> {/* Sheet for complex forms */}
    </>
  );
}
```

#### 2. 불필요한 로딩 상태

```tsx
// BAD: Loader for everything
function OverLoading() {
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner /> {/* Full page spinner for 50ms load */}
      </div>
    );
  }
  return <Content />;
}

// GOOD: Skeleton or optimistic UI
function ProperLoading() {
  return (
    <Suspense fallback={<ContentSkeleton />}>
      <Content />
    </Suspense>
  );
}
```

#### 3. 토스트 남용

```tsx
// BAD: Toast for everything
function ToastAbuse() {
  const handleClick = () => {
    toast.success('Button clicked!');  // Nobody cares
    toast.info('Loading...');          // Use loading state
    toast.success('Loaded!');          // Obviously
  };
}

// GOOD: Meaningful toasts only
function ProperToasts() {
  const handleSubmit = () => {
    // Only toast for important actions
    toast.success('Changes saved');
    // Or for errors
    toast.error('Failed to save. Please try again.');
  };
}
```

### 레이아웃 실수

#### 4. 과도한 패딩

```css
/* BAD: Excessive padding */
.card-over-padded {
  padding: 4rem; /* 64px - too much for most cards */
}

/* GOOD: Appropriate padding */
.card-proper {
  padding: 1.5rem; /* 24px - comfortable */
}

.card-large {
  padding: clamp(1.5rem, 4vw, 3rem); /* Responsive */
}
```

#### 5. 너무 좁은 컨테이너

```css
/* BAD: Too narrow for readability */
.container-too-narrow {
  max-width: 400px; /* Hard to read long text */
}

/* BAD: Too wide for comfort */
.container-too-wide {
  max-width: 1800px; /* Eye tracking fatigue */
}

/* GOOD: Optimal reading width */
.container-optimal {
  max-width: 65ch; /* 65 characters - optimal for prose */
}

/* GOOD: Flexible container */
.container-flexible {
  max-width: min(1200px, 90vw);
}
```

### 타이포그래피 실수

#### 6. 줄 길이 무시

```css
/* BAD: No line length control */
.text-uncontrolled {
  /* Text spans full container width - hard to read */
}

/* GOOD: Controlled measure */
.text-controlled {
  max-width: 65ch; /* Optimal for readability */
}

.text-wide {
  max-width: 75ch; /* For UI text */
}
```

#### 7. 행간 불일치

```css
/* BAD: Inconsistent line-height */
.heading-bad { line-height: 1.2; }
.body-bad { line-height: 1.8; }
.caption-bad { line-height: 1.3; }

/* GOOD: Systematic line-heights */
.heading { line-height: 1.1; }    /* Tight for display */
.subheading { line-height: 1.25; }
.body { line-height: 1.5; }       /* Comfortable for reading */
.caption { line-height: 1.4; }
```

---

## 레드 플래그 패턴

### 코드 레드 플래그

```tsx
// RED FLAG: Inline styles everywhere
<div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0' }}>

// RED FLAG: Magic numbers
<div className="mt-[23px] p-[11px]">

// RED FLAG: !important abuse
.override-everything {
  color: red !important;
  margin: 0 !important;
}

// RED FLAG: Deep nesting
<div className="container">
  <div className="wrapper">
    <div className="inner">
      <div className="content">
        <div className="text">
          Hello
        </div>
      </div>
    </div>
  </div>
</div>
```

### 디자인 레드 플래그

| 패턴 | 왜 문제인가 | 해결책 |
|------|------------|--------|
| **10+ 색상 사용** | 일관성 부족, 혼란 | 5색 이하로 제한 |
| **5+ 폰트 사용** | 시각적 혼란 | 2-3 폰트로 제한 |
| **일관성 없는 간격** | 비전문적 | 8px 단위 시스템 |
| **다양한 border-radius** | 정돈되지 않은 느낌 | 2-3개 값만 사용 |
| **그림자 남용** | 플랫/머티리얼 혼합 | 일관된 그림자 시스템 |

### 접근성 레드 플래그

```tsx
// RED FLAG: No alt text
<img src="hero.jpg" />

// RED FLAG: Click handler on non-interactive
<div onClick={handleClick}>Click me</div>

// RED FLAG: Color-only indication
<span className="text-red-500">Error</span>

// RED FLAG: No focus states
.button:focus {
  outline: none; /* NEVER do this without replacement */
}

// RED FLAG: Fixed font sizes
.text {
  font-size: 12px; /* Use rem */
}
```

### 성능 레드 플래그

```tsx
// RED FLAG: Unoptimized images
<img src="hero-5000x3000.jpg" />

// RED FLAG: Layout shift
function LayoutShift() {
  const [loaded, setLoaded] = useState(false);
  return loaded ? <BigContent /> : null; // No skeleton
}

// RED FLAG: Excessive re-renders
function ReRenderHell() {
  const [count, setCount] = useState(0);
  return (
    <div>
      {/* This re-renders everything on count change */}
      <HeavyComponent />
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
    </div>
  );
}

// RED FLAG: No code splitting
import { HugeLibrary } from 'huge-library';
// vs
const HugeLibrary = dynamic(() => import('huge-library'));
```

### 빠른 자가 진단

아래 항목 중 3개 이상 해당하면 디자인 재검토 필요:

- [ ] 모든 텍스트가 중앙 정렬됨
- [ ] 3열 등간격 그리드 사용
- [ ] 보라-파랑 그라데이션 사용
- [ ] "AI-powered" 또는 "Revolutionary" 사용
- [ ] 스톡 일러스트레이션 사용
- [ ] Inter/Roboto/Open Sans 기본 사용
- [ ] 모든 카드가 동일한 크기
- [ ] 움직임 없는 정적 페이지
- [ ] 경쟁사와 비슷한 색상 팔레트
- [ ] 템플릿 느낌
