# Contracts: Diffusion into the Goal/Team/Agent surfaces (C-13…C-20)

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the four diffusion surfaces this slice adds or amends — the team conceptual
model's Stage-vocabulary boundary, the Agent authoring baseline's hosting-responsibility rule, the
project instructions' pointer-level routing surface, and the proactive trigger's promotion
conjunction. Each diffused fact is a **pointer** to its owner: the routing owner
`shared/definitions/sdd-routing-definitions.md`, the neutral key set in `src/specify_cli/__init__.py`,
and the driver's stage roster. None of them restates a table, a threshold, or an enumeration.
**Pinned by**: `tests/contract/test_sdd_diffusion.py` (planned)
**Measures**: DoD-2 / DoD-4 / DoD-6 + T010/T016/T019/T024 (pointers into `tasks.md`; no SC is added or
re-scoped here — the diffusion faces are graded by those rows rather than by a second acceptance claim)
**Parent source**: `parent C-55`, `parent C-66` (Stage-vocabulary facet), `parent C-25`,
`parent C-26`, `parent C-56`, `parent C-57`; `parent C-60` is cited (claimed and delivered by
`074a`).

**C-13**: The team conceptual model states that its Stage dimension (`executor` / `evaluator` /
`optimizer`) is not the SDD stage roster, and that the SDD stage roster remains owned by the driver.
No team Stage value is renamed or overloaded with an SDD stage name, and the statement is added at the
existing Stage bullet rather than as a new top-level section of the owner file (FR-003). *(parent C-55.
The constraint is **bidirectional**: no team Stage value may take an SDD stage name, and no SDD stage
name may be added to the team Stage vocabulary — C-14 asserts the second direction as an absence. Where
one definition appears to carry both the hosting duty and the stage-execution duty, the seat's
**operating object** decides — the layer the seat actually operates on selects its duty set — never its
name, and C-15…C-17 state that leaf side (FR-003))*

**C-14**: No surface produced by this slice enumerates SDD stage names, duplicates the stage roster,
or declares a second team Stage vocabulary. The check reads the text this slice adds and asserts the
absence of a roster-shaped enumeration, with the driver as the only roster owner (FR-003).
*(parent C-66, Stage-vocabulary facet)*

**C-15**: The SDD stage-executor capacity remains a leaf and MUST NOT declare `[[STR-002]]`. The rule
is asserted against the delivered artifact — the shipped stage-executor preset
`agents/sdd-executor.agent.md` declares no `[[STR-001]]` key — so the leaf boundary is checked against
what ships, not against a convention (FR-004). *(parent C-25)*

**C-16**: An Agent Template or Instance that hosts SDD declares `[[STR-002]]` and states in its
responsibilities that it hosts the driver, that it does not execute stage commands itself, and that it
ends at review. The conformance check reads the declaration and the responsibility text together: a
declaration without the three statements fails, and the three statements without the declaration fail
(FR-004). *(parent C-26)*

**C-17**: The hosting-responsibility rule is stated where an author reads while writing — the
authoring baseline (`skills/internal/run-agent/SKILL.md` § Authoring Baseline), immediately after the
existing `[[STR-001]]` paragraph. The statement points at the key set's owner for the closed values
and restates none of them, so the key set stays a single definition point (FR-004). *(parent C-60
cited; no value is re-declared)*

**C-18**: The project instructions carry exactly one pointer-level routing surface: when a
write-bearing change is proposed, run the decision at the owner's path. The surface MUST NOT restate
the input set, the closed value domains, the verdict table, or the reason-code vocabulary, and it MUST
NOT introduce a second copy of the precedence rule (FR-005). *(parent C-56)*

**C-19**: The proactive trigger MUST NOT start an SDD run on the strength of a suggestion alone:
promotion requires both a routing verdict of the SDD kind and an effective authorization of
`[[STR-002]]`. The conjunction is stated once in the routing owner and reached from the trigger
discipline by pointer; the trigger document gains one sentence inside its existing
§ Promotion & Safety Boundary and no new section, since its section set is a delivered closed set
(FR-005). *(parent C-57)*

**C-20**: The instructions pointer is delivered as exactly one additive `## ` section of
`templates/instructions-template.md`, regenerated into `.specify/instructions.md` by
`scripts/bash/generate-instructions.sh`; the live file is never hand-edited, and the compatibility
instruction symlinks follow because they point at it. Because both files already exceeded the
generator's byte budget before this slice, the acceptance criterion is the section's own declared byte
ceiling plus a measured delta, never an absolute "fits the budget" claim (FR-005). *(Design-level
criterion: the requirement anchor is FR-005's "one pointer-level routing surface", while the byte
ceiling, the generator route and the symlink consequence are design quantities with no requirement
anchor; this clause is therefore graded as a design obligation and MUST NOT be cited as an
acceptance criterion in its own right)*

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-13, C-14 | FR-003 | — | `skills/internal/create-team/references/conceptual-model.md:10` |
| C-15, C-16, C-17 | FR-004 | — | `agents/sdd-executor.agent.md` (negative); `skills/internal/run-agent/SKILL.md` § Authoring Baseline |
| C-18, C-20 | FR-005 | — | `templates/instructions-template.md` → `.specify/instructions.md` |
| C-19 | FR-005 | — | `shared/guidelines/proactive-trigger.md` § Promotion & Safety Boundary |
