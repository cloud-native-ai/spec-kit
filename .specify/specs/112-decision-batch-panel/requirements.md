# Requirements Specification: Batch Decision Panel — 待决策项集中决策（Batch Decision Panel）

**Requirement Branch**: `112-decision-batch-panel`
**Created**: 2026-11-27
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（需要判定每个待决策项从哪个既有载体被聚合、建议默认值依据哪条既往证据、一次批次处置落到哪里、如何只凭记录重放审计的人）与项目所有者（面对一批未决事项，希望一次看完完整信息、只对有异议的项发声、其余按建议默认值结案的人）；读者基准沿用 `.specify/shared/guidelines/user-facing-comprehension.md` 的全局基准读者，不新建
**Reading scenario**: 当需要判定「哪些未决事项算待决策项、来自哪些既有载体」「一次批次如何做到完备（没有静默遗漏、不可读载体如何拒绝）」「建议默认值从哪里来、没有证据时说什么」「用户只提异议时其余项如何结案、沉默何时等于接受」「处置写入哪些既有载体、如何只凭记录重放一次批次」「人工决策与 AI 自主决策的边界在哪里」时打开本规格，据 FR-001…FR-045 与 SC-001…SC-010 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "整个决策管理机制应该能做到: 汇总一下所有的待决策项集中进行决策, 决策项需要使用完整信息呈现, 每个决策项都需要根据之前的经验给出一个合理的建议作为默认选项, 在决策时我只针对有异议的选项提出, 其他选项都使用建议的默认值."

**输入校正（本阶段裁定，详见 Assumptions）**：

- 「待决策项」= 封闭来源清单中的**未决决策项**：`.specify/register.md` 中状态为 open 的 OI- / D- 族行，与既有载体内按「待决策项块」形态撰写的条目；不是全部 TODO、parked idea 或澄清标记（A-3）。
- 「完整信息」= 107 既有 `human-interactive` 呈现模板的全部要素（主体完整名称、同名定位、上下文、封闭选项集与每项后果/可逆性/默认/证据），加建议依据与来源指针；信息不完整时如实标为未决，MUST NOT 补造（A-16）。
- 「根据之前的经验给出合理的建议」= 项自带的默认选项加上对封闭既往证据清单的确定性接地；没有可用既往证据时明写 `no-evidence`，绝不发明偏好（A-6）。
- 「其他选项都使用建议的默认值」= 未被点名的**合格项**采用其默认选项；沉默只在一次已获用户应答的交互式批次内、且默认选项可逆时才算接受；不可逆默认、无默认项与前例冲突项必须显式选择（A-9、A-10）。
- 「决策管理机制」= 扩展现有 107 所有者页；不新建第二登记、存储或决策 schema；不与 ai-harness 091 对齐（A-2、A-4）。

## Related Feature *(mandatory)*

**Feature ID**: 112
**Feature Name**: Batch Decision Panel（批量决策面板）
**Binding basis**: 这是一个**新的独立特性**，只对 Feature 107 Decision Governance 的既有所有者页做加法式扩展，不新建第二个所有者页。候选复用扫描：Feature 107 拥有决策词汇、两类模板、选项集契约、记录文法、生产者清单与传递义务，但**没有任何聚合或呈现面**；Feature 020 todo 拥有的是 parked idea 队列（不是决策项）；Feature 058 sdd-loop-driver 拥有阶段检查点（其决策多为 `ai-autonomous`）；Feature 027/028 feedback 拥有反馈条目与门控观察族（不是决策记录载体）；Feature 102 拥有 line 登记（不是决策面）。没有任何候选拥有「批量决策面板」能力，且 107 的唯一 sibling 规格集中不含批量决策规格，绑定先例指向 create。本阶段按 Feature Integration Protocol 登记 `.specify/features.md` 行与 `.specify/features/112-decision-batch-panel.md` 详情（`Draft`）；`.specify/register.md` 与状态脊在本阶段不被编辑（A-2）。

## Overview

**问题**：107 已把「一个决策项」的文本、选项集、记录、归档投影、传递与回执都规定清楚了，但决策仍然**一次只来一个**：确认门在会话中当场发问；无人值守运行遇到人持有的决策时停在一个问题上；打开的事项（OI 行）静默躺在 register 里等某个未来回合。框架因此缺一个面，同时暴露三种失效：

- **单题打断**：用户没有一次看到全部未决事项的机会，只能被逐题召回；
- **建议不可追溯**：「建议默认值」若由各生产者随手填写，事后无法回答它依据哪条既往证据；
- **沉默无定义**：用户未回答的项，到底是「未指定」还是「接受默认」，今天没有契约。

**本特性交付**：**批量决策面板（Batch Decision Panel）**——一次调用把封闭来源清单中的全部未决决策项汇总为**一次呈现**：

1. **聚合**：按封闭来源清单扫描既有载体（register 的 open 行 + 既有载体中的待决策项块），按身份合并重复引用，做到一项一行。
2. **完整信息**：每项按 107 的 `human-interactive` 模板呈现（主体完整名称、同名定位、上下文、封闭选项集与五要素、唯一默认、证据/定位器），加来源指针、建议依据与接地状态、资格状态与原因、异议方式。
3. **建议默认值**：默认选项取自项自身的 107 声明；接地来自对封闭既往证据集的确定性联接（默认选项的可解析证据指针、主体全名逐字命中的既往决策记录及其引用的 `T-NNN`）；无证据时明写 `no-evidence`，绝不发明偏好。
4. **异议式交互**：用户只点名有异议的项（改选具名选项或暂缓）；其余**合格项**按建议默认值结案；不可逆默认、无默认项、来源冲突项与前例冲突项必须显式选择。
5. **落盘**：每批次写一份**批次记录**（既有 knowledge 存储中的一条日期化记录，经既有记忆引擎写入），内含完整性记账、逐项行与已决项的 `D-NNN` 决策记录；register 登记批次与决策编号并更新已决 OI 行的状态；待决策项块补记 `resolution`。
6. **可审计可重放**：批次记录 + 可解析指针即可重放整批（项集、完整性、默认值、异议、处置、记录），不依赖对话记忆。
7. **边界**：只服务人持有的决策；`ai-autonomous` 决策保持其谓词驱动路径，永不被呈现或静默转换；无人值守运行不得记录「沉默接受」；零网络、零自动传输。

**实测基线（2026-11-27，base `c3489e52c`，本 worktree 可复现）**：`.specify/register.md` 含状态为 open 的 OI- / D- 族行八条（OI-3、OI-4、OI-7、OI-9、OI-069b-01、OI-073-01、OI-082-01、D-2 (092)）；四个扫描根（`.specify/specs/`、`.specify/goals/`、`.specify/anchoring/`、`.specify/teams/`）中 `### PENDING —` 块为零；107 所有者页的生产者清单止于 P-12，无批次生产者；`templates/commands/` 与技能树中没有 decide 入口。这些读数在实现期可复测；首轮批次的真实形态因此是「八条 open 行为 `incomplete`、零项可批量结案」，这正是完整信息披露的诚实起点（A-16）。

