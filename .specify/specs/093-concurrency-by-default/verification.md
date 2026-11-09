# Verification Log — 093-concurrency-by-default

**Stage**: implement (WP5 release wave) · **Run**: `r202609...-wp5` · **Branch**: `093-wp5` · **Base**: `6001c9ad1`
**Authority**: `requirements.md` (FR-001…FR-036 / SC-001…SC-012) · `plan.md` · `contracts/` (94 clauses)
**Baseline**: `notes/test-baseline.txt` (161 serial failed ids, frozen by WP1 T002)

## Success criteria (human view — the machine block below is the record)

| Criterion | Path | Status | Evidence | Reading |
|---|---|---|---|---|
| SC-001 | final | **pass** | `test-evidence/wp5-t034-t040-class-obligations.txt`, `test-evidence/wp5-t028-t043-t045-mutations.txt`, `tests/contract/test_concurrency_class_table.py` | classify live: pass, 0 uncovered / 0 ambiguous, root counts measured (agents 17 / anchoring 6 / commands 29 / skills 54 / teams 12); both drift mutations red |
| SC-002 | final | **pass** | `tests/contract/test_concurrency_serial_reason.py::test_default_concurrency_fixture_reads_effective_two`, `tests/contract/test_concurrency_high_order.py::test_reverting_analyze_to_off_turns_the_judgement_red` | the two-unit fixture reads effective 2; reverting the stage default to serial turns the judgement red |
| SC-003 | final | **pass** | `test-evidence/wp5-t028-t043-t045-mutations.txt`, `tests/contract/test_concurrency_serial_reason.py` | closed vocabulary + form-matching evidence; both C-030 shapes red; bijection mutations red in both directions |
| SC-004 | final | **pass** | `tests/contract/test_concurrency_units.py`, `test-evidence/wp5-t062-t085-unit-obligations.txt` | seven obligations each with a fixture (partition replay, file-level write domain, slot+reserve arithmetic, verifier independence, declared-order integration, failure isolation, re-entry); separately, the retained 070 model suites (`tests/contract/test_sdd_loop_driver_wp_coordination.py`, `tests/contract/test_sdd_loop_driver_wp_model.py`) read 168 passed — a retained-suite reading, not part of the seven 093 fixtures (C-3 split) |
| SC-005 | final | **pass** | `test-evidence/wp5-t090-reproduction-092.txt`, `tests/contract/test_concurrency_reproduction_092.py` | the 092 shape is accepted by a pre-repair engine copy (exit 0) and refused by the repaired engine (exit 1, two `declaration-execution-mismatch` findings) |
| SC-006 | final | **blocked** | `notes/coordination-report.md`, `notes/serial-baseline.md`, `test-evidence/wp5-t110-t112-coordination-coverage.txt` | this feature's own run was a serial fold: `effective: not_evaluated`, reason `mechanism-not-yet-landed`; no real run with effective >= 2 exists — not `0`, not an estimate |
| SC-007 | supporting | **partial** | `test-evidence/wp5-t110-t112-coordination-coverage.txt`, `test-evidence/wp2-t109-t113-t119.txt` | goal: partition fixture measured (5 targets → [3,2]; <2 available → serial with `budget-reserve`); team/loop: obligations stated in their owner documents and the territory machinery is retained, but no executable team/loop concurrency fixture exists this run |
| SC-008 | supporting | **pass** | `test-evidence/wp5-t110-t112-coordination-coverage.txt`, `tests/unit/test_concurrency_check_engine.py::test_coverage_undeclared_stage_turns_red` (+ the sibling red arms `::test_coverage_off_without_decision_turns_red`, `::test_coverage_partition_under_ceiling_turns_red`) | every stage resolves through `decomposition-coverage.yaml` (requirements/tasks covered-by-default, analyze `on`); an undeclared stage, an `off` stage without a named decision, and a partition under `--ceiling` each turn the judgement red |
| SC-009 | supporting | **pass** | `test-evidence/wp5-t017-t019-owner-unavailable.txt` | unregistered / broken / unparsable facts all read `owner-unavailable` at exit 2 with a named message; no default is produced |
| SC-010 | supporting | **partial** | `notes/disposal-ledger.md`, `test-evidence/wp5-gate1-comparison.txt`, `test-evidence/wp5-suite-final.txt` | the 064/070/077/086/092 dispositions are recorded and the re-pin set is green; the literal "whole suite green" is not met because 161 frozen-baseline + 44 master-inherited + 2 trigger-order reds sit outside this feature's write domain — zero NEW 093-caused names remain |
| SC-011 | supporting | **pass** | `tests/contract/test_concurrency_high_order.py::test_anti_nesting_chain_is_depth_two_with_its_three_prohibitions` | dispatch depth stays 2 with the three prohibitions; the tamper mutation reds |
| SC-012 | supporting | **pass** | `tests/unit/test_concurrency_check_engine.py::test_cost_benefit_fixture_identical_result_set_lower_wall_clock` | the fixture's concurrent form yields an identical result set with a lower wall clock |

