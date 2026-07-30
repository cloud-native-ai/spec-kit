---
title: "问题诊断:Type-follows-Stage 规则将流程阶段与抽象层次错误耦合"
created: 2026-07-30
expires: 2026-09-28
status: resolved
target: "skills/create-team/references/conceptual-model.md"
tags: [conceptual-model, agent-team, type-system, diagnosis]
---

# 问题诊断报告:Type-follows-Stage 派生规则的概念错误

> **已修复(2026-07-30)**:按**方案 A** 实施完毕。派生规则改为"按操作对象判定"的判据规则,
> 保留 Team Supervisor 恒 Meta 这一半正确耦合。沿扩散路径逐层修正:规范(conceptual-model.md)
> → 4 个 stage/triad 模板 → 7 个 role 模板 + 7 个 agent 文件 → 3 个 preset → 2 个实例团队
> → design.md(含 Role×Stage 矩阵重判)→ conformance 场景。另修复根因:`create-team/SKILL.md`
> 组建花名册的步骤此前**从未说明如何判定 Type**,已补入显式判据指令。
> 验证:全量测试失败集与基线一致(74),零新增失败;`skills/` ↔ `.specify/` 镜像 `diff -rq` 一致。

## 1. 问题现象

在 `/speckit.team run cws-workspace-cluster` 的运行预览中,用户发现团队成员
`consistency-checker`(stage: evaluator)被标记为 `type: Meta`,但其实际职责是
"跨仓一致性判定与结论分类"——操作对象是**具体业务信息**(各仓库的分支策略、
工作区脏度、构建产物新鲜度),按 Meta/Worker 的原始定义应为 **Worker**。

## 2. Meta/Worker 的原始定义(判别基准)

Meta 与 Worker 的区分是**抽象层次**(纵向分层),不是任务分工(横向分站):

- **Meta**:操作对象只能是其他 agent、skill、或定义 agent/skill 的项目配置。
  不接触具体业务信息。
- **Worker**:操作对象是业务工件与业务信息本身。

判别一个 agent 的 Type,问的是"它的操作对象处于哪个抽象层次",而不是
"它在流程的哪一站"。

## 3. 根因分析

### 3.1 直接原因(源头规则)

`skills/create-team/references/conceptual-model.md:11` 定义了 Type-follows-Stage
派生规则:

> **Type** — `Worker` or `Meta`, **derived from Stage** (Type-follows-Stage):
> `executor → Worker`, `evaluator → Meta`, `optimizer → Meta`.

该规则把两个**正交维度**捆绑成了单向派生关系:

| 维度 | 回答的问题 | 性质 |
|------|-----------|------|
| Stage(executor/evaluator/optimizer) | 它在协作流程的哪一站? | 横向分工 |
| Type(Worker/Meta) | 它的操作对象是业务还是 agent 系统本身? | 纵向分层 |

"evaluator 必然 Meta"隐含假设"评估行为一定发生在 agent 系统层"。反例即本案:
consistency-checker 评估的是**业务工件**(仓库状态),是业务层评估者——
evaluator-stage 的 Worker。对照组:team-supervisor 抽查 subAgent 结论的证据形态、
派发与打回 subAgent,操作对象是 agent 及其产出的元属性,才是真正的 Meta。

### 3.2 规则如何形成(历史沿革)

- 该耦合在 spec `023-agent-framework-redesign` 中被定为规范性契约
  (FR-004、contract C3),动机是"capability follows role"——防止编排者
  越界执行(orchestrator-is-not-implementer,见 research.md RD-4)。
- 防越界本身是正确诉求,但被过度概括为"evaluator/optimizer 一律 Meta",
  丢失了"评估对象处于哪一层"这个判据。
- 后续 `026-agent-team-management` 的 data-model、四个 stage 模板、
  三个 team preset 均继承该规则,错误随之扩散。

### 3.3 错误扩散路径

```
023 spec 契约 C3(源头)
  → conceptual-model.md:11(现行规范)
  → agent-stage-evaluator-template.md:14(模板固化 Type: Meta)
  → teams/*.md(workspace-cluster / artifact-optimizer / process-monitor)
  → 实例化团队 team.md(cws-workspace-cluster、draw-plantuml-optimizer)
```

