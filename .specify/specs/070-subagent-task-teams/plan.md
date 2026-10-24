# Implementation Plan: 070-subagent-task-teams

**Branch**: `070-subagent-task-teams` | **Date**: 2026-10-24 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `070-subagent-task-teams` → Feature 070 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD）
**Input**: Specification from `.specify/specs/070-subagent-task-teams/requirements.md`

## Summary

Feature 070 adds a decomposition-and-coordination layer to the existing unattended SDD driver. At a stage boundary the driver derives bounded Work Packages from the stage's own artifacts, validates them with a deterministic gate, dispatches the ready packages through the existing dispatch forms (native subagents locally, detached `stage-runner.sh` processes remotely), lets independent read-only packages overlap within a slot cap while serializing every write package, verifies each package with an independent execution, integrates the verified outputs in a deterministic order with one integrator execution, and only then runs the unchanged stage U4 and sentinel check.

The layer is additive. The driver remains the sole coordinator; stage commands remain opaque; package completion is never a stage completion. Feature 064's line registry, Ownership Manifest, worktree, and integration queue are reused read-only. Feature 067's part brief and dispatch log are extended, not replaced. The improvement is measured from the existing line state spine, with unmeasured metrics recorded as `not_evaluated`, and acceptance is relative to the conservative 2026-10-24 baseline plus zero gate regression.

The design is carried by seven contracts and one data model. Exact schemas, check codes, and event fields live there; this plan records the architecture, the Constitution Check, the delivery surface, the task budget, and the risks.

## Technical Context

**Language/Version**: Python 3.8+ for the two new scripts (stdlib only; this host runs Python 3.11.11), Markdown for the runtime owner document and contracts, Bash for the existing runner paths.
**Primary Dependencies**: none new. Reuses `run-agent` native dispatch, `stage-runner.sh`, `watch-target.sh`, `line-registry.py`, `sync-mirrors.py`, and the existing pytest suites.
**Storage**: the existing line state spine (`wp-plan`, amendment, and `wp-ledger` fences) plus per-entry evidence files under the line state directory. No database, daemon, queue service, or second ledger.
**Testing**: pytest (`tests/unit`, `tests/contract`, `tests/integration`) with the repository's canonical runner `scripts/bash/run-tests.sh`. Tests Mode = **ON**: red-first evidence, contract tests, fixture dry runs, mutation drills, and regression tests. The plan stage changes documentation only and runs the deterministic pre-checks; the two full-suite slots remain implement-baseline and closure.
**Target Platform**: macOS/Linux driver hosts; local native topology, or remote `ssh` + `su` + detached runner topology. The same WP model applies to both.
**Project Type**: SDD framework plus a self-contained external driver skill.
**Performance Goals**: a median stage wall-clock reduction of at least 20% for comparable decomposed `plan` and `review` stages against the conservative anchor, using the OR-04 interval; at most 1.5 stage dispatch attempts per canonical stage (one per stage attempt, not per plan event); and zero gate regressions. These are relative targets only; a result without a comparable benchmark is `not_evaluated`, and an all-`not_evaluated` benchmark blocks closure unless the user records an explicit waiver naming SC-001/SC-002. No absolute wall-clock promise is made.
**Constraints**: 30 FRs at the decomposition ceiling; a task budget of 35 planned steps against a ceiling of 40; read-only concurrency only; write packages serialized; no stage-command change; no second registry/ownership model/integration queue/ledger/brief; no persisted team; no push; no new runtime dependency, service, daemon, or model API.
**Scale/Scope**: one line, the canonical 8-stage chain; decomposition by default for `plan`, `implement`, and `review`; `analyze`/`clarify` only on explicit opt-in; slot cap default 2 with a ceiling of `min(4, line remaining allowance)`; package size bounded by 8 tasks or 40 clauses.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.13.0, in heading order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design section cites FR groups; `contracts/` carries the FR traceability; no untraced technical choice |
| II | Feature-Centric Development | ✅ Pass | Feature 070 is registered; the plan moves Draft → Planned; `feature-ref.md` records the binding and coverage |
| III | Intent-Driven Development | ✅ Pass | The requirements' what/why precede this how; `research.md` records alternatives and trade-offs |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; red-first plan in § 10 and `FN-14`/`FN-15`; unit, contract, integration, non-regression, and mutation layers |
| V | AI Agent Integration Standards | ✅ Pass | No provider/config change; dispatch eligibility stays with `CAPABILITY_MATRIX`; no new agent surface |
| VI | Continuous Quality & Observability | ✅ Pass | JSON outputs with `schema_version`, deterministic gate/report scripts, ledger metrics, docs entry, and zero-gate-regression checks |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan respected; the plan does not enter Implemented; the task budget is below the ceiling; no gate exception |
| VIII | Code as the Single Source of Truth | ✅ Pass | Phase 0 read the driver scripts, the line registry, the test suites, and the mirror generator; the plan cites those surfaces rather than assuming them |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | The scheduler is prompt logic, not a runtime engine; only two small stdlib scripts are added; no daemon/service/dependency; YAGNI applied to parallel writes |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic names (`references/decomposition-model.md`, `templates/stage-team-preset.md`); no reserved ALL-CAPS names added |
| XI | Dogfooding (Self-Application) | ✅ Pass | The feature runs through its own SDD chain; framework-source edits are mirrored by `sync-mirrors.py`; no client-runtime hand edits; deviations are recorded |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses the existing runner, watcher, registry, mirror generator, and test runner; no Tool record covers the two new gates, so writing them is the expected outcome |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | Strengthens Controlled Execution (bounded packages), Change Validation (independent verdicts), Reliable Delivery (deterministic integration), and Learning Capture (ledger metrics); no new scoring system |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | The contracts own the design clauses; the runtime owner document and code are the runtime authority; 058/063/064/067/068 are cited, never restated; contract tests guard the duplication |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | The plan and quickstart define terms at first use, give commands with premises, and point to evidence paths instead of dumping transcripts |
| XVI | Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest) | ✅ Pass | Gate exit 2, missing verdict, integration conflict, and overlap adjudication are surfaced, never silently repaired; subagent dispatch carries the anomaly-line obligation |

