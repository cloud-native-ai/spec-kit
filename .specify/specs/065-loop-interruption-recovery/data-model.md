# Data Model — Feature 065 Loop Interruption Awareness & Recovery

**Date**: 2026-10-21 | **Spec**: [requirements.md](requirements.md) | **Research**: [research.md](research.md)

This model describes the projection and record shapes the new layer reads or writes. Existing owners are not redefined: watch verdicts belong to `scripts/watch-target.sh` / `references/watch-model.md`; stall defaults, U3/U4/U5 procedure and spine write points belong to `references/stage-prompts.md`; the plan-owned artifact set belongs to `references/efficiency-model.md` §3. The new owner reference `references/state-awareness.md` carries the numbered rule tables this model references.

## 1. Entities

### E-01 LoopStateSnapshot

One read-only evaluation for one `(line, stage)`; also the unit persisted by `--out` and consumed as a probe.

| Field | Type | Presence | Meaning |
|-------|------|----------|---------|
| `schema_version` | integer | required, `1` | Envelope version; append-only evolution |
| `action` | string | required, `"snapshot"` | Command discriminator |
| `line_id` / `run_id` / `stage` | string | required, `"unknown"` when unresolvable | Identity; never invented |
| `loop_state` | enum | required | `RUNNING/DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL/STALLED/REENTRY_REQUIRED/UNKNOWN` |
| `derived_rule` | string | present when `verdict_source=derived`, else `null` | `D0`–`D8`, or `null` for a watcher verdict |
| `verdict_source` | enum | required | `watcher` or `derived` |
| `watch_verdict` | object | required | `present`, `verdict`, `reason`, `exit_code`, `source`, `attribution`, `pid`, `heartbeat`, `rc`, `sentinel`, `grace_expired`; absent values are `null`, never zero |
| `recovery_action` | enum | required | `none/watch/verify/resume/retry/stop` |
| `spine` | object | required | `path`, `present`, `schema` (`v1/legacy/missing`), `state`, `attempt`, `last_verdict`, `consistent`, `missing_fields[]` |
| `evidence_source` | enum | required | `local` or `probe` |
| `probe` | object | required | `used`, `path`, `reachable`, `collected_at` |
| `evidence` | object | required | `pid`, `status`, `log`, `heartbeat`, `watchbeat`, `artifacts`, `commits` (E-02) |
| `thresholds` | object | required | `deadline_grace`, `heartbeat_max_age`, `start_grace` (integer or `null`), `source` (`cli/watch-target.sh-help/unknown`) |
| `interruptions` | array | required | E-05 findings, ordered I1–I8 |
| `missing_artifacts` / `uncommitted_artifacts` | array | required | Repo/spec-relative paths, ordered |
| `stale_signals` | array | required | `{kind, path, reason}` ordered by kind |
| `evaluated_at` | ISO-8601 string | required | The only wall-clock field in the stable core besides `observed_at` |

### E-02 EvidenceBundle

| Sub-object | Fields | Rules |
|------------|--------|-------|
| `pid` | `status`, `path`, `pid`, `start`, `alive`, `process_state`, `attribution` | `alive` is `true/false/null`; `process_state ∈ alive/dead/zombie/reused/missing/unknown`; PID identity uses PID file + `kill -0` + start token |
| `status` | `status`, `path`, `exit`, `sentinel`, `at`, `run_id`, `attribution`, `stale` | `exit`/`sentinel` are integers or `null`; a stale status never feeds derivation |
| `log` | `status`, `path`, `last_line`, `sentinel_present`, `anomaly_line` | Last non-empty line only; no body inference |
| `heartbeat` | `status`, `path`, `mtime`, `fresh`, `attribution`, `stale`, `threshold` | `fresh` is `true/false/null`; `threshold` is the resolved max age or `null` |
| `watchbeat` | `status`, `path`, `mtime`, `at`, `window`, `run_id`, `event`, `fresh`, `attribution`, `stale`, `threshold` | Freshness = `at + window + deadline_grace ≥ now`; only presence evidence |
| `artifacts` | `status`, `required[]`, `present[]`, `missing[]`, `commit_required`, `no_change_allowed` | Completeness = every required path exists and is non-empty; directory entries require ≥1 `.md` |
| `commits` | `status`, `base`, `commits[]`, `uncommitted[]`, `scope` | `committed/missing/unknown/not-applicable`; base is `spine_stage_base_commit` only |

