# Contracts: Control hierarchy and two-half authorization (C-1…C-16)

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the slice's statement of the control hierarchy, the two storage forms that
carry one authorization value, the AND resolution, and the narrowed anti-nesting predicate at its
existing owner site. The neutral metadata key set is owned by `src/specify_cli/__init__.py`; the
`team.md` schema by `skills/internal/create-team/references/create-mode.md`; the anti-nesting
obligation by `shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation.
Each is amended once, in place.
**Pinned by**: `tests/contract/test_sdd_authorization.py`, `tests/contract/test_sdd_invocation_governance.py`,
`tests/contract/test_neutral_metadata_schema.py` (planned)
**Measures**: SC-001, SC-004, SC-005

**Clause ids are the slice's own projection.** The slice numbers its clauses consecutively
(`C-1`…`C-47` across the four files of `contracts/`) because it inherits 47 of the parent design's
67 clauses and defers 20; each clause is tagged with its parent source as `父 C-nn`, and
`../plan.md` § Parent Design Mapping carries the two-way table. The parent design
(`.specify/specs/074-goal-team-sdd-unification/contracts/`) remains the authority for the deferred
clauses and for the requirement text behind every inherited one.

**C-1** (父 C-2): The routing owner document states one control hierarchy with one boundary: the Goal
is the highest layer, a Team bound to one Goal orchestrates Agent members, an Agent executes a duty,
and an SDD run is a subordinate execution path that an authorized Agent may start. No SDD run may
create, rebind, re-scope, or terminate a Goal, Target, Team, or roster. (FR-001)

**C-2** (父 C-3): The routing owner document defines direct modification as executing a change
without an SDD artifact chain while remaining subject to every applicable quality and confirmation
gate, and distinguishes it from an SDD run. The gate set is cited by path
(`.specify/shared/guidelines/confirmation-gates.md` and the constitution's quality principles), never
restated. (FR-002)

**C-3** (父 C-15): An Agent definition declares SDD invocation capability through the neutral
metadata key [[STR-001]], whose closed values are [[STR-002]] and [[STR-003]]; an absent key means
[[STR-003]]. The key is framework-level: its metadata entry carries `renders_to_tools = False`, is a
member of the framework assembly key set, and MUST NOT be produced in any host tool's rendered agent
fields. (FR-003)

**C-4** (父 C-60): The agent authoring baseline — the framework frontmatter field list owned by the
`run-agent` skill and consumed by the authoring skills — lists the new key, so an authored instance
can declare it and a validator rejects a value outside its closed set. The baseline entry is a
pointer to the key set's owner, not a second definition of the values. (FR-003)

**C-5** (父 C-16): A Team roster seat declares SDD invocation policy through the same key
[[STR-001]] with the same closed values, as a `[[STR-010]]` block map in `team.md` frontmatter keyed
by seat slug. An absent map, an absent entry for the seat, or an absent key inside the entry all mean
[[STR-003]]. An existing team without the key keeps byte-identical behaviour, and no flow back-fills
the key. (FR-004)

**C-6** (父 C-17): The [[STR-010]] map is accepted in block style only. A flow-style map is refused as
malformed input with the seat named, and a seat entry that matches no member role or seat instance is
reported as dangling rather than ignored; neither case degrades to [[STR-002]]. (FR-004)

**C-7** (父 C-18): The dispatch payload carries the team slug, and the authorization probe resolves
the seat policy by (team, seat). Resolution requires both coordinates; a payload that carries only
the seat cannot satisfy the predicate and is refused. (FR-004)

**C-8** (父 C-19): Effective authorization is the logical AND of the Agent capability and the seat
policy, both resolved through one deterministic, read-only engine action
(`scripts/python/sdd-route.py --action authorize`). An SDD run MUST NOT start unless the effective
value is [[STR-002]]. A refusal names which half failed — the Agent side, the seat side, or both —
and records both source paths plus the seat slug so the verdict is recheckable. (FR-004, SC-001)

**C-9** (父 C-20): The anti-nesting obligation is narrowed once, in its existing owner
(`.specify/shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation), to a
decidable predicate: a dispatch prompt may name or assign an SDD driver only when the recipient
resolves to an Agent definition declaring [[STR-002]], its seat policy declares [[STR-002]], and the
assigned task is an SDD assignment. Every dispatch that does not satisfy all three conditions keeps
the original prohibition unchanged; the amendment states the predicate without moving the obligation,
and no second copy of the predicate is created elsewhere. (FR-005)

