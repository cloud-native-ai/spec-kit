# [PROJECT_NAME] Feature Index

**Last Updated**: [LAST_UPDATED_DATE]
**Total Features**: [FEATURE_COUNT]

## Features

| ID | Name | Description | Status | Feature Details | Last Updated |
|----|------|-------------|--------|----------------|--------------|
| 003 | Dynamic VS Code Settings | Generate settings based on tech stack | Implemented | .specify/memory/features/003.md | 2025-12-10 |

## Spec–Feature Mapping

This section lists all specs and the feature IDs they are currently associated with.

| Spec Branch | Spec Path | Feature ID |
|-------------|-----------|------------|
| [SPEC_BRANCH] | [SPEC_PATH] | [FEATURE_ID] |

## Feature Entry Format

Each feature entry should follow this format in the table:

| ID | Name | Description | Status | Feature Details | Last Updated |
|----|------|-------------|--------|----------------|--------------|
| [FEATURE_ID] | [FEATURE_NAME] | [FEATURE_DESCRIPTION] | [FEATURE_STATUS] | .specify/memory/features/[FEATURE_ID].md | [FEATURE_LAST_UPDATED] |

### Column Definitions

| Column | Description |
|--------|-------------|
| ID | Sequential three-digit feature identifier (001, 002, etc.) |
| Name | Short feature name (2-4 words) describing the feature |
| Description | Brief summary of the feature's purpose and scope |
| Status | Current implementation status (Draft, Planned, Implemented, Ready for Review, Completed) |
| Feature Details | Path to feature detail file in .specify/memory/features/[FEATURE_ID].md |
| Last Updated | When the feature entry was last modified (YYYY-MM-DD format) |

## Template Usage Instructions

This template contains placeholder tokens in square brackets (e.g., `[PROJECT_NAME]`, `[FEATURE_COUNT]`). 
When generating the actual feature index:

1. Replace `[PROJECT_NAME]` with the actual project name
2. Replace `[LAST_UPDATED_DATE]` with current date in YYYY-MM-DD format
3. Replace `[FEATURE_COUNT]` with the actual number of features
4. Replace `[FEATURE_ENTRIES]` with the complete Markdown table containing all feature entries
5. Each individual feature entry should have its placeholders replaced accordingly:
   - `[FEATURE_ID]`: Sequential three-digit ID
   - `[FEATURE_NAME]`: Short descriptive name (2-4 words)
   - `[FEATURE_DESCRIPTION]`: Brief feature description
   - `[FEATURE_STATUS]`: Current status (Draft, Planned, etc.)
   - `[SPEC_PATH]`: Path to spec file or "(Not yet created)"
   - `[FEATURE_LAST_UPDATED]`: Feature-specific last updated date

Ensure all placeholder tokens are replaced before finalizing the feature index.