`[final]`-path criteria not `pass`: **SC-006** (`blocked`) — the gap is the missing executed concurrent run,
not missing work. A user waiver is **not** a legal exit here: the waiver clause belongs to
`Implemented → Ready for Review`, a gate unreachable while the feature is not `Implemented`; `Blocked → Ready
for Review` is illegal, and `Blocked → Implemented` requires the blocker lifted **and** every `final`-path
criterion `pass` (both, not either). The resolution is a future run that dispatches `>= 2` units, records
per-unit `dispatched_at` / `settled_at` intervals, and re-reads this row (`SC-006_unblock`).

**Open task rows at this record's date**: `tasks.md` holds 159 `- [ ]` rows (closure reading
`tasks: {closed: 0, open: 159}`); flipping the state sigils is the integration owner's close-out act, never
this record's. **T098 is genuinely open by design** — the coordinator-dispatch verdict value awaits its owner
(F-093-003), and `notes/implement-wp1.md` records the row that way; it is open, not deferred, which is why
`deferred_tasks=` below stays empty.

## Machine-readable record

The schemas projected here are owned by `shared/workflow/acceptance-hardening.md` § Verification
Vocabulary; this file is a declared carrier and does not widen a value domain.

```text
# -- Baseline --

baseline_commit=6001c9ad1
baseline_date=2026-11-09
baseline_branch=093-wp5
baseline_failed_ids=161 (.specify/specs/093-concurrency-by-default/notes/test-baseline.txt)

# -- Smoke test record (exactly one per feature — the only copy of these three keys in this file) --

smoke_command=bash scripts/bash/run-tests.sh tests/contract/test_concurrency_declarations.py tests/contract/test_concurrency_class_table.py tests/contract/test_concurrency_serial_reason.py tests/contract/test_concurrency_units.py tests/contract/test_concurrency_high_order.py tests/contract/test_concurrency_dispatch_capability.py tests/contract/test_concurrency_disposal.py tests/contract/test_concurrency_real_run_evidence.py tests/contract/test_concurrency_reproduction_092.py tests/contract/test_test_entry_guard.py tests/unit/test_concurrency_check_engine.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/093-concurrency-by-default/test-evidence/wp5-acceptance-final.txt

# -- Success Criteria evaluation --

SC-001_status=pass
SC-001_value=classify: pass, 0 uncovered / 0 ambiguous; roots measured 17/6/29/54/12; both drift mutations red
SC-001_note=see § Success criteria row SC-001

SC-002_status=pass
SC-002_value=two-unit fixture effective 2; analyze-default revert turns the judgement red
SC-002_note=see § Success criteria row SC-002

SC-003_status=pass
SC-003_value=both form/reason shapes red; bijection mutations red in both directions; evidence forms enforced per code
SC-003_note=see § Success criteria row SC-003

SC-004_status=pass
SC-004_value=seven obligations each fixture-backed; separately, the retained 070 model suites read 168 passed (a retained-suite reading, not one of the seven 093 fixtures)
SC-004_note=see § Success criteria row SC-004

SC-005_status=pass
SC-005_value=092 shape: pre-repair copy exit 0 (accepted) vs repaired engine exit 1 with 2 mismatch findings
SC-005_note=see § Success criteria row SC-005

SC-006_status=blocked
SC-006_value=effective not_evaluated (serial fold, intervals not recorded); 091 baseline 62 tasks / 1 agent / 116 minutes cited
SC-006_note=see § Success criteria row SC-006 and notes/coordination-report.md
SC-006_blocked_at=no real run with effective >= 2 exists; the feature's own fold ran serially
SC-006_reduced_measurement=the reproduction and reading fixtures measure the mechanism's semantics (effective-from-overlap, not_evaluated on missing intervals)
SC-006_reduced_measurement_run=yes
SC-006_why_reduced_insufficient=fixtures prove the judgement, not that a real executor dispatched concurrently; SC-006 requires the non-fixture reading
SC-006_unblock=the next run that actually dispatches >= 2 units and records their intervals, then re-read this row

SC-007_status=partial
SC-007_value=goal partition fixture measured; team/loop obligations stated in owner documents; no executable team/loop concurrency fixture this run
SC-007_note=supporting path — see § Success criteria row SC-007
SC-007_blocked_at=team binding-time and loop per-stage readings exist as owner text but have no dedicated fixture row
SC-007_reduced_measurement=goal-target partition measured through the coverage action (5 targets -> [3,2]; degraded -> budget-reserve)
SC-007_reduced_measurement_run=yes
SC-007_why_reduced_insufficient=the goal fixture does not exercise a team's seat-territory binding or a loop stage's per-unit reading
SC-007_unblock=add the two fixture rows (team territory binding, loop per-stage reading) and re-run

SC-008_status=pass
SC-008_value=all 8 stages resolve through the fact; off-without-decision -> coverage-undeclared
SC-008_note=supporting path — see § Success criteria row SC-008

SC-009_status=pass
SC-009_value=absent / broken / unparsable facts -> owner-unavailable exit 2, named message, no default
SC-009_note=supporting path — see § Success criteria row SC-009

SC-010_status=partial
SC-010_value=dispositions recorded (12 ledger rows); zero NEW 093-caused failures vs the frozen baseline; 161 baseline + 44 master-inherited + 2 trigger-order names remain
SC-010_note=supporting path — see § Success criteria row SC-010
SC-010_blocked_at=the literal whole-suite-green is not measured on this tree; inherited reds sit outside this feature's write domain
SC-010_reduced_measurement=GATE-1 name-set comparison vs the frozen baseline, classified per name (wp5-gate1-comparison.txt)
SC-010_reduced_measurement_run=yes
SC-010_why_reduced_insufficient=a red set reduced to zero NEW is not the same claim as an all-green suite
SC-010_unblock=the owners of the inherited reds repair them (094 scope vocabulary, trigger-order family), or the baseline is formally re-frozen with a dated record

SC-011_status=pass
SC-011_value=depth 2 + three prohibitions pinned; the stage-can-carry-driver tamper reds
SC-011_note=supporting path — see § Success criteria row SC-011

SC-012_status=pass
SC-012_value=identical result set with lower wall clock on the cost-benefit fixture
SC-012_note=supporting path — see § Success criteria row SC-012

# -- Joint acceptance (in-scope runtime-stack rows only: RS-003, RS-004) --

RS-003_joint_acceptance=pass
RS-004_joint_acceptance=pass

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=none deferred (no `[~]` row exists); all 159 task rows read `- [ ]` at this record's date and the sigil flip is the integration owner's close-out act, not this record's; T098 is genuinely open by design (F-093-003), not deferred

# -- Free-form notes --

notes=the two WP4 modules that skipped on not_evaluated (T110 report, T134 ledger) now run and pass; the acceptance suite reads 96 passed / 0 skipped; see notes/implement-wp5.md for the per-row closure record.
```

## Gate readings carried by this record

- **GATE-1**: `test-evidence/wp5-suite-final.txt` (207 failed / 8256 passed / 2 skipped) compared
  name-by-name against the frozen baseline — **0 NEW 093-caused failures**; the 46 NEW names are 44
  master-inherited and 2 trigger-order (evidence: `wp5-gate1-comparison.txt`).
- **GATE-2**: `test-evidence/wp5-t130-t131-release-parity.txt` — `sync-mirrors.py --check` exit 0,
  `regen-command-copies.py --check` exit 0.
- **GATE-5**: `script-interface-check` reading in `test-evidence/wp2-t021-t025.txt` (WP2) plus the
  release re-run recorded in `notes/implement-wp5.md`.
- **GATE-6**: `test-evidence/wp5-validate-tasks.txt` — PASS, 0 error / 0 warning, 159 rows;
  `test-evidence/wp5-validate-requirements.txt` — 0 error / 0 warning (345 lines / 48 definitions / 11 strings).
- **GATE-7**: this record cites `086:SC-010` as inherited: 086's own gate keeps it; 093 neither closes
  nor inherits the gap (plan.md § Inherited Blockers row 1).
