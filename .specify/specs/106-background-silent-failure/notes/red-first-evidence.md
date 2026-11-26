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

## T012–T017 — US2 owner text and pointer rows

- Surfaces edited (framework source; mirrors regenerated by the scripts, never by hand):
  `skills/internal/create-team/SKILL.md` § Report (7-column header, 5-column legacy
  carve-out, seat start record), `skills/internal/run-agent/SKILL.md` (C4 native
  obligations), `shared/definitions/subagent-definitions.md` § Three Execution Modes
  (written virtual exclusion), `shared/workflow/external-dispatch-recipes.md` (Recipe 4
  per-value dispositions + two permitted background forms; Recipe 7 per-validator
  settlement), `shared/definitions/superagent-definitions.md` § Termination
  (observer-optional sentence), and the pointer rows in `skills/internal/run-team/SKILL.md`,
  `skills/external/sdd-loop-driver/SKILL.md`, `templates/commands/agents.md`,
  `templates/commands/team.md` and the four `agents/sdd-*-coordinator.agent.md` templates.
- Regeneration (generated surfaces only): `sync-mirrors.py --write --only shared`,
  `--only skills/internal`, `--only skills/external`, `--only agents` → each scope synced;
  `sync-mirrors.py --check` rc **0** (six pairs ok); `regen-command-copies.py` then
  `--check` → `OK: all per-tool command copies match the source templates.` rc **0**.

## T018 — US2 turn-green and per-carrier readings

- Command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_carriers.py -q`
- Exit code: **0**; real output: `21 passed in 6.31s` (all 12 red-first legs from T009
  turned green).
- Per-carrier settlement readings (deterministic fixtures, same engine face):
  - **C1** dead-pid stage (start sidecar, recorded pid gone, no status record) →
    `silent-end` (`detail=pid-gone`), engine exit **0**
  - **C2** silent death (real `dispatch.sh` + fake CLI, SIGKILL) → `silent-end`,
    engine exit **0**; live pid → `running`, never `silent-end`; TERM/INT/HUP → `failed`
  - **C3** seat with `c3-team-seat` start record and no report row → `silent-end`;
    seat with a report row and no start record → `unknown`
    (`unknown_cause=start-record-missing`), that run's engine exit **2**
  - **C4** native attempt record past its wait deadline → `silent-end`
    (`detail=deadline-passed`), engine exit **0**; the native obligations themselves are
    text-pinned (behavior-class: review/mutation evidence, per C-34)
  - **C5** exclusion assertion — the written virtual exclusion text pin
    (`test_c5_virtual_exclusion_is_written_in_three_execution_modes`)
  - **C6** through the compliant C2 runner record → `silent-end`, engine exit **0**;
    per-value disposition wording text-pinned
- `.status` old-format readability: the T011 old-vs-new comparison (byte-identical
  files; identical readings from `journal-utils._field` and the engine's
  `_apply_status_record`); a hand-shaped legacy `.status` (`<label> exit=0`, written by
  the fixture builder) is read by the engine as terminal `exit: 0` with zero unreadable
  findings.
- 7-column header parsing: `test_c3_seven_column_row_completes_with_evidence` and the
  four sibling C3 legs; the static fixture `c3-report/` still yields `seat-ok completed`,
  `seat-legacy silent-end (legacy=true)`, `seat-missing-start unknown`.
- Pointer exercises owner uniqueness: `test_c22_dispatch_entries_reference_the_same_owner`
  (all eight entry surfaces name `superagent-definitions.md` § Termination) and
  `test_no_dispatch_surface_carries_a_second_value_table` (zero dispatch surface carries
  ≥5 backticked settlement values) both green; the T004 owner-page scan stays green
  (104 passed across the settlement + owner battery).
- Regression battery on every touched surface (three runs, 26 module paths):
  `104 passed`; `6 failed, 304 passed`; `2 failed, 226 passed` — every failing nodeid is
  present in `baseline-failed.txt` (pre-existing red at the implement entry), so the
  package adds **zero** new failing nodeids.


## T019/T020 — run-agent reaction obligations and retry assertions

- `skills/internal/run-agent/SKILL.md` gained the reaction obligations (settle every opened
  attempt before the outward report; per-attempt settlement value + evidence pointers;
  unsettled attempts marked 「未结算」; failure / anomaly / silent ending / detection defect
  reported item by item; retry = new attempt with a new label and kept evidence; retry of
  silent-end/unknown needs a named diagnosis or the user's ruling; stop records `running` +
  live evidence + reason; no silent repair). Mirror regenerated by
  `sync-mirrors.py --write --only skills/internal` (check rc 0; `cmp` source/mirror identical).
- Guard-vs-content measurement: run-agent now names 4 distinct backticked settlement values
  (`failed`, `running`, `silent-end`, `unknown`) — below the second-value-table thresholds of
  both `test_settlement_contract_definitions.py` (≥5) and
  `test_settlement_carriers.py::test_no_dispatch_surface_carries_a_second_value_table` (≥5),
  so both guards stay green with no heuristic change.
- Appended engine assertions: `test_retry_is_a_new_label_and_the_old_attempt_keeps_its_value`
  and `test_late_completion_after_the_deadline_lands_on_its_own_label`; appended text pins
  `test_run_agent_reports_every_attempt_before_the_outward_report` /
  `test_run_agent_retry_and_stop_rules_forbid_silent_repair`. These are the T020
  migration/regression exception declared in tasks.md (they guard T007/T019 behaviour after
  implementation; red capability is proven by the T021 drill and the T025 mutations).

## T021 — reaction drill (SC-004 source)

- Record: `test-evidence/reaction-drill.md`. Scenario: old attempt `silent-end` + new-label
  retry → `completed`; stale return present for the old attempt.
- Readings: uplink entries for both labels (values + evidence item counts 3 / 4); retry
  label differs; old evidence hashes equal before/after; engine-created attempts 0 (no
  auto-retry); engine `os.kill` signals `[0]` (non-zero kills 0); stale return file hash
  unchanged (consumption count 0). `settle_rc=0`.

## T022 — US3 turn-green

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_engine.py tests/contract/test_settlement_carriers.py -q`
- Exit code: **0**; real output: `48 passed in 6.45s` (engine module 25, carriers module 23).

