> Note: 
> - Argument format: `<name> - <description>` (e.g., `testing - Unit testing utils`) 
> - Or flags: `--name <name> --description <desc>`

## User Input

```text
$ARGUMENTS
```

## Outline

Goal: Interactively guide the user to create a high-quality SpecKit Skill, ensuring all necessary components are properly structured and documented according to best practices.

Execution Steps:

1.  **Initialize Skill Structure**:
    - Execute `.specify/scripts/bash/create-new-skill.sh --json $ARGUMENTS` (which runs `create-new-skill.sh --json "$ARGUMENTS"`).
    - Parse the JSON output to extract `SKILL_DIR`, `SKILL_NAME`, and `SKILL_DESCRIPTION`.
    - If the script execution fails, explain the error to the user (e.g., invalid name format) and stop.
    - Confirm the creation of the skill directory to the user.

2.  **Step 1: Understand the Goal (Interactive)**:
    - Reference: [Understanding the Skill with Concrete Examples](#step-1-understanding-the-skill-with-concrete-examples).
    - Engage with the user to clarify the skill's purpose if the description is brief.
    - Ask for concrete usage examples (e.g., "What user query should trigger this skill?").

3.  **Step 2: Plan Contents (Interactive)**:
    - Reference: [Planning the Reusable Skill Contents](#step-2-planning-the-reusable-skill-contents).
    - Based on the examples from Step 1, identify needed resources (Scripts, References, Assets).
    - Analyze the identified needs against the [Anatomy of a Skill](#anatomy-of-a-skill) guidelines.
    - Ask the user if they have existing files to include in the `.specify/scripts/`, `references/`, or `assets/` directories created in the new skill folder.

4.  **Step 3: Edit and Refine (Interactive)**:
    - Reference: [Edit the Skill](#step-4-edit-the-skill).
    - Guide the user to edit `SKILL.md` in their editor. 
    - Remind them to update the `description` in the frontmatter and the body instructions.
    - If resources were identified in Step 2, guide the user to place them in the correct subdirectories and reference them in `SKILL.md`.

5.  **Completion**:
    - Summarize the created skill components.
    - Verify that `SKILL.md` exists and has content.
    - Mention the [packaging step](#step-5-packaging-a-skill) if they wish to distribute it (or just mention it's ready for local use).