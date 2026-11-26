# Acceptance Evidence — SC-001…SC-009 (T034, spec 106)

Every row: status, the `requirements.md` path kind (final / supporting — labels match the
requirements table), the measurement command, the real output (decisive excerpt) and the
evidence pointer. All measurements were taken 2026-11-26 on branch
`106-background-silent-failure` at the T033 head (`6bc7a1bdd`); every test run went
through the unique entry `scripts/bash/run-tests.sh`.

| SC | Path | Status | Reading |
|----|------|--------|---------|
| SC-001 | final | **pass** | see § SC-001 |
| SC-002 | final | **pass** | see § SC-002 |
| SC-003 | supporting | pass | § SC-003 |
| SC-004 | final | **pass** | § SC-004 |
| SC-005 | supporting | pass | § SC-005 |
| SC-006 | supporting | pass | § SC-006 |
| SC-007 | supporting | pass | § SC-007 |
| SC-008 | supporting | pass | § SC-008 |
| SC-009 | supporting | pass | § SC-009 |

## SC-001 — dead / half-dead fixtures settle `silent-end`, unreadable settles `unknown`; zero misreads

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q -k "silent or zombie or pid_reuse or live"`
- Output: `16 passed in 6.29s` (rc 0).
- Dead fixtures: `test_silent_end_is_a_judged_attempt_not_a_violation`,
  `test_c2_sigkill_silent_death_settles_silent_end` (real `dispatch.sh` + SIGKILL —
  also the S-1 quickstart reading: `silent-end` / `pid-gone`, exit 0),
  `test_c3_seat_with_start_record_and_no_report_row_settles_silent_end`,
  `test_late_completion_after_the_deadline_lands_on_its_own_label` (C4, `deadline-passed`).
- Half-dead: `test_c2_zombie_is_silent_end_not_running` (state `Z` → subject gone),
  `test_c2_pid_reuse_is_silent_end_not_running` and the new
  `test_c1_pid_line_start_token_detects_pid_reuse` (start token mismatch).
  Unreadable: `test_unreadable_evidence_is_unknown_exit_two`,
  `test_unreadable_legacy_claim_is_unknown_exit_two_naming_the_pointer`,
  `test_unreadable_versioned_record_is_unknown_exit_two_naming_the_pointer`.
- Misjudgment counts: `completed`-as-silent-end 0 and `running`-as-silent-end 0 by
  construction of the reverse legs above; the live counterpart rows are in SC-008.
- Pointer: `notes/red-first-evidence.md` T021/T024/T027/T028/T033 entries.

## SC-002 — every dispatched attempt has one closed value + evidence pointers; missing value/evidence fails the guard

- Command: as SC-001 with `-k "unrecorded or unbacked or out_of_set or two_runs"` → `5 passed in 6.29s` (rc 0).
- Guard goes non-zero: `test_c3_missing_end_state_is_settlement_unrecorded` (7-column row
  without `end_state`/`evidence` → `settlement-unrecorded`, engine rc 1);
  `test_c3_completed_without_resolvable_evidence_is_settlement_unbacked` (rc 1);
  the out-of-set leg (`test_engine_carries_no_prebuilt_version_rejection` asserts the
  ordinary `settlement-out-of-set` predicate, rc 1).
- Zero evidence-less rows pass: every finding carries an `evidence` list with `start`
  plus terminal/lack/claim/unreadable kinds (`test_settlement_engine.py` schema legs);
  the C1 real-roots run (S-3, 114 attempts) reports `violations=0` with each row's
  evidence pointers.
- Smoke (final-path requirement, GATE-4 fields): recorded in
  `test-evidence/verification-input.md` — `smoke_command=`, `smoke_exit_code=0`,
  `smoke_evidence_path=` pointing at the S-1/SC-002 readings.
- Pointer: `notes/quickstart-run.md` S-3; `notes/red-first-evidence.md` T009/T018/T028.

## SC-003 — watcher token / exit-code / sentinel sets equal the `fbab7a45c` baseline

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_preservation.py -q`
- Output: `6 passed in 23.27s` (rc 0) — the three sets are extracted with the same
  extractor and compared member-for-member; `--self-test` 39/0; the sha256 of the live
  watcher equals the baseline copy
  (`955ddf7820a80cb3afad5af25877f2f8d7093e4fb08c46ec59dfe948ec3f2479`, S-6).
- Extractor inputs are exactly `skills/external/sdd-loop-driver/scripts/watch-target.sh`
  and its `--help` / `--self-test` output (baseline copies under `test-evidence/`).
- Pointer: `test_settlement_preservation.py`; `notes/red-first-evidence.md` T023.

## SC-004 — reaction drill: explicit uplink for 100% of silent-end/unknown fixtures; zero auto-kill / stale-consume

- Record: `test-evidence/reaction-drill.md` — two-attempt scenario (old attempt
  `silent-end`, retry under a new label `completed`): uplink entries exist for both
  labels (values + evidence item counts 3 / 4); retry label differs; old-evidence hashes
  equal before/after; engine-created attempts 0; non-zero `os.kill` signals 0; stale
  return hash unchanged → consumption count 0.
