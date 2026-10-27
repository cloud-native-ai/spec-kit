# Analyze RERUN Report: Feature 071 — Review × Code-Review Composition

**Command**: `/speckit.analyze` (strictly read-only, rerun 1 of max 1) · **Stage**: analyze · **Date**: 2026-10-27
**Requirement dir**: `.specify/specs/071-review-code-integration`
**Trigger**: first analyze run returned `GATE: CRITICAL=0 HIGH=6` (32 findings) — `test-evidence/analyze-report.md`. One upstream repair round followed: `14a1c6ec` (requirements) → `2c42bbbe` (plan) → `fc007019` (tasks).
**Prior report**: `test-evidence/analyze-report.md` (A-01…A-33). This run is the rerun-delta of that report.
**Artifacts under analysis (re-read in full at the repaired state)**: `requirements.md` (308 lines, 28 FR / 7 SC / 5 user stories / 10 shared strings), `plan.md` (299), `research.md` (R1–R14 + DR1), `data-model.md` (E1–E13, V1–V35), `contracts/*` (6 files, 74 clauses — C-1…C-73 + appended C-74), `quickstart.md` (A–H), `feature-ref.md`, `tasks.md` (36 rows), `checklists/requirements.md` (16/16), `checklists/review-composition.md` (40 items, 13 PASS / 27 FAIL), registry (`.specify/memory/features.md` row 071, `features/071.md`), constitution v1.13.0 (16 principles).

---

## 0. Method and the two disclosure obligations

**Scope discipline.** This stage wrote exactly two files: this report and the updated `test-evidence/analyze.jsonl`. No requirement, plan, contract, data-model, quickstart, feature-ref, task, checklist, code, template, skill, script, test or registry file was modified. Every finding below is reported, never applied.

**Same-author detection delegation (`shared/workflow/objective-analysis-gate.md`) — gate does NOT fire.** The chain under analysis was authored by earlier stage subagents in prior sessions (`8d18265b` requirements, `0d2d2d66` clarify, `4932c2b1` plan, `398ab796` tasks, `89daf845` checklist) plus the three remediation commits, none of which this session wrote. Independent authorship supplies the fresh context the gate exists to obtain.

**Detection path (disclosed).** This execution environment exposes no subagent dispatch (tools: file read/write/edit, shell, glob, grep — no Agent/Task dispatch). Detection was a bounded direct read of all artifacts above plus every live framework source a claim names, re-measured here: `templates/commands/review.md` (53 lines, `wc -l`), `templates/commands/checklist.md:36`, `shared/workflow/feature-integration.md:37/:38`, `templates/feature-details-template.md:71`, `skills/internal/code-review/scripts/git-delta-review.sh:22` / `:99-103` / `:442-446`.

**Validation path (disclosed).** The rerun's decision points could not be dispatched to an independent validation wave. Each closed finding was re-opened at its cited locus rather than re-argued from the remediation's own notes; each row below carries `(validated: direct re-read, subagent unavailable)`. Sent 6 HIGH + 26 others / confirmed closed 33 / downgraded 0 / still-open 0. **That 0-rejection rate is not accuracy evidence** — the confirming reader is the reading reader. Rule 6's downgrade metric stays unreportable for this run, not satisfied.

**Plan-constraint audit (`plan_constraint: active`, plan commit `2c42bbbe`).**

```
$ git diff --stat 2c42bbbe..HEAD -- .specify/specs/071-review-code-integration/
 tasks.md                                        | 143 +++---
 test-evidence/tasks-remediation-*  (8 files)    | 1000 ++++++++++++++++
$ git diff --stat 2c42bbbe..HEAD      (whole tree)
 .specify/memory/features.md +2/-2 · features/071.md +4/-4 · the two groups above
```

`plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`, `notes/plan-stage-checks.md`: **zero diff** since `2c42bbbe`. The tasks remediation touched only `tasks.md`, its evidence files, and the feature registry (unowned bookkeeping). **No substantive or undeclared change to a plan-owned artifact; no `PLAN-EDIT:` declaration was required and none is asserted.** `(validated: git diff, subagent unavailable)`

---

## 1. Deterministic rerun results (all re-executed, not inherited)

