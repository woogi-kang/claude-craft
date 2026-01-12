# CI/CD Skill

GitHub Actions와 Vercel을 사용하여 CI/CD를 설정합니다.

## Triggers

- "ci/cd", "github actions", "배포", "deploy", "vercel"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `provider` | ✅ | vercel, aws, gcp |
| `environments` | ❌ | preview, staging, production |

---

## GitHub Actions - CI

### 기본 CI 워크플로우

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm typecheck

  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test:coverage
      # Codecov 업로드 (선택사항 - CODECOV_TOKEN 설정 시에만 실행)
      - uses: codecov/codecov-action@v4
        if: ${{ secrets.CODECOV_TOKEN != '' }}
        with:
          files: ./coverage/lcov.info
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: false  # Codecov 실패 시 CI 중단 방지

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
        env:
          NEXT_TELEMETRY_DISABLED: 1
```

### E2E 테스트 워크플로우

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    name: Playwright Tests
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Install Playwright Browsers
        run: pnpm exec playwright install --with-deps chromium
      - name: Run Playwright tests
        run: pnpm test:e2e
        env:
          BASE_URL: http://localhost:3000
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

---

## Vercel 배포

### vercel.json

```json
{
  "git": {
    "deploymentEnabled": {
      "main": true,
      "develop": true
    }
  },
  "github": {
    "silent": true
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store, max-age=0" }
      ]
    }
  ]
}
```

### 환경 변수 관리

```bash
# Vercel CLI로 환경 변수 설정
vercel env add DATABASE_URL production
vercel env add DATABASE_URL preview
vercel env add DATABASE_URL development

# 환경 변수 pull
vercel env pull .env.local
```

### Preview 배포 알림

```yaml
# .github/workflows/preview-comment.yml
name: Preview Comment

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Wait for Vercel Preview
        uses: patrickedqvist/wait-for-vercel-preview@v1.3.2
        id: preview
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          max_timeout: 300
      - name: Comment Preview URL
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 Preview deployed: ${{ steps.preview.outputs.url }}`
            })
```

---

## Database Migration

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]
    paths:
      - 'drizzle/**'

jobs:
  migrate:
    name: Run Migrations
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Run migrations
        run: pnpm db:migrate
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Generate Changelog
        id: changelog
        uses: orhun/git-cliff-action@v4
        with:
          config: cliff.toml
          args: --latest
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.content }}
          draft: false
          prerelease: false
