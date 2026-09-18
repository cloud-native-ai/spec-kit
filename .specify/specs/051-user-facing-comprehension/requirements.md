# Requirements Specification: 面向用户可理解性纪律——不用行话、带足上下文(User-Facing Comprehension)

**Requirement Branch**: `051-user-facing-comprehension`
**Created**: 2026-09-17
**Status**: Draft
**Input**: User description: ""without jargon, with context"是一个很好的原则需要把它扩散的所有面向用户的流程中,比如提示用户进行确认的流程,比如feedback的流程. 还需要把这条原则输出到用户自己的项目的constitution中(通过constitution模板和命令输出). 当前项目中已经在很多流程中应用了这条规则,但是项目本身没有把它明确的定义出来. 可以把它定义到shared/guidelines中,设定好程度(不能完全杜绝jargon,也不能无限制的添加context)."

## Related Feature *(mandatory)*

**Feature ID**: 051  
**Feature Name**: 面向用户可理解性纪律(User-Facing Comprehension)

绑定依据(clarify 2026-09-17 第二轮 Mode A):**新建 Feature 051**,不绑定既有 Feature。按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 的**同胞吸收启发式**逐个核验 8 个候选后,结论是**无既有 Feature 拥有本需求引入的能力**——每个候选只匹配一个侧面,且同胞吸收证据均不支持绑定:

| 候选 Feature | Status | 同胞 specs | 与 051 的实际关系 |
|---|---|---|---|
| 040 Token Efficiency Discipline | Implemented | 1(自身) | **最接近的结构先例**:同为 `shared/guidelines/` 纪律文档 + 指令模板常驻章节 + 契约测试守卫,且其"全局阈值 + 场景可显式声明覆盖值(声明处生效,不回写本节)"形态被本特性直接复用为读者基准的裁定形状(R2-Q2)。但主题是 token 消耗,非读者可理解性 |
| 032 Task Complexity Rubric | Implemented | 1(自身) | **决定性先例**:同为嵌入指令文件、经 `/speckit.instructions` 非破坏投递的行为纪律,却仍自成一个 Feature 而非绑 008 Instructions Command——确立"以指令段形式嵌入是**投递事实**,不是**归属事实**"。050 已援引同一先例 |
| 046 Confirmation Gate Governance | Implemented | 1(044) | 051 消费其治理保留清单与执行报告三要素,并给门控提示**新增**措辞义务;但 051 明确不改其"是否门控"判据(FR-017),且 11 类界面中只有 2 类属门控——绑入会使归属名不副实 |
| 042 Interview Mode | Implemented | 0 | 拥有 `interview-pattern.md`,即可理解性规则今天唯一的完整表述处;但 FR-021 恰是要把那四条规则**从** 042 **搬出**到独立真源——绑入与本需求方向相反 |
| 028 Feedback Mechanism | Implemented | 3(027/041/047) | **同胞吸收能力最强**的候选,但主题是反馈存储与 Probe 建模;051 只消费其 `feedback-step.md` 的对外措辞规则并把它降级为实例(FR-019),不扩展反馈能力 |
| 031 Glossary Mechanism | Implemented | 1(自身) | 拥有 canonical 术语与就地注解的**出向**衔接点(白名单第 ② 条);但词汇表管的是"用哪个词",本纪律管的是"要不要注解、要不要给上下文" |
| 005 Constitution Command | Completed | 0 | 仅投递载体(生成下游宪章原则的命令);按 032 先例,投递事实不构成归属 |
| 023 Prompt Template Quality | Draft | 0 | 主题是模板的结构校验与一致性强制;051 的守卫确属结构契约测试,但约束对象是**面向用户消息的措辞**,不是模板结构 |

决定性先例是 **032**(与 **040**):投递载体与文件形态与本需求完全相同,却都各自成为独立 Feature。此外 051 引入三个既有 Feature 范围均不覆盖的持久面——**行话侧白/黑名单**、**上下文侧下限/上限与裁决顺序**、**一般化的双落点守卫**(FR-035)——归属新建。上表八个 Feature 以**交叉引用**(消费关系)记入 `.specify/memory/features/051.md`,不构成归属。

**同型先例的警示**:Principle XIV(One Source of Truth)作为一条纪律落地时**既未回流模板、也未登记 Feature**——今天它在 `.specify/memory/features.md` 中零命中。051 MUST NOT 重演:本特性同批完成 Feature 登记与模板双落点回流(FR-028)。

## Overview

框架今天**已经在很多流程里执行"不用行话、带足上下文"这条规矩,却从未把它定义出来**:研究实测在 `shared/`、`templates/`、`skills/` 中找到 **38 处独立措辞**,分散在至少 4 个互不引用的领域(访谈提问、反馈通知、门控执行报告、项目总结报告),而**真源文档数量为 0**,`白话`/`行话`/任何一个统一名字在仓库中的出现次数也是 0。这正是 `one-source-of-truth.md` 所定义的"静默分歧"温床——同一事实有 38 个定义点,改一次要改 38 个文件,纪律已经破了。

本特性把这条无名规矩**命名、定界、并给出可判定的程度**:

1. **定名与定源**:在 `shared/guidelines/` 建立唯一真源文档 [[STR-002]],命名该纪律,并按三层表面模式(真源文档 → 指令文件常驻章节 → 契约测试)使其常驻可见、可守。
2. **设定程度(双向边界,不是形容)**:用户明确要求"不能完全杜绝 jargon,也不能无限制的添加 context"。因此本纪律 MUST 同时给出**行话侧白名单/黑名单**(哪些术语 MUST 保留、哪些 MUST 不出现)与**上下文侧下限/上限**(每条消息至少承载什么、最多承载到哪为止),并配一套**第三方可复现的机械判据**,使两个独立评审者对同一条消息得出同一结论。
3. **扩散到全部面向用户界面**:枚举封闭的**界面类**集合(门控确认提示、执行报告、反馈通知、访谈提问、澄清提问、主动建议行、干系人工件、外部读者报告、词汇表校正呈现、收尾报告、失败报告),每类的规则真源以**单行指针**接入,不复制正文。
4. **输出到下游项目的宪章**:经 `templates/constitution-template.md` 新增一条原则 [[STR-003]] + `templates/commands/constitution.md` 的 `MUST include` 清单**双落点**导出,使每个下游项目 bootstrap 即得,并自动进入其 `plan` 门控的动态枚举。

该纪律最终围绕两个不可分割的判定:

1. **读者要不要解码**:面向用户的消息里每个未注解的技术术语,MUST 能归入白名单的某一条;否则读者会"自信地答错"——访谈模式文档已用这句话点明了后果(`interview-pattern.md:281`)。
2. **读者要不要翻页**:消息 MUST 让读者不打开其他工件即可行动(下限),同时 MUST NOT 复述读者可自行打开的工件(上限)——承载方式是**陈述决定所依赖的事实 + 以路径引用其余一切**,这与 One Source of Truth 的"指针而非副本"是同一种形状。

### 现状锚点(以源码实测为准)

- **唯一写全的地方在一份"模式"文档里,且作用域只有一种交互形态**:`shared/patterns/interview-pattern.md:119-126` 的 `**Comprehension rules (可理解性规则)**` 块含四条本纪律的核心规则(白话优先、无未解释缩写/行话、就地注解特殊术语、绝不假定共享上下文),`:281` 有对应反模式 `Jargon and bare abbreviations`,`:280` 有 `Context-free questions`(即"带足上下文"半侧)。但 `:125-126` 混在同一列表里的另两条(每问一决策、问 what 不问 whether)**不是**可理解性规则,本纪律 MUST NOT 吞并。更关键:该模式的"嵌入契约不可丢弃清单"(`:255`)**没有把 Comprehension rules 列进去**,所以宿主收窄时它可以被合法丢掉。
- **镜像关系**:`shared/patterns/interview-pattern.md` 与 `.specify/shared/patterns/interview-pattern.md` 为逐字节镜像(`sync-mirrors.py`);`templates/commands/interview.md:154` 与 4 份按工具再生的副本(`.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/`)以**内容形态**复述了同一条规则;`docs/reference/commands/interview.md:65` 是第三份手写复述。**无 interview 技能**(`skills/` 36 个目录中无 `*interview*`),故该流程只有命令模板 + 4 份机械副本 + 模式文档 + 文档空间四处表面。
- **门控治理只管"是否门控",从不管"如何措辞"**:`shared/guidelines/confirmation-gates.md` 全文 99 行,两级判据(`:7-12`)、破坏性清单(`:14-21`)、治理保留清单 13 行表(`:23-41`)、存疑从严(`:43-45`)、回流约束(`:47-52`)、门控观察协议(`:70-99`)**全部与措辞无关**。全文仅两处沾边:
  - `:56-60` 执行报告三要素(**执行内容 / 产出·变更工件逐项可定位 / 修改途径**)——这是"带足上下文"半侧,已一般化,本纪律 MUST 引用而非复述;
  - `:68` `收尾阶段达阈值触发的反馈提交提示 MUST 为非阻塞一次性提示(附 /speckit.feedback package 用户视角途径,不展示 feedback-utils.py 引擎原始调用)`——**这是该文档中最强的"不用行话"规则**,点名了`用户视角途径`并禁止暴露引擎调用,但作用域**仅限反馈提交提示**,且作为 `## 执行报告` 的尾段被埋没,从未一般化。其契约测试 `tests/contract/test_confirmation_gates_execution_report.py:44-46` 只断言了 `非阻塞` 与 `自动传输`,**并未断言 `用户视角途径` / 不暴露引擎调用这一子句**——即该规则今天连守卫都没有。
- **门控扫描器零措辞检查**:`scripts/python/scan-confirmation-gates.py:46-64` 的 **17 条** `BLOCKING_PATTERNS`(展开为 22 个顶层 alternation 分支)全部检测**阻塞行为**(`等待用户确认`、`explicit user confirmation`、`stop and confirm`、`preview → confirm → execute` 等),无任何行话/白话/注解/上下文模式。`:38-44` 的 `POLICY_DOCS` 豁免集(现含 `reconcile-pattern.md`、`interview-pattern.md`,外加 `SELF_REL` 的 `confirmation-gates.md`)是"定义纪律的文档可以援引门控措辞而不被计数"的既有机制——**新真源文档若引用任何阻塞措辞作反例,须在此登记**(具体注册点)。`:35` 的 `SCAN_DIRS` 含 `shared`、`:36` 的 `SCAN_ROOT_FILES = ("templates",)` 含根级 `templates/*.md`,故 `shared/guidelines/` 与 `templates/instructions-template.md`、`templates/constitution-template.md` 下新文件**全部自动进入扫描范围**。
- **反馈流程是本纪律传播最广的实例**:`shared/workflow/feedback-step.md` 是该规则的**事实真源**——`:89-90`(canonical 块第 6 步)、`:113-114`(`Present the choices in user-facing terms … never the raw feedback-utils.py engine path`)、`:141`(`engine detail — do not paste the bare flag into the user-facing line`)。其传播足迹为 **195 个文件**——本数值是 plan 期 2026-09-17 以 `grep -rl "never paste the raw" --include=*.md .` 实测的**唯一定义点**,该计数随仓库演进漂移(需求阶段实测为 194),故本规格他处一律以指针引用而不复述字面量,守卫亦 MUST NOT 钉死此数值。命中面含 21 个 `templates/commands/*.md` 各一行、`skills/merge-skills/SKILL.md:179-180`、`docs/reference/skills/feedback.md:140-142`,以及 4 棵按工具树。`:115` 自陈存在**两种并存措辞**(长式与 `sanitize.md:116` / `derive.md:184` 的短式),并规定"仍只写 invite the user to submit 的嵌入副本以本节为准"——即该文档已经在做"收敛到真源"的工作,但**它的权威只覆盖反馈,不覆盖其他界面类**。
- **澄清流程只借了半侧**:`templates/commands/clarify.md:70` 明写"从 `interview-pattern.md` 只借 **context discipline**(每问说明为何出现、答案将改变什么)与 fact-vs-decision 拆分","刻意不采纳其开放式提问规则"——**但从未借"不用行话"半侧**,`clarify.md` 全文无任何措辞/可理解性规则。`shared/guidelines/requirements-guidelines.md:72-88` 的 `[NEEDS CLARIFICATION]` 提示模板规定了 `**Context**` / `**What we need to know**` / 选项表,同样**对措辞零约束**。`shared/constants/clarify-taxonomy.md:56` 的 "Canonical glossary terms" 是澄清分类里唯一与行话相邻的钩子。
- **最完整的实现搁浅在一个技能里**:`skills/summarize-project/references/reporting-playbook.md:109-113` 的 `## 1.7 读者用语纪律(内部标识不得渗入正文)` 是**全仓最成体系的实例**——一份完整的内部标识黑名单(分级码 `T1–T5`、`E1–E5`、`RC-*`、`CG-*`、`§编号`、`M-*`、引擎字段名、库/表/列/SQL、脚本名)+ 一张读者向改写映射表(`unknown-schedule` → 「无计划日期,无法判定延期」),`:309` 有落盘门禁,`references/consistency-rules.md:31` 交叉引用(`**字段名是内部标识**`)。同技能 `references/project-overview.md:22` 有最直白的中文表述:`**业务语言**:摘要面向外部读者,只出现数值与业务措辞,不出现字段名、脚本名与内部编号。`,`:51` 有可机械核查的清单门 `- [ ] 无内部黑话;外部读者不读代码也能看懂`。**框架其余部分完全够不到它。**
- **主动建议行已有"上下文上限"的现成形态**:`shared/guidelines/proactive-trigger.md:47` `one non-blocking line = what the flow is for + the exact invocation the engine supplies`(镜像于 `templates/instructions-template.md:31`)——这正是"带足上下文但不膨胀"的落地样板:用途 + 确切调用形式,一行。`:95` 另有措辞约束(提议形态是批准而非阻塞)。
- **干系人工件侧的既有表述**:`shared/guidelines/requirements-guidelines.md:24,101` `Written for non-technical stakeholders` / `Written for business stakeholders, not developers`,`:22,32,43,129-131` `No implementation details` / `technology-agnostic`,`:138-141` 给出**坏→好改写对**(`"API response time is under 200ms"` → `"Users see results instantly"`);`templates/requirements-template.md:46,61,75` 占位符即 `[Describe this user journey in plain language]`。
- **词汇表流程是"入向 + 呈现"半侧**:`shared/workflow/glossary.md:23-24` `When a correction is applied, **surface it** so it is traceable and the user can override it`(附示例 `note: interpreted 『speck it』as canonical 『Spec Kit』 (glossary)`),`:25-26` 绝不破坏性改写用户原始输入,`:27-28` 歧义变体不猜而从用户,`:65` 该文件本身 MUST 人类可读。`templates/commands/interview.md:30` 是**出向**半侧:提问 MUST 用词汇表 canonical 术语并在每问首次出现时就地注解。
- **既有 guideline 文档的房子骨架**(新文档 MUST 对齐):H1 取 `# 中文名(English Name)` 或 `# English Name`;前 3–8 行内声明所有权(三要素:owns 什么、ambient 指针在哪、MUST 引用/MUST NOT 复制);紧接一段"防的是什么失效";H2 分节(规则 → 边界 → 程度 → 程序 → 与相邻原则的关系);全文 RFC-2119 大写关键词。**程度的表达有四种房子先例**:粗体数值字面量 + 单一定义点声明 + 覆盖协议(`token-efficiency.md:38` 小文件阈值 `≤ 100 行` 且 `≤ 10 KB`)、编号升级阶梯 + 禁止跳级(`:26-34`)、条件表(`one-source-of-truth.md:33-41` 三行"何种重复才合法")、粗体机械测试(`one-source-of-truth.md:29` `if changing the fact would require editing more than one file, the discipline is already broken`)。每份 guideline 都带一条**范围限制/不新增机制**子句(`one-source-of-truth.md:70`、`token-efficiency.md:42-44`)。
- **暴露通道的硬约束(传播陷阱)**:`generate-instructions.sh:73-78,101-137` 是**按整章节的增量调谐**——只注入模板中存在而活动文件中缺失的顶级 `## ` 章节,**既有章节永不触碰**;`proactive-trigger.md:3` 已明写此结论:`指针不依赖在既有章节(如文档地图表)内部新增一行,因为增量调谐只按整章节传播,既有章节内部的改动抵达不到已初始化项目`。守卫见 `tests/contract/test_instructions_section_propagation.py:35-46`。⇒ **新纪律 MUST 以新增顶级 `## ` 章节暴露;只往文档地图表(`templates/instructions-template.md:11-20`)加一行不会抵达任何已初始化项目。**
- **宪章导出的双落点与一个已发生的前车之鉴**:`templates/constitution-template.md` 现有 11 条原则(I–XI),单条结构为 `### <罗马数字>. <Title Case 名称>` → 一句以冒号结尾的主张 → 3–6 条 MUST/MUST NOT 要点(硬折行 <100 字符)→ 恰好一个空行 → `Rationale:` 段(1–4 句);唯一"援引 guideline 文档"的先例是 `:103-106`(Better-Harness 锚定 `.specify/shared/guidelines/better-harness.md` 并写明 "reference it, do not restate it"),其 `:110-111` 是配套的范围限制要点。`templates/commands/constitution.md:77-125` 的 **`MUST include` 清单**才是真正的导出机制(逐条点名 5 条原则并拼出其要点),`:40-41` 另授权 bootstrap 时**拒绝**不相关的模板原则。`:56-71` 版本方案 `x.y.z.ddd`,新增原则 = **MINOR** 递增(`:66`);`:142-148` 要求前置 Sync Impact Report。**前车之鉴**:本仓活动宪章 `.specify/memory/constitution.md` 已有 14 条原则,其中 `:155-163` 的 **Principle XIV(One Source of Truth)从未回流**到 `templates/constitution-template.md` 或命令的 `MUST include` 清单——`grep -n "One Source\|XIV"` 在这两个文件中**零命中**,故**没有任何下游项目收到它**。这是本特性 MUST 避免的同型失效,也是 FR-020 双落点要求的直接依据。
- **下游自动传导已成立,无需改 plan 模板**:`templates/plan-template.md:37-42` 的 `## Constitution Check` 明写"Do NOT hard-code principle names here",而是读 `.specify/memory/constitution.md`、按 `### <roman-or-arabic-numeral>. <name>` **动态枚举**每条原则各渲染一行。⇒ 新原则一旦进入宪章即自动抵达每次 `/speckit.plan` 门控。
- **镜像机制无需注册**:`scripts/python/sync-mirrors.py:72-78` 的 `MIRROR_PAIRS` 含 `("shared", ".specify/shared", False, set())`,`:83-94` 以 `rglob("*")` 发现全部文件——**无 manifest、无逐文件清单**,新增 `shared/guidelines/<name>.md` 自动被拾取。`pyproject.toml:37` 的 `"shared" = "specify_cli/shared"` 与 `_CORE_SPECIFY_ASSETS` 均为目录级,同样无需改动。`tests/contract/test_shared_reference_directory.py:19-22` 的 `TYPED_DOCS["guidelines"]` 是 `issubset` 断言(`:43`),新文件静默通过。
- **按工具副本自动再生**:`scripts/python/regen-command-copies.py`(由 `sync-mirrors.py:202-211` 委派)从 `templates/commands/*.md` 再生 `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`,仅处理目录已存在的工具。⇒ 命令模板改动后 MUST NOT 手工批改副本。
- **可复用的守卫模板**:`tests/contract/test_one_source_of_truth.py` 是最完整样板(C-1..C-9:文档存在 + 镜像逐字节一致 `:64-67`;前 8 行声明所有权且含 `"single source of truth"` + `"MUST NOT copy"` `:72-76`;各节齐备 `:79-82`;实质规则术语 `:87-104`;MUST/MUST NOT 关键词 `:106-109`;模板两份副本各含且仅含一次标题与指针 `:114-120`;模板**不内联**文档节名 `:125-131`;`shared/` + `templates/` 单源扫描 `:142-153`;**项目中立性** `FORBIDDEN = ["spec-kit","specify-cli","specify_cli","cloud-native-ai"]` `:37,158-163`;宪章含该原则 + 版本下限 `MIN_VERSION = (1,11)` `:168-180`)。`tests/contract/test_token_efficiency_discipline.py` 同形(`SECTION_HEADINGS` 钉死于 `:21-28`,`test_cd5_headings_only_in_discipline_doc` 扫描 `:94-104`)。
- **观察标记的先例**:`token-efficiency.md:54` 规定反馈发现 MUST 内嵌稳定字面量 `token-efficiency`(供 `feedback-utils.py --action list --contains token-efficiency` 检索聚合),且"干净运行 MUST NOT 追加空洞观察条目"、"MUST **不编造**具体数值"。本纪律的观察标记 [[STR-005]] 沿用同一形态。
- **三层表面与同批加守卫的房子规矩**:`shared/guidelines/ask-record-repeat.md:86` `**house 模式(三层表面)**:真源文档(细则)→ 指令文件的常驻章节(摘要 + 指针)→ 契约测试(防漂移)。第三层是关键:没有守卫的重复会各自漂移,最后三处说法不一,比重复之前更糟。`;`:117` `给一条规矩新增表面时,MUST 同批加守卫(契约测试或既有扫描),否则新增的是未来漂移点而不是可达性。`;`:88-99` 给出指针形态 vs 内容形态的裁定表与机械测试(`:97`)。

**与现状的差异(本需求要闭合的缺口)**:

| 缺口 | 现状 | 目标 |
|------|------|------|
| 真源与命名 | 38 处独立措辞,0 份真源文档,0 个统一名字 | 1 份命名真源 [[STR-002]],其余以指针接入 |
| 程度可判定性 | 各处为形容性表述("白话优先""业务语言""不出现内部编号"),无统一判据 | 行话侧白/黑名单 + 上下文侧下限/上限 + 第三方可复现机械判据 |
| 门控措辞 | `confirmation-gates.md` 99 行零措辞规则;13 个治理保留门控无一附措辞义务 | 每类门控提示附措辞义务(以指针接入);`:68` 的反馈专属规则提升为一般规则 |
| 澄清措辞 | 只借"上下文"半侧,"不用行话"半侧缺失 | 两半侧齐备 |
| 搁浅实现 | `summarize-project` 的内部标识黑名单 + 改写映射只有该技能够得到 | 提升为本纪律黑名单/改写指引的实例来源,全框架可达 |
| 下游导出 | 该原则**不在**宪章模板,也**不在**命令 `MUST include` 清单;Principle XIV 同型缺口已发生且至今未修 | 双落点导出 [[STR-003]],同批回流 [[STR-006]](FR-028),下游 bootstrap 即得并自动进入 plan 门控 |
| 漂移守卫 | `confirmation-gates.md:68` 的最强措辞规则连契约断言都没有;宪章原则无双落点守卫(XIV 因此漏过) | 五表面守卫 + 项目中立性 + 单源扫描 + **一般化的双落点守卫**(以 XIV 为首个受测样本) + 扫描器豁免登记 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条无名规矩获得名字、真源、常驻可见性与守卫 (Priority: P1)

框架维护者打开 `shared/guidelines/`,能看到一份名为"面向用户可理解性"的纪律文档:它在前几行声明自己是这条规矩的唯一定义处,写明引用它的人 MUST 以路径引用而 MUST NOT 复制正文;它给出这条规矩防的是什么失效(读者解码术语就会自信地答错;读者翻页找上下文就会答另一个问题);它把"程度"落成两张条件表(许可行话 / 禁用行话)加两条边界(上下文下限 / 上下文上限),再配一套任何两个人用了都会得出同一结论的机械判据。任何 agent 在任何 `/speckit.*` 流程里都能读到这条纪律的摘要与指针——因为它是 `.specify/instructions.md` 里一个**新增的顶级章节**,不是既有章节里悄悄加的一行(后者抵达不到已初始化的项目)。改动其中任何一处表面,CI 会失败。

**Why this priority**: 这是其余一切的地基。用户的核心诊断是"项目本身没有把它明确的定义出来"——没有真源,扩散就没有可指向的对象,38 处措辞会继续各自漂移。同时它也是唯一能独立交付价值的一片:即便一处界面都还没接入,框架从此**有了这条规矩的名字和判据**,后续每次评审都能援引。

**Independent Test**: 只实现本片即可验证——检查真源文档存在、前 8 行含所有权声明与 MUST NOT copy 语义、五节(白名单/黑名单/下限/上限/机械判据)齐备、镜像逐字节一致、指令模板两份副本各含且仅含一次该章节标题与指针且不内联文档节名、契约测试全绿、项目专有名称零泄漏。交付的价值是"这条纪律从此有唯一权威定义点且被守卫"。

**Acceptance Scenarios**:

1. **Given** 一个已初始化的下游项目, **When** 运行既有的指令再生流程, **Then** 其 `.specify/instructions.md` 出现新的顶级章节 [[STR-004]],形如摘要 + 指向 [[STR-001]] 的指针,且既有章节逐字节未被触碰。
2. **Given** 真源文档 [[STR-002]] 已建立, **When** 运行镜像一致性检查, **Then** `.specify/shared/guidelines/` 下的副本与源逐字节一致,无需任何 manifest 注册。
3. **Given** 任取一条面向用户的消息, **When** 两位互不沟通的评审者分别套用文档给出的机械判据, **Then** 两人对"是否违反行话侧""是否违反上下文侧"得出同一结论。
4. **Given** 有人把真源文档里的白名单条件复制进某命令模板, **When** CI 运行单源扫描, **Then** 该复述被检出为内容形态副本并要求改回指针。
5. **Given** 有人删掉指令模板里的该章节标题, **When** CI 运行守卫, **Then** 测试失败。

---

### User Story 2 - 确认提示说人话、带足上下文,用户不必先读代码才敢批准 (Priority: P1)

用户在一个门控前停下——比如"feedback consume 将原子删除已消费的反馈包"。今天框架有 13 个这样的治理保留门控,却**没有任何一条规定这个提示该怎么写**。本特性之后,每个门控提示都受一条措辞义务约束:它用读者的词汇说明将要发生什么、载明不可撤销的后果与可逆性、给出确切的用户视角途径;它不出现引擎脚本名、内部函数名或分级代号——除非存在用户 MUST 逐字键入的标识符。门控执行完的三要素报告(执行内容 / 产出·变更工件 / 修改途径)保持不变,本纪律只引用它、不复述它。原先只写给"反馈提交提示"的那条最强规则(附用户视角途径、不展示引擎原始调用)被**提升为面向全部界面类的一般规则**,原处收敛为指针。

**Why this priority**: 用户点名"提示用户进行确认的流程"为扩散目标之一。这也是**风险最高**的界面:确认提示是用户唯一一次阻止不可撤销动作的机会,而一个需要解码的提示换来的是"自信地批准错东西"——门控本身反而制造了虚假安全感。同时今天这一片**零规则、零守卫**(`confirmation-gates.md:68` 的最强措辞子句连契约断言都没有),边际收益最大。

**Independent Test**: 抽样既有 13 个治理保留门控的提示文案,逐个套用机械判据;检查 `confirmation-gates.md` 已接入单行指针且其 `:68` 专属规则已提升为一般规则并收敛为指针;检查既有两级判据、破坏性清单、治理保留清单、回流约束**逐字未变**(本特性只增措辞义务,不改是否门控);检查门控扫描器的门控计数在改动前后不变。

**Acceptance Scenarios**:

1. **Given** 一个破坏性门控触发, **When** 提示呈现给用户, **Then** 一位本会话未打开过仓库的读者能在不追问任何术语含义的前提下作出批准/否决决定。
2. **Given** 同一门控存在用户视角途径(如 `/speckit.*` 命令), **When** 提示措辞生成, **Then** 面向用户的行中不出现引擎脚本或内部函数调用形态。
3. **Given** 某门控**不存在**用户视角途径, **When** 提示必须给出可执行形态, **Then** 原始标识符被保留(白名单第 3 条),但被标注为引擎细节并附一句说明它做什么。
4. **Given** 一个可逆动作已自动执行, **When** 收尾呈现执行报告, **Then** 三要素齐备且由 `confirmation-gates.md` 继续拥有其定义,本纪律文档不复述该三要素。
5. **Given** 改动落地, **When** 运行门控扫描器与既有门控契约测试, **Then** 两级判据/清单/回流约束未被改写,门控计数不变,全部测试通过。

---

### User Story 3 - 下游项目的宪章收到这条原则,并在 plan 门控里被逐条枚举 (Priority: P1)

一位用户在自己的项目里跑 `specify init` 然后 `/speckit.constitution`。生成的宪章里出现一条新原则 [[STR-003]],结构与既有原则完全一致(罗马数字标题 → 一句以冒号结尾的主张 → 3–6 条 MUST/MUST NOT 要点 → 空行 → `Rationale:` 段);其中一条要点锚定 [[STR-001]] 并写明"reference it, do not restate it",另一条要点是"不新增机制"的范围限制。之后他跑 `/speckit.plan`,Constitution Check 门控**自动**把这条原则枚举成一行——因为该门控是动态枚举宪章标题的,不需要任何硬编码改动。宪章版本按 MINOR 递增,并前置 Sync Impact Report。

导出走**双落点**:宪章模板新增该原则 **且** `/speckit.constitution` 的 `MUST include` 清单新增对应条目。只改模板不改命令是不够的——本仓 Principle XIV(One Source of Truth)就是前车之鉴:它只存在于活动宪章与一份契约测试里,两个模板文件 `grep` 零命中,所以**没有任何下游项目收到它**。本特性一并把这个既有缺口修好(FR-028),并把它当作"宪章原则 MUST 双落点"这条新守卫的**第一个受测样本**(FR-035)——守卫本来就需要样本,而用一个真实发生过的事故做样本,才能证明它拦得住同型失效,不只是拦得住"新原则忘了写"。

**Why this priority**: 用户显式点名"还需要把这条原则输出到用户自己的项目的constitution中(通过constitution模板和命令输出)"。这一片也**独立可交付且独立有价值**:即便框架自身的界面接入尚未完成,下游项目从第一天起就在其宪章与 plan 门控中拥有这条原则。同时它是唯一一片**跨项目传播**的——US1/US2 的收益限于读到本仓真源的场合,US3 的收益抵达每一个采纳项目。

**Independent Test**: 在一个空白目录跑 init + `/speckit.constitution`,检查生成的宪章含 [[STR-003]] **与**回流的 [[STR-006]] 两条原则且结构合规(标题层级、冒号结尾主张、要点数、恰好一个空行、`Rationale:` 段、折行 <100 字符)、各含 guideline 锚定要点与范围限制要点、无未解释的方括号占位符、版本格式合规、Sync Impact Report 已前置;再跑 `/speckit.plan` 检查两条原则均出现在 Constitution Check 表中且 `plan-template.md` 未被改动;最后人为从模板侧或命令侧删掉**观察名单内**任一原则,确认双落点守卫失败。

**Acceptance Scenarios**:

1. **Given** 一个新初始化的下游项目, **When** 运行 `/speckit.constitution`, **Then** 其宪章含原则 [[STR-003]],且 `templates/constitution-template.md` 与 `templates/commands/constitution.md` 的 `MUST include` 清单**双双**含它。
2. **Given** 下游宪章已含该原则, **When** 运行 `/speckit.plan`, **Then** Constitution Check 表按动态枚举多出一行,且 `plan-template.md` 零改动。
3. **Given** 本仓活动宪章, **When** 同批落地, **Then** 新增对应原则、版本 MINOR 递增、Sync Impact Report 前置。
4. **Given** 某下游项目在 bootstrap 时判定该原则与其领域无关, **When** `/speckit.constitution` 依既有授权(`templates/commands/constitution.md:40-41`)拒绝它, **Then** 该拒绝被记录进 Sync Impact Report,MUST NOT 静默丢弃。
5. **Given** 随包分发的真源文档与两个模板文件, **When** CI 运行项目中立性断言, **Then** 本仓专有名称零泄漏。
6. **Given** Principle XIV 已回流至两个模板文件, **When** 新下游项目跑 `/speckit.constitution`, **Then** 其宪章同时含 [[STR-006]](基线:今天 0% 的下游项目收到它),且 `plan` 门控把它一并枚举。
7. **Given** 双落点守卫已一般化为一份**具名观察名单**(初始 = {[[STR-003]], [[STR-006]]},见 FR-035 范围订正), **When** 有人从宪章模板或命令 `MUST include` 清单任一侧删除**名单内**任一原则, **Then** CI 失败——包括删除 [[STR-006]] 这一历史上真的漏过的场合。

---

### User Story 4 - 反馈流程的对外措辞归入同一纪律,不再自成一格 (Priority: P2)

反馈流程今天已经是全仓**执行得最好**的一片:`shared/workflow/feedback-step.md` 拥有"绝不把引擎调用粘进面向用户的行"这条规则,并已传播到近百个命令模板、技能与文档表面(实测计数见 Overview 现状锚点)。但它自成权威——它的规矩只管反馈,别的界面类援引不到;它自己还承认存在两种并存措辞(长式与短式),靠一句"以本节为准"临时压住。本特性之后,该文档以单行指针接入本纪律,其既有规则**保留**为该纪律在"反馈通知"这一界面类上的实例(不另立第二套措辞规则),两种并存措辞的收敛方向从"以本节为准"变为"以纪律真源为准"。阈值提示、提交通知、自省呈现的对外措辞同受下限/上限约束。

**Why this priority**: 用户点名"feedback的流程"为扩散目标,故属显式要求。但排 P2 而非 P1:这一片**今天已高度合规**(其跨表面传播足迹即证据,实测计数见 Overview 现状锚点),边际工作是"命名归属 + 一般化",而非"从零修复";其失效风险与 US2(零规则、零守卫、直接决定不可撤销动作)不在一个量级。此为基于实测证据的排序判断,已记入 Assumptions。

