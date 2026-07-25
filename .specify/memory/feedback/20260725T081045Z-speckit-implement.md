---
id: "20260725T081045Z-speckit-implement"
unit_id: "/speckit.implement"
unit_type: "command"
run_id: "032-dogfooding-practice-dogfood-T005"
scope: "local"
feature: "032-dogfooding-practice"
partial: false
created: "2026-07-25T08:10:45Z"
summary: "Dogfooding 亲历摩擦点两条：(1) rm 交互别名拦截非交互删除，需 \\rm -f 重试；(2) 按 quickstart 初稿用自定义 unit-id 记录 Loop B 发现被引擎格式校验拒绝（仅接受 /speckit.<cmd> 或 skill:<name>），暴露文档示例未对齐源码校验——已回改 quickstart 与指引文案。这是本原则'指引动作名以实际代码为准'条款的现场实"
---

## Review
Dogfooding 亲历摩擦点两条：(1) rm 交互别名拦截非交互删除，需 \rm -f 重试；(2) 按 quickstart 初稿用自定义 unit-id 记录 Loop B 发现被引擎格式校验拒绝（仅接受 /speckit.<cmd> 或 skill:<name>），暴露文档示例未对齐源码校验——已回改 quickstart 与指引文案。这是本原则'指引动作名以实际代码为准'条款的现场实证。

## Optimization Points
- 清理步骤统一使用 `\rm -f` / `\cp -f` 绕过交互别名（本次删除废弃契约文件被 rm -i 拦截一次）。
- Loop B 指引与 quickstart 中自定义来源必须写成 `skill:<product-scenario>` 形式（引擎 _UNIT_ID_RE 仅接受 `/speckit.<cmd>` 或 `skill:<name>`）；"my-product:checkout-flow" 之类自由格式会被拒绝——文档动作示例须以源码校验为准（Principle VIII）。
