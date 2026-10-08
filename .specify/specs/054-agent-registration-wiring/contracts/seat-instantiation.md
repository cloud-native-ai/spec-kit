# Contract: Seat Instantiation(席位实例化)— 054

**Scope**: FR-004(实例化半)、FR-006、FR-008、FR-013。流程主体:`skills/create-team/SKILL.md` + `references/create-mode.md`(create 流程);委托受端:`skills/create-agent/SKILL.md` 的 `AgentAuthoringRequest` 约定。

## C-1 席位解析与实例化(create 流程新步,插于 roster 步与 team.md 落地步之间)

- C-1.1: 对 team.md `agent:` 字段引用的每个席位,解析顺序 MUST 为:① `.specify/agents/{templates,instances}/` 已有持久定义(instance 优先)→ 直接引用;② 无持久定义 → 以 stage 帧为源,经 `create-agent` 委托入口(kind 走 instance 层)实例化到 `.specify/agents/instances/<slug>.agent.md`。
- C-1.2: 实例化 MUST 产出占位符全部解析的定义(帧内 `{{AGENT_NAME}}`/`{{PROJECT_NAME}}`/`{{ENVIRONMENT_PATHS}}`/`{{TASK_DESCRIPTION}}` 等全部填实),使既有渲染器不变量(拒绝未解析占位符)不被触碰。
- C-1.3: 席位实例 MUST 携带 `team-scope: <team-slug>`(framework-only 中性键,加入键集并 `renders_to_tools=False`);不设 `capacity-scope`(stage 帧非已注册 template)。
- C-1.4: 只实例化该 team.md 实际引用的席位;未被引用的 stage 帧、capacity 类 MUST NOT 被安装(US2 场景 5)。
- C-1.5: 实例化遇到与既有持久定义同名的 slug 时,MUST 冲突披露(点名两方)并停在该席位,不静默覆写;loader 的 instance-wins 语义不因此改变。

## C-2 渲染触发(create 流程终点)

- C-2.1: team.md 与席位实例落盘后,create 流程 MUST 直接执行渲染触发命令(见 `render-trigger-cli.md`),对当前宿主工具渲染;不留给用户"事后自己跑"的隐含步骤。
- C-2.2: 触发失败(非零退出)MUST 披露失败原因(校验器点名输出)并作为流程异常上送,不得静默跳过(FR-004;fast-fail)。
- C-2.3: 触发成功 MUST 在流程报告中给出 stats 摘要(rendered/backups/unmapped)。

## C-3 引用可判定(FR-008)

- C-3.1: `create-mode.md` Schema notes 的成员解析条款 MUST 更新为:成员 MUST 解析到 `.specify/agents/{templates,instances}/<slug>.agent.md`(instance 优先)或**建队时按 C-1 实例化的席位**;流程完成后,不可解析的成员即真断裂("unresolved members are surfaced as broken references" 由建队路径保证可判定)。
- C-3.2: 该条款 MUST 同时声明 `team-scope` 键的存在与用途(指向 `agent-definitions.md` 分类学条目,不重述键集)。

## C-4 来源追溯与孤儿可检(FR-013)

- C-4.1: `team-scope` 的键语义(存在性、格式、framework-only 性质)owner 为代码键集 `NEUTRAL_AGENT_METADATA_KEYS`;`skills/create-agent/SKILL.md` 的作者键集段 MUST 把它列入(instance 作者面知道此键)。
- C-4.2: 孤儿态 = `team-scope` 指向的团队目录不存在。检测/清理的执行形态由 `/speckit.tasks` 决定;本契约只钉可检性(键在、格式定、校验通过)。

## C-5 边界

- C-5.1: 帧与 capacity 类的**原始**模板(带占位符)MUST NOT 落入 `.specify/agents/templates/`(被拒方案 (a) 不复存在;渲染器拒绝占位符为既有不变量)。
- C-5.2: 本契约不改变 instance/template 层语义、manifest 语义、execution 层边界。

**验收示例前提**(供 /speckit.tasks 与 /speckit.implement 复测,非现态声明):实例文件出现在 `.specify/agents/instances/` 且 frontmatter 含 `team-scope`,依赖——键集已加入代码、create 流程步已落、渲染器校验通过。
