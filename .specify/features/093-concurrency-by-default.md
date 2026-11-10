# 093 — Concurrency by Default（subagent 并发作为框架基本属性）

## Overview

框架里已有大量并发能力（064 的写线/worktree 与 integration queue、070 的 Work Package 与 `wp-gate.py`、092 的 goal/team 平行模型），但它们是**少数执行体的特权**而非基本属性：`/speckit.implement` 在 091 实测为 62 任务 / 单代理 / 116 分钟并触达 500 回合上限，`requirements` / `tasks` 之外的阶段不自带拆解规则，而**声明与执行脱节**——092 的 plan 声明「6 包并行」，执行它的协调者却没有派发工具，6 包被串行完成且无人察觉。

本特性把既有并发机制从「可选层」提升为「所有执行体的默认形态」：范围是封闭集、由文件系统枚举派生；默认值是并发，串行必须携带取自封闭词表的理由码与可判定依据；一个声明了 N 个单元的执行体必须真的能并发派发，「声明并行、实际串行」是一种必须判红的缺陷而不是可接受的降级。它不新增 `/speckit.*` 命令、不引入第二个派发引擎或 registry、不改 SDD 阶段链与哨兵。

## Latest Review（2026-11-09/10，review + review-repair）

- **Verdict**: pass-with-mandatory-repairs — segments A (process) and B (artifacts) **pass** with PF-1…PF-5 / AF-1…AF-9 (AF-1 and AF-3 are P1 truthfulness-of-record items); segments C (implementation) and D (code) **pass with repairs** (C-1/C-2 important, C-3 nitpick; D-B1 blocking, D-I1/I2/I3 important); ARC (acceptance reality check) **ACCEPT sustained**.
- **ARC reading**: `closure-acceptance-check.py` re-run → `verdict: block`, `final_path pass=5 blocked=1 total=6`, sole reason `final-path-not-pass: SC-006`, `claimed_status: Planned` at review time (the `Blocked` landing was owed at close-out and is now recorded on the registry row). The SC-002 (`pass`), SC-006 (`blocked` / `not_evaluated`) and SC-011 (`pass`) evidence chains each recomputed and held.
- **Review-repair forks**: two parallel forks on disjoint territories — R1 (code/docs/guards: `docs/`, `scripts/`, `shared/`, `tests/`) and R2 (records/registry: this spec tree, `features.md`, `features/093.md`, `register.md`, the spine). R2's repairs are landed in the review worktree (DoD-1/DoD-3/GATE-1 measured wording; GATE-1 headline re-based on `wp5-suite-final.txt`; quickstart live statements; Work Packages write domains reconciled with the disclosed deviations; registry `Blocked`; T-001…T-005 registered and FR-036@093 closed; DoD-8 vocabulary aligned to C-079; checklist header corrections; verification record's SC-006 exit aligned to the state machine, T098 recorded open, SC-008 pointer repaired, SC-004 attribution split); R1's repairs are the sibling fork's deliverable and the driver re-verifies after both return.
- **Close-out**: the line closes **blocked** (U6 — a `block` verdict never becomes `completed`); the registry row lands `Blocked`. Carried residuals: SC-006 (a future run must dispatch `>= 2` units and record per-unit intervals), SC-007/SC-010 `partial`, T098 open by design, F-093-002/020, and the 116-minute 091-figure provenance caveat.

## Plan Notes（2026-11-09，plan 阶段）

- **产物**：`plan.md`（22 条宪法逐条 ✅ Pass；Decision Tensions T-001…T-005；Execution Premises EP-001…EP-010 全 `verified`；Inherited Blockers 4 行）+ Phase 1 五件：`research.md`（14 节实测）、`data-model.md`（11 实体 / 26 规则 / 5 状态机）、`contracts/`（6 文件，**92 条** C-001…C-092）、`quickstart.md`（7 场景）、`feature-ref.md`（33 FR + 12 SC 映射行、逐文件交付面、重叠裁定）。
- **交付面（文件级）**：8 条新声明层 fact（`concurrency-class` / `serial-reason` / `effective-concurrency` / `concurrency-slot-and-reserve` / `decomposition-coverage` / `executor-enumeration-roots` / `concurrency-contract` / `coordinator-dispatch-verdict`）+ `contract.yaml` 登记 + 一个新引擎 `scripts/python/concurrency-check.py` + 10 个新测试模块；既有 owner 文档按章节改写，不新建第二处定义。
- **F-093-001 已解决**：`feature-ref.md` § Overlap adjudication 按**文件级路径**逐条裁定 064 / 070 / 086 / 092（含 `shared/declarations/contract.yaml`、`decomposition-model.md`、`stage-team-preset.md`、`sdd-loop-driver/SKILL.md`、`wp-gate.py` 五处真实同文件重叠的分段处置），并以「区域级声明不算交付面」的实测理由记录 `overlap-check.py` 读数为何不等于裁定。
- **F-093-002 残余**：`overlap-check.py` 在本 worktree 运行得 84 spec / 195 hit（113 为 `nested-path`），本阶段以主仓根 + 文件级阅读作为 workaround 并记录，不视为修复。
- **F-093-003 残余**：`coordinator-dispatch-verdict` 只登记、不自裁，作为 T-004 携带，裁定前 `capability` 判 `owner-unavailable`（退出码 2）。
- **本阶段执行形态**：串行单代理（执行者工具集无派发能力），按 [[STR-010]] 记录 `mechanism-not-yet-landed`，SC-006 记 `not_evaluated`；不得把该串行运行计为并发证据。
- **门读数**：`pre-analyze-check --stage plan` pass（0 error / 44 advisory）、`validate-decision-tensions` pass（5 记录）、`decomposition-check --mode plan` proceed（33 FR）。

