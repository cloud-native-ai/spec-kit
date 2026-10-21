# Contract SN — Snapshot, Evidence Attribution, Derived State & Interruptions

**Owner**: `skills/external/sdd-loop-driver/references/state-awareness.md` § Evidence Model, § Derived Loop State, § Interruption Forms.
**Scope**: what a snapshot aggregates, how each signal is attributed, the numbered derived-state rules and the eight interruption findings. Numeric watch defaults are not owned here; they are resolved from `scripts/watch-target.sh` (see SN-28).

## Snapshot envelope

- **SN-01**: A snapshot contains at least: `schema_version`, `action`, `line_id`, `run_id`, `stage`, `loop_state`, `derived_rule`, `verdict_source`, `watch_verdict`, `recovery_action`, `spine`, `evidence_source`, `probe`, `evidence`, `thresholds`, `interruptions`, `missing_artifacts`, `uncommitted_artifacts`, `stale_signals`, `evaluated_at`.
- **SN-02**: Every evidence sub-object carries a status from `present|missing|na`, a locatable path or `null`, and only measured values. Missing values are `missing`/`unknown`/`null`; zero, empty string and `ok` never stand in for a missing signal.
- **SN-03**: `spine` reports `path`, `present`, `schema ∈ v1|legacy|missing`, `state`, `attempt`, `last_verdict`, `consistent` and `missing_fields[]`. A legacy spine yields `unknown` for absent fields.
- **SN-04**: `schema_version` is `1`; new fields may be added, but existing field names and meanings never change. Old readers ignore unknown fields.

## Watch verdict and attribution

- **SN-05**: The attribution mode is `own` when the invocation passes `--line-id` and `--run-id`, `legacy` when it passes neither, and `probe` when a probe is consumed. Passing only one of the pair is forbidden.
- **SN-06**: Choose `own` only when a Registry entry exists for the line AND at least one existing carrier carries both `line=` and `run=` matching that entry. Otherwise use `legacy`; if more than one Registry line is active and the target is not attributable, `watch=unavailable(reason=attribution-required-multi-line)` and the derived map is used.
- **SN-07**: Watcher invocation uses `watch-target.sh --once` with the four carrier paths, sentinel, deadline, `--deadline-grace` and `--heartbeat-max-age`; the same execution identity as the runner is required.
- **SN-08**: When a `WATCH` line is returned, `loop_state` equals `verdict` verbatim, `verdict_source=watcher`, `derived_rule=null`; the aggregator MUST NOT rewrite, downgrade or upgrade it.
- **SN-09**: When no verdict is available (no watcher, invocation failure, missing script, probe without a verdict), `verdict_source=derived` and `watch_verdict.present=false` with the failure reason recorded. A failure is never a stage failure, `DEAD` or a fabricated verdict.

## Derived loop_state (no watcher verdict)

The rules are evaluated in this exact order; the first match wins and its id is emitted as `derived_rule`. The owner reference carries the same ids in the same order.

- **SN-10**: **D0 — not dispatched**: no `stage_started_at`, no carrier, no sentinel and no completion evidence ⇒ `loop_state=UNKNOWN`, `reason=not-dispatched`. A line beyond a start grace but never dispatched MUST NOT become `NO_SIGNAL`.
- **SN-11**: **D1 — spine decision**: `spine_state=stalled` ⇒ `STALLED`; `spine_state=reentry-required` ⇒ `REENTRY_REQUIRED`.
- **SN-12**: **D2 — exit record**: with an own, non-stale status record: if (status exists or pid is dead) and the last non-empty log line starts with `ANOMALY:` ⇒ `ANOMALY`; else `exit≠0` ⇒ `FAILED`; else `exit=0` with sentinel and complete artifacts ⇒ `DONE`; else `exit=0` with missing sentinel or missing artifacts ⇒ `INCOMPLETE`.
- **SN-13**: **D3 — sentinel without exit record**: sentinel present and artifacts complete ⇒ `DONE`; artifacts missing ⇒ `INCOMPLETE`.
- **SN-14**: **D4 — dead without exit record**: no status record, pid record present and process dead/zombie/reused ⇒ `DEAD`.
- **SN-15**: **D5 — deadline overrun**: a positive deadline exists, `now ≥ deadline + grace`, and no terminal verdict was matched above ⇒ `TIMEOUT`, including when the process is alive.
- **SN-16**: **D6 — no signal**: no pid record, no status record, and `now ≥ stage_started_at + start grace` ⇒ `NO_SIGNAL`.
- **SN-17**: **D7 — running**: pid alive or heartbeat fresh, with no terminal match ⇒ `RUNNING`.
- **SN-18**: **D8 — unknown**: every other case ⇒ `UNKNOWN`.
- **SN-19**: The derived map uses the same evidence predicates as the watcher for the same verdict names, but it is an independent aggregation: it MUST NOT produce watcher exit codes and MUST NOT claim watcher semantics.
- **SN-20**: If `spine_last_verdict` conflicts with the independent verdict, `spine.consistent=false` and both values are reported; the engine never silently picks one.

## Artifacts and commits

