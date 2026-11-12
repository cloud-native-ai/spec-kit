# Feature Detail: Anchor / Goal Realignment

**Feature ID**: 101
**Name**: Anchor / Goal Realignment
**Description**: 语义反转 + 命令面清理（Plan B）：Anchor 成为项目级远期目标（`.specify/anchoring/<slug>/anchor.md`，`/speckit.anchor` 接管旧 `/speckit.goal` 的七模式），Goal 降为行动级实际指导（`.specify/goals/<slug>/goal.md`，`/speckit.goal` 四模式 `create` / `view` / `modify` / `status`）；团队绑定字段 `goal_slug` → `anchor_slug`；`.specify/anchoring` 逐条分类、迁移、归档（archive-not-delete，逐条回执）；日期化记录不改写。
**Status**: Planned
**Created**: 2026-11-12
**Last Updated**: 2026-11-12（`/speckit.plan`：`plan.md` + `research.md` + `classification.json` + `data-model.md` + `contracts/`（4 页 49 条款）+ `quickstart.md` + `feature-ref.md` 落地；状态 Draft → Planned。此前 `/speckit.clarify` 登记：Feature 绑定裁定为新 Feature 101；71 FR / 10 SC 结构保持，`validate-requirements.py` 0 error；决策 D-1…D-5 见 requirements `## Clarifications`，证据 `.specify/specs/101-anchor-goal-realignment/test-evidence/clarify-2026-11-12.md`）

## Overview

当前活语义与用户裁定相反：`shared/definitions/goal-definitions.md` 把 **Goal** 定义为项目级、`outcome, not steps` 的一等概念，`.specify/anchoring/` 是它的档案，`/speckit.goal` 是唯一撰写入口并承载七模式；`sdd-routing-definitions.md` 因此把 Goal 画成控制层级最高层。094 只把目录 `.specify/goal/` 改名为 `.specify/anchoring/`，文件名 `goal.md`、字段 `goal_slug` 与命令面都未改名。

本特性执行 Plan B 语义反转：**Anchor** 成为项目级、长周期、跨交付物持续追求的远期目标；**Goal** 降为行动级、短周期、可执行的实际指导。命令面对调——`/speckit.anchor`（canonical `templates/commands/anchor.md`）接管七模式并成为锚点档案唯一撰写入口，`/speckit.goal` 收敛为四模式。存储面分离——锚点定义文件 `goal.md` → `anchor.md`（STR-001），行动级 Goal 落到 `.specify/goals/<slug>/goal.md`（STR-002），团队绑定 `goal_slug` → `anchor_slug`（STR-003）。最后对 `.specify/anchoring/` 现存 14 个条目逐条分类并清理：保留真锚点、迁移行动级条目、归档过期条目（archive-not-delete，逐条回执，可重跑、可中断续做）。

## Latest Review

- **2026-11-12 `/speckit.clarify`（Mode A，`requirements.md`）**：Feature Linkage 由 `Need clarification` 收敛为 **Feature 101**（不绑定 041 的扩展；041 保持 `Implemented` 与日期化记录，只加反向交叉引用）。五项决策落地：D-1 Feature 绑定；D-2 `goal_slug` 退役拆为"结构性改名 + 术语归一化"两步，逐字节断言只作用于结构性步骤，日期化 `runs/**` 保持原字节；D-3 Goal `status` = 生命周期报告/转换（终态保留，`reopen` 仅限 `owner: human`）；D-4 清理/迁移为 `goal-utils.py` 内独立动作组（`--check` / `--apply`），回执逐条 JSON 落在动作目标内，概念摘要为声明映射后归一化投影的 `sha256`，幂等判据"目标存在且回执存在"；D-5 悬空绑定处置顺序 R1–R3（`viz-skill-arena` → R2 落成 Anchor，`demo-seat-dispatch` → R3 归档团队），受保护日期化路径增加 `.specify/teams/**/runs/**` 与全部日期化 spec 目录，基线 `d7c9da7a3`。就地纠正：SC-002 三个→四个 Anchor-only 模式；FR-052 路由收敛为锚点侧 `/speckit.anchor`、团队侧 `/speckit.team`；FR-002/FR-004 共享 schema 唯一 owner 归 `anchor-definitions.md`；FR-033 补入 `handoff-ref`；A-5 决策者收敛为 plan。FR/SC 结构保持 71 / 10，`validate-requirements.py` 0 error / 0 warning。下一阶段 `/speckit.plan`。

## Key Changes (planned)

