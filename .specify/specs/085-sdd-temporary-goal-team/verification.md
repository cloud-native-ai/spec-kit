# Verification Log — 085-sdd-temporary-goal-team

evidence-path note: historical spelling, owner = efficiency-model.md

# -- Baseline (recorded once, BEFORE implementation changes the tree) --

baseline_commit=aafbf5a8352fa58daf5c09e5560d2ea36e1be99e
baseline_date=2026-11-06
baseline_branch=085-sdd-temporary-goal-team
baseline_full_suite=7347 tests collected
baseline_failure_source=.specify/specs/085-sdd-temporary-goal-team/test-evidence/full-suite-pre-review-failed.txt (pre-existing G-9 gate-baseline red disclosed)

# -- Implementation results --

implementation_date=2026-11-06
post_change_commit=2cb68c44
post_change_smoke=43 passed (see smoke record)
post_change_targeted_suites=scope/temp-goal/temp-team/child-line/checkpoint/wp-gate tests all green

# -- Smoke test record (exactly one per feature) --

smoke_command=python3 -m pytest -q tests/unit/test_goal_scope_engine.py tests/contract/test_scope_resolution.py tests/contract/test_temp_goal_contract.py tests/contract/test_temp_team_schema.py tests/contract/test_line_registry_child_lines.py tests/contract/test_checkpoint_protocol.py tests/unit/test_wp_gate_085.py tests/integration/test_temp_team_worktree_queue.py tests/integration/test_checkpoint_rollback.py
smoke_exit_code=0
smoke_evidence_path=.specify/specs/085-sdd-temporary-goal-team/test-evidence/smoke.txt

# -- Success criteria --

SC-001_status=pass
SC-001_value=7 contract + 8 unit scope cases
SC-001_note=global/spec/auto, ambiguity, wrong scope, writes reject auto, legacy global unchanged; test_scope_resolution.py + test_goal_scope_engine.py.

SC-002_status=pass
SC-002_value=6 contract checks
SC-002_note=temporary goal lives under the spec, not the global archive; criteria do not copy SC rows; engine validates it; spec list sees it, global list does not.

SC-003_status=pass
SC-003_value=7 contract checks
SC-003_note=team scope/spec_dir/goal_slug/lifecycle/stage_seats/isolation/concurrency fields present; all 8 stage keys; every seat resolves to a member.

SC-004_status=pass
SC-004_value=requested 24 / effective 18; 2 child lines active concurrently
SC-004_note=team config records requested/effective/verifier-reserve; checkpoint 03 records implement effective 18; test_temp_team_worktree_queue.py proves two child lines active concurrently under the agent cap.

SC-005_status=pass
SC-005_value=2 child worktrees, 2 merged entries, 0 lost changes, fsck clean
SC-005_note=test_temp_team_worktree_queue.py creates two child lines, real worktrees, distinct commits, deterministic integration order, merged results, removed worktrees, no push.

SC-006_status=pass
SC-006_value=4 checkpoint files + rollback drill
SC-006_note=checkpoints 01/02/03/04 carry the four parts; test_checkpoint_protocol.py pins the four parts, one-change cap and rollback triggers; test_checkpoint_rollback.py restores team bytes and records rollback=yes.

SC-007_status=pass
SC-007_value=0 generic executor references; 19 rendered agents at maxTurns 500
SC-007_note=generic sdd-executor removed from sources/mirrors/renders/manifest; all retained definitions and rendered copies are 500; test_unified_turn_budget-level scans and agent contract tests pass.

SC-008_status=pass
SC-008_value=global goal/team bytes identical before/after a spec-scope write
SC-008_note=test_scope_resolution.py::test_spec_write_leaves_global_stores_byte_identical.

SC-009_status=pass
SC-009_value=25 failures in the final run; 1 was the 085-introduced criterion-subject false positive (fixed); the remaining 24 reproduce at baseline aafbf5a8 or are in the 083 baseline
SC-009_note=Final full suite (excluding the Docker/Hugo test): 7356 passed / 25 failed / 1 skipped. The criterion-subject failure was fixed after that run. Eight representative remaining failures (acceptance-premises pin, execution-config, goal-migration historical directive, two lifecycle identity, summary writeset, user-facing comprehension, loop-state) reproduce on a detached worktree at aafbf5a8; the 083 baseline carries 24 failures. Targeted 070/064 suites pass (1048 cases).

SC-010_status=pass
SC-010_value=live full 8-stage SDD run via the 085 temporary Goal/Team: requirements..review each with a record and a checkpoint (01-requirements..13-review), 8 child lines in real worktrees merged through the integration queue, actual concurrency max 3, review `Ready for Review` with code blocking 0
SC-010_note=Feature 086's own unattended run used the spec-local temporary Goal and Team: every stage wave carries a dispatch record and a checkpoint (01-requirements..13-review), agent_concurrency_requested 24 / team effective 18 (verifier-reserve) with a per-stage effective and its named reason, actual concurrency from dispatch records max 3 (implement wave 2), worktree isolation and the integration queue exercised by 8 child lines, and the review stage completed with four passing segments and ARC `agree` (`.specify/specs/086-efficient-test-execution/review.md`). The carrier downgrade (host-native agent identities for 085's stage-agent types) is recorded as an observation, not a failure (contract C-051).
SC-010_blocked_at=
SC-010_reduced_measurement=live two-child worktree/queue run + run report + checkpoints 04/05 + 43-test smoke
SC-010_reduced_measurement_run=yes
SC-010_why_reduced_insufficient=The bounded dogfood proves concurrency, worktree isolation, integration and checkpoint discipline, not the LLM stage chain's end-to-end behavior.
SC-010_unblock=Run one small feature through the driver with the temporary team and record the stage agents' run report/checkpoints.

# -- Deferred tasks --

deferred_tasks=

# -- Joint acceptance (in-scope runtime rows) --

RS-003_joint_acceptance=pass
RS-003_joint_acceptance_note=child lines + integration queue test (test_temp_team_worktree_queue.py) passes; two child worktrees merged in declared order with fsck clean.
RS-004_joint_acceptance=pass
RS-004_joint_acceptance_note=agent cleanup + render manifest + 500 budget checks pass; no generic executor remains.
