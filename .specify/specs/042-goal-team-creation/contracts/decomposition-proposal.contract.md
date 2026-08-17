# Contract: goal→Target 分解提议与成组批准(提议面)

**Spec**: [requirements.md](../requirements.md) FR-006..009, FR-015(部分)  
**Surface**: `templates/commands/team.md`(分支内分解步骤)× `skills/create-team/references/{goal.md, create-mode.md}` × `scripts/python/goal-utils.py`(扩展动作)  
**Authority**: 形态检测文法 = `goal-utils.py` 与 `targets --add` 同源(`_bad_shape`/`_reject_bad_target_statement`/判据归一化比对);零第二套文法

## C-1 干跑校验动作(引擎扩展,本需求唯一新增写侧相邻面)

```
python3 scripts/python/goal-utils.py targets <goal-slug> --check "<候选语句>" [--json]
```

- **零写入**:不发放身份、不改 `goal.md`、不记 `## History`;输出仅 verdict 与拒绝原因。
- 校验器与 `--add` **同源**:GD-2(成果形,拒绝步骤序列)、GD-3(拒绝捆绑独立端态,提示改写或另立 goal)、判据复述拒绝(与该 goal criteria 归一化比对;同判 SC-xxx 语义由起草侧规避,引擎不读需求规格)。
- 退出码沿用全局语义:`0` 通过 / `2` 语句被拒(附原因)/ `3` goal 不存在 / `4` goal 处于终态(与 `--add` 的可变性断言一致——终态 goal 上提议无从落盘)。
- `--check` 与 `--add`/`--list`/`--set` 互斥(与既有"三选一"约束同构,违者 exit 2)。

## C-2 提议集起草纪律

- 分解路径产出**分解提议集**,以 [[STR-002]](逐字 `分解提议`)小节一次性呈现全量:每条语句 + 单独理由 + `--check` verdict。
- 呈现给用户前,提议集内每条 MUST 已通过 `--check`(exit 0);被拒条目 MUST 改写重检或移出,MUST NOT 以 exit-2 状态进入确认门禁。
- 集合为**无序集**:呈现顺序不承载执行顺序语义,落盘身份由引擎单调发放;MUST NOT 附依赖边/编号顺序/阶段化措辞。
- 独立成立的候选(自身即有意义的端态)MUST 被引导**另立 goal**(GD-3 litmus),退出提议集并在预览中说明。

## C-3 成组批准(一次合并确认 → 逐条落盘)

- 批准 MUST 为单次用户确认覆盖整组提议;随后**逐条**执行 `targets <slug> --add "<语句>"`。
- 每条 verdict 即时尊重:`exit 0` 记入 `## History`(引擎);`exit 2` 原样上报 verdict 与原因 → 修订后**重走 C-1 再提交**,或该条被显式放弃;MUST NOT 绕过引擎、MUST NOT 手写/手改 `## Targets` 节。
- **中途中止**:用户中止或某条落盘失败时,已落盘条目保留(它们是合法授权),其余丢弃;再次发起走 C-4 复用基线,零重复授权。

## C-4 复用基线(既有 Target 的处置)

- `parse_goal().targets` 为基线:`open` 条目直接复用(成组建队对象),MUST NOT 重复授权语义重复语句;`done`/`dropped` 条目保留展示、MUST NOT 复用身份、MUST NOT 顺带重开(重开仅 `/speckit.goal targets --set open`,由人发起)。
- 提议只能是**补缺口**或**确认复用**;提议集为空(无缺口)时直接进入成组建队,不强制新增。

## C-5 写入面红线

- team 侧流程对 `goal.md` **零写入**——包括 `## Targets`、`## History`、criteria、status;一切 Target 变更可溯源到 `goal-utils.py` 调用(SC-003)。
- 单一撰写入口不变:分支内落盘动作即 `/speckit.goal` 的引擎面调用(经用户批准),不构成第二撰写入口。

## 验证

- `tests/contract/test_targets_check.py`:进程内 `main()` 断言——合法语句 exit 0 且 goal.md 逐字节不变;步骤形 exit 2;判据复述 exit 2;终态 goal exit 4;`--check --add` 同给 exit 2;不存在 slug exit 3。
- `test_goal_team_creation.py` 补:模板含 [[STR-002]] 小节与"逐条 --add"措辞;`goal.md` 写入面断言(提议阶段 mtime/内容不变)。
