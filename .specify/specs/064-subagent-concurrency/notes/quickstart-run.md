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
