# Review — Feature 081, slice 081d (four-segment composition + Acceptance Reality Check)

**Date**: 2026-11-03
**Branch**: `081-acceptance-hardening`
**Reviewed range**: the dispatch names `54ad418d..a8dbb599` — "the reconciliation to the feature close".
Read strictly that is commit `a8dbb599` alone (10 files, no code path); this run reviews the
**inclusive span** `f29b6178..a8dbb599` — `54ad418d` (the 19-failure frozen-surface reconciliation:
12 test files re-pinned) plus `a8dbb599` (feature-level readings, `verification.md` close, status
landing, `CHANGELOG.md`) — 25 files, 12 code paths, 865 added / 121 deleted lines. The earlier 081d
implementation commits (`8ceaeb7a` vocabulary owner rules + SC-002 composition run, `fc6811c6` line
state `blocked` + driver gate, `f29b6178` audit mode + vocabularies + schema guard) were read as
context per the dispatch and are judged in the implementation segment against requirements/tasks.
Pre-081d and concurrent commits are excluded.
**Carriers**: this file and `code-review.md`. `review-081a.md`, `review-081b.md`, `review-081c.md`,
`code-review-081a.md`, `code-review-081b.md`, `code-review-081c.md` are dated records of earlier
slices and were not touched. This run's archive path is `none` (the 081c records were rotated at
slice open, commit `7f97d34b`, before this run started).
**Status**: `Ready for Review` (claimed at `a8dbb599`). This review judges that claim.

## Verdict

**The claim is earned on content, and the Acceptance Reality Check reads `agree` — with one P1
process finding against the checkpoint the flip used.** The evidence chain is genuine end to end:
SC-001's 3/3 call-site refusals are real checker outputs with closed-set reasons; SC-002's reading
(ii) is a real recorded four-segment composition run over `review-implemented-clean` with a produced
fixture-local record (not the reduced checker invocation its own ladder forbids); the 19-failure
reconciliation is honest — every pin re-measured with a dated comment naming its introducing commit,
no assertion deleted, no test skipped, anti-vacuous floors kept, and one containment actually
tightened to exact multiset equality; the id-level baseline difference at the final tree is
mechanically 0 new / 0 fixed (verified by set difference in this run, not taken from the prose); the
smoke re-run under this review exits 0 and leaves the tree byte-identical; the audit mode, the line
state, the driver gate and the schema guard match their requirements and carry green carriers. The
checker accepts: `final_path` 2/2 `pass`, no reasons.

The P1 process finding is about *when* the flip happened, not whether it was deserved: the
`Implemented → Ready for Review` transition was executed by the implement stage (T018, `a8dbb599`),
while the state-machine gate's owner assigns the flip to `/speckit.review` (or human) and its item 9
says the status "must not flip before that segment completes". At flip time gate condition (c) — no
`blocking` entry in the current `code-review.md` — was vacuous, because no current record existed.
This run's code segment completes with zero `blocking`, so the condition is now genuinely true and
the claim stands; but had this review refused, the refusal's guarantee ("leaves the claimed status
unchanged") would have held the feature at `Ready for Review`, not at `Implemented` — the early flip
removes the gate's ability to hold. Two further P1 artifact findings are self-contradictions in the
feature's own acceptance surfaces (`verification.md`'s notes vs its SC-009 row; the feature detail's
stale `Draft` current-position line), plus three P2s. Code segment: 4 entries, 0 `blocking`, 0
`important`, 0 code paths outside tests.