## T023 — preservation guard (readings)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_preservation.py -q`
- Exit code: **0**; real output: `6 passed in 23.29s`.
- Baselines committed under `test-evidence/`: `watch-target-fbab7a45c.sh` (identical sha256
  `955ddf78…` to the live watcher), `watch-self-test-baseline.txt` (39 ok names),
  `super-sub-protocol-fbab7a45c.txt` (Downlink/Uplink paragraphs from `git show
  fbab7a45c:shared/definitions/superagent-definitions.md`), and
  `role-edge-report-empty-fbab7a45c.json` (stdout of the **pre-change** engine extracted
  from `fbab7a45c` on `tests/fixtures/superagent-role/empty`; the live engine reproduces it
  byte-for-byte, with relative paths so the output is location-independent).
- Readings pinned: watcher verdict/exit-code pairs, verdict token set (incl. `USAGE`),
  exit-code set `{0,10,11,12,13,14,15,16,2}`, sentinel literals — all member-for-member
  equal to the baseline copy; `--self-test` `SELF-TEST: 39 passed, 0 failed` with the same
  39 case names; five-element/seven-field paragraphs unchanged; `report` byte-identical on
  two consecutive runs and to the baseline; per-touched-file gate hits never above the
  baseline (owner page 0 ≤ 1; driver SKILL 1 ≤ 1; all others 0 ≤ 0); the two-slot ledger
  read through `audit-test-budget.py` `read_fence` + `check_ledger` (`implement`): zero
  violations, `baseline=1`, `closure≤1`.

## T024 — live / zombie fixtures (readings)

- Builders extended: `c1_live`, `c2_live`, `c3_live`, `c4_live`, `c2_zombie` (with
  `spawn_zombie_holder`, `/proc` state `Z` readiness polled — no fixed `sleep`), `now_iso`.
  `c2_pid_reuse` unchanged.
