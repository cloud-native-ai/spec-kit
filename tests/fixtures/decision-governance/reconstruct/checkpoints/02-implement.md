# Checkpoint-carrier fixture — 一条可重建的决策记录

### D-001 — 阶段并发度裁定

- **decision_class**: ai-autonomous
- **context**: 检查点阶段的并发度裁定，记录落在检查点载体。
- **options**: 2
  - label: 并发度 3
    consequences: 吞吐提升，协调成本上升
    reversibility: reversible — 可降到 1
    default: yes
    evidence: tests/fixtures/decision-governance/reconstruct/checkpoints/02-implement.md
  - label: 并发度 1
    consequences: 最稳，吞吐最低
    reversibility: reversible — 可提升
    default: no
    evidence: tests/fixtures/decision-governance/reconstruct/checkpoints/02-implement.md
- **chosen_option**: 并发度 3
- **rationale**: 写目标互不相同
- **evidence**: tests/fixtures/decision-governance/reconstruct/checkpoints/02-implement.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
