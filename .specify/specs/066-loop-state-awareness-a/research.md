# Phase 0 Research — 066-loop-state-awareness-a

**Date**: 2026-10-21 | **Slice**: A (state awareness) of Feature 065
**Inputs**: slice `requirements.md`; parent `requirements.md`; `notes/decomposition-gate.md`; `notes/plan-blocked-review.md`; skill sources under `skills/external/sdd-loop-driver/`.

This is a dated research record. It measures the code and carrier formats the snapshot consumes, records the decisions that shape the design, and lists rejected alternatives. Where a value belongs to another owner (`watch-target.sh`, `watch-model.md`, `stage-prompts.md`, `efficiency-model.md`), this record cites the owner; the implementation and the owner reference must not copy the value.

## 0. Measured Baseline (2026-10-21)

Commands were run from the repository root. Outputs are reproduced as observed.

| Measurement | Command | Observed |
|-------------|---------|----------|
| Watcher self-test | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | `SELF-TEST: 38 passed, 0 failed` |
| Watcher SHA-256 | `shasum -a 256 skills/external/sdd-loop-driver/scripts/watch-target.sh` | `b6a275dbab62bffafadfb36eb5c389ab27e6f9bf7d498af8102c280201f2b0b4` |
| Mirror pair | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (26 files)`; 0 drift |
| Targeted pytest | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_sdd_loop_driver_skill.py tests/contract/test_sdd_loop_driver_efficiency.py tests/unit/test_line_registry_engine.py tests/unit/test_decomposition_check.py` | `108 passed in 27.67s` |
| Slice decomposition gate | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode plan --requirements .specify/specs/066-loop-state-awareness-a/requirements.md` | `proceed`, `fr_count=25`, ceiling 30 |
| Watcher help defaults (dated measurement, owner is the script) | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --help` | `Defaults: window=200s, interval=3s, start-grace=30s, deadline-grace=120s, heartbeat-max-age=120s` |
| Local Python / pytest | `python3 --version`; profiles venv pytest | Python 3.9.6; pytest 9.1.1 (repo `.venv` has no pytest) |

The watcher baseline is a dated observation. The implementation resolves defaults by parsing the current `--help` output at runtime; it does not embed the literals above (except the SHA-256, which is deliberately pinned by a contract test).

## 1. Code Facts the Design Consumes

### 1.1 Watcher output and verdict ownership

`scripts/watch-target.sh` owns the verdict state machine and the exit codes. The relevant observed facts:

- `--once` sets the window to zero and evaluates once, returning a single `WATCH` line (and an `EVIDENCE` line for terminal verdicts).
- The `WATCH` line carries `label=`, `verdict=`, `pid=`, `heartbeat=`, `hook=`, `anomaly=`, `sentinel=`, `rc=`, `elapsed=`, `reason=`, `stream=`, `line=`, `run=`, `stage=`, `at=`, `attribution=`.
- Exit codes are `0 DONE`, `10 RUNNING`, `11 ANOMALY`, `12 FAILED`, `13 DEAD`, `14 TIMEOUT`, `15 INCOMPLETE`, `16 NO_SIGNAL`, `2 USAGE`.
- Attribution classifies both `line=` and `run=`: missing envelope → `unattributed`; different line → `foreign`; same line/different run → `stale-run`; both match → `own`. Without `--line-id`/`--run-id` the watcher reports `legacy`.
- `--line-id`/`--run-id` with `--registry DIR` makes the watcher verify the registered identity and ignore an ambient pid file for a registered line with no registered PID.
- A `RUNNING` window expiry never produces `TIMEOUT`; only the stage deadline does.
- The watcher is read-only: it never kills, writes project state or mutates the tree.

The snapshot consumes this output verbatim when available. It does not import the watcher's bash functions and does not reproduce its exit codes in its own exit ladder.

### 1.2 Carrier formats and attribution precedence

Observed in `watch-target.sh` and `line-registry.py`:

- Status: a line beginning `exit=<rc>`; optional `sentinel=<0|1>`; optional envelope `line= run= stage= event=`.
- PID: `pid=<pid> start=<token> ...`; fallback first numeric token; optional envelope.
- Heartbeat: append/overwrite log whose mtime is the freshness source; the watcher reads the last non-empty line for its envelope.
- Log meta: `log-<line>-<stage>.log.meta.jsonl`; last line carries `line_id`, `run_id`, `sentinel_seen` and exit.
- The watcher's attribution precedence for the verdict is status → meta → heartbeat → pid → `unattributed`. The snapshot uses the same precedence for the log/status evidence projection, but applies the envelope rule to every carrier independently.

### 1.3 Registry entry and path resolution

`line-registry.py` is the Registry owner. Observed:

- Registry dir: `SPECIFY_LINE_REGISTRY_DIR`, else `$XDG_STATE_HOME/spec-kit/lines`, else `$HOME/.local/state/spec-kit/lines`.
- Entry: `<registry-dir>/<line_id>.json`, written atomically.
- Required entry fields: `line_id`, `run_id`, `project_dir`, `repo_root`, `driver_session`, `cli`, `state`; optional runtime fields: `stage`, `spine_path`, `status_path`, `log_path`, `heartbeat_path`, `worktree_path`, `branch`, `runner_pid`, `cli_pid`, identity tokens.
- Default runtime paths are `status-<line>-<stage>`, `log-<line>-<stage>.log`, `heartbeat-<line>-<stage>.log` under `$SPECIFY_LINE_RUNTIME_DIR` or `$HOME`; `pid-` is derived from the `status-` basename.
- `reattach-brief` aggregates the entry, spine state/last line, carrier existence, heartbeat age, reservation and lease. It does not expose every path the snapshot must report, and it performs identity checks beyond the snapshot's read-only scope.

The snapshot reads the entry JSON directly. The registry-dir resolver is a small mirror of the owner's env/XDG/HOME order; a contract test compares the two resolvers on env-set, XDG-set and default cases.

### 1.4 State spine shape

The existing spine is prose markdown. Observed in `.specify/specs/065-loop-interruption-recovery/state-spine.md`: header fields such as `**line_id**`, `**run_id**`, `**state**`, `**current_stage**`, `**tries**`, `**updated_at**`, followed by prose sections. There is no machine-readable fence yet. The slice reads:

- A future machine segment `<!-- loop-state:begin -->` … `<!-- loop-state:end -->` with `spine_schema: v1` and `spine_`-prefixed keys.
- A legacy fallback that recognizes the existing `**current_stage**`, `**tries**`, `**state**` and explicit `stage_started_at`/`stage_deadline_epoch`/`stage_base_commit`/`last_verdict` lines when present. Missing fields stay `unknown`.

The snapshot never writes the spine.

### 1.5 Stage artifacts and commit evidence

