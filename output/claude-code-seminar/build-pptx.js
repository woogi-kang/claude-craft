import PptxGenJS from 'pptxgenjs';
import html2pptx from './html2pptx.js';
import { readdir } from 'fs/promises';
import path from 'path';

async function build() {
  console.log('Building Claude Code 2.0 Seminar PPTX...');

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9'; // 10" x 5.625" = 720pt x 405pt
  pres.title = 'Claude Code 2.0 Seminar';
  pres.author = 'Anthropic';

  // Get all slide files
  const slidesDir = './slides';
  const files = await readdir(slidesDir);
  const slideFiles = files
    .filter(f => f.startsWith('slide-') && f.endsWith('.html'))
    .sort();

  console.log(`Found ${slideFiles.length} slides`);

  // Convert each slide
  for (const file of slideFiles) {
    const filePath = path.join(slidesDir, file);
    console.log(`Processing: ${file}`);
    try {
      await html2pptx(filePath, pres);
    } catch (error) {
      console.error(`Error processing ${file}:`, error.message);
      throw error;
    }
  }

  // Save the presentation
  const outputFile = 'Claude_Code_2.0_Seminar.pptx';
  await pres.writeFile({ fileName: outputFile });
  console.log(`\nCreated: ${outputFile}`);
}

build().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
