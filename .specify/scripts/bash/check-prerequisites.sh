#!/usr/bin/env bash

# Consolidated prerequisite checking script
#
# This script provides unified prerequisite checking for Spec-Driven Development workflow.
# It replaces the functionality previously spread across multiple scripts.
#
# Usage: ./check-prerequisites.sh [OPTIONS]
#
# OPTIONS:
#   --json              Output in JSON format
#   --require-spec      Require requirements.md to exist (for review/spec phases)
#   --include-spec      Include requirements.md in AVAILABLE_DOCS list
#   --include-plan      Include plan.md in AVAILABLE_DOCS list
#   --require-tasks     Require tasks.md to exist (for implementation phase)
#   --include-tasks     Include tasks.md in AVAILABLE_DOCS list
#   --paths-only        Only output path variables (no validation)
#   --help, -h          Show help message
#
# OUTPUTS:
#   JSON mode: {"REQUIREMENTS_DIR":"...", "FEATURE_ID":"...", "FEATURE_NAME":"...", "AVAILABLE_DOCS":["..."]}
#   Text mode: REQUIREMENTS_DIR:... \n AVAILABLE_DOCS: \n ✓/✗ file.md
#   Paths only: REPO_ROOT: ... \n BRANCH: ... \n REQUIREMENTS_DIR: ... etc.

set -e

# Parse command line arguments
JSON_MODE=false
REQUIRE_SPEC=false
INCLUDE_SPEC=false
INCLUDE_PLAN=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false
PATHS_ONLY=false

for arg in "$@"; do
    case "$arg" in
        --json)
            JSON_MODE=true
            ;;
        --require-spec)
            REQUIRE_SPEC=true
            ;;
        --include-spec)
            INCLUDE_SPEC=true
            ;;
        --include-plan)
            INCLUDE_PLAN=true
            ;;
        --require-tasks)
            REQUIRE_TASKS=true
            ;;
        --include-tasks)
            INCLUDE_TASKS=true
            ;;
        --paths-only)
            PATHS_ONLY=true
            ;;
        --help|-h)
            cat << 'EOF'
Usage: check-prerequisites.sh [OPTIONS]

Consolidated prerequisite checking for Spec-Driven Development workflow.

OPTIONS:
  --json              Output in JSON format
    --require-spec      Require requirements.md to exist (for review/spec phases)
    --include-spec      Include requirements.md in AVAILABLE_DOCS list
    --include-plan      Include plan.md in AVAILABLE_DOCS list
  --require-tasks     Require tasks.md to exist (for implementation phase)
  --include-tasks     Include tasks.md in AVAILABLE_DOCS list
  --paths-only        Only output path variables (no prerequisite validation)
  --help, -h          Show this help message

EXAMPLES:
  # Check task prerequisites (plan.md required)
  ./check-prerequisites.sh --json
  
  # Check implementation prerequisites (plan.md + tasks.md required)
  ./check-prerequisites.sh --json --require-tasks --include-tasks

    # Check review prerequisites (requirements.md + plan.md + tasks.md)
    ./check-prerequisites.sh --json --require-spec --include-spec --include-plan --include-tasks
  
  # Get feature paths only (no validation)
  ./check-prerequisites.sh --paths-only
  
EOF
            exit 0
            ;;
        *)
            echo "ERROR: Unknown option '$arg'. Use --help for usage information." >&2
            exit 1
            ;;
    esac
done

# Source common functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get feature paths and validate branch
eval $(get_feature_paths)
check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

# Normalize canonical naming used by current SDD prompts.
REQUIREMENTS_DIR="${REQUIREMENTS_DIR:-$FEATURE_DIR}"

# Extract REQUIREMENT_ID from branch name (requirement/spec key, not Feature ID).
REQUIREMENT_ID=""
if [[ "$CURRENT_BRANCH" =~ ^([0-9]+)- ]]; then
    REQUIREMENT_ID="${BASH_REMATCH[1]}"
fi

# Extract Feature metadata from requirements.md when available.
FEATURE_ID=""
FEATURE_NAME=""
if [[ -f "$FEATURE_SPEC" ]]; then
    FEATURE_ID=$(sed -n 's/^\*\*Feature ID\*\*:[[:space:]]*\([0-9][0-9][0-9]\).*/\1/p' "$FEATURE_SPEC" | head -n 1)
    FEATURE_NAME=$(sed -n 's/^\*\*Feature Name\*\*:[[:space:]]*//p' "$FEATURE_SPEC" | head -n 1)
fi

