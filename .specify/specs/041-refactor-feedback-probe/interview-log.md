# Interview Ledger: .specify/specs/041-refactor-feedback-probe/requirements.md

- **Started**: 2026-08-15
- **Target artifact**: .specify/specs/041-refactor-feedback-probe/requirements.md
- **Mode**: special
- **Branches**: modeling, truth-source, class-partition, external-target
- **Recording**: overwrite-style; latest round wins
- **Status legend**: ⬜ open / 🔄 asked / ✅ settled / ⏭ deferred / ↩︎ retracted

| ID | Round | Branch | Question | dependsOn | Status | Decision | Artifact span | Superseded by |
|----|-------|--------|----------|-----------|--------|----------|---------------|---------------|
| D0 |  | modeling | Probe 两层建模(Class/Object)形态是否成立 | — | ✅ | 成立:Probe Class 定义一类插点的特征,Probe Object 为其在当前系统中的实例化;既有 49 个插点重构为 Object 并归类到具体 Class 之下(面试前已由既有澄清记录裁定,不重问) | ## Clarifications → Session 2026-08-14(初始 Probe 粒度); FR-001 |  |
| D1 |  | truth-source | probe 真源(单一事实来源)的载体形态受什么约束 | D0 | ✅ | files-based 单一真源:可由程序枚举、派生物(结构图)可重建;禁止数据库/向量存储(既有条文绑定,非本次访谈新决策) | FR-003(单一真源+程序枚举+派生物重建); ## Out of Scope(不引入数据库/向量存储;维持 files-based 引擎形态) |  |
| D2 |  | class-partition | Probe Class 的划分方案:按单元类型/生命周期点/切片维度如何组合 | D0 | ⬜ |  |  |  |
| D3 |  | external-target | 外部 probe 的目标单元标识方式:如何引用宿主项目自定义 Skill/Agent/Command | D0 | ⬜ |  |  |  |
| D4 |  | truth-source | probe 真源的载体位置与文件格式(目录/模板/schema) | D1 | ⬜ |  |  |  |
