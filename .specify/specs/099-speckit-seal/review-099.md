# SDD Process Review Report: 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 099 |
| Requirement Key | 099-speckit-seal |
| Requirement Name | Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写） |
| Related Feature | 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写） |
| Repository | spec-kit |
| Repository URL | (no remote contains these commits; remotes: origin=github/spec-kit upstream, plus gitee/github/gitlab forks) |
| Reachability of COMMIT_SHA | UNRESOLVABLE — `git branch -r --contains HEAD` is empty. Cite absolute paths and recover files with `git show 34b6d9866:<path>`; no blob URL can resolve. |
| Branch | 099-speckit-seal |
| Commit SHA | 34b6d98667bcfcbef29f7d0ee651a2b4ff36bd39 (short: 34b6d9866) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal (git worktree; the repository root is /storage/project/cloud-native-ai/spec-kit) |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder review agent (fresh session; no implementation authorship in this session) |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash, Python 3.11.11, pytest 8.4.2, git 2.43.5 |
| spec-kit Source Snapshot | this repository at 34b6d9866 (self-hosted `.specify/` runtime; `.specify/shared/` is byte-identical to `shared/`, 111 files) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 251 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/requirements.md | 28 FR / 9 SC (final 6, supporting 3) / RS-001…003 / STR-001…003 + clarifications |
| plan.md | 333 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/plan.md | Constitution Check 22 Pass, 6 decision tensions, 12 verified premises, P1–P9 execution model |
| tasks.md | 374 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/tasks.md | 51 rows, all `[X]`, 0 open / 0 deferred; 10 DoD + 5 gates |
| verification.md | 76 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/verification.md | smoke triple + SC-001…009 all `pass` + final_path 6/6 accept + empty deferred set |
| data-model.md | 216 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/data-model.md | E1–E14 entities, V1–V16 validation rules |
| quickstart.md | 196 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/quickstart.md | S-1…S-9 walkthroughs |
| research.md | 228 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/research.md | R-01…R-21, all measured |
| feature-ref.md | 115 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/feature-ref.md | FR 28/28 and SC 9/9 mapping |
| contracts/ (4 files, 444 lines) | 444 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/contracts/ | C-001…C-045 across engine, merge-back, records, status |
| feature detail | 69 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features/099-speckit-seal.md | Status Implemented; Latest Review entry of the P9 implement run |
| code-review record (this run) | 1841 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review.md | six-level findings + coverage receipt 451/29/422/0 |
| 074 round evidence | 2 files + JSON/TXT set | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/test-evidence/074-round* | pre-fix and P8b rerun adjudication records |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Driver U0 entry writes the line state spine | `.specify/state/099-speckit-seal.md:5-9` (`stage: requirements`, `attempt: 0`) — the block is never advanced through the rest of the run | Yes — the spine stays at the U0 snapshot (Workflow finding F7) |
| 2 | requirements stage | e0e239709 → 594832030 (run records) → 404dcbde6 (close-out) | None |
| 3 | clarify stage | 0131e24d2 → 4951b5967 → c998f2a43 | None |
| 4 | plan stage | 749b613c0 → f7959ccc1 → 32406eddd | None |
| 5 | Out-of-band constitution amendment between plan and tasks | d4a52bd38 `docs(constitution): amend Principle VII carrier to verification.md (1.19.1)` — touches `.specify/constitution.md`, `shared/guidelines/better-harness.md`, its mirror and `tests/contract/test_fast_fail_discipline.py`; no 099 task row names it; the user ruling is recorded only in the constitution's Sync Impact Report | Yes — a write outside the slice's declared task rows (Workflow finding F8) |
| 6 | tasks stage | 4f1ef128f → 1afd6821f → b2f7ef451 → 2fd48f346 → cf7fb8f13 | None |
| 7 | checklist stage | 105d22c30 → 2f56a6de7 → 3b79af6e2 → bf576e58e | None |
| 8 | analyze round 1 + repair r1 | 026dd2aa8 (12 findings: 0 CRITICAL / 7 HIGH) → ff253f8e2 (requirements/plan/tasks/contracts repairs) | Prescribed (analyze before implement) |
| 9 | analyze round 2 + repair r2 | 6d4859316 (1 HIGH residual) → 484a9930c | Prescribed |
| 10 | analyze round 3 → PASS | 64120b3a8 (`0 CRITICAL / 0 HIGH / 5 MEDIUM / 1 LOW`; 6 open advisory findings carried) | None (gate admits MEDIUM) |
| 11 | implement P1–P7 | 1f88f8821 (setup) → 93843c567 (status domain) → 34f2a40fc → 32359073c → a9eb3f990 → 2939a408d → a2b07c584 → 3f2a05cba (command surface) | None |
| 12 | 074 round, first attempt | 1b3e422a8 (merge round) → cbf55b89c (adjudication) → b0cb4e6f4 (row states); terminal blocked with B1–B4 | Prescribed; the round exposed engine defects |
| 13 | P8b engine repair + 074 rerun | 8460536ca (three root-cause fixes + replay) → 611b8d982 (rerun adjudication) → 5e233678a (suite reading) | Corrective follow-up within P8; documented red-first |
| 14 | P9 polish + P9b deferral closure | 6aaa15019 (T045–T050) → 34b6d9866 (T041, T050 closed; verification rerun) | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 7 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 2 |
| Workflow | 3 |
| Documentation | 4 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | 34b6d98667bcfcbef29f7d0ee651a2b4ff36bd39 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec .specify/specs/099-speckit-seal` |
| Renderer mode | renderer: text | the code record's header marker (no TTY, non-interactive agent run) |
| Changed / judged / skipped / gap files | 451 / 29 / 422 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | blocked | one `blocking` entry (F1 below) |
| Gate verdict | `blocking-unresolved` | `report --summary --file` returns `gate=deny`, exit 1 (`blocking_entries=1`) |
| Reason, when one applies | The current `code-review.md` carries one blocking entry: the split-parent P0 hole in `scripts/python/seal-utils.py` (F1 below). Under the unattended disposition the transition halts and the status stays `Implemented`. | `code-review.md` § [BLOCKING] |
| Uncommitted scope | > **未提交范围（未评审）**: 2 个未提交路径未计入本次评审对象（.specify/memory/trigger/index.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt）；本回执不对该范围给出任何结论。 | disclosed, never concluded over; the same sentence lives in the record |
| Record | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review.md | written because the triage value is `run` |
| Archive | none | first code-segment run for this feature |

**The one blocking entry, named.** `scripts/python/seal-utils.py:2597` — for a split parent the seal P0 gate reads only the parent `review.md`, while merge-apply generates that file as a pointer-only view; a slice review P0 is therefore invisible to `p0-unresolved` (full finding F1). Six-level counts: blocking 1 · important 1 · suggestion 1 · nitpick 0 · question 0 · praise 1.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | union of the standard spec-stage set and `plan.md` § Project Structure (which additionally names research.md, feature-ref.md) |
| Coverage line | 9 / 9 (missing: none) | present members / expected members |
| Missing members | none | — |
| Segment verdict | blocked | one P1 internal contradiction (FR-006 vs C-013/C-021) plus four supporting P2s; the members themselves are all present |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | .specify/specs/099-speckit-seal/requirements.md | 132 (and 223) | none | FR-006 + its Clarifications entry require the split-parent P0 to be judged by the original slice records, while `contracts/merge-back.contract.md` C-013/C-021 defines the merged parent review view as pointers; the two owners contradict and the delivered view cannot satisfy FR-006 (F2). |
| P2 | .specify/features.md | 102 | none | The 099 row's Last Updated cell still discloses `T050 [~]` and the T041 deferral after 34b6d9866 closed both; tasks.md and verification.md record zero deferred (F4). |
| P2 | .specify/specs/099-speckit-seal/plan.md | 208-209 | none | The plan says the 074 round's write face is the parent spec dir plus the two slice requirements annotations, contradicting contract C-023, which also authorizes factory-doc reference fixes; the round wrote 18 source refs plus mirrors (F5). |
| P2 | .specify/specs/099-speckit-seal/verification.md | 23 | none | The SC-001 note cites the P8b targeted suite as `130 passed`, while the recorded evidence file reads `133 passed` (F6). |
| P2 | .specify/specs/099-speckit-seal/tasks.md | 116, 182, 183, 208 | none | Four `green-cross-phase` warnings: clause claims run backwards against row order, so those rows cannot leave their contract green at their own phase (F10). |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base (`feature-first-commit`) |
| Head commit | 34b6d98667bcfcbef29f7d0ee651a2b4ff36bd39 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec …` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/integration/test_seal_074_round.py -q` | recorded verbatim from `verification.md` `smoke_command=` |
| Smoke exit code | 0 | re-measured this session: 5 passed in 6.32s (capture retained at `.specify/.tmp/review-099/smoke-seal-074-round.txt`) |
| Smoke evidence path | .specify/specs/099-speckit-seal/notes/quickstart-run.md | exists and non-empty; the feature's smoke record |
| Scope and regression verdict | The P8b repair is root-caused and reproduced: the seal contract+integration set is 133/133 green; two independent seal runs on the 074 tree are byte-identical (exit 2, sole `closure-input-defect`, writes 0); 47/47 slice dated-record hashes unchanged; mirror and command-copy checks exit 0. One P0 correctness hole (split-parent P0) and one P2 atomicity edge remain. | see the rows below |
| Segment verdict | blocked | one P0 (F1) + one P2 (F9) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P0 | scripts/python/seal-utils.py | 2597 | none | For a split parent the seal P0 gate reads only the parent `review.md`; the merged parent view is pointer-only, so a slice P0 with only a driver-recorded waiver is invisible and a future split parent could seal with it unresolved (F1; independently validated). |
| P2 | scripts/python/seal-utils.py | 2463 | none | `_write_seal_batch` does not restore the in-flight file when `write_text` raises after truncation; C-005 requires every written file restored, and the guard test covers only an open() permission failure (F9). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Implemented | the bound feature detail's claim, copied |
| `final_path` record, copied verbatim (7/7) | pass 6 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 6 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/099-speckit-seal --json`, never recomputed here |
| Comparison verdict | agree | `verdict=accept` with `every_final_path_pass=true`, `no_open_rows=true`, `smoke_record_pass=true`, `status_row_per_criterion=true` |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The ARC does not refuse this transition. The refusal recorded in § 2.1 comes from the code segment's blocking entry, not from the acceptance record.

