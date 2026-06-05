# Feature Reference: Portable Skill Creation

**Feature ID**: 013  
**Feature Name**: Skills Command  
**Spec**: [requirements.md](./requirements.md)  
**Plan**: [plan.md](./plan.md)

## Feature Context

This spec is the fifth iteration under Feature 013 (Skills Command):

1. **005-tool-skill-ids**: Deterministic resource IDs for skills and tools
2. **007-skill-install-layout**: Canonical `.specify/skills/` installation layout
3. **008-create-skills-skill**: Extracted creation workflow into `create-skills` skill
4. **012-skill-home-workdir**: `${SKILL_HOME}` / `${SKILL_WORKDIR}` path conventions
5. **013-portable-skill-creation**: Remove tool-manifest coupling for cross-environment portability (this spec)

## Problem Statement

Skills created via `/speckit.skills` embed environment-specific tool-discovery logic that makes them non-portable. The creation workflow runs `refresh-tools.sh` to generate tool manifest JSON files (`system.json`, `shell.json`, `project.json`) into each skill's `tools/` directory. When the skill is used in a different environment — different machine, different AI agent, CI/CD pipeline — these manifests may reference tools that don't exist, and the refresh script itself may not be available.

## Solution

Remove the tool-discovery step from the skill creation pipeline entirely. Tool awareness is an agent-runtime concern, not a per-skill static artifact. The skill template, creation workflow, orchestration template, scaffolding script, and validation checklist are all updated to stop producing, requiring, or validating tool manifests.

## Impact on Feature 013

- **Subtractive change**: No new capabilities added. Existing tool-manifest generation is removed.
- **Backward compatible**: Existing skills with `tools/` directories are unaffected. The `tools/` directory remains valid for user-authored content.
- **Template simplification**: The skill template becomes lighter — fewer sections to maintain and no environment-specific boilerplate.
- **Script simplification**: `create-new-skill.sh` becomes simpler — the `refresh_tools_for_target()` function and its dependencies are removed.

## Related Files

- Specification: [requirements.md](./requirements.md)
- Plan: [plan.md](./plan.md)
- Data Model: [data-model.md](./data-model.md)
- Contract: [contracts/portable-skill-creation.openapi.yaml](./contracts/portable-skill-creation.openapi.yaml)
- Quickstart: [quickstart.md](./quickstart.md)
- Quality Checklist: [checklists/requirements.md](./checklists/requirements.md)
- Feature Detail: `.specify/memory/features/013.md`
- Feature Index: `.specify/memory/features.md`
