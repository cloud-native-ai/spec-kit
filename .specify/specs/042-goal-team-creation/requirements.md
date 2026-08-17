# Requirements Specification: 基于已定义 Goal 的团队创建流程(Goal→Target 分解提议 + 每 Target 一队)

**Requirement Branch**: `042-goal-team-creation`  
**Created**: 2026-08-17  
**Status**: Implemented (2026-08-17, via /speckit.implement — 33/33 tasks, SC-001..006 pass; see verification.md)  
**Input**: User description: "需要为team命令增加一个基于goal的创建流程. 通常情况下我们会先通过/speckit.goal命令定义一个goal,然后通过/speckit.team命令创建一个team去实现这个goal. 需要在/speckit.team命令中创建流程增加一个分支,如果用户传入了一个已定义的goal,需要能够根据这个goal的特点创建一个符合需要的team. 在创建之前需要新仔细分析goal的内容,如果goal的内容过于宽泛并且没法短期实现,那么可能需要将goal分解为多个Target(参考@.specify/shared/definitions/goal-definitions.md), 每个target创建一个team. 需要完善goal->target的分解过程来达成这一点."

## Related Feature *(mandatory)*

**Feature ID**: 027  
**Feature Name**: Team Management

**绑定理由**(2026-08-17 clarify 裁定):主体改动面在团队域——`/speckit.team` create 路径、`team.md` 新增 [[STR-004]] 字段、多团队 territory 提议;goal 侧零新增操作面(分解批准复用既有 `targets --add`,不动 `goal.md` 结构与 goal 引擎),与 036(team summary)扩展 027 的先例一致。Feature 041(Goal Registry)保持概念真源与 Goal/Target 消费面的交叉引用,不承载本需求。

## Overview

**定位**。典型工作流是:先经 `/speckit.goal` 归档一个 goal 定义,再经 `/speckit.team` 组建团队去实现它。当前 create 流程(team.md → Routing flow 第 2 步)把 goal 当作**自由文本**引导——即便 archive 里已有定义,也不会被识别、加载与分析;goal→Target 的分解(038 落地)只有**逐条手写**的授权入口(`targets --add`),没有任何辅助起草与成组批准的过程;更没有"一个宽泛 goal → 多个 Target → 每个(Target)一个团队"的成组建队路径。

**现状锚点(以源码实测为准)**:

- `templates/commands/team.md` create 路径:elicit 自由文本 goal → preset 匹配 → 派生 roster+pattern → 落盘 `team.md`(可选 `goal_slug`)。无 archive 识别分支。
- `templates/commands/goal.md` + `scripts/python/goal-utils.py`:`targets <slug> --add|--list|--set` 为 Target 唯一授权面(单一撰写入口,038 FR-007);GD-2/GD-3 切片尺度形态检测、判据复述拒绝、终态只读、身份单调发放均在引擎内。
- `skills/create-team/references/goal.md` § Target:团队侧对 Target 的影响是**提议形**(propose → ratify);`## Targets` 只由引擎渲染,派生流程禁写 `goal.md`(038 FR-008)。
- run 级 `--target` 指派与五项 preview 校验已落地(038 FR-009);`coordinate`(037)提供跨团队 territory 再划分的提议形机制。

**本需求补三块**:create 流程的**goal-based 分支**(识别已定义 goal → 加载 → 分析);**goal→Target 分解提议与成组批准过程**(提议起草在 team 侧、落盘仍唯一经 `/speckit.goal`);**每 Target 一个团队**的成组创建(N teams : 1 Goal,默认聚焦 + territory 不相交)。

**核心不变量一句话**:绑定轴保持 team ↔ Goal 且保持静态;分解对 team 侧永远是提议形,Target 落盘唯一入口是 `/speckit.goal`;分析结论是建议而非门禁;分析中的确定性事实全部经引擎判定。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 传入已定义 goal:创建流程识别、分析并产出单个匹配团队 (Priority: P1)

作为团队创建者,我希望 `/speckit.team` 的 create 流程能识别我传入的**已归档 goal**,加载其定义(叙事、判据、生命周期、既有 Targets),在创建前向我呈现对该 goal 的分析,并据此派生结构与模式匹配的团队——而不是把定义当成普通自由文本重新引导一遍。

