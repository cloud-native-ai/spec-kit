# Contracts: Diffusion, compatibility and containment (C-55…C-67)

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the diffusion surfaces (team conceptual model, project instructions,
proactive trigger, invocation-kind classification, agent authoring baseline) and the two
containment claims that make compatibility decidable. Each diffused fact is a pointer to its
owner; none of them restates a table, a threshold, or an enumeration.
**Pinned by**: `tests/contract/test_sdd_routing_definitions.py`,
`tests/contract/test_sdd_invocation_governance.py` (planned)
**Measures**: SC-004, SC-005, SC-006

**C-55**: The team conceptual model states that its Stage dimension (executor / evaluator /
optimizer) is not the SDD stage roster, and that the SDD stage roster remains owned by the
driver. No team Stage value is renamed, and no SDD stage name is used as a team Stage value
(FR-022).

**C-56**: The project instructions carry exactly one pointer-level routing surface: when a
write-bearing change is proposed, run the decision at the owner's path. The section MUST NOT
restate the input set, the closed value domains, the verdict table, or the reason-code
vocabulary, and it MUST NOT introduce a second copy of the precedence rule (FR-024, FR-014).

**C-57**: The proactive trigger MUST NOT start an SDD run on the strength of a suggestion alone:
promotion requires both a routing verdict of the SDD kind and an effective authorization of
`allowed`. The conjunction is stated once in the routing owner and reached from the trigger
discipline, which gains a pointer rather than a copy (FR-024).

**C-58**: The routing surface classifies the four invocation kinds it governs, so an Agent can
choose among them: the SDD development flow (the driver), framework bootstrap (the setup skill),
periodic maintenance (the house-keeping skill), and direct modification. Bootstrap and
maintenance are distinct from the development flow, and only the driver constitutes an SDD
invocation under the nested entry contract (FR-025).

**C-59**: When the setup or house-keeping skill dispatches subagents, that dispatch satisfies the
same effective-authorization predicate as an SDD invocation. The predicate is the routing owner's,
not a second one: the same two declared halves, resolved by (team, seat), form the AND
(FR-025, FR-005).

**C-60**: The agent authoring baseline — the framework frontmatter field list owned by the
`run-agent` skill and consumed by the authoring skills — includes the new key, so an authored
instance can declare it and a validator will reject a value outside its closed set. The baseline
entry is a pointer to the key set's owner, not a second definition of the values
(FR-003, FR-023).

**C-61**: The feature is additive on the four named surfaces: the standalone `sdd-loop-driver`
entry contract, the Feature 070 stage-team preset contract, the Feature 064
line/worktree/ownership contract, and the Feature 058 U0–U6 contract. On each surface no
existing key, section, entry form, or exit code is removed, renamed, or changed in meaning;
additions are permitted. As a decidable containment claim: for each surface, the post-change
contract-suite case set is a superset of the pre-change case set captured at the baseline commit
named in the verification record, and every pre-change case passes (FR-027, SC-005).

**C-62**: The containment claim is discharged mechanically: the case set of each named suite is
its collected test-node-id set, frozen at the pre-change commit before any edit; the check
asserts set containment (post ⊇ pre) and, for the shared ids, identical verdicts. A count
comparison is non-conforming, because one renamed case and one added case net to zero and would
hide a dropped obligation (FR-026, FR-027, SC-005).

**C-63**: The framework adds no automatic merge or push, no scheduler or daemon, no automatic
feedback transmission, and no second confirmation gate. Every integration decision remains with
the outer layer under its existing confirmation-gate discipline (FR-028).

**C-64**: No second registry, ledger, state spine, ownership model, or integration queue is
introduced. A nested run's records resolve to the existing line entry and the existing state
spine, and the structural check asserts both the reuse and the absence of a new store
(FR-018, SC-006).

**C-65**: An Agent definition or Team seat that carries no declaration resolves to `forbidden`,
so behaviour without a declaration is unchanged: the pre-dispatch probe rejects a dispatch for
that recipient that names an SDD driver, and nothing else about that recipient's dispatch
changes (FR-026).

**C-66**: No new surface produced by this feature enumerates SDD stage names, duplicates the
stage roster, or declares a second team Stage vocabulary. The check reads the added text and
asserts the absence of a roster-shaped enumeration, with the driver as the only roster owner
(FR-022, FR-014).

**C-67**: The feature adds no new `/speckit.*` command and no new skill. Every capability lands
on an existing command, skill, engine, template, or shared definition, and the delivered file set
is a diff of those owners (FR-028, FR-025).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-55 | FR-022 | — | `skills/internal/create-team/references/conceptual-model.md` |
| C-56, C-57 | FR-024, FR-014 | — | `templates/instructions-template.md` § SDD invocation routing |
| C-58, C-59 | FR-025, FR-005 | — | `shared/definitions/sdd-routing-definitions.md` § Invocation kinds |
| C-60 | FR-003, FR-023 | — | `skills/internal/run-agent/SKILL.md` authoring baseline |
| C-61, C-62 | FR-026, FR-027 | SC-005 | four predecessor contract suites + frozen case sets |
| C-63, C-67 | FR-028, FR-025 | — | repo-wide negative check |
| C-64, C-66 | FR-018, FR-022, FR-014 | SC-006 | structure check over the changed tree |
| C-65 | FR-026 | SC-004 | pre-dispatch governance suite |
