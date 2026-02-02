---
description: Create Agent Skills
scripts:
   sh: |
     cat << 'EOF' | .specify/scripts/bash/create-new-skill.sh --name "<SKILL_NAME>"
     $ARGUMENTS
     EOF
---

> Note: 
> - Argument format `<name> - <description>`: Create a new skill (e.g., `testing - Skill for running unit tests`).

## User Input

```text
$ARGUMENTS
```

## Outline

### Create New Skill

When `$ARGUMENTS` is provided (format "<name> - <description>"):
1. Execute the `create-new-skill.sh --json "$ARGUMENTS"` script to parse input parameters.
2. Create the new skill directory structure, including the `SKILL.md` file and resource directories (`scripts/`, `references/`, `assets/`).
3. Return the created skill path (`SKILL_DIR`) and related information.
4. Provide step-by-step guidance to help the user complete and refine the skill details.
5. The newly created skill will be automatically included in the `.ai/instructions.md` file upon the next refresh.

## Error Handling

If the script execution returns an error (non-zero exit code or error status in JSON):
- Explain the error reason to the user (e.g., invalid name format, skill name already exists).
- Suggest the correct command format: `/speckit.skills "<name> - <description>"`
