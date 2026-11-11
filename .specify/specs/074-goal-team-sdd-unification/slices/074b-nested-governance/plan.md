# Implementation Plan: 074b-nested-governance

**Branch**: `074b-nested-governance` | **Date**: 2026-10-29 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Input**: Specification from `.specify/specs/074b-nested-governance/requirements.md` (8 FR / 2 SC / 7 shared strings; requirements + clarify ratified 2026-10-29), projected from the parent design at `.specify/specs/074-goal-team-sdd-unification/` and from the implemented sibling slice `.specify/specs/074a-authorized-routing/` (merged at `9360718a1`)

## Summary

This slice is the second half of Feature 074. `074a` established *how* a nested SDD run may start and
*what* it returns; this slice delivers what the outer layer does with that return. Concretely it (a)
fixes the attribution boundary — the Goal gains no mandatory SDD field and no structural link to a
requirements specification, and a nested run's contribution is observational through the team run
report plus one ledger item carrying the existing Target reference written by the supervisor, (b) makes
the report contract's `## Nested SDD Runs` section mandatory, with the verbatim heading literal and
explicit-when-empty semantics, (c) disambiguates the team's own Stage dimension from the SDD stage
roster without renaming a value, (d) fixes the responsibility statement an SDD-hosting Agent
declaration must carry and the prohibition on a stage executor declaring the capability, (e) keeps the
project instructions at pointer level and forbids the proactive trigger from starting a run without
both a routing verdict and an effective authorization, and (f) states the two compatibility obligations
— the `forbidden` default with its pre-dispatch containment claim, and additivity on the four named
predecessor surfaces — as decidable containment claims.

The technical approach is the parent's, unforked, and deliberately thin: **five in-place edits** to
existing owners (report contract, team conceptual model, Agent authoring baseline, instructions
template, trigger discipline), **three new contract suites**, **one edited suite** whose case set grows
in the superset direction, and **no second definition point**. Every SDD fact this slice's surfaces
mention is reached by path from the owner `074a` delivered: the routing decision and its closed value
domains, the authorized-seat predicate, the handoff's closed field set, the line registry, the state
spine and the stage roster. No new `/speckit.*` command, skill, store, registry, ledger, state spine,
integration queue, scheduler, confirmation gate, or automatic transmission is introduced (local
FR-008).

