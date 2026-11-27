# 演示应答形态

### PENDING — 演示应答甲

- **decision_class**: human-interactive
- **subject**: 演示应答甲
- **context**: 应答演练：用户只对一项提出改选，其余按建议默认值结案。
- **options**: 2
  - label: 保留 30 天
    consequences: 存储成本较低，复查窗口较短
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 保留 90 天
    consequences: 复查窗口更长，存储成本更高
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 与现有备份策略一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示应答乙

- **decision_class**: human-interactive
- **subject**: 演示应答乙
- **context**: 应答演练：本项未被点名，按建议默认值结案。
- **options**: 2
  - label: INFO
    consequences: 保留关键事件，噪音较低
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
  - label: DEBUG
    consequences: 记录最详细，噪音较高但便于排查
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
- **basis**: 下次演练以排查为主
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z