- Machine twin: `test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value` (the old
  attempt keeps `claim: None` when a stale return appears) and the S-1 quickstart
  reading (a real SIGKILL attempt is reported, never dropped).
- Pointer: `test-evidence/reaction-drill.md`; `notes/red-first-evidence.md` T021.

## SC-005 — every background-settable carrier has a deterministic settlement test and a mapping; uncovered = 0

- Coverage matrix (C1…C6 with deterministic + reverse legs) in
  `notes/red-first-evidence.md` T027; uncovered carriers **0**. C4's foreground-terminal
  branch and C5's virtual exclusion are asserted by
  `test_c4_run_agent_native_settlement_obligations` /
  `test_c5_virtual_exclusion_is_written_in_three_execution_modes`.
- Scope guard: `tests/contract/test_settlement_scope.py` → 10 passed (part of the
  six-module 100-passed battery, S-7): the carrier inventory is closed C1…C6 and every
  C-ID is referenced by at least one settlement test.
- Pointer: T027 matrix; S-7 battery.

## SC-006 — new records declare `settlement_version`; legacy counted compliant = 0; zero NEW drift; every incompatible change tested

- `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_migration.py -q`
  → `8 passed in 6.30s` (rc 0): versioned claim audited under `settlement_version: 1`;
  legacy claim annotated (`legacy: true`) with derived value and rc 0 — legacy records
  are never counted compliant and never rewritten (tree-hash equality);
  `test_incompatible_change_ledger_is_empty` proves exactly one declared version across
  the framework sources (the ledger is empty, so the migration mapping is vacuous with a
  test); `test_engine_carries_no_prebuilt_version_rejection` proves the single refusal
  remains `unknown`.
- Drift: `sync-mirrors.py --check` rc 0 (six pairs byte-identical; 0 NEW members vs the
  T001 baseline) and `regen-command-copies.py --check` rc 0 — see
  `test-evidence/enforcement-honesty.md` § 1.
- Pointer: `notes/red-first-evidence.md` T028/T029/T031.

## SC-007 — unique entry; no third full-slot; repeat-run difference 0; zero fixed-wait tests

- Unique entry: every test command in this pack, the battery and the red-first ledger
  runs through `scripts/bash/run-tests.sh` (no interpreter-level pytest entry appears).
- Two-slot budget: `test_settlement_preservation.py::test_test_budget_keeps_one_baseline_and_at_most_one_closure_slot`
  passed in the SC-003 run; the implement baseline slot is the single E2 fence row in
  the spine; this package consumed no full-suite slot (all selections targeted).
- Repeat-run difference 0: `test_settlement_engine.py::test_two_runs_are_byte_identical`
  passed (in the SC-002 selection); T008's recorded repeated-run identity
  (`settle_runs_byte_identical=yes`, tree hash equal) stands.
- Fixed-wait tests 0: mechanical scan
  `grep -rn "time.sleep(" tests/contract/test_settlement_*.py tests/fixtures/settlement/builders.py`
  → 2 sites, both the 0.02 s interval inside fact-polling helpers
  (`test_settlement_carriers.py:208` `_poll_until`, `builders.py:250` `_poll`);
  `grep -rnE "\bsleep [0-9]+"` over the same files → none.
- Pointer: this section's commands; preservation/budget test.

## SC-008 — live fixtures never misread as `silent-end`; long silence stays `running`

- Legs (inside the SC-001 selection, all passed): `test_c1_live_stage_is_running_not_silent_end`,
  `test_c2_live_attempt_is_running_not_silent_end`, `test_c2_long_silence_with_a_live_pid_stays_running`,
  `test_c3_live_seat_inside_its_deadline_is_running`, `test_c4_live_native_inside_its_deadline_is_running`
  — five live/half-live carriers, misreport count 0.
- Real-world reading: the S-3 real-roots run settles the live
  `background-silent-failure-implement-p4` attempt `running` (`live-check`) while every
  finished attempt settles from its evidence — live and dead are distinguished on the
  real carrier, not only in fixtures.
- Pointer: `notes/quickstart-run.md` S-3; `notes/red-first-evidence.md` T024.

## SC-009 — confirmation-gate EP-005 fallback: per-file hits ≤ baseline, zero new; the frozen ==27 red reported honestly

- `python3 scripts/python/scan-confirmation-gates.py --root . --json` → `"total": 30`
  (S-6). Baseline before the feature: 31; the frozen `== 27` equality was already red at
  base (EP-005, recorded at `test-evidence/confirmation-total-red-at-base.txt`) and is
  reported as-is — never claimed green.
- Per-file guard: `test_settlement_preservation.py::test_confirmation_gate_scan_adds_no_hits_on_touched_files`
  passed in the SC-003 run (owner page 0 ≤ 1; driver SKILL 1 ≤ 1; all other touched
  files 0 ≤ 0) — zero NEW hits, no exemption set widened.
- Pointer: S-6 reading; preservation test; T036 non-goals audit
  (`test-evidence/non-goals-audit.md`).