### E-03 WatchbeatMarker

Path `<state-dir>/watchbeat-<line>-<stage>`; one line, atomic overwrite (temp + `mv`).

```text
run=<run_id> stage=<stage> window=<seconds> at=<epoch> event=watch-window|watch-return
```

`event` may additionally be absent in a legacy marker; absence makes the marker `attribution=legacy`. It never participates in `loop_state`, `DONE` or liveness.

### E-04 StateSpine (machine segment)

Fenced segment inside the per-line state spine:

```text
<!-- loop-state:begin -->
spine_schema: v1
spine_state: running|retrying|stalled|reentry-required|done
spine_line_id: <line_id>
spine_run_id: <run_id>
spine_stage: <stage>
spine_attempt: <int>
spine_stage_started_at: <epoch>
spine_stage_deadline_epoch: <epoch>
spine_pid_path: <path>
spine_status_path: <path>
spine_log_path: <path>
spine_heartbeat_path: <path>
spine_sentinel: <STAGE>-DONE
spine_last_verdict: RUNNING|DONE|INCOMPLETE|ANOMALY|FAILED|DEAD|TIMEOUT|NO_SIGNAL
spine_evidence: <pointer>[,<pointer>…]
spine_salvage: none|accepted
spine_salvage_evidence: <pointer>[,<pointer>…]
spine_salvage_at: <iso8601>
spine_recovery_action: none|watch|verify|resume|retry|stop
spine_recovery_result: dry-run|applied|already-applied|locked|refused|failed
spine_recovery_at: <iso8601>
spine_recovery_run_id: <run_id>
spine_recovery_attempt: <int>
spine_recovery_reason: <text>
spine_handoff_path: <path>
<!-- loop-state:end -->
```

Unknown `spine_*` keys are preserved and ignored by readers. Prose outside the fence is never modified by the engine.

### E-05 InterruptionFinding

| Field | Type | Meaning |
|-------|------|---------|
| `form` | enum | `unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable` |
| `rule` | string | `I1`–`I8` |
| `evidence` | array of strings | Locatable pointers (paths, commit ids, epoch values quoted in text) |
| `detail` | string | One factual sentence; no recommendation and no speculation |
| `suggested_spine_state` | enum/null | `stalled`, `reentry-required` or `null` when the form does not by itself require a write |

### E-06 RecoveryDecision

| Field | Type | Meaning |
|-------|------|---------|
| `action` | enum | `none/watch/verify/resume/retry/stop` |
| `rule` | string | `AD-1`–`AD-9` from the owner reference |
| `reason` | string | Stable machine reason (e.g. `attempt-limit`, `probe-unreachable`, `artifact-complete-no-sentinel`) |
| `requires_salvage` | boolean | True when `resume` would be legal only with a recorded salvage |
| `requires_explicit_decision` | boolean | True when a live process TIMEOUT or an unisolatable stale signal requires the user's decision |

### E-07 RecoveryRecord

The `spine_recovery_*` keys plus salvage keys. One current record per line/stage; history lives in the spine's git history and in handoff files. Idempotency is decided from this record, the attempt counter and the filesystem state, never from session memory.

### E-08 RecoveryLock

`<state-dir>/recover-<line>.lock`, exclusive-create, JSON body `{pid, start, run_id, at, action, stage}`. It serializes every `recover --apply` for the line; it is released only by its holder or by an explicit `--break-lock` (which moves it to `attempts/`).

### E-09 StageArtifactSpec / StageArtifactMap

