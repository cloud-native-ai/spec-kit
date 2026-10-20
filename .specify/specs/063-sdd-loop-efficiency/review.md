# Specification-Driven Development (SDD) Process Review Report: 063-sdd-loop-efficiency

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 063 |
| Requirement Key | 063-sdd-loop-efficiency |
| Requirement Name | sdd-loop-driver 运行效率优化（SDD Loop Efficiency） |
| Related Feature | 058 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver） |
| Repository | spec-kit |
| Repository URL | SSH-only remotes: `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` — none exposes an HTTPS web URL |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty (0 remotes contain the commit). All citations below use absolute local paths; recover any file with `git -C /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit show afca82f7:<path>` |
| Branch | 063-sdd-loop-efficiency |
| Commit SHA | afca82f77779a714eec56fe554f5799852ab3bcf (short: afca82f7) |
| Repo Root (absolute) | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit |
| Review Date | 2026-10-20 |
| Reviewer (Agent) | Qoder review-stage subagent (separate from the implement stage subagent; same-author gate not triggered because the reviewed artifacts predate this review stage) |
| Environment | macOS 25.6.0 arm64; bash 5.3.15(1); python3 3.9.6 (pytest unavailable via python3); python 3.14.6 + pytest 9.1.1 via `scripts/bash/run-tests.sh`; local direct-drive topology; state spine /tmp/sdd-loop-efficiency/state.md |
| spec-kit Source Snapshot | commit 9f2f7ba59ad63043e5598ce64fe1c82e025c5c69 (`.specify/source.json`, stamped 2026-10-19T065729Z) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 347 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/requirements.md | 43 FR / 13 SC / 8 shared strings; four loop-efficiency optimizations plus safety invariants |
| plan.md | 363 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/plan.md | Design by optimization, constitution check, five plan-repair records |
| tasks.md | 364 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/tasks.md | 53 task rows (T000 + T001…T052), seven target groups / 24 mutations |
| verification.md | 385 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md | Per-task gates, mutation tables, SC-001…SC-013 status table |
| research.md | 106 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/research.md | R-1…R-12 decisions plus B-1…B-8 measured baselines |
| data-model.md | 274 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/data-model.md | E1…E8 entities, 41 validation rules, stall behavior baseline SB-1…SB-5 |
| quickstart.md | 187 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/quickstart.md | S1…S7 scenarios with preconditions and pinning tests |
| feature-ref.md | 145 | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/feature-ref.md | FR/SC mapping, 24 deliverables, baseline records, exclusions |
| contracts/ (5 files, 50 clauses) | 300+ | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/contracts/ | FL-01…FL-10, TB-01…TB-10, PC-01…PC-11, PD-01…PD-10, DI-01…DI-09 |
| checklists/ (2 files) | 39 + 16 items | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/checklists/ | efficiency checklist 31 pass / 8 not pass; requirements checklist 16/16 |
| notes/ (12 evidence files) | ~40 KB | /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/ | Pre-change measurements, red-first evidence, quickstart runs, stall baseline, S7 trace |
| Analyze logs (4 rounds) | 20–27 KB each | /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze*.log | Gate reports: round 1 2 HIGH → rerun 1 HIGH → rerun 2 1 HIGH → rerun 3 READY 0/0/3/3 |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements + requirements checklist | 1915f903 (2026-10-20 00:31) | None |
| 2 | Shared-string citation tightening | 406e7fa3 (00:34) | Extra requirements commit before clarify |
| 3 | clarify: bind Feature 058 + five decisions | a7651c2a (00:40) | None |
| 4 | plan + design artifacts | 36aa5b0d (01:03) | None |
| 5 | Red-first / mutation plan | 5ab8a5e7 (01:07) | None |
| 6 | tasks: 52 rows | 09e1f104 (01:18) | None |
| 7 | checklist: 39 items, 31 pass / 8 not pass | ba2a18db (01:25) | Eight items deliberately left `[ ]` and routed to analyze |
| 8 | analyze round 1: 0 CRITICAL / 2 HIGH / 10 MEDIUM / 1 LOW, NOT READY | /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze.log | Gate loop required |
| 9 | requirements-repair → plan-repair → tasks-repair | 0c719b80 (01:37), f0c18e03 (01:44), 378acaca (01:53) | One bounded repair round used |
| 10 | analyze rerun: 0 CRITICAL / 1 HIGH / 4 MEDIUM / 2 LOW, NOT READY | /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze-rerun.log | **Second HIGH** — one-loop limit reached |
| 11 | User authorizes a second targeted repair round | /tmp/sdd-loop-efficiency/state.md, "user decision (2026-10-20)" | Explicit override of the one-loop limit; recorded |
| 12 | requirements-repair-2 + plan-repair-2 (which **adds** CLI capability profiles to 063) | 864940de (10:37), bcf27c77 (11:19) | Scope churn introduced here |
| 13 | Merge master (064 + monitor hotfix + setup) | 53162f4f | Cross-feature merge into an in-flight feature |
| 14 | tasks-repair-2 (CLI-profile scope removed and delegated to 064) + count correction | 144093c8 (18:33), 300e25ec (18:34) | Rework caused by step 12 |
| 15 | analyze rerun 2: 0 CRITICAL / 1 HIGH / 6 MEDIUM / 3 LOW, NOT READY | /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze-rerun-2.log | U-01R carried over |
| 16 | tasks-repair-3: T000 fixture author; close U-01R; 53 rows | a2279cc5 (18:50) | Third tasks repair |
| 17 | N-08 baseline correction (ba2a18db → a1aac7e5) | ed96d5c8 (19:04) | Correction before first behavior-face commit |
| 18 | analyze rerun 3: READY (0 CRITICAL / 0 HIGH / 3 MEDIUM / 3 LOW) | /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze-rerun-3.log | None |
| 19 | implement attempt 1 stopped after a suspected hang; runner exit 143, sentinel 0 | /tmp/sdd-loop-efficiency/status-sdd-loop-efficiency-implement: `exit=143 at=1792496664 sentinel=0` | User-initiated restart; worktree and commits preserved |
| 20 | implement-retry-1: foundation → US1 → US2 → US3 → US4 → US5 | 8a08b70a, 3ad6367d, 1b4e2721, b0e77437, b5994ccd, 8d6413a3, afca82f7 | Story-grouped commits; one full-suite baseline only |
| 21 | Verification declared green; review begins | afca82f7; verification.md `DoD Status: green`; closure slot still driver-owned | **Closure full suite has not run at review time** (see F2) |
| 22 | Review (this report) | — | Targeted tests only; no full suite (FR-012) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 8 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 4 |
| Workflow | 4 |
| Documentation | 3 |

