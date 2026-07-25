---
id: "20260725T081626Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "032-dogfooding-practice-20260725T161626"
scope: "local"
feature: "032-dogfooding-practice"
partial: false
created: "2026-07-25T08:16:26Z"
summary: "17/17 任务零延期完成；TDD 严格先失败后转绿（三批契约测试）；4 次分组提交留痕；SC 全 pass、回归零新增失败。运行本身即 Dogfooding 实证：两条真实摩擦点经既有机制记录并当场闭环。"
---

## Review
17/17 任务零延期完成；TDD 严格先失败后转绿（三批契约测试）；4 次分组提交留痕；SC 全 pass、回归零新增失败。运行本身即 Dogfooding 实证：两条真实摩擦点经既有机制记录并当场闭环。

## Optimization Points
- quickstart/指引中的 CLI 示例应在写入文档前先实际执行一次（本次 unit-id 自由格式示例被引擎校验拒绝，靠 dogfooding 亲历才暴露）；implement 流程可加"文档内命令样例须带一次真实执行证据"惯例。
- 收尾补写 verification 元数据时误用了 git --amend（应新建提交）；镜像/收尾类微修补统一走新提交，避免改写已生成的提交对象。