- Reverse assertions appended (carriers module): C1 live → `running` (live evidence), C2
  long silence + live pid → `running`; C3/C4 inside their wait deadline → `running`
  (`return-channel-open`); zombie → `silent-end` (`pid-gone`); recycled pid → `silent-end`
  (`pid-reused`).
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_carriers.py -q`
  → rc **0**, `30 passed in 6.29s`.

## T025 — mutation drill (readings)

- Record: `test-evidence/mutation-drill.md`. Four drills (silent-end detection, live
  evidence, `unknown` exit code, evidence pointer) each turned targeted tests red —
  3 / 4 / 3 / 1 failing nodes with real output; every drill restored byte-identically
  (sha256 `4a1b898b…` + empty `git diff`); post-drill engine+carriers run green
  (`54 passed in 6.44s`).

## T026 — scope guard (readings)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_scope.py -q`
  → rc **0**, `10 passed in 6.27s`.
- Meta-mutation recorded in `test-evidence/mutation-drill.md`: an injected second value
  table in `shared/workflow/external-dispatch-recipes.md` turned the table leg red
  (`1 failed`), then the file was restored byte-identically (sha256 `1406c61c…`).

## T027 — US4 turn-green and carrier × test coverage matrix

- Commands / readings:
  - `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_preservation.py tests/contract/test_settlement_scope.py tests/contract/test_settlement_carriers.py -q`
    → rc **0**, `46 passed in 22.33s` (6 + 10 + 30).
- Carrier × test coverage matrix (C-31; each listed carrier has a deterministic
  silent-death/settlement test and a reverse fixture; uncovered carriers = **0**):

| Carrier | Deterministic settlement test(s) | Reverse fixture / assertion | Contract notes |
|---------|----------------------------------|-----------------------------|----------------|
| C1 | `test_c1_dead_stage_settles_silent_end` (`silent-end`, `pid-gone`, start+lack evidence); `test_c1_done_without_u4_claim_is_incomplete`; `test_c1_done_with_u4_claim_is_completed` | `test_c1_live_stage_is_running_not_silent_end` (`running`, live evidence) | verdict-mapping pin `test_c1_mapping_function_covers_all_eight_tokens` |
| C2 | `test_c2_sigkill_silent_death_settles_silent_end`; `test_c2_signal_traps_write_termination_records` (TERM/INT/HUP → `failed`); `test_c2_exit_zero_without_declaration_is_failed_incomplete`; `test_c2_unreadable_evidence_is_unknown_exit_two` | `test_c2_long_silence_with_a_live_pid_stays_running`; `test_c2_zombie_is_silent_end_not_running`; `test_c2_pid_reuse_is_silent_end_not_running` | `.status` baseline reader leg; real `dispatch.sh` + fake CLI |
| C3 | `test_c3_seat_with_start_record_and_no_report_row_settles_silent_end`; `test_c3_report_row_without_start_record_is_unknown`; 5-/7-column row legs | `test_c3_live_seat_inside_its_deadline_is_running` (`return-channel-open`) | `settlement-unrecorded` / `settlement-unbacked` legs |
| C4 | `test_late_completion_after_the_deadline_lands_on_its_own_label` (native `silent-end`, `deadline-passed`); foreground-terminal branch pinned by `test_c4_run_agent_native_settlement_obligations` (`foreground-terminal`, `no settlement edge`) | `test_c4_live_native_inside_its_deadline_is_running` | C4 obligations are behavior-class beyond the text pins (C-34) |
| C5 | exclusion: `test_c5_virtual_exclusion_is_written_in_three_execution_modes`; no attempt record (engine carriers assert C5/C6 contribute no reader) | n/a — excluded by contract; the assertion IS the exclusion | unfinished virtual work must not be reported `completed` |
| C6 | through the compliant runner: `test_c2_sigkill_silent_death_settles_silent_end` (real `dispatch.sh` run); per-value dispositions `test_c6_recipes_carry_per_value_dispositions` | through-runner live leg: `test_c2_long_silence_with_a_live_pid_stays_running` | C6 settles only via C1/C2 evidence or foreground-terminal |