- `stage-prompts.md` § Independent Verification owns the U4 artifact list: requirements → `requirements.md`; plan → `plan.md`; tasks → `tasks.md`; checklist → a new `checklists/` file; analyze → report in the stage log, no commit requirement; implement → code/test commits; review → review artifact.
- `efficiency-model.md` §3 owns the plan-owned set: `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, `research.md`, `feature-ref.md`.
- The repository uses `verification.md` for implement and `review.md` for review in the existing feature directories. The slice's stage map follows those paths and records the commit scope explicitly.

### 1.6 Documentation and distribution surfaces

- Source: `skills/external/sdd-loop-driver/`.
- Generated mirror: `.specify/skills/sdd-loop-driver/`, regenerated only by `sync-mirrors.py`.
- Docs entry: `docs/reference/skills/sdd-loop-driver.md`.
- Existing contract test `tests/contract/test_sdd_loop_driver_skill.py` pins the SKILL.md H2 set, a mirror file list and byte identity. Adding a new reference and a new script requires updating its mirror list; adding a new H2 section is avoided by extending `Hard Requirements` and `References` instead.

## 2. Decisions

### D-01 — One new engine action, not a Registry extension

Add `scripts/loop-state.py` with `--action snapshot` and a stdlib `--self-test`; leave `recover` and `check-spine` reserved and non-mutating (they return exit 2 with an explicit "not available in this slice" error). Reason: the Registry engine owns registration/lease/ownership and is already large; the snapshot is read-only, needs spec/git evidence and must be independently testable. Rejected: extending `line-registry.py` (scope and blast radius), adding a second daemon (forbidden).

### D-02 — Watcher verbatim, derived only as a fallback

When a watcher verdict is available (local `--once` or a probe carrying `watch_status=available` + non-null `watch_verdict`), `loop_state` is that verdict verbatim and `verdict_source=watcher`. The derived map runs only when no watcher/probe verdict exists; it is labeled `verdict_source=derived` and never emits watcher exit codes. Reason: FR-004/FR-005 and the parent A-2 ownership rule. Rejected: reimplementing the watcher state machine (duplicate owner, drift), upgrading a probe's derived result to a watcher verdict (fabrication).

### D-03 — Independent completion verdict

Compute `completion` from sentinel configuration, sentinel presence, exit record and artifact completeness, separately from `loop_state`. A pseudo-completion leaves `loop_state` untouched and sets `completion=incomplete`; the action becomes `retry`. Reason: blocked-review findings 5 and 7. Rejected: overloading `loop_state` with `INCOMPLETE` for a watcher `DONE` (destroys the verbatim contract).

### D-04 — Envelope-first attribution

A carrier participates only when its own envelope proves `own` (`line=` matches, `run=` matches, `stage=` matches). `foreign`, `stale-run`, `unattributed`, and an own-run carrier whose mtime precedes `stage_started_at` go to `stale_signals[]`. Legacy attribution (no envelope) is allowed only when exactly one active line exists; with multiple active lines, an envelope-less carrier is `unattributed` with reason `legacy-stale`. The watcher's own attribution is line+run only; the snapshot's stricter stage rule applies only to its own evidence and completion projection, never to a verbatim watcher verdict (contract RUL-01). Reason: blocked-review finding 1, slice SA-6. Rejected: treating 063-style envelope-less files as own unconditionally (breaks multi-line isolation), duplicating `own`/`legacy` definitions in two rules.

### D-05 — Anomaly predicate independent of own status

Derived rule D2 evaluates `(exit record exists OR pid dead) AND last non-empty log line starts with "ANOMALY:"`; it does not require an own status record. Reason: blocked-review finding 3. Rejected: gating anomaly on own status (turns a dead process's anomaly into `DEAD`).

### D-06 — `dead-no-exit-record` requires no sentinel

Form I2 fires only when a pid record exists, the process is dead/zombie/reused, no exit record exists, and no sentinel is present. A sentinel routes the case to `completion`. Reason: blocked-review finding 4. Rejected: firing I2 alongside a sentinel and complete artifacts.

### D-07 — Forms annotate; only two producers set state

The eight interruption forms never set, override, downgrade or upgrade `loop_state`. Only the watcher verdict or the derived map sets it. Reason: blocked-review finding 5, slice SA-8. Rejected: assigning `TIMEOUT`/`RUNNING` from a form.

### D-08 — Three-state spine consistency

`spine.consistent` is `"true"` only when both the final `loop_state` and `last_verdict` belong to the watcher verdict set and are equal; `"false"` when both belong and differ; `"unknown"` when `last_verdict` is missing/unknown or the final state is `STALLED`/`REENTRY_REQUIRED`/`UNKNOWN`. `stalled`/`retrying` without `last_verdict` is not `false`. Reason: blocked-review findings 6 and slice SA-9. Rejected: requiring `last_verdict` on stop/retry states or silently choosing one value.

### D-09 — `stage_base_commit` is read-only evidence

The snapshot reads `spine_stage_base_commit`; absent means `commit=unknown` (or `not-applicable` when `commit_required=false`). It never falls back to "most recent commit". The writer obligation belongs to the later spine machine-segment slice. Reason: blocked-review finding 8 and slice SA-9. Rejected: guessing a base from `git log -1`.

### D-10 — Registry read with a pinned resolver parity

Read the `<line>.json` entry directly so every path is reportable. Resolve the registry directory with the same three-step order as `line-registry.py` (env → XDG → HOME). A contract test invokes both resolvers and asserts equality for the three cases. Registry status is `found`/`missing`/`unreadable`/`invalid`; unreadable and invalid are not collapsed into missing. Reason: blocked-review finding 10 and slice SA-12. Rejected: relying on `reattach-brief` alone (missing paths), importing the 2,500-line Registry module (coupling), inventing a private registry locator.

### D-11 — Strict input resolution

`--line-id` is required (or supplied by a probe). Path resolution is explicit override → Registry entry → missing. `spec-dir` is never guessed from the repo; absent means artifacts cannot be evaluated and completion is `unknown`. `repo` is explicit or the Registry worktree/repo; no current-working-directory fallback. `run_id`/`stage` follow probe → Registry → spine → `unknown`, with a legacy stage/checkpoint parser. Reason: deterministic, no silent guesses. Rejected: CWD as repo (unreproducible), scanning the specs tree for a matching line (cross-line inference).

### D-12 — Effective values come from owners, with no literals

Resolution order per value: explicit CLI → probe `effective` → spine machine field → stage artifact map (sentinel only) → watcher `--help` default (for watcher thresholds). If no source is available and a decision depends on it, the decision reports `UNKNOWN` and `effective.<key>.value="unknown"`. `retry_limit`/`attempt` have no parseable owner default in scope; absent input stays unknown and the retry-limit rule is skipped with a recorded reason. Reason: FR-004, slice clarify decision. Rejected: hardcoding 30/120/200/2, treating missing as zero.

### D-13 — Deterministic output

No elapsed/age numbers in the snapshot. Freshness is reported as `fresh`/`stale`/`missing`; liveness as `alive`/`dead`/`zombie`/`reused`/`missing`. Lists have a pinned order (interruptions by the FR-009 form order, then attribution order; stale signals by pointer; artifacts by the stage map order). `evaluated_at` is the only field allowed to vary between two identical-input runs. Reason: SC-002. Rejected: copying the watcher's `elapsed=`/`at=` into the snapshot, including heartbeat age seconds.

### D-14 — Probe is a snapshot, not a private format

`--probe` accepts a document with `schema_version=1` and snapshot-shaped fields. The probe's evidence is normalized to `evidence_source=probe`; a probe with `watch_status=available` and a non-null `watch_verdict` supplies a watcher verdict verbatim; otherwise the local engine re-evaluates from the probe's evidence and labels `derived`. Missing probe fields stay `missing`/`unknown`; the engine never reads a local file for a missing probe field. Remote unreachability is an additive `remote: {unreachable: true, reason: ...}` object. Reason: FR-005 and slice SA-13. Rejected: a separate probe schema, falling back to local files, upgrading probe-derived results.

### D-15 — Salvage is an input, never a post-decision flag

Valid salvage input is either repeatable `--salvage-evidence <ref>` (read-only) or a spine record with `spine_salvage: accepted` plus `spine_salvage_evidence` and `spine_salvage_at`. At least one non-empty reference is required. Salvage participates before the action is chosen; without it, artifacts-complete-but-no-positive-evidence resolves to `retry`. It never turns a pseudo-completion (sentinel present, artifacts missing) into `resume`, and it never authorizes an implement code commit. Reason: blocked-review finding 2 and slice SA-7. Rejected: a `--salvage` flag that overrides a `retry` after the fact.

### D-16 — Watchbeat is driver evidence only

The driver writes `<state-dir>/watchbeat-<line>-<stage>` atomically at each U3 window start (`event=watch-window`) and return (`event=watch-return`), containing `line=`, `run=`, `stage=`, `window=`, `at=`, `event=`. The snapshot reads it; it never participates in completion or liveness. `unwatched` fires when the stage is running (pid alive, or heartbeat fresh with a pid that is not dead) and the marker is missing, non-own or older than `window + effective.deadline_grace`; an `unknown` freshness due to a missing grace value does not fire the form. A fresh marker after a normal window expiry does not fire. `state-dir` resolves explicit → parent of `--spine` → parent of the Registry `spine_path`; unresolved means the marker is missing and the reason is `state-dir-unknown`. The owner reference carries the atomic write form and SKILL.md Hard Requirements carries the driver obligation (FR-010 verification route); no engine code writes the marker. Reason: FR-010/FR-011, slice clarify. Rejected: writing the state spine on every RUNNING window (violates watch-model §5), using the marker as a heartbeat.

### D-17 — Action table with two bounded guards

The action order follows FR-003 with two explicit guards:

- The retry-limit stop does not override `watch`/`none`/`verify`; if `attempt` or `retry_limit` is unknown, the stop rule is skipped and the reason records `retry-limit-unknown` when the resulting action is `retry`.
- A same-line `stale-run` drives `retry` only when the current attempt is not provably running and `completion≠complete`; otherwise the current `watch`/`verify`/`resume` is kept and the carrier remains reported. This is assumption A-P1.

Live `TIMEOUT` always resolves to `watch`, never to `stop`; the recovery slice owns the explicit live-stop decision. Reason: FR-003/FR-009, blocked-review finding 12. Rejected: letting a stale carrier retry a running stage, letting the retry limit stop a healthy watcher.

### D-18 — Stage artifact map in code and owner doc, parity-tested

The map has exactly the eight known stages (no ninth, no implicit "all files"). Each row carries required paths (relative to the spec dir), `commit_required` (`true`/`false`/`conditional` for clarify), `no_change_allowed`, sentinel literal and commit scope. The engine holds the data; the owner reference holds the prose table; a contract test compares every row. Analyze has no required file artifact and `commit_required=false`; clarify allows no change and is `conditional`; implement requires `verification.md` and non-`.specify/` commits; review requires `review.md`. Reason: FR-006/FR-008, parent A-12. Rejected: deriving artifacts from the log, an "all files" fallback.

### D-19 — Watchbeat and snapshot never write the spine or carriers

The snapshot's only filesystem write is an explicit `--out` JSON file; that path is refused if it resolves inside the state dir or the repo. Watcher invocation is a read-only `--once`; git commands are read-only; Registry is opened read-only. The `recover`/`check-spine` actions are not available in this slice and cannot mutate anything. Reason: FR-001, slice SA-4. Rejected: "helpful" lock acquisition, auto-isolating stale carriers during snapshot.

### D-20 — Documentation surface stays minimal

`SKILL.md` gains one Hard Requirement bullet and one References entry; `references/state-awareness.md` owns the new rules; `docs/reference/skills/sdd-loop-driver.md` gains a state-awareness section. No new H2 section is added to SKILL.md, so the existing pinned H2 contract remains stable; the mirror file list is extended with the two new files. Reason: FR-019 and the existing contract test's pinned surfaces. Rejected: a large SKILL.md section duplicating the owner reference, editing `stage-prompts.md` write timing.

## 3. Rejected Alternatives (Summary)

| Alternative | Why rejected |
|-------------|--------------|
| Extend `line-registry.py` with snapshot | Registry owns registration/lease/ownership; snapshot needs spec/git evidence and a different read-only test surface; engine is already large |
| Reimplement watcher verdict logic in Python | Duplicate owner; watcher exit codes and signal priority must stay exclusively in `watch-target.sh` |
| Hardcode thresholds or copy them into the owner doc | Violates one-source-of-truth and FR-004; drift is invisible until an incident |
| Use `pgrep`/process scans | Documented pgrep trap in watch-model §7/§13; file evidence only |
| Treat log text as artifact evidence | FR-007 requires file existence/non-empty; log parsing is not completion evidence |
| Mix local and probe evidence | FR-005 forbids fallback; mixed provenance is irreproducible |
| Include heartbeat age seconds in JSON | Breaks same-input determinism (SC-002) |
| Let forms set `loop_state` | Blocked-review finding 5; destroys watcher verbatim |
| Let salvage override a post-decision retry | Blocked-review finding 2; circular gate |
| Use the registration `run_id` as dispatch evidence | Registration is not dispatch (FR-002); would make every registered line look dispatched |
| A private probe format | FR-005 requires the snapshot schema; additive fields only |
| A new daemon or scheduler | FR-016 and constitution IX forbid it |

## 4. Test Strategy

- **Unit** (`tests/unit/test_loop_state_engine.py`): pure functions for spine parsing, attribution, derived rules D1–D11, completion, action table, effective resolution, watchbeat freshness, registry status, and the no-write snapshot proof. The engine's `--self-test` is invoked and must print a `SELF-TEST: N passed, 0 failed` line.
- **Contract** (`tests/contract/test_sdd_loop_driver_state_awareness.py`): one test per contract clause; owner-doc/code parity for the stage map and field set; watcher SHA-256 pinned (a byte change must turn the test red); exit ladder 0/1/2 in `--help` and `--self-test`; no threshold literals in the owner reference; mirror byte identity for the two new files; docs entry assertions; the pure named-fixture matrix (including accident replay, determinism, pseudo-completion, not-dispatched and probe projection).
- **Integration** (`tests/integration/test_loop_state_snapshot_matrix.py`): real watcher `--once`, real git commit/uncommitted evidence, the probe no-fallback case and the no-write tree proof, using the same named fixtures. The two suites both enumerate their fixture names in their own sources; CMP-07 lists the union.
- **Named fixtures**: `sentinel-with-missing-artifact`, `legacy-spine-snapshot`, `artifacts-without-completion`, `dead-no-exit-record`, `unwatched-vs-window`, `registry-missing`, `registry-present-spine-missing`, `registry-present-spine-missing-with-watcher-verdict`, `not-dispatched`, `probe-snapshot`, `stale-run`, `foreign-carrier`, `deadline-overrun-live`, `heartbeat-stalled`, `accident-replay`, `salvage-two-state`, `implement-commit-missing`, `resume-commit-missing`.
- **Determinism**: run the same fixture twice, remove `evaluated_at`, canonicalize JSON (sorted keys), compare.
- **No-write proof**: hash the fixture tree (paths + bytes) before and after a snapshot (without `--out`); require equality. With `--out`, only the output path changes.
- **Mutation drills**: implementation copies the engine to a temp tree and removes (1) no-watcher detection, (2) completion/loop_state separation, (3) interruption-only annotation; each mutation must turn at least one named test red. The drill log is a dated implementation record.
- **Real watcher case**: the integration suite runs `watch-target.sh --once` against fixture carriers and asserts `loop_state` equals the `WATCH` verdict; probe cases use a probe with a watcher verdict and a deliberately missing local watcher path to prove no fallback.

## 5. Open Points Carried to Tasks

- The engine's self-test case names and the pytest fixture names must stay in sync by a contract assertion (the test file enumerates the names; the self-test prints them).
- The implementation must decide the exact atomic watchbeat write snippet shown in the owner reference; it is a driver-side shell action, not engine code.
- The implementation must record baseline/closure test-budget evidence in the state spine per the existing efficiency rules; this plan only fixes the plan-time baseline (108 passed, watcher 38/0, mirror 0 drift).
- The implementation must execute the quickstart commands once the engine exists and replace the plan-time disclaimers with measured output.
