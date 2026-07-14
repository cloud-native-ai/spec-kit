# Contract: Reference Rewrite

**ID**: C-REFS | **Feature**: 029 | **Maps to**: FR-007, FR-008, FR-011

## Interface

Every reference that previously targeted `sdd-workflow` is rewritten to the shared location, in
the correct form for its artefact type, with no dead links.

## Rules

- Command templates (`templates/commands/*.md`, `templates/skills-template.md`) **MUST** use the
  **root-relative** form: `skills/sdd-workflow/references/<f>.md` → `shared/workflow/<f>.md`.
  (Install-time `rewrite_paths` upgrades these to `.specify/shared/workflow/<f>.md`.)
- Sibling skills (`skills/*/SKILL.md`) **MUST** use the **installed absolute** form:
  `.specify/skills/sdd-workflow/references/<f>.md` → `.specify/shared/workflow/<f>.md`.
- **MUST NOT** mix the two forms within a single artefact type.
- Prose references in `docs/` **MUST** describe the shared reference directory rather than a skill,
  and any skill count/list mention **MUST** drop `sdd-workflow` and decrement the count.
- Every rewritten path **MUST** resolve to an existing file at the new location (no dead link).
- The `.specify/` mirror **MUST** be regenerated from source (not hand-edited); post-regeneration it
  contains no `sdd-workflow` remnant.

## Filename token map

Only the directory segment changes; filenames are unchanged:

```
skills/sdd-workflow/references/  →  shared/workflow/
.specify/skills/sdd-workflow/references/  →  .specify/shared/workflow/
```

Files: `user-input-protocol.md`, `feature-integration.md`, `agent-configuration.md`,
`checklist-methodology.md`, `requirements-guidelines.md`, `dfx-catalog.md`,
`clarify-taxonomy.md`, `ignore-patterns.md`, `tool-definitions.md`, `feedback-step.md`.

## Referring files (exhaustive, source)

- Templates (17 commands): `agents, analyze, checklist, clarify, constitution, feature, implement, instructions, plan, requirements, research, review, skills, tasks, team, todo, tools`.
- Template (1): `templates/skills-template.md`.
- Skills (20): `analysis-project, browser-utils, cli-setup, create-agent, create-skills, create-team, database-utils, document-utils, draw-d3js, draw-echarts, draw-plantuml, extension-e2e-test, git-submodule-edit, git-workflow, improve-agent, improve-skills, improve-team, memory-recall, memory-record, think-skills`.
- Docs (4): `docs/agents/command-and-skills.md, docs/agents/design.md, docs/commands/skills.md, docs/skills/feedback.md`.

## Test Mapping

- Contract test: for each command template, the shared-ref link matches `shared/workflow/…` (no `sdd-workflow`).
- Contract test: for each skill, the shared-ref link matches `.specify/shared/workflow/…`.
- Integration test: after init, every rewritten path in generated commands resolves to an existing file.
