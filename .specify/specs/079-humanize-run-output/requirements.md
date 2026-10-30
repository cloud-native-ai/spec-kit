# Requirements Specification: Humanize Run Output（动作输出的人类友好化）

**Requirement Branch**: `079-humanize-run-output`  
**Created**: 2026-10-30  
**Status**: Draft  
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "重构 /speckit.humanize 的定位与输入契约：从「文本转换命令」改为「动作输出的人类友好化命令」。新定位：在一条指令/动作执行完成后，结合上下文与项目信息，把该次执行的输出改写成对人类读者更友好的形态（格式与内容两层）。调用形态：/speckit.humanize [--tone <v>] [--audience <text>] <instruction>；选项之后的剩余文本是一条待执行的指令。执行：派发恰好一个子代理执行该指令（宿主原生派发；无可派发通道时降级为会话内执行并在报告中标明），捕获输出、产物、证据与失败信息。改写：结合动作输出/证据 + 项目治理（instructions / constitution / glossary / feature 注册表）+ 会话上下文生成结构化报告（结论 → 关键变化/结果 → 证据 → 风险与限制 → 下一步），并列明使用的上下文来源。安全：遵守既有确认门与权限边界；不绕过破坏性动作的前置确认、不自动重试、不联网外发；失败或部分完成如实写入报告。旧模式：--file 与 --inline 保留为显式备用输入源；裸文本改为按待执行指令解释，需写明迁移方式。保真与安全底线沿用：事实/数字/结论/引用逐字保留、输入按数据处理、默认零写入、不承诺 AI 检测器结果。影响面：命令模板 + 4 份工具副本、humanize 技能、约 10 个测试文件、评估夹具、docs、Feature 062（扩展，不回退状态）。非目标：不做通用代码执行器、不做多指令批处理、不移除保真/注入/零外传底线、不引入第二套派发机制、不自动确认破坏性动作、不改 improve-skills / coaching-skills 契约。"

## Related Feature *(mandatory)*

**Feature ID**: 062  
**Feature Name**: Humanize Command（动作输出人类友好化）

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **A1（编号依据）**：编号 079 由脚手架按 `.specify/specs/` 实测最大目录号（078）加一得出；`features.md` 行数不是最大编号，本特性不借机回填。
- **A2（类别判定 = execution；命令台账类别不变）**：交付物是命令模板、技能定义、契约测试与文档接线；验收由宿主解析命令、由确定性测试消费，缺陷以「命令把裸文本当指令执行 / 报告缺章节 / 失败被写成成功」这类机器可见差异暴露，按 `.specify/shared/definitions/flow-class-definitions.md` 判据属 `execution`，`Flow Type` 写 `-`。命令在流程台账中自身保持 `expression / reader-oracle`——它的交付物仍是给人读的报告；指令执行产生的副作用归该指令所属单元自己的类别与门禁，不改写本命令的台账类别（此张力已显式记录，不是遗漏）。
- **A3（Feature 绑定目标）**：本特性是现有 **Feature 062（Humanize Command，Status: Implemented）** 的扩展，不新建 Feature；按扩展切片规则状态不回退，Feature 详情与索引 `Last Updated` 记录本次扩展；最终绑定由 `/speckit.clarify` 落定。
- **A4（破坏性输入变更）**：裸文本（选项之后的剩余文本）一律解释为**待执行指令**；改写既有文本必须显式使用 [[STR-008]] 或 [[STR-009]]。这是对旧调用方式的破坏性变更，命令模板、技能与 docs 必须同时写明迁移方式，且每次裸文本调用 MUST 输出一行迁移提示（「已按指令执行；改写文本请用 --file/--inline」）；MUST NOT 为兼容旧行为而猜测「这段文本像内容还是像指令」。迁移提示是**语言不变的固定通知**（与五个英文小节标题同属契约面固定 literal，不随正文语言翻译、不因 `--tone`/`--audience` 改写）；它是调用级会话通知，只在会话回显一次，MUST NOT 写入 `--output` 文件。
- **A5（派发拓扑）**：派发 MUST 走既有 `run-agent` 载体（它内部按宿主能力使用原生子代理）；宿主无原生派发通道时降级为 humanize 会话内执行，并在报告中以 [[STR-007]] 标明。不引入第二套派发机制；`run-skills` / `run-agent` 仅作为既有降级入口，不承担新的编排语义。
- **A6（上下文来源、报告作者与报告义务）**：**报告由 humanize 主会话撰写**——子代理只回传结果信封（输出/产物/证据/失败），不写最终报告，因为会话上下文只在主侧可得。上下文恰取三源——动作输出/证据、项目治理（`instructions` / `constitution` / `glossary` / Feature 注册表）、本次会话上下文。任一来源不可得时仍产出报告，但必须在 [[STR-004]] 声明缺失；MUST NOT 编造事实或引用不存在的工作。
- **A7（报告形态与语言）**：结构化报告使用稳定英文小节名（[[STR-001]]…[[STR-005]]）；正文语言取**封闭语言域** `zh` / `en`，判定顺位固定为：① 指令主语言（按 062 FR-013 的可复现计数口径：剔除受保护内容与纯数字/符号后比较中文字符数与拉丁词数，占比高者胜，并列取首个非空正文段落）→ ② 项目治理（instructions / glossary）的主语言（同一口径）→ ③ 回退 `en`；每一次回退 MUST 在 [[STR-004]] 声明。第三种书写系统（既非中文也非拉丁，如西里尔、阿拉伯、日文假名、韩文）在 ①② 均不可判时按 ③ 处理，其原文 MUST 逐字引用、MUST NOT 翻译或音译。语言判定只影响正文表述，不影响小节标题、元数据键名与 verdict token（后三者恒为英文原样）。执行载体标记（[[STR-006]]/[[STR-007]]）以一行元数据放在五个 H2 之前；小节名是机器可判定的契约面，正文不是。
- **A8（安全边界）**：指令执行沿用目标项目既有的确认门与权限边界；humanize 只负责「执行后改写」，不改变、不代答、不绕过指令自身的确认；破坏性动作被拒绝后，报告如实记录拒绝，不执行替代动作。
- **A9（保真、注入与零写入沿用）**：既有保真底线、输入按数据处理（注入防护）、不承诺检测器结果全部沿用。**零写入的范围收窄为 humanize 自身的写入**：未给 `--output` 时不得写报告或副本；指令自身产生的写入是执行结果的一部分，MUST 在报告 [[STR-003]]/[[STR-002]] 中逐项列出，不视为违反零写入。运行期并发占位（FR-030）是受制裁临时根下的瞬时状态，既不是报告也不是副本，运行结束即移除，MUST NOT 出现在 `git status`。
- **A10（旧内容模式的适用范围）**：[[STR-008]] / [[STR-009]] 仍是完整的改写入口，受单输入源规则、格式一致性与保真底线约束；它们不触发子代理执行，也不生成动作报告。
- **A11（影响面封闭集）**：需手改的活接线面 MUST 由「无限制发现 + 分类规则 + 闭环守卫」派生；规则、类别定义与守卫判据的唯一所有者是本文 § Wiring Surface — A11 Closed Set。MUST NOT 把该集合委托给可再生的 `tasks.md`，MUST NOT 用人工挑选的路径清单代替发现命令。历史记录、dated record 与评估夹具语料不改写。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条指令跑完，拿回一份人读得懂的报告 (Priority: P1)

