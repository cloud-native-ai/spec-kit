# Feature Reference: 074-goal-team-sdd-unification

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Bound at**: `/speckit.clarify` 2026-10-28 (the requirement key is the spec directory; the Feature ID is 074, already registered in `.specify/memory/features.md`)
**Status ceiling of this stage**: `Planned` (the `Implemented` transition belongs to `/speckit.implement`)

## 1. Binding

| Axis | Value |
|------|-------|
| Requirement key | `074-goal-team-sdd-unification` |
| Feature ID / name | 074 Goal/Team/Agent 与 SDD 开发流程统一 |
| Feature index row | `.specify/memory/features.md` (row 074) |
| Feature detail | `.specify/memory/features/074.md` |
| Specification | `.specify/specs/074-goal-team-sdd-unification/requirements.md` |
| Related features | 058 (driver U0–U6, state spine, sentinels — referenced, preserved), 060 (Agent Template/Instance/Execution + neutral key set — extended), 064 (line registry / worktree / ownership — reused as the only concurrency primitive), 069/052 (flow class, fast-fail — referenced), 070 (in-run work packages + stage-team preset — preserved) |

This plan maps onto Feature 074 as a **cross-layer capability feature**: it adds one vocabulary
owner, one neutral metadata key, one seat-policy field, one deterministic engine, one narrowing
amendment to an existing obligation, one report section, and one driver entry form. It creates no
new command, no new skill, and no new store.

## 2. Delivery surface

**Hat declared**: every row below is a **framework-source** edit, which reaches client projects
through publish → install → `specify init`. No row is a hand edit to this repository's `.specify/`
runtime copies; the runtime projections in rows M1–M5 are produced by the mirror and generator
machinery.

| # | Path | Kind | Purpose |
|---|------|------|---------|
| 1 | `shared/definitions/sdd-routing-definitions.md` | NEW | The routing owner: five input value domains, three-value verdict table, precedence, reason-code vocabulary, invocation-kind classification, golden case table |
| 2 | `shared/definitions/subagent-definitions.md` | EDIT | § Dispatch-Time Governance Obligation: narrow the anti-nesting obligation to the three-condition predicate + depth-2 chain + virtual prohibition (one amendment, in place) |
| 3 | `src/specify_cli/__init__.py` | EDIT | `sdd-invocation` added to `NEUTRAL_AGENT_METADATA_KEYS` (closed domain, default `forbidden`, no host rendering) and to `NEUTRAL_AGENT_FRAMEWORK_KEYS` |
| 4 | `scripts/python/sdd-route.py` | NEW | Read-only stdlib engine: `--action route\|authorize\|golden`, parsing the owner document at run time |
| 5 | `skills/internal/run-agent/SKILL.md` | EDIT | Pre-dispatch probe enforces the predicate fail-closed; authoring baseline lists the new key |
| 6 | `skills/internal/create-team/SKILL.md` | EDIT | § Report contract gains the mandatory `## Nested SDD Runs` section |
| 7 | `skills/internal/create-team/references/create-mode.md` | EDIT | `team.md` schema gains the `seats:` block map |
| 8 | `skills/internal/create-team/references/conceptual-model.md` | EDIT | Team Stage dimension disambiguated from the SDD stage roster |
| 9 | `skills/external/sdd-loop-driver/SKILL.md` | EDIT | New § Invoked-from-Team Entry (six accepted facts, validation, stop-at-review) + one Hard Requirement line; standalone entry contract unchanged |
| 10 | `skills/external/sdd-loop-driver/references/nested-invocation.md` | NEW | Handoff schema, closed field set, entry-validation table, failure/stall handoff |
| 11 | `templates/instructions-template.md` | EDIT | One pointer-level routing ambient section (no input set, no verdict table) |
| 12 | `shared/guidelines/proactive-trigger.md` | EDIT | One pointer sentence: promotion needs both a routing verdict and effective authorization |
| 13 | `tests/contract/test_sdd_routing_definitions.py` | NEW | Owner-document shape: declaration, closed domains, single declaration point |
| 14 | `tests/contract/test_sdd_routing_engine.py` | NEW | Determinism, precedence, reason codes, idempotence, golden table |
| 15 | `tests/contract/test_sdd_authorization.py` | NEW | Two halves, AND, defaults, malformed seat map, failed half named |
| 16 | `tests/contract/test_sdd_invocation_governance.py` | NEW | Pre-dispatch predicate, depth-2 chain, virtual prohibition, containment (superset + same verdict) |
| 17 | `tests/contract/test_nested_sdd_invocation.py` | NEW | Entry validation, stop at review, handoff field set, zero merge/push, stall handoff |
| 18 | `tests/contract/test_nested_run_report.py` | NEW | `## Nested SDD Runs` mandatory + explicit-when-empty, ledger attribution, no new Goal field |
| 19 | `tests/fixtures/nested_sdd.py` | NEW | Temp repo with minimal `.specify/`, two seats (allowed/forbidden), two agent definitions, one goal with an open Target |
| 20 | `tests/contract/test_neutral_metadata_schema.py` | EDIT | The single declared pin change (R12): the framework-key frozenset gains exactly one member |

