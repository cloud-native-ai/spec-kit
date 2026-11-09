# Line State — 093-concurrency-by-default

<!-- loop-state:begin -->
spine_state: running
run_id: r20261109T080000Z-093a
slice: 093
stage: clarify
stage_started_at: 1794210342
stage_deadline_epoch: 1794221142
stage_base_commit: e55d8136
attempt: 1
retry_limit: 3
last_verdict: "U4 pass — CLARIFY-DONE; Mode A on requirements.md; 15 ruled questions (each machine-read); 33 FR / 12 SC / 11 STR; validate ok 0/0; pre-analyze --stage requirements pass 0/0; overlap-check decision=clear but checked_specs=1 (VACUOUS — 093 declares no delivery surface yet); Feature 093 bound (Draft, index 86→87 + detail); F-093-001/002/003 registered; checkpoint 02; commit pending record; next = plan in its own worktree"
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
next_action: dispatch plan in the 093 worktree (its own branch/worktree per the 092 parallel-line addendum); plan MUST write feature-ref.md with file-level paths and adjudicate F-093-001 against 064/070/086
direction_contract: |
  goal_verbatim: "在当前speckit框架中的所有技能,命令和更高阶的goal,team,loop等都需要将subagent并发作为基本属性, 在能用并发的情况下默认都应该是并发的"
  non_goals: [新增 /speckit.* 命令, 第二个派发引擎/registry, 无条件并行（依赖/写冲突/宿主限制时必须串行）, 改变 SDD 阶段链与哨兵]
  acceptance_authority: .specify/specs/093-concurrency-by-default/requirements.md
  stage_plan: [requirements, clarify, plan, tasks, checklist, analyze, implement, review]
  decision_gates: [split-required (>120 FR / >160 tasks), fast-fail decision, destructive confirmation, push authorization]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 以目标代替规则做审计, 跳过 checklist/analyze/review, 声明并发而实际串行]
project_config:
  target_project: /storage/project/cloud-native-ai/spec-kit
  target_governance: .specify/memory/constitution.md + .specify/instructions.md
  execution_topology: local-native-subagents
  spec_dir: .specify/specs/093-concurrency-by-default
  evidence_dir: .specify/specs/093-concurrency-by-default/test-evidence
  write_isolation: worktree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 6
  agent_concurrency_requested: 24
  agent_concurrency_effective: 24
  agent_concurrency_reason: local native subagents; ready packages recomputed per stage; implement ~10 tasks/package up to 6
  verifier_reserve: 1
  breakpoint_verdict: "clarify CLARIFY-DONE; next stage = plan (its own worktree)"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
gates: |
  requirements U4: pass — validate ok 0/0; pre-analyze pass 0/0; 36 FR / 12 SC; commit a6b571f4 (executor claim only; independent verifier not yet run)
  clarify U4: pass (executor claim only; independent verifier not yet run) — validate ok 0/0 (33 FR / 12 SC / 11 STR); pre-analyze --stage requirements pass 0/0; overlap-check clear but VACUOUS (checked_specs=1)
  validate-requirements: pass — .specify/specs/093-concurrency-by-default/test-evidence/validate-requirements.txt ; clarify: test-evidence/validate-requirements-clarify.txt
  pre-analyze-check (stage=requirements): pass — .specify/specs/093-concurrency-by-default/test-evidence/pre-analyze-check.txt ; clarify: test-evidence/pre-analyze-check-clarify.txt
  overlap-check (clarify U4): clear-vacuous — test-evidence/overlap-check-clarify.{txt,json}
wrapup: done (requirements stage) — run-determination 093-requirements-a1 recorded; exec-quant recorded; feedback recorded
wrapup_clarify: done — run-determination 093-clarify-a1 recorded for /speckit.clarify + skill:clarify-artifact; exec-quant + feedback recorded (both)
feature_binding: "Feature 093 Concurrency by Default (Draft) — index header 86→87 + row + memory/features/093.md"
findings: "F-093-001 delivery-surface overlap vs 064/070/086 (open, plan-owned); F-093-002 overlap-check vacuous clear under a nested worktree repo (open, framework); F-093-003 coordinator dispatch verdict owner missing (open, STR-011)"
framework_observations:
  - "Blockquote-wrapped text is invisible to validate-requirements.py and pre-analyze-check.py: a spec whose FR/SC definition rows were altered so they no longer matched '^***' still returned status=ok with definition_rows derived only from what remained — the check is a filter, not a totality assertion."
  - "The two validators disagree on definition-row syntax: validate-requirements.py treats 'FR-007' with a trailing fullwidth colon as a non-definition (silently), while pre-analyze-check.py still resolves the reference through '\\bFR-(\\d{3})\\b' and reports the row as a dangling id — the pair detects the drift only by accident."
  - "pre-analyze-check.py § Runtime Stack 'Contract' cells reject a backticked path followed by a section anchor suffix, while the same shape is accepted in ordinary prose." 
  - "validate-requirements.py id-contiguous rejects letter-suffixed ids (FR-003a) and offers no safe add/remove path: a single mid-list addition forces folding or a full-tail renumber. Hit twice on this line (092 recorded the same friction) — recurrence 2."
  - "ref-resolvable's shared-string check is bidirectional: listing a row in 'Consumed by' is not enough, the row must itself cite [[STR-NNN]]. The taxonomy's own instruction ('cite from the row that consumes it') is what makes the pair work, and it caught six rows in one pass."
  - "overlap-check.py --repo <repo> where <repo> is the worktree itself puts '..' at the head of current_rel, so every declared path is filtered by startswith(spec_rel) and the engine answers 'no declaration artifact' (vacuous clear). Worktree-per-write-line is the house default, so this is the common case, not an edge (F-093-002)."
  - "pre-analyze-check.py's missing-path advisory reads Clarifications history rows as live paths: an old path quoted inside a dated Q/A bullet raises an advisory that can only be cleared by editing history (forbidden) — the gate should skip dated sections."
  - "declaration_reader.py --action list returns contract.yaml's own keys alongside facts/ slugs (one namespace, two kinds of member); --action get for an absent fact exits 1 with 'no declaration for fact …', not 2. Any 'owner-unavailable ⇒ exit 2' clause written against the reader must be reconciled with that observed exit code."
