const fs = require("node:fs");
const path = require("node:path");
const pptxgen = require("pptxgenjs");

const outDir = __dirname;
const outPptx = path.join(outDir, "seo-aeo-search-era.pptx");
const outOutline = path.join(outDir, "seo-aeo-search-era-outline.md");

const pptx = new pptxgen();
pptx.author = "Codex";
pptx.company = "Claude Craft";
pptx.subject = "SEO에서 AEO 검색 시대로의 전환";
pptx.title = "SEO -> AEO 검색 시대";
pptx.lang = "ko-KR";
pptx.defineLayout({ name: "WIDE_16_9", width: 13.333, height: 7.5 });
pptx.layout = "WIDE_16_9";
pptx.theme = {
  headFontFace: "Apple SD Gothic Neo",
  bodyFontFace: "Apple SD Gothic Neo",
  lang: "ko-KR",
};
pptx.margin = 0;

const SLIDE = { w: 13.333, h: 7.5 };
const FONT = "Apple SD Gothic Neo";
const COLORS = {
  bg: "F7F5EF",
  ink: "14213D",
  muted: "5F6977",
  line: "D8D5CC",
  panel: "FFFFFF",
  cobalt: "2457D6",
  teal: "0E918C",
  green: "2E8B57",
  amber: "E7A928",
  red: "D4524C",
  dark: "101827",
};

const slides = [
  {
    no: 1,
    title: "SEO -> AEO 검색 시대",
    subtitle: "링크 순위 경쟁에서 답변 채택 경쟁으로",
    takeaway: "SEO를 버리는 것이 아니라, AI 답변 레이어에 인용될 수 있는 구조를 더해야 한다.",
  },
  {
    no: 2,
    title: "검색 결과는 페이지 목록에서 답변 인터페이스로 이동한다",
    takeaway: "AI Overviews, AI Mode, ChatGPT search는 사용자가 여러 링크를 탐색하던 일을 답변·출처·후속질문 흐름으로 압축한다.",
  },
  {
    no: 3,
    title: "클릭은 줄고, 답변 안에서의 존재감이 중요해진다",
    takeaway: "Pew Research는 AI summary가 있는 Google 검색에서 전통 검색 결과 클릭률이 8%로, 없는 경우 15%보다 낮았다고 분석했다.",
  },
  {
    no: 4,
    title: "SEO와 AEO는 대체 관계가 아니라 레이어 관계다",
    takeaway: "SEO가 검색엔진의 색인과 랭킹을 다룬다면, AEO는 답변 엔진이 이해하고 인용하기 쉬운 지식 단위를 설계한다.",
  },
  {
    no: 5,
    title: "AEO 콘텐츠는 '정답 후보'로 읽히도록 설계한다",
    takeaway: "답변 블록, 엔티티 명확성, 구조화 데이터, 근거 패키지, 업데이트 루프가 함께 작동해야 한다.",
  },
  {
    no: 6,
    title: "측정 기준도 트래픽 중심에서 답변 점유율 중심으로 확장된다",
    takeaway: "검색 유입만 보던 대시보드에 AI citation, answer coverage, assisted conversion, source quality를 추가해야 한다.",
  },
  {
    no: 7,
    title: "90일 전환 로드맵",
    takeaway: "기존 SEO 자산을 감사하고, 핵심 질의별 answer page를 만든 뒤, AI citation 모니터링으로 운영 체계를 만든다.",
  },
  {
    no: 8,
    title: "결론: 검색 전략의 목표를 '랭킹'에서 '선택되는 답변'까지 넓힌다",
    takeaway: "지금 필요한 결정은 AEO 전담 조직이 아니라, SEO 운영 프로세스에 answer-readiness 기준을 넣는 것이다.",
  },
];

function addBg(slide) {
  slide.background = { color: COLORS.bg };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: SLIDE.w,
    h: SLIDE.h,
    fill: { color: COLORS.bg },
    line: { color: COLORS.bg, transparency: 100 },
  });
}

