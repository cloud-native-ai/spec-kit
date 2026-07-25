---
id: "20260725T145345Z-skill-manage-project"
unit_id: "skill:manage-project"
unit_type: "skill"
run_id: "speckit-dogfood-init-20260725"
scope: "local"
feature: "032-dogfooding-practice"
partial: false
created: "2026-07-25T14:53:45Z"
summary: "首次对 spec-kit 自身完成 manage-project 全六步运行（dogfooding）：初始化模式建立 .specify/project/project.md 四要素基线，三图（WBS 15 节点、里程碑视图 6+2、进度甘特 10 任务包+6 里程碑）渲染校验通过，三图一致性自检两轮收敛；期间按用户指令将管理根目录从 docs/project-management/ 迁移至 .sp"
---

## Review
首次对 spec-kit 自身完成 manage-project 全六步运行（dogfooding）：初始化模式建立 .specify/project/project.md 四要素基线，三图（WBS 15 节点、里程碑视图 6+2、进度甘特 10 任务包+6 里程碑）渲染校验通过，三图一致性自检两轮收敛；期间按用户指令将管理根目录从 docs/project-management/ 迁移至 .specify/project/ 并同步技能定义、契约测试与注册表。

## Optimization Points
- SKILL.md/playbook 未强制甘特图 `today` 使用确定性锚定（`today is N days after start`）；本次运行初稿依赖渲染环境时钟导致参照线位置不可控，二次修正才达标。建议在 Step 4 进度甘特图必备项与 playbook §7 自检清单中明确"today 必须相对项目起点显式定位"。
- 里程碑嵌入进度甘特图的一致性要求目前仅靠 Step 6 自检兜底；本次初稿甘特图仅含 1/6 里程碑，返工一次。建议 Step 4 第 3 点直接要求"逐条复制里程碑视图的全部 happens 条目"，把一致性前置到生成时刻。
