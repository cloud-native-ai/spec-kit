# M-02 逆向样本 — same_name_conflict 为 true 而 resource_locator 为空

### D-001 — 华东业务资源组扩容审批

- **decision_class**: human-interactive
- **context**: 同名资源组在多个 region 存在，需按定位信息区分后再审批扩容。
- **options**:
  - label: 扩容到 8 节点
    consequences: 峰值容量提升，成本上升
    reversibility: reversible
    default: yes
    evidence: tests/fixtures/decision-governance/m02/red-empty-locator.md
  - label: 保持 4 节点
    consequences: 容量不变，成本不变
    reversibility: reversible
    default: no
    evidence: tests/fixtures/decision-governance/m02/red-empty-locator.md
- **chosen_option**: 扩容到 8 节点
- **rationale**: 容量水位已超阈值
- **evidence**: tests/fixtures/decision-governance/m02/red-empty-locator.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
- **same_name_conflict**: true
- **resource_locator**:
