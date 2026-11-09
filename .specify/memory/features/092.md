# 092 — Goal/Team Parallel（目标/施工队 × spec 并行）

## Overview

085 把 goal/team 当作「临时」对象：定义住在 spec 目录里、生命周期挂在一次 spec 上、默认是 SDD 的下位物。
本特性重定义三个词并把绑定关系显式化：**临时与全局**指的是存档范围（`.specify/` 下的全局层 vs 某条线里的
局部层），不是 SDD 的下位关系；**goal** 是设计师画的目标，**team** 是施工队；两者与 spec 是**三向绑定**
（`goal_slug` / `team_slug` / `handoff_ref`），不是父子。目标是让 goal 线、team 线与 SDD 线三条线可以真正并行：
任何一条都不要求另一条先存在，复杂 spec 用一份交接契约（`handoff.md`）把目标转给施工队，施工队只能写自己的
territory 并逐任务回执。

## Key Changes

- `scripts/python/goal-utils.py`：绑定记录（`owner` / `owner_id` / `origin`）+ 引擎独写 + 字节级重写规则；
  存档范围闭集由 `global` / `spec` / `auto` 改为 `goal` / `teams` / `auto`（`spec` 出域）；新增 `binding` 读动作、
  `migrate-archive`、`probe-residual`、`handoff-decision`；可写性由函数 `writable(kind, binding, bound_teams)` 判定。
- 统一存档：`.specify/goal/<slug>/goal.md` 与 `.specify/teams/<slug>/team.md`；迁移为显式命令、幂等可恢复、
  **archive-not-delete**（源树移入 `.specify/archive/goal-team/trees/`，逐条回执落 `receipts/`）。
- 交接契约 `<spec-dir>/handoff.md`（八个必填节）+ 施工队回写 `<spec-dir>/writeback/<T-NNN>.yaml`（一任务一件）。
- 声明层两条事实：命令族闭集 `goal-team-command-family.yaml`、交接门槛 `goal-team-handoff-threshold.yaml`；
  `contract.yaml` 新增 `registered_facts:` 登记位（今日无此登记位 — R-11 实测）。
- owner 面重写：路由裁决层级段的「临时 = 下位」表述、驱动 SKILL 与 checkpoint 协议、状态脊柱键
  （`temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` → `goal_slug` / `team_slug` / `origin_spec_dir`，
  旧键保留只读别名）、`/speckit.goal` `/speckit.team` `/speckit.feedback` 模板、框架地图。

## Plan Notes

- **方案（planned 2026-11-09）**：`plan.md` + `research.md`（R-01…R-31 实测）+ `data-model.md`（13 实体 / 8 规则）+
  `contracts/`（5 页 111 条款：binding-and-lifecycle C-001…C-030 / unified-archive-and-migration C-031…C-052 /
  handoff-contract C-053…C-070 / command-family-and-declarations C-071…C-090 / owner-rewrites-and-tests C-091…C-111）+
  `quickstart.md`（9 走查 S-0…S-8）+ `feature-ref.md`（FR 42/42、SC 11/11 映射与 085 处置表）。
- **合规**：Constitution 22 项全 Pass；Complexity Tracking 无 violation，另有一条裁决记录（plan 阶段基线是
  46 条串行 `FAILED` 名单（第三次连跑仍为同一名单），红先模块由实现阶段按 C-109 落）。
- **承重裁决**：T-001 统一存档而非双存档；T-002 可写性由函数判定而非禁令清单；T-003 三维绑定；T-004 `spec` 出域；
  T-005 交接门槛 = 单条声明事实；T-006 交接创建时机由同一事实派生；T-007 迁移归 `/speckit.goal migrate-archive`。
- **阶段门读数**：`pre-analyze-check --stage plan` → pass / errors=0；`decomposition-check --mode plan` → proceed
  （fr=42）；`validate-decision-tensions` → 7 条记录 0 error。
- **执行模型（本特性自身的设计对象）**：plan 6 包、implement 约 10 任务/包且 ≤6 并发（worktree 写隔离 +
  integration queue）、review 4 段并行；比较面始终是串行 `FAILED` id 名单，不按并行模式的计数比较。
- **tasks（2026-11-09）**：`tasks.md` 80 行 / 7 包；`validate-tasks` 0 error + 1 条已披露前向边（`T043 → T054`，同包内、原因记录在 Package Map）。
- **checklist（2026-11-09）**：`checklists/` 40 项，100% 可追溯；两条门均以红先行证明（mutation probe → fail），8 行 fail 判为 requirements 缺陷、转为 analyze 输入。
- **analyze 第 1 轮（2026-11-09）**：报告条件通过——1 CRITICAL（C-01）+ 5 HIGH（H-01…H-05）阻断 implement；14 条发现全部落 `.specify/specs/092-goal-team-parallel/notes/analyze-round1-findings.md`，并给出 7 项有序 implement 前置。
- **analyze-repair（2026-11-09）**：C-01、H-01…H-05、M-01…M-05、L-01 全部闭；L-02 即本节（features 阶段记录刷新）；L-03 残余（见下）。修复账 `notes/analyze-round1-repair.md`。门读数：`validate-requirements` 0/0、`account-clause-coverage` FR 车道 42/42、`validate-tasks` 0 error / 1 disclosed warning、`pre-analyze-check` 三个阶段均 pass（fr=42）、`validate-decision-tensions` ok（7 记录 0 error）、`decomposition-check --mode tasks` proceed（fr=42 / tasks=80）。
- **残余**：L-03 —— `team/092-goal-team-parallel/team.md` 的 `name: SDD Temporary Team 092` 来自 create-team 的世代命名，C-107 的扫描面是 `shared/` `skills/` `scripts/` `templates/` `src/`，不含 `.specify/specs/**`，故不触发；但 085–091 七份同形命名与该概念的重定义并存，是否在实现阶段把世代名一并改写留待 analyze 第 2 轮判定。
- **待办**：analyze 第 2 轮 / implement / review 未跑。
