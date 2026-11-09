# Line State — 091-auto-git-closeout

<!-- loop-state:begin -->
spine_state: completed
run_id: r20261109T023000Z-auto-closeout
slice: 091
stage: closure
stage_started_at: 1794202090
stage_deadline_epoch: 1794212890
stage_base_commit: 9d5acb7a
attempt: 1
retry_limit: 3
last_verdict: "Closure complete — closure-acceptance-check accept (final_path 6/6); final serial suite 44 failed / 8064 passed; NEW 16 all R-36a (A/B proven), NEW=0 with R-36a; CLEARED 8; 5 review blocking findings closed by P1/P2/P3; registry Completed; next = merge + push + published-ref verification"
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
next_action: merge 091-auto-git-closeout into master, push gitlab/github/gitee, verify the three published master refs (F2 5b), then remove the feature branch
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
  write_isolation: worktree
  decomposition: auto
  decomposition_stages: [plan, implement, review]
  decomposition_slot_cap: 6
  agent_concurrency_requested: 24
  agent_concurrency_effective: 24
  agent_concurrency_reason: local native subagents; ready packages will be recomputed per stage
  verifier_reserve: 1
  breakpoint_verdict: "analyze round 1's blocking C-01/H-01..H-04 are resolved in commit 9d5acb7a and five gates are green; analyze round 2 is the next gate and MUST include the C/H validation wave round 1 could not dispatch"
  flow_class_quartet: "flow_class=execution; source=declaration; marker=; error=-"
