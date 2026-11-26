# M-03 正向样本 — 封闭选项集（声明计数 2，五要素齐备，选中项为具名成员）

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 评估把数据库迁移窗口放在周末还是工作日夜间；两种处置都可逆，回滚窗口是首要约束。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足，需要安排值班
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m03/green-complete.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m03/green-complete.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 回滚窗口是首要约束
- **evidence**: tests/fixtures/decision-governance/m03/green-complete.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
