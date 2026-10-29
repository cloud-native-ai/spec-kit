# Implementation Plan: 074a-authorized-routing

**Branch**: `074-goal-team-sdd-unification` | **Date**: 2026-10-29 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `074a-authorized-routing` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Input**: Specification from `.specify/specs/074a-authorized-routing/requirements.md` (20 FR / 6 SC / 10 shared strings; requirements + clarify ratified 2026-10-29), projected from the parent design at `.specify/specs/074-goal-team-sdd-unification/` (committed at `6297c14f6`)

## Summary

This slice is the MVP half of Feature 074. The parent requirement establishes one control hierarchy —
Goal → Team → Agent — inside which an SDD run is a subordinate execution path an authorized member may
start; this slice delivers the hierarchy statement, the two-half authorization (Agent capability AND
Team seat policy), the deterministic three-value routing verdict that separates an SDD run from a
direct modification, the governed depth-2 nesting predicate, and the nested invocation contract that
ends at review with a structured handoff. What the outer layer does with that handoff — the mandatory
team run-report section, the Goal-level observational attribution, the vocabulary diffusion into every
Goal/Team/Agent surface, and the additivity and containment guarantees — is `074b-nested-governance`'s.

The technical approach is the parent's, unforked: **one new vocabulary owner**
(`shared/definitions/sdd-routing-definitions.md`), **one new neutral metadata key** (`sdd-invocation`,
framework-level, never rendered to a host tool), **one frontmatter field** (`seats:` in `team.md`),
**one new read-only stdlib engine** (`scripts/python/sdd-route.py` with `route` / `authorize` /
`golden`), and **one in-place narrowing** of the existing anti-nesting obligation at its existing owner
site. Everything else is reuse by reference: the driver gains one entry form that validates before U0,
the run-agent pre-dispatch probe calls the engine instead of re-reading prose, and the team `team.md`
schema gains one block map. No new `/speckit.*` command, skill, store, registry, ledger, state spine,
integration queue, scheduler, confirmation gate, or automatic transmission is introduced.