**不做什么**：不新建第二套决策登记、队列、存储或调度器；不新增共享可变聚合；不把决策记录迁出既有载体；不发明缺失的选项或默认值；不替生产者撰写待决策项（A-16）；不对 `ai-autonomous` 决策做批量接受；不做调度、通知、守护进程或仪表盘；不做任何跨仓对齐或自动传输。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **Flow Class = `execution`**：交付物是所有者页扩展、命令模板、技能、确定性引擎与守卫；缺陷只在解析、断言或执行时暴露。`Flow Type` 写 `-`。四元组 `flow_class=execution; source=default; marker=; error=owner-unavailable` 记录于本阶段派发。 | 按验收 oracle 判定，而非按文本介质（`shared/declarations/facts/flow-class-basis.yaml`）。 |
| **A-2** | **特性身份 = 新 Feature 112**，独立特性，不是 107 的切片；**只扩展 107 所有者页**（`shared/definitions/decision-definitions.md`），不新建第二个所有者页。本阶段登记 `.specify/features.md` 行与 `.specify/features/112-decision-batch-panel.md`（`Draft`）；`.specify/register.md`、状态脊与主树在本阶段不被编辑；本阶段不铸造 `D-`/`OI-` 编号（运行期的编号由机制在使用时按 107 规则登记）。 | 107 所有者已拥有决策词汇与记录契约；批量面板是它的加法式能力面，第二所有者会制造第二定义点。 |
| **A-3** | **待决策项来源清单封闭（歧义 #1）**：恰两个来源——`register-open-decision-row`（register 中去皮 markdown 强调后状态以 `open` 开头的 OI- 族与 D- 族行）与 `authored-pending-item`（四个封闭扫描根中的 `### PENDING —` 块）。排除项各有理由：已触发的交互门（当场提问，不跨调用挂起）、澄清标记（归 `/speckit.clarify`）、parked idea（不是决策项）、`ai-autonomous` 检查点（不属人持有）。来源增删 MUST 以所有者页修订进行，MUST NOT 静默增加第三来源。 | 让「所有待决策项」成为可判定命题；只纳入既有可能承载完整选项集的载体。 |
| **A-4** | **待决策项形态与去重（歧义 #1 续）**：待决策项以独立的 `### PENDING —` 块语法撰写（字段见 § Pending Item Block），与 `### D-NNN` 记录语法**互不判定**；身份 = 主体完整名称 + （同名时的）定位信息，重复引用按身份合并为一行并列出全部来源，同身份但选项标签集不同时一行呈现并标 `source-conflict`、要求显式选择；不做模糊标题合并。register 行的完整信息必须在其**显式**权威路径上解析到待决策项块；`同上` 一类相对表述不解析，该项成为 `incomplete`。 | 批量结案需要机器可核对默认项与具名选项；身份合并只做字面可判定的联接，宁可不合并也不误合并。 |
| **A-5** | **入口面 = 新命令 `/speckit.decide`（歧义 #2）**：薄入口模板 `templates/commands/decide.md` + 内部技能 `skills/internal/decide-batch/SKILL.md` + 确定性引擎 `scripts/python/decision-batch.py`（封闭动作 `scan` / `record` / `replay`）。命名依据：既有命令族以单词动词/名词为入口（`clarify`、`review`、`analyze`、`status`、`measure`），无任何既有命令承担「决策裁决」；技能名沿用 `<动词>-<对象>` 兄弟形（`clarify-artifact`、`review-feature-quality`）。 | Grounded Naming + 同型兄弟模仿；把交互留给技能、把固定规则判断交给引擎（Program-First）。 |
| **A-6** | **默认值与接地（歧义 #3）**：建议默认值 = 项自身声明的**唯一**默认选项（107 选项集契约），面板 MUST NOT 发明默认值或选项。接地 = 对封闭既往证据集的**确定性联接**：①默认选项的 `evidence` 指针中可解析到既往经验载体者；②既往决策记录中 `context` 值**逐字包含**项主体全名字符串者；③这些记录引用的 `T-NNN`。既往经验载体闭集：决策记录载体（四个扫描根 + 批次记录）、`T-NNN` 张力记录、`.specify/history/` 条目、`.specify/feedback/` 条目、`.specify/knowledge/` 条目。至少一条可解析的既往经验指针 → `grounded`；否则 `no-evidence`（明示）。`basis` 是作者撰写的一行理由，本身不是证据，依据必须落到可解析指针。面板不得在呈现期用 LLM 语义检索补造接地。 | 「根据之前的经验」必须可追溯；确定性字面联接避免编造，同时保留一个诚实的 `no-evidence` 出口。 |
| **A-7** | **重决走既有取代规则（歧义 #4）**：异议若推翻一条既往决策，MUST 走 107 的取代规则——新增一条记录，旧记录以 `superseded_by` 指向新记录并**保留**，MUST NOT 删除或改写旧记录；旧记录载体不可写时拒绝重决，不得降级为「全新决策」。异议前，主体命中的既往记录若选择了不同选项，该项标 `prior-decision-conflict`，不得经沉默结案。 | 单一定义点与审计链：重决是新记录，不是覆盖。 |
| **A-8** | **批次完备性（歧义 #5）**：完备性是封闭清单断言——来源清单、每来源候选计数、逐候选处置分类与「扫描 = 呈现 + 合并引用 + 具名排除」的记账恒等式；断言形状遵循 `shared/guidelines/closed-set-claims.md`（参照物 = 本次扫描；比较单元 = 逐候选处置；允许差集恒为空）。任一载体**存在但不可读/不可解析** → 拒绝（不呈现、不记录、具名退出）；来源**缺席**（文件/目录不存在）→ 记为带原因的缺席空来源，不拒绝；批次绝不把部分结果标为完备。零待决策项 → 显式 `nothing-pending`。 | 完备性必须可判定；「静默漏掉一项」是批量决策最危险的失效。 |
| **A-9** | **常设默认值 = 无（歧义 #6）**：默认值只在**单次批次**内有效；MUST NOT 预授权未来同类项、MUST NOT 记忆用户偏好并自动套用；每次批次重新呈现并等待用户应答。 | 预授权会跨时间静默自动裁决，并制造第二份决策记忆；用户始终是裁决者。 |
| **A-10** | **沉默语义（承重决策，按 `shared/guidelines/decision-tension.md` 形态记录）**：**decision**：允许「沉默 = 接受默认」，但仅限交互式批次中、用户已作出应答、且默认选项可逆的合格项。**antithesis**：逐项显式确认——每项都必须被回答；当用户只对少数项有异议且信任建议时它更优（零误接受风险，且不需要「沉默」语义）。**binding_constraints**：pole_a 用户只愿处理异议，否则批量失去意义；pole_b 破坏性/不可逆动作必须显式确认（`shared/guidelines/confirmation-gates.md` 的两级判据）。**discriminating_evidence**：对一批同时含可逆默认与不可逆默认的夹具作零异议应答，观察是否只有可逆项记为 `accepted-default`、不可逆项保持待定；结果二值。**expected_sacrifice**：用户少读文本的代价是一项被误建议且未被细看即被接受；缓解 = 接地指针可解析 + 无证据明示 + 可逆性限制 + 事后重决留痕；反指标 = 被用户事后推翻的 `accepted-default` 项数（可由批次记录与后续取代记录读出）。**revision_trigger**：出现一例「沉默接受后用户明确否定且无法经重决修复」→ 重开，收紧为逐项确认或取消沉默规则。 | 用户原话要求「只针对有异议的选项提出」；把这条要求落成可判定规则必须同时守住既有确认门对不可逆动作的显式确认义务。 |
| **A-11** | **批次记录载体 = knowledge 存储中的一条日期化记录**（经既有记忆引擎写入，一文件一批次，标题携带批次编号，永不覆盖）：不是 feedback 存储（反馈计数与阈值提示会被污染），不是 session 存储（可遗忘层，不承载终态审计），不是 register 本身（register 只是编号索引）；不新建存储根。该选择复用记忆系统「lasting decisions（持久决策）」的既有定位与一文件一记录的并发安全布局。 | 「落进既有载体」且「无第二存储」；在既有存储中选语义最贴近、并发最安全的一个。 |
| **A-12** | **批次族记录字段 = 所有者页条件层加法**：仅当记录由批次产生时，追加 `batch_id` / `batch_disposition` / `recommendation_grounding` 三个条件层字段；既有记录（含本特性落地前的记录）语法不变、零改写、继续按 legacy/现行规则读取。字段闭集只能在所有者页修订，MUST NOT 在引擎常量或文档里另开第二套字段表。 | 审计需要区分「批次隐式接受」与「显式选择」；加法式条件层是 107 已声明字段闭集的唯一修订路径。 |
| **A-13** | **人工 / 自主边界**：面板只呈现 `human-interactive` 项；`ai-autonomous` 项（含类缺失项）永不呈现、永不转换、永不被默认值授权；无人值守调用可以扫描但 MUST NOT 记录接受，必须给出具名拒绝。 | 用户仍在场才存在「沉默」；把自主决策混入人类默认会静默改变其持有者。 |
| **A-14** | **语言与读者**：正文以中文为主、核心概念带双语定义（与 109/107 一致）；所有面向用户的呈现沿用全局读者基准与行话白名单（`shared/guidelines/user-facing-comprehension.md`），不新建读者层。 | 最新合并规格的语言惯例 + 用户可理解性纪律。 |
| **A-15** | **落地与分发**：所有者页扩展、命令模板、技能、引擎全部落在框架源（`shared/`、`templates/`、`skills/`、`scripts/`），经既有镜像对投影并由 `specify init` 分发；每工具命令副本经既有再生成器更新；**冻结的命令/技能名基线测试同批扩表**（新增命令与技能必须与基线同批移动）；框架地图的决策治理行更新为含批次能力与 P-13、consumer 增补；**不改** `.specify/instructions.md` 的 `## Decision Items` 段（实测 1,276 B / 声明上限 1,500 B，余量不用于新句；发现性由命令模板、命令文档与框架地图承载）；**不改** `.specify/.gitignore` 与运行期存储布局（无新运行期目录）。 | publish → install → init 是唯一分发路径；冻结基线同批移动是既有库存封闭纪律；指令段预算不挪用。 |
| **A-16** | **存量未决项不自动补全**：现有 open OI 行大多没有待决策项块，它们以 `incomplete` 呈现并逐项点名缺失要素；撰写缺失要素是生产者/用户的义务，不是面板的职责——面板发明选项或默认值就等于制造它本应中立呈现的决策内容。`incomplete` 是合法的呈现状态，不是缺陷。 | 完整信息的诚实边界：宁可不结案，也不编造。 |
| **A-17** | **排除范围**：调度器、提醒/通知、常驻扫描、UI/仪表盘、自动撰写待决策项、`ai-autonomous` 批量裁决、跨批次常设默认、任何第二存储/schema、与 ai-harness 091 的对齐、任何网络或自动传输——全部不属于本特性（详见 § Out of Scope）。 | 宪法 IX（框架不是运行平台）与 brief 的约束。 |
| **A-18** | **词汇表提案只提议不写入**：本特性引入的新词（Decision Batch、Batch Record、Pending Decision Item、Recommended Default、Recommendation Grounding、Acceptance by Silence）按其 owner 页定义并带双语形态；`.specify/glossary.md` 的实际写入遵循既有 glossary 协议（`origin=auto`、`status=proposed`），未获用户确认前不直接写入。 | glossary 冲突与用户优先规则；无人值守运行不因等待确认而阻塞。 |
| **A-19** | **脚手架偏差（披露）**：当前工作树已在分支 `112-decision-batch-panel`；`create-new-requirements.sh` 会把该分支计入编号空间并派生 113 且新建分支，与本线「停留在既有分支、编号 112」冲突。按 107/109/110 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到本目录，脚本的模板拷贝步骤等价复刻，仅跳过其编号派生与建分支步骤。 | 工作树拓扑与脚本编号派生假设不兼容；照抄会制造第二分支并改号。 |
| **A-20** | **本阶段边界**：只提交本特性产物；不 push；不编辑状态脊与 `.specify/register.md`；不触碰主树；最后动作是提交本阶段全部产物（制品提交 + 记录提交）。 | 无人值守纪律与本阶段 brief；提交纪律沿用 110 的 close-out 形态。 |

