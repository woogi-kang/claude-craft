#!/bin/bash

# claude-craft installer v2.0
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

echo "==================================="
echo "  Claude Craft Installer v2.0"
echo "==================================="
echo ""

# Validate source directory
if [ ! -d "$CLAUDE_SRC" ]; then
    echo "Error: .claude/ directory not found in $PROJECT_DIR"
    exit 1
fi

# Ensure ~/.claude exists
mkdir -p "$CLAUDE_DEST"

case "$MODE" in
    --link|-l)
        echo "Mode: Symbolic Links (development)"
        echo ""

        # 1. Install statusline.py (always copy for execution)
        echo "[1/4] Installing statusline.py..."
        cp "$CLAUDE_SRC/statusline.py" "$CLAUDE_DEST/"
        chmod +x "$CLAUDE_DEST/statusline.py"
        echo "      -> Copied to $CLAUDE_DEST/statusline.py"

        # 2. Link agents directory
        echo "[2/4] Linking agents..."
        if [ -d "$CLAUDE_SRC/agents" ] && [ "$(ls -A $CLAUDE_SRC/agents 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/agents" 2>/dev/null || true
            ln -sf "$CLAUDE_SRC/agents" "$CLAUDE_DEST/agents"
            echo "      -> Linked $CLAUDE_DEST/agents"
            for category_dir in "$CLAUDE_SRC/agents"/*/; do
                if [ -d "$category_dir" ]; then
                    category=$(basename "$category_dir")
                    agent_count=$(find "$category_dir" -maxdepth 1 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
                    echo "         - $category/ ($agent_count agents)"
                fi
            done
        else
            echo "      -> Skipped (no agents found)"
        fi

        # 3. Link skills directory
        echo "[3/4] Linking skills..."
        if [ -d "$CLAUDE_SRC/skills" ] && [ "$(ls -A $CLAUDE_SRC/skills 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/skills" 2>/dev/null || true
            ln -sf "$CLAUDE_SRC/skills" "$CLAUDE_DEST/skills"
            echo "      -> Linked $CLAUDE_DEST/skills"
            for skill_dir in "$CLAUDE_SRC/skills"/*/; do
                if [ -d "$skill_dir" ]; then
                    skill_name=$(basename "$skill_dir")
                    skill_count=$(find "$skill_dir" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
                    echo "         - $skill_name ($skill_count skills)"
                fi
            done
        else
            echo "      -> Skipped (no skills found)"
        fi

        # 4. Link hooks directory
        echo "[4/4] Linking hooks..."
        if [ -d "$CLAUDE_SRC/hooks" ] && [ "$(ls -A $CLAUDE_SRC/hooks 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/hooks" 2>/dev/null || true
            ln -sf "$CLAUDE_SRC/hooks" "$CLAUDE_DEST/hooks"
            echo "      -> Linked $CLAUDE_DEST/hooks"
        else
            echo "      -> Skipped (no hooks found)"
        fi
        ;;

    --copy|-c)
        echo "Mode: Copy Files (standalone install)"
        echo ""

        # 1. Install statusline.py
        echo "[1/4] Copying statusline.py..."
        cp "$CLAUDE_SRC/statusline.py" "$CLAUDE_DEST/"
        chmod +x "$CLAUDE_DEST/statusline.py"
        echo "      -> Copied to $CLAUDE_DEST/statusline.py"

        # 2. Copy agents directory
        echo "[2/4] Copying agents..."
        if [ -d "$CLAUDE_SRC/agents" ] && [ "$(ls -A $CLAUDE_SRC/agents 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/agents" 2>/dev/null || true
            cp -r "$CLAUDE_SRC/agents" "$CLAUDE_DEST/"
            echo "      -> Copied to $CLAUDE_DEST/agents"
        else
            echo "      -> Skipped (no agents found)"
        fi

        # 3. Copy skills directory
        echo "[3/4] Copying skills..."
        if [ -d "$CLAUDE_SRC/skills" ] && [ "$(ls -A $CLAUDE_SRC/skills 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/skills" 2>/dev/null || true
            cp -r "$CLAUDE_SRC/skills" "$CLAUDE_DEST/"
            echo "      -> Copied to $CLAUDE_DEST/skills"
        else
            echo "      -> Skipped (no skills found)"
        fi

        # 4. Copy hooks directory
        echo "[4/4] Copying hooks..."
        if [ -d "$CLAUDE_SRC/hooks" ] && [ "$(ls -A $CLAUDE_SRC/hooks 2>/dev/null)" ]; then
            rm -rf "$CLAUDE_DEST/hooks" 2>/dev/null || true
            cp -r "$CLAUDE_SRC/hooks" "$CLAUDE_DEST/"
            echo "      -> Copied to $CLAUDE_DEST/hooks"
        else
            echo "      -> Skipped (no hooks found)"
        fi
        ;;

    --export|-e)
        echo "Mode: Export Distribution Package"
        echo ""

        DIST_DIR="$PROJECT_DIR/dist"
        mkdir -p "$DIST_DIR"

        TIMESTAMP=$(date +%Y%m%d)
        PACKAGE_NAME="claude-craft-$TIMESTAMP.zip"

        echo "Creating distribution package..."
        cd "$PROJECT_DIR"
        zip -r "$DIST_DIR/$PACKAGE_NAME" .claude/ -x "*.DS_Store"

        echo ""
        echo "Package created: $DIST_DIR/$PACKAGE_NAME"
        echo ""
        echo "To install on another machine:"
        echo "  unzip $PACKAGE_NAME -d ~/.claude/"
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
        exit 0
        ;;

    *)
        echo "Unknown option: $MODE"
        echo "Use --help for usage information"
        exit 1
        ;;
esac

# Configure settings.json
echo ""
echo "Checking settings.json..."
SETTINGS_FILE="$CLAUDE_DEST/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    if grep -q "statusLine" "$SETTINGS_FILE"; then
        echo "  -> statusLine already configured"
    else
        echo "  -> Please add statusLine config to $SETTINGS_FILE"
    fi

    if grep -q "hooks" "$SETTINGS_FILE"; then
        echo "  -> hooks already configured"
    else
        echo "  -> Please add hooks config to $SETTINGS_FILE"
    fi
else
    echo "  -> settings.json not found. Creating with default config..."
    cat > "$SETTINGS_FILE" << 'EOF'
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
    echo "  -> Created $SETTINGS_FILE"
fi

echo ""
echo "==================================="
echo "  Installation Complete!"
echo "==================================="
echo ""
echo "Installed components:"
echo "  - Statusline (cost tracking)"
echo "  - Agents (workflow orchestrators)"
echo "  - Skills (individual capabilities)"
echo "  - Hooks (automation scripts)"
echo ""
echo "Restart Claude Code to apply changes."
