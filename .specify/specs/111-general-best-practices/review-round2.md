# Specification-Driven Development (SDD) Review Report — Round 2: General Best Practices（通用最佳实践模块）

> **Audience**: spec-kit framework maintainers and the SDD driver owning this line.
> **Purpose**: the round-2 `/speckit.review` record — the four segments in their fixed order plus the Acceptance Reality Check, re-run on the repaired tree (`e6e1aff7a`).
> **Relation to round 1**: `review.md` (committed `534469e54`) is the round-1 record and stays untouched as history. This file is the round-2 record; the driver's round-2 brief authorizes the separate-file form (round-2 dispatch of the review stage). It **supersedes the round-1 verdict**, keeps every round-1 finding ID, and re-adjudicates each one.
> **Intentionally problem-first**: artifact contents are described only where a finding needs the context.

## 0. Portable Project Context (Self-Contained Snapshot)

| Field | Value |
|-------|-------|
| Requirement ID | 111 |
| Requirement Key | `111-general-best-practices` |
| Requirement Name | General Best Practices（通用最佳实践模块） |
| Related Feature | 111 — General Best Practices（通用最佳实践），new standalone feature (no parent slice) |
| Repository | spec-kit (git worktree `general-best-practices`) |
| Repository URL | `origin` = upstream (does not carry this branch); fetch/push remotes present: `gitee`, `github`, `gitlab` |
| Reachability of COMMIT_SHA | **UNRESOLVABLE** — `git branch -r --contains HEAD` is empty (the branch is unpushed). Citations below use absolute paths plus `git show <sha>:<path>` recovery instead of URLs. |
| Branch | `111-general-best-practices` |
| Commit SHA | `e6e1aff7a4540f6643409e7b3db8eb6010293846` (short `e6e1aff7a`) |
| Round-1 reviewed head | `aca4fb076e9e9ea28ef6516f9d0a935949545fa9` (`aca4fb076`); the repair commit between the two heads is `e6e1aff7a` only |
| Repo Root (absolute) | `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/general-best-practices` |
| Review Date | 2026-11-27 |
| Reviewer (Agent) | SDD Review Coordinator (round 2, Qoder CLI) |
| Environment | Linux x64 · bash 4.4.20 · CPython 3.11.11 · pytest 8.4.2 · line run id `r20261127T071500Z-111a` |
| spec-kit Source Snapshot | This worktree at `e6e1aff7a` (self-hosted project; feature containment base `0419adae5`) |

### Artifact Inventory

| Artifact | Lines | Absolute Path | One-line Summary |
|----------|------:|---------------|-------------------|
| requirements.md | 228 | `<repo>/.specify/specs/111-general-best-practices/requirements.md` | 9 FR / 7 SC / 7 STR / 24 adjudicated assumptions; closed four-category content module + accumulation by pointer |
| plan.md | 151 | `<repo>/.specify/specs/111-general-best-practices/plan.md` | 23-row Constitution Check (all pass), EP-001…EP-005, mirror obligations, declares `verification.md` as implement output |
| tasks.md | 305 | `<repo>/.specify/specs/111-general-best-practices/tasks.md` | 20 task rows (T001–T019 + T007A), 24 clause green tags, 8 gate items, DoD-1…DoD-7 |
| data-model.md | 157 | `<repo>/.specify/specs/111-general-best-practices/data-model.md` | E1–E11 entities, INV-01…INV-12, 3 transitions |
| quickstart.md | 153 | `<repo>/.specify/specs/111-general-best-practices/quickstart.md` | S-0…S-8 scenarios with measured readings |
| research.md | 114 | `<repo>/.specify/specs/111-general-best-practices/research.md` | M1–M11 measurements + R-1…R-10 design points |
| feature-ref.md | 64 | `<repo>/.specify/specs/111-general-best-practices/feature-ref.md` | Feature 111 binding, delivery surface, FR→surface and SC→evidence maps |
| verification.md | 62 | `<repo>/.specify/specs/111-general-best-practices/verification.md` | **New at `e6e1aff7a`** (driver repair): baseline, implementation results, smoke triple, 7 SC status rows, 3 RS joint-acceptance rows |
| contracts/ (4 files) | 116 | `<repo>/.specify/specs/111-general-best-practices/contracts/` | C-101…C-106 / C-201…C-205 / C-301…C-306 / C-401…C-407 = 24 clauses |
| checklists/ (2 files) | 140 | `<repo>/.specify/specs/111-general-best-practices/checklists/` | 40-item requirements-quality checklist + spec-quality checklist |
| test-evidence/ (79 files) | — | `<repo>/.specify/specs/111-general-best-practices/test-evidence/` | gate captures, validator outputs, containment readings, closure payload (`closure-acceptance-2026-11-27.json`) |
| notes/ (6 files) | — | `<repo>/.specify/specs/111-general-best-practices/notes/` | red-first capture, pre-change measurements, quickstart run, US1/US2/US3 green records |
| checkpoints/ (7 files) | 83 | `<repo>/.specify/specs/111-general-best-practices/checkpoints/` | driver checkpoints 01–07 |
| review.md (round 1) | 356 | `<repo>/.specify/specs/111-general-best-practices/review.md` | Round-1 composed report — retained as history |
| code-review.md (round 2) + archive | — | `<repo>/.specify/specs/111-general-best-practices/code-review.md` · `code-review-20261127T092328Z.md` (round-1 record) | Round-2 code-segment record with coverage receipt; round-1 record rotated by `start` |
| Module documents (5) | 68 | `<repo>/shared/best-practices/` | manifest + four category owner files (closed set, one seed, three placeholders) |
| Contract guard | 288 | `<repo>/tests/contract/test_general_best_practices.py` | six legs (a)–(f) + module-read prelude, `pytest.mark.contract` |
| Framework map row | 1 row | `<repo>/shared/definitions/framework-map.md` (+ mirror) | registration row for `.specify/shared/best-practices/` with `Feature 111` |
| Feature registry + detail | 1 row / 33 | `<repo>/.specify/features.md` (line 118) · `<repo>/.specify/features/111-general-best-practices.md` | status flipped `Implemented → Ready for Review` by this run (see §2.4) |