用户在 `/speckit.humanize` 后写一条指令（例如「跑一下 078 的 closure 并告诉我结果」）。命令派发一个子代理执行它，然后结合动作输出、项目信息与会话上下文，交回一份结构化的主语言报告：结论先行，证据与风险齐备。

**Why this priority**: 这是新定位的全部价值；没有这条闭环，命令仍只是文本转换器。

**Independent Test**: 用一条可确定产出的夹具指令跑一次 humanize，检查报告五节齐备、结论与夹具输出一致、证据指向真实产物。

**Acceptance Scenarios**:

1. **Given** 一条可执行的指令与可用的原生派发通道，**When** 用户调用 `/speckit.humanize <instruction>`，**Then** 子代理恰好执行一次（派发记录为 [[STR-011]] `1`），报告按 [[STR-001]]→[[STR-002]]→[[STR-003]]→[[STR-004]]→[[STR-005]] 的顺序产出。
2. **Given** 指令产出了具体产物（文件/测试读数），**When** 生成报告，**Then** [[STR-003]] 引用真实路径与读数，[[STR-002]]/[[STR-003]] 列出指令造成的写入，[[STR-004]] 列出至少一条限制或语言适配的「无已知风险」。
3. **Given** 指令执行失败，**When** 生成报告，**Then** [[STR-001]] 明确写失败，[[STR-003]] 给出失败证据，MUST NOT 出现成功措辞。

---

### User Story 2 - 报告要“友好”：结论先行、证据可查、来源可追 (Priority: P1)

报告不是把原始日志套个壳：它先说结论，再讲关键变化/结果，用证据支撑，把风险与限制摊开，最后给下一步；同时列明这次用了哪些上下文来源。

**Why this priority**: 「格式与内容两层友好」是本特性的定义性要求。

**Independent Test**: 对同一动作输出分别生成报告，检查结论位于首节、每条结论有证据指针、上下文来源清单非空且与实际读取一致。

**Acceptance Scenarios**:

1. **Given** 一次运行捕获的结果信封（不重复派发），**When** 对同一信封生成两份报告，**Then** 结论先于细节，关键变化按 FR-019 的封闭影响尺排序。
2. **Given** 只读到了部分上下文源，**When** 生成报告，**Then** 来源清单只列状态为 `read` 的源，缺失项写入 [[STR-004]]。
3. **Given** 用户给出 `--audience` 或 `--tone`，**When** 生成报告，**Then** 表达层适配生效，但事实层与证据引用不变。

---

### User Story 3 - 安全与诚实：不绕过确认、不掩饰失败、不自动重试 (Priority: P2)

指令若含破坏性动作，必须先走该动作自己的确认门；被拒绝就不执行，报告如实写拒绝。执行失败或部分完成，报告不得修饰成成功；不得自动重试，不得联网外发。

**Why this priority**: 让命令获得“执行指令”的能力，就必须同时约束它不能越权或粉饰。

**Independent Test**: 构造一条需确认的破坏性指令并在确认处拒绝，检查未产生副作用且报告记录拒绝；再构造一条失败指令，检查报告不含成功措辞。

**Acceptance Scenarios**:

1. **Given** 指令包含破坏性动作，**When** 确认被用户拒绝，**Then** 不发生该动作，报告 status 记 `denied`（[[STR-014]]）、verdict 为 `aborted`、记录拒绝原因与未执行范围；humanize 转达请求或答复不等于代答。
2. **Given** 指令失败或超时，**When** 生成报告，**Then** 失败被如实记录，运行不自动重试；超时判定归执行载体/宿主所有，humanize 不自设阈值。
3. **Given** 一次运行结束，**When** 审计副作用，**Then** humanize 自身未联网、未在未给 `--output` 时写报告；指令自身的联网与写入（如有）已按 [[STR-003]] 披露。

---

### User Story 4 - 旧的文本改写入口仍可用，迁移路径清楚 (Priority: P2)

需要改写既有文本的用户改用 [[STR-008]] 或 [[STR-009]]，行为与保真底线保持；直接写裸文本会被当作指令执行，文档与提示消息必须把这一点讲清楚。

**Why this priority**: 旧用户不能被静默改变行为；迁移必须可发现。

**Independent Test**: 同一段文本分别以 [[STR-009]] 与裸文本调用，前者产出改写文本，后者被当作指令执行（夹具中以可观察的指令效果区分）；文档给出迁移示例。

**Acceptance Scenarios**:

1. **Given** [[STR-008]] 或 [[STR-009]]，**When** 调用，**Then** 走原改写流程，输出格式与输入一致，保真底线不变。
2. **Given** 裸文本，**When** 调用，**Then** 它被执行而不是被改写；文档与命令说明写明迁移方式。

### Edge Cases

- 裸文本其实不是可执行动作（像聊天问题/散文）：信封 status 为 `not-an-action`（[[STR-015]]），报告 verdict 取 `success` 但 [[STR-001]] 写「未执行任何动作」，[[STR-003]] 写 [[STR-010]]（派发记录行保留），并附迁移提示。
- **运行模式**下同一工作树根并发两次 humanize，或 `--output` 目标正被另一次运行占用：后到者 MUST 拒绝并点名冲突运行/路径；指令内部再嵌套 humanize（命中封闭 token 集）MUST 拒绝。内容模式不受此约束（FR-030）。
- 只有选项没有指令且无内容源：拒绝并给用法，不派发子代理。
- 指令为空或纯空白：拒绝。
- 子代理通道不可用：MUST 降级为会话内执行（不是可选），报告以 [[STR-007]] 标明、派发记录 [[STR-011]] 为 `0`；不得冒充 [[STR-006]]。
- 指令被用户中止：报告记录中止点与已完成部分，verdict 写 `aborted`，不得写完成。
- 指令执行到需确认步骤但用户明确拒绝：status `denied`（[[STR-014]]）、verdict `aborted`，记录拒绝点与未执行范围，不执行替代动作。
- 指令产出为空（无输出、无产物）：报告如实写「无可报告输出」，[[STR-003]] 写 [[STR-010]]，保留派发记录行，不得编造证据。
- 项目无 `.specify/` 治理文件：报告只列实际可得的来源，缺失项入 [[STR-004]]。
- `--tone` 非法：拒绝并列出支持集合；`--audience` 为空或纯空白：视为未提供，不拒收、不改变表达层缺省。
- `--output` 指向不可写路径：拒绝写入并报告，不产生部分文件。
- 运行模式 `--output` 写入完整五节报告与元数据行（载体标记、verdict、派发记录）；迁移提示只在会话回显，不写入文件。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 调用与输入解析

- **FR-001**: `/speckit.humanize` MUST 接受两个位置语义：选项集（`--tone` / `--audience` / [[STR-008]] / [[STR-009]] / `--output` / `--force`）与**待执行指令**。选项之后的剩余文本 MUST 解释为待执行指令；裸文本 MUST NOT 再被解释为待改写内容。
- **FR-002**: 当给出 [[STR-008]] 或 [[STR-009]] 时，输入 MUST 按显式备用内容源处理，受既有单输入源、扩展名与空输入拒收规则约束；本路径 MUST NOT 派发子代理执行任何内容。内容源与非空指令同现时 MUST 拒绝并点名两者（FR-006 优先于任何「内容优先」的猜测）。
- **FR-003**: 当既无显式内容源、也无非空指令时，命令 MUST 拒绝并给出用法与迁移提示（裸文本→指令；改写文本→[[STR-008]]/[[STR-009]]），MUST NOT 猜测用户意图。
- **FR-004**: `--tone` 的取值域与拒收语义 MUST 沿用现有契约（空值与纯空白按集合外拒绝）。`--audience` 是自由文本、只作用于表达层；空字符串或纯空白 MUST 视为**未提供**（不拒收、不改变表达层缺省），非空值 MUST NOT 改变事实层。`--force` 的覆盖语义 MUST 沿用现有契约。`--output` 的写入语义按模式分属：内容模式沿用现有契约（FR-023 引用），运行模式由 FR-024 拥有（含运行模式的扩展名封闭集）；本 FR MUST NOT 为运行模式保留「扩展名与输入格式族对齐」的语义。
- **FR-005**: 命令模板 MUST 在入口处写明破坏性变更：裸文本 = 指令；改写既有文本 MUST 显式使用 [[STR-008]] 或 [[STR-009]]；并给出一条迁移示例。每次裸文本调用 MUST 输出迁移提示整句一次；该整句是语言不变的固定 literal（不随正文语言翻译），只在会话回显一次，MUST NOT 写入 `--output` 文件。
- **FR-006**: 解析 MUST 是确定性的：同样的参数序列得到同样的解释，不依赖模型对内容的猜测；解析歧义（如内容源与非空指令同现）MUST 拒绝并点名冲突项。