**Why this priority**: 这是分支的地基:没有"识别 → 加载 → 分析 → 单团队产出"这条主路径,分解路径(US2)与成组建队(US3)都无从挂起。它自身即是最小可交付切片:窄而明确的 goal 直接获得一个结构有据可溯的团队。

**Independent Test**: 对 archive 中一个叙事+判据明确、对象单一的 active goal 执行 create;分支呈现分析四要素并经确认产出单个 `team.md`——`goal_slug` 正确、roster/pattern 附派生理由、preset 强匹配时推荐 preset。全程无 goal.md 写入。

**Acceptance Scenarios**:

1. **Given** archive 存在 active goal `g1`(叙事 + 2 条判据 + 无 Targets), **When** `/speckit.team create` 入参中的 token 与 `g1` 精确匹配并经用户确认进入 goal-based 分支, **Then** 呈现分析(维度 / 判据覆盖 / 无既有 Target / 单团队可达成建议,各附理由),确认后产出一个团队:`goal_slug: g1`,roster 与 pattern 派生自该 goal,preset 强匹配时推荐复用 preset。
2. **Given** 入参不匹配任何 archive slug(纯自由文本), **When** create, **Then** 走既有自由文本流程,产物与行为与引入本需求前逐项一致(零回归)。
3. **Given** 入参 `g2` 而 archive 无此 slug, **When** 尝试进入分支, **Then** 以 [[STR-003]] 前缀报错并指向 `/speckit.goal create`;零产物、零写入,MUST NOT 静默降级为内联 goal 创建。
4. **Given** `g3` 处于 `achieved` / `abandoned` 终态, **When** 尝试进入分支, **Then** 显式报出终态并拒绝创建;零产物。
5. **Given** 分支产出的团队定义, **When** 检查 goal 表述, **Then** frontmatter 声明 `goal_slug`(引用);内联 `goal` 字段(如有)与定义不一致时被显式报出供人裁决,MUST NOT 分叉出第二份权威叙事。

---

### User Story 2 - 宽泛 goal 的分解决策与 Target 提议-批准闭环(完善 goal→target 分解过程) (Priority: P1)

作为面对一个过于宽泛、无法短期实现的 goal 的创建者,我希望 goal-based 分支在创建前**仔细分析 goal 内容**并给出分解决策建议;确认分解后,起草一份满足概念约束的 Target 分解提议集,经我**一次性成组批准**后由 `/speckit.goal` 的既有授权面落盘——team 侧永远只提议,不代笔。

**Why this priority**: 用户诉求的核心增量。没有受辅助、受约束的分解过程,"每个 target 一个 team"就只能靠手工逐条起草授权;有了它,宽泛 goal 到切片集的转化获得了流程与纪律(概念约束、复用基线、成组批准、引擎 verdict 闭环)。

**Independent Test**: 对一个判据跨多维、无既有 Target 的宽泛 goal 走分解路径:获得带理由的提议集 → 一次合并确认 → 逐条经 `goal-utils.py targets --add` 落盘;`## Targets` 由引擎渲染,`## History` 记录每次授权;无任何 `goal.md` 手写。该故事可独立交付——即使暂不建团队,goal 已获得成组切片。

**Acceptance Scenarios**:

1. **Given** 分析判定 goal 宽泛(对象跨多组件/多维度、单团队短期不可达成), **When** 呈现分解决策, **Then** 结论与理由一并呈现,由用户裁决走分解或坚持单团队(建议非门禁)。
2. **Given** 用户确认分解, **When** 起草提议集, **Then** 每条候选为成果形语句(非步骤序列)、附单独理由、呈现为无序集;捆绑独立端态的候选被要求改写,自身独立成立的候选被引导**另立 goal**(GD-3),退出提议集;MUST NOT 复述该 goal 的成功判据或任何 SC-xxx。
3. **Given** 提议集呈现, **When** 用户批准, **Then** 以一次合并确认覆盖整组,随后逐条经 `targets <slug> --add` 落盘;每条引擎 verdict 被尊重——退出码 2 的拒绝被原样上报,修订后重提或被显式放弃,MUST NOT 绕过引擎手写 `## Targets`。
4. **Given** goal 已有 2 条 open Target, **When** 分解路径, **Then** 以既有集合为复用基线,提议只补缺口;语义重复的语句 MUST NOT 被重复授权;done/dropped 条目 MUST NOT 被复用身份或顺带重开。
5. **Given** 用户否决分解建议, **When** 做出裁决, **Then** 回退单团队路径或中止;宽泛 goal 上强行选择单团队不被阻止,但分析结论留痕于确认预览。
6. **Given** 批量落盘中途中止, **When** 再次发起, **Then** 已落盘条目按 FR-007 复用基线保留,其余重新提议;不出现重复授权。

