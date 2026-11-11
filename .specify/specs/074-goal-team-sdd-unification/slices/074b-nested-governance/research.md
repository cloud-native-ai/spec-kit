# Research: 074b-nested-governance

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Parent design (authority)**: `.specify/specs/074-goal-team-sdd-unification/` — read-only for this slice
**Sibling slice (implemented, read-only)**: `.specify/specs/074a-authorized-routing/`, merged at `9360718a1`

Phase 0 rulings RB1–RB10. Each ruling states the decision, the measured evidence it rests on (a
re-runnable command or a `file:line` anchor), and the alternatives rejected. Nothing here restates a
fact owned elsewhere: the routing input domains, verdict table, precedence and reason-code vocabulary
are owned by `shared/definitions/sdd-routing-definitions.md` (delivered by `074a` and cited, never
copied); the stage roster is the driver's; the handoff field set is
`skills/external/sdd-loop-driver/references/nested-invocation.md` (delivered by `074a`). This file
records only *why* the projection around those owners has the shape it has.

**Phase 0 evidence path (degraded, disclosed)**: this environment exposes no subagent dispatch
capability and the stage brief fixes `decomposition=single-package` with no subagent dispatch, so the
codebase exploration pass ran as a bounded manual probe (grep for headings/symbols plus targeted
excerpt reads under the token-efficiency discipline) rather than as an Explore-subagent pass. Every
ruling therefore carries a re-runnable command or a `file:line` anchor instead of a subagent digest.

---

## RB1 — Projection with a local id space, tagged to the parent clause it projects

**Decision**: the slice owns a continuous local clause set `C-1`…`C-30` across three contract files,
a local entity set `E1`…`E8`, and a local validation set `V-1`…`V-12`; every clause, entity and rule
that projects a parent clause carries its source tag (`parent C-nn` / `父 E-n` / `parent V-nn`). Only
the 30 parent clauses that serve this slice's eight requirement entries are claimed; the rest stay
`074a`'s and are cited by path.

