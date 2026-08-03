# Requirements Specification: /speckit.docs 文档规范与管理命令

**Requirement Branch**: `033-docs-command`  
**Created**: 2026-07-28  
**Status**: Draft  
**Input**: User description: "设计一个/speckit.docs命令用来规范和管理项目的文档,总体设计参考docs/notes/docs-design.md文档,docs/notes/notes-design.md文档中进行了补充设计.在docs命令中需要使用shared/patterns/reconcile-pattern.md模式进行设计,在实现之后基于dogfooding理念对项目自身也使用docs命令进行文档的整理和修改,在此过程中还可以基于feedback持续进行优化."

## Related Feature *(mandatory)*

**Feature ID**: 037  
**Feature Name**: Docs Command

## Overview

`/speckit.docs` 是一个面向**项目文档空间**的规范与管理命令。它把两份设计笔记（`docs/notes/docs-design.md` 的"K8s 基底 + ADR 机制 + 根目录索引"整体结构，`docs/notes/notes-design.md` 的 notes 退场机制补充设计）确立为文档空间的**期望态基线**，并按 `.specify/shared/patterns/reconcile-pattern.md` 的调谐模式（Reconcile Pattern）实现为**单一调谐引擎**：观察当前态 → 计算期望态 → 容忍带过滤 → 干跑计划 + 分级确认 → 收敛（只归档不删除）→ 校验与残差报告。

期望态基线的核心内容：

- **薄层根目录**：`README.md`（总入口索引）、`ARCHITECTURE.md`（一页纸架构摘要）、`CONTRIBUTING.md`（贡献入口摘要）、`CHANGELOG.md`（自包含时间线）——永远不超过一屏，内容膨胀即下沉到 `docs/`。
- **厚层 `docs/`**：按文档类型分目录——`concepts/`（What & Why）、`tutorials/`（学习路径）、`tasks/`（任务步骤）、`reference/`（精确规范）、`decisions/`（ADR，只追加）、`contribute/`（贡献者指南），外加 `notes/`（临时文档，受生命周期约束、会退场）。
- **Notes 退场机制**：frontmatter 元数据（created/expires/status/target 等）+ 状态机（draft → archived / expired）+ 确定性生命周期自动化（扫描、标记过期、确认清理、归档完整性检查、统计）。
- **命名语义**：特定名称的文档具有固定含义，文件名本身是语义的一部分——特殊文档全大写（当前注册：README / ARCHITECTURE / CONTRIBUTING / CHANGELOG），普通文档小写 kebab-case，注册表可扩展。
- **文档同步步骤**：仿照既有 Feedback 步骤，在核心命令收尾的同一生命周期点插入轻量文档同步评估（需记录 / 无需记录），持续保持文档与项目状态一致。

交付分两级：(1) 命令本体——与其他 `/speckit.*` 命令同等地分发到全部受支持的 AI 工具；(2) **Dogfooding 落地**——实现后对 Spec Kit 项目自身运行该命令完成文档整理（含 `docs/notes/` 中两份设计笔记自身的退场），并经既有 Feedback 机制在后续运行中持续优化（复用既有 Dogfooding / Feedback 两级循环，不新建循环机器）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 文档空间调谐（单一引擎收敛文档结构） (Priority: P1)

作为项目维护者，我在任意使用 Spec Kit 的项目中运行 `/speckit.docs`，命令将项目文档空间（根目录入口文件 + `docs/` 目录树）向标准期望态收敛：缺失的骨架被创建（bootstrap）、散落/膨胀的内容按类型归位、失效链接被指出，全过程先出计划、经我确认后才执行移动/归档，且从不静默删除内容。

**Why this priority**: 这是命令的核心引擎，其余故事（notes 生命周期、dogfooding、feedback 优化）都建立在调谐环之上；单独交付即是可用的 MVP。

**Independent Test**: 在一个空白目录与一个已有杂乱文档的样例项目上各运行一次：前者产出完整文档骨架，后者产出观察快照、干跑计划、审计日志与残差报告四件套，且未确认的移动/归档零执行。

**Acceptance Scenarios**:

1. **Given** 项目没有 `docs/` 结构或根目录入口文件, **When** 运行 `/speckit.docs`, **Then** 按 bootstrap 作用域生成完整骨架（薄层根目录入口 + 各类型目录 + notes 规则说明），并留有审计日志。
2. **Given** 项目已有文档且部分内容偏离期望态, **When** 运行全量调谐, **Then** 容忍带内的表面差异被标记"已一致（容忍）"且不进入收敛计划；实质偏差以干跑计划呈现，移动/归档类动作停下等待确认。
3. **Given** 干跑计划已确认, **When** 引擎收敛, **Then** 当前态中不属于期望态的内容被移入归档区而非删除，同名冲突以后缀避让，任一移动失败即停止剩余项并请求人工介入。
4. **Given** 一次调谐完成, **When** 查看输出, **Then** 残差报告如实列出已收敛/已归档/已容忍/待人工决策各项；若本次无净变化，审计日志仍记录"全部维度在容忍带内"。
5. **Given** 用户带着一个具体目标（如"整理 README"）或一份原始材料调用命令, **When** 引擎解析作用域, **Then** 分别进入单目标定向收敛或扇出分诊，而不是新增独立模式。
6. **Given** 用户带着写作要求（如"写一份部署教程"）调用命令, **When** 引擎解析作用域, **Then** 进入文档写作流程：解析需求并按 taxonomy 定位类型目录，产出符合命名与格式规范（kebab-case、保留名阻断、ADR 编号登记、notes frontmatter）的新文档，随后完成校验、索引更新与审计落盘；主题已被既有文档覆盖时提出定向更新而非新建近重复文件。

---

### User Story 2 - Notes 临时文档生命周期管理 (Priority: P2)

作为项目成员，我把调研笔记、方案草稿等临时内容放进 `docs/notes/`，每篇带 frontmatter 元数据（标题、创建/过期日期、状态、预期归宿）；到期后系统标记过期并提醒我三选一（合入正式文档、续期、确认删除），使 notes 保持"有进有出"，不变成垃圾场。

**Why this priority**: 退场机制是补充设计的核心增量，也是防止文档空间腐化的关键闭环；依赖 US1 的引擎但可独立验证。

**Independent Test**: 构造 draft / 超期 draft / archived 三类样例笔记，跑一轮生命周期动作（扫描 → 标记过期 → 三条退场路径各演练一次），验证状态流转与报告输出符合状态机定义。

**Acceptance Scenarios**:

1. **Given** 一篇缺失必填 frontmatter 字段的 notes 文档, **When** 调谐观察到它, **Then** 被点名为不合规并给出补全建议（含默认过期日期 = 创建日 + 60 天）。
2. **Given** 一篇 draft 笔记超过 expires 日期, **When** 执行生命周期扫描/标记, **Then** 其状态被标为 expired 并出现在待处理清单中，但文件不被自动删除。
3. **Given** 一篇 expired 笔记被作者判定值得正式化, **When** 走合入流程, **Then** 内容落到 target 指定的正式目录，笔记状态改为 archived 且正文标注归宿链接；归档完整性检查能发现 target 缺失的情况。
4. **Given** 一篇 expired 笔记被判定无用, **When** 执行清理, **Then** 删除仅在人工确认后发生（notes 区是唯一允许确认后真删除的区域）。
5. **Given** 一篇 expired 笔记仍有价值但未到合入时机, **When** 续期, **Then** expires 更新、状态回到 draft。

---

### User Story 3 - 核心命令的文档同步评估步骤 (Priority: P2)

作为使用 Spec Kit 的项目成员，核心 `/speckit.*` 命令在收尾（与既有 Feedback 自省同一生命周期点）额外执行一步轻量的**文档同步评估**：判断本次运行产生的信息（新能力、关键决策、结构变化）是否需要记录或更新到项目文档空间；需要时按语义路由落到正确的目标文档，从而使文档持续与项目实际状态保持一致，而不是等到某次全量调谐才集中纠偏。

**Why this priority**: 文档操作是必需动作——一致性靠高频小步维护成本最低；机制完全仿照既有 Feedback 步骤的插入点与约定形态，零新增循环机器。

**Independent Test**: 抽取任一核心命令模板，确认含文档同步步骤且与 Feedback 步骤同位、引用共享约定单一事实源；执行一次有文档影响的命令运行，评估识别出应记录项并落至正确目标文档；执行一次无文档影响的运行，步骤以"无需记录"结论收尾且不阻断命令完成。

**Acceptance Scenarios**:

1. **Given** 一次核心命令运行到达收尾, **When** 执行文档同步评估, **Then** 与 Feedback 评估在同一收尾点进行，产出"需记录（目标文档 + 要点）/ 无需记录"的明确结论，且不阻断命令完成。
2. **Given** 评估结论为需记录, **When** 执行文档写入, **Then** 写入遵循 `/speckit.docs` 的期望态基线与安全写入门禁（不覆写同名内容、正式区只归档不删除）。
3. **Given** 文档同步步骤的约定需要调整, **When** 修订约定, **Then** 只需修改共享约定文档（单一事实源），各命令仅通过引用生效，不存在各命令重复定义。

---

### User Story 4 - Dogfooding：对 Spec Kit 自身运行文档整理 (Priority: P3)

作为 Spec Kit 维护者，命令实现后我对 Spec Kit 项目自身运行 `/speckit.docs`，把项目现有文档（根目录入口、`docs/` 各子目录、`docs/notes/` 中的两份设计笔记）纳入调谐，基调为**激进重组**：以本次用户输入为最高优先级期望态来源，将 `docs/` 实质性向标准六类 taxonomy 收敛（既有子目录按类型归位），重组幅度由干跑计划逐项确认；两份设计笔记走完 notes 退场流程（内容合入正式文档后归档）；引用方向、符号链接、镜像同步与 Documentation Map 随重组同步更新。

**Why this priority**: 践行既有 Dogfooding 治理原则（框架用自己的能力开发/管理自己）；依赖 US1/US2 先就绪，且结果反哺命令设计。

**Independent Test**: 在 Spec Kit 仓库运行一次全量调谐并完成确认与收敛后，检查：审计日志与残差报告存在于 `.specify/` 命令工作区；`docs/` 顶层布局符合六类 taxonomy + notes；`docs/notes/` 中两份设计笔记状态为 archived 且 target 真实存在；全部内部链接可达。

**Acceptance Scenarios**:

1. **Given** Spec Kit 现有 `docs/` 布局与标准类型目录不一致, **When** 运行调谐, **Then** 差异按激进基调进入干跑计划（归类搬迁逐项可勾选退出），经确认后执行实质性重组，而非以既有命名为由容忍搁置。
2. **Given** `docs/notes/docs-design.md` 与 `docs/notes/notes-design.md` 的设计内容已随本需求落地为正式文档, **When** 走 notes 退场流程, **Then** 两份笔记被归档并标注归宿，notes 目录不留无主内容。
3. **Given** 重组触及项目既有文档引用方向（README → docs 单向索引）、兼容性符号链接或 Documentation Map, **When** 收敛执行, **Then** 相关引用与链接被同步更新到新路径，零悬空引用；无法自动同步的项列入待人工决策。

---

### User Story 5 - 基于 Feedback 的持续优化 (Priority: P4)

作为 Spec Kit 维护者，`/speckit.docs` 与其他复杂命令一样带标准 Feedback 自省步骤：每次合格运行在收尾时记录一条针对本命令的评审与优化点；在 dogfooding 及后续真实使用中，这些反馈经既有链路（记录 → 阈值提示 → 打包 → 手动提交）驱动命令自身迭代。

**Why this priority**: 复用既有 Feedback 机制（零新增机器），价值在长期；依赖命令先可用。

**Independent Test**: 完成一次合格的命令运行后，检查反馈存储中存在以本命令为 unit-id 的当次记录；同一运行标识重复记录时引擎去重不落双份。

**Acceptance Scenarios**:

1. **Given** 一次到达收尾阶段的命令运行, **When** 执行 Feedback 步骤, **Then** 一条 scope 为 local、单元为本命令的自省记录落盘，且不向用户征集反馈内容。
2. **Given** 反馈条目累计达到既有阈值, **When** 收尾提示出现, **Then** 提示为既有的合并提交邀请，提交保持手动可选。

---

### Edge Cases

