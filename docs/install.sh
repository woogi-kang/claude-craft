#!/bin/bash
# claude-craft Remote Installer v3.0
# MoAI-ADK: 37 Agents, 303 Skills, Hooks, Rules
#
# Usage:
#   curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/master/docs/install.sh | sh
#
# Options (via environment variables):
#   INSTALL_MODE=copy   # copy files instead of symlinks (default: link)
#   INSTALL_DIR=~/dev   # custom installation directory (default: ~/.claude-craft)

set -e

# ═══════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════

REPO_URL="https://github.com/woogi-kang/claude-craft.git"
REPO_NAME="claude-craft"
VERSION="11.1.0"

# Installation directories
INSTALL_DIR="${INSTALL_DIR:-$HOME/.claude-craft}"
CLAUDE_DEST="$HOME/.claude"

# Installation mode: link (default) or copy
INSTALL_MODE="${INSTALL_MODE:-link}"

# ═══════════════════════════════════════════════════════════════════════
# Colors & Formatting
# ═══════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

print_banner() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC}  ${BOLD}Claude Craft Installer v3.0${NC}                             ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     MoAI-ADK: 37 Agents, 303 Skills                        ${CYAN}║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

info() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

success() {
    echo -e "${GREEN}✓${NC}  $1"
}

warn() {
    echo -e "${YELLOW}⚠${NC}  $1"
}

error() {
    echo -e "${RED}✗${NC}  $1"
    exit 1
}

step() {
    echo -e "\n${BOLD}[$1/$2]${NC} $3"
}

# ═══════════════════════════════════════════════════════════════════════
# Platform Detection
# ═══════════════════════════════════════════════════════════════════════

detect_platform() {
    OS="$(uname -s)"
    ARCH="$(uname -m)"

    case "$OS" in
        Linux*)     PLATFORM="linux" ;;
        Darwin*)    PLATFORM="macos" ;;
        CYGWIN*|MINGW*|MSYS*)
            error "Windows is not supported. Please use WSL or Git Bash."
            ;;
        *)
            error "Unsupported operating system: $OS"
            ;;
    esac

    case "$ARCH" in
        x86_64|amd64)   ARCH="x86_64" ;;
        arm64|aarch64)  ARCH="arm64" ;;
        *)
            error "Unsupported architecture: $ARCH"
            ;;
    esac

    info "Detected platform: ${PLATFORM}/${ARCH}"
}

# ═══════════════════════════════════════════════════════════════════════
# Dependency Checks
# ═══════════════════════════════════════════════════════════════════════

check_dependencies() {
    local missing_deps=()

    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        error "Missing required dependencies: ${missing_deps[*]}\nPlease install them and try again."
    fi

    success "All dependencies satisfied"
}

# ═══════════════════════════════════════════════════════════════════════
# Installation Functions
# ═══════════════════════════════════════════════════════════════════════

clone_or_update_repo() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        info "Existing installation found, updating..."
        cd "$INSTALL_DIR"
        git fetch origin
        git reset --hard origin/main 2>/dev/null || git reset --hard origin/master
        success "Repository updated"
    else
        info "Cloning repository to $INSTALL_DIR..."
        rm -rf "$INSTALL_DIR"
        git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
        success "Repository cloned"
    fi
}

install_component() {
    local name="$1"
    local src_path="$2"
    local dest_path="$3"
    local count_pattern="$4"
    local count_name="$5"

    if [ -d "$src_path" ] && [ "$(ls -A $src_path 2>/dev/null)" ]; then
        rm -rf "$dest_path" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$src_path" "$dest_path"
            success "Copied $name"
        else
            ln -sf "$src_path" "$dest_path"
            success "Linked $name"
        fi
        if [ -n "$count_pattern" ]; then
            local count=$(find "$src_path" -name "$count_pattern" 2>/dev/null | wc -l | tr -d ' ')
            info "  → $count $count_name installed"
        fi
        return 0
    else
        warn "Skipped $name (not found)"
        return 1
    fi
}

