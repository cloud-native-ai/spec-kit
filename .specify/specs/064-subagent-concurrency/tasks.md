# Tasks: Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling）

**Requirement ID**: 064
**Requirement Key**: 064-subagent-concurrency
**Related Feature**: 064 Subagent 并发归属、CLI 能力档案与生命周期解耦
**Input**: `.specify/specs/064-subagent-concurrency/` — plan.md, requirements.md, research.md, data-model.md, contracts/ (6 files / 98 clauses), quickstart.md, feature-ref.md, notes/063-overlap-adjudication.md
**Prerequisites**: plan.md ✅, requirements.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅, quickstart.md ✅

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is NON-NEGOTIABLE; unit + contract + integration layers required; plan.md § Tests Mode).

**Organization**: Tasks are grouped by user story so each story is independently implementable and testable. Tests are authored before the implementation they exercise; red runs are captured before implementation; implementation ends with a green run and a mirror sync.

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]` or `[~]` with a recorded reason; zero `[ ]` and zero `[>]` rows remain.
- DoD-2: The 10 planned test files plus the US5 non-regression file exist; every executable test is green in a pytest-capable environment, or `green: Unobserved` is recorded verbatim per NG-10 without claiming a pass.
- DoD-3: All 6 contract files (LR/EN/WI/LC/CLP/NG, 98 clauses) are covered by named test tasks; FR-001…FR-068 map to the five story phases; SC-001…SC-010 each has a status in `verification.md`.
- DoD-4: Every touched mirror pair has no NEW drift; `shared/definitions/probe-definitions.md` is byte-identical in both trees; `compile-embeds --check` reports zero drift.
- DoD-5: `docs/reference/skills/sdd-loop-driver.md` carries concurrency/lifecycle and CLI-capability-profile entry sections that reference, never copy, the skill references.
- DoD-6: Quickstart S1–S6 have real command/output/exit evidence in `notes/quickstart-run.md`; teardown left no temp registry, worktree, or process.
- DoD-7: 063 overlap is closed: no duplicate CLI-profile owner, test, or Probe Object exists; merge-time deletion/pointer steps are recorded in `notes/063-overlap-adjudication.md`.
- DoD-8: No automatic push, no deletion of uncommitted work, no new daemon/external service/runtime dependency/model API, and no change to 058 sentinel/verdict/exit-code semantics or confirmation gates.
- DoD Status: done

## Completion Gate

- GATE-1: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/064-subagent-concurrency/tasks.md` exits 0 with 0 errors and 0 warnings.
- GATE-2: Full suite has zero NEW failures vs the recorded baseline — check `.specify/scripts/bash/run-tests.sh tests -q --names-out .specify/specs/064-subagent-concurrency/current-failed.txt` then `comm -13 .specify/specs/064-subagent-concurrency/baseline-failed.txt .specify/specs/064-subagent-concurrency/current-failed.txt`; if no pytest interpreter resolves, `verification.md` must carry `green: Unobserved`.
- GATE-3: No open or claimed task rows — check `grep -cE '^- \[[ >]\]' .specify/specs/064-subagent-concurrency/tasks.md` returns 0.
- GATE-4: `verification.md` lists every `SC-001`…`SC-010` with a status — check `python3 -c "import pathlib; t=pathlib.Path('.specify/specs/064-subagent-concurrency/verification.md').read_text(); m=[f'SC-{i:03d}' for i in range(1,11) if f'SC-{i:03d}' not in t]; assert not m, m"`.
- GATE-5: Mirror obligations have no NEW drift — check `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` exits 0, `--only shared/definitions/probe-definitions.md` exits 0, and the 9 pre-existing `shared/definitions` DIFFs are unchanged.
- GATE-6: Probe registry and compiled embeds are clean — check `python3 .specify/scripts/python/probe-utils.py --action probes --validate` exits 0 and `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` reports zero drift.
- GATE-7: No push action exists in engine/watcher surfaces — check `grep -R "git push" skills/external/sdd-loop-driver/scripts/` returns no matches.
- GATE-8: Quickstart S1–S6 are recorded — check `grep -cE '^### S[1-6]\.' .specify/specs/064-subagent-concurrency/notes/quickstart-run.md` returns 6.
- GATE-9: 063 duplicate-owner guard is green — check `run-tests.sh tests/contract/test_sdd_loop_driver_cli_profiles.py -q -k test_clp_17_no_063_duplicate_owner`.
- GATE-10: No new runtime dependency — the engine imports only Python stdlib and the watcher is bash; `tests/contract/test_non_regression_064.py` proves it.

## Environment Prerequisites

- `pytest`: **unavailable** — probe `python3 -m pytest --version` @ 2026-10-20 returned `No module named pytest`; affected: all test-execution tasks, including T002, T018, T031, T046, T064, T068–T076, and T079. `scripts/bash/run-tests.sh` fails loudly when no interpreter resolves; implement must record `green: Unobserved` per `contracts/non-regression-and-tests.md` NG-10 rather than fabricate a pass.
- `setsid`: **unavailable on this macOS host** — probe `command -v setsid` @ 2026-10-20 returned empty; affected: T042. Fallback is `nohup + disown` locally; Linux uses `setsid` when present (plan Assumptions).
- `nohup`: **available** — probe `command -v nohup` @ 2026-10-20 → `/usr/bin/nohup`; affected: T042.
- `git worktree`: **available** — probe `git --version` @ 2026-10-20 → `git version 2.54.0 (Apple Git-157)`; affected: T028.
- Python `fcntl`: **available** — probe `python3 -c 'import fcntl; print("fcntl ok")'` @ 2026-10-20 → `fcntl ok`; affected: T006, T038, T039.
- No docker daemon, network service, live cluster, or special hardware is required; all fixtures are local temp directories and temp git repositories.

## Format

