# Visual Test Skill

시각적 회귀 테스트와 Storybook을 설정합니다.

## Triggers

- "비주얼 테스트", "visual test", "스토리북", "storybook", "스냅샷"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `components` | ✅ | 테스트할 컴포넌트 |
| `viewports` | ❌ | 테스트 뷰포트 (desktop, tablet, mobile) |

---

## Playwright Visual Testing

### Snapshot 테스트

```typescript
// e2e/visual/components.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage should match snapshot', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });

  test('dashboard should match snapshot', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveScreenshot('dashboard.png', {
      animations: 'disabled',
    });
  });

  test('login form should match snapshot', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByRole('form')).toHaveScreenshot('login-form.png');
  });
});
```

### 반응형 테스트

```typescript
// e2e/visual/responsive.spec.ts
import { test, expect, devices } from '@playwright/test';

const viewports = [
  { name: 'desktop', viewport: { width: 1920, height: 1080 } },
  { name: 'tablet', viewport: { width: 768, height: 1024 } },
  { name: 'mobile', viewport: devices['iPhone 13'].viewport },
];

test.describe('Responsive Visual Tests', () => {
  for (const { name, viewport } of viewports) {
    test(`dashboard on ${name}`, async ({ page }) => {
      await page.setViewportSize(viewport);
      await page.goto('/dashboard');
      await page.waitForLoadState('networkidle');

      await expect(page).toHaveScreenshot(`dashboard-${name}.png`, {
        animations: 'disabled',
      });
    });
  }
});
```

### 컴포넌트별 스냅샷

```typescript
// e2e/visual/button.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button Visual Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/storybook-static/iframe.html?id=components-button--default');
  });

  test('default button', async ({ page }) => {
    await expect(page.locator('button')).toHaveScreenshot('button-default.png');
  });

  test('hover state', async ({ page }) => {
    const button = page.locator('button');
    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');
  });

  test('focus state', async ({ page }) => {
    const button = page.locator('button');
    await button.focus();
    await expect(button).toHaveScreenshot('button-focus.png');
  });

  test('disabled state', async ({ page }) => {
    await page.goto('/storybook-static/iframe.html?id=components-button--disabled');
    await expect(page.locator('button')).toHaveScreenshot('button-disabled.png');
  });
});
```

---

## Storybook 설정

### 설치

```bash
npx storybook@latest init
npm install -D @storybook/addon-a11y @storybook/test
```

### 설정 파일

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/nextjs';

const config: StorybookConfig = {
  stories: [
    '../components/**/*.stories.@(ts|tsx)',
    '../features/**/*.stories.@(ts|tsx)',
  ],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/nextjs',
    options: {},
  },
  staticDirs: ['../public'],
};

export default config;
```

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { ThemeProvider } from 'next-themes';
import '../app/globals.css';

const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    nextjs: {
      appDirectory: true,
    },
  },
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light">
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        icon: 'paintbrush',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
};

export default preview;
```

---

## Story 작성

### Button Story

```typescript
// components/ui/button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { fn } from '@storybook/test';
import { Button } from './button';
import { Mail, Loader2 } from 'lucide-react';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
    },
  },
  args: { onClick: fn() },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: {
    children: 'Button',
  },
};

export const Destructive: Story = {
  args: {
    variant: 'destructive',
    children: '삭제',
  },
};

export const Outline: Story = {
  args: {
    variant: 'outline',
    children: 'Outline',
  },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <Mail className="mr-2 h-4 w-4" />
        이메일 보내기
      </>
    ),
  },
};

export const Loading: Story = {
  args: {
    disabled: true,
    children: (
      <>
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        처리 중...
      </>
    ),
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
};

export const AllSizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};
```

### Card Story

