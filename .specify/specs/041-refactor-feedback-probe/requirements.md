# Requirements Specification: Feedback 机制的 Probe 化重构(反馈插点 + 切片定向 + 三模式管理命令 + 外部 probe)

**Requirement Branch**: `041-refactor-feedback-probe`  
**Created**: 2026-08-14  
**Status**: Draft  
**Input**: User description: "需要针对当前的 feedback 反馈机制做一次大的重构，当前反馈机制主要存在如下几个问题：

1. 所有的反馈都没有进行特定的系统切片的指定，也就是所有的反馈都是针对所有的系统，以全局视角去进行反馈。这种反馈带来的信息往往过于冗余，不容易进行特定的处理。
2. 这种反馈没有一个本地的管理接口。因为现在的反馈其实都是直接埋在流程中自动进行的，用户只能看到反馈信息，但没法在本地方便地对这些反馈进行处理。

需要单独提供一个 Feedback 命令去处理这些用户收集的反馈。最后最重要的一点，是为反馈定义一个新概念：Feedback Probe（反馈插点）。Feedback Probe 是将插入到当前 Spec Kit 框架流程中特定点的反馈进行显性、明确定义的工具。例如，一个 Probe 可用于收集特定信息，并插入到特定的执行流程中。

在项目层面，需要有一张完整的 Feedback Probe 结构图，以明确：当前系统中哪些位置插入了反馈点、这些反馈点用于收集什么信息、反馈数据收集后的处理流程。这些反馈点针对系统中的特定部分进行反馈。"

## Related Feature *(mandatory)*

**Feature ID**: 028  
**Feature Name**: Feedback Mechanism

## Overview

把反馈机制从「隐式埋点 + 全局视角自由文本」重构为「显式定义的 Feedback Probe(反馈插点)+ 切片定向 + 三模式本地管理接口 + 外部 probe 注入」。用户输入的问题对应解法:

| # | 现状问题 | 解法 |
|---|---------|------|
| 1 | 反馈无系统切片归属,一律单元运行整体自评,信息冗余、无法定向处理 | Feedback Probe 以 **Class/Object 两层**显式建模,条目经 Object→Class 继承**目标系统切片**归属 |
| 2 | 反馈埋在流程里自动产生,用户看得见、没法在本地处置 | `/speckit.feedback` 提供**三种执行模式**:probe 总览(无参数)/ 处理已收集反馈(含打包后清理)/ 注入反馈点 |
| 3 | 反馈点散落在各模板文本里,无系统性结构 | 项目级 **Feedback Probe 结构图**:从 probe 真源派生,按 Class→Object 层级完整回答「哪里插点/收集什么/数据去向」三问 |
| 4 | 反馈点只覆盖框架自身流程;宿主项目自定义 Skill/Agent/Command 无反馈能力 | **外部 probe(External Probe)**:经模式三注入,面向宿主项目自定义单元;其反馈保留在宿主项目内、与框架自身反馈分开处理、绝不上送 Spec Kit(Loop B 语义) |

**Probe 两层建模**:Feedback Probe 采用 Class/Object 两层形态——**Probe Class(插点类)**定义一类插点的特征(收集内容、目标系统切片、收集后处理流程、适用的插入位置类型),**Probe Object(插点实例)**是 Class 在当前系统中的实例化表现(绑定具体流程单元 × 生命周期点)。既有 49 个隐式埋点全部重构为 Object 并归类到具体 Class 之下。该建模与项目既有 Agent 分类法(Template/Instance)同构:Class 承载特征,Object 承载落点。

**内外类别维度**:每个 Probe Class 另携带**类别(internal/external)**——**内部 probe** 目标为 Spec Kit 框架自身(既有 49 个插点全部属内部);**外部 probe** 目标为宿主项目自定义的 Skill/Agent/Command 等单元,经 `/speckit.feedback` 模式三注入,其反馈保留在宿主项目内用于项目自身优化,与内部反馈分开处理、不上送框架。

### 现状锚点(以源码实测为准)

- **触发与嵌入**:全部 skills(`skills/*/SKILL.md` 实测 31 处)与 18/22 个命令模板(`templates/commands/*.md` 实测;简单命令 agents/constitution/feature/team 不嵌)在 wrap-up 阶段嵌入 canonical `## Feedback` 步骤,真源为 `.specify/shared/workflow/feedback-step.md`。
- **引擎**:`feedback-utils.py`(工具记录 `<TOOL:.specify/memory/tools/feedback-utils.py.md>`,Verified)提供 record / status / list / mark-submitted / reindex / package / upstream 七个动作。
- **存储**:`.specify/memory/feedback/`,Markdown 条目 + `index.json`;条目以 `(unit_id, run_id)` 去重,`scope: local`,正文为自由文本 `## Review` + `## Optimization Points`。
- **流转**:阈值默认 10 条触发合并提交提示 → package 打 zip → 用户**手动**投递 → mark-submitted 本地归档复位;intake 侧为框架仓库根 `feedback/` 目录。
- **痛点确认**:(1) 条目内容是对该单元整次运行的全局自评,无系统部位归属,消费侧无法按切片定向处理;(2) 无用户管理接口,处置只能翻文件或手工调引擎脚本;(3) 反馈点本身没有显式定义,「系统里有哪些反馈点、各收集什么」只能人工通读模板归纳。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 反馈点成为显式建模的 Feedback Probe(Class/Object 两层) (Priority: P1)

作为框架维护者,我希望每一个反馈插入点都是显式定义的 Feedback Probe——**Probe Class** 定义一类插点的特征(收集什么信息、目标系统切片、收集后处理流程、适用的插入位置类型),**Probe Object** 是 Class 在系统中的实例化(绑定具体流程单元与其生命周期点)——而不是散落在各命令/技能模板文本里的隐式步骤,这样我可以按类治理插点特征、按实例核对落点。

**Why this priority**:Probe 是整个重构的概念基座;Class/Object 两层让「特征定义」与「系统落点」分离,没有它,结构图与切片定向都无从谈起。

**Independent Test**:枚举 probe 真源:既有 49 个嵌入点每个都有对应 Object 定义,每个 Object 归属于唯一 Class,无悬空 Object、无未归类 Object、无特征缺失的 Class。

**Acceptance Scenarios**:

1. **Given** 任一现有反馈嵌入点(skill 或复杂命令的 wrap-up step),**When** 查询 probe 真源,**Then** 存在一个 Probe Object,其声明的插入位置与该嵌入点一致,且该 Object 归属于一个 Class。
2. **Given** 任一 Probe Class 及其任一 Object,**When** 检查要素,**Then** Class 的四项特征(收集内容/目标切片/处理流程/适用插入位置类型)全部存在且非空,Object 绑定具体流程单元与生命周期点且归属唯一 Class。
3. **Given** 维护者要新增一个反馈点,**When** 落地,**Then** 只能以「在既有 Class 下新增 Object(必要时先新增 Class)」的方式进行;不存在不经定义的隐式埋点路径。

---

### User Story 2 - 项目级 Feedback Probe 结构图 (Priority: P1)

作为框架维护者,我需要一张项目级 Feedback Probe 结构图,按 Class→Object 层级一眼看清:当前系统哪些位置插了反馈点、每个点收集什么信息、收集后的数据走什么处理流程——并且这张图从 probe 定义真源派生,定义变了图跟着变,不产生漂移。

**Why this priority**:用户输入中「最重要的一点」;结构图是 probe 两层模型在项目层面的完整投影,直接回答三问。

**Independent Test**:修改任一 probe 定义(Class 或 Object)后重建结构图,内容相应更新;真源不变时连续两次重建,产出零差异。

**Acceptance Scenarios**:

1. **Given** probe 定义集合(全部 Class 及其 Object),**When** 生成结构图,**Then** 图按 Class 分组完整覆盖全部 Object,每个 Object 在图中可回答三问:插入位置、收集内容、处理流程。
2. **Given** 任一 Class 或 Object 的定义被修改,**When** 重建结构图,**Then** 图反映修改后的定义,无需人工同步。
3. **Given** 结构图与真源处于一致状态,**When** 再次重建,**Then** 产出与现有图零差异(可程序判定)。