## 4. 影响面清单

| 层 | 文件 | 问题点 |
|----|------|--------|
| 规范 | `skills/create-team/references/conceptual-model.md:11`(+ `.specify/` 镜像) | 派生规则本体 |
| 模板 | `skills/create-team/templates/agent-stage-evaluator-template.md:14`(+ 镜像) | 固化 `Type: Meta` |
| 模板 | `skills/create-team/templates/agent-triad-orchestration-template.md:25`(+ 镜像) | 复述派生规则 |
| 预置 | `teams/workspace-cluster.md`、`artifact-optimizer.md`、`process-monitor.md`(+ 镜像) | evaluator 成员标 Meta |
| 实例 | `.specify/teams/cws-workspace-cluster/team.md:24` | consistency-checker 误标 Meta |
| 实例 | `.specify/teams/draw-plantuml-optimizer/team.md` | 需逐成员按操作对象重判 |
| 文档 | `docs/reference/agents/design.md:36,69` | 向用户解释了错误规则 |
| 测试 | `tests/scenarios/conceptual-model/role-stage-type-conformance-scenario.md` | 断言错误耦合(V2/C3) |
| 归档 | `.specify/specs/.archive/023-*`、`026-*` | 历史记录,建议不改(见 §5) |

注意镜像纪律:`skills/` ↔ `.specify/skills/` 是独立 git 副本,修改后需
`diff -rq` 验证字节一致。

## 5. 修复方案

### 方案 A(推荐):Type 独立判定,Stage 仅提供默认值

把派生规则改为**判据规则**:

> Type 由 agent 的**操作对象抽象层次**独立判定——操作对象为其他 agent/skill/
> agent 配置 → Meta;操作对象为业务工件与业务信息 → Worker。
> Stage 不决定 Type,只提供**默认倾向**:executor 默认 Worker;optimizer
> (team-supervisor)因其操作对象天然是 agent 系统,恒为 Meta;evaluator
> 按评估对象判定(评业务工件 → Worker,评 agent 表现/团队结构 → Meta)。

改动:conceptual-model.md 规则改写;evaluator 模板 Type 字段改为"按操作对象
判定"并给出两例;三个 preset 与两个实例团队逐成员重判;design.md 同步;
conformance 场景测试改为断言新判据;`optimizer → Meta` 保留(supervisor 的
操作对象确实是 agent 层)。

- 优点:保留了 023 的防越界本意(supervisor 恒 Meta),只解开错误的那一半耦合;
  改动面可控。
- 缺点:Type 不再可机械推导,创建团队时需要一次人为/模型判断。

### 方案 B(最小改动):仅修实例,规范加例外注记

只改 cws-workspace-cluster 的 consistency-checker 为 Worker,在
conceptual-model.md 加一条例外说明。

- 优点:改动最小。
- 缺点:规范与实例长期矛盾,preset 每次实例化都会复现错误;不推荐。

### 方案 C(彻底解耦):Type 完全独立声明,废除 Type-follows-Stage

每个成员必须显式声明 Type,规范只给判据不给任何派生。

- 优点:概念最干净。
- 缺点:失去默认值便利;需重审所有模板/契约措辞;历史契约 C3 的规范性
  引用全部要重写,改动面最大。

### 共同注意事项

1. 归档 specs(`.archive/023`、`026`)是历史事实记录,不回改;在
   conceptual-model.md 的修订说明中标注"取代 023-C3 的耦合定义"即可。
2. 修复属于 High-stakes 级(改共享概念模型 + 规范性测试),应走
   spec/plan 流程或至少获得用户确认后实施。
3. 修改 `skills/` 后必须同步 `.specify/skills/` 镜像并 `diff -rq` 验证。
4. 测试基线纪律:先跑全量测试记录基线,再改 conformance 场景。

## 6. 结论

这是一次**概念建模层面的源头性错误**:把"流程阶段"(横向)与"抽象层次"
(纵向)两个正交维度错误地绑成派生关系,导致业务层评估者被系统性误标为 Meta。
推荐按方案 A 修复——恢复 Type 的独立判据,保留 optimizer→Meta 这一半的
正确耦合,并沿"规范 → 模板 → 预置 → 实例 → 文档 → 测试"的扩散路径逐层修正。