**Independent Test**: 检查 `shared/workflow/feedback-step.md` 已接入单行指针且其 `:89-90`/`:113-114`/`:141` 三处既有规则**保留未删**(降级为实例,不是被替换);检查 `confirmation-gates.md:68` 的反馈专属措辞规则已被 US2 提升为一般规则、原处收敛为指针且二者不冲突;抽样若干命令模板的 `## Feedback` 第 6 步,确认仍指向 `/speckit.feedback package` 用户视角途径、仍为非阻塞、仍不自动传输。

**Acceptance Scenarios**:

1. **Given** 反馈条目数达阈值, **When** 收尾呈现提交提示, **Then** 提示为非阻塞单行、附用户视角途径、不含引擎原始调用、不触发任何自动传输。
2. **Given** `feedback-step.md` 已接入指针, **When** 检视其既有三条措辞规则, **Then** 三条全部保留,文档头部另有一行指向本纪律真源。
3. **Given** 一个只写短式措辞的嵌入副本, **When** 判定其权威来源, **Then** 优先级为"本纪律真源 > `feedback-step.md` 的反馈专属实例",不再是"`feedback-step.md` > 旧嵌入副本"的两级。
4. **Given** 反馈自省运行且无可理解性违规, **When** 收尾记录, **Then** 不追加空洞观察条目;有违规则条目内嵌稳定标记 [[STR-005]] 且不含编造计数。

---

### User Story 5 - 38 处分散措辞收敛为指针,搁浅的实现被提升为全框架可达 (Priority: P2)

维护者想改一次"什么算许可行话",今天需要改 38 个地方;本特性之后只改 1 个。每类面向用户界面的**规则真源文档**都携带一行指向本纪律的指针,不再各自复述白名单/黑名单/下限/上限。访谈模式文档的 `Comprehension rules` 收敛为指针 + 其**模式特有**规则(每问一决策、问 what 不问 whether)——本纪律不吞并后两条。澄清流程补齐它今天缺失的"不用行话"半侧。`summarize-project` 里那份最成体系的内部标识黑名单与读者向改写映射被**提升**为本纪律黑名单与改写指引的实例来源,提升后原处以指针接入、不再保留第二份独立黑名单。按工具的机械副本(4 棵树)交由既有再生脚本处理,MUST NOT 手工批改。

**Why this priority**: 这是把"定义了"变成"只有一处定义"的收敛工作,直接兑现 One Source of Truth 的修复方向("把它变成引用,而不是把措辞改得一致")。排 P2:它依赖 US1 的真源先存在;且其失效模式是**长期漂移**而非**当次答错**,风险曲线比 US2/US3 平缓。但它 MUST NOT 被无限期推迟——`ask-record-repeat.md` 已警告"没有守卫的重复会各自漂移,最后三处说法不一,比重复之前更糟",而本特性正在新增第 39 处表面。

**Independent Test**: 对 `shared/` + `templates/` + `skills/` 运行单源扫描,统计以**内容形态**复述本纪律规则(白名单/黑名单/下限/上限/机械判据)的位置数量,基线 38 → 目标 0(机械副本与测试钉死字面量除外,二者是 `one-source-of-truth.md:33-41` 承认的合法重复);检查 11 类界面的规则真源文档各含且仅含一行指针;检查 `interview-pattern.md` 仍保留其模式特有两规则、`clarify.md` 已补齐行话半侧、`reporting-playbook.md:109-113` 已收敛为指针。

**Acceptance Scenarios**:

1. **Given** 白名单新增一个许可条件, **When** 修订完成, **Then** 只需编辑真源文档 1 个文件;单源扫描不报出任何需同步修改的第二处。
2. **Given** `interview-pattern.md` 的 Comprehension rules 已收敛, **When** 检视该文档, **Then** 可理解性四规则改为一行指针,而"每问一决策""问 what 不问 whether"两条**原文保留**(它们不属本纪律)。
3. **Given** `clarify.md` 今天只借上下文半侧, **When** 接入完成, **Then** 其提问与选项表同受行话侧约束,且**不**采纳访谈模式的开放式提问规则(既有裁定不变)。
4. **Given** `summarize-project` 的内部标识黑名单已提升, **When** 检视该技能, **Then** 原处以指针接入本纪律,不再保留独立黑名单;其读者向改写映射成为本纪律的实例来源。
5. **Given** `templates/commands/interview.md` 被改动, **When** 运行既有再生脚本, **Then** 4 棵按工具树的副本自动更新,无手工批改痕迹。

---

### Edge Cases

- **不存在用户视角途径时怎么办?** 引擎调用形态是唯一可执行信息。此时原始标识符 MUST 保留(白名单第 3 条),但 MUST 标注为引擎细节并附一句说明它做什么——`feedback-step.md:141` 的 `(engine detail — do not paste the bare flag into the user-facing line)` 是该形态的既有样板。MUST NOT 因为"不用行话"而删掉用户唯一能执行的东西。
- **用户自己先用行话怎么办?** 白名单第 1 条:镜像用户本轮已使用的术语。MUST NOT 把专家用户的话降级改写——那是另一种不尊重。
- **白话改写会损失精度怎么办?**(安全/合规上的关键区分) 精度优先:保留术语并就地注解,MUST NOT 为了白话而抹掉区分。
- **消息是机器消费而非人类消费**(脚本解析的报告、测试夹具、JSON 字段名) 不在本纪律作用域内;纪律只约束人类面向的表面。
- **上下文下限与非阻塞单行上限冲突** 二者属**不同界面类**:单行上限约束的是"非阻塞流程建议"(`proactive-trigger.md:47` 是其形态真源),下限约束的是"需要用户作出决定的门控提示"。MUST NOT 把两类折叠成一条规则;文档 MUST 给出裁决顺序。
- **上下文下限与 Token 效率纪律的摘要优先冲突** 解法唯一:陈述**派生事实**、以**路径引用**其余一切,MUST NOT 把机器管理数据文件的原文当作上下文注入。文档 MUST 显式写出这条和解,不留给读者推断。
- **"每问就地注解"与"不要重复啰嗦"冲突** 消费单元是判定粒度:访谈模式的裁定是**每问**都要注解,因为"用户可能在数天后单独读到这一问"(`interview-pattern.md:122`)。⇒ 注解义务按**消费单元**计,不按会话计;文档 MUST 把消费单元定义清楚。
- **真源文档为举反例而引用阻塞措辞** 会命中 `scan-confirmation-gates.py:46-65` 的 `BLOCKING_PATTERNS` 并使门控计数虚增。MUST 依既有 `POLICY_DOCS` 机制(`:38-44`)登记豁免。
- **下游项目拒绝该原则** `templates/commands/constitution.md:40-41` 已授权 bootstrap 拒绝不相关的模板原则。允许,但拒绝 MUST 记录进 Sync Impact Report,MUST NOT 静默丢弃。
- **新增第 39 处表面本身成为漂移点** `ask-record-repeat.md:117` 的规矩:新增表面 MUST 同批加守卫。US1 的契约测试与本清单的每个表面一一对应,否则本特性自己就是它要修的问题的又一实例。
- **文档地图表加一行不生效** 增量调谐只按整章节传播(`generate-instructions.sh:73-78`;`proactive-trigger.md:3` 已明写)。MUST 以新增顶级 `## ` 章节暴露;只加表格行是一个**静默失效**——文件看着改了,已初始化项目收不到。
- **常驻章节到了、真源文档没到(悬空指针)** 实测两条投递路径不同步:章节经 `/speckit.instructions` 增量调谐注入既有指令文件,真源文档只在 `specify init` 附加式 copytree 或 `sync-mirrors.py` 时抵达,而 `generate-instructions.sh` 全文**不同步 `shared/`**。已初始化的下游项目只刷新指令文件,就会拿到指向不存在文件的指针。这是既有 11 份 guideline 共有的结构性状况,非 051 新造 ⇒ FR-038 只加**同批抵达 + 缺失显式提示**义务,MUST NOT 静默呈现悬空指针;修投递机制本身属另一条 Feature(见 Out of Scope)。
- **只改宪章模板不改命令** Principle XIV 的实际失效路径:模板里有的原则,命令的 `MUST include` 清单没点名,下游就拿不到。⇒ FR-020 要求双落点,守卫 MUST 分别断言两处。
- **`interview-pattern.md` 的嵌入契约不可丢弃清单没列 Comprehension rules**(`:255`) 收敛为指针后,该清单 MUST 把"接入本纪律的指针"纳入不可丢弃项,否则宿主收窄时仍可合法丢掉。
- **跨表面措辞轮换**(命中面实测计数见 Overview 现状锚点) MUST 经既有再生脚本处理机械副本;手写表面按 US5 逐个收敛为指针。MUST NOT 发起一次覆盖全部命中文件的手工批改。

## Requirements *(mandatory)*

### Functional Requirements

#### 真源、命名与常驻可见性

- **FR-001**: 框架 MUST 在 `shared/guidelines/` 下建立**唯一真源文档** [[STR-002]],为"不用行话、带足上下文"这一纪律命名并定义其全部规则。文档 MUST 在前 8 行内声明自身为该纪律的唯一定义处,并声明:引用本纪律的命令、技能、代理与共享文档 MUST 以路径引用本文档,MUST NOT 复制其规则正文。
- **FR-002**: 真源文档 MUST 经既有镜像机制在 `.specify/shared/guidelines/` 下产生**逐字节一致**的副本 [[STR-001]],使每个下游项目初始化即得;MUST NOT 要求任何 manifest 或逐文件注册(既有镜像按目录全量发现)。
- **FR-003**: 本纪律 MUST 以 `templates/instructions-template.md` 中**新增的顶级 `## ` 章节** [[STR-004]] 常驻暴露,形态为"摘要 + 指针"(对齐既有 guideline 章节的房子形态:一段引出核心主张与固定指针短语,2–5 条子规则要点,可选收尾指针行)。MUST NOT 仅以文档地图表格行暴露——增量调谐只按整章节传播,既有章节内部的改动抵达不到已初始化项目。该章节与真源文档的**同批抵达义务**见 FR-038。
- **FR-004**: 真源文档 MUST 遵循既有 guideline 房子骨架:H1 命名;前 3–8 行所有权声明(owns 什么 / ambient 指针在哪 / MUST 引用且 MUST NOT 复制);紧接一段"防的是什么失效";H2 分节(规则 → 边界 → 程度 → 与相邻原则的关系);全文使用 RFC-2119 大写关键词;并含一条**范围限制/不新增机制**子句。

#### 程度:行话侧(双向边界之一)

- **FR-005**: 真源文档 MUST 给出**许可行话**的封闭条件集(白名单),判定对象为 FR-037 定义的基准读者,至少覆盖:① 用户在本消费单元已先行使用的术语;② 项目词汇表的 canonical 术语,且在该消费单元内首次出现时就地注解;③ 用户 MUST 逐字键入或复制的标识符(命令、路径、参数、环境变量);④ 用户自身项目/领域的业务术语;⑤ 由输出格式自身定义、且同时被具名的短形式(如决策 ID)。
- **FR-006**: 真源文档 MUST 给出**禁用行话**的封闭条件集(黑名单),至少覆盖:① 存在用户视角途径时的引擎/脚本/函数内部调用形态;② 内部代号、分级码、字段名、库表列名等内部标识渗入面向读者的正文;③ 在该消费单元内首次出现却无就地注解的缩写;④ 以代码符号名充当行为概念名的提问。
- **FR-007**: 用户要求的"不能完全杜绝 jargon" MUST 以 FR-005 白名单的形式落地为**可判定的许可条件**;MUST NOT 落地为"尽量少用""避免术语"一类形容性表述。白名单之外的行话一律按违规处理。
- **FR-008**: 真源文档 MUST 定义**消费单元**(comprehension obligation 的计账粒度),并规定就地注解义务按消费单元计而非按会话计——依据是读者可能在数天后单独读到其中一条(既有裁定见 `interview-pattern.md:122`)。

#### 程度:上下文侧(双向边界之二)

- **FR-009**: 真源文档 MUST 定义**上下文下限**:每条面向用户的消息 MUST 承载足以让读者(基准读者定义见 FR-037)**不打开其他工件即可行动**的事实,至少包括——为何此刻出现、该决定/回答将改变什么、用户可以做什么(确切的用户视角途径或编辑入口);门控类消息另 MUST 载明不可撤销后果与可逆性。
- **FR-010**: 真源文档 MUST 定义**上下文上限**:"带足上下文" MUST NOT 被解释为复述读者可自行打开的工件。承载方式 MUST 为**陈述决定所依赖的事实 + 以路径引用其余一切**。上限 MUST 遵守既有约束:非阻塞建议保持单行(其形态真源为 `proactive-trigger.md`,本文档只引用不复述);MUST NOT 把机器管理数据文件的原文当作上下文注入(Token 效率纪律 摘要优先)。
- **FR-011**: 用户要求的"不能无限制的添加 context" MUST 以 FR-010 的上限**加**每类界面既有的长度/形态约束共同落地;真源文档 MUST NOT 引入与既有约束冲突的第二套长度规则。**程度表达形态已经用户裁定(clarify 2026-09-17 R2-Q3=A)**:取**定性上限 + 沿用各界面既有数值约束**,MUST NOT 为每类界面新增裸数值上限,亦 MUST NOT 新增单一全局数值上限。**已知代价经用户知情接受**:门控确认提示与流程收尾报告两类界面因此**没有长度界**,理论上可无限增长;接受该代价的**条件**是——增长 MUST 由 FR-013 的机械判据("读者要不要翻页")与 FR-010 的承载方式("陈述决定所依赖的事实 + 以路径引用其余一切")共同兜住,即长度不设界但**形态**设界(复述工件即违规,不论长短)。若实现后实测出现无复述的纯膨胀,升级路径是在该类界面真源处声明覆盖值(FR-037 同型协议),而非回写真源文档新增全局数值。
- **FR-012**: 当某类界面的上下文下限与上限冲突时,真源文档 MUST 给出**裁决顺序**,MUST NOT 留下"二者皆可解释"的空白界面类。已知冲突至少两处:① 下限 vs 非阻塞单行上限(裁决:属不同界面类,不折叠);② 下限 vs 摘要优先(裁决:陈述派生事实 + 路径引用,不注入原文)。两处和解 MUST 显式写出。
- **FR-013**: 真源文档 MUST 提供**第三方可复现的机械判据**(而非品味判断):对任一面向用户的消息,任何两个独立评审者按该判据 MUST 得出同一结论(是否违反行话侧、是否违反上下文侧)。判据 MUST 与既有房子的"机械测试"先例同形(粗体可执行判句,如 `one-source-of-truth.md:29`)。

#### 扩散:面向用户界面类

- **FR-014**: 真源文档 MUST 枚举本纪律约束的**面向用户界面类**(surface classes)为**封闭集**,至少覆盖:① 门控确认提示;② 门控执行报告;③ 反馈阈值/提交通知;④ 访谈提问;⑤ 澄清提问与选项表;⑥ 主动流程建议行;⑦ 面向干系人的需求/规划/任务工件;⑧ 面向外部读者的项目总结报告;⑨ 词汇表校正的对外呈现;⑩ 流程收尾报告;⑪ 失败如实报告。扩展该集合 MUST 只经修订真源文档,MUST NOT 分散到各命令模板。每类 MAY 依 FR-037 的覆盖协议在其真源文档处声明更严的读者基准;未声明者一律适用全局基准读者。
- **FR-015**: 每个被枚举界面类的**规则真源文档** MUST 以单行指针接入本纪律,MUST NOT 以内容形态复述其白名单/黑名单/下限/上限/机械判据。
- **FR-016**: 本特性 MUST 在**同一批**内完成全部 **11 类**面向用户界面的真源文档指针接入,**并**同批完成两处搁浅实现的收敛/提升(FR-021 的访谈模式 Comprehension rules 收敛、FR-022 的项目总结内部标识黑名单提升)。裁定依据(clarify 2026-09-17 R1-Q1=A):用户显式诉求为"扩散到**所有**面向用户的流程",分批接入会使 38 处措辞中的大部分在收敛完成前继续各自漂移;两处搬家虽改写被广泛镜像的模式文档与一个技能的内部参考文档、回归面最大,但**隔离到另一次并不会降低其回归面**,只会让"38 → 0"的收敛量长期停留在中间态。⇒ 回归风险 MUST 由同批的守卫(FR-029..FR-032)与端到端实测(FR-026)承接,而非由缩小范围承接。
- **FR-017**: 门控治理文档(`confirmation-gates.md`)MUST 保持**是否门控**的唯一判据真源地位不变;本特性只新增**门控如何措辞**的约束并以指针接入。其两级判据、破坏性动作清单、治理保留清单、存疑从严规则、回流约束 MUST 逐字未被改写。
- **FR-018**: 门控治理文档中既有的、**仅限反馈提交提示**的"用户视角途径、不展示引擎原始调用"规则 MUST 被提升为面向**全部**界面类的一般规则并归本纪律所有;原处 MUST 收敛为指针。此为"记录规则而非实例"(举一反三)的直接应用。
- **FR-019**: 反馈流程的对外措辞真源(`shared/workflow/feedback-step.md`)MUST 以单行指针接入本纪律;其既有三处措辞规则(`:89-90`、`:113-114`、`:141`)MUST **保留**为该纪律在"反馈通知"界面类上的实例,MUST NOT 另立第二套措辞规则;两种并存措辞(长式/短式)的收敛权威 MUST 从"以本节为准"上移为"以本纪律真源为准"。
- **FR-020**: 澄清流程(`/speckit.clarify` 命令模板与 `[NEEDS CLARIFICATION]` 提示模板)MUST 补齐其今天缺失的"不用行话"半侧,方式为接入本纪律的单行指针;其既有裁定(封闭式提问、选项表 + Recommended、不采纳访谈模式的开放式提问规则)MUST 保持不变。
- **FR-021**: 访谈模式文档(`interview-pattern.md`)的 `Comprehension rules` MUST 收敛为对本纪律的指针 + 其**模式特有**规则;"每问一决策""问 what 不问 whether"两条 MUST 原文保留(二者不属可理解性纪律),本纪律 MUST NOT 吞并。该文档的**嵌入契约不可丢弃清单** MUST 同批把"接入本纪律的指针"纳入不可丢弃项。
- **FR-022**: 项目总结技能中已充分实现但**搁浅**的内部标识黑名单与读者向改写映射 MUST 被提升为本纪律黑名单与改写指引的**实例来源**;提升后原处 MUST 以指针接入,MUST NOT 保留第二份独立黑名单。
- **FR-023**: 按工具再生的机械副本(4 棵按工具命令树)MUST 交由既有再生脚本处理;MUST NOT 手工批改。手写表面(命令模板、技能文档、`docs/` 参考文档)按 FR-016 裁定的广度逐个收敛为指针。

