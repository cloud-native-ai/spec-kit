# Quick Start: Skills Command Integration

## Overview

The `/speckit.skills` command provides two primary capabilities for managing skills in the spec-kit framework:

1. **Refresh existing skills**: Synchronize all installed skills with the latest speckit documentation
2. **Create new skills**: Generate new skill directories with proper structure and templates

## Usage Examples

### Refresh All Skills

```bash
/speckit.skills
```

This command will:
- Scan the `.github/skills/` directory for existing skills
- Refresh each skill based on current speckit specifications
- Create missing skills if specifications exist but skills are not installed
- Provide feedback on the number of skills refreshed/created

### Create New Skill

```bash
/speckit.skills "testing - Skill for running unit tests"
```

This command will:
- Parse the input to extract skill name (`testing`) and description (`Skill for running unit tests`)
- Validate the skill name against naming conventions
- Create a new skill directory at `.github/skills/testing/`
- Populate the directory with standard structure:
  - `SKILL.md` with proper YAML frontmatter
  - `scripts/` directory
  - `references/` directory  
  - `assets/` directory
- Provide success confirmation with the created skill path

## Expected Directory Structure

New skills follow this standard structure:

```
.github/skills/{skill-name}/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

The `SKILL.md` file contains:

```yaml
---
name: {skill-name}
description: |
  {skill-description}
---
```

## Error Handling

Common error scenarios and their handling:

- **Invalid skill name**: Names with invalid characters (spaces, special characters) are rejected with clear error messages
- **Existing skill name**: Attempts to create a skill with an existing name provide options to update or choose a different name
- **Missing skills directory**: The `.github/skills/` directory is created automatically if it doesn't exist
- **Malformed input**: Invalid parameter format provides guidance on expected `"name - description"` format

## Verification Steps

After running either command, verify success by:

1. **For refresh**: Check that existing skills have been updated and any missing skills have been created
2. **For create**: Confirm the new skill directory exists with proper structure and content
3. **Check logs**: Review command output for success messages and any warnings

## Next Steps

- Use the created skills in your development workflow
- Customize the skill content (SKILL.md, scripts, references, assets) as needed
- Run `/speckit.skills` periodically to keep skills synchronized with specifications