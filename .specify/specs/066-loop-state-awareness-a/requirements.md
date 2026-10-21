# Requirements Specification: 状态感知（State Awareness）— Feature 065 / Slice 066

**Requirement Branch**: `065-loop-interruption-recovery`（父特性线；切片规格目录 `066-loop-state-awareness-a`）  
**Created**: 2026-10-21  
**Status**: Draft  
**Input**: User description: "Feature 065 切片 A（状态感知）— 新建 `.specify/specs/066-loop-state-awareness-a/requirements.md`，父 FR-001…012 及适用边界 FR，短名 loop-state-awareness-a"

需求语义权威：父规格 `.specify/specs/065-loop-interruption-recovery/requirements.md`、拆分记录 `notes/decomposition-gate.md`、草案评审 `notes/plan-blocked-review.md`、切片简报 `brief-065a.md`；终态权威为 `skills/external/sdd-loop-driver/{SKILL.md,references/watch-model.md,references/stage-prompts.md,references/efficiency-model.md}` 与项目宪法。

## Related Feature *(mandatory)*

**Feature ID**: 065

**Feature Name**: SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）

**Binding intent**: 本切片是 Feature 065（SDD 循环中断感知与状态恢复）的 A 切片；2026-10-21 `/speckit.clarify` 已完成绑定，不新建第二个 Feature ID、不新增注册行、不改写 065 的 Draft 状态。切片规格目录独立，但 Feature 归属仍是 065。

## Slice Scope（切片边界）

本切片只交付「状态感知」：一次只读调用聚合并输出结构化判定与恢复动作建议；不执行任何恢复副作用。切片 FR 连续编号 001–025；父 FR 的精确编号映射见 `notes/parent-fr-mapping.md`（父引用统一写 `#FR-NNN`），编号变化不构成删除、合并或重排。

| 范围 | 父条目（章节序号） | 本切片处理 |
|------|--------------------|------------|
| 核心 A 区（状态感知） | 父 A 区第 1–12 条 | 全部纳入，映射为 FR-001…FR-012 |
| 边界 D/E 区（兼容、分发、非目标） | 父 D 区第 1–7、9、10 条；E 区第 1–4 条 | 按适用性纳入 13 条，映射为 FR-013…FR-025 |
| 核心 B 区（中断检测与生命周期） | 父 B 区第 1–12 条 | 不在本切片；后续切片承接检测谓词与校验器 |
| 核心 C 区（状态恢复执行） | 父 C 区第 1–13 条 | 不在本切片；后续切片承接 resume/retry/stop 的写入与提交 |
| 边界 D 区第 8 条（跨切片测试矩阵） | 父 D 区第 8 条 | 显式 out-of-slice；A 只覆盖自身测试矩阵，由后续末切片汇总 |
| 边界 D 区第 11 条（记录拓扑 + recover 锁） | 父 D 区第 11 条 | 显式 out-of-slice；A 只读，不产生恢复记录、不持有恢复锁 |

本切片 FR 定义总数 = 25（12 条核心 + 13 条边界），低于拆分门上限 30。

### Out-of-Slice Boundary Items

| 父条目（章节序号） | 归属 | 不纳入本切片的理由 |
|--------------------|------|--------------------|
| 父 D 区第 8 条 | 后续切片（末切片汇总） | 测试矩阵中的 retry/stop/隔离/四要素上送件依赖恢复执行切片；A 只按 FR-020 覆盖自身新增检查与逆样本。 |
| 父 D 区第 11 条 | 后续切片（恢复执行） | A 的快照只读求值，不写状态脊、不持有 `recover --apply` 锁、不产生并发写；记录拓扑与锁语义在执行切片落地。 |

精确的父 FR 编号（`#FR-NNN`）见 `notes/parent-fr-mapping.md`。

## Assumptions（父裁决 + 切片裁决）

以下父 Assumptions 适用于本切片，保留父编号并注明切片落点。A-7、A-8、A-9、A-19 以恢复执行、提交、隔离或并发写为前提，不在本切片适用。

- **A-1 入口形态**: 新建单一引擎 [[STR-001]]（Python 3 标准库）承载 `snapshot`（只读）、`recover`（默认 dry-run、`--apply` 才变更）与 `check-spine`（只读校验）三个动作，外加 `--self-test`。切片落点：A 实现 `snapshot` 与 `--self-test` 的快照部分；共享 JSON 信封与退出码阶梯在本切片冻结，`recover` / `check-spine` 的动作执行由后续切片承接。
- **A-2 判定所有权**: watch 域判定仍由 `watch-target.sh` 唯一拥有。`loop-state.py` 只调用 `--once` 或消费调用方提供的 WATCH 快照，绝不重新实现信号优先级与退出码；`loop_state` 在存在活动 target 时逐字等于 watcher 判定。
- **A-3 两套词表分离**: `loop_state`（快照输出的聚合判定，大写）与 `spine_state`（状态脊文件状态，小写连字符）是两个词表，各自有 owner，不互相替代；快照显式报告二者及 `spine.consistent`。
- **A-4 第五信号 watchbeat**: 新增由驱动者写入的 watchbeat 标记 [[STR-002]]`<line>-<stage>`，每窗口开始/返回各一次原子覆盖。它是驱动者存在证据，不是完成/存活信号，不参与任何 watch 判定；状态脊仍遵守「RUNNING 窗口不写」的既有规则。
- **A-5 动作集合**: 恢复动作取封闭集 `none / watch / verify / resume / retry / stop`。A 只输出建议，不执行；`watch` 表示继续监听，`verify` 表示进入独立校验，`none` 表示未派发或不适用。
- **A-6 salvage 有界例外**: 产物齐备但无正向终止证据时，`resume` 必须由驱动者显式记录 `salvage` 判定才允许；未记录时一律 `retry`。切片落点：A 只把 salvage 声明作为动作裁决的输入并输出 `salvage` 对象，不写记录、不提交。
- **A-10 停线不杀进程**: `stop` 只写 `stalled` 与四要素上送件，不 kill、不删 worktree；活进程的 TIMEOUT 停线必须先做最终 `--once` 快照并经用户显式决定。切片落点：A 只输出 `stop` 建议与理由，不执行。
- **A-11 状态脊机读段**: 状态脊增加固定 fencing 内的 `key: value` 机读段；散文部分不变。legacy 状态脊（无可读段）降级求值，缺字段记 `unknown`，不猜测、不补默认值。
- **A-12 产物映射 owner**: 阶段→产物映射由脚本内数据 + 对应 reference 章节唯一定义，并与 U4 的产物核验清单对齐；plan 阶段使用 `efficiency-model.md` §3 的 plan-owned 集合；analyze 无提交要求，clarify 允许无变更。
- **A-13 远端拓扑**: 聚合器在证据所在主机以同一执行身份运行，或消费调用方经 ssh 采集的 probe 快照；ssh 不可达记 `stalled(remote-unreachable)`，绝不记 `DEAD`。
- **A-14 未派发语义**: 尚未派发的线不在本特性判定范围内；快照以 `UNKNOWN` + `recovery_reason=not-dispatched` 表达，`completion=not-applicable`，恢复动作为 `none`。未派发谓词与优先级见 FR-002；注册本身不构成派发证据。
- **A-15 Feature 绑定**: 父特性 065 已注册为 Draft；本切片复用该绑定，不新增 Feature ID、不新增注册行。Related Feature 的最终绑定由 `/speckit.clarify` 完成（2026-10-21 已绑定）。
- **A-16 derived 映射**: 无活动 watcher 时，`loop_state` 由独立、固定优先级的聚合映射表导出，始终标注 `verdict_source=derived`；它不是 watcher 判定状态机的复制，不得声称具有 watcher 判定的语义或退出码。映射与状态脊 `last_verdict` 冲突时只报 `spine.consistent=false`，不静默择一。
- **A-17 引擎 CLI 契约**: 三个动作共享同一 JSON 信封（含 `schema_version`）与退出码阶梯 `0/1/2`；远端 probe 快照经 `--probe <file>` 输入。切片落点：A 冻结并验证 `snapshot` 的信封、退出码与 `--probe` 路径；变更动作在后续切片实现。
- **A-18 状态脊机读段**: 使用独立 fence `<!-- loop-state:begin -->` … `<!-- loop-state:end -->` 与 `spine_schema: v1`；状态键使用 `spine_state:` 前缀，MUST NOT 使用裸 `state:` 键；状态枚举为 `running / retrying / stalled / reentry-required / done`。切片落点：A 只读解析并报告 schema，不写状态脊。

切片裁决（吸收 blocked-review findings；`/speckit.clarify` 可推翻）：

