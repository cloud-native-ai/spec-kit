# M-01 逆向样本 — 未传递记录出现传递族时点占位

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 记录从未传递（not-transmitted），却带着 dispatched_at 占位。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m01/red-placeholder.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m01/red-placeholder.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 回滚窗口是首要约束
- **evidence**: tests/fixtures/decision-governance/m01/red-placeholder.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
- **dispatched_at**: 2026-11-26T01:00:00Z
