# Contracts: Cadence & loop-effectiveness metrics (C-40…C-50)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns what "continuous" means, what the four metrics are and how each derives its numerator and denominator, and the honesty rules that keep the metrics from becoming a gate or a score. The threshold protocol, the run-determination engine, and the routing backlog semantics are cited, never restated.
**Pinned by**: `tests/contract/test_client_metrics.py` (planned)
**Measures**: SC-005

**C-40**: "Continuous" is defined as the combination of capture on every qualifying run, the existing non-blocking threshold notice, and explicit user triggering of digest and improvement loops. No scheduler, resident process, timer, or self-starting periodic task is introduced in any form (FR-019).

**C-41**: No historical review record is backfilled: records produced before this feature lands are never given entries and are never batch-replayed to produce entries. The metrics state their coverage boundary — only runs from the channel's arming onward are counted — in the report itself (FR-020, SC-005).

**C-42**: The existing combination rule of the threshold protocol and run determination is unchanged: the notice appears only when both hold, stays non-blocking (no response reads as skipped, no repeated urging, no wrap-up blocking), and this feature changes neither its trigger condition, its placement, nor its blocking behavior (FR-020).

**C-43**: Four metrics answer whether continuous self-improvement works, each with an explicit numerator, denominator, and data source, all derived from existing records: capture coverage (runs captured / runs that produced a code-segment record), into-loop ratio (entries with an assigned carrier / total client entries), closure ratio (entries proven handled / total client entries), and repeat-finding rate (entries whose finding re-appears / total client entries) (FR-021, SC-005).

**C-44**: Closure is judged by change evidence on the assigned owner file, never by routing marks: the engine's `dispose` `processed`/`ignored` values are local metadata that verify no fix landed, and a `carried-by-spec-*` backlog row means carried, not completed, while an `open-unverified` row must be re-measured before anyone acts on it. An entry counts as closed only when its backlog row names an owner file that exists and changed after the entry was created (FR-021).

**C-45**: The repeat-finding rate is a coarse proxy: a finding counts as repeated when any of its record's (file, severity) pairs already appears in an earlier entry's record of the same unit, where the pairs are extracted deterministically from the pointed-to record. The metric is reported with a proxy label and is never phrased as a defect recurrence rate (FR-021, FR-023).

**C-46**: The metrics are read-built: recomputed from the existing records at every report, never persisted as an aggregate file, never written into any existing store partition, and never given a new directory or index. No scoring system, weights, total, or cross-metric conversion is introduced; the four metrics never compose into a single number (FR-022, SC-005).

**C-47**: The computation is program-first: a read-only action `client-metrics` on the existing feedback engine derives the four metrics from the store, the routing backlog, and the code-segment records, and emits machine-readable readings. The derivation is not performed by the agent from raw list output, and the action has no write point (FR-022).

**C-48**: Every zero or missing denominator renders that metric `not-evaluated` with its reason, never `0`, never `100%`, and the metric row is never omitted. The proxy label travels with the repeat-finding rate. The metrics influence nothing: they are not a gate, not a status-transition condition, and not a threshold input (FR-023, SC-005).

**C-49**: The capture-coverage denominator counts code-segment records from the channel's arming onward — the boundary is the creation stamp of the unit's first external entry (or of all external entries when no unit filter is given); earlier records are excluded by this rule, not backfilled, and the exclusion is disclosed in the output (FR-020, FR-021, SC-005).

**C-50**: An entry whose pointed-to record is unreadable is excluded from the repeat-finding rate's numerator and denominator together, and the output carries the excluded count with the reason; exclusion never changes the other three metrics (FR-021, FR-023, SC-005).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-40 | FR-019 | — | cadence definition |
| C-41 | FR-020 | SC-005 | no-backfill rule |
| C-42 | FR-020 | — | threshold protocol |
| C-43 | FR-021 | SC-005 | four metrics |
| C-44 | FR-021 | — | closure evidence |
| C-45 | FR-021, FR-023 | — | proxy label |
| C-46 | FR-022 | SC-005 | read-built rule |
| C-47 | FR-022 | — | engine action |
| C-48 | FR-023 | SC-005 | not-evaluated rule |
| C-49 | FR-020, FR-021 | SC-005 | coverage boundary |
| C-50 | FR-021, FR-023 | SC-005 | unreadable-record rule |
