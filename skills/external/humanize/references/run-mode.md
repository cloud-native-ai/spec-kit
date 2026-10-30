# Run mode — 行为细则（`/speckit.humanize` 的运行模式分支）

**归属**: 本文件是 `skills/external/humanize/SKILL.md` 运行模式分支的行为细则所有者：入口解析、模式路由、迁移提示与派发。报告面（五节、元数据块、证据与来源清单、语言与保真）的所有者是 `references/report-shape.md`；`SKILL.md` 正文只声明分支边界，不复述这里的步骤、字段或字面量。

**外部所有者**: 派发载体的步骤、拓扑声明与快速失败注入子句归 `run-agent` 技能的 Run Mode；`data-model.md` § E2 / § E5 拥有解析字段与信封字段；requirements FR-019 拥有 verdict 集合与映射；requirements § Shared Strings 拥有全部固定 literal。本文件只固定 humanize 侧必须满足的部分，不复制它们。

---

## Parse

入口解析是**纯语法过程**：同样的 argv 得到同样的结果；解析 MUST NOT 读取指令内容来猜测意图，MUST NOT 用「这段文本像内容还是像指令」来决定分支。

1. **选项集**：`--tone`、`--audience`、`--file`、`--inline`、`--output`、`--force`。选项只出现在指令之前。
2. **终止与起点**：`--` 终止选项解析，其后全部逐字进入指令；无 `--` 时，第一个不可识别为选项的 token 即指令起点。
3. **指令逐字**：选项之后的剩余文本整体是**待执行指令**，逐字保留（含换行与引号）；MUST NOT 改写、摘要或规范化它。裸文本 MUST NOT 再被解释为待改写内容——这是 A4 的破坏性变更，迁移方式见 § Migration Hint。
4. **选项语义（沿用 062，不新增取值、不改缺省）**：
   - `--tone`：取值域 `professional` / `humorous` / `empathetic` / `colloquial`；空值、纯空白与集合外取值按 `unknown-tone` 拒绝并列出支持集合。
   - `--audience`：自由文本，只作用于表达层；空字符串或纯空白视为**未提供**（不拒收、不改变表达层缺省）。
   - `--force`：覆盖语义沿用既有契约（目标已存在时需要它）。
   - `--output` 的写入语义按模式分属：内容模式沿用既有契约；运行模式由 FR-024 独占拥有（扩展名封闭集、原子写、会话回显摘要）。
5. **解析结果**：字段集 owner 是 `data-model.md` § E2 —— `tone`、`audience`、`file`、`inline`、`output`、`force`、`instruction_text`、`mode`、`reject_code`。`mode` 只有 `run` / `content` / `reject` 三值；不存在第四种或「模糊」形态。

解析不写任何文件、不派发、不读内容：它只产出一份 E2 结构。

## Mode Routing

判定表是封闭的、按顺序求值，**顺序不可调换**（判据与 `reject_code` 封闭集的 owner 是 `data-model.md` § E2）：

| # | 内容源（`file`/`inline`） | 指令文本 | 判定 |
|---|--------------------------|----------|------|
| 1 | 有 | 非空 | `reject` / `both-sources-and-instruction` |
| 2 | 有 | 空 | `content` |
| 3 | 无 | 非空 | `run` |
| 4 | 无 | 空 | `reject` / `no-input` |

- **两者同现（第 1 行）**：内容源与非空指令同现时 MUST 拒绝并**点名两者**（源名与指令前缀）。MUST NOT 走「内容优先」或「指令优先」的任何猜测分支；该拒绝优先于其他路由判断。
- **空内容源**：内容源自身为空或纯空白时按第 4 行走，拒绝为 `empty-input`——空内容不是内容。MUST NOT 因「有一个内容源参数」而落进内容模式。
- **无输入（第 4 行）**：拒绝消息三项齐全——**用法行**、**支持的内容源**（`--file` / `--inline`）、**迁移提示整句**；MUST NOT 猜测用户意图。
- **拒绝面**：任何拒绝路径 MUST NOT 产生派发、MUST NOT 留下占位、MUST NOT 写入任何文件；拒绝消息 MUST 含原因码对应的点名要素（表 owner 同上，本文件不复述触发条件）。
- **内容模式**：走 `SKILL.md` 的 Stage 1–Stage 7；不派发执行体、不生成动作报告、不读取动作结果、不取得并发占位。

## Migration Hint

迁移提示是**语言不变的固定通知**（与五个英文小节标题同属契约面固定 literal，不随正文语言翻译、不因 `--tone` / `--audience` 改写）。整句原文是：

> 已按指令执行；改写文本请用 --file/--inline

- **触发**：运行模式且调用中**无**任何显式内容源时输出该整句一次；内容模式与拒绝路径不输出该行。
- **落点**：`data-model.md` § E7 `migration_hint`，位于载体标记行之后、五个 H2 之前；MUST NOT 构成第六节；同一运行至多一行。
- **不写文件**：它是调用级会话通知，只在会话回显一次，MUST NOT 写入 `--output` 文件（FR-005 / FR-024）。

## Dispatch

运行模式每次调用 MUST 派发**恰好一个**顶层执行体；一次调用两次派发、或「先试一个再补一个」都判违反。

- **载体**：派发 MUST 经既有 `run-agent` 载体（Run Mode）发起；MUST NOT 引入第二套派发机制、MUST NOT 新建派发脚本、MUST NOT 直接调用某宿主的私有会话 API。
- **执行体**：执行体是**会话级临时执行体**——不写入 `.specify/agents/`、不产生 `.agent.md`、不占 Agent 席位；本次派发不声明 SDD 执行席位；`run-agent` 的「按名解析已存 Agent」分支不适用于本次派发，MUST NOT 因此就在磁盘上创建一个只为本次运行存在的 Agent 定义。若指令本身要启动一次 SDD 运行，那次运行的授权由指令所属单元自己的入口判定，本命令不代替判定。
- **载体模式**：按宿主能力二选一——具备原生派发通道 → `native`；不具备 → `in-session`（会话内执行，不是可选）。`run-agent` 的独立 CLI 进程模式 MUST NOT 被本命令使用：它会带来进程、凭据与网络面。
- **载体标记**：载体标记 MUST 与真实载体一致且恰一个——`native` → `mode: subagent`；`in-session` → `mode: in-session-degraded`。MUST NOT 冒充、MUST NOT 双写、MUST NOT 漏写。降级不得冒充子代理，也不得把会话内执行的推断当作子代理的观测。
