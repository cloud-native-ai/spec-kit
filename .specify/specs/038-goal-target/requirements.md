# Requirements Specification: Goal 的 Target 切片(run 级可指定的子成果分解)

**Requirement Branch**: `038-goal-target`  
**Created**: 2026-08-11  
**Status**: Draft  
**Input**: User description: "在使用 Team 实现 Goal 时,`/speckit.team run <team> 实现 <goal> 这个goal` 的调用方式缺少契约;分析后否决了 run 级 goal 绑定与 Team↔Goal 静态多对多,决定在 Goal 之下增加一套子概念 Target(目标切片):一个 goal 由多个 target 构成,现有 goal 的整体结构不变,run 级可指定 target,在 target 这一层实现灵活性。概念定义落 shared/definitions,并写成正式设计。"

## Related Feature *(mandatory)*

**Feature ID**: 041  
**Feature Name**: Goal Registry

**绑定理由**:Target 是 Goal 概念自身的组成机制(定义随 goal.md 归档、由 `/speckit.goal` 撰写、身份挂在 goal 命名空间下),不是团队属性——它扩展需求 037 落地的 Goal Registry,故与 037 同挂 Feature 041。团队侧只新增两个**消费面**(run 指派、台账归属),与 Feature 027(Team Management)交叉引用而不改其章程。

## Overview

**问题:Goal 与 run 之间缺一个粒度层。** Goal 是重概念——月级端态、刻意修改、按度量推进;一次团队 run 是小动作——小时级、一次派发。今天用户实际的调用形态(`run xuanji-iac-developer 实现 rund-log-component-split-1094633731167611 这个goal`)把一个**工作包级的对象**当作 goal 传入 run,而 run 模式没有任何槽位承接它:模型只能即兴解释(覆盖 goal_slug?临时改绑?当团队自定义参数?),summary 可能落错 `.specify/goal/<slug>/summary/` 目录,长 ID 笔误静默降级为推断身份而不报错。

已排除的两条路(设计过程记录于 Clarifications):

- **run 级 goal 绑定**(三级身份解析 run > team > inferred):粒度错配是根因——它迫使 036/037 的身份解析、GI 不变式、territory 静态枚举、continuous 运营语义全部松动,改动面大且概念别扭。
- **Team↔Goal 静态多对多**:同时服务多目标的团队失去单一北极星,结构推导、evaluator 打分、summary 归属全部失锚。

**方案:在 Goal 之下增加 Target(目标切片)。** Target 是同一端态的**子成果切片**——可独立推进、可判定完成、run 可指定。野生先例已存在:`requirement-implement-monitor` 的 team.md 明写"监控对象由每次 run 的输入参数决定,团队定义本身不绑定任何具体需求"——本需求把这类无契约的 run 输入升格为一等概念。命名保持 **Target** 而非"里程碑":summary 层的里程碑(`MS-<nnnn>`)已被 036/037 定义为成功判据的投影,同域复用会在一个 goal 内造出两套来源不同的"里程碑";且里程碑是时间点语义(when),Target 是范围切片语义(what),run 需要的是 what。

概念的单一事实源已随本需求落定:`shared/definitions/goal-definitions.md` → **Target Decomposition(目标切片)**节([[STR-004]])。本规格只承载操作面;概念表述以定义文件为准,不在此复述。核心不变量一句话:**绑定轴保持 team ↔ Goal 且保持静态;run 级变量是 Target,永不改绑、永不改变身份解析、永不迁移 summary 交付目录。**

层级与两条进度轴:

```
Goal (端态, authored)  1 ── N  Target (范围切片, run 可指定)  1 ── N  run / 台账工作项 (TI-xxxx)

判据轴 (criteria): 端态达成度 —— achieved 的唯一权威
切片轴 (targets):  范围覆盖度 (n/m done) —— 永不推导出 achieved
```

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 目标可以被切片:在 goal 之下授权 Target (Priority: P1)

作为项目维护者,我希望给一个已归档的 goal 增加若干 Target——每条是同一端态的子成果("日志组件拆分完成"),有稳定身份(`T-<nnn>`)与生命周期(`open`/`done`/`dropped`)——并且这一切经由既有的单一撰写入口 `/speckit.goal` 完成,变更可追溯。