- Task rows use exactly: `- [ ] TNNN [P?] [USn?] [blockedBy: Txxx,Tyyy] Description with exact file path`. The entire row stays on one line.
- `[P]` means the row can run in parallel with the other `[P]` rows in the same phase because it writes a different file; it never means "optional".
- `[USn]` is mandatory in every User Story phase and forbidden in Setup, Foundational, and Polish phases.
- `[blockedBy: ...]` names every earlier task that must be `[X]` before the row starts; it is machine-parsed, not prose.
- `[green: ...]` attribution tags are deliberately not used in this file; clause coverage is given by the explicit Contract Coverage Matrix below, and every story has a named verification row.

## Measured Premises (generation time: 2026-10-20, worktree `535ce680`)

| Premise | Command actually run | Measured result |
|---|---|---|
| Plan HEAD | `git rev-parse HEAD` | `535ce6803f50a3a481f98dca8f04ae89f87d6973`; `git worktree list` shows 064 on `064-subagent-concurrency` and the main worktree on `063-sdd-loop-efficiency` at `bcf27c77` |
| Skill mirror baseline | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | exit 2; `DIFF` on `SKILL.md`, `references/dispatch-recipes.md`, `references/watch-model.md` (3 files) |
| Shared definitions baseline | `python3 scripts/python/sync-mirrors.py --check --only shared/definitions` | exit 2; 9 `DIFF` files: `agent-definitions.md`, `contract-clause-definitions.md`, `derivation-definitions.md`, `dogfooding-definitions.md`, `framework-map.md`, `goal-definitions.md`, `self-improvement-definitions.md`, `subagent-definitions.md`, `tool-definitions.md` |
| Watcher self-test baseline | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | exit 1; `SELF-TEST: 12 passed, 4 failed`; failures: `pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced` (macOS platform degradation) |
| pytest availability | `python3 -m pytest --version` | `No module named pytest`; green baseline is Unobserved |
| Probe registry baseline | `python3 .specify/scripts/python/probe-utils.py --action probes --validate` | exit 0; `Probe registry valid: 10 classes, 113 internal + 0 external objects`; no `skill:sdd-loop-driver` object exists yet |
| Compiled embeds baseline | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` | exit 0; `compile-embeds --check: 74 units, zero drift` |
| SKILL H2 baseline | `grep -c '^## ' skills/external/sdd-loop-driver/SKILL.md` | `11`; the pinned list in `tests/contract/test_sdd_loop_driver_skill.py` has 11 entries; adding `CLI Capability Profiles` makes 12 |
| Planned test files | `find tests -name 'test_*.py' | wc -l` plus an explicit per-file `[ -e ]` loop | `267` test files exist; of the 10 planned files, 9 are absent and `tests/contract/test_sdd_loop_driver_skill.py` exists (1 of 10 present) |
| Toolchain | `python3 --version`; `git --version`; `command -v setsid`; `command -v nohup` | Python `3.9.6`; git `2.54.0`; `setsid` absent; `nohup` present at `/usr/bin/nohup` |
| Requirements validator | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/064-subagent-concurrency/requirements.md` | `scanned: 351 lines, 78 definition rows, 4 shared strings`; `0 error(s), 0 warning(s)` |
| 063 overlap | `git ls-tree -r --name-only bcf27c77 -- .specify/specs/063-sdd-loop-efficiency` and `git grep` | 063 contains `.specify/specs/063-sdd-loop-efficiency/contracts/cli-profiles.md` and references to `references/cli/README.md`, `skill-sdd-loop-driver-wrapup`, `tests/unit/test_cli_profile_record.py`; no concrete `skills/external/sdd-loop-driver/references/cli/` files and no Probe Object row exist on `bcf27c77` |

**Trap forms recorded deliberately**:

- Mirror checks legitimately exit 2 at baseline; `grep -c '^DIFF'` is the count (3 and 9), not the command exit. Treating exit 2 as a feature failure is the naive trap.
- `find tests -name 'test_line_*.py' | wc -l` returns 0; the planned set is 10 files of which 1 exists. Count the explicit list, not a glob.
- `pgrep -c` zero-match prints `0` then appends another `0` via `|| echo 0`; the self-test reproduces `got: 0` / two-line trap. Never use `pgrep -c` for liveness or completion.
- The 063 tree is a different branch in a different worktree; its files are not present in this worktree. Use `git show bcf27c77:...` or read the main worktree read-only, never `cd` there or modify it.

## Contract Coverage Matrix

| Contract | Clauses | Test-authoring tasks | Implementation tasks | Green / verification tasks |
|---|---|---|---|---|
| `contracts/line-registry.md` | LR-01…LR-13 | T004, T007, T010 | T006, T012, T013 | T018, T019, T020 |
| `contracts/line-envelope-and-ingress.md` | EN-01…EN-16 | T008, T009, T010 | T014, T015, T016, T017 | T018, T019, T020 |
| `contracts/workspace-isolation.md` | WI-01…WI-21 | T021, T022, T023 | T025, T026, T027, T028, T029, T030 | T031, T032, T033 |
| `contracts/lifecycle-detach-reattach.md` | LC-01…LC-18 | T034, T035, T036 | T038, T039, T040, T041, T042, T043, T044, T045 | T046, T047, T048 |
| `contracts/cli-profiles.md` | CLP-01…CLP-17 | T049, T050 | T052, T053, T054, T055, T056, T057, T058, T059, T060, T061, T062, T063 | T064, T065, T066, T067 |
| `contracts/non-regression-and-tests.md` | NG-01…NG-13 | T068 (new guards) plus the existing `tests/contract/test_confirmation_gates_sweep.py` and `tests/contract/test_sdd_loop_driver_skill.py` suites (NG-06/07/11/12) | T069, T070, T071, T072, T073, T074, T075, T076 | T077, T078, T079, T080, T081, T082 |

Requirement-group mapping: FR-001…FR-017 → Phase 3 (US1); FR-018…FR-032 → Phase 4 (US2); FR-033…FR-045 → Phase 6 (US4); FR-046…FR-059 → Phase 5 (US3); FR-060…FR-068 → Phase 7 (US5). The clause-level FR→contract map is owned by `feature-ref.md` §3; this matrix maps those contracts to tasks, so FR coverage is transitive and is not restated here (One Source Of Truth).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze the pre-change measurements and the failing-test baseline before any source edit.

