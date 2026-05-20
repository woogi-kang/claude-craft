const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const sharp = require("sharp");

const baseDir = path.join(__dirname, "future-tightened-variants");
const variants = [
  "v1-balanced-analysis",
  "v2-executive-metrics",
  "v3-framework-workshop",
];

function fileUrl(file) {
  return `file://${file}`;
}

async function makeContactSheet(variantDir, slideCount) {
  const qaDir = path.join(variantDir, "qa");
  const thumbW = 420;
  const thumbH = 236;
  const gap = 18;
  const composites = [];

  for (let i = 0; i < slideCount; i += 1) {
    const file = path.join(qaDir, `slide-${String(i + 1).padStart(2, "0")}.png`);
    const input = await sharp(file).resize(thumbW, thumbH, { fit: "cover" }).png().toBuffer();
    composites.push({
      input,
      left: (i % 2) * (thumbW + gap),
      top: Math.floor(i / 2) * (thumbH + gap),
    });
  }

  const out = path.join(qaDir, "contact-sheet.png");
  await sharp({
    create: {
      width: thumbW * 2 + gap,
      height: thumbH * Math.ceil(slideCount / 2) + gap * (Math.ceil(slideCount / 2) - 1),
      channels: 4,
      background: "#fafaf8",
    },
  }).composite(composites).png().toFile(out);
  return out;
}

