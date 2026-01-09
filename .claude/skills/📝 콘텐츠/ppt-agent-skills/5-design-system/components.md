# Component Library

PPT Design System의 HTML 컴포넌트 라이브러리입니다.
Research 데이터를 효과적으로 시각화하기 위한 컴포넌트 모음입니다.

---

## 기본 컴포넌트

### Badge (뱃지)

```html
<span class="badge badge--primary">RESEARCH</span>
<span class="badge badge--success">VERIFIED</span>
<span class="badge badge--warning">PENDING</span>
```

```css
.badge {
  display: inline-block;
  padding: 6pt 14pt;
  font-size: 11pt;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-radius: 4pt;
}
.badge--primary { background: var(--accent); color: white; }
.badge--success { background: #22c55e; color: white; }
.badge--warning { background: #f59e0b; color: white; }
.badge--outline { background: transparent; border: 1pt solid currentColor; }
```

### Card (카드)

```html
<div class="card">
  <div class="card__header">
    <span class="card__icon">📊</span>
    <h3 class="card__title">제목</h3>
  </div>
  <div class="card__body">내용</div>
  <div class="card__footer">
    <span class="card__source">출처: Gartner 2024</span>
  </div>
</div>
```

```css
.card {
  background: var(--bg-secondary);
  padding: 24pt;
  border-radius: 12pt;
  box-shadow: 0 2pt 8pt rgba(0, 0, 0, 0.08);
}
.card__header { display: flex; align-items: center; gap: 12pt; margin-bottom: 16pt; }
.card__icon { font-size: 24pt; }
.card__title { font-size: 18pt; font-weight: 600; margin: 0; }
.card__body { font-size: 16pt; line-height: 1.6; }
.card__footer { margin-top: 16pt; padding-top: 12pt; border-top: 1pt solid var(--border); }
.card__source { font-size: 12pt; color: var(--text-secondary); }
```

### Divider (구분선)

```css
.divider { height: 1pt; background: var(--border); margin: 24pt 0; }
.divider--vertical { width: 1pt; height: 100%; margin: 0 24pt; }
.divider--dashed { background: none; border-top: 2pt dashed var(--border); }
```

---

## 데이터 시각화 컴포넌트

### Metric Box (핵심 지표)

```html
<div class="metric-box">
  <div class="metric-box__value">$2M</div>
  <div class="metric-box__label">연간 손실</div>
  <div class="metric-box__delta metric-box__delta--negative">
    <span class="delta-icon">↓</span> 15% 감소
  </div>
  <div class="metric-box__source">(내부 감사 2024)</div>
</div>
```

```css
.metric-box {
  background: var(--bg-secondary);
  padding: 32pt;
  border-radius: 16pt;
  text-align: center;
  min-width: 180pt;
}
.metric-box__value {
  font-size: 60pt;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 8pt;
}
.metric-box__label {
  font-size: 16pt;
  color: var(--text-secondary);
  margin-bottom: 12pt;
}
.metric-box__delta {
  font-size: 14pt;
  font-weight: 500;
  padding: 4pt 12pt;
  border-radius: 20pt;
  display: inline-block;
}
.metric-box__delta--positive { background: #dcfce7; color: #166534; }
.metric-box__delta--negative { background: #fee2e2; color: #991b1b; }
.metric-box__source {
  font-size: 11pt;
  color: var(--text-secondary);
  margin-top: 12pt;
}
```

### Metric Row (가로 지표 배열)

```html
<div class="metric-row">
  <div class="metric-row__item">
    <span class="metric-row__value">85%</span>
    <span class="metric-row__label">정확도</span>
  </div>
  <div class="metric-row__divider"></div>
  <div class="metric-row__item">
    <span class="metric-row__value">2.5x</span>
    <span class="metric-row__label">속도</span>
  </div>
  <div class="metric-row__divider"></div>
  <div class="metric-row__item">
    <span class="metric-row__value">$1.2M</span>
    <span class="metric-row__label">절감</span>
  </div>
</div>
```

