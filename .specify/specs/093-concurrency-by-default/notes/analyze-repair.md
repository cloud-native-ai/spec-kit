# Analyze-repair — 093-concurrency-by-default

**Stage**: analyze-repair (the stage implied by the analyze stage's NOT-READY verdict)
**Branch / worktree**: `093-concurrency-by-default` @ `.specify/.tmp/sdd-loop/worktrees/093-clarify`
**Base commit**: `215c3dcb` (opened after the upstream merge `95e44f3a`)
**Date**: 2026-11-09
**Inputs**: `notes/analyze-findings.md` (15 findings; NOT-READY 1C/3H/8M/2L; repair brief § 6), checkpoints 03–06, `requirements.md`, `plan.md`, `tasks.md`, `contracts/*`, the spine, and the merged trunk.
**Execution shape of this stage**: serial, one executor. The two dated user rulings this stage encodes (FR-034 / FR-035) are about the *mechanism*; until that mechanism lands, this stage's own record is `mechanism-not-yet-landed` ([[STR-010]]), exactly as the stage records before it. SC-006 stays `not_evaluated` (F-093-011).

---

## 0. Repair verdict

**CRITICAL 0 / HIGH 0.** Both HIGH-severity blockers (F-093-005, F-093-006, F-093-007) and the CRITICAL (F-093-009) are closed; every remaining open item is MEDIUM or LOW with a recorded state (below). The verdict flips from NOT-READY to **ready for analyze round 2** — the next analyze pass must independently verify this ledger, the directive encoding, and the trunk reconciliation.

A **retry note** applies to this stage: a previous host-internal run died mid-edit, leaving `requirements.md` modified. That partial edit was assessed item by item before continuing — what was correct was kept (FR-031 rewrite, FR-001 exclusion sentence, FR-006/SC-003 group scoping, FR-032 anchoring rewrite, the member-count owner sentence, FR-034, the first Clarifications bullet), and what was incomplete was completed (FR-034's definition-row syntax and dead anchor, FR-035, the second Clarifications bullet, every contract/plan/tasks/feature-ref row, the ledger, the spine).

---

## 1. Closure ledger — per finding

| id | severity | state | evidence |
|----|----------|-------|----------|
| F-093-001 | — | **resolved** (plan), unchanged | `feature-ref.md` § Overlap adjudication |
| F-093-002 | — | **open** (framework), unchanged | this ledger § 5; spine `findings` |
| F-093-003 | — | **adjudicated** at analyze; work is implement-stage (T096/T098/T101/T105), value is an owner decision | `notes/analyze-findings.md` § 3 |
| F-093-004 | — | **RESOLVED, verified** — the ruling is recorded (findings § 2, register, spine) and implement row **T138 now exists** in `tasks.md` (Phase 8) with the framework-source targets; not re-litigated | `tasks.md` T138 |
| F-093-005 | HIGH | **CLOSED** — the FR lane reads **35 / 35** claimed (was 25 / 33): FR-011 / FR-013 → C-029's group, FR-016 → C-040, FR-017 / FR-028 → C-069…C-071, FR-025 → C-078's new group, FR-027 → C-066 / C-067, FR-033 → C-079…C-092's groups; FR-034 / FR-035 → C-093 / C-094 | `account-clause-coverage.py` reading in `test-evidence/analyze-repair-gates.txt` § G2 |
| F-093-006 | HIGH | **CLOSED** — FR-001 now excludes all three derived projection trees (command copies, `.specify/skills/` flat layer, `.specify/agents/templates/`) with the mirror-discipline owner named; C-005's `excluded_layers` names the same trees plus the two spec-local layers | `requirements.md` FR-001; `contracts/declaration-facts.contract.md` C-005 |
| F-093-007 | HIGH | **CLOSED** — FR-006 states the `condition-bound` / `factual` partition in its own text; SC-003's red-count sentence is group-scoped; the dated Clarifications answer is untouched | `requirements.md` FR-006, SC-003 |
| F-093-008 | MEDIUM | **CLOSED** — the Shared Strings section now carries the one-sentence owner ("成员数量与成员清单只以 [[STR-003]] 条目为准；Clarifications 中的数字是历史记录") | `requirements.md` § Shared Strings |
| F-093-009 | CRITICAL | **CLOSED** — FR-031's `"+'+'+"` fragment is gone (`grep -c '+"' = 0`); the row is one definition row stating the landing discipline, the mirror rule and the five fact landing pairs; `validate-requirements.py` 0 / 0 | `test-evidence/analyze-repair-gates.txt` § G1 |
| F-093-010 | MEDIUM | **CLOSED for the named clauses** — C-018 → FR-031, C-062 → FR-032, C-072 → FR-021 / FR-023, C-078 → FR-025, C-079…C-081 → FR-032, C-085…C-092 → FR-033; the finding's explicit exclusions (C-019–C-022, C-026, C-039, C-048, C-082–C-084) were left uncoupled, per its own instruction not to invent couplings | `contracts/*` |
| F-093-011 | MEDIUM | **accepted, unchanged** — SC-006 stays `not_evaluated`; only the feature's own engine running on the feature's own run closes it | `requirements.md` A4; `tasks.md` SC-006 evidence plan |
| F-093-012 | MEDIUM | **FIXED** — (a) the false "no dispatch tool" premise is corrected in the live artifacts (`plan.md` § Concurrency plan, `tasks.md` § Environment Prerequisites and § SC-006 evidence plan, `plan.md` R-3), and checkpoints 03 / 04 / 05 each carry one dated correction note above an untouched body; (b) the affected-task pointer now names T101 / T103 / T105 and the SC-006 evidence plan (T106 / T110), not T102; SC-006's stated reason is aligned: the gap is the feature's **mechanism**, not the host's tool set | `plan.md`; `tasks.md`; `checkpoints/03-plan.md`…`05-checklist.md` heads |
| F-093-013 | MEDIUM | **CLOSED** — the delivery map's closing claim no longer asserts totality by hand; it points at the `account-clause-coverage.py` reading as the evidence | `feature-ref.md` § Delivery map |
| F-093-014 | MEDIUM | **open by rule, unchanged** — `create-checklist` § Recheck forbids refreshing an existing checklist file; the correct form is a `recheck-<date>-<topic>.md`, which a later checklist pass may write. The checklist file is untouched | `checklists/2026-11-09-requirements-quality.md` |
| F-093-015 | MEDIUM | **routed to an implement row** — the dead one-line-per-task owner pointer in `templates/tasks-template.md` L110 (and its mirror) is folded into **T138**, because framework source outside the spec dir is not edited in analyze | `tasks.md` T138 |
| F-093-016 | LOW | **recorded note stands, no edit** — the body routes the projection-mirroring discipline to FR-032; the Clarifications line is a dated record (append-only) | `notes/analyze-findings.md` § 4 |
| F-093-017 | LOW | **CLOSED** — DoD-1 no longer restates a tag count (the "34 rows" claim is gone); the machine-checkable property (`validate-tasks.py` exits 0 with 0 WARN) is the sentence; the FR / clause ranges were updated to FR-035 / C-094 | `tasks.md` DoD-1 |
| F-093-018 | MEDIUM | **RESOLVED by confirmation** — measured: the 14 agent files carrying "Never dispatch another agent" are exactly the 14 files carrying a `## Responsibilities` heading (`comm -3` empty), so the § Responsibilities citations are accurate; no edit | this ledger § 5 |
| F-093-019 (NEW) | MEDIUM | **recorded, not renumbered** — the merged trunk carries two `092` rows in `features.md`: 092 Non-Disposable (absorbed into 090, retained as an archive pointer) and 092 Goal/Team Parallel. Every "092" in 093 means **092-goal-team-parallel**; fixture row **T090** was disambiguated in place (filename kept — renaming would break every reference); no 092 reference was renumbered. Impact: a reader searching "092" reaches two rows; the fixture's target file name `test_concurrency_reproduction_092.py` stays as-is and T090 now states which 092 it reproduces | `tasks.md` T090; `register.md` |
| F-093-020 (NEW) | MEDIUM | **recorded behavioural conflict, convergence at implement** — the user ruling encoded as FR-035 (FORK model through `stage-runner.sh`, `nproc`-bounded) conflict with today's text: `references/dispatch-recipes.md` § 本地原生拓扑 and `SKILL.md`'s topology line say local stage dispatch MUST NOT launch `qodercli` and MUST use host-native subagents; `decomposition-model.md` makes host-native subagents the local default. Also (for FR-034) `decomposition-model.md` § 20.1 sets `analyze` to `off`. The two conflicts converge through one explicit revision at implement (FR-033 disposal list; rows T140 / T142), not by an in-place edit here — editing the framework rule in analyze would decide the ruling by paraphrase and edit framework source outside the spec dir | `requirements.md` Clarifications 2026-11-09; `plan.md` § The analyze wave and its fork mechanism; `register.md` |

---

## 2. Where the two user directives landed

Both are **dated user rulings** (not self-adjudications, not clarifications inferred from the repo) and are recorded in `requirements.md` § Clarifications → *Session 2026-11-09 (analyze-repair · 用户裁定)*, one bullet per directive, verbatim quote first.

**(a) "the analysis stage can use multiple SDD Analysis Workers concurrently"**

- Requirement: **FR-034** — analyze defaults to N concurrent SDD Analysis Workers; N from the stage team configuration / spine `agent_concurrency_requested` (never a number in this spec); serial only with a closed-vocabulary reason code; three co-required properties (per-Worker file-level read domains red before dispatch; deterministic consolidation by declared domain order → finding id order with a first-declaration tie-break; the reading triple + `executor_id` / `verifier_id` per Worker); boundaries (stage chain, sentinels, analyze gate strength unchanged).
- Contract: **C-093** (high-order-executors § F), including its `[green:]` claim in T139.
- Plan: `plan.md` § *The analyze wave and its fork mechanism* — owners, default override location, and the recorded `decomposition-model.md` § 20.1 conflict.
- Tasks: **T139** (driver surfaces), **T140** (decomposition model § 20.1; the fact value itself is authored by T013, extended), **T141** (contract test).
- Composition: FR-034 is a **specialisation** of FR-028 / FR-005 / FR-016 on one stage, not a third criterion family.

**(b) "the concurrency mechanism is the FORK model — separate qodercli child processes launched through stage-runner.sh (stdin prompt + stream-json + sentinel), sized to nproc, NOT host-internal Agent fan-out (in-process subagents share one process/CPU and saturate a single core)"**

- Requirement: **FR-035** — independent `qodercli` child processes through `skills/external/sdd-loop-driver/scripts/stage-runner.sh`; prompt via stdin, `--output-format stream-json`, completion by stage sentinel; pool bound = the host's `nproc` **read at dispatch** (never frozen; `min(requested, nproc, slot cap)` with FR-008's reason); host in-process fan-out MUST NOT be recorded as the concurrency mechanism and MUST NOT satisfy FR-005(d); FR-021 (c)'s external-process form is what this fixes; the runner's positive-evidence quartet (pid/status/log/heartbeat) is unchanged.
- Contract: **C-094** (high-order-executors § F), `[green:]` claim in T142.
- Plan: the same `plan.md` subsection (mechanism paragraph).
- Tasks: **T142** (rewrite the local-topology surfaces), **T143** (contract test: runner shape against `stage-runner.sh --help`, frozen-`nproc` mutation red, in-process fan-out rejected).
- FR-033's disposal list was extended: the driver's existing local-topology dispatch rule is now one of the statements this feature must disposition, so the change lands through the recorded disposal discipline rather than as a silent override.

**Measured basis for the notes above** (2026-11-09, this worktree): `stage-runner.sh` already redirects the prompt file into the CLI's stdin and defaults to `--output-format stream-json` with a sentinel-driven status file (`stage-runner.sh` L292, L350) — the mechanism the ruling names exists; what does not exist is the analyze wave that launches N of them. `decomposition-model.md` § 20.1: built-in defaults `plan / implement / review = auto`, **`analyze` = `off`** — hence the recorded conflict.

---

## 3. Trunk reconciliation (merge `95e44f3a`)

**3.1 The anchoring rename (`.specify/goal/` → `.specify/anchoring/`).** Measured: `.specify/goal` no longer exists; `.specify/anchoring/` holds 6 entries; `goal-definitions.md` declares the global scope as "Anchoring (锚点)" at `.specify/anchoring/<slug>/goal.md` and states explicitly that *scope is not a lifetime* (line 34: "No 'temporary' property … Neither expires").

- Aligned in 093 (mechanical references): FR-001's fifth enumeration root; FR-032's goal-executor paragraph (the partial edit already replaced the "存档目标 vs 临时目标" reading with the *scope = storage location* reading, matching the merged owner — verified, kept); `quickstart.md` S-0 counts line; `research.md` R-6 table row; `tasks.md` T003's measurement line. The count stays 6 on both trees.
- Left as dated records (append-only): the Clarifications lines that quote the old path while recording the clarify session; `checklists/2026-11-09-requirements-quality.md` CHK001 / CHK027; `test-evidence/*`.
- **Partial-rename facts recorded, not repaired here** (outside 093's territory): the archive entry file is still `goal.md`; `--scope` still takes `global|spec|auto`; `register.md`'s own first rows still point at `.specify/goal/...`. These are trunk-side surface inconsistencies; 093 writes none of them and cites only what `goal-definitions.md` owns.

**3.2 The duplicate 092 numbering.** `features.md` now carries two rows numbered 092 — Non-Disposable (absorbed into 090; registry row retained as an archive pointer) and Goal/Team Parallel. Impact on 093: every "092" reference in this spec means **092-goal-team-parallel** (the 6-package plan, the reproduction fixture, the goal/team parallelism being dispositioned). Recorded as **F-093-019**; T090 carries a one-sentence disambiguation and the fixture filename is unchanged. No reference was renumbered — silently renumbering would break the register, the clause ids and every citing artifact at once.

**3.3 Behavioural conflicts recorded as findings.** F-093-020 (FR-034 / FR-035 versus the driver's current local-topology rule and § 20.1's `analyze: off`). Both converge at implement through FR-033's disposal discipline; the refused in-place edits are named in the plan subsection and § 5 below.

---

## 4. Gate readings (post-repair; full command lines, stdout/stderr, exit codes in `test-evidence/analyze-repair-gates.txt`)

| # | Gate | Reading | Verdict |
|---|------|---------|---------|
| G1 | `validate-requirements.py requirements.md` | `status: ok` — 335 lines, 47 definition rows (35 FR + 12 SC), 11 shared strings, **0 error / 0 warning**, EXIT 0 | PASS |
| G2 | `account-clause-coverage.py … --corpus-root <worktree>/.specify/specs` (no `--freeze`) | **FR lane 35 / 35 pass** (`[fr-uncovered] pass (0)`); clause lane `status: baseline-missing`, EXIT 2 — expected (T006 has not run) and reported honestly; the baseline file is absent and was **not** created here | PASS on the lane F-093-005 owns; clause lane red-by-baseline-missing, expected |
| G3 | `validate-tasks.py tasks.md` | `PASS — 0 error(s), 0 warning(s)`, EXIT 0 — **143 rows**, T138–T143 added, C-093 / C-094 claimed once each | PASS |
| G4 | `validate-decision-tensions.py --spec <spec-dir>` | EXIT 0 — 5 records T-001…T-005 intact after the plan edit | PASS |
| G5 | `pre-analyze-check.py --repo <worktree> --spec-dir … --stage requirements / plan / tasks` | all three `decision=pass`, **0 errors**, 111 advisories (creation-target paths + dated-history paths, each named in the evidence), `fr=35 / sc=12 / tasks=143` | PASS |
| G6 | `decomposition-check.py --mode tasks` | `proceed` — **35 FR / 143 tasks** against ceilings 120 / 160 | PASS |

The first post-repair gate run (`test-evidence/analyze-repair-gates-attempt1.txt`, retained) reported two `count-claim` errors, both on **dated** lines that still carried the pre-ruling counts: `plan.md`'s plan-stage gate row ("33 FR") and the checklist header ("33 FR"). Both were marked as historical readings in the checker's own vocabulary (plan: "33 FR was the count at that reading"; checklist: a dated delta annotation that keeps the original number visible and points here) — not deleted, not waived. The final run is `analyze-repair-gates.txt`; the attempt is retained as a dated record rather than overwritten (single-run evidence).

Every earlier green reading stayed green: requirements 0/0, tasks 0/0, decision-tensions 5 records, decomposition proceed, and the checklist evidence is untouched (no checklist row was edited).

---

## 5. Fast-fail decisions in this pass

**Repaired in passing, disclosed here** (each is one reading consistent with the recorded intent — corrections of *this stage's own* partial edit or of a mechanical path, never new intent):

1. FR-034's definition row was written `**FR-034**（用户裁定，2026-11-09）：` — `pre-analyze-check.py`'s definition regex requires `- **FR-034**:`, so the number was invisible to it and two dangling-id errors appeared. Moved the annotation after the colon. `validate-requirements.py` had counted it (its regex is laxer) — the pair disagreed exactly as the spine's framework observation describes.
2. FR-034's landing sentence named a section "「质量门编排 / analyze 门」" that does not exist in `references/dispatch-recipes.md`; re-pointed to the real headings (`## 本地原生拓扑`, and via FR-035 to `## Recipe 2`).
3. The 092 disambiguation in T090 is a one-sentence clarification of an ambiguous reference, not a renumbering (F-093-019).
4. F-093-015 was folded into T138 instead of a sixteenth row so the same owner document (tasks-template L110) is repaired once.
5. Two stale `33 FR` count claims failed `pre-analyze-check`'s `count-claim` rule on the first attempt. Both sit on dated lines (the plan-stage gate row and the checklist header). They were converted to dated readings — the checklist header keeps the original number and adds the delta pointer here — rather than deleted or waived. This is the same "dated correction note" shape the brief authorised for checkpoints; the checklist's verdicts and items were not touched.
6. A dangling `Txxx` / `Tyyy` advisory in the tasks `Format` legend is the shipped template's placeholder syntax, pre-existing and unrelated to this pass; left as-is.

**Refused (surfaced, not absorbed)**:

1. Editing `references/dispatch-recipes.md` / `decomposition-model.md` / `SKILL.md` in place to match the user rulings — framework source outside the spec dir, and the edit would have decided the ruling's convergence by paraphrase; routed to T140 / T142 and F-093-020.
2. Freezing `coverage-baseline.txt` to turn G2 green — answers a different question (the analyze stage refused it for the same reason; this pass did not run `--freeze` either).
3. Editing the 2026-11-09 checklist to refresh CHK002 / CHK008 / CHK009 verdicts — checklists are append-only; the recheck form is a separate dated file (F-093-014).
4. Rewriting checkpoint bodies 03 / 04 / 05 — one dated correction note each, bodies untouched.

---

## 6. Anomaly line

**ANOMALY: none unreported** — one anomaly was carried in and is fully disclosed above (the died-mid-edit partial state, assessed and completed, not redone); two new findings were coined (F-093-019 duplicate-092 numbering, F-093-020 ruling-vs-current-rule behaviour conflict) and registered; no gate was weakened, no baseline frozen, and no framework source outside the spec dir was edited.
