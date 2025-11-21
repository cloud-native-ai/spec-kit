# Contract: /speckit.specify Command

## Purpose
Create or update a feature specification from a natural language feature description, with proper integration into the feature index.

## Input

### User Input
- **Type**: String (natural language feature description)
- **Format**: Raw text provided after `/speckit.specify` command
- **Constraints**: Must not be empty (triggers error if empty)
- **Examples**: 
  - `"Add user authentication with email and password"`
  - `"Implement payment processing with credit cards"`
  - `"Create admin dashboard for user management"`

### Script Interface
The command template executes:
```bash
cat << 'EOF' | .specify/scripts/bash/create-new-feature.sh --json <short_name>
<user_input>
EOF
```

Where `<short_name>` is a 2-4 word identifier generated from the feature description.

## Output

### Script Output (JSON mode)
```json
{
  "BRANCH_NAME": "001-user-auth",
  "SPEC_FILE": "/absolute/path/to/.specify/specs/001-user-auth/spec.md"
}
```

### Script Output (human-readable mode)
```
BRANCH_NAME: 001-user-auth
SPEC_FILE: /absolute/path/to/.specify/specs/001-user-auth/spec.md
New feature branch created and specification initialized
```

## Feature Specification Format

The `spec.md` file follows the standard specification template with these key sections:
- Feature Specification header with branch name
- User Scenarios & Testing (mandatory)
- Requirements (mandatory)  
- Key Entities (if data involved)
- Success Criteria (mandatory)

## Integration Points

### Feature Index Integration
- **Status Update**: Updates corresponding feature entry in `feature-index.md` from "Draft" to "Planned"
- **Spec Path**: Records the specification file path in the feature entry
- **Feature ID**: Uses sequential ID based on existing features (001, 002, etc.)

### Git Integration
- **Branch Creation**: Creates and checks out a new feature branch with format `###-short-name`
- **Directory Structure**: Creates `.specify/specs/###-short-name/` directory
- **File Initialization**: Creates `spec.md` file with template content

### Workflow Integration
- **Input for /speckit.plan**: The generated spec.md serves as input for planning phase
- **Status Tracking**: Feature status in index reflects current implementation state
- **Traceability**: Links business requirements to technical implementation

## Error Conditions

| Condition | Error Message | Resolution |
|-----------|---------------|------------|
| Empty feature description | "No feature description provided" | Provide non-empty description |
| Cannot determine repository root | "Error: Could not determine repository root" | Run command from within repository |
| Invalid short name format | Standard shell validation errors | Use valid characters in description |
| File permission errors | Standard shell error messages | Check file permissions |
| Git branch conflicts | Git error messages | Resolve branch naming conflicts |

## Performance Requirements

- **Maximum execution time**: 3 seconds for specification creation
- **Memory usage**: Minimal (template-based generation)
- **File I/O**: Creates directory structure and single spec file

## Success Criteria

- Feature branch created with proper naming convention
- Specification file created with complete template structure
- Feature index updated with "Planned" status and spec path
- All mandatory sections in specification completed or marked for clarification
- Integration ready for next SDD phase (`/speckit.plan`)

## Script Format Clarification

The current heredoc script format is correct and should be maintained:
```bash
cat << 'EOF' | .specify/scripts/bash/create-new-feature.sh --json <short_name>
<user_input>
EOF
```

This format properly handles complex user input containing quotes, backslashes, and newlines by passing the raw input via stdin to the script, avoiding shell parsing issues.

The documentation description in the original template was misleading, but the actual implementation is correct and should not be changed.