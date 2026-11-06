# Checkpoint 06 — analyze

## 1. Artifact verification

- sentinel: `ANALYZE-DONE`
- U4: **pass (read-only)** — evidence: `test-evidence/analyze-findings.md`; the analyze stage modified no
  requirements/plan/tasks/contracts/source/template/test/085 path; only its Wrap-up records and
  `.specify/.tmp/086/analyze-coverage.json` exist
- findings: **1 CRITICAL / 5 HIGH / 13 MEDIUM / 5 LOW** (see the findings file)
- anomaly: `ANOMALY: analyze findings block implement until the driver repairs them; C-01 (contract FR citations) is a deterministic red, H-01 (085 live-status carve-out) spans FR-027/C-041/GATE-5/M-16/team/WP-C2/R-8/T041, H-02 (PYTHONPATH) is an unstated premise, H-03/H-04/H-05 affect mutation legs, baseline timing and the two-slot budget.`

## 2. Temporary Goal progress

- goal: `.specify/specs/086-efficient-test-execution/goal/086-efficient-test-execution/goal.md` (active)

| criterion | degree | evidence_ptr |
|---|---|---|
| Full-suite parallel wall-clock ≤ 40% of the 1031.48 s serial baseline. | not_evaluated | analyze; implementation pending |
| Final parallel run has zero new failure names vs the serial baseline, serial exceptions declared. | not_evaluated | analyze H-04/H-05; implementation pending |
| Principle ships in constitution template/live, instructions template/live, one owner guideline. | not_evaluated | analyze M-06/M-13; implementation pending |
| 085 temporary Goal/Team, concurrency, worktree/integration queue and checkpoints are used and green. | not_evaluated | analyze H-01; implementation pending |
| Feature reaches Ready for Review with zero blocking review findings. | not_evaluated | analyze findings; review pending |

## 3. Team configuration review

- evidence: team file; analyze stage used the `sdd-analysis-worker` seat
- symptom: one CRITICAL + five HIGH artifact defects before implementation
- proposal: no team configuration change; the repair pass is driver-owned artifact correction
- ratification: n/a
- applied: no

## 4. Next stage concurrency / roster

- stage: **repair pass (driver-owned) → implement**
- requested: 24; planned effective for implement: **10** (7 ready work packages WP-A1…A4 + WP-B1…B3 +
  3 verifier reserve; host/team cap 18 is not binding)
- stage max_parallel: 18 (team implement cap); verifier reserve: 3; executor slots: 7
- roster: `sdd-implement-coordinator` + `sdd-implement-executor` (host-native carriers) +
  `sdd-stage-verifier`/`sdd-stage-integrator`; WP-A/WP-B first wave, WP-C after integration
- gate: implement dispatch only after the repair pass and the re-run validate/coverage/pre-analyze/
  decomposition gates pass.
