# Data Model — 066-loop-state-awareness-a

**Date**: 2026-10-21 | **Slice**: A (state awareness) of Feature 065
**Scope**: the projection this slice emits and the evidence it reads. Existing owners are not redefined: watch verdicts belong to `scripts/watch-target.sh` / `references/watch-model.md`; stall defaults, U4 and spine write points belong to `references/stage-prompts.md`; the plan-owned artifact set belongs to `references/efficiency-model.md` §3. The new owner reference `references/state-awareness.md` carries the numbered rule tables this model references.

## 1. Entities

| ID | Entity | Purpose |
|----|--------|---------|
| E-01 | Snapshot | The complete read-only projection returned by `--action snapshot` |
| E-02 | EvidenceSignal | One carrier's status, attribution, provenance and pointer |
| E-03 | StageArtifactSpec | One row of the eight-stage artifact map |
| E-04 | EffectiveValue | One resolved threshold/retry/attempt/sentinel value with its source |
| E-05 | InterruptionFinding | One annotation-only interruption form with evidence |
| E-06 | StaleSignal | One carrier excluded from evaluation with an attribution and reason |
| E-07 | RecoveryDecision | The advisory action, reason, detail and isolation flag |
| E-08 | RegistryView | The Registry entry status and projected digest |
| E-09 | SpineView | The state spine path, schema, state, consistency and fields |
| E-10 | ProbeEnvelope | A caller-collected snapshot-shaped input |
| E-11 | WatchbeatMarker | The driver's atomic window-presence marker |
| E-12 | CommitEvidence | The base commit, observed commits and uncommitted stage paths |

### E-01 Snapshot

| Field | Type / domain | Rule |
|-------|---------------|------|
| `schema_version` | integer `1` | Initial version; additive fields only |
| `action` | string `"snapshot"` | The only action implemented in this slice |
| `line_id` | string or `"unknown"` | Resolved per E-08/input order; never guessed |
| `run_id` | string or `"unknown"` | Probe → Registry → spine → unknown |
| `stage` | one of the eight stage names or `"unknown"` | Probe → Registry → spine → legacy stage → unknown |
| `loop_state` | `RUNNING/DONE/INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL/STALLED/REENTRY_REQUIRED/UNKNOWN` | Set only by watcher verbatim or the derived map |
| `verdict_source` | `"watcher"` or `"derived"` | `watcher` only when a watcher verdict is present |
| `watch_status` | `"available"` or `"unavailable"` | `available` only with a non-null watcher verdict |
| `watch_verdict` | verdict string or `null` | Verbatim from the watcher or probe |
| `watch` | object or `null` | Parsed watcher fields (no elapsed/at numbers) |
| `completion` | `complete/incomplete/unknown/not-applicable` | Independent of `loop_state` (see §3.2) |
| `recovery_action` | `none/watch/verify/resume/retry/stop` | Exactly one advisory action (see §3.3) |
| `recovery_reason` | stable snake-case token | Machine criterion; owner reference carries the closed set |
| `recovery_detail` | one sentence | Human explanation; not used by tests as a criterion |
| `isolation_required` | boolean | `true` only for a same-line stale-run driven retry |
| `spine` | E-09 | State spine projection |
| `registry` | E-08 | Registry projection |
| `evidence` | object of E-02 entries | Carrier, artifact and commit evidence |
| `effective` | object of E-04 entries | Resolved values and sources |
| `salvage` | object `{declared, evidence[], source}` | Read-only salvage input |
| `interruptions` | array of E-05 | Annotation only |
| `missing_artifacts` | array of repo-relative POSIX paths | Required stage artifacts absent or empty |
| `uncommitted_artifacts` | array of repo-relative POSIX paths | Stage-owned paths dirty in the working tree |
| `stale_signals` | array of E-06 | Non-own/stale carriers only |
| `evaluated_at` | ISO-8601 UTC `...Z` | The only field allowed to vary between identical inputs |

The reserved `recover` action, when invoked in this slice, returns the shared envelope `{schema_version, action:"recover", applied:false, result:"refused", steps:[], reason:"action-not-available-in-slice"}` with exit 2. This freezes the envelope shape required by FR-003 without implementing execution.

### E-02 EvidenceSignal