**Evidence**:
- `074a-authorized-routing/plan.md:266-290` is the authority for the split. Its table names the
  parent clauses deferred to this slice (C-25, C-26, C-27, C-33, C-43, C-44, C-47, C-48, C-49, C-50,
  C-51, C-52, C-53, C-54, C-55, C-56, C-57, C-61, C-62, C-63, C-65) grouped by the parent FR each
  serves, and its prose records the two partial facets (parent C-54's report-section facet, parent
  C-66's Stage-vocabulary facet) that `074a` deliberately left here.
- **Disclosed inconsistency in the read-only sibling, recorded not repaired**: that table lists 21
  clause ids while its opening sentence says "20"; and the Stage-vocabulary facet of parent C-66 is
  named in the prose but absent from the table. This slice claims per the prose and the parent's own
  FR→clause rows (parent C-66 serves parent FR 022, which is this slice's FR-003), and does not edit
  `074a`'s artifact to reconcile the count — a correction there would touch another slice's committed
  plan, while nothing downstream depends on the integer.
- The parent's own FR→clause rows confirm the grouping: parent FR 020 → C-50…C-52, FR 021 →
  C-47…C-49 + C-53 + C-54, FR 022 → C-55 + C-66, FR 023 → C-25 + C-26 (+ C-60, claimed by `074a`),
  FR 024 → C-56 + C-57, FR 026 → C-27 + C-65, FR 027 → C-33 + C-43 + C-44 + C-61 + C-62, FR 028 →
  C-63 + C-67 (parent `feature-ref.md:62-91`).
- `074a` already claimed parent C-15/C-16/C-30/C-60 and the parent FR 013 / parent FR 018 facets of C-54/C-66
  (`074a-authorized-routing/feature-ref.md:63-89`), so this slice references them instead of
  re-claiming them.

**Rejected**: (a) inheriting all 67 parent clauses — 37 of them serve requirement entries this slice
does not carry, and re-claiming them would make two slices the owner of one obligation; (b) reusing
the parent ids verbatim with gaps — the slice's FR/SC/STR space is already local (requirements
§ 编号口径), and a gapped C-space reads as a deletion rather than a projection; (c) mirroring the
parent's five contract files — their grouping is by theme, while this slice's attribution is per
requirement entry (D-1), so the file set follows this slice's three behaviour groups.

## RB2 — The report section lands in the report contract's single owner; `run-team` is not edited

**Decision**: the one mandatory `## Nested SDD Runs` section is added to
`skills/internal/create-team/SKILL.md` § Report contract, and to no other document. The `run-team`
skill keeps delegating its report duty to that owner.

**Evidence**:
- `skills/internal/create-team/SKILL.md:53-63` is the report contract: the report path, the mandatory
  section list as one line (`## Result Summary ## Deliverables ## Verification ## Execution Detail ##
  Run Workspace ## Summary`), the summary vocabulary, and the first-activation line.
- `skills/internal/run-team/SKILL.md:66` already carries the delegation — "报告契约真源:
  create-team SKILL.md → Report" — plus the ledger field the attribution row uses
  (`"target_ref": "T-<nnn>"`), so the supervisor-side obligation already exists and needs no second
  statement.
- `grep -rn "Nested SDD Runs" skills/ templates/ shared/` returns zero hits in shipped surfaces at
  plan time; the only occurrences are `074a`'s test negative
  (`tests/contract/test_nested_sdd_invocation.py:560`) and specification text, which is exactly the
  D-3 hand-over.

**Rejected**: (a) editing both `create-team` and `run-team` — the second edit would restate one
section in two owners, the duplication the one-source-of-truth principle forbids; (b) a new
`references/` file carrying the section — the contract grammar is a fenced report skeleton inside the
owner, and a second carrier would split one obligation; (c) putting the section into the driver's
`nested-invocation.md` — that reference owns the handoff, not the consumer's report shape.

## RB3 — The routing-verdict reference is a reference; the section never re-derives a verdict (D-2)

**Decision**: the section's per-invocation field carries a *reference* to the verdict `074a` recorded
in the Agent execution evidence, and the section states that the input set, verdict table and reason
codes are reached at the owner's path. When the record cannot be located, the section records the
reference as missing and the outer layer MUST NOT re-derive it.

**Evidence**:
- `074a-authorized-routing/feature-ref.md:108-110` (ruling 3, RA6/D-2): the verdict is recorded in the
  Agent execution evidence, and "the report section that will reference it is parent FR 021's and
  lands with `074b-nested-governance`".
- `shared/definitions/sdd-routing-definitions.md` is the single owner of the input domains, verdict
  table, precedence and reason codes (212 lines, delivered by `074a`); `scripts/python/sdd-route.py`
  (1,045 lines) computes a verdict and never stores one in a report.
- The requirements' edge case fixes the failure direction: a missing reference is recorded as missing,
  and a fabricated or recomputed reference is a contract violation (local C-8).

**Rejected**: (a) re-running `sdd-route.py route` from the report-writing step — it would produce a
second verdict for one duty and could disagree with the one the duty acted on; (b) inlining the
verdict's inputs and reason code into the section — a second copy of a table the owner defines, and
the reverse-count audit would flag it; (c) widening the handoff's field set — the handoff is `074a`'s
closed set and this slice adds no field to it.

## RB4 — The hosting-responsibility rule lands in the authoring baseline, and is asserted against the shipped leaf preset

**Decision**: the three responsibility statements an `[[STR-002]]` declaration must carry (hosts the
driver, does not execute stage commands itself, ends at review) are added to
`skills/internal/run-agent/SKILL.md` § Authoring Baseline, immediately after the existing
`sdd-invocation` paragraph; the leaf prohibition is asserted against the shipped
`agents/sdd-executor.agent.md`, which declares no such key.

**Evidence**:
- `skills/internal/run-agent/SKILL.md:171-181` opens the authoring baseline and fixes it as the
  vocabulary the authoring skills enforce; `:193` lists the supported fields including
  `sdd-invocation`; `:195-205` is the existing key paragraph, which already points at
  `src/specify_cli/__init__.py` for the closed values.
- `agents/sdd-executor.agent.md:1-13` (frontmatter) declares `name`, `description`,
  `user-invocable`, `disable-model-invocation`, `supervisor`, `model-tier`, `capability-tools`,
  `skills`, `run-turn-budget`, `display-color` — no `sdd-invocation` (`grep -c sdd-invocation
  agents/*.agent.md` → 0). The leaf rule is therefore checkable against a delivered artifact rather
  than a convention.
- `shared/definitions/agent-definitions.md` owns the three-layer taxonomy (Template / Instance /
  Execution) and is the right place for *what an agent is*, not for *what an author must state*; the
  authoring baseline is the surface an author reads while writing (parent C-26's "conformance check
  reads the declaration and the responsibility text together").

**Rejected**: (a) a new section in `agent-definitions.md` — that file owns the taxonomy, and the rule
is an authoring obligation, not a layer definition; (b) shipping an SDD-host preset so the rule has a
subject in the repo — no requirement names one (parent ruling R9, already applied by `074a`), and a
new product surface is out of scope; (c) enforcing the rule only in the contract test — the rule must
be readable where it is obeyed, not only where it is checked.

## RB5 — The Stage-vocabulary disambiguation is one sentence at the existing bullet, not a new section

**Decision**: `skills/internal/create-team/references/conceptual-model.md` gains one statement at its
`Stage` bullet: the Stage dimension (`executor` / `evaluator` / `optimizer`) is not the SDD stage
roster, the roster stays the driver's, no value is renamed, and no SDD stage name may be used as a
Stage value.

**Evidence**:
- `skills/internal/create-team/references/conceptual-model.md:1-3` declares the file's ownership;
  `:10` is the Stage bullet with the three canonical values and the removal note for the deprecated
  names — the exact site where a reader could mistake the dimension for a stage list.
- `tests/contract/test_single_conceptual_model.py:26` pins that the file defines the Role × Stage ×
  Type model; the file's section structure (`## The three orthogonal dimensions`, `## Type criterion`,
  `## Static vs Dynamic structure`, `## The Team Supervisor`, `## Collaboration patterns`,
  `## Lifecycle`, `## Template home`) is the shape sibling suites navigate, so an added top-level
  section would have no consumer.
- The SDD stage roster's only owner is the driver (`skills/external/sdd-loop-driver/SKILL.md` § The
  Loop and its state-spine format); the parent clause C-66's negative shape (no roster enumeration in
  new text) is what keeps the sentence from becoming a second roster.

