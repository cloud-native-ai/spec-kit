# Phase 0 Research: 状态感知快照引擎（Feature 065 / Slice 065a）

**Requirement**: [`requirements.md`](./requirements.md)（`065a-state-awareness`）
**Date**: 2026-10-21
**Status**: Complete — no `NEEDS CLARIFICATION` remains.

本文件记录 plan 阶段为 065a 做出并采纳的技术裁决。每条裁决给出证据来源、被否方案与否决理由。输入仅为**切片 requirements**、项目宪法与仓库现状代码/文档；父特性目录下的未提交草稿（plan/research/data-model/contracts/quickstart/feature-ref）未被作为权威输入（SA-5）。

## 0. 结论摘要

065a 交付一个单文件、仅标准库的只读聚合入口 `loop-state.py`，实现 `snapshot`、`--probe` 与 `--self-test`，同时冻结三动作共享的 JSON 信封与 `0/1/2` 退出码阶梯。它**消费**而非重定义 `watch-target.sh` 的判定与阈值，**不写**状态脊、四件套、索引或工作树（显式 `--out` 除外），并为 `recover` / `check-spine` 保留显式拒绝分支，交由 065b / 065c 填充。

## 1. 证据基础（本次实测）

| 证据 | 观测 | 来源 |
|------|------|------|
| Watcher 判定与退出码 | `0 DONE / 10 RUNNING / 11 ANOMALY / 12 FAILED / 13 DEAD / 14 TIMEOUT / 15 INCOMPLETE / 16 NO_SIGNAL / 2 USAGE`；`--help` 明示“TIMEOUT is a budget verdict, not a death certificate” | `skills/external/sdd-loop-driver/scripts/watch-target.sh --help`（本次运行） |
| Watcher 默认阈值 | `--help` 打印 window / interval / start-grace / deadline-grace / heartbeat-max-age 的缺省值；脚本是代码侧 owner | 同上；`references/watch-model.md` §1 |
| Watcher 基线 | `--self-test` = `SELF-TEST: 38 passed, 0 failed`，exit 0 | 本次运行 |
| 信号信封格式 | status 为空格分隔 `exit=<rc> at=<epoch> sentinel=<0|1> ... line= stage= event=status`；`stage-runner.sh` **不写 `run=`**，`run-stage.sh` 写 `run=`；pid 为 `pid=<pid> start=<token> at=<epoch> ... line= stage= event=pid`；heartbeat 为 `at=<epoch> ... event=heartbeat`，新鲜度看 mtime | `scripts/stage-runner.sh`（写入）；`scripts/run-stage.sh`（写入 `run=` 的变体）；`watch-target.sh` 的 `classify_pair` / `read_status_file`；`references/watch-model.md` §2 |
| Watcher 归属过滤 | 传入 `--line-id/--run-id` 时，`classify_pair` 要求信封同时含匹配的 `line=` 与 `run=` 才判 `own`；缺 `run=` 判 `unattributed` 并抑制 status/pid/heartbeat；meta JSONL 可提供归属 | `scripts/watch-target.sh` 的 `classify_pair` / `read_meta_file`；`references/dispatch-recipes.md` §Watcher 归属参数 |
| 信号路径约定 | `status-<line>-<stage>`、`pid-<line>-<stage>`、`heartbeat-<line>-<stage>.log`、`log-<line>-<stage>.log`、`watchbeat-<line>-<stage>` | `scripts/stage-runner.sh`；`references/watch-model.md` §2；FR-010 |
| Registry | 目录解析 `SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`；条目含 `stage`、`run_id`、`spine_path`、`status_path` 等；只读 action `reattach-brief` | `skills/external/sdd-loop-driver/scripts/line-registry.py` |
| U4 产物清单 | 各阶段产物、analyze 无提交要求、review → `review.md` | `references/stage-prompts.md` § Independent Verification |
| plan-owned 集合 | `plan.md,data-model.md,contracts/,quickstart.md,research.md,feature-ref.md` | `references/efficiency-model.md` §3.1 |
| 重试上限 | 缺省值由 `references/stage-prompts.md` § Stall Handling 拥有，入口可覆盖 | 同上 |
| 既有聚合先例 | `line-registry.py --action reattach-brief` 已聚合 Registry/脊/四件套存在性，但不含产物、git、watchbeat、watcher 判定与动作建议 | `line-registry.py`；父 requirements「现状锚点」 |
| 名称可用性 | 仓库内无 `loop-state.py`，无 `watchbeat` 代码 | 全局搜索（本次） |
| 镜像对 | `skills/external/<name>/` → `.specify/skills/<name>/`；`--check` 有漂移时 exit 2 | `scripts/python/sync-mirrors.py` § MIRROR_PAIRS |

