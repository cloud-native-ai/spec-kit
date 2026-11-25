# Parked — sdd-observer agent（SDD 专用第三方观察者）

**寄存时间**: 2026-11-10 · **来源**: 用户在 095 运行期间的口述需求（原文要点如下）· **状态**: parked（095 收束后立项）

## 需求原文要点

- 定义一个 `sdd-observer` agent 定义：专门用来观察一个 SDD 的执行流程。
- 在确认启动 SDD 流程之后（如创建完 SDD git branch 之后），启动一个针对该 spec 开发流程的**专用 sdd-observer agent 实例**。
- sdd-observer 可以使用**内部 subagent** 作为 agent execution。
- 专门以**第三方视角**观察和记录整个 SDD 开发流程。
- 最后在对应的 `.specify/specs/NNN-<spec slug>/journal.md` 文件中记录整个过程。
- 必须**客观记录，不提供任何主动的评价或建议**。

## 处理计划

- 不在 095（super agent 相对角色）范围内实施——095 的 requirements 已冻结，扩围违反 SDD 纪律。
- 095 收束后：以 new feature 立项（编号 096+），运行 SDD 链；届时可直接复用 095 交付的 superagent 定义、角色边判定与身份转变注入清单（sdd-observer = 一个持 observer 角色的 superagent，派发 internal subagent 执行观察）。
- 立项时必须回答：观察者实例的启动时机与生命周期（与 line registry / state spine 的关系）、journal.md 的客观性构造（只记事件与证据指针，禁止评价/建议）、与 reporting-obligations 的边界、以及观察者自身的失败处理（观察者掉线不阻塞开发线）。

## 线索

- 与 095 的接口：`shared/definitions/superagent-definitions.md`（角色/边）、`reporting-obligations.md`（报告纪律）、`sdd-loop-driver`（阶段/哨兵/状态脊）、`line-registry.py`（实例身份）。
- 与 080–094 验证的接口：本 Park 条目本身是 095 运行的「运行中接收需求→寄存不扩围」纪律的实例。

## 立项记录（2026-11-10）

- 已作为独立 SDD 线启动（见对应的 096/097/098 状态脊与 U5 上送件）；运行至 analyze 门后按「一轮修复回环」规则停线，处置选项见各线 handoff。
