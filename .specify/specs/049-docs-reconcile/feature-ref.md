# Feature Binding: 049-docs-reconcile

**Requirement Key**: `049-docs-reconcile`
**Bound Feature**: Feature 037 — Docs Command
**Binding decided**: `/speckit.clarify` Session 2026-09-01
**Date**: 2026-09-01

## 绑定结论

需求 049（由合并前的 048 重编号）绑定既有 **Feature 037 Docs Command**,作为其**第四次 follow-up**,不新建 Feature。当前 Feature 总数以 `.specify/memory/features.md` 的自动派生头部为准。

## 绑定依据(证据)

| 依据 | 证据 |
|------|------|
| 037 的契约已治理本需求的核心对象 | `.specify/specs/033-docs-command/contracts/docs-command-template.md` C-18 已规定 create-docs(结构)/ improve-docs(内容)的配对边界 |
| improve-docs 无独立 Feature 归属 | `features.md` 全文无 improve-docs 条目;该技能经单次提交加入,从未注册 |
| 037 已有多次演进先例 | 2026-08-10 薄分发层重构 · 08-20 呈现层解耦 · 08-24 主题化导航 |
| 同构先例 | Feature 041 Goal Registry 吸收需求 038-goal-target 为扩展,未新建 Feature |

## 本需求在 Feature 037 中的位置

037 的演进轨迹与本需求的落点:

```
033-docs-command      → 命令 + 引擎 + 基线 + notes 生命周期(初版)
  ├─ 08-10 follow-up  → 核心逻辑抽入 create-docs 技能,命令降为薄分发层
  ├─ 08-20 follow-up  → 呈现层解耦到 create-pages;C-18 三分(结构/呈现/内容)
  ├─ 08-24 follow-up  → create-pages 主题化导航
  └─ 049(本需求;合并前 048) → 命令层升为三段式编排:目标结构声明 + 分型动作 + 双技能分发
```

本需求补上的是 08-20 三分之后遗留的**编排缺口**:C-18 划清了 improve-docs 的职责边界,但命令模板对其**引用为 0**——结构收敛与内容质量修复始终是两条互不知晓的通道,需用户分别触发。049 让二者在同一次调协中各就其位。

## 状态处理

Feature 037 当前状态 **Implemented**。本 plan **不回退**其状态:037 已交付的能力仍然成立,049（合并前 048）是增量演进。按 Feature 041 的先例(需求 038-goal-target planned 时 041 保持 Implemented 并在行注记记录),本轮只在 037 行追加 plan 阶段注记。

> `/speckit.plan` 的默认动作是 `Draft → Planned`。此处不适用:被绑定的 Feature 已是 Implemented,状态机不支持回退,且 037 的既有交付未被本需求废止。这一偏离在 037 行注记中显式记录,避免读者误以为漏了状态推进。

## 注册义务清单

| 义务 | 状态 |
|------|------|
| `features/037.md` § Related Specifications 交叉引用 049 | ✅ 已完成（合并期从 048 重编号） |
| `features.md` 037 行追加 049 绑定说明 | ✅ 已完成（合并期从 048 重编号） |
| `features.md` 037 行追加 **plan 阶段注记**(设计决策摘要) | ✅ 已于 plan 收尾完成 |
| `features/037.md` § Latest Review 追加本轮设计要点 | ✅ 已于 plan 收尾完成 |
| 本需求不新增 Feature；总数引用 Feature Index owner | ✅ Feature 049 来自上游 derive 能力,与本需求无关 |

## 交叉引用

- Feature 047 Framework Material Hygiene:`/speckit.sanitize` 只做 docs 引用存在性等正确性检查,内容编纂收敛移交 `/speckit.docs`——本需求扩大了后者的收敛面(纳入内容动作),该分工不变。
- Feature 028 Feedback Mechanism / 036 Dogfooding Practice:复用其 wrap-up 自省与 Loop A/B,零新增循环机器。