| Stage | Required artifacts (relative to spec dir) | `commit_required` | `no_change_allowed` | Commit scope |
|-------|------------------------------------------|-------------------|---------------------|--------------|
| requirements | `requirements.md` | true | false | `requirements.md` |
| clarify | `requirements.md` | conditional | true | `requirements.md` when changed |
| plan | `plan.md`, `research.md`, `data-model.md`, `contracts/` (≥1 `.md`), `quickstart.md`, `feature-ref.md` | true | false | the six plan-owned paths |
| tasks | `tasks.md` | true | false | `tasks.md` |
| checklist | `checklists/` (≥1 `.md`) | true | false | `checklists/` |
| analyze | none (sentinel + report in log are the U4 evidence) | false | true | not-applicable |
| implement | `verification.md`; code/test commits are commit evidence | true | false | commits after base touching non-`.specify/` paths |
| review | `review.md` | true | false | `review.md` |

`commit_required=conditional` means required only when the stage changed `requirements.md` since `stage_base_commit`; otherwise commit state is `not-applicable`. The map is data in `loop-state.py` plus § Stage Artifact Map in `references/state-awareness.md`; a contract test compares the two.

### E-10 ProbeEnvelope

`--probe FILE` accepts a snapshot (E-01) or `{schema_version:1, reachable:false, reason:<text>}`. A probe snapshot's own `evidence_source` is normalized to `probe`; the top-level output records `probe.used=true` and never invokes a local watcher.

### E-11 HandoffReport

Created only by `stop --apply`: `<state-dir>/handoff-<line>-<stage>-a<attempt>-<epoch>.md` with four sections — what was found (line/stage/`loop_state`/forms/watcher fields), why it was expensive (deterministic root-cause class with `derived=true`), every intermediate artifact locatable (spine, four-piece, watchbeat, artifacts, commits), and 2–3 options (fix environment and retry; inspect and record salvage; stop the line). It records `process_action=none`.

### E-12 AttemptIsolationBatch

`attempts/<attempt>-<run-id>-<epoch>/` holding moved carriers. Each file is moved with `os.replace`; the batch reports `moved[]`, `remaining[]`, `sequence`, and never deletes or truncates. A second `retry` after a partial move continues with the remaining files and does not increment the attempt until the batch is complete.

## 2. Validation Rules

### Snapshot

- **V-001**: `schema_version` is exactly `1`; unknown top-level fields are preserved for forward readers but never required.
- **V-002**: `loop_state` belongs to the closed set; no other casing or synonyms.
- **V-003**: `verdict_source=watcher` ⇒ `watch_verdict.present=true`, `derived_rule=null`, and `loop_state` equals `watch_verdict.verdict` verbatim.
- **V-004**: `verdict_source=derived` ⇒ `derived_rule` is one of `D0`–`D8`; a present watcher verdict is impossible in this mode.
- **V-005**: `recovery_action` belongs to the closed set and is emitted exactly once.
- **V-006**: Every evidence sub-object carries `status ∈ present/missing/na` and a `path` pointer or explicit `null`.
- **V-007**: A missing signal is `missing`/`unknown`/`null`; zero, empty string and `ok` MUST NOT stand in for missing.
- **V-008**: `missing_artifacts` and `uncommitted_artifacts` contain only paths from the Stage Artifact Map; no unrelated dirty files.
- **V-009**: `stale_signals[]` entries carry `kind ∈ status/pid/heartbeat/hook/watchbeat`, a path and a reason from `run-id-mismatch/before-stage-start/unprovable-envelope`.
- **V-010**: `interruptions[]` are ordered by rule id I1–I8 and carry no duplicate form.
- **V-011**: `thresholds.source=unknown` ⇒ every `fresh` that depends on a threshold is `null`, never a boolean guess.
- **V-012**: The stable core contains no elapsed/age numbers; `evaluated_at` and `observed_at` are the only time-varying fields.
- **V-013**: A probe snapshot sets `evidence_source=probe` and `probe.used=true`; local and probe evidence are never mixed in one evaluation.
- **V-014**: `spine.consistent` is `true/false` when both a spine `last_verdict` and an independent verdict exist, otherwise `null`; a conflict sets `false` and never silently picks one.

### State spine