---

### User Story 3 - 反馈按系统切片定向 (Priority: P1)

作为反馈的消费者(处理 dogfooding 回馈的框架维护者),我希望每条反馈条目都经由其 probe 绑定到一个明确的系统切片(某个命令/技能/脚本/模板/文档域),这样我能按切片过滤、拿到只关于某一部分的反馈,不必在全局视角的冗余信息里翻找。

**Why this priority**:直接解决痛点 1(冗余、无法定向处理);切片归属是消费侧可用性的前提。

**Independent Test**:录入一条反馈后,按其 probe 的切片过滤本地反馈库,一步命中该条目,且结果不含其它切片的任何条目。

**Acceptance Scenarios**:

1. **Given** 一条经 probe 录入的反馈条目,**When** 读取其元数据,**Then** 存在明确的切片归属(经 Object→Class 继承),且该归属可程序判定。
2. **Given** 本地反馈库含多个切片的条目,**When** 按某一切片过滤,**Then** 仅返回该切片的条目。
3. **Given** 一条反馈的叙述内容涉及多个系统部位,**When** 归档,**Then** 其切片归属仍唯一(以 probe 声明的目标切片为准),跨部位发现以条目内字段表达,不得拆散归属。

---

### User Story 4 - /speckit.feedback 三种执行模式 (Priority: P2)

作为 Spec Kit 的用户,我需要 `/speckit.feedback` 命令以三种执行模式工作——**模式一(无参数)**:打印当前项目全部已置入的 probe,以图形列表或竖状(树状)结构明确展示所有 probe 点;**模式二**:直接处理当前项目已收集到的反馈,包括打包与打包后的清理;**模式三**:主动注入一个反馈点(外部 probe)——这样查看、处置、扩展三类诉求各有一条入口,而不必手工翻存储文件或直接调用引擎脚本。

**Why this priority**:解决痛点 2 的完整形态;三模式依赖 probe/切片数据模型先行,故排在 P1 三故事之后。

**Independent Test**:在含 probe 定义与历史条目的真实工作区分别触发三种模式:无参数调用呈现与真源 100% 一致的 probe 总览;模式二完成一次「查看→过滤→处置→打包→清理」闭环;模式三完成一次外部 probe 注入并产出一条可区分的条目。全程不直接触碰存储文件。

**Acceptance Scenarios**:

1. **Given** 项目已置入若干 probe(含内部与外部),**When** 无参数运行 `/speckit.feedback`,**Then** 以图形列表/竖状结构打印全部 probe 点,覆盖度与 probe 真源一致,渲染自真源而非独立副本。
2. **Given** 本地反馈库有条目,**When** 以模式二按切片过滤并处置一批条目,**Then** 得到摘要视图,可执行打包提交路径(复用 package → 手动投递 → mark-submitted 语义),打包完成后已打包条目从活跃库清理(以包内留档为准,处置留痕),全程零网络行为。
3. **Given** 用户只想了解积累状态,**When** 在模式二中查看状态视图,**Then** 呈现计数、阈值与是否到达提示条件。
4. **Given** 用户希望机制安静运行,**When** 经命令调整阈值或静默,**Then** 后续流程不再提示,但反馈记录不停止。
5. **Given** 用户要为自定义单元增加反馈点,**When** 以模式三注入,**Then** 引导声明目标单元与收集特征并落成外部 probe(见 Story 6)。

---

### User Story 5 - 旧格式条目收敛处置,红线不破 (Priority: P2)

作为已在使用反馈机制的下游项目用户,我希望重构对旧格式反馈条目做一次性整体 review 收敛:反馈已合入当前系统的条目直接删除,未合入且仍有价值的以新格式(带 probe 归属)重登记,尽可能不再保留历史积累的陈旧反馈格式——同时四条红线(反馈目标=Spec Kit 框架自身;反馈为用户数据且完全可选;零自动传输;本地 workaround 价值)原样保留。

**Why this priority**:用户裁定的迁移语义(收敛优于堆积);与 P1 并行设计、后置执行,处置动作依赖 probe 模型先就位。