## 3. Findings (Problems & Improvement Targets)

### F1 — Test-budget audit silently removes missing stages from the completeness denominator

- **Severity**: P0 (independently validated: confirm)
- **Category**: Automation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-test-budget.py:347-350; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/unit/test_audit_test_budget.py:433-443; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/requirements.md:187,270; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:350
- **Evidence** (verbatim quote):

  ```
  for stage in E3_STAGES:
      rows = evidence.get(stage)
      if rows is None:
          continue
  ```
  (audit-test-budget.py:347-350; `load_evidence` returns `{}` when `test-evidence/` is absent at lines 281-283)

  ```
  assert _stages(completed) == (2, 2)
  ```
  (test_stages_complete_summary, test_audit_test_budget.py:443 — only plan and analyze evidence files exist; the five applicable stages are clarify, plan, tasks, analyze, review)

  ```
  **SC-005**: ... 完整性分母 = 全部适用阶段数（含文档型阶段），整阶段缺失证据记录的阶段计入分母并判未完整，MUST NOT 静默缩小分母；收口审计 MUST 输出 `stages=N complete=N`
  ```
  (requirements.md:270; FR-012 at line 187 says `整阶段没有任何证据记录 MUST 判证据不完整，MUST NOT 从完整性分母中消失。`)

  Reproduction (read-only; temp dir removed):
  ```
  slots=baseline:1 closure:1 reruns=0 exceptions=0 unknown=0 environment_failures=0
  stages=1 complete=1
  status=ok
  exit=0
  ```
  With only `analyze.jsonl` present, five applicable stages collapse to one; with the real 063 spec dir (only `implement.jsonl`, and `implement` is not in `E3_STAGES`), verification.md:106/111 records `stages=0 complete=0` and `status=ok`.

