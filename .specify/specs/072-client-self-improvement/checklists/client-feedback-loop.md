# Requirements Quality Checklist: Client-Project Feedback & Self-Improvement Loop

**Purpose**: Validate the quality, clarity, completeness and consistency of `requirements.md` for Feature 072 — an instrument that tests the specification ("unit tests for requirements writing"), not the implementation. Focus: client-project hat judgement, three-valued armed state and closed disclosure literals, fifth-step capture with pointer-shaped entries, package-exclusion non-bypassability, the fail-closed SI why-segment, the four loop metrics, cadence without schedulers, command-surface discipline, the four feedback red lines, non-regression of Feature 071's closed surfaces, and two-hat mirror sync.
**Created**: 2026-10-27
**Feature (Requirement Scope)**: Feature 072 客户项目的持续反馈与自我提升 — `.specify/specs/072-client-self-improvement/requirements.md`
**Requirements (What)**: [requirements.md](../requirements.md)
**Specifications (How, context only)**: [plan.md](../plan.md), [tasks.md](../tasks.md), [contracts/](../contracts/) — used for gap-finding only
**Depth**: Standard · **Audience**: Reviewer · **Focus**: top relevance clusters (capture/identity, digest/metrics, red lines/surfaces)
**Generation note**: Same-author condition avoided by generation in a fresh-context subagent dispatch (per `.specify/shared/workflow/objective-analysis-gate.md`); gap-finding pass derived from the contracts and tasks decomposition, not from author memory.

## Requirement Completeness

- [ ] CHK001 - Is the ownership of the client/framework hat judgement pinned to the existing owner (`.specify/shared/definitions/dogfooding-definitions.md` § 2.1), with an explicit ban on a second criterion and on `feedback/`-directory participation? [Completeness, Req §FR-001]
- [ ] CHK002 - Is the capture trigger defined as an explicit conjunction (client project AND applicability `run`), with every other case mandated to disclose rather than silently skip? [Completeness, Req §FR-006, Req §FR-009]
- [ ] CHK003 - Are both halves of the pointer-shaped entry specified: the closed field set (record path, applicability, six severity counts, run id, client unit) AND the prohibited content (review body, per-file verdict list, receipt per-file fields, file counts)? [Completeness, Req §FR-007]
- [ ] CHK004 - Are all four feedback red lines (target closure, fully optional, zero automatic transmission, local workaround value) restated as binding on client-side entries with equal force? [Completeness, Req §FR-024]
- [ ] CHK005 - Is the non-capture disclosure closure fully enumerated (unarmed / ambiguous / no-capture-object / counts-unavailable) with the zero-entry and no-zero-filling rules attached to each? [Completeness, Req §FR-009]
- [ ] CHK006 - Is the verification environment for client-side behavior specified as a simulated client project (no root-level framework source directories, framework-installed `.specify/`), excluding framework-repository self-testing? [Completeness, Req §FR-029]
- [ ] CHK007 - Are the three follow-up carriers closed-enumerated (todo Park mode / new requirements spec / improvement-loop subject) with the exactly-one-carrier rule and a no-fourth-carrier ban? [Completeness, Req §FR-011]
- [ ] CHK008 - Is the digest report's minimum fact set defined (hat + armed state and how it resolved, per-side counts and dispositions, four metric readings) without changing atomic cleanup semantics? [Completeness, Req §FR-013]

## Requirement Clarity

