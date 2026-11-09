# Line State — 091-auto-git-closeout

<!-- loop-state:begin -->
spine_state: running
run_id: r20261109T023000Z-auto-closeout
slice: 091
stage: clarify
stage_started_at: 1794191292
stage_deadline_epoch: 1794202092
stage_base_commit: 7cf87dad
attempt: 0
retry_limit: 3
last_verdict: "U4 pass — REQUIREMENTS-DONE; validate-requirements ok (0/0); pre-analyze decision=pass (0/0); 27 FR / 7 SC; commits 47f15b6b + 7cf87dad; checkpoint 01 written; next = clarify"
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
next_action: dispatch clarify (host native subagent)
direction_contract: |
  goal_verbatim: "我每次在作为修改执行都会要求执行:提交,合并,推送, 这应该是一套固定流程,不需要每次都手动触发,在框架中需要找到一个合适的切入点. 需要注意的是:不同的项目存在不同的git workflow, 这个动作需要和git workflow相结合"
  non_goals: [新增 /speckit.* 命令, 守护进程/调度器, 第二套分支 registry, 自动强推, 托管平台 PR/MR 自动化]
  acceptance_authority: .specify/specs/091-auto-git-closeout/requirements.md（待创建；输入简报 .specify/.tmp/sdd-loop/tmp/auto-git-closeout/design.md）
  stage_plan: [requirements, clarify, plan, tasks, checklist, analyze, implement, review]
  decision_gates: [split-required (>120 FR / >160 tasks), fast-fail decision, destructive confirmation, push authorization]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 以目标代替规则做审计, 跳过 checklist/analyze/review, 自动强推或推只读上游]
project_config:
  target_project: /storage/project/cloud-native-ai/spec-kit
  target_governance: .specify/memory/constitution.md + .specify/instructions.md
  execution_topology: local-native-subagents
  spec_dir: .specify/specs/091-auto-git-closeout
  evidence_dir: .specify/specs/091-auto-git-closeout/test-evidence
  write_isolation: shared-tree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 2
  agent_concurrency_requested: 24
  agent_concurrency_effective: 24
  agent_concurrency_reason: local native subagents; ready packages will be recomputed per stage
  verifier_reserve: 1
  breakpoint_verdict: "requirements present; next stage = clarify"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
gates: |
  requirements U4: pass — validate ok 0/0; pre-analyze pass 0/0; 27 FR / 7 SC; evidence .specify/specs/091-auto-git-closeout/test-evidence/requirements-gates.txt
wrapup: pending
framework_observations: []
temp_goal_slug: 091-auto-git-closeout
