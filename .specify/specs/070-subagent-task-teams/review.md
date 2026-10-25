# Specification-Driven Development (SDD) Process Review Report: 070-subagent-task-teams

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. Sections that would describe the feature instead of a process gap are reduced to the evidence needed to judge a finding.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 070 |
| Requirement Key | `070-subagent-task-teams` |
| Requirement Name | Task Decomposition & Team Coordination for Subagent-Driven SDD（驱动子代理的任务拆解与配合机制） |
| Related Feature | Feature 070 — same name; registry status `Planned`; `.specify/memory/features.md` row 070; detail `.specify/memory/features/070.md` |
| Repository | `spec-kit` (distributed as `specify-cli`; `pyproject.toml` version `0.0.22`) |
| Repository URL | `origin` = `git@github.com:github/spec-kit.git` (upstream); work remotes: `github`/`gitee` = `cloud-native-ai/spec-kit`, `gitlab` = `gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty; the commit is unpushed. All commit-anchored citations below use absolute paths plus `git show <sha>:<path>` recovery instructions, never a web URL. |
| Branch | `070-subagent-task-teams` |
| Commit SHA | `6d434b424db073b503cf6498020b3c2cac7fe8ef` (short `6d434b42`) |
| Repo Root (absolute) | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams` |
| Review Date | 2026-10-25 |
| Reviewer (Agent) | Qoder agent running `review-sdd-process` (`/speckit.review`) |
| Environment | Linux `5.10.134-15.2.al8.x86_64` x86_64; Bash; Python `3.11.11`; pytest `8.4.2`; git worktree |
| spec-kit Source Snapshot | This worktree at `6d434b42` (unpushed); CLI version `0.0.22` |
| Plan constraint | `plan_constraint=active` since 2026-10-24T15:55Z; `plan_commit=bad4ae1f`; recorded `approved_baseline_commit=bad4ae1f` (see F1 for the unrecorded re-baseline) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|------------------|
| requirements.md | 319 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/requirements.md` | 30 FR / 8 SC / 5 user stories, ownership table, A1–A12, edge cases |
| plan.md | 322 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/plan.md` | 16-principle Constitution Check, delivery surface, mirror owner, 35-step budget, R-01…R-15 |
| tasks.md | 419 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/tasks.md` | 39 task rows T001–T039, 8 phases, coverage map, clause partition, DoD/GATE |
| verification.md | 219 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/verification.md` | Segment verification, interpretations, T039 closure checks, SC-001…SC-008 matrix |
| checklists/quality.md | 339 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/checklists/quality.md` | 40 requirements-quality items, 7 PASS / 33 FAIL |
| data-model.md | 419 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/data-model.md` | E1–E13 entities, 91 validation rules, E13 required-output inventory owner |
| contracts/ | 7 files | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/contracts/` | 110 domain-prefixed clauses (WP/WG/SD/VI/ST/OR/FN) |
| research.md | 203 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/research.md` | R1–R20 decisions + DR1–DR12 refinements |
| quickstart.md | 130 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/quickstart.md` | Scenarios A–G with premises and execution-status notes |
| feature-ref.md | 117 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/feature-ref.md` | Feature binding, FR/SC coverage, overlap adjudication, pointer to mirror owner |
| notes/clarify-decisions.md | 544 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/clarify-decisions.md` | D1–D9 decision record |
| notes/red-first-evidence.md | 590 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/red-first-evidence.md` | Per-row red runs, disclosed false greens, mutation drills |
| notes/quickstart-run.md | 213 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/quickstart-run.md` | Scenarios A–G commands, real outputs, teardown |
| notes/benchmark-070.md | 68 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/benchmark-070.md` | `not_evaluated` benchmark record and closure consequence |
| notes/analyze-repair.md | 134 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/analyze-repair.md` | 10 substantive PLAN-EDIT declarations, blocking repairs, MEDIUM/LOW dispositions |
| test-evidence/analyze-report.md | 369 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-report.md` | Round-1 analyze: 1 CRITICAL / 7 HIGH / 22 MEDIUM / 4 LOW, validation, checklist accountability |
| test-evidence/analyze-rerun-report.md | 212 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md` | Round-2 analyze: READY, 0 C / 0 H, R2-01…R2-06; **untracked** (F2) |
| test-evidence/implement-stage-status.jsonl | 10 rows | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/implement-stage-status.jsonl` | E3 targeted test-budget rows through `impl-s6-optout-fallback`; no S7 row (F3) |
| test-evidence/final-070-suite.txt | 8 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/final-070-suite.txt` | 328 passed, rc 0 |
| test-evidence/final-clause-coverage.txt | 3 | `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/final-clause-coverage.txt` | `checked=110 missing=0` (id-presence check; F4) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements | `e42d620d` 2026-10-24T23:25:29+08:00; validator rc 0, 30 FR / 8 SC | None; Feature-binding timing deviation A7 and scaffolding deviation A8 disclosed |
| 2 | clarify | `cb0cbf76` 2026-10-24T23:35:42+08:00; nine decisions D1–D9; 30 FR unchanged | None |
| 3 | plan; constraint activation | `bad4ae1f` 2026-10-24T23:52:41+08:00 + `dd7a71fe` 23:53:46; `plan_constraint=active` at 15:55Z; `approved_baseline_commit=bad4ae1f` | None; overlap rc 1 adjudicated (Groups A–C), not a new relation |
| 4 | tasks | `5749531e` 2026-10-25T00:04:34+08:00; 39 rows; validators 0/0 | None |
| 5 | tasks-repair (post-plan) | `9b964d5c` 2026-10-25T00:07:10+08:00; `requirements.md` `4 ++--`, `data-model.md` `2 +-`; data-model declared `PLAN-EDIT ... 分类=minor` | **Yes** — a `requirements.md` change after plan activation; no E4 `rebaseline_events[]` is recorded (§3.6 obligation; F1) |
| 6 | checklist | `d348204b` 2026-10-25T00:23:08+08:00; 40 items, 7 PASS / 33 FAIL, two fresh-context detectors | None; FAILs are analyze inputs by design |
| 7 | analyze (round 1) | 2026-10-25T00:37+08:00; report 369 lines; verdict NOT READY, 1 CRITICAL + 7 HIGH; read-only, no commit | The report was left uncommitted until the next stage (same pattern as F2) |
| 8 | analyze-repair | `0df504b9` 2026-10-25T00:50:30+08:00; 10 plan-owned files + `requirements.md` `28 +-` + `tasks.md` `46 +--`; 10 `PLAN-EDIT ... 分类=substantive` | **Yes** — semantic FR/SC/contract changes were self-authorized under 063 branch (a), while §3.5 reserves branch (a) for changes that do **not** alter FR/SC/contract semantics; no branch-(b) user escalation and no E4 re-baseline (F1) |
| 9 | analyze-rerun (round 2) | 2026-10-25T01:01+08:00; report 212 lines; verdict READY, 0 C / 0 H; prompt says "read-only: … do not commit" | **Yes** — the READY evidence is untracked in `git status` and never committed (F2) |
| 10 | implement baseline (E2) | 2026-10-24T17:08:31Z; `bash scripts/bash/run-tests.sh --names-out …/baseline-failed.txt` → 19 failed / 5341 passed; E2 row in spine | None; exactly one full-suite slot |
| 11 | implement s1–s5 | `62d979b1` … `661377a3` (2026-10-25T01:11–02:02+08:00); red-first rows T005–T030; targeted sets only | None; plan-owned files untouched in these segments |
| 12 | implement s6 | `34bb4e57` … `94c5fccd` (2026-10-25T15:34–15:43+08:00); T031–T035; 324-test targeted audit; pre-T037 mirror drift disclosed | None; mirror drift resolved in s7 |
| 13 | implement s7 | `e83f510f` … `6d434b42` (2026-10-25T15:49–15:59+08:00); T036–T039; 328 passed; quickstart A–G; benchmark `not_evaluated`; closure blocked | **Yes** — the S7 E3 stage-status row is absent from `implement-stage-status.jsonl`; the closure full-suite slot is deferred to the driver (F3; the deferral itself is by design) |
| 14 | review (this run) | 2026-10-25T09:41Z; targeted 328 + 25 + 65 passed; mirror ok 32 files; validators 0/0 | None; review-only, no artifact edits, no push |

**Commit discipline**: the implementation history is stage/segment-grouped and task-attributable through the spine and task markers; the timeline claims above come from commit timestamps plus the appended spine, not from file mtimes.

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix before merge or record an explicit waiver. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 2 |
| Documentation | 1 |

## 3. Findings (Problems & Improvement Targets)

### F1 — The analyze-repair self-authorized a semantic plan revision under the wrong 063 branch, and no re-baseline was recorded

- **Severity**: P1 (merge-blocking until ratified/fixed)
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/skills/external/sdd-loop-driver/references/efficiency-model.md` §3.5–§3.6 (lines 185–204); `/home/agent/sdd-070/prompt-070-analyze-repair.md` §2 (lines 12–14); `/home/agent/sdd-070/spine-070.md` lines 91 and 115; `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/notes/analyze-repair.md` lines 9–24 and 37–72.
- **Evidence** (verbatim quotes):

  ```text
  # efficiency-model.md §3.5 (a)
  - **(a) 修复既有缺陷所必需**，且不改变已批准的需求范围/FR/SC 语义、架构方向、数据模型语义、契约语义或任务分解范围 → 驱动派发一次完整 plan 重审并记录触发与证据；重审通过后对门失败阶段做一次 U4 复验。
  # efficiency-model.md §3.5 (b)
  - **(b) 改变上述任一项、引入新能力/安全面，或驱动无法确定** → 作为决策以四要素上送（发现了什么 / 为何吃重 / 中间产物逐项可定位 / 可选处置），MUST NOT 自行重审。
  # efficiency-model.md §3.6
  plan 约束激活后，任何门内完成的 `requirements.md` 变更（含 analyze 路由修复、clarify 写回与显式范围修订）MUST 在下一个依赖该基线的 U4 分类之前触发 re-baseline：
  1. 在 E4 追加一条 `rebaseline_events[]`：触发、时间、前一基线提交、新基线提交（= 包含该变更的提交）、FR/SC 定义集合与语义差异摘要；
  2. 把 `approved_baseline_commit` 更新为新基线（此后一律使用**最新**锚点）；
  ```

  ```text
  # prompt-070-analyze-repair.md §2
  This repair is mandated by the analyze gate. The plan-owned changes below are authorized as a **plan revision** under the 063 plan-constraint branch (a): the analyze-repair plus the re-run analyze serve as the plan re-review.
  ```

  ```text
  # spine-070.md:91 (analyze-repair)
  - plan_revision: authorized under the 063 plan-constraint branch (a); findings repaired = C-01, I-02, A-01, A-02, A-03, G-01, A-15, A-18 (1 CRITICAL + 7 HIGH); ... the re-run analyze is the plan re-review
  # spine-070.md:115 (analyze-rerun)
  - plan_revision: 10 PLAN-EDIT lines present and every plan-owned file declared; ... this rerun is the plan re-review
  ```

  ```text
  # notes/analyze-repair.md — the repairs are semantic, not typo-level
  SC-005 now uses the four values ... and names the **plan fence** as the canonical decision record
  SC-001 now uses the A5/OR-13 conservative anchor ... the exact FR-022/OR-04 interval ...
  SC-002 states the comparator explicitly ...
  SC-006 ... The denominator is **per session** ...
  FR-013 ... children **inherit the parent's attempt count** ...
  FR-023 now defines the consequence: an all-`not_evaluated` benchmark blocks closure ...
  ```

  ```text
  # The review brief's active constraint still records the old baseline
  (plan_commit=bad4ae1f; approved_baseline_commit=bad4ae1f)
  ```

  ```text
  # git facts
  $ git log --oneline bad4ae1f..HEAD -- .specify/specs/070-subagent-task-teams/requirements.md
  0df504b9 docs(070-subagent-task-teams): repair analyze critical/high findings
  9b964d5c docs(070-subagent-task-teams): fix count-claim wording in requirements and data-model
  $ git show --stat 0df504b9
  ... requirements.md | 28 +- ... plan.md | 26 +- ... contracts/... (6 files) ... data-model.md | 38 +- ...
  # grep for a 070 rebaseline event returns nothing (the only rebaseline_events hit is another feature's evidence)
  ```

