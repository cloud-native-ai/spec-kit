#!/usr/bin/env bash

set -e

# Load common helpers for Unicode support and shared functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/common.sh" ]; then
    # shellcheck source=/dev/null
    source "$SCRIPT_DIR/common.sh"
    # Ensure UTF-8 locale for better Unicode handling
    ensure_utf8_locale || true
fi

# Set root dir
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    ROOT_DIR=$(git rev-parse --show-toplevel)
else
    # Fallback: assume script is in scripts/bash (depth 2)
    ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

SKILLS_DIR="$ROOT_DIR/.github/skills"
JSON_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      JSON_MODE=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Generate tools.md
TOOLS_DOC="$ROOT_DIR/.specify/memory/tools.md"
MCP_SCRIPT="$ROOT_DIR/.specify/scripts/python/list_mcp_tools.py"

# Ensure directory exists
mkdir -p "$(dirname "$TOOLS_DOC")"

# Try to get MCP tools list, default to empty list on failure
if [ -f "$MCP_SCRIPT" ]; then
    # Use the python from the virtualenv if active, or just python3
    MCP_LIST=$(python3 "$MCP_SCRIPT" 2>/dev/null || echo "[]")
else
    MCP_LIST="[]"
fi

if [ -z "$MCP_LIST" ]; then MCP_LIST="[]"; fi

{
    echo "# Helper Tools Index"
    echo "This document indexes available tools for the agent."
    echo ""
    echo "## MCP Tools"
    echo '```json'
    # Format with jq if available, otherwise raw
    if command -v jq >/dev/null 2>&1; then
        echo "$MCP_LIST" | jq '.'
    else
        echo "$MCP_LIST"
    fi
    echo '```'
    echo ""
    echo "## System Binaries"
    echo "Standard executables in PATH (checked via 'command -v' or 'which')."
    echo ""
    echo "## Shell Environment"
    echo "Active environment variables and shell functions."
    echo ""
    echo "## Project Scripts"
    echo "Automation scripts located in the project 'scripts/' directory."
} > "$TOOLS_DOC"

echo "Refreshing skills in $SKILLS_DIR..."

# T008: Create directory if not exists
if [ ! -d "$SKILLS_DIR" ]; then
    mkdir -p "$SKILLS_DIR"
    report_success "Created skills directory at $SKILLS_DIR" "" "$JSON_MODE"
    exit 0
fi

# T009: Scan existing skills
SKILLS_COUNT=0
REFRESHED_COUNT=0
CREATED_COUNT=0

# Iterate into directory
for skill_path in "$SKILLS_DIR"/*; do
    if [ -d "$skill_path" ]; then
        skill_name=$(basename "$skill_path")
        SKILLS_COUNT=$((SKILLS_COUNT + 1))
        
        # T010: Refresh structure
        needs_refresh=false
        
        # Check SKILL.md
        if [ ! -f "$skill_path/SKILL.md" ]; then
            # We can't easily recreate SKILL.md content without a source, so we just warn
            if [ "$JSON_MODE" = false ]; then
                echo "Warning: Skill '$skill_name' is missing SKILL.md" >&2
            fi
        else
             REFRESHED_COUNT=$((REFRESHED_COUNT + 1))
        fi
        
        # Check standard directories (Task T010/T005)
        create_skill_structure "$skill_path"
    fi
done

# T012: Feedback
if [ "$JSON_MODE" = true ]; then
    echo "{\"status\": \"success\", \"message\": \"Skills refreshed\", \"skills_found\": $SKILLS_COUNT, \"skills_refreshed\": $REFRESHED_COUNT}"
else
    echo "Refresh complete."
    echo "Found $SKILLS_COUNT skills."
    echo "Refreshed $REFRESHED_COUNT skills (structure verified)."
fi