- **Why it's a problem**: The audit is the feature's only closure gate for stage-evidence completeness, and it cannot go red when an evidence file is wholly absent. It reports `status=ok` and a shrunken denominator, so an incomplete run is indistinguishable from a complete one. The unit test codifies the wrong expectation `(2, 2)` instead of the spec's `(5, 2)` (or the applicable-stage count), so the defect is protected by the test suite. N-03R's closure and the SC-005 "pass" claim are therefore not real.
- **Proposed fix**: In `check_stages`, iterate every `E3_STAGES` entry; require either a readable evidence file or an authorized `not-applicable-skipped-stage` row; count a missing/empty file in the denominator and emit `unknown` + a violation (exit 1). Change `test_stages_complete_summary` to expect the full applicable-stage denominator and add `test_missing_stage_evidence_fails` (delete one stage file and assert exit 1). Update `test_valid_two_slot_ledger` so a missing evidence directory cannot pass. Record the corrected behavior in `references/efficiency-model.md` §2.4 and re-run the closure audit.

### F2 — SC-003/SC-012 are marked `pass` before the driver-owned closure full suite has run

- **Severity**: P1
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:336-340,348,357; /tmp/sdd-loop-efficiency/state.md (test-budget fence contains only `seq=1, slot=baseline`)
- **Evidence** (verbatim quote):

  ```
  **GATE-8 closure visibility**: the real spine's closure check fails until the
  driver appends the closure row (`closure check requires exactly 1 closure slot,
  found 0`) — this is the intended guard.
  ```
  (verification.md:336-338)

  ```
  | SC-003 | pass (automated + driver closure) | ledger audit two slots, exceptions visible; closure slot is driver-owned |
  ...
  | SC-012 | pass (automated) | 74 contract tests green (C-3/C-4 intentional); mirror pair 0 drift + zero NEW drift; name-level new failures empty |
  ```
  (verification.md:348,357)

  The only E2 row in /tmp/sdd-loop-efficiency/state.md is `{"seq":1,"slot":"baseline",...}`; no `closure` row exists, and no `final-failed.txt` exists under /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/.

- **Why it's a problem**: SC-012's "name-level new failures empty" is the result of the closure `comm -13` comparison, which has not run. GATE-8 itself says the closure check fails until the driver appends the row. Marking these criteria `pass` at review time is a false green: a regression introduced between the implement-start baseline and the final tree would be invisible to the reader.
- **Proposed fix**: Change SC-003 and SC-012 to `pending (driver closure)` in verification.md until the closure E2 row and `comm -13` output exist; add a verification rule (in the implement/review command prompt or a validator) that any SC whose evidence class includes "driver closure" cannot be `pass` before the closure artifact is present. The closure must be recorded before merge.

### F3 — SC-010's `next_stage_dispatched` is a constant, not an observed decision

- **Severity**: P1
- **Category**: Automation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py:225-229,299-310,436; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/requirements.md:222; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:355
- **Evidence** (verbatim quote):

  ```
  dispatch_path = os.path.join(state_dir, "dispatch.log")
  ...
  write_text(dispatch_path, "")
  ...
  "next_stage_dispatched": "yes" if "next_stage=" in dispatch_text else "no",
  ```
  (driver-stall-fixture.py:225-310; no `append_text(dispatch_path, ...)` exists anywhere in the file, so `dispatch_text` is always empty and the field is always `"no"`)
  ```
  if scenario["next_stage_dispatched"] != "no":
      failures.append("fake-done: next stage dispatched")
  ```
  (self-test, line 436 — only the negative value is ever exercised)

- **Why it's a problem**: FR-038 requires the fixture to observe "是否派发下一阶段" as one of the seven driver-side fields. A field that can only be `"no"` cannot detect a regression that dispatches the next stage; the mutation drill ("transcribed field → `DIFF: spine_stall_state`") does not cover this field. The plan-repair record claims U-01R fixed a "驱动侧字段同义反复", yet this field is itself tautological.
- **Proposed fix**: Add a dispatch branch to the fixture's documented U4/U5 program that writes `next_stage=<stage>` to `dispatch.log` (e.g., a fourth scenario or a positive control), assert both `yes` and `no` in `--self-test`, and add a mutation that flips the dispatch decision so the replay comparison fails. Alternatively, remove the field from the seven-field claim and state explicitly that the fixture never exercises dispatch.