- **Why it's a problem**: the repaired changes alter FR/SC semantics (SC-001 basis, SC-002 numerator/comparator, SC-005 vocabulary, SC-006 denominator, FR-013 split-retry semantics, FR-023 closure rule), contract semantics, and the data model — the exact set that §3.5(b) reserves for a four-element user escalation. The driver instead self-authorized them as §3.5(a), self-ran the re-review, and never recorded a branch-(b) decision. Independently, §3.6 requires an E4 `rebaseline_events[]` for both post-plan `requirements.md` commits; no such event exists, and the recorded `approved_baseline_commit` is still `bad4ae1f`. The artifacts themselves were re-reviewed and are coherent; the problem is the authorization/record path, not the repaired content.
- **Proposed fix**: before closure, the driver MUST do one of two things: (i) obtain an explicit user ratification of the semantic plan revision as a branch-(b) decision (four elements: what was found, why it mattered, where each intermediate artifact is, the options taken), or (ii) record an explicit user waiver of the branch-(b) escalation with its reason. Then append E4 `rebaseline_events[]` for the `requirements.md` changes (`9b964d5c` and `0df504b9`; latest baseline `0df504b9`), update `approved_baseline_commit` to the latest baseline, run `audit-plan-changes.py --repo <repo> --base bad4ae1f --head 0df504b9 --plan-owned … --declarations <file>`, and record the disposition as `gate-fail-escalate` for the branch-(b) path (or `gate-fail-rereview` if the user confirms branch (a) with a waiver); for the branch-(a) path, also record the one U4 re-verification. No artifact content change is required if the user ratifies.

