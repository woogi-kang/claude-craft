const fs = require("node:fs");
const path = require("node:path");

const templatePath = "/tmp/future-slide-skill-codex-260518/skills/tightened-slide/assets/template.html";
const baseOut = path.join(__dirname, "future-tightened-variants");
const template = fs.readFileSync(templatePath, "utf8");

function writeDeck(name, slides) {
  const outDir = path.join(baseOut, name);
  fs.mkdirSync(path.join(outDir, "images"), { recursive: true });
  const html = template
    .replace('<html lang="en" data-language="en">', '<html lang="ko" data-language="ko">')
    .replace("<title>Required Deck Title</title>", `<title>SEO -> AEO 검색 시대 / ${name}</title>`)
    .replace(
      /  <!-- Replace these sample sections with the final deck\. -->[\s\S]*?<\/section>\n<\/div>/,
      `  ${slides.trim()}\n</div>`,
    );
  const outFile = path.join(outDir, "index.html");
  fs.writeFileSync(outFile, html, "utf8");
  return outFile;
}

const v1 = String.raw`
  <section class="slide accent active" data-layout="S01" data-animate="hero">
    <div class="canvas-card">
      <canvas class="ascii-bg" aria-hidden="true"></canvas>
      <div class="chrome-min"><div class="l">V1 Balanced Analysis</div><div class="r">01 / 08</div></div>
      <div style="display:grid;gap:2.2vh;margin:auto 0">
        <div class="t-meta" style="color:rgba(255,255,255,.78)">SEO -> AEO</div>
        <h1 class="h-hero">링크 순위에서<br>답변 채택으로</h1>
        <p class="lead" style="color:rgba(255,255,255,.86);max-width:48ch">AI 검색 시대의 SEO는 사라지지 않는다. 목표가 검색 결과 노출에서 답변 엔진이 선택하는 근거까지 확장된다.</p>
      </div>
      <div class="foot" style="color:rgba(255,255,255,.62)">Future tightened slide / version 1</div>
    </div>
  </section>
  <section class="slide split" data-layout="S03" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-ink">
        <div class="chrome-min"><div class="l">Thesis</div><div class="r">02 / 08</div></div>
        <div style="margin-top:auto"><h2 class="h-statement">SEO는<br>기반이고,<br>AEO는<br>새 레이어다.</h2></div>
      </div>
      <div class="half b-paper">
        <div class="chrome-min"><div class="l">What changed</div><div class="r">Answer interface</div></div>
        <div style="display:grid;gap:24px;margin:auto 0;max-width:58ch">
          <p class="lead">검색 결과는 링크 목록에서 요약 답변, 출처, 후속 질문, 행동으로 이어지는 인터페이스로 이동하고 있다.</p>
          <div class="card-fill"><div class="t-meta">Practical implication</div><p class="body" style="margin-top:10px">기존 색인·랭킹 최적화는 유지하되, 질의별 답변 블록과 근거 패키지를 운영 단위로 추가한다.</p></div>
        </div>
      </div>
    </div>
  </section>
  <section class="slide" data-layout="S07" data-animate="bars">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Behavior signal</div><div class="r">03 / 08</div></div>
      <div class="t-meta">Pew Research Center, 2025</div>
      <h2 class="h-xl" style="max-width:11ch;margin-top:1.2vh">클릭은 이미<br>줄고 있다</h2>
      <div class="h-bar-chart nav-safe-bottom-tight" style="margin-top:5vh;max-width:92vw">
        <div class="bar-row"><div class="body">AI summary가 있는 검색의 전통 결과 클릭</div><div class="bar-fill" style="--w:27%"></div><div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">8%</div></div>
        <div class="bar-row"><div class="body">AI summary가 없는 검색의 전통 결과 클릭</div><div class="bar-fill" style="--w:50%"></div><div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">15%</div></div>
        <div class="bar-row"><div class="body">AI summary 내 출처 링크 클릭</div><div class="bar-fill" style="--w:3%"></div><div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">1%</div></div>
        <div class="bar-row"><div class="body">AI summary가 있는 검색 후 세션 종료</div><div class="bar-fill" style="--w:87%"></div><div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">26%</div></div>
      </div>
      <div class="foot">Source: Pew Research Center, July 22 2025. Bar scale max = 30%.</div>
    </div>
  </section>
  <section class="slide" data-layout="S08" data-animate="compare">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Operating model</div><div class="r">04 / 08</div></div>
      <div class="t-meta">From ranking to answer-readiness</div>
      <h2 class="h-xl" style="max-width:13ch;margin-top:1.2vh">SEO와 AEO의<br>역할 분담</h2>
      <div class="duo-compare nav-safe-bottom-tight" style="margin-top:4vh">
        <div style="display:flex;flex-direction:column;gap:18px">
          <div class="t-cat">SEO</div>
          <div class="card-fill"><div class="t-meta">Goal</div><p class="body">검색 결과에서 발견되고 클릭될 가능성을 높인다.</p></div>
          <div class="card-fill"><div class="t-meta">Unit</div><p class="body">키워드, 페이지, 내부링크, 색인 상태, SERP feature.</p></div>
          <div class="card-fill"><div class="t-meta">Metric</div><p class="body">Rank, CTR, organic sessions, conversion.</p></div>
        </div>
        <div class="vrule"></div>
        <div style="display:flex;flex-direction:column;gap:18px">
          <div class="t-cat">AEO</div>
          <div class="card-fill"><div class="t-meta">Goal</div><p class="body">AI 답변 안에서 언급·인용·추천될 가능성을 높인다.</p></div>
          <div class="card-fill"><div class="t-meta">Unit</div><p class="body">질문-답변 블록, entity 설명, 근거 단락, structured data.</p></div>
          <div class="card-fill"><div class="t-meta">Metric</div><p class="body">Citation rate, answer coverage, share of answer.</p></div>
        </div>
      </div>
      <div class="foot">Google frames AEO/GEO as generative AI search optimization inside broader SEO.</div>
    </div>
  </section>
  <section class="slide" data-layout="S17" data-animate="system">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">System</div><div class="r">05 / 08</div></div>
      <div class="t-meta">AEO-ready content architecture</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">정답 후보로<br>읽히는 페이지</h2>
      <div class="system-diagram nav-safe-bottom-tight" style="margin-top:4vh">
        <div style="display:grid;gap:16px">
          <div class="sys-label"><div class="t-cat">01 Answer-first block</div><p class="body-sm" style="margin-top:8px">2-4문장으로 정의, 조건, 핵심 근거를 먼저 제시한다.</p></div>
          <div class="sys-label"><div class="t-cat">02 Entity clarity</div><p class="body-sm" style="margin-top:8px">브랜드, 제품, 카테고리, 비교 대상 표기를 일관화한다.</p></div>
          <div class="sys-label"><div class="t-cat">03 Evidence pack</div><p class="body-sm" style="margin-top:8px">수치, 날짜, 방법론, 원문 출처를 본문 가까이에 둔다.</p></div>
        </div>
        <div style="position:relative;min-height:44vh">
          <svg class="sys-svg" viewBox="0 0 640 420" role="img" aria-label="AEO content system geometry">
            <rect x="40" y="40" width="560" height="86" fill="none" stroke="currentColor" stroke-width="1"/><rect x="80" y="168" width="210" height="84" fill="var(--accent)"/><rect x="350" y="168" width="210" height="84" fill="none" stroke="currentColor" stroke-width="1"/><rect x="160" y="294" width="320" height="72" fill="none" stroke="currentColor" stroke-width="1"/><path d="M320 126 V168 M290 210 H350 M320 252 V294" stroke="currentColor" stroke-width="1" fill="none"/>
          </svg>
          <div class="card-fill" style="position:absolute;left:8%;top:8%;width:84%"><div class="t-meta">Question mapped page</div></div>
          <div class="card-accent" style="position:absolute;left:14%;top:43%;width:28%"><div class="t-meta" style="color:rgba(255,255,255,.76)">Answer</div></div>
          <div class="card-fill" style="position:absolute;right:14%;top:43%;width:28%"><div class="t-meta">Schema</div></div>
          <div class="card-fill" style="position:absolute;left:30%;bottom:10%;width:40%"><div class="t-meta">Citation evidence</div></div>
        </div>
      </div>
      <div class="foot">Sources: Google Search Central AI optimization and structured data docs.</div>
    </div>
  </section>
  <section class="slide" data-layout="S20" data-animate="ledger">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Measurement</div><div class="r">06 / 08</div></div>
      <div class="t-meta">Dashboard expansion</div>
      <h2 class="h-xl" style="font-size:min(5.2vw,8.2vh);max-width:16ch;margin-top:1.2vh">트래픽 KPI에서<br>답변 점유율 KPI로</h2>
      <div class="stacked-ledger nav-safe-bottom-tight" style="margin-top:2.2vh">
        <div class="ledger-row" style="padding:1vh 0"><div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">01</div><div><div class="t-cat">AI citation rate</div><p class="body-sm" style="margin-top:8px">핵심 질의에서 우리 URL이 출처 또는 관련 링크로 등장하는 비율.</p></div><div class="t-meta">Visibility</div></div>
        <div class="ledger-row" style="padding:1vh 0"><div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">02</div><div><div class="t-cat">Answer coverage</div><p class="body-sm" style="margin-top:8px">질의 맵 기준으로 답변 가능한 콘텐츠가 있는 토픽 비율.</p></div><div class="t-meta">Coverage</div></div>
        <div class="ledger-row" style="padding:1vh 0"><div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">03</div><div><div class="t-cat">Answer sentiment</div><p class="body-sm" style="margin-top:8px">AI 답변에서 브랜드·제품이 정확하고 유리하게 설명되는 정도.</p></div><div class="t-meta">Quality</div></div>
        <div class="ledger-row" style="padding:1vh 0"><div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">04</div><div><div class="t-cat">Assisted conversion</div><p class="body-sm" style="margin-top:8px">AI 검색 접점 이후 발생하는 직접·간접 전환 기여.</p></div><div class="t-meta">Business</div></div>
      </div>
      <div class="foot">Keep SEO dashboards; add answer-layer monitoring by topic cluster.</div>
    </div>
  </section>
  <section class="slide" data-layout="S11" data-animate="timeline">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Roadmap</div><div class="r">07 / 08</div></div>
      <div class="t-meta">90-day transition</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">운영 리듬에<br>AEO를 넣는다</h2>
      <div class="timeline-h nav-safe-bottom-tight" style="--count:5;margin-top:5vh">
        <div class="tl-h-node"><div class="t-cat">Week 1-2</div><p class="body-sm" style="margin-top:12px">매출·브랜드 방어 질의 20개 선정</p></div>
        <div class="tl-h-node"><div class="t-cat">Week 3-4</div><p class="body-sm" style="margin-top:12px">상위 SEO 페이지 answer-readiness 감사</p></div>
        <div class="tl-h-node"><div class="t-cat">Week 5-8</div><p class="body-sm" style="margin-top:12px">답변 블록, FAQ, schema, 근거 패키지 반영</p></div>
        <div class="tl-h-node"><div class="t-cat">Week 9-10</div><p class="body-sm" style="margin-top:12px">AI citation과 answer coverage 측정 시작</p></div>
        <div class="tl-h-node"><div class="t-cat">Week 11-12</div><p class="body-sm" style="margin-top:12px">오류·누락 케이스를 SEO backlog에 편입</p></div>
      </div>
      <div class="foot">Success signal: visible citation or answer mention in five priority topics.</div>
    </div>
  </section>
  <section class="slide split" data-layout="S10" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-accent"><canvas class="ascii-bg" aria-hidden="true"></canvas><div class="chrome-min"><div class="l">Decision</div><div class="r">08 / 08</div></div><div style="margin-top:auto"><h2 class="h-statement">랭킹만<br>볼 것인가,<br>답변 선택까지<br>볼 것인가.</h2></div></div>
      <div class="half b-paper"><div class="chrome-min"><div class="l">Next actions</div><div class="r">End</div></div><div style="display:grid;gap:18px;margin:auto 0">
        <div class="card-fill"><div class="t-meta">Keep</div><h3 class="h-md">SEO 기반</h3><p class="body-sm">색인, 기술 SEO, 콘텐츠 품질, 링크 신호는 계속 유지한다.</p></div>
        <div class="card-fill"><div class="t-meta">Add</div><h3 class="h-md">AEO 기준</h3><p class="body-sm">질문별 answer block, entity consistency, citation monitoring을 운영 기준에 추가한다.</p></div>
        <div class="card-fill"><div class="t-meta">Start</div><h3 class="h-md accent-text">상위 50개 페이지 감사</h3><p class="body-sm">기존 SEO 자산에서 AEO 전환 효율이 가장 높은 페이지부터 점검한다.</p></div>
      </div></div>
    </div>
  </section>
`;

