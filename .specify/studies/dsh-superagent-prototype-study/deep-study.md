# Deep Study — dsh-superagent-prototype

> 证据路径均相对研读副本根：`stripped/…`（即 `$STUDY_DIR/stripped/`）。未标注即代码事实；推断处显式标 `推断`。

## 1. 核心概念（项目用自己的词汇解决什么问题）

### 1.1 一句话定位

dsh-superagent 是**一个 GitHub 仓库（可选 + Feishu）的"主动式编码 Agent"**，打包为 DeepSeek Harness（DSH）的 Cordis 插件 Bundle。它的目标不是"更强的编码"，而是**把团队注意力当作第一成本**：只在被请求或书面规则允许时行动，只在人必须动作或能使用结果时说话（`stripped/README.md:7-9`，`stripped/docs/000-philosophy.md:3-15`）。

**它要解决的真实痛点**：一个能替全团队干活的 Agent，也能消耗全团队的注意力。多数 Agent 产品把"主动性"做成"更多消息/更多 PR"，而这里把主动性拆成**可审计的授权链**（谁允许、依据什么、范围多大），并把"是否打扰人"做成领域规则而非提示词建议（`stripped/docs/001-domain.md:3-7`）。

### 1.2 术语表（概念 → 一句话定义 → 代码落点）

| 概念 | 一句话定义 | 代码落点（`stripped/` 下） |
|---|---|---|
| **Source** | 事件流；kind 是可复用实现、instance 是一次配置；自己保存读取位点与 bot 身份 | 协议 `src/sources/kind.ts`（缺失）；消费侧 `src/core/model.ts:23-39` 的 `Trigger.source`；门控 `src/policy.ts:133` `listened()` via `SourceScope` |
| **Trigger** | 一条不可变事件（含 actor、是否人写、是否点名），审计与幂等的最小单元 | `src/core/model.ts:23-39`；摄入 `src/core/intake.ts:19-62` |
| **Thread** | 按时间序的 Trigger 集合；同一 Thread 同时最多一个 Eval；订阅与 Decision 历史的聚合边界 | `src/core/model.ts:156-182`（`Thread` 接口）；`src/core/intake.ts:31-48` |
| **Correlation** | 一个 Trigger 所属多个 Thread 之间的关系；只添上下文、**永不路由** | `src/core/model.ts:170-171`（`correlated`），写入 `src/core/intake.ts:37` |
| **Channel** | Thread 的写侧地址（评论/话题回复/PR） | `src/core/model.ts:9` `ChannelRef`；发送 `src/app/outbox.ts:39-51` |
| **Policy** | 版本化的准入规则 + 每个 Source 的部分（白名单/准入表/bot 列表）；变更会**作废运行中的 Eval** | `src/policy.ts:111-118`（版本哈希）、`191-211`（gate）、`213-240`（revalidate） |
| **Eval** | 对一批 Trigger 的判定（gate + assessment 两层），无状态；输入含 Thread 快照与全部 Ticket | `src/core/evals.ts:71-119`（start）、`131-156`（decide） |
| **Mandate** | accept 授予的不可变授权：强度、Policy 版本、gate 依据（`MandateBasis`）、范围 | `src/core/model.ts:116-133`；创建 `src/core/evals.ts:306-316` |
| **Ticket** | 授权的工作单元；open→ended，可被人的消息在同一 Mandate 下 resume；**自己定义状态**而非跟随执行器 | `src/core/model.ts:277-308`；生命周期 `src/core/tickets.ts:37-56`（create）`252-270`（wake）`345-363`（end） |
| **Assignment** | Ticket ↔ 一个执行器实例的绑定；pending→running→ended，独立于 Ticket | `src/core/model.ts:211-233`；`src/core/assignments.ts:34-43` |
| **Subscription** | Ticket ↔ Thread 多对多；匹配的 Trigger **扇出**为上下文、不重新鉴权 | `src/core/model.ts:163-164`；扇出 `src/core/intake.ts:38-52`；规则全表 `docs/001:37` |
| **Eval / Gate / Assessment** | Eval 两层：`gate`=确定性准入（谁、什么强度）；`assessment`=模型研判 | `src/policy.ts:167-211`（gate 实现）；`src/app/assessment.ts:89-282`（模型研判） |
| **Strength** | `explicit`（白名单者点名 / 明确准入格）vs `inferred`（推断候选，受 accept mode 约束） | `src/core/model.ts:96`；`src/policy.ts:141` `STRENGTH` 序 |
| **Accept mode** | `off` / `observe`（默认，记录"would accept"）/ `auto` | `src/core/model.ts:99-103`；转换 `src/policy.ts:55-57` |
| **Human attention（Attention）** | Ticket 上等待人回答的结构化问题；面板与转发都围绕它 | `src/core/model.ts:275`；状态机 `src/core/stage.ts:12` |
| **Main Session / Executor Session** | 主 Session（代码/提示词里叫 `orchestrator`）只路由；Executor Session（`worker`）每 Ticket 一个，干活 | `src/app/sessions.ts:48`（preset 名）；`src/executor/dsh.ts:24`（`worker-<ticketId>`） |
| **Execution environment** | prepare 命令与 worker 共享的变量集合（键/值/描述，无凭据） | `src/app/execution-environment.ts`；`docs/003:63-79` |
| **Disposition** | Trigger 去向记录：filtered / eval / fan-out / handback / acked —— 同一 Trigger 的审计轨迹 | `src/core/model.ts:41-61`；写入 `src/core/intake.ts:54-55` |

