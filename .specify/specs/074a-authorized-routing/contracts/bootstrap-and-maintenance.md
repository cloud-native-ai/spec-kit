# Contracts: Bootstrap and maintenance classification (C-44…C-47)

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the slice's classification of the four invocation kinds an Agent chooses
among, the setup path taken when a target project carries no `.specify/` structure, and the boundary
that makes only the driver an SDD invocation. The routing owner document declares the classification;
this file states what the classification must contain and how the other surfaces reach it.
**Pinned by**: `tests/contract/test_sdd_routing_definitions.py`,
`tests/contract/test_sdd_invocation_governance.py` (planned)
**Measures**: SC-005

**C-44** (父 C-58): The routing surface classifies the four invocation kinds it governs, so an Agent
can choose among them: the SDD development flow (the driver), framework bootstrap (the setup skill),
periodic maintenance (the house-keeping skill), and direct modification. Bootstrap and maintenance
are distinct from the development flow, and only the driver constitutes an SDD invocation under the
nested entry contract. (FR-020)

**C-45** (父 C-45): When a routed change reaches a target project that carries no `.specify/`
structure, the route is the setup path, and the framework MUST NOT degrade an SDD-routed change into
a direct modification. The setup skill is named as the entry; it is not itself an SDD invocation.
(FR-020)

**C-46** (父 C-59): When the setup or house-keeping skill dispatches subagents, that dispatch
satisfies the same effective-authorization predicate as an SDD invocation. The predicate is the
routing owner's, not a second one: the same two declared halves, resolved by (team, seat), form the
AND. (FR-020, FR-005)

**C-47** (父 C-67): The slice adds no new `/speckit.*` command and no new skill. Every capability
lands on an existing command, skill, engine, template, or shared definition, and the delivered file
set is a diff of those owners. (FR-020)

## Parent Clause Mapping

| Slice clause | Parent clause | Parent contract file | Requirement face |
|--------------|---------------|----------------------|------------------|
| C-44 | C-58 | `diffusion-and-compat.md` | FR-020 |
| C-45 | C-45 | `nested-invocation.md` | FR-020 |
| C-46 | C-59 | `diffusion-and-compat.md` | FR-020, FR-005 |
| C-47 | C-67 | `diffusion-and-compat.md` | FR-020 |

Deferred to `074b-nested-governance` from the same parent file: parent C-55 (team Stage-vocabulary
disambiguation), C-56 / C-57 (the instructions pointer section and the proactive-trigger conjunction —
parent FR 024), C-61 / C-62 (the four-surface containment claim and its node-id discharge — parent
FR 027 / SC-005), C-63 (no new merge/push, scheduler, transmission, or second gate — parent FR 028),
C-65 (default-`forbidden` containment, parent FR 026).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-44, C-45, C-46 | FR-020, FR-005 | SC-005 | `shared/definitions/sdd-routing-definitions.md` § Invocation kinds |
| C-47 | FR-020 | SC-005 | repo-wide negative check (no new command, no new skill) |