*In-passing correction (disclosed)*: the round-1 inventory reported `test-evidence/` as 110 files; the measured count is 79 at both heads (`find … -type f | wc -l`). This record carries the measured number.

## 1. Process Execution Timeline

Round-1 events 1–11 are summarized from `review.md` § 1 (evidence: the same commits); rows 12–16 are this round's additions. All commits are local; the head is fixed for this run at `e6e1aff7a`.

| # | Step / Event | Evidence | Deviation from prescribed flow? |
|---|--------------|----------|---------------------------------|
| 1 | Requirements scaffolded by hand from the template (the script would derive number 112) | `requirements.md` A-9; `test-evidence/requirements-stage-2026-11-27.md` | Recorded deviation (branch pinned to 111) |
| 2 | Requirements stage left artifacts uncommitted; driver committed them | checkpoint 01 (`d53d3c228`) | Yes — commit discipline gap, repaired by driver (F7) |
| 3 | Clarify stage: same uncommitted-artifact repair | checkpoint 02 (`652f2c09e`) | Yes — second occurrence (F7) |
| 4 | Plan stage: plan set + four contracts, clean commit | `87ad3d068`, checkpoint 03 `1638077e4` | No |
| 5 | Tasks stage: 20 rows, 24 clause tags, 8 gates | `6c5fd4654`, checkpoint 04 `1f5b9284e` | No |
| 6 | Checklist stage: 40-item dated checklist | `7cb097c81`, checkpoint 05 `5af1c1290` | No |
| 7 | Analyze round 1: 1 CRITICAL / 2 HIGH → repaired by cause | `4f6905a95` → `61e3ccfb6` (A-22/A-23/A-24) | No — gate worked as designed |
| 8 | Analyze round 2 (incremental): round-1 C/H fixed; open set C0/H0/M4/L6 deferred | `93326d8bc`, checkpoint 06 `7db9d8dec` | Recorded deferrals (review-visible) |
| 9 | Implement P1/P2: module + guard, map + mirror + init proof, closure runs | `570ef1a6a` … `65b495b86` | No |
| 10 | Feature registration missing at stage closure; driver wrote row 111 + detail | `39be9495a`; checkpoint 07 line 4 | Yes — no stage in the driver sequence owns registration (F2) |
| 11 | Checkpoint 07 (implement U4) closes the stage | `aca4fb076` | No |
| 12 | **Review round 1**: four segments + ARC; `verification.md` absent → closure checker exit 2; `REVIEW-BLOCKED` (artifact P0 `F-ACCEPTANCE` + code `blocking`); no flip | `review.md`; `code-review.md`; commit `534469e54` | Gate worked as designed; the missing carrier is F1's symptom |
| 13 | Review round-1 wrap-up accounting: four units' records, engine settle of four prior 108 session records, first close-out receipt | `de9553e23` | No — but the receipt + settled records fall outside FR-009's closed set (F8) |
| 14 | Review amendment: F8 recorded (containment set vs close-out writes), severity counts updated | `57a7290b8` | No |
| 15 | **Driver repair**: derives `verification.md` from `test-evidence/verification-input.md` (7 SC rows + 3 RS joint-acceptance rows), writes the closure payload; checker exit 0 `accept` | `e6e1aff7a`; `test-evidence/closure-acceptance-2026-11-27.json` | Yes by design — the round-1 fix executed by the driver because no stage owns the derivation (F1) |
| 16 | **Review round 2** (this run): segments re-run, code record rotated (`start`), ARC `accept`, transition judged and landed | this record; `code-review.md`; archive `code-review-20261127T092328Z.md` | No |