```typescript
// components/ui/card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from './card';
import { Button } from './button';

const meta: Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Card>;

export const Default: Story = {
  render: () => (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>카드 제목</CardTitle>
        <CardDescription>카드 설명입니다.</CardDescription>
      </CardHeader>
      <CardContent>
        <p>카드 내용이 여기에 표시됩니다.</p>
      </CardContent>
      <CardFooter className="flex justify-between">
        <Button variant="outline">취소</Button>
        <Button>확인</Button>
      </CardFooter>
    </Card>
  ),
};

export const Simple: Story = {
  render: () => (
    <Card className="w-[350px] p-6">
      <p>간단한 카드 내용</p>
    </Card>
  ),
};
```

### Form Story

```typescript
// features/posts/components/post-form.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect, fn } from '@storybook/test';
import { PostForm } from './post-form';

const meta: Meta<typeof PostForm> = {
  title: 'Features/Posts/PostForm',
  component: PostForm,
  parameters: {
    layout: 'padded',
  },
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <div className="max-w-md">
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof PostForm>;

export const Empty: Story = {};

export const WithDefaultValues: Story = {
  args: {
    defaultValues: {
      title: '기존 제목',
      content: '기존 내용입니다.',
      status: 'draft',
    },
  },
};

export const FilledAndSubmit: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    await userEvent.type(canvas.getByLabelText(/제목/i), 'Test Title');
    await userEvent.type(canvas.getByLabelText(/내용/i), 'Test content');

    // Select status
    await userEvent.click(canvas.getByRole('combobox'));
    await userEvent.click(canvas.getByRole('option', { name: /발행/i }));

    // Submit
    await userEvent.click(canvas.getByRole('button', { name: /저장/i }));
  },
};

export const ValidationError: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Submit without filling
    await userEvent.click(canvas.getByRole('button', { name: /저장/i }));

    // Check for error message
    await expect(canvas.getByText(/필수/i)).toBeInTheDocument();
  },
};
```

---

## 스냅샷 관리 가이드

### 스냅샷 파일 구조

```
e2e/
├── visual/
│   ├── components.spec.ts
│   └── components.spec.ts-snapshots/    # Git에 커밋
│       ├── homepage-darwin.png
│       ├── homepage-linux.png
│       └── homepage-win32.png
```

### 스냅샷 업데이트

```bash
# 모든 스냅샷 업데이트
npx playwright test e2e/visual/ --update-snapshots

# 특정 테스트 스냅샷 업데이트
npx playwright test e2e/visual/button.spec.ts --update-snapshots
```

### 스냅샷 Threshold 설정

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      // 0.1% 픽셀 차이 허용 (폰트 렌더링 차이 대응)
      maxDiffPixelRatio: 0.001,
      // 또는 절대 픽셀 수
      maxDiffPixels: 100,
      // 애니메이션 비활성화
      animations: 'disabled',
    },
  },
});
```

### CI 환경 스냅샷 관리

```yaml
# .github/workflows/visual-test.yml
- name: Run visual tests
  run: npx playwright test e2e/visual/
  env:
    # Linux CI 환경에서 일관된 폰트 렌더링
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD: 1

- name: Upload diff on failure
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: visual-diff
    path: test-results/
```

> **Tip**: OS별 스냅샷 차이가 있을 경우 `playwright.config.ts`에서 `projects`를 분리하거나 Docker로 일관된 환경 유지 권장.

---

## Chromatic CI 설정

### Chromatic 설치 및 설정

```bash
npm install -D chromatic
```

### GitHub Actions 워크플로우

```yaml
# .github/workflows/chromatic.yml
name: Chromatic

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Chromatic은 git history 필요

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Publish to Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          buildScriptName: build-storybook
          exitZeroOnChanges: true  # PR에서 변경 시 fail 안 함
          autoAcceptChanges: main  # main 브랜치는 자동 승인
          onlyChanged: true        # 변경된 스토리만 테스트 (비용 절감)
