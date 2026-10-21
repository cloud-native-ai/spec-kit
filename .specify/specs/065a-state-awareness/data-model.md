# Data Model: 状态感知快照（Feature 065 / Slice 065a）

**Plan**: [`plan.md`](./plan.md) · **Requirements**: [`requirements.md`](./requirements.md)
**Date**: 2026-10-21

本模型描述 `loop-state.py --action snapshot` 的输入、内部证据模型与唯一输出信封。它是**观测记录**，不是新的状态 owner：状态脊、Registry、watcher 判定的语义仍由各自 owner 定义（`requirements.md` A-2/A-3/A-16/FR-039/FR-052）。

## 1. 实体总览

```text
PathContext ──┐
RegistryView ─┼──> EvidenceBundle ──> LoopStateSnapshot
SpineRecord ──┤        │                 ├── WatchVerdict
ThresholdSet ─┘        │                 ├── InterruptionFinding[]
                       │                 ├── StaleSignal[]
StageArtifactMap ──────┘                 └── RecoveryDecision (embedded)
ProbeInput ──(a|b)────> EvidenceBundle
```

| 实体 | 作用 | Owner |
|------|------|-------|
| `LoopStateSnapshot` | 一次只读求值的唯一输出信封 | 本切片 |
| `PathContext` | 解析后的路径集合（state/spec/repo/spine 等） | 本切片（解析规则引用 FR-002） |
| `RegistryView` | Line Registry 条目的只读投影 | Feature 064（字段语义） |
| `SpineRecord` | 状态脊机读段/legacy 行的只读投影 | Feature 058（文件语义）；本切片只读 |
| `SignalEvidence` | 单个证据源的 `status` / `value_state` / 指针 / 值 | 本切片 |
| `WatchVerdict` | watcher 判定或其不可用表达 | `watch-target.sh`（判定）；本切片（信封） |
| `WatchbeatMarker` | 驱动者监听标记的只读投影 | 驱动者写入；本切片只读 |
| `StageArtifactMap` | 阶段 → 必需产物/owned 路径/提交义务 | 本切片（脚本数据 + `references/state-awareness.md`） |
| `InterruptionFinding` | 封闭形态之一 + 证据指针 + 一句事实 | 本切片（六类）；065b（两类） |
| `RecoveryDecision` | 由状态/产物/中断/尝试次数导出的唯一动作建议 | 本切片只读求值；065c 执行 |
| `ProbeInput` | 调用方提供的远端证据快照（两种形状） | 本切片 |
| `StaleSignal` | 被排除出本次求值的旧尝试信号 | 本切片 |
| `ThresholdSet` | 本次求值使用的阈值及其来源 | `watch-target.sh`（缺省值） |

## 2. LoopStateSnapshot（输出信封，`schema_version: 1`）

### 2.1 顶层字段

| 字段 | 类型 | 必填 | 语义 |
|------|------|------|------|
| `schema_version` | int | 是 | 固定 `1`；增量字段只允许追加 |
| `line_id` | string | 是 | 请求的线标识 |
| `run_id` | string \| null | 是 | 当前尝试；无法判定时 `null` |
| `stage` | string \| null | 是 | 当前阶段；无 Registry `stage` 且无 `--stage` 时 `null` |
| `loop_state` | enum | 是 | 见 §2.2 |
| `verdict_source` | `watcher` \| `derived` | 是 | `watcher` 当且仅当 `watch_verdict.present=true` |
| `loop_state_reason` | string \| null | 是 | 命中规则的原因字面量（§2.3） |
| `watch_verdict` | WatchVerdict | 是 | §4 |
| `recovery_action` | enum | 是 | `none` / `watch` / `verify` / `resume` / `retry` / `stop` |
| `recovery_reason` | string | 是 | 动作依据（§7.2） |
| `recovery_decision` | RecoveryDecision | 是 | §7.1；`action`/`reason` 与顶层字段相等 |
| `false_completion` | bool | 是 | 哨兵存在且任一必需产物缺失/为空；为真时动作为 `retry`（除非 `IA-04` 证据缺口或 `IA-15` 尝试上限改为 `stop`） |
| `spine` | SpineRecord | 是 | §3.2 |
| `registry` | RegistryView | 是 | §3.1 |
| `paths` | object | 是 | `{state_dir, spec_dir, repo, spine, probe}`，未知为 `null` |
| `thresholds` | ThresholdSet | 是 | §5.2 |
| `evidence` | EvidenceBundle | 是 | §4；含 `evidence_source` |
| `interruptions` | InterruptionFinding[] | 是 | 可为空；多条并存 |
| `missing_artifacts` | string[] | 是 | 必需产物中缺失/为空的相对路径 |
| `uncommitted_artifacts` | string[] | 是 | 基线已知时，存在但无基线后提交覆盖的路径 |
| `stale_signals` | StaleSignal[] | 是 | 见 §4.4 |
| `evaluated_at` | string | 是 | ISO-8601 UTC；**唯一**允许在相同输入两次运行间变化的字段 |

