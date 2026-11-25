# Checkpoint 05 — goal/team activation

## 1. Artifact verification

- **task threshold**: `goal-utils.py handoff-decision` = `handoff` (37 tasks > 10)
- **Anchor**: `.specify/anchoring/106-background-silent-failure/anchor.md` — outcome-shaped objective, 3 criteria, active, engine-created
- **Team**: `.specify/teams/106-background-silent-failure/team.md` — serial, 5 seats, exactly one reporter, shared-tree isolation
- **Handoff**: `.specify/specs/106-background-silent-failure/handoff.md` — handoff/v1, active, T001–T037, SC-001…SC-009
- **engine checks**: `handoff-ref` wrote the anchor reference; `validate-roster` conforming; `run-checks` verdict `ok`, `blocked: false`; anchor `validate` valid
- **render**: `specify render-agents --ai qoder` → 25 rendered / 25 unmapped-intent notices; manifest + one re-rendered agent surface
- **workspace signature**: activation artifacts are new files; tasks snapshot re-check `clean` before this checkpoint
- **anomaly**: U0 `goal_team: none` corrected here (engine decides the direct/handoff axis; 37 > 10 → handoff). Disclosed, not silent.

## 2. Goal progress

| criterion | degree | evidence_ptr |
|---|---|---|
| FR/SC delivery (anchor criterion 1) | 0 / not started | construction has not run; 37 tasks are ready |
| Carrier settlement coverage (criterion 2) | 0 / not started | carrier implementation is future work |
| Preserved surfaces (criterion 3) | 0 / not started | preservation tests are future work |

## 3. Team configuration review

- **evidence**: new team, run-checks pass; no prior run report
- **symptom**: n/a
- **proposal**: none
- **ratification**: n/a
- **applied**: no

## 4. Next stage concurrency / roster

- **requested**: 1; **effective**: 1; **reason**: `single-unit`
- **stage max_parallel**: 1; **verifier reserve**: 1
- **roster**: driver continues checklist → analyze gates; construction crew idle until the implement handoff

## 5. Direction audit

- **reload tier**: T0+T1
- **Q1 rules**: in force — unattended/no approval, U4→next, spine-before-action, workspace guard, fast-fail, gates, plan constraint, budget/report; push forbidden.
- **Q2 process**: correction-applied — the U0 goal/team decision was corrected by the engine reading and the activation executed; no report substituted for execution.
- **Q3 next action**: on-track — checklist is the next stage in the plan after activation.
- **Q4 spine freshness**: on-track — activation record and `goal_slug`/`team_slug`/`origin_spec_dir` written before this checkpoint.
- **Q5 territory/workspace**: on-track — activation touched only anchor/team/handoff, the render manifest and one generated agent surface.
- **verdict**: `correction-applied`

## 5b. Published-state check

- **scope**: n/a — no history correction
