# Data Model: 070-subagent-task-teams

**Feature**: 070 — Task Decomposition & Team Coordination for Subagent-Driven SDD
**Created**: 2026-10-24
**Normative contracts**: `contracts/work-package-model.md`, `contracts/wp-gate.md`, `contracts/scheduler-and-dispatch.md`, `contracts/verification-and-integration.md`, `contracts/stage-team-adapter.md`, `contracts/observability-and-retry.md`, `contracts/fallback-and-nonregression.md`.

This file defines the entities, fields, relationships, and validation rules. Where a field name or literal is also pinned by a contract clause, the clause is the design authority and this file is the schema projection; the implementation's runtime owner is `skills/external/sdd-loop-driver/references/decomposition-model.md` plus the two scripts, with contract tests guarding the agreement.

## Entity map

```text
StageDecompositionDecision (E8)
        │ resolves
        ▼
WPPlan (E2) ── amendments ──▶ PlanAmendment (E3)
   │  packages[]                    │
   ▼                                │
WorkPackage (E1) ◀──────────────────┘
   │ depends_on
   ├──▶ WPResult (E5) ──▶ WPVerdict (E6) ◀── VerificationExecution (E7)
   ├──▶ SeatMapping (E10) ◀── StageTeamPreset (E9)
   └──▶ WPLedgerEvent (E4) ──▶ StageCloseRecord (E12) ──▶ StageCoordinationReport (E11)

DecompositionRule (E13) constrains WPPlan.rule and required_outputs.
```

## E1 — WorkPackage

The bounded unit of stage work (FR-001). One package has one accountable seat and one acceptance evidence set.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `wp_id` | string | yes | `<stage>-wp<NN>` (child ids `<parent>-a`, `<parent>-b`, …). Stable within a stage attempt. |
| `stage` | enum | yes | `plan`, `implement`, `review`, `analyze`, `clarify`. |
| `objective` | string | yes | One bounded outcome; non-empty. |
| `kind` | enum | yes | `read-only` or `write`. |
| `source_refs` | string[] | yes | Stable source anchors (for example `contracts/x.md#clause` or `tasks.md#T012`); used for ID assignment and replay. |
| `inputs` | string[] | yes | Repo-relative paths or named artifacts; may be empty only for a pure discovery package with a declared acceptance source. |
| `outputs` | string[] | yes | Repo-relative paths or named artifacts the package produces. |
| `intermediate_outputs` | string[] | no | Outputs consumed only by dependents, not required stage outputs. |
| `owned_paths` | string[] | yes | Write territory; empty for `read-only`. |
| `read_only_paths` | string[] | yes | Paths the package may read; may be empty (means no path restriction beyond the line manifest). |
| `depends_on` | string[] | yes | WP ids; empty for roots. |
| `parallel_safe` | boolean | yes | True only for `read-only` packages. |
| `max_turns` | integer | yes | Positive turn budget. |
| `bounded_by` | object | yes | `{unit: tasks|clauses|artifacts|acceptance, count: positive integer}`. |
| `acceptance` | object[] | yes | At least one `{id, check, evidence}`; `id` unique within the package. |
| `sentinel` | string | yes | `WP-<WP_ID_UPPER>-DONE` (rendering rule DR8). |
| `evidence` | string | yes | State-dir-relative evidence directory for this package. |
| `seat` | object | yes | `{role: stage-worker, stage: executor, type: Worker}`. |
| `resources` | object | yes | `{ports, tmp_dir, cache_dir, shared_readonly}`; absent values use the literal `none`; `shared_readonly` is an array. |
| `superseded_by` | string[] | amendment only | Present only after a split retry; the parent is not schedulable. |
| `dispatch_topology` | enum | derived | `parallel-native`, `serial-native`, or `detached-runner`; computed from the plan topology and concurrency, not hand-authored. |

**Validation rules**

