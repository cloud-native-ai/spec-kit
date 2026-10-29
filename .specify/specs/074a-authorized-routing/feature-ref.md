# Feature Reference: 074a-authorized-routing

**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Bound at**: `/speckit.clarify` 2026-10-28 for the parent requirement, reused here — the slice binds to Feature 074 by `Related Feature` and creates no Feature row of its own (registered as a slice of Feature 074 at `939766891`)
**Status ceiling of this stage**: `Planned` (the `Implemented` transition belongs to `/speckit.implement`)

## 1. Binding

| Axis | Value |
|------|-------|
| Requirement key | `074a-authorized-routing` |
| Feature ID / name | 074 Goal/Team/Agent 与 SDD 开发流程统一 (slice `074a-authorized-routing`) |
| Feature index row | `.specify/memory/features.md` (row 074 — **unchanged**; the slice adds no row) |
| Feature detail | `.specify/memory/features/074.md` |
| Specification | `.specify/specs/074a-authorized-routing/requirements.md` |
| Parent design (authority) | `.specify/specs/074-goal-team-sdd-unification/` — `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, `research.md`, `feature-ref.md` @ `6297c14f6` |
| Split record | `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28，`confirmed-user`） |
| Sibling slice | `074b-nested-governance` (parent FR 020–024 and FR 026–028; not started) |
| Related features | 058 (driver U0–U6, state spine, sentinels — referenced, preserved), 060 (Agent Template/Instance/Execution + neutral key set — extended), 064 (line registry / worktree / ownership — reused as the only concurrency primitive), 069/052 (flow class, fast-fail — referenced), 070 (in-run work packages + stage-team preset — referenced, unchanged) |

This slice maps onto Feature 074 as the **MVP half** of a cross-layer capability feature: it adds one
vocabulary owner, one neutral metadata key, one seat-policy field, one deterministic engine, one
narrowing amendment to an existing obligation, and one driver entry form — while delivering the
routing decision and the governed depth-2 nesting predicate that make the hierarchy safe. It creates
no new command, no new skill, and no new store.

## 2. Delivery surface

**Hat declared**: every row below is a **framework-source** edit, which reaches client projects
through publish → install → `specify init`. No row is a hand edit to this repository's `.specify/`
runtime copies; the runtime projections in rows M1–M4 are produced by the mirror machinery.

| # | Path | Kind | Purpose |
|---|------|------|---------|
| 1 | `shared/definitions/sdd-routing-definitions.md` | NEW | The routing owner: five input value domains, three-value verdict table, precedence, reason-code vocabulary, invocation-kind classification, golden case table |
| 2 | `shared/definitions/subagent-definitions.md` | EDIT | § Dispatch-Time Governance Obligation: narrow the anti-nesting obligation to the three-condition predicate + depth-2 chain + virtual prohibition (one amendment, in place) |
| 3 | `src/specify_cli/__init__.py` | EDIT | `sdd-invocation` added to `NEUTRAL_AGENT_METADATA_KEYS` (closed domain, default `forbidden`, no host rendering) and to `NEUTRAL_AGENT_FRAMEWORK_KEYS` |
| 4 | `scripts/python/sdd-route.py` | NEW | Read-only stdlib engine: `--action route\|authorize\|golden`, parsing the owner document at run time |
| 5 | `skills/internal/run-agent/SKILL.md` | EDIT | Pre-dispatch probe enforces the predicate fail-closed; authoring baseline lists the new key |
| 6 | `skills/internal/create-team/references/create-mode.md` | EDIT | `team.md` schema gains the `seats:` block map |
| 7 | `skills/external/sdd-loop-driver/SKILL.md` | EDIT | New § Invoked-from-Team Entry (six accepted facts, validation, stop-at-review) + one Hard Requirement line; standalone entry contract unchanged |
| 8 | `skills/external/sdd-loop-driver/references/nested-invocation.md` | NEW | Handoff schema, closed field set, entry-validation table, failure/stall handoff |
| 9 | `tests/contract/test_sdd_routing_definitions.py` | NEW | Owner-document shape: declaration, closed domains, single declaration point, invocation kinds |
| 10 | `tests/contract/test_sdd_routing_engine.py` | NEW | Determinism, precedence, reason codes, idempotence, golden table |
| 11 | `tests/contract/test_sdd_authorization.py` | NEW | Two halves, AND, defaults, malformed seat map, failed half named |
| 12 | `tests/contract/test_sdd_invocation_governance.py` | NEW | Pre-dispatch predicate, depth-2 chain, virtual prohibition, pre-existing cases stay green |
| 13 | `tests/contract/test_nested_sdd_invocation.py` | NEW | Entry validation, stop at review, handoff field set, zero merge/push, stall handoff, path references (D-3) |
| 14 | `tests/fixtures/nested_sdd.py` | NEW | Temp repo with minimal `.specify/`, two seats (allowed/forbidden), two agent definitions, one goal with an open Target |
| 15 | `tests/contract/test_neutral_metadata_schema.py` | EDIT | The single declared pin change (RA8): the framework-key frozenset gains exactly one member |

**Generated / mirrored projections** (not hand-edited; see `plan.md` § Mirror Obligations): rows 1–2 →
`.specify/shared/…`; rows 5–8 → `.specify/skills/…`; row 4 → `.specify/scripts/python/…`. No
`templates/**` file changes and no `templates/commands/**` file changes, so neither
`generate-instructions.sh` nor `regen-command-copies.py` has anything to regenerate for this slice.

