# Red-First Evidence — spec 106

Every entry records the command, the real output (decisive excerpt) and the exit code.
The test entry is `scripts/bash/run-tests.sh`; the interpreter override on this host is
`SPECKIT_PYTHON=/usr/local/bin/python3` (measured premise, tasks.md § Environment
Prerequisites).

<!-- entries are appended in execution order -->

## T004 — settlement contract definitions (owner page)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_contract_definitions.py -q`
- Exit code: **1**
- Real output (tail): `18 failed, 1 passed in 6.24s` — every owner-text leg fails on
  `AssertionError: § Termination is missing from shared/definitions/superagent-definitions.md
  (the settlement contract owner section, C-01)`; the single pass is the vacuous
  "no second value table" scan (no second table exists yet because the owner table does
  not exist yet).
- Red-first ordering note: the pinning test was authored **before** the owner-section
  amendment (T002/T003) precisely so the red is real, not a missing-file artifact; the
  named assertions quote the contract clauses C-01…C-12.
- Turn-green: after the owner-section amendment the same command returned **rc 0,
  19 passed in 6.24s**. The existing sibling guard
  `tests/contract/test_superagent_definitions.py` also stayed green (29 passed for the
  pair), and the shared mirror was regenerated through
  `sync-mirrors.py --write --only shared` (check rc 0).

## T005 — deterministic fixture tree

- Created `tests/fixtures/settlement/builders.py` + the committed sample dirs
  `c1-state/`, `c3-report/{teams,logs}/`, `legacy/logs/`, `versioned/logs/`.
- Builders cover the six terminal classes, the unreadable attempt, the missing start
  record, a live child (open stdin pipe; no fixed `sleep`), and pid-reuse (recorded
  start ticks deliberately offset). Every record carries a fixed timestamp, so the
  same fixture yields the same settlement.

## T006 — settlement engine contract (red-first)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py -q`
- Exit code: **1**
- Real output: `23 failed in 6.40s`; the first failure is
  `role-edge-check.py: error: argument --action: invalid choice: 'settle' (choose from 'report', 'query')`
  — the action does not exist yet, so every leg fails on its own named assertion.

## T007/T008 — settle action implemented; US1 green

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_contract_definitions.py tests/contract/test_settlement_engine.py tests/contract/test_role_edge_engine.py -q`
- Exit code: **0**; real output: `67 passed in 6.49s` (19 owner pins + 23 engine pins +
  25 existing role-edge pins, including the engine-mirror byte-equality leg).
- Repeated-run identity and zero writes (static fixture
  `c1-state` + `c3-report/{teams,logs}`):
  - `--action settle` run twice → both rc **2** (the one `unknown` seat), stdout
    byte-identical (`settle_runs_byte_identical=yes`)
  - fixture tree list sha256 before == after:
    `f5edf63f71436e86049071bdd2354e1791b00fb1f79212d216c07f11de7a6ee0`
    (`fixture_tree_unchanged=yes`; the list covers every file, `__pycache__` excluded)
  - summary: `{"attempts": 4, "unknown": 1, "values": {"completed": 1, "failed": 1, "silent-end": 1, "unknown": 1}, "violations": 0}`
    — findings: `seat-ok completed`, `seat-legacy silent-end (legacy=true)`,
    `seat-missing-start unknown (start-record-missing)`, `demo-line-implement failed
    (incomplete)`.
- `report` / `query` byte comparison against the pre-change engine (the un-synced
  runtime mirror was verified byte-identical to `HEAD` before the sync):

| Input | Action | rc (old = new) | stdout |
|-------|--------|----------------|--------|
| `superagent-role/empty` | report | 0 | byte-identical |
| `superagent-role/root-a-b` | report | 0 | byte-identical |
| `superagent-role/fanout-10` | report | 0 | byte-identical |
| `superagent-role/violations/self-dispatch` | report | 1 | byte-identical |
| `superagent-role/root-a-b` (root→A) | query | 0 | byte-identical |

- Mirror: `sync-mirrors.py --write --only scripts` then `--check` rc 0;
  `cmp` source/mirror rc 0 (engine copy byte-identical).
- Confirmation-gate reading after the owner edit:
  `scan-confirmation-gates.py --root . --json` → total **30** (base 31); the touched
  file `shared/definitions/superagent-definitions.md` carries **0** hits
  (base 1) — zero NEW hits, per-file count not above base (EP-005 fallback).

## T009 — carrier surfaces red-first (US2)

- Command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_carriers.py -q`
- Exit code: **1**
- Real output: `12 failed, 9 passed in 66.18s`
- Failing node set (the red-first target set):
  - `test_c2_sigkill_silent_death_settles_silent_end` — `kill-seat.attempt was never
    written (C-14: before the CLI launches)`
  - `test_c2_signal_traps_write_termination_records[15/1/2]` — same missing `.attempt`
  - `test_c2_live_attempt_is_running_not_silent_end` — same missing `.attempt`
  - `test_c2_exit_zero_without_declaration_is_failed_incomplete` — same missing `.attempt`
  - `test_c16_report_contract_declares_the_settlement_columns`,
    `test_c21_observer_remains_optional`,
    `test_c4_run_agent_native_settlement_obligations`,
    `test_c5_virtual_exclusion_is_written_in_three_execution_modes`,
    `test_c6_recipes_carry_per_value_dispositions`,
    `test_c22_dispatch_entries_reference_the_same_owner` — each fails on its own named
    missing owner sentence (never on an import/collection error)
