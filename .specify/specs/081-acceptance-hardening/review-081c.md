# Review — Feature 081, slice 081c (four-segment composition + Acceptance Reality Check)

**Date**: 2026-11-03
**Branch**: `081-acceptance-hardening`
**Reviewed range**: `c46da4d2..e5afed1f` — 7 commits, 67 changed files, 4 748 changed lines:
`959e9e49` (owner § Review Composition + three fixtures + red-first part 1), `a5b82dd8` (neutral
dependency example), `4ee76e5e` (the slice's test carrier, red), `df9bbe0e` (carrier skill + slots +
command rewrite), `dc72c941` (review call site wiring + four guard re-pins + docs page),
`677b934a` (tasks row correction), `e5afed1f` (slice close).
**Excluded**: `.specify/specs/081-acceptance-hardening/notes/analyze-081c*.md`,
`test-evidence/analyze-081c*.jsonl` and the analyze/checklist reports authored before the freeze
`c46da4d2`; concurrent non-081 commits do not lie inside this range.
**Carriers**: this file and `code-review.md`. `review-081a.md`, `review-081b.md`,
`code-review-081a.md`, `code-review-081b.md` are dated records of earlier slices and were not
touched.
**Status**: `Blocked` — unchanged by this slice, and correctly so (SC-001 `blocked` at 2 of 3 call
sites, SC-002 `partial`, closure checker `block` / exit 1 / `zero-final-path-pass`).

## Verdict

This is the first run of the four-segment composition, on the slice that landed it — the dogfooding
run. Read against what it claims, the slice does land the composition: four segments in one fixed
order plus a non-delegated ARC, one content owner in `shared/workflow/acceptance-hardening.md`
§ Review Composition with the command template declaring the five per-segment fields by anchor, three
stable report slots, the review call site actually **run** (not merely named) against four fixtures,
and four guards re-pinned deliberately with their reasons in their own docstrings. The red-first
record is honest (23 failed / 9 passed, per-leg readings, and a narrowing disclosed with the
measurement that forced it).

The defects that survive are the ones a composition of this shape is most exposed to. The
`### 2.2` / `### 2.3` slots declare "no opinion body and no per-item count" and then require a
findings table with one row per finding and a one-sentence defect description (A3, `P0`) — the place
where both new segments' findings land is self-contradictory, and the contradiction was ordered by
`tasks.md` T006 itself. The `P0`/`P1`/`P2` **meanings** are defined a second time, with different
content, in the new carrier's references file while two owner statements say the meanings are written
once (A2). And the contract's FR-015 traceability cell still names the `negative` fixture for
`F-ACCEPTANCE`, a fixture this slice's own test proves can never reach that conjunction (A1).

