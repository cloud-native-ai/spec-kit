# Verification Log — 086-efficient-test-execution

evidence-path note: historical spelling, owner = efficiency-model.md

baseline_commit=018b0455
baseline_date=2026-11-06
baseline_branch=086-efficient-test-execution
implementation_date=2026-11-06
post_change_commit=93e61050
flow_class=execution

# -- Full-run slots (owner of the two-slot model: skills/external/sdd-loop-driver/references/efficiency-model.md; this file records only what this feature spent) --

slot-1-baseline=test-evidence/baseline.txt — T050, serial, 19 failed / 7475 passed / 7 skipped in 687.41s, taken before any source edit
slot-2-closure=test-evidence/closure-diff.txt — T047, default-parallel, 19 failed / 7535 passed / 7 skipped in 284.12s + serial exception pass 1 passed / 7561 deselected in 35.22s, exit 1
slot-2-in-slot-rerun-attempt=test-evidence/closure-diff.txt — the contaminated first attempt (21 failed / 7533 passed / 271.72s), trigger = this package's own sandbox git worktree inside the repo root, disproved by tests/contract/test_isomorphism_map.py 27 passed after removal

# -- Smoke test record (exactly one per feature) --

smoke_command=env -u PYTHONPATH SPECKIT_PYTHON=.venv/bin/python bash scripts/bash/run-tests.sh tests/contract/test_run_tests_runner_contract.py tests/contract/test_test_execution_efficiency.py tests/unit/test_audit_test_budget.py -q
smoke_exit_code=0
smoke_evidence_path=.specify/specs/086-efficient-test-execution/test-evidence/smoke-086.txt

# -- Joint acceptance (one row per `in-scope` runtime-stack row) --

RS-003_joint_acceptance=pass
RS-004_joint_acceptance=pass

# -- Per-SC status rows --