---

### User Story 3 - 每个 Target 一个团队:N teams : 1 Goal 的成组创建 (Priority: P1)

作为创建者,我希望分解批准后(或 goal 已有可用切片集时)能**成组创建**团队——每个 open Target 一个团队,全部绑定同一 `goal_slug`,各自默认聚焦自己的 Target,territory 两两不相交——让我不必逐个手动建队、逐个指定写域。

**Why this priority**: 用户诉求的终点形态("每个 target 创建一个 team")。它把 US2 的切片集直接转化为可运行的多团队编队,并在创建时点——territory 最初被写入的时刻——解决共享 goal 的写域纪律,而不是等 summary 期才发现重叠。

**Independent Test**: 对含 3 条 open Target 的 goal 执行成组创建:产出 3 个 `team.md`——同一 `goal_slug`、默认聚焦各自 Target、slug 确定性无冲突、territory 两两不相交;不带 `--target` 的 run 归属其默认 Target;显式 `--target` 语义与 038 一致。

**Acceptance Scenarios**:

1. **Given** goal 下有 3 条 open Target 且用户批准成组创建, **When** 执行, **Then** 产出 3 个团队,全部声明同一 `goal_slug`;每个团队的 roster/pattern 以其 Target 语句为输入复用既有派生机制(preset 匹配、pattern 决策树),slug 派生确定且无冲突。
2. **Given** 多团队方案, **When** 呈现确认门禁, **Then** 同步呈现基于切片的两两不相交 territory 提议;用户否决提议时显式披露重叠风险并移交 `/speckit.goal coordinate`,MUST NOT 静默落盘已知重叠。
3. **Given** 某团队 run 未显式指定 `--target`, **When** preview, **Then** 解析为该团队的默认聚焦 Target,确认门禁以 [[STR-001]] 标记披露,新台账条目携带 `target_ref`(局部形)。
4. **Given** run 显式指定另一条 open Target, **When** preview, **Then** 按显式指派执行(语义同 038),默认聚焦不阻止显式覆盖。
5. **Given** 团队默认聚焦的 Target 已转终态, **When** run preview, **Then** 被既有五项校验拦截并走复核二分;MUST NOT 存在终态执行旁路,重聚焦经 modify、重开经 `/speckit.goal`。
6. **Given** 同一 goal 下已存在团队(含此前的 goal-based 创建), **When** 再次发起 goal-based 创建, **Then** 检测既有团队并提议复用或移交 coordinate,MUST NOT 无提示重复建队。

---

### Edge Cases

- 传入 slug 与 archive 某 slug 仅大小写/连字符近似但不精确匹配 → 视为不匹配(识别是确定性精确匹配),可在自由文本流程中照常处理;MUST NOT 语义猜测后静默进入分支。
- goal 判据为 `None provided.` → 分析显式声明判据缺失而非臆造;分解照常进行——切片轴(范围覆盖)独立于判据轴(达成度),两者不互为前提。
- goal 已有混合状态 Targets(open + done/dropped)→ 复用基线只取 open;终态条目保留展示但既不复用也不重开。
- 提议集中候选与既有某条判据措辞趋同 → 判据权威规则:该候选 MUST 被改写为范围切片,不得复述判据(引擎与起草双重把关)。
- 分解提议集为空集(分析后无可补缺口)→ 直接进入 US3 复用既有集合成组建队,不强制新增。
- 成组创建与人工并发编辑 archive(批准与落盘之间 goal 被他人置终态)→ 落盘时引擎终态拒绝被原样上报,流程安全中止,零部分写入逃逸。
- 多团队方案下某 Target 语句天然跨多个团队写域 → territory 提议以切片为界仍重叠时,披露为待裁决项并移交 coordinate,MUST NOT 自行缩小切片语句语义来消除重叠。

