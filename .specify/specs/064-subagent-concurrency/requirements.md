# Requirements Specification: Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling）

**Requirement Branch**: `064-subagent-concurrency`  
**Created**: 2026-10-20  
**Status**: Draft  
**Input**: User description: "Feature 064 — 让 subagent 驱动的 SDD 在同一环境多线并行、同一仓库多写线与主/子会话生命周期解耦的条件下，保持线路归属不串台、工作区互不破坏、CLI 行为知识持续沉淀、子代理不随主会话死亡。需求语义权威：`/tmp/sdd-064/brief.md`，已逐字归档为 dated record：[notes/source-requirement.md](notes/source-requirement.md)（2026-10-20 快照）；原路径仅保留为 provenance 注记，不再作为权威引用。"

## Related Feature *(mandatory)*

**Feature ID**: 064

**Feature Name**: Subagent 并发归属、CLI 能力档案与生命周期解耦（Subagent Concurrency, CLI Profiles, and Lifecycle Decoupling）

**Binding decision (2026-10-20, `/speckit.clarify`)**: 新建 Feature 064，不绑定既有 Feature。候选核验：058 拥有 U0–U6、状态脊、阶段哨兵与 watcher 判定；061 拥有 `CAPABILITY_MATRIX` 与派发配置；063（在途分支 `bcf27c77`，本分支未登记）拥有 SDD 循环吞吐优化。三者均不拥有「环境级线路登记 + 同仓工作区隔离 + 主/子会话生命周期解耦」的完整范围，且 064 是对它们的增量层而非替代，故新建。已登记于 `.specify/memory/features.md`（Draft）与 `.specify/memory/features/064.md`。

**Related features**:

- **058 — 无人值守 SDD 循环驱动机制（Implemented）**: 拥有 U0–U6 循环、每线状态脊、通用阶段哨兵、watcher 判定状态机与卡死处置。064 引用而不重定义这些语义，只增加归属信封、Line Registry、工作区隔离、CLI 档案与生命周期解耦。
- **061 — 子代理 CLI 配置管理与按派发量化（Implemented）**: 拥有 `CAPABILITY_MATRIX`（派发资格/旗标/支持集）与 `exec-quant` 的 `agent:<slug>` 记录。064 的 CLI 档案只记录观测行为，冲突时派发资格以矩阵为准。
- **063 — sdd-loop-efficiency（in-flight，分支 `bcf27c77`，本分支未登记）**: 拥有 SDD 循环吞吐优化（fast lane、test budget、plan constraint、stream-json/nohup）。其 provisional CLI-profile 范围（`FR-044`…`FR-049`、`CP-01`…`CP-10`）与 064 重叠；**064 是 CLI 能力档案的权威归属**，063 的临时条款由 analyze/plan 逐条裁决「保留在 063 / 迁入 064 / 合并去重」并记录，禁止双 owner 或静默复制。063 的 stream-json/nohup 工作可作为依赖复用；并发、Registry 与重接线由 064 定义。

## 现状锚点（2026-10-20 以 master `ae0eebeb` 与相关分支实测为准；dated record，仅作可行性输入，非运行时保证）

- `skills/external/sdd-loop-driver/` 已定义 U0–U6 循环、每线一份状态脊、通用阶段哨兵与独立校验；「线」目前是驱动侧概念，没有环境级 Line Registry，也没有事件级 line/run 归属信封。
- 监听模型（`references/watch-model.md`）以 PID 文件 + start ticks + status/log/heartbeat 四件套判定，明确禁止用 `pgrep` 零匹配推断完成；判定状态机与退出码由 `scripts/watch-target.sh` 代码侧拥有。
- `references/dispatch-recipes.md` 的远端配方已使用 `nohup` 脱离派发；但「主会话死亡后如何重新接线」没有定义，本地/远端也没有统一 Registry。
- `skills/internal/run-agent/SKILL.md` 拥有派发治理（fast-fail 注入、反嵌套、配置解析）；`shared/definitions/subagent-definitions.md` 拥有 Subagent 概念、三种执行模式与可见性契约。
- 主分支当前不存在 `skills/external/sdd-loop-driver/references/cli/`；Feature 063 的在途分支 `bcf27c77` 已临时加入 CLI 能力档案（`FR-044`…`FR-049`、`contracts/cli-profiles.md` 的 `CP-01`…`CP-10`），尚未合并。
- Feature 061 的 `CAPABILITY_MATRIX`（`scripts/python/execution-config.py`）是派发可接受形态/旗标/支持集的代码侧唯一 owner；CLI 能力档案只应记录观测行为，不得复述或替代该矩阵。
- 同仓库多写线目前共享工作树、Git index、运行时存储、镜像与构建/测试缓存；没有 worktree-per-line、归属清单或集成队列。

## Assumptions（对输入中开放点的裁决记录；2026-10-20 clarify 已确认，残余 plan-level 细节在条目内标注）

- **「线路」（line）**：一条独立推进的 SDD 循环实例（一个项目切片、一个分支/工作树、一份状态脊）。本特性把「线」升级为可登记、可归属的一等实体，但不替换既有状态脊；状态脊仍是阶段状态的 owner。
- **`line_id` / `run_id` 语义**：`line_id` 标识环境内的一条线路，在其证据存续期内不复用；`run_id` 标识该线路的一次执行尝试。重新接线复用同一 `run_id`；重试/重新派发可产生新 `run_id`，旧记录保留。两者与 feedback / exec-quant 的 `(unit_id, run_id)` 记录去重键**不是同一命名空间**，事件信封不得被当作反馈记录消费。
- **Registry 范围与存储**：同一环境（同一 OS 用户）一份；默认位置 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines/`，可由 `SPECIFY_LINE_REGISTRY_DIR` 覆盖（供测试与远端驱动使用），位于任一 line 的 worktree 之外，便于跨项目发现。每线一个 `<line_id>.json`，写入采用「临时文件 + fsync + `os.replace`」原子替换；同线更新用 `<line_id>.lock` 排他锁串行化，跨线写入互不覆盖。跨机器/多用户共享默认排除；远端 line 只在 Registry 中增加最小远端字段（host/alias、run_user、远端路径），由本地驱动经 ssh 读取/校验。
- **Registry 状态词表**：`active / waiting / stalled / completed / orphaned / stale / closed` 为本特性新引入的封闭集；`waiting` 表示已注册但尚未派发、因归属重叠或队列而等待，此时不存在阶段执行，故不与状态脊冲突。`completed` 是唯一的 pre-merge 状态：全部阶段完成即进入 `completed`（写线同时置 `merge_ready=true`，只读线不置），集成结果记录在 `integration_result` 上且不改变状态，U6 收尾才进入 `closed`。它与状态脊的 `running / retrying / stalled / done` 不互相替代，Registry 状态 MUST NOT 与状态脊矛盾。
- **信封编码**：语义字段固定为 `line_id`、`run_id`（以及 stage/事件类型）；编码采用 JSON 旁路记录——status/heartbeat 的字段加日志旁路 `.meta.jsonl`，不写入日志正文，不改变哨兵的「最后非空行」语义。旁路文件的具体命名由 plan 固定并记录。
- **哨兵归属**：通用哨兵字面量与「日志最后非空行」判定不变；归属由承载它的 line-scoped 记录（status/log 旁路/heartbeat 信封）完成，不以改写哨兵、位移最后一行或在哨兵之后追加信封实现。
- **消息入口**：活动线定义为 `state` 为 `active` 或 `waiting` 的 line；>1 条活动线且消息无标识 → 每条消息恰好一次澄清并列出候选；恰好 1 条 → 直接路由；0 条 → 明确报告无活动线路。可识别标识为显式 `line_id`，或唯一匹配的 `project_dir`/`repo_root`/分支名；回答仍无法唯一匹配时显式报告候选并停止路由，不追加第二个问题。任何情况下都不得用 `ps`/`pgrep`/进程名/cwd/环境态推断。
- **写线才要求独立 worktree**：只读 line 可以使用独立只读视图或单独的 worktree，但 MUST NOT 写入；每个 worktree 只允许一个写 line。写 line 的 worktree 默认路径为 `<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`，可配置；分支名由 plan 固定并记录在 Registry。
- **归属清单词表**：`owned_paths / read_only_paths / forbidden_paths` 借用 Team Territory 的三集合语汇，但由本特性的 line 层拥有；不修改也不重定义 Team Territory 语义。
- **集成协调者**：由驱动会话内选定的单一协调者承担，不引入常驻服务；`ready_for_merge` 队列按就绪时间 FIFO、同一时间以 `line_id` 字典序 tie-break，显式声明的拓扑依赖优先于同层 FIFO。
- **构建/测试隔离缺省**：每 line 独立缓存/端口/临时数据库，或只读共享缓存；具体分配算法（端口区间、临时目录命名）由 plan 决定，需求只约束「不得共享可写路径、不得启动全局服务」。
- **CLI 档案归属**：064 是 CLI 能力档案的权威归属；063 的在途 provisional 范围按 FR-044 记录并交由 analyze/plan 逐条裁决；064 的档案额外覆盖 detach/信号/孤儿检测与生命周期解耦事实。
- **CLI 观测触发**：U2 派发前只读查阅并记录 profile/CLI 版本；U4 独立校验与 U5 停线处置各做一次行为比对；反馈经既有 feedback 引擎按 `cli-profile:<cli>` 标记记录，probe 以最小 Probe Object 入既有注册表，不新增 lifecycle point 或平行观测机制。
- **CLI 事实纪律**：超时环境变量的 0/负值语义若未经实测，MUST 记为 `unknown`，不得按训练知识猜测；`known` 事实必须带观测日期、版本与证据指针。
- **脱附形态**：具体使用 `nohup`、`setsid`、`disown` 的哪种组合由对应 CLI 档案与拓扑决定；共同约束是独立进程组/会话、stdio 脱离、主会话终止信号不得传播。
- **单线兼容**：单线运行同样注册并携带信封，保证机制统一；其 U0–U6、阶段链、哨兵与卡死处置行为保持兼容。注册/注销失败时按 LR-02/LR-11 显式上送并停止该线，属受控例外。
- **平台豁免（cwd/branch）**：cwd 校验仅在平台暴露进程 cwd 时执行（Linux `/proc/<pid>/cwd`）；macOS 记录 `cwd_check=unsupported`，这是唯一允许的豁免。branch 校验在有登记且 git 元数据可用时执行，否则记 `skipped`。
- **standalone 反馈例外**：宿主无 `.specify/`（standalone）时，CLI 档案观测的 feedback 记录按编译 `## Wrap-up` 的 runtime-mode gate 跳过反馈引擎调用；档案更新与收尾汇总中的观测报告仍是必需项。
- **Feature 绑定**：已按 `/speckit.clarify` 绑定新建 Feature 064；注册表行与详情文件已落册，Related Feature 不再保留待裁决标记。