### 1.3 概念如何咬合（这张图是理解全项目的钥匙）

1. Source 产 Trigger → 入 **Intake**：去重、按 Source scope 过滤、写 disposition、给每个订阅 Ticket **扇出**为 Input，并把"无人拥有的消息"排入其主 Thread 的 **Eval**（`src/core/intake.ts:19-62`）。
2. Eval 用 **gate** 先定强度与 MandateBasis；只有 `explicit` 的请求或（`auto` 模式下）匹配启用规则的 inferred 候选能 accept 成 **Ticket**（`src/core/evals.ts:131-156`，`src/policy.ts:212`）。
3. Ticket 的授权封装在 **Mandate** 里；执行由 **Assignment** 绑定到 **Executor**；写入经 **Channel**；一切变化由 **Engine** 在一个事务里写（`src/core/engine.ts:24-48`）。
4. 人的后续消息走 **Subscription 扇出**回到 Ticket（绕过 gate、不加权）；执行器有权决定/交回（handback）；交回后无主才重新进 Eval（`src/core/model.ts:75-88`，`src/core/part.ts:42-48`）。

**被刻意拒绝的概念**（`docs/001:45-61`，代码一致）：把人变成实体、跨 Source 映射身份、Eval 自己调度延迟（等待属于 Source）、"每 Thread 最多一个活 Ticket"、让 Ticket 状态跟随 Session 等。这体现 `docs/000` 的"少概念"原则：业务需求落在既有概念的属性或提示词上（`docs/000:19-22`）。

## 2. 基本架构

### 2.1 系统边界与外部世界

- **宿主**：DeepSeek Harness（Cordis 插件框架）。插件 `apply(ctx, config)` 注入 11 个宿主服务（`src/index.ts:8`），把 `Runtime` 注册为 Cordis 服务 `orchestrator`（`src/app/runtime.ts:88`）。
- **外部系统**：GitHub（经 `gh` CLI，agent 账号）、Feishu（经 `lark-cli`，bot 身份，强制 `strict-mode=bot`，`src/deployment.ts:114-131`）。**没有 HTTP API 直连业务系统**——一切经 CLI（`src/infra/commands.ts`），这让审计与身份复用落在操作系统层。
- **硬边界**：`src/core` 不 import 外部（除 Node hashing）且无 I/O（`docs/007:256-259` 声明，实测 import 一致）；`src/sources` 不得 import `src/app`（同上）。

### 2.2 分层与依赖方向