- **SA-1 动作建议与执行分离**: A 输出 `recovery_action` 与 `interruptions[]`，其封闭动作集与裁决顺序沿用父恢复动作规则的只读投影；A MUST NOT 触发提交、隔离、重派、停线或任何写操作。执行、salvage 记录与四要素上送件归后续切片。
- **SA-2 编号空间**: 切片 FR 连续编号 001–025；父 FR 在 Parent FR Mapping 表以章节序号引用，精确 `#FR-NNN` 映射见 `notes/parent-fr-mapping.md`。此裁决不构成对父 FR 的删除、合并或重排。
- **SA-3 跨切片证据**: `stale-signal`、legacy 状态脊与 `remote-unreachable` 的完整检测谓词由后续切片拥有；A 只保证输出字段、封闭形态集合、归属裁决与 `missing`/`unknown` 语义，不重新定义检测阈值或 watcher 数值。
- **SA-4 只读边界**: A 的所有执行路径 MUST NOT 写状态脊、写四件套、移动/删除证据、提交或杀进程；显式 `--out` 持久化是唯一例外，且不得写入状态目录或工作树。
- **SA-5 未提交证据不权威**: 父特性 umbrella 草案 `plan.md`、`research.md`、`data-model.md`、`contracts/`、`quickstart.md`、`feature-ref.md` 不作为本切片的权威输入，也不因其存在而放宽本切片的 FR 范围。
- **SA-6 载体归属唯一规则（吸收 finding 1）**: 每个信号载体的归属 MUST 由载体自身信封（`line=`/`run=`/`stage=`）裁决；只有 `own` 参与求值，`stale-run`/`unattributed`/`foreign` 只进入 `stale_signals[]`。legacy 归属模式仅允许在恰有一条活动线且载体无法用信封证明归属时启用；多活动线 MUST NOT 以 legacy 模式绕过归属过滤。该规则替代草案中 `own`/`legacy` 的重复定义。
- **SA-7 salvage 是裁决输入（吸收 finding 2）**: salvage 声明 MUST 在动作裁决之前作为输入参与（来自状态脊 `salvage: accepted` + `salvage_evidence` + `salvage_at`，或只读调用参数提供的证据引用），MUST NOT 作为裁决后的覆盖开关。没有 salvage 输入时，产物齐备但无哨兵一律裁决为 `retry`。
- **SA-8 形态只注释（吸收 findings 3–5）**: 中断形态只作为证据注释，MUST NOT 设置或覆盖 `loop_state`；ANOMALY 谓词在「退出记录存在或进程已死」时求值；`dead-no-exit-record` 必须同时满足无哨兵；活进程 TIMEOUT 的动作建议只能是 `watch`。
- **SA-9 状态脊键与一致性（吸收 findings 6、8）**: 快照 MUST 读取 `spine_stage_base_commit`、`spine_stall_reason`、`spine_retry_reason`、`last_verdict`；缺失记 `unknown`。`stalled`/`retrying` 缺少 `last_verdict` MUST NOT 单独判 `spine.consistent=false`；`spine.consistent` 的三态判据见 FR-004。U2 写入 `stage_base_commit` 的义务属状态脊机读段切片；A 以缺失夹具证明不会猜测。
- **SA-10 completion 与 loop_state 分离（吸收 finding 7）**: 快照新增独立 `completion` 字段；`loop_state` 保持 watcher 逐字判定，伪完成（哨兵在而产物缺）只改变 `completion` 与动作建议，不把 `loop_state` 从 `DONE` 改为 `INCOMPLETE`。
- **SA-11 watcher 字节锚点（吸收 finding 9）**: 兼容性契约 MUST 钉住 `watch-target.sh` 的 SHA-256 基线；`--self-test` 位于被保护文件内部，不能单独作为回归证据。基线值在实现时从当前文件捕获并由测试钉住。
- **SA-12 Registry 缺失路径（吸收 finding 10）**: 输出新增 `registry` 对象；`registry.status=missing` 时，状态脊与四件套可读则继续求值；Registry 存在而状态脊缺失时判 `UNKNOWN` + `stop`，不得凭 Registry 单独猜阶段。
- **SA-13 非 A findings 的显式移交**: finding 11（锁仅限变更动作）与 finding 12（活进程 `stop` 需 `--confirm-live-stop`）属恢复执行切片；A 只读，不获取恢复锁，且对活进程 TIMEOUT 只建议 `watch`。finding 13（quickstart 生命周期）与 finding 15（基线标签）不适用于 A。
- **SA-14 具名测试夹具（吸收 finding 14）**: A 的测试 MUST 使用具名夹具覆盖 `sentinel-with-missing-artifact`、`legacy-spine-snapshot`、`artifacts-without-completion`、`dead-no-exit-record`、`unwatched-vs-window`、`registry-missing`、`probe-snapshot`；测试文件自身枚举夹具名，不在 checklist 中手抄。
- **SA-15 clarify 裁决落地（2026-10-21）**: 本次 clarify 的五项裁决已落入 FR-002/FR-003/FR-004/FR-005/FR-007/FR-009/FR-010/FR-012 与 `## Clarifications`；快照字段闭域以 `#### Snapshot Field Contract (normative)` 为准，未列字段只允许追加。

## Blocked-Review Reconciliation（A 相关 findings）

来源：`.specify/specs/065-loop-interruption-recovery/notes/plan-blocked-review.md`。下表逐条记录 A 的吸收方式；未列入的 finding 已在 SA-13 显式移交或标为不适用。

**三个跨切片主题**：状态脊权威（Registry 存在而状态脊缺失 → `UNKNOWN` + `stop`；快照不从 Registry 单独猜阶段）、verdict 委派（watcher 逐字判定与 derived 映射分离；中断形态只注释）、证据可复现（同一输入除 `evaluated_at` 外输出一致；每个信号带证据指针与来源）。

| # | Finding | A 相关面 | 本规格处理 |
|---|---------|----------|------------|
| 1 | 归属冲突：`own`/`legacy` 重复且不一致 | 四件套、watchbeat、日志归属 | FR-002 + SA-6：载体信封唯一裁决；legacy 仅单活动线；非 own 只入 `stale_signals[]` |
| 2 | salvage 门循环依赖 | 动作建议 | FR-003 + FR-007 + SA-7：salvage 作为裁决输入；无输入时一律 `retry` |
| 3 | ANOMALY 谓词被 own status 限制 | derived 映射 | FR-004 + SA-8：谓词为「退出记录存在或进程已死」 |
| 4 | `dead-no-exit-record` 与哨兵冲突 | 中断形态 | FR-009 + SA-8：该形态要求无哨兵；有哨兵走 completion 判定 |
| 5 | 中断形态覆盖 `loop_state` | 判定委派 | FR-004 + FR-009 + SA-8：形态只注释；只有 watcher 逐字或 derived 映射设置 `loop_state` |
| 6 | 状态脊 schema 与写入者不一致 | 状态脊读取 | FR-003 + FR-008 + SA-9：暴露 `stage_base_commit`/`stall_reason`/`retry_reason`；stalled/retrying 可无 `last_verdict` |
| 7 | 伪完成双重绑定 | 输出契约 | FR-003 + FR-007 + SA-10：新增 `completion`；哨兵在产物缺 = `completion=incomplete`，`loop_state` 不变 |
| 8 | `stage_base_commit` 无写入者 | 提交证据 | FR-008 + SA-9：A 读取并测试缺失 → `commit=unknown`；写入义务移交状态脊机读段切片 |
| 9 | watcher 非回归无法转红 | 兼容性 | FR-013 + SA-11：契约测试钉住 watcher SHA-256 |
| 10 | Registry 缺失路径无载体 | 输入解析 | FR-002 + FR-003 + SA-12：新增 `registry` 对象与继续求值路径 |
| 11 | 锁与无写动作冲突 | 恢复锁 | Out-of-slice（SA-13）；A 不获取锁、不写状态 |
| 12 | 活进程 TIMEOUT 停线未定义 | 动作建议 | FR-009 + SA-13：A 对活进程只建议 `watch`；`--confirm-live-stop` 归执行切片 |
| 13 | quickstart 生命周期 | 不适用 | A 不产出 quickstart |
| 14 | 测试矩阵缺少具名夹具 | 测试义务 | FR-012 + FR-020 + SA-14：具名夹具由测试文件枚举 |
| 15 | 基线标签错误 | 不适用 | A 不声称 engine baseline 数字 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次调用看清一条线的真实状态 (Priority: P1)

使用者或新接手的驱动会话面对一条可能中断的线，不再逐一检查 pid/status/log/heartbeat/产物与 git 提交。只需按线调用一个确定性入口，即可得到：当前阶段与断点、状态脊状态、四件套证据、产物与提交完整性、watcher 最近判定、识别出的中断形态、独立的完成度判定，以及唯一建议的下一步动作。所有缺失信号显式标为 `missing`/`unknown`，不猜测。

**Why this priority**: 这是「状态感知」的最小可用价值，也是恢复与生命周期治理的共同前提；实测事故中恢复耗时几乎全部花在人工拼装这些证据上。

**Independent Test**: 用夹具构造一条「产物齐备、未提交、`exit=1`、无哨兵、无 watcher」的线，调用快照入口，核对输出字段、证据指针与建议动作；再构造一条正常运行中的线、一条未派发的线与一条「哨兵在而产物缺」的线，核对 `loop_state`、`completion` 与 `verdict_source` 的差异。

**Acceptance Scenarios**:

1. **Given** 一条线的状态脊与四件套可读、watcher 可调用，**When** 执行一次快照，**Then** 输出包含阶段、`loop_state`、`verdict_source`、`watch_verdict`、`completion`、`recovery_action`、`recovery_reason`、产物/提交清单、`interruptions[]`、`registry` 与 `salvage`，且所有路径可定位。
2. **Given** 阶段运行中且刚完成一个监听窗口（watchbeat 新鲜），**When** 执行快照，**Then** `loop_state=RUNNING`、`verdict_source=watcher`，且不报 `unwatched`。
3. **Given** 阶段运行中但驱动者从未启动 watcher（无新鲜 watchbeat），**When** 执行快照，**Then** 报 `unwatched` 中断并建议 `watch`，不报提交、重派或终止建议。
4. **Given** 阶段产物齐备但无哨兵且未提交，**When** 执行快照且无 salvage 输入，**Then** `completion=incomplete`，不得判 `DONE`，动作建议为 `retry`；提供有效 salvage 证据后，动作建议可转为 `resume` 候选。
5. **Given** 阶段已写出哨兵但产物缺失，**When** 执行快照，**Then** `loop_state` 保持 watcher 的逐字判定（例如 `DONE`），`completion=incomplete`，动作建议为 `retry`；不得把 `loop_state` 改写为 `INCOMPLETE`。
6. **Given** 任一信号缺失或不可读，**When** 执行快照，**Then** 该信号以 `missing`/`unknown` 出现，输出中不出现零值或 `ok` 猜测。
7. **Given** Registry 条目缺失但状态脊与四件套可读，**When** 执行快照，**Then** 继续求值并输出 `registry.status=missing`；**Given** Registry 存在但状态脊缺失，**Then** `loop_state=UNKNOWN` 且建议 `stop`。
8. **Given** 同一次求值命中多个中断形态，**When** 执行快照，**Then** 全部列在 `interruptions[]`，且任一形态都不改变 `loop_state`。

---

### User Story 2 - 既有语义与分发面不回归 (Priority: P2)

使用者在升级后，现有 watcher 判定、四件套格式、Line Registry、阶段命令、确认门与 fast-fail 纪律保持原样；新增能力仅以增量层出现。框架源、运行时镜像、文档与测试保持一致，没有新增常驻服务或外部依赖。

**Why this priority**: 该特性改善的是「出事后的恢复」，若以改变判定语义或引入新运行时为代价，风险大于收益。拆分记录要求兼容性验收在每个切片运行；本切片以 P2 承接。

**Independent Test**: 运行既有 watcher `--self-test`、驱动技能契约测试、Registry 引擎测试与镜像一致性检查；对比升级前后的判定输出与退出码；核对 watcher 文件 SHA-256 锚点。

**Acceptance Scenarios**:

1. **Given** 既有 `watch-target.sh --self-test`，**When** 升级后运行，**Then** 全部用例保持绿色，判定与退出码零差异。
2. **Given** watcher 文件被任何字节修改，**When** 运行兼容性契约测试，**Then** SHA-256 锚点断言失败并指出漂移。
3. **Given** 既有四件套与 Registry 条目，**When** 升级后读取，**Then** 字段语义与 action 行为不变，旧条目可读。
4. **Given** 框架源改动，**When** 运行镜像同步与一致性检查，**Then** 运行时镜像字节一致，漂移为 0。
5. **Given** 既有 `/speckit.*` 命令与阶段提示词，**When** 升级后运行，**Then** 三段骨架、哨兵字面量、确认门与 no-push 策略不变。

### Edge Cases

- 驱动者派发后在同一回合启动 watcher，但 watcher 第一次调用即超时：watchbeat 存在且新鲜，不得报 `unwatched`；按调用失败处理，重入新窗口。
- 监听窗口正常到期（`RUNNING`）与「无 watcher」同时看似成立：以 watchbeat 是否新鲜区分；新鲜 = 正常窗口，不报中断。
- 阶段已写出哨兵但进程仍活：`loop_state` 可为 watcher 的 `DONE`，`completion` 仍须产物齐备，动作 `verify`。
- 阶段已完成（`completion=complete`）且产物齐备但提交证据 `missing`：动作建议 `resume`（仅补提交，不重派）；implement 代码路径不自动提交，仍按 implement 规则处理。
- 哨兵在而产物缺：`completion=incomplete`，动作 `retry`，不得建议 `resume`；`loop_state` 保持逐字判定。
- 产物齐备、无哨兵、但日志最后一行是 `ANOMALY:`：不满足 salvage 前提，动作 `retry`。
- 产物齐备、无哨兵、`exit=1`、无异常行：salvage 候选；没有显式 salvage 输入时动作仍为 `retry`。
- 旧 status 的 `run_id` 与当前一致但 mtime 早于 `stage_started_at`：按 stale 处理并列入 `stale_signals[]`。
- 旧 status 无信封且无法判断归属：按可疑处理并列入 `stale_signals[]`，记录 `legacy-stale` 原因；多活动线时不得启用 legacy 模式。
- `pid` 文件指向已复用 PID：start ticks 不符，判 `DEAD`/身份不符，不附着。
- deadline 已过、pid 活、心跳新鲜、且 status 尚未出现：`loop_state` 由 derived 映射判 `TIMEOUT`，中断形态为 `deadline-overrun-live`，动作建议 `watch`；只有用户显式决定才停线。
- deadline 已过、pid 死、无 status：最终快照后按父恢复动作规则建议 `retry` 或 `stop`，A 不执行。
- 状态脊是 legacy 格式（无机读段）：降级求值，缺失字段为 `unknown`；不得据默认值建议 `resume`。
- Registry 条目缺失但状态脊与四件套可读：继续求值并记 `registry.status=missing`；不得因此判 `UNKNOWN`。不可读/格式无效分别记 `unreadable`/`invalid`，不得合并为 `missing`。
- Registry 条目存在但状态脊缺失/不可读且无 watcher/probe 判定：`UNKNOWN` + `stop`，上送证据缺口；该路径先于未派发判定，不得因「没有阶段绑定」改判 `none`；不得凭 Registry 单独猜阶段。若 watcher/probe 判定存在，`loop_state` 保持逐字判定，状态脊缺口以 `lifecycle-spine-violation` + `stop` 建议记录，不得改写 `loop_state`；阶段信封不可得时 `stage=unknown`。
- 已注册但从未派发：无 `stage_started_at`/`stage_deadline_epoch`、无 `stage`/`run_id` 绑定、无可归属载体与 watcher/probe 判定，且状态脊无可读 legacy 阶段/断点记录时，按未派发处理（`UNKNOWN` + `recovery_reason=not-dispatched` + `none`），不得判 `NO_SIGNAL` 或 `RUNNING`。legacy 状态脊有可读阶段/断点记录时不算未派发，缺字段按 `unknown` 降级求值。
- 有效阈值缺失（watcher 不可用且无 CLI/probe/spine 来源）：依赖该阈值的 derived 判定记 `UNKNOWN` 且 `effective.<key>.value=unknown`；不得用硬编码默认值猜测，也不得把缺失当成 0。
- 有效重试上限或已试次数缺失：跳过「达到上限」规则并记 `recovery_reason=retry-limit-unknown`；不得猜测上限或默认 attempt=0。
- 同线 `stale-run` 归属明确：动作 `retry` + `isolation_required=true`；仅 `foreign`/`unattributed` 载体存在时不得改变动作或建议 `retry`。
- 远端 ssh 不可达：中断形态 `remote-unreachable`，`loop_state` 仍由 derived 求值（通常 `UNKNOWN`），动作建议 `stop` 并附原因；不得判 `DEAD`，不得重派。
- 状态脊 `spine_state=stalled` 或 `reentry-required` 但缺少 `last_verdict`：不单独判 `spine.consistent=false`；缺失字段记 `unknown`。
- 状态脊缺少 `stage_base_commit`：`commit=unknown`，不得回退猜测「最近一次提交」。
- `commit_required=false` 的阶段：`commit=not-applicable`，不因无提交判 incomplete。
- 快照运行期间 watcher 恰好结束：以 `--once` 的当次输出为准；不得混用两次调用的证据。
- `--probe` 快照缺少某信号：该信号记 `missing`/`unknown`，`evidence_source=probe`；不得回退读取本机同名文件。probe 只带 derived 判定时，本地必须重新求值而不得升级为 watcher 判定。
- `state-dir` 无法解析：watchbeat 记 `missing` 且 `recovery_reason=state-dir-unknown`；不得扫描全盘或猜测路径。
- 未派发的线：`loop_state=UNKNOWN`、`recovery_reason=not-dispatched`、`completion=not-applicable`、动作 `none`。
- 同一输入两次快照：除 `evaluated_at` 外输出一致；任何形态或动作不得依赖调用时刻的隐式状态。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 状态感知（State Awareness）