## 跨特性重叠与边界（record for analyze/plan；不构成第二 owner）

- **与 Feature 063（sdd-loop-efficiency）**：063 在途分支 `bcf27c77` 已临时加入 CLI 能力档案（其 `FR-044`…`FR-049`、`contracts/cli-profiles.md` 的 `CP-01`…`CP-10`，落点 `skills/external/sdd-loop-driver/references/cli/`，稳定标记 `cli-profile:<cli>`）。2026-10-20 clarify 确认：**064 是其权威归属**；两处 MUST NOT 形成双 owner，也不得静默复制。analyze/plan MUST 逐条裁决「保留在 063 / 迁入 064 / 合并去重」并记录决定；064 的要求额外覆盖 detach/信号/孤儿检测与生命周期解耦事实。063 的 stream-json/nohup 工作可作为依赖复用，但并发、Registry 与重接线由 064 定义。063 在本分支未登记，064 的注册不为 063 建行；其合并时自登记。
- **与 Feature 061（subagent-cli-config）**：061 的 `CAPABILITY_MATRIX` 是派发资格（可接受形态、旗标、支持集）的唯一代码 owner；064 的 CLI 档案是**观测行为知识**（缓冲、超时、哨兵可靠性、session 日志、detach、缺陷、版本证据）。档案 MUST 引用矩阵而不复述；二者冲突时派发资格以矩阵为准，档案记录观测并产生反馈。
- **与 Feature 058（sdd-loop-driver）**：U0–U6、状态脊、阶段尾标、卡死处置与 watcher 判定仍由 058 的既有制品与代码 owner 拥有；064 只增加归属信封、Registry、工作区隔离、档案与生命周期解耦，不改变其语义。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 同环境多线路的身份与归属隔离 (Priority: P1)

使用者在一个环境里同时推进多条 SDD 线路（可能属于不同项目，也可能同项目不同特性）。每条线路有自己的登记条目与状态脊；所有阶段事件都带线路信封。当使用者发来一条未标注线路的消息时，驱动只问一次「是哪条线」，绝不根据进程扫描或当前目录猜测。监听器只信任登记过的 PID 身份；其他线路的事件被标为 foreign，不会改变本线状态。

**Why this priority**: 这是全部并发安全的前提层，也是已观测事故的直接根因——缺少线路登记、事件信封与入口归属规则，导致把别的进程当成自己的进度。

**Independent Test**: 在同一环境启动两条模拟线路，使用相同的通用哨兵（如 `PLAN-DONE`）与相同的 CLI 命令名，注入各自的 status/log/heartbeat 与一个 foreign monitor 事件；逐项核对归属、澄清次数与状态转移。

**Acceptance Scenarios**:

1. **Given** 同一环境有两条活动线（`active` 或 `waiting`），且两条线的阶段日志最后一行都是相同的 `PLAN-DONE`，**When** 各线路的 watcher 分别监听，**Then** 每条线只把属于自己的哨兵判为完成；任何一方的完成都不会被记到另一方头上。
2. **Given** 两条活动线（`active` 或 `waiting`），**When** 用户发送一条不含 line/project 标识的消息，**Then** 驱动只提出恰好一个澄清问题并列出候选线路，不执行 `ps`/`pgrep`/进程名/cwd 推断；用户回答后消息路由到所指线路。
3. **Given** 当前线路正在监听，**When** 收到另一条已登记线路的 monitor 事件或 PID 事件，**Then** 该事件被标记为 `foreign`，当前线路的进度、判定与状态不变，也不会被转发成当前线路的进度。
4. **Given** 登记 PID 已死亡或发生 PID 复用（start ticks 不符），**When** watcher 校验身份，**Then** 不产生虚假完成；该条目进入 stale 处置路径。
5. **Given** 恰好一条活动线，**When** 收到未标注消息，**Then** 直接路由到该线路；**Given** 零条活动线，**When** 收到未标注消息，**Then** 明确报告无活动线路，不猜测目标。
6. **Given** 多条线路并发注册/更新 Registry，**When** 读写交错发生，**Then** Registry 始终可解析，不出现截断、半写或丢失其他线路条目。

---

### User Story 2 - 同仓库并发写线的工作区隔离与确定性集成 (Priority: P1)

使用者在同一仓库上并行推进两条写线路。每条写线路拥有独立 worktree、专用分支与归属清单；写-写重叠在写入前被拒绝或串行化，不相交的路径可以安全并发。运行时记录、镜像同步与命令副本再生成由单一集成协调者在一次集成中统一处理；合并队列顺序确定、可重放，不产生 Git index 损坏或丢失已提交工作。

**Why this priority**: 即使归属正确，共享工作树、Git index、镜像与构建缓存仍会让两条写线互相破坏；这是与串台事故独立的第二类数据风险。

**Independent Test**: 在同一仓库创建两条模拟写线（一条与主线路径重叠，一条完全不相交），并行走完提交与合并队列；检查 Git index、提交图、运行时记录、镜像与端口/临时路径。

**Acceptance Scenarios**:

1. **Given** 同一仓库有两条写线路，**When** 分配工作区，**Then** 每条写线路获得独立 worktree 与专用分支，`worktree_path`/`branch`/`base_sha` 被记录；阶段子代理不切换分支。
2. **Given** 两条线路声明了重叠的 `owned_paths`，**When** 协调者做派发前检查，**Then** 第二条被拒绝或串行化，两者不会同时写入同一路径。
3. **Given** 两条线路的 `owned_paths` 不相交，**When** 并发运行，**Then** 两者可以同时推进，端口、缓存与临时数据库不冲突。
4. **Given** 两条线路都已进入 `completed`（`merge_ready=true`，即 `ready_for_merge`），**When** 集成协调者执行队列，**Then** 按确定性顺序逐线 rebase、跑完整质量门、合并、更新该线 Registry 条目（`integration_result`）、归档运行时记录并移除 worktree，整批结束后统一执行一次镜像同步与命令副本再生成；同一输入的重复执行得到相同顺序与结果。
5. **Given** 一条线路的 worktree 仍有未提交工作或合并失败，**When** 收尾，**Then** 该 worktree 被保留并上送，不删除、不静默丢弃。
6. **Given** 集成中途崩溃，**When** 重新进入，**Then** 以 worktree + 状态脊 + Registry 为证据；stale lock 先验证持有者再处置，不盲目删除。

