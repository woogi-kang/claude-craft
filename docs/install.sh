#!/bin/bash
# claude-craft Remote Installer
#
# Usage:
#   curl -LsSf https://woogi.github.io/claude-craft/install.sh | sh
#   curl -LsSf https://raw.githubusercontent.com/woogi/claude-craft/main/docs/install.sh | sh
#
# Options (via environment variables):
#   INSTALL_MODE=copy   # copy files instead of symlinks (default: link)
#   INSTALL_DIR=~/dev   # custom installation directory (default: ~/.claude-craft)

set -e

# ═══════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════

REPO_URL="https://github.com/woogi/claude-craft.git"
REPO_NAME="claude-craft"
VERSION="latest"

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
    echo -e "${CYAN}║${NC}  ${BOLD}🎩 Claude Craft Installer${NC}                               ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC}     AI-Powered Development Environment                    ${CYAN}║${NC}"
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

    # 2. Install agents
    if [ -d "$claude_src/agents" ] && [ "$(ls -A $claude_src/agents 2>/dev/null)" ]; then
        rm -rf "$CLAUDE_DEST/agents" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$claude_src/agents" "$CLAUDE_DEST/"
            success "Copied agents directory"
        else
            ln -sf "$claude_src/agents" "$CLAUDE_DEST/agents"
            success "Linked agents directory"
        fi
        agent_count=$(find "$claude_src/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        info "  → $agent_count agents installed"
    fi

    # 3. Install skills
    if [ -d "$claude_src/skills" ] && [ "$(ls -A $claude_src/skills 2>/dev/null)" ]; then
        rm -rf "$CLAUDE_DEST/skills" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$claude_src/skills" "$CLAUDE_DEST/"
            success "Copied skills directory"
        else
            ln -sf "$claude_src/skills" "$CLAUDE_DEST/skills"
            success "Linked skills directory"
        fi
        skill_count=$(find "$claude_src/skills" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
        info "  → $skill_count skills installed"
    fi

    # 4. Install hooks
    if [ -d "$claude_src/hooks" ] && [ "$(ls -A $claude_src/hooks 2>/dev/null)" ]; then
        rm -rf "$CLAUDE_DEST/hooks" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$claude_src/hooks" "$CLAUDE_DEST/"
            success "Copied hooks directory"
        else
            ln -sf "$claude_src/hooks" "$CLAUDE_DEST/hooks"
            success "Linked hooks directory"
        fi
    fi

    # 5. Install commands
    if [ -d "$claude_src/commands" ] && [ "$(ls -A $claude_src/commands 2>/dev/null)" ]; then
        rm -rf "$CLAUDE_DEST/commands" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$claude_src/commands" "$CLAUDE_DEST/"
            success "Copied commands directory"
        else
            ln -sf "$claude_src/commands" "$CLAUDE_DEST/commands"
            success "Linked commands directory"
        fi
    fi

    # 6. Install output-styles
    if [ -d "$claude_src/output-styles" ] && [ "$(ls -A $claude_src/output-styles 2>/dev/null)" ]; then
        rm -rf "$CLAUDE_DEST/output-styles" 2>/dev/null || true
        if [ "$INSTALL_MODE" = "copy" ]; then
            cp -r "$claude_src/output-styles" "$CLAUDE_DEST/"
            success "Copied output-styles directory"
        else
            ln -sf "$claude_src/output-styles" "$CLAUDE_DEST/output-styles"
            success "Linked output-styles directory"
        fi
        style_count=$(find "$claude_src/output-styles" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        info "  → $style_count output styles installed"
    fi
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
  },
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
    echo -e "  Installation directory: ${CYAN}$INSTALL_DIR${NC}"
    echo -e "  Claude config:          ${CYAN}$CLAUDE_DEST${NC}"
    echo -e "  Install mode:           ${CYAN}$INSTALL_MODE${NC}"
    echo ""
    echo -e "  ${BOLD}Next steps:${NC}"
    echo -e "    1. Restart Claude Code to apply changes"
    echo -e "    2. Try ${CYAN}/moai:alfred \"hello world\"${NC} to test"
    echo ""
    echo -e "  ${BOLD}To update:${NC}"
    echo -e "    curl -LsSf https://woogi.github.io/claude-craft/install.sh | sh"
    echo ""
    echo -e "  ${BOLD}To uninstall:${NC}"
    echo -e "    rm -rf $INSTALL_DIR"
    echo -e "    rm -rf $CLAUDE_DEST/{agents,skills,hooks,commands}"
    echo ""
}

# Run main
main "$@"