**镜像基线说明**：本次 `sync-mirrors.py --check --only skills/external/sdd-loop-driver` 因并发隔离规则被工具策略拒绝执行，未取得数值基线。工作树已存在外部同步产生的驱动技能改动（`git status` 可见）。实现阶段 MUST 在首次编辑前测量一次基线，并把判据表述为“相对基线无新增漂移”，不得写成绝对通过。

## 2. 技术裁决

### R-01 入口形态：单文件、标准库、三动作面 + self-test

**裁决**：新增 `skills/external/sdd-loop-driver/scripts/loop-state.py`，Python 3 标准库、零外部依赖，单文件实现。CLI 采用 `--action snapshot|recover|check-spine` 与 `--self-test`。065a 实现 `snapshot`；`recover` 与 `check-spine` 接受但返回结构化拒绝信封（`result=failed`、`reason=not-implemented-in-065a`、退出码 1）。`owner` 字段逐动作钉死：`check-spine` → `owner=065b`，`recover` → `owner=065c`（与 `notes/decomposition-gate.md` 一致），确保 CLI 面在切片间不重构。

**理由**：FR-001 要求确定性只读入口；A-17 要求三动作共享信封与退出码阶梯在本切片冻结。冻结的是**契约面**，不是未实现动作的行为。

**否决**：扩写 `line-registry.py`（领域是登记/归属/lease，且已近 100 KB，状态感知需读 spec 产物与 git）；只暴露 `snapshot`（后续切片将被迫改动 CLI 面，违背“共享契约冻结”）。

### R-02 输入解析与路径推导

**裁决**：固定优先级如下，逐项独立求值；任何无法解析的项显式记为 `missing`，不猜默认。

| 输入 | 优先级 |
|------|--------|
| `line_id` | `--line-id`（必需，缺失 → exit 2） |
| `stage` | `--stage` → Registry 条目 `stage` → `unknown`（无产物映射） |
| `state_dir` | `--state-dir` → Registry `status_path` 的父目录 → `SPECIFY_LINE_RUNTIME_DIR` → `$HOME` |
| `spine` | `--spine` → Registry `spine_path` → `missing`（不推导、不猜测） |
| `spec_dir` | `--spec-dir` → `missing`（不从 spine 或 cwd 猜） |
| `repo` | `--repo` → `git -C <spec_dir|cwd> rev-parse --show-toplevel` → `missing` |
| watchbeat / 四件套 | 由 `state_dir` + `line_id` + `stage` 按既有命名约定拼出 |

「必需输入」= 必需 CLI 参数（`--line-id`，以及显式提供时的 `--probe` 文件）：不可读/不可解析 → exit 2。「证据源」= 状态脊、Registry、四件套等证据文件：不可读 → `status=missing` + exit 0。`--stage` 只是调用方意图，不是派发证据。

**理由**：FR-002 的覆盖顺序；`state_dir` 的推导与 `line-registry.py` 的 `resolve_runtime_dir` 及 `stage-runner.sh` 的落盘约定一致。spine 与 spec-dir 没有可靠默认值，猜测会制造伪证据。

**否决**：把 `<spec-dir>/state-spine.md` 当默认（本仓库的实际脊可能位于 `/tmp` 驱动目录）；把 cwd 当 spec-dir（调用方可能在仓库任意目录）。

