const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const Module = require("node:module");

const root = path.resolve(__dirname, "../..");
const outDir = __dirname;
const imageDir = path.join(outDir, "images");
const templatePath = path.join(
  root,
  ".claude/skills/📝 콘텐츠/future-slide-skills/_vendor/future-slide-skill/skills/tightened-slide/assets/template.html",
);

function addBundledNodeModules() {
  const bundled = path.join(os.homedir(), ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules");
  if (!fs.existsSync(bundled)) return;
  process.env.NODE_PATH = process.env.NODE_PATH ? `${bundled}${path.delimiter}${process.env.NODE_PATH}` : bundled;
  Module._initPaths();
}

function escapeAttr(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function heroSvg({ width, height, accent }) {
  const bg = "#fbfaf7";
  const ink = "#111111";
  const soft = "#e7e5df";

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <rect width="${width}" height="${height}" fill="${bg}"/>
  <rect x="90" y="92" width="430" height="610" fill="${ink}"/>
  <rect x="138" y="152" width="260" height="26" fill="${bg}" opacity=".86"/>
  <rect x="138" y="218" width="318" height="26" fill="${bg}" opacity=".72"/>
  <rect x="138" y="284" width="220" height="26" fill="${bg}" opacity=".52"/>
  <rect x="138" y="520" width="318" height="82" fill="${accent}"/>
  <rect x="615" y="118" width="350" height="92" fill="${soft}"/>
  <rect x="615" y="264" width="350" height="92" fill="${soft}"/>
  <rect x="615" y="410" width="350" height="92" fill="${soft}"/>
  <rect x="615" y="556" width="350" height="92" fill="${soft}"/>
  <rect x="690" y="146" width="200" height="16" fill="${ink}" opacity=".62"/>
  <rect x="690" y="292" width="160" height="16" fill="${ink}" opacity=".62"/>
  <rect x="690" y="438" width="240" height="16" fill="${ink}" opacity=".62"/>
  <rect x="690" y="584" width="180" height="16" fill="${ink}" opacity=".62"/>
  <path d="M520 172 C690 172, 760 180, 1110 260" fill="none" stroke="${ink}" stroke-width="2" opacity=".42"/>
  <path d="M520 305 C720 315, 840 324, 1110 330" fill="none" stroke="${accent}" stroke-width="5" opacity=".9"/>
  <path d="M520 450 C700 430, 820 410, 1110 390" fill="none" stroke="${ink}" stroke-width="2" opacity=".38"/>
  <path d="M520 590 C700 550, 830 505, 1110 455" fill="none" stroke="${ink}" stroke-width="2" opacity=".3"/>
  <rect x="1110" y="164" width="560" height="420" fill="${bg}" stroke="${ink}" stroke-width="2"/>
  <rect x="1160" y="218" width="345" height="34" fill="${ink}" opacity=".82"/>
  <rect x="1160" y="296" width="420" height="18" fill="${soft}"/>
  <rect x="1160" y="340" width="370" height="18" fill="${soft}"/>
  <rect x="1160" y="420" width="150" height="88" fill="${accent}"/>
  <rect x="1360" y="420" width="150" height="88" fill="${soft}"/>
  <rect x="1560" y="420" width="70" height="88" fill="${ink}" opacity=".82"/>
  <circle cx="595" cy="172" r="17" fill="${accent}"/>
  <circle cx="700" cy="310" r="17" fill="${ink}"/>
  <circle cx="845" cy="420" r="17" fill="${accent}"/>
  <circle cx="1040" cy="330" r="17" fill="${ink}"/>
  <rect x="1770" y="96" width="210" height="610" fill="${accent}"/>
</svg>`;
}

async function writePng(sharp, file, options) {
  await sharp(Buffer.from(heroSvg(options))).png().toFile(file);
}

function loadExistingManifest(file) {
  if (!fs.existsSync(file)) return new Map();
  try {
    const parsed = JSON.parse(fs.readFileSync(file, "utf8"));
    if (!Array.isArray(parsed)) return new Map();
    return new Map(parsed.map((entry) => [entry.file, entry]));
  } catch {
    return new Map();
  }
}

function hasCliGeneratedAsset(asset, existingManifest) {
  const manifestFile = `images/${asset.file}`;
  const entry = existingManifest.get(manifestFile);
  return Boolean(
    entry
      && entry.status === "generated_via_cli"
      && entry.generator === "codex-native-image-cli"
      && fs.existsSync(path.join(outDir, manifestFile)),
  );
}

function imageFrame(file, slot, alt) {
  return `<div class="frame-img r-21x9"><img src="images/${file}" data-image-slot="${slot}" alt="${escapeAttr(alt)}"></div>`;
}

function thumbFrame(file, slot, alt) {
  return `<div class="frame-img r-16x10" style="height:7.5vh"><img src="images/${file}" data-image-slot="${slot}" alt="${escapeAttr(alt)}"></div>`;
}

function moduleCard(index, title, body, mark) {
  return `
        <div class="brief-card" style="padding:18px;min-height:18vh">
          <div class="t-meta">${String(index).padStart(2, "0")}</div>
          <div style="height:42px;display:grid;grid-template-columns:repeat(5,1fr);gap:4px;align-items:end;margin:14px 0 18px">
            ${mark}
          </div>
          <div><h3 style="font:400 max(19px,1.35vw)/1.15 var(--sans)">${title}</h3><p class="body-sm" style="margin-top:8px">${body}</p></div>
        </div>`;
}

async function main() {
  addBundledNodeModules();
  const sharp = require("sharp");
  fs.mkdirSync(imageDir, { recursive: true });

  const manifestPath = path.join(outDir, "asset_manifest.json");
  const existingManifest = loadExistingManifest(manifestPath);
  const accent = "#00A676";
  const assets = [
    {
      slide: 3,
      slot: "s22-hero-21x9",
      file: "03-answer-engine-hero.png",
      alt: "브랜드 지식이 답변 엔진으로 연결되는 추상 네트워크",
      width: 2100,
      height: 900,
      prompt: "21:9 product evidence map for an AI answer visibility platform: source repository blocks flow into answer surface cards through citation paths. No readable text, letters, numbers, logo, watermark, UI labels, or slide chrome. Black, warm white, gray, and one green accent. Large negative space for Korean HTML typography.",
      visual_contract: {
        claim: "브랜드 공식 근거가 답변 엔진의 답변 표면으로 연결된다.",
        must_show: [
          "왼쪽의 브랜드 근거 저장소",
          "가운데의 인용/연결 경로",
          "오른쪽의 답변 표면",
        ],
        must_not_show: [
          "읽어야 하는 텍스트",
          "무작위 추상 도형",
          "브랜드 로고처럼 보이는 요소",
        ],
        acceptance_check: "이미지만 보아도 근거가 답변 표면으로 이동한다는 구조가 읽혀야 한다.",
      },
    },
  ];

  for (const asset of assets) {
    if (hasCliGeneratedAsset(asset, existingManifest)) continue;
    await writePng(sharp, path.join(imageDir, asset.file), {
      width: asset.width,
      height: asset.height,
      accent,
      seed: asset.seed,
      density: asset.density || 11,
    });
  }

  const manifest = assets.map((asset) => {
    const file = `images/${asset.file}`;
    const existing = existingManifest.get(file);
    const cliGenerated = hasCliGeneratedAsset(asset, existingManifest);

    return {
      slide: asset.slide,
      slot: asset.slot,
      file,
      alt: asset.alt,
      prompt: asset.prompt,
      status: cliGenerated ? "generated_via_cli" : "blocked_cli_generation_not_run",
      generator: cliGenerated ? "codex-native-image-cli" : "local-sharp-preview-not-production",
      required_generator: "codex-native-image-cli",
      visual_contract: existing?.visual_contract || asset.visual_contract,
      text_policy: "no readable text embedded in image",
    };
  });
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

  const slides = `
  <section class="slide accent active" data-layout="S01" data-animate="hero">
    <div class="canvas-card">
      <canvas class="ascii-bg" aria-hidden="true"></canvas>
      <div class="chrome-min">
        <div class="l">Product Brand Deck</div>
        <div class="r">01 / 08</div>
      </div>
      <div style="flex:1;display:grid;align-content:center;gap:3vh">
        <div class="t-meta" style="color:rgba(255,255,255,.78)">Answer Visibility Platform</div>
        <h1 class="h-hero">AnswerLayer</h1>
        <p class="lead" style="color:rgba(255,255,255,.86);max-width:48ch">AI 검색 시대의 브랜드 답변 레이어</p>
      </div>
      <div class="foot" style="color:rgba(255,255,255,.72)">Future Slide product / brand visual archetype</div>
    </div>
  </section>

  <section class="slide split" data-layout="S03" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-ink">
        <div class="chrome-min"><div class="l">Thesis</div><div class="r">02 / 08</div></div>
        <div style="margin-top:auto">
          <div class="t-meta" style="color:rgba(255,255,255,.64)">Search is becoming an answer surface</div>
          <h2 class="h-statement">브랜드는<br>링크보다<br>답변으로<br>발견된다</h2>
        </div>
      </div>
      <div class="half b-paper">
        <div class="chrome-min"><div class="l">Shift</div><div class="r">AEO</div></div>
        <div style="display:grid;gap:24px;margin:auto 0;max-width:54ch">
          <p class="lead">SEO는 노출 기반을 만든다. AEO는 모델이 인용하고 요약할 수 있는 브랜드 지식 구조를 만든다.</p>
          <div class="hr-hairline"></div>
          <p class="body">AnswerLayer는 브랜드의 공식 근거, 제품 정보, 비교 포인트를 답변 엔진이 읽기 쉬운 형태로 정렬한다.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S22" data-animate="image-hero">
    <div class="canvas-card nav-safe-bottom-tight">
      <div class="chrome-min"><div class="l">Product Promise</div><div class="r">03 / 08</div></div>
      ${imageFrame("03-answer-engine-hero.png", "s22-hero-21x9", "브랜드 지식이 답변 엔진으로 연결되는 추상 네트워크")}
      <div class="image-hero-body" style="padding:3.6vh 0 0">
        <div>
          <div class="t-meta">Brand knowledge layer</div>
          <h2 class="h-md" style="margin-top:12px">정답 후보로<br>읽히는 브랜드</h2>
        </div>
        <div class="image-hero-stats">
          <div><div class="t-meta">01</div><p class="body-sm">공식 근거를 모델 친화 구조로 정리</p></div>
          <div><div class="t-meta">02</div><p class="body-sm">질문 의도별 답변 단위를 설계</p></div>
          <div><div class="t-meta">03</div><p class="body-sm">경쟁 답변면에서 누락 지점을 추적</p></div>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S20" data-animate="ledger">
    <div class="canvas-card nav-safe-bottom">
      <div class="chrome-min"><div class="l">Positioning</div><div class="r">04 / 08</div></div>
      <div class="t-meta">SEO stack vs AEO stack</div>
      <h2 class="h-md" style="margin-top:12px">SEO 기반 위에<br>AEO 운영 지표를 올린다</h2>
      <div class="stacked-ledger" style="margin-top:3vh">
        <div class="ledger-row" style="padding:1.05vh 0"><div><div class="t-meta">Search unit</div><p class="body-sm">키워드에서 질문 의도로 전환</p></div><div class="hr-hairline"></div><div class="ledger-num" style="font-size:min(8vw,11vh)">01</div></div>
        <div class="ledger-row" style="padding:1.05vh 0"><div><div class="t-meta">Content unit</div><p class="body-sm">페이지에서 답변 블록으로 재구성</p></div><div class="hr-hairline"></div><div class="ledger-num" style="font-size:min(8vw,11vh)">02</div></div>
        <div class="ledger-row" style="padding:1.05vh 0"><div><div class="t-meta">Trust unit</div><p class="body-sm">주장에서 출처와 근거 묶음으로 이동</p></div><div class="hr-hairline"></div><div class="ledger-num accent-text" style="font-size:min(8vw,11vh)">03</div></div>
        <div class="ledger-row" style="padding:1.05vh 0"><div><div class="t-meta">Success unit</div><p class="body-sm">순위와 트래픽에 답변 채택률을 추가</p></div><div class="hr-hairline"></div><div class="ledger-num" style="font-size:min(8vw,11vh)">04</div></div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S17" data-animate="system">
    <div class="canvas-card nav-safe-bottom">
      <div class="chrome-min"><div class="l">System</div><div class="r">05 / 08</div></div>
      <div class="system-diagram">
        <div>
          <div class="t-meta">Operating model</div>
          <h2 class="h-xl" style="margin-top:12px">브랜드 지식<br>답변 단위<br>재배열</h2>
          <p class="lead" style="margin-top:24px">콘텐츠를 더 많이 쓰는 문제가 아니라, 모델이 신뢰할 수 있는 증거와 구조를 만드는 문제다.</p>
        </div>
        <div style="display:grid;gap:18px">
          <svg class="sys-svg" viewBox="0 0 640 360" aria-hidden="true">
            <path d="M60 72 H250 V132 H380 V192 H560" fill="none" stroke="currentColor" stroke-width="2" opacity=".55"/>
            <path d="M60 180 H250 V132" fill="none" stroke="var(--accent)" stroke-width="5"/>
            <path d="M60 288 H250 V228 H380 V192" fill="none" stroke="currentColor" stroke-width="2" opacity=".4"/>
            <rect x="36" y="44" width="142" height="56" fill="var(--accent)"/>
            <rect x="36" y="152" width="142" height="56" fill="currentColor" opacity=".9"/>
            <rect x="36" y="260" width="142" height="56" fill="currentColor" opacity=".18"/>
            <rect x="250" y="104" width="142" height="56" fill="currentColor" opacity=".12"/>
            <rect x="398" y="164" width="142" height="56" fill="var(--accent)"/>
          </svg>
          <div class="grid-12">
            <div class="sys-label span-4"><div class="t-meta">Input</div><p class="body-sm">공식 문서, 제품 설명, 고객 질문</p></div>
            <div class="sys-label span-4"><div class="t-meta">Structure</div><p class="body-sm">엔티티, 근거, 비교, FAQ</p></div>
            <div class="sys-label span-4"><div class="t-meta">Output</div><p class="body-sm">모델이 선택 가능한 답변 블록</p></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S16" data-animate="brief-grid">
    <div class="canvas-card nav-safe-bottom-tight">
      <div class="chrome-min"><div class="l">Modules</div><div class="r">06 / 08</div></div>
      <div class="t-meta">Product surface</div>
      <h2 class="h-md" style="margin-top:12px">여섯 개의 작은 모듈이<br>답변 채택률을 만든다</h2>
      <div class="brief-grid" style="margin-top:3.2vh;gap:12px">
        ${moduleCard(1, "Source Map", "공식 근거의 출처와 업데이트 지점을 연결", '<span style="height:18px;background:var(--ink)"></span><span style="height:28px;background:var(--accent)"></span><span style="height:12px;background:var(--grey-2)"></span><span style="height:34px;background:var(--grey-2)"></span><span style="height:22px;background:var(--ink)"></span>')}
        ${moduleCard(2, "Authority", "브랜드가 말할 자격이 있는 주제를 분류", '<span style="height:34px;background:var(--accent)"></span><span style="height:34px;background:var(--accent)"></span><span style="height:18px;background:var(--grey-2)"></span><span style="height:18px;background:var(--grey-2)"></span><span style="height:28px;background:var(--ink)"></span>')}
        ${moduleCard(3, "Coverage", "질문 의도별 답변 누락 영역을 추적", '<span style="height:12px;background:var(--grey-2)"></span><span style="height:26px;background:var(--ink)"></span><span style="height:38px;background:var(--accent)"></span><span style="height:16px;background:var(--grey-2)"></span><span style="height:30px;background:var(--accent)"></span>')}
        ${moduleCard(4, "Freshness", "오래된 근거와 최신 근거를 분리", '<span style="height:34px;background:var(--ink)"></span><span style="height:24px;background:var(--grey-2)"></span><span style="height:16px;background:var(--grey-2)"></span><span style="height:30px;background:var(--accent)"></span><span style="height:38px;background:var(--accent)"></span>')}
        ${moduleCard(5, "Competitor", "경쟁사가 선택되는 답변면을 비교", '<span style="height:22px;background:var(--grey-2)"></span><span style="height:36px;background:var(--ink)"></span><span style="height:22px;background:var(--grey-2)"></span><span style="height:36px;background:var(--accent)"></span><span style="height:22px;background:var(--grey-2)"></span>')}
        ${moduleCard(6, "Action", "수정할 콘텐츠와 구조 변경을 우선순위화", '<span style="height:14px;background:var(--grey-2)"></span><span style="height:20px;background:var(--grey-2)"></span><span style="height:28px;background:var(--ink)"></span><span style="height:36px;background:var(--accent)"></span><span style="height:42px;background:var(--accent)"></span>')}
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S19" data-animate="cards">
    <div class="canvas-card nav-safe-bottom">
      <div class="chrome-min"><div class="l">Brand System</div><div class="r">07 / 08</div></div>
      <div class="t-meta">Design language</div>
      <h2 class="h-xl" style="margin-top:12px">브랜드 시스템은<br>차분해야 신뢰된다</h2>
      <div class="four-cards" style="margin-top:6vh">
        <div class="fc-col"><div class="t-cat">Evidence</div><p class="body-sm" style="margin-top:18px">주장보다 근거를 먼저 배치한다.</p></div>
        <div class="fc-col"><div class="t-cat">Structure</div><p class="body-sm" style="margin-top:18px">엔티티와 질문을 같은 축에서 관리한다.</p></div>
        <div class="fc-col"><div class="t-cat">Freshness</div><p class="body-sm" style="margin-top:18px">갱신일과 출처를 답변 품질 신호로 본다.</p></div>
        <div class="fc-col"><div class="t-cat">Contrast</div><p class="body-sm" style="margin-top:18px">경쟁 답변과의 차이를 운영 지표로 만든다.</p></div>
      </div>
    </div>
  </section>

  <section class="slide split" data-layout="S10" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-accent">
        <div class="chrome-min"><div class="l">Close</div><div class="r">08 / 08</div></div>
        <div style="margin-top:auto">
          <div class="t-meta" style="color:rgba(255,255,255,.72)">Operating principle</div>
          <h2 style="font:300 min(4.7vw,8vh)/1.04 var(--sans);letter-spacing:0">검색은 페이지를 찾고<br>AI는 답을 고른다</h2>
        </div>
      </div>
      <div class="half b-paper">
        <div class="chrome-min"><div class="l">Next</div><div class="r">Pilot</div></div>
        <div style="display:grid;gap:18px;margin:auto 0">
          <div class="card-fill"><div class="t-meta">01</div><h3 class="h-md">질문 수집</h3><p class="body-sm">브랜드가 답해야 하는 상위 질문면을 정의한다.</p></div>
          <div class="card-fill"><div class="t-meta">02</div><h3 class="h-md">근거 정렬</h3><p class="body-sm">공식 출처와 비교 근거를 답변 단위로 재구성한다.</p></div>
          <div class="card-fill"><div class="t-meta">03</div><h3 class="h-md accent-text">채택 추적</h3><p class="body-sm">AI 답변면에서 브랜드가 선택되는 변화를 추적한다.</p></div>
        </div>
      </div>
    </div>
  </section>`;

  let html = fs.readFileSync(templatePath, "utf8");
  html = html
    .replace("<title>Required Deck Title</title>", "<title>AnswerLayer Product Brand Deck</title>")
    .replace('<html lang="en" data-language="en">', '<html lang="ko" data-language="ko">')
    .replace("--accent:#002FA7;", "--accent:#00A676;")
    .replace("--accent-rgb:0,47,167;", "--accent-rgb:0,166,118;")
    .replace("--accent-bright:#5B7BFF;", "--accent-bright:#62D7B1;")
    .replace("--paper:#fafaf8;", "--paper:#fbfaf7;")
    .replace(/<div id="deck">[\s\S]*?<\/div>\n<div id="nav"/, `<div id="deck">\n${slides}\n</div>\n<div id="nav"`);

  fs.writeFileSync(path.join(outDir, "index.html"), html);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
