# Specification-Driven Development (SDD) Process Review Report: Speckit 框架可视化（Speckit Framework Visualization）

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 087 |
| Requirement Key | 088-speckit-visualization |
| Requirement Name | Speckit 框架可视化（Speckit Framework Visualization） |
| Related Feature | 087 — same id; bound at `/speckit.clarify` (Clarification Q1) |
| Repository | spec-kit |
| Repository URL | `git@gitee.com:cloud-native-ai/spec-kit.git`, `git@github.com:cloud-native-ai/spec-kit.git`, `git@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (SSH remotes; `origin` is the UPSTREAM `github/spec-kit` and does **not** contain these commits) |
| Reachability of COMMIT_SHA | UNRESOLVABLE: `git branch -r --contains HEAD` is empty — no remote branch carries `0df6f6c6`. Cite absolute paths plus `git show <sha>:<path>`; all SSH remotes cannot render `blob/` web URLs |
| Branch | 088-speckit-visualization |
| Commit SHA | 0df6f6c6740480b821a1aab793c865e15673e67c (short: 0df6f6c6) |
| Repo Root (absolute) | /storage/project/cloud-native-ai/spec-kit |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | SDD Review Coordinator (`/speckit.review`, run r20261106T040353Z-087a) |
| Environment | Linux 5.10.134-15.2.al8.x86_64 x86_64 · bash · Python 3.11.11 · git-delta absent (`renderer: text`) |
| spec-kit Source Snapshot | same repository @ 0df6f6c6 (self-hosting: framework source and client runtime in one tree) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 521 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/requirements.md | 22 FR / 10 SC, 5 runtime-stack rows, 15 assumptions |
| plan.md | 342 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/plan.md | Constitution Check 19/19, Decision Tensions T-001/T-002, 10 execution premises, mirror obligations |
| research.md | 242 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/research.md | RO-01…RO-15 measured readings, unknowns U-1…U-5 |
| data-model.md | 221 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/data-model.md | 7 entities E1–E7, invariants INV-01…INV-12 |
| quickstart.md | 331 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/quickstart.md | 8 executable scenarios A–H |
| contracts/ (6 files) | 827 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/contracts/ | 52 clauses C-01…C-52 across 6 families |
| tasks.md | 313 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/tasks.md | 50 rows T001–T046 + T051–T054, all `[x]` |
| verification.md | 148 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/verification.md | baseline + smoke record + 10 SC status rows with ladders |
| feature-ref.md | 161 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/feature-ref.md | 28-row delivered-path roster, FR→artifact map |
| checklists/ | 157 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/checklists/ | requirements-quality checklist, 60 items |
| code-review.md | 592 | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/code-review.md | code-segment record, 166/166 files with receipt |

## 1. Process Execution Timeline

Reconstructed from 34 commits touching the spec directory plus the whole-tree commits between `56f3f881` and `0df6f6c6`. Commits exist and are largely stage-grouped, so the timeline is commit-traced except where marked.

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | requirements authored | 52b2d5a6 | none |
| 2 | Goal + requirements checkpoint | 7f9012ee | none |
| 3 | clarify: Feature binding + 5 adjudications | 6e969caa, 56f3f881 | none |
| 4 | plan + Phase 1 design artifacts | 2b24d24e | none |
| 5 | temporary Team created; plan checkpoint | b2e3b447 | none |
| 6 | tasks generated | 47fd6d07, 424d970c | none |
| 7 | checklist generated; checkpoint | efe24cff, 1b12a2f9 | none |
| 8 | analyze round 1 → 3-stage repair wave | a7eaaa4a, 142ecc4d, 644ebf35, 852e0843 | none |
| 9 | analyze round 2 → repair wave | 8b4b2c7e, b2c044e0, 3ec54975, 799083f2 | none |
| 10 | analyze round 3 → repair wave | 428e5a22, f61fec7d, e14b10a2, 0d97dfd3 | none |
| 11 | **out-of-band commit after the analyze checkpoint** | 0d97dfd3, message: "close the round-3 tasks findings F-11/F-12/G-02"; the diff also carries `agents/sdd-analysis-worker.agent.md` `display-color: teal → cyan` and its four per-tool mirrors | **yes** — an undeclared, unreviewed edit riding a "close the analyze findings" commit; see F7 |
| 12 | analyze round 4 → gate-green | c047740d, ce1a37fd, f7acc23f | none |
| 13 | implement Part 1 (setup + foundation) | 650b70f3 | none |
| 14–18 | implement Parts 2–6 (US1–US4 + Polish) + E3 rows | 62676f38, 3f58e3d3, c0fd01ac, 59180541, a289f756, d82063f5, f74cc7e6, 930adc2f | none |
| 19 | implement checkpoint; status landed `Blocked` with the closure reason | 0df6f6c6; `.specify/memory/features/088.md` § Status Tracking | none — `Blocked` is the honest landing; see F4 for what the report does *not* say |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 6 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 1 |
| Automation / Scripts | 3 |
| Workflow | 4 |
| Documentation | 1 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 24cb4edcc53db3cfc86f574e5e6d627c78b2ca08 | the resolved diff base |
| Head commit | 0df6f6c6740480b821a1aab793c865e15673e67c | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec …` |
| Renderer mode | renderer: text | the code record's header marker (git-delta absent, non-interactive) |
| Changed / judged / skipped / gap files | 166 / 166 / 0 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | blocked | one `important` item is a new regression on a pre-existing contract assertion; three `important` items in total |
| Gate verdict | pass | `report --summary --file` exits 0: `blocking_entries=0`, `gate=allow`, with three `important` answered in § 2.1 below |
| Reason, when one applies | none | `not-applicable` / `not-evaluated` do not apply (triage = `run`) |
| Uncommitted scope | Disclosed: the working tree carries uncommitted changes under `.specify/memory/` (session, exec-quant, feedback records from earlier runs) and this run's own `review.md` / `code-review.md` / `test-evidence/review*`. None of them is part of the reviewed range; no conclusion here covers them. | disclosed, never concluded over |
| Record | /storage/project/cloud-native-ai/spec-kit/.specify/specs/088-speckit-visualization/code-review.md | written because the triage value is `run` |
| Archive | none | first code-segment run for this feature |

