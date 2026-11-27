# Context Model Requirements Quality Checklist: 110-context-management

**Purpose**: Requirements-quality checklist (unit tests for requirements writing) for the context-management feature — it tests whether the requirements define the two-axis model, the five materialization forms and their layer legality, the eighteen fact classes and their caps, the composition triggers and composer roles, the audit engine's actions/rules/exit codes/presence vocabulary, the dispatch and recall projections, init/offline behavior, the zero-change owner set and the containment claims — not whether the implementation works.
**Created**: 2026-11-27
**Feature (Requirement Scope)**: [110-context-management](../requirements.md) — Feature 110 `Context Management（上下文管理）`
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md) / [tasks.md](../tasks.md) / [contracts/](../contracts/) — read only to surface requirement gaps, ambiguities, conflicts and traceability issues in the requirements.

**Note**: Every item is a question about the requirement text. An item that could only be answered by running the product is a defect in this checklist. `[Gap]` marks an item whose answer the requirements do not currently provide; those items are also listed under "Unanswerable from requirements.md alone" in Notes for the analyze stage.

## Requirement Completeness

- [ ] CHK001 - Are the two modeling dimensions defined once — each category's membership test, each layer's definition and the composition order — and is every (category, layer) pair's legality derivable from the requirement set? [Completeness, Req §FR-002/FR-003/FR-029]
- [ ] CHK002 - Are all eighteen seed fact classes listed with an assigned layer and at least one named source, and does the 4/7/7 split agree across FR-004, FR-006–FR-008 and A-6? [Completeness, Req §FR-004/FR-006/FR-007/FR-008]
- [ ] CHK003 - Are the layout table's structural constraints (unique class ids across the table, non-empty layers, in-layer row order equal to the roster) each stated with their audit consequence? [Completeness, Req §FR-004/FR-021]
- [ ] CHK004 - Are the five materialization forms each defined with a meaning that distinguishes them from their neighbours — especially `bounded-index` vs `read-in-full` vs `inline-digest`? [Completeness, Req §FR-009]
- [ ] CHK005 - Is the form×layer legality matrix complete for all fifteen form-layer combinations, and do the three legal landing cells plus three forbidden combinations avoid restating a second form value list? [Completeness, Req §FR-009/FR-029]
- [ ] CHK006 - Is every cap-bearing row required to cite the cap owner by path and section, and is the cap-reference cell content for non-cap rows (`pointer`, `runtime-discovery`) specified? [Completeness, Gap, Req §FR-019]
- [ ] CHK007 - Is the durable increment — owner document, four facts, four registration keys, engine, guards/fixtures, ambient section, three framework-map rows — stated as a closed set with no other persistent addition? [Completeness, Req §FR-011/A-11]
- [ ] CHK008 - Is the zero-change owner set enumerated once and closed, with its two allowed additive edits (three map rows, one template section) and a verification surface for every member? [Completeness, Consistency, Req §FR-005/FR-027/SC-008]
- [ ] CHK009 - Are the four governed structures of the concept-pointer slot each assigned a carrier and a named, mechanically readable presence surface? [Completeness, Req §FR-028]

## Requirement Clarity

- [ ] CHK010 - Is "zero copied bytes" given an observable definition — which composition or audit artifact demonstrates that no governance text was copied? [Clarity, Req §FR-007/FR-010/SC-002]
- [ ] CHK011 - Is the `source-reading` digest input tuple fully specified for sources that are absent, unreadable or empty (which tuple fields are present)? [Clarity, Gap, Req §FR-022]
- [ ] CHK012 - Is `present` for `inline-digest` rows explicitly limited to the resident witness, never to the transient digest content? [Clarity, Req §FR-008/FR-020]
- [ ] CHK013 - Is the composition evidence for every trigger defined with its producing invocation and layer scope, including the baseline union used by `source-drift`? [Clarity, Gap, Req §FR-014/FR-016/FR-022]
- [ ] CHK014 - Is the owner document's machine-parseable surface (layout-table anchor, six-column header literal, row and multi-source cell grammar) specified or explicitly delegated to the design artifacts? [Clarity, Gap, Req §FR-004/FR-021]
- [ ] CHK015 - Is the one-to-one mapping between the three concept-pointer entries (glossary / definitions / explanations) and the three project-layer rows stated, so a missing row identifies the unobserved entry? [Clarity, Req §FR-028/SC-010]

