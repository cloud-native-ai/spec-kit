---
id: "20260807T133132Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "l1-shape-gate-20260807"
scope: "local"
partial: false
created: "2026-08-07T13:31:32Z"
summary: "用户指出上一轮改进产出的 dispatch-workitem/SKILL.md 塞满实现细节，违反技能优化最佳实践，要求分析漏检原因并优化 improve-skills 本身。度量确认：该文件 10334 tokens（2 倍 L1 预算）、262/625 行在代码围栏内（42%）、含 112 行示例章节。漏检有三重成因且相互放大：(1) 作用域——瘦身规则原文只要求评估 existing sec"
---

## Review
用户指出上一轮改进产出的 dispatch-workitem/SKILL.md 塞满实现细节，违反技能优化最佳实践，要求分析漏检原因并优化 improve-skills 本身。度量确认：该文件 10334 tokens（2 倍 L1 预算）、262/625 行在代码围栏内（42%）、含 112 行示例章节。漏检有三重成因且相互放大：(1) 作用域——瘦身规则原文只要求评估 existing sections 是否移出，而上一轮是新写 ~190 行示例与命令，规则字面不覆盖新增内容；(2) 位置——规则是最长步骤 Step 4 的第 8 条巨型 bullet，而 improve-skills 自身正文超预算 56%，正落在其 constraint-placement.md 实测 75.8% 合规率的注意力低区，且该技能当时完全没有硬约束集中块；(3) 无客观条件——量化事实（L1<=5K tokens、代码块>5 行）只存在于 L2 reference，未打开就看不到数字，'是否够瘦' 没有判定。修复：新增 scripts/skill-shape.py 确定性门禁（先在 26 个技能语料上标定，并把契约强制块从预算中扣除）；把瘦身规则改为同时约束新增方向（新细节默认落 L2/L3）；新增 late-positioned ## Hard Constraints 块（7 条客观条件）；Step 6 增加强制门禁。并按新规则自举瘦身 improve-skills：抽出 references/loop-playbook.md，可控正文 7822→4751 tokens，自身门禁转为 pass。附带修掉 hardening-examples.md 末尾遗留的 </content></invoke> 工具调用标记。契约测试失败集与基线完全一致（19 failed/1008 passed），零回归。

## Optimization Points
- 规则存在但未生效的三重成因（作用域/位置/无客观条件）应成为 improve-skills 诊断
- 「约束未遵守」类问题的固定排查顺序：先问规则是否覆盖本次动作的方向（增/删），
- 再看规则位置是否落在注意力低区，最后看有没有可执行的判定数。仅重写措辞是无效修复。
- 「依赖 agent 自愿去读 reference 才能生效的纪律 = 未落地的纪律」。凡量化事实只存在于
- L2 的规则，都应在 L1 留一个数字或一条脚本调用，否则未打开该 reference 的运行永远看不到阈值。
- 门禁必须先在语料上标定再接线：本次 oversized-section 以 40 行为阻塞条件时命中 17/26 个技能，
- 会训练执行者忽略门禁；降为告警后阻塞项命中 9/26（后续修正为 7/26）。
- 另一半是「不可控项要从预算中扣除」——契约强制内联块（Feedback、Agent-Specific Configuration）
- 的 token 作者无法削减，计入预算会让门禁永久红灯。两者共同结论：
- 门禁的判定必须落在执行者真正能改变的量上。
