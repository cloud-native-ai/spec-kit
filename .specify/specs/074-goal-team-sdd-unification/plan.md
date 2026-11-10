# Implementation Plan: 074-goal-team-sdd-unification

**Branch**: `074-goal-team-sdd-unification` | **Date**: 2026-10-28 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一（Unified Goal/Team/Agent Control Hierarchy with SDD Invocation）
**Input**: Specification from `.specify/specs/074-goal-team-sdd-unification/requirements.md` (28 FR / 8 SC / 11 Shared Strings; requirements + clarify ratified 2026-10-28)

## Summary

Feature 074 turns two parallel delivery paths into one hierarchy. Today the Goal → Team → Agent
chain and the standalone SDD flow (`sdd-loop-driver`, U0–U6) meet only inside Feature 070's
driver-owned stage-team preset: the Goal/Team layer never learns an SDD flow exists, and an SDD run
never knows which Goal or Target it advances. After this feature an authorized seat can start one
bounded nested SDD run for a declared scope, the run stops at review and hands back its artifacts,
evidence, findings and integration identity, and the outer team reports and attributes it — while
the decision *whether* to run SDD at all becomes one deterministic three-value verdict
(`sdd` / `direct` / `adjudicate`) over five declared inputs.

The technical approach is deliberately thin on new machinery: **one new vocabulary owner**
(`shared/definitions/sdd-routing-definitions.md`), **one new neutral metadata key**
(`sdd-invocation`, framework-level, never rendered to a host tool), **one frontmatter field**
(`seats:` in `team.md`), **one new read-only stdlib engine** (`scripts/python/sdd-route.py` with
`route` / `authorize` / `golden`), and **one in-place narrowing** of the existing anti-nesting
obligation at its existing owner site. Everything else is diffusion by reference: the project
instructions gain a pointer, the trigger discipline gains one sentence, the team conceptual model
disambiguates its Stage dimension, the report contract gains one mandatory section, and the driver
gains one entry form that validates before U0. No new `/speckit.*` command, skill, store, registry,
ledger, state spine, integration queue, scheduler, confirmation gate, or automatic transmission is
introduced (FR-028).