| Field | Type / domain | Rule |
|-------|---------------|------|
| `status` | `present/missing/na` | A signal that cannot be read is `missing`, never zero/ok |
| `attribution` | `own/stale-run/unattributed/foreign` | Envelope-first; only `own` participates |
| `evidence_source` | `local/probe` | Probe evidence never mixes with local evidence |
| `pointer` | absolute path or `null` | Carrier/status/log/spine/Registry pointer |
| `detail` | string or `null` | Additive one-line explanation (e.g. `artifact-map-unknown`) |

The concrete `evidence` keys are `pid`, `status`, `log`, `heartbeat`, `watchbeat`, `artifacts`, `commits`. Artifact and commit entries use `attribution="own"` because they are line-owned projections, not carrier envelopes; they still carry `status`, `evidence_source` and a `pointer` (the absolute spec directory or repo path, or `null` when unresolved).

### E-03 StageArtifactSpec

| Field | Type | Rule |
|-------|------|------|
| `stage` | one of the eight stage names | No ninth stage, no implicit fallback |
| `required` | array of spec-relative POSIX paths | Directory entries require at least one non-empty `.md` |
| `commit_required` | `true/false/conditional` | `conditional` only for clarify |
| `no_change_allowed` | boolean | `true` for clarify and analyze |
| `sentinel` | string or `null` | Uppercase stage + `-DONE`; owner: stage-prompts |
| `commit_scope` | array of spec-relative paths or `non-specify` | Implement uses `non-specify`; analyze uses `not-applicable` |

### E-04 EffectiveValue

| Field | Type | Rule |
|-------|------|------|
| `value` | integer/string/`null`/`"unknown"` | `null` only for an explicitly disabled sentinel |
| `source` | `cli/probe/spine/stage-map/watcher-help/unknown` | Every value names its source |

### E-05 InterruptionFinding

| Field | Type | Rule |
|-------|------|------|
| `form` | one of the eight closed forms | See §3.4 |
| `evidence` | array of absolute pointers | At least one pointer |
| `detail` | one sentence | States one fact; does not merge root causes |
| `attribution` | `own/stale-run/unattributed/foreign` | Matches the carrier(s) that produced the form |

### E-06 StaleSignal

| Field | Type | Rule |
|-------|------|------|
| `pointer` | absolute path | The excluded carrier |
| `attribution` | `own/stale-run/unattributed/foreign` | `own` is allowed only for a same-run carrier that predates `stage_started_at` |
| `reason` | `run-id-mismatch/before-stage-start/stage-mismatch/unprovable-envelope/legacy-stale` | Stable token; `legacy-stale` is the envelope-less legacy case required by the requirements |

The watcher's own `legacy` attribution class is normalized into the snapshot's four-value set: in the allowed single-active-line legacy mode an envelope-less carrier that can be proven current is `own`; otherwise it is `unattributed` with reason `legacy-stale`. The watcher's `legacy` literal is not added to the snapshot's attribution closed set.

### E-07 RecoveryDecision

The decision is exactly one of `none/watch/verify/resume/retry/stop` plus a reason token from the closed set. `isolation_required` is `true` only when a same-line `stale-run` drives a `retry`. The decision never mutates state in this slice.

### E-08 RegistryView

| Field | Type | Rule |
|-------|------|------|
| `status` | `found/missing/unreadable/invalid` | `unreadable` and `invalid` are not collapsed into `missing` |
| `entry` | object or `null` | Projected digest: line/run/stage/state/spine/status/log/heartbeat/worktree/repo/branch/identity |
| `pointer` | absolute path or `null` | The expected or existing `<line>.json` path |
| `error` | string or `null` | Read/parse error for `unreadable`/`invalid` |

### E-09 SpineView

| Field | Type | Rule |
|-------|------|------|
| `path` | absolute path or `null` | Explicit or Registry `spine_path` |
| `state` | `running/retrying/stalled/reentry-required/done/unknown` | Machine segment first; legacy downgrade second |
| `schema` | `v1/legacy/missing/unreadable` | A missing fence is `legacy`, not `v1` |
| `consistent` | `"true"/"false"/"unknown"` | String three-state; see §3.5 |
| `fields` | object | At least `stage_base_commit`, `last_verdict`, `stall_reason`, `retry_reason`; missing values are `"unknown"` |