**The three `important` items, each answered (the gate requires an answer, not a fix).**

1. `scripts/python/status-digest.py:1434` — RO-12's path test is `if Path(value).suffix:`, so any token with a suffix passes. **Agreed.** The proposition cannot distinguish a declared triplet from an arbitrary token; the fix belongs with the feature's next iteration (a closed-suffix check plus a negative fixture).
2. `scripts/python/status-digest.py:1147` — RO-04 reads `--roster` paths through `_read_text`, which prefixes `REPO_ROOT`, so an out-of-repo roster is reported as `unreadable`. **Agreed, and it bites the feature's own unblock path**: SC-002's `SC-002_unblock=` says "create a roster after this feature, then re-run `validate-roster.py` over it", and a roster created outside this repository would be judged unreadable by the guard's population read.
3. `agents/sdd-analysis-worker.agent.md:11` — `display-color: teal → cyan` with no requirement or task row. **Agreed.** It is undeclared scope inside the reviewed delta, traced to commit 0d97dfd3.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md | union of the standard spec-stage set and `plan.md` § Project Structure (which lists no further named artifact beyond these plus `research.md`, `feature-ref.md`, `checklists/`, `test-evidence/`) |
| Coverage line | 7 / 7 | present members / expected members |
| Missing members | none | — |
| Segment verdict | blocked | one P1 (acceptance honesty) plus supporting P2s; see the rows below |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | .specify/specs/088-speckit-visualization/tasks.md | 21 | none | **DoD-5 as written ("Every `final`-path success criterion (SC-001…SC-007) reads `pass`") is false by measurement**, and the row is declared "void, not unmet" in a note underneath it — the Definition of Done survives in the file in a falsified form instead of being recomputed from the counts. An artifact reader running `grep DoD-5` gets a red bullet with a paragraph explaining why it is allowed. |
| P2 | .specify/specs/088-speckit-visualization/test-evidence/success-criteria.txt | 39 | none | The `supporting`-path row for SC-009 records verdict `**not-measured**` while `verification.md` records `SC-009_status=blocked`; the file explains the mapping but the two vocabularies now disagree on the one row that matters for a reader checking honesty. |
| P2 | .specify/specs/088-speckit-visualization/verification.md | 39 | none | `post_change_commit=working tree on d82063f5 (the Part 6 commit is the one this log ships with)` — a `working tree` reading for a field the schema expects to be a commit id. The Part 6 commit is `f74cc7e6`; the value names neither HEAD nor that commit. |
| P2 | .specify/specs/088-speckit-visualization/tasks.md | 189 | none | T042's green clause points at `contracts/ownership-map.contract.md#C-52` while the row's own body writes `§ 3 point 4` and `test-evidence/success-criteria.txt § 2 and § 3`; the numbering inside that evidence file runs `1,2,3,4,5` under a heading that § 1 also uses, so "§ 3 point 4" resolves only after the reader notices § 3 is a numbered prose list, not a section. |

