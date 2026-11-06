# Feature Reference — 087-speckit-visualization

**Feature ID**: 087 | **Feature Name**: Speckit 框架可视化（Speckit Framework Visualization）
**Requirement key**: `087-speckit-visualization` | **Branch**: `087-speckit-visualization`
**Status at this stage**: `Draft → Planned` | **Date**: 2026-11-06

## Binding

| Item | Value |
|------|-------|
| Feature index row | `.specify/memory/features.md` (ID 087) |
| Feature detail | `.specify/memory/features/087.md` |
| Spec | `.specify/specs/087-speckit-visualization/requirements.md` |
| Plan | `.specify/specs/087-speckit-visualization/plan.md` |
| Flow class | `execution` (`**Flow Class**` line in `requirements.md`; read by `flow-class-check.py --action lookup --unit-id "spec:087-speckit-visualization"` → `flow_class: execution`, `source: declaration`) |

The binding was decided at `/speckit.clarify` (Clarifications Q1: a new Feature 087, no existing Feature owns
"current-state visibility of concurrent/asynchronous flows") and is recorded here so `/speckit.tasks` and
`/speckit.implement` never mistake the spec directory name for a Feature identity.

## Shared delivery root

The feature's framework-source delivery root is the **repository root**, distributed by `specify init` from these
five source trees and their mirrors:

| Framework source tree | Mirror / generated target | Distribution route |
|-----------------------|---------------------------|--------------------|
| `shared/` | `.specify/shared/` | `scripts/python/sync-mirrors.py` |
| `agents/` | `.specify/agents/templates/` | `scripts/python/sync-mirrors.py` |
| `skills/external/<name>/` | `.specify/skills/<name>/` | `scripts/python/sync-mirrors.py` (the `external/` component is dropped) |
| `skills/internal/<name>/` | `.specify/skills/internal/<name>/` | `scripts/python/sync-mirrors.py` |
| `scripts/` | `.specify/scripts/` | `scripts/python/sync-mirrors.py` (**STRICT** pair) |
| `templates/commands/` | `.claude/commands/`, `.github/prompts/`, `.opencode/command/`, `.qoder/commands/` | `scripts/python/regen-command-copies.py` (`.specify/templates/commands/` is retired) |

**Overlap declaration for later stages**: this feature's write scope is disjoint from every other active feature
line at the time of planning — checked by listing the line registry
(`line-registry.py --action list --active --format json` returned one active line, `087-speckit-visualization`
itself). The four source trees this feature edits (`shared/`, `agents/`, `skills/`, `scripts/`, `templates/commands/`)
are the framework's hot spots, so `/speckit.implement` MUST re-run the overlap check before the first write rather
than inherit this reading.

## Delivered paths (dry inventory)

The set `/speckit.implement` must produce, enumerated so contract `ownership-map.contract.md` C-52 (OM-06) can audit
it as a file list rather than a claim. Counts are the plan's target, not a claim about the tree; the rows below are
the enumeration owner (28 paths).

