# Contract: Modify-Time Seat Backfill(modify 时席位回填)— 054

**Scope**: FR-014。流程主体:`skills/improve-team/SKILL.md` 的 modify 流程(`/speckit.team modify` 的受端技能,`templates/commands/team.md:45,52` 既有路由)。从句形态:`md-bold-closed`(语法真源 `shared/definitions/contract-clause-definitions.md`)。

## § 触发与范围(opt-in)

**C-1**: 回填步只在用户显式发起的 `/speckit.team modify` 流程内执行;MUST NOT 自动扫描未被本次 modify 触及的团队。(FR-014 / US2 场景 6 后半)

**C-2**: 对本次 modify 目标团队的 team.md,每个 `agent:` 引用按 `seat-instantiation.md` C-4..C-7 的同序解析与同约束实例化:已有持久定义 → 直接引用;缺失 → 补实例化(占位符全解析、`team-scope` 齐、冲突披露不覆写)。

## § 回填后动作

**C-3**: 补实例化完成后 MUST 执行渲染触发(命令契约 `render-trigger-cli.md`,对当前宿主工具),失败披露不跳过。

**C-4**: modify 报告 MUST 区分:直接引用的既有席位数、本次补实例化的席位数、渲染 stats 摘要。

## § 一致性与边界

**C-5**: 回填产出的席位实例与建队产出同构(同校验、同 `team-scope`、同孤儿可检性)——两条路径共享 `seat-instantiation.md` 的全部条款,不另立变体。

**C-6**: 本契约不赋予 modify 任何清理职责(孤儿清理形态归实现阶段);modify 只补缺、不删孤儿。

**C-7**: 未被 modify 触及的存量团队行为与现状一致(席位继续按现行通用载体派发)——不静默批量改写。

**C-8**: 建议面:create-team 与 improve-team 的 modify 文档 MUST 各带一行「存量团队经一次 modify 即可让席位上注册面」的指引;该行的归属在本契约(`teaching-and-guards.md` 覆盖的是 create/agents 侧文件,不含此两处)。

**验收示例前提**(供 /speckit.implement 复测):「modify 前席位缺失 → modify 后实例在册且已上注册面」依赖——improve-team 回填步已落、渲染命令已实现。
