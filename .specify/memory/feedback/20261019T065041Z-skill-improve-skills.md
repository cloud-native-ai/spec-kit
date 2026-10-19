---
id: "20261019T065041Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "sdd-loop-driver-routing-20261019T065041Z"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-19T06:50:41Z"
summary: "修复 sdd-loop-driver 的路由缺陷：以技能名加功能描述加载时曾被误路由到 improve-skills 并直接改代码，跳过 U0–U6。新增触发语义、主导流程唯一、U0 缺省解析、U0.5 自检、HR7 流程不可替换与常见误路由表；fresh-context 只读子代理复测确认第一步为 U0 声明且禁止 improve-skills 直接编辑。"
---

## Review
修复 sdd-loop-driver 的路由缺陷：以技能名加功能描述加载时曾被误路由到 improve-skills 并直接改代码，跳过 U0–U6。新增触发语义、主导流程唯一、U0 缺省解析、U0.5 自检、HR7 流程不可替换与常见误路由表；fresh-context 只读子代理复测确认第一步为 U0 声明且禁止 improve-skills 直接编辑。

## Optimization Points
- 以技能名加功能描述加载时必须先写 U0 入口声明与阶段计划，禁止在 U0 前另起流程。
- 入口缺省解析：当前仓库 / 本地直驱 / 入口描述加 docs 加宪法为权威 / U1 自动探测，不得因参数不全切换流程。
- 新增 HR7 与 U0.5 自检，并以 fresh-context 压力测试验证路由文本可被新上下文正确理解。
