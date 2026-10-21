# Contract: 中断形态与恢复动作建议

**Scope**: 065a 实现的六类只读形态、八类封闭词表、`loop_state` 推导入口与唯一 `recovery_action` 建议。
**Owner note**: `loop_state` 的固定优先级表与 watcher 优先不变量的唯一 owner 是切片 `requirements.md` FR-004（parent #FR-004）；watcher 判定归 `watch-target.sh`。本契约只定义 065a 的检测入口、两个前置短路与动作建议的确定性顺序，不复述阈值数值，也不拥有 derived 映射表。

## 0. 条款编号与别名

本契约的 17 条条款使用项目规范形态 `**C-N**`（语法 owner：`.specify/shared/definitions/contract-clause-definitions.md` §3）。全局编号接续 `snapshot-envelope`（C-19…C-32）；历史文字引用使用下列别名。

| 历史别名 | 规范 ID | 历史别名 | 规范 ID |
|----------|---------|----------|---------|
| IA-01 | C-33 | IA-10 | C-42 |
| IA-02 | C-34 | IA-11 | C-43 |
| IA-03 | C-35 | IA-12 | C-44 |
| IA-04 | C-36 | IA-13 | C-45 |
| IA-05 | C-37 | IA-14 | C-46 |
| IA-06 | C-38 | IA-15 | C-47 |
| IA-07 | C-39 | IA-16 | C-48 |
| IA-08 | C-40 | IA-17 | C-49 |
| IA-09 | C-41 | | |

## 1. 词表与条目

- **C-33**: 中断形态 MUST 取自封闭集 `unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable`。065a MUST 只产出 `unwatched`、`dead-no-exit-record`、`deadline-overrun-live`、`artifacts-without-completion`、`stale-signal`、`remote-unreachable` 六类；`heartbeat-stalled` 与 `lifecycle-spine-violation` 的判定归 065b，065a 只为它们保留词表、字段与 `missing`/`unknown` 语义。 (FR-009)
- **C-34**: 每个条目 MUST 携带 `form`、一句事实描述 `detail`、至少一个 `evidence` 指针与 `detector`。同一次求值中多个不同根因 MUST 各自成条，MUST NOT 以一条掩盖另一条。同一根因涉及的多个文件合为一条，`evidence[]` 列全；每条只归本线本次求值，MUST NOT 跨线推断。 (FR-009, FR-047)

## 2. 两个前置短路（位于 FR-004 映射之前）

- **C-35**: `not-dispatched` MUST 当且仅当以下条件**全部**成立时判为真：未提供 `--probe`；无 `stage_started_at`；四件套（pid/status/log/heartbeat）均不存在；无完成哨兵；无完成/提交证据；且 Registry 条目缺失或条目没有 `stage`。排除条件：状态脊存在且 `spine_state` 非空时，即使无 `stage_started_at`/四件套，也 MUST NOT 判 `not-dispatched`。`--stage` 是调用方意图，不是派发证据。命中时输出 `loop_state=UNKNOWN`、`loop_state_reason=not-dispatched`、`recovery_action=none`、`recovery_reason=not-dispatched`，且四件套、watchbeat、artifacts、commits MUST 记 `status=na`、`value_state=na`。MUST NOT 在缺脊时把从未派发的线判为 `NO_SIGNAL`；probe 模式 MUST 先按 `C-44`（`IA-12`）求值。 (FR-002, FR-003, FR-004)
- **C-36**: 任一派遣证据（Registry 含 `stage` 或尝试记录、四件套任一存在、哨兵存在、提交证据存在）存在而状态脊缺失时，MUST 输出 `UNKNOWN` + `recovery_action=stop`（`reason=evidence-gap`），MUST NOT 记为 `not-dispatched`，MUST NOT 凭 Registry 单独猜阶段。 (FR-004, SC-002)

## 3. 判定来源

