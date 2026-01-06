import PptxGenJS from 'pptxgenjs';
import { chromium } from 'playwright';
import { readdir, writeFile } from 'fs/promises';
import path from 'path';
import { PDFDocument } from 'pdf-lib';
import { fileURLToPath } from 'url';
import html2pptx from './html2pptx.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function buildAll(projectName = 'Presentation') {
  const slidesDir = path.join(__dirname, 'slides');
  const files = await readdir(slidesDir);
  const slideFiles = files
    .filter(f => f.startsWith('slide-') && f.endsWith('.html'))
    .sort((a, b) => {
      const numA = parseInt(a.match(/slide-(\d+)/)[1]);
      const numB = parseInt(b.match(/slide-(\d+)/)[1]);
      return numA - numB;
    });

  console.log(`Found ${slideFiles.length} slides\n`);

  // ═══════════════════════════════════════════════════════════
  // PPTX 생성
  // ═══════════════════════════════════════════════════════════
  console.log('═'.repeat(50));
  console.log('Building PPTX...');
  console.log('═'.repeat(50));

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';
  pres.title = projectName;

  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    console.log(`[PPTX] Processing: ${file}`);
    await html2pptx(filePath, pres);
  }

  const pptxFile = `${projectName.replace(/\s+/g, '_')}.pptx`;
  await pres.writeFile({ fileName: pptxFile });
  console.log(`\nCreated: ${pptxFile}\n`);

  // ═══════════════════════════════════════════════════════════
  // PDF 생성
  // ═══════════════════════════════════════════════════════════
  console.log('═'.repeat(50));
  console.log('Building PDF...');
  console.log('═'.repeat(50));

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 960, height: 540 }
  });

  const mergedPdf = await PDFDocument.create();

  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    const fileUrl = `file://${filePath}`;

    console.log(`[PDF] Processing: ${file}`);

    const page = await context.newPage();
    await page.goto(fileUrl, { waitUntil: 'networkidle' });
    await page.waitForTimeout(500);

    const pdfBuffer = await page.pdf({
      width: '960px',
      height: '540px',
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });

    const slidePdf = await PDFDocument.load(pdfBuffer);
    const [copiedPage] = await mergedPdf.copyPages(slidePdf, [0]);
    mergedPdf.addPage(copiedPage);

    await page.close();
  }

  const pdfFile = `${projectName.replace(/\s+/g, '_')}.pdf`;
  const pdfBytes = await mergedPdf.save();
  await writeFile(pdfFile, pdfBytes);

  await browser.close();
  console.log(`\nCreated: ${pdfFile}\n`);

  // ═══════════════════════════════════════════════════════════
  // 완료 리포트
  // ═══════════════════════════════════════════════════════════
  console.log('═'.repeat(50));
  console.log('BUILD COMPLETE');
  console.log('═'.repeat(50));
  console.log(`
  Project: ${projectName}
  Slides:  ${slideFiles.length}

  Output Files:
  ├── ${pptxFile}
  └── ${pdfFile}
  `);

  return { pptxFile, pdfFile };
}

export default buildAll;

// CLI execution
const projectName = process.argv[2] || 'Claude_Code_Team_Guide';
buildAll(projectName).catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
