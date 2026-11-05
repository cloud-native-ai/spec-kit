# Analyze Report — 084 Harness 三重结构（markdown + yaml + script）

**Round**: 1 (no prior report for this feature → no rerun delta)
**Date**: 2026-11-05 | **Stage**: analyze | **Base commit**: `9abb10fb` (checklist U4 PASS) | **Branch**: `084-harness-triple-structure`
**Artifacts judged**: `requirements.md` · `plan.md` · `data-model.md` · `contracts/`×5 · `quickstart.md` · `research.md` · `feature-ref.md` · `tasks.md` · `checklists/*.md` · `.specify/memory/features.md` · `.specify/memory/features/084.md` · `.specify/memory/constitution.md`
**Read-only**: no artifact was modified, no commit was made, nothing was pushed. The only writes are this evidence file, `test-evidence/account-clause-coverage.txt`, the E3 row in `test-evidence/stage-status.md`, and the wrap-up engine records.

## Verdict

**Not ready to `/speckit.implement` as the artifacts stand.** One CRITICAL and two HIGH findings are open. Each is disposed below with the upstream stage that must repair it and the minimal repair — none was repaired here (analyze holds no write authority over artifacts), and none is left unadjudicated.

- **CRITICAL**: 1 (`F-01`) — a constitution MUST violation, so the constitution carve-out applies: it is never a downgrade candidate.
- **HIGH**: 2 (`F-02`, `F-03`) — both `confirm`ed by the independent validation wave.
- **MEDIUM**: 10 · **LOW**: 4 · total 17 findings (cap 50, no overflow).
- **Checklist accountability**: 10 unchecked `[Gap]` items → 6 raised as findings, 4 given an explicit `covered-by` marker; `unchecked + unraised + undispositioned = 0`.

Headline distinction (round 1, so there is no cleared backlog to lean on): the *shape* of the feature is sound — 19/19 FRs reach a task, 31/31 tasks map back, the constitution check re-reads 18/18, decision-tension records pass mechanically — and the defects cluster in one place: **the same fact restated in several artifacts with divergent content**, which is precisely the failure mode this feature exists to remove.

## Metrics

| Metric | Value | Source |
|---|---|---|
| Total requirements | 19 FR + 6 SC + 14 STR | `requirements.md` |
| Tasks | 31 (Setup 2 / Foundational 5 / US1 3 / US2 7 / US3 2 / US4 4 / Polish 8) | `tasks.md` |
| FR → task coverage | 19/19 (100%) | § Traceability, re-derived row by row |
| Task → FR/SC mapping | 31/31 rows carry at least one FR or SC | § Traceability |
| Contract clauses claimed mechanically | 0 of 59 | `account-clause-coverage.py` |
| FRs cited from contract citation groups | 0 of 19 | same run |
| Coverage accountant status | `baseline-missing` (533 errors) | `test-evidence/account-clause-coverage.txt` |
| Feature linkage | 100% (index row + detail file agree) | `features.md` (Total 77 = 77 rows), `features/084.md` |
| Finding classes | inconsistency 9 · underspecification 6 · coverage 1 · feature linkage 1 · duplication 0 | findings table |
| CRITICAL / HIGH / MEDIUM / LOW | 1 / 2 / 10 / 4 | findings table |
| Validators dispatched / confirm / downgrade / reject | 4 / 3 / 1 / 0 (downgrade rate 25%) | § Validation wave |
| Checklist `[Gap]` accountability | 10 unchecked = 6 raised + 4 dispositioned; residue 0 | § Checklist accountability |

## Findings