---

### User Story 3 - 主会话与子代理生命周期解耦与重新接线 (Priority: P1)

使用者的主会话可能崩溃、被关闭或重启，但已派发的阶段子代理不能随之死亡。子代理运行在独立进程组/会话中，runner 写入四件套证据与 Registry。主会话恢复后，新会话只凭 Registry 与状态脊重新接线：验证 PID 身份、做一次 `--once` 快照；运行中则继续监听，已完成则走 U4/U5，已死亡则按卡死程序处置——不重复派发。

**Why this priority**: 无人值守长跑中主会话故障是常态；若子代理随主会话死亡，工作丢失；若恢复后盲目重派，则重复执行与写入冲突。

**Independent Test**: 在模拟阶段运行中 kill 主会话进程/会话，确认子代理存活；启动新会话，按 Registry + 状态脊重新接线，统计重复派发次数与阶段结局。

**Acceptance Scenarios**:

1. **Given** 一个阶段子代理已脱离启动，**When** 主会话进程被 kill，**Then** 子代理进程组继续运行，心跳与最终 status/哨兵仍会被写入。
2. **Given** 主会话已恢复且 Registry/状态脊可读，**When** 新会话重新接线，**Then** 校验 PID start ticks、cwd 与 branch，先做 `--once` 快照；判定 running 时恢复监听，重复派发次数为 0。
3. **Given** 快照判定阶段已完成（哨兵 + 证据齐备），**When** 新会话处置，**Then** 进入既有 U4/U5 校验/收尾路径，不重新派发。
4. **Given** 快照判定子代理已死亡或 PID 身份不符，**When** 新会话处置，**Then** 按既有卡死/重试程序处理，保留 worktree 与证据，不盲目杀进程。
5. **Given** 已有同一 `(line_id, stage)` 的活动执行，**When** 第二次启动尝试发生，**Then** 第二次附着监听或被拒绝，绝不启动第二个同阶段进程。
6. **Given** 远端拓扑的 ssh 连接断开，**When** 主会话重连，**Then** 已脱离的远端子代理仍在运行，并能用同一 Registry 字段重新接线。

---

### User Story 4 - CLI 能力档案的持续沉淀与派发消费 (Priority: P2)

维护者为每个作为 subagent 调用的 CLI 建立独立能力档案。派发前查阅档案以选择正确的输出/超时/脱离形态；运行中在 U4/U5 观察到的实际行为若与档案不符，立即更新档案并记录一条带稳定标记的反馈。qodercli 的已知事实（`-p` 缓冲、超时环境变量、默认最大 600,000 ms、stream-json、session 日志、需脱离 runner）从第一天起可查。

**Why this priority**: 它是可靠性/效率知识层，直接防止「把缓冲当卡死」「把 600 秒上限当阶段超时」一类误判；但不改变阶段判定本身。

**Independent Test**: 检查五份档案与 qodercli 的八个维度；注入一次「行为与 known 不符」的模拟观测，核对档案 provenance 与 `cli-profile:qodercli` 反馈条目。

**Acceptance Scenarios**:

1. **Given** qodercli 档案存在，**When** 维护者查阅，**Then** 八个维度均有 `known` 或 `unknown` 标注，且已知事实带观测日期、版本与证据指针。
2. **Given** claude/codex/opencode/hermes 尚未完整观测，**When** 查阅其骨架档案，**Then** 每个维度显式标注 `unknown`，没有猜测值冒充实测。
3. **Given** 一次派发准备使用某 CLI，**When** 执行 U2 前置检查，**Then** 读取该 CLI 档案并按档案记载选择超时/脱离形态（输出模式的吞吐默认沿用 063 的 stream-json，档案不改写默认）；派发记录带 profile id/version。
4. **Given** U4/U5 观察到档案与实际不符，**When** 处置观测事件，**Then** 先写状态脊观测段，再更新档案 provenance，再记录恰好一条包含 `cli-profile:<cli>` 的反馈；没有新事实时不产生反馈。
5. **Given** 档案更新与一次进行中的阶段，**When** 观察值变化，**Then** 当前阶段继续使用 U2 记录的形态，更新不回溯改变哨兵、判定、退出码、确认门或 deadline。
6. **Given** 档案观测与 061 的能力矩阵冲突，**When** 判断派发资格，**Then** 以矩阵为准；档案记录观测与证据并产生反馈，不暗改矩阵。

---

### User Story 5 - 既有安全与质量边界不回归 (Priority: P2)

使用者在启用上述能力后，既有确认门、no-push 策略、独立校验、哨兵语义与卡死处置保持不变。新增的 Registry、信封、隔离、档案与重接线都是增量层，不引入常驻服务或外部依赖，也不静默删除未提交工作或丢失内容。

**Why this priority**: 这些是框架的红线；并发与生命周期改造不得以牺牲安全边界为代价。

**Independent Test**: 运行既有相关契约/集成测试；模拟 push 尝试、未合并 worktree 清理与单线运行，核对边界。

**Acceptance Scenarios**:

1. **Given** 任意流程运行，**When** 完成阶段或收尾，**Then** 不发生自动 push；push 仍须显式授权。
2. **Given** worktree 存在未提交工作，**When** 收尾或清理，**Then** 工作被保留并上送，不被删除。
3. **Given** 既有阶段哨兵与 watcher 判定，**When** 启用归属信封，**Then** 哨兵字面量、最后一行判定、判定状态机与退出码保持不变。
4. **Given** 本特性交付，**When** 检查依赖面，**Then** 没有新增常驻服务、外部服务或运行时依赖；复用既有 shell/Python/stdlib、feedback/probe 与镜像机制。
5. **Given** 单线运行的既有场景，**When** 启用 Registry/信封，**Then** U0–U6、阶段链、哨兵校验与卡死处置行为与之前一致。

---

### Edge Cases

- 两条线路使用相同的通用哨兵和相同的 CLI 命令名，其中一条先完成：另一条不得因「看到相同哨兵」被判完成。
- 用户消息未标注线路，且用户不回答澄清：驱动不得自行推断；其他线路继续运行，不被这次澄清阻塞。
- Registry 条目存在，但 PID 已死亡而 status 文件恰好有 `exit=0` + 哨兵：按完成证据进入 U4/U5，不按 stale 丢弃。
- PID 被系统复用，start ticks 不匹配：判为死亡/身份不符，绝不附着到新进程。
- 两个启动者同时尝试启动同一 `(line_id, stage)`：原子 reservation 只能让一个成功，另一个附着或拒绝。
- Registry 更新与读取并发：读取方永不见到半写 JSON 或丢失其他条目。
- 两条写线的 `owned_paths` 路径前缀重叠但字符串写法不同（相对/绝对、符号链接）：归一化后仍被识别为重叠并拒绝/串行。
- 两条写线不相交，但共享同一个构建缓存或测试端口：按隔离规则必须分配独立路径/端口，或只读共享；不得写入。
- 集成队列 rebase 后质量门失败：该 line 被保留并上送，不合并、不删除 worktree，不阻塞其他可合并线路的确定性顺序记录。
- 主会话在「Registry 已登记、子代理尚未启动」之间崩溃：留下 reservation/orphan 证据；恢复时先调查，不盲目重试或清理。
- 主会话在子代理运行中崩溃：子代理继续；恢复后 `--once` 判定 running，恢复监听而不重派。
- 远端 ssh 断连但远端子代理仍运行：本地不得把「ssh 失败」当作阶段失败或 DEAD。
- 事件缺失信封或信封不可解析：视为 unattributed，不消费为当前线路证据，显式报告。
- CLI `-p` 模式下日志长时间静默：按档案记录判为缓冲预期，用 status/exit 证据推进，不误判卡死。
- 超时环境变量为 0 或负值且未实测：档案记为 `unknown`，不得猜测其含义，也不据此改变阶段 deadline。
- CLI 观测与档案一致：不产生反馈；只有 mismatch / unknown 获值 / 新版本行为才产生事件。
- 063 与 064 同时存在 CLI 档案制品：不得出现两个 owner；analyze/plan 记录保留/迁移决定。
- 集成失败或显式放弃后经 U6 收尾且尚未合并：注销只做安全的证据归档，worktree 保留并上送；合并成功时 worktree 已由集成序列移除。
- 单线运行：仍注册并携带信封；不得因归属机制引入行为回归。
- 用户回答仍无法唯一匹配候选活动线：显式报告候选并停止路由；不得再问第二个问题，也不得按进程/cwd 猜测。
- 同一 line 的旧 `run_id` 事件到达：标记 `stale-run`，不改变当前尝试状态；不得因 `run_id` 不同而把事件计为 `foreign` 或当前进度。
- Registry 目录不可写或已损坏：U0.5 注册失败即显式上送并停止该 line 启动，不得回退到项目内共享路径。
- 持线 line 的进程死亡但 worktree 仍有未合并工作：`waiting` line 保持等待，归属不自动释放；先保留并上送持线者的 worktree/证据，再由显式处置决定。
- worktree 目标路径已被占用或跨文件系统：显式失败并上送，不得复用或删除其他 line 的 worktree。
- 远端 ssh 不可达而子代理仍在运行：记为 `stalled`（reason=`remote-unreachable`）并重试连通性，不得判 dead，也不得触发重派。
- 同一 stage 的 reservation 存在但持有进程已死且心跳过期：先验证 PID/心跳/状态脊并留痕破除，不得盲目重派。
- 集成时 line 运行时记录与 trunk 同名文件冲突：保留双方证据并上送，不得静默覆盖任一方；由显式处置决定归档形态。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 线路身份、归属与消息入口

