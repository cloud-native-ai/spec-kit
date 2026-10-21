# Requirements Specification: SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）

**Requirement Branch**: `065-loop-interruption-recovery`  
**Created**: 2026-10-21  
**Status**: Draft  
**Input**: User description: "Feature 065 — 在无人值守 SDD 循环中，针对流程中断提供确定性的状态感知与状态恢复：新增只读状态聚合入口（状态脊 + 四件套 + spec 产物 + git 提交 + watcher 判定），识别中断形态并给出 stalled/reentry-required 落脊建议；提供按判定执行 resume/retry/stop 的续跑程序（补提交、隔离旧信号、生成上送件），并把驱动者生命周期约束（派发与监听同回合、退出前落脊）固化为可校验规则。需求语义权威：`/Users/liuqiming.lqm/project/profiles/data/projects/04_知识管理/tmp/sdd-loop-speckit-065/brief-065.md`，已逐字归档为 dated record：[notes/source-requirement.md](notes/source-requirement.md)（2026-10-21 快照）；原路径仅保留为 provenance 注记，不再作为权威引用。"

## Related Feature *(mandatory)*

**Feature ID**: 065（2026-10-21 由 `/speckit.clarify` 新建并绑定；注册状态 Draft）
**Feature Name**: SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）

**Related features**:

- **058 — 无人值守 SDD 循环驱动机制（Implemented）**: 拥有 U0–U6 循环、每线状态脊、阶段哨兵、U4 独立校验、U5 卡死处置与 `watch-target.sh` 判定状态机。065 只在其上增加观测与恢复层，引用而不重定义这些语义。
- **064 — Subagent 并发归属、CLI 能力档案与生命周期解耦（Implemented）**: 拥有环境级 Line Registry、归属信封、lease/reservation/ownership 与重接线协议。065 读取 Registry 作为证据来源，不改变其任何状态机或 action 语义。
- **063 — SDD 循环效率优化（Implemented）**: 拥有 fast lane、两槽位测试预算、plan 只小修约束与 stream-json/脱离形态。065 只读取其产物（plan-owned 设计件、阶段基线提交），不改写其规则。

## 现状锚点（2026-10-21 以 master `5e5cd0d8` 实测为准；dated record，仅作可行性输入，非运行时保证）

- **实测事故（xuanji-doc 线 015）**: plan 阶段派发后驱动者未在同一回合启动 watcher；Mac 休眠导致会话挂起；实际写盘发生在 15:30–16:04，已越过 90 分钟阶段 deadline，但因无 watcher 未产生 `TIMEOUT` 判定；16:04:51 qodercli 以 `exit=1` 退出且无哨兵，`plan/data-model/contracts/quickstart/research/feature-ref` 产物齐全但未提交；循环静默停摆约 13 小时。恢复只能人工逐一检查 pid/status/log/heartbeat/产物与 git 提交。
- **监听模型**: `references/watch-model.md` 拥有四类信号（哨兵/退出记录/PID+start ticks/心跳）、判定状态机与退出码（`ANOMALY/FAILED/INCOMPLETE/DEAD/TIMEOUT/NO_SIGNAL/DONE/RUNNING`）、窗口 vs deadline、`--once` 快照与 `--deadline-grace` 语义；`scripts/watch-target.sh` 是代码侧精确值 owner，且监听只读、不写项目状态。
- **状态脊**: `references/stage-prompts.md` § Stall Handling & State Spine 拥有字段与写入时点（U0 入口、U2 派发前、U3 终止判定、U4 校验后、U5 停线时先写后动），并要求驱动者提前结束时写 `stalled` / `reentry-required`；但状态脊是散文式 markdown，没有机器可读段、没有确定性校验器。
- **既有聚合能力**: `scripts/line-registry.py --action reattach-brief` 已聚合 Registry 条目、状态脊（仅 `state` 与最后一行）、四件套存在性、heartbeat 年龄、reservation 与 lease；它不聚合阶段产物、git 提交、watchbeat 或 watcher 判定，也不产出恢复动作。
- **缺口**: 没有面向驱动者的统一「状态感知」入口；没有确定性「中断检测」；没有自动化「状态恢复」程序；没有 watchbeat 之类的驱动者存在证据；没有「派发与监听同回合启动」的可校验规则。
- **分发面**: 源为 `skills/external/sdd-loop-driver/`，运行时镜像为 `.specify/skills/sdd-loop-driver/`（由 `scripts/python/sync-mirrors.py` 生成，禁止手改）；文档入口为 `docs/reference/skills/sdd-loop-driver.md`；契约测试 `tests/contract/test_sdd_loop_driver_skill.py` 钉住 SKILL.md 章节集合与镜像字节一致。
- **命名面**: 仓库内当前不存在 `loop-state.py`、`watchbeat-*` 或状态恢复相关 reference；新增名称不冲突。

## Assumptions（对输入中开放点的裁决记录；2026-10-21 `/speckit.clarify` 已复核：修正 A-1/A-15，新增 A-16…A-19，其余维持）