`propagation_surface` = the downstream artifact that inherits the finding; severity is read from that field. `none` rows are capped at MEDIUM.

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| F-01 | Inconsistency + constitution XIV | `FR-019` / `SC-006` verification → `tasks.md` T029 → implement acceptance | **CRITICAL** | `requirements.md` FR-010, FR-019, N5, SC-006, SC-006 Source; `constitution.md` § XIV | The closed set "既有门禁脚本" is stated four times with three different memberships — FR-010: five incl. `doc-consistency-check.py` (prose says 四个面); FR-019: an unnamed four; N5: four excl. `doc-consistency-check.py`; SC-006: five incl. `closure-acceptance-check.py`, excl. `doc-consistency-check.py`; SC-006 Source: 四个. None of the four is one of § XIV's three legitimate duplicate kinds. | Text-level repair in **requirements**: post the enumeration once (a named set), make FR-019 / N5 / SC-006 / SC-006 Source reference it, and correct the count words. The set that satisfies SC-006's measurement is the five SC-006 itself names (their test-reference union measures 38 files); `doc-consistency-check.py` belongs to the "must not re-judge" side (FR-010). |
| F-02 | Inconsistency (plan artifact vs framework owner) | `tasks.md` § Traceability → implement / closure coverage lane | **HIGH** | `contracts/*.contract.md` clause lines; `shared/definitions/contract-clause-definitions.md` § 1–3; accountant run | The five contracts id their clauses `DS-/HC-/SR-/MB-/DM-nn`. The syntax owner defines a clause id as `C-<digits>` and its § 3 says a **new** contract MUST use only `md-bold-closed`. Consequence, measured: all five parse as `md-none`, `claimed clauses 0`, `[fr-uncovered] fail (19) — 0 of 19 FRs cited from citation groups`. | **plan** (substantive, PLAN CONSTRAINT): re-id the five contracts to `**C-001**…` and update `plan.md` / `tasks.md` references. Alternative adjudication if the orchestrator prefers: keep the prefixes and record an explicit, dated deviation in the syntax owner — but that is an owner edit, not a tasks-side workaround. |
| F-03 | Underspecification (void containment claim) | `SC-005` / `SC-006` verification → `tasks.md` GATE-3/5/6 → implement closure | **HIGH** | `requirements.md` FR-009, SC-005, SC-006, § Measurement Sources | Three containment claims compare against "基线" and `requirements.md` never names the baseline referent (no commit, tree state, or captured list). Under `shared/guidelines/closed-set-claims.md` 要件 1 the claim is void, and because it backs two success criteria the owner's disposition rule makes it HIGH. Downstream referents do exist (`plan.md` EP-003 `171c2ff8` / EP-004; `tasks.md` T001 + GATE-3/5/6 `4b65517c` and `notes/pre-change-measurements.md`) — see the validator boundary in § Validation wave. | **requirements** (text-level): name the referent in each claim and point at the owner of the captured reading (e.g. "baseline = the reading captured by T001 into `notes/pre-change-measurements.md`"), rather than re-deriving a baseline inside the criterion. |
| F-04 | Inconsistency (residual-literal reading) | `tasks.md` T010 / T027(b) → implement US1 reading | **LOW** *(validated: downgraded from HIGH)* | `requirements.md` FR-007(b), SC-002, FR-010; `doc-consistency-check.py --help` | FR-007(b)/SC-002 read "the reused `duplicate` face reports zero hits **for that fact**", but the face has no fact selector and its result depends on the owner path passed (measured: 2 findings / rc 1 with the carrier-vs-engine shape; 0 findings / rc 0 with owner = the carrier). The tool's specified fact attribution is elsewhere (`lookup --fact`, and the `duplicated-fact-literal: <fact>@<path>` reason). | **requirements** (editorial): pin the invocation shape and say fact attribution comes from the checker's `duplicated-fact-literal` reading, so FR-010's "reuse, do not build a second scanner" and SC-002's per-fact counting are not in tension. |
| C-01 | Underspecification (anomaly 2) | `tasks.md` T014–T016 → implement batch 2/3 | MEDIUM | `contracts/migration-batches.contract.md` MB-03, MB-04 | MB-01 gives a per-row `engine side` column; MB-03 names the engine only for the operator-table row and otherwise says "the review engine" / names the carrier alone; MB-04 names engines but not the constant or the read site. T014–T016 therefore instruct the implementer to locate the engine side with `grep` at edit time. | **Not blocking implement** — MB-06 step 1 + MB-09 make the edit-time measurement legitimate and require the corrected face to be recorded in `note`. If the orchestrator wants it closed, it is a **minor** plan edit (fill the `engine side` cell for the seven MB-03 rows and name the constant for MB-04); the finding is therefore an accepted-by-design risk, not a defect to force. |
| F-05 | Inconsistency (anomaly 3) | `tasks.md` T001 → implement attribution / review | MEDIUM | `tasks.md` T001 row tag + § Traceability T001 row | `tasks.md` cites `FR-023` twice; `requirements.md` defines `FR-001..FR-019`. **Adjudication: out-of-range task reference, not a requirements gap** — the content T001 captures is already entailed by FR-011 (batch baseline), FR-018 (081 zero-diff) and SC-006, and requirements deliberately froze 19 FRs (`fr_count` 19 at the plan and tasks gates). | **tasks**: replace `FR-023` with `FR-011, FR-018` in the T001 row and in the Traceability cell (2 edits). The coverage statement "all 19 FRs named" survives: all 19 are named elsewhere. |
| F-06 | Inconsistency (anomaly 4) | `SC-003` reading → `tests/contract/test_harness_triple_structure.py` fixtures | MEDIUM | `requirements.md` § Shared Strings, closing paragraph | The form rule's own partition is corrupted: it says four reasons carry one placeholder, one carries two, and "one has none (`STR-013` has exactly one `<unit>`)" — a clause that contradicts itself, and the authoritative table shows every template carries at least one placeholder (`STR-011` two). SC-003 requires a verbatim 6/6 judgement against this rule. | **requirements** (one-line text repair): state the real partition — five templates with one placeholder, `STR-011` with two, none without. The value table itself is intact, which is why this is not HIGH. |
| E-01 | Coverage input missing (`baseline-missing`) | the fixed coverage step of this and every later stage → implement T002 / closure | MEDIUM | `account-clause-coverage.py` output; `skills/internal/create-tasks/SKILL.md` § notes deliverables; `tasks.md` T002 | `coverage-baseline.txt` does not exist, so the accountant exits 2 with `status: baseline-missing` and cannot judge the delta (533 errors, `baseline-internal existing uncovered: 0`). The tasks stage owns this freeze (create-tasks names `coverage-baseline.txt` as a tasks-time deliverable) and instead deferred it to implement task T002. | **tasks**: either freeze it during the tasks stage per its own duty, or record an explicit dated decision that T002 owns it and that this stage's coverage lane is read as "not yet frozen" — the analyze side MUST NOT `--freeze` (owner rule), so it cannot close this itself. |
| F-07 | Inconsistency (unreproducible measurement) | `plan.md` § D10 / § Evidence List → `tasks.md` GATE-2 selection basis | MEDIUM | `plan.md` D10 + Evidence List ("39 test files"); `research.md` § R7; `test-evidence/plan-readings.txt` § R10 (command elided as `<five script names>`) | "39 files reference the five frozen gate scripts" is not reproducible from any five-name set: measured unions are **38** for SC-006's five, **35** for FR-010's five, and **39** only for the six-script union. The recorded command was elided, so the reading inherits an unknown membership — and F-01 is why. | **plan** (minor, measurement repair): record the five names verbatim with the reading, and correct 39 → the measured value for the set F-01 settles on. Impact is bounded: the *rule* (reference the five scripts, compare at implement start) stays reproducible. |
| C-02 | Underspecification | `tasks.md` T011–T016 → implement (which owner docs flip to pointers) | MEDIUM | `requirements.md` FR-018 | FR-018's affected-owner list is qualified by "至少", so "did we miss an owner document?" has no closing rule; the migration roster (MB-01/03/04) names carriers FR-018 does not (e.g. `templates/review-template.md`, `shared/definitions/probe-definitions.md`, the self-improvement and memory/history carriers). | **requirements**: state the closing rule (e.g. "every carrier named in MB-01/03/04 plus every markdown carrier of an in-scope fact") and drop the open quantifier. Raised from checklist CHK030. |
| C-03 | Underspecification | `tests/fixtures/harness-triple-structure/legacy-project/` + T022 / T030 readings | MEDIUM | `requirements.md` FR-003, FR-013, FR-017; `plan.md` D7 | The degradation annotation has no verbatim owner: FR-013 requires "显式标注" and stresses it MUST NOT read as a pass, FR-017 closes the six reasons, and D7 rules the label an exit-2 *input error* rather than a seventh finding — but no table registers the label's literal, so the "explicit label" a fixture asserts is implementer-chosen. | **requirements**: register the exit-2 label as a Shared String (or say explicitly that its text is free and only its exit code is judged) — the second reading needs one sentence, not a new mechanism. Raised from checklist CHK013. |
| F-08 | Inconsistency | `tasks.md` T020 → `exclusions/*.yaml` shape | MEDIUM | `requirements.md` FR-005 vs § Key Entities | `reason` is a filename in FR-005 (`exclusions/<reason>.yaml`, rows carry `unit`/`carrier`/`anchor`, "three keys complete") and an attribute of the row in § Key Entities ("属性：`unit`、`carrier`、`anchor`、`reason`"). The plan resolved it in favour of the filename (`DS-06`, `data-model.md` E-2), which is why nothing downstream inherits an ambiguity. | **requirements**: drop `reason` from the entity's attribute list (or mark it "filename-borne"). Editorial, one clause. Raised from checklist CHK016. |
| C-04 | Underspecification (edge case) | `tasks.md` T008 → `consumers` shape | MEDIUM | `requirements.md` FR-005, FR-007(c), SC-002 | A fact whose `consumers` lists carriers only has no engine read point, so FR-007(c) can never hold: it stays `pending` forever while SC-002 requires zero `pending` in the in-scope set at closure. The spec does not judge that cell — schema violation, or a legal permanent `pending`? | **requirements**: one sentence — a fact with no engine consumer is a schema error (`consumers` MUST contain ≥1 engine), which also keeps "one fact, one file" honest. Raised from checklist CHK015. |
| C-05 | Underspecification (traceability) | `tasks.md` T005 → SR-07 boundary guard | MEDIUM | `requirements.md` FR-009, FR-019; `contracts/shared-reader.contract.md` SR-07 | The "only one subset parser under `scripts/` and `skills/`, two grandfathered parsers in an allowlist" guard exists only as a plan clause (SR-07). FR-009 states the rule and FR-019 enumerates the test module's legs without it, so the rule has no requirement-level acceptance surface. Downstream is fine (T005 carries SR-07), so the surface is `none` and the cap applies. | **requirements**: add the guard leg to FR-019's enumeration (or cite SR-07 from FR-009). Raised from checklist CHK038. |
| F-09 | Inconsistency | `tasks.md` T005/T006 → implement attribution | LOW | `tasks.md` T005, T006 row tags vs § Traceability | FR-008 is attributed to T005 and T006 in the Traceability table (and the coverage statement says so deliberately) but appears in neither task row's own tag list. All other rows agree with the table. | **tasks**: add `FR-008` to the two row tags, or state once that the table is the sole attribution surface (the banner already says so for clauses). |
| C-06 | Underspecification | `requirements.md` SC-001 → implement determinism readings | LOW | `requirements.md` SC-001, FR-016 | Determinism ("two runs byte-identical") is stated only for `coverage`; `verify` / `lookup` determinism is unstated at requirement level (the plan's HC-13 generalises it). Intent is probably "coverage is the reading that matters", but that is an inference. | **requirements**: one clause in SC-001 or FR-016 scoping determinism (either "all three actions" or "coverage only, by design"). Raised from checklist CHK023. |
| G-01 | Feature linkage | `.specify/memory/features.md` row 084 · `features/084.md` | LOW | index row, detail `Latest Review`, § Related Files | Status is lawful (`Planned` held through tasks/checklist; the state machine owns no transition before implement) and `Total Features` 77 equals 77 rows, so the *status* duty is met. The *stage record* is not: the detail file's latest review and status note stop at `/speckit.plan`, and a second checklist file (`checklists/layer-criteria-2026-11-05.md`) is absent from § Related Files. Same-day dates make the drift invisible mechanically. | `/speckit.feature` or the next stage's wrap-up: append a dated tasks + checklist line to the detail file and add the new checklist path to § Related Files. |

## The five disclosed anomalies (逐条裁决)

1. **Contract clause IDs vs `clause_extract.py`** → **F-02, HIGH, plan-owned defect.** Not an acceptable convention deviation: the syntax owner's § 3 makes the canonical `**C-N**` form a MUST for *new* contracts, and § 2's six forms have no slot for the `DS-/HC-/SR-/MB-/DM-` prefixes, so the five files are not "legacy form" but "no form". Measured consequence: `claimed clauses 0`, `0 of 19` FRs cited, and (with E-01) the coverage lane cannot go green for this feature. Repair stage: **plan** (re-id the 59 clauses and update references) — a substantive change under the active PLAN CONSTRAINT, so it MUST be reopened deliberately, never folded in silently. The tasks stage's `[green:]` non-use is *not* itself the defect (the tag is optional by template); it is the symptom.
2. **MB-03 / MB-04 engine-side precision** → **C-01, MEDIUM, not blocking implement.** MB-06 step 1 + MB-09 already require the edit-time measurement and the recorded correction; T014–T016's `grep` instructions are the sanctioned form for a locator that moves. Filed as an accepted-by-design risk; a **minor** plan edit (fill the `engine side` cells) would close it if the orchestrator prefers precision over edit-time discovery.
3. **`FR-023` cited but undefined** → **F-05, MEDIUM, task reference out of range.** Not a spec gap: the duty T001 performs is already entailed by FR-011 / FR-018 / SC-006, requirements deliberately froze 19 FRs, and no requirement content is missing. Minimal repair: **tasks.md**, 2 edits, `FR-023` → `FR-011, FR-018`.
4. **Shared Strings placeholder self-contradiction** → **F-06, MEDIUM, requirements text.** The authoritative value table is intact; the corrupted sentence is the *partition* ("four with one … one with two … one with none"), which contradicts its own parenthesis. One-line repair in **requirements**. Not HIGH because no fixture can be built wrongly from the table itself — only the prose misleads.
5. **"Existing gate scripts" in four voices** → **F-01, CRITICAL, requirements.** The correct set is not one set but two roles the artifact conflates: the "must not re-judge / must not change" side (SC-006's five plus `doc-consistency-check.py`, whose face is *reused* rather than frozen) and the "zero new failures + zero test-file diff" side (SC-006's five). Measured corroboration: 38 test files reference SC-006's five, 35 reference FR-010's five, 39 only the six-script union (which is where the plan's `39` came from — F-07). One owner enumeration + references is the repair.

## Validation wave

Dispatched under the read-only fan-out carrier (external CLI `qodercli`, one process per finding, in parallel, write tools excluded, `--no-session-persistence`), because the analyzing executor is itself a non-nesting subagent.

| Finding | Severity sent | Verdict | Resulting severity |
|---|---|---|---|
| F-01 | CRITICAL | `confirm` | CRITICAL (constitution carve-out: never downgraded) |
| F-02 | HIGH | `confirm` | HIGH |
| F-03 | HIGH | `confirm` | HIGH |
| F-04 | HIGH | `downgrade` → LOW | LOW |

**Downgrade rate: 1/4 (25 %)** — recorded as remediation advice, not absorbed: F-04's detection over-rated severity by treating the raw face's missing selector as the defect when the chain specifies fact attribution elsewhere (`lookup --fact`, `duplicated-fact-literal`). Detection is tightened to require the *prescribed* invocation in future rounds.

**Evidence boundaries (validator, verbatim where load-bearing)**

- **F-01** `EVIDENCE_SUPPORTED`: "All four enumerated restatements exist in requirements.md and their memberships diverge." · `EVIDENCE_NOT_SUPPORTED`: "The claim does not identify which of the four (or five) lists is the correct one. A8(a) (requirements.md:52–53) records the clarify decision that moved the closure set from four to five to include closure-acceptance-check.py and left doc-consistency-check.py in a different role … so the truth is inferable from the artifact but the requirements.md statements alone do not say which is authoritative. Nothing in the cited artifacts makes this a release blocker."
- **F-02** `EVIDENCE_NOT_SUPPORTED`: "The 513 `[clause-uncovered]` errors and the `baseline-missing` exit 2 are repo-wide, not specific to 084 … In practice the prefix change is what makes every clause unparseable, not just non-canonical, so the effect is stronger than the claim states."
- **F-03** `EVIDENCE_NOT_SUPPORTED`: "The claim's reading of requirements.md holds, but it overlooks that the referent exists downstream. tasks.md:62 (T001) … GATE-3 … plan.md:229 (EP-003) pins commit `171c2ff8` … So the three claims are not void in the repository as a whole; the defect is that the success criteria state void forms and the referent lives only in tasks/plan prose … the finding should not be closed by patching requirements.md alone."
- **F-04** `EVIDENCE_SUPPORTED`: "The core observation holds — the raw `duplicate` face has no fact selector, and SC-002's phrasing implies one." · `EVIDENCE_NOT_SUPPORTED`: the two invocations cited are not the ones any task or contract prescribes; the intended reading (with `--spec-dir`) is vacuous in a different way; fact-level attribution is already specified via `lookup --fact` and `duplicated-fact-literal`; relative-path resolution of the cited runs is unverified.

**Read-only proof**: `git status --porcelain` taken before the wave and after it are identical (18 lines both times) — the wave wrote nothing into the judged tree.

## Coverage summary

| Lane | Reading | Verdict |
|---|---|---|
| FR → task | 19/19 FRs named by at least one of the 31 rows; 31/31 rows carry an FR or SC. Four FRs rest on a single row (FR-001→T004, FR-003→T003, FR-012→T009, FR-014→T003) and all four rows were re-read: each is substantive and its evidence carrier exists | **covered** |
| Task → requirement | every row's parenthetical and Traceability cell resolve to a defined FR/SC after F-05's repair | covered (1 dangling token: F-05) |
| Clause → task (`[green:]`) | 0 claimed; tag legitimately unused (template marks it optional), **but** the underlying contracts are unparseable | **unmeasurable** → F-02 |
| FR cited from clause citation groups | 0/19 | **fail** → F-02 |
| Baseline | `coverage-baseline.txt` missing, accountant exits 2 | **`baseline-missing`** → E-01, remedy: `/speckit.tasks` freezes it (`--freeze`, the analyze side MUST NOT) |
| Zero-finding floor | not triggered (findings exist), and every pass A–I ran; the single-row coverage sample (FR-001/003/012/014) was re-read row by row | n/a |

Not a green claim: the clause lanes are red for a *mechanical* reason (unparseable contracts + unfrozen baseline), not because coverage is absent. The human-readable partition in `tasks.md` § Traceability is complete, and it is the artifact F-02's repair must keep in sync.

## Feature linkage summary

| Check | Reading |
|---|---|
| Index row bound to this spec | `features.md:90` → `084`, status `Planned`, spec path `.specify/specs/084-harness-triple-structure/requirements.md` |
| Detail file agrees on status | `features/084.md` `**Status**: Planned` |
| Header/rows consistency | `Total Features: 77`, 77 matching rows |
| Feature identity in the spec | `requirements.md` § Related Feature: ID 084, name matches the index; binding verdict recorded and evidenced |
| Stage record (judged separately) | stale at `/speckit.plan` → `G-01` (LOW) |
| 081 frozen surface | `git diff --stat 3ffeb26e -- shared/workflow/acceptance-hardening.md .specify/shared/workflow/acceptance-hardening.md tests/contract/test_requirements_checker.py tests/contract/test_checker_form.py scripts/python/validate-requirements.py scripts/python/closure-acceptance-check.py` → **empty** (zero diff on this branch) |

## Constitution alignment

- The plan's `## Constitution Check` renders all eighteen principles, in document order, with names identical to `constitution.md` v1.15.0 — re-read and matched one by one. No row claims a pass contradicted by the artifacts, except as follows.
- **§ XIV (One Source of Truth)** is violated by an artifact of this feature itself: `F-01` (one enumerated set, four statements, three memberships). Reported CRITICAL per the skill's standing rule; the constitution's own carve-out forbids downgrading it, and the repair is an artifact edit, not a principle edit.
- No other principle is crossed. Notably § IV (test-first) is honoured by Tests Mode ON plus the red-first ordering in Phase 2 (T005 before T006/T007); § XVII (directory governance) by same-change registration (DS-11 / DM-11); § XI (Two Hats) by the mirror obligations and the source-route distribution reading.
- Nothing here asks for a constitution change.

## Unmapped tasks

None. All 31 rows map to at least one FR/SC. Two attribution defects are recorded rather than dropped: `F-05` (a row citing a nonexistent FR) and `F-09` (a row whose tag list omits an FR the table attributes to it).

## Checklist accountability (pass H)

Source: `checklists/layer-criteria-2026-11-05.md` (38 items, subagent-unavailable single-context path — re-checked here), `checklists/requirements.md` (all items `[x]`, no `[Gap]`).

| Item | Tag | Disposition |
|---|---|---|
| CHK003 | Gap | `CHK003 disposition: covered-by requirements.md § FR-002` — the three reason glosses ("无机器消费事实" / "无 harness 资产" / "由上级 owner 显式保留为两层") map onto a D2-only / D1-only / by-decree failure, and FR-002 states the conjunctive criterion; sufficiency is explicitly `/speckit.review`'s (SC-004) |
| CHK005 | Gap | `CHK005 disposition: covered-by requirements.md § FR-004 + § Key Entities` — a 流程单元's identity is one of the three carrier surfaces; a markdown file outside them is a carrier (E-1 `consumers`), not a unit, and owes no disposition. The screen *defines* the candidate universe, so "exhaustive" is definitional |
| CHK007 | Gap | `CHK007 disposition: covered-by requirements.md § FR-004 + § Key Entities` — carrier-vs-unit is stated there; the residual weakness (it is stated structurally, not in one sentence) is folded into `C-02`'s recommendation |
| CHK013 | Gap | `CHK013 disposition: raised-as-finding C-03` |
| CHK015 | Gap | `CHK015 disposition: raised-as-finding C-04` |
| CHK023 | Gap | `CHK023 disposition: raised-as-finding C-06` |
| CHK025 | Gap | `CHK025 disposition: covered-by requirements.md § FR-011` — "每批独立可验收" plus "对该批 0 报错、对未迁单元 0 误红" is the requirement-level form; the attribution sentence lives in `MB-05` |
| CHK030 | Gap | `CHK030 disposition: raised-as-finding C-02` |
| CHK037 | Gap | `CHK037 disposition: raised-as-finding F-05` |
| CHK038 | Gap | `CHK038 disposition: raised-as-finding C-05` |

**unchecked(10) + unraised(0) + undispositioned(0) = 10 = raised(6) + dispositioned(4).** Residue: **0**.

Non-`[Gap]` items re-checked with an outcome (not required by pass H, recorded for the reviewer): CHK011→F-06 · CHK016→F-08 · CHK020→F-03 · CHK021→F-01 · CHK029→*pass* (both 081 files are named and the two readings — zero edit vs zero new failure — are stated separately) · CHK036→F-04. The checklist's own priority three all land on findings, which is corroboration rather than coincidence.

## Systemic observations

1. **The feature's requirements exhibit the failure the feature removes.** Four of the seventeen findings are one fact restated across the spec chain with divergent content (F-01 gate roster, F-06 placeholder partition, C-02 owner list, F-05 dangling FR). This is not irony to enjoy — it is a prediction: an artifact that enumerates without an owner cannot be kept consistent by review, and this feature is the mechanism that would catch it later. Expect the same shape in the implement-time carriers until `harness-triple-check.py` runs on the tree.
2. **Readings whose derivation was never recorded are the recurring weak link.** `research.md` § R7/R10 records `39` with the membership elided (`<five script names>`), and no five-name set reproduces it (F-07). The tasks stage warned about exactly this trap in its own Notes. The fix pattern is already in this repo: record the command and its verbatim output, then derive the number.
3. **The tasks stage's compensating decisions are load-bearing and visible.** Two workarounds exist because of the artifacts, not in spite of them: clause attribution moved into § Traceability (F-02's consequence) and zero-new-failure attribution moved to an id-level set difference against an implement-start baseline. Both are defensible; both must survive F-02's repair, which is why the recommendation keeps the table and re-ids the contracts rather than the reverse.
4. **Cost note (`token-efficiency` marker)**: reading all 1 953 artifact lines was necessary for an Exhaustive-tier gate, but the clause/FR lanes and the task↔traceability comparison should have been program verdicts from the start — the accountant and a 20-line comparison produced four of the findings far more cheaply than reading did. Recorded as an avoidable-spend observation for the next analyze dispatch; no token counts are claimed (no source).

## Rerun delta

None — this is the first analysis of feature 084, so there is no prior report to diff against. A round 2 will re-adjudicate these 17 rows and must publish a residue list for any open MEDIUM/LOW row.

## Next actions (not applied)

1. **Reopen `/speckit.requirements`** for a text-level repair pass: F-01 (one owner enumeration + references; correct the count words), F-03 (baseline referents), F-06 (placeholder partition), F-08 (`reason` as filename), C-02 (closing rule for the owner list), C-03 (exit-2 label), C-04 (engine-less `consumers`), C-05 (SR-07 leg in FR-019), C-06 (determinism scope), F-04 (residual reading's invocation).
2. **Decide explicitly on `/speckit.plan`** for the two plan-owned items, because both are substantive under the active PLAN CONSTRAINT: F-02 (re-id 59 clauses `DS/HC/SR/MB/DM-*` → `**C-NNN**` and sync `plan.md`/`tasks.md`) and F-07 (record the five names verbatim; correct `39`). C-01 is a **minor** plan edit if wanted.
3. **`/speckit.tasks`** for the two task-level items: F-05 (`FR-023` → `FR-011, FR-018`) and E-01 (freeze `coverage-baseline.txt` or record the dated deferral), plus F-09 (row tags).
4. **`/speckit.feature`** (or the next stage's wrap-up) for G-01.
5. Re-run `/speckit.analyze` after 1–3; the gate closes when CRITICAL and HIGH are zero, not when the table is quiet.

*Concrete remediation edits are offered here and deliberately not applied — applying them belongs to the owning commands.*

## Evidence pointers

- `.specify/specs/084-harness-triple-structure/test-evidence/account-clause-coverage.txt` — the accountant's full output for this run (533 errors, `status: baseline-missing`).
- `.specify/specs/084-harness-triple-structure/test-evidence/stage-status.md` — § "analyze" E3 row (test budget: `not-run-docs-only`).
- Validation wave: the four transcripts lived in `.specify/.tmp/084-analyze/validators/logs/validate-F-0{1,2,3,4}.{jsonl,live.log,status}` — a sanctioned scratch root (matched by `.specify/.gitignore:30`) torn down at the end of this run. What survives is the part that is evidence: each verdict, its resulting severity, and the validator's two evidence-boundary fields quoted verbatim in § Validation wave above. Dispatch shape, for a re-run: `DISPATCH_CLI_FLAGS="-p --output-format stream-json --permission-mode auto --tools Read Grep Glob Bash --no-session-persistence"` through `.specify/skills/internal/create-team/scripts/dispatch.sh`, one process per finding, all four in parallel; all four returned `exit=0`.
- Commands re-run for this report (all read-only): `check-prerequisites.sh --json` · `flow-class-check.py --action lookup` · `account-clause-coverage.py --spec-dir` · `validate-decision-tensions.py --spec --json` · `doc-consistency-check.py --action verify --faces duplicate` (two invocation shapes) · `grep -rlE` over `tests/` for each gate script (five- and six-name unions) · `git diff --stat 3ffeb26e` on the 081 frozen surface · `git status --porcelain` before/after the validation wave.