### 2.2 `loop_state` 封闭集与来源

状态集合：`RUNNING / DONE / INCOMPLETE / ANOMALY / FAILED / DEAD / TIMEOUT / NO_SIGNAL / STALLED / REENTRY_REQUIRED / UNKNOWN`。

- 存在 watcher 判定时，取值**逐字等于** `watch_verdict.verdict`，`verdict_source=watcher`；聚合器不改写。
- 无 watcher 判定时按 `requirements.md` FR-004 的固定优先级导出，`verdict_source=derived`；三个前置分支：`not-dispatched`（`IA-03`）、远端不可达（`IA-06`/`IA-12`）、有派发证据但缺脊（`IA-04`）。
- 状态优先级表与 watcher 优先不变量的**唯一 owner** 是 `requirements.md` FR-004（parent #FR-004）；本文件与代码只作为该表的镜像，不复述阈值或完整规则文本，也不得声称拥有该表。
- 一致性字段统一为嵌套 `spine.consistent`（bool \| null）；MUST NOT 输出顶层 `spine_consistent` 别名。

### 2.3 `loop_state_reason` 取值

`watcher-verdict`、`spine-stalled`、`spine-reentry-required`、`anomaly-line`、`exit-nonzero`、`sentinel-and-artifacts`、`exit-zero-incomplete`、`sentinel-no-exit`、`dead-no-exit-record`、`deadline-overrun`、`no-signal`、`running`、`remote-unreachable`、`not-dispatched`、`unknown`。

## 3. 路径与登记投影

### 3.1 RegistryView

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | `present` \| `missing` | Registry 条目文件是否存在且可解析 |
| `path` | string \| null | `<registry-dir>/<line_id>.json` |
| `state` | string \| null | 原样只读（`active`/`waiting`/…） |
| `stage` | string \| null | 用于 `stage` 回退 |
| `run_id` | string \| null | 用于与信号信封比对 |
| `spine_path` | string \| null | 用于 `spine` 回退 |

**规则**：Registry 缺失不是致命错误（FR-002）：继续求值并记 `status=missing`。Registry 字段语义归 Feature 064；本切片不写、不改、不重解释。

### 3.2 SpineRecord

| 字段 | 类型 | 说明 |
|------|------|------|
| `path` | string \| null | 解析后的路径 |
| `status` | `present` \| `missing` \| `na` | 文件是否存在/可读 |
| `schema` | `v1` \| `legacy` \| `missing` | 是否存在 `<!-- loop-state:begin -->`…`<!-- loop-state:end -->` 机读段 |
| `state` | string \| null | `spine_state:`（v1）或 legacy 的 `state[:=]` 行 |
| `state_value_state` | `known` \| `unknown` \| `na` | 值是否可判 |
| `consistent` | bool \| null | `last_verdict` 与 `loop_state` 是否一致；任一侧未知 → `null` |
| `fields` | object | 只读投影：`stage_started_at`、`stage_deadline_epoch`、`stage_base_commit`、`attempt`、`last_verdict`、`salvage`、`salvage_evidence`、`salvage_at`、`pid_path`、`status_path`、`log_path`、`heartbeat_path` |
| `missing_fields` | string[] | legacy 或缺字段时列出，用于“不猜测”的可审计性 |

**规则**：legacy 脊（`schema=legacy`）缺字段记 `value_state=unknown`；`state` 仅按 `line-registry.py` 既有的 `state[:=]` 行读取，不新增裸 `state:` 写侧。`salvage=accepted` 只有在 `salvage_evidence` 与 `salvage_at` 均非空时才算记录完整；否则按未记录处理（动作降级 `retry`）。

## 4. 证据模型

### 4.1 通用规则

每个信号对象至少含：