Findings: **P0 = 1, P1 = 4, P2 = 10** (15 non-code findings); code segment: **6** findings, 3 of them
`important`, recorded in `code-review.md`. All findings are **open** — this stage judges and does not
repair; none was resolved inside the range.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 081 |
| Requirement Key | `081-acceptance-hardening` |
| Requirement Name | Stricter Acceptance & Artifact Review（更严格的验收与产物审查） |
| Related Feature | 081 — the same feature (this slice is `081c` of four) |
| Repository | `spec-kit` |
| Repository URL | `gitlab@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (the only remote; `git remote -v` lists `gitlab` only, no `origin`) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains e5afed1fd15e02eab3510f9f817056a62489e09d` is empty — the commit is unpushed. Every citation below is an absolute path plus `git show <sha>:<path>`; no `blob/` URL form is used for it |
| Branch | `081-acceptance-hardening` |
| Commit SHA | `e5afed1fd15e02eab3510f9f817056a62489e09d` (short `e5afed1f`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-03 |
| Reviewer (Agent) | SDD executor, `/speckit.review` composition run (four segments + ARC) |
| Environment | macOS (darwin/arm64); `python3` 3.9.6 (system, runs the stdlib engines); `.venv/bin/python` 3.14.6 / `pytest` 9.2.0 (test runner); `git` 2.54.0 (Apple Git-157) |
| spec-kit Source Snapshot | the reviewed checkout itself (framework source and self-hosted runtime in one tree); `HEAD` = `e5afed1f` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 271 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/requirements.md` | 25 FR / 9 SC / 17 STR; § C is this slice's scope |
| plan.md | 363 | `…/081-acceptance-hardening/plan.md` | D1–D10, 10 execution premises, 8 inherited-blocker records, mirror obligations |
| tasks.md | 285 | `…/081-acceptance-hardening/tasks.md` | slice 081c: 17 rows (T001–T017), 8 completion gates, DoD-1…DoD-9 |
| data-model.md | 206 | `…/081-acceptance-hardening/data-model.md` | entities E-1…E-9, fixture census with the `Slice` column |
| quickstart.md | 171 | `…/081-acceptance-hardening/quickstart.md` | executable scenarios S1…S9 with per-scenario premises |
| verification.md | 116 | `…/081-acceptance-hardening/verification.md` | smoke record, 9 SC status rows + ladder, copied acceptance summary |
| contracts/ (5 files) | 5 files | `…/081-acceptance-hardening/contracts/` | RC-01…RC-19, GW-*, C-*, AS-* clause sets |
| research.md | 127 | `…/081-acceptance-hardening/research.md` | R1–R9 measurements (runner, resolver, marker, driver landing points) |
| feature-ref.md | 29 | `…/081-acceptance-hardening/feature-ref.md` | Feature 081 binding + delivery surface |
| notes/red-first-evidence-081c.md | 710 | `…/081-acceptance-hardening/notes/red-first-evidence-081c.md` | the slice's pre-change readings, fixture payloads, red run, polish readings |
| code-review.md | this run | `…/081-acceptance-hardening/code-review.md` | the code segment's record (six-level family) |

## 1. Process Execution Timeline

Reconstructed from `git log c46da4d2..e5afed1f`, `.specify/state/081-acceptance-hardening.md`, and the
slice's own notes. Chronological; the pre-freeze stages are included because the slice's task list is
their product.

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | `/speckit.checklist` on the slice | `checklists/081c-2026-11-03.md`; state spine records 44 items, 22 PASS / 22 FAIL, 10 P1 (ARC count self-contradiction, negative-path fixture unreachable, census second carrier unlisted, docs-page assertion unable to go red, expected-artifact denominator unable to be falsified) | None — checklist FAIL items hand to `/speckit.analyze`, as that command states |
| 2 | `/speckit.analyze` round 1 | `notes/analyze-081c.md`, `test-evidence/analyze-081c.jsonl`: C=1 / H=8 / M=11 / L=4, gate **fail**; independent re-validation 19 confirm / 2 downgrade / 1 reject, and two corrections to the dispatch brief | None — the gate refused |
| 3 | analyze-fix part 1 (`af43a4a4`) | state spine: ownership split by layer, three new fixtures + T015–T017, ARC to seven keys, locator MUST restored, RC-12 count leg, RC-19's two pins, T010 re-pointed at the criteria owner | None |
| 4 | `/speckit.analyze` round 2 | `notes/analyze-081c-r2.md`: gate **pass**, 9/9 round-1 C/H resolved, 4 new M + 3 L | Round 2 adjudicates **C/H only** by the run's own choice — F1 below |
| 5 | analyze-fix part 2 (`c46da4d2`, the freeze) | `notes/known-items-081c.md` § Post-r2 M/L cleanup: R2-F-10…F-16 + round-1 F-11…F-21, F-24 repaired; F-22/F-23 deferred as L hygiene | None, but the M/L closure is a hand-written list, not a gate reading (F1) |
| 6 | implement part 1 (`959e9e49`) | T001 readings, T015/T016/T017 fixtures with their checker payloads, owner § Review Composition, two sibling-skill boundaries | None |
| 7 | part 1 follow-up (`a5b82dd8`) | `shared/workflow/acceptance-hardening.md:363` example rewritten to a neutral `NNN` placeholder to clear C-57 | **Yes** — no task row asks for it, and `notes/red-first-evidence-081c.md:512-521` says the repair was *not* made (F3, I1) |
| 8 | part 2a (`4ee76e5e`) — T004 | `notes/red-first-evidence-081c.md` § 7.2: `bash scripts/bash/run-tests.sh tests/contract/test_acceptance_review_composition.py -q` → `23 failed, 9 passed`, exit 1, 32 collected | None — the red precedes T005/T006/T007 |
| 9 | part 2b (`df9bbe0e`) — T005/T006/T007 | carrier skill + references, three report slots, four-segment command rewrite, 32/32 green; § 8.1 records one leg narrowed and the dependency inversion that forced it | None, disclosed |
| 10 | part 3 (`dc72c941`) — T008–T011 | review call site wired (2/3), four guard re-pins, docs page + checklist pointer, three inventory censuses 38/53/53; targeted `211 passed` (`test-evidence/tasks-081c-part3-tests.txt`, 11 modules) | None |
| 11 | part 4 — T012–T014 | T012 `28 passed` + zero inherited rows; T013 SC re-statements; T014 smoke twice exit 0/0, mirrors/regen exit 0, close set `214 passed` | **Partly** — the recorded close run carries 10 modules, not T014's 11 (A6) |
| 12 | slice close (`e5afed1f`) | verification.md, `closure-verdict-081c.json`, `smoke-081b.txt` preserved, state spine § 081c implement + slice close | None |
| 13 | tasks-stage ledger correction (`c38e92b2` + follow-up, pre-range) | `plan.md:247`: the driver re-pointed IB-004/IB-006 onto live 081c row ids, spec-only, after `pre-analyze-check --stage tasks` exited 1 on a `this-slice` carrier naming 081b's archived `T005` | **Yes** — a plan-stage artifact edited at the tasks stage; disclosed in `tasks.md` § Notes and recorded as mechanism defect F15 |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 4 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 10 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 1 |
| Command Prompt | 4 |
| Automation / Scripts | 1 |
| Workflow | 3 |
| Documentation | 6 |

Row-by-row: `### 2.2` carries 1 P0, 2 P1 and 5 P2; `### 2.3` carries 1 P1 and 3 P2; § 3 carries the
process findings (1 P1, 2 P2). 1 + 4 + 10 = 15.

The code segment's six findings live in `code-review.md` under their own six-level family and are
**not** counted above: no mapping, conversion or combined value exists between the two families, and
none is stored here.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c46da4d2` | the dispatched review range's base (explicit) |
| Head commit | `e5afed1f` | the run-start `HEAD`, fixed for the run |
| Base source | `explicit` (caller-supplied). Disclosed: this run also executed `git-delta-review.sh base --spec .specify/specs/081-acceptance-hardening`, which resolved `base=cb841d90`, `base_source=feature-first-commit` — the **feature's** first commit, not this slice's. The command passes a caller's explicit values through and invents no default, so the explicit pair governs; the two readings are both recorded rather than reconciled silently | resolution tier the code segment reported |
| Renderer mode | `renderer: text` | the code record's header marker — no interactive terminal, so no `delta` claim |
| Changed / judged / skipped / gap files | 67 / 29 / 38 / 0 | copied field by field from the coverage receipt block in `code-review.md` (generated in the review-fix); never recomputed |
| Segment verdict | `blocked` | one `important`-class defect pair (C1, C2) is unresolved and 11 `suggestion`-level items are open |
| Gate verdict | `blocking-unresolved` | no `blocking` entry was raised; the refusal literal is recorded because the segment's own open `important` items are unanswered |
| Reason, when one applies | `none` | the triage value is `run`, so neither a basis nor a `not-evaluated` reason applies |
| Uncommitted scope | none — `git status --short` is clean over the reviewed paths at the time of this run; the only path this review wrote is the two carrier files named in the header | disclosed, never concluded over; the same sentence lives in `code-review.md` |
| Record | `.specify/specs/081-acceptance-hardening/code-review.md` | written, because the triage value is `run` |
| Archive | `none` | first run — no `code-review.md` existed (`3f93fa45` renamed the previous one to `code-review-081b.md`), so nothing was rotated |

`git-delta-review.sh triage` on the same tree: `triage=run`, `basis=code path in the committed delta`
(the first 30 code paths include `scripts/python/closure-acceptance-check.py`,
`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`, `src/specify_cli/__init__.py` and 27
test modules). The six-level findings are read in `code-review.md`; this subsection carries only the
verdict and the pointers.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md` | derived per slice from the stage rules plus `plan.md` § Project Structure. Disclosed second reading: 081's own § Project Structure declares **eleven** members (the seven above plus `research.md`, `feature-ref.md`, `baseline-failed.txt`, `test-evidence/`); the strict union the owner defines therefore reads `11 / 11`, which is also full. The seven is the product the composition declares for a slice closing the standard spec stage, and it is the one the slice's own contract and carrier test pin. That the two readings differ for this feature is finding A8 |
| Coverage line | 7 / 7 | present members / expected members |
| Missing members | `none` | every expected member was found on disk (`test -e`, one probe per member) |
| Segment verdict | `blocked` | three `P1` findings and five `P2` findings are open against artifacts the slice owns |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P0 | `templates/review-template.md` | 92 | none | A3 — slots `### 2.2` / `### 2.3` declare "carries no opinion body and no per-item count" and then mandate one row per finding plus a one-sentence defect description (see § 3) |
| P1 | `contracts/review-composition.contract.md` | 46 | none | A1 — FR-015's traceability cell names the `negative` fixture for `F-ACCEPTANCE` + refusal; the slice's own test asserts that fixture can never reach the conjunction |
| P1 | `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md` | 81 | none | A2 — § A.4 defines `P0`/`P1`/`P2` a second time, with different meanings, while two owner statements say the meanings are written once |
| P2 | `verification.md` | 116 | none | A4 — the `notes=` line names `test-evidence/closure-verdict.json` as the acceptance summary's provenance while line 112 names `…-081c.json`, and its disclosure pointers name the previous slices' note files |
| P2 | `quickstart.md` | 148 | none | A5 — premise (2) says a smoke run leaves `test-evidence/smoke-081.txt` dirty; measured byte-identical, tree clean |
| P2 | `.specify/specs/081-acceptance-hardening/test-evidence/tasks-081c-slice-tests.txt` | 1 | none | A6 — the recorded close-set run carries 10 modules; `tasks.md` T014 names 11, and the missing one is RC-19's second census pin |
| P2 | `docs/reference/commands/review.md` | 33 | none | A7 — the page claims it "restates none of that content" and then restates the owner's artifact-segment prose at line 42 |
| P2 | `requirements.md` | 208 | none | A8 — the owner's derivation rule (union of stage rules and § Project Structure) and the seven-member product named by the command, the contract and the carrier skill disagree for this feature (11 vs 7 members) |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `c46da4d2` | the resolved diff base |
| Head commit | `e5afed1f` | the run-start `HEAD`, fixed for the run |
| Base source | `explicit` | the resolution tier recorded in `### 2.1`; same tier, same disclosure |
| Smoke command | `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` | recorded verbatim; this is the feature's one smoke record (`verification.md:11`) |
| Smoke exit code | `0` | run in this review: `.  [100%]` / `1 passed in 1.69s`, exit 0 |
| Smoke evidence path | `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` | exists, non-empty; **byte-stable**: `shasum -a 256` before and after this run both `1989b4ba4030bdb590865b171cd543f9cdebbaec164f6c9e5644e2cbee1d05c4`, and `git status --short` over `test-evidence/` stayed empty |
| Scope and regression verdict | Scope: one edit has no task row (I1). Regression: none found — the 11-module close set re-run here is `239 passed` exit 0, the smoke is `1 passed` exit 0 twice over, and both parity engines exit 0 (`regen` OK; `sync-mirrors` 22 / 409 / 138 / 3 / 119 / 62 files) | the segment's own reading of scope and regression |
| Segment verdict | `blocked` | three `P2` findings are open; the delta does what FR-013…FR-016 say in substance |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P1 | `templates/review-template.md` | 80 | none | I4 — the `### 2.1` field set requires the four coverage-receipt counts "copied field by field from the coverage receipt block", but no surface of the composition requires the code segment to run `receipt`, and this feature's archived records carry no receipt block (measured: `review-081a.md`/`081b`… see § 3) |
| P2 | `shared/workflow/acceptance-hardening.md` | 363 | none | I1 — `a5b82dd8` rewrites the shipped dependency example; no task row asks for it and the disclosure note says the repair was not made |
| P2 | `templates/review-template.md` | 149 | none | I2 — `[ARC_VERDICT]` is `agree`\|`refused`, but the composition never assigns a value to the case this run is in: verdict `block` with a claim that is neither `Implemented` nor `Ready for Review` |
| P2 | `templates/commands/review.md` | 2 | none | I3 — the frontmatter `description`/`short-description` still describe the two-segment process-only review, while the docs page's equivalent paragraph was rewritten |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Blocked` | the bound feature detail's claim (`.specify/memory/features/081.md:6` `**Status**: Blocked`; the registry row in `.specify/memory/features.md` agrees) |
| `final_path` record, copied verbatim (7/7) | pass 0 · blocked 1 · deferred 0 · partial 1 · fail 0 · unknown 0 · total 2 | `scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening --json-out .specify/.tmp/review-081c-verdict.json`, never recomputed here |
| Comparison verdict | `agree` | the claim survives the copied record |
| Failed condition, on refusal | `none` — no refusal applies. Disclosed: the checker's own verdict is `block` with the named reason `zero-final-path-pass`, and per the composition a `block` verdict is a non-pass that refuses the `Implemented → Ready for Review` transition on its own. That transition is not the one this feature is in: a `Blocked` feature has no such transition to refuse, and FR-003 makes `Blocked → Ready for Review` illegal by construction. The claim `Blocked` and the verdict `block` therefore agree — the two are the same fact stated by the two surfaces | named, not merely "the transition was refused" (no refusal is claimed here) |
| Fixed item, on refusal | `none` | `F-ACCEPTANCE` at `P0` is spelled exactly *when it fires*; the claim is `Blocked`, so the zero-`pass` conjunction is not reached |

```
$ python3 scripts/python/closure-acceptance-check.py \
      --spec-dir .specify/specs/081-acceptance-hardening \
      --json-out .specify/.tmp/review-081c-verdict.json
verdict: block
flow_class: execution
claimed_status: Blocked
final_path: pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2
reason: zero-final-path-pass
EXIT=1

completion_conditions  every_final_path_pass=false  no_open_rows=true
                       smoke_record_pass=true  status_row_per_criterion=true
tasks                  closed=17  deferred=0  in_progress=0  open=0        (slice 081c's tasks.md)
smoke                  present=true exit_code=0 records=1 evidence_exists=true
```

The record is **copied, not re-derived**: one program, one invocation, all seven keys verbatim above, and
no bucket re-counted from `verification.md` here. `test-evidence/closure-verdict-081c.json` is
byte-identical to this run's payload apart from the absolute `spec_dir` field (`diff` of the two payloads
with `spec_dir` dropped: no output).