```

### package.json 스크립트

```json
{
  "scripts": {
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "chromatic": "chromatic --exit-zero-on-changes",
    "test:visual": "playwright test e2e/visual/",
    "test:visual:update": "playwright test e2e/visual/ --update-snapshots"
  }
}
```

### Chromatic 환경 변수

```bash
# GitHub Secrets에 추가
CHROMATIC_PROJECT_TOKEN=chpt_xxxxxxxx
```

### TurboSnap (Monorepo 최적화)

```yaml
# .github/workflows/chromatic.yml
- name: Publish to Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    onlyChanged: true
    traceChanged: 'expanded'  # TurboSnap 활성화
```

---

## Dark Mode Story 패턴

### preview.ts 다크 모드 데코레이터

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { ThemeProvider } from 'next-themes';
import '../app/globals.css';

const preview: Preview = {
  parameters: {
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#0a0a0a' },
      ],
    },
  },
  decorators: [
    (Story, context) => {
      const theme = context.globals.theme || 'light';

      return (
        <ThemeProvider attribute="class" defaultTheme={theme} forcedTheme={theme}>
          <div className={theme === 'dark' ? 'dark' : ''}>
            <div className="min-h-screen bg-background text-foreground p-4">
              <Story />
            </div>
          </div>
        </ThemeProvider>
      );
    },
  ],
  globalTypes: {
    theme: {
      name: 'Theme',
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        icon: 'paintbrush',
        items: [
          { value: 'light', title: 'Light', icon: 'sun' },
          { value: 'dark', title: 'Dark', icon: 'moon' },
        ],
        dynamicTitle: true,
      },
    },
  },
};

export default preview;
```

### 다크/라이트 모드 Story 예제

```typescript
// components/ui/button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: {
    children: 'Button',
  },
};

// 라이트/다크 모드를 모두 보여주는 Story
export const LightMode: Story = {
  args: {
    children: 'Light Mode Button',
  },
  parameters: {
    backgrounds: { default: 'light' },
  },
  globals: {
    theme: 'light',
  },
};

export const DarkMode: Story = {
  args: {
    children: 'Dark Mode Button',
  },
  parameters: {
    backgrounds: { default: 'dark' },
  },
  globals: {
    theme: 'dark',
  },
};

// 모든 variant를 라이트/다크 모드로 비교
export const AllVariantsComparison: Story = {
  render: () => (
    <div className="grid grid-cols-2 gap-8">
      {/* Light Mode */}
      <div className="space-y-4 rounded-lg bg-white p-4">
        <h3 className="font-semibold text-gray-900">Light Mode</h3>
        <div className="flex flex-wrap gap-2">
          <Button variant="default">Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
        </div>
      </div>

      {/* Dark Mode */}
      <div className="dark space-y-4 rounded-lg bg-gray-950 p-4">
        <h3 className="font-semibold text-gray-100">Dark Mode</h3>
        <div className="flex flex-wrap gap-2">
          <Button variant="default">Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
        </div>
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
  },
};
```

### Card 다크 모드 Story

```typescript
// components/ui/card.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './card';

const meta: Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  parameters: {
    layout: 'centered',
  },
};

export default meta;
type Story = StoryObj<typeof Card>;

const CardExample = () => (
  <Card className="w-[350px]">
    <CardHeader>
      <CardTitle>카드 제목</CardTitle>
      <CardDescription>카드 설명입니다.</CardDescription>
    </CardHeader>
    <CardContent>
      <p>카드 내용이 여기에 표시됩니다.</p>
    </CardContent>
  </Card>
);

export const Light: Story = {
  render: CardExample,
  parameters: {
    backgrounds: { default: 'light' },
  },
  globals: { theme: 'light' },
};

export const Dark: Story = {
  render: CardExample,
  parameters: {
    backgrounds: { default: 'dark' },
  },
  globals: { theme: 'dark' },
};

// Chromatic용 Side-by-Side 비교
export const ThemeComparison: Story = {
  render: () => (
    <div className="flex gap-8">
      <div className="rounded-lg bg-white p-4">
        <CardExample />
      </div>
      <div className="dark rounded-lg bg-gray-950 p-4">
        <CardExample />
      </div>
    </div>
  ),
  parameters: {
    layout: 'padded',
    chromatic: { viewports: [1200] },
  },
};
```

