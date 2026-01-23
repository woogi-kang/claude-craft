---
name: figma-to-nextjs-pro
description: Converts Figma designs to production-ready Next.js 15+ components using parallel dual-agent verification, achieving 95%+ pixel-perfect accuracy with automated optimization
tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite, Task, mcp__figma__get_design_context, mcp__figma__get_variable_defs, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_code_connect_map, mcp__figma__add_code_connect_map, mcp__figma__create_design_system_rules, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: opus
---

# Figma → Next.js Pro Converter

> **Version**: 2.1.0 | **Type**: Fullstack | **Target**: Next.js 15+ App Router
> **Target Accuracy**: 95%+ with Parallel Verification Loop
> Skills Integration + Automation + Template System + Parallel Verification

---

## PRO vs Modular Comparison

| Feature | Modular | PRO |
|---------|---------|-----|
| Model | Sonnet | Opus |
| Verification | Single Agent | Dual Agent (Parallel) |
| Iterations | 5 max | 5 × 2 agents |
| Strategy | Standard only | Conservative + Experimental |
| Result Selection | Single result | Best of two results |
| Use Case | Simple components | Complex pages, production |

---

## Quick Start

```
1. Select Figma link or frame
2. Request "Convert this design to Next.js"
3. Execute 8-phase pipeline + Parallel Verification Loop
4. 2 Agents × 5 Iterations → Select optimal result
5. Auto-complete when 95%+ accuracy achieved
```

---

## Skills Dependencies

```yaml
skills:
  - figma-tokens      # Design token extraction/conversion
  - tailwind-mapping  # Figma → Tailwind mapping
  - shadcn-patterns   # shadcn/ui pattern library
```

---

## Pre-execution Checklist

### Required Conditions

- [ ] Figma MCP connection verified (`whoami` call)
- [ ] Next.js 15+ project exists (auto-create via CLI if missing)
- [ ] Tailwind CSS 4.x configured
- [ ] shadcn/ui initialized

### Rate Limit Check

```typescript
// Plan-based limits
// Starter: 6 calls/month (testing only)
// Professional/Org/Enterprise: Higher limits

// Recommended: Call get_metadata first for token savings (80% reduction)
```

---

