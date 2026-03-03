#!/usr/bin/env bash

# Load common helpers for Unicode support and shared functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/common.sh" ]; then
  # shellcheck source=/dev/null
  source "$SCRIPT_DIR/common.sh"
  # Ensure UTF-8 locale for better Unicode handling
  ensure_utf8_locale || true
else
  echo "Faied to load common.sh, spec-kit framework not installed correctly"
fi

set -e

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

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --mcp)
      QUERY_MCP=true
      shift
      ;;
    --system)
      QUERY_SYSTEM=true
      shift
      ;;
    --shell)
      QUERY_SHELL=true
      shift
      ;;
    --project)
      QUERY_PROJECT=true
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

if [ "$QUERY_MCP" = false ] && [ "$QUERY_SYSTEM" = false ] && [ "$QUERY_SHELL" = false ] && [ "$QUERY_PROJECT" = false ]; then
  QUERY_MCP=true
  QUERY_SYSTEM=true
  QUERY_SHELL=true
  QUERY_PROJECT=true
fi

# Generate tools list script path
MCP_SCRIPT="$ROOT_DIR/.specify/scripts/python/list_mcp_tools.py"
# Fallback to local script if not found in .specify
if [ ! -f "$MCP_SCRIPT" ]; then
  MCP_SCRIPT="$ROOT_DIR/scripts/python/list_mcp_tools.py"
fi

get_mcp_tools_json() {
  if [ -f "$MCP_SCRIPT" ]; then
    python3 "$MCP_SCRIPT" 2>/dev/null || echo "[]"
    return
  fi
  printf '[]'
}

get_system_binaries_json() {
  local os_release=""
  if [ -f /etc/os-release ]; then
    os_release=$(cat /etc/os-release)
  fi
  local kernel
  kernel=$(uname -a)

  local binaries=(git docker kubectl python3 python pip node npm hatch gh jq curl wget make)

  printf '{"os_release":"%s","kernel":"%s","binaries":[' "$(json_escape "$os_release")" "$(json_escape "$kernel")"

  local first=true
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
  printf ']}'
}

get_shell_function_json() {
  local first=true
  printf '['

  while IFS= read -r func; do
    # Filter out functions starting with "_"
    if [[ $func == _* ]]; then
      continue
    fi

    if [ "$first" = true ]; then
      first=false
    else
      printf ','
    fi
    printf '{"name":"%s"}' "$(json_escape "$func")"
  done < <(compgen -A function | sort)
  printf ']'
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
    local description=""

    if [[ $file == *.py ]]; then
      type="python"
      if command -v python3 >/dev/null 2>&1; then
        description=$(python3 -c "import ast; print((ast.get_docstring(ast.parse(open('$file').read())) or '').split('\n')[0])" 2>/dev/null || true)
      fi
    else
      # Get first non-shebang comment
      description=$(grep '^#' "$file" | grep -v '^#!' | head -n 1 | sed 's/^#[[:space:]]*//')
    fi

    # Default description if empty
    if [ -z "$description" ]; then
      description="No description available"
    fi

    if [ "$first" = true ]; then
      first=false
    else
      printf ','
    fi
    printf '{"name":"%s","path":"%s","type":"%s","description":"%s"}' \
      "$(json_escape "$name")" "$(json_escape "$rel_path")" "$(json_escape "$type")" "$(json_escape "$description")"
  done < <(find "$scripts_dir" -type f \( -name "*.sh" -o -name "*.py" \) | sort)
  printf ']'
}

