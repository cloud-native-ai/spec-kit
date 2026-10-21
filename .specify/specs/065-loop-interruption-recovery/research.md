# Research — Feature 065 Loop Interruption Awareness & Recovery

**Date**: 2026-10-21 | **Baseline**: `de56646301ab112447254745b091b26bcc78daf1` on `065-loop-interruption-recovery` | **Spec**: [requirements.md](requirements.md)

Phase 0 resolves how the new observation/recovery layer attaches to the existing 058/063/064 mechanisms without changing any of their owners. Every fact below was measured against the current tree; commands and outputs are pasted from the runs.

## 0. Measured baseline

### 0.1 Environment

```text
$ git rev-parse HEAD
de56646301ab112447254745b091b26bcc78daf1
$ python3 --version
Python 3.9.6
$ uname -sm
Darwin arm64
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version
pytest 9.1.1
```

The repo-local `.venv` contains Python 3.14.6 but no pytest; the usable pytest is the profiles virtualenv (`pytest 9.1.1`). Implementation MUST use that interpreter for the suite and record the interpreter in the evidence file.

### 0.2 Watcher regression baseline

```text
$ bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
SELF-TEST: 38 passed, 0 failed
```

This is the zero-difference baseline for FR-038: the 38 cases (including zero-match, zombie, PID reuse, fake-done, attribution, hook, stream) must stay green and their verdict/exit-code pairs must not change.

### 0.3 Existing test baselines

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/unit/test_line_registry_engine.py tests/unit/test_decomposition_check.py
31 passed in 1.04s

$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_sdd_loop_driver_skill.py
2 failed, 23 passed in 24.75s
FAILED test_c18_mirror_pair_no_drift
FAILED test_c12_mirror_byte_identical
```

The two failures are pre-existing mirror drift, not behavioral regressions (see 0.4).

### 0.4 Mirror baseline (before any edit)

```text
$ python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
DIFF  .specify/skills/sdd-loop-driver/SKILL.md
DIFF  .specify/skills/sdd-loop-driver/references/cli/hermes.md
DIFF  .specify/skills/sdd-loop-driver/references/cli/index.md
DIFF  .specify/skills/sdd-loop-driver/references/dispatch-recipes.md
DIFF  .specify/skills/sdd-loop-driver/references/efficiency-model.md
DIFF  .specify/skills/sdd-loop-driver/references/stage-prompts.md
DIFF  .specify/skills/sdd-loop-driver/references/watch-model.md
DIFF  .specify/skills/sdd-loop-driver/scripts/admission-check.py
DIFF  .specify/skills/sdd-loop-driver/scripts/overlap-check.py
DIFF  .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py
DIFF  .specify/skills/sdd-loop-driver/scripts/watch-hook.sh
DRIFT detected — run: python3 scripts/python/sync-mirrors.py --write
EXIT=2
```

Criterion for this spec: **no NEW drift**, and because the 11 differing files are all inside the pair this spec edits, the intended end state is zero drift for the whole pair after `--write` (disclosed in plan.md Mirror Obligations). The source tree is canonical; the write direction is source → runtime mirror.

### 0.5 Plan-entry decomposition gate

```text
{"mode": "plan", "decision": "split-required",
 "measured": {"fr_count": 52, "task_count": null, "fr_ceiling": 30, "task_ceiling": 40},
 "reasons": ["FR definitions=52 exceeds ceiling 30"]}
