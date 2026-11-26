# Requirements Specification: Team View Degradation Hardening — 真实团队定义下的诚实呈现与降级语义（Team View Degradation Hardening）

**Requirement Branch**: `108-team-view-degradation`
**Created**: 2026-11-26
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订 `templates/commands/team.md`、`skills/internal/view-team/**`、`scripts/python/team-view.py`、`docs/reference/commands/team.md`、`tests/**` 的作者，需要判定「view 在读不懂的真实团队上该说什么、不该猜什么」）与下游项目维护者（在真实团队档案上使用 `/speckit.team view`、需要区分「团队有问题」与「查看器读不懂」的人）——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「真实世界的运行报告文件名如何被识别、最新报告如何选出」「哪些文件是运行报告、哪些是辅助产物、哪些是无法识别的残留」「items.jsonl / 持续运营脊柱缺失时说什么、后果是什么」「binding 缺块或缺键、内联 goal 不是 slug 时呈现什么、修复路径是什么」「正文矩阵缺 agent 列时名册差异如何呈现」「降级原因与退出码的封闭集是什么、哪些情况不算降级」「哪些既有输出必须逐字节保持」时打开本规格，据 FR-001…FR-025 与 SC-001…SC-008 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "以如下真实的team view的执行输出作为输入优化 /speckit.team view命令"

**输入校正**：①用户随输入附带的真实执行输出为其客户端项目 `/cws_data/kangaroo-xuanji/xuanji-iac` 的 `/speckit.team view log-metrics-collection-system` 结果；该客户端项目不在本仓库内，其事实按用户提供的关键事实记录于下方 Overview 的「生产证据」并以本仓可复现的 fixture 与实测语料承载验收（A-12）。②用户要求是「优化 `/speckit.team view` 命令」，因此**读取侧的容错与诚实呈现**是本特性的落点；生产输出自带的纠正建议中「报告命名须统一**或**程序须接受真实命名」取后者——命名 owner 不变，容错在读取侧（A-3）。③「以真实输出为输入」按「以该输出暴露的问题为需求证据」理解，不是要求逐字复刻该输出。

## Related Feature *(mandatory)*

**Feature ID**: 027
**Feature Name**: Team Management
**Binding basis**: 027 owns the `/speckit.team` command surface（create / modify / run / view）与团队档案层；本规格只修订 `view` 模式的读取程序（`scripts/python/team-view.py`）、`view-team` 技能措辞与测试，是 103-team-view（同一命令面的第四模式）的直接后续切片，036 / 042 / 103-team-view 直接绑定 027 的先例成立（binding-precedent heuristic）。Brief 的 leading candidate `103-team-view` 经查找为已定稿的 spec 编号而非 Feature ID（Feature 103 = Technical Debt Governance），其父 Feature 即 027。Bind 分支：不新建 Feature，索引登记切片行 108（`Draft`），027 状态保持 `Ready for Review` 不回退（no-status-regression gate）。

## Overview

**问题**：`/speckit.team view` 的读取程序 `scripts/python/team-view.py` 对「团队定义与运行历史是否长成模板的样子」做了隐含假设。在真实团队档案上，这些假设导致三类失真：

1. **运行历史被读丢**：报告识别只接受单一字面量 `^(\d{8}T\d{6}Z)-report\.md$`；带 4-hex 冲突/阶段后缀、ISO 连字符或小时分钟形态的**真实运行报告**全部落进 `unrecognized`，既不参与「最新报告」选择，也不被计为报告。生产证据中 60 份报告因此不可识别，「最新报告」落到了更旧的 `20261124T074500Z-report.md` 上；本仓实测中三个团队的报告甚至被呈现为「运行报告: 为空」而退出码仍为 0。
2. **降级状态不可行动**：binding 缺块、内联 `goal` 非 slug、正文矩阵缺 `agent` 列、非 continuous 团队的持续运营脊柱缺失——这些状态有的被呈现为笼统的「未记录」，有的缺少受制裁修复路径，读者无法区分「团队定义需要修」与「查看器读不懂」。生产输出以退出码 5 结束，但「为何降级、下一步修什么」没有收敛到可执行的指针。
3. **降级语义未封闭**：退出码 5 的触发面只有「引擎读失败」一种；报告识别失败、最新判定不确定、最新报告不可读都不进入降级语义，于是**沉默被读成干净**——正是「缺失 / 为空 / 不可读 / 未记录」四态纪律要防止的失真。

**生产证据（用户提供；客户端项目，不在本仓）**：一次 `single` 模式查看，程序退出码 **5**；团队 `log-metrics-collection-system`：`team.md` 无 `binding` 块 → binding 不可读（缺 owner / owner_id / origin）；frontmatter `goal` 为内联长文本而非 slug → goal 不可读；`anchor_identity` 经 `anchor_slug` 解析为 declared（正常）；正文矩阵无 `agent` 列 → `roster_delta` 不可比对、9 名 frontmatter 成员仍被列出、`seats` / `stage_seats` 未声明；`runs/` 中 60 份报告因 4-hex 后缀或非标准时间戳被归为 `unrecognized`，「最新报告」选出的是更旧的 `20261124T074500Z-report.md`；`items.jsonl`、`STATE.md`、`run-log.jsonl` 缺失；`handoff_ref` 未声明；锚点存在（10 条判据、active、Targets T-001…T-034）；config 为 `iteration` 带阈值、协作项目、自底向上次序、质量维度、constraints 文件与集群 runbook。该输出自带的纠正建议：经 `/speckit.team modify` 修复定义（binding + goal 归一为锚点 slug）；报告命名须统一或程序须接受真实命名（框架层）。

**实测语料（2026-11-26，基线 `54c6efa8c`，`.specify/teams/*/runs/`）**：46 个文件；28 个符合 `YYYYMMDDThhmmssZ-report.md`；18 个不符合——其中 16 个带可解析的起始时间戳（13 个 `-report.md` 报告样式：ISO 连字符 `2026-09-17T072239Z-report.md`、`2026-08-07T18-30-00Z-report.md`、小时分钟 `20261014T1710Z-report.md`；3 个辅助产物：`-verification.md` ×2、`-seat-result.md` ×1），2 个无起始时间戳（`2026-10-07-progress-snapshot.md`、`2026-10-06-S1-judgment-contract.md`）。三个团队（`viz-skill-arena` 5 份、`draw-two-layer-structure` 7 份、`draw-diagram-interactive` 1 份）的全部报告均不可识别：现程序对它们呈现「运行报告: 为空」「最近报告: 未记录」并以退出码 0 结束——报告存在而查看器说空，属于现有 FR 级别的失真（103 FR-015 的「为空（存在但无条目）」被误用为「存在但读不懂」）。

