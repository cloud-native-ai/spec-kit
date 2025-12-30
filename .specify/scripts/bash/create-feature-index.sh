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
i=1
while [ $i -le $# ]; do
    arg="${!i}"
    case "$arg" in
        --json) 
            JSON_MODE=true 
            ;;
        --help|-h) 
            echo "Usage: $0 [--json]"
            echo ""
            echo "Options:"
            echo "  --json              Output in JSON format"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Behavior:"
            echo "  - Creates or updates .specify/memory/feature-index.md with feature index in Markdown table format"
            echo "  - Reads feature descriptions from stdin if available"
            echo "  - Automatically stages .specify/memory/feature-index.md changes with git"
            echo ""
            echo "Examples:"
            echo "  echo 'Add user authentication system' | $0 --json"
            echo "  $0"
            exit 0
            ;;
        *) 
            # Ignore unknown arguments for now
            ;;
    esac
    i=$((i + 1))
done

# Read feature descriptions from stdin if available
FEATURE_DESCRIPTIONS=""
if [ ! -t 0 ]; then
    # stdin is not a terminal, read from it
    FEATURE_DESCRIPTIONS=$(cat)
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

# Create .specify/memory directory if it doesn't exist
MEMORY_DIR="$REPO_ROOT/.specify/memory"
mkdir -p "$MEMORY_DIR"
FEATURES_FILE="$MEMORY_DIR/feature-index.md"

# Function to get current date in YYYY-MM-DD format
get_current_date() {
    if command -v date >/dev/null 2>&1; then
        date -I 2>/dev/null || date +%Y-%m-%d
    else
        # Fallback for systems without date -I
        printf '%(%Y-%m-%d)T\n' -1 2>/dev/null || echo "Unknown date"
    fi
}

