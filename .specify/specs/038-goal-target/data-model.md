# Data Model: 038-goal-target

实体清单:3 个(Target、`target_ref` 台账字段、run 指派运行时值)。概念事实源为 [[STR-004]](`shared/definitions/goal-definitions.md` → Target Decomposition);本文件只定义操作面数据结构。

## Entity 1: Target(goal 定义内的授权条目)

**持久化位置**: `.specify/goal/<goal-slug>/goal.md` 的 [[STR-001]] 节(引擎渲染,MUST NOT 手写)。节**整体缺省** = 该 goal 无 Target(可选装饰件,FR-002)。

### Fields

| 字段 | 类型 | 必填 | 约束 |
|------|------|------|------|
| `id` | string | 是 | 局部形 `T-<nnn>`,`<nnn>` 零填充三位;goal 命名空间内单调发放;终态身份 MUST NOT 复用(FR-005)。限定形 `<goal-slug>.T-<nnn>` 仅用于跨 goal 呈现/聚合 |
| `statement` | string | 是 | 成果形子成果语句;MUST 通过 GD-2/GD-3 同源检测(复用 `_reject_bad_objective`);MUST NOT 归一化等值于该 goal 任一成功判据(FR-004,D5);MUST NOT 为空 |
| `status` | enum | 是 | 恰为 [[STR-002]] 三态;新建必为 `open` |
| `history`(派生) | — | — | 每次授权与状态迁移追加 goal `## History` 一行(D6 记法);Target 自身不持有独立历史节 |

### 渲染文法(D3)

```markdown
## Targets

| ID | Target | Status |
|----|--------|--------|
| T-001 | 日志组件拆分完成 | open |
| T-002 | 指标采集链路独立可部署 | done |
```

- 行正则: `^\| (T-\d{3}) \| (.+) \| (open|done|dropped) \|$`
- 表头行固定;条目按 ID 升序(呈现序,**不承载执行语义**——FR-003 无序集)。
- 空表格(表头无行)非法:`validate` 报出,退出码 4;无 Target 的正确形态是节整体缺省。

### Lifecycle & State Transitions(FR-006)

```text
open ──(done)──▶ done      (approved completion, 经 /speckit.goal 人批准)
open ──(drop)─▶ dropped    (刻意放弃, 经 /speckit.goal 人批准)
done ──(reopen)─▶ open     (终态复核发现证据不符, clarify 2026-08-11 裁决路径)
dropped ─(reopen)─▶ open   (同上)
```

- 合法迁移集合: `{open→done, open→dropped, done→open, dropped→open}`;其余组合(含终态→终态)MUST 拒绝,退出码 2。
- 终态条目 MUST 保留在节内携带终态,MUST NOT 删除。
- goal 处于终态(`achieved`/`abandoned`)时:新增 Target 与任何状态迁移 MUST 拒绝(退出码 2),延续 037 生命周期语义。

### Validation Rules(validate_goal 扩展)

1. 身份文法: `T-\d{3}`;节内唯一;满足既有 DDL 字面量文法(首字符字母/数字,仅 `[A-Za-z0-9_.-]`)。
2. 状态枚举: 恰为三态之一。
3. 语句非空;手写结构破坏(行不匹配正则、表头缺失)→ 报"结构由引擎渲染,手写即违规"。
4. 序号连续性不作强约束(终态不复用导致跳号合法),但 MUST 单调——出现回退序号即违规。

## Entity 2: `target_ref`(台账可选字段)

**持久化位置**: `.specify/teams/<team-slug>/items.jsonl` 行内可选字段([[STR-003]])。

| 属性 | 约定 |
|------|------|
| 类型 | string,可选 |
| 取值 | **局部形** `T-<nnn>`——goal 由团队 `goal_slug` 绑定隐含(FR-013);限定形不合法 |
| 缺省语义 | 字段缺失 = 归属 goal 整体;存量行与无 Target 团队的行 MUST 语义不变 |
| 不变式 | IL-1…IL-5 全部保持;`target_ref` 不改变 append-only、末行定态、tracked provenance、身份文法、supersedes 折叠的任何语义 |
| 折叠规则 | 指向不存在身份 → 报为无效归属,按 goal 整体降级计入并声明(FR-014);MUST NOT 臆造 Target |
| 写入者 | 仅团队主管(FR-021 纪律不变);run 指派产生新条目时由主管写入本字段 |

## Entity 3: run 指派(运行时值,不持久化为独立实体)

一次 run 选定的 Target 引用。生命周期仅覆盖 preview → confirm → execute → report。

| 阶段 | 落痕 |
|------|------|
| preview | 校验:引用存在于绑定 goal 的 [[STR-001]] 节且为 `open`;悬空 → 报错停止(exit: 报为悬空引用并提议经 `/speckit.goal` 添加);终态 → 报出并停止(复核二分,D8);跨 goal → 拒绝(FR-012) |
| confirm | 确认门禁披露:绑定 goal + 本次 Target(`T-002: <语句>` 或"无")+ Target 状态(FR-011) |
| execute | 工作聚焦该 Target;不改绑定、不改身份解析、不改交付目录(FR-012) |
| report | run report 记录指派(含"无");新台账条目携带 [[STR-003]](FR-011/FR-013) |

## 派生结构:切片轴卷积(总结侧,非持久实体)

`build-summary-input.py` 折叠产出,写入表单 `targets:` 块(D4):

```yaml
targets:
  goal_slug: <slug>
  axis_note: 切片轴(范围覆盖度)——与判据轴分列,不推导 achieved
  items:
    - id: T-001
      statement: <语句>
      authored_status: open
      attributed_items: 3        # 携带 target_ref=T-001 的台账条目数
      completed_items: 2
      pending_approval: false    # authored 与证据不一致时为 true(FR-015)
  coverage: "2/3 done"           # 按 authored_status 计
  unattributed_to_target: 5      # 无 target_ref 的条目数(归属 goal 整体)
  invalid_refs: 1                # 指向不存在身份的降级行数(声明不静默)
```

- 里程碑吸收(FR-016, P3):`authored_status: done` 的 Target 追加为 `milestones` 行,`source: goal-target:<goal-slug>/goal.md#T-<nnn>`。
- 无 Target 的 goal:表单 MUST NOT 出现 `targets:` 块——既有行为逐字节等价(SC-002)。