```css
.metric-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48pt;
  padding: 32pt;
}
.metric-row__item { text-align: center; }
.metric-row__value { display: block; font-size: 48pt; font-weight: 700; color: var(--accent); }
.metric-row__label { display: block; font-size: 14pt; color: var(--text-secondary); margin-top: 8pt; }
.metric-row__divider { width: 1pt; height: 60pt; background: var(--border); }
```

### Comparison Table (비교 테이블)

```html
<div class="comparison-table">
  <div class="comparison-table__header">
    <div class="comparison-table__cell"></div>
    <div class="comparison-table__cell comparison-table__cell--highlight">Our Solution</div>
    <div class="comparison-table__cell">Competitor A</div>
    <div class="comparison-table__cell">Competitor B</div>
  </div>
  <div class="comparison-table__row">
    <div class="comparison-table__cell comparison-table__cell--label">가격</div>
    <div class="comparison-table__cell comparison-table__cell--highlight">$99/월</div>
    <div class="comparison-table__cell">$149/월</div>
    <div class="comparison-table__cell">$199/월</div>
  </div>
  <div class="comparison-table__row">
    <div class="comparison-table__cell comparison-table__cell--label">속도</div>
    <div class="comparison-table__cell comparison-table__cell--highlight">
      <span class="check-icon">✓</span> 2x 빠름
    </div>
    <div class="comparison-table__cell">기본</div>
    <div class="comparison-table__cell">기본</div>
  </div>
</div>
```

```css
.comparison-table {
  width: 100%;
  border-collapse: collapse;
}
.comparison-table__header {
  display: grid;
  grid-template-columns: 1fr repeat(3, 1fr);
  background: var(--bg-secondary);
  font-weight: 600;
}
.comparison-table__row {
  display: grid;
  grid-template-columns: 1fr repeat(3, 1fr);
  border-bottom: 1pt solid var(--border);
}
.comparison-table__cell {
  padding: 16pt;
  text-align: center;
  font-size: 14pt;
}
.comparison-table__cell--label {
  text-align: left;
  font-weight: 500;
  background: var(--bg-secondary);
}
.comparison-table__cell--highlight {
  background: rgba(var(--accent-rgb), 0.1);
  color: var(--accent);
  font-weight: 600;
}
.check-icon { color: #22c55e; margin-right: 4pt; }
```

### Progress Bar (진행률)

```html
<div class="progress">
  <div class="progress__label">
    <span>프로젝트 진행률</span>
    <span>75%</span>
  </div>
  <div class="progress__bar">
    <div class="progress__fill" style="width: 75%"></div>
  </div>
</div>
```

```css
.progress { margin: 16pt 0; }
.progress__label {
  display: flex;
  justify-content: space-between;
  font-size: 14pt;
  margin-bottom: 8pt;
}
.progress__bar {
  height: 12pt;
  background: var(--bg-secondary);
  border-radius: 6pt;
  overflow: hidden;
}
.progress__fill {
  height: 100%;
  background: var(--accent);
  border-radius: 6pt;
  transition: width 0.3s ease;
}
```

---

## Quote & Citation 컴포넌트

### Quote Block (인용문)

```html
<blockquote class="quote-block">
  <div class="quote-block__mark">"</div>
  <p class="quote-block__text">
    The only way to do great work is to love what you do.
  </p>
  <footer class="quote-block__attribution">
    <cite class="quote-block__author">Steve Jobs</cite>
    <span class="quote-block__role">CEO, Apple</span>
  </footer>
</blockquote>
```

```css
.quote-block {
  position: relative;
  padding: 48pt 64pt;
  text-align: center;
}
.quote-block__mark {
  font-size: 120pt;
  color: var(--accent);
  opacity: 0.2;
  position: absolute;
  top: 0;
  left: 32pt;
  line-height: 1;
}
.quote-block__text {
  font-size: 32pt;
  font-style: italic;
  line-height: 1.4;
  margin: 0 0 24pt;
}
.quote-block__attribution { font-size: 16pt; }
.quote-block__author { font-weight: 600; display: block; }
.quote-block__role { color: var(--text-secondary); }
```

