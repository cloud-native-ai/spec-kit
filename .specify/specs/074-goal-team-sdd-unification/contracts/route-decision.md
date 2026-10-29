# Contracts: Routing decision (C-1…C-14)

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the routing decision's *mechanics* — the owner document's required
content, the engine's interface and exit alphabet, the golden table's shape, the override
record, and the per-duty application point. The **input value domains, the verdict table, the
precedence, and the reason-code vocabulary are owned by
`shared/definitions/sdd-routing-definitions.md`** and are cited here, never restated.
**Pinned by**: `tests/contract/test_sdd_routing_engine.py`,
`tests/contract/test_sdd_routing_definitions.py` (planned)
**Measures**: SC-002, SC-007

**C-1**: The routing rule has exactly one authoritative owner document at
`shared/definitions/sdd-routing-definitions.md`. Its opening lines declare it as the owner and
enumerate what it owns: the five inputs' closed value domains, the three-value verdict table,
the fixed precedence, and the reason-code vocabulary. No other document, table, YAML file, or
code constant declares a second copy of any of those four facts (FR-014).

**C-2**: The owner document states one control hierarchy and one boundary for it: Goal is the
highest layer, a Team bound to one Goal orchestrates Agent members, an Agent executes a duty, an
SDD run is a subordinate execution path an authorized Agent may start, and no SDD run may
create, rebind, re-scope, or terminate a Goal, Target, Team, or roster (FR-001, SC-006).

**C-3**: The owner document defines direct modification as executing a change without an SDD
artifact chain while remaining subject to every applicable quality and confirmation gate, and
distinguishes it from an SDD run. The gate set itself is cited by path
(`shared/guidelines/confirmation-gates.md`, the constitution's quality principles), never
restated (FR-002).

**C-4**: The decision consumes exactly five declared inputs — change nature, whether durable
traceability is required, blast radius, reversibility, and the Task Complexity Rubric tier. Each
input's closed value domain is declared in the owner document. The decision MUST NOT consume
implementation medium, file extension, language, artifact count, or author identity, and the
owner document states that prohibition as a rule rather than a preference (FR-008).

**C-5**: The Task Complexity Rubric tier input carries the rubric's own four tier names as its
closed domain and cites `shared/guidelines/task-complexity-rubric.md` as the tier owner. The
owner document MUST NOT restate the rubric's signals, its table, or its depth prescriptions; a
tier rename in the rubric reaches the routing decision by reference (FR-008, FR-014).

**C-6**: Changes to definition-class surfaces — the constitution, the project instructions,
Agent/Skill/Team definitions, and the templates that generate them — are declared `cross-cutting`
by default. The bounded-correction escape is a distinct declared blast-radius value requiring a
non-empty rationale; the value's semantics are owned by the owner document, so a caller can
declare a bounded correction but cannot declare a plain local radius for a definition-class
surface and have it accepted as equivalent (FR-008, FR-010).

**C-7**: The decision returns the SDD verdict when any of the following holds: the change adds or
alters a capability or contract; durable traceability is required; the blast radius is
cross-cutting; the change is irreversible or hard to reverse; the complexity tier is Complex or
High-stakes (FR-009).

**C-8**: The decision returns the direct verdict only when all of the following hold together:
the change preserves every existing capability and contract; no durable traceability is
required; the blast radius is local; the change is reversible; the complexity tier is Trivial or
Standard; and, for a definition-class surface, the change is declared a bounded correction with a
recorded rationale. A single unmet condition removes the direct verdict (FR-010).

**C-9**: One fixed precedence governs every call: adjudicate first, then SDD, then direct. The
decision returns adjudicate whenever a required input is missing, is ambiguous (a value outside
the declared closed domain), or the inputs conflict; only in the non-adjudicate branch does the
definition-class cross-cutting default apply. The decision MUST NOT silently default to direct,
and every verdict carries its inputs plus a reason code from the owner's closed vocabulary
(FR-011, SC-007).

**C-10**: The conflict condition is a closed enumerated set declared in the owner document, not a
free judgement: a declared capability change paired with a declared bounded definition
correction. Every other input combination is either consistent (one branch applies) or
non-conflicting, so the SDD branch's categorical rules stay reachable. When several conditions
trigger at once, the verdict follows the precedence and the record states every triggered
condition, with the reason code taken by the owner's declared order so that two evaluations of
the same inputs yield byte-identical output (FR-011, SC-002).

**C-11**: An explicit user instruction overrides the verdict. The override is recorded as an
adjudication containing the user's instruction verbatim and the overridden verdict. The engine
MUST NOT override the user and MUST NOT discard the overridden verdict from the record
(FR-012).

**C-12**: The decision is applied once per declared member duty before that duty performs a
write-bearing change, and the verdict is reused for that duty until one of its inputs changes.
On an input change the decision is re-applied, the earlier verdict is retained in the record, and
the new verdict supersedes its effect. The verdict with its inputs and reason code is recorded in
the team run report or the Agent execution evidence in a form the outer layer can consume
(FR-013).

**C-13**: The decision is implemented by one deterministic, read-only, stdlib-only engine at
`scripts/python/sdd-route.py` exposing three actions — `route`, `authorize`, `golden` — and the
engine takes the value domains, verdict table, precedence, and reason codes from the owner
document at run time. The engine MUST NOT carry a second copy of any of them and MUST NOT write
any file. `route` exits `0` whenever a verdict is produced, including the adjudicate verdict,
because an exit code that conflated "adjudicate" with "engine failure" would make the two
indistinguishable to the caller that must record the first and repair the second; input errors
exit `2` (FR-007, FR-014).

**C-14**: The owner document carries the golden case table as a Markdown table whose rows name a
case id, the five input values, the expected verdict, the expected reason code, and the
requirement face covered. Rows cover at least: a feature-scale change, a bounded maintenance
change, a cross-cutting change, an irreversible change, an ambiguous input set, a conflicting
input set, and a bounded definition correction that satisfies every remaining condition.
`--action golden` parses and judges every row; re-evaluating a row returns an identical verdict
and reason code. No second copy of the rows exists in test code or in a separate data file
(FR-007, FR-011, SC-002, SC-007).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1, C-2, C-3, C-4, C-5, C-6, C-10 | FR-014, FR-001, FR-002, FR-008 | — | `shared/definitions/sdd-routing-definitions.md` |
| C-7, C-8, C-9, C-11 | FR-009, FR-010, FR-011, FR-012 | SC-007 | owner document § Verdict table / § Precedence |
| C-12, C-13 | FR-013, FR-007 | SC-002 | `scripts/python/sdd-route.py` |
| C-14 | FR-007, FR-011 | SC-002, SC-007 | owner document § Golden case table |