**Same-author gate**: not fired — the repaired artifact was produced by the driver, and this review re-reads it; detection stayed with this read and is disclosed as such.

## 2. Findings Summary

| Severity | Count (open) | Closed this round | Definition |
|----------|-------------:|------------------:|------------|
| P0 | 0 | 1 | Blocks correct use of spec-kit, or creates silent corruption risk. Fix before next spec. |
| P1 | 3 | 0 | Recurring friction across specs. Fix when convenient — currently every spec writer pays the toll. |
| P2 | 5 | 0 | Quality-of-life. Compounding gains across many specs. |

| Category (open findings) | Count |
|--------------------------|------:|
| Template | 0 |
| Command Prompt | 0 |
| Automation / Scripts | 1 |
| Workflow | 5 |
| Documentation | 2 |

Disposition at a glance: **F-ACCEPTANCE (P0) — CLOSED** (carrier present, checker `accept`, ARC reads the record). F1/F2/F8 (P1) and F3/F4/F5/F6/F7 (P2) carried open with per-finding dispositions in § 3. No new finding was raised this round.

### 2.1 Code Segment (Verdict and Pointers)

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | resolved diff base (`--since 0419adae5`, the feature's declared containment baseline) |
| Head commit | `e6e1aff7a4540f6643409e7b3db8eb6010293846` | run-start `HEAD`, fixed for the run |
| Base source | `explicit` | `git-delta-review.sh base --spec … --since 0419adae5 --head e6e1aff7a` |
| Renderer mode | `renderer: text` | record header |
| Changed / judged / skipped / gap files | 159 / 15 / 144 / 0 | copied field by field from the coverage receipt |
| Severity counts | blocking 0 · important 1 · suggestion 2 · nitpick 2 · question 0 · praise 1 | `report --summary --file --format json` |
| Gate verdict | `allow` | `report --summary --file` exit 0; `blocking_entries=0`; the 1 `important` item is answered below (the gate also prints the answer obligation) |
| Record | `.specify/specs/111-general-best-practices/code-review.md` | written by `start` → `note` → `receipt` |
| Archive | `.specify/specs/111-general-best-practices/code-review-20261127T092328Z.md` | round-1 record rotated by `start`; never counted by the transition gate |
| Client capture | `skipped hat=framework basis=root owns framework source directories …; triage=run` | zero entries (framework-hat repository) |
| Uncommitted scope | this run's own review records are uncommitted at receipt time (they are committed by this run's close-out); disclosed, never concluded over | receipt disclosure line |

**Re-adjudication of the round-1 `blocking` entry — resolved.** The round-1 blocking entry's subject was "Status claim unsupported by its declared carrier: both the registry row and the feature detail read `Implemented`, but `verification.md` never landed; the closure checker exits 2". At `e6e1aff7a` the carrier exists and the checker returns `accept` with zero reasons, so the claim is now supported. Under the state-machine rule the transition gate is an existence test over the **current** record: the round-2 record carries zero `blocking` entries, and the archived round-1 record is history, never counted. No clearing action exists or was needed.