### F2 — The final analyze-rerun READY evidence is untracked and was left that way for every implement segment

- **Severity**: P1 (merge-blocking until fixed or waived)
- **Category**: Workflow
- **Location**: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md` (untracked); `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun.jsonl` (untracked); `/home/agent/sdd-070/prompt-070-analyze-rerun.md` §2; `/home/agent/sdd-070/spine-070.md` lines 139, 156, 176, 194, 211, 230, 247.
- **Evidence** (verbatim quotes):

  ```text
  # git status --short (review time)
  ?? .specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md
  ?? .specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun.jsonl
  # git log --all -- <both paths> is empty
  ```

  ```text
  # prompt-070-analyze-rerun.md
  - This stage is **read-only**: do not modify any artifact, do not write code, do not commit.
  ```

  ```text
  # spine-070.md:139 (repeated verbatim at :156, :176, :194, :211, :230, :247)
  - commit scope: Feature 070 artifacts only; the two pre-existing untracked analyze-rerun evidence files were left uncommitted; no push
  ```

  ```text
  # analyze-rerun-report.md (the gate verdict that authorized implementation)
  **READY — 0 CRITICAL / 0 HIGH.**
  ...
  **Mode**: strictly read-only. The only feature writes are this report and `test-evidence/analyze-rerun.jsonl`; ... no commit was made.
  ```

- **Why it's a problem**: the round-2 gate that converted NOT READY into READY — and therefore authorized all seven implement segments — exists only in the working tree. A clean checkout of `6d434b42` cannot reproduce or even read the authorization; the round-1 report was committed by the repair commit, so the same read-only-stage gap was closed once by accident and then reopened for the final, decisive gate. The implement spine repeats the exception in every segment instead of closing it.
- **Proposed fix**: commit `test-evidence/analyze-rerun-report.md` and `test-evidence/analyze-rerun.jsonl` with the closure evidence; add a driver step that commits every read-only gate verdict (report + E3 row) before dispatching the next stage; update the stage prompts so "read-only" means no artifact edits, not no evidence commit. Target: `skills/external/sdd-loop-driver/references/dispatch-recipes.md` (stage commit discipline) and the analyze/review stage prompt text.

### F3 — The S7 E3 stage-status row is absent from the test-budget ledger

- **Severity**: P2
- **Category**: Automation
- **Location**: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/implement-stage-status.jsonl`; `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/verification.md` § T036–T038 / § Closure verification; `/home/agent/sdd-070/spine-070.md` lines 234–249.
- **Evidence** (verbatim quotes):

  ```text
  # the last row of implement-stage-status.jsonl
  "substage": "impl-s6-optout-fallback"
  # the ten recorded substages
  impl-s1-foundational-gate, impl-s2-us1-plan-gate (x2), impl-s3-us2-coordination,
  impl-s4-us3-verification, impl-s5-us4-preset, impl-s5-us5-report,
  impl-s6-entry-surface, impl-s6-nonregression, impl-s6-optout-fallback
  ```

  ```text
  # spine-070.md:245 (impl-s7)
  - test budget: targeted only; no full suite; E2 slot remains T002. The closure full-suite slot ... is the driver's post-review slot and is recorded as deferred in `verification.md`.
  ```