- **A-1 入口形态**: 新建单一引擎 `loop-state.py`（Python 3 标准库）承载 `snapshot`（只读）、`recover`（默认 dry-run、`--apply` 才变更）与 `check-spine`（只读校验）三个动作，外加 `--self-test`，而不是继续扩充 `line-registry.py`。理由：line-registry 的领域是登记/归属/lease，已近 100 KB；状态感知需要读 spec 产物与 git，且必须保持只读，独立入口更容易被测试与约束。两者共享 Registry/状态脊证据，但不互相替代。
- **A-2 判定所有权**: watch 域判定仍由 `watch-target.sh` 唯一拥有。`loop-state.py` 只调用 `--once` 或消费调用方提供的 WATCH 快照，绝不重新实现信号优先级与退出码；`loop_state` 在存在活动 target 时逐字等于 watcher 判定。
- **A-3 两套词表分离**: `loop_state`（快照输出的聚合判定，大写）与 `spine_state`（状态脊文件状态，小写连字符）是两个词表，各自有 owner，不互相替代；快照显式报告二者及 `spine_consistent`。
- **A-4 第五信号 watchbeat**: 为检测「已派发但无 watcher」，新增由驱动者写入的 watchbeat 标记（`watchbeat-<line>-<stage>`），每窗口开始/返回各一次原子覆盖。它是驱动者存在证据，不是完成/存活信号，不参与任何 watch 判定；状态脊仍遵守「RUNNING 窗口不写」的既有规则。
- **A-5 动作集合**: 恢复动作取封闭集 `none / watch / verify / resume / retry / stop`。在输入建议的 `resume / retry / stop` 之外增加 `watch`（继续监听，不重派）、`verify`（进入 U4 独立校验）、`none`（未派发或不适用），以避免把「活着但没人监听」「已完成待校验」误映射到 mutating 动作。
- **A-6 salvage 有界例外**: 产物齐备但无正向终止证据（无哨兵、非 `exit=0`）时，`resume` 必须由驱动者显式记录 `salvage` 判定（依据 = 产物清单 + 无 `ANOMALY:` 行 + U4 产物/纪律核验）才允许提交；未记录时一律 `retry`。该例外必须出现在 U4 结论与收尾汇总中，不得静默放行。
- **A-7 implement 排除自动提交**: 恢复程序不对 implement 阶段自动提交代码路径；implement 只在「工作已提交、仅缺状态推进」时 `resume`，否则 `retry`。
- **A-8 隔离而非删除**: 旧 status/pid/heartbeat/hook/watchbeat 一律原子移动到 `attempts/` 下的隔离目录，永不删除或就地清空；无信封的 legacy 文件按可疑处理（doubtful-strict），同样隔离。
- **A-9 先写后动与幂等**: 恢复动作先写状态脊恢复记录再执行副作用；每个动作幂等，重复执行返回 `already-applied` 且不产生第二次提交/隔离/计数漂移。
- **A-10 停线不杀进程**: `stop` 只写 `stalled` 与四要素上送件，不 kill、不删 worktree；活进程的 TIMEOUT 停线必须先做最终 `--once` 快照并经用户显式决定。
- **A-11 状态脊机读段**: 状态脊增加固定 fencing 内的 `key: value` 机读段；散文部分不变。legacy 状态脊（无可读段）降级求值，缺字段记 `unknown`，不猜测、不补默认值。
- **A-12 产物映射 owner**: 阶段→产物映射由脚本内数据 + 对应 reference 章节唯一定义，并与 U4 的产物核验清单对齐；plan 阶段使用 `efficiency-model.md` §3 的 plan-owned 集合；analyze 无提交要求，clarify 允许无变更。
- **A-13 远端拓扑**: 聚合器在证据所在主机以同一执行身份运行，或消费调用方经 ssh 采集的 probe 快照；ssh 不可达记 `stalled(remote-unreachable)`，绝不记 `DEAD`。
- **A-14 未派发语义**: 尚未派发的线不在本特性判定范围内；快照以 `UNKNOWN` + `reason=not-dispatched` 表达，恢复动作为 `none`。
- **A-15 Feature 绑定**: 入口已声明特性 ID 065；2026-10-21 `/speckit.clarify` 已新建并绑定 Feature 065（Draft），注册行与 `.specify/memory/features/065.md` 同批落盘；不另开新 ID。
- **A-16 derived 映射**: 无活动 watcher 时，`loop_state` 由独立、固定优先级的聚合映射表导出，始终标注 `verdict_source=derived`；它不是 watcher 判定状态机的复制，不得声称具有 watcher 判定的语义或退出码。映射与状态脊 `last_verdict` 冲突时只报 `spine_consistent=false`，不静默择一。
- **A-17 引擎 CLI 契约**: 三个动作共享同一 JSON 信封（含 `schema_version`）与退出码阶梯 `0/1/2`；`recover` 仅在 `resume/retry/stop` 且 `--apply` 时写状态脊恢复记录，`watch` 只刷新 watchbeat，`verify/none` 不写任何状态；远端 probe 快照经 `--probe <file>` 输入。
- **A-18 状态脊机读段**: 使用独立 fence `<!-- loop-state:begin -->` … `<!-- loop-state:end -->` 与 `spine_schema: v1`；状态键使用 `spine_state:` 前缀，MUST NOT 使用裸 `state:` 键，以避免改变 `line-registry.py` 对首个 `state[:=]` 行的既有读取；状态枚举扩展为 `running / retrying / stalled / reentry-required / done`。
- **A-19 并发恢复锁**: `recover --apply` 对同一线持有独立原子锁；第二个写者等待有界时间后返回 `result=locked`（exit 1），不自动清理疑似 stale lock；显式 `--break-lock` 才把旧锁移动至 `attempts/` 隔离并继续，绝不删除。

## 跨特性重叠与边界（record for analyze/plan；不构成第二 owner）

- **与 058（sdd-loop-driver）**: U0–U6、状态脊、哨兵、U4/U5、watcher 判定与退出码仍归 058 的既有制品与代码。065 只增加观测、恢复与生命周期校验，不改变 watcher 判定、不改变阶段命令内部流程。
- **与 064（subagent-concurrency）**: Registry、lease、reservation、ownership 与重接线语义归 064。065 只读 Registry 作为证据来源；新增字段（若需要）只能是追加且可被旧版本忽略。
- **与 063（sdd-loop-efficiency）**: fast lane、test budget、plan constraint 与 stream-json 归 063。065 只消费 plan-owned 产物列表与阶段基线提交，不复述其阈值。
- **与 feedback/probe**: 065 的恢复与中断事件不新增记录引擎；如需反馈，经既有 `feedback-utils.py` / probe 注册表按既有形态记录。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次调用看清一条线的真实状态 (Priority: P1)

使用者或新接手的驱动会话面对一条可能中断的线，不再逐一检查 pid/status/log/heartbeat/产物与 git 提交。只需按线调用一个确定性入口，即可得到：当前阶段与断点、状态脊状态、四件套证据、产物与提交完整性、watcher 最近判定、识别出的中断形态，以及唯一建议的下一步动作。所有缺失信号显式标为 `missing`/`unknown`，不猜测。

**Why this priority**: 这是「状态感知」的最小可用价值，也是恢复与生命周期治理的共同前提；实测事故中恢复耗时几乎全部花在人工拼装这些证据上。

**Independent Test**: 用夹具构造一条「产物齐备、未提交、`exit=1`、无哨兵、无 watcher」的线，调用快照入口，核对输出字段、证据指针与建议动作；再构造一条正常运行中的线与一条未派发的线，核对三者的 `loop_state` 与 `verdict_source` 差异。

**Acceptance Scenarios**:

1. **Given** 一条线的状态脊与四件套可读、watcher 可调用，**When** 执行一次快照，**Then** 输出包含阶段、`loop_state`、`verdict_source`、`watch_verdict`、产物/提交清单、`interruptions[]` 与唯一 `recovery_action`，且所有路径可定位。
2. **Given** 阶段运行中且刚完成一个监听窗口，**When** 执行快照，**Then** `loop_state=RUNNING`、`verdict_source=watcher`，且不报 `unwatched`。
3. **Given** 阶段运行中但驱动者从未启动 watcher（无 watchbeat），**When** 执行快照，**Then** 报 `unwatched` 中断并建议 `watch`，不提交、不重派。
4. **Given** 阶段产物齐备但无哨兵且未提交，**When** 执行快照，**Then** 报 `artifacts-without-completion`，不得判 `DONE`，建议动作遵循 salvage 门。
5. **Given** 任一信号缺失，**When** 执行快照，**Then** 该信号以 `missing`/`unknown` 出现，输出中不出现零值或 `ok` 猜测。

---

### User Story 2 - 中断形态被识别并给出落脊建议 (Priority: P1)

驱动者或恢复者能在不读日志正文的前提下，区分「无 watcher」「进程死且无退出记录」「deadline 已过但进程仍活」「心跳停跳」「产物齐备但无完成声明」「旧信号污染」「驱动者退出未落脊」「远端不可达」八类中断。每类都带证据指针与建议的状态脊写入（`stalled` 或 `reentry-required`），且不会把活着的进程误判为可终止。

**Why this priority**: 误判中断形态会直接导致错误处置——重派已完成阶段、杀掉仍在工作的进程、或把旧 status 当成本次证据。实测中旧 status 污染已造成过一次误判。