Additive spine fields read when present: `stage`, `run_id`, `attempt`, `retry_limit`, `stage_started_at`, `stage_deadline_epoch`, `sentinel`, `salvage`, `salvage_evidence`, `salvage_at`.

`spine.consistent` is represented as the JSON strings `"true"`/`"false"`/`"unknown"` (assumption A-P6) so the field has one JSON type. A reader must not coerce `"false"` to a boolean.

### E-10 ProbeEnvelope

A probe is a snapshot-shaped document with `schema_version=1`. It may additionally carry `remote: {unreachable: true, reason: <string>}`. The engine never reads a local file for a probe field that is absent; it records `missing`/`unknown`. A probe's `watch_status=available` plus a non-null `watch_verdict` is a watcher verdict; a probe's derived verdict is re-evaluated locally and labelled `derived`.

### E-11 WatchbeatMarker

| Field | Type | Rule |
|-------|------|------|
| Path | `<state-dir>/watchbeat-<line>-<stage>` | Single-line, atomically replaced |
| `line` / `run` / `stage` | envelope strings | Required for `own` attribution |
| `window` | positive integer seconds | Owned by the writer; the snapshot uses it only for freshness |
| `at` | epoch seconds | Marker time; fallback to mtime if invalid |
| `event` | `watch-window/watch-return` | Window start or return |
| Snapshot projection | `status`, `attribution`, `pointer`, `at`, `window`, `event`, `freshness` | No age number; freshness is `fresh/stale/missing/unknown` (`unknown` when `effective.deadline_grace` is unavailable) |

### E-12 CommitEvidence

| Field | Type | Rule |
|-------|------|------|
| `base` | commit id or `"unknown"` | From `spine_stage_base_commit` only |
| `commits` | array of commit ids | Commits after base touching the stage paths |
| `uncommitted` | array of repo-relative paths | `git status --porcelain --untracked-files=all -- <stage paths>` |
| `state` | `committed/missing/not-applicable/unknown` | `not-applicable` when `commit_required=false` |

## 2. Stage Artifact Map (single owner in code + owner reference)

| Stage | Required (spec-relative) | `commit_required` | `no_change_allowed` | Sentinel | Commit scope |
|-------|--------------------------|-------------------|---------------------|----------|--------------|
| requirements | `requirements.md` | true | false | `REQUIREMENTS-DONE` | `requirements.md` |
| clarify | `requirements.md` | conditional | true | `CLARIFY-DONE` | `requirements.md` when changed |
| plan | `plan.md`, `research.md`, `data-model.md`, `contracts/` (≥1 `.md`), `quickstart.md`, `feature-ref.md` | true | false | `PLAN-DONE` | the six plan-owned paths |
| tasks | `tasks.md` | true | false | `TASKS-DONE` | `tasks.md` |
| checklist | `checklists/` (≥1 `.md`) | true | false | `CHECKLIST-DONE` | `checklists/` |
| analyze | none (sentinel + report in log are U4 evidence) | false | true | `ANALYZE-DONE` | not-applicable |
| implement | `verification.md`; code/test commits are commit evidence | true | false | `IMPLEMENT-DONE` | commits after base touching non-`.specify/` paths |
| review | `review.md` | true | false | `REVIEW-DONE` | `review.md` |

The sentinel column follows the stage-prompts convention (uppercase stage + `-DONE`); the owner reference states that a stage literal may be overridden by explicit `--sentinel`/`--no-sentinel`. The map is data in `loop-state.py` and the prose table in `references/state-awareness.md`; a contract test compares every row.

## 3. Rule Tables

### 3.1 Derived `loop_state` map (D1–D11)

This map runs only when no watcher/probe verdict exists. It is an independent aggregation mapping; it does not reproduce the watcher state machine and emits no watcher exit code.

