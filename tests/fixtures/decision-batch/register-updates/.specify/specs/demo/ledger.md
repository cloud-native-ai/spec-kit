# 演示登记与状态更新

### PENDING — 演示登记结案项

- **decision_class**: human-interactive
- **subject**: 演示登记结案项
- **context**: 登记册来源行 OI-801 联接到本块，结案后该行状态应点名批次与决策编号。
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
- **origin**: 登记行 OI-801
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示登记暂缓项

- **decision_class**: human-interactive
- **subject**: 演示登记暂缓项
- **context**: 登记册来源行 OI-802 联接到本块，本项在本次批次被暂缓。
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
- **origin**: 登记行 OI-802
- **created_at**: 2026-11-20T00:00:00Z
