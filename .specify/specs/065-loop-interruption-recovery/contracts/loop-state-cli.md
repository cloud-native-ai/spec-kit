# Contract LS — `loop-state.py` CLI, Inputs, Envelope & Exit Codes

**Owner**: `skills/external/sdd-loop-driver/references/state-awareness.md` § Entry & Invocation.
**Scope**: the executable surface shared by `snapshot`, `recover` and `check-spine`. The meaning of the output fields is owned by the snapshot and recovery contracts; this contract owns grammar, input resolution, envelope and process behavior.

- **LS-01**: The entry is `scripts/loop-state.py` in the skill directory, executable with `python3`, Python 3.8+ standard library only, zero third-party imports, zero network calls, zero daemons.
- **LS-02**: Exactly three actions exist: `snapshot`, `recover`, `check-spine`. A missing or unknown action is a usage error (exit 2), never a default action.
- **LS-03**: Global options: `--action`, `--line-id`, `--run-id`, `--stage`, `--spine`, `--state-dir`, `--spec-dir`, `--repo`, `--probe`, `--watch-script`, `--watch-timeout`, `--deadline-grace`, `--heartbeat-max-age`, `--out`, `--self-test`, `--help`.
- **LS-04**: `recover` additionally accepts `--apply`, `--salvage`, `--evidence` (repeatable), `--window`, `--lock-wait`, `--break-lock`. An option that does not apply to the chosen action is a usage error (exit 2).
- **LS-05**: Input resolution order is: explicit `--spine`/`--state-dir`/`--spec-dir`/`--repo`/`--probe` values → the Registry entry selected by `--line-id` → failure for a required input. A missing optional input is reported as `unknown`, never filled with a guess.
- **LS-06**: When both an explicit path and a Registry value exist, the explicit path wins. The output records every resolved path.
- **LS-07**: `--probe FILE` is exclusive with local evidence collection: no local watcher is invoked, no local state file decides the verdict, and `evidence_source=probe`. A malformed probe is exit 2.
- **LS-08**: Every action writes exactly one JSON object to stdout (or to `--out` atomically) with `schema_version`; human-readable text never shares stdout. Diagnostics go to stderr.
- **LS-09**: Exit codes are `0` (successful evaluation/application, `already-applied`, or `action=stop`), `1` (validation failure, refusal, lock contention, application failure), `2` (usage error or unreadable required input). `loop_state` is data and never encoded as an exit code.
- **LS-10**: The engine MUST NOT emit watcher exit codes 10–16 from any action; those remain owned by `watch-target.sh`.
- **LS-11**: `--help` prints the three actions, the input groups, the exit-code ladder and the dry-run default, and exits 0.
- **LS-12**: `--self-test` runs in a temporary directory, prints one `ok <name>` line per case plus a summary, exits 0 only when every case passes, and leaves no files outside its temporary root.
- **LS-13**: `snapshot` and `check-spine` are read-only: no file write, no git state change, no process signal, no lock. `--out` is the only write and is explicit.
- **LS-14**: `recover` defaults to dry-run. Without `--apply` it performs no write, commit, move or lock, and emits the same decision plus a `steps[]` plan.
- **LS-15**: `recover --apply` applies only `resume`, `retry`, `stop` and `watch`; `verify` and `none` remain no-write control returns even with `--apply`.
- **LS-16**: Every `recover --apply` acquires the per-line recovery lock before re-evaluating and applying; a dry-run never locks.
- **LS-17**: The lock is `<state-dir>/recover-<line>.lock`, created with `O_CREAT|O_EXCL`, carrying `pid`, `start`, `run_id`, `at`, `action`, `stage`. A second writer waits `--lock-wait` seconds and then returns `result=locked` (exit 1) with the holder metadata.
- **LS-18**: A stale lock is never cleared automatically. `--break-lock` moves it into `attempts/` and re-attempts acquisition; it never unlinks the old lock.
- **LS-19**: `--salvage` is legal only when the resolved recovery action is `resume`, and requires at least one `--evidence` reference. A non-resume action with `--salvage` is exit 2; an unlocatable evidence reference is a refusal (exit 1). The requirement's `recover --action resume --salvage --evidence` form is expressed as `--action recover --salvage --evidence`, because `--action` selects the three-action engine surface (LS-02); the engine refuses the flag unless the adjudicated action is `resume`.
- **LS-20**: `--watch-script` defaults to the sibling `watch-target.sh`; a missing or non-executable watcher is `watch=unavailable`, never a stage failure and never `DEAD`.
- **LS-21**: Watcher attribution mode is explicit in the output: `own` when `--line-id`/`--run-id` are passed, `legacy` when they are not, `probe` when a probe is used. The choice follows the attribution rule in SN-05.
- **LS-22**: When a required input is missing or unreadable, the engine exits 2 and names the input; it does not emit a partial snapshot with a guessed state.
- **LS-23**: Each action's output is deterministic for the same file state: keys are sorted, arrays follow rule/map order, and no elapsed/age number is emitted.

## Clause → requirement map

| Clause | FR / SC |
|--------|---------|
| LS-01 | FR-001, FR-041 |
| LS-02–LS-04 | FR-001, FR-025 |
| LS-05–LS-07 | FR-002, FR-024 |
| LS-08–LS-10 | FR-003, FR-012 |
| LS-11–LS-12 | FR-012 |
| LS-13–LS-15 | FR-001, FR-035 |
| LS-16–LS-18 | FR-048 |
| LS-19 | FR-028 |
| LS-20–LS-21 | FR-005, FR-038 |
| LS-22–LS-23 | FR-003, FR-037, SC-009 |
