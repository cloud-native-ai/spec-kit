# Requirements Specification: Derivation Command

**Requirement Branch**: `048-derive-command`  
**Created**: 2026-09-05  
**Status**: Draft  
**Input**: User description: "Add /speckit.derive: a command that reaches an architecture by replaying the reasoning methods of authoritative sources rather than summarizing their content. It grounds every source online (mandatory), extracts each source's way of thinking as a reusable Reasoning Move (思维算子) with named slots, accumulates those moves into a project-level library that later runs reuse and augment, builds an auditable derivation chain (premises -> move -> conclusion -> falsification) under enforceable integrity rules, and composes a complete architecture in which every element traces back to a chain step. Gaps where grounded premises run out are recorded as open questions, never silently filled. Motivated by a handed-in reading list that contained one dead link and one community-retitled article - both defects that would silently poison the chain without online verification."

## Related Feature *(mandatory)*

**Feature ID**: 049  
**Feature Name**: Derivation Command

> 归属裁定(详见 `feature-ref.md`):判定为**新 Feature** 而非绑定既有。推导式架构生成是一个新能力面——013 为技能生命周期管理编排、037 仅覆盖 docs 域、031/040 为效率与治理纪律、041 提供的是「项目级一等概念归档」的结构先例而非能力归属。无既有 Feature 拥有「从权威源重放推理方法以推导架构」这一能力。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 把 handed-in 的文献清单落地为可核实的分级来源表 (Priority: P1)

使用者交给命令一份阅读清单(标题 + 作者 + URL,可能来自他人推荐、社区整理或模型生成)。命令逐个联网核实:链接是否还活着、原文标题是否就是清单上那个标题、这段文字究竟是不是被归因的那个人或机构写的。核实结果落成一张来源表,每行携带溯源等级与**具体证据**(HTTP 状态、存档快照地址、确立归属的那条搜索结果)。死链走存档回退与归属搜索;社区改标题的文章被检出并双标题留痕;确实核实不了的来源进入「无法核实」清单并附理由,绝不静默消失。

**Why this priority**: 这是整条价值链的地基。清单里的死链和改标题文章如果不在这一层被拦住,后面每一层都会把它们当作可靠前提,最终产出一个建立在误引之上、却看起来完全严谨的架构。没有这一层,其余三个故事都无从谈起。

**Independent Test**: 给定一份固定语料(含 1 个活链、1 个死链但有存档快照、1 个死链且无快照、1 个社区改标题文章),运行落地阶段后检查来源表:四行的 `access` / `resolved_via` / `grade` / `title_mismatch` 各自符合协议,`## Unverifiable Sources` 恰好收录无快照那一行且带理由。

**Acceptance Scenarios**:

1. **Given** 一条指向作者本人站点的活链, **When** 执行落地, **Then** `access: live`、`resolved_via: direct`、`grade: primary`,且 `verification` 携带具体状态证据而非裸断言。
2. **Given** 一条死链但存档服务有快照, **When** 执行落地, **Then** `access: wayback:<ts>`、`resolved_via: wayback`,且等级**按快照内容判定**——作者本人页面的快照仍是 `primary`,清单体文章的快照仍是 `community`。
3. **Given** 一条死链且无任何快照、归属搜索也未命中, **When** 执行落地, **Then** `access: dead`、`grade: unverified`,该来源出现在 `## Unverifiable Sources` 且附理由,未出现在任何步骤的 `premises` 中。
4. **Given** 清单标题是社区整理的而原文另有标题, **When** 执行落地, **Then** `title_mismatch` 由引擎按归一化字符串比较算出为真,`claimed_title` 与 `resolved_title` 双标题都保留,引用该来源的步骤引用的是 `resolved_title`。
5. **Given** 宿主 CLI 不具备任何线上检索或抓取能力, **When** 执行落地, **Then** 全部来源标 `unverified` 且理由为 [[STR-007]],可锚定步骤数为 0,运行在建链前停止并输出降级说明,**不产出任何架构**。

---

### User Story 2 - 从来源中提取可复用的思维算子并累积进项目级算子库 (Priority: P1)

命令读来源不是为了知道它主张什么,而是为了知道它**怎么从前提走到结论**。每个这样的推理形状被抽成一个「思维算子」:带命名槽位的推理形式、它防住的失败模式、它的适用条件**与过度使用护栏**、以及展示这一论证方式的来源锚点。算子累积进项目级库,后续运行先读投影再补充——同一个算子在别的领域还能用,这是「学思维方式」而非「整理资料」的兑现方式。

**Why this priority**: 这是本命令区别于 `/speckit.research` 的唯一实质差异。research 产出的是决策与理由(结论层);本命令产出的是可跨领域重放的推理模式(方法层)。没有这一层,命令退化成一个带引用的调研工具,用户的原始诉求直接落空。

**Independent Test**: 对同一主题连续运行两次。第一次入库若干算子;第二次读取投影后,对已存在的算子只增锚点(处置 `reinforced`)或标记复用(处置 `reused`),仅对 genuinely new 的推理形状追加新行 —— 三个处置值均由引擎输出报告,不写入库的 `status` 列。检查算子库:重复 `move_id` 数为 0,重复归一化 `inference_form` 数为 0,第二次的 `stats` 报告 reused/reinforced 计数大于 0。

**Acceptance Scenarios**:

1. **Given** 一个来源以「举出满足 D 但不满足 P 的反例」的方式驳斥某性质 P, **When** 提取算子, **Then** `inference_form` 写成带命名槽位(`P`、`D`)的形状而非该来源的具体结论,`anchor` 以限定形式 `<topic-slug>.S-<k>` 指向该来源(FR-014),`prevents` 写明它挡住的失败模式。
2. **Given** 一个候选算子的 `inference_form` 与库中既有算子归一化后近似重复, **When** 经 `moves-add` 提交, **Then** 引擎**拒绝**写入并返回既有 `move_id`,本次运行转为对该算子增锚点(`reinforced`)而非分叉出变体。
3. **Given** 算子库已发放过的最大 `move_id` 为 `M-<max>`, **When** 追加一个 genuinely new 算子, **Then** 新 `move_id` 为 `M-<max+1>`(按现存最大编号发放,而非按行数),严格单调;历史 `move_id` 未被复用或重编号。
4. **Given** 某算子的 `applies_when` 只写了适用条件、没写过度使用护栏, **When** 校验, **Then** 该行被判为不完整——一个无护栏的算子会被到处套用并悄悄变成教条。
5. **Given** 一次运行产出的 `derive.md`, **When** 校验, **Then** 其 `## Reasoning Moves Applied` 节引用 `M-<nnn>` 身份;若某行同时复写了完整算子且 `inference_form` 与库中同 ID 行不一致,校验失败。

---

### User Story 3 - 在可校验的完整性规则下构建推导链并组装出可溯源架构 (Priority: P1)

有了分级来源与算子库,命令开始逐步推导:每一步取显式前提(已核实来源 + 更早的步骤结论)、套用**恰好一个**算子、写出实例化后的推理、得出一句**可证伪**的结论、并写出什么观察能推翻它。步骤的结论向后传递成为后续步骤的前提,形成有向无环链。链走到头时组装架构:每个元素都回指它所依赖的步骤,置信度按最小值继承;两个来源的算子推出冲突结论时不静默择一,而是标 `contested`、双向互指、写出判别性问题;前提耗尽处记为未决问题,**绝不用听起来合理的猜测填空**。

**Why this priority**: 这是交付物本身。前两个故事是它的输入面;这一个故事是使用者最终要拿到的东西——一个「完整架构」,且每一处都能被独立读者重放核查,而不是被要求信任作者。

**Independent Test**: 用固定的来源表与算子库 fixture 构建一条链与架构,`validate` 退出码 0 且 A1–A10/A12/A13 全绿;再对同一 fixture 分别注入四类缺陷(孤儿前提、缺 `derived-from`、含禁用论证字面量、`derived` 元素建立在 `contested` 步骤上),每次 `validate` 退出码 4 且错误信息定位到具体规则编号。

**Acceptance Scenarios**:

1. **Given** 一个步骤的 `premises` 引用了未在 `## Sources` 出现的 `S-<k>`, **When** 校验, **Then** 报 C1 孤儿前提并拒绝。
2. **Given** 一个步骤的 `premises` 引用了编号更大的 `D-<j>`(前向引用), **When** 校验, **Then** 报 C1 并拒绝——链必须是步骤序上的有向无环图。
3. **Given** 一个步骤引用了零个或两个算子, **When** 校验, **Then** 报 C2 并拒绝(零个 = 无论证的断言;两个 = 应拆成两步)。
4. **Given** 某步骤的 `derivation` 含 [[STR-001]] 中任一禁用字面量, **When** 校验, **Then** 报 C3 并拒绝;禁用集为封闭集,扩充须同时改概念锚与引擎。
5. **Given** 某步骤的 `falsification` 为 `none` 或其 `conclusion` 的复述, **When** 校验, **Then** 报 C4 并拒绝。
6. **Given** 两个来源的算子推出冲突结论, **When** 建链, **Then** 该步骤标 `contested`、与对向步骤双向 `contested-with`、写出判别性问题,残余进 `## Open Questions`;任何消费该步骤的 `derived` 置信度步骤被拒绝(C5 传播)。
7. **Given** 下一步所需前提无任何已核实来源可提供, **When** 建链, **Then** 运行以终止条件 (b) 收尾,该缺口成为 `## Open Questions` 一行(含 `why-undetermined` 与 `discriminator`),**不出现编造的前提**;运行在 [[STR-008]] 中显式声明触发的是 (a) 还是 (b)。
8. **Given** 一个架构元素没有 `derived-from`, **When** 校验, **Then** 报 A7 硬失败并拒绝整个文件——不可溯源的元素是穿着架构外衣的偏好。
9. **Given** 一个元素的 `derived-from` 含一个 `contested` 步骤, **When** 校验, **Then** 该元素的 `confidence` 不得为 `derived`(按最小值继承),否则报 A8 并拒绝。
10. **Given** 步骤数达到 `--max-steps` 预算上限, **When** 建链, **Then** 触顶被如实报告,而非静默截断或静默继续。

---

### User Story 4 - 自审、执行报告与命令面接线 (Priority: P2)

运行收尾时产物携带一张固定自审表:结构性检查由引擎程序化判定,两项语义检查(A11「本次真的联网核实了」、A14「产物陈述的是来源的思维方式而非内容摘要」)由 agent **显式背书**而非继承一个绿色。A12 是唯一分半的一项:步数对预算的计数由引擎判定,而「触发的是 (a) 还是 (b)」由 agent 在 [[STR-008]] 中声明并背书 —— 引擎只校验声明存在且取值合法,故 A12 不进待背书集(该集恒为 A11 与 A14)。任何引擎检查为红的运行必须如实报告失败,不得把架构当作已推导出来呈现。命令本身作为**复杂命令**接入框架既有接线:feedback probe 登记、复杂命令分类、docs-sync 收尾步骤、四份工具副本再生成;其产物(新文件 + 追加)可逆,故全程自动执行并出具三要素执行报告,零阻塞确认门控。

**Why this priority**: 这一层不改变推导本身,但决定了产物是否**可信**与是否**合规接入框架**。它可以作为 P1 三件事之后的快速跟进交付;但没有它,一次失败的运行可能被当作成功呈现,而命令也无法在受支持的工具里被发现。

**Independent Test**: 对一个 fixture 产物运行 `validate`,断言 JSON 输出含 `semanticChecksPending` 且恰好包含 A11 与 A14;对一份引擎检查全红的 fixture,断言运行报告如实呈现失败而非呈现架构。命令面部分由契约测试断言(四份副本 + AUTO-GENERATED 标记、probe internal 计数 +1 且 `--validate` 退出码 0、门控扫描 total 不超基线、两个分类计数各 +1)。

**Acceptance Scenarios**:

1. **Given** 一份结构完整但语义检查未背书的产物, **When** 运行 `validate`, **Then** 输出 `semanticChecksPending` 恰好为 `["A11", "A14"]`,agent 必须显式背书二者,不得默认视为通过。
2. **Given** 某引擎检查为红, **When** 收尾报告, **Then** 报告如实呈现该失败与定位,**不**把 `## Derived Architecture` 作为已推导结果呈现。
3. **Given** 命令模板已落地, **When** 再生成工具副本, **Then** 四份副本均存在且携带指向 `templates/commands/derive.md` 的 AUTO-GENERATED 标记。
4. **Given** 命令模板携带 `## Feedback` 节, **When** 校验 probe 注册表, **Then** 存在与之匹配的 `command-wrapup` Object [[STR-005]],`--validate` 退出码 0,internal 计数较基线 +1;`--reconcile` 的错误集不因本命令而扩大。
5. **Given** 命令的产物均为可逆写入, **When** 扫描确认门控, **Then** 新增文件里的阻塞门控匹配数为 0,扫描器 total 不超过既有基线。
6. **Given** 命令模板为复杂命令, **When** 校验节序, **Then** `## Feedback` 在 `## Documentation` 之前且二者相邻,`## Documentation` 在 `## Handoffs` 之前。

---

### Edge Cases

- 同一 URL 在清单里出现两次(不同标题)→ 按来源身份(URL)去重为一行,但两个 `claimed_title` 变体都要留痕:两者留在该行的 `claimed_title` 单元格内、以转义分隔符 `\|` 连接(FR-008),因为改标题的证据正在差异里。
- 来源活着但内容与标题或归因不符(标题党、被改写的转载)→ 等级按**实际内容**判定,不按域名声誉判定。
- 存档快照只有部分正文(截断、缺章节)→ `verification` 必须写明快照不完整;不足以支撑的推理形状不得抽取。
- 付费墙来源但有公开摘要 → `access: paywalled`;摘要可支撑归属判定,但不得支撑任何需要完整论证的算子抽取(FR-001)。
- 探活本身未能运行(无连通性、主机不可达、超时)→ `access: unknown` 且 `grade: unverified`,**不得**记 `dead`:网络故障不是死链,记 `dead` 就是编造本次运行从未确立的事实(FR-001/FR-004/FR-033)。
- 来源之间互相引用形成回音壁(A 引 B、B 引 A,二者实为同一主张)→ 不得把互相引用当作两个独立锚点;`authoritative-secondary` 不得作为与 primary 相冲突主张的唯一锚点。
- 算子库文件被手工编辑(绕过 `moves-add`)→ 引擎 `validate` 检出行形、ID 单调性与重复 ID 异常并报告,不静默接受。
- 主题 slug 与既有推导档案重名 → `init` 拒绝覆盖(no-clobber),需显式 `--force` 才可重新脚手架。
- 链在中途发现某个早期步骤的前提来源事后被降级 → 依赖它的所有下游步骤与元素置信度必须随之下降(最小值继承),不得保留旧的 `derived`。
- 步骤预算触顶但架构元素尚未全部溯源 → 如实报告触顶;未溯源元素不得出现在 `## Derived Architecture`,应留在 `## Open Questions`。

## Requirements *(mandatory)*

### Functional Requirements

**来源落地(US1)**

- **FR-001**: 命令 MUST 对每个输入来源执行线上核实,按固定次序降级:直连抓取 → 存档可用性查询 → 按标题+作者做一次归属搜索;每级结果 MUST 记入 `access` 与 `resolved_via`(两者的取值集归锚 §Source Record,本文件不复列)。两个分支由锚 §Dead-Link Protocol 拥有并 MUST 被实现:① 直连可解析但正文在付费墙后、仅摘要公开 → `access: paywalled`,摘要 MAY 支撑归属判定,MUST NOT 支撑任何需要完整论证的算子抽取;② 探活本身未能运行(无连通性、主机不可达、超时)→ `access: unknown` 且 `grade: unverified`,MUST NOT 记 `dead` —— 网络故障不是死链,记 `dead` 等于把本次运行从未确立的事实写进档案。
- **FR-002**: `verification` 字段 MUST 是具体证据引用(HTTP 状态、存档快照地址、或确立归属的搜索结果)。裸断言 MUST 被引擎拒绝(最小长度 + 禁字面量检查)。
- **FR-003**: `title_mismatch` MUST 由引擎按归一化字符串比较计算,MUST NOT 由 agent 断言。为真时 `claimed_title` 与 `resolved_title` MUST 双双保留,且引用该来源的每个步骤 MUST 引用 `resolved_title`。
- **FR-004**: 每个来源 MUST 被赋予四级溯源等级(`primary` / `authoritative-secondary` / `community` / `unverified`)之一。仅前两级 MAY 出现在步骤的 `premises`;后两级 MUST 仅出现在可选的 `leads` 字段。`access: unknown` 的行 MUST 落 `grade: unverified`:探活没跑起来就不构成任何等级证据(锚 §Dead-Link Protocol 第 4 步),该耦合 MUST 由引擎校验而非留给 agent 自觉。
- **FR-005**: 每个 `unverified` 来源 MUST 出现在 `## Unverifiable Sources` 并附理由,MUST NOT 被静默丢弃。
- **FR-006**: 经存档救回的来源,其等级 MUST 由快照内容决定,MUST NOT 因被救回而升级。
- **FR-007**: 宿主不具备任何线上能力时,命令 MUST NOT 编造核实:全部来源 MUST 标 `unverified` 且理由为 [[STR-007]],可锚定步骤数 MUST 为 0,运行 MUST 在建链前停止并报告降级,MUST NOT 产出架构。
- **FR-008**: 同一 URL 的重复条目 MUST 按来源身份(URL)去重为一行;全部 `claimed_title` 变体 MUST 保留在**该行的 `claimed_title` 单元格内**、以转义分隔符 `\|` 连接,使表仍可被引擎按位置解析。变体之间的分歧本身即改标题证据,MUST NOT 被折叠成其中一个。

**思维算子(US2)**

- **FR-009**: 命令 MUST 从已核实来源中提取思维算子,每个算子 MUST 记录 `name` / `inference_form`(带命名槽位)/ `prevents` / `applies_when`(含过度使用护栏)/ `anchor` / `status`。`status` 是算子的**持久**状态,取值集归锚 §Move Record(`active` / `superseded`);本次运行与算子的关系(`new` / `reused` / `reinforced`)是**运行相对处置**,MUST 由引擎 `moves-add` 与 `stats` 的输出报告,MUST NOT 作为库列存储 —— 把运行相对值写进持久行,正是库从第二次运行起开始自相矛盾的方式。
- **FR-010**: `inference_form` MUST 表达推理形状而非该来源的具体结论;缺少命名槽位、或替换领域名词后失效的表述 MUST 被判为不合格。
- **FR-011**: `applies_when` MUST 同时给出适用条件与过度使用护栏;缺护栏的行 MUST 被判为不完整。
- **FR-012**: 算子 MUST 累积进项目级库 [[STR-006]] 中的 `moves.md`,该文件 MUST 只由引擎的 `moves-add` 动作写入。
- **FR-013**: `moves-add` MUST 按归一化 `inference_form` 去重;近重复时 MUST 拒绝写入并返回既有 `move_id`,使本次运行的处置转为 `reinforced`(增锚点)而非分叉出变体。
- **FR-014**: `M-<nnn>` MUST 项目级单调发放(下一个 = 库中现存最大编号 + 1)、永不复用、永不重编号,且 MUST **只由引擎发放**。因 `S-<nnn>` 按主题发放而算子库是项目级的,算子的 `anchor` MUST 以限定形式 `<topic-slug>.S-<nnn>` 存储(点号命名,形式与理由归锚 §Source Record / §Move Record),使其在任何后续主题中仍可解析;裸 `S-<nnn>` 入库 MUST 被拒。
- **FR-015**: 运行 MUST 通过 `moves-list` 投影消费算子库;`derive.md` MUST 引用 `M-<nnn>` 身份而非复制整行;携带与库中同 ID 但 `inference_form` 不一致的复写行 MUST 被拒绝。
- **FR-016**: 算子库 MUST 被 git 跟踪(算子不可重新推导,丢失即丢失累积的推理资本);`status: superseded` 的行 MUST 保留而非删除,且 MUST NOT 再被任何步骤引用 —— `superseded` 是终态,它让该算子永久不可引用,需要该形状时只能由 `moves-add` 落新行。

**推导链与架构(US3)**

- **FR-017**: 每个推导步骤 MUST 恰好引用一个算子(C2)。
- **FR-018**: 步骤的 `premises` MUST 全部可解析:每个 `S-<k>` 存在于 `## Sources` 且等级达标,每个 `D-<j>` 满足 `j < k`;前向引用与环 MUST 被拒绝(C1)。
- **FR-019**: `derivation` 与 `conclusion` MUST NOT 含封闭禁用论证集 [[STR-001]] 中的任何字面量(C3)。该集合为封闭集,扩充 MUST 同时修改概念锚与引擎。
- **FR-020**: 每个步骤 MUST 携带非空洞的 `falsification`:不为 `none` / `n/a` / `-`,且非 `conclusion` 的复述(C4)。
- **FR-021**: 结论冲突 MUST NOT 被静默择一或折中:相关步骤 MUST 标 `contested`、双向 `contested-with`、写出判别性问题,残余 MUST 进 `## Open Questions`(C5)。
- **FR-022**: `contested` 步骤 MUST NOT 作为 `derived` 置信度步骤的前提;消费 `contested` 前提的步骤置信度 MUST 至多为 `provisional`(C5 传播)。
- **FR-023**: 终止条件 MUST 被显式声明为 (a) 全部在范围内元素已溯源,或 (b) 下一步所需前提无已核实来源可提供;(b) 时缺口 MUST 进 `## Open Questions`,MUST NOT 编造前提(C6)。该声明 MUST 落在机器可读的 [[STR-008]] 节中,使 A12 可被程序校验而非靠读者在散文里找。
- **FR-024**: 步骤数 MUST 受 `--max-steps` 预算约束,预算解析次序为**显式 flag → 引擎默认常量**(常量取值归 `contracts/derive-engine.md`,本文件不复述);触顶 MUST 被如实报告,MUST NOT 静默截断或静默继续(C6)。
- **FR-025**: 仅复述来源主张而无推理的 `conclusion` MUST 被识别为结论洗白;引擎 MUST 拒绝其退化形态(`derivation` 为空或过短、`conclusion` 与来源标题相同)(C7)。
- **FR-026**: 每个架构元素 MUST 携带非空且全部可解析的 `derived-from`;缺失 MUST 为硬校验失败,引擎 MUST 拒绝该文件而非仅告警。
- **FR-027**: 元素置信度 MUST 按其 `derived-from` 各步骤置信度的**最小值**继承。
- **FR-028**: `## Open Questions` 的 `Q ↔ A` 链接 MUST 双向可解析;被未决问题阻塞的元素 MUST 为 `provisional` 或 `contested`。

**自审、报告与接线(US4)**

- **FR-029**: 产物 MUST 携带 [[STR-002]] 定义的 `## Self-Audit` 固定表;A1–A10 与 A13 MUST 由引擎程序化判定,A11 与 A14 MUST 由 agent 显式背书。A12 MUST 按锚 §Self-Audit 的两半执行:**步数对预算的计数由引擎判定**;**触发的是 (a) 还是 (b) 由 agent 声明**(落在 [[STR-008]]),引擎只校验该声明存在且取值合法,MUST NOT 假装能判定其真伪。A13 MUST 以「本次运行报告为新发放的每个算子都能解析到算子库中的一行」为判据 —— 即它经 `moves-add`(唯一写入者)落库,而不是被手写进产物。
- **FR-030**: `validate` MUST 在输出中返回 `semanticChecksPending`,使语义检查 MUST 被显式背书而非继承为通过。
- **FR-031**: 任一引擎检查为红的运行 MUST 如实报告失败并定位,MUST NOT 把架构作为已推导结果呈现。
- **FR-032**: 引擎 MUST 为 stdlib-only,提供 [[STR-003]] 六个动作,退出码遵循 [[STR-004]]。
- **FR-033**: `probe-links` MUST 离线容错(探活未能运行 → `access: unknown`、退出码 0、绝不阻塞),MUST NOT 把网络故障报成 `dead`(FR-001 分支 ②),且 MUST NOT 被任何测试对真实网络调用。
- **FR-034**: 命令模板 MUST 为复杂命令:携带 `## Feedback` 与 `## Documentation`,节序为 Feedback → Documentation → Handoffs,并登记匹配的 `command-wrapup` probe Object [[STR-005]]。
- **FR-035**: 命令产物均为可逆写入,故 MUST 全程自动执行并出具三要素执行报告(执行内容、变更工件、修改途径),MUST 零阻塞确认门控。
- **FR-036**: 概念锚 `shared/definitions/derivation-definitions.md` MUST 为推导模型的唯一真源;命令模板、引擎 docstring、词汇表与用户文档 MUST 引用而非复述其规则。
- **FR-037**: 随框架分发的文件(`templates/` 与 `shared/`)MUST 保持客户中性:不含特性或需求编号,不含真实语料的 URL 或标题;示例 MUST 用槽位化合成形式。
- **FR-038**: `.specify/derive/` MUST 在框架布局图 `shared/definitions/framework-map.md` 中登记一行,使新存储根对布局真源可见。

### Key Entities *(include if requirement involves data)*

- **Source Record (`S-<nnn>`)**: 一个经线上核实的来源。属性:claimed_title(含去重后保留的全部标题变体,FR-008)、resolved_title、title_mismatch(脚本计算)、grade、url、access、resolved_via、verification(具体证据)。等级与 access / resolved_via 的取值集归锚 §Provenance Grades / §Source Record,本文件不复列。是链条最底层的前提来源。
- **Reasoning Move (`M-<nnn>`)**: 一个从来源论证方式中抽取的可复用推理模式。属性:name、inference_form(带命名槽位)、prevents、applies_when(含过度使用护栏)、anchor(限定形式 `<topic-slug>.S-<nnn>`,FR-014)、status(**持久**二值,取值归锚 §Move Record)。项目级累积,身份全局单调且只由引擎发放;`new`/`reused`/`reinforced` 不是属性,只作为运行相对处置出现在引擎输出里(FR-009)。
- **Derivation Step (`D-<k>`)**: 一次算子对显式前提的应用。属性:premises(S 与更早的 D)、leads(可选,community/unverified 线索)、move(恰好一个 M)、derivation、conclusion、falsification、confidence(取值归锚 §Step Record)、contested-with。步骤序上构成有向无环图。
- **Architecture Element (`A-<k>`)**: 一条被推导出的架构断言。属性:statement、derived-from(≥1 个 D,强制且全部可解析)、confidence(按最小值继承)、open-questions。
- **Open Question (`Q-<k>`)**: 一处已记录的前提缺口。属性:question、why-undetermined、would-resolve(指向被阻塞的 A)、discriminator(能定案的证据)。与 A 双向链接。
- **Move Library**: [[STR-006]] 中的 `moves.md` 单表文件,项目级累积算子存储,引擎独写,git 跟踪。
- **Derivation Archive**: [[STR-006]] 中的 `<topic-slug>/derive.md`,一个主题一份推导档案,含来源表、无法核实来源清单、所应用算子、推导链、派生架构、未决问题、终止声明 [[STR-008]]、自审表(冻结节序归 `data-model.md` §持久化形态)。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对一份含 1 个死链与 1 个社区改标题文章的 handed-in 清单,检出率为 100%(两者都在来源表里留下可定位的记录:双标题 / `access` / `resolved_via` / `verification`),静默丢弃数为 0。
- **SC-002**: 对任意通过 `validate`(退出码 0)的推导档案:锚定在 `community`/`unverified` 来源上的步骤数 = 0,缺 `derived-from` 的架构元素数 = 0,前向引用与环数 = 0。
- **SC-003**: 对同一主题连续两次运行:第二次运行的 `stats` 报告 `reused` + `reinforced` 计数 > 0,且算子库中重复 `move_id` 数 = 0、重复归一化 `inference_form` 数 = 0。
- **SC-004**: 禁用论证字面量在 `derivation`/`conclusion` 中的命中数 = 0;对分别注入 [[STR-001]] 中任一字面量的 fixture,`validate` 退出码为 4 且错误信息定位到 C3。
- **SC-005**: 在无线上能力的环境下运行:可锚定步骤数 = 0,`unverified` 来源数 = 全部来源数,运行在建链前停止,`## Derived Architecture` 节为空或不存在,且输出含降级说明。
- **SC-006**: 命令面接线完备且零回流:四份工具副本存在并携带 AUTO-GENERATED 标记;probe 注册表 internal 计数较基线 +1 且 `--validate` 退出码 0,`--reconcile` 错误集不因本命令扩大;门控扫描 total 不超过基线;复杂命令分类计数与 docs-step 分类计数各 +1;全套件名字级新增失败数 = 0。三条纪律型 FR 由同一 SC 承载,各自有可判定计数:**FR-036** —— 命令模板对概念锚的根相对引用数 ≥ 1、正文含字面 `never restate`,且模板与锚内复述锚表/枚举/阈值的命中数 = 0;**FR-037** —— `templates/commands/derive.md` 与 `shared/definitions/derivation-definitions.md` 中真实域名 URL 命中数 = 0(`example.invalid` 除外)、特性/需求编号形态命中数 = 0;**FR-038** —— `shared/definitions/framework-map.md` 中 `.specify/derive/` 行数 = 1。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 引擎 `validate` 与 `stats` 的 JSON 输出(来源表按 grade / access / title_mismatch 分组计数)+ 集成测试 US1 的固定语料 fixture(含活链、死链有快照、死链无快照、改标题四类)。基线:0(命令尚不存在)。每次运行该 fixture 时测量。
- **SC-002 Source**: 引擎 `validate` 的 `errors[]`(按规则编号 C1 / A7 分类)。单元测试对注入缺陷的 fixture 逐个断言退出码 4;集成测试 US3 对完整 fixture 断言退出码 0。每次 `validate` 调用即时可得。
- **SC-003 Source**: 引擎 `stats` 的运行相对处置分量(new / reused / reinforced 计数 —— 由引擎输出报告,不是库列,FR-009)+ 对 `moves.md` 的重复 ID 与重复归一化 `inference_form` 扫描。由集成测试 US2 以两次顺序运行测量。
- **SC-004 Source**: 引擎 `validate` 的 C3 命中明细。单元测试参数化遍历 [[STR-001]] 的每个字面量,断言各自被拒。基线:0。
- **SC-005 Source**: 集成测试 US3 在模拟无线上能力(不注入任何线上工具、`probe-links` 被 monkeypatch 为失败)下的运行输出:锚定步骤计数、unverified 计数、是否存在 `## Derived Architecture`、降级说明是否存在。
- **SC-006 Source**: 契约测试 `tests/contract/test_derive_command_surface.py`(副本 + 标记 + 节序 + 零 BLOCKING 匹配;并承载三条纪律型 FR 的计数:FR-036 的根相对锚引用数与字面 `never restate` 存在性、模板与锚内复述命中数 = 0;FR-037 的 shipped-surface 中性扫描 —— 两文件真实域名 URL 命中数 = 0、编号形态命中数 = 0;FR-038 的 `shared/definitions/framework-map.md` 中 `.specify/derive/` 行数 = 1)、`feedback-utils.py --action probes --validate` 与 `--reconcile` 的退出码与计数、`scan-confirmation-gates.py --root . --json` 的 `total`、两个分类契约测试的计数断言、以及 `run-tests.sh --names-out` 与 `baseline-failed.txt` 的 `comm -13` 差集(必须为空)。基线:门控 total 23、probe internal 72、复杂命令分类 18、docs-step 分类 15、全套件 50 条既有失败;三条纪律型计数的基线为 0(命令与锚尚不存在)/ framework-map 行数 0 → 1。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `best practice` · `best practices` · `industry standard` · `commonly accepted` · `it is generally agreed` · `everyone knows` · `as is well known` · `obviously` · `业界通用` · `业界最佳实践` · `最佳实践` · `众所周知` · `经验之谈` · `权威做法` · `不言而喻` | 封闭禁用论证字面量集(封闭集:扩充须同时改概念锚与引擎,见 FR-019)。FR-019, SC-004, `contracts/derivation-model.md` C-3, `shared/definitions/derivation-definitions.md` §Banned Justifications, 引擎 `BANNED_JUSTIFICATIONS` 常量, `tests/unit/test_derive_validate.py` 参数化用例 |
| `STR-002` | 自审表列头:`\| # \| check \| method \| result \|`;检查项 ID 集 `A1`…`A14`;语义待背书集字面量 `semanticChecksPending` | FR-029, FR-030, `contracts/derivation-model.md`, 引擎 `validate` 输出, `tests/unit/test_derive_validate.py` |
| `STR-003` | 引擎六动作名:`init` · `validate` · `moves-list` · `moves-add` · `probe-links` · `stats` | FR-032, `contracts/derive-engine.md`, `tests/contract/test_derive_engine_contract.py`, `templates/commands/derive.md` 内联调用, Tool 记录 |
| `STR-004` | 退出码语义:`0` ok · `1` usage/unknown action · `2` input error · `3` not found · `4` validation failed | FR-032, `contracts/derive-engine.md`, 引擎 `EXIT_*` 常量, 全部引擎测试 |
| `STR-005` | probe object 身份:`speckit-derive-wrapup`(class `command-wrapup`,unit `/speckit.derive`,lifecycle `wrap-up`) | FR-034, `shared/definitions/probe-definitions.md` Objects 表, `feedback-utils.py --action probes --validate` 与 `--reconcile`, SC-006 |
| `STR-006` | 存储路径:`.specify/derive/moves.md`(算子库)与 `.specify/derive/<topic-slug>/derive.md`(推导档案) | FR-012, FR-016, FR-038, `contracts/move-library.md`, `shared/definitions/framework-map.md` 新行, 引擎 `ARCHIVE_DIRNAME` 与 `MOVES_FILENAME` 常量 |
| `STR-007` | 降级理由字面量:`no-online-capability` | FR-007, SC-005, `contracts/derivation-model.md`, 引擎降级分支, 集成测试 US3 |
| `STR-008` | 终止声明节:节标题 `## Termination`;节内两行字面量 `- condition: <a\|b>` 与 `- steps: <n> / <budget>` | FR-023, FR-024, FR-029(A12), `data-model.md` §持久化形态(冻结节序), `contracts/derivation-model.md` C-14, `contracts/derive-engine.md` C-8/C-18, `tests/unit/test_derive_validate.py` |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Out of Scope

- **handed-in 语料本身**:触发本特性的那份阅读清单是**示例输入**,MUST NOT 随框架分发(裁定见 §Clarifications 末条,纪律见 FR-037);分发面只允许槽位化合成示例。
- **爬虫 / 镜像能力**:`probe-links` 是**佐证者**而非爬虫 —— 它只为 agent 的落地判断留下不可编造的证据痕迹(锚 §Script / Prompt Boundary),MUST NOT 抓整站、批量下载正文、建本地语料缓存,也 MUST NOT 替代 agent 自己的阅读。
- **用户源代码**:本命令 MUST NOT 修改用户源代码、产品脚本或测试用例;其写入集只有 [[STR-006]] 下的推导档案与算子库。
- **替代 Plan**:Derivation MUST NOT 替代 `/speckit.plan`,也 MUST NOT 引用 Plan —— 依赖方向单向(Plan MAY 按 `A-<k>` 身份引用架构元素);边界表归锚 §Derivation vs Research vs Plan。
- **特性级调研**:特性范围内的证据采集与选型归 `/speckit.research`;本命令的对象是**主题**,不产出特性级决策记录。
- **`.specify/derive/` 作为镜像对**:该根是项目运行时数据(与 `.specify/goal/`、`.specify/specs/` 同类),MUST NOT 登记进 `sync-mirrors.py` 的 `MIRROR_PAIRS` —— 否则 `specify init` 的加法 copytree 会把一份示例库推进每个下游项目。

## Clarifications

- Q: 命令的核心职责是「从主题推导经典文献图谱」「从权威资料推导项目规范」「从结论反推依据链(溯源)」还是「从上游产物推导下游产物」? → A: 都不是。需要进一步阅读这几篇文献的内容;**重点不在于理解文献或整理资料,而是通过学习其思维方式,构建用于推导的思维链路,通过逐步逻辑推导,形成完整架构**。(2026-09-05,用户直接裁定)
- Q: 命令运行时是否需要联网抓取原始资料? → A: **必须联网核实来源**。(2026-09-05,用户直接裁定)
- Q: 新命令按哪种规格落地——直接落地命令、走完整 SDD 特性流程、还是命令 + 仅登记特性索引? → A: **走完整 SDD 特性流程**(注册特性 → requirements → plan → contracts → tasks → implement),与仓库既有惯例一致。(2026-09-05,用户直接裁定)
- Q: 推导产物 `derive.md` 写到哪里——特性内产物、项目级推导档案、还是两者按上下文解析? → A: **项目级推导档案** `.specify/derive/<topic-slug>/derive.md`,类比 `.specify/goal/<goal-slug>/`;这样领域级推导可跨特性复用。(2026-09-05,用户直接裁定)
- Q: 从文献里提取的「思维算子」是否跨运行累积复用? → A: **累积为项目级算子库**,后续运行先复用再补充。(2026-09-05,用户直接裁定)
- Q: handed-in 的 REST/Web 架构文献清单是否应作为默认语料随框架分发? → A: 否。它是**示例输入**而非框架内容;真实 URL 与标题一旦进入 `templates/` 或 `shared/` 就会随包分发一份会腐烂的语料(清单中已有一个死链),并预判了本应保持中性的领域。分发文件只用槽位化合成示例(FR-037)。(2026-09-05,设计裁定)
