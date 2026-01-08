import PptxGenJS from 'pptxgenjs';
import html2pptx from './html2pptx.js';
import { readdir } from 'fs/promises';
import path from 'path';

async function build() {
  console.log('Building Claude Code Team Guide PPTX...');

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_16x9';
  pres.title = 'Claude Code Team Guide';
  pres.author = 'Development Team';

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
  const outputFile = 'Claude_Code_Team_Guide.pptx';
  await pres.writeFile({ fileName: outputFile });
  console.log(`\nCreated: ${outputFile}`);
}

build().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