gates: |
  requirements U4: pass — validate ok 0/0; pre-analyze pass 0/0; 27 FR / 7 SC; evidence .specify/specs/091-auto-git-closeout/test-evidence/requirements-gates.txt
  clarify U4: pass with corrections — validate ok 0/0; pre-analyze pass 0/0 after RS-001 cell + feature-ref count fixes; overlap adjudicated (completed-only, 0 active); decomposition-check plan proceed (28 FR < 120); workspace-guard clean
  plan U4: pass — pre-analyze plan 0/0; 26 clauses across 4 contracts; 5 decision tensions 0/0; 22/22 Constitution; checkpoint 03 accepted; Temporary Team created (validate-roster conforming)
  tasks U4: pass — decomposition proceed (60 tasks < 160); pre-analyze tasks pass 0 errors/46 advisories; validate-tasks 0 errors/46 warnings adjudicated; forward condition: implement T056 freezes the clause baseline
  checklist U4: pass — 47 items; duplicate pass; G-checklist-reader pass (path form); validate-requirements ok; pre-analyze pass 0 errors/46 advisories; 15 fail items are requirements-quality findings for analyze/implement; record anomaly disclosed
  analyze U4: conditional — sentinel + report + wrap-up present; 1 CRITICAL + 4 HIGH block implement; repair brief at test-evidence/analyze-round1-findings.md
  analyze-repair U4: pass — C-01 resolved (FR 28/28 uncovered 0); H-01..H-04 resolved; validate-requirements ok 0/0; pre-analyze requirements pass 0/47; pre-analyze plan pass 0/47; decision-tensions 5/0; decomposition proceed; commit 9d5acb7a
  analyze round 2 U4: pass — CRITICAL=0 / HIGH=0; 20/20 resolved; residual 10 dispositioned; 32 clauses / 28 FR uncovered 0; five gates green
  implement U4: pass — 62/62 tasks; full suite 34 failed / 8045 passed; NEW=0 with R-36a applied (4 pre-existing compile_embeds ids, A/B proven), cleared 6; gates green; verification.md; commit 9f635f75
  analyze-repair U4: done — commit 9d5acb7a; C-01 + H-01..H-04 resolved; 11/13 MEDIUM + 4/4 LOW resolved; clauses 26 -> 32;
    tasks 60 -> 62; FR coverage 24/28 -> 28/28; five required gates green (see below)
    evidence: test-evidence/analyze-repair-round1.md (dispositions by ID) + test-evidence/analyze-repair-gates.txt (readings)
    gates: validate-requirements ok 0/0 (320 lines) | pre-analyze requirements pass 0 errors/47 advisories (fr=28 sc=8 tasks=62)
      | pre-analyze plan pass 0 errors/47 advisories | validate-decision-tensions 5 records 0/0 | decomposition proceed fr=28
    supporting: account-clause-coverage FR claimed 28/28 uncovered 0 (still status=baseline-missing by design, T056 owns the freeze)
      | validate-tasks 0 errors/69 warnings, green-dangling+collision 0, green-cross-phase 2 (both disclosed)
      | doc-consistency --faces reader --path requirements.md reader=pass (was reader-declaration-missing)
    residual: none of C/H/M/L silently dropped; the 5 analyze-owned CHK dispositions (CHK011/016/038/040/045) stay open for round 2
  clarify U4 (pending verifier):
    overlap_check: decision=overlap — before the declaration artifact the gate was clear with
      checked=1 and note "no declaration artifact" (vacuous); after it: checked=82, overlaps=36
      over 5 paths, 0 against any active line (line-registry --action list --active => []).
      Adjudicated as C-16 in requirements.md + feature-ref.md § Adjacency; implement MUST re-run.
      evidence: test-evidence/overlap-check-clarify.json + test-evidence/clarify-gates.txt § 3-4
    validate_requirements_after_clarify: ok 0/0 (304 lines, 36 definition rows, 6 shared strings)
    pre_analyze_input_error: pre-analyze-check.py --stage requirements exits 2 on an UNCHANGED
      cell (clause_extract line 177, RS-001 Contract): clean_cell() strips with str.strip("`"),
      so a paired code span followed by prose is read as a path. Reproduced on a /tmp copy;
      the identical post-clarify artifact passes once that one cell is bare (decision=pass,
      errors=0, fr=28, sc=8). Class = pre-analyze-check.py parsing defect (driver skill = the
      owner, not editable from this stage); surfaced, not repaired. No clarify-added clause is
      implicated. evidence: test-evidence/clarify-gates.txt § 6
  plan U4 (candidate):
    pre_analyze_plan: decision=pass errors=0 advisories=0 waived=0 (fr=28, sc=8, files=10)
      evidence: test-evidence/plan-gates.txt § 5 + test-evidence/pre-analyze-plan.json
    validate_decision_tensions: 5 records, 0 error 0 warning (T-001..T-005 dense)
      evidence: test-evidence/decision-tensions-plan.json
    validate_requirements: ok 0/0 (306 lines, 36 definition rows, 6 shared strings)
    decomposition_plan: decision=proceed fr_count=28 fr_ceiling=120
    overlap_plan: decision=overlap checked=82 overlaps=36 over 7 declared paths — 36 rows all land on
      completed spec lines, 0 on an active line (line-registry --action list --active => []); same reading
      as clarify C-16. evidence: test-evidence/overlap-check-plan.json + plan-gates.txt § 3 and § 5
    plan_integrity: 1 top-level H1; Requirement -> Feature stamp present; 0 residual UPPER_SNAKE placeholders
    corrections_in_passing: 2 — EP-006 Evidence cell carried a pipe-delimited number the premise parser read
      as its Status; the Inherited Blockers Disposition cell used an em dash outside the closed set
      (verified/unverified are for premises; resolved/inherited/not-applicable for blockers). Both disclosed.
    inherited_blockers: none (the row is explicitly not-applicable)
wrapup: done (clarify, unit skill:sdd-loop-driver, run r20261109T023000Z-auto-closeout)
  run_determination: .specify/memory/session/20261109T023417Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
    (four quantities not_evaluated: token/elapsed source_unavailable, correctness no_baseline,
     satisfaction pending_next_turn; passive_trigger.trigger_feedback=false)
  exec_quant: .specify/memory/exec-quant/records/20261109T023419477214Z-26fe7a30.json
  feedback_record: .specify/memory/feedback/20261109T023425Z-skill-sdd-loop-driver.md
  threshold_notice: should_prompt=true (351/10) composed with trigger_feedback=false => NOT surfaced
  token_reflection: no instrumented token source; self-assessment = the largest avoidable spend
    was re-running overlap-check three times while learning that its declaration collector reads
    every backticked path; reading _collect() first would have cost one run instead of three.
