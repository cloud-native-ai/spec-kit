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
SHORT_NAME=""
ARGS=()
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --short-name)
            if [ $((i + 1)) -gt $# ]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            i=$((i + 1))
            next_arg="${!i}"
            # Check if the next argument is another option (starts with --)
            if [[ "$next_arg" == --* ]]; then
                echo 'Error: --short-name requires a value' >&2
                exit 1
            fi
            SHORT_NAME="$next_arg"
            ;;
        --help|-h) 
            echo "Usage: $0 [--json] [--short-name <name>] [<feature_description>]"
            echo ""
            echo "Options:"
            echo "  --json              Output in JSON format"
            echo "  --short-name <name> Provide a custom short name (2-4 words) for the branch"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Behavior:"
            echo "  - If feature_description is provided as argument, creates a new feature specification"
            echo "  - If no arguments provided but input is available on stdin, creates a new feature specification from stdin content"
            echo ""
            echo "Examples:"
            echo "  $0 'Add user authentication system' --short-name 'user-auth'"
            echo "  $0 'Implement OAuth2 integration for API'"
            echo "  echo 'Price is \$100' | $0 --json"
            exit 0
            ;;
        *) 
            ARGS+=("$arg") 
            ;;
    esac
    i=$((i + 1))
done

FEATURE_DESCRIPTION="${ARGS[*]}"

# If no command line arguments provided, read from stdin
if [ -z "$FEATURE_DESCRIPTION" ]; then
    if [ ! -t 0 ]; then
        # stdin is not a terminal, read from it
        FEATURE_DESCRIPTION=$(cat)
    fi
fi

if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] [--short-name <name>] <feature_description>" >&2
    exit 1
fi