- **C-37**: 存在 watcher 判定时，`loop_state` 与 `verdict_source` 的取值 MUST 按 `requirements.md` FR-004 的 watcher 优先级规则执行；该不变量只在 FR-004 定义一次，本条不重复其规则内容（owner：FR-004）。中断清单与动作建议仍按本契约求值。 (FR-004, FR-005)
- **C-38**: 无 watcher 判定时，按 `requirements.md` FR-004 的固定优先级导出 `loop_state`，`verdict_source=derived`；`C-35`/`C-36` 的短路先于该优先级。远端证据不可达（`C-11` 形状 b）时 MUST 输出 `STALLED` + `loop_state_reason=remote-unreachable`，MUST NOT 判 `DEAD` 或阶段失败。 (FR-004)
- **C-39**: 一致性 MUST 只报告、不裁决：`spine.last_verdict` 与 `loop_state` 不相等时嵌套字段 `spine.consistent=false`；任一侧不可判时 `null`。MUST NOT 静默选择其一，MUST NOT 输出顶层 `spine_consistent` 别名。 (FR-004, SC-002)

## 4. 六类 065a 检测谓词（基础只读谓词）

- **C-40**: `unwatched`: MUST 在“阶段处于运行中且无终态证据”时成立——运行中 =（pid 存活 ∨ 心跳新鲜），且无哨兵（按 `requirements.md` FR-004：哨兵 = 日志最后非空行 `== <STAGE>-DONE`）、无退出记录、状态脊非 `stalled`/`reentry-required`；无终态证据下，watchbeat 标记缺失，或标记年龄 > 其自身 `window=` + deadline-grace。标记 `window=` 缺失或阈值不可得时，MUST NOT 判“过期”分支，只保留“标记缺失”分支。该形态 MUST NOT 在已写出末行哨兵的阶段上触发（否则会与 `DONE → verify` 冲突）。watchbeat 的写入义务归 065b，本条只读消费。 (FR-010, FR-011, SC-003)
- **C-41**: `dead-no-exit-record`: MUST 在无退出记录、pid 记录存在且进程已死或 start token 不符时成立；MUST NOT 判 `DONE`。`deadline-overrun-live`: MUST 在 `stage_deadline_epoch` 可读、`now ≥ deadline + deadline-grace`、pid 存活、且无退出记录/末行哨兵时成立；该形态 MUST 指向继续观察，MUST NOT 指向杀进程或立即停线。 (FR-009, SC-003)
- **C-42**: `artifacts-without-completion`: MUST 在阶段产物映射可建立、全部必需产物齐备、且无末行哨兵（按 `requirements.md` FR-004）时成立（无论退出记录是否存在、退出码为何）。`false_completion` 是同一判据的另一侧，MUST 当且仅当末行哨兵存在且至少一项必需产物缺失/为空时置真。二者互斥，MUST NOT 同时为真；`false_completion=true` 时动作 MUST 为 `retry`（除非 `C-36` 的证据缺口短路或 `C-47` 的尝试上限将其改为 `stop`），两种情形 MUST NOT 互相顶替。 (FR-007, SC-001, SC-003)
- **C-43**: `stale-signal`: MUST 在下列任一条件成立时成立——信号信封的 `run=` 与当前尝试不符；文件 mtime 早于 `stage_started_at`；文件无任何归属字段（既无 `run=` 也无 `line=`）且无 meta 佐证（reason=`legacy-stale`，doubtful-strict）。仅有 `line=`/`stage=` 而缺 `run=` 的现行信封 MUST NOT 因此单独判 stale；其归属记 `legacy`，仅在无其它 stale 信号时参与求值（`C-14`）。被列入 `stale_signals` 的信号 MUST 从 `loop_state`、产物与动作求值中排除。`at`/`mtime_ns` MUST 输出原始值，不输出年龄。065a 不执行物理隔离；`stale-unisolated → stop` 的隔离可行性判定与执行由 065c 承接（SA-1 显式推迟），065a 对 stale 的动作仅限“列入 `stale_signals[]`/`interruptions[]` 并从本次求值排除”，不因单纯 stale 改变候选动作。 (FR-009, SC-002)
- **C-44**: `remote-unreachable`: MUST 在 `--probe` 形状 (b) 证明不可达时成立；输出 `STALLED` 与动作 `stop`，证据指针指向 probe 文件。watcher 调用失败 MUST NOT 映射为该形态（那是 `watch_verdict.reason=unavailable`，走 derived）。更细的远端谓词归 065b。 (FR-009, SC-003)