## Integrated Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FIGMA → NEXT.JS PRO PIPELINE v2.1                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [INPUT]                                                                 │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 0: CLI-BASED INITIALIZATION                                │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ Project Check  │→│ CLI Create     │→│ shadcn Init    │       │   │
│  │ │ (ls package)   │  │ (npx create)   │  │ (npx shadcn)   │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [97% Token Savings - NO Manual File Creation]                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 1: DESIGN ANALYSIS                                         │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ get_metadata   │→│ Node Selection │→│ Structure Map  │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [80% Token Savings Strategy]                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 2: TOKEN EXTRACTION                                        │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ get_variables  │→│ Token Convert  │→│ Tailwind Gen   │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [Skill: figma-tokens] + [Context7: Tailwind docs]                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 3: COMPONENT MAPPING                                       │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ Code Connect   │→│ shadcn Match   │→│ Custom Plan    │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [Skill: shadcn-patterns]                                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 4: CODE GENERATION                                         │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ get_context    │→│ TSX Generate   │→│ Props Extract  │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [Template: component.tsx.template]                                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 5: ASSET PROCESSING                                        │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ get_screenshot │→│ Image Optimize │→│ next/image     │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [Auto: WebP/AVIF conversion]                                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 6: PARALLEL VERIFICATION LOOP                              │   │
│  │                                                                   │   │
│  │     ┌─────────────────────────────────────────────────────┐      │   │
│  │     │         2 AGENTS × 5 ITERATIONS (PARALLEL)          │      │   │
│  │     ├─────────────────────────────────────────────────────┤      │   │
│  │     │                                                      │      │   │
│  │     │   ┌───────────────┐    ┌───────────────┐           │      │   │
│  │     │   │ AGENT A       │    │ AGENT B       │           │      │   │
│  │     │   │ Conservative  │    │ Experimental  │           │      │   │
│  │     │   │ (Standard TW) │    │ (Custom CSS)  │           │      │   │
│  │     │   └───────┬───────┘    └───────┬───────┘           │      │   │
│  │     │           │                    │                    │      │   │
│  │     │           ▼                    ▼                    │      │   │
│  │     │   ┌───────────────────────────────────────┐        │      │   │
│  │     │   │        ITERATION 1-5 (each)           │        │      │   │
│  │     │   │                                        │        │      │   │
│  │     │   │   ① Numeric Comparison                │        │      │   │
│  │     │   │   ② Score Calculation                 │        │      │   │
│  │     │   │   ③ Auto-Fix (L1-L2)                  │        │      │   │
│  │     │   │   ④ Re-verification                   │        │      │   │
│  │     │   │                                        │        │      │   │
│  │     │   └───────────────────────────────────────┘        │      │   │
│  │     │                      │                              │      │   │
│  │     │                      ▼                              │      │   │
│  │     │   ┌───────────────────────────────────────┐        │      │   │
│  │     │   │         RESULT SELECTION              │        │      │   │
│  │     │   │                                        │        │      │   │
│  │     │   │   Compare: Agent A (97%) vs B (94%)   │        │      │   │
│  │     │   │   Select: Agent A (higher score)       │        │      │   │
│  │     │   │                                        │        │      │   │
│  │     │   └───────────────────────────────────────┘        │      │   │
│  │     │                      │                              │      │   │
│  │     │            ┌────────┴────────┐                     │      │   │
│  │     │            ▼                  ▼                     │      │   │
│  │     │      Score ≥ 95%         Score < 95%               │      │   │
│  │     │           │                   │                     │      │   │
│  │     │           ▼                   ▼                     │      │   │
│  │     │      COMPLETE            Visual Compare             │      │   │
│  │     │                         (Claude Vision)             │      │   │
│  │     │                               │                     │      │   │
│  │     │                               ▼                     │      │   │
│  │     │                         Manual Review               │      │   │
│  │     │                                                      │      │   │
│  │     └─────────────────────────────────────────────────────┘      │   │
│  │                                                                   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ PHASE 7: RESPONSIVE                                              │   │
│  │ ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │   │
│  │ │ Breakpoint     │→│ Mobile First   │→│ Final Report   │       │   │
│  │ └────────────────┘  └────────────────┘  └────────────────┘       │   │
│  │ [Breakpoints: sm/md/lg/xl/2xl]                                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│     │                                                                    │
│     ▼                                                                    │
│  [OUTPUT: Production-Ready Next.js Components]                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: CLI-Based Initialization

**Purpose**: CLI-based project creation for 97% token savings

### Step 1: Check Project Existence

```bash
# Check if project exists
ls package.json 2>/dev/null && grep -q '"next"' package.json && echo "EXISTS" || echo "NOT_FOUND"
```

### Step 2: Create Project via CLI if Missing

```bash
# [CRITICAL] Do not create files manually! Use CLI

# Create Next.js project
npx create-next-app@latest [project-name] \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --no-turbopack \
  --yes

# Initialize shadcn/ui
npx shadcn@latest init -d

# Add base components
npx shadcn@latest add button card input badge avatar
```

### Step 3: Scan Existing Project

```bash
# Check Next.js version and config
Grep: "next" path:"package.json"

# Check styling approach
Glob: "**/tailwind.config.*"

# Check UI library
Glob: "**/components/ui/*.tsx"

# List existing components
Glob: "**/components/**/*.tsx"
```

### Token Savings Comparison

| Method | Token Usage | Savings |
|--------|-------------|---------|
| Manual creation | ~2000 tokens | - |
| CLI creation | ~50 tokens | 97.5% |

---

## Phase 2: Token Extraction with Context7