## Pending-Source Roster (closed; dated declaration)

本表是 requirements 阶段的**日期化声明**；实现后含义与清单归所有者页（FR-001），本表不构成第二定义点。

| 来源 id | 既有载体 | 机器可检谓词 | 类别 | 判定为待决策项的条件 |
|---------|----------|--------------|------|----------------------|
| `register-open-decision-row` | `.specify/register.md`（表格行） | 行 id 族为 OI- 或 D-，且状态单元格去掉 markdown 强调与前导空白后以 `open` 为起始词 | 由权威路径上的待决策项块声明 | 权威路径为**显式**仓库路径，且其载体中存在与主体一致的 `### PENDING —` 块并声明 `human-interactive` |
| `authored-pending-item` | 四个封闭扫描根下的 tracked Markdown 载体：`.specify/specs/`、`.specify/goals/`、`.specify/anchoring/`、`.specify/teams/` | 存在标题前缀为 `### PENDING —` 的块（围栏代码块内不计） | 块内 `decision_class` 字段 | 块字段齐备且 `decision_class: human-interactive` |

**排除族（具名理由，计入记账）**：已触发的交互门（当场问答，不跨调用挂起）；澄清标记（`/speckit.clarify` 拥有）；parked idea（`.specify/todo/`，想法队列不是决策项）；`ai-autonomous` 检查点裁决（不属人持有）；`REC-` 行（建议是决策的输入，不是决策项）；已在先前批次解决的身份（FR-012）。

**来源在场读数**：`read`（成功读取）/ `absent`（载体不存在，记为带原因的缺席空来源）/ `unreadable`（存在但不可读或不可解析 → 触发拒绝，FR-016）。

## Pending Item Block (closed; dated declaration)

待决策项块**不是决策记录**：它没有 `chosen_option`，也不被记录文法检查；记录文法 MUST NOT 把待决策项块判为不完整记录，待决策项块检查 MUST NOT 判记录。

- 标题：`### PENDING — <标题>`（占位为完整名称；围栏代码块内不计）。
- 字段行：`- **<小写字段名>**: <值>`；续行缩进 ≥2 空格。
- 字段闭集：

| 字段 | 层级 | 含义 |
|------|------|------|
| `decision_class` | 必填 | 闭集 `human-interactive` / `ai-autonomous`；批量面板只呈现前者 |
| `subject` | 必填 | 决策主体的完整名称（107 文本契约 R1） |
| `same_name_conflict` / `resource_locator` | 条件（同名族） | 同名冲突风险存在时必须成对在场；定位维度下限沿用 107 规则 |
| `context` | 必填 | 决策所处情境与约束（含为何此刻要选） |
| `options` | 必填 | 声明计数开头；每个选项五要素（label / consequences / reversibility / default / evidence）；恰一个 `default: yes`；`other` 的 `path` 与单可行项的 `forced` 规则沿用 107 选项集契约 |
| `basis` | 必填 | 建议默认值的一行理由；本身不是证据，依据必须由可解析指针承载 |
| `origin` | 必填 | 该待决策项的产出身份（生产者/载体/行或锚），用于审计与去重回指 |
| `created_at` | 必填 | ISO-8601 UTC 创建时点 |
| `resolution` | 条件（解决族） | 解决后追加：`<batch_id> -> <D-NNN>`；块内容不因解决而改写 |

**不完整判定**：任一必填字段缺失、选项五要素缺失、默认项不是恰一个、`evidence` 指针不可解析、`subject` 不是完整名称形态可判部分——记为 `incomplete` 并逐项点名缺失要素；不完整项不进入「沉默接受」资格，但仍被完整呈现其现有内容与缺失清单。

## Batch States and Batch Family Fields (closed; dated declaration)

**呈现行的资格状态（闭集）**：`eligible` / `incomplete` / `no-default` / `irreversible-default` / `source-conflict` / `prior-decision-conflict`。只有 `eligible` 项可经沉默结案。

**排除状态（不呈现，计入记账）**：`not-human-held` / `already-resolved` / `duplicate-merged`。

**处置（闭集）**：`accepted-default`（沉默接受默认）/ `objected-alternative`（异议改选具名选项）/ `objected-parked`（异议暂缓）。

**接地状态（闭集）**：`grounded` / `no-evidence`。

**批次族记录字段（107 条件层加法，仅批次产生的记录携带）**：

| 字段 | 含义 |
|------|------|
| `batch_id` | 产生该记录的批次编号；解析到批次记录载体 |
| `batch_disposition` | 该记录对应的处置：`accepted-default` / `objected-alternative` |
| `recommendation_grounding` | 该记录采用的默认值接地：`grounded` / `no-evidence` |

**批次编号**：`B-<YYYYMMDDTHHMMSSZ>-<8 位小写十六进制>`；时间戳为 UTC，后缀保证两个并发批次不共享路径；批次编号在诞生时登记于 register（与决策编号同批）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次集中呈现全部待决策项，每项完整、可比较、带建议默认值 (Priority: P1)