### Citation Footnote (출처 각주)

```html
<div class="citation-footnote">
  <sup class="citation-footnote__number">1</sup>
  <span class="citation-footnote__text">Gartner AI Market Report, November 2024</span>
</div>
```

```css
.citation-footnote {
  font-size: 11pt;
  color: var(--text-secondary);
  display: flex;
  align-items: baseline;
  gap: 4pt;
}
.citation-footnote__number {
  font-size: 9pt;
  color: var(--accent);
}
```

### Source Badge (출처 뱃지)

```html
<span class="source-badge">
  <span class="source-badge__icon">📊</span>
  <span class="source-badge__text">Gartner 2024</span>
</span>
```

```css
.source-badge {
  display: inline-flex;
  align-items: center;
  gap: 6pt;
  padding: 4pt 10pt;
  background: var(--bg-secondary);
  border-radius: 12pt;
  font-size: 11pt;
  color: var(--text-secondary);
}
```

---

## 리스트 & 불릿 컴포넌트

### Icon List (아이콘 리스트)

```html
<ul class="icon-list">
  <li class="icon-list__item">
    <span class="icon-list__icon">✓</span>
    <span class="icon-list__text">첫 번째 포인트</span>
    <span class="icon-list__source">(McKinsey, 2024)</span>
  </li>
  <li class="icon-list__item">
    <span class="icon-list__icon">✓</span>
    <span class="icon-list__text">두 번째 포인트</span>
  </li>
</ul>
```

```css
.icon-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.icon-list__item {
  display: flex;
  align-items: flex-start;
  gap: 12pt;
  padding: 12pt 0;
  font-size: 18pt;
  line-height: 1.5;
}
.icon-list__icon {
  flex-shrink: 0;
  width: 24pt;
  height: 24pt;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  font-size: 14pt;
}
.icon-list__text { flex: 1; }
.icon-list__source {
  font-size: 12pt;
  color: var(--text-secondary);
  white-space: nowrap;
}
```

### Numbered List (번호 리스트)

```html
<ol class="numbered-list">
  <li class="numbered-list__item">
    <span class="numbered-list__number">01</span>
    <div class="numbered-list__content">
      <h4 class="numbered-list__title">첫 번째 단계</h4>
      <p class="numbered-list__desc">상세 설명이 여기에 들어갑니다.</p>
    </div>
  </li>
</ol>
```

```css
.numbered-list {
  list-style: none;
  padding: 0;
  counter-reset: item;
}
.numbered-list__item {
  display: flex;
  align-items: flex-start;
  gap: 24pt;
  padding: 24pt 0;
  border-bottom: 1pt solid var(--border);
}
.numbered-list__number {
  font-size: 36pt;
  font-weight: 700;
  color: var(--accent);
  opacity: 0.5;
  min-width: 60pt;
}
.numbered-list__title {
  font-size: 20pt;
  font-weight: 600;
  margin: 0 0 8pt;
}
.numbered-list__desc {
  font-size: 16pt;
  color: var(--text-secondary);
  margin: 0;
}
```

---

## 타임라인 & 프로세스 컴포넌트

### Timeline Horizontal (가로 타임라인)

```html
<div class="timeline-h">
  <div class="timeline-h__item timeline-h__item--active">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q1 2024</div>
    <div class="timeline-h__title">계획</div>
  </div>
  <div class="timeline-h__line"></div>
  <div class="timeline-h__item">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q2 2024</div>
    <div class="timeline-h__title">개발</div>
  </div>
  <div class="timeline-h__line"></div>
  <div class="timeline-h__item">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q3 2024</div>
    <div class="timeline-h__title">출시</div>
  </div>
</div>
```

