# Requirements Specification: Automatic git Close-out（自动收口：提交 · 合并 · 推送与 git workflow 结合）

**Requirement Branch**: `091-auto-git-closeout`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "我每次在作为修改执行都会要求执行:提交,合并,推送, 这应该是一套固定流程,不需要每次都手动触发,在框架中需要找到一个合适的切入点. 需要注意的是:不同的项目存在不同的git workflow, 这个动作需要和git workflow相结合"

## Related Feature *(mandatory)*

**Feature ID**: 091
**Feature Name**: Automatic git Close-out（自动收口）

## Overview

用户每次做完一处修改都要口头要求「提交、合并、推送」——这是一套**固定动作**，却每次都要人工触发，且在无人值守运行里根本没有触发入口。同时，各项目的 git workflow 不同（本仓为临时分支 / trunk-based；他项目可能是单分支、双分支或 MAIN/PRE/DEV 三层），任何写死的分支操作序列都会在别的项目里做错事。

本特性把这个动作做成**框架的一步固定流程**：策略声明在 git workflow 的既有 owner（`.specify/workflow/git.md` 托管块）里，生命周期的插入点放在既有的共享 wrap-up 步骤（`shared/workflow/artifact-commit-step.md`）之后，执行器是既有的 `git-utils` 技能（作用域 A），实际命令序列由所声明的 workflow 模型**推导**而非硬编码。破坏性动作（远程推送、强推、写只读上游）保留其确认门。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 策略在 git workflow 的 owner 里声明一次，收口按它执行 (Priority: P1)

项目维护者在 `.specify/workflow/git.md` 的托管块里声明收口策略（`commit+merge+push` / `commit+merge` / `commit-only` / `ask`，缺省 `ask`）以及可推送的远端集合。此后每次无人值守运行结束，收口动作依该声明执行，不再需要有人在对话里说「提交、合并、推送」，也不会推送托管块标为只读的上游远端。

**Why this priority**: 这是整个特性成立的根——没有单一策略声明点，收口要么无法跨项目复用，要么变成第二份分支事实来源（违反 One Source of Truth）。它单独交付时已经给出「声明 → 行为可预测」的价值。

**Independent Test**: 在一份只含托管块的夹具项目里分别写入四种 `Closeout` 取值，调用执行器的预演（dry-run），断言推导出的动作序列与 `Closeout`、`Closeout remotes` 一致；把 `Closeout` 缺省（released 文本仍为 `ask`）时断言预演给出「需呈现并等待」而不是自动推送。

**Acceptance Scenarios**:

1. **Given** 一个 `Workflow model` 为临时分支、`Closeout` 为 `commit+merge+push` 的项目，**When** 一次产出工件的运行结束，**Then** 收口按「切出短命分支 → 提交 → 合回主干 → 删除本地分支 → 推送主干」的序列推进，且推送只落在 `Closeout remotes` 声明的远端上。
2. **Given** 一个托管块里没有 `Closeout` 行的项目，**When** 同样的运行结束，**Then** 收口只呈现待执行的命令并等待用户决定，MUST NOT 自动推送。
3. **Given** 一个托管块把某远端标为只读上游（本仓为 `origin`），**When** 收口推导推送目标，**Then** 该远端不出现在任何推送步骤中。

---

### User Story 2 - 收口是每个写入运行的固定末尾步骤，不需要额外触发 (Priority: P1)

框架的使用者在任意一个产出工件的命令或技能里做完工作，wrap-up 在既有的步骤序列之后自动带上一步「收口」：先把本次运行产生的记录（反馈、执行量化、会话、运行判定）作为一个提交落下，再按声明的 workflow 合并与推送。只读运行跳过这一步并明说；即使本次运行没有产生记录，也仍然合并并推送已存在的东西并如实报告结果。

**Why this priority**: 用户的诉求正是「不需要每次都手动触发」。策略声明（US1）只是让行为可预测，不把它接进生命周期就没有解决任何事；两者都必须在 MVP 里。

**Independent Test**: 在一个夹具仓库里分别跑一次「产出工件 + 产生记录」的运行、一次「只读、无工件」的运行和一次「有工件、无记录」的运行，断言：第一种一次收口后主干上同时有工件提交与记录提交、远端主干已更新；第二种只打一行「本运行无可提交内容，跳过收口」；第三种仍完成合并与推送并在报告里列出被推送的内容。

**Acceptance Scenarios**:

1. **Given** 一次产出工件的运行，**When** wrap-up 执行到记录步骤之后，**Then** 产生一次收口：记录提交、合并、推送，报告里以一个提交哈希与远端/分支终态说明结果。
2. **Given** 一次只读运行（无工件、无记录），**When** wrap-up 执行，**Then** 跳过收口步骤并以一行说明，不创建空提交。
3. **Given** 一次产出工件但没有产生任何记录的运行，**When** 收口执行，**Then** 仍合并并推送既有内容，报告明确写出「本次收口未包含记录提交」。

---

### User Story 3 - 四种 workflow 模型各自得到正确的收口序列 (Priority: P2)

同一套收口逻辑对四种已声明的 workflow 模型都给出该模型自己的正确序列：单分支直接提交并推送主干；双分支在日常分支提交后按声明的同步/合并关系处理再推送；临时分支切出短命分支、合回主干、删除本地分支并推送主干；MAIN/PRE/DEV 三层沿声明的链逐级合并并逐级推送。

**Why this priority**: 这正是用户强调的「需要和 git workflow 相结合」。但它依赖 US1 的策略声明与 US2 的生命周期插入点先存在，因此排在 P2；对单个项目而言，只有它自己那一个模型的分支起作用。

**Independent Test**: 每种模型一个夹具仓库加一个假远端，跑一次收口后断言分支/远端终态：单分支只多一个提交且主干已推送；双分支提交落在日常分支且归档分支按声明关系更新；临时分支的本地短命分支已不存在且主干 FF 推进；三层模型两个中间分支各自前进且三处远端都已更新。

**Acceptance Scenarios**:

1. **Given** 一个声明 `Workflow model` 为 MAIN/PRE/DEV 三层的项目，**When** 收口执行，**Then** 序列为 DEV 提交 → DEV→PRE → PRE→MAIN → 逐级推送，且 MUST NOT 存在跳过 PRE 直接把 DEV 合入 MAIN 的步骤。
2. **Given** 一个声明为临时分支的项目，**When** 收口执行，**Then** 本地短命特性分支在合回主干后被删除，且只有在已合并的情况下才允许删除。

---

### User Story 4 - 失败即停并交出可复现的命令，而不是重试掩盖 (Priority: P2)

收口过程中的冲突、非快进、推送被拒都会让这一行停在第一处失败上：把状态与失败那一刻的确切命令写进本次运行的记录/状态脊，然后把该命令原样交回使用者，不做隐藏失败的重试循环，也不自动强推。

**Why this priority**: 无人值守的价值前提是失败不会被静默吞掉。它单独可用（只要收口存在），但只有在收口真正跑起来之后才能被观察到，故为 P2。

**Independent Test**: 在夹具远端预置一个让推送被拒的状态（远端分支被另一个提交推进），跑一次收口，断言退出为非零、记录里写明失败阶段与确切命令、远端未被强推覆盖，且没有第二次自动尝试。

**Acceptance Scenarios**:

1. **Given** 远端在上次 fetch 之后被推进，**When** 收口尝试推送，**Then** 它停下、记录「推送被拒」并给出确切命令，MUST NOT 自动 `--force` 或 `--force-with-lease` 重推。
2. **Given** 合并产生冲突，**When** 收口执行到合并步骤，**Then** 它停在冲突处、把冲突路径写上报告，后续推送步骤不再执行。

---

### User Story 5 - 破坏性动作与「别人的脏文件」边界不被收口吞掉 (Priority: P3)

收口遵守既有的确认门与归属纪律：强推、推送到只读上游、跨项目共享分支的破坏性操作仍按治理保留清单停下确认；提交一律按显式路径，绝不 `git add -A`；工作树里属于其他线的未提交文件被报为上游偏差，绝不扫进本次收口提交。

**Why this priority**: 这是安全底线而非新价值；但若缺席，前四个故事的自动化会把别人的工作与不可逆动作一起带进去，所以必须有，只是排在最后。

**Independent Test**: 在工作树里同时放入本特性产物与其他线的一个脏文件，跑收口，断言：本次提交只含显式路径列出的文件，脏文件仍未提交且报告里有一行上游偏差；`Closeout` 为 `commit+merge+push` 时对受治理动作（强推 / 只读上游 / 共享分支破坏）仍要求确认。

**Acceptance Scenarios**:

1. **Given** 工作树里存在本次运行未产出的脏文件，**When** 收口提交，**Then** 该文件不出现在提交里，并在报告中被列为上游偏差。
2. **Given** 收口推导出的所有步骤都是已声明 workflow 内的常规动作，**When** 收口执行，**Then** 它不停下等待确认；**And given** 某一步落在确认门清单内（强推、只读上游、共享分支破坏），**When** 执行到该步，**Then** 它停下确认。

---

### Edge Cases

- **托管块尚未填写**（`Workflow model` 仍是占位行）：收口 MUST NOT 猜测一个模型，报告「workflow 未声明」并把该步标为无法执行。
- **`Closeout remotes` 为空或缺行**：视为「无可推送远端」，`commit+merge+push` 退化为只做本地提交与合并，并在报告里明说推送被省略及其原因。
- **`Closeout remotes` 指向一个无法解析的远端名**：停下并报告该远端名，不猜测替代远端。
- **只读上游是唯一列出的远端**：拒绝执行推送步骤（治理保留），报告「唯一可选远端为只读上游」。
- **短命特性分支已存在于本地且属于其他线**：不得复用它，也不得删除它；停下报告命名冲突。
- **推送被拒后用户手动解决并重跑**：第二次运行以正常的收口路径继续，不产生「重试循环」语义（重跑是使用者的显式动作）。
- **无 git 仓库的目录**（standalone 技能部署）：收口步骤整体跳过并说明，不报错。
- **detached HEAD 或操作中途遗留的 merge 状态**：停下报告，不自动修复工作树。
- **`.gitexcludes` 存在且当前模型为临时分支**：收口遵循既有「谁接收代码、谁的规则说了算」处理，不新增第二套排除逻辑。

**Clarify 补记的 Edge Cases**（判据具名化，见 C-2 / C-5 / C-12）：

- **托管块已存在但 `Workflow model` 仍是占位行 `None yet.`（Bootstrap 尚未完成）**：收口 MUST NOT 猜测模型，也 MUST NOT 把任何远端当作可推送（此时唯一可解析的远端往往正是被标为只读上游的 `origin`）；报告「workflow 未声明」并按「无可推送远端」降级为本地提交与合并。
- **托管块整体缺失**（`.specify/workflow/git.md` 不存在，或 START/END 标记不成对）：MUST NOT 由收口代行 Bootstrap；报告「workflow 状态面不可用」并跳过收口的合并与推送两步，提交照常。
- **`Closeout remotes` 为空时的「呈现」形态**：呈现本地提交与合并的确切命令，并附一行「推送被省略：无已声明可推送远端」；呈现即报告，MUST NOT 因此转为阻塞等待。

## Requirements *(mandatory)*

### Functional Requirements

**策略声明（策略 owner）**

- **FR-001**: `.specify/workflow/git.md` 的托管块 MUST 新增一个收口策略声明（行名 [[STR-001]]），取值域为封闭集 [[STR-003]] / [[STR-004]] / [[STR-005]] / [[STR-006]]，缺省值为 [[STR-006]]；改值与默认值 MUST 只在该块内定义一次，其余位置只能指针引用。
- **FR-002**: 托管块 MUST 新增一个可推送远端声明（[[STR-002]]），供收口推导推送目标；[[STR-001]] 声明之外的任何位置 MUST NOT 参与推送目标判定。声明与既有的只读上游标记若冲突，收口 MUST 以「只读上游永不推送」为准并不受该声明推翻。
- **FR-003**: 托管块 MUST NOT 因本特性新增第二套分支表或任何与既有 `Workflow model` / 分支约定行重复的事实；收口的模型专属序列 MUST 由既有声明**推导**得出。
- **FR-004**: 托管块的整文件模板（`git-utils` 技能的 asset）MUST 携带上述两行的占位形态，使新项目 Bootstrap 时即得到可填写的收口声明，且必须填写模型专属行（不预设任一模型）。

