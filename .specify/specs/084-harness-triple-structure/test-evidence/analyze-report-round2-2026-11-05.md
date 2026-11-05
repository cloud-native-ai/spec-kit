# Analyze Report — Round 2 — 084 Harness 三重结构（markdown + yaml + script）

**Round**: 2 (rerun after the round-1 remediation; **final** gate — the one-round loop budget is spent after this run)
**Date**: 2026-11-05 | **Stage**: analyze | **Base commit**: `2b18485e` (tasks repair) | **Branch**: `084-harness-triple-structure`
**Prior report**: `test-evidence/analyze-report-2026-11-05.md` (round 1: 1 CRITICAL / 2 HIGH / 10 MEDIUM / 4 LOW)
**Artifacts judged**: `requirements.md` · `plan.md` · `data-model.md` · `contracts/`×5 · `quickstart.md` · `research.md` · `feature-ref.md` · `tasks.md` · `checklists/*.md` · `.specify/memory/features.md` · `.specify/memory/features/084.md` · `.specify/memory/constitution.md`
**Read-only**: no artifact was modified, no commit was made, nothing was pushed. The write surface is this report, `test-evidence/analyze-round2-targeted-set.txt`, `test-evidence/analyze-round2-targeted-run.txt`, the E3 row appended to `test-evidence/stage-status.md`, and the wrap-up engine records. `git status --porcelain` read 22 lines before the validation wave and 22 lines after it; the single pre-existing dirty path (`.specify/memory/session/…-081a.md`) is unchanged.

## Verdict

**Gate NOT GREEN. `CRITICAL = 0`, `HIGH = 2`.** The round-1 CRITICAL and both round-1 HIGH findings are closed with evidence (below), but the re-adjudication finds two HIGH defects that were not in the round-1 table — one of them **introduced by the remediation itself** — plus one re-tiered residue and one LOW.

