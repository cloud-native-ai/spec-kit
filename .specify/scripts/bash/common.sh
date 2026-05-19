#!/usr/bin/env bash
# Common functions and variables for all scripts

ensure_utf8_locale() {
    if locale 2>/dev/null | grep -qi 'utf-8'; then
        return 0
    fi

    if locale -a 2>/dev/null | grep -qi '^C\.utf8\|^C\.UTF-8$'; then
        export LC_ALL=C.UTF-8
        export LANG=C.UTF-8
        return 0
    fi

    if locale -a 2>/dev/null | grep -qi '^en_US\.utf8\|^en_US\.UTF-8$'; then
        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8
        return 0
    fi

    return 1
}

# Get repository root, with fallback for non-git repositories
get_repo_root() {
    if git rev-parse --show-toplevel >/dev/null 2>&1; then
        git rev-parse --show-toplevel
    else
        # Fall back to script location for non-git repos
        local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        (cd "$script_dir/../../.." && pwd)
    fi
}

# Get current branch, with fallback for non-git repositories
get_current_branch() {
    # First check if SPECIFY_FEATURE environment variable is set
    if [[ -n "${SPECIFY_FEATURE:-}" ]]; then
        echo "$SPECIFY_FEATURE"
        return
    fi
    
    # Then check git if available. If the current branch is not a feature branch,
    # fall back to the latest .specify/specs entry so review/read-only commands
    # can still resolve a current requirement context from main/master.
    if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
        local git_branch
        git_branch=$(git rev-parse --abbrev-ref HEAD)
        if [[ "$git_branch" =~ ^[0-9]{3}- ]]; then
            echo "$git_branch"
            return
        fi
    fi

    # For non-feature branches or non-git repos, try to find the latest feature directory
    local repo_root=$(get_repo_root)
    local specs_dir="$repo_root/.specify/specs"
    
    if [[ -d "$specs_dir" ]]; then
        local latest_feature=""
        local highest=0
        
        for dir in "$specs_dir"/*; do
            if [[ -d "$dir" ]]; then
                local dirname=$(basename "$dir")
                if [[ "$dirname" =~ ^([0-9]{3})- ]]; then
                    local number=${BASH_REMATCH[1]}
                    number=$((10#$number))
                    if [[ "$number" -gt "$highest" ]]; then
                        highest=$number
                        latest_feature=$dirname
                    fi
                fi
            fi
        done
        
        if [[ -n "$latest_feature" ]]; then
            echo "$latest_feature"
            return
        fi
    fi
    
    echo "main"  # Final fallback
}

# Check if we have git available
has_git() {
    git rev-parse --show-toplevel >/dev/null 2>&1
}

check_feature_branch() {
    local branch="$1"
    local has_git_repo="$2"
    
    # For non-git repos, we can't enforce branch naming but still provide output
    if [[ "$has_git_repo" != "true" ]]; then
        echo "[specify] Warning: Git repository not detected; skipped branch validation" >&2
        return 0
    fi
    
    if [[ ! "$branch" =~ ^[0-9]{3}- ]]; then
        echo "ERROR: Not on a feature branch. Current branch: $branch" >&2
        echo "Feature branches should be named like: 001-feature-name" >&2
        return 1
    fi
    
    return 0
}

get_feature_dir() { echo "$1/.specify/specs/$2"; }

get_feature_paths() {
    local repo_root=$(get_repo_root)
    local current_branch=$(get_current_branch)
    local has_git_repo="false"
    
    if has_git; then
        has_git_repo="true"
    fi
    
    local feature_dir=$(get_feature_dir "$repo_root" "$current_branch")
    local requirement_id=""

    if [[ "$current_branch" =~ ^([0-9]+)- ]]; then
        requirement_id="${BASH_REMATCH[1]}"
    fi
    
    cat <<EOF
REPO_ROOT='$repo_root'
CURRENT_BRANCH='$current_branch'
REQUIREMENT_ID='$requirement_id'
HAS_GIT='$has_git_repo'
FEATURE_DIR='$feature_dir'
REQUIREMENTS_DIR='$feature_dir'
FEATURE_SPEC='$feature_dir/requirements.md'
IMPL_PLAN='$feature_dir/plan.md'
TASKS='$feature_dir/tasks.md'
RESEARCH='$feature_dir/research.md'
DATA_MODEL='$feature_dir/data-model.md'
QUICKSTART='$feature_dir/quickstart.md'
CONTRACTS_DIR='$feature_dir/contracts'
EOF
}

check_file() { [[ -f "$1" ]] && echo "  ✓ $2" || echo "  ✗ $2"; }
check_dir() { [[ -d "$1" && -n $(ls -A "$1" 2>/dev/null) ]] && echo "  ✓ $2" || echo "  ✗ $2"; }

# Function: safe_quote
# Description: Safely quotes a string so it can be used as a shell argument without interpretation
safe_quote() {
    local input="$1"
    if [[ -z "$input" ]]; then
        echo "Error: No input provided to safe_quote" >&2
        return 1
    fi
    printf '%q' "$input"
}

# Function: validate_input
# Description: Validates input length and basic structure
validate_input() {
    local input="$1"
    local max_length="${2:-10000}"

    if [[ -z "$input" ]]; then
        echo "Error: No input provided to validate_input" >&2
        return 1
    fi

    if [[ ${#input} -gt $max_length ]]; then
        echo "Error: Input exceeds maximum length of $max_length characters (actual length: ${#input})" >&2
        return 1
    fi

    return 0
}

# Function: is_valid_utf8
# Description: Checks if input contains valid UTF-8 sequences
is_valid_utf8() {
    local input="$1"
    if [[ -z "$input" ]]; then
        return 0
    fi
    if printf '%s' "$input" | iconv -f UTF-8 -t UTF-8 >/dev/null 2>&1; then
        return 0
    fi
    echo "Error: Input contains invalid UTF-8 sequences" >&2
    return 1
}

# Validate skill name
validate_skill_name() {
    local name="$1"
    [[ "$name" =~ ^[a-zA-Z0-9_-]+$ ]]
}

# Create standard skill directory structure
create_skill_structure() {
    local skill_path="$1"
    mkdir -p "$skill_path"
    mkdir -p "$skill_path/scripts"
    mkdir -p "$skill_path/references"
    mkdir -p "$skill_path/assets"
}

# Report error
report_error() {
    local message="$1"
    local json_mode="${2:-false}"

    if [[ "$json_mode" == true ]]; then
        local safe_msg="${message//\"/\\\"}"
        echo "{\"status\": \"error\", \"message\": \"$safe_msg\"}"
    else
        echo "Error: $message" >&2
    fi
}

# Report success
report_success() {
    local message="$1"
    local data="$2"
    local json_mode="${3:-false}"

    if [[ "$json_mode" == true ]]; then
        local safe_msg="${message//\"/\\\"}"
        if [[ -n "$data" ]]; then
            echo "{\"status\": \"success\", \"message\": \"$safe_msg\", $data}"
        else
            echo "{\"status\": \"success\", \"message\": \"$safe_msg\"}"
        fi
    else
        echo "$message"
    fi
}
