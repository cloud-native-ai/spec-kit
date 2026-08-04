# Project Glossary (项目词汇表)

> **Note**: This file is initialized by `/speckit.instructions` and lives beside `constitution.md` / `features.md`. It is the project's single, project-wide vocabulary anchor: it corrects voice/dictated input (homophones, easily-confused words) and doubles as a lightweight domain-knowledge dictionary. It is loaded as ambient context by every `/speckit.*` command via the Documentation Map. See `.specify/shared/workflow/glossary.md` for the correction / enrichment / conflict protocol.

## Authoring Rules

- **Common words are NOT recorded** — only project-specific / domain terms that carry special meaning here.
- **User edits are authoritative (以用户输入为准)** — manual entries win over automatic proposals and are preserved across regenerations; automatic proposals MUST NOT silently overwrite a `user` entry.
- **Conflicts require confirmation** — a new term that collides with an existing entry (same term/different meaning, or a homophone/near-duplicate) is written only after the user confirms the resolution.

## Column Definitions

| Column | Meaning |
|--------|---------|
| Canonical | The agreed project term (unique, case-insensitive). |
| Variants | Comma-separated homophones / easily-confused / dictation-error forms that anchor back to Canonical; `-` when none. |
| Meaning | Brief one-line domain definition. |
| Origin | `auto` (framework-proposed) or `user` (manually authored/confirmed). |
| Status | `proposed` (awaiting confirmation) or `confirmed`. |

## Glossary

| Canonical | Variants | Meaning | Origin | Status |
|-----------|----------|---------|--------|--------|
| Spec Kit | speckit, spec-kit, speck it | The SDD CLI toolkit distributed as specify-cli | user | confirmed |
| SDD | - | Spec-Driven Development: specifications drive implementation | user | confirmed |
| Constitution | - | Project governance principles at .specify/memory/constitution.md | auto | proposed |
| Feature Index | - | Single source of truth for project capabilities at .specify/memory/features.md | auto | proposed |
| Reconcile Engine | - | Diff-and-converge engine used by Spec Kit commands to align artifacts with desired state | auto | proposed |
| Task Complexity Rubric | - | Tiered effort-calibration framework embedded in .specify/instructions.md | auto | proposed |
| 程序优先 (Program-First) | program first, 程序优先原则 | Token 效率纪律之一:可用固定规则表达的文本/数据判断交由确定性程序执行,不送入大模型 | auto | proposed |
| 摘要优先 (Summary-First) | summary first, 摘要化访问 | Token 效率纪律之一:机器管理数据文件原文不整体注入大模型上下文,例行消费摘要/投影/节选 | auto | proposed |
| 升级阶梯 (Escalation Ladder) | escalation ladder, 访问升级阶梯 | 数据访问逐级放宽路径:摘要 → 定向节选 → 有界整读(整读须满足例外情形或记录理由) | auto | proposed |
| Static Structure | 静态结构 | 团队的 Role × Stage × Type 成员名册 | auto | proposed |
| Dynamic Structure | 动态结构, 拓扑结构, topology | 团队的协作模式(parallel/serial/iteration/continuous),即成员间的运行时协作关系 | auto | proposed |
| Team Goal | 团队目标, team 目标 | 团队的北极星目标:具体可验证、区别于 description、可刻意修改但不得漂移 | auto | proposed |
| Team Summary | 团队总结 | 把团队自身视作项目而产出的累积式状态总结,落在团队目录的 summary/ 交付目录 | auto | proposed |
| 工作项四态色板 | 四态色板, work item four-state palette | 已完成/进行中/延期/未开始 四态的统一颜色与冗余符号编码,颜色之外必配符号 | auto | proposed |
| Agent Template | agent模板, 能力模板, 抽象agent类, capacity template | Agent 三层分类法第一层:能力与行为框架描述,源码 agents/ 角色集由 specify init 安装到 .specify/agents/templates/;真源 shared/definitions/agent-definitions.md | user | confirmed |
| Agent Instance | agent实例, 落地定义, agent definition | Agent 三层分类法第二层:职责描述定义(.specify/agents/instances/*.agent.md、team 名册席位),引用 Agent Template 并绑定具体职责,由命令/技能实例化产生 | user | confirmed |
| Agent Execution | agent执行, 运行实例, subagent, 子代理 | Agent 三层分类法第三层:定义真正执行时的运行形态,持久产物在 .specify/agents/execution/(configs/scripts 归档,logs 不入库);三种模式(native/virtual/external)见 shared/definitions/subagent-definitions.md | user | confirmed |