**Independent Test**:在含旧格式条目的工作区副本上执行迁移 review:每条旧条目获得明确处置结论、旧格式残留为 0、处置记录可审计;红线检查清单逐条通过。

**Acceptance Scenarios**:

1. **Given** 含旧格式条目(无 probe 归属)的反馈库,**When** 执行一次性整体 review,**Then** 每条旧条目获得处置结论——反馈已合入(或已过时)的删除、未合入且仍有价值的以带 probe 归属的新格式重登记——且全部结论记入可审计的处置记录。
2. **Given** 迁移处置完成,**When** 读取阈值与提交计数状态,**Then** 计数按处置结果重算(重登记条目计入,已删除条目不再计入),不重复触发合并提交提示。
3. **Given** 任意记录/管理/处置操作,**When** 审计其行为,**Then** 不存在任何网络传输动作。

---

### User Story 6 - 外部 probe:面向宿主项目自定义单元的本地反馈环 (Priority: P2)

作为宿主项目维护者,我的项目在 Spec Kit 之上自定义了 Skill / Agent / Command——它们不属于框架自身,现有的框架反馈点覆盖不到。我希望能通过 `/speckit.feedback` 模式三主动注入**外部 probe(External Probe)**,对这些自定义单元收集运行反馈;这些反馈**保留在本项目内**,用于项目自身 skill/command 的优化,与框架自身的反馈(内部 probe)分开处理,绝不上送 Spec Kit。

**Why this priority**:用户裁定的第三模式核心扩展;把反馈机制的受益面从「框架自身」扩展到「宿主项目自定义单元」(Dogfooding Loop B 的 probe 化落地)。依赖 probe 模型与命令先就位,故 P2。

**Independent Test**:在一个含自定义 skill 的项目中注入一个外部 probe 并触发一次其目标单元的运行:产出一条带外部归属、可单独过滤的条目;随后执行框架反馈打包,包内该条目出现次数为 0。

**Acceptance Scenarios**:

1. **Given** 项目含自定义 skill/agent/command,**When** 经 `/speckit.feedback` 模式三注入外部 probe(声明目标单元与收集特征),**Then** 新增一个类别为外部、遵循 Class/Object 建模且四项特征完备的 probe 定义,指向该自定义单元。
2. **Given** 外部 probe 产出的一条反馈条目,**When** 查看其归属与检索,**Then** 与内部 probe 条目可区分、可单独过滤,并保留在宿主项目本地。
3. **Given** 用户执行框架反馈的打包提交,**When** 生成上送包,**Then** 外部 probe 条目 100% 被排除在外。
4. **Given** 项目维护者要优化自己的自定义单元,**When** 消费外部 probe 反馈,**Then** 可作为本地改进依据(workaround/优化点检索),全程零网络行为。

---

### Edge Cases

- 旧条目 review 中「反馈是否已合入当前系统」无法判定时,处置缺省如何裁定(倾向保留并重登记,而非误删)?
- Probe Object 被重命名/删除,或被重新归类到另一 Class 后,历史条目上的 probe 引用与切片归属如何呈现(按记录时点还是当前定义),不误报为数据损坏?
- 同一次运行命中多个 probe(嵌套 command→skill 各自 wrap-up):条目各自归属各自 Object,互不覆盖、不重复计数(沿用现有嵌套规则)。
- 某 probe 长期零产出(对应流程一直干净运行):「空产出」与「probe 失效」如何区分,结构图如何标注?
- standalone 部署(工作区无 `.specify/`):runtime-mode gate 整体跳过反馈,probe 化不得破坏此门。
- 插点总量大(49 个 Object)时结构图的可读性:按 Class 分组、组内 Object 明细呈现,而非平铺长表。
- 外部 probe 的目标自定义单元被删除/重命名后,probe 定义与历史条目如何呈现(不误报损坏,允许悬空标注)?
- 外部 probe 与内部 probe 的标识命名空间:同名冲突如何避免(强制隔离或允许同名不同类别)?
- 宿主项目无任何自定义单元时,模式三的空态呈现与引导。
- 模式二「打包后的清理」与既有 mark-submitted 归档语义的衔接:清理范围 MUST 限定为已进入打包批次的条目,不得误清未打包条目。