**Acceptance summary, copied from the payload**: `final_path_pass=0`, `final_path_blocked=1`,
`final_path_deferred=0`, `final_path_partial=1`, `final_path_fail=0`, `final_path_unknown=0`,
`final_path_total=2`, `acceptance_verdict=block`. `total=2` is the two `final`-path criteria
(SC-001, SC-002), not the nine SCs; the other seven are `supporting` by the parent's own ruling.

**Residual risk recorded (not a waiver).** No user waiver was sought or given for this run. Nothing
in this review lifts a condition, and the refusal path above is recorded as inapplicable rather than
waived.

## 3. Findings (Problems & Improvement Targets)

Every non-code finding is expanded below with its quoted evidence — the seven rows the `### 2.2` and
`### 2.3` slot tables carry, and the three process findings this section owns. A `P2` is a severity, not
a reason to withhold the excerpt. Code-segment findings are in `code-review.md` and are not repeated
here.

### F1 — The second analyze round adjudicates only C/H, so M-level findings leave the gate with no owner

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/notes/analyze-081c-r2.md:80`
- **Evidence** (verbatim quote):

  ```
  Round 2's gate is C/H only, so the eleven M and four L rows of round 1 were not re-adjudicated.
  ```

- **Why it's a problem**: the round-2 gate can pass while eleven M findings and four L findings are
  open, and no surface states the restriction — `templates/commands/analyze.md` and
  `skills/internal/analyze-artifacts/SKILL.md` define no round semantics at all (`grep` for
  `re-adjudicat`/`round` returns nothing in either). The residue was closed by a hand-written
  paragraph, `notes/known-items-081c.md` § Post-r2 M/L cleanup, which asserts F-11…F-24 were
  repaired "in the same pass"; nothing mechanical reads that assertion, and the same file defers
  F-22/F-23. A reader comparing `gate pass` against the leftover M set cannot tell whether the set
  was closed or forgotten.
- **Proposed fix**: state the round-2 scope in the analyze owner (either "round 2 re-adjudicates the
  full severity set" or "round 2 is C/H-only and M/L residue MUST be enumerated in a machine-readable
  list with a disposition"), and make the residue list a gate input rather than prose.

### F2 — The process report has no rotation rule, and the archive form the runs actually use is unauthorised

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/review.md:133`
- **Evidence** (verbatim quote):

  ```
  **Rotation.** When a run finds an existing `code-review.md`, it first archives that file inside the same directory as `code-review-<YYYYMMDDTHHMMSSZ>.md` (UTC, second resolution) and then writes the new record.
  ```

