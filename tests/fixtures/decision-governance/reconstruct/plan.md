# Plan-carrier fixture — 一条可重建的决策记录（承重决策只交叉引用 T-NNN）

### D-001 — 迁移路径取舍

- **decision_class**: ai-autonomous
- **context**: 承重取舍的六字段在 T-020 记录中，本记录只交叉引用。
- **options**: 2
  - label: 一次性切换路径
    consequences: 停机 30 分钟，结构一次到位
    reversibility: reversible — 可回切旧路径
    default: yes
    evidence: tests/fixtures/decision-governance/reconstruct/plan.md
  - label: 双写过渡路径
    consequences: 停机 45 分钟，过渡期双写成本高
    reversibility: reversible — 可终止双写
    default: no
    evidence: tests/fixtures/decision-governance/reconstruct/plan.md
- **chosen_option**: 一次性切换路径
- **rationale**: 见 T-020
- **evidence**: tests/fixtures/decision-governance/reconstruct/plan.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