## Requirement Consistency

- [ ] CHK016 - Does the category remain strictly derived from the layer — never an independent axis or layout column — consistently across FR-002, FR-004, FR-021 and FR-029? [Consistency, Req §FR-002/FR-004/FR-021/FR-029]
- [ ] CHK017 - Do all seven triggers name a composer, as the closed-set claim asserts — including `task-switch` and `stage-boundary`, whose entries name none — and do those composers resolve through the existing relative role model with no new role value? [Consistency, Gap, Req §FR-014/FR-015]
- [ ] CHK018 - Do the `concept-explanations` row sources in FR-007 and the explanations slot entry in FR-028 name the same carrier set, including explanatory documentation reached through `docs/concepts/documentation-model.md`? [Consistency, Req §FR-007/FR-028]
- [ ] CHK019 - Is the boundary between a declaration-fact unknown/missing member (input error, exit 2) and a layout-table unknown token (finding, exit 1) applied consistently across FR-018, FR-021 and the edge cases? [Consistency, Req §FR-018/FR-021]
- [ ] CHK020 - Are the presence tokens closed at exactly five, with `Unobserved` kept outside that vocabulary and reached only by pointer to the evidence-state owner? [Consistency, Req §FR-020/FR-027/FR-028]

## Acceptance Criteria & Measurability

- [ ] CHK021 - Can every absence-token claim in SC-003 be measured on the named fixture classes with a named source and reason for each row? [Measurability, Req §SC-003/FR-020]
- [ ] CHK022 - Are SC-002's referent trees and exclusion names (interpreter bytecode caches by name; the set of audited trees) closed enough to make the empty-delta claim decidable? [Measurability, Req §SC-002]
- [ ] CHK023 - Is SC-008's baseline referent and comparison unit named for each protected surface, including the recall command, query and output format? [Measurability, Gap, Req §SC-008/RS-004]
- [ ] CHK024 - Is SC-005's offline claim given a counting method (socket opens, bytes transferred) and an explicit scope covering the audit runtime versus install/refresh flows? [Measurability, Ambiguity, Req §SC-005/FR-024]
- [ ] CHK025 - Is SC-007's "exercised" definition applied member-by-member to the three closed domains, and is refusal of unknown/missing members measured at exit 2? [Measurability, Req §SC-007/FR-018]

## Scenario Coverage

- [ ] CHK026 - Is a baseline composition at a new line entry within an existing session mapped to a trigger, given only `session-entry` and `source-drift` refresh the baseline? [Coverage, Ambiguity, Req §FR-012/FR-014]
- [ ] CHK027 - Is the memory-recall projection defined precisely enough to show which existing recall output and which task-layer row carry the concept-pointer triple? [Coverage, Gap, Req §FR-008/FR-028/RS-004]
- [ ] CHK028 - Is the upgrade path for an already-initialized client project specified for the owner document, facts, engine and ambient section? [Coverage, Gap, Req §FR-023]
- [ ] CHK029 - Are the source-drift classes each tied to a named readable project record, rather than a general "recorded change" phrase? [Coverage, Gap, Req §FR-016]
- [ ] CHK030 - Are the fresh-init absence expectations for each fact-class family (tools, memory, docs, state, register) defined beyond the single tools example? [Coverage, Req §US3/Edge Cases/SC-003]
- [ ] CHK031 - Is the feature's edit fan-out to existing files stated as a closed containment claim in the success criteria (map rows, template section, registration keys, generated copies)? [Coverage, Gap, Req §FR-011/FR-023/FR-025/A-11]

## Edge Case Coverage

