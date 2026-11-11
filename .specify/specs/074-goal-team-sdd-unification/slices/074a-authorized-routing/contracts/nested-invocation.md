# Contracts: Nested SDD invocation and handoff (C-31…C-43)

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the invoked-from-team entry form, its validation set, the stop-at-review
boundary, the handoff's closed field set, and the reuse of the existing line/state primitives. The
stage roster, state-spine format, sentinels, U4 verification, watcher semantics, and stall handling
remain owned by Feature 058 / `sdd-loop-driver`; the work-package model by Feature 070; the line
registry, worktree-per-write-line, ownership, and integration queue by Feature 064. All are cited,
never re-specified.
**Pinned by**: `tests/contract/test_nested_sdd_invocation.py` (planned)
**Measures**: SC-003, SC-005

**C-31** (父 C-31): `sdd-loop-driver` supports an invoked-from-team entry form accepting exactly six
facts: the bound Goal reference, an optional Target reference, the team slug, the invoking seat, the
authorized artifact/territory scope, and the routing verdict reference. The form validates all six
before U0 begins; a fact the form does not accept is not silently ignored. (FR-015)

**C-32** (父 C-32): Entry validation fails closed on each of these conditions, naming the condition: a
missing or undefined Goal; a Target that is dangling, closed, dropped, or outside the bound Goal; a
terminal Goal; a missing team slug or seat; a scope outside the seat's territory; a missing routing
verdict or a verdict other than [[STR-004]]. A failing entry does not start a run and does not
re-scope the duty to fit. (FR-015)

**C-33** (父 C-34): A nested run ends at review completion — after the driver's existing
review-repair loop settles, not before its findings are addressed — and returns a structured
handoff. It does not proceed to a merge step and does not claim the merge authority that belongs to
the outer layer. (FR-016)

**C-34** (父 C-35): The handoff carries a closed field set: the outcome, the stages reached, the
artifact paths, the evidence paths, the unresolved review findings, an explicit anomaly line, and the
integration identity. Missing any field makes the handoff incomplete; an incomplete handoff is never
a successful return. (FR-016)

**C-35** (父 C-36): The outcome takes exactly one of three values — [[STR-007]], [[STR-008]],
[[STR-009]]. A [[STR-008]] or [[STR-009]] nested run MUST NOT be reported as success by any consumer,
and the invoking Agent's own result MUST carry the failing value rather than a summary that hides it.
(FR-016, FR-017)

**C-36** (父 C-37): The integration identity is exactly four facts — line id, branch, worktree path,
and HEAD commit — and the handoff names the retained branch. The four are read from the existing line
registry entry plus one git read at handoff time; no second record of them is created. (FR-016)

**C-37** (父 C-38): A nested run MUST NOT merge and MUST NOT push. The outer layer adjudicates
integration under its existing confirmation-gate discipline; the nested run's only integration act is
to name where the work lives. (FR-016)

**C-38** (父 C-39): A nested run registers with the existing line registry and the existing
worktree-per-write-line and ownership mechanism as one write line. Concurrent nested runs whose
territories overlap are serialized or rejected by that mechanism, citing it rather than a new gate.
(FR-018, SC-005)

**C-39** (父 C-40): On stall, timeout, or budget exhaustion the nested run stops, persists its state
spine, and returns a [[STR-009]] handoff carrying what was found, why the run was costly, the
intermediate artifacts by path, and the available dispositions. The outer team's failure isolation
and reporting apply, and the run MUST NOT wait silently. (FR-019)

**C-40** (父 C-41): The invoking Agent includes the nested run's handoff in its own result and in the
team run report, verbatim or by stable path. It MUST NOT report success when the nested outcome is
[[STR-008]] or [[STR-009]], and MUST NOT paraphrase an incomplete handoff into a complete-sounding
sentence. (FR-017)

**C-41** (父 C-42; delivered under `../requirements.md` § Cross-Slice Design Attribution D-3): the
slice's end-to-end acceptance shape is fixed at the **content face** — one nested run reaches review,
produces the complete SDD artifact chain, performs zero merge and zero push (assertable from
`git log` and `git status`), and every artifact and evidence path is referenced from the invoking
Agent's result and from the team run report written under its existing contract. The `## Nested SDD
Runs` heading literal and that section's mandatory-and-explicit-when-empty semantics belong to
`074b-nested-governance`; the slice's fixture asserts the path references and does not assert the
heading literal. (FR-017, SC-003)

**C-42** (父 C-46): A handoff without its integration identity leaves the outer layer unable to
integrate, so it is incomplete by definition and the run MUST NOT be reported successful. The
consuming check is a field-presence test over the handoff block, not a prose reading.
(FR-016, FR-017)

**C-43** (父 C-64, FR-018 facet): No second registry, ledger, state spine, ownership model, or
integration queue is introduced. A nested run's records resolve to the existing line entry and the
existing state spine, and the structural check asserts both the reuse and the absence of a new store.
(FR-018, SC-005)

## Parent Clause Mapping

| Slice clause | Parent clause | Parent contract file | Requirement face |
|--------------|---------------|----------------------|------------------|
| C-31 | C-31 | `nested-invocation.md` | FR-015 |
| C-32 | C-32 | `nested-invocation.md` | FR-015 |
| C-33 | C-34 | `nested-invocation.md` | FR-016 |
| C-34 | C-35 | `nested-invocation.md` | FR-016 |
| C-35 | C-36 | `nested-invocation.md` | FR-016, FR-017 |
| C-36 | C-37 | `nested-invocation.md` | FR-016 |
| C-37 | C-38 | `nested-invocation.md` | FR-016 |
| C-38 | C-39 | `nested-invocation.md` | FR-018, SC-005 |
| C-39 | C-40 | `nested-invocation.md` | FR-019 |
| C-40 | C-41 | `nested-invocation.md` | FR-017 |
| C-41 | C-42 | `nested-invocation.md` | SC-003 (D-3 content face) |
| C-42 | C-46 | `nested-invocation.md` | FR-016, FR-017 |
| C-43 | C-64 | `diffusion-and-compat.md` | FR-018 (facet) |

Deferred to `074b-nested-governance`: parent C-33, C-43, C-44 (additivity on the standalone driver
entry, the Feature 070 stage-team preset, and the Feature 058 U0–U6 contract — parent FR 027).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-31, C-32 | FR-015 | — | `skills/external/sdd-loop-driver/SKILL.md` § Invoked-from-Team Entry |
| C-33, C-34, C-35, C-36, C-42 | FR-016, FR-017 | SC-003 | `sdd-loop-driver/references/nested-invocation.md` |
| C-37, C-38, C-39, C-41 | FR-016, FR-018, FR-019 | SC-003, SC-005 | driver Hard Requirements; Feature 064 registry (referenced) |
| C-40 | FR-017 | SC-003 | `run-team` / `create-team` report duty (existing) |
| C-43 | FR-018 | SC-005 | structure check over the changed tree |
