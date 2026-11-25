# Checkpoint 05 — goal/team activation

## 1. Artifact verification

- **task threshold**: `goal-utils.py handoff-decision` = `handoff` (43 tasks > 10)
- **Anchor**: `.specify/anchoring/105-runtime-store-layout/anchor.md` — outcome-shaped objective, 3 criteria, active
- **Team**: `.specify/teams/105-runtime-store-layout/team.md` — serial, 5 seats, one reporter, shared-tree isolation
- **Handoff**: `.specify/specs/105-runtime-store-layout/handoff.md` — active, T001–T043, SC-001…SC-009
- **engine checks**: `run-checks` verdict `ok`, blocked `false`; reverse `handoff_ref` written on both definitions
- **roster guard**: `conforming: team 105-runtime-store-layout carries exactly one reporter seat`
- **render**: `specify render-agents --ai qoder` rendered 25 agents, 25 unmapped-intent notices (existing template metadata)
- **workspace signature**: tasks snapshot re-check `clean`; activation snapshot recorded
- **anomaly**: Anchor creation omitted the engine-owned binding block. `validate` accepts it as legacy, run-checks pass; this is recorded as F-OBS-4 and not hand-edited.

## 2. Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| FR/SC delivery (anchor criterion 1) | 0 / not started | construction has not run; spec tasks are ready |
| migration safety (criterion 2) | 0 / not started | fixture implementation is future work |
| memory/injection preservation (criterion 3) | 0 / not started | preservation tests are future work |

## 3. Team configuration review

- **evidence**: new team, run-checks pass; no prior run report
- **symptom**: n/a
- **proposal**: none
- **ratification**: n/a
- **applied**: no

## 4. Next stage concurrency / roster

- **requested**: 1; **effective**: 1; **reason**: `single-unit`
- **stage max_parallel**: 1; **verifier reserve**: 1
- **roster**: driver continues the checklist/analyze gates; construction crew remains idle until the implement handoff.

## 5. Direction audit

- **reload tier**: T0+T1
- **Q1 rules**: in force — unattended/no approval, U4→next, spine-before-action, workspace guard, fast-fail, gates, budget/report; push forbidden.
- **Q2 process**: correction-applied — the threshold was honored, the anchor/team/handoff were created through the engine/skill surfaces, and the Anchor binding omission is disclosed rather than hidden.
- **Q3 next action**: on-track — checklist is the next mandatory stage before analyze/implement.
- **Q4 spine freshness**: on-track — goal/team fields, activation evidence and next action recorded before this checkpoint.
- **Q5 territory/workspace**: on-track — workspace signature clean; team territory excludes all spec design faces and dated trees.
- **verdict**: `correction-applied`

## 5b. Published-state check

- **scope**: n/a — no history correction; no push authorized.