| Rule | Condition (first match wins) | Result |
|------|------------------------------|--------|
| D1 | `spine.state=stalled` → `STALLED`; `spine.state=reentry-required` → `REENTRY_REQUIRED` | Same |
| D2 | `(exit record exists OR pid dead)` AND last non-empty log line starts `ANOMALY:` | `ANOMALY` |
| D3 | exit record `rc≠0` | `FAILED` |
| D4 | exit `rc=0`, artifacts complete, and (a required sentinel is present OR the sentinel is explicitly disabled) | `DONE` |
| D5 | exit `rc=0`, and ((a required sentinel is missing) or artifacts incomplete) | `INCOMPLETE` |
| D6 | no exit record, sentinel present: artifacts complete → `DONE`; artifacts incomplete → `INCOMPLETE` | `DONE`/`INCOMPLETE` |
| D7 | no exit record, pid record exists and pid state is dead/zombie/reused | `DEAD` |
| D8 | `stage_deadline_epoch` known, `now ≥ deadline + effective.deadline_grace`, no earlier terminal match | `TIMEOUT` (live process included) |
| D9 | no pid record and no exit record, `now − start_anchor ≥ effective.start_grace` | `NO_SIGNAL` |
| D10 | pid alive, or heartbeat fresh and pid is not dead, and no earlier terminal match | `RUNNING` |
| D11 | everything else | `UNKNOWN` |

If sentinel configuration is `unknown`, an exit `rc=0` cannot decide D4/D5/D6 and falls through to D11. If `start_anchor` or `start_grace` is unknown, D9 is skipped (D11). `start_anchor` is `stage_started_at` when known, otherwise the earliest mtime of an attributable carrier.

### 3.2 Completion map

| Condition (first match wins) | `completion` |
|------------------------------|--------------|
| not-dispatched predicate true | `not-applicable` |
| exit record `rc≠0` | `incomplete` |
| sentinel required and present, artifacts complete, and (no exit record or `rc=0`) | `complete` |
| sentinel required and present, artifacts incomplete | `incomplete` |
| sentinel required and missing | `incomplete` |
| sentinel disabled (`--no-sentinel`), exit `rc=0`, artifacts complete | `complete` |
| sentinel disabled, exit `rc=0`, artifacts incomplete | `incomplete` |
| sentinel disabled and no exit record | `unknown` |
| sentinel configuration unknown, or artifacts cannot be evaluated | `unknown` |

`completion` never writes or changes `loop_state`. A pseudo-completion (sentinel present, artifacts missing) is `incomplete` with the watcher/derived `loop_state` preserved.

### 3.3 Action decision table (A1–A10)

The order is the FR-003 order. The two bounded guards are stated with A3 and A4.

| Rule | Condition | Action | Reason |
|------|-----------|--------|--------|
| A1 | not-dispatched predicate | `none` | `not-dispatched` |
| A2 | `UNKNOWN` (non-not-dispatched), `remote-unreachable`, `lifecycle-spine-violation`, or stale signals that cannot be attributed and leave no own evidence | `stop` | `evidence-insufficient` / `remote-unreachable` / `lifecycle-spine-violation` / `stale-signal-unattributable` |
| A3 | `attempt` and `retry_limit` known and `attempt ≥ retry_limit`, and the candidate from A4–A10 would be `resume`/`retry`/`stop` | `stop` | `retry-limit-reached` (`watch`/`none`/`verify` are never limited) |
| A4 | same-line `stale-run` exists, the current attempt is not provably running, and `completion≠complete` | `retry` | `stale-signal-attributed`; `isolation_required=true` |
| A5 | `loop_state=RUNNING`, `unwatched` form, or `deadline-overrun-live` form | `watch` | `running` / `unwatched` / `deadline-overrun-live` (`state-dir-unknown` when the marker path is unknown) |
| A6 | `completion=complete` and artifacts/commit complete (`committed` or `not-applicable`) | `verify` | `complete-verified` |
| A7 | `completion=complete`, commit evidence `missing`, non-implement stage that allows a recovery commit | `resume` | `commit-missing` |
| A8 | artifacts complete, no positive completion evidence (sentinel missing or exit `rc≠0`), valid salvage input, non-implement stage | `resume` | `salvage-accepted` |
| A9 | pseudo-completion, other terminal states, or artifacts complete without salvage input | `retry` | `pseudo-complete` / `no-positive-evidence` / `retry-limit-unknown` when the limit is unknown |
| A10 | everything else | `stop` | `other` |

A live `TIMEOUT` reaches A5 (`deadline-overrun-live`) and is `watch`, never `stop`. A3 is a guard on the candidate, not an earlier unconditional branch; A4 is likewise guarded so a running or complete current attempt keeps A5/A6. The reason token set is owned by `references/state-awareness.md` and includes the tokens named in the slice requirements.