- **HIGH**: 2 — `R2-01` (a 084 artifact turns an existing contract test red, and the implement-stage baseline will absorb it), `R2-02` (the plan's migration roster puts eight `none`-engine-side facts in scope, contradicting the requirement that owns scope, while `tasks.md` T015 instructs the opposite).
- **MEDIUM**: 1 — `R2-03` (the `tasks.md` banner's stated reason for not using `[green:]` was falsified by the plan repair; it is F-02's unsynced tasks-side prose, re-tiered on its current propagation surface).
- **LOW**: 1 — `R2-04` (a `DM`→`DN` typo inside commit `2b18485e`'s message body; the files are correct).
- Round-1 residue: **16 of 17 closed** with re-measured evidence; **1 carried** (`F-02`, contract side closed, tasks-side prose open → `R2-03`).

**Both HIGH rows were confirmed by independent read-only validators** (2 dispatched, 2 `confirm`, 0 `downgrade`, 0 `reject`; § Validation wave carries both evidence boundaries verbatim). **The loop budget is exhausted: this run does not repair anything and does not reopen a stage. Hand up — see § Next actions.**

Headline separation (round 1 vs round 2 are different claims): the round-1 backlog is cleared except one prose residue, so the *artifact shape* is sound; what remains is **one factual contradiction inside the migration scope** and **one regression this feature's own repair put into an existing test**. Neither is a style matter; both land on `/speckit.implement`'s acceptance path.

## Rerun delta

### Resolved since last run (each with the evidence that closes it)

| Round-1 ID | Was | Closed by | Evidence re-measured this round |
|---|---|---|---|
| F-01 | CRITICAL | `fd84ed63` | `requirements.md:147` (FR-010) is now the **single** owner enumeration and splits the set into two roles: "不得重判侧（六脚本）" (incl. `doc-consistency-check.py`) and "零 diff 侧（五脚本）" (the same six minus `doc-consistency-check.py`), with an explicit statement that this is a superset of plan `C-032`'s five and not a second list. `FR-019` (`:156`), `N5` (`:207`), `SC-006` (`:220`) and `SC-006 Source` (`:229`) each say "枚举见 FR-010，本行不复述" and carry no member list. Count words are consistent with the two roles (六 / 五 wherever each applies). |
| F-02 (contract side) | HIGH | `9284c789` | `clause_extract.py` over the five contracts: `declaration-schema` 12, `distribution-and-mirror` 13, `harness-triple-check` 16, `migration-batches` 10, `shared-reader` 8 — **all five `form=md-bold-closed`, 59 clauses total**; zero `DS-/HC-/SR-/MB-/DM-<dd>` occurrences in any normative file. |
| F-03 | HIGH | `fd84ed63` | `FR-009` (`:146`), `SC-005` (`:219`), `SC-006` (`:220`) each name the referent ("基线 = T001 采集进 `notes/pre-change-measurements.md` 的该条读数", with plan `EP-003`'s `git diff --stat 171c2ff8` as the plan-side precedent) and state that the criterion compares against that capture rather than re-deriving a baseline; `SC-005 Source` (`:228`) and `SC-006 Source` (`:229`) repeat the referent. |
| F-04 | LOW | `fd84ed63` | `FR-007 (b)` (`:144`) pins the invocation verbatim (`--action verify --faces duplicate --spec-dir <spec 目录>`), states the face has no per-fact selector, and moves fact attribution to the reason text `duplicated-fact-literal: <fact>@<path>` plus `lookup --fact`; `SC-002` (`:216`) cites the same reason-borne attribution. |
| F-05 | MEDIUM | `2b18485e` | `FR-023` occurs 0 times in `requirements.md`, `tasks.md` and `checklists/layer-criteria-2026-11-05.md`; T001 now carries `FR-011, FR-018` in both the row tag and the Traceability cell. |
| F-06 | MEDIUM | `fd84ed63` | `requirements.md:252` now states the real partition: five templates with one placeholder, `STR-011` with two, none without (5 + 1 = 6), matching the value table row by row. |
| F-07 | MEDIUM | `9284c789` | `plan.md:375-386` (D10) names the five frozen scripts verbatim and records three derived readings with provenance — **38** (SC-006's five), **35** (the analyze-time five-name set), **39** (the six-name union that the pre-repair plan had inherited); the commands and file lists are in `test-evidence/f07-test-file-readings.txt` § A/B/C. |
| F-08 | MEDIUM | `fd84ed63` | `requirements.md:162` (§ Key Entities, Exclusion Record) drops `reason` from the attribute list and states it is filename-borne. |
| F-09 | LOW | `2b18485e` | T005 and T006 both carry `FR-008` in their own tag list. |
| C-01 | MEDIUM | `9284c789` | `migration-batches.contract.md` C-044/C-045 now carry an `engine side (constant or read point today)` column for every row, `none` rows included, each `none` carrying its measurement. |
| C-02 | MEDIUM | `fd84ed63` | `FR-018` (`:155`) replaces "至少" with a closing rule: C-042/C-044/C-045 carriers ∪ every in-scope fact's markdown carriers; the five named rows are explicitly "举例，不是第二份枚举". |
| C-03 | MEDIUM | `fd84ed63` | `FR-013` (`:150`) rules the exit-2 degradation label free-text and mechanically judged on three items only (exit 2, non-empty label naming the missing directory, no traceback), and says it is neither a Shared String nor a seventh reason. |
| C-04 | MEDIUM | `fd84ed63` | `FR-005` (`:142`) states `consumers` MUST contain at least one engine and that a carrier-only declaration is a schema error, not a permanent `pending`. |
| C-05 | MEDIUM | `fd84ed63` | `FR-019` (`:156`) adds the single-subset-parser guard leg (C-058 in the requirement layer, allowlist = N4's two grandfathered parsers, assertion is a search). |
| C-06 | LOW | `fd84ed63` | `FR-016` (`:153`) scopes determinism to all three actions and says SC-001 (i) is only the `coverage` instance. |
| E-01 | MEDIUM | `2b18485e` | `coverage-baseline.txt` exists: 515 lines = 2 header + **513 names**, `base-sha: 9284c789e154`, `files: 248 (parsed 145 + named 103)`; re-freeze is byte-identical (`test-evidence/coverage-baseline-freeze.txt`), and the accountant's status moved `baseline-missing` (exit 2) → `uncovered` (exit 1, a verdict). |
| G-01 | LOW | `2b18485e` | `features/084.md` § Latest Review now carries dated tasks / checklist / analyze-loop records; § Related Files registers `checklists/layer-criteria-2026-11-05.md`; the dangling `§ MB-01` points at `C-042`; `features.md` reads `Total Features: 77` over 77 rows and the 084 row's clause phrase is `C-001…C-059`. |

### New since last run (including what the remediation itself introduced)

| ID | Severity | Why it is new |
|---|---|---|
| `R2-01` | **HIGH** | Introduced **by** the remediation commit `2b18485e`: the dated checklist record it appended to `.specify/memory/features/084.md` (line 31) contains `flow_class: execution`, and that single line is now the only offender in an existing contract test. |
| `R2-02` | **HIGH** | Not in the round-1 table: round 1 disposed C-01 as "engine-side precision" and never adjudicated the roster's **membership**. Completing C-01's column with `none` made the membership question mechanical: eight rows have no engine-side copy today and are nonetheless in scope. |
| `R2-03` | MEDIUM | `F-02`'s tasks-side prose. Round 1 measured F-02 against the contracts; the plan repair fixed the contracts and the tasks-side banner that explains the `[green:]` non-use was not synced with it. |

### Carried over

None unchanged. `F-02`'s contract half is closed; its tasks half is re-tiered and carried as `R2-03` (re-tiering rationale in that row).

## Metrics

| Metric | Value | Source |
|---|---|---|
| Total requirements | 19 FR + 6 SC + 14 STR | `requirements.md` (282 lines, 25 definition rows — `validate-requirements.py`) |
| Tasks | 31 (Setup 2 / Foundational 5 / US1 3 / US2 7 / US3 2 / US4 4 / Polish 8) | `tasks.md`, phase headings counted mechanically |
| FR → task coverage | 19/19 (100%) | re-derived programmatically this run: every `FR-0NN` appears in at least one task row |
| Task → FR/SC mapping | 31/31 rows carry at least one FR or SC; `§ Traceability` has 31 rows keyed to the same 31 ids | same run |
| Contract clauses parseable | 59 of 59 across 5 files, `md-bold-closed` | `clause_extract.py` |
| Contract clauses claimed by the tasks file | 0 of 59 | `account-clause-coverage.py` |
| FRs cited from contract citation groups | 0 of 19 | same run (cause analysis: § Coverage summary) |
| Coverage accountant status | `uncovered` (exit 1; 572 uncovered, 59 beyond the frozen baseline of 513 names, 103 named-unparseable files) | same run |
| Feature linkage | 100% (index row 084 = detail file; `Total Features: 77` = 77 rows) | `features.md`, `features/084.md` |
| Finding classes | inconsistency 2 · underspecification 1 · coverage 0 · feature linkage 0 · duplication 0 | findings table |
| CRITICAL / HIGH / MEDIUM / LOW | 0 / 2 / 1 / 1 | findings table |
| Round-1 residue | 16 closed / 1 carried / 0 rejected | § Residue list |
| Validators dispatched / confirm / downgrade / reject | 2 / 2 / 0 / 0 (downgrade rate 0%) | § Validation wave |
| Checklist `[Gap]` accountability | 10 unchecked = 6 raised + 4 dispositioned; residue 0 | § Checklist accountability |
| Targeted test set (E3) | 16 contract/integration files, 3 failed / 295 passed, 19.18 s, rc 1 | `test-evidence/analyze-round2-targeted-run.txt` |

## Findings

`propagation_surface` = the downstream artifact that inherits the finding; severity is read from that field. `none` rows are capped at MEDIUM.

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| R2-01 | Inconsistency (regression introduced by the round-1 remediation) | implement-start baseline (E2 slot) → closure "zero new failures" reading | **HIGH** | `.specify/memory/features/084.md:31`; `tests/contract/test_expression_compatibility.py:247-254,730-752`; commit `2b18485e` | `2b18485e` appended a dated checklist record containing `flow_class: execution`. The existing contract test `test_c2_no_project_side_classification_store` (clause C-2 of the expression-compatibility contract: classification data MUST NOT be stored project-side; the flow-class ledger is the owner) scans `.specify/memory/**` and matches exactly that literal. Measured: the targeted run of 2026-11-05 exits 1 with this test failing and **exactly one offender** — `features/084.md:31`. The pattern is absent from `.specify/memory/` at trunk `3ffeb26e` (where the file does not exist), and `git log -S` attributes the line to `2b18485e` alone. | **Feature-owned, one-line repair**: reword line 31 so the record states the reading without the `flow_class: <value>` assignment token (e.g. "类别读取：`execution`，读数在 `test-evidence/flow-class-lookup-checklist.txt`，取值由 flow-class 台账拥有"). This is not a plan-owned artifact; it is the feature detail file, so no PLAN-EDIT is implied. Until it lands, the regression exists in the tree and would be normalised as baseline by the implement-stage capture. |
| R2-02 | Inconsistency (scope criterion vs roster membership) | `tasks.md` T014/T015/T016 → implement → `DoD-5`, `SC-002` closure | **HIGH** | `contracts/migration-batches.contract.md` C-044 table rows `analyze-severity-values`, analysis finding-channel set, `review-segment-sequence`, `self-improvement-stage-sequence`, track-to-executor mapping, `improvement-track-values`, changed-asset-category mapping; C-045 row `history-categories`; `requirements.md` FR-006 (i), FR-011, § Initial Scope Adjudication; `tasks.md` T015 | Eight roster rows have `engine side = none` today and C-044 nonetheless keeps them in scope, prescribing "step 3 of `C-047` creates the read point". FR-006 — the requirement that owns scope — defines the criterion as machine consumption ∧ cross-face and rules that when either conjunct fails the fact **stays where it is**; its A2 narrowing (in FR-006's own closing sentence and in `## Clarifications`) reduces (i) to "there exists a deterministic engine whose judgement changes with the value", explicitly so that consumerless label sets do not enter the declaration layer. FR-011 defines batch 2 as gate-consumed mappings. `tasks.md` T015, the row that would perform the batch-2 migration, instead closes with "a carrier whose mapping is prose-only and consumed by nothing stays where it is and is recorded as out of scope by the FR-006 (ii) test". An implementer therefore cannot satisfy FR-006 (i), C-044's roster and T015's sentence at once; and the requirements' own scope table asserts an engine-side second copy for four of these units ("分析侧 owner 与判定引擎各一份" / "`review-template.md` 与审查引擎各一份" / "工作流散文与改进技能族各一份"), which the plan's `none` measurements contradict. | **Decision required upstream, not repairable in analyze.** Two readings exist and only an owner can pick: (a) requirements is authoritative because it owns scope → the eight rows are out of today's in-scope set and the roster must drop or re-mark them (**substantive plan change, PLAN CONSTRAINT → deliberate reopen**), or (b) "the read point is created during migration" is the intended reading → then FR-006 (i) must be restated to a post-migration criterion and T015's closing sentence must be replaced (**requirements change**). Either way T015's sentence must be brought into line. Analyze cannot choose between two live readings; this is the halt point. |
| R2-03 | Inconsistency (stale premise) | `tasks.md` banner → implement reading of the coverage lane | MEDIUM | `tasks.md:11` (banner), `tasks.md:204` (§ Traceability preamble pointing at the banner) | The banner states the `[green:]` tag is unusable because "the five contract documents name their clauses `DS-nn` / `HC-nn` / `SR-nn` / `MB-nn` / `DM-nn`" and "`clause_extract.py` classifies all five as `md-none`". Those clauses are now `C-001…C-059` and all five parse as `md-bold-closed` (measured above), so the recorded reason is false; § Traceability repeats the pointer ("the measured reason the `[green:]` tag is unusable … is in the banner"). Re-tiered from F-02 (HIGH) on its present surface: the contracts themselves resolve, so no clause is un-resolvable and no acceptance criterion depends on the lane. | **tasks-owned**, and it is a choice: (a) restate the banner's reason honestly ("the tag is optional per `.specify/templates/tasks-template.md:110`; the clause partition is stated in § Traceability") — a two-location text repair, or (b) claim the 59 clauses with `[green:]` tags — a 59-claim addition that also turns the accountant's clause lane green. Whichever is chosen, the banner and § Traceability must agree. |
| R2-04 | Inconsistency (cosmetic, history) | `none` | LOW | commit `2b18485e` message body | The message body writes `59 条款 DS·HC·SR·MB·DN` where the fifth family is `DM`. The *file* edits in the same commit are correct (`features.md` reads `C-001…C-059`; no `DN` anywhere in the tree). | **No repair.** History is immutable and no artifact carries the typo; recorded so a later reader does not treat the message as a reading. |

## The four adjudications the dispatch asked for

### 1. Coverage lane — `status=uncovered`, 59 beyond baseline, 0/19 FRs → **not blocking**, but the dispatch's stated cause is incomplete

Two independent causes, and conflating them was round 1's error as well:

- **`59 uncovered beyond the frozen baseline`** — the fifty-nine are this feature's own `C-001…C-059`, which no row claims, because `tasks.md` emits no `[green: <contract>#<clause>]` claim. The tag is **optional by its owner** (`.specify/templates/tasks-template.md:110`: "(optional, repeatable) … a row declaring none keeps exactly the plain form"); `validate-tasks.py` only judges claims that are made; no gate anywhere requires the lane to be green (the accountant is consumed by `create-tasks` for the freeze and by `analyze` for a reading — `grep` over `.specify/`, `scripts/`, `skills/`, `templates/` finds no third consumer). **Verdict: an optional-label reading, not a defect.**
- **`0 of 19 FRs cited from citation groups`** — the FR lane is derived from each contract clause's *last parenthetical containing an FR/SC id* (`clause_extract.clause_citations` per the syntax owner § 4.2). The five 084 contracts carry **no** such citation group; § 4.2 defines where a citation sits, it does not require one. So the lane reads zero **even though all 59 clauses now parse** — the round-1 attribution of 0/19 to F-02 is no longer the operative cause.

**Therefore: not blocking.** The feature's FR→task coverage is complete and is re-derived mechanically in this run (19/19 FRs named; 31/31 rows carry an FR or SC; 31 traceability rows keyed to the same ids), and `§ Traceability` is the declared single statement of the clause partition. Consequence to state plainly: **the clause lane cannot go green for this feature while the tag is unused** — and it will stay red at implement and closure. If the orchestrator wants it green, the minimal repair is R2-03's option (b), which is **tasks-owned** and simultaneous with the banner repair.

### 2. The eight `none`-engine-side rows — **not "a migration-phase read point" as the artifacts assert; they are outside FR-006 (i) today, and the artifacts disagree about that** → adjudicated as **R2-02, HIGH**

Adjudication: (i) is evaluated on **today's tree** — FR-006's own disposition clause ("任一不成立即留在原处") plus A2's narrowing ("存在一个确定性引擎，其判决结果随该取值改变而改变") leave no other reading; a post-migration reading would make the criterion vacuous (the migration would manufacture its own justification), which is precisely the mechanism A2 removed. On a today's-tree reading the eight rows fail (i) (verified by measurement: no engine carries the analyze severity scale, the finding-channel set, the review or self-improvement stage sequences, the track-to-executor or changed-asset-category mappings, or the history categories). Four of them also fail (ii) — their carriers are all `markdown 载体`, one face.

Effect on FR-006 (i): **the criterion stands; it is the roster and T015 that must move.** Note the two readings are not symmetric: reading (a) keeps the requirement intact and needs a **substantive plan edit** under the active PLAN CONSTRAINT, reading (b) needs a **requirements semantic edit**. Both are upstream of analyze, so this run halts rather than picking one (§ Fast-fail).

### 3. `pre-analyze-check.py` `CLAUSE_DEF` prefix gap → **not blocking for this feature; a framework observation**

`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:41` compiles `^- \*\*([A-Z]{2,4}-\d{2})\b` — 2–4 letters plus **exactly two** digits. The canonical clause id is `C-<digits>` (one letter), so `C-001` is invisible; `summary.clauses` reads `0` for all three stages, while the syntax owner's own extractor reads 59. This is repo-wide, not 084-specific: `077-doc-sdd-integration`, `079-bilingual-expression` and this feature all use the `**C-001**` form, and applying the owner regex to their contract files matches **0 lines in each** (6 / 4 / 5 files respectively) — so the count is zero for all three by construction, not by any property of 084's contracts. The gate's `decision` is nevertheless `pass` on `requirements`/`plan`/`tasks` because no error class depends on that count. **Verdict: framework observation, non-blocking for 084**; the repair belongs to the host script's id pattern (and to whoever owns the `clause_extract` ↔ host coupling), not to this feature.

### 4. Commit message `DM` → `DN` in `2b18485e` → **not blocking**

The message body is the only place the typo exists; `features.md` and `features/084.md` carry the correct `C-001…C-059`. No artifact needs correction, and rewriting history to fix a message is not a repair a feature may perform. Recorded as `R2-04` (LOW) so it is not later mistaken for a reading.

## Validation wave

Dispatched under the read-only carrier of `external-dispatch-recipes.md` § Recipe 7 — external CLI `qodercli`, one process per finding, both in parallel, write tools excluded (`--tools Read Grep Glob Bash`), `--no-session-persistence`, briefs carrying only id / category / claim / severity / evidence locations (§ `.specify/.tmp/084-analyze-r2/brief-R2-0{1,2}.md`, a scratch root matched by `.specify/.gitignore`, torn down after this run).

| Finding | Severity sent | Verdict | Resulting severity |
|---|---|---|---|
| R2-01 | HIGH | `confirm` | HIGH |
| R2-02 | HIGH | `confirm` | HIGH |

**Downgrade rate: 0/2.** Detection was not over-rated this round.

**Evidence boundaries (validator, verbatim where load-bearing)**

- **R2-01** `EVIDENCE_SUPPORTED`: "Full HEAD suite: `25 failed, 7151 passed, 4 skipped … 1046.46s`. The failed-id list … includes `tests/contract/test_expression_compatibility.py::test_c2_no_project_side_classification_store`. … at HEAD the suite is already red on 25 ids, and the GATE-2 baseline … will absorb all of them, including C-2. The 'zero new failures' closure reading is therefore blind to this regression by construction, not only in theory. The other 24 failures are environment-caused … `test_e_a_stale_pin…` (git-version pin mismatch), `test_c22_watch_target_hook_selftest` (`/home/agent/tmp/spec-kit` permission denied), `tests/unit/test_loop_state_engine.py` (9 failures, reproducible in isolation) … None of these read `.specify/memory/`." · `EVIDENCE_NOT_SUPPORTED`: "The 25-failure count is not a clean baseline usable to *reject* 'zero new failures' for the whole feature. It mixes environment failures with this artifact-caused one, so the finding's causal claim rests on the targeted single-test run (exactly one offender, `features/084.md:31`) and the attribution in `git log -L31,31`, not on the full-suite count. … still unobserved: the failure executed as red *at trunk* (no trunk worktree, inferred from the identical regex plus the empty grep), and the implement-stage capture/closure commands executed end-to-end."
- **R2-02** `EVIDENCE_SUPPORTED`: "FR-006 (`requirements.md:143`) defines the criterion as a conjunction of (i) and (ii), and states '任一不成立即留在原处'. … The Clarifications answer (`requirements.md:275`) says the same. FR-011 (`requirements.md:148`) defines batch 2 as '被门禁消费的映射与有序算子表'. … `migration-batches.contract.md:41-45` (C-044) reads each engine side 'as they stand today' and states that `none` means the row has no engine-side copy today, so step 3 of C-047 (`:81`) creates the read point. … `tasks.md:113` (T015) says a prose-only, unconsumed mapping 'stays where it is and is recorded as out of scope by the FR-006 (ii) test rather than migrated for symmetry'. That test is FR-006 (ii), but FR-006 (i) is the one that fails, and the route named is exclusions, not 'creates the read point'. … T015's traceability entry (`tasks.md:222`) binds the row to FR-006(i), and the row itself is tagged FR-006(i)." · `EVIDENCE_NOT_SUPPORTED`: "The claim omits a resolution the cited artifacts already contain. C-044 and C-047 step 3 are explicitly written relative to today's tree, and step 3 creates the read point during migration. C-048(c) checks `(c)` on the migrated tree. So the criterion can be satisfied … The claim overstates the 'initial scope' contradiction. Those table rows declare that a second copy exists today, which is a reading the plan disputes, not a statement of requirement. … The real independent defect is in T015, not the roster. … I could not observe whether T015's sentence applies to any specific roster row, or whether those mappings' carrier prose counts as a second face. … C-044's Verification section says its readings must be re-measured at implement time, so whether a second copy exists for the analyze, review, self-improvement and improve mappings is unconfirmed."

Both boundaries are adopted: R2-02's row keeps the validator's own hedge (the roster's `none` readings are the plan's measurement and are re-measurable at implement; the *conflict* — three artifacts giving three instructions — is what blocks, not the accuracy of the `none` cells).

**Read-only proof**: `git status --porcelain` read 22 lines before the wave and 22 lines after it; the only modified path in both readings is the pre-existing `.specify/memory/session/…-081a.md` from the clarify run. One validator reported that a full-suite attempt of its own left a `create-pages` test process behind; a re-check after the wave found no surviving `scaffold-hugo.py` or docker process. The wave wrote nothing into the judged tree.

## Coverage summary

| Lane | Reading | Verdict |
|---|---|---|
| FR → task | 19/19 FRs named by at least one of the 31 rows; 31/31 rows carry an FR or SC (re-derived programmatically this run) | **covered** |
| Single-row FRs (re-read one by one, per the zero-finding floor) | 5 rows now rest on a single task: FR-001→T004, FR-003→T003, FR-011→T001, FR-012→T009, FR-014→T003 (round 1 had four; FR-011 joined when T001's dangling `FR-023` became `FR-011, FR-018`). Each re-read: T001 captures the comparison values everything later compares against (a substantive, evidenced duty), T003 authors `contract.yaml` (the value-domain owner), T004 writes the owner document and its chapter tree, T009 deletes `DEFAULT_THRESHOLD` and routes the read through the shared entry, T012 migrates the five flow-class sets. All five are correct attributions | covered |
| Task → requirement | every row's tag list and Traceability cell resolve to defined FR/SC ids; the table is keyed to the same 31 ids (`set(traceability ids) == set(task ids)`) | covered |
| Clause → task (`[green:]`) | 0 claimed of 59. Tag optional by template owner; **the file's own recorded reason for that is stale** → `R2-03` | unmeasurable, non-blocking (§ Adjudication 1) |
| FR cited from clause citation groups | 0/19 — the contracts carry no citation group; § 4.2 does not require one | not a defect; FR coverage read from § Traceability instead |
| Baseline | frozen: 513 names / 248 corpus files / `base-sha 9284c789`; accountant now exits 1 with a verdict instead of 2 with an input error | **resolved** (E-01 closed) |
| Whole-corpus context | 253 files scanned; 1576 distinct clause names over 150 parsed files; 572 uncovered repo-wide, of which 513 are baseline-internal and do not block | informational |

## Feature linkage summary

| Check | Reading |
|---|---|
| Index row bound to this spec | `features.md:90` → `084`, status `Planned`, spec path to `requirements.md` |
| Detail file agrees on status | `features/084.md` `**Status**: Planned`; the state machine owns no transition before implement, so the status is lawfully held |
| Stage record | tasks / checklist / analyze-loop records present with dates; `checklists/layer-criteria-2026-11-05.md` in § Related Files; `§ MB-01` → `C-042` (G-01 closed) |
| Header/rows consistency | `Total Features: 77`, 77 matching rows |
| Feature identity in the spec | `requirements.md` § Related Feature: ID 084 and the name match the index |
| 084 row content | clause phrase reads `C-001…C-059`; no old id family, no `DN` |
| 081 frozen surface | `git diff --stat 3ffeb26e -- shared/workflow/acceptance-hardening.md .specify/shared/workflow/acceptance-hardening.md tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py` → **empty** (zero diff on this branch) |

## Constitution alignment

- `plan.md` § Constitution Check renders 18 rows in document order; re-read against `constitution.md` v1.15.0 in this run: **18/18 names identical, 0 missing, 0 mismatched**.
- § XIV (One Source of Truth): F-01's four-voice enumeration is repaired to one owner + references. `R2-01` is *not* a § XIV violation in substance — a dated record is one of the three legitimate duplicate kinds — but it is a live conflict with a **pinned contract test** (069 C-2) that cannot distinguish a dated record from an assignment, so it is a test-level regression, not a principle breach. Reported HIGH, not CRITICAL, for that reason; the constitution carve-out was not needed.
- § II (Feature Index as single source of truth) and § XVII (directory governance) hold: no new top-level directory is proposed, and registration of `shared/declarations/…` is a same-change obligation (DS-11 / DM-11 / FR-014).
- § IV (test-first) holds at the artifact level: Tests Mode ON, T005 authored red before T006/T007.
- Nothing here asks for a constitution change.

## Unmapped tasks

None. All 31 rows map to at least one FR or SC. Two attribution questions were re-checked and are not defects: row tags that name fewer FR/SC than their Traceability cell (the preamble declares the table the single statement of the partition, so the cell is the authoritative reading), and the five single-row FRs above (each re-read).

## Checklist accountability (pass H)

Sources: `checklists/layer-criteria-2026-11-05.md` (38 items, all unchecked — judging belongs to the reviewer; 38/38 carry a `Req §` anchor, 38/38 are question-shaped, ids continuous `CHK001…CHK038`) and `checklists/requirements.md` (17/17 checked, no `[Gap]`).

| Item | Tag | Disposition |
|---|---|---|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-002` (unchanged; FR-002 states the conjunctive criterion and the three reason glosses map onto a D2-only / D1-only / by-decree failure) |
| CHK005 | Gap | `CHK005 disposition: covered-by requirements.md § FR-004 + § Key Entities` (the screen defines the candidate universe; a markdown file outside the three carrier surfaces is a carrier, not a unit) |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § FR-004 + § Key Entities`; the residual weakness (stated structurally rather than in one sentence) is closed by FR-018's new closing rule |
| CHK013 | Gap | `CHK013 disposition: raised-as-finding C-03` → **closed** by `fd84ed63` (FR-013 registers the label's freedom and its three mechanical judgements) |
| CHK015 | Gap | `CHK015 disposition: raised-as-finding C-04` → **closed** (FR-005: carrier-only `consumers` is a schema error) |
| CHK023 | Gap | `CHK023 disposition: raised-as-finding C-06` → **closed** (FR-016: all three actions) |
| CHK025 | Gap | `CHK025 disposition: covered-by requirements.md § FR-011` (batch-level attribution sentence lives in C-04x, unchanged) |
| CHK030 | Gap | `CHK030 disposition: raised-as-finding C-02` → **closed** (FR-018's ∪ closing rule) |
| CHK037 | Gap | `CHK037 disposition: raised-as-finding F-05` → **closed** (`FR-023` 0 occurrences; T001 cites `FR-011, FR-018`) |
| CHK038 | Gap | `CHK038 disposition: raised-as-finding C-05` → **closed** (FR-019's guard leg) |

**unchecked(10) + unraised(0) + undispositioned(0) = 10 = raised(6) + dispositioned(4).** Residue: **0**.

## Residue list (round-1 findings)

| Round-1 ID | Severity then | Status | Disposition |
|---|---|---|---|
| F-01 | CRITICAL | `fixed` | `fd84ed63` — single owner enumeration in FR-010, two roles separated, four sites reference it by name |
| F-02 | HIGH | `deferred` (partially fixed) | Contracts `fixed` by `9284c789` (59/59 `md-bold-closed`); the tasks-side banner is **carried as R2-03** (MEDIUM) — re-tiered on its present surface, not downgraded for convenience |
| F-03 | HIGH | `fixed` | `fd84ed63` — referents named in FR-009 / SC-005 / SC-006 and both Measurement Sources rows |
| F-04 | LOW | `fixed` | `fd84ed63` — invocation pinned in FR-007 (b); attribution moved to the reason text |
| F-05 | MEDIUM | `fixed` | `2b18485e` |
| F-06 | MEDIUM | `fixed` | `fd84ed63` |
| F-07 | MEDIUM | `fixed` | `9284c789` — 38/35/39 with provenance; five names verbatim |
| F-08 | MEDIUM | `fixed` | `fd84ed63` |
| F-09 | LOW | `fixed` | `2b18485e` |
| C-01 | MEDIUM | `fixed` | `9284c789` — engine-side column complete. **Its completion is what exposed R2-02's membership question** |
| C-02 | MEDIUM | `fixed` | `fd84ed63` |
| C-03 | MEDIUM | `fixed` | `fd84ed63` |
| C-04 | MEDIUM | `fixed` | `fd84ed63` |
| C-05 | MEDIUM | `fixed` | `fd84ed63` |
| C-06 | LOW | `fixed` | `fd84ed63` |
| E-01 | MEDIUM | `fixed` | `2b18485e` — baseline frozen and idempotent |
| G-01 | LOW | `fixed` | `2b18485e` |

No round-1 row is `rejected`.

## Systemic observations

1. **The remediation repaired what the report named and left what the report's *cause analysis* named un-repaired.** Round 1 wrote two causes for the same symptom (F-02 "the contracts are unparseable" and "the tasks file emits no `[green:]` claim"). The plan repair fixed the first; the tasks repair's own closing paragraph says the second is "not a defect", while `tasks.md:11` still gives the *first* cause as the reason for the non-use. The lesson is mechanical: when a finding has two causes, the repair list must name **both sites**, not both symptoms.
2. **A feature that edits the registry can break a registry guard.** `R2-01` is the second instance in this loop of the same pattern — an artifact edit in one file breaking a machine judgement in another (`F-05`'s checklist residue was the first). The guard set over `.specify/memory/` is not part of the feature's own test surface, so no stage's gate looked at it. Recommend that any stage that writes to `.specify/memory/` run `tests/contract/test_expression_compatibility.py` (one file) as part of its targeted set.
3. **The scope owner and the scope roster drifted because the roster was derived from a dated table, not from the criterion.** The requirements' `## Initial Scope Adjudication` table is explicitly "dated record, not owner" — but its D2 column is what the plan's roster inherited, and measurement has since contradicted four of its cells. A dated record that a later stage *consumes as input* inherits the owner's authority in practice; either the table should be re-marked as "not an input" or the consuming stage should re-derive from the criterion.
4. **Test-budget bookkeeping note (for the driver, not a spec finding).** Round 1's E3 row recorded `not-run-docs-only` and justified it with "targeted-set-v1 yields the empty set". Clause (b) of TB-05 is unconditional — it selects the delivery-surface tests for every stage — so the correct statement is "16 files selected, none run because the stage changed only documentation (TB-06)". This round records the selection **and** runs it, which is the stricter reading of the same clause (§ E3 row, below).
5. **Cost note (`token-efficiency` marker)**: the mechanical checks that produced the two HIGH findings were cheap — one pytest invocation (19 s), one `grep` over `.specify/memory/`, one `git log -S`, one table parse of C-044/C-045. Reading artifacts end-to-end (≈2 000 lines) was still needed for the residue list, but the two *new* findings came entirely from programs. No token counts are claimed (no source).

## Next actions (not applied — analyze holds no write authority)

1. **`R2-01` (HIGH, feature-owned, one line)**: reword `.specify/memory/features/084.md:31` so it records the reading without a `flow_class: <value>` assignment token; re-run `python3 -m pytest -q tests/contract/test_expression_compatibility.py` to confirm the offender list is empty. Not plan-owned → no PLAN-EDIT.
2. **`R2-02` (HIGH, needs an owner's decision — this is the halt point)**: choose between (a) requirements-as-scope-owner → drop/re-mark the eight `none` rows in C-044/C-045 (**substantive plan change under the active PLAN CONSTRAINT, deliberate reopen**) and align T015; or (b) restate FR-006 (i) as a post-migration criterion and replace T015's closing sentence (**requirements semantic change**). Both are upstream of analyze.
3. **`R2-03` (MEDIUM, tasks-owned)**: make `tasks.md:11` and `tasks.md:204` state a true reason — either "optional per the template; the partition is in § Traceability" or claim the 59 clauses with `[green:]` (which also turns the clause lane green).
4. **`R2-04` (LOW)**: no action.
5. **Framework observations (not this feature)**: `pre-analyze-check.py:41` `CLAUSE_DEF` cannot see the canonical `C-<digits>` id (077, 079, 084 all read `clauses: 0`); TB-05 clause (b) should be reconciled with TB-06's docs-only shape so an E3 row can record both the selection and the non-run.
6. **Loop budget**: exhausted — requirements → plan → tasks each had one bounded repair and this is the final analyze. **Hand up rather than iterate a third time.**

## E3 row (stage-status)

Appended to `test-evidence/stage-status.md` under "analyze（round 2, 2026-11-05）":

```yaml
stage: analyze
row_type: stage-status
status: ran
selection_basis: targeted-set-v1@stage_base=2b18485e (clauses (a) 0 / (b) 16 / (c) 0)
selected_paths: 16 files (test-evidence/analyze-round2-targeted-set.txt)
sufficiency: the delivery-surface contract/integration tests of clause (b); (a) and (c) are empty because no changed path is executable or a fixture
rc: 1
passed: 295
failed: 3
new_failures: not_computable (the implement-start baseline has not been captured yet); per-failure attribution taken instead — 1 artifact-caused (R2-01), 2 environmental (git pin 2.54.0 vs 2.43.7; temp-dir permission)
baseline_compare: none available at this stage (baseline slot belongs to implement start)
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/analyze-round2-targeted-run.txt
```

## Evidence pointers

- `test-evidence/analyze-round2-targeted-set.txt` — the targeted-set selection for `stage_base=2b18485e`, with the input changed-path set and the per-clause hit counts.
- `test-evidence/analyze-round2-targeted-run.txt` — the full pytest output of the 16 selected files plus the three failure transcripts (exit code and elapsed time appended).
- `test-evidence/stage-status.md` — the E3 row above.
- `test-evidence/analyze-report-2026-11-05.md` — round 1, the delta baseline for this report.
- Commands run for this report (all read-only except the two evidence writes): `clause_extract.py` over the five contracts · `account-clause-coverage.py --spec-dir …` (no `--freeze`) · `pre-analyze-check.py --stage {requirements,plan,tasks}` · `validate-requirements.py` · `validate-tasks.py` · `validate-decision-tensions.py --json` · `decomposition-check.py --mode {plan,tasks}` · `python3 -m pytest -q <16 selected files>` · `git diff --stat 3ffeb26e -- …` (081 frozen surface) · `git diff --stat 9284c789..HEAD` / `4b65517c..HEAD` over the plan-owned set · `git log -S "flow_class: execution"` · `grep` over `.specify/memory/` for the guard pattern · `git status --porcelain` before/after the validation wave.
- Validation wave scratch: `.specify/.tmp/084-analyze-r2/` (briefs + stream-json transcripts), a sanctioned scratch root; what survives is this report's § Validation wave, which quotes both evidence boundaries verbatim.
