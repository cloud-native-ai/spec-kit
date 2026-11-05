# Specification-Driven Development (SDD) Process Review Report: Harness 三重结构（markdown + yaml + script）— review round 3

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
>
> **This is round 3 — the final quality gate — of the review of Feature 084.** Round 2's report is archived as
> `review-r2.md` in this directory, round 1's as `review-r1.md` (rotation per
> `shared/workflow/acceptance-hardening.md` § Review Composition § Records and rotation; the slice id here is the
> review round, so each archive keeps the content's own round marker). Round 3's delta is the fix commit
> `e1f59096`; round 3's first duty is to close or retain every round-2 item.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 084 |
| Requirement Key | 084-harness-triple-structure |
| Requirement Name | Harness 三重结构（markdown + yaml + script） |
| Repository | spec-kit (`git rev-parse --show-toplevel` → `/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | `(no publishable HTTPS remote)` — remotes are `gitee`/`github`/`gitlab` (SSH) plus `origin` = `git@github.com:github/spec-kit.git` (upstream; it does not contain these commits) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch was never pushed. Every citation is an absolute path plus `git show e1f59096:<path>` recovery |
| Branch | `084-harness-triple-structure` |
| Commit SHA | `e1f5909634018375b2de838936a4c0dfbd3c4a22` (short: `e1f59096`) — the review round-3 `HEAD`, fixed for the run |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | SDD Executor (fresh dispatch; same-author detection delegated per `shared/workflow/objective-analysis-gate.md`) |
| Environment | Linux, bash, CPython 3.11.13, `pytest 9.2.0` pin (EP-001), no subagent-dispatch capability in this topology |
| spec-kit Source Snapshot | this repository at `e1f59096` (self-hosting: `.specify/` is the same flow every client project runs) |
| Round-1 record | `review.md` at `03a19487` → archived as `review-r1.md` (43294 B); its code segment → `code-review-20261105T160943Z.md` |
| Round-2 record | `review.md` at `e0453f9e` → archived as `review-r2.md` (40484 B); its code segment → `code-review-20261105T162652Z.md` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|------------------|
| requirements.md | 285 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/requirements.md` | 19 FR / 6 SC / 14 STR, A1–A10 adjudications, scope criteria D1∧D2 |
| plan.md | 434 | `…/084-harness-triple-structure/plan.md` | 18/18 Constitution Check, 4 decision tensions, EP-001…EP-007, D1–D13 |
| tasks.md | 262 | `…/084-harness-triple-structure/tasks.md` | 32 rows (all `[X]`), 7 phases, GATE-1…7, `**DoD Status**: green-with-void` |
| verification.md | 134 | `…/084-harness-triple-structure/verification.md` | baseline block, one machine-readable smoke record (now four fields), six SC status rows, joint-acceptance rows |
| contracts/ (5 files) | 426 | `…/084-harness-triple-structure/contracts/` | C-001…C-059, `md-bold-closed` (verified: 12+13+16+10+8 = 59) |
| data-model.md | 169 | `…/084-harness-triple-structure/data-model.md` | E-1…E-10 + six fixture families |
| quickstart.md | 152 | `…/084-harness-triple-structure/quickstart.md` | S1…S8 (4 measured, 4 route-(b)) |
| research.md | 157 | `…/084-harness-triple-structure/research.md` | R1–R10 measured readings |
| feature-ref.md | 42 | `…/084-harness-triple-structure/feature-ref.md` | bound Feature 084 + status movement |
| code-review.md | this run | `…/084-harness-triple-structure/code-review.md` | round-3 code segment record (1 blocking, 2 important, 3 suggestion, 2 praise) |
| review-r1.md | 43294 B | `…/084-harness-triple-structure/review-r1.md` | round-1 report |
| review-r2.md | 40484 B | `…/084-harness-triple-structure/review-r2.md` | round-2 report, archived by this run |
| code-review-20261105T160943Z.md | 64141 B | `…/084-harness-triple-structure/code-review-20261105T160943Z.md` | round-1 code record |
| code-review-20261105T162652Z.md | 74424 B | `…/084-harness-triple-structure/code-review-20261105T162652Z.md` | round-2 code record, rotated by `start` in this run |

## 1. Process Execution Timeline (round-2 close → round-3 open)

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | round 2 judged 0 P0 / 5 P1 / 2 P2, ARC read `accept`, and refused the flip on the status machine's condition (c) | `review-r2.md` § 2.4 (`verdict: accept`, pass 2 / 0 / 0 / 0 / 0 / 0 / 2) and § Status Transition (failed condition (c): 1 `blocking`) | No — the refusal is the prescribed disposition |
| 2 | round-2 code segment carried exactly 1 `blocking`: the surviving `flow-class-classes` inline copy | `code-review-20261105T162652Z.md` § Review 意见 `[BLOCKING] scripts/python/closure-acceptance-check.py (Line 227)` | No |
| 3 | fix commit `e1f59096` "close the last inline class copy and the review P1s" — 9 paths, +111 −12, **subject only, no body** | `git show --stat e1f59096` | **Yes** — see N1: the subject claims the P1s closed; of round 2's five P1s three closed outright (its N1, N2, N5) and two only partially (its N3, N4), and the per-site closure table REC-084-10 asks for is absent |
| 4 | the fix round's own test evidence is **not captured**: the only test file in the evidence directory is the previous round's (`e0453f9e`) run, and the fix round's contract set has no archive | `git show --name-only --format= e1f59096` adds no test-evidence capture beyond `review-r3-closure-2026-11-06.txt` (the ARC JSON); `test-evidence/review-fix-targeted-tests-2026-11-05.txt` tail reads `2 failed, 219 passed in 6.33s`, a run whose commit predates the defect | **Yes** — see N2: the run that would have had to prove the fix left no record, and the module that reproduces the broken shape is not in any captured set |
| 5 | round-3 targeted set (`targeted-set-v1` over the fix's code paths): **4 failed, 356 passed**, two of them new | `test-evidence/review-round3-targeted-2026-11-06.txt` tail: `4 failed, 356 passed`; set in `review-round3-targeted-set.txt` (14 files) | No — the run is the gate's own reading |
| 6 | the two new failures are the same defect: `closure-acceptance-check.py` aborts in a tree without `declaration_reader.py` | `test-evidence/review-round3-regression-2026-11-06.txt` (HEAD `rc=1`, 0 stdout bytes, traceback; parent `e0453f9e` `rc=2`, three labelled degradation lines, no traceback) | No — this is the finding, not a deviation |
| 7 | ARC re-read at `e1f59096`: `verdict: accept`, all four completion conditions true | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), copied into § 2.4 | No — the machine's answer, not the run's prose |
| 8 | round 3 dispatched against `e1f59096` | state spine `stage_base_commit: e1f59096`, `attempt: 3` | No |

## 2A. Round-2 Closure Ledger (round 3's first duty)

| Round-2 item | Severity then | Round-2 location | Round-3 reading | Owner stage of what remains |
|---|---|---|---|---|
| **N1** the delta did not deliver SC-002's one-machine-read-copy property; the third site held the inline tuple | P1 (and the code segment's 1 `blocking`) | `closure-acceptance-check.py:227` | **Closed on both sides**: `_declared_flow_classes()` reads the fact through `declaration_reader`, `FLOW_CLASSES` is the declaration's `statement`, `DEFAULT_FLOW_CLASS` takes member 0 (248) so the "two owner claims" defect collapses, the membership test compares against the derived tuple, and `consumers:` names the engine (4 entries). `verify` reads `31/31` + `16/16`, `findings: 0` | — (the same function introduces this round's blocking, see N2) |
| **N2** round 1's second legal carrier was never written | P1 | `features/084.md` `## Latest Review` | **Closed**: round 2 wrote its own review-record entry (`grep -n 'speckit.review' .specify/memory/features/084.md` hits), and this run adds round 3's | — |
| **N3** the new `smoke_comparison` slot shipped without a reader | P1 | `templates/verification-log-template.md:65` | **Half closed**: the field is in `SMOKE_FIELDS` and `evaluate_smoke` copies it into the record, so the closure JSON now carries `"comparison": "byte-identical with …(cmp exit 0)"`. No existence test, and the recorded value is prose where the slot declares a repo-relative path — see N5 | implement (the recorded value) / template (the slot's reader) → REC-084-09 |
| **N4** a closed row whose named carrier is absent is indistinguishable from a closed row | P1 | `tasks.md:31`, `tasks.md:166` | **Half closed**: T031's carrier `notes/quickstart-run.md` now exists (it records `waived-by-user`, "No output is claimed"); GATE-2's `test-evidence/head-failed.txt` still has never existed on this branch (`git log --all -- '*head-failed.txt'` finds only 081's `081d-head-failed.txt`) — see N7 | implement (`tasks.md` rows) → REC-084-06 |
| **N5** a `pass` row recorded a count the tree no longer reads; limb (iii) falsified | P1 | `verification.md:70` | **Count limb closed, traceability limb re-opened**: the row now reads `31/31` and that matches the live `verify`, but its own evidence pointer still resolves to a capture that reads `28/28` (`t032-classification-readings-2026-11-05.txt:578`) — the value moved and the reading under it did not. Limb (iii) is now true (all four readers are named in `consumers:`) — see N3 | implement (`verification.md` evidence pointer) → REC-084-06 |
| **N6** `post_change_commit` names a commit that never touched the file | P2 | `verification.md:39` | **Open, unchanged**: still `98288d45`, and `git log --oneline -- verification.md` reads `e1f59096`, `e0453f9e`, `03a19487`, `e185da6c`, `1e4ca01e` — see N4 | implement (`verification.md`) |
| **N7** `green-with-void` used for a user waiver | P2 | `tasks.md:26`, `:202` | **Open, unchanged**: the token and its annotation are byte-identical to round 2 — see N6 | template (`tasks-template.md`) → REC-084-02 |
| **F4 / F5 / F6 / F7** (round-1 framework items: opt-in flag default, `verify`'s non-reading `residual_literals`, delegation topology, help-text step count) | P2 | round-1 report § 3 | **All four open**: `verify` still prints `residual-literals: delegated: …` (a constant, now item 3 of the code record); the other three are untouched by the fix | framework recommendations REC-084-03 / 04 / 07 / 08 |
| **F16** the client-project limbs of SC-005 never ran | P2 | `verification.md:95-102` | **Open under the user's test waiver** — no scratch-tree `specify init` reading exists; the mirror limb is green (six pairs `ok`) | user waiver (residual risk, not a defect) |

**Round-2 dispositions that need no action**: the ARC verdict, the two-carrier rule for round 2's own run, and the code-blocking closure all held. Round 3's new blocking is not a retention — it is a defect the fix commit introduced (N2).

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 2 |
| Documentation | 2 |

Round 2 closed three of its five P1s outright (its N1, N2 and N5) and left two only partially closed (its N3 → this round's N5, graded P2; its N4 → this round's N7, retained at P1). Two of the four P1s here are new — N1 and N2 — and both are about how a fix round reports and proves itself rather than about the feature's own code.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `e1f5909634018375b2de838936a4c0dfbd3c4a22` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base --spec …` reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 289 / 5 / 284 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `blocked` | the record carries 1 `blocking` entry |
| Gate verdict | `blocking-unresolved` | `report --summary --file …` exits 1 with `blocking_entries=1`, `gate=deny` |
| Reason, when one applies | none | a `blocked` verdict needs no basis line |
| Uncommitted scope | disclosed, never concluded over: this run's own surface is `review.md` (rewritten), `review-r2.md` (round-2 report archived), `code-review.md` (rewritten after rotation), `code-review-20261105T162652Z.md` (round-2 code record archived), the four `test-evidence/review-round3-*` evidence files, the `stage-status.md` round-3 row, the `## Latest Review` entry in `.specify/memory/features/084.md` and the one new `REC-084-12` row in `.specify/memory/register.md`; a pre-existing modified run record `session/20261102T231648Z-…-081a.md` and pre-existing untracked `memory/` records are outside the slice and were left untouched | the same sentence in [`code-review.md`](/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md) |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` | written (triage `run`) |
| Archive | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review-20261105T162652Z.md` | round 2's record, rotated by `start` |

Six-level counts in the record: `blocking` 1 · `important` 2 · `suggestion` 3 · `nitpick` 0 · `question` 0 · `praise` 2. The `blocking` entry is **new** and is the one fact that decides this round: `_declared_flow_classes()` in `scripts/python/closure-acceptance-check.py` (129-139) omits the `declaration_reader is None` guard its sibling carries, so in a tree that ships the checker without its sibling read entry the module raises `AttributeError` at import — exit 1, zero stdout, no verdict. The two `important` entries are the retained round-2 items (FR-012's fallback-vs-delete ruling, and `verify`'s non-reading `residual_literals`). The three `suggestion` entries are the `smoke_comparison` resolution, the fact file's stale header comment, and the import-time label write. The findings themselves are read there; this subsection carries the verdict and the pointers only.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | derived: the standard spec-stage set ∪ `plan.md` § Project Structure § Documentation (which declares `research.md` and `feature-ref.md` in addition) — **9 members** |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | two P1 traceability/acceptance findings plus four P2 rows |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/084-harness-triple-structure/tasks.md` | 31 | none | GATE-2 names `test-evidence/head-failed.txt`, a file that has never existed on this branch, while the DoD block reports the gate area green under the waiver — N7 |
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 70 | none | `SC-001_value` now reads `31/31`, but `SC-001_evidence` still points at a capture that reads `28/28` — the criterion's value and the reading under it disagree — N3 |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 166 | none | T031 is `[X]` and its carrier now exists, but the carrier says the work was not done (`waived-by-user`, "No output is claimed") — N7 |
| P2 | `.specify/specs/084-harness-triple-structure/verification.md` | 39 | none | `post_change_commit=98288d45` names a Part-3 commit that never touched this file — N4 |
| P2 | `.specify/specs/084-harness-triple-structure/verification.md` | 57 | none | `smoke_comparison` holds a sentence where the template declares a repo-relative transcript, and the closure engine now copies that sentence into its JSON as `comparison` — N5 |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 26 | none | `green-with-void` used for a user waiver rather than a falsified premise — N6 |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `e1f5909634018375b2de838936a4c0dfbd3c4a22` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Smoke command | `python3 scripts/python/harness-triple-check.py --action coverage` (run twice, byte-compared) | recorded verbatim |
| Smoke exit code | `0` | the integer the command returned, both runs |
| Smoke evidence path | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/test-evidence/review-round3-smoke-2026-11-06.txt` | exists, non-empty; holds both runs' full stdout/stderr, both exit codes, the `cmp` exit and both sha256 values (`f9cd934a…b13473`, identical — the same value as rounds 1 and 2) |
| Scope and regression verdict | scope clean (the fix touches 9 paths, all inside the feature's own surfaces; `sync-mirrors.py --check` exit 0 with six pairs `ok`; `git diff 4b65517c -- pyproject.toml` empty); **regression not clean** — the fix introduces two new failures in a module it never ran | the segment's own reading |
| Segment verdict | `blocked` | the delta breaks a delivered, documented behaviour and two existing contract tests |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `scripts/python/closure-acceptance-check.py` | 138 | none | The delta aborts the closure checker in the reader-absent deployment shape (`rc=1`, zero stdout) instead of degrading with a label, and `tests/contract/test_gate_wiring_081.py` loses two legs — N2 |

Scope reading in one sentence: everything the fix changed belongs to the task rows it answers, and nothing outside the feature's surfaces moved; the delta fails on **regression**, not on scope.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `features.md` row 084 and `features/084.md` `**Status**` |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), never recomputed here |
| Comparison verdict | `agree` | the checker's verdict is `accept` and the claim is `Implemented` |
| Failed condition, on refusal | none — no refusal fires on this record | `completion_conditions` reads `every_final_path_pass: true`, `no_open_rows: true`, `smoke_record_pass: true`, `status_row_per_criterion: true`; `reasons: []`; the four-field smoke block now reports `comparison` as well |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 2 |

**ARC does not refuse this round either.** For the third time the run's refusal comes from the status machine's condition (c) — a different gate reading a different artifact — and this time the implementation segment independently refuses on regression, which is a third reading again. Collapsing them into one sentence would hide which gate fired for what.

## Status Transition — refused, and the condition is named

The transition judged here is `Implemented → Ready for Review`, whose four conjunctive conditions are owned by `templates/feature-details-template.md` § Canonical Status State Machine and are cited here, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | `tasks.md`: `closed 32 / deferred 0 / open 0` (the checker's own `tasks` block) | satisfied |
| (b) review evidence produced | this report + `code-review.md`, both on disk | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `code-review.md` carries **1** `blocking` entry (`closure-acceptance-check.py:138`); `report --summary --file` exits 1 with `gate=deny` | **FAILS** |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 2 `pass`, 0 in every non-pass bucket | satisfied |

**The refusal literal is `blocking-unresolved`, the failed condition is (c), and the status stays `Implemented`.** No surface is written back: `features.md` and `features/084.md` keep `Implemented`, because a refusal is not a downgrade. Round 3's own artifacts land on the two verifiable carriers — this report's § 2.1 and the `## Latest Review` entry this run adds to `features/084.md` — and neither states a new status.

The round-3 refusal is materially different from rounds 1 and 2: those were refused on a **surviving** defect being found again, this one on a **newly introduced** one. The fix closed the last copy of the declared closed set — the very thing rounds 1 and 2 asked for — and in doing so replaced a labelled degradation with an unhandled `AttributeError`. Both halves are true and both are reported: the closure is real (§ 2.1's `praise` entries and § 2A's first row), and so is the regression.

## 3. Findings (Problems & Improvement Targets)

### N1 — A fix round's closure is asserted from the commit subject, and this round it is wrong in both directions

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` § 2.1; the claiming artifact is `git log -1 --format=%B e1f59096`
- **Evidence** (verbatim quote, the whole message):

  ```
  fix(084): close the last inline class copy and the review P1s
  ```

  against round 2's own list of what was open, read at `review-r2.md` § 2A:

  ```
  | **N3** The new smoke slot ships without a reader | P1 | … | **Open** |
  | **N4** A closed row whose named carrier is absent … | P1 | … | **Open, unchanged** |
  ```

- **Why it's a problem**: REC-084-10 asked for a per-site closure table so the next round could read the claim instead of the subject line; round 3 has neither, and the subject is inaccurate in both directions at once — three of round 2's five P1s are in fact closed (N1/N2/N5), and two are only half closed (N3/N4), while a new blocking was introduced that the subject does not mention. A reviewer who trusted the subject would have flipped the status; the per-site table is what made the difference detectable, and it exists only in this report.
- **Proposed fix**: REC-084-10 as written (a fix round carries finding → enumerated site → commit → reading, and the next round reads that table), plus the observation that the table must also carry **new defects the fix introduced**, since a fix round's message has no natural place to admit them. Framework shape: `skills/internal/review-sdd-process/SKILL.md` § 5 gains the obligation; `templates/commit-template.md` gains the slot.

### N2 — The change that broke a deployment shape left no test evidence, and the set that would produce it is not selected

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Automation / Scripts
- **Location**: `scripts/python/closure-acceptance-check.py:138` (the defect) and `tests/contract/test_gate_wiring_081.py:68` (the module that would have caught it)
- **Evidence** (verbatim quote, the fixture's own copy step and the constant that makes it a candidate):

  ```
  CHECKER_REL = "scripts/python/closure-acceptance-check.py"
  ```

  ```
  (wt / "scripts" / "python").mkdir(parents=True, exist_ok=True)
  shutil.copy2(ROOT / CHECKER_REL, wt / CHECKER_REL)
  ```

  the only test-evidence capture in the fix's neighbourhood, whose run belongs to the **previous** commit:

  ```
  2 failed, 219 passed, 1 warning in 6.33s
  ```

  the fix commit's own evidence inventory (`git show --name-only --format= e1f59096`), which adds no run capture at all:

  ```
  .specify/specs/084-harness-triple-structure/test-evidence/review-r3-closure-2026-11-06.txt
  ```

  and this round's re-run of the same surfaces at `e1f59096`:

  ```
  FAILED tests/contract/test_gate_wiring_081.py::test_a_block_lands_blocked_after_the_record
  FAILED tests/contract/test_gate_wiring_081.py::test_a_passing_line_merges_and_records_merged
  4 failed, 356 passed, 1 warning in 15.50s
  ```

- **Why it's a problem**: `test_gate_wiring_081.py` is the only test that copies the engine into a tree **without** `declaration_reader.py`, i.e. exactly the shape FR-013 promises will degrade with a label instead of a traceback. It contains the changed path literally (`CHECKER_REL`), so `targeted-set-v1` clause (a) selects it — but the fix round archived no run (the 219-passed file is `e0453f9e`'s, a commit at which this module is green because the new function did not exist yet), so nothing in the tree shows the module running after the change. The defect is deterministic: a set containing this module would have reported at least three failures. It reported none, because none was captured. Two costs compound: a shipped `blocking` went unseen by the round that was supposed to prove the fix, and the run that might have seen it cannot be audited at all — the feature's own `verify` stayed green (`findings: 0`, `31/31`) because C-033 walks the parties the declaration names and this shape carries no declaration at all.
- **Proposed fix**: REC-084-12 — `targeted-set-v1` gains a **shape leg**: for every changed engine, select the test files that copy that engine into a constructed tree (`shutil.copy2(ROOT / "<path>"`, `*_REL = "<path>"` and equivalents), because a test that reproduces a deployment shape is the only thing that can see a shape-dependent failure. Second limb, same recommendation: a stage's targeted run MUST leave a captured evidence file (command line, exit code, full output) — a count reported in a commit message is not a reading. Owner: `contracts/test-budget.md` TB-05 (the algorithm's owner) with the carrier in `skills/sdd-loop-driver/references/efficiency-model.md` § 2.3 and `shared/guidelines/single-run-evidence.md`. Expected impact: a change to an engine can no longer ship having run only the tests that give it everything it needs, and it can no longer ship with no record of what ran.

### N3 — A `pass` row's value now disagrees with the reading it points at

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:70` and its evidence pointer on line 72
- **Evidence** (verbatim quote, the row at HEAD):

  ```
  SC-001_value=… consumer consistency declarations→carriers 31/31 and carriers→declarations 16/16
  ```

  and the line the row cites (`SC-001_evidence=…/t032-classification-readings-2026-11-05.txt`), at line 578 of that file:

  ```
  consistency-declarations-to-carriers: 28/28
  ```

- **Why it's a problem**: round 2's N5 said the row's number was stale; the fix corrected the number and left the pointer. Now the criterion claims a reading its own archived capture contradicts, which is the same "two surfaces, one fact" drift one level down — and it is invisible to the program that awards the row, because `closure-acceptance-check.py` reads `SC-00N_status` and never resolves `SC-00N_evidence`. A later reader cannot tell whether `31/31` was measured or transcribed. This is the third appearance of the same class in three rounds (round 1's F3, round 2's N5, this), which is the strongest available evidence that a restated count in prose is not a reading.
- **Proposed fix**: REC-084-06's second half as written — the row's value becomes a pointer to the run's output (`harness-triple-check.py --action verify`) instead of a restated pair, and the evidence pointer resolves to a capture produced by that run. Until then, a `SC-00N_evidence` that does not contain the row's own numbers should be red in the checker.

### N4 — `post_change_commit` still names a commit that never touched the file

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:39`
- **Evidence** (verbatim quote):

  ```
  post_change_commit=98288d45 (this segment's commit is the one carrying these files; recorded here as the parent-inclusive working tree)
  ```

  `git log --oneline -- .specify/specs/084-harness-triple-structure/verification.md` → `e1f59096`, `e0453f9e`, `03a19487`, `e185da6c`, `1e4ca01e`.

- **Why it's a problem**: the field's parenthetical asserts that `98288d45` carries these files, which the file's own history contradicts twice over (the file has now been committed twice more since). An anchor that points at the wrong commit is the same defect class as round 1's F12, which was repaired for `baseline_commit` and not for its sibling.
- **Proposed fix**: derive the field from `git log -1 --format=%h -- <file>` at write time, or drop it in favour of the baseline pair the checker actually reads.

### N5 — The `smoke_comparison` slot now has a reader that reads a sentence

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/templates/verification-log-template.md:65` and its mirror `.specify/templates/verification-log-template.md:65`; the value it consumes is `verification.md:57`
- **Evidence** (verbatim quote, the slot):

  ```
  smoke_comparison     optional: a repo-relative comparison transcript (e.g. the second run's evidence)
                       when the smoke is a determinism comparison; the three fields above MUST carry
                       no annotation — a value the checker parses is a literal
  ```

  the recorded value:

  ```
  smoke_comparison=byte-identical with .specify/specs/084-harness-triple-structure/test-evidence/smoke-run2-2026-11-05.txt (cmp exit 0)
  ```

  and the reader the fix added (`closure-acceptance-check.py:881-883`):

  ```
  comparison = smoke.get("smoke_comparison", [])
  if comparison:
      detail["comparison"] = comparison[0]
  ```

- **Why it's a problem**: round 2's N3 said the slot had no reader; the fix wired one, so the claim is now touched. But the reader copies, never resolves: there is no `is_file()` on the value, and the value this feature recorded is prose around a path, so the template's own grammar ("a repo-relative comparison transcript") is already broken by the first feature to use it. A fabricated or stale comparison still passes condition ④ exactly as a true one does — the "slot that would not go red" shape one level down, now with a program attached that makes it look checked.
- **Proposed fix**: REC-084-09 extended — a slot's reader must **resolve** the value it reads (existence test on the path, red when nothing resolves) and the slot's line must state which reading consumes it; a prose value in a path-shaped slot is an input error, not a comment.

### N6 — `green-with-void` is still used for a user waiver

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:26` and `:202`; the token's owner is `.specify/templates/tasks-template.md:52`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: green-with-void
  ```

  ```
  - **DoD Status `green-with-void`**: the void rows are the user-waived scratch-tree limbs (T022/T030) and the closure full-suite leg, not a premise that measured false. …
  ```

- **Why it's a problem**: byte-identical to round 2's N7 and therefore still true: the token's own definition is a row **whose premise is measurably false**, and the annotation states in the same sentence that these rows are not that. The vocabulary's escape hatch is being used for a case the vocabulary does not cover, which launders a waiver into a green — and the feature's status rests on that block.
- **Proposed fix**: REC-084-02 as written — the template's `DoD Status` domain gains the waiver case explicitly (or states that a waived row is `pending` + annotation and does not feed the status machine).

### N7 — A gate row and a task row still promise evidence that says the work was not done

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:31` (GATE-2) and `:166` (T031)
- **Evidence** (verbatim quote, GATE-2's named output):

  ```
  - GATE-2: Zero new failures on the five frozen gate scripts' existing tests, read at id level — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt -q`, then `comm -13 <implement-start baseline> head-failed.txt` prints nothing …
  ```

  the carrier the fix did create for T031 (`notes/quickstart-run.md`, complete file):

  ```
  **Status**: waived-by-user (2026-11-05). The user directed this run to skip tests and
  scratch-tree proofs; quickstart S5–S8 were not executed. No output is claimed. …
  ```

  and `ls …/test-evidence/head-failed.txt` → `No such file or directory` (the file has never existed on this branch).

- **Why it's a problem**: round 2 graded the pair as one P1 because a `[X]` row with an absent carrier is indistinguishable from a closed row. The fix closed the mechanical half — it created the T031 carrier — and in doing so made the other half explicit: the carrier exists and says the work was not done, while the row stays `[X]` with its promise ("record the real output") intact. GATE-2 is untouched and still names a file that has never existed, while SC-006's note says the id-level leg was not read. Under the user's waiver the honest row state is a waiver token **on the row**, not a tick plus a note three hundred lines below; and a gate whose named output never existed cannot be read as green by anyone who does not `ls`.
- **Proposed fix**: REC-084-06 as written — `validate-tasks.py` gains a carrier-existence leg (`[X]` row → named path must exist, unless the row carries `waived-by-user`), and a gate row's named output is either produced or the gate is recorded as waived on the row. Round 3 adds the datum that the fix round created one carrier and passed over the other while editing the same file.

## 4. What Worked — Preserve (Brief)

- The round-2 blocking is closed by derivation, not by a second literal: one read through `declaration_reader`, member 0 as the default, four declared consumers, and `verify` reading `31/31` + `16/16` with `findings: 0`.
- The two labelled degradations in the same file are documented side by side (`read entry present` = input error, `read entry absent` = labelled skip, "never a traceback") — the documentation that made this round's regression a one-line diagnosis instead of an investigation.
- The smoke record's four fields are now all machine-consumed, and the smoke itself is stable across three rounds: `sha256 f9cd934a…b13473`, identical in rounds 1, 2 and 3.
- The targeted set is reproducible from the fix commit alone (`review-round3-targeted-set.txt` records the paths, the clause that selected each and the command), which is what let this round show that a *selection* gap, not a judgement gap, let the regression through.
- The regression was proven by a two-command differential in a scratch shape (HEAD vs parent, same tree), so the finding does not depend on trusting this review's narrative.
- Determinism of the *verdict* inputs held: ARC's record is byte-identical across three rounds (`pass 2 / total 2`), so the flip's refusal never rests on a moving machine answer.

## 5. spec-kit / SDD Improvement Recommendations

**New this round.** Each is registered in `.specify/memory/register.md` in the same commit as this report.

- **REC-084-12** — Target: `contracts/test-budget.md` TB-05 (the algorithm's owner) with its implementation carrier `skills/sdd-loop-driver/references/efficiency-model.md` § 2.3 (absolute: `/storage/project/cloud-native-ai/spec-kit/skills/sdd-loop-driver/references/efficiency-model.md`). Change: two limbs. (1) `targeted-set-v1` gains a **shape leg** — for each changed engine, also select the test files that copy that engine into a constructed tree (`shutil.copy2(ROOT / "<path>"`, `*_REL = "<path>"` and equivalents) — because a shape-dependent failure is invisible to every test that runs the engine in a complete tree. (2) A stage's targeted run MUST leave a captured evidence file (command line, exit code, full stdout/stderr); a pass count reported only in a commit message or a dispatch brief is not a reading. Source: N2. Expected impact: an engine change can no longer ship having run only the tests that give it everything it needs, and it can no longer ship with no auditable record of what ran.

**Round-2 recommendations, unchanged status** (registered, still `open`, none withdrawn): REC-084-09 (half delivered — a reader exists, it does not resolve; see N5), REC-084-10 (still the right fix, N1 shows the need again), REC-084-11 (delivered by practice in rounds 2 and 3, not yet by a check), REC-084-01/02/03/04/05/06/07/08 (unchanged; N3 renews the need for 06's derived counts, N6 renews 02, N5 renews 09).

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Fix the reader-absent abort in `_declared_flow_classes()` (copy the sibling's guard) | `scripts/python/closure-acceptance-check.py` | N2 (code `blocking`) |
| P1 | `targeted-set-v1` gains the shape leg, and every targeted run leaves a capture | `contracts/test-budget.md` TB-05; `skills/sdd-loop-driver/references/efficiency-model.md` § 2.3 | N2 (REC-084-12) |
| P1 | Per-site closure table for review-fix rounds, including introduced defects | `skills/internal/review-sdd-process/SKILL.md` § 5; `templates/commit-template.md` | N1 (REC-084-10) |
| P1 | Derive SC rows / resolve their evidence pointers instead of restating counts | `scripts/python/closure-acceptance-check.py`, `verification.md` | N3 (REC-084-06) |
| P1 | Carrier existence and a waiver token on a `[X]` row | `scripts/python/validate-tasks.py`, `templates/tasks-template.md` | N7 (REC-084-06, REC-084-02) |
| P2 | The slot's reader must resolve the value it reads | `templates/verification-log-template.md` | N5 (REC-084-09) |
| P2 | `post_change_commit` derived or dropped | `templates/verification-log-template.md` | N4 |
| P2 | `DoD Status` domain names the waiver case | `templates/tasks-template.md` | N6 (REC-084-02) |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target is `external`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document (earlier rounds are reached by the repo-relative paths `review-r1.md` / `review-r2.md` in the same directory).
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status**: **no P0 was raised this round** (round 1 raised three; all closed by machine-readable state; round 2 raised none). The four P1 findings were validated by direct mechanical re-read — each cites a command whose output is quoted, and N2's causal claim is backed by a two-command differential — and none was validated by an independent read-only subagent: this topology has no dispatch capability and the declared fallback (`skills/internal/review-sdd-process/SKILL.md` § 5) was used. The weaker evidence path is disclosed rather than hidden; REC-084-04 would put it on the report's own face.
- [x] **Round-level honesty**: this run refuses the status transition on condition (c) — a newly introduced `blocking`, not a surviving one — while stating in the same breath that the fix closed the round-2 blocking it was asked to close. ARC reads `accept` and the implementation segment refuses on regression; the three readings are reported separately because they read different artifacts.

## 8. Feedback

Framework friction worth posting as feedback (one entry per unit, four units — `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review`): the round-3 run had no way to make the coverage receipt's "first write means everything was read" default say the truth without passing 284 `--skip-with-reason` flags by hand; the receipt's own carried-verdict mechanism only helps from the second write on, and a review whose judged face is 5 of 289 files has to spell out 284 skips to avoid publishing a false `judged=289`. A `--judged-from-notes` or `--judged-only <path>` form would make the honest count the cheap one. No code defect from `code-review.md` is posted here — per `templates/commands/review.md` § Feedback boundary those stay in that record with their severity, file and line.
