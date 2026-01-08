import PptxGenJS from 'pptxgenjs';
import { chromium } from 'playwright';
import { readdir } from 'fs/promises';
import path from 'path';
import { PDFDocument } from 'pdf-lib';
import { fileURLToPath } from 'url';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_NAME = 'LLM_프롬프트_작성의_기술';

// AI Futuristic Theme Colors (no # prefix for pptxgenjs)
const COLORS = {
  bgPrimary: '0a0a0f',
  bgSecondary: '12121a',
  bgCard: '1a1a25',
  bgCode: '0d0d12',
  textPrimary: 'e8e8ec',
  textSecondary: '888898',
  textMuted: '585868',
  accentPrimary: '667eea',
  accentSecondary: '00d9ff',
  accentTertiary: 'a855f7',
  accentSuccess: '4ade80',
  badRed: 'ef4444',
  goodGreen: '22c55e'
};

// Slide data
const slides = [
  { type: 'cover', title: 'LLM 프롬프트 작성의 기술', subtitle: 'Claude Code와 AI를 200% 활용하는 프롬프팅 가이드' },
  { type: 'contents', title: 'Contents', items: ['01 프롬프트 엔지니어링이란?', '02 7가지 핵심 원칙', '03 실전 프롬프트 예시', '04 핵심 요약'] },
  { type: 'section', number: '01', title: '프롬프트 엔지니어링이란?', subtitle: 'AI와 효과적으로 대화하는 방법' },
  { type: 'content', title: '프롬프트 = AI와의 대화 언어', bullets: ['프롬프트 품질이 AI 응답의 정확성, 관련성, 일관성을 결정', 'Claude 4.x는 이전 버전보다 지시를 더 정확히 따름', '말 그대로 실행하므로 구체적인 지시가 필수'], highlight: '모호한 지시는 모호한 결과를 낳는다' },
  { type: 'section', number: '02', title: '7가지 핵심 원칙', subtitle: '프롬프트 엔지니어링의 본질' },
  { type: 'comparison', title: '원칙 1: 명확하고 구체적으로', bad: '코드 작성해줘', good: '사용자 인증을 처리하는\nPython 함수를\nJWT 토큰 방식으로 작성해줘' },
  { type: 'comparison', title: '원칙 2: 맥락과 이유 설명', bad: '줄임표 사용 금지', good: 'TTS 엔진이 읽을 것이므로\n줄임표 사용 금지' },
  { type: 'content', title: '원칙 3: 예시로 보여주기 (Few-shot)', bullets: ['1-3개의 예시를 제공하면 원하는 출력 형식을 정확히 전달', '모델이 패턴을 학습하여 정확도가 크게 향상', 'JSON, 코드, 문서 형식 등 모든 출력에 적용 가능'] },
  { type: 'content', title: '원칙 4: 생각의 사슬 (Chain-of-Thought)', bullets: ['"단계별로 생각해봐" 한 줄 추가로 정확도 향상', 'Extended Thinking 활성화 시 복잡한 추론 성능 대폭 향상', '수학, 논리, 코드 디버깅 등에 효과적'], highlight: '"단계별로 생각해줘" 한 줄 추가로 정확도 대폭 향상' },
  { type: 'code', title: '원칙 5: XML 태그로 구조화', code: '<context>\n현재 프로젝트는 React + TypeScript 기반입니다.\n</context>\n\n<task>\n로그인 컴포넌트를 만들어주세요.\n</task>\n\n<format>\nTypeScript로 작성해주세요.\n</format>' },
  { type: 'content', title: '원칙 6: 역할 부여하기', bullets: ['전문가 역할을 부여하면 해당 관점에서 더 전문적인 답변', '"당신은 10년 경력의 시니어 개발자입니다" - 품질 향상', 'Role-Context-Task 3계층 구조로 명확한 역할 정의'] },
  { type: 'content', title: '원칙 7: 반복해서 개선하기', bullets: ['첫 시도에 완벽한 프롬프트를 기대하지 않기', '작은 단어 변경도 결과에 큰 영향', '테스트 → 조정 → 재테스트 사이클 반복'], highlight: '프롬프트는 한 번에 완성되지 않는다' },
  { type: 'section', number: '03', title: '실전 프롬프트 예시', subtitle: '개발팀 · 영업팀 · 기획팀 맞춤 활용법' },
  { type: 'content', title: '개발팀: 코드리뷰 · 디버깅 · 리팩토링', bullets: ['[코드리뷰] "시니어 개발자로서 보안 취약점, 성능 이슈, 컨벤션 관점에서 우선순위별 정리"', '[디버깅] "단계별로 원인 분석: 에러 위치 → 근본 원인 → 해결 방법 → 예방책"', '[리팩토링] "SOLID 원칙 위반 지적 + Before/After 비교 + 변경 이유 설명"'], highlight: '역할 부여 + 단계별 분석 + 구체적 관점 요청' },
  { type: 'content', title: '영업/마케팅팀: 이메일 · 제안서 · 고객분석', bullets: ['[콜드메일] "B2B 전문가로서 150자 이내, pain point → 핵심가치 → 데모 제안"', '[경쟁분석] "기능/가격/타겟 관점 비교표 + 차별화 포인트 3가지 + 영업 멘트"', '[리뷰대응] "친근하지만 전문적 톤으로 공감 → 책임 → 해결 → 긍정 마무리"'], highlight: '제약조건(길이/형식) + 구조화된 출력 요청' },
  { type: 'content', title: '기획/경영지원: 보고서 · 회의록 · 분석', bullets: ['[회의록] "결정사항/논의사항/Action Item 구분, 담당자·마감일 명시"', '[SWOT] "단계별로 생각하며 항목 5개씩 도출 → SO/ST/WO/WT 전략 → 액션"', '[데이터분석] "Let\'s think step by step. 트렌드 → 이상치 → 가설 → 인사이트 3개"'], highlight: 'Chain of Thought로 체계적 분석 유도' },
  { type: 'summary', title: '핵심 요약: 검증된 5가지 기법', items: [{ num: '01', title: 'XML 태그', desc: '구조화된 프롬프트' }, { num: '02', title: 'Extended Thinking', desc: '충분한 생각 시간' }, { num: '03', title: '명확한 지시', desc: '구체적으로 요청' }, { num: '04', title: 'Few-shot 예시', desc: '예시 함께 제공' }, { num: '05', title: '컨텍스트 배치', desc: '배경 정보 먼저' }] },
  { type: 'closing', message: '구체적일수록 정확하다', bullets: ['명확하고 구체적으로 지시하기', '예시와 컨텍스트로 맥락 제공하기', 'XML 태그로 구조화하고 반복해서 개선하기'], cta: '오늘부터 실천해보세요!' }
];