- **Why it's a problem**: the E3 ledger does not cover T036–T039. The only record of the S7 test budget is the free-text spine entry plus `final-070-suite.txt`; a later budget audit (the `audit-test-budget.py` slot check named in `dispatch-recipes.md`) cannot tell from the ledger whether S7 ran a targeted set or an unauthorized full suite. The final logs do exist and are cited; this is a record-layout gap, not a product failure.
- **Proposed fix**: backfill an `impl-s7-closure` row from `final-070-suite.txt` and `final-clause-coverage.txt` (command, `selection_basis=targeted-set-v1: T039 closure audit`, selected paths, rc 0, 328 passed / 0 failed, `new_failures=0`, baseline = E2 19 failed / 5341 passed). Add a driver check that every implement segment writes exactly one E3 row before its U4. Target: `skills/external/sdd-loop-driver/references/efficiency-model.md` §2 / `dispatch-recipes.md` test-budget discipline.

### F4 — The 110-clause closure check is an id-presence grep, and the T039 repair satisfied it by adding ids to a docstring

- **Severity**: P2 (known deferred residual G-02; not a new design change)
- **Category**: Automation
- **Location**: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/tasks.md` line 328 (T039); `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/verification.md` lines 119, 125–133; `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md` lines 150 and 168.
- **Evidence** (verbatim quotes):

  ```text
  # tasks.md T039
  the 110-ID clause-inventory check (`for id in $(cat notes/contract-clause-inventory.txt); do grep -q "$id" tests/contract/test_sdd_loop_driver_wp_model.py ... || exit 1; done`)
  ```

  ```text
  # verification.md — T039 repair
  T039 added a clause-to-test mapping block to the
  `tests/contract/test_sdd_loop_driver_wp_gate.py` docstring (the same pattern
  used for WG-06…WG-13 at T011). No assertion, behaviour, or contract text
  changed. After the repair the loop reports `checked=110 missing=0`.
  ```

  ```text
  # analyze-rerun-report.md — carried residual
  T039's clause check is id-presence only (carried MEDIUM)
  the id-presence check remains a falsifiability weakness (carried MEDIUM)
  ```

- **Why it's a problem**: `grep -q "$id"` passes on a comment, a docstring, or an unrelated mention; it cannot detect that a clause has no behavioural pin. The T039 repair did exactly what the check cannot distinguish — it added the missing ids to a docstring, and the check went green. The underlying contract tests do contain behavioural assertions, so no product behaviour is wrong; the defect is that the closure evidence is weaker than the `checked=110 missing=0` line suggests, which is precisely the FR-030 "a green check that would not turn red" class.
- **Proposed fix**: replace the id-presence loop with a behaviour-level check: for each clause id, require a test that turns red when the pinned behaviour is mutated (the existing mutation-drill harness in `tests/contract/test_wp_mutation_drills.py` is the reusable pattern), or add a negative control per contract file that removes the clause's anchor and expects a failure. Keep the 110-id inventory as an index, not as the proof. Owner: the carried G-02 residual; this review does not reopen its design, only records that the current closure check is tautological.

### F5 — The checklist still reports 33 FAILs with no post-repair re-score or reconciliation header

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/checklists/quality.md` lines 17 and 331; `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/test-evidence/analyze-rerun-report.md` line 115.
- **Evidence** (verbatim quotes):

  ```text
  # checklists/quality.md
  - This is a judged checklist: **40 items — 7 PASS / 33 FAIL**. ...
  - **Checklist result**: 40 items — 7 PASS / 33 FAIL. FAILs are requirement-quality findings, not run anomalies.
  ```

  ```text
  # analyze-rerun-report.md
  `checklists/quality.md` remains **40 items — 7 PASS / 33 unchecked**. All 33 unchecked items were dispositioned in round 1: **30 raised-as-finding + 3 covered-by + 0 undispositioned**; ...
  The checklist is a point-in-time artifact dated 2026-10-25; this read-only stage did not re-score it. A later `/speckit.checklist` or implement-stage re-score would reflect the repaired text; the old FAIL verdicts in the checklist are dated observations, not current owners.
  ```