### F4 — The feature's own run produced no E3 stage evidence for any intermediate stage

- **Severity**: P1
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/test-evidence/; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-test-budget.py:33 (`E3_STAGES` excludes `implement`); /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:106-114,350
- **Evidence** (verbatim quote):

  ```
  $ ls .specify/specs/063-sdd-loop-efficiency/test-evidence/
  implement.jsonl
  ```
  (the only file; `implement` is not in `E3_STAGES = ("clarify", "plan", "tasks", "checklist", "analyze", "review")`)

  ```
  ... `stages=0 complete=0`
  ```
  (verification.md:111 — recorded as the live spine audit result)

  ```
  | SC-005 | pass (automated) | audit tests: `stages=N complete=N`, docs-only reduced fields, skipped stage excluded, unknown reported |
  ```
  (verification.md:350)

- **Why it's a problem**: FR-012 requires every applicable intermediate stage (and review) to leave a uniquely decidable evidence row (`ran` / `not-run-docs-only` / `empty-selection-escalated`, or the authorized skip). The feature's own run left none; the audit's F1 denominator bug reported `stages=0 complete=0 status=ok`; and SC-005 was declared pass. This is a self-application failure: the feature did not apply its own evidence discipline to its own lifecycle.
- **Proposed fix**: Require the driver to write an E3 `stage-status` row for every applicable stage of its own run (docs-only stages use the reduced field set), then re-run the closure audit with the corrected F1 denominator. Add this obligation to `references/stage-prompts.md` and the driver's U4/U5 checklist; the closure gate must fail if the rows are absent.

### F5 — L-02 pointer correction is incomplete

- **Severity**: P2
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/requirements.md:338; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/research.md:18,87; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/checklists/efficiency.md:158; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/checklists/requirements.md:41
- **Evidence** (verbatim quote):

  ```
  - Q: 063 在 plan-repair-2 临时加入的 CLI 能力档案条款如何处置？ → A: 按 Feature 064 的 `notes/063-overlap-adjudication.md` 逐条裁决迁入 064 ...
  ```
  (requirements.md:338)

  ```
  | B-8 | CLI 能力档案与 probe 注册现状 | 由 Feature 064 记录并拥有（... `notes/063-overlap-adjudication.md`）...
  ```
  (research.md:18; line 87 has the same bare pointer)
  ```
  - 2026-10-20 tasks-repair-2：063 的临时 CLI-profile 范围已按 Feature 064 的 `notes/063-overlap-adjudication.md` 迁出 ...
  ```
  (checklists/efficiency.md:158; checklists/requirements.md:41 has the same form)

- **Why it's a problem**: `notes/063-overlap-adjudication.md` does not resolve from the 063 spec directory; the file lives under `.specify/specs/064-subagent-concurrency/notes/`. Analyze L-02 marked this PARTIAL and asked for a requirements/research/checklist-owned correction. The state spine's Line Notes claims "requirements.md pointers corrected", but the Clarifications row and both research/checklist pointers still carry the bare form.
- **Proposed fix**: Complete the L-02 correction in every file in one pass, using `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`; add a grep guard that `notes/063-overlap-adjudication.md` never appears without the `.specify/specs/064-subagent-concurrency/` prefix.

### F6 — Watcher self-test is flaky; GATE-2/DoD-5 claim a deterministic 33/0

- **Severity**: P2
- **Category**: Automation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/watch-target.sh (grace-timeout self-test); /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:328; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/tasks.md:23 (DoD-5)
- **Evidence** (verbatim quote):

  ```
  SELF-TEST: 32 passed, 2 failed
  FAIL grace-timeout — exit 10 != 14; output: WATCH ... verdict=RUNNING ... elapsed=0 ...
  FAIL grace-timeout-reason — grace expiry reason missing: WATCH ... verdict=RUNNING ...
  ```
  (one of six consecutive `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` runs; the other five printed `SELF-TEST: 33 passed, 0 failed`)
  ```
  | GATE-2 watcher self-test | `33 passed, 0 failed` (28 historical + 4 stream cases + progress sub-check) |
  ```
  (verification.md:328)