#### 下游导出

- **FR-024**: 本纪律 MUST 经 `templates/constitution-template.md` 以**一条新原则** [[STR-003]] 输出到下游项目宪章。该原则结构 MUST 与既有原则一致:`### <罗马数字>. <Title Case 名称>` → 一句以冒号结尾的主张 → 3–6 条 MUST/MUST NOT 要点(硬折行 <100 字符)→ 恰好一个空行 → `Rationale:` 段(1–4 句)。要点 MUST 含:一条锚定 [[STR-001]] 并写明 "reference it, do not restate it";一条"不新增机制"的范围限制(对齐 Better-Harness 原则 `:110-111` 的先例)。
- **FR-025**: 本纪律 MUST 同时进入 `templates/commands/constitution.md` 的 **`MUST include` 原则清单**(即命令逐条点名、强制生成的原则列表),使 `/speckit.constitution` 在下游 bootstrap 时强制生成该原则。MUST NOT 只改模板而不改命令——本仓 Principle XIV(One Source of Truth)从未回流即为同型失效的实证(两个模板文件对其零命中,故无下游项目收到它);该缺口由 FR-028 在本批一并修复。
- **FR-026**: 下游宪章获得该原则后,`/speckit.plan` 的 Constitution Check 门控 MUST 自动纳入它(该门控按 `### <num>. <name>` **动态枚举**)。`plan-template.md` MUST NOT 需要任何硬编码改动;本特性 MUST **验证**该自动传导确实成立,而非假定成立。
- **FR-027**: 本仓自身的 `.specify/memory/constitution.md` MUST 同批获得对应原则,版本按 MINOR 递增,并按既有约定前置 Sync Impact Report。该宪章已含 Principle XIV,故本仓侧只新增一条原则;随包分发的宪章模板侧则新增两条(FR-024 的本纪律 + FR-028 的回流)。
- **FR-028**: 既有 Principle XIV(One Source of Truth,[[STR-006]])从未回流到 `templates/` 这一同型缺口 MUST 在**本批一并修复**:该原则 MUST 同时补入 `templates/constitution-template.md` 与 `templates/commands/constitution.md` 的 `MUST include` 清单,使其抵达下游项目。裁定依据(clarify 2026-09-17 R1-Q2=C):一并回流,并把这次事故用作 FR-035 双落点守卫的**第一个受测样本**——守卫本来就需要样本,边际成本近乎为零,而用一个真实发生过的缺口做样本能证明该守卫拦得住同型失效,而不只是拦得住"新原则忘了写"。

#### 漂移守卫

- **FR-029**: 新增的每一处表面 MUST **同批**获得漂移守卫(三层表面模式:真源文档 → 常驻章节 → 契约测试)。守卫 MUST 至少覆盖:① 真源文档存在且镜像逐字节一致;② 前 8 行声明所有权且含 MUST NOT copy 语义;③ 白名单/黑名单/下限/上限/机械判据/界面类枚举各节齐备;④ 指令模板两份副本各含且仅含一次章节标题 [[STR-004]] 与指针 [[STR-001]],且**不内联**真源文档的节名;⑤ 宪章模板与宪章命令 `MUST include` 清单**分别**含 [[STR-003]]。
- **FR-030**: 守卫 MUST 含**项目中立性**断言:随包分发的真源文档、宪章模板与命令模板 MUST NOT 泄漏本仓专有名称(对齐 `test_one_source_of_truth.py` 的 `FORBIDDEN` 先例)。
- **FR-031**: 守卫 MUST 含**单源扫描**:`shared/` + `templates/` 下以内容形态复述本纪律规则的位置数量为 0(机械副本与测试钉死的字面量属 `one-source-of-truth.md:33-41` 承认的合法重复,不计入)。
- **FR-032**: 若真源文档为说明违规形态而引用任何命中门控扫描器阻塞模式的措辞,该文档 MUST 被登记进扫描器的策略文档豁免集(`scan-confirmation-gates.py` 的 `POLICY_DOCS`),MUST NOT 使门控计数虚增;门控计数在本特性改动前后 MUST 不变。
- **FR-033**: 本特性 MUST NOT 引入任何新的运行时检查器、行话 lint 引擎、措辞评分系统、成熟度报告或跟踪台账(框架范围纪律 / 不新增机制)。执行手段 MUST 限于既有契约测试与既有扫描器的豁免登记。
- **FR-034**: `confirmation-gates.md:68` 既有措辞规则今天**无契约断言**(其测试只断言 `非阻塞` 与 `自动传输`)。该规则被 FR-018 提升为一般规则后,MUST 同批获得断言,MUST NOT 在无守卫状态下继续存在。
- **FR-035**: FR-029 ⑤ 的双落点断言 MUST **一般化**为一份**具名双落点观察名单**(watchlist)守卫:名单中的每个原则名 MUST 同时出现在随包分发的宪章模板与宪章命令的 `MUST include` 清单中,任一侧缺失即失败;名单初始为 {[[STR-003]], [[STR-006]]},扩展只经追加名单条目。回流的 Principle XIV([[STR-006]],FR-028)MUST 作为该守卫的**第一个受测样本**,以证明它拦得住一个真实发生过的同型缺口,而不只是拦得住"新原则忘了写"。守卫 MUST 按**完整原则标题**匹配(含括注),MUST NOT 钉死罗马数字字面量(模板与活动宪章的原则名册与编号本就不同),且 MUST NOT 把 `Code as the Single Source of Truth`(宪章命令 `:91` 既有条目)与 [[STR-006]] `One Source of Truth (Authority & Reference Discipline)` 混为一谈——二者是不同原则,活动宪章 XIV 的 Rationale 已显式区分。
  **范围订正(plan 期实测,2026-09-17)**:本条原文要求"宪章模板中的**每条**原则 MUST 在 `MUST include` 清单中有对应条目",该全称形式**在当前仓库不成立**——实测宪章模板有 11 条原则(I–XI),而命令的 `MUST include` 清单只有 5 条,二者交集仅 3 条(III Documentation-First、VIII Feature-Centric Development、IX Better-Harness Orientation);清单另含 2 条**不在模板中**的原则(Code as the Single Source of Truth、Documentation Naming & Location Conventions)。两个方向的包含关系今天都不成立,故全称守卫会在 8 条既有原则上立即失败。`MUST include` 清单的语义是"命令 bootstrap 时**至少**必须生成的原则",不是模板的镜像 ⇒ 唯一可实现的形态是具名观察名单。该订正**不削弱**用户在 clarify R1-Q2 选择的"当守卫样本"意图:XIV 在名单内,从任一侧删除它仍会使 CI 失败。

#### 观察与反馈

- **FR-036**: 收尾反馈自省 MUST 能捕获本纪律的违规观察。观察条目 MUST 内嵌稳定字面标记 [[STR-005]](供既有反馈引擎按标记检索聚合);MUST NOT 编造计数或数值;干净运行 MUST NOT 追加空洞观察条目。此为纯观察,MUST NOT 阻塞宿主流程,MUST NOT 追加对用户的提问。

#### 读者基准与投递(clarify 2026-09-17 第二轮裁定)

- **FR-037**: 真源文档 MUST 定义**唯一的基准读者**,作为行话侧(FR-005..FR-008)与上下文侧(FR-009..FR-013)共同的判定对象:**未在本会话打开过本仓库、但具备该项目领域知识的人**。各界面类 MAY 在其**规则真源文档处**声明更严的覆盖基准(如"面向干系人的需求/规划/任务工件"类覆盖为"不具备代码知识"),覆盖值**声明处生效、MUST NOT 回写真源文档**——形态对齐 `token-efficiency.md:38` 的"全局阈值 + 场景显式覆盖"房子先例。裁定依据(clarify R2-Q2=A):三种既有基准(SC-001 的"本会话未打开过仓库的读者"、`requirements-guidelines.md` 的"非技术干系人"、`summarize-project` 的"外部读者")MUST 收敛为**一条全局基准 + 至多两处类级覆盖**,而不是 11 套各自定义——后者会使真源文档从规则集退化为元规则,并让 38 处措辞的收敛量下降(各类仍可各说各话),与本需求核心目标相左。
- **FR-038**: 常驻章节(FR-003)与真源文档(FR-002)MUST **同批抵达**任一目标项目。二者投递路径实测不同步:常驻章节经 `/speckit.instructions` 的增量调谐注入既有指令文件(`generate-instructions.sh:101-137`,有 `test_instructions_section_propagation.py` 守卫),而真源文档只在 `specify init` 的附加式 copytree(`src/specify_cli/__init__.py:2202`)或 `sync-mirrors.py` 时抵达——`generate-instructions.sh` 全文**不同步 `shared/`**。故当宿主只刷新指令文件时,agent MUST 显式提示该指针所指文档缺失及其获取途径(重跑 init 或镜像同步),MUST NOT 静默呈现一个指向不存在文件的指针。裁定依据(clarify R2-Q4=A):该窗口是既有 11 份 guideline **共有的结构性状况**,不是 051 新造的,故本特性只加**提示义务**、不修投递机制(修 `generate-instructions.sh` 属另一条 Feature 的归属,见 Out of Scope)。

### Key Entities *(include if requirement involves data)*