# Function to generate a short name from feature description
generate_short_name() {
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
    
    # If we have meaningful words, use first 2-4 of them
    if [ ${#meaningful_words[@]} -gt 0 ]; then
        local max_words=4
        if [ ${#meaningful_words[@]} -lt 4 ]; then max_words=${#meaningful_words[@]}; fi
        
        local result=""
        local count=0
        for word in "${meaningful_words[@]}"; do
            if [ $count -ge $max_words ]; then break; fi
            if [ $count -gt 0 ]; then result="$result "; fi
            result="$result$word"
            count=$((count + 1))
        done
        echo "$result"
    else
        # Fallback to first 4 words of original description
        echo "$description" | cut -d' ' -f1-4
    fi
}

# Function to parse existing features from feature-index.md
parse_existing_features() {
    local features_file="$1"
    local -n existing_features_ref=$2
    local -n next_id_ref=$3
    
    if [ ! -f "$features_file" ]; then
        existing_features_ref=()
        next_id_ref=1
        return 0
    fi
    
    # Check if file has the expected table format
    if ! grep -q "| ID | Name | Description | Status | Feature Details | Last Updated |" "$features_file" 2>/dev/null; then
        existing_features_ref=()
        next_id_ref=1
        return 0
    fi
    
    # Parse existing features from table
    local line_num=0
    local in_table=false
    local highest_id=0
    local features=()
    
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        
        # Check for table header
        if echo "$line" | grep -q "| ID | Name | Description | Status | Feature Details | Last Updated |"; then
            in_table=true
            continue
        fi
        
        # Check for table separator
        if $in_table && echo "$line" | grep -q "|----|"; then
            continue
        fi
        
        # Parse table rows
        if $in_table && echo "$line" | grep -q "^[[:space:]]*|[[:space:]]*[0-9][0-9][0-9][[:space:]]*|"; then
            # Extract ID (first column after |)
            local id=$(echo "$line" | sed 's/^[[:space:]]*|//; s/|.*$//' | tr -d '[:space:]')
            local name=$(echo "$line" | cut -d'|' -f3 | tr -d '[:space:]')
            local description=$(echo "$line" | cut -d'|' -f4)
            local status=$(echo "$line" | cut -d'|' -f5 | tr -d '[:space:]')
            local spec_path=$(echo "$line" | cut -d'|' -f6)
            local last_updated=$(echo "$line" | cut -d'|' -f7 | tr -d '[:space:]')
            
            # Clean up fields
            description=$(echo "$description" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            spec_path=$(echo "$spec_path" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
            
            # Store feature
            features+=("$id|$name|$description|$status|$spec_path|$last_updated")
            
            # Track highest ID
            if [ "$id" -gt "$highest_id" ] 2>/dev/null; then
                highest_id=$id
            fi
        fi
        
        # End of table if we hit a non-table line after being in table
        if $in_table && ! echo "$line" | grep -q "^[[:space:]]*|"; then
            in_table=false
        fi
    done < "$features_file"
    
    existing_features_ref=("${features[@]}")
    next_id_ref=$((highest_id + 1))
}

# Function to find spec path for a feature
find_spec_path() {
    local feature_id="$1"
    local repo_root="$2"
    local specs_dir="$repo_root/.specify/specs"
    
    if [ -d "$specs_dir" ]; then
        # Look for directory matching the feature ID pattern
        for dir in "$specs_dir"/"$feature_id"-*; do
            if [ -d "$dir" ]; then
                spec_file="$dir/spec.md"
                if [ -f "$spec_file" ]; then
                    # Return relative path
                    echo "${dir#$repo_root/}/spec.md"
                    return 0
                fi
            fi
        done
    fi
    
    echo "(Not yet created)"
}

# Function to determine feature status based on spec path
determine_status() {
    local spec_path="$1"
    if [ "$spec_path" = "(Not yet created)" ]; then
        echo "Draft"
    else
        echo "Planned"
    fi
}

# Function to update orphaned features
update_orphaned_features() {
    local -n features_ref=$1
    local repo_root="$2"
    local specs_dir="$repo_root/.specify/specs"
    
    local updated_features=()
    for feature in "${features_ref[@]}"; do
        IFS='|' read -r id name description status spec_path last_updated <<< "$feature"
        
        # Check if spec path exists and is valid
        if [ "$spec_path" != "(Not yet created)" ] && [ "$spec_path" != "(Orphaned - spec file deleted)" ]; then
            full_spec_path="$repo_root/$spec_path"
            if [ ! -f "$full_spec_path" ]; then
                # Spec file doesn't exist - mark as orphaned
                spec_path="(Orphaned - spec file deleted)"
            fi
        fi
        
        updated_features+=("$id|$name|$description|$status|$spec_path|$last_updated")
    done
    
    features_ref=("${updated_features[@]}")
}

# Parse existing features
declare -a existing_features
next_id=1
parse_existing_features "$FEATURES_FILE" existing_features next_id

# Update orphaned features
update_orphaned_features existing_features "$REPO_ROOT"

# Process new feature descriptions
new_features=()
if [ -n "$FEATURE_DESCRIPTIONS" ]; then
    # Split input by newlines (handle multiple features)
    while IFS= read -r description; do
        [ -z "$description" ] && continue
        
        # Generate short name
        short_name=$(generate_short_name "$description")
        
        # Find or create feature ID
        feature_id=$(printf "%03d" "$next_id")
        next_id=$((next_id + 1))
        
        # Determine spec path and status
        spec_path=$(find_spec_path "$feature_id" "$REPO_ROOT")
        status=$(determine_status "$spec_path")
        last_updated=$(get_current_date)
        
        new_features+=("$feature_id|$short_name|$description|$status|$spec_path|$last_updated")
    done <<< "$FEATURE_DESCRIPTIONS"
fi

# Combine existing and new features
all_features=("${existing_features[@]}" "${new_features[@]}")

# Sort features by ID
IFS=$'\n' sorted_features=($(sort -t'|' -k1,1n <<<"${all_features[*]}"))
unset IFS

# Write updated feature-index.md
{
    echo "# Project Feature Index"
    echo ""
    current_date=$(get_current_date)
    total_features=${#sorted_features[@]}
    echo "**Last Updated**: $current_date"
    echo "**Total Features**: $total_features"
    echo ""
    echo "## Features"
    echo ""
    echo "| ID | Name | Description | Status | Spec Path | Last Updated |"
    echo "|----|------|-------------|--------|-----------|--------------|"
    
    for feature in "${sorted_features[@]}"; do
        IFS='|' read -r id name description status spec_path last_updated <<< "$feature"
        echo "| $id | $name | $description | $status | $spec_path | $last_updated |"
    done
} > "$FEATURES_FILE"

# Automatically stage the changes if git is available
if [ "$HAS_GIT" = true ]; then
    if command -v git >/dev/null 2>&1; then
        git add "$FEATURES_FILE" 2>/dev/null || true
    fi
fi

# Output results
if $JSON_MODE; then
    printf '{"FEATURES_FILE":"%s","TOTAL_FEATURES":%d}\n' "$FEATURES_FILE" "$total_features"
else
    echo "FEATURES_FILE: $FEATURES_FILE"
    echo "TOTAL_FEATURES: $total_features"
    echo "Feature index created/updated successfully"
fi