- **Why it's a problem**: the dispositions are complete and correct in the analyze reports, but the checklist file itself has no reconciliation marker. A maintainer opening the checklist sees 33 open FAILs and has to know to search the analyze reports for their status; a later re-score would silently change the denominator and could be mistaken for a new regression. The 7 PASS / 33 FAIL record should stay dated, but its current status must be visible where it is read.
- **Proposed fix**: after an analyze-repair round, either re-score the checklist (a new dated file or a new revision) or add a short reconciliation header naming each disposition class and the owner path, e.g. "33 FAILs → 7 resolved by analyze-repair, 23 deferred with owners in `notes/analyze-repair.md`, 3 covered by design clauses; this file is the round-1 observation, not the current status." Target: `templates/commands/checklist.md` (post-repair reconciliation rule) and the analyze-repair workflow.

## 4. What Worked — Preserve (Brief)

- **Single-owner discipline**: `plan.md` § Mirror Obligations and `data-model.md` E13 are the only complete owners; `feature-ref.md`, `research.md`, and the runtime doc are pointers; the T033 owner-agreement check turns the C-01 class red if a copy reappears.
- **`not_evaluated` discipline**: the benchmark records zero samples as `not_evaluated`, refuses to promote fixture timestamps, and blocks closure; no absolute wall-clock claim was made.
- **Red-first evidence**: real failing commands, disclosed false/accidental greens (T005, T016, T027), anti-drift passes separated from new-behaviour evidence, and four mutation drills with control halves that prove the mutant was executed.
- **Traceability**: 30/30 FR and 8/8 SC mapped, 39/39 task rows `[x]`, 110/110 clause ids partitioned, validators rc 0, and the two deterministic gates (`pre-analyze-check`, `decomposition-check`) re-run clean at review.
- **Invariant preservation**: no stage-command change, no second registry/ownership model/integration queue/ledger, no persisted team, no push; the mirror is generated and byte-identical; the SKILL pin update is intentional and commented.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Workflow Improvements

- **R1 — Enforce the 063 branch-(b) escalation for semantic plan revisions** — Target: `skills/external/sdd-loop-driver/references/efficiency-model.md` §3.5–§3.6 (absolute supplement: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/skills/external/sdd-loop-driver/references/efficiency-model.md`). Change: make the branch classifier check FR/SC/contract semantics before accepting branch (a); when a `requirements.md` or plan-owned edit changes a definition, SC basis, or contract clause, force branch (b) or a recorded user waiver; pair every accepted revision with an E4 `rebaseline_events[]` and a U4 re-verification record. Source: F1. Expected impact: semantic repairs stop being self-authorized and the approved baseline cannot silently go stale.
- **R2 — Commit read-only gate evidence before the next stage** — Target: `skills/external/sdd-loop-driver/references/dispatch-recipes.md` (stage commit discipline) and the analyze/review stage prompts (absolute supplement: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/skills/external/sdd-loop-driver/references/dispatch-recipes.md`). Change: after a read-only gate produces a verdict report and an E3 row, the driver commits both before dispatching the next stage; "read-only" continues to forbid artifact edits, not evidence commits. Source: F2. Expected impact: every gate that authorizes downstream work is reproducible from a clean checkout.

### 5.2 Automation / Script Improvements