**生命周期插入点**

- **FR-005**: `shared/workflow/artifact-commit-step.md` MUST 声明一个新的生命周期位置「收口」，位于既有的工件提交步骤与记录型 wrap-up 步骤（反馈 / 文档）之后，不复用也不移动既有步骤的次序。
- **FR-006**: 该 owner MUST 规定收口的**记录提交**语义：把本次运行产生的记录制品作为一个提交落下，与先前的工件提交分开、可归因；同一条记录 MUST NOT 同时出现在两个提交里。
- **FR-007**: 该 owner MUST 规定三个分叉：只读运行（无工件、无记录）跳过收口并一行说明；有工件无记录时仍合并并推送并如实说明；存在其他线未提交文件时按上游偏差报告而非扫入。
- **FR-008**: `artifact-commit-step.md` 现有的「本步不推送」边界 MUST 被本特性修订为「工件提交步骤本身不推送；推送属于其后的收口步骤」，使二者不再互相矛盾，且该修订 MUST 落在同一 owner 内。

**执行器（git-utils 作用域 A）**

- **FR-009**: `git-utils` 技能的 `SKILL.md` MUST 在作用域 A 声明一个具名 `closeout` 操作，并给出它在三类输入（块缺失或未填 / 块已填且无操作参数 / 块已填且有操作参数）下的定位，MUST NOT 引入第二个技能或第二个引擎。
- **FR-010**: `closeout` MUST 从托管块推导序列，覆盖四种模型的既有形态：单分支（主干提交 → 推送）、双分支（日常分支提交 → 按声明的同步/合并关系处理 → 推送）、临时分支（切出短命分支 → 提交 → 合回主干 → 删除本地分支 → 推送主干）、MAIN/PRE/DEV（DEV 提交 → DEV→PRE → PRE→MAIN → 逐级推送）。
- **FR-011**: 收口 MUST 在第一个失败处停止（冲突 / 非快进 / 推送被拒），把失败阶段与确切命令写入本次运行的记录或状态脊，并把该命令原样交回；MUST NOT 存在隐藏失败的重试循环。
- **FR-012**: 收口 MUST NOT 自动强推；任何强推需求 MUST 按确认门停下确认，且只允许 `--force-with-lease` 形态（禁止 `--force`）。
- **FR-013**: 收口 MUST NOT 推送托管块标为只读上游的远端，即使 `Closeout remotes` 或调用方指令把它列入。
- **FR-014**: 收口 MUST NOT 以 `git add -A` 或等价的全量暂存提交；MUST 按显式路径提交，并把工作树中其他线的未提交文件报为上游偏差。
- **FR-015**: 临时分支模型下，本地短命特性分支 MUST 仅在已合并后才删除；名字冲突或已属其他线时不复用、不删除，停下报告。
- **FR-016**: 在非 git 仓库或 standalone 技能部署下，收口 MUST 整体跳过并说明，MUST NOT 报错中断。

**标准授权与确认门**

- **FR-017**: `commit+merge+push` MUST 作为**项目级标准授权**（托管块中的一个值）生效，覆盖收口序列内已声明 workflow 的常规动作；它 MUST NOT 被理解为对确认门清单内动作（强推、只读上游推送、跨项目共享分支破坏）的全局豁免。
- **FR-018**: 既有确认门 owner（`shared/guidelines/confirmation-gates.md`）MUST 保持为破坏性动作与治理保留清单的唯一真源；本特性的任何面 MUST NOT 复制其清单纯文本，只能指针引用。
- **FR-019**: [[STR-001]] 的策略值为 [[STR-006]]（缺省）或该行缺失时，收口 MUST 呈现待执行命令并等待用户决定，MUST NOT 自动执行推送；[[STR-003]] 是唯一允许自动推送的取值。

**统一入口与投影**

- **FR-020**: 无人值守机制（SDD 驱动者的收尾合并步、周期性维护、反馈消化，以及将来的自动运行）MUST 调用同一个收口步骤；驱动者现有的合并/推送动作 MUST 收敛为它的一个实例，MUST NOT 保留为第二个机制。
- **FR-021**: 技能侧与命令侧的 wrap-up 编译面（探针注册表与 `probe-utils.py --action compile-embeds` 的渲染产物）MUST 表达这一新步骤，MUST NOT 手写编译面正文；新增行 MUST 与既有的 wrap-up 处理器次序不冲突。
- **FR-022**: 面向使用者的指令面（`templates/instructions-template.md` 与其运行时投影）的 `## Git Workflow` 段落 MUST 保留其现有「指针而非复述」形态，仅在有需要时增加对收口步骤的指针；MUST NOT 在其中罗列收口规则。

**防漂移与验证**

- **FR-023**: 契约测试 MUST 覆盖：托管块的两行声明存在性与取值域、四种模型的序列推导、`artifact-commit-step.md` 与其 embedder 的指针存在性、以及「不存在第二套分支表」结构不变量。
- **FR-024**: 每个模型 MUST 有一个夹具仓库加一个假远端，断言收口后的分支与远端**终态**（分支存在性、HEAD 位置、提交归属），而非只断言命令串。
- **FR-025**: 本特性 MUST 在真实仓库上提供一次干跑证据（不推送），证明当前声明（临时分支 + `Closeout`）推导出的序列与本仓实际 workflow 一致。
- **FR-026**: 任何「收口后其余行为不受影响」一类的稳定性断言 MUST 按 `shared/guidelines/closed-set-claims.md` 给出基线参照物、比较单元与允许差异集来源，否则 MUST NOT 作为验收依据。

**非目标（由声明排除，审计时按此判定越界）**

