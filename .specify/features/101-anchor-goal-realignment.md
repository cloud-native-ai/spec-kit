# Feature Detail: Anchor / Goal Realignment

**Feature ID**: 101
**Name**: Anchor / Goal Realignment
**Description**: 语义反转 + 命令面清理（Plan B）：Anchor 成为项目级远期目标（`.specify/anchoring/<slug>/anchor.md`，`/speckit.anchor` 接管旧 `/speckit.goal` 的七模式），Goal 降为行动级实际指导（`.specify/goals/<slug>/goal.md`，`/speckit.goal` 四模式 `create` / `view` / `modify` / `status`）；团队绑定字段 `goal_slug` → `anchor_slug`；`.specify/anchoring` 逐条分类、迁移、归档（archive-not-delete，逐条回执）；日期化记录不改写。
**Status**: Planned
**Created**: 2026-11-12
**Last Updated**: 2026-11-12（`/speckit.implement` WP-01…WP-06 收尾：语义反转、七/四模式命令面、双存储引擎、`.specify/anchoring` 14 条分类清理（9 保留 / 3 迁移 / 2 归档，逐条回执）、16 个团队绑定改名 + 6×R3 + 1×R2 处置、G-1…G-10 守卫、收尾全量与 `verification.md` 读数落盘。状态停在 `Planned`：`Planned → Implemented` 的第①条「tasks 零开放行」不在本包的写域内，由阶段集成器的 task-sigil sweep 随后关闭；闭包判定与状态翻转归 review 阶段。此前 `/speckit.plan`：`plan.md` + `research.md` + `classification.json` + `data-model.md` + `contracts/`（4 页 49 条款）+ `quickstart.md` + `feature-ref.md` 落地；Draft → Planned。此前 `/speckit.clarify`：Feature 绑定裁定为新 Feature 101；71 FR / 10 SC 保持；决策 D-1…D-5 见 requirements `## Clarifications`，证据 `test-evidence/clarify-2026-11-12.md`）

## Overview

当前活语义与用户裁定相反：`shared/definitions/goal-definitions.md` 把 **Goal** 定义为项目级、`outcome, not steps` 的一等概念，`.specify/anchoring/` 是它的档案，`/speckit.goal` 是唯一撰写入口并承载七模式；`sdd-routing-definitions.md` 因此把 Goal 画成控制层级最高层。094 只把目录 `.specify/goal/` 改名为 `.specify/anchoring/`，文件名 `goal.md`、字段 `goal_slug` 与命令面都未改名。

本特性执行 Plan B 语义反转：**Anchor** 成为项目级、长周期、跨交付物持续追求的远期目标；**Goal** 降为行动级、短周期、可执行的实际指导。命令面对调——`/speckit.anchor`（canonical `templates/commands/anchor.md`）接管七模式并成为锚点档案唯一撰写入口，`/speckit.goal` 收敛为四模式。存储面分离——锚点定义文件 `goal.md` → `anchor.md`（STR-001），行动级 Goal 落到 `.specify/goals/<slug>/goal.md`（STR-002），团队绑定 `goal_slug` → `anchor_slug`（STR-003）。最后对 `.specify/anchoring/` 现存 14 个条目逐条分类并清理：保留真锚点、迁移行动级条目、归档过期条目（archive-not-delete，逐条回执，可重跑、可中断续做）。

**已交付（2026-11-12，implement）**：上述五项全部落地并读取数——语义反转写在两份 owner 中，命令面对调并由契约测试钉住，存储层分离且引擎为唯一定义写者，14 条分类清理与 20 个团队的绑定/处置完成（活面旧语义残留 C1–C7 全 0）。收尾全量套件按失败 id 名与实现入口基线比较 **未通过**：228 failed / 8936 passed / 3 skipped 对基线 192 / 8900 / 3，按 id 名计 37 个新增失败（29 陈旧断言 / 6 活面缺口 / 2 工作树残留），GATE-1 判 FAIL；该集合全部落在 WP-06 写域之外，本包未编辑测试或源码（逐条归因见 `verification.md` § GATE-1）。逐条证据见 `test-evidence/` 与 `verification.md`。

## Latest Review

