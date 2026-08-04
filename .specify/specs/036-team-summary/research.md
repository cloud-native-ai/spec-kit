# Phase 0 Research: Team Summary 信息管理机制

**Requirement**: `036-team-summary` → Feature 027 Team Management
**Date**: 2026-08-04
**Method**: 代码优先(Constitution VIII)——每条结论要么来自对 `skills/summarize-project` 与 `skills/create-team` 源码/DDL 的定向阅读,要么来自本轮**实际执行**被调技能的脚本链。文档声明只作线索,不作依据。

## E. 执行验证(先做,再设计)

对真实存量团队 `cws-workspace-cluster` 的 tracked 工件手工派生一份表单,跑完被调技能的全链路:

| 步骤 | 命令 | 结果 |
|------|------|------|
| 齐备性校验 | `validate-project-input.py --input … --json` | `status: ready`,`missing_required: []`,**exit 0** |
| 装载(非法 ID) | `project-db.py --load …` | **exit 3**,拒绝并报可读原因 |
| 装载(合法 ID) | `project-db.py --load …` | exit 0,`inferred_fields=1` |
| 完整性体检 | `project-db.py --check` | `状态 ok`,**exit 0** |
| 进度引擎 | `progress-engine.py --db …` | exit 0,输出 19 个顶层字段 |

**E-1(证实 SC-001/SC-002)**:R 档三条**完全可由团队 tracked 工件满足**——`project_name` ← `team.md` frontmatter `name`;`baseline_date` ← 本次 cycle 时间戳;`work_items`/`milestones` 至少一组非空 ← `STATE.md` 被跟踪条目 + goal 成功判据。首次总结无需任何人工补填,不触发退出码 3 阻断。这是本需求最关键的可行性前提,现已由执行证实而非推断。

**E-2(约束 FR-026 的 ID 形态)**:装载被拒的原文——

> `item_id='TIX-3f9a1c load'` 不是合法标识 —— DDL 约束 `entity_ids.entity_id` 只允许字母/数字/`_`/`-`/`.`,且以字母或数字开头。

故团队发放的条目 ID 受 DDL 硬约束:`[A-Za-z0-9][A-Za-z0-9_.-]*`。**推论**:FR-027 的「标题 + 所属阶段」推断身份**不能**把中文标题直接当 ID(中文与空格均越界),必须先做确定性摘要(短哈希)再作 ID。若无此次执行,设计极可能落入"用标题当键"的陷阱。

**E-3(证实 FR-006 / US4 场景 3 已被引擎兜住)**:无勾选比、无明写百分比时引擎给
`project.progress.progress_pct = null`,并附 `reason: "…无可计数依据,只报状态计数"`。**引擎自身拒绝写 0%**,团队侧无需另建防线,只需不伪造输入。

**E-4(证实 FR-023 / US5 场景 3 已被引擎兜住)**:无排期材料时 `gantt.bar_count = 0`、`schedule_material.has_planned_dates = false`、`split_recommended = false`——**甘特自动不出图**,无需团队侧判断。

**E-5(发现一条新的强制要求)**:`coverage` 在引擎输出中为 `null`——`coverage` 块**只在表单显式提供时**才有值。而 `consistency-rules.md` 的落盘门禁 **CG-COVERAGE** 规定:报告含 `@startwbs` 却无覆盖完整性声明 → **FAIL**。功能分解图是无条件出图项,故**表单生成器 MUST 恒定产出 `coverage` 块**(`candidate_total` / `excluded` / `granularity_truncated` / `unattributed` / `source_label`),否则每次总结都会在落盘门禁前失败。此项在 requirements.md 中没有对应 FR,属规格未覆盖的实现级强制项,记入本文件并由契约承载。

**E-6(阶段聚合对"未知"的处置)**:阶段节点输出 `status: "completed"` + `status_source: "aggregated(2 个子项)"`,而其 `children` 有 3 个——被判 `unknown` 的条目**不参与**聚合分母。故 FR-006 的"未知"终态不会把阶段拖成延期,亦不虚增完成率。

**E-7(聚合引入的 ID 撞号,范围修订期实测)**:双索引把 N 个团队的台账装载进**同一个** `project.db`。实测两条:

- 两个团队各自发放的 `TI-0001` 同时入库 → **exit 3** 被拒,原文:`item_id='TI-0001' 在本实体内重复 —— DDL 约束 PRIMARY KEY(同一实体不得两行同号)`。
- 改为团队命名空间前缀(`team-a.TI-0001` / `team-b.TI-0002` / `team-a.PH-0001`)后 → **exit 0**,装载与体检均通过(`.` 属 DDL 允许字符)。

**推论**:团队内单调递增的条目 ID 在聚合层**必须**加团队前缀,否则任何两个共享 goal 的团队一相遇即整体阻断。该前缀同时天然承载 FR-033 的机器可判定归属。此坑只有在真跑聚合装载时才暴露——按"每团队 ID 团队内唯一"的直觉设计会直接踩中。

## D. 设计决策

### D-1 累积状态存放在团队 tracked 台账,而非派生数据库

**决策**:表单生成器每次从团队的**累积台账**重新折叠出全量表单,用 `project-db.py --load`(默认重建)装载;**不**采用 `--update` 让历史数据库承载累积状态。

**依据**:
- 被调技能明确定位数据库为**派生物**("默认每次运行重建…绝不写入目标项目管理工件"),`--update` 是例外路径。
- FR-011 要求出处指向 tracked 工件。若累积状态只活在 `data/project.db`,则该状态自身没有 tracked 出处,与 FR-010/FR-011 冲突。
- 可复现性:删除整个交付目录后重跑应得到同一份总结。`--load` + tracked 台账满足;`--update` 不满足(状态随库丢失)。
- FR-018 的"MUST NOT 每次从零重建而丢失此前累积的工作项"约束的是**丢失**,不是**重建**。从完整台账重建不丢任何条目。

**被否方案**:`--update` UPSERT 模式。否决理由:把权威状态放进派生物,违反上一条,且使"删库重跑"产生静默的历史丢失。

**人工批注**:无需团队侧实现——被调技能 Step 1 已有"存在既有报告 → 读取其 `## 附注` 节以备保留",Step 7 刷新时保留。FR-018 后半句由既有能力满足。

### D-2 新增一份 tracked 的按条目台账 `items.jsonl`

**决策**:每个团队目录新增 append-only、tracked 的 `.specify/teams/<slug>/items.jsonl`,由团队主管在其正常写入相中追加;每行一个条目状态事件,携带 `item_id` / `title` / `phase_ref` / `state` / `provenance` / `ts` / `identity`(`explicit|inferred`)。

**依据(三条硬事实迫使新增载体)**:
1. `STATE.md` **没有机器可读结构**——实测两个 continuous 团队:`cws-workspace-cluster` 用叙述段落(`## 洞察台账` 内是散文 + 剔除清单),`requirement-implement-monitor` 用状态桶标题(`## High Priority` / `## Watch List` / `## Resolved`)。二者分节名与形态均不同,无共同 schema 可确定性解析。FR-008 要求确定性程序派生,`STATE.md` 现状无法承担。
2. `run-log.jsonl` 是**每 cycle 聚合**(`items_found` / `resolved` 等计数),不含逐条目身份;且**仅 continuous 模式有**(实测:两个 iteration 团队只有 `team.md` + `runs/`)。
3. 子代理结果清单位于 **git-ignored** `.specify/teams/.work/<slug>/`,外部派发三元组更在 `${TMPDIR}/spec-kit-dispatch`(**仓库之外**)。FR-011 禁止其作为出处。

台账因此同时解决三件事:提供确定性解析面(FR-008)、承载显式 ID(FR-026)、把不可作出处的运行时事实**提升**为 tracked 出处(FR-010/FR-011)——台账行本身即出处路径。

**被否方案**:
- *扩展 `run-log.jsonl` 行加 `items[]` 数组*:continuous 专属,其余三模式无此文件;且把按 cycle 的聚合记录与按条目的身份记录混在一张表,查询与去重都要在读侧重做。
- *标准化 `STATE.md` 分节*:`STATE.md` 是给人读的跨运行记忆,强加 schema 会同时损害其可读性与既有两个团队的现存内容,且仍需为 iteration/parallel/serial 从零建立。
- *只在 `runs/*-report.md` 上做正则*:报告契约确实固定(`## Deliverables` 表等),但只能拿到**每次运行**的交付物,拿不到跨运行的条目推进;仅用于 FR-025/FR-027 的历史回填路径。

**FR-026 的 `STATE.md` 覆盖**:台账是权威结构面;`STATE.md` 条目额外内联 `[TI-nnnn]` 标记,供人交叉引用,满足 FR-026 "至少覆盖 `STATE.md` 的被跟踪条目"的字面要求而不改变其散文形态。

