# Glossary Proposal (proposal-only) — 107-decision-governance

Per A-11 / FR-005 of the spec: proposals are recorded here and in the run evidence; they are **not written** to `.specify/glossary.md` before user confirmation. When confirmed, they are to be added through `glossary-utils.py --action add --origin auto --status proposed` after conflict detection (owner: `.specify/shared/workflow/glossary.md`).

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Decision Item | 决策项, decision item | 一个被呈现给人或由 agent 持有的选择：类别、完整名称与定位、上下文、封闭选项集、选中项、理由、证据、持有者；真源 `shared/definitions/decision-definitions.md` | auto | proposed |
| Decision Class | 决策类别, decision class | 决策持有者类别闭集：`human-interactive`（人持有）与 `ai-autonomous`（agent 在无用户时持有）；决定适用模板与检查集 | auto | proposed |
| Human-Interactive Decision | 人工交互式决策 | 由人持有的决策项；强调可读性、上下文、后果与完整定位 | auto | proposed |
| AI-Autonomous Decision | AI 自主决策, ai autonomous decision | 由 agent 在无用户在场时持有的决策项；强调封闭选项、决策谓词、显式假设与可机器核查证据 | auto | proposed |
| Decision Record | 决策记录, decision record | 决策项在既有载体中的归档投影；字段闭集 `decision_id` / `decision_class` / context / options / chosen option / rationale / evidence pointers / actor / timestamps / `transmission_status`；不是新存储 | auto | proposed |
| Decision Archive | 决策档案, decision archive | 封闭 Decision Producer Inventory × 既有载体的并集，加 `.specify/register.md` 索引；不是第二台账 | auto | proposed |
| Decision Producer | 决策生产者, decision producer | 封闭清单内会产生决策项的既有面；携带 obligation、载体与 owner | auto | proposed |
| Decision Transmission | 决策传递, decision transmission | 决策块搭乘既有派发载荷通道跨越 superagent→subagent 边并获确认的机制 | auto | proposed |
| Implementation Receipt | 实施回执, implementation receipt | 子代理回传中的 `implementation_receipt`：decision_id、实施摘要、证据指针、偏离声明；把实施钉回决策编号 | auto | proposed |

**Conflict check status**: not run as a write precheck because nothing is written at this stage. At implementation, run `glossary-utils.py --action detect-conflict` for each term before any proposed write.
