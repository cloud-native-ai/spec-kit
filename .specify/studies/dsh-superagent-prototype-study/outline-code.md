# Outline — 代码清单（stripped/）

## 总述

这是一个从 DeepSeek 内部工作流生长出的 **TypeScript 研究原型**：把"主动式编码 Agent"打包为 DeepSeek Harness（DSH，Cordis 插件体系）的 Bundle。全部为 TypeScript / TSX，无构建产物、无包清单（由宿主提供依赖，见 `docs/007` 与 `.qoder` 生成知识树之"无包清单的 DSH Cordis 插件"条目，后者已剥离）。代码按"领域内核（core）—应用编排（app）—执行器（executor）—基础设施（infra）—管理面板（client）"分区；`src/sources/`（GitHub/Feishu 适配器）在本快照中缺失（见 strip-manifest 与 deep-study § 冲突记录）。

## 目录树（剥离去噪后）

```
stripped/
├── README.md                 39 行
├── docs/                    各篇设计文档 000–007（缺 006-deployment）
├── prompts/                 15 个角色/工作流提示词文档
├── locale/                  en.json / zh.json（启动文案）
└── src/   (120 files, ≈13.5k lines)
    ├── index.ts             插件入口（27 行）
    ├── deployment.ts        Config/Machine/账号探测（131 行）
    ├── setup.ts             SetupError 目录（39 行）
    ├── policy.ts            Zod 设置 schema + gate/revalidate/评估转换（242 行）
    ├── core/    15 files, 2,088 行   ← 纯领域内核，零 I/O
    ├── app/     38 files, 5,292 行   ← 编排/胶水（含 views/、tools/）
    ├── executor/ 2 files,  838 行   ← DshExecutor + 后台工作
    ├── infra/    5 files,  347 行   ← CLI 传输/健康/文本/环境
    └── client/  27 files, 4,419 行   ← React 管理面板（含 382 行 CSS）
```

## 语言与规模

| 语言 | 文件数 | 行数（估） | 说明 |
|---|---:|---:|---|
| TypeScript `.ts` | 76 | ≈9,100 | 服务端逻辑主体 |
| TypeScript `.tsx` | 18 | ≈3,200 | 面板 React 组件 |
| Markdown `.md` | 23 | ≈1,700 | 设计文档 + 提示词 |
| JSON | 2 | 12 | locale |
| CSS | 1 | 382 | 面板样式 |

（`.ts`/`.tsx` 行数由按目录汇总推算，含 client 4,419 与 core 2,088 等实测值。）

## 按目录的文件清单（摘要）

### `src/core/` — 领域内核（无 I/O）
| 文件 | 行 | 角色 |
|---|---:|---|
| model.ts | 353 | 全部领域类型与不变量谓词（Trigger/Thread/Ticket/Mandate/…） |
| engine.ts | 270 | 唯一写入口 + 角色化 `Pick` 接口 |
| tickets.ts | 423 | Ticket 生命周期、订阅、Inputs、resume/retry/stop/end |
| evals.ts | 340 | 线程级评估、批处理、Decision |
| assignments.ts | 140 | 执行器事实与 Worker Report |
| ports.ts | 134 | Repositories / Policy / SourceScope / Assessor / Executor / Outbox / 领域事件 |
| replies.ts | 95 | Channel 写入规则（ack/answer/result/attention） |
| model/intake/part/stage/errors/reasons/ids/memory/index | 共 ~330 | 摄入、基类、阶段、错误码、原因码、id 派生、内存仓储 |