### R-03 信号解析：消费既有空格信封，不引入第二套格式

**裁决**：`status` 解析首个 `exit=` 字段及 `at=`/`sentinel=`/`run=`/`line=`/`stage=`；`pid` 解析 `pid=`/`start=`/`at=`；`heartbeat` 解析 `at=` 并以 mtime 判新鲜；日志取最后非空行判哨兵（`<STAGE>-DONE`）与 `ANOMALY:` 前缀。全部按 `watch-target.sh` 的既有读取语义实现。

**理由**：FR-038/FR-039 要求既有格式与语义不变；两套解析器会产生漂移。FR-003 的 JSON 信封是**快照输出**，不是信号文件格式。

**否决**：把所有信号转成 JSON 落盘（改变 runner 写侧，越界）；只读 JSON（现状不是 JSON）。

### R-04 状态与值的两层模型

**裁决**：每个信号输出 `status ∈ present|missing|na`（源在不在）与 `value_state ∈ known|unknown|na`（读出的值可不可判）；值本身缺失用 `null`。`legacy`、不可解析信封、阶段未知导致无产物映射 → `value_state=unknown`。watcher 不可用不是值级 `unknown`，而是三态映射：`present=false` + `status=missing` + `value_state=na` + `reason=unavailable`。悬挂的 stale 信号保留 `status=present`，但**不参与** `loop_state` 求值。

**理由**：Q2 裁决；SC-002 需要分别断言“源缺失”与“值未知”。stale 信号若参与求值会复现实测的旧 status 误判。

**否决**：把 `unknown` 并入 `status`（扩枚举、破坏旧读取方）；把 legacy 值当默认值（A-11 禁止）。

### R-05 阈值的唯一 owner 与运行时发现

**裁决**：start-grace、deadline-grace、heartbeat-max-age 缺省值不在本切片复述。解析顺序：显式 `--start-grace/--deadline-grace/--heartbeat-max-age` → 解析 `watch-target.sh --help` 的 `Defaults:` 行 → `unknown`。`unknown` 时依赖该阈值的判定不触发，输出 `thresholds.value_state=unknown`。watchbeat 自身 `window=` 缺失时同样不得推断新鲜度。

**理由**：FR-004/FR-011 明确阈值的 owner 是 `scripts/watch-target.sh`；帮助文本是脚本自己发布的稳定面。回归测试将把“发现值 == 脚本帮助文本中的值”钉住，漂移即转红。

**否决**：在 `loop-state.py` 内硬编码同一组数字（第二 owner，必然漂移）；要求调用方每次传参（缺省不可用）。

### R-06 watcher 委托与不可用表达

**裁决**：仅当存在活动 watch target 且非 `not-dispatched`、非 `--probe` 时调用 `watch-target.sh --once`，传入既有四件套路径、`--sentinel <STAGE>-DONE`、`--deadline-epoch`（来自脊）与 `--stage`。归属参数按可证性分三态：

1. **归属形态**：`run_id` 已知，且 Registry `meta_paths` 中存在 meta 文件，或四件套信封自带与 `run_id` 相等的 `run=` → 附 `--line-id/--run-id/--registry/--meta`，watcher 输出 `attribution=own`。
2. **兼容形态**：归属不可证（现行 `stage-runner.sh` 的 status/pid 不带 `run=`，且无 meta），且 `stale_signals` 为空 → 不附归属参数，watcher 输出 `attribution=legacy`，正常消费当前证据。
3. **不调用**：归属不可证且存在 stale 信号 → 不调用 watcher，`present=false`、`reason=unavailable`、`detail=stale-evidence`，走 derived（stale 已排除）。

解析 stdout 的 `WATCH ... verdict=... rc=... reason=... attribution=...` 行；`watch_verdict.exit_code` 保存 watcher 的判定码（0 或非零，owner：`watch-target.sh --help`）；usage 与调用失败记 `exit_code=null`。watcher 不可用（脚本缺失、调用失败、超时、输出不可解析、usage）→ `present=false`、`status=missing`、`value_state=na`、`verdict=null`、`reason=unavailable` + `detail=<具体原因>`，改走 derived 映射，绝不伪造 verdict、绝不判 `DEAD`。watch target 是否存在由文件证据判定：pid/status 记录存在、哨兵存在或 `stage_started_at` 可读；否则无目标 → `present=false`、`status=na`、`value_state=na`、`reason=null`。

