# M-04 正向样本 — 同载体密集编号 D-001、D-002，且均在 register 中登记

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 第一条决策记录。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m04/green-dense.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m04/green-dense.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 回滚窗口是首要约束
- **evidence**: tests/fixtures/decision-governance/m04/green-dense.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted

### D-002 — 迁移后回归范围选择

- **decision_class**: ai-autonomous
- **context**: 第二条决策记录。
- **options**: 2
  - label: 全量回归
    consequences: 覆盖完整，耗时最长
    reversibility: reversible — 可缩小范围重跑
    default: yes
    evidence: tests/fixtures/decision-governance/m04/green-dense.md
  - label: 定向回归
    consequences: 耗时短，覆盖有限
    reversibility: reversible — 可扩大范围重跑
    default: no
    evidence: tests/fixtures/decision-governance/m04/green-dense.md
- **chosen_option**: 全量回归
- **rationale**: 迁移面触及共享层
- **evidence**: tests/fixtures/decision-governance/m04/green-dense.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