---

## Chromatic 설정 파일

```javascript
// chromatic.config.json
{
  "projectToken": "chpt_xxxxxxxx",
  "buildScriptName": "build-storybook",
  "onlyChanged": true,
  "externals": ["public/**"],
  "skip": "@(docs|example)/**"
}
```

---

## 실행 명령어

```bash
# Storybook 개발 서버
npm run storybook

# 빌드
npm run build-storybook

# Chromatic (로컬에서 테스트)
npm run chromatic

# Chromatic (CI에서 자동 실행)
# GitHub Actions에서 자동 실행됨

# Playwright로 Storybook 테스트
npx playwright test e2e/visual/
```

---

## 테스트 예제

### Storybook Interaction 테스트

```typescript
// components/ui/button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect, fn } from '@storybook/test';
import { Button } from './button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  args: { onClick: fn() },
};

export default meta;

export const ClickTest: StoryObj<typeof Button> = {
  args: { children: 'Click Me' },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    // 클릭 테스트
    await userEvent.click(button);

    // onClick 호출 확인
    await expect(args.onClick).toHaveBeenCalled();
  },
};

export const DisabledTest: StoryObj<typeof Button> = {
  args: { children: 'Disabled', disabled: true },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    // disabled 속성 확인
    await expect(button).toBeDisabled();
    await expect(button).toHaveAttribute('disabled');
  },
};
```

### 스냅샷 테스트 유틸리티

```typescript
// e2e/visual/utils.ts
import { Page, expect } from '@playwright/test';

export async function takeComponentScreenshot(
  page: Page,
  componentSelector: string,
  name: string,
  options?: { animations?: 'disabled' | 'allow' }
) {
  const component = page.locator(componentSelector);
  await expect(component).toBeVisible();

  // 애니메이션 완료 대기
  await page.waitForLoadState('networkidle');

  await expect(component).toHaveScreenshot(`${name}.png`, {
    animations: options?.animations ?? 'disabled',
  });
}

export async function compareViewports(
  page: Page,
  url: string,
  name: string,
  viewports: { name: string; width: number; height: number }[]
) {
  for (const viewport of viewports) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    await page.goto(url);
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveScreenshot(`${name}-${viewport.name}.png`, {
      animations: 'disabled',
      fullPage: true,
    });
  }
}
```

---

## 안티패턴 (❌ Bad → ✅ Good)

### 1. 불안정한 스냅샷

```typescript
// ❌ Bad: 동적 콘텐츠 포함
await expect(page).toHaveScreenshot('page.png');  // 날짜, 시간 등 변경됨

// ✅ Good: 동적 콘텐츠 마스킹
await expect(page).toHaveScreenshot('page.png', {
  mask: [
    page.locator('[data-testid="timestamp"]'),
    page.locator('[data-testid="random-id"]'),
  ],
});
```

### 2. 환경 의존 스냅샷

```typescript
// ❌ Bad: OS별 다른 스냅샷
// macOS와 Linux에서 폰트 렌더링 차이로 실패

// ✅ Good: 허용 오차 설정 또는 Docker 사용
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixelRatio: 0.01,  // 1% 차이 허용
});

// 또는 Docker로 일관된 환경
// playwright.config.ts
projects: [
  {
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      // Docker 환경에서 일관된 폰트
      launchOptions: {
        args: ['--font-render-hinting=none'],
      },
    },
  },
],
```

### 3. 애니메이션으로 인한 실패

```typescript
// ❌ Bad: 애니메이션 중 스냅샷
await page.goto('/animated-page');
await expect(page).toHaveScreenshot();  // 애니메이션 상태에 따라 다름

// ✅ Good: 애니메이션 비활성화
await expect(page).toHaveScreenshot('page.png', {
  animations: 'disabled',
});

// 또는 CSS로 애니메이션 비활성화
await page.addStyleTag({
  content: '*, *::before, *::after { animation-duration: 0s !important; }',
});
```