```

### Changelog 설정

```toml
# cliff.toml
[changelog]
header = """
# Changelog\n
"""
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end="") }})\
{% endfor %}
{% endfor %}
"""
trim = true

[git]
conventional_commits = true
filter_commits = false
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^docs", group = "Documentation" },
  { message = "^perf", group = "Performance" },
  { message = "^refactor", group = "Refactoring" },
  { message = "^style", group = "Styling" },
  { message = "^test", group = "Testing" },
  { message = "^chore", group = "Miscellaneous" },
]
```

---

## Docker 배포 (Self-hosted)

### Dockerfile

```dockerfile
# Dockerfile
FROM node:20-alpine AS base
RUN corepack enable

FROM base AS deps
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN pnpm build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  output: 'standalone',
};
```

### Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    restart: unless-stopped

volumes:
  postgres_data:
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "typecheck": "tsc --noEmit",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```

---

## 테스트 예제

### GitHub Actions Workflow 테스트

```typescript
// scripts/__tests__/ci-validation.test.ts
import { describe, it, expect } from 'vitest';
import { load } from 'js-yaml';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('CI Workflow Validation', () => {
  it('ci.yml이 유효한 YAML이다', () => {
    const content = readFileSync(
      join(process.cwd(), '.github/workflows/ci.yml'),
      'utf-8'
    );

    expect(() => load(content)).not.toThrow();
  });

  it('필수 job들이 정의되어 있다', () => {
    const content = readFileSync(
      join(process.cwd(), '.github/workflows/ci.yml'),
      'utf-8'
    );
    const workflow = load(content) as Record<string, any>;

    expect(workflow.jobs).toHaveProperty('lint');
    expect(workflow.jobs).toHaveProperty('typecheck');
    expect(workflow.jobs).toHaveProperty('test');
    expect(workflow.jobs).toHaveProperty('build');
  });

  it('build job이 다른 job에 의존한다', () => {
    const content = readFileSync(
      join(process.cwd(), '.github/workflows/ci.yml'),
      'utf-8'
    );
    const workflow = load(content) as Record<string, any>;

    expect(workflow.jobs.build.needs).toContain('lint');
    expect(workflow.jobs.build.needs).toContain('typecheck');
    expect(workflow.jobs.build.needs).toContain('test');
  });
});
```

### Dockerfile 테스트

```typescript
// scripts/__tests__/docker.test.ts
import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync } from 'fs';

describe('Docker Configuration', () => {
  it('Dockerfile이 존재한다', () => {
    expect(existsSync('Dockerfile')).toBe(true);
  });

  it('multi-stage 빌드를 사용한다', () => {
    const dockerfile = readFileSync('Dockerfile', 'utf-8');

    expect(dockerfile).toContain('FROM node:20-alpine AS base');
    expect(dockerfile).toContain('FROM base AS deps');
    expect(dockerfile).toContain('FROM base AS builder');
    expect(dockerfile).toContain('FROM base AS runner');
  });

  it('non-root 사용자로 실행된다', () => {
    const dockerfile = readFileSync('Dockerfile', 'utf-8');

    expect(dockerfile).toContain('USER nextjs');
  });
});
```

---

## 안티패턴

### 1. 시크릿 하드코딩

```yaml
# ❌ Bad: 시크릿 하드코딩
- name: Deploy
  run: |
    DATABASE_URL=postgres://user:password@host/db npm run deploy

# ✅ Good: GitHub Secrets 사용
- name: Deploy
  run: npm run deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 2. 캐시 미사용

```yaml
# ❌ Bad: 매번 전체 설치
- run: pnpm install

# ✅ Good: 의존성 캐싱
- uses: pnpm/action-setup@v4
  with:
    version: 9
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'pnpm'
- run: pnpm install --frozen-lockfile
```

### 3. 병렬화 미활용

```yaml
# ❌ Bad: 순차 실행
jobs:
  ci:
    steps:
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test
      - run: pnpm build

# ✅ Good: 병렬 job 실행
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: pnpm lint
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - run: pnpm typecheck
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pnpm test
  build:
    needs: [lint, typecheck, test]
    steps:
      - run: pnpm build
```

### 4. 환경 분리 미흡

```yaml
# ❌ Bad: 환경 구분 없이 배포
- name: Deploy
  run: vercel --prod

# ✅ Good: 환경별 분리
- name: Deploy Preview
  if: github.event_name == 'pull_request'
  run: vercel

- name: Deploy Production
  if: github.ref == 'refs/heads/main'
  run: vercel --prod
  environment: production
```

---

## 에러 처리

### CI 에러 분류

```typescript
// scripts/ci/error-handler.ts
type CIErrorType =
  | 'LINT_FAILED'
  | 'TYPE_ERROR'
  | 'TEST_FAILED'
  | 'BUILD_FAILED'
  | 'DEPLOY_FAILED';

interface CIError {
  type: CIErrorType;
  message: string;
  exitCode: number;
  logs?: string;
}

function handleCIError(error: CIError): void {
  console.error(`::error::${error.type}: ${error.message}`);

  // GitHub Actions 어노테이션
  if (error.logs) {
    console.log('::group::Error Details');
    console.log(error.logs);
    console.log('::endgroup::');
  }

  process.exit(error.exitCode);
}
```

### 재시도 로직

```yaml
# GitHub Actions에서 재시도
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: pnpm test
```

---

## 성능 고려사항

### 1. Concurrency 제어

```yaml
# 중복 워크플로우 취소
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### 2. 변경된 파일만 체크

```yaml
# 변경된 파일 경로로 필터링
- uses: dorny/paths-filter@v3
  id: changes
  with:
    filters: |
      src:
        - 'src/**'
      tests:
        - 'tests/**'

- name: Run tests
  if: steps.changes.outputs.src == 'true' || steps.changes.outputs.tests == 'true'
  run: pnpm test
```

### 3. Docker 레이어 캐싱

```yaml
- name: Build and push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: myapp:latest
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 4. Turborepo 리모트 캐싱

```yaml
- name: Build with Turbo
  run: pnpm build
  env:
    TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
    TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

---

## 보안 고려사항

### 1. 시크릿 관리

```yaml
# 환경별 시크릿 분리
jobs:
  deploy:
    environment: production
    steps:
      - run: npm run deploy
        env:
          # production 환경의 시크릿만 접근 가능
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 2. PR 보안

```yaml
# Fork PR에서 시크릿 접근 제한
- name: Run secure task
  if: github.event.pull_request.head.repo.full_name == github.repository
  run: npm run deploy
  env:
    SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

### 3. OIDC 인증

```yaml
# AWS 배포 시 OIDC 사용 (장기 크레덴셜 대신)
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
      aws-region: ap-northeast-2
```

### 4. 의존성 감사

```yaml
- name: Security audit
  run: pnpm audit --audit-level=high

- name: Dependency review
  uses: actions/dependency-review-action@v4
  if: github.event_name == 'pull_request'
```

---

## References

- `_references/ARCHITECTURE-PATTERN.md`
- `_references/TEST-PATTERN.md`