- **Why it's a problem**: A gate that intermittently fails its own self-test cannot serve as reproducible evidence; the recorded green is not deterministic. The failure is a timing race (the watcher returns RUNNING with `elapsed=0` before the fixture pid/status state is ready), not a product regression, but it makes DoD-5/GATE-2 unreliable.
- **Proposed fix**: Make the `grace-timeout` case wait for the pid file (and, where applicable, the status file) before starting the deadline clock; repeat the self-test N times in the verification run and report the flake rate rather than a single green.

### F7 — SC-010 baseline evidence pointers are dangling after recording

- **Severity**: P2
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline.json:18,32,46; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py:357-370
- **Evidence** (verbatim quote):

  ```
  "evidence_ptr": "/var/folders/d1/243gzhtd0pvdfsg1jl8jfcjm0000gn/T/stall-fixture-pnmw7bbp/timeout-run/timeout/spine.md"
  ```
  (stall-behavior-baseline.json:18; the sibling pointers at lines 32 and 46 have the same prefix; `ls` of that directory returns `No such file or directory`)
  ```
  finally:
      shutil.rmtree(root_dir, ignore_errors=True)
  ```
  (driver-stall-fixture.py:369-370 — the recording root is deleted at the end of `record()`)

- **Why it's a problem**: The baseline's per-scenario `evidence_ptr` is supposed to let a reviewer locate the observed spine/status/watcher output. The temp root is deleted, so the pointer cannot be resolved; the replay artifact also normalizes the pointer to the basename `spine.md`. The tuple is reproducible only by re-running the fixture, not from the recorded baseline alone.
- **Proposed fix**: Before `rmtree`, copy each scenario's spine/status/watcher output into a durable location under the feature notes (e.g., `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/stall-evidence/<scenario>/`) and write those paths into the baseline; keep the replay normalization but compare the durable relative paths.

### F8 — Security-invariant clauses are pinned by substring presence, not behavior

- **Severity**: P2
- **Category**: Automation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_sdd_loop_driver_efficiency.py:572-588 (DI-01/DI-02)
- **Evidence** (verbatim quote):

  ```
  def test_di_01_confirmation_gates_unchanged():
      skill = _text(SKILL_MD)
      assert "push" in skill
      assert "确认门" in skill or "确认" in skill
      docs = _text(DOCS_PAGE)
      assert "确认门" in docs or "确认" in docs
  ```
  (lines 572-577; DI-02 at 583-588 likewise only checks that `独立校验` and the sentence `校验者不是该阶段的执行子代理` appear)

- **Why it's a problem**: A regression that adds an automatic push or an approval bypass would still pass these tests as long as the existing prose remains. The repo's confirmation-gate sweep (`tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`) is already among the 68 pre-existing baseline failures, so no independent behavioral guard is green at review time. The actual run did not push, but the invariant test cannot prove that for the next change.
- **Proposed fix**: Replace DI-01/DI-02 substring checks with behavioral checks: scan the driver/skill/scripts for new `git push`/auto-approval paths, assert the destructive-action inventory is unchanged, and run the repo's `scan-confirmation-gates.py` (or the existing sweep) as part of the gate. Pin the destructive list in one owner document rather than in the test prose.

### F9 — Hand-maintained counts drifted repeatedly across artifacts

- **Severity**: P2
- **Category**: Documentation
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/plan.md:70; tasks.md:30; checklists/efficiency.md:15; /tmp/sdd-loop-efficiency/log-sdd-loop-efficiency-analyze-rerun-3.log (L-01/F-01)
- **Evidence** (verbatim quote):

  ```
  | L-01 | **RESOLVED** | plan.md:41 Constitution IV 证据已为「50 个契约条款」；无活动 49 计数（:327 为 dated repair record）。 |
  | F-01 | MEDIUM | 058 详情缺 063 checklist 阶段记录；tasks 记录 52 vs 当前 53。T050/DoD-10 路由。 |
  ```
  (analyze-rerun-3 log, lines 61 and 19; the same round fixed `49→50` clauses and `52→53` tasks)
  ```
  - **计数口径**：准入只使用 FR-003(a) 的窄模式 ... 当前 requirements 为 43 条 FR 定义行（tasks-repair-2 收口 CLI-profile 条款后复算）...
  ```
  (plan.md:70; tasks.md:15 and checklists/efficiency.md:15 restate the same counts)

