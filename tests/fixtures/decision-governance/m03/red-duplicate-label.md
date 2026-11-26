# M-03 逆向样本 — 重复标签（两个选项使用同一标签）

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 两个选项被写成了同一标签，集合无法比较。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m03/red-duplicate-label.md
  - label: 周末迁移窗口
    consequences: 与上一项重复，无法区分
    reversibility: reversible — 可在 4 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m03/red-duplicate-label.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 标签重复使选择无法比较
- **evidence**: tests/fixtures/decision-governance/m03/red-duplicate-label.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
