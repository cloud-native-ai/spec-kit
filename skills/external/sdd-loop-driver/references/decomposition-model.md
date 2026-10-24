# Decomposition Model — Runtime Owner (Parts 1–3)

**Feature**: 070 — Task Decomposition & Team Coordination for Subagent-Driven SDD
**Status**: runtime-owner projection, parts 1–3: the Work Package model, the scheduler/retry procedure, and independent verification/integration. The preset-adapter (T025) and observability (T029) sections land with their owning task rows; this file does not pre-empt them.

**Design authority**: the seven contracts under `.specify/specs/070-subagent-task-teams/contracts/` and `.specify/specs/070-subagent-task-teams/data-model.md`. This document owns *how the driver applies* those clauses at runtime. Where a field name, check code, path pattern, or event field is fixed, the contract clause is authoritative; this file points to it instead of restating its table.

**Scope guard**: one Work Package record, one plan fence, one ledger fence inside the existing line state spine, one brief format. No second brief, ledger, registry, ownership model, integration queue, or persisted team is introduced. Stage-command internals, stage sentinels, U4, and the two-slot test budget are unchanged.

---

## 1. Work Package record

A Work Package is the bounded, independently verifiable unit of stage work defined by `contracts/work-package-model.md` WP-01 and `data-model.md` E1. The contract owns the required field set; the driver reads the same record shape for every decomposed stage.

The runtime rule is strict: a package missing any required field is never dispatched. The gate reports the missing field as `schema-missing` before any graph or dispatch decision (WG-06), and schema failures suppress the checks that would need an incomplete record.

Two invariants decide whether a package may exist at all (WP-02):

- `kind=read-only` requires an empty `owned_paths`; `kind=write` requires a non-empty `owned_paths`.
- `parallel_safe=true` is legal only for a read-only package. A write package is always dispatched alone, so it never declares parallel safety.

Ownership and read access are projections inside the line's existing Ownership Manifest (Feature 064). They never create a second ownership model.

### Identity and sentinels (WP-03)

A planned package id is `<stage>-wp<NN>`, assigned by the rule in section 2. A split child id is `<parent>-a`, `<parent>-b`, and so on. The package sentinel is `WP-<WP_ID_UPPER>-DONE`, which renders the stage-plus-package sentinel without duplicating the stage segment; for example `plan-wp03` renders `WP-PLAN-WP03-DONE`, and a child keeps its suffix (`WP-PLAN-WP03-A-DONE`). A package sentinel is never promoted to a stage sentinel.

## 2. ID assignment, layers, and tie-break (WP-04)

The driver assigns ids deterministically from the stage artifacts, not from dispatch timing:

1. Assign each candidate package a provisional key derived from its primary `source_refs` and its position in the declared candidate set.
2. Build the dependency DAG on those provisional keys.
3. Compute topological layers: a root is layer 0; every other package is one layer deeper than its deepest dependency.
4. Sort each layer by provisional key **lexicographic**.
5. Assign `wp_id` sequence numbers `01..NN` in layer order.
6. Rewrite `depends_on` from provisional keys to the assigned `wp_id`s.

The same source artifacts plus the same rule MUST yield the same ids and the same layers on replay. A changed artifact set may legitimately change them, and the new plan hash records that fact (WP-16).

The gate emits the resulting `dispatch_layers` (a list of layers, each sorted by `wp_id` lexicographic) and `integration_order` (the same layers flattened) in its JSON envelope. Dispatch order is recorded separately in the ledger as an actual counter; integration order is the declared deterministic order and never the dispatch order.

## 3. Fences and spine write authority

The plan, amendments, and ledger are fenced sections of the existing **line state spine**. There is no spec-local plan file, no second JSONL stream, no mutable aggregate index, and **no second ledger** (WP-14).

```text
<!-- wp-plan:begin stage=<stage> stage_attempt=<n> -->
...one UTF-8 JSON object...
<!-- wp-plan:end -->

<!-- wp-plan-amendment:begin stage=<stage> stage_attempt=<n> seq=<n> -->
...one UTF-8 JSON object...
<!-- wp-plan-amendment:end -->

<!-- wp-ledger:begin -->
...one complete JSON object per line...
<!-- wp-ledger:end -->
```

