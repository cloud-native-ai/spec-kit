# Line State — 090-re-anchoring

<!-- loop-state:begin -->
spine_state: running
run_id: r20261108T220214Z-8647
slice: 090
stage: checklist
stage_started_at: 1794179659
stage_deadline_epoch: 1794190459
stage_base_commit: 9af8418e
attempt: 1
retry_limit: 3
last_verdict: tasks U4 pass (b2d7612b; validate-tasks PASS; decomposition proceed 10/38); F-6/F-7 routed to rows T032/T033; checkpoint 03 on-track
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
next_action: dispatch checklist (SDD Checklist Worker); U4 must show a dated checklist file under checklists/ and the checker verdict
direction_contract: |
  goal_verbatim: "将『开局加载一次』的动作，变成『每执行完一个核心步骤就再加载一次』，使用 session compact + reload + evaluation 来明确和最开始的方向是否存在偏差；在核心概念中针对 agent 加入『不忘初心：一直记得最开始的任务和规则』和『温故而知新：通过不断复习来强化记忆和回顾目标』"（后续纠正：回顾的重点是规则而不是目标——目标由当前/下一步隐含，被丢弃的是规则）。
  non_goals: [每工具调用重载全文, 新增评分器/日志服务/调度器, 第二个 checkpoint 系统, 改写历史记录, 改动 sdd-loop-driver 的阶段序列与哨兵]
  acceptance_authority: .specify/specs/090-re-anchoring/requirements.md（FR-001…010 / SC-001…004）
  stage_plan: [clarify, plan, tasks, checklist, analyze, implement, review]
  decision_gates: [split-required (>120 FR / >160 tasks), fast-fail decision, destructive confirmation, push authorization]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 以目标代替规则做审计, 跳过 checklist/analyze/review]
project_config:
  target_project: /cws_data/cloud-native-ai/spec-kit
  target_governance: .specify/memory/constitution.md v1.19.0 + .specify/instructions.md
  execution_topology: local-native-subagents
  spec_dir: .specify/specs/090-re-anchoring
  evidence_dir: .specify/specs/090-re-anchoring/test-evidence
  write_isolation: shared-tree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 2
  agent_concurrency_requested: 24
  agent_concurrency_effective: 24
  agent_concurrency_reason: local native subagents; ready packages will be recomputed per stage
  verifier_reserve: 1
  breakpoint_verdict: "requirements present (Draft) + implementation pre-landed; no clarify/plan/tasks artifacts => next stage = clarify"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
gates: |
  requirements U4: pre-analyze --stage requirements decision=pass (errors=0); decomposition-check --mode plan proceed (fr=10)
  clarify U4: overlap-check decision=clear; checkpoint 01 written
wrapup: pending
framework_observations:
  - "The 090 line's implementation was pre-landed while the spec chain had not run; the driver must verify the chain against an already-written tree, so every stage's U4 compares the artifact to the landed state rather than creating it."
temp_goal_slug: 090-re-anchoring
temp_team_slug: 090-re-anchoring
temp_team_path: .specify/specs/090-re-anchoring/team/090-re-anchoring/team.md