- **2026-11-12 `/speckit.clarify`（Mode A，`requirements.md`）**：Feature Linkage 由 `Need clarification` 收敛为 **Feature 101**（不绑定 041 的扩展；041 保持 `Implemented` 与日期化记录，只加反向交叉引用）。五项决策落地：D-1 Feature 绑定；D-2 `goal_slug` 退役拆为"结构性改名 + 术语归一化"两步，逐字节断言只作用于结构性步骤，日期化 `runs/**` 保持原字节；D-3 Goal `status` = 生命周期报告/转换（终态保留，`reopen` 仅限 `owner: human`）；D-4 清理/迁移为 `goal-utils.py` 内独立动作组（`--check` / `--apply`），回执逐条 JSON 落在动作目标内，概念摘要为声明映射后归一化投影的 `sha256`，幂等判据"目标存在且回执存在"；D-5 悬空绑定处置顺序 R1–R3（`viz-skill-arena` → R2 落成 Anchor，`demo-seat-dispatch` → R3 归档团队），受保护日期化路径增加 `.specify/teams/**/runs/**` 与全部日期化 spec 目录，基线 `d7c9da7a3`。就地纠正：SC-002 三个→四个 Anchor-only 模式；FR-052 路由收敛为锚点侧 `/speckit.anchor`、团队侧 `/speckit.team`；FR-002/FR-004 共享 schema 唯一 owner 归 `anchor-definitions.md`；FR-033 补入 `handoff-ref`；A-5 决策者收敛为 plan。FR/SC 结构保持 71 / 10，`validate-requirements.py` 0 error / 0 warning。下一阶段 `/speckit.plan`。

## Key Changes (delivered)

1. **概念归属**：`shared/definitions/anchor-definitions.md` 为 Anchor 唯一 owner（兼共享绑定记录、生命周期表与 archive-layer / `--scope` 取值集 owner）；`shared/definitions/goal-definitions.md` 重写为行动级 Goal owner 并按路径引用共享 schema。
2. **命令面**：`templates/commands/anchor.md` 与 `skills/internal/manage-anchor/` 承载七模式；`templates/commands/goal.md` 与 `skills/internal/manage-goal/` 收敛为四模式，Anchor-only 四模式（`targets` / `migrate` / `migrate-archive` / `coordinate`）具名拒绝（`anchor-only-mode`，指向 `/speckit.anchor`）；四套 per-tool 副本由生成器产出。
3. **存储与引擎**：`goal-utils.py` 是唯一引擎/定义写者；按层解析 `anchor.md` / `goal.md` / `team.md`；`--scope` 四成员 `anchor` / `teams` / `goals` / `auto`；行动级 Goal 动作组与清理/迁移动作组落地。
4. **清理与迁移**：14 条逐条分类（9 保留 / 3 迁移 / 2 归档，规则 id + 证据），行动级迁入 `.specify/goals/`，过期归档到 `.specify/archive/anchoring/`，回执逐条且摘要前后相等；16 个团队绑定改名为 `anchor_slug`，两处悬空修复（`viz-skill-arena` R2 → `visualization-skill-selection`，`demo-seat-dispatch` R3），6×R3 + 1×R2 处置记录齐全。
5. **活面收敛**：framework-map、glossary、routing 层级、re-anchoring 引用、flow-class 台账、probe 登记、setup/house-keeping、命令参考与教程、团队域参考同步；G-1…G-10 契约/集成守卫使缺失 `/speckit.anchor` 或残留旧语义转红（活面残留 C1–C7 全 0）。

## Implementation Notes

- **六包硬顺序**：WP-01（owner + 引擎）→ WP-02（命令面）→ WP-03（活面收敛）→ WP-04（清理/迁移/处置）→ WP-05（守卫与读数）→ WP-06（注册与收尾，本包）。每个包的提交只动其文件级写域；源与镜像同包落地。
- **单写者不变量**：两层定义文件的定义写者只有 `goal-utils.py`；派生 `summary/**` 由既有总结流写入，明确列在定义写者之外（G-4 静态审计 + 两写者模拟）。
- **archive-not-delete**：迁移/归档逐条 JSON 回执，幂等判据为「目标存在 + 回执存在 + 摘要相等」；第二次 apply 记录 0 非 no-op 决策、185 文件哈希前后一致；I5 半状态 exit 4 `half-state`。受保护日期化路径以 `d7c9da7a3` 为基线逐文件 `git hash-object` 比较（G-8）。
- **WP-05b 两处活面纠正**：`shared/definitions/derivation-definitions.md` 的 `Goal` 行改为 `Anchor`，`.specify/memory/tools/build-summary-input.py.md` 的默认 `--out` 对齐 `.specify/anchoring/<slug>/summary/`；镜像仅经 `sync-mirrors.py --write` 刷新。
- **披露的残余**：12 个活 `team.md` 的 `forbidden_paths` 仍列 `.specify/goal/**`——记录为分类后的陈旧地址（禁止字段），未编辑；SC-008 文档站构建腿 = `not-evaluated`（EP-006：Hugo v0.141.0 对 `.Site.Language.Locale` exit 1，特性前既有）；T004 的 `coverage-baseline.txt` 在 setup 阶段未落盘，收尾的条款覆盖仅能给出同刻读数，不能声称实现前后无退化（详见 `verification.md`）。

## Status Tracking