```
client (React 面板) ──HTTP(/orchestrator/api)──> app/http+views
        │ 只 import 类型与纯值
app  ──> core（经 ports.ts 的端口类型）
executor ──> app(Effects/Sessions) + core 类型
sources(协议) ──> core 类型；被 app 经 SourceRegistry 使用
infra ──> 无领域依赖（CLI/环境/健康/文本）
```

依赖注入的形态是 **`Pick` 窄接口**而非抽象基类：`EngineForSources`/`EngineForMainSession`/`EngineForPeople`/`EngineForSettings`/`EngineForExecutor`（`src/core/engine.ts:260-270`），以及各宿主接口（`ExecutorHost` `src/executor/dsh.ts:59-82`、`AssessorHost` `src/app/assessment.ts:49-64` 等）。这是"一个状态只有一个写者"的边界技术（`docs/007:259-271`）。

### 2.3 架构风格：**事件摄入 + 事务内状态机 + 事务外持久副作用**

风格不是常见"事件总线"，而是：**同步领域命令**（Engine 全部方法同步，`docs/007:48`）在 SQLite 事务内改聚合，同时把外部工作 `enqueue` 成 **Effects** 行；事务提交后才执行（`src/app/effects.ts:61-66`，`docs/007:164-181`）。这解决三个约束：

1. **崩溃一致性**：状态与"待做的副作用"同事务落盘（`docs/003:153-161`）。
2. **顺序与幂等**：每种 effect 有 kind/key 合并与有序/限额策略（`src/app/effects.ts:104-122`）；Outbox 用收据保证同 Ticket 同会话顺序（`src/app/outbox.ts:39-51`）。
3. **可观测**：每个 kind 一条健康项（`src/app/effects.ts:147-160`）。

**代价**：所有外部行为至少延迟一个事务提交 + 一个 microtask；复杂逻辑被拆成"命令（现在）+ effect handler（稍后）"两段，调试需跨两处（推断）。

### 2.4 运行拓扑（单进程）

一个 DSH 进程内：`Runtime`（组合根）持有全部组件；`Passes` 每 2 秒触发一次 pass（`src/app/passes.ts:28-33`）；状态在 `<stateDir>/orchestrator.sqlite`（WAL，schema 11，`src/app/store.ts:63-90`）；目录锁防双进程（`src/app/runtime.ts:91-94`）；worker 在 `<stateDir>/work/<ticket>-<id前12位>` 的独立目录/工作树里跑（`src/executor/dsh.ts:97-111`）。

> **降级说明**：UML 主视图（组件图/部署图/时序图）已按计划编写 `.puml` 源（`figures/*.puml`），但本次运行环境无法访问 draw-diagram 渲染后端（`xuanji-render.aliyun-inc.com` 9696-9701 全部不可达），因此报告内以 Mermaid 草图替代；源文件保留待渲染后替换。

## 3. 组件构成

### 3.1 组件清单（按业务功能划分）