**Run input classification** (the planning skill's step 2): the dispatch brief arrived as run
parameters — the authoritative slice requirement, the parent design as read-only authority, the split
record, and the discipline defaults — not as a new requirement set. No mid-run addendum arrived, so
`requirements.md` was not restructured and its checklist was not re-validated.

## Technical Context

**Language/Version**: Python 3.8+ for the new engine and the contract tests (project floor per
`pyproject.toml`; host 3.11.11, pytest 8.4.2); Markdown for the owner document, the driver reference,
the skill edits, and the contracts.
**Primary Dependencies**: none new. Reuses the CLI's neutral metadata validator
(`NEUTRAL_AGENT_METADATA_KEYS` / `parse_agent_frontmatter` / `validate_agent_metadata` in
`src/specify_cli/__init__.py`), `scripts/python/sync-mirrors.py`, and the existing line registry
(`skills/external/sdd-loop-driver/scripts/line-registry.py`).
**Storage**: files only, and no new store. The agent capability rides the existing agent-definition
frontmatter; the seat policy rides the existing `team.md` frontmatter; a verdict is recorded in the
Agent execution evidence (D-2); a nested run's durable state is the existing
`.specify/state/<line-id>.md` spine; line/worktree identity is the existing line registry entry.
**Testing**: pytest contract suites under `tests/contract/`. Five new files (one per behaviour group)
plus one new fixture module, all red-first during implementation; one existing file gains the single
declared pin change. Measured pre-change baseline of the 13-file targeted set at `stage_base=939766891`:
**191 passed, 0 failed** (`test-evidence/targeted-set-v1-baseline.txt`). Tests Mode = **ON**.
**Target Platform**: the framework repository (source hat) and every consuming client project (runtime
hat); hosts with or without native subagent capability; repositories whose `.specify/` runtime predates
this feature (undecorated teams and agents must behave exactly as before).
**Project Type**: SDD framework — prompt templates, skills, shared definitions, deterministic scripts,
contract tests. No application runtime is added.
**Performance Goals**: not a performance feature. `route` and `authorize` are one frontmatter read plus
one arithmetic decision each; `golden` reads one Markdown table (about a dozen rows). No network call,
no process spawn beyond the engine itself.
**Constraints**: no new command, skill, store, registry, ownership model, integration queue, state
spine, scheduler, daemon, confirmation gate, or automatic feedback transmission; never push; every
projection of an edited source is produced by the mirror machinery, never hand-edited; the slice stays
additive on the four predecessor surfaces `074b` must later claim containment over.
**Scale/Scope**: 20 FR / 6 SC / 10 shared strings → 4 contract files with 47 clauses (C-1…C-47),
9 data-model entities, 29 validation rules, 3 state machines, 1 engine (3 actions), and a **15-row
delivery surface = 9 new + 6 edited** (`feature-ref.md` § 2): 3 new framework files, 5 new test files,
1 new fixture, 5 edited framework sources, 1 edited existing test file carrying the declared pin
change. No new `/speckit.*` command and no new skill.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Same-author condition (disclosed, per `.specify/shared/workflow/objective-analysis-gate.md`)**: these
design artifacts were authored in this session, this environment exposes no subagent dispatch
capability, and the stage brief fixes `decomposition=single-package` with no subagent dispatch.
Scoring therefore could not be delegated. Every row carries `(direct read, subagent unavailable)`, and
the program-derivable checks were actually executed instead — `clause_extract.py` (4 files, 47
clauses, all `md-bold-closed`, ids contiguous), `account-clause-coverage.py` (FR lane 20/20,
uncovered 0), `pre-analyze-check.py --stage plan`, `sync-mirrors.py --check` and
`regen-command-copies.py --check` (baseline clean), `flow-class-check.py` (no new flow unit), and the
191-case targeted suite — with real output in `test-evidence/plan-stage-checks.md`.

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.15.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every slice clause cites the requirement it serves, and each inherited clause names its parent source (`父 C-nn`); the owner document is created because FR-014 requires exactly one owner (direct read, subagent unavailable) |
| II | Feature-Centric Development | ✅ Pass | The slice binds to Feature 074 without adding a Feature row; the parent's `Planned` status is unchanged and the slice's key changes are recorded in `.specify/memory/features/074.md`; no feature is created, merged, or split (direct read, subagent unavailable) |
| III | Intent-Driven Development | ✅ Pass | The three user stories fix the what/why; `research.md` RA1–RA9 records the rejected alternative behind every projection choice (mirroring the parent files, renumbering the rules, adding cases to the existing suite) (direct read, subagent unavailable) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Five new behaviour groups with named pinning tests, red-first by plan; § 3 of `feature-ref.md` maps every FR to a clause and every clause to a surface; the declared pin change is one member, guarded from both sides (`test_neutral_metadata_schema.py:130`/`:137`) (direct read, subagent unavailable) |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster, provider, or config-key change. The new metadata key is tool-neutral by construction (`renders_to_tools = False`), so no host's field mapping changes; `test_tool_mapping.py` keeps every rendering key mapped (direct read, subagent unavailable) |
| VI | Continuous Quality & Observability | ✅ Pass | The verdict, the authorization resolution, and the nested outcome are recorded with named reason codes and source paths; the slice's only self-decidable non-regression obligation (SC-004) is measured, not asserted; no speculative capability is added (direct read, subagent unavailable) |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify → plan respected on the slice's own chain; status ceiling `Planned`; the slice reuses Feature 074 rather than creating one (direct read, subagent unavailable) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 re-measured the surfaces before designing: the neutral key maps at `src/specify_cli/__init__.py:119`/`:149`, the flat-only frontmatter parser at `:227`, the flat team.md reader at `scripts/python/goal-utils.py:325`, the anti-nesting owner at `shared/definitions/subagent-definitions.md:98` and its exclusivity sentence at `:104`; `research.md` quotes each (direct read, subagent unavailable) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine for two predicates, one owner document, one entry form, one narrowed obligation; explicitly no new command, skill, store, registry, queue, scheduler, or daemon (C-16/C-47); authorization is a lookup, not a service (direct read, subagent unavailable) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic lowercase names (`sdd-routing-definitions.md`, `nested-invocation.md`); no reserved ALL-CAPS name is used; mandated names (`SKILL.md`) unchanged (direct read, subagent unavailable) |
| XI | Dogfooding (Self-Application) | ✅ Pass | Every row of `feature-ref.md` § 2 is a framework-source edit carried by the mirror flow (hat declared); the mechanism fix lands at the owner site — the anti-nesting obligation is narrowed where it lives, not patched in a prompt (direct read, subagent unavailable) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the CLI validator, the mirror engine, and the line registry instead of re-implementing them; where no Tool record covers routing or authorization, writing the engine is the expected outcome (`.specify/shared/workflow/tool-reuse-gate.md`) (direct read, subagent unavailable) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (a decidable rule replaces per-agent thresholds) and Controlled Execution (a bounded, authorized, governed nested path); no scoring system, maturity report, or recording engine is added (direct read, subagent unavailable) |
| XIV | One Source Of Truth (Authority & Reference Discipline) | ✅ Pass | The four routing facts have exactly one owner and are cited by path from the contracts, the execution-evidence record shape, and the tests; V-19 and slice clause C-17/C-30 are the mechanical guards against a second copy (direct read, subagent unavailable) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The new surfaces address agents and maintainers in the project's existing vocabulary; `quickstart.md` carries per-example disclaimers naming their premises so a reader can act without opening the engine (direct read, subagent unavailable) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Every refusal names the failing half or condition instead of a bare denial (C-8/C-14/C-32); an unreadable seat map is malformed input, never a policy value; the same-author condition and the subagent-unavailable condition are disclosed rather than papered over (direct read, subagent unavailable) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created: the new files land in existing directories (`shared/definitions/`, `skills/external/sdd-loop-driver/references/`, `scripts/python/`, `tests/contract/`, `tests/fixtures/`); the planned fixture's scratch repo uses the sanctioned temp root (direct read, subagent unavailable) |
| XVIII | Grounded Naming | ✅ Pass | Names follow the user's own vocabulary from the spec (`sdd-invocation`, `seats`, `sdd` / `direct` / `adjudicate`) and imitate the closest siblings (`flow-class-definitions.md` for the owner document, `flow-class-check.py` for the engine); the slice's inherited names are never renamed (direct read, subagent unavailable) |

**Gates Status**: ✅ All gates pass. No ❌ and no ⚠ row, so Complexity Tracking is N/A.

**Re-check after Phase 1** (2026-10-29, after the design artifacts landed): the same eighteen rows
remain ✅ Pass. New evidence: `research.md` (9 rulings, each with a measured anchor and the rejected
alternatives), `data-model.md` (9 entities, 29 validation rules, 3 state machines), four contract
files with 47 clauses (all `md-bold-closed`, C-1…C-47 contiguous, 20/20 FR and 6/6 SC cited),
`quickstart.md` (7 scenarios; S7 executed live with output pasted, S1–S6 with per-example disclaimers
and named pinning tests), and `feature-ref.md` (15-row delivery surface, 20-row FR map, 6-row SC map,
7 disclosed rulings). No new violation; no Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/074a-authorized-routing/
├── plan.md                 # This file (/speckit.plan output)
├── requirements.md         # Input (20 FR / 6 SC / 10 shared strings; parent mapping; D-1/D-2/D-3)
├── research.md             # Phase 0 output: rulings RA1–RA9 with measured anchors
├── data-model.md           # Phase 1: entities E1–E9, rules V-1…V-29, 3 state machines
├── contracts/              # Phase 1: 4 files, clauses C-1…C-47
│   ├── hierarchy-and-authorization.md   # C-1…C-16
│   ├── routing-decision.md              # C-17…C-30
│   ├── nested-invocation.md             # C-31…C-43
│   └── bootstrap-and-maintenance.md     # C-44…C-47
├── quickstart.md           # Phase 1: scenarios S1–S7 (S7 executed; S1–S6 disclaimed per example)
├── feature-ref.md          # Phase 1: binding, delivery surface, FR/SC maps, disclosed rulings
├── checklists/
│   └── requirements.md     # Requirements-stage quality checklist (unchanged by this stage)
├── test-evidence/          # Deterministic check records for this stage
├── tasks.md                # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md         # Implementation output (/speckit.implement — NOT created here)
```

Phase 0 produced 9 rulings with measured evidence, past the inline threshold (~50 lines), so
`research.md` is a standalone file rather than an inlined section.

### Source Code (repository root)

```text
shared/definitions/
├── sdd-routing-definitions.md   # NEW — routing owner: 5 input domains, verdict table,
│                                #   precedence, reason codes, invocation kinds, golden table
└── subagent-definitions.md      # EDIT — § Dispatch-Time Governance Obligation: predicate
                                 #   + depth-2 chain + virtual prohibition (one in-place amendment)

src/specify_cli/
└── __init__.py                  # EDIT — `sdd-invocation` in NEUTRAL_AGENT_METADATA_KEYS
                                 #   (closed domain, default forbidden, no rendering) and in
                                 #   NEUTRAL_AGENT_FRAMEWORK_KEYS

scripts/python/
└── sdd-route.py                 # NEW — read-only stdlib engine:
                                 #   --action route | authorize | golden

skills/internal/run-agent/
└── SKILL.md                     # EDIT — pre-dispatch probe enforces the predicate fail-closed;
                                 #   authoring baseline lists the new key

skills/internal/create-team/references/
└── create-mode.md               # EDIT — team.md schema gains the `seats:` block map

skills/external/sdd-loop-driver/
├── SKILL.md                     # EDIT — § Invoked-from-Team Entry (six facts, validation,
│                                #   stop-at-review) + one Hard Requirement; standalone unchanged
└── references/
    └── nested-invocation.md     # NEW — handoff schema, closed field set, validation table,
                                 #   failure/stall handoff

tests/contract/
├── test_sdd_routing_definitions.py    # NEW
├── test_sdd_routing_engine.py         # NEW
├── test_sdd_authorization.py          # NEW
├── test_sdd_invocation_governance.py  # NEW
├── test_nested_sdd_invocation.py      # NEW
└── test_neutral_metadata_schema.py    # EDIT — the single declared pin change (RA8)

tests/fixtures/
└── nested_sdd.py                      # NEW — temp repo: minimal .specify/, two seats, two
                                       #   agent definitions, one goal with an open Target
```

**Structure Decision**: this slice extends the existing SDD-framework layout and creates **no new
top-level directory** — the three new framework files land in `shared/definitions/`,
`skills/external/sdd-loop-driver/references/`, and `scripts/python/`; six files are edited (five
framework sources and one existing test file); five test files are new, and one fixture is new. The
documentation plane and the runtime plane stay separate: every edit above is a source edit, and the
`.specify/` runtime copies listed under Mirror Obligations are produced by the mirror machinery.

### Mirror Obligations

The live mirror pairs are defined in `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`. This slice edits
**no** `templates/**` file and no `templates/commands/**` file, so neither
`scripts/bash/generate-instructions.sh` nor `scripts/python/regen-command-copies.py` has anything to
regenerate for it — both are nonetheless measured below so a later stage cannot mistake their silence
for an unmeasured surface.

**Baseline drift measured before this plan's edits** (2026-10-29):
`python3 scripts/python/sync-mirrors.py --check` → exit `0`, every pair `ok` — `templates/` 22 files,
`skills/external/` 405, `skills/internal/` 136, `agents/` 3, `scripts/` 113, `shared/` 58;
`regen-command-copies.py --check` → clean by the same run's first line. There is **zero** pre-existing
drift, so the criterion for every row below is "no NEW drift" *and* it is measurable as "clean".

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/sdd-routing-definitions.md` (new), `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/…` via `sync-mirrors.py` (`shared/` pair, 58 files at baseline) | `python3 scripts/python/sync-mirrors.py --check` — no new drift vs the measured-clean baseline |
| `skills/internal/run-agent/SKILL.md`, `skills/internal/create-team/references/create-mode.md` | `.specify/skills/internal/…` via `sync-mirrors.py` (`skills/internal/` pair, 136 files) | same check, same criterion |
| `skills/external/sdd-loop-driver/SKILL.md` + new `references/nested-invocation.md` | `.specify/skills/sdd-loop-driver/…` via `sync-mirrors.py` (`skills/external/` pair, 405 files) | same check, same criterion |
| `scripts/python/sdd-route.py` (new) | `.specify/scripts/python/sdd-route.py` via `sync-mirrors.py` (`scripts/` pair, 113 files, strict extras) | same check, same criterion; the copies must be byte-identical, not merely present |
| `src/specify_cli/__init__.py` | none — the CLI package is the source of truth for the neutral key set; no projection carries it | `grep -c 'sdd-invocation' src/specify_cli/__init__.py` measured `0` at plan time (`test-evidence/plan-stage-checks.md` § 8); the post-edit criterion is exactly one definition point, pinned by the framework-key frozenset equality at `tests/contract/test_neutral_metadata_schema.py:130` and the membership cross-check at `:137` — never a pre-written number |

## Complexity Tracking

N/A — the Constitution Check has no ❌ Fail and no ⚠ Partial row.

## Parent Design Mapping

**Reading**: the slice's requirement entries come from
`.specify/specs/074a-authorized-routing/requirements.md` § Parent Mapping (parent FR-001–FR-019 plus
parent FR 025, parent SC-001–SC-004 / SC 006 / SC 007, parent STR-001–STR-009 / STR 011). The parent
design at `.specify/specs/074-goal-team-sdd-unification/` is the design authority: every slice clause is
a projection of the parent clause named in its `父 C-nn` tag, and the parent contract file is recorded
here so a reader can reach the source without opening all five files. Attribution is drawn **per
requirement entry**, never per parent file's physical grouping (D-1).

### Slice FR → parent FR → parent clause → parent contract file

| Slice FR | Parent FR | Parent clause(s) | Parent contract file |
|----------|-----------|------------------|----------------------|
| FR-001 | FR-001 | C-2 | `route-decision.md` |
| FR-002 | FR-002 | C-3 | `route-decision.md` |
| FR-003 | FR-003 | C-15, C-60 | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-004 | FR-004 | C-16, C-17, C-18, C-19 | `authorization-and-probe.md` |
| FR-005 | FR-005 | C-20, C-21, C-29, C-59 | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-006 | FR-006 | C-22, C-23, C-24 | `authorization-and-probe.md` |
| FR-007 | FR-007 | C-13, C-14 | `route-decision.md` |
| FR-008 | FR-008 | C-4, C-5, C-6 | `route-decision.md` |
| FR-009 | FR-009 | C-7 | `route-decision.md` |
| FR-010 | FR-010 | C-6, C-8 | `route-decision.md` |
| FR-011 | FR-011 | C-9, C-10 | `route-decision.md` |
| FR-012 | FR-012 | C-11 | `route-decision.md` |
| FR-013 | FR-013 | C-12, C-54 (FR-013 facet, D-2) | `route-decision.md`, `report-and-attribution.md` |
| FR-014 | FR-014 | C-1, C-5, C-13, C-14, C-66 (FR-014 facet) | `route-decision.md`, `diffusion-and-compat.md` |
| FR-015 | FR-015 | C-31, C-32 | `nested-invocation.md` |
| FR-016 | FR-016 | C-34, C-35, C-36, C-37, C-38, C-46 | `nested-invocation.md` |
| FR-017 | FR-017 | C-36, C-41, C-46 | `nested-invocation.md` |
| FR-018 | FR-018 | C-24, C-30, C-39, C-64 (FR-018 facet) | `authorization-and-probe.md`, `nested-invocation.md`, `diffusion-and-compat.md` |
| FR-019 | FR-019 | C-40 | `nested-invocation.md` |
| FR-020 | parent FR 025 | C-45, C-58, C-59, C-67 | `nested-invocation.md`, `diffusion-and-compat.md` |

### Slice SC → parent SC → parent clause(s)

| Slice SC | Parent SC | Parent clause(s) | Delivered facet in this slice |
|----------|-----------|------------------|-------------------------------|
| SC-001 | SC-001 | C-19, C-29 | authorization refusal names the failing half, with both source paths |
| SC-002 | SC-002 | C-10, C-13, C-14 | golden table judged row by row; repeated evaluation identical |
| SC-003 | SC-003 | C-42 (+ parent C-48 deferred) | content face per D-3: artifact chain, zero merge/push, path references |
| SC-004 | SC-004 | C-28 (+ parent C-65 deferred) | stage executors cannot start; unqualified prompts blocked; pre-existing cases green |
| SC-005 | parent SC 006 | C-24, C-30, C-39, C-64 | no second registry / ledger / spine / ownership / queue |
| SC-006 | parent SC 007 | C-9, C-14 | ambiguous or conflicting input never yields direct |

### Parent clauses deferred to `074b-nested-governance` (not counted as slice coverage)

20 of the parent design's 67 clauses fall outside this slice, because the requirement entries they
serve belong to the sibling slice. They are listed so their absence from `contracts/` is a recorded
decision rather than an omission:

| Parent clause(s) | Serves | Slice that owns it |
|------------------|--------|--------------------|
| C-25, C-26 | parent FR 023 (Agent responsibility statement; leaf stays leaf) | `074b-nested-governance` |
| C-27, C-65 | parent FR 026 (default-`forbidden` containment claim) | `074b-nested-governance` |
| C-33, C-43, C-44 | parent FR 027 (additive on the four predecessor surfaces) | `074b-nested-governance` |
| C-47, C-48, C-49, C-53 | parent FR 021 (the `## Nested SDD Runs` report section) | `074b-nested-governance` |
| C-50, C-51, C-52 | parent FR 020 (supervisor-only writes; ledger attribution; no Goal field) | `074b-nested-governance` |
| C-54 (report-section facet) | parent FR 021 (the section's verdict reference) | `074b-nested-governance` |
| C-55 | parent FR 022 (team Stage-vocabulary disambiguation) | `074b-nested-governance` |
| C-56, C-57 | parent FR 024 (instructions pointer; trigger conjunction) | `074b-nested-governance` |
| C-61, C-62 | parent FR 027 (containment claim and its node-id discharge) | `074b-nested-governance` |
| C-63 | parent FR 028 (no merge/push, scheduler, transmission, second gate) | `074b-nested-governance` |

Two consequences are recorded rather than hidden. **First**, the slice inherits two parent clauses only
partially — parent C-54 and parent C-66 each carry an FR-013/FR-018 facet (slice) and a report-section
or Stage-vocabulary facet (`074b`); the slice keeps the facet its own requirement entry governs and
names the other in § Deferred. **Second**, the slice owes no containment verdict (parent FR 026 /
FR 027), but its implementation must stay additive on those surfaces: removing a key, section, entry
form, or exit code here would falsify a claim `074b` is required to make (`feature-ref.md` § 5 ruling 7).

## Phase 1: Design Artifacts Summary

Counts below were taken from the artifacts on disk after they landed, via the commands quoted — never
pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 9 rulings (RA1–RA9), each with a measured anchor and the rejected alternatives |
| Data model | [`data-model.md`](data-model.md) | 9 entities (E1–E9), 29 validation rules (V-1…V-29), 3 state machines (authorization resolution, nested-run lifecycle, verdict supersession) |
| Contracts | [`contracts/`](contracts/) | 4 files, **47 clauses** (C-1…C-47) — `clause_extract.py` reports every file as `md-bold-closed`: `hierarchy-and-authorization.md` 16, `routing-decision.md` 14, `nested-invocation.md` 13, `bootstrap-and-maintenance.md` 4 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios: S1–S6 not-executed with per-example disclaimers naming premises and pinning tests; S7 executed live 2026-10-29 with outputs pasted (3 sub-checks: mirror baseline, targeted suite, new-file absence) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, 15-row delivery surface, 20-row FR map, 6-row SC map, 7 disclosed rulings, non-regression statement |

Executed derivation commands (real output pasted into `test-evidence/plan-stage-checks.md`):
`clause_extract.py contracts/*.md` → 47 clauses across 4 files, all `md-bold-closed`, ids contiguous
(C-1…C-47); `account-clause-coverage.py` → **FR lane 20/20 claimed, uncovered 0**, while its clause
lane reports `status: baseline-missing` — expected at plan stage, because the claims are `[green:]`
rows in `tasks.md` and freezing a baseline before any claim exists would make that stage trivially
green; `pre-analyze-check.py --stage plan` → see the recorded output;
`sync-mirrors.py --check` → exit 0, no drift; `regen-command-copies.py --check` → clean;
`flow-class-check.py --action check` → 79 units, 0 findings; targeted suite → 191 passed.

## Plan Revision

**2026-10-29 — analyze-fix round 1 (slice `074a-authorized-routing`).** Authorized by the driver for
one plan re-review (efficiency-model §3.5(a)) after `/speckit.analyze` returned 0 CRITICAL / 3 HIGH /
8 MEDIUM / 3 LOW. Each entry records the decision and the reason; the requirement text each one
projects is already in `requirements.md` and is read there, never re-derived here.

1. **F-01 — `authorize` exit alphabet (substantive: C-8, C-28, `quickstart.md` S4, `tasks.md` T007).**
   Decision: `authorize` exits `0` for **any** authorization verdict — allowed and refused alike — and
   `2` for malformed or unreadable input; a refusal is expressed by the JSON `verdict` / `reason`
   fields together with the failing half, never by the process status. Reason: the pre-revision text
   carried two contradictory alphabets for one engine (C-28 fixed `0` / `2` for `route`, while
   `quickstart.md` S4 documented `0` / `2` / `3` for `authorize`), so a caller could not tell
   "refused" from "engine failed", and any test written from one surface would have contradicted the
   other. Both verdict-producing actions now share one two-valued alphabet, and the refusal/error
   distinction lives where the record is. Pinned by `tests/contract/test_sdd_authorization.py`, whose
   T007 obligation now asserts `0` on the refused case.
2. **HIGH-1 — definition-class closure (substantive: C-18, C-20, with C-21 / C-22 / C-24 kept in
   step).** Decision: `definition-class` is a value of `change_nature` — the five inputs stay five —
   its membership is derived from the target path by the predicate owned by `requirements.md` FR-008,
   and the change is cross-cutting by default, bounded only on a declared bounded correction with a
   recorded rationale. Reason: the class was an open phrase ("templates that generate them") while
   both the cross-cutting default and the bounded-correction escape keyed off class membership, so no
   implementer could decide membership; carrying it inside the declared change nature closes the set
   without adding the sixth input C-18 forbids. C-21's and C-22's first conditions are now read off
   the `feature` / `maintenance` values instead of an unmapped one, and C-24's conflict pair uses the
   `feature` literal.
3. **HIGH-2 — `SDD assignment` defined (substantive, narrow: C-9).** Decision: the third predicate
   condition names a defined term — a member duty whose routing decision is recorded as [[STR-004]],
   with the definition owned by `requirements.md` FR-005. Reason: two readings survived (a recorded
   `sdd` verdict vs. any dispatch intending to run SDD) and they differ exactly on the dispatch FR-005
   exists to block. The three conditions themselves are unchanged.
4. **Driver-adjudicated MEDIUM repairs touching this plan's artifacts** (decisions recorded in the
   state spine; listed here so the plan does not read as untouched): C-13's per-member cap escape is
   removed in favour of a hard cap of one run per member (B-04); C-14 names the two SC-001 carriers
   (B-01); C-25 makes the FR-011 reason code mandatory on an override record (B-03); C-26 defines
   `write-bearing change` by pointer to FR-007 (C-03); `data-model.md` E4 / E7 carry the same three
   alignments; and the delivery-surface counts become 15 rows = 9 new + 6 edited with `feature-ref.md`
   § 2 as the owner (F-02).

**What this revision does not do**: it changes no clause id, adds no clause, moves no clause between
files, defers no clause differently, and re-opens no requirement. The clause count stays 47 and the
C-1…C-47 partition `tasks.md` claims is untouched, so every `[green:]` claim still resolves. The same
eighteen Constitution Check rows remain ✅ Pass: no principle depends on the exit alphabet or on the
class phrase, and the one-source-of-truth row is strengthened rather than weakened, because the path
predicate now has a single owner in `requirements.md` FR-008 that the contracts cite.
