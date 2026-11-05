# Requirements-Quality Checklist: Self-Explanatory Framework Integration（不言自明的框架集成）

**Purpose**: Test the **requirements text** of Feature 082 — whether every obligation it states is
decidable, traceable, internally consistent and complete against the plan-stage gap surface. This
instrument never grades `plan.md` or `tasks.md`; those two are read only to expose what
`requirements.md` leaves unnamed.
**Created**: 2026-11-05
**Feature (Requirement Scope)**: 082 Self-Explanatory Framework Integration（不言自明的框架集成）
**Requirements (What)**: [../requirements.md](../requirements.md)
**Specifications (How, context only)**: [../plan.md](../plan.md) · [../tasks.md](../tasks.md) · [../contracts/](../contracts/)
**Depth**: Standard · **Audience**: Reviewer · **Focus clusters**: (1) pointer/authority discipline and
publication reach of requirements, (2) decidable acceptance for the guard-test requirements

**Note**: Each item is answerable by reading the requirement text, never by running the product. A
`Yes` means the requirements already define it; a `No` is a finding against `requirements.md` — repair
it by revising the requirements, not by changing this checklist.

## Requirement Completeness — publication and naming obligations

- [ ] CHK001 - Do the requirements state whether the framework's own Documentation Map must gain a row
      for the concept owner document — or that the decision is deliberately not to add one?
      [Completeness, Gap; anchored on Req §FR-004]
      <!-- Context only, not the obligation: plan C-19 / instructions-propagation.contract.md requires the
      caller to record that decision, and no FR carries it. -->
- [ ] CHK002 - Do the requirements state whether the three deliverable documents (`STR-002`, the
      practice owner, the optimization-workflow owner) must be registered in the packaged-resource
      inventory (i.e. whether the package specification enumerates `shared/`) — or that they ship by
      tree copy without per-file registration? [Completeness, Gap; anchored on Req §FR-007, Req §RS-004]
      <!-- Context only: plan EP-002 cites the copy site in src/specify_cli/__init__.py, and no FR states
      whether that path needs an inventory entry. -->
- [ ] CHK003 - Is the new file `shared/workflow/best-practice-optimization.md` (the optimization-workflow
      owner) given an explicit naming obligation — a canonical title or term binding — as `STR-003` gives
      the concept? [Completeness, Gap; anchored on Req §FR-006, Req §A2]

## Requirement Completeness — guard-test obligations

- [ ] CHK004 - Do the requirements assign an owner and a carrier to the three out-of-scope guard suites
      this feature depends on (`test_instructions_size_budget.py`, `test_glossary_mechanism.py`, the
      reused-and-unmodified `test_mirror_parity_suite.py`), i.e. state that they must stay green without
      being edited? [Completeness, Gap; anchored on Req §SC-004, Req §SC-007]
      <!-- Context only: the contracts name these carriers; no FR or SC does. -->
- [ ] CHK005 - Do the requirements state whether the mutation legs (each new guard's proof that it can go
      red) are a delivery obligation visible on every affected requirement, rather than only in `SC-006`
      and the plan-stage contracts? [Completeness, Req §FR-008, Req §FR-009, Req §FR-010, Req §SC-006]
- [ ] CHK006 - Do the requirements state the completeness obligation behind `SC-006` — that a mutation leg
      exists for **every** new guard, and how many there are — or is "至少各有一个" left as the full
      extent? [Completeness, Clarity, Req §SC-006]
- [ ] CHK007 - Is the obligation to *record* pre-existing failures and stage evidence (baseline,
      mutation-leg runs, budget readings, no-new-failure-node comparison) assigned to a requirement, as
      opposed to being implied by the `SC-00N Source` lines? [Completeness, Gap; anchored on Req §SC-002,
      Req §SC-006, Req §SC-009]
- [ ] CHK008 - Are the requirements silent on the feature-lifecycle obligations this integration implies
      (the feature index row and detail-document status advance), and is that silence deliberate?
      [Completeness, Gap; anchored on Req §Related Feature]