function addTopBar(slide, idx, section) {
  slide.addText("SEO -> AEO", {
    x: 0.55,
    y: 0.28,
    w: 1.8,
    h: 0.22,
    fontFace: FONT,
    fontSize: 8,
    bold: true,
    color: COLORS.cobalt,
    margin: 0,
    charSpace: 0.3,
  });
  slide.addText(section, {
    x: 2.35,
    y: 0.28,
    w: 5.4,
    h: 0.22,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    margin: 0,
  });
  slide.addText(String(idx).padStart(2, "0"), {
    x: 12.14,
    y: 0.25,
    w: 0.55,
    h: 0.22,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    align: "right",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.55,
    y: 0.65,
    w: 12.2,
    h: 0,
    line: { color: COLORS.line, width: 0.7 },
  });
}

function addFooter(slide, source) {
  slide.addShape(pptx.ShapeType.line, {
    x: 0.55,
    y: 6.92,
    w: 12.2,
    h: 0,
    line: { color: COLORS.line, width: 0.55 },
  });
  slide.addText(source || "Sample deck generated for Claude Craft environment review", {
    x: 0.55,
    y: 7.05,
    w: 11.2,
    h: 0.22,
    fontFace: FONT,
    fontSize: 6.2,
    color: COLORS.muted,
    margin: 0,
    fit: "shrink",
  });
}

function addTitle(slide, title, subtitle, opts = {}) {
  slide.addText(title, {
    x: opts.x || 0.7,
    y: opts.y || 0.95,
    w: opts.w || 9.2,
    h: opts.h || 0.92,
    fontFace: FONT,
    fontSize: opts.size || 28,
    bold: true,
    color: opts.color || COLORS.ink,
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: opts.x || 0.7,
      y: (opts.y || 0.95) + 0.88,
      w: opts.subW || 8.0,
      h: 0.42,
      fontFace: FONT,
      fontSize: opts.subSize || 13,
      color: COLORS.muted,
      margin: 0,
      fit: "shrink",
    });
  }
}

function addPill(slide, text, x, y, w, color, fill = "EEF2FF") {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h: 0.32,
    rectRadius: 0.05,
    fill: { color: fill },
    line: { color: fill, transparency: 100 },
  });
  slide.addText(text, {
    x: x + 0.12,
    y: y + 0.085,
    w: w - 0.24,
    h: 0.1,
    fontFace: FONT,
    fontSize: 7.6,
    bold: true,
    color,
    margin: 0,
    align: "center",
  });
}

function addPanel(slide, x, y, w, h, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    fill: { color: opts.fill || COLORS.panel },
    line: { color: opts.line || COLORS.line, width: opts.lineWidth || 0.7 },
  });
}

function addCard(slide, x, y, w, h, label, headline, body, color) {
  addPanel(slide, x, y, w, h);
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w: 0.08,
    h,
    fill: { color },
    line: { color, transparency: 100 },
  });
  slide.addText(label, {
    x: x + 0.22,
    y: y + 0.22,
    w: w - 0.45,
    h: 0.18,
    fontFace: FONT,
    fontSize: 7.2,
    bold: true,
    color,
    margin: 0,
  });
  slide.addText(headline, {
    x: x + 0.22,
    y: y + 0.58,
    w: w - 0.45,
    h: 0.38,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: COLORS.ink,
    margin: 0,
    fit: "shrink",
  });
  slide.addText(body, {
    x: x + 0.22,
    y: y + 1.1,
    w: w - 0.45,
    h: h - 1.25,
    fontFace: FONT,
    fontSize: 8.7,
    color: COLORS.muted,
    breakLine: false,
    margin: 0,
    fit: "shrink",
    valign: "top",
    breakLine: false,
  });
}

function addMetric(slide, x, y, w, h, value, label, color) {
  addPanel(slide, x, y, w, h, { fill: "FBFAF6" });
  slide.addText(value, {
    x: x + 0.18,
    y: y + 0.18,
    w: w - 0.36,
    h: 0.55,
    fontFace: FONT,
    fontSize: 24,
    bold: true,
    color,
    margin: 0,
    align: "center",
    fit: "shrink",
  });
  slide.addText(label, {
    x: x + 0.22,
    y: y + 0.84,
    w: w - 0.44,
    h: 0.35,
    fontFace: FONT,
    fontSize: 7.2,
    color: COLORS.muted,
    margin: 0,
    align: "center",
    fit: "shrink",
  });
}

