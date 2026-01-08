# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**claude-craft** is a collection of Claude Code customizations including custom statusline for cost tracking, multi-skill agents, and hooks. All Claude Code compatible components are organized under the `.claude/` directory.

## Installation

```bash
# Default: Symbolic links (for development)
./scripts/install.sh

# Copy files (standalone installation)
./scripts/install.sh --copy

# Create distribution package
./scripts/install.sh --export
```

This installs:
1. `.claude/statusline.py` to `~/.claude/statusline.py`
2. Links/copies `.claude/agents/` to `~/.claude/agents/`
3. Links/copies `.claude/skills/` to `~/.claude/skills/`
4. Links/copies `.claude/hooks/` to `~/.claude/hooks/`
5. Configures `settings.json` with statusline and hooks

## Architecture

### Directory Structure

```
claude-craft/
├── .claude/                    # Claude Code compatible package
│   ├── agents/                 # Agent definitions
│   ├── skills/                 # Skill definitions
│   ├── hooks/                  # Hook scripts
│   └── statusline.py           # Cost tracking script
│
├── workspace/                  # Work outputs (gitignored)
│   ├── output/                 # PPT outputs
│   ├── work-blog/              # Blog drafts
│   ├── work-social/            # Social media drafts
│   └── work-plan/              # Planning docs
│
├── scripts/
│   └── install.sh              # Installation script
│
└── memoriz/                    # Other projects
```

### Agents

Agents are multi-skill orchestrators that combine multiple skills into coherent workflows. Located in `.claude/agents/<agent-name>/AGENT.md`.

| Agent | Skills | Description |
|-------|--------|-------------|
| **ppt-agent** | 11 skills | 프레젠테이션 제작 파이프라인 (Research → Validation → Structure → Content → Design System → Visual → Image Gen → Review → Refinement → Export-PPTX → Export-PDF) |
| **tech-blog-agent** | 4 skills | Hashnode 블로그 작성 파이프라인 (Research → Draft → Review → Publish) |
| **social-media-agent** | 12 skills | 멀티플랫폼 소셜미디어 콘텐츠 제작 (Strategy → Research → Validation → Compliance → Content → Visual → Hashtag → Approval → Schedule → Repurpose → Engagement → Analytics) |

### Skills

Skills are located in `.claude/skills/<agent-name>-skills/<number>-<skill-name>/SKILL.md`. Each skill defines:
- Trigger keywords
- Input/output specification
- Workflow steps

**Skill Directories:**
- `.claude/skills/ppt-agent-skills/` - PPT 제작 관련 skills (11개)
- `.claude/skills/tech-blog-agent-skills/` - 블로그 작성 관련 skills (4개)
- `.claude/skills/social-media-agent-skills/` - 소셜미디어 관련 skills (12개)

### PPT Design System

The PPT agent uses a comprehensive design system (`.claude/skills/ppt-agent-skills/5-design-system/`):
- **10 topic-based themes**: Healthcare, Education, Fintech, AI/Tech, Sustainability, Startup, Luxury, Creative, Real Estate, F&B
- **10 slide templates**: Cover, Contents, Section Divider, Content, Statistics, Split Layout, Team, Quote, Timeline, Closing
- **5 color palettes**: Executive Minimal, Sage Professional, Modern Dark, Corporate Blue, Warm Neutral
- **Typography system**: Pretendard (Korean) / Inter (English), 7-level hierarchy from Hero (72-96pt) to Label (10-12pt)

Theme files: `.claude/skills/ppt-agent-skills/5-design-system/themes/<number>-<theme>/THEME.md`

### Social Media Platforms

The Social Media agent supports 4 platforms:
- **Instagram**: 피드, 릴스, 스토리, 캐러셀
- **LinkedIn**: 텍스트 포스트, 아티클, 캐러셀
- **X (Twitter)**: 트윗, 스레드, 인용
- **Threads**: 텍스트, 이미지

Platform-specific content skills: `.claude/skills/social-media-agent-skills/4-content/<platform>/SKILL.md`

### Hooks

Automated scripts that run on Claude Code events. Located in `.claude/hooks/`.

| Hook | Trigger | Description |
|------|---------|-------------|
| `post-write-hook.sh` | PostToolUse (Write/Edit) | Detects changes to AGENT.md or SKILL.md files |
| `sync-docs.sh` | Called by post-write-hook | Scans agents/skills and reports structure changes |

**Hook Configuration** (in `~/.claude/settings.json`):
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/post-write-hook.sh \"$CLAUDE_TOOL_USE_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

When a new agent or skill is added, the hook automatically:
1. Detects the file change in `.claude/agents/` or `.claude/skills/` directory
2. Runs `sync-docs.sh` to scan the current structure
3. Reports the updated agent/skill counts

### Statusline

`.claude/statusline.py` - Real-time cost tracking for Claude Code sessions displaying:
- Session cost, daily cost, block cost
- Time remaining in current block
- Hourly burn rate

Pricing data is embedded for Opus, Sonnet, and Haiku models.

### Output Structure

**PPT Output** - `workspace/output/<project-name>/`:
- `slides/` - HTML slide files
- `design-system/` - Project-specific design tokens
- `*.pptx` - Generated PowerPoint files
- `*.pdf` - Generated PDF files
- `build-pptx.js` - PPTX generation script
- `build-pdf.js` - PDF generation script
- `build-all.js` - Combined PPTX + PDF generation

**Blog Output** - `workspace/work-blog/`:
- `research/` - 리서치 노트
- `drafts/` - 초안
- `published/` - 발행 아카이브

**Social Media Output** - `workspace/work-social/`:
- `strategy/` - 브랜드 전략 문서
- `research/` - 리서치 노트
- `drafts/<platform>/` - 플랫폼별 드래프트
- `visuals/` - 비주얼 에셋
- `calendar/` - 콘텐츠 캘린더
- `analytics/` - 성과 리포트

## Build Commands

### PPT Generation (pptxgenjs)

```bash
cd workspace/output/<project-name>
npm install

npm run build        # PPTX only
npm run build:pdf    # PDF only
npm run build:all    # Both PPTX + PDF
```

## Key Files

| Path | Purpose |
|------|---------|
| `.claude/agents/<name>/AGENT.md` | Agent configuration and workflow |
| `.claude/skills/<agent>-skills/<n>-<skill>/SKILL.md` | Individual skill definition |
| `.claude/skills/ppt-agent-skills/5-design-system/THEMES.md` | Theme selection guide |
| `.claude/skills/ppt-agent-skills/5-design-system/themes/INDEX.md` | Theme keyword mapping |
| `.claude/hooks/post-write-hook.sh` | PostToolUse hook for detecting agent/skill changes |
| `.claude/hooks/sync-docs.sh` | Script to scan and report agent/skill structure |
| `.claude/statusline.py` | Cost tracking statusline script |
| `workspace/work-blog/` | Tech blog drafts and research |
| `workspace/work-social/` | Social media drafts and calendar |
| `workspace/work-plan/` | Planning documents |

## Conventions

- Agent workflows: Korean documentation, YAML frontmatter
- Skill naming: `<number>-<name>` for execution order
- Skills directory: `<agent-name>-skills` suffix to distinguish from agents
- PPT themes: `<number>-<topic>/THEME.md` with full color specs and CSS
- PptxGenJS colors: Use HEX without `#` prefix (e.g., `667eea` not `#667eea`)

## memoriz-docs

- @./memoriz/docs/prd.md
- @./memoriz/docs/architecture.md
- @./memoriz/docs/design-guide.md
- @./memoriz/docs/ia.md