- **可理解性纪律真源(Comprehension Discipline Owner)**: 该纪律的唯一权威定义点。属性:名称、所有权声明、失效陈述、行话侧两表、上下文侧两界、机械判据、界面类枚举、范围限制。与其他实体的关系:被所有"指针"引用;被守卫钉死;经导出实体投影到下游。
- **面向用户界面类(User-Facing Surface Class)**: 本纪律约束的一类人类面向消息(封闭集,11 类)。属性:类名、规则真源文档路径、**读者基准覆盖**(缺省即适用 FR-037 的全局基准;声明处生效、不回写真源文档)、上下文下限、上下文上限、既有长度/形态约束、是否含门控后果披露义务。关系:每类携带一行指向真源的指针;门控确认提示与执行报告两类的"是否门控"判据仍归 `confirmation-gates.md` 所有。既有三种读者基准按 FR-037 收敛为一条全局基准 + 至多两处类级覆盖(干系人工件类、外部读者报告类)。
- **许可行话条目(Permitted-Jargon Entry)**: 白名单的一条可判定许可条件。属性:条件描述、依据、示例。关系:构成 FR-007 的"不能完全杜绝 jargon"的落地形态。
- **禁用行话条目(Forbidden-Jargon Entry)**: 黑名单的一条可判定禁止条件。属性:条件描述、内部标识类别、读者向改写映射(可选)。关系:由 `summarize-project` 的搁浅实现提升而来(FR-022)。
- **上下文界项(Context Bound Item)**: 下限项或上限约束。属性:方向(下限/上限)、内容、所属界面类、与既有纪律的和解方式。关系:冲突时由 FR-012 的裁决顺序裁定。
- **机械判据(Mechanical Verdict Test)**: 使可理解性违规可被独立复现判定的判句集合。属性:判句、判定对象(行话侧/上下文侧)、预期一致率。关系:SC-006 的度量对象。
- **宪章原则导出(Constitution Principle Export)**: 一条原则向下游项目的投影。属性:原则名([[STR-003]] / [[STR-006]])、罗马数字位置(按名匹配,不钉死字面量)、要点集(含 guideline 锚定要点与范围限制要点)、Rationale、**双落点**(宪章模板 + 命令 `MUST include` 清单)、版本递增类型。关系:使下游 `plan` 门控经动态枚举自动纳入(FR-026);任一侧落点缺失即由 FR-035 的守卫拦下——Principle XIV 正是历史上漏掉命令侧的实例。
- **漂移守卫(Drift Guard)**: 钉死各表面一致性的契约断言集合。属性:受测表面、断言类型(存在性 / 镜像一致性 / 所有权声明 / 节齐备 / 唯一性 / 项目中立性 / 单源扫描 / **双落点**)、合法重复豁免、变异式有效性抽查。关系:三层表面模式的第三层;缺失即"新增的是未来漂移点而不是可达性"(`ask-record-repeat.md:117`)。
- **可理解性观察条目(Comprehension Observation Entry)**: 收尾自省捕获的违规观察。属性:稳定标记 [[STR-005]]、所属单元、生命周期点、观察事实正文。关系:沿用 Token 效率纪律 `token-efficiency` 标记的同构形态;可经既有反馈引擎按标记聚合。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 任取一条面向用户的门控确认提示,一位本会话未打开过仓库的读者能在**不追问任何术语含义**的前提下作出批准/否决决定;抽样评审通过率 **100%**(基线:今天 13 个治理保留门控**无一**附措辞义务)。
- **SC-002**: 在存在用户视角途径的场合,面向用户的消息中出现引擎/脚本内部调用形态的次数为 **0**(可由既有文本检索机械核验;基线:该规则仅覆盖反馈提交提示 1 类界面)。
- **SC-003**: 本纪律的真源文档数量为 **1**;`shared/` + `templates/` + `skills/` 下以**内容形态**复述其规则(白名单/黑名单/下限/上限/机械判据)的位置数量为 **0**。基线:研究实测 **38 处独立措辞、0 份真源文档、0 个统一名字**。
- **SC-004**: 被枚举的 **11 类**面向用户界面,其规则真源文档携带指向本纪律的单行指针的比例为 **100%**(FR-016 已裁定为全量同批接入,无分批过渡态);两处搁浅实现在同批完成收敛/提升后,独立第二份规则副本数量为 **0**。
- **SC-005**: 新建下游项目经既有初始化 + 宪章流程后,其宪章含原则 [[STR-003]] 的比例为 **100%**,且含回流的 [[STR-006]] 的比例为 **100%**(基线:后者今天为 **0%**);该两条原则均出现在其 `plan` 门控的动态枚举中,`plan-template.md` 改动量为 **0 行**;导出双落点(FR-024/FR-025,守卫见 FR-035)零遗漏。
- **SC-006**: 两位互不沟通的评审者对同一批 **≥20 条**面向用户消息套用机械判据,结论一致率 **≥90%**(判据可复现,非品味判断;基线:今天无任何判据,判定完全依赖评审者直觉)。
- **SC-007**: 非阻塞流程建议行在接入本纪律后维持既有单行约束,**长度膨胀率为 0%**(抽样 100% 合规)。
- **SC-008**: 上下文下限与上限存在冲突的界面类,真源文档给出裁决顺序的比例为 **100%**;"二者皆可解释"的空白界面类数量为 **0**(已知冲突至少 2 处,均已点名)。
- **SC-009**: 漂移守卫覆盖**五个表面**(真源文档 / 镜像一致性 / 指令模板常驻章节 / 宪章模板 / 宪章命令 MUST-include 清单)的比例为 **100%**;守卫在 CI 中执行,人为改动任一处即失败。附加覆盖项目中立性与单源扫描两项断言。
- **SC-010**: 随包分发的真源文档、宪章模板与命令模板中,本仓专有名称泄漏数为 **0**。
- **SC-011**: 本特性引入的新运行时检查器 / 行话 lint 引擎 / 措辞评分系统 / 成熟度报告 / 跟踪台账数量为 **0**。
- **SC-012**: 门控扫描器的门控计数在本特性改动前后**完全不变**(真源文档的示例措辞未虚增计数;基线:扫描器 17 条阻塞模式全部只检测阻塞行为,零措辞检查)。
- **SC-013**: `confirmation-gates.md:68` 既有措辞规则在被提升为一般规则后**获得契约断言**(基线:0 条断言覆盖该子句);该规则处于无守卫状态的表面数量为 **0**。
- **SC-014**: 搁浅实现的可达性:`summarize-project` 的内部标识黑名单与读者向改写映射被全框架可引用的比例为 **100%**(基线:仅该技能内部可达),且提升后独立黑名单副本数量为 **0**。
- **SC-015**: 具名双落点观察名单(FR-035)中的原则,其在宪章模板与命令 `MUST include` 清单**两侧同时存在**的比例为 **100%**(名单初始 2 条:[[STR-003]]、[[STR-006]];基线:0 条原则受此守卫,且 [[STR-006]] 两侧均为 0 命中);人为从任一侧删除名单内任一原则后守卫失败的比例为 **100%**。
- **SC-016**: 两处搬家(FR-021 访谈模式可理解性规则收敛、FR-022 项目总结黑名单提升)完成后的**既有行为回归数为 0**——具体核验点:访谈模式仍原文保留其模式特有两规则、其嵌入契约不可丢弃清单已含新指针、澄清流程既有形态裁定未变、项目总结技能仍能产出合规报告、门控扫描器计数不变(SC-012)。此项是 FR-016 选择最大接入广度的配套风险约束。
- **SC-017**: 常驻章节所指的真源文档在目标项目中**缺失且未被显式提示**的发生数为 **0**(FR-038)。基线(**经 A-02 实测订正**):今天 `shared/guidelines/` 实有 **11** 份,但其中只有 **8** 份在活动指令文件里带常驻指针(模板面只 **7** 份,缺 `better-harness.md`),因而**只有这 8 份可能从指令面悬空**;`checklist-methodology.md`、`requirements-guidelines.md`、`self-improvement.md` 三份两个指令面都无指针,不会悬空、却也不受指针断言保护,改由余集断言核算(见 SC-017 Source)。全部 11 份的真源文档在"只刷新指令文件"路径下都**不会抵达**(实测 `generate-instructions.sh` 全文不同步 `shared/`)——该窗口存在但从未被度量或披露。
- **SC-018**: 全框架声明的**读者基准总数 ≤ 3**(1 条全局基准 + 至多 2 处类级覆盖),且覆盖值只出现在对应界面类的真源文档处、不回写真源纪律文档(FR-037)。基线:实现前并存 3 种互不引用的基准表述(SC-001 的"本会话未打开过仓库的读者"、`requirements-guidelines.md` 的"非技术干系人"、`summarize-project` 的"外部读者"),且无任何一处声明其为全局或覆盖。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 门控提示文案抽样评审——从 `confirmation-gates.md` 治理保留清单的 13 个门控中取样,由未参与本特性实现的评审者按机械判据逐条判定;每次门控文案变更后复测。基线于实现前采集一次(预期:0/13 附措辞义务)。
- **SC-002 Source**: 对 `shared/` + `templates/` + `skills/` 的既有文本检索(与本次研究用的同一手法:`grep -rl` 引擎调用形态字面量),统计面向用户行中的命中数;由契约测试在 CI 中执行,每次提交触发。基线:研究已实测该规则仅覆盖 1 类界面。
- **SC-003 Source**: 契约测试的单源扫描(对齐 `test_one_source_of_truth.py:142-153` 与 `test_token_efficiency_discipline.py:94-104` 的既有形态),排除机械副本与测试钉死字面量;CI 每次提交执行。基线 **38 处 / 0 真源** 由本次研究实测记录于 Overview 现状锚点。
- **SC-004 Source**: 契约测试遍历 FR-014 的 11 类界面枚举,逐类断言其规则真源文档含且仅含一行指针;CI 每次提交执行。基线:0/11。
- **SC-005 Source**: 端到端演练——在空白目录执行既有初始化 + `/speckit.constitution`,检查生成宪章含 [[STR-003]] 与 [[STR-006]] 两条原则;随后执行 `/speckit.plan` 检查 Constitution Check 表含二者;并对 `plan-template.md` 做 `git diff` 确认零改动。每次发布前执行一次。基线:[[STR-003]] 0%(不在任一模板中)、[[STR-006]] 0%(仅在活动宪章与一份契约测试中)。
- **SC-006 Source**: 双评审者盲测——取样 ≥20 条面向用户消息(覆盖 ≥5 个界面类),两人独立套用机械判据,比对结论;计算一致率。实现后执行一次,后续每次修订机械判据时复测。基线:不适用(今天无判据)。
- **SC-007 Source**: 对主动建议行的形态断言(既有 `proactive-trigger.md:47` 单行约束),由契约测试执行;另在实现前后各抽样一批建议行比对长度分布。基线:既有单行约束已生效,本项防的是接入本纪律后的**回归**。
- **SC-008 Source**: 契约测试断言真源文档含裁决顺序节,并对已点名的 2 处冲突逐个断言其和解文案存在;CI 每次提交执行。基线:0 处和解成文。
- **SC-009 Source**: 契约测试文件自身的覆盖清点(逐表面一条测试),对齐 `test_one_source_of_truth.py` C-1..C-9 的分组形态;CI 每次提交执行。另以"人为改动某表面后测试必须失败"的变异式抽查验证守卫**有效**而非仅存在。基线:0 个表面受守。
- **SC-010 Source**: 契约测试的项目中立性断言(复用 `test_one_source_of_truth.py:37,158-163` 的 `FORBIDDEN` 列表形态);CI 每次提交执行。基线:不适用(文件尚不存在)。
- **SC-011 Source**: 实现评审 + 新增文件清点——检查本特性新增的文件中是否存在可执行检查器/评分器/台账;由 `/speckit.analyze` 或代码评审判定。基线:0。
- **SC-012 Source**: 在实现前后各运行一次 `scripts/python/scan-confirmation-gates.py` 并比对门控计数(既有测试 `tests/contract/test_scan_confirmation_gates.py:64-130` 提供断言骨架);CI 每次提交执行。基线:实现前的计数值。
- **SC-013 Source**: 契约测试断言 `confirmation-gates.md` 的一般化措辞规则被覆盖(扩展 `tests/contract/test_confirmation_gates_execution_report.py:44-46` 既有用例);CI 每次提交执行。基线:0 条断言。
- **SC-014 Source**: 契约测试断言 `summarize-project` 原处以指针接入、且 `shared/` + `skills/` 下独立黑名单副本数为 0;CI 每次提交执行。基线:1 份搁浅黑名单、0 处外部可达。
- **SC-015 Source**: 双落点守卫测试(FR-035)——读取一份具名观察名单常量,逐个断言名单内原则标题同时出现在 `templates/constitution-template.md` 的 `### <num>. <title>` 标题集与 `templates/commands/constitution.md` 的 `**MUST include** a principle for "<name>"` 名称集中;并以变异式抽查验证守卫有效(人为从任一侧删除名单内一条原则后测试 MUST 失败)。匹配按完整标题、不按罗马数字。CI 每次提交执行。基线:0 条原则受此守卫;[[STR-006]] 在两个模板文件中零命中(`grep -c "One Source"` 实测双双为 0)。**注**:全称形式(遍历模板全部原则)经 plan 期实测**不可实现**,已按 FR-035 的范围订正改为具名名单。
- **SC-016 Source**: 逐点核验 + 既有测试套件——按 SC-016 列出的五个核验点逐个检查搬家涉及位置的既有行为(访谈模式两规则原文保留、嵌入契约不可丢弃清单含新指针、澄清既有形态裁定未变、项目总结技能端到端产出合规报告、门控扫描器计数不变),并运行既有相关契约测试(`test_confirmation_gates_*`、`test_scan_confirmation_gates`、`test_instructions_section_propagation`)确认全绿。改动前后各执行一次取差值。基线:不适用(搬家尚未发生);本项度量**回归**,不是收敛量。
- **SC-017 Source**: 契约测试 + 演练——构造"只有常驻章节、真源文档缺失"的项目状态(临时移除镜像副本),断言 agent 侧的提示义务被真源文档/常驻章节以规范措辞承载(即 FR-038 的义务成文且可被守卫检出),并断言既有 guideline 的同类窗口被同一义务覆盖而非只覆盖新文档。**"覆盖全部 11 份"的实现方式经 A-02 实测订正**:指针遍历只能抵达有指针者,故由 `ambient-section.md` **C-11** 的两段断言合计核算——C-11 主体对 `templates/instructions-template.md` 与 `.specify/instructions.md` **两个**指令面的全部指针断言目标存在(实测 7 / 8 份),**C-11(b)** 再从 `shared/guidelines/*.md` 派生全集、断言"全集 − 被指向集"**⊆** 那三份具名无指针者(子集语义:删指针即失败、日后补指针不误报),于是 11 份全部有归属而**不假装**遍历能抵达无指针的 3 份。CI 每次提交执行;另在发布前对一个真实的旧初始化项目演练一次。基线:0 份 guideline 有缺失提示义务(实测 `generate-instructions.sh` 全文不同步 `shared/`)。
- **SC-018 Source**: 契约测试遍历真源纪律文档与 11 类界面真源文档,统计"读者基准"声明处数量并断言 ≤3、且真源纪律文档中恰为 1(全局)、其余至多 2 处位于对应界面类真源文档内;CI 每次提交执行。基线:3 种并存表述、0 处声明为全局或覆盖(实测于 `SC-001` / `requirements-guidelines.md:24,101` / `summarize-project` 各层参考文档)。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | ".specify/shared/guidelines/user-facing-comprehension.md" | FR-002, FR-024, FR-029;宪章原则的 guideline 锚定要点;指令模板常驻章节的指针行;契约测试的路径断言 |
| `STR-002` | "shared/guidelines/user-facing-comprehension.md" | FR-001;镜像一致性断言的源侧路径;单源扫描的范围声明 |
| `STR-003` | "User-Facing Comprehension (No Jargon, With Context)" | FR-024, FR-025, FR-027, FR-029, FR-035;`templates/constitution-template.md` 新增原则标题;`templates/commands/constitution.md` 的 `MUST include` 条目名;`.specify/memory/constitution.md` 对应原则标题;契约测试的原则存在性断言与双落点守卫 |
| `STR-004` | "## User-Facing Comprehension" | FR-003, FR-029;`templates/instructions-template.md` 新增顶级章节标题;`.specify/instructions.md` 再生后的对应章节;章节传播契约测试 |
| `STR-005` | "user-facing-comprehension" | FR-036;反馈观察条目的稳定字面标记;既有反馈引擎按标记检索聚合的过滤值(形态对齐 `token-efficiency` 标记先例) |
| `STR-006` | "One Source of Truth (Authority & Reference Discipline)" | FR-028, FR-035;回流至 `templates/constitution-template.md` 的原则标题(取自 `.specify/memory/constitution.md:155` 既有原则名);`templates/commands/constitution.md` 的 `MUST include` 条目名;双落点守卫的第一个受测样本;SC-005 / SC-015 的断言对象 |

**Citation convention**: 当 FR、契约、任务或测试引用上述字符串时,写 `[[STR-NNN]]` 而非复制字面量;`/speckit.analyze` 可据此校验每个 `[[STR-NNN]]` 引用都解析到本节某一行。

**命名依据**: `user-facing-comprehension` 经预留标识符核查——该字串在本特性的 `shared/`、`templates/`、`skills/`、`scripts/`、`src/`、`tests/` 范围内**零占用**;`comprehension` 一词的既有使用为 `interview-pattern.md:119` 的 `Comprehension rules (可理解性规则)`(本纪律将收敛为指针的对象)与若干历史 spec 中的 `reader-comprehension` 度量措辞,二者均不构成标识符冲突。`STR-005` 的标记值取真源文档 basename,与 `token-efficiency` 标记取法一致。`STR-006` 逐字取自 `.specify/memory/constitution.md:155` 的既有原则标题(已实测核对),回流时 MUST 沿用该名而 MUST NOT 另拟——否则双落点守卫(FR-035)按名匹配会把它判为两条不同原则。`grep -c "One Source" templates/constitution-template.md templates/commands/constitution.md` 实测双双为 **0**,即 FR-028 所修缺口确实存在。

## Clarifications

### Session 2026-09-17

- Q: 界面类接入广度——本纪律写好后,11 类面向用户界面的真源文档各加一行指针即可;但其中两处不只是"加指针",而是要给已有内容搬家(访谈模式文档里那份今天写得最全的可理解性规则要收敛成一行指针;项目总结技能里那份最完整的"内部代号/字段名不许进正文"黑名单要被提升成全局够得到的来源)。这次做多少? → A: **全做,含两处搬家**。11 类指针接入 + 两处搬家在同一批内完成,38 处措辞一次收敛到 0。回归风险由同批守卫与端到端实测承接,而非由缩小范围承接(FR-016)。
- Q: 本仓宪章第十四条原则(One Source of Truth)从未回流到随包分发的模板里,导致没有任何下游项目收到它——这个既有缺口要不要顺手一起修? → A: **一起修,并当守卫样本**。该原则同批补入宪章模板与命令的强制包含清单(FR-028),并把这次真实发生过的事故用作"宪章原则 MUST 双落点"守卫的第一个受测样本(FR-035),以证明该守卫拦得住同型失效。

### Session 2026-09-17(第二轮 — `/speckit.clarify` Mode A)

- Q: 051 规格的 `Related Feature` 仍为 Need clarification;按绑定规则扫描 8 个候选 Feature 的同胞吸收证据后,051 归到既有 Feature 还是新建? → A: **新建 Feature 051(面向用户可理解性纪律)**。决定性先例是 032 Task Complexity Rubric 与 040 Token Efficiency Discipline——两者与本需求形状完全相同(`shared/guidelines/` 纪律文档 + 指令模板常驻章节 + 契约测试守卫),都各自成为独立 Feature 而非绑到投递载体,确立"以指令段形式嵌入是投递事实、不是归属事实"。8 个候选的同胞吸收证据均不支持绑定(040/032/031 各只有自身 1 个同胞,042/023/005 零同胞,028 有 3 个但主题是反馈,046 有 1 个但主题是"是否门控"而本需求明确不改它)。候选核验表与交叉引用记入 `Related Feature`;八个候选以消费关系记入 `features/051.md`,不构成归属。
- Q: 规格里"读者"有三种不同基准并存(SC-001 的"本会话未打开过仓库的读者"、`requirements-guidelines.md` 的"非技术干系人"、`summarize-project` 的"外部读者"),而 FR-005..FR-013 用泛指"读者"——白名单/黑名单/下限/上限是一套全局判据,还是按界面类参数化? → A: **全局一套 + 按类覆盖**。全局基准读者 = 未在本会话打开过本仓库、但具备该项目领域知识的人;界面类只在需要时于其真源文档处声明更严覆盖(声明处生效、不回写真源),形态复用 `token-efficiency.md:38` 的"全局阈值 + 场景显式覆盖"先例。落 FR-037;FR-005/FR-009/FR-014 加前向引用;Key Entities 的「面向用户界面类」增"读者基准覆盖"属性;新增 SC-018(读者基准总数 ≤3)。**未取方案的代价已成文**:11 套各自定义会使真源退化为元规则并削弱收敛量;单一基准不允许覆盖则与白名单第 ①④ 条冲突。
- Q: "不能无限制的添加 context"目前落成定性上限(陈述决定所依赖的事实 + 以路径引用其余一切),Assumptions 记录了为何不取裸数值——这个选型在需求阶段未经询问。定性上限够不够,还是要数值上限? → A: **定性上限 + 沿用各界面既有数值约束**,不新增逐类数值上限,也不新增单一全局数值上限。落 FR-011(选型由推断转为**用户裁定**)。**已知代价经知情接受并成文**:门控确认提示与流程收尾报告两类界面因此没有长度界;接受条件是长度不设界但**形态**设界——由 FR-013 机械判据("读者要不要翻页")与 FR-010 承载方式("路径引用而非复述")共同兜住,复述工件即违规、不论长短;若实测出现无复述的纯膨胀,升级路径是在该类界面真源处声明覆盖值(FR-037 同型协议)。
- Q: 实测发现常驻章节与真源文档投递路径不同步(章节经 `/speckit.instructions` 增量调谐注入既有指令文件;真源文档只经 `specify init` 附加式 copytree 或 `sync-mirrors.py` 抵达,`generate-instructions.sh` 全文不同步 `shared/`),已初始化的下游项目只刷新指令文件会拿到指向不存在文件的指针——这是既有 11 份 guideline 共有的结构性状况。051 要不要处理? → A: **记录为既有结构性状况 + 在 051 内加同批抵达义务**,不修投递机制。落 FR-038(同批抵达 + 缺失时 MUST 显式提示文档缺失及获取途径,MUST NOT 静默呈现悬空指针)、FR-003 加前向引用、Edge Cases 增"常驻章节到了、真源文档没到"一条、新增 SC-017(悬空且无提示的发生数为 0,守卫 MUST 覆盖全部 11 份 guideline 而非只覆盖新文档)、Out of Scope 增"投递机制本身的修复属另一条 Feature"。

### Session 2026-09-17(第三轮 — `/speckit.plan` Phase 0 实测订正)