| 组件 | 职责 | 对外接口 | 依赖 | 证据 |
|---|---|---|---|---|
| **Engine（领域内核）** | 唯一写者：Trigger/Thread/Decision/Ticket/Assignment；五部件（Intake/Evals/Tickets/Assignments/Replies）单向依赖 | 角色化 `Pick` 接口 | ports（Repositories/Policy/SourceScope/Assessor/Executor/Outbox） | `src/core/engine.ts:24-270` |
| **Intake** | 摄入、过滤、关联、扇出、入 Eval | `Engine.receive` | Tickets | `src/core/intake.ts:16-63` |
| **Evals** | 批处理、gate 强度选择、截止期、过期重排、Decision | `Engine.evaluateDue/decide/reevaluate/handback` | Tickets | `src/core/evals.ts:27-340` |
| **Tickets** | Ticket 生命周期、订阅、Inputs、resume/retry/stop/end、Policy 通知 | `bindThread/threadClosed/attach/stopTicket/retryTicket/unsubscribe/note...` | Replies | `src/core/tickets.ts:29-423` |
| **Assignments** | 执行器事实与 Worker Report、attention 生命周期、restart | `assignmentStarted/inputsDelivered/inputsRead/report...` | Tickets, Replies | `src/core/assignments.ts:30-140` |
| **Replies** | Channel 写入四用途的规则化（幂等 id） | `Engine.reply` | 无 | `src/core/replies.ts:26-95` |
| **Policy（配置即策略）** | Zod schema、Policy 版本哈希、gate、Mandate 重验证、评估→Outcome 转换 | `settingsPolicy()` 返回无状态 Policy | Settings 类型 | `src/policy.ts:1-242` |
| **Runtime** | 组合根：锁目录、构建全部组件、启动/关闭顺序 | Cordis service `orchestrator` | 全部 | `src/app/runtime.ts:59-253` |
| **Store** | SQLite 仓储（JSON 行 + 生成列索引）、只读查询、kv、收据 | `Repositories` + `storeReads` | node:sqlite | `src/app/store.ts:30-120`，`src/app/store-read.ts` |
| **Effects** | 持久副作用队列：assessment/launch/delivery/relay/notice/reply | `enqueue/handle` | Store | `src/app/effects.ts:46-161` |
| **Outbox** | 发送收据 + 每 Ticket 每会话顺序 + 退避 | `Outbox` 端口 | Effects, SourceRegistry | `src/app/outbox.ts:22-52` |
| **Passes** | 每 2s / 按需的 pass；单飞合并 | `request/idle` | Engine, Effects | `src/app/passes.ts:22-69` |
| **MasterAssessor** | 候选卡片投递、受限上下文窗口、评估结果转换 | `Assessor` 端口 + `orchestrator_eval*` | Sessions, effects | `src/app/assessment.ts:89-282` |
| **Sessions** | 两个角色的 DSH Session：preset、prompt 幂等投递、noWait 守卫、工具注册 | `ensure/prompt/relay/notify` | DSH agent | `src/app/sessions.ts:93-...` |
| **DshExecutor** | 每 Ticket 一个 Session+目录；launch/delivery、WorkerSlots、瞬态重试、恢复、后台工作收敛 | `Executor` 端口 | Effects, Sessions | `src/executor/dsh.ts:207-673` |
| **Settings / Prompts** | 版本化设置块与提示词配置；Policy 变更效果计算与通知 | `save/pause/sync`，`save/preview/compose` | Store, Engine | `src/app/settings.ts:82-...`；`src/app/prompts.ts:135-...` |
| **HTTP + views + client** | `/orchestrator/api`（same-origin、限额）、六个视图投影、React 面板六 Tab | `registerHttp` | Store 只读 | `src/app/http.ts:230`，`src/client/index.tsx` |
| **infra** | CLI 传输（gh/lark/git）、环境 shim、HealthBoard、文本限额 | 函数级 | 无 | `src/infra/commands.ts`，`src/infra/environment.ts`，`src/infra/health.ts` |
| **sources（协议，缺失实现）** | `SourceKind`/`SourceRegistry`/`SourceHost`/`SourceContext` 契约 + GitHub/Feishu 适配 | Cordis 注入 `orchestrator` | core 类型 | 仅剩消费侧 import；文件缺失（见 §5） |

### 3.2 核心 vs 次要

- **核心（承重）**：Engine 及其五部件、Policy、Effects、DshExecutor、Outbox。项目所有硬保证（授权不可被提示词绕过、崩溃一致、注意力约束）都压在这五处。
- **次要（支撑）**：Store 是记录层；Passes 是时钟；Sessions/assessment/tools 是模型接口适配；client/views 是只读投影；infra 是传输。
- **特殊边界**：`sources/` 既是宿主给插件的契约（`SourceContext`），又是插件给宿主的实现（`SourceKind`）——**双向端口**，本快照只保留了宿主侧（`docs/007:183-195`，`src/app/runtime.ts:50-51` 的模块声明 `Context.orchestrator: SourceHost`）。

### 3.3 组件如何协作（叙事）

