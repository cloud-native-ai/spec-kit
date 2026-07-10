# Contract: Template Migration & Terminology

**Spec**: [requirements.md](../requirements.md) | **Plan**: [plan.md](../plan.md)

Normative rules for the rename/merge/terminology migration. Keywords per RFC 2119.

## M1. Canonical Template Location

`skills/create-agent/templates/` MUST be the single source of truth for agent templates; `.specify/skills/create-agent/templates/` is its installed mirror. Legacy `.specify/templates/agent-*` duplicates MUST be removed. No agent template MUST remain in the top-level `templates/` directory (FR-013, SC-003).

## M2. Stage Renames

| Old | New |
|-----|-----|
| `agent-subrole-executor-template.md` | `agent-stage-executor-template.md` |
| `agent-subrole-evaluator-template.md` | `agent-stage-evaluator-template.md` |
| `agent-subrole-improver-template.md` | `agent-stage-optimizer-template.md` |

The optimizer template's internal `name`/`description` MUST NOT contain "improver" (FR-014).

## M3. Supervisor Merge

`agent-role-meta-coordinator-template.md` and `agent-team-supervisor-template.md` MUST be merged into a single `agent-role-team-supervisor-template.md` (Meta role). The `organize-agents` Team Loop MUST be updated from three layers to two (Team Supervisor + Workers) (FR-007, Decision D2).

## M4. Terminology Substitution

Across all live templates, skills, orchestration files, docs, and tests: "SubRole"/"Subrole" MUST be replaced by "Stage" and "improver" MUST be replaced by "optimizer" (FR-015). Immutable history (`draft/`, `CHANGELOG`, prior `.specify/specs/*`, historical narrative in `features/019.md`) is excluded (Decision D5).

## M5. Reference Integrity

All references to template paths and stage names MUST resolve after migration. A dangling reference to a pre-migration path MUST be detectable (fail loudly), not silently resolve to nothing (FR-016, SC-004). The existing test suite MUST pass, and a deprecated-term / reference-integrity guard MUST be added.

## M6. Persisted-Agent Migration

Existing persisted agents under `.specify/agents/*.agent.md` (and `AGENTS.md`) MUST be migrated to the new model and terminology; 0 live persisted agents MUST retain deprecated concepts/terms (FR-020, SC-009).

## M7. Installed-Mirror Sync

Installed mirrors under `.specify/skills/**` and `.specify/templates/` MUST be re-synced from the refactored source so that source and installed copies are consistent (Constitution VI).
