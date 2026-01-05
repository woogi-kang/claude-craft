import sharp from 'sharp';
import path from 'path';

const WIDTH = 960;
const HEIGHT = 540;

// Generate gradient background as SVG then convert to PNG
async function generateGradient(name, colors, angle = 135) {
  const radians = (angle - 90) * (Math.PI / 180);
  const x1 = 50 - Math.cos(radians) * 50;
  const y1 = 50 - Math.sin(radians) * 50;
  const x2 = 50 + Math.cos(radians) * 50;
  const y2 = 50 + Math.sin(radians) * 50;

  const stops = colors.map((c, i) => {
    const offset = (i / (colors.length - 1)) * 100;
    return `<stop offset="${offset}%" stop-color="${c}"/>`;
  }).join('');

  const svg = `
    <svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad" x1="${x1}%" y1="${y1}%" x2="${x2}%" y2="${y2}%">
          ${stops}
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#grad)"/>
    </svg>
  `;

  const outputPath = path.join('design-system/backgrounds', `${name}.png`);
  await sharp(Buffer.from(svg)).png().toFile(outputPath);
  console.log(`Created: ${outputPath}`);
}

// Generate solid color background
async function generateSolid(name, color) {
  const svg = `
    <svg width="${WIDTH}" height="${HEIGHT}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="${color}"/>
    </svg>
  `;

  const outputPath = path.join('design-system/backgrounds', `${name}.png`);
  await sharp(Buffer.from(svg)).png().toFile(outputPath);
  console.log(`Created: ${outputPath}`);
}

async function main() {
  console.log('Generating background images...\n');

  // Primary gradient (purple) - for cover slides
  await generateGradient('gradient-primary', ['#667eea', '#764ba2'], 135);

  // Dark gradient - for section dividers
  await generateGradient('gradient-dark', ['#1a1a2e', '#16213e'], 135);

  // Light background
  await generateSolid('light', '#f5f5f0');

  // White background
  await generateSolid('white', '#ffffff');

  // Dark background
  await generateSolid('dark', '#0f0f23');

  // Accent gradient
  await generateGradient('gradient-accent', ['#667eea', '#f093fb'], 135);

  console.log('\nDone!');
}

main().catch(console.error);