## Requirements *(mandatory)*

### Functional Requirements

**Probe 概念与真源**

- **FR-001**: Feedback Probe MUST 采用两层建模:**Probe Class(插点类)**定义一类插点的特征——收集内容(该类点收集什么信息)、目标系统切片、收集后处理流程、适用的插入位置类型;**Probe Object(插点实例)**是 Class 在当前系统中的实例化,绑定具体流程单元与其生命周期点。Class 的四项特征任一缺失 MUST 被判定为无效 Class 定义。
- **FR-002**: 每个 Probe Class 与每个 Probe Object MUST 各自拥有项目内唯一标识;每个 Object MUST 归属且仅归属一个 Class;反馈条目 MUST 经由 Object 标识引用其 probe,并自该 Object 所属 Class 继承目标系统切片。
- **FR-003**: Class 与 Object 的定义 MUST 集中于单一真源并可由程序枚举;Probe 结构图及任何派生视图 MUST 从该真源生成,MUST NOT 维护独立的手工副本。
- **FR-004**: 重构 MUST 覆盖现有全部隐式反馈嵌入点(实测 31 个 skills + 18 个命令模板的 wrap-up step):每个嵌入点重构为对应的 Probe Object,并归类到具体的 Probe Class 之下;迁移前后插点数量与覆盖面守恒(既有嵌入点不新增、不丢失),且不存在未归类的 Object。Class 集合的划分 MUST 覆盖既有全部插入形态;后续增删插点只能经 probe 定义(Object 或 Class)。

**切片定向**

- **FR-005**: 每条新录反馈条目 MUST 经由其 probe 绑定唯一的系统切片;MUST NOT 产生无切片归属的新条目。
- **FR-006**: 系统切片的划分 MUST 与框架既有组成维度对齐(命令/技能/脚本/模板/文档),MUST NOT 自造一套平行分类体系。
- **FR-007**: 反馈的检索与消费接口 MUST 支持按切片与按 probe 过滤;过滤 MUST 由程序判定完成,不依赖人工通读条目。

**本地管理命令**

- **FR-008**: 系统 MUST 提供 `/speckit.feedback` 命令 [[STR-001]] 作为反馈的本地管理接口,并以**三种执行模式**组织——模式一(probe 总览,无参数时的缺省模式)、模式二(处理已收集反馈)、模式三(注入外部 probe);该命令归类为复杂命令(调用引擎脚本),用户 MUST NOT 需要手工编辑存储文件或直接调用引擎脚本才能完成管理动作。
- **FR-009**: 命令 MUST 支持模式一:不带参数时打印当前项目全部已置入的 probe,以图形列表或竖状(树状)结构呈现,按 Class→Object 层级组织并标注内外类别;呈现内容 MUST 渲染自 probe 真源,覆盖度与真源 100% 一致。
- **FR-010**: 命令 MUST 支持模式二:直接处理当前项目已收集的反馈——摘要视图(按 probe/切片/单元/时间过滤)、状态视图(积累计数、阈值、是否到达提示条件)、处置动作(处置标记、打包提交路径、阈值与静默调整),以及**打包后的清理**(打包完成后,已打包条目从活跃库移除、以包内留档为准,处置 MUST 留痕);全部动作 MUST 复用既有流转语义(package → 手动投递 → mark-submitted 本地记账),MUST NOT 引入任何网络传输行为。
- **FR-011**: 条目的处置状态(如已处理/忽略)MUST 为附加的本地元数据, MUST NOT 改写条目正文内容。

**结构图**

- **FR-012**: 项目级 Feedback Probe 结构图 MUST 完整回答三问——系统中哪些位置插入了反馈点、各点收集什么信息、收集后数据经什么处理流程——并按 Class→Object 层级组织(每个 Class 一组,组内 Object 各自标明插入位置、收集内容、处理流程);其覆盖度 MUST 可与 probe 真源程序对账(图 ↔ 真源双向零缺漏)。
- **FR-013**: 结构图 MUST 为派生物:从 probe 真源重建 MUST 得到与当前图一致的内容;真源未变时两次重建 MUST 零差异。

