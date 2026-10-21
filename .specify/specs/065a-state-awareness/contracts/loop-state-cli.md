# Contract: `loop-state.py` CLI 与进程契约

**Scope**: Feature 065 / Slice 065a。定义入口、参数解析、退出码、只读边界与 `--probe`/`--self-test` 的进程级行为。
**Owner note**: watcher 的判定状态机、信号优先级与退出码归 `scripts/watch-target.sh`；本契约只规定聚合器如何**消费**它们，不复制其规则。derived `loop_state` 映射表的唯一 owner 是切片 `requirements.md` FR-004（parent #FR-004）；本契约只引用，不拥有该表。

## 0. 条款编号与别名

本契约的 18 条条款使用项目规范形态 `**C-N**`（语法 owner：`.specify/shared/definitions/contract-clause-definitions.md` §3）。全局编号按 `loop-state-cli → snapshot-envelope → interruption-and-action → stage-artifact-map` 连续递增；历史文字引用使用下列别名，二者指向同一条款。

| 历史别名 | 规范 ID | 历史别名 | 规范 ID |
|----------|---------|----------|---------|
| LS-01 | C-1 | LS-10 | C-10 |
| LS-02 | C-2 | LS-11 | C-11 |
| LS-03 | C-3 | LS-12 | C-12 |
| LS-04 | C-4 | LS-13 | C-13 |
| LS-05 | C-5 | LS-14 | C-14 |
| LS-06 | C-6 | LS-15 | C-15 |
| LS-07 | C-7 | LS-16 | C-16 |
| LS-08 | C-8 | LS-17 | C-17 |
| LS-09 | C-9 | LS-18 | C-18 |

## 1. 入口

- **C-1**: 入口文件 MUST 为 `skills/external/sdd-loop-driver/scripts/loop-state.py`（运行时镜像 `.specify/skills/sdd-loop-driver/scripts/loop-state.py` 由 `sync-mirrors.py` 生成，MUST NOT 手改）。实现 MUST 仅使用 Python 3 标准库（Python `>=3.8` 语法），MUST NOT 引入常驻服务、后台进程或外部依赖。 (FR-001, FR-041, FR-042, SC-005)
- **C-2**: 动作面 MUST 为 `--action snapshot|recover|check-spine` 与 `--self-test`。065a MUST 实现 `snapshot` 与 `--self-test`；`recover` 与 `check-spine` MUST 返回结构化拒绝信封（`schema_version=1`、`action=<name>`、`applied=false`、`result=failed`、`steps=[]`、`reason=not-implemented-in-065a`、`owner=<动作归属>`、`message=<一句用户可读说明>`）并以退出码 `1`（拒绝）结束。`owner` 字段逐动作钉死：`check-spine` → `owner=065b`；`recover` → `owner=065c`。两个动作的行为实现归属与 `notes/decomposition-gate.md` 一致（`check-spine` → `065b`，`recover` → `065c`）；本切片 MUST NOT 预置其副作用路径，也不改变既有 `/speckit.*` 命令流程。 (FR-001, FR-012, FR-040)
- **C-3**: `--help` MUST 列出三个动作、全部参数，以及 `0/1/2` 退出码阶梯的语义；MUST 明示 watcher 的判定码是**数据**，本入口不复用、不重定义。`--self-test` MUST 断言该文本包含阶梯语义。 (FR-012)

## 2. 输入解析

- **C-4**: 解析顺序 MUST 为：显式 `--spine` / `--state-dir` / `--spec-dir` / `--repo` / `--probe` 覆盖 → 按 `--line-id` 读取 Registry 条目 → 失败。`--line-id` 缺失 MUST 以退出码 `2` 拒绝。每个路径的逐项优先级见 `data-model.md` §5.1 与 `research.md` R-02。 (FR-002, FR-012)
- **C-5**: Registry 缺失但状态脊与四件套可解析时，MUST 继续求值并在 `registry.status` 记 `missing`；MUST NOT 因 Registry 缺失判 `UNKNOWN`（`IA-03` 的未派发判据除外）。 (FR-002, FR-003)
- **C-6**: 本条区分两类输入，二者处置不同且不得互换：

  | 输入类 | 定义 | 不可读/不可解析时的处置 |
  |--------|------|--------------------------|
  | 必需输入（required input） | 必需 CLI 参数：`--line-id`；显式提供时的 `--probe` 文件 | MUST 以退出码 `2` 拒绝，不进入求值 |
  | 证据源（evidence source） | 状态脊、Registry、四件套、watchbeat、阶段产物、git 提交等证据文件 | MUST 显式记为 `missing`（值用 `null`），并仍以退出码 `0` 完成求值 |

  证据源不可读时 MUST NOT 以零值、空串、`"ok"` 或猜测默认值填充。 (FR-002, FR-003, FR-012)