function addBar(slide, x, y, label, value, max, color, note) {
  const barW = 4.3;
  slide.addText(label, {
    x,
    y,
    w: 2.2,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8.3,
    color: COLORS.ink,
    margin: 0,
    fit: "shrink",
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: x + 2.35,
    y: y + 0.03,
    w: barW,
    h: 0.16,
    fill: { color: "ECE8DE" },
    line: { color: "ECE8DE", transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: x + 2.35,
    y: y + 0.03,
    w: (barW * value) / max,
    h: 0.16,
    fill: { color },
    line: { color, transparency: 100 },
  });
  slide.addText(`${value}%`, {
    x: x + 6.78,
    y: y - 0.02,
    w: 0.5,
    h: 0.18,
    fontFace: FONT,
    fontSize: 8.2,
    bold: true,
    color,
    margin: 0,
  });
  if (note) {
    slide.addText(note, {
      x,
      y: y + 0.25,
      w: 6.5,
      h: 0.16,
      fontFace: FONT,
      fontSize: 6.4,
      color: COLORS.muted,
      margin: 0,
    });
  }
}

function addBullets(slide, items, x, y, w, h, color = COLORS.cobalt, textColor = COLORS.ink) {
  const lineH = h / items.length;
  items.forEach((item, i) => {
    const yy = y + i * lineH;
    slide.addShape(pptx.ShapeType.ellipse, {
      x,
      y: yy + 0.09,
      w: 0.08,
      h: 0.08,
      fill: { color },
      line: { color, transparency: 100 },
    });
    slide.addText(item, {
      x: x + 0.18,
      y: yy,
      w,
      h: Math.min(0.46, lineH - 0.02),
      fontFace: FONT,
      fontSize: 8.7,
      color: textColor,
      margin: 0,
      fit: "shrink",
    });
  });
}

function addNote(slide, text, x, y, w, color = COLORS.teal) {
  slide.addShape(pptx.ShapeType.rect, {
    x,
    y,
    w: 0.08,
    h: 0.7,
    fill: { color },
    line: { color, transparency: 100 },
  });
  slide.addText(text, {
    x: x + 0.2,
    y: y + 0.02,
    w,
    h: 0.65,
    fontFace: FONT,
    fontSize: 10,
    bold: true,
    color: COLORS.ink,
    margin: 0,
    fit: "shrink",
  });
}

function cover() {
  const slide = pptx.addSlide();
  addBg(slide);
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 3.95,
    h: SLIDE.h,
    fill: { color: COLORS.dark },
    line: { color: COLORS.dark, transparency: 100 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 3.95,
    y: 0,
    w: 0.1,
    h: SLIDE.h,
    fill: { color: COLORS.cobalt },
    line: { color: COLORS.cobalt, transparency: 100 },
  });
  slide.addText("SEARCH\nSHIFT", {
    x: 0.58,
    y: 0.72,
    w: 2.8,
    h: 0.82,
    fontFace: FONT,
    fontSize: 13,
    bold: true,
    color: "FFFFFF",
    margin: 0,
    breakLine: false,
    fit: "shrink",
  });
  slide.addText("SEO", {
    x: 0.63,
    y: 2.18,
    w: 1.35,
    h: 0.45,
    fontFace: FONT,
    fontSize: 26,
    bold: true,
    color: "FFFFFF",
    margin: 0,
  });
  slide.addText("AEO", {
    x: 2.0,
    y: 4.55,
    w: 1.38,
    h: 0.45,
    fontFace: FONT,
    fontSize: 26,
    bold: true,
    color: COLORS.amber,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 1.25,
    y: 3.0,
    w: 1.25,
    h: 1.0,
    line: { color: COLORS.amber, width: 2.0 },
  });
  slide.addText("링크 순위 경쟁에서\n답변 채택 경쟁으로", {
    x: 4.9,
    y: 1.24,
    w: 6.95,
    h: 1.45,
    fontFace: FONT,
    fontSize: 33,
    bold: true,
    color: COLORS.ink,
    margin: 0,
    fit: "shrink",
    breakLine: false,
  });
  slide.addText("SEO -> AEO 검색 시대", {
    x: 4.95,
    y: 3.0,
    w: 4.9,
    h: 0.4,
    fontFace: FONT,
    fontSize: 15,
    color: COLORS.cobalt,
    bold: true,
    margin: 0,
  });
  slide.addText("AI Overviews, AI Mode, ChatGPT search가 만든 검색 운영의 새 기준", {
    x: 4.95,
    y: 3.58,
    w: 6.6,
    h: 0.36,
    fontFace: FONT,
    fontSize: 11.5,
    color: COLORS.muted,
    margin: 0,
    fit: "shrink",
  });
  addMetric(slide, 4.95, 4.68, 1.95, 1.3, "8%", "AI summary가 있을 때\n전통 검색결과 클릭", COLORS.red);
  addMetric(slide, 7.15, 4.68, 1.95, 1.3, "15%", "AI summary가 없을 때\n전통 검색결과 클릭", COLORS.green);
  addMetric(slide, 9.35, 4.68, 1.95, 1.3, "10%+", "AI Overviews 노출 질의의\nGoogle 사용 증가", COLORS.cobalt);
  addFooter(slide, "Sources: Pew Research Center, 2025; Google Search blog, 2025");
}

function slide2() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 2, "상황 변화");
  addTitle(slide, "검색 결과는 페이지 목록에서 답변 인터페이스로 이동한다", "사용자는 더 긴 질문을 하고, 엔진은 여러 검색을 동시에 수행해 답변을 조립한다.");

  const y = 2.4;
  addCard(slide, 0.78, y, 2.85, 2.38, "기존 SEO", "SERP 순위", "키워드별 상위 노출, title/snippet, 백링크, 페이지 품질 신호가 중심", COLORS.cobalt);
  addCard(slide, 5.2, y, 2.85, 2.38, "전환 지점", "Answer Layer", "AI summary, citation, follow-up, comparison, multimodal context가 사용자 화면의 중심", COLORS.amber);
  addCard(slide, 9.62, y, 2.85, 2.38, "AEO 목표", "인용 가능한 답변", "엔진이 이해하고, 압축하고, 출처로 연결하기 쉬운 지식 단위", COLORS.teal);

  slide.addText("사용자 질문", {
    x: 0.9,
    y: 5.4,
    w: 2.0,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    bold: true,
    margin: 0,
  });
  slide.addText("링크 목록", {
    x: 3.0,
    y: 5.4,
    w: 1.6,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    bold: true,
    margin: 0,
  });
  slide.addText("AI가 조립한 답변 + 출처", {
    x: 5.1,
    y: 5.4,
    w: 2.45,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    bold: true,
    margin: 0,
  });
  slide.addText("후속 질문/행동", {
    x: 8.1,
    y: 5.4,
    w: 1.8,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    bold: true,
    margin: 0,
  });
  slide.addText("전환", {
    x: 10.5,
    y: 5.4,
    w: 1.0,
    h: 0.2,
    fontFace: FONT,
    fontSize: 8,
    color: COLORS.muted,
    bold: true,
    margin: 0,
  });

  const cx = [1.22, 3.4, 5.95, 8.55, 10.75];
  cx.forEach((xx, i) => {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: xx,
      y: 5.82,
      w: 0.32,
      h: 0.32,
      fill: { color: i === 2 ? COLORS.amber : COLORS.cobalt },
      line: { color: i === 2 ? COLORS.amber : COLORS.cobalt, transparency: 100 },
    });
    if (i < cx.length - 1) {
      slide.addShape(pptx.ShapeType.line, {
        x: xx + 0.35,
        y: 5.98,
        w: cx[i + 1] - xx - 0.42,
        h: 0,
        line: { color: COLORS.line, width: 1.5 },
      });
    }
  });
  addNote(slide, "AEO의 실무 과제는 '검색엔진이 찾는 페이지'를 넘어 '답변 엔진이 선택하는 근거'를 만드는 것이다.", 0.78, 6.25, 8.5, COLORS.teal);
  addFooter(slide, "Sources: Google Search blog, AI Mode posts, 2025; OpenAI, Introducing ChatGPT search, 2024/2025 update");
}