**Answer to the round-1 `important` item (required by the gate).** The item — `tasks.md` DoD-7 reassigns the `verification.md` derivation to an unnamed "spec side" while `implement-feature` SKILL § Step 9 assigns it to the implement run, and no stage owns it. **Agreed**: the cause is confirmed at `e6e1aff7a` (the file needed a driver repair after the implement stage closed), the recurrence now spans 107, 108 and 111, and the remediation is a framework-side change (`skills/internal/create-tasks/SKILL.md`, `skills/internal/implement-feature/SKILL.md` § Step 9) recorded as REC-111-02. No disagreement. The finding stays tracked as F1 (§ 3).

Correctness readings behind the opinions: the five module documents are byte-unchanged since the round-1 read (`git diff --stat aca4fb076..e6e1aff7a -- shared/ tests/ src/ …` is empty); the guard's six legs are executable and green (this run: `6 passed`, exit 0); the map row exists once in source and mirror; no second `best-practices*` engine file exists. The six opinions (1 important / 2 suggestions / 2 nitpicks / 1 praise) are the round-1 set carried with refreshed line anchors and round-2 verification; they live in the record and are not restated here.

### 2.2 Artifact Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Expected set (denominator) | `requirements.md`, `plan.md`, `tasks.md`, `contracts/`, `data-model.md`, `quickstart.md`, `verification.md`, `research.md`, `feature-ref.md`, `checklists/`, `test-evidence/` | union of the stage rules (implement Step 9 requires `verification.md`) and `plan.md` § Project Structure (lines 79–91) |
| Coverage line | **11 / 11** | present members / expected members |
| Missing members | none | `verification.md` now on disk (62 lines) |
| Segment verdict | `pass` — P2 ×1 carried (F3) | no P0/P1 |

| Expected member | Present | Shape verdict |
|-----------------|:-------:|---------------|
| requirements.md | yes | 9 FR / 7 SC / 7 STR, 24 adjudications; closed sets declared |
| plan.md | yes | Constitution Check 23 rows all pass; EP-001…EP-005; project-structure block intact |
| tasks.md | yes | 20 rows, 24 clause tags each claimed once; `validate-tasks.py` PASS 0 error / 0 warning (re-run this round) |
| contracts/ (4) | yes | C-101…C-106 / C-201…C-205 / C-301…C-306 / C-401…C-407 = 24 clauses |
| data-model.md | yes | E1–E11 / INV-01…INV-12 / 3 transitions |
| quickstart.md | yes | S-0…S-8 with measured readings |
| verification.md | yes | template blocks present; 7 `SC-NNN_status/value/note` rows + smoke triple + 3 RS rows; 21/21 status/value/note values verbatim-identical to the gate input (programmatic compare) |
| research.md | yes | M1–M11 / R-1…R-10 |
| feature-ref.md | yes | FR→surface and SC→evidence maps |
| checklists/ (2) | yes | 40-item requirements-quality checklist + spec-quality checklist |
| test-evidence/ (79) | yes | gate captures, validator outputs, containment readings, closure payload |

**Dimension readings**

1. **Completeness** — 11/11; the derived `verification.md` carries every block `.specify/templates/verification-log-template.md` requires for a passing feature (baseline, implementation results, exactly one smoke record, SC rows, RS joint-acceptance rows, empty deferred-task row).
2. **Internal consistency** — one defect stands: F3 (the checklist/registry/checkpoint task-count phrasing "19" versus the 20-row set). The round-1 review-side inventory miscount was corrected in § 0 (in-passing). `verification.md`'s SC values are verbatim copies of the gate input (verified by program, 21/21), and the smoke triple is identical.
3. **Traceability** — FR→task 9/9 and SC→task 7/7 (`tasks.md` § Requirement Coverage Map); 24 clause lines each claimed once (`validate-tasks.py` green-point attribution checks, 0 error / 0 warning, re-run this round); every SC row carries a measured value and a note naming its evidence, and every named evidence path exists (`notes/us1-green.txt`, `notes/us2-green.txt`, `notes/us3-green.txt`, `notes/quickstart-run.md`, `notes/red-first-evidence.md`, `test-evidence/init-distribution-proof.txt`, `test-evidence/containment.txt`, `test-evidence/full-suite.txt`, `test-evidence/targeted-set.txt`; `test-evidence/mirror-parity-names.txt` is the recorded 0-entry set by design).
4. **Dependency and premise ownership** — EP-001…EP-005 in `plan.md`; the RS rows name their premises; the manifest's spec-local contract pointer (AR1-04) remains the known carried item, by design deferred.
5. **Acceptance honesty** — statuses are gate products: the closure checker returns `accept` on the same tree, the red-first record (6 errors on the absent module → 6 passed) is archived, and the smoke record carries command, exit 0 and an existing evidence path. One boundary reading is stated instead of glossed: SC-006's `pass` was measured at the implement head with the A-20 predicate; at the review head the range additionally holds review-owned paths the declaration does not admit — the recorded F8 (P1), not a new honesty defect, because the measurement window is disclosed and the added paths are framework-mandated, not feature scope.

