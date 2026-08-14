# Feature Reference: 040-agent-metadata-portability

## Binding

- **Requirement**: `040-agent-metadata-portability`(`.specify/specs/040-agent-metadata-portability/requirements.md`)
- **Feature**: Feature 044 **Agent Metadata Portability**(`.specify/memory/features/044.md`)
- **绑定来源**: 2026-08-13 `/speckit.clarify` 第一轮 Q1(创建新 Feature 而非并入 Feature 033)。
- **相邻 Feature**: Feature 033 Agent Project Context Parameterization(互补层:033 渲染正文 Project Context 段,本 Feature 拥有元信息与分发管线;033 的渲染将来搭在本管线的刷新语义上)。

## Plan → Feature 映射

| Feature 044 承诺 | 本计划承接 |
|------------------|-----------|
| 元信息与正文程序可判定分离 | Technical Context D1 + contracts/neutral-metadata-schema.md |
| 中立词汇、消除 Qoder 方言 | D2 中立键集 + C-3/C-4 禁用词表 + [[STR-001]]/[[STR-002]]/[[STR-003]] 文档测试去工具化 |
| init 时按工具渲染真实文件 | D4/D8 + contracts/tool-mapping.md + contracts/render-pipeline.md |
| 三目录差别成文(Worker/Meta) | D6/D7 + contracts/relocation-taxonomy.md |
| 迁移不吞用户资产 | D5 + R-5/R-6/R-8 + SC-006 |

## 状态推进

- Draft → **Planned**(本命令,2026-08-13);Implemented 的所有权归 `/speckit.implement`。

## 术语表提案(写入需用户确认,术语表协议)

| 术语 | 拟登记含义 | origin / status |
|------|-----------|-----------------|
| Meta Agent(目录级) | `agents/` 预置集:操作其他技能/agent、可独立运行的框架维护型 agent | auto / proposed |
| Worker Agent(模板级) | 技能模板中面向问题域的 agent 模板(能力维度在 create-agent、职责维度在 create-team) | auto / proposed |
| 渲染产物 | init 时由中立元信息按目标工具格式生成的派生 agent 文件 | auto / proposed |
| 渲染清单 | `.specify/agents/.render-manifest.json`,漂移检测与失效清理的依据 | auto / proposed |
| "原 Agent" | "元 Agent"的语音易混淆变体(更正条目) | auto / proposed |

冲突检测结果:与既有 `Agent Template / Agent Instance / Agent Execution` 三条目无同名冲突;"Agent Template" 条目含义将随 T-1 划分修订(实现期,经用户确认)。