**Independent Test**: 对八类中断各构造一个夹具，逐一调用快照，核对 `interruptions[]` 的形态、证据与建议；另构造「监听窗口到期（RUNNING）」夹具，验证它不被误报为中断。

**Acceptance Scenarios**:

1. **Given** 进程已死且无退出记录，**When** 执行快照，**Then** 形态为 `dead-no-exit-record`，`loop_state=DEAD`，不判完成。
2. **Given** deadline 已过但 pid 与心跳均新鲜，**When** 执行快照，**Then** 形态为 `deadline-overrun-live`，建议 `watch`，不得建议杀进程或立即停线。
3. **Given** pid 记录存在而心跳早于约定最大年龄，**When** 执行快照，**Then** 报 `heartbeat-stalled` 警告，`loop_state` 保持 `RUNNING`。
4. **Given** status 文件来自上一次尝试（`run_id` 不符），**When** 执行快照，**Then** 它进入 `stale_signals[]`，不被当作本次证据。
5. **Given** 状态脊 `state=running` 但无存活进程、无 watchbeat 且无终态证据，**When** 执行快照，**Then** 报 `lifecycle-spine-violation` 并建议写 `stalled`/`reentry-required`。
6. **Given** 远端 ssh 不可达，**When** 执行快照，**Then** 报 `remote-unreachable` 并建议 `stalled(remote-unreachable)`，不得判 `DEAD`。

---

### User Story 3 - 恢复程序按判定执行 resume / retry / stop (Priority: P1)

面对中断的线，恢复者得到一个确定性动作而不是自行发挥：已完成但未提交的阶段补提交后进入独立校验，不重派；失败或证据不足的阶段在隔离旧信号后重试；达到上限或无法判定时停线并生成四要素上送件。所有变更默认 dry-run，只有显式 `--apply` 才落地，且重复执行保持幂等。

**Why this priority**: 这是用户目标的另一半——不仅要知道发生了什么，还要能以最小代价安全续跑；错误的自动提交或误删证据会放大事故。

**Independent Test**: 对「产物齐备未提交」「哨兵在产物缺」「旧 status 污染」「达到重试上限」「活进程 TIMEOUT」五类夹具分别执行恢复；核对动作、提交路径集合、隔离目录、计数与上送件四要素。

**Acceptance Scenarios**:

1. **Given** 阶段产物齐备且仅缺提交，**When** 执行 `resume --apply`，**Then** 只提交该阶段产物路径，提交消息含中断来源，阶段不被重派，控制权交回 U4。
2. **Given** 无正向终止证据但产物齐备，**When** 未记录 `salvage` 判定，**Then** 动作为 `retry`；记录判定后才允许 `resume`，且该例外在 U4 结论中可见。
3. **Given** 旧 status/pid 污染存在，**When** 执行 `retry --apply`，**Then** 旧信号被移动到隔离目录、删除数为 0、已试次数递增一次、下一次派发看到干净信号面。
4. **Given** 已试次数达到既有上限，**When** 执行恢复，**Then** 动作为 `stop`，生成四要素上送件，不杀进程、不删 worktree。
5. **Given** 未提供 `--apply`，**When** 执行任何恢复动作，**Then** 不发生写、提交或移动，输出仍给出完整判定与将执行的步骤。
6. **Given** 同一动作已执行成功，**When** 再次执行，**Then** 返回 `already-applied`，无第二次提交/隔离/计数漂移。

---

### User Story 4 - 驱动者生命周期约束可校验 (Priority: P2)

驱动者加载技能后，能读到两条硬性生命周期规则：派发与首个监听窗口必须在同一回合启动；确须结束会话前必须把状态脊写为 `stalled`/`reentry-required`。同时，状态脊有确定性校验器，派发前与停线前各跑一次；缺字段或取值非法会直接失败，而不是留到下一次事故才发现。

**Why this priority**: 这些规则已以散文形式存在，但缺少可执行检查；实测事故正是规则存在却无人执行的典型。

**Independent Test**: 构造合法/非法状态脊各一组，运行校验器；在派发前与停线前各注入一次缺失字段，核对失败与清单。

**Acceptance Scenarios**:

1. **Given** 状态脊缺 `stage_deadline_epoch` 或四件套路径，**When** 运行校验，**Then** 非零退出并列出缺失字段。
2. **Given** 状态脊 `state=stalled` 但缺 `stall_reason`/证据指针，**When** 运行校验，**Then** 判定失败。
3. **Given** 状态脊状态与最近 watcher 判定矛盾，**When** 运行校验，**Then** 报告矛盾并给出两处取值。
4. **Given** 合法状态脊，**When** 运行校验，**Then** 退出码 0，无 false positive。
5. **Given** SKILL.md 被加载，**When** 阅读 Hard Requirements，**Then** 两条生命周期规则逐字可见，并指向确定性校验入口。

---

### User Story 5 - 既有语义与分发面不回归 (Priority: P2)

使用者在升级后，现有 watcher 判定、四件套格式、Line Registry、阶段命令、确认门与 fast-fail 纪律保持原样；新增能力仅以增量层出现。框架源、运行时镜像、文档与测试保持一致，没有新增常驻服务或外部依赖。

**Why this priority**: 该特性改善的是「出事后的恢复」，若以改变判定语义或引入新运行时为代价，风险大于收益。

**Independent Test**: 运行既有 watcher `--self-test`、驱动技能契约测试、Registry 引擎测试与镜像一致性检查；对比升级前后的判定输出与退出码。

**Acceptance Scenarios**:

1. **Given** 既有 `watch-target.sh --self-test`，**When** 升级后运行，**Then** 全部用例保持绿色，判定与退出码零差异。
2. **Given** 既有四件套与 Registry 条目，**When** 升级后读取，**Then** 字段语义与 action 行为不变，旧条目可读。
3. **Given** 框架源改动，**When** 运行镜像同步与一致性检查，**Then** 运行时镜像字节一致，漂移为 0。
4. **Given** 既有 `/speckit.*` 命令与阶段提示词，**When** 升级后运行，**Then** 三段骨架、哨兵字面量、确认门与 no-push 策略不变。

---

### Edge Cases

