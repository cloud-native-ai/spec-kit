# M-03 逆向样本 — 单一可行选项未声明 forced

### D-001 — 合规审计日志存储厂商选择

- **decision_class**: ai-autonomous
- **context**: 合规过滤后只剩一个候选，但记录没有声明 forced，伪装成多选。
- **options**: 1
  - label: 厂商甲合规审计日志存储
    consequences: 满足数据驻留条款，成本高于市场均价
    reversibility: reversible — 合同按年签署，可到期不续
    default: yes
    evidence: tests/fixtures/decision-governance/m03/red-single-without-forced.md
- **chosen_option**: 厂商甲合规审计日志存储
- **rationale**: 条款过滤后无第二可行候选
- **evidence**: tests/fixtures/decision-governance/m03/red-single-without-forced.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
