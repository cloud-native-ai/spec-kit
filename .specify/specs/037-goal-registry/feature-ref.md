# Feature Reference: 037-goal-registry

**Requirement key**: `037-goal-registry`
**Bound Feature**: **Feature 041 — Goal Registry**
**Feature detail**: `.specify/memory/features/041.md`
**Feature index row**: `.specify/memory/features.md`
**Status transition owned by this plan**: Draft → **Planned**

> Numbering caution: the requirement key `037` and the Feature ID `041` are different identifiers. Feature 037 is *Docs Command*, unrelated to this work. Always write "Feature 041", never a bare number.

## Why a new Feature rather than an existing one

Binding was resolved at the `/speckit.clarify` checkpoint. Feature 027 (Team Management) was the obvious candidate — requirement 036 had already extended it with goal-indexed summary aggregation — and it was rejected on scope:

- goal is a **project-level** concept whose consumers include objects outside the team domain (the host CLI's goal mechanism, and any reader asking "what is this project currently trying to achieve").
- Feature 027's charter is explicitly "team multi-agent configuration". Filing a project-level concept under it would contradict this requirement's core claim that goal is not a team attribute.

Feature 041 therefore records the goal concept itself, and 027 keeps the team side of the binding.

## Mapping: requirement → Feature 041

| Feature 041 key change | Requirement coverage |
|------------------------|----------------------|
| Authored definition archive (`goal.md`, three parts, three lifecycle states) | US1; FR-001…FR-007, FR-027…FR-032 |
| Team reference instead of copy | US2; FR-008…FR-012 |
| Consumer integration (036 summary sources narrative and milestones from the definition) | US3; FR-013…FR-015 |
| Single goal index (036's delivery directory consolidated under the goal archive) | FR-020…FR-024 |
| `/speckit.goal` as sole authoring entry | FR-025, FR-026 |
| Multi-team coordination (derived roster, team-level territory, overlap detection, proposal-only round) | US5; FR-033…FR-042 |
| Legacy migration, per-team and optional | US4; FR-016…FR-019 |

## Cross-references

- **Feature 027 (Team Management)** — owns the team side. Requirement 036 established the `goal_slug` aggregation key that this Feature supplies the missing definition source for, and this Feature relocates 036's delivery directory. `features/027.md` carries the reverse pointer.
- **Requirement 036 (`036-team-summary`)** — the direct upstream. Its aggregation semantics and identity grammar are preserved unchanged (FR-014); only the delivery path moves, and its assertions are updated for paths only (FR-024).
- **`shared/definitions/goal-definitions.md`** — the concept authority, **read-only** for this requirement. It fixes the Goal's composition, lifecycle, plane separation from Requirement, criteria authority, singularity, and binding semantics; it explicitly delegates the file layout inside `<goal-slug>/` to this Feature.

## Feature-list review for this plan

Per Constitution Principle II, this plan re-evaluated the Feature list:

| Question | Answer |
|----------|--------|
| Does this plan introduce new Features? | No. Feature 041 was already registered during clarification; this plan only advances its status |
| Does it deprecate or merge existing Features? | No. Feature 027 remains active and is cross-referenced, not absorbed |
| Does the functional/non-functional classification stay consistent? | Yes. 041 is a functional capability entry, consistent with 027 and 036 |
| Is the Feature detail updated with this plan's key changes? | Yes — `features/041.md` records the planned changes, implementation notes, and what the plan leaves open |

## Status gate

The canonical state machine (`.specify/templates/feature-details-template.md` § "Canonical Status State Machine") requires, for Draft → Planned: `plan.md`, `data-model.md`, `contracts/`, and `quickstart.md` exist for the bound requirement, and the Constitution Check carries no unjustified Fail rows.

| Requirement | State |
|-------------|-------|
| `plan.md` | present |
| `data-model.md` | present |
| `contracts/` | present — 4 contracts |
| `quickstart.md` | present |
| Constitution Check | 12 Pass / 1 Partial (Principle IX, justified in Complexity Tracking); zero Fail rows |

Gate satisfied. `/speckit.plan` lands `Planned` and MUST NOT land `Implemented` — that transition belongs to `/speckit.implement` once `tasks.md` has no open rows and `verification.md` carries a status line for all 18 success criteria.
