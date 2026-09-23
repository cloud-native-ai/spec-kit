---
id: "20260916T053329Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "20260916T000000Z-speckit-team-create-draw-two-layer-structure"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-two-layer-structure"
partial: false
created: "2026-09-16T05:33:29Z"
summary: "Goal-Based create 分支一次跑通:引擎枚举精确命中 draw-two-layer-structure(active/3 判据) → 四要素分析(既有 Target 全 dropped、open=0 → 成组路径不可用,走单团队) → preset 匹配 confidence low 不复用 → pattern 决策树 Q3 命中 serial → territory verify "
introspection_ref: "introspection-20260923T120035Z#F-15"
---

## Review
Goal-Based create 分支一次跑通:引擎枚举精确命中 draw-two-layer-structure(active/3 判据) → 四要素分析(既有 Target 全 dropped、open=0 → 成组路径不可用,走单团队) → preset 匹配 confidence low 不复用 → pattern 决策树 Q3 命中 serial → territory verify exit 0 → 落盘 team.md(4 席、1 Meta、三阶段 DAG、独立验证门)。范围守住了:viz-skill-arena 与 goal-definitions.md 逐字节未动(git status 双确认为空)。发现四处文档/模板缺口见优化点,其中两处是硬冲突(pattern 决策树 Q1 与 continuous L1 强制起步;Type 准则与 serial 模板 model-alignment 行),本次靠人工识别绕开而非文档指引。token-efficiency:同一文档分次小窗口重复读取两处。

## Optimization Points
- # /speckit.team create 运行优化点（draw-two-layer-structure，2026-09-16）
- **[模板缺口] `/speckit.team` 命令模板缺 `## Feedback` 与 `## Documentation` 两段，但它按分类判据是复杂命令。**
- `templates/commands/team.md` 只有 `## User Input` / `## Outline` / `## Handoffs`（grep 确认无 feedback-step、
- 无 docs-step 引用）。而 `.specify/shared/workflow/feedback-step.md` 的判据是「调用 scripts/CLI 工具、
- 产出另一流程消费的制品」即为复杂命令 —— 本次一条 create 路径就调了 `goal-utils.py list`、
- `match-team-preset.py`、`verify-territory-disjoint.py` 三个脚本，并产出 `team.md` 供 run 模式与
- summary 映射消费。结果：Feedback 只能靠被委派的 `skills/create-team/SKILL.md:221` 兜住，
- 而 Documentation 段**两边都没有**（create-team SKILL.md 亦无 `## Documentation`），
- docs-sync 评估在这条路径上根本不会触发。建议给 `templates/commands/team.md` 补这两段（指针形态），
- 改后跑 `scripts/python/regen-command-copies.py` 重生成四份工具副本。
- **[匹配器判据] `match-team-preset.py` 的 confidence 只看词面信号，会把用户已排除的形态重新端上来。**
- 本次 goal 文本含「持续」「长期」（出自 D7 的长期目标表述）→ 两个 preset 都拿到 `score: 2.0`、
- **`matchedSignals: []`**、confidence `low`。但 `capability-arena` 恰恰是用户在 D2 明确排除的
- 「竞技场优化」形态（"不是『这种画法好不好、能不能实现效果』这种小的层面上的优化"）。
- 若 confidence 落到 `medium`，create-mode 步骤 2 要求「present the top 2 candidates alongside the
- from-scratch option」，就会把一个已被排除的形态当成候选重新呈现。
- 建议：`matchedSignals` 为空时把 confidence 直接压到 `none`，或在输出里显式标注
- 「仅 pattern 关键词命中、无领域信号」，让调用方知道这个分数不代表形态契合。
- **[文档冲突] pattern 决策树与 continuous 的 L1 强制起步之间有一条未被指出的死路。**
- `patterns.md` 决策树把 Q1（长期/周期性）排在最前，「长期目标 + 持续改进」会直接命中 continuous；
- 但 `operating-loops.md` §1 规定 continuous **必须从 L1 报告态起步、不可跳级**，L1 的写权限仅为
- 「读、评、写 STATE.md 与 run report」且 `max_subagents_per_cycle: 0`。
- 于是任何**主体是有界交付物改动、只有尾部是长期运营**的工作，按决策树会被导向一个
- 在可预见几轮里做不了该工作的 pattern。本次靠人工识别才绕开（选 serial，把长期性交给 Goal 的
- lifecycle 承载）。建议在 Q1 处加一条判据提示：若工作主体是一次性的交付物改动、长期性只体现在
- 目标不设终止阈值，Q1 应判否，长期性由 Goal lifecycle 而非团队 pattern 承载。
- **[文档冲突] Type 判定准则与 serial 模板的 model-alignment 行互相矛盾。**
- `create-mode.md` 步骤 4：「a member that must **write** ... skill definitions MUST be `Meta`」、
- 「Decide each member's Type from **what it writes to**, never from its role name」；
- 而 `agent-serial-orchestration-template.md` 开头写「Each stage agent is a **Worker** running at the
- `executor` stage」。本次 S1 重构阶段要改六个技能的 SKILL.md（即技能定义），按准则该席必须 Meta，
- 按模板则是 Worker。我沿用了 `viz-skill-arena` 的既有解法（Worker 只产补丁到工作区，唯一 Meta
- supervisor 落 canonical）绕开冲突，但这是我自行找的解释，两份文档都没写。
- 建议在其中一处显式说明该冲突如何消解。
- **[token-efficiency] 同一文档分次小窗口重复读取。**
- `create-mode.md` 分两次读（1-60、60-140），`patterns.md` 分两次读（决策树段 + serial 段），
- 各自本可一次定位读完。未发生原文转储（evidence 走引擎投影、findings.json 只取 6 条的字段投影）；
- 确定性判断全部交引擎（goal list/validate/targets、preset 匹配、territory 校验、YAML 与模板可解析性校验）。
