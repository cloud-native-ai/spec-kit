---
id: "20261016T190240Z-sdd-project-setup-run-xuanji-robot"
scope: "session"
source: "skill:sdd-project-setup"
tags: ["sdd-project-setup", "reconcile", "xuanji-robot", "improvement-points"]
title: "sdd-project-setup run on xuanji-robot: complete + 2 improvement points"
created: "2026-10-16T19:02:40Z"
summary: "对 xuanji-robot 的调协运行完整完成（S1 complete → S4 全绿 → S5 候选清单落 04_知识管理/tmp/）。两条改进点待吸收：① setup-recipes S3+ goal 项与 manage-goal 用户著作权条款冲突；② 旧版安装项目缺 run-determination/exec-quant 引擎需声明降级。feedback 引擎对本 skill unit 报 no probe object（.qoder 外部层技能未进 probe 注册表），改以本笔记承载。"
---

2026-10-17 skill:sdd-project-setup run=xuanji-robot-20261017（run_id 对应 run-determination 记录 cp-xuanji-robot-20261017）：

- **运行结果**：xuanji-robot 调协 grade complete→complete；已执行动作 = /speckit.instructions 刷新（历史蒸馏证据触发，目标仓提交 bc0bc06）+ /speckit.history 首蒸（4/4 会话 → .specify/history/ 四文件）；跳过项全部声明（constitution/sanitize/feature/docs/research）；goal 项跳过待用户（engine 在位、objective 须用户陈述）。
- **改进点 ①（setup-recipes）**：S3+ 强化序列的 goal 行隐含「自动定义 3–5 个目标」，与 manage-goal create 面的显式条款「objective 与切片由用户陈述，绝不代拟」冲突。本次按 lex specialis 处理（跳过+声明+候选首位）。建议在 setup-recipes.md S3+ goal 行加注：「goal 触发时只登记缺口与候选，objective 待用户陈述后经 /speckit.goal create 执行」。
- **改进点 ②（兼容性）**：客户端项目安装若早于 Run Determination/Exec Quant 机制（如 xuanji-robot，commit c8d29087, stamped 2026-09-20），目标仓缺 run-determination.py/exec-quant.py，S4 五族检查与命令 wrap-up 的 step 1–2 无法执行——须按缺记录降级显式声明，不得静默跳过。本次已在目标仓 instructions 会话笔记与本笔记双处声明。
- **附**：feedback-utils 对 `skill:sdd-project-setup` 在框架仓与客户端仓均报 `no probe object for unit`（技能属 `.qoder/skills` 外部层、未进 probe-definitions 注册表，而其 SKILL.md 内嵌 wrap-up 要求调用引擎）——probe 注册面与 .qoder 外部技能的 wrap-up 编译产物之间存在覆盖缺口，建议 probe-definitions 增补或 wrap-up 编译时对外部技能豁免步骤 3。