### 3.4 Interruption forms (I1–I8, annotation only)

| Form | Condition | Annotation |
|------|-----------|------------|
| I1 `unwatched` | stage running (pid alive, or heartbeat fresh with pid not dead) and watchbeat missing/non-own/older than `window + effective.deadline_grace`; a marker whose freshness is `unknown` does not fire this form | Never sets `loop_state`; drives `watch` |
| I2 `dead-no-exit-record` | pid record exists, pid dead/zombie/reused, no exit record, no sentinel | Never sets `loop_state` |
| I3 `deadline-overrun-live` | deadline known, `now ≥ deadline + deadline_grace`, pid alive or (heartbeat fresh and pid not dead), no terminal match | Annotates; live `TIMEOUT` action is `watch` |
| I4 `heartbeat-stalled` | pid alive, heartbeat present, freshness `stale` (not `unknown`), no terminal match | Annotates; `loop_state` stays `RUNNING` |
| I5 `artifacts-without-completion` | artifacts complete and sentinel missing (exit record may exist, any rc) | Drives completion only |
| I6 `stale-signal` | any `stale_signals[]` entry exists | One finding per attribution present; never sets state |
| I7 `lifecycle-spine-violation` | Registry entry exists but spine missing/unreadable/invalid; or spine says running while no live process, no fresh heartbeat and no terminal evidence | Annotates; evidence gap recommends `stop`. This is the interruption form, not the out-of-scope `check-spine` validator |
| I8 `remote-unreachable` | probe carries `remote.unreachable=true` | Annotates; never `DEAD` |

Forms are ordered I1–I8; within a form, attributions are ordered `own`, `stale-run`, `foreign`, `unattributed`. Every form carries at least one absolute evidence pointer.

### 3.5 `spine.consistent` three-state

| Condition | Value |
|-----------|-------|
| `last_verdict` missing/`unknown` | `"unknown"` |
| final `loop_state` is `STALLED`/`REENTRY_REQUIRED`/`UNKNOWN` | `"unknown"` |
| both are in the watcher verdict set and equal | `"true"` |
| both are in the watcher verdict set and differ | `"false"` |

`stalled`/`retrying` without `last_verdict` is not `"false"`. The value is a JSON string to keep one type across the three states.

### 3.6 Effective value resolution

| Key | Priority |
|-----|----------|
| `start_grace` | CLI → probe → spine `spine_start_grace` → watcher `--help` |
| `deadline_grace` | CLI → probe → spine `spine_deadline_grace` → watcher `--help` |
| `heartbeat_max_age` | CLI → probe → spine `spine_heartbeat_max_age` → watcher `--help` |
| `retry_limit` | CLI → probe → spine `spine_retry_limit` → unknown |
| `attempt` | CLI → probe → spine `spine_attempt` → unknown |
| `sentinel` | CLI (`--sentinel`/`--no-sentinel`) → probe → spine `spine_sentinel` → stage map → unknown |

A value whose source is unavailable is `"unknown"`; a decision that depends on it reports `UNKNOWN` or skips the rule, never a hardcoded default.

### 3.7 Not-dispatched predicate

Not-dispatched is true only when no dispatch evidence exists:

- the spine has no machine segment carrying `spine_stage_started_at`/`spine_stage_deadline_epoch`, and no readable legacy stage/checkpoint line;
- the Registry entry has no non-empty `stage` bound to stage runtime paths or a dispatch `last_event` (the auto-generated registration `run_id` alone does not count);
- there are no attributable carriers and no watcher/probe verdict.

Registration alone is not dispatch evidence. A readable legacy stage/checkpoint is dispatch evidence, even if its timing fields are missing (then `unknown`). The Registry-present/spine-missing path is evaluated before this predicate.

### 3.8 Registry/spine precedence

| Registry file | Spine | Watcher/probe verdict | Result |
|---------------|-------|-----------------------|--------|
| missing/unreadable/invalid | readable | any | Continue; `registry.status` preserved; no `UNKNOWN` solely for Registry |
| missing/unreadable/invalid | missing | none | Not-dispatched (`UNKNOWN`, `none`) when no other dispatch evidence |
| found (or file exists) | missing/unreadable/invalid | none | `UNKNOWN` + `stop`; form `lifecycle-spine-violation`; `stage=unknown` when unavailable |
| found (or file exists) | missing/unreadable/invalid | present | `loop_state` verbatim; form `lifecycle-spine-violation`; action `stop`; `stage=unknown` when unavailable |