## Tasks Notes（2026-11-09，tasks 阶段）

- **产物**：`tasks.md` —— **137** 行任务（T001–T137，8 个阶段：Setup 7 / Foundational 19 / US1 15 / US2 24 / US3 20 / US4 20 / US5 6 / Polish 26），DoD-1…DoD-9 + GATE-1…GATE-7，34 个 `[green: <contract>#<clause>]` 红先标记。
- **默认并发包划分**：5 个包 —— `WP1-facts`（声明层与登记）→ `WP2-engine`（`concurrency-check.py`）/ `WP3-owners`（owner 文档、agent/skill/命令面）/ `WP4-tests`（10 个测试模块）三者**文件级写域两两不相交**，WP1 关闭后同轮就绪；`WP5-release`（证据与发布）串行收尾，集成按声明顺序折叠而非返回顺序。每个包 20–35 行，边界是写域而非行数（拆细会让两个包写同一文件，正是 FR-012 禁止的冲突）。
- **SC-006 处置**：分包已就绪，但本阶段执行体工具集无派发能力，故本轮仍为串行单代理，SC-006 记 `not_evaluated`（[[STR-010]] `mechanism-not-yet-landed`）——不是 `0`、不是估计、不是「用夹具证明并发」。实现阶段若执行体同样无派发工具，必须照此记录并把缺口命名为「缺派发能力」。
- **门读数**：`validate-tasks.py` PASS（0 error / 0 warning，首轮为 2 error / 277 warning，收敛过程写在 `tasks.md` § Notes § Validator adjudication）；`decomposition-check --mode tasks` proceed（33 FR / 137 tasks）；`pre-analyze-check --stage tasks` pass（0 error / 101 advisory，全部是「本特性待创建路径」）。
- **F-093-004（新，框架层）**：`validate-tasks.py` 的 `green-*` 规则要求「一条 clause 只由一行认领」，而 `create-tasks` 技能把同一标记定义为「红先标记」——两者对同一工件给出不同结构断言。本阶段采用标记读法，并把分歧作为 F-093-004 记录，等待单一 owner 裁定。

## Key Changes（landed 2026-11-09）

**As landed (2026-11-09, WP5 release)**: all five surfaces shipped — the eight declaration facts plus their `contract.yaml` registration, the `concurrency-check.py` engine (five read-only actions), the eleven test modules, the revised owner documents / command surfaces, and the 064/070/086/092 disposal ledger (12 rows, C-079 four-value domain). The closure verdict reads `block` on SC-006 alone (no real concurrent run), so the feature lands **`Blocked`**, not `Implemented`.

- **声明层**：新增 `shared/declarations/facts/` 条目承载五个判定面（并发类别 [[STR-001]]、串行理由码 [[STR-003]]、槽位与保留位、单元划分规则标识、枚举根映射 [[STR-008]]），并经既有 `scripts/python/declaration_reader.py` 登记后读取；未登记按 `owner-unavailable` 处理。
- **既有门面的修订面**：`skills/external/sdd-loop-driver/references/decomposition-model.md`（阶段覆盖 [[STR-007]]、槽位/保留位与集成顺序）、`skills/external/sdd-loop-driver/scripts/wp-gate.py`、`skills/external/sdd-loop-driver/templates/stage-team-preset.md`、`skills/internal/create-team/references/conceptual-model.md`、`.specify/shared/definitions/subagent-definitions.md`（派发能力 [[STR-004]]）与 `.specify/shared/definitions/goal-definitions.md`（goal/target）。
- **执行体义务**：`skills/internal/**`（38）、`skills/external/**`（16）、`templates/commands/*.md`（29）、`agents/`（17，含 `.specify/agents/templates/` 投影）、`.specify/teams/`（12）与 `.specify/goal/` 各自读得同一套并发契约；协调者是否可派发由 [[STR-011]] 的单一裁定处回答。
- **既有语义处置**：064 / 070 / 086 / 092 的受影响断言逐条处置（改写 / 保持 / 显式移除），任何改动册正文的处置作为一次带 [[STR-006]] 条目的纪律修订记录。