- 驱动者派发后在**同一回合**启动 watcher，但 watcher 第一次调用即超时：watchbeat 存在且新鲜，不得报 `unwatched`；按调用失败处理，重入新窗口。
- 监听窗口正常到期（`RUNNING`）与「无 watcher」同时看似成立：以 watchbeat 是否新鲜区分；新鲜 = 正常窗口，不报中断。
- 阶段已写出哨兵但进程仍活：watcher 可判 `DONE`；快照 `loop_state=DONE`，动作 `verify`，不因进程存活改判。
- 哨兵在而产物缺：伪完成，动作 `retry`，不得 `resume`。
- 产物齐备、无哨兵、但日志最后一行是 `ANOMALY:`：不满足 salvage 前提，动作 `retry`。
- 产物齐备、无哨兵、`exit=1`、无异常行：salvage 候选；未记录独立校验前动作仍为 `retry`。
- 旧 status 的 `run_id` 与当前一致但 mtime 早于 `stage_started_at`：按 stale 处理并隔离。
- 旧 status 无信封且无法判断归属：按可疑处理并隔离，记录 `legacy-stale` 原因。
- `pid` 文件指向已复用 PID：start ticks 不符，判 `DEAD`/身份不符，不附着。
- deadline 已过、pid 活、心跳新鲜、且 status 尚未出现：建议 `watch` 并延长观察；只有用户显式决定才 `stop`。
- deadline 已过、pid 死、无 status：最终快照后按 `retry` 或 `stop`（取决于已试次数）。
- 状态脊是 legacy 格式（无机读段）：降级求值，缺失字段为 `unknown`；不得据默认值建议 `resume`。
- Registry 条目缺失但状态脊与四件套可读：继续求值并记 `registry=missing`；不得因此判 `UNKNOWN`。
- Registry 条目存在但状态脊缺失：`UNKNOWN` + `stop`，上送证据缺口；不得凭 Registry 单独猜阶段。
- 远端 ssh 不可达：`stalled(remote-unreachable)`，重试连通性；不得判 `DEAD`，不得重派。
- 两条线并发执行恢复：各自写各线路径，互不覆盖；同一线并发恢复由 FR-048 的独立锁串行化，后者返回 `locked`（exit 1），不得返回 `already-applied` 来掩盖并发写。
- `resume` 时工作树存在非本阶段脏文件：只提交本阶段产物路径；脏文件保持原状，绝不 `git add -A`。
- `resume` 时产物路径存在未合并冲突：显式拒绝并上送，不部分提交。
- `retry --apply` 时隔离目录已存在同名尝试：使用下一序号，不覆盖既有隔离证据。
- `stop` 时 worktree 有未提交工作：保留 worktree 与证据，上送件中逐项可定位。
- 同一次派发内出现多个中断形态（如 `unwatched` + `stale-signal`）：全部列出，动作按 FR-026 的优先级裁决，不以一条掩盖另一条。
- 快照运行期间 watcher 恰好结束：以 `--once` 的当次输出为准；不得混用两次调用的证据。
- 状态脊与快照同时写入：快照只读，不竞争；恢复写脊遵循单写者与原子替换。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 状态感知（State Awareness）

- **FR-001**: 驱动技能 MUST 提供一个确定性、只读的状态聚合入口 [[STR-001]]（Python 3 标准库、零外部依赖），一次调用聚合状态脊、Line Registry 条目、pid/status/log/heartbeat 四件套、watchbeat 标记、阶段产物、git 提交与可用的 watcher 判定；快照动作 MUST NOT 写文件、改状态、杀进程或修改工作树（显式 `--out` 持久化除外）。
- **FR-002**: 入口的输入解析顺序 MUST 为：显式 `--spine`/`--state-dir`/`--spec-dir`/`--repo`/`--probe` 覆盖 → 按 `--line-id` 读取 Registry 条目 → 失败。`--probe <file>` 是调用方经 ssh 采集的只读 WATCH/probe JSON 快照；显式提供时以它为准并在输出标注 `evidence_source=probe`。Registry 缺失但状态脊与四件套可解析时 MUST 继续求值并记 `registry=missing`；任何必需输入缺失 MUST 显式记为 `missing`，MUST NOT 以零值或猜测填充。
- **FR-003**: 快照输出 MUST 为机器可读 JSON，至少含：`schema_version`（初始值 `1`）、`line_id`、`run_id`、`stage`、`loop_state`、`verdict_source`、`watch_verdict`、`recovery_action`、`spine`（path/state/schema/consistent）、`evidence`（pid/status/log/heartbeat/watchbeat/artifacts/commits，含 `evidence_source=local|probe`）、`interruptions`、`missing_artifacts`、`uncommitted_artifacts`、`stale_signals`、`evaluated_at`；每个信号 MUST 标注 `present|missing|na` 及证据指针。`recover` 输出 MUST 复用同一 `schema_version` 信封，并至少含 `action`、`applied`（bool）、`result`（`dry-run|applied|already-applied|locked|refused|failed`）、`steps[]`、`reason`；增量字段只允许追加，旧读取方 MUST 可忽略未知字段。
- **FR-004**: `loop_state` MUST 取自封闭集 `RUNNING / DONE / INCOMPLETE / ANOMALY / FAILED / DEAD / TIMEOUT / NO_SIGNAL / STALLED / REENTRY_REQUIRED / UNKNOWN`。存在活动 watch target 时，`loop_state` MUST 与 watcher 判定逐字一致且 `verdict_source=watcher`，聚合器 MUST NOT 改写、降级或升级该判定。无 watch target 时以 `verdict_source=derived` 按下列固定优先级推导，且 MUST NOT 复制或声称 watcher 判定：(1) 状态脊 `spine_state=stalled` → `STALLED`，[[STR-004]] → `REENTRY_REQUIRED`；(2) 若（退出记录存在或进程已死）且日志最后非空行以 `ANOMALY:` 开头 → `ANOMALY`，否则退出记录 `exit≠0` → `FAILED`，否则退出记录 `exit=0` 且哨兵存在且产物齐备 → `DONE`，否则退出记录 `exit=0` 且（哨兵缺失或产物缺）→ `INCOMPLETE`；(3) 无退出记录但哨兵存在：产物齐备 → `DONE`，产物缺 → `INCOMPLETE`；(4) 无退出记录、pid 记录存在且进程已死/start ticks 不符 → `DEAD`；(5) 有 `stage_deadline_epoch` 且 now ≥ deadline + deadline grace 且无终态 → `TIMEOUT`（活进程也判 `TIMEOUT`，处置仍按 FR-015 继续观察）；(6) pid 记录与退出记录均缺失且超过启动宽限期 → `NO_SIGNAL`；(7) pid 存活或心跳新鲜且未命中上述终态 → `RUNNING`；(8) 其余 → `UNKNOWN`。启动宽限期、deadline grace 与心跳新鲜度均由 watcher 参数/标记 owner 定义（`scripts/watch-target.sh`；本规格不复述数值）。derived 映射的证据谓词与 watcher 同名判定保持一致，但它是独立的聚合映射，不产生 watcher 的退出码；与状态脊 `last_verdict` 冲突时 MUST 报 `spine_consistent=false`，不得静默择一。映射表由 FR-043 的唯一 owner 文档定义，代码与测试引用它。
- **FR-005**: 监听域判定 MUST 经既有 `watch-target.sh --once`（与 runner 同一执行身份）取得，或消费调用方提供的 WATCH 快照；聚合器 MUST NOT 重新定义或声称 watcher 的判定状态机、信号优先级或退出码。watcher 不可用（ssh 255、宿主工具超时、脚本缺失）时 MUST 记为 `watch=unavailable`，并且只能走 FR-004 的 derived 映射（标注 `verdict_source=derived`），MUST NOT 判为阶段失败、`DEAD` 或伪造 watcher 判定。
- **FR-006**: 阶段产物映射 MUST 由单一 owner（脚本内数据 + 对应 reference 章节）定义，覆盖 `requirements / clarify / plan / tasks / checklist / analyze / implement / review`，每阶段显式标注 `commit_required` 与 `no_change_allowed`；映射 MUST 至少覆盖 U4 的产物核验清单（owner：`references/stage-prompts.md` § Independent Verification），plan 阶段另须覆盖其 plan-owned 设计件集合（owner：`references/efficiency-model.md` §3），analyze `commit_required=false`，clarify `no_change_allowed=true`。
- **FR-007**: 产物完整性 MUST 只由「文件存在且非空」判定，MUST NOT 从日志文本推断；哨兵仍是唯一的完成声明；「哨兵在而产物缺」MUST 判为伪完成（`INCOMPLETE` 语义），MUST NOT 因产物部分存在而判 `DONE`。
- **FR-008**: 提交证据 MUST 以状态脊的 `stage_base_commit` 为基线，检查基线之后是否有提交触及该阶段产物路径（implement 为代码/测试提交）；基线缺失时 MUST 记 `commit=unknown`，MUST NOT 回退猜测「最近一次提交」；`commit_required=false` 的阶段记 `not-applicable`。
- **FR-009**: 中断形态 MUST 取自封闭集 `unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable`；每个条目 MUST 携带证据指针与一句事实描述，MUST NOT 用一个形态掩盖另一个不同根因。
- **FR-010**: 驱动者 MUST 在每个 U3 监听窗口开始时原子写/覆盖 watchbeat 标记 [[STR-002]]`<line>-<stage>`（至少含 `run=<run_id> stage=<stage> window=<seconds> at=<epoch> event=watch-window`），窗口返回时刷新 `event=watch-return`；该标记只证明驱动者存在，MUST NOT 参与任何完成/存活判定；`watch-model.md` §5「RUNNING 窗口不写状态脊」保持不变。
- **FR-011**: 阶段仍在运行（pid 存活或心跳新鲜）而 watchbeat 标记缺失，或标记年龄超过其自身 `window=` 字段 + watcher `--deadline-grace` 缺省值（owner：`scripts/watch-target.sh`；本规格不复述数值）时，快照 MUST 报 [[STR-003]] 中断；其恢复方向 MUST 为重新监听，MUST NOT 触发提交、重派或终止。
- **FR-012**: 引擎 MUST 使用统一退出码阶梯：`0` = 求值或应用成功（`snapshot`、`recover` dry-run、`recover --apply` 成功或 `already-applied`、`check-spine` 通过；`recover` 的 `action=stop` 是成功求值，仍为 0）；`1` = 拒绝或校验失败（`check-spine` 违规、`recover --apply` 因路径冲突/未合并变更/非本阶段文件/并发锁被拒绝、或应用过程中失败）；`2` = 参数错误或必需输入不可读。任何 `loop_state` 都是数据，不得编码为退出码；MUST NOT 复用或重定义 watcher 的判定退出码（10–16）。阶梯 MUST 在 `--help` 与 `--self-test` 中钉住。`--self-test` MUST 覆盖 FR-009 全部中断形态，以及旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 状态脊、不可达证据、并发锁与拒绝路径。