```css
.timeline-h {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 32pt 0;
}
.timeline-h__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120pt;
}
.timeline-h__dot {
  width: 16pt;
  height: 16pt;
  background: var(--border);
  border-radius: 50%;
  margin-bottom: 12pt;
}
.timeline-h__item--active .timeline-h__dot {
  background: var(--accent);
  box-shadow: 0 0 0 4pt rgba(var(--accent-rgb), 0.2);
}
.timeline-h__line {
  flex: 1;
  height: 2pt;
  background: var(--border);
  margin-top: 7pt;
  min-width: 60pt;
}
.timeline-h__label {
  font-size: 12pt;
  color: var(--text-secondary);
}
.timeline-h__title {
  font-size: 16pt;
  font-weight: 600;
  margin-top: 4pt;
}
```

### Process Flow (프로세스 플로우)

```html
<div class="process-flow">
  <div class="process-flow__step">
    <div class="process-flow__icon">1</div>
    <div class="process-flow__content">
      <h4>데이터 수집</h4>
      <p>다양한 소스에서 데이터 수집</p>
    </div>
  </div>
  <div class="process-flow__arrow">→</div>
  <div class="process-flow__step">
    <div class="process-flow__icon">2</div>
    <div class="process-flow__content">
      <h4>분석</h4>
      <p>AI 기반 데이터 분석</p>
    </div>
  </div>
  <div class="process-flow__arrow">→</div>
  <div class="process-flow__step">
    <div class="process-flow__icon">3</div>
    <div class="process-flow__content">
      <h4>인사이트</h4>
      <p>액션 가능한 인사이트 도출</p>
    </div>
  </div>
</div>
```

```css
.process-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16pt;
}
.process-flow__step {
  display: flex;
  align-items: center;
  gap: 16pt;
  background: var(--bg-secondary);
  padding: 20pt 24pt;
  border-radius: 12pt;
}
.process-flow__icon {
  width: 40pt;
  height: 40pt;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18pt;
}
.process-flow__content h4 {
  font-size: 16pt;
  margin: 0 0 4pt;
}
.process-flow__content p {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 0;
}
.process-flow__arrow {
  font-size: 24pt;
  color: var(--accent);
}
```

---

## 팀 & 프로필 컴포넌트

### Team Card (팀 카드)

```html
<div class="team-card">
  <div class="team-card__avatar">
    <img src="avatar.jpg" alt="Name">
  </div>
  <h4 class="team-card__name">홍길동</h4>
  <p class="team-card__role">CEO & Founder</p>
  <p class="team-card__bio">10년 경력의 테크 리더</p>
  <div class="team-card__links">
    <a href="#">LinkedIn</a>
    <a href="#">Twitter</a>
  </div>
</div>
```

```css
.team-card {
  text-align: center;
  padding: 24pt;
}
.team-card__avatar {
  width: 100pt;
  height: 100pt;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 16pt;
  background: var(--bg-secondary);
}
.team-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.team-card__name {
  font-size: 18pt;
  font-weight: 600;
  margin: 0 0 4pt;
}
.team-card__role {
  font-size: 14pt;
  color: var(--accent);
  margin: 0 0 8pt;
}
.team-card__bio {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 0;
}
.team-card__links {
  margin-top: 12pt;
  display: flex;
  justify-content: center;
  gap: 12pt;
}
.team-card__links a {
  font-size: 12pt;
  color: var(--accent);
}
```

### Case Study Card (사례 연구 카드)

고객 성공 사례를 요약 카드 형태로 표현합니다.