- **Why it's a problem**: the clause covers `code-review.md` and is silent on `review.md`, so the
  report's own archive has no rule; `templates/review-template.md:301` delegates it to "unless project
  convention says otherwise". The convention that emerged is a slice key: `3f93fa45` renamed
  `review.md → review-081b.md` and `code-review.md → code-review-081b.md` — 0-line renames, neither
  timestamped. So the stated form is unexercised, the sub-rule about two runs inside one second
  cannot ever fire, and the form actually used appears nowhere in the owner.
- **Proposed fix**: give `review.md` the same rotation clause, and change the archive form to the one
  the project actually uses (`<record>-<slice>.md`) — or state the timestamped form and let a guard
  read it. State it once, in § Review Composition.

### F3 — The red-first note says a known red was left open; the next commit repaired it

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/notes/red-first-evidence-081c.md:518-521`
- **Evidence** (verbatim quote):

  ```
  It is **not** repaired here because a repair needs a decision this part cannot make — the example
  illustrates a syntax whose whole point is naming a dependency's real paths, so "rewrite the example
  to a placeholder" and "whitelist the file in `PRE_EXISTING_NEUTRALITY_DEBT`" are two different
  readings of what C-57 wants, and either one edits 081b's landed schema example. Surfaced for the
  orchestrator (081b residue or 081d's sweep), with GATE-2 at slice close in mind.
  ```

- **Why it's a problem**: `a5b82dd8 fix(081c): keep the shipped dependency example neutral` is the
  **next commit** after the note was written and it takes the first of the two readings. The note is
  the slice's designated disclosure record and its § 6 declares it append-only; no later section
  records the repair. A reader — or the next review — is told a red is outstanding when the tree is
  green, and is told a decision is someone else's when it was already taken.
- **Proposed fix**: append a § recording the repair, the commit and the reading that closed it — or,
  better, make the disclosure record machine-checked against the guard's final state so a
  "not repaired" claim cannot outlive the repair.

### A3 — The two new report slots forbid the very content they mandate (`P0`)

- **Severity**: P0
- **Category**: Template
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md:92`
  (and `:115` for the sibling slot; the tables they contradict are at `:105` and `:131`)
- **Evidence** (verbatim quotes, both from the same slot):

  ```
  > Verdicts and pointers only: this slot carries no opinion body and no per-item count. The dimension set, the
  > finding form and the denominator's consequence are owned by
  > `.specify/skills/internal/review-feature-quality/SKILL.md` § Segment A — Artifact Review, …
  ```

  ```
  | Severity | Artifact path | Line | Why the line is absent | Finding |
  |----------|---------------|------|------------------------|---------|
  | [ARTIFACT_FINDING_SEVERITY] | [ARTIFACT_FINDING_PATH] | [ARTIFACT_FINDING_LINE] | [ARTIFACT_FINDING_LINE_REASON] | [ARTIFACT_FINDING_SUMMARY] |
  ```

- **Why it's a problem**: the preamble and the table below it are two instructions about one slot, and
  obeying the preamble deletes the table. `[ARTIFACT_FINDING_SUMMARY]` is glossed as "One sentence
  naming the defect and the section that would fix it" — that is an opinion body by any reading — and
  "one row per finding" is a per-item count. `### 2.1`'s identical preamble is coherent because that
  slot has no findings table and points at `code-review.md`; `2.2`/`2.3` copied the sentence and then
  added the table. The consequence is not cosmetic: SC-006 requires every finding in a produced
  `review.md` to carry severity, artifact path and line, and the slots are the only place the artifact
  and implementation findings live. It was ordered: `tasks.md:124` (T006) told the row to "state in
  each slot that it carries verdicts and pointers only — no opinion bodies, no per-item counts" *and*
  to build the findings tables in the same slot. The analyze gate did not catch the collision.
- **Proposed fix**: state the resolution the slot actually needs — "verdicts and finding rows only; no
  narrative opinion body and no severity roll-up, which lives in § 2's summary" — in both slots, and
  amend T006's instruction in `tasks.md` so the row and its product agree.

### A1 — FR-015's traceability cell names a fixture that cannot produce the item it claims (`P1`)

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/contracts/review-composition.contract.md:46`
- **Evidence** (verbatim quote):

  ```
  | FR-015 | RC-13…RC-16 | `tests/contract/test_acceptance_review_composition.py` (negative fixture: `F-ACCEPTANCE` + refusal) |
  ```

- **Why it's a problem**: the clause's carrier fixture is named as `negative`, and the module this
  slice landed asserts the opposite in the same breath —
  `test_f3_the_refusal_fires_on_the_blocked_case_and_cannot_fire_on_negative` asserts
  `_arc_item(negative_payload) is None` precisely because `negative` claims `Planned`
  (measured payload: `claimed_status: Planned`). Both `data-model.md:199` and `tasks.md:242` name
  `review-implemented-blocked` as the only input that reaches RC-15's conjunction. A reader verifying
  FR-015 against the contract drives the wrong fixture, sees no `F-ACCEPTANCE`, and has two wrong
  explanations available (the implementation is broken, or the item was measured and passed) — the
  false-green reading the feature exists to remove. Note the cell was written before the analyze fix
  that introduced the two new fixtures and was never revisited.
- **Proposed fix**: change the cell to `review-implemented-blocked` and, so this cannot recur, make
  the traceability cell name the fixture by the id `data-model.md`'s fixture census assigns it.

### A2 — The `P0`/`P1`/`P2` meanings are defined twice, differently (`P1`)

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/skills/internal/review-feature-quality/references/artifact-and-implementation-review.md:81`
- **Evidence** (verbatim quotes — the second definition, then the two statements it contradicts):

  ```
  - `P0` — a reader acting on the artifacts would be misled, or the slice's acceptance claim is false: a
    missing required artifact, a `pass` without its measurement, a red-first claim with no red run, a
    broken traceability link whose far end is the acceptance evidence.
  - `P1` — a defect every later slice pays for: the same fact stated twice, a row that names no owner, a
    premise copied instead of referenced.
  ```

  ```
  - **Severity vocabulary**: `P0`/`P1`/`P2` — the family owned by
    `skills/internal/review-sdd-process/SKILL.md` § Severity Vocabulary. This segment emits those three
    tokens as a consumer and defines no level of its own; the meanings are written once, in the report
    template's severity table, and are not repeated here.
  ```

  ```
  What each level **means** in a review report is written once, in `templates/review-template.md` § Findings Summary's severity table; this section owns the family and its closure, not a second copy of those meanings.
  ```

- **Why it's a problem**: one family, two meaning-sets, and they are not paraphrases of each other.
  `templates/review-template.md:58` says `P0` "Blocks correct use of spec-kit, or creates silent
  corruption risk. Fix before next spec."; § A.4 says `P0` is "a reader acting on the artifacts would be
  misled, or the slice's acceptance claim is false". `P1`: "Recurring friction across specs" versus "a
  defect every later slice pays for". A finding can therefore be `P0` under one reading and `P2` under
  the other, and a review's severity counts become a function of which file the grader opened first.
  § A.4's own `P1` definition — "the same fact stated twice" — is satisfied by § A.4 itself.
- **Proposed fix**: delete § A.4 and replace it with a pointer plus, at most, the *grading procedure*
  ("apply the owner's table") — the carve-out § A.4 really wants (artifact findings graded by
  consequence to a reader of the artifacts) belongs as an explicit scope note on the owner's table,
  not as a second table.

### A4 — The acceptance summary names two different provenance files, in one file (`P2`)

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/verification.md:116`
- **Evidence** (verbatim quotes, both from `verification.md`):

  ```
  final_path_source=test-evidence/closure-verdict-081c.json (byte-identical copy of `.specify/.tmp/081c-closure-verdict.json`, …)
  ```

  ```
  Provenance of the acceptance summary above: it is copied from test-evidence/closure-verdict.json (produced by the checker with --json-out), never recomputed by hand.
  ```

- **Why it's a problem**: both files exist and are different payloads — `closure-verdict.json`
  (1107 B, 081a-era) and `closure-verdict-081c.json` (1103 B, this slice's). The same line also carries
  two stale disclosure pointers: "notes/known-items.md (F12 recorded, F13 fixed, F14 deferred to 081d)"
  and "notes/driver-completions.md (the three stages the loop driver completed…)". `notes/known-items.md`
  is the 081a/081b cumulative record whose items are F12–F14; this slice's known items are F15–F24 in
  `notes/known-items-081c.md`, and `notes/driver-completions.md` contains 081a entries only. The
  paragraph was carried forward when the rest of the line was rewritten for 081c.
- **Proposed fix**: name `closure-verdict-081c.json` in both places, and re-point the two disclosure
  pointers at `notes/known-items-081c.md` and (for 081c) whatever completion record applies — or say
  "no driver completion was recorded for 081c" instead of citing the 081a record.

### A5 — "A smoke run leaves the tree dirty" is refuted by the smoke run (`P2`)

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/quickstart.md:148`
  (the same claim is the owning record at `notes/known-items.md:14`, F12)
- **Evidence** (verbatim quote):

  ```
  the test uses `tmp_path` for every fixture it creates, so nothing is written outside the pytest temp root **except** `<spec-dir>/test-evidence/smoke-081.txt`, which is a **tracked** file — running the smoke rewrites it, so `git status` shows that file dirty after a run. That is the evidence-writing mechanism, not drift: review the diff and commit it deliberately rather than reverting it
  ```

- **Why it's a problem**: measured in this review, the rewrite is byte-identical:
  `shasum -a 256 …/smoke-081.txt` → `1989b4ba4030bdb590865b171cd543f9cdebbaec164f6c9e5644e2cbee1d05c4` before
  and after, and `git status --short` over `test-evidence/` printed nothing. The smoke module says so
  itself (`tests/integration/test_acceptance_smoke.py:23-24`: "two runs of this module write a
  byte-identical file and their exit codes are the only thing that can differ"). So the artifact
  instructs a reviewer to look for a diff that does not exist and to "commit it deliberately", while
  the code it describes guarantees there is nothing to commit. F12 grades it "recorded, no change — the
  mechanism is intended"; the mechanism is intended and the consequence is misdescribed.
- **Proposed fix**: restate premise (2) and F12 as "the file is rewritten in place and is byte-stable
  across runs, so a clean `git status` is the expected reading; a *dirty* file means a sub-check's
  output moved, which is the signal" — which is strictly more useful than the current text.

### A6 — The recorded close-set run is not the run its own row specifies (`P2`)

- **Severity**: P2
- **Category**: Automation / Scripts
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/test-evidence/tasks-081c-slice-tests.txt:1`
- **Evidence** (verbatim, the recorded command; `tasks.md:141` T014 names the same list **plus**
  `tests/contract/test_client_guard_sweep.py`):

  ```
  # test runner: .venv/bin/python -m pytest tests/contract/test_acceptance_review_composition.py tests/contract/test_review_code_composition.py tests/contract/test_review_feedback_boundary.py tests/contract/test_status_gate_owner.py tests/contract/test_review_docs_isomorphism.py tests/contract/test_gate_wiring_081.py tests/contract/test_skill_layer_visibility_guards.py tests/contract/test_expression_compatibility.py tests/contract/test_migration_distribution.py tests/contract/test_acceptance_premises.py -q
  … 214 passed in 9.53s
  ```

- **Why it's a problem**: ten of the eleven modules. `214 = 211 − 25 + 28` — the part-3 run
  (`tasks-081c-part3-tests.txt`, 211 passed) included `test_client_guard_sweep.py`, and the close run
  dropped it while adding `test_acceptance_premises.py`. The dropped module is the census's **second
  carrier** and RC-19's explicit subject; `verification.md:116` then reports "Close set `214 passed`"
  as the slice's close evidence. The fact holds — this review re-ran the eleven-module set and got
  `239 passed in 21.89s`, exit 0 — but the authoritative record does not contain the reading its own
  row specifies, so a later reader cannot tell "green" from "not run".
- **Proposed fix**: re-run and re-record the exact eleven-module command T014 names; the row and its
  evidence should be generated from one source.

### A7 — The docs page says it restates nothing and restates the owner (`P2`)

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/docs/reference/commands/review.md:33`
- **Evidence** (verbatim quotes — the claim, then the row below it):

  ```
  Each segment's judgment object, boundary sentence and severity family are owned by `shared/workflow/acceptance-hardening.md` § Review Composition; this page states the surface and restates none of that content.
  ```

  ```
  | 2 | Artifact segment | `review-feature-quality` § Segment A (`.specify/skills/internal/review-feature-quality/SKILL.md`) | the slice's stage artifacts, taken as the expected set — completeness, internal consistency, traceability, dependency and premise ownership, acceptance honesty |
  ```

- **Why it's a problem**: the owner's boundary sentence is "…judged for completeness, internal
  consistency, traceability (FR → task → SC → evidence), dependency and premise ownership, and
  acceptance honesty" — the page reproduces the same five nouns in the same order, one parenthetical
  dropped. The owner forbids exactly this at
  `shared/workflow/acceptance-hardening.md:463`: "Every other surface — the report template, the two
  sibling skills, the docs page — reaches this content by path plus `§ Review Composition`", and a copy
  of the segment prose at such a surface "is a defect". `test_review_docs_isomorphism` only requires
  the four segment **concepts** to be declared, so the judgment-object column can become a
  `see § Review Composition` pointer without any guard going red — the duplication is not forced.
- **Proposed fix**: replace the four judgment-object cells with a one-line pointer to the owner
  (keeping the segment name and the skill path per row), and keep the sentence at line 33 — it is
  correct once the table stops contradicting it.

### A8 — The denominator's derivation rule and the set it names disagree for this feature (`P2`)

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/requirements.md:208`
  (the rule's owner is `shared/workflow/acceptance-hardening.md:530-537`; the seven-member / per-feature-product sentence is at `:543-545`)
- **Evidence** (verbatim quote, the SC that restates the derivation):

  ```
  覆盖率 = 已判定成员 / 期望集大小；应当存在而缺失的产物记 finding 并计入未覆盖，不得落到分母之外
  ```

- **Why it's a problem**: the owner defines the expected set as "the union of what the slice's stage
  rules require it to have produced for the stage it is closing, and what that feature's `plan.md`
  **§ Project Structure** declares it owns", and then names seven members as the product "for a
  feature whose plan declares the standard spec set". Feature 081's own plan declares **eleven**
  (`plan.md:126-137`: the seven plus `research.md`, `feature-ref.md`, `baseline-failed.txt`,
  `test-evidence/`), and all eleven are on disk. Applied literally, the rule yields 11; the command,
  the contract RC-06 and the carrier skill each name 7. Both readings are full coverage here, so no
  number is at stake — but the first feature to run the segment had to choose a denominator from two
  disagreeing definitions, and nothing in the owner says which of the two numbers a run should print.
- **Proposed fix**: make the owner's product sentence explicit about its scope — "the seven is the
  product when the plan declares nothing further; a plan declaring additional artifacts extends the
  set, and the run MUST print the size it used" — so a run reads one number, not two.

### I4 — `### 2.1` mandates coverage-receipt counts, but nothing requires the receipt (`P1`)

- **Severity**: P1
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md:80`
- **Evidence** (verbatim quote — the mandated field):

  ```
  | Changed / judged / skipped / gap files | [CHANGED_COUNT] / [JUDGED_COUNT] / [SKIPPED_COUNT] / [GAP_COUNT] | copied field by field from the coverage receipt block; never recomputed, re-aggregated, or read off the record's prose |
  ```

- **Why it's a problem**: the field presumes a receipt block, and no surface of this composition
  requires the code segment to produce one. The `code-review` skill does have the deterministic step
  (`git-delta-review.sh receipt --review-file <record>`, step 4 of its non-interactive path, described
  there as "回执是「已读全 diff」的唯一证据形态"), but `/speckit.review` § Composition never invokes it
  — and this feature's two archived records carry no receipt block at all
  (`code-review-081a.md`, `code-review-081b.md`: `grep` for the receipt finds nothing; the last record
  that has one is `071-review-code-integration/code-review.md`). So the first run after this field
  landed cannot fill it, and this run is that run: the counts above are a hand-authored disclosure,
  labelled as such, which is exactly the "prose" the field forbids. A field that cannot be filled from
  the record it describes invites a fabricated number.
- **Proposed fix**: make step 4 of the code skill's non-interactive path mandatory for the composed
  run (the command names it, the way it names `base`/`triage`), and let the record's absence of a
  receipt block be an input error rather than a prose-filling occasion.

### I1 — An edit inside the delta has no task row (`P2`)

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/shared/workflow/acceptance-hardening.md:363`
- **Evidence** (verbatim, the diff `a5b82dd8` applies):

  ```
  -- `071`: `.specify/memory/features/071.md`, `.specify/specs/071-review-code-integration/verification.md`
  +- `NNN`: `.specify/memory/features/NNN.md`, `.specify/specs/NNN-<slug>/verification.md`
  ```

- **Why it's a problem**: the change is correct — it clears the pre-existing C-57 neutrality failure
  disclosed in `notes/red-first-evidence-081c.md:512` — but it is not asked for by any FR and no row of
  `tasks.md` (T001–T017) names it. Its only record is the state spine
  (`.specify/state/081-acceptance-hardening.md` § 081c implement), which is not one of the slice's task
  carriers, and § Inherited Blockers' example is 081b's schema text, so the edit reaches outside this
  slice's declared subject while sitting inside a file the slice does own. The implementation segment's
  scope judgement is "no work that no requirement and no task row asks for"; this is that, disclosed in
  one place and undeclared in the one place the segment reads.
- **Proposed fix**: either add the row (a `[P]` hygiene row "clear the pre-existing C-57 neutrality
  failure in the shipped dependency example") or record the change under an existing row's description;
  a delta edit with no row is indistinguishable from scope creep in a later audit.

### I2 — `[ARC_VERDICT]` has no value for the run it just met (`P2`)

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/review-template.md:149`
- **Evidence** (verbatim quotes — the field, then the clause that leaves its third case unstated):

  ```
  | Comparison verdict | [ARC_VERDICT] | `agree` or `refused` |
  ```

  ```
  The checker's verdict is a closed two-value set — `accept` and `block` — and `block` is a **non-pass**: it refuses the transition on its own, whatever the claim reads, and it is never carried beside an `accept` as a caveat.
  ```

- **Why it's a problem**: two rules can be read for the state this run is in (verdict `block`, claim
  `Blocked`, and no `Implemented → Ready for Review` transition in play): "`block` refuses on its own,
  whatever the claim reads" points at `refused`; `[ARC_VERDICT]`'s own gloss — "`agree` when the claimed
  status survives the copied record" — points at `agree`, because a `Blocked` claim and a `block`
  verdict are the same fact. `accept`/`block` and `agree`/`refused` are two different binary alphabets
  and the composition never maps them for the claim-not-`Implemented` case. Every review of a blocked
  feature lands here, so the ambiguity is not exotic — it is the default state of this feature.
- **Proposed fix**: state the pairing explicitly, e.g. "`agree` when the checker's verdict is `block`
  *and* the claimed status is already `Blocked`/`Planned`; `refused` when the verdict is `block` **and**
  the claim is `Implemented`/`Ready for Review`, or when `F-ACCEPTANCE` fires" — one sentence, in §
  Review Composition.

### I3 — The command's registration face still describes a two-segment review (`P2`)

- **Severity**: P2
- **Category**: Command Prompt
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/review.md:2`
- **Evidence** (verbatim quote of the frontmatter, unchanged by this slice):

  ```
  description: Critically review the SDD process for the current feature and produce a self-contained, improvement-focused report for the spec-kit maintainers.
  short-description: 批判性评审当前特性的 SDD 过程，出具改进导向报告
  ```

- **Why it's a problem**: this is the text an agent CLI shows a user choosing a command, and it
  describes the pre-change composition — process segment only, one report. The command now also judges
  the artifact set and the implementation delta and runs ARC, and it produces a second artifact
  (`code-review.md`). The slice treated the equivalent text as in scope elsewhere: the docs page's
  opening paragraph was rewritten to the four-segment wording (`docs/reference/commands/review.md:3`),
  and the process skill's `description` was reworded for the same reason (T003). The composition
  declares only `scripts:`, `## Wrap-up` and `## Handoffs` unchanged (`shared/workflow/acceptance-hardening.md`
  is silent on frontmatter; `templates/commands/review.md:139`), so this face was neither frozen nor
  updated. A model selecting among commands still reads "process review only".
- **Proposed fix**: reword `description` (and `short-description`) to the four-segment surface, in the
  same change as the body — the file the copies are generated from, so the four per-tool copies follow.

## 4. What Worked — Preserve (Brief)

- The two-layer split (content in `shared/workflow/acceptance-hardening.md` § Review Composition,
  declaration by anchor in `templates/commands/review.md` § Composition) held: the command declares four
  headings and five fields and inlines no dimension list, and the A3 defect above is the one place the
  split was violated.
- `test_acceptance_review_composition.py`'s anti-vacuity test
  (`test_the_judges_reject_near_misses_so_no_leg_is_a_bare_string_test`) proves the three judges it
  leans on can each reject a near miss — that is the guard-a-guard pattern worth copying, not just the
  guard.
- Leg (d) **applies** the declaration instead of asserting it: `expected-artifact-missing` reads
  `6 / 7` with one named finding under the expected set and `6 / 6` with none under "the ones that
  exist", and the leg asserts the two readings differ. The denominator cannot silently regress.
- Leg (i) extracts the documented invocation from the command template and **runs** it against four
  fixtures, so the call site is a verdict rather than a string match — and the four fixtures were
  rebuilt (T015–T017) precisely because the older two could not discriminate.
- The four census/inventory guard updates name, in their own docstrings, what they used to assert,
  why the assertion moved, and what would still be red if it had not; none was deleted and each is
  still a verbatim pin (`test_client_guard_sweep.py`, `test_review_feedback_boundary.py`,
  `test_expression_compatibility.py`, `test_migration_distribution.py`,
  `test_skill_layer_visibility_guards.py`).
- The red-first record is a measurement, not a memo: a real console tail, a real failing count (23),
  per-leg first assertions, the nine green tests named *with why they were already green*, and one
  narrowed leg disclosed with the dependency inversion that forced it.

## 5. spec-kit / SDD Improvement Recommendations

### 5.1 Template Improvements

- **REC-T1 — resolve the slot contradiction.** Target: `templates/review-template.md` (§ 2.2 at line 92,
  § 2.3 at line 115). Change: replace "carries no opinion body" with the resolution the tables need
  ("verdict rows and finding rows only; narrative opinion and severity roll-ups live in § 2"), keeping
  the pointer to the carrier skill. Source: A3. Expected impact: the two new segments' findings have a
  home they are not forbidden to use.
- **REC-T2 — give `review.md` a rotation rule and one archive form.** Target:
  `shared/workflow/acceptance-hardening.md` § Review Composition (the Rotation paragraph, currently
  cited from `templates/commands/review.md:133`). Change: state the report's rotation, and use the form
  the project already exercised (`<record>-<slice>.md`). Source: F2. Expected impact: no run has to
  invent an archive name, and the "two runs in one second" sub-rule stops being dead text.
- **REC-T3 — state the ARC comparison pairing.** Target: `templates/review-template.md:149` +
  `templates/commands/review.md:95`. Change: one sentence pairing `accept`/`block` with
  `agree`/`refused` for the claim-not-`Implemented` case. Source: I2. Expected impact: every review of a
  blocked feature reads its verdict off the rule instead of choosing one.

### 5.2 Command Prompt Improvements

- **REC-C1 — reword the command's frontmatter description.** Target: `templates/commands/review.md:2-3`.
  Change: four-segment surface in `description` and `short-description`; regenerate the copies. Source:
  I3. Expected impact: a user (or a model) selecting the command sees what it does.
- **REC-C2 — require the coverage receipt in the composed run.** Target:
  `templates/commands/review.md` § Segment 4. Change: name `receipt --review-file <record>` as a step the
  composed run performs, the way it names `base`/`triage`; an absent receipt block becomes an input
  error. Source: I4. Expected impact: the `### 2.1` count field becomes fillable from the record it
  describes.
- **REC-C3 — state the second analyze round's scope.** Target: `templates/commands/analyze.md` (or the
  analyze skill). Change: declare whether a verification round re-adjudicates M/L or only C/H, and make
  M/L residue a machine-readable list with dispositions. Source: F1. Expected impact: a green gate stops
  implying a closed finding set.

### 5.3 Automation / Script Improvements

- **REC-A1 — one source for a row and its evidence.** Target: `scripts/python/run-tests.sh` usage in
  `tasks.md` completion rows. Change: let a row's evidence file record the command it ran, and have the
  close-set check compare the recorded module list against the row's list. Source: A6. Expected impact:
  "the recorded run is not the specified run" becomes a failing assertion instead of a hand-read.

### 5.4 Workflow Improvements

- **REC-W1 — make a disclosure record falsifiable.** Target: the red-first/known-item convention
  (`notes/red-first-evidence-081c.md` § 5, `notes/known-items-081c.md`). Change: a "not repaired here"
  row MUST name the guard that would go green when it is repaired, so the next run can check the claim
  against the tree. Source: F3. Expected impact: a disclosure cannot outlive its subject.
- **REC-W2 — give a delta edit a row or a reason.** Target: `tasks.md` DoD set. Change: add the
  symmetric duty to DoD-1's "every row's artifact exists" — every *edit* in the delta names a row, or the
  slice records why an out-of-row edit was unavoidable. Source: I1. Expected impact: scope judgement
  stops depending on whether the driver remembered the state spine.

### 5.5 Documentation Improvements

- **REC-D1 — collapse the duplicated severity meanings.** Target:
  `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md:79-87`.
  Change: delete § A.4 and point at `templates/review-template.md` § Findings Summary; if a grading
  procedure is wanted, state it as a procedure, not as three new definitions. Source: A2. Expected
  impact: one family, one meaning-set, and a review's severity counts stop depending on which file was
  opened.
- **REC-D2 — re-point FR-015's traceability cell.** Target:
  `contracts/review-composition.contract.md:46`. Change: `review-implemented-blocked`, named as
  `data-model.md`'s fixture census names it. Source: A1. Expected impact: the clause's carrier can
  produce the item the clause claims.
- **REC-D3 — re-point the docs page's judgment-object column at the owner.** Target:
  `docs/reference/commands/review.md:42-45`. Change: pointer per row, keep the segment names and skill
  paths. Source: A7. Expected impact: the page's own claim ("restates none of that content") becomes true.
- **REC-D4 — refresh `verification.md`'s disclosure tail.** Target: `verification.md:116`. Change: one
  provenance file (`closure-verdict-081c.json`), and note pointers at this slice's own note files.
  Source: A4. Expected impact: the acceptance summary has one source, and the disclosures resolve.
- **REC-D5 — restate the smoke's dirtiness reading.** Target: `quickstart.md:148` (and
  `notes/known-items.md:14`). Change: "rewritten in place, byte-stable across runs; a *dirty* file is the
  signal". Source: A5. Expected impact: a reviewer stops looking for a diff that cannot exist.
- **REC-D6 — make the denominator's product explicit about its scope.** Target:
  `shared/workflow/acceptance-hardening.md` § The artifact denominator is the expected set. Change: state
  that a plan declaring more than the standard set extends the denominator, and that the run prints the
  size it used. Source: A8. Expected impact: the first run of the segment stops having to pick between
  two numbers.

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P0 | Resolve the `### 2.2`/`### 2.3` slot contradiction | `templates/review-template.md` § 2.2 / § 2.3 | A3 |
| P1 | Collapse the duplicated severity meanings | `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md` § A.4 | A2 |
| P1 | Re-point FR-015's traceability cell | `contracts/review-composition.contract.md` | A1 |
| P1 | Require the coverage receipt in the composed run | `templates/commands/review.md` § Segment 4 | I4 |
| P1 | State the second analyze round's scope | `templates/commands/analyze.md` | F1 |
| P2 | Rotation rule for `review.md`; one archive form | `shared/workflow/acceptance-hardening.md` § Review Composition | F2 |
| P2 | ARC verdict pairing for a non-`Implemented` claim | `templates/review-template.md` § 2.4 | I2 |
| P2 | Reword the command's frontmatter description | `templates/commands/review.md` | I3 |
| P2 | Docs page restatement → pointer | `docs/reference/commands/review.md` | A7 |
| P2 | Denominator scope note | `shared/workflow/acceptance-hardening.md` | A8 |
| P2 | `verification.md` disclosure tail | `verification.md` | A4 |
| P2 | Smoke dirtiness reading | `quickstart.md` / `notes/known-items.md` | A5 |
| P2 | Row and evidence from one source | `tasks.md` completion rows / `run-tests.sh` | A6 |
| P2 | Falsifiable disclosure records | `notes/*` convention | F3 |
| P2 | Every delta edit has a row or a reason | `tasks.md` DoD set | I1 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary); no absolute-only target exists in this report.
- [x] Every finding in Section 3 carries a quoted excerpt that lets the reader judge the problem
      without opening the source file; every `### 2.2`/`### 2.3` row carries severity, path and line.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside
      this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in this report except where a token is quoted as
      *evidence of a defect* (A3's table row, I4's field row, I2's field row) — quoted, not filled.
- [x] Section 4 is short and bullet-only.
- [x] Section 5 recommendations each cite an exact target file and at least one source finding id.
- [x] P0 validation status stated explicitly: **one P0 finding was raised (A3)**, and it was validated
      by direct re-read of `templates/review-template.md:92`/`:115` against `:105`/`:131` and against
      `tasks.md:124` — the two instructions are quoted verbatim in § 3. No independent subagent
      validator was dispatched for this run; the weaker path is disclosed here rather than implied
      (`(validated: direct re-read, subagent unavailable)` — the run has no subagent surface).

## 8. Feedback

This document is the process- and artifact-side review of slice 081c. The code-side review is the
separate record `code-review.md`. The feature remains `Blocked`; nothing in this report moves it, and
the slice's own claim (`Blocked`, 2 of 3 call sites) survives the Acceptance Reality Check above.

## Review-fix dispositions (081c)

All P0/P1 findings were repaired in the review-fix commit; P2s were fixed or recorded.

| Finding | Disposition | Evidence |
|---|---|---|
| A3 (P0) — the two new slots forbid the content they mandate | **Fixed**: the slot preambles now read "verdicts and finding rows only — no narrative opinion body and no severity roll-up"; the findings table is the required per-finding record; T006's instruction was aligned | `templates/review-template.md`; `tasks.md` T006 |
| F1 (P1) — round 2 adjudicates C/H only | **Fixed**: the analyze skill states round semantics and requires a machine-readable residue list for M/L; this slice's residue is enumerated in `analyze-081c-r2.jsonl` (`R2-RESIDUE`, 22 entries) | `skills/internal/analyze-artifacts/SKILL.md`; `test-evidence/analyze-081c-r2.jsonl` |
| A1 (P1) — FR-015 traceability names the wrong fixture | **Fixed**: the cell names `review-implemented-blocked` and says `negative` cannot produce the item | `contracts/review-composition.contract.md` |
| A2 (P1) — two severity meaning sets | **Fixed**: the second set is deleted; the segment applies the owner's table with a stated grading procedure | `skills/internal/review-feature-quality/references/artifact-and-implementation-review.md` |
| I4 (P1) — the receipt is not required | **Fixed**: mandatory receipt step, missing block = input error, and this record now carries the receipt | command, code skill, template, `code-review.md` |
| F2 (P2) — rotation form | **Fixed**: owner rule `<record>-<slice>.md` + timestamp fallback; `test_c12` re-pinned | owner doc; guard |
| F3 (P2) — the note says a red was left open | **Fixed**: § 10 records `a5b82dd8` and the reading that closed it | `notes/red-first-evidence-081c.md` |
| A4 (P2) — two provenance files | **Fixed**: both places name `closure-verdict-081c.json`; the stale pointers now name `known-items-081c.md` and state no 081c driver completion exists | `verification.md` |
| A5 (P2) — the smoke "leaves the tree dirty" | **Fixed**: the rewrite is byte-identical; a clean tree is expected and a dirty file is the signal | `quickstart.md`; `notes/known-items.md` F12 |
| A6 (P2) — the close set omitted a module | **Fixed**: T014 now names 11 modules; the close run is `239 passed` | `tasks.md` T014; `test-evidence/tasks-081c-slice-tests.txt` |
| A7 (P2) — the docs page restates the owner | **Fixed**: judgment-object cells are pointers | `docs/reference/commands/review.md` |
| A8 (P2) — the denominator's product | **Fixed**: the owner says the seven is the default and a plan declaring more extends the set; the run prints the size | `shared/workflow/acceptance-hardening.md` |
| I1 (P2) — an edit with no task row | **Fixed**: T018 records the neutrality edit (`a5b82dd8`) | `tasks.md` |
| I2 (P2) — the ARC verdict alphabet | **Fixed**: owner + template state the mapping | owner doc; template |
| I3 (P2) — the registration face | **Fixed**: frontmatter describes four segments + ARC | command |
