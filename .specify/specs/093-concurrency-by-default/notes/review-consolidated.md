# Review — consolidated record (segments A–D + ARC) — 093-concurrency-by-default

**Date**: 2026-11-09/10 · **Worktree**: `.specify/.tmp/sdd-loop/worktrees/093-review` · **Branch**: `093-review` @ `46bcb8716` · **Driver**: U4 consolidation

**Inputs**: `notes/review-process-artifacts.md` (A+B), `notes/review-implementation-code.md` (C+D), `notes/review-arc.md` (ARC). Each produced by an independent read-only fork; every fork's runner sentinel read 0 while its note carries the sentinel as the final line — recorded as a stage-runner derivation miss, not an artifact defect.

## 1. Segment verdicts and gate

| Segment | Verdict | Findings |
|---|---|---|
| A — process | pass | PF-1…PF-5, all P2 |
| B — artifacts | pass | AF-1, AF-3 (P1, truthfulness of record); AF-2/4/5/6/7/8/9 (P2) |
| C — implementation | pass with two evidence-record repairs | C-1, C-2 (important); C-3 (nitpick); every SC status reproduced; SC-006 `blocked` honest |
| D — code | pass with repairs | D-B1 (blocking: stale user-facing docs + dropped docs guards); D-I1/I2/I3 (important); suggestions |
| ARC | **ACCEPT sustained** | `verdict: block / final_path pass=5 blocked=1 total=6 / reason final-path-not-pass: SC-006`; close-out must land `Blocked`, record T098 open, fix the waiver sentence |

**Gate decision**: review gate **pass-with-mandatory-repairs** (A/B/C/D verdicts above; the P1/blocking items are record/doc/guard corrections, no behavioral falsification). Two parallel repair forks are dispatched on disjoint territories; the driver commits and re-verifies after both return.

## 2. Repair brief

**R1 — code / docs / guards** (territory `docs/reference/skills/`, `scripts/python/concurrency-check.py`, `shared/declarations/facts/serial-reason.yaml`, `tests/`):
- D-B1: update `docs/reference/skills/sdd-loop-driver.md` (lines 3/16/20) and `docs/reference/skills/sdd-project-setup.md` (lines 16/61) to the fork/subprocess carriers + the in-process ban; re-pin the docs assertions in `tests/contract/test_sdd_loop_driver_skill.py` and `test_sdd_project_setup_skill.py` (do not leave them dropped).
- D-I1: declare the `missing_mechanism` evidence extra-field in `serial-reason.yaml` (or accept both spellings) and read it from the engine; add a positive fixture for `mechanism-not-yet-landed`.
- D-I2: a present-but-non-list `units` field → emit `record-malformed`, never `effective=0 pass`.
- D-I3/C-2: add the three red-arm tests (undeclared stage; `off` without decision; partition under `--ceiling`) to `tests/unit/test_concurrency_check_engine.py` as `test_coverage_undeclared_stage_turns_red`, `test_coverage_off_without_decision_turns_red`, `test_coverage_partition_under_ceiling_turns_red`.
- D-S1: replace the two conditional skips in `test_concurrency_disposal.py` / `test_concurrency_real_run_evidence.py` with hard assertions.

**R2 — records / registry** (territory `.specify/specs/093-concurrency-by-default/`, `.specify/memory/features.md`, `.specify/memory/features/093.md`, `.specify/memory/register.md`, `.specify/state/093-concurrency-by-default.md`):
- AF-1: reword DoD-1's FR→row sentence to the measured clause statement (69/94 map, 39/94 row citations) and name the FR half as not machine-checked.
- AF-3: GATE-1 and DoD-3 → "zero NEW 093-caused failures" with the attribution surface (44 master-inherited + 2 trigger-order).
- AF-2/C-1: `test-evidence/wp5-gate1-comparison.txt` summary line → 207 failed / 8256 passed / 2 skipped, naming `wp5-suite-final.txt` as the source run; note the 211/8252 superseded run.
- AF-4: `quickstart.md` — (a) landed mechanism + the declared-order serial fold cause; (b) S-0 premise registered (live exit 0); (c) the S-5 command → `bash scripts/bash/run-tests.sh`.
- AF-5: reconcile the Work Packages table with the executed write domains (disclosed deviations; disjointness held for concurrent execution).
- AF-6: registry row 093 `Planned → Blocked` + Last Updated closure reason/date; `features/093.md` Implementation Notes + Latest Review; 33→36 FR; `features.md` header Total Features 88→89.
- AF-7: register T-001…T-005 (pointer shape); FR-036@093 → closed with T156–T159 evidence.
- AF-8: DoD-8 disposition vocabulary → the four-value closed set (C-079).
- AF-9: checklist live header — dated correction of the superseded subagent-capability and FR-count claims.
- ARC: `verification.md` SC-006 waiver sentence aligned to the state machine (no legal waiver exit; resolution = a future run with recorded intervals); record T098 as a genuinely open row; keep `deferred_tasks=` consistent.
- PF-3/PF-4: coordination-report worktree claim corrected; record the sigil/status state honestly (159 rows unflipped is the measured state; T098 open by design).
- SC-008/SC-011 pointer repairs: SC-008 cites the new red-arm tests; C-3 splits the 168-model-test attribution.

## 3. Close-out obligations (after repairs + driver U4)

1. Commit the review notes + repairs on `093-review`; fast-forward `093-concurrency-by-default`.
2. Close the line **blocked** (U6: a `block` verdict never becomes `completed`); registry lands `Blocked`.
3. Merge the line branch into master; resolve the known conflict on `tests/contract/test_stage_class_wiring.py` (master carries the humanize→humanize-conclusion pin; the 093 branch carries its own re-pins).
4. Carried residuals: SC-006 (needs a real run with per-unit intervals), SC-007/SC-010 partial, T098, F-093-002/020, the 116-minute provenance caveat, and the stage-runner sentinel-derivation miss.

**Anomaly line**: the runner sentinel read 0 for all three review forks while each artifact carries the sentinel as its final line — recorded as a derivation miss; no artifact defect.
