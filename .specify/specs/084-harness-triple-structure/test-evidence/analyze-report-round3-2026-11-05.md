# Analyze Report — Round 3 — 084 Harness 三重结构（markdown + yaml + script）

**Round**: 3 (final gate; the loop budget was **explicitly reset by the user** after round 2's hand-up, and the path-A reopen was completed before this run)
**Date**: 2026-11-05 | **Stage**: analyze | **Stage base**: `b1b19e93` (= HEAD) | **Branch**: `084-harness-triple-structure`
**Prior reports**: `analyze-report-2026-11-05.md` (round 1: 1 CRITICAL / 2 HIGH / 10 MEDIUM / 4 LOW) · `analyze-report-round2-2026-11-05.md` (round 2: 0 / 2 / 1 / 1, hand-up)
**Artifacts judged**: `requirements.md` · `plan.md` · `data-model.md` · `contracts/`×5 · `quickstart.md` · `research.md` · `feature-ref.md` · `tasks.md` · `checklists/*.md` · `.specify/memory/features.md` · `.specify/memory/features/084.md` · `.specify/memory/constitution.md`
**Read-only**: no artifact was modified, no commit was made, nothing was pushed. The only writes are this report, the three round-3 evidence files, the E3 row appended to `test-evidence/stage-status.md`, and the wrap-up engine records. `.specify/specs/` and `.specify/memory/` are byte-identical before and after this run (`git status --porcelain` read 27 lines before the analysis and the same 27 lines after it; all of them pre-existing runtime records, none of them an artifact).

## Verdict

**GATE GREEN. `CRITICAL = 0`, `HIGH = 0`, `MEDIUM = 3`, `LOW = 2`.**

All four rows of the round-2 report are closed with re-measured evidence, and the one reading the dispatch flagged as still open — **R2-02**, the scope/roster conflict — is closed **structurally**, not by assertion: the eight `engine side = none` facts no longer appear in any in-scope table, the requirement that owns scope was not inverted, and the three artifacts that used to give three instructions now give one. `tasks.md` T015/T016 and the scope table are in sync; the exclusion-record arithmetic obeys `data-model.md` E-2 **R-4** (one disposition per unit, never both).

What remains is **not** a cleared-backlog artefact: three MEDIUM rows are new this round, and one of them (`F-12`) was **introduced by the R2-03 repair itself**. None of them blocks `/speckit.implement`: each is a one-line wording/precision repair on a non-criterion surface, and each is stated with its measurement so the implementer cannot mistake it for a reading.

- **`F-10` (MEDIUM)** — the row count `no-machine-fact.yaml` "carries 8" collides with the two rows `T020` writes into the same file (total 10).
- **`F-11` (MEDIUM)** — the `history-categories` exclusion anchor ("the five category names are in no `.py` and no `.sh`") does not reproduce: 4 of the 5 names occur in engine sources as unrelated tokens. The conclusion survives on a different measurement.
- **`F-12` (MEDIUM)** — the new `tasks.md` banner attributes the FR-lane `0/19` reading to the unused `[green:]` tag; its own cited authority (§ 5.1 of the round-2 report) says the opposite cause, and the contracts carry no citation group at all.
- **`F-13` (LOW)** — `C-044`'s ARC row says "the template's `[ARC_*]` placeholders are copied from `--json` verbatim"; § 2.4 of `templates/review-template.md` holds 11 distinct placeholders, of which 7 are the checker's copied keys.
- **`F-14` (LOW)** — `ARC verdict mapping` is the only in-scope roster row not written as a kebab-case `<fact-slug>`.

**No CRITICAL/HIGH row exists, so the independent validation wave dispatched zero validators** (MEDIUM/LOW skip validation by the skill's own rule). The zero-finding floor's obligation — "re-read every requirement whose coverage rests on a single task row, plus a sample" — is discharged in § Coverage summary with the sample named.

**Headline separation**: the round-1 and round-2 backlogs are cleared (17/17 and 4/4), **and** this rerun is not clean. Those are two different claims and both are reported.

## Rerun delta

### Resolved since last run (each with the evidence that closes it)

| Prior ID | Was | Closed by | Evidence re-measured this round |
|---|---|---|---|
| `R2-01` | HIGH | `43dcf30e` | `python3 -m pytest -q tests/contract/test_expression_compatibility.py -k c2_no_project_side_classification_store` → **1 passed, 15 deselected**, exit 0. `grep -rn "flow_class" .specify/memory/` returns 12 hits over 5 files and **none of them is `features/084.md`**; that file's line 31 now reads 「类别读取结果：`execution`（由 `requirements.md` 的声明行解析）」, which the C-2 regex (`flow_class["']?\s*[:=]\s*…`) cannot match. The targeted run below fails **2** tests, not 3, and the disappeared failure is exactly this one. |
| `R2-02` | HIGH | `ba141671` (path A, user-authorized) | See § R2-02 closure — four independent measurements, including the one the round-2 validator said was unproven. |
| `R2-03` | MEDIUM | `b1b19e93` | `tasks.md:11` now states the **true** premise: clauses are `C-001…C-059`, all five contracts parse as `md-bold-closed` (re-measured: 12+13+16+10+8 = 59), and the tag's non-use is grounded in the template's own "optional" wording — not in the falsified `DS/HC/SR/MB/DM` + `md-none` story. `tasks.md:204` (§ Traceability preamble) agrees. **Its repair introduced `F-12`**, a narrower mis-attribution. |
| `R2-04` | LOW | no action (by design) | History is immutable and no artifact carries the `DN` typo: `grep -rnE '\b(DS\|HC\|SR\|MB\|DM)-[0-9]{1,2}\b'` over the spec tree (excluding `test-evidence/`) returns **0**. Recorded once more so it is never mistaken for a reading. |

### New since last run (including what the remediation itself introduced)

| ID | Severity | Why it is new |
|---|---|---|
| `F-10` | MEDIUM | The path-A repair moved the row-count question from "which facts are in scope" to "how many rows one file holds". The `8` was written while only the roster's rows were counted; `T020` writes two more rows into the same file, and the requirements' own scope table is where those two units are already dispositioned `[[STR-006]]`. |
| `F-11` | MEDIUM | Also a path-A product: the anchor column is new, and the `history-categories` anchor is the only one of the eight whose sentence is a **name-substring** containment claim rather than a structural one (`Bootstrap/Operationalize/Optimize` measure 0 hits; the five history names do not). |
| `F-12` | MEDIUM | Introduced by `b1b19e93`: the replacement banner sentence carries a causal claim about the **FR** lane borrowed from § 5.1, whose own text assigns that zero to the missing citation groups, not to the tag. |
| `F-13` | LOW | Not path-A-introduced (the sentence predates it and round 2 read the same cell); re-measured now against `templates/review-template.md` § 2.4 and reported because it is decidable and wrong as written. |
| `F-14` | LOW | Path A made this row the **last** in-scope fact still named by a human phrase rather than a slug — the seven batch-2 rows above it are all slugs, so the omission is now conspicuous and load-bearing for one file name. |

### Carried over

None. Every round-2 row is closed; nothing is carried at any severity.

## R2-02 closure — the four measurements the dispatch asked for

**(1) Are the eight engine-less facts out of every in-scope roster?** Yes. `C-044` now holds **7** rows (`expression-gate-faces`, `expression-stage-operator-table`, `ARC verdict mapping`, `driver-stage-sequence`, `driver-gate-roster`, `driver-completion-sentinels`, `driver-stage-artifacts`) and `C-045` holds **7** (`memory-types`, `memory-retention-thresholds`, `history-manifest-schema`, `probe-class-values`, `probe-object-binding-map`, `quant-record-schema`, `trigger-state-schema`) — 14 rows, down from 22. The only `none` left in either paragraph is the English word inside the sentence "a record fact that measured `none` on 2026-11-05 is recorded in § Facts outside the roster", i.e. a pointer, not a row.

**(2) Do `C-044`/`C-045` keep only rows with an engine side?** Yes, and the contract is now explicit that this is a membership condition, not luck: "**Every row in this table has a live engine side today** — that is now a membership condition of the roster, not a coincidence". Every one of the 14 cells names a file and a constant or read point. Spot-verified against the tree: `closure-acceptance-check.py:801 def final_path_counts(` and `:1334 "verdict": "block" if blocking else "accept"` exist as described; `history-utils.py:208 _manifest_path(` / `:212 read_manifest(` / `:222 write_manifest(` exist.

**(3) Eight unit-level exclusion records vs FR-002 / FR-005 / E-2's one-disposition rule?** Consistent, and the arithmetic is stated rather than implied. § Facts outside the roster measures 8 facts onto **8 units** (2 analyze + 1 self-improvement + 5 improve), and it names the two facts that get **no** row (`review-segment-sequence`, `history-categories`) with the reason (`R-4`: a unit is never both declared and excluded; E-5 makes that pair a finding, not a file-order win). I re-derived the carrier/unit intersection mechanically: no unit named in the exclusion list appears as a `carrier side` in `C-042`/`C-044`/`C-045`, so the both-states condition does not arise anywhere in the feature. The phrasing of the rule is deferred to its owner (`data-model.md` E-2 **R-4**) rather than restated — correct under One-Source-of-Truth.

**(4) Do `review-segment-sequence` / `history-categories` units legitimately stay in scope?** Yes. `templates/commands/review.md` + `skills/internal/review-sdd-process/SKILL.md` keep `ARC verdict mapping` in `C-044`; `skills/internal/manage-history/SKILL.md` keeps `history-manifest-schema` in `C-045`. Both requirements rows (`:187`, `:190`) say so in the D2 column, and the requirements' date-record paragraph (`:203`) states the same rule in the same words. I also checked the neighbouring unit that could have been orphaned — `shared/workflow/self-improvement-workflow.md` — and it is **not** a candidate unit at all: `grep -E 'scripts/python/[a-z0-9_-]+\.py|skills/(external|internal)/[a-z0-9_-]+/scripts/'` over that file returns **0** hits, so screen S never yields it and no disposition is owed.

**(5) Is T015/T016 in sync, and is the scope table in sync?** Yes, in both directions. `T015` now migrates **only** `ARC verdict mapping` and then writes the `no-machine-fact` rows "one row per unit that lost its last in-scope fact", naming the 8 units; `T016` drops `history-categories` and writes **no** row for it, with the `R-4` reason inline. `tasks.md` § Traceability rows T015/T016 say the same. The scope table changed 3 rows to `excluded [[STR-006]] (no-machine-fact)` and 2 rows stay in-scope with their surviving fact written into the D2 column; FR/SC ids, the `Flow Class` line and every `Path` marker are untouched (`validate-requirements` still reads 286 lines / 25 definition rows / 14 strings).

**(6) Is FR-006 (i) reversed? (path B did not happen)** No. `requirements.md:143` still defines (i) as 「存在至少一个确定性引擎**必须读取该值才能作出判定**，且该判定结果随取值改变而改变」 with the A2 narrowing intact, and the disposition clause 「任一不成立即留在原处」 is unchanged. The competing reading is now rejected **in the artifact that would have used it**: `contracts/migration-batches.contract.md:104` says the "read point is created during migration" reading "is explicitly **not** available to this feature: it would make the criterion vacuous". `grep -rniE "read point is created|created during migration|post-migration criterion"` returns exactly that one line and nothing else in the spec tree. `C-047` step 3 still describes replacing **an existing** inline constant with a read through the shared entry, which is now coherent for all 14 in-scope rows because every one of them has an inline constant today.

**One residue of the repair, raised separately as `F-10`**: the *scope* question is settled, but the *file-row count* sentence is not, and `T020` contradicts it by two rows.

## Metrics

| Metric | Value | Source |
|---|---|---|
| Total requirements | 19 FR + 6 SC + 14 STR | `requirements.md` (286 lines, 25 definition rows — `validate-requirements.py`) |
| Tasks | 31 (Setup 2 / Foundational 5 / US1 3 / US2 7 / US3 2 / US4 4 / Polish 8), 8 `[P]` rows in four path-disjoint pairs | `tasks.md`, phase headings counted mechanically |
| FR → task coverage | 19/19 from § Traceability; 19/19 also from row tags | re-derived programmatically this run |
| Task → FR/SC mapping | 31/31 rows carry at least one FR or SC; `set(traceability ids) == set(task ids)` (31 = 31) | same run |
| Contract clauses parseable | 59 of 59 across 5 files, `md-bold-closed` (12+13+16+10+8) | `clause_extract.py` |
| Contract clauses claimed by the tasks file | 0 of 59 | `account-clause-coverage.py` |
| FRs cited from contract citation groups | 0 of 19 (cause: the contracts carry **no** `(FR-0NN)` group — measured `count=0`) | same run |
| Coverage accountant | `status: uncovered`, **exit 1**; 572 uncovered, 59 beyond the frozen baseline of 513 names, 103 named-unparseable files | `analyze-round3-gates-2026-11-05.txt` |
| Feature linkage | `Total Features: 77` = 77 rows; index row 084 (`Planned`) → `features/084.md` (`Planned`); spec path → `requirements.md` | `features.md`, `features/084.md` |
| Finding classes | inconsistency 5 · underspecification 0 · coverage 0 · duplication 0 · feature linkage 0 | findings table |
| CRITICAL / HIGH / MEDIUM / LOW | **0 / 0 / 3 / 2** | findings table |
| Prior-run residue | round 1: 17 closed; round 2: 4 closed; **0 carried, 0 rejected** | § Residue list |
| Validators dispatched / confirm / downgrade / reject | 0 / 0 / 0 / 0 (no CRITICAL/HIGH to validate; downgrade rate not applicable) | § Validation wave |
| Checklist `[Gap]` accountability | 10 unchecked = 10 dispositioned; residue 0 | § Checklist accountability |
| Targeted test set (E3) | 16 contract/integration files, **2 failed / 296 passed**, 18.83 s, rc 1 (both failures environmental and named) | `analyze-round3-targeted-run.txt` |

## Findings

`propagation_surface` = the downstream artifact that inherits the finding; severity is read from that field. A row whose surface is `none` is capped at MEDIUM.

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| `F-10` | Inconsistency (row-count reading vs the feature's own exclusion set) | `tasks.md` T015+T020 → implement writes `exclusions/no-machine-fact.yaml` → `SC-004`'s N/N count | **MEDIUM** | `contracts/migration-batches.contract.md:132`; `requirements.md:203`; `features/084.md:33`; `tasks.md:144` (T020); `requirements.md:198-199` | `requirements.md:203`, the contract's § closing sentence and `features/084.md:33` all state a **file** property — "`no-machine-fact.yaml` carries **8 rows**" / 「写 8 行」 — while `T020` writes two more rows into that same file for `skills/internal/summarize-project/SKILL.md` and `skills/external/humanize/SKILL.md`, which the scope table (`:198`, `:199`) already disposes as `excluded [[STR-006]]` = `no-machine-fact`. FR-005 puts exclusion rows in `exclusions/<reason>.yaml`, so all ten land in one file. No acceptance criterion breaks (SC-004's N/N is a ratio and DoD-6 is per-unit), which is why this is MEDIUM and not HIGH — but a closure reviewer counting rows against "8" will read a correct tree as wrong. | **requirements + plan + feature record, one qualifier each**: say "these eight facts contribute 8 rows; the file's total is 10, the other two coming from the scope table's own `no-machine-fact` units (`summarize-project`, `humanize`, `T020`)". Do not move the count; move its scope. |
| `F-11` | Inconsistency (exclusion anchor not reproducible as written) | `tasks.md` T015/T016 → implement re-measures the anchor → exclusion row for `skills/internal/manage-history/SKILL.md` | **MEDIUM** | `contracts/migration-batches.contract.md:120`; `requirements.md:190` | The `history-categories` anchor asserts 「五个分类名在 `.py`／`.sh` 零命中」 / "the five category names are in no `.py` and no `.sh`". Measured this run with a token grep: `decisions` 27 hits, `lessons` 1, `flows` 5, `conflicts` 35, `TODOs` 0 — **4 of the 5 occur in engine sources**, all of them as unrelated tokens (`docs/decisions/` paths, `interview-utils.py`'s own `decisions` key, "concurrent flows" prose, `conflicts` counters). The **substantive** conclusion still holds — no engine enumerates the five-name set or branches on it, and `history-utils.py` writes the store without enumerating categories — so the exclusion is right and only its evidence sentence is wrong. The risk is mechanical: the contract's own Verification row says a fact "whose anchor grep returns a live engine read point moves **back** into `C-044`/`C-045`", so an implementer who runs the anchor as written meets a contradiction and must adjudicate scope at edit time. The other seven anchors are structurally stated and reproduce: `Bootstrap\|Operationalize\|Optimize` over `scripts/` + `skills/` = **0 files**. | **plan-owned, one sentence**: restate the anchor with its comparison unit — "no engine enumerates or branches on the five-name set (measured: `TODOs` 0 hits; `decisions`/`lessons`/`flows`/`conflicts` occur only as unrelated tokens — `docs/decisions/` paths, `interview-utils.py`'s `decisions` key, prose 'flows', `feedback-utils.py`'s `conflicts` counter) — `history-utils.py` writes the store and manifest without enumerating categories". Mirror the same sentence at `requirements.md:190`; the conclusion (and the exclusion) does not change. |
| `F-12` | Inconsistency (cause mis-attribution in the repaired banner) | `tasks.md:11` banner + `:44` → implement reading of the coverage lane | **MEDIUM** | `tasks.md:11`; cited authority `analyze-report-round2-2026-11-05.md` § 5.1; measured `count=0` `(FR-0NN)` groups in `contracts/` | The banner says the "`0/19 FRs cited from citation groups`" reading "is a known, non-blocking consequence of the optional tag being unused (analyze round 2 § 5.1)". § 5.1 says the opposite: the **clause** lane reads 0 because no `[green:]` claim exists, while the **FR** lane reads 0 because the five contracts carry **no citation group** — "the round-1 attribution of 0/19 to F-02 is no longer the operative cause". Measured: `grep -oE '\(FR-0[0-9]{2}\)'` over the five contracts = **0**, so adding `[green:]` tags would move the clause lane and leave the FR lane at 0. The *verdict* the banner supports ("not a parse failure", "non-blocking") is true; the cause it records is not, and an implementer reading it would expect a green FR lane after claiming clauses. This is the same surface as `R2-03` (banner → implement's reading of the coverage lane), hence the same tier, even though the magnitude is smaller. | **tasks-owned, one clause**: either drop the causal claim ("both lanes are readings, not gates; the partition is in § Traceability, and the FR lane is fed by contract citation groups that these five contracts do not carry") or state the two causes separately, citing § 5.1 correctly. Keep the honest part — the fields now parse and the tag is optional. |
| `F-13` | Inconsistency (over-claimed copy semantics) | `tasks.md` T015 → implement's pointer-scope decision in `templates/review-template.md` § 2.4 | **LOW** | `contracts/migration-batches.contract.md:53` (engine-side cell); `tasks.md:113`; `templates/review-template.md:138-152`, `:287` | The `C-044` ARC row says "the template's `[ARC_*]` placeholders are copied from `--json` verbatim, never recomputed". § 2.4 holds **11** distinct placeholders; the **7** checker keys are copied verbatim (the template's own glossary calls them "the seven keys of the checker"), but `[ARC_CLAIMED_STATUS]` comes from the feature detail, `[ARC_VERDICT]` is `agree`/`refused` derived by the review from the checker's `block`/`accept`, and `[ARC_FAILED_CONDITION]` / `[ARC_FIXED_ITEM]` are judgement on refusal. `T015`'s phrasing ("both of which copy the seven `[ARC_*]` keys verbatim") is defensible; the `C-044` sentence is not, because "the template's `[ARC_*]` placeholders" reads as all eleven. | **plan-owned, one word**: say "the template's **seven checker keys** are copied from `--json` verbatim; its four other `[ARC_*]` slots are sourced elsewhere (claimed status ← feature detail; verdict, failed condition, fixed item ← the review's own judgement)". No pointer scope changes; only the claim's reach. |
| `F-14` | Inconsistency (identity form of the one remaining in-scope fact) | `tasks.md` T015 → the file name implement must create (`facts/<fact-slug>.yaml`) | **LOW** | `contracts/migration-batches.contract.md:53` (row header `<fact-slug>`, cell `ARC verdict mapping`); `tasks.md:113`; `requirements.md:187`, `:203` | `C-044`'s table header is `<fact-slug>` and 13 of its 14 rows are backticked kebab-case slugs; the remaining row is the phrase `ARC verdict mapping`, and the artifacts name that same fact three ways (`ARC verdict mapping` in the contract, `ARC 判定` in the requirements table, `ARC` in prose). `C-003` requires `<fact-slug>` to match `^[a-z0-9]+(-[a-z0-9]+)*$` and to equal both the `fact` key and the filename stem, so today's wording cannot be used as a path. The name is derivable (`arc-verdict-mapping`, by imitation of the 13 siblings), which is why this is LOW — but it is the one place where "path is identity" is satisfied by inference rather than by the roster. | **plan-owned, one token**: write the row as `arc-verdict-mapping` (and mirror it in `T015` and the requirements D2 column). No rename of anything else; the exclusion table's other phrase-named facts never become files, so they need no change. |

## Coverage lane — `status=uncovered`, 59 beyond baseline, 0/19 FRs → **still not blocking after the scope contraction**

Re-adjudicated because the dispatch asked whether the round-2 judgement survives path A. It does, and for two independent reasons, neither of which the scope contraction touched:

- **Scope contraction cannot move the lane.** The lane's inputs are (a) the contracts' clause names and (b) the tasks file's `[green:]` claims. Path A edited roster **rows** inside two clauses; the clause count is unchanged at 59 (re-measured 12+13+16+10+8) and no claim was added, so the reading is byte-identical to round 2: `claimed clauses 0`, `59 beyond the frozen baseline`, `status: uncovered`, exit 1. The lane is red **by construction of the feature**, not by anything path A did.
- **The tag is optional by its owner**, and nothing gates on the lane. `.specify/templates/tasks-template.md` declares `[green:]` optional; `validate-tasks.py` judges only claims that are made; the accountant is consumed by `create-tasks` (for the freeze) and by `analyze` (for a reading) and by **no gate**. `T002` froze the baseline (513 names / 248 corpus files / `base-sha 9284c789`) exactly as intended, so `baseline-missing` does not occur.

Consequence stated plainly: **the clause lane cannot go green for this feature while the tag is unused, and it will stay red at implement and at closure.** That is a recorded, non-blocking reading — not a pass, and not a defect of the artifacts. The FR lane's zero has a *different* cause (no citation groups in the contracts), which is `F-12`'s subject.

## Validation wave

**Zero validators dispatched — by rule, not by omission.** The wave exists to confirm CRITICAL/HIGH rows; this round produced none, and MEDIUM/LOW rows skip validation. Consequently: sent 0, `confirm` 0, `downgrade` 0, `reject` 0, and the downgrade-rate metric is not applicable.

**Same-author delegation not triggered.** Detection was performed by a fresh-context read-only executor that authored none of these artifacts, so the gate's "this session produced them" condition is false and no delegation is owed. That is a weaker guarantee than round 2's two external validators, and it is stated rather than implied: **the MEDIUM/LOW rows above carry a single-reader verdict.**

**Zero-finding floor (applied on the C/H axis).** With no CRITICAL/HIGH row, the skill requires a re-read of the coverage mapping: every requirement whose coverage rests on a single task row, plus a sample. From § Traceability: **FR-001 → T004** (the owner document and its seven-chapter tree — substantive, no other row writes it), **FR-003 → T003** (`contract.yaml` as the value-domain owner — substantive), **FR-012 → T009** (delete the inline constant, keep the `[[STR-014]]` fallback — substantive), **FR-014 → T003** (same-change registration in `framework-map.md` — correctly folded into the row that creates the directory). Sample of the remaining rows: T005 (red-first module, FR-008/FR-015/FR-017/FR-019), T015 (ARC + exclusion rows, FR-006(i)), T027/T028 (batch closure readings, FR-011), T031 (quickstart S5–S8, all 19 FRs). All attributions are correct.

**Read-only proof**: the working tree held 27 lines before the analysis and the same 27 after it; all of them are the pre-existing runtime records (session, exec-quant, feedback, state spine) plus the one 081a session file the clarify engine settled earlier. This run opened no write handle on any artifact.

## Coverage summary

| Lane | Reading | Verdict |
|---|---|---|
| FR → task | 19/19 named by at least one of the 31 rows; 31/31 rows carry an FR or SC (Traceability, re-derived) | **covered** |
| Single-row FRs (re-read one by one) | 4 rows rest on a single task: FR-001→T004, FR-003→T003, FR-012→T009, FR-014→T003. Each re-read; all correct | covered |
| Task → requirement | every tag and Traceability cell resolves to a defined FR/SC; `set(traceability ids) == set(task ids)` at 31 | covered |
| Clause → task (`[green:]`) | 0 claimed of 59 — tag optional by its owner; the banner's cause for the **FR** lane is `F-12` | unmeasurable, non-blocking |
| FR cited from clause citation groups | 0/19 — the contracts carry no `(FR-0NN)` group (measured 0); § 4.2 does not require one | not a defect; FR coverage read from § Traceability |
| Baseline | frozen: 513 names / 248 corpus files / `base-sha 9284c789`; accountant exits 1 with a verdict, not 2 with an input error | resolved (E-01 stays closed) |
| Whole-corpus context | 253 files scanned; 1576 distinct clause names over 150 parsed files; 572 uncovered repo-wide, 513 of them baseline-internal | informational |

## Feature linkage summary

| Check | Reading |
|---|---|
| Index row bound to this spec | `features.md:90` → `084`, status `Planned`, spec path → `requirements.md`, path phrase `C-001…C-059`, no `DS-/HC-/SR-/MB-/DM-` residue (0 hits) |
| Detail file agrees on status | `features/084.md` `**Status**: Planned`; the state machine owns no pre-implement transition, so the status is lawfully held |
| Stage records | § Latest Review carries dated clarify / tasks / checklist / analyze-loop / plan-reopen records (the last one cites the round-2 report as its authority); `checklists/layer-criteria-2026-11-05.md` is in § Related Files; `§ MB-01` → `C-042` |
| Header/rows consistency | `Total Features: 77`, 77 matching rows |
| Feature identity in the spec | `requirements.md` § Related Feature: ID 084 and the name match the index |
| 081 frozen surface | `git diff --stat 3ffeb26e -- shared/workflow/acceptance-hardening.md .specify/shared/workflow/acceptance-hardening.md tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py` → **empty** (zero diff on this branch) |

## Constitution alignment

- `plan.md` § Constitution Check renders **18** rows; re-read against `constitution.md` v1.15.0 this run: **18/18 names identical, 0 missing, 0 mismatched, 0 reordered**.
- § XIV (One Source of Truth): the path-A section defers the one-disposition rule to `data-model.md` E-2 R-4 and the exclusion-reason semantics to FR-002/FR-003 instead of restating them — the pattern round 1's F-01 was repaired into. The three phrase-named facts that never become files (`F-14`) do not create a second namespace; only the ARC row does, and it is LOW for that reason.
- § XVII (Directory Governance) holds: no new top-level directory, and registration of `shared/declarations/…` is a same-change obligation carried by T003 (C-011/C-023).
- § IV (test-first) holds at the artifact level: Tests Mode ON, T005 authors red before T006/T007.
- Nothing here asks for a constitution change, and no constitutional conflict was found (so the CRITICAL carve-out never had to be invoked).

## Unmapped tasks

None. All 31 rows map to at least one FR or SC. Two attribution questions were re-checked and are not defects: rows whose tag list names fewer ids than their Traceability cell (the preamble declares the table the single statement of the partition), and the four single-row FRs above (each re-read).

## Checklist accountability (pass H)

Sources: `checklists/layer-criteria-2026-11-05.md` (38 items, none checked — judging belongs to the reviewer; 38/38 carry a `Req §` or `Non-Goals` anchor; 38/38 question-shaped; ids continuous `CHK001…CHK038`) and `checklists/requirements.md` (17/17 checked, 0 `[Gap]`). Ten items carry `[Gap]`; all ten carry a machine-checkable disposition.

| Item | Tag | Disposition |
|---|---|---|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-002 + § FR-003` — and now **demonstrated** rather than merely covered: path A applies the D2-fails branch (`no-machine-fact`) to three units and the D1-fails branch to two others, each with an anchor |
| CHK005 | Gap | `CHK005 disposition: covered-by requirements.md § FR-004 + § Key Entities` (the screen defines the candidate universe; a markdown file outside the three carrier surfaces is a carrier, not a unit) |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § FR-004 + § Key Entities`; the residual weakness is closed by FR-018's ∪ closing rule |
| CHK013 | Gap | `CHK013 disposition: covered-by requirements.md § FR-013` (finding C-03, closed by `fd84ed63`: the label is free text judged on three mechanical items, and is neither a Shared String nor a seventh reason) |
| CHK015 | Gap | `CHK015 disposition: covered-by requirements.md § FR-005` (C-04, closed: a carrier-only `consumers` is a schema error, not a permanent `pending`) |
| CHK023 | Gap | `CHK023 disposition: covered-by requirements.md § FR-016` (C-06, closed: determinism covers all three actions) |
| CHK025 | Gap | `CHK025 disposition: covered-by requirements.md § FR-011` (batch independence is the requirement; its per-batch attribution sentence lives in `C-046`, which is the plan-side detail of the same requirement) |
| CHK030 | Gap | `CHK030 disposition: covered-by requirements.md § FR-018` (C-02, closed: the ∪ closing rule replaced 「至少」) |
| CHK037 | Gap | `CHK037 disposition: covered-by requirements.md § FR-019` (F-05, closed: `FR-023` occurs 0 times in requirements/tasks/checklist; T001 cites `FR-011, FR-018`; the checklist's three sites were synced in `2b18485e` and the original id survives only in the dated evidence) |
| CHK038 | Gap | `CHK038 disposition: covered-by requirements.md § FR-019` (C-05, closed: the single-subset-parser guard leg, allowlist = N4's two grandfathered parsers) |

**unchecked(10) + unraised(0) + undispositioned(0) = 10 = raised(10) + dispositioned(10).** Residue: **0**.

## Residue list

| Prior ID | Severity then | Status | Disposition |
|---|---|---|---|
| F-01 | CRITICAL | `fixed` | `fd84ed63` — single owner enumeration in FR-010; re-read this round: two roles (六 / 五), four sites reference it by name |
| F-02 | HIGH | `fixed` | contracts `9284c789` (59/59 `md-bold-closed`); tasks half `b1b19e93` — banner now states a true premise (new residue: `F-12`) |
| F-03 | HIGH | `fixed` | `fd84ed63` — referents named in FR-009 / SC-005 / SC-006 and both Measurement Sources rows |
| F-04 / F-06 / F-08 / C-02…C-06 | LOW/MEDIUM | `fixed` | `fd84ed63` (each re-read this round, each still holds) |
| F-05 / F-09 / E-01 / G-01 | MEDIUM/LOW | `fixed` | `2b18485e`; `coverage-baseline.txt` present and idempotent |
| F-07 / C-01 | MEDIUM | `fixed` | `9284c789` — 38/35/39 recorded with provenance, five names verbatim, engine-side column complete (its completion is what exposed R2-02 and, indirectly, `F-11`) |
| R2-01 | HIGH | `fixed` | `43dcf30e` — guard test green, offender list empty |
| R2-02 | HIGH | `fixed` | `ba141671` — path A; see § R2-02 closure (new residue: `F-10`) |
| R2-03 | MEDIUM | `fixed` | `b1b19e93` — false premise removed (new residue: `F-12`) |
| R2-04 | LOW | `no action` | history immutable, no artifact carries the typo |

No row is `rejected`. **0 carried.**

## Systemic observations

1. **Three rounds found the same defect class three times: a recorded reading that a re-run contradicts.** Round 1: the contracts could not be parsed (recording said they could). Round 2: the banner's `md-none` premise (recording said it held). Round 3: the banner's FR-lane cause (`F-12`) and one exclusion anchor (`F-11`). Each was cheap to measure and expensive to inherit. The mechanical countermeasure already exists in this feature's own design (`C-048`'s five readings, `C-044`'s "re-measure, never inherit") — the remaining gap is that **plan-owned prose written *about* a measurement is not itself re-measured by any gate.** A plan-side `grep`-backed claim is only checked when a human rereads it.
2. **A count is the most reusable defect shape.** `F-10` is not a wrong number; it is a right number with an unstated denominator (8 = these eight facts' rows, not the file's rows). Round 1's C-01, round 2's `R2-03` and this round's `F-10` are one family: the artifact states a quantity without its comparison unit. The feature's own `closed-set-claims` constraint (requirements § Constraints) asks exactly for that unit — the constraint held for the acceptance criteria and did not reach the narrative.
3. **Path A validated the criterion rather than weakening it, and the validation was cheap.** The three claims that could have been hollow were checked with three programs (`clause_extract`, a table parse, and the anchor greps) in seconds. Two of the eight anchors pass cleanly (`Bootstrap|Operationalize|Optimize` = 0 files); one is the `F-11` imprecision. So the answer to "did the exclusion set hide a scope error?" is no — and it is now an evidenced no rather than an asserted one.
4. **The scope owner and the roster are now on one measurement basis.** Before path A, the roster's membership was derived from a dated table; after it, membership is "does the engine side exist today", which is the requirement's own (i) evaluated on the tree. `F-11` is the residual cost of moving evidence into a table: the anchor column is new prose and inherits prose's failure modes.
5. **Test-budget bookkeeping.** The targeted set re-derives to the same 16 files at `stage_base=b1b19e93` (clause (a) 0 hits, clause (b) 16, clause (c) 0 — the changed paths are all runtime records under `.specify/memory/`). It was **run**, not just selected: 2 failed / 296 passed, and both failures are the environmental pair round 2 already named (`test_e_a_stale_pin…`: `git version 2.43.7` vs the recorded `2.54.0 (Apple Git-157)`; `test_c22_watch_target_hook_selftest`: `mkdir /home/agent/tmp/spec-kit: Permission denied`). The third round-2 failure — the artifact-caused one — is gone.
6. **Cost note (`token-efficiency` marker)**: all five findings came from programs — one pytest invocation (19 s), two counts over `templates/review-template.md`, one token grep over `scripts/`+`skills/`, one regex over the contracts, one row-count parse. No token counts are claimed (no source).

## Next actions (not applied — analyze holds no write authority)

1. **`F-10` (MEDIUM, requirements + plan + feature record, wording)**: scope the "8 rows" claim to the eight facts it counts, and state the file's total (10) with its two other contributors. Low risk; no count moves.
2. **`F-11` (MEDIUM, plan-owned)**: restate the `history-categories` anchor with its comparison unit and the measured token hits; mirror the sentence at `requirements.md:190`. The exclusion stands.
3. **`F-12` (MEDIUM, tasks-owned)**: split the banner's two causes and cite § 5.1 correctly; keep "not a parse failure / not blocking".
4. **`F-13`, `F-14` (LOW, plan-owned)**: one word each ("seven checker keys"; `arc-verdict-mapping`).
5. **`R2-04` (LOW)**: no action.
6. **Framework observations carried from round 2, unchanged and still not this feature's**: `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py:41` `CLAUSE_DEF` compiles `^- \*\*([A-Z]{2,4}-\d{2})\b` and cannot see the canonical `C-<digits>` id, so `summary.clauses` reads 0 for 077 / 079 / 084 alike (this run: `clauses: 0` with 59 clauses present); and `audit-test-budget.py` does not read the E3 rows in `stage-status.md`.

## E3 row (stage-status)

Appended to `test-evidence/stage-status.md` under "analyze（round 3, 2026-11-05）":

```yaml
stage: analyze
row_type: stage-status
status: ran
selection_basis: targeted-set-v1@stage_base=b1b19e93 (clauses (a) 0 / (b) 16 / (c) 0); the stage itself is docs-only — changed_paths[] are 27 pre-existing runtime records under .specify/memory/ and .specify/state/
changed_paths[]: 27 paths, all .specify/memory/{session,exec-quant,feedback}/* and .specify/state/084-harness-triple-structure.md (none under tests/, scripts/, skills/**/scripts/, src/, or tests/fixtures/)
selected_paths: 16 files (test-evidence/analyze-round3-targeted-set.txt)
sufficiency: the delivery-surface contract/integration tests of clause (b); (a) and (c) are empty because no changed path is executable or a fixture
rc: 1
passed: 296
failed: 2
new_failures: not_computable (the implement-start baseline has not been captured yet); per-failure attribution taken instead — 0 artifact-caused, 2 environmental (git pin 2.54.0 vs 2.43.7; /home/agent/tmp/spec-kit permission denied). The round-2 artifact-caused failure (test_c2_no_project_side_classification_store) is gone.
baseline_compare: none available at this stage (baseline slot belongs to implement start)
evidence_ptr: .specify/specs/084-harness-triple-structure/test-evidence/analyze-round3-targeted-run.txt
```

## Evidence pointers

- `test-evidence/analyze-round3-gates-2026-11-05.txt` — every deterministic gate of this run captured in full (commands, complete stdout, exit codes): `validate-requirements`, `validate-tasks`, `validate-decision-tensions`, `decomposition --mode plan|tasks`, `pre-analyze --stage requirements|plan|tasks`, `clause_extract` ×5, `account-clause-coverage` (exit 1), the 081 frozen-surface diff, the guard test, plus the round-3 supplemental readings (`no-machine-fact.yaml` mentions, ARC placeholder counts, history-category token hits, `Bootstrap|Operationalize|Optimize` hits).
- `test-evidence/analyze-round3-targeted-set.txt` — the `targeted-set-v1` selection for `stage_base=b1b19e93` with the input changed-path set and the per-clause hit counts.
- `test-evidence/analyze-round3-targeted-run.txt` — the full pytest output of the 16 selected files, the two failure transcripts, exit code and elapsed time.
- `test-evidence/stage-status.md` — the E3 row above.
- `test-evidence/analyze-report-round2-2026-11-05.md` — round 2, the delta baseline for this report (and the authority for `F-12`'s § 5.1 comparison).
- `test-evidence/plan-reopen-pathA-gates-2026-11-05.txt` — the path-A reopen's own gate readings, which this round re-measured rather than inherited.