# Function to find the repository root by searching for existing project markers
find_repo_root() {
    local dir="$1"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.git" ] || [ -d "$dir/.specify" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Resolve repository root. Prefer git information when available, but fall back
# to searching for repository markers so the workflow still functions in repositories that
# were initialised with --no-git.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$(find_repo_root "$SCRIPT_DIR")"
    if [ -z "$REPO_ROOT" ]; then
        echo "Error: Could not determine repository root. Please run this script from within the repository." >&2
        exit 1
    fi
    HAS_GIT=false
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/.specify/specs"
MEMORY_DIR="$REPO_ROOT/.specify/memory"
FEATURES_DIR="$MEMORY_DIR/features"
FEATURE_INDEX_FILE="$MEMORY_DIR/feature-index.md"

mkdir -p "$SPECS_DIR" "$FEATURES_DIR"

HIGHEST=0
if [ -d "$SPECS_DIR" ]; then
    for dir in "$SPECS_DIR"/*; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
FEATURE_NUM=$(printf "%03d" "$NEXT")

# Function to generate branch name with stop word filtering and length filtering
generate_branch_name() {
    local description="$1"
    
    # Common stop words to filter out
    local stop_words="^(i|a|an|the|to|for|of|in|on|at|by|with|from|is|are|was|were|be|been|being|have|has|had|do|does|did|will|would|should|could|can|may|might|must|shall|this|that|these|those|my|your|our|their|want|need|add|get|set)$"
    
    # Convert to lowercase and split into words
    local clean_name=$(echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g')
    
    # Filter words: remove stop words and words shorter than 3 chars (unless they're uppercase acronyms in original)
    local meaningful_words=()
    for word in $clean_name; do
        # Skip empty words
        [ -z "$word" ] && continue
        
        # Keep words that are NOT stop words AND (length >= 3 OR are potential acronyms)
        if ! echo "$word" | grep -qiE "$stop_words"; then
            if [ ${#word} -ge 3 ]; then
                meaningful_words+=("$word")
            elif echo "$description" | grep -q "\b${word^^}\b"; then
                # Keep short words if they appear as uppercase in original (likely acronyms)
                meaningful_words+=("$word")
            fi
        fi
    done
    
    # If we have meaningful words, use first 3-4 of them
    if [ ${#meaningful_words[@]} -gt 0 ]; then
        local max_words=3
        if [ ${#meaningful_words[@]} -eq 4 ]; then max_words=4; fi
        
        local result=""
        local count=0
        for word in "${meaningful_words[@]}"; do
            if [ $count -ge $max_words ]; then break; fi
            if [ -n "$result" ]; then result="$result-"; fi
            result="$result$word"
            count=$((count + 1))
        done
        echo "$result"
    else
        # Fallback to original logic if no meaningful words found
        echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//' | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//'
    fi
}

# Generate branch name
if [ -n "$SHORT_NAME" ]; then
    # Use provided short name, just clean it up
    BRANCH_SUFFIX=$(echo "$SHORT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
else
    # Generate from description with smart filtering
    BRANCH_SUFFIX=$(generate_branch_name "$FEATURE_DESCRIPTION")
fi

BRANCH_NAME="${FEATURE_NUM}-${BRANCH_SUFFIX}"

# GitHub enforces a 244-byte limit on branch names
# Validate and truncate if necessary
MAX_BRANCH_LENGTH=244
if [ ${#BRANCH_NAME} -gt $MAX_BRANCH_LENGTH ]; then
    # Calculate how much we need to trim from suffix
    # Account for: feature number (3) + hyphen (1) = 4 chars
    MAX_SUFFIX_LENGTH=$((MAX_BRANCH_LENGTH - 4))
    
    # Truncate suffix at word boundary if possible
    TRUNCATED_SUFFIX=$(echo "$BRANCH_SUFFIX" | cut -c1-$MAX_SUFFIX_LENGTH)
    # Remove trailing hyphen if truncation created one
    TRUNCATED_SUFFIX=$(echo "$TRUNCATED_SUFFIX" | sed 's/-$//')
    
    ORIGINAL_BRANCH_NAME="$BRANCH_NAME"
    BRANCH_NAME="${FEATURE_NUM}-${TRUNCATED_SUFFIX}"
    
    >&2 echo "[specify] Warning: Branch name exceeded GitHub's 244-byte limit"
    >&2 echo "[specify] Original: $ORIGINAL_BRANCH_NAME (${#ORIGINAL_BRANCH_NAME} bytes)"
    >&2 echo "[specify] Truncated to: $BRANCH_NAME (${#BRANCH_NAME} bytes)"
fi

if [ "$HAS_GIT" = true ]; then
    # In JSON mode, prevent any git messages from polluting output
    if $JSON_MODE; then
        if ! git checkout -b "$BRANCH_NAME" >/dev/null 2>&1; then
            >&2 echo "[specify] Error: Failed to create and switch to branch '$BRANCH_NAME'"
            exit 1
        fi
    else
        git checkout -b "$BRANCH_NAME"
    fi
else
    >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

TEMPLATE="$REPO_ROOT/.specify/templates/spec-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi

# Set the SPECIFY_FEATURE environment variable for the current session
export SPECIFY_FEATURE="$BRANCH_NAME"

#############################################
# Feature linkage: one Feature, many Specs  #
#############################################

# Helper: find existing feature ID for this branch/spec, if any
find_existing_feature_id() {
    local candidate_id=""

    # 1) SPECIFY_FEATURE env like NNN-slug
    if [ -n "$SPECIFY_FEATURE" ] && [[ "$SPECIFY_FEATURE" =~ ^([0-9]{3})- ]]; then
        candidate_id="${BASH_REMATCH[1]}"
    # 2) current git branch name like NNN-slug
    elif git rev-parse --git-dir >/dev/null 2>&1; then
        local branch_name
        branch_name=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null || true)
        if [[ "$branch_name" =~ ^([0-9]{3})- ]]; then
            candidate_id="${BASH_REMATCH[1]}"
        fi
    fi

    # 3) fallback to BRANCH_NAME prefix
    if [ -z "$candidate_id" ] && [[ "$BRANCH_NAME" =~ ^([0-9]{3})- ]]; then
        candidate_id="${BASH_REMATCH[1]}"
    fi

    # Cross-check with FEATURES_DIR / FEATURE_INDEX_FILE
    if [ -n "$candidate_id" ]; then
        if [ -f "$FEATURES_DIR/${candidate_id}.md" ]; then
            echo "$candidate_id"
            return 0
        fi
        if [ -f "$FEATURE_INDEX_FILE" ] && \
           grep -qE "^\|[ ]*${candidate_id}[ ]*\|" "$FEATURE_INDEX_FILE" 2>/dev/null; then
            echo "$candidate_id"
            return 0
        fi
    fi

    return 1
}

# Helper: create a new feature detail file from template
create_new_feature_from_template() {
    local new_id

    # Determine next available feature ID based on existing detail files
    local highest=0
    if [ -d "$FEATURES_DIR" ]; then
        for f in "$FEATURES_DIR"/*.md; do
            [ -f "$f" ] || continue
            local base
            base=$(basename "$f")
            local num
            num=$(echo "$base" | grep -o '^[0-9]\{3\}' || echo "000")
            num=$((10#$num))
            if [ "$num" -gt "$highest" ]; then
                highest="$num"
            fi
        done
    fi
    new_id=$(printf "%03d" $((highest + 1)))

    local feature_tpl="$REPO_ROOT/.specify/templates/feature-template.md"
    local feature_file="$FEATURES_DIR/${new_id}.md"
    local today
    today=$(date +%Y-%m-%d)

    local feature_slug
    feature_slug="$BRANCH_SUFFIX"

    if [ -f "$feature_tpl" ]; then
        # Very lightweight instantiation: just wire ID/slug/path/dates, leave其他内容给 speckit.feature 深化
        sed \
            -e "s/\[FEATURE_ID\]/${new_id}/g" \
            -e "s/\[FEATURE_SLUG\]/${feature_slug}/g" \
            -e "s/\[FEATURE_CREATED_DATE\]/${today}/g" \
            -e "s/\[FEATURE_LAST_UPDATED_DATE\]/${today}/g" \
            -e "s/\[FEATURE_STATUS\]/Draft/g" \
            "$feature_tpl" > "$feature_file"
    else
        cat > "$feature_file" <<EOF
# Feature Detail: ${FEATURE_DESCRIPTION}

**Feature ID**: ${new_id}
**Status**: Draft
**Created**: ${today}
**Last Updated**: ${today}
EOF
    fi

    echo "$new_id"
}

# Helper: ensure feature-index is present and updated with this spec path
link_spec_to_feature() {
    local fid="$1"
    local spec_rel_path
    spec_rel_path=".specify/specs/${BRANCH_NAME}/spec.md"
    local today
    today=$(date +%Y-%m-%d)

    # Create basic index file if missing
    if [ ! -f "$FEATURE_INDEX_FILE" ]; then
        cat > "$FEATURE_INDEX_FILE" <<EOF
# $(basename "$REPO_ROOT") Feature Index

**Last Updated**: ${today}
**Total Features**: 0

## Features

<!-- Entries will be populated automatically -->

## Feature Entry Format

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
EOF
    fi

    # If update-feature-index.sh exists, prefer delegating to it for full regeneration
    if [ -x "$SCRIPT_DIR/update-feature-index.sh" ]; then
        "$SCRIPT_DIR/update-feature-index.sh" >/dev/null 2>&1 || true
        return 0
    fi

    # Minimal inline update: ensure at least one row exists for this feature ID
    if ! grep -qE "^\|[ ]*${fid}[ ]*\|" "$FEATURE_INDEX_FILE" 2>/dev/null; then
        echo "| ${fid} | Feature ${fid} | Auto-linked from spec ${BRANCH_NAME} | Planned | ${spec_rel_path} | ${today} |" >> "$FEATURE_INDEX_FILE"
    fi
}

# Resolve or create Feature and link this spec
feature_id=""
if ! feature_id=$(find_existing_feature_id); then
    feature_id=$(create_new_feature_from_template)
fi

link_spec_to_feature "$feature_id"

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s"}\n' "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    echo "SPECIFY_FEATURE environment variable set to: $BRANCH_NAME"
fi