## T028 — migration contract, green-on-arrival (declared exception)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_migration.py -q`
- Exit code: **0** on the first run; real output: `8 passed in 6.30s`.
- **Planned red did not reproduce (disclosed)**: tasks.md expected the module to stay red
  until T029 landed the `legacy` field. The field — and the whole version-bearing shape
  rule — actually shipped inside the T007 settle action (commit `eabebe7bf`:
  `version_bearing` at `scripts/python/role-edge-check.py:1194`, legacy annotation at
  `:1571`), because the C-28 legs required 5-column vs 7-column parsing from the start.
  There is exactly one reading consistent with the recorded intent: T028 is the declared
  migration/regression **guard** (tasks.md § Tests Mode exception), and its red capability
  is evidenced by the T021 reaction drill, the T025 mutation drills and the T032 honesty
  record — not by a manufactured red here. No source was rolled back to fake a red.
- What the 8 legs pin (all against the already-delivered behaviour):
  `test_legacy_annotated_not_compliant` (legacy fixture: `legacy: true`, derived
  `completed`, rc 0, tree hashes unchanged), `test_versioned_claim_is_audited`
  (`settlement_version: 1`, `legacy: false`, clean audit, hashes unchanged),
  `test_version_bearing_is_decided_by_claim_shape` (claim file by field, report row by
  7-column header), `test_legacy_disagreement_is_annotated_not_a_violation` (legacy claim
  vs derived value: `consistent: false` yet zero violations and rc 0),
  `test_unreadable_legacy_claim_is_unknown_exit_two_naming_the_pointer` /
  `test_unreadable_versioned_record_is_unknown_exit_two_naming_the_pointer` (the single
  deterministic refusal names the pointer in both shapes),
  `test_incompatible_change_ledger_is_empty` (exactly one declared version across
  `shared/ skills/ templates/ agents/ scripts/`; owner page declares it the first
  version), `test_engine_carries_no_prebuilt_version_rejection` (no version comparison
  in the engine; a `settlement_version: 2` claim is audited — clean claim stays clean,
  bad value hits the ordinary `settlement-out-of-set` predicate).

## T029 — settle output version / legacy (verification, no code delta)

- T029's deliverable was already present in the T007 commit (see T028 entry). Verified
  against the task's checklist with real CLI readings on the committed fixture pair
  (scratch roots `.specify/.tmp/p4-t029/{state,teams}`, empty):
  - legacy fixture → rc **0**; `legacy-run` `verdict=completed`, `legacy=true`,
    `claim.settlement_version=null`, `violations=[]`, `consistent=true`.
  - versioned fixture → rc **0**; `versioned-run` `verdict=completed`, `legacy=false`,
    `claim.settlement_version=1`, `violations=[]`.
- Checklist mapping (code pointers, no source change made):
  - version-bearing by shape — claim file `settlement_version` presence `:1194`;
    team-report 5-column vs 7-column header `:1209`, `:1224-1250`;
  - legacy still derives from raw evidence — `_derive_settlement` runs before the claim
    audit `:1504-1560`; `_audit_claims` exempts legacy from all three predicates
    `:1587-1590`;
  - 5-column row exempt from `settlement-unrecorded` (exit 0), 7-column row missing
    `end_state`/`evidence` → `settlement-unrecorded` (exit 1) — pinned in
    `test_settlement_carriers.py::test_c3_legacy_five_column_row_is_annotated_not_judged`
    / `test_c3_missing_end_state_is_settlement_unrecorded`;
  - compliance counting only on version-bearing records — every violation row is
    produced by the version-bearing branch of `_audit_claims`; the legacy leg asserts
    `violations == []` and `summary.violations == 0` (T028);
  - legacy annotation never affects the exit code — `settle_exit_code` reads only
    `summary.unknown` and `violations` `:1738-1743`;
  - no new rejection branch — `test_engine_carries_no_prebuilt_version_rejection`
    (T028) plus the absence of any version comparison in the engine.