- **既有文档结构与标准目录严重分歧**：一般项目默认本地惯例优先、容忍带兜底，引擎不得为追求形式一致而未经指示强制搬迁；当用户显式给出重组基调（如 dogfooding 的激进重组指示，用户输入是期望态最高优先级来源）时按指示收敛——两种情形下超出容忍带且影响面大的重组都必须在计划中逐项可勾选退出。
- **重复运行防抖**：对同一状态连续运行两次，第二次不得产生新的收敛动作（反 churn）；但审计日志仍须留痕。
- **frontmatter 缺失/损坏的 notes**：点名并给出修复建议，不猜测状态、不自动删除。
- **archived 笔记的 target 失效**（目标文件被移动/不存在）：归档完整性检查报告异常，列入待人工决策。
- **正式文档区（concepts/tutorials/tasks/reference/decisions/contribute）**：只增不删、只归档不删除；`decisions/` 中的 ADR 只追加，状态变更（Deprecated/Superseded）通过标注而非改写历史。
- **命令误用为终端命令**：`/speckit.docs` 是聊天指令而非 shell 命令，文档与提示须与既有约定一致。
- **期望态无法确定**（如用户输入含糊且本地无惯例可循）：提出最少必要问题（≤3），不得虚构期望态。
- **异常中断**：收敛中途失败时保留已完成项、停止后续项、审计日志记录断点，不回滚已成功的归档。
- **文档同步步骤成本失控**：收尾评估必须是增量判断（只看本次运行触及的信息），不得触发完整 R0–R6 全量扫描；连续多次"无需记录"是正常结果，不得为凑产出强行写文档。
- **特殊名滥用**：普通文档使用大写保留名（含小写化变体、或在注册位置之外使用保留名——如子目录中的 README.md）属确定性违规，点名并给出小写替代名（目录索引 → `index.md`）；重命名属移动类动作，须经干跑计划确认。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 框架 MUST 提供 `/speckit.docs` 聊天命令，管理的制品空间为：项目根目录入口文件（README、ARCHITECTURE、CONTRIBUTING、CHANGELOG）+ `docs/` 目录树；命令 MUST 与其他 `/speckit.*` 命令同等地分发到全部受支持的 AI 工具，并提供命令参考文档。
- **FR-002**: 命令 MUST 内置标准文档期望态基线：(a) 薄层根目录——四个入口文件各司其职（总入口索引 / 一页纸架构摘要 / 贡献入口摘要 / 自包含变更时间线），且"永远不超过一屏"，膨胀内容下沉 `docs/`；(b) 厚层 `docs/`——六个正式类型目录（concepts、tutorials、tasks、reference、decisions、contribute）+ notes 临时区；(c) 文档生命周期流转（想法 → ADR Proposed → Accepted → 沉淀到 concepts/reference → 操作文档 → 过时决策标注 Deprecated/Superseded）。
- **FR-003**: 命令 MUST 按调谐模式实现为单一引擎：作用域判定（无参全量 / 单目标定向 / 原始材料扇出 / 写作委托文档写作 / 空间为空 bootstrap）+ 调谐环（观察快照 → 期望态计算 → 容忍带优先的分维度差异 → 干跑计划 + 分级确认 → 收敛 → 校验与残差报告）；MUST 产出四件强制产物（观察快照、干跑计划、审计日志、残差报告，审计日志即使零收敛也要落盘），其中需落盘的运行产物（干跑计划、审计日志等）MUST 落在 `.specify/` 下的命令工作区，不混入读者可见的 `docs/`；期望态来源优先级 MUST 为：模板 < 规则阈值 < 原则 < 外部权威事实 < 本地既有惯例 < 本次用户输入。MUST NOT 以新增顶层模式的方式扩展能力。写作作用域 MUST 遵循同一调谐环语义（期望态新增文档，收敛 = 创作），其产出的新文档 MUST 符合期望态基线规范：类型归位与命名（FR-002、FR-010）、ADR 编号与登记（FR-005）、notes frontmatter（FR-006），且 MUST 经校验、索引更新与审计落盘收尾。
- **FR-004**: 收敛动作 MUST 执行分级确认门禁：安全本地写入（建目录、建/补管理文件、修链接、更新索引）自动执行且从不覆写同名内容（冲突加后缀避让）；移动/归档/重组类动作 MUST 先出现在可逐项勾选退出的干跑计划中并经确认；正式文档区 MUST 只归档不删除（无"删除"概念），归档区 MUST 位于 `docs/` 内（对文档读者可见、随仓库可追溯）。
- **FR-005**: 命令 MUST 支持 ADR 决策记录管理：`decisions/` 目录含索引与模板，条目按序号追加，具备状态字段（Proposed / Accepted / Deprecated / Superseded by），历史条目只标注不改写。
- **FR-006**: 命令 MUST 支持 notes 退场机制：(a) 每篇 notes 文档强制 frontmatter（标题、创建日期、过期日期、状态，及可选的预期归宿 target 与标签），过期日期默认为创建日 + 60 天；(b) 状态机 [[STR-001]] → [[STR-003]]（已合入，标注归宿）/ [[STR-001]] → [[STR-002]]（超期标记，待处理）/ [[STR-002]] → [[STR-001]]（续期）；(c) 三条退场路径（合入正式文档、续期、确认后删除），其中删除 MUST 经人工确认且仅限 notes 区；(d) 提供确定性的生命周期自动化能力（状态扫描报告、超期标记、确认清理、归档完整性检查、统计），可脱离对话独立重复执行。
- **FR-007**: 差异判定 MUST 区分确定性维度（路径/命名存在性、大写保留名合规、"一屏"尺寸阈值、链接可达性、frontmatter 完整性、ADR 编号连续性）与语义维度（内容归类是否得当、根目录文件是否越权承载实质内容），并为各维度定义容忍带；容忍带内差异 MUST 标记"已一致（容忍）"且不进入收敛计划。
- **FR-008**: 实现完成后 MUST 对 Spec Kit 项目自身执行一次 dogfooding 调谐，基调为**激进重组**：以本次用户输入（期望态最高优先级来源）指示向标准六类 taxonomy 实质性收敛（如 commands → reference、spec-driven → concepts 等归类搬迁），既有目录命名不作为容忍理由；重组仍 MUST 经干跑计划逐项确认；`docs/notes/` 中两份设计笔记 MUST 走完退场流程（设计内容已由本需求落地后归档并标注归宿）；重组 MUST 同步更新而非破坏项目既有一贯性约束（文档单向引用方向、兼容性符号链接、镜像同步关系、Documentation Map 与全部内部链接）。
- **FR-009**: 命令 MUST 携带标准 Feedback 自省步骤（收尾自省、scope local、稳定 run-id 去重、阈值触发合并提交提示），完全复用既有反馈机制；MUST NOT 新建平行的记录、统计或提醒系统。
- **FR-010**: 期望态基线 MUST 包含**保留文件名（Reserved Filenames）**概念——类比编程语言的保留关键字：特定名称的文档具有固定含义，**文件名本身是语义的一部分**；此类特殊文档的文件名 MUST 全大写，且每个保留名 MUST 同时注册其固定语义与**注册位置**，仅允许在注册位置以注册语义使用（严格阻断）。用户自己的文档 MUST NOT 使用保留名；相同语义的文档在其他位置 MUST 改用小写替代名（如目录索引使用 `index.md`）。当前已注册的保留文件（注册位置均为项目根目录）：`README.md`（索引 `docs/` 全部）、`ARCHITECTURE.md`（摘要 `docs/concepts/` + `docs/decisions/`）、`CONTRIBUTING.md`（摘要 `docs/contribute/`）、`CHANGELOG.md`（自包含时间线）。注册表 MUST 可扩展（新增保留名须同时登记语义与位置）；普通文档 MUST 使用小写 kebab-case；保留名的大小写变体与越位使用均属确定性差异维度（FR-007）；本约束 MUST 上升为宪法条款（文档命名原则强化）。
- **FR-011**: 框架 MUST 仿照既有 Feedback 步骤约定，在核心命令的执行路径中插入**文档同步评估步骤**：在评估 feedback 的同一收尾点，评估本次运行产生的信息是否需要记录或更新到项目文档空间，以保持文档与项目当前状态一致。约束：(a) 步骤定义 MUST 以共享约定文档为单一事实源，各命令仅引用不复制；(b) 评估结论 MUST 为"需记录（目标文档 + 要点）/ 无需记录"二者之一，且不阻断命令完成；(c) 需记录时的写入 MUST 遵循 `/speckit.docs` 的期望态基线、语义路由与安全写入门禁；(d) 步骤 MUST 为轻量增量评估，MUST NOT 在命令收尾触发全量调谐；(e) 复用既有插入点形态，MUST NOT 新建平行的记录/统计/提醒系统。