- **V-015**: The machine segment is delimited by exactly one `<!-- loop-state:begin -->` / `<!-- loop-state:end -->` pair.
- **V-016**: Every key inside the segment starts with `spine_`; a bare `state:` key is a violation even if duplicated elsewhere.
- **V-017**: Keys are unique; duplicate keys are a violation (first-wins parsing is forbidden).
- **V-018**: `spine_schema` is exactly `v1` for a machine segment; a missing segment is `legacy`, not `v1`.
- **V-019**: `spine_state` belongs to `running/retrying/stalled/reentry-required/done`.
- **V-020**: `spine_stage`, when present, belongs to the eight known stage names.
- **V-021**: `spine_attempt` is a non-negative integer; `retrying` requires ≥1.
- **V-022**: `running` requires the four carrier paths and `spine_stage_deadline_epoch` (positive integer).
- **V-023**: `retrying` requires `spine_retry_reason` (non-empty) and `spine_attempt`.
- **V-024**: `stalled` requires `spine_stall_reason` and at least one non-empty `spine_evidence` pointer.
- **V-025**: `reentry-required` requires `spine_stage`, `spine_attempt`, `spine_last_verdict` and at least one evidence pointer.
- **V-026**: `done` requires `spine_stage`, `spine_attempt` and `spine_last_verdict`.
- **V-027**: `spine_last_verdict` belongs to the watcher verdict set `RUNNING/DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL`.
- **V-028**: `done` ⇒ `spine_last_verdict=DONE`; `retrying`/`stalled` ⇒ a present `last_verdict` that is not `DONE`; `running` ⇒ absent or `RUNNING`; `reentry-required` accepts any verdict.
- **V-029**: `spine_salvage=accepted` requires non-empty `spine_salvage_evidence` and `spine_salvage_at`; `none` or absence requires both keys absent.
- **V-030**: `spine_evidence` is a comma-separated list of at least one non-empty pointer; existence is not required (evidence may be archived remotely).
- **V-031**: A legacy/missing segment is reported as `schema=legacy/missing`; `snapshot` continues with `unknown`, `check-spine` fails.
- **V-032**: The engine never writes prose outside the fence and never rewrites unrelated keys.
- **V-033**: Recovery writes use temp-file + `os.replace` + fsync; a reader never observes a half-written segment.
- **V-034**: The segment MUST NOT reuse `<!-- test-budget:begin -->` or any other owner's fence.

### Watchbeat

- **V-035**: Filename is exactly `watchbeat-<line>-<stage>` under the state dir.
- **V-036**: The marker is one line; the last write wins atomically.
- **V-037**: Required fields `run`, `stage`, `window`, `at`, `event`; `window`/`at` are integers.
- **V-038**: Freshness is computed from `at` (not mtime) plus `window` plus the watcher's deadline grace; a future `at` yields age 0 and a `clock-skew` note, never a failure.
- **V-039**: A marker never feeds `loop_state`, `DONE`, liveness or the attempt counter.
- **V-040**: A legacy marker without `event` is attributable only by run/stage/mtime; it is never treated as proof of a watch window without the fresh test.

### Interruption and action

- **V-041**: Every finding form is from the closed eight-form set and carries evidence pointers.
- **V-042**: Multiple forms may coexist; the decision consumes all of them.
- **V-043**: `unwatched` requires live evidence (pid alive or fresh heartbeat) AND a missing/stale watchbeat.
- **V-044**: `deadline-overrun-live` requires `now ≥ deadline + grace`, live pid/heartbeat, and no terminal verdict; it never suggests a kill.
- **V-045**: `heartbeat-stalled` never changes `RUNNING`; the deadline remains the only timeout criterion.
- **V-046**: `artifacts-without-completion` requires all required artifacts present and no sentinel; the `loop_state` keeps its source verdict.
- **V-047**: `stale-signal` findings never contribute to the derived mapping.
- **V-048**: `lifecycle-spine-violation` requires `spine_state=running` with no live evidence, no fresh watchbeat and no terminal evidence (or a terminal `last_verdict` contradicting `running`).
- **V-049**: `remote-unreachable` never yields `DEAD` or a stage failure; it yields `STALLED` + `stop`.
- **V-050**: The action rule order is exactly `AD-1`–`AD-9`; the first matching rule wins and is reported.
- **V-051**: `none` requires `reason=not-dispatched`; it is never a fallback for unknown evidence.
- **V-052**: `stop` is returned for any decision branch that would otherwise guess; unknown evidence never produces `resume`/`retry`/`verify`.
- **V-053**: `watch/none/verify` bypass the attempt-limit rule; `resume/retry/stop` are not exempt.
- **V-054**: `resume` with a missing sentinel requires a valid `--salvage --evidence`; without it the action is `retry`.
- **V-055**: `resume` for implement is legal only when the code/test work is already committed; otherwise `retry`.
- **V-056**: A live-process `stop` carries `requires_explicit_decision=true` and the final watcher snapshot fields.
- **V-057**: Action adjudication under the lock re-evaluates the snapshot; if the action changed, the result is `refused(action-changed)` and no side effect occurs.

