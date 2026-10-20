# Contract: Line Registry（线路登记册）

**Feature**: 064
**Owning FR**: FR-001…FR-007, FR-016（注册表部分）, FR-017（注册部分）
**实体**: `data-model.md` § E1；存储/原子性决策 `research.md` § R1
**Implementation surface**: `skills/external/sdd-loop-driver/scripts/line-registry.py`（Python 3 stdlib-only）+ `references/stage-prompts.md`（U0.5/U6 程序）+ `SKILL.md`（入口）

## Clauses

- **LR-01（位置与覆盖）**: 同一 OS 用户一份环境级 Registry。默认目录 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines`；`SPECIFY_LINE_REGISTRY_DIR` 覆盖。目录 MUST 位于任一 line 的 worktree 之外，且无需扫描项目目录即可发现。跨机器/多用户共享默认不支持；远端 line 只在驱动侧 Registry 增加最小远端字段（FR-001, FR-065）。
- **LR-02（注册与注销时点）**: 每条 line 在 U0.5（首次派发前）注册；U6 收尾后注销（`state=closed`）。注册/注销失败 MUST 显式上送并停止该 line 的启动/收尾断言，MUST NOT 静默继续（FR-002, FR-057）。
- **LR-03（每线文件与原子写）**: 每线一个 `<line_id>.json`。写入 MUST 为同目录临时文件 + `fsync(file)` + `os.replace` + `fsync(dir)`；读取方不得观察到截断/半写（FR-002, FR-003）。
- **LR-04（同线锁）**: 同线读-改-写 MUST 经 `<line_id>.lock` 的排他锁串行化（`fcntl.flock`，超时即失败上报）。跨线写入 MUST NOT 共享锁或互相覆盖（FR-003）。
- **LR-05（读取保证）**: 并发读取方 MUST 始终得到可解析 JSON、唯一 `line_id`、且不丢失其他 line 条目；`list --active` 只返回 `active/waiting`，并输出可机读摘要（`line_id/run_id/project/branch/stage/state/updated_at`）（FR-003, FR-010, SC-009）。
- **LR-06（身份格式与生命周期）**: `line_id` 环境内唯一且证据存续期内不复用；`run_id` 标识一次执行尝试。重接线 MUST 复用原 `run_id`；重试/重派 MAY 产生新 `run_id` 并保留 `run_history`。二者与 feedback/exec-quant 的 `(unit_id, run_id)` 不是同一命名空间（FR-004, `data-model.md` V-LR-2/V-LR-3）。
- **LR-07（字段完整性）**: Registry 条目 MUST 覆盖 `data-model.md` § E1 表中 `always/active/after dispatch/write lines/U6` 规定时点的字段；缺字段的写入被拒绝（FR-005, V-LR-1）。FR-005 的 `qodercli_pid` 映射为 `cli_pid`（`cli=qodercli` 时同一值，Decision D-02）。
- **LR-08（远端最小字段）**: 远端条目 MUST 另含 `remote.alias`、`remote.run_user`、`remote.remote_root`；Registry 始终位于驱动侧 OS 用户，远端经 ssh 读取/校验（FR-058, FR-065, V-LR-8）。
- **LR-09（状态封闭集与同步点）**: `state` MUST ∈ `active/waiting/stalled/completed/orphaned/stale/closed`；六个同步点（U0.5/U2/U3/U4/U5/U6）各自写入的状态值由 FR-006 的映射表唯一规定，`completed` 是唯一 pre-merge 状态；MUST NOT 与状态脊矛盾（映射见 `data-model.md` V-LR-9）（FR-006, V-LR-4/V-LR-9）。
- **LR-10（stale 识别与显式清理）**: stale = PID 死亡、PID 复用（start token 不符）、cwd/branch 不符、或证据超期（沿用既有 watcher 心跳/阶段期限语义，不另设阈值）。清理 MUST 是显式、留痕动作；MUST NOT 盲目删除/覆盖其他 line 登记（FR-007, V-LR-10）。
- **LR-11（注册失败语义）**: Registry 目录不可写或已有 JSON 损坏 → 注册/更新以非零退出并给出路径与原因；line MUST NOT 回退到项目内共享路径启动（Edge Case, FR-002）。
- **LR-12（并发完整性验收）**: N 条 line 并发注册/更新后，Registry 可解析率 100%、丢失条目数 0、重复 `line_id` 数 0；同线锁下无半写（FR-003, SC-009）。
- **LR-13（单线兼容）**: 单线运行 MUST 同样注册并走同一原子写/状态同步路径；不得因归属机制改变 U0–U6 既有行为（FR-017, FR-068）。受控例外：注册/注销失败时按 LR-02/LR-11 显式上送并停止该线，不继续启动/收尾断言。

## Engine Actions (interface)

> 本表是 `line-registry.py` 动作接口的唯一 owner；`contracts/line-envelope-and-ingress.md`、`contracts/lifecycle-detach-reattach.md` 与 quickstart 只引用本表，不另立接口清单。

`line-registry.py --action <action> [flags] [--format json]`

| action | 关键输入 | 输出（JSON） | 退出码 |
|--------|----------|--------------|--------|
| `register` | `--line-id` `--run-id` `--project-dir` `--repo-root` `--state` `[--manifest]` | 条目快照 | 0 / 2 / 6 |
| `update` | `--line-id` + 字段 flags | 条目快照 | 0 / 2 / 3 / 6 |
| `deregister` | `--line-id` `--reason` | 终态摘要 | 0 / 2 / 6 |
| `list` | `--active` / `--all` | 条目摘要数组 | 0 / 2 / 6 |
| `resolve-message` | `--message` `[--clarified]` | `route/clarify/ambiguous-stop/no-active/no-match` | 0 / 2 / 6 |
| `verify-identity` | `--line-id` `[--probe-json]` | `data-model.md` § E6 JSON | 0 / 2 / 4 / 6 |
| `classify-remote` | `--probe-json` | `{identity, reason}` | 0 / 2 / 6 |
| `reattach-brief` | `--line-id` | Registry + 状态脊 + 四件套 + reservation/lease 摘要 | 0 / 2 / 6 |
| `lease-acquire` | `--line-id` `--session` `--pid` `[--ttl]` | lease 快照 | 0 / 2 / 3 / 6 |
| `lease-renew` | `--line-id` `--session` | lease 快照 | 0 / 2 / 3 / 6 |
| `lease-release` | `--line-id` `--session` | 释放摘要 | 0 / 2 / 3 / 6 |
| `lease-break` | `--line-id` `--reason` `--evidence-ref` `[--override]` | 破除记录 | 0 / 2 / 3 / 6 |
| `reserve` | `--line-id` `--stage` `--run-id` `--pid` `--start-token` | reservation 快照 | 0 / 2 / 3 / 6 |
| `reservation-status` | `--line-id` `--stage` | reservation 摘要 | 0 / 2 / 6 |
| `reservation-break` | `--line-id` `--stage` `--reason` `--evidence-ref` | 破除记录 | 0 / 2 / 3 / 6 |
| `orphan-check` | `--line-id` | `{orphaned, evidence[]}` | 0 / 2 / 6 |
| `ownership-check` | `--line-id` `--manifest` | `{overlaps[], decision: proceed\|waiting, holder_line_id?, waiting_reason?}` | 0 / 2 / 6 |
| `release-ownership` | `--line-id` `--reason` `--evidence-ref` | 释放记录 | 0 / 2 / 3 / 6 |
| `promote-waiting` | `--line-id` | 新状态 | 0 / 2 / 3 / 6 |
| `integration-enqueue` | `--line-id` `--at` | 条目 | 0 / 2 / 6 |
| `integration-plan` | — | 有序条目数组 | 0 / 2 / 6（环/依赖非法=6） |
| `integration-record` | `--line-id` `--result` `--commit` | 条目 | 0 / 2 / 6 |
| `allocate-resources` | `--line-id` `[--port-range-start]` `[--block-size]` `[--cap]` | 资源摘要 | 0 / 2 / 3 / 6 |
| `archive-runtime` | `--line-id` `--worktree` `--dest` | 归档清单 | 0 / 2 / 6 |

退出码封闭集：`0` 成功；`2` 用法/校验错误；`3` 有活跃资源持有者（lease/reservation/ownership/cap）；`4` 身份无法计算（registry/状态脊/探针缺失）；`6` Registry I/O 或数据损坏。`resolve-message` 与 `verify-identity` 的判定结果走 JSON，不以退出码表达正常判定。

## Traceability

| Clause | FR/SC | Planned tests |
|--------|-------|---------------|
| LR-01/LR-11 | FR-001, FR-002 | `test_line_registry_contract.py::test_lr_01_location_override`, `test_lr_11_unwritable_fails_start` |
| LR-02/LR-09/LR-13 | FR-002, FR-006, FR-017, FR-068 | `test_lr_02_register_deregister`, `test_lr_09_state_enum_and_spine_consistency`, `test_lr_13_single_line_compat` |
| LR-03/LR-04/LR-05/LR-12 | FR-003, SC-009 | `test_lr_03_atomic_replace`, `test_lr_04_same_line_lock`, `test_lr_12_concurrent_registration` |
| LR-06/LR-07 | FR-004, FR-005 | `test_lr_06_id_formats_and_run_history`, `test_lr_07_required_fields` |
| LR-08 | FR-058, FR-065 | `test_lr_08_remote_minimal_fields` |
| LR-10 | FR-007 | `test_lr_10_stale_detection_explicit_cleanup` |
