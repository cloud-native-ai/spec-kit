# Specification-Driven Development (SDD) Process Review Report: 100-seal-slice-archive

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

**Round**: review round 2 (re-run after review-repair r1, commit `7aa624e4c`). The round-1 report is archived as `review-100.md` and the round-1 code record as `code-review-20261111T062320Z.md`; the two round-1 P1s (F1, F2) are re-verified as resolved in § 3.0, the surviving P2s (F3–F9) are re-confirmed against the current tree, and three new P2s (F10–F12) were exposed by this run.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 100 |
| Requirement Key | 100-seal-slice-archive |
| Requirement Name | /speckit.seal — 分片归档步骤（Seal Slice Archive） |
| Related Feature | 099 Speckit Seal |
| Repository | spec-kit (git worktree `.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive`) |
| Repository URL | `gitee` `git@gitee.com:cloud-native-ai/spec-kit.git`; `github` `git@github.com:cloud-native-ai/spec-kit.git`; `gitlab` `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git`; `origin` is the upstream `git@github.com:github/spec-kit.git` and does not hold these commits |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty, so no remote URL citation resolves. Use the absolute paths below plus `git show 7aa624e4c:<path>` for recovery. |
| Branch | 100-seal-slice-archive |
| Commit SHA | `7aa624e4c8d28f36e0b320f57c558f8f849ab1e8` (short: `7aa624e4c`) |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive` |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder agent — unattended `/speckit.review` round 2 (four segments + Acceptance Reality Check) |
| Environment | Linux 5.10.134 x86_64; Python 3.11.11; git 2.43.5; pytest 8.4.2; tests run through `scripts/bash/run-tests.sh` |
| spec-kit Source Snapshot | this repository @ `7aa624e4c8d28f36e0b320f57c558f8f849ab1e8` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 231 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/requirements.md` | 28 FR / 10 SC / 5 shared strings / 5 clarification rulings for the slice-archive step. |
| plan.md | 275 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/plan.md` | 22-principle Constitution Check, 6 decision tensions, 8 work packages, mirror obligations. |
| research.md | 186 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/research.md` | R-01…R-14 owner file:line measurements. |
| data-model.md | 158 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/data-model.md` | E1–E10 entities and V1–V14 validation rules. |
| quickstart.md | 169 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/quickstart.md` | S-1…S-6 walkthroughs with plan-stage premises. |
| contracts/ (3 files) | 305 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/contracts/` | 40 clauses: archive-actions 16 (C-101…C-116), archive-manifest 12 (C-201…C-212), reference-classification 12 (C-301…C-312); C-306(c)/C-308 carry the carrier-class dated criterion. |
| feature-ref.md | 124 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/feature-ref.md` | FR 28/28 and SC 10/10 delivery maps. |
| tasks.md | 368 | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/100-seal-slice-archive/.specify/specs/100-seal-slice-archive/tasks.md` | 53 rows / 8 work packages / 40 green claims, all `[X]`; `DoD Status` still `pending`. |
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
| 7 | Analyze closes 37 C/H with 0 open | `f821daf83`; `test-evidence/analyze-merged-2026-11-11.md` | none at the gate, but the cross-clause C-302/C-306/C-307 contradiction survived (F1, round 1) |
| 8 | Setup baselines frozen | `8974dc8ef` | none |
| 9 | P1 engine six-action set; P2 manifest-aware discovery; P3 archive-plan; P4 archive-apply | `21f30f445`, `efe5f4d3f`, `4b62d1677` + `b85f7afd3`, `595d78a86` | none |
| 10 | P6 command/skill surface; P5 owner-page revisions | `be41fb2ec`, `24d920bd0` | none |
| 11 | First real 074 round refused: 61 `unclassified-reference` + 1 `unresolved-references` | `2fe5661e5`; `test-evidence/074-archive-round.txt` § P7 (lines 1–899) | **deviation**: a contract-level contradiction blocked the real acceptance round |
| 12 | Owner ruling converges C-302 by carrier class (dated loose forms → `dated-preserved`) | `abdf9a6df`; 074-archive-round.txt § P7b | **deviation**: a mid-implementation contract revision, not planned at the plan stage |
| 13 | 074 archive batch: 112 `R100` moves, 19 M carriers, 1 A manifest | `a2c1f2bf7`; same evidence file § T043 | none |
| 14 | Reproducibility + rollback drill; P8 suite/mirror/quickstart closure | `f3bd72866`, `64931e488`, `8f4e4276e` | **deviation**: the P7b engine edit left the `.specify/scripts/` mirror stale until P8 (F5) |
| 15 | Review round 1: four segments + ARC; P1 2 / P2 7; code segment `not-evaluated`, gate allow | `970a3dadc`; round-1 report archived as `review-100.md` | none (the transition was judged legal; the bound Feature 099 already read `Ready for Review`, so no status write) |
| 16 | Review-repair r1 (user-directed, P1-only): C-306(c)/C-308 carrier-class wording + section-level engine guard + 2 tests; analyze `F` cross-clause rule | `7aa624e4c`; `test-evidence/review-repair-dispositions-r1-2026-11-11.md`, `review-repair-r1-red-first.txt`, `review-repair-r1-suite.txt` | Corrective follow-up after review; red-first evidence recorded, source/mirror pair byte-identical |
| 17 | Review round 2 (this run): P1 anchors re-verified, 074 replay, smoke and affected suite re-run, code record re-created, ARC re-run | this `review.md`, `code-review.md`, `test-evidence/review-r2-smoke.txt`, `test-evidence/review-r2-074-replay.json` | One friction: the `receipt` step silently re-resolved the trunk merge base without `--spec` and refused at exit 2 on an unrelated binary (F11); re-run with `--spec` wrote the correct block |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 0 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 10 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 1 |
| Automation / Scripts | 6 |
| Workflow | 2 |
| Documentation | 1 |

Round-1 findings F1 (P1) and F2 (P1) are resolved and re-verified (§ 3.0); they are not counted above.

**P0 validation status**: No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `48e273d7395d949656099c596161ac9210687cfa` | the resolved diff base |
| Head commit | `7aa624e4c8d28f36e0b320f57c558f8f849ab1e8` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec .specify/specs/100-seal-slice-archive` |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 361 / 27 / 334 / 0 | copied field by field from the record's coverage-receipt block |
| Segment verdict | `not-evaluated` | 334 legal skips earn no coverage credit (generated mirrors/command copies, non-code artifacts, fixture data); zero `blocking` entries |
| Gate verdict | `allow` | `report --summary --file` → `{"record":".specify/specs/100-seal-slice-archive/code-review.md","counts":{"blocking":0,"important":2,"suggestion":1,"nitpick":0,"question":0,"praise":1},"blocking_entries":0,"gate":"allow"}`, exit 0 |
| Reason, when one applies | not-evaluated: 334 of 361 changed files were legal skips; 27 code/surface files judged (round-1's 26 plus `skills/internal/analyze-artifacts/SKILL.md`); gap 0 | the receipt's own skip reasons |
| Uncommitted scope | `> **未提交范围（未评审）**: 15 个未提交路径未计入本次评审对象（.specify/specs/100-seal-slice-archive/review.md, .specify/templates/gitignore-specify-template, .specify/memory/exec-quant/records/20261111T061002731745Z-c16c0110.json, .specify/memory/exec-quant/records/20261111T061003197722Z-9a5863cc.json, .specify/memory/exec-quant/records/20261111T061003661020Z-337c8cb3.json, .specify/memory/exec-quant/records/20261111T061004127027Z-0b8e8637.json, .specify/memory/feedback/20261111T061010Z-skill-review-feature-quality.md, .specify/memory/feedback/20261111T061010Z-skill-review-sdd-process.md, .specify/memory/feedback/20261111T061010Z-speckit-review.md, .specify/memory/session/20261111T061002Z-run-determination-skill-review-sdd-process-r20261111t060957z.md, .specify/memory/session/20261111T061002Z-run-determination-speckit-review-r20261111t060957z-b100-revi.md, .specify/memory/session/20261111T061003Z-run-determination-skill-code-review-r20261111t060957z-b100-r.md, .specify/memory/session/20261111T061003Z-run-determination-skill-review-feature-quality-r20261111t060.md, .specify/specs/100-seal-slice-archive/review-100.md, .specify/specs/100-seal-slice-archive/test-evidence/review-r2-smoke.txt）；本回执不对该范围给出任何结论。` — Note: `git status` also lists `.specify/memory/feedback/20261111T061010Z-skill-code-review.md` and this run's later `test-evidence/review-r2-074-replay.json`, which the disclosure's suffix filter masks (F12). | the record's disclosure line |
| Record | `.specify/specs/100-seal-slice-archive/code-review.md` | written (triage `run`) |
| Archive | `.specify/specs/100-seal-slice-archive/code-review-20261111T062320Z.md` | round-1 record, rotated by `start` |

The two `important` items are answered in §3 F3 and F4 (agreement plus a reason); `important` never blocks the transition, and no `blocking` entry exists. Client capture did not run: this is a framework-hat repository (spec-kit source), so the conclusion names the hat verdict as its basis instead of a capture token — `.specify/shared/definitions/dogfooding-definitions.md` § 2.1.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, research.md, data-model.md, quickstart.md, contracts/, feature-ref.md, tasks.md, verification.md | union of the standard spec-stage set and `plan.md` § Project Structure (which additionally names research.md and feature-ref.md) |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `pass` | all expected members exist and carry their required sections; the round-1 contract finding (F2) is resolved (§ 3.0); one P2 record-status finding (F8) remains |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | `.specify/specs/100-seal-slice-archive/tasks.md` | 73 | none | `**DoD Status**: pending` survives 53/53 closed rows and a satisfied DoD-1…DoD-10 set (F8). |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `48e273d7395d949656099c596161ac9210687cfa` | the resolved diff base |
| Head commit | `7aa624e4c8d28f36e0b320f57c558f8f849ab1e8` | the run-start `HEAD` |
| Base source | `feature-first-commit` | `git-delta-review.sh base --spec .specify/specs/100-seal-slice-archive` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py tests/integration/test_seal_archive_round.py -q` | recorded verbatim from `verification.md` `smoke_command=` |
| Smoke exit code | 0 | re-measured this session: `54 passed in 6.64s` |
| Smoke evidence path | `.specify/specs/100-seal-slice-archive/test-evidence/review-r2-smoke.txt` | exists, non-empty, carries the same command and `54 passed` |
| Scope and regression verdict | Scope is the declared surface: 361 changed files = 204 A + 45 M + 112 R100 and zero D. Relative to round 1 (354 = 199 A + 43 M + 112 R100) the delta is the review pair (+2 A), the r1 repair's 3 evidence records (+3 A) and 2 newly modified files (`skills/internal/analyze-artifacts/SKILL.md` + its mirror). The 112 R100 are the two 074 slices moved byte-identically, the 19 M are the declared live carriers, and the one A manifest is unchanged. Regression: the affected 12-file suite reads 146 passed / 2 failed, both failures the pre-existing baseline reds `test_c5_gate_budget_is_unchanged_by_the_owner_document` (final-failed.txt:5) and `test_live_plan_identifies_both_slices_from_the_split_record` (final-failed.txt:158); the recorded full-suite comparison still holds (`test-evidence/final-suite.txt`, `comm -13` empty against the 217-entry baseline); the 074 round replays idempotently this session (`already-archived`, `unclassified=0`, unresolved `0/0`, mixed carrier 10 `live-rewrite` + 2 `dated-preserved`). Three P2 code defects remain (F3, F4, F9). | `test-evidence/review-r2-smoke.txt`, `test-evidence/review-r2-074-replay.json`, `test-evidence/final-failed.txt`, `test-evidence/final-suite.txt` |
| Segment verdict | `pass` | no P0/P1 in the delta; the r1 repair is reproduced; remaining findings are P2 |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | `.specify/specs/074-goal-team-sdd-unification/archive-manifest.json` | 610 | none | 117 of the 123 merge-manifest ledger rows carry a stale `line` after the digest relocation (F3). |
| P2 | `scripts/python/seal-utils.py` | 4342 | none | `unresolved_after` is passed as a literal 0 and never re-measured after the apply batch (F4). |
| P2 | `scripts/python/seal-utils.py` | 506 | none | The C-102 `not-evaluated (blocked-by <reason>)` rows are not emitted on an early input defect (F9). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/features/099-speckit-seal.md` (the bound feature detail) |
| `final_path` record, copied verbatim (7/7) | pass 4 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 4 | `python3 .specify/scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/100-seal-slice-archive --feature-detail .specify/features/099-speckit-seal.md --json`, never recomputed here |
| Comparison verdict | `agree` | checker verdict `accept`; claimed status `Ready for Review`; the pass bucket is non-zero (4) |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

**Status transition judgement.** The one transition this run judges is `Implemented → Ready for Review`. Its four conjunctive gate conditions (owner: `.specify/templates/feature-details-template.md` § Canonical Status State Machine) all hold: (a) every deferred `[~]` task is resolved — `deferred_tasks=` is empty and the ARC task record reads closed 53 / deferred 0 / open 0; (b) review evidence is produced — this report plus the current `code-review.md`; (c) the current code-segment record carries zero `blocking` entries (`report --summary --file` → `gate=allow`); (d) no `final`-path criterion sits in `blocked` / `deferred` / `fail` — all four read `pass`. Because the bound feature detail already claims `Ready for Review` (carried by Feature 099's review round 2), this run performs no status write: the transition is legal and already in force, and the claim is neither advanced nor regressed. The code segment's `not-evaluated` verdict is disclosed on both carriers and does not block.

## 3. Findings (Problems & Improvement Targets)

### 3.0 Round-1 findings re-verified as resolved

- **F1 (P1) — resolved.** The analyze pass now carries the cross-clause contradiction rule at `skills/internal/analyze-artifacts/SKILL.md:122-127`:
  > **F — cross-clause contradictions.** Two clauses that impose mutually exclusive criteria on the same object MUST be reported as one `inconsistency` finding naming both clauses and the shared object — for example, one clause requires an artifact's whole-file hash to remain unchanged while another requires a section of that same file to be rewritten, or two clauses classify the same predicate into different closed sets.
  The runtime mirror `.specify/skills/internal/analyze-artifacts/SKILL.md` is byte-identical (`sync-mirrors.py --check --only skills/internal/analyze-artifacts` → `ok (3 files, byte-identical)`).
- **F2 (P1) — resolved.** C-306(c) (`contracts/reference-classification.contract.md:59`) now judges `(c) 载体字节不变，按载体类判定——纯 dated 载体…整文件 sha256 相等；混合载体…其 dated 章节（按 C-304 的 H2 章节边界切分）字节逐字节相等`, and C-308 (`:71`) states the same two-case rule with the `write-failed` consequence. The engine implements it: `mixed_dated_sections` (`scripts/python/seal-utils.py:1261`) snapshots a mixed carrier's dated H2 blocks byte for byte, `_archive_apply_batch` compares that region after the live rewrites (`:4470`, `:4518-4522`) and restores on drift. Two tests cover the permitted and rejected cases (`tests/contract/test_seal_archive_apply.py:277`, `:309`); red-first evidence shows `2 failed` before the engine hunk and `2 passed` after (`test-evidence/review-repair-r1-red-first.txt`), and both pass in this round's re-run. Real tree: the 074 replay reads `unclassified=0`, unresolved `0/0`, and the mixed carrier `.specify/features/074-goal-team-sdd-unification.md` carries exactly 10 `live-rewrite` + 2 `dated-preserved` rows (`test-evidence/review-r2-074-replay.json`).

### F3 — The 074 manifest's merge-manifest ledger lines are stale for 117 of 123 rows

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/074-goal-team-sdd-unification/archive-manifest.json:610` (first stale row; `"line": 1554`); cause at `scripts/python/seal-utils.py:1322-1324` and `:4127`
- **Evidence** (verbatim quote):

  ```
        "carrier": ".specify/specs/074-goal-team-sdd-unification/merge-manifest.json",
        "kind": "live-rewrite",
        "line": 1554
  ```

  The recorded `after` text sits at line 1553 in the archived file; the file's `digest` moved from line 1549 to 3773 because `amended_merge_document` pops and re-adds it (`amended.pop("digest", None)` / `amended["digest"] = digest_after`). All 117 stale rows still contain their `after` text somewhere; only the locator drifted. Answer to code-review `important` item 1: **agree**; rollback is unaffected because C-110 restores the merge manifest with `git restore`, but the ledger's row locators are not usable. Open as REC-100-2.
- **Why it's a problem**: A ledger whose `line` cannot locate its own row defeats the C-110 rollback recipe's row-level audit and any future row-level rewrite; the drift is systematic (117/123), not an edge case.
- **Proposed fix**: Keep the `digest` key in its original position (compute the digest on a copy without reordering), or recompute the merge-manifest ledger rows against the serialized amended document; add a 074 regression assertion that every row's `after` text occupies its recorded `line`.

### F4 — FR-015's post-apply re-verification is asserted, not measured

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/requirements.md:130` (FR-015); `scripts/python/seal-utils.py:4342-4343`, `:4448-4516`
- **Evidence** (verbatim quote):

  ```
  `archive-plan` MUST 报告未解析数；`archive-apply` MUST 在未解析数大于 0 时拒绝；apply 成功后复验 MUST 仍为 0。
  ```

  The manifest candidate is built with the literal `0, 0` (`_archive_manifest_candidate(..., runtime, 0, 0, head)`); `_archive_apply_batch` verifies slice hashes and dated-carrier bytes but never re-runs the reference scan; the `already-archived` branch reports the stored `checks.unresolved_after`. The 074 rerun's "zero unresolved" is therefore a plan-time value re-quoted, not a fresh post-apply measurement. Answer to code-review `important` item 2: **agree**; the property holds by construction today, but the required measurement is missing. Open as REC-100-3.
- **Why it's a problem**: The clause promises a post-write verification step; the engine's only post-write checks are hashes that cannot detect a reference that no longer resolves.
- **Proposed fix**: After the manifest write, re-run `_archive_reference_scan` + `_archive_unresolved` over the archived tree; on a non-zero count restore the batch and exit `2`, otherwise record the measured value in `checks.unresolved_after`; add a mutation test that corrupts one rewritten target and asserts the recheck refuses.

### F5 — A P7b engine edit left the `.specify/scripts/` mirror stale until P8

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/test-evidence/final-mirrors.txt:34`; source commit `abdf9a6df`, mirror fix `64931e488`
- **Evidence** (verbatim quote):

  ```
  - P8 入口发现一处**新增**漂移：`.specify/scripts/python/seal-utils.py`（引擎源在 `abdf9a6df` 的 P7b 修订未同步到镜像侧；镜像 sha256 `86548298…` vs 源 `f6acd8b9…`）。
  ```

- **Why it's a problem**: The repo's Two Hats rule requires a source/mirror pair to land in the same change; the P7b contract-convergence package edited only `scripts/python/seal-utils.py`. The drift was found and repaired at P8, so the final state is clean, but the rule was violated for one intermediate package and only a later checkpoint caught it. This is the recurring mirror-drain pattern the project's own lessons list warns about. Open as REC-100-6.
- **Proposed fix**: Make every work-package checkpoint run `python3 scripts/python/sync-mirrors.py --check` (and `regen-command-copies.py --check`) before the package is declared closed; record the pair's digest in the package evidence.

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

  The same file's Stage Records list clarify, checklist and later stages, and the status/heartbeat logs cover implement P1–P8; the loop-state header is the only surface that still says requirements. Re-confirmed unchanged in round 2. Open as REC-100-7.
- **Why it's a problem**: A reader or an observability tool that trusts the loop-state block sees a run that never left requirements, while the artifact set and the separate status files show a closed implementation. This is exactly the state-spine staleness shape already recorded as REC-095-04 for an earlier feature and REC-099-4 for 099; the pattern recurs here.
- **Proposed fix**: Advance the `<!-- loop-state:begin -->` block on every stage record write (or mark the block as a U0 snapshot and point it at the line registry); add a guard that refuses a stage record whose loop-state did not move.

### F7 — The first round's blocker count was recorded as a single "62 unclassified" figure

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/specs/100-seal-slice-archive/test-evidence/074-archive-round.txt:907-912`
- **Evidence** (verbatim quote):

  ```
  The P7 block was recorded as “62 × `unclassified-reference`”. Re-measured from the payload:
  **61** `unclassified-reference` + **1** `unresolved-references` naming four absent targets
  ```

- **Why it's a problem**: The initial record collapsed two different reason families into one number; the correction is honest and disclosed, but the first reading would have sent a repairer after 62 form problems instead of 61 form problems plus one dangling-target problem. Count-bearing evidence should be derived from the payload fields, not a human tally. Open as REC-100-7.
- **Proposed fix**: Record blocker counts as field projections from the JSON payload (`len(conditions)` grouped by `code`), never as a typed total; when a count is re-derived, keep the original and the correction side by side (as the P7b section already does).

### F8 — `DoD Status` stays `pending` after every DoD row is satisfied

- **Severity**: P2
- **Category**: Documentation
- **Location**: `.specify/specs/100-seal-slice-archive/tasks.md:73`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: pending
  ```

- **Why it's a problem**: All 53 rows are `[X]`, DoD-1…DoD-10's checks are recorded in the evidence files, and the sibling features carry `green` (099) or `met` (098). A reader who trusts the DoD line (rather than re-running every check) concludes the feature is not done. The template says to flip it only when every DoD row is satisfied — they are. Open as REC-100-8.
- **Proposed fix**: Flip to `**DoD Status**: green` in the closure commit, and have the closure step verify the flip against the DoD checks it just ran.

### F9 — The C-102 `not-evaluated (blocked-by <reason>)` rows are not emitted

- **Severity**: P2
- **Category**: Automation
- **Location**: `.specify/specs/100-seal-slice-archive/contracts/archive-actions.contract.md:14` (C-102); `scripts/python/seal-utils.py:506-516`
- **Evidence** (verbatim quote):

  ```
  因更早的输入缺陷而无法求值的条件 MUST 报告为 `not-evaluated (blocked-by <reason>)`，MUST NOT 计为「未满足」。
  ```

- **Why it's a problem**: On an early input defect (`merge-manifest-missing` / `merge-manifest-invalid`), the engine raises and emits one condition (`_archive_manifest_error` builds exactly one `_condition`); it never enumerates the later conjuncts as blocked-by rows, and the condition payload schema has no status field to carry them. The contract's promise that "only the first missing item is never reported" is therefore only half implemented. Open as REC-100-5.
- **Proposed fix**: Either add a `status` / `blocked_by` field to the condition payload and emit the skipped conjuncts, or narrow C-102's wording to the observable behavior (one named error plus its repair path).

### F10 — The analyze command template still counts "seven detection passes" while the skill enumerates eight

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `templates/commands/analyze.md:56`; skill enumeration at `.specify/skills/internal/analyze-artifacts/SKILL.md:116`
- **Evidence** (verbatim quote):

  ```
  The skill owns the entire workflow: context initialization, progressive-disclosure artifact loading, semantic models, the seven detection passes (including same-author detection delegation and the stale-copy decision test), severity assignment, ...
  ```

  while the skill says:

  ```
  Eight passes (A duplication · B ambiguity · C underspecification · D constitution alignment
  · E coverage gaps · F inconsistency · G feature relevance & accuracy · I decision tension
  records) plus one checklist pass (H)
  ```

- **Why it's a problem**: The command template is the thin entry every analyze run reads first; a count that disagrees with the skill's own enumeration misstates the pass set — pass I (decision tension records) is unmentioned, and the r1 repair extended pass F without the template noticing. Pre-existing drift, exposed by this feature's repair and left in place by it.
- **Proposed fix**: Update the sentence to the skill's own count (eight plus the checklist pass), or replace the enumeration with a pointer to § 5 of the skill so the count has one owner. Open as REC-100-9.

### F11 — `receipt` silently re-resolves the diff base when `--spec` is omitted

- **Severity**: P2
- **Category**: Automation
- **Location**: `skills/internal/code-review/scripts/git-delta-review.sh` (`cmd_receipt` → `resolve_range`); non-interactive path step 4 in `skills/internal/code-review/SKILL.md`
- **Evidence** (verbatim quote, this run's observation):

  ```
  $ git-delta-review.sh receipt --review-file .specify/specs/100-seal-slice-archive/code-review.md ...
  行数无法测量 (binary): .specify/anchoring/command-logic-as-classified-skills/summary/assets/wbs.png
  不可量测的数字字段意味着不写块 (C-41 / V16)
  exit=2
  ```

  The record written by `start --spec` carried `base=48e273d73…`, but the receipt re-resolved to the trunk merge base `926836e0f…` (measured: `git-delta-review.sh base` without `--spec` → `base=926836e0fc931bfdbd531f45b0b27e3715e84a0c`, `base_source=trunk-merge-base`) and therefore saw an unrelated binary from another feature. Re-running with `--spec .specify/specs/100-seal-slice-archive` wrote the correct block (`changed_files=361`, `base=48e273d73…`).
- **Why it's a problem**: Step 4 of the skill's own non-interactive path is written as `receipt --review-file <record>` — no `--spec`. When the operator follows that line, the receipt silently uses a different range than the record's own header; had the wrong range contained no binary file, the block would have been written with a different `changed set`/`judged set` than the header records. The record is the run's single source for its range; the receipt should read it, not guess a new one.
- **Proposed fix**: Make `receipt` read `base=` / `head=` from the record's existing range header (or from the block written by `start`) and refuse on a mismatch with an explicit `--spec`; make `--spec` mandatory in step 4 otherwise; add a test that a receipt on a record created with `--spec` cannot silently resolve to the trunk. Open as REC-100-10.

### F12 — The uncommitted-scope exclusion masks any path ending in `code-review.md`

- **Severity**: P2
- **Category**: Automation
- **Location**: `skills/internal/code-review/scripts/git-delta-review.sh` (`uncommitted_scope`)
- **Evidence** (verbatim quote):

  ```
  git status --porcelain 2>/dev/null \
      | grep -vE '^\?\? \.specify/review/|code-review(-[0-9]{8}T[0-9]{6}Z)?\.md$' \
      || true
  ```

  This run's disclosure names 15 paths, but `git status` also lists the untracked `.specify/memory/feedback/20261111T061010Z-skill-code-review.md`, which the suffix `code-review…\.md$` filters out although it is not a review record.
- **Why it's a problem**: The exclusion exists to keep the run's own record out of its disclosure; a suffix match also hides unrelated files (`*-code-review.md`, e.g. a feedback entry) and silently under-reports unreviewed scope — the one direction a disclosure must never err in.
- **Proposed fix**: Anchor the exclusion to the record's exact location (the `<spec-dir>/code-review.md` and its timestamped archives, matched as full paths), not a filename suffix; add a test with an unrelated tracked-name file that must stay in the disclosure. Open as REC-100-11.

## 4. What Worked — Preserve (Brief)

- The real 074 round is a genuine end-to-end acceptance object: 112 files moved as `R100`, zero deletions, byte-identical hashes, and an idempotent `already-archived` rerun — re-confirmed in this round.
- The single manifest validator covers closed key sets at every level, path basis, three closure-arithmetic families and the C-034 digest, and is shared by the read and write paths.
- The C-110 rollback recipe is documented and proven by a skip-a-step negative test that turns each completion check red.
- The dated-record discipline held: `features.md` and `.specify/memory/**` were not touched by the archive batch, and the slice bytes are unchanged.
- The contract-convergence commit (`abdf9a6df`) and the r1 repair (`7aa624e4c`) are clean fast-fail dispositions: contradiction named, owner ruling recorded, contract + requirements + plan + tests + fixture updated together; the repair carries red-first evidence and a byte-identical source/mirror pair.
- The evidence files carry verbatim commands, exit codes and payloads, so this review could recompute every headline count.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-100-1 — State the mixed-carrier dated criterion exactly** — Target: `.specify/specs/100-seal-slice-archive/contracts/reference-classification.contract.md` § C-306 / C-308. Change: replace the unconditional file-level sha sentence with the two-case rule (dated-only file hash; mixed carrier preserves dated section bytes and lists every live row), and align `scripts/python/seal-utils.py` and `tests/contract/test_seal_archive_apply.py` with that wording. Source: F2. Expected impact: the contract's mechanical test matches the behavior a future validator will implement. **Status: resolved 2026-11-11 in `7aa624e4c`** — contract C-306(c)/C-308 rewritten, the engine's section-level guard added, both new tests red-first then green, mirror pair byte-identical.
- **REC-100-8 — Enforce the DoD Status flip at closure** — Target: `.specify/templates/tasks-template.md` § DoD Status and the closure step. Change: make the closure reading flip `pending` to `green` when every DoD check passes, and fail the closure when a satisfied DoD still reads `pending`. Source: F8. Expected impact: the DoD line stops disagreeing with the evidence. **Status: open.**

### 5.2 Command Prompt Improvements

- **REC-100-9 — One owner for the analyze pass count** — Target: `templates/commands/analyze.md` § the skill-workflow sentence. Change: replace "the seven detection passes" with the skill's own enumeration (eight passes plus the checklist pass), or point at `.specify/skills/internal/analyze-artifacts/SKILL.md` § 5 so the count has one owner. Source: F10. Expected impact: the command entry stops misstating the pass set. **Status: open.**

### 5.3 Automation / Script Improvements

- **REC-100-2 — Stabilize the merge-manifest ledger locators** — Target: `scripts/python/seal-utils.py` `amended_merge_document` / `_archive_apply_batch`. Change: preserve the `digest` key position or recompute the merge-manifest rows against the serialized document; add the 074 row-locator regression. Source: F3. Expected impact: every ledger row locates its own carrier line. **Status: open.**
- **REC-100-3 — Add the post-apply unresolved re-scan** — Target: `scripts/python/seal-utils.py` `_archive_apply_batch`. Change: re-run the scan over the archived tree after the writes, fail + restore on a non-zero count, and record the measured `unresolved_after`. Source: F4. Expected impact: FR-015's "复验" becomes a measurement, not a literal. **Status: open.**
- **REC-100-5 — Emit the C-102 blocked-by rows** — Target: `scripts/python/seal-utils.py` `_archive_manifest_error` and `contracts/archive-actions.contract.md` C-102/C-103. Change: add the blocked-by status to the condition payload and enumerate the un-evaluable conjuncts, or narrow the clause. Source: F9. Expected impact: a refusal report is complete in the sense the contract promises. **Status: open.**
- **REC-100-6 — Run the mirror/copy checks at every package checkpoint** — Target: the implement work-package checkpoint (the `sync-mirrors.py --check` / `regen-command-copies.py --check` pair). Change: make the pair a closure prerequisite, with the pair digest recorded in the package evidence. Source: F5. Expected impact: a source edit can no longer close a package with a stale mirror. **Status: open.**
- **REC-100-10 — Make the receipt read its record's range** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` `cmd_receipt` and `skills/internal/code-review/SKILL.md` § 非交互路径 step 4. Change: read `base=` / `head=` from the record (the range `start` wrote) and refuse on a mismatch, or require `--spec`; add the trunk-divergence test. Source: F11. Expected impact: a receipt can no longer be written over a different range than its record. **Status: open.**
- **REC-100-11 — Anchor the uncommitted-scope exclusion to record paths** — Target: `skills/internal/code-review/scripts/git-delta-review.sh` `uncommitted_scope`. Change: match the exact record paths instead of a `code-review…\.md$` suffix; add a test that an unrelated `*-code-review.md` file stays disclosed. Source: F12. Expected impact: the disclosure can no longer silently drop unreviewed scope. **Status: open.**

### 5.4 Workflow Improvements

- **REC-100-4 — Add cross-clause contradiction detection to analyze** — Target: `skills/internal/analyze-artifacts` (the analyze pass) plus the analyze gate record. Change: compare clauses that classify the same predicate into different closed sets and report the pair before implementation. Source: F1. Expected impact: the C-302/C-306/C-307 class of contradiction is caught at analyze time, not by the real round. **Status: resolved 2026-11-11 in `7aa624e4c`** — the `F — cross-clause contradictions` rule landed in the skill (source + mirror byte-identical).
- **REC-100-7 — Advance the state spine and derive counts from payloads** — Target: the sdd-loop driver's stage-record write and the blocker-count recording practice. Change: move the `<!-- loop-state:begin -->` block on every stage record (or label it a U0 snapshot), and project blocker counts from the payload's `code` field. Source: F6, F7. Expected impact: the spine and the evidence agree with the stage timeline; one count cannot collapse two reason families. **Status: open.**

### 5.5 Documentation Improvements

- None beyond REC-100-1 (a contract page), REC-100-8 (the tasks template) and REC-100-9 (the analyze command page), which are listed under their owning targets.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P2 | REC-100-2 ledger line stability | `scripts/python/seal-utils.py` | F3 |
| P2 | REC-100-3 post-apply unresolved re-scan | `scripts/python/seal-utils.py` | F4 |
| P2 | REC-100-5 C-102 blocked-by rows | `scripts/python/seal-utils.py` + archive-actions contract | F9 |
| P2 | REC-100-6 mirror checks per package | implement work-package checkpoint | F5 |
| P2 | REC-100-7 state spine + payload-derived counts | sdd-loop driver stage records | F6, F7 |
| P2 | REC-100-8 DoD Status closure flip | `templates/tasks-template.md` + closure step | F8 |
| P2 | REC-100-9 analyze pass count single owner | `templates/commands/analyze.md` | F10 |
| P2 | REC-100-10 receipt reads its record's range | `skills/internal/code-review/scripts/git-delta-review.sh` | F11 |
| P2 | REC-100-11 exact-path disclosure exclusion | `skills/internal/code-review/scripts/git-delta-review.sh` | F12 |

Round-1's P1 rows (mixed-carrier criterion, analyze contradiction pass) are resolved; REC-100-1 and REC-100-4 carry their resolution evidence in § 5.

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
