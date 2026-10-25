# Clarify Decisions — Feature 070

**Status**: normative decisions for the plan stage; created 2026-10-24 by the `clarify` stage.
**Authority**: `requirements.md` § Clarifications (Session 2026-10-24 — clarify) owns the decision record; this file owns the exact schemas, paths, interfaces, and checks those decisions fix. When a field name or path here changes, the change is a scope revision, not an implementation detail.
**Scope guard**: the 30-FR ceiling is unchanged. These decisions resolve ambiguities inside the existing FRs, Assumptions, and Clarifications; they add no FR. Anything that would have required a new requirement is either folded into an existing FR's declared behavior or explicitly deferred.

---

## D1. Stage-team preset

### D1.1 Location and status

- **Path**: `skills/external/sdd-loop-driver/templates/stage-team-preset.md` (new driver-owned asset; mirrored to `.specify/skills/sdd-loop-driver/templates/stage-team-preset.md` by the existing mirror flow at delivery time, never hand-edited).
- **Catalog status**: **not** registered in `create-team`'s preset catalog (`skills/internal/create-team/templates/teams/`). The driver adapter loads it by explicit path. `match-team-preset.py`, `create-team`, and `run-team` are not modified; no `preset:` reference is added to any persisted team.
- **Persistence**: no `.specify/teams/<slug>/team.md` is created per stage, per attempt, or per run. The adapter's output is a run-scoped plan written into the line state spine (D2); it has no team directory, goal binding, or run report of its own.
- **Contract compatibility**: field-level compatibility with `skills/internal/create-team/references/team-presets.md` (frontmatter fields and mandatory body sections). It is not a catalog preset, so the catalog's "distilled from a team that actually ran" admission rule does not apply; provenance records the source shape and the first-run evidence obligation instead.

### D1.2 Frontmatter schema

```yaml
---
preset_id: sdd-stage-team
name: SDD Stage Work-Package Team
pattern: parallel
summary: Run one SDD stage as bounded work packages coordinated by the driver, with independent verification and deterministic integration.
when_to_use: The driver reaches a stage that passes the Work Package decomposition gate and needs coordinated read-only parallelism with serialized writes.
signals:                       # schema compatibility only; the driver adapter does not run the catalog matcher
  - sdd stage work packages
  - subagent task decomposition
  - stage team preset
inputs:
  - name: stage
    required: true
    description: Canonical stage name (plan, implement, review; analyze/clarify only on explicit opt-in).
  - name: wp_graph
    required: true
    description: The admitted Work Package plan (packages, dependencies, pattern, slot cap).
  - name: line
    required: true
    description: Line label and state-spine path for the run.
  - name: slot_cap
    required: false
    description: Read-only concurrency cap; defaults to 2 and is capped by the line's remaining allowance.
members:
  - role: stage-planner
    stage: executor
    type: Worker
    lifecycle: persistent
    responsibility: Derive and own the stage Work Package plan and its acceptance boundaries (the driver itself).
  - role: stage-worker
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: Execute exactly one Work Package inside its owned paths, budget, and evidence contract.
  - role: stage-verifier
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: Independently verify settled Work Packages; never the executor of the package being verified.
  - role: stage-integrator
    stage: executor
    type: Worker
    lifecycle: temporary
    responsibility: Aggregate verified outputs in the declared order, make the single stage-closing commit, and emit the stage sentinel.
config:
  default_pattern: parallel
  pattern_selection: parallel only when every concurrently dispatchable package is read-only; serial when any package owns write paths or dependencies order the work; iteration only for a bounded repair loop with an explicit maximum; continuous excluded.
  slot_cap_default: 2
  slot_cap_ceiling: min(4, the line's remaining concurrency allowance owned by Feature 064)
  write_packages: dispatched alone (effective concurrency 1)
  verification: one fresh-context verifier execution per Work Package
  retry: at most one automatic retry per Work Package; the retry must change scope, budget, or topology
  persistence: run-scoped only; never .specify/teams/<slug>/team.md
provenance: Feature 070 clarify 2026-10-24; shape derived from the measured baseline in the 070 brief and the existing Role × Stage × Type vocabulary, not from a create-team catalog run. First-run provenance is attached to this file when the first decomposed stage closes (report path recorded in the spine).
---
```

### D1.3 Mandatory body sections

The body keeps every section the preset contract requires, with `Instantiation` repurposed for a run-scoped adapter:

- `## Goal Skeleton` — one stage, bounded packages, independent verification, deterministic integration, stage gate unchanged.
- `## Static Structure` — the Role × Stage × Type table above, with the seat-to-execution mapping in D1.4.
- `## Dynamic Structure` — the parallel, serial-with-read-only-layers, and bounded-iteration flows; `continuous` is excluded.
- `## Instantiation` — projection into a run-scoped plan: substitute stage, line, plan hash, slot cap, pattern, and package-to-seat mapping; explicitly **do not** create a team directory or persist a team definition.
- `## Constraints & Hard Rules` — driver sole coordinator; no nested driver; no stage-command change; stage sentinel plus U4 mandatory; write packages never concurrent; no second registry, ownership model, integration queue, or ledger.
- `## Known Pitfalls` — at minimum: treating a package sentinel as the stage sentinel; running a write package concurrently; verifying with the executor's own context; letting a same-budget retry repeat; letting the preset's default pattern override the graph-derived pattern.

### D1.4 Seat-to-execution mapping

| Preset seat | Filled by | Lifetime |
|---|---|---|
| `stage-planner` | The driver itself (decomposition, gate invocation, scheduling, spine writes). It never dispatches another coordinator. | stage |
| `stage-worker` | One subagent execution per Work Package: a fresh native subagent in local topology, or one detached `stage-runner.sh` execution in remote topology. | one package |
| `stage-verifier` | One fresh-context read-only subagent execution per Work Package; never the package executor. | one verdict |
| `stage-integrator` | One subagent execution per decomposed stage attempt, run after all packages verify; it aggregates, commits once, and emits the stage sentinel. | one stage attempt |

The preset's declared `pattern` is the default shape only. The **selected** pattern is always the graph-derived value recorded in the plan (D2); the preset never overrides the graph.

---

## D2. Work Package document

### D2.1 Canonical location

The Work Package plan and the package ledger are **fenced sections of the existing line state spine**. There is no spec-local plan file and no second ledger.

- Plan fence: `<!-- wp-plan:begin stage=<stage> stage_attempt=<n> -->` … `<!-- wp-plan:end -->`
- Amendment fence: `<!-- wp-plan-amendment:begin stage=<stage> stage_attempt=<n> seq=<n> -->` … `<!-- wp-plan-amendment:end -->`
- Ledger fence: `<!-- wp-ledger:begin -->` … `<!-- wp-ledger:end -->` (one JSON object per line, append-only)

The driver is the sole writer of these fences. Work Package executors never write the spine. In `SPINE_WRITE_MODE=transport`, stage executors keep writing their existing transport rows; the driver still writes the WP fences directly, because it owns coordination. Per-package result and verdict records are **evidence files**, not a ledger (D2.4).

Precedent for a machine-readable fence inside the spine: the Feature 063 E2 test-budget JSONL fence (`<!-- test-budget:begin -->` … `<!-- test-budget:end -->`).

### D2.2 Plan schema

```json
{
  "schema_version": 1,
  "line_id": "<line>",
  "run_id": "<run>",
  "stage": "plan | implement | review | analyze | clarify",
  "stage_attempt": 1,
  "decision": "decomposed | single-package | disabled | fallback",
  "reason": "<one line>",
  "rule": "decompose-plan-v1 | decompose-implement-v1 | decompose-review-v1 | decompose-investigation-v1 | null",
  "source_artifacts": ["<repo-relative path>"],
  "required_outputs": ["<named artifact or repo-relative path>"],
  "pattern": "parallel | serial | iteration",
  "tie_break": "wp_id-lexicographic",
  "slot_cap": 2,
  "repair_loop": {
    "max_iterations": 3,
    "stop_condition": "zero open blockers | no new findings",
    "findings_source": "<path or named artifact>"
  },
  "packages": [
    {
      "wp_id": "<stage>-wp<NN>",
      "stage": "<stage>",
      "objective": "<one bounded outcome>",
      "kind": "read-only | write",
      "source_refs": ["<artifact>#<section or task id>"],
      "inputs": ["<repo-relative path or named artifact>"],
      "outputs": ["<repo-relative path or named artifact>"],
      "intermediate_outputs": ["<repo-relative path or named artifact>"],
      "owned_paths": ["<repo-relative path>"],
      "read_only_paths": ["<repo-relative path>"],
      "depends_on": ["<wp_id>"],
      "parallel_safe": true,
      "max_turns": 120,
      "bounded_by": {"unit": "tasks | clauses | artifacts | acceptance", "count": 1},
      "acceptance": [
        {"id": "A1", "check": "<what is checked>", "evidence": "<command or evidence path>"}
      ],
      "sentinel": "WP-<STAGE-UPPER>-<WPID-UPPER>-DONE",
      "evidence": "<state-dir-relative evidence directory>",
      "seat": {"role": "stage-worker", "stage": "executor", "type": "Worker"},
      "resources": {
        "ports": "none | <start-end>",
        "tmp_dir": "none | <path>",
        "cache_dir": "none | <path>",
        "shared_readonly": ["<path>"]
      }
    }
  ],
  "plan_hash": "sha256:<hex over the canonical JSON of the fields above except plan_hash and all timestamps>"
}
```