```

The gate record is [notes/decomposition-gate.md](notes/decomposition-gate.md). The upstream driver dispatched this plan for the full feature; the dispatch is recorded as the §5.3.3 confirmation (see §6 below). Plan targets a task decomposition of at most 40 task rows; `tasks` U4 must re-run the gate and, if it still returns `split-required`, the driver must either split or record a further explicit upstream decision before `analyze`.

## 1. Code facts that shape the design

| Fact | Evidence | Design consequence |
|------|----------|--------------------|
| Watcher owns verdicts and exit codes 0/10–16; `--once` returns one `WATCH …` line plus `EVIDENCE …` for terminal verdicts | `scripts/watch-target.sh` (`EXIT_*`, `format_verdict`, `emit_single`) | `loop-state.py` consumes `--once` output; it never re-implements the verdict state machine and never emits 10–16 |
| Watcher defaults are published in `--help` (`Defaults: window=200s, interval=3s, start-grace=30s, deadline-grace=120s, heartbeat-max-age=120s`) | `scripts/watch-target.sh` usage block | Thresholds are resolved from that help text (or explicit flags); the new engine does not define a second copy |
| Watcher attribution requires BOTH `line=` and `run=` in a carrier; missing either → `unattributed` and the carrier is ignored | `classify_pair` in `watch-target.sh` | `loop-state.py` must choose legacy vs attributed watcher invocation; passing `--run-id` at a 063-style file set would silently hide the status |
| `stage-runner.sh` writes status/pid/heartbeat with `line=`/`stage=` but **no** `run=`; `run-stage.sh` writes `run=` too | `stage-runner.sh:113,114,241`; `run-stage.sh:125,152,198` | Attribution cannot assume `run=`; a file without it is own only when it can be proven (matching line/stage + mtime ≥ `stage_started_at` + registry PID identity); otherwise it is a suspect stale signal |
| `line-registry.py --action reattach-brief` aggregates registry, spine (`state` + last line), four-piece existence, heartbeat age, reservation and lease | `line-registry.py:2280` | Reused as a registry read path only; it neither becomes the aggregator nor gains recovery actions |
| `line-registry.py` consistency check reads the FIRST `^\s*state\s*[:=]` line of the spine | `line-registry.py:474-493` | The machine segment MUST use `spine_state:`; a bare `state:` inside the fence is a validation failure |
| Stage artifact ownership: plan-owned set is `plan.md,data-model.md,contracts/,quickstart.md,research.md,feature-ref.md`; analyze produces no commit; U4 artifact expectations live in stage-prompts | `efficiency-model.md` §3.1; `stage-prompts.md` § Independent Verification | The Stage Artifact Map is data in code plus one section in the new owner reference, aligned with those owners |
| The existing spine is free-form prose; its fields are written at U0/U2/U3/U4/U5 | `stage-prompts.md` § Stall Handling & State Spine | Add a bounded fenced machine segment; prose stays untouched; legacy spines degrade to `unknown` |

## 2. Decisions

### D-01 — One new engine, three actions, one owner reference

Create `scripts/loop-state.py` (Python 3.8+ stdlib) with `--action snapshot|recover|check-spine` and `--self-test`; create `references/state-awareness.md` as the single owner of the new awareness/interruption/recovery rules. `watch-model.md` remains the sole owner of watch verdicts; `stage-prompts.md` remains the owner of stall defaults, U3/U4/U5 procedure and the spine write points; `efficiency-model.md` remains the owner of the plan-owned artifact set. The new reference points at them and never copies their tables or numeric defaults.

Rejected: extending `line-registry.py` (its domain is registration/ownership/lease, it is already ~2.5k lines, and mixing a read-only projection plus mutating recovery into it would blur two owners); reimplementing the watcher state machine (forbidden by FR-005).

### D-02 — Watcher delegation with explicit attribution mode

Snapshot obtains the watch verdict by invoking `watch-target.sh --once` with the same four-piece paths, sentinel and deadline. It passes `--line-id/--run-id` only when a Registry entry exists for the line and the evidence carriers are attributable (at least one existing carrier carries `run=`); otherwise it invokes legacy mode and records `attribution=legacy`. If the environment has more than one active Registry line and the target line cannot be attributed, `watch=unavailable(reason=attribution-required-multi-line)` and the derived mapping is used — never a guessed watcher verdict. A probe snapshot bypasses invocation entirely.

The aggregator's `loop_state` is copied verbatim from the watcher verdict when a verdict is present (`verdict_source=watcher`). `verdict_source=derived` is used only when no verdict exists, and the output carries the derived rule id.

Rejected: always passing attribution parameters (breaks 063-style carriers); always running legacy (unsafe in multi-line environments).

### D-03 — Thresholds are read from the watcher, never restated

`loop-state.py` resolves `deadline-grace`, `heartbeat-max-age` and `start-grace` in this order: explicit CLI flag → parse the `Defaults:` line of `watch-target.sh --help` → `unknown`. If `unknown`, threshold-dependent findings (`watchbeat stale`, `heartbeat-stalled`, `deadline-overrun-live`) are suppressed and the evidence object records `threshold=unknown`; the engine never invents a number. Contract tests parse the same help text and assert the engine's resolver agrees with the script.

Rejected: duplicating 120/120/30 constants in the new engine (one-source-of-truth violation); adding a new `--print-defaults` flag to the watcher (FR-038 forbids touching its interface semantics).

### D-04 — Derived loop_state is a numbered, testable mapping

The owner reference defines rules `D0`–`D8` in a fixed order: D0 not-dispatched → `UNKNOWN(reason=not-dispatched)`; D1 spine `stalled`/`reentry-required`; D2 exit-record/ANOMALY/FAILED/DONE/INCOMPLETE; D3 sentinel-only; D4 dead-without-exit; D5 deadline overrun (including a live process); D6 no-signal; D7 running; D8 unknown. The code exposes `derived_rule` in every derived snapshot and carries the same rule ids as constants. A contract test extracts the ids from the owner reference and asserts they equal the code constants and the FR-004 order.

D0 is a design addition required by A-14: a line that was never dispatched must not be reported as `NO_SIGNAL` merely because the start grace elapsed. It fires only when the spine has no `stage_started_at`, no carrier and no sentinel.

### D-05 — Evidence attribution and stale-signal rules

A carrier (status/pid/heartbeat/hook/watchbeat) is **own** when either (a) its `run=` envelope equals the current run and its `line=`/`stage=` match, or (b) it has no `run=` but its line/stage match, `stage_started_at` is known, its mtime is not earlier than `stage_started_at`, and — when the Registry has a runner/cli PID — its PID matches that identity. It is **stale** when the current run is known and either the envelope mismatches, the mtime predates `stage_started_at`, or the carrier cannot be proven own. If no current run is known, attribution is `unknown` and no stale finding is invented.

Stale carriers never feed the derived mapping. They are listed in `stale_signals[]` with `kind` and reason, and `retry` isolates them. This is what closes the measured accident's old-status contamination.

Rejected: treating every no-`run=` file as stale (would quarantine legitimate 063-style evidence on every recovery); trusting mtime alone (a copied/restored file would masquerade as current).

### D-06 — Eight interruption forms, multiple findings, one action

The forms are exactly the FR-009 closed set, coded `I1`–`I8` and emitted in that order. They are computed independently and all matching forms are reported; no form suppresses another. The suggested spine write is carried per finding (`suggested_spine_state`) but the recovery action is adjudicated once from the full snapshot (D-07).

`unwatched` is decided only from file evidence: a stage with live evidence (pid alive or fresh heartbeat) and no fresh watchbeat. `deadline-overrun-live` is `now ≥ deadline + grace` with live pid/heartbeat and no terminal verdict. `heartbeat-stalled` is a warning and never changes `RUNNING` to `STALLED`/`TIMEOUT`. The other five follow FR-014/017/018/021/024.

### D-07 — Recovery action adjudication (fixed priority)

The owner reference carries the ordered decision table; the code implements it as one function returning `(action, reason, rule_id)`. Priority: D0 → `none`; remote-unreachable/UNKNOWN → `stop`; stale signals present and not isolatable → `stop`; attempt limit reached → `stop` for `resume/retry/stop` (never for `watch/none/verify`); live/unwatched/deadline-live → `watch`; `DONE` with artifacts and commit complete → `verify`; artifacts complete and last line not `ANOMALY:` → `resume`, except (a) a missing sentinel without a recorded `--salvage` → `retry`, (b) implement with uncommitted code → `retry`; everything else terminal → `retry`.

`stop` is also the sink for every unknown branch (FR-037). No action ever kills a process or deletes evidence.

### D-08 — `resume` commits only stage-owned paths

Resume preflights: no unmerged entries (`git ls-files -u -- <paths>`), no path outside the stage artifact map, and only existing/uncommitted files are staged by explicit path. Commit message: `docs(<spec-key>): resume <stage> after interruption (run=<run_id> attempt=<n>)`. It never starts a subagent, never writes artifact content and never re-dispatches; control returns to U4. Clarify with no change is `not-applicable`; analyze never commits; implement is never auto-committed — its resume is limited to state advancement after the work is already committed (FR-029).

Rejected: `git add -A` (would capture unrelated dirty files, the exact accident hazard); committing implementation code (FR-029/FR-049).

### D-09 — `retry` isolates, never deletes

Retry moves status/pid/heartbeat/hook/watchbeat carriers of the old attempt into `<state-dir>/attempts/<attempt>-<run-id>-<epoch>/` with `os.replace` (same filesystem, atomic per file). Existing target directories get the next sequence number; no file is deleted or truncated. The attempt counter increments only after every planned move succeeds; a partial move is reported as `failed` with the moved list and no increment. Logs and worktrees are never moved.

### D-10 — `stop` writes a handoff, not a kill

Stop writes the spine to `stalled` with `stall_reason` and evidence pointers, then atomically creates `<state-dir>/handoff-<line>-<stage>-a<attempt>-<epoch>.md` containing the four required elements (what was found, why it was expensive, every intermediate artifact locatable, 2–3 options), plus the watcher snapshot fields (`verdict/pid/heartbeat/rc/reason/grace_expired`). It never sends a signal, removes a worktree or deletes evidence. A live-process TIMEOUT only reaches stop after a final `--once` and an explicit user decision — the engine is not that decision-maker and records `requires_explicit_decision=true` instead of acting.

### D-11 — Watchbeat is a presence marker, not a verdict

`watchbeat-<line>-<stage>` is one atomic-overwrite line: `run=<run_id> stage=<stage> window=<seconds> at=<epoch> event=watch-window|watch-return`. Freshness = `now - at ≤ window + deadline-grace` (both values from the marker/watcher owner). It never participates in completion or liveness, and `RUNNING` windows still do not write the spine. The driver writes it at every window start/return; `recover --action watch --apply` refreshes it and returns control. If the existing marker is already fresh for the same run/stage, it returns `already-applied` without rewriting.

### D-12 — Spine machine segment: additive, fenced, validator-enforced

Fence `<!-- loop-state:begin -->` … `<!-- loop-state:end -->`; keys are `key: value` with a mandatory `spine_` prefix; `spine_schema: v1`; state key is `spine_state:` only. The segment is appended/replaced atomically by recovery, and by the driver at U0/U2/U3/U4/U5. Prose outside the fence is untouched. Snapshot degrades a legacy spine (`schema=legacy`) to `unknown` fields and never guesses. `check-spine` fails a legacy/missing segment (exit 1) because its contract is to enforce the new schema, while snapshot continues to be usable for recovery triage.

### D-13 — Recovery lock: exclusive file, bounded wait, explicit break

`<state-dir>/recover-<line>.lock` is created with `O_CREAT|O_EXCL` and carries holder pid/start token/run_id/at/action/stage. A second writer waits `--lock-wait` seconds (default bounded) then returns `result=locked` (exit 1) with holder metadata. A stale lock is never auto-cleared; `--break-lock` moves it into `attempts/` and retries acquisition. The lock is released on normal exit; a dead holder leaves the explicit break path.

### D-14 — Probe input is a snapshot or an unreachable envelope

`--probe FILE` accepts either (a) a snapshot JSON produced by a remote `loop-state.py snapshot` (its `evidence_source` is already `probe`), or (b) `{"schema_version":1,"reachable":false,"reason":"…"}`. Case (b) produces `loop_state=STALLED`, `interruptions=[remote-unreachable]`, `recovery_action=stop`, and never `DEAD`. A malformed probe is exit 2, not a guessed state. When a probe is supplied, no local watcher is invoked and the top-level `evidence_source=probe`.

### D-15 — Determinism: no time-varying numbers in the stable core

Snapshot emits no `age_seconds` or elapsed values; it emits `mtime` (stable), booleans (`fresh`), threshold provenance and `evaluated_at`/`observed_at` timestamps. Two snapshots of the same file state therefore differ only in timestamp fields; the derived rule, findings, action and ordering are stable. Arrays are emitted in map/rule order, and JSON keys are sorted.

### D-16 — Distribution and task budget

Deliverables: `SKILL.md`, new `references/state-awareness.md`, new `scripts/loop-state.py`, targeted edits to `references/stage-prompts.md` and `references/dispatch-recipes.md`, the docs page, the new unit/contract/integration tests, and the existing skill contract test's pinned H2/mirror lists. The runtime mirror is regenerated, never hand-edited. The plan is structured so `/speckit.tasks` can stay at or below 40 task rows (test matrix consolidated per file); `tasks` U4 re-runs the gate.

## 3. Rejected alternatives

| Alternative | Why rejected |
|-------------|--------------|
| Extend `line-registry.py` with snapshot/recover | Two domains in one engine; would mix a read-only projection with mutating recovery and risk the Registry owner's semantics (FR-039) |
| Re-derive the watcher state machine inside the aggregator | FR-005/FR-038 forbid it; the derived map exists only for the no-watcher case and is labelled `derived` |
| Add a daemon that watches all lines | FR-041 forbids daemons; the driver already has bounded watch windows |
| Delete stale status files during retry | FR-030/FR-050 require isolation only; deletion destroys evidence |
| Auto-clear a stale recovery lock | A-19 requires explicit `--break-lock`; silent clearing could allow two writers |
| Treat `/proc` or `pgrep` scans as liveness | watch-model §7 and FR-013 forbid process scanning; PID file + `kill -0` + start-token identity is the only accepted path |
| Auto-commit implement code on resume | FR-029/FR-049 forbid it |

## 4. Test strategy

| Layer | File | Coverage |
|-------|------|----------|
| Unit | `tests/unit/test_loop_state.py` | CLI grammar/exit codes; snapshot derivation D0–D8; eight interruption forms; stale attribution; action table; check-spine valid/invalid matrix; recover dry-run/idempotency/isolation/commit/salvage/stop/handoff/lock; self-test |
| Contract | `tests/contract/test_sdd_loop_driver_state_awareness.py` | Owner-doc sections and rule ids; SKILL.md lifecycle lines and H2 registration; CLI/JSON schema literals; no bare `state:`; no threshold duplication; stdlib-only; docs page; mirror byte identity |
| Integration | `tests/integration/test_loop_state_interruption_matrix.py` | Accident replay; eight forms as fixtures; retry→clean signal surface; resume in a real temp git repo; stop handoff; concurrent lock; 063-style no-run carriers; probe unreachable |
| Regression | existing watcher `--self-test`, `test_sdd_loop_driver_skill.py`, `test_non_regression_064.py`, `test_sdd_loop_driver_gates.py` | Zero verdict/exit-code difference; mirror clean; pinned structure updated only where this feature adds surface |

Mutation drills (FR-046) at implement time: disable `unwatched` detection, disable stale isolation, disable the salvage gate — each must turn at least one named test red; record commands and outputs in `verification.md`.

## 5. Risks

- **Carrier format split (063 vs 064)**: the attribution rule (D-05/D-02) is the mitigation; integration tests cover a no-`run=` carrier.
- **Threshold drift**: the resolver parses the watcher help; a contract test compares the resolver with the real script. If the help format changes, tests fail rather than the engine inventing a value.
- **Task budget**: the feature is large (52 FR). The plan keeps one implementation chain and consolidates test rows; if `tasks` U4 exceeds 40, the driver must decide per §5.3 before `analyze`.
- **Mirror pre-existing drift**: the 11-file baseline is disclosed; the implementation's sync resolves it and the verify criterion is zero drift for this pair, not "no new drift only".
- **Spine coexistence**: `line-registry.py` reads the first bare `state:` line; the `spine_state:` prefix plus a fence-content validation prevents accidental capture.

## 6. Planning gate record (decomposition)

`notes/decomposition-gate.md` records `split-required` (52 FR > 30). The upstream driver dispatched this plan for the full Feature 065; per §5.3.3 the dispatch is the upstream-flow confirmation required before advancing. This plan does not delete, merge or reorder any FR. The `tasks` U4 gate remains in force and is called out in plan.md as a risk; if it returns `split-required`, the driver must split or record a further explicit decision before `analyze`.
