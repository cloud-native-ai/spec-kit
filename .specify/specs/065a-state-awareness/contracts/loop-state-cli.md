# Contract: `loop-state.py` CLI 与进程契约

**Scope**: Feature 065 / Slice 065a。定义入口、参数解析、退出码、只读边界与 `--probe`/`--self-test` 的进程级行为。
**Owner note**: watcher 的判定状态机、信号优先级与退出码归 `scripts/watch-target.sh`；本契约只规定聚合器如何**消费**它们，不复制其规则。

## 1. 入口

- **LS-01**: 入口文件 MUST 为 `skills/external/sdd-loop-driver/scripts/loop-state.py`（运行时镜像 `.specify/skills/sdd-loop-driver/scripts/loop-state.py` 由 `sync-mirrors.py` 生成）。实现 MUST 仅使用 Python 3 标准库（Python `>=3.8` 语法），MUST NOT 引入常驻服务、后台进程或外部依赖。
- **LS-02**: 动作面 MUST 为 `--action snapshot|recover|check-spine` 与 `--self-test`。065a MUST 实现 `snapshot` 与 `--self-test`；`recover` 与 `check-spine` MUST 返回结构化拒绝信封（`schema_version=1`、`action=<name>`、`applied=false`、`result=failed`、`steps=[]`、`reason=not-implemented-in-065a`、`owner=065b|065c`、`message=<一句用户可读说明>`）并以退出码 `1`（拒绝）结束。两个动作的行为实现归 065b（`check-spine`）与 065c（`recover`），本切片 MUST NOT 预置其副作用路径。
- **LS-03**: `--help` MUST 列出三个动作、全部参数，以及 `0/1/2` 退出码阶梯的语义；MUST 明示 watcher 的判定码是**数据**，本入口不复用、不重定义。`--self-test` MUST 断言该文本包含阶梯语义。

## 2. 输入解析

- **LS-04**: 解析顺序 MUST 为：显式 `--spine` / `--state-dir` / `--spec-dir` / `--repo` / `--probe` 覆盖 → 按 `--line-id` 读取 Registry 条目 → 失败。`--line-id` 缺失 MUST 以退出码 `2` 拒绝。每个路径的逐项优先级见 `data-model.md` §5.1 与 `research.md` R-02。
- **LS-05**: Registry 缺失但状态脊与四件套可解析时，MUST 继续求值并在 `registry.status` 记 `missing`；MUST NOT 因 Registry 缺失判 `UNKNOWN`（`IA-03` 的未派发判据除外）。
- **LS-06**: 任何必需输入不可解析时 MUST 显式记为 `missing`（值用 `null`），MUST NOT 以零值、空串、`"ok"` 或猜测默认值填充。
- **LS-07**: `stage` MUST 依次取 `--stage` → Registry `stage`；两者皆无时 `stage=null`，产物映射不可建立：spec 路径可读时 `artifacts.status=present`、`value_state=unknown`，否则 `status=missing`、`value_state=na`。

## 3. 退出码阶梯

- **LS-08**: 退出码封闭集 MUST 为 `0`（求值成功；任何 `loop_state` 都是数据，不编码为退出码）、`1`（拒绝或校验失败；含 `LS-02` 的未实现动作拒绝）、`2`（参数错误或必需输入不可读）。`snapshot` 在成功求值后 MUST 返回 `0`，包括 `loop_state=UNKNOWN`、`STALLED`、`DEAD` 或动作建议为 `stop` 的情形。
- **LS-09**: 本入口 MUST NOT 复用或重定义 watcher 的判定退出码 `10–16`；watcher 的退出码只写入 `watch_verdict.exit_code` 作为数据。

## 4. 只读边界

- **LS-10**: 除显式 `--out <file>` 外，`snapshot` MUST NOT 写文件、改 mtime、改状态脊/四件套/Registry、杀进程或修改工作树。`--out` 写入 MUST 为同目录临时文件 + 原子替换；目标路径落在解析后的 `state_dir` 或 `repo` 工作树内时 MUST 以退出码 `2` 拒绝。`--out` 内容 MUST 与 stdout 信封相同。

## 5. `--probe`