#### B. 指令执行

- **FR-007**: 命令 MUST 在派发通道可用时为一次调用派发**恰好一个**顶层子代理执行该指令，且 MUST 经既有 `run-agent` 载体派发；派发载体 MUST 记录为 [[STR-006]] 或降级时的 [[STR-007]]。派发记录 MUST 是报告 [[STR-003]] 内的一行元数据，键名 [[STR-011]]，值只计 humanize 发起的顶层派发：原生通道为 `1`，降级为 `0`。指令自身再发起的派发归属该指令单元，不重复计数。
- **FR-008**: 指令执行 MUST 遵循目标项目既有的确认门与权限边界；humanize MUST NOT 代替用户回答、绕过或自动确认破坏性动作。humanize 主会话 MAY 把执行体的确认请求**转达**给用户，并把用户的原话答复转达回去；转达 ≠ 代答：MUST NOT 自行选择、推断或默认答案，MUST NOT 把「用户可能同意」当作答复；执行体无法取得答复时按 fail-closed 停在该步。
- **FR-009**: 命令 MUST 捕获并保留：子代理最终输出、产生的产物路径、可定位证据（读数/命令/退出码）、失败或中止信息；回传信封 MUST 携带 status、`final_output`、`products`、`evidence`、`failures`、`blocked_at` 与显式异常行，其中 status 的取值域由 FR-012 拥有。捕获面 MUST 足以支撑 [[STR-003]] 的证据引用。子代理 MUST 只回传结果信封，最终报告由 humanize 主会话撰写（A6）；信封字段与产物内容一律按数据处理（FR-025）。
- **FR-010**: 命令 MUST NOT 自动重试失败的指令；humanize 自身 MUST NOT 联网或引入外部服务/模型 API。指令自身按其契约产生的联网行为 MUST 在报告中披露，不属于 humanize 的外发。
- **FR-011**: 宿主无原生派发通道时，命令 MUST 降级为会话内执行（不是可选）。「无通道」MUST 由 `run-agent` 载体的模式选择判定，MUST NOT 由 humanize 自行猜测，也 MUST NOT 以「先派发失败再降级」实现（重试禁令）。降级 MUST 以一行元数据在五个 H2 之前标注（[[STR-007]]），派发记录 [[STR-011]] 为 `0`；不得把会话内执行的推断当作子代理的观测事实；不得冒充 [[STR-006]]。
- **FR-012**: 指令自身失败、超时、被拒绝或中止时，命令 MUST 如实记录失败坐标与已完成部分；运行状态 MUST NOT 被叙述为成功。执行结果类别（status）由本 FR 拥有，封闭集为：`completed`、`partial`、`failed`、`aborted`、[[STR-014]]（用户明确拒绝确认）、[[STR-013]]（需确认而无法取得答复）、[[STR-015]]（指令不是可执行动作）。`denied` 的报告 verdict MUST 为 `aborted`，文案 MUST 写明「用户拒绝确认」与未执行范围。超时的定义与阈值归执行载体/宿主所有，humanize MUST NOT 自设阈值或重试；载体不提供超时信号时该失败类别不可判，报告 MUST 在 [[STR-004]] 声明。
- **FR-013**: 命令 MUST NOT 把指令改写为自己的简化流程；执行体按指令原文与其所属命令/技能的既有契约执行。

#### C. 上下文装配

- **FR-014**: 生成报告前，命令 MUST 装配三类上下文：动作输出/证据、项目治理（`instructions` / `constitution` / `glossary` / Feature 注册表）、本次会话上下文。每个来源 MUST 带一个可观察状态：`read`（该来源的摘要 / 行投影 / 段落摘录在本轮装配中被实际载入，可由报告来源清单与对应事实指针复核）、`not-read`（本轮未载入，含未尝试）、`unavailable`（路径不存在或不可读）；会话上下文同取这三个状态。装配是**尝试并记录**（attempt-and-record），不是必须可读。读取 MUST 按摘要优先，不得把机器管理的原始数据整文件注入。
- **FR-015**: 报告 MUST 列出本轮状态为 `read` 的上下文来源；`not-read` / `unavailable` MUST 在 [[STR-004]] 显式声明缺失。来源清单 MUST NOT 列出未载入的来源；`used` 不再是独立判据（`read` 已含实际载入），MUST NOT 以「是否被引用」二次判定来源。
- **FR-016**: 上下文补全 MUST 只使用已蕴含或可严格推出的信息；MUST NOT 引入新事实、新数字、新来源或新因果。
- **FR-017**: 保真底线（事实/数字/单位/日期/名称/结论/因果/引文/代码/路径/URL/标识符）MUST 在报告与旧内容模式中同时生效。

#### D. 报告生成

