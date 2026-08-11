# Contract: targets-engine(goal-utils.py `targets` 动作组)

**Surface**: `python3 scripts/python/goal-utils.py targets <slug> [flags]`
**Implements**: FR-003, FR-004, FR-005, FR-006, FR-007(引擎面);SC-003
**Authority**: 概念语义以 [[STR-004]] 为准;本契约只规范 CLI、渲染与退出码。

## 1. CLI Grammar

```text
targets <slug> --add "<statement>"
targets <slug> --list
targets <slug> --set <open|done|dropped> --id <T-nnn>
```

- 三个标志互斥;同时给出或全部缺省 → 退出码 2(input error)。
- `<slug>` 解析为 `.specify/goal/<slug>/goal.md`(沿用既有 `definition_path` 语义);不存在 → 退出码 3(not found)。
- `--add`:追加一条 `open` 态 Target,身份为下一个未用的 `T-<nnn>`(三位零填充、单调、终态不复用)。
- `--set` 必须与 `--id` 成对;缺一 → 退出码 2。
- `--list`:输出该 goal 全部 Target(含终态),机器可解析:每行 `T-<nnn>\t<status>\t<statement>`;无 Target → 输出空(stdout 无行)且退出码 0。

## 2. Validation(add / set 前置)

| 检查 | 失败退出码 | 拒绝信息要求 |
|------|-----------|-------------|
| goal 处于终态(`achieved`/`abandoned`) | 2 | 指明"终态 goal 只读" |
| statement 为空 | 2 | — |
| GD-2 违规(任务清单/步骤形,复用 `_reject_bad_objective` 同源检测) | 2 | 指明改写为子成果方向(SC-003) |
| GD-3 违规(复合,同复用) | 2 | 指明拆分为独立 goal 的判据 |
| statement 归一化等值于任一成功判据(D5) | 2 | 指明判据权威互斥,改写为范围切片 |
| `--id` 不存在 | 3 | — |
| 状态迁移不在 `{open→done, open→dropped, done→open, dropped→open}` | 2 | 指明合法迁移集 |
| `--set` 目标态等于当前态 | 0(no-op,记 history 与否见 §4) | — |

退出码语义沿用既有四值:`0 ok | 2 input error | 3 not found | 4 validation failed`(本动作组不产生 4;4 属 `validate` 动作)。

## 3. Rendering([[STR-001]] 节)

- 首次 `--add` 创建节;节形态与 data-model.md §Entity 1 渲染文法逐字一致(表头固定、行正则、ID 升序)。
- 节 MUST 由本引擎渲染;`goal.md` 其余部分逐字节保留(不得重排 objective/criteria/history 的既有内容)。
- 无 Target 的 goal:节整体缺省——`create`/`modify`/`status`/`criteria`/`migrate` 既有输出 MUST 逐字节不变(SC-002 的引擎侧)。

## 4. History

每次成功的 `--add` 与状态迁移追加 goal `## History` 一行(D6 记法):

```text
- 2026-08-11 target T-001 added: <statement>
- 2026-08-11 target T-001 open→done
```

no-op `--set`(目标态等于当前态)不写 history。

## 5. Parsing / validate_goal 扩展

- `parse_goal` 返回新增 `targets` 键(list of `{id, statement, status}`);节缺省 → 空 list。
- `validate_goal` 新增:data-model.md §Entity 1 Validation Rules 全四条;违规计入 problems,退出码 4(既有 validate 语义)。

## 6. Contract Test Pins

- GD-2/GD-3 样例集:复用 037 objective 拒绝样例改写为切片尺度,断言拒绝率 100% 与退出码 2(SC-003)。
- 身份单调与终态不复用:连续 add/drop/add 序列断言编号严格递增且不复用。
- 迁移矩阵:9 组(3×3)状态对逐一断言合法/拒绝。
- 渲染往返:`--add` → `parse_goal` → 再渲染,字节稳定。