| # | Path | Kind | FR |
|---|------|------|----|
| 1 | `shared/guidelines/reporting-obligations.md` | NEW owner document | FR-001, FR-002, FR-003, FR-004, FR-008, FR-009, FR-010, FR-011, FR-013, FR-014, FR-015, FR-016, FR-018, FR-020, FR-021 |
| 2 | `.specify/shared/guidelines/reporting-obligations.md` | mirror (generated) | same |
| 3 | `agents/reporter.agent.md` | NEW Agent Template | FR-005 |
| 4 | `.specify/agents/templates/reporter.agent.md` | mirror (generated) | FR-005 |
| 5 | `skills/internal/create-team/SKILL.md` | edit — the seat obligation + the guard's call site | FR-006, FR-021 |
| 6 | `skills/internal/create-team/references/create-mode.md` | edit — schema note, create step, runtime-omission condition | FR-006, FR-021 |
| 7 | `skills/internal/create-team/references/patterns.md` | edit — one pointer line to the reporting cadence (threshold table unchanged) | FR-008, FR-009 |
| 8 | `skills/internal/create-team/scripts/validate-roster.py` | NEW deterministic guard | FR-006, FR-017 |
| 9 | `.specify/skills/internal/create-team/` (paths 5–8 mirrored) | mirror (generated) | — |
| 10 | `skills/external/coaching-skills/SKILL.md` | edit — § Dispatch Payload gains exactly one field, one forbidden class, one return clause | FR-019, FR-013 |
| 11 | `.specify/skills/coaching-skills/SKILL.md` | mirror (generated) | — |
| 12 | `templates/commands/status.md` | NEW thin command (`/speckit.status`) | FR-022 |
| 13 | `.claude/commands/speckit.status.md` | per-tool copy (generated) | FR-022 |
| 14 | `.github/prompts/speckit.status.prompt.md` | per-tool copy (generated) | FR-022 |
| 15 | `.opencode/command/speckit.status.md` | per-tool copy (generated) | FR-022 |
| 16 | `.qoder/commands/speckit.status.md` | per-tool copy (generated) | FR-022 |
| 17 | `scripts/python/status-digest.py` | NEW deterministic script (digest + guard + report) | FR-007, FR-011, FR-012, FR-017, FR-022 |
| 18 | `.specify/scripts/python/status-digest.py` | mirror (generated) | — |
| 19 | `shared/definitions/subagent-definitions.md` | edit — one pointer line (§ Dispatch-Time Governance Obligation) | FR-013, FR-014 |
| 20 | `.specify/shared/definitions/subagent-definitions.md` | mirror (generated) | — |
| 21 | `shared/workflow/external-dispatch-recipes.md` | edit — one pointer line | FR-013 |
| 22 | `.specify/shared/workflow/external-dispatch-recipes.md` | mirror (generated) | — |
| 23 | `tests/contract/test_reporting_obligations.py` | NEW contract test | FR-001…FR-005, FR-014, FR-015, FR-016, FR-018, FR-020 |
| 24 | `tests/contract/test_roster_reporter_seat.py` | NEW contract test | FR-006, FR-021 |
| 25 | `tests/contract/test_coaching_reporting_duty.py` | NEW contract test | FR-008, FR-009, FR-010, FR-013, FR-019 |
| 26 | `tests/contract/test_status_digest.py` | NEW contract test | FR-011, FR-012, FR-017, FR-022 |
| 27 | `tests/unit/test_status_digest_unit.py` | NEW unit test | FR-011, FR-012 |
| 28 | `tests/contract/test_coaching_dispatch_contract.py` | edit — `REQUIRED_FIELDS` gains `reporting-cadence` (declared expected delta, contract OM-05) | FR-019 |

**Audit answer for contract OM-06**: no path in the list above is a scheduler, a timer service, a daemon, a
persistent store, a console channel, a registry, a state spine or a ledger. Paths 8 and 17 are deterministic,
single-file, stdlib-only readers; path 1 is a document; paths 3 and 12 are prompt surfaces.

**Roster population (no roster is a delivered path)**: `FR-006` binds exactly two sets — rosters created or modified
through the team-creation entry from this feature's delivering commit onward, plus rosters passed explicitly by
path. No `.specify/teams/*/team.md` path appears above because none is bound: the rosters already in the repository
are outside the population, they are not amended or backfilled with a `reporting-reason`, and a guard run that
supplies no population path reports its roster proposition `not-evaluated` rather than judging them (owner:
`contracts/reporting-obligations.contract.md` C-04).

## FR → artifact map

