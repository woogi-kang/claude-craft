import { chromium } from 'playwright';
import { readdir } from 'fs/promises';
import path from 'path';
import { PDFDocument } from 'pdf-lib';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function buildPdf() {
  console.log('Building Claude Code Team Guide PDF...');

  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 960, height: 540 }
  });

  // Get all slide files
  const slidesDir = path.join(__dirname, 'slides');
  const files = await readdir(slidesDir);
  const slideFiles = files
    .filter(f => f.startsWith('slide-') && f.endsWith('.html'))
    .sort((a, b) => {
      const numA = parseInt(a.match(/slide-(\d+)/)[1]);
      const numB = parseInt(b.match(/slide-(\d+)/)[1]);
      return numA - numB;
    });

  console.log(`Found ${slideFiles.length} slides`);

  // Create merged PDF
  const mergedPdf = await PDFDocument.create();

  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    const fileUrl = `file://${filePath}`;

    console.log(`Processing: ${file}`);

    const page = await context.newPage();
    await page.goto(fileUrl, { waitUntil: 'networkidle' });

    // Wait a bit for fonts to load
    await page.waitForTimeout(500);

    // Generate PDF for this slide
    const pdfBuffer = await page.pdf({
      width: '960px',
      height: '540px',
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }
    });

    // Add to merged PDF
    const slidePdf = await PDFDocument.load(pdfBuffer);
    const [copiedPage] = await mergedPdf.copyPages(slidePdf, [0]);
    mergedPdf.addPage(copiedPage);

    await page.close();
  }

  // Save merged PDF
  const outputFile = 'Claude_Code_Team_Guide.pdf';
  const pdfBytes = await mergedPdf.save();

  const fs = await import('fs/promises');
  await fs.writeFile(outputFile, pdfBytes);

  await browser.close();

  console.log(`\nCreated: ${outputFile}`);
}

buildPdf().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
