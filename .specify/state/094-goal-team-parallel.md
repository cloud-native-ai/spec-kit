# Line State — 094-goal-team-parallel

<!-- loop-state:begin -->
spine_state: running
run_id: r20261109T064500Z-092a
slice: 094
stage: implement
stage_started_at: 1794220564
stage_deadline_epoch: 1794231364
stage_base_commit: e8d716e3
attempt: 0
retry_limit: 3
last_verdict: "Implement stage CLOSED — closure-acceptance on the MAIN tree = verdict ACCEPT, final_path 8/8 pass, reason none (SC-001 moved to supporting per R2; SC-003 migration applied with 16 receipts + 16 archived definitions per R1; SC-002 pin, SC-010 disposal, two one-line repairs). Requirements 0/0; tasks 85 rows 0 err/1 disclosed warn, all sigils ticked by the integration sweep; mirrors byte-identical. Residuals: 128 pre-existing reds unchanged (outside the causal surface); trigger/index.json host mutation left uncommitted; the one-level 088 team.md outside the probe glob needs a future ruling."
driver_contract: |
  HR1 — U4 pass => dispatch the next stage/package in the same turn; never ask "continue".
  HR2 — completion is judged by an independent verifier, never by the executor's own claim.
  HR3 — retry limit 3 / stage deadline 180 min => stop the line, write the spine, surface four elements.
  HR4 — write this spine BEFORE U2, at U3 termination, after U4, at U5; reentry reads only this.
  HR5 — the driver stays alive until U6 or an explicit U5 stop; no detached waiting.
  HR6 — the loader is the driver; native subagents only, never qodercli locally.
  HR10 — target governance (constitution + instructions) is read and obeyed before any write.
  HR11 — runtime directories live only under .specify/ (.tmp/sdd-loop/, state/).
  HR14 — every checkpoint carries the rule-first direction audit (T0/T1/T2).
next_action: "dispatch the review stage (4 segments: process / artifacts / implementation / code + ARC) on the closure-accepted tree; then the line close-out (registry status transition + merge/push history)"

direction_contract: |
  goal_verbatim: "需要将085扩展到 /speckit.feedback 这类命令, 临时goal和临时team不仅仅是作用于SDD流程,也作用于speckit*命令, 在这点上需要将临时goal和临时team的归档目录挪到原本的.specify/goal和.specify/teams中,而不是.specify/specs/091-auto-git-closeout/goal和.specify/specs/091-auto-git-closeout/team这类spec子目录,  spec的SDD和goal+team应该是平行关系而不是从属关系. '临时'和'全局'也不是一个标准概念, 需要进行重定义. spec和goal+team的关系应该类似于 '设计师'和'施工队'..."
  non_goals: [新增 /speckit.* 命令, 第二个 goal/team 引擎, 破坏性迁移旧数据（archive-not-delete）, 改变 SDD 阶段链与哨兵]
  acceptance_authority: .specify/specs/094-goal-team-parallel/requirements.md（待创建；输入简报 .specify/.tmp/sdd-loop/tmp/goal-team-parallel/design.md）
  stage_plan: [requirements, clarify, plan, tasks, checklist, analyze, implement, review]
  decision_gates: [split-required (>120 FR / >160 tasks), fast-fail decision, destructive confirmation, push authorization]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 以目标代替规则做审计, 跳过 checklist/analyze/review, 把 goal/team 写成 spec 的从属物]
project_config:
  target_project: /storage/project/cloud-native-ai/spec-kit
  target_governance: .specify/memory/constitution.md + .specify/instructions.md
  execution_topology: local-native-subagents
  spec_dir: .specify/specs/094-goal-team-parallel
  evidence_dir: .specify/specs/094-goal-team-parallel/test-evidence
  write_isolation: worktree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 6
  agent_concurrency_requested: 24
  agent_concurrency_effective: 24
  agent_concurrency_reason: local native subagents; ready packages recomputed per stage; implement packages ~10 tasks, up to 6 concurrent
  verifier_reserve: 1
  breakpoint_verdict: "requirements + clarify + plan + tasks + checklist complete; next stage = analyze"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
