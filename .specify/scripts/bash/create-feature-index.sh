#!/usr/bin/env bash

set -e

# Load common helpers for Unicode support and shared functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/../common.sh" ]; then
    # shellcheck source=/dev/null
    source "$SCRIPT_DIR/../common.sh"
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
FEATURE_DESCRIPTIONS=""
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --help|-h) 
            echo "Usage: $0 [--json] [<feature_descriptions>]"
            echo ""
            echo "Options:"
            echo "  --json              Output in JSON format"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Behavior:"
            echo "  - Creates or updates a features.md file in the project root"
            echo "  - Generates feature entries from input descriptions"
            echo "  - Integrates with existing SDD workflow"
            echo ""
            echo "Examples:"
            echo "  $0 'Add user authentication system'"
            echo "  echo 'Implement OAuth2 integration for API' | $0 --json"
            exit 0
            ;;
        *) 
            # Collect all remaining arguments as the feature description
            if [ -z "$FEATURE_DESCRIPTIONS" ]; then
                FEATURE_DESCRIPTIONS="$arg"
            else
                FEATURE_DESCRIPTIONS="$FEATURE_DESCRIPTIONS $arg"
            fi
            ;;
    esac
    i=$((i + 1))
done

# If no command line arguments provided, read from stdin
if [ -z "$FEATURE_DESCRIPTIONS" ]; then
    if [ ! -t 0 ]; then
        # stdin is not a terminal, read from it
        FEATURE_DESCRIPTIONS=$(cat)
    fi
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

FEATURES_FILE="$REPO_ROOT/features.md"

# Function to find the highest existing feature number
find_highest_feature_number() {
    local highest=0
    if [ -f "$FEATURES_FILE" ]; then
        # Look for existing feature numbers in features.md
        while IFS= read -r line; do
            if [[ "$line" =~ Feature\ ([0-9]+): ]]; then
                local num="${BASH_REMATCH[1]}"
                num=$((10#$num))
                if [ "$num" -gt "$highest" ]; then
                    highest=$num
                fi
            fi
        done < "$FEATURES_FILE"
    fi
    
    # Also check existing spec directories
    SPECS_DIR="$REPO_ROOT/.specify/specs"
    if [ -d "$SPECS_DIR" ]; then
        for dir in "$SPECS_DIR"/*; do
            [ -d "$dir" ] || continue
            dirname=$(basename "$dir")
            number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
            number=$((10#$number))
            if [ "$number" -gt "$highest" ]; then highest=$number; fi
        done
    fi
    
    echo "$highest"
}

# Function to generate a clean feature name from description
generate_feature_name() {
    local description="$1"
    # Convert to lowercase and clean up
    echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g' | tr -s ' ' | sed 's/^ //;s/ $//' | tr ' ' '-'
}

# Create or update the features.md file
create_feature_index() {
    local description="$1"
    local highest_num=$(find_highest_feature_number)
    local current_num=$((highest_num + 1))
    
    # Read existing content if file exists
    local existing_content=""
    local existing_features=()
    if [ -f "$FEATURES_FILE" ]; then
        existing_content=$(cat "$FEATURES_FILE")
        # Extract existing feature entries
        while IFS= read -r line; do
            if [[ "$line" =~ ^###\ Feature\ ([0-9]+): ]]; then
                existing_features+=("${BASH_REMATCH[1]}")
            fi
        done < "$FEATURES_FILE"
    fi
    
    # Generate new content
    local new_content="# Project Feature Index

**Last Updated**: $(date '+%B %d, %Y')
**Total Features**: TBD

## Features
"
    
    # Add existing features first (but only the feature entries, not the header)
    if [ -n "$existing_content" ]; then
        # Extract content after "## Features" header
        if [[ "$existing_content" == *"## Features"* ]]; then
            local features_content=$(echo "$existing_content" | sed -n '/^## Features$/,$p' | tail -n +2)
            if [ -n "$features_content" ] && [ "$features_content" != "## Features" ]; then
                new_content="$new_content$features_content"
            fi
        fi
    fi
    
    # Add new feature from input
    if [ -n "$description" ]; then
        local feature_name=$(generate_feature_name "$description")
        local feature_id=$(printf "%03d" "$current_num")
        
        # Check if this feature already exists (by description similarity)
        local exists=false
        if [ -f "$FEATURES_FILE" ]; then
            if grep -q "$description" "$FEATURES_FILE" 2>/dev/null; then
                exists=true
            fi
        fi
        
        if [ "$exists" = false ]; then
            new_content="$new_content
### Feature $feature_id: $(echo "$description" | cut -c1-50)$( [ ${#description} -gt 50 ] && echo "..." || echo "")
- **Status**: Draft
- **Description**: $description
- **Specification**: (Not yet created)
- **Key Acceptance Criteria**: (To be defined in specification)
"
            current_num=$((current_num + 1))
        fi
    fi
    
    # Update total features count
    local total_features=$(echo "$new_content" | grep -c "^### Feature ")
    new_content=$(echo "$new_content" | sed "s/Total Features: TBD/Total Features: $total_features/")
    
    echo "$new_content" > "$FEATURES_FILE"
    
    if $JSON_MODE; then
        printf '{"FEATURES_FILE":"%s","TOTAL_FEATURES":%d}\n' "$FEATURES_FILE" "$total_features"
    else
        echo "FEATURES_FILE: $FEATURES_FILE"
        echo "TOTAL_FEATURES: $total_features"
        echo "Feature index created/updated successfully"
    fi
}

# Main execution
if [ -z "$FEATURE_DESCRIPTIONS" ]; then
    # No input provided, just ensure features.md exists or create empty one
    if [ ! -f "$FEATURES_FILE" ]; then
        echo "# Project Feature Index

**Last Updated**: $(date '+%B %d, %Y')
**Total Features**: 0

## Features

" > "$FEATURES_FILE"
    fi
    
    if $JSON_MODE; then
        printf '{"FEATURES_FILE":"%s","TOTAL_FEATURES":0}\n' "$FEATURES_FILE"
    else
        echo "FEATURES_FILE: $FEATURES_FILE"
        echo "TOTAL_FEATURES: 0"
        echo "Feature index initialized (no new features added)"
    fi
else
    # Process the feature description
    create_feature_index "$FEATURE_DESCRIPTIONS"
fi