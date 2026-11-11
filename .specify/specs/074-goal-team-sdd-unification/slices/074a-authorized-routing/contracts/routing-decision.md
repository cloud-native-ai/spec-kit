# Contracts: Deterministic routing decision (C-17…C-30)

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the routing decision's *mechanics* — the owner document's required
content, the engine's interface and exit alphabet, the golden table's shape, the override record, and
the per-duty application point. The **input value domains, the verdict table, the precedence, and
the reason-code vocabulary are owned by `shared/definitions/sdd-routing-definitions.md`** and are
cited here, never restated.
**Pinned by**: `tests/contract/test_sdd_routing_engine.py`, `tests/contract/test_sdd_routing_definitions.py`
(planned)
**Measures**: SC-002, SC-006

**C-17** (父 C-1): The routing rule has exactly one authoritative owner document at
`shared/definitions/sdd-routing-definitions.md`. Its opening lines declare it as the owner and
enumerate what it owns: the five inputs' closed value domains, the three-value verdict table, the
fixed precedence, and the reason-code vocabulary. No other document, table, YAML file, or code
constant declares a second copy of any of those four facts. (FR-014)

**C-18** (父 C-4): The decision consumes exactly five declared inputs — change nature, whether
durable traceability is required, blast radius, reversibility, and the Task Complexity Rubric tier.
Each input's closed value domain is declared in the owner document, and no sixth input carries the
surface class. The change-nature domain is `change_nature ∈ {feature, maintenance, definition-class}`,
where `feature` declares a capability or contract change and `maintenance` declares their
preservation, so C-21's first condition and C-22's first condition are read off this input instead
of an unmapped one. Membership of `definition-class` is derived from the target path by the
predicate owned by `../requirements.md` FR-008 (this file does not repeat the path roots). The
decision MUST NOT consume implementation medium, file extension, language, artifact count, or author
identity — the path predicate of FR-008 is the sole read of the target path, and the owner document
states that prohibition as a rule rather than a preference. (FR-008)

**C-19** (父 C-5): The Task Complexity Rubric tier input carries the rubric's own four tier names as
its closed domain and cites `.specify/shared/guidelines/task-complexity-rubric.md` as the tier owner.
The owner document MUST NOT restate the rubric's signals, its table, or its depth prescriptions; a
tier rename in the rubric reaches the routing decision by reference. (FR-008)

**C-20** (父 C-6): A `definition-class` change is classified cross-cutting by default, because the
surface it lands on defines the behaviour of other surfaces; the default is a property of the
change-nature value, not of a separately supplied class flag. The bounded-correction escape is a
distinct declared blast-radius value requiring a non-empty rationale, and a caller cannot declare a
plain local radius for a `definition-class` change and have it accepted as equivalent. Membership of
the `definition-class` value is decided by the target-path predicate owned by `../requirements.md`
FR-008; this file cites it and does not repeat the path roots. (FR-008, FR-010)

**C-21** (父 C-7): The decision returns [[STR-004]] when any of the following holds: the declared
change nature is `feature` (the change adds or alters a capability or contract); durable
traceability is required; the blast radius is cross-cutting; the change is irreversible or hard to
reverse; or the complexity tier is Complex or High-stakes. (FR-009)

**C-22** (父 C-8): The decision returns [[STR-005]] only when all of the following hold together: the
declared change nature is not `feature`, so every existing capability and contract is preserved; no
durable traceability is required; the blast radius is local; the change is reversible; the complexity
tier is Trivial or Standard; and, for a `definition-class` change, the caller declares a bounded
correction with a recorded rationale. A single unmet condition removes the [[STR-005]] verdict.
(FR-010)

**C-23** (父 C-9): One fixed precedence governs every call: [[STR-006]] first, then [[STR-004]], then
[[STR-005]]. The decision returns [[STR-006]] whenever a required input is missing, is ambiguous (a
value outside the declared closed domain), or the inputs conflict; only in the non-adjudicate branch
does the definition-class cross-cutting default apply. The decision MUST NOT silently default to
[[STR-005]], and every verdict carries its inputs plus a reason code from the owner's closed
vocabulary. (FR-011, SC-006)

**C-24** (父 C-10): The conflict condition is a closed enumerated set declared in the owner
document, not a free judgement: a declared `feature` change paired with a declared bounded definition
correction. Every other input combination is either consistent (one branch applies) or
non-conflicting, so the [[STR-004]] branch's categorical rules stay reachable. When several
conditions trigger at once, the verdict follows the precedence and the record states every triggered
condition, with the reason code taken by the owner's declared order so that two evaluations of the
same inputs yield byte-identical output. (FR-011, SC-002)

**C-25** (父 C-11): An explicit user instruction overrides the verdict. The override is recorded as an
adjudication containing the user's instruction verbatim, the overridden verdict, and the reason code
FR-011 requires of every verdict — an adjudication is a verdict record, so the reason code is
mandatory rather than optional. The engine MUST NOT override the user and MUST NOT discard the
overridden verdict from the record. (FR-012)