- **C-7**: `stage` MUST 依次取 `--stage` → Registry `stage`；两者皆无时 `stage=null`，产物映射不可建立：spec 路径可读时 `artifacts.status=present`、`value_state=unknown`，否则 `status=missing`、`value_state=na`。`--stage` 是调用方意图，不是派发证据；`IA-03` 的 never-dispatched 判定成立时，四件套、watchbeat、artifacts 与 commits MUST 记 `status=na`、`value_state=na`。 (FR-002, FR-003, FR-006, FR-007)

## 3. 退出码阶梯

- **C-8**: 退出码封闭集 MUST 为 `0`（求值成功；任何 `loop_state` 都是数据，不编码为退出码）、`1`（拒绝或校验失败；含 `C-2` 的未实现动作拒绝）、`2`（参数错误，或必需 CLI 参数/`--probe` 文件不可读、不可解析；证据源不可读不在此档，按 `C-6` 记 `missing` 并以 `0` 完成求值）。`snapshot` 在成功求值后 MUST 返回 `0`，包括 `loop_state=UNKNOWN`、`STALLED`、`DEAD` 或动作建议为 `stop` 的情形。 (FR-012)
- **C-9**: 本入口 MUST NOT 复用或重定义 watcher 的判定退出码 `10–16`；watcher 的退出码只写入 `watch_verdict.exit_code` 作为数据。 (FR-012, FR-038)

## 4. 只读边界

- **C-10**: 除显式 `--out <file>` 外，`snapshot` MUST NOT 写文件、改 mtime、改状态脊/四件套/Registry、杀进程或修改工作树。`--out` 写入 MUST 为同目录临时文件 + 原子替换；目标路径与其父目录 MUST 先以 `realpath`（Python `Path.resolve`）规范化，再与解析后的 `state_dir`/`repo` 比较，且该比较 MUST 先于创建任何临时文件；目标落在 `state_dir` 或 `repo` 工作树内时 MUST 以退出码 `2` 拒绝，且 MUST NOT 留下任何文件。`--out` 内容 MUST 与 stdout 信封相同。 (FR-001, FR-049, FR-050, SC-002)

## 5. `--probe`

- **C-11**: `--probe <file>` MUST 接受两种 JSON 形状，并按下列判据分流：

  | 形状 | 必需键 | 行为 |
  |------|--------|------|
  | (a) 快照信封 | `schema_version=1`、`watch_verdict`、`evidence` | 逐字消费 probe 的 `spine`/`registry`/`watch_verdict`/`evidence`；本地重算 `interruptions`/`recovery_action`；`loop_state` 在 `watch_verdict.present=true` 时逐字取 probe 的 verdict（`IA-05`），否则走 derived；`evidence_source=probe`；probe 自带 freshness 视为权威 |
  | (b) 最小可达性 | `schema_version=1`、`reachable=false`、`reason` | 输出 `STALLED` + `remote-unreachable` + 动作 `stop`；全部信号 `missing` |

  (FR-002, FR-009)
- **C-12**: JSON 不可解析、`schema_version≠1`、形状 (b) 的 `reachable=true`（无可求值证据）、或 probe 中 `line_id` 与 `--line-id` 不一致时，MUST 以退出码 `2` 拒绝。未知字段 MUST 被忽略。 (FR-002, FR-012)
- **C-13**: 提供 `--probe` 时，MUST NOT 调用本地 watcher，MUST NOT 读取本地状态脊/四件套/产物/git 证据；与 `--spine`、`--state-dir`、`--spec-dir`、`--repo`、`--watch-script` 同时出现 MUST 以退出码 `2` 拒绝（互斥，不得混用本地证据）。 (FR-002, SC-002)

