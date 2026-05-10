# Quickstart: Create Skills Skill

**Branch**: `008-create-skills-skill`  
**Date**: 2026-05-10

## Goal

Validate that detailed Skill creation guidance has been extracted into `create-skills` and that `/speckit.skills` remains a concise orchestration entrypoint.

## Prerequisites

- Current branch: `008-create-skills-skill`
- Requirements clarified: `Related Feature` is `013` / `Skills Command`
- Python environment available for existing pytest checks

## Validation Scenarios

### Scenario 1: Missing target Skill routes to `create-skills`

1. Open `templates/commands/skills.md`.
2. Confirm the command explains how to parse the requested target Skill.
3. Confirm the command states that when the target Skill does not exist, creation is delegated to `create-skills`.
4. Confirm detailed Skill-authoring methodology is not duplicated inline in the command body.

**Expected result**: The command is understandable as a router without carrying the full Skill creation playbook.

### Scenario 2: Existing target Skill routes to `improve-skills`

1. Use an existing Skill name such as `improve-skills` or `analysis-project` as the target.
2. Review `templates/commands/skills.md` routing language.
3. Confirm existing targets are delegated to `improve-skills` for refinement rather than recreated.

**Expected result**: Existing Skills are protected from accidental recreation.

### Scenario 3: `create-skills` preserves creation guidance

1. Open `skills/create-skills/SKILL.md` after implementation.
2. Confirm it includes guidance for:
   - explicit user input parsing,
   - empty-argument conversation distillation,
   - minimal clarification,
   - `SKILL.md` frontmatter and body structure,
   - resource directories,
   - registry updates,
   - validation and completion reporting.
3. Confirm the Skill focuses on creation and does not absorb improvement responsibilities from `improve-skills`.

**Expected result**: A new Skill can be created end-to-end using `create-skills` alone.

### Scenario 4: Regression checks

Run targeted checks after implementation:

```bash
pytest tests/contract/test_create_new_skill_contract.py tests/contracts/test_skill_install_layout_contract.py tests/integration/test_skill_install_layout_integration.py tests/integration/test_skills_resource_ids.py
```

If implementation adds prompt-asset tests, run those tests as well.

**Expected result**: Existing Skill installation, compatibility, and resource ID behavior remains unchanged.

## Review Checklist

- [ ] `skills/create-skills/SKILL.md` exists and has valid frontmatter.
- [ ] `templates/commands/skills.md` explicitly delegates missing targets to `create-skills`.
- [ ] `templates/commands/skills.md` explicitly delegates existing targets to `improve-skills`.
- [ ] Creation logic is not duplicated in both the command template and the Skill body.
- [ ] The Skill includes example prompts or completion reporting guidance.
- [ ] Existing Skill layout tests pass.
