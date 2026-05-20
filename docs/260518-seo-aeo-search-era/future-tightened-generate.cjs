const fs = require("node:fs");
const path = require("node:path");

const templatePath = "/tmp/future-slide-skill-codex-260518/skills/tightened-slide/assets/template.html";
const outDir = path.join(__dirname, "future-tightened");
const outFile = path.join(outDir, "index.html");

fs.mkdirSync(path.join(outDir, "images"), { recursive: true });

const template = fs.readFileSync(templatePath, "utf8");

const slides = String.raw`
  <section class="slide accent active" data-layout="S01" data-animate="hero">
    <div class="canvas-card">
      <canvas class="ascii-bg" aria-hidden="true"></canvas>
      <div class="chrome-min">
        <div class="l">SEO -> AEO</div>
        <div class="r">01 / 08</div>
      </div>
      <div style="display:grid;gap:2.4vh;margin-top:auto;margin-bottom:auto">
        <div class="t-meta" style="color:rgba(255,255,255,.78)">Search strategy field note</div>
        <h1 class="h-hero">링크 순위에서<br>답변 채택으로</h1>
        <p class="lead" style="color:rgba(255,255,255,.86);max-width:48ch">AI 검색 시대의 SEO는 사라지지 않는다. 다만 목표가 검색 결과 노출에서 답변 엔진이 선택하는 근거까지 확장된다.</p>
      </div>
      <div class="foot" style="color:rgba(255,255,255,.62)">Sample deck generated with future-slide-skill / tightened-slide</div>
    </div>
  </section>

  <section class="slide split" data-layout="S03" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-ink">
        <div class="chrome-min">
          <div class="l">Thesis</div>
          <div class="r">02 / 08</div>
        </div>
        <div style="margin-top:auto">
          <h2 class="h-statement">SEO는<br>기반이고,<br>AEO는<br>새 레이어다.</h2>
        </div>
      </div>
      <div class="half b-paper">
        <div class="chrome-min">
          <div class="l">What changed</div>
          <div class="r">Answer interface</div>
        </div>
        <div style="display:grid;gap:24px;margin:auto 0;max-width:58ch">
          <p class="lead">검색 결과는 링크 목록에서 요약 답변, 출처, 후속 질문, 행동으로 이어지는 인터페이스로 이동하고 있다.</p>
          <div class="card-fill">
            <div class="t-meta">Practical implication</div>
            <p class="body" style="margin-top:10px">기존 색인·랭킹 최적화는 유지하되, 질의별 답변 블록과 근거 패키지를 운영 단위로 추가해야 한다.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="S07" data-animate="bars">
    <div class="canvas-card">
      <div class="chrome-min">
        <div class="l">Behavior signal</div>
        <div class="r">03 / 08</div>
      </div>
      <div class="t-meta">Pew Research Center, 2025</div>
      <h2 class="h-xl" style="max-width:10ch;margin-top:1.2vh">클릭은 이미 줄고 있다</h2>
      <div class="h-bar-chart nav-safe-bottom-tight" style="margin-top:5vh;max-width:92vw">
        <div class="bar-row">
          <div class="body">AI summary가 있는 검색의 전통 결과 클릭</div>
          <div class="bar-fill" style="--w:27%"></div>
          <div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">8%</div>
        </div>
        <div class="bar-row">
          <div class="body">AI summary가 없는 검색의 전통 결과 클릭</div>
          <div class="bar-fill" style="--w:50%"></div>
          <div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">15%</div>
        </div>
        <div class="bar-row">
          <div class="body">AI summary 내 출처 링크 클릭</div>
          <div class="bar-fill" style="--w:3%"></div>
          <div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">1%</div>
        </div>
        <div class="bar-row">
          <div class="body">AI summary가 있는 검색 후 세션 종료</div>
          <div class="bar-fill" style="--w:87%"></div>
          <div class="mono" style="font:500 13px/1 var(--mono);letter-spacing:0;color:var(--text-secondary)">26%</div>
        </div>
      </div>
      <div class="foot">Source: Pew Research Center, July 22 2025. Bar scale max = 30%.</div>
    </div>
  </section>

  <section class="slide" data-layout="S08" data-animate="compare">
    <div class="canvas-card">
      <div class="chrome-min">
        <div class="l">Operating model</div>
        <div class="r">04 / 08</div>
      </div>
      <div class="t-meta">From ranking to answer-readiness</div>
      <h2 class="h-xl" style="max-width:13ch;margin-top:1.2vh">SEO와 AEO의 역할 분담</h2>
      <div class="duo-compare nav-safe-bottom-tight" style="margin-top:4vh">
        <div style="display:flex;flex-direction:column;gap:18px">
          <div class="t-cat">SEO</div>
          <div class="card-fill"><div class="t-meta">Goal</div><p class="body">검색 결과에서 발견되고 클릭될 가능성을 높인다.</p></div>
          <div class="card-fill"><div class="t-meta">Primary unit</div><p class="body">키워드, 페이지, 내부링크, 색인 상태, SERP feature.</p></div>
          <div class="card-fill"><div class="t-meta">Metric</div><p class="body">Rank, CTR, organic sessions, conversion.</p></div>
        </div>
        <div class="vrule"></div>
        <div style="display:flex;flex-direction:column;gap:18px">
          <div class="t-cat">AEO</div>
          <div class="card-fill"><div class="t-meta">Goal</div><p class="body">AI 답변 안에서 언급·인용·추천될 가능성을 높인다.</p></div>
          <div class="card-fill"><div class="t-meta">Primary unit</div><p class="body">질문-답변 블록, entity 설명, 근거 단락, structured data.</p></div>
          <div class="card-fill"><div class="t-meta">Metric</div><p class="body">Citation rate, answer coverage, share of answer.</p></div>
        </div>
      </div>
      <div class="foot">Google frames AEO/GEO as generative AI search optimization inside broader SEO.</div>
    </div>
  </section>

  <section class="slide" data-layout="S17" data-animate="system">
    <div class="canvas-card">
      <div class="chrome-min">
        <div class="l">System</div>
        <div class="r">05 / 08</div>
      </div>
      <div class="t-meta">AEO-ready content architecture</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">정답 후보로 읽히는 페이지</h2>
      <div class="system-diagram nav-safe-bottom-tight" style="margin-top:4vh">
        <div style="display:grid;gap:16px">
          <div class="sys-label">
            <div class="t-cat">01 Answer-first block</div>
            <p class="body-sm" style="margin-top:8px">2-4문장으로 정의, 조건, 핵심 근거를 먼저 제시한다.</p>
          </div>
          <div class="sys-label">
            <div class="t-cat">02 Entity clarity</div>
            <p class="body-sm" style="margin-top:8px">브랜드, 제품, 카테고리, 비교 대상 표기를 일관화한다.</p>
          </div>
          <div class="sys-label">
            <div class="t-cat">03 Evidence pack</div>
            <p class="body-sm" style="margin-top:8px">수치, 날짜, 방법론, 원문 출처를 본문 가까이에 둔다.</p>
          </div>
        </div>
        <div style="position:relative;min-height:44vh">
          <svg class="sys-svg" viewBox="0 0 640 420" role="img" aria-label="AEO content system geometry">
            <rect x="40" y="40" width="560" height="86" fill="none" stroke="currentColor" stroke-width="1"/>
            <rect x="80" y="168" width="210" height="84" fill="var(--accent)"/>
            <rect x="350" y="168" width="210" height="84" fill="none" stroke="currentColor" stroke-width="1"/>
            <rect x="160" y="294" width="320" height="72" fill="none" stroke="currentColor" stroke-width="1"/>
            <path d="M320 126 V168 M290 210 H350 M320 252 V294" stroke="currentColor" stroke-width="1" fill="none"/>
          </svg>
          <div class="card-fill" style="position:absolute;left:8%;top:8%;width:84%">
            <div class="t-meta">Question mapped page</div>
          </div>
          <div class="card-accent" style="position:absolute;left:14%;top:43%;width:28%">
            <div class="t-meta" style="color:rgba(255,255,255,.76)">Answer</div>
          </div>
          <div class="card-fill" style="position:absolute;right:14%;top:43%;width:28%">
            <div class="t-meta">Schema</div>
          </div>
          <div class="card-fill" style="position:absolute;left:30%;bottom:10%;width:40%">
            <div class="t-meta">Citation evidence</div>
          </div>
        </div>
      </div>
      <div class="foot">Sources: Google Search Central AI optimization and structured data docs.</div>
    </div>
  </section>

  <section class="slide" data-layout="S20" data-animate="ledger">
    <div class="canvas-card">
      <div class="chrome-min">
        <div class="l">Measurement</div>
        <div class="r">06 / 08</div>
      </div>
      <div class="t-meta">Dashboard expansion</div>
      <h2 class="h-xl" style="font-size:min(5.2vw,8.2vh);max-width:16ch;margin-top:1.2vh">트래픽 KPI에서 답변 점유율 KPI로</h2>
      <div class="stacked-ledger nav-safe-bottom-tight" style="margin-top:2.2vh">
        <div class="ledger-row" style="padding:1vh 0">
          <div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">01</div>
          <div><div class="t-cat">AI citation rate</div><p class="body-sm" style="margin-top:8px">핵심 질의에서 우리 URL이 출처 또는 관련 링크로 등장하는 비율.</p></div>
          <div class="t-meta">Visibility</div>
        </div>
        <div class="ledger-row" style="padding:1vh 0">
          <div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">02</div>
          <div><div class="t-cat">Answer coverage</div><p class="body-sm" style="margin-top:8px">질의 맵 기준으로 답변 가능한 콘텐츠가 있는 토픽 비율.</p></div>
          <div class="t-meta">Coverage</div>
        </div>
        <div class="ledger-row" style="padding:1vh 0">
          <div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">03</div>
          <div><div class="t-cat">Answer sentiment</div><p class="body-sm" style="margin-top:8px">AI 답변에서 브랜드·제품이 정확하고 유리하게 설명되는 정도.</p></div>
          <div class="t-meta">Quality</div>
        </div>
        <div class="ledger-row" style="padding:1vh 0">
          <div class="ledger-num" style="font-size:min(6.2vw,8.6vh)">04</div>
          <div><div class="t-cat">Assisted conversion</div><p class="body-sm" style="margin-top:8px">AI 검색 접점 이후 발생하는 직접·간접 전환 기여.</p></div>
          <div class="t-meta">Business</div>
        </div>
      </div>
      <div class="foot">Keep Search Console and SEO dashboards; add answer-layer monitoring by topic cluster.</div>
    </div>
  </section>

  <section class="slide" data-layout="S11" data-animate="timeline">
    <div class="canvas-card">
      <div class="chrome-min">
        <div class="l">Roadmap</div>
        <div class="r">07 / 08</div>
      </div>
      <div class="t-meta">90-day transition</div>
      <h2 class="h-xl" style="max-width:12ch;margin-top:1.2vh">운영 리듬에 AEO를 넣는다</h2>
      <div class="timeline-h nav-safe-bottom-tight" style="--count:5;margin-top:5vh">
        <div class="tl-h-node">
          <div class="t-cat">Week 1-2</div>
          <p class="body-sm" style="margin-top:12px">매출·브랜드 방어 질의 20개 선정</p>
        </div>
        <div class="tl-h-node">
          <div class="t-cat">Week 3-4</div>
          <p class="body-sm" style="margin-top:12px">상위 SEO 페이지 answer-readiness 감사</p>
        </div>
        <div class="tl-h-node">
          <div class="t-cat">Week 5-8</div>
          <p class="body-sm" style="margin-top:12px">답변 블록, FAQ, schema, 근거 패키지 반영</p>
        </div>
        <div class="tl-h-node">
          <div class="t-cat">Week 9-10</div>
          <p class="body-sm" style="margin-top:12px">AI citation과 answer coverage 측정 시작</p>
        </div>
        <div class="tl-h-node">
          <div class="t-cat">Week 11-12</div>
          <p class="body-sm" style="margin-top:12px">오류·누락 케이스를 분기 SEO backlog에 편입</p>
        </div>
      </div>
      <div class="foot">Success signal: visible citation or answer mention in five priority topics.</div>
    </div>
  </section>

  <section class="slide split" data-layout="S10" data-animate="split-statement">
    <div class="canvas-card">
      <div class="half b-accent">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min">
          <div class="l">Decision</div>
          <div class="r">08 / 08</div>
        </div>
        <div style="margin-top:auto">
          <h2 class="h-statement">랭킹만<br>볼 것인가,<br>답변 선택까지<br>볼 것인가.</h2>
        </div>
      </div>
      <div class="half b-paper">
        <div class="chrome-min">
          <div class="l">Next actions</div>
          <div class="r">End</div>
        </div>
        <div style="display:grid;gap:18px;margin:auto 0">
          <div class="card-fill"><div class="t-meta">Keep</div><h3 class="h-md">SEO 기반</h3><p class="body-sm">색인, 기술 SEO, 콘텐츠 품질, 링크 신호는 계속 유지한다.</p></div>
          <div class="card-fill"><div class="t-meta">Add</div><h3 class="h-md">AEO 기준</h3><p class="body-sm">질문별 answer block, entity consistency, citation monitoring을 운영 기준에 추가한다.</p></div>
          <div class="card-fill"><div class="t-meta">Start</div><h3 class="h-md accent-text">상위 50개 페이지 감사</h3><p class="body-sm">기존 SEO 자산에서 AEO 전환 효율이 가장 높은 페이지부터 점검한다.</p></div>
        </div>
      </div>
    </div>
  </section>
`;

const out = template
  .replace('<html lang="en" data-language="en">', '<html lang="ko" data-language="ko">')
  .replace("<title>Required Deck Title</title>", "<title>SEO -> AEO 검색 시대</title>")
  .replace(/  <!-- Replace these sample sections with the final deck\. -->[\s\S]*?<\/section>\n<\/div>/, `  ${slides.trim()}\n</div>`);

fs.writeFileSync(outFile, out, "utf8");
console.log(outFile);