Rules fixed by the schema:

- `wp_id` format `<stage>-wp<NN>`; IDs are assigned in deterministic plan order (topological layers, each layer sorted lexicographically by the source artifact reference), never by dispatch timing.
- `kind=read-only` requires empty `owned_paths`; `kind=write` requires non-empty `owned_paths`; `parallel_safe` may be true only for `kind=read-only`.
- `repair_loop` is present if and only if `pattern=iteration`; `max_iterations` is a positive integer and `stop_condition` is non-empty. `continuous` is never a valid value.
- `tie_break` has exactly one admitted value in the first slice: `wp_id-lexicographic`.
- `plan_hash` is the canonical-JSON hash of the plan body (sorted keys, UTF-8, no insignificant whitespace), excluding `plan_hash` and any timestamp. Same stage artifacts plus the same `rule` must yield the same hash on replay.

### D2.3 Amendments, retries, and stability

- The original plan fence is never edited. A retry that changes scope, budget, or topology appends an amendment fence with `seq`, `supersedes_plan_hash`, the changed package records, the new `plan_hash`, and a `retry_delta` (D6).
- A split retry keeps the parent record with its attempt history and marks it `superseded_by: ["<parent>-a", "<parent>-b"]`; the children are new packages with child IDs. Evidence from the failed attempt remains attributed to the parent.
- A stage-level U5 retry starts a new **stage attempt** with a fresh plan fence, a fresh plan hash, and a fresh per-WP attempt counter. Prior stage attempts remain in the spine.
- Package IDs never change within a stage attempt. Across stage attempts, deterministic derivation yields the same IDs for the same artifacts; a changed artifact set may legitimately change them, and the new plan hash records that.

### D2.4 Per-package evidence files

These are per-entry evidence files, not a ledger; each Work Package writes only its own paths:

- Result: `<state-dir>/wp/<line>-<stage>-<wp_id>.result.json` — `{wp_id, stage_attempt, status, outputs[], changed_paths[], tests{}, commits[], notes}`. A result is an input to verification, never proof of success.
- Verdict: `<state-dir>/wp/<line>-<stage>-<wp_id>.verdict.json` — D5.2.
- Gate evidence: `<state-dir>/wp/<line>-<stage>-a<stage_attempt>-gate-<check>.json` — D3.4.
- Report: `<state-dir>/reports/<line>-<stage>-a<stage_attempt>-coordination.{md,json}` — D7.4.

The WP brief passes absolute paths for these files. A read-only Work Package's "read-only" status means it does not modify repository-owned paths; writing its own evidence file under the state directory is permitted and is not an owned path.

### D2.5 Relation to the 067 part brief and dispatch log

For `implement`, the Work Package is the 067 part brief extended with the WP identity, dependency, ownership, parallel-safety, and evidence fields above. The ledger's `dispatch` event carries the 067 dispatch-log fields: `part_id` (= `wp_id`), `task_ids[]`, `turns`, `test_delta{passed, failed, new_failures[]}`, `commit`, `outcome`, `duration_seconds`, `token_cost`. There is one brief format and one ledger; unavailable 067 quantities are `not_evaluated`.

### D2.6 Stage-command opacity

Work Package executors do **not** invoke the stage command as a monolith. Each executes its bounded slice directly under the WP brief, using the stage's authority artifacts and templates as inputs. The integrator is responsible for assembling the stage deliverable in the stage's required format, and the unchanged stage-level U4 verifies the assembled artifact. No `/speckit.*` command internal is modified, and no WP prompt instructs loading any skill or the driver.

---

## D3. Decomposition gate interface

### D3.1 Script

`skills/external/sdd-loop-driver/scripts/wp-gate.py` (new; standard library only, Python ≥ 3.8). The name intentionally differs from `decomposition-check.py`, which owns the Feature-level FR/task slicing gate and is not changed.

### D3.2 Invocation

```text
wp-gate.py --spine <path> --stage <stage> --check plan|preflight|retry
          [--plan-json <path>] [--manifest <path>] [--repo <path>]
          [--slot-cap-ceiling <int>] [--wp-id <id> --wp-attempt <n>]
          [--json-out <path>]
```

- `--spine`: the line state spine holding the plan/amendment fences and the ledger. `--plan-json` is a fixture/testing alternative whose content must equal a plan body.
- `--manifest`: the Feature 064 Ownership Manifest JSON (the only ownership owner). Required by `--check preflight` when any package has `owned_paths`.
- `--slot-cap-ceiling`: the line's remaining concurrency allowance; default 4 (the Feature 064 line cap). The plan's `slot_cap` must be ≤ this value and ≥ 1.
- `--wp-id` / `--wp-attempt`: required by `--check retry`.