function slide3() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 3, "행동 변화");
  addTitle(slide, "클릭은 줄고, 답변 안에서의 존재감이 중요해진다", "AI summary가 나타나는 검색은 사용자의 다음 행동을 바꾼다.");

  addPanel(slide, 0.78, 2.18, 7.85, 3.68);
  slide.addText("Google 검색 후 다음 행동", {
    x: 1.08,
    y: 2.48,
    w: 3.2,
    h: 0.25,
    fontFace: FONT,
    fontSize: 10.5,
    bold: true,
    color: COLORS.ink,
    margin: 0,
  });
  slide.addText("Pew Research Center, 900명 U.S. adults, 2025년 3월 브라우징 데이터", {
    x: 4.1,
    y: 2.52,
    w: 4.1,
    h: 0.2,
    fontFace: FONT,
    fontSize: 6.6,
    color: COLORS.muted,
    margin: 0,
    align: "right",
  });

  addBar(slide, 1.15, 3.1, "전통 검색결과 클릭: AI summary 있음", 8, 30, COLORS.red, "AI summary가 있는 방문 기준");
  addBar(slide, 1.15, 3.9, "전통 검색결과 클릭: AI summary 없음", 15, 30, COLORS.green, "전통 검색결과만 있는 방문 기준");
  addBar(slide, 1.15, 4.7, "AI summary 안의 출처 링크 클릭", 1, 30, COLORS.amber, "AI summary가 있는 방문 중 직접 출처 클릭");
  addBar(slide, 1.15, 5.5, "검색 후 세션 종료: AI summary 있음", 26, 30, COLORS.cobalt, "AI summary가 있는 페이지에서 세션 종료");

  addMetric(slide, 9.1, 2.18, 1.55, 1.15, "58%", "조사 대상 중 2025년 3월\nAI summary 노출 경험", COLORS.cobalt);
  addMetric(slide, 10.9, 2.18, 1.55, 1.15, "18%", "데이터셋 내 Google 검색 중\nAI summary 생성 비중", COLORS.teal);
  addMetric(slide, 9.1, 3.72, 1.55, 1.15, "53%", "10단어 이상 검색에서\nAI summary 생성", COLORS.amber);
  addMetric(slide, 10.9, 3.72, 1.55, 1.15, "60%", "의문사로 시작한 검색에서\nAI summary 생성", COLORS.green);

  addNote(slide, "의미: '방문자 수'만 최적화하면 브랜드가 답변 안에서 사라지는 위험을 놓친다.", 9.1, 5.44, 3.05, COLORS.red);
  addFooter(slide, "Source: Pew Research Center, 'Google users are less likely to click on links when an AI summary appears in the results', Jul 22 2025");
}

function slide4() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 4, "개념 정리");
  addTitle(slide, "SEO와 AEO는 대체 관계가 아니라 레이어 관계다", "기존 SEO 기반 위에 답변 엔진이 읽을 수 있는 구조를 얹는다.");

  const x = 0.78;
  const y = 2.0;
  const w = 11.78;
  const rowH = 0.66;
  addPanel(slide, x, y, w, 4.0);
  const headers = ["구분", "SEO", "AEO"];
  const col = [x + 0.25, x + 2.0, x + 6.9];
  const widths = [1.3, 4.4, 4.45];
  headers.forEach((h, i) => {
    slide.addText(h, {
      x: col[i],
      y: y + 0.25,
      w: widths[i],
      h: 0.23,
      fontFace: FONT,
      fontSize: 8.6,
      bold: true,
      color: i === 2 ? COLORS.teal : COLORS.cobalt,
      margin: 0,
    });
  });
  slide.addShape(pptx.ShapeType.line, { x: x + 0.2, y: y + 0.68, w: w - 0.4, h: 0, line: { color: COLORS.line, width: 0.8 } });
  const rows = [
    ["목표", "검색 결과 상위 노출과 클릭 확보", "AI 답변 안에서 언급·인용·추천될 확률 확보"],
    ["콘텐츠 단위", "키워드 타깃 페이지, 카테고리, 블로그", "질문-답변 블록, 엔티티 설명, 근거 단락, FAQ"],
    ["기술 신호", "크롤링, 색인, 내부링크, Core Web Vitals", "구조화 데이터, 출처 명확성, 최신성, entity consistency"],
    ["성과 지표", "Rank, CTR, organic sessions, conversion", "Citation rate, answer coverage, share of answer, assisted conversion"],
    ["운영 방식", "키워드 리서치 -> 콘텐츠 -> 링크/기술 개선", "질문 맵 -> 답변 원자화 -> 근거 패키징 -> AI visibility 모니터링"],
  ];
  rows.forEach((r, idx) => {
    const yy = y + 0.85 + idx * rowH;
    if (idx > 0) {
      slide.addShape(pptx.ShapeType.line, { x: x + 0.2, y: yy - 0.12, w: w - 0.4, h: 0, line: { color: "EEEAE0", width: 0.5 } });
    }
    slide.addText(r[0], { x: col[0], y: yy, w: widths[0], h: 0.32, fontFace: FONT, fontSize: 8.4, bold: true, color: COLORS.ink, margin: 0, fit: "shrink" });
    slide.addText(r[1], { x: col[1], y: yy, w: widths[1], h: 0.34, fontFace: FONT, fontSize: 8.2, color: COLORS.muted, margin: 0, fit: "shrink" });
    slide.addText(r[2], { x: col[2], y: yy, w: widths[2], h: 0.34, fontFace: FONT, fontSize: 8.2, color: COLORS.ink, margin: 0, fit: "shrink" });
  });

  addNote(slide, "운영 원칙: SEO는 발견 가능성의 기반, AEO는 답변 채택 가능성의 확장이다.", 0.88, 6.25, 8.5, COLORS.teal);
  addFooter(slide, "Sources: Google Search Central, Optimizing for generative AI search; structured data documentation; internal synthesis");
}