**本特性交付**：读取侧的报告识别与最新选择按解析时间戳工作；辅助产物与残留各有显式分类；缺失/不可读状态带后果与 pattern 适用性；binding/goal 的降级形态带精确原因与受制裁修复路径；矩阵缺列与名册不可比对成为一等状态；降级原因与退出码收成封闭集并由测试钉住；健康团队的输出保持逐字节不变。**全部收敛在一个读取引擎内，不新增第二读取器、第二存储或团队 schema 变更。**

**不做什么**：不新建第二读取器、缓存、快照、索引或 registry；不自动修复团队定义（修复路径只呈现、不执行）；不改 create-team 的报告命名契约或 `team.md` schema（容错是读取侧的）；不新增退出码；不新增面向用户的机器可读格式（既有 `--json` 仍只是内部测试面）；不改 `goal-utils.py`（只消费其读动作）；不重写任何 dated record（既有 spec、报告、历史记录正文）。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是读取程序、技能/文档措辞与测试，验收时被机器执行与断言。 | 按验收 oracle 判定：缺陷只在程序执行与断言时暴露。 |
| **A-2** | **单一读取引擎**：全部固定规则仍只由 `scripts/python/team-view.py` 完成；本特性只修改该程序（及其技能/文档/测试面），MUST NOT 新增第二读取器或第二匹配入口。 | 103 A-16 / FR-014 的延续；「一个引擎」是本特性的显式最低要求。 |
| **A-3** | **命名 owner 不变、容错在读取侧**：运行报告的权威命名仍是 `skills/internal/create-team/SKILL.md` § Report contract 的 `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md`；本特性让读取器**接受**真实世界已存在的可解析形态，而不是改命名契约。 | 用户证据明确给出二选一（统一命名或程序接受），程序接受不动任何既有团队；改 owner 会要求全仓迁移，违反「既有团队不需要迁移」。 |
| **A-4** | **最新 = 解析时间戳的最大者**：时间戳按 UTC 解析（紧凑 `YYYYMMDDThhmmssZ`、ISO 连字符、小时分钟等真实形态）；并列时以文件名字典序确定；MUST NOT 回落到「更旧的已识别报告」。 | 「latest」语义只能由时间决定；生产事件的直接根因就是按窄模板先过滤再取最大。 |
| **A-5** | **三类文件分离**：`runs/` 内的文件分为（a）运行报告（带可解析时间戳与实际报告形态，含 4-hex/阶段后缀）、（b）辅助产物（同目录的非报告文件，如 `-verification.md`、`-seat-result.md`、progress snapshot）、（c）残留（无任何可解析时间戳的文件）。分类规则必须显式、可判定、文档化。 | 同目录确实存在辅助产物（本仓实测 3 个）；把它们当报告会伪造 latest，把它们当残留会制造噪声。 |
| **A-6** | **不确定即披露**：当残留文件可能包含比已选最新更晚的运行时（存在无时间戳文件且无法证明其更旧），view MUST 披露不确定性并按降级呈现；MUST NOT 静默。 | 「沉默不得被读作干净」；这也是用户证据中「最新不是真最新」的兜底。 |
| **A-7** | **降级不推断**：binding 三键、goal→slug、最新报告、名册差异一律不推断、不填补、不猜测；每处呈现要么是读得的事实，要么是命名状态加原因。 | 与 103 FR-015 / A-8 的状态诚实一致；修复由人经受制裁路径执行。 |
| **A-8** | **脊柱产物的 pattern 适用性**：`constraints.md` / `STATE.md` / `run-log.jsonl` 是 continuous 团队的持续运营脊柱（owner：`references/operating-loops.md`）；非 continuous 团队缺失时 MUST 按「按声明 pattern 不适用的产物」呈现，而不是无差别「缺失」；pattern 未声明时按 owner 的缺省语义呈现并披露缺省来源。 | 生产团队是 `iteration`，把 continuous-only 产物缺失渲染成缺陷会误导修复方向。 |
| **A-9** | **降级原因封闭集最小扩展**：降级原因恰为 `engine-degraded`（既有：引擎读动作未能产出必需事实）与新增 `report-recognition-uncertain`（最新判定不确定）；两者都映射退出码 `5`；退出码闭集仍为 `0/2/3/4/5`；「缺失 / 为空」是诚实状态，单独出现 MUST NOT 触发降级退出码。 | 封闭集越小越可测；生产证据的降级根因（binding 不可读）本就走 `engine-degraded`。 |
| **A-10** | **健康输出保持是可判定声明**：以基线提交 `54c6efa8c` 的同一程序在**同一健康 fixture**（完整 binding、全部报告名为紧凑 `-report.md`、无残留、矩阵含 `agent` 列、无内联 goal、报告可读）上的输出为基线 referent；变更后程序在该 fixture 上的 stdout MUST 逐字节一致、退出码相同（机器 diff）。 | 封闭声明须有基线 referent 与可推导允许增量（owner：`shared/guidelines/closed-set-claims.md`）；健康谓词使允许增量为空，判定不依赖人工清单。 |
| **A-11** | **既有团队不需要迁移，但非规范命名的团队输出会被纠正**：本特性只读、不改任何团队定义；符合健康谓词的团队输出逐字节不变；本仓三个「报告全不可识别」的团队以及任何带非标准名/残留/缺 binding 的团队，输出会变为**纠正后的诚实读数**——这是本特性枚举的预期增量，不是回归。 | 诚实呈现必然改变「原本失真」的输出；将其定义为具名增量，避免「其余不变」的不可判定聚合。 |
| **A-12** | **证据形态**：生产证据是用户提供的客户端输出关键事实（项目不在本仓）；本仓实测语料与 fixture 复现同一组失真；验收断言在 fixture 上进行，不依赖客户端项目或活档案的易变状态。 | 需求只能绑定可复现的观察；活档案计数只作本阶段的实测基线记录。 |
| **A-13** | **两顶帽子**：源面为 `scripts/python/team-view.py`、`skills/internal/view-team/**`、`docs/reference/commands/team.md`、本特性新增契约与 `tests/**`；`.specify/**` 镜像由 `scripts/python/sync-mirrors.py` 再生成，不手改。 | framework source 与 client runtime 的编辑不可互换；手改镜像会漂移。 |
| **A-14** | **不新增 glossary 词条**：本特性不引入新实体，只细化 view 既有呈现语义；词汇登记遵循 103 A-11 先例。 | 词汇表只登记项目域术语。 |
| **A-15** | **渲染标签词汇表所有者转移**：当前「渲染行类型（封闭集）」的 owner 是 `.specify/specs/103-team-view/data-model.md` § Rendering Line Types；本特性新增/改用的标签（残留行的一等处、`不可比对（not comparable）` 等）MUST 并入一个**唯一活所有者**（本特性的契约面），103 数据模型保留为日期化记录，不再作为活 owner 被引用。 | One Source Of Truth：新标签不能只活在新代码里，也不能在两个 spec 里各留一份活副本。 |
| **A-16** | **脚手架偏差（披露）**：`create-new-requirements.sh` 会把当前本地分支 `108-team-view-degradation` 计入编号空间而派生 109 并新建分支；与本线「不建第二分支、规格编号 108」冲突。按 107 先例，本阶段**手工**从 `.specify/templates/requirements-template.md` 脚手架到 `.specify/specs/108-team-view-degradation/requirements.md`，脚本的模板拷贝步骤以等价方式复刻，仅跳过其建分支步骤，并记录于 `test-evidence/requirements-stage-2026-11-26.md`。 | 工作树必须停留在 `108-team-view-degradation`；脚本的编号派生把「本线分支」当成了「已用编号」。 |
| **A-17** | **unsupported-shape 的边界**：本特性不实现「任意命名解析」；只接受**可解析时间戳**的文件名形态。无法解析的文件永远走残留，不做模糊猜测。 | 识别规则必须可判定；模糊匹配会把无关文件读成运行报告。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 真实运行历史不被读丢：报告识别、最新选择与残留 (Priority: P1)

