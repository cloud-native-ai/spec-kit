# M-03 正向样本 — 单一可行选项携带 forced 声明与理由

### D-001 — 合规审计日志存储厂商选择

- **decision_class**: ai-autonomous
- **context**: 合规审计要求日志存储满足数据驻留条款；候选厂商经合规过滤后只剩一项。
- **options**: 1
  forced: 合规过滤后仅剩唯一可行厂商，选择由条款唯一决定
  - label: 厂商甲合规审计日志存储
    consequences: 满足数据驻留条款，成本高于市场均价
    reversibility: reversible — 合同按年签署，可到期不续
    default: yes
    evidence: tests/fixtures/decision-governance/m03/green-single-forced.md
- **chosen_option**: 厂商甲合规审计日志存储
- **rationale**: 条款过滤后无第二可行候选
- **evidence**: tests/fixtures/decision-governance/m03/green-single-forced.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