**兼容与红线**

- **FR-014**: 旧格式反馈条目(无 probe 归属)MUST 经一次性整体 review 完成收敛处置:反馈已合入当前系统或已过时的条目直接删除;未合入且仍有价值的条目以新格式(带 probe 归属)重新登记;每条旧条目的处置结论(删除/重登记)MUST 记入可审计的处置记录;目标为旧格式残留条目数为 0。
- **FR-015**: 迁移处置完成后,阈值与提交计数状态 MUST 按处置结果重算(重登记条目计入,已删除条目不再计入),MUST NOT 重复触发合并提交提示。
- **FR-016**: 四条红线按内外类别分级成立——**内部 probe**:反馈目标=Spec Kit 框架自身、反馈为用户数据且完全可选、零自动传输、本地 workaround 价值,四条原样保留;**外部 probe**:反馈目标=宿主项目自定义单元,其余三条(用户数据可选、零自动传输、本地 workaround 价值)同样成立,且其反馈 MUST NOT 上送 Spec Kit。
- **FR-017**: skills 的 runtime-mode gate(无 `.specify/` 的 standalone 部署整体跳过反馈体系)MUST 在 probe 化后仍然成立。

**外部 probe(模式三)**

- **FR-018**: Probe Class MUST 携带类别标注(internal/external 二值);既有 49 个框架插点的 Class 全部为内部类别;外部类别专用于宿主项目自定义单元(Skill/Agent/Command 等非框架资产)。
- **FR-019**: 系统 MUST 支持 `/speckit.feedback` 模式三注入外部 probe:经引导声明目标自定义单元与收集特征,生成遵循 Class/Object 两层建模、四项特征完备、类别为外部的 probe 定义,落入 probe 真源;注入后的外部 probe 与内部 probe 使用同一记录引擎与条目格式。
- **FR-020**: 外部 probe 产出的反馈条目 MUST 与内部条目分开处理:类别归属可程序判定、可单独过滤,并保留在宿主项目本地;框架上送打包路径(package)MUST 100% 排除外部条目。
- **FR-021**: 外部 probe 反馈的目标是宿主项目自定义单元(而非 Spec Kit 框架),服务于项目自身 skill/command 的优化(Dogfooding Loop B);其查看/处置/清理复用同一命令与引擎能力,全部处置为零网络本地操作。

### Key Entities *(include if requirement involves data)*

