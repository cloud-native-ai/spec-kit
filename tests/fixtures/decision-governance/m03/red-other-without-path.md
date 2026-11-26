# M-03 逆向样本 — `other` 选项没有 path

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 名为 other 的选项没有定义新增选项的路径，构成「其他」黑洞。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m03/red-other-without-path.md
  - label: other
    consequences: 未定义的新增路径，无法比较
    reversibility: unknown
    default: no
    evidence: tests/fixtures/decision-governance/m03/red-other-without-path.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 其余候选未枚举
- **evidence**: tests/fixtures/decision-governance/m03/red-other-without-path.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
