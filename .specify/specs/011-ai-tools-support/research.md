# Research: AI Tools Support

## Decision 1: Use one assistant support matrix as the source of truth

**Decision**: Treat the existing assistant configuration matrix in the CLI as the canonical machine-readable source for official assistant keys, display names, folders, install guidance, and CLI validation expectations.

**Rationale**: The current project already lists `claude`, `copilot`, `qwen`, `opencode`, and `qoder` in CLI metadata and public docs. A shared matrix prevents every assistant path from repeating support claims and reduces drift across README, docs, CLI help, templates, and generated outputs.

**Alternatives considered**:

- Maintain separate support lists per assistant path. Rejected because it caused the current Copilot-centered drift and increases release-audit cost.
- Infer assistants from directories found in a workspace. Rejected because a configured directory does not prove official support or full workflow coverage.

## Decision 2: Preserve initialized `.specify` core files by default

**Decision**: Existing initialized core files under `.specify` must be reused and reported as preserved or reused. Only missing core files are copied from templates by default.

**Rationale**: The requirement explicitly identifies existing initialized `.specify` files as user-maintained project state. Replacing them with template defaults can destroy updated instructions, memory, scripts, templates, skills, and workflow conventions.

**Alternatives considered**:

- Always copy templates with `dirs_exist_ok=True`. Rejected because it silently overwrites or mutates shared core assets.
- Require users to manually merge templates before adding a tool. Rejected because it blocks the main user goal of adding AI tools safely.

## Decision 3: Keep tool-specific assets isolated from canonical workflow assets

**Decision**: Assistant-specific commands, instruction links, settings, ignore files, and skill entry points should live under their assistant roots and reference canonical `.specify` files where appropriate.

**Rationale**: Multi-tool coexistence requires each tool to have its own compatibility surface without creating independent workflow sources. This mirrors the existing symlink model for instructions and skills.

**Alternatives considered**:

- Duplicate full workflow instructions into every assistant directory. Rejected because it creates divergence when canonical instructions evolve.
- Use only `.specify` without assistant-specific assets. Rejected because many tools need discoverable tool-specific command or guidance locations.

## Decision 4: Add structured initialization and refresh summaries

**Decision**: Initialization/refresh should collect and display a summary with created, reused, skipped, preserved, conflict, and attention-required categories.

**Rationale**: The requirements demand user-visible understanding of what happened. A structured summary also provides a basis for tests and release audits.

**Alternatives considered**:

- Rely on ad hoc console messages. Rejected because they are hard to validate and easy to miss.
- Only report errors. Rejected because reuse/preservation is successful but must still be visible to users.

## Decision 5: Extend validation through contract, integration, and unit tests

**Decision**: Cover assistant parity through contract tests for support surfaces, integration tests for filesystem outcomes, and unit tests for assistant metadata and preservation logic.

**Rationale**: Existing Qoder and Claude Code features already use this pattern successfully. This feature generalizes the pattern to all official assistants and repeat-run behavior.

**Alternatives considered**:

- Manual release checklist only. Rejected because it cannot reliably prevent regressions across five assistant surfaces.
- End-to-end CLI tests only. Rejected because unit-level preservation and summary logic need precise edge-case coverage.

## Decision 6: Fix workflow path helper consistency as a supporting requirement

**Decision**: Path helpers used by `.specify/scripts/bash/` must resolve `.specify/specs/<requirements-key>/requirements.md`, not legacy `specs/<branch>/spec.md` paths.

**Rationale**: Running `/speckit.plan` exposed a local helper mismatch that blocked plan creation until corrected. Reliable multi-tool initialization depends on the same script layer working for all assistants.

**Alternatives considered**:

- Work around the path mismatch only in the current plan. Rejected because downstream `/speckit.tasks` and assistant command flows would still be fragile.
- Move all specs to root `specs/`. Rejected because current docs and existing artifacts use `.specify/specs/`.
