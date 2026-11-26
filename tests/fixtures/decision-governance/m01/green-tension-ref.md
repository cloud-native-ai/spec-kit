# C-205 正向样本 — 承重决策只交叉引用 T-NNN，不复制六字段

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 承重取舍的六字段在 plan 的 T-020 记录里，本记录只交叉引用。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m01/green-tension-ref.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m01/green-tension-ref.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 见 T-020（承重取见的六字段归 decision-tension 契约，本记录不复制）
- **evidence**: tests/fixtures/decision-governance/m01/green-tension-ref.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