- **FR-027**: 本特性 MUST NOT 新增 `/speckit.*` 命令、守护进程或调度器、第二套分支 registry、自动强推、代码托管平台 PR/MR 自动化，亦 MUST NOT 让托管块新增第二张分支表。
- **FR-028**: 收口的记录提交 MUST NOT 直接写入按 entry 一文一件的记录文件本身，MUST 改为写入一个收口回执（close-out receipt）文件，与该文件同属一个共享交付根、同样一文一件；回执 MUST 记录本次提交涵盖的每一条记录文件的路径、动作、占用它的提交哈希，以及本类记录所用引擎的读法指针。对该引擎，回执即这条记录的消费生命周期终点，MUST NOT 同时满足「记录仍可读」与「提交删除它」两种处理（澄清依据见 C-10(a)/A19）。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 shell/git 运行时、既有 Python 引擎与既有测试运行器。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | `git` 命令行的本地分支/合并/推送能力（收口序列的实际执行面） | signed-contract | 宿主环境提供（本仓只消费，不打包） | 本特性实现期实测记录 `git --version` 输出，作为实现的运行时前提 | `pyproject.toml` | `/speckit.implement` 收口阶段在宿主 `git` 上跑通四个模型夹具仓库 | FR-010, FR-011, FR-012, FR-015 | EP-001 |
| RS-002 | 托管块声明读取（本特性不改引擎；读取方是 `git-utils` 技能流程与契约测试） | in-scope | 本特性自身修订的 `git-utils` 技能与契约测试 | 不适用（无外部版本面） | `skills/external/git-utils/SKILL.md` | `tests/contract/` 下的收口契约测试在 `>=3.8` 解释器上通过 | FR-001, FR-002, FR-003, FR-009, FR-023 | EP-002 |
| RS-003 | `pytest` 测试运行器（契约测试与夹具仓库断言） | signed-contract | CPython/pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增第三方依赖 | `pyproject.toml` | `pytest -m contract` 通过，夹具仓库测试在 `>=3.8` 解释器上执行 | FR-024, FR-025 | EP-002 |

> RS-001 的 `Contract` 列只声明本仓 Python 依赖面；`git` 由宿主环境提供，不列为 Python 依赖。

### Key Entities *(include if requirement involves data)*

- **收口策略声明（Close-out declaration）**: 托管块内的两行——策略取值（封闭四值）与可推送远端集合；唯一存在于 `.specify/workflow/git.md`。
- **收口序列（Close-out sequence）**: 由 workflow 模型推导出的有序动作集合（提交 → 合并 → 推送，含模型专属中间步）；不是存储实体，是每次收口的投影。
- **记录提交（Records commit）**: 一次运行产生的记录制品集合在收口时形成的单个提交，与工件提交互不重叠。
- **收口报告（Close-out report）**: 每次收口的终态说明——提交哈希、合并结果、推送目标与结果，或停下来的失败阶段与确切命令。
- **夹具仓库 + 假远端（Fixture repo & fake remote）**: 验证用的每模型一个最小仓库与本地假远端，用于断言分支/远端终态。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 四个 workflow 模型各有一个夹具仓库收口后达到声明的终态（分支存在性、HEAD、提交归属逐项断言通过），四个全绿。 **Path**: final
- **SC-002**: 托管块两行声明（[[STR-001]] 的四个取值 [[STR-003]] / [[STR-004]] / [[STR-005]] / [[STR-006]]，与 [[STR-002]]）的存在性、取值域与缺省 [[STR-006]] 由契约测试钉住；把策略值改成非法值或删掉该行时，测试转红。 **Path**: final
- **SC-003**: 收口的失败路径可判定：在推送被拒与合并冲突两个夹具里，收口以非零退出、写出失败阶段与确切命令、且远端状态未被强推改写；两个夹具都转绿，且把「自动重试」注入实现时转红。 **Path**: final
- **SC-004**: 破坏性边界未被扩大：以既有 `scan-confirmation-gates.py` 读数为对象，本特性落地后确认门条数不减少，且不存在任何面复制确认门清单纯文本（结构不变量断言）。本条是比较型封闭清单声明，基线取**本特性第一个实现提交之前**的扫描读数；2026-11-09 实测基线为 `blocking confirmation gates: 27`（`destructive: 20` / `governance_kept: 7`，`violations: 0`）。（澄清判据收紧见 C-11a。） **Path**: final
- **SC-005**: 无人值守入口收敛为单一机制：驱动者的收尾合并步、周期性维护与反馈消化都指向同一个收口 owner（指针存在性断言），且仓库中不存在第二个收口实现。 **Path**: final
- **SC-006**: 本仓真实仓库上的一次干跑不推送、不改写远端，并产出与当前声明一致的序列证明（载于干跑记录，不另产核对产物；见 C-9a）。 **Path**: supporting
- **SC-007**: 只读运行与「有工件无记录」两个分叉的行为各自被一个夹具断言到（跳过时有一行说明、不产生空提交；缺记录时仍合并推送并如实报告）。 **Path**: supporting
- **SC-008**: SC-004 的封闭清单声明可判定：基线参照物（上述 27 条读数）、比较单元（确认门条的集合，按名比较）、允许差异集来源（`shared/guidelines/closed-set-claims.md`）三者都在测试内具名，且把一条确认门删去或把清单纯文本复制进任一面时测试转红。（澄清新增，见 C-11a。） **Path**: final

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/contract/` 下的四模型夹具测试；每个模型记录命令、退出码、夹具仓库最终 `git log --graph --oneline` 与 `git ls-remote <fake-remote>` 输出到 `test-evidence/`。
- **SC-002 Source**: 契约测试读取 `skills/external/git-utils/assets/git-workflow-block.md` 与 `.specify/workflow/git.md` 托管块，断言声明行与取值域；变异验证（手工改成非法值 / 删除行）记录在 `test-evidence/`。
- **SC-003 Source**: 两个失败夹具（推送被拒、合并冲突）的实测记录：退出码、报告中的失败阶段与命令、以及 `git ls-remote` 前后对照证明远端未被强推改写。
- **SC-004 Source**: `python .specify/scripts/python/scan-confirmation-gates.py` 的落地前后读数对比（条数不减少），加上一个结构不变量断言（不给各面复制清单文本）。
- **SC-005 Source**: 对 `skills/external/sdd-loop-driver/`、周期性维护与反馈消化 skill 的指针存在性断言；`rg` 检索「第二实现」的负向断言。
- **SC-006 Source**: 本仓干跑命令、退出码与推导出的序列打印，记录在 `test-evidence/`；远端 `ls-remote` 前后对照为「未变」。
- **SC-007 Source**: 两个 wrap-up 分叉夹具的实测记录（只读运行的一行说明、空提交不发生的断言；缺记录运行的合并推送与报告文本）。
- **SC-008 Source**: SC-004 的同一个契约测试内的三个具名元素（基线读数、按名比较的确认门集合、`closed-set-claims.md` 的允许差异集来源），加上两次变异实测（删一条门 / 复制清单纯文本进一面）转红的记录，落在 `test-evidence/`。
- **C-10a / C-18a / C-19a 判据**（澄清新增，取代「文档级不变量」的软断言）：对 `.specify/skills/sdd-loop-driver/SKILL.md` 与 `skills/external/git-utils/SKILL.md` 各做一次**合成变异**（在内存副本里插入一个 `git push origin <branch>` 形态的示例命令 / 一处 `repo.git.add("-A")` 等价调用），断言同一测试转红；不修改树上的任何文件。依据：`docs/reference/history/00-cross-cutting-lessons.md` §「盲检查」——「grep 命中的是文档措辞，不是被查的东西在运行」，只看措辞的绿不构成证据。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"Closeout"` | FR-001, FR-002, SC-002 |
| `STR-002` | `"Closeout remotes"` | FR-002, SC-002 |
| `STR-003` | `"commit+merge+push"` | FR-001, FR-019, SC-002 |
| `STR-004` | `"commit+merge"` | FR-001, SC-002 |
| `STR-005` | `"commit-only"` | FR-001, SC-002 |
| `STR-006` | `"ask"` | FR-001, FR-019, SC-002 |

