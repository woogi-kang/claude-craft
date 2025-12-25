# claude-craft

Claude Code customizations - statusline, skills, agents, hooks, and more.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/woogi-kang/claude-craft.git ~/Development/claude-craft

# Run installer
cd ~/Development/claude-craft
./install.sh
```

## Structure

```
claude-craft/
├── statusline/          # Cost tracking statusline
│   └── statusline.py
├── skills/              # Custom Claude Code skills
├── agents/              # Custom agent configurations
├── hooks/               # Hook scripts
├── mcp-servers/         # MCP server scripts
├── templates/           # CLAUDE.md templates, etc.
└── install.sh           # Installer script
```

## Components

### Statusline
Real-time cost monitoring for Claude Code sessions.

**Display format:**
```
🎒 Opus 4.5 | 💰 $2.09 session / $28.03 today / $2.09 block (3h 58m left) | 🔥 $5.23/hr
```

### Skills
Custom skills for Claude Code. Add new skills by creating folders in `skills/`.

### Hooks
Pre/post execution hooks. Add scripts in `hooks/`.

## Syncing Across Machines

```bash
# On new machine
cd ~/Development/claude-craft
git pull
./install.sh
```

## License

MIT
