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

# Read from stdin if available and no description provided (or append to it)
if [ ! -t 0 ]; then
    STDIN_CONTENT=$(cat)
    if [ -n "$STDIN_CONTENT" ]; then
        if [ -n "$DESCRIPTION" ]; then
            DESCRIPTION="$DESCRIPTION $STDIN_CONTENT"
        else
            DESCRIPTION="$STDIN_CONTENT"
        fi
    fi
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

# Create SKILL.md if it doesn't exist
if [ ! -f "$SKILL_FILE" ]; then
    cat <<EOF > "$SKILL_FILE"
---
name: $SKILL_NAME
description: |
  $DESCRIPTION
---

# $SKILL_NAME

## Overview
Briefly describe what this skill does. (Conciseness is key!)

## Workflow / Instructions
1. Step 1
2. Step 2
...

## Available Tools & Resources

### Scripts (\`./scripts/\`)
- No scripts currently. (Add executable scripts here for deterministic tasks)

### References (\`./references/\`)
- No references currently. (Add documentation/schemas here to be loaded on-demand)

### Assets (\`./assets/\`)
- No assets currently. (Add output templates/files here)

EOF
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
