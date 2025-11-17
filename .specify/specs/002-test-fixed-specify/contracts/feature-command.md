# Contract: /speckit.feature Command

## Purpose
Create or update the project-level feature index (`features.md`) based on high-level goals or existing context.

## Input

### User Input
- **Type**: String (natural language description)
- **Format**: Raw text provided after `/speckit.feature` command
- **Constraints**: Can be empty (creates empty feature index) or contain feature descriptions
- **Examples**: 
  - `"Add user authentication system"`
  - `"Implement OAuth2 integration for API"`
  - `""` (empty - creates empty feature index)

### Script Interface
The command template executes:
```bash
cat << 'EOF' | .specify/scripts/bash/create-feature-index.sh --json
<user_input>
EOF
```

## Output

### Script Output (JSON mode)
```json
{
  "FEATURES_FILE": "/absolute/path/to/features.md",
  "TOTAL_FEATURES": 2
}
```

### Script Output (human-readable mode)
```
FEATURES_FILE: /absolute/path/to/features.md
TOTAL_FEATURES: 2
Feature index created/updated successfully
```

## Feature Index Format

The `features.md` file must follow this exact Markdown table format:

```markdown
# Project Feature Index

**Last Updated**: YYYY-MM-DD
**Total Features**: N

## Features

| ID | Name | Description | Status | Spec Path | Last Updated |
|----|------|-------------|--------|-----------|--------------|
| 001 | Feature Name | Brief description | Draft | (Not yet created) | YYYY-MM-DD |
| 002 | Another Feature | Another description | Planned | .specify/specs/002-another-feature/spec.md | YYYY-MM-DD |
```

### Table Column Definitions

| Column | Description | Format Rules |
|--------|-------------|--------------|
| ID | Sequential three-digit feature identifier | Exactly 3 digits with leading zeros (001, 002, etc.) |
| Name | Short feature name (2-4 words) | Alphanumeric + spaces/hyphens, 2-50 characters |
| Description | Brief summary of feature purpose | 10-500 characters, plain text |
| Status | Current implementation status | One of: Draft, Planned, Implemented, Ready for Review |
| Spec Path | Path to specification file | Either "(Not yet created)" or relative path starting with `.specify/specs/` |
| Last Updated | When feature entry was last modified | YYYY-MM-DD format |

## Integration Points

### Git Integration
- **Automatic staging**: Changes to `features.md` are automatically staged with `git add features.md`
- **Manual commits**: Users must manually commit with their own messages
- **Conflict handling**: Concurrent updates handled via git merge conflicts

### SDD Command Integration
The feature index serves as input for all other SDD commands:
- `/speckit.specify` reads feature ID from branch name to link specification
- `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`, `/speckit.checklist` update feature status

## Error Conditions

| Condition | Error Message | Resolution |
|-----------|---------------|------------|
| Cannot determine repository root | "Error: Could not determine repository root" | Run command from within repository |
| Invalid feature description format | N/A (graceful handling) | Use best-effort parsing |
| File permission errors | Standard shell error messages | Check file permissions |
| Concurrent write conflicts | Git merge conflicts | Manual resolution during merge |

## Performance Requirements

- **Maximum execution time**: 5 seconds for up to 100 features
- **Memory usage**: Linear with number of features (minimal overhead)
- **File I/O**: Single read/write operation per execution

## Success Criteria

- Feature index file created or updated successfully
- All feature entries have proper IDs, names, descriptions, and status
- File serves as single source of truth for project features
- Integration points are ready for SDD command updates
- Changes automatically staged in git