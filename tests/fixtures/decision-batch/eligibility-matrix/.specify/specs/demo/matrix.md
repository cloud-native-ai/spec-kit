# 演示资格矩阵

### PENDING — 演示矩阵合格项

- **decision_class**: human-interactive
- **subject**: 演示矩阵合格项
- **context**: 合格项：块完整、恰一个可逆默认、无来源与前例冲突。
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

### PENDING — 演示矩阵不可逆项

- **decision_class**: human-interactive
- **subject**: 演示矩阵不可逆项
- **context**: 默认选项一旦执行不可撤销，必须由用户显式选择。
- **options**: 2
  - label: 方案甲
    consequences: 一步到位，但不可撤销
    reversibility: irreversible
    default: yes
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 分步执行，可以回退
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 一步到位更省时
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示矩阵无默认项

- **decision_class**: human-interactive
- **subject**: 演示矩阵无默认项
- **context**: 两个备选都没有获准成为默认，必须由用户显式选择。
- **options**: 2
  - label: 方案甲
    consequences: 代价较低
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
  - label: 方案乙
    consequences: 代价较高
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/ref.md
- **basis**: 两种做法各有取舍
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示矩阵前例冲突项

- **decision_class**: human-interactive
- **subject**: 演示矩阵前例冲突项
- **context**: 既往记录选择了更长的保留期，与当前建议默认不一致。
- **options**: 2
  - label: 保留 30 天
    consequences: 与既往选择相反
    reversibility: reversible
    default: yes
    evidence: .specify/specs/demo/prior.md
  - label: 保留 90 天
    consequences: 与既往选择一致
    reversibility: reversible
    default: no
    evidence: .specify/specs/demo/prior.md
- **basis**: 与现状一致
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z

### PENDING — 演示矩阵不完整项

- **decision_class**: human-interactive
- **subject**: 演示矩阵不完整项
- **options**: 2
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
- **basis**: 缺少上下文时不能形成完整呈现
- **origin**: demo-producer
- **created_at**: 2026-11-20T00:00:00Z