### D3.3 Checks and finding codes

`--check plan`:

| Code | Rejects when |
|---|---|
| `schema-missing` | a required field is absent, empty, or of the wrong type |
| `dup-wp-id` | two packages share a `wp_id` |
| `cycle` | `depends_on` is not acyclic |
| `dangling-dep` | `depends_on` names an unknown package |
| `orphan-output` | a required output is owned by zero packages, or a non-intermediate output is not a required output, or an intermediate output is not consumed by a dependent |
| `duplicate-output` | two packages claim the same required output |
| `unbounded` | `bounded_by.count` is not positive; `tasks` > 8; `clauses` > 40 |
| `pattern-mismatch` | `parallel` with a write package; `serial`/`parallel` without the graph compatibility FR-007 requires; `iteration` without `repair_loop` or with `continuous`; a write package marked `parallel_safe` |
| `kind-mismatch` | `kind` disagrees with `owned_paths`, or `parallel_safe` is true for a write package |
| `plan-hash-mismatch` | the recorded `plan_hash` does not equal the recomputed canonical hash |

`--check preflight` (adds to the plan checks):

| Code | Rejects when |
|---|---|
| `manifest-uncovered` | an `owned_path` is not covered by the line's Ownership Manifest `owned_paths` |
| `manifest-forbidden` | an `owned_path` or `read_only_path` hits the manifest's `forbidden_paths` |
| `path-overlap` | two concurrently dispatchable packages have overlapping write/read territories |
| `read-write-unordered` | a write package and any package reading its `owned_paths` are not ordered by the DAG |
| `write-write-unordered` | two write packages with overlapping `owned_paths` are not ordered by the DAG |
| `slot-cap-exceeded` | `slot_cap` > the ceiling or < 1 |
| `isolation-missing` | a package lacks a complete `resources` object, or a concurrently dispatched package declares no isolated resource and no `shared_readonly` |

`--check retry`:

| Code | Rejects when |
|---|---|
| `retry-unchanged` | attempt 2 carries no material change on scope, budget, or topology, or is an identical same-budget rerun |
| `retry-exhausted` | the package already has two attempts; escalation to the stage gate/U5 is required |
| `retry-delta-invalid` | the delta is malformed, the budget change has no dispatch-level evidence pointer, the scope change is not smaller, or the topology change is not a real dispatch-form change |

### D3.4 Verdict and exit codes

- JSON stdout (and optional `--json-out`):
  ```json
  {"schema_version": 1, "check": "plan|preflight|retry", "stage": "<stage>",
   "verdict": "admit|single-package|reject", "findings": [{"code": "...", "wp_id": "...", "detail": "..."}],
   "plan_hash": "sha256:...", "checked_at": "<ISO-8601>", "evidence_ptr": "<path>"}
  ```
- Exit codes: `0` = `admit` or `single-package`; `1` = `reject`; `2` = input/parse/IO error (treated as decomposition-unavailable, not as a plan rejection).
- The driver appends the verdict to the ledger's `plan` event: `{verdict, gate_evidence, plan_hash, at}`. The plan fence itself is not edited. The plan fence and the `plan` ledger event (including the gate verdict) are both written **before the first package dispatch**, satisfying the stage-decomposition-record requirement.
- A `reject` blocks dispatch. The driver may make **one** repair attempt (split, serialize, or reduce to one package), recorded as an amendment; a second `reject` falls back to `single-package` with `decision=fallback` and the finding list as the reason.
- Exit `2` falls back to `single-package` with `decision=fallback` and `reason=decomposition-unavailable`; it never runs a partial package set.

---

## D4. Scheduler and dispatch execution

### D4.1 Scheduling rule

- Ready set: packages whose `depends_on` packages are all `verified=pass`.
- Pattern semantics: the stage pattern follows FR-007 (`serial` when any package owns write paths or dependencies order the work; `parallel` only when every concurrently dispatchable package is read-only; `iteration` only for a bounded repair loop). A `serial`-pattern stage may still run independent ready read-only packages concurrently — the pattern names the dominant discipline ("serial chain with parallel read-only layers"), and FR-011's read-only concurrency applies.
- Read-only concurrency: up to `slot_cap` read-only packages may run at once. Slot cap default 2; override `decomposition_slot_cap`; ceiling `min(4, line remaining allowance)`.
- Write packages: dispatched **alone**. Before launching one write package, the scheduler waits for every running package to settle. A write package's effective concurrency is 1.
- Dispatch order: topological layers; within a layer, `wp_id` lexicographic (the declared tie-break). The ledger records the actual `dispatch_order` counter separately.
- Integration order: the same topological layers, each layer sorted by `wp_id` lexicographic; not dispatch order.