## Implementation Notes（2026-11-09）

- **Delivery shape**: 159 task rows in 5 write-domain packages (16+26+30+38+49); WP1 `facts` → WP2 `engine` / WP3 `owners` / WP4 `tests` were declared file-level disjoint and executed as the driver's **declared-order serial fold** (`WP1 → WP2 → WP3 → WP4 → enginefix → WP5`), so `effective` is `not_evaluated` with `mechanism-not-yet-landed` — never `0`, never an estimate (`notes/coordination-report.md`).
- **Engine**: `scripts/python/concurrency-check.py` — five read-only actions (`classify` / `serial-reason` / `reading` / `coverage` / `capability`), declaration-driven (eight facts), fail-closed (`owner-unavailable` exit 2), and carrying no numeric ceiling of its own; the 092 reproduction fixture is red before the repair and green after (SC-005, `notes/engine-fix.md`).
- **Enginefix wave**: 23 formerly red contract tests turned green, with three stale test expectations corrected against readings rather than silently (`notes/engine-fix.md` § 5). Acceptance smoke: `test-evidence/wp5-acceptance-final.txt` — 96 passed / 0 skipped.
- **GATE-1**: the final suite (`test-evidence/wp5-suite-final.txt`) reads 207 failed / 8256 passed / 2 skipped; the 46 NEW names are attributed as 44 master-inherited + 2 trigger-order — zero NEW 093-caused (`test-evidence/wp5-gate1-comparison.txt` § Classification).
- **Closure**: `closure-acceptance-check.py` → `verdict: block`, `final_path pass=5 blocked=1 total=6`, sole reason `final-path-not-pass: SC-006`; 159 task sigils remain `[ ]` (flipped by the integration owner at close-out) and T098 is genuinely open by design (F-093-003 — the coordinator-dispatch verdict value awaits its owner).

## Clarify Notes（2026-11-09）

- **绑定**：Mode A 将 `Related Feature` 绑定为本条 Feature 093（新建，Draft），索引行与 `Total Features` 表头同一次编辑。
- **裁定问题 15 条**，全部携机器读数（`test-evidence/overlap-check-clarify.txt`、`declaration_reader.py` 实测、注册表 sweep）；其中 4 条改变了规范形态：串行理由词表与并发条件改为**一一覆盖 + 有序列表**、并发度改为**区间最大重叠数**判据、写域改为**文件级路径集**、`goal` 的 spec-local 层按 085 投影处理而不另立枚举根。
- **编号**：clarify 会话内 4 行并入其前一条（`id-contiguous` 拒绝字母后缀），FR 由 36 → **33**，SC 维持 12，STR 由 7 → **11**（新增 STR-008…STR-011）。
- **登记为 finding（非本规格自修）**：F-093-001 交付面与 064/070/086 在区域级重叠，须由 plan 的 `feature-ref.md` 逐文件裁定并随 FR-033 的处置表落地；F-093-002 `overlap-check.py --repo <内部 worktree>` 的 `current_rel` 以 `..` 开头，导致声明路径被整体过滤为「无交付面」（vacuous clear）；F-093-003 `agents/` 的「Never dispatch another agent」与 `capability-tools` 一致、却与 092 的 6 包声明矛盾，裁定处为 [[STR-011]]。

## Related Specifications

- `.specify/specs/093-concurrency-by-default/requirements.md` — 本特性规格（36 FR / 12 SC）
- `.specify/specs/092-goal-team-parallel/requirements.md` — goal/team 平行模型（本特性处置对象之一；其 `notes/execution-lessons-2026-11-09.md` 记录了 092 的串行实测与平行线 worktree 隔离 addendum）
- `.specify/specs/070-subagent-task-teams/requirements.md` — Work Package 拆解与 `wp-gate.py`（被修订的门面）
- `.specify/specs/064-subagent-concurrency/requirements.md` — 写线 / worktree / integration queue（并发底座）
- `.specify/specs/086-efficient-test-execution/requirements.md` — 测试执行效率（并发语义的既有 owner 之一）

## Status Criteria

- 五个枚举根覆盖的每个执行体能被映射到恰好一个声明类别，且该类别在其正文或指针 owner 中给得出一条可读的并发义务（SC-001）。
- 并发夹具以并发形态执行并记录生效并发度 ≥ 2；串行夹具逐条携带词表内的理由码与可判定依据（SC-002 / SC-003）。
- 七件事（划分 / 写域 / 槽位与保留位 / 独立校验 / 确定性集成 / 失败隔离 / 重入）逐项可判定（SC-004）。
- 092 形态复现夹具在修复前判红、修复后转绿；每个声明并发的执行体具备 [[STR-004]] 或已移交派发（SC-005）。
- 至少一次真实运行产出协同报告并以区间重叠数取证生效并发度（SC-006）。
