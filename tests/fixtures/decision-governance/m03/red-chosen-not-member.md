# M-03 逆向样本 — selected 项不是选项集中的具名成员

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: chosen_option 写了一个不在选项集中的标签。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m03/red-chosen-not-member.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m03/red-chosen-not-member.md
- **chosen_option**: 周五下午迁移窗口
- **rationale**: 选中项不在选项集中
- **evidence**: tests/fixtures/decision-governance/m03/red-chosen-not-member.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