print_mcp_tools_markdown() {
  echo "## MCP Tools"
  if command -v jq >/dev/null 2>&1; then
    get_mcp_tools_json | jq -r '
            def format_args:
                if (.inputSchema and .inputSchema.properties and (.inputSchema.properties | length > 0)) then
                    "\n  - Arguments:\n" +
                    (.inputSchema.properties | to_entries | map("    - `" + .key + "` (" + (.value.type // "any") + ")" + (if .value.description then ": " + .value.description else "" end)) | join("\n"))
                else
                    ""
                end;

            if type=="object" and .servers then
                .servers[] | (
                    "### " + (.name // "Unknown Server") + "\n",
                    (.tools[]? | 
                        "- **" + (.name // "Unknown") + "**: " + (.description // "No description") + format_args
                    )
                )
            else
                .[] | 
                "- **" + (.name // "Unknown") + "**: " + (.description // "No description") + format_args
            end'
  else
    echo '```json'
    get_mcp_tools_json
    echo '```'
  fi
  echo ""
}

print_system_binaries_markdown() {
  echo "## System Information"
  if command -v jq >/dev/null 2>&1; then
    get_system_binaries_json | jq -r '
            if .os_release != "" then
                "### OS Release\n```\n" + .os_release + "\n```\n"
            else "" end,
            "### Kernel\n`" + .kernel + "`\n",
            "### System Binaries\n| Binary | Path |\n|---|---|",
            (.binaries[] | "| " + .name + " | " + .path + " |")
        '
  else
    # Fallback to json dump
    echo '```json'
    get_system_binaries_json
    echo '```'
  fi
  echo ""
}

print_shell_function_markdown() {
  echo "## Shell Functions"
  if command -v jq >/dev/null 2>&1; then
    get_shell_function_json | jq -r '
            if length > 0 then
                "| Function |\n|---|",
                (.[] | "| " + .name + " |")
            else
                "No custom shell functions found."
            end'
  else
    echo '```json'
    get_shell_function_json
    echo '```'
  fi
  echo ""
}

print_unified_json() {
  local mcp_json="[]"
  local system_json='{"binaries":[]}'
  local shell_json="[]"
  local project_json="[]"

  if [ "$QUERY_MCP" = true ]; then
    mcp_json="$(get_mcp_tools_json)"
  fi
  if [ "$QUERY_SYSTEM" = true ]; then
    system_json="$(get_system_binaries_json)"
  fi
  if [ "$QUERY_SHELL" = true ]; then
    shell_json="$(get_shell_function_json)"
  fi
  if [ "$QUERY_PROJECT" = true ]; then
    project_json="$(get_project_scripts_json)"
  fi

MCP_JSON="$mcp_json" SYSTEM_JSON="$system_json" SHELL_JSON="$shell_json" PROJECT_JSON="$project_json" QUERY_MCP="$QUERY_MCP" QUERY_SYSTEM="$QUERY_SYSTEM" QUERY_SHELL="$QUERY_SHELL" QUERY_PROJECT="$QUERY_PROJECT" python3 <<'PY'
import json
import os


def load_json(name, fallback):
    raw = os.environ.get(name, "")
    if not raw:
        return fallback
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return fallback


query_mcp = os.environ.get("QUERY_MCP") == "true"
query_system = os.environ.get("QUERY_SYSTEM") == "true"
query_shell = os.environ.get("QUERY_SHELL") == "true"
query_project = os.environ.get("QUERY_PROJECT") == "true"

mcp = load_json("MCP_JSON", [])
system = load_json("SYSTEM_JSON", {"binaries": []})
shell = load_json("SHELL_JSON", [])
project = load_json("PROJECT_JSON", [])

tools = []

if query_mcp:
    if isinstance(mcp, dict) and isinstance(mcp.get("servers"), list):
        for server in mcp["servers"]:
            source_name = server.get("name", "mcp")
            for tool in server.get("tools", []) or []:
                canonical_name = tool.get("name", "")
                if not canonical_name:
                    continue
                tools.append({
                    "sourceType": "mcp",
                    "sourceName": source_name,
                    "canonicalName": canonical_name,
                    "displayName": canonical_name,
                    "metadata": {
                        "description": tool.get("description", ""),
                        "inputSchema": tool.get("inputSchema", {}),
                    },
                })
    elif isinstance(mcp, list):
        for tool in mcp:
            canonical_name = tool.get("name", "")
            if not canonical_name:
                continue
            tools.append({
                "sourceType": "mcp",
                "sourceName": tool.get("server", "mcp"),
                "canonicalName": canonical_name,
                "displayName": canonical_name,
                "metadata": {
                    "description": tool.get("description", ""),
                    "inputSchema": tool.get("inputSchema", {}),
                },
            })

if query_system:
    for item in system.get("binaries", []):
        canonical_name = item.get("name", "")
        if not canonical_name:
            continue
        tools.append({
            "sourceType": "system",
            "sourceName": "local-system",
            "canonicalName": canonical_name,
            "displayName": canonical_name,
            "metadata": {"path": item.get("path", "")},
        })

if query_shell:
    for item in shell:
        canonical_name = item.get("name", "")
        if not canonical_name:
            continue
        tools.append({
            "sourceType": "shell",
            "sourceName": "current-shell",
            "canonicalName": canonical_name,
            "displayName": canonical_name,
            "metadata": {},
        })

if query_project:
    for item in project:
        canonical_name = item.get("name", "")
        if not canonical_name:
            continue
        tools.append({
            "sourceType": "project",
            "sourceName": "workspace-scripts",
            "canonicalName": canonical_name,
            "displayName": canonical_name,
            "metadata": {
                "path": item.get("path", ""),
                "type": item.get("type", ""),
                "description": item.get("description", ""),
            },
        })

payload = {
    "tools": tools,
    "mcp_tools": mcp if query_mcp else [],
    "system_binaries": system if query_system else {"binaries": []},
    "shell_functions": shell if query_shell else [],
    "project_scripts": project if query_project else [],
}

print(json.dumps(payload, ensure_ascii=False))
PY
}

print_project_scripts_markdown() {
  local json
  json=$(get_project_scripts_json)
  if [ "$json" = "[]" ]; then
    return
  fi

  echo "## Project Scripts"
  if command -v jq >/dev/null 2>&1; then
    echo "$json" | jq -r '
            if length > 0 then
                "| Script | Description | Path | Type |\n|---|---|---|---|",
                (.[] | "| " + .name + " | " + .description + " | " + .path + " | " + .type + " |")
            else
                "No project scripts found."
            end'
  else
    echo '```json'
    echo "$json"
    echo '```'
  fi
  echo ""
}

if [ "$OUTPUT_FORMAT" = "markdown" ]; then
  if [ "$QUERY_MCP" = true ]; then
    print_mcp_tools_markdown
  fi
  if [ "$QUERY_SYSTEM" = true ]; then
    print_system_binaries_markdown
  fi
  if [ "$QUERY_SHELL" = true ]; then
    print_shell_function_markdown
  fi
  if [ "$QUERY_PROJECT" = true ]; then
    print_project_scripts_markdown
  fi
else
  print_unified_json
fi