一个项目所有者打开批量决策面板：封闭来源清单中的每个待决策项恰好出现一次，按确定顺序排列。每项给出主体完整名称与（必要时）同名定位、上下文、封闭选项集与每项后果/可逆性/默认/证据、来源指针、建议默认值与其接地状态（`grounded` 带可解析既往证据指针，或明写 `no-evidence`）、资格状态与原因、以及异议方式。信息不完整的项也出现，但明确列出缺失要素且标为不可结案。`ai-autonomous` 项不出现，但在记账中带理由计数。重复引用合并为一行并列出全部来源。同一输入重复扫描得到同一项集与同一顺序。

**Why this priority**: 没有「一次看完、每项完整、建议有据」的呈现，后面的异议交互与记录都无从谈起；这是用户原话的直接落点。

**Independent Test**: 一个覆盖两个来源、重复引用、不完整项与 `ai-autonomous` 项的 fixture 产出预期呈现行；连续两次扫描除时间戳外逐字段一致；篡改一项的默认标记后复核转红。

**Acceptance Scenarios**:

1. **Given** 一个 register open 行与一个待决策项块，**When** 面板扫描，**Then** 两者按身份各出现一次，每项携带 107 `human-interactive` 模板全部要素、来源指针、接地状态与资格状态。
2. **Given** 两条 register 行指向同一个待决策项块，**When** 面板扫描，**Then** 它们合并为一行并列出两条来源引用；不按标题做模糊合并。
3. **Given** 一个 `ai-autonomous` 待决策项块，**When** 面板扫描，**Then** 它不出现在呈现中，且记账中有一行 `not-human-held` 排除。
4. **Given** 一个缺选项集的 open register 行，**When** 面板扫描，**Then** 它以 `incomplete` 出现并点名缺失要素，不进入沉默接受资格。
5. **Given** 同一输入重复扫描，**Then** 项集、顺序与逐项内容相同（扫描时间戳除外）。

---

### User Story 2 - 只对异议发声，其余合格项按建议默认值结案，不合格项不被吞 (Priority: P1)

用户读到批次呈现后，只回复有异议的项：有的改选另一个具名选项，有的说「这项先放着」。其余**合格项**按建议默认值结案。不可逆的默认值、没有默认值的项、来源冲突项与前例冲突项即使未被点名也不会被结案，而是保持待定并在收尾中说明原因。用户若回复「无异议」，全部合格项按默认值结案。用户若中止会话，不写任何处置。

**Why this priority**: 这是用户原话的操作核心；沉默语义若判错，会把「没看到」误当成「同意」。

**Independent Test**: 一个含可逆默认、不可逆默认、无默认、前例冲突四项的 fixture，用「仅异议一项」的应答记录批次，断言恰好一项 `objected-alternative`、可逆默认项 `accepted-default`、其余三项保持待定且各有具名原因；再用零异议应答与中止会话各跑一次，断言全合格项结案与零记录两种结果。

**Acceptance Scenarios**:

1. **Given** 四项合格性与默认值不同的待决策项，**When** 用户只对一项提出改选，**Then** 该项记 `objected-alternative`，其余 `eligible` 项记 `accepted-default`，不合格项保持待定并各有原因。
2. **Given** 默认选项为不可逆的项，**When** 用户未点名它，**Then** 它不被结案，呈现中明确要求显式选择（确认门对不可逆动作的显式确认义务不被批量规则绕过）。
3. **Given** 用户回复「无异议」，**When** 批次记录，**Then** 全部 `eligible` 项记 `accepted-default`；不合格项仍保持待定。
4. **Given** 用户中止会话（无可记录的应答），**When** 结束，**Then** 不写任何决策记录，批次不成立；下次批次重新呈现。
5. **Given** 异议点名的选项不是该选项集的具名成员，**When** 校验应答，**Then** 拒绝该应答并给出行名不匹配的错误；不猜、不近似匹配。

---

### User Story 3 - 处置落进既有载体，整批可只凭记录重放 (Priority: P1)

一次批次结束后，审计者不打开对话历史，也能从记录重建：本批的来源清单与逐来源计数、每个待决策项的身份与来源、建议默认值与接地指针、用户的异议原话与处置、每个已决项的 `D-NNN` 记录与批次族字段、register 的批次与编号登记、以及被解决项的来源状态更新。用重放动作可以得到同一份项集与处置；任一指针不可解析即被报告，绝不静默跳过。

**Why this priority**: 「决策必须可审计」是决策治理的既有承诺；没有落盘与重放，面板只是一次聊天。

**Independent Test**: 一个 fixture 批次落盘后，删除对话上下文，仅凭批次记录与指向的载体重放，断言项集、处置与记录齐全；把一条证据指针改坏，重放转红并点名该指针。

**Acceptance Scenarios**:

1. **Given** 一次完成的批次，**When** 审计，**Then** 批次记录含批次头（编号、时点、来源清单与逐来源计数、完备性判定）、逐项行表与每个已决项的 `D-NNN` 记录；记录含 `batch_id`、`batch_disposition`、`recommendation_grounding`、`rationale`、`evidence`、`actor` 与 `created_at`。
2. **Given** 一次解决的 register open 行，**Then** 该行状态被更新为点名批次与决策编号（行不删除），register 增加批次编号行与决策编号（按载体+区间）行；待决策项块追加 `resolution` 字段。
3. **Given** 批次记录落盘后某来源状态更新失败，**Then** 失败被披露，且再次扫描不会重新呈现该身份（读时联接已决批次记录）。
4. **Given** 一条被改坏的证据指针，**When** 重放，**Then** 重放报告该指针不可解析并以非零退出；不跳过、不降级为「干净」。
5. **Given** 同一批次编号重复记录，**Then** 拒绝第二次写入，绝不覆盖已有批次记录。

---

### User Story 4 - 完备性是诚实的：记账、拒绝、空集明说 (Priority: P2)

面板不声称「我列出了所有项」除非它能给出记账：每个来源被读取（或带原因缺席），每个候选被分类恰好一次，计数恒等。任一载体存在却读不了，整批拒绝：不呈现缺项的半批，不记录任何处置。零待决策项时显式回答「当前无待决策项」，不是空输出，也不是失败。

**Why this priority**: 批量决策的信任来自完备；不完备却自称完备，等于把漏掉的决策静默埋葬。

**Independent Test**: 一个不可读的 register（权限/解析失败）触发具名拒绝且零记录；一个缺席的来源目录被记为缺席空来源而非拒绝；一个空项目返回 `nothing-pending`；一个被删去扫描根的 fixture 的记账仍能解释每个候选。

**Acceptance Scenarios**:

1. **Given** 一个存在但不可解析的 register，**When** 面板扫描，**Then** 拒绝并点名该来源，退出码有文档，不产生呈现与记录。
2. **Given** 某个扫描根目录缺席，**When** 面板扫描，**Then** 该来源记为带原因的缺席空来源，记账恒等式仍成立，完备性判定如实标注该缺席。
3. **Given** 零待决策项，**When** 面板运行，**Then** 输出显式 `nothing-pending` 结果（成功），不创建批次记录。
4. **Given** 一个候选既不能被呈现、也不能被具名排除，**When** 记账，**Then** 这是拒绝而不是静默丢弃。

---

### User Story 5 - 重决不覆盖前例；人工与自主不混淆；零传输 (Priority: P2)

用户对一项提出与既往决策相反的改选。面板先呈现该既往记录与冲突，要求显式选择；用户确认后新增一条记录，旧记录保留并以 `superseded_by` 指向新记录。若旧记录载体不可写，重决被拒绝而不是降级为新决策。`ai-autonomous` 决策从不进入面板；无人值守调用不能把「无人应答」记成接受。批次只写本地既有载体，不访问网络、不写入反馈存储、不自动传输任何内容。

**Why this priority**: 覆盖前例会毁掉审计链；把自主决策混入人类默认会改变持有者；传输会越过反馈红线。

**Independent Test**: 一个主体命中既往记录且默认值不同的 fixture，断言呈现 `prior-decision-conflict` 且不因沉默结案；用户改选后断言新记录 + 旧记录 `superseded_by` 且旧内容零改写；一个无人值守调用断言具名拒绝；一次批次结束后断言反馈存储与网络零接触。