```
$ python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/071-review-code-integration
FR universe: 28 · FR claimed: 28 · FR uncovered: 0
companion: claimed clauses 74, scanned files 197, clause universe 1109, FR universe 28
  [clause-uncovered] pass (495) — 495 uncovered, 0 beyond the frozen baseline
  [fr-uncovered]     pass (0)   — 28 of 28 FRs cited from citation groups
  [clause-unparsable] warn (94) — 94 files yield no clause id; 0 declare a positive form
  [coverage-baseline-delta] pass (0) — baseline holds 495 names
0 error(s), 0 warning(s) · status: ok · exit 0

$ python3 .specify/scripts/python/clause_extract.py .specify/specs/071-review-code-integration/contracts/*.md
code-review-skill 14 · command-orchestration 16 · coverage-receipt 15 ·
feedback-and-boundaries 10 · status-gate-ownership 10 · tests-and-docs-sync 9
total_clauses = 74 (16+14+15+10+10+9) · every block carries a non-empty citation group

$ python3 scripts/python/validate-tasks.py …/tasks.md         → PASS: 0 error(s), 0 warning(s), exit 0
$ python3 scripts/python/validate-requirements.py …/requirements.md
                                                             → 0 error(s), 0 warning(s) · 35 definition
                                                               rows (28 FR + 7 SC) · 10 shared strings
```

**Claim partition (re-derived, not trusted).** `[green: …]` tags in `tasks.md` = 75 occurrences; 74 of them are clause claims and the 75th is the format example `[green: <contract>#<clause>]` on the format line. Unique claims per file: command-orchestration 16, code-review-skill 14, coverage-receipt 15, status-gate-ownership 10, feedback-and-boundaries 10, tests-and-docs-sync 9 = **74**, every clause claimed exactly once, C-74 on T018 (`tasks.md:262`).

**Other counts re-measured**: 36 task rows; `doD-2`'s 74 holds; shared-string rows 10 (`STR-001`…`STR-010`, no id outside that range used anywhere in the artifact set); checklist 40 items / 27 unchecked; the six contract files named as Shared-Strings consumers all exist.

**Verdict**: the three measured premises the tasks remediation corrected (Shared Strings 4 → 10, clauses 73 → 74, transition surfaces re-grepped) are **true** at the current tree. The round-1 report's `73/73` figure is now `74/74`, and the one beyond-baseline name it produced at plan time (`#C-74`) is claimed rather than re-frozen.

---

## 2. Per-finding closure matrix (A-01…A-33)

`closed-by` names the commit and the locus that carries the repair, re-opened at that locus. Every row is `(validated: direct re-read, subagent unavailable)`.

### 2.1 The six HIGH rows

