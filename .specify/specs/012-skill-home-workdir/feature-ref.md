# Feature Reference: 012-skill-home-workdir → Feature 013 (Skills Command)

**Branch**: `012-skill-home-workdir` | **Date**: 2026-05-30 | **Plan**: [plan.md](plan.md)

## Linkage

| Field | Value |
|-------|-------|
| Iteration (Requirements ID) | `012-skill-home-workdir` |
| Feature ID | `013` |
| Feature Name | `Skills Command` |
| Feature Index Row | `.specify/memory/features.md` (Feature 013 row) |
| Feature Detail | `.specify/memory/features/013.md` |
| Authoritative Spec | `.specify/specs/012-skill-home-workdir/requirements.md` |
| Plan | `.specify/specs/012-skill-home-workdir/plan.md` |
| Research | `.specify/specs/012-skill-home-workdir/research.md` |
| Data Model | `.specify/specs/012-skill-home-workdir/data-model.md` |
| Contract | `.specify/specs/012-skill-home-workdir/contracts/skill-home-workdir-template.openapi.yaml` |
| Quickstart | `.specify/specs/012-skill-home-workdir/quickstart.md` |
| Quality Checklist | `.specify/specs/012-skill-home-workdir/checklists/requirements.md` |
| Tasks | `.specify/specs/012-skill-home-workdir/tasks.md` *(produced by `/speckit.tasks`)* |

## Why this iteration belongs to Feature 013

Feature 013 ("Skills Command") owns the lifecycle of project-level Skills — creation, installation layout, authoring guidance, and improvement workflows. Previous iterations of Feature 013 already settled:

- `005-tool-skill-ids` — deterministic Skill IDs.
- `007-skill-install-layout` — canonical `.specify/skills/` location with compatibility symlinks.
- `008-create-skills-skill` — extraction of the creation playbook into a dedicated `create-skills` Skill.

This iteration (`012-skill-home-workdir`) is the next refinement: defining the **path conventions** Skill authors and Skill-invoked scripts use to reference resources. It directly extends Feature 013's authoring-guidance surface (`templates/commands/skills.md`, `skills/create-skills/SKILL.md`, `skills/improve-skills/SKILL.md`) without introducing a new feature concept.

## Deltas to record in `features/013.md`

The Key Change list in `.specify/memory/features/013.md` already includes entry #15 capturing the start of this iteration. After this plan, that entry should be augmented (or extended via #16) to note:

> 16. Generated planning-phase artifacts for `012-skill-home-workdir` (`plan.md`, `research.md`, `data-model.md`, `contracts/skill-home-workdir-template.openapi.yaml`, `quickstart.md`, `feature-ref.md`) — locked in the portable `cd … && pwd -P` script idiom (no GNU coreutils dependency), confirmed `SKILL_HOME` supersedes `SKILL_ROOT` everywhere in scope, and defined a structural CI contract for the convention.

The `Last Updated` field on the Feature 013 row in `.specify/memory/features.md` should reflect `2026-05-30`.

## Out of scope for this iteration

- No new Skills are created.
- No changes to the four non-authoring Skills (`analysis-project`, `draw-d3js`, `draw-echarts`, `draw-plantuml`) beyond the SC-004 regression-only verification.
- No changes to the CLI (`src/specify_cli/`), no new scaffolding scripts, no new template engine work.
- The compatibility symlink model from `007-skill-install-layout` is consumed but not modified.