**Acceptance Scenarios**:

1. **Given** 一个待决策项，其主体全名逐字出现在一条既往决策记录的 `context` 中且既往选中项与当前默认不同，**When** 呈现，**Then** 该项标 `prior-decision-conflict`，默认值不因沉默被接受。
2. **Given** 用户显式选择推翻既往决策，**Then** 新记录携带批次族字段，旧记录保留并追加 `superseded_by`；旧记录的既有内容零改写。
3. **Given** 旧记录载体不可写或不可解析，**When** 尝试重决，**Then** 拒绝并点名原因，不写「全新」记录。
4. **Given** 无人值守调用，**When** 尝试记录接受，**Then** 拒绝并说明无人应答不能构成沉默；扫描仍可只读进行。
5. **Given** 任意批次，**Then** 无网络访问、无反馈条目写入、无自动传输。

### Edge Cases

- **register 缺席**（新客户项目）：记为缺席空来源；批次仍可处理待决策项块；记录时若需登记编号，按 ID Register 的既有头部形态创建 register 后再登记（创建登记册是既有协议的合法动作，不是新存储）。
- **register 权威路径写着「同上」**：不解析（A-4）；该行成为 `incomplete` 并点名 `authority-unresolved`。
- **待决策项块位于围栏代码块内**：不计为待决策项（与 107 的围栏规则同源）。
- **同一主体的两个块选项标签集不同**：一行呈现，标 `source-conflict`，必须显式选择；不得任选一侧默认。
- **同一主体在不同载体使用不同名称拼写**：不做模糊匹配，按两条项呈现，并披露可能的重复（字面身份不成立即不合并）。
- **默认项不是恰一个（零个或多个）**：`no-default`，不可沉默结案。
- **默认选项的 `reversibility` 写 `irreversible`**：`irreversible-default`，不可沉默结案，呈现中说明不可逆后果与确认义务。
- **默认证据指针不可解析**：块判 `incomplete`（缺失要素 = 不可解析指针），不得记 `grounded`。
- **既往记录命中但用户未处理冲突项**：冲突项保持待定；批次收尾逐项说明。
- **异议提出一个不在选项集中的新选项且项没有 `other` 路径**：拒绝该异议并给出 `other` 路径规则；有 `path` 时按路径处理。
- **异议点名的项已被先前批次解决**：拒绝并指向既有决策记录；不重复结案。
- **批次记录写入成功但 register 更新失败**：披露失败；读时联接保证不重复呈现；下一次批次或人工修复补齐 register。
- **两个并发批次**：不同批次编号 → 不同知识条目路径；互不读写对方记录；register 为单一索引，编号冲突按既有 renumber 机制修复，不静默改号。
- **批次记录路径与既有知识条目同名冲突**：标题携带唯一批次编号；写入前检测同编号已存在 → 拒绝，绝不 upsert 覆盖。
- **用户对不合格项提出改选**：允许（显式选择可解决部分不合格态，例如无默认项选择具名选项）；处置仍按 `objected-alternative` 记录，但该项的资格状态与原因保留在批次行。
- **重放时来源载体已归档或迁移**：指针不可解析 → 重放报错；不得以「历史记录」为由跳过。
- **扫描根中出现本特性批次记录之外的 `decision-batch-` 知识条目**：只按批次编号/标题前缀识别；未知形态条目报为不可解析候选（拒绝），不猜测。
- **register 中 `open` 行与 `resolved` 行混排、状态带加粗/标点**：去强调后按起始词判定；`resolved-for-v1` 等前缀词不是 `open`（按词边界判定）。

## Requirements *(mandatory)*

### Functional Requirements

**A. 所有者扩展与词汇（FR-001…FR-005）**

- **FR-001**: MUST 在既有决策治理单一所有者页 [[STR-001]] 中**加法式**扩展本特性的全部规则面：待决策项与待决策项块语法、封闭待决策项来源清单、批次呈现契约、建议默认值与接地契约、异议式处置契约、批次记录契约、批次族记录字段、批次生产者行、人工/自主边界、完备性与拒绝规则、重放契约。其他任何面（命令模板、技能、文档、检查器）MUST 以指针抵达，MUST NOT 复述其判据表；MUST NOT 新建第二个决策所有者页。
- **FR-002**: 所有者页 MUST 拥有以下新词的定义与含义（核心概念带双语形态，owner: `shared/guidelines/bilingual-expression.md`）：Pending Decision Item（待决策项）、Pending Item Block（待决策项块）、Decision Batch（决策批次）、Batch Record（批次记录）、Recommended Default（建议默认值）、Recommendation Grounding（建议依据）、Batch Disposition（批次处置）、Acceptance by Silence（沉默接受默认）。既有九个词的含义不被改写。
- **FR-003**: 所有者页的封闭决策生产者清单 MUST 新增一行：生产者 = 批量决策面板（`/speckit.decide` 批次会话）；既有载体 = 批次记录；义务 = `record-when-decision`（已决项记录；暂缓与不完整不是决策）；类别 = 仅 `human-interactive`；事实所有者 = 本扩展节。清单的封闭性检查（含既有守卫与冻结基线）MUST 在同一变更内同步扩展，MUST NOT 静默放行清单外入口。
- **FR-004**: MUST NOT 新建第二套决策登记、队列、存储或调度器；MUST NOT 新增运行期存储根或顶层目录；`.specify/register.md` MUST 保持持久编号的唯一索引；记录字段闭集只经所有者页加法式扩展（A-12），MUST NOT 出现与 107 平行的第二套记录 schema；批次记录是既有 knowledge 存储中的一条日期化记录，不是新存储。
- **FR-005**: MUST NOT 与 ai-harness 091 或任何外部决策治理做能力对齐；MUST NOT 访问网络、MUST NOT 自动传输任何内容、MUST NOT 把批次记录写入反馈存储或打包上传。

**B. 待决策项来源与形态（FR-006…FR-013）**

- **FR-006**: 待决策项来源 MUST 是封闭清单（§ Pending-Source Roster）：`register-open-decision-row`（[[STR-003]]）与 `authored-pending-item`（[[STR-004]]）。第二来源的扫描根封闭为 `.specify/specs/`、`.specify/goals/`、`.specify/anchoring/`、`.specify/teams/`；来源或扫描根的增删 MUST 以所有者页修订进行。
- **FR-007**: 排除族 MUST 具名并计入记账：已触发的交互门、澄清标记、parked idea、`ai-autonomous` 检查点裁决、`REC-` 行。MUST NOT 静默丢弃任何候选；MUST NOT 把排除族改写成「不存在」。
- **FR-008**: 待决策项 MUST 以独立块语法承载，标题前缀为 [[STR-002]]；字段闭集见 § Pending Item Block 的封闭字段表（含同名族与解决族两条条件字段）；待决策项块 MUST NOT 被记录文法判为记录，记录 MUST NOT 被判为待决策项块。选项集 MUST 沿用 107 的五要素、声明计数、唯一默认、`other` 路径与 `forced` 规则。
- **FR-009**: 去重 MUST 按身份进行：主体完整名称 +（同名时的）定位信息；重复引用合并为一行并列出全部来源；同身份而选项标签集不同时 MUST 标 `source-conflict` 并要求显式选择；MUST NOT 按标题相似度或语义相似度合并。
- **FR-010**: register 行的完整信息 MUST 在其权威路径上的待决策项块中解析；`同上` 一类相对表述 MUST NOT 被解析为路径；解析失败的行 MUST 以 `incomplete` 呈现并点名缺失要素（含 `authority-unresolved`），MUST NOT 由面板补全。
- **FR-011**: 类别门 MUST 生效：批次只呈现 `human-interactive` 项；`ai-autonomous` 或类缺失的候选 MUST 以 `not-human-held` 排除并计数；MUST NOT 转换类别。
- **FR-012**: 已解决项 MUST 被排除（`already-resolved`）：来源带 `resolution` 字段，或读时联接在既往批次记录中发现同身份已决项；来源状态与已决记录不一致时 MUST 披露（MUST NOT 沉默）。
- **FR-013**: 扫描 MUST 只读：在用户应答被记录之前，MUST NOT 写任何记录、状态或登记。