- [X] T001 Record pre-change measurements (mirror drift 3/9, watcher self-test 12/4, pytest unavailable, probe 113 objects, compile 74 units zero drift, H2 count 11, planned tests 1/10 present, setsid absent) with commands and real output in `.specify/specs/064-subagent-concurrency/notes/pre-change-measurements.md`
- [X] T002 [P] Capture the failing-test name baseline with `.specify/scripts/bash/run-tests.sh tests -q --names-out .specify/specs/064-subagent-concurrency/baseline-failed.txt`; if the runner reports no pytest interpreter, record `green: Unobserved` verbatim (NG-10) without creating a fake baseline

**Checkpoint**: Baselines and evidence landing points exist; no source file has been edited.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the shared test fixtures and the stdlib engine core that all user stories consume.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 Create shared fixtures in `tests/fixtures/line_fixtures.py`: temp registry/project/git-repo builders, four-piece writers, detached fake runner, PATH stubs for ps/pgrep, and `engine_path()`/`watcher_path()` resolvers honoring `SDD_ENGINE`/`SDD_WATCHER` for mutation drills
- [X] T004 [blockedBy: T003] Author foundational unit tests in `tests/unit/test_line_registry_engine.py` for engine-core behavior: action dispatch, `line_id`/`run_id` formats, atomic write + fsync + os.replace, per-line flock, registry dir resolution (`SPECIFY_LINE_REGISTRY_DIR`/XDG), exit-code taxonomy 0/2/3/4/6, unknown-field preservation
- [X] T005 [blockedBy: T004] Capture the red run of T004 (command, real failing output, exit status) in `.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md`
- [X] T006 [blockedBy: T005] Implement the engine core in `skills/external/sdd-loop-driver/scripts/line-registry.py`: argparse action table, registry-dir resolution, atomic JSON write/read, same-line flock with timeout, id generation/validation, exit-code mapping; run the foundational unit subset to green and record the command/output

**Checkpoint**: The engine module imports and its core primitives are green; story tests can now be authored against it.

---

## Phase 3: User Story 1 - 同环境多线路的身份与归属隔离 (Priority: P1) — MVP

**Goal**: A line registers once, every event carries `(line_id, run_id)`, foreign/stale-run/unattributed events cannot change the current line, and an unlabelled message asks exactly one clarification when more than one line is active.

**Independent Test**: Start two simulated lines with the same `PLAN-DONE` sentinel and the same CLI command name; inject each line's status/log/heartbeat plus a foreign monitor event; assert zero cross-attribution, exactly one clarification, and unchanged verdicts/exit codes.

### Tests for User Story 1 (MANDATORY) ⚠️

> Write these tests FIRST and keep the red evidence; they must fail before T012–T017.

- [X] T007 [P] [US1] [blockedBy: T003,T006] Author `tests/contract/test_line_registry_contract.py` covering LR-01…LR-13: location/override, register/deregister timing, per-line atomic write, same-line lock, concurrent read integrity, id formats/run_history, required fields, remote minimal fields, state enum/spine consistency, stale explicit cleanup, unwritable registry, single-line compatibility
- [X] T008 [P] [US1] [blockedBy: T003,T006] Author `tests/contract/test_line_envelope_contract.py` covering EN-01…EN-16: envelope fields, carriers (status, pid, and heartbeat tails; log `.meta.jsonl`; prompt meta), sentinel/last-line preservation, own/foreign/stale-run/unattributed/legacy classification, watcher flags and unchanged verdicts/exit codes, targeted-PID-only, ingress decision table, exactly-one clarification, ambiguous-stop, single/zero active lines, clarification non-blocking for other lines (EN-13: named assertion that other-line heartbeat/state keeps advancing), no-process-scan (PATH-stub count + source scan), single-line envelope compatibility
- [X] T009 [P] [US1] [blockedBy: T003,T006] Author `tests/integration/test_two_line_isolation.py` (S2): two lines with identical `PLAN-DONE` and identical CLI name, foreign status/pid/meta injection, `run_id` stale-run, PID reuse/death, no-line message exactly one clarification, `resolve-message` answer ambiguity, and zero `ps`/`pgrep` attributions
- [X] T010 [US1] [blockedBy: T006] Append US1 unit tests to `tests/unit/test_line_registry_engine.py` for envelope classification, ingress decision table, state word list, and id/field validation (partition this file by story; do not duplicate foundational cases)
- [X] T011 [US1] [blockedBy: T007,T008,T009,T010] Capture the red run of T007-T010 (commands, real failing output, exit status) in `.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md`

### Implementation for User Story 1

- [X] T012 [US1] [blockedBy: T011] Implement registry lifecycle actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `register`, `update`, `deregister`, `list --active/--all`, state enum, stale marking and explicit cleanup path, remote minimal fields, run_history; no blind deletion or overwrite of other lines
- [X] T013 [US1] [blockedBy: T012] Implement `resolve-message` in `skills/external/sdd-loop-driver/scripts/line-registry.py`: active = `active|waiting`, explicit `line_id`/unique `project_dir`/`repo_root`/branch matching, `route|clarify|ambiguous-stop|no-active|no-match`, exactly one question, zero process/cwd inference
- [X] T014 [P] [US1] [blockedBy: T011] Extend `skills/external/sdd-loop-driver/scripts/watch-target.sh` with optional `--line-id/--run-id/--meta`, attribution classification and output fields (`line=`, `run=`, `attribution=`), targeted registered-PID checks only, unchanged verdict state machine and exit codes, and new attribution self-test cases
- [X] T015 [P] [US1] [blockedBy: T011] Update the runner recipe in `skills/external/sdd-loop-driver/references/dispatch-recipes.md` to write the four-piece envelopes: status, pid, and heartbeat line-tail fields `line=`, `run=`, `stage=`, `event=`; append-only `log-<line>-<stage>.log.meta.jsonl`; and `prompt-<line>-<stage>.md.meta.json`; keep the sentinel as the log's last non-empty line
- [X] T016 [P] [US1] [blockedBy: T011] Update `skills/external/sdd-loop-driver/references/stage-prompts.md` with U0.5 registration, the message-ingress program (exactly one clarification, no process scan, ambiguous-stop), foreign/stale-run/unattributed handling, and single-line compatibility
- [X] T017 [P] [US1] [blockedBy: T011] Update `skills/external/sdd-loop-driver/SKILL.md` References/loop text with pointers to the Line Registry, envelope, and ingress rules; do not add the new `CLI Capability Profiles` H2 (US4 owns it)
- [X] T018 [US1] [blockedBy: T012,T013,T014,T015,T016,T017] Run US1 unit/contract/integration tests to green, fix failures, and record the command/output; do not weaken assertions to pass
- [X] T019 [US1] [blockedBy: T018] Sync the skill mirrors with `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`, then verify no NEW drift and run `tests/contract/test_sdd_loop_driver_skill.py`
- [X] T020 [US1] [blockedBy: T019] Execute quickstart S1 (single-line envelope) and S2 (two-line isolation), append the real commands/output/exit status under `### S1.` and `### S2.` headings to `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`, and tear down temp fixtures

**Checkpoint**: US1 is independently green; two lines with the same sentinel never cross-attribute, and the unlabelled-message rule is proven.

---

## Phase 4: User Story 2 - 同仓库并发写线的工作区隔离与确定性集成 (Priority: P1)

**Goal**: Every write line owns a worktree and branch, ownership overlap is rejected or serialized before writing, and a single coordinator merges `ready_for_merge` lines in a deterministic, replayable order.

**Independent Test**: In a temp git repo, run two write lines (one overlapping, one disjoint); assert worktree/branch records, overlap waiting ticket, `git fsck`, deterministic queue replay, runtime/mirror single-pass, and worktree retention on failure.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T021 [P] [US2] [blockedBy: T003,T006] Author `tests/contract/test_workspace_isolation_contract.py` covering WI-01…WI-21: worktree-per-write-line, branch discipline, target-path conflict, Manifest/projection, normalized overlap, FIFO/tie-break serialization, dead-holder no-auto-release, read-only/forbidden paths, runtime commit prohibition, archive conflicts, mirrors once, single coordinator, deterministic queue, per-line steps/failure retention, no force push, cleanup without `--force`, crash re-entry, resource isolation/cap/report, two-write-line acceptance
- [X] T022 [P] [US2] [blockedBy: T003,T006] Author `tests/integration/test_worktree_integration_queue.py` (S3): temp git repo + two worktrees, overlapping vs disjoint ownership, `git fsck`, commit-graph preservation, deterministic queue replay, runtime/mirror once, failure retention, no push, and disjoint concurrent resources
- [X] T023 [US2] [blockedBy: T006] Append US2 unit tests to `tests/unit/test_line_registry_engine.py` for path normalization/overlap, FIFO/tie-break waiting, topological queue layering/replay/cycle refusal, archive conflict naming, and port-block allocation
- [X] T024 [US2] [blockedBy: T021,T022,T023] Capture the red run of T021-T023 in `.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md`

### Implementation for User Story 2

- [X] T025 [US2] [blockedBy: T024] Implement Ownership Manifest storage and actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `ownership-check`, `release-ownership`, `promote-waiting`, normalized path comparison, overlap rejection/waiting ticket, dead-holder retention
- [X] T026 [US2] [blockedBy: T025] Implement integration actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `integration-enqueue`, `integration-plan`, `integration-record`, `integration_depends_on` topology, FIFO/tie-break, cycle refusal, deterministic replay
- [X] T027 [US2] [blockedBy: T026] Implement `archive-runtime` (runtime-record path set, conflict-preserving names, sha256, archive-before-remove) and `allocate-resources` (39000 + 20/line, cap 4, waiting reason) in `skills/external/sdd-loop-driver/scripts/line-registry.py`
- [X] T028 [P] [US2] [blockedBy: T024] Update `skills/external/sdd-loop-driver/references/dispatch-recipes.md` with worktree creation/branch discipline, ownership declaration, the integration protocol (rebase → full gate → merge → registry record → archive → remove), mirrors once per batch, no force push, and worktree retention on failure
- [X] T029 [P] [US2] [blockedBy: T024] Update `skills/external/sdd-loop-driver/references/stage-prompts.md` Concurrency Isolation with worktree/branch/ownership/resources declarations, one-writer-per-worktree, U6 worktree retention, and no shared writable runtime paths
- [X] T030 [P] [US2] [blockedBy: T024] Update `skills/external/sdd-loop-driver/SKILL.md` References/Boundary with workspace-isolation and integration-queue pointers (reference only, do not copy WI rules)
- [X] T031 [US2] [blockedBy: T025,T026,T027,T028,T029,T030] Run US2 unit/contract/integration tests to green, fix failures, and record the command/output
- [X] T032 [US2] [blockedBy: T031] Sync the skill mirrors with `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`, verify no NEW drift, and re-run the skill structure contract
- [X] T033 [US2] [blockedBy: T032] Execute quickstart S3 (worktree/ownership/integration queue) and append the real commands/output/exit status under a `### S3.` heading to `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`; tear down temp repos/worktrees safely

**Checkpoint**: US2 is independently green; two write lines produce no Git index corruption or lost commits, and the queue is replay-identical.

---

## Phase 5: User Story 3 - 主会话与子代理生命周期解耦与重新接线 (Priority: P1)

**Goal**: A stage subagent survives main-session death, and a new session reattaches through Registry + state spine with zero redispatch across the running, done, and dead branches.

**Independent Test**: Start a detached fake stage with heartbeats, kill the driver shell, start a new session, acquire the lease, verify PID/start token/cwd/branch, take one `--once` snapshot, and assert the three branches plus zero redispatch and reservation exclusivity.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T034 [P] [US3] [blockedBy: T003,T006] Author `tests/contract/test_lifecycle_detach_reattach.py` covering LC-01…LC-18: detached process group/stdio, main-session failure isolation, four-piece + CLI child PID, reservation exclusivity, live/expired lease, identity start token/cwd/branch, `--once` before decision, remote-unreachable, running, done, and dead branches, orphan, stale, duplicate launch, U6 closure, local/remote isomorphism, kill/reattach acceptance
- [X] T035 [P] [US3] [blockedBy: T003,T006] Author `tests/integration/test_session_kill_reattach.py` (S4): detached fake stage survives driver kill, new session reattaches via Registry + state spine, running, done, and dead branches, zero redispatch, reservation exclusivity, remote-unreachable → stalled; support `SDD_RUNNER_MODE=detached|foreground` for the detach mutation drill
- [X] T036 [US3] [blockedBy: T006] Append US3 unit tests to `tests/unit/test_line_registry_engine.py` for lease TTL/expiry, renewal cadence ≤ TTL/3, `suspected-alive` (PID alive + heartbeat expired → `--override` required), reservation O_EXCL/attach/refuse, start-token identity classification, `remote-unreachable` classification, and U6 residue checks
- [X] T037 [US3] [blockedBy: T034,T035,T036] Capture the red run of T034-T036 in `.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md`

### Implementation for User Story 3

- [X] T038 [US3] [blockedBy: T037] Implement driver-lease actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `lease-acquire`, `lease-renew`, `lease-release`, `lease-break` with O_CREAT|O_EXCL, TTL 600s, renewal cadence ≤ TTL/3 (default ≤200s) with renewal at U2/U3/U4/U5, live-holder refusal (exit 3), `suspected-alive` (PID alive + heartbeat expired) requiring explicit `--override`, evidence-based break, and lease-history append
- [X] T039 [US3] [blockedBy: T038] Implement reservation actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `reserve`, `reservation-status`, `reservation-break` with O_CREAT|O_EXCL, same-run attach vs refuse, stale-reservation evidence break, and history
- [X] T040 [US3] [blockedBy: T039] Implement identity/reattach/orphan actions in `skills/external/sdd-loop-driver/scripts/line-registry.py`: `verify-identity` (runner/cli start tokens, Linux cwd, branch), `classify-remote` (ssh failure → remote-unreachable, never dead), `reattach-brief`, `orphan-check` using line-owned evidence only
- [X] T041 [US3] [blockedBy: T040] Implement U6 closure in `skills/external/sdd-loop-driver/scripts/line-registry.py` after `integration_result` is recorded: release reservation/lease, `state=closed` with `closed_at`, worktree-retained flag when unmerged (worktree removal belongs to the merged integration sequence only), no active residue, explicit evidence archive
- [X] T042 [P] [US3] [blockedBy: T037] Update `skills/external/sdd-loop-driver/references/dispatch-recipes.md` with the detached runner: `setsid` when available + `nohup` + stdio redirect, CLI child PID + start token, reservation before dispatch, four-piece envelopes, lease renew, and the same Registry fields for ssh+su+nohup remote topology
- [X] T043 [P] [US3] [blockedBy: T037] Update `skills/external/sdd-loop-driver/references/stage-prompts.md` with the reattach program (lease → identity → `--once` → running, done, dead, and remote branches), orphan/stale handling, duplicate-launch prevention, and U6 cleanup; keep 058 verdict/exit semantics
- [X] T044 [P] [US3] [blockedBy: T037] Update `skills/external/sdd-loop-driver/references/watch-model.md` with the attribution layer, reattach snapshot, and remote-unreachable reference; do not change the verdict state machine text or exit codes
- [X] T045 [P] [US3] [blockedBy: T037] Update `skills/external/sdd-loop-driver/SKILL.md` References with lifecycle-decoupling and reattach pointers (reference only)
- [X] T046 [US3] [blockedBy: T038,T039,T040,T041,T042,T043,T044,T045] Run US3 unit/contract/integration tests to green, fix failures, and record the command/output
- [X] T047 [US3] [blockedBy: T046] Sync the skill mirrors with `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`, verify no NEW drift, and re-run the skill structure contract
- [X] T048 [US3] [blockedBy: T047] Execute quickstart S4 (kill/reattach three branches + remote-unreachable) and append the real commands/output/exit status under a `### S4.` heading to `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`; clean up fake processes and temp registries

**Checkpoint**: US3 is independently green; the subagent survives a driver kill, reattach is zero-redispatch, and dead/mismatch preserves worktree and evidence.

---

## Phase 6: User Story 4 - CLI 能力档案的持续沉淀与派发消费 (Priority: P2)

**Goal**: Five CLI profiles exist with eight dimensions and known/unknown provenance; U2 consults them, U4 and U5 update them, each genuine observation records exactly one `cli-profile:<cli>` feedback, and 063 has no duplicate owner.

**Independent Test**: Inspect `references/cli/index.md` plus five profiles; inject a simulated `-p` behavior mismatch and verify provenance update plus exactly one retrievable feedback entry; verify zero feedback when nothing new is observed; verify the 061 matrix remains the eligibility owner.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T049 [P] [US4] Author `tests/contract/test_sdd_loop_driver_cli_profiles.py` covering CLP-01…CLP-17: profile set/location, eight dimensions, known/unknown/provenance, qodercli facts, skeleton discipline, single knowledge point, SKILL H2, U2 consult record, U4 and U5 triggers, write order + exactly one feedback, marker searchability, Probe Object, behavior non-interference, version/defect lifecycle, matrix authority, delivery/mirror/docs, 063 no-duplicate-owner
- [X] T050 [P] [US4] Update `tests/contract/test_sdd_loop_driver_skill.py` to add `CLI Capability Profiles` to the pinned H2 set (immediately before `Wrap-up`) and extend mirror coverage to `references/cli/index.md` plus the five profiles
- [X] T051 [US4] [blockedBy: T049,T050] Capture the red run of T049-T050 in `.specify/specs/064-subagent-concurrency/notes/red-first-evidence.md`

### Implementation for User Story 4

- [X] T052 [US4] [blockedBy: T051] Author `skills/external/sdd-loop-driver/references/cli/index.md` as the schema/observation owner: eight dimensions, known/unknown/provenance table, U2 consult and U4 and U5 observation triggers, `cli-profile:<cli>` feedback marker, `CAPABILITY_MATRIX` boundary, and the profile index
- [X] T053 [P] [US4] [blockedBy: T052] Author `skills/external/sdd-loop-driver/references/cli/qodercli.md` with all eight dimensions: `-p` buffers until exit, `BASH_DEFAULT_TIMEOUT_MS`/`BASH_MAX_TIMEOUT_MS` positive override, 600,000 ms default max, stream-json support, `~/.qoder/logs/` session logs, detached runner requirement, sentinel/buffering/detach facts, and 0/negative timeout semantics marked `unknown` with date/version/evidence pointers
- [X] T054 [P] [US4] [blockedBy: T052] Author `skills/external/sdd-loop-driver/references/cli/claude.md` as an eight-dimension skeleton with explicit `unknown` values and no guessed facts
- [X] T055 [P] [US4] [blockedBy: T052] Author `skills/external/sdd-loop-driver/references/cli/codex.md` as an eight-dimension skeleton with explicit `unknown` values and no guessed facts
- [X] T056 [P] [US4] [blockedBy: T052] Author `skills/external/sdd-loop-driver/references/cli/opencode.md` as an eight-dimension skeleton with explicit `unknown` values and no guessed facts
- [X] T057 [P] [US4] [blockedBy: T052] Author `skills/external/sdd-loop-driver/references/cli/hermes.md` as an eight-dimension skeleton with explicit `unknown` values and a recorded `CAPABILITY_MATRIX` gap (no matrix entry; do not change the matrix)
- [X] T058 [US4] [blockedBy: T052] Add exactly one Probe Object row `skill-sdd-loop-driver-cli-profile | skill-wrapup | skill:sdd-loop-driver | wrap-up` to `shared/definitions/probe-definitions.md`, run `probe-utils.py --action probes --validate`, and confirm no new class/handler/lifecycle point
- [X] T059 [P] [US4] [blockedBy: T052] Add the H2 `CLI Capability Profiles` to `skills/external/sdd-loop-driver/SKILL.md` immediately before `Wrap-up`: consult before dispatch, update after U4 and U5 observations, `references/cli/` is the single knowledge point, `index.md` is schema owner, and the 061 matrix owns dispatch eligibility
- [X] T060 [P] [US4] [blockedBy: T052] Update `skills/external/sdd-loop-driver/references/stage-prompts.md` with the U2 profile consult and dispatch record (`profile_id`, `profile_version`, `observed_cli_version`), U4 and U5 observation comparisons, state-spine `cli_observations`, and the write order (spine → profile provenance → exactly one feedback)
- [X] T061 [P] [US4] [blockedBy: T052] Update `skills/external/sdd-loop-driver/references/dispatch-recipes.md` U2 preflight with a reference-only pointer to the CLI profile index and dispatch-record fields; do not copy profile content
- [X] T062 [P] [US4] [blockedBy: T052] Update `docs/reference/skills/sdd-loop-driver.md` with concurrency/lifecycle and CLI-capability-profile entry sections pointing to the skill references (reference only, no copied tables)
- [X] T063 [US4] [blockedBy: T049] Close the 063 overlap on this branch: read-only inspect `bcf27c77` for `.specify/specs/063-sdd-loop-efficiency/contracts/cli-profiles.md`, `references/cli/README.md`, `skill-sdd-loop-driver-wrapup`, and `tests/unit/test_cli_profile_record.py`; verify none of these artifacts exists in the 064 tree and implement `test_clp_17_no_063_duplicate_owner` as a repository-wide residual scan (any second CLI-profile contract, `references/cli/README.md`, `test_cli_profile_record.py`, or second Probe Object for `skill:sdd-loop-driver` fails the guard); append the branch-verification record and merge-time deletion/pointer steps to `notes/063-overlap-adjudication.md`; never modify the 063 worktree or branch
- [X] T064 [US4] [blockedBy: T052,T053,T054,T055,T056,T057,T058,T059,T060,T061,T062,T063] Run US4 contract tests (CLI profiles + updated skill structure) to green, fix failures, and record the command/output
- [X] T065 [US4] [blockedBy: T064] Sync the two mirror pairs with two scoped writes: `sync-mirrors.py --write --only skills/external/sdd-loop-driver` and `sync-mirrors.py --write --only shared/definitions/probe-definitions.md`; verify no NEW drift and confirm the probe-definitions mirror is byte-identical. MUST NOT run an unscoped `--write` (the 9 pre-existing `shared/definitions` drifts stay untouched)
- [X] T066 [US4] [blockedBy: T065] Run `probe-utils.py --action probes --validate` and `probe-utils.py --action compile-embeds --check`; require exit 0 / zero drift and exactly one object for unit `skill:sdd-loop-driver`
- [X] T067 [US4] [blockedBy: T066] Execute quickstart S5 (profile consultation, no-fact zero-feedback, mismatch exactly one `cli-profile:qodercli` feedback) and append the real commands/output/exit status under a `### S5.` heading to `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`; do not commit the runtime feedback entry

**Checkpoint**: US4 is independently green; all five profiles are present, qodercli facts are sourced, mismatch produces exactly one retrievable feedback, and 063 has no second owner.

---

## Phase 7: User Story 5 - 既有安全与质量边界不回归 (Priority: P2)

**Goal**: The new layers do not change 058 sentinels/verdicts/exit codes, confirmation gates, the no-push policy, independent verification, or the existing test baseline.

