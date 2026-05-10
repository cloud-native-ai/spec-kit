---
description: Create Agent Skills
handoffs:
  - label: Update Instructions
    agent: speckit.instructions
    prompt: Update project instructions so the new skill is discoverable.
    send: true
scripts:
  sh: scripts/bash/create-new-skill.sh --json $ARGUMENTS
---

> Note
>
> `/speckit.skills` is the orchestration entrypoint for Skill management. It determines whether the target Skill already exists, then delegates:
> - **Missing target** → `create-skills` for new Skill creation.
> - **Existing target** → `improve-skills` for Skill refinement.
>
> Detailed creation methodology lives in `skills/create-skills/SKILL.md`. Detailed improvement methodology lives in `skills/improve-skills/SKILL.md`.

## User Input

```text
$ARGUMENTS
```

## Orchestration Workflow

### Step 1: Parse target Skill

Extract the target Skill name from `$ARGUMENTS`:

- If the user explicitly names a Skill (e.g., `docx-utils` or `testing - Unit testing utils`), use that name.
- If `$ARGUMENTS` is empty, infer the target from the current conversation or ask one targeted clarification question.
- The name must be a concise command-like identifier using only letters, digits, hyphens (`-`), and underscores (`_`).

### Step 2: Check target existence

Determine whether `.specify/skills/<name>/SKILL.md` already exists:

- Run `scripts/bash/create-new-skill.sh --json <name>` or check the filesystem directly.
- Consider `.github/skills/<name>/SKILL.md` only after confirming `.specify/skills/` is the canonical source.

### Step 3: Route to the correct Skill

**If the target Skill does NOT exist**: Delegate creation to `create-skills`.

- Read `skills/create-skills/SKILL.md` for the full creation workflow.
- This covers: explicit-input parsing, conversation distillation, minimal clarification, SKILL.md structure, resource directories, registry updates, and completion reporting.

**If the target Skill ALREADY exists**: Delegate refinement to `improve-skills`.

- Read `skills/improve-skills/SKILL.md` for the full improvement workflow.
- This covers: evidence collection, root-cause analysis, minimal targeted changes, and validation.

### Step 4: Validate and report

After the delegated Skill completes:

- Confirm the target Skill's `SKILL.md` frontmatter is valid and the canonical path matches the expected `.specify/skills/<name>/SKILL.md`.
- Verify the Skills registry in `.specify/instructions.md` includes one deduplicated row for the Skill.
- Report the created or updated paths, `skill_id`, and follow-up actions (e.g., run `/speckit.instructions`).

## Handoffs

- After creation or improvement, run `/speckit.instructions` to update project instructions so the Skill remains discoverable.
- If validation surfaces issues, re-route to the appropriate Skill for further refinement.