- **Why it's a problem**: The feature went through at least three count corrections (FR 49→43, SC 16→13, tasks 52→53, clauses 49→50, requirements line counts 313→343→348) because counts are copied into plan/tasks/checklists/feature docs by hand. Each repair round fixes one copy and leaves another; the One Source of Truth principle is violated in content shape, not just pointer shape.
- **Proposed fix**: Generate a single machine-derived counts block (FR/SC/tasks/clauses/deliverables/E-rules) from `validate-requirements.py` / `validate-tasks.py` and reference it from plan/tasks/checklists; make the validators fail on any hand-written count that disagrees. Add the count block to the feature template so downstream features do not re-derive it.

### F10 — CLI-profile scope was added after plan/tasks and removed after the merge

- **Severity**: P2
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/plan.md:241,286; commits bcf27c77, 144093c8, 53162f4f
- **Evidence** (verbatim quote):

  ```
  **CLI Capability Profiles（已迁出）**：plan-repair-2 的临时 CLI-profile 增量已由 tasks-repair-2 按 064 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` 迁入 064（`contracts/cli-profiles.md` CLP-01…CLP-17）。本规格不再保留档案、契约、观测、Probe Object 或测试条款；064 是唯一 owner。
  ```
  (plan.md:286; the trigger at line 241 says the increment was added in plan-repair-2 and removed in tasks-repair-2)

- **Why it's a problem**: The 063/064 ownership overlap was discovered only after plan-repair-2, producing an extra requirements/plan/tasks repair cycle and a merge (53162f4f) into an in-flight feature. The final state is clean (one owner, no duplicate contract/test/Object), but the sequencing cost is visible in the commit history and the four analyze rounds.
- **Proposed fix**: Add a cross-feature ownership check at requirements/plan time that scans active specs for the same owner terms (CLI profiles, probe objects, shared contracts) and records the adjudication before tasks. Reuse `check-063-overlap.py` earlier in the lifecycle (it already supports `--strict-premerge`) rather than only at merge time.

### F11 — Compiled wrap-up calls omit `--run-id`, causing retries and missing run records

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: /tmp/sdd-loop-efficiency/state.md:56-58 (framework observations); /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/python/run-determination.py; compiled `## Wrap-up` faces in the command templates
- **Evidence** (verbatim quote):

  ```
  - `/speckit.clarify` wrap-up: `run-determination.py` call was missing required `--run-id`; first call exit 2, corrected in place with an explicit run-id. Framework position: clarify command template / wrap-up compiled face. Impact: one retry per clarify run.
  - `/speckit.tasks` wrap-up: the dispatch prompt had no run-id, so no run-determination record was produced; the compiled wrap-up requires `--run-id`. Framework position: compiled wrap-up call line / stage prompt contract. Impact: missing run-determination evidence for that stage.
  - `/speckit.analyze` wrap-up: same missing `--run-id` issue; the subagent reported it as a non-blocking ANOMALY and skipped run-determination/exec-quant/feedback bookkeeping rather than inventing an id. Framework position: analyze command template / compiled wrap-up. Impact: missing local run records for analyze.
  ```
  (state spine, framework_observations)

- **Why it's a problem**: Three stages in this one run either retried or silently lost their run-determination records because the compiled wrap-up call line did not carry the required argument. This is a framework-level friction that every feature pays; the stage subagent's decision to skip rather than invent an id was correct but leaves holes in the run history.
- **Proposed fix**: Add `--run-id` to the compiled wrap-up call lines for clarify/tasks/analyze (and any sibling command), or make `run-determination.py` derive a deterministic default when the flag is absent. Add a contract test that every compiled wrap-up face includes the required arguments, so `compile-embeds --check` fails on the drift.

### F12 — End-to-end fast-lane evidence is a hand-recorded trace, not a live driver run

- **Severity**: P2
- **Category**: Workflow
- **Location**: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/s7-dry-run-trace.md:3-6; /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/verification.md:347 (SC-002 evidence class)
- **Evidence** (verbatim quote):

  ```
  This is a recorded decision trace, not a nested driver launch
  (the skill's Hard Requirement 6 forbids nested driving). The deterministic
  components were actually executed; the LLM-orchestrated stage sequence is the
  documented decision path. The trace is non-CI evidence.
  ```
  (s7-dry-run-trace.md:3-6)