- **FR-001**: 同一环境（同一 OS 用户）MUST 维护唯一的环境级 Line Registry；默认位置 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines/`，可由 `SPECIFY_LINE_REGISTRY_DIR` 覆盖；其位置 MUST 在任一 line 的 worktree 之外，并可被发现而无需扫描项目目录；跨机器/多用户共享默认不在范围内。
- **FR-002**: 每条 line MUST 在 U0.5（首次派发前）完成注册，并在 U6 收尾后注销；注册与注销 MUST 原子化（每线一个 `<line_id>.json`，临时文件 + fsync + `os.replace`；同线更新经 `<line_id>.lock` 排他锁串行化），失败 MUST 显式上送而不是静默继续。
- **FR-003**: Registry 的并发更新 MUST 串行化或使用原子替换；每线一条独立记录 + 同线排他锁，跨线写入 MUST NOT 互相覆盖；任何读取方 MUST NOT 观察到截断、半写、重复 `line_id` 或丢失其他 line 条目的状态。
- **FR-004**: 每个 Registry 条目 MUST 含环境内唯一且不复用的 `line_id` 与标识一次执行尝试的 `run_id`；重新接线 MUST 复用原 `run_id`，重试/重新派发 MAY 产生新 `run_id`，历史记录 MUST 保留。
- **FR-005**: Registry 条目 MUST 覆盖：`line_id`（[[STR-003]]）、`run_id`（[[STR-004]]）、`project_dir`、`repo_root`、`worktree_path`、`branch`、`base_sha`、`driver_session`、`cli`、`runner_pid` 与 `qodercli_pid`（各带 start ticks）、prompt/status/log/heartbeat 路径、`owned_paths`（写归属投影）、Ownership Manifest 引用、`stage`、`state`、`created_at`、`updated_at`；远端 line MUST 另含最小远端字段（host/alias、run_user、远端路径）。
- **FR-006**: Registry 的 `state` MUST 使用封闭集 `active / waiting / stalled / completed / orphaned / stale / closed`，并在六个同步点各写入唯一值：**U0.5 注册** → `active`（无归属重叠且未超并发上限）或 `waiting`（`waiting_reason=ownership-overlap|concurrency-cap`）；**U2 派发** → 保持 `active`（`waiting` 不得派发）；**U3 终止判定到达** → 保持 `active`（仅更新 `last_event`，等待 U4 判定）；**U4 校验** → 通过且尚有阶段为 `active`，全部阶段完成为 `completed`（写线同时置 `merge_ready=true` 并写 `ready_for_merge_at`；只读线不置 `merge_ready`，U6 直接关闭）；**U5 停线** → `stalled`（重试可产生新 `run_id` 后回到 `active`，显式放弃进入 U6）；**U6 收尾** → `closed`（`closed_at` 必填）。`waiting` 表示已注册但尚未派发、因归属重叠或队列而等待，此时不得存在阶段执行，故不与状态脊冲突。集成结果不引入新状态：merged/failed 记录为 `completed` 条目上的 `integration_result`，U6 在集成结果记录之后执行。Registry 状态 MUST NOT 与状态脊的阶段判定相矛盾（映射见 `data-model.md` V-LR-9）。
- **FR-007**: 系统 MUST 识别 stale（PID 死亡、PID 复用、start ticks/cwd/branch 与登记不符、或证据超期）；证据超期以既有 watcher 的心跳/阶段期限语义为准，不另设阈值；stale 条目的清理 MUST 是显式、留痕的动作，MUST NOT 盲目删除、覆盖或静默改写其他 line 的登记。
- **FR-008**: 每个阶段 prompt、status、log、heartbeat、哨兵承载记录、watcher 输出与 monitor 事件 MUST 携带机器可读的归属信封，至少包含 `line_id`（[[STR-003]]）与 `run_id`（[[STR-004]]），并含 stage/事件类型；信封 MUST 采用 JSON 旁路记录（status/heartbeat 字段 + 日志旁路 `.meta.jsonl`），MUST NOT 写入日志正文或改变哨兵的「最后非空行」语义。
- **FR-009**: 既有通用阶段哨兵（大写阶段名 + `-DONE`）的字面量与「日志最后非空行」判定 MUST 保持不变；每个哨兵 MUST 可经其所在 line-scoped 记录的信封归属到唯一 line，MUST NOT 通过改写哨兵字面量、位移最后一行或在哨兵之后追加信封来换取归属。
- **FR-010**: 当 >1 条 line 处于 `active` 或 `waiting`（本组条款统称「活动线」），而用户消息未携带 line/project 标识时，驱动 MUST 对每条此类消息只提出恰好一个澄清问题并列出候选活动线；可识别的标识形态为显式 `line_id`，或唯一匹配的 `project_dir`/`repo_root`/分支名；MUST NOT 基于 `ps`、`pgrep`、进程名、cwd 或环境态推断归属。用户回答仍无法唯一匹配时，MUST 显式报告候选并停止路由，MUST NOT 再问第二个问题或猜测。
- **FR-011**: 当恰好 1 条活动线时，未标注消息 MUST 路由到该 line；当 0 条活动线时，MUST 明确报告无活动线路并请求目标，MUST NOT 推断。
- **FR-012**: 一次入口澄清 MUST NOT 停止、暂停或改变其他 line 的子代理与监听；未回答期间，其他 line MUST 继续按状态脊推进；等待回答只阻塞该条消息的路由，不阻塞任何 line 的执行。
- **FR-013**: watcher/monitor MUST 只消费 Registry 中登记且身份校验通过的 PID（start ticks；cwd 在平台暴露时校验，branch 在有登记时校验）；归属判定 MUST NOT 使用宽泛 `ps`/`pgrep`、进程名匹配或当前 shell 状态。
- **FR-014**: 事件归属键为 `(line_id, run_id)`；任何 `line_id` 与当前 line 不同的事件 MUST 被标记为 `foreign`（[[STR-002]]），MUST NOT 被当前 line 消费、转发、计入进度或改变其状态；同一 line 但 `run_id` 非当前执行尝试的事件 MUST 被标记为 `stale-run`，同样不得作为当前尝试的证据。
- **FR-015**: 缺失或不可解析信封的事件 MUST 视为 `unattributed`，MUST NOT 作为当前 line 的完成/失败证据；系统 MUST 显式报告该归属缺口；`foreign`/`stale-run`/`unattributed` 事件 MAY 出现在监听摘要或线日志中，但 MUST NOT 被计入当前 line 的进度、判定或 Registry 状态。
- **FR-016**: 同环境双 line 模拟测试 MUST 证明：相同通用哨兵、相同 CLI 命令名下事件零串台；无标识消息只澄清一次；foreign monitor 事件不改变当前 line 状态；PID 复用/死亡不产生假完成。
- **FR-017**: 单线运行 MUST 同样注册并携带信封；其 U0–U6、哨兵校验、watcher 判定与退出码 MUST 与既有行为兼容，归属为增量。

#### B. 工作区隔离与确定性集成

- **FR-018**: 每条写 line MUST 使用独立的 `git worktree` 与专用分支，从 trunk（或当前集成分支）的 `base_sha` 创建；worktree 默认路径为 `<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`（可配置），MUST 位于任一 line 的 worktree 之外；`worktree_path`、`branch`、`base_sha` MUST 记录在 Registry。
- **FR-019**: 每个 worktree MUST 只有一个写 line；阶段子代理 MUST NOT 切换分支、创建/删除 worktree，或改写其他 line 的 worktree。
- **FR-020**: 每条 line MUST 声明 Ownership Manifest：`owned_paths`（写）、`read_only_paths`（只读）、`forbidden_paths`（禁止访问）；路径 MUST 归一化（相对/绝对统一、符号链接解析）后比较；Manifest 是路径集的 owner，Registry 中的 `owned_paths` 是可由 Manifest 再生的投影。
- **FR-021**: 协调者 MUST 在注册/派发前拒绝写-写重叠；重叠 line MUST 按当前认领时间 FIFO（Manifest `claimed_at`，无则 `created_at`；同一时间戳以 `line_id` 字典序 tie-break）串行化，后到 line 进入 `waiting` 并持有等待票据，直到持线者完成集成合并并完成 U6 收尾，或显式放弃；持线者死亡 MUST NOT 自动释放归属，须先保留其 worktree/证据并显式处置；路径集拆分后才可改为并发；不相交的写 line MAY 并发；任何 line MUST NOT 写入另一活动 line 的 `read_only_paths` 或 `forbidden_paths`。
- **FR-022**: line 本地运行时记录 MUST 写在各自 worktree/line 范围内，且该 line 的阶段提交 MUST NOT 包含这些运行时记录；MUST NOT 存在跨 line 共享的可写运行时路径。运行时记录路径集合是封闭集；其唯一枚举、排除项及排除理由由 `data-model.md` § E8 **Runtime-record path set** 与 **Excluded stores** 表拥有，本条款只声明集合封闭且排除项 MUST NOT 被当作可合并的运行时记录。
- **FR-023**: 集成者 MUST 在一次集成过程中统一提交/归档各 line 的运行时记录（在移除 worktree 之前读取并归档）；MUST NOT 由各 line 分别提交共享运行时记录。
- **FR-024**: 镜像同步与命令副本再生成（`sync-mirrors.py`、`regen-command-copies.py`）MUST 只在集成过程执行一次；MUST NOT 每 line 执行。
- **FR-025**: 合并 MUST 由单一集成协调者执行；队列输入 = Registry 中 `state=completed` 且 `merge_ready=true` 的条目；队列顺序 MUST 确定：按 `ready_for_merge_at` 时间 FIFO，同一时间戳以 `line_id` 字典序 tie-break；若 line 间存在显式声明的拓扑依赖，依赖先于被依赖者，同层仍按 FIFO/tie-break；重放同一输入 MUST 得到相同顺序与结果。
- **FR-026**: 集成流程 MUST 对每条 `ready_for_merge` line 依次执行：rebase 到最新 trunk、运行完整质量门、合并、更新该 line 的 Registry 条目（`integration_result`，状态保持 `completed`）、归档运行时记录、移除 worktree（仅合并成功时）；镜像同步与命令副本再生成 MUST NOT 出现在逐线序列中，MUST 由集成者在整批集成结束时统一执行一次（FR-024）；任一步失败 MUST 保留该 line 的 worktree 与证据并上送，继续下一条。
- **FR-027**: 集成 MUST NOT force push，MUST NOT 绕过既有确认门；push 仍是显式授权动作。
- **FR-028**: 构建/测试隔离 MUST 为每条 line 提供独立的缓存、端口与临时数据库，或只读共享缓存；MUST NOT 启动全局服务；并发上限 MUST 可配置并在派发前检查。
- **FR-029**: 每条 line MUST 报告其分配的端口、缓存/临时路径与并发上限使用情况，供协调者与收尾汇总消费。
- **FR-030**: 崩溃/重入 MUST 以 worktree + 状态脊 + Registry 为恢复证据；遇到 stale lock MUST 先验证持有者身份，MUST NOT 盲目删除；重入 MUST 在任何重派或去向决定之前先做一次 `--once` 快照（快照程序见 LC-08 / V-ID-4）。
- **FR-031**: 同仓库双写线模拟测试 MUST 覆盖重叠与不相交路径集：无 Git index 损坏、无丢失已提交工作、重叠被拒/串行、确定性队列、运行时/镜像只集成一次。
- **FR-032**: worktree 清理 MUST 只在合并成功或用户显式动作后执行；存在未提交工作时 MUST 保留并上送，MUST NOT 删除。

#### C. CLI 能力档案

- **FR-033**: 每个作为 subagent 调用的 CLI MUST 拥有独立档案 `skills/external/sdd-loop-driver/references/cli/<cli>.md`；`qodercli` MUST 存在；`claude`、`codex`、`opencode`、`hermes` MUST 以 known/unknown 骨架存在；没有档案的 CLI MUST NOT 被派发（先建骨架并记录缺口）。
- **FR-034**: 每份档案 MUST 覆盖八个维度：调用方式、关键参数、提示词/权限模式；输出模式（`-p` 缓冲 vs `--output-format stream-json`）与事件形状；后台/超时上限（`BASH_DEFAULT_TIMEOUT_MS`/`BASH_MAX_TIMEOUT_MS`、默认最大 600,000 ms、正值覆盖、0/负值语义）；哨兵可靠性与非终止回显；缓冲/可见性行为；session/run 日志位置；detach 行为（`nohup`/`setsid`/`disown`）、信号/退出与孤儿检测；已知缺陷、版本适用性与证据。
- **FR-035**: 每个条目 MUST 标注 `known` 或 `unknown`；`known` MUST 带观测日期、CLI 版本与证据指针；`unknown` MUST NOT 被猜测值填充；版本/平台不一致 MUST 视为新的观测事件，不得直接沿用旧结论。
- **FR-036**: `qodercli` 初始档案 MUST 至少记录：`-p` 缓冲至退出；`BASH_DEFAULT_TIMEOUT_MS`/`BASH_MAX_TIMEOUT_MS` 与默认最大 600,000 ms、正值覆盖语义；`--output-format stream-json` 支持；session/run 日志位置（含 `~/.qoder/logs/` 的实测路径）；主会话故障需脱离 runner 才能存活；0/负值超时语义 MUST 记录为 `known` 或 `unknown`，不得猜测。
- **FR-037**: 派发前（U2）MUST 查阅目标 CLI 档案，并据此选择超时形态与 detach 形态；输出模式的吞吐默认（stream-json）由 Feature 063 拥有，档案只记录缓冲/事件事实，不得改写该默认；派发记录 MUST 带 profile id/version 与观测到的 CLI 版本。
- **FR-038**: 观测触发点 MUST 至少覆盖 U2 派发前（只读查阅档案、记录 profile id/version 与观测到的 CLI 版本，不改档）、U4 独立校验（比对缓冲/哨兵/退出/日志行为）与 U5 停线（比对超时/detach/孤儿行为）；发现实际行为与 `known` 不符、`unknown` 获得已验证值、或新版本/平台行为首次出现时，MUST 更新档案并记录反馈；匹配且无新事实时 MUST NOT 产生反馈。
- **FR-039**: 观测更新 MUST 先写状态脊的 CLI 观测段，再更新档案 provenance，再记录反馈（先写后动）；一次观测事件 MUST 恰好产生一条 feedback；同一次派发内出现多个独立观测事件时，每个事件各产生一条，不得合并或遗漏；匹配且无新事实时 MUST NOT 产生反馈。
- **FR-040**: 观测反馈 MUST 使用稳定标记 [[STR-001]] + `<cli>`（例如 `cli-profile:qodercli`），经既有 feedback 机制记录并可检索（机制 owner：`.specify/shared/workflow/feedback-step.md` 与 `.specify/scripts/python/feedback-utils.py`）；该观测点 MUST 经既有 probe 注册表登记为最小 Probe Object `skill-sdd-loop-driver-cli-profile`（`class_id=skill-wrapup`、`unit=skill:sdd-loop-driver`、`lifecycle_point=wrap-up`），以 `probe-utils.py --action probes --validate` exit 0 作为唯一登记判据；MUST NOT 使用无法通过注册表校验的 fallback 形态（`custom:` unit 不满足注册表 unit 正则，external 形态要求 `ext-` 前缀，二者均不得登记）；若主落点未来被注册表拒绝，MUST 先修订注册表契约并记录裁决，不得静默改用非法形态；并以 stage dispatch 的 U4/U5 收尾作为反馈记录时点；MUST NOT 新增 lifecycle point、引入未注册的观测机制或复制/替代 feedback 引擎，MUST NOT 自动外传。
- **FR-041**: 档案更新 MUST NOT 改变哨兵语义、watcher 判定状态机/退出码、确认门、阶段 deadline 或测试预算；当前阶段 MUST 使用 U2 记录的形态，更新 MUST NOT 回溯改变它。
- **FR-042**: `references/cli/` MUST 是 CLI 行为知识的唯一落点；其他 references、阶段提示词与 docs MUST 只引用，不得复制档案内容；档案 MUST 经既有镜像机制同步，并提供 docs 入口。
- **FR-043**: CLI 档案 MUST NOT 成为派发资格的第二 owner；可接受形态、旗标与支持集仍由 Feature 061 的代码侧 `CAPABILITY_MATRIX` 唯一拥有。二者冲突时，派发资格以矩阵为准；档案记录观测并产生反馈；矩阵变更 MUST 经其 owner 流程，不得由档案更新暗改。
- **FR-044**: Feature 063 在途的 provisional CLI-profile 范围（其 `FR-044`…`FR-049`、`contracts/cli-profiles.md` 的 `CP-01`…`CP-10`）MUST 被记录为与 064 重叠；064 是其权威归属；analyze/plan MUST 逐条裁决保留/迁移/去重并记录决定，MUST NOT 双 owner 或静默复制；064 的要求 MUST 额外覆盖 detach/信号/孤儿检测与生命周期解耦事实。
- **FR-045**: 档案与契约测试 MUST 钉住档案集合、八个维度、known/unknown 纪律、`cli-profile:<cli>` 标记、镜像与 docs 入口；MUST NOT 新增技能、命令、常驻服务、外部依赖或模型 API。

#### D. 主会话与子代理生命周期解耦

- **FR-046**: 阶段子代理 MUST 在独立进程组/会话中运行（`setsid`/`nohup`/`disown` 的适用组合），stdio MUST 与主会话脱离（重定向到日志或 `/dev/null`）；主会话的终止信号 MUST NOT 传播到子代理。
- **FR-047**: 主会话故障（进程或会话终止）MUST NOT 终止已启动的子代理；子代理生命周期 MUST 独立于驱动的模型循环。
- **FR-048**: runner MUST 在启动前/启动时写入四件套（PID + start ticks、原子 status、log、heartbeat）并在 Registry 登记；派发前 MUST 建立原子 reservation 以防重复启动。
- **FR-049**: 重新接线 MUST 只使用 Registry + 状态脊（以及四件套证据）；MUST NOT 依赖会话记忆、对话历史或宽泛进程扫描；接管前 MUST 取得该 line 的 driver lease（`<line_id>.driver.lock`），lease 由活会话持有时 MUST NOT 夺取。持有者 MUST 以不超过 `ttl_seconds/3` 的周期续租（缺省 TTL 600s → 续租周期 ≤ 200s），并在 U2 派发、U3 终止、U4 校验、U5 处置等阶段推进点各续租一次；lease 存活判据 = 心跳未过期（`now < heartbeat_at + ttl`）且（本地）PID/start token 匹配。过期 lease MUST 先验证持有者证据（心跳/PID/状态脊）再显式破除并留痕；若 PID 仍存活且 start token 匹配但心跳已过期，视为 `suspected-alive`，MUST NOT 自动夺取或自动破除，只允许显式 `--override` 破除并在历史中记录该证据。
- **FR-050**: 取得 lease 后，重新接线 MUST 校验登记的 PID start ticks、cwd 与 branch；校验通过后 MUST 先做一次 `--once` 快照，再决定去向；远端 line 的校验经 ssh 执行，ssh 不可达 MUST NOT 判为死亡或身份不符。
- **FR-051**: 快照判定 running 时 MUST 恢复监听，MUST NOT 重新派发该阶段。
- **FR-052**: 快照判定已完成（哨兵 + 证据）时 MUST 进入既有 U4/U5 校验/收尾路径，MUST NOT 重新派发。
- **FR-053**: 快照判定死亡/身份不符时 MUST 按既有 U5 卡死/重试程序处置，保留 worktree 与证据；MUST NOT 盲目杀进程或删除工作树。
- **FR-054**: Orphan（进程存活但无有效驱动/Registry/状态脊，或 Registry 缺失）MUST 被显式识别、标记并上送；识别只允许使用线自有证据（Registry、worktree、状态脊、reservation、heartbeat/status 文件）与已登记 PID，MUST NOT 用宽泛 `ps`/`pgrep` 发现 orphan；处置 MUST 留痕，MUST NOT 静默认领或静默终止。
- **FR-055**: Stale（Registry 指向的进程已死、PID 复用、cwd/branch 不符或证据超期）MUST 被显式识别、标记并上送；清理 MUST 是显式动作，MUST NOT 覆盖其他 line 的登记；远端 ssh 不可达 MUST 记为 `stalled`（reason=`remote-unreachable`）并重试连通性，MUST NOT 记为 stale/dead。
- **FR-056**: 重复启动防护 MUST 以 `(line_id, stage)` 的原子 reservation 实现（`O_CREAT|O_EXCL` 创建 reservation 文件，内容含 `run_id`、PID、时间戳）；已有活动 reservation 时，第二次启动 MUST 附着监听或拒绝，MUST NOT 启动第二个同阶段进程；stale reservation MUST 先验证 PID/心跳/状态脊再显式破除。
- **FR-057**: U6 收尾 MUST 在集成结果（`integration_result` = merged|failed）记录之后执行；只读线无集成步骤，阶段完成后直接 U6；写线在集成前显式放弃时以放弃记录（`last_event=abandoned`）关闭。U6 MUST 注销该 line 的 Registry 条目（`closed`）、释放 reservation 与 lease、按保留策略归档证据；worktree 的移除只由集成序列在合并成功后执行（FR-026），未合并（集成失败或显式放弃）时 MUST 保留并置 `worktree_retained=true`（用户显式动作除外，见 FR-032）；MUST NOT 留下 `active` 残留。
- **FR-058**: 本地与远端拓扑 MUST 同构：远端使用 ssh + su + nohup，Registry 字段与身份校验规则相同，仅增加最小远端字段（host/alias、run_user、远端路径）；Registry 始终位于驱动侧 OS 用户，远端 line 经 ssh 读取/校验；远端连接断开 MUST NOT 杀死已脱离的子代理，也 MUST NOT 被记为阶段失败或 DEAD。
- **FR-059**: 主会话 kill / 重新接线模拟测试 MUST 证明：子代理存活、新会话经 Registry + 状态脊重新接线、零重复派发、阶段结局正确（running / done / dead 三分支）。

#### E. 边界、非目标与非回归

- **FR-060**: 任何流程 MUST NOT 自动 push；远端写操作仍受显式授权门控。
- **FR-061**: 任何清理流程（包括 FR-032 与 FR-057 所指的 worktree 收尾）MUST NOT 删除未提交工作；清理只在合并成功或用户显式动作后执行。
- **FR-062**: 指令/技能/文档迁移 MUST NOT 静默丢失内容；迁移 MUST 可审计地保留原文，或提供可追溯的等价引用。
- **FR-063**: 除 FR-009 的归属增量和 FR-041 的档案约束外，本特性 MUST NOT 改变既有阶段哨兵语义、watcher 判定状态机与退出码；退出码仍由 watcher 代码 owner 决定。
- **FR-064**: 本特性 MUST NOT 引入常驻服务/daemon、外部服务或新运行时依赖；实现 MUST 复用既有 shell/Python/stdlib、feedback/probe 引擎与镜像脚本。
- **FR-065**: 跨机器/多用户协调 MUST 保持排除；仅允许 Registry 的最小远端字段（host/alias、run_user、远端路径）以支持同构重接线。
- **FR-066**: 既有确认门、独立校验、no-push 策略与阶段命令内部流程 MUST 保持不变；本特性只增加归属、隔离、档案与生命周期层。
- **FR-067**: 契约/集成测试 MUST 覆盖双线模拟、foreign 事件、工作区重叠/不相交、确定性队列、主会话崩溃/重接线、档案更新与反馈标记；删除归属或脱离行为时，至少一条测试 MUST 转红（变异演练）。
- **FR-068**: 单线既有运行 MUST 保持行为兼容：U0–U6、阶段链、哨兵校验与卡死处置不变；新增 Registry/信封为统一增量。

### 显式排除项（Out of Scope）

- 自动 push、自动合并到远端、绕过确认门的任何写操作。
- 删除未提交工作、强制移除未合并 worktree、盲目清理 stale lock。
- 指令/技能/文档迁移中的静默内容丢失或不可追溯的等价替换。
- 改变阶段哨兵字面量、watcher 判定状态机、既有退出码或阶段命令内部流程。
- 新增常驻服务/daemon、外部服务、模型 API 或新的运行时依赖。
- 跨机器、多用户的全量协调（仅保留最小远端字段）。
- 自动选题、自动启动新特性、自动决定合并策略或替代人工裁定。
- 替代 Feature 061 的 `CAPABILITY_MATRIX`，或替代 Feature 063 的吞吐优化范围。

### Key Entities *(include if requirement involves data)*

- **Line（线路）**: 一条独立推进的 SDD 循环实例，由 `line_id` 标识；拥有 worktree/branch、CLI、阶段、状态与归属清单。它是本特性新引入的一等实体；阶段状态仍由状态脊拥有。
- **Line Registry（线路登记册）**: 环境级、worktree 之外的登记集合；默认位于 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines/`（可经 `SPECIFY_LINE_REGISTRY_DIR` 覆盖），每线一个 `<line_id>.json`，同线更新以 `<line_id>.lock` 串行化；每个条目记录 `line_id`、`run_id`、项目/仓库/工作树、分支与 `base_sha`、驱动会话、CLI、PID 身份、四件套路径、归属投影、阶段、状态与时间戳；远端条目带最小远端字段。它是线路发现、归属校验与重接线的唯一恢复入口之一（另一个是状态脊）。
- **Line Envelope（线路信封）**: 附着在阶段 prompt/status/log/heartbeat/哨兵记录/watcher/monitor 事件上的机器可读归属记录，至少含 `line_id`、`run_id`、stage 与事件类型；以 JSON 旁路记录承载（status/heartbeat 字段 + 日志旁路 `.meta.jsonl`），不改变日志正文与哨兵最后一行。
- **Ownership Manifest（归属清单）**: 每条 line 的路径集声明（`owned_paths` / `read_only_paths` / `forbidden_paths`）；它是路径集的 owner，Registry 的 `owned_paths` 是其可再生产投影。与 Team Territory 语汇同形但由 line 层拥有。
- **Integration Queue（集成队列）**: `ready_for_merge` 线路的确定性合并序列；按就绪时间 FIFO、同一时间以 `line_id` 字典序 tie-break，显式拓扑依赖优先；由单一协调者消费，记录顺序，保证重放一致。
- **CLI Capability Profile（CLI 能力档案）**: 每个 CLI 一份的活文档，承载八个维度的观测事实、known/unknown 标注、版本/证据与已知缺陷；是 CLI 行为知识的唯一落点，但不是派发资格 owner（资格归 061 的 `CAPABILITY_MATRIX`）。
- **Detached Stage Execution（脱离式阶段执行）**: 子代理的独立进程组/会话 + runner 四件套 + Registry 条目 + `(line_id, stage)` reservation + driver lease；其生命周期独立于主会话，可被重新接线。
- **Line State Spine（状态脊，既有）**: 每线一份的恢复状态文件；本特性引用而不重定义，继续拥有阶段状态与卡死状态。
- **CAPABILITY_MATRIX（既有，Feature 061）**: 派发可接受形态/旗标/支持集的代码侧唯一 owner；本特性只引用，不复制。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在同一环境双线路模拟中，使用相同通用哨兵与相同 CLI 命令名时，跨线路归属错误事件数为 0；两条线路各自完成判定的正确率为 100%。
- **SC-002**: 当 ≥2 条活动线（`active` 或 `waiting`）时，每条无标识用户消息产生的澄清问题数恰为 1，基于进程扫描的线路推断次数为 0；用户回答后消息路由正确率为 100%。
- **SC-003**: foreign PID/monitor 事件导致当前线路状态转移的次数为 0；被正确标记为 [[STR-002]] 的事件比例为 100%。
- **SC-004**: 同一仓库两条写线（重叠与不相交路径各一组）运行时，Git index 损坏次数为 0，已提交工作丢失次数为 0；写-写重叠在写入前被拒绝或串行化的比例为 100%；同一输入的集成队列顺序与合并结果在重放中差异为 0。
- **SC-005**: 主会话被 kill 后，运行中的阶段子代理存活率为 100%；新会话经 Registry + 状态脊重新接线成功率为 100%，重复阶段派发次数为 0；阶段结局（running / done / dead）与证据一致率为 100%。
- **SC-006**: `qodercli` 档案覆盖八个维度并包含超时/缓冲/session 日志/detach 的已验证事实；一次模拟行为变化产生恰好 1 条可检索的 [[STR-001]]`qodercli` 反馈；无新事实时新增反馈为 0 条。
- **SC-007**: 既有确认门、no-push 策略、独立校验、哨兵字面量与 watcher 退出码保持不变；模拟运行中的 push 动作数为 0；相关既有契约测试保持绿色。
- **SC-008**: 双线模拟与崩溃/重接线模拟均有契约或集成测试覆盖；移除归属信封或脱离行为时，至少 1 条测试转红（变异演练）。
- **SC-009**: 并发注册/更新 N 条线路后，Registry 可解析率为 100%，丢失条目数为 0，重复 `line_id` 数为 0。
- **SC-010**: U6 后该线路的 active Registry 条目数为 0；未合并或仍有未提交工作时 worktree 保留率为 100%；崩溃重入时 `--once` 快照执行率为 100%，重复阶段启动数为 0。