- **SN-21**: Artifact completeness is decided by existence and non-empty content only. A directory artifact requires at least one non-empty `.md` file. Log text never proves completeness.
- **SN-22**: The Stage Artifact Map (data-model E-09) supplies `required`, `commit_required`, `no_change_allowed` and commit scope per stage; an unknown stage yields `artifacts=unknown`, never an empty required set.
- **SN-23**: Commit evidence uses `spine_stage_base_commit` as its only base. A missing/invalid base yields `commits.status=unknown`; it never falls back to the latest commit.
- **SN-24**: `commit_required=false` yields `not-applicable`; clarify yields `not-applicable` when `requirements.md` did not change since the base.
- **SN-25**: Uncommitted detection runs `git status --porcelain -- <stage paths>`; only stage-owned paths enter `uncommitted_artifacts[]`. Unrelated dirty files are neither reported nor staged.
- **SN-26**: Implement commit evidence scans commits after the base that touch non-`.specify/` paths; `verification.md` remains its required artifact.
- **SN-27**: A sentinel with missing artifacts is `INCOMPLETE` (pseudo-completion), never `DONE`, for both watcher and derived paths.

## Interruption forms

All matching forms are emitted, ordered I1–I8. Each carries evidence pointers and one factual sentence. The suggested spine state is advisory; the action comes from the recovery contract.

- **SN-28** (`I1 unwatched`): Live evidence exists (pid alive or heartbeat fresh) and the watchbeat is missing or stale by SN-30 ⇒ emit `unwatched`, suggest no spine write, action direction `watch`.
- **SN-29** (`I2 dead-no-exit-record`): A pid record exists, the process is dead/zombie/reused, and no own status record exists ⇒ emit `dead-no-exit-record`; never report completion.
- **SN-30** (`I3 deadline-overrun-live`): Deadline + grace has elapsed, pid is alive or heartbeat fresh, and no terminal verdict exists ⇒ emit `deadline-overrun-live`; `loop_state=TIMEOUT`; never suggest a kill.
- **SN-31** (`I4 heartbeat-stalled`): A pid record exists and the heartbeat age exceeds the resolved maximum ⇒ emit `heartbeat-stalled` as a warning; `loop_state` remains `RUNNING`; deadline stays the only timeout criterion.
- **SN-32** (`I5 artifacts-without-completion`): Every required artifact is present and the sentinel is missing, regardless of the exit record or code ⇒ emit `artifacts-without-completion`; `loop_state` keeps its source verdict (`INCOMPLETE`/`FAILED`/`DEAD`), never `DONE`.
- **SN-33** (`I6 stale-signal`): A carrier's envelope mismatches the current run, its mtime predates `stage_started_at`, or it cannot be proven own while a current run is known ⇒ emit `stale-signal` and list the carrier in `stale_signals[]`; the carrier never feeds derivation.
- **SN-34** (`I7 lifecycle-spine-violation`): `spine_state=running` while no live evidence, no fresh watchbeat and no terminal evidence exist (or a terminal `spine_last_verdict` contradicts `running`) ⇒ emit `lifecycle-spine-violation`; suggest `stalled` or `reentry-required`.
- **SN-35** (`I8 remote-unreachable`): A probe declares `reachable=false`, or the caller records an unreachable transport for the evidence host ⇒ emit `remote-unreachable`, `loop_state=STALLED`, suggest `stalled(remote-unreachable)`; never `DEAD` and never a stage failure.
- **SN-36**: Multiple different forms coexist in one snapshot; no form suppresses another. The action is adjudicated once from the complete list (recovery contract RC-02).
- **SN-37**: `unwatched` and a normal window-end `RUNNING` are distinguished only by a fresh watchbeat; a fresh marker means normal re-entry, not an interruption.

## Watchbeat and thresholds

- **SN-38**: Watchbeat evidence reports `run`, `stage`, `window`, `at`, `event`, `fresh`, `threshold` and `attribution`. Freshness uses `at` (not mtime) plus `window` plus the resolved deadline grace; a future `at` yields age 0 and a `clock-skew` note.
- **SN-39**: A missing/unparseable `window` or unresolved grace makes freshness `null`; the engine suppresses `unwatched` and records `threshold=unknown` instead of guessing.
- **SN-40**: Thresholds resolve as: explicit CLI flag → the `Defaults:` line of `watch-target.sh --help` → `unknown`. The resolved values and source appear in `thresholds`.
- **SN-41**: The engine never restates watch defaults as its own constants; the watcher is the owner.
- **SN-42**: A probe snapshot is normalized with `evidence_source=probe`, `probe.used=true`, `probe.reachable` and `probe.collected_at`; local evidence is not mixed in.
- **SN-43**: A snapshot emits no elapsed/age numbers; `evaluated_at` and `observed_at` are the only time-varying fields. Two snapshots of the same file state differ only in timestamps.
- **SN-44**: No `ps`/`pgrep` scan is used for liveness; PID identity comes from the PID file plus `kill -0` plus the start token (and `/proc` on Linux).

## Clause → requirement map

| Clause | FR / SC |
|--------|---------|
| SN-01–SN-04 | FR-003 |
| SN-05–SN-09 | FR-002, FR-004, FR-005, FR-024 |
| SN-10–SN-20 | FR-004, FR-022 |
| SN-21–SN-27 | FR-006, FR-007, FR-008, FR-017 |
| SN-28–SN-37 | FR-009, FR-011, FR-013–FR-018, FR-024 |
| SN-38–SN-41 | FR-010, FR-011, FR-016 |
| SN-42–SN-44 | FR-002, FR-012, FR-023, FR-024, SC-001, SC-002, SC-009 |