- **FR-018**: 报告 MUST 按顺序包含五个固定小节：[[STR-001]]、[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]；执行载体元数据（[[STR-006]]/[[STR-007]]）MUST 位于五个 H2 之前的独立一行，不构成第六节；裸文本调用的迁移提示行（会话面）紧随载体标记行；写入 `--output` 文件时按 FR-024 省略该提示行。缺任一小节即判不合格。正文语言 MUST 按 A7 的封闭域（`zh` / `en`）与固定顺位判定，每次回退 MUST 在 [[STR-004]] 声明。
- **FR-019**: [[STR-001]] MUST 先于一切细节给出可直接行动的总判断，其首行 MUST 是 [[STR-012]] 后接 `<token>` 的机器可判定行（形如 `verdict: <token>`）。verdict 取值封闭为 `success` / `partial` / `failure` / `aborted` / `needs-confirmation`，由本 FR 独占拥有（唯一 owner）；token MUST 为英文原样，其后的正文 MUST 用报告语言写出对应措辞（zh：成功 / 部分完成 / 失败 / 已中止 / 需要确认；en：succeeded / partially completed / failed / aborted / needs confirmation）并给出一句可直接行动的理由。status → verdict 的映射（封闭、单向）：`completed`→`success`；`partial`→`partial`；`failed`→`failure`；`aborted`→`aborted`；[[STR-014]]→`aborted`（文案「用户拒绝确认」）；[[STR-013]]→`needs-confirmation`；[[STR-015]]→`success`（文案「未执行任何动作」，不称执行成功）。verdict MUST NOT 被上调或下调。[[STR-002]] MUST 按**封闭影响尺**降序列出关键变化或结果：① 用户可见行为变化 → ② 接线/接口变化 → ③ 文档与记录变化；同尺并列按文件路径字典序；MUST NOT 使用其他排序依据；无变化时 MUST 明写「无变化」。
- **FR-020**: [[STR-003]] MUST 为每条关键结论提供证据指针（产物路径、命令与退出码、测试读数或可定位引用），不得只写形容词；无可报告输出时 MUST 写 [[STR-010]]，该 literal 只替代证据指针与产物清单，MUST NOT 替代派发记录行（[[STR-011]] 仍须出现）。
- **FR-021**: [[STR-004]] MUST 列出风险、限制、未验证项与缺失上下文；无已知风险时 MUST 用报告语言显式写出「无已知风险」（英文报告为 `no known risks`），不得省略该节。
- **FR-022**: [[STR-005]] MUST 给出可执行的下一步（或显式「无下一步」）；报告表达层 MUST 应用既有四维度自然化中的适用部分（去套话、补过渡、格式可读、语言一致），且服从保真底线与 `--tone`/`--audience`。

#### E. 旧内容模式

- **FR-023**: [[STR-008]] / [[STR-009]] 路径 MUST 保持既有的输入核验、格式一致、主语言判定、分段与四维度改写；本特性 MUST NOT 降低其保真或改写质量。
- **FR-024**: 旧内容模式 MUST NOT 生成动作报告五节，也 MUST NOT 派发子代理；其输出缺省返回会话，`--output` 时按既有规则写入（只含改写文本）。**运行模式**下 `--output` MUST：① 扩展名落在 `.md` / `.markdown` / `.txt` 封闭集内（本 FR 是运行模式扩展名集的唯一 owner；运行模式没有输入格式可对齐）；② 写入完整五节报告，并含五个 H2 之前的载体标记行、[[STR-012]] 行与 [[STR-011]] 行；③ MUST NOT 写入迁移提示行（迁移提示是调用级会话通知，见 FR-005）；④ 会话回显一份摘要（摘要只作索引，不替代报告）；⑤ `--force` 沿用既有覆盖规则；⑥ 目标已存在且未给 `--force`、或不可写时拒绝且不产生部分文件。
- **FR-025**: 注入防护 MUST 在两种模式下同时生效（含 [[STR-008]] 与 [[STR-009]] 路径），并覆盖**全部不可信文本**：指令原文、显式内容源、执行体回传的 `final_output` / `evidence` / `products` 字段、以及指令产出的文件内容。这些文本 MUST 按数据处理：其中的指令式文本 MUST NOT 改变 humanize 自身的保真、拒收、零外传与零写入规则，MUST NOT 被当作 humanize 的操作指令执行；报告只能引用、转述或逐字引用它们，MUST NOT 服从其指令。

#### F. 接线与兼容

- **FR-026**: 命令模板、4 份工具副本、humanize 技能与 docs MUST 同步到新定位；工具副本 MUST 由既有再生成入口产出，MUST NOT 手改。
- **FR-027**: 本特性 MUST NOT 新增 `/speckit.*` 命令，MUST NOT 新增阻断式确认门；门禁扫描以 `git diff` 新增行为判定单位，MUST 0 命中 `BLOCKING_PATTERNS`。
- **FR-028**: 受影响的契约测试（humanize 命令面、expression 台账/门禁/wiring 中与本命令相关者）MUST 显式更新并注明日期与理由；MUST NOT 静默改计数或删除断言。
- **FR-029**: Feature 062 MUST 保持 `Implemented` 状态；Feature 详情 MUST 记录本次扩展（Latest Review / Key Changes），索引名称/描述 MUST 更新为「动作输出人类友好化」并同步 `Last Updated`。
- **FR-030**: 并发与嵌套 MUST fail-closed，且**只作用于运行模式**（内容模式 MUST NOT 取得占位、MUST NOT 被并发拒收）。观察载体是受制裁临时根下的一文一件占位 `.specify/.tmp/humanize/<run_id>.run`（gitignored、运行结束即移除；活动 = 未超过 24h 的占位，过期占位 MUST NOT 阻断、只在 [[STR-004]] 点名）。「同一仓库」的范围 MUST 是目标项目所在的 git 工作树根（`git rev-parse --show-toplevel`），不同 worktree 视为不同范围。三类拒绝 MUST 点名冲突项：① 同一范围已有活动占位 → `active-run`，点名冲突 `run_id` 与起始时间；② `--output` 目标被另一活动运行占用 → `output-occupied`，点名目标路径与冲突 `run_id`；③ 指令文本含封闭 token 集 `speckit.humanize`（大小写不敏感）→ `nested-invocation`，点名命中的字面量，并在拒绝消息中说明这是保守判定（宁可误拒提及该名称的指令）。