The driver is the sole writer of these fences (WP-05, WP-18). Package executors **never write** a fence. Stage executors keep writing their existing transport rows while `SPINE_WRITE_MODE=transport`; the WP fences are written by the driver because coordination is driver-owned. Re-entry reads the spine and never reconstructs a plan from session memory.

The original plan fence is never edited. A correction or retry is a separate amendment fence with a strictly increasing `seq`, a `supersedes_plan_hash`, the changed package records, and the new effective `plan_hash` (WP-07). Amendments apply in `seq` order; the latest effective hash wins.

## 4. Canonical plan hash and replay (WP-06, WP-16)

`plan_hash` is the `sha256:<hex>` digest of the canonical JSON of the effective plan: sorted keys, UTF-8, separators `,` and `:`, `ensure_ascii=false`. The digest removes `plan_hash`, `slot_cap_requested`, `slot_cap_ceiling`, and every timestamp key (`at` and any key ending in `_at`). The exclusion list is owned by WP-06 and `data-model.md` V-PLAN.7.

Before the first dispatch the driver records the applied rule, `source_artifacts`, the package list, the dependency edges, the selected pattern, the slot cap, the gate verdict, and the plan hash. This record is what makes the decomposition **replay**-able: replaying the same artifacts with the same rule must reproduce the package set, the layers, and the hash. A recorded hash that differs from the recomputed one is `plan-hash-mismatch` (WG-12).

## 5. Amendments, retries, and split children (WP-07, WP-08)

An amendment may replace existing package records, add split children, and carry an addressable retry block (`wp_id`, `wp_attempt`, `retry_delta`). The retry counter is derived from the ledger, never from a separate counter file (see section 10 and OR-14).

A split retry keeps the parent record with its attempt history and sets `superseded_by` to the child ids. The children receive distinct ids and distinct outputs, and every dependent's `depends_on` is rewritten from the parent to all children. The children **inherit** the parent's attempt count: their sole dispatch is the lineage's retry attempt, **split depth is one** (a child is never split again), and a child failure fails the stage gate without a further automatic retry. A superseded parent is never dispatched again; its evidence remains attributed to the parent.

## 6. Attempt-scoped evidence files (WP-11, OR-02)

Per-package evidence lives outside the spine, one file per entry, under the line state directory:

- `<state-dir>/wp/<line>-<stage>-<wp_id>-a<N>w<M>.result.json` — the executor's result.
- `<state-dir>/wp/<line>-<stage>-<wp_id>-a<N>w<M>.verdict.json` — the independent verifier's verdict.
- `<state-dir>/wp/<line>-<stage>-a<N>-gate-<check>.json` — the gate's evidence record.
- `<state-dir>/reports/<line>-<stage>-a<N>-coordination.{md,json}` — the stage coordination report.

These are per-entry evidence files, not a ledger. A read-only package may write only its own evidence path under the state directory; that write is not a repository-owned path.

Every dispatch is addressable as `attempt_id = <wp_id>-a<stage_attempt>-w<wp_attempt>` (OR-02), and its result and verdict files carry the same identity. Attempt-scoped names make a retry's evidence distinguishable from the attempt it replaced.

## 7. Implement: projection of the 067 part brief (WP-12)

For `implement`, the Work Package **is** the Feature **067** part brief extended with WP identity, dependency, ownership, parallel-safety, and evidence fields. There is one brief format and one dispatch log.

The ledger `dispatch` event for an implement package carries the 067 fields in addition to the WP fields: `part_id` (equal to `wp_id`), `task_ids[]`, `turns`, `test_delta{passed, failed, new_failures[]}`, `commit`, `outcome`, `duration_seconds`, and `token_cost`. An unavailable 067 quantity is the literal `not_evaluated`, never a fabricated number. Feature 067's part-commit discipline is preserved; the WP layer does not squash or rewrite part commits.