**Why this priority**: 这是概念的地基。没有被授权的 Target,run 指派(US2)与台账归属(US3)都无所指。它也是最小可交付切片:哪怕没有任何 run 引用,goal 定义已经获得了此前不存在的"范围分解视图"。

**Independent Test**: 对一个既有 goal 添加 3 条 Target;`goal.md` 出现引擎渲染的 `## Targets` 节,身份单调发放;把其中一条置为 `dropped` 后它仍保留在节内;步骤形("首先…然后…")与复合形条目被拒绝。

**Acceptance Scenarios**:

1. **Given** 一个已归档的 goal, **When** 经 `/speckit.goal` 添加一条成果形 Target, **Then** `goal.md` 的 [[STR-001]] 节新增该条目,身份为下一个未用的 `T-<nnn>`,状态 [[STR-002]],变更记入 `## History`。
2. **Given** 一条写成步骤序列的 Target 候选, **When** 尝试添加, **Then** 被引擎以 GD-2 语义拒绝(退出码 2),并提示改写为子成果。
3. **Given** 一条捆绑两个独立端态的 Target 候选, **When** 尝试添加, **Then** 被要求拆分——切片仍从属同一目标,独立成立的端态应另立 goal(GD-3 litmus)。
4. **Given** 一条 `done` 或 `dropped` 的 Target, **When** 查看 goal, **Then** 它仍在 [[STR-001]] 节中携带终态,MUST NOT 被删除;其身份编号 MUST NOT 被复用。
5. **Given** 一个从未添加过 Target 的 goal, **When** 执行任何既有 goal 操作(view/validate/status/criteria), **Then** 行为与 Target 机制不存在时完全一致。

---

### User Story 2 - run 指定 Target:调用方式获得契约 (Priority: P1)

作为团队使用者,我希望 `/speckit.team run <team>` 能显式指定本次 run 推进绑定 goal 之下的哪一个 Target,取代"实现 XXX 这个goal"的自然语言即兴解析;引用被校验,确认门禁把它披露出来,run report 记录它。

**Why this priority**: 这是驱动整个设计的原始诉求——run 级控制点。与 US1 并列 P1:两者合起来才构成最小闭环(授权 → 指派)。

**Independent Test**: 对绑定了含 3 条 Target 的 goal 的团队,分别以合法 Target、悬空 Target、终态 Target、以及不带 Target 执行 run:第一种进入确认门禁并披露,中间两种在 preview 阶段被拦截,最后一种行为与引入前一致。

**Acceptance Scenarios**:

1. **Given** 团队绑定的 goal 下存在 `open` 态的 `T-002`, **When** run 指定 `T-002`, **Then** 确认门禁披露"绑定 goal + 本次 Target(T-002: 语句)",执行后 run report 记录该指派。
2. **Given** 指定的 Target 不存在于绑定 goal 之下, **When** preview, **Then** 报为悬空引用并停止,提议先经 `/speckit.goal` 添加;MUST NOT 静默接受或降级。
3. **Given** 指定的 Target 处于 `done` / `dropped` 终态, **When** preview, **Then** 显式报出终态并停止执行,要求复核:终态属实 → 返回报告并结束本次 run;发现仍有未完成工作项或状态与证据不符 → 须经 `/speckit.goal` 重开该 Target 后重新发起指派。MUST NOT 在终态下直接执行,也 MUST NOT 默默当作 open 执行。
4. **Given** run 未指定任何 Target, **When** 执行, **Then** 对 goal 整体运行——与本需求引入前的行为逐字节等价(报告结构、summary 状态行均无新增必填项)。
5. **Given** 团队未绑定任何 goal 定义(纯内联 goal 的存量团队), **When** 尝试指定 Target, **Then** 报"Target 依赖 goal 定义"并指向 `migrate` 路径;不指定 Target 时该团队一切照旧。

---

### User Story 3 - 进度按 Target 归属:切片轴进入总结 (Priority: P2)

