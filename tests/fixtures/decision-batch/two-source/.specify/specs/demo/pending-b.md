# 演示待决策项（B）

### PENDING — 演示日志级别

- **decision_class**: human-interactive
- **subject**: 演示日志级别
- **context**: 演示环境日志噪音偏高，需要在下次演练前选定默认级别。
- **options**: 2
  - label: INFO
    consequences: 保留关键事件，噪音较低
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/evidence-a.md
  - label: DEBUG
    consequences: 记录最详细，噪音较高但便于排查
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/evidence-a.md
- **basis**: 下次演练以排查为主
- **origin**: OI-903 demo-producer
- **created_at**: 2026-11-20T00:00:00Z