```html
<div class="case-card">
  <div class="case-card__header">
    <img class="case-card__logo" src="company-logo.png" alt="삼성전자">
    <div class="case-card__company">
      <span class="case-card__name">삼성전자</span>
      <span class="case-card__industry">전자/IT</span>
    </div>
  </div>
  <div class="case-card__body">
    <h4 class="case-card__headline">생산성 40% 향상</h4>
    <p class="case-card__summary">수작업 오류 문제를 AI 자동화로 해결</p>
  </div>
  <div class="case-card__metrics">
    <div class="case-card__metric">
      <span class="case-card__metric-value case-card__metric-value--up">+40%</span>
      <span class="case-card__metric-label">생산성</span>
    </div>
    <div class="case-card__metric">
      <span class="case-card__metric-value case-card__metric-value--down">-90%</span>
      <span class="case-card__metric-label">오류율</span>
    </div>
  </div>
  <div class="case-card__testimonial">
    <p class="case-card__quote">"AutoFlow 도입 후 팀 생산성이 40% 향상되었습니다."</p>
    <span class="case-card__author">— 김철수, IT팀장</span>
  </div>
</div>
```

```css
.case-card {
  background: var(--bg-secondary);
  border-radius: 16pt;
  padding: 24pt;
  border-left: 4pt solid var(--accent);
}
.case-card__header {
  display: flex;
  align-items: center;
  gap: 16pt;
  margin-bottom: 20pt;
}
.case-card__logo {
  width: 48pt;
  height: 48pt;
  object-fit: contain;
  border-radius: 8pt;
  background: white;
  padding: 4pt;
}
.case-card__name {
  display: block;
  font-size: 16pt;
  font-weight: 600;
}
.case-card__industry {
  display: block;
  font-size: 12pt;
  color: var(--text-secondary);
}
.case-card__headline {
  font-size: 24pt;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 8pt;
}
.case-card__summary {
  font-size: 14pt;
  color: var(--text-secondary);
  margin: 0;
}
.case-card__metrics {
  display: flex;
  gap: 24pt;
  margin-top: 20pt;
  padding-top: 16pt;
  border-top: 1pt solid var(--border);
}
.case-card__metric {
  text-align: center;
}
.case-card__metric-value {
  display: block;
  font-size: 28pt;
  font-weight: 700;
}
.case-card__metric-value--up {
  color: #22c55e;
}
.case-card__metric-value--down {
  color: #22c55e; /* 오류 감소는 긍정적이므로 녹색 */
}
.case-card__metric-label {
  display: block;
  font-size: 12pt;
  color: var(--text-secondary);
  margin-top: 4pt;
}
.case-card__testimonial {
  margin-top: 16pt;
  padding-top: 16pt;
  border-top: 1pt solid var(--border);
}
.case-card__quote {
  font-size: 14pt;
  font-style: italic;
  color: var(--text-primary);
  margin: 0 0 8pt;
}
.case-card__author {
  font-size: 12pt;
  color: var(--text-secondary);
}
```

### Case Study Grid (사례 그리드)

여러 고객 사례를 그리드로 배치합니다.

```html
<div class="case-grid">
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="samsung.png" alt="삼성전자">
    <h4 class="case-card__headline">생산성 40%↑</h4>
    <span class="case-card__industry">전자/IT</span>
  </div>
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="hyundai.png" alt="현대자동차">
    <h4 class="case-card__headline">오류 90%↓</h4>
    <span class="case-card__industry">자동차</span>
  </div>
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="kakao.png" alt="카카오">
    <h4 class="case-card__headline">비용 50%↓</h4>
    <span class="case-card__industry">IT서비스</span>
  </div>
</div>
```

```css
.case-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24pt;
}
.case-card--compact {
  text-align: center;
  border-left: none;
  border-top: 4pt solid var(--accent);
}
.case-card--compact .case-card__logo {
  width: 64pt;
  height: 64pt;
  margin: 0 auto 12pt;
}
.case-card--compact .case-card__headline {
  font-size: 20pt;
  margin-bottom: 4pt;
}
```

---

## CTA & 버튼 컴포넌트

### Button Group (버튼 그룹)

```html
<div class="button-group">
  <button class="btn btn--primary">시작하기</button>
  <button class="btn btn--secondary">자세히 보기</button>
</div>
```