- **V-WP.1**: All required fields are present and non-empty (empty arrays are legal only where stated). Missing any field → `schema-missing`.
- **V-WP.2**: `kind=read-only` requires `owned_paths=[]`; `kind=write` requires a non-empty `owned_paths`. Violation → `kind-mismatch`.
- **V-WP.3**: `parallel_safe=true` requires `kind=read-only`. Violation → `kind-mismatch`.
- **V-WP.4**: `wp_id` is unique within the effective plan; the format is `<stage>-wp<NN>` for planned packages or `<parent>-a|b|…` for split children.
- **V-WP.5**: `depends_on` names only packages in the effective plan and the graph is acyclic; a dependency on a `superseded_by` parent is rewritten to its children.
- **V-WP.6**: Every required stage output is claimed by exactly one package's `outputs`; an intermediate output must be consumed by at least one dependent's `inputs`.
- **V-WP.7**: `bounded_by.count` is positive; `unit=tasks` allows at most 8; `unit=clauses` allows at most 40; `artifacts` and `acceptance` allow any positive count.
- **V-WP.8**: `max_turns` is a positive integer.
- **V-WP.9**: `acceptance` contains at least one entry and every entry's `id`, `check`, and `evidence` are non-empty.
- **V-WP.10**: `sentinel` equals `WP-` + `wp_id` upper-cased with `-` retained + `-DONE`, except that a child id's suffix is retained (for example `WP-PLAN-WP03-A-DONE`).
- **V-WP.11**: `resources` carries all four keys; a value is `none` or a non-empty string/array. A concurrently dispatched package must satisfy the isolation rule (V-DEC.6 / WG-16).
- **V-WP.12**: `superseded_by` appears only in an amendment; a superseded package is excluded from readiness and dispatch.

## E2 — WPPlan

The stage decomposition record written before the first package dispatch (FR-004, WP-05, WP-06).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | integer | yes | `1`. |
| `line_id` | string | yes | Line label from the spine. |
| `run_id` | string | yes | Run id from the line envelope. |
| `stage` | enum | yes | One of the five decomposed stages. |
| `stage_attempt` | integer | yes | ≥ 1. |
| `decision` | enum | yes | `decomposed`, `single-package`, `disabled`, `fallback`. |
| `reason` | string | yes | One line; for fallback one of `gate-reject`, `decomposition-unavailable`, `not-beneficial`. |
| `rule` | enum/null | yes | `decompose-plan-v1`, `decompose-implement-v1`, `decompose-review-v1`, `decompose-investigation-v1`, or `null` for non-decomposed decisions. |
| `source_artifacts` | string[] | yes | Repo-relative paths the decomposition was derived from (non-empty for `decomposed`). |
| `required_outputs` | string[] | yes | Run-specific coverage inventory (non-empty for `decomposed`). |
| `pattern` | enum | yes | `parallel`, `serial`, or `iteration`. |
| `tie_break` | enum | yes | Exactly `wp_id-lexicographic` in the first slice. |
| `slot_cap` | integer | yes | 1..min(4, line remaining allowance). |
| `slot_cap_requested` | integer | no | Pre-clamp request; defaults to `slot_cap`. |
| `slot_cap_ceiling` | integer | no | Resolved ceiling at plan time. |
| `topology` | enum | no | `native` (default) or `detached`; used by retry topology checks and dispatch. |
| `repair_loop` | object/null | conditional | Required iff `pattern=iteration`: `{max_iterations, stop_condition, findings_source}`. |
| `packages` | object[] | yes | Exactly one package for non-decomposed decisions; one or more for `decomposed`. |
| `plan_hash` | string | yes | `sha256:<hex>` over the canonical effective plan (V-PLAN.7). |

**Validation rules**