**C-26** (父 C-12): The decision is applied once per declared member duty before that duty performs a
write-bearing change — a change that writes a tracked file (source, configuration, definition, or
documentation), as defined by `../requirements.md` FR-007; a read-only analysis that writes no tracked
file needs no verdict — and the verdict is reused for that duty until one of its inputs changes. On an
input change the decision is re-applied, the earlier verdict is retained in the record, and the new
verdict supersedes its effect. (FR-013)

**C-27** (父 C-54, FR-013 facet — see `## Cross-Slice Design Attribution` D-2 in
`../requirements.md`): the carrier of the recorded verdict in this slice is the Agent execution
evidence; the invoker's result and the nested run's handoff reach that record by stable path. The
carrier holds a **reference** to the recorded verdict and never a re-derived one, so the outer layer
reads the same verdict the duty acted on. The team run report's own nested section, and the verdict
reference it will carry, arrive with `074b-nested-governance`; that section reads the same record and
never recomputes it. (FR-013)

**C-28** (父 C-13): The decision is implemented by one deterministic, read-only, stdlib-only engine at
`scripts/python/sdd-route.py` exposing three actions — `route`, `authorize`, `golden` — and the
engine takes the value domains, verdict table, precedence, and reason codes from the owner document
at run time. The engine MUST NOT carry a second copy of any of them and MUST NOT write any file.
The exit alphabet is shared by the two verdict-producing actions and carries exactly two meanings:
`0` whenever a verdict is produced and `2` for input errors, and nothing else. For `route` that means
`0` including the [[STR-006]] verdict — an exit code that conflated "adjudicate" with "engine
failure" would make the two indistinguishable to the caller that must record the first and repair
the second. For `authorize` it means `0` for **any** authorization verdict, whether the effective
value is [[STR-002]] or [[STR-003]]: a refusal is a produced verdict, expressed by the JSON verdict
and reason fields (C-8), not by the process exit status; only malformed or unreadable input exits
`2`. No third exit code exists on either action. (FR-007)

**C-29** (父 C-14): The owner document carries the golden case table as a Markdown table whose rows
name a case id, the five input values, the expected verdict, the expected reason code, and the
requirement face covered. Rows cover at least: a feature-scale change, a bounded maintenance change,
a cross-cutting change, an irreversible change, an ambiguous input set, a conflicting input set, and
a bounded definition correction that satisfies every remaining condition. `--action golden` parses
and judges every row; re-evaluating a row returns an identical verdict and reason code, and no second
copy of the rows exists in test code or in a separate data file. (FR-007, SC-002)

**C-30** (父 C-66, FR-014 facet): No surface produced by this slice enumerates a roster, a threshold,
or a value domain that another document owns. The owner document is the only place the routing
facts are written out, and every other new surface — the anti-nesting amendment, the driver entry
form, the execution-evidence record shape — reaches them by path. (FR-014)

## Parent Clause Mapping

| Slice clause | Parent clause | Parent contract file | Requirement face |
|--------------|---------------|----------------------|------------------|
| C-17 | C-1 | `route-decision.md` | FR-014 |
| C-18 | C-4 | `route-decision.md` | FR-008 |
| C-19 | C-5 | `route-decision.md` | FR-008 |
| C-20 | C-6 | `route-decision.md` | FR-008, FR-010 |
| C-21 | C-7 | `route-decision.md` | FR-009 |
| C-22 | C-8 | `route-decision.md` | FR-010 |
| C-23 | C-9 | `route-decision.md` | FR-011, SC-006 |
| C-24 | C-10 | `route-decision.md` | FR-011, SC-002 |
| C-25 | C-11 | `route-decision.md` | FR-012 |
| C-26 | C-12 | `route-decision.md` | FR-013 |
| C-27 | C-54 | `report-and-attribution.md` | FR-013 (D-2 facet) |
| C-28 | C-13 | `route-decision.md` | FR-007 |
| C-29 | C-14 | `route-decision.md` | FR-007, SC-002 |
| C-30 | C-66 | `diffusion-and-compat.md` | FR-014 (facet) |

Deferred to `074b-nested-governance`: parent C-54's report-section facet (the `## Nested SDD Runs`
verdict reference) together with parent C-47…C-53, and parent C-66's Stage-vocabulary facet
(parent FR 022).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-17, C-30 | FR-014 | — | `shared/definitions/sdd-routing-definitions.md` (declaration + single point) |
| C-18, C-19, C-20 | FR-008, FR-010 | — | owner document § Inputs / § Definition-class default |
| C-21, C-22 | FR-009, FR-010 | — | owner document § Verdict table |
| C-23, C-24 | FR-011 | SC-002, SC-006 | owner document § Precedence / § Conflict set; `sdd-route.py --action route` |
| C-25 | FR-012 | — | owner document § User override |
| C-26, C-27 | FR-013 | — | Agent execution evidence record; `sdd-route.py --action route` |
| C-28, C-29 | FR-007 | SC-002 | `scripts/python/sdd-route.py`; owner document § Golden case table |