### Measurement Sources & Collection Methods

- **SC-001 / SC-003 Source**: `tests/integration/` 或 `tests/scenarios/` 下的双线模拟夹具 + Registry/status/log/heartbeat 证据；按事件归属逐条计数，输出差异清单；变异演练移除信封字段后复跑。
- **SC-002 Source**: 消息入口模拟夹具记录每次澄清问题数与路由结果；同时断言运行期间无 `ps`/`pgrep` 归因调用（以桩替换并计数）。
- **SC-004 / SC-009 Source**: 临时仓库 + 两条 worktree 的集成测试；`git fsck`/index 校验、提交图比对、队列日志重放；并发注册脚本对每线独立 `<line_id>.json` 做 N 次写入后解析、去重与丢失检查，并验证同线锁下无半写。
- **SC-005 / SC-010 Source**: 崩溃/重接线测试夹具：启动带心跳的模拟阶段进程，kill 驱动会话，重启新会话并按 Registry/状态脊重接；统计派发次数、`--once` 调用、driver lease 获取/破除、worktree 保留与 Registry 残留。
- **SC-006 Source**: 档案文件内容核对 + `feedback-utils.py --action list --contains "cli-profile:qodercli"` 输出；注入 mismatch / unknown-fill / new-version 三类观测夹具，统计条目数。
- **SC-007 / SC-008 Source**: 既有契约/集成测试套件、watcher `--self-test`、变异演练记录；push 动作以命令桩计数。
- 所有度量都从测试或运行产生的制品读取，不手填；无法测量的量显式记为未评估。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "cli-profile:" | FR-040, SC-006 |
| `STR-002` | "foreign" | FR-014, SC-003 |
| `STR-003` | "line_id" | FR-005, FR-008 |
| `STR-004` | "run_id" | FR-005, FR-008 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-20