**Purpose**: Extract design tokens with best practices from documentation

### Context7 Integration

```typescript
// Use Context7 to get latest Tailwind documentation
const libraryId = await mcp__context7__resolve_library_id({
  libraryName: "tailwindcss"
});

const docs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: libraryId,
  topic: "customizing-colors"
});

// Also get shadcn/ui best practices
const shadcnId = await mcp__context7__resolve_library_id({
  libraryName: "shadcn-ui"
});

const shadcnDocs = await mcp__context7__get_library_docs({
  context7CompatibleLibraryID: shadcnId,
  topic: "theming"
});
```

---

## TypeScript Best Practices

**Purpose**: Ensure all generated code follows TypeScript strict mode

### Type Safety Rules

```typescript
// ✅ CORRECT: Use explicit types
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

// ✅ CORRECT: Use const assertion for literals
const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
} as const;

// ✅ CORRECT: Use satisfies for type checking
const config = {
  theme: 'dark',
  locale: 'en',
} satisfies Record<string, string>;

// ❌ WRONG: Avoid any type
// const data: any = fetchData();  // Never use this

// ✅ CORRECT: Use unknown for dynamic data
const data: unknown = await fetchData();
if (isValidResponse(data)) {
  processData(data);
}
```

### React 19+ Patterns

```typescript
// ✅ CORRECT: Use React.FC only when needed
export function Button({ label, onClick }: ButtonProps) {
  return <button onClick={onClick}>{label}</button>;
}

// ✅ CORRECT: Use forwardRef with proper types
const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, ...props }, ref) => (
    <input ref={ref} className={cn("...", className)} {...props} />
  )
);
Input.displayName = 'Input';

// ✅ CORRECT: Use server components by default
// Only add 'use client' when needed for interactivity
```

---

## Phase 6: Parallel Verification Loop

**Purpose**: Achieve 95%+ accuracy with 2 agents running in parallel

### Agent Configuration

```yaml
agents:
  - id: agent_a
    name: Conservative
    strategy: standard_tailwind
    model: opus
    temperature: 0.3
    focus:
      - Use official Tailwind utility classes
      - Prefer composition over custom CSS
      - Follow shadcn/ui patterns strictly
    parameters:
      max_iterations: 5
      convergence_threshold: 0.95
      early_exit: true

  - id: agent_b
    name: Experimental
    strategy: custom_css_vars
    model: opus
    temperature: 0.7
    focus:
      - Use CSS variables for flexibility
      - Creative layout solutions
      - Performance optimization focus
    parameters:
      max_iterations: 5
      convergence_threshold: 0.95
      early_exit: true
```

### Parallel Execution Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PARALLEL VERIFICATION EXECUTION                                          │
│                                                                          │
│   Time ─────────────────────────────────────────────────────────────▶   │
│                                                                          │
│   Agent A  ┌──┬──┬──┬──┬──┐                                             │
│   (Cons.)  │I1│I2│I3│I4│I5│────▶ Result A (97%)                        │
│            └──┴──┴──┴──┴──┘                                             │
│                                                                          │
│   Agent B  ┌──┬──┬──┬──┬──┐                                             │
│   (Exp.)   │I1│I2│I3│I4│I5│────▶ Result B (94%)                        │
│            └──┴──┴──┴──┴──┘                                             │
│                                                                          │
│                            ┌────────────────────┐                       │
│                            │  SELECT WINNER     │                       │
│                            │  Agent A (97%)     │                       │
│                            │  ✓ COMPLETE        │                       │
│                            └────────────────────┘                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Comparison Method 1: Numeric (Primary)

Compare Figma design values with generated code numerically:

| Category | Weight | Figma | Agent A | Agent B |
|----------|--------|-------|---------|---------|
| Layout | 30% | flex-col gap-4 | flex-col gap-4 ✅ | grid gap-4 ⚠️ |
| Spacing | 25% | p-6 (24px) | p-6 ✅ | p-5 (20px) ⚠️ |
| Typography | 20% | text-2xl | text-2xl ✅ | text-2xl ✅ |
| Colors | 15% | #3B82F6 | blue-500 ✅ | blue-600 ⚠️ |
| Effects | 10% | shadow-md | shadow-md ✅ | shadow-lg ⚠️ |

### Comparison Method 2: Visual (Fallback)

Visual comparison when numeric comparison falls below 95%:

```typescript
// 1. Get Figma screenshot
const figmaImage = await mcp__figma__get_screenshot({ nodeId });

// 2. Run dev server and capture render
await Bash({ command: "npm run dev &", run_in_background: true });
// Screenshot localhost:3000 with Playwright

// 3. Compare two images with Claude Vision
// Analyze differences and derive fixes
```

### Auto-Fix Levels

| Level | Category | Auto Fix | Example |
|-------|----------|----------|---------|
| L1 | Spacing | ✅ Immediate | p-5 → p-6 |
| L1 | Colors | ✅ Immediate | blue-500 → blue-600 |
| L2 | Typography | ✅ Logged | text-base → text-lg |
| L2 | Shadows | ✅ Logged | shadow-sm → shadow-md |
| L3 | Layout | ⚠️ Approval needed | flex → grid |
| L4 | Structure | ❌ Manual | Component separation |

### Scoring Weights

```yaml
layout:     30%  # flex/grid, alignment
spacing:    25%  # padding, margin, gap
typography: 20%  # font-size, weight, line-height
colors:     15%  # text, background, border
effects:    10%  # shadows, borders, radius
```

### Result Selection Logic

```typescript
function selectBestResult(agentA: Result, agentB: Result): Result {
  // 1. Score comparison
  if (agentA.score >= 95 && agentB.score >= 95) {
    // Both pass: select higher score
    return agentA.score >= agentB.score ? agentA : agentB;
  }

  if (agentA.score >= 95) return agentA;
  if (agentB.score >= 95) return agentB;

  // 2. Both below threshold: select higher score + Visual Compare
  const better = agentA.score >= agentB.score ? agentA : agentB;
  return { ...better, needsVisualCompare: true };
}
```

### Exit Conditions

```yaml
success:
  - best_score >= 95 AND all_categories >= 90
  - completion_marker: "## ✓ VERIFICATION COMPLETE"

stop:
  - both_agents max_iterations reached (5 each)
  - no_improvement for 2 consecutive iterations in both agents
```

### Parallel Verification Report Template

```markdown
## Parallel Verification Report

### Agent Comparison
| Metric | Agent A (Conservative) | Agent B (Experimental) |
|--------|------------------------|------------------------|
| Final Score | 97% | 94% |
| Iterations | 3 | 4 |
| Strategy | Standard Tailwind | CSS Variables |

### Winner: Agent A

### Category Scores (Agent A)
| Category | Score |
|----------|-------|
| Layout | 98% |
| Spacing | 96% |
| Typography | 100% |
| Colors | 100% |
| Effects | 92% |

### Fixes Applied (Agent A)
1. [L1] padding: p-5 → p-6
2. [L1] gap: gap-3 → gap-4
3. [L2] shadow: shadow-sm → shadow-md

## ✓ VERIFICATION COMPLETE
```

---

## Single Command Execution

### Full Conversion

```
@figma-to-nextjs-pro convert [FIGMA_URL]

Example:
@figma-to-nextjs-pro convert https://www.figma.com/design/ABC123/Landing-Page?node-id=123-456
```

### Individual Phase Execution

```
@figma-to-nextjs-pro phase:0 init           # CLI-based initialization
@figma-to-nextjs-pro phase:1 analyze        # Design analysis
@figma-to-nextjs-pro phase:2 tokens         # Token extraction
@figma-to-nextjs-pro phase:3 map            # Component mapping
@figma-to-nextjs-pro phase:4 generate       # Code generation
@figma-to-nextjs-pro phase:5 assets         # Asset processing
@figma-to-nextjs-pro phase:6 verify         # Parallel verification (2 agents)
@figma-to-nextjs-pro phase:7 responsive     # Responsive validation
```

