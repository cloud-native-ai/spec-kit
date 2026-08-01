# Feature Reference: spec 035 → Feature 040

**Requirement**: `035-token-efficiency`(`.specify/specs/035-token-efficiency/requirements.md`)  
**Bound Feature**: Feature 040 — Token Efficiency Discipline(`.specify/memory/features/040.md`,Status: Draft → Planned by this plan)

## 映射

| Feature 040 关键面 | 本 plan 落点 |
|--------------------|--------------|
| 纪律单一事实源 | `shared/guidelines/token-efficiency.md`(+ 镜像);contracts/discipline-doc.md |
| Ambient 生效 | `templates/instructions-template.md` 引用节(C-D4) |
| 程序优先/摘要优先硬约束 | 存量审计 audit.md + top-5 整改(contracts/audit-and-gates.md) |
| 引擎摘要访问模式 | 引擎能力矩阵(data-model.md §4);feedback-utils `--contains`(C-M2) |
| 创作门槛 | create-*/improve-* 检查单与验证步骤检查项(C-A3) |
| 消耗观察 | feedback-step.md Reflect 扩展 + [[STR-001]] 标记 + `list --contains` 检索(contracts/feedback-marker.md) |

## 关联 Feature(非归属)

- 028 Feedback Mechanism:消耗观察的载体(条目结构/阈值协议零改动)。
- 038 Evidence Infrastructure:feedback 泳道消费 Token 观察,recurrence 信号复用。
- 032 Task Complexity Rubric:效率相邻——032 管思考深度校准,040 管上下文注入纪律,互不覆盖。