# If paths-only mode, output paths and exit (support JSON + paths-only combined)
if $PATHS_ONLY; then
    if $JSON_MODE; then
        # Minimal JSON paths payload (no validation performed)
        printf '{"REPO_ROOT":"%s","BRANCH":"%s","REQUIREMENT_ID":"%s","REQUIREMENTS_DIR":"%s","FEATURE_DIR":"%s","FEATURE_ID":"%s","FEATURE_NAME":"%s","FEATURE_SPEC":"%s","IMPL_PLAN":"%s","TASKS":"%s"}\n' \
            "$REPO_ROOT" "$CURRENT_BRANCH" "$REQUIREMENT_ID" "$REQUIREMENTS_DIR" "$FEATURE_DIR" "$FEATURE_ID" "$FEATURE_NAME" "$FEATURE_SPEC" "$IMPL_PLAN" "$TASKS"
    else
        echo "REPO_ROOT: $REPO_ROOT"
        echo "BRANCH: $CURRENT_BRANCH"
        echo "REQUIREMENT_ID: $REQUIREMENT_ID"
        echo "REQUIREMENTS_DIR: $REQUIREMENTS_DIR"
        echo "FEATURE_DIR: $FEATURE_DIR"
        echo "FEATURE_ID: $FEATURE_ID"
        echo "FEATURE_NAME: $FEATURE_NAME"
        echo "FEATURE_SPEC: $FEATURE_SPEC"
        echo "IMPL_PLAN: $IMPL_PLAN"
        echo "TASKS: $TASKS"
    fi
    exit 0
fi

# Validate required directories and files
if [[ ! -d "$REQUIREMENTS_DIR" ]]; then
    echo "ERROR: Feature directory not found: $REQUIREMENTS_DIR" >&2
    echo "Run /speckit.specify first to create the feature structure." >&2
    exit 1
fi

if $REQUIRE_SPEC && [[ ! -f "$FEATURE_SPEC" ]]; then
    echo "ERROR: requirements.md not found in $REQUIREMENTS_DIR" >&2
    echo "Run /speckit.requirements first to create the specification." >&2
    exit 1
fi

if [[ ! -f "$IMPL_PLAN" ]]; then
    echo "ERROR: plan.md not found in $REQUIREMENTS_DIR" >&2
    echo "Run /speckit.plan first to create the implementation plan." >&2
    exit 1
fi

# Check for tasks.md if required
if $REQUIRE_TASKS && [[ ! -f "$TASKS" ]]; then
    echo "ERROR: tasks.md not found in $REQUIREMENTS_DIR" >&2
    echo "Run /speckit.tasks first to create the task list." >&2
    exit 1
fi

# Build list of available documents
docs=()

if $INCLUDE_SPEC && [[ -f "$FEATURE_SPEC" ]]; then
    docs+=("requirements.md")
fi

if $INCLUDE_PLAN && [[ -f "$IMPL_PLAN" ]]; then
    docs+=("plan.md")
fi

# Always check these optional docs
[[ -f "$RESEARCH" ]] && docs+=("research.md")
[[ -f "$DATA_MODEL" ]] && docs+=("data-model.md")

# Check contracts directory (only if it exists and has files)
if [[ -d "$CONTRACTS_DIR" ]] && [[ -n "$(ls -A "$CONTRACTS_DIR" 2>/dev/null)" ]]; then
    docs+=("contracts/")
fi

[[ -f "$QUICKSTART" ]] && docs+=("quickstart.md")

# Include tasks.md if requested and it exists
if $INCLUDE_TASKS && [[ -f "$TASKS" ]]; then
    docs+=("tasks.md")
fi

# Output results
if $JSON_MODE; then
    # Build JSON array of documents
    if [[ ${#docs[@]} -eq 0 ]]; then
        json_docs="[]"
    else
        json_docs=$(printf '"%s",' "${docs[@]}")
        json_docs="[${json_docs%,}]"
    fi
    
    printf '{"REQUIREMENTS_DIR":"%s","FEATURE_DIR":"%s","REQUIREMENT_ID":"%s","FEATURE_ID":"%s","FEATURE_NAME":"%s","AVAILABLE_DOCS":%s}\n' \
        "$REQUIREMENTS_DIR" "$FEATURE_DIR" "$REQUIREMENT_ID" "$FEATURE_ID" "$FEATURE_NAME" "$json_docs"
else
    # Text output
    echo "REQUIREMENTS_DIR:$REQUIREMENTS_DIR"
    echo "FEATURE_DIR:$FEATURE_DIR"
    echo "REQUIREMENT_ID:$REQUIREMENT_ID"
    echo "FEATURE_ID:$FEATURE_ID"
    echo "FEATURE_NAME:$FEATURE_NAME"
    echo "AVAILABLE_DOCS:"
    
    # Show status of each potential document
    if $INCLUDE_SPEC; then
        check_file "$FEATURE_SPEC" "requirements.md"
    fi
    if $INCLUDE_PLAN; then
        check_file "$IMPL_PLAN" "plan.md"
    fi
    check_file "$RESEARCH" "research.md"
    check_file "$DATA_MODEL" "data-model.md"
    check_dir "$CONTRACTS_DIR" "contracts/"
    check_file "$QUICKSTART" "quickstart.md"
    
    if $INCLUDE_TASKS; then
        check_file "$TASKS" "tasks.md"
    fi
fi