| Severity | Artifact path | Line | Finding |
|----------|---------------|------|---------|
| P2 | `.specify/specs/111-general-best-practices/checklists/general-best-practices-2026-11-27.md` | 7 | F3 (carried): states `tasks.md` carries 19 task rows while the file carries 20 (T001–T019 + T007A); the same phrasing appears in the registry row, the feature detail line 24 and closure records |

### 2.3 Implementation Review Segment

| Field | Value | Source |
|-------|-------|--------|
| Base commit | `0419adae5e6e0e208ad6bcb443e45be8d266f04a` | resolved diff base (`explicit`) |
| Head commit | `e6e1aff7a4540f6643409e7b3db8eb6010293846` | run-start `HEAD` |
| Base source | `explicit` | `git-delta-review.sh base --since 0419adae5 --head e6e1aff7a` |
| Smoke command | `env SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py` | recorded verbatim; re-run by this review |
| Smoke exit code | 0 | `6 passed in 6.28s` |
| Smoke evidence path | `.specify/.tmp/review-111-r2/smoke.log` | exists, non-empty (git-ignored run capture; the committed green record is `notes/us3-green.txt`) |
| Scope verdict | 159 paths = 117 declared + 2 registry exception + 35 residual-predicate pass + 4 residual-predicate fail + 1 out-of-set — the 5 rejecting paths are exactly the recorded F8 class (1 close-out receipt + 4 engine-settled prior-108 session records); **0 feature-scope violations beyond F8** | re-derived at `e6e1aff7a` by the A-20 program (`.specify/.tmp/review-111-r2/containment-e6e1aff7a.txt`); 131 → 159 growth from the implement head is all declared or F8-class |
| Regression verdict | none — the code surface is byte-unchanged since `aca4fb076` (`git diff --stat aca4fb076..e6e1aff7a -- src/ shared/ tests/ scripts/ templates/ skills/ agents/ .specify/…` empty); mirror parity `ok (122 files, byte-identical)`; guard re-run exit 0; the full-suite reading was not re-run because the tree it measures is identical (same-tree subject), so the frozen-tree reading of 223 failure names byte-identical to the entry baseline stands, consumed per the single-run evidence discipline | — |
| Segment verdict | `pass` — P2 ×1 carried (F4) | — |

| Severity | Diff path | Line | Finding |
|----------|-----------|------|---------|
| P2 | `.specify/specs/111-general-best-practices/test-evidence/containment.txt` | 81 | F4 (carried): Reading 2 is labeled "final-tree re-read" but was taken at `0cbec5aa4` (135 paths); the HEAD reading at `e6e1aff7a` is 159 paths (invariant intact). Relabel as interim or cite a HEAD reading |

Disclosure: this run's own close-out writes one new `.specify/retention/closeout/` receipt (a framework-mandated write), which extends the F8 class to 6 rejecting paths at the round-2 commit — the same structural omission F8 already records, not a new finding.

### 2.4 Acceptance Reality Check

| Field | Value | Source |
|-------|-------|--------|
| Claimed status (read, never written) | `Implemented` (registry row 118 and feature detail line 6 agree at ARC time) | copied |
| `final_path` record, copied verbatim | **pass 6 · blocked 0 · deferred 0 · partial 0 · fail 0 · unknown 0 · total 6** | `closure-acceptance-check.py --spec-dir … --json`, exit 0; payload `test-evidence/closure-acceptance-2026-11-27.json` |
| Checker verdict | `accept` — completion conditions all `true` (`no_open_rows`, `status_row_per_criterion`, `every_final_path_pass`, `smoke_record_pass`); `reasons: []`; tasks 20 closed / 0 deferred / 0 open / 0 in progress | same run (re-run this round, `.specify/.tmp/review-111-r2/arc.json`) |
| Comparison verdict | `agree` — `accept` agrees with the claim | ARC mapping |
| Transition judgment | `Implemented → Ready for Review` **allowed** — four conjunctive conditions: (a) every deferred `[~]` task resolved or waived — no `[~]` rows exist; (b) review evidence produced — this record plus `code-review.md`; (c) the current code-segment record contains no `blocking` entry — gate `allow`, `blocking_entries=0`; (d) no `final`-path criterion sits in blocked/deferred/fail — all six pass | `templates/feature-details-template.md` § Canonical Status State Machine (owner of the four conditions) |
| Status transition | **`Implemented → Ready for Review` landed** on both carriers — `.specify/features.md` line 118 (registry row) and `.specify/features/111-general-best-practices.md` line 6 (detail `**Status**`) | this run |