**Traceability reading** (the dimension, stated as its result rather than as prose). All 22 `FR-…` reach at least one task row; 44 of 50 rows carry `[green: <contract clause>]`; the six that do not are the setup/baseline rows (T002, T005), the red-first test rows whose green is their implementation row (T006), the pointer/mirror rows (T010, T025), and the closure row (T046). The `SC-…` links concentrate in row 46: T042 names SC-001, SC-007, SC-008, SC-009, SC-010 (twice) and **omits SC-002, SC-003, SC-004, SC-005, SC-006**. Traceability from SC to evidence therefore runs through `test-evidence/success-criteria.txt` and `verification.md`, not through `tasks.md`, which is a legal route but means a `tasks.md`-only reader sees five of ten criteria linked.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | 24cb4edcc53db3cfc86f574e5e6d627c78b2ca08 | the resolved diff base (`feature-first-commit`) |
| Head commit | 0df6f6c6740480b821a1aab793c865e15673e67c | the run-start `HEAD`, fixed for the run |
| Base source | feature-first-commit | `git-delta-review.sh base --spec …` |
| Smoke command | `python3 skills/internal/create-team/scripts/validate-roster.py .specify/specs/088-speckit-visualization/fixtures/us1-compliant-fixture/team.md && python3 scripts/python/status-digest.py --action digest --cap 5 && python3 scripts/python/status-digest.py --action guard --structure 087-supervision --run-stamp r20261106T090000Z-us2f --sub-flow 087-supervision--r20261106T090000Z-us2f--worker=$PWD/.specify/specs/088-speckit-visualization/fixtures/us2-supervision-fixture/above-threshold --threshold-row 'Manifest stuck at ``in-progress``' && python3 scripts/python/status-digest.py --action guard --flow-sample .specify/specs/088-speckit-visualization/test-evidence/us4-scope-sample.txt --roster-baseline .specify/specs/088-speckit-visualization/test-evidence/roster-baseline.txt --line-set .specify/specs/088-speckit-visualization/test-evidence/us2-line-set.lines.txt --supervision-line-set .specify/specs/088-speckit-visualization/test-evidence/us4-supervision-capture.txt --carrier .specify/specs/088-speckit-visualization/test-evidence/us2-execution-modes.txt --run-record .specify/specs/088-speckit-visualization/test-evidence/us2-execution-modes.txt` | recorded verbatim (copied from `verification.md` `smoke_command=`, re-run this session) |
| Smoke exit code | 0 | the integer the command returned (re-measured: 1 s wall clock) |
| Smoke evidence path | .specify/specs/088-speckit-visualization/test-evidence/review-smoke/smoke-run.txt | this run's capture; the feature's own record is `test-evidence/smoke.txt` (153 lines, non-empty) |
| Scope and regression verdict | one new red against the pre-change tree (`test_i11`), plus undeclared scope in the delta; every new suite green | see the rows below |
| Segment verdict | blocked | one P1 (regression) + one P2 (scope) |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | tests/contract/test_fast_fail_discipline.py | 1561 | none | `test_i11_channel_two_mirrors_and_per_tool_copies` is **green at 56f3f881 and red at HEAD** — a new failure introduced by this delta, not an inherited one. It is absent from `baseline-failed.txt` (27 names) and from the feature's `cl-01-closure.txt` node-id comparison, which covers only the six C-51 suites, so nothing in the delivered evidence records it. Cause: every per-tool agent copy carries the clause interval with the un-rewritten `` `shared/guidelines/fast-fail.md` `` while the assertion expects `rewrite_paths(owner)`; the newly registered `reporter` copy makes the 17-member `FACTORY_PRESETS` loop reach it for the first time. Evidence: `test-evidence/review-smoke/baseline-reproduction.txt`. |
| P2 | agents/sdd-analysis-worker.agent.md | 11 | none | `display-color: teal → cyan`, propagated to four per-tool copies, with no requirement row and no task row; it enters the delta through 0d97dfd3 (see § 1 row 11). |

