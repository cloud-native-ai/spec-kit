---
id: "20260821T032029Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "self-improve-research-and-user-priority-20260821"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-08-21T03:20:29Z"
summary: "improve-skills 自改进:新增步骤 2(调研实现——全量读 SKILL.md/references/scripts + shape 门禁 + 优缺点/优化空间调研笔记,Hard Constraint 1)与步骤 6(按用户要求优化——用户要求优先于内置规范默认、规范级冲突显式上报,Hard Constraint 2),流程重述为 调研→按规范优化→按用户要求优化→最终检查;SKILL."
---

## Review
improve-skills 自改进:新增步骤 2(调研实现——全量读 SKILL.md/references/scripts + shape 门禁 + 优缺点/优化空间调研笔记,Hard Constraint 1)与步骤 6(按用户要求优化——用户要求优先于内置规范默认、规范级冲突显式上报,Hard Constraint 2),流程重述为 调研→按规范优化→按用户要求优化→最终检查;SKILL.md 203→158 行、正文 ≈4998→4062 tokens(预算 5000),Workflow 64→51 行;playbook 新增 Step 2/Step 6 并重编号锚点;FR-010 条款回归被契约测试捕获并修复;零回归经 failure-set diff 证明;干预账本已写入 ev-20260821-025731。

## Optimization Points
- # Optimization Points — improve-skills 自改进运行 (2026-08-21)
- 1. **契约钉住的不只是标题**:本次精简把 FR-010 钉住的 legacy-idiom 三枚举从 bullet 中删掉,
- `test_us3_improve_skills_has_legacy_idiom_detection_clause` 当场捕获并修复。教训:步骤 5 的
- "never slim a contract-mandated section"纪律已要求 grep tests/contract/,但该条款是
- **bullet 内枚举而非标题**——grep 时对条款关键词(如 SKILL_ROOT、.copilot/skills)也要查,
- 不能只查 heading。已在修复中把三枚举压缩保留为一行内联子句。
- 2. **基线失败集 diff 再次证明价值**:24 个既有失败掩盖下,肉眼无法区分新旧失败;
- failure-set diff 一次性给出零回归/回归结论(本次正是它暴露了第 1 点)。
- 3. (token-efficiency) 本次证据收集跑了全量 lanes 但 findings 对 improve-skills 无缺陷信号——
- 用户指令驱动型改进中,证据步骤的价值是确认"无潜伏失败"而非产出候选;开销合理。