### `src/app/` — 应用编排
| 文件组 | 行（合计） | 角色 |
|---|---:|---|
| runtime.ts | 254 | 组合根：装配全部组件、加锁、启动/关闭 |
| effects.ts | 161 | 持久化副作用队列（6 种 kind） |
| store.ts / store-read.ts / migration.ts / versions.ts / cache.ts | 616+81+616+34+27 | SQLite（node:sqlite）仓储、只读查询、schema 11 迁移、版本化快照、LRU 文本缓存 |
| settings.ts / settings-history.ts / prompts.ts | 267+91+247 | 版本化设置、Policy 版本效果、提示词装配（内置 15 个可覆盖 part） |
| assessment.ts | 282 | MasterAssessor：候选卡片投递、受限上下文读取、评估→决定 |
| sessions.ts | 352 | DSH Session 管理（主 Session/worker、preset、noWait 守卫） |
| notices.ts / outbox.ts / passes.ts / delivery.ts / retry-health.ts / role-models.ts | 129+52+69+86+91+44 | 通知/中继、Outbox 收据、2s pass 调度、幂等投递、模型预算重试、角色模型 |
| cards.ts / links.ts / resources.ts / execution-environment.ts / source-context.ts / context.ts / skill-files.ts | 96+71+308+46+72+33+32 | 卡片/链接/资源读/执行环境/源上下文/内置提示词文本 |
| tools/main.ts / tools/executor.ts / tools/tool.ts | 301+105+35 | 主 Session 14 工具、执行器 6 工具、read 工具基座 |
| http.ts / api.ts / views/*.ts（6 个） | 247+52+≈460 | 管理 HTTP 路由、路由类型契约、面板视图投影 |
| setup.ts | 99 | 启动探测与问题目录 |

### `src/executor/`
| 文件 | 行 | 角色 |
|---|---:|---|
| dsh.ts | 673 | 每 Ticket 一个 worker Session+目录；launch/delivery 效果；WorkerSlots；瞬态重试；恢复 |
| background.ts | 165 | worker 后台 shell jobs / subagents 的等待、杀死、释放 |

### `src/infra/`
| 文件 | 行 | 角色 |
|---|---:|---|
| commands.ts | 115 | CLI 传输（gh/lark/git），错误码携带、非法条目跳过计数 |
| environment.ts | 157 | 进程环境、命令 shim、runAsWorker、目录校验 |
| health.ts / paths.ts / text.ts | 35+20+20 | HealthBoard、包根路径、字数限制 |

### `src/client/` — React 面板（27 files）
入口 `index.tsx`；`app.tsx` 框架 + 按阶段页（source/trigger/eval/execution）+ 记录页（thread/ticket）+ 设置页（settings/prompts/deployment）；`locales.ts` 双语全量文案（770 行）；`controls.tsx` 本地控件复刻；`client.css` 382 行。

### `docs/` `prompts/` `locale/`
`docs/000–007`（006-deployment 缺）逐篇累进；`prompts/` 含角色（orchestrator/worker）、工作流（dispatch/work/subscriptions/replies/admission/handoff*）与团队约定（team/*）；locale 仅有两条启动状态文案。

## 入口点候选

| 入口 | 位置 | 性质 |
|---|---|---|
| 插件入口 | `src/index.ts:10` `export async function apply(ctx, config)` | Cordis 插件 `apply`，注入 11 个宿主服务 |
| 面板入口 | `src/client/index.tsx` | DSH Web 客户端插件 |
| 组合根 | `src/app/runtime.ts:59` `class Runtime` | 服务注册名 `orchestrator`（`super(ctx,'orchestrator')`） |
| 领域入口 | `src/core/engine.ts:24` `class Engine` | 唯一写入口 `receive/decide/attach/...` |
| 源插件契约 | `src/sources/host.ts` `SourceHost`/`SourceContext`（文件缺失，接口被多处 import） | 外部插件经 Cordis 服务 `orchestrator` 注入 |

## 模块边界初判

- **core 不 import core 之外**（仅 Node hashing），无 I/O —— 由 `docs/007:256-259` 声明，且 `src/core/*` 的 import 实测一致。
- **app 依赖 core + infra + sources 类型**；executor 依赖 app（Effects/Sessions）与 core 类型；client 只 import 类型与少量纯值模块（`docs/007:258`）。
- **sources/ 是双向边界**：宿主向源提供 `SourceContext`，源向宿主提供 `SourceKind`；本快照缺失该目录，但 `app/` 侧契约（类型 import）完整保留。
- **prompts/ 与 locale/ 是文案资产**，运行期由 `app/skill-files.ts` 的 `promptFile` 读入并拼为系统提示词段落（`docs/007:600`）。
