# Contract: 进度可见与驱动会话解耦（progress-decoupling）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-026…FR-035
**载体**: `references/efficiency-model.md`、`references/dispatch-recipes.md`、`references/watch-model.md`、`scripts/stage-runner.sh`、`scripts/derive-live-log.py`、`scripts/watch-target.sh`、`docs/reference/skills/sdd-loop-driver.md`

- **PD-01（stream-json 主路径）**: 阶段 runner MUST 默认以 [[STR-001]] 调用阶段 CLI，并把原始事件流完整落盘为 raw stream 证据文件（`raw-<line>-<stage>.jsonl`）；stderr 单独落 runner-log，不混入 raw（FR-026）。CLI 行为事实（输出模式支持、事件形状、哨兵可靠性、超时上限）以 Feature 064 的 `references/cli/<cli>.md` 为单一 owner（064 `contracts/cli-profiles.md` CLP-02）；本契约只规定 runner 在这些事实下的行为，MUST NOT 复制档案内容。派发前 MUST 按 064 CLP-08 只读查档；文档记录该 CLI 不支持 stream-json 时按 PD-05 降级，不得强传旗标。**派发资格**：supported CLI = Feature 061 的 `CAPABILITY_MATRIX` eligible 集合（owner: `scripts/python/execution-config.py`；064 CLP-15 同口径）；CLI 档案存在不等于可派发，本契约只决定输出模式默认，不定义派发资格。
- **PD-02（增量派生）**: runner MUST 有一个确定性派生步骤把 raw stream 在运行期增量转换为紧凑实时日志：每个有意义的进度事件输出一行可读进度，MUST NOT 缓冲到进程退出；实时日志 MUST 可追加读取与尾部跟踪。非终止事件只产生带前缀的进度行（FR-027）。每个有效进度事件从 runner 接收并写入 raw stream 的时刻，到对应派生行写入紧凑实时日志的时刻，延迟 MUST ≤120 秒（事件→派生行延迟）；无事件的静默区间不适用该阈值；每条派生行 MUST 可追溯到一条 raw 事件，阶段无事件时伪造进度行数 MUST 为 0（SC-007）。
- **PD-03（哨兵契约）**: 阶段正常结束时，紧凑实时日志的最后一个非空行 MUST 恰好是阶段哨兵（大写阶段名 + [[STR-002]]）。派生 MUST 取 CLI 终止 `result` 事件的文本并在 EOF 时作为最后内容追加；MUST NOT 让 JSON 信封、事件元数据或非终止事件中的哨兵字样满足判定（FR-028）。
- **PD-04（watcher 只做可见性）**: watcher MUST 把流式进度只当作可见性信号：进度行数/增长 MUST NOT 单独产生 `DONE` 或 `TIMEOUT`；完成仍须哨兵 + U4 独立校验，超时仍只由阶段 deadline 产生。既有判定顺序、退出码与窗口/deadline 语义 MUST 保持不变；判定表与退出码的精确值 owner 是 `scripts/watch-target.sh` 的 `--help` / `--self-test`，本契约不复写数值（FR-029）。`BASH_DEFAULT_TIMEOUT_MS` / `BASH_MAX_TIMEOUT_MS` 是宿主工具调用上限，不是阶段 deadline；派发 MUST 按 Feature 064 的 CLI 档案设置兼容的工具超时，阶段 TIMEOUT MUST 仍只由 deadline 产生，工具上限导致的提前终止 MUST NOT 被记作阶段超时。
- **PD-05（降级）**: CLI 不支持 stream-json（能力探测失败）或派生运行时缺失/派生失败时，runner MUST 回退既有缓冲模式，在状态记录 [[STR-004]] 与原因，并继续以退出记录 + 哨兵 + deadline 判定。派生失败后 runner 的收口 MUST 先跑一次性 `--finish` 从 raw 恢复终止 `result` 文本；恢复成功即写入 live log（最后非空行 = 哨兵）并记 `degraded:derivation-recovered`。若 raw 无终止 result 事件但最后一个非空行恰为哨兵（CLI 未按 stream 输出），MUST 走 buffered fallback 并记 `degraded:buffered-fallback`。两者皆无 → `sentinel=0`，按 INCOMPLETE 处理——这是缺失完成证据，不是降级导致的阶段失败。降级 MUST NOT 产生伪完成或阶段失败（FR-030）。
- **PD-06（nohup 双拓扑）**: 阶段派发 MUST 在本地与远端两种拓扑下都完全脱离驱动会话：以 `nohup` 启动 runner，stdin 接 `/dev/null`，stdout/stderr 重定向到文件；远端保留 `ssh + su + nohup` 形态，本地补齐等价形态。脱离 MUST 是默认形态；派发记录 MUST 写 `detached=yes|no`，遗漏 nohup/`</dev/null` MUST 标记「未脱离」并记录风险，不计为受保护运行（FR-031）。
- **PD-07（脱离后监听/校验/重入）**: 脱离后四件套（pid/status/log/heartbeat）与状态脊字段 MUST 保持；新会话 MUST 能用 `--once` 快照接管；已完成的阶段 MUST 被核验而非重新派发；脱离 MUST NOT 削弱 U3/U4（FR-032）。
- **PD-08（watcher 证据面与自测）**: watcher MUST 支持把派生实时日志作为哨兵来源（`--log`），并保留 raw stream 作为证据（可选 `--raw-stream` 输出成长/字节数，只作可见性）。其自测 MUST 覆盖：非终止事件中的哨兵字样不计、终止 result 事件中的哨兵计、派生失败降级不伪完成、脱离 runner 在驱动退出后存活（FR-033）。既有自测的平台假设（`/proc`、`pgrep` 输出差异）与时序夹具 MUST 一并修正为可跨平台运行或显式跳过。
- **PD-09（不新增等待形态与服务）**: 驱动等待 MUST 仍是既有长轮询窗口；实时日志只在窗口内读取用于可见性；MUST NOT 新增独立 `sleep` 回合或固定 cadence 空转。raw stream 与派生实时日志 MUST 作为 U4/U5 与事后审计证据保留；MUST NOT 引入新的常驻服务、守护进程或外部依赖（FR-034/FR-035）。
- **PD-10（runner 脚本接口）**: `scripts/stage-runner.sh` MUST 以参数接收 CLI、CLI 参数、项目目录、提示词文件、哨兵、线/阶段标签、状态目录与模式（`auto|stream|buffered`），写四件套与 `runner-log`；退出码 MUST 等于 CLI 退出码。`scripts/derive-live-log.py` MUST 自包含（Python 标准库）、支持管道增量读取与一次性 `--finish` 提取，MUST NOT 需要 `jq` 或网络。

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| PD-01 | FR-026 | `test_pd_01_stream_default_and_raw` |
| PD-02 | FR-027, SC-007 | `test_pd_02_incremental_live_log`；单测 `test_derive_live_log.py` |
| PD-03 | FR-028, SC-009 | `test_pd_03_sentinel_from_result_only` |
| PD-04 | FR-029, SC-009 | `test_pd_04_watcher_unchanged`；`watch-target.sh --self-test` |
| PD-05 | FR-030, SC-011 | `test_pd_05_degradation_marker` |
| PD-06 | FR-031 | `test_pd_06_nohup_both_topologies` |
| PD-07 | FR-032, SC-008 | `test_pd_07_reentry_once`；集成 `test_sdd_loop_efficiency_runner.py` |
| PD-08 | FR-033, SC-008, SC-009 | `test_pd_08_watcher_raw_and_selftests` |
| PD-09 | FR-034, FR-035 | `test_pd_09_no_new_wait_or_service` |
| PD-10 | FR-026, FR-035 | `test_pd_10_runner_interface`；集成 runner 测试 |