## Requirements *(mandatory)*

### Functional Requirements

**分支识别与 goal 加载**

- **FR-001**: `/speckit.team` create 模式 MUST 识别**已定义 goal 引用**:入参 token 与 `.specify/goal/` 下现存 `<goal-slug>` 精确匹配(或为指向其定义的路径)时,向用户确认后进入 goal-based 分支;识别 MUST 为对 archive 的确定性枚举匹配,MUST NOT 语义猜测。无匹配时走既有自由文本流程,行为与引入前一致(零回归)。
- **FR-002**: goal-based 分支 MUST 经 `goal-utils.py` 读取定义(叙事、判据、生命周期、既有 Targets),并复述给用户确认;悬空引用 MUST 以 [[STR-003]] 前缀报错并指向 `/speckit.goal create`,MUST NOT 静默降级为内联创建;终态 goal(`achieved`/`abandoned`)MUST 被显式拒绝。
- **FR-003**: 该分支产出的每个团队 MUST 在 frontmatter 声明 `goal_slug`(引用,不是内容副本);定义存在时定义权威,内联 `goal` 字段仅作可读性渲染,与定义不一致时 MUST 显式报出供人裁决。

**goal 分析与分解决策**

- **FR-004**: 创建前 MUST 呈现 **goal 分析**,至少覆盖四要素:goal 维度(对象所处平面)、判据覆盖(含缺失的显式声明)、既有 Target 集合、单团队短期可达成性判断;每项附理由。分析结论是**建议**:单团队/分解路径 MUST 由用户裁决,MUST NOT 作为硬门禁。
- **FR-005**: 分析中一切可确定性判定的事实(archive 枚举、终态判定、既有 Target 清单、引擎 verdict)MUST 经引擎获得(程序优先);语义判断(宽泛度、分解起草、结构派生)由 agent 产出并附理由,落盘前一律经确认门禁。

**goal→Target 分解提议(过程完善)**

- **FR-006**: 分解路径 MUST 产出**分解提议集**(一次性呈现全量,见 [[STR-002]] 小节):每条候选语句 MUST 为成果形(GD-2 切片尺度)、从属同一目标(GD-3:自身独立成立的候选 MUST 被引导另立 goal 而非嵌套),MUST NOT 复述该 goal 成功判据或任何需求规格的 SC-xxx;提议集 MUST 呈现为无序集——MUST NOT 附执行顺序、依赖边或任何编号顺序语义。
- **FR-007**: goal 已有 Target 时,MUST 以既有集合为**复用基线**:open 条目直接复用;提议只能是补充缺口或确认复用,MUST NOT 推倒重建、MUST NOT 重复授权语义重复的语句;终态条目的身份 MUST NOT 被复用,终态条目 MUST NOT 被顺带重开(重开只经 `/speckit.goal`)。
- **FR-008**: 分解对 team 侧 MUST 保持**提议形**:落盘 MUST 经 `/speckit.goal targets <slug> --add` 由用户批准后逐条执行(单一撰写入口不变);分支 MUST NOT 写入 `goal.md` 的任何部分(`## Targets` 只由引擎渲染);引擎拒绝(退出码 2)MUST 原样上报 verdict,修订后重提或显式放弃,MUST NOT 绕过引擎。
- **FR-009**: 批量批准 MUST 为**一次合并确认**(预览全部语句 → 单次用户批准 → 逐条落盘);中途中止时已落盘条目按 FR-007 保留、其余丢弃,续起时不重复授权。

**每 Target 一个团队**

