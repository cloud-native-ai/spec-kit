# Quickstart — 066-loop-state-awareness-a

**Status**: design-time walkthrough for slice A. The snapshot engine lands in implementation; the engine examples below are **not executable at plan time** and are marked per example. The plan-time baseline section contains only commands that were actually run on 2026-10-21.

## Premises shared by S1–S8

- `<skill-dir>` is `skills/external/sdd-loop-driver/` in this repository.
- `<line-id>` is a registered line in the environment Line Registry; `<spec-dir>` is the feature's spec directory; `<repo>` is the target git repository.
- The state spine, carriers and watchbeat are fixture files unless the scenario says otherwise.
- The watcher is the existing `scripts/watch-target.sh`; it is never modified by this slice.
- A snapshot without `--out` writes nothing. A snapshot with `--out` writes only that file.
- `recovery_action` is advisory. Slice A never executes `resume`, `retry` or `stop`.

## Executed plan-time baseline

These commands were run during planning and their real results are reproduced below. They do not require the new engine.

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q \
  tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_sdd_loop_driver_efficiency.py \
  tests/unit/test_line_registry_engine.py \
  tests/unit/test_decomposition_check.py
```

Observed on 2026-10-21:

- `SELF-TEST: 38 passed, 0 failed`
- `ok skills/external/ == .specify/skills/ (26 files)`
- `108 passed in 27.67s`

These three results are the plan-time compatibility floor. The watcher SHA-256 pinned by the contract suite is `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4`.

## S1 — Accident replay: artifacts complete, exit=1, no sentinel, no watcher

**Premises**: the fixture reproduces the xuanji-doc 015 shape; plan artifacts are complete but uncommitted; the status record is `exit=1 sentinel=0`; no watchbeat exists; the registry entry points at the fixture spine and carriers; the watcher is unavailable for this fixture (or the probe reports unavailable). **Engine example — not executable at plan time** (the engine does not exist yet).

```bash
python3 <skill-dir>/scripts/loop-state.py --action snapshot \
  --line-id <line-id> --spec-dir <spec-dir> --repo <repo>
```

Expected contractual result (to be measured by the `accident-replay` fixture in `tests/contract/test_sdd_loop_driver_state_awareness.py` and the real-watcher mirror in `tests/integration/test_loop_state_snapshot_matrix.py`): `verdict_source=derived`, `loop_state=FAILED` (exit `rc≠0`), `completion=incomplete`, `interruptions[]` contains exactly `artifacts-without-completion` for the clean reply fixture (a `stale-signal` entry appears only if a non-own carrier is deliberately added), `recovery_action=retry`, exit 0.

## S2 — Normal running window with a fresh watchbeat

**Premises**: pid alive, heartbeat fresh, watchbeat present with `event=watch-window` and a fresh `at`; the watcher is available and returns `RUNNING`. **Engine example — not executable at plan time.**

```bash
python3 <skill-dir>/scripts/loop-state.py --action snapshot \
  --line-id <line-id> --spine <state-spine> --spec-dir <spec-dir> --repo <repo>
```

Expected contractual result: `loop_state=RUNNING`, `verdict_source=watcher`, `watch_status=available`, no `unwatched` finding, `recovery_action=watch`. **Verification**: `unwatched-vs-window` fixture in both the contract and integration suites.

## S3 — Running stage but the driver never started a watcher

**Premises**: pid alive or heartbeat fresh; no watchbeat (or a stale one); the watcher is unavailable so the derived map is used. **Engine example — not executable at plan time.**

Expected contractual result: `loop_state=RUNNING` (derived), `interruptions[]` contains `unwatched`, `recovery_action=watch`, no commit/retry/stop recommendation. **Verification**: `unwatched-vs-window` fixture plus the state-dir-unknown sub-case in the contract suite.

## S4 — Pseudo-completion: sentinel present, artifacts missing

**Premises**: the watcher/probe says `DONE` (sentinel), the stage artifact map knows the stage, and at least one required artifact is missing. **Engine example — not executable at plan time.**

Expected contractual result: `loop_state=DONE` verbatim, `completion=incomplete`, `interruptions[]` may contain `stale-signal` only if a carrier is non-own; `recovery_action=retry`; `loop_state` is never rewritten to `INCOMPLETE`. **Verification**: `sentinel-with-missing-artifact` fixture in both suites.

## S5 — Registered but never dispatched

**Premises**: Registry entry exists with no stage binding, no spine machine timing and no legacy stage/checkpoint, no attributable carriers, no watcher/probe verdict. **Engine example — not executable at plan time.**

Expected contractual result: `loop_state=UNKNOWN`, `recovery_reason=not-dispatched`, `completion=not-applicable`, `recovery_action=none`. **Verification**: `not-dispatched` fixture in both suites.

## S6 — Registry missing, and Registry present with a missing spine

**Premises**: two sub-fixtures. (a) Registry file missing but the spine and carriers are readable. (b) Registry entry present, spine missing; with and without a probe/watcher verdict. **Engine example — not executable at plan time.**

Expected contractual result: (a) evaluation continues, `registry.status=missing`, no `UNKNOWN` solely for Registry; (b) without a verdict `loop_state=UNKNOWN` + `interruptions[]` contains `lifecycle-spine-violation` + `recovery_action=stop`; with a verdict `loop_state` is verbatim and the form plus `stop` are still reported; `stage=unknown` when the envelope is unavailable. **Verification**: `registry-missing`, `registry-present-spine-missing` and `registry-present-spine-missing-with-watcher-verdict` fixtures in both suites.

## S7 — Probe snapshot from a remote host

**Premises**: the caller ran a snapshot on the evidence host and passes the JSON with `--probe`; the local watcher is deliberately unavailable; the probe may carry `watch_status=available` + `watch_verdict`, and may add `remote: {unreachable: true, reason: ...}`. **Engine example — not executable at plan time.**

```bash
python3 <skill-dir>/scripts/loop-state.py --action snapshot \
  --probe <probe.json> --line-id <line-id>
```

Expected contractual result: `evidence_source=probe` on probe-derived evidence; a probe watcher verdict is adopted verbatim (`verdict_source=watcher`); a probe derived result is re-evaluated locally (`verdict_source=derived`); a missing probe field never falls back to a local file; `remote.unreachable=true` yields `remote-unreachable`, action `stop`, never `DEAD`. **Verification**: `probe-snapshot` fixture plus the remote-unreachable sub-case in the contract suite and the no-fallback real-watcher case in the integration suite.

## S8 — Legacy spine

**Premises**: the state spine has no machine fence but has a readable `**current_stage**`/`**tries**`/`**state**` record; timing fields may be absent. **Engine example — not executable at plan time.**

Expected contractual result: `spine.schema=legacy`, missing fields are `unknown`, the readable stage/checkpoint counts as dispatch evidence, and the action never invents a `resume` from a missing default. **Verification**: `legacy-spine-snapshot` fixture in both suites.

## Execution obligations for implementation

When the engine lands, `/speckit.tasks` turns each scenario into a named contract or integration test and executes the examples once. The named matrix is split: the contract suite covers the pure fixtures (including accident replay and determinism), and the integration suite covers the real watcher, real git, probe no-fallback and no-write cases. The implementation MUST replace each "not executable at plan time" line with the measured result, or record why the scenario cannot be executed. Teardown of every temp fixture is part of the same scenario; no fixture may leak into the repository.