```css
.button-group {
  display: flex;
  gap: 16pt;
  justify-content: center;
}
.btn {
  padding: 14pt 32pt;
  font-size: 16pt;
  font-weight: 600;
  border-radius: 8pt;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
.btn--primary {
  background: var(--accent);
  color: white;
}
.btn--secondary {
  background: transparent;
  border: 2pt solid var(--accent);
  color: var(--accent);
}
.btn--large {
  padding: 18pt 48pt;
  font-size: 18pt;
}
```

### CTA Box (CTA 박스)

```html
<div class="cta-box">
  <h3 class="cta-box__title">지금 시작하세요</h3>
  <p class="cta-box__desc">30일 무료 체험으로 시작해보세요</p>
  <button class="btn btn--primary btn--large">무료 체험 시작</button>
  <p class="cta-box__note">신용카드 불필요</p>
</div>
```

```css
.cta-box {
  text-align: center;
  padding: 48pt;
  background: var(--bg-secondary);
  border-radius: 16pt;
}
.cta-box__title {
  font-size: 32pt;
  font-weight: 700;
  margin: 0 0 12pt;
}
.cta-box__desc {
  font-size: 18pt;
  color: var(--text-secondary);
  margin: 0 0 24pt;
}
.cta-box__note {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 16pt 0 0;
}
```

---

## 레이아웃 헬퍼

### Grid System (그리드 시스템)

```css
/* 균등 분할 그리드 */
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32pt; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24pt; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20pt; }

/* 비대칭 그리드 */
.grid-1-2 { display: grid; grid-template-columns: 1fr 2fr; gap: 32pt; }
.grid-2-1 { display: grid; grid-template-columns: 2fr 1fr; gap: 32pt; }
.grid-golden { display: grid; grid-template-columns: 1fr 1.618fr; gap: 32pt; }

/* 콘텐츠+비주얼 */
.grid-content-visual { display: grid; grid-template-columns: 2fr 3fr; gap: 32pt; align-items: center; }
.grid-visual-content { display: grid; grid-template-columns: 3fr 2fr; gap: 32pt; align-items: center; }
```

### Flexbox Helpers

```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-center { justify-content: center; align-items: center; }
.flex-between { justify-content: space-between; }
.flex-wrap { flex-wrap: wrap; }
.gap-sm { gap: 12pt; }
.gap-md { gap: 24pt; }
.gap-lg { gap: 48pt; }
```

### Spacing Utilities

```css
.mt-0 { margin-top: 0; }
.mt-sm { margin-top: 12pt; }
.mt-md { margin-top: 24pt; }
.mt-lg { margin-top: 48pt; }
.mb-0 { margin-bottom: 0; }
.mb-sm { margin-bottom: 12pt; }
.mb-md { margin-bottom: 24pt; }
.mb-lg { margin-bottom: 48pt; }
.p-0 { padding: 0; }
.p-sm { padding: 12pt; }
.p-md { padding: 24pt; }
.p-lg { padding: 48pt; }
```

---

## 컴포넌트-데이터 타입 매핑

| data_type | 1순위 컴포넌트 | 2순위 컴포넌트 | 선택 기준 |
|-----------|--------------|--------------|----------|
| `statistic` | metric-box | metric-row | 단일 지표 vs 복수 지표 |
| `quote` | quote-block | case-card (testimonial) | 독립 인용 vs 사례 내 인용 |
| `case_study` | case-card | process-flow | outcome 중심 vs 과정 중심 |
| `comparison` | comparison-table | metric-row | 다항목 비교 vs 핵심 수치 비교 |
| `trend` | timeline-h | line-chart | 마일스톤 중심 vs 연속 데이터 |
| `roadmap` | timeline-h | numbered-list | 시각적 강조 vs 텍스트 중심 |
| `team` | team-card (grid-4) | icon-list | 상세 프로필 vs 간단 목록 |
| `cta` | cta-box | button-group | 강조 CTA vs 옵션 제시 |

