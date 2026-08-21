---
id: "20260820T155821Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "preset-consolidation-20260820"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-08-20T15:58:21Z"
summary: "将 4 个 team 预置重构为 2 个通用预置(capability-arena 能力竞技场:技能/命令/子代理的同题竞技+多角度变体探索+双轮裁判+收敛休止;project-cluster 跨项目协作集群:显式项目登记+每项目子代理按各自 harness 行事+统一协调面),并扫描改造 5 个实例团队(viz-skill-arena/draw-plantuml-optimizer/summar"
---

## Review
将 4 个 team 预置重构为 2 个通用预置(capability-arena 能力竞技场:技能/命令/子代理的同题竞技+多角度变体探索+双轮裁判+收敛休止;project-cluster 跨项目协作集群:显式项目登记+每项目子代理按各自 harness 行事+统一协调面),并扫描改造 5 个实例团队(viz-skill-arena/draw-plantuml-optimizer/summarize-project-optimizer 指向 capability-arena,cws-workspace-cluster 指向 project-cluster,requirement-implement-monitor 记 Lineage)。过程中暴露的耦合面已蒸馏为 team-presets.md 退役六步清单;matcher flow-style signals 漏读已修复;契约测试 142 项相关全绿,24 个基线失败与本次无关。

## Optimization Points
- # Optimization Points — create-team 预置重构运行 (2026-08-20)
- 1. **预置退役/改名曾有零规程**——本次 4→2 合并时,耦合面(SKILL.md Resources / team.md 命令模板 / confirmation-gates.md 治理表 / scan-confirmation-gates.py 路径模式 / 契约测试 / 实例团队 preset 字段)全靠人工扫描逐一发现。已蒸馏为 `references/team-presets.md` 的 "Retiring or renaming a preset" 六步清单。
- 2. **SKILL.md Resources 表曾长期漏列 skills-arena**(只列 3/4 预置)——预置枚举靠手维护,已在本次修正为 2 个新预置;后续可考虑由 match-team-preset.py --presets-dir 动态生成清单以免再漂移。
- 3. **match-team-preset.py 的 parse_frontmatter 曾只支持 block 风格 signals 列表**——预置若写 flow 风格(`signals: [a, b]`)会被静默漏读、匹配置信度无故归零。已修复为两种风格兼容并实测验证。
- 4. **实例团队的 `preset:` 字段无校验**——预置改名后旧 id 悬空无任何报错(silent rot)。已在退役清单第 2 步登记人工扫尾;后续可考虑在 improve-team 加载时校验 preset id 存在性并提示。