- **FR-010**: 分解批准后(或复用基线成立时),每个 open Target MUST 对应创建一个团队:所有团队声明同一 `goal_slug`(N teams : 1 Goal);每个团队的 roster 与 pattern MUST 以其 Target 语句为输入复用既有派生机制(preset 匹配、pattern 决策树);团队 slug 派生 MUST 确定性且无冲突(沿用 create-mode 既有命名规则)。
- **FR-011**: Target 对应团队 MUST 持久化**默认聚焦引用**:frontmatter 可选字段 [[STR-004]],值为其 Target 的局部形 `T-<nnn>`(与台账逐条字段 `target_ref`、run 级 `--target` 选项显式消歧,不复用任一名称)。未显式指定 `--target` 的 run 解析为默认聚焦 Target,确认门禁披露时以 [[STR-001]] 标记来源;显式 `--target` 语义与 038 完全一致;默认聚焦 MUST NOT 改变 Goal–Team 绑定、goal 身份解析与 summary 交付目录——它只是 run 级变量的预填。run preview 的五项校验 MUST 原样适用于解析后的 Target(含 open 态检查与终态复核二分)。
- **FR-012**: 多团队创建 MUST 同步处理写域纪律:MUST 基于切片呈现两两不相交的 territory 提议并随团队定义落盘;用户否决提议时 MUST 显式披露重叠风险并移交 `/speckit.goal coordinate`,MUST NOT 静默落盘已知重叠的 territory。
- **FR-013**: 确认门禁 MUST 披露:分支判定所基于的定义、分析结论与路径决策、[[STR-002]] 提议集(或复用声明)、多团队方案下的 territory 划分;同一 goal 下已存在团队时,MUST 检测并提议复用或移交 coordinate,MUST NOT 无提示重复建队。

**兼容与文档**

- **FR-014**: 既有 create 流程(自由文本 goal、preset 匹配、无 `goal_slug` 的存量团队)MUST 零回归;既有 goal 定义与既有团队 MUST 零迁移可用;run/modify 模式的既有行为 MUST 不变。
- **FR-015**: 下游文档(canonical:`templates/commands/team.md`、`skills/create-team/references/{goal.md,create-mode.md,execution-guide.md,summary-mapping.md}`、`docs/reference/commands/`)MUST 更新并按概念锚(`shared/definitions/goal-definitions.md`)链接而非复述;全部变更 MUST 经 `sync-mirrors.py` 扇出,MUST NOT 手工双写镜像。

### Key Entities *(include if requirement involves data)*

- **goal-based 创建计划**: 确认门禁处的一次性呈现物——分支判定、分析结论、路径决策、(分解提议集 | 单团队方案)、territory 划分提议;不持久化为独立实体,落痕于确认预览与创建产物。
- **分解提议集**: N 条候选 Target 语句 + 各自理由;提议形,批准前不落盘,批准后逐条经引擎成为正式 Target。
- **Target 聚焦团队**: 声明 `goal_slug` + 默认聚焦引用的 `team.md`;同一 `goal_slug` 下 N 个团队各聚焦一个 Target,territory 两两不相交。
- **默认聚焦引用**([[STR-004]] 字段,新): team.md 中指向其 bound goal 下某 Target 的局部形引用;是 run 级 `--target` 的预填,不是写域声明、不是绑定变更。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: goal-based 分支产出的全部团队 100% 携带与所依据定义一致的 `goal_slug`,且 roster/pattern 派生理由在确认预览中可溯源;自由文本路径(无 archive 匹配)与引入前行为逐项一致——既有测试全绿、无断言削弱。
- **SC-002**: 悬空引用与终态 goal 的拦截率为 100%:均显式报错并给出指引,静默降级为内联创建的次数为 0。
- **SC-003**: 提议-批准纪律:goal.md 的 `## Targets` 全部变更 100% 可溯源到 `goal-utils.py` 调用(team 分支直写次数为 0);被引擎拒绝(退出码 2)的提议语句 100% 经修订重提或被显式放弃。
- **SC-004**: 复用基线:对已含 open Targets 的 goal(重复)执行 goal-based 创建,语义重复语句的重复授权次数为 0;终态 Target 被复用或顺带重开的次数为 0。
- **SC-005**: 多团队方案:同一 goal 下各团队 territory 两两不相交(静态检查通过率 100%);未显式指定 `--target` 的 run 100% 归属其默认聚焦 Target(台账 `target_ref` 可查);Goal–Team 绑定、身份解析与 summary 交付目录的变化次数为 0。
- **SC-006**: 分析披露完整性:每次 goal-based 创建的确认预览 100% 含四要素(维度 / 判据覆盖 / 既有 Target / 可达成性判断),判据缺失时 100% 以显式声明呈现(臆造判据次数为 0)。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 集成测试——构造 archive goal(窄/宽各若干),驱动 create 流程,断言产物 `team_slug`→`goal_slug` 映射与确认预览内容;回归依托既有 create/团队测试套件全量运行。
- **SC-002 Source**: 契约测试——悬空 slug、终态 goal 各若干例,断言报错文案前缀、指引与零产物。
- **SC-003 Source**: 契约测试——批准路径走引擎调用断言(无 goal.md 直写);引擎 exit-2 注入用例断言上报-修订-重提闭环。
- **SC-004 Source**: 集成测试——预置 open/终态混合 Targets 的 goal 上二次执行创建,断言无重复授权、无终态复用。
- **SC-005 Source**: 静态检查——多团队产物 territory 两两交集断言;run 集成测试断言默认解析的披露标记与台账 `target_ref`。
- **SC-006 Source**: 模板/流程产物抽检——确认预览文本断言四要素标题与缺失声明句式。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "(团队默认)" | FR-011, US3 场景 3, execution-guide(run 披露格式), run 报告契约测试 |
| `STR-002` | "分解提议" | FR-006, FR-013, US2 场景 3, 确认门禁模板与测试断言 |
| `STR-003` | "goal 未定义:" | FR-002, US1 场景 3, SC-002 契约测试(报错前缀) |
| `STR-004` | "focus_target" | FR-011, Related Feature 绑定理由, Assumptions, Key Entities, data-model 与 team.md 模板/契约测试 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Out of Scope

