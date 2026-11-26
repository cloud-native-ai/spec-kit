# C-205 逆向样本 — 决策记录复制了承重张力的六字段内容

### D-001 — 数据库迁移窗口选择

- **decision_class**: human-interactive
- **context**: 记录把承重张力的字段原样复制了进来，形成第二定义点。
- **options**: 2
  - label: 周末迁移窗口
    consequences: 业务低峰，回滚窗口充足
    reversibility: reversible — 可在 4 小时内回滚
    default: yes
    evidence: tests/fixtures/decision-governance/m01/red-tension-copy.md
  - label: 工作日夜间迁移窗口
    consequences: 影响面小，但回滚窗口只有 2 小时
    reversibility: reversible — 可在 2 小时内回滚
    default: no
    evidence: tests/fixtures/decision-governance/m01/red-tension-copy.md
- **chosen_option**: 周末迁移窗口
- **rationale**: 见 T-020 的六字段（本记录只应交叉引用，不应复制）
- **antithesis**: 把窗口放在工作日凌晨并接受更短的回滚窗口
- **binding_constraints**: pole_a: 回滚窗口 ≥4 小时；pole_b: 业务影响可控
- **evidence**: tests/fixtures/decision-governance/m01/red-tension-copy.md
- **actor**: maintainer@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
