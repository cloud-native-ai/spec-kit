# Quickstart Run Evidence — Feature 064

Real commands and outputs executed in this worktree. Temp registries/worktrees are removed at the end of each scenario.

### S1. 单线兼容 + 信封（回归）

Command shape: `bash /tmp/run-s1-s2.sh` (temp `SPECIFY_LINE_REGISTRY_DIR`, fixture four-piece, engine register/update, watcher `--once`).

```text
== S1.1 register ==
state active line demo-20261020T120000Z-a1b2
== S1.2 four-piece + update ==
stage plan state active runner_pid 34758
active_count 1
== S1.3 watcher own ==
WATCH label=demo-20261020T120000Z-a1b2 verdict=DONE pid=alive heartbeat=fresh anomaly=no sentinel=yes rc=0 elapsed=0 reason=exit-record-sentinel line=demo-20261020T120000Z-a1b2 run=r20261020T120000Z-a1b2 attribution=own
EVIDENCE label=demo-20261020T120000Z-a1b2 last="PLAN-DONE" status="exit=0 sentinel=1" line=demo-20261020T120000Z-a1b2 run=r20261020T120000Z-a1b2 attribution=own
watcher_exit=0
== S1.4 legacy watcher ==
WATCH label=demo-20261020T120000Z-a1b2 verdict=DONE pid=alive heartbeat=fresh anomaly=no sentinel=yes rc=0 elapsed=0 reason=exit-record-sentinel line= run= attribution=legacy
EVIDENCE label=demo-20261020T120000Z-a1b2 last="PLAN-DONE" status="exit=0 sentinel=1" line= run= attribution=legacy
legacy_exit=0
```

Exit status: watcher own `0`, legacy `0`; the 058 DONE path is unchanged and the envelope is carry-only.

### S2. 双线同哨兵 + 无标识消息 + foreign 事件

Same script continues with a second active line in the same registry.

```text
== S2.1 register second line ==
== S2.2 clarify ==
decision clarify questions 1 candidates 2
== S2.3 ambiguous-stop ==
decision ambiguous-stop has_question False candidates 2
== S2.4 explicit route ==
decision route target demo-20261020T120000Z-a1b2
== S2.5 foreign event ==
WATCH label=demo-20261020T120000Z-a1b2 verdict=RUNNING pid=alive heartbeat=fresh anomaly=no sentinel=no rc=na elapsed=0 reason=alive line=demo-20261020T120000Z-a1b2 run=r20261020T120000Z-a1b2 attribution=foreign
foreign_exit=10
== S2.6 stub count ==
stub_calls=0
```

Exit status: foreign injection returns `10 RUNNING` (never DONE) with `attribution=foreign`; `ps`/`pgrep`/`pidof` PATH stubs recorded zero invocations.

Teardown: both scenarios use `mktemp -d` and `rm -rf` the temp root; no registry entry, worktree, or process remains.

### S3. 同仓双写线：worktree、所有权与集成队列

Command: `bash /tmp/run-s3.sh` (temp git repo + two worktrees; no push).

```text
== S3.1 worktrees ==
== S3.2 ownership ==
L1 proceed overlaps 0
L2 waiting holder wt-20261020T130000Z-a1b2
== S3.3 commits + fsck ==
fsck=ok
commits=3
== S3.4 enqueue + plan replay ==
replay=identical
order [(1, 'wt-20261020T130000Z-a1b2'), (2, 'wt-20261020T130001Z-c3d4')]
== S3.5 runtime archive once ==
files ['.specify/memory/feedback/entry.md']
== S3.6 failure retention ==
worktree_retained=yes
```

Exit status: all engine calls `0` (except the intentional waiting decision, which is a JSON result, not an error); `git fsck --no-dangling` exit 0. The evidence directory is excluded from the runtime archive; a failed integration record keeps the worktree.

Teardown: temp repo/worktrees/registry removed (`rm -rf` of the mktemp root).

### S4. 主会话 kill / 重接线

Command: `python3 /tmp/run-s4.py` (temp project/registry; detached fake stage; driver killed with SIGHUP).

```text
== S4.1 dispatch ==
lease holder old ttl 600
second reserve: attach
== S4.2 kill driver ==
runner_alive_after_driver_kill: True
heartbeat_advancing: True
== S4.3 new session lease ==
lease_acquire_exit: 3 holder_state: expired
identity: ok cwd: unsupported hint: running
== S4.4 snapshot ==
WATCH label=life-… verdict=RUNNING pid=alive heartbeat=fresh anomaly=no sentinel=no rc=na elapsed=0 reason=alive line=life-… run=r… attribution=own
watch_exit: 10
WATCH label=life-… verdict=DONE pid=alive heartbeat=fresh anomaly=no sentinel=yes rc=0 elapsed=0 reason=exit-record-sentinel line=life-… run=r… attribution=own
watch_exit: 0
== S4.5 remote unreachable ==
remote-unreachable
```

Exit status: lease refusal `3` (expired holder, explicit break required); snapshot `10 RUNNING` → `0 DONE` without a second dispatch; reservation attach on the second start; remote probe classified `remote-unreachable`. Teardown killed the fake runner/driver and removed the temp root.

> **Post-review (2026-10-20)**: the abbreviated `life-…` output above is a dated record. The authoritative S4 evidence is now the behavior test `test_delivered_runner_recipe_survives_driver_kill_and_reattaches`, which uses the delivered `run-stage.sh`, real line/run IDs, a real driver-group SIGHUP, and prints full watcher lines.

### S5. CLI 档案观测 → 恰好一条反馈

Command: `bash /tmp/run-s5.sh` (temp feedback workspace; profile copy for the simulated mismatch; no runtime feedback committed).

```text
== S5.1 qodercli dimensions ==
invocation => known
output_mode => known
timeouts => known
sentinel => known
buffering => known
session_logs => known
detach_signals => known
defects_versions => known
== S5.2 no new fact -> zero feedback ==
count 0
== S5.3 mismatch -> spine -> provenance -> exactly one feedback ==
count 1
== S5.4 probe registry ==
Probe registry valid: 10 classes, 114 internal + 0 external objects
contains_object=1
```

Exit status: all commands `0`; zero new feedback when no fact changed; exactly one retrievable `cli-profile:qodercli` entry after the simulated `-p` mismatch; the probe object is registered and the registry validates.

> **Post-review (2026-10-20)**: `/tmp/run-s5.sh` was ephemeral, so the output above is retained only as a dated record. The reproducible counterpart is committed at `tests/fixtures/cli_observation.py` and executed by `test_clp_10_observation_fixture_cardinality`, which asserts the same cardinality from `HEAD`: no new fact → one spine event, zero feedback, profile bytes unchanged; mismatch → one spine event, one provenance row, exactly one retrievable `cli-profile:qodercli` entry.

### S6. 非回归收口（全特性矩阵 + 名称级基线对比）

Feature matrix command (all 11 planned test files, including the additive non-regression file):

```bash
SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 \
  bash scripts/bash/run-tests.sh tests/unit/test_line_registry_engine.py \
  tests/contract/test_line_registry_contract.py tests/contract/test_line_envelope_contract.py \
  tests/contract/test_workspace_isolation_contract.py tests/contract/test_lifecycle_detach_reattach.py \
  tests/contract/test_sdd_loop_driver_cli_profiles.py tests/contract/test_sdd_loop_driver_skill.py \
  tests/contract/test_non_regression_064.py tests/integration/test_two_line_isolation.py \
  tests/integration/test_worktree_integration_queue.py tests/integration/test_session_kill_reattach.py \
  -q --names-out /tmp/064-feature-failed.txt
```

```text
151 passed in 56.45s
# failed-name list written: /tmp/064-feature-failed.txt (       0 entries)
```

Full suite with name-level baseline comparison:

```bash
SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 \
  bash scripts/bash/run-tests.sh tests -q --names-out .specify/specs/064-subagent-concurrency/current-failed.txt
comm -13 .specify/specs/064-subagent-concurrency/baseline-failed.txt \
         .specify/specs/064-subagent-concurrency/current-failed.txt
```

```text
69 failed, 4077 passed, 1 skipped, 4 warnings in 295.19s
# failed-name list written: .specify/specs/064-subagent-concurrency/current-failed.txt (69 entries)
comm -13 output: <empty>        # zero NEW failures
comm -23 (fixed): tests/contract/test_sdd_loop_driver_skill.py::test_c12_mirror_byte_identical,
                  tests/contract/test_sdd_loop_driver_skill.py::test_c18_mirror_pair_no_drift
baseline=71 current=69
```

Watcher self-test: `18 passed, 4 failed`; the four failures are the recorded macOS baseline (`pid-reuse`, `zombie`, `manifest`, `pgrep-zero-match-trap-reproduced`); all new attribution and lease-renew-hook cases pass.

Mutation drills (each re-run green after deleting the copied mutation):
- Drill 1 (attribution filter removed): `2 failed, 4 passed` in `test_two_line_isolation.py`; after deletion `6 passed`.
- Drill 2 (`SDD_RUNNER_MODE=foreground`): `4 failed` in `test_session_kill_reattach.py`; default mode `4 passed`.
- Drill 3 (reservation exclusivity removed): `1 failed, 15 passed` (`test_lc_04_reservation_concurrent_single_winner`); after deletion `16 passed`.

Teardown: all scenarios use `mktemp` roots and remove them; no temp registry, worktree, or fake process remains (verified by each scenario's `finally` cleanup).