**Gates Status**: ✅ All gates pass. No ❌ or ⚠ rows; Complexity Tracking is therefore N/A.

**Re-check after Phase 1** (2026-10-24, after the design artifacts landed): the same 16 rows remain ✅ Pass. New evidence: `data-model.md` (13 entities, 91 validation rules), seven contracts with 110 clauses, the preset schema, and the dry-run/red-first test plan. No new violation and no Complexity Tracking row.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/070-subagent-task-teams/
├── plan.md                       # This file
├── research.md                   # Phase 0 decisions, alternatives, refinements
├── data-model.md                 # Phase 1 entities + validation rules
├── contracts/                    # Phase 1 design contracts
│   ├── work-package-model.md
│   ├── wp-gate.md
│   ├── scheduler-and-dispatch.md
│   ├── verification-and-integration.md
│   ├── stage-team-adapter.md
│   ├── observability-and-retry.md
│   └── fallback-and-nonregression.md
├── quickstart.md                 # Phase 1 operator scenarios with premises
├── feature-ref.md                # Phase 1 binding, delivery surface, overlap adjudication
├── notes/
│   └── overlap-adjudication-plan.md   # Dated overlap record
├── test-evidence/                # Plan-stage deterministic checks and baseline
├── tasks.md                      # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md               # Implementation output (/speckit.implement — NOT created here)
```

### Source Code (repository root)

```text
skills/external/sdd-loop-driver/
├── SKILL.md                                    # + new decomposition H2 section and pointers
├── references/
│   └── decomposition-model.md                  # NEW runtime owner (model, gate use, scheduler, verification, metrics)
├── templates/
│   └── stage-team-preset.md                    # NEW schema-compatible preset
└── scripts/
    ├── wp-gate.py                              # NEW deterministic gate
    └── wp-report.py                            # NEW deterministic report/metrics

docs/reference/skills/sdd-loop-driver.md        # + decomposition layer entry (pointers only)

tests/
├── fixtures/
│   ├── wp_fixtures.py                          # NEW plan/spine/manifest builders
│   └── wp_driver_sim.py                        # NEW deterministic scheduler simulator for dry runs
├── unit/
│   ├── test_wp_gate.py                         # NEW
│   └── test_wp_report.py                       # NEW
├── contract/
│   ├── test_sdd_loop_driver_wp_model.py        # NEW
│   ├── test_sdd_loop_driver_wp_gate.py         # NEW
│   ├── test_sdd_loop_driver_wp_coordination.py # NEW
│   ├── test_sdd_loop_driver_wp_preset.py       # NEW
│   ├── test_non_regression_070.py              # NEW
│   ├── test_wp_mutation_drills.py              # NEW
│   └── test_sdd_loop_driver_skill.py           # pin update for the new H2
└── integration/
    └── test_wp_coordination_dry_runs.py        # NEW fixture dry runs
