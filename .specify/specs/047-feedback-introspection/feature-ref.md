# Feature Binding: 047-feedback-introspection → Feature 028

| 项 | 值 |
|----|-----|
| Requirement | `047-feedback-introspection` |
| Feature | **028 — Feedback Mechanism**(Implemented;027 初建、041 递进、047 递进) |
| 绑定裁定 | `/speckit.clarify` Session 2026-08-27(requirements.md ## Clarifications) |
| 反向登记 | `.specify/memory/features/028.md`(Related Specifications + Last Updated) |

## 需求 → 设计产物映射

| 用户故事 / FR | 设计产物 |
|---------------|----------|
| US1 场景化自省(FR-001..005, FR-011, FR-012) | `contracts/command-mode.md`(模式流程)+ `contracts/introspection-report.md`(报告 schema)+ `data-model.md`(Report/Finding) |
| US2 分流与处置(FR-006, FR-008) | `data-model.md`(RoutingDecision + 条目扩展字段)+ `contracts/engine-cli.md`(introspect-register C-1..C-6、dispose 扩展 C-7/C-8) |
| US3 上行包富化(FR-009) | `contracts/engine-cli.md`(package 扩展 C-9..C-12)+ `contracts/command-mode.md` C-9/C-10 |
| FR-007 报告持久化 | `data-model.md`(存储路径与生命周期)+ `contracts/introspection-report.md` C-1/C-2 |
| FR-010 红线 | `contracts/command-mode.md` C-6/C-7 + `contracts/engine-cli.md` C-12 |

## 对 Feature 028 的增量

- 闭环由"记录→管理→上行→消费"扩展为"记录→**自省**→管理→上行(富化)→消费";
- 引擎 13 动作 → 14 动作(+introspect-register),2 动作扩展(dispose/package);
- 命令模式 4 → 5;probe 注册表零变更(probe 按命令 × wrap-up 注册,不随模式细分);
- 红线全集不变(无网络/无自动传输/外部不上行/条目正文不改写)。