- **V-PLAN.1**: `schema_version=1`; `stage` and `decision` are in their closed sets; `stage_attempt ≥ 1`.
- **V-PLAN.2**: `decision=decomposed` requires a non-null `rule`, at least two packages, non-empty `source_artifacts` and `required_outputs`. A non-decomposed decision requires `rule=null` and exactly one package.
- **V-PLAN.3**: `pattern=iteration` iff `repair_loop` is present. `repair_loop.max_iterations` is positive, and `stop_condition` and `findings_source` are non-empty. `continuous` is never valid.
- **V-PLAN.4**: `tie_break` is exactly `wp_id-lexicographic`.
- **V-PLAN.5**: `1 ≤ slot_cap ≤ slot_cap_ceiling`; `slot_cap ≥ 2` when `pattern=parallel`; a single-package plan uses `slot_cap=1`.
- **V-PLAN.6**: The package graph is acyclic and every required output is covered exactly once; these are the WG-07/WG-08 checks.
- **V-PLAN.7**: `plan_hash` is the SHA-256 of the canonical JSON (sorted keys, UTF-8, separators `,` and `:`, `ensure_ascii=false`) of the effective plan with `plan_hash`, `slot_cap_requested`, `slot_cap_ceiling`, and every key ending in `_at` (or named `at`) removed. The same artifacts and rule yield the same hash on replay.
- **V-PLAN.8**: `source_artifacts` paths are repo-relative and exist at plan time; a missing source is `schema-missing` or a recorded fallback cause.
- **V-PLAN.9**: The effective plan is the original plan with amendments applied in `seq` order; the latest `plan_hash` wins.
- **V-PLAN.10**: A plan written for a stage other than the five enumerated stages is invalid.
- **V-PLAN.11**: `slot_cap_requested` above the ceiling is clamped before writing; the recorded `slot_cap` is the clamped value and `reason` names the clamp.
- **V-PLAN.12**: For `decision=decomposed`, `pattern=parallel` requires every package to be `read-only` and independent; otherwise `serial` (or `iteration` under V-PLAN.3) is required.

## E3 — PlanAmendment

Append-only correction to a plan (WP-07, WP-08).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | integer | yes | `1`. |
| `stage` | enum | yes | Matches the plan. |
| `stage_attempt` | integer | yes | Matches the plan. |
| `seq` | integer | yes | Starts at 1; strictly increasing per stage attempt. |
| `supersedes_plan_hash` | string | yes | The hash this amendment builds on. |
| `reason` | string | yes | One line. |
| `wp_id` | string | conditional | Present for a package retry or a package-scope amendment. |
| `wp_attempt` | integer | conditional | Present with `wp_id`; the attempt being authorized (2 in the first slice). |
| `retry_delta` | object | conditional | Required for a retry amendment; schema in E13. |
| `packages` | object[] | yes | Full replacement records for changed packages plus any new child packages. |
| `plan_hash` | string | yes | Canonical hash of the effective plan after applying this amendment. |

**Validation rules**

- **V-AMD.1**: `seq` is strictly increasing; duplicate or out-of-order seq → `schema-missing`.
- **V-AMD.2**: `supersedes_plan_hash` must equal the previous effective hash; a mismatch → `plan-hash-mismatch`.
- **V-AMD.3**: A package record in `packages` either matches an existing `wp_id` (replacement) or is a new child with a distinct id and distinct outputs.
- **V-AMD.4**: A split parent keeps its original record with `superseded_by` listing every child; dependents' `depends_on` are rewritten to all children.
- **V-AMD.5**: A retry amendment carries `wp_id`, `wp_attempt=2`, and a valid `retry_delta` (OR-15).
- **V-AMD.6**: The original plan fence is never edited; amendments are separate fences.
- **V-AMD.7**: `plan_hash` in the amendment covers the effective plan after the amendment, including all prior amendments.
- **V-AMD.8**: An amendment that would remove a required output, introduce a cycle, or create an unordered overlapping write territory is rejected by the next gate run and is not dispatched.

## E4 — WPLedgerEvent

One JSON object per line inside `<!-- wp-ledger:begin -->` … `<!-- wp-ledger:end -->` (WP-09, WP-10, OR-01).

| `event` | Required fields |
|---------|-----------------|
| `plan` | `stage`, `stage_attempt`, `plan_hash`, `decision`, `pattern`, `slot_cap`, `verdict`, `gate_evidence`, `at`; optional `supersedes_plan_hash` |
| `dispatch` | `wp_id`, `stage_attempt`, `wp_attempt`, `dispatch_order`, `started_at`, `effective_concurrency`, `attempt_id`; for `implement` also `part_id`, `task_ids[]`, `turns`, `test_delta`, `commit`, `outcome`, `duration_seconds`, `token_cost` |
| `settle` | `wp_id`, `ended_at`, `runner_status`, `result_ptr`, `outputs[]` |
| `verdict` | `wp_id`, `verdict`, `verifier_execution`, `evidence_ptr`, `at` |
| `retry` | `wp_id`, `wp_attempt`, `retry_delta`, `gate_evidence`, `at` |
| `integrate` | `stage_attempt`, `order[]`, `at`, `conflict`, `commit` |
| `stage-close` | `stage_attempt`, `stage_u4_at`, `wall_clock_seconds`, `critical_path_seconds`, `parallelism_efficiency`, `retries_package`, `retries_stage`, `stage_attempts`, `canonical_stages`, `stage_executions_per_canonical`, `manual_interventions`, `token_cost`, `report_ptr` |
| `wp_failed` | `wp_id`, `attempts`, `verdict_evidence`, `at` |

