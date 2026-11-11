# Feature Reference: 074b-nested-governance

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Bound at**: `/speckit.clarify` 2026-10-28 for the parent requirement, reused here — the slice binds to
Feature 074 by `Related Feature` and creates no Feature row of its own (split confirmed by the user
2026-10-28, `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录)
**Status ceiling of this stage**: `Planned` (Feature 074 is already `Planned`; the `Implemented`
transition belongs to `/speckit.implement` over the whole feature)

## 1. Binding

| Axis | Value |
|------|-------|
| Requirement key | `074b-nested-governance` |
| Feature ID / name | 074 Goal/Team/Agent 与 SDD 开发流程统一 (slice `074b-nested-governance`) |
| Feature index row | `.specify/memory/features.md` (row 074 — **unchanged**; the slice adds no row) |
| Feature detail | `.specify/memory/features/074.md` (this stage appends its entry to § Latest Review) |
| Specification | `.specify/specs/074b-nested-governance/requirements.md` |
| Parent design (authority) | `.specify/specs/074-goal-team-sdd-unification/` — read-only: `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, `research.md`, `feature-ref.md` |
| Sibling slice (implemented) | `.specify/specs/074a-authorized-routing/` — merged at `9360718a1`; its surfaces are cited, never redefined |
| Split record | `.specify/state/074-goal-team-sdd-unification.md` § 拆分记录（tasks U4，2026-10-28，`confirmed-user`） |
| Related features | 058 (U0–U6, state spine, sentinels — preserved by reference), 060 (Agent layers + neutral key set — referenced), 064 (line/worktree/ownership — preserved), 069/052 (flow class, fast-fail — referenced), 070 (in-run work packages + stage-team preset — preserved) |

This slice maps onto Feature 074 as the **second half**: it makes a nested SDD run consumable and
auditable by the Team and Goal layers (report section + observational attribution), diffuses the SDD
vocabulary into four existing surfaces at pointer level, and states the two compatibility obligations
as decidable containment claims. It creates no command, no skill, no store, and no second definition
point.

## 2. Delivery surface

**Hat declared**: every row below is a **framework-source** edit, which reaches client projects through
publish → install → `specify init`. No row is a hand edit to this repository's `.specify/` runtime
copies; the runtime projections in the "Generated / mirrored" block are produced by the mirror and
generator machinery.

| # | Path | Kind | Purpose |
|---|------|------|---------|
| 1 | `skills/internal/create-team/SKILL.md` | EDIT | § Report contract gains one mandatory `## Nested SDD Runs` section (per-invocation fields, explicit-when-empty, supervisor-only writer, one ledger attribution row, verdict reference by reference) |
| 2 | `skills/internal/create-team/references/conceptual-model.md` | EDIT | Stage bullet gains the disambiguation sentence: the Stage dimension is not the SDD stage roster; no value renamed; roster stays the driver's |
| 3 | `skills/internal/run-agent/SKILL.md` | EDIT | § Authoring Baseline gains the hosting-responsibility rule (three statements for a `allowed` declaration; the leaf stays a leaf, asserted against the shipped preset) |
| 4 | `templates/instructions-template.md` | EDIT | One pointer-level routing section: when a write-bearing change is proposed, run the decision at the owner's path — no input set, no verdict table, no reason codes |
| 5 | `shared/guidelines/proactive-trigger.md` | EDIT | One sentence in § Promotion & Safety Boundary: promotion to an SDD run needs both a routing verdict of the SDD kind and an effective authorization (conjunction owned by the routing owner) |
| 6 | `tests/contract/test_nested_run_report.py` | NEW | Report section literal + mandatory-ness + explicit-when-empty + per-invocation fields + supervisor-only write + one ledger row with the existing Target reference + verdict reference; Goal field set unchanged |
| 7 | `tests/contract/test_sdd_diffusion.py` | NEW | Stage disambiguation and vocabulary stability, hosting-responsibility conformance, leaf preset negative, instructions pointer without restatement, trigger conjunction pointer, no roster enumeration |
| 8 | `tests/contract/test_sdd_compat_containment.py` | NEW | default-`forbidden` resolution cases, containment carrier shape, four-surface additivity negatives, no new command/skill, no merge/push/scheduler/second gate, gate-scan total stability |
| 9 | `tests/contract/test_sdd_invocation_governance.py` | EDIT | The absent-declaration default-resolution cases, which make the FR-006 superset relation non-trivial (superset direction only; no existing case's proposition changes) |

**Generated / mirrored projections** (not hand-edited; see `plan.md` § Mirror Obligations): rows 1–3 →
`.specify/skills/internal/…`; row 4 → `.specify/templates/instructions-template.md`; row 5 →
`.specify/shared/guidelines/…`; row 4 also regenerates `.specify/instructions.md` through
`scripts/bash/generate-instructions.sh`, which the compatibility instruction symlinks already point at.
No `templates/commands/**` file changes, so `regen-command-copies.py` has nothing to regenerate.

**Explicitly not touched** (read-only subjects or owners): `agents/sdd-executor.agent.md` (the negative
subject of the leaf assertion), `skills/internal/run-team/SKILL.md` (it already delegates its report
duty to row 1's owner), `skills/external/sdd-loop-driver/**` and its `references/nested-invocation.md`
(the handoff owner), `shared/definitions/sdd-routing-definitions.md` and `scripts/python/sdd-route.py`
(the routing owner and engine), `shared/definitions/subagent-definitions.md` (the anti-nesting owner),
`src/specify_cli/__init__.py` (the neutral key set), and `tests/fixtures/nested_sdd.py` (reused as-is).

## 3. FR coverage

| FR | Owning clause(s) | Surface |
|----|------------------|---------|
| FR-001 | C-24, C-25, C-26 | supervisor write duty; team ledger `items.jsonl`; `goal-definitions.md` (cited) |
| FR-002 | C-21, C-22, C-23, C-27, C-28, C-29, C-30 | `skills/internal/create-team/SKILL.md` § Report contract |
| FR-003 | C-13, C-14 | `conceptual-model.md` Stage bullet; roster stays the driver's |
| FR-004 | C-15, C-16, C-17 | `run-agent/SKILL.md` § Authoring Baseline; `agents/sdd-executor.agent.md` (negative) |
| FR-005 | C-18, C-19, C-20 | `templates/instructions-template.md` → `.specify/instructions.md`; `proactive-trigger.md` |
| FR-006 | C-1, C-2, C-3, C-4 | default-`forbidden` resolution (074a, cited) + containment carrier S1 |
| FR-007 | C-4, C-5, C-6, C-7, C-8, C-9 | four predecessor surfaces + containment carriers S2–S5 |
| FR-008 | C-10, C-11, C-12 | repo-wide negatives; structure check over the changed tree |

Every local FR is claimed by at least one clause, and the clause-to-FR citation groups in `contracts/`
are the mechanical form of this table.

## 4. SC coverage

| SC | Owning clause(s) | Measurement source |
|----|------------------|--------------------|
| SC-001 | C-3, C-4, C-5, C-6 | frozen node-id sets (`test-evidence/compat-baseline-nodeids.txt`, 266 cases / 17 files / 7 sets), post ⊇ pre + same verdicts |
| SC-002 | C-25, C-26 | goal fixture parsed before/after (`parse_goal` field set, 12 keys, identical); attribution resolves only through the existing ledger reference |

## 5. Disclosed rulings

1. **Projection, not re-design** (RB1): the slice claims the 21 parent clauses that `074a`'s deferred
   table names plus parent C-66's Stage-vocabulary facet, with a local continuous id space
   (`C-1`…`C-30`, `E1`…`E8`, `V-1`…`V-12`) and a `parent C-nn` tag on every projected clause. The
   sibling's table lists 21 ids while its prose says 20; this slice claims per the prose and the
   parent's FR→clause rows and does not edit the sibling to reconcile an integer nothing depends on.
2. **One document owns the report section** (RB2): `create-team/SKILL.md`; `run-team` keeps delegating
   (`:66`) and is not edited — a second statement would give one section two owners.
3. **The verdict is consumed by reference** (RB3/D-2): the section carries a reference to `074a`'s
   recorded verdict; a missing record is recorded as missing, never re-derived.
4. **The containment claim is a verification-time procedure over node-id sets** (RB8): the carrier is
   `test-evidence/compat-baseline-nodeids.txt`; the permanent guard asserts the structural negatives and
   the carrier's shape, not a superset ratchet over other features' suites — the claim's scope is
   "relative to the baseline commit in the verification record".
5. **The instructions pointer is judged by a declared ceiling plus a measured delta** (RB6): both files
   were over the generator's 32,768 B budget before this slice (41,948 B live, 34,666 B template).
6. **A pre-existing red is recorded, not repaired** (RB7): `test_proactive_trigger_section.py::
   test_c11_gate_scan_total_unchanged` fails at the stage base (27 vs frozen 23). This slice's criterion
   is that its own edit does not move the total, and the frozen baseline is not rebased inside this
   change.
7. **No new shipped Agent preset** (parent R9, carried): FR-004 is a conditional conformance rule; the
   shipped stage-executor preset stays the negative subject.
8. **Same-author scoring disclosed, not delegated** (RB10): every Constitution Check row is a direct
   read; the program-derivable checks were executed instead.
9. **Feature status is at its ceiling** (RB10): row 074 is already `Planned`; this stage appends its
   entry to the feature detail and flips nothing.

## 6. Non-regression / containment statement

The slice's containment claims are local FR-006, FR-007 and SC-001. Their discharge is mechanical: the
seven named suite sets are collected as node-id sets at `33269994a` before any edit (266 cases, frozen
into `test-evidence/compat-baseline-nodeids.txt`), and the post-change check asserts set containment
plus identical verdicts for the shared ids. A count comparison is non-conforming.

Two facts are recorded so the claim cannot be read as wider than it is. **First**, the baseline must be
re-captured at implement start under the never-cache rule: this capture is valid for the commit it
names, and a sibling suite may have moved since. **Second**, the suite that pins the trigger document
already carries one failing case at that commit (ruling 6); that case's verdict must remain *the same*
— red before, red after — and no green claim is made over it.