### D-3 ID 方案(受 E-2 约束)

| 实体 | 形态 | 说明 |
|------|------|------|
| 工作项(显式) | `TI-<nnnn>` | 团队主管按台账序号发放,重命名不变(FR-026) |
| 工作项(推断) | `TIX-<8hex>` | `sha256(标题 + 所属阶段)` 前 8 位十六进制;仅历史条目(FR-027) |
| 阶段 | `PH-<nnnn>` | cycle / generation / stage / 派发批次序号 |
| 里程碑 | `MS-<nnnn>` | goal 成功判据序号 |
| 人员 | agent slug | 直接用名册引用的 agent slug(已合法) |

全部满足 E-2 的 DDL 字面量约束(实测 `TI-0001` / `TIX-3f9a1c` / `PH-0001` / `MS-0001` / `insight-synthesizer` 均装载通过)。

**身份归并(FR-027)**:台账行携带 `supersedes: TIX-<hex>`;折叠时以显式 ID 为权威、合并历史事件为一条记录,并在 `inferred_fields` 留痕。

### D-4 FR-029 的聚合落到既有 `coverage` 块

**决策**:已完成/已归档条目全量留在台账与表单 `work_items`,在呈现层通过 `coverage.granularity_truncated` 表达为按阶段的计数,不逐条进入分解图。

**依据**:`consistency-rules.md` 明列「分解树只画聚合工作项 → **允许**,但候选全集差值须有名有数 + 残差清单落盘」。拆图阈值是可机械判定的 **CG-6:WBS 深度 ≥2 节点数 > 15**(另有引擎 `gantt.split_recommended`)。故 SC-012 的"节点阈值"= 15,由既有门禁脚本判定,团队侧无需自建阈值。配合 E-5,`coverage` 块本就必须恒定产出,聚合与覆盖声明是同一机制的两面。

### D-5 触发点:四模式各一处,插在既有流程的收尾相

| 模式 | 插入点 | 依据 |
|------|--------|------|
| continuous | 每-cycle 循环新增第 9 相 `SUMMARIZE`,在第 8 相 `REPORT` 之后 | 既有 8 相循环末尾即 cycle 收尾(FR-012) |
| iteration | 每代 `DECIDE` 相完成后 | FR-012 |
| serial | 每个 stage 交接验证通过后 | FR-012 |
| parallel | 交叉校验 + 结果汇总完成后 | FR-012 |
| 全模式终态 | goal 达成 / 收敛 / halt / 人工停止 | FR-012 后半句 |

门控顺序(硬序):**预算 → 节奏 → 材料**。预算优先由 Edge Case「同一 cycle 内既到达节奏点又触发预算阶梯」直接规定。

**非调度器**:触发点是提示层编排指令,不是守护进程——与 Constitution IX 一致。`scripts/dispatch.sh` 是**派发包装器**(被主管在一次运行内调用),不是调度器;spec Assumption 的结论因此不变,仅其"无可执行运行器"的措辞需按 plan.md 预置约束块的分层术语校正。

### D-6 交付目录与非交互调用

- 交付目录 `[[STR-001]]` = `.specify/project/goal/<goal-slug>/`(2026-08-04 范围修订前为团队目录下的 `summary/`)。被调技能的交付目录**本就可由用户指定**("用户可指定其他位置"),故 FR-024(技能不变)成立。实测 `.specify/.gitignore` 仅忽略 `teams/.work/` 与 `agents/execution/logs/`,`.specify/project/` 未被忽略,该目录保持 tracked。
- 被调技能 Step 4 默认有**四道逐层交互确认门禁**;团队触发是自动流程,故 MUST 以**非交互模式**调用并在 `## 元信息` 标注(技能已支持"用户显式声明跳过 → 自动确认并标注")。

### D-7 双索引:goal 为聚合索引,team 为运行索引(2026-08-04 范围修订)

**决策**:产物分两侧——`.specify/teams/<team-slug>/` 只保留运行信息(team 索引),`[[STR-001]]` 承载唯一的完整总结并聚合同一 goal 下全部团队(goal 索引)。goal 身份由 `team.md` frontmatter 显式声明的 [[STR-006]] 承载。

