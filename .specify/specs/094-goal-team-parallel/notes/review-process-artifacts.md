# Review — Segments 1 (process) + 2 (artifacts): 094-goal-team-parallel

**Scope**: this record covers the process segment and the artifact segment of `/speckit.review` only.
The implementation segment (`base..head` delta), the code segment (`code-review.md`) and the Acceptance
Reality Check are **not** run here; the checker's `final_path` record is quoted, never judged.
**Review mode**: strict read-only, no subagents, no edits outside this file.
**Reviewer**: Qoder (review segment A+B) · **Date**: 2026-11-09.

## 0. Portable context

| Field | Value |
|---|---|
| Requirement key | `094-goal-team-parallel` |
| Repository | `cloud-native-ai/spec-kit` (three remotes: github, gitlab, gitee) |
| Branch / HEAD | `master` @ `19003b6131efab4ecdc451f7df8f3e199270a792` |
| Reachability | pushed: `gitee/master`, `github/master`, `gitlab/master` (`git branch -r --contains HEAD`) |
| Review date | 2026-11-09 |
| Environment | Linux x86_64, Python 3.11.11, pytest 8.4.2, git 2.43.5 (plan § Environment Prerequisites) |
| Registry row (read, not written) | `.specify/memory/features.md:101` — status `Planned` (correct for a review-stage line; unchanged by this record) |

**Artifact inventory** (repo-relative, line counts):

| Artifact | Lines | Reading |
|---|---:|---|
| `.specify/specs/094-goal-team-parallel/requirements.md` | 330 | 43 FR / 12 SC / 6 STR; Clarifications incl. R1/R2 |
| `.specify/specs/094-goal-team-parallel/plan.md` | 374 | 22-row Constitution check, 7 decision tensions, 6 execution premises, Project Structure |
| `.specify/specs/094-goal-team-parallel/research.md` | 147 | R-01…R-31 |
| `.specify/specs/094-goal-team-parallel/tasks.md` | 494 | 85 rows, Package Map, DoD, 7 gates |
| `.specify/specs/094-goal-team-parallel/contracts/` (5 files) | 685 | C-1…C-113 (30/24/18/20/21 per file) |
| `.specify/specs/094-goal-team-parallel/data-model.md` | 137 | E-1…E-13, 8 validation rules, 6 state transitions |
| `.specify/specs/094-goal-team-parallel/quickstart.md` | 129 | S-0…S-8 |
| `.specify/specs/094-goal-team-parallel/feature-ref.md` | 117 | FR→clause map (43/43), SC→module map (12/12), 085 disposal |
| `.specify/specs/094-goal-team-parallel/verification.md` | 128 | SC status block + smoke triple + human view |
| `.specify/specs/094-goal-team-parallel/checklists/2026-11-09-requirements-quality.md` | — | 40 items (26 pass / 8 fail / 6 observe) |
| `.specify/specs/094-goal-team-parallel/checkpoints/` (6 files) | 232 | 01-requirements…06-analyze, each with the direction audit |
| `.specify/specs/094-goal-team-parallel/notes/` (28 files) | — | per-package, per-round and wave records |
| `.specify/specs/094-goal-team-parallel/test-evidence/` (200+ files) | — | dated readings, one file per reading |

---

## 1. Process Execution Timeline

Reconstructed from `.specify/state/094-goal-team-parallel.md`, `checkpoints/`, `notes/` and `git log`
(all timestamps CST, 2026-11-09). The line was renamed `092 → 094` mid-flight (`29c3aa08`, 17:39)
after the merged trunk claimed 092 for the Non-Disposable archive pointer.

