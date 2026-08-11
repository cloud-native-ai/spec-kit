# Contract: run-target-assignment(/speckit.team run 的 `--target` 参数)

**Surface**: `/speckit.team run <team-slug> [--target <T-nnn | goal-slug.T-nnn>]`(参数出现于 `$ARGUMENTS`;run 意图路由与 preview → confirm → execute 门禁结构不变)
**Implements**: FR-009, FR-010, FR-011, FR-012;SC-001, SC-002, SC-004
**Authority**: [[STR-004]] §Run assignment;终态复核二分见 Clarifications Session 2026-08-11(D8)。

## 1. 参数文法

- 局部形 `T-<nnn>` 为规范形;限定形 `<goal-slug>.T-<nnn>` 接受,其 `<goal-slug>` MUST 等于绑定 goal 身份,否则按跨 goal 引用拒绝(§2.4)。
- 未出现 `--target` → 目标整体运行:preview/confirm/execute/report 全流程与本需求引入前**逐字节等价**(报告结构、summary 状态行无新增必填项;SC-002)。
- 团队未绑定 goal **定义**(无 `goal_slug` 且无 `.specify/goal/<team-slug>/goal.md` 可推断定义)而指定了 `--target` → 报"Target 依赖 goal 定义",指向 `/speckit.goal migrate` 路径并停止;不指定时一切照旧(FR-010)。

## 2. Preview 校验(确认门禁之前)

按序执行,任一失败即停止且不产生执行痕迹(SC-004):

1. **解析绑定 goal**:沿用既有两级身份解析(`goal_slug` 显式 → 团队 slug 推断,036 §10.1)——本契约 MUST NOT 引入第三级。
2. **悬空引用**:`T-<nnn>` 不存在于绑定 goal 的 [[STR-001]] 节 → 报为悬空引用并停止,提议先经 `/speckit.goal targets --add` 添加;MUST NOT 静默接受、降级或臆测。
3. **终态引用**:目标状态为 `done`/`dropped` → 显式报出终态并停止,附复核指引(复核二分):
   - 终态属实 → 返回报告并结束本次 run,不执行;
   - 证据不符(仍有未完成工作项)→ 经 `/speckit.goal targets --set open --id <T-nnn>` 重开后重新发起 run。
   - run 模式 MUST NOT 提供终态执行旁路,MUST NOT 默默当作 open 执行。
4. **跨 goal 引用**:限定形前缀与绑定 goal 身份不一致 → 拒绝,指明绑定轴不可越界(FR-012)。
5. goal 自身终态(`achieved`/`abandoned`)→ 拒绝指派,指明终态 goal 只读。

## 3. 确认门禁披露(FR-011)

既有披露项(绑定 goal、身份类型 explicit/inferred、summary 决策、交付目录)之外,MUST 追加一行:

```text
本次 Target: T-002 — <statement>(open)
```

未指定时该行值为 `本次 Target: 无(对 goal 整体运行)`。

## 4. Run Report 记录

`runs/<UTC-timestamp>-report.md` 既有结构不变,MUST 追加指派行(字段名固定):

```text
**Target 指派**: T-002(<statement>)   # 或 "无(goal 整体)"
```

新产生的台账条目 MUST 携带 [[STR-003]](由团队主管写入;SC-001 的归属断言面)。

## 5. 不变式保持(SC-002 / FR-012)

- Goal–Team 绑定、身份解析结果、summary 交付目录位置、GI-1…GI-4 全部不因 `--target` 改变。
- 同一 Target 被多团队/多 run 先后推进合法;写域冲突仍由 territory 纪律管辖,`--target` 不是写域声明。

## 6. Contract Test Pins

- 三类非法引用(悬空/终态/跨 goal)各若干例:断言 preview 停止、无执行痕迹、无台账写入(SC-004,拦截率 100%)。
- 合法指派:断言门禁披露行与 report 指派行格式逐字匹配(SC-001)。
- 无 `--target` 回归:既有 run 契约测试全绿、断言不削弱(SC-002)。