**C. 聚合与完备性（FR-014…FR-018）**

- **FR-014**: 一次调用 MUST 扫描全部来源并产出**一次**呈现；顺序 MUST 确定（来源清单顺序 → 载体仓库相对路径 → 块在文件内的出现序）；相同输入重复扫描 MUST 得到相同项集与顺序（扫描时间戳除外）。
- **FR-015**: 完备性 MUST 以封闭清单断言表达（owner: `shared/guidelines/closed-set-claims.md`）：参照物 = 本次扫描的来源清单与候选集；比较单元 = 每个候选的处置分类；允许差集 MUST 为空；记账恒等式「扫描候选 = 呈现行来源 + 合并引用 + 具名排除」MUST 成立；批次记录 MUST 携带逐来源计数与判定。
- **FR-016**: 任一来源或候选载体**存在但不可读/不可解析** MUST 触发**拒绝**：不呈现、不记录任何处置、给具名原因与文档化退出码；MUST NOT 呈现半批并称完备。
- **FR-017**: 来源**缺席**（文件/目录不存在）MUST 记为带原因的缺席空来源，MUST NOT 使整批拒绝，MUST NOT 被读成「干净」；完备性判定 MUST 如实标注该缺席。
- **FR-018**: 零待决策项 MUST 产出显式 `nothing-pending` 成功结果，MUST NOT 是空输出、MUST NOT 创建批次记录。

**D. 呈现与建议默认值（FR-019…FR-025）**

- **FR-019**: 每项呈现 MUST 携带：107 `human-interactive` 模板的全部要素（平实语言的问题、上下文、每选项后果与可逆性、唯一默认、完整名称与同名定位、选项证据）、来源指针、`decision_class`、`basis`、接地状态与指针、资格状态与原因、以及异议方式。
- **FR-020**: 批次呈现 MUST 承载批次级上下文下限：为何此刻出现、沉默将意味着什么、如何提出异议或暂缓、哪些项保持待定及原因、完备性披露（含缺席来源）。面向用户的措辞 MUST 遵循 `shared/guidelines/user-facing-comprehension.md` 的白名单与上下文规则；MUST NOT 把内部标识符（字段名、脚本名、状态码）写入面向用户的正文。
- **FR-021**: 建议默认值 MUST 是该选项集声明的唯一默认成员；MUST NOT 由面板发明默认值或选项；`no-default` 项 MUST 呈现并不得经沉默结案。
- **FR-022**: 接地 MUST 按 A-6 的确定性联接计算，输出 [[STR-011]] 或 [[STR-012]]；`grounded` 时 MUST 至少给出一条可解析的既往经验指针，且每条发出的指针 MUST 可解析；`no-evidence` MUST 明示且不得暗示经验支持；`basis` MUST NOT 单独充当证据。
- **FR-023**: 前例冲突 MUST 被检出并呈现：主体全名逐字命中既往决策记录的 `context` 且既往选中项与当前默认不同 → `prior-decision-conflict`；该项 MUST NOT 经沉默结案；呈现 MUST 给出既往记录指针与所选选项。
- **FR-024**: 沉默接受资格 MUST 同时满足：`human-interactive`、块完整、恰一个默认、默认选项 `reversibility` 为可逆（不可逆/破坏性默认 MUST 显式确认，判据指针 `shared/guidelines/confirmation-gates.md`）、无 `source-conflict`、无 `prior-decision-conflict`、未被先前批次解决。任一不满足 MUST 以对应状态呈现并保持待定。
- **FR-025**: 呈现 MUST NOT 静默截断或遗漏任何已呈现项；长批次仍须完整呈现（不设人为长度上限）；任何省略 MUST 是拒绝而非摘要。

**E. 交互与处置（FR-026…FR-031）**

- **FR-026**: 异议 MUST 按项身份绑定，MUST NOT 按位置或顺序猜测；每条异议 MUST 指向该选项集的具名成员（完整标签）或暂缓；新选项只有在该项声明了带 `path` 的 `other` 时按路径处理，否则 MUST 被拒绝并给出路径规则；应答校验 MUST 在写任何记录之前完成。
- **FR-027**: 沉默语义 MUST 受限：仅在**已获用户应答**的交互式批次内，未被点名的 `eligible` 项记为 [[STR-008]]；零应答/中止会话 MUST 记零条记录；无人值守调用 MUST NOT 记录接受（FR-040）。
- **FR-028**: 处置 MUST 取闭集：[[STR-008]]、[[STR-009]]、[[STR-010]]。`objected-parked` MUST NOT 产生决策记录，项保持待定，并在批次记录中留下暂缓行；后续批次重新呈现该项。
- **FR-029**: 重决 MUST 走 107 取代规则（A-7）：新记录 + 旧记录追加 `superseded_by` 且内容零改写；旧记录载体不可写/不可解析时 MUST 拒绝重决；MUST NOT 覆盖、删除或静默改写旧记录。
- **FR-030**: 人的选择信号 MUST 复用既有门控观察词表（指针 `shared/guidelines/confirmation-gates.md`；`accepted-default` 映射 `approved-as-is`，`objected-alternative` 映射 `modified`），MUST NOT 另立第二套信号词表；`objected-parked` 不产生选择信号。
- **FR-031**: 面板 MUST NOT 解决用户未处置的项（除 FR-027 声明的沉默规则外）；MUST NOT 从「无用户回合」推断接受；MUST NOT 跨批次预授权默认值（A-9）。

**F. 记录与审计（FR-032…FR-038）**

- **FR-032**: 每批次 MUST 产出一份**批次记录**：既有 knowledge 存储中的一条日期化记录，一文件一批次、批次编号唯一、永不覆盖、经既有记忆引擎的写入面落盘（记录头含批次编号、时点、工具版本、来源扫描计数与完备性判定；逐项行表含项身份、来源、资格、接地、处置与决策编号；随后是已决项的记录块）；MUST NOT 写共享可变聚合。
- **FR-033**: 已决项 MUST 各产出一条 107 决策记录，文法与分层闭集不变，并按 A-12 携带条件层批次族字段 [[STR-005]]、[[STR-006]]、[[STR-007]]；`rationale` MUST 陈述建议依据与用户应答（沉默或异议原话要点）；`actor` MUST 按既有身份形态在场；`transmission_status` MUST 从 `not-transmitted` 起；`evidence` MUST 含接地指针与来源项指针。
- **FR-034**: register MUST 反映批次：[[STR-005]] 的取值（批次编号 `B-…`）与各决策编号在诞生时登记（可按载体+区间分组）；已决 register 来源行的状态 MUST 更新为点名批次与决策编号，行 MUST NOT 被删除；暂缓行保持 open 并标注批次；除状态单元格与追加行外 MUST NOT 改写 register。register 缺席时 MUST 先按既有头部形态创建再登记。
- **FR-035**: 已决来源状态 MUST 同步：register 行状态更新；待决策项块追加条件字段 `resolution`（值含批次编号与决策编号），块内容 MUST NOT 因解决而改写或删除；来源更新失败 MUST 披露，且读时联接（FR-012）MUST 阻止重复呈现。
- **FR-036**: 重放 MUST 只凭已记录载体重建整批：批次记录 + 可解析指针给出项集、完备性记账、默认值与接地、异议与处置、决策记录；重放 MUST 只读、确定（同输入同输出）；任一不可解析指针 MUST 被报告并以非零退出，MUST NOT 跳过或用对话记忆补足。
- **FR-037**: 幂等与并发 MUST 成立：同一批次编号的第二次记录 MUST 被拒绝；不同批次编号 MUST 写不同路径且互不读写对方记录；MUST NOT 修改他批记录。
- **FR-038**: 批次决策被传递实施时 MUST 沿用 107 的审计链三段（记录 → 派发尝试 → 实施回执）与传递义务；批次 MUST NOT 生成第二条记录或第二条传输路径。

**G. 入口、边界与落地（FR-039…FR-045）**

