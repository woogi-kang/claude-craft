#!/bin/bash

# claude-craft installer
# This script sets up Claude Code customizations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "==================================="
echo "  Claude Craft Installer"
echo "==================================="
echo ""

# Ensure ~/.claude exists
mkdir -p "$CLAUDE_DIR"

# 1. Install statusline.py
echo "[1/4] Installing statusline.py..."
cp "$SCRIPT_DIR/statusline/statusline.py" "$CLAUDE_DIR/"
chmod +x "$CLAUDE_DIR/statusline.py"
echo "      -> Copied to $CLAUDE_DIR/statusline.py"

# 2. Link skills directory
echo "[2/4] Linking skills..."
if [ -d "$SCRIPT_DIR/skills" ] && [ "$(ls -A $SCRIPT_DIR/skills 2>/dev/null)" ]; then
    rm -rf "$CLAUDE_DIR/skills" 2>/dev/null || true
    ln -sf "$SCRIPT_DIR/skills" "$CLAUDE_DIR/skills"
    echo "      -> Linked $CLAUDE_DIR/skills"
else
    echo "      -> Skipped (no skills defined yet)"
fi

# 3. Link hooks directory
echo "[3/4] Linking hooks..."
if [ -d "$SCRIPT_DIR/hooks" ] && [ "$(ls -A $SCRIPT_DIR/hooks 2>/dev/null)" ]; then
    rm -rf "$CLAUDE_DIR/hooks" 2>/dev/null || true
    ln -sf "$SCRIPT_DIR/hooks" "$CLAUDE_DIR/hooks"
    echo "      -> Linked $CLAUDE_DIR/hooks"
else
    echo "      -> Skipped (no hooks defined yet)"
fi

# 4. Check settings.json for statusline
echo "[4/4] Checking settings.json..."
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    if grep -q "statusLine" "$SETTINGS_FILE"; then
        echo "      -> statusLine already configured"
    else
        echo "      -> Please add the following to $SETTINGS_FILE:"
        echo ""
        echo '  "statusLine": {'
        echo '    "type": "command",'
        echo '    "command": "python3 ~/.claude/statusline.py"'
        echo '  }'
        echo ""
    fi
else
    echo "      -> settings.json not found. Creating with statusLine config..."
    cat > "$SETTINGS_FILE" << 'EOF'
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
EOF
    echo "      -> Created $SETTINGS_FILE"
fi

echo ""
echo "==================================="
echo "  Installation Complete!"
echo "==================================="
echo ""
echo "Restart Claude Code to apply changes."
