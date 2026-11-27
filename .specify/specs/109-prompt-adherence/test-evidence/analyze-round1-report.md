# Analyze — Round 1 Report: 109-prompt-adherence

**Run**: `r20261127T053750Z-109a` · **Stage**: analyze · **Baseline**: `d3c9dfa4b` (checkpoint 05, checklist U4 pass)
**Spec**: `.specify/specs/109-prompt-adherence/` · **Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）
**Authority**: `.specify/constitution.md` v1.20.0; `.specify/instructions.md`; `requirements.md`; source 092 set at `/storage/project/cloud-native-ai/ai-harness/.ah/specs/092-prompt-adherence/` (behavior provenance, read-only)
**Read domain (15 files, analyzed in full)**: `requirements.md`, `checklists/requirements.md`, `checklists/requirements-quality-2026-11-27.md`, `feature-ref.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `tasks.md`, and the six `contracts/*.contract.md` files. Precedence-only reads: constitution, instructions, `.specify/features.md` row 109, the feature detail `109-prompt-adherence.md`, and the discipline owners cited by the skill (closed-set-claims, one-source-of-truth, objective-analysis-gate, feature-integration, decision-tension, dogfooding § 2.1, script-interface § 2).
**Method**: read-only `/speckit.analyze` round 1 — full severity set; detection direct (same-author condition not established: every artifact was authored by a different stage executor of this line, none by this worker); no artifact was modified.

## Verdict

**0 CRITICAL · 0 HIGH · 13 MEDIUM · 7 LOW — 20 findings.** The chain is coherent at the structural level: 30/30 FRs reach a task and at least one contract clause, 9/9 SCs carry evidence surfaces, 39/39 clauses carry exactly one `[green:]` claim, and the constitution check holds on all 23 principles. The open issues are textual and derivational, not architectural: two identity-edge semantics for the probe/feedback rows, a determinism parameter set that is under-declared, three inherited vocabulary residues, a coverage baseline that the analyze gate cannot consume, and one stale feature-stage record. The headline is **NOT "ready to implement"**: the MEDIUM cluster below should be settled in a remediation round before `/speckit.implement`.

## Findings

| ID | Category | propagation_surface | Severity | Location(s) | Summary | Recommendation |
|----|----------|---------------------|----------|-------------|---------|----------------|
| **G-01** | coverage-gap | analyze coverage gate → tasks/implement clause-coverage accounting (T003) | **MEDIUM** | `coverage-baseline.txt` (absent); `tasks.md:167`; analyze-artifacts SKILL.md:112 | The required clause-coverage accountant cannot judge the feature: exit 2, `status: baseline-missing` (786 errors); `[fr-uncovered]` passes 30/30 and `claimed clauses 39`, but the clause delta lane has no baseline. The freeze is scheduled only as implement task T003, while the skill assigns it to `/speckit.tasks` and requires the state to surface with that remedy. | Re-run `/speckit.tasks` (or a tasks remediation) to freeze `coverage-baseline.txt` before the gate closes; never pass `--freeze` from analyze. If T003's implement-phase placement is kept, record the analyze-side waiver explicitly. |
| **G-02** | coverage-gap | implement coverage accounting (unmapped rows) | **LOW** | `tasks.md:113`; `tasks.md:166-167`; `tasks.md:261`; `tasks.md:126` | T002, T003, T036 appear in no Requirement Coverage Map row and cite no FR/SC on their own lines (T036 anchors only to A-14). | Add them as expected process rows in the coverage note, or anchor T036 explicitly to A-14; do not invent FR anchors. |
| **G-03** | coverage-gap | clause→carrier traceability | **LOW** | `requirements.md:200`; `guards-and-boundaries.contract.md:66`; `tasks.md:263` | FR-024's porting map omits C-043, the only clause without a family/disposition; C-043's carriers exist only in its own clause and the T038 green claim. | Name C-043's carriers (declarations guard + full suite) in FR-024. |
| **I-01** | inconsistency | engine probe-row derivation → SC-001 fixtures → reading output | **MEDIUM** | `requirements.md:139`, `:178`, `:185`, `:210`; `plan.md:56`; `reading-semantics.contract.md:36` | The probe row's state under an explicit `--run` is contradictory: FR-011's positive branch yields `Wired` (registry ships non-empty), while Edge Cases/PA2 say `not_evaluated` is reachable only under `--run` and FR-015 says the row evaluates once, window-exempt. No principle distinguishes run from window for a run-identity-exempt row; the zero-object registry case has no state. | Write the probe-row scope rule as one sentence: explicit `--run` → `not_evaluated`/`no-matching-records`; default/window → evaluate current registry (`Wired`), `Unobserved` only at zero objects; define the zero-object case. |
| **I-02** | inconsistency | engine duplicate disclosure + source references → fixtures | **MEDIUM** | `requirements.md:210`, `:186`; `research.md:44`; `data-model.md:141`; `feedback-utils.py:544` | The probe row's identity is absent per FR-028/E-2 but `registry object_id` per R-2; FR-016/E-8 key duplicates on declared identity fields, so the probe row's key is empty, and feedback entries with missing `run_id` share the empty key. No rule says whether they participate. | Declare the probe row's citation identity (`object_id`) or declare it identity-less with duplicates N/A; state whether empty-`run_id` entries participate in duplicate keying. |
| **I-03** | inconsistency | engine state literal + fixtures | **MEDIUM** | `requirements.md:178`, `:184`, `:226`, `:246`; `declarations-and-vocabularies.contract.md:69` | `not evaluated` (spaced, 9 occurrences) vs `not_evaluated` (16) — FR-011 uses both in one paragraph; the canonical literal is `not_evaluated`. | Normalize the nine spaced occurrences; keep a single canonical spelling (optionally add a Shared Strings row). |
| **I-04** | inconsistency | owner catalog layer cells → declarations guard | **MEDIUM** | `requirements.md:165`, `:188`; `declarations-and-vocabularies.contract.md:40`; `data-model.md:41` | FR-004(d) names layer candidacy `(host / project / both)` while the layers fact is closed at `host-prompt`/`project-rules` and every catalog cell must be a member; `both` has no home. | Drop `both` (or give it a declared home) and use the closed tokens. |
| **I-05** | inconsistency | engine `--check-coverage` → SC-004 verification | **MEDIUM** | `requirements.md:164`, `:245`; `owner-and-catalog.contract.md:44`; `data-model.md:82` | FR-003 mandates four check legs including blind-spot citation (exit 1), but SC-004 lists three legs, C-003's Red-when omits the fourth, and E-5 calls it an "owner-document completeness rule"; the artifacts disagree on its enforcement surface. Tasks (T020) follow FR-003. | Add the fourth leg to SC-004 and C-003's Red-when, or scope it explicitly to the owner guard in FR-003. |
| **I-06** | inconsistency | guard-authoring audit (C-040 vs DoD-7) | **MEDIUM** | `guards-and-boundaries.contract.md:10`; `tasks.md:9`, `:225`, `:250`, `:27` | C-040 says all five guards are authored red-first; tasks declare T023/T024/T030 as migration/regression exceptions placed after the guarded behaviour (sanctioned by create-tasks SKILL.md:166-171). The contract's blanket statement is stale. | Reword C-040 to carry the declared exception, or move the exception into the contract. |
| **I-07** | inconsistency | none (scope-statement wording) | **LOW** | `requirements.md:309`, `:45`; `distribution.contract.md:14`; `tasks.md:181` | Out of Scope allows "框架地图一行" while A-7/C-033/T008 require two rows. | Say "框架地图两行（owner 行 + 读取入口行）". |
| **I-08** | inconsistency | implement optional parallelism | **LOW** | `tasks.md:56`, `:259-260`, `:298` | The Format note says `[P]` appears only at T007/T008 and T023/T024, but T034/T035 also carry `[P]` and the Parallel Opportunities section lists them; six actual `[P]` rows. | Update the legend to T007/T008, T023/T024, T034/T035. |
| **I-09** | inconsistency | owner-document bilingual forms | **LOW** | `requirements.md:24-25`, `:163`, `:52`, `:55` | Both layer definition sites write the Chinese term twice (`宿主提示层（宿主提示层）`); the English names live only in A-14. | Write the bilingual pair at both definition sites. |
| **U-01** | underspecification | engine feedback-row predicates + counts | **MEDIUM** | `requirements.md:207-208`; `owner-and-catalog.contract.md:78`; `feedback-utils.py:544` | Empty or malformed `run_id` is undecided between the two feedback rows: empty is the engine default, and a malformed `gate:` value satisfies neither/both readings; no rule says whether it is an ordinary entry, a gate entry, an invalid source, or outside all rows. | Define the family test as a full-protocol match (and state where non-matching entries go and whether they count in `records_in_scope`). |
| **U-02** | underspecification | longitudinal output → determinism tests | **MEDIUM** | `requirements.md:186`; `reading-semantics.contract.md:54`; `data-model.md:100` | The per-state count listing order is undeclared — in particular the position of the composed `not_evaluated` literal relative to the seven evidence states. | Declare the count order (e.g. seven states in fact order, then `not_evaluated`) in C-023. |
| **U-03** | underspecification | engine CLI + quickstart Scenario 5 + tests | **MEDIUM** | `requirements.md:196`; `quickstart.md:140-141`; `engine-and-read.contract.md:11` | `--check-coverage --json` is exercised by quickstart but no artifact defines the check-mode JSON shape or the combination of `--check-coverage` with `--run`/`--since`/`--until`/`--workspace-root`. | Declare the check-mode JSON shape and the combination rule (accept, ignore, or exit 2). |
| **U-04** | ambiguity | none (edge-case wording) | **LOW** | `requirements.md:150` | "layer-B 行" matches no declared layer token, row id or blind-spot id (inherited from source 092 line 230). | Replace the label with the project-rules row ids or the layer token. |
| **U-05** | underspecification | reading JSON shape → default-scope tests | **LOW** | `data-model.md:152`, `:155`; `requirements.md:184` | E-9 declares `scope.kind` only for `--run` and window invocations; the no-flag default reading (and the no-identity case) has no declared `kind`. | Declare the default `kind` value alongside `resolution: none`. |
| **A-01** | ambiguity | engine CLI failure form → workspace tests | **MEDIUM** | `requirements.md:196`, `:178`, `:195` | A nonexistent/file/ancestor-less `--workspace-root` fits both FR-011 (source-unavailable, exit 0) and FR-022 (invalid argument, exit 2); no artifact chooses. | Choose one form; recommend exit 2 for an invalid target, reserving `source-unavailable` for a valid project with absent stores. |
| **A-02** | ambiguity | engine self-location + both-copies tests | **MEDIUM** | `requirements.md:196`, `:154`; `engine-and-read.contract.md:75`; `dogfooding-definitions.md:108` | The self-location criterion ("own resolved path contains a literal `.specify` component") misclassifies this worktree's framework-source copy, whose absolute path contains `.specify` via `.specify/.tmp/...`; the owner supplies the missing conjunct and the negative case, but the requirement's copy drops it and leaves the base undefined. | Adopt the owner's full rule (the `.specify` component must be the project-runtime component directly above `scripts/python/`; never an ancestor `.specify`); add this worktree as a guard case. |
| **F-01** | feature-relevance | feature status reporting (index/detail consumers) | **MEDIUM** | `.specify/features/109-prompt-adherence.md:57`, `:6`; `.specify/features.md:118` | Status is lawfully `Planned` (header and index), but the detail's Status Tracking still marks `Draft` as "(current — 2026-11-27)" after the plan-stage advance. | Move the current marker to Planned with the plan-stage date, or add the plan-stage entry. |

## Coverage Summary

| Lane | Result | Source |
|------|--------|--------|
| FR → task row | **30/30** (map rows; every FR named) | `tasks.md` § Requirement Coverage Map; machine-checked |
| SC → task row | **9/9** | same |
| FR → contract clause | **30/30** (each FR appears in at least one `Serves:` line) | six contract files |
| Contract clause → `[green:]` claim | **39/39 exactly once** (7/7/10/5/3/7; no duplicate, no miss) | `tasks.md` green claims; machine-checked |
| Clause-coverage accountant | `[fr-uncovered] pass` (30/30 cited), `claimed clauses 39`; clause-delta lane **unjudgeable** (`status: baseline-missing`, exit 2) | `account-clause-coverage.py` run this stage (G-01) |
| Single-task coverage floor sample | **None**: no FR/SC rests on a single task row (minimum 2 rows). Sampled FR-010 (T010/T015), FR-012 (T014/T015), FR-013 (T015/T016); each cited task line carries the mapped obligation. | `tasks.md` |
| Deliverable paths | 15/15 absent (mechanism is new; expected pre-implementation) | `pre-analyze-check --stage tasks` advisories |
| Unmapped tasks | T002, T003, T036 (G-02) | machine extraction |

## Feature Linkage Summary

| Check | Result |
|-------|--------|
| Feature bound | **Feature 109 — Prompt Adherence Evaluation** (new standalone; additive port of external 092/Feature 097; source ID not reused) |
| Index row | `.specify/features.md:118` — `Planned`; Last Updated `2026-11-27`; Spec Path and Details link present |
| Detail file | `.specify/features/109-prompt-adherence.md` — `Status: Planned`; Overview / Key Changes / Implementation Notes / Related Files present; Last Updated `2026-11-27` |
| Reverse cross-reference | `.specify/features/028-feedback-mechanism.md:80` cites Feature 109 and the two consumed feedback rows |
| Delivery surface | 10 rows in `feature-ref.md`; plan § Source Code and tasks § Deliverable Coverage Map (11 families) agree on the same artifacts |
| Stage record | **Stale** `(current)` marker on Draft (F-01); status itself lawful |

## Constitution Alignment

**No constitution conflicts.** All 23 principles (v1.20.0) hold on independent re-read; the plan's 23-row check is accurate on its face. I-06 (C-040 red-first wording vs the tasks' declared migration/regression exception) is a design-contract textual inconsistency, **not** a Principle IV violation: the exception is sanctioned by `.specify/skills/internal/create-tasks/SKILL.md:166-171` for tests that guard already-delivered behaviour, and DoD-7 already permits the declared form. Constitution conflicts remain automatically CRITICAL; none was found.

## Decision-Tension Records (pass I)

`python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/109-prompt-adherence --json` → **status: ok**, 0 errors, 0 warnings, 0 records; all six labels pass (`dtr-anchor`, `dtr-section-missing`, `dtr-record-incomplete`, `dtr-tension-id`, `dtr-rejected-form`, `expected-sacrifice-unmapped`). The plan's compliant `N/A` carries per-trigger justification and consumes the three source-plan tensions (T-001…T-003) as dated records by reference. No finding; the program verdict is consumed, not re-scored.

## Unmapped Tasks

- **T002** — capture pre-change measurements (setup/evidence duty; no FR/SC anchor).
- **T003** — freeze the clause-coverage baseline (the C-6 duty deferred to implement; no FR/SC anchor; also G-01).
- **T036** — register the three glossary proposals (anchored to requirements A-14, not an FR/SC).

No task references an undefined component: every engine, script, test file, fixture root and mirror pair cited by tasks/plan was measured present (or is a declared new deliverable).

## Checklist Accountability (pass H)

`checklists/requirements.md` — all items checked; no unchecked `[Gap]` item.
`checklists/requirements-quality-2026-11-27.md` — 40 items, all unchecked; `[Gap]`-tagged items are CHK007, CHK020, CHK025:

```
CHK007 disposition: raised-as-finding U-01
CHK020 disposition: raised-as-finding U-02
CHK025 disposition: raised-as-finding U-03
```

Count: unchecked `[Gap]` 3 − raised-as-finding 3 − covered-by 0 − undispositioned 0 = **0**.

Adjudication of the 15 candidate confirmation points named in the checklist's closing note:

| CHK | Disposition | Where |
|-----|-------------|-------|
| CHK003 | raised-as-finding **I-05** | blind-spot leg enforcement split |
| CHK007 | raised-as-finding **U-01** | empty/malformed `run_id` boundary |
| CHK008 | raised-as-finding **I-01** | probe-row scope asymmetry; zero-object case |
| CHK011 | covered-by `FR-014` + `data-model E-9` + `I-4` | default scope may resolve an `ev-…` identity; status then follows I-4 (Unobserved rows do not force `partial`). Recorded as a systemic observation, not a finding |
| CHK018 | covered-by `FR-014` + `FR-019` + `FR-022` | digest coarse form fixed by FR-014; exact serialization is engine schema; fact paths are disclosed; a missing fact is exit 2 |
| CHK020 | raised-as-finding **U-02** | state-count order |
| CHK021 | raised-as-finding **I-02** | identity/duplicate keying for probe and empty-identity rows |
| CHK022 | covered-by `FR-026` + `C-045` | replay is defined as an engine rerun over the cited references; the improvement claim stays an evidence-discipline obligation |
| CHK025 | raised-as-finding **U-03** | flag combinations and check-mode JSON |
| CHK026 | raised-as-finding **A-01** | workspace-resolution failure form |
| CHK027 | raised-as-finding **A-02** | Two Hats judgment base |
| CHK028 | covered-by `FR-023` + `declaration_reader.find_repo` + script-interface § 2 | the layer follows the engine's own repo; the version search is bounded by the script's own directory up to the `.git` root, `unknown` otherwise |
| CHK013 | raised-as-finding **I-03** | absence-token spelling |
| CHK037 | raised-as-finding **U-04** | undefined `layer-B` label |
| CHK038 | covered-by `A-5→FR-030`, `A-6→FR-005/FR-006 + Out of Scope + C-033`, `A-8→Out of Scope`, `A-9→FR-026`, `A-18→FR-023`, `A-14→T036` | every behaviour-constraining adjudication has a normative home |

## Systemic Observations

1. **Identity-edge semantics is the weakest surface.** I-01, U-01 and I-02 all concern rows that lack a run identity or whose identity value is empty. The general rules (four-way absence, duplicate keying) are written for identity-bearing records; the two identity-edge rows need their own explicit sentences.
2. **Determinism is strongly mandated, but its parameters are partly undeclared.** U-02 (count order), U-03 (check-mode JSON/flag combinations) and U-05 (`scope.kind` for the default) are output-shape parameters; a strong FR-016 plus undeclared parameters is where two compliant implementations diverge.
3. **Port residue survives the vocabulary tightening.** I-03 (`not evaluated`), I-04 (`both`) and U-04 (`layer-B`) are inherited from source 092; the port's new closed sets (FR-018) make them visible as defects. A port-review habit: re-tighten every inherited vocabulary token against the new closed sets before declaring the port complete.
4. **Two rule surfaces disagree on guard authoring order.** I-06 is the only contract-vs-tasks process conflict; the tasks side is the sanctioned one.
5. **The coverage gate has an unowned freeze.** G-01/G-03: the analyze skill assigns the freeze to `/speckit.tasks`, the tasks file assigns it to implement T003, and the result is that the analyze coverage lane cannot be judged. The disposition is a process choice, not a defect in the accountant.
6. **Feature recording is healthy except one stale marker.** F-01; the index row, detail header, dates and reverse cross-reference all agree.

## Metrics

| Metric | Value |
|--------|-------|
| Total FRs / SCs / contract clauses / tasks | 30 / 9 / 39 / 39 |
| FR → task coverage | 100% (30/30) |
| SC → task coverage | 100% (9/9) |
| FR → contract clause coverage | 100% (30/30) |
| Clause → green claim | 100% (39/39, exactly once) |
| Feature linkage | bound and consistent (one stale marker, F-01) |
| Findings | 20 total — CRITICAL 0 · HIGH 0 · MEDIUM 13 · LOW 7 |
| By category | inconsistency 9 · underspecification 4 · coverage-gap 3 · ambiguity 3 · feature-relevance 1 · duplication 0 · constitution 0 |
| Ambiguity / Duplication / Inconsistency / Critical | 3 / 0 / 9 / 0 |

## Validation Wave

No CRITICAL/HIGH finding was produced, so the independent CRITICAL/HIGH validation wave is **not required** by the skill and was not dispatched; MEDIUM/LOW findings skip validation. Per the assignment, no finding was self-validated as CRITICAL/HIGH. Downgrade rate: not applicable (no wave).

## Residue and Rerun Delta

- **Residue list (round 1)**: none expected; all 20 findings are open and carried into the report table and JSONL.
- **Rerun delta**: not applicable — this is the first analyze report for 109; no prior report exists to diff against.

## Deterministic Checks Run This Stage (read-only)

| Check | Command | Verdict |
|-------|---------|---------|
| Clause/FR coverage accountant | `python3 scripts/python/account-clause-coverage.py .specify/specs/109-prompt-adherence` | exit 2 — `status: baseline-missing` (G-01); FR lane 30/30; claimed clauses 39 |
| Decision tensions | `python3 scripts/python/validate-decision-tensions.py --spec .specify/specs/109-prompt-adherence --json` | exit 0 — status ok, 0 errors, 0 records, six labels pass |
| Tasks structure | `python3 scripts/python/validate-tasks.py .specify/specs/109-prompt-adherence/tasks.md` | exit 0 — PASS, 0 error / 0 warning |
| Requirements structure | `python3 scripts/python/validate-requirements.py .specify/specs/109-prompt-adherence/requirements.md` | exit 0 — status ok, 310 lines / 39 definition rows / 2 shared strings |
| Pre-analyze gate (tasks) | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/109-prompt-adherence --stage tasks --repo .` | `decision=pass`, errors=0, advisories=127 (all missing-path deliverables this feature creates) |
| Store layout fact | `declaration_reader.load_fact(..., 'runtime-store-layout')` | 14 stores, no per-store `root` key — matches A-5/FR-030/EP-007 |
| Evidence seven-state fact | `shared/declarations/facts/evidence-seven-states.yaml` | members and order match C-014 exactly |
| Mechanical coverage extraction | in-line program over the 15 domain files | 30 FR / 9 SC / 18 A / 5 US / 16 edge cases; 39 clauses (7/7/10/5/3/7); 39 green claims; 36/39 tasks mapped |

## Limits

Read-only artifact analysis; the engine, tests and fixtures do not exist yet, so every "will behave/guards" claim was judged against the artifacts and the measured owners, not against an execution. The source 092 set was consulted for provenance on inherited patterns only; the port's own artifacts govern.

## Evidence Pointers

- Findings JSONL: `.specify/specs/109-prompt-adherence/test-evidence/analyze-round1-findings.jsonl` (20 records; `propagation_surface` is the first key of every record)
- This report: `.specify/specs/109-prompt-adherence/test-evidence/analyze-round1-report.md`