#### B. 中断检测与驱动者生命周期

- **FR-013**: 系统 MUST 能识别「已派发但无 watcher」：阶段运行中、存在存活证据且无新鲜 watchbeat；并 MUST 与「监听窗口正常到期（`RUNNING`）」区分——后者有新鲜 watchbeat。该判定 MUST 只使用文件证据，MUST NOT 使用 `ps`/`pgrep` 扫描。
- **FR-014**: 进程已死且无退出记录 MUST 判为 `DEAD`（形态 `dead-no-exit-record`），MUST NOT 判为完成；有退出记录时以记录为准；有哨兵时按 FR-007 进入伪完成判定。
- **FR-015**: 阶段 deadline 已过而进程仍存活时，快照 MUST 报 `TIMEOUT` + `deadline-overrun-live`；恢复方向 MUST 为继续观察，MUST NOT 建议杀进程；停线只允许在最终 `--once` 快照与用户显式决定之后。
- **FR-016**: pid 记录存在而心跳年龄超过 watcher 的 `--heartbeat-max-age`（owner：`scripts/watch-target.sh`；语义见 `references/watch-model.md`，本规格不复述数值）时，MUST 报 `heartbeat-stalled` 警告并保持 `RUNNING`，MUST NOT 据此判 `STALLED` 或 `TIMEOUT`；阶段 deadline 仍是唯一超时判据。
- **FR-017**: 阶段产物齐备但无完成哨兵（无论退出记录是否存在、退出码为何）MUST 报 `artifacts-without-completion`；`loop_state` MUST 保持其真实来源判定（`INCOMPLETE`/`FAILED`/`DEAD`），MUST NOT 直接判 `DONE`。
- **FR-018**: status/pid/heartbeat/hook/watchbeat 文件若其信封 `run_id` 与当前执行尝试不符，或修改时间早于 `stage_started_at`，MUST 判为 `stale-signal`；无信封的 legacy 文件在无法证明属于当前尝试时 MUST 按可疑处理并列入 `stale_signals`。
- **FR-019**: 驱动者生命周期约束 MUST 写入 SKILL.md 的 Hard Requirements：U2 派发与首个 U3 监听窗口 MUST 在同一驱动回合内启动；只派发不监听 MUST 被视为生命周期违规。
- **FR-020**: 驱动者确须结束会话时，MUST 在结束前把状态脊写为 `stalled` 或 [[STR-004]]（含当前阶段、已试次数、最近判定与证据指针），并显式上报；静默退出 MUST NOT 被视为合法输出。
- **FR-021**: 系统 MUST 提供状态脊确定性校验（`--action check-spine`）：校验必需字段、封闭取值与跨字段约束。机读段 MUST 声明 `spine_schema: v1`，状态键 MUST 为 `spine_state:`，取值取自 `running / retrying / stalled / done` 以及 [[STR-004]]；`stalled` MUST 有 `stall_reason` 与至少一个证据指针；`running` MUST 有四件套路径与 `stage_deadline_epoch`；`retrying` MUST 有 `retry_reason` 与递增的 `attempt`；[[STR-004]] MUST 有阶段、已试次数、`last_verdict` 与证据指针；`done` MUST 有阶段、已试次数与 `last_verdict`。任何声称 `salvage: accepted` 的记录 MUST 同时有 `salvage_evidence` 与 `salvage_at`；未声称 salvage 时必须缺席或为 `none`。状态脊状态不得与其记录的 `last_verdict` 矛盾。违规 MUST 以 exit 1 与机器可读清单返回；不得使用裸 `state:` 键。驱动者 MUST 在 U2 派发前与写 `stalled` 前运行该校验。
- **FR-022**: 状态脊 MUST 提供有界的机器可读段，使用独立 fence `<!-- loop-state:begin -->` … `<!-- loop-state:end -->` 承载 FR-021 所需字段；fence 内为 `key: value` 行，键带 `spine_` 前缀（至少 `spine_schema`、`spine_state`），MUST NOT 使用裸 `state:` 键，MUST NOT 复用 063 的 `<!-- test-budget:begin -->` fence；散文部分不变。legacy 状态脊（无可读段）MUST 被识别为 `spine_schema=legacy` 并降级求值：缺字段记 `unknown`，MUST NOT 猜测或以默认值补齐。
- **FR-023**: 生命周期与中断检查 MUST NOT 依赖会话记忆、聊天历史或宽泛进程扫描；恢复源 MUST 为状态脊 + Registry + 四件套 + watchbeat + 产物 + git 证据。
- **FR-024**: 远端拓扑下，证据读取 MUST 在证据所在主机以同一执行身份完成，或消费调用方经 ssh 采集的 probe 快照；ssh 不可达 MUST 报 `remote-unreachable` 并建议 `stalled(remote-unreachable)`，MUST NOT 判 `DEAD` 或阶段失败。

