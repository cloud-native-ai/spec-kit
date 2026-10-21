# Feature Reference — 065 Loop Interruption Awareness & Recovery

**Requirement → Feature**: `065-loop-interruption-recovery` → Feature 065 SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）
**Plan**: [plan.md](plan.md) | **Spec**: [requirements.md](requirements.md) | **Date**: 2026-10-21

## Binding

| Item | Value |
|------|-------|
| Feature ID / status | 065 / `Draft → Planned` at the end of this plan run |
| Binding form | New Feature bound at `/speckit.clarify` (Mode A) on 2026-10-21 |
| Registry row | `.specify/memory/features.md` row 065 |
| Detail file | `.specify/memory/features/065.md` |
| Owner surfaces | Existing mechanisms stay with their owners: 058 (U0–U6, spine, sentinels, U4/U5, watcher verdicts), 063 (fast lane, test budget, plan constraint, plan-owned artifacts), 064 (Registry, envelope, lease, reservation, ownership) |
| New surface | `references/state-awareness.md` (rules), `scripts/loop-state.py` (engine), watchbeat marker, spine machine segment, recovery record/actions |

This plan does not create a new Feature, merge or split an existing one, or change another Feature's status. The new capability is an additive layer over Feature 058's loop and Feature 064's registry; Feature 065 owns only the observation/recovery rules and their records.

## FR coverage

| FR | Owning artifact / contract |
|----|----------------------------|
| FR-001 | `references/state-awareness.md` § Entry; LS-01–LS-04, LS-13; `scripts/loop-state.py` |
| FR-002 | LS-05–LS-07, LS-22; SN-05–SN-06 |
| FR-003 | SN-01–SN-04; LS-08; data-model E-01/E-02 |
| FR-004 | SN-08–SN-20; owner reference § Derived Loop State (D0–D8) |
| FR-005 | SN-07–SN-09; LS-20–LS-21 |
| FR-006 | data-model E-09; SN-21–SN-22; NR-22 |
| FR-007 | SN-21, SN-27 |
| FR-008 | SN-23–SN-26 |
| FR-009 | SN-28–SN-37; owner reference § Interruption Forms (I1–I8) |
| FR-010 | SP-23–SP-27; owner reference § Watchbeat |
| FR-011 | SN-28, SN-38–SN-39 |
| FR-012 | LS-09–LS-12; SN-44; `--self-test` case list |
| FR-013 | SN-28 (I1) |
| FR-014 | SN-29 (I2) |
| FR-015 | SN-30 (I3); RC-28 |
| FR-016 | SN-31 (I4) |
| FR-017 | SN-32 (I5); SN-27 |
| FR-018 | SN-33 (I6) |
| FR-019 | SP-29; SKILL.md Hard Requirements |
| FR-020 | SP-30; SKILL.md Hard Requirements |
| FR-021 | SP-01–SP-22; `check-spine` |
| FR-022 | SP-01–SP-09, SP-21 |
| FR-023 | SN-44; LS-13 |
| FR-024 | SN-06, SN-35, SN-42; LS-07 |
| FR-025 | RC-01–RC-05 |
| FR-026 | RC-03 (AD-1–AD-9) |
| FR-027 | RC-11–RC-13 |
| FR-028 | RC-15–RC-16; LS-19 |
| FR-029 | RC-14 |
| FR-030 | RC-19–RC-22 |
| FR-031 | RC-22–RC-24 |
| FR-032 | RC-25–RC-31 |
| FR-033 | RC-07–RC-09; SP-28 |
| FR-034 | RC-10 |
| FR-035 | LS-14–LS-15; RC-32–RC-33 |
| FR-036 | RC-18, RC-24, RC-31, RC-34 |
| FR-037 | RC-37; SN-02, SN-07 |
| FR-038 | NR-01; research § 0.2 |
| FR-039 | NR-02, NR-04 |
| FR-040 | NR-03 |
| FR-041 | NR-05; LS-01 |
| FR-042 | NR-09, NR-10, NR-14 |
| FR-043 | owner reference; NR-12; SP-31 |
| FR-044 | NR-11–NR-13 |
| FR-045 | NR-15–NR-21; test matrix |
| FR-046 | NR-19 (mutation drills) |
| FR-047 | NR-08; RC-36 |
| FR-048 | LS-16–LS-18; RC-34–RC-36 |
| FR-049 | NR-06; RC-13, RC-27–RC-28 |
| FR-050 | RC-19, RC-28; NR-06 |
| FR-051 | RC-15–RC-16; SN-27 |
| FR-052 | NR-01–NR-03; RC-10 |

