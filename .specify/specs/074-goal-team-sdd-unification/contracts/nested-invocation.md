# Contracts: Nested SDD invocation and handoff (C-31…C-46)

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the invoked-from-team entry form, its validation set, the stop-at-review
boundary, the handoff's closed field set, and the additive relationship to the four named
predecessor surfaces. The stage roster, state-spine format, sentinels, U4 verification, watcher
semantics, and stall handling remain owned by Feature 058 / `sdd-loop-driver`; the work-package
model by Feature 070; the line registry, worktree-per-write-line, ownership, and integration
queue by Feature 064. All are cited, never re-specified.
**Pinned by**: `tests/contract/test_nested_sdd_invocation.py` (planned)
**Measures**: SC-003, SC-006

**C-31**: `sdd-loop-driver` supports an invoked-from-team entry form accepting exactly six
facts: the bound Goal reference, an optional Target reference, the team slug, the invoking seat,
the authorized artifact/territory scope, and the routing verdict reference. The form validates
all six before U0 begins; a fact the form does not accept is not silently ignored (FR-015).

**C-32**: Entry validation fails closed on each of these conditions, naming the condition: a
missing or undefined Goal; a Target that is dangling, closed, dropped, or outside the bound Goal;
a terminal Goal; a missing team slug or seat; a scope outside the seat's territory; a missing
routing verdict or a verdict other than the SDD verdict. A failing entry does not start a run and
does not re-scope the duty to fit (FR-015).

**C-33**: The nested entry form is additive on the standalone entry contract: no existing key,
section, entry form, or exit code of `sdd-loop-driver` is removed, renamed, or changed in
meaning, and the standalone default-resolution behaviour is unchanged. The new form is a
distinct entry whose semantics are validation-then-refuse, never default-resolution
(FR-027, SC-005).

**C-34**: A nested run ends at review completion — after the driver's existing review-repair loop
settles, not before its findings are addressed — and returns a structured handoff. It does not
proceed to a merge step and does not claim the merge authority that belongs to the outer layer
(FR-016).

**C-35**: The handoff carries a closed field set: the outcome, the stages reached, the artifact
paths, the evidence paths, the unresolved review findings, an explicit anomaly line, and the
integration identity. Missing any field makes the handoff incomplete; an incomplete handoff is
never a successful return (FR-016).

**C-36**: The outcome takes exactly one of three values — `completed`, `blocked`, `failed`. A
blocked or failed nested run MUST NOT be reported as success by any consumer, and the invoking
Agent's own result MUST carry the failing value rather than a summary that hides it (FR-016,
FR-017).

**C-37**: The integration identity is exactly four facts — line id, branch, worktree path, and
HEAD commit — and the handoff names the retained branch. The four are read from the existing line
registry entry plus one git read at handoff time; no second record of them is created (FR-016).

**C-38**: A nested run MUST NOT merge and MUST NOT push. The outer layer adjudicates integration
under its existing confirmation-gate discipline; the nested run's only integration act is to name
where the work lives (FR-016).

**C-39**: A nested run registers with the existing line registry and the existing
worktree-per-write-line and ownership mechanism as one write line. Concurrent nested runs whose
territories overlap are serialized or rejected by that mechanism, citing it rather than a new
gate. No second registry, ownership model, integration queue, or state spine is created
(FR-018, SC-006).

**C-40**: On stall, timeout, or budget exhaustion the nested run stops, persists its state spine,
and returns a `failed` handoff carrying what was found, why the run was costly, the intermediate
artifacts by path, and the available dispositions. The outer team's failure isolation and
reporting apply, and the run MUST NOT wait silently (FR-019).

**C-41**: The invoking Agent includes the nested run's handoff in its own result and in the team
run report, verbatim or by stable path. It MUST NOT report success when the nested outcome is
`blocked` or `failed`, and MUST NOT paraphrase an incomplete handoff into a complete-sounding
sentence (FR-017).

**C-42**: The end-to-end acceptance shape is fixed: one nested run reaches review, produces the
complete SDD artifact chain, performs zero merge and zero push, and every artifact and evidence
path appears in the team run report's nested section (SC-003).

**C-43**: Feature 070's stage-team preset contract is preserved as the in-run decomposition
mechanism: work packages remain the only in-run decomposition, the preset is not a substitute for
nested invocation, and nested invocation is not a substitute for the preset. No preset key,
section, or entry form changes (FR-027, SC-005).

**C-44**: Feature 058's U0–U6 contract is preserved: the nested form adds an entry and a stop
boundary; it does not change stage semantics, sentinels, independent verification, watcher
判定/退出码, stall disposition, or the fast-lane/test-budget rules (FR-027, SC-005).

**C-45**: When a routed change reaches a target project that carries no `.specify/` structure,
the route is the setup path, and the framework MUST NOT degrade an SDD-routed change into a
direct modification. The setup skill is named as the entry; it is not itself an SDD invocation
(FR-025).

**C-46**: A handoff without its integration identity leaves the outer layer unable to integrate,
so it is incomplete by definition and the run MUST NOT be reported successful. The consuming
check is a field-presence test over the handoff block, not a prose reading (FR-016, FR-017).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-31, C-32, C-33, C-44 | FR-015, FR-027 | SC-005 | `skills/external/sdd-loop-driver/SKILL.md` § Invoked-from-Team Entry |
| C-34, C-35, C-36, C-37, C-46 | FR-016, FR-017 | SC-003 | `skills/external/sdd-loop-driver/references/nested-invocation.md` |
| C-38, C-39, C-40, C-42 | FR-016, FR-018, FR-019 | SC-003, SC-006 | driver Hard Requirements; Feature 064 registry (referenced) |
| C-41 | FR-017 | SC-003 | `run-team` / `create-team` report duty |
| C-43 | FR-027 | SC-005 | Feature 070 stage-team preset (unchanged) |
| C-45 | FR-025 | — | `sdd-project-setup` (named as the setup path) |