- **FR-001**: 驱动技能 MUST 提供一个确定性、只读的状态聚合入口 [[STR-001]]（Python 3 标准库、零外部依赖），一次调用聚合状态脊、Line Registry 条目、pid/status/log/heartbeat 四件套、watchbeat 标记、阶段产物、git 提交与可用的 watcher 判定；快照动作 MUST NOT 写文件、改状态、杀进程或修改工作树（显式 `--out` 持久化除外）。切片 A 实现 `snapshot` 与 `--self-test` 的快照部分；`recover` / `check-spine` 的动作执行由后续切片承接，但共享 JSON 信封与退出码阶梯在本切片冻结。
- **FR-002**: 入口的输入解析顺序 MUST 为：显式 `--spine`/`--state-dir`/`--spec-dir`/`--repo`/`--probe` 覆盖 → 按 `--line-id` 读取 Registry 条目 → 失败。`--probe <file>` 是调用方经 ssh 采集的只读快照（schema 与 `snapshot` 输出同一 `schema_version`，见 FR-005）；显式提供时以其证据为准并在输出标注 `evidence_source=probe`。`registry.status` MUST 取 `found|missing|unreadable|invalid`；Registry 缺失、不可读或格式无效但状态脊与四件套可解析时 MUST 继续求值，并分别保留 `missing`/`unreadable`/`invalid`，MUST NOT 合并为同一原因。Registry 条目存在而状态脊缺失/不可读时，**仅当 `verdict_source=derived` 且无 watcher/probe 判定** MUST 判 `loop_state=UNKNOWN` 并建议 `stop`；存在 watcher/probe 判定时 `loop_state` MUST 按 FR-004 逐字保留，该证据缺口 MUST 以 `lifecycle-spine-violation` 中断条目 + `stop` 建议记录，MUST NOT 借此改写 watcher 判定；此时若 Registry/载体也无法提供阶段信封，`stage` MUST 记 `unknown`。Registry 条目存在而状态脊缺失/不可读的路径 MUST 先于未派发判定；只有 Registry 缺失/不可读/无效且无任何派发证据时才按未派发处理。未派发判定 MUST 先于 FR-004 的 derived 状态规则：仅当不存在任何派发证据——状态脊既无可读机读段也无可读 legacy 阶段/断点记录（或两者均缺少 `stage_started_at`/`stage_deadline_epoch`），Registry 条目无 `stage`/`run_id` 绑定，且无可归属载体与 watcher/probe 判定——时，记 `loop_state=UNKNOWN`、`recovery_reason=not-dispatched`、`completion=not-applicable`、动作 `none`；注册本身不构成派发证据，legacy 状态脊中的可读阶段/断点记录构成派发证据（缺字段按 FR-004 降级为 `unknown`，不得据此判 `DONE`/`RUNNING`）。derived 规则使用的启动宽限期锚点 MUST 取状态脊 `stage_started_at`；该字段缺失时取最早的可归属载体 mtime；两者皆无即按未派发处理，MUST NOT 以快照调用时刻代替。任何必需输入缺失 MUST 显式记为 `missing`，MUST NOT 以零值或猜测填充。四件套、watchbeat 与日志的归属 MUST 由载体自身信封（`line=`/`run=`/`stage=`）裁决；只有 `own` 参与求值，`stale-run`、`unattributed`、`foreign` 与无法证明归属的 legacy 载体 MUST 只进入 `stale_signals[]`，MUST NOT 作为本次尝试的证据。legacy 归属模式仅允许在恰有一条活动线时启用；多活动线 MUST NOT 以 legacy 模式绕过归属过滤。
- **FR-003**: 快照输出 MUST 为机器可读 JSON，至少含：`schema_version`（初始值 `1`）、`line_id`、`run_id`、`stage`、`loop_state`、`verdict_source`、`watch_status`、`watch_verdict`、`completion`、`recovery_action`、`recovery_reason`、`recovery_detail`、`isolation_required`、`spine`（path/state/schema/consistent/fields）、`registry`（status/entry/pointer/error）、`evidence`（pid/status/log/heartbeat/watchbeat/artifacts/commits，含 `evidence_source=local|probe` 与每项归属）、`effective`（含 `start_grace`/`deadline_grace`/`heartbeat_max_age`/`retry_limit`/`attempt`/`sentinel`，每项 `{value, source}`）、`salvage`（declared/evidence/source）、`interruptions`、`missing_artifacts`、`uncommitted_artifacts`、`stale_signals`、`evaluated_at`；每个信号 MUST 标注 `present|missing|na` 及证据指针。字段闭域、类型与路径形态 MUST 以 `#### Snapshot Field Contract (normative)` 为准；未列字段只允许追加，旧读取方 MUST 可忽略未知字段。`completion` MUST 取自封闭集 `complete|incomplete|unknown|not-applicable`，并与 `loop_state` 分离：`loop_state` 只由 FR-004 的 watcher 逐字判定或 derived 映射产生，`completion` 只回答「是否具备完成的正证据 + 产物是否齐备」。`spine.fields` MUST 至少暴露 `stage_base_commit`、`last_verdict`、`stall_reason`、`retry_reason`；字段缺失记 `unknown`，MUST NOT 补默认值。`recovery_action` MUST 取自封闭集 `none / watch / verify / resume / retry / stop`，按以下固定顺序只读裁决，同一输入 MUST 得到同一建议（除 `evaluated_at` 外可复现）：(1) 未派发（FR-002 谓词）→ `none`；(2) 证据不足（`UNKNOWN` 且非未派发）、`remote-unreachable` 或 `lifecycle-spine-violation` → `stop`；(3) 已试次数达到有效重试上限 → `stop`（`watch`/`none`/`verify` 不受此限；有效值来源与优先级见 FR-004；若 `attempt` 或 `retry_limit` 任一为 `unknown`，MUST 记 `retry-limit-unknown` 并跳过本规则，MUST NOT 猜测上限或把缺失当 0）；(4) `stale-signal` 无法归属 → `stop`；仅同线 `stale-run` 归属明确且存在 → `retry`（`isolation_required=true`）；`foreign`/`unattributed` MUST NOT 改变动作，也 MUST NOT 建议 `resume`；(5) 运行中/监听缺失/`deadline-overrun-live` → `watch`；(6) `completion=complete` 且产物与提交齐备 → `verify`；(7) `completion=complete` 且提交证据为 `missing`、该阶段允许恢复提交且非 implement 代码路径 → `resume`（仅补提交，不重派）；(8) 产物齐备、无正向完成证据（哨兵缺失或非 `exit=0`）、有有效 salvage 输入、且非 implement 自动提交场景 → `resume` 候选；有效 salvage 输入 MUST 来自只读参数 `--salvage-evidence <ref>`（可重复）或状态脊 `salvage: accepted` + `salvage_evidence` + `salvage_at`，前者 MUST NOT 写状态脊；无至少一个可定位引用时视为无输入；(9) 伪完成、其余终态或产物齐备但无 salvage 输入 → `retry`；(10) 其余 → `stop`。`recover` 输出 MUST 复用同一 `schema_version` 信封，并至少含 `action`、`applied`（bool）、`result`（`dry-run|applied|already-applied|locked|refused|failed`）、`steps[]`、`reason`；动作执行由后续切片承接；A 只输出建议，不产生副作用。
- **FR-004**: `loop_state` MUST 取自封闭集 `RUNNING / DONE / INCOMPLETE / ANOMALY / FAILED / DEAD / TIMEOUT / NO_SIGNAL / STALLED / REENTRY_REQUIRED / UNKNOWN`。存在活动 watch target 时，`loop_state` MUST 与 watcher 判定逐字一致且 `verdict_source` 取 [[STR-006]]，聚合器 MUST NOT 改写、降级或升级该判定。无 watch target 时 `verdict_source` 取 [[STR-005]]，按下列固定优先级推导（含 [[STR-004]] 的映射），且 MUST NOT 复制或声称 watcher 判定：

  1. 状态脊 `spine_state=stalled` → `STALLED`，`spine_state` 为 [[STR-004]] → `REENTRY_REQUIRED`；
  2. 若（退出记录存在或进程已死）且日志最后非空行以 `ANOMALY:` 开头 → `ANOMALY`；
  3. 否则退出记录 `exit≠0` → `FAILED`；
  4. 否则退出记录 `exit=0` 且哨兵存在且产物齐备 → `DONE`；
  5. 否则退出记录 `exit=0` 且（哨兵缺失或产物缺）→ `INCOMPLETE`；
  6. 无退出记录但哨兵存在：产物齐备 → `DONE`，产物缺 → `INCOMPLETE`；
  7. 无退出记录、pid 记录存在且进程已死/start ticks 不符 → `DEAD`；
  8. 有 `stage_deadline_epoch` 且 now ≥ deadline + `effective.deadline_grace` 且无终态 → `TIMEOUT`（活进程也判 `TIMEOUT`，动作建议仍按 FR-003 为 `watch`）；
  9. pid 记录与退出记录均缺失且超过 `effective.start_grace` → `NO_SIGNAL`；
  10. pid 存活或心跳年龄 ≤ `effective.heartbeat_max_age` 且未命中上述终态 → `RUNNING`；
  11. 其余 → `UNKNOWN`。

  启动宽限期、deadline grace 与心跳新鲜度均由 watcher 参数/标记 owner 定义（`scripts/watch-target.sh`；本规格不复述数值）。`effective` 输入 MUST 按以下优先级解析每个阈值/重试值：显式 CLI 参数（`--start-grace`/`--deadline-grace`/`--heartbeat-max-age`/`--retry-limit`/`--attempt`/`--sentinel`/`--no-sentinel`）→ `--probe` 快照携带的 `effective`/`params` → 状态脊机读段对应字段 → 阶段产物映射的哨兵配置 → watcher `--help` 暴露的缺省值（解析而不复制数值）。任一来源都不可得且某判定依赖该值时，该判定 MUST 记 `UNKNOWN` 且 `effective.<key>.value=unknown`，MUST NOT 猜测或回退到硬编码数字；`effective` MUST 在输出中逐项标注取值来源。derived 映射的证据谓词与 watcher 同名判定保持一致，但它是独立的聚合映射，不产生 watcher 的退出码。`spine.consistent` MUST 为三态：仅当最终 `loop_state` 与 `last_verdict` 都属于 watcher 判定闭集时按字面比较（相同 `true` / 不同 `false`）；`last_verdict` 缺失或为 `unknown`，或最终 `loop_state` 为 `STALLED`/`REENTRY_REQUIRED`/`UNKNOWN` 时记 `unknown`，MUST NOT 判 `false` 或静默择一；`stalled`/`retrying` 状态脊缺少 `last_verdict` MUST NOT 单独判为不一致。中断形态 MUST 只作注释，MUST NOT 设置、覆盖、降级或升级 `loop_state`；只有本条的 watcher 逐字判定与 derived 映射可以产生 `loop_state`。ANOMALY 谓词 MUST 在「退出记录存在或进程已死」时求值，MUST NOT 以「存在 own status 记录」为前提。映射表由 FR-018 的唯一 owner 文档定义，代码与测试引用它。