**Rejected**: (a) a comparison table of team stages vs SDD stages — it would enumerate the roster
outside its owner, the exact duplication C-66 forbids; (b) renaming a team Stage value to clear the
collision — FR-003 forbids renaming and the rename would break every persisted team; (c) a new
`stages.md` reference — a fifth carrier of one vocabulary.

## RB6 — The instructions pointer is one additive section, and its acceptance is a declared ceiling plus a measured delta

**Decision**: `templates/instructions-template.md` gains exactly one pointer-level `## ` section for
the routing surface; `.specify/instructions.md` is regenerated by
`scripts/bash/generate-instructions.sh` and never hand-edited; the acceptance criterion is the
section's own byte ceiling plus a measured delta, because both files were over the generator's budget
before this slice.

**Evidence** (measured at plan time, `test-evidence/plan-stage-checks.md` § 5):
- `wc -c` → `.specify/instructions.md` 41,948 B, `templates/instructions-template.md` 34,666 B;
  `INSTRUCTIONS_BUDGET_BYTES=32768` (`scripts/bash/generate-instructions.sh:38`). The overage
  predates the slice by several features.
- Section counts: template 29 top-level `## ` headings, live file 30 — the additive reconcile has
  already injected one section the template no longer carries, and it never rewrites existing
  sections.
- `tests/contract/test_instructions_section_propagation.py:11-17` states the C-1/C-2 propositions:
  every template `## ` section MUST exist verbatim in the live file (C-1) and the generator injects
  additively and idempotently (C-2). Adding the section without regenerating therefore turns C-1 red,
  which is the mechanical reason the regeneration is part of the same change.
- `tests/contract/test_instructions_size_budget.py` reports size against the budget and never restates
  the number in the command template, so the ceiling this slice declares lives in its own plan and
  contract, not in the budget owner.