| FR | Delivered by (path # from the table) | Contract clause |
|----|--------------------------------------|-----------------|
| FR-001 | 1, 2 | C-01 |
| FR-002 | 1 | C-02 |
| FR-003 | 1, 5, 12 | C-03, C-24 |
| FR-004 | 1, 3 | C-05, C-23 |
| FR-005 | 3, 4 | C-14, C-19 |
| FR-006 | 5, 6, 8, 9 | C-15, C-16, C-17 |
| FR-007 | 1, 3 | C-22, C-26 |
| FR-008 | 1, 10 | C-32, C-33 |
| FR-009 | 1, 7, 10 | C-07, C-35 |
| FR-010 | 1, 10 | C-08, C-34 |
| FR-011 | 1, 12, 17 | C-09, C-42, C-44 |
| FR-012 | 1, 17 | C-43 |
| FR-013 | 1, 10, 19, 21 | C-40, C-39 |
| FR-014 | 1, 3, 19 | C-27, C-12 |
| FR-015 | 1, 3 | C-28, C-10 |
| FR-016 | 1, 3 | C-29, C-11 |
| FR-017 | 8, 17 | C-41, C-46 |
| FR-018 | whole set | C-13, C-49, C-50 |
| FR-019 | 10, 11, 28 | C-37, C-38, C-39 |
| FR-020 | 1, 12 | C-03, C-30 |
| FR-021 | 5, 6, 8 | C-18, C-04 |
| FR-022 | 12–18 | C-41 |

Every FR has at least one delivered path and one contract clause. (29 FR; FR-023…FR-029 rows are added by the plan refresh, 22 rows before it).

## Consuming / Consumed Owners

| Relation | Document | Note |
|----------|----------|------|
| owns | `shared/guidelines/reporting-obligations.md` (NEW) | the new owner; the facts it owns are enumerated once, in `contracts/reporting-obligations.contract.md` C-01 (mirroring `requirements.md` FR-001), and are not re-enumerated here |
| consumes | `shared/guidelines/progress-reporting.md` | cadence anchor, four content elements, deferral rule, not-a-gate, measured figures, dispatch channel — reached by section anchor, **no clause rewritten** |
| consumes | `shared/definitions/subagent-definitions.md` | artifact triplet, liveness monitoring, three execution modes; **one pointer line added** |
| consumes | `shared/workflow/external-dispatch-recipes.md` | dispatch recipes; **one pointer line added** |
| preserves | `shared/guidelines/fast-fail.md` § 子代理派发注入 | referenced, never modified |
| consumes | `shared/guidelines/user-facing-comprehension.md` | the emitted line is a governed surface |
| preserves | `shared/guidelines/confirmation-gates.md` | no gate added; blocking count stays 27 |
| extends | `skills/internal/create-team/` | roster schema note + create step + `scripts/validate-roster.py` |
| amends | `skills/external/coaching-skills/SKILL.md` § Dispatch Payload | exactly one field, one forbidden-content class, one return-handling clause; closed-set invariant preserved |
| consumes | `skills/external/sdd-loop-driver/scripts/line-registry.py` | registry entry fields + `STATE_VALUES` / `ACTIVE_STATES` + directory resolution — read-only |

This table is the same relation set contract `contracts/ownership-map.contract.md` C-48 declares (ten rows, same
order and same relation words over the same ten documents);
`tests/contract/test_reporting_obligations.py` asserts the two agree.

## Neighbouring Features (binding decision record — carried forward)

| Candidate | Why not bound |
|-----------|---------------|
| 070 driving-subagent decomposition | its subject is *division of labour*, not what the user sees |
| 074 Goal/Team/Agent × SDD unification | its subject is *hierarchy governance*, not visibility |
| 085 temporary Goal/Team + multi-agent concurrency | owns *how many* agents run; this Feature owns *what the user sees* |
| 062 humanize / 079 run-output | both rewrite output **once at wrap-up**; this Feature adds a cadence **during** a run |

## Strengthened harness dimension

Per constitution XIII, this feature strengthens **Task Understanding** (the user can see which stage/work package is
active) and **Reliable Delivery** (a stalled sub-flow becomes visible instead of silent). It adds no scoring
system, maturity report or runtime evaluation platform.

## Stage status

| Stage | State | Artifact |
|-------|-------|----------|
| requirements | done (29 FR / 14 SC, 15 assumptions, 5 clarifications) | `requirements.md` |
| clarify | done (Feature binding + 5 adjudications) | `requirements.md` § Clarifications |
| plan | **this stage** | `plan.md`, `research.md`, `data-model.md`, `contracts/` (6 files / 52 clauses `C-01`…`C-52`), `quickstart.md` (8 scenarios A–H), this file (28 delivered paths) |
| tasks | not started | — |
| checklist / analyze / implement / review / closure | not started | — |