作为关心"目标推进到哪里"的读者,我希望团队台账的工作项能归属到 Target,goal 总结按 Target 卷积出范围覆盖度(n/m),并与判据轴分列呈现——切片做完不等于目标达成。

**Why this priority**: 兑现点,依赖 US1/US2 已有授权与指派,故 P2。它把"这个 run 干了哪块"变成可聚合的结构化事实。

**Independent Test**: 两个团队各自带 `target_ref` 追加台账条目后刷新总结:总结含按 Target 的覆盖卷积;无 `target_ref` 的旧条目仍归属 goal 整体;authored 状态与证据矛盾的 Target 被列为待批准项。

**Acceptance Scenarios**:

1. **Given** 台账条目携带 `target_ref: T-002`, **When** 总结刷新, **Then** 该条目计入 `T-002` 的覆盖卷积,归属同时保留团队命名空间(`<team-slug>.TI-nnnn`)。
2. **Given** 不带 `target_ref` 的条目(含全部存量条目), **When** 折叠, **Then** 语义不变——归属 goal 整体,MUST NOT 被强分到任何 Target。
3. **Given** 某 Target authored 状态为 `open` 而其全部归属条目已 `completed`, **When** 总结刷新, **Then** 该不一致被显式列为"待批准完成",两侧都 MUST NOT 被自动翻转。
4. **Given** `target_ref` 指向不存在的身份, **When** 折叠, **Then** 报为无效归属并按 goal 整体降级计入,MUST NOT 臆造 Target。
5. **Given** 总结已产出, **When** 检查两条进度轴, **Then** 判据达成度与切片覆盖度分列,不存在"all targets done ⇒ achieved"形态的推导。

---

### User Story 4 - 已完成的 Target 喂给里程碑视图 (Priority: P3)

作为总结读者,我希望里程碑视图除既有的判据投影外,也能吸收已 `done` 的 Target 作为里程碑条目(带来源标记区分)——"日志组件拆分完成"天然比"误报率 < 20%"更像里程碑。

**Why this priority**: 纯呈现层增强,不影响概念闭环,可独立延后。

**Independent Test**: 对含已完成 Target 的 goal 刷新总结:里程碑组同时含判据来源(`source` 指向 goal.md 判据)与 Target 来源(标记区分)的条目;移除该增强不影响 US1–US3 的任何断言。

**Acceptance Scenarios**:

1. **Given** goal 有 2 条判据与 1 条 `done` Target, **When** 总结刷新, **Then** 里程碑组含 3 条,Target 来源条目带区分标记;判据投影语义(036 FR-013)原样保留。
2. **Given** goal 判据为空(`None provided.`)但存在 `done` Target, **When** 刷新, **Then** 里程碑组不再空缺——由 Target 来源条目填充并声明来源。

---

### Edge Cases

- 同一 Target 被多个团队(同 goal_slug)的 run 先后推进 → 合法(N runs : 1 Target);写域冲突仍由既有 territory 纪律管辖,Target 不是写域声明。
- Target 语句与某条成功判据措辞趋同 → 判据权威规则延伸:Target MUST NOT 复述判据(FR-004);授权时提示改写为范围切片。
- goal 处于终态(`achieved`/`abandoned`) → MUST 拒绝新增 Target 与状态迁移(终态 goal 只读,延续 037 生命周期语义)。
- `## Targets` 节被手工编辑破坏结构 → `validate` MUST 报出(结构由引擎渲染,手写即违规)。
- 项目里同名概念混淆(`optimization_target`、territory 条目的 `target` 字段、evidence/interview 引擎的 `--target`) → 词汇表消歧(FR-017),概念锚已列消歧行。

## Requirements *(mandatory)*

### Functional Requirements

**概念与形态(以 [[STR-004]] 为准)**