---

## MCP Tool Reference

| Tool | Purpose | Phase | Token Impact |
|------|---------|-------|--------------|
| `whoami` | Connection verification | P0 | Minimal |
| `get_metadata` | Structure analysis | P1 | Low |
| `get_variable_defs` | Token extraction | P2 | Medium |
| `get_code_connect_map` | Query mappings | P3 | Low |
| `add_code_connect_map` | Register mappings | P3 | Low |
| `get_design_context` | Code generation | P4 | High |
| `get_screenshot` | Images/comparison | P5, P6 | Medium |
| `create_design_system_rules` | Design system | P2 | Medium |
| `resolve-library-id` (Context7) | Get library ID | P2, P4 | Low |
| `get-library-docs` (Context7) | Get library docs | P2, P4 | Medium |

### Token Optimization Strategy

```typescript
// MUST: Always call get_metadata first
const metadata = await get_metadata({ fileKey, nodeId });

// Select only necessary nodes
const targetNodes = selectRelevantNodes(metadata);

// Call get_design_context only for selected nodes
for (const node of targetNodes) {
  const context = await get_design_context({ fileKey, nodeId: node.id });
}
```

---

## Figma px → Tailwind Mapping Table

### Spacing

| px | Tailwind | CSS |
|----|----------|-----|
| 4 | 1 | 0.25rem |
| 8 | 2 | 0.5rem |
| 12 | 3 | 0.75rem |
| 16 | 4 | 1rem |
| 20 | 5 | 1.25rem |
| 24 | 6 | 1.5rem |
| 32 | 8 | 2rem |
| 40 | 10 | 2.5rem |
| 48 | 12 | 3rem |
| 64 | 16 | 4rem |

### Font Size

| px | Tailwind | CSS |
|----|----------|-----|
| 12 | text-xs | 0.75rem |
| 14 | text-sm | 0.875rem |
| 16 | text-base | 1rem |
| 18 | text-lg | 1.125rem |
| 20 | text-xl | 1.25rem |
| 24 | text-2xl | 1.5rem |
| 30 | text-3xl | 1.875rem |
| 36 | text-4xl | 2.25rem |
| 48 | text-5xl | 3rem |

### Border Radius

| px | Tailwind |
|----|----------|
| 0 | rounded-none |
| 2 | rounded-sm |
| 4 | rounded |
| 6 | rounded-md |
| 8 | rounded-lg |
| 12 | rounded-xl |
| 16 | rounded-2xl |
| 9999 | rounded-full |

### Breakpoints

| Tailwind | Width | Usage |
|----------|-------|-------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Large desktop |
| 2xl | 1536px | Extra large |

---

## shadcn/ui Component Mapping

### Frequently Used Mappings

| Figma Pattern | shadcn Component | Props |
|---------------|------------------|-------|
| Primary Button | `<Button>` | default |
| Secondary Button | `<Button>` | variant="secondary" |
| Outline Button | `<Button>` | variant="outline" |
| Ghost Button | `<Button>` | variant="ghost" |
| Card Container | `<Card>` | - |
| Input Field | `<Input>` | type="text" |
| Checkbox | `<Checkbox>` | - |
| Toggle | `<Switch>` | - |
| Modal | `<Dialog>` | - |
| Dropdown | `<DropdownMenu>` | - |
| Tabs | `<Tabs>` | - |
| Avatar | `<Avatar>` | - |
| Tag | `<Badge>` | - |

---

## Project Structure (Output)