本轮**无新增用户提问**;以下是 plan 期按 Principle VIII(代码为唯一真源)对源码实测后,对既有陈述的就地订正。全部订正均为**事实修正**,不改变任何已裁定的范围。

- 订正: `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS` 条数由 **18 → 17**(实测 `:46-64`;17 个元组条目展开为 22 个顶层 alternation 分支),引用范围 `:46-65` → `:46-64`。受影响处:Overview 现状锚点、SC-012。
- 订正: 反馈措辞规则的传播足迹由 **194 → 195 个文件**(`grep -rl "never paste the raw" --include=*.md .` 实测)。同时按 One Source of Truth 把该数值收敛为 **Overview 现状锚点的单一定义点**(附实测日期 2026-09-17 与"MUST NOT 被守卫钉死"声明);原先散布在 US4 叙述、US4 优先级论证、Edge Cases、Out of Scope、Assumptions 的 **6 处复述字面量改为指针引用**——该计数已在两个阶段之间漂移过一次,正是本纪律要消除的重复形态。
- 订正: `skills/merge-skills/SKILL.md:180` → **`:179-180`**;`docs/reference/skills/feedback.md:139-141` → **`:140-142`**。
- 订正: `shared/workflow/feedback-step.md:113-114` 的 `user-facing terms` 在源文件中**未加粗**,规格引文的粗体标记已去除(引文 MUST 逐字)。
- 订正(**范围性**): **FR-035 的全称双落点守卫不可实现**——实测宪章模板有 11 条原则(I–XI),命令 `MUST include` 清单只有 5 条,交集仅 3 条(III Documentation-First / VIII Feature-Centric Development / IX Better-Harness Orientation),且清单另含 2 条**不在模板中**的原则(Code as the Single Source of Truth、Documentation Naming & Location Conventions)。两个方向的包含关系今天都不成立 ⇒ 改为**具名双落点观察名单**(初始 {[[STR-003]], [[STR-006]]});SC-015 与其 Source 同步订正。该订正**不削弱** clarify R1-Q2 的"当守卫样本"意图:XIV 在名单内,从任一侧删除它仍会使 CI 失败。
- 确认(非订正,但提高约束强度): 门控预算实测 `total = 23`、`cap = 93 × 0.25 = 23.25` ⇒ **整数余量为 0**;且 `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` 钉死 total **等于** 23(不只是 ≤ cap)。故 SC-012("计数完全不变")是**硬门禁**而非软目标:新真源文档、新指令模板章节、新宪章原则中任何一行命中 17 条阻塞模式,即同时打爆两个契约测试。另实测 `SCAN_ROOT_FILES = ("templates",)` 使根级 `templates/*.md` 也在扫描范围内,且 `constitution-template.md` 的 governance-path 归类**不豁免于 `total` 计数**。处置方案见 `research.md` D-2。
- 订正: 界面类 ⑦(面向干系人的需求/规划/任务工件)与 ⑩(流程收尾报告)存在**规则真源缺口**——实测 `templates/plan-template.md` 与 `templates/tasks-template.md` **零**读者/措辞规则,⑩ 也无专属真源(规则分裂在 `confirmation-gates.md:62-66` 与 `feedback-step.md:86-93`)。FR-014 的枚举不变,归属裁定见 `research.md` D-3:⑦ 由 `requirements-guidelines.md` 单独拥有(缺口如实记录、不在本特性内给 plan/tasks 模板新增措辞规则),⑩ 由 `confirmation-gates.md` § 执行报告 拥有。

### Session 2026-09-18(第四轮 — `/speckit.analyze` 发现项的修复)

本轮**无新增用户提问**;以下是只读跨制品分析(3 个检测代理 + 12 个验证代理,全部 fresh-context)产出 46 条发现后,经用户指示"按照建议进行修复"而落地的**第一批修复**(3 条 HIGH + 5 条与系统性簇直接相关的 MEDIUM)。逐条记录如下,每条附验证代理的裁定。

- 订正(**I-01,HIGH**;原报 CRITICAL,验证裁定 downgrade):US3 的验收场景 7 与同故事的 Independent Test 仍要求**全称**双落点守卫("覆盖模板中全部原则""删除任一原则"),而 FR-035 在第三轮已判定全称形式不可实现并改为具名观察名单——第三轮的订正记录只列了 FR-035 / SC-015 / SC-015 Source 三处,**漏掉这两处**。验证代理独立复算:模板 11 条原则、命令清单 5 条、交集 3 条 ⇒ 8 条反例,两个方向包含关系均假。已把两处改为"具名观察名单(初始 = {STR-003, STR-006})"+"删除**名单内**任一原则"。**验证代理同时确认缺陷未向下传播**:`contracts/constitution-export.md`、`tasks.md` DoD-5、`feature-ref.md`、`plan.md` 四处均已是观察名单形态。
- 订正(**G-1,HIGH**;验证裁定 confirm):FR-008 的**消费单元**被 `feature-ref.md` 与 `discipline-doc.md` 的映射表**双向声称**由 C-13 覆盖,但 C-13 正文没有任何消费单元断言;该词在 `tasks.md` 与 `contracts/` 中零命中,`data-model.md` 的 V1.1–V1.6 也无一条断言它,T006 列举 E6 时只写了 4 个字段中的 3 个 ⇒ **映射自洽而被映射对象不存在**。验证代理另指出缺口比原报更宽:C-9/C-10 对 FR-005②/FR-006③ 的转述也丢掉了"该消费单元内"限定词。已修四处:C-13 增消费单元断言(恰好 1 条 + 按消费单元计而非按会话计 + 声明它是该限定词的唯一出处)、C-9 与 C-10 还原限定词并加"MUST NOT 简化为『首次出现』"、`data-model.md` V1.5 纳入该字段、T006 补齐 E6 的第 4 个字段。
- 订正(**G-4,HIGH**;验证裁定 confirm):T056 的证明命令 `git diff --stat --diff-filter=A HEAD~<n> -- . | grep -E '\.(py|sh)$'` **可证明是盲的**——`--stat` 的行尾是 `| N ++++` 且长路径被省略为 `.../name`,故该 grep 永远零命中,FR-033 / SC-011 / DoD-7 / `gate-neutrality` C-5 全部空真。验证代理在一个新增了 `scripts/python/validate-tasks.py` 的真实提交上做了对照(`--stat` 形式零输出 exit 1、`--name-only` 形式正确命中),并在 6 个提交 16 个真实新增 `.py` 上循环,`--stat` 命中数**恒为 0**;另指出 `HEAD~<n>` 是未落定占位符。已修:命令改为 `git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- . | grep -E '\.(py|sh)$' | grep -vE '^tests/contract/' | wc -l` 且断言输出为 0(**空结果与通过由此可区分**);`BASE` 由 T001 以 `BASE_SHA=<字面 SHA>` 记录;新增 **GATE-9** 承载该命令;GATE-4 的路径集补 `.specify/scripts/`(而 `shared/` 与 `skills/` 是本特性合法改动面,故**不纳入** GATE-4,全仓探测由 GATE-9 承担)。
- 订正(**G-5,MEDIUM**):`gate-neutrality` C-1(c) 要求一条"两块新宪章原则零 `BLOCKING_RE` 命中"的测试,但 `constitution-export` 的 12 条里没有它、T023 的撰写范围也不含 ⇒ 该子条只剩撰写约束加扫描器 `total` 的**间接**探测;而 `constitution-template.md` 的 governance-path 归类**不豁免于 `total` 计数**,间接探测只能给出 +1 而无法定位是哪一块原则哪一行。已新增 `constitution-export` **C-13**,并纳入 T023 的撰写范围、T024 的 red-first 期望与 T032 的转绿清单。
- 订正(**T-2,MEDIUM**):`gate-neutrality.md` 开头笼统声明 C-2/C-3/C-5/C-6/C-7"由 `test_user_facing_comprehension_doc.py` 承载",而 T003(该文件唯一的撰写任务)的范围只列 `discipline-doc` C-1…C-16 ⇒ 这 5 条只剩手工 shell 核验、**不进 CI**;且经核实没有任何既有测试钉住 `POLICY_DOCS` / `SELF_REL` 字面量。已把该行改为**逐条归属表**(C-1a/C-1b/C-1c 分别归三个测试文件;C-2/C-3/C-5/C-6 归纪律文档测试;C-4 明标为撰写指引不设断言;C-7 由既有套件经 T057 与 GATE-1 承担),并在 T003 与 T012 的范围里显式点名这 4 条。
- 订正(**T-3,MEDIUM**):`feature-ref.md` 称 FR-036 的观察节"由 `discipline-doc` C-6 钉死该节存在",但 C-6 的七节封闭元组内**并无观察节**(V1.3 也没有)⇒ T006 写的"观察节含 STR-005 标记约定"背后没有任何断言。已新增 `discipline-doc` **C-17**(断言观察约定存在 + STR-005 字面量 + 三条红线;载体形态不限,故不与 C-6 的七节元组冲突),并把 `data-model.md` E1 增 `observation_convention` 字段、`feature-ref.md` 的 FR-036 行改指 C-17、"未由契约覆盖的 FR"由 2 条减为 1 条。
- 订正(**F-1,MEDIUM**):`contracts/ambient-section.md` 的编号同批清单把 `generate-instructions.sh` 排在 `sync-mirrors.py --write` **之前**,与它自己的收尾句相反;而 `generate-instructions.sh:22` 的 `TEMPLATE_FILE` 指向 `.specify/templates/instructions-template.md`,即它读的是**镜像**⇒ 编号清单是错的那一个(`tasks.md` 的 T008→T009 是对的)。已把该清单重排为 1 编辑 → 2 同步镜像 → 3 再生指令 → 4 symlink 核验,并把理由内联进列表引言,删去与之矛盾的收尾句。
- 订正(**F-2,MEDIUM**):GATE-1 与 T057 的 `comm -13` 管线只在本地偶然可用——pytest 在 `running_on_ci()`(检查 `CI` / `BUILD_NUMBER`)为真时给每条 FAILED 行追加 ` - <crash message>`,而 `baseline-failed.txt` 存的是裸 node ID,缺处理会使 24 条基线全部失配、报出 24 条假"新增失败";本地因每个 node ID ≥88 字符(非 tty 下 `fullwidth=80`)恰好抑制了该后缀。已在两处的 `sed` 中加入 `s/ - .*$//` 并把该陷阱成文。
- 顺带订正(**T-1,LOW**,因与 G-1 同处一句):T012 称 `discipline-doc` C-10 的"完整绿点归 **T052**",但 T052 只跑 pointers 测试;真正复绿它的是 **T054**。已改为 T054,并在 T054 显式声明它是 C-10 的完整绿点。验证代理同时否证了原报的"不可满足"半边:C-10 只断言黑名单节**指明**实例来源,而 T006 在撰写时就写了这句指名 ⇒ C-10 在 T012 时点即为绿,提升后的**内容**由成对条款 `surface-pointers` C-11 守护,而 C-11 在 T052 的清单里。
- **契约条款计数随之变更**:60 → **62**(`discipline-doc` 16→17、`constitution-export` 12→13)。已同批订正 `plan.md` 的 Phase 1 摘要与落盘后核验段、`feature-ref.md` 的守卫圈行、`tasks.md` 的 Prerequisites 行、`data-model.md` E8 的基数行,并把 `plan.md` 的核验段标注为 2026-09-18 **重新核验**(不假装首次核验就得到了这些数字)。
- **本批未修**:其余 33 条(25 MEDIUM + 8 LOW)留待后续批次,其中 I-05(上游质量清单的九项计数过期,根因是 `clarify-taxonomy.md` 的 Mode A 集成规则无一触及 `checklists/`,属**机制缺口**且在 `041` 有同型证据)建议按 Principle XI 修机制侧而非逐个 spec 手工刷新。

### Session 2026-09-18(第五轮 — `/speckit.analyze` 复跑发现项的修复:第二批)

本轮**无新增用户提问**;以下是只读复跑(3 个检测代理 + 13 个验证代理,全部 fresh-context,检测与验证集合互不相交)产出 56 条发现、去重为 50 条后,经用户指示落地的**第二批修复**(4 条机械项 + 发现项 C-01 的 Principle XIV 修复)。验证波裁定:4 confirm / 9 downgrade / 0 reject,**降级率 69%**——每一次降级都落在检测代理未核的传播面事实上,该观测本身已记入本轮 feedback 的优化点。

> **编号消歧(本轮必需)**:下文 `A-*`/`B-*`/`C-*`/`V-*` 是 `/speckit.analyze` **复跑报告的发现项编号**,按检测代理的作用域字母编(A = 规格↔计划↔研究↔quickstart,B = 计划↔契约↔数据模型↔任务,C = Feature 链接↔注册表↔宪章),**与 `contracts/` 的条款编号 `C-N` 无关**。二者在本轮首次同形冲突(第四轮用的发现项前缀是 I-/G-/T-/F-,不与条款号相撞)。实测冲突范围**比看上去窄、但确实存在**:条款编号一律**不补零**(`C-1`…`C-17`,五份契约中 `grep -oE '\bC-0[0-9]\b'` 零命中),故补零的发现项 `C-01`/`C-09` 不与任何条款同形;但 **`C-11` 与 `C-12` 本身就是真条款号**(`ambient-section.md` 有 C-11,`discipline-doc.md` 与 `surface-pointers.md` 各有 C-12),同形歧义成立。故本块凡引用 **`C-*` 系列**发现项一律写作「发现项 C-NN」形态;`A-*`/`B-*`/`V-*` 不与任何既有编号空间相撞,可裸引。这是本轮发现项 A-15 所报缺陷(裸条款号在同一制品集内有多个不同指称)的同型实例,由修复批次自身引入,故在此显式消歧而不留待下轮。

- 订正(**B-01**,原报 HIGH、验证裁定 downgrade 至 MEDIUM):T056 的核验命令写作 `grep -E '\.(py\|sh)$'`——**ERE 内的转义竖线匹配字面量 `.py|sh`**,故该计数恒为 0、该任务恒"通过"。验证代理实测:合成名单上未转义形式命中 3、转义形式命中 0;在契约自身引用的真实提交上为 13 vs 0。同一行 169 字符之后就是正确形态。**该缺陷是第四轮 G-4 修复时由本代理亲手输入的**,已删去反斜杠。GATE-9 与 `gate-neutrality.md` C-5 的形态本就正确,故该义务此前仍有兜底。
- 订正(**B-15**):DoD-1 要求与 `discipline-doc.md` `C-1…C-16` 相符,而该文件有 17 条——按现文可在缺 C-17 的情况下宣告完成。**修法不是把 16 改成 17**(那只是再修正一次副本),而是改为引用:"与该文件的**全部条款**相符,编号以该文件头部声明为准,MUST NOT 在本行枚举区间"。
- 订正(**B-16**):`## Parallel Example: User Story 1` 的派发片段复述 T003 的范围且写作 `C-1…C-16`,同时漏掉 T003 额外承载的 `gate-neutrality` 四条——而该块是多代理派发的**字面文本**,按它派发的代理会写出缺 5 条的测试文件。已改为"范围见 T003 行",不再复述(复述即副本)。
- 订正(**B-17**):T055 要求确认 `POLICY_DOCS` 仍为 `['…reconcile-pattern.md', '…interview-pattern.md']`,但**实测值是 `PosixPath` 元组**,与字符串列表 `==` 恒为假 ⇒ 该 gate-neutrality FINAL 复核按现文不可能通过;同一错误形态若被 T003 抄进 CI 断言,该测试会恒红或被"修好"成空断言。已改为内容形态 `tuple(str(p) for p in POLICY_DOCS) == (…)` 与 `str(SELF_REL) == …`,并把类型陷阱成文。
- 订正(**发现项 C-01**,CRITICAL;验证裁定 confirm,证据边界收窄):条款总数是**可机械计数**的数(`grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md`),却被手写在 6 处非豁免位置且已漂移——`features/051.md` 的 Status Tracking 行(标 `(current)`,即 `Planned` 状态的现行 DoD)仍写第四轮之前的旧值。违反 Principle XIV(`constitution.md:156` 明列"a count")与 `one-source-of-truth.md:49`;而第四轮的修法是**把数字改正**到 4 个文件里,正是 `:51` 明令禁止的方向("remove the copy; do not correct the number")。**本批按 `:51` 修**:6 处手写总数**全部删除并改为引用**(`plan.md` 的 Phase 1 摘要两行、`tasks.md` 的 Prerequisites、`feature-ref.md` 的守卫圈行、`data-model.md` E8 基数、`features/051.md` 的 Planned 行),派生方式只在 `plan.md` 摘要行声明一次;`plan.md:158` 的核验段保留为**日期化记录**并显式声明 MUST NOT 当作当前真源引用(`one-source-of-truth.md:39` 第三个合法副本条件)。同时给 `gate-neutrality.md` 补上缺失的条款编号头部声明,使"每份文件拥有自己的编号区间"对 5 份全部成立。**验证代理另指出:被报的 60/62 分歧有一半是豁免的日期化记录**(`features.md:60` 的 3 处、`features/051.md:29` 与 `:46`),本批**未动**它们——真正的活体分歧只有 1 处;`plan.md:61` 的 XIV 行所引证据(传播足迹收敛)经复核**为真**,故该行是不完整而非被自身引证否证。
- 顺带订正(**发现项 C-12**,LOW):`plan.md:50` 的 Principle III 行引"clarify **三轮** session 块",第四轮后即过期。按发现项 C-12 的建议**删去计数、改为按路径引用** `## Clarifications`——否则本批新增的第五轮会第二次使其过期。
- **本批未修**:其余 44 条,其中 A-02/B-05(HIGH,"覆盖全部 11 份 guideline"实测只能遍历到 7/8 份)、A-03(HIGH,quickstart 场景 6e 的 grep 因目标字面量跨行而恒零命中,是 T049 的唯一核验且其输出会被 T059 写入 `verification.md`)、B-08(HIGH,SC-018 无任何条款度量却会被 T059 记为 `pass`)三条 HIGH 待下一批;**V-01**(T050 的裸 `sync-mirrors.py --write` 会把 `skills/draw-diagram/` 的在途改动吸收进本特性的提交,从而"以错误理由转绿"五个门禁,正是 `049/tasks.md:284` 同词禁止的动作)由验证代理建议单列,亦待下一批;**发现项 C-09**(质量清单机制缺口)经验证代理复核为"方向正确但三点不完整",应按 Principle XI 修机制侧;**发现项 C-11** 的建议本身会把代码拥有的事实复制成散文,应改为指针。