- **FR-005**: 监听域判定 MUST 经既有 `watch-target.sh --once`（与 runner 同一执行身份）取得，或消费调用方提供的快照；聚合器 MUST NOT 重新定义或声称 watcher 的判定状态机、信号优先级或退出码。watcher 不可用（ssh 255、宿主工具超时、脚本缺失）时 MUST 记 `watch_status=unavailable`、`watch_verdict=null`，并且只能走 FR-004 的 derived 映射（`verdict_source` 取 [[STR-005]]），MUST NOT 判为阶段失败、`DEAD` 或伪造 watcher 判定。`--probe <file>` 消费与 `snapshot` 输出同一 `schema_version` 的只读快照（不引入私有 probe 格式）；若 probe 的 `watch_status=available` 且 `watch_verdict` 非空，则视为调用方提供的 watcher 判定并逐字采用（`verdict_source=watcher`）；否则本地 MUST 按 FR-004 从 probe 证据求值（`verdict_source=derived`），MUST NOT 把 probe 的 derived 结果升级为 watcher 判定。所有来自 probe 的证据项 MUST 标注 `evidence_source=probe`；probe 缺失的字段记 `missing`/`unknown`，MUST NOT 回退读取本机同名文件，MUST NOT 与其内容冲突时静默择优。
- **FR-006**: 阶段产物映射 MUST 由单一 owner（脚本内数据 + 对应 reference 章节）定义，覆盖 `requirements / clarify / plan / tasks / checklist / analyze / implement / review`，每阶段显式标注 `commit_required` 与 `no_change_allowed`；映射 MUST 至少覆盖 U4 的产物核验清单（owner：`references/stage-prompts.md` § Independent Verification），plan 阶段另须覆盖其 plan-owned 设计件集合（owner：`references/efficiency-model.md` §3），analyze `commit_required=false`，clarify `no_change_allowed=true`。切片 A 只消费映射，不执行阶段命令；映射与 U4 清单对齐的测试在本切片建立。
- **FR-007**: 产物完整性 MUST 只由「文件存在且非空」判定，MUST NOT 从日志文本推断；哨兵仍是唯一的完成声明；哨兵字面量与是否要求哨兵 MUST 由 FR-006 的阶段产物映射提供，并允许 `--sentinel <literal>`/`--no-sentinel` 显式覆盖；`stage=unknown` 且无法取得映射时记 `effective.sentinel.value=unknown`，`completion` MUST NOT 判 `complete`。「哨兵在而产物缺」MUST 判为伪完成，MUST NOT 因产物部分存在而判 `DONE`。`completion` MUST 按以下规则求值：未派发 → `not-applicable`；退出记录 `exit≠0` → `incomplete`（即使哨兵存在）；哨兵存在且产物齐备且（退出记录缺失或 `exit=0`）→ `complete`；哨兵存在而产物缺 → `incomplete`；产物齐备而哨兵缺失 → `incomplete`（无正向完成证据；动作裁决见 FR-003）；未配置哨兵时退出记录 `exit=0` 且产物齐备 → `complete`（与 watcher 的 `DONE` 语义一致）；未配置哨兵时退出记录 `exit=0` 而产物缺 → `incomplete`；`commit_required=false` 的阶段不因无提交判 incomplete；无法判定 → `unknown`。`loop_state` 与 `completion` MUST 分离：伪完成只改变 `completion` 与动作建议，MUST NOT 把 watcher 的 `DONE` 改写为 `INCOMPLETE`。
- **FR-008**: 提交证据 MUST 以状态脊的 `stage_base_commit` 为基线，检查基线之后是否有提交触及该阶段产物路径（implement 为代码/测试提交）；基线缺失时 MUST 记 `commit=unknown`，MUST NOT 回退猜测「最近一次提交」；`commit_required=false` 的阶段记 `not-applicable`。`stage_base_commit` MUST 从状态脊机读段读取；其 U2 写入义务属状态脊机读段切片，本切片 MUST 用缺失夹具证明不会猜测。
- **FR-009**: 中断形态 MUST 取自封闭集 `unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable`；每个条目 MUST 至少含 `form`（上述封闭集）、`evidence`（可定位指针数组）、`detail`（一句事实描述）与 `attribution`（`own|stale-run|unattributed|foreign`），MUST NOT 用一个形态掩盖另一个不同根因。切片 A 的形态求值 MUST 遵守以下裁决：[[STR-008]] 只有在 pid 已死且无退出记录且无哨兵时成立；哨兵存在时按 FR-007 的 completion 判定，不得报该形态。`deadline-overrun-live` 只注释，`loop_state` 仍由 FR-004 求值，动作建议 `watch`，MUST NOT 建议杀进程。`heartbeat-stalled` 只注释并保持 `RUNNING`。[[STR-007]] 只注释并驱动 FR-007 的 completion，MUST NOT 直接改 `loop_state`。`stale-signal` 的归属裁决见 FR-002；只有同线 `stale-run` 可驱动 FR-003 的 `retry`，`foreign`/`unattributed` 只进入 `stale_signals[]`。`remote-unreachable` MUST NOT 判 `DEAD` 或阶段失败；`loop_state` 仍由 derived 求值（通常 `UNKNOWN`），建议动作为 `stop` 并携带原因。`lifecycle-spine-violation` 只注释；其中「Registry 存在而状态脊缺失/不可读」的证据缺口 MUST 建议 `stop`，但 MUST NOT 覆盖 watcher/probe 的 `loop_state`。[[STR-003]] 见 FR-011。所有形态 MUST NOT 覆盖 `loop_state`。
- **FR-010**: 驱动者 MUST 在每个 U3 监听窗口开始时原子写/覆盖 watchbeat 标记 [[STR-002]]`<line>-<stage>`（至少含 `run=<run_id> stage=<stage> window=<seconds> at=<epoch> event=watch-window`），窗口返回时刷新 `event=watch-return`；该标记只证明驱动者存在，MUST NOT 参与任何完成/存活判定；`watch-model.md` §5「RUNNING 窗口不写状态脊」保持不变。标记路径 MUST 为 `<state-dir>/`[[STR-002]]`<line>-<stage>`；`state-dir` 解析顺序 MUST 为显式 `--state-dir` → 显式 `--spine` 的父目录 → Registry `spine_path` 的父目录；无法解析时 watchbeat 记 `missing` 且 `recovery_reason=state-dir-unknown`，MUST NOT 扫描全盘或猜测。快照只读消费 watchbeat；标记 MUST 携带 `line=`/`run=`/`stage=` 信封，归属裁决见 FR-002；标记新鲜度 MUST 使用标记自身 `window=` + `effective.deadline_grace`（owner：`scripts/watch-target.sh`；本规格不复述数值；有效值来源见 FR-004）。
- **FR-011**: 阶段仍在运行（pid 存活或心跳新鲜）而 watchbeat 标记缺失，或标记年龄超过其自身 `window=` 字段 + `effective.deadline_grace`（owner：`scripts/watch-target.sh`；本规格不复述数值；有效值来源见 FR-004）时，快照 MUST 报 [[STR-003]] 中断；其恢复方向 MUST 为重新监听，MUST NOT 触发提交、重派或终止。正常窗口到期而 watchbeat 新鲜时 MUST NOT 报该形态。
- **FR-012**: 引擎 MUST 使用统一退出码阶梯：`0` = 求值或应用成功（`snapshot`、`recover` dry-run、`recover --apply` 成功或 `already-applied`、`check-spine` 通过；`recover` 的 `action=stop` 是成功求值，仍为 0）；`1` = 拒绝或校验失败（`check-spine` 违规、`recover --apply` 因路径冲突/未合并变更/非本阶段文件/并发锁被拒绝、或应用过程中失败）；`2` = 参数错误或必需输入不可读。任何 `loop_state` 都是数据，不得编码为退出码；MUST NOT 复用或重定义 watcher 的判定退出码（10–16）。阶梯 MUST 在 `--help` 与 `--self-test` 中钉住。切片 A 的 `--self-test` MUST 覆盖 FR-009 中适用的中断形态，以及旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 状态脊、不可达证据、`registry.status=missing`/`unreadable`/`invalid`、`registry-present-spine-missing`（有/无 watcher 判定两态）、`not-dispatched`、`retry_limit=unknown`/`attempt=unknown`、probe 快照与「形态不覆盖 `loop_state`」、`foreign` 载体不驱动 `retry`；并发锁与 recover 拒绝路径由后续切片追加，不得在本切片伪造通过。