### Key Entities

- **文档空间（Docs Space）**: 命令管理的制品空间 = 薄层根目录入口文件 + 厚层 `docs/` 目录树；含管理区（A）、只读区（B，如代码与规格目录）与锚点（C，如符号链接）三类作用域；归档区位于 `docs/` 内（读者可见），运行产物工作区位于 `.specify/` 下（不混入 `docs/`）。
- **期望态基线（Desired-State Baseline）**: 标准目录分类 + 根目录职责定义 + 尺寸/命名/链接规则 + 文档生命周期流转 + 本地既有惯例 + 本次用户输入的合成体。
- **ADR 条目（Decision Record）**: 编号、标题、状态（Proposed/Accepted/Deprecated/Superseded by）、日期、决策者、背景/决策/替代方案/后果。
- **Notes 文档（Note）**: 带 frontmatter 的临时文档：标题、创建日期、过期日期、状态（[[STR-001]]/[[STR-002]]/[[STR-003]]）、预期归宿 target、标签；受状态机与退场流程约束。
- **特殊文档注册表（Special-Name Registry / Reserved Filenames）**: "文件名即语义"的大写保留名清单，每条含固定含义与注册位置（当前：README/ARCHITECTURE/CONTRIBUTING/CHANGELOG，注册位置均为项目根目录）；类比保留关键字严格阻断——保留名仅限注册位置使用，其他位置同语义文档用小写替代名（目录索引 `index.md`）；可扩展、新增须登记语义与位置；作为期望态基线与确定性校验的一部分。
- **文档同步步骤（Docs-Sync Step）**: 插入核心命令收尾（与 Feedback 步骤同点）的轻量评估约定：输入为本次运行产生的信息，输出为"需记录（目标 + 要点）/ 无需记录"结论；定义在共享约定文档（单一事实源）。
- **调谐产物（Reconcile Artifacts）**: 观察快照、干跑计划（含可勾选退出项）、审计日志（时间戳、作用域、逐项动作与结果、容忍摘要、回滚依据）、残差报告（已收敛/已归档/已容忍/待人工决策）；落盘产物统一存放于 `.specify/` 命令工作区。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在空白样例项目上运行一次即产出完整文档骨架（4 个根目录入口 + 6 个正式类型目录 + notes 区及其规则说明），无需任何手工补建，一次通过。
- **SC-002**: 对同一文档空间连续运行两次全量调谐，第二次收敛动作为零（防抖），且两次均留有审计日志；全部移动/归档动作 100% 先出现在确认计划中，未确认项零执行。
- **SC-003**: notes 生命周期三条退场路径（合入、续期、确认删除）各演练一次全部走通；超期未处理笔记在扫描报告中 100% 被点名；无一次未经人工确认的删除发生。
- **SC-004**: Dogfooding 完成后：`.specify/` 命令工作区存在本次调谐的审计日志与残差报告；Spec Kit `docs/` 顶层布局符合六类 taxonomy + notes，既有文档 100% 归入类型目录或 `docs/` 内归档区；`docs/notes/` 中两份设计笔记 100% 处于 archived 状态且归宿文件真实存在；全部内部链接与 Documentation Map 引用零悬空，兼容性符号链接与镜像同步零破坏。
- **SC-005**: 命令的每次合格运行 100% 留有以本命令为单元的反馈自省记录，同一运行零重复条目；全程零新增反馈机器（引擎动作集、存储布局不变）。
- **SC-006**: 命名语义校验可走通：对含违规命名（小写 readme.md、滥用大写保留名的普通文档）的样例项目运行调谐，违规项 100% 被点名；bootstrap 骨架中 4 个注册特殊文件的职责语义逐项正确。
- **SC-007**: 纳入范围的核心命令模板 100% 含文档同步评估步骤（与 Feedback 步骤同一收尾点、引用共享约定单一事实源、零重复定义）；无文档影响的运行以"无需记录"收尾且零阻断；有文档影响的抽查运行中应记录项被识别并落至正确目标文档。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 空白样例项目演练（集成测试场景或 quickstart 手工演练记录），核对骨架清单逐项存在。
- **SC-002 Source**: 同一夹具连续两次运行的审计日志对比 + 计划文件与实际文件系统变更的差异核对（verification 记录）。
- **SC-003 Source**: 三类样例笔记的生命周期演练记录 + 扫描报告输出核对（集成测试或 verification 记录）。
- **SC-004 Source**: Spec Kit 仓库内审计日志/残差报告存档、`docs/notes/` frontmatter 抽检、`find . -type l` 与镜像 diff 前后比对。
- **SC-005 Source**: 反馈存储条目按 unit-id 过滤核对 + 实现前后反馈引擎动作清单与存储布局 diff。
- **SC-006 Source**: 含违规命名的样例夹具演练记录 + bootstrap 骨架内容抽检（集成测试或 verification 记录）。
- **SC-007 Source**: 命令模板静态扫描（步骤存在性 + 单一事实源引用）+ 两类运行（有/无文档影响）的演练记录。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "draft" | FR-006 状态机、notes frontmatter、生命周期自动化与其测试 |
| `STR-002` | "expired" | FR-006 状态机、notes frontmatter、生命周期自动化与其测试 |
| `STR-003` | "archived" | FR-006 状态机、notes frontmatter、生命周期自动化与其测试 |
| `STR-004` | "expires" | FR-006 frontmatter 必填键、生命周期自动化与其测试 |

