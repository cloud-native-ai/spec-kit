# 演示两个批次的写隔离

### PENDING — 演示并发甲

- **decision_class**: human-interactive
- **subject**: 演示并发甲
- **context**: 批次一结案本项，批次二不得改写批次一的记录。
- **options**: 2
  - label: 方案甲
    consequences: 代价较低，可以回退
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 代价较高，可以回退
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 与既有做法一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示并发乙

- **decision_class**: human-interactive
- **subject**: 演示并发乙
- **context**: 批次一暂缓本项，批次二重新呈现并按建议默认值结案。
- **options**: 2
  - label: 方案甲
    consequences: 代价较低，可以回退
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 代价较高，可以回退
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 与既有做法一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z