## SC coverage

| SC | Evidence route |
|----|----------------|
| SC-001 | Integration S1 accident replay (NR-17); no manual per-file inspection |
| SC-002 | SN-28–SN-37 + eight-form fixtures (NR-15/NR-17); zero false `unwatched` on a fresh marker |
| SC-003 | RC-11–RC-18; commit path assertions in `test_loop_state.py` |
| SC-004 | RC-19–RC-24; `attempts/` inventory and zero-deletion assertions |
| SC-005 | RC-25–RC-31; handoff four-element assertions; no-kill check |
| SC-006 | SP-17–SP-22; valid/invalid/legacy spine matrix |
| SC-007 | NR-01, NR-18; watcher `--self-test` 38/0 and exit-code comparison |
| SC-008 | NR-09–NR-14; mirror check, docs page, dependency scan |
| SC-009 | SN-43; RC-18/RC-24/RC-31; deterministic diff excluding timestamps |
| SC-010 | NR-19; three mutation drills each turn a named test red |

## Deliverables

| Path | Change |
|------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` | New State Awareness & Recovery section; Hard Requirements lifecycle lines; References rows |
| `skills/external/sdd-loop-driver/references/state-awareness.md` | NEW owner reference (state awareness, D0–D8, I1–I8, AD-1–AD-9, spine/watchbeat, lock, handoff) |
| `skills/external/sdd-loop-driver/references/stage-prompts.md` | Pointer edits at the state-spine section: machine segment, `check-spine` call points, watchbeat writes (no restated rules) |
| `skills/external/sdd-loop-driver/references/dispatch-recipes.md` | Pointer edit in Recipe 3: same-turn first window and watchbeat |
| `skills/external/sdd-loop-driver/scripts/loop-state.py` | NEW engine (snapshot/recover/check-spine/self-test) |
| `.specify/skills/sdd-loop-driver/**` | Generated mirror via `sync-mirrors.py --write --only skills/external/sdd-loop-driver` |
| `docs/reference/skills/sdd-loop-driver.md` | Entry, actions, watchbeat/lifecycle, relationship to watcher/Registry |
| `tests/unit/test_loop_state.py` | NEW unit suite |
| `tests/contract/test_sdd_loop_driver_state_awareness.py` | NEW contract suite |
| `tests/integration/test_loop_state_interruption_matrix.py` | NEW integration matrix |
| `tests/contract/test_sdd_loop_driver_skill.py` | Update pinned H2 and mirror file lists only |
| `.specify/memory/features.md`, `.specify/memory/features/065.md` | Status `Draft → Planned`, last-updated and plan note |
| `.specify/specs/065-loop-interruption-recovery/` | This plan, research, data-model, contracts, quickstart, feature-ref |

## Related features and boundaries

- **058**: U0–U6, state spine, sentinels, U4/U5 and watcher verdicts remain owned by 058. 065 adds observation, recovery and lifecycle validation only.
- **063**: fast lane, test budget, plan constraint and plan-owned artifact set remain owned by 063. 065 consumes the plan-owned set and the stage base commit.
- **064**: Registry, envelope, lease, reservation and ownership remain owned by 064. 065 reads the Registry entry and never changes its state machine or actions.
- **Feedback/probe**: no new recording engine; any framework observation goes through the existing feedback/probe mechanisms.

## Planning gate record

The decomposition gate measured 52 FR against a ceiling of 30 and returned `split-required` (`notes/decomposition-gate.md`). The upstream driver dispatched this plan for the full Feature 065; per `efficiency-model.md` §5.3.3 that dispatch is the upstream-flow confirmation to advance. No FR is deleted, merged or reordered. The `tasks` U4 gate remains in force; the plan targets ≤40 task rows and the driver must resolve any further `split-required` before `analyze`.
