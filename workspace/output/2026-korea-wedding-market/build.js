import html2pptx from './html2pptx.js';
import PptxGenJS from 'pptxgenjs';
import { chromium } from 'playwright';
import { PDFDocument } from 'pdf-lib';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function build() {
  const pptx = new PptxGenJS();

  // 16:9 layout
  pptx.defineLayout({ name: 'CUSTOM', width: 10, height: 5.625 });
  pptx.layout = 'CUSTOM';

  pptx.title = '2026 대한민국 결혼 시장';
  pptx.author = 'Wedding Market Research';
  pptx.subject = '2026 Korea Wedding Market Analysis';

  const slidesDir = path.join(__dirname, 'slides');
  const slideFiles = fs.readdirSync(slidesDir)
    .filter(f => f.endsWith('.html'))
    .sort();

  console.log(`Found ${slideFiles.length} slides`);

  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    console.log(`Processing: ${file}`);

    try {
      const { slide, placeholders } = await html2pptx(filePath, pptx);
      console.log(`  ✓ Converted successfully`);
      if (placeholders.length > 0) {
        console.log(`  Placeholders: ${placeholders.map(p => p.id).join(', ')}`);
      }
    } catch (error) {
      console.error(`  ✗ Error: ${error.message}`);
    }
  }

  const outputPath = path.join(__dirname, '2026-korea-wedding-market.pptx');
  await pptx.writeFile({ fileName: outputPath });
  console.log(`\n✓ PPTX saved to: ${outputPath}`);

  // PDF Export
  console.log('\n--- PDF Export ---');
  await exportPDF(slideFiles, slidesDir);
}

async function exportPDF(slideFiles, slidesDir) {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 960, height: 540 }
  });

  const mergedPdf = await PDFDocument.create();

  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    console.log(`Rendering PDF: ${file}`);

    try {
      const page = await context.newPage();
      await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });

      const pdfBuffer = await page.pdf({
        width: '960px',
        height: '540px',
        printBackground: true,
        pageRanges: '1'
      });

      const tempPdf = await PDFDocument.load(pdfBuffer);
      const [copiedPage] = await mergedPdf.copyPages(tempPdf, [0]);
      mergedPdf.addPage(copiedPage);

      await page.close();
      console.log(`  ✓ Done`);
    } catch (error) {
      console.error(`  ✗ Error: ${error.message}`);
    }
  }

  await browser.close();

  const pdfBytes = await mergedPdf.save();
  const pdfOutputPath = path.join(__dirname, '2026-korea-wedding-market.pdf');
  fs.writeFileSync(pdfOutputPath, pdfBytes);
  console.log(`\n✓ PDF saved to: ${pdfOutputPath}`);
}

build().catch(console.error);
