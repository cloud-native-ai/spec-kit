# M-02 正向样本 — 业务资源组 + region id 成对在场

### D-001 — 华北业务资源组扩容审批

- **decision_class**: human-interactive
- **context**: 同名资源组在多个 region 存在，定位信息按成对维度给出。
- **options**: 2
  - label: 扩容到 8 节点
    consequences: 峰值容量提升，成本上升
    reversibility: reversible
    default: yes
    evidence: tests/fixtures/decision-governance/m02/green-complete.md
  - label: 保持 4 节点
    consequences: 容量不变，成本不变
    reversibility: reversible
    default: no
    evidence: tests/fixtures/decision-governance/m02/green-complete.md
- **chosen_option**: 扩容到 8 节点
- **rationale**: 容量水位已超阈值
- **evidence**: tests/fixtures/decision-governance/m02/green-complete.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
- **same_name_conflict**: true
- **resource_locator**: business_resource_group=rg-prod-north; region_id=cn-beijing
