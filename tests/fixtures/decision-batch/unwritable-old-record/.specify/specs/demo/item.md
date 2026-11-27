# 演示不可写前例项

### PENDING — 演示不可写前例项

- **decision_class**: human-interactive
- **subject**: 演示不可写前例项
- **context**: 既往记录的选中项与当前建议默认不同，且旧记录载体不可写。
- **options**: 2
  - label: 保留 30 天
    consequences: 与既往选择相反
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/old-record.md
  - label: 保留 90 天
    consequences: 与既往选择一致
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/old-record.md
- **basis**: 与现状一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z