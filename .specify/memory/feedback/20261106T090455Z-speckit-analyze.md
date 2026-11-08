---
id: "20261106T090455Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261106T090000Z-086a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "086-script-interface-contract"
partial: false
created: "2026-11-06T09:04:55Z"
summary: "086 analyze 只读跨产物分析: 5 HIGH / 10 MEDIUM / 6 LOW; 零 CRITICAL; analyze gate 不通过, 需回环修 requirements 与设计文档的 clause 映射"
---

## Review
086 analyze 只读跨产物分析: 5 HIGH / 10 MEDIUM / 6 LOW; 零 CRITICAL; analyze gate 不通过, 需回环修 requirements 与设计文档的 clause 映射

## Optimization Points
- SC-006 计数等式不可满足; data-model V13-V22 的 clause 列系统性错位; 契约间 clause 交叉引用指向不存在或不匹配的条款; SC-012 的删除真实例外行肢在空登记下不可执行; coverage-baseline.txt 未被 tasks 阶段冻结; 计数漂移(38/207/208/431/7)与 A4/A6/Q3/Q6 的未修文本; 两份 checklist 无回指