**理由**：FR-005 与 Q5；A-2 的判定所有权。归属分态避免把一个“无 run= 的现行信封”在 `--line-id` 下误判 `unattributed` 而丢弃终止证据；兼容形态只在快照已排除 stale 后使用，安全性由本地 stale 过滤兜底。`loop-state.py` 的退出码始终由自身阶梯决定，watcher 的退出码只作数据。

**否决**：复刻 watcher 优先级（双 owner）；把 watcher 非零退出当快照失败（FR-012 明确 `loop_state` 是数据）；无条件附 `--line-id`（会复现实测中的“terminating evidence suppressed”盲点）；无条件不附归属参数（会让 stale-run 证据被当作本次证据）。

### R-07 derived `loop_state`：按 FR-004 固定优先级逐条实现，外加两个前置短路

**裁决**：在 FR-004 的 8 条规则**之前**加入两个显式前置分支：

1. `not-dispatched` 判据成立 → `UNKNOWN` + `reason=not-dispatched`（否则规则 (6) 会把从未派发的线误判为 `NO_SIGNAL`）。
2. 远端证据不可达（probe `reachable=false`）→ `STALLED` + `reason=remote-unreachable`（A-13 与 Edge Cases「远端 ssh 不可达」的显式要求；此时不允许混入本地证据去跑规则 (2)–(7)）。

其余严格按 FR-004 的 (1)→(8) 顺序短路；`verdict_source=derived`。与脊 `last_verdict` 不一致时只报 `spine.consistent=false`，不择一。watcher 存在时 `loop_state` 逐字等于 verdict，前置分支只影响中断清单与动作。

**理由**：两条前置条件都不在 FR-004 的“证据已可读”前提内；不显式短路会产生与 FR-002/A-13/Edge Cases 相反的结论。

**否决**：把 remote 当普通 `UNKNOWN`（SSH 抖动会被升级成 stop 之外的猜测链）；把 not-dispatched 交给规则 (6)（把“未开始”误报为“无信号”）。

### R-08 产物映射与提交证据

**裁决**：脚本内 `STAGE_ARTIFACTS` 数据表为机器权威，`references/state-awareness.md` 的同名章节为其人类可读投影，契约测试断言两者一致。表覆盖 8 个阶段，每项含 `artifacts[]`（必需）、`owned_paths[]`（受约束但可选，plan 的 `research.md` 落此）、`commit_required`、`no_change_allowed`。完整性只看“文件存在且非空”（目录类产物要求至少一个非空文件）；`checklist` 阶段另要求自 `stage_base_commit` 起新增或修改的 checklist 文件，仅有预存文件不判完整。提交证据以脊 `stage_base_commit` 为基线，`git log <base>..HEAD -- <pathspec>`；基线缺失 → `commits.value_state=unknown`，不回退“最近一次提交”；`commit_required=false` → `status=na`。implement 的产物完整性以基线后的代码/测试提交表达，`pathspec` 枚举为 `src/`、`skills/`、`scripts/`、`tests/`、`templates/`、`agents/`；仅文档提交不计。`提交齐备` 谓词与特例动作（analyze vacuous complete、clarify 合法无变更、unknown baseline → verify）由 `IA-14` 唯一定义。

**理由**：FR-006/007/008；A-12 的 owner 形式；plan-owned 集合来自 `efficiency-model.md` §3.1，U4 清单来自 `stage-prompts.md`。`research.md` 在 plan 模板中是条件产物，故列为 owned-but-optional，而 `feature-ref.md` 等为本流程必需产物。

**否决**：把所有 plan-owned 路径都当必需（模板允许无 research.md，会制造伪缺失）；用日志文本推断产物（FR-007 明令禁止）。