- **FR-039**: 交付面 MUST 是：薄入口命令模板 [[STR-013]]、内部技能 [[STR-014]]、确定性引擎 [[STR-015]]（封闭动作 `scan` / `record` / `replay`；`-h` / `--help` / `--version`；拒绝未声明选项；只读/写入面与退出码有文档，形态遵循 `shared/definitions/script-interface-definitions.md`）；固定规则判断（扫描、接地联接、成员校验、记账、成员集合与指针解析）MUST 由引擎判定，MUST NOT 由 LLM 复算。
- **FR-040**: 面板 MUST 只在交互式会话记录处置：无人值守调用 MAY 扫描（只读），但 MUST 拒绝记录接受并给出具名原因；MUST NOT 把无人应答读作沉默。
- **FR-041**: `ai-autonomous` 决策 MUST 保持其谓词驱动路径：批次 MUST NOT 呈现、转换或授权它们；人类默认值 MUST NOT 流入 `ai-autonomous` 记录。
- **FR-042**: 落地 MUST 在同一变更内完成：所有者页 [[STR-001]] 扩展（含 P-13 与本特性规则）、命令模板 [[STR-013]]、技能 [[STR-014]]、引擎 [[STR-015]]；镜像经 `sync-mirrors.py` 生成；每工具命令副本经既有再生成器更新；**冻结的命令与技能名基线测试同批扩表**；框架地图的决策治理行更新（P-13、批次能力、consumer 增补）；MUST NOT 手改镜像；MUST NOT 修改 `.specify/.gitignore` 或运行期存储布局（无新运行期目录）。
- **FR-043**: 命令文档 MUST 在 `docs/reference/commands/decide.md` 登记入口、动作集与退出语义，并以指针抵达所有者页；文档 MUST NOT 复述所有者页的判据表。
- **FR-044**: 守卫 MUST 覆盖并可转红：来源清单封闭性与成员、待决策项块语法、身份去重、记账恒等式与拒绝、`nothing-pending`、接地联接与无证据明示、前例冲突与重决取代、沉默资格与无人值守拒绝、批次族字段与记录文法、register 登记与状态更新、只读/无网络/无反馈写入、镜像与 init 分发、冻结基线；每条守卫 MUST 有逆向样本（改坏对象后转红），MUST 经唯一测试入口 `scripts/bash/run-tests.sh` 执行，fixtures 作为仓内开发资产放在 `tests/fixtures/decision-batch/`，不分发。
- **FR-045**: 机器/行为边界 MUST 诚实：机器只判结构命题（在场性、文法、闭集取值、计数恒等、成员集合、指针可解析性）；「建议是否合理」「后果陈述是否真实」「名称是否足够完整」「理由是否充分」MUST 由既有评审承接面判定（`/speckit.analyze`、`/speckit.review` 产物段、人工决策评审），MUST NOT 被任何文档或测试声称机器覆盖。

### Key Entities *(include if requirement involves data)*

- **Pending Decision Item（待决策项）**：一个尚未裁决的人持有决策项；属性：身份（主体完整名称 + 可选定位）、来源引用集、待决策项块、资格状态。
- **Pending Item Block（待决策项块）**：承载待决策项的既有载体区块；字段闭集见 § Pending Item Block；不是决策记录。
- **Decision Batch（决策批次）**：一次扫描—呈现—应答—记录的完整会话；属性：批次编号、扫描时点、来源计数、完备性判定、应答原文。
- **Batch Record（批次记录）**：决策批次在 knowledge 存储中的日期化记录；含批次头、逐项行表与已决项记录块；审计与重放的唯一入口。
- **Recommended Default & Grounding（建议默认值与依据）**：项声明的唯一默认选项 + 确定性联接得到的既往经验指针集或 `no-evidence` 明示。
- **Batch Disposition（批次处置）**：已决项的处置闭集成员（`accepted-default` / `objected-alternative`），或暂缓（`objected-parked`，不产生记录）。
- **Prior-Experience Evidence（既往经验证据）**：封闭载体集中的可解析指针（决策记录、`T-NNN`、history、feedback、knowledge 条目），用于接地。
- **Batch Item Row（批次项行）**：批次记录中的一行——项身份、来源、资格、接地、处置、决策编号。

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | CPython `>=3.8` 标准库（扫描、解析、联接、记账与重放引擎） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 新增引擎与测试在 `>=3.8` 解释器上经唯一入口通过；新增第三方 import 为零 | FR-039, FR-044 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约/单元测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；零新增依赖 | `pyproject.toml` | 新增测试经 `scripts/bash/run-tests.sh` 运行，相对入口基线零新增失败名 | FR-044 | EP-001 |
| RS-003 | POSIX `bash` 运行时（唯一测试入口） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增显式版本下限；本特性不改该入口 | `scripts/bash/run-tests.sh` | 新增测试全部经该入口执行且一次退出 0 | FR-044 | EP-001 |
| RS-004 | 记忆引擎的 knowledge 存储写入面（批次记录载体） | signed-contract | 记忆系统所有者（`scripts/python/memory-utils.py`） | 一文件一记录、upsert by slug 的既有布局；本特性不改其 schema | `scripts/python/memory-utils.py` | 批次记录经该引擎落盘且 frontmatter 合规；同批次编号第二次写入被拒绝；并发批次路径互异 | FR-032, FR-036 | EP-002 |
| RS-005 | 既有决策检查器（记录文法、字段闭集、指针可解析） | in-scope | 本特性扩展的框架源检查器与守卫 | 不适用（仓内实现，无外部版本面） | `scripts/python/validate-decisions.py` | 批次记录中的记录块通过文法与批次族字段检查；逆向样本转红；待决策项块不被判为记录 | FR-008, FR-033, FR-044 | EP-003 |
| RS-006 | 既有镜像与命令副本工具链 | in-scope | 本特性修改的框架源与工具链 | 不适用（仓内实现） | `scripts/python/sync-mirrors.py` | 镜像对无新增漂移；每工具命令副本再生成检查 rc 0 | FR-042 | EP-004 |
| RS-007 | ID Register 文件（批次与决策编号的唯一索引） | signed-contract | ID Register 规则所有者（`.specify/instructions.md` § ID Register） | 手工唯一索引；逐条或按载体+区间分组 | `.specify/register.md` | 批次编号与决策编号在诞生时登记；已决 OI 行状态更新且行未删除 | FR-034 | EP-005 |
| RS-008 | 冻结命令/技能名基线测试（库存封闭） | in-scope | 本特性同批扩表的契约测试 | 不适用（仓内实现） | `tests/contract/test_migration_distribution.py` | 基线集合与磁盘实际集合相等；新增一项两处同批移动 | FR-042, FR-044 | EP-006 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对一个同时覆盖两个来源、重复引用、不完整项与 `ai-autonomous` 项的 fixture，扫描记账恒等式成立（扫描候选 = 呈现行来源 + 合并引用 + 具名排除），每项恰一行；把 register 改为存在但不可解析后，面板拒绝并点名来源、零呈现零记录；空 fixture 返回 `nothing-pending` **Path**: final
- **SC-002**: 对每个已呈现项，机器检查断言 107 `human-interactive` 模板要素齐备（主体全名、上下文、选项五要素与唯一默认、来源指针、接地状态、资格与原因）；不完整项逐项点名缺失要素且不进入沉默资格；`ai-autonomous` 项呈现数为零 **Path**: final
- **SC-003**: 在含既往证据的 fixture 上，每个 `grounded` 项至少一条既往经验指针可解析，且指针命中封闭载体集；在无证据 fixture 上，项标 `no-evidence`；两套 fixture 上发出的指针 100% 可解析，零编造指针 **Path**: final
- **SC-004**: 「仅异议一项」的应答产出恰一条 `objected-alternative` 与其余 `eligible` 项的 `accepted-default`；不可逆默认、无默认与前例冲突项保持待定且各有具名原因；零异议应答使全部 `eligible` 项结案；中止会话产出零记录；不在选项集内的异议被拒绝 **Path**: final
- **SC-005**: 一次完成的批次只凭批次记录与可解析指针即可重放项集、完备性、默认值、异议与处置；所有记录含批次族字段且通过文法检查；register 有批次与决策登记且已决 OI 行状态已更新；把任一指针改坏后重放非零退出并点名该指针 **Path**: final
- **SC-006**: 主体命中既往记录且默认冲突时，项标 `prior-decision-conflict` 且不因沉默结案；用户改选后新记录存在、旧记录保留且带 `superseded_by`、旧内容零改写；旧载体不可写时重决被拒绝且不产生新记录 **Path**: final
- **SC-007**: `ai-autonomous` 项呈现数为零且记账有 `not-human-held` 排除；无人值守调用记录接受时被具名拒绝；人类批次处置不写入任何 `ai-autonomous` 记录 **Path**: final
- **SC-008**: 对一份批次呈现，按其批级上下文下限与行话白名单判定：读者无需打开其他工件即可知道为何出现、沉默含义、如何异议、哪些项待定；评审承接面的检查材料齐备（行为类，不声称机器覆盖） **Path**: supporting
- **SC-009**: 无新增运行期存储根、无 `.specify/.gitignore` 变更、无运行期存储布局变更；镜像与命令副本逐字节一致；fresh `specify init` fixture 含命令与技能；本特性零网络访问、零反馈存储写入、零自动传输；冻结命令/技能基线同批移动后测试转绿 **Path**: supporting
- **SC-010**: 相同输入重复扫描的项集与顺序逐字段一致（时间戳除外）；同一批次编号的第二次记录被拒绝；两个并发批次的记录路径互异且互不修改 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 三个 fixture（双来源+重复+不完整+自主项 / 不可解析 register / 空项目）在契约测试中的扫描输出与退出码；记账恒等式由测试断言；完整命令行、stdout/stderr、退出码与时长按 single-run evidence 捕获。
- **SC-002 Source**: 呈现 payload 的结构断言（逐项要素在位）+ 不完整项缺失清单快照；`ai-autonomous` 呈现计数为零的断言输出。
- **SC-003 Source**: 两个接地 fixture 的呈现 payload 中 `recommendation_grounding` 与指针列表；逐指针解析器输出（100% 可解析断言）。
- **SC-004 Source**: 四种应答形态（异议一项 / 零异议 / 中止 / 非成员异议）的批次记录行表快照与校验退出码。
- **SC-005 Source**: 批次记录的落盘内容（批次头、行表、记录块）+ `validate-decisions.py` 对批次记录的运行输出 + register 的 diff（仅状态单元格与追加行）+ 重放输出与坏指针用例的退出码。
- **SC-006 Source**: 前例冲突 fixture 的呈现状态 + 重决后的两条记录文本（旧记录零改写用行级读数）+ 不可写载体用例的拒绝输出。
- **SC-007 Source**: 呈现 payload 的排除记账 + 无人值守调用用例的具名拒绝输出 + 记录集中 `decision_class` 取值断言。
- **SC-008 Source**: 批次呈现文本 + 评审承接面（`/speckit.review` 产物段）的检查记录；不引入评分器或新追踪机制。
- **SC-009 Source**: `sync-mirrors.py --check` 输出、命令副本再生成检查输出、fresh init fixture 文件树、网络与反馈存储的零接触断言（测试内）、冻结基线测试输出。
- **SC-010 Source**: 两次扫描输出的逐字段比较（时间戳字段分离）；同编号二次写入的拒绝输出；并发批次 fixture 的路径集合断言。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "shared/definitions/decision-definitions.md" | FR-001, FR-042 |
| `STR-002` | "### PENDING —" | FR-008 |
| `STR-003` | "register-open-decision-row" | FR-006 |
| `STR-004` | "authored-pending-item" | FR-006 |
| `STR-005` | "batch_id" | FR-033, FR-034 |
| `STR-006` | "batch_disposition" | FR-033 |
| `STR-007` | "recommendation_grounding" | FR-033 |
| `STR-008` | "accepted-default" | FR-027, FR-028 |
| `STR-009` | "objected-alternative" | FR-028 |
| `STR-010` | "objected-parked" | FR-028 |
| `STR-011` | "grounded" | FR-022 |
| `STR-012` | "no-evidence" | FR-022 |
| `STR-013` | "templates/commands/decide.md" | FR-039, FR-042 |
| `STR-014` | "skills/internal/decide-batch/SKILL.md" | FR-039, FR-042 |
| `STR-015` | "scripts/python/decision-batch.py" | FR-039, FR-042 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-27（无人值守 requirements 阶段；无提问，裁决记于 Assumptions）

