#!/bin/bash

# claude-craft installer v3.0
# MoAI-ADK: 37 Agents, 303 Skills, Hooks, Rules
#
# This script sets up Claude Code customizations from .claude/ directory
#
# Usage:
#   ./scripts/install.sh          # Default: symbolic links
#   ./scripts/install.sh --link   # Symbolic links (for development)
#   ./scripts/install.sh --copy   # Copy files (for standalone install)
#   ./scripts/install.sh --export # Create distribution package

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_SRC="$PROJECT_DIR/.claude"
CLAUDE_DEST="$HOME/.claude"

MODE="${1:---link}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}  ${BOLD}Claude Craft Installer v3.0${NC}                             ${CYAN}║${NC}"
echo -e "${CYAN}║${NC}     MoAI-ADK: 37 Agents, 303 Skills                        ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# Validate source directory
if [ ! -d "$CLAUDE_SRC" ]; then
    echo -e "${RED}Error:${NC} .claude/ directory not found in $PROJECT_DIR"
    exit 1
fi

# Ensure ~/.claude exists
mkdir -p "$CLAUDE_DEST"

# Component installation function
install_component() {
    local step="$1"
    local total="$2"
    local name="$3"
    local src_path="$4"
    local dest_path="$5"
    local mode="$6"
    local count_pattern="$7"
    local count_name="$8"

    echo -e "[${step}/${total}] Installing ${name}..."

    if [ -d "$src_path" ] && [ "$(ls -A $src_path 2>/dev/null)" ]; then
        rm -rf "$dest_path" 2>/dev/null || true

        if [ "$mode" = "copy" ]; then
            cp -r "$src_path" "$dest_path"
            echo -e "      ${GREEN}✓${NC} Copied to $dest_path"
        else
            ln -sf "$src_path" "$dest_path"
            echo -e "      ${GREEN}✓${NC} Linked to $dest_path"
        fi

        if [ -n "$count_pattern" ]; then
            local count=$(find "$src_path" -name "$count_pattern" 2>/dev/null | wc -l | tr -d ' ')
            echo -e "        → $count $count_name"
        fi
    else
        echo -e "      ${YELLOW}⚠${NC} Skipped (not found)"
    fi
}