SC-001_status=pass
SC-001_value=the default-parallel and serial failure-name sets have an empty symmetric difference on the same tree, same selection, same --names-out convention, and the parallel wall clock is inside the 40% ceiling — both limbs measured on the two slot runs: baseline 19 names (test-evidence/baseline-failed.txt), closure 19 names (test-evidence/final-failed.txt), comm -13 empty (added 0) and comm -23 empty (dropped 0); closure parallel pass 284.12s against the ceiling 1031.48s x 40% = 412.59s, i.e. 69% of it
SC-001_note=evidence test-evidence/closure-diff.txt; the 0.41x ratio against the T050 serial slot (687.41s) is recorded there as a like-for-like observation only, NOT as SC-001's formula — SC-001's 40% is judged against the 412.59s pre-pull ceiling, as requirements.md SC-001 Source states. The 60-test passed-count difference between the slots (7475 vs 7535) is a collection-scope difference between the two paths, not a membership change; the empty name diff is the criterion. Carrier tests/contract/test_test_execution_efficiency.py + test_run_tests_runner_contract.py green in the smoke run (84 passed)
SC-002_status=pass
SC-002_value=the shipped constitution template and the live constitution each carry the principle entry, and the shipped instructions template and the live instructions each carry its ambient section, all four present and none missing: template constitution-template.md `### XIX. Efficient Test Execution (Concurrent by Default)` (1 hit), live .specify/memory/constitution.md `### XX. Efficient Test Execution (Concurrent by Default)` (1 hit), template instructions-template.md `## Test Execution Efficiency (测试执行效率)` (1 hit) at line 124, live .specify/instructions.md the same heading (1 hit); every one of the four is summary + pointer shape toward shared/guidelines/test-execution-efficiency.md, and the live constitution records the amendment at `**Version**: 1.17.0 | **Last Amended**: 2026-11-06`
SC-002_note=evidence test-evidence/mirror-parity.txt (both --check outputs, six pairs ok, and the six surface diff/byte readings) and test-evidence/no-new-machinery.txt; owner guideline is a single file with both carriers byte-identical (shared/guidelines/test-execution-efficiency.md and .specify/shared/guidelines/test-execution-efficiency.md, 17,055 B each); carrier tests/contract/test_test_execution_efficiency.py asserts all six surfaces in one guard and is green in the smoke run
SC-003_status=pass
SC-003_value=a project initialised from this checkout's CLI receives the principle, the owner-guideline pointer and the owner-guideline file name, so a downstream reader needs no access to this repository: `specify init ds086 --ai claude --no-git --script sh --ignore-agent-tools` exits 0, and the shipped templates the generated tree carries answer all three greps — principle title at constitution-template.md line 326, section at instructions-template.md line 124, `shared/guidelines/test-execution-efficiency.md` 1 hit in each, `test-execution-efficiency.md` 1 hit in each; the generated tree's instructions template is byte-identical to this repo's
SC-003_note=evidence test-evidence/downstream-init.txt, run under /Users/liuqiming.lqm/tmp/spec-kit/086/downstream-086/ outside the repo root. Disclosed in that file: the reading is taken on the shipped templates the initialised project carries, not on a rendered .specify/memory/constitution.md — at init time that file is the product's two-line placeholder and .specify/instructions.md does not exist yet, so a grep there would have measured the initialisation order rather than this feature's delivery. The principle block's own wording states that it binds any project that builds a test framework or test cases, which is SC-003's reader-independence limb
SC-004_status=pass
SC-004_value=the three escape hatches each complete a full run with a valid failure-name list, and the path actually taken is decidable from the command and the stderr header: explicit switch gives `mode=serial reason=explicit` with an inner `-m pytest -n0` header; the missing engine gives `mode=serial reason=no-xdist detail=pytest-xdist-not-importable-by-<interpreter>`; the nested call gives `mode=serial reason=nested detail=PYTEST_XDIST_WORKER=gw3` with an inner `-n0` command line, i.e. no second worker pool derived. All three arms over the probe fixture: exit 1, exactly one failure name, passes=1, and the three name lists identical; all three additionally complete a 32-test green suite at exit 0 with a 0-entry name list
SC-004_note=evidence test-evidence/escape-hatch.txt; the no-engine arm uses the three-part shim the contract case itself builds (shadowing xdist.py + relocated xdist_dist package + synthetic pytest_xdist dist-info), and the probe was re-checked to fail before the run so the premise is measured, not assumed; two earlier two-part shims are recorded as discarded because they produced a broken environment (exit 3, plugin load abort) rather than an absent engine. Code green points belong to C-004/C-005/C-006 carriers in tests/contract/test_run_tests_runner_contract.py
SC-005_status=pass
SC-005_value=an explicitly parallel full run is classified as a full run, neither dropped nor downgraded to a targeted run, and pre-existing records parse unchanged — both limbs green: 10 parallel switch shapes (-n 8, -n auto --dist load, -n4, -n=4, --numprocesses 4, --numprocesses=auto, --dist loadfile, --dist=loadfile, --maxprocesses=8, and the shape the runner itself emits) each classify as a full run with an empty positional list, the same parallel command logged but absent from the ledger is still reported unaccounted rather than reclassified, an accounted parallel row audits to exit 0 with no unaccounted, and all seven pre-existing row shapes replay to their exact pre-upgrade verdicts including the two that must stay non-runs
SC-005_note=evidence test-evidence/budget-ledger.txt and test-evidence/ledger-parallel-flags.txt (the M-8/M-9 doctored-copy readings); the two-part assertion (verdict AND empty positionals) is what keeps the reading honest, since a parser stripping only the separated form still returns full-run; the attached-form token set is pinned separately and is the M-9 surface. tests/unit/test_audit_test_budget.py 32 passed, of which 6 are the limb cases
SC-006_status=pass
SC-006_value=the successor's closure full run has an empty failure-name difference against the same-convention serial baseline, and both sides of the difference are recorded: baseline 19 names, closure 19 names, `comm -13` (appeared) empty and `comm -23` (disappeared) empty, both pasted in the evidence file rather than asserted in prose
SC-006_note=evidence test-evidence/closure-diff.txt § the two comm readings; final-failed.txt holds exactly 19 names (wc -l) and baseline-failed.txt holds 19; the two runs share the runner, the selection (whole suite, no tests/ narrowing), the --names-out convention and the cleared-PYTHONPATH environment, which is what makes the difference meaningful
SC-007_status=pass
SC-007_value=085's temporary Goal/Team, stage agents, concurrency, worktree isolation, integration queue and checkpoint mechanisms are all preserved, and 085's contract and integration tests show zero new failure names: the five 085 preservation files re-run to 20 passed in 6.22s with a 0-entry failure-name list (exit 0), and the only 085 path that moved anywhere on this branch is verification.md with six added lines, every one matching the SC-010 carve-out prefix, while git status over the 085 spec, .specify/goal and .specify/teams is empty
SC-007_note=evidence test-evidence/preservation-085.txt (§ 1/§ 2 both GATE-5 halves, § 3 the untracked check, § 8 the five-file re-run); the 20-passed run is a targeted five-file selection, not a full-suite run, so it consumes no slot. Carrier tests/contract/test_temp_goal_contract.py and the four sibling files are themselves the 085 contracts, unchanged
SC-008_status=pass
SC-008_value=this feature's own run left complete dogfood evidence: a spec-local temporary Goal and Team exist and bind, 11 stage checkpoints exist on disk (01-requirements through 11-implement-wave4), each stage records a carrier identity, agent_concurrency_requested, agent_concurrency_effective with a named reason whenever it is lower, and its checkpoint path, and actual concurrency taken from dispatch records reaches a maximum above one
SC-008_note=evidence test-evidence/dogfood-record.md; the concurrency figures are read from dispatch records, not from the declared 24 — requested 24, team effective 18 (verifier reserve), per-stage effective with its reason, and actual_concurrency_max = 3 measured in implement wave 2 (three packages in flight). Carriers C-048/C-049/C-050/C-051 green points recorded in test-evidence/preservation-085.txt § 5/§ 6/§ 7
SC-009_status=pass
SC-009_value=the runner's two carriers are byte-identical and both mirror checks pass, with the count and budget guards that the new principle forces green in the same change: `sync-mirrors.py --check` exits 0 with six pairs ok, `regen-command-copies.py --check` exits 0, `diff -q scripts/bash/run-tests.sh .specify/scripts/bash/run-tests.sh` is silent at 17,463 B on both sides, the live constitution carries 20 principles against the template's 19 and the live instructions 34 sections against the template's 33, and the live instructions file measures 34,685 B inside the 34,816 B budget with 131 B of headroom
SC-009_note=evidence test-evidence/mirror-parity.txt; the six surface pairs (owner guideline, constitution template, live constitution, instructions template, live instructions, generator skill) are each diff-silent; the counts are the pins updated by T028 in tests/contract/test_constitution_double_landing.py (TEMPLATE_COUNT 19, LIVE_COUNT 20, COMMAND_COUNT 12) and test_fast_fail_discipline.py (LIVE_EXPECTED 34, version 1.17.0), both green
SC-010_status=pass
SC-010_value=the CLI package's runtime dependency set has an empty difference against the pre-change state, and the new dependency sits only on the development side: the runtime set reads identically at HEAD and at the merge base 24cb4edc as ['httpx[socks]', 'platformdirs', 'readchar', 'rich', "truststore>=0.10.4; python_version >= '3.10'", 'typer'], and pytest-xdist appears only inside the new [project.optional-dependencies] dev block
SC-010_note=evidence test-evidence/no-new-machinery.txt check 3; disclosed there that the task's own `python3 -c "import tomllib..."` cannot run on this host (python3 is 3.9.6) so the reading was taken with /opt/homebrew/bin/python3 (3.14.6) and cross-checked against the merge-base pyproject.toml, both giving the same list; the pyproject diff touches only the dev extra block and one markers entry, so no runtime dependency could have moved
SC-011_status=pass
SC-011_value=after a complete default-parallel run the working tree carries no new pollution beyond what was already dirty before it: the before/after `git status --porcelain --untracked-files=all` snapshots that bracket the closure run differ by exactly one appeared line, and that line is the run's own tracked --names-out target (final-failed.txt) changing from clean to modified — not foreign content; the only other entry, the pre-existing `.specify/memory/trigger/index.json` modification, is present on both sides, and `comm -23` is empty, so nothing was deleted or cleansed either
SC-011_note=evidence test-evidence/worktree-clean.txt; `git worktree list` showed exactly two entries (no sandbox worktree) during the bracket and `sync-mirrors.py --check` exits 0 afterwards; the snapshot was taken before the evidence file itself was written, which is stated in that file so the reading is not self-referential
SC-012_status=pass
SC-012_value=085 SC-010's acceptance status was updated from evidence, not from the fact that this feature ran: 085 verification.md now carries SC-010_status=pass because the full chain exists — all eight stages (requirements → review) with a record and a checkpoint each (01-requirements..13-review), requested 24 / team effective 18 with per-stage reasons, actual concurrency max 3 from dispatch records, 8 child lines merged through the integration queue, the carrier downgrade recorded as an observation, and the review stage passing with ARC `agree`
SC-012_note=the cited 085 line is `.specify/specs/085-sdd-temporary-goal-team/verification.md` SC-010_status=pass, written under the T041 carve-out (FR-027, authorized by FR-030, contract C-041); the earlier partial state named the missing review record, and the flip happened only after `review.md`, `code-review.md` and `checkpoints/13-review.md` existed. The M-18 leg in test-evidence/parallel-safety-attribution.md shows the evidence-chain check goes red exactly when `pass` is claimed with only requirements/clarify/plan checkpoints on record, so the pass is not a default

