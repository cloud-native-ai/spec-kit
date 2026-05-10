# Research: Create Skills Skill

**Branch**: `008-create-skills-skill`  
**Date**: 2026-05-10  
**Spec**: `requirements.md`

## Decisions

### Decision 1: Extract creation guidance into `skills/create-skills/SKILL.md`

**Decision**: Create a dedicated `create-skills` Skill under the repository `skills/` directory and move detailed Skill-authoring guidance out of `templates/commands/skills.md`.

**Rationale**: The user explicitly requested `skills/create-skills`, and the repository packages the root `skills/` directory in `pyproject.toml`. This makes the Skill available as a reusable source asset for generated projects while reducing command-template size.

**Alternatives considered**:

- Keep all guidance inline in `templates/commands/skills.md`: rejected because it duplicates reusable knowledge and keeps the command oversized.
- Store only under `.specify/skills/create-skills`: rejected as the sole source because this repo packages root `skills/` as template/runtime content; however, implementation may mirror or refresh `.specify/skills` for current-workspace compatibility.

### Decision 2: Keep `/speckit.skills` as the explicit orchestration entrypoint

**Decision**: Refactor the command template so it detects whether the target Skill exists and routes accordingly: missing target → `create-skills`; existing target → `improve-skills`.

**Rationale**: Project instructions define `/speckit.*` commands as chat-instruction entrypoints and Skills as reusable execution knowledge. This preserves predictable user invocation while letting Skills carry specialized methodology.

**Alternatives considered**:

- Rely on automatic Skill triggering only: rejected because Skill triggering can be inconsistent and the command should remain a predictable route.
- Introduce a new slash command only for creation: rejected because `/speckit.skills` already owns Skill management and should delegate internally.

### Decision 3: Preserve creation quality rules through a focused Skill body

**Decision**: The new Skill should preserve existing guidance for metadata extraction, conversation-history distillation, minimal clarification, Skill directory structure, progressive disclosure, resource directories, registry updates, and validation.

**Rationale**: Requirements require behavioral equivalence or improvement after extraction. Existing docs emphasize concise `SKILL.md`, clear descriptions, and on-demand resources.

**Alternatives considered**:

- Move only a short pointer into the Skill: rejected because it would lose the existing creation workflow.
- Copy the full command body verbatim: rejected because the Skill should be focused and should not include command frontmatter or routing responsibilities.

### Decision 4: Validate through documentation and prompt artifact tests

**Decision**: Use pytest for existing script/layout tests and add lightweight assertions or review checks for the new Skill and command template if implementation changes warrant it.

**Rationale**: The project already uses pytest for command scripts and resource ID behavior. This feature primarily changes Markdown prompt/Skill assets, so tests should verify expected files, routing phrases, and registry/frontmatter invariants where practical.

**Alternatives considered**:

- Manual-only review: rejected because the Constitution requires quality gates and regression coverage for important flows.
- Heavy runtime integration harness: deferred because this feature changes prompt assets rather than adding new command execution code.