## 5. 恢复动作建议（只读）

- **C-45**: `recovery_action` MUST 为封闭集 `none / watch / verify / resume / retry / stop` 中的恰好一个，且对相同输入可复现。065a MUST 只输出建议，MUST NOT 提交、隔离、重派、停线、写脊或杀进程。 (FR-001, SC-001)
- **C-46**: `提交齐备`（commit-ready）谓词的唯一 owner 为本条：

  - `commit_required=false` 或 `commits.status=na` → `true`；
  - `no_change_allowed=true` 且阶段产物相对 `stage_base_commit` 无变更 → `true`（合法的无变更阶段，无可提交内容）；
  - `commits.value_state=unknown` → `false`，且 MUST NOT 进入 `resume`/`stop` 的提交分支，而是进入 `verify`（`reason=commit-baseline-unknown`）；
  - 否则 → 基线之后存在触及该阶段产物路径的提交（implement：仅代码/测试路径，见 `stage-artifact-map.md` C-58/C-60）。

  `analyze` 无必需文件产物 → `artifacts.complete=true`（vacuous truth）；`implement` 以代码/测试路径的提交证据为完整判据。候选动作 MUST 按下列顺序取首个命中项：

  | 顺序 | 条件 | 候选 |
  |------|------|------|
  | 1 | `not-dispatched` | `none` |
  | 2 | `remote-unreachable` | `stop` |
  | 3 | `loop_state=UNKNOWN`（非未派发） | `stop` |
  | 4 | `unwatched` ∨ `deadline-overrun-live` ∨ `loop_state=RUNNING` ∨（`loop_state=TIMEOUT` ∧ `pid.alive=true`） | `watch` |
  | 5 | `loop_state=DONE` ∧ `commit_required=false`（含 `commits.status=na`） | `verify` |
  | 6 | （`loop_state=DONE` ∨ 产物齐备）∧ `commits.value_state=unknown` | `verify`（`reason=commit-baseline-unknown`） |
  | 7 | `loop_state=DONE` ∧ 产物齐备 ∧ 提交齐备 | `verify` |
  | 8 | 产物齐备 ∧ 末行非 `ANOMALY:` ∧（末行哨兵 ∨ salvage 完整记录） | `resume` |
  | 9 | 产物齐备 ∧ 无末行哨兵 ∧ 无 salvage | `retry` |
  | 10 | `false_completion=true` | `retry` |
  | 11 | `STALLED` ∨ `REENTRY_REQUIRED` | `stop` |
  | 12 | 其余终态（`INCOMPLETE/ANOMALY/FAILED/DEAD/TIMEOUT/NO_SIGNAL`） | `retry` |
  | 13 | 兜底 | `stop` |

  (FR-007, FR-008, SC-001, SC-003)
- **C-47**: 在候选动作得到后 MUST 应用重试上限：`attempt` 已知且 `attempt ≥ retry_limit` 时，候选为 `resume`/`retry`/`stop` 的 MUST 改为 `stop`（`reason=attempts-exhausted`）；`watch`/`none`/`verify` 不受此限。`attempt` 未知时 MUST NOT 给 `resume`（降级 `retry`，`blocked_by` 记 `attempt-unknown`）。 (FR-051, SC-001)
- **C-48**: `salvage` MUST 仅在状态脊同时具备 `salvage=accepted`、非空 `salvage_evidence` 与非空 `salvage_at` 时才算“完整记录”；否则按未记录处理，候选动作 MUST NOT 为 `resume`。065a MUST NOT 写入 salvage 记录（065c 承接）。 (FR-051, SC-001)
- **C-49**: `stop` 在 065a 只是建议：MUST NOT 杀进程、删除证据或移除 worktree；活进程的 `TIMEOUT` 建议 MUST 优先落到 `watch`，停线只能在最终快照与用户显式决定之后发生（执行归 065c）。 (FR-050, SC-003)
