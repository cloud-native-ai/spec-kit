# SDD Process Review Report: 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

**Round**: review round 2 (re-run after review-repair r1, commit `55dd6d61d`). The round-1 report is archived as `review-099.md`; its P0 (F1) and two P1s (F2, F3) are re-verified as resolved in this round (§ 3.0), and the surviving P2s (F4–F10) are re-confirmed against the current tree.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 099 |
| Requirement Key | 099-speckit-seal |
| Requirement Name | Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写） |
| Related Feature | 099 Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写） |
| Repository | spec-kit |
| Repository URL | (no remote contains these commits; remotes: gitee/github/gitlab forks; `origin` is upstream) |
| Reachability of COMMIT_SHA | UNRESOLVABLE — `git branch -r --contains HEAD` is empty. Cite absolute paths and recover files with `git show 55dd6d61d:<path>`; no blob URL can resolve. |
| Branch | 099-speckit-seal |
| Commit SHA | 55dd6d61dddd2ed529cbbd61dc3c3e966b470988 (short: 55dd6d61d) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal (git worktree; the repository root is /storage/project/cloud-native-ai/spec-kit) |
| Review Date | 2026-11-11 |
| Reviewer (Agent) | Qoder review agent (round 2; fresh session, no authorship of this feature's artifacts in this session) |
| Environment | Linux 5.10.134-15.2.al8.x86_64, bash, Python 3.11.11, pytest 8.4.2, git 2.43.5 |
| spec-kit Source Snapshot | this repository at 55dd6d61d (self-hosted `.specify/` runtime; `shared/` mirror check: 111 files byte-identical) |
| Constitution | v1.19.2 (the 1.19.1 carrier amendment between plan and tasks is F8) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 250 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/requirements.md | 28 FR / 9 SC (final 6, supporting 3) / RS-001…003 / STR-001…003 + clarifications |
| plan.md | 333 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/plan.md | Constitution Check 22 Pass, 6 decision tensions, 12 verified premises, P1–P9 execution model |
| tasks.md | 374 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/tasks.md | 51 rows, all `[X]`, 0 open / 0 deferred; 10 DoD + 5 gates |
| verification.md | 76 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/verification.md | smoke triple + SC-001…009 all `pass` + final_path 6/6 accept + empty deferred set |
| data-model.md | 216 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/data-model.md | E1–E14 entities, V1–V16 validation rules |
| quickstart.md | 196 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/quickstart.md | S-1…S-9 walkthroughs |
| research.md | 228 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/research.md | R-01…R-21, all measured |
| feature-ref.md | 115 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/feature-ref.md | FR 28/28 and SC 9/9 mapping |
| contracts/ (4 files, 448 lines) | 448 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/contracts/ | C-001…C-045 across engine, merge-back, records, status |
| feature detail | 69 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features/099-speckit-seal.md | prior claim `Implemented`; round-2 review entry added by this run |
| code-review record (this run) | this run | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review.md | six-level findings + coverage receipt 485/5/480/0 |
| code-review archive | 1841 | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review-20261110T190504Z.md | round-1 code record (451/29/422/0, one blocking) |
| review-repair r1 evidence | 8 files | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/test-evidence/ | f1-red-first, f3-supersede-claims, 074-round-repair, t050-replay, required-suites, suites, dispositions |
| round-2 evidence | 4 files | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/test-evidence/ | review-r2-suites / review-r2-074-replay / review-r2-arc / review-r2-code-receipt |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Driver U0 entry writes the line state spine | `.specify/state/099-speckit-seal.md:5-14` (`stage: requirements`, `attempt: 0`) — the block is never advanced through the rest of the run | Yes — the spine stays at the U0 snapshot (F7) |
| 2 | requirements stage | e0e239709 → 594832030 (run records) → 404dcbde6 (close-out) | None |
| 3 | clarify stage | 0131e24d2 → 4951b5967 → c998f2a43 | None |
| 4 | plan stage | 749b613c0 → f7959ccc1 → 32406eddd | None |
| 5 | Out-of-band constitution amendment between plan and tasks | d4a52bd38 `docs(constitution): amend Principle VII carrier to verification.md (1.19.1)` — touches `.specify/constitution.md`, `shared/guidelines/better-harness.md`, its mirror and `tests/contract/test_fast_fail_discipline.py`; no 099 task row names it; the user ruling is recorded only in the constitution's Sync Impact Report | Yes — a write outside the slice's declared task rows (F8) |
| 6 | tasks stage | 4f1ef128f → 1afd6821f → b2f7ef451 → 2fd48f346 → cf7fb8f13 | None |
| 7 | checklist stage | 105d22c30 → 2f56a6de7 → 3b79af6e2 → bf576e58e | None |
| 8 | analyze round 1 + repair r1 | 026dd2aa8 (12 findings: 0 CRITICAL / 7 HIGH) → ff253f8e2 (requirements/plan/tasks/contracts repairs) | Prescribed (analyze before implement) |
| 9 | analyze round 2 + repair r2 | 6d4859316 (1 HIGH residual) → 484a9930c | Prescribed |
| 10 | analyze round 3 → PASS | 64120b3a8 (`0 CRITICAL / 0 HIGH / 5 MEDIUM / 1 LOW`) | None (gate admits MEDIUM) |
| 11 | implement P1–P7 | 1f88f8821 → 93843c567 → 34f2a40fc → 32359073c → a9eb3f990 → 2939a408d → a2b07c584 → 3f2a05cba | None |
| 12 | 074 round, first attempt | 1b3e422a8 (merge round) → cbf55b89c (adjudication) → b0cb4e6f4 (row states); terminal blocked with B1–B4 | Prescribed; the round exposed engine defects |
| 13 | P8b engine repair + 074 rerun | 8460536ca (three root-cause fixes + replay) → 611b8d982 (rerun adjudication) → 5e233678a (suite reading) | Corrective follow-up within P8; documented red-first |
| 14 | P9 polish + P9b deferral closure | 6aaa15019 (T045–T050) → 34b6d9866 (T041, T050 closed; verification rerun) | None |
| 15 | Review round 1 → refusal | efd1f9266 (review.md + code-review.md; `blocking-unresolved`) → d8a165739 (run determination, exec-quant, feedback) → 99af8cb3b (close-out receipt) | Correct per the unattended disposition: halt-and-report, status stays `Implemented` |
| 16 | Review-repair r1 (user-directed) | 55dd6d61d — F1 (P0): seal reads each slice's original review/code-review records; F2 (P1): FR-006 / C-013 / C-044 converge; F3 (P1): superseded rows retain `[green:]` claims; 4 new F1 tests + 1 F3 test | Corrective follow-up after the review; red-first evidence in `test-evidence/f1-red-first-20261111.txt`, `f3-supersede-claims-20261111.txt` |
| 17 | Review round 2 (this run) | re-verified F1/F2/F3; seal family 137 passed; 074 replay twice byte-identical (exit 2, writes 0); coverage 099 45/45, residual 0; ARC `accept`; transition judged and applied | None |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 0 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 7 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 2 |
| Documentation | 3 |

Round-1 findings F1 (P0), F2 (P1) and F3 (P1) are resolved and re-verified (§ 3.0); they are not counted above.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base |
| Head commit | 55dd6d61dddd2ed529cbbd61dc3c3e966b470988 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec .specify/specs/099-speckit-seal` |
| Renderer mode | renderer: text | the code record's header marker (no TTY, non-interactive agent run) |
| Changed / judged / skipped / gap files | 485 / 5 / 480 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | not-evaluated | the receipt's own derivation: 480 legal skips earn no coverage credit, so the four-value set lands on `not-evaluated`, not `pass`; zero `blocking` entries |
| Gate verdict | allow | `report --summary --file` exits 0 with `blocking_entries=0`; one `important` item is answered in § 3 F9 |
| Reason, when one applies | The five judged files are this round's repair-touched code paths (`scripts/python/seal-utils.py`, `scripts/python/validate-tasks.py`, `scripts/python/account-clause-coverage.py`, `tests/contract/test_clause_coverage.py`, `tests/contract/test_seal_seal.py`). The 480 skips carry legal reasons only: `generated` (agent command copies and `.specify/` mirrors), `non-code-file` (docs, spec artifacts, dated records) and `size-guard-focus-not-reviewed` (code files outside this round's repair focus; their full reading is the archived round-1 record). | `test-evidence/review-r2-code-receipt-20261111.txt` |
| Uncommitted scope | > **未提交范围（未评审）**: 2 个未提交路径未计入本次评审对象（.specify/memory/trigger/index.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt）；本回执不对该范围给出任何结论。 | disclosed, never concluded over; the same sentence lives in the record |
| Record | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review.md | written because the triage value is `run` |
| Archive | /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/code-review-20261110T190504Z.md | the round-1 record, archived by `start` before this record was written |

**The round-1 blocking entry is resolved.** `scripts/python/seal-utils.py:2594` now reads each slice's original `review.md` / `code-review.md` alongside the parent pointer view; the real 074 replay emits `p0-unresolved: 074b-nested-governance:F1 (line 115 of .specify/specs/074b-nested-governance/review.md)` from the engine itself, with exit 2 and zero writes. Six-level counts in this round's record: blocking 0 · important 1 · suggestion 2 · nitpick 0 · question 0 · praise 2.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | union of the standard spec-stage set and `plan.md` § Project Structure (which additionally names research.md, feature-ref.md) |
| Coverage line | 9 / 9 (missing: none) | present members / expected members |
| Missing members | none | — |
| Segment verdict | pass | complete and traceable after the r1 repair; four P2 narrative/warning rows remain (F4, F5, F6, F10) |

F2 is resolved in this round's tree: `requirements.md:132` (FR-006) now states that a split spec's current record set includes the merged parent view **and** each slice's original review records, that the parent view is a pointer view carrying no finding block, and that the pointer view does not narrow the P0/`blocking` reading surface; `requirements.md:223` (Clarifications) uses the same wording; `contracts/merge-back.contract.md:35-37` (C-013) states the same reading-surface rule; `contracts/records-and-boundaries.contract.md:119-120` (C-044) names the slice's original review code section as the review carrier for a slice P0. The repaired engine behavior matches all four statements.

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P2 | .specify/features.md | 102 | none | The 099 row's Last Updated cell still carries the P9 disclosure `T050 [~]` and the T041 deferral after 34b6d9866 closed both; tasks.md and verification.md record zero deferred (F4). |
| P2 | .specify/specs/099-speckit-seal/plan.md | 208-209 | none | The plan says the 074 round's write face is the parent spec dir plus the two slice requirements annotations, contradicting contract C-023, which also authorizes factory-doc reference fixes (F5). |
| P2 | .specify/specs/099-speckit-seal/verification.md | 23 | none | The SC-001 note cites the P8b targeted suite as `130 passed`, while the recorded evidence file reads `133 passed` and this round's seal family reads `137 passed` (F6). |
| P2 | .specify/specs/099-speckit-seal/tasks.md | 116, 182, 183, 208 | none | Four `green-cross-phase` warnings: clause claims run backwards against row order, so those rows cannot leave their contract green at their own phase (F10). |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | b3da3a26dfba209057f65c2b17962b9516812c39 | the resolved diff base (`feature-first-commit`) |
| Head commit | 55dd6d61dddd2ed529cbbd61dc3c3e966b470988 | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec …` |
| Smoke command | `bash scripts/bash/run-tests.sh tests/integration/test_seal_074_round.py -q` | recorded verbatim from `verification.md` `smoke_command=` |
| Smoke exit code | 0 | re-measured this session: 5 passed in 6.33s (fresh capture at `.specify/.tmp/review-099-r2/smoke-seal-074-round.txt`) |
| Smoke evidence path | .specify/specs/099-speckit-seal/notes/quickstart-run.md | exists and non-empty; the feature's smoke record |
| Scope and regression verdict | The r1 repair is root-caused and reproduced: the seal family reads 137 passed (P8b baseline 133 + 4 new F1 tests); the 074 replay is byte-identical across two runs (exit 2, sole `p0-unresolved` + `closure-input-defect`, writes 0, 47/47 + 074a/074b hash sets unchanged); 099 clause coverage is ok with 45/45 claimed and 0 beyond baseline; the 074 lane reads claimed=144 with zero `074-*` names beyond its baseline; validate-tasks is 0 error / 4 warning, validate-requirements 0/0; mirror and command-copy checks exit 0. One P2 correctness gap (F9) remains. | `test-evidence/review-r2-suites-20261111.txt`, `test-evidence/review-r2-074-replay-20261111.txt`, `test-evidence/f3-supersede-claims-20261111.txt`, `test-evidence/t050-replay-repair-r1-20261111.txt` |
| Segment verdict | pass | no P0/P1 in the delta; the F1 fix is verified end to end; one P2 (F9) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | scripts/python/seal-utils.py | 2472 | none | `_write_seal_batch` does not restore the in-flight file when `write_text` raises after truncation; C-005 requires every written file restored, and the guard test covers only an open() permission failure (F9). |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Implemented | the bound feature detail's claim, copied at check time |
| `final_path` record, copied verbatim (7/7) | pass 6 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 6 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/099-speckit-seal --json`, never recomputed here (payload: `test-evidence/review-r2-arc-20261111.json`) |
| Comparison verdict | agree | `verdict=accept` with `every_final_path_pass=true`, `no_open_rows=true`, `smoke_record_pass=true`, `status_row_per_criterion=true`; tasks closed 51, deferred 0, open 0 |
| Failed condition, on refusal | none | — |
| Fixed item, on refusal | none | — |

The ARC does not refuse this transition. No condition was waived; no `F-ACCEPTANCE` item fires.

### 2.5 Status Transition — `Implemented → Ready for Review`

The four conjunctive conditions owned by `templates/feature-details-template.md` § Canonical Status State Machine, judged once after all segments and after both records are on disk:

1. **Every deferred (`[~]`) task resolved or explicitly waived** — satisfied. `tasks.md` has 0 `[~]` rows; `verification.md` `deferred_tasks=` is empty; the ARC task record reads closed 51 / deferred 0 / open 0. T041 and T050 were closed by 34b6d9866; the 67-name coverage residual they disclosed now reads 0 after the r1 repair (F3 resolution).
2. **Review evidence produced** — satisfied. This `review.md` and the current `code-review.md` are on disk.
3. **The current code-segment record contains no `blocking` entry** — satisfied. `report --summary --file` returns `gate=allow`, `blocking_entries=0`, exit 0. The round-1 blocking entry (F1) is repaired and re-verified; the record is `not-evaluated` only because of legal skips, which the state machine's rule 8 explicitly treats as non-blocking.
4. **No `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver** — satisfied. The ARC record reads pass 6, total 6, with the other buckets zero.

**Verdict: the transition is legal and is applied by this run** — `features.md` and the feature detail move to `Ready for Review`. The one `important` code item is answered: **F9 — agreed; the atomic-batch gap is real, remains open as REC-099-5, and does not block** (the six-level `important` level never blocks; the six-level and P0/P1/P2 families are not mapped).

## 3. Findings (Problems & Improvement Targets)

### 3.0 Resolved since the previous review (re-verified this round)

| ID | Original severity | Category | Repair | This round's verification |
|----|-------------------|----------|--------|---------------------------|
| F1 | P0 | Automation / Scripts | `55dd6d61d`: `evaluate_seal` reads each slice's original `review.md` / `code-review.md` in addition to the parent pointer view; finding ids are qualified `<slice>:F1`; summary and `unaccounted` aggregate per source; the receipt names every record read and each waiver's carrier; the C-044 waiver form stays two-carrier (slice record code section + feature detail) | `test-evidence/f1-red-first-20261111.txt` (4 failed pre-fix → 4 passed); `test-evidence/review-r2-074-replay-20261111.txt` (two byte-identical runs, exit 2, writes 0, hashes unchanged, `p0-unresolved` named by the engine); seal family 137 passed (`test-evidence/review-r2-suites-20261111.txt`) |
| F2 | P1 | Documentation | `55dd6d61d`: FR-006 (`requirements.md:132`), its clarification (`:223`), C-013 (`contracts/merge-back.contract.md:35-37`) and C-044 (`contracts/records-and-boundaries.contract.md:119-120`) now state one fact: the merged parent view is a pointer view, and it never narrows the P0/`blocking` reading surface | The four statements were read side by side; the repaired engine behavior matches them; validate-requirements 0 error / 0 warning |
| F3 | P1 | Workflow | `55dd6d61d`: `validate-tasks.py` parses `[green:]` claims inside a `## Superseded pre-split record` block into **retained claims** (same `_strip_claims` implementation, current-plan checks skipped); the owner rule lives in `shared/workflow/acceptance-hardening.md`; `account-clause-coverage.py` consumes the single parser | `test-evidence/f3-supersede-claims-20261111.txt` (claimed 0→3, uncovered 3→0 on one hermetic fixture); `test_superseded_pre_split_rows_retain_their_claims` passes; 099 coverage ok / 45 / 0 beyond; 074 lane claimed=144 with zero `074-*` beyond baseline (`test-evidence/t050-replay-repair-r1-20261111.txt`) |

### F4 — The registry row and the dated implement entry still disclose T050 `[~]` / T041 deferrals that no longer exist

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features.md L102 (Last Updated cell); /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/features/099-speckit-seal.md L22 (dated P9 entry under `## Latest Review`)
- **Evidence** (verbatim quote):

  ```
  披露：T050 `[~]`——074 回合按 C-022 把父级 57 条拆前行 green 认领转为记录，遗留 67 条 074 父契约未覆盖名逐名归因（非本 spec 缺口，待用户裁定）；T041 保留 P8 历史延后记录
  ```

  and the current authoritative records: `tasks.md:222` `- [X] T041 …`, `tasks.md:240` `- [X] T050 …`, `verification.md` `deferred_tasks=` (empty), and the r1 replay reading `uncovered_beyond_baseline=0`.
- **Why it's a problem**: the registry cell still tells a reader that T041/T050 are deferred and that a 67-name residual remains, while the authoritative task, verification and coverage records now read closed / zero. This round's status flip appends a review entry to the same cell but does not rewrite the stale sentence, so the contradiction remains visible; a reader checking the gate condition "every deferred task resolved" sees conflicting statements. (The feature detail's sentence is inside a dated P9 record; keeping history is correct, but the cell needs a superseding current statement.)
- **Proposed fix**: refresh the 099 registry Last Updated cell so the current claim names the r1 closure facts (T041/T050 closed; 67→0) and keeps the P9 disclosure only as a dated historical sentence; point the feature detail's next claim at the same facts rather than repeating the stale numbers. Source: F4; carried from round 1.

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
- **Why it's a problem**: the plan omits the third write face C-023 explicitly authorizes (factory-doc reference fixes); the round actually wrote 18 source references plus their mirrors (`test-evidence/074-factory-resolutions.md` § A/B). A reader of the plan would believe those writes are out of scope.
- **Proposed fix**: replace the plan sentence with a pointer to C-023, or restate all three write faces and cite C-023 as the owner. Source: F5; carried from round 1.

### F6 — The P8b suite reading is cited as 130 passed while the recorded evidence says 133, and this round reads 137

- **Severity**: P2
- **Category**: Documentation
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/specs/099-speckit-seal/verification.md L23
- **Evidence** (verbatim quote):

  ```
  P8b targeted suite 130 passed on the seal contract+integration set
  ```

  vs the evidence file `test-evidence/p8b-suite-20261111.txt:13` (`133 passed in 8.38s`) and this round's family reading (`137 passed in 8.34s`, `test-evidence/review-r2-suites-20261111.txt`).
- **Why it's a problem**: the final reading was extended from 9 to 10 files (adding `test_seal_merge_determinism.py`) in 5e233678a, moving 130 → 133; the r1 repair added four tests, moving it to 137. The verification note was never updated, so a reader checking the note against its own evidence sees a number that does not match.
- **Proposed fix**: update the SC-001 note to the current 137 with its evidence path, or state the progression 130 (9 files) → 133 (10 files) → 137 (r1). Source: F6; carried from round 1.

### F7 — The driver's state spine is stale at the U0 requirements snapshot

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/state/099-speckit-seal.md L5–L14 (loop-state block; repository root, outside the worktree)
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
- **Why it's a problem**: after the line completed requirements → … → review round 2, the machine-readable block still says the run is in the requirements stage with attempt 0. Any orchestrator or resume path that reads this block sees a snapshot from the first minutes of the run; the prose sections below it were also never advanced. The review dispatch had to supply the real state from conversation context.
- **Proposed fix**: have the driver's stage transitions rewrite the loop-state block (stage, attempt, last_verdict, timeline) or explicitly mark the block as a U0-only snapshot and point to the live line registry as the authority. Source: F7; carried from round 1.

### F8 — An out-of-band constitution amendment lands between plan and tasks without a task row

- **Severity**: P2
- **Category**: Workflow
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/constitution.md L16–L27 (the 1.19.1 Sync Impact Report); commit d4a52bd38 in the feature range
- **Evidence** (verbatim quote):

  ```
  - Version change: 1.19.0 → 1.19.1 (PATCH; carrier correction, 2026-11-10)
  - Modified principles: VII. Workflow Gates — the Pre-Status-Flip Gate's status-line carrier is corrected from `verification.log` to `verification.md` ... User ruling (2026-11-10): amend the constitution to the framework carrier rather than create a second record surface.
  ```
- **Why it's a problem**: the amendment changed `.specify/constitution.md`, `shared/guidelines/better-harness.md` (+ mirror) and `tests/contract/test_fast_fail_discipline.py` between the plan and tasks stages; no 099 task row authorizes it, and the feature's plan/tasks do not mention it. The user ruling exists, but it is recorded only inside the constitution's own report, so a reader of the feature artifacts cannot account for the write. (T014 later bumps the constitution to 1.19.2 for the Sealed narrative and does have a task row; this finding is about the separate 1.19.1 amendment.)
- **Proposed fix**: record out-of-band user-ruled amendments as a dated row in the feature's plan or tasks (with the ruling reference), or require the manage-constitution flow to emit a linked task row when it runs inside a feature's timeline. Source: F8; carried from round 1.

### F9 — `_write_seal_batch` leaves a partially written in-flight file unrestored on a mid-write failure

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py L2460–L2481
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
- **Proposed fix**: restore the current path in the exception handler as well (or append the path to `written` before writing), and add a fault-injection test that fails between truncation and write completion. **Answer (required for the code segment's `important` item): agreed — the gap is real, remains open as REC-099-5, and does not block the transition.** Source: F9; carried from round 1.

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
- **Proposed fix**: re-cut the clause partition between the paired rows or move the earlier clause's row ahead of its consumer; add the warning count to the tasks-stage close-out reading so it is dispositioned rather than merely printed. Source: F10; carried from round 1.

## 4. What Worked — Preserve (Brief)

- The r1 repair is root-caused with red-first evidence: the four F1 tests fail on the pre-fix engine and pass after it; the F3 fixture flips claimed 0→3 / uncovered 3→0 on one hermetic corpus.
- The 074 replay is genuinely reproducible: two independent seal runs are byte-identical (exit 2, writes 0), the engine itself now names `074b-nested-governance:F1`, and every parent/slice file hash is unchanged.
- The F3 fix keeps one parser: retained claims flow through the same `validate-tasks.py` `_strip_claims` implementation that every active row uses; the accountant consumes the single output.
- The coverage receipt refuses to treat skips as coverage credit: this round's 5/480/0 honestly lands the segment on `not-evaluated` instead of claiming a clean pass over 485 files.
- Mirror discipline: `sync-mirrors.py --check` (111 shared files byte-identical) and `regen-command-copies.py --check` both exit 0.
- The seal family reads 137/137 green and 099 clause coverage reads 45/45 with zero names beyond baseline.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-099-6** — Target: `templates/tasks-template.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/templates/tasks-template.md). Change: add a tasks-stage close-out obligation to disposition every `green-cross-phase` warning (re-cut the partition or record why the order is intentional), so the warning is actionable rather than printed. Source: F10. Expected impact: the per-row green claim stays a truthful checkpoint signal. **Status: open.**

### 5.2 Automation / Script Improvements

- **REC-099-1** — Target: `scripts/python/seal-utils.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py). Change: carry an aggregate P0/blocking summary into the merged views and/or make the P0 gate follow the pointer lines into the slice records; add a split-parent fixture whose slice review carries an unwaived P0 and assert `p0-unresolved` exit 1 with zero writes. Source: F1, F2. Expected impact: the seal P0 condition is no longer vacuous for the feature's primary split scenario. **Status: resolved 2026-11-11 in 55dd6d61d** — the engine reads the slice records, and the nine new assertions (4 F1 tests) plus the real 074 replay verify it.
- **REC-099-5** — Target: `scripts/python/seal-utils.py` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py). Change: restore the in-flight path on a mid-write failure (or register it as written before the write) and add a fault-injection test. Source: F9. Expected impact: C-005's atomic-batch promise holds on every failure class, not only open() failures. **Status: open.**

### 5.3 Workflow Improvements

- **REC-099-2** — Target: `shared/workflow/acceptance-hardening.md` / `contracts/merge-back.contract.md` in the declaring feature (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/shared/workflow/acceptance-hardening.md). Change: state once whether a superseded pre-split record retains its `[green:]` claim for coverage accounting, and make the accountant consume that form. Source: F3. Expected impact: split merges stop producing a 67-name residual that every future merge must re-explain. **Status: resolved 2026-11-11 in 55dd6d61d** — the owner rule and the retained-claim parser landed; the 074 lane reads zero `074-*` names beyond baseline.
- **REC-099-4** — Target: `skills/external/sdd-loop-driver/scripts/line-registry.py` and the driver's state-spine writer (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/skills/external/sdd-loop-driver/). Change: advance the loop-state block on every stage transition, or mark it as a U0-only snapshot with the live registry named as the authority. Source: F7, F8. Expected impact: resume and audit paths read the real stage instead of a first-minute snapshot. **Status: open.**

### 5.4 Documentation Improvements

- **REC-099-3** — Target: `.specify/features.md`, `.specify/features/099-speckit-seal.md`, `.specify/specs/099-speckit-seal/plan.md`, `.specify/specs/099-speckit-seal/verification.md` (absolute supplement: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/.specify/). Change: refresh the deferral disclosure after P9b, point the plan's round write-face sentence at C-023, and update the P8b suite number to the current reading with its evidence path. Source: F4, F5, F6. Expected impact: the status carriers and plan agree with the authoritative task/verification/coverage records. **Status: open.**

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P2 | Atomic batch restores the in-flight file | `scripts/python/seal-utils.py` | F9 |
| P2 | Status-spine advancement | driver state writer | F7, F8 |
| P2 | Artifact narrative refresh | feature registry/detail/plan/verification | F4, F5, F6 |
| P2 | Green-cross-phase disposition | `templates/tasks-template.md` | F10 |

The round-1 P0 and P1 rows (split-parent P0 gate, superseded-claim retention) are closed; their RECs are resolved.

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target needed an `external` marker.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens remain anywhere in the report.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: this round raises no P0. The prior round's P0 (F1) was confirmed by an independent read-only validator then; this round re-verifies its repair with red-first test evidence and a live two-run replay, so the P0-validation history is not vacuous and no unvalidated P0 was carried forward.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