维护者在一个真实团队上执行 `view <slug>`：`runs/` 里的报告是长期演进中累积的，命名形态混杂（旧的 ISO 连字符、小时分钟、带 4-hex 冲突或阶段后缀），同目录还有 verification / seat-result 之类辅助产物。他需要看到**真实的最新运行**——最新报告按文件名中的可解析 UTC 时间戳决定，不能因为只认一种模板就把更新的报告藏起来、把更旧的报告当最新；读不懂的文件必须作为有计数的残留被点名，而不是被静默吞掉。

**Why this priority**: 这是本特性的直接根因（生产输出的「最新不是真最新」与本仓三个团队「报告存在却显示为空」）；不修它，view 的运行状态组整体不可信。

**Independent Test**: 构造 fixture：一份旧的紧凑命名报告 + 更新的 4-hex/阶段后缀报告 + 更新的 ISO 连字符报告 + 一个同时间戳的 `-seat-result.md` 辅助产物 + 两个无时间戳文件；执行一次 view，断言最新 = 解析时间戳最大者、旧报告冒充最新次数为 0、辅助产物未被选为报告、残留行含计数与有界示例。

**Acceptance Scenarios**:

1. **Given** `runs/` 同时含 `20261124T074500Z-report.md` 与更新的 `20261125T121924Z-93cc-stage.md`／`2026-11-25T140000Z-report.md`，**When** 执行 `view <slug>`，**Then** 「最近报告」是解析时间戳最大的那一份，更旧的报告 MUST NOT 被呈现为最新。
2. **Given** 团队的**全部**报告都是非标准可解析命名，**When** 执行 `view <slug>`，**Then** 运行报告状态 MUST NOT 呈现为「为空」或「缺失」，最新报告 MUST 被选出。
3. **Given** 同目录存在 `-verification.md` / `-seat-result.md` 辅助产物，**When** 执行 `view <slug>`，**Then** 它们 MUST 与运行报告区分呈现，MUST NOT 被选为最新报告。
4. **Given** `runs/` 含无任何可解析时间戳的文件，**When** 执行 `view <slug>`，**Then** 这些文件 MUST 以 [[STR-001]] 残留形式呈现（计数 + 有界示例），且当残留可能影响「最新」判定时，view MUST 披露不确定性并以 [[STR-003]] 降级。

---

### User Story 2 - 降级团队被诚实呈现并给出修复路径 (Priority: P1)

维护者查看一个「定义不合模板但真实存在」的团队：`team.md` 没有 `binding` 块、`goal` 是内联长文本、正文矩阵没有 `agent` 列、`items.jsonl` 与持续运营脊柱缺失、pattern 是 `iteration`。他需要一眼看出：哪些事实不可得、为什么不可得、下一步该执行什么修复命令；同时 frontmatter 名册与矩阵数据不能被吞掉。

**Why this priority**: 这是生产证据的第二组失真（binding/goal/矩阵/缺失）；没有它，view 只能报告「降级」，不能把维护者带到修复动作。

**Independent Test**: 用复现生产形态的 fixture 执行一次 view：断言 binding 不可读带精确原因（命名缺失键或「无 binding 块」）与 `/speckit.team modify` 指针；内联 goal 是命名状态且带归一指针；矩阵缺 `agent` 列被标 `形态异常` 且 roster_delta 为 `不可比对`；`items.jsonl` 缺失带后果；非 continuous 团队的三件脊柱标注为按 pattern 不适用；9 名 frontmatter 成员全量呈现；退出码 5。

**Acceptance Scenarios**:

1. **Given** `team.md` 无 `binding` 块或 binding 键不齐，**When** 执行 `view <slug>`，**Then** 绑定 MUST 呈现为 `不可读` 并保留引擎给出的精确原因，附受制裁修复路径（`/speckit.team modify`；引擎写面 `goal-utils.py bind`），MUST NOT 填补缺省值。
2. **Given** frontmatter `goal` 是内联长文本且 `anchor_slug` 已声明，**When** 执行 `view <slug>`，**Then** 锚点身份 MUST 维持 `declared`（既有解析次序不变），`goal` MUST 呈现为命名状态（非 slug 形态）并附归一修复路径，MUST NOT 把内联文本猜成 slug。
3. **Given** 正文矩阵无 `agent` 列，**When** 执行 `view <slug>`，**Then** 矩阵 MUST 携带 `形态异常` 状态并点名缺列，已解析的矩阵行 MUST 仍被呈现；`roster_delta` MUST 呈现为 [[STR-002]] 并给原因，MUST NOT 使用「未记录」标签；frontmatter 成员与 `seats` / `stage_seats` 的声明状态 MUST 完整呈现。
4. **Given** `items.jsonl` 缺失、且团队 pattern 为 `iteration` 因而三件 continuous 脊柱缺失，**When** 执行 `view <slug>`，**Then** 台账缺失 MUST 带后果说明（无聚合状态、无非终态信号），脊柱 MUST 按「按声明 pattern 不适用的产物」呈现，MUST NOT 与真正的定义缺陷混为一谈，MUST NOT 编造零值。

---

### User Story 3 - 降级语义封闭、可测，健康输出保持不变 (Priority: P2)

框架维护者需要确认这次优化没有把查看器变成「更爱报错」或「更爱猜测」：降级原因是一个封闭集合，每个原因映射到封闭退出码集合中的恰一个，测试钉住映射；缺失与为空仍是诚实状态而不是错误；对健康团队，输出与基线逐字节一致；整个仓库仍然只有一个读取引擎。

**Why this priority**: 没有封闭语义与健康保真，前两条故事会以「修复一个失真的同时制造新失真」告终；但它是护航性价值，低于两条主呈现路径。

**Independent Test**: 对健康 fixture 分别运行基线提交程序与变更后程序，断言 stdout 逐字节一致、退出码相同；对降级 fixture 断言原因标识与退出码映射；扫描源码断言报告识别入口唯一、无第二读取器；全部测试经唯一入口执行。

**Acceptance Scenarios**:

1. **Given** 健康 fixture（完整 binding、全部报告紧凑命名、无残留、矩阵含 `agent` 列、无内联 goal），**When** 分别运行基线程序与变更后程序，**Then** 两次 stdout MUST 逐字节相同、退出码相同。
2. **Given** 任一降级形态（binding 不可读 / anchor 不可读 / 最新判定不确定），**When** 执行一次 view，**Then** 退出码 MUST 为 `5`，且输出的降级说明点名原因；原因集合外的取值与退出码集合外的取值出现数 MUST 为 0。
3. **Given** 产物缺失或为空（`items.jsonl`、`runs/`、脊柱），**When** 执行一次 view 且无其它降级原因，**Then** 退出码 MUST 为 `0`，状态标签 MUST 是四态词汇表中的成员。
4. **Given** 变更后的读取程序，**When** 扫描其源码与调用面，**Then** 报告识别/最新选择入口 MUST 唯一，MUST NOT 存在第二读取器或第二个识别规则；概览模式 MUST 复用同一入口。

### Edge Cases