**Independent Test**: Run the existing suites with a name-level baseline diff, run the watcher self-test, run the confirmation-gate/push-stub scenario, execute the three mutation drills, and run the single-line compatibility path.

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T068 [US5] [blockedBy: T066] Author `tests/contract/test_non_regression_064.py` with NG-01, NG-02, NG-03, NG-04, NG-05, NG-08, NG-09, and NG-13 guards: watcher exit-code constants unchanged, no `git push` in engine/watcher surfaces, no `--force` worktree removal, stdlib-only imports, no daemon/model API, docs entry present, mirror baseline comparison, the 10 planned test files present, and the NG-03 guard (the full 063 adjudication table is intact and every migrated 063 clause has a 064 carrier — no silent deletion)

### Verification for User Story 5

- [X] T069 [US5] [blockedBy: T068] Run the existing full suite with `.specify/scripts/bash/run-tests.sh tests -q --names-out .specify/specs/064-subagent-concurrency/current-failed.txt`, compare to `baseline-failed.txt` with `comm -13`, and record the result in `verification.md`; if pytest is unavailable, record `green: Unobserved` verbatim (NG-10)
- [X] T070 [US5] [blockedBy: T068] Run `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test`, assert the 12-passed/4-failed baseline is not worsened and new attribution cases pass, and record the output in `verification.md`
- [X] T071 [US5] [blockedBy: T068] Run `tests/contract/test_confirmation_gates_sweep.py` and the push-stub integration scenario; assert zero push actions and unchanged confirmation gates; record in `verification.md`
- [X] T072 [US5] [blockedBy: T069] Mutation drill 1: copy the watcher to `notes/mutation-watch-target.sh`, remove the attribution filter, run `SDD_WATCHER=<copy> run-tests.sh tests/integration/test_two_line_isolation.py -q`, record the red result in `verification.md`, delete the copy, and re-run green
- [X] T073 [US5] [blockedBy: T069] Mutation drill 2: run `SDD_RUNNER_MODE=foreground run-tests.sh tests/integration/test_session_kill_reattach.py -q` to simulate removed detach, record the red result in `verification.md`, then re-run the default detached mode green
- [X] T074 [US5] [blockedBy: T069] Mutation drill 3: copy the engine to `notes/mutation-line-registry.py`, replace the O_CREAT|O_EXCL reservation with check-then-create, run `SDD_ENGINE=<copy> run-tests.sh tests/contract/test_lifecycle_detach_reattach.py -q`, record red in `verification.md`, delete the copy, and re-run green
- [X] T075 [US5] [blockedBy: T069] Run the single-line compatibility regression (quickstart S1 + LR-13/EN-16 cases) and assert 058 U0–U6/sentinel/verdict/exit behavior is unchanged; record in `verification.md`
- [X] T076 [US5] [blockedBy: T072,T073,T074,T075] Execute quickstart S6 (full feature test matrix + name-level baseline comparison) and append the real output under a `### S6.` heading to `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`

**Checkpoint**: US5 is green or honestly Unobserved; the three mutation drills each turn at least one test red, and no boundary is relaxed.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final mirror, probe, test, quickstart, verification, and boundary audit across all stories.

- [X] T077 [blockedBy: T076] Final mirror audit: run `sync-mirrors.py --check --only skills/external/sdd-loop-driver` and `--only shared/definitions/probe-definitions.md`; require zero diff for both, and confirm the 9 pre-existing `shared/definitions` diffs are unchanged (no NEW drift)
- [X] T078 [blockedBy: T077] Final registry/drift check: `probe-utils.py --action probes --validate` exit 0, `probe-utils.py --action compile-embeds --check` zero drift, and `test_clp_12_probe_object_registered` green
- [X] T079 [blockedBy: T077] Final full test run with `run-tests.sh tests -q --names-out .specify/specs/064-subagent-concurrency/current-failed.txt` and `comm -13 baseline-failed.txt current-failed.txt`; record zero NEW failures or the exact `Unobserved` reason in `verification.md`
- [X] T080 [blockedBy: T077] Final quickstart rerun S1–S6 end to end; confirm each scenario's real output is present and current under `### S1.`–`### S6.` headings in `.specify/specs/064-subagent-concurrency/notes/quickstart-run.md`; confirm teardown left no temp registry/worktree/process
- [X] T081 [blockedBy: T079,T080] Write `verification.md` with SC-001…SC-010 statuses, red-first/mutation evidence pointers, deferred_tasks, and the Completion Gate results; run GATE-1…GATE-10 checks against the current tree
- [X] T082 [blockedBy: T081] Final boundary review: no automatic push, no deletion of uncommitted work, no new daemon/external service/runtime dependency/model API, no duplicate 063 CLI-profile owner, and docs/mirrors consistent; record in `verification.md`

**Checkpoint**: All stories are complete, the mirror/probe/test/quickstart evidence is current, and the feature is ready for `/speckit.implement` closure and `/speckit.review`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependency; T001 and T002 can start immediately.
- **Foundational (Phase 2)**: depends on Setup; T003 → T004 → T005 → T006 is strictly sequential because each uses the previous artifact.
- **US1 (Phase 3)**: depends on Foundational; it is the MVP and must complete before US2/US3 because its registry actions and fixtures are reused.
- **US2 (Phase 4)**: depends on US1; the ownership/queue actions extend the same engine file.
- **US3 (Phase 5)**: depends on US1 and may start after US2; the lease/reservation/identity actions extend the same engine file and the same stage-prompt/dispatch surfaces.
- **US4 (Phase 6)**: may start after US1 for documentation context; it is independently testable and does not import US2/US3 code. Its `stage-prompts.md` and `dispatch-recipes.md` edits must be sequenced after US3's edits in this single-agent run.
- **US5 (Phase 7)**: depends on US1–US4 being green; it is the non-regression gate.
- **Polish (Phase 8)**: depends on all stories.

### User Story Dependencies

- **US1 (P1)**: no dependency on other stories after Foundational; it is the MVP.
- **US2 (P1)**: depends on US1's engine core and registry actions; independently testable with its own worktree fixture.
- **US3 (P1)**: depends on US1; shares the engine but has an independent kill/reattach fixture.
- **US4 (P2)**: independent of US2/US3 implementation; depends on US1 only for the docs context that names the concurrency layer.
- **US5 (P2)**: depends on all four stories; verifies boundaries rather than adding runtime behavior.