- [ ] CHK032 - Is the engine's behavior for a present-but-unparsable owner document (missing layout table, malformed row) decided as input error versus finding? [Gap, Req §FR-021]
- [ ] CHK033 - Does the closed usage-error set cover a missing `--action` and an unknown `--action` value? [Gap, Req §FR-021]
- [ ] CHK034 - Is the governing reading specified when a Tool record and runtime path discovery disagree, without introducing a second context source? [Ambiguity, Req §FR-006]

## Non-Functional Requirements

- [ ] CHK035 - Is determinism specified completely — byte-identical reruns on an unchanged tree, no timestamps or host values, workspace-relative paths only? [Non-Functional, Req §FR-022]

## Dependencies & Assumptions

- [ ] CHK036 - Is each missing-sensor adaptation (render owner, seven-component package, absence-word owner, per-slot caps) recorded with its substitute real owner and a no-fabrication rule? [Dependency, Req §A-3/A-8/A-15/FR-019]

## Ambiguities & Conflicts

- [ ] CHK037 - Is the `inline-digest` definition ("only when a task-layer pointer is unreachable") consistent with the two seed rows whose witness is a resident owner path? [Conflict, Req §FR-008/FR-009]
- [ ] CHK038 - Is `Unobserved` given a mechanical carrier — which artifact emits the derived consistency reading, given the manifest's fixed JSON keys contain no such field? [Ambiguity, Req §FR-020/FR-021/FR-028]

## Notes

- **Checklist self-checks**: 38 items (soft cap 40); 38/38 (100%) carry a traceability reference; every item is a question; zero items start with a prohibited verb (Verify / Test / Confirm / Check); all nine quality dimensions are represented. Deterministic lint output: `test-evidence/checklist-self-check.txt`.
- **Focus-area coverage**: two-axis model completeness/consistency → CHK001, CHK005, CHK016; five material forms and layer legality → CHK004, CHK005, CHK037; eighteen fact classes and caps → CHK002, CHK003, CHK006, CHK022; composition triggers and roles → CHK013, CHK017, CHK026, CHK029; audit engine actions/rules/exit codes/presence vocabulary → CHK011, CHK019, CHK020, CHK032, CHK033, CHK038; dispatch/recall projections → CHK009, CHK015, CHK017, CHK027; init/offline behavior → CHK024, CHK028, CHK030; zero-change owner set → CHK008, CHK036; containment claims → CHK007, CHK010, CHK022, CHK031.
- **Unanswerable from requirements.md alone — route to analyze (not defects of this checklist)**: CHK006 (cap cell for non-cap rows carries no stated value; design's `—` is not ratified in requirements), CHK010 (zero-copy has no observable composition artifact), CHK011 (`source-reading` tuple for absent/unreadable/empty sources unstated), CHK013 (trigger evidence invocation and baseline union unstated), CHK014 (layout-table parse grammar unstated or undelegated), CHK017 (`task-switch` / `stage-boundary` name no composer; task-scope composer is not a named role), CHK018 (`concept-explanations` row sources vs slot entry differ), CHK026 (line-entry baseline refresh has no trigger), CHK027 (recall projection carrier boundary ambiguous), CHK028 (upgrade path for existing projects unstated), CHK029 (drift records not named per class), CHK031 (edit fan-out containment absent from SCs), CHK032 (unparsable owner document behavior undecided), CHK033 (missing/unknown `--action` outside the closed usage-error set), CHK034 (Tool record vs runtime discovery conflict undecided), CHK037 (`inline-digest` definition contradicts its two seed rows), CHK038 (`Unobserved` has no mechanical carrier).
- **Partially answerable — analyze should ratify**: CHK008 (guard obligations cover the protocol boundary, not every zero-change owner), CHK022 (fixture family is named only as "具名 fixture 族"), CHK023 (surface named; the recall query/format is not), CHK024 (audit-path offline is stated; install/refresh scope is only implied by SC-005).
- **Answerable as written (confirm quality)**: CHK001–CHK005, CHK007, CHK009, CHK012, CHK015, CHK016, CHK019–CHK021, CHK025, CHK030, CHK035, CHK036.
- Check items off as answered; findings from answering an item belong in the analyze stage's report, not in this file.