The `verification.md` statuses are gate products copied verbatim from `test-evidence/verification-input.md` (verified 21/21 identical), so ARC reads one record, not a second counter.

## 3. Findings — Re-Adjudication and Dispositions

Round-1 evidence blocks (quoted excerpts, line anchors) remain in `review.md` § 3; each entry below states the finding, its round-2 verification and its disposition. Finding IDs are unchanged; no new ID was coined this round.

### F-ACCEPTANCE — The acceptance carrier `verification.md` never landed (P0, Workflow) — **CLOSED**

- **Round-2 verification**: the file exists at `e6e1aff7a` (62 lines; the header discloses it was derived spec-side from `test-evidence/verification-input.md`). The closure checker exits 0 with `accept` (four conditions true, zero reasons, `final_path` pass 6 / total 6), and ARC reads the record. The code segment's round-1 blocking entry named this exact carrier; the current code record carries zero blocking entries.
- **Disposition**: closed — verified by the deterministic checker and by the code gate, not by this review's judgement.
- **Residual**: the derivation still has no owning stage; the structural cause stays open as F1. The next occurrence is predicted until REC-111-02 lands.

### F1 — The `verification.md` derivation has no named owner between implement and review (P1, Workflow) — **open, carried**

- **Round-2 evidence**: the repair landed as a **driver** commit (`e6e1aff7a`), the same ad-hoc seat that produced F-ACCEPTANCE. `tasks.md:23` still reads `verification.md 由 spec 侧从该输入派生（crew MUST NOT 直接写）` while `skills/internal/implement-feature/SKILL.md` § Step 9 assigns the population to the implement run. Third feature in this pattern (107, 108, 111).
- **Disposition**: carried open; remediation is a framework-source change (REC-111-02) outside this feature's write set. The round-1 `important` code item is answered in § 2.1.

### F2 — The driver's stage sequence has no feature-registration stage (P1, Workflow) — **open, carried**

- **Round-2 evidence**: unchanged — `checkpoints/07-implement.md:4` still records "the stage closed without registering the feature; the driver added the registry row 111…" (`39be9495a`). The driver's `stage_plan` still has no registration seat.
- **Disposition**: carried open; REC-111-03. The U6 reconciliation debt for sibling rows 109/110 persists.

### F8 — The closed containment set omits the framework-mandated close-out receipt and the engine's settle updates (P1, Workflow) — **open, carried**

- **Round-2 evidence** (re-derived at `e6e1aff7a`): 159 paths; the declared set rejects **5** of them — `.specify/retention/closeout/20261127T091620Z-r20261127T071500Z-111a-review.md` (outside every declared prefix) and four `.specify/session/…-108a.md` records whose bodies carry `feature: 108-team-view-degradation` (fail the A-20 body predicate). This very run's close-out adds a second receipt → 6 at the round-2 commit.
- **Disposition**: carried open; REC-111-08. The finding is design-level: the claim cannot survive its own review stage while the framework mandates writes the claim forbids.

### F3 — Task-row count stated as 19 while the file carries 20 rows (P2, Documentation) — **open, carried**

- **Round-2 evidence**: `checklists/general-best-practices-2026-11-27.md:7` still reads `（19 任务行；…）`; `.specify/features/111-general-best-practices.md:24` reads "Tasks T001–T019 closed"; the registry row reads "19/19 tasks"; `test-evidence/closure-gates.txt` records `tasks=20` (19 T-rows + T007A).
- **Disposition**: carried open; REC-111-06 (state 20 rows including T007A, or define the counting unit once).

### F4 — The containment "final-tree re-read" predates the last three commits (P2, Documentation) — **open, carried**

- **Round-2 evidence**: `test-evidence/containment.txt:81` still labels Reading 2 "final-tree re-read" at `0cbec5aa4` (135 paths); the HEAD reading is 159 paths with the SC-006 invariant intact (0 feature-scope violations; the 5 F8-class paths named).
- **Disposition**: carried open; REC-111-07. This record itself supplies the missing HEAD reading (§ 2.3).

### F5 — Full-suite run 1 executed while the executor was still writing the tree (P2, Workflow) — **open, carried**

- **Round-2 evidence**: `test-evidence/full-suite.txt` still records the invalid window and the authoritative frozen-tree re-run; no new full-suite execution was bought this round (identical tree), so the lesson stands unaddressed in the implement skill.
- **Disposition**: carried open; REC-111-04 (freeze the tree before a full-suite measurement).

### F6 — Code-review `base` resolution picks the fork merge base in a worktree topology (P2, Automation / Scripts) — **open, carried**

- **Round-2 evidence**: not re-probed this round (deliberately — the round-1 reading stands: default `trunk-merge-base` returned `926836e0`, a 13,389-file denominator). The round-2 code segment again used the explicit declared baseline (`--since 0419adae5`), which is the workaround the finding proposes to automate.
- **Disposition**: carried open; REC-111-01.

### F7 — Stage artifacts repeatedly left uncommitted, repaired by the driver (P2, Workflow) — **open, carried**

- **Round-2 evidence**: checkpoints 01 and 02 still record the two driver commits (`d53d3c228`, `652f2c09e`); the round-1 review's own records also needed a driver commit (`534469e54`). This round commits its own artifacts as its brief mandates, which does not change the stage-completion criterion F7 targets.
- **Disposition**: carried open; REC-111-05 (clean-worktree stage completion).

## 4. What Worked — Preserve (Brief)

- The repair followed the round-1 fix exactly: derive `verification.md` from the gate input, keep the statuses verbatim (21/21 checked by program), re-run the checker to `accept`.
- The code segment's rotation is fully mechanical: `start` archives, `note` appends, `receipt` writes the only counts, `report --summary --file` decides the gate — no hand-edited record.
- ARC and the transition gate consumed one machine record each (`final_path` 6/6; the existence test over the current code record) with zero re-derivation.
- The A-20 containment program is reproducible: 159 paths classified at the new head; the delta from the implement reading is fully accounted (declared + F8 class).
- The gate's `important` rule gave the carried DoD-7 finding an explicit answer slot instead of silent carriage.

## 5. spec-kit / SDD Improvement Recommendations (carry-forward)

All eight round-1 recommendations remain **open**; no new `REC-` id is coined this round. The owner of each statement is the round-1 report; this record only carries them forward. The eight ids are **not yet registered** in `.specify/register.md`: the register lies outside this run's briefed write set and outside FR-009's declared containment set, so registration is handed back to the driver (disclosed in § 9).

| Id | One-line change | Target | Source | Status |
|----|-----------------|--------|--------|--------|
| REC-111-01 | Resolve the code-segment base from the spec's declared baseline before the trunk merge base | `skills/internal/code-review/scripts/git-delta-review.sh` (`base` tiers) | F6 | open |
| REC-111-02 | Name the seat that derives `verification.md` (implement run owns Step 9 population; a tasks DoD may not reassign it without naming the deriving stage) | `skills/internal/implement-feature/SKILL.md` § Step 9; `skills/internal/create-tasks/SKILL.md` | F-ACCEPTANCE, F1 | open |
| REC-111-03 | Declare the feature-registration seat (row + detail + status advance) in the driver's stage sequence | `skills/external/sdd-loop-driver/SKILL.md` | F2 | open |
| REC-111-04 | Freeze the tree before any full-suite measurement | `skills/internal/implement-feature/SKILL.md` § Step 8 | F5 | open |
| REC-111-05 | Stage-completion criterion includes a clean worktree (driver commit stays the fallback) | `skills/external/sdd-loop-driver/SKILL.md` (U4 criteria) | F7 | open |
| REC-111-06 | One way to state the task-row count (20 rows incl. T007A, or define the unit) | feature checklists/closure records; tasks-template guidance | F3 | open |
| REC-111-07 | Keep "final" readings actually final (or label them interim with their commit) | evidence conventions (`shared/workflow/acceptance-hardening.md` evidence guidance) | F4 | open |
| REC-111-08 | Make the containment declaration cover the review close-out (receipts + engine-settled records) | closed-set-claims consumers; this feature's FR-009 | F8 | open |

## 6. Priority Roadmap