## 8. Decomposition rules and required-output coverage (WP-15)

Four replayable rules are declared, one per stage family:

| Rule | Stages | Package derivation |
|------|--------|--------------------|
| `decompose-plan-v1` | plan | design artifacts, research, registry update, verification |
| `decompose-implement-v1` | implement | task groups under the existing part-size ceiling, verification |
| `decompose-review-v1` | review | read-only review dimensions and a bounded finding-repair package |
| `decompose-investigation-v1` | analyze, clarify | read-only investigation |

The **required-output inventory** for each rule is owned by `data-model.md` **E13**; this file does not restate it. The plan's run-specific `required_outputs` must cover that inventory minus the integrator-owned outputs, and WG-08 rejects any orphan or duplicate claim. A required inventory item that cannot be represented by a package (or the integrator seat) forces the single-package fallback.

Package executors do not invoke the stage command as a monolith. Each executes its bounded slice from the stage authority artifacts and templates. The integrator assembles the stage deliverable and owns `integrator_outputs` (at minimum clarify's clarification write-back). The unchanged stage U4 still verifies the assembled deliverable.

The **mirror obligations** for the driver source files are owned by `plan.md` § **Mirror Obligations**; this file does not restate that table. The generated mirror under `.specify/skills/` is never hand-edited.

## 9. Single-package representation (WP-13)

A non-decomposed stage still records a decision. The plan fence carries `decision` in `single-package|disabled|fallback` and the gate verdict projected by FN-08, with exactly one package:

- id `<stage>-wp01`;
- `kind=write` unless the stage itself is read-only;
- `parallel_safe=false`;
- `bounded_by={"unit":"acceptance","count":1}`;
- sentinel `<STAGE>-DONE` (the stage sentinel, not a promoted package sentinel);
- `integrator_outputs=[]`;
- `slot_cap=1`.

The plan fence is the canonical decision record; the ledger `plan` event references it by `plan_hash`. The sole package is the stage execution itself: the standard single-subagent stage path (unchanged prompt, runner/native dispatch, sentinel, and U4) with the same acceptance evidence. For `implement`, the existing 067 part discipline remains in force.

## 10. Ledger (WP-09, WP-10, OR-01)

The ledger is the single append-only `wp-ledger` fence in the same spine. The closed event set is owned by WP-09, and the per-event required field sets are owned by `data-model.md` **E4** and OR-01; this file does not restate them.

Runtime rules:

- The driver appends one complete JSON object per line and never rewrites or truncates a line.
- A `plan` event (with the gate verdict and evidence pointer) is written before the first package dispatch and references the plan fence by `plan_hash`.
- A post-repair `plan` event appends `supersedes_plan_hash` without creating a new stage attempt; it never increments the stage-attempt numerator.
- A package that fails twice, or a split child that fails at all, appends `wp_failed` before the stage enters U5.
- Every unavailable quantity is the literal `not_evaluated`, never zero, an estimate, or another stage's value.
- No other run ledger may be created.

## 11. Timestamp units (WP-17)

Ledger arithmetic timestamps (`started_at`, `ended_at`, `at`, `stage_u4_at`) are **epoch seconds**. Evidence timestamps (`verified_at`, `checked_at`) are **ISO-8601**. Mixed units are invalid. Wall-clock and critical-path arithmetic never use commit timestamps or transcripts.

## 12. Gate invocation, repair, and fallback pointers

The gate is `skills/external/sdd-loop-driver/scripts/wp-gate.py`: deterministic, standard-library only, never dispatches, never writes the spine, and never modifies the plan.

- CLI grammar and input precedence: WG-02 and WG-03.
- JSON envelope, including `dispatch_layers` and `integration_order`: WG-04 plus WP-04.
- Exit taxonomy (`0` admit/single-package, `1` reject, `2` input/parse/I/O or unavailable layer): WG-05.
- Plan checks: WG-06 (schema), WG-07 (graph), WG-08 (output coverage), WG-09 (boundedness), WG-10 (kind), WG-11 (pattern), WG-12 (hash), WG-13 (benefit).
- Preflight checks: WG-14 (manifest coverage and forbidden paths), WG-15 (unordered write/read and write/write territories), WG-16 (slot cap and resource isolation). Preflight re-runs the plan checks first, so one invocation can report a cycle, an orphan output, and a path overlap together; a schema failure suppresses the checks that need an incomplete record (WG-06 ordering).
- Retry checks: WG-17 (ledger-derived dispatch counts, attempt-1 admission, a material delta for attempt 2, strictly-greater budget with dispatch-level evidence, split-child attempt inheritance, split depth one, `retry-unchanged`/`retry-delta-invalid`/`retry-exhausted`). The counter source is OR-14; there is no counter file.
- One repair is allowed (split, serialize, or reduce to one package), recorded as an amendment. A second reject falls back to `single-package` with `decision=fallback`, `reason=gate-reject`, and the finding list as evidence. Exit 2 falls back with `reason=decomposition-unavailable`. The fallback verdict mapping is owned by FN-08 and WG-18.
- The gate's verdict is appended to the ledger's `plan` event before the first dispatch. The plan fence itself is never edited by the gate and remains the canonical decision record.

## 13. Scheduler and dispatch (SD-01…SD-16)

The scheduler is **driver prompt logic**, not a runtime engine. The driver is the sole coordinator: it selects the ready set, enforces the slot cap, dispatches packages, collects results, reads verifiers, records the ledger, and decides the stage gate. Package executors never dispatch other packages, never spawn a driver, and never edit the plan (SD-01, FR-015).

### 13.1 Readiness and the write-alone rule (SD-02, SD-03, SD-06)

A package is **ready** when every `depends_on` entry has a ledger `verdict=pass` with an evidence pointer in the current stage attempt. A failed, missing, or malformed verdict keeps the dependent `blocked`; the driver records it instead of dropping it. The dependency status is re-read from the ledger after every settlement, never from session memory.

Every write package is dispatched **write-alone**: if a write is ready, the driver stops launching new read-only packages, waits for every running package to settle, dispatches exactly one write package, and only after it settles resumes the read-only queue. A ready write is never deferred behind newly launched reads. Its effective concurrency is 1.

### 13.2 Read-only concurrency and the slot cap (SD-04, SD-05)

Up to `slot_cap` read-only packages run concurrently; the default and the ceiling are owned by SD-04 and enforced by WG-16. When the local host cannot issue parallel native calls, the driver records `parallel_requested=yes`, `effective=serial`, `reason=host-no-parallel-native` and dispatches serially (SD-07); the effective concurrency is recorded on every dispatch event (V-LED.10).

The ready set is ordered by topological layer and then `wp_id` lexicographic, the declared tie-break (WP-04). The ledger records the actual `dispatch_order` counter separately; integration uses the declared order, never the dispatch timing order (SD-05).

### 13.3 Collection, verifier dispatch, and failure isolation (SD-09…SD-12)

A package **settles** only when the runner's terminal status (`exit`, `sentinel`) and the last non-empty log line agree on the WP sentinel. The driver then reads the attempt-scoped result file. `INCOMPLETE`, a missing result file, a missing sentinel, or an `ANOMALY` line means the package did not complete and is not verified.

After a complete result, the driver dispatches one independent verifier and waits for the verdict before treating the package as verified (SD-10; VI-01 owns independence). A dependency unlocks only on `verdict=pass` with an evidence pointer. A failed, stalled, or budget-exhausted package never cancels unrelated running packages; its dependents remain blocked, unrelated ready packages continue and are recorded, and the failure is surfaced (SD-11). A package that fails twice appends `wp_failed` and the stage enters the unchanged U5 path (SD-12).

### 13.4 Dispatch topologies (SD-07, SD-08, SD-15)

Local: one native host subagent per package through the existing `run-agent` dispatch path. No external CLI is launched locally; when the host cannot issue parallel native calls, the serial fallback above applies. Remote: one detached `stage-runner.sh` per package with the unique label `<stage>-<wp_id>` and the package sentinel; each package keeps its own pid/status/log/heartbeat set, and no runner or sentinel is shared.

SD-15 owns the closed list of mechanisms this layer does not add; the runtime rule here is simply **no dispatcher** — the scheduler loop is the driver's prompt logic, and both dispatch forms are the existing ones.

Before dispatch the driver applies SD-13: the outgoing prompt must not name or load `sdd-loop-driver`, must not instruct the subagent to load any skill, and must contain no loop logic. A failing prompt is not dispatched and the block is recorded. The check is `run-agent` dispatch governance, cited here, not redefined.

### 13.5 Resource isolation and re-entry (SD-14, SD-16)

WG-16 is the preflight check for resource isolation: every concurrently dispatchable package declares an isolated port block, temporary directory, cache directory, or a non-empty shared read-only resource; no package starts a global service or writes a shared mutable cache.

On re-entry the driver reads the spine, re-runs `watch-target.sh --once` for any detached runners, and **never redispatches a completed package**. A U5 stage retry starts a new `stage_attempt` with a fresh plan fence, a fresh plan hash, and a fresh per-package attempt counter; earlier records remain in the spine.

## 14. Retry, delta, and escalation (OR-14…OR-16)

The per-package retry counter is derived by counting ledger `dispatch` events for `(stage, stage_attempt, wp_id)`; there is no counter file (OR-14). Attempt 1 is admitted without a delta. Attempt 2 requires a `retry_delta` naming `scope`, `budget`, or `topology` (OR-15); `wp-gate.py --check retry` validates it. Attempt 3, a package already at two attempts, a split child's further attempt, and any proposed split of a child are `retry-exhausted`.

A split is permitted once per lineage. The parent record keeps its attempt history and gains `superseded_by`; the children inherit the parent's attempt count — their sole dispatch is the lineage's retry attempt — and split depth is one, so a child is never split again or retried. A child failure fails the stage gate without a further automatic retry.

A scope change strictly decreases `bounded_by.count` or splits into children with distinct outputs. A budget change strictly increases `max_turns` and carries a dispatch-level `evidence_ref`; an identical same-budget rerun is `retry-unchanged`. A topology change uses the closed OR-15 value set and must change the value. The three finding codes the driver routes on are `retry-unchanged`, `retry-delta-invalid`, and `retry-exhausted`.

A package failing twice, or a split child failing at all, records `wp_failed` with its attempt history and verdict evidence, fails the stage gate, and enters the unchanged U5 stage-retry path (OR-16). Package retries never consume the stage-level retry budget before that escalation.

### 14.1 Simulator limitation

`tests/fixtures/wp_driver_sim.py` is a **test-only** deterministic model of the algorithm above. It proves the mechanical rules (readiness, ordering, slot cap, write-alone, collection, isolation, re-entry), not an LLM's adherence to the prompt; live claims require spine evidence (research.md R4, plan.md R-12).

## 15. Independent verification (VI-01…VI-06)

Every settled package is verified by exactly one fresh-context **stage-verifier** execution that is not the package's executor (VI-01). The verifier is read-only with respect to repository content: it may run the package's declared targeted tests, including the existing `targeted-set-v1` selection, but never a full suite (VI-02; the two-slot test budget is unchanged). A native topology uses one host subagent; a detached topology uses `stage-runner.sh` labeled `<stage>-<wp_id>-verify`; when the host cannot spawn a subagent, the driver itself verifies as `driver-u4`, records `host-no-subagent`, and remains structurally independent of the executor.

The verdict is written to `<state-dir>/wp/<line>-<stage>-<wp_id>-a<N>w<M>.verdict.json` and carries the E6 fields: `schema_version`, identity, `verdict`, `checks[]` covering every acceptance criterion, `evidence_refs[]`, the verifier's `execution_id`, and `verified_at` (VI-03; the schema is owned by `data-model.md` E6). The driver appends a `verdict` ledger event `{wp_id, verdict, verifier_execution, evidence_ptr, at}` after reading the file; a package without that event is not verified (VI-05).

A missing, unreadable, malformed, or ambiguous verdict counts as `fail` (VI-04). Success is never inferred from a package self-report, a missing file, or a package sentinel. A dependent unlocks only on the resulting `verdict=pass` plus its evidence pointer (SD-02, SD-12).

### 15.1 Verdict failure handling

| Verdict artifact | Ledger event | Package state |
|---|---|---|
| valid `pass` | `verdict=pass` | verified; dependents may unlock |
| valid `fail` | `verdict=fail` | unverified; dependents stay blocked |
| missing / unreadable / malformed / ambiguous | `verdict=fail` with the expected path as `evidence_ptr` | unverified; dependents stay blocked |

The attempt-scoped path is owned by WP-11. Verifier executions do not consume the slot cap and are excluded from package durations and parallelism efficiency (`data-model.md` E7, V-EXE.3/V-EXE.4).

## 16. Integration and stage close (VI-07…VI-14)

After every dispatchable package settles, the driver aggregates the verified verdict set (VI-06). Coverage is checked against `required_outputs` minus `integrator_outputs`: package outputs must cover the former exactly, while every `integrator_outputs` entry is expected from the single integrator seat. Missing or contradictory outputs are surfaced with both evidence pointers; a contradiction is two sources claiming one output path with different content.

Verified outputs are integrated in topological layers, each layer sorted by `wp_id` lexicographic (VI-07). The order is declared by the plan and recorded in the `integrate` event; it is not the dispatch order. An integration conflict or a missing output stops integration, fails the stage gate, and leaves no partial commit presented as a complete stage deliverable (VI-08).

For `decision=decomposed`, one `stage-integrator` execution per stage attempt receives the plan, the verified outputs, and the stage authority artifacts (VI-11). It aggregates in the declared order, produces the plan's `integrator_outputs`, makes the single closing commit, and emits `<STAGE>-DONE` as its last non-empty line. `integrator_outputs` belong to this seat, are excluded from package coverage (WG-08), and are verified by the stage U4. The integrator never dispatches a package, never re-plans, and never loads the driver.

Package sentinels are never promoted: only the integrator's `<STAGE>-DONE` satisfies the stage requirement, while a `WP-…-DONE` package sentinel never satisfies it (VI-12). The single-package path is the stage execution itself, so its sentinel is the stage sentinel.

### 16.1 Commit discipline (VI-09, VI-10)

For stages without a part-commit discipline (`plan`, `review`, `analyze`, `clarify`), package executors do not commit; the integrator makes the single closing commit after integration (VI-09). For `implement`, the 067 part-commit discipline is preserved: part commits stay as they are, and the closing commit covers the remaining integrated deliverable without rewriting, squashing, or bypassing them (VI-10).

### 16.2 Unchanged stage U4 and closure (VI-13, VI-14)

After integration the driver runs the unchanged stage U4: the stage sentinel is necessary, artifact verification is required, and discipline checks are required; package verdicts are inputs and never substitutes (VI-13). A failed package or a failed U4 fails the stage gate.

Closure and merge stay driver-owned under 058 and 064: this layer does not push, force-merge, or auto-merge, and preserves the existing confirmation gates (VI-14). The `integrate` event, the stage U4, `wp-report.py`, and the `stage-close` event follow in that order (OR-03, OR-11).

The deterministic simulator in `tests/fixtures/wp_driver_sim.py` models this part as `verify()` plus `integrate()`; like section 14.1 it proves the mechanical rules, not an LLM's adherence.

## 17. Non-regression boundaries

This layer adds pre-U4 steps only. It does not change stage sentinel literals, the stage chain, U4 independent verification, watcher verdicts/exit codes, stall handling, the fast lane, the two-slot test budget, the plan minor-fix constraint, Feature 064's registry/ownership/worktree/integration semantics, Feature 067's part brief and test economics, or Feature 068's feedback channel. Preserved-behavior obligations are owned by `contracts/fallback-and-nonregression.md` FN-09…FN-16 and are cited here, not restated.
