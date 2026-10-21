# Decomposition Gate Record — Feature 065

**Date**: 2026-10-21
**Gate**: plan 入口（requirements U4 后、plan 派发前）
**Owner rule**: `skills/external/sdd-loop-driver/references/efficiency-model.md` §5
**Command**:

```text
python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py \
  --mode plan \
  --requirements .specify/specs/065-loop-interruption-recovery/requirements.md
```

**Result**: `split-required` (exit 1)

```json
{"mode": "plan", "decision": "split-required", "measured": {"fr_count": 52, "task_count": null, "fr_ceiling": 30, "task_ceiling": 40}, "reasons": ["FR definitions=52 exceeds ceiling 30"]}
```

## Blocking effect

Per §5.3, the driver MUST NOT dispatch plan until a split record carrying the measured counts, reasons, ceilings, `proposed_slices[]` and `base_commit` is written to the line state spine and confirmed by the user or upstream flow. This note is evidence for that record; the state spine remains the driver's authoritative record.

## Proposed slices (proposal, not a decision)

| Slice | Theme | Core FRs | Count | Headline value |
|-------|-------|----------|-------|----------------|
| `065a-state-awareness` | US1 + snapshot engine | FR-001…FR-012 | 12 | one-call read-only state awareness |
| `065b-interruption-lifecycle` | US2 + US4 + check-spine | FR-013…FR-024 | 12 | eight interruption forms + lifecycle validator |
| `065c-recovery` | US3 + recover engine | FR-025…FR-037 | 13 | resume/retry/stop + salvage + isolation + lock |

All slices allocate the D boundary FRs (FR-038…FR-048) and E boundary FRs (FR-049…FR-052) by applicability; US5 compatibility acceptance runs in every slice. Each core slice is within the 8–30 FR band. The umbrella remains Feature 065; each slice gets its own spec directory and binds to Feature 065. The driver or user MUST confirm the split before any slice advances.

## Re-run

After a split decision, re-run the gate per slice. Do not delete, merge or reorder FRs to evade the ceiling (§5.3.4).

## Dispatch attempt halted (2026-10-21)

A `/speckit.plan` dispatch for the umbrella Feature 065 arrived while this gate was still blocking. The line state spine (`state-spine.md`) records `state: stalled`, `current_stage: plan (not dispatched)` and "Do not dispatch plan for the umbrella"; the gate re-measured `split-required` (`fr_count=52`, ceiling 30, exit 1). The plan stage therefore halted instead of treating its own dispatch as the §5.3.3 confirmation: that would be self-confirmation, not a user/upstream decision.

Draft plan artifacts were produced for review but are **not committed** and MUST NOT be treated as a completed plan. To advance, the user/upstream flow must either (a) confirm the three-slice split (`065a`/`065b`/`065c`) and update the state spine, or (b) record an explicit decision that overrides the decomposition gate in the state spine. Independent review findings against the draft are recorded in `notes/plan-blocked-review.md`; they must be fixed before any plan is landed.