### D4.2 Local topology

- The driver dispatches one **native host subagent** per Work Package; it MUST NOT launch `qodercli` or another external CLI locally.
- Independent read-only packages are dispatched as parallel native calls when the host supports them; otherwise the driver records `parallel_requested=yes`, `effective=serial`, `reason=host-no-parallel-native` and dispatches them serially. The effective concurrency is recorded in the ledger.
- The native call is synchronous; its return is the package's terminal event for dispatching purposes. The driver records `started_at` before the call and `ended_at` on return.
- No runner, pid file, FIFO, or watcher is used for a native call.

### D4.3 Remote topology

- One `stage-runner.sh` process per Work Package, with a unique label `--stage <stage>-<wp_id>` (so pid/status/log/heartbeat/raw names never collide) and `--sentinel WP-<STAGE-UPPER>-<WPID-UPPER>-DONE`.
- Each WP runner is detached (`--detached yes`) and watched with the existing watcher (`watch-target.sh`) against its own pid/status/log/heartbeat; one watcher invocation per running WP, or a batched manifest form only if it preserves per-package verdicts. Verdicts remain per package.
- The driver enforces the slot cap before each launch. A write package waits until every running WP is terminal.
- Result collection: the runner's terminal status (`exit`, `sentinel`) plus the log's last non-empty line must agree on the WP sentinel; then the driver reads the package result file (D2.4) and dispatches the verifier. `INCOMPLETE`, a missing result file, a missing sentinel, or an `ANOMALY` line means the package did not complete and is not verified.

### D4.4 Failure isolation and aggregation

- A failed, stalled, or budget-exhausted package never cancels unrelated running packages. Its dependents remain blocked; other ready independent packages continue.
- After every dispatchable package settles, if any package is failed or unverified, the stage gate fails (after the retry path, D6); integration does not start.
- Aggregation never infers success from a package self-report. It checks the verified verdict set, output existence, output coverage, and contradictions before integration.

### D4.5 Integrator and stage sentinel