#### Snapshot Field Contract (normative)

字段闭域与类型是测试与下游读取方的契约；未列字段只允许追加。路径形态：产物路径与 `missing_artifacts`/`uncommitted_artifacts` 使用 repo-relative POSIX；状态脊/Registry/载体指针使用绝对路径；提交证据使用 `commit:<sha>`。

| Field | Domain / type | Rule |
|-------|---------------|------|
| `schema_version` | integer `1` | 初始版本；增量字段只追加 |
| `line_id` / `run_id` / `stage` | string or `unknown` | 不可解析记 `unknown`，不猜 |
| `loop_state` | FR-004 closed set | 只由 watcher/probe 逐字判定或 derived 映射产生 |
| `verdict_source` | `watcher` / `derived` | probe 携带 watcher 判定时才为 `watcher` |
| `watch_status` | `available` / `unavailable` | 无 watcher/probe 判定为 `unavailable` |
| `watch_verdict` | watcher verdict or `null` | `watch_status=unavailable` 时为 `null` |
| `completion` | `complete` / `incomplete` / `unknown` / `not-applicable` | FR-007 |
| `recovery_action` | `none` / `watch` / `verify` / `resume` / `retry` / `stop` | FR-003 固定顺序 |
| `recovery_reason` | stable snake-case token | 机器判据；闭集见下方清单 |
| `recovery_detail` | one sentence | 人类可读解释；不参与测试判定 |
| `isolation_required` | boolean | 仅同线 `stale-run` 触发 `retry` 时为 `true` |
| `spine` | object: `path`, `state`, `schema`, `consistent`, `fields` | `state`: `running`/`retrying`/`stalled`/`reentry-required`/`done`/`unknown`; `schema`: `v1`/`legacy`/`missing`/`unreadable`; `consistent`: `true`/`false`/`unknown`; 缺失字段 `unknown` |
| `registry` | object: `status`, `entry`, `pointer`, `error` | `status`: `found`/`missing`/`unreadable`/`invalid` |
| `evidence` | object of signal entries | 每项含 `status`: `present`/`missing`/`na`、`attribution`: `own`/`stale-run`/`unattributed`/`foreign`、`evidence_source`: `local`/`probe`、`pointer` |
| `effective` | object of `{value, source}` | 阈值/重试/attempt/sentinel 的有效值；不可得时 `value=unknown` |
| `salvage` | object: `declared`, `evidence[]`, `source` | `source`: `spine`/`argument`/`none` |
| `interruptions[]` | array of `{form, evidence[], detail, attribution}` | `form` 取 FR-009 闭集；只注释 |
| `missing_artifacts` / `uncommitted_artifacts` | array of repo-relative POSIX paths | 不推断，不补默认 |
| `stale_signals[]` | array of `{pointer, attribution, reason}` | 非 `own` 载体只在此出现 |
| `evaluated_at` | ISO-8601 UTC (`Z`) | 唯一允许在两次同输入间变化的字段 |

`recovery_reason` 的闭集至少含：`not-dispatched`、`evidence-insufficient`、`remote-unreachable`、`lifecycle-spine-violation`、`retry-limit-reached`、`retry-limit-unknown`、`state-dir-unknown`、`stale-signal-unattributable`、`stale-signal-attributed`、`running`、`unwatched`、`deadline-overrun-live`、`complete-verified`、`commit-missing`、`salvage-accepted`、`pseudo-complete`、`no-positive-evidence`、`other`；FR-018 owner 文档可追加但 MUST NOT 重命名既有 token。

#### D/E. 兼容、分发与非目标（适用于切片 A 的边界）

- **FR-013**: `watch-target.sh` 的判定状态机、信号优先级、退出码与 `--self-test` 用例 MUST 保持不变；新增标记与聚合 MUST NOT 改变任何既有判定。切片 A MUST 在契约测试中钉住 watcher 文件的 SHA-256 基线，任何字节改动 MUST 使测试转红；`--self-test` 位于被保护文件内部，不能单独作为回归证据。
- **FR-014**: 四件套文件格式与 `line-registry.py` 的既有 action/字段 MUST 保持兼容；若需增量字段，只允许追加并保证旧条目可读；本特性 MUST NOT 改变 Registry、lease、reservation 或 ownership 语义（owner：Feature 064）。切片 A 只读 Registry，归属裁决 MUST NOT 写回 Registry。
- **FR-015**: 各 `/speckit.*` 命令内部流程、阶段提示词三段骨架、哨兵字面量、确认门与 fast-fail 纪律 MUST 保持不变；本特性只改驱动技能及其测试与文档。切片 A MUST NOT 修改 `watch-model.md` 的判定语义或 `stage-prompts.md` 的状态脊写入时点。
- **FR-016**: 本特性 MUST NOT 引入常驻服务/daemon、外部服务或新的运行时依赖；实现 MUST 复用既有 shell/Python 标准库、watcher、Registry 与 feedback/probe 机制。切片 A 的快照 MUST 在单次调用内完成，MUST NOT 启动后台进程或保活。
- **FR-017**: 两顶帽子：改动 MUST 落在框架源 `skills/external/sdd-loop-driver/`；`.specify/skills/sdd-loop-driver/` 为生成镜像，MUST NOT 手改；镜像 MUST 经 `sync-mirrors.py` 再生成并通过镜像一致性检查；打包随既有 hatch 构建流程，无手工步骤。切片 A 的 spec 目录是需求制品，不是运行时镜像；实现时必须改源再同步镜像。
- **FR-018**: 状态感知/中断/恢复规则 MUST 在技能内有一个唯一 owner 文档（references 下的专门文件或章节），SKILL.md 与各 references MUST 引用而非复述判定表；`references/watch-model.md` 仍是 watch 判定的唯一 owner，本特性 MUST NOT 在其中复制状态恢复规则或改变其语义。切片 A MUST 在 owner 文档中定义：derived 映射、快照字段与归属裁决、completion 与 loop_state 的分离、中断形态的注释语义、`effective` 阈值来源与 `recovery_reason` 闭集；owner 文档 MUST 与 `#### Snapshot Field Contract (normative)` 一致，MUST NOT 复制 watcher 阈值数值；动作执行规则由后续切片在同一 owner 内追加。
- **FR-019**: 文档 MUST 更新：SKILL.md（Hard Requirements 与 References）、owner reference（状态感知、判定表、恢复动作、watchbeat）、`docs/reference/skills/sdd-loop-driver.md`（入口、调用形态、与 watcher/Registry 的关系）；文档取值 MUST 与代码一致。切片 A MUST 更新状态感知/快照/watchbeat 读取部分；恢复动作与生命周期校验章节由后续切片补齐，A MUST NOT 声称它们已实现。
- **FR-020**: 测试 MUST 含变异演练：移除「无 watcher 检测」「旧信号隔离」「salvage 门」任一行为时，至少一条测试 MUST 转红；全部新检查 MUST 有逆样本，MUST NOT 出现只在通过路径上运行的绿。切片 A MUST 执行「无 watcher 检测」「completion 与 loop_state 分离」「中断只注释不覆盖」三项变异；「旧信号隔离」与「salvage 门」的执行动作变异由后续切片承接，但 A MUST 覆盖其只读裁决面（产物齐备无哨兵 → 无 salvage 输入时 `retry`）。
- **FR-021**: 单线与多线 MUST 同构：快照按线独立求值，不引入跨线推断；多线调用 MAY 由调用方逐线循环，本特性 MUST NOT 新增 manifest 或批量判定语义。
- **FR-022**: 任何流程 MUST NOT 自动 push、自动合并、删除分支或改写远端历史；恢复程序的提交仅为本地阶段提交。切片 A 只读，MUST NOT 产生任何提交。
- **FR-023**: 任何流程 MUST NOT 自动 kill 进程、删除日志/信号/worktree 或静默修复证据缺口；清理只能是显式动作，隔离只能是移动。切片 A MUST NOT 执行任何清理或隔离。
- **FR-024**: 本特性 MUST NOT 改变「完成需正证据」原则：哨兵/退出记录仍是完成的正证据，产物齐备只是 U4 证据；唯一有界例外是后续切片的显式 `salvage` 判定，且必须可见与可审计。切片 A MUST 在不声称完成的前提下输出 `completion=incomplete` 与 `retry`/`resume` 候选。
- **FR-025**: 本特性 MUST NOT 替代 Feature 058 的 U4 独立校验、U5 卡死处置或 Feature 064 的 Registry/lease/ownership；它只提供观测与恢复建议，最终去向由驱动者按既有程序裁决。

