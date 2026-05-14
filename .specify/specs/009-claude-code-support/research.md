# Research: Claude Code Support

## Research Scope

This research reviews existing Spec Kit assistant integrations and project governance to plan Claude Code support without introducing drift across CLI behavior, templates, docs, and feature memory.

## Context Reviewed

- `README.md`: Supported AI agents currently list GitHub Copilot, Qwen Code, opencode, and Qoder.
- `docs/installation.md`: Initialization examples currently expose `--ai copilot`, `--ai qwen`, `--ai opencode`, and `--ai qoder`.
- `docs/usage.md`: Describes Spec Kit slash-command workflow and contains Qoder maintenance guidance that can inform Claude Code maintenance guidance.
- `.specify/memory/constitution.md`: Principle V currently approves only GitHub Copilot, Qwen Code, opencode, and Qoder.
- `.specify/memory/features/020.md`: Qoder Support is the closest implementation pattern for adding a first-class assistant.
- `src/specify_cli/__init__.py`: Contains `AGENT_CONFIG`, `generate_commands()`, initialization copy flow, assistant validation, and CLI help text.
- `scripts/bash/generate-instructions.sh`: Generates canonical instructions and compatibility symlinks/files for multiple AI tools, including root-level `CLAUDE.md` but not full Claude Code custom command or ignore support.
- `templates/commands/*.md`: Canonical Spec Kit workflow command templates to reuse for Claude Code custom command surfaces.
- Existing Qoder tests under `tests/contract`, `tests/integration`, and `tests/unit`: Provide patterns for support matrix, initialization, refresh, and support-surface audits.

## Decisions

### Decision 1: Model Claude Code as a first-class supported assistant

**Decision**: Add Claude Code to the same assistant support matrix used for other first-class assistants, with explicit display name, folder/assets, install guidance, validation behavior, and generated command surfaces.

**Rationale**: FR-001 and FR-011 require Claude Code to be presented and governed consistently. Reusing the assistant matrix keeps validation, CLI help, and initialization behavior centralized.

**Alternatives considered**:

- Treat Claude Code as only a root-level `CLAUDE.md` compatibility link: rejected because it does not satisfy custom command or `.claudeignore` requirements.
- Treat Claude Code as a hidden fallback: rejected because support claims and user selection would remain inconsistent.

### Decision 2: Use canonical command templates for Claude Code custom commands

**Decision**: Generate Claude Code custom command files from `templates/commands/*.md`, preserving the canonical Spec Kit workflow and `$ARGUMENTS` handoff semantics.

**Rationale**: FR-003 and SC-002 require full command coverage without conflicting workflow definitions. Existing Qwen/opencode/Qoder generation shows that command templates can be adapted by target assistant format.

**Alternatives considered**:

- Write separate Claude Code-only command content: rejected because it risks drift from canonical `/speckit.*` commands.
- Generate only a subset of commands: rejected unless a command has an explicit documented exclusion, because SC-002 expects 100% coverage.

### Decision 3: Treat `.claudeignore` as a security and context-control asset

**Decision**: Add `.claudeignore` as a managed Claude Code compatibility asset with defaults for dependency folders, caches, build outputs, local environment files, generated temporary content, and secret-like files while preserving required `.specify/` workflow assets.

**Rationale**: FR-004 and the clarified constraints require privacy/security validation. The ignore policy must protect local/generated/private content without making Claude Code unusable for SDD artifacts.

**Alternatives considered**:

- Rely only on `.gitignore`: rejected because Claude Code context control is not identical to version-control ignore behavior.
- Ignore all generated Spec Kit artifacts: rejected because Claude Code must be able to read requirements, plans, tasks, and canonical instructions.

### Decision 4: Preserve user customizations during refresh

**Decision**: Refresh should update generated Claude Code assets safely, preserve user-authored custom content where possible, and report conflicts when safe preservation cannot be guaranteed.

**Rationale**: FR-006 and User Story 2 require existing workspace adoption without destructive overwrites.

**Alternatives considered**:

- Always overwrite Claude Code files: rejected due to data-loss risk.
- Never update existing Claude Code files: rejected because canonical workflow changes would not propagate.

### Decision 5: Make governance update a release blocker

**Decision**: Planning may proceed, but implementation cannot be marked ready for review until the constitution and support claims include Claude Code as an officially approved assistant.

**Rationale**: Current constitution excludes Claude Code. FR-011 explicitly requires governance and support claim updates.

**Alternatives considered**:

- Ignore constitution mismatch: rejected because Principle V is a hard governance gate.
- Create a separate non-functional feature for governance: rejected because the governance update is intrinsic to Feature 021 and should be tracked here.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Governance drift between constitution, README, docs, and CLI help | Add support-surface audit tests and release checklist coverage |
| `.claudeignore` excludes required SDD artifacts | Add quickstart and unit tests validating required `.specify/` paths remain available |
| Claude Code command files drift from canonical templates | Generate commands from `templates/commands/*.md` and audit command inventory coverage |
| Existing assistant integrations regress | Add coexistence integration tests and avoid touching unrelated assistant roots during refresh |
| User custom Claude files are overwritten | Add preservation/conflict rules and tests for customized files |

## Open Questions

No unresolved planning blockers remain. Detailed file paths and exact command filename conventions should be finalized during task implementation against Claude Code's current documented conventions.