**Citation convention**: 下游产物引用以上字面量时写 `[[STR-NNN]]`，不重新誊写。

## Assumptions

- **路径更正**：用户输入的 `shared/patterns/reconcile-pattern.md` 解释为规范路径 `.specify/shared/patterns/reconcile-pattern.md`（协议文档实际位置）。
- **notes 定位采纳"选项 A + 生命周期约束"**：docs-design.md 结尾给出选项 A（保留 notes 目录）与选项 B（用 ADR Proposed 替代）两案；notes-design.md 作为补充设计已完整给出选项 A 的退场机制，故本需求采纳"保留 notes 目录 + 强生命周期约束"，选项 B 精神通过 target 归宿字段（临时文档须有毕业路径）体现。
- **标准 taxonomy 是基线而非铁律**：按调谐模式"本地既有惯例优先于模板"，已有项目的既有目录布局在容忍带内默认视为一致，命令不强制既有项目重命名目录；但用户输入优先级最高——Spec Kit 自身的 dogfooding 运行已由用户指示采用激进重组基调（见 Clarifications），向标准 taxonomy 实质性收敛。
- **CI 定期扫描为可选增强**：notes-design.md 第六节的 CI 集成不列入本需求核心范围，生命周期自动化以可独立重复执行为验收口径。
- **Dogfooding 与 Feedback 复用既有机制**：分别复用既有 Dogfooding 治理原则与 Feedback 机制的既有链路，本需求零新增循环机器。
- **正式区与 notes 区的删除语义**：正式文档区遵循调谐模式"只归档不删除"；notes 区按其生命周期设计允许"经人工确认的删除"，这是设计笔记明确定义的退场路径，不视为与调谐模式冲突。
- **术语规范**："Reconcile Pattern（调谐模式）"与词汇表既有条目 "Reconcile Engine" 同源；"ADR" 指 Architecture Decision Record（架构决策记录）。