主 Session 与 worker 是**两种不同能力集**的 Session（`src/app/sessions.ts:61` 的 `WORK_TOOLS`、`260-280` 的 preset 守卫）：主 Session 只拿到 14 个 `orchestrator_*` 工具——读资源、路由（1-20 条决策/次）、触发重评、评估、回复、退订、改设置/提示词（`src/app/tools/main.ts:154-301`）；worker 只有 6 个（读、ack、report、thread_follow/unrelated、handback，`src/app/tools/executor.ts:23-105`）。**二者的协作不靠共享内存，而靠 Engine 的领域状态 + Effects 投递**：worker 的 report 先写 Ticket，再由 `reportRelay` 转成主 Session 消息（`src/app/notices.ts:121-129`）。

## 4. 核心实现（关键路径的机制拆解）

### 4.1 授权闸门：为什么"消息内容无法改变权限"

gate 是纯函数（`settingsPolicy().gate`，`src/policy.ts:191-211`）：非人消息走 `machineGate`（只允许 bot 列表成员/无 actor 的系统事件，且最高 inferred，`src/policy.ts:171-188`）；人消息先查白名单是否点名（→ explicit），再查准入表三格（listed/unlisted × addressed），最后才是"Thread 上有 Ticket 的 follow-up"（`src/policy.ts:198-210`）。**关键顺序**：explicit 准入格先于 follow-up 判断（`:203-207` 注释即理由——防止线程上的 Ticket 把明确请求降级为 follow-up）。

**替代方案代价**：把授权交给提示词（如"请不要接受越权请求"）成本低但不可证；本项目选择"提示词只影响语义判断，权限由代码强制"（`docs/004:65-73` 五层优先级），代价是 Policy 每次变更都要重算 `policyVersion` 并使运行中的 Eval 作废（`src/core/evals.ts:217-230`），以及 Mandate 的 14 种 basis 分支重验证（`src/policy.ts:213-240`）——复杂度集中在 schema 与重验证，而非提示词。

### 4.2 崩溃一致性：状态与副作用同事务

命令里 `effects.enqueue(...)` 只写行（`src/app/effects.ts:61-66`），执行在 `afterCommit`（`src/app/store.ts` 的 `atomic/afterCommit`，`docs/007:162`）。launch 的"停止旧后台工作 → 启动新 assign"顺序刻意放在事务后（`src/executor/dsh.ts:443-470`，`src/core/tickets.ts:357-363` 的 `afterCommit` 停止）。**为什么**：若在事务内做外部动作，回滚会留下无法撤销的外部副作用（如开了 PR、发了消息）。代价：同一逻辑分成"记录"与"动作"两半，需要 `generation` 字段防止旧尝试覆盖新载荷（`src/app/effects.ts:38-39,130-145`）。

### 4.3 Worker 槽与"人优先"

`WorkerSlots` 在 await 之前同步预留槽位，防止两个启动抢最后一个槽（`src/executor/dsh.ts:166-199`）；`reserve(ticketId,'person')` 允许**超出 maxWorkers 一个槽**（`:192-196`），保证人的消息永远不排队在新工作之后。launch 效果的并发限额取"剩余可用槽"（`:232-233`）。

### 4.4 注意力预算的硬实现

- 主 Session **不允许等待**：`noWait` 守卫拒绝 `sleep`、>30s 的 shell timeout、>5s 的 job wait（`src/app/sessions.ts:77-...`，`docs/007:509-515`）——因为阻塞的一步会延迟所有新候选。
- 回复受目的约束：`Replies` 只允许 ack/answer/result/attention 四类，result 必须 Ticket 处于 ready/completed/merged/dropped（`src/core/replies.ts:69-78`）；ack 幂等（同一 Trigger 只有一条，`:48-63`）。
- 通知去噪：progress report 不转发、attention 立即转发、relay 合并/排序（`src/app/notices.ts:121-129`，`docs/003:42-43`）。

### 4.5 执行恢复：三层事实