- **`runs/` 存在但全部文件不可解析**：运行报告状态 MUST 是「残留 + 不确定性」，MUST NOT 是「为空」；退出码按 [[STR-003]] 降级（5）。
- **`runs/` 不存在 vs 存在但零条目**：维持「缺失」与「为空」的既有区分（103 data-model 四态词汇表）。
- **同一时间戳的报告与辅助产物**（如 `20261008T214100Z-report.md` 与 `20261008T214100Z-seat-result.md`）：报告 MUST 被选为最新；辅助产物 MUST NOT 参与 latest 竞争。
- **同时间戳的两份报告**：按文件名字典序确定性选择，并在呈现上保持稳定。
- **4-hex 后缀的多种位置**（如 `…-93cc-report.md`、`…-93cc-stage.md`）：都属于可解析时间戳的报告形态；具体分类规则由实现契约钉住，但 MUST 覆盖生产证据中的样本。
- **最新报告文件存在但不可读**（权限/IO）：MUST 呈现 `不可读` 并点名路径，MUST NOT 把全部字段静默渲染为 `未记录`。
- **binding 块存在但键不齐**：MUST 呈现引擎给出的缺失键名（如 `owner_id, origin`），与「无 binding 块」区分原因文本。
- **`goal` 与 `goal_slug` 并存或 `goal_slug` 旧拼写**：身份解析维持既有次序（`anchor_slug` > `goal_slug` > 推断），归一建议 MUST NOT 改变本次呈现的身份类型。
- **非 continuous 团队的脊柱文件部分存在**：已存在者正常列出，缺失者按 pattern 不适用标注；pattern 未声明时披露缺省语义来源。
- **归档团队（`lifecycle_state: archived`）**：维持既有正常呈现，不因本特性新增拒绝。
- **概览模式遇到非标准命名/残留团队**：「最近运行」列 MUST 与单团队视图使用同一解析与规范化结果；无法判定时 MUST 标注不确定性而不是留空或取旧值。概览不发起引擎读动作、不产生降级原因，退出码维持既有 `0/2` 域；不确定性 MUST 以行内标注披露。
- **`runs/` 目录本身不可读**（权限）：维持 `不可读` 状态并点名路径（既有行为）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 运行报告识别 MUST 以文件名**起始处**的**可解析 UTC 时间戳**为准，MUST NOT 依赖单一字面量模板；被接受的时间戳语形恰为封闭集 `YYYYMMDDThhmmssZ` / `YYYYMMDDThhmmZ` / `YYYY-MM-DDThh:mm:ssZ` / `YYYY-MM-DDThh-mm-ssZ` / `YYYY-MM-DDThhmmssZ`（日期段紧凑或 ISO 连字符，时间段 `hhmmss` / `hhmm` / `hh:mm:ss` / `hh-mm-ss`，紧随 `T` 与 `Z`），且 MUST 构成合法 UTC 日历时刻；仅日期前缀（如 `2026-10-07-progress-snapshot.md`）、非法月日时分与非 `Z` 时区标记一律不解析、不猜测（A-17）。时间戳之后、`.md` 之前的剩余段匹配 `(?:-[0-9a-f]{4})?-(?:report|stage)`（4-hex 冲突段可选，角色词为 `report` 或 `stage`）者为运行报告形态。识别规则 MUST 可判定且文档化于 view 的活契约面。
- **FR-002**: 「最新报告」MUST 是**解析时间戳最大者**；并列时间戳 MUST 以确定性次序决出——文件名字典序**升序第一份**（与既有实现的稳定次序一致）；MUST NOT 因某文件不匹配窄模板而回落到更旧的已识别报告；`as_of.latest_report_timestamp` 与概览「最近运行」列 MUST 携带同一**规范化解析值**（UTC、`YYYYMMDDThhmmssZ` 形态、秒精度），而不是窄模板的捕获组或未规范化的文件名片段；紧凑标准命名的文件其规范化值与文件名 token 相同（健康保真不受影响）。
- **FR-003**: `runs/` 内每个常规文件 MUST 被显式分为运行报告、辅助产物与残留三类，分类 MUST 只依据文件名并按固定次序判定：(1) 无 FR-001 语形的前导可解析时间戳 → 残留（即使角色词形似 progress-snapshot / judgment-contract，或文件不是 `.md`）；(2) 有可解析时间戳且剩余段为 FR-001 的运行报告形态 → 运行报告；(3) 有可解析时间戳但剩余段不是运行报告形态（如 `-verification.md`、`-seat-result.md`）→ 辅助产物。辅助产物 MUST NOT 被选为最新报告、MUST NOT 被计入 [[STR-001]] 残留；残留 MUST NOT 被计为运行报告；分类规则 MUST 显式、可判定。
- **FR-004**: 无任何可解析时间戳的文件 MUST 以 [[STR-001]] 残留形式呈现：**总数 + 有界示例**（示例上限与省略计数 MUST 同时给出）；MUST NOT 逐名无界转写整目录。
- **FR-005**: `runs/` 目录存在且残留计数 ≥ 1 时，「最新」判定即视为不可证明——残留文件无任何可解析时间戳，view MUST NOT 以文件 mtime 或内容推断其更旧——view MUST 显式披露不确定性并以 [[STR-003]] 进入降级语义；`runs/` 缺失或为空、或全部非报告文件均带可解析时间戳（仅辅助产物）时不产生不确定性。无任何可识别报告而仅有残留时，运行报告状态 MUST NOT 呈现为「为空」或「缺失」，MUST 表达「仅残留、最新不可确定」并由 [[STR-001]] 行给出计数与有界示例。MUST NOT 把任何更旧报告冒充为最新，MUST NOT 静默。
- **FR-006**: 概览模式的「最近运行」列 MUST 复用与单团队视图相同的识别与解析入口（同一引擎、同一规则、同一提取）；MUST NOT 维护第二套窄匹配或第二套最新选择。
- **FR-007**: `items.jsonl` 缺失 MUST 呈现为显式 `缺失` 状态并给出后果（无台账聚合计数、无非终态信号）；MUST NOT 以零值、空聚合或占位行冒充；`为空`（存在但无行）与 `不可读` 的既有区分 MUST 保持。
- **FR-008**: 持续运营脊柱（`constraints.md` / `STATE.md` / `run-log.jsonl`）的存在性 MUST 按团队**声明 pattern** 的适用性呈现：continuous 团队缺失 = 真实缺口；非 continuous 团队缺失 MUST 标注为「按声明 pattern 不适用的产物」并给出 owner 指针；pattern 未声明时 MUST 按 owner 的缺省语义呈现并披露该缺省来源，MUST NOT 发明默认。
- **FR-009**: 最新报告文件存在但不可读（权限/IO）时 MUST 呈现 `不可读` 并点名路径；MUST NOT 把该情况静默渲染成各字段 `未记录`。
- **FR-010**: 「缺失 / 为空 / 不可读 / 未记录」四态区分 MUST 维持（103 FR-015 的既有纪律），并 MUST 适用于本特性新增的产物面（残留、辅助产物、不可读报告、pattern 不适用）。
- **FR-011**: 绑定事实 MUST 仅在引擎读动作成功且三键（`owner` / `owner_id` / `origin`）齐备时呈现为已声明；缺 `binding` 块或键不齐 MUST 呈现引擎给出的精确原因（点名缺失键或无块事实）为 `不可读`；MUST NOT 以缺省值填补、MUST NOT 从其它字段推断。
- **FR-012**: 绑定不可读时 MUST 给出受制裁修复路径：`/speckit.team modify`（定义修复入口）与引擎写面 `goal-utils.py bind` 的指针，修复记录语义的 owner 是 `.specify/shared/definitions/anchor-definitions.md` § The Binding Record；view MUST NOT 自动执行修复。
- **FR-013**: frontmatter 声明 `goal` 键时（无论其值为内联长文本还是 slug 形态——`goal` 不是身份解析的声明键，身份次序只读 `anchor_slug` > `goal_slug` > 推断）MUST 呈现为命名状态（如「goal 需归一为 `anchor_slug`」）并给出修复路径（`/speckit.team modify` 将 `goal` 归一为 `anchor_slug`；需要派生锚点定义时经 `goal-utils.py migrate`）；取值形态 MUST NOT 改变该呈现或身份类型，MUST NOT 把任何 `goal` 值猜成身份 slug、MUST NOT 因 `anchor_slug` 已声明而静默略过该键。
- **FR-014**: `anchor_slug` 已声明时锚点身份 MUST 维持既有解析次序下的 `declared`（`anchor_slug` > `goal_slug` > 推断 slug）；归一建议 MUST NOT 改变本次呈现的身份类型，MUST NOT 触发任何迁移动作。
- **FR-015**: 正文 `## Static Structure` 矩阵缺 `agent` 列时 MUST 在矩阵组内呈现 `形态异常` 状态并点名缺失列；已解析的矩阵行 MUST 仍被完整呈现，MUST NOT 因缺列而隐藏矩阵或整段留空。
- **FR-016**: 两侧名册不可比对时 `roster_delta` MUST 呈现为 [[STR-002]] 并附原因；MUST NOT 使用「未记录」标签冒充；frontmatter 成员 MUST 全量呈现；`seats` / `stage_seats` 未声明 MUST 显式标注（含 owner 指针）；MUST NOT 出现静默空段。
- **FR-017**: 降级原因 MUST 是封闭集合 `{engine-degraded, [[STR-003]]}`：`engine-degraded` 表示引擎读动作未能产出必需事实（binding / anchor），[[STR-003]] 表示最新运行判定不确定；每个原因 MUST 映射到封闭退出码集合 `0/2/3/4/5` 中的恰一个（两者均为 `5`）；原因可以并存，一次 view MUST 逐个点名每个活跃原因且退出码仍为 `5`；映射 MUST 由测试逐项钉住。
- **FR-018**: 退出码 `5` MUST 表示「呈现已产出，但必需事实组不可读或不可确定」；既有的引擎读失败用例 MUST 保持 `5`；「缺失 / 为空」单独出现 MUST NOT 触发 `5`；文件级命名状态（`缺失` / `为空` / `不可读` / `未记录`）本身 MUST NOT 产生降级原因、也 MUST NOT 单独把退出码从 `0` 改为 `5`——`engine-degraded` 仅由引擎读动作失败（binding / anchor）触发，最新报告不可读仅是 FR-009 的命名状态；MUST NOT 产生集合外退出码。
- **FR-019**: 「不推断」规则 MUST 被钉住：绑定值、goal→slug、最新报告、名册差异 MUST 全都不允许推断或填充；输出的每一处呈现 MUST 是读得的事实或命名状态（含原因），MUST NOT 是猜测值。
- **FR-020**: 退出码与降级说明 MUST 在三处一致：`docs/reference/commands/team.md` 的 view 小节、`skills/internal/view-team/SKILL.md` 的错误导航闭集表、`scripts/python/team-view.py` 的声明（`--help` / 模块文档）；一致性 MUST 由测试断言（允许以「指向单一 owner 的指针」形态一致）。
- **FR-021**: 全部固定规则提取 MUST 继续只由单一读取引擎 `scripts/python/team-view.py` 完成；MUST NOT 新增第二读取器、第二存储、缓存、快照、索引或 registry；`goal-utils.py` MUST 零修改（只消费其只读动作）。
- **FR-022**: 健康输出保持 MUST 是可判定的封闭声明：健康谓词 = 完整三键 binding + 全部报告名为紧凑 `<8d>T<6d>Z-report.md` + 无残留 + 矩阵含 `agent` 列 + 无内联 `goal` + 所有报告可读；在满足该谓词的 fixture 上，**基线提交 `54c6efa8c` 的程序**与变更后程序的 stdout MUST 逐字节一致、退出码 MUST 相同（采集方式：同一 fixture 上两次运行的机器 diff）。具名允许增量（A-11）只适用于不满足健康谓词的输入，MUST NOT 以「其余不变」等未定义聚合承载验收。
- **FR-023**: 本特性 MUST NOT 改变运行报告命名的 owner（`skills/internal/create-team/SKILL.md` § Report contract）或 `team.md` schema；容错 MUST 落在读取侧；若实现提出任何形态变更，MUST 附带迁移或确定性拒绝（封闭声明），否则 MUST NOT 合并。
- **FR-024**: 渲染标签词汇表 MUST 保持单一活所有者：本特性新增/改用的标签（残留行的计数形态、[[STR-002]]、[[STR-003]]、pattern 不适用标注、goal 命名状态）MUST 并入 view 的活契约面作为唯一 owner；`.specify/specs/103-team-view/data-model.md` § Rendering Line Types 保留为日期化记录，实现 MUST NOT 让它继续充当新标签的活 owner。
- **FR-025**: 六组信息与既有字段 MUST 全部保留；新增状态行 MUST 增补而非删除、重排或合并既有行；`view-team` 技能 MUST 维持「程序 stdout 逐字重发 + 正文外降级说明」的重发规则，降级说明 MUST NOT 替代、删减或改写六组正文。