- **LS-11**: `--probe <file>` MUST 接受两种 JSON 形状，并按下列判据分流：

  | 形状 | 必需键 | 行为 |
  |------|--------|------|
  | (a) 快照信封 | `schema_version=1`、`watch_verdict`、`evidence` | 逐字消费 probe 的 `spine`/`registry`/`watch_verdict`/`evidence`；本地重算 `interruptions`/`recovery_action`；`loop_state` 在 `watch_verdict.present=true` 时逐字取 probe 的 verdict（`IA-05`），否则走 derived；`evidence_source=probe`；probe 自带 freshness 视为权威 |
  | (b) 最小可达性 | `schema_version=1`、`reachable=false`、`reason` | 输出 `STALLED` + `remote-unreachable` + 动作 `stop`；全部信号 `missing` |

- **LS-12**: JSON 不可解析、`schema_version≠1`、形状 (b) 的 `reachable=true`（无可求值证据）、或 probe 中 `line_id` 与 `--line-id` 不一致时，MUST 以退出码 `2` 拒绝。未知字段 MUST 被忽略。
- **LS-13**: 提供 `--probe` 时，MUST NOT 调用本地 watcher，MUST NOT 读取本地状态脊/四件套/产物/git 证据；与 `--spine`、`--state-dir`、`--spec-dir`、`--repo`、`--watch-script` 同时出现 MUST 以退出码 `2` 拒绝（互斥，不得混用本地证据）。

## 6. watcher 委托

- **LS-14**: 仅当存在活动 watch target（`pid` 或 `status` 记录存在、哨兵存在、或 `stage_started_at` 可读）、且非 `not-dispatched`、且未提供 `--probe` 时调用 watcher，MUST 以 runner 同一执行身份执行 `watch-target.sh --once`，传入既有四件套路径、`--sentinel <STAGE>-DONE`、`--deadline-epoch`（来自脊）与 `--stage`。归属参数的选取 MUST 按以下规则，避免把无 `run=` 的现行信封误判为 `unattributed` 而丢弃终止证据：

  | 条件 | 调用形态 |
  |------|----------|
  | `run_id` 已知，且 Registry `meta_paths` 中存在 meta 文件，或 status 与 pid 信封均带与 `run_id` 相等的 `run=` | 归属形态：附 `--line-id <id> --run-id <run> --registry <dir> --meta <file>` |
  | `run_id` 未知或归属不可证，且 `stale_signals` 为空 | 兼容形态：不附归属参数（watcher 输出 `attribution=legacy`） |
  | 归属不可证且 `stale_signals` 非空 | 不调用 watcher；`present=false`、`reason=unavailable`、`detail=stale-evidence`，走 derived（stale 已排除） |

  调用输出 MUST 解析 `verdict`、`rc`、`reason`、`attribution`。
- **LS-15**: watcher 输出 MUST 按 `WATCH` 行的 `key=value` 解析 `verdict`、`rc`、`reason`、`attribution`。watcher 不可用（脚本缺失、调用失败、超时、输出不可解析、usage）时 MUST 输出 `present=false`、`verdict=null`、`reason=unavailable` 与 `detail ∈ {script-missing, invocation-failed, timeout, unparseable, usage, stale-evidence, probe-unreachable}`；`exit_code` 只为判定码（`0` 或非零判定码，owner：`watch-target.sh --help`），usage 记 `exit_code=null`。MUST NOT 伪造 verdict、判阶段失败或判 `DEAD`。

## 7. 阈值发现

- **LS-16**: `start-grace`、`deadline-grace`、`heartbeat-max-age` 的取值 MUST 依次来自显式参数 → `watch-target.sh --help` 的 `Defaults:` 行 → `unknown`。本入口 MUST NOT 内置第二套缺省数字；发现失败时 `thresholds.value_state=unknown`，依赖该阈值的判定不触发。`retry_limit` 同理，owner 为 `references/stage-prompts.md` § Stall Handling，并由契约测试钉住引擎常量与 owner 字面量一致。

## 8. `--self-test`

- **LS-17**: `--self-test` MUST 自建临时夹具，不依赖真实进程、网络或仓库状态；逐例输出 `ok <case>` / `FAIL <case> — <detail>`，最后一行 MUST 为 `SELF-TEST: N passed, M failed`；全部通过退出 `0`，任一失败退出 `1`。
- **LS-18**: `--self-test` MUST 覆盖：六类 065a 形态（含 `unwatched` 的缺失与过期两分支）、旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 状态脊、不可达证据、`not-dispatched`、Registry 缺失继续求值、probe 两形状、probe 拒绝路径、未实现动作的拒绝信封（exit 1）、确定性（两次同输入仅 `evaluated_at` 不同）与退出码阶梯/`--help` 文本钉住。`heartbeat-stalled`、`lifecycle-spine-violation`、并发锁与 `recover/check-spine` 的**执行**路径不在本切片自测范围。