# -- Deferred tasks --

deferred_tasks=

# -- Closure verdict (source: closure-acceptance-check.py, copied verbatim, never recounted) --

final_path_source=.specify/specs/086-efficient-test-execution/test-evidence/completion-gate.txt
final_path_pass=8
final_path_blocked=0
final_path_deferred=0
final_path_partial=0
final_path_fail=0
final_path_unknown=0
final_path_total=8

# -- Closure verdict, verbatim payload --

closure_checker_command=python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/086-efficient-test-execution --repo . --feature-detail .specify/memory/features/086.md --feature-registry .specify/memory/features.md --json
closure_checker_verdict=accept
closure_checker_exit_code=0
closure_checker_reasons=
closure_checker_completion_conditions=every_final_path_pass=true, no_open_rows=true, smoke_record_pass=true, status_row_per_criterion=true
closure_checker_tasks=closed=56, deferred=0, in_progress=0, open=0
closure_checker_waived=
closure_checker_note=the payload is pasted in full in test-evidence/completion-gate.txt § GATE-8; the counts above are copied from it, not recounted. Note the interaction with 085: its SC-010 stays partial, and the checker accepts this feature anyway because an `inherited` row is judged by whether its carrier RESOLVES (here `gate:GATE-086` in tasks.md), not by whether the dependency has already flipped that row to pass. That row-legality path was confirmed non-vacuous in passing: blanking the carrier, or aiming it at `gate:GATE-999`, each immediately yields `inherited-blocker-undisposed: 085:SC-010_status`. No waiver was used at any point.