## Clarifications

<!-- 由 /speckit.clarify 填充：- Q: <question> → A: <answer> -->

### Session 2026-11-09 (requirements, 无人值守)

本阶段无人值守运行：全部疑点由本代理自行裁决并记录于此（也是 Assumptions 的来源），依据是设计简报 + 仓库实测 + 相邻特性（089/090）惯例。**未向用户提问，未改写任何已实现文本。**

### Session 2026-11-09 (clarify, 无人值守)

本会话模式 **A（post-requirements）**，目标文件本文件。**只写本特性规格面**，MUST NOT 触碰任何 owner / 技能 / 镜像 / 测试（Two Hats：仍是 requirements 之后的规格阶段，实现要等 plan→implement 的门）。**未向用户提问；每条裁定都给落点；未改写任何已实现文本。**

**前置实测**（澄清的事实基座，全部本次实跑，命令与输出原文见 `test-evidence/clarify-gates.txt`）：

| 读数 | 值 |
|------|-----|
| `python .specify/scripts/python/validate-requirements.py <本文件>`（改前） | `status: ok`，6 项检查全 pass，0 error / 0 warning，34 definition rows / 6 shared strings |
| `python .specify/scripts/python/scan-confirmation-gates.py` | `blocking confirmation gates: 27`（destructive 20 / governance_kept 7），`violations: 0` |
| `git --version` | `git version 2.43.5` |
| `python -m pytest --version` | `pytest 8.4.2` |
| `pyproject.toml:5` | `requires-python = ">=3.8"` |
| 记录文件在 git 内的跟踪状态 | `git ls-files .specify/memory/exec-quant/records` → 242 个 tracked；`git ls-files .specify/memory/feedback` → 376 个 tracked |