- [ ] CHK009 - Is the armed state defined as an explicit three-valued fact (armed / unarmed / ambiguous) with a closed resolution order (explicit unit > unique external probe object > everything else), resolved once and reused for the whole run? [Clarity, Req §FR-002]
- [ ] CHK010 - Is "exactly one capture per qualifying run" quantified against per-opinion, per-file, and per-severity multiplicity so the one-entry scope cannot be misread? [Clarity, Req §FR-006, Req §FR-004]
- [ ] CHK011 - Is the count set unambiguously pinned at six severity counts including zero values, one-to-one with the existing summary command's six-level vocabulary, with omission and merging forbidden? [Clarity, Req §FR-007, Req §SC-001]
- [ ] CHK012 - Is the "probe registry unavailable" case (un-upgraded `.specify/` runtime) distinguished from "no probe object" within the unarmed classification, each with its own one-time guidance target? [Clarity, Req §FR-002, Req §Edge Cases]
- [ ] CHK013 - Is the disclosure's co-visibility rule specified unambiguously — the disclosure appears in the run's human-facing conclusion and is visible together with the run's applicability value? [Clarity, Req §FR-009]
- [ ] CHK014 - Is the third metric's closure criterion ("routing ≠ completion") defined as owner-file change evidence, with disposition markers, `carried-by-spec-*` rows and `open-unverified` rows explicitly named as non-evidence? [Clarity, Req §FR-021]

## Requirement Consistency

- [ ] CHK015 - Is unit naming consistent across the specification — `custom:<owner>/<name>` with `custom-unit` type in FR-003 and FR-004, and the same form mandated in the Dogfooding Loop B recipe rewrite? [Consistency, Req §FR-003]
- [ ] CHK016 - Are the disclosure literals consistent between the requirement closure (FR-009's four non-capture tokens plus the armed token) and the success-criterion judgement surface (SC-002's exit-code + named-disclosure check)? [Consistency, Req §FR-009, Req §SC-002]
- [ ] CHK017 - Is the amendment to the preceding feature's closed surfaces consistent: exactly one explicit revision (non-interactive path four steps → five, with reason and cost recorded at the amendment site) and every other closed surface preserved verbatim? [Consistency, Req §FR-005, Req §FR-025]
- [ ] CHK018 - Is the no-new-command-surface constraint consistent with the responsibility allocation — review command carries capture (+ optional `--client-unit`), feedback command carries digest/carriers/metrics, improve command carries the client-subject loop, and any unmappable entry must be reported as a decision gap rather than silently adding a command? [Consistency, Req §FR-026]
- [ ] CHK019 - Is the "not evaluated" semantics consistent between metric reporting (any zero/missing denominator → `not-evaluated` with reason, never 0 or 100%) and User Story 5's acceptance scenarios? [Consistency, Req §FR-023]

## Measurability & Acceptance Criteria Quality

- [ ] CHK020 - Can SC-001's "six counts equal item-by-item" be objectively judged by deterministic command-output comparison (entry-list JSON filtered by run id vs summary command output), without a human reading entry bodies? [Measurability, Req §SC-001]
- [ ] CHK021 - Can SC-005's read-built guarantee be verified by a path-set comparison of the store tree before and after reporting, plus identical readings from two reports over the same records? [Measurability, Req §SC-005]
- [ ] CHK022 - Can SC-007's non-regression claim be verified by verbatim text/structure assertions on the step enumeration, closing-step set, three-unit census, receipt field block and process-report field list? [Measurability, Req §SC-007]
- [ ] CHK023 - Is each of the four metrics' numerator and denominator mechanically derivable from existing records only (no new aggregates, no LLM-derived values), with named data sources? [Measurability, Req §FR-021, Req §FR-022]
- [ ] CHK024 - Is the red-first evidence requirement for the five behavior groups stated with a mechanical record shape (command line, exit code, failure count) so "recorded failing run" is decidable? [Measurability, Req §SC-006]

## Scenario & Edge Case Coverage

