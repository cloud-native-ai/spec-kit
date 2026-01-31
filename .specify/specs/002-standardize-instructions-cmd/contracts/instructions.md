# Command Contract: instructions

## Definition

- **Command**: `instructions`
- **Description**: Generate/Update project instructions for AI agents.
- **Script**: `scripts/bash/generate-instructions.sh` (Standard Speckit Script Protocol)

## Input

The command accepts optional arguments passed through to the underlying script.

- **Variables (Internal)**:
  - `PROJECT_ROOT`: Root path of the project.
  - `PROJECT_NAME`: Name of the project.
  - `DATE`: Current date (YYYY-MM-DD).

## Output

- **File**: `.ai/instructions.md`
  - **Format**: Markdown
  - **Content**: Derived from `templates/instructions-template.md`
- **Symlinks**:
  - `.clinerules/project_rules.md` -> `../.ai/instructions.md`
  - (Extensible for other tools)

## Error Handling

- **Missing Template**: Exit Code 1, Error message displayed.
- **Write Permission Denied**: Exit Code 1, Error message displayed.
