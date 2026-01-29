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

# Fallback: if common.sh wasn't sourced or locale still isn't UTF-8, set a UTF-8 locale
if ! locale 2>/dev/null | grep -qi 'utf-8'; then
    if locale -a 2>/dev/null | grep -qi '^C\.utf8\|^C\.UTF-8$'; then
        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
    elif locale -a 2>/dev/null | grep -qi '^en_US\.utf8\|^en_US\.UTF-8$'; then
        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8
    fi
fi

JSON_MODE=false
SKILL_NAME=""
DESCRIPTION=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --json)
      JSON_MODE=true
      shift
      ;;
    --name)
      SKILL_NAME="$2"
      shift
      shift
      ;;
    --description)
      DESCRIPTION="$2"
      shift
      shift
      ;;
    *)
      # Accumulate other args as description if not set
      if [ -z "$DESCRIPTION" ]; then
          DESCRIPTION="$1"
      else
          DESCRIPTION="$DESCRIPTION $1"
      fi
      shift
      ;;
  esac
done

# Read from stdin if available, regardless of arguments
STDIN_INPUT=""
if [ ! -t 0 ]; then
    STDIN_INPUT=$(cat)
fi

# Combine arguments and stdin
if [ -n "$DESCRIPTION" ] && [ -n "$STDIN_INPUT" ]; then
    # Both provided: use newline separator
    DESCRIPTION="$DESCRIPTION"$'\n\n'"$STDIN_INPUT"
elif [ -z "$DESCRIPTION" ] && [ -n "$STDIN_INPUT" ]; then
    # Only stdin provided
    DESCRIPTION="$STDIN_INPUT"
fi

# Validate inputs
if [ -z "$SKILL_NAME" ]; then
    echo "Error: Skill name is required. Use --name <name>" >&2
    exit 1
fi

# Default description if empty
if [ -z "$DESCRIPTION" ]; then
    DESCRIPTION="Skill for $SKILL_NAME"
fi

# Set root dir (assuming script is in .specify/scripts/bash)
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SKILLS_DIR="$ROOT_DIR/.github/skills"
TARGET_DIR="$SKILLS_DIR/$SKILL_NAME"
SKILL_FILE="$TARGET_DIR/SKILL.md"

# Create directory structure
mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/scripts"
mkdir -p "$TARGET_DIR/references"
mkdir -p "$TARGET_DIR/assets"

TEMPLATE_FILE="$ROOT_DIR/templates/skills-template.md"

# Create SKILL.md if it doesn't exist
if [ ! -f "$SKILL_FILE" ]; then
    if [ -f "$TEMPLATE_FILE" ]; then
        python3 -c "import sys; from pathlib import Path; template = Path(sys.argv[1]).read_text(encoding='utf-8'); content = template.replace('{{SKILL_NAME}}', sys.argv[2]).replace('{{DESCRIPTION}}', sys.argv[3]); sys.stdout.buffer.write(content.encode('utf-8'))" "$TEMPLATE_FILE" "$SKILL_NAME" "$DESCRIPTION" > "$SKILL_FILE"
    else
        echo "Error: Template file not found at $TEMPLATE_FILE" >&2
        exit 1
    fi
fi

if [ "$JSON_MODE" = true ]; then
    # Output JSON
    # Simple JSON construction
    echo "{"
    echo "  \"SKILL_DIR\": \"$TARGET_DIR\","
    echo "  \"SKILL_FILE\": \"$SKILL_FILE\","
    echo "  \"SKILL_NAME\": \"$SKILL_NAME\","
    echo "  \"CREATED\": true"
    echo "}"
else
    echo "Skill created at: $SKILL_FILE"
fi
