# Contract RC — Recovery Decision and Actions (`resume / retry / stop / watch / verify / none`)

**Owner**: `skills/external/sdd-loop-driver/references/state-awareness.md` § Recovery Actions.
**Scope**: the single-action adjudication and the exact side effects of each action. Defaults such as the retry ceiling and stage timeout are not owned here; they are read from `references/stage-prompts.md` § Stall Handling (RC-03).

## Decision

- **RC-01**: Every snapshot and recover output carries exactly one action from the closed set `none / watch / verify / resume / retry / stop`.
- **RC-02**: The action is adjudicated by the ordered table below; the first matching rule wins and its id (`AD-1`–`AD-9`) is reported. The table consumes the complete interruption list, never one form in isolation.
- **RC-03**: **AD-1** `reason=not-dispatched` ⇒ `none`. **AD-2** `remote-unreachable`, or `UNKNOWN` for any reason other than not-dispatched ⇒ `stop`. **AD-3** stale signals exist and cannot be isolated (state dir not writable, target collision unresolved) ⇒ `stop`. **AD-4** `RUNNING`, `unwatched`, or `deadline-overrun-live` ⇒ `watch`. **AD-5** `DONE` with complete artifacts and commit evidence `committed`/`not-applicable` ⇒ `verify`. **AD-6** the attempt count has reached the ceiling owned by `stage-prompts.md` ⇒ `stop` (this rule is evaluated only after AD-4/AD-5, so `watch`/`none`/`verify` are never limited). **AD-7** artifacts complete and the last log line does not start with `ANOMALY:` ⇒ `resume`, except: a missing sentinel without a valid recorded salvage ⇒ `retry`; implement whose code/test work is not already committed ⇒ `retry`. **AD-8** sentinel present with missing artifacts (pseudo-completion), or any other terminal state ⇒ `retry`. **AD-9** every remaining case ⇒ `stop`, never a guessed resume.
- **RC-04**: The same input produces the same action; only `evaluated_at` and `observed_at` may vary.
- **RC-05**: `requires_salvage=true` is set whenever AD-7 would need a salvage record; `requires_explicit_decision=true` is set for a live-process `stop` and for an unisolatable stale-signal `stop`. Neither flag changes the action by itself.

## `none`

- **RC-06**: `none` is legal only for `reason=not-dispatched`. It performs no write, lock, commit or process action and returns `applied=false`, `result=dry-run`.

## `watch`

- **RC-07**: `watch` refreshes the watchbeat marker with `event=watch-return` and hands control back to the driver, which must start the next watch window in the same turn.
- **RC-08**: `watch --apply` writes no spine, no recovery record and no attempt increment. It never commits or re-dispatches.
- **RC-09**: If a fresh marker already exists for the same run/stage, `watch --apply` returns `already-applied` without rewriting; otherwise it writes and returns `applied`. A dry-run only reports the planned refresh.

## `verify`

- **RC-10**: `verify` returns control to U4 and writes nothing, even with `--apply`. `loop_state=DONE` is a completion candidate, never "independently verified".

## `resume`

- **RC-11**: `resume` never re-dispatches, starts a subagent or writes artifact content. It may (a) commit existing uncommitted stage artifacts, (b) write the recovery record, and (c) hand control back to U4.
- **RC-12**: Only existing stage-owned paths are staged by explicit path. A path outside the Stage Artifact Map, an unmerged entry (`git ls-files -u`), or an unresolved conflict refuses the whole action (`result=refused`, exit 1); no partial commit occurs.
- **RC-13**: The commit message is `docs(<spec-key>): resume <stage> after interruption (run=<run_id> attempt=<n>)`; `spec-key` is the spec directory name. Implement code is never committed by resume.
- **RC-14**: Implement resume is legal only when the code/test work is already committed and only state advancement is missing; otherwise the action is `retry` (RC-03 AD-7).
- **RC-15**: A missing sentinel requires `--salvage --evidence <ref>`; `--apply` writes `spine_salvage: accepted`, `spine_salvage_evidence` and `spine_salvage_at` before the commit. Without it the action is `retry`.
- **RC-16**: The salvage exception is visible in the U4 conclusion and the closure summary; it is never silent.
- **RC-17**: If no stage artifact is uncommitted and no conflict exists, resume records the recovery and hands back to U4 without creating an empty commit.
- **RC-18**: Resume is idempotent: after a successful resume for the same run/attempt, a repeat returns `already-applied` and creates no second commit.