### Parent FR Mapping

切片 FR 连续编号；下表的父来源使用章节序号。精确的 `#FR-NNN` 映射见 `notes/parent-fr-mapping.md`；除表中注明的切片调整外，正文语义沿用父 FR。

| 切片 FR | 父来源（章节序号） | 切片处理 |
|---------|--------------------|----------|
| FR-001 | 父 A 区第 1 条 | 沿用；A 实现 `snapshot` 与 `--self-test` 快照部分 |
| FR-002 | 父 A 区第 2 条 | 沿用并细化：Registry 对象、载体归属唯一规则、Registry/状态脊缺失路径 |
| FR-003 | 父 A 区第 3 条 | 沿用并细化：新增 `completion`、`registry`、`salvage`、`recovery_reason`；动作建议为只读投影 |
| FR-004 | 父 A 区第 4 条 | 沿用并细化：ANOMALY 谓词、形态不覆盖、stalled/retrying 的 `last_verdict` 放宽 |
| FR-005 | 父 A 区第 5 条 | 沿用；probe 快照作为 watcher 判定来源 |
| FR-006 | 父 A 区第 6 条 | 沿用；A 只消费产物映射 |
| FR-007 | 父 A 区第 7 条 | 沿用并细化：`completion` 求值，伪完成与 `loop_state` 分离 |
| FR-008 | 父 A 区第 8 条 | 沿用；`stage_base_commit` 缺失记 `unknown`，写入义务移交后续切片 |
| FR-009 | 父 A 区第 9 条 | 沿用并细化：`dead-no-exit-record` 要求无哨兵；形态只注释；活 TIMEOUT 只建议 `watch` |
| FR-010 | 父 A 区第 10 条 | 沿用；A 只读消费 watchbeat，归属与新鲜度规则见 FR-002/FR-010 |
| FR-011 | 父 A 区第 11 条 | 沿用；正常窗口不误报 |
| FR-012 | 父 A 区第 12 条 | 沿用；A 的 `--self-test` 覆盖快照适用项，并发锁/拒绝路径由后续切片追加 |
| FR-013 | 父 D 区第 1 条 | 沿用并细化：新增 watcher SHA-256 锚点 |
| FR-014 | 父 D 区第 2 条 | 沿用；A 只读 Registry |
| FR-015 | 父 D 区第 3 条 | 沿用 |
| FR-016 | 父 D 区第 4 条 | 沿用 |
| FR-017 | 父 D 区第 5 条 | 沿用；spec 目录不是运行时镜像 |
| FR-018 | 父 D 区第 6 条 | 沿用；A 的 owner 文档定义状态感知/快照/watchbeat 读取 |
| FR-019 | 父 D 区第 7 条 | 沿用；A 只更新状态感知相关文档，不声称恢复动作已实现 |
| FR-020 | 父 D 区第 9 条 | 沿用；A 执行三项变异并覆盖 salvage 只读裁决面 |
| FR-021 | 父 D 区第 10 条 | 沿用 |
| FR-022 | 父 E 区第 1 条 | 沿用；A 不产生提交 |
| FR-023 | 父 E 区第 2 条 | 沿用；A 不执行清理/隔离 |
| FR-024 | 父 E 区第 3 条 | 沿用；A 输出 `completion=incomplete`，不声称完成 |
| FR-025 | 父 E 区第 4 条 | 沿用 |

### Key Entities *(include if requirement involves data)*

- **Loop State Snapshot（循环状态快照）**: 一次只读求值的结构化结果，聚合状态脊、Registry、四件套、watchbeat、产物、提交与 watcher 判定；含 `loop_state`、`verdict_source`、`completion`、中断清单、缺失/未提交产物与唯一恢复动作建议。它是观测记录，不是新的状态 owner。
- **Interruption Finding（中断条目）**: 封闭形态之一 + 证据指针 + 一句话事实；可多条并存，只作注释，不覆盖 `loop_state`。
- **Recovery Decision（恢复裁决）**: `loop_state` + `completion` + 产物/提交完整性 + 中断形态 + 已试次数 + salvage 输入映射到唯一动作建议（`none/watch/verify/resume/retry/stop`）；A 只求值，不执行。
- **Completion Verdict（完成度判定）**: 独立于 `loop_state` 的 `complete|incomplete|unknown|not-applicable`，只回答正证据与产物齐备性，解决伪完成与 watcher 逐字判定之间的双重绑定。
- **Watchbeat Marker（驱动者监听标记）**: [[STR-002]]`<line>-<stage>` 单行原子覆盖文件；只证明驱动者存在，不参与完成/存活判定。
- **Stage Artifact Map（阶段产物映射）**: 阶段→产物路径/提交要求/允许无变更的唯一映射；与 U4 产物清单对齐。
- **State Spine（状态脊，既有）**: 每线一份的恢复状态文件（owner：Feature 058 的 `stage-prompts.md`）；A 只读取其机读段并报告 schema/一致性，不改变状态词表与写入时点。
- **Watcher Verdict（监听判定，既有）**: 由 `watch-target.sh` 代码侧精确拥有；A 只消费，不重定义。
- **Line Registry（线路登记册，既有）**: 环境级登记集合（owner：Feature 064）；A 只读消费。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 实测事故回放夹具（产物齐备未提交、`exit=1`、无哨兵、无 watcher）中，快照在单次调用内识别出至少一个中断形态并给出 `resume` 或 `retry` 建议，人工逐文件检查次数为 0。
- **SC-002**: 同一输入两次快照除 `evaluated_at` 外差异数为 0；任一缺失信号在输出中以 `missing`/`unknown` 出现，零值或 `ok` 猜测次数为 0。
- **SC-003**: 正常监听窗口被误报为 `unwatched` 的次数为 0；进程已死且无退出记录被误判为 `DONE` 的次数为 0；活进程被建议立即终止的次数为 0。
- **SC-004**: 「哨兵在而产物缺」的夹具中，`loop_state` 被改写的次数为 0，`completion=incomplete` 与 `retry` 建议的正确率为 100%；任一中断形态覆盖 `loop_state` 的次数为 0。
- **SC-005**: 既有 `watch-target.sh --self-test` 通过率为 100%，判定与退出码差异数为 0；watcher SHA-256 锚点生效，字节漂移检出率为 100%；四件套与 Registry 兼容读取测试保持绿色。
- **SC-006**: 源与镜像字节一致率为 100%，镜像漂移数为 0；文档入口已更新；新增 daemon/外部依赖数为 0。
- **SC-007**: 本切片新增检查的逆样本覆盖率为 100%；移除「无 watcher 检测」「completion 与 loop_state 分离」「中断只注释不覆盖」任一行为时，至少 1 条测试转红；具名夹具 `sentinel-with-missing-artifact`、`legacy-spine-snapshot`、`artifacts-without-completion`、`dead-no-exit-record`、`unwatched-vs-window`、`registry-missing`、`registry-present-spine-missing`、`not-dispatched`、`probe-snapshot` 全部存在并通过。
- **SC-008**: 在「产物齐备、无哨兵、无 ANOMALY 行」的夹具中，无 salvage 输入时 `retry` 建议率为 100%；有有效 salvage 输入且非 implement 自动提交场景时，`resume` 候选建议率为 100%；完成且仅缺提交时 `resume`（补提交）建议率为 100%；salvage 门循环依赖导致的错误 `resume` 次数为 0。

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 Source**: `tests/unit/` 与 `tests/contract/` 下的具名快照夹具（构造状态脊、四件套、watchbeat、产物与 git 历史）；逐条断言 `interruptions[]`、`loop_state`、`completion`、`recovery_action` 与字段存在性；事故回放夹具直接使用父 requirements「现状锚点」的事实形态；相同夹具两次运行 diff（剔除 `evaluated_at`）。
- **SC-003 / SC-004 Source**: 正常窗口、进程死无退出记录、TIMEOUT 活进程、哨兵在产物缺四组夹具的断言计数；`loop_state` 改写断言为 0；建议动作断言不得出现 kill/terminate 语义。
- **SC-005 Source**: 既有 `watch-target.sh --self-test` 输出、驱动技能契约测试（`tests/contract/test_sdd_loop_driver_skill.py`）、watcher SHA-256 锚点断言与 `line-registry` 引擎测试。
- **SC-006 Source**: `sync-mirrors.py --check --only skills/external/sdd-loop-driver`、`docs/reference/skills/sdd-loop-driver.md` 存在性与内容断言、依赖清单比对。
- **SC-007 Source**: 变异演练记录：逐项移除行为并运行测试，记录转红用例；具名夹具清单由测试文件枚举。
- **SC-008 Source**: salvage 两态夹具（无输入/有输入）与 implement 场景夹具的动作断言；失败用例名单由测试输出捕获。
- 所有度量都从测试或运行产生的制品读取，不手填；无法测量的量显式记为未评估。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "loop-state.py" | FR-001 |
| `STR-002` | "watchbeat-" | FR-010 |
| `STR-003` | "unwatched" | FR-011, FR-009 |
| `STR-004` | "reentry-required" | FR-004 |
| `STR-005` | "derived" | FR-004, FR-005 |
| `STR-006` | "watcher" | FR-004 |
| `STR-007` | "artifacts-without-completion" | FR-009 |
| `STR-008` | "dead-no-exit-record" | FR-009 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-21 — requirements（无人值守切片）