| 字段 | 类型 | 语义 |
|------|------|------|
| `status` | `present` \| `missing` \| `na` | 期望的证据源/路径是否存在且可读；`na` = 对本次尝试不适用 |
| `value_state` | `known` \| `unknown` \| `na` | 源存在但值不可判定 → `unknown`；与 `status=na` 配对 → `na` |
| `path` | string \| null | 证据指针；未知为 `null` |

**边界（Q2 裁决）**：

- `missing`：路径不存在或不可读 → 值用 `null`，`value_state=na`（没有可判定的值）。
- `na`：该信号对本阶段/本次尝试不适用（如 `commit_required=false`、未配置 hook、`not-dispatched` 的四件套/watchbeat/artifacts/commits），`value_state=na`。
- `unknown`：源存在、值不可判（legacy 缺字段、信封不可解析、阶段未知无产物映射）→ `present` + `unknown`。watcher 不可用不是值级 `unknown`，而是三态映射（§4.3）：`present=false` + `status=missing` + `value_state=na` + `reason=unavailable`。
- `--stage` 只是调用方意图，不是派发证据；never-dispatched 时四件套、watchbeat、artifacts 与 commits 一律 `status=na`、`value_state=na`。
- 禁止用 `0`、`""`、`"ok"` 代替缺失值。

**stale 排除**：被列入 `stale_signals` 的信号保留 `status=present`，但**不进入** `loop_state`/产物/动作求值。

### 4.2 四件套与可选信号

| 信号 | 关键字段 | 说明 |
|------|----------|------|
| `pid` | `pid`、`start`、`at`、`alive`、`identity`、`attribution` | `identity ∈ ok\|mismatch\|unknown`；只用记录的 PID 做 `kill -0` 与 start token 比对，不做进程发现扫描 |
| `status` | `exit_code`、`at`、`sentinel`、`run_id`、`stage`、`event`、`legacy`、`attribution` | 空格信封；`run_id` 取 `run=`，现行 `stage-runner.sh` 不写该字段时为 `null`；`legacy=true` 表示无 `line=`/`run=` 归属 |
| `log` | `last_line`、`sentinel_present`、`sentinel`、`anomaly` | `sentinel_present` = 最后非空行恰好等于 `<STAGE>-DONE`（owner：`requirements.md` FR-004）；更早出现的哨兵字样不置真 |
| `heartbeat` | `at`、`mtime_ns`、`fresh`、`attribution` | 新鲜度按 mtime 与阈值 |
| `watchbeat` | `run_id`、`stage`、`window`、`at`、`event`、`fresh` | `event ∈ watch-window\|watch-return`；新鲜度 = 年龄 ≤ `window` + deadline-grace；写入义务归 065b，本切片只读 |
| `hook` | `path`、`observed_at` | 可选；未配置 → `status=na` |
| `artifacts` | `stage`、`complete`、`commit_required`、`no_change_allowed`、`items[]` | `items[] = {path, required, status, size}` |
| `commits` | `base`、`pathspec[]`、`commits[]`、`touching` | `commits[] = {sha, subject}` |

`attribution ∈ own|legacy|unattributed|stale-run|foreign|null`，语义与 `watch-target.sh` 的归属分类一致：`own` 证明属于当前尝试；`legacy` 表示未启用归属过滤；其余不得作为本次证据。信封不带 `run=` 且无 meta 佐证时，归属只能是 `legacy` 或 `unattributed`，不得据 `line=`/`stage=` 单独声称 `own`。

`EvidenceBundle` 顶层含 `evidence_source ∈ local|probe`，并包含以上八个键。

### 4.3 WatchVerdict

| 字段 | 类型 | 语义 |
|------|------|------|
| `present` | bool | 是否取得 watcher 判定 |
| `status` | `present` \| `missing` \| `na` | 判定源是否存在（取得判定 = `present`；不可用 = `missing`；无 target = `na`） |
| `value_state` | `known` \| `na` | 判定值是否可判 |
| `verdict` | string \| null | watcher 字面量；不可用/无目标 → `null` |
| `reason` | string \| null | 不可用时固定 `unavailable`；其余透传 watcher 的 `reason=` |
| `exit_code` | int \| null | watcher 的判定码（`0` 或非零判定码，owner：`watch-target.sh --help`）；usage 记 `null` |
| `attribution` | string \| null | 取得判定时取 watcher 输出的归属字面量（`own`/`legacy`/`unattributed`/`stale-run`/`foreign`）；其余 `null` |
| `detail` | string \| null | 不可用的具体原因（`script-missing`/`invocation-failed`/`timeout`/`unparseable`/`usage`/`stale-evidence`/`probe-unreachable`） |