### Key Entities *(include if requirement involves data)*

- **Run Report File**: `.specify/teams/<slug>/runs/` 下的运行报告；命名 owner 是 create-team § Report contract（`<UTC-timestamp>-report.md`）；本特性只扩展**识别**，不改命名。
- **Report Timestamp**: 从文件名起始部分解析出的 UTC 时刻；最新选择、`as_of` 指针与概览列的唯一排序依据。
- **Auxiliary Artifact**: 同目录的非报告文件（verification / seat-result / progress snapshot 等）；与运行报告、残留三分类。
- **Residue**: 无可解析时间戳的文件集合；以计数 + 有界示例呈现，可触发 [[STR-003]] 不确定性。
- **Binding Record**: 团队的三键所有权记录（owner / owner_id / origin）；含义 owner 是 `shared/definitions/anchor-definitions.md` § The Binding Record。
- **Continuous Spine**: `constraints.md` / `STATE.md` / `run-log.jsonl` 三件；适用性 owner 是 `skills/internal/create-team/references/operating-loops.md`。
- **Degradation Reason**: 封闭集 `{engine-degraded, report-recognition-uncertain}`；每个原因映射恰一个封闭退出码。
- **Rendering Label Vocabulary**: 状态与声明标签的封闭词汇表；活 owner 由本特性契约承接（FR-024）。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它修改一个 Python 标准库读取程序、其技能/文档措辞与测试，并消费既有的 Python 解释器、pytest 运行器、唯一测试入口与既有 `goal-utils.py` 引擎的只读动作。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段只保留引用）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（报告名时间戳解析、目录遍历、前沿解析与台账聚合；测试夹具生成） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python` 下限；本特性零新增第三方依赖 | `pyproject.toml` | 读取程序与新增测试在 `>=3.8` 解释器上经唯一入口 `scripts/bash/run-tests.sh` 通过；新增第三方 import 为零 | FR-001, FR-021 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约、集成与单元测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；本特性零新增依赖 | `pyproject.toml` | `scripts/bash/run-tests.sh` 运行新增 `contract` / `integration` / `unit` 测试，结果集相对 implement 入口基线零新增红 | FR-017, FR-022, FR-025 | EP-001 |
| RS-003 | POSIX `bash` 运行时（唯一测试入口） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增版本下限；本特性不改动该入口 | `scripts/bash/run-tests.sh` | 新增测试全部经该入口执行且一次退出 0；不直接调用解释器级测试命令 | FR-022, FR-025 | EP-001 |
| RS-004 | 既有 `goal-utils.py` 引擎的只读动作面（`binding`、`list`、`targets --list`；`bind` / `migrate` 仅作为修复路径被点名，不被 view 调用） | signed-contract | 既有 anchor / goal 引擎（本特性只读消费，零修改其动作集与退出码闭集） | 仓内既有实现，无外部版本面；pin 由 `--help` 声明的动作集固定 | `scripts/python/goal-utils.py` | 绑定与锚点事实只经三个读动作取得；读取程序不含第二套解析路径；本特性对该引擎文件零修改 | FR-011, FR-012, FR-014 | EP-002 |
| RS-005 | 单一读取引擎 `scripts/python/team-view.py`（报告分类/时间戳解析/最新选择/降级原因/渲染标签的交付面） | in-scope | 本特性修改的 framework 源程序（既有 103 交付面） | 不适用（无外部版本面）；路径由 103 A-16 定稿 | `scripts/python/team-view.py` | `-h` / `--version` 退出 0 且零写盘；健康 fixture 输出与基线程序逐字节一致；降级 fixture 命中封闭原因与退出码映射 | FR-001, FR-002, FR-003, FR-006, FR-017, FR-018, FR-021, FR-022 | EP-003 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在生产复现 fixture（旧 `20261124T074500Z-report.md` + 更新的 `20261125T121924Z-93cc-stage.md` + `2026-11-25T140000Z-report.md` + 同时间戳 `-seat-result.md` + 两个无时间戳文件）上，一次 view 的「最近报告」等于解析时间戳最大者；旧报告冒充最新次数 = 0；5 个报告/辅助样本的分类命中率 = 5/5；[[STR-001]] 残留行同时给出总数与有界示例（示例数 ≤ 上限，且报告省略数） **Path**: final
- **SC-002**: 三个实测团队的命名复刻 fixture（全部报告为非标准可解析命名）在变更后：运行报告状态 ≠ `为空` 且 ≠ `缺失`；「最近报告」等于解析最新文件名；退出码 = 0；这些团队的报告样式文件识别覆盖率 = 13/13 **Path**: final
- **SC-003**: 在生产形态降级 fixture（无 binding 块、内联 goal、无 `agent` 列、`items.jsonl` 缺失、`iteration` pattern 下三件脊柱缺失、最新报告不可读）上，一次 view 退出码 = 5，且六个具名状态全部出现：绑定 `不可读`（含精确原因）、goal 命名状态 + 修复路径、矩阵 `形态异常`（点名缺列）、`roster_delta` = [[STR-002]]、台账 `缺失`（含后果）、脊柱「按 pattern 不适用」；frontmatter 成员覆盖 = 输入成员数（9/9 形态）；`/speckit.team modify` 指针出现 ≥ 1 次；编造零值/占位值出现数 = 0 **Path**: final
- **SC-004**: 健康 fixture 上，基线提交 `54c6efa8c` 的程序与变更后程序的 stdout 逐字节相同（机器 diff 行数 = 0）、退出码相同；允许增量集合对满足健康谓词的输入为空 **Path**: final
- **SC-005**: 降级原因→退出码映射逐项命中（`engine-degraded` → 5、[[STR-003]] → 5，2/2）；退出码集合外取值出现数 = 0；仅「缺失/为空」的 fixture 退出码 = 0（1/1）；`-h` / `--version` 退出 0 且零写盘（2/2） **Path**: supporting
- **SC-006**: 同一 fixture 上，概览「最近运行」列的值与单团队「最近报告」的解析时间戳一致率 = 100%；源码扫描中报告识别/最新选择入口数 = 1，第二匹配入口出现数 = 0 **Path**: supporting
- **SC-007**: 在健康、降级、概览三个场景各执行一次 view，前后 fixture 工作树内容哈希一致（新增/修改/删除文件数 = 0） **Path**: supporting
- **SC-008**: 新增与既有相关测试经 `scripts/bash/run-tests.sh` 一次执行退出码 = 0；新增测试覆盖 FR 清单点名的全部形态（非标准命名、辅助产物、残留、不确定性、缺 binding、内联 goal、缺 agent 列、缺失产物、不可读报告、健康保真） **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: fixture 集成测试的断言输出（最新文件名、分类计数、残留行解析），由 `scripts/bash/run-tests.sh` 执行。
- **SC-002 Source**: 实测命名复刻 fixture 的集成测试断言（状态标签、最新文件名、覆盖计数）。
- **SC-003 Source**: 降级 fixture 集成测试的断言输出（逐状态字面量与修复路径计数）。
- **SC-004 Source**: 测试内用 `git show 54c6efa8c:scripts/python/team-view.py` 物化基线程序，与工作树程序在同一 fixture 上各运行一次并做字节 diff（机器采集，无人工清单）。
- **SC-005 Source**: 退出码矩阵测试的逐项通过计数；`--help`/`--version` 的写盘快照比较。
- **SC-006 Source**: 概览与单团队同 fixture 的值比对断言；源码入口扫描断言（单一函数/正则）。
- **SC-007 Source**: 工作树内容哈希快照（测试开始前 / 结束后各一次）求差。
- **SC-008 Source**: `scripts/bash/run-tests.sh` 的退出码与测试汇总。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"未识别（unrecognized）"` | FR-003, FR-004, SC-001, residue-line tests |
| `STR-002` | `"不可比对（not comparable）"` | FR-016, SC-003, roster-delta tests |
| `STR-003` | `"report-recognition-uncertain"` | FR-005, FR-017, SC-005, degradation-mapping tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!--
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-11-26

