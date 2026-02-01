---
description: Manage Agent Skills (Refresh or Create)
scripts:
  sh: |
    if [ -z "$ARGUMENTS" ] || [ "$ARGUMENTS" = "null" ]; then
      .specify/scripts/bash/refresh-skills.sh --json
    else
      .specify/scripts/bash/create-new-skill.sh --json "$ARGUMENTS"
    fi
---

> Note: 
> - No arguments: Refresh installed skills from documentation.
> - Argument `<name> - <description>`: Create a new skill (e.g. `testing - Skill for running unit tests`).

## User Input

```text
$ARGUMENTS
```

## Outline

### Mode 1: Refresh Skills (No Arguments)

If \`$ARGUMENTS\` is empty:
1. The script \`refresh-skills.sh\` has been executed to scan and refresh skills in \`.github/skills/\`.
2. Check the JSON output for status and details.
3. Report which skills were refreshed and if any missing skills were created.

### Mode 2: Create New Skill (With Arguments)

If \`$ARGUMENTS\` is provided:
1. The script \`create-new-skill.sh\` has been executed to parse the input and create the skill directory.
2. Check the JSON output for the created skill path (\`SKILL_DIR\`).
3. Report the completion of skill creation.
4. Encourage the user to populate the \`SKILL.md\` and resource directories (\`scripts/\`, \`references/\`, \`assets/\`).

## Error Handling

If the script execution returned an error (non-zero exit code or error status in JSON):
- Explain the error to the user (e.g., invalid name format, name already exists).
- Suggest the correct format: \`/speckit.skills "<name> - <description>"\`