### Session 2026-09-18(第六轮 — `/speckit.analyze` 复跑发现项的修复:第三批)

本轮**无新增用户提问**;以下是经用户指示"Fix A-02, A-03, B-08 and V-01"落地的**第三批修复**(3 条 HIGH + 1 条 MEDIUM)。编号沿用第五轮的消歧规则:`A-*`/`B-*`/`V-*` 为复跑报告的发现项编号,与契约条款 `C-N` 无关。

- 订正(**发现项 A-02 / B-05**,HIGH;验证裁定 confirm):多处断言悬空指针守卫"覆盖既有 **11 份** guideline",而遍历只能抵达**有指针**者。实测:`ls -1 shared/guidelines/*.md` = 11 份;`templates/instructions-template.md` 命中 **7** 份、`.specify/instructions.md` 命中 **8** 份(两面本身就不一致,后者多出 `better-harness.md`);`checklist-methodology.md`、`requirements-guidelines.md`、`self-improvement.md` 三份**两面无指针**。quickstart 场景 2 的命令实跑输出 **8 行 `ok`、0 行 `MISSING`**,原文"对既有 11 份全部 ok"为假。已修:`ambient-section` **C-11** 拆为主条 + **C-11(a)**(实测分母)+ **C-11(b)**(**余集断言**——从 `shared/guidelines/*.md` 派生全集、减去被指向集,断言余集 **⊆** 那三份具名者),并把遍历面定为**两个指令面**;T004 与 C-11 对齐;`plan.md`、SC-017 的基线与 Source、`feature-ref.md` 的 SC-017 行、quickstart 场景 2 全部改为实测值。**取子集而非相等语义**是有意的:删指针即失败(覆盖率不能静默缩小),日后为这 3 份补指针则不误报。于是"覆盖全部 11 份"的**用户意图以可实现的形式成立**——8 份经指针存在性、3 份经具名余集。
- 订正(**发现项 A-03**,HIGH;验证裁定 confirm):quickstart 场景 6e 的 `grep -c 'never the raw engine path' docs/reference/skills/feedback.md` **恒为 0**——该字面量在目标文件里跨行断开(`:141` 行尾 `…(never the raw`、`:142` 行首 `engine path);`),而其期望是"计数下降",故 0→0 永不可满足,是**可证明的盲探针**(与 T056 曾有的 `--stat` 盲命令同类)。已改用完整落在 `:141` 单行内的片段 `never the raw`(实测 **1**),并把四条命令的**改前基线写成具体数字 2 / 1 / 1 / 0**——原文"具体值由实现期测定"使执行者手里没有"改前"值,于是一个 0 会被读成"已收敛"而记为通过;盲探针之所以危险,正因为它与"成功收敛到 0"不可区分。跨行形态若确需匹配,附 `python3 -c` 配 `never\s+the\s+raw\s+engine\s+path`(实测 1)。
- 订正(**发现项 B-08**,HIGH;验证裁定 confirm):SC-018("读者基准总数 ≤3")被映射到 `discipline-doc` C-13/C-14,而 C-13 只断言真源文档内"全局基准恰好 1 条"、C-14 只断言 11 行表的行数/类名/去重路径数,**两者都不做跨框架计数**;`data-model.md` 的 V1.1…V1.6 亦无一条断言 E6 的 `override_sites` 字段 ⇒ SC-018 无条款度量,却会被 T059 记为 `pass`(GATE-7 只数行数不读内容)。已新增 `discipline-doc` **C-18**:(a) **计数口径 = 登记项而非模式命中数**——断言 11 行表 `reader_baseline_override` 列非空条目 **≤2**(按类计),与 C-13 的"全局恰好 1"合并即 ≤3;**MUST NOT 用裸模式计数**,因实测 `外部读者` 仅在 `skills/summarize-project/` 的 9 个文件里就作散文出现 **17** 次;(b) **完备性针扫**——以 `Written for [^.]*stakeholders` 与 `外部读者不读代码也能看懂` 两个**声明形态**正则扫 `shared/`+`templates/`+`skills/`,实测命中 **4 处 / 3 文件、零散文误报**,断言命中集 ⊆ 已登记站点**且**每处命中都落在其所属类的规则真源文件内;(c) 第 4 处的处置。同步修:`feature-ref.md` 的 FR-037 与 SC-018 两行(C-14 的错误归属已去掉——`discipline-doc.md` 自己的映射表就把 C-14 归给 SC-004)、`data-model.md` V1.5 纳入 `override_sites`、T003/T012/T054 的范围改为 **C-1…C-18**、T043 承担类 ⑦ 的覆盖登记。
- **实测发现 `research.md` D-14 从未登记的第 4 处读者基准**:`templates/commands/requirements.md:82`(`Written for business stakeholders`),是类 ⑦ 的**命令侧孪生**。按 D-3"类 ⑦ 唯一真源是 `requirements-guidelines.md`",它是**复述**而非第二个覆盖站点,故 C-18(c) 要求同批收敛为指针(T043 承担)。**这引入了本特性此前没有的改动面**,已同批补齐其镜像义务:`plan.md` 的源码树清单与 Mirror Obligations 表各加一行、T050 的再生清单加 `requirements.md`。
- **待用户裁定(本轮不替规格作选择)**:SC-018 写"至多 **2 处**类级覆盖",而"处"可读作**类**或**行**。C-18(a) 取**按类计**;但类 ⑦ 的真源今天在 `:24`(检查清单项)与 `:101`(散文规则)各表述一次,按类计为 1 处、按行计为 2 处。**若采按行口径**,则 1 全局 + 3 行 = 4 > 3,SC-018 需改为 ≤4 或要求把 `:24`/`:101` 合并为一处。该口径与其代价已写进 C-18 的引注,裁定权归本行。
- 订正(**发现项 V-01**,MEDIUM;由验证代理建议自 B-03 拆出):T050 原写**裸** `sync-mirrors.py --write`,会把本特性**未触及**的在途漂移(实测 `skills/draw-diagram/` 的 1 DIFF + 1 MISS)一并吸收进镜像,从而让 GATE-2 / DoD-8 / T010 / T029 / T051 五个门禁**以错误理由转绿**——把别人的在途工作并入本特性的提交,正是 `049` 的 tasks 同词禁止的动作。已改为 `--write --only shared --only templates --only skills/summarize-project`(实测该范围 `--check` **EXIT=0**,而全树 `--check` 为 EXIT=2),并把理由与 T008/T019/T029/T037 均已范围化的事实写进行内。**注意本修使门禁"诚实地红"而非"虚假地绿"**:全树绝对判据本身的问题(发现项 B-03)仍开放。
- 顺带订正:T051 原以 **Mirror Obligations 表行号**枚举所覆盖的镜像对(第 3/4/5/7、10/11、13 行),而本批新增一行会使行号静默错位——与 DoD-1/派发片段曾有的 `C-1…C-16` 同类缺陷。已改为**按文件名**枚举,并把其 `--check` 范围与 T050 对齐。
- **契约条款计数随之变更**:62 → **63**(`discipline-doc` 17→18)。**本次无需修改任何计数**——第五轮按 `one-source-of-truth.md:51` 把 6 处手写总数删除改为引用后,总数已由 `grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` 派生;这是该修复的第一次实测收益(第四轮同类变更需同批改 4 个文件)。
- **本批未修**:其余 40 条。其中 **B-03**(全树镜像绝对判据无既有状况护栏,GATE-2/DoD-8/T010/T029 仍会被无关漂移拖红)、**B-02**(零改动面用 `git diff --stat HEAD`,对已提交改动盲,且在 CI 洁净检出下**恒真空过**;实测还有 T011/T033 两处未报的同类)、**B-04**(C-7 要求开工前重冻基线却无任务承担,而 049/050 的同一惯例都由 T001 承担)、**B-06/B-07/B-09/B-12/B-14/B-18** 等 MEDIUM,以及 **C-09/C-11** 两条应按 Principle XI 修机制侧的项。三条环境性失败(`skills/draw-diagram/` 在途改动所致)不属本特性。

### Session 2026-09-18(第七轮 — `/speckit.analyze` 复跑发现项的修复:第四批)

本轮**无新增用户提问**;以下是经用户指示"Fix B-02, B-03 and B-04"落地的**第四批修复**(3 条 MEDIUM,均由验证代理自 HIGH 降级)。三条发现共享同一根因——**门禁比对的基线选错了**——故按一个整体修:把 **T001 变成本特性所有比对型门禁的唯一基线冻结点**(承 049/050 惯例,二者都由各自 T001 承担),其余各行一律引用它冻结的产物,而不再用 `HEAD` 或绝对判据。

- 订正(**发现项 B-02**):零改动面用 `git diff --stat HEAD -- <路径>` 断言,对**已提交**的改动不可见(提交纪律要求逐任务提交),且**在 CI 里无条件空真**——洁净检出下工作树恒等于 HEAD,该断言永远通过。**实测实例数比原报多 2 处**:GATE-4、T055(原报)+ T011、T033(漏报);T002 则**不是**缺陷(开工时 HEAD 即基线)。已修:① `gate-neutrality.md` C-6 补 **C-6(a)**(基线 MUST 是 T001 的 `BASE_SHA` 字面值,附 CI 空真的机理与实测对照)、**C-6(b)**(MUST NOT 按扩展名过滤:`templates/plan-template.md` 是 `.md`、`scripts/` 下另有 **70** 个非 `.py`/`.sh` 受跟踪文件,扩展名过滤使其结构性逃逸;并说明为何 MUST NOT 靠扩大 GATE-9 的过滤来补——那会让一个门承担两个命题且仍漏 `.md`)、**C-6(c)**(T002 是唯一合法的 `HEAD` 相对用法);② C-6 在归属表里的那行改为**命令级指令**,因 T003 会照它撰写 CI 断言;③ GATE-4 / T011 / T033 / T055 全部改为 `git diff --name-only --no-renames --diff-filter=ACMR "$BASE" … | wc -l` 且断言为 `0`(T055 原写"与 T002 的起点比对"却从未读取 T002 的记录,而 T002 记录的就是空值,等于空比空)。**已实测新形态非空真**:取一个早于 `scripts/` 真实改动的 `BASE`(`111e151b~1`),新形态报 **7** 个文件,而旧形态 `git diff --stat HEAD` 报 **0**——正是 B-02 所指的盲。
- 订正(**发现项 B-03**):`plan.md` 依"改前基线实测 EXIT=0"采用**全树绝对判据**并显式拒绝 `--only` 范围化,而该前提已被本特性**未触及**的 `skills/draw-diagram/` 在途改动推翻(全树现 **EXIT=2**,触及范围仍 **EXIT=0**)。已把 DoD-8 / GATE-2 / T010 / T029 的判据改为 **049 先例形态**:"所触及镜像对报 `ok` + 全树相对 T001 冻结集**无新增 `MISS`/`DIFF` 行**";`regen-command-copies.py --check` 今天仍干净,故**保留**绝对判据。GATE-2 因此拆为三段(触及对 EXIT=0 / regen EXIT=0 / 无新增漂移行)。**归因订正**:原文写"无需 **050** 那样的 `--only` workaround"归属错误——范围化是 **049** 的 workaround,**050** 恰是退役它的那个特性。另澄清 `research.md` **D-15 只覆盖 pytest 基线、不覆盖镜像基线**,故镜像侧重冻义务由 `plan.md` 该段与 T001 共同承载。**已实测**:GATE-2 三段今天全部通过(① ② EXIT=0;③ 冻结集与当前集相同 ⇒ `comm -13` 为空),并跑了**负对照**(从冻结集删掉一行 ⇒ ③ 立即报出该行),证明它不是恒空。
- 订正(**发现项 B-04**):C-7 明令"开工前 MUST 重新冻结 `baseline-failed.txt`"却**无任务承担**,而 049/050 的同一惯例都由各自 T001 承担。已修:① **T001 重写为四组冻结**(`BASE_SHA` / 重冻 `baseline-failed.txt` / 冻结既有镜像漂移集到 `MIRROR_DRIFT_PREEXISTING_BEGIN/END` 标记之间 / 其余结构实测值),并明写"本行列出的数字只是快照,**所有写入值 MUST 取自开工当时实跑**,不符则以实跑为准并记录差异";② C-7 补上**执行者是 T001**,并说明冻结集不得沿用既有那份(实测那条自愈项已转通过、另有在途漂移导致的失败须一并纳入);③ **去钉死**:T001 的"24 failed / 1924 passed"(今天实为 26 / 1972)、DoD-10 的"(24 条)"、T057 的"当前失败数预期为 **23**"、GATE-1 与 T057 的"24 条基线"全部改为不写数字(判据只有"`comm -13` 输出为空"),承 050 自己记录的"不硬编码字面量"教训;④ § Environment Prerequisites 新增**两条**探测结论(镜像既有漂移、套件既有失败集),各附探测命令、日期、归因证据与受影响任务——该节自称"探测结论的唯一落点",此前对这两项无记录。
- 顺带订正:`## Notes` 的**提交纪律**行仍写"否则全树 `sync-mirrors.py --check` 门禁会红",引用的是本轮已删除的判据,已改为指向 GATE-2 的新形态,并把"逐任务提交"与"MUST 用 `BASE_SHA` 而非 `HEAD`"点明为**同一件事的两面**;T010 / T029 原以 **Mirror Obligations 表行号**枚举所覆盖的行,新增表行会使其静默错位,已改为**按文件名**(与上一批 T051 同类缺陷、同种修法)。
- **与上一批 V-01 的合流**:V-01 使 T050 的 WRITE 不再吸收无关在途改动(不再"以错误理由转绿"),本轮 B-03 使 VERIFY 侧的判据也不再被无关状态拖红。两者合起来把该门禁从"要么污染、要么阻塞"变为"在触及对上诚实地通过"。实测三者的组合今天成立:T050 的范围化 `--write` 前缀与 GATE-2 ① 的 `--check` 前缀一致,均 EXIT=0。
- **契约条款计数不变**(仍 **63**):C-6(a)/(b)/(c) 与 C-11(a)/(b) 是既有条款的子断言,其行首形态不匹配计数正则 `^\*\*C-[0-9]+\*\*`(已实测各文件计数未变)。
- **本批未修**:其余 37 条,含 B-06(`confirmation-gates.md:68` 无条款守护,落在 C-4 冻结区与 C-2 禁区之外的盲点)、B-07(FR-030 的项目中立性在两个宪章侧面上无任何条款)、B-09(DoD-3 的 `逐字未动` 覆盖 `feedback-step.md:115`,而 C-10/T036 要求改写它;根因是 FR-019 的 `:113-114` 被 5 处下游放宽成 `:113-115`)、B-12(red-first 取证行把若干**改前即绿**的条款写成"因制品未改而失败")、B-14、B-18,以及 C-09/C-11 两条应按 Principle XI 修机制侧的项。三条环境性失败(`skills/draw-diagram/` 在途改动所致)不属本特性。

### Session 2026-09-18(第八轮 — `/speckit.implement` 开工前的阻塞项清理)

本轮**无新增用户提问**;以下是 `/speckit.implement` 启动时,经用户裁定"先清 B-09/B-10/B-12 再开工"而落地的**上游修正批**。三条都是 MEDIUM,但都**正落在具体任务的执行路径上**,若不先清会产出错误制品或在执行期报假警。裁定依据是 analyze 的 Handoffs 规则与 implement step 5"被证伪的前提 MUST 回写上游而非静默绕过"。

