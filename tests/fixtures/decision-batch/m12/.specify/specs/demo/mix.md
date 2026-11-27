# 演示类别门

### PENDING — 演示自主项

- **decision_class**: ai-autonomous
- **subject**: 演示自主项
- **context**: 由代理在无人在场时持有的一类决策。
- **options**: 2
  - label: 方案甲
    consequences: 保持现状
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 改变现状
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 谓词驱动的既定做法
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示人工项

- **decision_class**: human-interactive
- **subject**: 演示人工项
- **context**: 由人持有的一类决策。
- **options**: 2
  - label: 保留方案
    consequences: 保持现状
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 更换方案
    consequences: 改变现状
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 保留方案与现状一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z