### 4. 과도한 스냅샷

```typescript
// ❌ Bad: 모든 것을 스냅샷
// 수백 개의 스냅샷 → 유지보수 어려움

// ✅ Good: 중요 컴포넌트/페이지만 선별
// 디자인 시스템 컴포넌트
// 주요 페이지 레이아웃
// 중요 사용자 흐름
```

---

## 에러 처리

### 스냅샷 불일치 처리

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      // 허용 오차
      maxDiffPixelRatio: 0.005,  // 0.5%
      threshold: 0.2,  // 픽셀 색상 차이 허용치

      // 실패 시 차이점 저장
    },
  },
  // 실패 시 diff 이미지 저장
  outputDir: 'test-results',
});
```

### Chromatic 실패 처리

```yaml
# .github/workflows/chromatic.yml
- name: Publish to Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    exitZeroOnChanges: true  # 변경 시 실패하지 않음
    exitOnceUploaded: true   # 업로드 후 즉시 종료
  continue-on-error: true    # 워크플로우 계속 진행

- name: Comment PR with Chromatic link
  if: github.event_name == 'pull_request'
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '📸 Visual changes detected. [Review on Chromatic](${{ steps.chromatic.outputs.url }})'
      })
```

---

## 성능 고려사항

### 선택적 스냅샷 테스트

```typescript
// 변경된 컴포넌트만 테스트
// Chromatic의 TurboSnap 활용
// chromatic.yml
- uses: chromaui/action@latest
  with:
    onlyChanged: true  # 변경된 스토리만 테스트
    traceChanged: 'expanded'  # 의존성 추적
```

### Storybook 빌드 최적화

```typescript
// .storybook/main.ts
const config: StorybookConfig = {
  // 필요한 스토리만 포함
  stories: ['../components/**/*.stories.tsx'],

  // 불필요한 애드온 제거
  addons: [
    '@storybook/addon-essentials',
    // '@storybook/addon-docs',  // 비주얼 테스트에 불필요
  ],

  // 빌드 최적화
  core: {
    disableTelemetry: true,
  },
};
```

### 병렬 스냅샷 테스트

```typescript
// playwright.config.ts
export default defineConfig({
  // 비주얼 테스트 병렬 실행
  fullyParallel: true,
  workers: process.env.CI ? 4 : undefined,

  // 프로젝트별 분리
  projects: [
    {
      name: 'visual-desktop',
      testDir: './e2e/visual',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'visual-mobile',
      testDir: './e2e/visual',
      use: { ...devices['iPhone 13'] },
    },
  ],
});
```

---

## 보안 고려사항

### 민감 정보 마스킹

```typescript
// 개인정보가 포함된 페이지 테스트
test('profile page screenshot', async ({ page }) => {
  await page.goto('/profile');

  await expect(page).toHaveScreenshot('profile.png', {
    mask: [
      page.locator('[data-testid="email"]'),
      page.locator('[data-testid="phone"]'),
      page.locator('[data-testid="address"]'),
    ],
  });
});
```

### Chromatic 프로젝트 설정

```typescript
// chromatic.config.json
{
  "projectToken": "chpt_xxx",  // GitHub Secrets로 관리
  "zip": true,  // 업로드 데이터 압축
  "externals": ["public/**"],  // 외부 파일 포함
  "skip": "**/*.private.stories.tsx"  // 민감한 스토리 제외
}
```

### 스냅샷 저장소 분리

```yaml
# .gitignore에 추가하고 별도 저장소로 관리
# 또는 Git LFS 사용
e2e/**/*.png-snapshots/

# .gitattributes
*.png filter=lfs diff=lfs merge=lfs -text
```

---

## References

- `_references/TEST-PATTERN.md`
- `_references/COMPONENT-PATTERN.md`