## Clarifications

### Session 2026-07-28

- Q: 本需求应绑定哪个 Feature（索引中无文档管理域 Feature）？ → A: 新建 Feature 037 "Docs Command"（Status: Draft）；028 Feedback / 036 Dogfooding 作为复用关联而非归属。
- Q: 调谐归档区与四件强制产物应落在哪里？ → A: 混合方案——归档区在 `docs/` 内（读者可见、随仓库可追溯）；落盘运行产物（干跑计划、审计日志等）在 `.specify/` 命令工作区，不混入 `docs/`。
- Q: Dogfooding 对 Spec Kit 自身的重组幅度基调？ → A: 激进——向标准六类 taxonomy 实质性重组（如 commands → reference、spec-driven → concepts），链接/符号链接/镜像/Documentation Map 同步更新；仍经干跑计划逐项确认。
- 用户修订指示（2026-07-28，plan 阶段）：新增命名语义设计——特定名称的文档有固定含义，文件名本身是语义的一部分，此类特殊文档文件名必须大写；当前已定义：README.md（索引 docs/ 全部）、ARCHITECTURE.md（摘要 concepts + decisions）、CONTRIBUTING.md（摘要 contribute）、CHANGELOG.md（自包含时间线）→ 落为 FR-010 + SC-006。
- 用户修订指示（2026-07-28，plan 阶段）：文档操作是必须的——仿照既有 Feedback 机制，在核心执行路径插入文档同步评估步骤，在评估 feedback 的同时评估当前信息是否需要记录到文档，保持文档与项目状态一致 → 落为 US3 + FR-011 + SC-007。
- 用户修订指示（2026-07-28，implement 阶段）：设计"保留文件名"概念（类比保留关键字）并严格阻断——大写特定名称仅作为保留语义定义（注册位置 + 注册语义），用户文件不得使用相同名称，相同语义可用小写其他名称（目录索引 → index.md），并将该约束写入项目宪法 → FR-010 强化 + 宪法原则 X 修订 + 子目录 README.md 全部更名 index.md。