| ID | closed-by (commit · locus) | Why the finding no longer holds |
|----|---------------------------|---------------------------------|
| **A-01** | `14a1c6ec` · `requirements.md:170` FR-019, `:151` FR-012, `:208` SC-001, `:272` adjudication · `2c42bbbe` · `contracts/command-orchestration.md:34` C-14, `contracts/status-gate-ownership.md:22` C-52 / `:24` C-53, `contracts/coverage-receipt.md:32` C-43, `data-model.md:30` (E1), `:175` V22, `:213` (E13) · `fc007019` · `tasks.md:216` T008, `:262` T018, `:282` T022 | The closing summary is no longer a carrier anywhere. Two verifiable carriers are named (`review.md` § 2.1 + the feature detail's `## Latest Review` entry); the summary is a presentation with "no independent content obligation", and the carriers govern on disagreement. SC-001 keeps the one-file reading. The duplicate-carrier defect is gone, not reworded. |
| **A-02** | `14a1c6ec` · `requirements.md:119-123` FR-003, `:99` edge case, `:212` SC-005 · `2c42bbbe` · `contracts/command-orchestration.md:20` C-7, `contracts/code-review-skill.md:34` C-30, `data-model.md:69` E4 `basis` / `:77` V30, `plan.md:175` § 2 / `:243` R-13 · `fc007019` · `tasks.md:209` T004, `:214` T006, `:237` T011 | "What counts as a code path" has exactly one owner — the skill's deterministic script with a closed default set and `--code-paths` — and both the command template and the requirement are forbidden from carrying a second list. The empty-delta case is decided before the receipt runs. A mixed delta is now mechanically decidable, so SC-005 is testable. |
| **A-03** | `14a1c6ec` · `requirements.md:127-129` FR-004, `:43` US2 scenario 1 · `2c42bbbe` · `contracts/code-review-skill.md:10` C-18 / `:16` C-21, `data-model.md:84` E5 `head_sha` / `:91` V31, `research.md:54` · `quickstart.md:44` | Head is specified with the same rigour as base: explicit `--head` > `HEAD` resolved once at run start and fixed for the run; the range MAY contain unrelated commits; strict slicing requires an explicit head; both SHAs plus the base source are recorded so `git diff base..head` recomputes. The one asymmetry (head carries no source tier) is a *declared* decision in V31 and `research.md`, not an omission. |
| **A-04** | `14a1c6ec` · `requirements.md:130` FR-005, `:148` FR-011 · `2c42bbbe` · `contracts/command-orchestration.md:24` C-9 / `:34` C-44, `data-model.md:72` E4, `:213` E13 · `fc007019` · `tasks.md:215` T007, `:262` T018 | The two MUSTs no longer dictate opposite acts: FR-011's closed list now *contains* the uncommitted-scope disclosure, and the design states it is one fact with two carriers by design (report subsection + record), not two criteria. |
| **A-05** | `14a1c6ec` · `requirements.md:136` FR-008, `:211` SC-004, `:67/:71` US4, `:276` adjudication · `2c42bbbe` · `contracts/status-gate-ownership.md:10` C-46, `contracts/coverage-receipt.md:20` C-37 / `:22` C-38, `data-model.md:62` V6 / `:163` V35 · `fc007019` · `tasks.md:278` T019, `:282` T020 | The unrepresentable state is retired rather than defined: the gate is an existence predicate over the current record ("≥1 `blocking` heading blocks"), "clearing"/"cleared" is explicitly forbidden, and SC-004's second run is a *rereun producing a record with zero `blocking` entries* instead of a clearing action. The instrument's existing presence-based count (`git-delta-review.sh:442-446`, `^### .* \[blocking\]`) is retained as the implementation. |
| **A-06** | `14a1c6ec` · `requirements.md:186` FR-027 · `2c42bbbe` · `contracts/feedback-and-boundaries.md:26` C-64, `contracts/tests-and-docs-sync.md:12` C-67, `research.md:115`, `plan.md:233` R-03, `feature-ref.md:88` · `fc007019` · `tasks.md:319` T030, `:21` DoD-4 | FR-027 now authorizes exactly one assertion change, in its own words: keep the subject, add the owner-path assertion, add a negative assertion that the removed wording is gone, net assertion count rises, rationale declared in the feature detail's review-record entry, **non-precedential**. C-64/C-67 say the same; T030/DoD-4 cite the exception instead of an absolute prohibition. The pin is rewritten, never retired (`research.md:112` rejects deletion explicitly). |

### 2.2 The 22 MEDIUM rows (round-1 numbering retained)

| ID | closed-by (commit · locus) | Verdict |
|----|---------------------------|---------|
| A-07 | `14a1c6ec` · `requirements.md:118` FR-002, `:296` · `2c42bbbe` · `contracts/command-orchestration.md:16` C-5, `data-model.md:47` E2 | CLOSED — the abort case names carrier *and* author: the command writes a minimal `review.md` carrying only the code subsection + abort reason, so the carrier stays single. |
| A-08 | `14a1c6ec` · `requirements.md:145` FR-010, `:297` · `2c42bbbe` · `contracts/command-orchestration.md:28` C-11, `data-model.md:76` V29 · `quickstart.md:71` | CLOSED — record existence is tied to the triage value: only `run` writes `code-review.md`; `not-applicable`/`not-evaluated` write no file, not even an empty one; conclusion and reason live in the report subsection. |
| A-09 | `14a1c6ec` · `requirements.md:234` `STR-005` · `2c42bbbe` · `contracts/command-orchestration.md:18` C-6, `data-model.md:68` E4 | CLOSED — `run` is a pinned Shared String and the triage set is cited by id. |
| A-10 | `14a1c6ec` · `requirements.md:127` FR-004, `:102` · `2c42bbbe` · `contracts/code-review-skill.md:10` C-18, `data-model.md:88` V9, `research.md:52` | CLOSED — trunk identification is a closed five-step order ending in a pinned literal; no heuristic outside it is allowed, which is what makes two resolvers agree. |
| A-11 | `14a1c6ec` · `requirements.md:123` FR-003, `:156` FR-014 · `2c42bbbe` · `contracts/command-orchestration.md:20` C-7, `contracts/coverage-receipt.md:22` C-38, `data-model.md:162` V20 / `:77` V30 | CLOSED — the conjunction is scoped to `run` with a non-empty changed set; an empty delta is triaged before the receipt runs, so a 0/0/0 pass over nothing is unreachable at the requirement layer, not only in the data model. |
| A-12 | `14a1c6ec` · `requirements.md:158` FR-014 · `2c42bbbe` · `contracts/coverage-receipt.md:14` C-34 / `:16` C-35, `data-model.md:172` E10 · `fc007019` · `tasks.md:259` T015, `:262` T018 · `quickstart.md:115` | CLOSED — the exit alphabet is closed at `0`/`1`/`2` with one meaning each, stated at requirement layer, in the contracts, in the data model and in the drill. |
| A-13 | `14a1c6ec` · `requirements.md:160` FR-014 · `2c42bbbe` · `contracts/coverage-receipt.md:18` C-36, `data-model.md:128` E7 / `:141` E8 / `:145` V34 | CLOSED — five legal reasons; any other reason (free text included) is a coverage gap with exit `1`. "Reasoned" now has testable content. |
| A-14 | `14a1c6ec` · `requirements.md:235` `STR-006` / `:236` `STR-007` · `2c42bbbe` · `contracts/coverage-receipt.md:24` C-39, `data-model.md:149` E9 | CLOSED — `pass` and `blocked` are pinned and cited by id wherever the verdict set is closed. |
| A-15 | `14a1c6ec` · `requirements.md:210` SC-003 · `2c42bbbe` · `contracts/code-review-skill.md:20` C-23 | CLOSED — SC-003 owns a closed four-literal forbidden list; the test searches each literal verbatim, not a broad word. Adding a phrase requires amending SC-003 first. |
| A-16 | `14a1c6ec` · `requirements.md:155` FR-013, `:237` `STR-008` · `2c42bbbe` · `contracts/code-review-skill.md:18` C-22, `data-model.md:109` V32, `quickstart.md:86-94`, `research.md:74` | CLOSED — mode selection is two-conditioned (renderer **and** TTY); the rendered literal is pinned; the agent/non-TTY path is the stated default on this host, and scenario D gained the no-TTY case. |
| A-17 | `14a1c6ec` · `requirements.md:162` FR-014, `:184` FR-027, `:200` Key Entities · `2c42bbbe` · `contracts/feedback-and-boundaries.md:24` C-63 | CLOSED — the disambiguation runs both ways: the receipt counts reviewed files; FR-027's prohibition targets compile/test coverage; neither may be cited against the other. |
| A-18 | `14a1c6ec` · `requirements.md:138` FR-008 · `2c42bbbe` · `contracts/status-gate-ownership.md:14` C-48 · `fc007019` · `tasks.md:283` T021 | CLOSED — `/speckit.checklist` is named a *conditional* initiator: after implement it initiates and cites the same owner criterion; before implement it initiates nothing and must not error or manufacture a conclusion. The shipped "applies only when the checklist runs after implement" annotation is preserved because a pin reads it. |
| A-19 | `14a1c6ec` · `requirements.md:139-141` FR-009, `:239` `STR-010`, `:106` · `2c42bbbe` · `contracts/status-gate-ownership.md:20` C-51, `data-model.md:175` V22 | CLOSED — the unattended disposition is halt-and-report with a named refusal literal; a driver/orchestrator confirmation is explicitly **not** a user ruling. |
| A-20 | `14a1c6ec` · `requirements.md:169` FR-018 · `2c42bbbe` · `contracts/feedback-and-boundaries.md:14` C-58 / `:16` C-59, `data-model.md:193` E12 · `fc007019` · `tasks.md:305` T025 · `quickstart.md:150-152` | CLOSED — the census is three, the `(unit_id, run_id)` key is reused unchanged, and the "must not be read as two" caveat is written into both the requirement and the clause. **Residual in `plan.md` only — see N-02.** |
| A-21 | `14a1c6ec` · `requirements.md:151` FR-012 · `2c42bbbe` · `contracts/command-orchestration.md:32` C-13 | CLOSED — the carrier is the existing `## Latest Review` entry, and the clause forbids adding a structured field or a second count copy. No template shape change beyond the state-machine row is required. |
| A-22 | `14a1c6ec` · `requirements.md:147` FR-010, `:238` `STR-009` · `2c42bbbe` · `contracts/command-orchestration.md:30` C-12, `data-model.md:107` V12 / `:182` E11 / `:187` V24, `research.md:121` · `fc007019` · `tasks.md:238` T012 | CLOSED — `YYYYMMDDTHHMMSSZ` UTC at second resolution; a same-second collision waits or exits `2` with a reason and never overwrites an archive; a first run records the pinned `none`. The script's legacy `%Y%m%d-%H%M%S` form is explicitly barred from reuse. |
| A-23 | `14a1c6ec` · `requirements.md:189` FR-028, `:213` SC-006 · `2c42bbbe` · `contracts/tests-and-docs-sync.md:10` C-66, `research.md:206` · `fc007019` · `tasks.md:318` T029 | CLOSED — red-first is a per-group obligation at requirement level with the four recorded fields, and a group that cannot go red is reported as a fast-fail finding instead of counted. |
| A-24 | `14a1c6ec` · `requirements.md:223` SC-006 Source · `fc007019` · `tasks.md:183` T002, `:34` GATE-5 | CLOSED — the baseline instant (implement start), the artifact (`baseline-failed.txt`), the name-level comparison form and the "must not be re-captured elsewhere" rule are all in SC-006's Source row and in T002. |
| A-25 | `14a1c6ec` · `requirements.md:191` FR-028 · `2c42bbbe` · `contracts/tests-and-docs-sync.md:18` C-70, `plan.md:123-142` · `fc007019` · `tasks.md:322` T033 | CLOSED — the criterion is relative ("no NEW drift against a pre-edit measurement"), the per-pair table has one declared owner (`plan.md` § Mirror Obligations), and FR-028 points there instead of restating it. |
| A-26 | `14a1c6ec` · `requirements.md:175` FR-021 · `2c42bbbe` · `contracts/code-review-skill.md:8` C-17, `research.md:127` · `fc007019` · `tasks.md:238` T012 | CLOSED — the non-interactive enumeration is four steps including record creation *and rotation*, with the "must not be read as three" caveat, and the second-run degradation is named as the reason. |

### 2.3 The 4 LOW rows

| ID | closed-by (commit · locus) | Verdict |
|----|---------------------------|---------|
| A-27 | `14a1c6ec` · `requirements.md:230-239` | CLOSED — every `Consumed by` cell now names the six contract files that exist (`command-orchestration`, `code-review-skill`, `coverage-receipt`, `status-gate-ownership`, `feedback-and-boundaries`, `tests-and-docs-sync` — verified present) plus `data-model.md`, `tests`, `docs`. No dead path remains. |
| A-28 | `14a1c6ec` · `.specify/memory/features.md:80`, `.specify/memory/features/071.md:25` | CLOSED — the checklist stage is recorded with its commit `89daf845` on both registry surfaces, status stays `Planned` (that stage produces no transition), and the gap note says it was omitted at the time and backfilled. |
| A-29 | `14a1c6ec` · `requirements.md:150` FR-011 · `2c42bbbe` · `contracts/coverage-receipt.md:36` **C-74**, `contracts/command-orchestration.md:24` C-9, `data-model.md:133` V33 / `:209` E13 · `fc007019` · `tasks.md:262` T018 | CLOSED — the receipt block is the single source of the four counts, both disclosures copy it, and a three-way equality assertion guards it (mirroring C-40's renderer guard). C-74 is claimed on T018, so the clause is accounted, not merely written. |
| A-30 | `14a1c6ec` · `research.md:50` | CLOSED — the built-in-default prohibition now cites FR-004, which is where it lives. |
| A-31 | `14a1c6ec` · `research.md:13` | CLOSED — the count reads 53 and `wc -l templates/commands/review.md` = 53 at this tree. |
| A-32 | `14a1c6ec` · `requirements.md:178` FR-024 · `2c42bbbe` · `contracts/code-review-skill.md:30` C-28 | CLOSED — the mode rule lives once (FR-013) and FR-024/C-28 cite it; the duplicate normative twin is gone. |
| A-33 | `14a1c6ec` · `requirements.md:148` FR-011 | CLOSED — the closed list now carries the base source, matching C-9 and E13. |

**Closure tally**: 33 closed by `14a1c6ec` / `2c42bbbe` / `fc007019` · **0 still-open** · **0 regressed**. The six HIGH rows are each closed by a *decision encoded as one mechanical reading*, not by softened wording: an owner named, a boundary fixed, a state deleted, an exception bounded, a carrier reduced to two.

---

## 3. Cross-artifact consistency re-check (the twelve points this rerun owes)

| # | Point | Result |
|---|-------|--------|
| 1 | **10 Shared Strings** | 10 rows (`STR-001`…`STR-010`), each with a value and a truthful `Consumed by` column; no id outside the range is used anywhere; every id the contracts cite is defined; `renderer: delta`/`renderer: text`, `run`/`pass`/`blocked`, `none`, `blocking-unresolved` are the values the contracts and E9/E10 consume. Consistent. |
| 2 | **C-74** | Defined in `coverage-receipt.md:36`, carried in its traceability table and amendment log, counted in the 15-clause band, claimed by T018, cited by FR-011/SC-001/SC-002/`C-9`/`V33`/`E13`, and mirrored in `plan.md:15/:271`, `feature-ref.md:104`, `tasks.md:8/:19/:35`. One fact, one owner, all references resolve. Consistent. |
| 3 | **Three-value triage** | `run` / `not-applicable` / `not-evaluated` stated identically in FR-003, C-6, E4 `value`, `plan.md:175`, `docs` surface (C-71), quickstart B/C; the fourth state (silent skip) is forbidden in all four. Record existence is tied to the value in FR-010, C-11, V29, quickstart C, T008. Consistent. |
| 4 | **head / trunk** | FR-004 = C-18 = E5/V9/V31 = `research.md:52/:54` = quickstart A. Trunk order closed in all; head fixed at run start in all; the "strict slice needs explicit `--head`" consequence stated in FR-004, C-18, V31, quickstart A, `plan.md` § 2. Consistent. |
| 5 | **`blocking` existence** | FR-008, SC-004, US4, C-46, C-37/C-38, V6/V35, quickstart G, T019/T020/T022/T023 all say presence-over-current-record and none defines clearing. The only surviving "未清除" wording sits in the append-only clarify session row (`requirements.md:262/:264`), which the remediation-session preamble (`:270`) explicitly marks as superseded historical text with "冲突时以本轮为准". Consistent under a declared precedence, not by accident. |
| 6 | **Pin authorization** | FR-027 (one exception, net gain, declaration duty, non-precedential) = C-64 = C-67 = T030 = DoD-4 = `plan.md:233` R-03 = `feature-ref.md:88` = `research.md:115`. `research.md:103-108` quotes the three assertions the change touches. No artifact still reads it as an unqualified permission. Consistent. |
| 7 | **Exit codes** | `0`/`1`/`2` with one meaning each in FR-014, C-34/C-35, E10, quickstart E/G, T015/T017/T018; C-65 (d) pins the same two codes in the test-group obligation. The gate's own `0/1/2` (E10, `plan.md:185`, T017) uses the same alphabet without contradiction. Consistent. |
| 8 | **Skip reasons** | Five values owned by FR-014, cited (never re-listed) by C-36, E7 `reason`, E8, V34, quickstart F, T015; an unrecognised reason is a gap in every one. Consistent — no sixth value and no free-text escape. |
| 9 | **TTY mode** | FR-013 (two conditions, exactly) = C-22 = V32 = quickstart D (both blocks: missing `DELTA_BIN` and present-renderer/no-TTY) = T016/T018/T010. Consistent. |
| 10 | **Three-unit census** | FR-018 = C-58/C-59 = E12 (three `unit_id` values) = `research.md:145-151` = quickstart H = T025/T026/T024/T028 = `plan.md:197` § 6. Consistent across the normative set; one stale digest line in `plan.md` (N-02). |
| 11 | **Red-first** | FR-028 = SC-006 = C-66 = `research.md:206` = T029 = Tests preamble in `tasks.md:12`, all requiring a *recorded failing run per group* with command line, exit code and failing count, and all treating an unfalsifiable green as a finding rather than coverage. Consistent. |
| 12 | **Mirror criterion** | FR-028 (relative criterion, plan owns the table) = C-70 (criterion + pointer) = `plan.md:125-142` (measured 22/136/55 + per-tool copies, "no NEW drift") = T033 = `feature-ref.md:95`. The remediation explicitly did not re-measure the unchanged tree. Consistent. |

**Additional checks beyond the twelve.** (a) `templates/commands/review.md` measures 53 lines, matching `research.md:13`. (b) `templates/commands/checklist.md:36` and `shared/workflow/feature-integration.md:37/:38` are exactly the three transition surfaces the tasks round claims, and the owner row (`feature-details-template.md:71`) is indeed table-shaped with no arrow literal — the round-1 correction was right. (c) The owner row currently lacks the `blocking` condition, so FR-008 is an extension of it, not a restatement — matching `requirements.md:266`. (d) `git-delta-review.sh:22` still hard-codes `GIT_BASE:-main` and `:99-103` still builds `%Y%m%d-%H%M%S` names, so C-20's "the composed path must not rely on the built-in default" and R6's form-conflict are live facts, not stale claims.

---

## 4. Checklist consumption (`checklists/review-composition.md`, 063 F2)

```
unchecked 27 = resolved-by-remediation 26 + covered-by 1 + undispositioned 0
```

- **The 27 FAIL items keep their round-1 dispositions and none regressed.** Each of the 26 finding-mapped items is answered by a closure in §2 (CHK001→A-07, CHK002→A-01, CHK003→A-08, CHK006→A-09, CHK007→A-02, CHK008→A-03, CHK009→A-10, CHK010→A-11, CHK011→A-04, CHK013→A-12, CHK014→A-13, CHK015→A-14, CHK016→A-15, CHK017→A-16, CHK018→A-17, CHK020→A-05, CHK021→A-18, CHK022→A-19, CHK025→A-20, CHK030→A-21, CHK031→A-22, CHK033→A-06, CHK034→A-23, CHK035→A-24, CHK036→A-25, CHK038→A-26); CHK026 stays `covered-by requirements.md § FR-017`, whose text is unchanged by the remediation, so the disposition still stands. The checklist file itself is a dated artifact and was correctly left unedited by a read-only stage; its unchecked boxes are now "answered", not "ignored".
- **The 13 PASS items survive the remediation on their subject.** The only wording that went stale is CHK024's evidence clause "disclosed in three named places (C-52)": C-52 now names two carriers because the third was demoted (A-01). The item's subject — "is each fact's disclosure place fixed?" — is *more* precisely fixed than before, so PASS holds and only the parenthetical is superseded. No PASS item's subject was weakened.
- **New, previously undispositioned items — reported, not absorbed.** The remediation introduced four checkable gaps the checklist has no item for (§5, N-01…N-04). Each is raised as a finding here, which is what keeps the identity's third term at zero.

---

## 5. New findings from this rerun (N-01…N-04)

| ID | Class | propagation_surface | Severity | Location(s) | Claim | Recommendation |
|----|-------|---------------------|----------|-------------|-------|----------------|
| N-01 | C underspecification | `test_coverage_receipt.py` (T014), `data-model.md` E9 | **MEDIUM** | `requirements.md:156` FR-014; `contracts/coverage-receipt.md:22` C-38 / `:20` C-37; `data-model.md:153-159` (E9 table); `tasks.md:255` T014 | FR-014 fixes the segment verdict only for `skipped_files > 0` ("`blocked` if the current record has `blocking`, else `not-evaluated`") and for the gap case says only "MUST NOT be `pass`". Two readings therefore survive a `gap_files > 0` run: `blocked` (a gap is a failed review) or `not-evaluated` (a gap is no conclusion). E9's derivation table fixes the second — including when `blocking` entries are present — and T014 pins the derivation, so a test-consumed verdict value rests on a data-model table with no requirement row authorizing it. Same shape as the closed A-11/A-12 rows, one layer lower. | Add one sentence to FR-014 closing the gap case ("`gap_files > 0` ⇒ `not-evaluated` regardless of `blocking` presence, a gap being no conclusion"), or state explicitly that E9 owns that mapping. |
| N-02 | F inconsistency | `plan.md` § Phase 0 digest; `plan.md` R-06 title | LOW | `plan.md:160` ("**Two feedback units, one key** — both units are already probe-registered …") and `plan.md:236` (risk title "Two feedback units collide"); correct owners: `plan.md:197` § 6, `research.md:145-151` R9, `contracts/feedback-and-boundaries.md:14` C-58, `data-model.md:193` E12 | The remediation changed R9 and § 6 to *three* units and left the Phase 0 digest line (and a risk title) saying "two … both units". A reader of the digest takes away the retired census. A-20's own defect class, surviving in a digest rather than in the normative text. | Reword `plan.md:160` to "three feedback units, one key" and retitle R-06 to match; no substantive change. |
| N-03 | F inconsistency | `plan.md` § 3 / `research.md` R7 vs `tasks.md` T011 | LOW | `plan.md:179-185` (five script surfaces: `base`, `start`, `note`, `receipt`, `report --file`); `research.md:127-135` (four-step enumeration); `tasks.md:237` T011 ("Add the `base` and **`triage`** subcommands") | The tasks round materialized the code-path predicate as a **sixth** script surface (`triage`), which C-30 permits ("a subcommand or option of the skill's existing script entity") but neither `plan.md` § 3 nor `research.md` R7 enumerates. An implementer working from `plan.md` would build five surfaces and miss one the tests exercise; the tasks row is the operative instruction, so the risk is containment, not contradiction. | Add a `triage` bullet to `plan.md` § 3 (and name it in R7's enumeration), or drop the subcommand name from T011 and express it as a `--code-paths`-bearing option of `base`. Either way one artifact owns the list. |
| N-04 | F inconsistency | `tasks.md` task rows (all 36) | LOW | `requirements.md:241` citation convention ("下游契约、任务与测试引用上表字面量时 MUST 写 `[[STR-NNN]]`，MUST NOT 复制粘贴字面量"); `tasks.md` contains **zero** `[[STR-NNN]]` citations and copies the literals — `not-applicable` ×12, `not-evaluated` ×11, `blocking-unresolved` ×2, `code-review.md` ×1, plus bare `run`/`pass`/`blocked`/`none` | The convention is a MUST addressed to contracts, tasks and tests. Contracts and data-model honour it (`[[STR-NNN]]` throughout); `tasks.md` does not, so the convention's own reach is unmet by one of its three named consumers. Carried over from before the remediation (round 1 did not flag it) rather than introduced by it. Note also that the "tests" limb is unsatisfiable as written — a Python test cannot write a markdown citation; only the *reading* of the table is possible there. | Either cite ids in task rows where the literal is a decision (leaving concrete file names as prose), or narrow the convention to "contracts and data-model cite by id; tasks and tests must read the value from the owner and never restate it as a new definition" — the current wording over-reaches in one direction and is unmet in the other. |

**Not raised, deliberately** (named so a later reader does not relitigate): (a) the append-only clarify rows still carry "未清除" and "收尾摘要…同时披露" — superseded by a written precedence clause, i.e. a legitimate dated record; (b) `checklists/requirements.md:34` still records "230 lines … 4 shared strings" — a stamped run record of that stage, correctly not rewritten (single-run evidence discipline); (c) `checklists/review-composition.md:271` still claims "STR-001/002/003/004" and "C-1…C-73" — the same dated-snapshot reason; (d) the gate subcommand's `0/1/2` is not named in an FR — E10, `plan.md:185` and T017 agree on one alphabet and no competing reading changes a reported verdict, so this stays an observation rather than a finding.

---

## 6. Constitution alignment (v1.13.0, 16 principles)

No CRITICAL conflict, and no MUST violation found in the repaired set. Three rows were re-examined because the remediation moved what they rest on:

- **XIV (One Source of Truth)** — strengthened: the four counts have one declared source with an equality assertion (C-74/V33), the code-path predicate has one owner (C-7/C-30), skip reasons and forbidden phrases are cited from their requirement rows instead of re-listed, and the cross-reference columns now point at files that exist (A-27 closed). The three surviving duplicates are all legitimate: the machine-regenerated projections (DR1's two renderer forms with an equality test), the pins that detect drift (the frozen clause baseline), and the dated session rows under a written precedence clause.
- **XVI (Fast Fail)** — exercised rather than claimed: every amended clause names its finding id in its contract's amendment log, the three measured premises the tasks round corrected are stated as corrections, and the one place where intent had to be chosen (head carries no source tier) is recorded as a decision with its cost (V31, `research.md:54`).
- **VIII (Code as Single Source of Truth)** — re-measured here, not trusted: 53 lines for `review.md`, `GIT_BASE:-main` at `:22`, the dash-form timestamp at `:99-103`, the presence-based `blocking` count at `:442-446`, and the two disagreeing transition rows are all still true at this tree.

Principle IV (Test-First) — six groups, per-group red-first, one bounded pin change, no assertion deleted. Principle IX (Framework Scope Discipline) — the remediation added specification text only; T035 sweeps the delivery surface.

---

## 7. Metrics

| Metric | First run | This rerun |
|--------|-----------|------------|
| Findings (new, this pass) | 32 | **4** (N-01…N-04) |
| Findings still-open from the prior pass | — | **0 of 33** |
| Severity this pass | CRITICAL 0 · HIGH 6 · MEDIUM 22 · LOW 4 | CRITICAL 0 · HIGH 0 · MEDIUM 1 · LOW 3 |
| Clause coverage | 73/73 claimed, status ok | **74/74** claimed, status ok, exit 0 |
| Baseline delta | 0 beyond frozen baseline | **0** beyond the frozen baseline (baseline not re-frozen) |
| FR coverage | 28/28 | **28/28** |
| Shared Strings | 4 | **10**, all consumers resolve |
| Task rows | 36 | 36 (new obligations absorbed into existing rows) |
| Plan-owned diff since plan commit | 0 | **0** |
| Checklist consumption | 27 = 26 + 1 + 0 | 27 = 26 + 1 + 0, no regression |
| Validation wave | 6 sent / 6 confirmed / 0 downgraded (direct re-read) | 33 re-read / 0 still-open / 0 regressed (direct re-read; downgrade rate unreportable, non-delegated) |

---

## 8. Gate

```
GATE: CRITICAL=0 HIGH=0
```

**Disposition.** All six HIGH findings of the first pass are closed at their cited loci and each closure is a single mechanical reading, not a softened sentence; the 27 remaining findings are closed with 0 still-open; the deterministic lanes are green (`status: ok`, 74/74 claimed, FR 28/28, 0 beyond the frozen baseline) and the plan-owned artifacts show zero diff since the plan commit. **The analyze gate passes; no `upstream-repair-required` row remains.**

The four new findings are carried forward as **non-blocking**: N-01 (MEDIUM) is a requirement-layer omission of one verdict mapping that E9 already fixes consistently — worth one sentence at the next requirements touch, not a gate failure; N-02 and N-03 are stale/unenumerated lines inside `plan.md` that no test consumes; N-04 is a citation-convention reach problem in `tasks.md`. None of them makes a downstream artifact say two things that cannot both be implemented, which is the bar the HIGH rows failed at.

**Next stage** may proceed. If the implement stage is asked to touch FR-014, `plan.md` § 3 or the Phase 0 digest, the three documentation findings are one-line repairs; N-01 needs a requirements edit and should not be silently decided inside a contract test.
