# Record carrier — a re-decision supersedes the old record, which is preserved

### D-001 — 选择迁移执行方案 plan-a（随后被 D-002 取代）

- **decision_class**: ai-autonomous
- **context**: 迁移窗口已定，需在两种执行方案中选择；两种方案都可回滚。
- **options**: 2
  - label: plan-a
    consequences: 停机窗口 30 分钟，回滚脚本已就绪
    reversibility: reversible — 可在 15 分钟内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/chain/carriers/redecision.md
  - label: plan-b
    consequences: 停机窗口 45 分钟，人工回滚
    reversibility: reversible — 可在 45 分钟内回滚
    default: no
    evidence: tests/fixtures/decision-governance/chain/carriers/redecision.md
- **chosen_option**: plan-a
- **rationale**: 谓词取停机窗口最小者。
- **evidence**: tests/fixtures/decision-governance/chain/carriers/redecision.md
- **actor**: root
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: diverged
- **dispatched_at**: 2026-11-26T00:05:00Z
- **acknowledged_at**: 2026-11-26T00:06:00Z
- **implemented_at**: 2026-11-26T01:00:00Z
- **superseded_by**: D-002 (carrier: tests/fixtures/decision-governance/chain/carriers/redecision.md)

### D-002 — 重决：因新增区域约束改择 plan-b

- **decision_class**: ai-autonomous
- **context**: 区域约束变化使 plan-a 不再可行；重新决策。
- **options**: 2
  - label: plan-a
    consequences: 区域约束下不可行
    reversibility: reversible — 可在 15 分钟内回滚
    default: no
    evidence: tests/fixtures/decision-governance/chain/carriers/redecision.md
  - label: plan-b
    consequences: 停机窗口 45 分钟，人工回滚，满足区域约束
    reversibility: reversible — 可在 45 分钟内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/chain/carriers/redecision.md
- **chosen_option**: plan-b
- **rationale**: 谓词：区域约束可行者优先；仅 plan-b 满足。
- **evidence**: tests/fixtures/decision-governance/chain/carriers/redecision.md
- **actor**: root
- **created_at**: 2026-11-26T02:00:00Z
- **transmission_status**: not-transmitted