gates: |
  requirements U4: pass — validate ok 0/0; pre-analyze pass 0/0; 35 FR / 10 SC; commit af1fcae3
  clarify U4: pass — 42 FR / 11 SC; overlap clear; validate ok 0/0; pre-analyze pass 0/0; commit 8badbd03
  plan U4: pass — 111 clauses; 7 tensions; pre-analyze pass 0/37; decomposition proceed; overlap adjudicated; commits 58516812 + 679a3f51; team created
  tasks U4: pass — 80 rows / 7 packages; decomposition proceed; pre-analyze pass 0/86; validate-tasks 0 errors/1 warning; commit 00c36d9c
  checklist U4: pass — 40 items; both gates pass with red-first proof; 8 fail rows are requirements defects for analyze; commit d8ec0a1e
  analyze U4: conditional — report delivered; 1 CRITICAL + 5 HIGH block implement; repair brief written; next = analyze-repair
  analyze-repair U4: pass — C-01/H-01…H-05/M-01…M-05/L-01 closed, L-02 = features record refreshed, L-03 residual; validate-requirements 0/0; account-clause-coverage FR 42/42; validate-tasks 0 error / 1 disclosed warning; pre-analyze 3 stages pass (fr=42); validate-decision-tensions ok (7 records); decomposition --mode tasks proceed (fr=42/tasks=80); commit dae4a26c; next = analyze round 2
  tasks U4: pass — 80 rows / 7 packages / 111 clause attributions; decomposition proceed; pre-analyze pass 0/86; validate-tasks 0 errors / 1 disclosed warning
  analyze-repair round 2 U4: pass — C-2/H-2/H-3/H-4/H-5/M-3 closed; FR 43/43 (was 42/42); 113 clauses (was 111); validate-requirements 0/0; coverage fr 43/43 uncovered-beyond-baseline 0; validate-tasks 0 error / 1 disclosed warning; decision-tensions ok 7; pre-analyze x3 pass 0 non-advisory; decomposition --mode tasks proceed 43 FR/83 tasks; ledger notes/analyze-round2-repair.md; evidence test-evidence/analyze-repair2-*; commit d03fca61; next = analyze round 3
  checklist U4: pass — 40 items (100% traceable, soft cap 40 met); G-checklist-reader pass (mutation probe -> fail, exit 1); G-checklist-duplicate pass; validate-requirements ok 0/0; 8 fail rows are requirements findings for analyze
  analyze round 2 U4: fail — NOT ready to implement; 1 CRITICAL (C-2 contract C-71 keeps the refuted predicate; no clause names `source`) + 4 HIGH (H-2 feature-ref map stale 36/42; H-3 18 archive residents lack the binding record C-1 demands, no owner; H-4 command:<name> unit-id outside engine grammar; H-5 repair-note closures absent from plan.md/feature-ref.md) + 4 MEDIUM + 3 LOW; closure 11/14 rows hold (H-02, M-04 do not); six gates green (validate-requirements 0/0; coverage --corpus-root fr 42/42 0 beyond baseline; validate-tasks 0 err/1 disclosed warn; decision-tensions 7 ok; pre-analyze x3 pass; decomposition proceed 42/80); M-2 repaired in passing; report notes/analyze-round2-findings.md; next = analyze-repair round 2
wrapup: requirements records committed in af1fcae3; spec-local goal created; tasks stage records in test-evidence/ (+ coverage-baseline.txt); run-determination + exec-quant recorded; checklist stage: test-evidence/checklist-readings-2026-11-09.txt + checklist-gates-2026-11-09.txt + run-determination-checklist.txt; run-determination + exec-quant + feedback recorded for /speckit.checklist
framework_observations:
  - "Concurrency-line gate leakage (driver-measured 2026-11-09): when two lines share one driver session whose cwd is line B's worktree, a gate that derives its corpus/repo root from cwd reads the sibling line's spec into line A's verdict. Measured: a 092 verification run of account-clause-coverage.py (no --corpus-root) reported 57 false `beyond the frozen baseline` clause names, all from 093's contracts; pre-analyze-check.py has the same shape via --repo. Framework location: .specify/scripts/python/account-clause-coverage.py default corpus root, .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py repo resolution. Impact: driver U4 must pass explicit --corpus-root/--repo whenever it stands outside the target tree."
  - "Analyze-repair loop cost (measured 2026-11-09): 092's analyze phase consumed ~60 of the 136 wall-clock minutes because round 1's repair claimed closures that round 2 disproved — repair commit dae4a26c never touched plan.md or feature-ref.md, and no gate looked at file-level deltas. Fix applied for round 3: repair briefs must name target files, and the verifier reads git show --stat <repair-commit> before accepting any prose closure."
  - "Fork-model directive (user, 2026-11-09): the host's in-process subagents share one process/CPU, so fan-out beyond a few saturates a single core and total throughput drops even on a 192-core machine. Analysis/repair waves MUST use the fork model — separate qodercli child processes launched through .specify/skills/sdd-loop-driver/scripts/stage-runner.sh (stdin prompt + stream-json + sentinel; validated 2026-11-09: sentinel=1, exit=0) — sized to nproc, never host-internal Agent fan-out."
  - "Concurrency-model correction (user directive 2026-11-09; routed sdd-capability-or-contract-change at 2026-11-09T09:31:51Z): the host-internal in-process subagent path is BANNED under concurrency — it shares one process/CPU, saturates it, and hangs the main agent; it is no longer an optimization option to consider. Default local carrier = fork (same-family qodercli child processes via stage-runner.sh) or subprocess (heterogeneous agent CLIs). Correction scope: skills/external/sdd-loop-driver (SKILL.md HR6/U2/topology table + references dispatch-recipes/watch-model/decomposition-model/stage-prompts + templates/stage-team-preset), sdd-house-keeping, sdd-project-setup, coaching-skills, skills/internal/analyze-artifacts, shared/workflow/execution-topology.md, shared/workflow/external-dispatch-recipes.md, shared/definitions/agent-definitions.md + subagent-definitions.md, contract tests test_sdd_loop_driver_skill / test_sdd_project_setup_skill / test_coaching_run_contract / test_sdd_carrier_contract; mirrors re-synced. Lands through the 093 line (its implement stage owns the framework-source edits)."
  - "Test-runner ownership (driver-measured 2026-11-09): the canonical runner scripts/bash/run-tests.sh is the sole xdist entry (default -n <effective> --dist load, Python>=3.9 guard, C-009 no-叠加). Implement workers dispatched with a raw `python3 -m pytest -q` bypassed it and ran the full suite single-process for 10+ minutes while the machine sat at ~3% load (192 cores). Dispatch briefs MUST name the runner as the test entry, never a raw pytest command."