### 3.9 Stale-signal attribution

A carrier is `own` only when its envelope proves line, run and stage. A same-run own carrier whose mtime precedes `stage_started_at` is excluded and recorded with `attribution="own"`, `reason="before-stage-start"`; it does not by itself change the action. `foreign`/`unattributed` carriers never change the action. A same-line `stale-run` may drive `retry` under the A4 guard. Legacy mode (no envelope) is allowed only for a single active line; with multiple active lines, an envelope-less carrier is `unattributed`. An envelope-less legacy carrier that cannot be proven current is recorded with reason `legacy-stale`; the watcher's `legacy` attribution literal is normalized into the snapshot's four-value set. Without a readable Registry proving exactly one active line, an envelope-less carrier is `unattributed` rather than legacy-own.

## 4. Validation Rules

### Snapshot shape and determinism

- **V-001**: `schema_version` is exactly `1`.
- **V-002**: `action` is exactly `"snapshot"`; `recover`/`check-spine` are not available in this slice.
- **V-003**: `loop_state` belongs to the closed set; no other casing or synonym.
- **V-004**: `verdict_source="watcher"` implies `watch_status="available"` and `loop_state` equals `watch_verdict` verbatim.
- **V-005**: `verdict_source="derived"` implies no watcher/probe verdict is present.
- **V-006**: `recovery_action` belongs to the closed set and appears exactly once.
- **V-007**: Every evidence signal has `status ∈ present/missing/na`, an attribution from the closed set and an absolute pointer or `null`.
- **V-008**: A missing signal is `missing`/`unknown`/`null`; zero, empty string and `ok` never stand in.
- **V-009**: `evaluated_at` is the only field allowed to vary between two identical-input runs.
- **V-010**: The snapshot contains no heartbeat age, elapsed time or other derived duration number.
- **V-011**: Lists are ordered: interruptions I1–I8 then attribution order; stale signals by pointer; artifacts by stage-map order.
- **V-012**: Unknown top-level fields are allowed for forward readers but are never required by this slice.

### Loop state and completion

- **V-013**: `loop_state` is set only by the watcher/probe verdict or the derived map.
- **V-014**: No interruption form may set, override, downgrade or upgrade `loop_state`.
- **V-015**: `completion` is computed independently and never writes `loop_state`.
- **V-016**: A pseudo-completion (sentinel present, artifacts missing) yields `completion=incomplete`, never `complete`.
- **V-017**: `completion=complete` requires artifacts complete and positive completion evidence (sentinel, or disabled sentinel plus exit `rc=0`).
- **V-018**: `commit_required=false` never makes `completion` incomplete for a missing commit.
- **V-019**: When sentinel configuration is unknown, `completion` is never `complete`.
- **V-020**: `completion=not-applicable` only when the not-dispatched predicate is true.

### Spine

- **V-021**: A machine segment is delimited by one `<!-- loop-state:begin -->`/`<!-- loop-state:end -->` pair and declares `spine_schema: v1`.
- **V-022**: Machine keys use the `spine_` prefix; a bare `state:` key is never read as a machine state.
- **V-023**: A missing fence is `schema="legacy"`, not `"v1"`.
- **V-024**: `spine.state` belongs to `running/retrying/stalled/reentry-required/done/unknown`.
- **V-025**: `spine.fields` exposes at least `stage_base_commit`, `last_verdict`, `stall_reason`, `retry_reason`; missing values are `"unknown"`.
- **V-026**: A missing `stage_base_commit` yields `commit=unknown`, never a guessed base.
- **V-027**: `stalled`/`retrying` with no `last_verdict` does not force `spine.consistent="false"`.
- **V-028**: `spine.consistent` is one of `"true"/"false"/"unknown"` and follows §3.5.
- **V-029**: Legacy parsing only recognizes explicit stage/checkpoint/tries/state/timing lines; anything else is `unknown`.
- **V-030**: A legacy stage/checkpoint line is dispatch evidence; absence of timing fields does not make it not-dispatched.

### Registry and inputs

