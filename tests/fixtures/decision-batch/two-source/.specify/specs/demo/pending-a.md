# 演示待决策项（A）

### PENDING — 演示数据保留期

- **decision_class**: human-interactive
- **subject**: 演示数据保留期
- **context**: 团队正在确定演示数据的保留周期，必须在月底归档前给出结论。
- **options**: 2
  - label: 保留 30 天
    consequences: 存储成本最低，但复查窗口较短
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/evidence-a.md
  - label: 保留 90 天
    consequences: 复查窗口更长，存储成本更高
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/evidence-a.md
- **basis**: 30 天与现有备份策略一致
- **origin**: OI-901 OI-902
- **created_at**: 2026-11-20T00:00:00Z
