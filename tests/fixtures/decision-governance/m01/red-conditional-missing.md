# M-01 逆向样本 — 传送族条件字段在触发成立时缺失

### D-001 — 派发实施取舍

- **decision_class**: ai-autonomous
- **context**: 决策已派发给子代理实施，状态已到 dispatched，但缺少 dispatched_at。
- **options**: 2
  - label: 交由子代理甲实施
    consequences: 与既有席位对齐，交接成本低
    reversibility: reversible — 可撤回重派
    default: yes
    evidence: tests/fixtures/decision-governance/m01/red-conditional-missing.md
  - label: 由父侧直接实施
    consequences: 无需交接，但占用父侧预算
    reversibility: reversible — 可转派
    default: no
    evidence: tests/fixtures/decision-governance/m01/red-conditional-missing.md
- **chosen_option**: 交由子代理甲实施
- **rationale**: 席位与职责匹配
- **evidence**: tests/fixtures/decision-governance/m01/red-conditional-missing.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: dispatched
