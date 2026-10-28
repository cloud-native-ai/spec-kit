# Contracts: Authorization and the pre-dispatch predicate (C-15…C-30)

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the two authorization storage forms' *increment*, the AND resolution,
and the narrowed anti-nesting predicate at its existing owner site. The neutral metadata key set
is owned by `src/specify_cli/__init__.py`; the `team.md` schema by
`skills/internal/create-team/references/create-mode.md`; the anti-nesting obligation by
`shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation. Each is
amended once, in place.
**Pinned by**: `tests/contract/test_sdd_authorization.py`,
`tests/contract/test_sdd_invocation_governance.py` (planned)
**Measures**: SC-001, SC-004, SC-005

**C-15**: An Agent definition declares SDD invocation capability through the neutral metadata key
`sdd-invocation`, whose closed values are `allowed` and `forbidden`; an absent key means
`forbidden`. The key is framework-level: it carries `renders_to_tools = False`, is a member of
the framework assembly key set, and MUST NOT be produced in any host tool's rendered agent
fields (FR-003).

**C-16**: A Team roster seat declares SDD invocation policy through the same key with the same
closed values, as a `seats:` block map in `team.md` frontmatter keyed by seat slug. An absent
`seats` key, an absent entry for the seat, or an absent key inside the entry all mean
`forbidden`. An existing team without the key keeps byte-identical behaviour, and no flow
back-fills the key (FR-004, FR-026).

**C-17**: The `seats:` map is accepted in block style only. A flow-style map is refused as
malformed input with the seat named, and a seat entry that matches no member role or seat
instance is reported as dangling rather than ignored; neither case degrades to `allowed`
(FR-004).

**C-18**: The dispatch payload carries the team slug, and the authorization probe resolves the
seat policy by (team, seat). Resolution therefore requires both coordinates; a payload that
carries only the seat cannot satisfy the predicate and is refused (FR-004).

**C-19**: Effective authorization is the logical AND of the Agent capability and the seat policy,
both resolved through one deterministic, read-only engine action
(`scripts/python/sdd-route.py --action authorize`). An SDD run MUST NOT start unless the
effective value is `allowed`. A refusal names which half failed — the Agent side, the seat side,
or both — and records both source paths plus the seat slug so the verdict is recheckable
(FR-004, SC-001).

**C-20**: The anti-nesting obligation is narrowed once, in its existing owner
(`shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation), to a
decidable predicate: a dispatch prompt may name or assign an SDD driver only when the recipient
resolves to an Agent definition declaring `allowed`, its seat policy declares `allowed`, and the
assigned task is an SDD assignment. Every dispatch that does not satisfy all three conditions
keeps the original prohibition unchanged. The amendment states the predicate; it does not move
the obligation, and no second copy of the predicate is created elsewhere (FR-005).

**C-21**: The pre-dispatch probe in `skills/internal/run-agent/SKILL.md` enforces the predicate
and fails closed: a prompt naming an SDD driver without all three conditions is not dispatched,
and the refusal names the condition that failed. The probe calls the engine action of C-19 rather
than re-reading the definitions in prose, and its refusal text carries the failed condition so
the caller cannot repair it by rewording the prompt (FR-005).

**C-22**: The permitted nesting chain is depth 2: team orchestrator → invoking member (driver
host) → stage executor (leaf). The anti-nesting owner states this chain, replacing the
unqualified "loop depth is always 1" claim, and states the three prohibitions in the same place:
a stage executor MUST NOT start or host any SDD run; an SDD stage executor MUST NOT itself be an
SDD invocation host; SDD-within-SDD recursion is prohibited (FR-006).

**C-23**: A member executed in virtual mode MUST NOT host an SDD run. Virtual execution occupies
the orchestrating session, so hosting a driver inside it collapses the outer layer into the
driver; the probe refuses the dispatch before it leaves and reports the reason (FR-006).

**C-24**: A member hosts at most one SDD run at a time unless the team declares a higher
per-member cap within the existing line mechanism. No second concurrency primitive is
introduced: overlapping territories are serialized or rejected by the line registry and
ownership mechanism of Feature 064, and the decision cites that mechanism rather than inventing
a gate (FR-006, FR-018, SC-006).

**C-25**: The SDD stage-executor capacity remains a leaf and MUST NOT declare `allowed`. The
shipped stage-executor preset is asserted not to declare it, so the leaf rule is checked against
the delivered artifact rather than against a convention (FR-023, FR-006).

**C-26**: An Agent Template or Instance that declares `allowed` states in its responsibilities
that it hosts the driver, that it does not execute stage commands itself, and that it ends at
review. The conformance check reads the declaration and the responsibility text together: a
declaration without the three statements fails (FR-023).

**C-27**: An Agent definition or Team seat carrying no declaration resolves to `forbidden`, and
the pre-dispatch probe rejects any dispatch for that recipient that names an SDD driver. This is
the feature's first containment claim: relative to the case set captured at the pre-change
commit named in the verification record, the post-change case set of the pre-dispatch governance
suite is a superset, and every pre-change case returns the same verdict (FR-026, SC-005).

**C-28**: Stage executors cannot start an SDD run, and every dispatch prompt that names a driver
without satisfying all three conditions is blocked before dispatch. All pre-existing
anti-nesting contract cases remain green for the paths that do not satisfy the predicate — the
narrowing adds an allowance, it removes no prohibition from any path that fails it
(SC-004, FR-026).

**C-29**: A refused dispatch produces a record naming the failed condition and the recipient's
resolved values. A record that states only "not authorized" is non-conforming: the two halves
exist precisely so a reader can tell a policy decision from a missing declaration (FR-005,
SC-001).

**C-30**: The authorization surface adds no confirmation gate, no scheduler, and no second
registry. Its only stored state is the two declared values; everything else is read at probe
time from the definition, the roster, and the line registry (FR-028, FR-018).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-15, C-16, C-17, C-18, C-19, C-29 | FR-003, FR-004, FR-005 | SC-001 | `src/specify_cli/__init__.py`, `create-mode.md` schema, `sdd-route.py --action authorize` |
| C-20, C-21, C-22, C-23, C-27, C-28 | FR-005, FR-006, FR-026 | SC-004, SC-005 | `subagent-definitions.md` § Dispatch-Time Governance Obligation, `run-agent/SKILL.md` |
| C-24, C-30 | FR-006, FR-018, FR-028 | SC-006 | Feature 064 line registry (referenced) |
| C-25, C-26 | FR-023, FR-006 | — | `agents/sdd-executor.agent.md` (negative), authored instances (positive) |