**Validation rules**

- **V-LED.1**: Every line is a standalone JSON object with a known `event`; unknown event types are rejected by the report and ignored by scheduling.
- **V-LED.2**: `attempt_id` equals `<wp_id>-a<stage_attempt>-w<wp_attempt>`.
- **V-LED.3**: All arithmetic timestamps (`started_at`, `ended_at`, `at`, `stage_u4_at`) are epoch seconds; `verified_at` and `checked_at` in evidence files are ISO-8601.
- **V-LED.4**: The ledger is append-only; the driver never rewrites or truncates lines.
- **V-LED.5**: A `plan` event precedes the first `dispatch` for its stage attempt.
- **V-LED.6**: A `verdict` event for a package appears only after its `settle`.
- **V-LED.7**: A `retry` event carries the gate evidence generated by `wp-gate --check retry`.
- **V-LED.8**: A `stage-close` event appears once per stage attempt, after the stage U4; a failed stage writes `wp_failed` and enters U5 instead.
- **V-LED.9**: `implement` dispatch events carry every 067 field; an unavailable quantity is the literal `not_evaluated`, never a fabricated number.
- **V-LED.10**: A dispatch event's `effective_concurrency` is the number of packages actually running concurrently after the dispatch (1 for a write package).

## E5 — WPResult

`<state-dir>/wp/<line>-<stage>-<wp_id>-a<N>w<M>.result.json` (WP-11, DR1, DR9).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | integer | yes | `1`. |
| `wp_id` | string | yes | Package id. |
| `stage` | enum | yes | Stage name. |
| `stage_attempt` | integer | yes | ≥ 1. |
| `wp_attempt` | integer | yes | ≥ 1. |
| `attempt_id` | string | yes | `<wp_id>-a<N>-w<M>`. |
| `status` | enum | yes | `done`, `failed`, `stalled`, `budget-exhausted`, `anomaly`. |
| `outputs` | string[] | yes | Outputs produced (may be empty on failure). |
| `changed_paths` | string[] | yes | Repo-relative paths actually changed. |
| `tests` | object | no | `{command, rc, passed, failed}` or `not_evaluated`. |
| `commits` | string[] | no | Part commits (implement only; non-implement packages do not commit). |
| `notes` | string | no | One-line residual risk or anomaly. |

**Validation rules**

- **V-RES.1**: The file is written by the package executor (or its runner adapter) before it exits; a missing file counts as `failed`.
- **V-RES.2**: `status=done` requires every declared output to exist; a declared output that does not exist makes the package failed at aggregation.
- **V-RES.3**: `changed_paths` must be within `owned_paths` plus the package's own evidence path; an out-of-territory change fails verification.
- **V-RES.4**: `commits` is empty for non-implement packages.
- **V-RES.5**: A result is an input to verification, never proof of success.
- **V-RES.6**: `tests` that were not run are `not_evaluated`, never zero.

## E6 — WPVerdict

`<state-dir>/wp/<line>-<stage>-<wp_id>-a<N>w<M>.verdict.json` (VI-01…VI-05).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | integer | yes | `1`. |
| `wp_id` | string | yes | Package id. |
| `stage` | enum | yes | Stage name. |
| `stage_attempt` | integer | yes | ≥ 1. |
| `wp_attempt` | integer | yes | ≥ 1. |
| `verdict` | enum | yes | `pass` or `fail`. |
| `checks` | object[] | yes | `{id, kind: artifact|contract|test|adversarial|ownership, command|null, result: pass|fail, evidence_ref}`. |
| `evidence_refs` | string[] | yes | Paths to the checked evidence. |
| `execution_id` | string | yes | Distinct from the package executor's execution id. |
| `verified_at` | string | yes | ISO-8601. |