| Priority | Recommendation | Target File / Subsystem | Source Finding(s) |
|----------|----------------|--------------------------|-------------------|
| — | *(P0 row cleared — `verification.md` derived; closure gate `accept`)* | — | F-ACCEPTANCE (closed) |
| P1 | Name the deriving seat for `verification.md` | `skills/internal/implement-feature/SKILL.md` § Step 9; `skills/internal/create-tasks/SKILL.md` | F1 |
| P1 | Declare the feature-registration stage | `skills/external/sdd-loop-driver/SKILL.md` | F2 |
| P1 | Cover the review close-out in the containment declaration | `shared/guidelines/closed-set-claims.md` consumers; this feature's FR-009 | F8 |
| P2 | Declared-baseline tier in `base` | `skills/internal/code-review/scripts/git-delta-review.sh` | F6 |
| P2 | Freeze the tree before full-suite runs | `skills/internal/implement-feature/SKILL.md` § Step 8 | F5 |
| P2 | Clean-worktree stage completion | `skills/external/sdd-loop-driver/SKILL.md` (U4) | F7 |
| P2 | One task-count phrasing; truly-final readings | feature checklists/evidence conventions | F3, F4 |

## 7. Self-Containment Check

- [x] Every `REC-…` target is repo-relative; the round-1 report holds the full statements and is cited by path.
- [x] Every carried finding states its round-2 verification and disposition; the closed P0 states the evidence that closes it.
- [x] No bullet says "see attached", "as discussed earlier", or references context outside this document plus the committed round-1 record.
- [x] No placeholder tokens remain.
- [x] Section 4 is short and bullet-only.
- [x] Recommendation rows cite exact target files and source findings.
- [x] P0 validation status stated: the closed P0 is a machine fact (checker exit 0 `accept`), not a model judgement; the carried set was re-read on the repaired tree.

## 8. Feedback

Please share the contents of this document with the spec-kit framework developers.

## 9. Round-2 Wrap-up Accounting

Engine verdicts and dispositions for the four composed units (one run, four units, shared run id `r20261127T071500Z-111a`):

| Unit | Run Determination | Exec Quant | Feedback Record |
|------|-------------------|------------|-----------------|
| `/speckit.review` (command) | `duplicate` — round-1 record stands (one record per unit+run) | `duplicate` | `duplicate` |
| `skill:review-sdd-process` | `duplicate` | `duplicate` | `duplicate` |
| `skill:review-feature-quality` | `duplicate` | `duplicate` | `duplicate` |
| `skill:code-review` | `duplicate` | `duplicate` | `duplicate` |

- **Threshold notice**: the store still holds 10 entries (`count=10 threshold=10 should_prompt=true`); the run-determination routing bit is `false` for all four units, so the composed notice stays suppressed per the owner's composition rule — no notification, no transmission.
- **Token reflection**: no machine-managed data file was injected wholesale; deterministic readings (containment classification, status-row verbatim compare, receipt counts, gate verdict, ARC record) came from programs; the guard, the five module documents and the record were read because they are the judgment object. The round-1 record re-read plus the absent need for a full-suite re-run are the two largest savings this round.
- **Documentation evaluation**: 无需记录 — the review produces records, not docs; no docs sync was requested by the stage brief.
- **Close-out receipt**: written for this round under `.specify/retention/closeout/` (new file, written once); it carries the records' disposition and the deviations below.
- **Concurrency attribution**: at entry the worktree was clean; no sibling-line (109/110) path appears in this worktree. The only cross-line session-store change in the range is the run-determination engine's settle of four prior **108** review records (`de9553e23`) — attributed to the engine, recorded under F8, not anomalous.
- **Deviations**: (1) the review runs as a separate `review-round2.md` record (driver brief form) instead of rotating `review.md`; the round-1 record remains untouched history and `code-review.md` rotated normally. (2) The eight `REC-111-*` ids coined in round 1 remain **unregistered** in `.specify/register.md` — the register is outside this run's briefed write set and outside FR-009's declared containment set (writing it would add a path the feature's own SC-006 claim rejects), so the review-command Handoffs registration obligation is handed back to the driver, disclosed rather than silently skipped. (3) The round-1 inventory's test-evidence count is corrected in § 0. (4) This round adds one `.specify/retention/closeout/` receipt of its own, extending the recorded F8 class from 5 to 6 out-of-set paths at the round-2 head.