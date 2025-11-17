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
        # Look for existing feature numbers in features.md table
        while IFS= read -r line; do
            if [[ "$line" =~ ^\|\ *([0-9]{3})\ *\| ]]; then
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
    # Convert to lowercase and clean up, limit to 4 words
    echo "$description" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/ /g' | tr -s ' ' | sed 's/^ //;s/ $//' | cut -d' ' -f1-4
}

# Function to check if a feature already exists in the table
feature_exists() {
    local description="$1"
    if [ -f "$FEATURES_FILE" ]; then
        # Escape special characters for grep
        local escaped_desc=$(echo "$description" | sed 's/[]\/$*.^[]/\\&/g')
        if grep -q "|.*|.*|.*$escaped_desc.*|.*|" "$FEATURES_FILE" 2>/dev/null; then
            return 0  # Feature exists
        fi
    fi
    return 1  # Feature doesn't exist
}

# Create or update the features.md file in Markdown table format
create_feature_index() {
    local description="$1"
    local highest_num=$(find_highest_feature_number)
    local current_num=$((highest_num + 1))
    
    # Check if this feature already exists
    if feature_exists "$description"; then
        # Feature already exists, just update the date
        local today=$(date '+%Y-%m-%d')
        sed -i "s/Last Updated: .*/Last Updated: $today/" "$FEATURES_FILE"
        
        # Count existing features
        local total_features=$(grep -c "^| [0-9][0-9][0-9] |" "$FEATURES_FILE" || echo "0")
        
        if $JSON_MODE; then
            printf '{"FEATURES_FILE":"%s","TOTAL_FEATURES":%d}\n' "$FEATURES_FILE" "$total_features"
        else
            echo "FEATURES_FILE: $FEATURES_FILE"
            echo "TOTAL_FEATURES: $total_features"
            echo "Feature index updated successfully"
        fi
        return
    fi
    
    # Read existing content if file exists
    local existing_content=""
    local existing_features=()
    local table_header=""
    local table_separator=""
    
    if [ -f "$FEATURES_FILE" ]; then
        existing_content=$(cat "$FEATURES_FILE")
        
        # Check if we have a table already
        if echo "$existing_content" | grep -q "^| ID | Name | Description | Status | Spec Path | Last Updated |$"; then
            # Extract content before table
            local header_content=$(echo "$existing_content" | sed -n '1,/^| ID | Name | Description | Status | Spec Path | Last Updated |$/p' | head -n -1)
            
            # Extract table header and separator
            table_header="| ID | Name | Description | Status | Spec Path | Last Updated |"
            table_separator="|----|------|-------------|--------|-----------|--------------|"
            
            # Extract existing table rows
            local table_content=$(echo "$existing_content" | sed -n '/^| ID | Name | Description | Status | Spec Path | Last Updated |$/,/^$/p' | tail -n +3 | head -n -1)
            
            # Store existing features
            while IFS= read -r line; do
                if [[ "$line" =~ ^\|\ [0-9]{3}\ \| ]]; then
                    existing_features+=("$line")
                fi
            done <<< "$table_content"
        else
            # No table exists, use all content as header
            header_content="$existing_content"
            table_header="| ID | Name | Description | Status | Spec Path | Last Updated |"
            table_separator="|----|------|-------------|--------|-----------|--------------|"
        fi
    else
        # Create default header if file doesn't exist
        header_content="# Project Feature Index

**Last Updated**: $(date '+%B %d, %Y')
**Total Features**: 0

## Features

"
        table_header="| ID | Name | Description | Status | Spec Path | Last Updated |"
        table_separator="|----|------|-------------|--------|-----------|--------------|"
    fi
    
    # Generate new content
    local new_content="$header_content"
    new_content="${new_content}${table_header}
${table_separator}
"
    
    # Add existing features
    for feature in "${existing_features[@]}"; do
        new_content="${new_content}${feature}
"
    done
    
    # Add new feature from input
    if [ -n "$description" ]; then
        local feature_name=$(generate_feature_name "$description")
        local feature_id=$(printf "%03d" "$current_num")
        local today=$(date '+%Y-%m-%d')
        
        # Add new feature row
        new_content="${new_content}| ${feature_id} | ${feature_name} | ${description} | Draft | (Not yet created) | ${today} |
"
        current_num=$((current_num + 1))
    fi
    
    # Add empty line at the end
    new_content="${new_content}
"
    
    # Update total features count and last updated date
    local total_features=$(echo "$new_content" | grep -c "^| [0-9][0-9][0-9] |")
    local today=$(date '+%Y-%m-%d')
    new_content=$(echo "$new_content" | sed "s/Total Features: [0-9]*/Total Features: $total_features/")
    new_content=$(echo "$new_content" | sed "s/Last Updated: [0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/Last Updated: $today/")
    new_content=$(echo "$new_content" | sed "s/Last Updated: [A-Z][a-z]* [0-9]\{1,2\}, [0-9]\{4\}/Last Updated: $(date '+%B %d, %Y')/")
    
    echo "$new_content" > "$FEATURES_FILE"
    
    # Automatically stage changes if git is available
    if [ "$HAS_GIT" = true ] && command -v git >/dev/null 2>&1; then
        git add "$FEATURES_FILE" >/dev/null 2>&1 || true
    fi
    
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

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|

" > "$FEATURES_FILE"
    else
        # Update last updated date
        sed -i "s/Last Updated: .*/Last Updated: $(date '+%B %d, %Y')/" "$FEATURES_FILE"
    fi
    
    # Count existing features
    local total_features=0
    if [ -f "$FEATURES_FILE" ]; then
        total_features=$(grep -c "^| [0-9][0-9][0-9] |" "$FEATURES_FILE" || echo "0")
    fi
    
    # Automatically stage changes if git is available
    if [ "$HAS_GIT" = true ] && command -v git >/dev/null 2>&1; then
        git add "$FEATURES_FILE" >/dev/null 2>&1 || true
    fi
    
    if $JSON_MODE; then
        printf '{"FEATURES_FILE":"%s","TOTAL_FEATURES":%d}\n' "$FEATURES_FILE" "$total_features"
    else
        echo "FEATURES_FILE: $FEATURES_FILE"
        echo "TOTAL_FEATURES: $total_features"
        echo "Feature index initialized (no new features added)"
    fi
else
    # Process the feature description
    create_feature_index "$FEATURE_DESCRIPTIONS"
fi