**Rejected**: (a) writing the pointer straight into `.specify/instructions.md` — a client-side
instance fix under the two-hats rule, lost on the next regeneration; (b) putting the pointer only into
`shared/guidelines/proactive-trigger.md` — the trigger layer is not read by an agent that is about to
write; (c) claiming "fits the budget" — unpassable before the slice and a false accusation after it.

## RB7 — The trigger edit is one sentence inside an existing section, and it adds no gate-scannable declaration

**Decision**: `shared/guidelines/proactive-trigger.md` gains one pointer sentence inside its existing
§ Promotion & Safety Boundary stating that promoting an SDD run requires both a routing verdict of the
SDD kind and an effective authorization of `[[STR-002]]`, with the conjunction stated once at the
routing owner. No new `## ` section is created, and the sentence restates no destructive-action class.

**Evidence**:
- `shared/guidelines/proactive-trigger.md` has exactly 10 top-level `## ` sections
  (`## Ownership` … `## Maintenance Duties`), and `tests/contract/test_proactive_trigger_section.py`
  C-2 pins that set as closed and ordered — a new section would break a delivered contract.
- `:68-79` is § Promotion & Safety Boundary, which already carries the promotion threshold, the
  destructive-never-promotes rule and the execution-report duty; the new conjunction belongs beside
  them and must point at the owner rather than re-derive the classification.
