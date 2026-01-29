#!/bin/bash
set -e

# Try to source common.sh for logging if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/common.sh" ]; then
    source "$SCRIPT_DIR/common.sh"
else
    function log() {
        echo "[$1] $2"
    }
fi

function copilot_generate_instructions() {
  # Create .copilotignore based on .gitignore
  if [ ! -f .copilotignore ]; then
    log info "Creating .copilotignore"

    # Start with .gitignore content if exists
    if [ -f .gitignore ]; then
      log info "Using .gitignore as base for .copilotignore"
      cat .gitignore >.copilotignore
    else
      log warn ".gitignore not found, creating basic .copilotignore"
      touch .copilotignore
    fi

    # Add additional patterns that should be ignored by Copilot
    cat <<BLOCK >>.copilotignore

# Additional patterns for Copilot indexing exclusion
.clinerules/
.github/
.lingma/
.trae/
.qoder/
BLOCK
  else
    log info ".copilotignore already exists, skipping"
  fi

  mkdir -p .ai
  INSTRUCTIONS_FILE=".ai/instructions.md"

  if [ ! -f "$INSTRUCTIONS_FILE" ]; then
    log info "Creating $INSTRUCTIONS_FILE template"
    cat <<'TEMPLATE' >"$INSTRUCTIONS_FILE"
# Project Instructions for AI Agents

## Project Overview
[Brief summary of what the app does, its core value proposition, and key features based on README]

## Documentation Map
This project documentation is distributed across several key files. You MUST refer to these documents for specific details:

| Document | Location | Purpose | Key Content |
|----------|----------|---------|-------------|
| **Constitution** | `memory/constitution.md` | Single source of truth for principles | Coding standards, architectural rules, constraints |
| **Feature Index** | `memory/feature-index.md` | Feature roadmap status | List of active/planned/implemented features |
| **Development** | `CONTRIBUTING.md` | Setup and Guidelines | Setup, testing, and pull request guidelines |
| **Architecture** | `docs/index.md` | High-level architecture | Architecture and design documentation |
| [Other Doc] | [Path] | [Purpose] | [Summary] |

> **Directive**: When answering questions or generating code, ALWAYS check the relevant document from the map above first.

## Tech Stack & Resources
[Detected tech stack from config files]
- **Languages**: [e.g. Python 3.11+]
- **Package Manager**: [e.g. uv]
- **Frameworks**: [e.g. FastAPI, React]
- **Key Directories**:
  - `src/`: Source code
  - `tests/`: Test suite
  - [Other detected dirs]

# MCP Tools Usage Guide

## Tool Selection Strategy
- Prioritize using the `mcp_...` series of tools to query internal documents and code, rather than trying to guess.
- Do not guess about architectural rules; verify them in the **Constitution**.

## Tools
<!-- TOOLS_PLACEHOLDER -->
[Tools section will be populated by the skills command]

## Skills
<!-- SKILLS_PLACEHOLDER -->
[Skills section will be populated by the skills command]
TEMPLATE
  else
    log info "$INSTRUCTIONS_FILE already exists, skipping creation"
  fi

  # Create symlinks for various AI agents
  mkdir -p .clinerules
  # Use -f to force relink if exists but changes needed (ln -sfv handles this)
  pushd .clinerules >/dev/null && ln -sfv ../.ai/instructions.md project_rules.md && popd >/dev/null

  mkdir -p .github
  pushd .github >/dev/null && ln -sfv ../.ai/instructions.md copilot-instructions.md && popd >/dev/null

  mkdir -p .lingma/rules
  pushd .lingma/rules >/dev/null && ln -sfv ../../.ai/instructions.md project_rule.md && popd >/dev/null

  mkdir -p .trae/rules
  pushd .trae/rules >/dev/null && ln -sfv ../../.ai/instructions.md project_rules.md && popd >/dev/null

  mkdir -p .qoder
  pushd .qoder >/dev/null && ln -sfv ../.ai/instructions.md project_rules.md && popd >/dev/null

  # Helper symlinks in root
  ln -sfT .ai/instructions.md QWEN.md
  ln -sfT .ai/instructions.md CLAUDE.md
  ln -sfT .ai/instructions.md IFLOW.md
  
  log info "Instructions generation and linking complete."
}

copilot_generate_instructions