**三态**：

| 状态 | `present` | `status` | `value_state` | `verdict` | `reason` |
|------|-----------|----------|---------------|-----------|----------|
| 取得判定 | `true` | `present` | `known` | watcher 字面量 | watcher 的 reason 或 `null` |
| watcher 不可用 | `false` | `missing` | `na` | `null` | `unavailable` |
| 无活动 target | `false` | `na` | `na` | `null` | `null` |

### 4.4 StaleSignal

| 字段 | 类型 | 语义 |
|------|------|------|
| `signal` | `status` \| `pid` \| `heartbeat` \| `hook` \| `watchbeat` | 信号名 |
| `path` | string | 指针 |
| `reason` | `run-mismatch` \| `before-stage-start` \| `legacy-stale` | 判据 |
| `run_id` | string \| null | 文件信封中的值（如有） |
| `at` | int \| null | 文件 `at=`（如有） |
| `mtime_ns` | int \| null | 文件 mtime（原始值，非年龄） |

## 5. 阈值与路径上下文

### 5.1 PathContext

`state_dir`、`spec_dir`、`repo`、`spine`、`probe` 五个路径；按 `research.md` R-02 的顺序解析。未解析项为 `null`，对应证据记 `missing`。两类输入 MUST 区分：必需输入 = 必需 CLI 参数（`--line-id`，显式提供时的 `--probe` 文件），不可读/不可解析 → exit 2；证据源 = 上述路径指向的脊/四件套/产物等证据文件，不可读 → `status=missing` + exit 0。

### 5.2 ThresholdSet

| 字段 | 类型 | 语义 |
|------|------|------|
| `source` | `explicit` \| `watch-target-help` \| `unknown` | 阈值来源 |
| `value_state` | `known` \| `unknown` | 任一阈值不可得 → `unknown` |
| `start_grace` | int \| null | 来自 owner，**本文件不写数值** |
| `deadline_grace` | int \| null | 同上 |
| `heartbeat_max_age` | int \| null | 同上 |
| `retry_limit` | int \| null | 来自 `references/stage-prompts.md` § Stall Handling，**不写数值** |

`value_state=unknown` 时，依赖该阈值的判定不触发；输出保留 `null` 与 `unknown`，不以默认值补齐。

### 5.3 ProbeInput

| 形状 | 必需键 | 字段映射 |
|------|--------|----------|
| (a) 快照信封 | `schema_version=1`、`watch_verdict`、`evidence` | 可选 `spine`、`registry`、`line_id`；`evidence`/`watch_verdict` 逐字消费；probe 自带 freshness 为权威 |
| (b) 最小可达性 | `schema_version=1`、`reachable=false`、`reason` | 仅证明不可达；不携带其他证据 |

未知键 MUST 被忽略；`line_id` 存在且与请求不一致、或形状不可解析时以退出码 `2` 拒绝。ProbeInput 与本地路径参数互斥（`LS-13`）。

## 6. 中断条目

### 6.1 InterruptionFinding

| 字段 | 类型 | 语义 |
|------|------|------|
| `form` | enum | 八类封闭词表之一（§6.2） |
| `detail` | string | 一句事实描述（不含建议、不含猜测） |
| `evidence` | object[] | `{signal, path, field?}` 指针数组；至少一项 |
| `detector` | `065a` \| `065b` | 形态判定的归属切片 |

### 6.2 八类封闭词表与检测归属

| 形态 | 检测归属 | 065a 行为 |
|------|----------|-----------|
| `unwatched` | 065a | 运行中（pid 活或心跳新鲜）且无终态证据（无哨兵、无退出记录、脊非 `stalled`/`reentry-required`），且 watchbeat 缺失或超过 `window`+grace |
| `dead-no-exit-record` | 065a | 无退出记录、有 pid 记录、进程死/身份不符 |
| `deadline-overrun-live` | 065a | 已过 `stage_deadline_epoch`+grace、pid 活、无终态 |
| `artifacts-without-completion` | 065a | 必需产物齐备且无完成哨兵（无论退出记录/退出码） |
| `stale-signal` | 065a（基础谓词） | run 不符 / mtime 早于 `stage_started_at` / 无信封 legacy |
| `remote-unreachable` | 065a（基础谓词） | probe 形状 (b) 证明不可达 |
| `heartbeat-stalled` | 065b | 只保留词表、字段与 `missing`/`unknown` 语义，不检测 |
| `lifecycle-spine-violation` | 065b | 同上 |