- Q: 本阶段是否留下 `[NEEDS CLARIFICATION]` 标记？→ A: 无。brief 的歧义清单逐条在 A-3…A-9 就地裁定（来源与去重 = A-3/A-4；入口面 = A-5；默认值推导 = A-6；重决 = A-7；完备性 = A-8；常设默认 = A-9），其余边界记于 A-1、A-2、A-10…A-20。
- Q: 「待决策项」包含哪些载体？→ A: 封闭两来源（register open 的 OI-/D- 行、四个扫描根中的待决策项块），排除交互门、澄清标记、parked idea 与 `ai-autonomous` 检查点；register 行必须解析到显式权威路径上的块，`同上` 不解析（A-3、A-4、FR-006、FR-010）。
- Q: 入口是命令、既有命令扩展还是技能？→ A: 新命令 `/speckit.decide` + 内部技能 `decide-batch` + 确定性引擎 `decision-batch.py`；既有命令族无决策裁决入口，命名沿用单词动词与 `<动词>-<对象>` 兄弟形（A-5、FR-039）。
- Q: 建议默认值如何得出，是否允许 LLM 现场推荐？→ A: 默认值取项声明的唯一默认选项；接地只做确定性联接（默认证据指针 + 主体全名逐字命中的既往记录 + 其 `T-NNN`）；无证据明写 `no-evidence`；面板不得现场语义检索或发明（A-6、FR-021、FR-022）。
- Q: 异议推翻既往决策怎么办？→ A: 走 107 取代规则，新记录 + 旧记录 `superseded_by` 且零改写；旧载体不可写即拒绝重决（A-7、FR-023、FR-029）。
- Q: 完备性如何声称与检查？→ A: 封闭来源清单 + 逐候选处置分类 + 记账恒等式 + 允许差集为空；存在但不可读 → 拒绝；缺席 → 具名缺席空来源；零项 → `nothing-pending`（A-8、FR-015…FR-018）。
- Q: 默认值能否跨批次预授权？→ A: 否，仅单批次有效；不记忆偏好、不自动套用（A-9、FR-031）。
- Q: 批次记录落在哪里？→ A: 既有 knowledge 存储的一条日期化记录（经记忆引擎写入，一文件一批次）；不写反馈存储（避免阈值污染）、不写 session（可遗忘层）、不新建存储根（A-11、FR-032）。
- Q: 特性绑定与注册？→ A: 新独立 Feature 112；所有者页只做加法式扩展；本阶段登记 `.specify/features.md` 行与 `.specify/features/112-decision-batch-panel.md`（`Draft`），不编辑 `.specify/register.md` 与状态脊（A-2、FR-001、FR-003）。
- Q: 存量 open 行没有待决策项块怎么办？→ A: 以 `incomplete` 呈现并点名缺失要素；不补造、不代写；作者补全后才可批量结案（A-16、FR-010、FR-019）。
- Q: 脚手架偏差？→ A: 当前分支已存在时脚本会派生新编号与分支；按 107/109/110 先例手工从模板脚手架，停留在 112 分支（A-19）。

## Out of Scope

- 调度器、提醒、通知、常驻扫描或任何后台守护；面板是按需调用。
- UI、仪表盘或可视化界面。
- 自动撰写或补全待决策项（缺失要素的补全是生产者/用户的义务；A-16）。
- `ai-autonomous` 决策的批量裁决或任何类别转换。
- 跨批次常设默认值、用户偏好记忆或自动套用。
- 任何第二存储根、第二决策登记、第二记录 schema 或共享可变聚合。
- 与 ai-harness 091 或任何外部决策治理的能力对齐。
- 网络访问、自动传输或把批次记录当作反馈打包。
- 对既有 dated 记录（历史规格、历史评审、既有决策记录正文）的改写；批次只追加新记录与条件字段。