| # | Step / event | Evidence | Deviation from prescribed flow? |
|---|---|---|---|
| 1 | Requirements stage closes | `af1fcae3`; checkpoint `01-requirements.md`; spine gates line 50 | Minor: run-determination argument-shape friction recorded (not hidden) |
| 2 | Clarify closes with 13 adjudicated Q/A rows | `8badbd03`; checkpoint `02-clarify.md` | None; letter-suffix renumber + un-backticking of `[[STR-]]` citations are framework frictions, disclosed |
| 3 | Plan closes: 111 clauses, 7 tensions, 6 premises | `58516812` + `679a3f51`; checkpoint `03-plan.md` | **Disclosed**: the declared 6-package partition was executed serially by one coordinator (no dispatch tool in that subagent); true parallelism deferred to implement |
| 4 | Tasks closes: 80 rows / 7 packages | `00c36d9c`; checkpoint `04-tasks.md` | None; the `fr-uncovered` 26/42 citation-form lane disclosed as an artifact of the citation grammar |
| 5 | Checklist closes: 40 items; 8 fail rows handed to analyze | `d8ec0a1e`; checkpoint `05-checklist.md` | None; both gates proven red-first |
| 6 | Analyze rounds 1–4 + repairs + anchoring wave + renumber 092→094 | `14c6777e3`…`e8d716e3`, `29c3aa08`, `aeadddd2`; checkpoints `06-analyze.md`; `notes/analyze-round*` | **Deviation, self-corrected**: round-1 repair claimed prose-only closures (disproved round 2); round-3 H-1/H-2; round-4 FV1/FV2 corrections. The loop cost (~60 min on the predecessor line) is recorded as a lesson |
| 7 | Implement wave 1: `wp01-foundation` on the MAIN tree | `a8965b03`, `26688b3de`; `notes/implement-wp01.md:3-5` | **Disclosed**: entry package bypassed `write_isolation=worktree` (no concurrent package at that moment) |
| 8 | `wp02` and `wp03` merge | `2ee5c37b5`, `aaf5cff90`; `notes/implement-wp02.md`, `notes/implement-wp03.md` | **Partial closure**: wp03 merged with 10 red guard tests; 9 engine-dependent rows cannot close inside its write domain (sentinel-level closure not achieved) |
| 9 | Engine-fix wave: `command-family` + `handoff-decision` actions; T084/T085 registered | `7960fb564` + `055f57f0a`; `notes/engine-fix.md`; tasks.md:195,271 | **Deviation, repaired**: F-094-R3-1 — no package's write domain owned `goal-utils.py`; rows 83→85 |
| 10 | `wp04` merges | `531d93e03`; `notes/implement-wp04.md` | **Partial closure**: 5 rows closed (3 package + 2 delegated guards), T055/T057/T058 blocked by domain, T061 half-closed; the note names the Package-Map vs Mutable-state-map contradiction |
| 11 | `wp05` merges | `7201d1fdc`; `notes/implement-wp05.md` | **Partial at closure level**: 18/18 rows closed, but 17–18 disposal-module ids (wp01-caused) are owned by no package — the note's ANOMALY |
| 12 | Consolidation commits interleave on trunk | `c5b17a9fc` (20:32:51), `37aad2954` (20:55:12) | **Interference**: an unrelated line archived 11 spec dirs (incl. `069b`, the 092 tree) and re-pointed their contract paths; `37aad2954` also carried the two wp04 mirror files under a consolidation title |
| 13 | `wp06` + `wp04b` merge | `8c91e832f`, `893077499`, `notes/implement-wp06.md`, `notes/implement-wp04b.md` | **Repaired**: T055/T057/T058 closed, T061's engine half lands (`handoff-ref`); wp06's mirror ANOMALY closed by wp04b |
| 14 | `wp07` closure package | `e865ad865`; `notes/closure-readings.md`; `wp07-closure-acceptance.txt` | **Gate result `block`**: `final_path: pass=6 blocked=1(SC-003) deferred=0 partial=1(SC-002) fail=1(SC-001) unknown=0 total=9`; GATE-1 not readable from the nested worktree; main-repo `trigger/index.json` mutated |
| 15 | Repair wave under user rulings R1/R2 | `3aca34383` + `d2681ba5a`; `notes/repairwave.md` | **Repaired**: authorized apply (16 migrated, 16 noop on rerun), SC-002 pin, SC-010 disposal wave, two one-line repairs; `verdict: accept / final_path 8/8` (run in the repair-wave worktree) |
| 16 | Close-out: merge + sigil sweep | `72ac18551`, `19003b613`; spine line 13 | **Deviation**: all 85 task sigils ticked in one sweep, including T016–T019 whose named evidence does not exist; the spine asserts a main-tree `ACCEPT` reading that has no preserved evidence file; registry stays `Planned` (correct) |