同一根因的多个文件合为一条形态条目（`evidence[]` 列全部指针）；不同根因各自成条，不以一条掩盖另一条。

## 7. 恢复裁决

### 7.1 RecoveryDecision（内嵌于快照）

| 字段 | 类型 | 语义 |
|------|------|------|
| `action` | enum | `none/watch/verify/resume/retry/stop` |
| `reason` | string | 见 §7.2 |
| `preconditions` | string[] | 让该动作成立的关键事实（如 `salvage=accepted`、`attempt<limit`） |
| `blocked_by` | string[] | 阻止更高优先级动作的事实（如 `attempt-unknown`） |

优先级与门由契约 `IA-14`–`IA-17` 定义；本表不复制其顺序文本。该对象 MUST 以顶层 `recovery_decision` 暴露，且 `action`/`reason` MUST 与顶层 `recovery_action`/`recovery_reason` 相等（`SN-02`）。

### 7.2 `recovery_reason` 取值

`not-dispatched`、`remote-unreachable`、`evidence-gap`、`attempts-exhausted`、`unwatched`、`deadline-overrun-live`、`running`、`done-complete`、`commit-baseline-unknown`、`artifacts-uncommitted`、`salvage-accepted`、`salvage-not-recorded`、`false-completion`、`terminal-retry`、`stalled-handoff`。

## 8. 不变量与校验

1. `schema_version=1`；未知字段由旧读取方忽略。
2. `verdict_source` 与 `watch_verdict.present` 的对应关系、以及 watcher 来源下 `loop_state` 的逐字相等约束，按 `requirements.md` FR-004 执行（owner）；本文件不复述该不变量。
3. `loop_state` 只能取 `§2.2` 的封闭集；watcher 在时逐字一致。
4. 任何缺失值只以 `null` 出现；`status`/`value_state` 只取各自封闭集。
5. 除 `evaluated_at` 外不得输出随当前时间变化的派生数值。
6. 完成哨兵 = 日志最后非空行 `== <STAGE>-DONE`（owner：FR-004）。`false_completion=true` ⇔ 末行哨兵 ∧ 至少一项必需产物缺失/为空；此时 `recovery_action=retry`，除非 `IA-04` 的证据缺口短路或 `IA-15` 的尝试上限将其改为 `stop`。`false_completion` 与 `artifacts-without-completion` 互斥。
7. `recovery_action=resume` ⇒ 产物齐备 ∧ 日志末行非 `ANOMALY:` ∧（末行哨兵 ∨ salvage 完整记录）∧ `attempt` 已知且未达上限；`loop_state=DONE` 且提交齐备时 MUST 为 `verify`。
8. `--probe` 模式下所有证据 `evidence_source=probe`，且不得读取本地文件或调用本地 watcher；与本地路径参数同时提供时 exit 2。
9. 被列入 `stale_signals` 的信号不参与任何求值；065a 不因单纯 stale 改变动作，`stale-unisolated → stop` 由 065c 承接（SA-1）。
10. 快照不写状态脊、四件套、Registry 或工作树；`--out` 为唯一写路径，目标与父目录先 `realpath`/`Path.resolve` 再与解析后的 state dir / repo 比较，比较先于创建临时文件，拒绝时 exit 2 且不留文件。
11. `recovery_decision.action`/`reason` 与顶层 `recovery_action`/`recovery_reason` 相等；`blocked_by` 非空时必须解释为何未采用更高优先级动作。
12. `status=missing` ⇒ `value_state=na`；`value_state=unknown` 只与 `status=present` 配对。watcher 不可用是 `present=false` + `status=missing` + `value_state=na` + `reason=unavailable`，不是值级 `unknown`。
13. 一致性字段为嵌套 `spine.consistent`（bool \| null）；不输出顶层 `spine_consistent` 别名。
14. （summary only；owner 为 `contracts/interruption-and-action.md` C-46）`commit_required=false` 或 `commits.status=na` ⇒ 提交齐备；`commits.value_state=unknown` ⇒ 提交齐备=false，且仅当 `loop_state=DONE` 时动作走 `verify`（`reason=commit-baseline-unknown`），其他终态按 C-46 行 11/12；`analyze` 无必需文件产物 ⇒ `artifacts.complete=true`（vacuous truth）。
15. `not-dispatched` ⇒ 四件套、watchbeat、artifacts、commits 均为 `status=na`、`value_state=na`；`--stage` 只是意图，不是派发证据。