## 3. Findings (Problems & Improvement Targets)

### F1 — The split-parent seal P0 gate is vacuous (slice P0s are invisible)

- **Severity**: P0
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py L2557–L2597 (`evaluate_seal` P0 gate), L2117–L2125 (`_review_summary`), L2189–L2207 (`_p0_findings`), L1525–L1567 (`_pointer_view_block` / `_pointer_view_content`)
- **Evidence** (verbatim quote):

  ```
  父级聚合 review 视图为 summary+pointer、不含 finding 块，seal 的 P0 扫描未点名该项；
  回合按原记录（.specify/specs/074b-nested-governance/review.md:115-136）判 blocked，不得读作已处置。
  ```

  and the generated parent view itself (`.specify/specs/074-goal-team-sdd-unification/review.md:1-4`):

  ```
  # Review — aggregated pointer view (074-goal-team-sdd-unification)

  - 074a-authorized-routing: .specify/specs/074a-authorized-routing/review.md — > **Audience**: spec-kit framework maintainers.
  - 074b-nested-governance: .specify/specs/074b-nested-governance/review.md — > **Audience**: spec-kit framework maintainers.
  ```

- **Why it's a problem**: `_p0_findings` scans finding blocks only in the parent `review.md`; `_review_summary` reads a Findings Summary table and silently counts zero when none exists; the merge engine writes the parent review view with pointer lines and no finding block or summary. The 074b slice review's P0 F1 (lettered slice branch resolves `/speckit.*` to the parent directory) carries only a driver-recorded waiver (`.specify/specs/074b-nested-governance/review.md:115-140`), so it is exactly the shape FR-006 must refuse. Re-running seal on the 074 tree confirms it: exit 2 with the sole condition `closure-input-defect` and no `p0-unresolved`; the round record names the P0 only because a human authored the adjudication. A future split parent with a valid closure input could write `Sealed` with an unresolved slice P0 — a silent false terminal state that the archive gate would then admit. The clarification at `requirements.md:223` requires "P0 处置按原记录判定"; no code path follows the pointers. Independent read-only validation returned `confirm` at P0.
- **Proposed fix**: make the merged review view carry an aggregate P0/blocking summary (per slice: P0 count and the finding anchors), and/or make `_p0_findings` follow the pointer lines into the slice review records; add a split-parent fixture whose slice review carries an unwaived P0 and assert `p0-unresolved` exit 1 with zero writes. Record the current-vs-archived review record derivation rule in the contract at the same time (the analyze round's open finding C-02 asks for exactly this).

### F2 — FR-006's original-record rule and C-013/C-021's pointer-only view contradict

- **Severity**: P1
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/requirements.md L132 and L223; /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/contracts/merge-back.contract.md L23–L40 (C-013) and L112–L117 (C-021)
- **Evidence** (verbatim quote):

  ```
  - **FR-006**: 「review 结论无 P0」MUST 按当前 review 记录判定：当前 `review.md`（若存在多个，取当前记录集合，归档记录不计）的 findings 摘要 MUST 显示**零个未处置 P0**
  ```

  ```
  Q: seal 读取「哪一份 review 结论？」… A: 不需要重跑。单体 spec 读其当前 `review.md`/`code-review.md`；拆分 spec 读**合并后的父级 review 汇总视图**（由各分片当前 review 记录合并而来，见 FR-019/FR-026），P0 处置按原记录判定。
  ```

  ```
  **C-021** — 散文类产物的合并规则。… 父级 `review.md` / `code-review.md` / `verification.md` 的合并视图按 C-013 / C-020 的「汇总 + 指针」形态生成。
  ```

- **Why it's a problem**: the requirement says the split-parent P0 disposition is judged by the original records; the merge contract's "汇总 + 指针" shape was implemented as pointers-only for review.md and code-review.md (C-013's own pointer-view row names no summary content). Two owners state the same fact differently, and the implementation followed the weaker one (F1). A reader implementing from the contract has no obligation to carry P0 information; a reader implementing from the requirement expects it.
- **Proposed fix**: define the review.md/code-review.md merged view's summary content in C-013/C-021 (the per-slice P0 count and finding anchors are the minimum), or extend FR-006 with an explicit pointer-walk obligation; then align the engine and add the fixture (paired with REC-099-1).

### F3 — C-022's supersede rendering voids the parent's `[green:]` claims, producing a 67-name coverage residual per split merge

- **Severity**: P1
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/contracts/merge-back.contract.md L118–L130 (C-022); /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/tasks.md L240 (T050); /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/test-evidence/coverage-final.txt
- **Evidence** (verbatim quote):

  ```
  status=uncovered (exit 1)
  claimed_clauses_this_feature=45 (45/45 contract clauses claimed by [green:] declarations in tasks.md; ...)
  uncovered_beyond_baseline=67
  ```

  ```
  67 条具名残留为 C-022 强制保留拆前行的必然后果，本 spec 自身条款 45/45 与 FR 28/28 无缺口
  ```

- **Why it's a problem**: converting the parent's 57 pre-split task rows into `> - [ ]` quoted records removes the rows that carried the parent contracts' `[green:]` claims; the clause-coverage engine then reads 67 parent contract clauses as uncovered (five 074 parent contracts). This is inherent to the C-022 rendering: every split merge will pay the same toll, and each must record a named residual instead of a clean coverage reading. The user's D-074-R1 ruling accepts the residual for 074; the framework-level conflict remains (state spine FO, 2026-11-11).
- **Proposed fix**: record the claim on the superseded record itself (e.g., a machine-readable `retains-claim` field on the supersede disposition) so the coverage engine can count the claim as retained, or make C-022's rendering keep the `[green:]` annotation outside the quoted row; then update `account-clause-coverage.py` to consume the new form.

### F4 — The registry row and feature detail still disclose T050 `[~]` / T041 deferrals that no longer exist

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features.md L102 (Last Updated cell); /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features/099-speckit-seal.md L21–L29 (`## Latest Review`)
- **Evidence** (verbatim quote):

  ```
  披露：T050 `[~]`——074 回合按 C-022 把父级 57 条拆前行 green 认领转为记录，遗留 67 条 074 父契约未覆盖名逐名归因（非本 spec 缺口，待用户裁定）；T041 保留 P8 历史延后记录
  ```

  and the current task rows/verification: `tasks.md:222` `- [X] T041 …`, `tasks.md:240` `- [X] T050 …`, `verification.md:59` `deferred_tasks=` (empty).
- **Why it's a problem**: the two status carriers still tell a reader that T041/T050 are deferred while the authoritative task and verification records show 0 deferred. The stale text predates 34b6d9866 (P9b closure) and was not refreshed; a reader checking the gate condition "every deferred task resolved" sees conflicting statements.
- **Proposed fix**: refresh the 099 registry Last Updated cell and the feature detail's current review entry to state that T041/T050 were closed on 2026-11-11 (P9b), keeping the historical disclosure in the dated record rather than in the current claim.

### F5 — The plan's 074-round write-face sentence is narrower than contract C-023

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/plan.md L208–L209; /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/contracts/merge-back.contract.md L132–L136 (C-023)
- **Evidence** (verbatim quote):

  ```
  074 回合写面被限制在父 spec 目录与两片各自 `requirements.md` 的一行标注上。
  ```

  ```
  `merge-apply` 只写父 spec 目录、分片的 `merged into` 标注与 C-017 记录过解决方式的出厂文档引用修正；
  ```

- **Why it's a problem**: the plan omits the third write face that C-023 explicitly authorizes (factory-doc reference fixes); the round actually wrote 18 source references plus their mirrors (`test-evidence/074-factory-resolutions.md` § A/B). A reader of the plan would believe those writes are out of scope, and a scope audit against the plan would flag them.
- **Proposed fix**: replace the plan sentence with a pointer to C-023 (or restate all three write faces in the plan and cite C-023 as the owner).

### F6 — The P8b suite reading is cited as 130 passed while the recorded evidence says 133

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/verification.md L23
- **Evidence** (verbatim quote):

  ```
  P8b targeted suite 130 passed on the seal contract+integration set
  ```

  vs the evidence file `test-evidence/p8b-suite-20261111.txt:13`:

  ```
  133 passed in 8.38s
  ```

- **Why it's a problem**: the final reading was extended from 9 to 10 files (adding `test_seal_merge_determinism.py`) in 5e233678a, moving 130 → 133; the verification note was not updated. A reader checking the note against the evidence sees a number that does not match its own source.
- **Proposed fix**: update the SC-001 note to 133 passed and name the evidence file, or state that 130 was the earlier 9-file selection.

### F7 — The driver's state spine is stale at the U0 requirements snapshot

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/state/099-speckit-seal.md L5–L9 (loop-state block; repository root, outside the worktree)
- **Evidence** (verbatim quote):

  ```
  spine_state: running
  run_id: r20261110T121314Z-b099
  slice: 099-speckit-seal
  stage: requirements
  ...
  attempt: 0
  last_verdict: U0 entry written; requirements dispatching
  ```

- **Why it's a problem**: after the line completed requirements → … → P9b closure, the machine-readable block still says the run is in the requirements stage with attempt 0. Any orchestrator or resume path that reads this block sees a snapshot from the first minutes of the run; the prose sections below it were also never advanced. The user's review dispatch had to supply the real state from conversation context.
- **Proposed fix**: have the driver's stage transitions rewrite the loop-state block (stage, attempt, last_verdict, timeline) or explicitly mark the block as a U0-only snapshot and point to the live line registry as the authority.

### F8 — An out-of-band constitution amendment lands between plan and tasks without a task row

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/constitution.md L18–L27 (the 1.19.1 Sync Impact Report); commit d4a52bd38 in the feature range
- **Evidence** (verbatim quote):

  ```
  - Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)
  - Modified principles: VII. Workflow Gates — the Pre-Status-Flip Gate's status-line carrier is corrected from `verification.log` to `verification.md` ...
  - User ruling (2026-11-10): amend the constitution to the framework carrier rather than create a second record surface.
  ```

- **Why it's a problem**: the amendment changed `.specify/constitution.md`, `shared/guidelines/better-harness.md` (+ mirror) and `tests/contract/test_fast_fail_discipline.py` between the plan and tasks stages; no 099 task row authorizes it, and the feature's plan/tasks do not mention it. The user ruling exists, but it is recorded only inside the constitution's own report, so a reader of the feature artifacts cannot account for the write. (T014 later bumps the constitution to 1.19.2 for the Sealed narrative and does have a task row; this finding is about the separate 1.19.1 amendment.)
- **Proposed fix**: record out-of-band user-ruled amendments as a dated row in the feature's plan or tasks (with the ruling reference), or require the manage-constitution flow to emit a linked task row when it runs inside a feature's timeline.

### F9 — `_write_seal_batch` leaves a partially written in-flight file unrestored on a mid-write failure

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py L2451–L2472
- **Evidence** (verbatim quote):

  ```
  for path, text in targets:
      originals[path] = path.read_bytes() if path.is_file() else None
      path.write_text(text, encoding="utf-8")
      written.append(path)
  except (OSError, UnicodeError) as exc:
      for path in reversed(written):
          previous = originals.get(path)
  ```

- **Why it's a problem**: `Path.write_text` opens with truncation before writing. If the write raises mid-stream (e.g. ENOSPC), the current path is not yet in `written`, so the restore loop skips it; the file that failed may be left partially written. Contract C-005 requires restoring every written file on any failure, and the guard test (`tests/contract/test_seal_seal.py` L457–L480) only exercises an open() permission failure on the detail file, so this path is unexercised. The consequence is a half-sealed registry row or detail on a rare I/O failure.
- **Proposed fix**: restore the current path in the exception handler as well (or append the path to `written` before writing), and add a fault-injection test that fails between truncation and write completion.

### F10 — Four task rows claim contract clauses in an order that cannot go green at their phase

- **Severity**: P2
- **Category**: Template
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/tasks.md L116, L182, L183, L208
- **Evidence** (verbatim quote):

  ```
  WARN  116: green-cross-phase: T003 ... claims contracts/status-sealed.contract.md#C-029 while the later T006 ... claims #C-024 — the clause order runs backwards against the row order ...
  WARN  208: green-cross-phase: T038 ... claims contracts/records-and-boundaries.contract.md#C-041 while the later T042 ... claims #C-038 ...
  ```

- **Why it's a problem**: `validate-tasks.py` passes with 0 errors but the four warnings mean the rows' green claims are not phase-consistent: the earlier row claims a higher clause than a later row and cannot leave that contract fully green at its own checkpoint. The feature delivered, so this is retrospective quality debt in the task graph rather than a live failure; it erodes the "green means this row closed its claim" signal for later features.
- **Proposed fix**: re-cut the clause partition between the paired rows or move the earlier clause's row ahead of its consumer; add the warning count to the tasks-stage close-out reading so it is dispositioned rather than merely printed.

## 4. What Worked — Preserve (Brief)

- The P8b repair is root-caused with red-first evidence: three targeted tests fail on the unfixed engine (`p8b-red-first-20261111.txt`) and pass after the fix (133/133).
- The 074 round rerun is genuinely reproducible: two independent seal runs are byte-identical (exit 2, sole `closure-input-defect`, zero writes); re-verified in this review.
- Dated-record discipline holds for the slices: 47/47 slice review/code-review/verification/test-evidence hashes unchanged across the round (re-verified).
- The status domain has one owner and seven consumer faces; the drift guard names any surface that drops `Sealed`, and the archive gate has a single implementation with a static single-owner scan.
- The code-segment receipt correctly refuses to treat skipped files as coverage credit, and the blocking gate is an existence test with no "cleared" state.
- Mirror discipline: `sync-mirrors.py --check` (111 shared files byte-identical) and `regen-command-copies.py --check` both exit 0.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-099-6** — Target: `templates/tasks-template.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/templates/tasks-template.md). Change: add a tasks-stage close-out obligation to disposition every `green-cross-phase` warning (re-cut the partition or record why the order is intentional), so the warning is actionable rather than printed. Source: F10. Expected impact: the per-row green claim stays a truthful checkpoint signal.

### 5.2 Automation / Script Improvements

- **REC-099-1** — Target: `scripts/python/seal-utils.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py). Change: carry an aggregate P0/blocking summary into the merged `review.md`/`code-review.md` views and/or make `_p0_findings` follow the pointer lines into the slice records; add a split-parent fixture whose slice review carries an unwaived P0 and assert `p0-unresolved` exit 1 and zero writes. Source: F1, F2. Expected impact: the seal P0 condition is no longer vacuous for the feature's primary split scenario.
- **REC-099-5** — Target: `scripts/python/seal-utils.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py). Change: restore the in-flight path on a mid-write failure (or register it as written before the write) and add a fault-injection test. Source: F9. Expected impact: C-005's atomic-batch promise holds on every failure class, not only open() failures.

### 5.4 Workflow Improvements

- **REC-099-2** — Target: `shared/workflow/acceptance-hardening.md` / `contracts/merge-back.contract.md` in the declaring feature (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/shared/workflow/acceptance-hardening.md). Change: state once whether a superseded pre-split record retains its `[green:]` claim for coverage accounting, and make `account-clause-coverage.py` consume that form. Source: F3. Expected impact: split merges stop producing a 67-name residual that every future merge must re-explain.
- **REC-099-4** — Target: `skills/external/sdd-loop-driver/scripts/line-registry.py` and the driver's state-spine writer (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/skills/external/sdd-loop-driver/). Change: advance the loop-state block on every stage transition, or mark it as a U0-only snapshot with the live registry named as the authority. Source: F7, F8. Expected impact: resume and audit paths read the real stage instead of a first-minute snapshot.

### 5.5 Documentation Improvements

- **REC-099-3** — Target: `.specify/features.md`, `.specify/features/099-speckit-seal.md`, `.specify/specs/099-speckit-seal/plan.md`, `.specify/specs/099-speckit-seal/verification.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/). Change: refresh the deferral disclosure after P9b, point the plan's round write-face sentence at C-023, and update the P8b suite number to 133 with its evidence path. Source: F4, F5, F6. Expected impact: the status carriers and plan agree with the authoritative task/verification records.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Split-parent P0 gate must read the original records | `scripts/python/seal-utils.py` + merge view generation | F1, F2 |
| P1 | Superseded records must retain their claim | `shared/workflow/acceptance-hardening.md` + `account-clause-coverage.py` | F3 |
| P2 | Atomic batch restores the in-flight file | `scripts/python/seal-utils.py` | F9 |
| P2 | Status-spine advancement | driver state writer | F7, F8 |
| P2 | Artifact narrative refresh | feature registry/detail/plan/verification | F4, F5, F6 |
| P2 | Green-cross-phase disposition | `templates/tasks-template.md` | F10 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target needed an `external` marker.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: one P0 finding was raised and confirmed by an independent read-only validator (`confirm`, P0); the P0 independent-validation pass is not vacuous.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