- **Draft**: Feature row first added to `.specify/features.md`.
- **Planned**: `plan.md`（及设计制品）存在；Constitution Check 无未声明的 Fail 行。*(2026-11-12 起)*
- **Implemented**: `tasks.md` 零 `[ ]` / `[>` 行 **且** `verification.md` 为每条 SC 记录状态（六值词表），**且** 每条 `final` 路径判据 `pass`，**且** 冒烟记录三元组 `pass`（命令、exit 0、非空证据路径）。
- **Blocked**: tasks 关闭但存在 `final` 路径判据非 `pass`。
- **Ready for Review**: 延后任务全部解除或豁免、review 证据产生、当前代码段记录无 `blocking` 条目、且无 `final` 判据停在 `blocked` / `deferred` / `fail`（除非用户显式豁免）。
- **Sealed**: review 结论完成、验收记录齐备、合并回写完成。**Completed** 仅为遗留记录值，新工作不得落入。

**当前读数（2026-11-12，WP-06 交回时）**：第②③④条由 `verification.md` 与收尾读数支撑；第①条不满足——`tasks.md` 的 81 行在本包写域之外，由阶段集成器随后做 sigil sweep。**收尾全量套件 GATE-1 判 FAIL**：37 个新增失败 id 超出实现入口基线（归因见 `verification.md` § GATE-1），修复归属需由驱动方裁定；`closure-acceptance-check.py` 对当前记录报 `accept`（final 6/6 pass，claimed `Planned`）。因此状态停在 `Planned`，`Planned → Implemented` 的闭包判定与翻转归 review 阶段，本包不自行改写状态。

## Related Specifications/Requirements

- `.specify/specs/101-anchor-goal-realignment/requirements.md` — 本特性需求（71 FR / 10 SC）。
- **041 Goal Registry**（`.specify/features/041-goal-registry.md`）：本特性是其概念与命令面的语义反转，作为独立 Feature 登记，不是 041 的增量扩展。
- **094 Goal-Team Parallel**：`.specify/anchoring/` 的目录改名来源；本特性完成其未落地的命令面与文件名改名。
- **090 Re-Anchoring**：保留其运行内纪律；本特性只做术语消歧（Anchor / anchoring archive / Re-Anchoring）。

## Plan Notes

- **方案（planned 2026-11-12）**：`plan.md` + `research.md`（R-01…R-16 实测基线）+ `classification.json`（14 条目 + 7 团队处置，schema `101-classification/v1`）+ `data-model.md`（11 实体 E-1…E-11）+ `contracts/`（4 页 49 条款：anchor-command C-1…C-12 / goal-command C-13…C-22 / goal-engine C-23…C-35 / migration-cleanup C-36…C-49）+ `quickstart.md`（9 走查 S-0…S-8，逐条标注 `[today]` / `[premise]` / `[pin]`）+ `feature-ref.md`（FR 71/71 与 SC 10/10 映射 + 16 条裁决）。
- **合规**：Constitution 23 项全 Pass；Complexity Tracking 无 violation；`validate-decision-tensions.py` ok（4 records / 0 error）；Execution Premises EP-001…EP-005 verified、EP-006 falsified（Hugo 文档站构建预存失败，Decision `fallback`，SC-008 构建腿报 `not-evaluated`）；Inherited Blockers 声明六依赖、抽出 5 条记录（2 resolved / 3 not-applicable）。
- **分类基线**：14 条 = 9 anchor / 3 action-goal / 2 obsolete（与 A-5 暂定清单零偏差）；团队 20 个定义、16 个带绑定；处置 6 条 R3（全部 apply，含 091 的绑定移除与回执）+ 1 条 R2（`viz-skill-arena` → 新建 `visualization-skill-selection`），无 R1。
- **清理纪律**：迁移/归档幂等判据「目标存在且回执存在且摘要相等」；中断续做 I1–I5（I5 = exit 4）；冲突 exit 4 点名两候选；archive-not-delete；每个动作目标内一条回执。
- **承重裁决**：T-001 单引擎加层参数而非第二引擎；T-002 命令面拆分而非单命令加 `--layer`；T-003 归档而非删除；T-004 退役取值与退役模式不设别名。
- **requirements 订正**：4 条 `PLAN-EDIT:`（FR-011 / FR-028 / SC-006 把单写者不变量限定到定义文件，`summary/**` 是派生例外；FR-061 / SC-009 把 `.specify/archive/**` 等值断言限定为基线时已存在条目，新增 `.specify/archive/anchoring/**` 不计入）；`validate-requirements.py` 复核 0 error / 0 warning。

## Notes

- **不推送远端**：本线无人值守，推送需显式授权。
- **不重写日期化记录**：037 / 038 / 042 / 074 / 085 / 094、全部日期化 spec、`.specify/teams/**/runs/**`、`.specify/archive/**`、`.specify/history/**`、`docs/notes/**` 保持原字节。
- **不新建第二套引擎或多份 schema**：094 FR-001 与 041 的单一撰写入口不变量保留。