wrapup: done (analyze-repair, unit skill:sdd-loop-driver, run r20261109T023000Z-auto-closeout-repair1)
  run_determination: .specify/memory/session/20261109T032435Z-run-determination-skill-sdd-loop-driver-r20261109t023000z-au.md
    (four quantities not_evaluated: token/elapsed source_unavailable, correctness no_baseline,
     satisfaction pending_next_turn; passive_trigger.trigger_feedback=false; 5 declared checks / 5 green)
  exec_quant: .specify/memory/exec-quant/records/20261109T032439928949Z-5f18730f.json (score 4, score record in exec-quant/scores/)
  feedback_record: .specify/memory/feedback/20261109T032455Z-skill-sdd-loop-driver.md (6 optimization points)
  threshold_notice: should_prompt=true (356/10) composed with trigger_feedback=false => NOT surfaced
  token_reflection: no instrumented token source for a subagent slice; the two largest avoidable spends were
    (a) four failed attempts to place the 32-clause green partition because validate-tasks.py's green-cross-phase
    compares clause order against ROW order — reading that check's source before moving tags would have cost one pass;
    (b) one wrong run-determination invocation passing gate-evidence paths to --names-current/--names-baseline,
    which want FAILED-test-nodeid lists.
wrapup: done (plan, units skill:create-plan + skill:sdd-loop-driver)
  run_determination: .specify/memory/session/20261109T024806Z-run-determination-skill-create-plan-r20261109t025000z-auto-c.md
    (four quantities not_evaluated: token/elapsed source_unavailable, correctness no_baseline,
     satisfaction pending_next_turn; passive_trigger.trigger_feedback=false; same store carries the
     stage's own driver-unit record at .specify/memory/session/20261109T023417Z-... for the clarify run)
  exec_quant: .specify/memory/exec-quant/records/20261109T024808293296Z-6583474b.json
  feedback_record: .specify/memory/feedback/20261109T024802Z-skill-create-plan.md (5 optimization points)
  threshold_notice: should_prompt=true (352/10) composed with trigger_feedback=false => NOT surfaced
  token_reflection: no instrumented token source for a subagent stage; the largest avoidable spend was the
    three pre-analyze iterations, each caused by a gate parser reading free text (a pipe-delimited cell and an
    em-dash cell) — reading the premise/blocker parser first would have cost one iteration instead of three.
review_stage: done (fail / fail / fail / blocked; ARC refused)
  verdicts:
    process: fail — P0 unauthorised `Implemented` claim written by the implement stage (F1), P0 published mirrors left at
      e06fcc52 on github/gitee by the branch correction (F2); 3 P1 + 6 P2 reusable friction
    artifact: fail — expected set 16/16 present (`missing none`), completeness passes, acceptance honesty fails (A-02, A-03)
    implementation: fail — scope over-delivery into docs/ plus two of the four target criteria supported only by the
      fixture's planner, not by the shipped surface (I-01, I-02); smoke re-ran `42 passed` exit 0
    code: blocked — code-review.md, changed/judged/skipped/gap = 371/371/0/0, 6 findings (3 blocking C1–C3),
      `report --summary --file` => blocking_entries=3, gate=deny
    arc: refused — closure-acceptance-check.py verdict `block`, final_path pass 0 / blocked 0 / deferred 0 / partial 0 /
      fail 0 / unknown 6 / total 6; claim `Implemented` left unchanged; fixed item F-ACCEPTANCE at P0
  target_criteria_evidence (direction_contract):
    four_workflow_models: partial — 6 structural arms + per-model push-remote sequences pass, but the read-only
      exclusion computed in plan.py:144 is discarded at repo.py:281 (F4) and no arm passes `remote_name=` (C3)
    ask_or_absent: pass — `Closeout` four-value closed set, git.md managed block + `Closeout remotes`; absent/ask arms green
    fail_stop: pass — first-failure stop, no force push, no retry, state recorded (mutation probe + failure fixtures)
    single_mechanism: partial — one owner (`artifact-commit-step.md` § Close-out) with a pointer from every unattended
      mechanism proven by a negative search, but that same search reds on the feature's own close-out heading (F5/C2)
  checked_this_stage: R-36a residual (pre-existing, reproduced at HEAD with the feature stashed, not repaired here);
    humanize out-of-territory edit (accepted as a correction, 4998/5000 shape pass); branch correction (local ok,
    published refs divergent — F2); implement two-slice flow (WIP 18d9c3bc + completion 9f635f75, no hand-back)
  blocking_disposition: all three code blocking items and both P0 process items are fixed-in-place at a named landing
    point (REC-T1 / REC-W1 / REC-W3 / REC-A1 / REC-A2) and stay OPEN — the review stage does not repair product code;
    the closure stage must land or explicitly waive them
  artifacts: .specify/specs/091-auto-git-closeout/review.md, code-review.md, test-evidence/arc-closure-check.json,
    test-evidence/review-2026-11-09/{smoke-rerun,gates-rerun,confirmation-gates-rerun,code-segment-base}.txt
  checkpoint: .specify/specs/091-auto-git-closeout/checkpoints/10-review.md
wrapup: done (review, units skill:review-feature-quality + skill:review-sdd-process, runs r20261109t023000z-auto-closeout)
  run_determination: .specify/memory/session/20261109T053527Z-run-determination-skill-review-feature-quality-r20261109t023.md
    .specify/memory/session/20261109T053545Z-run-determination-skill-review-sdd-process-r20261109t023000z.md
    (four quantities not_evaluated: token source_unavailable, elapsed not_comparable, correctness no_baseline,
     satisfaction pending_next_turn on both units)
  exec_quant: .specify/memory/exec-quant/records/20261109T053548472154Z-e0e08f1f.json
    .specify/memory/exec-quant/records/20261109T053548795074Z-6e7093c5.json
  feedback_record: .specify/memory/feedback/20261109T053552Z-skill-review-sdd-process.md
    .specify/memory/feedback/20261109T053556Z-skill-code-review.md
  threshold_notice: should_prompt=true => NOT surfaced (no user turn in an unattended subagent slice)
  census: 3 units — review-sdd-process and code-review recorded above (run-determination + exec-quant), driver unit
    recorded by the implement slice 2 block; no feature-quality (implementation/artifact) unit exists as a skill, so
    that segment's accounting rides on review-sdd-process (disclosed, not silently dropped)
  token_reflection: no instrumented token source; the largest avoidable spend was the review coordinator's own
    inability to dispatch subagents — two reviewer briefs were composed at .specify/.tmp/review-091/briefs/ and never
    dispatched, so the same 371-file delta was read once instead of in parallel, and the objective-analysis gate
    fell back to direct re-read for every P0 (F11). Second spend: sequential string surgery on review.md corrupted
    the file and cost a full repair pass; emitting the document in one pass would have avoided it.
wrapup: done (implement completion slice 2, unit skill:sdd-loop-driver, run implement-091-slice2)
  run_determination: .specify/memory/session/20261109T050936Z-run-determination-skill-sdd-loop-driver-implement-091-slice2.md
    (four quantities not_evaluated: token source_unavailable, elapsed not_comparable, correctness no_baseline,
     satisfaction pending_next_turn; 1 declared check / 2 collected)
  exec_quant: .specify/memory/exec-quant/records/20261109T050941886215Z-44baddaa.json
  feedback_record: .specify/memory/feedback/20261109T050944Z-skill-sdd-loop-driver.md
  threshold_notice: should_prompt=true (358/10) => NOT surfaced (no user turn in an unattended subagent slice)
  token_reflection: no instrumented token source; the largest avoidable spend was three full-suite runs where one
    would have done — the first two started while the tree was still being edited (mirror sync + humanize slimming),
    so both caught a mid-edit state and had to be discarded. Starting a full run only after `git status` is clean of
    in-flight edits would have saved ~19 minutes of wall clock.
implement_slice_2: done
  tasks: 62/62 rows checked, each with an evidence pointer; DoD Status: met
  artifacts: .specify/specs/091-auto-git-closeout/verification.md (SC/GATE/DoD tables, rulings R-14..R-23 + R-21b + R-37/R-38, residuals R-36a/R-36b)
  suite: final-full.txt 34 failed / 8045 passed / 2 skipped (566.07s); final-failed.txt vs baseline-failed.txt =>
    NEW 0 once R-36a (test_compile_embeds.py, red at HEAD too) is applied, cleared 6
  repaired-at-root: three compiled-face closing-step pins + analyze's C-5 containment allowance (read out of git)
    + humanize body budget 5023 -> 4998 tokens
  gates: sync-mirrors 0 | compile-embeds 0 (79 units, zero drift) | closeout contract 42 passed | four-model arms 6 passed
    | dry-run exit 0 | validate-tasks 0 errors | account-clause-coverage status ok (FR 28/28, 32 clauses)
    | scan-confirmation-gates 27/20/7/violations 0
framework_observations:
  - "The tests/ tree is collected TWICE in a plain `pytest tests/` run: the repo-root `scripts/` mirror and `.specify/scripts/` project the same modules, so a full run reports ~8000 passed for a suite whose distinct assertions are far fewer. The count is therefore not a comparable quantity across selections, and this feature's GATE-1 had to be judged on the failed node-id set alone; the passed total moved by 219 between two runs of the same selection purely because one run also included three extra modules."
  - "tests/contract/test_compile_embeds.py, test_engine_face_contract.py and test_compile_reconcile_guards.py build a throwaway workspace by copying the LIVE probe registry plus a hand-maintained `_OWNER_COPIES` list (feedback-step.md, docs-step.md, create-team SKILL, confirmation-gates.md). Any registry row whose behaviour owner is not on that list makes the sandboxed compile exit 2, so the module reds for a reason that has nothing to do with the change under test — 091's `h-closeout` (owner: shared/workflow/artifact-commit-step.md) is the current instance, but the defect is structural: the copy list should be derived from the registry it copies."
  - "Compiled `## Wrap-up` faces are pinned verbatim by at least five independent contract modules (client-guard sweep C-53, review composition C-16, review feedback boundary C-55, decision-tension C-5, humanize WC-07 body budget) with no shared owner for the expected set. One registry row therefore forces five separate re-pins in five files, each with its own containment argument, and a sixth pin (a skill body token budget) can break without any step-set assertion being involved. A single 'expected compiled step set' owner — derived from the registry — would make all five read from one place."
  - "A skill body token budget (humanize WC-07, 5000) has ~1 token of headroom at HEAD (4999), so ANY registry addition that compiles a step into every skill face pushes it over: the 091 row cost 24 tokens because of re-wrapping, and the repair had to delete body text that the skill's own contract already owned elsewhere. A budget whose only growth direction is deletion needs either headroom or a documented way to re-derive it."
  - "validate-tasks.py's green-path-divergence warning count is quadratic in the number of rows that mention the same test path, so appending an `— evidence: tests/...` pointer to every row inflates the count from 69 to 381 without any claim changing. A warning count that moves on a documentation-only edit cannot be used as a gate signal, and its message ('two rows cannot each be the one that turns this file green') describes a detector premise the plan explicitly rejected."
  - "pre-analyze-check.py Runtime Stack Contract check: clean_cell() uses str.strip(chr(96)), so a PAIRED inline code span followed by prose is parsed as a path and the check exits 2 (input error). Any spec annotating its Contract cell this way is falsely blocked. Owner = driver skill, out of scope for a spec stage."
  - "overlap-check.py current-surface declaration is collected from every backticked shared-root path anywhere in feature-ref.md, including lines that say a document is NOT delivered. There is no way to mark a path as read-only input except by omitting its backticks, which conflicts with the file's own citation habit."
  - "overlap-check.py has no exit-code distinction between 'compared nothing because there is no declaration artifact' (clear, checked=1) and 'compared and found nothing'. A feature with no declaration passes the clarify U4 gate vacuously."
  - "run-determination.py --declared-check / --green-check: green values must be a subset of declared values (exact string membership, not substring); two invocations were rejected before the required form was found, and --help does not state the relation."
  - "docs/reference/skills/sdd-loop-driver.md and the driver's stage-prompts table omit run-determination.py --action settle from the clarify wrap-up, so a clarify run's satisfaction axis stays pending by construction; the sibling stage evidence shows the same standing gap."
  - "pre-analyze-check.py § Execution Premises row parsing treats any pipe-delimited cell inside free text as a field: an Evidence cell containing a table-shaped number was reported as `EP-006 declares Status: <number>`. The FAIL message names the parsed field, not the parsed cell, so the author cannot locate the defect."
  - "pre-analyze-check.py `missing-path` advisories fire on every backticked token that does not exist yet — i.e. exactly the files a plan promises to create. Declaring a deliverable and claiming a path exists are different propositions; one advisory class serves both, so the only way to a clean plan is to stop naming deliverables as paths."
  - "pre-analyze-check.py `inherited-blocker-undisposed` rejects the conventional empty-cell marker with the opaque key `<feature>:—`; the closed set (resolved / inherited / not-applicable) is not discoverable from the message."
  - "validate-decision-tensions.py enforces dense T-NNN order across the whole document, so inserting a record mid-document forces renumbering every later record; a T-NNN is positional rather than stable, and the renumbering is invisible to anything that cited the old number."
  - "Gate CLIs disagree on how to name the same concept: pre-analyze-check/overlap-check take --spec-dir, decomposition-check takes --requirements, validate-requirements takes a positional path, validate-decision-tensions takes --spec. Four scripts, four forms, no shared invocation contract."
  - "account-clause-coverage.py reads a clause's LAST FR-containing parenthetical as its citation group, so a clause that mentions an id in prose cites nothing. A spec can therefore assert 'every FR is discharged' in its own map while the accountant reports four uncovered — the two readings differ only by a rule stated in clause_extract.py's docstring, which the artifact author has no reason to read. The repair cost four clauses and a map rewrite; naming the citation-group rule in the validation message would have surfaced it at plan time."
  - "validate-tasks.py green-cross-phase compares clause ORDER against ROW order within one contract page, so a clause whose subject belongs to an earlier user story than the row that turns it green always warns — e.g. an authorization table (US1 concern) that must precede the sequences it authorizes (US3 content). There is no 'disclosed exception' channel, so the only honest resolution is a recorded adjudication plus a non-zero count asserted in the DoD; a zero-warning goal is unreachable without renumbering the page into a worse reading."
  - "run-determination.py --names-current/--names-baseline are sorted FAILED-test-nodeid lists, not free-text summaries, and --args-manifest does not say so. The flag names read like notes ('names current / names baseline'), so passing gate-evidence file paths is silently accepted as a 'baseline' and only fails on the existence check. Costs an invocation each time a caller has no test-run diff to report."
  - "run-determination.py admits custom:<owner>/<name> in its own record schema but the memory engine's --source contract rejects it: a custom unit's record is emitted and NOT landed, with the reason on stdout only. A subagent slice that identifies itself honestly loses its run record; identifying as skill:sdd-loop-driver lands the record but misattributes the unit. The engine reports the gap rather than dropping the record, which is the right failure mode — but the gap leaves no honest option."
  - "pre-analyze-check.py missing-path advisories fire on every backticked deliverable a plan has not created yet, so a feature's advisory count can only move by deleting its own deliverable names from its task rows. An advisory class that punishes declaring promised work is indistinguishable at a glance from a defect count, and this feature's count rose 46 -> 47 for exactly that reason (a new row names a new fixture directory)."
temp_goal_slug: 091-auto-git-closeout
temp_team_slug: 091-auto-git-closeout
temp_team_path: .specify/specs/091-auto-git-closeout/team/091-auto-git-closeout/team.md