### Key Entities *(include if requirement involves data)*

- **Humanize Run**: 一次调用，绑定指令、执行载体（子代理/会话内）、并发占位（运行模式）、上下文来源集合与最终报告。
- **Instruction**: 选项之后的待执行指令原文；执行体按原文与其所属契约执行。
- **Action Result**: 子代理输出、产物路径、证据指针、失败/中止信息；status 取值域见 FR-012。
- **Context Bundle**: 动作证据 + 项目治理 + 会话上下文；每项带 `read` / `not-read` / `unavailable` 状态（FR-014）。
- **Human Report**: 五节结构化报告（[[STR-001]]…[[STR-005]]），含 verdict 行（[[STR-012]]）、派发记录行（[[STR-011]]）与来源清单。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 夹具指令在原生通道下运行一次，派发记录为 [[STR-011]] `1`（1/1）；报告五节（[[STR-001]]、[[STR-002]]、[[STR-003]]、[[STR-004]]、[[STR-005]]）按序齐备（5/5）。
- **SC-002**: 报告结论与夹具输出一致（1/1）；[[STR-003]] 的每条关键结论都有可定位证据——分母 = 夹具报告 [[STR-002]] 的条目，≤5 条时全量、>5 条时取前 5 条（按报告顺序，不挑选），逐条断言（L/L）；[[STR-004]] 内的来源清单非空且每项状态为 `read`（1/1）。
- **SC-003**: 失败夹具的 [[STR-012]] 行取值为 `verdict: failure`（1/1）；[[STR-001]] 正文按 § Failure Wording — Closed Banned Vocabulary 的按语言封闭词表扫描命中 0（1/1，允许「部分完成」类短语）；[[STR-003]] 含失败证据（1/1）。
- **SC-004**: 破坏性指令在确认被拒绝时不产生副作用（1/1），报告记录 [[STR-014]]、verdict `aborted` 与拒绝原因/未执行范围（2/2）。
- **SC-005**: 旧模式回归——[[STR-009]] 与 [[STR-008]] 各跑一次，输出格式与输入一致且保真检查通过（2/2）；裸文本夹具被执行而非改写（1/1）。
- **SC-006**: 接线一致性（封闭集，owner = § Wiring Surface — A11 Closed Set）——① 无限制发现命令的每个命中都被分类且未分类为 0（1/1）；② 活源类每一项满足其类义务（L/L，L = 实测重算的分母）；③ `regen-command-copies.py --check` 与 `sync-mirrors.py --check` 均 exit 0（2/2）；④ 冻结验证类每个文件与基线逐字节一致（F/F，F = 实测重算的分母）；⑤ 无新增命令（1/1）、门禁新增行 0 命中（1/1）。
- **SC-007**: 安全与写入——humanize 自身无网络外发（1/1）；无 `--output` 时 humanize 未写报告/副本，且指令造成的写入均在 [[STR-003]] 披露（2/2）；失败不触发重试（1/1）。
- **SC-008**: Feature 062 在运行前后均为 `Implemented`，详情含扩展记录且索引名称/描述已更新（3/3）；门禁新增行 0 命中（1/1）。
- **SC-009**: 拒收、并发与降级可判——① 内容源与非空指令同现被拒（1/1）；② `active-run` 被拒并点名冲突 `run_id` 与起始时间（1/1）；③ `output-occupied` 被拒并点名目标路径与冲突 `run_id`（1/1）；④ `nested-invocation` 被拒并点名命中的字面量（1/1）；⑤ 内容模式不取占位、不受并发拒收影响（1/1）；⑥ 降级路径报告含 [[STR-007]]、不含 [[STR-006]]，派发记录为 [[STR-011]] `0`（1/1）；⑦ [[STR-004]] 在无风险时显式写「无已知风险/no known risks」（1/1）；⑧ [[STR-005]] 存在并给出下一步或显式「无下一步」（1/1）；⑨ 无可报告输出时 [[STR-003]] 写 [[STR-010]] 且保留派发记录行（1/1）。
- **SC-010**: 注入防护——三种注入场景各一条样本：运行模式指令注入、内容模式输入注入、执行体回传注入（`final_output` / `evidence` / `products` 与产物内容）；每组断言四项（保真不变、拒收语义不变、零外传、零写入）各 1 次，共 12/12 次断言。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 夹具运行的报告文件；按小节标题解析；[[STR-011]] 行取值。
- **SC-002 Source**: 报告与夹具输出的逐条对照；证据路径存在性检查；抽样规则见 SC-002 本体（分母来自报告 [[STR-002]] 条目，不另挑样本）。
- **SC-003 Source**: 失败夹具报告；[[STR-012]] 行解析；§ Failure Wording — Closed Banned Vocabulary 的确定性扫描器（剥离允许短语 → 匹配禁用词）。
- **SC-004 Source**: 需确认指令夹具 + 拒绝路径；副作用快照（`git status` / 目标文件哈希）；status 与 verdict 行。
- **SC-005 Source**: [[STR-009]] / [[STR-008]] 回归夹具 + 裸文本指令夹具；保真差异脚本 `tests/fixtures/humanize/diff_protected.py`。
- **SC-006 Source**: § Wiring Surface — A11 Closed Set 的发现命令与分类规则（在基线提交上执行）+ `regen-command-copies.py --check` + `sync-mirrors.py --check` + `git diff --quiet <baseline> -- <冻结验证文件>` + 命令清单对比。
- **SC-007 Source**: 运行前后 `git status --porcelain` 与网络调用审计（无外部请求记录）；重试记录计数。
- **SC-008 Source**: `features.md` / `features/062.md` 状态与详情；`scan-confirmation-gates.py` 新增行判定。
- **SC-009 Source**: 四类拒收夹具（both-sources / active-run / output-occupied / nested-invocation）+ 内容模式并发对照 + 降级夹具 + 空输出夹具；占位目录清空检查与 `git status`。
- **SC-010 Source**: 三组注入夹具（运行模式、内容模式、执行体回传与产物内容）；四项规则的确定性断言；不含模型自评。