**Regression detail.** `tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline` is also red (`gate total moved from the frozen 23 to 27`), but it is red at 56f3f881 with the identical numbers, so it is inherited, not introduced. Targeted readings: 156 passed across the five new suites; 131 passed / 2 failed across the three edited suites; the full suite was **not** run (review-stage budget).

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | Blocked | `.specify/memory/features.md` row 087 and `.specify/memory/features/088.md` § Status Tracking |
| `final_path` record, copied verbatim (7/7) | pass 5 · blocked 0 · deferred 0 · partial 2 · fail 0 · unknown 0 · total 7 | `scripts/python/closure-acceptance-check.py --json`, never recomputed here |
| Comparison verdict | agree | `block` against a `Blocked` claim |
| Failed condition, on refusal | none (the claim is already `Blocked`; the checker's own reason codes are `final-path-not-pass` for SC-001 and SC-002) | — |
| Fixed item, on refusal | none | — |

## 3. Findings (Problems & Improvement Targets)

### F1 — the CC-11 renderer writes an un-rewritten clause interval into every per-tool agent copy

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `src/specify_cli/__init__.py` (`rewrite_paths`) as consumed by the per-tool agent renderer; observed in `.qoder/agents/sdd-analysis-worker.agent.md` line 50
- **Evidence** (verbatim quote):

  ```
  - 判据、两份封闭清单与上送件形态的唯一真源:`shared/guidelines/fast-fail.md`。
  ```

  while `rewrite_paths(owner)` renders the same line as

  ```
  - 判据、两份封闭清单与上送件形态的唯一真源:`.specify/shared/guidelines/fast-fail.md`。
  ```

- **Why it's a problem**: `tests/contract/test_fast_fail_discipline.py::test_i11` asserts that every per-tool copy's clause interval equals `rewrite_paths(owner)`. Rendering the whole per-tool tree writes the un-rewritten form into **all 17** copies, so the assertion can only pass for a tree that was rendered once by a renderer applying the rewrite — and the next whole-tree render silently reverts it. The feature's own author hit this and worked around it by rendering one file at a time (`notes/red-first-evidence.md` § "Correction to the paragraph above"), which is a per-run local fix for a framework-level defect, and the tree at HEAD still carries the un-rewritten form.
- **Proposed fix**: make the per-tool agent renderer call `rewrite_paths` on the clause interval (the command template renderer already does), or make `test_i11` render the expected value through the same entry point the tree was produced by — and add a whole-tree render → `test_i11` round-trip test so the two cannot diverge again.

### F2 — the status-digest guard and the roster guard cannot tell "outside the population" from "unreadable" when the path is outside the repository

- **Severity**: P1
- **Category**: Automation / Scripts
- **Location**: `scripts/python/status-digest.py` line 1147 (`_read_text` usage in `proposition_ro_04`)
- **Evidence** (verbatim quote):

  ```
  text = _read_text(Path(path_text))
  ```

  with `_read_text` defined as

  ```
  path = REPO_ROOT / rel_path
  ```

- **Why it's a problem**: `--roster` is the documented way to name an in-population roster for one run (`reporting-obligations.contract.md` C-04). Passing a path outside the repository — which is exactly what SC-002's own documented unblock step produces, "create a roster through the framework's team-creation entry after this feature, then re-run `validate-roster.py` over it" in another project — makes the guard report `unreadable` and count it as a defect. The helper that would have been correct (`_read_any`, line 452) already exists in the same file and says so in its own docstring.
- **Proposed fix**: use `_read_any` for caller-supplied roster paths, and report a genuine read error as an input error rather than as an absent seat.

### F3 — the closure check is not wired into any stage gate, so a feature can reach `Blocked` with an unrecorded new red

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/specs/088-speckit-visualization/test-evidence/cl-01-closure.txt` § 1; `.specify/specs/088-speckit-visualization/baseline-failed.txt`
- **Evidence** (verbatim quote):

  ```
  91 node ids before, 92 after: **0 removed**, **1 added**
  ```

  This review re-measured the same six suites and reproduces the reading exactly (`test-evidence/review-smoke/c51-reproduction.txt`), so the C-51 clause holds. The gap is the clause's **scope**: against the full tree the same delta also reports

  ```
  FAILED tests/contract/test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies
  ```

- **Why it's a problem**: `test_fast_fail_discipline.py` is an **edited file in this delta** (`FACTORY_PRESETS` gains `agents/reporter.agent.md`; the C-10 and C-12 counts move 16 → 17 and 18 → 19) and it is *not* among C-51's six suites, so the new red is invisible to the feature's closure evidence, to `baseline-failed.txt` (27 names, none of them this) and to the closure checker, which judges criteria and says nothing about regressions. The scope of the compared suite set is therefore chosen per run with no rule behind it — the one guarantee that would have caught this is "every `tests/**/*.py` path in `git diff --name-only base..HEAD`", and it is written nowhere.
- **Proposed fix**: give `closure-acceptance-check.py` (or the implement gate) a fifth input — the node-id diff against the recorded baseline for the *changed* suites, derived from `git diff --name-only` rather than a hand-written list — and make a new red on a changed suite a named reason code.

### F4 — `Blocked` has no "what would unblock this" surface on the feature index, and the index row is the only place a reader looks

- **Severity**: P1
- **Category**: Workflow
- **Location**: `.specify/memory/features.md` row 087 (Last Updated cell) vs `.specify/memory/features/088.md` § Status Tracking
- **Evidence** (verbatim quote, features.md row 087):

  ```
  | 087 | Speckit 框架可视化（Speckit Framework Visualization） | … | Blocked | .specify/memory/features/088.md | .specify/specs/088-speckit-visualization/requirements.md | 2026-11-06 (… «closure reason» …) |
  ```

- **Why it's a problem**: the row is accurate and very long, and it is the only place a status scanner reads. The two unblock actions live in `verification.md` (`SC-001_unblock=`, `SC-002_unblock=`) and are restated in the feature detail — three surfaces, none of which a `grep -n "| 087 |" features.md` reader reaches. `shared/workflow/feature-integration.md` § Feature Binding Rules defines the row shape as **pointer** (id → one-line meaning → authority path → status), and this cell has grown into a decision record.
- **Proposed fix**: keep the cell pointer-shaped and let the feature detail own the narrative; or add a `Blocked` reason-code column that carries the closure checker's own reason codes (`final-path-not-pass: SC-001`) so the index row is machine-readable without restating the ladder.

### F5 — `review-feature-quality` segment A has no traceability slot, so a segment can run its five dimensions and show only one of them

- **Severity**: P2
- **Category**: Template
- **Location**: `templates/review-template.md` § 2.2
- **Evidence** (verbatim quote from the slot's own preamble):

  ```
  > Verdicts and finding rows only: no narrative opinion body and no severity roll-up (the roll-up lives in § 2's summary); the findings table below is the required per-finding record.
  ```

- **Why it's a problem**: the skill fixes five dimensions (completeness, internal consistency, traceability, dependency and premise ownership, acceptance honesty) and the template gives the slot one table of *findings*. A clean dimension renders as nothing, so a reader cannot tell "traceability was checked and is fine" from "traceability was not checked". The `checked / expected` coverage line survives only because it is a completeness artifact.
- **Proposed fix**: add a per-dimension verdict line to the slot (`traceability: pass | blocked (n findings)`), or let the segment's five dimensions be the slot's own row set.

### F6 — the code segment's headline § 2.1 field is titled "Segment verdict" but the closed value set mixes a severity read with a non-conclusion

- **Severity**: P2
- **Category**: Template
- **Location**: `templates/review-template.md` § 2.1 (the `SEGMENT_VERDICT` row)
- **Evidence** (verbatim quote):

  ```
  | Segment verdict | `SEGMENT_VERDICT` | one of the four closed values the `code-review` skill owns (`pass`, `blocked`, `not-applicable`, `not-evaluated`) |
  ```

- **Why it's a problem**: the `code-review` skill's own closed vocabulary for this slot is not stated in the skill at all — the template attributes it there and the skill body never enumerates `pass` / `blocked`. A run has to reconstruct the mapping from "no blocking entries" to `pass`, and this run had to decide what `blocked` means when there are zero `blocking` entries but an `important` item is a genuine regression. The gate is unambiguous (`gate=allow`); the segment verdict is not.
- **Proposed fix**: enumerate the four values and their derivation in `skills/internal/code-review/SKILL.md`, next to the gate, so the template can cite a section instead of describing the values.

### F7 — an analyze-repair commit carried an undeclared framework edit that no later stage's evidence could see

- **Severity**: P2
- **Category**: Workflow
- **Location**: git commit 0d97dfd3 (`agents/sdd-analysis-worker.agent.md` line 11 and four per-tool copies)
- **Evidence** (verbatim quote from the commit message):

  ```
  fix(088-speckit-visualization): close the round-3 tasks findings F-11/F-12/G-02
  ```

  versus the diff:

  ```
  -display-color: teal
  +display-color: cyan
  ```

- **Why it's a problem**: the commit landed after the analyze checkpoint, touches a framework Agent Template no requirement or task row names, and describes only tasks-row repairs in its message. Nothing downstream re-reads the whole delta against `tasks.md`: `/speckit.implement` builds its contract from `tasks.md`, and `/speckit.review`'s own implementation segment is the first place the edit becomes visible. A single-field cosmetic edit is harmless; the same channel would carry a harmful one.
- **Proposed fix**: give the analyze repair wave a declared write scope (the three stage artifacts) and have `analyze`'s wrap-up fail when a commit after its checkpoint touches a path outside it — or at minimum require the commit body to enumerate every path in the diff.

### F8 — `run-determination` writes session files into the tracked `.specify/memory/session/` tree, so every run leaves the working tree dirty

- **Severity**: P2
- **Category**: Workflow
- **Location**: `.specify/memory/session/` (modified by ten earlier run determinations; new records untracked)
- **Evidence** (verbatim quote, `git status --short` at review time):

  ```
   M .specify/memory/session/20261104T080021Z-run-determination-speckit-requirements-20261104t080021z.md
  ?? .specify/memory/exec-quant/records/20261106T040830002388Z-9d3fe0ac.json
  ```

- **Why it's a problem**: the review-stage instruction to "commit only the review artifacts, never the run records" implies the run records are untracked or ignored. They are neither: earlier sessions' records are tracked *and modified*, so every stage boundary produces a tree that is dirty in a way unrelated to the work, and the implementation segment must disclose uncommitted scope on every run. The concurrent-development rule ("records are per-entry files so two branches write different paths") is honoured; the git-tracking policy for them is not stated anywhere.
- **Proposed fix**: either `.gitignore` the run-record stores (session / exec-quant / feedback) wholesale and delete the tracked copies, or state in `shared/workflow/feedback-step.md` that these records are tracked and must be committed with each stage's checkpoint — pick one and write it where the engine's own docs point.

### F9 — the digest cap and stale-bound defaults are owned by a code constant while the owner document owns everything they interact with

- **Severity**: P2
- **Category**: Documentation
- **Location**: `scripts/python/status-digest.py` lines 68 and 73
- **Evidence** (verbatim quote):

  ```
  #: The digest's entry cap default. Owner of this value: this constant (contract
  #: ``ownership-map.contract.md`` C-47 row "Digest cap default"); overridable per invocation with ``--cap``.
  DEFAULT_CAP = 20
  ```

- **Why it's a problem**: `shared/guidelines/reporting-obligations.md` is declared the single owner of the digest contract, the cadence default, the stale rule and the seat obligation, and it is — except for these two numbers, whose declared owner is a Python constant in the implementation. A prose reader of the owner document cannot find the cap or the stale bound; a machine reader of the constant cannot find why they are what they are. The C-47 row is an honest declaration, which is what makes this a documentation gap rather than a `one-source-of-truth` violation — but a reader is still sent to a `.py` file to learn a user-facing number.
- **Proposed fix**: state both numbers in the owner document and have the script read them (or cite the owner's section in the constant's comment), so the declared owner of the digest contract holds every constant of the digest contract.

### F10 — `pytest -q` gives no per-suite attribution for a mixed green/red run, and the stage evidence format has no slot for it

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `.specify/templates/verification-log-template.md` § /speckit.implement results
- **Evidence** (verbatim quote, this run's reading):

  ```
  2 failed, 131 passed in 3.27s
  ```

  against the log's own field:

  ```
  post_change_affected_suites_node_ids=92 (0 removed, 1 declared addition; 92 passed post-change, 91 passed pre-change)
  ```

- **Why it's a problem**: the log's fields are all *counts over a chosen suite set*, and nothing asks the implement run to name which suites it chose or to include the suites whose files it edited. The 087 run chose C-51's six and excluded `test_fast_fail_discipline.py`, an edited file; the count therefore reads clean while two node ids in the delta's own edited surface are red. A required field naming the suite set's derivation would have surfaced F3 at implement time.
- **Proposed fix**: add `affected_suites_set=<the rule that produced the set>` to the verification-log template and require it to include every `tests/**/*.py` path in `git diff --name-only base..HEAD`.

## 4. What Worked — Preserve (Brief)

- **`Blocked` as a first-class status with the checker's own reason codes.** The feature did not claim `Implemented` with a footnote; it landed `Blocked` and cited `final-path-not-pass: SC-001`, `SC-002`.
- **The five-field measurement ladder** (`blocked_at` / `reduced_measurement` / `reduced_measurement_run` / `why_reduced_insufficient` / `unblock`). Both `partial` rows carry all five and the `unblock` fields are actionable instructions, not wishes.
- **The `not-evaluated` reading for an empty population.** RO-04 returns `not-evaluated … the recorded name-list holds no in-population row` instead of a vacuous `pass`.
- **The AST-based machinery scan in RO-13**, which asks "is a spawn API called?" rather than "does the text contain the word".
- **The red-first red readings recorded with their failure text** (`notes/red-first-evidence.md`), including the one test that passed at RED and why.
- **The `checked / expected` coverage discipline in the code segment**: 166/166 with a real receipt block, and the receipt is what makes "the diff was read" a checkable claim rather than a sentence.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Automation / Script Improvements

- **REC-A1 — make the per-tool agent renderer rewrite the clause interval, and test the round trip** — Target: `src/specify_cli/__init__.py` (absolute: /storage/project/cloud-native-ai/spec-kit/src/specify_cli/__init__.py) and `tests/contract/test_fast_fail_discipline.py` (absolute: /storage/project/cloud-native-ai/spec-kit/tests/contract/test_fast_fail_discipline.py). Change: apply `rewrite_paths` to the clause interval in the per-tool agent renderer and add a whole-tree-render → `test_i11` round-trip test. Source: F1. Expected impact: a green `test_i11` that stays green after the next render, instead of one that depends on which renderer was used and on rendering one file at a time.
- **REC-A2 — route caller-supplied paths through `_read_any`** — Target: `scripts/python/status-digest.py` (absolute: /storage/project/cloud-native-ai/spec-kit/scripts/python/status-digest.py) § `proposition_ro_04`. Change: use `_read_any` for `--roster` paths and distinguish a read error from an absent seat. Source: F2. Expected impact: the population half of SC-002 becomes measurable in another project, which is the criterion's whole subject.

### 5.2 Workflow Improvements

- **REC-W1 — derive the regression suite set from the changed files** — Target: `.specify/templates/verification-log-template.md` and `scripts/python/closure-acceptance-check.py` (absolute: /storage/project/cloud-native-ai/spec-kit/scripts/python/closure-acceptance-check.py). Change: require a named derivation for the compared suite set, and have the closure checker take the changed-suite node-id diff as an input with its own reason code. Source: F3, F10. Expected impact: a new red on a changed suite refuses the transition instead of hiding behind a hand-picked subset.
- **REC-W2 — give the analyze repair wave a declared write scope** — Target: `templates/commands/analyze.md` (absolute: /storage/project/cloud-native-ai/spec-kit/templates/commands/analyze.md) § wrap-up. Change: name the writable path set and fail the wrap-up when a commit after the analyze checkpoint touches a path outside it. Source: F7. Expected impact: no more undeclared framework edits riding a "close the findings" commit.
- **REC-W3 — state the git-tracking policy for the run-record stores** — Target: `shared/workflow/feedback-step.md` (absolute: /storage/project/cloud-native-ai/spec-kit/shared/workflow/feedback-step.md). Change: say whether `.specify/memory/{session,exec-quant,feedback}/` are tracked-with-checkpoint or ignored, and align `.gitignore` with the answer. Source: F8. Expected impact: stage boundaries stop producing dirty trees unrelated to the work.
- **REC-W4 — make the feature index row carry the closure reason code** — Target: `templates/feature-index-template.md` (absolute: /storage/project/cloud-native-ai/spec-kit/templates/feature-index-template.md) and `shared/workflow/feature-integration.md` § Feature Binding Rules. Change: keep the row pointer-shaped and add a machine-readable reason-code column for non-`Implemented` rows. Source: F4. Expected impact: a status scanner can act on `Blocked` without parsing a 600-character decision record.

### 5.3 Template Improvements

- **REC-T1 — give artifact segment A a per-dimension verdict line** — Target: `templates/review-template.md` (absolute: /storage/project/cloud-native-ai/spec-kit/templates/review-template.md) § 2.2. Change: add a five-row dimension verdict block beside the findings table. Source: F5. Expected impact: a clean dimension is visible as clean rather than as silence.
- **REC-T2 — enumerate the four segment-verdict values where the code skill owns them** — Target: `skills/internal/code-review/SKILL.md` (absolute: /storage/project/cloud-native-ai/spec-kit/skills/internal/code-review/SKILL.md) § Phase 3. Change: state what `pass` / `blocked` / `not-applicable` / `not-evaluated` mean and how each is derived, then cite that section from `templates/review-template.md` § 2.1. Source: F6. Expected impact: the segment verdict stops being re-derived per run.

### 5.4 Documentation Improvements

- **REC-D1 — move the digest's two numeric defaults into the owner document** — Target: `shared/guidelines/reporting-obligations.md` (absolute: /storage/project/cloud-native-ai/spec-kit/shared/guidelines/reporting-obligations.md) § digest contract. Change: state the entry cap and the stale bound there and have `status-digest.py` read or cite them. Source: F9. Expected impact: the declared owner of the digest contract holds every constant of it.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | REC-A1 — renderer rewrites the clause interval, round-trip test | `src/specify_cli/__init__.py`, `tests/contract/test_fast_fail_discipline.py` | F1 |
| P1 | REC-A2 — caller-supplied roster paths via `_read_any` | `scripts/python/status-digest.py` | F2 |
| P1 | REC-W1 — regression suite set derived from the changed files | `templates/verification-log-template.md`, `scripts/python/closure-acceptance-check.py` | F3, F10 |
| P1 | REC-W4 — machine-readable closure reason code | `templates/feature-index-template.md`, `shared/workflow/feature-integration.md` | F4 |
| P2 | REC-W2 — declared write scope for the analyze repair wave | `templates/commands/analyze.md` | F7 |
| P2 | REC-W3 — git-tracking policy for run-record stores | `shared/workflow/feedback-step.md` | F8 |
| P2 | REC-T1 — per-dimension verdict line in segment A | `templates/review-template.md` | F5 |
| P2 | REC-T2 — enumerate the segment-verdict values in the code skill | `skills/internal/code-review/SKILL.md` | F6 |
| P2 | REC-D1 — digest defaults in the owner document | `shared/guidelines/reporting-obligations.md` | F9 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly: **No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.**

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.
