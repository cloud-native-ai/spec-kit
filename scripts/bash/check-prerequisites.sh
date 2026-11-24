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
#   --require-tasks     Require tasks.md to exist (for implementation phase)
#   --include-tasks     Include tasks.md in AVAILABLE_DOCS list
#   --paths-only        Only output path variables (no validation)
#   --help, -h          Show help message
#
# OUTPUTS:
#   JSON mode: {"REQUIREMENTS_DIR":"...", "FEATURE_ID":"...", "FEATURE_NAME":"...", "AVAILABLE_DOCS":["..."], "MODE":"A|B|C|NONE", "WRITABLE":true|false}
#     MODE     — phase detected from file existence: A = requirements only
#                (plan.md missing), B = plan.md exists (tasks.md missing),
#                C = tasks.md exists, NONE = requirements.md missing.
#     WRITABLE — write-bit probe: feature dir AND the mode's target artifact
#                accept writes (false e.g. on root-owned spec dirs).
#   Text mode: REQUIREMENTS_DIR:... \n AVAILABLE_DOCS: \n ✓/✗ file.md
#   Paths only: REPO_ROOT: ... \n BRANCH: ... \n REQUIREMENTS_DIR: ... etc.

set -e

# Load common helpers for Unicode support and shared functions

# script-interface: the sourceable guard block (086) lives in script-interface.sh
# It sits above this script's own parsing and above `source common.sh`: a shared
# library's top-level checks would otherwise turn `--help` into a non-zero exit, and
# the flags must win over any write. Authority: shared/definitions/
# script-interface-definitions.md section 4.
SCRIPT_INTERFACE_LIB="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/script-interface.sh"
if [ -f "$SCRIPT_INTERFACE_LIB" ]; then
    # shellcheck source=/dev/null
    . "$SCRIPT_INTERFACE_LIB"
    script_interface_guard entry
    script_interface_guard define name="$0" \
        usage="[--json] [--require-tasks] [--include-tasks] [--require-spec] [--include-spec] [--include-plan] [--paths-only]" \
        effects="reads the feature tree and prints a prerequisite report; writes nothing" \
        codes="0 prerequisites satisfied; 1 a prerequisite is missing; 2 an unrecognized option" \
        writes=--paths-only \
        -- --json --require-tasks --include-tasks --require-spec --include-spec --include-plan --paths-only
    script_interface_guard guard "$@"
fi

main() {

    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/common.sh" ]; then
        # shellcheck source=/dev/null
        source "$SCRIPT_DIR/common.sh"

        # Host-library fallbacks (backlog F1, 2026-11-23). When CWS_LIB_BASH_HOME is
        # unset, common.sh's library-link publishes no host helpers; the --json path
        # still needs these four. They are defined only when the host did not publish
        # a function of the same name, so the host library remains the owner when
        # present. The escaper mirrors the scaffold-path precedent in
        # create-new-requirements.sh (RFC 8259, complete and byte-wise under LC_ALL=C).
        if ! declare -F git_repo_root >/dev/null 2>&1; then
            git_repo_root() { git rev-parse --show-toplevel 2>/dev/null; }
        fi
        if ! declare -F git_current_branch >/dev/null 2>&1; then
            git_current_branch() { git rev-parse --abbrev-ref HEAD 2>/dev/null; }
        fi
        if ! declare -F is_git_repo >/dev/null 2>&1; then
            is_git_repo() { git rev-parse --is-inside-work-tree >/dev/null 2>&1; }
        fi
        if ! declare -F json_escape >/dev/null 2>&1; then
            json_escape() {
                local s="$1"
                s="${s//\\/\\\\}"
                s="${s//\"/\\\"}"
                s="${s//$'\n'/\\n}"
                s="${s//$'\t'/\\t}"
                s="${s//$'\r'/\\r}"
                s="${s//$'\b'/\\b}"
                s="${s//$'\f'/\\f}"
                # LC_ALL=C makes ${#s} count bytes and ${s:$i:1} yield single bytes,
                # so multi-byte UTF-8 sequences pass through intact.
                local LC_ALL=C
                local i char code
                for (( i=0; i<${#s}; i++ )); do
                    char="${s:$i:1}"
                    printf -v code '%d' "'$char" 2>/dev/null || code=256
                    if (( code >= 1 && code <= 31 )); then
                        printf '\\u%04x' "$code"
                    else
                        printf '%s' "$char"
                    fi
                done
            }
        fi

        # Ensure UTF-8 locale for better Unicode handling
        ensure_utf8_locale || true
    fi

    # Parse command line arguments
    JSON_MODE=false
    REQUIRE_TASKS=false
    INCLUDE_TASKS=false
    REQUIRE_SPEC=false
    INCLUDE_SPEC=false
    INCLUDE_PLAN=false
    PATHS_ONLY=false

    for arg in "$@"; do
        case "$arg" in
            --json)
                JSON_MODE=true
                ;;
            --require-tasks)
                REQUIRE_TASKS=true
                ;;
            --include-tasks)
                INCLUDE_TASKS=true
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
            --paths-only)
                PATHS_ONLY=true
                ;;
            --help|-h)
                cat << 'EOF'
