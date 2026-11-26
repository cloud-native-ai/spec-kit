# C-107 逆向样本 — chosen_option 与重放结果不符（记录被改写）

### D-001 — 迁移路径选择

- **decision_class**: ai-autonomous
- **context**: 两条迁移路径的预计停机时间已实测；判定规则取停机时间最小者，但选中项被改写。
- **options**: 2
  - label: plan-a
    consequences: 停机 30 分钟，迁移期一次性切换
    reversibility: reversible — 可回切到旧路径
    default: yes
    evidence: tests/fixtures/decision-governance/m03/ai-replay-mismatch.md
  - label: plan-b
    consequences: 停机 45 分钟，迁移期双写
    reversibility: reversible — 可回切到旧路径
    default: no
    evidence: tests/fixtures/decision-governance/m03/ai-replay-mismatch.md
- **chosen_option**: plan-b
- **rationale**: 判定规则取预计停机时间最小者。
  predicate: min(downtime_minutes)
  inputs: plan-a=30; plan-b=45
- **evidence**: tests/fixtures/decision-governance/m03/ai-replay-mismatch.md
- **actor**: driver-run@example
- **created_at**: 2026-11-26T00:00:00Z
- **transmission_status**: not-transmitted
