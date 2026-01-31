# Data Model

## Instruction Template Variables

The following placeholders are supported in `templates/instructions-template.md`:

| Variable | Description | Source |
|---|---|---|
| `{{PROJECT_NAME}}` | Name of the current project | `basename $PWD` |
| `{{PROJECT_ROOT}}` | Absolute path to project root | `$PWD` |
| `{{DATE}}` | Current date | `date +%Y-%m-%d` |

## Smart Fusion Strategy

When updating an existing `.ai/instructions.md` file:

1. **Parse**: Read existing file and identifying content under standard headers.
2. **Preserve**: Keep content under headers that match the template.
3. **Append**: Any custom headers from the old file should be appended to a "Custom / Legacy" section or kept at the bottom.
4. **Update**: Replace standard boilerplates (like Constitution links) with the fresh version from the template.

**Note**: The "Backup & Replace" strategy is a fallback if fusion fails or is disabled.