async function buildPptx() {
  console.log('═'.repeat(50));
  console.log('Building PPTX...');
  console.log('═'.repeat(50));

  const pptx = new PptxGenJS();
  pptx.layout = 'LAYOUT_16x9';
  pptx.title = PROJECT_NAME;
  pptx.author = 'Claude Code PPT Agent';

  const totalSlides = slides.length;

  slides.forEach((data, idx) => {
    const slideNum = idx + 1;
    console.log(`[PPTX] Creating slide ${slideNum}/${totalSlides}: ${data.type}`);

    const slide = pptx.addSlide();
    slide.background = { color: COLORS.bgPrimary };

    switch(data.type) {
      case 'cover':
        slide.addText(data.title, { x: 0.5, y: 2.2, w: 12.33, h: 1.2, fontSize: 54, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true, align: 'center' });
        slide.addShape('rect', { x: 4, y: 3.5, w: 5.33, h: 0.05, fill: { color: COLORS.accentPrimary } });
        slide.addText(data.subtitle, { x: 0.5, y: 3.7, w: 12.33, h: 0.6, fontSize: 22, fontFace: 'Pretendard', color: COLORS.accentSecondary, align: 'center' });
        break;

      case 'contents':
        slide.addText(data.title, { x: 0.7, y: 0.5, w: 11.93, h: 0.8, fontSize: 36, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        data.items.forEach((item, i) => {
          const y = 1.8 + (i * 1.1);
          slide.addShape('rect', { x: 0.7, y: y, w: 0.7, h: 0.7, fill: { color: COLORS.bgCard }, line: { color: COLORS.accentPrimary, width: 1 } });
          slide.addText(`0${i+1}`, { x: 0.7, y: y, w: 0.7, h: 0.7, fontSize: 18, fontFace: 'Pretendard', color: COLORS.accentPrimary, bold: true, align: 'center', valign: 'middle' });
          slide.addText(item, { x: 1.6, y: y, w: 10.5, h: 0.7, fontSize: 22, fontFace: 'Pretendard', color: COLORS.textPrimary, valign: 'middle' });
        });
        break;

      case 'section':
        slide.addText(data.number, { x: 0.7, y: 1.8, w: 2, h: 1.2, fontSize: 80, fontFace: 'Pretendard', color: COLORS.accentPrimary, bold: true });
        slide.addShape('rect', { x: 0.7, y: 3.1, w: 4, h: 0.05, fill: { color: COLORS.accentPrimary } });
        slide.addText(data.title, { x: 0.7, y: 3.4, w: 11.93, h: 0.9, fontSize: 42, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        slide.addText(data.subtitle, { x: 0.7, y: 4.4, w: 11.93, h: 0.5, fontSize: 18, fontFace: 'Pretendard', color: COLORS.textSecondary });
        break;

      case 'content':
        slide.addText(data.title, { x: 0.7, y: 0.5, w: 11.93, h: 0.8, fontSize: 32, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        let bulletY = 1.5;
        data.bullets.forEach(bullet => {
          slide.addShape('ellipse', { x: 0.9, y: bulletY + 0.12, w: 0.12, h: 0.12, fill: { color: COLORS.accentSecondary } });
          slide.addText(bullet, { x: 1.2, y: bulletY, w: 11, h: 0.7, fontSize: 18, fontFace: 'Pretendard', color: COLORS.textPrimary });
          bulletY += 0.85;
        });
        if (data.highlight) {
          slide.addShape('rect', { x: 0.7, y: 5.2, w: 11.93, h: 0.9, fill: { color: COLORS.bgCard }, line: { color: COLORS.accentPrimary, width: 2 } });
          slide.addText(data.highlight, { x: 0.7, y: 5.2, w: 11.93, h: 0.9, fontSize: 20, fontFace: 'Pretendard', color: COLORS.accentSecondary, bold: true, align: 'center', valign: 'middle' });
        }
        break;

      case 'comparison':
        slide.addText(data.title, { x: 0.7, y: 0.5, w: 11.93, h: 0.8, fontSize: 32, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        // Bad box
        slide.addShape('rect', { x: 0.7, y: 1.6, w: 5.3, h: 3.2, fill: { color: COLORS.bgCard }, line: { color: COLORS.badRed, width: 2 } });
        slide.addText('Bad', { x: 0.7, y: 1.6, w: 5.3, h: 0.5, fontSize: 16, fontFace: 'Pretendard', color: COLORS.badRed, bold: true, align: 'center' });
        slide.addText(data.bad, { x: 1, y: 2.3, w: 4.7, h: 2.2, fontSize: 16, fontFace: 'Consolas', color: COLORS.textSecondary });
        // Good box
        slide.addShape('rect', { x: 6.33, y: 1.6, w: 5.3, h: 3.2, fill: { color: COLORS.bgCard }, line: { color: COLORS.goodGreen, width: 2 } });
        slide.addText('Good', { x: 6.33, y: 1.6, w: 5.3, h: 0.5, fontSize: 16, fontFace: 'Pretendard', color: COLORS.goodGreen, bold: true, align: 'center' });
        slide.addText(data.good, { x: 6.63, y: 2.3, w: 4.7, h: 2.2, fontSize: 16, fontFace: 'Consolas', color: COLORS.accentSuccess });
        // Arrow
        slide.addText('→', { x: 5.5, y: 2.8, w: 1.2, h: 0.8, fontSize: 36, color: COLORS.accentPrimary, align: 'center', valign: 'middle' });
        break;

      case 'code':
        slide.addText(data.title, { x: 0.7, y: 0.5, w: 11.93, h: 0.8, fontSize: 32, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        slide.addShape('rect', { x: 0.7, y: 1.5, w: 11.93, h: 4.2, fill: { color: COLORS.bgCode }, line: { color: COLORS.accentPrimary, width: 1, transparency: 70 } });
        slide.addShape('rect', { x: 0.7, y: 1.5, w: 11.93, h: 0.4, fill: { color: COLORS.bgCard } });
        slide.addShape('ellipse', { x: 1, y: 1.62, w: 0.15, h: 0.15, fill: { color: COLORS.badRed } });
        slide.addShape('ellipse', { x: 1.25, y: 1.62, w: 0.15, h: 0.15, fill: { color: 'fbbf24' } });
        slide.addShape('ellipse', { x: 1.5, y: 1.62, w: 0.15, h: 0.15, fill: { color: COLORS.goodGreen } });
        slide.addText(data.code, { x: 1, y: 2.1, w: 11.33, h: 3.4, fontSize: 15, fontFace: 'Consolas', color: COLORS.accentSuccess });
        break;

      case 'summary':
        slide.addText(data.title, { x: 0.7, y: 0.5, w: 11.93, h: 0.8, fontSize: 32, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true });
        const itemWidth = 2.1;
        data.items.forEach((item, i) => {
          const x = 0.7 + (i * (itemWidth + 0.2));
          slide.addShape('rect', { x: x, y: 1.5, w: itemWidth, h: 4, fill: { color: COLORS.bgCard }, line: { color: COLORS.accentPrimary, width: 1 } });
          slide.addText(item.num, { x: x, y: 1.7, w: itemWidth, h: 0.7, fontSize: 28, fontFace: 'Pretendard', color: COLORS.accentPrimary, bold: true, align: 'center' });
          slide.addText(item.title, { x: x + 0.1, y: 2.5, w: itemWidth - 0.2, h: 0.8, fontSize: 14, fontFace: 'Pretendard', color: COLORS.textPrimary, bold: true, align: 'center' });
          slide.addText(item.desc, { x: x + 0.1, y: 3.4, w: itemWidth - 0.2, h: 1.5, fontSize: 11, fontFace: 'Pretendard', color: COLORS.textSecondary, align: 'center' });
        });
        break;

      case 'closing':
        slide.addText(data.message, { x: 0.5, y: 1.5, w: 12.33, h: 1, fontSize: 44, fontFace: 'Pretendard', color: COLORS.accentSecondary, bold: true, align: 'center' });
        let closingY = 2.8;
        data.bullets.forEach(bullet => {
          slide.addText('✓  ' + bullet, { x: 2.5, y: closingY, w: 8.33, h: 0.5, fontSize: 18, fontFace: 'Pretendard', color: COLORS.textPrimary });
          closingY += 0.6;
        });
        slide.addShape('rect', { x: 3.5, y: 5, w: 6.33, h: 0.7, fill: { color: COLORS.accentPrimary } });
        slide.addText(data.cta, { x: 3.5, y: 5, w: 6.33, h: 0.7, fontSize: 18, fontFace: 'Pretendard', color: COLORS.bgPrimary, bold: true, align: 'center', valign: 'middle' });
        break;
    }

    // Add slide number
    if (data.type !== 'cover') {
      slide.addText(`${slideNum} / ${totalSlides}`, { x: 11.5, y: 6.8, w: 1, h: 0.3, fontSize: 10, color: COLORS.textMuted, align: 'right' });
    }
  });

  const pptxFile = `${PROJECT_NAME}.pptx`;
  await pptx.writeFile({ fileName: pptxFile });
  console.log(`\nCreated: ${pptxFile}\n`);
  return pptxFile;
}

async function buildPdf() {
  console.log('═'.repeat(50));
  console.log('Building PDF...');
  console.log('═'.repeat(50));

  const slidesDir = path.join(__dirname, 'slides');
  const files = await readdir(slidesDir);
  const slideFiles = files
    .filter(f => f.startsWith('slide-') && f.endsWith('.html'))
    .sort((a, b) => {
      const numA = parseInt(a.match(/slide-(\d+)/)[1]);
      const numB = parseInt(b.match(/slide-(\d+)/)[1]);
      return numA - numB;
    });

  console.log(`Found ${slideFiles.length} HTML slides\n`);

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

  const pdfFile = `${PROJECT_NAME}.pdf`;
  const pdfBytes = await mergedPdf.save();
  await fs.writeFile(pdfFile, pdfBytes);

  await browser.close();
  console.log(`\nCreated: ${pdfFile}\n`);
  return pdfFile;
}

async function buildAll() {
  console.log('\n' + '═'.repeat(50));
  console.log('PPT Agent - Build All');
  console.log('═'.repeat(50) + '\n');
  console.log(`Project: ${PROJECT_NAME}`);
  console.log(`Total slides: ${slides.length}\n`);

  const pptxFile = await buildPptx();
  const pdfFile = await buildPdf();

  console.log('═'.repeat(50));
  console.log('BUILD COMPLETE');
  console.log('═'.repeat(50));
  console.log(`
  Project: ${PROJECT_NAME}
  Slides:  ${slides.length}

  Output Files:
  ├── ${pptxFile}
  └── ${pdfFile}
  `);
}

buildAll().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