**C-10** (父 C-21): The pre-dispatch probe in `skills/internal/run-agent/SKILL.md` enforces the
predicate and fails closed: a prompt naming an SDD driver without all three conditions is not
dispatched, and the refusal names the condition that failed. The probe calls the engine action of C-8
rather than re-reading the definitions in prose, so the caller cannot repair a refusal by rewording
the prompt. (FR-005)

**C-11** (父 C-22): The permitted nesting chain is depth 2: team orchestrator → invoking member
(driver host) → stage executor (leaf). The anti-nesting owner states this chain in place of the
unqualified "loop depth is always 1" sentence, and states the three prohibitions in the same place: a
stage executor MUST NOT start or host any SDD run; an SDD stage executor MUST NOT itself be an SDD
invocation host; SDD-within-SDD recursion is prohibited. (FR-006)

**C-12** (父 C-23): A member executed in virtual mode MUST NOT host an SDD run. Virtual execution
occupies the orchestrating session, so hosting a driver inside it collapses the outer layer into the
driver; the probe refuses the dispatch before it leaves and reports the reason. (FR-006)

**C-13** (父 C-24): A member hosts at most one SDD run at a time unless the team declares a higher
per-member cap within the existing line mechanism. No second concurrency primitive is introduced:
overlapping territories are serialized or rejected by the line registry and ownership mechanism of
Feature 064, and the decision cites that mechanism rather than inventing a gate.
(FR-006, FR-018, SC-005)

**C-14** (父 C-29): A refused dispatch produces a record naming the failed condition and the
recipient's resolved values. A record that states only "not authorized" is non-conforming: the two
halves exist precisely so a reader can tell a policy decision from a missing declaration.
(FR-005, SC-001)

**C-15** (父 C-28): Stage executors cannot start an SDD run, and every dispatch prompt that names a
driver without satisfying all three conditions is blocked before dispatch. All pre-existing
anti-nesting contract cases remain green for the paths that do not satisfy the predicate: the
narrowing adds an allowance and removes no prohibition from any path that fails it. (FR-006, SC-004)

**C-16** (父 C-30): The authorization surface adds no confirmation gate, no scheduler, and no second
registry. Its only stored state is the two declared values; everything else is read at probe time
from the definition, the roster, and the line registry. (FR-018)

## Parent Clause Mapping

| Slice clause | Parent clause | Parent contract file | Requirement face |
|--------------|---------------|----------------------|------------------|
| C-1 | C-2 | `route-decision.md` | FR-001 |
| C-2 | C-3 | `route-decision.md` | FR-002 |
| C-3 | C-15 | `authorization-and-probe.md` | FR-003 |
| C-4 | C-60 | `diffusion-and-compat.md` | FR-003 |
| C-5 | C-16 | `authorization-and-probe.md` | FR-004 |
| C-6 | C-17 | `authorization-and-probe.md` | FR-004 |
| C-7 | C-18 | `authorization-and-probe.md` | FR-004 |
| C-8 | C-19 | `authorization-and-probe.md` | FR-004, SC-001 |
| C-9 | C-20 | `authorization-and-probe.md` | FR-005 |
| C-10 | C-21 | `authorization-and-probe.md` | FR-005 |
| C-11 | C-22 | `authorization-and-probe.md` | FR-006 |
| C-12 | C-23 | `authorization-and-probe.md` | FR-006 |
| C-13 | C-24 | `authorization-and-probe.md` | FR-006, FR-018, SC-005 |
| C-14 | C-29 | `authorization-and-probe.md` | FR-005, SC-001 |
| C-15 | C-28 | `authorization-and-probe.md` | FR-006, SC-004 |
| C-16 | C-30 | `authorization-and-probe.md` | FR-018 |

Deferred to `074b-nested-governance` from the same parent file: parent C-25 / C-26 (Agent
responsibility statement, leaf capacity) and parent C-27 (default-`forbidden` containment claim), all
carried by parent FR 023 / FR 026.

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1, C-2 | FR-001, FR-002 | — | `shared/definitions/sdd-routing-definitions.md` § Hierarchy / § Direct modification |
| C-3, C-4 | FR-003 | — | `src/specify_cli/__init__.py`; `run-agent/SKILL.md` authoring baseline |
| C-5, C-6, C-7, C-8, C-14 | FR-004, FR-005 | SC-001 | `team.md` schema; `sdd-route.py --action authorize` |
| C-9, C-10 | FR-005 | SC-004 | `subagent-definitions.md` § Dispatch-Time Governance Obligation; `run-agent/SKILL.md` |
| C-11, C-12, C-15 | FR-006 | SC-004 | same owner site; pre-dispatch governance suite |
| C-13, C-16 | FR-018 | SC-005 | Feature 064 line registry (referenced) |