- **FR-001**: Target 概念(定义、四条性质、层级、身份、两条进度轴、写入模型)MUST 以 [[STR-004]] 为单一事实源;本规格与所有下游文档 MUST 链接而不复述,MUST NOT 出现第二套概念表述。
- **FR-002**: Target 分解 MUST 是 goal 定义的**可选装饰件**:无 Target 的 goal MUST 完全合法且行为与机制不存在时一致;存量 goal 与团队 MUST 零迁移可用。
- **FR-003**: 每条 Target MUST 是成果形态(GD-2 在切片尺度递归适用),集合 MUST 为无序集(身份序号不承载执行顺序);引擎 MUST 复用与 objective 同源的任务清单/复合检测拒绝违规条目,MUST NOT 另立第二套检测文法。
- **FR-004**: Target MUST 从属其父 goal 的同一目标(GD-3 litmus:独立成立的端态引导拆分为独立 goal);Target 语句 MUST NOT 复述该 goal 的成功判据,也 MUST NOT 复述任何需求规格的 SC-xxx(判据权威互斥延伸到切片)。
- **FR-005**: Target 身份 MUST 为 goal 命名空间内的 `T-<nnn>`(单调发放、终态不复用);限定形 MUST 为 `<goal-slug>.T-<nnn>`(点命名空间,沿用 `<team-slug>.TI-<nnnn>` 先例),并满足既有 DDL 身份文法。
- **FR-006**: Target 生命周期 MUST 恰为三态 [[STR-002]];终态条目 MUST 保留不删除;每次授权与状态迁移 MUST 记入 goal 的 `## History`(承接 037 FR-005 的变更追溯)。

**撰写入口与写入面**

- **FR-007**: Target 的授权与状态迁移 MUST 只经 `/speckit.goal`(037 FR-025 单一撰写入口不变);[[STR-001]] 节 MUST 由引擎渲染,MUST NOT 手写;`goal-utils.py` MUST 新增确定性动作(add / list / 状态迁移,动作名计划期定),退出码沿用 `0/2/3/4` 语义,MUST NOT 另立第二引擎。
- **FR-008**: 团队与 run 侧对 Target 的一切影响 MUST 是**提议形**(提议新 Target、提议完成),由人经 `/speckit.goal` 批准落盘(propose → ratify,与 coordinate 同构);任何派生流程 MUST NOT 写入 `goal.md`(承接 037 FR-007/FR-023 写入面纪律)。

**run 指派(消费面一:`/speckit.team`)**

- **FR-009**: `/speckit.team` 的 run 模式 MUST 接受可选的 Target 指定(规范式参数,具体选项名计划期定且 MUST 满足 FR-017);指定的引用 MUST 被校验:存在于该团队**绑定的** goal 之下且处于 `open` 态——悬空引用 MUST 报错停止;终态引用 MUST 显式报出并停止执行,复核后终态属实者返回报告结束,状态与证据不符者须经 `/speckit.goal` 重开后重新指派;MUST NOT 静默接受、降级或臆测。
- **FR-010**: 未指定 Target 的 run MUST 与本需求引入前行为逐字节等价(对 goal 整体运行;报告结构与 summary 状态行无新增必填项);未绑定 goal 定义的存量内联团队 MUST 不受影响,其指定 Target 的尝试 MUST 报"依赖 goal 定义"并指向 `migrate`。
- **FR-011**: 确认门禁 MUST 披露绑定 goal、本次 Target(或"无")及其状态;run report MUST 记录本次指派(含"无")。
- **FR-012**: Target 指派 MUST NOT 改变 Goal–Team 绑定、goal 身份解析(036 §10.1 两级)、summary 交付目录与既有 GI 不变式;跨 goal 指派(指向绑定 goal 之外的 Target)MUST 被拒绝。

**台账与总结(消费面二:summary 链路)**

- **FR-013**: `items.jsonl` 契约 MUST 新增**可选**字段 [[STR-003]](值为局部形 `T-<nnn>`,goal 由团队绑定隐含);既有 IL-1…IL-5 不变式 MUST 保持;无该字段的行(含全部存量行)语义 MUST 不变——归属 goal 整体。
- **FR-014**: goal 总结 MUST 产出按 Target 的覆盖卷积(切片轴,n/m);切片轴 MUST 与判据轴分列,MUST NOT 从 Target 完成度推导 goal 达成度(037 FR-030/FR-031 权威不变);[[STR-003]] 指向不存在身份的行 MUST 报为无效归属并按 goal 整体降级。
- **FR-015**: authored 状态与台账证据不一致的 Target(如 `open` 而归属条目全部完成)MUST 在总结中显式列为待批准项,MUST NOT 自动翻转任何一侧。
- **FR-016** *(P3, 随 US4)*: 里程碑视图 MAY 吸收 `done` Target 为里程碑条目,且 MUST 以来源标记与判据投影区分;036 FR-013 的判据投影语义 MUST NOT 被改变或移除。

