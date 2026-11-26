# M-01 逆向样本 — 时点与 transmission_status 相位矛盾

### D-001 — 派发实施取舍

- **decision_class**: ai-autonomous
- **context**: 状态停在 dispatched，却已经出现 acknowledged_at，相位矛盾。
- **options**: 2
  - label: 交由子代理甲实施
    consequences: 与既有席位对齐，交接成本低
    reversibility: reversible — 可撤回重派
    default: yes
    evidence: tests/fixtures/decision-governance/m01/red-timepoint-phase.md
  - label: 由父侧直接实施
    consequences: 无需交接，但占用父侧预算
    reversibility: reversible — 可转派
    default: no
    evidence: tests/fixtures/decision-governance/m01/red-timepoint-phase.md
- **chosen_option**: 交由子代理甲实施
- **rationale**: 席位与职责匹配
- **evidence**: tests/fixtures/decision-governance/m01/red-timepoint-phase.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: dispatched
- **dispatched_at**: 2026-11-26T01:00:00Z
- **acknowledged_at**: 2026-11-26T02:00:00Z