install_components() {
    local claude_src="$INSTALL_DIR/.claude"

    # Ensure ~/.claude exists
    mkdir -p "$CLAUDE_DEST"

    # 1. Install statusline.py (always copy)
    if [ -f "$claude_src/statusline.py" ]; then
        cp "$claude_src/statusline.py" "$CLAUDE_DEST/"
        chmod +x "$CLAUDE_DEST/statusline.py"
        success "Installed statusline.py"
    fi

    # 2. Install agents (37 total)
    install_component "agents" "$claude_src/agents" "$CLAUDE_DEST/agents" "*.md" "agents"

    # 3. Install skills (303 total)
    install_component "skills" "$claude_src/skills" "$CLAUDE_DEST/skills" "SKILL.md" "skills"

    # 4. Install hooks
    install_component "hooks" "$claude_src/hooks" "$CLAUDE_DEST/hooks" "" ""

    # 5. Install rules (16 languages + core)
    install_component "rules" "$claude_src/rules" "$CLAUDE_DEST/rules" "*.md" "rules"

    # 6. Install commands
    install_component "commands" "$claude_src/commands" "$CLAUDE_DEST/commands" "*.md" "commands"

    # 7. Install output-styles
    install_component "output-styles" "$claude_src/output-styles" "$CLAUDE_DEST/output-styles" "*.md" "output styles"
}

configure_settings() {
    local settings_file="$CLAUDE_DEST/settings.json"

    if [ -f "$settings_file" ]; then
        info "settings.json already exists, preserving..."
    else
        info "Creating default settings.json..."
        cat > "$settings_file" << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
EOF
        success "Created settings.json"
    fi
}

# ═══════════════════════════════════════════════════════════════════════
# Main Installation Flow
# ═══════════════════════════════════════════════════════════════════════

main() {
    print_banner

    step 1 5 "Detecting platform..."
    detect_platform

    step 2 5 "Checking dependencies..."
    check_dependencies

    step 3 5 "Downloading claude-craft..."
    clone_or_update_repo

    step 4 5 "Installing components..."
    install_components

    step 5 5 "Configuring settings..."
    configure_settings

    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}  ${BOLD}✓ Installation Complete!${NC}                                ${GREEN}║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${BOLD}Installed Components:${NC}"
    echo -e "    • agents/       37 AI agents (MoAI + Domain)"
    echo -e "    • skills/       303 skills (52 MoAI + 251 Domain)"
    echo -e "    • hooks/        Automation scripts"
    echo -e "    • rules/        16 language rules + workflows"
    echo -e "    • commands/     Slash commands"
    echo -e "    • output-styles/ Alfred, Yoda, R2D2 styles"
    echo -e "    • statusline.py Real-time cost tracking"
    echo ""
    echo -e "  ${BOLD}Paths:${NC}"
    echo -e "    Installation:   ${CYAN}$INSTALL_DIR${NC}"
    echo -e "    Claude config:  ${CYAN}$CLAUDE_DEST${NC}"
    echo -e "    Install mode:   ${CYAN}$INSTALL_MODE${NC}"
    echo ""
    echo -e "  ${BOLD}Next steps:${NC}"
    echo -e "    1. Restart Claude Code to apply changes"
    echo -e "    2. Try ${CYAN}\"Hello, build me a FastAPI server\"${NC}"
    echo -e "    3. Or use ${CYAN}/moai plan \"your feature\"${NC}"
    echo ""
    echo -e "  ${BOLD}To update:${NC}"
    echo -e "    curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/master/docs/install.sh | sh"
    echo ""
    echo -e "  ${BOLD}To uninstall:${NC}"
    echo -e "    rm -rf ~/.claude/{agents,skills,hooks,rules,commands,output-styles}"
    echo -e "    rm ~/.claude/statusline.py"
    echo -e "    rm -rf $INSTALL_DIR"
    echo ""
}

# Run main
main "$@"
