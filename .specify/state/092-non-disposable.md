# Line State — 092-non-disposable

<!-- loop-state:begin -->
spine_state: running
run_id: r20261109T024154Z-3301
slice: 092
stage: implement
stage_started_at: 1794197091
stage_deadline_epoch: 1794207891
stage_base_commit: 1a7fed0e
attempt: 1
retry_limit: 3
last_verdict: analyze 25 findings (1 CRITICAL / 8 HIGH) closed in a repair round (0fc3a33e): contracts 8 files / 62 clauses, FR uncovered 0, tasks PASS, pre-analyze pass
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
next_action: dispatch implement P1-P8 under the team; packages may run in waves, hand back a precise remainder if the turn budget ends
direction_contract: |
  goal_verbatim: "在 speckit 框架中引入『Non-Disposable』理念：任何过程和文档都不应该是『用过即丢』(Use and throw)，需要时常回顾和修正，同时过去的历史也是重要的参考和借鉴。这就要求设计一系列机制，杜绝『这个没用了但是留在这里』或『这个过时了但是我现在不想删除』等一系列将问题推到将来的行为。以上面分析 A~H 的结论作为这个新特性的输入和验证用例。新特性的落点可以放到 /speckit.history 命令中：speckit.history 命令执行时先回顾历史，然后进行设计给出方案，向用户确定是否执行。回顾历史需要回顾当前 git head 指向的 workdir 中的 .specify 目录中记录的历史文件，而不是 git history。需要将所有的 .specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}/* 这些带『历史』属性的目录和文件都纳入其中。这是一个浩大的工程，因此需要使用一个 team 通过大并发的 subagent 来完成。"
  non_goals:
    - 不删除或改写历史证据（archive-not-delete；历史记录本身不重写）
    - 不重写 git 历史（回顾对象是 HEAD 工作树的 .specify/，不是 commit 史）
    - 不新增第二套历史存储或第二个 /speckit.history 入口
    - 不一次性清理脚本替代机制（机制 > 一次性清理）
    - 不改阶段序列、哨兵字面量、watcher 判定与退出码
  acceptance_authority: .specify/specs/092-non-disposable/requirements.md（FR/SC 以该文件为准）
  stage_plan: [requirements, clarify, plan, tasks, checklist, analyze, implement, review]
  decision_gates: [split-required (>120 FR / >160 tasks), fast-fail decision, destructive confirmation, push authorization, design-approval-before-execute (/speckit.history 的方案确认门)]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 以目标代替规则做审计, 跳过 checklist/analyze/review, 把 A–H 修复做成一次性清理]
project_config:
  target_project: /cws_data/cloud-native-ai/spec-kit
  target_governance: .specify/memory/constitution.md v1.19.0 + .specify/instructions.md
  execution_topology: local-native-subagents
  spec_dir: .specify/specs/092-non-disposable
  evidence_dir: .specify/specs/092-non-disposable/test-evidence
  write_isolation: shared-tree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 15
  agent_concurrency_requested: 24
  agent_concurrency_effective: 15
  agent_concurrency_reason: 15-slot wave per the user's directive; effective = min(requested 24, stage max_parallel 15, ready 15 + verifier reserve 1) per 085 C-002
  verifier_reserve: 1
  breakpoint_verdict: "new feature; no spec directory yet => next stage = requirements"
  history_review_surface: ".specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}/* under the current git HEAD worktree"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
  validation_corpus: "the 080–090 cross-spec review A–H, persisted at .specify/specs/092-non-disposable/notes/input-review-080-090.md"
gates: |
  clarify — validate-requirements.py 0 error / 0 warning (65 FR / 20 SC, contiguous + document order);
  flow-class-check execution (source=declaration); validate-decision-tensions unreadable (no plan.md yet,
  0 findings); decomposition-check --mode plan proceed (fr=65 <= 120).
  readings: .specify/specs/092-non-disposable/test-evidence/clarify-gates.txt
  checklist — doc-consistency-check --faces reader|duplicate over the checklist (reader 0, duplicate 0 vs
  requirements.md and vs one-source-of-truth.md / checklist-methodology.md); spec-dir duplicate 0/22 files;
  spec-dir reader 21 pre-existing reader-declaration-missing findings, checklist not among them, 085 reads 23
  under the same predicate. readings: .specify/specs/092-non-disposable/test-evidence/checklist-gates.txt
wrapup: pending
framework_observations:
  - "The A–H review is itself evidence that history review must be semantic (claims/owners/constants), not a file-by-file listing."
temp_goal_slug: 092-non-disposable
temp_goal_path: .specify/specs/092-non-disposable/goal/092-non-disposable/goal.md
temp_team_slug: 092-non-disposable