- **R3 — Make the E3 row a per-segment invariant** — Target: `skills/external/sdd-loop-driver/references/efficiency-model.md` §2 (test budget) and the implement-stage prompt/records (absolute supplement: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/skills/external/sdd-loop-driver/references/efficiency-model.md`). Change: the driver's U4 verifies that the segment's E3 row exists (command, selection basis, selected paths, rc, pass/fail, new failures, baseline) before accepting the segment; backfill the missing `impl-s7` row. Source: F3. Expected impact: the test-budget ledger covers every segment, so a full-suite deviation is detectable from the ledger alone.
- **R4 — Replace the id-presence clause check with a falsifiable check** — Target: `.specify/specs/070-subagent-task-teams/tasks.md` T039 (feature instance) and `templates/commands/tasks.md` / `templates/commands/implement.md` (general rule) (absolute supplement: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/.specify/specs/070-subagent-task-teams/tasks.md`). Change: require each clause id to be attached to a test that goes red when the clause's behaviour is mutated, or add a negative control per contract file; keep the inventory as an index. Source: F4 / carried G-02. Expected impact: `checked=110 missing=0` becomes a behavioural claim rather than a string-presence claim.

### 5.3 Documentation Improvements

- **R5 — Reconcile the checklist after a repair round** — Target: `templates/commands/checklist.md` and the analyze-repair workflow (absolute supplement: `/tmp/sdd-worktrees/spec-kit/070-subagent-task-teams/templates/commands/checklist.md`). Change: add a post-repair re-score or a reconciliation header that names each disposition class and its owner path, while preserving the dated 33-FAIL record. Source: F5. Expected impact: readers see the current status of every FAIL where the checklist is read, without re-opening the design.

### 5.4 Open Decision (not a file change)

- **R6 — SC-001 / SC-002 closure decision** — The benchmark is `not_evaluated` (0 comparable samples; the Scenario E timestamps are synthetic fixture epochs). `not_evaluated` alone never satisfies SC-001 or SC-002 (FR-023). The user must either run a comparable benchmark (≥3 samples per measured stage, same host class and topology, FR-022 first-dispatch-to-U4 interval) or record the exact waiver below. SC-006 is also `not_evaluated`; the waiver should acknowledge whether it is covered. This review does **not** claim SC-001 or SC-002 met.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | R1 — Enforce branch-(b) escalation + E4 re-baseline + U4 re-verification | `skills/external/sdd-loop-driver/references/efficiency-model.md` §3.5–§3.6 | F1 |
| P1 | R2 — Commit read-only gate evidence before the next stage | `skills/external/sdd-loop-driver/references/dispatch-recipes.md` + stage prompts | F2 |
| P2 | R3 — E3 row per segment; backfill `impl-s7` | `skills/external/sdd-loop-driver/references/efficiency-model.md` §2 | F3 |
| P2 | R4 — Falsifiable clause check | `tasks.md` T039 + `templates/commands/tasks.md` / `implement.md` | F4 |
| P2 | R5 — Checklist reconciliation after repair | `templates/commands/checklist.md` | F5 |
| Open decision | R6 — SC-001/SC-002 benchmark or user waiver | Verification/closure evidence | FR-023 / SC-001 / SC-002 |

## 7. Required Stage Audit Ledger

### 7.1 FR / SC coverage and task-row completeness

| Check | Result | Evidence |
|-------|--------|----------|
| FR definition rows | 30/30 | `requirements.md` (validator: 38 definition rows = 30 FR + 8 SC, rc 0); `tasks.md` § Requirement Coverage Map maps every FR |
| SC definition rows | 8/8 | `verification.md` SC-001…SC-008 matrix; `grep -cE '^- \*\*SC-00[1-8]\*\*'` → 8 |
| Task rows | 39/39 `[x]`; 0 `[~]`, 0 `[ ]` | `grep -cE '^- \[x\]'` → 39; `grep -cE '^- \[[ >~]\]'` → 0 |
| Task ceiling | 39 ≤ 40 | `decomposition-check.py --mode tasks` → `proceed`, `task_count=39` |
| FR/SC/validator counts | fr 30 / sc 8 / tasks 39 / clauses 110 | `pre-analyze-check.py --stage tasks` → `decision=pass errors=0 advisories=0 waived=0` |