- **Pre-existing red, measured and disclosed**: `tests/contract/test_proactive_trigger_section.py::
  test_c11_gate_scan_total_unchanged` fails at the stage base — `gate total moved from the frozen 23
  to 27` (targeted-set run, `test-evidence/targeted-set-v1-baseline.txt`). The four added gates
  predate this slice. The criterion for this slice's edit is therefore "the scan total measured after
  the edit equals the pre-change total", not "the frozen budget is met", and the pre-existing failure
  is recorded rather than repaired here (repairing it would mean editing another feature's
  declarations or its frozen baseline — outside this slice's scope and a decision, not a correction).

**Rejected**: (a) a new `## SDD Invocation` section in the trigger doc — breaks the pinned closed
ordered section set for no reader's benefit; (b) restating the routing verdict table in the trigger
doc so the sentence is self-contained — the duplication C-56/C-57 forbid; (c) repairing the frozen
gate baseline in this slice — it would silently absorb four other features' drifts into this commit
and turn a recorded anomaly into an unrecorded one.

## RB8 — The containment claims are discharged by frozen node-id sets at verification time, not by a permanent ratchet test

**Decision**: FR-006/FR-007/SC-001 are discharged by collecting each named suite's
`pytest --collect-only` node-id set, freezing it at the baseline commit named in the verification
record (captured at plan time into `test-evidence/compat-baseline-nodeids.txt`, 266 cases across 17
files in 7 named sets), and asserting after the change that each post-change set is a superset and
that every shared id keeps its verdict. The permanent guard in the new compat suite asserts the
*structural* negatives and that the frozen carrier exists and parses non-empty per set; it does not
re-collect other suites.

**Evidence**:
- Parent C-62 fixes the method (case set, not count) and its reason: "one renamed case and one added
  case net to zero". Parent ruling R11 records the `comm -13` failure-set precedent and the
  absolute-count anti-pattern.
- The baseline is measurable today and was measured: S1 pre-dispatch governance 49 cases,
  S2 standalone driver entry 25, S3 070 preset 24, S4 064 line/worktree/ownership 40, S5 058 U0–U6 36,
  S6 team suites 54, S7 Agent suites 38.
- `docs/reference/history/00-cross-cutting-lessons.md` records both the absolute-count lesson and the
  "a green check is a claim" lesson; a permanent superset ratchet over *other* features' suites would
  convert a per-change claim into an invariant nobody granted — legitimate case removals (a wording
  pin replaced by an engine test, as `test_proactive_trigger_section.py` documents for its own former
  C-8…C-16) would then fail for reasons unrelated to this feature.

**Rejected**: (a) a count comparison — non-conforming by C-62; (b) a permanent test that re-collects
the sibling suites and compares with a checked-in set — it would fire on every future legitimate case
rename and would make the claim's scope ("relative to the baseline commit in the verification
record") unrepresentable; (c) trusting "the suites stay green" — a green suite says nothing about a
dropped case.

## RB9 — Test plan: three new files, one edited suite, one reused fixture, no new fixture

**Decision**:

| Surface | File | Behaviour group |
|---------|------|-----------------|
| Report section + attribution | `tests/contract/test_nested_run_report.py` (NEW) | `[[STR-007]]` literal and mandatory-ness, per-invocation fields, explicit-when-empty, supervisor-only write, one ledger row with `target_ref`, no new Goal field, verdict reference by reference |
| Diffusion | `tests/contract/test_sdd_diffusion.py` (NEW) | Stage disambiguation, host responsibility statement, leaf preset negative, instructions pointer with no restatement, trigger conjunction pointer, no roster enumeration |
| Compatibility + safety | `tests/contract/test_sdd_compat_containment.py` (NEW) | default-`forbidden` resolution cases, containment carrier shape, four-surface additivity, no new command/skill, no merge/push/scheduler/gate, gate-scan total stability |
| Pre-dispatch governance (edit) | `tests/contract/test_sdd_invocation_governance.py` (EDIT) | the absent-declaration default-resolution cases that make the superset relation non-trivial |
| Fixture | `tests/fixtures/nested_sdd.py` (reused, unchanged) | temp repo with two seats, two agent definitions, one goal with an open Target |

**Evidence**:
- `tests/fixtures/nested_sdd.py` (369 lines, `074a`) already builds the repository shape every 074b
  assertion needs; a second fixture would duplicate it and drift.
- `tests/contract/test_sdd_invocation_governance.py` collects 17 cases today; the eleven
  `default-resolution` propositions FR-006 adds have no home there yet, and adding them is the
  superset direction the containment claim requires.
- The parent's own test assignment (`074-goal-team-sdd-unification/research.md:303-320`, R14) named
  `test_nested_run_report.py` for exactly this slice, so the file name is grounded in the parent
  design rather than chosen here.
- Sibling naming for the two other new files follows `test_sdd_authorization.py`,
  `test_sdd_invocation_governance.py`, `test_sdd_routing_definitions.py`.

**Rejected**: (a) a new fixture module — duplicate repository scaffolding; (b) putting the report
cases into `test_nested_sdd_invocation.py` — that file is `074a`'s handoff suite and its D-3
assertion is explicitly a negative about this section; (c) one catch-all suite for all three behaviour
groups — the disjoint-owner convention used by the sibling slice.

## RB10 — Same-author scoring disclosed, not delegated; the feature status is already at its ceiling

**Decision**: every Constitution Check row carries `(direct read, subagent unavailable)`, and the
program-derivable checks were executed instead (`clause_extract.py`, `account-clause-coverage.py`,
`pre-analyze-check.py --stage plan`, `sync-mirrors.py --check`, `regen-command-copies.py --check`,
`flow-class-check.py`, the targeted suite). The Feature 074 registry row stays `Planned`: no
`Draft → Planned` transition exists for a slice whose parent row is already `Planned`, and
`Implemented` is `/speckit.implement`'s transition over the whole Feature.

**Evidence**:
- `shared/workflow/objective-analysis-gate.md` delegates scoring when the artifacts under analysis
  were authored in the same pass; this environment exposes no subagent tool and the stage brief fixes
  `decomposition=single-package`, so delegation is impossible and a self-scored row presented as
  independent evidence would be worse than a disclosed one.
- `.specify/memory/features.md` row 074 reads `Planned`, and
  `074a-authorized-routing/feature-ref.md:104-105` records the same reading for the first slice ("no
  new Feature row — the slice reuses Feature 074, status stays Planned"). This stage therefore
  appends its entry to `.specify/memory/features/074.md` § Latest Review and updates `Last Updated`;
  it flips nothing.

**Rejected**: (a) claiming delegated scoring (false); (b) skipping the Constitution Check (it is a
gate); (c) advancing the row to `Planned` as if it were a new feature — a no-op that would imply a
transition which did not happen.