- Passing at red time (9): the engine legs (C3 five/seven-column rows, seat silent
  death, `start-record-missing`, C2 unreadable → `unknown` exit 2), the `.status` line
  shape / baseline-reader leg (the current writer already emits the byte-compatible
  line), and the "no second value table on dispatch surfaces" scan (vacuous until the
  new texts land).
- Process mechanics disclosed: every C2 leg drives the shipped `dispatch.sh` with a
  deterministic fake CLI (a python script that writes its pid then exits or blocks on
  stdin) and a passthrough stream filter; synchronization is fact-based polling, zero
  fixed `sleep`.

## T010 — C2 additive settlement evidence (dispatch.sh)

- `<label>.attempt` is written before the CLI launches: `settlement_version: 1`,
  `attempt_id` (= label), `carrier: c2-subprocess`, `parent_identity`
  (`DISPATCH_PARENT`, default `root`), `started_at` (UTC ISO-8601), `pid` (the wrapper
  shell), `pid_start_ticks` from `/proc/$$/stat` where `/proc` exists, and the `contract`
  pointer to § Termination. Both new records are written with an atomic
  `write-then-os.replace` so a reader never observes a half-written JSON object.
- `<label>.end` is written on normal exit (`exit`) and on TERM/INT/HUP traps (`signal`,
  `exit` = 128 + signum, `ended_at`, `settlement_version: 1`); SIGKILL stays untrappable
  and is the intended `silent-end` fixture.
- The pipeline now runs in a background subshell so `wait` stays interruptible by the
  traps; `PIPESTATUS[0]` inside the subshell keeps `.status` = the CLI's own exit code.
  The wrapper's stdin is carried across the async boundary on fd 8 (bash otherwise
  redirects an asynchronous list's stdin from `/dev/null` when job control is off) —
  without it the CLI would see EOF and a live dispatch would end instantly.
- Preserved surfaces (measured):
  - `.status` line format unchanged — `fail-seat exit=2` for a failing fake CLI
    (wrapper rc 2, engine verdict `failed` / `non-zero-terminal`); normal run
    `seat-x exit=0`.
  - `-h` rc 0, `--version` rc 0 (`dispatch.sh 0.0.22`), undeclared option rc 2 —
    the `script-interface:86` generated region was not touched.

## T011 — C2 turn-green and `.status` baseline readers

- Command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_carriers.py -q -k "test_c2_"`
- Exit code: **0**; real output: `7 passed in 6.30s` (three consecutive runs, stable;
  the signal legs ran 10× in isolation without a flake).
- Per-reader assertions inside that set (real process, fake CLI):
  - SIGKILL → recorded pid gone, no `.end` / `.status` → `silent-end`, engine **exit 0**
  - TERM / INT / HUP → `.end` with `signal` and `exit` 128+signum, `.status`
    `<label> exit=<128+signum>` → `failed`
  - live pid → `running` (evidence kind `live`), never `silent-end`
  - exit 0, no completion declaration → `failed` / detail `incomplete`
  - unreadable `.attempt` → `unknown` (`unknown_cause: unreadable`), engine **exit 2**
- Old vs new `.status`, same fake CLI (rc 0), old script materialized from
  `git show HEAD:…dispatch.sh` (sha256 prefix `877ff955453b6cb3`):
  - files byte-identical: `cmp` rc **0**, both `seat-x exit=0`
  - existing readers, old and new readings equal:
    `journal-utils._field(text, "exit")` → `"0"` / `"0"`;
    `status-digest.project_exit_record(path)` → `(None, None)` / `(None, None)` (that
    reader targets the C1 line-start `exit=` shape; identical on both sides — recorded
    as-is, not claimed as a C2 reading);
    `role-edge-check._apply_status_record` → terminal `[(0, None)]` / `[(0, None)]`,
    `unreadable=[]` on both.