function slide5() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 5, "실행 구조");
  addTitle(slide, "AEO 콘텐츠는 '정답 후보'로 읽히도록 설계한다", "엔진이 단락을 추출해도 의미가 무너지지 않는 정보 구조가 필요하다.");

  const items = [
    ["01", "Answer-first block", "첫 화면에 2-4문장 정의, 대상, 조건, 핵심 근거를 먼저 배치", COLORS.cobalt],
    ["02", "Entity clarity", "브랜드명, 제품명, 카테고리, 비교 대상의 표기를 일관되게 유지", COLORS.teal],
    ["03", "Structured data", "FAQ, HowTo, Product, Organization 등 가능한 schema를 정확히 적용", COLORS.green],
    ["04", "Evidence pack", "수치, 날짜, 원문 출처, 방법론을 본문 가까이에 붙여 인용 가능하게 구성", COLORS.amber],
    ["05", "Refresh loop", "AI 답변이 선호하는 최신성 신호를 위해 업데이트 이력과 검증 루틴 운영", COLORS.red],
  ];

  items.forEach((it, i) => {
    const yy = 2.0 + i * 0.82;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: 0.94,
      y: yy,
      w: 0.38,
      h: 0.38,
      fill: { color: it[3] },
      line: { color: it[3], transparency: 100 },
    });
    slide.addText(it[0], {
      x: 0.98,
      y: yy + 0.115,
      w: 0.3,
      h: 0.1,
      fontFace: FONT,
      fontSize: 6.2,
      bold: true,
      color: "FFFFFF",
      margin: 0,
      align: "center",
    });
    slide.addText(it[1], {
      x: 1.55,
      y: yy - 0.03,
      w: 2.25,
      h: 0.24,
      fontFace: FONT,
      fontSize: 10.8,
      bold: true,
      color: COLORS.ink,
      margin: 0,
    });
    slide.addText(it[2], {
      x: 3.82,
      y: yy - 0.02,
      w: 4.45,
      h: 0.34,
      fontFace: FONT,
      fontSize: 8.2,
      color: COLORS.muted,
      margin: 0,
      fit: "shrink",
    });
    if (i < items.length - 1) {
      slide.addShape(pptx.ShapeType.line, {
        x: 1.13,
        y: yy + 0.43,
        w: 0,
        h: 0.38,
        line: { color: COLORS.line, width: 1 },
      });
    }
  });

  addPanel(slide, 9.05, 2.0, 3.2, 3.94, { fill: "101827", line: "101827" });
  addTextBlock(slide, 9.38, 2.34, 2.55, "AEO-ready page", "AI가 답변을 조립할 때 그대로 가져갈 수 있는 콘텐츠 단위", "FFFFFF", "BFD6FF");
  addBullets(slide, [
    "질문별 명확한 H2/H3",
    "요약 -> 근거 -> 예외 순서",
    "출처와 날짜를 문단 가까이에 배치",
    "FAQ와 schema를 내용과 일치",
    "브랜드/제품/entity 표기 통일",
  ], 9.42, 3.55, 2.35, 1.48, COLORS.amber, "DCE7FF");
  addFooter(slide, "Sources: Google Search Central structured data docs, last updated Dec 10 2025; internal synthesis");
}