**术语与文档对齐**

- **FR-017**: 词汇表 MUST 收录「Goal Target(目标切片)」词条,并与既有同词用法显式消歧:`optimization_target`/`co_targets`(迭代环优化对象)、territory 条目的 `target` 字段、evidence/interview 引擎的 `--target` 选项;存量用法 MUST NOT 被重命名。新 CLI 选项 MUST NOT 与既有 `--goal`(两支脚本占用,037 FR-021)冲突。
- **FR-018**: 下游文档(canonical:`templates/commands/goal.md`、`templates/commands/team.md`、`skills/create-team/references/{goal.md,execution-guide.md,summary-mapping.md}`、`docs/reference/commands/`)MUST 按 FR-001 链接概念锚;全部变更 MUST 经 `sync-mirrors.py` 扇出,MUST NOT 手工双写镜像或 per-tool 副本。

### Key Entities *(include if requirement involves data)*

- **Target**: goal 定义内的授权条目——语句(成果形)、局部身份 `T-<nnn>`、状态([[STR-002]] 之一);变更史寄宿于 goal 的 `## History`。持久化于 `goal.md` 的 [[STR-001]] 节,由引擎渲染。
- **`target_ref`**(台账字段): 工作项对 Target 的归属声明,可选,局部形;是切片轴卷积的唯一数据来源。
- **run 指派**(运行时值,不持久化为独立实体): 一次 run 选定的 Target 引用,落痕于确认门禁披露与 run report。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对含 ≥3 条 Target 的 goal,指定 Target 的 run 其 report 与新增台账条目可无歧义归属到该 Target 的比例为 100%。
- **SC-002**: 不指定 Target 时,既有团队 run 的行为零回归——报告结构、summary 状态行、身份解析结果与引入前完全一致(既有测试全绿,无断言削弱)。
- **SC-003**: GD-2/GD-3 违规样例集(步骤形、复合形)被引擎拒绝率 100%,且拒绝信息指明改写方向。
- **SC-004**: 悬空/终态/跨 goal 的 Target 引用在 preview 阶段被拦截率 100%,静默降级次数为 0。
- **SC-005**: 总结中切片轴与判据轴分列呈现,全文不存在由 Target 完成度推导 achieved 的表述;authored/证据不一致项 100% 出现在待批准列表。
- **SC-006**: 概念一致性:[[STR-004]] 与本规格逐维核对零冲突;词汇表消歧后,四处既有 "target" 用法在文档中零重定义。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 集成测试——构造 goal+Targets+团队,执行指定 Target 的 run,断言 report 指派行与台账 `target_ref`;抽查逐条比对。
- **SC-002 Source**: 既有测试套件(基线先行,区分存量失败与回归)+ 对一个存量团队的 run 报告做引入前后 diff。
- **SC-003 Source**: 引擎单元测试——GD-2/GD-3 样例集(复用 037 的 objective 拒绝样例改写为切片尺度),统计拒绝率与退出码。
- **SC-004 Source**: run 模式契约测试——悬空/终态/跨 goal 三类引用各若干例,断言 preview 停止且无执行痕迹。
- **SC-005 Source**: 对刷新产物做文本断言(轴分列、待批准列表存在性);负向断言扫描 "targets done" 与 "achieved" 的推导句式。
- **SC-006 Source**: 以 [[STR-004]] 条目为清单逐项比对本规格;词汇表核对四处消歧行的存在与指向。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "## Targets" | FR-007, US1, Edge Cases, goal.md 渲染/解析, `goal-utils.py` 测试 |
| `STR-002` | "`open` / `done` / `dropped`" | FR-006, FR-009, US1/US2, 引擎状态迁移测试 |
| `STR-003` | "target_ref" | FR-013, FR-014, US3, items.jsonl 契约与折叠测试 |
| `STR-004` | "shared/definitions/goal-definitions.md → Target Decomposition(目标切片)" | FR-001, FR-004, SC-006, 全部下游文档链接 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Out of Scope