**实测前提**:
- `.specify/project/` **已存在且 tracked**(10 个文件):`project.md` + wbs / gantt / milestones 各自的 `.puml`/`.svg`/`.png`,由已重构的 `manage-project` 于 2026-07-25 建立,其正文自述"不再由技能维护,现作为信息源之一"。故 `goal/` 子树必须**平级新增**、不得覆盖(FR-036),且新路径与被调技能对 SpecKit 项目的默认交付目录 `.specify/project/summary/` 亦为平级、不冲突。
- 现有 4 个团队 frontmatter **均无 goal 标识字段**,且 goal 是多行折叠 prose;`requirement-implement-monitor` 的 goal 更是**每次运行参数化**("run 输入:requirement key")。这三点共同否决了"从 goal 正文派生 slug"。

**七实体在聚合语义下的重解**:
- `project` 从"团队"上移为"**goal**":`project_name` ← goal 的显式标识/标题,`project_desc` ← goal 正文。这使 `milestones` 的来源更自然——里程碑取自 **goal 的**可验证成功判据,一套即可,不再逐团队重复(FR-032)。
- `phases` MUST **按团队命名空间化**(`phase_name` 携带 team 前缀),因为同一 goal 下的团队可能模式不同、阶段单位不同(cycle vs generation vs stage vs 派发批次),混为一条序列会产生无意义的顺序(Edge Case)。
- `work_items` / `people` 取各团队之并集;`work_items` 的 `source` 出处路径天然以 `.specify/teams/<team-slug>/` 开头,**归属因此机器可判定**(FR-033),无需新增字段;呈现层以阶段的 team 前缀承载归属,不泄漏代理 id 等内部标识符(FR-022)。

**累积语义的加强**:D-1 已确定累积状态的权威在团队 tracked 台账而非派生库。在聚合下这一点更关键——goal 总结每次从**该 goal 下全部团队的台账**重新折叠,故"某团队本次未参与刷新"不会使其历史贡献消失(FR-032),且"删除交付目录后重跑得同一份总结"依然成立。

**并发**:多个团队共享一个 goal 后,两个团队邻近触发会并发写同一交付目录。决策:**串行化为一次成功刷新**(单写者),被跳过的那次在自己的运行报告里留状态行(FR-035)。这不需要新机制——总结步骤本就只由团队主管写入(FR-021),加一道"目录级互斥 + 写后即完整"的纪律即可;半写产物是被明确禁止的失败态。

**存量降级**:未声明 [[STR-006]] 的团队以其 team slug 回填推断 goal 身份并标记为推断(FR-034),与 FR-027 的工作项推断身份完全同构——同一套"显式优先、推断兜底、交接归并"的模式复用两次,不引入第二套概念。

**被否方案**:
- *goal 目录只放索引页链接到各团队总结*:直接违反被调技能的目录自包含红线(禁止引用交付目录外的文件),外部读者拿到 goal 目录无法独立阅读。
- *两侧都出完整总结*:图表渲染与数据装载翻倍,正是 continuous 团队的预算压力点(SC-005 / FR-014),且两份产物需额外保证同源一致。
- *从 goal 正文哈希派生 slug*:FR-019 明确允许刻意修改 goal 正文,一改即换目录、留下孤立产物;且长 prose 派生出的 slug 不可读。
- *沿用 team slug 作目录名*:等于取消 goal 索引——目录仍以团队为索引,只是换了位置。

## O. 遗留与移交

| 项 | 处置 |
|----|------|
| E-5 的 `coverage` 恒定产出 | 规格无对应 FR;由 `contracts/team-project-form.contract.md` 承载为 MUST,并在 `/speckit.tasks` 建独立任务 |
| `dispatch.sh` 三元组实际落 `${TMPDIR}/spec-kit-dispatch`,而 spec/预置块称其在 `.specify/agents/execution/logs/` | 二者对 FR-011 的**结论一致**(均非 tracked)。建议实现期把 `DISPATCH_LOG_DIR` 默认改为 `execution/logs/`,使文档与代码一致;记入本表待 `/speckit.tasks` 决定归属 |
| 存量团队无 serial / parallel 实例(实测 4 个团队:2 continuous + 2 iteration) | SC-001 的"四种模式各取一个既有团队"无法只用存量团队满足;需为 serial/parallel 构造夹具团队,或将 SC-001 的这两格标注为夹具验证 |
| 无可执行的团队运行器(措辞) | 按 D-5 校正为分层术语,结论不变 |