> 本阶段为无人值守运行，未向用户发起访谈；以下为按入口指令自行裁决的关键开放点，已同步落入 Assumptions。`/speckit.clarify` 可推翻。

- Q: `line_id` 与 `run_id` 的关系是什么？ → A: `line_id` 标识线路且不复用；`run_id` 标识一次执行尝试；重新接线复用 `run_id`，重试可产生新 `run_id` 并保留历史。二者与 feedback/exec-quant 的 `(unit_id, run_id)` 记录键不是同一命名空间。
- Q: Line Registry 的作用范围？ → A: 同一环境同一 OS 用户一份，位于任何 worktree 之外；跨机器/多用户共享排除，只保留最小远端字段。
- Q: 无标识消息在只有一条/零条活动线路时如何处理？ → A: 一条直接路由；零条明确报告无活动线路；只有 >1 条时才提出恰好一个澄清。
- Q: Feature 063 的在途 CLI 档案范围如何处理？ → A: 064 为权威归属；requirements 记录重叠，analyze/plan 逐条裁决保留/迁移/去重并记录，禁止双 owner 或静默复制。
- Q: CLI 档案与 Feature 061 的 `CAPABILITY_MATRIX` 边界？ → A: 矩阵拥有派发资格；档案拥有观测行为知识；冲突时资格以矩阵为准，档案记录观测并产生反馈。

