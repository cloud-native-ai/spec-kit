---
id: "20260804T133743Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "037-goal-registry-requirements-20260804T213000Z"
scope: "local"
feature: "037-goal-registry"
partial: false
created: "2026-08-04T13:37:43Z"
summary: "为「goal 提升为项目级一等概念」生成规格 `.specify/specs/037-goal-registry/requirements.md`(28 FR / 11 SC / 5 用户故事 / 2 Shared Strings / 1 澄清标记)与质量清单。达成命令声明目的:把一句概念级诉求落成可验证的需求切片,并按 house convention 对齐 036 的行文与结构。"
---

## Review
为「goal 提升为项目级一等概念」生成规格 `.specify/specs/037-goal-registry/requirements.md`(28 FR / 11 SC / 5 用户故事 / 2 Shared Strings / 1 澄清标记)与质量清单。达成命令声明目的:把一句概念级诉求落成可验证的需求切片,并按 house convention 对齐 036 的行文与结构。

起草前先用程序核实了三件事,而非照抄用户措辞:(1)「goal 分散」的实际规模——4 个存量团队**每个都在两处**写同一目标(frontmatter `goal:` + 正文 `## Goal`,即 4 个 goal 写成 8 份),团队域另有 12+ 文件讨论 goal 写法;(2) 保留标识符冲突——`--goal` **已被两支脚本占用且含义不同**(`build-summary-input.py` 指要聚合的 goal 身份,`match-team-preset.py` 指目标文本),`goal_slug` 已是 036 确立的身份键,故 FR-003 明确复用而不新造、FR-025 明确避开该选项名;(3) 宿主 CLI 的 `/goal` 在本仓库**无法核实**(`docs/reference/cli/` 未记载、仓库无实现),故按 Principle VIII 把它写成"须以官方文档核实后再实现"的 FR-019 并保留唯一一个澄清标记,而不是凭记忆编一个配置格式。

最有价值的一步是主动暴露与刚落地需求的碰撞:036 数小时前刚把 `.specify/project/goal/<goal-slug>/` 作为总结交付目录写进约 12 个源文件与 10 个测试文件,而本需求用户指定的归档位置是 `.specify/goal/`——两者仅差一层目录、语义却相反(输入 vs 输出)。我把它作为高影响待裁决项连同三个选项与各自代价一并提出,用户给出了第四种更好的方案:**用 `.specify/goal/` 收编 `.specify/project/goal/`**。这一裁定直接与草稿的 FR-015("MUST NOT 改变 036 的交付目录布局")矛盾,我改的是那条 FR 而非在其上叠加例外,并新增 FR-026/027/028 承载迁移、定义与总结的结构分离、以及"迁移不得削弱 036 既有断言";迁移面在承诺之前先实测为 37 个文件并写成 SC-011 的基线。

产出后做了机械复核:FR 连续无重号、SC 与 Source 11/11 配对、STR 全部定义且被引用、标记数 1(上限 3)、零模板占位符,并专门跑了一次"是否仍有禁止迁移交付目录"的矛盾扫描。glossary 按协议提出 4 项(3 新增 + 修订 Team Goal 释义)并经用户确认后写入,同时顺手修正了 Team Summary 一行——它仍写着已被 036 取代的"团队目录 summary/"位置。

## Optimization Points
- Outline 第 5 步的"house conventions 采样"要求参考**最高编号的既有规格**,但没要求检查该规格是否**刚刚落地且与本需求存在实体冲突**。本次 036 在数小时前才合并,其 `.specify/project/goal/` 已进入约 12 个源文件与 10 个测试文件;若只按"采样行文风格"执行,极可能写出一份与刚落地路径并列冲突的规格,而冲突要到 plan 甚至 implement 才暴露。建议该步补一句:采样时 MUST 同时对本需求引入的**路径、标识符、目录**做与近期规格的碰撞检查,并把发现的碰撞写成待裁决项而非 Assumption 里的一句备注。
- 保留标识符检查(第 5 步 5)只说"grep 该名称",没说**同名但语义不同**也算冲突。本次 `--goal` 在两支脚本里已有两种不同含义(聚合身份 vs 目标文本),这不是"未被占用",而是比未占用更危险——第三种语义会让三处互相误用。建议把该条从"是否存在同名"升级为"是否存在同名**或**同名不同义",后者必须给出替代名并记入 Assumptions。
- 命令允许"informed guess"并把 `[NEEDS CLARIFICATION]` 限为 3 个,但没区分**可推断的缺省**与**外部系统的事实**。本次宿主 CLI `/goal` 的契约属后者:仓库内无实现、docs 未记载,任何"合理默认"都是编造,与 Principle VIII 直接冲突。我因此只保留这一个标记,其余候选全部降为 Assumption。建议明确:涉及外部工具/系统能力的未知 MUST 用标记而非 informed guess,且理由写明"无法在本仓库核实"。
- Glossary 步骤要求"at wrap-up 提出新术语并经用户确认",但未要求检查新术语是否**改变既有条目的释义**。本次新增项目级 `Goal` 直接把既有 `Team Goal` 从"团队的北极星目标(定义)"降为"对项目级 Goal 的引用",若只新增不修订,词汇表会同时存在两个互相矛盾的定义。我把"修订 Team Goal 释义"作为一个可选项交用户确认。建议该步补一句:新术语与既有条目存在包含/取代关系时,MUST 同时提出对既有条目的修订。
- 顺带发现一处既有词汇表陈旧:`Team Summary` 一行仍写"落在团队目录的 summary/ 交付目录",而 036 已把它改为按 goal 索引。说明词汇表条目会随实现漂移而无人复核。建议在 Glossary 协议里加一条轻量规则:凡本次改动触及某既有术语所描述的机制,MUST 顺带复核该条目是否仍然成立。
- token-efficiency: 起草前的三项核实全部用一次性批量 grep/循环完成(团队 goal 承载位统计、保留标识符扫描、迁移面计数),未通读任何团队文件或 036 的规格全文;house convention 只取 036 的标题清单(`grep -n '^#'`)而非整读 314 行;规格产出后的结构核验用一段 Python 一次性输出 FR 连续性/SC 配对/STR 解析/标记计数/占位符/矛盾扫描六项。可改进点:我先写完整份规格再整合用户裁定,导致 FR-015 等条目需要回改;若把"高影响待裁决项"在起草**之前**问出来(本次的路径命名完全可以先问),可省去一轮返工——命令的 Outline 把澄清完全放在 clarify 阶段,但对"与刚落地实现冲突"这类项,提前问的收益明显大于流程整齐。