**Deferred to `074b-nested-governance`** (parent delivery rows, listed so the omission is not read as
an oversight): `skills/internal/create-team/SKILL.md` § Report contract (`## Nested SDD Runs`),
`skills/internal/create-team/references/conceptual-model.md` (Stage-vocabulary disambiguation),
`templates/instructions-template.md` (routing pointer section), `shared/guidelines/proactive-trigger.md`
(promotion conjunction), and `tests/contract/test_nested_run_report.py`.

## 3. FR coverage

| FR | Owning slice clause(s) | Surface |
|----|------------------------|---------|
| FR-001 | C-1 | routing owner § Hierarchy |
| FR-002 | C-2 | routing owner § Direct modification |
| FR-003 | C-3, C-4 | CLI neutral key set; authoring baseline |
| FR-004 | C-5, C-6, C-7, C-8 | `seats` map; payload; AND resolution |
| FR-005 | C-8, C-9, C-10, C-14, C-46 | anti-nesting owner; pre-dispatch probe |
| FR-006 | C-11, C-12, C-13, C-15 | depth-2 chain; virtual prohibition; per-member cap |
| FR-007 | C-28, C-29 | engine; golden table |
| FR-008 | C-18, C-19, C-20 | five inputs; rubric reference; `definition-class` closure (a change-nature value, path-derived) and its cross-cutting default |
| FR-009 | C-21 | SDD branch conditions |
| FR-010 | C-20, C-22 | direct branch conditions |
| FR-011 | C-23, C-24 | precedence; conflict set |
| FR-012 | C-25 | user override |
| FR-013 | C-26, C-27 | per-duty application; verdict record carrier (D-2) |
| FR-014 | C-17, C-19, C-28, C-29, C-30 | single owner; no restatement |
| FR-015 | C-31, C-32 | invoked-from-team entry; validation |
| FR-016 | C-33, C-34, C-35, C-36, C-37, C-42 | stop at review; handoff; integration identity |
| FR-017 | C-35, C-40, C-41, C-42 | consumer duty; acceptance content face (D-3) |
| FR-018 | C-13, C-16, C-38, C-43 | line registry reuse; no second store |
| FR-019 | C-39 | stall handoff |
| FR-020 | C-44, C-45, C-46, C-47 | invocation kinds; setup path; same predicate |

Every local FR is claimed by at least one clause, and the clause-to-FR citation groups in
`contracts/` are the mechanical form of this table.

## 4. SC coverage

| SC | Owning slice clause(s) | Measurement source |
|----|------------------------|--------------------|
| SC-001 | C-8, C-14 | `tests/contract/test_sdd_authorization.py` + fixture team (allowed/forbidden seats) |
| SC-002 | C-24, C-29 | `tests/contract/test_sdd_routing_engine.py` + `--action golden` judged twice per row |
| SC-003 | C-41 | `tests/contract/test_nested_sdd_invocation.py` + assertions over artifact paths, `git log`, `git status` (D-3 content face) |
| SC-004 | C-15, C-46 | `tests/contract/test_sdd_invocation_governance.py` + the pre-existing anti-nesting cases |
| SC-005 | C-13, C-38, C-43, C-47 | structure check over the changed tree + line-registry reuse assertion |
| SC-006 | C-23 | the golden table filtered to missing/ambiguous/conflicting rows |

## 5. Disclosed rulings

1. **Projection, not re-design** (parent = authority): the slice inherits 47 of the parent design's 67
   clauses and defers 20 to `074b-nested-governance`; § 2 lists the deferred delivery rows and each
   contract file lists its deferred parent clauses. Nothing here contradicts a parent clause.
2. **Local id spaces** (RA1): slice clauses are `C-1`…`C-47`, entities `E1`…`E9`; each carries its
   parent tag. Validation rules keep the parent's `V-1`…`V-29` unchanged because all 29 fall inside
   the slice — a renumbering would have produced two ids for one identical set.
3. **D-2 — verdict record carrier** (RA6): recorded in the Agent execution evidence; the report
   section that will reference it is parent FR 021's and lands with `074b-nested-governance`.
4. **D-3 — SC-003 content face** (RA7): artifact chain, zero merge/push, and path references are
   asserted here; the `## Nested SDD Runs` heading literal and section semantics are not.
5. **One intentional pin change** (RA8): the framework-key frozenset literal in
   `tests/contract/test_neutral_metadata_schema.py` gains exactly one member, in the same change as
   the code edit. It is the slice's only intentional change to an existing test proposition.
6. **Same-author scoring disclosed, not delegated** (RA9): every Constitution Check row is a direct
   read; the program-derivable checks were executed instead.
7. **Container-claim deferral, stated explicitly**: the additivity and containment claims over the
   four predecessor surfaces (parent C-61 / C-62, and the default-`forbidden` containment of parent
   C-27 / C-65) are `074b-nested-governance`'s. The slice owes them no verdict, but its implementation
   must stay additive on those surfaces — removing a key, section, entry form, or exit code here would
   falsify a claim 074b is required to make.

## 6. Non-regression statement

The slice's only non-regression obligation it can decide by itself is SC-004's second half: all
pre-existing anti-nesting contract cases remain green for the paths that do not satisfy the narrowed
predicate. Its measurable form is the 13-file targeted suite, measured green at `stage_base=939766891`
(`191 passed`, `test-evidence/targeted-set-v1-baseline.txt`). The slice makes **no** superset claim
over any predecessor suite's case set — that claim is parent FR 027's and belongs to `074b`.