### R-09 `--probe` 两种形状与隔离

**裁决**：

| 形状 | 判据 | 消费方式 |
|------|------|----------|
| (a) 快照信封 | 顶层含 `schema_version=1` + `watch_verdict` + `evidence` | 逐字消费其 `spine`/`registry`/`watch_verdict`/`evidence`；忽略未知键；本地重算 `loop_state`/`interruptions`/`recovery_action`；`evidence_source=probe` |
| (b) 最小可达性 | `schema_version=1` + `reachable=false` + `reason` | `STALLED` + `remote-unreachable` + 动作 `stop`；所有信号 `missing` |

不可解析、`schema_version≠1`、`reachable=true`（无证据）、与 `--spine/--state-dir/--spec-dir/--repo/--watch-script` 同时出现 → exit 2。probe 模式不读本地任何证据、不调用本地 watcher。

**理由**：Q3 裁决；FR-002 的互斥要求。形状 (a) 的派生字段不直接采信，保证“一个判定算法”。probe 内部的 `fresh` 等由证据所在主机计算，消费侧不重算时间判定，避免跨主机时钟与本地混算。

**否决**：`reachable=true` 空对象（没有可求值证据，只能猜）；只接受 verdict 对象（无法表达整份远端快照）。

### R-10 动作建议：复用父 C 区优先级，只读求值

**裁决**：按下列顺序得出**唯一** `recovery_action`；065a 只输出建议，不执行：

1. `not-dispatched` → `none`。
2. `remote-unreachable` → `stop`。
3. `loop_state=UNKNOWN`（证据缺口）→ `stop`。
4. `unwatched` / `deadline-overrun-live` / `loop_state=RUNNING` /（`TIMEOUT` 且 pid 存活）→ `watch`。
5. `DONE` + `commit_required=false`（含 `commits.status=na`）→ `verify`。
6. （`DONE` 或产物齐备）+ `commits.value_state=unknown` → `verify`（`reason=commit-baseline-unknown`，不得进入 `resume`/`stop` 提交分支）。
7. `DONE` + 产物齐备 + 提交齐备 → `verify`。
8. 产物齐备 + 日志末行非 `ANOMALY:` +（末行哨兵或脊 salvage **完整记录**：`accepted` + `salvage_evidence` + `salvage_at`）→ `resume`；`attempt` 未知时不得给 `resume`（降级 `retry`）。
9. 产物齐备 + 无末行哨兵 + salvage 未完整记录 → `retry`（salvage 门）。
10. 伪完成（末行哨兵而产物缺）→ `retry`，除非证据缺口（`IA-04`）或尝试上限（`IA-15`）改为 `stop`。
11. `STALLED` / `REENTRY_REQUIRED` → `stop`（交回驱动者，不重派）。
12. 其余终态（`INCOMPLETE/ANOMALY/FAILED/DEAD/NO_SIGNAL`；`TIMEOUT` 仅在 pid 不存活时）→ `retry`。
13. 兜底 → `stop`（不猜）。

`提交齐备` 的判据：`commit_required=false` 或 `commits.status=na` → true；`no_change_allowed=true` 且相对 `stage_base_commit` 无变更 → true（clarify 合法无变更）；`value_state=unknown` → false 且走 `verify`；否则以基线后触及阶段产物路径的提交为准（implement 仅代码/测试路径）。analyze 无必需文件产物 → `artifacts.complete=true`（vacuous truth）。`stale-signal` 在 065a 只列入并排除求值，不单独改变候选动作；`stale-unisolated → stop` 由 065c 承接（SA-1 显式推迟）。

在得出候选后应用重试上限：`attempt >= retry_limit` 且候选 ∈ {resume, retry, stop} → `stop`；`watch/none/verify` 不受限。`retry_limit` 取 `--retry-limit` → 引擎常量；常量由契约测试与 `references/stage-prompts.md` § Stall Handling 的缺省值钉住（漂移转红），不在本规格复述。