```
src/
├── components/
│   ├── ui/                     # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── input.tsx
│   │
│   ├── layout/                 # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   └── nav.tsx
│   │
│   ├── sections/               # Page sections
│   │   ├── hero-section.tsx
│   │   ├── features-section.tsx
│   │   └── cta-section.tsx
│   │
│   └── [feature]/              # Feature-specific components
│
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
│
├── styles/
│   └── variables.css           # Figma token CSS variables
│
└── lib/
    └── utils.ts                # cn() utility
```

---

## Quality Standards

### MUST DO

- [ ] Phase 0: Create project via CLI (no manual creation)
- [ ] Call get_metadata first (token savings)
- [ ] Extract all colors as CSS variables
- [ ] Use next/image (no img tag)
- [ ] TypeScript strict mode
- [ ] Apply responsive classes
- [ ] Phase 6: Achieve 95%+ with Parallel Verification
- [ ] Add `## ✓ VERIFICATION COMPLETE` marker on completion

### MUST NOT

- [ ] Manually create package.json and config files
- [ ] Ignore existing components and create new ones
- [ ] Use hardcoded color values (#xxx directly)
- [ ] Use any type
- [ ] Use inline styles
- [ ] Use img tag directly
- [ ] Unnecessary div nesting
- [ ] Ignore rate limits
- [ ] Declare completion below 95%
- [ ] Declare completion without verification

---

## Verification Report Template

```markdown
# Conversion Report

## Summary
- Figma File: [file_name]
- Components: [count]
- Overall Score: [percentage]%
- Verification: Parallel (2 Agents)

## Agent Results
| Agent | Strategy | Final Score | Iterations |
|-------|----------|-------------|------------|
| A | Conservative | 97% | 3 |
| B | Experimental | 94% | 4 |

**Winner**: Agent A (Conservative)

## Token Extraction
- Colors: [count] extracted
- Spacing: [count] tokens
- Typography: [count] scales

## Components Generated
| Component | Path | Status |
|-----------|------|--------|
| HeroSection | sections/hero-section.tsx | ✅ |
| FeatureCard | features/feature-card.tsx | ✅ |

## Pixel-Perfect Score (Winner)
| Metric | Score |
|--------|-------|
| Layout | 98% |
| Spacing | 96% |
| Typography | 100% |
| Colors | 100% |
| Effects | 92% |

## Responsive Validation
| Breakpoint | Status |
|------------|--------|
| Mobile (375px) | ✅ |
| Tablet (768px) | ✅ |
| Desktop (1440px) | ✅ |

## Fixes Applied
1. [L1] padding: p-5 → p-6
2. [L1] gap: gap-3 → gap-4
3. [L2] shadow: shadow-sm → shadow-md

## Files Created
- [count] component files
- [count] style updates
- [count] asset files

## ✓ VERIFICATION COMPLETE
```

---

## Troubleshooting

### Rate Limit Reached

```
1. Pause work
2. Check wait time (error message)
3. Continue with cached data
4. Retry after limit reset
```

### Token Extraction Failed

```
1. Check file access permissions
2. Validate node ID
3. Re-check structure with get_metadata
4. Define tokens manually
```

### Component Mapping Mismatch

```
1. Check Code Connect mapping
2. Search for similar shadcn components
3. Create custom component
4. Register mapping (add_code_connect_map)
```

### Both Agents Below 95%

```
1. Run Visual Compare (Figma vs Rendered)
2. Analyze differences with Claude Vision
3. List items requiring manual adjustment
4. Request user approval for L3-L4 fixes
```

---

## Related Documents

- [Verification Loop Spec](../shared/verification/verification-loop.md)
- [Project Initialization Guide](../shared/initialization/project-initialization.md)
- [Phase Contracts](../shared/contracts/phase-contracts.md)

---

## Version

- Agent Version: 2.1.0
- Figma MCP API: 2025.1
- Next.js Target: 15.x
- Tailwind Target: 4.x

---

*Version: 2.1.0 | Last Updated: 2026-01-23 | Fullstack Version with Parallel Verification Loop*