**Validation rules**

- **V-VER.1**: A missing, unreadable, or malformed verdict counts as `fail`.
- **V-VER.2**: `execution_id` must differ from the package executor's execution id; equality makes the package unverified.
- **V-VER.3**: Every acceptance criterion checked maps to an entry in `checks`; an unaddressed criterion prevents `pass`.
- **V-VER.4**: The verifier is read-only with respect to repository content; its only write is the verdict file and optional evidence under the state directory.
- **V-VER.5**: A verifier may run the package's declared targeted tests, never a full suite (two-slot budget preserved).
- **V-VER.6**: A verdict is an input to stage U4 and never a substitute for it.

## E7 — VerificationExecution

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `execution_id` | string | yes | Runner label, native execution id, or `driver-u4`. |
| `kind` | enum | yes | `native`, `runner`, `driver-u4`. |
| `wp_id` | string | yes | Package being verified. |
| `started_at` / `ended_at` | integer | yes | Epoch seconds. |
| `fresh_context` | boolean | yes | True for native/runner; false for `driver-u4`. |

**Validation rules**

- **V-EXE.1**: A `driver-u4` execution is allowed only when the host cannot spawn a subagent; the fallback is recorded in the ledger verdict event.
- **V-EXE.2**: The execution id never equals the package executor's id.
- **V-EXE.3**: The verifier execution itself is not a package dispatch and does not consume the slot cap.
- **V-EXE.4**: The verifier's duration is excluded from package durations and from parallelism efficiency.

## E8 — StageDecompositionDecision

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `feature_decomposition` | enum | yes | `auto` or `off` from U0. |
| `stage_map` | object | yes | Per-stage `auto|on|off` values (defaults apply when absent). |
| `stage_attempt_override` | enum/null | no | `auto|on|off` for this attempt only. |
| `slot_cap_requested` | integer | no | From `decomposition_slot_cap`; default 2. |
| `slot_cap_ceiling` | integer | yes | `min(4, line remaining allowance)`. |
| `resolved_decision` | enum | yes | `decomposed`, `single-package`, `disabled`, `fallback`. |
| `reason` | string | yes | Why this decision was taken. |

**Validation rules**

- **V-DEC.1**: Feature-level `off` is a hard opt-out; no override can re-enable decomposition in the same run.
- **V-DEC.2**: Otherwise the stage-attempt override wins over the stage map, which wins over the built-in defaults.
- **V-DEC.3**: Built-in defaults: `plan`, `implement`, `review` = `auto`; `analyze`, `clarify` = `off`; `requirements`, `tasks`, `checklist` = `off`.
- **V-DEC.4**: `auto` resolves to `decomposed` only when the gate verdict is `admit`, at least two packages exist, and the benefit test (WG-13) holds; otherwise it resolves to `single-package` with `reason=not-beneficial`.
- **V-DEC.5**: `off` resolves to `disabled`; a gate rejection or unavailable layer resolves to `fallback` with a named cause.
- **V-DEC.6**: For a concurrently dispatchable set, every package declares an isolated port block, temporary directory, or cache directory, or a non-empty `shared_readonly`; otherwise the plan is rejected.

## E9 — StageTeamPreset

`skills/external/sdd-loop-driver/templates/stage-team-preset.md` (ST-01…ST-12).

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `preset_id` | string | yes | `sdd-stage-team`. |
| `name` | string | yes | Display name. |
| `pattern` | enum | yes | Default shape only; `parallel` in the shipped preset. |
| `summary` | string | yes | One line. |
| `when_to_use` | string | yes | Situation description. |
| `signals` | string[] | yes | Schema compatibility; the adapter does not run the catalog matcher. |
| `inputs` | object[] | yes | `stage`, `wp_graph`, `line`, optional `slot_cap`. |
| `members` | object[] | yes | Four seats: stage-planner, stage-worker, stage-verifier, stage-integrator. |
| `config` | object | yes | Pattern selection, slot cap, write isolation, verification, retry, persistence. |
| `provenance` | string | yes | Feature 070 clarify source and first-run evidence obligation. |

