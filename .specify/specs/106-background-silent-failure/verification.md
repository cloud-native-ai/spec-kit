# Verification Log — 106-background-silent-failure

# -- Baseline (recorded once, BEFORE any /speckit.implement work changes the tree) --

baseline_commit=907426e1c
baseline_date=2026-11-26
baseline_branch=106-background-silent-failure

# -- /speckit.implement results --

implementation_date=2026-11-26
post_change_commit=0a01f797a

# -- Smoke test record (exactly one per feature) --

smoke_command=env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/106-background-silent-failure/test-evidence/t033-smoke.txt

# -- SC status rows (derived spec-side from test-evidence/verification-input.md, T035) --

SC-001_status=pass
SC-001_value=dead_fixtures=4 half_dead=3 unreadable=3 misreads=0 selection=16 passed
SC-001_note=final path. Dead/half-dead fixtures settle `silent-end` (pid-gone, zombie, pid-reuse incl. the C1 start-token leg) or `unknown` when unreadable; `completed`/`running` misjudgment count 0. Evidence test-evidence/acceptance-106.md § SC-001, notes/quickstart-run.md § S-1/S-3, notes/red-first-evidence.md T024/T028/T033.

SC-002_status=pass
SC-002_value=unrecorded=exit1 unbacked=exit1 out_of_set=exit1 evidence_less_rows_passing=0 real_roots_violations=0
SC-002_note=final path. Every dispatched attempt carries one closed value plus evidence pointers; a 7-column row missing end_state/evidence is `settlement-unrecorded` (rc 1), a `completed` claim without resolvable evidence is `settlement-unbacked` (rc 1), an out-of-set value hits the ordinary predicate (rc 1); the 114-attempt real-roots run reports violations=0. Evidence test-evidence/acceptance-106.md § SC-002, notes/quickstart-run.md § S-3.

SC-003_status=pass
SC-003_value=test_settlement_preservation.py=6 passed watcher_sha_match=yes self_test=39/0
SC-003_note=supporting path (measured baseline). The same extractor yields verdict-token / exit-code / sentinel-literal sets member-for-member equal to fbab7a45c; watcher sha256 955ddf78… equals the baseline copy; --self-test 39 passed / 0 failed. Evidence test-evidence/acceptance-106.md § SC-003, notes/quickstart-run.md § S-6.

SC-004_status=pass
SC-004_value=uplink_entries=2 retry_new_label=yes old_hashes_equal=yes auto_kill=0 stale_consume=0
SC-004_note=final path. Reaction drill: every silent-end/unknown fixture produces an explicit uplink; retry uses a new label with old evidence kept; non-zero kills 0; stale-return consumption 0. Machine twin `test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value` plus the real SIGKILL S-1 reading. Evidence test-evidence/reaction-drill.md, test-evidence/acceptance-106.md § SC-004, notes/quickstart-run.md § S-1.

SC-005_status=pass
SC-005_value=carriers=C1..C6_uncovered=0 matrix_rows=6 scope_guard=10 passed
SC-005_note=supporting path (measured baseline). Every background-settable carrier has a deterministic settlement test and a reverse fixture; C4's foreground-terminal branch and C5's virtual exclusion are asserted; the scope guard keeps the inventory closed. Evidence notes/red-first-evidence.md T027, test-evidence/acceptance-106.md § SC-005.

SC-006_status=pass
SC-006_value=test_settlement_migration.py=8 passed declared_versions={1} legacy_compliant_rows=0 new_drift_members=0 regen_copies=rc0
SC-006_note=supporting path (measured baseline). Versioned claims declare settlement_version 1; legacy records are annotated, never counted compliant, never rewritten; the incompatible-change ledger is empty with a test; mirrors and command copies show zero NEW drift on the touched faces. Evidence test-evidence/enforcement-honesty.md § 1, test-evidence/acceptance-106.md § SC-006.

SC-007_status=pass
SC-007_value=unique_entry=run-tests.sh third_full_slot=no repeat_run_diff=0 fixed_wait_tests=0
SC-007_note=supporting path (measured baseline). All new tests run through scripts/bash/run-tests.sh; no third full-suite slot consumed (targeted selections only); `test_two_runs_are_byte_identical` green; the only time.sleep sites are 0.02 s intervals inside fact-polling helpers. Evidence test-evidence/acceptance-106.md § SC-007, test-evidence/t033-smoke.txt.

SC-008_status=pass
SC-008_value=live_legs=5 live_misreads=0 real_live_attempt=running(live-check)
SC-008_note=supporting path (measured baseline). Live fixtures on all background-settable carriers stay `running`, never `silent-end`; the real-roots run settles the live implement-p4 attempt `running` by a settlement-time live check. Evidence test-evidence/acceptance-106.md § SC-008, notes/quickstart-run.md § S-3.

SC-009_status=pass
SC-009_value=scan_total=30(base 31) frozen_27_red_at_base=yes touched_file_new_hits=0
SC-009_note=supporting path (measured baseline, EP-005 fallback). Touched files carry zero NEW blocking hits (owner 0 ≤ 1, driver SKILL 1 ≤ 1, all others 0 ≤ 0); the frozen ==27 equality was already red at base and is reported as-is, never claimed green. Evidence test-evidence/non-goals-audit.md, test-evidence/acceptance-106.md § SC-009, test-evidence/confirmation-total-red-at-base.txt.

# -- Runtime-stack joint acceptance (requirements.md § Runtime Stack & Dependency Ownership, duty ③) --

RS-001_joint_acceptance=pass — watcher --self-test 39 passed / 0 failed; verdict-token / exit-code / sentinel-literal sets member-for-member equal to fbab7a45c; settlement consumes watcher verdicts with zero semantic change (tests/contract/test_settlement_preservation.py 6 passed; test_settlement_engine.py C1 mapping legs)
RS-002_joint_acceptance=pass — legacy .status line format unchanged and read back by the same parsers; SIGKILL fixture settles silent-end from the additive .attempt record (test_c2_sigkill_silent_death_settles_silent_end); .attempt start record present on every dispatch.sh launch
RS-003_joint_acceptance=pass — every attempt carries one closed settlement value plus evidence pointers; missing-evidence rows exit 1 (settlement-unrecorded / settlement-unbacked); legacy rows annotated, never counted compliant (test_settlement_engine.py / test_settlement_carriers.py / test_settlement_migration.py green)
RS-004_joint_acceptance=pass — every new test runs through scripts/bash/run-tests.sh; two-slot budget unchanged (no third full slot); repeat-run settlement diff 0 (test_two_runs_are_byte_identical; SC-007 readings)

deferred_tasks=