#### C. 状态恢复（State Recovery）

- **FR-025**: 恢复入口 MUST 输出恰好一个封闭动作 `none / watch / verify / resume / retry / stop`，由 `loop_state`、产物完整性、中断形态与已试次数按确定性规则裁决；同一输入 MUST 得到同一动作（除 `evaluated_at` 外输出可复现）。
- **FR-026**: 动作裁决优先级 MUST 为：证据不足（`UNKNOWN` 且非未派发）→ `stop`；已试次数达到既有重试上限 → `stop`（`watch`/`none`/`verify` 不受此限）；`stale-signal` 存在且无法隔离 → `stop`；运行中/监听缺失/deadline 活进程 → `watch`；`DONE` 且产物与提交齐备 → `verify`；产物齐备且日志最后一行不是 `ANOMALY:` → `resume`（已提交仅缺状态推进时直接续环；未提交时补提交；无哨兵时按 FR-028 以 salvage 判定为前提）；哨兵在而产物缺（伪完成）或其余终态 → `retry`。既有重试上限与阶段超时数值 MUST 引用 `references/stage-prompts.md` § Stall Handling，不在此复述。
- **FR-027**: `resume` MUST NOT 重派阶段、启动子代理或生成产物内容；它只允许：(a) 提交该阶段产物路径中已存在且未提交的文件，(b) 写入状态脊恢复记录，(c) 把控制权交回驱动者进入 U4。提交 MUST 使用阶段提交约定并在消息中记录中断来源（`run_id` 与已试次数）；任何路径冲突、未合并变更或非本阶段文件 MUST 导致显式拒绝而非部分提交。
- **FR-028**: 阶段无完成哨兵而产物齐备时，`resume` MUST 以独立校验为前提：驱动者 MUST 通过 `recover --action resume --salvage --evidence <ref>` 显式记录 `salvage` 判定（依据 = 产物清单 + 无 `ANOMALY:` 行 + U4 的产物/纪律核验）；`--salvage` MUST 携带至少一个可定位的证据引用，`--apply` 时 MUST 先写状态脊 `salvage: accepted` / `salvage_evidence` / `salvage_at` 记录再提交；未提供 `--salvage` 时动作 MUST 为 `retry`。该路径是对「哨兵为必要条件」的有界例外，MUST 在 U4 结论与收尾汇总中显式可见。
- **FR-029**: implement 阶段 MUST NOT 被恢复程序自动提交代码路径；其 `resume` 仅适用于「工作已提交、只缺状态推进」的情形，否则 MUST 为 `retry`。
- **FR-030**: `retry` MUST 先隔离旧信号再允许下一次派发：把 `status / pid / heartbeat / hook / watchbeat` 中属于旧尝试或无法归属的文件原子移动到状态目录下的 [[STR-005]] 按 `run_id`/尝试序号命名的隔离目录；MUST NOT 删除、覆盖或就地清空任何证据；隔离完成后，下一次派发 MUST 看到干净的本阶段信号面。
- **FR-031**: `retry` MUST 递增状态脊的已试次数并写 `state=retrying`；MUST NOT 自行派发，派发仍由驱动者 U2 执行；同一动作重复执行 MUST 幂等（返回 `already-applied`，不重复递增）。
- **FR-032**: `stop` MUST 写状态脊 `stalled`、生成四要素上送件（发现了什么 / 为何吃重 / 已产生中间产物逐项可定位 / 2–3 个可选处置），并携带 watcher 快照字段（verdict/pid/heartbeat/rc/reason/grace_expired）；MUST NOT 杀进程、删除证据或移除 worktree；活进程的 `TIMEOUT` 停线只允许在最终快照与用户显式决定之后。
- **FR-033**: `watch` 在 `--apply` 下 MUST 刷新 watchbeat 标记并把控制权交回驱动者重新进入监听窗口；dry-run 下只报告将刷新；MUST NOT 修改阶段状态、写状态脊、提交文件或递增已试次数。
- **FR-034**: `verify` MUST 只把控制权交回 U4，不修改任何状态，也不写恢复记录；`loop_state=DONE` MUST 被表述为完成候选，MUST NOT 被表述为已通过独立校验。
- **FR-035**: 恢复动作 MUST 默认 dry-run：未显式 `--apply` 时只输出将执行的步骤与同一判定，MUST NOT 产生写、提交或移动；`--apply` 下只有 `resume / retry / stop` 三个变更动作 MUST 先写状态脊恢复记录（动作、依据、时间、`run_id`/attempt）再执行副作用，完成后回填结果；`watch` 只刷新 watchbeat，`verify / none` 不写任何状态或恢复记录。
- **FR-036**: 所有恢复动作 MUST 幂等且可重入：重复执行同一动作 MUST 不产生第二次提交、第二次隔离或计数漂移；中断后重新执行 MUST 从状态脊与文件系统现状继续，不依赖会话记忆。
- **FR-037**: 恢复程序 MUST NOT 伪造证据：缺失产物保持 `missing`、未知信号保持 `unknown`、无正向证据不得声称完成；任何无法判定的分支 MUST 以 `stop` + 原因上送，而非猜测继续。

#### D. 兼容、分发与测试