**理由**：SA-1 与父 requirements C 区「动作裁决优先级」条目；`salvage` 门与“无默认值 resume”来自 A-6/A-11。伪完成优先于 resume，避免把“哨兵在而产物缺”误判为可补提交。

**否决**：065a 自创动作优先级（与 065c 执行分歧）；在缺 `attempt` 时假定 0（会在已耗尽时继续 resume）。

### R-11 确定性

**裁决**：输出不包含 `age_seconds`、剩余时间、生成序号等随时间变化的派生数值；只输出原始 `at`/`mtime_ns` 与布尔判定。`evaluated_at` 是唯一允许在两次同输入运行间变化的字段。probe 模式的 freshness 由 probe 提供，不在本地重算。

**理由**：SC-002 要求“除 `evaluated_at` 外差异数为 0”。输出派生年龄会直接破坏该断言。

**否决**：输出人类友好的年龄字段（可读性让位于可复现性）。

### R-12 `--self-test` 设计

**裁决**：自带临时目录夹具，输出 `ok <case>` / `FAIL <case> — <detail>` 与 `SELF-TEST: N passed, M failed`（与 watcher 的自测形态一致），exit 0/1。覆盖：

- 六类已实现形态（`unwatched` 缺失/过期两分支、`dead-no-exit-record`、`deadline-overrun-live`、`artifacts-without-completion`、`stale-signal`、`remote-unreachable`）；
- 旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 脊、不可达证据；
- `not-dispatched`（含 `--stage` 仅为意图与脊存在排除条件）、Registry 缺失但可继续求值、必需输入与证据源分档（exit 2 vs `missing` + exit 0）、末行哨兵边界（末行哨兵 + 活进程 + 其后 `ANOMALY:` 行）、提交齐备特例（analyze vacuous complete、`commit_required=false`、unknown baseline、clarify 合法无变更、implement 仅文档提交、checklist 仅预存文件）、probe 两形状、probe 拒绝路径、确定性、退出码阶梯与 `--help` 钉住。

并发锁与 `recover/check-spine` 拒绝路径不在本切片自测范围（065c/065b 追加）。

**理由**：FR-012 与 Q1 的“按切片累计覆盖”。自测不依赖真实进程或网络。

### R-13 分发、文档与测试面

**裁决**：

- 源改动只落 `skills/external/sdd-loop-driver/`；`.specify/skills/sdd-loop-driver/` 通过 `scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver` 再生成。
- 新增 owner reference `references/state-awareness.md`，拥有：快照入口、六类检测表（+ 八类封闭词表与 065b 归属）、derived 映射、产物映射章节、probe 契约、动作建议表。`watch-model.md` 不改。
- `SKILL.md` 增加 Reference 行与一条只读 Hard Requirement；`docs/reference/skills/sdd-loop-driver.md` 增加入口、调用形态、与 watcher/Registry 的关系。
- 测试：`tests/unit/test_loop_state_engine.py`（求值逻辑与夹具，含归属三态与无 `run=` 信封）+ `tests/contract/test_loop_state_contract.py`（信封、退出码、probe、自测、确定性、变异演练、AM-01 映射一致性、文档/镜像表）；`tests/contract/test_sdd_loop_driver_skill.py` 的 `MIRROR_FILES` 增补新文件。

**理由**：FR-042/043/044/046/047。

**否决**：把规则写进 `watch-model.md`（FR-043 明令禁止复制恢复规则、且该文件是 watch 判定 owner）；手改镜像（两顶帽子违规）。

## 3. 未决项

无。`NEEDS CLARIFICATION` 计数为 0；5 项 clarify 裁决均已落入设计（见 data-model 与 contracts 的对应条款）。

## 4. 复现命令与测量状态

```bash
bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test
# 本次实测: SELF-TEST: 38 passed, 0 failed; exit 0
```

镜像基线命令**在 plan 阶段未执行**（并发隔离策略拒绝调用该路径上的脚本），它是实现阶段首次编辑前的测量程序，不是本次实测结果：

```bash
python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver
# 判据：记录本次退出的漂移项；实现后只要求“无新增漂移”
```