**Run input classification** (the planning skill's step 2): the dispatch brief arrived as run
parameters — background facts, the eight delivery surfaces to cover, and the discipline defaults —
not as a new requirement set. No mid-run addendum arrived, so `requirements.md` was not
restructured and its checklist was not re-validated.

## Technical Context

**Language/Version**: Python 3.8+ for the new engine and the contract tests (project floor per
`pyproject.toml`; host 3.11.11, pytest 8.4.2); Markdown for the owner document, templates, skills,
and shared guidelines.
**Primary Dependencies**: none new. Reuses the CLI's neutral metadata validator
(`NEUTRAL_AGENT_METADATA_KEYS` / `parse_agent_frontmatter` / `validate_agent_metadata` in
`src/specify_cli/__init__.py`), `scripts/python/sync-mirrors.py`,
`scripts/python/regen-command-copies.py`, `scripts/bash/generate-instructions.sh`, and the existing
line registry (`skills/external/sdd-loop-driver/scripts/line-registry.py`).
**Storage**: files only, and no new store. The agent capability rides the existing agent-definition
frontmatter; the seat policy rides the existing `team.md` frontmatter; a verdict is recorded in the
existing team run report or the Agent execution evidence; a nested run's durable state is the
existing `.specify/state/<line-id>.md` spine; line/worktree identity is the existing line registry
entry.
**Testing**: pytest contract suites under `tests/contract/`. Six new files (one per FR/SC behaviour
group) plus one shared fixture module, all red-first during implementation. Measured pre-change
baseline of the 13-file targeted set: **191 passed, 0 failed** (`test-evidence/targeted-set-v1-baseline.txt`).
Tests Mode = **ON**.
**Target Platform**: the framework repository (source hat) and every consuming client project
(runtime hat); hosts with or without native subagent capability; repositories whose `.specify/`
runtime predates this feature (undecorated teams and agents must behave exactly as before).
**Project Type**: SDD framework — prompt templates, skills, shared definitions, deterministic
scripts, contract tests. No application runtime is added.
**Performance Goals**: not a performance feature. `route` and `authorize` are one frontmatter read
plus one arithmetic decision each; `golden` reads one Markdown table (about a dozen rows). No
network call, no process spawn beyond the engine itself.
**Constraints**: no new command, skill, store, registry, ownership model, integration queue, state
spine, scheduler, daemon, confirmation gate, or automatic feedback transmission; never push; every
projection of an edited source is produced by the mirror/generator machinery, never hand-edited;
the four predecessor contracts named in FR-027 stay additive.
**Scale/Scope**: 28 FR / 8 SC / 11 shared strings → 5 contract files with 67 clauses (C-1…C-67),
11 data-model entities, 29 validation rules, 3 state machines, 1 new engine (3 actions), 12 edited
framework files, 3 new framework files, 6 new test files, 1 declared pin change.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Same-author condition (disclosed, per `shared/workflow/objective-analysis-gate.md`)**: these
design artifacts were authored in this session, and this environment exposes no subagent dispatch
capability while the stage brief fixes `decomposition=single-package` with no subagent dispatch.
Scoring could therefore not be delegated. Every row carries `(direct read, subagent unavailable)`,
and the program-derivable checks were actually executed instead: `clause_extract.py` (5 files, 67
clauses, all `md-bold-closed`), `pre-analyze-check.py --stage plan`, `account-clause-coverage.py`,
`sync-mirrors.py --check` / `regen-command-copies.py --check` (baseline measured clean), `flow-class-check.py`
(no new flow unit), and the 191-case targeted suite — evidence in `test-evidence/`.

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.15.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design decision cites an FR or a recorded ruling: the owner document (row 1 of the delivery surface) is created *because* FR-014 requires one owner, and each of `research.md` R1–R14 names the FR it serves (direct read, subagent unavailable) |
| II | Feature-Centric Development | ✅ Pass | Feature 074 is bound and registered; this stage advances `Draft → Planned` and records key changes in `.specify/memory/features/074.md`; no feature is created, merged, or split (direct read, subagent unavailable) |
| III | Intent-Driven Development | ✅ Pass | The spec's five user stories fix the what/why; `research.md` records the rejected alternative behind every structural choice (second engine, second skill, preset addition, gold table duplication) (direct read, subagent unavailable) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Six new behavior groups with named pinning tests, red-first by plan; the pre-change case sets are frozen as node-id sets before any edit (C-61/C-62); the fixture proves the authorized/unauthorized split the framework's own repo cannot reach (direct read, subagent unavailable) |
| V | AI Agent Integration Standards | ✅ Pass | No agent roster, provider, or config-key change. The new metadata key is tool-neutral by construction (`renders_to_tools = False`), so no host's field mapping changes; `test_tool_mapping.py` (in the 191-case baseline) keeps every rendering key mapped (direct read, subagent unavailable) |
| VI | Continuous Quality & Observability | ✅ Pass | The verdict, the authorization resolution, and the nested outcome are all recorded with named reason codes and source paths; the containment claims are measured, not asserted; no speculative capability is added (FR-028) (direct read, subagent unavailable) |
| VII | Specification-Plan-Task-Implementation Workflow (NON-NEGOTIABLE) | ✅ Pass | requirements → clarify → plan respected; status ceiling `Planned`; the feature reuses an existing Feature rather than creating one (direct read, subagent unavailable) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 re-measured the surfaces before designing: the neutral key tuple shape at `src/specify_cli/__init__.py:116-144`, the flat-only frontmatter parser at `:224-229`, the flat team.md reader at `scripts/python/goal-utils.py:325-336`, the driver U0 table at `sdd-loop-driver/SKILL.md:31-42`; `research.md` quotes each (direct read, subagent unavailable) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | One engine for two predicates, one owner document, one report section, one entry form; explicitly no new command, skill, store, registry, queue, scheduler, or daemon (C-30/C-63/C-67); authorization is a lookup, not a service (direct read, subagent unavailable) |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic lowercase names (`sdd-routing-definitions.md`, `nested-invocation.md`); no reserved ALL-CAPS name is used; mandated names (`SKILL.md`) unchanged (direct read, subagent unavailable) |
| XI | Dogfooding (Self-Application) | ✅ Pass | Every edit is a framework-source edit carried by the mirror/generator flow (hat declared in `feature-ref.md` § 2); the mechanism fix lands at the owner site (the anti-nesting obligation is narrowed where it lives, not patched in a prompt) (direct read, subagent unavailable) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the CLI validator, the mirror/generator engines, and the line registry instead of re-implementing them; where no Tool record covers routing or authorization, writing the engine is the expected outcome (`shared/workflow/tool-reuse-gate.md`) (direct read, subagent unavailable) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Task Understanding (a decidable rule replaces per-agent thresholds — US2) and Controlled Execution (a bounded, authorized, governed nested path — US1/US3); no scoring system, maturity report, or recording engine is added (direct read, subagent unavailable) |
| XIV | One Source Of Truth (Authority & Reference Discipline) | ✅ Pass | The four routing facts have exactly one owner and are cited by path from the instructions, the trigger discipline, the driver, the team surfaces, and the tests; the neutral key set stays in the CLI; V-19 and contract C-56/C-66 are the mechanical guards against a second copy (direct read, subagent unavailable) |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The new surfaces are addressed to agents and maintainers and use the project's existing vocabulary; the instructions section stays pointer-level with the owner's path; quickstart disclaimers name premises so a reader can act without opening the engine (direct read, subagent unavailable) |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Every refusal names the failing half or condition instead of a bare denial (C-19/C-29/C-32); an unreadable seat map is malformed input, never a policy value; the same-author condition and the subagent-unavailable condition are disclosed rather than papered over (direct read, subagent unavailable) |
| XVII | Directory Governance (Named, Documented, Ignored When Temporary) | ✅ Pass | No new directory is created: the new files land in existing directories (`shared/definitions/`, `skills/.../references/`, `scripts/python/`, `tests/contract/`, `tests/fixtures/`); the fixture's scratch repo uses the sanctioned temp root (direct read, subagent unavailable) |
| XVIII | Grounded Naming | ✅ Pass | Names follow the user's own vocabulary from the spec (`sdd-invocation`, `seats`, `sdd` / `direct` / `adjudicate`, `## Nested SDD Runs`) and imitate the closest siblings (`flow-class-definitions.md` for the owner document, `flow-class-check.py` for the engine) (direct read, subagent unavailable) |

**Gates Status**: ✅ All gates pass. No ❌ and no ⚠ row, so Complexity Tracking is N/A.

**Re-check after Phase 1** (2026-10-28, after the design artifacts landed): the same eighteen rows
remain ✅ Pass. New evidence: `research.md` (14 rulings, each with a measured anchor),
`data-model.md` (11 entities, 29 validation rules, 3 state machines), five contract files with 67
clauses (all `md-bold-closed`, C-1…C-67 contiguous, 28/28 FR and 8/8 SC cited), `quickstart.md`
(7 scenarios; S7 executed live, S1–S6 with per-example disclaimers and named pinning tests), and
`feature-ref.md` (20-row delivery surface, 28-row FR map, 8-row SC map, 7 disclosed rulings). The
executed program checks are recorded in `test-evidence/`. One precision fix was applied during the
re-check: `quickstart.md` S3 originally paired "ambiguous input" with an input set that was merely
traceability-bound (which the SDD branch owns, not the adjudicate branch); it now uses a genuinely
missing input so the example demonstrates the precedence rule it claims. No new violation; no
Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/074-goal-team-sdd-unification/
├── plan.md                 # This file (/speckit.plan output)
├── requirements.md         # Input (28 FR / 8 SC / 11 shared strings)
├── research.md             # Phase 0 output: rulings R1–R14 with measured anchors
├── data-model.md           # Phase 1: entities E1–E11, rules V-1…V-29, 3 state machines
├── contracts/              # Phase 1: 5 files, clauses C-1…C-67
│   ├── route-decision.md              # C-1…C-14
│   ├── authorization-and-probe.md     # C-15…C-30
│   ├── nested-invocation.md           # C-31…C-46
│   ├── report-and-attribution.md      # C-47…C-54
│   └── diffusion-and-compat.md        # C-55…C-67
├── quickstart.md           # Phase 1: scenarios S1–S7 (S7 executed; S1–S6 disclaimed per example)
├── feature-ref.md          # Phase 1: binding, delivery surface, FR/SC maps, disclosed rulings
├── checklists/
│   └── requirements.md     # Requirements-stage quality checklist (unchanged by this stage)
├── test-evidence/          # Deterministic check records for this stage
├── tasks.md                # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md         # Implementation output (/speckit.implement — NOT created here)
```

Phase 0 produced 14 rulings with measured evidence, well past the inline threshold
(~50 lines), so `research.md` is a standalone file rather than an inlined section.

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

skills/internal/create-team/
├── SKILL.md                     # EDIT — § Report contract gains mandatory `## Nested SDD Runs`
└── references/
    ├── create-mode.md           # EDIT — team.md schema gains the `seats:` block map
    └── conceptual-model.md      # EDIT — Stage dimension disambiguated from the SDD stage roster

skills/external/sdd-loop-driver/
├── SKILL.md                     # EDIT — § Invoked-from-Team Entry (6 facts, validation,
│                                #   stop-at-review) + one Hard Requirement; standalone unchanged
└── references/
    └── nested-invocation.md     # NEW — handoff schema, closed field set, validation table,
                                 #   failure/stall handoff

templates/
└── instructions-template.md     # EDIT — one pointer-level routing ambient section

shared/guidelines/
└── proactive-trigger.md         # EDIT — one pointer sentence (verdict + authorization)

tests/contract/
├── test_sdd_routing_definitions.py    # NEW
├── test_sdd_routing_engine.py         # NEW
├── test_sdd_authorization.py          # NEW
├── test_sdd_invocation_governance.py  # NEW
├── test_nested_sdd_invocation.py      # NEW
├── test_nested_run_report.py          # NEW
└── test_neutral_metadata_schema.py    # EDIT — the single declared pin change (R12)

tests/fixtures/
└── nested_sdd.py                      # NEW — temp repo: minimal .specify/, two seats, two
                                       #   agent definitions, one goal with an open Target

.specify/instructions.md         # REGENERATED by scripts/bash/generate-instructions.sh
                                 #   (never hand-edited; compatibility symlinks point at it)
```

**Structure Decision**: this spec extends the existing SDD-framework layout; it creates **no new
top-level directory**. Three framework files are new (one owner document, one driver reference, one
engine), twelve are edited, six test files are new and one gains a declared pin change. The
documentation plane and the runtime plane stay separate: every edit in the tree above is a source
edit, and the `.specify/` runtime copies listed under Mirror Obligations are produced by the
mirror/generator machinery.

### Mirror Obligations

The live mirror pairs are defined in `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`; command
templates fan out only to `regen-command-copies.py` per-tool copies (`templates/commands/`
is retired). This spec edits **no** `templates/commands/**` file, so no per-tool command copy is
regenerated.

**Baseline drift measured before this plan's edits** (2026-10-28):
`python3 scripts/python/sync-mirrors.py --check` → exit `0`, every pair `ok` — `templates/` 22
files, `skills/external/` 405, `skills/internal/` 136, `agents/` 3, `scripts/` 113, `shared/` 58;
`regen-command-copies.py` is clean by the same run's first line. There is **zero** pre-existing
drift, so the criterion for every row below is "no NEW drift" *and* it is measurable as "clean".
`.specify/instructions.md` is measured at 41,948 B against the generator's
`INSTRUCTIONS_BUDGET_BYTES=32768` — already over budget before this feature (R8), so its row's
acceptance is a declared per-section byte ceiling plus a measured delta.

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/sdd-routing-definitions.md` (new), `shared/definitions/subagent-definitions.md`, `shared/guidelines/proactive-trigger.md` | `.specify/shared/definitions/…`, `.specify/shared/guidelines/…` via `sync-mirrors.py` (`shared/` pair, 58 files at baseline) | `python3 scripts/python/sync-mirrors.py --check` — no new drift vs the measured-clean baseline |
| `skills/internal/run-agent/SKILL.md`, `skills/internal/create-team/SKILL.md` + its `references/create-mode.md` / `references/conceptual-model.md` | `.specify/skills/internal/…` via `sync-mirrors.py` (`skills/internal/` pair, 136 files) | same check, same criterion |
| `skills/external/sdd-loop-driver/SKILL.md` + new `references/nested-invocation.md` | `.specify/skills/sdd-loop-driver/…` via `sync-mirrors.py` (`skills/external/` pair, 405 files) | same check, same criterion |
| `scripts/python/sdd-route.py` (new) | `.specify/scripts/python/sdd-route.py` via `sync-mirrors.py` (`scripts/` pair, 113 files, strict extras) | same check, same criterion; the copies must be byte-identical, not merely present |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` via `sync-mirrors.py` (`templates/` pair, 22 files) | same check, same criterion |
| `templates/instructions-template.md` → generated runtime instructions | `.specify/instructions.md` via `scripts/bash/generate-instructions.sh` (additive section reconcile); `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` are symlinks at it and need no repair | run the generator once; then assert the new section heading is present in `.specify/instructions.md`, that no existing section was rewritten, and that the file's byte delta matches the declared ceiling (`test_instructions_section_propagation.py` + the size report; no absolute "fits the budget" claim — it was already 41,948 B > 32,768 B before this feature) |
| `src/specify_cli/__init__.py` | none — the CLI package is the source of truth for the neutral key set; no projection carries it | `grep -c 'sdd-invocation' src/specify_cli/__init__.py` = 1 definition point; `test_tool_mapping.py` / `test_neutral_metadata_schema.py` green |

## Complexity Tracking

N/A — the Constitution Check has no ❌ Fail and no ⚠ Partial row.

## Phase 1: Design Artifacts Summary

Counts below were taken from the artifacts on disk after they landed, via the commands quoted —
never pre-written.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | 14 rulings (R1–R14), each with a measured anchor and the rejected alternatives |
| Data model | [`data-model.md`](data-model.md) | 11 entities (E1–E11), 29 validation rules (V-1…V-29), 3 state machines (authorization resolution, nested-run lifecycle, verdict supersession) |
| Contracts | [`contracts/`](contracts/) | 5 files, **67 clauses** (C-1…C-67) — `clause_extract.py` reports every file as `md-bold-closed`: `route-decision.md` 14, `authorization-and-probe.md` 16, `nested-invocation.md` 16, `report-and-attribution.md` 8, `diffusion-and-compat.md` 13 |
| Quickstart | [`quickstart.md`](quickstart.md) | 7 scenarios: S1–S6 not-executed with per-example disclaimers naming premises and pinning tests; S7 executed live 2026-10-28 with outputs pasted (3 sub-checks: mirror baseline, targeted suite, instructions size) |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, 20-row delivery surface, 28-row FR map, 8-row SC map, 7 disclosed rulings, containment/non-regression statement |

Executed derivation commands (real output pasted into `test-evidence/plan-stage-checks.md`):
`clause_extract.py contracts/*.md` → 67 clauses across 5 files, all `md-bold-closed`, ids
contiguous (C-1…C-67); FR/SC citation groups cover 28/28 FR and 8/8 SC;
`account-clause-coverage.py` → **FR lane 28/28 claimed, uncovered 0**, while its clause lane
reports `status: baseline-missing` — expected at plan stage, because the baseline freezes with the
tasks-stage claims and a baseline frozen now (before any claim exists) would make that stage
trivially green; `pre-analyze-check.py --stage plan`
(`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`) → `decision=pass errors=0
advisories=0 fr=28 sc=8` (`clauses=0` because that checker's legacy prefix pattern does not read
the canonical `**C-N**` form); `sync-mirrors.py --check` → exit 0, no drift;
`regen-command-copies.py --check` → clean; targeted suite → 191 passed.

## Merged from slices

<!-- source: 074a-authorized-routing -->

### Parent Design Mapping


**Reading**: the slice's requirement entries come from
`.specify/specs/074a-authorized-routing/requirements.md` § Parent Mapping (parent FR-001–FR-019 plus
parent FR 025, parent SC-001–SC-004 / SC 006 / SC 007, parent STR-001–STR-009 / STR 011). The parent
design at `.specify/specs/074-goal-team-sdd-unification/` is the design authority: every slice clause is
a projection of the parent clause named in its `父 C-nn` tag, and the parent contract file is recorded
here so a reader can reach the source without opening all five files. Attribution is drawn **per
requirement entry**, never per parent file's physical grouping (D-1).

#### Slice FR → parent FR → parent clause → parent contract file

| Slice FR | Parent FR | Parent clause(s) | Parent contract file |
|----------|-----------|------------------|----------------------|
| FR-001 | FR-001 | C-002 | `route-decision.md` |
| FR-002 | FR-002 | C-003 | `route-decision.md` |
| FR-003 | FR-003 | C-015, C-60 | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-004 | FR-004 | C-016, C-001, C-002, C-003 | `authorization-and-probe.md` |
| FR-005 | FR-005 | C-004, C-005, C-013, C-59 | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-006 | FR-006 | C-006, C-007, C-008 | `authorization-and-probe.md` |
| FR-007 | FR-007 | C-013, C-014 | `route-decision.md` |
| FR-008 | FR-008 | C-004, C-005, C-006 | `route-decision.md` |
| FR-009 | FR-009 | C-007 | `route-decision.md` |
| FR-010 | FR-010 | C-006, C-008 | `route-decision.md` |
| FR-011 | FR-011 | C-009, C-010 | `route-decision.md` |
| FR-012 | FR-012 | C-011 | `route-decision.md` |
| FR-013 | FR-013 | C-012, C-54 (FR-013 facet, D-2) | `route-decision.md`, `report-and-attribution.md` |
| FR-014 | FR-014 | C-001, C-005, C-013, C-014, C-66 (FR-014 facet) | `route-decision.md`, `diffusion-and-compat.md` |
| FR-015 | FR-015 | C-047, C-048 | `nested-invocation.md` |
| FR-016 | FR-016 | C-050, C-051, C-052, C-053, C-054, C-003 | `nested-invocation.md` |
| FR-017 | FR-017 | C-052, C-057, C-003 | `nested-invocation.md` |
| FR-018 | FR-018 | C-008, C-014, C-055, C-64 (FR-018 facet) | `authorization-and-probe.md`, `nested-invocation.md`, `diffusion-and-compat.md` |
| FR-019 | FR-019 | C-056 | `nested-invocation.md` |
| FR-025 | parent FR 025 | C-002, C-58, C-59, C-67 | `nested-invocation.md`, `diffusion-and-compat.md` |

#### Slice SC → parent SC → parent clause(s)

| Slice SC | Parent SC | Parent clause(s) | Delivered facet in this slice |
|----------|-----------|------------------|-------------------------------|
| SC-001 | SC-001 | C-003, C-013 | authorization refusal names the failing half, with both source paths |
| SC-002 | SC-002 | C-010, C-013, C-014 | golden table judged row by row; repeated evaluation identical |
| SC-003 | SC-003 | C-058 (+ parent C-48 deferred) | content face per D-3: artifact chain, zero merge/push, path references |
| SC-004 | SC-004 | C-012 (+ parent C-65 deferred) | stage executors cannot start; unqualified prompts blocked; pre-existing cases green |
| SC-006 | parent SC 006 | C-008, C-014, C-055, C-64 | no second registry / ledger / spine / ownership / queue |
| SC-007 | parent SC 007 | C-009, C-014 | ambiguous or conflicting input never yields direct |

#### Parent clauses deferred to `074b-nested-governance` (not counted as slice coverage)

20 of the parent design's 67 clauses fall outside this slice, because the requirement entries they
serve belong to the sibling slice. They are listed so their absence from `contracts/` is a recorded
decision rather than an omission:

| Parent clause(s) | Serves | Slice that owns it |
|------------------|--------|--------------------|
| C-009, C-010 | parent FR 023 (Agent responsibility statement; leaf stays leaf) | `074b-nested-governance` |
| C-011, C-65 | parent FR 026 (default-`forbidden` containment claim) | `074b-nested-governance` |
| C-049, C-059, C-001 | parent FR 027 (additive on the four predecessor surfaces) | `074b-nested-governance` |
| C-004, C-48, C-49, C-53 | parent FR 021 (the `## Nested SDD Runs` report section) | `074b-nested-governance` |
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

### Plan Revision


**2026-10-29 — analyze-fix round 1 (slice `074a-authorized-routing`).** Authorized by the driver for
one plan re-review (efficiency-model §3.5(a)) after `/speckit.analyze` returned 0 CRITICAL / 3 HIGH /
8 MEDIUM / 3 LOW. Each entry records the decision and the reason; the requirement text each one
projects is already in `requirements.md` and is read there, never re-derived here.

1. **F-01 — `authorize` exit alphabet (substantive: C-008, C-012, `quickstart.md` S4, `tasks.md` T007).**
   Decision: `authorize` exits `0` for **any** authorization verdict — allowed and refused alike — and
   `2` for malformed or unreadable input; a refusal is expressed by the JSON `verdict` / `reason`
   fields together with the failing half, never by the process status. Reason: the pre-revision text
   carried two contradictory alphabets for one engine (C-012 fixed `0` / `2` for `route`, while
   `quickstart.md` S4 documented `0` / `2` / `3` for `authorize`), so a caller could not tell
   "refused" from "engine failed", and any test written from one surface would have contradicted the
   other. Both verdict-producing actions now share one two-valued alphabet, and the refusal/error
   distinction lives where the record is. Pinned by `tests/contract/test_sdd_authorization.py`, whose
   T007 obligation now asserts `0` on the refused case.
2. **HIGH-1 — definition-class closure (substantive: C-002, C-004, with C-005 / C-006 / C-008 kept in
   step).** Decision: `definition-class` is a value of `change_nature` — the five inputs stay five —
   its membership is derived from the target path by the predicate owned by `requirements.md` FR-008,
   and the change is cross-cutting by default, bounded only on a declared bounded correction with a
   recorded rationale. Reason: the class was an open phrase ("templates that generate them") while
   both the cross-cutting default and the bounded-correction escape keyed off class membership, so no
   implementer could decide membership; carrying it inside the declared change nature closes the set
   without adding the sixth input C-002 forbids. C-005's and C-006's first conditions are now read off
   the `feature` / `maintenance` values instead of an unmapped one, and C-008's conflict pair uses the
   `feature` literal.
3. **HIGH-2 — `SDD assignment` defined (substantive, narrow: C-009).** Decision: the third predicate
   condition names a defined term — a member duty whose routing decision is recorded as [[STR-004]],
   with the definition owned by `requirements.md` FR-005. Reason: two readings survived (a recorded
   `sdd` verdict vs. any dispatch intending to run SDD) and they differ exactly on the dispatch FR-005
   exists to block. The three conditions themselves are unchanged.
4. **Driver-adjudicated MEDIUM repairs touching this plan's artifacts** (decisions recorded in the
   state spine; listed here so the plan does not read as untouched): C-013's per-member cap escape is
   removed in favour of a hard cap of one run per member (B-04); C-014 names the two SC-001 carriers
   (B-01); C-009 makes the FR-011 reason code mandatory on an override record (B-03); C-010 defines
   `write-bearing change` by pointer to FR-007 (C-03); `data-model.md` E4 / E7 carry the same three
   alignments; and the delivery-surface counts become 15 rows = 9 new + 6 edited with `feature-ref.md`
   § 2 as the owner (F-02).

**What this revision does not do**: it changes no clause id, adds no clause, moves no clause between
files, defers no clause differently, and re-opens no requirement. The clause count stays 47 and the
C-001…C-004 partition `tasks.md` claims is untouched, so every `[green:]` claim still resolves. The same
eighteen Constitution Check rows remain ✅ Pass: no principle depends on the exit alphabet or on the
class phrase, and the one-source-of-truth row is strengthened rather than weakened, because the path
predicate now has a single owner in `requirements.md` FR-008 that the contracts cite.

<!-- source: 074b-nested-governance -->

### Plan Revision


**2026-10-29 — analyze-fix round 1 (slice `074b-nested-governance`).** One remediation pass after
`/speckit.analyze` returned 0 CRITICAL / 2 HIGH / 7 MEDIUM / 5 LOW. The requirement text is not
re-derived here; each entry records what changed in the design and why.

1. **F-01 (HIGH) — one containment criterion instead of two (classification: minor).**
   `contracts/compat-and-safety.md` gains a reading rule between C-006 and C-007 that reads FR-026/SC-005's
   "same verdict" and FR-027/C-006's "every pre-change case passes" as **one** decidable criterion over
   the set both claims reach (`S2`, the standalone-driver entry suite): for a case id that is already
   **red** in the pre-change baseline the criterion is **verdict-unchanged**, and "MUST pass" governs
   only the case ids that are **green** in that baseline. Reason: two criteria stood over one shared
   suite and they disagree exactly on an already-red case — "same verdict" permits it to stay red while
   "MUST pass" forbids it, and T055 forbids repairing a pre-existing red, so no reader could tell which
   one governs. The edit changes no scope, no architecture, no clause id and no clause count (still 30,
   `md-bold-closed`); it is text-level disambiguation, hence **minor**, and the plan's scope needs no
   re-anchoring beyond this record.
2. **Text-level alignment carried in the same pass (classification: minor).** MEDIUM/LOW findings whose
   remedy is wording rather than design: C-059 and `data-model.md` V-5 now state **one** cardinality (at
   most one attributed ledger item per report — exactly one with a Target, none without) instead of
   "exactly one" versus "at most one"; FR-020's "summary" is bound to the **existing** goal-level
   summary channel so it cannot be read as a second artifact; C-063 names the handoff's integration
   identity and the incomplete-handoff rule (missing identity ⇒ the outer layer MUST NOT report
   success); `contracts/diffusion.md` `Measures` names the DoD / task rows that grade the diffusion
   faces instead of `—`, adding no SC; C-011 declares its anchor prose-level (`requirements.md`
   § Overview) and C-008 declares itself a design-level criterion; C-001 states the Stage boundary
   **bidirectionally** and lets the seat's operating object — not the name — decide a definition that
   carries both duties.

### Parent Design Mapping


**Reading**: this slice's requirement entries come from
`.specify/specs/074b-nested-governance/requirements.md` § Parent Mapping (parent FR 020–024 and
parent FR 026–028; parent SC 005 and parent SC 008; parent STR 001–003 and STR 007–010). The parent
design at `.specify/specs/074-goal-team-sdd-unification/` is the design authority: every projected
clause names the parent clause in its `parent C-nn` tag, and the parent contract file is recorded here
so a reader can reach the source without opening all five. Attribution is drawn **per requirement
entry**, never per parent file's physical grouping (D-1).

#### Slice FR → parent FR → parent clause(s) → parent contract file

| Slice FR | Parent FR | Parent clause(s) | Parent contract file |
|----------|-----------|------------------|----------------------|
| FR-020 | parent FR 020 | C-50, C-51, C-52 | `report-and-attribution.md` |
| FR-021 | parent FR 021 | C-47, C-48, C-49, C-53, C-54 (report-section facet) | `report-and-attribution.md` |
| FR-022 | parent FR 022 | C-55, C-66 (Stage-vocabulary facet) | `diffusion-and-compat.md` |
| FR-023 | parent FR 023 | C-059, C-060 (C-60 cited; claimed by `074a`) | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-024 | parent FR 024 | C-56, C-57 | `diffusion-and-compat.md` |
| FR-026 | parent FR 026 | C-061, C-65 (C-004/C-062 cited; delivered by `074a`) | `authorization-and-probe.md`, `diffusion-and-compat.md` |
| FR-027 | parent FR 027 | C-61, C-62, C-33, C-43, C-44 | `nested-invocation.md`, `diffusion-and-compat.md` |
| FR-028 | parent FR 028 | C-63, C-67 (parent FR 028 facet) (C-064/C-64 cited; delivered elsewhere) | `diffusion-and-compat.md`, `authorization-and-probe.md` |

#### Slice SC → parent SC → parent clause(s)

| Slice SC | Parent SC | Parent clause(s) | Delivered facet in this slice |
|----------|-----------|------------------|-------------------------------|
| SC-005 | parent SC 005 | C-061, C-61, C-62 | superset + same-verdict over 7 frozen node-id sets (17 files, 266 cases) |
| SC-008 | parent SC 008 | C-51, C-52 | parsed Goal field set identical before/after (12 keys); attribution only through the existing ledger reference |

#### Parent clauses that are `074a`'s or another owner's (cited, not claimed)

| Parent clause(s) | Serves | Owner |
|------------------|--------|-------|
| C-003, C-004, C-005, C-006, C-007, C-008, C-055, C-056, C-057, C-058, C-062, C-063 | parent FR 003–006 (key set, seat map, AND resolution, anti-nesting predicate, depth-2 chain) | `074a-authorized-routing` |
| C-31, C-32, C-34…C-42, C-45, C-46 | parent FR 015–019, 025 (entry form, handoff, stop at review, stall, setup path) | `074a-authorized-routing` |
| C-54 (parent FR 013 facet) | parent FR 013 (verdict record carrier) | `074a-authorized-routing` (D-2) |
| C-58, C-59 | parent FR 025 (invocation kinds, bootstrap/maintenance authorization) | `074a-authorized-routing` |
| C-60 (key-set facet) | parent FR 003 (authoring baseline lists the key) | `074a-authorized-routing` |
| C-66 (parent FR 018 facet) | parent FR 018 (no second store) | `074a-authorized-routing` |
| C-001…C-002 | parent FR 001–014 (control hierarchy, routing verdict) | `074a-authorized-routing` |
| C-064, C-64 | parent FR 026/028, 018 | `074a-authorized-routing` (cited by this slice's C-012) |

**Recorded discrepancy, not repaired**: `074a`'s deferred table lists 21 clause ids while its prose says
"20", and parent C-66's Stage-vocabulary facet is named in that prose but absent from the table. This
slice claims per the prose and per the parent's own FR→clause rows (parent C-66 serves parent FR 022),
and does not edit the sibling's committed plan — nothing downstream depends on the integer, and a
correction there would rewrite another slice's artifact.

### Cross-Slice Attribution


The slice's requirement file already ratified D-1/D-2/D-3; this section states how the design honours
each, in the same order.

- **D-1 — attribution follows the requirement entry, not the parent file's grouping.** The design set
  covers local FR-020–FR-028 and SC-005–SC-008. Each projected clause names its parent clause as
  *source*, drawn from `report-and-attribution.md` (parent C-47…C-54) and `diffusion-and-compat.md`
  (parent C-55…C-67) plus two clauses from `authorization-and-probe.md` (parent C-059/C-060) and three
  from `nested-invocation.md` (parent C-33/C-43/C-44). Clauses in those files that serve `074a`'s
  entries (parent C-58, C-59, C-64, C-66's parent FR 018 facet, C-54's parent FR 013 facet) are **not** claimed; the
  parent-deferred table above records each of them with its owner. Because the parent's files are
  organized by theme, this slice's three files are organized by its own behaviour groups instead
  (`compat-and-safety` C-001…C-012, `diffusion` C-001…C-008, `report-and-attribution` C-055…C-064), and the
  clause ids stay contiguous across them in file-name order so the coverage audit can partition them.

- **D-2 — the routing verdict is consumed by reference here, never recomputed.** Local C-062 is the
  receiving end of `074a`'s D-2: the section's `routing-verdict reference` points at the verdict that
  `074a` recorded in the Agent execution evidence (inputs, verdict, reason code, actor, user override),
  carried by the handoff and the invoking agent's result. The section copies no input set, no verdict
  table and no reason-code vocabulary (local C-062, guarded by V-10's reverse-count audit), and when the
  record cannot be located the section records the reference as missing while the outer layer is
  forbidden to re-derive it (`requirements.md` § Edge Cases, 5th item). The engine
  `scripts/python/sdd-route.py` is cited as the producer of that record and is not invoked from the
  report-writing step.

- **D-3 — the `## Nested SDD Runs` heading literal and the section's semantics are this slice's.** Local
  STR-010 is the single heading literal; local C-055/C-056/C-057 deliver "mandatory for every run,
  explicit when no invocation occurred, per-invocation fields"; `tests/contract/test_nested_run_report.py`
  is the only new suite that asserts them, and `074a`'s `test_nested_sdd_invocation.py:560` keeps its
  negative assertion (the literal is not present in the driver's handoff reference). Two slices,
  disjoint surfaces: content face in `074a`, section format face here — neither is a second definition
  point, and together they cover parent SC 003.

### Test Budget Record (targeted-set-v1, `stage_base=plan`)


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
