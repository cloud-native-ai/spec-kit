# Specification-Driven Development (SDD) Process Review Report: 100-seal-slice-archive

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 100 |
| Requirement Key | 100-seal-slice-archive |
| Requirement Name | /speckit.seal — 分片归档步骤（Seal Slice Archive） |
| Related Feature | 099 Speckit Seal |
| Repository | spec-kit (git worktree `.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive`) |
| Repository URL | `gitee` `git@gitee.com:cloud-native-ai/spec-kit.git`; `github` `git@github.com:cloud-native-ai/spec-kit.git`; `gitlab` `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`; `origin` is the upstream `git@github.com:github/spec-kit.git` and does not hold these commits |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty, so no remote URL citation resolves. Use the absolute paths below plus `git show 8f4e4276e:<path>` for recovery. |
| Branch | 100-seal-slice-archive |
| Commit SHA | `8f4e4276e84fc9d7c8fdae39febcf6ca81c970c4` (short: `8f4e4276e`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder agent — unattended `/speckit.review` run (four segments + Acceptance Reality Check) |
| Environment | Linux 5.10.134 x86_64; Python 3.11.11; git 2.43.5; pytest 8.4.2; tests run through `scripts/bash/run-tests.sh` |
| spec-kit Source Snapshot | this repository @ `8f4e4276e84fc9d7c8fdae39febcf6ca81c970c4` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 231 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/requirements.md` | 28 FR / 10 SC / 5 shared strings / 5 clarification rulings for the slice-archive step. |
| plan.md | 275 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/plan.md` | 22-principle Constitution Check, 6 decision tensions, 8 work packages, mirror obligations. |
| research.md | 186 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/research.md` | R-01…R-14 owner file:line measurements. |
| data-model.md | 158 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/data-model.md` | E1–E10 entities and V1–V14 validation rules. |
| quickstart.md | 169 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/quickstart.md` | S-1…S-6 walkthroughs with plan-stage premises. |
| contracts/ (3 files) | 305 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/contracts/` | 40 clauses: archive-actions 16 (C-101…C-116), archive-manifest 12 (C-201…C-212), reference-classification 12 (C-301…C-312). |
| feature-ref.md | 124 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/feature-ref.md` | FR 28/28 and SC 10/10 delivery maps. |
| tasks.md | 368 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/tasks.md` | 53 rows / 8 work packages / 40 green claims, all `[X]`. |
| verification.md | 65 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/verification.md` | SC-001…SC-010 status rows, smoke triple, RS-004 joint acceptance. |
| checklists/ (dated + pointer) | 112 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/checklists/` | 36-item requirements-quality checklist and its pointer file. |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | U0 line registered; worktree from master `48e273d73` | `/storage/project/cloud-native-ai/spec-kit/.specify/state/100-seal-slice-archive.md` § U0 Entry Declaration | none |
| 2 | Requirements authored | `17962af8c` `docs(100-seal-slice-archive): author requirements and archive-owner research` | none |
| 3 | Clarify binds Feature 099 and records five rulings | `9695d78c5`; requirements.md § Clarifications (lines 213–220) | none |
| 4 | Plan, research, data model, contracts, quickstart | `0c7a2bd28`; same-author repairs `90bab87ee` | none |
| 5 | Tasks authored (53 rows, 40 green claims) | `d2386834c`; close-out `d6544a9e2`, `c15f3bf17` | none |
| 6 | Checklist authored (36 items, 11 fail handed to analyze) | `9c88fbb53`; close-out `6f01f7919`, `134daf45f` | none |
| 7 | Analyze closes 37 C/H with 0 open | `f821daf83`; `test-evidence/analyze-merged-2026-11-11.md` | none at the gate, but the cross-clause C-302/C-306/C-307 contradiction survived (F1) |
| 8 | Setup baselines frozen | `8974dc8ef` | none |
| 9 | P1 engine six-action set; P2 manifest-aware discovery; P3 archive-plan; P4 archive-apply | `21f30f445`, `efe5f4d3f`, `4b62d1677` + `b85f7afd3`, `595d78a86` | none |
| 10 | P6 command/skill surface; P5 owner-page revisions | `be41fb2ec`, `24d920bd0` | none |
| 11 | First real 074 round refused: 61 `unclassified-reference` + 1 `unresolved-references` | `2fe5661e5`; `test-evidence/074-archive-round.txt` § P7 (lines 1–899) | **deviation**: a contract-level contradiction blocked the real acceptance round |
| 12 | Owner ruling converges C-302 by carrier class (dated loose forms → `dated-preserved`) | `abdf9a6df`; 074-archive-round.txt § P7b | **deviation**: a mid-implementation contract revision, not planned at the plan stage |
| 13 | 074 archive batch: 112 `R100` moves, 19 M carriers, 1 A manifest | `a2c1f2bf7`; same evidence file § T043 | none |
| 14 | Reproducibility + rollback drill; P8 suite/mirror/quickstart closure | `f3bd72866`, `64931e488`, `8f4e4276e` | **deviation**: the P7b engine edit left the `.specify/scripts/` mirror stale until P8 (F5) |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 2 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 7 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 4 |
| Workflow | 3 |
| Documentation | 2 |

**P0 validation status**: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `48e273d7395d949656099c596161ac9210687cfa` | the resolved diff base |
| Head commit | `8f4e4276e84fc9d7c8fdae39febcf6ca81c970c4` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec .specify/specs/100-seal-slice-archive` |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 354 / 26 / 328 / 0 | copied field by field from the record's coverage-receipt block |
| Segment verdict | `not-evaluated` | 328 legal skips earn no coverage credit (generated mirrors/command copies and non-code artifacts); zero `blocking` entries |
| Gate verdict | `allow` | `report --summary --file` → `{"blocking":0,"important":3,"suggestion":1,"nitpick":1,"question":0,"praise":1}`, exit 0 |
| Reason, when one applies | not-evaluated: 328 of 354 changed files were legally skipped; 26 code/surface files judged; gap 0 | the receipt's own skip reasons |
| Uncommitted scope | `.specify/templates/gitignore-specify-template` (pre-existing working-tree modification) is not part of the reviewed delta; this receipt gives no conclusion over it. | the record's disclosure line |
| Record | `.specify/specs/100-seal-slice-archive/code-review.md` | written (triage `run`) |
| Archive | `none` | first run |

The three `important` items are answered in §3 F2, F3 and F4 (agreement plus a reason); `important` never blocks the transition, and no `blocking` entry exists.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, research.md, data-model.md, quickstart.md, contracts/, feature-ref.md, tasks.md, verification.md | union of the standard spec-stage set and `plan.md` § Project Structure (which additionally names research.md and feature-ref.md) |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | all expected members exist and carry their required sections; one P1 contract-precision finding (F2) and one P2 record-status finding (F8) |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md` | 59 (and 71) | none | C-306(c) and C-308 require a file-level sha256 equality for every `dated-preserved` carrier, but a mixed carrier that also has live rows must change; the 074 feature detail is exactly that case (F2). |
| P2 | `.specify/specs/100-seal-slice-archive/tasks.md` | 73 | none | `**DoD Status**: pending` survives 53/53 closed rows and a satisfied DoD-1…DoD-10 set (F8). |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `48e273d7395d949656099c596161ac9210687cfa` | the resolved diff base |
| Head commit | `8f4e4276e84fc9d7c8fdae39febcf6ca81c970c4` | the run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec .specify/specs/100-seal-slice-archive` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py tests/integration/test_seal_archive_round.py -q` | recorded verbatim from `verification.md` `smoke_command=` |
| Smoke exit code | 0 | re-measured this session: `52 passed in 6.65s` |
| Smoke evidence path | `.specify/specs/100-seal-slice-archive/test-evidence/us1-checkpoint.txt` | exists, non-empty, carries the same command and `52 passed` |
| Scope and regression verdict | Scope is the declared surface: 354 changed files = 199 A + 43 M + 112 R100 and zero D; the 112 R100 are the two 074 slices moved byte-identically, the 19 M are exactly the declared live carriers, and the one A is the archive manifest. Regression: the archive suites read 137 passed with the two named baseline reds (`test_seal_boundaries.py` unregistered live specs 097/098/100); the recorded full-suite evidence compares 207 failures against the 217-entry implement-entry baseline with `comm -13` empty. The 074 round replayed idempotently this session (`already-archived`, zero diff); `merge-plan` and `seal` on the archived tree read the same slice set from the manifest. Two P2 record-accuracy/evaluation gaps remain (F3, F4) plus one P2 reporting gap (F9). | `test-evidence/final-suite.txt`, `test-evidence/074-archive-round.txt`, `test-evidence/us4-checkpoint.txt`, this run's `git diff`/status readings |
| Segment verdict | `pass` | no P0/P1 in the delta; the 074 acceptance is reproduced; findings are P2 |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | `.specify/specs/074-goal-team-sdd-unification/archive-manifest.json` | 610 | none | 117 of the 123 merge-manifest ledger rows carry a stale `line` after the digest relocation (F3). |
| P2 | `scripts/python/seal-utils.py` | 4320 | none | `unresolved_after` is passed as a literal 0 and never re-measured after the apply batch (F4). |
| P2 | `scripts/python/seal-utils.py` | 506 | none | The C-102 `not-evaluated (blocked-by <reason>)` rows are not emitted on an early input defect (F9). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features/099-speckit-seal.md` (the bound feature detail) |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/100-seal-slice-archive --feature-detail .specify/features/099-speckit-seal.md --json`, never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept`; claimed status `Ready for Review`; the pass bucket is non-zero (4) |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition judgement.** The one transition this run judges is `Implemented → Ready for Review`. Its four conjunctive gate conditions (owner: `.specify/templates/feature-details-template.md` § Canonical Status State Machine) all hold: (a) every deferred `[~]` task is resolved — `deferred_tasks=` is empty and ARC reads 53 closed / 0 deferred; (b) review evidence is produced — this report plus `code-review.md`; (c) the current code-segment record carries zero `blocking` entries; (d) no `final`-path criterion sits in `blocked` / `deferred` / `fail` — all four read `pass`. Because the bound feature detail already claims `Ready for Review` (carried by Feature 099's review round 2), this run performs no status write: the transition is legal and already in force, and the claim is neither advanced nor regressed. The code segment's `not-evaluated` verdict is disclosed on both carriers and does not block.

## 3. Findings (Problems & Improvement Targets)

### F1 — Analyze accepted a contract-level contradiction that only the real round exposed

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/100-seal-slice-archive/test-evidence/analyze-merged-2026-11-11.md:274` (repaired disposition), `.specify/specs/100-seal-slice-archive/test-evidence/074-archive-round.txt:900-930` (P7b disposition record)
- **Evidence** (verbatim quote):

  ```
  | R3/RC-N01 | HIGH | F1/F2 lacked token boundaries; absolute paths and `../<slug>` matched; cross-line forms were undetectable | F1/F2 now carry explicit left/right boundaries and `<slug>` ∈ manifest slices; cross-line/absolute carriers with a slug literal and no line-level form are `unclassified-reference` |
  ```

  and, from the first real round:

  ```
  ## Premise correction (input sanity)

  The P7 block was recorded as “62 × `unclassified-reference`”. Re-measured from the payload:
  **61** `unclassified-reference` + **1** `unresolved-references` naming four absent targets
  ```

- **Why it's a problem**: The analyze stage's own disposition made "out-of-shape source path ⇒ `unclassified-reference`" the settled reading; that reading directly contradicted C-306/C-307's dated-record preservation and blocked the first 074 round with 61 + 1 items. The contradiction had to be resolved by an owner ruling and a contract amendment (`abdf9a6df`) after implementation had started. Analyze is the only stage positioned to catch two clauses that prescribe opposite dispositions for the same predicate, and its gate read green.
- **Proposed fix**: Add a cross-clause contradiction pass to `skills/internal/analyze-artifacts` (compare clauses that classify the same predicate into different closed sets) and make the analyze gate record the pass. Source: F1.

### F2 — C-306(c)/C-308's file-level hash rule is not the implemented mixed-carrier criterion

- **Severity**: P1
- **Category**: Documentation
- **Location**: `.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md:59` (C-306(c)) and `:71` (C-308)
- **Evidence** (verbatim quote):

  ```
  (c) 该文件归档前后 sha256 相等
  ```

  ```
  所有 `dated-preserved` 载体 MUST 在运行前后保持 sha256 相等；任一日 dated 文件哈希变化 MUST 使 apply 以 `2` 结束并按原字节恢复。
  ```

- **Why it's a problem**: A **mixed carrier** — `.specify/features/074-goal-team-sdd-unification.md` — carries 10 `live-rewrite` rows and 2 `dated-preserved` rows. Its file sha256 necessarily changes (live section rewritten; measured `b4264897…` → `1032e179…`), so C-306(c) and C-308 are false for its dated rows as written. The engine silently exempts such carriers from the dated hash check (`scripts/python/seal-utils.py:4444`, `- set(live_rows)`), and the test mirrors the exemption (`tests/contract/test_seal_archive_apply.py:246-249`). Preservation is true at row level, not at the clause's file level. Answer to code-review `important` item 1: **agree**; the delivered 074 manifest is schema-valid but one of its own acceptance criteria is not the criterion actually enforced.
- **Proposed fix**: Amend C-306(c) and C-308 to state the mixed-carrier criterion explicitly — dated-only carriers keep a file-level sha; a mixed carrier's dated rows keep their exact line bytes and every live row is listed — and make the engine/test assert that wording. Source: F2.

### F3 — The 074 manifest's merge-manifest ledger lines are stale for 117 of 123 rows

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/074-goal-team-sdd-unification/archive-manifest.json:610` (first stale row; `"line": 1554`); cause at `scripts/python/seal-utils.py:1302-1304` and `:4480-4484`
- **Evidence** (verbatim quote):

  ```
        "carrier": ".specify/specs/074-goal-team-sdd-unification/merge-manifest.json",
        "kind": "live-rewrite",
        "line": 1554
  ```

  The recorded `after` text sits at line 1553 in the archived file; the file's `digest` moved from line 1549 to 3773 because `amended_merge_document` pops and re-adds it. All 117 stale rows still contain their `after` text somewhere; only the locator drifted. Answer to code-review `important` item 2: **agree**; rollback is unaffected because C-110 restores the merge manifest with `git restore`, but the ledger's row locators are not usable.
- **Proposed fix**: Keep the `digest` key in its original position (compute the digest on a copy without reordering), or recompute the merge-manifest ledger rows against the serialized amended document; add a 074 regression assertion that every row's `after` text occupies its recorded `line`. Source: F3.

### F4 — FR-015's post-apply re-verification is asserted, not measured

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/requirements.md:130` (FR-015); `scripts/python/seal-utils.py:4320-4323`, `:4448-4516`
- **Evidence** (verbatim quote):

  ```
  `archive-plan` MUST 报告未解析数；`archive-apply` MUST 在未解析数大于 0 时拒绝；apply 成功后复验 MUST 仍为 0。
  ```

  The manifest candidate is built with the literal `unresolved_after=0`; `_archive_apply_batch` verifies slice hashes and dated-carrier hashes but never re-runs the reference scan; the `already-archived` branch reports the stored `checks.unresolved_after`. The 074 rerun's "zero unresolved" is therefore a plan-time value re-quoted, not a fresh post-apply measurement. Answer to code-review `important` item 3: **agree**; the property holds by construction today, but the required measurement is missing.
- **Proposed fix**: After the manifest write, re-run `_archive_reference_scan` + `_archive_unresolved` over the archived tree; on a non-zero count restore the batch and exit `2`, otherwise record the measured value in `checks.unresolved_after`; add a mutation test that corrupts one rewritten target and asserts the recheck refuses. Source: F4.

### F5 — A P7b engine edit left the `.specify/scripts/` mirror stale until P8

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/test-evidence/final-mirrors.txt:34`; source commit `abdf9a6df`, mirror fix `64931e488`
- **Evidence** (verbatim quote):

  ```
  - P8 入口发现一处**新增**漂移：`.specify/scripts/python/seal-utils.py`（引擎源在 `abdf9a6df` 的 P7b 修订未同步到镜像侧；镜像 sha256 `86548298…` vs 源 `f6acd8b9…`）。
  ```

- **Why it's a problem**: The repo's Two Hats rule requires a source/mirror pair to land in the same change; the P7b contract-convergence package edited only `scripts/python/seal-utils.py`. The drift was found and repaired at P8, so the final state is clean, but the rule was violated for one intermediate package and only a later checkpoint caught it. This is the recurring mirror-drain pattern the project's own lessons list warns about.
- **Proposed fix**: Make every work-package checkpoint run `python3 scripts/python/sync-mirrors.py --check` (and `regen-command-copies.py --check`) before the package is declared closed; record the pair's digest in the package evidence. Source: F5.

### F6 — The state spine's loop-state block never advanced past requirements

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/100-seal-slice-archive.md:4-7`
- **Evidence** (verbatim quote):

  ```
  spine_state: active
  stage: requirements
  attempt: 0
  last_verdict: U0 entry written; requirements dispatching
  ```

  The same file's Stage Records list clarify, checklist and later stages, and the status/heartbeat logs cover implement P1–P8; the loop-state header is the only surface that still says requirements.
- **Why it's a problem**: A reader or an observability tool that trusts the loop-state block sees a run that never left requirements, while the artifact set and the separate status files show a closed implementation. This is exactly the state-spine staleness shape already recorded as REC-095-04 for an earlier feature and REC-099-4 for 099; the pattern recurs here.
- **Proposed fix**: Advance the `<!-- loop-state:begin -->` block on every stage record write (or mark the block as a U0 snapshot and point it at the line registry); add a guard that refuses a stage record whose loop-state did not move. Source: F6.

### F7 — The first round's blocker count was recorded as a single "62 unclassified" figure

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/100-seal-slice-archive/test-evidence/074-archive-round.txt:907-912`
- **Evidence** (verbatim quote):

  ```
  The P7 block was recorded as “62 × `unclassified-reference`”. Re-measured from the payload:
  **61** `unclassified-reference` + **1** `unresolved-references` naming four absent targets
  ```

- **Why it's a problem**: The initial record collapsed two different reason families into one number; the correction is honest and disclosed, but the first reading would have sent a repairer after 62 form problems instead of 61 form problems plus one dangling-target problem. Count-bearing evidence should be derived from the payload fields, not a human tally.
- **Proposed fix**: Record blocker counts as field projections from the JSON payload (`len(conditions)` grouped by `code`), never as a typed total; when a count is re-derived, keep the original and the correction side by side (as the P7b section already does). Source: F7.

### F8 — `DoD Status` stays `pending` after every DoD row is satisfied

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/100-seal-slice-archive/tasks.md:73`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: pending
  ```

- **Why it's a problem**: All 53 rows are `[X]`, DoD-1…DoD-10's checks are recorded in the evidence files, and the sibling features carry `green` (099) or `met` (098). A reader who trusts the DoD line (rather than re-running every check) concludes the feature is not done. The template says to flip it only when every DoD row is satisfied — they are.
- **Proposed fix**: Flip to `**DoD Status**: green` in the closure commit, and have the closure step verify the flip against the DoD checks it just ran. Source: F8.

### F9 — The C-102 `not-evaluated (blocked-by <reason>)` rows are not emitted

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md:14` (C-102); `scripts/python/seal-utils.py:506-516`
- **Evidence** (verbatim quote):

  ```
  因更早的输入缺陷而无法求值的条件 MUST 报告为 `not-evaluated (blocked-by <reason>)`，MUST NOT 计为「未满足」。
  ```

- **Why it's a problem**: On an early input defect (`merge-manifest-missing` / `merge-manifest-invalid`), the engine raises and emits one condition; it never enumerates the later conjuncts as blocked-by rows, and the condition payload schema has no status field to carry them. The contract's promise that "only the first missing item is never reported" is therefore only half implemented.
- **Proposed fix**: Either add a `status` / `blocked_by` field to the condition payload and emit the skipped conjuncts, or narrow C-102's wording to the observable behavior (one named error plus its repair path). Source: F9.

## 4. What Worked — Preserve (Brief)

- The real 074 round is a genuine end-to-end acceptance object: 112 files moved as `R100`, zero deletions, byte-identical hashes, and an idempotent `already-archived` rerun.
- The single manifest validator covers closed key sets at every level, path basis, three closure-arithmetic families and the C-034 digest, and is shared by the read and write paths.
- The C-110 rollback recipe is documented and proven by a skip-a-step negative test that turns each completion check red.
- The dated-record discipline held: `features.md` and `.specify/memory/**` were not touched by the archive batch, and the slice bytes are unchanged.
- The contract-convergence commit (`abdf9a6df`) is a clean example of a fast-fail disposition: contradiction named, owner ruling recorded, contract + requirements + plan + tests + fixture updated together.
- The evidence files carry verbatim commands, exit codes and payloads, so this review could recompute every headline count.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-100-1 — State the mixed-carrier dated criterion exactly** — Target: `.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md` § C-306 / C-308. Change: replace the unconditional file-level sha sentence with the two-case rule (dated-only file hash; mixed carrier preserves dated line bytes and lists every live row), and align `scripts/python/seal-utils.py` and `tests/contract/test_seal_archive_apply.py` with that wording. Source: F2. Expected impact: the contract's mechanical test matches the behavior a future validator will implement.
- **REC-100-8 — Enforce the DoD Status flip at closure** — Target: `.specify/templates/tasks-template.md` § DoD Status and the closure step. Change: make the closure reading flip `pending` to `green` when every DoD check passes, and fail the closure when a satisfied DoD still reads `pending`. Source: F8. Expected impact: the DoD line stops disagreeing with the evidence.

### 5.2 Command Prompt Improvements

- None raised by this feature.

### 5.3 Automation / Script Improvements

- **REC-100-2 — Stabilize the merge-manifest ledger locators** — Target: `scripts/python/seal-utils.py` `amended_merge_document` / `_archive_apply_batch`. Change: preserve the `digest` key position or recompute the merge-manifest rows against the serialized document; add the 074 row-locator regression. Source: F3. Expected impact: every ledger row locates its own carrier line.
- **REC-100-3 — Add the post-apply unresolved re-scan** — Target: `scripts/python/seal-utils.py` `_archive_apply_batch`. Change: re-run the scan over the archived tree after the writes, fail + restore on a non-zero count, and record the measured `unresolved_after`. Source: F4. Expected impact: FR-015's "复验" becomes a measurement, not a literal.
- **REC-100-5 — Emit the C-102 blocked-by rows** — Target: `scripts/python/seal-utils.py` `_archive_manifest_error` and `contracts/archive-actions.contract.md` C-102/C-103. Change: add the blocked-by status to the condition payload and enumerate the un-evaluable conjuncts, or narrow the clause. Source: F9. Expected impact: a refusal report is complete in the sense the contract promises.
- **REC-100-6 — Run the mirror/copy checks at every package checkpoint** — Target: the implement work-package checkpoint (the `sync-mirrors.py --check` / `regen-command-copies.py --check` pair). Change: make the pair a closure prerequisite, with the pair digest recorded in the package evidence. Source: F5. Expected impact: a source edit can no longer close a package with a stale mirror.

### 5.4 Workflow Improvements

- **REC-100-4 — Add cross-clause contradiction detection to analyze** — Target: `skills/internal/analyze-artifacts` (the analyze pass) plus the analyze gate record. Change: compare clauses that classify the same predicate into different closed sets and report the pair before implementation. Source: F1. Expected impact: the C-302/C-306/C-307 class of contradiction is caught at analyze time, not by the real round.
- **REC-100-7 — Advance the state spine and derive counts from payloads** — Target: the sdd-loop driver's stage-record write and the blocker-count recording practice. Change: move the `<!-- loop-state:begin -->` block on every stage record (or label it a U0 snapshot), and project blocker counts from the payload's `code` field. Source: F6, F7. Expected impact: the spine and the evidence agree with the stage timeline; one count cannot collapse two reason families.

### 5.5 Documentation Improvements

- None beyond REC-100-1 (a contract page) and REC-100-8 (the tasks template), which are listed under their owning targets.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-100-1 mixed-carrier dated criterion | `.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md` + engine/test | F2 |
| P1 | REC-100-4 analyze cross-clause contradiction pass | `skills/internal/analyze-artifacts` | F1 |
| P2 | REC-100-2 ledger line stability | `scripts/python/seal-utils.py` | F3 |
| P2 | REC-100-3 post-apply unresolved re-scan | `scripts/python/seal-utils.py` | F4 |
| P2 | REC-100-5 C-102 blocked-by rows | `scripts/python/seal-utils.py` + archive-actions contract | F9 |
| P2 | REC-100-6 mirror checks per package | implement work-package checkpoint | F5 |
| P2 | REC-100-7 state spine + payload-derived counts | sdd-loop driver stage records | F6, F7 |
| P2 | REC-100-8 DoD Status closure flip | `templates/tasks-template.md` + closure step | F8 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly with the standard wording (zero P0, vacuous pass).

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
