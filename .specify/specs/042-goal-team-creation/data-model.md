# Data Model: 042-goal-team-creation

实体均为仓内既有存储之上的**增量**;除 `focus_target` 字段与解析值外无新持久化实体,提议类实体是确认门禁处的**瞬态呈现物**(落痕于确认预览与创建产物,不另存文件)。

## 1. team.md `focus_target` 字段(唯一新持久化字段)

| 属性 | 值 |
|------|-----|
| 位置 | `.specify/teams/<team-slug>/team.md` frontmatter,插在 `goal_slug` 之后(字段序 `slug, name, description, goal, goal_slug, focus_target, territory, pattern, members, config, created, updated`) |
| 类型 | 可选 string;值域 = 局部形 Goal Target 身份 `^T-\d{3}$` |
| 语义 | 该团队**默认聚焦**的 Target:是 run 级 `--target` 的预填——未显式指定时 run 解析到它;显式 `--target` 恒覆盖;不是写域声明、不是 Goal–Team 绑定变更、不参与 goal 身份解析 |
| 校验时机 | ① 创建落盘前:值 MUST 存在于团队绑定 goal 的 `## Targets` 且为 `open`(否则创建拒绝);② 每次 run preview:经 `resolve_effective_target` → `preview_target_check` 五查(悬空/终态/跨 goal/goal 终态均按既有 verdict 拦截,终态走复核二分) |
| 写入者 | 仅 create(goal-based 分支)与 modify(improve-team 重聚焦);与台账字段 `target_ref`(逐条归属)、run 选项 `--target` 显式消歧,不复用任一名称 |
| 生命周期 | 随 team.md;对应 Target 转 `dropped` 后字段保留,run 侧由五查拦截并指引 modify 重聚焦或 `/speckit.goal` 重开 |

## 2. 有效 run Target(运行时解析值,不持久化为独立实体)

```
resolve_effective_target(team_md_path, explicit_target|None)
  → { "effective": "T-<nnn>" | None,
      "source":    "explicit" | "team-default" | "none",
      "declared_focus": "T-<nnn>" | None }
```

- 解析顺序:**显式 `--target` > `focus_target` > 无**;`source` 驱动披露标记(STR-001 "(团队默认)" 仅在 `team-default`)。
- `effective` 喂给既有 `preview_target_check`(五查不变);`source=none` 时全流程与引入前逐字节等价。
- 落痕:确认门禁披露行、run 报告 `**Target 指派**:` 行(来源标记随行)、新台账条目 `target_ref = effective`。

## 3. 分解提议集(瞬态,FR-006..009)

| 字段 | 说明 |
|------|------|
| `statements[]` | 候选 Target 语句,各为成果形(GD-2 切片尺度);无序集——携带顺序仅为其呈现顺序,身份序号在落盘时由引擎单调发放,不承载语义 |
| `rationale` (每条) | 起草理由(缺口分析、从属性依据) |
| `check_verdicts[]` (每条) | `targets --check` 干跑结果(exit 0 通过 / exit 2 拒绝原因);呈现给用户前 MUST 全部通过,或该条被移出/改写重检 |
| `baseline` | 复用基线:goal 既有 open Targets 清单(来自 `parse_goal().targets`);提议集 MUST NOT 语义重复基线条目 |

不落盘;批准后逐条成为正式 Target(身份由引擎发放,与提议顺序无关)。

## 4. goal-based 创建计划(瞬态确认载荷,FR-004/013)

确认门禁一次性呈现:`分支判定`(命中的 goal-slug 与定义摘要)、`分析结论`(四要素:维度/判据覆盖/既有 Target/可达成性)、`路径决策`(单团队 | 分解 N 队,用户裁决)、`提议集或复用声明`、`territory 划分提议`。落痕于会话与创建产物(team.md 内容),不持久化为独立文件。

## 5. territory 提议条目(verify-territory-disjoint.py 输入 JSON)

```json
{
  "goal_slug": "<slug>",
  "teams": [
    { "slug": "<team-slug>",
      "write":     ["path-or-glob", "..."],
      "read":      ["..."],
      "forbidden": ["..."],
      "non_path":  [{ "type": "<typed-entry>", "target": "<...>" }] }
  ]
}
```

- 值域与 team.md frontmatter `territory` 键一致(create-mode.md 既有 schema);`non_path` 条目只列仲裁、永不求交(沿既有语义)。
- 校验对象 = 提议团队 + 同 `goal_slug` 既有团队(从磁盘读);输出 = 两两 `overlap_verdict`(import 既有文法)。
- 判定:`no-overlap` 全覆盖 → exit 0;任何 `overlap`/`undecidable` → exit 2 并逐对列出,流程披露风险、移交 `/speckit.goal coordinate` 或人工改划后重跑。

## 6. Target 聚焦团队(派生视图,非新存储)

`goal_slug` + `focus_target` + `territory` 三键齐备的 team.md 在 goal-based 分支语境下的称谓;N 个此类团队共享同一 `goal_slug`,各聚焦一个 open Target,`write` 范围两两不相交。slug 派生缺省模式 `<goal-slug>-t<nnn>`(如 `log-split-t003`,小写、零填充三位),落盘前查重,用户可在确认门禁改名。

## 关系图(文字)

```
Goal(定义,authored) 1 ── N Target(T-nnn,engine-rendered)
   ▲ goal_slug(N teams : 1 Goal,静态)
   └── team.md × N:focus_target → 恰一个 open Target(创建时校验,run 时五查)
run(时点):explicit --target > focus_target > none → preview_target_check → 报告/台账 target_ref
创建期(瞬态):分解提议集 --check→ 合并确认 → 逐条 --add;territory 提议 JSON → verify 脚本 → 落盘/移交 coordinate
```