```

**Structure Decision**: this feature extends the existing self-contained external skill `skills/external/sdd-loop-driver/` with one owner document, one preset, and two scripts, plus their tests and one docs entry. No new top-level directory, command template, agent role, or runtime package is introduced. The feature registry row and feature detail update required by the `data-model.md` E13 `plan` inventory are governance bookkeeping outside FR-027's delivery surface (they are neither driver source, documentation page, nor canonical test suite).

### Mirror Obligations

**Owner declaration**: this section is the sole owner of the mirror source/mirror/verify obligations for this feature. `feature-ref.md` §7, `tasks.md` § Mirror Obligations, and the runtime owner document reference this section and MUST NOT restate its table (Constitution XIV).

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `skills/external/sdd-loop-driver/SKILL.md` | `.specify/skills/sdd-loop-driver/SKILL.md` (via `sync-mirrors.py`) | `sync-mirrors.py --check --only skills/external/sdd-loop-driver` reports no NEW drift against the clean 28-file baseline |
| `skills/external/sdd-loop-driver/references/decomposition-model.md` | `.specify/skills/sdd-loop-driver/references/decomposition-model.md` | same |
| `skills/external/sdd-loop-driver/templates/stage-team-preset.md` | `.specify/skills/sdd-loop-driver/templates/stage-team-preset.md` | same |
| `skills/external/sdd-loop-driver/scripts/wp-gate.py` | `.specify/skills/sdd-loop-driver/scripts/wp-gate.py` | same |
| `skills/external/sdd-loop-driver/scripts/wp-report.py` | `.specify/skills/sdd-loop-driver/scripts/wp-report.py` | same |

`docs/` and `tests/` have no mirror. The mirror is generated, never hand-edited; the baseline drift was measured before this plan (`ok`, 28 files, exit 0).

## Complexity Tracking

N/A — no Constitution Check violation requires justification.

## Phase 0: Research Review

Full decisions, alternatives, environment facts, and design refinements are in `research.md`. The load-bearing conclusions:

1. **One WP record**: the 067 part brief extended with WP fields; one brief format, one dispatch log (WP-12).
2. **One ledger**: the plan and ledger are fences in the existing line state spine; per-entry evidence lives under the state directory (WP-05, WP-09, WP-11, WP-14).
3. **One gate script**: `wp-gate.py` owns plan, preflight, and retry checks; `decomposition-check.py` keeps its Feature-level slicing role (WG-01).
4. **Prompt-level scheduler**: the driver schedules; the gate emits layers and order; a test-only simulator proves the algorithm; no runtime scheduler (SD-01, Constitution IX).
5. **Preset plus procedure**: a schema-compatible preset and a run-scoped projection in the owner document; no team directory (ST-01…ST-12).
6. **Reused dispatch**: native subagents locally and detached `stage-runner.sh` remotely; no new mechanism (SD-07, SD-08, SD-15).
7. **Independent verdicts**: one fresh-context verifier per package; missing verdict equals fail; driver fallback recorded (VI-01…VI-06).
8. **Deterministic integration**: one integrator, graph order, one closing commit, unchanged U4 (VI-07…VI-13).
9. **Ledger-derived retry**: count dispatches, require a delta, escalate on the second failure (OR-14…OR-16).
10. **Measured metrics**: derive from the spine; `not_evaluated` for anything missing; no absolute promise (OR-04…OR-13).

The plan also records twelve design refinements (DR1…DR12 in `research.md` § R17). Each is inside the fixed FR/SC scope; none adds a requirement or a deferred 070b item. The most consequential are the attempt-scoped evidence filenames (DR1, preventing retry evidence overwrite), the mechanical benefit rule (DR7), the sentinel rendering rule (DR8), and the implement-off/067 reconciliation (DR12).

## Design Overview

### 1. Work Package model and ledger

A Work Package carries the FR-001 fields plus `kind`, `source_refs`, `intermediate_outputs`, `bounded_by`, `seat`, and `resources`; full field semantics and validation rules are in `data-model.md` E1 and `contracts/work-package-model.md` WP-01…WP-04.

`wp_id` is `<stage>-wp<NN>`. The driver assigns provisional keys from `source_refs`, builds the DAG, computes topological layers, sorts each layer lexicographically, assigns `01..NN` in layer order, and rewrites `depends_on` to ids; this makes replay deterministic (WP-04). Split children are `<parent>-a`, `<parent>-b`, with distinct outputs; dependents are rewritten to the children (WP-08).

The plan is a JSON object in a `<!-- wp-plan:begin stage=<stage> stage_attempt=<n> -->` fence; the ledger is an append-only JSONL `<!-- wp-ledger:begin -->` fence; amendments are separate fences applied in `seq` order. The driver is the sole writer; package executors never write the spine (WP-05, WP-07, WP-09, WP-18).

`plan_hash` is the canonical-JSON SHA-256 of the effective plan, excluding the hash and timestamps; replaying the same artifacts and rule reproduces it (WP-06). A post-repair plan appends a second `plan` event with `supersedes_plan_hash`; a package that fails twice appends `wp_failed` (WP-10).

Per-package evidence is attempt-scoped (DR1): `wp/<line>-<stage>-<wp_id>-a<N>w<M>.result.json`, `wp/<line>-<stage>-<wp_id>-a<N>w<M>.verdict.json`, `wp/<line>-<stage>-a<N>-gate-<check>.json`, and `reports/<line>-<stage>-a<N>-coordination.{md,json}` (WP-11). The attempt suffixes prevent a U5 retry from overwriting the evidence an earlier ledger pointer references.

For `implement`, the WP record is the 067 part brief extended, and the `dispatch` event carries the 067 fields (`part_id`, `task_ids[]`, `turns`, `test_delta`, `commit`, `outcome`, `duration_seconds`, `token_cost`) (WP-12). There is no second brief or dispatch log.

A non-decomposed stage still writes a plan fence: one synthetic package, the stage sentinel, and the gate verdict fixed by WP-13 / FN-08, so every stage has a recorded decision (WP-13, FN-08, SC-005). The plan fence is the canonical decision record; the ledger `plan` event references it by `plan_hash`. For `implement`, the 070 single-package boundary does not remove the pre-existing 067 part discipline (FN-05, FN-12, DR12).

### 2. Decomposition gate `wp-gate.py`

`wp-gate.py` is a stdlib-only script at `skills/external/sdd-loop-driver/scripts/wp-gate.py` (WG-01). Its CLI is `--spine <path> --stage <stage> --check plan|preflight|retry` with `--plan-json`, `--manifest`, `--repo`, `--slot-cap-ceiling`, `--stage-attempt`, `--wp-id`, `--wp-attempt`, and `--json-out` (WG-02, WG-03, DR2). It prints the WG-04 JSON and uses exit `0` = `admit|single-package`, `1` = `reject`, `2` = input/parse/IO (WG-05).

`--check plan` enforces schema completeness, id uniqueness, acyclicity, dependency resolution, output coverage, boundedness (8 tasks / 40 clauses), kind consistency, pattern compatibility, and the canonical hash (WG-06…WG-12). It also computes the benefit test for an `auto` stage and returns `single-package` with a `not-beneficial` advisory when decomposition would not help (WG-13, DR7).

`--check preflight` adds the FR-009 obligations: manifest coverage and forbidden paths, unordered write/read territory overlaps, unordered write/write overlaps, slot-cap bounds, and resource isolation (WG-14…WG-16). Path normalization follows the 064 Ownership Manifest rule; coverage is equality or directory-prefix containment.

`--check retry` counts ledger dispatches per `(stage, stage_attempt, wp_id)`, admits attempt 1, validates the attempt-2 delta, and rejects attempt 3 as exhausted (WG-17, OR-14…OR-16).

The driver records the gate verdict in the ledger's `plan` event before the first dispatch. A reject blocks dispatch; the driver may repair once (split, serialize, or reduce to one package) as an amendment and re-run the gate; a second reject falls back with `decision=fallback` and `reason=gate-reject`, and the plan fence records the FN-08 fallback verdict with a reference to the reject evidence. Exit 2 falls back with `reason=decomposition-unavailable` and the same FN-08 fallback verdict (WG-18).

### 3. Scheduler and coordination

The scheduler is driver prompt logic (SD-01, Constitution IX). The algorithm:

1. **Ready set**: packages whose `depends_on` all have a `verdict=pass` in the current stage attempt (SD-02).
2. **Write priority**: if any ready package is a write package, stop launching new read-only packages, wait for every running package to settle, dispatch exactly one write package, then resume (SD-03, SD-06).
3. **Read-only concurrency**: otherwise dispatch up to `slot_cap` ready read-only packages, in topological-layer and `wp_id` lexicographic order (SD-04, SD-05).
4. **Collection**: on settle, record the result, dispatch the verifier, and mark the package verified only on a `pass` (SD-09, SD-10, SD-12).
5. **Isolation**: a failure never cancels unrelated running packages; dependents stay blocked (SD-11).
6. **Completion**: after every dispatchable package settles, if any package is failed or unverified, fail the stage gate into U5; otherwise aggregate and integrate (SD-12, VI-06).

The slot cap is `min(requested_or_default, min(4, line remaining allowance))`; the default is 2; a write package's effective concurrency is 1. The gate's `dispatch_layers` and `integration_order` are the deterministic inputs; the driver does not reorder by intuition.

Local topology uses one native host subagent per package through `run-agent`; it never launches `qodercli` locally. If the host cannot issue parallel native calls, the driver records `effective=serial`, `reason=host-no-parallel-native` and proceeds serially (SD-07). Remote topology launches one detached `stage-runner.sh` per package with a unique label `<stage>-<wp_id>` and the WP sentinel; each package keeps its own four-piece evidence set (SD-08). A package is settled only when the runner status and the last non-empty log line agree on the sentinel; then the result file is read (SD-09).

The driver performs the anti-nesting check before dispatch: no driver-skill name, no skill-loading instruction, no loop logic (SD-13). The check is the `run-agent` governance obligation, cited not redefined.

### 4. Stage-team preset and adapter

The preset is `skills/external/sdd-loop-driver/templates/stage-team-preset.md` (ST-01). Its frontmatter carries `preset_id: sdd-stage-team`, `pattern: parallel` (default only), `summary`, `when_to_use`, `signals`, four inputs (`stage`, `wp_graph`, `line`, optional `slot_cap`), four members (`stage-planner`, `stage-worker`, `stage-verifier`, `stage-integrator`), a `config` block, and `provenance` (ST-02, ST-04). Its body carries the six mandatory sections, including `Instantiation`, which forbids creating a team directory (ST-03).

Seat mapping (ST-05): the planner/lead is the driver itself; each package maps to `stage-worker` with one execution; each verdict maps to `stage-verifier` with one fresh-context execution; each decomposed stage attempt maps to one `stage-integrator` execution. Each package's `seat` field records the Role × Stage × Type tuple (E10).

Pattern selection is graph-derived and overrides the preset default: `iteration` only with a complete repair loop (review repair in the first slice); otherwise `parallel` when two or more packages are independent and all are read-only; otherwise `serial` when any write package or dependency edge exists (ST-06, ST-12). `continuous` is never selected (ST-07). A serial stage may still run independent ready read-only packages concurrently (SD-04).

The adapter is a run-scoped projection into the plan fence; it creates no `.specify/teams/<slug>/team.md`, no goal binding, and no team run report (ST-08, ST-09). `create-team` and `run-team` are unchanged (ST-10).

### 5. Independent verifier

Every package gets exactly one fresh-context verifier execution, never the executor (VI-01). The verifier is read-only with respect to repository content, may run the package's declared targeted tests, and must not run a full suite (VI-02). It writes the verdict JSON with `pass|fail`, per-criterion checks, evidence refs, an `execution_id`, and `verified_at`; the driver appends the verdict event (VI-03, VI-05). A missing, malformed, or ambiguous verdict counts as fail (VI-04). If the host cannot spawn a subagent, the driver verifies itself (`driver-u4`) and records the capability fallback; the driver is structurally independent of the executor (VI-01, DR11).

The evidence layout is attempt-scoped: `wp/<line>-<stage>-<wp_id>-a<N>w<M>.verdict.json`, with the `checks[]` entries pointing to outputs, test logs, and ownership evidence (WP-11, VI-03). A dependent unlocks only on a ledger `verdict=pass` with an evidence pointer (SD-02, SD-12).

### 6. Integration and stage close

After every package verifies, the driver dispatches one integrator execution for the stage attempt (VI-11). It receives the plan, the verified outputs, and the stage authority artifacts; it aggregates in topological-layer and `wp_id` lexicographic order, detects missing or contradictory outputs, produces the plan's `integrator_outputs` (for `clarify`, the clarification write-back), makes the single stage-closing commit, and emits `<STAGE>-DONE` as its last non-empty line (VI-07, VI-09, VI-11). `integrator_outputs` are owned by the integrator seat, excluded from package output coverage, and verified by the unchanged stage U4 (FR-003(b), SC-004, WP-15).

Integration stops on a conflict or missing output; no partial commit is presented as a complete stage deliverable (VI-08). For stages without a part-commit discipline, package executors do not commit; the integrator's commit is the only stage commit. For `implement`, part commits are preserved and not rewritten or squashed (VI-10).

Package sentinels are never promoted: only the integrator's `<STAGE>-DONE` (or the standard stage executor's sentinel in a non-decomposed stage) satisfies the stage requirement (VI-12). After integration, the unchanged stage U4 runs: sentinel plus artifact verification plus discipline checks (VI-13). The driver records the `integrate` event, runs the stage U4, runs `wp-report.py`, and appends `stage-close` with the metrics and report pointer (OR-03, OR-11). Closure and merge remain driver-owned, with no push or force merge (VI-14).

### 7. Retry and escalation

The per-package counter is derived from the ledger's `dispatch` events for `(stage, stage_attempt, wp_id)`; there is no counter file (OR-14). Attempt 1 needs no delta. Attempt 2 requires a `retry_delta` changing scope, budget, or topology; `wp-gate.py --check retry` validates the delta: scope strictly smaller or a split into distinct children, budget strictly larger with dispatch-level evidence, or a materially different topology (OR-15). A split is permitted once per lineage: children inherit the parent's attempt count (their sole dispatch is the lineage's retry attempt), split depth is one, and a child is never split again or retried (WG-17, OR-15). An unchanged same-budget rerun is rejected even if reworded (WG-17).

A second failure (or attempt 3) records `wp_failed` with the attempt history and verdict evidence, fails the stage gate, and enters the unchanged U5 stage-retry path; WP retries do not consume the stage retry budget before that escalation (OR-16). A U5 retry starts a new stage attempt with a fresh plan, plan hash, and per-package counter; earlier records remain in the spine (SD-16).

### 8. Metrics and reports

The ledger fields are fixed in `data-model.md` E4 and OR-01. The metric definitions are fixed in OR-04…OR-09:

- **Stage wall-clock**: `stage_u4_at - first started_at`.
- **Critical path**: the duration-weighted longest path through the dependency DAG, using verified executor intervals.
- **Parallelism efficiency**: `sum(package durations) / (wall_clock × max_concurrent)` (the product is in the denominator).
- **Stage executions per canonical stage**: `stage_attempts / 8`, where `stage_attempts` counts distinct `(stage, stage_attempt)` pairs that dispatched at least one package; a repair `plan` event never adds an attempt.
- **Retry counts**: package and stage separately.
- **Manual interventions**: user continue/retry/status messages per run and the run's driver-session count; both are optional inputs, and the reported rate is per session; otherwise `not_evaluated`.

`wp-report.py` writes the Markdown and JSON reports and prints the derived metrics, accepting `--stage-u4-at`, `--manual-interventions`, and `--sessions` because those values are not derivable before stage close (OR-11, DR6). Both reports carry decisions, pattern, slot cap, order, metrics, retries, verdicts, and evidence paths, never raw transcripts (OR-12).

Any missing source is the literal `not_evaluated`; it is never zero or an estimate, and an SC whose metric is `not_evaluated` is not claimed as met (OR-10). An all-`not_evaluated` benchmark blocks feature closure until a comparable benchmark exists or the user records an explicit waiver naming SC-001 and/or SC-002 (FR-023, OR-10). The benchmark anchor is the conservative upper bound of the dated baseline (plan 70 min, review 37 min); a median requires at least three comparable samples on the same host class and topology; a re-measured baseline uses the OR-04 interval and replaces the anchor, and sources are never mixed (OR-13).

### 9. Opt-out and fallback

The U0 entry declaration carries `decomposition: auto|off`, `decomposition_stages`, and `decomposition_slot_cap`; the stage attempt may carry `decomposition_override` (FN-01). Precedence: feature-level `off` (hard) > stage-attempt override > stage map > built-in defaults (FN-02). Defaults: `plan`/`implement`/`review` = `auto`; `analyze`/`clarify` = `off`; the rest = `off` (FN-03).

`auto` admits decomposition only with a gate `admit`, at least two packages, and the benefit test; otherwise it records `single-package` with `reason=not-beneficial` (FN-04). `off` records `disabled`; a gate reject after the one repair, an unavailable layer (exit 2), or an unrepresentable stage contract records `fallback` with a named cause; both carry the verdict FN-08 assigns to a non-run decision (FN-06). A fallback never runs a partial package set; it runs the standard single-subagent stage path with the unchanged prompt, dispatch, sentinel, and U4 (FN-05, FN-07). Every stage records one decision in the plan fence, the canonical decision record, and the ledger `plan` event references it; a silent run is a gate failure (FN-08, SC-005).

### 10. Tests and evidence

Tests Mode is ON. The test plan is layered:

- **Unit**: `tests/unit/test_wp_gate.py` covers every check code, the hash, benefit, preflight, and retry; `tests/unit/test_wp_report.py` covers each metric, overlap detection, and `not_evaluated`.
- **Contract**: one file per contract group pins the clauses and literals (`test_sdd_loop_driver_wp_model.py`, `..._wp_gate.py`, `..._wp_coordination.py`, `..._wp_preset.py`); the existing skill pin test is intentionally updated for the new H2.
- **Integration dry runs**: `tests/integration/test_wp_coordination_dry_runs.py` uses `tests/fixtures/wp_driver_sim.py` to prove overlapping read-only intervals, write serialization, ownership rejection, deterministic integration, failure isolation, dependency unlock rules, fallback, no nested driver, and no team directory.
- **Non-regression**: `tests/contract/test_non_regression_070.py` pins the 058 sentinel/U4 text, the 063 fast lane/test budget/plan constraint/detach literals, the 064 registry/ownership/worktree/integration interfaces, the 067 part brief/log fields, and the 068 channel boundary.
- **Mutation drills**: `tests/contract/test_wp_mutation_drills.py` points the tests at mutated copies (cycle check removed; write concurrency allowed; missing verdict treated as pass; `not_evaluated` replaced by zero) and asserts each drill turns at least one test red.
- **Red-first evidence**: before implementation, the new tests are run and recorded as failing; the evidence file carries command, exit code, pass/fail counts, changed paths, and an evidence pointer (FN-15). A green check that would not go red is not cited.

The plan stage itself changes documentation only; its deterministic checks are `pre-analyze-check.py --stage plan` and the overlap check, plus the mirror baseline. The two full-suite slots remain the implement baseline and closure (063). The dry-run simulator is test-only and its limitation (it models the prompt algorithm, not an LLM's adherence) is recorded in `research.md` R4 and in the risks table.

## Task Budget

The implementation is designed to fit one slice. The estimate is 35 planned steps against the 40-step ceiling; the tasks stage may split a step but must keep the total at or below the ceiling. If the tasks gate would exceed it, the contingent 070a/070b split in the requirements' Decomposition / Slicing Record applies — no requirement may be deleted to fit.

| Phase | Steps | Contents |
|-------|-------|----------|
| Red-first tests and fixtures | 10 | WP/ledger contracts, gate unit tests, report unit tests, preset/adapter contracts, scheduler/non-regression contracts, dry-run tests, red evidence |
| Scripts | 8 | `wp-gate.py` plan/preflight/retry/CLI; `wp-report.py` metrics/report; green runs and evidence |
| Owner docs and surface | 6 | `decomposition-model.md`, preset, SKILL section, docs page, contract pins and green evidence |
| Dry runs, regression, mutation | 7 | Concurrency/write serialization, ownership/unlock/isolation, integration/sentinel, fallback/no-nested-driver, non-regression, mutation drills, evidence audit |
| Mirror and closure | 4 | Mirror sync and no-new-drift verification, task-stage pre-checks, final evidence, verification handoff |
| **Total** | **35** | |

## Risks and Assumptions

| # | Risk / assumption | Impact | Mitigation | Evidence / owner |
|---|-------------------|--------|------------|------------------|
| R-01 | Remote read-only concurrency runs several `qodercli` processes with their own logs, ports, and caches. | Resource contention, CLI limits, confusing logs. | Slot cap default 2 and ceiling `min(4, allowance)`; unique labels; per-package resources; capability profiles; failure isolation. | 064 line cap; SD-04, SD-08, SD-14; WG-16 |
| R-02 | The slot cap and write serialization limit the achievable wall-clock gain. | The 20% target may not be met. | Relative acceptance only; benchmark with ≥3 samples or `not_evaluated`; no absolute promise. | OR-13; SC-001 |
| R-03 | Verifier independence can degrade when the host cannot spawn a fresh subagent. | A self-verified stage could look green. | Fresh execution preferred; `driver-u4` fallback recorded; `execution_id` distinctness; missing verdict = fail. | VI-01, VI-04; DR11 |
| R-04 | Test baseline variance between this Linux/Python 3.11 host and the dated macOS/Python 3.14 baseline. | Absolute durations and counts are not comparable. | Name-level failure comparison; baseline captured at implement start; benchmark host identity recorded or `not_evaluated`. | FN-14; OR-13; 067 measurement protocol |
| R-05 | New driver files must be mirrored; a missed mirror is the highest-frequency rework source. | Client-runtime drift. | `sync-mirrors.py --write --only skills/external`; `--check` against the clean 28-file baseline; mirror parity suite. | Mirror Obligations; R16 |
| R-06 | The 30-FR ceiling is already reached and the step estimate is close to the 40-step ceiling. | Growth forces a split mid-flight. | No new FR; 35-step estimate; tasks gate checked before analyze; contingent 070a/070b proposal. | Requirements Slicing Record; Task Budget |
| R-07 | Decomposed stages bypass the monolithic stage command, so a command-internal obligation could be missed. | A stage deliverable could be incomplete. | Required-output inventories and acceptance clauses per stage; integrator assembly; unchanged U4; fallback when unrepresentable. | WP-15; R13 |
| R-08 | Attempt-free evidence names would let a retry overwrite prior evidence. | Broken attribution and false history. | Attempt-scoped filenames and `attempt_id` in every record. | DR1; WP-11; V-RES/V-VER |
| R-09 | The 067 part discipline conflicts with a literal reading of 070's single-package path for `implement`. | Two owners could both claim the implement split. | FR-025 wins for large implement stages: 067 remains in force; 070's single-package is a layer boundary. | FN-05, FN-12; DR12 |
| R-10 | The deterministic overlap check reports same-path relations with closed predecessors. | A literal `clear` is unattainable. | Full-surface declaration; recorded adjudication; no narrowing to manufacture green; re-check after the first edit. | feature-ref § 5; notes/overlap-adjudication-plan.md |
| R-11 | A metric could be fabricated or silently zeroed. | False improvement claims. | `not_evaluated` literal; report contract tests; mutation drill replacing `not_evaluated` with zero. | OR-10; FN-14 |
| R-12 | The scheduler is prompt-level, so a live LLM might deviate from the documented algorithm. | Dry runs could pass while a real run misbehaves. | Deterministic simulator + contract pins + ledger audit; live claims require spine evidence; limitation disclosed. | R4; SD-01; SC-007 |
| R-13 | Downstream edits could silently rewrite plan artifacts. | Design contract drift. | The 063 plan-only-minor-fix constraint stays active; new 070 artifacts are plan-owned; `PLAN-EDIT:` declarations. | FN-10; 063 efficiency model § 3 |
| R-14 | The new H2 changes the pinned SKILL section set. | A contract test goes red. | Intentional pin update in `test_sdd_loop_driver_skill.py`, recorded as a pin change, not a weakening. | R20; delivery surface |
| R-15 | Local hosts without parallel native calls cannot realize read-only concurrency. | No wall-clock gain locally. | Recorded `host-no-parallel-native` and effective concurrency; no measured claim without overlap evidence. | SD-07; SC-007 |

## Dependencies and Sequencing

1. **Red before green**: tests and fixtures land before the scripts; the red run is recorded (FN-15).
2. **Scripts before docs**: the owner document is written from the implemented behavior and the contracts; the contract tests pin the agreement.
3. **Docs before dry runs**: the simulator and the prompt-owner text are needed for the dry-run assertions.
4. **Dry runs before mirror**: the mirror sync is the last source change; the mirror check must show no NEW drift.
5. **Tasks stage after plan**: the tasks stage derives the step list and re-runs the decomposition gate; the step ceiling is checked there.
6. **Implementation stage**: baseline full suite at the first implement step; targeted sets elsewhere; closure full suite after review. The 063 plan-only-minor-fix constraint becomes active at plan U4.

## Out of Scope Preserved

Nested drivers; stage-command internals, sentinel literals, U4 semantics, and quality-gate criteria; a second line registry, ownership model, worktree model, integration queue, CLI profile store, ledger, or brief format; parallel write packages and WP-level sub-worktrees; multi-feature or multi-line scheduling beyond 064; a persisted team per stage or any `create-team`/`run-team` modification; the `continuous` pattern or a long-lived team loop; a new service, daemon, external dependency, or model API; push, force merge, or confirmation-gate bypass; weakening any quality gate, test-budget slot, or independent-verification requirement.

## Phase 1: Design Artifacts Summary

Filled after the Phase 1 artifacts landed on disk (counts measured from the files, not pre-written).

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research decisions | [`research.md`] | 20 decision sections (R1–R20) + 12 disclosed design refinements (DR1…DR12) |
| Data model | [`data-model.md`] | 13 entities (E1–E13), 91 validation rules |
| Contracts | [`contracts/`] | 7 files, 110 clauses: `work-package-model.md` (WP-01…WP-18), `wp-gate.md` (WG-01…WG-18), `scheduler-and-dispatch.md` (SD-01…SD-16), `verification-and-integration.md` (VI-01…VI-14), `stage-team-adapter.md` (ST-01…ST-12), `observability-and-retry.md` (OR-01…OR-16), `fallback-and-nonregression.md` (FN-01…FN-16) |
| Quickstart | [`quickstart.md`] | 7 scenarios (A–G) plus the regression/evidence command block; every new-script example carries an execution-status note and premises |
| Feature reference | [`feature-ref.md`] | Binding, delivered surface, FR 30/30 and SC 8/8 coverage, overlap adjudication, mirror-obligations pointer (owner: this file § Mirror Obligations), required-output-inventory pointer (owner: `data-model.md` E13) |

**Drift from the Phase 0 expectation**: none. The contract count is 7 and the clause count is 110; the data model carries 13 entities and 91 validation rules. The plan deliberately keeps the exact schemas in the contracts and data model rather than duplicating them here.
