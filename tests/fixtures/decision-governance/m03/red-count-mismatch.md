# M-03 逆向样本 — 声明计数与选项条目数不一致

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 声明计数为 3，实际只有 2 个选项条目，集合不封闭。
- **options**: 3
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m03/red-count-mismatch.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m03/red-count-mismatch.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 声明计数与条目数不符
- **evidence**: tests/fixtures/decision-governance/m03/red-count-mismatch.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
