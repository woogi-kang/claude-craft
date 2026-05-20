const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");

const deckPath = path.join(__dirname, "future-tightened", "index.html");
const outDir = path.join(__dirname, "future-tightened", "qa");
fs.mkdirSync(outDir, { recursive: true });

function fileUrl(file) {
  return `file://${file}`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1366, height: 768 }, deviceScaleFactor: 1 });
  await page.goto(fileUrl(deckPath));
  await page.evaluate(() => {
    localStorage.setItem("tightened-slide-low-power", "1");
    document.body.classList.add("low-power");
  });

  const slideCount = await page.locator(".slide").count();
  const results = [];

  for (let i = 0; i < slideCount; i += 1) {
    await page.evaluate((idx) => {
      const slides = Array.from(document.querySelectorAll(".slide"));
      slides.forEach((slide, slideIdx) => slide.classList.toggle("active", slideIdx === idx));
      window.__currentSlideIndex = idx;
      const navButtons = Array.from(document.querySelectorAll("#nav button"));
      navButtons.forEach((button, buttonIdx) => button.classList.toggle("active", buttonIdx === idx));
    }, i);
    await page.waitForTimeout(120);
    const screenshot = path.join(outDir, `slide-${String(i + 1).padStart(2, "0")}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });

    const qa = await page.evaluate(() => {
      const active = document.querySelector(".slide.active");
      const width = window.innerWidth;
      const height = window.innerHeight;
      const inspected = Array.from(active.querySelectorAll("h1,h2,h3,p,div.t-meta,div.t-cat,div.body,div.body-sm,div.lead,div.ledger-num"));
      const offscreen = [];
      const overflow = [];
      for (const el of inspected) {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        const label = (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80);
        if (!label || rect.width === 0 || rect.height === 0) continue;
        if (rect.left < -1 || rect.top < -1 || rect.right > width + 1 || rect.bottom > height + 1) {
          offscreen.push({ label, rect: [rect.left, rect.top, rect.width, rect.height] });
        }
        if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
          overflow.push({ label, scroll: [el.scrollWidth, el.scrollHeight], client: [el.clientWidth, el.clientHeight] });
        }
        if (Number.parseFloat(style.fontSize) < 10) {
          overflow.push({ label: `tiny:${label}`, fontSize: style.fontSize });
        }
      }
      return {
        layout: active.getAttribute("data-layout"),
        title: active.querySelector("h1,h2,.h-hero,.h-xl,.h-statement")?.textContent?.trim().replace(/\s+/g, " ") || "",
        offscreen,
        overflow,
      };
    });
    results.push({ slide: i + 1, screenshot, ...qa });
  }

  await browser.close();

  const report = [
    "# Future Tightened Deck QA",
    "",
    `Deck: ${deckPath}`,
    `Viewport: 1366x768`,
    `Slides: ${slideCount}`,
    "",
    "## Results",
    "",
    results.map((r) => [
      `### Slide ${String(r.slide).padStart(2, "0")} / ${r.layout}`,
      "",
      `Title: ${r.title}`,
      `Screenshot: ${r.screenshot}`,
      `Offscreen elements: ${r.offscreen.length}`,
      `Overflow or tiny text warnings: ${r.overflow.length}`,
      r.offscreen.length ? `Offscreen detail:\n\`\`\`json\n${JSON.stringify(r.offscreen, null, 2)}\n\`\`\`` : "",
      r.overflow.length ? `Warning detail:\n\`\`\`json\n${JSON.stringify(r.overflow, null, 2)}\n\`\`\`` : "",
      "",
    ].filter(Boolean).join("\n")).join("\n"),
  ].join("\n");

  const reportPath = path.join(outDir, "qa-report.md");
  fs.writeFileSync(reportPath, report, "utf8");
  console.log(reportPath);
})();
