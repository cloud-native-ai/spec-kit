# Run-report-carrier fixture — 一条可重建的决策记录

### D-001 — 回归范围选择

- **decision_class**: ai-autonomous
- **context**: 运行报告的处置决策，记录落在 run report 载体。
- **options**: 2
  - label: 全量回归
    consequences: 覆盖完整，耗时最长
    reversibility: reversible — 可缩小范围重跑
    default: yes
    evidence: tests/fixtures/decision-governance/reconstruct/run-report.md
  - label: 定向回归
    consequences: 耗时短，覆盖有限
    reversibility: reversible — 可扩大范围重跑
    default: no
    evidence: tests/fixtures/decision-governance/reconstruct/run-report.md
- **chosen_option**: 全量回归
- **rationale**: 改动触及共享层
- **evidence**: tests/fixtures/decision-governance/reconstruct/run-report.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
