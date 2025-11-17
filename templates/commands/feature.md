---
description: Create or update the project-level feature index based on high-level goals or existing context.
scripts:
  sh: |
    cat << 'EOF' | .specify/scripts/bash/create-feature-index.sh --json
    $ARGUMENTS
    EOF
  ps: .specify/scripts/powershell/create-feature-index.ps1 -Json "{ARGUMENTS}"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/speckit.feature` in the triggering message **is** the feature description or high-level goals. Assume you always have it available in this conversation even if `{ARGUMENTS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that input, do this:

1. **Analyze existing context**: 
   - Check if a `features.md` file already exists in the project root
   - If it exists, parse the current feature entries
   - If it doesn't exist, prepare to create a new feature index

2. **Generate or update feature entries**:
   - Extract key concepts from the input description
   - Create feature entries with ID, name (2-4 words), brief description, and initial status
   - Use sequential feature IDs (001, 002, 003, etc.) based on existing features
   - Set initial status to "Draft" for new features

3. **Create or update the feature index file**:
   - Generate a `features.md` file in the project root with proper header and feature entries in Markdown table format
   - Ensure the file serves as the single entry point for feature views
   - Include metadata like feature ID, name, description, status, and relevant links

4. **Integration with SDD workflow**:
   - Ensure that subsequent SDD commands (`/speckit.specify`, `/speckit.plan`, etc.) can reference feature IDs
   - Prepare the feature index to be updated by other SDD commands as features progress through their lifecycle

5. **Return completion status** with feature index file path and readiness for SDD commands.

**NOTE**: The `/speckit.feature` command only manages the feature index. All specification, planning, and implementation still follow the standard SDD process using existing commands.

## Feature Index Structure

The `features.md` file should follow this structure:

```markdown
# Project Feature Index

**Last Updated**: [DATE]
**Total Features**: [COUNT]

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | [Feature Name] | [Brief description of the feature] | Draft | (Not yet created) | YYYY-MM-DD |
| 002 | [Feature Name] | [Brief description of the feature] | Planned | .specify/specs/002-[branch-name]/spec.md | YYYY-MM-DD |

[... additional features ...]
```

### Table Column Definitions

| Column | Description |
|--------|-------------|
| ID | Sequential three-digit feature identifier (001, 002, etc.) |
| Name | Short feature name (2-4 words) describing the feature |
| Description | Brief summary of the feature's purpose and scope |
| Status | Current implementation status (Draft, Planned, Implemented, Ready for Review) |
| Spec Path | Path to specification file or "(Not yet created)" if not yet created |
| Last Updated | When the feature entry was last modified (YYYY-MM-DD format) |

## Success Criteria

- Feature index file is created or updated successfully in proper Markdown table format
- All feature entries have proper IDs, names, descriptions, and status
- File serves as single source of truth for project features
- Integration points are ready for SDD command updates
- Changes are automatically staged in git for user to commit