**Validation rules**

- **V-PRE.1**: Frontmatter carries every field required by `skills/internal/create-team/references/team-presets.md`.
- **V-PRE.2**: The body carries the six mandatory sections: `Goal Skeleton`, `Static Structure`, `Dynamic Structure`, `Instantiation`, `Constraints & Hard Rules`, `Known Pitfalls`.
- **V-PRE.3**: The preset is not placed in `skills/internal/create-team/templates/teams/` and is not registered in that catalog.
- **V-PRE.4**: The preset's `pattern` is a default only; the graph-derived pattern in the plan always wins.
- **V-PRE.5**: `continuous` never appears as a selected pattern or an adapter flow.
- **V-PRE.6**: The preset does not create a team directory, goal binding, or run report.

## E10 — SeatMapping

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `wp_id` | string | yes | Package id. |
| `role` | string | yes | `stage-worker` for package executors. |
| `stage` | enum | yes | `executor` for packages, `evaluator` for verifiers. |
| `type` | enum | yes | `Worker`. |
| `execution_form` | enum | yes | `native`, `detached-runner`, `integrator`. |
| `lifetime` | enum | yes | `one-package`, `one-verdict`, `one-stage-attempt`, `stage`. |

**Validation rules**

- **V-SEAT.1**: Each package maps to exactly one accountable seat.
- **V-SEAT.2**: The verifier seat is never filled by the package executor.
- **V-SEAT.3**: The planner/lead seat is the driver itself and never dispatches another coordinator.
- **V-SEAT.4**: The integrator seat is filled once per decomposed stage attempt.

## E11 — StageCoordinationReport

`<state-dir>/reports/<line>-<stage>-a<N>-coordination.md` and `.json` (OR-11, OR-12).

| Field | Type | Notes |
|-------|------|-------|
| `schema_version` | integer | `1`. |
| `line_id` / `run_id` / `stage` / `stage_attempt` | string/int | Identity. |
| `decision` / `pattern` / `slot_cap` | mixed | From the plan and ledger. |
| `dispatch_order` | string[] | Actual dispatch order. |
| `integration_order` | string[] | Declared integration order. |
| `wall_clock_seconds` | number or `not_evaluated` | D7.2 definition. |
| `critical_path_seconds` | number or `not_evaluated` | Duration-weighted longest path. |
| `parallelism_efficiency` | number or `not_evaluated` | `sum(durations) / (wall_clock × max_concurrent)`. |
| `max_concurrent` | integer or `not_evaluated` | Sweep result. |
| `retries_package` / `retries_stage` | integer or `not_evaluated` | Counts. |
| `stage_executions_per_canonical` | number or `not_evaluated` | `stage_attempts / canonical_stages`. |
| `manual_interventions` | integer or `not_evaluated` | Optional input. |
| `token_cost` | number or `not_evaluated` | Sum only when every dispatch has a value. |
| `verdicts` | object[] | Per package verdict and evidence path. |
| `evidence_refs` | string[] | Paths only; no raw transcripts. |

**Validation rules**

- **V-REP.1**: Every metric with a missing source is the literal string `not_evaluated`.
- **V-REP.2**: A parallel-execution claim requires at least two overlapping executor intervals; otherwise the report states `overlap=false` and the claim is invalid.
- **V-REP.3**: The report never contains raw transcript lines or full log bodies.
- **V-REP.4**: The Markdown and JSON reports carry the same values.
- **V-REP.5**: `stage-close` references both report files through `report_ptr`.
- **V-REP.6**: A report written for a stage without a plan fence reports `decision=not_evaluated` and does not invent a decomposition.

## E12 — StageCloseRecord

The `stage-close` ledger event (OR-03). Fields are fixed by E4 and D7.1.

**Validation rules**

- **V-CLOSE.1**: `stage_u4_at` is not earlier than the first `started_at`.
- **V-CLOSE.2**: `retries_stage = stage_attempt - 1` for the stage; `retries_package` is the count of `retry` events in the stage attempt.
- **V-CLOSE.3**: `stage_attempts` is the count of plan events for the stage in the run; `canonical_stages = 8`.
- **V-CLOSE.4**: A missing metric is `not_evaluated`; a stage-close is written once per successful stage attempt.