Findings: **P0 = 0, P1 = 3, P2 = 3** (6 non-code findings); code segment: **4** entries (1
`suggestion`, 1 `nitpick`, 1 `question`, 1 `praise`), recorded in `code-review.md`. All findings are
**open** — this stage judges and does not repair; none was resolved inside the range.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 081 |
| Requirement Key | `081-acceptance-hardening` |
| Requirement Name | Stricter Acceptance & Artifact Review（更严格的验收与产物审查） |
| Related Feature | 081 — the same feature (this slice is `081d`, the fourth and final slice) |
| Repository | `spec-kit` |
| Repository URL | `gitlab@gitlab.alibaba-inc.com:cloud-native-ai/spec-kit.git` (the only remote; `git remote -v` lists `gitlab` only, no `origin`) |
| Reachability of COMMIT_SHA | **UNRESOLVABLE**: `git branch -r --contains a8dbb599e0ce2adc98766c517f0a19ac14a7afc0` is empty — the branch is 11 commits ahead of `gitlab/081-acceptance-hardening` and unpushed. Every citation below is a repo-relative path plus `git show <sha>:<path>`; no `blob/` URL form is used |
| Branch | `081-acceptance-hardening` |
| Commit SHA | `a8dbb599e0ce2adc98766c517f0a19ac14a7afc0` (short `a8dbb599`) |
| Repo Root (absolute) | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit` |
| Review Date | 2026-11-03 |
| Reviewer (Agent) | SDD executor, `/speckit.review` composition run (four segments + ARC), slice 081d review stage |
| Environment | macOS (darwin/arm64); `python3` 3.9.6 (system interpreter, runs the stdlib engines); `.venv/bin/python` 3.14.6 / `pytest` 9.2.0 (test runner, pins match `test-evidence/plan-runner-pins.txt`); `git` 2.54.0 (Apple Git-157) |
| spec-kit Source Snapshot | the reviewed checkout itself (framework source and self-hosted runtime in one tree); `HEAD` = `a8dbb599` |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 271 | `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/requirements.md` | 25 FR / 9 SC / 17 STR; § D (US4) + FR-017/FR-008/FR-023/FR-011 are 081d's scope |
| plan.md | 365 | `…/081-acceptance-hardening/plan.md` | D1–D10, EP-001…EP-010, IB-001…IB-008 ledger, mirror obligations, D6 landing map |
| tasks.md | 272 | `…/081-acceptance-hardening/tasks.md` | slice 081d: 18 rows T001–T018, GATE-1…GATE-9, DoD-1…DoD-10, all closed |
| verification.md | 81 | `…/081-acceptance-hardening/verification.md` | 9 SC status rows (all `pass`), smoke record, checker-copied acceptance summary |
| data-model.md | 211 | `…/081-acceptance-hardening/data-model.md` | E-1…E-10, V-1…V-32, SM-1/SM-2, fixture census incl. 081d's `audit-history` |
| quickstart.md | 176 | `…/081-acceptance-hardening/quickstart.md` | S1–S9+ executable scenarios with per-scenario execution status |
| contracts/ (5 files) | — | `…/081-acceptance-hardening/contracts/` | closure checker, state vocabulary, artifact schemas (AS-13…AS-16), review composition, gate wiring (GW-03 rewritten by `4d195cb7`) |
| research.md | — | `…/081-acceptance-hardening/research.md` | R1–R9 plan-stage measurements (context; unchanged in the range) |
| feature-ref.md | — | `…/081-acceptance-hardening/feature-ref.md` | Feature 081 binding + delivery surface (context; unchanged in the range) |
| baseline-failed.txt | 39 | `…/081-acceptance-hardening/baseline-failed.txt` | plan-stage failed-id baseline (39 ids at `cb841d90`) |
| test-evidence/ | — | `…/081-acceptance-hardening/test-evidence/` | 081d evidence: call sites, review-site measurement, gates, audit zero-write, inherited ledger, baselines 1+2, closure verdict JSON |
| code-review.md | — | `…/081-acceptance-hardening/code-review.md` | this run's code-segment record (receipt 25/25, verdict `pass`, gate `allow`) |

## 1. Process Execution Timeline

| # | Step / Event | Evidence (commit SHA, file, or quoted excerpt) | Deviation from prescribed flow? |
|---|--------------|------------------------------------------------|---------------------------------|
| 1 | Slice opened; 081c carriers rotated to `review-081c.md` / `code-review-081c.md` | `7f97d34b` | none — the composition's rotation rule |
| 2 | Slice tasks authored (18 rows, GATE-1…9, DoD-1…10, FR/SC coverage + ownership roster) | `b3d44922` | none |
| 3 | Dated checklist audit of the final wiring slice | `312e2da4` (43 items: 18 PASS / 25 FAIL; P0 CHK028) | none |
| 4 | Analyze r1: C=2 / H=9, gate `fail` → repair lands 11/11 C/H resolutions (SC-002 three readings; schema-guard subject → owner column sets; audit root `--repo` + `Spec Path` resolution; GW-03 derivation end to end) | `8b1e6cc8`; `notes/analyze-081d-r2.md` round-1 table | none — the repair is the analyze flow's own next step |
| 5 | Analyze r2: 0 open C, **1 open H** (R2-F-12: driver has no disposition for checker exit 2), gate `fail` → owner ruling recorded in the r2 report; exit 2 = input error (`closure-input-error`, state unchanged, merge refused), landed in GW-03 + T008 + two per-shape carrier legs | `4d195cb7`; `notes/analyze-081d-r2.md` § "R2-F-12 resolution (owner ruling, 2026-11-03)"; `contracts/gate-wiring.contract.md` GW-03 | none — the decision is a design ruling inside the feature's own contract, not a status waiver |
| 6 | Implementation parts 1–3: T001–T004 (incl. the SC-002 (ii) recorded composition run at run-start HEAD `72c16f33`, 08:39Z), T005–T009 (line state + driver gate), T010–T015 (vocabularies, audit mode, ledger re-read, schema guard, regeneration) | `8ceaeb7a`, `fc6811c6`, `f29b6178`; red-first readings in `notes/red-first-evidence-081d.md` | none |
| 7 | Part 4 discovery: the feature-level full-suite run measures **19 new failure ids** (16 bucket A from 081b/081c late commits, 3 bucket B from 081d's own T010 edit); the fail reading is recorded with each id listed | `test-evidence/081d-final-baseline.txt` § (c) (committed in `a8dbb599`); `test-evidence/081d-head-failed.txt` (58 ids) | disclosed, not silenced — the reading names the introducing windows |
| 8 | The 19 reconciled: 12 test files re-pinned with dated stale-pin comments; full suite re-run → 39 failed / 7134 passed / 7 skipped, `head − baseline` = 0, `baseline − head` = 0 | `54ad418d`; `test-evidence/081d-final-baseline-2.txt`; `head-failed-2.txt` | judged honest by this review (§ 3, none of the dispositions deletes an assertion; verified against the diff) |
| 9 | Feature-level readings taken (3/3 call sites, SC-002's three readings, gates, audit zero-write, ledger 3/3, final smoke 0/0) and `verification.md` rewritten; checker read before and after the status landing; feature flipped `Blocked → Implemented → Ready for Review` in the implement stage's T018 | `a8dbb599`; `test-evidence/081d-call-sites.txt`, `081d-gates.txt`, `081d-audit-zero-write.txt`, `081d-inherited-ledger.txt`, `closure-verdict-081d.json` | **deviation — F1 (P1)**: the `Implemented → Ready for Review` flip is executed by the implement stage, while the gate's owner command is `/speckit.review` (or human) and its item 9 forbids flipping before the review's code segment completes (condition (c) was vacuous at flip time) |
| 10 | This review run: triage, smoke re-run, all four segments, ARC | `code-review.md` (created by `git-delta-review.sh start`, archive `none`) | none |

## 2. Findings Summary

| Severity | Count | Definition |
|----------|------:|------------|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 3 | Quality-of-life. Compounding gains across many specs. |

| Category | Count |
|----------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 0 |
| Workflow | 3 |
| Documentation | 3 |

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `f29b6178789539622fd9b7ee9af811b956cfa909` | the inclusive reading of the dispatch range (`54ad418d^`); the strict `--since 54ad418d` reading (10 files, no code path → `not-applicable`) is disclosed in the record's Scope notes |
| Head commit | `a8dbb599e0ce2adc98766c517f0a19ac14a7afc0` | the run-start `HEAD`, fixed for the run |
| Base source | `explicit` | `git-delta-review.sh base --since f29b6178 --head a8dbb599 --json` |
| Renderer mode | `renderer: text` | the code record's header marker |
| Changed / judged / skipped / gap files | 25 / 25 / 0 / 0 | copied field by field from the record's coverage receipt block; never recomputed |
| Segment verdict | `pass` | one of the four closed values the `code-review` skill owns |
| Gate verdict | `allow` (exit 0; 0 `blocking`, 0 `important`) | `git-delta-review.sh report --summary --file <record>` |
| Reason, when one applies | `none` | — |
| Uncommitted scope | none at run start (`git status --porcelain` = 0 lines); the smoke re-run refreshed the smoke evidence byte-identically and porcelain stayed 0; the same sentence lives in `code-review.md` § Scope notes | disclosed, never concluded over |
| Record | `.specify/specs/081-acceptance-hardening/code-review.md` | written by the skill's `start` → `note` → `receipt` path |
| Archive | `none` | first run in the current record state |

This subsection carries the verdict and the pointers only: no opinion body, no per-severity item count. The findings themselves live in `.specify/specs/081-acceptance-hardening/code-review.md` and are read there.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `verification.md`, `contracts/`, `data-model.md`, `quickstart.md`, `research.md`, `feature-ref.md`, `baseline-failed.txt`, `test-evidence/` | derived per slice from the stage rules (the standard seven) ∪ `plan.md` § Project Structure § Documentation (which additionally declares `research.md`, `feature-ref.md`, `baseline-failed.txt`, `test-evidence/`); the size used is **11** |
| Coverage line | 11 / 11 | present members / expected members |
| Missing members | `none` | every expected member exists on disk and non-empty |
| Segment verdict | `pass` | one of `pass`, `blocked`, `not-applicable`, `not-evaluated` |

| Severity | Artifact path | Line | Why the line is absent | Finding |
|----------|---------------|------|------------------------|---------|
| P1 | `.specify/specs/081-acceptance-hardening/verification.md` | 81 | — | A1 — the `notes=` paragraph still says "SC-009 is recorded `fail` honestly … recorded as this row's unblock" while the row itself (lines 53–60) reads `SC-009_status=pass` with `SC-009_unblock=` empty: two contradictory statements about one criterion's status in the acceptance log of the acceptance-honesty feature |
| P1 | `.specify/memory/features/081.md` | 83 | — | A2 — the state-machine section's current-position line still reads "当前：`Draft`（requirements 已落地；plan 未落地）… **尚未**写入该 owner" under a detail whose own `**Status**` (line 6) is `Ready for Review` and whose four transitions landed in 081a; a stale second status statement GATE-9's agreement check cannot see |
| P2 | `.specify/specs/081-acceptance-hardening/verification.md` | 22 | — | A3 — SC-001's value says "measured at the final tree" while its own evidence header reads "tree: `f29b6178` + this part's CHANGELOG entry (the only tracked delta at run time)": materially equivalent (neither later commit touches the checker's inputs) but the row's wording is stronger than the evidence it cites |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `54ad418d5341a3601955e28ff68299383d223eeb` | the dispatch-named range start |
| Head commit | `a8dbb599e0ce2adc98766c517f0a19ac14a7afc0` | the run-start `HEAD`, fixed for the run |
| Base source | `explicit` | the dispatch passes the caller's values through; the three context commits (`8ceaeb7a`, `fc6811c6`, `f29b6178`) holding the five named surfaces (driver gate, exit-2 disposition, audit mode, vocabularies, schema guard) were read and judged as the dispatch directs |
| Smoke command | `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` | recorded verbatim; **re-run by this segment**, not copied |
| Smoke exit code | `0` | the integer this segment's run returned (`1 passed in 6.68s`) |
| Smoke evidence path | `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` | exists and is non-empty; the re-run refreshed it byte-identically (`git status --porcelain` stayed 0 — SC-008's determinism claim verified live) |
| Scope and regression verdict | `pass` — the range and context surfaces match `tasks.md` T001–T018: the driver gate defaults to the checker through the existing `--gate-cmd` hook (GW-04), resolves the spec dir by GW-03's rule with the four input-error shapes, records `closure-blocked` while `completed` then lands `blocked`; the exit-2 disposition is `closure-input-error` with state unchanged; `line-registry.py` carries all eight A6 dispositions (10/10 carrier assertions); the audit mode keeps one judgement pipeline (`judge_spec`) for both modes, refuses `--spec-dir` by name in audit mode and `--json-out` under the audited root; the three vocabulary owners and the narrow exception are in place; the schema guard derives its subject mechanically from the owner's three `| Column |` tables. No unclaimed work in the range; earlier deliveries re-verified green (carrier suite 119 passed recorded at the final tracked tree, `test-evidence/081d-call-sites.txt`; smoke re-run exit 0; checker `accept`) | this segment's own reading |
| Segment verdict | `pass` | one of `pass`, `blocked`, `not-applicable`, `not-evaluated` |

| Severity | Diff path | Line | Why the line is absent | Finding |
|----------|-----------|------|------------------------|---------|
| P2 | `.specify/specs/081-acceptance-hardening/tasks.md` | 64 | — | F2 (shared with § 3) — the R2 recommendation limb "disclose the 55/63 exposure in § Environment Prerequisites" was not landed: `tasks.md` § Environment Prerequisites carries no row for the measured exposure (21 branch-null / 27 no-three-digit / 7 empty `Spec Path`; 55 of 63 registry lines unresolvable under the default-on gate), which lives only in `notes/analyze-081d-r2.md` |

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Ready for Review` | `.specify/memory/features.md` row 081 (the checker's `claimed_status_source`); `.specify/memory/features/081.md` `**Status**` line 6 reads the same |
| `final_path` record, copied verbatim (7/7) | pass 2 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 2 | `python3 scripts/python/closure-acceptance-check.py --spec-dir .specify/specs/081-acceptance-hardening --json`, run by this review; never recomputed here |
| Comparison verdict | `agree` | the checker's verdict is `accept` (exit 0, `reasons: []`) and the claim is `Ready for Review`; the `pass` bucket is 2, so `F-ACCEPTANCE` cannot fire |
| Failed condition, on refusal | `none` — no refusal | the payload's `.reasons` is empty |
| Fixed item, on refusal | `none` | as above |

**Transition judgement (one checkpoint, this run).** The `Implemented → Ready for Review` conditions: (a) every deferred task resolved or waived — `deferred_tasks=` empty, zero `[~]` rows; (b) review evidence produced — T004's recorded four-segment composition run over `review-implemented-clean` (`tests/fixtures/acceptance-hardening/review-implemented-clean/review.md` + `test-evidence/081d-review-site-measurement.txt`) plus this run's two carriers; (c) the current `code-review.md` contains no `blocking` entry — **true of this run's record** (0 `blocking`, 0 `important`, gate `allow`), but it was **vacuous at flip time**, which is finding F1; (d) no `final`-path criterion in `blocked`/`deferred`/`fail` — SC-001 and SC-002 are both `pass`. ARC: `agree`; the claim survives.

## 3. Findings (Problems & Improvement Targets)

### F1 — The `Implemented → Ready for Review` flip was performed by the implement stage, so gate condition (c) was vacuous at flip time (`P1`)

- **Severity**: P1
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/tasks.md` (T018, line 154) and `a8dbb599` (`.specify/memory/features.md` row 081, `.specify/memory/features/081.md`); owner text at `templates/feature-details-template.md` lines 78 and 108
- **Evidence** (verbatim quote):

  ```
  templates/feature-details-template.md line 78:
  | Implemented | Ready for Review | `/speckit.review` (or human) | **Four conjunctive conditions,
  all required**: … the current code-segment record (`code-review.md`) contains no `blocking` entry; …

  templates/feature-details-template.md line 108:
  9. **One checkpoint, after both segments.** … the status must not flip before that segment
  completes; an early flip is a violation even when the process segment already passed.

  a8dbb599 commit subject: "feat(081d): take the feature-level readings and land Ready for Review"
  ```

- **Why it's a problem**: the transition's owner command is `/speckit.review` (or human), and T018 is an implement-stage row. When `a8dbb599` landed, no current `code-review.md` existed (the 081c record had been rotated to `code-review-081c.md`, which the gate says is "never counted"), so condition (c) held vacuously rather than by judgement — exactly what item 9 exists to prevent. The harm is structural, not cosmetic: a refusal "leaves the claimed status unchanged", so had this review refused, the feature would have stayed `Ready for Review` instead of being held at `Implemented` — the early flip defeats the gate's hold-at-`Implemented` guarantee. In this run the claim survives on its merits (this record carries zero `blocking`), so ARC reads `agree`; the defect is the checkpoint, not the verdict.
- **Proposed fix**: one owner decision, then alignment: either the flip moves to the review run's accept path (and `tasks`-stage rows like T018 stop at `Implemented`), or the gate's owner names the implement stage as a permitted flipper with the evidence condition that replaces the vacuous-(c) reading. Touch `templates/feature-details-template.md` § Canonical Status State Machine (item 9 / Owner Command cell) and the `templates/tasks-template.md` guidance that produces rows like T018.

### F2 — Analyze R2's recommendation limb "disclose the 55/63 exposure in § Environment Prerequisites" was not landed (`P2`)

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/tasks.md` (§ Environment Prerequisites, lines 54–64) vs `notes/analyze-081d-r2.md`
- **Evidence** (verbatim quote):

  ```
  notes/analyze-081d-r2.md, R2-F-12 recommendation:
  "… Either way add the `tmp_path`-registry leg (one line per shape, asserting resulting `state` and
  `integration_result`) and disclose the 55/63 exposure in § Environment Prerequisites."

  notes/analyze-081d-r2.md, measurement 5:
  "GW-03 resolvability over the live registry (63 lines): branch-null 21, no-3-digit 27, empty
  `Spec Path` 7, resolvable 8; active lines 18, resolvable 1."
  ```

- **Why it's a problem**: the ruling closed R2-F-12 and its carrier legs landed (`test_an_input_error_refuses_the_merge_and_leaves_the_state_completed`, `test_the_resolution_input_error_shapes_refuse_without_inventing_a_spec_dir`), but of the recommendation's two limbs only the carrier leg landed; the exposure measurement — the reason the disposition matters for the default-on gate — lives only in a notes file, while A13 names `tasks.md` § Environment Prerequisites the home of task-generation probe verdicts. A reader of the gate's default-on behaviour must rediscover that 55 of 63 registry lines land on the input-error path.
- **Proposed fix**: add one row to the slice's § Environment Prerequisites (or a `No Deferred Slice` bullet) citing the measured exposure with its probe command; and make the analyze repair-verification round carry a dispositioned list of its own recommendation limbs (landed / rejected / carried) so a limb cannot drop silently — see REC-W2.

### F3 — The reconciliation's disclosure landed in git history after the reconciliation itself (`P2`)

- **Severity**: P2
- **Category**: Workflow
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/test-evidence/081d-final-baseline-2.txt` (committed `54ad418d`) vs `081d-final-baseline.txt` § (c) and `081d-head-failed.txt` (committed `a8dbb599`)
- **Evidence** (verbatim quote):

  ```
  081d-final-baseline-2.txt lines 4–5:
  Predecessor: 081d-final-baseline.txt § (c) — the feature-level comparison that listed
  the 19 (16 bucket A + 3 bucket B) and classified them by introducing window.
  ```

- **Why it's a problem**: a reader walking the history meets the fix (`54ad418d`) before the finding it disposes (`a8dbb599`); the disclosure files that justify the reconciliation were committed later than the reconciliation result. The reading is recoverable — the reconciliation file names its predecessor and both carry the full 19-id lists — so this is ordering friction, not dishonesty.
- **Proposed fix**: nothing to repair retroactively (history is immutable); for future slices, the reconciliation commit should carry (or precede with) the disclosure listing what it reconciles.

### A1 — `verification.md` carries two contradictory statements about SC-009's status (`P1`)

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/verification.md` line 81 (vs lines 53–60)
- **Evidence** (verbatim quote):

  ```
  line 53: SC-009_status=pass
  line 54: SC-009_value=the four limbs hold: … ② the id-level baseline comparison is green —
           … (the 19 earlier failures were each reconciled deliberately in
           `test-evidence/081d-final-baseline-2.txt`, 12 pins updated with their reasons); …
  line 60: SC-009_unblock=
  line 81: notes=… SC-009 is recorded `fail` honestly: limbs ①③④ pass and ④'s guard is green,
           but limb ② measured 19 new full-suite failure ids vs the plan-stage baseline — … the
           reconciliation is a cross-feature adjudication recorded as this row's unblock, not
           silently repaired here.
  ```

- **Why it's a problem**: the notes paragraph describes the intermediate state (the fail reading at the part-3 close) in the present tense and claims the adjudication is "recorded as this row's unblock" — but the final row reads `pass` and its `SC-009_unblock` field is empty, so the pointer the notes promise does not exist. In the acceptance log of the feature whose business is acceptance honesty, a reader cannot tell which statement is current without archaeology (the answer: the row, per `081d-final-baseline-2.txt`).
- **Proposed fix**: rewrite the notes paragraph into a dated record ("SC-009 read `fail` at the part-3 close; the reconciliation (`54ad418d`) moved limb ② to 0 new / 0 fixed; the row now reads `pass`") and point at the evidence file instead of an unblock field.

### A2 — The feature detail's current-position line still says `Draft` under a `Ready for Review` status (`P1`)

- **Severity**: P1
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/memory/features/081.md` line 83 (vs line 6)
- **Evidence** (verbatim quote):

  ```
  line 6:  **Status**: Ready for Review
  line 83: 当前：`Draft`（requirements 已落地；plan 未落地）。本特性自身要往该 owner 加的四条转移
           （…）属实现阶段交付物，**尚未**写入该 owner；写入后本文件只引用、不复述。
  ```

- **Why it's a problem**: the detail contradicts itself: the `**Status**` line (which GATE-9's registry-agreement check reads) says `Ready for Review`, while the state-machine section's "current position" note is a clarify-stage snapshot saying the feature is `Draft` and its four transitions are "尚未" (not yet) written into the owner — they were written in 081a. A second, stale status statement inside the bound detail is precisely the drift the feature's own one-source rules forbid.
- **Proposed fix**: update the current-position line to the actual position (or drop the stale sentence and keep only the pointer to `templates/feature-details-template.md` § Canonical Status State Machine), in the same maintenance pass that would land this review's `## Latest Review` entry.

### A3 — SC-001's row says "measured at the final tree"; its evidence header names an earlier tree (`P2`)

- **Severity**: P2
- **Category**: Documentation
- **Location**: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/.specify/specs/081-acceptance-hardening/verification.md` line 22 (vs `test-evidence/081d-call-sites.txt` line 3)
- **Evidence** (verbatim quote):

  ```
  verification.md line 22: SC-001_value=the 026 shape is refused at all three call sites — 3/3
  refused, 0 passed, measured at the final tree: …

  081d-call-sites.txt line 3: Date: 2026-11-03 · branch 081-acceptance-hardening · tree: f29b6178
  + this part's CHANGELOG entry (the only tracked delta at run time)
  ```

- **Why it's a problem**: the reading was taken before the reconciliation commit (`54ad418d`) and the close commit (`a8dbb599`) landed; the row's wording is stronger than the evidence it cites. The gap is materially nil — neither commit touches the checker's inputs or the three call-site surfaces — and the evidence file discloses its exact tree, so this is precision, not fabrication.
- **Proposed fix**: align the row's wording with the evidence header (or re-run the three invocations at `a8dbb599` — three commands, seconds — and refresh the header).

## 4. What Worked — Preserve (Brief)

- The 19-failure reconciliation is honest and diff-verifiable: every pin re-measured with a dated comment naming its introducing commit; assertion shapes preserved; anti-vacuous floors kept (`LEDGER_FLOOR` 39); the decision-tension containment **tightened** to exact multiset equality.
- SC-002's reading (ii) is a genuine recorded four-segment composition run with a produced fixture-local record — the exact measurement its own ladder demanded, not the reduced checker invocation.
- The exit-2 disposition was decided at contract level (GW-03) with per-shape carrier legs, not in a docstring; the R2 open H was closed by a recorded owner ruling.
- The audit mode keeps one judgement pipeline (`judge_spec`) for both modes, refuses `--spec-dir` by name in audit mode, and refuses `--json-out` under the audited root.
- The smoke's determinism claim survived an independent re-run: byte-identical evidence, `git status --porcelain` 0.
- The id-level baseline invariant is real: `head − baseline` and `baseline − head` both empty, verified mechanically in this run.

## 5. spec-kit / SDD Improvement Recommendations

### 5.4 Workflow Improvements

- **REC-W1: give the `Ready for Review` flip one owner at the gate** — Target: `templates/feature-details-template.md` § Canonical Status State Machine (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/feature-details-template.md`), with the matching guidance in `templates/tasks-template.md`. Change: decide whether the flip belongs to the review run's accept path or is permitted at the implement stage with an evidence condition that replaces the vacuous no-record reading of condition (c); state whichever is chosen once, where the four conditions are stated. Source: F1. Expected impact: an unattended feature can no longer reach `Ready for Review` before the code segment's record exists, so a refusing review can still hold the feature at `Implemented`.
- **REC-W2: analyze repair-verification rounds disposition their own recommendation limbs** — Target: `templates/commands/analyze.md` (absolute supplement: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/templates/commands/analyze.md`). Change: require each repair-verification round to end with a per-recommendation disposition list (landed / rejected / carried, each naming its carrier), so a limb like the 55/63 exposure disclosure cannot drop silently between rounds. Source: F2. Expected impact: recommendations become traceable obligations instead of prose a later commit may half-apply.

(A1–A3 are repairs to this feature's own artifacts, not framework changes; they belong to the feature's next maintenance pass together with the `## Latest Review` entry for this run. F3 needs no retroactive repair.)

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| P1 | One owner for the `Ready for Review` flip | `templates/feature-details-template.md` § Canonical Status State Machine; `templates/tasks-template.md` | F1 |
| P1 | Rewrite `verification.md`'s SC-009 notes into a dated record; delete the pointer to the empty unblock field | `.specify/specs/081-acceptance-hardening/verification.md` | A1 |
| P1 | Update the feature detail's current-position line | `.specify/memory/features/081.md` | A2 |
| P2 | Analyze rounds disposition their recommendation limbs | `templates/commands/analyze.md` | F2 |
| P2 | Align SC-001's "final tree" wording with its evidence header | `.specify/specs/081-acceptance-hardening/verification.md` | A3 |
| P2 | Reconciliation commits carry their disclosure evidence in the same commit (future-slice guidance) | `shared/workflow/acceptance-hardening.md` (evidence rules) | F3 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative (primary), with an absolute path only as a parenthetical supplement; targets with no repo-relative form are marked `external` with a reason. (No `external` targets were used.)
- [x] Every finding in Section 3 has a quoted excerpt that lets the reader judge the problem without opening the source file.
- [x] No bullet says "see attached", "as discussed earlier", or otherwise references context outside this document.
- [x] No placeholder tokens (`[...]`) remain anywhere in the report.
- [x] Section 4 is short and bullet-only — no multi-paragraph narrative summaries leaked back in.
- [x] Section 5 recommendations each cite an exact target file in the spec-kit repo and at least one source finding ID.
- [x] P0 validation status is stated explicitly. No P0 findings raised; the P0 independent-validation pass is vacuously satisfied.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

## Review-fix dispositions (081d)

| Finding | Disposition | Evidence |
|---|---|---|
| F1 (P1) — the flip was performed by implement | **Fixed**: T018 now lands the implement stage's earned value `Implemented`; the `Implemented → Ready for Review` flip is this review's action, taken after both review records exist. The status transition is recorded below | `tasks.md` T018; this section |
| F2 (P2) — the 55/63 exposure was not disclosed | **Fixed**: the measured exposure is a row in `tasks.md` § Environment Prerequisites with its probe basis | `tasks.md` § Environment Prerequisites |
| F3 (P2) — the reconciliation's disclosure landed after it | **Recorded, no retroactive repair** (history is immutable); the rule for future slices is: the reconciliation commit carries or precedes the disclosure it disposes | this section |
| A1 (P1) — SC-009 had two contradictory statements | **Fixed**: the notes paragraph is now a dated record (fail at part-3 close → `54ad418d` → pass) and points at `081d-final-baseline-2.txt` | `verification.md` notes |
| A2 (P1) — the detail's current-position line said `Draft` | **Fixed**: the line now reads `Ready for Review` and points at the state-machine owner | `features/081.md` |
| A3 (P2) — SC-001's wording exceeded its evidence tree | **Fixed**: the row now names the evidence tree and notes that the later commits do not touch the call sites | `verification.md` SC-001 |

## Status transition (owned by this review)

The implement stage's earned value is `Implemented` (T018). With both review records now on disk — `review.md` (four segments + ARC, `agree`) and `code-review.md` (six-level family, no `blocking` entry, receipt 25/25) — this review performs the `Implemented → Ready for Review` transition per `templates/feature-details-template.md` § Canonical Status State Machine. The earlier implement-stage flip is corrected here; the transition's owner is `/speckit.review`, not the implement stage.