## Requirement Clarity

- [ ] CHK009 - Is "MUST NOT 复制 owner 的完整定义" given a decidable boundary — what counts as a copy versus
      a summary (`FR-001`, `FR-004`), and what the maximum permitted quoted length is? [Clarity, Ambiguity;
      Req §FR-001, Req §FR-004]
      <!-- Context only: plan C-20 makes it decidable ("none of the owner's level-2 heading lines appear on
      the surface") and C-21 bounds the summary at <= 2 sentences; neither bound is stated in the requirements. -->
- [ ] CHK010 - Is "**最小必要幅度**" for raising `INSTRUCTIONS_BUDGET_BYTES` quantified with a rule, so two
      readers compute the same new constant? [Clarity, Measurability; Req §FR-004, Req §A10, Req §SC-009]
      <!-- Context only: plan R-1 / T-001 define the rule (raised to S + 1024 rounded up to the next multiple of
      1024, at least 1 KiB headroom); the requirements text carries only the adjective "最小必要". -->
- [ ] CHK011 - Is "记录理由" for the budget raise quantified — which fields the record must carry (old
      value, new value, measured live size, reason, raise rule) and where the record lives? [Clarity;
      Req §FR-004, Req §A10, Req §SC-009]
- [ ] CHK012 - Is "该小节的**位置**" specified, or is the reader left to invent a placement that the
      generator's additive reconcile will then make permanent? [Clarity, Gap; anchored on Req §FR-004,
      Req §FR-005]
      <!-- Context only: contract C-12 fixes placement ("immediately after the One Source Of Truth /
      Closed-Set Claims / Grounded Naming cluster, before Bilingual Expression"); no FR states it. -->
- [ ] CHK013 - Is the meaning of "**保留旧小节**" / "增量注入" given a decidable test form in the
      requirements — the fixture shape and the byte-identity expectation for pre-existing sections?
      [Clarity, Measurability; Req §FR-005, Req §FR-009, Req §A9]
- [ ] CHK014 - Is "**真实树上同组测试全绿**" (`SC-006`) reconcilable with the feature's own knowledge that one
      pre-existing node is red, and does any requirement carry that exception? [Ambiguity, Conflict;
      Req §SC-006]
      <!-- Context only: plan EP-003 records test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
      as red at stage base, decided as `fallback` and to be named in every stage's evidence; `SC-006` and the
      requirements text carry no such exception. -->
- [ ] CHK015 - Is "至少各有一个契约测试变红" adequate as the acceptance form for a suite known to go red
      **before** the change (a vacuous red), and do the requirements distinguish a red that proves the
      guard from a red that proves nothing? [Ambiguity, Measurability; Req §SC-006, Req §FR-008]

## Requirement Consistency

- [ ] CHK016 - Do the two places that own "the pointer must be resolvable in a client runtime" — `A11`
      (client-facing outputs use `STR-004`, the runtime path) and `RS-004` (the distribution path) — align
      with `STR-002`'s declaration in `Shared Strings` that it is consumed by `FR-007` and `SC-005`, which
      talk about distribution rather than about a pointer? [Consistency, Traceability; Req §A11,
      Req §RS-004, Req §Shared Strings]
- [ ] CHK017 - Are the guard-test obligations in `FR-008` / `FR-009` / `FR-010` stated at the same level of
      determination, given that `FR-010` explicitly delegates its enumeration to an existing suite
      (`MIRROR_PAIRS`) while the other two spell out their assertions inline? [Consistency; Req §FR-008,
      Req §FR-009, Req §FR-010]
- [ ] CHK018 - Do the requirements keep a single position on whether a rendered template count or a heading
      set is the truth for the mandate list — i.e. do `A4` (never hard-code a numeral) and `FR-008`
      (`TEMPLATE_COUNT` / `LIVE_COUNT` / `COMMAND_COUNT` each +1) agree on what those constants count?
      [Consistency, Ambiguity; Req §A4, Req §FR-008]

## Requirement Traceability

- [ ] CHK019 - Does every `FR-001…FR-012` terminate in at least one `SC-NNN`, and does every `SC-NNN` name
      the requirement it measures? [Traceability, Req §Success Criteria]
      <!-- Determined by collection: FR-002 and FR-003 are named by no SC (requirements.md § Success Criteria, scanned
      2026-11-05); FR-003's subject is reached only through SC-002, which does not cite it. -->
- [ ] CHK020 - Do the requirements state which clause makes the mandate-list entry (`FR-002`) and the live
      constitution amendment (`FR-003`) observable as outcomes, not merely as tasks? [Traceability, Gap;
      Req §FR-002, Req §FR-003]
- [ ] CHK021 - Is the reason `SC-002` is `supporting` and `SC-001` is `final` stated — i.e. is the
      `Path` vocabulary (`final` / `supporting`) defined anywhere the requirements point at?
      [Traceability, Clarity; Req §SC-001, Req §SC-002]
- [ ] CHK022 - Does the requirements text carry the four contract-file names its guard requirements lean on
      (`FR-010` names `test_mirror_parity_suite.py` and `MIRROR_PAIRS` but not the contract document), so a
      reader can walk from FR to guard without the plan? [Traceability; Req §FR-008, Req §FR-009,
      Req §FR-010, Req §FR-011, Req §FR-012]

## Scenario & Edge-Case Coverage

- [ ] CHK023 - Are zero-state and first-run scenarios covered in the requirements — a project whose live
      instructions file does not exist yet, and a client project initialised *before* this feature (where
      the section and the mirror arrive by refresh rather than by init)? [Coverage, Edge Case;
      Req §Edge Cases]
- [ ] CHK024 - Are recovery requirements defined for the two repair paths the edge cases imply — mirror
      drift repaired by `--write`, and a live constitution whose Sync Impact Report is missing or malformed?
      [Coverage, Edge Case; Req §Edge Cases, Req §FR-003]
- [ ] CHK025 - Are the requirements explicit about the **partial-failure** shape of `FR-006` (one pair
      byte-identical, another drifted) — must the check fail the whole set, and does the requirement say so?
      [Coverage, Edge Case; Req §FR-006]
- [ ] CHK026 - If the installed `specify` entry point predates this change, is the accepted weaker reading
      of `SC-005` (path and landing directory work, the three documents cannot yet arrive) stated in the
      requirements, not only in the tasks-stage environment notes? [Edge Case, Assumption; Req §SC-005,
      Req §RS-004]
      <!-- Context only: tasks.md § Environment Prerequisites records the installed CLI as `partial` for exactly
      this reason; requirements.md's SC-005 states the full outcome without the qualifier. -->

## Non-Functional Requirements

- [ ] CHK027 - Is the byte-budget constraint stated as one requirement with its operator semantics (a size
      equal to the budget already counts as exceeding it), or must the reader derive it?
      [Measurability; Req §FR-004, Req §SC-009]
- [ ] CHK028 - Is "MUST NOT 复制一份新的对表" (`FR-010`) given a decidable form — what counts as a second
      table versus a reference? [Measurability, Clarity; Req §FR-010]
- [ ] CHK029 - Is the reuse obligation in `FR-012` ("MUST NOT 新建独立链接检查引擎") decidable — where the
      boundary runs between a link assertion inside an existing suite and a new checker? [Clarity;
      Req §FR-012]
- [ ] CHK030 - Are the non-functional properties this feature is *not* required to meet (runtime
      performance, availability, security of the new documents) explicitly declared out of scope rather
      than left unmentioned? [Completeness, Gap; anchored on Req §Performance Goals — plan only]

## Dependencies & Assumptions

- [ ] CHK031 - Is the frozen-entry-point dependency (the packaged CLI resource tree) recorded as an
      assumption with its consequence, given that `RS-004` is `in-scope` but the acceptance ran against a
      pre-feature package? [Dependency, Assumption; Req §RS-004, Req §SC-005]
- [ ] CHK032 - Does every `EP-00N` premise cited in the runtime-stack table's `Premises` column have a
      corresponding assumption or edge-case entry in the requirements? [Dependency, Assumption;
      Req §Runtime Stack & Dependency Ownership]
      <!-- Determined by collection: RS-001…RS-003 cite EP-001 and RS-004 cites EP-002; requirements.md § Assumptions
      A1–A11 contains no A-row for either premise (scanned 2026-11-05). -->
- [ ] CHK033 - Is the glossary-promotion dependency (`A6`: `status=proposed` until the user confirms)
      carried as a user-actionable step somewhere in the requirements' acceptance surface, rather than only
      as a prohibition in `FR-011`? [Dependency, Assumption; Req §A6, Req §FR-011, Req §SC-007]

## Ambiguities & Conflicts

- [ ] CHK034 - Is the retired name "望文生义" given an allowed appearance set — variants column only, or also
      in prose about the retirement? [Ambiguity; Req §FR-011, Req §A6, Req §Edge Cases]
- [ ] CHK035 - Does the requirements text fix the **heading level** of the new surface entries (the
      constitution principle's level, the instructions section's level), so "小节" and "原则" cannot be
      satisfied at the wrong granularity? [Ambiguity, Measurability; Req §FR-001, Req §FR-004]
- [ ] CHK036 - Are the requirements explicit about whether the constitution transaction and the budget
      raise must land in the **same** commit/change, or may be split? [Ambiguity, Consistency;
      Req §FR-003, Req §FR-004, Req §A10]

## Notes

- **Purpose boundary**: no item above can be answered by running the product; each is a judgement about
  `requirements.md`'s text. Mechanism detail in the `<!-- Context only -->` comments is quoted from
  plan-owned artifacts to make a gap visible — it is never itself the graded object.
- **Traceability**: `[Req §…]` / `[Gap]` / `[Ambiguity]` / `[Assumption]` / `[Coverage]` markers appear
  on all 36 items (100 %, floor is 80 %) — verified by re-parsing this file with continuation lines
  joined, not by eye.
- **Same-author detection**: the gate is binding for `/speckit.checklist`
  (`tests/contract/test_objective_analysis_gate.py` `BINDING` roster). This run's artifacts were
  produced by a **different run** from the one now auditing them, and the dispatch brief does not state
  whether a `DECLARED_CHECK` extends the gate's firing condition past "same session, same author".
  Reading the weaker side of the doubtful-strict rule, gap detection was additionally run in a **direct
  bounded read** rather than delegated to fresh-context subagents. Every gap item above is therefore an
  inline-detected row, and the weaker evidence path is kept visible here instead of passing as the
  delegated path. Items most exposed to this limitation: CHK001, CHK002, CHK012, CHK026 (their subject
  lives in plan/tasks, not in `requirements.md`). If a later review rules that the gate does fire here,
  this checklist owes a fresh-context detection pass and a re-issued file — never an in-place refresh.
- **Counts measured at generation** (2026-11-05): 36 items; 8 completeness (3 publication/naming +
  5 guard-test), 7 clarity, 3 consistency, 4 traceability, 4 scenario/edge-case, 4 non-functional,
  3 dependencies/assumptions, 3 ambiguity. Input facts re-derived mechanically this run:
  `requirements.md` 12 FR / 9 SC / 4 Shared Strings rows / 11 assumptions; `tasks.md` 53 task rows;
  34 contract clauses each claimed exactly once by a `[green:]` marker, 0 unclaimed, 0 phantom;
  6 mutation legs (M-1…M-6); `STR-001` found on 0 of the four landing surfaces (pre-change, as
  expected); template roster 17 / live roster 18; live instructions 32,739 B against a 32,768 B
  constant; `sync-mirrors.py --check` `ok` on all six pairs.