- **Probe Class(插点类)**: 一类反馈插点的特征定义。关键属性:项目内唯一标识、类别(internal/external)、收集内容声明、目标系统切片、收集后处理流程、适用的插入位置类型。关系:一个 Class 下有多个 Probe Object;一个系统切片可被多个 Class 声明为目标。
- **Probe Object(插点实例)**: Probe Class 在当前系统中的实例化。关键属性:项目内唯一标识、归属 Class(唯一)、绑定的流程单元 × 生命周期点。关系:继承所属 Class 的特征(含类别与切片);产出 Feedback Entry;同一 Class 的 Object 共享收集内容与处理流程定义。
- **External Probe(外部 probe)**: 类别为 external 的 probe,目标是宿主项目自定义单元(Skill/Agent/Command 等)。关系:与内部 probe 同构建模、同引擎记录;其条目与内部条目分开处理,不进入框架上送路径。
- **System Slice(系统切片)**: 反馈针对的框架部位,取值沿框架既有组成维度(命令/技能/脚本/模板/文档);外部 probe 的切片取值为宿主项目自定义单元。关系:被 Probe Class 声明为目标;由条目经 Object→Class 继承,作为过滤与统计维度。
- **Feedback Entry(反馈条目)**: 既有实体;本需求扩展 probe 引用(Object 级)、类别与切片归属(继承)及本地处置状态,正文与既有字段不动。
- **Probe Map(Probe 结构图)**: probe 真源的派生呈现,按 Class→Object 层级回答三问并标注内外类别;非独立维护实体,只能重建生成。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 隐式反馈点迁移覆盖率 100%:程序对账「probe 真源 ↔ 嵌入点清单」双向零缺漏且无未归类 Object——既有嵌入点 49 个(31 skills + 18 commands)逐一对账;本需求新增的 `/speckit.feedback` 命令自身插点(第 50 个 Object)与其模板落地**同变更登记**(对账以实施时嵌入清单实测为准)。
- **SC-002**: 切片归属完备:全部新录条目 100% 具备 probe 引用与切片归属,无归属新条目数为 0。
- **SC-003**: 结构图零漂移:真源不变时连续两次重建产出零差异;真源修改后重建差异仅出现在对应 Class/Object 条目。
- **SC-004**: 按切片一步过滤:在含 ≥3 个切片条目的库上,单次命令操作完成过滤,结果不含其它切片的条目。
- **SC-005**: 旧条目处置完备:每条旧格式条目均有处置结论(删除/重登记)记入处置记录,旧格式残留条目数为 0;重登记条目以新格式可检索;计数按处置结果重算且不重复触发提示。
- **SC-006**: 红线行为不变:全部记录/管理/处置动作的网络传输次数为 0。
- **SC-007**: 三模式单步可用:模式一无参数一次调用呈现全部已置入 probe 且与真源零缺漏;模式二完成含打包后清理的处置闭环(清理后活跃库中已打包条目数为 0,包内留档完整);模式三完成一次外部 probe 注入闭环(定义落源 + 产出一条可区分条目)。
- **SC-008**: 外部隔离:框架上送包中外部位条目数为 0;外部条目按类别单独过滤一步命中且不出现在内部过滤结果中。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 对账程序比对 probe 真源与嵌入点清单(`templates/commands/*.md`、`skills/*/SKILL.md` 的 `## Feedback` 嵌入),并校验每个 Object 的 Class 归属唯一且非空;实施与回归各跑一次。
- **SC-002 Source**: 对反馈存储库(或引擎记录路径)做条目元数据完备性校验,抽样或全量。
- **SC-003 Source**: 结构图重建产物的 diff(两次重建比对 + 一次受控修改后比对)。
- **SC-004 Source**: `/speckit.feedback` 在含混合切片数据的测试工作区实测。
- **SC-005 Source**: 迁移处置记录逐条核对(结论覆盖率)+ 迁移前后 store 目录对账(残留为 0、重登记条目可检索)+ index 计数重算结果;在副本环境执行。
- **SC-006 Source**: 引擎代码路径审计(无网络调用)+ 实测行为观察,与现行红线核查口径一致。
- **SC-007 Source**: `/speckit.feedback` 三模式在测试工作区实测;打包产物与活跃库对账(包内留档 vs 活跃库清空)。
- **SC-008 Source**: 打包产物审计(外部位条目计数)+ 按类别过滤实测(含混合内外条目的库)。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `/speckit.feedback` | FR-008, tasks(命令模板落地任务), contracts(命令存在性与命名契约) |

## Out of Scope

- 不改变反馈内容的生产方式:仍为 agent 自评,绝不向用户征求反馈内容(既有红线)。
- 不引入自动上传/网络传输;不建设任何服务端。
- 不重构 intake 侧(框架仓库根 `feedback/` 目录的批量处理流程)。
- 不引入数据库/向量存储;维持 files-based 引擎形态。
- 不改变 `/speckit.review` 的全局评估职责边界(反馈条目仍 `scope: local`)。
- 不在本需求内扩充新的收集语义(如性能计量、遥测埋点);仅将既有反馈点显性化、结构化,并新增面向宿主项目自定义单元的外部 probe 注入(收集语义与内部一致,仍为 agent 自评)。

## Assumptions