- Target 间依赖边、排序、DAG——切片集是无序集(038 已裁定);需要顺序编排的是团队 pattern,不是 goal 定义。
- run 级 `--target` 的校验语义与终态复核二分——038 FR-009 已定,本需求只复用,不修改。
- goal 侧独立的辅助分解入口(如 `/speckit.goal targets --propose` 子命令面)——分解起草随 team 创建分支交付,批准走既有 `--add`;若实践需要 goal 侧独立入口,另行需求。
- summary / 评估侧的切片轴卷积语义——038 US3/US4 已覆盖;默认聚焦只是 run 变量预填,不新增卷积规则。
- 既有团队的迁移与重聚焦改造——`migrate`(037)与 `modify` 既有面可用,不为本需求扩展。
- Target 完成的自动判定——只提议、人批准(038 FR-008 不变)。
- goal 定义本身的撰写辅助(客观陈述引导、判据起草)——`/speckit.goal create` 既有职责,不在此扩展。

## Assumptions

- 输入为 chat 文本参数(语音输入经词汇表协议纠正后同形);无独立输入通道,不设输入模态特化逻辑。
- 分解规模为个位到十位级 Target、一次成组创建小规模团队;顺序创建即可,无需并发建队基础设施。
- `goal-utils.py` 沿用为唯一 goal 引擎;如需扩展动作(如批量读取面),沿用 `0/2/3/4` 退出码语义,不另立第二引擎。
- 语义判断(宽泛度、分解起草、结构派生)由 agent 以提议+理由呈现;一切确定性校验经引擎;分析结论不构成硬门禁(建议非门禁)。
- goal-based 分支只作用于 create 模式;run / modify 的 goal 相关行为不变。
- team.md frontmatter 既有字段序不变;默认聚焦引用以可选字段 [[STR-004]] 落在 frontmatter(字段序内的具体插入位置由计划期微调,字段名已定)。

## Clarifications

### Session 2026-08-17

- Q: 需求 042 绑定哪个 Feature? → A: 绑定 Feature 027 Team Management:主体改动面在 `/speckit.team` create 路径与 `team.md`(focus_target 字段、territory 提议);goal 侧零新增操作面(分解批准复用既有 `targets --add`,不动 `goal.md` 结构),与 036 扩展 027 的先例一致;027 索引行与详情页已加反向交叉引用,Feature 041 保持概念真源交叉引用。
- Q: 团队级"默认聚焦引用"的 frontmatter 字段名? → A: 定为 `focus_target`([[STR-004]]):与台账逐条字段 `target_ref`、run 级 `--target` 选项均不撞名,消歧成本最低;FR-011 / Assumptions / Key Entities 已同步落名,消除规格中唯一的"计划期裁定"残留(字段序内插入位置仍留计划期微调)。
- Q: 两条新术语是否写入项目词汇表? → A: 均收录(origin=auto, status=proposed):Focus Target(默认聚焦引用)、Decomposition Proposal(分解提议集),已按冲突检测流程写入 glossary。

