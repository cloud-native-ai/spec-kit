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

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时——它消费既有的 shell/git 运行时、既有 Python 引擎与既有测试运行器。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | `git` 命令行的本地分支/合并/推送能力（收口序列的实际执行面） | signed-contract | 宿主环境提供（本仓只消费，不打包） | 本特性实现期实测记录 `git --version` 输出，作为实现的运行时前提 | `pyproject.toml`（本仓 Python 包的依赖面；`git` 按宿主提供，不列为 Python 依赖） | `/speckit.implement` 收口阶段在宿主 `git` 上跑通四个模型夹具仓库 | FR-010, FR-011, FR-012, FR-015 | EP-001 |
| RS-002 | 托管块声明读取（本特性不改引擎；读取方是 `git-utils` 技能流程与契约测试） | in-scope | 本特性自身修订的 `git-utils` 技能与契约测试 | 不适用（无外部版本面） | `skills/external/git-utils/SKILL.md` | `tests/contract/` 下的收口契约测试在 `>=3.8` 解释器上通过 | FR-001, FR-002, FR-003, FR-009, FR-023 | EP-002 |
| RS-003 | `pytest` 测试运行器（契约测试与夹具仓库断言） | signed-contract | CPython/pytest 上游（本仓只消费） | `pyproject.toml` 中既有的 `pytest` 依赖声明；本特性零新增第三方依赖 | `pyproject.toml` | `pytest -m contract` 通过，夹具仓库测试在 `>=3.8` 解释器上执行 | FR-024, FR-025 | EP-002 |

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
- **SC-004**: 破坏性边界未被扩大：以既有 `scan-confirmation-gates.py` 读数为对象，本特性落地后确认门条数不减少，且不存在任何面复制确认门清单纯文本（结构不变量断言）。 **Path**: final
- **SC-005**: 无人值守入口收敛为单一机制：驱动者的收尾合并步、周期性维护与反馈消化都指向同一个收口 owner（指针存在性断言），且仓库中不存在第二个收口实现。 **Path**: final
- **SC-006**: 本仓真实仓库上的一次干跑不推送、不改写远端，并产出与当前声明一致的序列证明。 **Path**: supporting
- **SC-007**: 只读运行与「有工件无记录」两个分叉的行为各自被一个夹具断言到（跳过时有一行说明、不产生空提交；缺记录时仍合并推送并如实报告）。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: `tests/contract/` 下的四模型夹具测试；每个模型记录命令、退出码、夹具仓库最终 `git log --graph --oneline` 与 `git ls-remote <fake-remote>` 输出到 `test-evidence/`。
- **SC-002 Source**: 契约测试读取 `skills/external/git-utils/assets/git-workflow-block.md` 与 `.specify/workflow/git.md` 托管块，断言声明行与取值域；变异验证（手工改成非法值 / 删除行）记录在 `test-evidence/`。
- **SC-003 Source**: 两个失败夹具（推送被拒、合并冲突）的实测记录：退出码、报告中的失败阶段与命令、以及 `git ls-remote` 前后对照证明远端未被强推改写。
- **SC-004 Source**: `python .specify/scripts/python/scan-confirmation-gates.py` 的落地前后读数对比（条数不减少），加上一个结构不变量断言（不给各面复制清单文本）。
- **SC-005 Source**: 对 `skills/external/sdd-loop-driver/`、周期性维护与反馈消化 skill 的指针存在性断言；`rg` 检索「第二实现」的负向断言。
- **SC-006 Source**: 本仓干跑命令、退出码与推导出的序列打印，记录在 `test-evidence/`；远端 `ls-remote` 前后对照为「未变」。
- **SC-007 Source**: 两个 wrap-up 分叉夹具的实测记录（只读运行的一行说明、空提交不发生的断言；缺记录运行的合并推送与报告文本）。

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

## Assumptions