### Failure Wording — Closed Banned Vocabulary（SC-003 owner）

本节拥有「失败/中止报告不得读作成功」的**按语言封闭词表**与匹配规则；SC-003 与 Measurement Sources 只引用本节，不另列词。

- **作用域**：verdict ∈ {`failure`, `aborted`} 的报告，扫描对象是 [[STR-001]] 的正文（[[STR-012]] 行之外）。其他小节的事实陈述（如「3/5 步已完成」）不受本节约束，由保真底线约束。
- **匹配规则（确定性）**：先按「允许短语」表**最长优先**逐次删除，再在剩余文本上匹配禁用词；zh 用子串匹配（中文不分词），en 用词边界、大小写不敏感匹配。删除后仍命中任一禁用词即判违反。

| 语言 | 允许短语（先剥离，最长优先） | 禁用词（剥后匹配） | 匹配方式 |
|------|------------------------------|--------------------|----------|
| zh | `部分完成`、`未完成`、`未执行任何动作`、`未通过`、`未成功` | `成功`、`完成`、`通过` | 子串 |
| en | `partially completed`、`partially complete`、`not completed`、`not complete`、`did not complete`、`no action taken` | `success`、`successful`、`successfully`、`complete`、`completed`、`pass`、`passed` | 词边界、大小写不敏感 |

## Wiring Surface — A11 Closed Set

**Owner**: 本节是「需手改的活接线面」封闭集的唯一所有者——发现命令、五类分类规则、类义务与守卫判据都定义在这里。成员清单是本节的**派生量**（基线树 + 规则重算），MUST NOT 在任何可再生文档（含 `tasks.md`）里手写白名单，MUST NOT 用人工挑选的路径清单代替发现命令。

- **基线参照物**：改动前的 git 工作树（基线提交号由阶段证据记录）；发现命令 MUST 在该提交上执行。
- **发现命令（无限制）**：`git grep -l -i humanize <baseline-commit>`——不带路径白名单、不带额外过滤；任何命中都 MUST 落入下表某一类。命令钉在基线提交上，因此本特性新增的文件（spec / 证据 / 夹具）不在分母内。
- **分类规则（封闭；按顺序求值，首个匹配生效）**：

| # | 类 | 路径族判据 | 类义务 |
|---|----|-----------|--------|
| 1 | 活源 | `templates/commands/humanize.md`；`skills/external/humanize/**`；`docs/reference/commands/humanize.md`；`tests/contract/test_humanize_command_surface.py`；`tests/contract/test_stage_class_wiring.py`；`.specify/memory/features.md`；`.specify/memory/features/062.md` | 本特性手改：命令模板/技能/docs 含新定位，命令模板与 docs 另含可复制的迁移示例；两份契约测试断言新契约；Feature 登记追加扩展记录且状态不变 |
| 2 | 派生副本 | `.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/` 下文件名含 `humanize` 的副本 | 只由 `regen-command-copies.py` 生成；`--check` exit 0；与源逐字节相等 |
| 3 | 镜像 | `.specify/skills/humanize/**` | 只由 `sync-mirrors.py` 生成；`--check` exit 0；与 `skills/external/humanize/**` 零差异 |
| 4 | dated record | `.specify/specs/**`、`.specify/state/**`、`.specify/history/**`、`.specify/memory/session/**`、`.specify/memory/feedback/**` | 历史/记录面，不属于消费者：MUST NOT 被要求携带新定位；只允许新增 dated 文件，或由所属阶段在原文件内更新 |
| 5 | 冻结验证 | 其余全部命中（其余 `tests/**`、`shared/`、`.specify/shared/`、`.specify/memory/` 中非活源项、其他 `skills/` 与 `docs/` 页） | MUST 与基线逐字节一致（`git diff --quiet`）；其既有断言/检查 MUST 仍绿 |