function addTextBlock(slide, x, y, w, title, body, titleColor, bodyColor) {
  slide.addText(title, {
    x,
    y,
    w,
    h: 0.34,
    fontFace: FONT,
    fontSize: 16,
    bold: true,
    color: titleColor,
    margin: 0,
    fit: "shrink",
  });
  slide.addText(body, {
    x,
    y: y + 0.62,
    w,
    h: 0.46,
    fontFace: FONT,
    fontSize: 8.6,
    color: bodyColor,
    margin: 0,
    fit: "shrink",
  });
}

function slide6() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 6, "측정");
  addTitle(slide, "측정 기준도 트래픽 중심에서 답변 점유율 중심으로 확장된다", "AEO는 새 대시보드를 추가해야 운영 가능한 전략이 된다.");

  addPanel(slide, 0.78, 2.0, 5.7, 3.8);
  addPanel(slide, 6.85, 2.0, 5.7, 3.8, { fill: "FBFAF6" });
  slide.addText("기존 SEO KPI", { x: 1.08, y: 2.3, w: 2.1, h: 0.25, fontFace: FONT, fontSize: 12, bold: true, color: COLORS.cobalt, margin: 0 });
  slide.addText("AEO 추가 KPI", { x: 7.15, y: 2.3, w: 2.1, h: 0.25, fontFace: FONT, fontSize: 12, bold: true, color: COLORS.teal, margin: 0 });

  addBullets(slide, [
    "키워드 순위 / SERP feature",
    "Organic CTR / sessions",
    "Backlink / domain authority",
    "페이지 속도와 색인 상태",
    "Organic conversion",
  ], 1.1, 2.95, 4.8, 2.2, COLORS.cobalt);
  addBullets(slide, [
    "AI citation rate",
    "Share of answer by topic",
    "AI answer sentiment / accuracy",
    "AI referral quality",
    "Source freshness / entity consistency",
  ], 7.17, 2.95, 4.8, 2.2, COLORS.teal);

  slide.addShape(pptx.ShapeType.line, { x: 6.65, y: 2.3, w: 0, h: 3.25, line: { color: COLORS.line, width: 1 } });
  addPill(slide, "확장", 5.88, 3.68, 1.55, COLORS.ink, "F1E1A8");

  addNote(slide, "권장 운영: Search Console과 기존 SEO 도구는 유지하고, AI search monitoring을 topic cluster 단위로 추가한다.", 0.9, 6.22, 9.4, COLORS.teal);
  addFooter(slide, "Sources: Google AI Mode query fan-out explanations, 2025; Google Search Central measurement guidance; internal synthesis");
}

function slide7() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 7, "로드맵");
  addTitle(slide, "90일 전환 로드맵", "새 조직을 만들기보다 기존 SEO 운영 리듬에 answer-readiness를 넣는다.");

  const cols = [
    ["0-30일", "진단", ["핵심 토픽 20개 선정", "검색 의도와 AI summary 노출 여부 조사", "상위 페이지의 answer block gap 점검", "schema와 entity inconsistency 감사"], COLORS.cobalt],
    ["31-60일", "구축", ["토픽별 answer-first page 리라이트", "FAQ/HowTo/Product schema 정비", "근거·수치·출처를 본문 가까이에 배치", "비교/정의/절차 페이지 우선 개선"], COLORS.teal],
    ["61-90일", "운영화", ["AI citation 모니터링 시작", "검색 유입과 assisted conversion 비교", "답변 오류·누락 케이스 수정 루프", "분기별 AEO backlog로 편입"], COLORS.amber],
  ];

  cols.forEach((c, i) => {
    const x = 0.78 + i * 4.05;
    addPanel(slide, x, 2.02, 3.62, 3.88);
    addPill(slide, c[0], x + 0.28, 2.35, 0.95, COLORS.ink, "EEF2FF");
    slide.addText(c[1], {
      x: x + 0.28,
      y: 2.86,
      w: 2.6,
      h: 0.34,
      fontFace: FONT,
      fontSize: 17,
      bold: true,
      color: c[3],
      margin: 0,
    });
    c[2].forEach((item, j) => {
      const yy = 3.55 + j * 0.48;
      slide.addShape(pptx.ShapeType.rect, {
        x: x + 0.3,
        y: yy + 0.05,
        w: 0.11,
        h: 0.11,
        fill: { color: c[3] },
        line: { color: c[3], transparency: 100 },
      });
      slide.addText(item, {
        x: x + 0.52,
        y: yy,
        w: 2.82,
        h: 0.24,
        fontFace: FONT,
        fontSize: 7.8,
        color: COLORS.ink,
        margin: 0,
        fit: "shrink",
      });
    });
  });
  addNote(slide, "첫 90일의 성공 기준: 5개 핵심 토픽에서 AI 답변 내 브랜드/콘텐츠 언급 또는 출처 후보 노출을 확인한다.", 0.88, 6.25, 9.2, COLORS.green);
  addFooter(slide, "Sample roadmap; adapt by industry, content volume, and baseline SEO maturity");
}