- probe 真源的载体位置与文件格式(目录/模板/schema)留待 plan 阶段裁定;需求层仅约束「单一真源、可程序枚举、派生物可重建」。
- Probe Object 与既有嵌入点一一对应(31 + 18 = 49);Probe Class 的具体划分方案(按单元类型/生命周期点/切片维度组合)留待 plan 裁定,但 MUST 覆盖既有全部插入形态。同一单元内多个生命周期点各自成 Object 属于后续扩展。
- 内外 probe 共用同一真源与条目引擎,以类别字段区分;物理目录是否分离由 plan 裁定。
- 外部 probe 的目标单元标识方式(如何引用宿主项目的自定义 skill/agent/command)由 plan 裁定。
- 模式二「打包后的清理」语义:仅清理已进入打包批次的条目,以包内留档为准;与 mark-submitted archive-then-reset 语义的衔接在 plan 中核对落位。
- 结构图为单一派生文档,内含渲染架构图与 Class→Object 明细表;渲染手段留待 plan。
- 旧条目整体 review 由 agent 逐条裁定、处置记录供用户审计;处置仅本地文件操作,不构成投递。
- `/speckit.feedback` 归类为复杂命令:自身按嵌套规则在 wrap-up 记录 `scope: local` 自评。
- 条目处置状态为本地记账语义(mark-submitted 语义的扩展),不产生任何投递动作。
- 用户输入中的「Spike 框架」为 Spec Kit 的同音误写,已按项目词汇表校正为 Spec Kit。
- 「系统切片」沿用框架既有组成维度(命令/技能/脚本/模板/文档),真源表述见 `docs/reference/skills/feedback.md` 与 `.specify/instructions.md` Key Directories。

## Clarifications

### Session 2026-08-14

- Q: Related Feature 绑定既有 Feature 028 还是新建 Feature? → A: 绑定 **Feature 028(Feedback Mechanism)**——Probe 概念仍属反馈域、消费方即反馈机制自身,沿用 027/036 扩展绑定与 016 重构绑定先例;028 的 Feature 描述在交付时扩展覆盖 Probe 化模型。
- Q: 初始 Probe 粒度(与既有 49 个埋点 1:1,还是粗粒度聚合)? → A: 引入**两层建模**——Probe Class 定义插点特征,Probe Object 为其在当前系统中的实例化表现;既有 49 个插点重构为 Probe Object 并**归类到具体 Class 之下**(Object 级数量守恒不变,Class 划分方案留待 plan)。
- Q: 旧格式条目(无 probe 归属)在切片过滤视图中如何处理? → A: **不保留旧格式残留**——对旧库做一次性整体 review:反馈已合入当前系统的条目直接删除;未合入且仍有价值的以新格式(带 probe 归属)重登记;尽可能不再保留历史积累的陈旧反馈格式,处置留痕。
- Q: 词汇表登记哪些新术语? → A: 登记 **Feedback Probe** 与 **System Slice**(均 origin=auto, status=proposed)。

### Session 2026-08-14(第二轮,经 /speckit.plan 传入)

- 用户修订指示(原话,problem→probe、Spark Kit→Spec Kit 已按词汇表校正):「在 /speckit.feedback 命令这个执行流程中需要设计三种执行模式:1. 不带参数的情况下,打印当前项目所有已置入的 probe,并生成图形列表或竖状结构,明确展示项目中所有的 probe 点。2. 直接处理当前项目中已收集到的 feedback,包括打包后的清理。3. 三是主动注入一个反馈点。因为当前的所有反馈都是针对 Spec Kit 框架本身的流程进行的,但很多项目会自定义自己的 Skill 或 Command。手动注入的反馈点可以针对这些用户自定义的 Skill、Agent 或 Command 进行反馈收集。当然,在处理这种反馈点时,需要将其与 Spec Kit 框架自身的反馈信息分开处理。要求 probe 中定义『外部 probe』,即这些 probe 插入点获取到的反馈信息不反馈给 Spec Kit 项目,而是保留到对应项目中,用于项目自定义 skill 和 command 的优化。」
- 集成:Story 4 重写为三模式;新增 Story 6(外部 probe);FR-008/009/010 重写(三模式与打包后清理)、FR-016 改为按内外类别分级;新增 FR-018~021(外部 probe 组);Key Entities 增类别维度与 External Probe 实体;新增 SC-007/008;Edge Cases 与 Assumptions 增补。
- FR 编号映射(旧→新):旧 FR-009(摘要/状态/处置三类能力)并入新 FR-010(模式二);新 FR-009 承担模式一(probe 总览);旧 FR-010(流转语义)并入新 FR-010;其余 FR 编号未变、无删除。
