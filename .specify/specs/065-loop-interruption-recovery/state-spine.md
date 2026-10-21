# Line State Spine — spec-kit / 065-loop-interruption-recovery

**line_id**: speckit-065
**run_id**: r20261021T173459Z-0650
**state**: done (umbrella split confirmed; see split decision)
**current_stage**: split-confirmed (umbrella plan not pursued)
**tries**: 0
**updated_at**: 2026-10-21T17:34:59+08:00

## U0 entry declaration

- **target**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` (local topology)
- **terminal authority**: `.specify/specs/065-loop-interruption-recovery/notes/source-requirement.md` (dated brief snapshot) + `requirements.md` + `notes/decomposition-gate.md`
- **slice**: SDD 循环中断感知与状态恢复 — umbrella Feature 065; split required before plan
- **checkpoint**: U1 probe, not guessed
- **stage plan**: requirements → clarify → **plan (blocked)** → tasks → checklist → analyze → implement → review → local merge

## U1 probe

- branch: `065-loop-interruption-recovery`
- HEAD: `de566463` (`docs(065-loop-interruption-recovery): clarify requirements and bind feature 065`)
- dirty: 5 (run records only; no code changes)
- present: `requirements.md`, `checklists/requirements.md`, `notes/decomposition-gate.md`, `notes/source-requirement.md`
- absent: `plan.md`, `tasks.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`
- verdict: requirements + clarify complete; next stage = plan, but blocked by decomposition gate.

## Decomposition gate (blocking)

- command: `decomposition-check.py --mode plan --requirements .specify/specs/065-loop-interruption-recovery/requirements.md`
- result: **split-required** (exit 1)
- measured: `fr_count=52`, `fr_ceiling=30`
- reason: `FR definitions=52 exceeds ceiling 30`
- base_commit: `de566463`
- rule: `skills/external/sdd-loop-driver/references/efficiency-model.md` §5.3 — MUST NOT dispatch plan until a split record (counts, reasons, ceilings, proposed_slices, base_commit) is confirmed by the user or upstream flow.

### Proposed slices (proposal, not a decision)

| Slice | Theme | Core FRs | Count |
|---|---|---|---|
| `065a-state-awareness` | US1 + snapshot engine | FR-001…FR-012 | 12 |
| `065b-interruption-lifecycle` | US2 + US4 + check-spine | FR-013…FR-024 | 12 |
| `065c-recovery` | US3 + recover engine | FR-025…FR-037 | 13 |

Boundary D/E FRs (FR-038…FR-052) are allocated by applicability; US5 compatibility runs in every slice. Umbrella remains Feature 065; each slice gets its own spec directory and binds to Feature 065.

## Evidence pointers

- `requirements.md` (52 FR / 8 interruption forms / recovery actions)
- `checklists/requirements.md`
- `notes/decomposition-gate.md`
- `notes/source-requirement.md`
- branch `065-loop-interruption-recovery`, HEAD `de566463`
- no plan artifacts; no runner dispatched; no state/pid/log/heartbeat for plan.

## Split decision (confirmed 2026-10-21T17:35+08:00)

User confirmed the three-slice split and selected the execution order:

1. `065a-state-awareness` — **active slice**, spec dir `.specify/specs/065a-state-awareness/`, line `speckit-065a`
2. `065b-interruption-lifecycle` — queued
3. `065c-recovery` — queued

The umbrella Feature 065 remains the binding feature; each slice gets its own spec directory and binds to Feature 065. The umbrella plan is not pursued; the existing uncommitted umbrella draft plan artifacts are evidence only and MUST NOT be treated as a landed plan.

## Next action

`slice-065a-requirements` — see `/tmp/sdd-loader/speckit-065a/state-spine-065a.md`. Do not dispatch plan for the umbrella.
