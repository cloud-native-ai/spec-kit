---
id: "20260725T152003Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "manage-project-agile-loop-20260725"
scope: "local"
partial: false
created: "2026-07-25T15:20:03Z"
summary: "基于用户方向（敏捷管理循环、复用 spec-kit 概念、预留 Jira/CI-CD/SCM 扩展点）与 dogfood 首跑证据（today 时钟依赖返工、里程碑 1/6 缺失返工、两次手写相同提取代码）完成 manage-project 定向改进：SKILL.md 新增管理循环章节+概念映射表+Step 7，playbook 新增迭代记录骨架、§10/§11 与标准渲染校验命令，两条运行回归教"
---

## Review
基于用户方向（敏捷管理循环、复用 spec-kit 概念、预留 Jira/CI-CD/SCM 扩展点）与 dogfood 首跑证据（today 时钟依赖返工、里程碑 1/6 缺失返工、两次手写相同提取代码）完成 manage-project 定向改进：SKILL.md 新增管理循环章节+概念映射表+Step 7，playbook 新增迭代记录骨架、§10/§11 与标准渲染校验命令，两条运行回归教训固化为生成时规则；契约测试 27→32 全绿，实例文档补齐迭代 1 行，镜像同步。

## Optimization Points
- `assert_ordered` 步骤有序性契约按子串匹配 "Step N"，正文散文中对后续步骤的字面前向引用（如"留待 Step 6 自检"）会误触发失败。可复用教训：技能工作流散文避免字面步骤号前向引用，或将有序性断言锚定到 `### Step N` 标题级别而非全文子串。
- 本次改进以"锚点而非副本"原则映射 spec-kit 概念，但未对目标技能做一次真实更新模式运行来验证迭代记录追加行为；下次真实执行 manage-project 更新模式时需验证 Step 7 迭代行追加与"只追加不改写"规则的实际可操作性。