1. **Ticket 自己的状态**（不跟随 Session）：`ticketStage` 首匹配行（`src/core/stage.ts:9-21`）。
2. **Assignment 事实**：`deliveredAt`/`idleAt`/`report` 记录"worker 是否已读/是否在忙"（`src/core/model.ts:218-233`，`readUntil` `:341-344`）。
3. **宿主事实**：DSH 的 `agent/status`、`session/event(user/message)`、`agent/error` 事件驱动 `inputsRead`/`turnEnded`/failed（`src/executor/dsh.ts:476-512`）。

restart 时 `DshExecutor.resume()` 由旧到新重放：运行中的 → `assignmentInterrupted`（worker 未收尾则带恢复注记重启，`src/core/assignments.ts:83-92`），pending 且不等人 → 重新 launch（`src/executor/dsh.ts:524-537`）。

### 4.6 提示词装配：可覆盖、可演进、不可越权

系统提示词按固定 8 步顺序装配（`docs/004:46-59`），最后是每次模型请求都重新生成的 Policy 段（`src/app/prompts.ts:92-99`），所以 Policy 变更不改动前缀文本。每个内置 part 保存 `base` 指纹；默认升级时面板显示 "Default updated" 并三选一（`docs/004:40-42`）。**边界**：`prompts/` 只影响模型指令；gate、Mandate、工具参数校验、账号包装仍由代码强制（`docs/004:65-73`）。

## 5. 文档-代码冲突与快照完整性（重要发现）

| # | 冲突/缺口 | 证据 | 判定 |
|---|---|---|---|
| 1 | `src/sources/` 整目录缺失（13 文件：kind/registry/host/poll/github*/feishu*/admission-context） | 缺失 import 清单；`src/app/runtime.ts:18,36,41,42` 等 import | 快照为**裁剪版**（README 自称"adapted for publication"，`README.md:5`）；GodHub/Feishu 实现不可研读 |
| 2 | `README.md:15-17,29,31` 引用 `SETUP.md`、`docs/006-deployment.md`、`docs/008-cookbook.md`；`docs/007:400,532` 引用 `package.json`/`tsdown.config.ts`/`cordis.patch.yml`；`docs/007:402-447` 列出 40+ 测试文件 | 文件缺失 | 同上；架构文档描述的是完整系统 |
| 3 | `docs/001:109` 与 `src/core/model.ts:190` 的 `DecisionKind` 含 `reopen`，但无产生路径 | `grep reopen` 仅迁移相关 | 历史遗留值（迁移后不再产生），不构成行为错误 |
| 4 | `.qoder/repowiki/**`（180 files）描述了完整源码与测试细节 | 已剥离至 strip-manifest | 二手生成物，**不作一手证据** |
| 5 | 文档声称 `pnpm check`（`README.md:35`）但无包清单 | 快照无 `package.json` | 无法复核构建/测试 |

## 6. 证据覆盖表

| 区域 | 文件数 | 已读文件 | 覆盖说明 |
|---|---:|---|---|
| `src/core/` | 15 | 9（model/ports/engine/stage/intake/evals/tickets/part/reasons + assignments/replies 共 11） | 核心 11 个全读；ids/errors/memory/index 为薄文件 |
| `src/app/` | 38 | 12（runtime/effects/outbox/passes/notices/assessment/sessions 关键段/tools×2/store 头部/prompts 关键段/settings 签名） | 视图/迁移/缓存等按其职责一句话覆盖 |
| `src/executor/` | 2 | 2 | 全读 |
| `src/infra/`、`src/client/` | 5 / 27 | 按签名与结构 | 面板为次要组件，按文件职责表覆盖 |
| `docs/`、`prompts/` | 9+15 | docs 000-005,007 全读；prompts 抽样（admission/work/handoff 全读，team/ 读 communication 概要） | — |

**结论**：核心概念、授权、执行、恢复、注意力预算五个主题均以 `文件:行` 级证据闭环；缺失的 `sources/` 实现与测试不在本快照内，相关机制只能以文档 + 消费侧契约描述，已显式标注。