## E13 — RetryDelta and DecompositionRule

**RetryDelta** (part of E3; OR-15):

```json
{
  "changed": ["scope | budget | topology"],
  "reason": "one line",
  "scope": {"from_unit": "tasks", "from_count": 8, "to_unit": "tasks", "to_count": 4,
            "split_into": ["<wp_id>a", "<wp_id>b"]},
  "budget": {"from_max_turns": 120, "to_max_turns": 160, "evidence_ref": "<path>"},
  "topology": {"from": "parallel-native", "to": "serial-native"}
}
```

- **V-DELTA.1**: `changed` is a non-empty subset of `scope`, `budget`, `topology`; only the named keys are required.
- **V-DELTA.2**: A scope change strictly decreases `bounded_by.count`, or splits into child packages with distinct outputs.
- **V-DELTA.3**: A budget change strictly increases `max_turns` and carries a non-empty `evidence_ref` that resolves to dispatch-level evidence.
- **V-DELTA.4**: A topology change uses the closed value set `parallel-native`, `serial-native`, `detached-runner`, `split-serial-children` and the `to` value differs from `from`.

**DecompositionRule**:

| Rule id | Stage | Package derivation | Required-output inventory |
|---------|-------|--------------------|---------------------------|
| `decompose-plan-v1` | plan | design artifacts, research, registry update, verification | plan.md, research.md, data-model.md, contracts/ (≥1 file), quickstart.md, feature-ref.md, feature registry row, feature detail update |
| `decompose-implement-v1` | implement | task groups (≤8 tasks), verification | task-owned paths, verification.md, baseline/closure evidence |
| `decompose-review-v1` | review | review dimensions (read-only), finding repair (write, bounded iteration) | review.md, review evidence |
| `decompose-investigation-v1` | analyze, clarify | read-only investigation | findings report/evidence; for clarify the integrator performs the write-back |

- **V-RULE.1**: A rule is replayable: the same source artifacts and rule yield the same package set and ids.
- **V-RULE.2**: A rule's run-specific `required_outputs` must cover its inventory; an uncovered inventory item is `orphan-output`.
- **V-RULE.3**: A stage with no rule is single-subagent only and never produces a decomposed plan.

## State transitions

| Subject | From | To | Trigger |
|---------|------|----|---------|
| Stage decision | unresolved | `decomposed` | gate `admit` + benefit test |
| Stage decision | unresolved | `single-package` | `auto` without benefit, one package, or explicit stage `off` resolution |
| Stage decision | unresolved | `disabled` | feature-level `off` |
| Stage decision | unresolved | `fallback` | gate reject after one repair, exit 2, or unrepresentable contract |
| Package | planned | ready | every dependency has a `verdict=pass` |
| Package | ready | running | dispatched within the slot rule |
| Package | running | settled | `settle` event recorded |
| Package | settled | verified | independent `verdict=pass` |
| Package | settled | failed | `verdict=fail`, missing verdict, or malformed result |
| Package | failed | retried | attempt 1 failed and a valid delta is admitted |
| Package | failed twice | stage-failed | `wp_failed` recorded; U5 entered |
| Package | planned | superseded | split amendment; children replace it |
| Stage | verified | closed | integration + stage U4 pass + `stage-close` |

## Traceability

| Requirement group | Entities | Primary clauses |
|-------------------|----------|-----------------|
| FR-001…FR-005 | E1, E2, E3, E8, E12, E13 | WP-01…WP-18, WG-06…WG-13, FN-01…FN-08 |
| FR-006…FR-009 | E9, E10, E2 | ST-01…ST-12, WG-14…WG-16, SD-14 |
| FR-010…FR-015 | E1, E4, E7 | SD-01…SD-16, WP-09, WP-10 |
| FR-016…FR-019 | E5, E6, E7 | VI-01…VI-14 |
| FR-020…FR-023 | E4, E11, E12 | OR-01…OR-13 |
| FR-024…FR-027 | E8, E9, E12 | FN-01…FN-16, ST-03…ST-12 |
| FR-028…FR-030 | test fixtures and evidence files | FN-14…FN-16 |