### Within Each User Story

- Tests are authored first and must be red before implementation; the red evidence row follows the test rows and precedes the implementation rows.
- Engine actions are implemented sequentially in the same `line-registry.py` file.
- Documentation/watcher rows that write different files are `[P]` within a story but are sequenced after the story's red-evidence row.
- Every story ends with a green run, a mirror sync, and a quickstart evidence row.

### Parallel Opportunities

- Setup: T002 can run alongside T001 (different write targets).
- US1 tests: T007, T008, T009 (three test files).
- US1 implementation: T014, T015, T016, T017 (watcher, recipes, prompts, SKILL).
- US2 tests: T021, T022 (two test files).
- US2 implementation: T028, T029, T030 (recipes, prompts, SKILL).
- US3 tests: T034, T035 (two test files).
- US3 implementation: T042, T043, T044, T045 (recipes, prompts, watch-model, SKILL).
- US4 tests: T049, T050 (two test files).
- US4 implementation: T053–T057 (five profile files), plus T059–T062 (SKILL, prompts, recipes, docs) once T052 lands.
- Do not mark two rows `[P]` when they write the same file; the structural validator enforces this.

---

## Parallel Example: User Story 1

```text
Author together (different files):
  T007  tests/contract/test_line_registry_contract.py
  T008  tests/contract/test_line_envelope_contract.py
  T009  tests/integration/test_two_line_isolation.py

Then implement together (different files, after T011):
  T014  watch-target.sh
  T015  dispatch-recipes.md
  T016  stage-prompts.md
  T017  SKILL.md
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 alone. It is the independently valuable attribution layer that prevents the observed cross-line incident; it has its own two-line fixture and can be validated without US2/U3/U4. US2 and US3 are also P1 and should follow immediately, because they close the independent workspace-destruction and lifecycle-loss risks.

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete US1 (Phase 3) and validate the two-line checkpoint.
3. Complete US2 (Phase 4) and validate the worktree/integration checkpoint.
4. Complete US3 (Phase 5) and validate the kill/reattach checkpoint.
5. Complete US4 (Phase 6) and validate the profile/feedback checkpoint.
6. Complete US5 (Phase 7) and the Polish phase (Phase 8).

### Incremental Delivery

Each story adds value without breaking the previous one: US1 makes intake safe, US2 makes writing safe, US3 makes long runs recoverable, US4 makes CLI behavior knowledge durable, US5 proves the existing safety boundaries still hold.

### Execution Notes

- This is a single-agent, single-feature run; the recommended execution order is the phase order above.
- If a story is split across workers, respect the `[P]` file boundaries and the `[blockedBy:]` tags; never let two workers edit `line-registry.py`, `stage-prompts.md`, `dispatch-recipes.md`, or `SKILL.md` concurrently.
- Do not commit runtime records (`feedback/`, `session/`, `exec-quant/`, `baseline-failed.txt` unless the implement convention explicitly includes it); only feature artifacts and evidence listed in the task row are committed.

---

## Notes

- **PLAN-EDIT**: none. This tasks breakdown only decomposes the approved plan; it does not rewrite plan.md, requirements.md, or any design artifact.
- **D-T01**: Tests resolve the engine and watcher through `SDD_ENGINE`/`SDD_WATCHER` environment variables (defaulting to the skill files) so the three mutation drills can run against copies without mutating the source tree.
- **D-T02**: US5 adds `tests/contract/test_non_regression_064.py` as its independent test. Plan's 10-file matrix remains the minimum gate; this file is additive non-regression coverage, not a replacement.
- **D-T03**: Mirror sync runs as a build step at the end of each story that edits skill sources, then is audited once in Polish. The runtime WI-11 "mirrors once per integration batch" rule governs the mechanism being built, not this repository's own source→runtime projection.
- **D-T04**: 063 is not merged on this branch (`git worktree list`: 064 at `535ce680`, 063 at `bcf27c77`). The deletion/pointer actions are merge-time obligations recorded in `notes/063-overlap-adjudication.md`; this branch verifies no 063 artifact exists and installs `test_clp_17_no_063_duplicate_owner` as a guard.
- **D-T05**: `pytest` is unavailable at generation time; green is Unobserved until implement resolves an interpreter through `.specify/scripts/bash/run-tests.sh`. No task may claim a pass without a real run.
- **D-T06**: `setsid` is absent on macOS; US3 uses `nohup + disown` locally and `setsid` when available on Linux, per plan Assumptions.
- **D-T07**: The new `CLI Capability Profiles` H2 is inserted immediately before `Wrap-up`; the pinned H2 list in `tests/contract/test_sdd_loop_driver_skill.py` is updated in the same story.
- **D-T08**: US1, US2, and US3 are all P1. The MVP is US1, the smallest independently valuable increment; full delivery is US1→US2→US3→US4→US5.
- **D-T09**: Task IDs are stable and contiguous T001–T082; this is the first tasks.md for 064. A rerun must validate-and-amend, never renumber.
- **D-T10**: No new command, skill, daemon, external service, model API, or runtime dependency is introduced; the engine is Python 3 stdlib-only and the watcher remains bash.
- **D-T11**: The 10 planned test files are `tests/unit/test_line_registry_engine.py`, `tests/contract/test_line_registry_contract.py`, `tests/contract/test_line_envelope_contract.py`, `tests/contract/test_workspace_isolation_contract.py`, `tests/contract/test_lifecycle_detach_reattach.py`, `tests/contract/test_sdd_loop_driver_cli_profiles.py`, the updated `tests/contract/test_sdd_loop_driver_skill.py`, and the three `tests/integration/` files; T068 adds the eleventh non-regression file.
- **D-T12**: The 063 worktree is a different branch; never `cd` into it, never edit it, and use `git show bcf27c77:...` for read-only inspection.