Usage: check-prerequisites.sh [OPTIONS]

Consolidated prerequisite checking for Spec-Driven Development workflow.

OPTIONS:
  --json              Output in JSON format
  --require-tasks     Require tasks.md to exist (for implementation phase)
  --include-tasks     Include tasks.md in AVAILABLE_DOCS list
  --require-spec      Require requirements.md to exist
  --include-spec      Include requirements.md in AVAILABLE_DOCS list
  --include-plan      Include plan.md in AVAILABLE_DOCS list
  --paths-only        Only output path variables (no prerequisite validation)
  --help, -h          Show this help message

EXAMPLES:
  # Check task prerequisites (plan.md required)
  ./check-prerequisites.sh --json

  # Check implementation prerequisites (plan.md + tasks.md required)
  ./check-prerequisites.sh --json --require-tasks --include-tasks

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
    SCRIPT_DIR="$(CDPATH="" cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    source "$SCRIPT_DIR/common.sh"

    # Ensure UTF-8 locale for better Unicode handling across tools
    ensure_utf8_locale || true

    # Get feature paths and validate branch.
    # Capture, check the resolver's status, then eval the QUOTED output. The old
    # `eval $(get_feature_paths)` word-split the assignments and let a value's own
    # single quote break out of its quoting and run as code; get_feature_paths now
    # emits printf '%q' values and returns 1 when the spec directory is ambiguous.
    # Adapted-from: 46bc65b1cefc487e507aa7b809ce4e48b96ba4ec
    local _paths_output
    _paths_output=$(get_feature_paths) || {
        echo "ERROR: Failed to resolve feature paths" >&2
        exit 1
    }
    eval "$_paths_output"
    unset _paths_output
    check_feature_branch "$CURRENT_BRANCH" "$HAS_GIT" || exit 1

    # Extract REQUIREMENT_ID from branch name (NOT feature name)
    # Branch name format: NNN-requirement-name (e.g., 003-speckit-agents-command)
    # This is the requirement/spec key, NOT the feature name
    REQUIREMENT_ID=""
    if [[ $CURRENT_BRANCH =~ ^([0-9]+)- ]]; then
        REQUIREMENT_ID="${BASH_REMATCH[1]}"
    fi

    # Extract Feature metadata from requirements.md when available.
    FEATURE_ID=""
    FEATURE_NAME=""
    if [[ -f "$FEATURE_SPEC" ]]; then
        FEATURE_ID=$(sed -n 's/^\*\*Feature ID\*\*:[[:space:]]*\([0-9][0-9][0-9]\).*/\1/p' "$FEATURE_SPEC" | head -n 1)
        FEATURE_NAME=$(sed -n 's/^\*\*Feature Name\*\*:[[:space:]]*//p' "$FEATURE_SPEC" | head -n 1)
    fi

    # Phase detection (MODE) — same rule as /speckit.clarify Phase 0, computed
    # from file existence in REQUIREMENTS_DIR so callers do not redo it agent-side:
    #   A = post-requirements (plan.md missing), B = post-plan (tasks.md missing),
    #   C = post-tasks. NONE = requirements.md missing → callers must route to
    #   /speckit.requirements first (clarify's abort rule).
    MODE="NONE"
    if [[ -f "$FEATURE_SPEC" ]]; then
        if [[ -f "$TASKS" ]]; then
            MODE="C"
        elif [[ -f "$IMPL_PLAN" ]]; then
            MODE="B"
        else
            MODE="A"
        fi
    fi

    # Writability probe (WRITABLE) — write-bit stat on the feature dir and the
    # mode's target artifact (the fail-fast probe the commands otherwise perform
    # as a separate agent-side step; root-owned dirs are the known failure class).
    # Reported as a JSON boolean; the caller still decides whether to stop.
    MODE_TARGET=""
    case "$MODE" in
        A) MODE_TARGET="$FEATURE_SPEC" ;;
        B) MODE_TARGET="$IMPL_PLAN" ;;
        C) MODE_TARGET="$TASKS" ;;
    esac
    WRITABLE=false
    if [[ -d "$REQUIREMENTS_DIR" && -w "$REQUIREMENTS_DIR" ]]; then
        if [[ -z "$MODE_TARGET" || ! -e "$MODE_TARGET" || -w "$MODE_TARGET" ]]; then
            WRITABLE=true
        fi
    fi

    # If paths-only mode, output paths and exit (support JSON + paths-only combined)
    if $PATHS_ONLY; then
        if $JSON_MODE; then
            # Minimal JSON paths payload (no validation performed)
            # Note: REQUIREMENT_ID is extracted from branch name, not FEATURE_ID
            # Feature metadata must be retrieved from .specify/features.md
            # Every quoted value goes through json_escape (common.sh publishes the
            # host-owned RFC 8259 escaper): FEATURE_NAME is free text read out of
            # requirements.md, and a path or branch may carry a quote or a newline.
            # WRITABLE stays raw — it is a JSON boolean, not a string.
            # Adapted-from: 9c0c1446ecc7b8e92d866050b5cbc620d8a307e5
            printf '{"REPO_ROOT":"%s","BRANCH":"%s","REQUIREMENT_ID":"%s","REQUIREMENTS_DIR":"%s","FEATURE_ID":"%s","FEATURE_NAME":"%s","FEATURE_SPEC":"%s","IMPL_PLAN":"%s","TASKS":"%s","MODE":"%s","WRITABLE":%s}\n' \
                "$(json_escape "$REPO_ROOT")" \
                "$(json_escape "$CURRENT_BRANCH")" \
                "$(json_escape "$REQUIREMENT_ID")" \
                "$(json_escape "$REQUIREMENTS_DIR")" \
                "$(json_escape "$FEATURE_ID")" \
                "$(json_escape "$FEATURE_NAME")" \
                "$(json_escape "$FEATURE_SPEC")" \
                "$(json_escape "$IMPL_PLAN")" \
                "$(json_escape "$TASKS")" \
                "$(json_escape "$MODE")" \
                "$WRITABLE"
        else
            echo "REPO_ROOT: $REPO_ROOT"
            echo "BRANCH: $CURRENT_BRANCH"
            echo "REQUIREMENT_ID: $REQUIREMENT_ID"
            echo "REQUIREMENTS_DIR: $REQUIREMENTS_DIR"
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
        echo "Run /speckit.requirements first to create the feature structure." >&2
        exit 1
    fi

    # Check for requirements.md if required
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

    # Include requirements.md if requested and it exists
    if $INCLUDE_SPEC && [[ -f "$FEATURE_SPEC" ]]; then
        docs+=("requirements.md")
    fi

    # Include plan.md if requested and it exists
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

    # Include checklists/ directory (only if it exists and has files)
    if [[ -d "$REQUIREMENTS_DIR/checklists" ]] && [[ -n "$(ls -A "$REQUIREMENTS_DIR/checklists" 2>/dev/null)" ]]; then
        docs+=("checklists/")
    fi

    # Include feature linkage + verification artifacts when present
    [[ -f "$REQUIREMENTS_DIR/feature-ref.md" ]] && docs+=("feature-ref.md")
    [[ -f "$REQUIREMENTS_DIR/verification.md" ]] && docs+=("verification.md")

    # Include tasks.md if requested and it exists
    if $INCLUDE_TASKS && [[ -f "$TASKS" ]]; then
        docs+=("tasks.md")
    fi

    # Output results
    if $JSON_MODE; then
        # Build JSON array of documents. The names are literals today, but each is
        # escaped individually so the array stays valid JSON if a name ever becomes
        # dynamic — escaping the assembled array would escape its structural quotes.
        # Adapted-from: 9c0c1446ecc7b8e92d866050b5cbc620d8a307e5
        if [[ ${#docs[@]} -eq 0 ]]; then
            json_docs="[]"
        else
            local _doc
            json_docs=""
            for _doc in "${docs[@]}"; do
                json_docs+="\"$(json_escape "$_doc")\","
            done
            json_docs="[${json_docs%,}]"
        fi

        printf '{"REQUIREMENTS_DIR":"%s","REQUIREMENT_ID":"%s","FEATURE_ID":"%s","FEATURE_NAME":"%s","AVAILABLE_DOCS":%s,"MODE":"%s","WRITABLE":%s}\n' \
            "$(json_escape "$REQUIREMENTS_DIR")" \
            "$(json_escape "$REQUIREMENT_ID")" \
            "$(json_escape "$FEATURE_ID")" \
            "$(json_escape "$FEATURE_NAME")" \
            "$json_docs" \
            "$(json_escape "$MODE")" \
            "$WRITABLE"
    else
        # Text output
        echo "REQUIREMENTS_DIR:$REQUIREMENTS_DIR"
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
        check_dir "$REQUIREMENTS_DIR/checklists" "checklists/"
        check_file "$REQUIREMENTS_DIR/feature-ref.md" "feature-ref.md"
        check_file "$REQUIREMENTS_DIR/verification.md" "verification.md"

        if $INCLUDE_TASKS; then
            check_file "$TASKS" "tasks.md"
        fi
    fi

}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi
