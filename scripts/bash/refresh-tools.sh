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
    # Fallback: check if we are in .specify/scripts/bash (depth 3) or scripts/bash (depth 2)
    case "$SCRIPT_DIR" in
        */.specify/scripts/bash)
            ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
            ;;
        *)
            ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
            ;;
    esac
fi

SKILLS_DIR="$ROOT_DIR/.github/skills"
JSON_MODE=false

# Query mode flags
QUERY_MCP=false
QUERY_SYSTEM=false
QUERY_SHELL=false
QUERY_PROJECT=false
OUTPUT_FORMAT="json"
IS_QUERY_MODE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --mcp)
      QUERY_MCP=true
      IS_QUERY_MODE=true
      shift
      ;;
    --system)
      QUERY_SYSTEM=true
      IS_QUERY_MODE=true
      shift
      ;;
    --shell)
      QUERY_SHELL=true
      IS_QUERY_MODE=true
      shift
      ;;
    --project)
      QUERY_PROJECT=true
      IS_QUERY_MODE=true
      shift
      ;;
    --format)
      OUTPUT_FORMAT="$2"
      shift 2
      ;;
    --json)
      JSON_MODE=true
      OUTPUT_FORMAT="json"
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Shared paths
TOOLS_DOC="$ROOT_DIR/.specify/memory/tools.md"

json_escape() {
    local value="$1"
    value=${value//\\/\\\\}
    value=${value//"/\\"}
    value=${value//$'\n'/\\n}
    value=${value//$'\r'/\\r}
    value=${value//$'\t'/\\t}
    printf '%s' "$value"
}

get_mcp_tools_json() {
    if [ -f "$TOOLS_DOC" ]; then
        local json
        json=$(awk '
            BEGIN { in_section=0; in_block=0 }
            /^## MCP Tools/ { in_section=1 }
            in_section && /^```json/ { in_block=1; next }
            in_block && /^```/ { exit }
            in_block { print }
        ' "$TOOLS_DOC")
        if [ -n "$json" ]; then
            printf '%s' "$json"
            return
        fi
    fi
    printf '[]'
}

get_system_binaries_json() {
    local binaries=(git docker kubectl python3 python pip node npm hatch gh jq curl wget make)
    local first=true
    printf '['
    for b in "${binaries[@]}"; do
        local path
        path=$(command -v "$b" 2>/dev/null || true)
        if [ -n "$path" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '{"name":"%s","path":"%s"}' "$(json_escape "$b")" "$(json_escape "$path")"
        fi
    done
    printf ']'
}

get_shell_env_json() {
    local keys=(SHELL TERM USER LANG PWD VIRTUAL_ENV SSH_CONNECTION EDITOR VISUAL)
    local first=true
    printf '{'
    for k in "${keys[@]}"; do
        local value="${!k-}"
        if [ -n "$value" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '"%s":"%s"' "$(json_escape "$k")" "$(json_escape "$value")"
        fi
    done
    printf '}'
}

get_project_scripts_json() {
    local scripts_dir=""
    if [ -d "$ROOT_DIR/.specify/scripts" ]; then
        scripts_dir="$ROOT_DIR/.specify/scripts"
    elif [ -d "$ROOT_DIR/scripts" ]; then
        scripts_dir="$ROOT_DIR/scripts"
    else
        printf '[]'
        return
    fi

    local first=true
    printf '['
    while IFS= read -r file; do
        local rel_path="${file#$ROOT_DIR/}"
        local name
        name=$(basename "$file")
        local type="bash"
        if [[ "$file" == *.py ]]; then
            type="python"
        fi
        if [ "$first" = true ]; then
            first=false
        else
            printf ','
        fi
        printf '{"name":"%s","path":"%s","type":"%s"}' \
            "$(json_escape "$name")" "$(json_escape "$rel_path")" "$(json_escape "$type")"
    done < <(find "$scripts_dir" -type f \( -name "*.sh" -o -name "*.py" \) | sort)
    printf ']'
}

print_mcp_tools_markdown() {
    local json
    json=$(get_mcp_tools_json)
    echo "## MCP Tools"
    if command -v jq >/dev/null 2>&1; then
        echo "$json" | jq -r '.[] | "- **\(.name // \"Unknown\")**: \(.description // \"No description\")"'
    else
        echo '```json'
        echo "$json"
        echo '```'
    fi
    echo ""
}

print_system_binaries_markdown() {
    local binaries=(git docker kubectl python3 python pip node npm hatch gh jq curl wget make)
    echo "## System Binaries"
    echo "| Binary | Path |"
    echo "|---|---|"
    for b in "${binaries[@]}"; do
        local path
        path=$(command -v "$b" 2>/dev/null || true)
        if [ -n "$path" ]; then
            echo "| $b | $path |"
        fi
    done
    echo ""
}

print_shell_env_markdown() {
    local keys=(SHELL TERM USER LANG PWD VIRTUAL_ENV SSH_CONNECTION EDITOR VISUAL)
    echo "## Shell Environment"
    for k in "${keys[@]}"; do
        local value="${!k-}"
        if [ -n "$value" ]; then
            echo "- **$k**: \`$value\`"
        fi
    done
    echo ""
}

print_project_scripts_markdown() {
    local scripts_dir=""
    if [ -d "$ROOT_DIR/.specify/scripts" ]; then
        scripts_dir="$ROOT_DIR/.specify/scripts"
    elif [ -d "$ROOT_DIR/scripts" ]; then
        scripts_dir="$ROOT_DIR/scripts"
    else
        return
    fi

    echo "## Project Scripts"
    echo "| Script | Path | Type |"
    echo "|---|---|---|"
    while IFS= read -r file; do
        local rel_path="${file#$ROOT_DIR/}"
        local name
        name=$(basename "$file")
        local type="bash"
        if [[ "$file" == *.py ]]; then
            type="python"
        fi
        echo "| $name | $rel_path | $type |"
    done < <(find "$scripts_dir" -type f \( -name "*.sh" -o -name "*.py" \) | sort)
    echo ""
}

# If in query mode, handle directly in shell and exit
if [ "$IS_QUERY_MODE" = true ]; then
    if [ "$OUTPUT_FORMAT" = "markdown" ]; then
        if [ "$QUERY_MCP" = true ]; then
            print_mcp_tools_markdown
        fi
        if [ "$QUERY_SYSTEM" = true ]; then
            print_system_binaries_markdown
        fi
        if [ "$QUERY_SHELL" = true ]; then
            print_shell_env_markdown
        fi
        if [ "$QUERY_PROJECT" = true ]; then
            print_project_scripts_markdown
        fi
    else
        first=true
        printf '{'
        if [ "$QUERY_MCP" = true ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '"mcp_tools":%s' "$(get_mcp_tools_json)"
        fi
        if [ "$QUERY_SYSTEM" = true ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '"system_binaries":%s' "$(get_system_binaries_json)"
        fi
        if [ "$QUERY_SHELL" = true ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '"shell_environment":%s' "$(get_shell_env_json)"
        fi
        if [ "$QUERY_PROJECT" = true ]; then
            if [ "$first" = true ]; then
                first=false
            else
                printf ','
            fi
            printf '"project_scripts":%s' "$(get_project_scripts_json)"
        fi
        printf '}'
    fi
    exit 0
fi

# Generate tools.md
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