- 无人值守裁决：本轮不发起阻塞式提问；候选问题按「可判定 + 最小改动」自裁决并逐条写回对应节，再在下方记录。同作者检测门未触发：本规格的输入是用户提供的生产证据与本仓实测语料，非上阶段作者产物。
- Q: 规格编号与分支如何落地？ → A: **编号 108、分支保持 `108-team-view-degradation`**。`create-new-requirements.sh` 会把当前本地分支计入编号空间而派生 109 并新建分支；按 107 先例手工从模板脚手架并记录偏差（A-16）。
- Q: 报告命名契约改不改？ → A: **改读取侧，不改命名 owner**。用户证据给出二选一；程序接受真实可解析命名不要求任何团队迁移，符合「既有团队不需要迁移」（A-3）。
- Q: 最新报告按什么排序？ → A: **按解析后的 UTC 时间戳取最大**，并列按文件名字典序；不允许回落到更旧的已识别报告（A-4）。
- Q: 辅助产物如何归类？ → A: **三分类（运行报告 / 辅助产物 / 残留）**，规则显式可判定；辅助产物不参与 latest、不计入残留（A-5）。
- Q: 降级原因集合多大？ → A: **最小封闭集** `{engine-degraded, report-recognition-uncertain}`，两者都映射退出码 5；缺失/为空不算降级（A-9）。
- Q: 非 continuous 团队的脊柱缺失怎么呈现？ → A: **按声明 pattern 的适用性呈现**，owner 指向 `operating-loops.md`；不发明默认（A-8）。
- Q: 「既有团队不受影响」与实测三个团队输出会变化如何统一？ → A: 精确化为**健康谓词**上的逐字节保真（A-10）+ 对不满足谓词的输入列出具名纠正增量（A-11）；不迁移任何团队定义。
- Q: Related Feature 绑定？ → A: 保持 `Need clarification`，由 `/speckit.clarify` 按 Feature Binding Rules 解析（本阶段不建 Feature、不查表）。