- For `decision=decomposed` stages, after all packages verify, the driver dispatches **one integrator execution** for the stage attempt (the preset's `stage-integrator` seat). It receives the verified outputs, the plan, and the stage authority artifacts; it aggregates in the D4.1 integration order, detects missing or contradictory outputs, makes the single stage-closing commit, and emits the stage sentinel (`<STAGE>-DONE`) as its last non-empty line.
- The integrator never dispatches another package, never re-plans the stage, and never loads the driver.
- For `decision=single-package`/`disabled`/`fallback`, the standard stage executor emits the stage sentinel; no integrator execution is added.
- Work Package executors never emit the stage sentinel. A package sentinel (`WP-…-DONE`) is never promoted to a stage sentinel.
- The driver runs the unchanged stage-level U4 after integration: sentinel + artifact verification + discipline checks.

### D4.6 Stage commits

- For stages without a part-commit discipline (plan, review, analyze, clarify), Work Package executors do not commit; the integrator makes the single stage-closing commit after integration.
- For `implement`, the 067 part-commit discipline is preserved: parts may commit their own bounded changes. The integrator's single stage-closing commit covers the remaining integrated deliverable and MUST NOT rewrite or squash prior part commits. The stage still closes once, after integration.
- An integration conflict or missing output stops integration; no partial set is reported or committed as a complete stage deliverable.

---

## D5. Independent verifier

### D5.1 Who verifies

- Exactly one **fresh-context verifier execution per Work Package**, dispatched by the driver after the package settles. It is a different subagent execution from the package executor and fills the preset's `stage-verifier` seat.
- Local topology: a native host subagent with a verifier brief. Remote topology: one `stage-runner.sh` invocation labeled `<stage>-<wp_id>-verify` with sentinel `WP-<STAGE-UPPER>-<WPID-UPPER>-VERIFIED`.
- The verifier is read-only with respect to repository content. It may run the acceptance checks declared by the package, including targeted tests selected by the existing `targeted-set-v1` procedure; it MUST NOT run a full suite (the two-slot test budget is unchanged).
- The driver, not the verifier, remains the U4 authority for the stage.

### D5.2 Verdict record

`<state-dir>/wp/<line>-<stage>-<wp_id>.verdict.json`:

```json
{
  "schema_version": 1,
  "wp_id": "<id>",
  "stage": "<stage>",
  "stage_attempt": 1,
  "verdict": "pass | fail",
  "checks": [{"id": "A1", "kind": "artifact|contract|test|adversarial|ownership", "command": "<command or null>", "result": "pass|fail", "evidence_ref": "<path>"}],
  "evidence_refs": ["<path>"],
  "execution_id": "<runner label or native execution id>",
  "verified_at": "<ISO-8601>"
}
```

- The driver appends a `verdict` ledger event: `{wp_id, verdict, verifier_execution, evidence_ptr, at}`.
- A missing, malformed, or ambiguous verdict file counts as `fail`; success is never inferred.
- A package verdict is an input to the stage U4 and never a substitute for it.

### D5.3 Dependent unlocking

- The scheduler unlocks a dependent only when every `depends_on` package has a ledger `verdict=pass` with an evidence pointer.
- A failed package keeps its dependents `blocked`; it does not unlock them and does not silently drop them.
- If a package fails after its one retry, the stage gate fails and the existing U5 stage-retry path is entered.

---

## D6. Retry enforcement

### D6.1 Counter location and scoping

- The per-WP retry counter is **derived from the spine ledger** by counting `dispatch` events for `(stage, stage_attempt, wp_id)`. There is no separate counter file.
- `wp_attempt` starts at 1 for each package in each stage attempt, and at most one automatic retry is allowed (attempt 2). A stage-level U5 retry starts a new `stage_attempt` with a fresh `wp_attempt` counter; all earlier records remain in the spine.

### D6.2 Delta schema

An amendment that retries a package carries:

```json
"retry_delta": {
  "changed": ["scope | budget | topology"],
  "reason": "<one line>",
  "scope": {"from_unit": "tasks", "from_count": 8, "to_unit": "tasks", "to_count": 4, "split_into": ["<wp_id>a", "<wp_id>b"]},
  "budget": {"from_max_turns": 120, "to_max_turns": 160, "evidence_ref": "<path>"},
  "topology": {"from": "parallel-native", "to": "serial-native"}
}
```

Only the keys named in `changed` are required; at least one is required.

### D6.3 Mechanical checks (wp-gate `--check retry`)

- `scope`: the total `bounded_by.count` must strictly decrease, or the package must split into child packages with distinct outputs.
- `budget`: the new `max_turns` must be strictly greater than the prior attempt's, and `evidence_ref` must point to dispatch-level evidence (turn count, budget exhaustion record, or output-token evidence).
- `topology`: the dispatch form must materially change (for example, read-only concurrency reduced to 1, a native package moved to a detached runner for isolation, or a split into serial children).
- An attempt 2 whose scope, budget, and topology are identical to attempt 1 is rejected as `retry-unchanged` even if re-worded.
- Attempt 3 is rejected as `retry-exhausted`; the stage gate fails and the existing U5 path applies (default two stage retries). WP retries do not consume the stage retry budget before that escalation.

### D6.4 Escalation

- A package failing twice fails the stage gate; the driver records `wp_failed`, the attempt history, the verdict evidence, and enters U5.
- The U5 stage retry re-dispatches the stage with a new plan/stage attempt; it does not silently reuse the failed package set.

---

## D7. Metrics and report

### D7.1 Spine fields (ledger events)

Each ledger line is one JSON object. The event types and their required fields:

| `event` | Required fields |
|---|---|
| `plan` | `stage`, `stage_attempt`, `plan_hash`, `decision`, `pattern`, `slot_cap`, `verdict`, `gate_evidence`, `at` |
| `dispatch` | `wp_id`, `stage_attempt`, `wp_attempt`, `dispatch_order`, `started_at`, `effective_concurrency`, `attempt_id`; for `implement` also the 067 fields: `task_ids[]`, `turns`, `test_delta`, `commit`, `outcome`, `duration_seconds`, `token_cost` |
| `settle` | `wp_id`, `ended_at`, `runner_status`, `result_ptr`, `outputs[]` |
| `verdict` | `wp_id`, `verdict`, `verifier_execution`, `evidence_ptr`, `at` |
| `retry` | `wp_id`, `wp_attempt`, `retry_delta`, `gate_evidence`, `at` |
| `integrate` | `stage_attempt`, `order[]`, `at`, `conflict`, `commit` |
| `stage-close` | `stage_attempt`, `stage_u4_at`, `wall_clock_seconds`, `critical_path_seconds`, `parallelism_efficiency`, `retries_package`, `retries_stage`, `stage_attempts`, `canonical_stages`, `stage_executions_per_canonical`, `manual_interventions`, `token_cost`, `report_ptr` |

All timestamps used for arithmetic (`started_at`, `ended_at`, `stage_u4_at`, `at`) are epoch seconds. `verified_at` and `checked_at` are ISO-8601. A dispatch event's `attempt_id` is `<wp_id>-a<stage_attempt>-w<wp_attempt>` so every attempt is uniquely addressable in evidence.

### D7.2 Metric definitions (FR-022, fixed)

- **Stage wall-clock**: first package dispatch to stage U4 completion (`stage_u4_at - first started_at`).
- **Critical path**: the duration-weighted longest path through the package graph, using each package's `ended_at - started_at`.
- **Parallelism efficiency**: `sum(package durations) / (wall_clock × max concurrent package count)`. This is the formula with the product in the denominator; it is not `(sum / wall_clock) × max`.
- **Stage executions per canonical stage**: stage dispatch attempts divided by the canonical stage count (the canonical chain is 8 in this driver).
- **Retry counts**: package retries and stage retries recorded separately.
- **Manual interventions**: user continue/retry/status messages per run, from the run record; `not_evaluated` when unavailable.

### D7.3 `not_evaluated`

Every metric with a missing source record is written as the literal string `not_evaluated` in the spine and the report. It is never written as `0`, an estimate, or another stage's value. A success criterion whose metric is `not_evaluated` is not claimed as met.

### D7.4 Report and digest

`skills/external/sdd-loop-driver/scripts/wp-report.py` (new, standard library only) derives both files from the spine:

```text
wp-report.py --spine <path> --stage <stage> [--stage-attempt <n>] --out-dir <state-dir>/reports
```

- `<state-dir>/reports/<line>-<stage>-a<stage_attempt>-coordination.md` — human digest: decomposition decision, pattern, slot cap, dispatch order, critical path, wall-clock, parallelism efficiency, retries, verdicts, evidence paths (no raw transcripts).
- `<state-dir>/reports/<line>-<stage>-a<stage_attempt>-coordination.json` — the same fields machine-readably.
- `stage-close` in the spine carries `report_ptr` to both.
- If `wp-report.py` cannot read a field, it writes `not_evaluated`; it never fabricates a number.

### D7.5 Benchmark method

1. **Comparable feature**: full chain (checklist/analyze/review, no fast lane), 8–30 FR definitions and 10–40 task rows, same host class and topology as the baseline record (or a re-measured baseline on the current host).
2. **Samples**: at least three comparable stage samples per measured stage (for example, three runs of `plan` and three runs of `review`). Fewer than three → `not_evaluated`, never a median claim.
3. **Computation**: stage wall-clock per sample from the spine epochs; median across samples; compare with the baseline anchor.
4. **Baseline anchor**: the upper bound of the 2026-10-24 dated range is the conservative anchor — `plan` 70 minutes, `review` 37 minutes. A 20% reduction therefore means `plan` ≤ 56 minutes and `review` ≤ 29.6 minutes. If a later stage re-measures the baseline, its dated median replaces this anchor; sources are never mixed.
5. **Gate regression**: the name-level failure set from the canonical runner (`--names-out`) against the run's baseline; zero new failures.
6. **Record**: the benchmark result is a dated record in the feature's `test-evidence/` (for example, `benchmark-<date>.md`), with the reports' paths and the baseline anchor used. Token/run cost comes from the existing exec-quant record when available; otherwise `not_evaluated`.

---

## D8. Opt-out and defaults

### D8.1 Declaration fields

U0 entry declaration (the run's per-feature configuration):

```text
decomposition: auto|off
decomposition_stages: plan=auto, implement=auto, review=auto, analyze=off, clarify=off, requirements=off, tasks=off, checklist=off
decomposition_slot_cap: 2
```

Stage-attempt declaration (written to the spine before the stage's first dispatch):

```text
decomposition_decision: decomposed|single-package|disabled|fallback
decomposition_override: auto|on|off      # optional, this stage attempt only
```

### D8.2 Precedence

1. `decomposition: off` at the feature/run level is a **hard opt-out**: no stage override can re-enable it; a new entry declaration is required.
2. Otherwise, the stage-attempt `decomposition_override` wins over the per-stage map; the per-stage map wins over the built-in defaults.
3. Built-in defaults: `plan`, `implement`, `review` = `auto`; `analyze`, `clarify` = `off` (an explicit `on` is required); `requirements`, `tasks`, `checklist` = `off`.
4. `auto` admits decomposition only when the gate returns `admit` with at least two packages and a beneficial decomposition; otherwise `single-package` with the reason recorded.
5. `off`, `disabled`, `single-package`, and `fallback` all run the standard single-subagent stage path with the unchanged stage prompt, runner/native dispatch, sentinel, and U4. No new argument, field, or service is required for that path; a run with no entry declaration gets the built-in defaults.

### D8.3 Recorded decision

Every stage records one of `decomposed`, `single-package`, `disabled`, or `fallback` with a reason and, where applicable, the gate evidence. A silent partial package set is never allowed; `fallback` always names its cause (`gate-reject`, `decomposition-unavailable`, or `not-beneficial`).

---

## D9. Overlap adjudication

### D9.1 Deterministic check output

Command:

```text
python3 /home/agent/sdd-070/tools/overlap-check.py --spec-dir .specify/specs/070-subagent-task-teams --repo .
```

Recorded result: `decision=clear`, `overlaps=0`, `checked_specs=["070-subagent-task-teams"]`, exit 0, note `current feature has no declaration artifact` (no `feature-ref.md` exists before the plan stage). The raw JSON is stored in `test-evidence/overlap-clarify.txt`.

### D9.2 Manual adjudication against 064 / 067 / 068

The deterministic check cannot compare a declaration that does not exist yet, so the delivery surface is adjudicated from the actual git history of the sibling features:

| Sibling | Actual shared delivery surface | Relationship to 070 | Adjudication |
|---|---|---|---|
| 064 | `skills/external/sdd-loop-driver/` (SKILL.md, references, scripts), `docs/reference/skills/sdd-loop-driver.md`, `shared/definitions/probe-definitions.md` | 070 is an additive evolution of the same driver skill; 064 is merged and closed | 070 reuses 064's line registry, Ownership Manifest, worktree, and integration queue as read-only owners. 070 does not create a second registry, ownership model, or integration queue. Same-skill edits are sequential features, not a live conflict. |
| 067 | `tests/contract/`, `tests/unit/`, spec/test-evidence; no driver-source changes | 070 extends the 067 part brief and adds driver tests | One brief format, one dispatch log, one ledger. 070 adds WP identity/dependency/ownership fields to the same record; it does not create a competing brief or ledger. |
| 068 | `scripts/python/exec-quant.py`, `scripts/python/feedback-utils.py`, `shared/workflow/feedback-step.md`, feedback docs/skills | No delivery-path overlap | 068's channel is preserved; 070 adds no transmission surface and no runtime record type. |

No overlap requires an ownership transfer. The plan stage MUST re-run the overlap check after `feature-ref.md` declares 070's delivery surface and confirm `clear` before implementation; the clarify gate is satisfied by the recorded `clear` plus this adjudication.

### D9.3 Non-duplication statement

Feature 070 creates **no** second line registry, ownership model, integration queue, or ledger:

- **Registry**: Feature 064's line registry remains the only registry. The WP plan is a stage-local plan, not a registry.
- **Ownership**: Feature 064's Ownership Manifest remains the only ownership owner. A WP's `owned_paths` / `read_only_paths` are a finer projection inside one line's manifest, and `wp-gate --check preflight` reads the manifest; it never writes a second one.
- **Integration queue**: Feature 064's line integration queue (`integration-plan` / `integrate-lines.py`) remains the only line-level queue. WP integration is intra-stage deterministic aggregation, not a queue of lines.
- **Ledger**: the line state spine remains the only ledger. The WP ledger is an append-only fence inside the spine; per-WP result/verdict files are evidence entries, and the 067 dispatch log is extended, not duplicated.

---

## Clarify taxonomy coverage summary

| Category | Status | Resolution |
|---|---|---|
| Feature linkage | Clear | Feature 070 bound and registered in the requirements stage; deviation recorded (A7). |
| Functional scope & behavior | Resolved | D1–D8 fix the decomposition, coordination, verification, retry, metrics, and opt-out behavior. |
| Domain & data model | Resolved | D2 fixes the WP plan/ledger schema, IDs, hash, amendments, and evidence files. |
| Interaction & UX flow | Clear | Unattended driver flow; no user-facing interaction is added. |
| Non-functional quality attributes | Resolved | D7 fixes metric definitions, baseline anchor, and `not_evaluated`; FR-025 preserves the existing safety gates. |
| Integration & external dependencies | Resolved | D3/D4/D9 reuse the 064 manifest/registry and the 067 brief; no external dependency or service is added. |
| Edge cases & failure handling | Resolved | Retry splits, stage-attempt reset, missing verdict = fail, write-alone scheduling, gate reject/fallback. |
| Constraints & tradeoffs | Clear | Read-only-only concurrency, no parallel writes, no persisted team, no stage-command change. |
| Terminology & consistency | Resolved | Team vocabulary: Role × Stage × Type, parallel/serial/iteration; `continuous` excluded. |
| Completion signals | Clear | SC-001…SC-008 remain the measurable outcomes; D7.5 fixes the benchmark method. |
| Misc / placeholders | Clear | No active `[NEEDS CLARIFICATION]` marker; no unresolved placeholder. |
| Deferred-by-assumption | Resolved | A1–A12 re-read; no entry still names a later decision-maker after D1–D8. |

**Deferred 070b items**: none. These decisions fit inside the existing 30 FRs; the 070a/070b split remains contingent on later growth only. Parallel write packages remain out of scope, not deferred to 070b (they require a Feature 064 extension).
