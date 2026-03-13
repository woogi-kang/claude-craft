#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CLAUDE_SRC="$PROJECT_DIR/.claude"
CLAUDE_DEST="$HOME/.claude"
MODE="${1:---link}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

print_banner() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  ${BOLD}Claude Craft Installer${NC}                                 ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     Domain agents, skills, commands, status line         ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

install_dir_component() {
    local step="$1"
    local total="$2"
    local name="$3"
    local src="$4"
    local dest="$5"
    local install_mode="$6"
    local count_pattern="$7"

    echo "[${step}/${total}] Installing ${name}..."

    if [ ! -d "$src" ] || [ -z "$(ls -A "$src" 2>/dev/null)" ]; then
        echo -e "      ${YELLOW}Skipped${NC} (not found)"
        return
    fi

    rm -rf "$dest" 2>/dev/null || true
    if [ "$install_mode" = "copy" ]; then
        cp -R "$src" "$dest"
        echo -e "      ${GREEN}✓${NC} Copied to $dest"
    else
        ln -s "$src" "$dest"
        echo -e "      ${GREEN}✓${NC} Linked to $dest"
    fi

    if [ -n "$count_pattern" ]; then
        local count
        count=$(find "$src" -name "$count_pattern" 2>/dev/null | wc -l | tr -d ' ')
        echo "        → $count items"
    fi
}

export_package() {
    local dist_dir="$PROJECT_DIR/dist"
    local package_name="claude-craft-$(date +%Y%m%d).zip"
    local files=(
        "CLAUDE.md"
        "README.md"
        "docs/install.sh"
        "scripts/install.sh"
        ".claude/statusline.py"
        ".claude/settings.json"
    )

    [ -d "$PROJECT_DIR/.claude/agents" ] && files+=(".claude/agents")
    [ -d "$PROJECT_DIR/.claude/skills" ] && files+=(".claude/skills")
    [ -d "$PROJECT_DIR/.claude/hooks" ] && files+=(".claude/hooks")
    [ -d "$PROJECT_DIR/.claude/commands" ] && files+=(".claude/commands")

    mkdir -p "$dist_dir"
    (
        cd "$PROJECT_DIR"
        zip -r "$dist_dir/$package_name" "${files[@]}" \
            -x "*.DS_Store" \
            -x "*/__pycache__/*" \
            -x "*.pyc"
    )

    echo ""
    echo -e "${GREEN}Package created:${NC} $dist_dir/$package_name"
}

create_default_settings() {
    local settings_file="$CLAUDE_DEST/settings.json"

    if [ -f "$settings_file" ]; then
        echo -e "  ${GREEN}✓${NC} settings.json exists (preserving)"
        return
    fi

    cat > "$settings_file" << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
EOF
    echo -e "  ${GREEN}✓${NC} Created $settings_file"
}

print_banner

if [ ! -d "$CLAUDE_SRC" ]; then
    echo -e "${RED}Error:${NC} $CLAUDE_SRC not found"
    exit 1
fi

mkdir -p "$CLAUDE_DEST"

case "$MODE" in
    --link|-l)
        install_mode="link"
        ;;
    --copy|-c)
        install_mode="copy"
        ;;
    --export|-e)
        export_package
        exit 0
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --link, -l    Install with symbolic links"
        echo "  --copy, -c    Install by copying files"
        echo "  --export, -e  Create distribution zip package"
        echo "  --help, -h    Show this help message"
        exit 0
        ;;
    *)
        echo -e "${RED}Unknown option:${NC} $MODE"
        exit 1
        ;;
esac

echo "[1/5] Installing statusline.py..."
cp "$CLAUDE_SRC/statusline.py" "$CLAUDE_DEST/"
chmod +x "$CLAUDE_DEST/statusline.py"
echo -e "      ${GREEN}✓${NC} Copied to $CLAUDE_DEST/statusline.py"

install_dir_component 2 5 "agents" "$CLAUDE_SRC/agents" "$CLAUDE_DEST/agents" "$install_mode" "*.md"
install_dir_component 3 5 "skills" "$CLAUDE_SRC/skills" "$CLAUDE_DEST/skills" "$install_mode" "SKILL.md"
install_dir_component 4 5 "hooks" "$CLAUDE_SRC/hooks" "$CLAUDE_DEST/hooks" "$install_mode" ""
install_dir_component 5 5 "commands" "$CLAUDE_SRC/commands" "$CLAUDE_DEST/commands" "$install_mode" "*.md"

echo ""
echo "Checking settings.json..."
create_default_settings

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}  ${BOLD}✓ Installation Complete!${NC}                                ${GREEN}║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Installed Components:"
echo "  • statusline.py"
echo "  • agents/"
echo "  • skills/"
echo "  • hooks/"
echo "  • commands/"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code to apply changes"
echo "  2. Confirm the status line appears"
