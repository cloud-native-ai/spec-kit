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
templates fan out only to `regen-command-copies.py` per-tool copies (`.specify/templates/commands/`
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