> 本阶段为无人值守运行，未向用户发起访谈；以下裁决按父 requirements、拆分记录、blocked-review 与入口指令自行作出，已同步落入 Assumptions 与相应 FR。`/speckit.clarify` 可推翻。

- Q: 切片 FR 是否沿用父编号？ → A: 不沿用。切片 FR 连续编号 001–025；父 FR 在 Parent FR Mapping 表以章节序号引用，精确 `#FR-NNN` 映射落在 `notes/parent-fr-mapping.md`；这避免编号空间混淆，同时不删除、不合并、不重排父需求。
- Q: 哪些边界 FR 适用于本切片？ → A: 纳入父 D 区第 1–7、9、10 条与 E 区第 1–4 条；父 D 区第 8 条（跨切片测试矩阵）与第 11 条（记录拓扑 + recover 锁）显式 out-of-slice，由后续切片承接。
- Q: 恢复动作在 A 中如何定义？ → A: A 只做只读求值并输出动作建议，封闭动作集与裁决顺序是父恢复动作规则的只读投影；不执行提交、隔离、重派、停线或任何写操作。
- Q: 父规格中引用了本切片外条目的两条 FR 如何处理？ → A: 改为父 requirements 相应章节的文字指针，避免切片内悬空引用；精确编号只在 `notes/parent-fr-mapping.md` 记录；不删除、不合并、不重排父 FR。
- Q: 兼容性验收是否进入本切片？ → A: 进入。拆分记录要求每个切片运行兼容性验收；本切片以 US2 与 FR-013–FR-019、FR-022–FR-025 承接，并新增 watcher SHA-256 锚点。
- Q: Feature 如何绑定？ → A: Related Feature 保持 `Need clarification`；`/speckit.clarify` MUST 绑定到既有 Feature 065，不新建 Feature ID、不新增注册行。
- Q: blocked-review 的 A 相关 findings 如何吸收？ → A: 逐条落入 SA-6…SA-14 与 FR-002/FR-003/FR-004/FR-007/FR-008/FR-009/FR-013/FR-020；finding 11/12 显式移交恢复执行切片，finding 13/15 标为不适用。
- Q: 伪完成时 `loop_state` 与 `completion` 冲突如何裁决？ → A: 新增独立 `completion` 字段；`loop_state` 保持 watcher 逐字判定，伪完成只改变 `completion` 与动作建议，不把 `DONE` 改写为 `INCOMPLETE`。
- Q: salvage 何时参与裁决？ → A: 在动作裁决之前作为输入参与（状态脊已记录或只读调用提供的证据引用），不是裁决后的覆盖开关；无输入时产物齐备但无哨兵一律 `retry`。
- Q: 多活动线下的 legacy 载体如何处理？ → A: 不启用 legacy 归属模式；无法用信封证明归属的载体进入 `stale_signals[]`，不得作为当前尝试证据。

### Session 2026-10-21 — clarify（无人值守切片）

> 本阶段为无人值守运行，未向用户发起访谈；覆盖扫描由 fresh-context 只读子代理执行（requirements 制品产生于既有会话，本次不满足同作者门触发条件）。以下 5 项裁决按父规格、终态权威文档与既有 owner 边界自行作出，已同步落入 Assumptions 与相应 FR；选项与后果一并记录。`/speckit.clarify` 可推翻。

- Q: Feature 绑定到既有 065 还是新建 066？ → A: 绑定既有 Feature 065（`SDD 循环中断感知与状态恢复`），不新建 Feature ID、不新增注册行、不改变 065 的 Draft 状态；同时更新 `features/065.md` 的 Related Specifications 与 `features.md` 的 Last Updated 备注。候选「新建 066」被拒：拆分记录明确每个切片共享父特性 065，且本切片没有独立于 065 的能力域。此裁决推翻上一会话「保持 Need clarification」的占位决定，旧行保留为历史记录。
- Q: watcher/probe 判定与「Registry 存在而状态脊缺失 → UNKNOWN + stop」冲突时谁优先？ → A: watcher/probe 逐字判定优先；`UNKNOWN + stop` 仅限 `verdict_source=derived` 且无 watcher/probe 判定。存在 watcher/probe 判定时，状态脊缺口以 `lifecycle-spine-violation` + `stop` 建议记录，`loop_state` 不得被改写；阶段信封不可得时 `stage=unknown`。候选「Registry 规则无条件覆盖」被拒：违反 FR-004 与父规格的 watcher 逐字原则。
- Q: 「未派发」如何确定性判定，启动宽限期以何为锚？ → A: 未派发 = 无任何派发证据（状态脊既无可读机读段也无可读 legacy 阶段/断点记录，或两者均缺少 `stage_started_at`/`stage_deadline_epoch`、Registry 条目无 `stage`/`run_id` 绑定、无可归属载体与 watcher/probe 判定）；注册本身不算派发，legacy 状态脊中的可读阶段/断点记录算派发证据。Registry 存在而状态脊缺失的路径优先于未派发判定。未派发优先于 derived 的 `DEAD`/`NO_SIGNAL`/`RUNNING` 规则，输出 `UNKNOWN` + `recovery_reason=not-dispatched` + `completion=not-applicable` + 动作 `none`。启动宽限期锚定 `stage_started_at`，缺失时取最早可归属载体 mtime，不得用快照调用时刻。候选「按 watcher 调用时刻计时」被拒：A 不是 watcher，无法复现其 invocation 时点。
- Q: 快照的阈值、重试上限、attempt、哨兵配置、probe schema、watchbeat 路径与 salvage 输入如何冻结？ → A: 有效值按「显式 CLI 参数 → probe 的 `effective` → 状态脊机读段 → 阶段产物映射哨兵配置 → watcher `--help` 缺省值」解析，并在 `effective` 逐项标注来源；任一来源不可得时依赖该值的判定记 `UNKNOWN`/`value=unknown`，不得硬编码或把缺失当 0。`--probe` 复用 `snapshot` 的同一 `schema_version`，不引入私有格式；probe 带 watcher 判定才逐字采用，否则本地按 derived 重新求值。watchbeat 路径冻结为 `<state-dir>/watchbeat-<line>-<stage>`，`state-dir` 按显式参数 → 显式 spine 父目录 → Registry `spine_path` 父目录解析。salvage 只读输入冻结为 `--salvage-evidence <ref>`（可重复，不写状态脊），与状态脊 `salvage: accepted` 记录二选一。候选「全部沿用默认值、不提供输入」被拒：stage-prompts 明确超时/重试默认可被入口参数覆盖，沿用默认会把 override 运行判错。
- Q: 输出字段闭域、stale 归属对动作的影响与路径形态如何冻结？ → A: 以 `#### Snapshot Field Contract (normative)` 为准：`watch_status` 取 `available|unavailable`、`watch_verdict` 不可用时为 `null`、`registry.status` 取 `found|missing|unreadable|invalid`、`spine.schema` 取 `v1|legacy|missing|unreadable`、`spine.consistent` 三态、`evidence.*.status` 取 `present|missing|na`、`attribution` 取 `own|stale-run|unattributed|foreign`；`recovery_reason` 用稳定 token，人类解释放 `recovery_detail`，`isolation_required` 进入契约。只有同线 `stale-run` 可驱动 `retry`；`foreign`/`unattributed` 只报告、不改变动作。产物路径用 repo-relative POSIX，载体/状态脊/Registry 指针用绝对路径，提交用 `commit:<sha>`，`evaluated_at` 用 ISO-8601 UTC。候选「继续用自由文本字段/让 foreign 参与动作」被拒：前者无法测试，后者违反单线独立求值（FR-021）。

- 就地修正（非裁决，属于术语与一致性归一）：`reason=not-dispatched` → `recovery_reason=not-dispatched`；`watch=unavailable` → `watch_status=unavailable` + `watch_verdict=null`；`spine_consistent` → `spine.consistent`（true/false/unknown）；`registry=missing` 统一写 `registry.status=missing`；`isolation_required` 与 `recovery_detail` 补入 FR-003 输出契约。
