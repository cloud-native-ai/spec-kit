# Basic project initialization Feature Index

**Last Updated**: 2025-12-03
**Total Features**: 3

## Features

| 001 | Test Feature Spec Linkage | Specification completed for feature 001 | Planned | .specify/specs/001-test-feature-spec-linkage/spec.md | 2025-12-03 |
| 002 | Second Spec Same Feature | Specification completed for feature 002 | Planned | .specify/specs/002-second-spec-same-feature/spec.md | 2025-12-03 |
| 004 | Remove GitHub API Integration | Remove all code and dependencies related to GitHub API interaction, including the taskstoissues command. | Implemented | .specify/specs/004-remove-github-api/spec.md | 2025-12-11 |

## Spec–Feature Mapping

This section lists all specs and the feature IDs they are currently associated with.

| Spec Branch | Spec Path | Feature ID |
|-------------|-----------|------------|
| 001-test-feature-spec-linkage | .specify/specs/001-test-feature-spec-linkage/spec.md | 001 |
| 002-second-spec-same-feature | .specify/specs/002-second-spec-same-feature/spec.md | 002 |
| 004-remove-github-api | .specify/specs/004-remove-github-api/spec.md | 004 |

## Feature Entry Format

Each feature entry should follow this format in the table:

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | Feature Name | Brief description of the feature | Draft | .specify/specs/001-feature-name/spec.md | 2025-11-21 |

### Column Definitions

| Column | Description |
|--------|-------------|
| ID | Sequential three-digit feature identifier (001, 002, etc.) |
| Name | Short feature name (2-4 words) describing the feature |
| Description | Brief summary of the feature's purpose and scope |
| Status | Current implementation status (Draft, Planned, Implemented, Ready for Review, Completed) |
| Spec Path | Path to specification file or "(Not yet created)" if not yet created |
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
