# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**claude-craft** is a collection of Claude Code customizations including custom statusline for cost tracking, multi-skill agents, and hooks. The project installs components to `~/.claude/` via symlinks for easy syncing across machines.

## Installation

```bash
./install.sh
```

This installs:
1. `statusline.py` to `~/.claude/`
2. Symlinks `skills/` to `~/.claude/skills/`
3. Symlinks `hooks/` to `~/.claude/hooks/`
4. Configures `settings.json` with statusline command

## Architecture

### Agents

Agents are multi-skill orchestrators that combine multiple skills into coherent workflows:

- **ppt-agent**: 9-skill pipeline for presentation creation (Research → Validation → Structure → Content → Design System → Visual → Review → Refinement → Export)
- **tech-blog-agent**: 4-skill pipeline for Hashnode blog posts (Research → Draft → Review → Publish)
- **social-media-agent**: Multi-platform content creation agent

### Skills

Skills are located in `skills/<agent-name>/<number>-<skill-name>/SKILL.md`. Each skill defines:
- Trigger keywords
- Input/output specification
- Workflow steps

### PPT Design System

The PPT agent uses a comprehensive design system (`skills/ppt-agent/5-design-system/`):
- **10 topic-based themes**: Healthcare, Education, Fintech, AI/Tech, Sustainability, Startup, Luxury, Creative, Real Estate, F&B
- **10 slide templates**: Cover, Contents, Section Divider, Content, Statistics, Split Layout, Team, Quote, Timeline, Closing
- **5 color palettes**: Executive Minimal, Sage Professional, Modern Dark, Corporate Blue, Warm Neutral
- **Typography system**: Pretendard (Korean) / Inter (English), 7-level hierarchy from Hero (72-96pt) to Label (10-12pt)

Theme files: `skills/ppt-agent/5-design-system/themes/<number>-<theme>/THEME.md`

### Statusline

`statusline/statusline.py` - Real-time cost tracking for Claude Code sessions displaying:
- Session cost, daily cost, block cost
- Time remaining in current block
- Hourly burn rate

Pricing data is embedded for Opus, Sonnet, and Haiku models.

### Output Structure

Generated presentations go to `output/<project-name>/`:
- `slides/` - HTML slide files
- `design-system/` - Project-specific design tokens
- `*.pptx` - Generated PowerPoint files
- `generate_ppt.py` or `build-pptx.js` - Generation scripts

## PPT Generation

For PPT output projects using pptxgenjs:

```bash
cd output/<project-name>
npm install
npm run build
```

## Key Files

| Path | Purpose |
|------|---------|
| `agents/<name>/AGENT.md` | Agent configuration and workflow |
| `skills/<agent>/<n>-<skill>/SKILL.md` | Individual skill definition |
| `skills/ppt-agent/5-design-system/THEMES.md` | Theme selection guide |
| `skills/ppt-agent/5-design-system/themes/INDEX.md` | Theme keyword mapping |
| `statusline/statusline.py` | Cost tracking statusline script |
| `work-blog/` | Tech blog drafts and research |
| `work-plan/` | Planning documents |

## Conventions

- Agent workflows: Korean documentation, YAML frontmatter
- Skill naming: `<number>-<name>` for execution order
- PPT themes: `<number>-<topic>/THEME.md` with full color specs and CSS
- PptxGenJS colors: Use HEX without `#` prefix (e.g., `667eea` not `#667eea`)

## memoriz-docs

- @./memoriz/docs/prd.md
- @./memoriz/docs/architecture.md
- @./memoriz/docs/design-guide.md
- @./memoriz/docs/ia.md