- **Why it's a problem**: The feature's core throughput claim — skip checklist, keep analyze/review, keep the closure slot — is exercised end to end only by a hand-written decision table. The deterministic scripts and contracts are well tested, but no real driver run has executed the sequence, so a wiring error in the prompt-level orchestration would not be caught. The verification labels the evidence class honestly, which keeps this from being a false green.
- **Proposed fix**: Add a stub-stage dry-run harness that replays the driver's dispatch decisions (stage order, skip marker, E1/E2 writes) without invoking an LLM, and assert the sequence in CI; keep the recorded trace as supplemental evidence. If a live pilot is required, record it as a dated acceptance run before claiming the throughput optimization works in production.

## 4. What Worked — Preserve (Brief)

- Story-grouped commits (`feat(063…): implement … (USn)`) make the process history attributable; every user story has its own commit and checkpoint.
- Red-first evidence records the command, real output, and exit status for every new script and the watcher extension (`notes/red-first-evidence.md`).
- Mutation drills are enumerated as 7 target groups / 24 applications with a named red test and a restore checksum for each; the PC-11 pin was strengthened after a mutation initially failed to turn red.
- The GATE-1 targeted set reproduces exactly: `144 passed in 123.64s` in this review, using `scripts/bash/run-tests.sh` (no `python3 -m pytest`).
- Mirror and generated-face evidence reproduces: `sync-mirrors.py --check --only skills/external/sdd-loop-driver` exits 0 with `ok (21 files)`; `diff -rq` exits 0; `probe-utils.py --action compile-embeds --check` reports `74 units, zero drift`.
- The 063/064 CLI-profile adjudication is clean in the final tree: 063 has no `contracts/cli-profiles.md`, no CP tests, and no second Probe Object; the 064 guard `test_clp_17_no_063_duplicate_owner` is green.
- The 68 pre-existing full-suite failures are disclosed, not waived; a sample (`test_confirmation_gates_sweep`, `test_clause_coverage`, `test_criterion_subject`, `test_agent_dispatch_mechanism`) reproduces and is attributed to mirror drift outside the owned pair.
- The plan constraint re-anchoring is recorded with four `rebaseline_events[]`; the N-08 correction (`ba2a18db` → parent of `9e69f3de`, `a1aac7e5`) is verified against git.
- The one-loop analyze limit was overridden by an explicit user decision, recorded in the state spine rather than silently ignored.
- No push occurred: `git branch -r --contains HEAD` is empty; confirmation gates were not bypassed during this run.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Command Prompt Improvements

- **REC-C1 — Carry `--run-id` in every compiled wrap-up** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/scripts/python/run-determination.py and the compiled `## Wrap-up` faces generated from the probe registry. Change: pass `--run-id` in the clarify/tasks/analyze wrap-up calls, or derive a deterministic default; add a compile-time contract assertion. Source: F11. Expected impact: no retry and no missing run record for every stage.
- **REC-C2 — Forbid `pass` before driver-owned closure evidence exists** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/implement.md (verification output discipline) and the review command's closing rules. Change: any SC whose evidence class includes "driver closure" must be `pending` until the closure E2 row and name-level diff exist; the review must not mark it pass. Source: F2. Expected impact: the closure safety net cannot be bypassed by a verification table.

### 5.2 Automation / Script Improvements

- **REC-A1 — Fix the completeness denominator** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/audit-test-budget.py. Change: iterate all `E3_STAGES`; missing/empty evidence → `unknown` + violation; denominator includes every applicable stage (excluding only authorized skips); update `tests/unit/test_audit_test_budget.py` expectations and add a missing-file test. Source: F1, F4. Expected impact: the audit can go red when a stage is missing; `stages=N complete=N` becomes meaningful.
- **REC-A2 — Make `next_stage_dispatched` observable** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py. Change: write `next_stage=` on the dispatch branch, test both values, add a reversal mutation; copy per-scenario evidence to a durable path before `rmtree`. Source: F3, F7. Expected impact: SC-010's seven-field observation is non-tautological and auditable from the artifact.
- **REC-A3 — Stabilize the watcher self-test** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/watch-target.sh. Change: wait for the pid/status fixture state before starting the grace clock; report a flake rate over N runs. Source: F6. Expected impact: GATE-2/DoD-5 becomes reproducible.
- **REC-A4 — Replace security-invariant substring checks with behavior checks** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/contract/test_sdd_loop_driver_efficiency.py. Change: scan for new push/auto-approval paths and run the confirmation-gate sweep; pin the destructive list in one owner. Source: F8. Expected impact: DI-01/DI-02 can fail when the invariant is actually broken.