All 30 FR and 8 SC have an implementation path and a verification pointer. The SC statuses are the honest matrix, not a blanket "met": SC-001/002/006 are `not_evaluated`; SC-003 is partial (the driver's closure full-suite slot is deferred); SC-004/005/007/008 are met on targeted evidence. The 30-FR/8-SC claim is not exaggerated by the task markers.

### 7.2 Verification evidence quality, red-first, and reproducibility

| Check | Result | Evidence |
|-------|--------|----------|
| Red-first evidence for new behaviour | Present, with real failing commands and rc | `notes/red-first-evidence.md` T005–T035; disclosed false greens: T005 `test_exit_two_on_malformed_plan_json`, T016 three accidental exit-2 greens, T027 one accidental rc-2 green |
| Mutation / falsifiability | 4 drills, each with a control and a mutant that turns a named test red | `tests/contract/test_wp_mutation_drills.py`; `notes/red-first-evidence.md` § T036 (cycle, write-alone, missing-verdict, `not_evaluated`) |
| Final green reproducible | Yes — reproduced at review | `test-evidence/review-targeted-run.txt`: 328 passed / rc 0; skill contract 25 passed; existing driver subset 65 passed (identical to T001) |
| Behaviour-level vs string-level | Substantive evidence is behavioural (gate/report CLI, simulator, dry runs); the one string-level closure check is F4 | `test-evidence/final-070-suite.txt`; `tests/unit`, `tests/contract`, `tests/integration`; F4 |
| Live-driver end-to-end | Not demonstrated; the scheduler/verifier/integrator are proven by the test-only simulator | Plan R4/R12 disclose this; `notes/benchmark-070.md` records 0 live samples. The plan's acceptance for SC-008 is fixture dry runs, so this is a disclosed limitation, not a product failure. |

### 7.3 Invariant checks

| Invariant | Result | Evidence |
|-----------|--------|----------|
| No nested driver | Preserved | SD-13 dry runs and `test_nested_driver...`; the SKILL boundary says package executors never load the driver |
| No stage-command change | Preserved | `git diff --name-only master...HEAD -- templates/commands/ src/ .specify/templates/ .specify/commands/` is empty |
| No second registry / ownership model / integration queue / ledger | Preserved | New files are two scripts, one reference, one preset, docs, tests; the wp-ledger is a fence inside the 058 spine; the scripts only write `--json-out`/report files |
| No persisted team | Preserved | `git diff --name-only master...HEAD -- .specify/teams/` empty; the no-team dry run snapshots the tree before/after |
| No push | Preserved | `git branch -r --contains HEAD` empty; no remote was updated |
| Mirror sync / no new drift | Preserved | `sync-mirrors.py --check` → `ok skills/external/ == .specify/skills/ (32 files)`, rc 0; 5 `cmp` pairs `IDENTICAL`; SKILL pin update intentional (T031 comment) |
| Plan constraint | **Not fully recorded** — see F1 | 10 declared substantive PLAN-EDITs; no E4 re-baseline; no branch-(b) escalation; no recorded branch-(a) U4 re-verification |

### 7.4 Checklist FAIL disposition ledger (33 items)

The per-item authority is `test-evidence/analyze-report.md` § Checklist accountability (33 = 30 raised-as-finding + 3 covered-by + 0 undispositioned). The disposition classes are:

| Class | Items | Status / owner |
|-------|-------|----------------|
| Resolved by the blocking repair | CHK001 (G-01 + C-01), CHK013 (I-02), CHK014 (A-01), CHK015 (A-02), CHK016 (A-03), CHK027 (A-15), CHK034 (A-18) | Resolved; round-2 analyze READY, 0 C / 0 H |
| Covered by existing design clauses | CHK021 (SD-04/D4.1), CHK022 (SD-06/SD-07/D4.1), CHK023 (SD-04/WG-11/WG-15) | Accepted as covered; no requirement change |
| Deferred with a named owner (MEDIUM unless noted) | CHK002 (L-03, LOW), CHK006/CHK007 (A-05), CHK008 (U-02), CHK009 (I-01), CHK010 (A-07), CHK011 (A-08), CHK012 (I-03), CHK017 (A-04), CHK018 (U-04), CHK019 (U-05), CHK024/CHK025 (A-09), CHK026 (U-06), CHK028 (U-07), CHK029 (U-08), CHK030 (I-05), CHK032/CHK033 (A-12), CHK037 (A-11), CHK038 (G-02), CHK039/CHK040 (A-19) | Deferred; owners and one-line fixes in `notes/analyze-repair.md` and `test-evidence/analyze-rerun-report.md`; none blocking |

No checklist FAIL is undispositioned. The checklist file itself remains the dated round-1 observation (F5).

### 7.5 Analyze residual disposition (24 MEDIUM / 3 LOW; R2-01…R2-06)

Disposition: all are **accepted or deferred with an owner**; none is re-opened here and none blocks the review gate. The authority is `notes/analyze-repair.md` § MEDIUM/LOW dispositions and `test-evidence/analyze-rerun-report.md` § New/residual findings.

| Set | IDs | Count | Disposition / owner |
|-----|-----|------:|---------------------|
| Carried MEDIUM, deferred | I-01, I-03, G-02, A-04, A-05, A-07, A-08, A-09, A-11, A-12, A-19, U-02, U-04, U-05, U-06, U-07, U-08, I-05, F-01 | 19 | Deferred to the requirements/design/tasks round named per row in `notes/analyze-repair.md`; F-01 specifically belongs to the next lifecycle command (feature registry refresh) |
| Carried MEDIUM, accepted | G-03 | 1 | Accepted implementation obligation: the overlap re-check after the first driver-source edit is carried by `research.md` R20 item 3 and `feature-ref.md` §5; no task row added |
| Carried MEDIUM, fixed | I-06, I-07 | 2 | Fixed in the repair commit `0df504b9` |
| Carried LOW, deferred | L-02, L-03 | 2 | Deferred; L-03 is the FR-025 060/061 preservation wording |
| Carried LOW, fixed | L-01, L-04 | 2 | Fixed in the repair commit `0df504b9` |
| Rejected appendix | I-04 | 0 open | Rejected as not a finding (the cited contract reconciles the rules) |
| New/residual MEDIUM | R2-01, R2-02, R2-03, R2-04, R2-05 | 5 | Deferred with the one-line fixes already named in `analyze-rerun-report.md` § Next actions; R2-05 is the PLAN-EDIT per-file mapping correction |
| New/residual LOW | R2-06 | 1 | Deferred; cosmetic duplicate 1.5 bound in SC-002 |
| **Open total** | — | **24 MEDIUM / 3 LOW** | 19 + 5 = 24 MEDIUM; 2 + 1 = 3 LOW; none blocking |

### 7.6 Test budget

| Slot | Evidence | Result |
|------|----------|--------|
| E2 implement baseline (exactly once) | spine test-budget fence, seq 1; `baseline-failed.txt`; `baseline-full-run-2026-10-24.txt` | 19 failed / 5341 passed / 1 skipped, rc 1; name list preserved |
| Intermediate targeted sets | `implement-stage-status.jsonl` rows s1–s6 (10 rows); red-first notes | Targeted only; no second full suite |
| S7 targeted set | `final-070-suite.txt` (328 passed), `final-clause-coverage.txt` (110/110), spine s7 | Targeted only; E3 row missing (F3) |
| Review targeted set (this stage) | `review-targeted-run.txt` | 328 + 25 + 65 passed, rc 0; no full suite |
| Closure full suite | `verification.md` § Deferred closure slot | Deferred to the driver after review, by the stage brief; `SC-003` therefore partial |

### 7.7 SC matrix (as recorded by verification.md; not promoted by this review)

| SC | Status | Note |
|----|--------|------|
| SC-001 | `not_evaluated` (closure-blocking) | 0 comparable samples; no user waiver; must not be claimed met |
| SC-002 | `not_evaluated` (closure-blocking) | 0 run-level samples; no user waiver; must not be claimed met |
| SC-003 | `partial` | Targeted suites green; full-suite name-level comparison is the driver's closure slot |
| SC-004 | `met` (targeted) | Gate ownership/coverage tests; zero orphan/cross-territory claims |
| SC-005 | `met` (targeted) | Four-value decision, plan fence canonical, FN-08 verdict mapping |
| SC-006 | `not_evaluated` | No run record supplies interventions/sessions; not named by the FR-023 waiver clause |
| SC-007 | `met` (targeted) | Report metrics and overlap flag; Scenario E derivation |
| SC-008 | `met` (targeted) | Fixture dry runs; existing driver subset 65 passed; live-driver adherence not demonstrated (disclosed) |

### 7.8 Open decision: exact SC-001 / SC-002 waiver wording

The user would need to record a decision in the workspace (for example appended to `verification.md` § Closure verification or a dated decision file) with this shape:

```text
Decision: Waive Feature 070 efficiency criteria.
Criterion/criteria waived: SC-001 / SC-002 (name the one(s) actually waived; a waiver of only one leaves the other `not_evaluated` and closure blocked).
Reason: <why a comparable benchmark is not required for this closure; the benchmark is `not_evaluated` with 0 samples>.
Recorded by: <user name>.
Date: <YYYY-MM-DD>.
Carried into: .specify/specs/070-subagent-task-teams/verification.md § Closure verification (T039) and the closure evidence.
```

If the user prefers measurement instead of a waiver, the benchmark must supply at least three samples per measured stage on the same host class and topology, using the FR-022 interval (first package dispatch to stage U4 completion); the dated anchor is plan 70 min / review 37 min, and a re-measured baseline replaces the anchor rather than mixing sources. SC-006 is also `not_evaluated`; the decision should state whether it is acknowledged (FR-023's naming requirement is SC-001 and/or SC-002).

## 8. Self-Containment Check

- [x] Every recommendation target is repo-relative (primary) with an absolute path only as a parenthetical supplement; no target is marked `external` because every target is in this repository.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in this report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **"No P0 findings raised; the P0 independent-validation pass is vacuously satisfied."**
- [x] **Reachability disclosure**: `HEAD` is unpushed (`git branch -r --contains HEAD` empty), so every commit citation is an absolute path plus a `git show <sha>:<path>` recovery instruction, not a web URL.
- [x] **Recommendation-ID disclosure**: no `REC-…` identifiers were coined; recommendations are keyed `R1`–`R6` so the review-only commit scope (review report + its evidence) does not require a `register.md` edit. If the driver wants registered IDs, assign them at closure and add the register rows in the same commit.

## 9. Feedback

Please share the contents of this document with the spec-kit framework developers.

## 10. Review Gate Statement

- **P0**: 0.
- **P1**: 2 (F1 plan-constraint branch/re-baseline/U4 record; F2 untracked READY evidence).
- **P2**: 3 (F3 S7 E3 row; F4 tautological clause check; F5 checklist reconciliation).
- **Merge-readiness**: the P0 gate is satisfied, but the feature is **not merge-ready until F1 and F2 are fixed or explicitly waived**; the P2 findings may be recorded as follow-ups. Feature closure remains **blocked** independently by SC-001/SC-002 (`not_evaluated`, no user waiver) and by the driver's deferred full-suite closure slot. `not_evaluated` is not promoted to `met` anywhere in this report.