### Session 2026-11-26（无人值守 clarify 阶段，Feature 绑定与五点残留歧义裁决）

- Q: `Related Feature` 绑定到哪个既有 Feature，是否新建？ → A: 绑定既有 **Feature 027（Team Management）**，以索引切片行 108 登记 `Draft`（详情指针 `.specify/features/027-team-management.md`）；不新建 Feature，027 状态保持 `Ready for Review` 不回退。依据：027 拥有 `/speckit.team` 命令面与团队档案层，本规格只修订 `view` 读取程序 / 技能 / 测试，是 103-team-view 的直接后续切片；036 / 042 / 103-team-view 直接绑定 027 的先例成立。Brief 的 leading candidate `103-team-view` 是已定稿 spec 编号而非 Feature ID（Feature 103 = Technical Debt Governance），按查找结果绑定其父 Feature（binding-precedent heuristic）。
- Q: 报告名识别接受哪些时间戳语形、何谓残留？ → A: 封闭语形集 = 日期段 `YYYYMMDD` 或 `YYYY-MM-DD` × 时间段 `hhmmss` / `hhmm` / `hh:mm:ss` / `hh-mm-ss`，紧随 `T` 与 `Z`，且构成合法 UTC 时刻；运行报告形态的剩余段 = `(?:-[0-9a-f]{4})?-(?:report|stage)`。无此前导时间戳的**任何**常规文件（含仅日期前缀 `2026-10-07-progress-snapshot.md`、非法时刻、非 `.md` 文件）一律为 [[STR-001]] 残留；全部判定只看文件名、不做模糊猜测（A-17）；具体 regex 由 plan 契约钉住（骨架见 FR-001 / FR-003）。`as_of.latest_report_timestamp` 与概览列用同一规范化值（UTC、`YYYYMMDDThhmmssZ`）；同时间戳并列取文件名字典序升序第一份（既有稳定次序）。
- Q: 残留如何进入降级（不确定性判据）？ → A: `runs/` 存在且残留 ≥ 1 即判「最新不可证明」，以 [[STR-003]] 进入降级、退出码 `5`——不存在「证明残留更旧」的受制裁路径（mtime / 内容推断被拒：非确定且超出只读引擎契约）；`runs/` 缺失或为空、或仅带时间戳的辅助产物时不产生不确定性。A-5 中「progress snapshot」示例因此限定为带可解析时间戳者；无时间戳的 snapshot 命名走残留（与实测语料 46 文件 = 28 合规 + 16 带戳非合规 + 2 无戳 的计数一致）。
- Q: 降级原因到退出码如何映射、边界在哪？ → A: 封闭原因集 `{engine-degraded, [[STR-003]]}` 逐项映射 `5`（2/2），原因可并存且 MUST 逐个点名；文件级命名状态（`缺失` / `为空` / `不可读` / `未记录`）本身不产生原因、不单独改变退出码；最新报告不可读只是 FR-009 命名状态；概览不发起引擎读动作、不产生原因，维持既有 `0/2` 退出域并以行内标注披露不确定性；退出码闭集不变 `0/2/3/4/5`（不新增）。
- Q: binding / goal 归一是只呈现指引还是执行修复？ → A: **只呈现指引、view 零写**：`/speckit.team modify` 是定义修复入口，`goal-utils.py bind` / `migrate` 只作为引擎写面被点名、不被 view 调用（RS-004 零修改）；`goal` 键的任何取值（含 slug 形态）都呈现为命名状态，身份类型维持既有次序结果（`anchor_slug` > `goal_slug` > 推断）；SC-007 以工作树哈希差钉住零写盘。
- Q: 矩阵缺 `agent` 列的呈现与名册差异措辞？ → A: 正文矩阵组携带 `形态异常` 并点名缺列 `agent`，已解析矩阵行仍完整呈现（不隐藏、不留空）；`roster_delta` 呈现为 [[STR-002]] 并附原因（MUST NOT 用「未记录」冒充）；frontmatter 成员全量列出；`seats` / `stage_seats` 未声明时显式标注并附 owner 指针；不出现静默空段。
- Q: 健康保真、单一引擎与迁移 / 拒绝的边界？ → A: 健康谓词 fixture（三键 binding、全部紧凑 `-report.md`、无残留、矩阵含 `agent` 列、无 `goal` 声明、报告可读）上，基线 `54c6efa8c` 程序与变更后程序 stdout 逐字节一致、退出码相同；报告识别 / 最新选择入口唯一且概览列复用同一入口；唯一读取交付面 `scripts/python/team-view.py`，`goal-utils.py` 零修改；不改命名 owner（create-team § Report contract）与 `team.md` schema → 既有团队零迁移；若实现提出任何形态变更 MUST 附带迁移或确定性拒绝，否则 MUST NOT 合并（FR-023）。