- **FR-038**: `watch-target.sh` 的判定状态机、信号优先级、退出码与 `--self-test` 用例 MUST 保持不变；新增标记与聚合 MUST NOT 改变任何既有判定。
- **FR-039**: 四件套文件格式与 `line-registry.py` 的既有 action/字段 MUST 保持兼容；若需增量字段，只允许追加并保证旧条目可读；本特性 MUST NOT 改变 Registry、lease、reservation 或 ownership 语义（owner：Feature 064）。
- **FR-040**: 各 `/speckit.*` 命令内部流程、阶段提示词三段骨架、哨兵字面量、确认门与 fast-fail 纪律 MUST 保持不变；本特性只改驱动技能及其测试与文档。
- **FR-041**: 本特性 MUST NOT 引入常驻服务/daemon、外部服务或新的运行时依赖；实现 MUST 复用既有 shell/Python 标准库、watcher、Registry 与 feedback/probe 机制。
- **FR-042**: 两顶帽子：改动 MUST 落在框架源 `skills/external/sdd-loop-driver/`；`.specify/skills/sdd-loop-driver/` 为生成镜像，MUST NOT 手改；镜像 MUST 经 `sync-mirrors.py` 再生成并通过镜像一致性检查；打包随既有 hatch 构建流程，无手工步骤。
- **FR-043**: 状态感知/中断/恢复规则 MUST 在技能内有一个唯一 owner 文档（references 下的专门文件或章节），SKILL.md 与各 references MUST 引用而非复述判定表；`references/watch-model.md` 仍是 watch 判定的唯一 owner，本特性 MUST NOT 在其中复制状态恢复规则或改变其语义。
- **FR-044**: 文档 MUST 更新：SKILL.md（Hard Requirements 与 References）、owner reference（状态感知、判定表、恢复动作、watchbeat）、`docs/reference/skills/sdd-loop-driver.md`（入口、调用形态、与 watcher/Registry 的关系）；文档取值 MUST 与代码一致。
- **FR-045**: 测试 MUST 至少覆盖：(a) 实测事故回放（派发后无 watcher、产物齐全未提交、`exit=1` 无哨兵）→ 识别中断并给出 `resume` 或 `retry`；(b) 旧 status 污染 → 隔离后才重试；(c) 进程死无退出记录 → `DEAD`；(d) 哨兵在产物缺 → 伪完成；(e) `TIMEOUT` 活进程 → `watch` 不杀；(f) 心跳停跳 → 警告不 `STALLED`；(g) 重试上限 → `stop` 四要素；(h) legacy 状态脊 → 降级不猜；(i) 远端不可达 → `stalled(remote-unreachable)`。
- **FR-046**: 测试 MUST 含变异演练：移除「无 watcher 检测」「旧信号隔离」「salvage 门」任一行为时，至少一条测试 MUST 转红；全部新检查 MUST 有逆样本，MUST NOT 出现只在通过路径上运行的绿。
- **FR-047**: 单线与多线 MUST 同构：快照按线独立求值，不引入跨线推断；多线调用 MAY 由调用方逐线循环，本特性 MUST NOT 新增 manifest 或批量判定语义。
- **FR-048**: 状态脊、快照与恢复记录 MUST 遵守「记录类数据一文一件」：每线每阶段每尝试独立文件或独立机读段，两条活动线并发恢复 MUST NOT 写同一路径，读取方 MUST NOT 观察到半写内容。`recover --apply` MUST 对同一线持有独立原子锁（至少含 holder pid、start ticks、`run_id`、`at`）；第二个写者等待有界时间后 MUST 返回 `result=locked`（exit 1）并附 holder 元数据；疑似 stale lock MUST NOT 被自动清理，只有显式 `--break-lock` 才把旧锁移动到 [[STR-005]] 隔离后继续，绝不删除。

#### E. 边界与非目标

- **FR-049**: 任何流程 MUST NOT 自动 push、自动合并、删除分支或改写远端历史；恢复程序的提交仅为本地阶段提交。
- **FR-050**: 任何流程 MUST NOT 自动 kill 进程、删除日志/信号/worktree 或静默修复证据缺口；清理只能是显式动作，隔离只能是移动。
- **FR-051**: 本特性 MUST NOT 改变「完成需正证据」原则：哨兵/退出记录仍是完成的正证据，产物齐备只是 U4 证据；唯一有界例外是 FR-028 的显式 `salvage` 判定，且必须可见与可审计。
- **FR-052**: 本特性 MUST NOT 替代 058 的 U4 独立校验、U5 卡死处置或 064 的 Registry/lease/ownership；它只提供观测与恢复建议，最终去向由驱动者按既有程序裁决。

### 显式排除项（Out of Scope）

- 自动 push、自动合并、分支删除、改写远端历史或任何绕过确认门的写操作。
- 自动 kill 进程、删除证据/日志/worktree、强制清理 stale lock 或静默修平异常。
- 改变阶段哨兵字面量、watcher 判定状态机、退出码、四件套格式或阶段命令内部流程。
- 新增常驻服务/daemon、外部服务、模型 API 或新的运行时依赖。
- 自动生成缺失产物内容、自动重写 plan/requirements、自动决定任务拆分。
- 跨机器/多用户的全量协调；仅保留既有远端探针形态。
- 替代 058 的独立校验与卡死处置、064 的 Registry/lease/ownership、063 的吞吐优化。

### Key Entities *(include if requirement involves data)*

- **Loop State Snapshot（循环状态快照）**: 一次只读求值的结构化结果，聚合状态脊、Registry、四件套、watchbeat、产物、提交与 watcher 判定；含 `loop_state`、`verdict_source`、中断清单、缺失/未提交产物与唯一恢复动作。它是观测记录，不是新的状态 owner。
- **Interruption Finding（中断条目）**: 封闭形态之一 + 证据指针 + 一句话事实；可多条并存，动作裁决按优先级消费全部条目，不以一条掩盖另一条。
- **Recovery Decision（恢复裁决）**: `loop_state` + 产物完整性 + 中断形态 + 已试次数映射到唯一动作（`none/watch/verify/resume/retry/stop`）；同一输入可复现。
- **Recovery Record（恢复记录）**: 状态脊内的机读记录（动作、依据、时间、`run_id`/attempt、结果），先写后动，幂等。
- **Watchbeat Marker（驱动者监听标记）**: `watchbeat-<line>-<stage>` 单行原子覆盖文件；只证明驱动者存在，不参与判定。
- **Stage Artifact Map（阶段产物映射）**: 阶段→产物路径/提交要求/允许无变更的唯一映射；与 U4 产物清单对齐。
- **State Spine（状态脊，既有）**: 每线一份的恢复状态文件（owner：058 的 `stage-prompts.md`）；本特性增加有界机读段与校验器，不改变其状态词表与写入时点。
- **Watcher Verdict（监听判定，既有）**: 由 `watch-target.sh` 代码侧精确拥有；本特性只消费，不重定义。
- **Line Registry（线路登记册，既有）**: 环境级登记集合（owner：064）；本特性只读消费。
- **Handoff Report（上送件）**: `stop` 生成的四要素报告，含 watcher 快照字段与证据指针。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 实测事故回放夹具（产物齐备未提交、`exit=1`、无哨兵、无 watcher）中，快照在单次调用内识别出至少一个中断形态并给出 `resume` 或 `retry`，人工逐文件检查次数为 0。
- **SC-002**: FR-009 的八类中断形态各至少一个夹具，识别率为 100%；活进程被误判为可终止的次数为 0；正常监听窗口被误报为 `unwatched` 的次数为 0。
- **SC-003**: `resume` 导致的阶段重派次数为 0；提交路径集合中非本阶段文件数为 0；未提供 `--apply` 时的写入/提交/移动次数为 0。
- **SC-004**: `retry` 后旧信号进入隔离目录的比例为 100%，删除数为 0；隔离后下一次派发读取到的旧信号数为 0。
- **SC-005**: `stop` 上送件四要素齐全率为 100%；进程终止数为 0；worktree 删除数为 0；活进程 `TIMEOUT` 停线均带最终快照与显式决定记录。
- **SC-006**: 状态脊校验对注入的缺失/非法字段报告率为 100%，对合法状态脊的 false positive 数为 0；U2 派发前与停线前的执行率为 100%。
- **SC-007**: 既有 `watch-target.sh --self-test` 通过率为 100%，判定与退出码差异数为 0；四件套与 Registry 兼容测试保持绿色。
- **SC-008**: 源与镜像字节一致率为 100%，镜像漂移数为 0；文档入口已更新；新增 daemon/外部依赖数为 0。
- **SC-009**: 同一输入两次快照除时间戳外差异数为 0；同一恢复动作重复执行产生的第二次提交/隔离/计数漂移数为 0。
- **SC-010**: 变异演练中，移除「无 watcher 检测」「旧信号隔离」「salvage 门」任一行为时，至少 1 条测试转红；新增检查的逆样本覆盖率为 100%。

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 Source**: `tests/unit/` 与 `tests/contract/` 下的夹具（构造状态脊、四件套、watchbeat、产物与 git 历史）；逐条断言 `interruptions[]`、`loop_state` 与 `recovery_action`；事故回放夹具直接使用本文件「现状锚点」的事实形态。
- **SC-003 / SC-004 / SC-005 Source**: 临时仓库 + 模拟状态目录的恢复测试；以 `git status`/`git log` 核对提交路径集合，以目录清单核对隔离与删除，以进程桩计数核对 kill/worktree 操作。
- **SC-006 Source**: 合法/非法状态脊夹具矩阵 + 校验器退出码与 JSON 清单；派发前/停线前执行率由契约测试对 SKILL.md 与调用序列断言。
- **SC-007 Source**: 既有 `watch-target.sh --self-test` 输出、驱动技能契约测试、`line-registry` 引擎测试与镜像一致性检查（`sync-mirrors.py --check --only skills/external/sdd-loop-driver`）。
- **SC-008 Source**: `sync-mirrors.py --check`、docs 页面文件存在性、依赖清单比对（无新增包/服务）。
- **SC-009 Source**: 相同夹具两次运行 diff（剔除 `evaluated_at`）；同一动作连续两次 `--apply` 的文件/提交/计数快照比对。
- **SC-010 Source**: 变异演练记录：逐项移除行为并运行测试，记录转红用例；逆样本清单由测试文件枚举。
- 所有度量都从测试或运行产生的制品读取，不手填；无法测量的量显式记为未评估。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "loop-state.py" | FR-001 |
| `STR-002` | "watchbeat-" | FR-010 |
| `STR-003` | "unwatched" | FR-011 |
| `STR-004` | "reentry-required" | FR-020, FR-021 |
| `STR-005` | "attempts/" | FR-030 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-21 — requirements（无人值守）

