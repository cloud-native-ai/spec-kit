# Outline — 文档清单（stripped/）

## 清点总览

| 类别 | 条目 | 可信度 |
|---|---|---|
| 官方设计文档（按序阅读） | `docs/000`–`007`（006 缺）| 官方（与代码高度自洽，见逐篇注记）；`docs/007` 含少量与快照不符之处 |
| 团队/工作流提示词 | `prompts/` 15 篇 | 官方（运行期系统提示词正文） |
| 启动文案 | `locale/en.json`、`zh.json` | 官方（面板/日志文案） |
| 入口 README | `README.md` | 官方（定位与阅读顺序） |
| 引用但缺失 | `SETUP.md`、`docs/006-deployment.md`、`docs/008-cookbook.md`、`skills/`、`scripts/dsh-superagent`、`src/sources/` | **不可得**（快照缺件；README/007 引用） |

## 逐条主题摘要

| 文档 | 行数 | 主题摘要 | 可信度 | 与代码冲突点 |
|---|---:|---|---|---|
| `README.md` | 39 | 定位：单 GitHub 仓库的主动式编码 Agent、DSH Bundle、可选 Feishu；"研究原型，非官方产品"；阅读顺序；`pnpm check` | 官方 | 引用 `SETUP.md`/`docs/006`/`docs/008`（均缺失） |
| `docs/000-philosophy.md` | 33 | 核心原则"人类注意力最小化、价值最大化"；对 Agent 与设计的推论（少概念、少设置、静默、按影响停止）；运营者责任 | 官方 | 无 |
| `docs/001-domain.md` | 112 | 领域词汇权威：Source/Trigger/Thread/Eval/Mandate/Ticket/Assignment/Subscription/Channel/Policy 的规则与"被拒概念"；术语表（中英）与封闭值集 | 官方 | `Decision` 含 `reopen` 于 `docs/001:109`，代码 `DecisionKind` 亦含（`model.ts:190`），但已无 reopen 路径（仅迁移遗留） |
| `docs/002-authorization.md` | 155 | 授权两路径（Eval gate vs Subscription fan-out）；强度 explicit/inferred；准入表；accept mode off/observe/auto；Policy 版本与 Mandate 重验证；resume/stop | 官方 | 无重大冲突；gate 实现见 `policy.ts:191-211` 与文档一致 |
| `docs/003-execution.md` | 172→203 | Ticket 阶段表（首匹配行胜出）；执行器 Session/目录；后台工作与 worker 槽；prepare 命令；并发；执行变量；合并；Ticket 结束方式；失败与恢复（retry/restart/stored work/source failure/channel failure/pause） | 官方 | 阶段表与 `core/stage.ts:9-21` 逐行对应 |
| `docs/004-prompts.md` | 96 | 团队可编辑三段（Communication/Scope/Delivery）+ skills；内置 part 键；装配顺序（8 步）；优先级 5 层；版本化与冲突 | 官方 | part 键与 `app/prompts.ts:24-26` 一致 |
| `docs/005-panel.md` | 58 | 面板三问、六 Tab、设置组、搜索、七条设计原则 | 官方 | 客户端代码结构一致（client/*.tsx） |
| `docs/007-architecture.md` | 617 | 开发者索引：核心类/Engine 五部件与命令表/Model/Policy/Store/Effects/Sources/DshExecutor/MasterAssessor/Settings/Prompts/Sessions/Glue；依赖规则；模块与测试表；持久化 schema；面向模型的接口；配置重载；开放问题 | 官方（主力文档） | **多处引用缺失物**：`src/sources/*`（13 个文件缺失）、`tests/*`（全部缺失）、`cordis.patch.yml`/`tsdown.config.ts`/`package.json`（缺失）。写作时以代码为准 |
| `prompts/orchestrator.md` | 16 | 主 Session 角色：只路由不决策、路由注记 ≤30 词、不等待 | 官方 | 无 |
| `prompts/worker.md` | 10 | 执行器角色：读原始来源、判断范围、实现与验证 | 官方 | 无 |
| `prompts/shared.md` | 7 | 双角色共享：消息克制、100 词硬限 | 官方 | 无 |
| `prompts/subscriptions.md` | 13 | 订阅扇出语义、上下文只读线程 | 官方 | 无 |
| `prompts/replies.md` | 35 | 回复目的与措辞规则（ack/answer/result/attention） | 官方 | 无 |
| `prompts/dispatch.md` | 59 | 主 Session 路由细则（accept/attach/stop/ignore） | 官方 | 无 |
| `prompts/work.md` | 49 | 执行器工作细则（范围自判、PR 绑定、报告时机） | 官方 | 无 |
| `prompts/admission.md` | 68 | 主动候选评估细则：三事实判定、规则逐条评估、intent_evidence | 官方（`runtime/admission` 唯一来源，`docs/007:600`） | 无 |
| `prompts/handoff*.md`（3 篇） | 6/4/7 | 交接语义（分角色） | 官方 | 极短，可能为占位 |
| `prompts/cli.md` | 17 | CLI 使用约定 | 官方 | 无 |
| `prompts/team/communication.md` | 97 | 团队沟通约定（含 review bot 识别） | 官方（默认值） | 无 |
| `prompts/team/delivery.md` | 28 | 交付要求（证据、自动合并阈值 200 行、作者） | 官方（默认值） | 与 `docs/003:88` 一致 |
| `prompts/team/scope.md` | 22 | 工单范围判定 | 官方（默认值） | 无 |
| `locale/en.json`,`zh.json` | 6+6 | 启动等待文案 | 官方 | 无 |
| `.qoder/repowiki/**`（已剥离，180 files） | — | Qoder 自动生成的二手知识树与"使用文档" | 生成物/二手 | 与 `src/sources` 缺失事实矛盾（描述了大量 GitHub/Feishu 细节）——仅作交叉参考 |

## 文档-代码交叉验证提示（供 Step 4）

1. **快照完整性**：`docs/007` 的模块表列出 `src/sources/*`、`tests/*`、构建文件；这些在快照中全部缺失。判定：代码快照不完整（或为对外发布版裁剪），文档描述的是完整系统。
2. **`docs/001` 的 `reopen` Decision**：代码 `DecisionKind` 仍含 `reopen`，但 `grep` 未见产生路径，仅迁移相关（`app/migration.ts`）；与"被拒概念"（`docs/001:45-60`）中"append to Ticket"的拒绝逻辑一致——历史遗留值。
3. **`docs/003` 阶段表** 与 `core/stage.ts` 完全同构，可信度最高。
4. **`docs/002` 授权表** 与 `policy.ts` 的 `gate()`/`revalidate()` 可逐条对应（如 explicit 优先于 follow-up 的判断在 `policy.ts:203-207`）。