**Visual Type 자동 선택 로직:**

```
data_type 확인
    │
    ├─ statistic
    │     ├─ 단일 값 → metric-box
    │     └─ 복수 값 (2-4개) → metric-row
    │
    ├─ case_study
    │     ├─ steps 배열 존재 → process-flow
    │     ├─ outcome_metrics 존재 → case-card
    │     └─ testimonial만 존재 → quote-block + source-badge
    │
    ├─ trend
    │     ├─ milestones 배열 존재 → timeline-h
    │     └─ 연속 데이터 → line-chart
    │
    └─ comparison
          ├─ 3개 이상 항목 → comparison-table
          └─ 2개 항목 → metric-row (before/after)
```

---

## 컴포넌트 조합 예시

### 문제 정의 슬라이드

```html
<section class="slide slide--problem">
  <header class="slide__header">
    <span class="badge badge--outline">PROBLEM</span>
    <span class="slide__number">05</span>
  </header>

  <h1 class="slide__title">수작업 오류로 연간 $2M 손실</h1>

  <div class="grid-content-visual">
    <div class="slide__content">
      <ul class="icon-list">
        <li class="icon-list__item">
          <span class="icon-list__icon">!</span>
          <span class="icon-list__text">수작업 데이터 입력 오류율 15%</span>
          <span class="icon-list__source">(운영팀 조사)</span>
        </li>
        <li class="icon-list__item">
          <span class="icon-list__icon">!</span>
          <span class="icon-list__text">직원 40% 업무시간 수동 작업에 소비</span>
          <span class="icon-list__source">(직원 설문)</span>
        </li>
      </ul>
    </div>
    <div class="slide__visual">
      <div class="metric-box">
        <div class="metric-box__value">$2M</div>
        <div class="metric-box__label">연간 손실</div>
        <div class="metric-box__source">(내부 감사 2024)</div>
      </div>
    </div>
  </div>

  <footer class="slide__footer">
    <div class="citation-footnote">
      <sup>1</sup> 내부 감사 보고서 2024, n=500 거래 분석
    </div>
  </footer>
</section>
```

### 솔루션 슬라이드

```html
<section class="slide slide--solution">
  <header class="slide__header">
    <span class="badge badge--primary">SOLUTION</span>
  </header>

  <h1 class="slide__title">3단계 자동화로 오류율 90% 감소</h1>

  <div class="process-flow mt-lg">
    <div class="process-flow__step">
      <div class="process-flow__icon">1</div>
      <div class="process-flow__content">
        <h4>데이터 수집 자동화</h4>
        <p>API 연동으로 수동 입력 제거</p>
      </div>
    </div>
    <div class="process-flow__arrow">→</div>
    <div class="process-flow__step">
      <div class="process-flow__icon">2</div>
      <div class="process-flow__content">
        <h4>AI 검증</h4>
        <p>실시간 오류 탐지 및 수정</p>
      </div>
    </div>
    <div class="process-flow__arrow">→</div>
    <div class="process-flow__step">
      <div class="process-flow__icon">3</div>
      <div class="process-flow__content">
        <h4>대시보드</h4>
        <p>실시간 모니터링 및 알림</p>
      </div>
    </div>
  </div>

  <div class="metric-row mt-lg">
    <div class="metric-row__item">
      <span class="metric-row__value">90%</span>
      <span class="metric-row__label">오류 감소</span>
    </div>
    <div class="metric-row__divider"></div>
    <div class="metric-row__item">
      <span class="metric-row__value">3개월</span>
      <span class="metric-row__label">ROI 달성</span>
    </div>
    <div class="metric-row__divider"></div>
    <div class="metric-row__item">
      <span class="metric-row__value">$1.8M</span>
      <span class="metric-row__label">연간 절감</span>
    </div>
  </div>
</section>
```
