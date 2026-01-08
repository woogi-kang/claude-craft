#!/bin/bash

# sync-docs.sh
# Automatically scans agents/skills directories and reports structure
#
# This script scans the .claude/agents/ and .claude/skills/ directories
# and outputs the current structure.

set -e

# Get the hooks directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Try to find the .claude directory (could be in ~/.claude or project/.claude)
if [[ "$SCRIPT_DIR" == *"/.claude/hooks" ]]; then
    # We're inside a .claude directory
    CLAUDE_DIR="$(dirname "$SCRIPT_DIR")"
else
    # Fallback to home directory
    CLAUDE_DIR="$HOME/.claude"
fi

AGENTS_DIR="$CLAUDE_DIR/agents"
SKILLS_DIR="$CLAUDE_DIR/skills"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}[sync-docs]${NC} Scanning agents and skills..."

# Function to count skills in a directory
count_skills() {
    local dir="$1"
    find "$dir" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' '
}

# Function to get agent description from AGENT.md
get_agent_description() {
    local agent_file="$1"
    if [ -f "$agent_file" ]; then
        # Extract description from YAML frontmatter
        sed -n '/^description:/,/^[a-z]*:/p' "$agent_file" | head -n 2 | tail -n 1 | sed 's/^[[:space:]]*//'
    fi
}

# Check if directories exist
if [ ! -d "$AGENTS_DIR" ]; then
    echo -e "${YELLOW}[sync-docs]${NC} No agents directory found at $AGENTS_DIR"
    exit 0
fi

# Gather agent information
echo -e "${GREEN}[sync-docs]${NC} Found agents:"
for agent_dir in "$AGENTS_DIR"/*/; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename "$agent_dir")
        agent_file="$agent_dir/AGENT.md"

        # Find corresponding skills directory
        skills_dir_name="${agent_name}-skills"
        skills_path="$SKILLS_DIR/$skills_dir_name"

        if [ -d "$skills_path" ]; then
            skill_count=$(count_skills "$skills_path")
        else
            skill_count=0
        fi

        # Get description
        if [ -f "$agent_file" ]; then
            desc=$(get_agent_description "$agent_file")
        else
            desc="No description"
        fi

        echo -e "  - ${YELLOW}$agent_name${NC} ($skill_count skills)"
    fi
done

# Gather skills information
if [ -d "$SKILLS_DIR" ]; then
    echo -e "${GREEN}[sync-docs]${NC} Found skill sets:"
    for skill_dir in "$SKILLS_DIR"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_set_name=$(basename "$skill_dir")
            skill_count=$(count_skills "$skill_dir")
            echo -e "  - ${YELLOW}$skill_set_name${NC} ($skill_count skills)"
        fi
    done
fi

echo -e "${GREEN}[sync-docs]${NC} Documentation sync complete!"
echo ""
echo "Summary:"
echo "  Agents: $(ls -d "$AGENTS_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')"
echo "  Skill Sets: $(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l | tr -d ' ')"
