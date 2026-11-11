# Contracts: Compatibility, containment and safety (C-1…C-12)

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns this slice's two containment claims and its negative safety boundary. The
authorization resolution, the pre-dispatch probe, the routing decision, the line registry, the
state-spine format, the stage roster and the stage-team preset are **cited by path, never
re-specified**: they belong to `074a-authorized-routing`
(`scripts/python/sdd-route.py`, `shared/definitions/sdd-routing-definitions.md`), Feature 058
(`skills/external/sdd-loop-driver/SKILL.md`), Feature 064 (`.../scripts/line-registry.py`) and
Feature 070 (its preset contract).
**Pinned by**: `tests/contract/test_sdd_compat_containment.py` (planned),
`tests/contract/test_sdd_invocation_governance.py` (edited)
**Measures**: SC-001
**Parent source**: `parent C-27`, `parent C-65`, `parent C-61`, `parent C-62`, `parent C-33`,
`parent C-43`, `parent C-44`, `parent C-63`, `parent C-67` (parent FR 028 facet) — see `plan.md`
§ Parent Design Mapping for the per-entry attribution.

**C-1**: An Agent definition or Team seat that carries no `[[STR-001]]` declaration resolves to
`[[STR-003]]`, and the pre-dispatch probe rejects any dispatch for that recipient that names an SDD
driver. The resolution itself is `074a`'s implemented surface
(`scripts/python/sdd-route.py --action authorize`, `shared/definitions/subagent-definitions.md`
§ Dispatch-Time Governance Obligation) and is consumed here by reference (FR-006, SC-001).
*(parent C-27, first sentence)*

**C-2**: The absence of a declaration changes nothing else about that recipient's dispatch: no other
key's resolution, no payload field, and no failure message form is altered, so a pre-change dispatch
that did not name a driver keeps its pre-change behaviour bit for bit (FR-006).
*(parent C-65)*

**C-3**: As a decidable containment claim over the pre-dispatch governance suite: relative to the
baseline case set captured at the pre-change commit named in the verification record, the post-change
case set is a superset, and every pre-change case returns the same verdict. The claim is discharged
mechanically and its carrier is `test-evidence/compat-baseline-nodeids.txt`, set `S1`
(FR-006, SC-001). *(parent C-27, second sentence)*

**C-4**: The containment claim is discharged over **collected test-node-id sets**, not over counts and
not over test modules: the case set of each named suite is its `pytest --collect-only` node-id set,
frozen before any edit at the baseline commit named in the verification record; the post-change check
asserts set containment (post ⊇ pre) and, for the shared ids, identical verdicts. A count comparison
is non-conforming, because one renamed case and one added case net to zero and would hide a dropped
obligation (FR-006, FR-007, SC-001). *(parent C-62)*

**C-5**: The slice is additive on the four named surfaces: the standalone `sdd-loop-driver` entry
contract, the Feature 070 stage-team preset contract, the Feature 064 line/worktree/ownership
contract, and the Feature 058 U0–U6 contract. On each surface no existing key, section, entry form, or
exit code is removed, renamed, or changed in meaning; additions are permitted (FR-007, SC-001).
*(parent C-61)*

**C-6**: For each of the four surfaces the post-change contract-suite case set is a superset of the
pre-change case set captured at the baseline commit named in the verification record, and every
pre-change case passes. The carriers are sets `S2` (standalone driver entry), `S3` (070 preset),
`S4` (064 line/worktree/ownership) and `S5` (058 U0–U6) of
`test-evidence/compat-baseline-nodeids.txt` (FR-007, SC-001). The team suite (`S6`) and Agent suite
(`S7`) in the same carrier are the SC-001 carriers for those two surfaces and are read with the same
superset-and-verdict rule. *(parent C-61)*

*Reading rule for C-3 and C-6, and for the set both claims reach (S2, the standalone-driver entry
suite named by FR-006/SC-001 and one of C-6's four surfaces)*: the criterion for a case id that is
**already red in the pre-change baseline** is **verdict-unchanged** — the post-change verdict equals
the pre-change verdict, red included — and the "every pre-change case MUST pass" criterion of FR-007 /
C-6 applies only to case ids that are **green** in that baseline. The two readings are therefore not
alternatives to be chosen between: on the shared set `S2` they are read jointly by this rule, so a
pre-existing red is neither required to be repaired (T023 forbids it) nor counted as an added failure,
while a case that turns red after the change still fails the claim (FR-006, FR-007, SC-001).

**C-7**: The nested entry form stays additive on the standalone entry contract: the standalone
default-resolution behaviour is unchanged, and the nested form remains a distinct entry whose
semantics are validation-then-refuse rather than default-resolution. This slice adds no fact to that
form and no branch to its validation (FR-007). *(parent C-33)*

**C-8**: Feature 070's stage-team preset remains the in-run decomposition mechanism: work packages
stay the only in-run decomposition, the preset is not a substitute for nested invocation, and nested
invocation is not a substitute for the preset. No preset key, section, or entry form changes, and this
slice's report section does not describe work packages (FR-007). *(parent C-43)*

**C-9**: Feature 058's U0–U6 contract is preserved: this slice changes no stage semantics, sentinel,
independent-verification rule, watcher verdict or exit code, stall disposition, fast-lane rule, or
test-budget rule. The report section records an outcome and paths; it introduces no stage and no
sentinel (FR-007). *(parent C-44)*

**C-10**: The framework adds no automatic merge or push, no scheduler or daemon, no automatic feedback
transmission, and no second confirmation gate. Every integration decision remains with the outer layer
under its existing confirmation-gate discipline, and the report section's outcome is data, never an
authorization to integrate (FR-008). *(parent C-63)*

**C-11**: The slice adds no new `/speckit.*` command and no new skill: every capability lands on an
existing command, skill, engine, template, or shared definition, and the delivered file set is a diff
of those owners. The flow-class inventory therefore keeps its unit count and finding count (FR-008).
*(parent C-67, parent FR 028 facet. Requirement anchor: `requirements.md` § Overview prose — "no new
command, no new skill, no new store" — **rated prose-level**: FR-008's four prohibitions do not name
commands or skills, so this clause is a prose-anchored design obligation, not an FR clause claim)*

**C-12**: The slice adds no store: the report section is text inside an existing report, the
attribution row is one item in the existing team ledger, the pointer surfaces are sections of existing
documents, and the containment carrier is a test-evidence artifact. No registry, ledger, state spine,
ownership model, integration queue, or second state store is introduced (FR-008). *(parent C-30 and
parent C-64 cited, both delivered by other owners)*

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-1, C-2, C-3 | FR-006 | SC-001 | default-`forbidden` resolution (074a surface, cited); `test-evidence/compat-baseline-nodeids.txt` set S1 |
| C-4, C-6 | FR-006, FR-007 | SC-001 | frozen node-id sets, 7 named sets / 17 files |
| C-5, C-7, C-8, C-9 | FR-007 | SC-001 | the four predecessor surfaces (cited, unchanged) |
| C-10, C-11 | FR-008 | — | repo-wide negative checks |
| C-12 | FR-008 | — | structure check over the changed tree |