### Session 2026-10-20 — clarify（无人值守）

> 本阶段仍为无人值守运行，未向用户发起访谈；以下裁决按入口指令与终态权威文档 `/tmp/sdd-064/brief.md` 自行作出，已同步落入 Assumptions 与相应 FR。裁决依据：brief §3/§4/§5、058/061/063 的既有 owner 边界、以及以 master `ae0eebeb` 为基准的现状锚点。

- Q: Feature 064 应绑定既有 Feature 还是新建？063 在途的 provisional CLI-profile 范围如何归属？ → A: 新建 Feature 064（058/061/063 均不拥有并发归属、同仓工作区隔离与生命周期解耦的完整范围）；064 是 CLI 能力档案的权威归属，063 的 `FR-044`…`FR-049`、`CP-01`…`CP-10` 由 analyze/plan 逐条裁决保留/迁入/去重并记录，禁止双 owner 或静默复制；063 未在本分支登记，合并时自登记。
- Q: Line Registry 的存储位置与原子性、无标识消息入口、foreign/unattributed 事件、哨兵归属的最终规则？ → A: Registry 默认为 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines/`（`SPECIFY_LINE_REGISTRY_DIR` 可覆盖），每线一个 `<line_id>.json`，临时文件 + fsync + `os.replace` 原子替换，同线 `<line_id>.lock` 排他锁串行化；活动线 = `active` 或 `waiting`，>1 条时每条无标识消息恰好一次澄清并列出候选，1 条直接路由，0 条显式报告，禁止进程扫描推断；归属键 `(line_id, run_id)`，`line_id` 不同→`foreign`，缺失/不可解析→`unattributed`，同线旧 `run_id`→`stale-run`，三者均不得改变当前状态；哨兵仍为日志最后非空行原文，信封写入旁路 JSON，不追加/不改写哨兵行。
- Q: worktree 路径与清理、ownership 重叠串行化、集成队列顺序、运行时/镜像提交归属？ → A: worktree 默认 `<repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`；清理仅在合并成功或用户显式动作后以 `git worktree remove` 执行（无 `--force`），未提交/未合并保留上送。写-写重叠按当前认领时间（`claimed_at`，无则 `created_at`）FIFO、`line_id` 字典序 tie-break 串行化，后到线 `state=waiting`；持线者死亡不自动释放归属。集成队列按 `ready_for_merge_at` 时间 FIFO、`line_id` tie-break，显式拓扑依赖优先；每线依次 rebase→完整门→合并→更新该线 Registry 条目→归档运行时→移除 worktree（仅合并成功），整批结束后统一执行一次镜像同步与命令副本再生成，失败保留并继续下一条。运行时记录由各 line 写在自身 worktree 且不提交，集成者一次归档/提交；镜像同步与命令副本再生成只在集成过程执行一次（FR-026 为逐线/批次基数唯一 owner）。
- Q: 主会话 kill/restart 的 reattach 协议、orphan/stale/重复启动、跨机器边界？ → A: 新会话以 Registry+状态脊为唯一恢复源，先取 `<line_id>.driver.lock` lease（活会话持有不得夺取，过期 lease 先验证再破除），校验 PID start ticks/cwd/branch，再跑 `--once`；running→恢复监听零重派，done→U4/U5，dead/身份不符→既有 U5 卡死/重试并保留 worktree/证据。`(line_id, stage)` 以 `O_CREAT|O_EXCL` reservation 防重复启动，第二启动者只能附着或拒绝。orphan 仅由线自有证据与已登记 PID 识别，禁止宽泛进程扫描；stale 由 PID 死亡/复用/cwd/branch 不符/证据超期识别，清理留痕。Registry 位于驱动侧 OS 用户；远端 line 只加 host/alias、run_user、远端路径，ssh 不可达记 `stalled`（reason=`remote-unreachable`）而非 dead。
- Q: CLI 能力档案的 probe+feedback 触发点与既有边界？ → A: U2 派发前只读查阅并记录 profile/CLI 版本；U4 独立校验与 U5 停线各做一次行为比对；仅在 `known` 不符、`unknown` 获得已验证值、或新版本/平台首次出现时，先写状态脊观测段→更新档案 provenance→经 `feedback-utils.py` 记录恰好一条 `cli-profile:<cli>` 反馈；无新事实不产生反馈。probe 以最小 Probe Object `skill-sdd-loop-driver-cli-profile` 入既有注册表（`skill-wrapup` + `skill:sdd-loop-driver` + `wrap-up`；不使用无法通过 `probes --validate` 的 `custom:` fallback），不新增 lifecycle point、不复制 feedback 引擎、不自动外传。既有哨兵字面量、watcher 判定状态机/退出码、确认门、阶段 deadline 与测试预算不变。

### Session 2026-10-20 — analyze repair-1（无人值守）

> 本阶段为 analyze 门回环第 1 轮，未向用户发起访谈；以下裁决按入口指令、终态权威 brief 与既有 owner 边界作出，已同步落入相应 FR/契约/数据模型，`/speckit.clarify` 可推翻。

- Q: 「全部阶段完成但尚未合并」的 Registry 状态是 `completed` 还是 `active + merge_ready`？ → A: **`completed` 是唯一 pre-merge 状态**：U4 全部阶段完成即置 `completed`，写线同时置 `merge_ready=true`（只读线不置，直接 U6）；集成只更新 `integration_result` 并把 `merge_ready` 置 false，状态保持 `completed`；U6 在集成结果记录之后执行并置 `closed`。`active` 仅表示已派发且脊为 `running/retrying`，或尚未派发的 `stage=null` 空窗。
- Q: U6 与集成的先后？ → A: **集成先行、U6 收尾**：合并成功由集成序列移除 worktree；集成失败或显式放弃时 line 保持 `completed` 等待显式处置；经 U6 关闭且未合并时保留 worktree（`worktree_retained=true`）。等待线只在持线者完成集成合并并 U6 `closed`，或显式放弃后晋级；stale 清理产生的 `closed` 不构成自动释放。
- Q: 镜像与 Registry 的更新基数？ → A: 每条合并线只更新自己的 Registry 条目（`integration-record`）；镜像同步与命令副本再生成由集成者在整批结束时统一执行一次（FR-024 为唯一基数，FR-026 的逐线步骤不含镜像）。
- Q: driver lease 的续租节奏与「PID 活但心跳过期」如何处置？ → A: 持有者 MUST 以 ≤ `ttl_seconds/3`（缺省 TTL 600s → ≤200s）续租，并在阶段推进点各续租一次；存活判据为心跳未过期且 PID/token 匹配；心跳过期但 PID 仍存活且 token 匹配视为 `suspected-alive`，不得自动夺取或破除，只允许显式 `--override` 破除并留痕。
- Q: Probe Object 的 fallback 形态？ → A: 主落点 `skill-wrapup` + `unit=skill:sdd-loop-driver` 经实测可通过 `probes --validate`；`custom:` 形态不匹配注册表 unit 正则、external 形态要求 `ext-` 前缀，故 MUST NOT 保留不可执行的 fallback。
- Q: 运行时记录集合如何闭合？ → A: 以 `data-model.md` § E8 的四路径为唯一枚举；`evidence/`、`history/`、`trigger/` 明确排除（理由见 FR-022）。
- Q: SC-002 的路由正确率如何处理 `ambiguous-stop`？ → A: `ambiguous-stop` 是 FR-010 规定的正确终止结局，计为正确而非错误；正确率 = 正确结局数 / 已回答消息数。SC-003/SC-005 的其余测量面（stale-run/unattributed、orphan/stalled/remote-unreachable）留待 G-04 后续收口。