## 6. watcher 委托

- **C-14**: 仅当存在活动 watch target（`pid` 或 `status` 记录存在、哨兵存在、或 `stage_started_at` 可读）、且非 `not-dispatched`、且未提供 `--probe` 时调用 watcher，MUST 以 runner 同一执行身份执行 `watch-target.sh --once`，传入既有四件套路径、`--sentinel <STAGE>-DONE`、`--deadline-epoch`（来自脊）与 `--stage`。归属参数的选取 MUST 按以下规则，避免把无 `run=` 的现行信封误判为 `unattributed` 而丢弃终止证据：

  | 条件 | 调用形态 |
  |------|----------|
  | `run_id` 已知，且 Registry `meta_paths` 中存在 meta 文件，或 status 与 pid 信封均带与 `run_id` 相等的 `run=` | 归属形态：附 `--line-id <id> --run-id <run> --registry <dir> --meta <file>` |
  | `run_id` 未知或归属不可证，且 `stale_signals` 为空 | 兼容形态：不附归属参数（watcher 输出 `attribution=legacy`） |
  | 归属不可证且 `stale_signals` 非空 | 不调用 watcher；`present=false`、`reason=unavailable`、`detail=stale-evidence`，走 derived（stale 已排除） |

  调用输出 MUST 解析 `verdict`、`rc`、`reason`、`attribution`。 (FR-005, FR-038, FR-039, SC-004)
- **C-15**: watcher 输出 MUST 按 `WATCH` 行的 `key=value` 解析 `verdict`、`rc`、`reason`、`attribution`。watcher 不可用（脚本缺失、调用失败、超时、输出不可解析、usage）时 MUST 输出 `present=false`、`status=missing`、`value_state=na`、`verdict=null`、`reason=unavailable` 与 `detail ∈ {script-missing, invocation-failed, timeout, unparseable, usage, stale-evidence, probe-unreachable}`；`exit_code` 只为判定码（`0` 或非零判定码，owner：`watch-target.sh --help`），usage 与调用失败记 `exit_code=null`。MUST NOT 伪造 verdict、判阶段失败或判 `DEAD`。 (FR-005, SC-002)
- **C-16**: `start-grace`、`deadline-grace`、`heartbeat-max-age` 的取值 MUST 依次来自显式参数 → `watch-target.sh --help` 的 `Defaults:` 行 → `unknown`。本入口 MUST NOT 内置第二套缺省数字；发现失败时 `thresholds.value_state=unknown`，依赖该阈值的判定不触发。`retry_limit` 同理，owner 为 `references/stage-prompts.md` § Stall Handling，并由契约测试钉住引擎常量与 owner 字面量一致。 (FR-004, FR-011, FR-038)

## 7. `--self-test`

- **C-17**: `--self-test` MUST 自建临时夹具，不依赖真实进程、网络或仓库状态；逐例输出 `ok <case>` / `FAIL <case> — <detail>`，最后一行 MUST 为 `SELF-TEST: N passed, M failed`；全部通过退出 `0`，任一失败退出 `1`。该自测是 `FR-046` 变异演练的靶面。 (FR-012, FR-046, SC-006)
- **C-18**: `--self-test` MUST 覆盖：六类 065a 形态（含 `unwatched` 的缺失与过期两分支）、旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 状态脊、不可达证据、`not-dispatched`（含 `--stage` 仅为意图与脊存在排除条件）、Registry 缺失继续求值、必需输入与证据源的分档处置（exit 2 vs `missing` + exit 0）、probe 两形状、probe 拒绝路径、未实现动作的拒绝信封（exit 1，含逐动作 `owner`）、确定性（两次同输入仅 `evaluated_at` 不同）与退出码阶梯/`--help` 文本钉住。`heartbeat-stalled`、`lifecycle-spine-violation`、并发锁与 `recover/check-spine` 的**执行**路径不在本切片自测范围。 (FR-009, FR-012, SC-006)