**Run input classification** (the planning skill's step 2): the dispatch brief arrived as run
parameters — the authoritative slice requirement, the parent design as read-only authority, the
implemented sibling surface to cite, and the discipline defaults — not as a new requirement set. No
mid-run addendum arrived, so `requirements.md` was not restructured and its checklist was not
re-validated.

## Technical Context

**Language/Version**: Python 3.8+ for the contract tests (project floor per `pyproject.toml`; host
3.11.11, pytest 8.4.2); Markdown for every edited owner document and for the contracts themselves.
**Primary Dependencies**: none new. Reuses `scripts/python/sync-mirrors.py`,
`scripts/python/regen-command-copies.py`, `scripts/bash/generate-instructions.sh`, the goal engine
`scripts/python/goal-utils.py` (`parse_goal` for the SC-002 field-set comparison), the driver's
`pre-analyze-check.py` / `clause_extract.py` / `account-clause-coverage.py` gates, and the existing
test fixture `tests/fixtures/nested_sdd.py` (delivered by `074a`).
**Storage**: files only, and **no new store**. The section is text inside an existing run report; the
attribution row is one item in the existing team ledger (`items.jsonl`); the pointer surfaces are
sections of existing documents; the containment carrier is a test-evidence artifact
(`test-evidence/compat-baseline-nodeids.txt`), written by a recorded command and consumed by a
recorded comparison — not by an engine.
**Testing**: pytest contract suites under `tests/contract/`. Three new files plus one edited suite
(the superset direction) and one reused fixture; Tests Mode = **ON**. Measured targeted set at
`stage_base=33269994a`: **19 files → 289 passed, 1 failed**, the single failure being pre-existing and
named below (`test-evidence/targeted-set-v1-baseline.txt`).
**Target Platform**: the framework repository (source hat) and every consuming client project (runtime
hat); repositories whose `.specify/` runtime predates this feature (teams without the section, agents
without the declaration, and instruction files already over the size budget must behave exactly as
before).
**Project Type**: SDD framework — prompt templates, skills, shared definitions, human-checked artifacts
and contract tests. No application runtime is added.
**Performance Goals**: not a performance feature. The new checks read one document each; the
containment comparison reads two sorted node-id lists. No network call, no process spawn beyond
`pytest --collect-only` at verification time.
**Constraints**: no new command, skill, store, registry, ledger, state spine, ownership model,
integration queue, scheduler, daemon, confirmation gate, or automatic feedback transmission; never
push; every projection of an edited source is produced by the mirror/generator machinery, never
hand-edited; the four predecessor surfaces named in local FR-007 stay additive; the report section
never re-derives a routing verdict.
**Scale/Scope**: 8 FR / 2 SC / 7 shared strings → 3 contract files with **30 clauses** (C-1…C-30),
8 data-model entities, 12 validation rules, 2 state machines, a **9-row delivery surface = 3 new + 6
edited** (`feature-ref.md` § 2), 7 named containment sets over 17 suite files (266 cases), and
zero new framework files outside `tests/`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Same-author condition (disclosed, per `.specify/shared/workflow/objective-analysis-gate.md`)**: these
design artifacts were authored in this session, this environment exposes no subagent dispatch
capability, and the stage brief fixes `decomposition=single-package` with no subagent dispatch. Scoring
could therefore not be delegated. Every row carries `(direct read, subagent unavailable)`, and the
program-derivable checks were actually executed instead — `clause_extract.py` (3 files, 30 clauses, all
`md-bold-closed`, ids contiguous), `account-clause-coverage.py` (FR lane 8/8, uncovered 0),
`pre-analyze-check.py --stage plan`, `sync-mirrors.py --check` and `regen-command-copies.py --check`
(measured clean), `flow-class-check.py` (79 units, 0 findings), the 19-file targeted set, and the
containment baseline capture — with real output in `test-evidence/`.

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.15.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every local clause cites the requirement it serves and names the parent clause it projects (`parent C-nn`); each of `research.md` RB1–RB10 names the FR it serves (direct read, subagent unavailable) |
| II | Feature-Centric Development | ✅ Pass | The slice binds to Feature 074 without adding a registry row; the stage appends its entry to `.specify/memory/features/074.md` § Latest Review; no feature is created, merged, or split (direct read, subagent unavailable) |
| III | Intent-Driven Development | ✅ Pass | The two user stories fix the what/why; `research.md` records the rejected alternative behind every projection choice (a second section owner, a new conceptual-model section, an SDD-host preset, a permanent superset ratchet) (direct read, subagent unavailable) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Three new behaviour groups with named pinning tests plus one suite whose case set grows in the superset direction; every FR maps to a clause and every clause to a surface (`feature-ref.md` § 3); the four-surface additivity is measured, not asserted (direct read, subagent unavailable) |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster, provider, or config-key change; the hosting-responsibility rule constrains authored definitions, and the neutral key set stays owned by `src/specify_cli/__init__.py` (cited, not edited) (direct read, subagent unavailable) |
| VI | Continuous Quality & Observability | ✅ Pass | The outcome vocabulary, the verdict reference, the attribution row and the containment sets are all recorded with stable paths; the single pre-existing red (`test_c11_gate_scan_total_unchanged`, 27 vs frozen 23) is disclosed rather than absorbed (direct read, subagent unavailable) |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify → plan respected on the slice's own chain; status ceiling `Planned`; the slice reuses Feature 074 rather than creating one (direct read, subagent unavailable) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 re-measured every surface before designing: the report skeleton at `create-team/SKILL.md:55-63`, `run-team`'s delegation at `:66`, the Stage bullet at `conceptual-model.md:10`, the authoring baseline at `run-agent/SKILL.md:171-205`, the trigger's ten `## ` sections and its § Promotion & Safety Boundary at `:68-79`, and the leaf preset's frontmatter; `research.md` anchors each (direct read, subagent unavailable) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Five in-place edits, three new test files, no new fixture, no new engine, no new document; explicitly no new command, skill, store, registry, queue, scheduler, or daemon (local C-10/C-11/C-12) (direct read, subagent unavailable) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic lowercase names (`test_nested_run_report.py`, `test_sdd_diffusion.py`, `test_sdd_compat_containment.py`); no reserved ALL-CAPS name is used; mandated owners (`SKILL.md`) keep their names (direct read, subagent unavailable) |
| XI | Dogfooding (Self-Application) | ✅ Pass | Every row of `feature-ref.md` § 2 is a framework-source edit carried by the mirror/generator flow (hat declared); the mechanism obligations land at their owners (report contract, authoring baseline, trigger discipline), not in a prompt patch (direct read, subagent unavailable) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the mirror/generator engines, the goal engine as the SC-002 measurement instrument, the driver's own gates, and `074a`'s fixture instead of writing new tooling (`shared/workflow/tool-reuse-gate.md`) (direct read, subagent unavailable) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (a nested run's result becomes readable at the outer layer) and Controlled Execution (attribution without a new Goal field; containment stated decidably); no scoring system or reporting engine is added (direct read, subagent unavailable) |
| XIV | One Source Of Truth (Authority & Reference Discipline) | ✅ Pass | Each diffused fact has exactly one owner and is cited by path: the routing owner for the decision, the driver for the roster, the key set for the capability values, the report contract for the section. V-10 and local C-14/C-18/C-19 are the mechanical guards; the trigger document gains a pointer, not a copy (direct read, subagent unavailable) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The new surfaces address agents and maintainers in the project's existing vocabulary; `quickstart.md` gives each example its premises, and its one executed caveat (`--repo-root` self-match) is stated as a measured fact (direct read, subagent unavailable) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Three measured anomalies are surfaced rather than patched: the sibling's 20-vs-21 clause count, the trigger suite's pre-existing gate-total failure, and the `--repo-root` self-write trap; each names what was corrected locally and what was left to its owner (direct read, subagent unavailable) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory: the three test files land in `tests/contract/`, the evidence in the slice's existing `test-evidence/`, and the one scratch probe used the sanctioned `.specify/.tmp/` root and was removed in the same capture (direct read, subagent unavailable) |
| XVIII | Grounded Naming | ✅ Pass | Names come from the requirement and the parent design (`## Nested SDD Runs`, `completed`/`blocked`/`failed`, `sdd-invocation`, `allowed`/`forbidden`), and the new test files imitate the closest siblings (`test_nested_sdd_invocation.py`, `test_sdd_authorization.py`); no inherited name is renamed (direct read, subagent unavailable) |

**Gates Status**: ✅ All gates pass. No ❌ and no ⚠ row, so Complexity Tracking is N/A.

**Re-check after Phase 1** (2026-10-29, after the design artifacts landed): the same eighteen rows
remain ✅ Pass. New evidence: `research.md` (10 rulings, each with a measured anchor and the rejected
alternatives), `data-model.md` (8 entities, 12 validation rules, 2 state machines), three contract
files with 30 clauses (all `md-bold-closed`, C-1…C-30 contiguous, 8/8 FR and 2/2 SC cited),
`quickstart.md` (7 scenarios: S1/S3/S6-pre/S7 executed with output pasted, S2/S4/S5 pinned by named
tests with premises listed), and `feature-ref.md` (9-row delivery surface, 8-row FR map, 2-row SC map,
9 disclosed rulings). Program checks: `clause_extract.py` 30 clauses; `account-clause-coverage.py` FR
lane 8/8 with the clause lane `baseline-missing` by design (claims and the frozen baseline belong to
the tasks stage); `pre-analyze-check.py --stage plan` decision=pass; mirrors clean; flow-class 79/0;
targeted set 289 passed / 1 pre-existing failed. No new violation; no Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/074b-nested-governance/
├── plan.md                 # This file (/speckit.plan output)
├── requirements.md         # Input (8 FR / 2 SC / 7 shared strings; parent mapping; D-1/D-2/D-3)
├── research.md             # Phase 0 output: rulings RB1–RB10 with measured anchors
├── data-model.md           # Phase 1: entities E1–E8, rules V-1…V-12, 2 state machines
├── contracts/              # Phase 1: 3 files, clauses C-1…C-30
│   ├── compat-and-safety.md          # C-1…C-12   (FR-006, FR-007, FR-008)
│   ├── diffusion.md                  # C-13…C-20  (FR-003, FR-004, FR-005)
│   └── report-and-attribution.md     # C-21…C-30  (FR-001, FR-002)
├── quickstart.md           # Phase 1: scenarios S1–S7 (4 executed, 3 pinned)
├── feature-ref.md          # Phase 1: binding, delivery surface, FR/SC maps, disclosed rulings
├── checklists/
│   └── requirements.md     # Requirements-stage quality checklist (unchanged by this stage)
├── test-evidence/          # Deterministic check records + the containment baseline carrier
├── tasks.md                # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md         # Implementation output (/speckit.implement — NOT created here)
```

Phase 0 produced 10 rulings with measured evidence, well past the inline threshold (~50 lines), so
`research.md` is a standalone file rather than an inlined section.

### Source Code (repository root)

```text
skills/internal/create-team/
├── SKILL.md                          # EDIT — § Report contract: one mandatory `## Nested SDD Runs`
│                                     #   section (per-invocation fields, explicit-when-empty,
│                                     #   supervisor-only writer, one ledger attribution row,
│                                     #   verdict reference by reference)
└── references/
    └── conceptual-model.md           # EDIT — Stage bullet gains the disambiguation sentence
                                      #   (not the SDD stage roster; no value renamed)

skills/internal/run-agent/
└── SKILL.md                          # EDIT — § Authoring Baseline: hosting-responsibility rule
                                      #   (three statements; the leaf stays a leaf)

templates/
└── instructions-template.md          # EDIT — one pointer-level routing section

shared/guidelines/
└── proactive-trigger.md              # EDIT — one conjunction sentence in
                                      #   § Promotion & Safety Boundary (no new section)

tests/contract/
├── test_nested_run_report.py         # NEW — section literal/mandatory/explicit-when-empty,
│                                     #   attribution, no new Goal field, verdict reference
├── test_sdd_diffusion.py             # NEW — Stage disambiguation, host responsibility,
│                                     #   leaf negative, instructions pointer, trigger pointer
├── test_sdd_compat_containment.py    # NEW — default-`forbidden` cases, containment carrier,
│                                     #   four-surface additivity, safety negatives
└── test_sdd_invocation_governance.py # EDIT — absent-declaration cases (superset direction)

tests/fixtures/
└── nested_sdd.py                     # REUSED unchanged (074a): temp repo, two seats,
                                      #   two agent definitions, one goal with an open Target

.specify/instructions.md              # REGENERATED by scripts/bash/generate-instructions.sh
                                      #   (never hand-edited; the compatibility symlinks point at it)
```

**Structure Decision**: this slice extends the existing SDD-framework layout and creates **no new
top-level directory** — three test files in `tests/contract/`, five in-place edits to owners that
already exist, one reused fixture, and one regenerated runtime file. The documentation plane and the
runtime plane stay separate: every edit above is a source edit, and the `.specify/` runtime copies
listed under Mirror Obligations are produced by the mirror and generator machinery.

### Mirror Obligations

The live mirror pairs are defined in `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`; command templates
fan out only to `regen-command-copies.py` per-tool copies. This slice edits **no**
`templates/commands/**` file, so no per-tool command copy is regenerated.

**Baseline drift measured before this plan's edits** (2026-10-29, `test-evidence/plan-stage-checks.md`
§ 5): `python3 scripts/python/sync-mirrors.py --check` → exit `0`, every pair `ok` — `templates/` 22
files, `skills/external/` 406, `skills/internal/` 136, `agents/` 3, `scripts/` 114, `shared/` 59;
`regen-command-copies.py --check` → `OK`. There is **zero** pre-existing drift, so the criterion for
every row below is "no NEW drift" *and* it is measurable as "clean". (These counts are higher than
`074a`'s recorded 405/113/58 because `074a` added three files — a baseline is read at the commit it was
taken.)

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/internal/create-team/SKILL.md`, `skills/internal/create-team/references/conceptual-model.md`, `skills/internal/run-agent/SKILL.md` | `.specify/skills/internal/…` via `sync-mirrors.py` (`skills/internal/` pair, 136 files) | `python3 scripts/python/sync-mirrors.py --check` — no new drift vs the measured-clean baseline |
| `shared/guidelines/proactive-trigger.md` | `.specify/shared/guidelines/proactive-trigger.md` via `sync-mirrors.py` (`shared/` pair, 59 files) | same check, same criterion |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` via `sync-mirrors.py` (`templates/` pair, 22 files) | same check, same criterion |
| `templates/instructions-template.md` → generated runtime instructions | `.specify/instructions.md` via `scripts/bash/generate-instructions.sh` (additive section reconcile); `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` are symlinks at it and need no repair | run the generator once, then: the new section heading is present in `.specify/instructions.md`; no existing section was rewritten; the byte delta is within the section's declared ceiling. Measured before the edit: live 41,948 B, template 34,666 B, budget 32,768 B — the criterion is a declared ceiling plus a measured delta, never "fits the budget" |
| `tests/contract/test_sdd_invocation_governance.py` | none — test files have no mirror pair | collect the pre-change node-id set for this file (set `S1` in `test-evidence/compat-baseline-nodeids.txt`) before editing, then assert post ⊇ pre |

## Complexity Tracking

N/A — the Constitution Check has no ❌ Fail and no ⚠ Partial row.

## Plan Revision

**2026-10-29 — analyze-fix round 1 (slice `074b-nested-governance`).** One remediation pass after
`/speckit.analyze` returned 0 CRITICAL / 2 HIGH / 7 MEDIUM / 5 LOW. The requirement text is not
re-derived here; each entry records what changed in the design and why.

1. **F-01 (HIGH) — one containment criterion instead of two (classification: minor).**
   `contracts/compat-and-safety.md` gains a reading rule between C-6 and C-7 that reads FR-006/SC-001's
   "same verdict" and FR-007/C-6's "every pre-change case passes" as **one** decidable criterion over
   the set both claims reach (`S2`, the standalone-driver entry suite): for a case id that is already
   **red** in the pre-change baseline the criterion is **verdict-unchanged**, and "MUST pass" governs
   only the case ids that are **green** in that baseline. Reason: two criteria stood over one shared
   suite and they disagree exactly on an already-red case — "same verdict" permits it to stay red while
   "MUST pass" forbids it, and T023 forbids repairing a pre-existing red, so no reader could tell which
   one governs. The edit changes no scope, no architecture, no clause id and no clause count (still 30,
   `md-bold-closed`); it is text-level disambiguation, hence **minor**, and the plan's scope needs no
   re-anchoring beyond this record.
2. **Text-level alignment carried in the same pass (classification: minor).** MEDIUM/LOW findings whose
   remedy is wording rather than design: C-25 and `data-model.md` V-5 now state **one** cardinality (at
   most one attributed ledger item per report — exactly one with a Target, none without) instead of
   "exactly one" versus "at most one"; FR-001's "summary" is bound to the **existing** goal-level
   summary channel so it cannot be read as a second artifact; C-29 names the handoff's integration
   identity and the incomplete-handoff rule (missing identity ⇒ the outer layer MUST NOT report
   success); `contracts/diffusion.md` `Measures` names the DoD / task rows that grade the diffusion
   faces instead of `—`, adding no SC; C-11 declares its anchor prose-level (`requirements.md`
   § Overview) and C-20 declares itself a design-level criterion; C-13 states the Stage boundary
   **bidirectionally** and lets the seat's operating object — not the name — decide a definition that
   carries both duties.

## Parent Design Mapping

**Reading**: this slice's requirement entries come from
`.specify/specs/074b-nested-governance/requirements.md` § Parent Mapping (parent FR 020–024 and
parent FR 026–028; parent SC 005 and parent SC 008; parent STR 001–003 and STR 007–010). The parent
design at `.specify/specs/074-goal-team-sdd-unification/` is the design authority: every projected
clause names the parent clause in its `parent C-nn` tag, and the parent contract file is recorded here
so a reader can reach the source without opening all five. Attribution is drawn **per requirement
entry**, never per parent file's physical grouping (D-1).

### Slice FR → parent FR → parent clause(s) → parent contract file

| Slice FR | Parent FR | Parent clause(s) | Parent contract file |
|----------|-----------|------------------|----------------------|
| FR-001 | parent FR 020 | C-50, C-51, C-52 | `report-and-attribution.md` |
| FR-002 | parent FR 021 | C-47, C-48, C-49, C-53, C-54 (report-section facet) | `report-and-attribution.md` |
| FR-003 | parent FR 022 | C-55, C-66 (Stage-vocabulary facet) | `diffusion-and-compat.md` |
| FR-004 | parent FR 023 | C-25, C-26 (C-60 cited; claimed by `074a`) | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-005 | parent FR 024 | C-56, C-57 | `diffusion-and-compat.md` |
| FR-006 | parent FR 026 | C-27, C-65 (C-16/C-28 cited; delivered by `074a`) | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-007 | parent FR 027 | C-61, C-62, C-33, C-43, C-44 | `nested-invocation.md`, `diffusion-and-compat.md` |
| FR-008 | parent FR 028 | C-63, C-67 (parent FR 028 facet) (C-30/C-64 cited; delivered elsewhere) | `diffusion-and-compat.md`, `authorization-and-probe.md` |

### Slice SC → parent SC → parent clause(s)

| Slice SC | Parent SC | Parent clause(s) | Delivered facet in this slice |
|----------|-----------|------------------|-------------------------------|
| SC-001 | parent SC 005 | C-27, C-61, C-62 | superset + same-verdict over 7 frozen node-id sets (17 files, 266 cases) |
| SC-002 | parent SC 008 | C-51, C-52 | parsed Goal field set identical before/after (12 keys); attribution only through the existing ledger reference |

### Parent clauses that are `074a`'s or another owner's (cited, not claimed)

| Parent clause(s) | Serves | Owner |
|------------------|--------|-------|
| C-15, C-16, C-17, C-18, C-19, C-20, C-21, C-22, C-23, C-24, C-28, C-29 | parent FR 003–006 (key set, seat map, AND resolution, anti-nesting predicate, depth-2 chain) | `074a-authorized-routing` |
| C-31, C-32, C-34…C-42, C-45, C-46 | parent FR 015–019, 025 (entry form, handoff, stop at review, stall, setup path) | `074a-authorized-routing` |
| C-54 (parent FR 013 facet) | parent FR 013 (verdict record carrier) | `074a-authorized-routing` (D-2) |
| C-58, C-59 | parent FR 025 (invocation kinds, bootstrap/maintenance authorization) | `074a-authorized-routing` |
| C-60 (key-set facet) | parent FR 003 (authoring baseline lists the key) | `074a-authorized-routing` |
| C-66 (parent FR 018 facet) | parent FR 018 (no second store) | `074a-authorized-routing` |
| C-1…C-14 | parent FR 001–014 (control hierarchy, routing verdict) | `074a-authorized-routing` |
| C-30, C-64 | parent FR 026/028, 018 | `074a-authorized-routing` (cited by this slice's C-12) |

**Recorded discrepancy, not repaired**: `074a`'s deferred table lists 21 clause ids while its prose says
"20", and parent C-66's Stage-vocabulary facet is named in that prose but absent from the table. This
slice claims per the prose and per the parent's own FR→clause rows (parent C-66 serves parent FR 022),
and does not edit the sibling's committed plan — nothing downstream depends on the integer, and a
correction there would rewrite another slice's artifact.

## Cross-Slice Attribution

The slice's requirement file already ratified D-1/D-2/D-3; this section states how the design honours
each, in the same order.

- **D-1 — attribution follows the requirement entry, not the parent file's grouping.** The design set
  covers local FR-001–FR-008 and SC-001–SC-002. Each projected clause names its parent clause as
  *source*, drawn from `report-and-attribution.md` (parent C-47…C-54) and `diffusion-and-compat.md`
  (parent C-55…C-67) plus two clauses from `authorization-and-probe.md` (parent C-25/C-26) and three
  from `nested-invocation.md` (parent C-33/C-43/C-44). Clauses in those files that serve `074a`'s
  entries (parent C-58, C-59, C-64, C-66's parent FR 018 facet, C-54's parent FR 013 facet) are **not** claimed; the
  parent-deferred table above records each of them with its owner. Because the parent's files are
  organized by theme, this slice's three files are organized by its own behaviour groups instead
  (`compat-and-safety` C-1…C-12, `diffusion` C-13…C-20, `report-and-attribution` C-21…C-30), and the
  clause ids stay contiguous across them in file-name order so the coverage audit can partition them.

- **D-2 — the routing verdict is consumed by reference here, never recomputed.** Local C-28 is the
  receiving end of `074a`'s D-2: the section's `routing-verdict reference` points at the verdict that
  `074a` recorded in the Agent execution evidence (inputs, verdict, reason code, actor, user override),
  carried by the handoff and the invoking agent's result. The section copies no input set, no verdict
  table and no reason-code vocabulary (local C-28, guarded by V-10's reverse-count audit), and when the
  record cannot be located the section records the reference as missing while the outer layer is
  forbidden to re-derive it (`requirements.md` § Edge Cases, 5th item). The engine
  `scripts/python/sdd-route.py` is cited as the producer of that record and is not invoked from the
  report-writing step.

- **D-3 — the `## Nested SDD Runs` heading literal and the section's semantics are this slice's.** Local
  STR-007 is the single heading literal; local C-21/C-22/C-23 deliver "mandatory for every run,
  explicit when no invocation occurred, per-invocation fields"; `tests/contract/test_nested_run_report.py`
  is the only new suite that asserts them, and `074a`'s `test_nested_sdd_invocation.py:560` keeps its
  negative assertion (the literal is not present in the driver's handoff reference). Two slices,
  disjoint surfaces: content face in `074a`, section format face here — neither is a second definition
  point, and together they cover parent SC 003.

## Phase 1: Design Artifacts Summary

Counts below were taken from the artifacts on disk after they landed, via the commands quoted — never
pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 10 rulings (RB1–RB10), each with a measured anchor and the rejected alternatives |
| Data model | [`data-model.md`](data-model.md) | 8 entities (E1–E8), 12 validation rules (V-1…V-12), 2 state machines (report-section composition, containment verification) |
| Contracts | [`contracts/`](contracts/) | 3 files, **30 clauses** (C-1…C-30) — `clause_extract.py` reports every file as `md-bold-closed`: `compat-and-safety.md` 12, `diffusion.md` 8, `report-and-attribution.md` 10 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios: S1 (pre-change absence), S3 (goal field-set measurement, teardown executed) and S7 (mirror/flow-class baselines) executed live with output pasted; S6's pre-change half executed; S2, S4, S5 pinned by named tests with premises listed; S6's post-change half is `not-executed` by design |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, 9-row delivery surface, 8-row FR map, 2-row SC map, 9 disclosed rulings, containment statement |
| Containment carrier | [`test-evidence/compat-baseline-nodeids.txt`](test-evidence/compat-baseline-nodeids.txt) | 266 cases across 17 files in 7 named sets (S1 49, S2 25, S3 24, S4 40, S5 36, S6 54, S7 38) |

Executed derivation commands (real output pasted into
[`test-evidence/plan-stage-checks.md`](test-evidence/plan-stage-checks.md)): `clause_extract.py
contracts/*.md` → 30 clauses across 3 files, all `md-bold-closed`, ids contiguous C-1…C-30;
`account-clause-coverage.py --spec-dir …` → **FR lane 8/8 claimed, uncovered 0**, while its clause lane
reports `status: baseline-missing` — expected at plan stage, because the claims are `[green:]` rows in
`tasks.md` and freezing a baseline before any claim exists would make that stage trivially green;
`pre-analyze-check.py --spec-dir … --stage plan` → see the recorded output; `sync-mirrors.py --check` →
exit 0, no drift; `regen-command-copies.py --check` → `OK`; `flow-class-check.py --action check` → 79
units, 0 findings; targeted set (19 files) → 289 passed, 1 pre-existing failed; containment baseline →
266 cases / 7 sets.

## Test Budget Record (targeted-set-v1, `stage_base=plan`)

**E3 stage-status row (targeted evidence)** — `stage=plan`, `row_type=stage-status`, `status=ran`,
`selection_basis=targeted-set-v1` (19 files, `test-evidence/targeted-set-v1-baseline.txt`),
`changed_paths[]=.specify/specs/074b-nested-governance/{plan.md,research.md,data-model.md,contracts/*.md,quickstart.md,feature-ref.md,test-evidence/*}`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt`.

**Full-suite row (docs-only, six reduced fields per
`.specify/skills/sdd-loop-driver/references/efficiency-model.md`)** — `stage=plan`,
`row_type=stage-status`, `status=not-run-docs-only`, `selection_basis=no executable surface changed by
this stage (design artifacts only), so the full suite has no new subject`,
`changed_paths[]=.specify/specs/074b-nested-governance/** (markdown only)`,
`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/plan-stage-checks.md`. Run fields do
not apply and are not reported as `unknown`.