**Generated / mirrored projections** (not hand-edited; see plan.md § Mirror Obligations): rows
1–2 and 12 → `.specify/shared/…`; rows 5–10 → `.specify/skills/…`; row 4 →
`.specify/scripts/python/…`; row 11 → `.specify/templates/…`; row 11 also regenerates
`.specify/instructions.md` through `scripts/bash/generate-instructions.sh`, which the
compatibility symlinks already point at. No `templates/commands/**` file changes, so
`regen-command-copies.py` has nothing to regenerate.

## 3. FR coverage

| FR | Owning clause(s) | Surface |
|----|------------------|---------|
| FR-001 | C-2 | routing owner § Hierarchy |
| FR-002 | C-3 | routing owner § Direct modification |
| FR-003 | C-15, C-60 | CLI neutral key set; authoring baseline |
| FR-004 | C-16, C-17, C-18, C-19 | `seats` map; payload; AND resolution |
| FR-005 | C-20, C-21, C-29, C-59 | anti-nesting owner; pre-dispatch probe |
| FR-006 | C-22, C-23, C-24 | depth-2 chain; virtual prohibition; per-member cap |
| FR-007 | C-13, C-14 | engine; golden table |
| FR-008 | C-4, C-5, C-6 | five inputs; rubric reference; definition-class default |
| FR-009 | C-7 | SDD branch conditions |
| FR-010 | C-6, C-8 | direct branch conditions |
| FR-011 | C-9, C-10 | precedence; conflict set |
| FR-012 | C-11 | user override |
| FR-013 | C-12, C-54 | per-duty application; verdict reference carrier |
| FR-014 | C-1, C-5, C-13, C-14, C-66 | single owner; no restatement |
| FR-015 | C-31, C-32 | invoked-from-team entry; validation |
| FR-016 | C-34, C-35, C-36, C-37, C-38, C-46 | stop at review; handoff; integration identity |
| FR-017 | C-36, C-41, C-46 | consumer duty |
| FR-018 | C-24, C-30, C-39, C-64 | line registry reuse; no second store |
| FR-019 | C-40 | stall handoff |
| FR-020 | C-50, C-51, C-52 | supervisor-only writes; ledger attribution; no Goal field |
| FR-021 | C-47, C-48, C-49, C-53, C-54 | report contract section |
| FR-022 | C-55, C-66 | Stage disambiguation; no roster enumeration |
| FR-023 | C-25, C-26, C-60 | host declares `allowed`; leaf stays leaf |
| FR-024 | C-56, C-57 | instructions pointer; trigger conjunction |
| FR-025 | C-45, C-58, C-59, C-67 | invocation kinds; setup path |
| FR-026 | C-16, C-27, C-28, C-62, C-65 | default `forbidden`; containment |
| FR-027 | C-33, C-43, C-44, C-61, C-62 | additive on four surfaces; containment |
| FR-028 | C-30, C-63, C-67 | no new machinery |

## 4. SC coverage

| SC | Owning clause(s) | Measurement source |
|----|------------------|--------------------|
| SC-001 | C-19, C-29 | `test_sdd_authorization.py` + fixture team (allowed/forbidden seats) |
| SC-002 | C-10, C-13, C-14 | `test_sdd_routing_engine.py` + `--action golden` judged twice per row |
| SC-003 | C-42, C-48 | `test_nested_sdd_invocation.py` + report assertions over paths, `git log`, `git status` |
| SC-004 | C-28, C-65 | `test_sdd_invocation_governance.py` + the pre-existing anti-nesting cases |
| SC-005 | C-27, C-33, C-43, C-44, C-61, C-62 | frozen node-id case sets at `7831bb4bb` vs post-change, superset + same verdict |
| SC-006 | C-2, C-24, C-30, C-39, C-64 | structure check over the changed tree + line-registry reuse assertion |
| SC-007 | C-9, C-14 | golden-table rows filtered to missing/ambiguous/conflicting |
| SC-008 | C-51, C-52 | goal fixture parsed before/after; field-set equality |

## 5. Disclosed rulings

1. **Same-author scoring not delegated** (R13): no subagent capability in this environment and the
   stage brief fixes `decomposition=single-package`; every Constitution Check row is a direct read,
   and the program-derivable checks were executed instead.
2. **One intentional pin change** (R12): the framework-key frozenset literal in
   `test_neutral_metadata_schema.py` gains exactly one member in the same change as the code edit.
3. **No new shipped Agent preset** (R9): FR-023 is implemented as a conditional conformance rule;
   no FR names a preset to create.
4. **Seat map is block-style only** (R3): a flow-style map is malformed input, not best-effort
   parsed.
5. **The engine's exit code does not encode the verdict** (C-13): `adjudicate` is data, not an
   error, so a caller cannot mistake "needs adjudication" for "engine broke".
6. **Instructions size budget already exceeded at baseline** (R8): 41,948 B against a 32,768 B
   budget before this feature; the criterion is a declared per-section ceiling plus a measured
   delta, never an absolute pass.
7. **Golden table lives in the owner document** (R10): no second copy in test code or a data file.

## 6. Non-regression statement

The feature's containment claims are the two in FR-026/FR-027 plus SC-005. Their discharge is
mechanical (C-62): the named suites' collected test-node-id sets are frozen at the pre-change
commit `7831bb4bb`, and the post-change check asserts set containment plus identical verdicts for
shared ids. Everything else in the targeted set is expected to stay green unchanged; the only
intentional change to an existing assertion is item 2 of § 5.
