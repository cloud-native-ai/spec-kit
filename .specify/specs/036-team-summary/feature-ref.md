# Feature Reference: `036-team-summary`

**Requirement → Feature**: `036-team-summary` → Feature 027 Team Management
**Feature detail**: `.specify/memory/features/027.md`
**Feature index row**: `.specify/memory/features.md` → `| 027 | Team Management | … |`
**Date**: 2026-08-04

## Binding

| Field | Value |
|-------|-------|
| Feature ID | 027 |
| Feature Name | Team Management |
| Binding decided at | `/speckit.clarify` session 2026-08-04 |
| Feature status before this plan | Implemented (from requirement `026-agent-team-management`) |
| Status transition this plan lands | Draft → **Planned** for the requirement; Feature 027 stays **Implemented** (no status regression per Principle VII) |

## Why 027 and not a new Feature

Feature 027 owns the entire team domain: `/speckit.team` (create / modify / run), the `create-team` + `improve-team` skills, and `.specify/teams/` persistence. Its own `## Future Evolution Suggestions` already predicted this requirement:

> Team run history/observability under `.specify/teams/` for improve-team evidence.

Every surface this requirement changes lies inside that domain — team configuration schema, the four patterns' execution-flow trigger points, the `/speckit.team run` confirmation gate, and the per-team delivery directory.

**Not bound to Feature 013 (Skills Command)** despite `summarize-project` being a skill: FR-024 forbids modifying that skill, so its lifecycle owner is not the change surface. Binding to 013 would misattribute the work.

## Many-specs-to-one-feature lineage

| Requirement | Role | Spec path |
|-------------|------|-----------|
| `026-agent-team-management` | Established the team domain | `.specify/specs/.archive/026-agent-team-management/` (Historical) |
| `036-team-summary` | Adds the summary information-management layer | `.specify/specs/036-team-summary/` (Latest) |

Per the Feature reuse-first workflow gate, this is an evolution spec appended to an already-`Implemented` Feature. Feature 027 is not reverted to `Planned`.

## How this plan maps to Feature 027

| Feature 027 asset | This plan's change |
|-------------------|--------------------|
| `templates/commands/team.md` | Run-mode confirmation gate discloses the summary decision (FR-016); output-discipline assertion corrected for the new directory entries |
| `skills/create-team/SKILL.md` | New SUMMARIZE phase in the continuous per-cycle loop; trigger points for the other three patterns; revised Rules / Hard Constraints bullets |
| `skills/create-team/references/` | New `summary-mapping.md` — the FR-001 concept-mapping single source of truth |
| `skills/create-team/scripts/` | New `build-summary-input.py` — the FR-008 deterministic form generator |
| `skills/improve-team/SKILL.md` | `config.summary` becomes a tunable surface (cadence, enablement, delivery directory) |
| `skills/create-team/templates/teams/*.md` | Three presets declare their pattern's default summary cadence |
| `.specify/teams/<slug>/` runtime layout | Adds tracked `items.jsonl` (team index — run info only) |
| `.specify/project/goal/<goal-slug>/` (new subtree) | The goal index — the sole complete summary delivery directory, coexisting with the pre-existing `.specify/project/` artifacts (FR-036) |

## Feature-list review (Principle II)

- **New Features introduced**: none. The mechanism is an evolution of the existing team domain.
- **Features deprecated or merged**: none.
- **Classification**: Feature 027 remains functional. No functional/non-functional reclassification.
- **Adjacent Feature affected**: Feature 013 (Skills Command) owns `summarize-project`'s lifecycle and is **explicitly not modified** — FR-024 and SC-003 assert byte-invariance of that skill, which is the guard that keeps this requirement inside 027's boundary.
- **Re-reviewed after the 2026-08-04 scope revision (dual index)**: the revision added FR-030…FR-036 and User Story 6, introducing a goal-indexed delivery directory under `.specify/project/`. This does **not** warrant a new Feature: `goal_slug` is a field on the team definition, goal membership is derived from team frontmatter, the aggregation runs inside the team-domain generator, and the trigger remains the team execution flow. The change is where output *lands*, not a new capability domain — so Feature 027 keeps ownership per the reuse-first gate, and no Feature is split or merged.
