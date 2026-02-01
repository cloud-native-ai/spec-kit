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

CUSTOM_OUTPUT_DIR=""

# Check for "Name - Description" format in first argument if it's not a flag
if [[ "$1" != -* ]] && [[ "$1" == *" - "* ]]; then
    # Extract name and description
    SKILL_NAME="${1%% - *}"
    DESCRIPTION="${1#* - }"
    shift
fi

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
    --description|--desc|-d)
      DESCRIPTION="$2"
      shift
      shift
      ;;
    --output-dir|-o)
      CUSTOM_OUTPUT_DIR="$2"
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
    report_error "Skill name is required. Use --name <name> or 'speckit.skills name - desc'" "$JSON_MODE"
    exit 1
fi

# Validate name
if ! validate_skill_name "$SKILL_NAME"; then
    report_error "Invalid skill name '$SKILL_NAME'. Use alphanumeric, hyphens, underscores only." "$JSON_MODE"
    exit 1
fi

# Default description if empty
if [ -z "$DESCRIPTION" ]; then
    DESCRIPTION="Skill for $SKILL_NAME"
fi

# Set root dir
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    ROOT_DIR=$(git rev-parse --show-toplevel)
else
    # Fallback: assume script is in scripts/bash (depth 2)
    ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
fi

# Determine target directory
if [ -n "$CUSTOM_OUTPUT_DIR" ]; then
    SKILLS_DIR="$CUSTOM_OUTPUT_DIR"
else
    SKILLS_DIR="$ROOT_DIR/.github/skills"
fi

TARGET_DIR="$SKILLS_DIR/$SKILL_NAME"
SKILL_FILE="$TARGET_DIR/SKILL.md"

# Check if already exists
if [ -d "$TARGET_DIR" ]; then
    report_error "Skill directory already exists at $TARGET_DIR" "$JSON_MODE"
    exit 1
fi

# Create directory structure
create_skill_structure "$TARGET_DIR"

# Detect template path
if [ -f "$ROOT_DIR/.specify/templates/skills-template.md" ]; then
    TEMPLATE_FILE="$ROOT_DIR/.specify/templates/skills-template.md"
elif [ -f "$ROOT_DIR/templates/skills-template.md" ]; then
    TEMPLATE_FILE="$ROOT_DIR/templates/skills-template.md"
else
    # Fallback default
    TEMPLATE_FILE="$ROOT_DIR/templates/skills-template.md"
fi

# Define fallback template content
FALLBACK_TEMPLATE='---
name: {{SKILL_NAME}}
description: |
  {{DESCRIPTION}}
---

# {{SKILL_NAME}}

## Overview
{{DESCRIPTION}}

## Workflow / Instructions
1. [Step 1]
2. [Step 2]

## Available Tools & Resources

### Scripts (`./scripts/`)
- [Add scripts here]

### References (`./references/`)
- [Add references here]

### Assets (`./assets/`)
- [Add assets here]
'

# Create SKILL.md
if [ -f "$TEMPLATE_FILE" ]; then
    TEMPLATE_CONTENT=$(cat "$TEMPLATE_FILE")
else
    echo "Warning: Template file not found at $TEMPLATE_FILE. Using built-in fallback." >&2
    TEMPLATE_CONTENT="$FALLBACK_TEMPLATE"
fi

export TEMPLATE_CONTENT
# Use python for safe string replacement
python3 -c "import os, sys; content = os.environ.get('TEMPLATE_CONTENT', ''); print(content.replace('{{SKILL_NAME}}', sys.argv[1]).replace('{{DESCRIPTION}}', sys.argv[2]))" "$SKILL_NAME" "$DESCRIPTION" > "$SKILL_FILE"

if [ "$JSON_MODE" = true ]; then
    # Output JSON
    report_success "Skill created" "\"SKILL_DIR\": \"$TARGET_DIR\", \"SKILL_FILE\": \"$SKILL_FILE\", \"SKILL_NAME\": \"$SKILL_NAME\", \"CREATED\": true" "true"
else
    echo "Skill created at: $SKILL_FILE"
    echo "  ├── SKILL.md"
    echo "  ├── scripts/"
    echo "  ├── references/"
    echo "  └── assets/"
fi