1. **概念归属**：新增 `shared/definitions/anchor-definitions.md`（Anchor 唯一 owner，兼共享绑定记录、生命周期表与 archive-layer/`--scope` 取值集 owner）；`shared/definitions/goal-definitions.md` 重写为行动级 Goal owner 并按路径引用共享 schema。
2. **命令面**：新增 `templates/commands/anchor.md` 与 `skills/internal/manage-anchor/`（七模式）；重写 `templates/commands/goal.md` 与 `skills/internal/manage-goal/`（四模式，Anchor-only 模式具名拒绝并指向 `/speckit.anchor`）。
3. **存储与引擎**：`goal-utils.py` 保持唯一引擎/写者；按层解析 `anchor.md` / `goal.md` / `team.md`；`--scope` 四成员 `anchor` / `teams` / `goals` / `auto`；新增行动级 Goal 动作组与清理/迁移动作组。
4. **清理与迁移**：14 条逐条分类（规则 id + 证据），行动级迁入 `.specify/goals/`，过期归档到 `.specify/archive/anchoring/`，回执逐条；团队绑定改名为 `anchor_slug` 并修复两处悬空。
5. **活面收敛**：framework-map、glossary、routing 层级、re-anchoring 引用、flow-class 台账、probe 登记、setup/house-keeping、命令参考与教程、团队域参考同步；契约测试使缺失 `/speckit.anchor` 或残留旧语义转红。

## Related Specifications/Requirements

- `.specify/specs/101-anchor-goal-realignment/requirements.md` — 本特性需求（71 FR / 10 SC）。
- **041 Goal Registry**（`.specify/features/041-goal-registry.md`）：本特性是其概念与命令面的语义反转，作为独立 Feature 登记，不是 041 的增量扩展。
- **094 Goal-Team Parallel**：`.specify/anchoring/` 的目录改名来源；本特性完成其未落地的命令面与文件名改名。
- **090 Re-Anchoring**：保留其运行内纪律；本特性只做术语消歧（Anchor / anchoring archive / Re-Anchoring）。

## Plan Notes

- **方案（planned 2026-11-12）**：`plan.md` + `research.md`（R-01…R-16 实测基线）+ `classification.json`（14 条目 + 7 团队处置，schema `101-classification/v1`）+ `data-model.md`（11 实体 E-1…E-11）+ `contracts/`（4 页 49 条款：anchor-command C-1…C-12 / goal-command C-13…C-22 / goal-engine C-23…C-35 / migration-cleanup C-36…C-49）+ `quickstart.md`（9 走查 S-0…S-8，逐条标注 `[today]` / `[premise]` / `[pin]`）+ `feature-ref.md`（FR 71/71 与 SC 10/10 映射 + 16 条裁决）。
- **合规**：Constitution 23 项全 Pass；Complexity Tracking 无 violation；`validate-decision-tensions.py` ok（4 records / 0 error）；Execution Premises EP-001…EP-005 verified、EP-006 falsified（Hugo 文档站构建预存失败，Decision `fallback`，SC-008 构建腿报 `not-evaluated`）；Inherited Blockers 声明六依赖、抽出 5 条记录（2 resolved / 3 not-applicable）。
- **分类基线**：14 条 = 9 anchor / 2 action-goal / 2 obsolete（与 A-5 暂定清单零偏差）；团队 20 个定义、16 个带绑定；处置 6 条 R3（其中 1 条 already-satisfied）+ 1 条 R2（`viz-skill-arena` → 新建 `visualization-skill-selection`），无 R1。
- **清理纪律**：迁移/归档幂等判据「目标存在且回执存在且摘要相等」；中断续做 I1–I5（I5 = exit 4）；冲突 exit 4 点名两候选；archive-not-delete；每个动作目标内一条回执。
- **承重裁决**：T-001 单引擎加层参数而非第二引擎；T-002 命令面拆分而非单命令加 `--layer`；T-003 归档而非删除；T-004 退役取值与退役模式不设别名。
- **requirements 订正**：4 条 `PLAN-EDIT:`（FR-011 / FR-028 / SC-006 把单写者不变量限定到定义文件，`summary/**` 是派生例外；FR-061 / SC-009 把 `.specify/archive/**` 等值断言限定为基线时已存在条目，新增 `.specify/archive/anchoring/**` 不计入）；`validate-requirements.py` 复核 0 error / 0 warning。

## Notes

- **不推送远端**：本线无人值守，推送需显式授权。
- **不重写日期化记录**：037 / 038 / 042 / 074 / 085 / 094、全部日期化 spec、`.specify/teams/**/runs/**`、`.specify/archive/**`、`.specify/history/**`、`docs/notes/**` 保持原字节。
- **不新建第二套引擎或多份 schema**：094 FR-001 与 041 的单一撰写入口不变量保留。
