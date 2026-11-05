# Specification-Driven Development (SDD) Process Review Report: Harness 三重结构（markdown + yaml + script）— review round 4

> **Audience**: spec-kit framework maintainers.
> **Purpose**: Identify concrete problems and improvement targets in spec-kit templates, command prompts, automation, and workflow as exposed by this feature's SDD lifecycle.
> **Intentionally problem-first**: this report omits long narrative summaries of artifact contents. If a sentence describes the feature instead of identifying a process gap, it does not belong here.
>
> **This is round 4 — the final quality gate — of the review of Feature 084.** Round 3's report is archived as
> `review-r3.md` in this directory, round 2's as `review-r2.md`, round 1's as `review-r1.md` (rotation per
> `shared/workflow/acceptance-hardening.md` § Review Composition § Records and rotation; the slice id here is the
> review round, so each archive keeps the content's own round marker). Round 4's delta is the fix commit
> `2d8576b5`; round 4's first duty is to close or retain every round-3 item.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 084 |
| Requirement Key | 084-harness-triple-structure |
| Requirement Name | Harness 三重结构（markdown + yaml + script） |
| Repository | spec-kit (`git rev-parse --show-toplevel` → `/storage/project/cloud-native-ai/spec-kit`) |
| Repository URL | `(no publishable HTTPS remote)` — remotes are `gitee`/`github`/`gitlab` (SSH) plus `origin` = `git@github.com:github/spec-kit.git` (upstream; it does not contain these commits) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains HEAD` is empty — the branch was never pushed. Every citation is an absolute path plus `git show 2d8576b5:<path>` recovery |
| Branch | `084-harness-triple-structure` |
| Commit SHA | `2d8576b5cb251ca22e90f5312564b657c04811c3` (short: `2d8576b5`) — the review round-4 `HEAD`, fixed for the run |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-06 |
| Reviewer (Agent) | SDD Executor (fresh dispatch; same-author detection delegated per `shared/workflow/objective-analysis-gate.md`) |
| Environment | Linux, bash, CPython 3.11.13, `pytest 9.2.0` pin (EP-001), no subagent-dispatch capability in this topology |
| spec-kit Source Snapshot | this repository at `2d8576b5` (self-hosting: `.specify/` is the same flow every client project runs) |
| Round-1 record | `review.md` at `03a19487` → archived as `review-r1.md` (43294 B); its code segment → `code-review-20261105T160943Z.md` |
| Round-2 record | `review.md` at `e0453f9e` → archived as `review-r2.md` (40484 B); its code segment → `code-review-20261105T162652Z.md` |
| Round-3 record | `review.md` at `4d7270fe` → archived as `review-r3.md` (43217 B) by this run; its code segment → `code-review-20261105T163841Z.md`, rotated by `start` in this run |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|------------------|
| requirements.md | 285 | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/requirements.md` | 19 FR / 6 SC / 14 STR, A1–A10 adjudications, scope criteria D1∧D2 |
| plan.md | 434 | `…/084-harness-triple-structure/plan.md` | 18/18 Constitution Check, 4 decision tensions, EP-001…EP-007, D1–D13 |
| tasks.md | 262 | `…/084-harness-triple-structure/tasks.md` | 32 rows (all `[X]`), 7 phases, GATE-1…7, `**DoD Status**: green-with-void` |
| verification.md | 134 | `…/084-harness-triple-structure/verification.md` | baseline block, one machine-readable smoke record (four fields), six SC status rows, joint-acceptance rows |
| contracts/ (5 files) | 426 | `…/084-harness-triple-structure/contracts/` | C-001…C-059, `md-bold-closed` (12+13+16+10+8 = 59) |
| data-model.md | 169 | `…/084-harness-triple-structure/data-model.md` | E-1…E-10 + six fixture families |
| quickstart.md | 152 | `…/084-harness-triple-structure/quickstart.md` | S1…S8 (4 measured, 4 route-(b)) |
| research.md | 157 | `…/084-harness-triple-structure/research.md` | R1–R10 measured readings |
| feature-ref.md | 42 | `…/084-harness-triple-structure/feature-ref.md` | bound Feature 084 + status movement |
| code-review.md | this run | `…/084-harness-triple-structure/code-review.md` | round-4 code segment record (0 blocking, 2 important, 4 suggestion, 2 praise) |
| review-r1.md | 43294 B | `…/084-harness-triple-structure/review-r1.md` | round-1 report |
| review-r2.md | 40484 B | `…/084-harness-triple-structure/review-r2.md` | round-2 report |
| review-r3.md | 43217 B | `…/084-harness-triple-structure/review-r3.md` | round-3 report, archived by this run |
| code-review-20261105T160943Z.md | 64141 B | `…/084-harness-triple-structure/code-review-20261105T160943Z.md` | round-1 code record |
| code-review-20261105T162652Z.md | 74424 B | `…/084-harness-triple-structure/code-review-20261105T162652Z.md` | round-2 code record |
| code-review-20261105T163841Z.md | 77683 B | `…/084-harness-triple-structure/code-review-20261105T163841Z.md` | round-3 code record, rotated by `start` in this run |

## 1. Process Execution Timeline (round-3 close → round-4 open)

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | round 3 refused the flip on condition (c), naming `blocking-unresolved`, with the fix it had asked for recorded as real | `review-r3.md` § Status Transition (condition (c) FAILS; `blocking_entries=1`, `gate=deny`) | No — the refusal is the prescribed disposition |
| 2 | fix commit `2d8576b5` "guard the flow-class read and keep the FR-012 fallback" — 3 paths, +51 −0, **subject only, no body** | `git show --stat 2d8576b5` | **Yes** — see N1: the message names the mechanism and not one round-3 item, and the per-site closure table REC-084-10 asks for is absent for the second consecutive round |
| 3 | the fix round's only captured artifact is a copy of the ARC JSON; the test reading it truthfully relied on (`gate_wiring 22 passed`, `241 passed / 2 failed`) exists in the state spine and the dispatch brief, not on disk | `git show --name-only --format= 2d8576b5` → `.specify/specs/084-harness-triple-structure/test-evidence/review-r4-closure-2026-11-06.txt` only | **Yes** — see N2: REC-084-12's second limb (a targeted run leaves a captured file) is violated for the second round running |
| 4 | round-4 targeted set (`targeted-set-v1` over the fix's code path; identical to round 3's 14 files because the delta touches one engine): **2 failed, 358 passed** | `test-evidence/review-round4-targeted-2026-11-06.txt` (rc=1, 16 s); set in `review-round4-targeted-set.txt` | No — this is the gate's own reading |
| 5 | the two round-3 red legs are green; the module reads 22 passed | `test-evidence/review-round4-gates-2026-11-06.txt` §4 | No |
| 6 | the regression is closed by a two-command differential in the same scratch shape (parent vs HEAD) | `test-evidence/review-round4-regression-2026-11-06.txt` §A (parent: `rc=1`, 0 stdout bytes, `AttributeError` traceback) vs §B (HEAD: `rc=2`, four labelled lines, no traceback) | No |
| 7 | the fix's own comment claim ("a readable declaration wins") is measured by narrowing the declaration's `statement` in a scratch tree | same file §C/§C2/§C3: `accept` → `input error: … outside the closed set expression` → `accept` | No |
| 8 | ARC re-read at `2d8576b5`: `verdict: accept`, four completion conditions true, record byte-identical to the copy the fix committed | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), copied into § 2.4 | No — the machine's answer, not the run's prose |
| 9 | round 4 dispatched against `2d8576b5` | state spine `stage_base_commit: 2d8576b5`, `attempt: 4` | No |

