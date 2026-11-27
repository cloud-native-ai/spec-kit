# 演示块级缺陷

### PENDING — 演示计数不符项

- **decision_class**: human-interactive
- **subject**: 演示计数不符项
- **context**: 声明计数与条目数不一致。
- **options**: 3
  - label: 方案甲
    consequences: 代价较低
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 代价较高
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 无
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示缺类项

- **subject**: 演示缺类项
- **context**: 未声明决策类别。
- **options**: 1
  - label: 唯一方案
    consequences: 保持现状
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  forced: 只有一种可行做法
- **basis**: 无
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z