function slide8() {
  const slide = pptx.addSlide();
  addBg(slide);
  addTopBar(slide, 8, "결론");
  slide.addText("결론", {
    x: 0.78,
    y: 1.05,
    w: 1.2,
    h: 0.25,
    fontFace: FONT,
    fontSize: 9,
    bold: true,
    color: COLORS.cobalt,
    margin: 0,
  });
  slide.addText("검색 전략의 목표를\n'랭킹'에서 '선택되는 답변'까지 넓힌다", {
    x: 0.78,
    y: 1.58,
    w: 8.3,
    h: 1.35,
    fontFace: FONT,
    fontSize: 31,
    bold: true,
    color: COLORS.ink,
    margin: 0,
    fit: "shrink",
    breakLine: false,
  });
  addCard(slide, 0.78, 3.5, 3.62, 1.62, "KEEP", "SEO 기반 유지", "크롤링, 색인, 기술 SEO, 콘텐츠 품질, 링크 신호는 여전히 기반이다.", COLORS.cobalt);
  addCard(slide, 4.85, 3.5, 3.62, 1.62, "ADD", "AEO 운영 기준 추가", "질문별 answer block, structured data, entity consistency, citation 모니터링을 더한다.", COLORS.teal);
  addCard(slide, 8.92, 3.5, 3.62, 1.62, "DECIDE", "우선순위 토픽 20개", "매출·브랜드 방어·지원 비용 절감에 직접 연결되는 질의부터 시작한다.", COLORS.amber);

  slide.addShape(pptx.ShapeType.rect, {
    x: 0.78,
    y: 5.75,
    w: 11.76,
    h: 0.74,
    fill: { color: COLORS.dark },
    line: { color: COLORS.dark, transparency: 100 },
  });
  slide.addText("다음 액션: 기존 SEO 상위 50개 페이지를 대상으로 answer-readiness audit을 실행한다.", {
    x: 1.05,
    y: 6.0,
    w: 10.8,
    h: 0.22,
    fontFace: FONT,
    fontSize: 12,
    bold: true,
    color: "FFFFFF",
    margin: 0,
    fit: "shrink",
  });
  addFooter(slide, "Sample recommendation deck generated by Codex");
}

cover();
slide2();
slide3();
slide4();
slide5();
slide6();
slide7();
slide8();

const outline = `# SEO -> AEO 검색 시대

${slides.map((s) => `## ${s.no}. ${s.title}\n\n${s.takeaway}\n`).join("\n")}

## 주요 출처

- Google Search Blog: Expanding AI Overviews and introducing AI Mode, Mar 5 2025
- Google Search Blog: AI in Search, Going beyond information to intelligence, May 20 2025
- Google Search Blog: AI Mode agentic features and global expansion, Aug 21 2025
- OpenAI: Introducing ChatGPT search, Oct 31 2024; updates through Feb 5 2025
- Pew Research Center: Google users are less likely to click on links when an AI summary appears in the results, Jul 22 2025
- Google Search Central: Optimizing your website for generative AI features on Google Search
- Google Search Central: Structured data and helpful content documentation
`;

fs.writeFileSync(outOutline, outline, "utf8");

pptx.writeFile({ fileName: outPptx }).then(() => {
  console.log(outPptx);
  console.log(outOutline);
});