**Process reading.** The prescribed stage chain ran in order (requirements → clarify → plan → tasks →
checklist → analyze → implement → review pending), and every deviation above is surfaced in a dated
artifact rather than silently absorbed. The dominant friction was **task-partition ownership**: the
Package Map's write-domain column, the per-package row lists and the Mutable-state map disagree, which
produced the wp03/wp04 partial closures, the engine-fix wave, wp04b and the final repair wave. Reporting
discipline was strong: every package note carries an explicit `ANOMALY:` line, the R1/R2 user rulings are
quoted verbatim, the repair wave refuses to claim its one non-attributable fixed id, and
`verification.md` uses the five-field measurement ladder for the one partial criterion.

### 1.1 Process findings

| ID | Severity | Anchor | Finding |
|---|---|---|---|
| PF-1 | P1 | `tasks.md:104-126`; `notes/implement-wp03.md:24-28`; `notes/implement-wp04.md:111-120`; `notes/engine-fix.md:7-13` | **The Package Map's write domains contradict the row lists and the Mutable-state map.** wp03's domain omits `scripts/python/goal-utils.py` while T019–T021/T054 require it, and `test_command_run_goal_team.py` is owned by no package; wp04's rows T055/T057/T058 write outside its four-surface domain. Quote (`implement-wp04.md:111`): "the Mutable-state map's cell `wp04/wp03 (T051, T053–T058)` says these guards belong partly to wp04's pen, so the tasks file contradicts itself." Cost: 9+3 blocked rows, two repair waves (enginefix, wp04b) and one criterion (SC-001) left unimplemented. Fix: a partition-validation gate that intersects each package's row set with its declared write domain and fails on an unowned module. |
| PF-2 | P1 | `tasks.md:38`, `tasks.md:47`; `verification.md:103`; `notes/repairwave.md:69-100`; spine `:13` | **The stage closed on a comparison surface narrower than the one its own gate declares, without an owner-recorded decision.** GATE-1/DoD-5 require "zero new failed node ids against the serial baseline … (46 ids at plan entry)"; the last measured set is 186 ids (152−24+58) with 128 pre-existing ids left "on the recorded baseline". The substitution ("causal surface" instead of the 46-id baseline) is disclosed in notes but has no ruling record and no waiver; the spine then asserts the accept. Fix: either re-freeze the baseline with a recorded decision (as the run did for the coverage baseline under D3) or state the closure criterion as attribution-based in `tasks.md` before implement. |
| PF-3 | P2 | `checkpoints/` (6 files); spine `:49-61`; `checkpoints/06-analyze.md:4` | **The implement stage has no checkpoint with the rule-first direction audit.** Checkpoints stop at `06-analyze`; the five-question audit never ran over implement/closure, and the spine's `gates:` block carries no implement row. HR14's cadence degrades to per-package notes, which are reports, not direction audits. |
| PF-4 | P2 | `.specify/.tmp/sdd-loop/forks/094-wp0{3,4,5}/log-*.log` (tails) | **Fork completion sentinels are free text (`WP03-DONE`, `WP04-DONE`, `WP05-DONE`), and the stage-runner's numeric `sentinel=` status is not preserved for any 094 package.** The claim that wp03/wp04/wp05 returned `sentinel=0` is not reproducible from the artifacts; only `checkpoint 06` records `sentinel=1` for the analyze fork waves. |
| PF-5 | P2 | commits `c5b17a9fc`, `37aad2954`; `notes/implement-wp06.md:77-79`; `notes/closure-readings.md:90-95` | **Concurrent unrelated work landed on trunk inside the feature's integration window** (consolidation archived 11 spec dirs, including the `069b` tree the measurement-instrument tests pin, and re-pointed 092/069b paths under a "(094 T022/T025)" label). The measurement surface moved under the run; 9 + 4 + 1 failing ids had to be re-attributed. Handled and disclosed, but no snapshot was frozen, so every pre/post comparison carries a moving-tree caveat. |
| PF-6 | P2 | spine `:13`; `test-evidence/repairwave-closure-acceptance.txt:2`; commit `12dc3e36a` | **The "closure-acceptance on the MAIN tree = verdict ACCEPT" claim has no preserving evidence file.** The only acceptance records are worktree readings whose `spec_dir` is `.specify/.tmp/sdd-loop/worktrees/094-repairwave/...` (no longer on disk); `12dc3e36a` changed only the spine. Single-Run Evidence Discipline asks the decisive run to be captured in full. |

---

## 2. Artifact Review Segment (`### 2.2` slot shape)

### 2.1 Expected set and coverage

