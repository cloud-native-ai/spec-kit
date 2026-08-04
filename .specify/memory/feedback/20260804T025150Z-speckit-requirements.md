---
id: "20260804T025150Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "036-team-summary-20260804T000000Z"
scope: "local"
feature: "036-team-summary"
partial: false
created: "2026-08-04T02:51:50Z"
summary: "本次运行完整走通了 /speckit.requirements 的声明职责:短名生成 → 编号推算(035→036)→ 脚本单次执行 → 模板加载 → 规格生成 → 质量校验闭环。产出 .specify/specs/036-team-summary/requirements.md(25 条 FR / 10 条 SC + 10 条测量来源 / 5 条 Shared Strings / 5 个用户故事"
---

## Review
本次运行完整走通了 /speckit.requirements 的声明职责:短名生成 → 编号推算(035→036)→ 脚本单次执行 → 模板加载 → 规格生成 → 质量校验闭环。产出 .specify/specs/036-team-summary/requirements.md(25 条 FR / 10 条 SC + 10 条测量来源 / 5 条 Shared Strings / 5 个用户故事 / 8 个边界情形),以及 checklists/requirements.md(含 4 项修复的迭代日志)。质量校验第一轮发现 4 个真实问题并全部修复:FR-012 阶段边界定义循环、FR-013 默认节奏不可测、SC-001 混入退出码(非技术无关)、FR-024 缺少可测结果背书;第二轮全项通过。零 [NEEDS CLARIFICATION] 标记,三处真实歧义以 Assumptions 一等条目留痕。步骤 5.5 保留标识符检查发挥了实际作用(发现团队预设顶层已占用 summary: 字段,改为嵌套 config.summary)。命令层面暴露出的问题集中在编号扫描集不完整、披露落点未指定、Glossary 步骤与其余 wrap-up 步骤时序冲突三点。

## Optimization Points
- **编号扫描集漏掉了归档目录(具体缺陷)**:Outline 步骤 2 要求从"remote branches / local branches / specs 目录"三处取最大编号,但 `.specify/specs/.archive/` 下同样存放着带编号的规格(本仓现有 `023-agent-framework-redesign`、`026-agent-team-management`)。本次最大编号恰好在活跃目录(035),因此未撞号;但一旦某个归档编号成为全局最大,该命令会直接分配一个已被占用的编号。建议把 `.specify/specs/.archive/` 显式加入编号扫描集。
- **保留标识符披露没有指定落点**:步骤 5.5 要求 grep 冲突并"surface with a proposed alternate name and an explicit user-override note",但没说这段披露应该写进规格的哪一节。本次发现团队预设文件顶层已存在一行式 `summary:` 字段,我自行决定落到 `## Assumptions`(附带 override 说明)并在 checklist Notes 复述。建议命令明确落点(默认 `## Assumptions`;若该标识符具契约性则同时进 `## Shared Strings`),否则披露容易散落或丢失。
- **Glossary 步骤与其余 wrap-up 步骤的时序不可兼容**:Glossary 步骤要求"at wrap-up 提出新词条并取得用户显式确认后再写入",而 Feedback / Documentation / Git-commit 三个 wrap-up 步骤都在同一轮内完成。结果是:反馈已按"运行完成"落库,而词条提案仍悬在等待用户回复的状态,下一轮是否还会回到该提案没有约定。建议明确:词条提案可跨轮悬置且不阻塞 feedback/docs 收尾,或把 Glossary 提案步骤前移到报告之前。
- **零 CLARIFICATION 标记时缺少"默认值必须留痕"的显式要求**:步骤 5.7 允许 informed guess 代替标记,但未要求把被替代的歧义点显式记录下来。本次三处真实歧义(「拓扑结构」词汇对齐、"项目"指团队自身还是被监控外部目标、快照式还是累积式产物)我主动写进了 `## Assumptions`,但这是自选动作。建议把"每一个替代了 CLARIFICATION 标记的默认判断 MUST 在 `## Assumptions` 留一条"写成硬要求,以便 `/speckit.clarify` 能定向复核而不是重新发现。
- **token-efficiency**:本次为摸清 team 与 summarize-project 两侧概念模型,并行派了两个 Explore 子代理,回传的两份报告体量都很大(数千行级的字段/引用摘录),其中相当一部分(如渲染层的 PlantUML 字面量、色板十六进制值、里程碑出图决策阶梯的完整判据)对"写一份需求规格"并非必需——需求层只需要实体名、字段名、必填档位与边界规则。可避免的消耗点:子代理提示应按字段投影方式限定回传粒度(只要实体/字段/档位/边界,显式排除渲染实现细节与示例代码),或分两阶段(先要实体清单,确认需要后再定向索取细节)。未做精确 token 计量,此处为定性判断,不编造数值。