case "$MODE" in
    --link|-l)
        echo -e "Mode: ${CYAN}Symbolic Links${NC} (development)"
        echo ""
        INSTALL_MODE="link"

        # 1. Install statusline.py (always copy for execution)
        echo "[1/7] Installing statusline.py..."
        if [ -f "$CLAUDE_SRC/statusline.py" ]; then
            cp "$CLAUDE_SRC/statusline.py" "$CLAUDE_DEST/"
            chmod +x "$CLAUDE_DEST/statusline.py"
            echo -e "      ${GREEN}✓${NC} Copied to $CLAUDE_DEST/statusline.py"
        fi

        # 2-7. Link directories
        install_component 2 7 "agents" "$CLAUDE_SRC/agents" "$CLAUDE_DEST/agents" "link" "*.md" "agents"
        install_component 3 7 "skills" "$CLAUDE_SRC/skills" "$CLAUDE_DEST/skills" "link" "SKILL.md" "skills"
        install_component 4 7 "hooks" "$CLAUDE_SRC/hooks" "$CLAUDE_DEST/hooks" "link" "" ""
        install_component 5 7 "rules" "$CLAUDE_SRC/rules" "$CLAUDE_DEST/rules" "link" "*.md" "rules"
        install_component 6 7 "commands" "$CLAUDE_SRC/commands" "$CLAUDE_DEST/commands" "link" "*.md" "commands"
        install_component 7 7 "output-styles" "$CLAUDE_SRC/output-styles" "$CLAUDE_DEST/output-styles" "link" "*.md" "output styles"
        ;;

    --copy|-c)
        echo -e "Mode: ${CYAN}Copy Files${NC} (standalone install)"
        echo ""
        INSTALL_MODE="copy"

        # 1. Install statusline.py
        echo "[1/7] Installing statusline.py..."
        if [ -f "$CLAUDE_SRC/statusline.py" ]; then
            cp "$CLAUDE_SRC/statusline.py" "$CLAUDE_DEST/"
            chmod +x "$CLAUDE_DEST/statusline.py"
            echo -e "      ${GREEN}✓${NC} Copied to $CLAUDE_DEST/statusline.py"
        fi

        # 2-7. Copy directories
        install_component 2 7 "agents" "$CLAUDE_SRC/agents" "$CLAUDE_DEST/agents" "copy" "*.md" "agents"
        install_component 3 7 "skills" "$CLAUDE_SRC/skills" "$CLAUDE_DEST/skills" "copy" "SKILL.md" "skills"
        install_component 4 7 "hooks" "$CLAUDE_SRC/hooks" "$CLAUDE_DEST/hooks" "copy" "" ""
        install_component 5 7 "rules" "$CLAUDE_SRC/rules" "$CLAUDE_DEST/rules" "copy" "*.md" "rules"
        install_component 6 7 "commands" "$CLAUDE_SRC/commands" "$CLAUDE_DEST/commands" "copy" "*.md" "commands"
        install_component 7 7 "output-styles" "$CLAUDE_SRC/output-styles" "$CLAUDE_DEST/output-styles" "copy" "*.md" "output styles"
        ;;

    --export|-e)
        echo -e "Mode: ${CYAN}Export Distribution Package${NC}"
        echo ""

        DIST_DIR="$PROJECT_DIR/dist"
        mkdir -p "$DIST_DIR"

        TIMESTAMP=$(date +%Y%m%d)
        PACKAGE_NAME="claude-craft-$TIMESTAMP.zip"

        echo "Creating distribution package..."
        cd "$PROJECT_DIR"

        # Create zip with all necessary files
        zip -r "$DIST_DIR/$PACKAGE_NAME" \
            .claude/ \
            .moai/ \
            CLAUDE.md \
            README.md \
            scripts/install.sh \
            -x "*.DS_Store" \
            -x "*/__pycache__/*" \
            -x "*.pyc"

        echo ""
        echo -e "${GREEN}Package created:${NC} $DIST_DIR/$PACKAGE_NAME"
        echo ""
        echo "To install on another machine:"
        echo "  1. unzip $PACKAGE_NAME"
        echo "  2. cd claude-craft-*"
        echo "  3. ./scripts/install.sh --copy"
        exit 0
        ;;

    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --link, -l    Create symbolic links (default, for development)"
        echo "  --copy, -c    Copy files (for standalone installation)"
        echo "  --export, -e  Create distribution zip package"
        echo "  --help, -h    Show this help message"
        echo ""
        echo "Components installed:"
        echo "  • agents/       37 AI agents (MoAI + Domain)"
        echo "  • skills/       303 skills (52 MoAI + 251 Domain)"
        echo "  • hooks/        Automation scripts"
        echo "  • rules/        16 language rules + workflows"
        echo "  • commands/     Slash commands"
        echo "  • output-styles/ Alfred, Yoda, R2D2 styles"
        echo "  • statusline.py Real-time cost tracking"
        exit 0
        ;;

    *)
        echo -e "${RED}Unknown option:${NC} $MODE"
        echo "Use --help for usage information"
        exit 1
        ;;
esac

# Configure settings.json
echo ""
echo "Checking settings.json..."
SETTINGS_FILE="$CLAUDE_DEST/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    echo -e "  ${GREEN}✓${NC} settings.json exists (preserving)"

    if grep -q "statusLine" "$SETTINGS_FILE"; then
        echo -e "    → statusLine already configured"
    else
        echo -e "    ${YELLOW}⚠${NC} Add statusLine config manually if needed"
    fi
else
    echo "  Creating default settings.json..."
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
EOF
    echo -e "  ${GREEN}✓${NC} Created $SETTINGS_FILE"
fi

# Summary
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}  ${BOLD}✓ Installation Complete!${NC}                                ${GREEN}║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}Installed Components:${NC}"
echo "  • agents/       37 AI agents (MoAI + Domain)"
echo "  • skills/       303 skills (52 MoAI + 251 Domain)"
echo "  • hooks/        Automation scripts"
echo "  • rules/        16 language rules + workflows"
echo "  • commands/     Slash commands"
echo "  • output-styles/ Alfred, Yoda, R2D2 styles"
echo "  • statusline.py Real-time cost tracking"
echo ""
echo -e "${BOLD}Paths:${NC}"
echo -e "  Source:  ${CYAN}$CLAUDE_SRC${NC}"
echo -e "  Target:  ${CYAN}$CLAUDE_DEST${NC}"
echo -e "  Mode:    ${CYAN}$INSTALL_MODE${NC}"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Restart Claude Code to apply changes"
echo -e "  2. Try ${CYAN}\"Hello, build me a FastAPI server\"${NC}"
echo -e "  3. Or use ${CYAN}/moai plan \"your feature\"${NC}"
echo ""