- [ ] CHK025 - Are all three armed-state branches (armed / unarmed / ambiguous) each covered by an acceptance scenario asserting zero-entry behavior, non-blocking exit, and the named disclosure literal? [Coverage, Req §SC-002]
- [ ] CHK026 - Are the three capture invariants (idempotent, non-blocking, non-overreaching) each individually covered by a requirement clause rather than collapsed into one blanket statement? [Coverage, Req §FR-008]
- [ ] CHK027 - Are both hat directions covered by success criteria — framework side polluted by no client defect, client side leaking through no channel — including the vendored-framework-source edge case that must take the framework branch and disclose its basis? [Coverage, Req §SC-003, Req §Edge Cases]
- [ ] CHK028 - Are edge cases defined for: summary exit 1 (gate rejection, capture still runs) vs exit 2 (unparseable, zero entries + counts-unavailable) vs engine write refusal; same-second duplicate capture; and a client unit disappearing from the registry afterwards? [Edge Cases, Req §Edge Cases, Req §FR-008]
- [ ] CHK029 - Are the history-related exclusions specified — no backfill of pre-landing review records, legacy entries stay readable and unrewritten, and the metric window statement covers only post-landing runs? [Edge Cases, Req §FR-020]
- [ ] CHK030 - Is the multiple-client-units case specified — only the explicitly selected unit is captured, other units present in the store MUST NOT be captured "because they are also there"? [Edge Cases, Req §Edge Cases]

## Non-Functional Requirements

- [ ] CHK031 - Is "continuous" explicitly bounded as capture-on-every-qualifying-run + existing non-blocking threshold prompt + explicit triggers, with an absolute ban on schedulers, resident processes, timers and background tasks? [Non-Functional, Req §FR-019]
- [ ] CHK032 - Is the edit-surface constraint specified — framework sources are the only edit surface, runtime projections and compiled artifacts must be produced by the existing regen/mirror mechanisms and never hand-edited (probe registry recompiled before sync if touched)? [Non-Functional, Req §FR-027]
- [ ] CHK033 - Is the client-neutrality constraint on distributed surfaces specified — no new copy may reference this framework project's spec keys, feature numbers or register entries, and the two existing negative assertions must survive verbatim? [Non-Functional, Req §FR-028]

## Dependencies & Assumptions

- [ ] CHK034 - Are the load-bearing dependencies on existing owners documented and validated by reference (hat owner, probe registry and its injection capability, carrier owners, run-determination engine's fail-closed source contract, existing exclusion in the packaging path) rather than redefined inline? [Dependency, Req §FR-001, Req §FR-002, Req §FR-015]
- [ ] CHK035 - Are the assumptions about the client project's form recorded (framework-installed `.specify/` runtime, unmodified engine/registry/skill mirrors) so behavior outside that form is out of scope rather than undefined? [Assumption, Req §Assumptions]
- [ ] CHK036 - Is the dependency on the preceding feature's open recommendation items handled explicitly — they stay open, are not implemented, and the capture counts deliberately take opinion-level counts so the metrics do not depend on the undecided items? [Dependency, Req §FR-025]

## Ambiguities & Conflicts

- [ ] CHK037 - Is the optional review-command parameter's semantic boundary ambiguity-free — it disambiguates the armed state and takes precedence over auto-resolution, but never waives the probe-object existence check that is a necessary condition for armed? [Ambiguity, Req §FR-002, Req §FR-026]
- [ ] CHK038 - Is the derivation of the run identifier (the idempotency dimension of the one-unit-one-run scope) pinned to a deterministic source, or is it an ambiguity that plan-level resolution leaves unguarded at requirement level? [Ambiguity, Req §FR-004, Req §FR-007]
- [ ] CHK039 - Is the fourth metric explicitly labeled a coarse proxy (file, severity) pair-matching that MUST NOT be presented as a defect-recurrence rate, with the proxy label travelling with every report? [Ambiguity, Req §FR-021, Req §FR-023]
- [ ] CHK040 - Is the single-refinement direction rule free of conflict — an entry judged "actually this project's own config problem" may move framework-ward but never external-ward, and the move must be reported? [Conflict, Req §Edge Cases]

## Notes

- Check items off as completed: `[x]`; add findings inline.
- Every item is a question about the requirement text; none is answerable only by running the product.
- Traceability: 40/40 items carry a `[Req §...]` reference (100%, floor 80%); items CHK005/CHK016/CHK025 additionally cross-check the shared-string table (`[[STR-003]]`…`[[STR-010]]`).
- Deterministic self-check (numbering continuity, traceability rate, soft cap, prohibited-pattern scan) archived at `../test-evidence/checklist-selfcheck.txt`.