- **C-1（`feature-ref.md` 是否存在）** → A: **不存在；本阶段创建**（唯一的 clarify 新产物）。`overlap-check.py` 的当前特性交付面只来自 `feature-ref.md`（回退 `tasks.md`/`plan.md`），后者在本阶段均不存在，故没有 `feature-ref.md` 时该门无论本特性真实交付面有多大都会返回 `clear (note: current feature has no declaration artifact)`——一次**空洞的绿**。另：`overlap_adjudication` 的处置第 1–2 步（「裁决结果 MUST 同时写入…相关 spec 的 Clarifications/**feature-ref 注记**」）本身就以 `feature-ref.md` 为回执面；兄弟特性 088 即用它承载该注记。**落点**：新建 `feature-ref.md`（含交付路径总表）。
- **C-2（workflow 未声明时，PR-自建仓库里 `origin` 是唯一远端而它又是只读上游）** → A: **这是 FR-016（非 git 仓库）之外的第二条降级轴，必须显式补入。** 实测本仓 `Workflow model` 已填写（临时分支），但该值为占位行 `None yet.` 的**新 Bootstrap 项目**必然出现；此时 `Closeout remotes` 要么为空（Edge Case 已覆盖，退化为本地提交+合并），要么只能解析到只读上游 `origin`。后者行为未定义，而 Edge Case「只读上游是唯一列出的远端」只覆盖了「已声明模型」一种语境。裁定：**未声明模型时不得猜测模型，也不得把任何远端当作可推送**；报告「workflow 未声明」并按「无可推送远端」降级。**落点**：Edge Cases 新增两条（见文末「Clarify 补记的 Edge Cases」）、A13。
- **C-3（`Closeout: ask` 在无人值守下的行为：呈现还是阻塞）** → A: **呈现即报告，不阻塞。** 与状态脊 `direction_contract` 的 HR1（U4 通过即派发下一阶段，绝不问「继续」）一致：等待是下一次用户回合的事。**落点**：FR-019、A7 不变；此处补记它与 HR1 的一致性来源。
- **C-4（远端名与只读上游的排除机制）** → A: **按能力标记排除，不按名字。** 本仓托管块把 `origin` 标为*上游只读参照*，而 A3 已登记 `execute-commands.md` 的示例一律写 `git push origin <branch>`——那正是「按名字」的写法。收口 MUST 只从 `Closeout remotes` 取推送目标，并对每个目标复核该远端在托管块中的角色 vs 调用方指令，冲突时只读优先。**落点**：FR-002、FR-013 已表达，此处确认判据（复核而非复制），A14。
- **C-5（`Workflow model` 为占位行时，占位符是列出的哪个字面量）** → A: **`None yet.`**。实测 `tests/contract/test_git_workflow_instructions_block.py::test_state_file_carries_the_managed_block` 断言块内含 `**Workflow model**:` 与字面量 `None yet.`（占位判定依据），`references/instructions-lookup.md` 同。**落点**：Edge Case 1 的判据具名化。
- **C-6（`closeout` 操作在 git-utils 的 Phase 0 判据表里如何落位）** → A: **不改判据表，只做具名操作。** 实测 `SKILL.md` § Phase 0 的三行表（Bootstrap / 全维度体检 / 定向收敛）由「块已填写」与「有操作参数」两轴决定；收口是**有操作参数**的一类，走「定向收敛（Execute）」行，与操作 A–G 同类，故 FR-009 的「三类输入」正是这两轴的投影。**落点**：FR-009、A15。
- **C-7（`closeout` 需要的三个事实在托管块里由哪一行承载）** → A: **不新增行第三行以上；每个事实都在块内已有归属。** 合并形态（ff / merge）与截断与否是 FR-003 明令禁止复制的「模型专属事实」，故由**既有 `Workflow model` 行的模型语义推导**，不在块内新增行；`Closeout remotes` 空/缺行时退化为「无可推送远端」（既有 Edge Case）；块缺失（文件不存在或标记不成对）走 Bootstrap，不执行收口。**落点**：A16、FR-003 不变。
- **C-8（`artifact-commit-step.md` 的「本步不推送」边界改为「推送属于其后的收口步骤」后，验证面从哪里来）** → A: **没有既有测试锚定那句话，需要新契约测试。** 实测 `grep -rln "does not push" tests/` 只命中 `tests/contract/test_sdd_loop_driver_wp_coordination.py`，且该命中是 VI-14 断言 `wp_driver_sim` 的 integration 结果（`push: False`），**不是** `artifact-commit-step.md` 的文本。故 FR-008 的验证 MUST 由本特性自己的契约测试承担。**落点**：FR-023 的覆盖项之一在 plan 阶段具化为独立断言。
- **C-9（SC-006 的「序列证明」是否需要新产物）** → A: **不需要。** 把证明当成一次 dry-run **记录**而不是一份**归档核对报告**，可避免 FR-021（编译面不得手写）与 SC-004（不新增面的重复）的双重风险，也不给仓库添第二套文档。**落点**：SC-006 就地补注。
- **C-10（记录提交是否直接改写记录文件——最大的一处欠指定）** → A: **改为回执文件，MUST NOT 直接改写记录文件。** 见下方分项：
  - **(a) 事实冲突**：FR-006 的「同一条记录 MUST NOT 同时出现在两个提交里」+ A4 的「四类记录合并为一个提交」× 记录文件是**一文一件**、被 git 跟踪、且由 `sanitize-materials` 的 `record-retention` 泳道管理**删除**（`record-retention.py --action scan|distill`；「consume → receipt → retire；没有回执就不得删除；30 天宽限」）。若收口把同一文件路径再提交一次，就是第二个提交持有同一条记录；若收口删除它，则删掉的是同时被引擎读取的记录，且必须自造一套与 `record-retention` 平行的回执。三条读法各自都违反一条既有规则——这是**裁定点**，不是纠正点。
  - **(b) 裁定**：收口写入**回执**（一条收口一个文件、一文一件、时间戳命名），内容 = 涵盖的每条记录路径 + 动作（含入 / 保持 / 移交消费）+ 占用它的提交哈希 + 该记录类所用引擎的**读法指针**（不复制读法正文）。对该引擎，回执即这条记录的消费生命周期终点。**理由**：满足 FR-006 与 A4 的全部约束，不新造引擎，不删可读记录，不与 `record-retention` 争写同一文件。
  - **(c) 落点**：**FR-028 新增**、SC-001 的「提交归属」断言对象改为回执 + 记录路径、A4 补注、A19。
  - **(d) 为何不在本阶段就地修 FR-006**：FR-006 的意图（记录可归因、不重复）未被推翻，被推翻的是「记录 MUST 以文件改写的方式落进提交」这条**实现读法**；按 Fast Fail，选择读法 = 裁定，已在回执读法上闭合，并以 FR-028 承载，不改 FR-006 的意图句。
- **C-11（哪些判据目前是「机器绿但证明不了什么」）** → A: **三处，全部就地收紧。**
  - **(C-11a) SC-004 是封闭清单声明，现有文本缺三元素**：`shared/guidelines/closed-set-claims.md` 要求基线参照物、比较单元、允许差异集来源三者具名，而 SC-004 原文只说「条数不减少」。就地补入实测基线（27 / 20 / 7 / 0）与三者，并新增 **SC-008** 把「可判定」本身立为验收项（删一条门或复制清单进任一面时转红）。另实测发现 `tests/contract/test_wrap_up_wording_gate_safe.py::test_confirmation_gate_budget_unchanged` 以 `== 27` 钉住总数——**本特性的门若动到这个数，那条既有测试会先红**，这属于 plan 阶段必须处置的既有 pin，登记为 A20。
  - **(C-11b) SC-001 的「提交归属」在 C-10 裁定后必须换对象**：否则会断言一个按裁定根本不会发生的文件改写。
  - **(C-11c) FR-003 / FR-009 / FR-027 的「不存在第二套分支表 / 第二实现 / `git push origin`」目前只能靠人读文本**：既有教训明写「grep 命中的是文档措辞，不是被查的东西在运行」。就地补入**合成变异**判据（在内存副本里注入一处反例，断言同一测试转红；不改树上文件），避免这三条变成永远为真的空声明。
- **C-12（`Closeout remotes` 为空时「呈现待执行命令」呈现什么）** → A: **呈现本地提交与合并的命令，加上一行「推送被省略：无已声明可推送远端」。** 与 A7「呈现即报告」同形；不得因为呈现而改走阻塞。**落点**：Edge Case 2 补注。
- **C-13（远程短命分支是否删除）** → A: **不在远端创建短命分支，故无远程删除**（A5 已裁）。这里补记它的**推导链**：临时分支模型把短命分支当作本地工作脚手架、推送的是主干（`git.md` Feature branch convention 行），若在远端建分支则收口会引入一个破坏性动作（远程删分支）进无人值守路径，与 FR-012 / confirmation-gates 的保留清单相抵触。**落点**：A5 补注。
- **C-14（驱动者 U6 的「合并」是否等于本特性的 push）** → A: **不是；U6 只是本 owner 在无 `Closeout` 授权下的一个实例形态。** 实测 `decomposition-model.md:244` 明写该层「does not push, force-merge, or auto-merge」、`stage-prompts.md:455` 的 `integration_result` 记录只要求 merged 提交可从 HEAD 到达。故 FR-020 的收敛是**表述收敛**：U6 变成「按本 owner 取序列、在 `Closeout=ask` 下止于本地合并」的执行，MUST NOT 让 U6 凭空获得推送权。**落点**：A9 补注、FR-020 的解释口径。
- **C-15（`instructions-template.md` 的 `## Git Workflow` 段是否要加收口指针）** → A: **只加一行指针，不罗列规则（FR-022 已定），且本阶段不改。** 实测该段现有措辞已把 `close-out` 列为触发无人值守提交/合并/推送的机制之一（`templates/instructions-template.md:277` 与 `.specify/instructions.md:299` 逐字相同），说明该面已经指向本特性；真正缺的是「收口步骤在哪里」的具体指针，归 plan 的实现任务。

- **C-16（跨特性重叠预检：两次判定的差，以及 36 条 overlap 的归属裁决）** → A: **改前是空的绿，改后是 36 条与已完成线的重叠、零条与活动线的重叠；逐路径归属裁决如下，plan 可派发。** 实测（证据 `test-evidence/overlap-check-clarify.json`，改前读数见 `clarify-gates.txt`）：
  - **改前**：`decision=clear, checked=1, overlaps=0, note="current feature has no declaration artifact"` —— 只比了本特性自己，什么都没比。
  - **改后**：`decision=overlap, checked=82, overlaps=36`。36 条覆盖 5 条路径：`templates/instructions-template.md`（18 条，全部 `same-path`）、`shared/definitions/probe-definitions.md`（12 条 `same-path` + 2 条 `nested-path`，对手分别是 089 / 090 的 `shared/definitions` 目录声明）、`skills/external/git-utils/SKILL.md`（3 条，对手 059 / 062 / 063）、`shared/workflow/external-dispatch-recipes.md`（1 条，对手 088）、`shared/workflow/artifact-commit-step.md`（0 条）。
  - **归属裁决（§7.4-1）**：四份共享文档（probe 注册表、工件提交步骤、派发配方、指令模板）**按设计就是多线共写的注册面**，历史上已被十余条已完成线编辑，没有任何一条拥有它们；本特性的编辑是**追加式**（新增一行 handler / 新增一节 / 新增一行指针），沿用既有约定，owner 保持为文档本身。唯一特性专属的碰撞是 `git-utils/SKILL.md`，其中对手 059 / 062 / 063 三条线均已 closed，且本特性在作用域 A 内**新增一个操作名**，不与它们的编辑争同一行。
  - **活动线判据**：`line-registry.py --action list --active --format json` 实测返回 `[]`——本特性此刻是唯一在跑的线，36 条全部是与**已完成**线的历史叠加，不是并发写冲突。故无需为另一条活动线写 `overlap_adjudication`，只在本文件与 `feature-ref.md` 记裁决（本仓没有第二条活动线状态脊可写）。
  - **为何不退化成「稍后可能不冲突」**：§7.4-4 明令禁止跳过；本裁决不是跳过，而是把每条路径的 owner 写明、把活动线集合实测为空、并把「实现前重跑」写成 implement 的必做项（feature-ref § Adjacency）。
  - **落点**：`feature-ref.md`（交付面声明 + Adjacency 段）、本裁定、状态脊 `gates`。

**本阶段对规格面的可判定净变化**：FR 27 → 28（新增 FR-028）、SC 7 → 8（新增 SC-008）、3 条 SC 就地补注（SC-004 / SC-006 / SC-008 source）、3 条 Edge Case 补入（未声明模型 / 托管块缺失 / 空远端呈现形态）、Assumptions 12 → 21（A13–A21）、1 份新产物 `feature-ref.md`、1 次跨特性重叠裁决（C-16）。

## Assumptions

- **A1（步骤次序：收口在反馈/文档之后，而不是取代它们）**: 设计简报要求把收口放在 Feedback/Documentation 之后，而 `artifact-commit-step.md` 现文规定工件提交**先于**这两者。两条规则并不冲突：工件提交 → 反馈/文档（产生记录）→ 收口（提交记录 + 合并 + 推送）。本规格按此落地；FR-008 专门把「该步不推送」修订为「推送属于收口」以消除字面矛盾。
- **A2（单一 owner 内闭合，不新增文档）**: 收口的语义归 `shared/workflow/artifact-commit-step.md`（既有 owner），策略声明归 `.specify/workflow/git.md` 托管块（既有 owner），操作归 `git-utils` 作用域 A（既有 owner）。本特性不新建任何文档/技能/引擎——这是宪法 Principle IX 与 XIV 的直接要求。
- **A3（远端名不写死）**: 本仓的 `origin` 是**上游只读**，`github`/`gitlab`/`gitee` 是同一 fork 的三镜像；而 `skills/external/git-utils/references/execute-commands.md` 中的示例命令一律写 `git push origin <branch>`。这是**文档级的既有不一致**，本特性 MUST NOT 在收口中假定任何远端名：推送目标只能来自 `Closeout remotes`，只读上游以能力标记（不是名字）排除。该不一致登记为框架观察，交由 plan/implement 处理，本阶段不修改既有 references。
- **A4（「记录提交」= 一个提交，不是逐类一个）**: 反馈 / 执行量化 / 会话 / 运行判定四类记录合并为收口时的一个提交，理由是归因单位是「一次运行」。若实现期发现某类记录由独立引擎在收口之后才落盘，按 Fast Fail 的「纠正」就地调整提交边界并在回传披露。**（clarify 补记，见 C-10）** 「一个提交」的承载物是**收口回执**，不是对记录文件本身的再写或删除——见 FR-028 与 A19。
- **A5（临时分支的远端分支不删除）**: 设计简报开放问题 2 裁为「不在远端创建短命分支，因此收口无需远程删分支」。临时分支模型的短命分支只在本地存在，合回主干后删本地；推送的是主干。这样避免了远程分支删除这一破坏性动作进入无人值守路径。
- **A6（提交粒度：每次收口两个提交）**: 设计简报开放问题 1 裁为「两个提交」——工件先行（既有步骤，保归因），记录在收口时一次落下。若某次运行不产生记录，则只有一个提交，FR-007 已覆盖。
- **A7（`Closeout: ask` 在无人值守下的行为）**: 缺省 `ask` 意味着无人值守运行**不会**自动推送——它在收口步骤呈现命令并以一行说明结束，而不是阻塞等待。这与既有的「无人值守不征求继续」一致：呈现即报告，等待是下一次用户回合的事。
- **A8（不新增脚本）**: 收口序列由技能流程 + 契约测试判定，不引入第二个可执行引擎脚本；若实现期证明需要确定性推导，以扩展现有 Python 工具的方式落地，且必须在其 `--help` / `--version` 上满足宪法 Principle XXI（Script Interface Contract）。
- **A9（驱动者 U6 收敛为实例）**: 驱动者当前在 U6 做本地合并（不 push）。本特性将其表述为该 owner 的一个实例；驱动者**不新增**推送行为，除非其线所声明的 `Closeout` 允许。状态脊 `direction_contract` 的 `forbidden_drifts` 已禁止自动强推与推只读上游，二者一致。
- **A10（夹具仓库的落点）**: 夹具仓库建在受制裁的临时根下（`tempfile.TemporaryDirectory()`，属 `temp-directory-discipline.md` §5 例外），不落仓库内目录，避免第二套目录治理。
- **A11（本特性自身的收口受同样约束）**: 本阶段的提交只含本特性产物、按显式路径、不 push——即在收口机制落地之前，本特性自己的运行仍按手工步骤完成，并把这件事实记录在此以免被误读为「机制已生效」。
- **A12（术语）**: 中文统一用「收口」（close-out），避免与「收尾 / 合并 / 结束」混用；英文统一 `close-out`（连字符），与既有 `git.md` 措辞一致。
- **A13（未声明 workflow 是第二条降级轴，不是 FR-016 的重复）**: FR-016 覆盖「没有 git 仓库」，A13 覆盖「有 git 仓库但没有已声明的 workflow」以及「托管块整体缺失」。三种状态各自有独立处置，MUST NOT 合并成一句「跳过收口」。（C-2 / C-7）
- **A14（只读上游按能力排除，不按名字）**: 托管块对远端角色的标注（`origin` = 上游只读参照）是判据来源；`Closeout remotes` 里出现该名字时只读优先。A3 登记的 `execute-commands.md` 示例写死 `git push origin` 是既存文档不一致，仍归 plan/implement 处置，本阶段不改 references。（C-4）
- **A15（`closeout` 落在 git-utils 已有的「定向收敛」作用域，不是第四种模式）**: Phase 0 的两轴判据表不变，`closeout` 是「块已填写 且 有操作参数」时的具名操作，与操作 A–G 同类。（C-6）
- **A16（不在托管块内新增第三类事实行）**: 合并形态 / 冲突处置 / 截断规则均**由模型语义推导**，不写成块内新行——否则就是 FR-003 禁止的「与既有声明重复的事实」。（C-7）
- **A17（不经远端托管平台读外部事实）**: 收口与验证完全不访问 GitHub/GitLab/Gitee API，也不做分支保护、PR/MR 状态判断；验收只在 `git` 命令、夹具仓库与假远端上进行。既有的「推送被拒」夹具即这一维度的判据载体。（澄清自设计简报边界推出）
- **A18（钉住落点不在本阶段）**: 本阶段只钉住规格面。`closeout` 的契约测试、SC-008 的变异验证、`feature-ref.md` 的交付路径总表均属 plan/implement；clarify 不产生实现、不新增测试、不改任何 owner 文件。
- **A19（回执即消费终点，不与记录保留泳道争写）**: 记录文件由 `sanitize-materials` 的 `record-retention` 泳道在「存有回执 + 30 天宽限」后退役；收口因此只**新增**回执，不删除、不改写 `exec-quant/records/`、`memory/feedback/` 下的任何文件。回执本身按 Concurrent Development Safety 的「一文一件 + 时间戳命名」落盘。（C-10）
- **A20（SC-004 的按名比较不得与既有 pin 互相拉扯）**: 已实测 `tests/contract/test_wrap_up_wording_gate_safe.py` 以 `== 27` 钉住确认门总数，注释亦把该数称为「owner fact = live scan total」。本特性的契约测试 MUST 断言「集合不缩小」而不重新断言总数常量；若实现期确需改动该计数，先由该 pin 的 owner 重裁，MUST NOT 顺手改数。这是 clarify 阶段发现的**既有 pin 张力**，移交 plan。（C-11a）
- **A21（本特性的自指：C-1 的绿是「空的绿」这一发现本身）**: 本阶段一旦创建 `feature-ref.md`，`overlap-check.py` 的「无声明」分支就失效，该门从此检查本特性声明的交付面——这正是 C-1 所述缺口的**纠正性**修复。MUST 在证据中记录改前/改后两次判定，避免用改后的 `clear` 反推改前也成立。