- 订正(**发现项 B-10**,真矛盾,阻塞 T014):`surface-pointers` C-12 一面要求 `shared/`+`skills/` 下"独立黑名单副本数 MUST 为 0",一面要求 `reporting-playbook.md:309` 的落盘门禁"MUST **保留**",而 `:309` **字面枚举了七类内部标识**(`T1`–`T5` / `E1`–`E5` / `RC-*` / `CG-*` / `§编号` / `M-*` / 脚本名)⇒ 两句不可同时满足;而 C-13 的判定针又含"黑名单条件",于是同一行被两条条款以**相反方向**指认,撰写 T014 时无规则可依。已补三条子条:**C-12(a)** 裁定区分规则——**判据是"是否枚举",不是"用途为何"**:一处文本 MAY 为落盘检查而**指称**黑名单,MUST NOT **复述其类别枚举**;故 `:309` 保留清单项本身(勾选框、`§1.7` 引用、"无内部标识渗入"断言与"只出现在 `## 元信息`"限定),把括号内七类枚举替换为指称(`:51` 不含枚举,原样合规)。**C-12(b)** 规定该指称 MUST **不含仓库路径**——否则与 C-1 的"每文件含且仅含一行指针"冲突,在 T052 汇聚点转红而 C-12 又禁止删 `:309`,形成第二个不可满足对(这同时是发现项 **B-11** 的修法)。**C-12(c)** 给出机械判定形态并要求该针**可证伪**(`:309` 改写前为 1、改写后为 0),T014 MUST 在 red-first 取证里记录改写前的命中数以证明针有效。
- 订正(**发现项 B-12**,会在执行期报假警,阻塞 T016/T024/T040 的判据):三行 red-first 取证把**改前即绿**的条款列为"因制品未改而失败",而这三行的判据恰是"确认失败原因是制品未改**而非断言写错**"⇒ 执行者遇到绿的条款会据此**削弱一个正确的断言**。已按 **T035 的正确形态**改写(只列真红的子义务,并显式列出改前即绿者及其理由):**T016** 真红 = C-2 与 T015 新断言;改前即绿 = **C-4**(冻结断言,改前本就未改写)、**C-5**(两侧改前即成立)。**T024** 真红 = C-1…C-7、C-9、C-11…C-13;不为红 = **C-8**(关于测试自身匹配逻辑的设计规则,T023 写对即绿)、**C-10**(变异式抽查,其前提是 C-7 已绿;改前 STR-006 两侧皆缺,故属**改前不可测**而非"因制品未改而失败")。**T040** 真红 = C-1、C-6、C-8、C-9、C-11…C-13;改前即绿 = **C-3**(本行在 T041…T049 之前运行,源侧尚未改动)、**C-7**(冻结断言)、**C-14**(实测今天 `--check` 即 EXIT=0)。
- 订正(**发现项 B-09**,不可满足对,阻塞 DoD-3 收尾):DoD-3 要求 `feedback-step.md` 的 `:89-90`/`:113-115`/`:141` **逐字未动**,而 C-10/T036 要求把 `:115` 的并存措辞收敛权威**上移**——二者互斥。**根因是范围漂移**:需求侧真源 **FR-019 写的是 `:113-114`**,而 **7 处**下游把它放宽成 `:113-115`。已实测确认 FR-019 正确:`:113-114` 才是完整的一句措辞规则("Present the choices in user-facing terms: … never the raw `feedback-utils.py` engine path."),`:115` 是其后的**独立括注**("(Embedded copies … defer to this section):")。已按 FR-019 把 7 处全部收窄为 `:113-114`,并在 C-10 显式声明"本条含一个**保留**义务与一个**改写**义务,作用于**不相交**的行":C-10、DoD-3、T036、US4 的 Independent Test、`plan.md` 的 Mirror Obligations 行、`data-model.md` V3.4、`research.md` D-3 的类 ③ 行。**未走 void 逃生阀**——`feature-integration.md:48-51` 的 `green-with-void` 虽可用,但根因是可修的范围漂移,修对优于记为 void。
- 顺带订正(**发现项 B-11**,系 B-10 修法的直接后果):C-1 限定 8 个文件**各含且仅含一行**路径指针,而 T041 对 `interview-pattern.md` 做三处编辑、T046 对 `reporting-playbook.md` 做两处,二者原**均未声明该上限**(而 T017/T036/T043/T048 都写了"一行")。已把上限与"不含路径的指称"要求写进 T041 与 T046 两行。
- **`/speckit.implement` step 2 的门禁状况(如实记录)**:`checklists/requirements.md` 为 **16/16 `[x]`**,故该命令按"全部完成即自动放行"放行本轮。但该 16/16 是**基于过期证据**——发现项 C-05/C-06 已实测其 12 项断言计数中 **7 项**与当前规格不符(声称 FR 36 / SC 16 / SC Source 16 / Edge 14 / OoS 13 / Assum 14 / 主题组 7;实为 38 / 18 / 18 / 15 / 14 / 16 / 8),且 **SC-017 与 SC-018 从未被任何清单项评估过**。放行的**依据不是该清单**,而是规格已经过四次 `/speckit.analyze`(CRITICAL 与 HIGH 全部已修)。C-05/C-06 的根因是机制缺口(C-09:`clarify-taxonomy.md` 的 Mode A 集成规则无一触及 `checklists/`),应按 Principle XI 修机制侧,不在本轮逐个刷新。
- **本轮范围裁定(用户)**:MVP = **Phase 1 Setup(2)+ US1(11)= 13 个任务**,依 `tasks.md` 的 MVP 规则(US1 的 checkpoint 单独即可独立测试且有独立价值)。US2–US5 留下一轮。**已知 US3 会触发 `.specify/gate.yaml` 的 CONFIRM**(`.specify/memory/constitution.md` 在 `confirm` 清单内,实测 `gate-check.py` 对其返回 EXIT=1),本轮范围不含它;Phase 1 / US1 / US2 / US5 的计划写入路径实测均为 **allow(EXIT=0)**。

## Out of Scope

- **门控"是否触发"的判据改写**——两级判据、破坏性动作清单、治理保留清单、存疑从严、回流约束全部保持 `confirmation-gates.md` 为唯一权威;本特性只新增"门控如何措辞"(FR-017)。
- **任何新的行话检测运行时机制**——行话 lint 引擎、措辞评分器、成熟度报告、跟踪台账、可读性打分流水线,一律排除(FR-033;框架范围纪律 / 不新增机制)。执行手段限于既有契约测试与既有扫描器的豁免登记。
- **`scan-confirmation-gates.py` 的措辞检查扩展**——扫描器保持只检测阻塞行为;本特性至多在其 `POLICY_DOCS` 豁免集登记新真源文档(FR-032),MUST NOT 给它新增措辞模式。
- **投递机制本身的修复**——`generate-instructions.sh` 不同步 `shared/` 是既有 11 份 guideline **共有的结构性缺口**(实测:该脚本全文无 `shared` 拷贝逻辑),修复它收益超出本特性且属另一条 Feature 的归属。051 只加**同批抵达 + 缺失显式提示**义务(FR-038),MUST NOT 改投递脚本。
- **Token 效率纪律的改写**——摘要优先/程序优先/升级阶梯/小文件阈值仍由 `token-efficiency.md` 独家拥有;本纪律只引用它来约束上下文上限(FR-010)。
- **确认门控既有分类与执行报告三要素定义的改写**——三要素(执行内容 / 产出·变更工件 / 修改途径)继续由 `confirmation-gates.md:56-60` 拥有,本纪律引用而不复述(FR-009)。
- **访谈模式的其他规则**——设计树/依赖 DAG、决策记录、隔离规划、frontier、`I0–I6` 循环、退出门、事实 vs 决策拆分、台账 schema、可恢复性:均不属本特性;"每问一决策""问 what 不问 whether"两条 MUST 原文保留(FR-021)。
- **澄清流程的既有形态裁定**——封闭式提问、选项表 + Recommended、不采纳开放式提问规则:保持不变(FR-020)。
- **机械副本的手工批改**(命中面实测计数见 Overview 现状锚点)——交由既有再生脚本(FR-023)。
- **`docs/` 文档空间的全量调谐**——本特性只收敛与本纪律直接相关的手写复述处;需要移动/归档级变更时,推荐运行 `/speckit.docs` 而非在此执行。
- **词汇表机制的改写**——入向校正与出向 canonical 措辞协议仍由 `shared/workflow/glossary.md` 拥有;本纪律只引用其"就地注解优先采用词汇表 canonical 措辞"这一衔接点。
- **主动触发机制的规则集、晋升态与遥测**——`proactive-trigger.md` 独家拥有;本纪律只引用其"单行 = 用途 + 确切调用形式"作为上下文上限的既有形态(FR-010)。
- **各 agent 的原生 hook / 运行时拦截**——本纪律是提示指令层的写作纪律,不是运行时强制;不建任何 agent 原生 hook。
- **面向用户消息的语言本地化/翻译机制**——纪律是语言无关的(注解用读者的语言),但本特性不引入任何翻译或多语言渲染机制。

## Assumptions

- **真源文档命名**: 采用 `user-facing-comprehension.md`([[STR-002]])。已执行预留标识符核查,该字串在仓库内零占用;`comprehension` 的既有使用(`interview-pattern.md:119` 的 `Comprehension rules (可理解性规则)`)是本纪律将收敛的对象而非冲突项。中文侧命名取"面向用户可理解性纪律",与既有 `可理解性规则` 词汇连续,不新造第二套词。
- **程度以"条件表 + 机械判据"表达,不以裸数值表达(已经用户裁定,clarify 2026-09-17 R2-Q3=A)**: 用户要求"设定好程度",但本纪律的对象是散文措辞而非数据量。房子的四种程度先例中,**条件表**(`one-source-of-truth.md:33-41`)与**粗体机械测试**(`:29`、`ask-record-repeat.md:97`)适配散文对象;**裸数值 + 覆盖协议**(`token-efficiency.md:38` 的 `≤100 行` 且 `≤10 KB`)适配可计量对象。故本纪律以白/黑名单条件集 + 下限/上限 + 可复现判据落地"程度",数值型长度约束**复用各类界面既有值**(如非阻塞建议的单行)而不另造(FR-007、FR-011、FR-013)。**该选型在 `/speckit.requirements` 阶段是未经询问的推断,已于第二轮澄清提交并获用户批准**;其已知代价(门控提示与收尾报告无长度界)按 FR-011 的知情接受条款成文,升级路径是在该类界面真源处声明覆盖值(FR-037 同型协议),而非回写真源文档新增全局数值。
- **读者基准取"全局一套 + 按类覆盖"(clarify 2026-09-17 R2-Q2=A)**: 全局基准读者为"未在本会话打开过本仓库、但具备该项目领域知识的人";界面类只在需要时于**其真源文档处**声明更严覆盖,声明处生效、不回写真源纪律文档(FR-037)。既知的两处覆盖是"面向干系人的需求/规划/任务工件"(不具备代码知识)与"面向外部读者的项目总结报告"(不读代码也能看懂)。该形状直接复用 `token-efficiency.md:38` 的房子先例,故不引入新机制。**未取的两个替代方案及其代价已记入 FR-037**:11 套各自定义会使真源退化为元规则并削弱 38 处措辞的收敛量;单一基准不允许覆盖则与白名单第 ①④ 条(用户先用的术语、用户领域术语)直接冲突。
- **投递窗口按"记录状况 + 加提示义务"处理(clarify 2026-09-17 R2-Q4=A)**: 常驻章节与真源文档投递路径实测不同步(前者经 `/speckit.instructions` 增量调谐,后者只经 `specify init` copytree 或 `sync-mirrors.py`;`generate-instructions.sh` 全文不同步 `shared/`)。051 只加同批抵达与缺失显式提示义务(FR-038),不修投递脚本——修它收益超出本特性且属另一条 Feature 的归属(见 Out of Scope)。该窗口是既有 11 份 guideline 共有的结构性状况,故 SC-017 的守卫 MUST 覆盖全部 guideline 而非只覆盖新文档。
- **暴露通道 MUST 为新增顶级章节**: 依 `proactive-trigger.md:3` 与 `generate-instructions.sh:73-78` 的实测语义,只往文档地图表加一行是**静默失效**(文件看着改了,已初始化项目收不到)。故 FR-003 把"新增顶级 `## ` 章节"写成硬约束而非风格偏好。
- **镜像无需注册**: `sync-mirrors.py` 按 `rglob("*")` 全量发现,`pyproject.toml:37` 与 `_CORE_SPECIFY_ASSETS` 均为目录级 ⇒ 新文件自动被拾取(FR-002)。`tests/contract/test_shared_reference_directory.py` 的 `TYPED_DOCS["guidelines"]` 是 `issubset` 断言,可选择性加入以钉死存在性。
- **同批加守卫**: 依 `ask-record-repeat.md:117`,新增表面 MUST 同批获得守卫,否则新增的是漂移点而非可达性。本特性正在新增第 39 处表面,故 FR-029..FR-032 与 FR-001..FR-003 属同一批、不可拆分交付。
- **接入广度已裁定(clarify 2026-09-17 R1-Q1=A)**: 11 类界面真源的指针接入 **与** 两处搁浅实现的收敛/提升同批完成,不留分批过渡态。理由:用户显式诉求为"扩散到**所有**面向用户的流程";分批会使 38 处措辞中的大部分在收敛完成前继续各自漂移;而把两处搬家隔离到另一次**并不会降低其回归面**,只会让收敛量长期停在中间态。⇒ 回归风险 MUST 由同批守卫(FR-029..FR-032、FR-035)与端到端实测(FR-026)承接,并以 SC-016 作为配套风险约束(既有行为回归数为 0)。
- **Principle XIV 回流已裁定(clarify 2026-09-17 R1-Q2=C)**: 研究中发现的同型既有缺陷(该原则从未回流到随包分发的模板,故无下游项目收到它)随本特性一并修复(FR-028),并用作双落点守卫的第一个受测样本(FR-035)。选择"当守卫样本"而非仅"修好"的依据:守卫本来就需要样本,边际成本近乎为零,而用一个**真实发生过**的缺口做样本能证明它拦得住同型失效,不只是拦得住"新原则忘了写"。回流后随包分发的宪章模板原则数 11 → 13,活动宪章原则数 14 → 15(活动宪章已含 XIV,故只新增一条)。
- **宪章编号**: `templates/constitution-template.md` 现有 11 条原则(I–XI)⇒ 本批新增两条(本纪律 + 回流的 One Source of Truth),位置在 XI(`:132-141`)之后、`## [SECTION_2_NAME]`(`:143`)之前;二者先后顺序由 `/speckit.plan` 定。本仓活动宪章 `.specify/memory/constitution.md` 现有 I–XIV ⇒ 对应新增原则为 **XV**。模板与活动宪章的编号不同属正常(模板是通用脚手架,活动宪章含本项目专有原则);守卫 MUST 按**原则名**匹配([[STR-003]] / [[STR-006]]),MUST NOT 钉死罗马数字字面量(FR-035)。
- **版本递增**: 新增原则 = MINOR(`templates/commands/constitution.md:66`);本仓宪章现为 `1.11.0` ⇒ 递增后为 `1.12.0`,并前置 Sync Impact Report(`:142-148`)。
- **下游 plan 门控自动传导成立但 MUST 验证**: `plan-template.md:37-42` 明写动态枚举、禁止硬编码原则名 ⇒ 逻辑上自动纳入。FR-026 要求实测验证而非假定,依据是既有教训"重构命令/引擎时 MUST 端到端执行其真实流水线——'文件存在/标题存在'式检查会漏掉只在运行时浮现的潜在缺陷"。
- **US4 排 P2 的依据**: 反馈流程是本纪律**今天执行得最好**的一片(`feedback-step.md` 拥有规则 + 跨表面传播足迹,实测计数见 Overview 现状锚点),其边际工作是命名归属与一般化,而非从零修复;相较之下 US2(门控措辞)是**零规则、零守卫、且直接决定不可撤销动作**,失效风险高一个量级。此为基于实测证据的排序判断,若用户认为反馈流程应同等优先,调整只影响实现顺序、不影响 FR 集合。
- **输入模态**: 本次为中文键入文本(非语音),glossary 校正协议已先行——用户输入中的 `jargon` / `context` / `feedback` / `constitution` / `shared/guidelines` 均为本仓既有 canonical 术语,无需校正;无同音/近形变体需提交确认。
- **落地层级**: 真源文档 + 常驻章节 + 宪章模板 + 宪章命令 MUST-include 条目随 `templates/` 与 `shared/` 分发,框架自身与下游采纳项目**同一机制同时受益**(init 即得);按工具副本经既有再生脚本处理;本仓活动宪章与活动指令文件的落地属客户端实例侧,同批完成。
- **术语提案(wrap-up 提交)**: 拟按 glossary 协议以 `origin=auto`、`status=proposed` 提交 "面向用户可理解性(User-Facing Comprehension)"、"许可行话 / 禁用行话"、"上下文下限 / 上下文上限"、"消费单元"、"面向用户界面类" 等新词条;需先做冲突检测——`可理解性规则` 已存在于 `interview-pattern.md`(非词汇表条目),`Comprehension` 一词在历史 spec 中作度量措辞使用,二者是否构成需用户确认的冲突由 wrap-up 的冲突检测判定。