- **A1（步骤次序：收口在反馈/文档之后，而不是取代它们）**: 设计简报要求把收口放在 Feedback/Documentation 之后，而 `artifact-commit-step.md` 现文规定工件提交**先于**这两者。两条规则并不冲突：工件提交 → 反馈/文档（产生记录）→ 收口（提交记录 + 合并 + 推送）。本规格按此落地；FR-008 专门把「该步不推送」修订为「推送属于收口」以消除字面矛盾。
- **A2（单一 owner 内闭合，不新增文档）**: 收口的语义归 `shared/workflow/artifact-commit-step.md`（既有 owner），策略声明归 `.specify/workflow/git.md` 托管块（既有 owner），操作归 `git-utils` 作用域 A（既有 owner）。本特性不新建任何文档/技能/引擎——这是宪法 Principle IX 与 XIV 的直接要求。
- **A3（远端名不写死）**: 本仓的 `origin` 是**上游只读**，`github`/`gitlab`/`gitee` 是同一 fork 的三镜像；而 `skills/external/git-utils/references/execute-commands.md` 中的示例命令一律写 `git push origin <branch>`。这是**文档级的既有不一致**，本特性 MUST NOT 在收口中假定任何远端名：推送目标只能来自 `Closeout remotes`，只读上游以能力标记（不是名字）排除。该不一致登记为框架观察，交由 plan/implement 处理，本阶段不修改既有 references。
- **A4（「记录提交」= 一个提交，不是逐类一个）**: 反馈 / 执行量化 / 会话 / 运行判定四类记录合并为收口时的一个提交，理由是归因单位是「一次运行」。若实现期发现某类记录由独立引擎在收口之后才落盘，按 Fast Fail 的「纠正」就地调整提交边界并在回传披露。
- **A5（临时分支的远端分支不删除）**: 设计简报开放问题 2 裁为「不在远端创建短命分支，因此收口无需远程删分支」。临时分支模型的短命分支只在本地存在，合回主干后删本地；推送的是主干。这样避免了远程分支删除这一破坏性动作进入无人值守路径。
- **A6（提交粒度：每次收口两个提交）**: 设计简报开放问题 1 裁为「两个提交」——工件先行（既有步骤，保归因），记录在收口时一次落下。若某次运行不产生记录，则只有一个提交，FR-007 已覆盖。
- **A7（`Closeout: ask` 在无人值守下的行为）**: 缺省 `ask` 意味着无人值守运行**不会**自动推送——它在收口步骤呈现命令并以一行说明结束，而不是阻塞等待。这与既有的「无人值守不征求继续」一致：呈现即报告，等待是下一次用户回合的事。
- **A8（不新增脚本）**: 收口序列由技能流程 + 契约测试判定，不引入第二个可执行引擎脚本；若实现期证明需要确定性推导，以扩展现有 Python 工具的方式落地，且必须在其 `--help` / `--version` 上满足宪法 Principle XXI（Script Interface Contract）。
- **A9（驱动者 U6 收敛为实例）**: 驱动者当前在 U6 做本地合并（不 push）。本特性将其表述为该 owner 的一个实例；驱动者**不新增**推送行为，除非其线所声明的 `Closeout` 允许。状态脊 `direction_contract` 的 `forbidden_drifts` 已禁止自动强推与推只读上游，二者一致。
- **A10（夹具仓库的落点）**: 夹具仓库建在受制裁的临时根下（`tempfile.TemporaryDirectory()`，属 `temp-directory-discipline.md` §5 例外），不落仓库内目录，避免第二套目录治理。
- **A11（本特性自身的收口受同样约束）**: 本阶段的提交只含本特性产物、按显式路径、不 push——即在收口机制落地之前，本特性自己的运行仍按手工步骤完成，并把这件事实记录在此以免被误读为「机制已生效」。
- **A12（术语）**: 中文统一用「收口」（close-out），避免与「收尾 / 合并 / 结束」混用；英文统一 `close-out`（连字符），与既有 `git.md` 措辞一致。