- **无「其他」桶**：任一命中必须命中第 1–5 类；无法分类即判不合格（守卫断言未分类 = 0）。
- **闭环守卫**：① 分类完备（未分类 = 0）；② 活源分母 = 第 1 类的实测条数（重算，不写死），逐项满足类义务；③ 派生副本与镜像由各自 `--check` 的 exit 0 证明；④ 补集断言——第 5 类每个文件与基线 `git diff --quiet` 为 0；⑤ 结构不变量——命令名册不变、门禁新增行 0 命中、Feature 062 状态不变。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `## Conclusion` | FR-018, FR-019, SC-001, SC-003 |
| `STR-002` | `## Key Changes` | FR-018, FR-019, SC-001 |
| `STR-003` | `## Evidence` | FR-018, FR-020, SC-001, SC-002, SC-003 |
| `STR-004` | `## Risks & Limits` | FR-018, FR-021, SC-001, SC-002 |
| `STR-005` | `## Next Steps` | FR-018, FR-022, SC-001 |
| `STR-006` | `mode: subagent` | FR-007, 派发记录 |
| `STR-007` | `mode: in-session-degraded` | FR-007, FR-011, Edge Cases |
| `STR-008` | `--file` | FR-001, FR-002, FR-003, FR-005, FR-023, FR-025, SC-005 |
| `STR-009` | `--inline` | FR-001, FR-002, FR-003, FR-005, FR-023, FR-025, SC-005 |
| `STR-010` | `none` | SC-009, Edge Cases |
| `STR-011` | `dispatches:` | FR-007, SC-001 |
| `STR-012` | `verdict:` | FR-019, SC-003 |
| `STR-013` | `needs-confirmation` | FR-012, FR-019 |
| `STR-014` | `denied` | FR-012, SC-004 |
| `STR-015` | `not-an-action` | FR-012, FR-019 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-30

- Q: 指令执行到需要用户确认的步骤、但子代理无法直接询问用户时怎么办？ → A: fail-closed——不执行该步，[[STR-001]] 写「需要确认，未获答复」，[[STR-003]] 记录卡点，其余已完成部分照常报告；不自动重试、不代答。
- Q: 新模式下 `--output` 写什么？ → A: 写入完整五节报告并在会话回显摘要；`--force` 沿用既有覆盖规则；不可写即拒绝且不产生部分文件。
- Q: 报告正文语言如何确定？ → A: 指令的主语言优先；不可判时回退到项目治理（instructions/glossary）的主语言；五节标题固定英文。
- Q: 本次扩展绑定到哪个 Feature？ → A: 绑定 **Feature 062** 并更新其名称/描述为「动作输出人类友好化」；状态保持 `Implemented`（扩展不回退）。

### Session 2026-10-30（analyze 回环修复轮 1）

- Q: verdict 的呈现形态是英文 token 还是本地化措辞？ → A: 两者都要且分工固定——[[STR-001]] 首行是机器可判定的 `verdict: <token>`（英文 token，集合与映射由 FR-019 独占拥有），其后正文用报告语言写出对应措辞；token 不被翻译、不被改写。
- Q: 活接线面封闭集由谁拥有、成员如何得到？ → A: 本文 § Wiring Surface — A11 Closed Set 拥有发现命令、五类分类规则与守卫；成员是从基线树 + 规则重算的派生量，MUST NOT 委托给 `tasks.md` 或人工白名单。
- Q: `--audience` 空值的语义？ → A: 视为**未提供**（不拒收、不改变表达层缺省）；这与 `--tone` 空值/纯空白按集合外拒收不同（FR-004）。
- Q: 用户明确拒绝确认时记什么？ → A: status `denied`（[[STR-014]]），verdict `aborted`，文案写明「用户拒绝确认」与未执行范围（FR-012、FR-019）。
- Q: 超时阈值归谁？ → A: 归执行载体/宿主所有；humanize 不自设阈值、不重试；载体不提供超时信号时该类别不可判并在 [[STR-004]] 声明（FR-012）。
- Q: 运行模式 `--output` 的文件内容边界？ → A: 写完整五节与元数据行（载体标记、verdict、派发记录）；迁移提示是调用级会话通知，只回显一次、不写入文件（FR-005、FR-024）。
- Q: 报告语言域是否封闭、第三书写系统怎么办？ → A: 封闭域 `zh` / `en`；顺位为指令 → 治理 → 回退 `en`，每次回退在 [[STR-004]] 声明；第三书写系统在 ①② 均不可判时按回退处理，原文逐字引用不翻译（A7、FR-018）。
- Q: M-02 的三类拒绝为何不新增 SC 编号？ → A: SC 定义数被 plan / tasks / checklist 的既有计数钉扎，本阶段不得改这些属主制品；三类拒绝与内容模式豁免并入已拥有「拒收与降级」面的 SC-009，覆盖以 9 条断言表达，不新增编号。

**本轮覆盖扫描说明**：同作者条件成立，扫描由 2 个 fresh-context 只读子代理分域执行；共 24 条发现，其中 20 条由既有 owner 事实裁决并就地修正（零写入范围收窄、内容源与指令同现拒绝、SC 分母、失败词表、派发记录载体、字面量登记、并发与嵌套 fail-closed、覆盖缺口补 SC-009/SC-010 等），4 条作为上面的问答写回；无未决项。

**analyze 回环修复轮 1 说明**：requirements 侧关闭 H-01（FR-019 独占 verdict 集与映射、呈现形态固定）、H-02（§ Wiring Surface 拥有发现/分类/守卫，SC-006 改为派生分母与补集断言）、H-03（FR-025 覆盖回传字段与产物内容、SC-010 增第三组样本）、H-04（§ Failure Wording 拥有按语言封闭词表与剥离式匹配），以及 M-01、M-02、M-05、M-06、M-08、M-09、M-10、M-11、M-13、M-14、M-15、M-16、M-18；plan/contracts 与 tasks 侧条目留给对应修复轮，本文件不改其属主制品。