- **V-031**: `registry.status` is one of `found/missing/unreadable/invalid`; unreadable and invalid are not merged into missing.
- **V-032**: Registry present + spine missing/unreadable + no watcher/probe verdict yields `loop_state=UNKNOWN`, `recovery_action=stop`, form `lifecycle-spine-violation`.
- **V-033**: Registry present + spine missing/unreadable + watcher/probe verdict yields the verbatim verdict, form `lifecycle-spine-violation` and action `stop`; `stage="unknown"` when the envelope is unavailable.
- **V-034**: Registry missing/unreadable/invalid + readable spine/carriers continues evaluation; it does not force `UNKNOWN`.
- **V-035**: The registration `run_id` alone is not dispatch evidence.
- **V-036**: `line_id` is `--line-id` or the probe's line id; absent both is exit 2.
- **V-037**: `spec-dir` absent is `unknown`; artifacts cannot be evaluated and `completion` is not `complete`.
- **V-038**: `repo` is explicit or from the Registry; no current-working-directory fallback.
- **V-039**: A probe field that is absent is `missing`/`unknown`; the engine never reads a local file in its place.
- **V-040**: Probe evidence is labelled `evidence_source="probe"`; local evidence is `"local"`.

### Carriers and attribution

- **V-041**: `own` requires the carrier's own line, run and stage envelope to match.
- **V-042**: `foreign`, `stale-run`, `unattributed` and own-before-stage-start carriers never participate in evaluation.
- **V-043**: Non-own carriers appear only in `stale_signals[]` and, when `stale-signal` is emitted, in its evidence.
- **V-044**: Legacy attribution is allowed only for a single active line; multiple active lines make an envelope-less carrier `unattributed`.
- **V-045**: A stale-run carrier with the same line may drive `retry` only under the A4 guard; `foreign`/`unattributed` never change the action.
- **V-046**: A carrier path that cannot be read is `missing`, not `na`, unless the stage never configures it.

### Interruptions

- **V-047**: `form` belongs to the closed set; one form per attribution present, no duplicate form/attribution pair.
- **V-048**: I1 `unwatched` requires the stage to be running and the watchbeat missing/non-own/stale; a fresh marker after a normal window expiry does not fire.
- **V-049**: I2 `dead-no-exit-record` requires no sentinel; a sentinel routes to completion.
- **V-050**: I3 `deadline-overrun-live` only annotates; a live `TIMEOUT` action is `watch`.
- **V-051**: I4 `heartbeat-stalled` keeps `loop_state=RUNNING` when no terminal signal exists.
- **V-052**: I5 `artifacts-without-completion` fires when artifacts are complete and the sentinel is missing, regardless of the exit record.
- **V-053**: I7 `lifecycle-spine-violation` is emitted for the Registry-present/spine-missing path and for a running spine contradicted by dead/no-heartbeat/no-terminal evidence. It is an annotation form; the deterministic `check-spine` validator is out of scope.
- **V-054**: I8 `remote-unreachable` never yields `DEAD` or a stage-failure verdict.

### Watchbeat and effective values

- **V-055**: The marker path is `<state-dir>/watchbeat-<line>-<stage>`.
- **V-056**: `state-dir` resolves explicit → parent of `--spine` → parent of the Registry `spine_path`; unresolved means marker `missing` and reason `state-dir-unknown`.
- **V-057**: Marker freshness uses `window=` + `effective.deadline_grace`; the marker never participates in completion or liveness.
- **V-058**: `effective.<key>` is `{value, source}`; an unavailable value is `"unknown"` and its dependent decision is `UNKNOWN` or skipped.
- **V-059**: Watcher thresholds are parsed from the current `--help` output, never copied as literals.
- **V-060**: A retry-limit decision with unknown `attempt` or `retry_limit` is skipped; a retry reason records `retry-limit-unknown`.

### Commit evidence

- **V-061**: Commit checks are read-only git queries against the explicit/Registry repo; a missing git, repo or base yields `commit=unknown`, never a guessed commit.

## 5. State Transitions

This slice has no persistent state transitions. The only transition-shaped outputs are the projection's decision labels:

```text
evidence → loop_state (watcher verbatim | derived D1–D11)
evidence → completion (independent table)
loop_state + completion + forms + attempts + salvage → recovery_action (A1–A10)
```

No path writes the state spine, carriers, Registry, worktree or git history.