| Field | Value |
|---|---|
| Expected set (denominator) | `requirements.md`, `plan.md`, `research.md`, `tasks.md`, `contracts/` (5 files), `data-model.md`, `quickstart.md`, `feature-ref.md`, `verification.md`, `checklists/`, `checkpoints/` — 11 members |
| Coverage line | **11 / 11** |
| Missing members | none |
| Segment verdict | **blocked** — the set is complete, but acceptance honesty fails (AF-1, AF-2); consistency findings AF-3…AF-6 |

`notes/` and `test-evidence/` are the evidence carriers every member points into; they exist
(28 note files, 200+ dated readings) and were sampled for this review, not counted as separate members.

### 2.2 One verdict row per expected member

| Member | Present | Reading |
|---|---|---|
| `requirements.md` | yes | Sound; R1/R2 recorded verbatim (§ Clarifications 271–275); SC-001/SC-012 path markers correct |
| `plan.md` | yes | Sound; 22-row Constitution check, 7 tensions, 6 premises; EP-002's census is stale but self-protected ("the probe's reading, not a frozen constant") |
| `research.md` | yes | R-01…R-31 present; not re-run here |
| `tasks.md` | yes | **Defective**: false-complete T016–T019 (AF-1); stale DoD/GATE lane (AF-2); DoD-4 evidence pointers never produced (AF-5) |
| `contracts/` | yes | 113 definition lines across 5 files; id space C-1…C-113 contiguous; page-ambiguous ids anchored (`handoff#C-53/54`, `unified#C-112/113`) |
| `data-model.md` | yes | 13 entities, 8 validation rules, 6 transitions |
| `quickstart.md` | yes | S-0…S-8 |
| `feature-ref.md` | yes | FR→clause map complete; SC→module map stale/misaligned (AF-4) |
| `verification.md` | yes | SC block honest (SC-001 partial with ladder); human-view path cell wrong for SC-012 (AF-3) |
| `checklists/` | yes | 40 items, 100% traceable, gates proven red-first |
| `checkpoints/` | yes (6 of 8 stages) | 01–06 present with direction audits; no implement-stage checkpoint (PF-3) |

### 2.3 Artifact findings

| ID | Severity | Artifact / line | Finding |
|---|---|---|---|
| AF-1 | P1 | `tasks.md:180-186`; `verification.md:39`; `notes/implement-wp03.md:25` | **T016–T019 are ticked complete although their named evidence does not exist.** The rows say `- [x] T016 … in tests/contract/test_command_run_goal_team.py … evidence: tests/contract/test_command_run_goal_team.py::test_a_command_run_creates_both_definitions_in_the_unified_archive` and `- [x] T019 … evidence: scripts/python/goal-utils.py (create binding write)` — but the module is absent (`file-not-found at T079 collection`) and `create_goal` "carries no binding/owner/origin token" (`verification.md:39`). The final sweep (`19003b613`) changed only the checkbox. Fix: set T016–T019 to the honest state (deferred/blocked-with-R2-pointer), cite the R2 ruling in the row, and keep GATE-4 keyed to "no unchecked row without a disposition". |
| AF-2 | P1 | `tasks.md:37-47` (`DoD-4` 37, `DoD-5` 38, `DoD-7` 40, `**DoD Status**: pending` 43, `GATE-1` 47); `requirements.md:198`, `:274` | **The DoD/GATE lane is stale and self-contradictory after R2 and after the closure.** DoD-7 still lists "SC-001, SC-002, … SC-012 are `final`" while R2 moved SC-001 to `supporting`; `DoD Status` still reads `pending` while the stage was closed; DoD-5/GATE-1 still demand zero new ids versus the 46-id baseline, which no closure reading satisfies. A reader of `tasks.md` alone is told three things the accepted closure contradicts. Fix: update DoD-7's path roster, record the DoD verdict (with the attribution-based comparison surface and its owner decision), and let GATE-1 cite that surface instead of the frozen 46. |
| AF-3 | P2 | `verification.md:120` vs `requirements.md:209` | **The human-readable view marks SC-012 `supporting` while the criterion is `final`.** Row: `| SC-012 | supporting | pass | test_resident_backfill.py green + T083 readings |`. The closure checker reads only the `SC-NNN_status=` lines, so this does not change the verdict — but the rendered view contradicts the owner record. Fix: re-render the table from the requirements' `Path` markers. |
| AF-4 | P2 | `feature-ref.md:81-88` | **The SC→module map is stale after R2 and its description cells do not match the criteria.** Line 81 maps SC-001 to `tests/contract/test_command_run_goal_team.py` (absent, and R2 explicitly says no new guard is implemented); line 82's SC-002 text is "every engine write path reports its binding record" (not SC-002's zero-spec-local-writers criterion); line 88's SC-008 text is the command-family sentence, not the 临时/全局-scan criterion. Fix: regenerate the row descriptions from `requirements.md` and record the R2 delegation for SC-001. |
| AF-5 | P2 | `tasks.md:37` | **DoD-4 names two evidence files that were never produced:** "the T079 readings in `test-evidence/migration-applied.json` plus `test-evidence/residual-after.txt`" — both absent; the actual readings are `repairwave-T079-apply.txt` / `repairwave-T079-probe-after.json`. Fix: point DoD-4 at the produced filenames. |
| AF-6 | P2 | `.specify/memory/features.md:101`; `.specify/memory/features/094.md:47`; `tasks.md:30` | **Registry row and feature detail still record 83 rows `T001–T083`** ("`tasks.md` 83 行（T001–T083）/ 7 包") while `tasks.md` now declares "85 rows, T001…T085" and the gates read 85. The status `Planned` is correct and must not change; the counts are stale. Fix: refresh the count text in the same pass that later moves the status at close-out. |

