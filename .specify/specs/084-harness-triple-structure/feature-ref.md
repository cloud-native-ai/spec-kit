# Feature Reference — 084

**Feature ID**: 084 | **Name**: Harness 三重结构（markdown + yaml + script）
**Requirement key**: `084-harness-triple-structure` → **Feature 084** (bound at `/speckit.clarify`, 2026-11-05)
**Spec**: `.specify/specs/084-harness-triple-structure/requirements.md`
**Feature detail**: `.specify/memory/features/084.md` | **Index row**: `.specify/memory/features.md`

## How this plan maps onto the Feature

| Feature-level statement (`features/084.md` § Key Changes) | Where this plan carries it |
|---|---|
| 1. New YAML declaration layer `shared/declarations/` | `contracts/declaration-schema.contract.md` (C-001…C-012); `data-model.md` E-1/E-2/E-3 |
| 2. New judging engine with three actions | `contracts/harness-triple-check.contract.md` (C-026…C-041); `data-model.md` E-8/E-10 |
| 3. Range and coverage criteria recomputed on the tree | `contracts/harness-triple-check.contract.md` C-030/C-031; `data-model.md` E-4/E-5/E-6 |
| 4. Three migration batches, each independently acceptable | `contracts/migration-batches.contract.md` (C-042…C-051) — the first roster the spec asked the plan for |
| 5. Owner documents become pointers, criteria stay | `contracts/migration-batches.contract.md` C-047/§ Verification; `plan.md` § Mirror Obligations for the copies |
| 6. Distribution and bounded compatibility | `contracts/distribution-and-mirror.contract.md` (C-013…C-025) — the asset roster and upgrade actions the spec asked the plan for |

## Status movement this plan is responsible for

`Draft → Planned` in `.specify/memory/features.md` and `.specify/memory/features/084.md`. The ceiling is `Planned`:
`Implemented` belongs to `/speckit.implement`, and this plan does not touch any other Feature's status. Feature 081
stays `Completed`; the only reference to it here is the A8(a) hard constraint (its acceptance tests move by zero).

The two list deliverables that `features/084.md` § Status Tracking names as the `Planned` precondition are landed here:
the first migration roster (`contracts/migration-batches.contract.md` C-042) and the `specify init` asset roster with
its upgrade actions (`contracts/distribution-and-mirror.contract.md` § A).

## Delivery surface (what the Feature row must report when the work lands)

- `shared/declarations/` (framework source) + `.specify/shared/declarations/` (generated mirror)
- `shared/definitions/harness-triple-definitions.md` (owner doc) + its mirror
- `scripts/python/harness-triple-check.py`, `scripts/python/declaration_reader.py` + their strict mirror pair
- the five owner documents turned into pointers, plus `shared/definitions/framework-map.md`'s new directory rows
- `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` (opt-in delegation) + mirror
- `tests/contract/test_harness_triple_structure.py`, `tests/fixtures/harness-triple-structure/`
- `docs/` pointer page, `CHANGELOG.md` entry

## Decomposition

`decomposition-check.py --mode plan` → `proceed` (`fr_count` 19, ceiling 30). Decision: **`single-package`**, no slice
split. The `tasks` ceiling is read by the gate at the tasks stage; this plan deliberately pre-commits no task count.