async function qaVariant(browser, variant) {
  const variantDir = path.join(baseDir, variant);
  const deckPath = path.join(variantDir, "index.html");
  const qaDir = path.join(variantDir, "qa");
  fs.mkdirSync(qaDir, { recursive: true });

  const page = await browser.newPage({ viewport: { width: 1366, height: 768 }, deviceScaleFactor: 1 });
  await page.goto(fileUrl(deckPath));
  await page.evaluate(() => {
    localStorage.setItem("tightened-slide-low-power", "1");
    document.body.classList.add("low-power");
  });

  const slideCount = await page.locator(".slide").count();
  const slides = [];

  for (let i = 0; i < slideCount; i += 1) {
    await page.evaluate((idx) => {
      const slideNodes = Array.from(document.querySelectorAll(".slide"));
      slideNodes.forEach((slide, slideIdx) => slide.classList.toggle("active", slideIdx === idx));
      const navButtons = Array.from(document.querySelectorAll("#nav button"));
      navButtons.forEach((button, buttonIdx) => button.classList.toggle("active", buttonIdx === idx));
      window.__currentSlideIndex = idx;
    }, i);
    await page.waitForTimeout(100);

    const screenshot = path.join(qaDir, `slide-${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });

    const result = await page.evaluate(() => {
      const active = document.querySelector(".slide.active");
      const width = window.innerWidth;
      const height = window.innerHeight;
      const elements = Array.from(active.querySelectorAll(
        "h1,h2,h3,p,div.t-meta,div.t-cat,div.body,div.body-sm,div.lead,div.ledger-num,div.force-num,div.why-num-bottom,div.num-mega",
      ));
      const offscreen = [];
      const overflow = [];
      const padding = [];
      const wordBreaking = [];
      const navSafeBottom = height - 26;

      for (const el of elements) {
        const label = (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 100);
        if (!label) continue;
        const rect = el.getBoundingClientRect();
        if (rect.width < 1 || rect.height < 1) continue;
        const style = getComputedStyle(el);
        const isHeading = /H[1-3]/.test(el.tagName) || el.classList.contains("h-xl") || el.classList.contains("h-md") || el.classList.contains("h-statement") || el.classList.contains("h-hero");
        const isMeta = el.classList.contains("t-meta") || el.classList.contains("t-cat");
        const isDisplayNumber = el.classList.contains("ledger-num") || el.classList.contains("force-num") || el.classList.contains("why-num-bottom") || el.classList.contains("num-mega");

        if (rect.left < -1 || rect.top < -1 || rect.right > width + 1 || rect.bottom > height + 1) {
          offscreen.push({ label, rect: [rect.left, rect.top, rect.width, rect.height] });
        }

        if (rect.left < 32 || rect.right > width - 32 || rect.top < 30 || rect.bottom > navSafeBottom) {
          if (!isMeta || rect.bottom > navSafeBottom || rect.left < 24 || rect.right > width - 24) {
            padding.push({ label, rect: [rect.left, rect.top, rect.width, rect.height], safe: { left: 32, right: width - 32, bottom: navSafeBottom } });
          }
        }

        const overflowX = el.scrollWidth > el.clientWidth + 2;
        const overflowY = el.scrollHeight > el.clientHeight + (isHeading ? 42 : 2);
        if ((overflowX || overflowY) && !isDisplayNumber) {
          const diff = {
            label,
            tag: el.tagName,
            heading: isHeading,
            scroll: [el.scrollWidth, el.scrollHeight],
            client: [el.clientWidth, el.clientHeight],
          };
          overflow.push(diff);
        }

        const wordBreak = style.wordBreak;
        const overflowWrap = style.overflowWrap;
        if (wordBreak === "break-all" || overflowWrap === "anywhere") {
          wordBreaking.push({ label, reason: `CSS ${wordBreak}/${overflowWrap}` });
        }

        if (isHeading && !el.innerHTML.includes("<br") && /[가-힣]/.test(label)) {
          const lineHeight = Number.parseFloat(style.lineHeight);
          const fontSize = Number.parseFloat(style.fontSize);
          const expectedLine = Number.isFinite(lineHeight) ? lineHeight : fontSize * 1.1;
          if (rect.height > expectedLine * 1.6) {
            wordBreaking.push({ label, reason: "Heading wraps without explicit <br>; check Korean line break manually." });
          }
        }

        if (/[0-9]+%/.test(label) && Number.parseFloat(style.letterSpacing) > 1) {
          wordBreaking.push({ label, reason: "Numeric percent label has wide letter spacing." });
        }
      }

      return {
        layout: active.getAttribute("data-layout"),
        title: active.querySelector("h1,h2,.h-hero,.h-xl,.h-statement")?.textContent?.trim().replace(/\s+/g, " ") || "",
        offscreen,
        overflow,
        padding,
        wordBreaking,
      };
    });

    const failCount = result.offscreen.length + result.padding.length + result.wordBreaking.length + result.overflow.filter((item) => !item.heading).length;
    const warnCount = result.overflow.filter((item) => item.heading).length;
    slides.push({
      slide: i + 1,
      screenshot,
      status: failCount ? "FAIL" : warnCount ? "WARN" : "PASS",
      failCount,
      warnCount,
      ...result,
    });
  }

  await page.close();
  const contactSheet = await makeContactSheet(variantDir, slideCount);
  return { variant, deckPath, qaDir, contactSheet, slideCount, slides };
}

(async () => {
  const browser = await chromium.launch();
  const results = [];
  for (const variant of variants) {
    results.push(await qaVariant(browser, variant));
  }
  await browser.close();

  const report = [
    "# Future Tightened Variants QA",
    "",
    "Viewport: 1366x768",
    "Checks: offscreen, overflow, safe padding, bottom navigation safe area, Korean heading word break, percent label spacing.",
    "",
    "## Summary",
    "",
    "| Variant | Slides | PASS | WARN | FAIL | Contact sheet |",
    "|---|---:|---:|---:|---:|---|",
    ...results.map((r) => {
      const pass = r.slides.filter((s) => s.status === "PASS").length;
      const warn = r.slides.filter((s) => s.status === "WARN").length;
      const fail = r.slides.filter((s) => s.status === "FAIL").length;
      return `| ${r.variant} | ${r.slideCount} | ${pass} | ${warn} | ${fail} | ${r.contactSheet} |`;
    }),
    "",
    "## Details",
    "",
    results.map((r) => [
      `### ${r.variant}`,
      "",
      `Deck: ${r.deckPath}`,
      `Contact sheet: ${r.contactSheet}`,
      "",
      r.slides.map((s) => [
        `#### Slide ${String(s.slide).padStart(2, "0")} / ${s.layout} / ${s.status}`,
        "",
        `Title: ${s.title}`,
        `Screenshot: ${s.screenshot}`,
        `Offscreen: ${s.offscreen.length}`,
        `Overflow: ${s.overflow.length}`,
        `Padding safe-area: ${s.padding.length}`,
        `Word breaking: ${s.wordBreaking.length}`,
        s.offscreen.length ? `Offscreen detail:\n\`\`\`json\n${JSON.stringify(s.offscreen, null, 2)}\n\`\`\`` : "",
        s.overflow.length ? `Overflow detail:\n\`\`\`json\n${JSON.stringify(s.overflow, null, 2)}\n\`\`\`` : "",
        s.padding.length ? `Padding detail:\n\`\`\`json\n${JSON.stringify(s.padding, null, 2)}\n\`\`\`` : "",
        s.wordBreaking.length ? `Word breaking detail:\n\`\`\`json\n${JSON.stringify(s.wordBreaking, null, 2)}\n\`\`\`` : "",
        "",
      ].filter(Boolean).join("\n")).join("\n"),
    ].join("\n")).join("\n"),
  ].join("\n");

  const reportPath = path.join(baseDir, "qa-summary.md");
  fs.writeFileSync(reportPath, report, "utf8");
  console.log(reportPath);
})();