### 2.4 Ruling records — explicit check

- **SC-001 re-scope (R2)**: the ruling record itself is complete — verbatim user quote at
  `requirements.md:274`, the `**Path**: supporting` marker at `requirements.md:198`, and the
  five-field measurement ladder at `verification.md:39-45` ("own guard and T019 write absent;
  acceptance delegates to SC-004/SC-005"). **Propagation is incomplete**: AF-1 (ticked rows with
  absent evidence), AF-2 (DoD-7 still `final`), AF-4 (module map still names the absent module).
- **SC-003 authorization (R1)**: complete and reproducible — verbatim quote at
  `requirements.md:273`; pre-execution refusal recorded (`wp07-T079-apply-blocked.txt`); applied
  sequence with 16 migrated / 0 conflicts / exit 0 (`repairwave-T079-apply.txt`), post-probe 0/0,
  16/16 existence assertions, idempotent rerun 16 noop with a byte-identical snapshot; definition
  counts on this tree verified at review time (14 `goal.md`, 20 `team.md`).
- **Consistency with the registry row**: `Planned` remains correct (the line has not entered the
  `Implemented → Ready for Review` transition); this review does not change it. Only the count text
  is stale (AF-6).

---

## 3. Findings summary

| Severity | Count | Definition (owner: `templates/review-template.md` § Findings Summary) |
|---|---:|---|
| P0 | 0 | Blocks correct use of spec-kit, or creates silent corruption risk |
| P1 | 4 | Recurring friction across specs — every spec writer pays the toll |
| P2 | 8 | Quality-of-life; compounding gains across many specs |

No P0 findings were raised; the P0 independent-validation pass is vacuously satisfied. (No subagent
validation was used in this run — the dispatch forbids subagents; with P0 = 0 the obligation is empty.)

**Finding IDs**: process — PF-1…PF-6; artifacts — AF-1…AF-6.

## 4. What worked — preserve

- Every package note carries an explicit `ANOMALY:` line and names what it did **not** repair.
- R1/R2 are recorded as verbatim user quotes plus the derived status change — no paraphrase.
- The repair wave refuses to claim its one non-attributable fixed id and classifies all 58 new ids
  by environment cause instead of asserting a pass.
- `verification.md` uses the five-field measurement ladder for the one partial criterion and states
  "delegated evidence is not its own evidence".
- Per-reading evidence files (one file per reading) and name-level suite diffs (`comm`, LC_ALL=C)
  made the closure auditable.
- The closure checker's record is quoted verbatim in the notes rather than recomputed.

## 5. Verdicts

- **Process segment: pass** — stage order held, every deviation is disclosed in a dated artifact,
  and the repair waves are named and evidenced. The two P1 findings (PF-1 partition ownership,
  PF-2 closure-gate substitution) are framework-level friction to fix, not silent process failure.
- **Artifact segment: blocked** — the expected set is complete (11/11) and the SC-level record is
  honest, but the task ledger claims completions its evidence does not support (AF-1) and its
  DoD/GATE lane is stale and unmet (AF-2).
- **Findings counts**: P0 0 · P1 4 · P2 8 · total 12.
