# Contract: focus_target 与 run 侧解析(run 面)

**Spec**: [requirements.md](../requirements.md) FR-011, FR-012(territory 部分), FR-014  
**Surface**: `scripts/python/goal-utils.py`(新函数)× `templates/commands/team.md`(Run Mode 第 2 步)× `skills/create-team/references/execution-guide.md`  
**Authority**: 五查 verdict 唯一权威仍是 `preview_target_check`;本契约只新增其**输入的解析层**

## C-1 解析函数(引擎扩展)

```
resolve_effective_target(team_md_path, explicit_target=None)
  → { "effective": "T-<nnn>" | None,
      "source": "explicit" | "team-default" | "none",
      "declared_focus": "T-<nnn>" | None }
```

- 解析顺序恒为 **显式 `--target` > team.md `focus_target` > 无**;显式值与 `focus_target` 相同不构成特殊情形(`source=explicit`)。
- `focus_target` 值域 `^T-\d{3}$`;格式非法 = 配置错误,报 `input-error` 停止(不静默忽略、不降级为无)。
- 本函数只解析、不判定;`effective`(非 None 时)MUST 喂给既有 `preview_target_check` 走完整五查——悬空/终态/跨 goal/goal 终态 verdict 与复核二分语义逐字沿用 038,零旁路。
- `source=none`(无显式且未声明字段)时下游全流程与引入前**逐字节等价**(038 SC-002 保持:无该字段的团队感知不到本需求)。

## C-2 披露与落痕

- 确认门禁 Target 披露行在 038 两式之上增加来源后缀,`source=team-default` 时追加 [[STR-001]](逐字 `(团队默认)`):

```text
本次 Target: T-003 — <statement>(open)(团队默认)
```

- 其余两式不变:`(open)`(显式)/`无(对 goal 整体运行)`(none)。
- run 报告 `**Target 指派**:` 行同样携带来源标记;新台账条目 `target_ref = effective`(局部形),仍仅由 Team Supervisor 写入 `items.jsonl`。
- 绑定不变量:`focus_target` 不改 Goal–Team 绑定、不参与 goal 身份解析(仍两级)、不改 summary 交付目录;`--target` 显式覆盖恒合法。

## C-3 默认聚焦的创建期校验与后续状态

- 创建落盘前:`focus_target` MUST 存在于绑定 goal 的 `## Targets` 且为 `open`,否则创建拒绝(错误信息指明"focus_target 引用的切片不存在/非 open")。
- 后续该 Target 转 `done`/`dropped`:run preview 五查按既有语义拦截(终态走复核二分);团队重聚焦经 improve-team(modify 改 `focus_target`),重开 Target 经 `/speckit.goal`——**无终态执行旁路**。

## C-4 无字段团队的等价钉

- 未声明 `focus_target` 的 team.md:run 流程不读取、不解析、披露行无第三式;契约测试钉"逐字节等价"(无该字段时 `resolve_effective_target` 不会被调用,或调用后行为与直通完全一致——实现取前者)。
- 存量团队零迁移:字段缺省即合法,`improve-team` 可后补(补值时按 C-3 校验)。

## 验证

- `tests/contract/test_focus_target_resolution.py`:显式覆盖默认 / 默认生效(含披露标记)/ 无字段直通 / 非法格式 exit-input-error / 终态默认走复核二分;`team.md` 无字段样本与 038 既有 run 契约测试共用夹具证明零回归。
- 模板子串断言:三式披露行、`**Target 指派**` 行、解析顺序句,入 `test_goal_team_creation.py` 的模板面。