const v2 = String.raw`
  <section class="slide accent active" data-layout="S01" data-animate="hero">
    <div class="canvas-card">
      <canvas class="ascii-bg" aria-hidden="true"></canvas>
      <div class="chrome-min"><div class="l">V2 Executive Metrics</div><div class="r">01 / 08</div></div>
      <div style="margin:auto 0;display:grid;gap:2vh">
        <div class="t-meta" style="color:rgba(255,255,255,.78)">Management readout</div>
        <h1 class="h-hero">AI 검색은<br>유입 지표를<br>다시 쓴다</h1>
        <p class="lead" style="color:rgba(255,255,255,.86);max-width:48ch">SEO 성과를 트래픽만으로 판단하던 방식에서, AI 답변 안의 점유율과 citation을 같이 보는 방식으로 옮겨야 한다.</p>
      </div>
      <div class="foot" style="color:rgba(255,255,255,.62)">Future tightened slide / version 2</div>
    </div>
  </section>
  <section class="slide" data-layout="S18" data-animate="why-now">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Why now</div><div class="r">02 / 08</div></div>
      <div class="t-meta">Three pressure signals</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">지금 전환해야<br>하는 이유</h2>
      <div class="why-now-grid nav-safe-bottom-tight" style="margin-top:5vh">
        <div class="why-col"><div class="t-cat">Adoption</div><p class="body" style="margin-top:18px">AI Overviews는 2025년 3월 기준 Google의 대표 AI 검색 기능으로 확대됐다.</p><div class="why-num-bottom">1B+</div></div>
        <div class="why-col"><div class="t-cat">Behavior</div><p class="body" style="margin-top:18px">AI summary가 있으면 전통 검색결과 클릭이 낮아진다.</p><div class="why-num-bottom">8%</div></div>
        <div class="why-col" style="border-top-color:var(--accent)"><div class="t-cat">Query depth</div><p class="body" style="margin-top:18px">10단어 이상 긴 검색에서 AI summary가 더 자주 생성된다.</p><div class="why-num-bottom accent-text">53%</div></div>
      </div>
      <div class="foot">Sources: Google Search blog; Pew Research Center, 2025.</div>
    </div>
  </section>
  <section class="slide" data-layout="S06" data-animate="kpi">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">KPI tower</div><div class="r">03 / 08</div></div>
      <div class="grid-12" style="align-items:start;gap:24px">
        <div class="span-5"><div class="t-meta">Search behavior</div><h2 class="h-xl" style="font-size:min(5.4vw,8.8vh);margin-top:1.2vh">AI summary가<br>나타나는 순간</h2></div>
        <div class="span-7"><p class="lead" style="margin-top:2vh">질문이 길고 구체적일수록 검색은 더 많이 답변형 화면으로 이동한다. 이는 콘텐츠 단위를 페이지가 아니라 답변 후보로 설계해야 한다는 신호다.</p></div>
      </div>
      <div class="kpi-tower-row nav-safe-bottom-tight" style="margin-top:2vh;align-items:end">
        <div class="card-outlined" style="padding:16px"><div class="bar-tower" style="--h:6vh"></div><div class="mono" style="font:600 18px/1 var(--mono);letter-spacing:0;color:var(--accent);margin-top:12px">8%</div><p class="body-sm" style="margin-top:8px">1-2단어 검색의 AI summary 생성</p></div>
        <div class="card-outlined" style="padding:16px"><div class="bar-tower" style="--h:13vh"></div><div class="mono" style="font:600 18px/1 var(--mono);letter-spacing:0;color:var(--accent);margin-top:12px">36%</div><p class="body-sm" style="margin-top:8px">문장형 검색의 AI summary 생성</p></div>
        <div class="card-outlined" style="padding:16px"><div class="bar-tower" style="--h:18vh"></div><div class="mono" style="font:600 18px/1 var(--mono);letter-spacing:0;color:var(--accent);margin-top:12px">53%</div><p class="body-sm" style="margin-top:8px">10단어 이상 검색의 AI summary 생성</p></div>
        <div class="card-outlined" style="padding:16px"><div class="bar-tower" style="--h:21vh"></div><div class="mono" style="font:600 18px/1 var(--mono);letter-spacing:0;color:var(--accent);margin-top:12px">60%</div><p class="body-sm" style="margin-top:8px">의문사 검색의 AI summary 생성</p></div>
      </div>
      <div class="foot">Source: Pew Research Center, 2025. Tower height is proportional to percentage.</div>
    </div>
  </section>
  <section class="slide" data-layout="S15" data-animate="matrix">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Audit matrix</div><div class="r">04 / 08</div></div>
      <div class="t-meta">Answer-readiness inventory</div>
      <h2 class="h-xl" style="max-width:13ch;margin-top:1.2vh">상위 페이지를<br>답변 후보로 전환</h2>
      <div class="matrix-fill nav-safe-bottom-tight" style="margin-top:4vh">
        <div class="matrix-cell"><div class="t-cat">Definition</div><p class="body-sm">핵심 용어 정의가 첫 화면에 있는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">FAQ</div><p class="body-sm">질문형 검색 의도에 직접 답하는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Schema</div><p class="body-sm">보이는 콘텐츠와 structured data가 일치하는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Evidence</div><p class="body-sm">수치, 날짜, 출처가 본문 가까이에 있는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Entity</div><p class="body-sm">브랜드·제품 표기가 일관적인가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Comparison</div><p class="body-sm">대체재와 차이를 명확히 설명하는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Freshness</div><p class="body-sm">업데이트 날짜와 변경 이력이 있는가.</p></div>
        <div class="matrix-cell"><div class="t-cat">Internal link</div><p class="body-sm">답변에서 상세 근거로 이동할 경로가 있는가.</p></div>
      </div>
      <div class="hero-stat-bottom"><div class="num-mega accent-text" style="font-size:min(10vw,13vh)">50</div><p class="lead">초기 감사 대상은 기존 SEO 상위 페이지 50개로 충분하다.</p></div>
    </div>
  </section>
  <section class="slide" data-layout="S05" data-animate="stack">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Three layers</div><div class="r">05 / 08</div></div>
      <div class="t-meta">Operating layers</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">AEO 운영은<br>세 층으로 나뉜다</h2>
      <div class="stack-row nav-safe-bottom-tight" style="margin-top:auto;margin-bottom:5vh">
        <div class="card-fill"><div class="t-cat">Content layer</div><h3 class="h-md" style="margin-top:18px">답변 블록</h3><p class="body-sm" style="margin-top:12px">정의, 조건, 근거, 예외를 문단 단위로 재구성한다.</p></div>
        <div class="card-fill"><div class="t-cat">Technical layer</div><h3 class="h-md" style="margin-top:18px">검색 접근성</h3><p class="body-sm" style="margin-top:12px">색인 가능성, semantic HTML, structured data를 유지한다.</p></div>
        <div class="card-accent"><div class="t-meta" style="color:rgba(255,255,255,.74)">Measurement layer</div><h3 class="h-md" style="margin-top:18px">답변 점유율</h3><p class="body-sm" style="margin-top:12px;color:rgba(255,255,255,.86)">citation, answer coverage, sentiment를 토픽별로 본다.</p></div>
      </div>
    </div>
  </section>
  <section class="slide" data-layout="S21" data-animate="spec">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Spec sheet</div><div class="r">06 / 08</div></div>
      <div class="tech-spec nav-safe-bottom-tight">
        <div class="spec-title-col">
          <div class="t-meta">Program specification</div>
          <h2 class="h-xl" style="max-width:10ch;margin-top:1.2vh">AEO 전환<br>운영 스펙</h2>
          <p class="lead" style="margin-top:3vh">기존 SEO 프로세스에 작은 측정 레이어를 붙이는 방식으로 시작한다.</p>
        </div>
        <div style="display:grid;gap:24px;align-content:center">
          <div class="spec-kpi-grid">
            <div class="card-fill"><div class="t-cat">20</div><p class="body-sm">우선 질의</p></div>
            <div class="card-fill"><div class="t-cat">50</div><p class="body-sm">감사 페이지</p></div>
            <div class="card-fill"><div class="t-cat">90D</div><p class="body-sm">초기 전환</p></div>
          </div>
          <div class="card-outlined">
            <div class="t-meta">Workload mix</div>
            <div class="spec-bars" style="margin-top:18px">
              <div class="bar-vert" style="--h:14vh"></div><div class="bar-vert" style="--h:20vh"></div><div class="bar-vert" style="--h:28vh"></div><div class="bar-vert" style="--h:18vh"></div><div class="bar-vert" style="--h:24vh"></div>
            </div>
            <p class="body-sm" style="margin-top:16px">Audit, rewrite, schema, measurement, backlog의 다섯 작업 묶음.</p>
          </div>
        </div>
      </div>
      <div class="foot">Spec is a pilot scope, not a headcount model.</div>
    </div>
  </section>
  <section class="slide" data-layout="S11" data-animate="timeline">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Decision timeline</div><div class="r">07 / 08</div></div>
      <div class="t-meta">90-day executive cadence</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">의사결정은<br>3번이면 충분하다</h2>
      <div class="timeline-h nav-safe-bottom-tight" style="--count:4;margin-top:7vh">
        <div class="tl-h-node"><div class="t-cat">Day 0</div><p class="body-sm" style="margin-top:12px">토픽·페이지 범위 승인</p></div>
        <div class="tl-h-node"><div class="t-cat">Day 30</div><p class="body-sm" style="margin-top:12px">초기 감사와 quick win 승인</p></div>
        <div class="tl-h-node"><div class="t-cat">Day 60</div><p class="body-sm" style="margin-top:12px">리라이트와 schema 반영 결과 확인</p></div>
        <div class="tl-h-node"><div class="t-cat">Day 90</div><p class="body-sm" style="margin-top:12px">AI visibility 지표를 정규 KPI에 편입</p></div>
      </div>
      <div class="foot">Executive ask: approve the initial AEO audit sprint.</div>
    </div>
  </section>
  <section class="slide split" data-layout="S10" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-accent"><canvas class="ascii-bg" aria-hidden="true"></canvas><div class="chrome-min"><div class="l">Recommendation</div><div class="r">08 / 08</div></div><div style="margin-top:auto"><h2 class="h-statement">삭제가 아니라<br>측정 레이어<br>추가다.</h2></div></div>
      <div class="half b-paper"><div class="chrome-min"><div class="l">Board note</div><div class="r">End</div></div><div style="display:grid;gap:18px;margin:auto 0">
        <div class="card-fill"><div class="t-meta">Decision</div><h3 class="h-md">90일 파일럿 승인</h3><p class="body-sm">기존 SEO 운영을 중단하지 않고 AEO audit을 추가한다.</p></div>
        <div class="card-fill"><div class="t-meta">Risk</div><h3 class="h-md">트래픽 감소 오판</h3><p class="body-sm">클릭 감소가 브랜드 노출 감소인지, 답변 내 존재감 전환인지 구분한다.</p></div>
        <div class="card-fill"><div class="t-meta">Outcome</div><h3 class="h-md accent-text">토픽별 answer share</h3><p class="body-sm">순위 보고서에 answer-layer visibility를 병기한다.</p></div>
      </div></div>
    </div>
  </section>
`;

