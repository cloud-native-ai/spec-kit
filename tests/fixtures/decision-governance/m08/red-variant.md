# M-08 逆向样本 — 决策主体用了已登记变体 `spec-kit`

### D-001 — spec-kit 迁移评估

- **decision_class**: ai-autonomous
- **context**: 评估是否把本仓迁移到新的目录布局。
- **options**: 2
  - label: 迁移到新布局
    consequences: 结构统一，迁移期成本上升
    reversibility: reversible
    default: yes
    evidence: tests/fixtures/decision-governance/m08/red-variant.md
  - label: 保持现状
    consequences: 零迁移成本，结构继续分叉
    reversibility: reversible
    default: no
    evidence: tests/fixtures/decision-governance/m08/red-variant.md
- **chosen_option**: 保持现状
- **rationale**: 迁移收益未超过一次迭代的迁移成本
- **evidence**: tests/fixtures/decision-governance/m08/red-variant.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