## 2A. Round-3 Closure Ledger (round 4's first duty)

| Round-3 item | Severity then | Round-3 location | Round-4 reading | Owner stage of what remains |
|---|---|---|---|---|
| **N2** (its blocking, in the code record): `_declared_flow_classes()` aborted in the reader-absent shape and took two 081 legs with it | P1 + code `blocking` | `closure-acceptance-check.py:138` | **Closed, measured two ways**: the guard `if declaration_reader is None: return (), "declaration-absent: flow-class-classes"` (130-131) precedes the `try`, the same shape its sibling has carried since round 2; the scratch tree reads `rc=2` + four labels instead of `rc=1` + traceback; `tests/contract/test_gate_wiring_081.py` reads `22 passed` and both round-3 ids are green. The FR-012 fallback the same commit added is provably subordinate (§C2: a narrowed declaration refuses `execution`, which the fallback would have accepted) | — |
| **N1** a fix round's closure asserted from the commit subject, with no per-site table | P1 | `code-review.md` § 2.1; `git log -1 --format=%B e1f59096` | **Open, second occurrence**: `2d8576b5`'s whole message is `fix(084): guard the flow-class read and keep the FR-012 fallback` — accurate this time, and silent about which round-3 items it answers. REC-084-10 still unimplemented | framework (`skills/internal/review-sdd-process/SKILL.md` § 5, `templates/commit-template.md`) → REC-084-10 |
| **N2** the change that broke a deployment shape left no captured test run, and the shape leg is not in the selection algorithm | P1 | `scripts/python/closure-acceptance-check.py:138` + `tests/contract/test_gate_wiring_081.py:68` | **Open, second occurrence**: this fix round also archived no run — its only evidence file is an ARC JSON. The reading exists (`gate_wiring 22 passed`, `241 passed / 2 failed`) but only in the state spine and the dispatch brief. This round applied the shape leg by hand (§ 1 #4-#5) rather than by the algorithm | framework → REC-084-12 |
| **N3** a `pass` row's value disagrees with the reading it points at | P1 | `verification.md:70` / `:72` | **Open, unchanged**: the row still reads `31/31` while `t032-classification-readings-2026-11-05.txt:578` still reads `28/28` — see N3 | implement (`verification.md` evidence pointer) → REC-084-06 |
| **N7** a gate row and a task row still promise evidence that says the work was not done | P1 | `tasks.md:31` (GATE-2) / `:166` (T031) | **Open, unchanged**: `test-evidence/head-failed.txt` still does not exist anywhere on this branch, and T031's carrier still says `waived-by-user … No output is claimed` while the row is `[X]` — see N4 | implement (`tasks.md`) → REC-084-06 / REC-084-02 |
| **N5** the `smoke_comparison` slot has a reader that copies a sentence | P2 | `templates/verification-log-template.md:65` | **Open, unchanged**: re-read through the closure JSON, `comparison` is still `byte-identical with … (cmp exit 0)` — prose in a path-shaped slot — see N5 | implement (the recorded value) / template (the slot's reader) → REC-084-09 |
| **N4** `post_change_commit` names a commit that never touched the file | P2 | `verification.md:39` | **Open, unchanged**: still `98288d45`; the file has now been committed three times after it — see N6 | implement (`verification.md`) |
| **N6** `green-with-void` used for a user waiver | P2 | `tasks.md:26`, `:202` | **Open, unchanged**: byte-identical to rounds 2 and 3 — see N7 | template (`tasks-template.md`) → REC-084-02 |
| **F4 / F5 / F6 / F7** (round-1 framework items) | P2 | round-1 report § 3 | **All four open**: untouched by the fix — satisfied by the unchanged-status note in § 5 | REC-084-03 / 04 / 07 / 08 |
| **F16** the client-project limbs of SC-005 never ran | P2 | `verification.md:95-102` | **Open under the user's test waiver** — no scratch-tree `specify init` reading exists; the mirror limb is green (six pairs `ok`) | user waiver (residual risk, not a defect) |

**Round-3 dispositions that need no action**: the ARC verdict, both carriers of round 3's own run, and the code-blocking closure all held. The one thing round 4 adds to the ledger is that the fix did not merely stop crashing — it made the degraded shape judge again (§ 2.3).

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 2 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 3 |
| Documentation | 3 |

Round 3 closed its own blocking outright and left its other six items standing; round 4's fix touches exactly one engine, so no artifact and no template item could have moved — and none did. Two of the four P1s are now in their second or third occurrence, and both are about how a **fix round reports and proves itself** rather than about the feature's code. Two of the five P2s are new this round: the driver's own test-budget record and the register's authority paths, both of which churn every review round and neither of which is guarded.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `2d8576b5cb251ca22e90f5312564b657c04811c3` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base --spec …` reported |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 298 / 1 / 297 / 0 | copied field by field from the record's coverage receipt block |
| Segment verdict | `pass` | the record carries 0 `blocking` entries |
| Gate verdict | `allow` | `report --summary --file …` exits 0 with `blocking_entries=0`; 2 `important` entries each answered (§ the record's closure section) |
| Reason, when one applies | none | a `pass` verdict needs no basis line |
| Uncommitted scope | disclosed, never concluded over: this run's own surface is `review.md` (rewritten), `review-r3.md` (round-3 report archived), `code-review.md` (rewritten after rotation), `code-review-20261105T163841Z.md` (round-3 code record archived), the six `test-evidence/review-round4-*` files, the `stage-status.md` round-4 row, the `## Latest Review` entry in `.specify/memory/features/084.md`, the two new `REC-084-13`/`REC-084-14` rows and the twelve re-pointed `REC-084-01…12` rows in `.specify/memory/register.md`, the flipped status in `.specify/memory/features.md` + `features/084.md` (`**Status**` and § Status Tracking) and the same-commit rewrite of `verification.md`'s `notes_feature_status` line (REC-084-05: no surface may keep stating the old status); a pre-existing modified run record `session/20261102T231648Z-…-081a.md` and pre-existing untracked `memory/` records are outside the slice and were left untouched | the same sentence in [`code-review.md`](/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md) |
| Record | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` | written (triage `run`) |
| Archive | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review-20261105T163841Z.md` | round 3's record, rotated by `start` |

Six-level counts in the record: `blocking` 0 · `important` 2 · `suggestion` 4 · `nitpick` 0 · `question` 0 · `praise` 2. The one fact that decides this round is the disappearance of `blocking`: round 3's single `blocking` is closed at the site it named, and the two contract legs it took with it are green. Both `important` entries are retentions and each is answered in the record's closure section (FR-012's two readings belong to `requirements.md`; `verify`'s `residual_literals` constant belongs to C-032). The record also carries one **reading that is deliberately not a finding**: in the reader-absent shape the engine now exits 0 with `"verdict": "accept"` and no machine-readable degradation marker, and that behaviour is pinned by `test_gate_wiring_081.py`'s passing-line leg, so filing it as a defect would contradict a frozen 081 assertion — the observation is recorded where a future re-grade can find it, with no severity attached.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | requirements.md, plan.md, tasks.md, contracts/, data-model.md, quickstart.md, verification.md, research.md, feature-ref.md | derived: the standard spec-stage set ∪ `plan.md` § Project Structure § Documentation (which declares `research.md` and `feature-ref.md` in addition) — **9 members** |
| Coverage line | 9 / 9 | present members / expected members |
| Missing members | none | — |
| Segment verdict | `blocked` | two P1 traceability/acceptance findings plus four P2 rows, all unchanged from round 3 |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/084-harness-triple-structure/verification.md` | 70 | none | `SC-001_value` reads `31/31` while `SC-001_evidence` (line 72) resolves to a capture whose line 578 reads `28/28` — N3 |
| P1 | `.specify/specs/084-harness-triple-structure/tasks.md` | 31 | none | GATE-2 names `test-evidence/head-failed.txt`, a file that has never existed on this branch, while the DoD block reports the gate area green under the waiver — N4 |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 166 | none | T031 is `[X]` and its carrier exists but says the work was not done — N4 |
| P2 | `.specify/specs/084-harness-triple-structure/verification.md` | 39 | none | `post_change_commit=98288d45` names a Part-3 commit that never touched this file — N6 |
| P2 | `.specify/specs/084-harness-triple-structure/verification.md` | 57 | none | `smoke_comparison` holds a sentence where the template declares a repo-relative transcript — N5 |
| P2 | `.specify/specs/084-harness-triple-structure/tasks.md` | 26 | none | `green-with-void` used for a user waiver rather than a falsified premise — N7 |

**Why the P1 pair is still P1 and not P0.** The artifact segment's acceptance-honesty dimension makes a criterion "reported as passing without the measurement that produced that reading" a `P0` by construction. N3 is not that shape: the reading exists and is reproducible — `harness-triple-check.py --action verify` on the final tree reads `31/31` today (§ 2.3's gates file §2) — so the claim is measured and true, and what is stale is the pointer under it. A `P0` would have to be able to say the number is unsupported; it cannot. The same reading applies to GATE-2 with one difference that is stated rather than smoothed over: the file the gate names was never produced, so the gate's own id-level difference has **no** reading under it — what exists instead is the review rounds' targeted comparison against the 23-name baseline (`4 failed / 356 passed` in round 3, `2 failed / 358 passed` in round 4, zero new failures in both), which covers the modules the targeted set selects and not the five frozen gate scripts as a whole. That is why N4 stays a traceability `P1` and why it is the one item a single `ls` can still falsify.

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `3ffeb26e4880f134f7a5e220ecbffb869f165632` | the resolved diff base |
| Head commit | `2d8576b5cb251ca22e90f5312564b657c04811c3` | the run-start `HEAD`, fixed for the run |
| Base source | `feature-first-commit` | the resolution tier `git-delta-review.sh base` reported |
| Smoke command | `python3 scripts/python/harness-triple-check.py --action coverage` (run twice, byte-compared) | recorded verbatim |
| Smoke exit code | `0` | the integer the command returned, both runs |
| Smoke evidence path | `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/test-evidence/review-round4-smoke-2026-11-06.txt` | exists, non-empty; holds both runs' full stdout, both exit codes, the `cmp` exit and both sha256 values (`f9cd934a…b13473`, identical — the same digest rounds 1, 2 and 3 recorded) |
| Scope and regression verdict | **scope clean, regression clean** — the fix touches 3 paths and all of them are inside the feature's own surfaces (one engine + its byte-identical mirror + one evidence file); `sync-mirrors.py --check` exits 0 with six pairs `ok`; `git diff 4b65517c -- pyproject.toml` and `-- tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py` are both empty; the 14-file targeted set reads `2 failed / 358 passed` with both failures inside the 23-name baseline and zero new failures | the segment's own reading (`test-evidence/review-round4-gates-2026-11-06.txt`, `review-round4-targeted-2026-11-06.txt`) |
| Segment verdict | `pass` | the delta delivers what T-row it answers promises, and nothing the feature already delivered stopped working |

No implementation-segment finding this round. The three judgments in one line each: **correctness** — the guarded function returns the labelled STR-014 instance before it touches the read entry, and the compatibility tuple is only reachable when the declaration is unreadable (§ 1 #7); **scope** — no file outside the feature's surfaces and no fragment closing a row it does not answer; **regression** — the shape round 3 found broken now degrades instead of aborting, and the two 081 legs it took are back.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` | `features.md` row 084 and `features/084.md` `**Status**`, read before the flip |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/084-harness-triple-structure --json` (exit 0), never recomputed here |
| Comparison verdict | `agree` | the checker's verdict is `accept` and the claim is `Implemented` |
| Failed condition, on refusal | none — no refusal fires on this record | `completion_conditions` reads `every_final_path_pass: true`, `no_open_rows: true`, `smoke_record_pass: true`, `status_row_per_criterion: true`; `reasons: []`; the four-field smoke block reports `comparison` as well |
| Fixed item, on refusal | none | `F-ACCEPTANCE` fires only when the `pass` bucket reads zero; here it reads 2 |

**ARC does not refuse this round.** The record is byte-identical to the copy the fix committed (verified with `diff`), so the machine answer has not moved across four rounds — which is the point: the flips rounds 1–3 refused were refused by the status machine and by the segments, never by a moving ARC. The record above is the **pre-flip** reading (`claimed_status: Implemented`), which is the state the transition was judged on; after the flip the same command re-reads `claimed_status: Ready for Review` with `verdict: accept` and `pass 2` (exit 0), i.e. the comparison stays `agree` — recorded in `test-evidence/review-round4-gates-2026-11-06.txt` § 7.

## Status Transition — allowed, and the condition is named

The transition judged here is `Implemented → Ready for Review`, whose four conjunctive conditions are owned by
`templates/feature-details-template.md` § Canonical Status State Machine and are cited here, not restated.

| Condition | Reading | Verdict |
|---|---|---|
| (a) every deferred (`[~]`) task resolved or explicitly waived | `tasks.md`: `closed 32 / deferred 0 / open 0` (the checker's own `tasks` block) | satisfied |
| (b) review evidence produced | this report + `code-review.md`, both on disk | satisfied |
| (c) the current code-segment record contains no `blocking` entry | `code-review.md` carries **0** `blocking` entries; `report --summary --file` exits 0 with `gate=allow` | satisfied |
| (d) no `final`-path criterion in `blocked` / `deferred` / `fail` without a user waiver | `final_path`: 2 `pass`, 0 in every non-pass bucket | satisfied |

**The four conditions hold, so the flip is executed**: `.specify/memory/features.md` row 084 and
`.specify/memory/features/084.md` `**Status**` move `Implemented → Ready for Review` in this round's commit. What
stays open is stated rather than carried silently: the artifact segment refuses (`blocked`) on two P1s — a stale
evidence pointer and a gate row naming a file that was never produced — and both are `P1`, not `P0`, and neither is
one of the four conditions. That is the same separation rounds 1–3 relied on in the other direction: then, a `P1`
could not lift a `blocking`; now, a `P1` cannot hold a transition whose conditions are all satisfied. The residual
risk is disclosed in § 3 and remains with the owners named there.

## 3. Findings (Problems & Improvement Targets)

### N1 — A fix round still reports itself from a one-line subject, and the round it answers cannot read what it closed

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/code-review.md` § 2.1; the claiming artifact is `git log -1 --format=%B 2d8576b5`
- **Evidence** (verbatim quote, the whole message):

  ```
  fix(084): guard the flow-class read and keep the FR-012 fallback
  ```

  against what round 3 left open, read at `review-r3.md` § 2A:

  ```
  | **N1** the delta did not deliver SC-002's one-machine-read-copy property … | P1 | … | **Closed on both sides** |
  | **N3** The new `smoke_comparison` slot shipped without a reader | P1 | … | **Half closed** |
  | **N4** A closed row whose named carrier is absent … | P1 | … | **Half closed** |
  ```

- **Why it's a problem**: second consecutive round, same shape. `2d8576b5` answers exactly one item — round 3's `blocking` — and says nothing about it; the reader has to reconstruct the mapping from a diff. The subject is at least accurate this time (round 3's was not: it claimed the P1s), which is precisely the point — the honesty of the message is unverifiable either way, because no per-site table exists to check it against. REC-084-10 asked for `finding → enumerated site → commit → reading`; two rounds have now passed without one, and both rounds' closure analysis had to be rebuilt from `git show` by the next reviewer.
- **Proposed fix**: REC-084-10 as written, plus one addition this round's data supports: the table must be able to carry **"closed / not attempted / attempted and still open"** per round-3 item, because this fix closed one item and touched nothing else, and a message that had to say so would have made the review's duty trivial. Framework shape: `skills/internal/review-sdd-process/SKILL.md` § 5 gains the obligation; `templates/commit-template.md` gains the slot.

### N2 — The fix round's own test reading is still not on disk, and the selection algorithm still cannot produce it

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Automation / Scripts
- **Location**: `skills/internal/code-review/scripts/git-delta-review.sh` (the `start`/`receipt` path that archives what a run leaves) and `tests/contract/test_gate_wiring_081.py:68` (the module a shape leg would select)
- **Evidence** (verbatim quote, the fix commit's complete evidence inventory):

  ```
  $ git show --name-only --format= 2d8576b5
  .specify/scripts/python/closure-acceptance-check.py
  .specify/specs/084-harness-triple-structure/test-evidence/review-r4-closure-2026-11-06.txt
  scripts/python/closure-acceptance-check.py
  ```

  and the reading the dispatch brief and the state spine both record, which exists nowhere as a file:

  ```
  tests/contract/test_gate_wiring_081.py 22 passed；关键定向集 241 passed / 2 failed
  ```

- **Why it's a problem**: REC-084-12's second limb says a stage's targeted run MUST leave a captured evidence file, and a count in a commit message or a dispatch brief is not a reading. The fix round compiled with neither half: it captured an ARC JSON and no test output. Round 3 found the *selection* gap (a shape leg would have selected `test_gate_wiring_081.py`); round 4 shows the *capture* gap is independent of it — the counts exist, were used to justify the fix, and are unauditable. This round had to re-run the set to learn what the fix round knew (rc=1, `2 failed / 358 passed`), and the fix round's own number (241 passed / 2 failed) cannot be reproduced from the tree at all, because the set it used is not recorded either.
- **Proposed fix**: REC-084-12 unchanged, with the second limb strengthened to name the failure mode observed twice: capture is a property of the **stage**, not of the author's diligence — `start` should refuse to rotate a record whose predecessor's round produced no evidence file, or the stage should refuse to close without one. Owner: `contracts/test-budget.md` TB-05 with the carrier in `skills/sdd-loop-driver/references/efficiency-model.md` § 2.3 and `shared/guidelines/single-run-evidence.md`; the enforcement point is the code skill's `start`/`receipt` pair.

### N3 — A `pass` row's value still disagrees with the reading it points at

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:70` and its evidence pointer on line 72
- **Evidence** (verbatim quote, the row at HEAD):

  ```
  SC-001_value=candidates 83 / in-scope 13 / excluded 70 / unclassified 0; coverage exit 0; verify exit 0 with 0 findings; … consumer consistency declarations→carriers 31/31 and carriers→declarations 16/16
  ```

  and the line the row cites (`t032-classification-readings-2026-11-05.txt:578`):

  ```
  consistency-declarations-to-carriers: 28/28
  ```

- **Why it's a problem**: third appearance of the same class in four rounds (round 1's F3, round 2's N5, round 3's N3, this). The fix corrected the number in round 2 and left the pointer; the number then moved again when round 3's fix added a consumer, and the pointer still reads `28/28`. A later reader cannot tell whether `31/31` was measured or transcribed, and `closure-acceptance-check.py` cannot help — it reads `SC-00N_status` and never resolves `SC-00N_evidence`. The live reading is `31/31` (§ 2.3's gates file §2), so the value is right and the row is still not trustworthy.
- **Proposed fix**: REC-084-06's second half as written — the row's value becomes a pointer to the run's output instead of a restated pair, and a `SC-00N_evidence` that does not contain the row's own numbers goes red in the checker.

### N4 — A gate row and a task row still promise evidence that says the work was not done

- **Severity**: P1 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:31` (GATE-2) and `:166` (T031)
- **Evidence** (verbatim quote, GATE-2's named output and the file's absence):

  ```
  - GATE-2: Zero new failures on the five frozen gate scripts' existing tests, read at id level — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt -q`, then `comm -13 <implement-start baseline> head-failed.txt` prints nothing …
  ```

  ```
  $ ls .specify/specs/084-harness-triple-structure/test-evidence/head-failed.txt
  ls: cannot access '…/head-failed.txt': No such file or directory
  ```

  and T031's carrier (`notes/quickstart-run.md`), which round 3's fix created:

  ```
  **Status**: waived-by-user (2026-11-05). … quickstart S5–S8 were not executed. No output is claimed.
  ```

- **Why it's a problem**: unchanged from round 3, and now the only P1 in the ledger that a one-line edit could close. A gate whose named output never existed cannot be read as green by anyone who does not `ls`; a `[X]` row whose carrier says "No output is claimed" is the same shape with the evidence inverted. Under the user's waiver the honest row state is a waiver token **on the row**, not a tick plus a note three hundred lines below.
- **Proposed fix**: REC-084-06 as written — `validate-tasks.py` gains a carrier-existence leg (`[X]` row → named path must exist, unless the row carries `waived-by-user`), and a gate row's named output is either produced or the gate is recorded as waived on the row.

### N5 — The `smoke_comparison` slot's reader copies a sentence

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `templates/verification-log-template.md:65` and its mirror `.specify/templates/verification-log-template.md:65`; the value it consumes is `verification.md:57`
- **Evidence** (verbatim quote, the slot's own declaration and the value recorded against it):

  ```
  smoke_comparison     optional: a repo-relative comparison transcript (e.g. the second run's evidence)
                       when the smoke is a determinism comparison; …
  ```

  ```
  smoke_comparison=byte-identical with .specify/specs/084-harness-triple-structure/test-evidence/smoke-run2-2026-11-05.txt (cmp exit 0)
  ```

- **Why it's a problem**: unchanged from round 3. The reader the previous fix added copies the field into the closure JSON as `comparison` and never resolves it — no `is_file()`, no path extraction — so a fabricated or stale comparison passes condition ④ exactly as a true one does. This round re-read it through the JSON (§ 2.4) and got the same prose back. The feature that introduced the slot is also the first feature to violate its grammar, which is the strongest available evidence that an unchecked slot does not get used as written.
- **Proposed fix**: REC-084-09 extended — a slot's reader must **resolve** the value it reads (existence test, red when nothing resolves), and the slot's line must state which reading consumes it; a prose value in a path-shaped slot is an input error, not a comment.

### N6 — `post_change_commit` still names a commit that never touched the file

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/verification.md:39`
- **Evidence** (verbatim quote):

  ```
  post_change_commit=98288d45 (this segment's commit is the one carrying these files; recorded here as the parent-inclusive working tree)
  ```

  `git log --oneline -- .specify/specs/084-harness-triple-structure/verification.md` at HEAD reads `4d7270fe`, `e1f59096`, `e0453f9e`, `03a19487`, `e185da6c`, `1e4ca01e` — the file has been committed three times since the named commit.

- **Why it's a problem**: unchanged from rounds 2 and 3, and the parenthetical asserting that `98288d45` carries these files is now contradicted three times over. An anchor that points at the wrong commit is the same defect class as round 1's F12, repaired for `baseline_commit` and never for its sibling.
- **Proposed fix**: derive the field from `git log -1 --format=%h -- <file>` at write time, or drop it in favour of the baseline pair the checker actually reads.

### N7 — `green-with-void` is still used for a user waiver

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Template
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/specs/084-harness-triple-structure/tasks.md:26` and `:202`; the token's owner is `.specify/templates/tasks-template.md:52`
- **Evidence** (verbatim quote):

  ```
  **DoD Status**: green-with-void
  ```

- **Why it's a problem**: byte-identical to rounds 2 and 3 and therefore still true. The token's own definition is a row **whose premise is measurably false**; the annotation three lines below states that these rows are the user-waived scratch-tree limbs and the closure full-suite leg — not that shape. The vocabulary's escape hatch is being used for a case the vocabulary does not cover, which launders a waiver into a green, and the feature's status block rests on it.
- **Proposed fix**: REC-084-02 as written — the template's `DoD Status` domain gains the waiver case explicitly (or states that a waived row is `pending` + annotation and does not feed the status machine).

### N8 — The driver's own test-budget record still declares a budget the last two rounds did not obey

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Workflow
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/state/084-harness-triple-structure.md` — the `<!-- test-budget:begin -->` block's `test_budget_after_baseline` field versus the file's own § final 测试预算
- **Evidence** (verbatim quotes, both from the same file):

  ```
  "test_budget_after_baseline": "waived-by-user (2026-11-05: skip all tests in subsequent steps; no targeted suites, no smoke, no closure full suite; test-based evidence recorded as waived-by-user, never as pass)"
  ```

  ```
  ### final 测试预算（用户授权，2026-11-05）
  - 契约模块：`tests/contract/test_harness_triple_contract.py` → **68 passed**
  - 残余 `duplicate` 面：… → **pass / 0 findings**
  - smoke：`harness-triple-check.py --action coverage` 两次 → exit 0、逐字节一致
  ```

  and the two rounds that followed ran targeted suites regardless — round 3 read `4 failed, 356 passed`, round 4 read `2 failed, 358 passed`.

- **Why it's a problem**: the block is the machine-readable half of the budget record and it says "no targeted suites, no smoke"; the human-readable half of the same file records the authorization that produced both. Two rounds then ran fourteen-module suites and a smoke, and no surface reconciles the three. A budget recorded in a closed field that a later authorization silently widens is not a budget — and the next reader (a driver auditing the slots, or a reviewer asking whether a run stayed inside its budget) gets a wrong answer from the machine half and a right one from the prose half.
- **Proposed fix**: REC-084-14 — the budget slot is a **sequence**, not a single settled field: a later authorization appends a new entry with its own scope and date rather than living only in prose below, and the audit reads the latest entry. Owner: `skills/external/sdd-loop-driver/references/efficiency-model.md` (the budget slots) with the writer in `skills/external/sdd-loop-driver/scripts/loop-state.py`.

### N9 — The register's authority paths for twelve recommendations resolve to nothing, and every round makes it worse

- **Severity**: P2 (validated: direct re-read, subagent unavailable)
- **Category**: Documentation
- **Location**: `/storage/project/cloud-native-ai/spec-kit/.specify/memory/register.md` lines 131–142 (`REC-084-01` … `REC-084-12`)
- **Evidence** (verbatim quote, two rows of the twelve):

  ```
  | REC-084-01 | 验证日志为「两次运行逐字节一致」的 smoke 声明给一个法定载体… | `.specify/specs/084-harness-triple-structure/review.md` § 5.1 REC-084-01（F8、F15） | open |
  | REC-084-12 | `targeted-set-v1` 增加**形态腿**… | `.specify/specs/084-harness-triple-structure/review.md` § 5 REC-084-12（N2；目标 …） | open |
  ```

  and the section structure of the file those rows name — `grep -n '^### 5\.' review.md` on rounds 2, 3 and 4 returns nothing; only round 1's report has `### 5.1` … `### 5.5` (`review-r1.md:454-473`).

- **Why it's a problem**: the ID Register's row form is `identifier → one-line meaning → authority path → status`, and an authority path that resolves to no file and no section is not an authority path. Ten of the twelve rows have pointed at a section that has not existed since round 2 rewrote `review.md`; the two newest point at a file that the next rotation moves. Each rotation is itself prescribed, so the drift is not an accident of one careless edit — the rotation step and the register row form disagree about where a recommendation lives, and nothing checks.
- **Proposed fix**: REC-084-13 — a review round's rotation re-points the rows it owns at the **archived** report (`review-r1.md` § 5.1 …), and a guard asserts every `REC-…` row's authority path resolves to an existing file and, when it names a `§`, to a heading that exists. Owner: `skills/internal/manage-features` / the register's row form in `.specify/memory/register.md` § ID Register protocol, with the obligation landing on `/speckit.review`'s rotation step. **This round performs the repair for `REC-084-01…12`** (declared in § 5), which is a correction with exactly one reading — each recommendation is defined in the round-named report the row's source finding points at — and it is disclosed here rather than left silent.

## 4. What Worked — Preserve (Brief)

- The round-3 `blocking` is closed by copying the sibling's shape, not by inventing a third one: `return (), "declaration-absent: …"` before the `try`, the same two lines `_declared_path_values()` has carried since round 2 — and the restore was measured differentially (parent `rc=1` + traceback → HEAD `rc=2` + labels → HEAD with a resolvable claim: `accept`).
- The fix's own comment was checkable: a narrowed declaration in a scratch tree refuses `execution`, which the compatibility tuple would have accepted, so "a readable declaration wins" is a reading and not a claim.
- The degraded shape got *better* than "not crashing": it judges again. At HEAD, a tree without the read entry and with a resolvable claim returns `verdict: accept` with three labelled lines; at the parent the same tree died.
- The smoke surface is stable across four rounds: `sha256 f9cd934a…b13473`, identical in rounds 1, 2, 3 and 4, run twice and byte-compared each time.
- The targeted set is reproducible from the set file alone, and its 14-file membership did not change when the fix touched the same engine — which is what let this round say "zero new failures" as a comparison rather than as a hope.
- ARC's record is byte-identical to the copy the fix committed, so the flip's input is not a moving machine answer; the status machine's condition (c) did the refusing for three rounds and stopped refusing for a reason that can be read in one line of the record.

## 5. spec-kit / SDD Improvement Recommendations

**New this round.** Each is registered in `.specify/memory/register.md` in the same commit as this report.

- **REC-084-13** — Target: `.specify/memory/register.md` § ID Register protocol (row form) with the obligation landing on `/speckit.review`'s rotation step, carried in `shared/workflow/acceptance-hardening.md` § Review Composition § Records and rotation and in `templates/commands/review.md` § Output and placement. Change: (1) a review round's rotation re-points every `REC-…` row it owns at the **archived** report (`review-rN.md § …`), never at the churning `review.md`; (2) a guard asserts that every register row's authority path resolves to an existing file and, when it names a `§`, to an existing heading. Source: N9. Expected impact: a recommendation stays reachable after the report that defines it is rotated — today twelve of them are not — and the check makes the next drift a red, not a discovery.
- **REC-084-14** — Target: `skills/external/sdd-loop-driver/references/efficiency-model.md` (the budget slots) with the writer in `skills/external/sdd-loop-driver/scripts/loop-state.py`. Change: the test-budget record is a **sequence of authorizations**, each carrying its own date, scope and slot set, and the audit reads the latest entry; a later authorization MUST append an entry rather than living only in prose below the block, and the block's own settled field MUST NOT keep claiming a narrower budget than the latest entry. Source: N8. Expected impact: "did this run stay inside its budget?" becomes answerable from the machine half of the record — today the machine half says no targeted suites while two rounds ran fourteen-module suites.

**Register repair performed this round** (the correction disclosed in N9): `REC-084-01…08` re-pointed at `review-r1.md § 5.1…5.5` (the report that defines them), `REC-084-09…11` at `review-r2.md § 5`, `REC-084-12` at `review-r3.md § 5`. No row's meaning, status or id changed.

**Earlier recommendations, unchanged status** (registered, still `open`, none withdrawn): REC-084-01/02/03/04/05/06/07/08 (round 1), REC-084-09/10/11 (round 2), REC-084-12 (round 3). This round renews the need for 02 (N7), 06 (N3, N4), 09 (N5), 10 (N1) and 12 (N2), and for the first time records that 01 has been *delivered in practice* — the smoke record now carries `smoke_comparison=` and all four fields are machine-consumed — without the recommendation being withdrawn, because the general rule (a slot must name its reader) is still unguarded.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | Per-site closure table for review-fix rounds, carrying closed / not attempted / still open | `skills/internal/review-sdd-process/SKILL.md` § 5; `templates/commit-template.md` | N1 (REC-084-10) |
| P1 | Every stage's targeted run leaves a capture; `start` refuses a rotation whose predecessor round produced none | `contracts/test-budget.md` TB-05; `skills/sdd-loop-driver/references/efficiency-model.md` § 2.3; the code skill's `start`/`receipt` | N2 (REC-084-12) |
| P1 | Derive SC rows / resolve their evidence pointers instead of restating counts | `scripts/python/closure-acceptance-check.py`, `verification.md` | N3 (REC-084-06) |
| P1 | Carrier existence and a waiver token on a `[X]` row; a gate's named output produced or recorded waived | `scripts/python/validate-tasks.py`, `templates/tasks-template.md` | N4 (REC-084-06, REC-084-02) |
| P2 | The slot's reader must resolve the value it reads | `templates/verification-log-template.md` | N5 (REC-084-09) |
| P2 | `post_change_commit` derived or dropped | `templates/verification-log-template.md` | N6 |
| P2 | `DoD Status` domain names the waiver case | `templates/tasks-template.md` | N7 (REC-084-02) |
| P2 | The budget record becomes a sequence of authorizations | `skills/external/sdd-loop-driver/references/efficiency-model.md`; `loop-state.py` | N8 (REC-084-14) |
| P2 | Register rows point at archived reports, with a resolvability guard | `.specify/memory/register.md` row form; `/speckit.review` rotation step | N9 (REC-084-13) |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; no target is `external`.
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document (earlier rounds are reached by the repo-relative paths `review-r1.md` / `review-r2.md` / `review-r3.md` in the same directory).
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] **P0 validation status**: **no P0 was raised this round** (round 1 raised three, all closed by machine-readable state; rounds 2, 3 and 4 raised none). The four P1 findings were validated by direct mechanical re-read — each cites a command whose output is quoted, and N2's claim is a `git show --name-only` inventory — and none was validated by an independent read-only subagent: this topology has no dispatch capability and the declared fallback (`skills/internal/review-sdd-process/SKILL.md` § 5) was used. The weaker evidence path is disclosed rather than hidden; REC-084-04 would put it on the report's own face.
- [x] **Round-level honesty**: this run executes the flip the three previous rounds refused, and states the two things that could make that look convenient — that the fix closed one item and touched nothing else (N1/N2: it also kept its own evidence off disk), and that the artifact segment still refuses on two P1s which are not one of the state machine's four conditions. The ARC record is copied, not recomputed, and the comparison verdict `agree` refers to the pre-flip claim.

## 8. Feedback

Framework friction worth posting as feedback (one entry per unit, four units — `/speckit.review`, `skill:review-sdd-process`, `skill:review-feature-quality`, `skill:code-review`):

1. **The coverage receipt's first write still means "everything was read"** — second consecutive round to pay it. This round's judged face is one file out of 298, so the honest count required 297 hand-built `--skip-with-reason … --reason …` pairs, generated by a throwaway script because passing them by hand is not feasible. A `--judged-from-notes` or `--judged-only <path>` form would make the honest count the cheap one; round 3's feedback reported the same wall from 5-of-289.
2. **Rotation has no companion step for the register.** The review command's rotation moves `review.md` to `review-rN.md` and the handoff tells the run to register every new `REC-…` against `review.md` — a path that the next rotation invalidates. Twelve rows are already stale (N9). The fix is cheap (REC-084-13) and the cost of not fixing it compounds once per round.

No code defect from `code-review.md` is posted here — per `templates/commands/review.md` § Feedback boundary those stay in that record with their severity, file and line.