### Recovery execution

- **V-058**: Dry-run performs no write, commit, move, lock or counter change.
- **V-059**: `resume` stages explicit paths only; a path outside the stage map or an unmerged entry refuses the whole action.
- **V-060**: `resume` never re-dispatches, starts a subagent, writes artifact content or commits implement code.
- **V-061**: `retry` moves, never deletes; each moved file lands in the attempt directory with `os.replace`.
- **V-062**: `retry` increments the attempt only after every planned move succeeds; a partial batch reports `failed` and the moved list.
- **V-063**: `stop` writes `stalled` + `stall_reason` + evidence and a handoff; it never signals, kills, deletes or removes a worktree.
- **V-064**: `watch` writes only the watchbeat and never the spine or the attempt counter.
- **V-065**: `verify`/`none` write nothing, even with `--apply`; their result is `dry-run` with `applied=false`.
- **V-066**: Every mutating action writes its recovery record before the side effect and backfills the result after; a failure leaves a visible `failed` record.
- **V-067**: Repeated execution of the same applied action returns `already-applied` and produces no second commit, isolation batch or attempt increment.
- **V-068**: `--salvage` without `resume` is a usage error (exit 2); `--salvage` without a locatable `--evidence` is a refusal (exit 1).
- **V-069**: Evidence refs are locatable when a path exists or a 7–40 hex commit id resolves via `git cat-file -e`.
- **V-070**: The lock is acquired for every `recover --apply` (including `watch`); dry-run never locks; `verify/none` never lock.
- **V-071**: A second writer within the wait bound returns `locked` (exit 1) with `{pid,start,run_id,at}`; a stale lock is never auto-cleared.
- **V-072**: `--break-lock` moves the lock into `attempts/` and re-acquires; it never deletes it.
- **V-073**: The engine exits `0` for successful evaluation/application/`already-applied`/`action=stop`, `1` for refusal/validation/lock/failure, `2` for usage or unreadable required input.
- **V-074**: `--self-test` covers all eight forms plus stale pollution, artifact-complete-no-sentinel, dead-no-exit, sentinel-with-missing-artifact, live TIMEOUT, legacy spine, unreachable probe, lock and refusal paths.
- **V-075**: Handoff files are append-only records (one per stop event), never overwritten; the path is recorded in the spine.
- **V-076**: Multi-line invocations are independent; no cross-line inference, manifest or shared mutable aggregate is introduced.

### Artifact map and commits

- **V-077**: Artifact completeness uses existence + non-empty content only; log text never proves completeness.
- **V-078**: A sentinel without complete artifacts is `INCOMPLETE` (pseudo-completion), never `DONE`.
- **V-079**: Commit evidence uses `spine_stage_base_commit` as its only base; a missing base is `unknown`, never "latest commit".
- **V-080**: `commit_required=false` (analyze) records `not-applicable`; clarify without a change records `not-applicable`.
- **V-081**: Implement commit evidence scans commits after the base that touch non-`.specify/` paths; artifact completeness still requires `verification.md`.
- **V-082**: Uncommitted detection uses `git status --porcelain -- <paths>`; unrelated dirty files are neither listed nor committed.
- **V-083**: The Stage Artifact Map in code and in the owner reference are equal; a contract test pins every row.
- **V-084**: The map never adds a ninth stage or an implicit "all files" fallback.