const v3 = String.raw`
  <section class="slide accent active" data-layout="S01" data-animate="hero">
    <div class="canvas-card">
      <canvas class="ascii-bg" aria-hidden="true"></canvas>
      <div class="chrome-min"><div class="l">V3 Framework Workshop</div><div class="r">01 / 08</div></div>
      <div style="margin:auto 0;display:grid;gap:2.2vh">
        <div class="t-meta" style="color:rgba(255,255,255,.78)">Workshop deck</div>
        <h1 class="h-hero">AEO를<br>어떻게<br>일로 만들까</h1>
        <p class="lead" style="color:rgba(255,255,255,.86);max-width:48ch">팀이 바로 적용할 수 있도록 질문 맵, 콘텐츠 구조, 측정 루프를 하나의 운영 프레임워크로 정리한다.</p>
      </div>
      <div class="foot" style="color:rgba(255,255,255,.62)">Future tightened slide / version 3</div>
    </div>
  </section>
  <section class="slide" data-layout="S12" data-animate="manifesto">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Manifesto</div><div class="r">02 / 08</div></div>
      <div class="manifesto-top">
        <div><div class="t-meta">Operating principle</div><h2 class="h-statement" style="margin-top:2vh">답변은<br>페이지보다<br>작은 단위로<br>선택된다.</h2></div>
        <p class="lead" style="margin-top:8vh">그래서 AEO 작업은 긴 문서를 더 쓰는 일이 아니라, 엔진이 집어갈 수 있는 단락과 근거를 설계하는 일이다.</p>
      </div>
      <div class="ink-banner-full nav-safe-bottom-tight"><div class="t-meta" style="color:rgba(255,255,255,.68)">Rule</div><h3 class="h-md" style="margin-top:1vh">하나의 페이지는 여러 답변 후보를 담는 컨테이너다.</h3></div>
    </div>
  </section>
  <section class="slide" data-layout="S04" data-animate="grid">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Six blocks</div><div class="r">03 / 08</div></div>
      <div class="t-meta">AEO page anatomy</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">한 페이지가<br>갖춰야 할 6개 블록</h2>
      <div class="sub-grid-3-2 nav-safe-bottom-tight" style="margin-top:4vh;min-height:44vh">
        <div><div class="t-cat">Question</div><p class="body-sm" style="margin-top:12px">사용자가 실제로 묻는 문장.</p></div>
        <div><div class="t-cat">Short answer</div><p class="body-sm" style="margin-top:12px">두세 문장으로 끝나는 직접 답변.</p></div>
        <div><div class="t-cat">Proof</div><p class="body-sm" style="margin-top:12px">수치, 사례, 원문 출처.</p></div>
        <div><div class="t-cat">Boundary</div><p class="body-sm" style="margin-top:12px">예외, 조건, 적용 범위.</p></div>
        <div><div class="t-cat">Entity</div><p class="body-sm" style="margin-top:12px">브랜드·제품·카테고리 표기.</p></div>
        <div><div class="t-cat">Next step</div><p class="body-sm" style="margin-top:12px">상세 근거 또는 전환 경로.</p></div>
      </div>
    </div>
  </section>
  <section class="slide" data-layout="S13" data-animate="forces">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Three forces</div><div class="r">04 / 08</div></div>
      <div class="three-forces nav-safe-bottom-tight" style="margin-top:2vh">
        <div class="hero-ink-col"><div class="t-meta" style="color:rgba(255,255,255,.68)">Force map</div><h2 class="h-md">AEO 전환을<br>밀어내는<br>세 가지 힘</h2><p class="body-sm" style="color:rgba(255,255,255,.78)">사용자 행동, 검색 제품, 콘텐츠 측정이 동시에 변한다.</p></div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
          <div class="force-card"><div class="force-num">01</div><div class="t-cat">Longer queries</div><p class="body-sm" style="margin-top:12px">대화형·문장형 검색은 요약 답변을 더 자주 만든다.</p></div>
          <div class="force-card"><div class="force-num">02</div><div class="t-cat">Fewer clicks</div><p class="body-sm" style="margin-top:12px">답변이 충분하면 링크 클릭은 뒤로 밀린다.</p></div>
          <div class="force-card"><div class="force-num">03</div><div class="t-cat">New attribution</div><p class="body-sm" style="margin-top:12px">브랜드는 방문 전 답변 안에서 먼저 평가된다.</p></div>
        </div>
      </div>
    </div>
  </section>
  <section class="slide" data-layout="S14" data-animate="loop">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Loop</div><div class="r">05 / 08</div></div>
      <div class="t-meta">AEO operating loop</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">반복 루프로<br>운영한다</h2>
      <div class="loop-diagram nav-safe-bottom-tight" style="margin-top:3vh">
        <div class="loop-steps" style="gap:8px">
          <div class="card-fill" style="padding:12px 16px"><div class="t-cat">01 Map questions</div><p class="body-sm" style="font-size:max(11px,.78vw);margin-top:5px">핵심 고객 질문과 검색 의도를 묶는다.</p></div>
          <div class="card-fill" style="padding:12px 16px"><div class="t-cat">02 Rewrite answers</div><p class="body-sm" style="font-size:max(11px,.78vw);margin-top:5px">짧은 답변, 근거, 예외를 재구성한다.</p></div>
          <div class="card-fill" style="padding:12px 16px"><div class="t-cat">03 Measure citations</div><p class="body-sm" style="font-size:max(11px,.78vw);margin-top:5px">AI 답변 노출과 출처 등장을 확인한다.</p></div>
          <div class="card-fill" style="padding:12px 16px"><div class="t-cat">04 Feed backlog</div><p class="body-sm" style="font-size:max(11px,.78vw);margin-top:5px">누락과 오류를 다음 SEO 작업으로 보낸다.</p></div>
        </div>
        <div style="position:relative;min-height:34vh">
          <svg class="loop-svg" viewBox="0 0 520 420" role="img" aria-label="AEO loop geometry" style="min-height:34vh">
            <path d="M260 50 C370 50 460 140 460 250 C460 330 395 380 320 380" fill="none" stroke="currentColor" stroke-width="2"/>
            <path d="M260 370 C150 370 60 280 60 170 C60 90 125 40 200 40" fill="none" stroke="var(--accent)" stroke-width="10"/>
            <rect x="226" y="26" width="68" height="68" fill="var(--accent)"/><rect x="426" y="216" width="68" height="68" fill="none" stroke="currentColor" stroke-width="1"/><rect x="226" y="326" width="68" height="68" fill="none" stroke="currentColor" stroke-width="1"/><rect x="26" y="136" width="68" height="68" fill="none" stroke="currentColor" stroke-width="1"/>
          </svg>
          <div class="card-accent" style="position:absolute;left:41%;top:5%;width:18%;padding:16px"><div class="t-meta" style="color:rgba(255,255,255,.78)">Map</div></div>
          <div class="card-fill" style="position:absolute;right:3%;top:46%;width:22%;padding:16px"><div class="t-meta">Rewrite</div></div>
          <div class="card-fill" style="position:absolute;left:41%;top:62%;width:22%;padding:16px"><div class="t-meta">Measure</div></div>
          <div class="card-fill" style="position:absolute;left:3%;top:31%;width:22%;padding:16px"><div class="t-meta">Backlog</div></div>
        </div>
      </div>
    </div>
  </section>
  <section class="slide" data-layout="S19" data-animate="cards">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Four cards</div><div class="r">06 / 08</div></div>
      <div class="t-meta">Team responsibilities</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">누가 무엇을<br>맡아야 하는가</h2>
      <div class="four-cards nav-safe-bottom-tight" style="margin-top:5vh">
        <div class="fc-col"><div class="t-cat">SEO</div><p class="body-sm" style="margin-top:18px">질의 맵, 기존 순위, 내부링크, 색인 상태를 관리한다.</p></div>
        <div class="fc-col"><div class="t-cat">Content</div><p class="body-sm" style="margin-top:18px">답변 블록과 근거 문단을 작성한다.</p></div>
        <div class="fc-col"><div class="t-cat">Engineering</div><p class="body-sm" style="margin-top:18px">semantic HTML, schema, 렌더링 접근성을 보장한다.</p></div>
        <div class="fc-col"><div class="t-cat">Analytics</div><p class="body-sm" style="margin-top:18px">citation, answer coverage, 전환 기여를 측정한다.</p></div>
      </div>
      <div class="foot">AEO is cross-functional, but it starts inside the SEO operating rhythm.</div>
    </div>
  </section>
  <section class="slide" data-layout="S02" data-animate="timeline">
    <div class="canvas-card">
      <div class="chrome-min"><div class="l">Vertical timeline</div><div class="r">07 / 08</div></div>
      <div class="t-meta">Workshop agenda</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">하루 워크숍으로<br>시작한다</h2>
      <div class="grid-12 nav-safe-bottom-tight" style="margin-top:4vh;gap:36px">
        <div class="span-7 timeline-v">
          <div class="tl-node"><div class="tl-axis"><div class="dot"></div></div><div><div class="t-cat">09:30</div><p class="body-sm" style="margin-top:8px">핵심 토픽과 고객 질문 선정</p></div></div>
          <div class="tl-node"><div class="tl-axis"><div class="dot"></div></div><div><div class="t-cat">11:00</div><p class="body-sm" style="margin-top:8px">상위 페이지 answer-readiness 점검</p></div></div>
          <div class="tl-node"><div class="tl-axis"><div class="dot"></div></div><div><div class="t-cat">14:00</div><p class="body-sm" style="margin-top:8px">페이지 리라이트 패턴 합의</p></div></div>
          <div class="tl-node"><div class="tl-axis"><div class="dot"></div></div><div><div class="t-cat">16:00</div><p class="body-sm" style="margin-top:8px">측정 지표와 30일 backlog 확정</p></div></div>
        </div>
        <div class="span-5 kpi-row-4" style="grid-template-columns:repeat(2,1fr);align-content:start">
          <div class="card-fill"><div class="t-cat">20</div><p class="body-sm">질문</p></div><div class="card-fill"><div class="t-cat">10</div><p class="body-sm">페이지</p></div><div class="card-fill"><div class="t-cat">3</div><p class="body-sm">패턴</p></div><div class="card-accent"><div class="t-meta" style="color:rgba(255,255,255,.78)">30D</div><p class="body-sm" style="color:rgba(255,255,255,.86)">backlog</p></div>
        </div>
      </div>
    </div>
  </section>
  <section class="slide split" data-layout="S10" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-accent"><canvas class="ascii-bg" aria-hidden="true"></canvas><div class="chrome-min"><div class="l">Workshop close</div><div class="r">08 / 08</div></div><div style="margin-top:auto"><h2 class="h-statement">첫 작업은<br>새 콘텐츠가<br>아니다.</h2></div></div>
      <div class="half b-paper"><div class="chrome-min"><div class="l">Output</div><div class="r">End</div></div><div style="display:grid;gap:18px;margin:auto 0">
        <div class="card-fill"><div class="t-meta">01</div><h3 class="h-md">질문 맵</h3><p class="body-sm">상위 토픽을 고객 질문으로 바꾼다.</p></div>
        <div class="card-fill"><div class="t-meta">02</div><h3 class="h-md">페이지 감사표</h3><p class="body-sm">기존 페이지의 answer-readiness를 점수화한다.</p></div>
        <div class="card-fill"><div class="t-meta">03</div><h3 class="h-md accent-text">30일 backlog</h3><p class="body-sm">가장 빨리 바꿀 수 있는 답변 블록부터 고친다.</p></div>
      </div></div>
    </div>
  </section>
`;

const outputs = [
  ["v1-balanced-analysis", v1],
  ["v2-executive-metrics", v2],
  ["v3-framework-workshop", v3],
].map(([name, slides]) => writeDeck(name, slides));

outputs.forEach((file) => console.log(file));