> 本阶段为无人值守运行，未向用户发起访谈；以下裁决按入口指令、终态权威简报与既有 owner 边界自行作出，已同步落入 Assumptions 与相应 FR。`/speckit.clarify` 可推翻。

- Q: 状态感知应扩展现有 `line-registry.py` 还是新增入口？ → A: 新增 `loop-state.py`（`snapshot` / `recover` 两个动作），保持只读与可测试；Registry 仍由 064 拥有，聚合器只读消费。
- Q: 快照的 `loop_state` 与 watcher 判定冲突时以谁为准？ → A: watch 域以 `watch-target.sh` 为准，`loop_state` 逐字等于 watcher 判定；聚合器只增加 `interruptions`、证据与恢复动作，不改写判定。
- Q: 「已派发但无 watcher」如何确定性检测？ → A: 新增驱动者写入的 watchbeat 标记（每窗口开始/返回），快照以「窗口 + deadline grace」判新鲜度；标记不参与任何完成/存活判定。
- Q: 产物齐备但无哨兵是否允许恢复？ → A: 仅当驱动者显式记录独立校验的 `salvage` 判定时允许 `resume`；否则 `retry`。该例外必须在 U4 与收尾汇总中可见。
- Q: 旧 status 污染如何清理？ → A: 原子移动到 `attempts/` 隔离目录，永不删除；无信封文件按可疑处理；隔离完成后才允许下一次派发。
- Q: `stop` 是否终止进程？ → A: 不终止。只写 `stalled` 与四要素上送件；活进程 `TIMEOUT` 的停线需最终快照与用户显式决定。
- Q: 恢复动作是否默认落地？ → A: 默认 dry-run，`--apply` 才落地；所有动作幂等，重复执行返回 `already-applied`。
- Q: 状态脊如何变得可校验？ → A: 增加固定 fencing 内的 `key: value` 机读段；legacy 状态脊降级求值，缺字段记 `unknown`，不猜测。
- Q: 远端拓扑如何求值？ → A: 在证据所在主机以同一执行身份运行，或消费 probe 快照；ssh 不可达记 `stalled(remote-unreachable)`，不记 `DEAD`。
- Q: Feature 是否在本阶段绑定？ → A: 否。只记录入口声明的 065；最终绑定与注册由 `/speckit.clarify` 完成。

### Session 2026-10-21 — clarify（无人值守）

> 本阶段为无人值守运行，未向用户发起访谈；以下 5 项裁决按入口指令、终态权威文档与既有 owner 边界自行作出，已同步落入 Assumptions（A-1/A-15 修正，A-16…A-19 新增）与相应 FR。独立覆盖扫描由 fresh-context 只读子代理执行；requirements 与 clarify 分属不同执行会话，不构成同作者条件。

- Q: Feature 065 是新建还是绑定既有 Feature（058）？ → A: 新建 Feature 065 并绑定为 Draft；058/063/064 为被引用 owner，绑定先例（063 绑定 058、064 在 058 之上新建）支持新建；注册行与 `features/065.md` 同批落盘，058 的 Related Specifications 增加反向交叉引用。
- Q: `loop-state.py` 的动作集合以 A-1 的“两个动作”为准还是包含 FR-021 的 `check-spine`？ → A: 三个动作 `snapshot` / `recover` / `check-spine`，外加 `--self-test`；A-1 与 requirements 会话中的“两个动作”表述被本裁决修正（旧行保留为历史记录）。
- Q: 无活动 watcher 时 `loop_state` 如何确定性推导，且不与 FR-005 的“不重实现 watcher 状态机”冲突？ → A: derived 映射按 FR-004 的固定优先级（spine stalled/reentry-required → 同名状态；ANOMALY/FAILED/DONE/INCOMPLETE/DEAD/TIMEOUT/NO_SIGNAL/RUNNING/UNKNOWN 按文件证据）求值，始终标注 `verdict_source=derived`，不得声称是 watcher 判定；与 `last_verdict` 冲突时报 `spine_consistent=false`。watchbeat 新鲜度用标记自身 `window=` + `--deadline-grace`，心跳最大年龄用 `--heartbeat-max-age`，两者 owner 均为 `scripts/watch-target.sh`，本规格不复述数值。
- Q: salvage 判定如何被恢复程序识别？ → A: `recover --action resume --salvage --evidence <ref>` 显式提供；`--salvage` 必须带至少一个可定位证据引用，`--apply` 先写状态脊 `salvage: accepted` / `salvage_evidence` / `salvage_at` 再提交；未提供时动作保持 `retry`，且 `check-spine` 对声称 salvage 但缺证据的记录判失败。
- Q: 三个动作的 JSON/退出码/并发契约如何统一？ → A: 所有 JSON 输出带 `schema_version`；退出码统一为 0（求值/应用成功，含 `action=stop` 与 `already-applied`）/1（`check-spine` 失败、apply 被拒或失败、并发锁 `locked`）/2（参数或输入错误）；`recover --apply` 只对 `resume/retry/stop` 先写状态脊恢复记录，`watch` 只刷新 watchbeat，`verify/none` 不写状态；同线并发由独立原子锁串行化，后者返回 `locked`，只有显式 `--break-lock` 才把旧锁移入 [[STR-005]] 隔离。

- 就地修正（非裁决）：FR-016 的“约定的最大年龄”悬空表述改为引用 `scripts/watch-target.sh --heartbeat-max-age`；FR-011 删除“watch-model.md 定义 watchbeat”的错误归属，改为标记自身 `window=` + watcher `--deadline-grace`。
