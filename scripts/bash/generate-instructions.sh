#!/bin/bash
set -e

# Source common for logging
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/common.sh" ]; then
    source "$SCRIPT_DIR/common.sh"
fi

if ! command -v log &> /dev/null; then
    function log() { echo "[$1] $2"; }
fi

PROJECT_ROOT="$PWD"
PROJECT_NAME="$(basename "$PROJECT_ROOT")"
CURRENT_DATE="$(date +%Y-%m-%d)"
TEMPLATE_FILE="templates/instructions-template.md"
TARGET_FILE=".ai/instructions.md"
TARGET_DIR=".ai"

# T005: Hard Fail
if [ ! -f "$TEMPLATE_FILE" ]; then
    log error "Template file not found at $TEMPLATE_FILE. Please create it or copy it from defaults."
    exit 1
fi

mkdir -p "$TARGET_DIR"

# helper to escape for sed
escape_sed() {
    echo "$1" | sed 's/[\/&]/\\&/g'
}

SAFE_PROJECT_NAME=$(escape_sed "$PROJECT_NAME")
SAFE_PROJECT_ROOT=$(escape_sed "$PROJECT_ROOT")
SAFE_DATE=$(escape_sed "$CURRENT_DATE")

# Function to render template
render_template() {
    local input_file="$1"
    sed -e "s/{{PROJECT_NAME}}/$SAFE_PROJECT_NAME/g" \
        -e "s/{{PROJECT_ROOT}}/$SAFE_PROJECT_ROOT/g" \
        -e "s/{{DATE}}/$SAFE_DATE/g" \
        "$input_file"
}

# Function to extract section body: Text between `## Header` and the CA start of next header `##` or `#`
extract_section_body() {
    local file="$1"
    local header_pattern="$2"
    
    # Check if header exists
    if ! grep -q "$header_pattern" "$file"; then
        return 0
    fi

    # Find start line
    local start_line=$(grep -n "$header_pattern" "$file" | head -1 | cut -d: -f1)
    
    # Start reading from the line AFTER the header
    local body_start=$((start_line + 1))
    
    # Print from body_start until next line starting with #
    # We use awk to print lines until we see a line starting with top-level header '#'
    # Note: This implies we only preserve top-level content blocks properly if they are delimited by headings
    tail -n "+$body_start" "$file" | awk '/^#/ { exit } { print }'
}

# T007: Backup
if [ -f "$TARGET_FILE" ]; then
    log info "Backing up existing instructions to ${TARGET_FILE}.bak"
    cp "$TARGET_FILE" "${TARGET_FILE}.bak"
    
    log info "Performing Smart Fusion..."
    
    # T008/T009: Smart Fusion Logic
    # 1. Render the NEW template to a temp file
    TEMP_NEW=$(mktemp)
    render_template "$TEMPLATE_FILE" > "$TEMP_NEW"
    
    # 2. Extract "Project Overview" from OLD file (Preserve user context)
    OLD_OVERVIEW=$(extract_section_body "${TARGET_FILE}.bak" "^## Project Overview")
    
    # 3. Construct the fused file
    if [ ! -z "$OLD_OVERVIEW" ] && [ "$OLD_OVERVIEW" != "" ]; then
        log info "Preserving existing Project Overview..."
        FUSED_FILE=$(mktemp)
        
        # Methodology: Replace contents of "## Project Overview" in TEMP_NEW
        
        # Print header
        awk '/^## Project Overview/ { print; exit }' "$TEMP_NEW" > "$FUSED_FILE"
        
        # Append old content
        echo "$OLD_OVERVIEW" >> "$FUSED_FILE"
        
        # Find start of NEXT section in TEMP_NEW
        OVERVIEW_LINE=$(grep -n "^## Project Overview" "$TEMP_NEW" | cut -d: -f1)
        NEXT_SECTION_REL=$(tail -n "+$((OVERVIEW_LINE + 1))" "$TEMP_NEW" | grep -n "^#" | head -1 | cut -d: -f1)
        
        if [ ! -z "$NEXT_SECTION_REL" ]; then
             ABS_NEXT_LINE=$((OVERVIEW_LINE + NEXT_SECTION_REL))
             tail -n "+$ABS_NEXT_LINE" "$TEMP_NEW" >> "$FUSED_FILE"
        fi
        
        mv "$FUSED_FILE" "$TARGET_FILE"
    else
        log info "No existing Project Overview found or empty. Using template default."
        mv "$TEMP_NEW" "$TARGET_FILE"
    fi
    
    rm -f "$TEMP_NEW"

else
    log info "Generating new instructions file from template..."
    render_template "$TEMPLATE_FILE" > "$TARGET_FILE"
fi

# T010: Symlinks
mkdir -p .clinerules
log info "Updating symlinks in .clinerules..."
ln -sf "../.ai/instructions.md" ".clinerules/project_rules.md"

log success "Instructions generated/updated at $TARGET_FILE"