### 5.3 Workflow Improvements

- **REC-W1 — Require E3 evidence for the feature's own run** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/stage-prompts.md and /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md. Change: the driver writes a `stage-status` row for every applicable stage of its own lifecycle (docs-only uses the reduced field set) before closure; the closure gate rejects a missing row. Source: F4, F1. Expected impact: self-application matches the feature's own requirement.
- **REC-W2 — Add a pre-plan cross-feature ownership check** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/scripts/check-063-overlap.py and /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/plan.md. Change: at requirements/plan time, scan active specs for shared owner terms and record the adjudication before tasks; use `check-063-overlap.py --strict-premerge` earlier. Source: F10. Expected impact: no late scope churn or merge rework.
- **REC-W3 — Generate counts from validators** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-requirements.py and /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/scripts/python/validate-tasks.py. Change: derive FR/SC/tasks/clauses/deliverables counts once and reference them; fail on hand-written drift. Source: F9. Expected impact: no more 49/50 or 52/53 repair rounds.
- **REC-W4 — Require a live or stub-driver end-to-end exercise** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/external/sdd-loop-driver/references/dispatch-recipes.md and /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/integration/test_sdd_loop_efficiency_runner.py. Change: add a stub-stage dispatch harness to CI; keep the recorded trace as supplemental. Source: F12. Expected impact: the orchestration wiring is exercised, not just documented.

### 5.4 Documentation Improvements

- **REC-D1 — Complete the L-02 pointer correction** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/requirements.md, /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/research.md, and /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/checklists/. Change: use `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md` everywhere; add a grep guard. Source: F5. Expected impact: every pointer resolves from the 063 spec directory.
- **REC-D2 — Make the stall baseline self-contained** — Target: /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/063-sdd-loop-efficiency/notes/stall-behavior-baseline.json and the fixture. Change: durable evidence copies plus relative pointers; replay compares them. Source: F7. Expected impact: the baseline can be audited without re-running the fixture.
- **REC-D3 — Mark pending closure explicitly** — Target: the verification template/section in /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/implement.md and the 063 verification.md. Change: add `pending (driver closure)` as a first-class status; never use `pass` with an absent artifact. Source: F2. Expected impact: readers cannot mistake a pending safety net for a green one.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Fix the completeness denominator and its tests | skills/external/sdd-loop-driver/scripts/audit-test-budget.py; tests/unit/test_audit_test_budget.py | F1 |
| P1 | Forbid `pass` before driver-owned closure evidence | templates/commands/implement.md; review closing rules; verification.md | F2 |
| P1 | Make SC-010's dispatch field observable and evidence durable | tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py | F3, F7 |
| P1 | Require E3 evidence for the feature's own run | skills/external/sdd-loop-driver/references/stage-prompts.md; driver U4/U5 | F4 |
| P2 | Complete L-02 pointers | .specify/specs/063-sdd-loop-efficiency/{requirements,research,checklists} | F5 |
| P2 | Stabilize the watcher self-test | skills/external/sdd-loop-driver/scripts/watch-target.sh | F6 |
| P2 | Replace DI substring checks with behavior checks | tests/contract/test_sdd_loop_driver_efficiency.py | F8 |
| P2 | Generate counts from validators | .specify/scripts/python/validate-*.py; plan/tasks/checklist templates | F9 |
| P2 | Add a pre-plan ownership check | skills/external/sdd-loop-driver/scripts/check-063-overlap.py; requirements/plan flow | F10 |
| P2 | Carry `--run-id` in compiled wrap-ups | .specify/scripts/python/run-determination.py; compiled wrap-up faces | F11 |
| P2 | Add a stub-driver end-to-end harness | tests/integration; skills/external/sdd-loop-driver/references/dispatch-recipes.md | F12 |

## 7. Self-Containment Check

- [x] Every file path in the report is absolute. (The commit is unpushed, so absolute paths and `git show afca82f7` recovery are used; §0 records the reachability result.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No unresolved template placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **one P0 finding (F1) was raised and independently validated as `confirm` by a fresh-context read-only subagent that received only the finding, location, and quoted evidence; no validator was drawn from the detection pass.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
