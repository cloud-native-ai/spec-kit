# Record carrier — the round-trip decision D-001 (transmitted and implemented)

### D-001 — 选择迁移执行方案 plan-a

- **decision_class**: ai-autonomous
- **context**: 迁移窗口已定，需在两种执行方案中选择；两种方案都可回滚。
- **options**: 2
  - label: plan-a
    consequences: 停机窗口 30 分钟，回滚脚本已就绪
    reversibility: reversible — 可在 15 分钟内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/chain/carriers/round-trip.md
  - label: plan-b
    consequences: 停机窗口 45 分钟，人工回滚
    reversibility: reversible — 可在 45 分钟内回滚
    default: no
    evidence: tests/fixtures/decision-governance/chain/carriers/round-trip.md
- **chosen_option**: plan-a
- **rationale**: 谓词取停机窗口最小者；plan-a 的 30 分钟小于 plan-b 的 45 分钟。
- **evidence**: tests/fixtures/decision-governance/chain/carriers/round-trip.md
- **actor**: root
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: implemented
- **dispatched_at**: 2026-11-26T00:05:00Z
- **acknowledged_at**: 2026-11-26T00:06:00Z
- **implemented_at**: 2026-11-26T01:00:00Z
