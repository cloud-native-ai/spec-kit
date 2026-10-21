# Contract SP — State Spine Machine Segment, `check-spine` & Watchbeat

**Owner**: `skills/external/sdd-loop-driver/references/state-awareness.md` § State Spine & Watchbeat; the pre-existing spine write points and stall defaults remain owned by `references/stage-prompts.md`.
**Scope**: the additive machine-readable segment, its validator, the driver lifecycle rules that make it useful, and the watchbeat presence marker.

## Segment shape

- **SP-01**: The segment is delimited by exactly one `<!-- loop-state:begin -->` line and one `<!-- loop-state:end -->` line.
- **SP-02**: Inside the fence every key is `key: value`, every key starts with `spine_`, and keys are unique. A bare `state:` key is a violation even if another prefixed key exists.
- **SP-03**: `spine_schema: v1` is required. The segment never reuses `<!-- test-budget:begin -->` or any other owner's fence.
- **SP-04**: Prose outside the fence is preserved byte-for-byte by the engine; the engine only replaces the fenced block (or appends one when absent).
- **SP-05**: Unknown `spine_*` keys are preserved and ignored by readers. Non-`spine_` keys inside the fence are a validation violation.
- **SP-06**: `spine_state` belongs to `running / retrying / stalled / reentry-required / done`. `spine_stage`, when present, belongs to the eight known stages.
- **SP-07**: `spine_attempt` is a non-negative integer; `spine_stage_started_at` and `spine_stage_deadline_epoch` are positive epochs when present.
- **SP-08**: `spine_last_verdict`, when present, belongs to the watcher verdict set (`RUNNING/DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL`).
- **SP-09**: `spine_evidence` is a comma-separated list of at least one non-empty pointer. Existence is not required because evidence may be remote or archived.

## Required fields per state

- **SP-10**: `running` requires `spine_pid_path`, `spine_status_path`, `spine_log_path`, `spine_heartbeat_path` and `spine_stage_deadline_epoch`.
- **SP-11**: `retrying` requires `spine_retry_reason` and a positive `spine_attempt`.
- **SP-12**: `stalled` requires `spine_stall_reason` and at least one `spine_evidence` pointer.
- **SP-13**: `reentry-required` requires `spine_stage`, `spine_attempt`, `spine_last_verdict` and at least one evidence pointer.
- **SP-14**: `done` requires `spine_stage`, `spine_attempt` and `spine_last_verdict`.
- **SP-15**: `spine_salvage=accepted` requires non-empty `spine_salvage_evidence` and `spine_salvage_at`; `none` or absence requires both keys absent. A claimed salvage without evidence is a validation failure.
- **SP-16**: State/verdict consistency: `done` ⇒ `spine_last_verdict=DONE`; `retrying`/`stalled` ⇒ a present verdict that is not `DONE`; `running` ⇒ absent or `RUNNING`; `reentry-required` accepts any recorded verdict.

## Validator

- **SP-17**: `--action check-spine` returns exit 0 only when the segment and all required cross-field rules pass; exit 1 with a machine-readable `violations[]` (`code`, `field`, `detail`); exit 2 for unreadable input.
- **SP-18**: A missing fence or `spine_schema` other than `v1` is a violation (`machine-segment-missing` / `schema-unsupported`), exit 1. The snapshot still evaluates a legacy spine with `unknown` fields.
- **SP-19**: Duplicate keys, bare `state:`, non-`spine_` keys, empty values, invalid enums and every per-state requirement produce a distinct violation code.
- **SP-20**: The driver runs `check-spine` before every U2 dispatch and before writing `stalled`; a non-zero result blocks the dispatch/write and is recorded in the spine.
- **SP-21**: A legacy spine (no fence) is reported as `schema=legacy` by snapshot with missing fields `unknown`; snapshot never guesses and never auto-migrates the file.
- **SP-22**: Recovery writes to the segment are temp-file + `os.replace` + fsync; a concurrent reader never observes a half-written segment. The recovery record keys are `spine_recovery_action/result/at/run_id/attempt/reason` plus the optional `spine_handoff_path`.

## Watchbeat

- **SP-23**: The marker path is `<state-dir>/watchbeat-<line>-<stage>`, one line, atomically overwritten.
- **SP-24**: Required fields: `run`, `stage`, `window` (integer seconds), `at` (integer epoch), `event ∈ watch-window|watch-return`. A missing `event` makes the marker legacy-attributable, not proof of a window.
- **SP-25**: The driver writes `event=watch-window` at each U3 window start and `event=watch-return` when the window returns; this is the fifth signal, not a completion or liveness signal.
- **SP-26**: Freshness is `now - at ≤ window + deadline_grace` with the grace resolved from the watcher (SN-40). A missing/unparseable window or unresolved grace makes freshness `null`, and no `unwatched` finding is emitted.
- **SP-27**: Watchbeat never participates in `loop_state`, `DONE`, liveness, the attempt counter or any verdict. `RUNNING` windows still do not write the spine.
- **SP-28**: Recovery `watch --apply` refreshes the marker with `event=watch-return` and returns control; it writes no spine or attempt state.

## Lifecycle rules

- **SP-29**: SKILL.md Hard Requirements state: U2 dispatch and the first U3 watch window MUST start in the same driver turn; dispatch-without-listen is a lifecycle violation.
- **SP-30**: SKILL.md Hard Requirements state: before a driver ends its session it MUST write `stalled` or `reentry-required` with stage, attempt, last verdict and evidence pointers, and report explicitly; silent exit is not a legal output.
- **SP-31**: SKILL.md points to `check-spine` as the deterministic validator and to this contract/owner reference for the segment, without restating the field table.
- **SP-32**: `references/watch-model.md` remains the sole owner of watch verdicts and is not edited by this feature.

## Clause → requirement map

| Clause | FR / SC |
|--------|---------|
| SP-01–SP-09 | FR-021, FR-022 |
| SP-10–SP-16 | FR-021 |
| SP-17–SP-22 | FR-021, FR-022, FR-035, SC-006 |
| SP-23–SP-28 | FR-010, FR-011, FR-033 |
| SP-29–SP-32 | FR-019, FR-020, FR-043, FR-044 |