## `retry`

- **RC-19**: `retry` moves every status/pid/heartbeat/hook/watchbeat carrier of the old attempt into `<state-dir>/attempts/<attempt>-<run-id>-<epoch>/` with atomic per-file moves. Logs, worktrees and spec artifacts are never moved or deleted.
- **RC-20**: A carrier without a `run=` envelope is isolated as suspicious when it cannot be proven own; a carrier that is already absent is not an error.
- **RC-21**: Isolation targets use the next free sequence number; an existing attempt directory is never overwritten.
- **RC-22**: The attempt counter and `spine_state: retrying` are written only after every planned move succeeds. A partial move reports `result=failed` (exit 1) with `moved[]` and `remaining[]`, and does not increment the attempt.
- **RC-23**: `retry` never dispatches; the next dispatch remains the driver's U2. A successful retry leaves a clean signal surface for that dispatch.
- **RC-24**: Retry is idempotent: a repeat after a completed isolation for the same run returns `already-applied` and does not increment again.

## `stop`

- **RC-25**: `stop --apply` writes the spine to `stalled` with `spine_stall_reason`, evidence pointers and the recovery record, then creates a handoff file.
- **RC-26**: The handoff contains the four required elements: what was found (line/stage/state/forms/watcher fields), why it was expensive (deterministic root-cause class marked `derived=true`), every intermediate artifact locatable (spine, carriers, watchbeat, artifacts, commits), and 2–3 options.
- **RC-27**: The handoff carries `verdict`, `pid`, `heartbeat`, `rc`, `reason` and `grace_expired`, records `process_action=none`, and never sends a signal.
- **RC-28**: `stop` never kills a process, deletes evidence, removes a worktree or pushes. A live-process `TIMEOUT` reaches stop only after a final `--once` and an explicit user decision; the engine records `requires_explicit_decision=true` instead of deciding.
- **RC-29**: `stop` is a successful evaluation (exit 0) even though it mutates the spine; a failed handoff write is `result=failed` (exit 1) and leaves the failure visible.
- **RC-30**: The handoff path is stored in `spine_handoff_path`; handoff files are one per stop event and are never overwritten.
- **RC-31**: Stop is idempotent: a repeat when the spine is already stalled and the handoff exists returns `already-applied`; a missing handoff is re-created rather than reported as applied.

## Apply, failure and concurrency

- **RC-32**: Dry-run performs no write, commit, move, lock or counter change and emits the same action plus `steps[]`.
- **RC-33**: For `resume`, `retry` and `stop`, `--apply` writes the recovery record before the side effect and backfills `result` afterwards; a failure leaves a visible `failed` record with the failing step.
- **RC-34**: Every `recover --apply` acquires the per-line lock, re-evaluates the snapshot under the lock, and refuses with `action-changed` if the action no longer matches; no side effect occurs on refusal.
- **RC-35**: A second writer returns `locked` (exit 1) with holder metadata; a stale lock is never auto-cleared; `--break-lock` moves it into `attempts/` before re-acquiring.
- **RC-36**: Two lines recover independently; the engine writes only paths containing that line id and introduces no manifest, batch verdict or shared mutable aggregate.
- **RC-37**: Missing artifacts stay `missing`, unknown signals stay `unknown`, and an unresolvable branch becomes `stop` with a reason. The engine never fabricates evidence to reach a mutating action.
- **RC-38**: `already-applied` and `locked` are distinct: the former means the desired state already holds, the latter means another writer holds the lock. A concurrent write is never masked as `already-applied`.

## Clause → requirement map

| Clause | FR / SC |
|--------|---------|
| RC-01–RC-05 | FR-025, FR-026, FR-037 |
| RC-06–RC-10 | FR-033, FR-034, SC-003 |
| RC-11–RC-18 | FR-027, FR-028, FR-029, SC-003 |
| RC-19–RC-24 | FR-030, FR-031, SC-004 |
| RC-25–RC-31 | FR-032, FR-015, FR-050, SC-005 |
| RC-32–RC-38 | FR-035, FR-036, FR-037, FR-047, FR-048, FR-049, SC-009 |
