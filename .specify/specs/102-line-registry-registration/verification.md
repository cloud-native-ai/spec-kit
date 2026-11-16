# Verification Log — 102-line-registry-registration

<!--
  Schema owner: shared/workflow/acceptance-hardening.md — § Verification Vocabulary and
  § Closure Verdict. The key=value block below is the record; any table is a view of it.
  Written by implement package 6/6 (T051–T057), 2026-11-16. This file records readings; it
  does not by itself flip the feature status (the Pre-Status-Flip Gate does that).
-->

# -- Baseline (recorded once, before implement work changed the tree) --

baseline_commit=cdc79cdb52c892e8ed43145860cea2cd6ffdbfdf
baseline_date=2026-11-16
baseline_branch=102-line-registry-registration
baseline_failed_ids=241
baseline_passed=8922
baseline_skipped=6
baseline_runner=full-suite rc=1 duration=319.51s
baseline_failed_ids_source=.specify/specs/102-line-registry-registration/baseline-failed.txt

# -- /speckit.implement results --

implementation_date=2026-11-16
post_change_commit=a026be9ff (package 6/6 entry base; the T057 commit carries this record)
post_change_targeted_passed=153
post_change_targeted_failed=0
post_change_new_failure_names=0

# -- Smoke test record (exactly one per feature) --

smoke_command=bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py tests/contract/test_line_registration_scan.py tests/contract/test_line_registration_wiring.py tests/integration/test_line_run_behavior.py tests/integration/test_line_registration_scan_live.py tests/contract/test_status_digest.py tests/contract/test_status_digest_roles.py tests/unit/test_status_digest_unit.py -q --names-out .specify/specs/102-line-registry-registration/final-failed.txt
smoke_exit_code=0
smoke_evidence_path=.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt

# -- Success Criteria evaluation --
# status ∈ pass | fail | partial | blocked | deferred | unknown

SC-001_status=pass
SC-001_value=run-time digest lists the line state=active rc=0; close leaves state=closed reason completed and failed; SIGKILL rc=137 leaves state=active and visible; an unwrapped command reads nothing-running rc=3
SC-001_note=Readings from digest stdout, registry entry JSON and wrapper exit codes only: `test-evidence/us1-sc-001.txt`; behaviour node `test_digest_lists_the_line_while_running_and_renders_nothing_running_after` green in the smoke.

SC-002_status=pass
SC-002_value=fixture with a marker exits 1 naming the path and the same file through the wrapper exits 0; live roots read 159 files, violations 0, owner-skipped 1; injected live-root script exits 1; removing a COMPLIANT_INVOCATIONS member flips a single-member fixture 0→1; disabling self-declaration flips 1→0; a missing root exits 2
SC-002_note=`test-evidence/us2-scanner-green.txt` (17 passed), `test-evidence/us2-teeth.txt` (injections with sha256 restores), live reading `test-evidence/line-registration-scan-live.txt`, quickstart S-4/S-5 in `notes/quickstart-run.md`.

SC-003_status=pass
SC-003_value=success and failure entries carry line_id, state and reason completed/failed; wrapper references journal-utils.py 0 times; only engine actions register and deregister are invoked; 0 new journal files
SC-003_note=`test-evidence/us1-sc-003.txt`; contract node `test_c19_the_wrapper_never_reaches_for_the_journal_writer` green in the smoke.

SC-004_status=pass
SC-004_value=help/version rc=0 with zero registry writes; undeclared option rc=2 and the command never runs; registration refused rc=6 and not executed; no git toplevel rc=4 and not executed; child status 7 propagated; double failure rc=5 with stderr naming engine exit 6; close failure over child 0 rc=6; SIGKILL rc=137 and entry active
SC-004_note=`test-evidence/us1-sc-004.txt`; exit matrix asserted by the contract and behaviour nodes in the smoke.

SC-005_status=pass
SC-005_value=owner section, status Single source sentence, template pointer bullet, live bullet and run-team §5/§6/§7 all present by path; five removal injections each turn the guard red then restore byte-identically (sha256 equal); wiring suite 15 passed
SC-005_note=`test-evidence/us4-wiring-green.txt` and `test-evidence/us4-injections-full.txt`; locators in `test-evidence/sc008-recitation-2026-11-16.txt` § 1.

SC-006_status=pass
SC-006_value=sync-mirrors rc=2 with the baseline only (5 DIFF + 2 ORPHAN) and all four touched pairs ok; regen-command-copies rc=0; flow-class check 91 units 0 findings rc=0; doc-consistency-check not-evaluated for the distribution lane (not a parity checker)
SC-006_note=`test-evidence/polish-distribution.txt`; the not-evaluated reason is recorded there verbatim and not counted as a pass.

SC-007_status=pass
SC-007_value=103 existing digest tests passed rc=0 with an empty failed-name list; status-digest.py has zero diff since the approved baseline; the smoke adds the same 103 nodes to a 153-passed run
SC-007_note=`test-evidence/polish-digest-regression.txt` and `test-evidence/polish-targeted-suite.txt`; digest action set, exit codes and nothing-running rendering untouched.

SC-008_status=pass
SC-008_value=five surfaces resolve by path; a fresh-context reader who took no part in the feature answered both questions correctly (unregistered means invisible because the registry is the sole source and the probe is PID-bounded; the operator wraps the command with line-run.sh)
SC-008_note=`test-evidence/sc008-recitation-2026-11-16.txt` carries the reader's two sentences and the path locators.

SC-009_status=partial
SC-009_value=changeset 92 paths, 90 after subtracting the two pre-existing untracked scripts, 86 mapped to the 24 declared paths, 4 outside them (all from ratified D-102-01), 0 unexplained; the two pre-existing scripts stay untracked; no push
SC-009_note=`test-evidence/polish-scope.txt`: the subset claim is literally false for four paths even though every one of them is attributable to the user-ratified budget change D-102-01.
SC-009_blocked_at=2026-11-16 D-102-01 (U5 stall decision, status decided-ratified in .specify/register.md)
SC-009_reduced_measurement=path-by-path attribution of the full changeset (diff plus untracked) against the 24 declared delivery paths, with the two pre-existing untracked scripts subtracted, plus git status and git log checks for untracked state and absence of push
SC-009_reduced_measurement_run=yes
SC-009_why_reduced_insufficient=attribution explains each outside path but does not make the containment claim true: four files are outside the declared surface, so the criterion cannot be recorded as a pass on its written terms
SC-009_unblock=a user waiver naming SC-009 for D-102-01, or a plan and feature-ref amendment adding generate-instructions.sh and its two superagent guard tests to the declared delivery surface, then a re-run of the scope audit

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-006_joint_acceptance=pass

# -- Deferred tasks --

deferred_tasks=
deferred_reason_summary=

# -- Free-form notes --

notes=T051 zero-machinery audit is test-evidence/polish-zero-machinery.txt; T054 closing gates are test-evidence/polish-gates.txt; the closure verdict for this record is run by the Pre-Status-Flip Gate and its reading is stored beside the gates.