- **run 级 goal 绑定与三级身份解析**——已否决(见 Clarifications);绑定轴保持静态。
- **Team↔Goal 静态多对多**——已否决;跨 goal 复用团队仍走既有 GI-2 刻意改绑。
- **Target 间依赖边、排序、DAG**——切片集是无序集;需要顺序编排的是团队的 serial 模式,不是 goal 定义。
- **judgment 自动化**:criteria 与 Target 的自动互导、Target 完成的自动判定(只提议,人批准)。
- **轻量层与 solo run**:内联 goal 团队的"小目标"契约、无团队会话对 goal 贡献的追踪——正交问题,另行需求。
- **存量 "target" 用法的重命名**(`optimization_target` 等)——只消歧,不改名。
- **里程碑=判据投影的重定义**——FR-016 是叠加增强,非替换。

## Assumptions

- 沿用 `goal-utils.py` 单引擎与 `goal.md` 单文件:Target 预期数量为个位到十位级,`## Targets` 节内联渲染即可读;若实践中膨胀,拆分 `targets/` 子目录由后续需求裁定。
- run 指派选项的具体拼写(如 `--target`)由计划期裁定:evidence/interview 引擎的 `--target` 在不同命令表面,不构成冲突面,但 FR-017 的词汇表消歧与 037 FR-021 的 `--goal` 排他检查在命名落定时 MUST 复核。
- Target 机制以 goal **定义**存在为前提(纯内联团队不可用)——这与 037 的"定义存在时定义权威"一致,亦是推动存量团队 `migrate` 的自然激励。
- 本规格创建时未运行 `create-new-requirements.sh`(避免其副作用:创建并切换 git 分支);目录与编号(038)按既有序列手工延续,格式对齐 `templates/requirements-template.md`。

## Clarifications

- Q: run 时传入 goal 名(如 `run <team> 实现 <goal> 这个goal`)如何获得契约——run 级 goal 绑定? → A: 否决。goal(月级端态)与 run(小时级动作)粒度错配;三级身份解析会松动 036/037 的 GI 不变式、territory 静态枚举与 continuous 语义。(2026-08-11)
- Q: Team↔Goal 改为静态多对多? → A: 否决。同时服务多目标的团队失去单一北极星,evaluator/summary/结构推导失锚;跨时间的多对多由既有改绑(GI-2)承载。(2026-08-11)
- Q: 子概念叫"里程碑"? → A: 否决。同域撞名——summary 的 `MS-<nnnn>` 已是判据投影;且里程碑是时间点(when)、Target 是范围切片(what),run 需要 what;有序路线图心智会加剧 GD-2 张力。已完成 Target 可作为里程碑视图的**材料**(FR-016),概念本身保持 Target。(2026-08-11)
- Q: Target 状态谁写?团队能直接把 Target 标成 done 吗? → A: 混合制——授权与刻意生命周期只经 `/speckit.goal`(人批准);执行进度从台账 `target_ref` 推导;不一致显式报出,不自动翻转。goal 归档 authored-only 边界不开口子。(2026-08-11)
- Q: 概念定义放哪? → A: `shared/definitions/goal-definitions.md` 新增 Target Decomposition 节(与 Goal 同锚,不另立文件);本规格为操作面。(2026-08-11)

### Session 2026-08-11

- Q: run 指定的 Target 处于终态(`done`/`dropped`)时,preview 报出之后允许什么路径? → A: 复核二分——终态属实:返回报告并结束本次 run,不执行;发现仍有未完成工作项或状态与证据不符:须经 `/speckit.goal` 重开该 Target 后重新发起指派。不存在"确认即在终态下执行"的路径。已同步改写 US2 场景 3 与 FR-009;并修正 FR-009 交叉引用(选项名碰撞约束在 FR-017,原误写 FR-016)。
