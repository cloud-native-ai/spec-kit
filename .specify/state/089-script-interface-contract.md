# Line State — 089-script-interface-contract

<!-- loop-state:begin -->
spine_state: completed
run_id: r20261106T090000Z-086a
slice: 089
stage: implement
stage_started_at: 1793959000
stage_deadline_epoch: 1793976400
stage_base_commit: ea2f3f0d
attempt: 1
retry_limit: 3
last_verdict: merged to master (2026-11-09) as 089-script-interface; SC-003 green (751 candidates / 0 violations / 737 exemptions); the merged-tree suite matches the origin/master failure set except environment-only cases; the feature was renumbered from 086 to 089 to avoid the remote 086
driver_contract: |
  HR1 — U4 pass => dispatch the next stage/package in the same turn; never ask "continue".
  HR4 — write this spine BEFORE U2, at U3/U4/U5; reentry reads only this, never conversation memory.
  HR5 — a subagent turn limit is a bounded stall: split the package or finish driver-side; write stalled/reentry-required only at the retry limit.
  Reporting — a progress report is a statement, not an approval request.
  Workspace — run workspace-guard --check before accepting any package; drift rejects the package.
next_action: 089 closed and pushed; start the 090 Re-Anchoring SDD chain (clarify -> plan -> tasks -> review) on top of this trunk
direction_contract: |
  goal_verbatim: "为了避免后续再出现『执行 generate-instructions.sh --help 想看接口，该脚本没有 --help 处理，直接把一次 reconcile 跑了起来』这样的问题，需要在 constitution 中增加所有的 *.sh/*.py 脚本都需要默认添加 --help/--version 参数"（补充裁定：通用规则，落点含 templates/constitution-template.md 与 templates/instructions-template.md，不只服务本仓库）。
  non_goals: [纯库加 help, 脚本内部重构或统一 CLI 库, 改 src/specify_cli 的 Typer CLI, 每脚本独立版本系统, 新增命令或门禁, 追溯改写历史记录]
  acceptance_authority: requirements.md 的 31 FR / 12 SC；final 路径 SC 以 test-evidence 读数为准
  stage_plan: [requirements, clarify, plan, tasks, checklist, analyze, implement, review, closure]
  decision_gates: [routing, split-required, fast-fail-decision, destructive-confirmation]
  forbidden_drifts: [包边界征求继续, 状态脊滞后, 子代理轮次上限当作交回理由, 探针越界运行]
temp_team_slug: 089-script-interface-contract
split_required: |
  measured: fr=31, tasks=87
  ceilings: fr=60, tasks=80
  reasons: ["task rows=87 exceeds ceiling 80"]
  base_commit: 56dc6dfd
  proposed_slices:
    - id: 086a-script-interface-governance
      theme: 规则文本与五处治理落点 + help/version/未知选项的行为保证 + 豁免判据
      tasks: Setup 5 + Foundational 6 + US4 18 + US6 6 + US1/2/3 5 + Polish（治理部分）约 5 = ~45
      fr_scope: FR-001, FR-003..FR-016, FR-023..FR-031（约 22 条）
    - id: 086b-script-interface-enforcement
      theme: 检查器引擎 + 契约测试 + 本仓脚本补齐 + 镜像投影与回归
      tasks: US5 37 + Polish（执行部分）约 5 = ~42
      fr_scope: FR-002, FR-010, FR-017..FR-022（其余）
  status: resolved-by-gate-uplift (b6bb7356 raised FR/TASK ceilings to 120/160; the tasks gate re-measured proceed at 31/87 on 2026-11-06)
framework_observation: |
  efficiency-model.md §5.1 的 plan 入口判据写「FR > 30」，而 decomposition-check.py 的 FR_CEILING=60 同时用于 plan 与 tasks；两处对同一门给出不同阈值，属 owner 文档与引擎的漂移，建议后续记录为框架反馈。
plan_constraint: inactive
temp_goal_slug: script-interface-contract
<!-- plan-fence: decomposition=auto@plan-entry; test-budget=baseline@implement-start + closure@post-review; fast-lane=not-adopted -->
<!-- loop-state:end -->

- line_id: `089-script-interface-contract`
- run_id: `r20261106T090000Z-086a`
- project_dir: `/cws_data/cloud-native-ai/spec-kit`
- repo_root: `/cws_data/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，主工作区；特性分支由 requirements 阶段创建 089-script-interface-contract）`
- base_sha: `24cb4edc`
- trunk: `master`
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/cws_data/cloud-native-ai/spec-kit`）
- **执行拓扑**：本地（宿主原生子代理）
- **终态权威文档**：用户本轮需求（"所有 *.sh/*.py 脚本都需要默认添加 --help/--version 参数"；"这是一个通用规则，不仅仅限定在 spec-kit 自身"）+ 目标仓 `.specify/memory/constitution.md` + `.specify/instructions.md` + `templates/constitution-template.md` + `templates/instructions-template.md` + `.specify/shared/guidelines/confirmation-gates.md` + `.specify/shared/guidelines/temp-directory-discipline.md`
- **特性切片**：Feature 086 `089-script-interface-contract`——新增通用治理规则：所有可直接执行的 `*.sh` / `*.py` 脚本 MUST 支持 `--help`（含用法、参数、副作用、退出码）与 `--version`，且任一标志在场时 MUST 零副作用、MUST NOT 执行主动作；被 source/import 的纯库文件豁免。落点：框架模板（constitution-template + instructions-template）、本仓宪法、manage-constitution 的 MUST include 清单、镜像与契约测试 pin。
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链
- **拆解开关**：`decomposition=auto`
- **测试预算**：implement 起点一次全量基线、review 后 closure；中间定向集
- **类别四元组（requirements 派发）**：`flow_class=null`；`source=default`；`marker=`；`error=owner-unavailable`（spec 目录与 requirements.md 尚不存在，引擎按 class-resolution C-003 退出码 2；requirements 阶段自身写入 `**Flow Class**` 声明行后再解析）

## U1 断点探测（2026-11-06 07:55 UTC）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `master` |
| 工作树 | 干净（会话开始快照） |
| 最近提交 | `24cb4edc`（merge 085） |
| spec 目录 | 最高 `085-sdd-temporary-goal-team`；无 086 目录 |
| 治理 | constitution v1.16.0；instructions 含 Fast Fail / One Source / Two Hats / Directory Governance 等 |
| 结论 | **断点 = requirements**；新建 Feature 086，分支 `089-script-interface-contract` |

## 阶段记录

| 阶段 | 状态 | 证据 |
|------|------|------|
| requirements | DONE | `27b8080d` + `5b470835` + `19f53dd2`；requirements.md（23 FR / 8 SC / 7 用户故事 / 9 Assumptions）、checklists/requirements.md、test-evidence/requirements-gates.txt、features/086.md、features.md 086 行 |
| requirements U4 | PASS（2026-11-06 08:00 UTC） | 驱动者独立复跑：validate-requirements ok（303 行，0/0）、pre-analyze pass（0 advisories）、decomposition proceed（23/60）；记账缺失已由驱动者补跑三步（session + feedback 已落盘）；checkpoint `checkpoints/01-requirements.md` |
| 异常（驱动者观测） | goal-utils.py 参数顺序陷阱 | `--scope spec --spec-dir <dir>` 放在子命令**之前**时被静默忽略，Goal 落到全局 `.specify/goal/`；改到子命令之后才生效。误建产物已由驱动者清理并正确重建到 spec-local `goal/`。正属本特性要治的「未知/错位参数被静默吞掉」问题，交 analyze/implement 记录 |
| clarify | DONE | `bed9f256`；9 条 Q/A 写回，FR 23→31、SC 8→12；驱动侧修复 `ef00a9f5`（8 条 FR 行补 ASCII 冒号） |
| clarify U4 | PASS（2026-11-06 08:09 UTC） | validate ok（374 行，0/0）、pre-analyze pass（0 err / 8 advisory 均计划路径）、overlap clear；记账缺失已补跑三步；checkpoint `checkpoints/02-clarify.md` |
| plan | DONE | `f259f157`；plan.md（19/19 Pass）+ research / data-model / quickstart / feature-ref + contracts×4（C-1…C-38） |
| plan U4 | PASS（2026-11-06 08:22 UTC） | pre-analyze plan pass（0 err / 35 计划路径 advisory）、decision-tensions 0/0、sync-mirrors 0 drift、requirements 零改动；4 条 PLAN-EDIT 已声明；classification 事实更正；Temporary Team 已创建；checkpoint `checkpoints/03-plan.md` |
| tasks | DONE | `56dc6dfd`；tasks.md（87 行 T001–T087，Tests Mode ON，31 FR / 12 SC 全追踪，38 clauses 各认领一次） |
| tasks U4 | PASS（2026-11-06 08:56 UTC） | 首次门判 split-required（87>80）；用户裁定提高上限后 `b6bb7356` 把 FR/TASK 上限改为 120/160 并复跑 82 项测试通过；3 条 runtime-stack-row 由驱动者补行级 FR 引用后转绿；checkpoint `checkpoints/04-tasks.md` |
| checklist | DONE | `6156c668` + `726100dd`；`checklists/contract-integrity-2026-11-06.md`（CHK001–CHK060，10 维，60/60 可追溯）；既有 requirements checklist 零改动 |
| checklist U4 | PASS（2026-11-06 08:59 UTC） | 新清单文件存在；驱动者更正清单里 34/34 的错误 section 读数（实测 32/33，pin 32/33）；6 条 stage anomalies 转 analyze；checkpoint `checkpoints/05-checklist.md` |
| analyze | DONE / gate NOT GREEN | 报告在阶段日志；CRITICAL 0 / HIGH 6（F-01 SC-006 计数等式不可满足、F-02 data-model V-13..22 条款错位、F-03 四处 clause 交叉引用、F-04 SC-012 空登记不可执行、F-05 coverage-baseline 缺失、F-06 规模门记录过期）/ MEDIUM 10 / LOW 6；记账已由执行者写入 |
| analyze 回环 1 | DONE | requirements 修复 `5c2bb98f`（F-01/F-04/F-07/F-08/F-09/F-10/F-11/F-14）；设计与任务修复 `8e410a88`（F-02/F-03/F-05/F-06/F-12/F-13/F-15/F-16/F-17..F-22）；子代理在 150 轮触顶，驱动者补齐 clause 级 FR 引用组；coverage 31/31 ok；validate-tasks 0 error / 73 warning；pre-analyze tasks pass；decomposition proceed |
| analyze round 2 | NOT GREEN（CRITICAL 0 / HIGH 4） | H-01 SC-012 取证肢残留、H-02 feature-ref §3 FR 映射全错、H-03 墓碑 FR-028 被当有效条款、H-04 sandbox 退出码冲突；修复 `754f3d3b` |
| analyze round 3 | **GATE GREEN**（CRITICAL 0 / HIGH 0 / MEDIUM 8 / LOW 10） | 4 条 HIGH 全关；13 条 implement-affecting MEDIUM 由驱动者收口；coverage 31/31、validate-tasks 62 warning、门禁全绿；checkpoint `checkpoints/06-analyze.md` |
| implement | in progress | T001–T077 + T088–T091 done; T092/T093/T078–T087 open. Packages: 121b605e, b33751cc, efa3a270, b5585cb4, 8a6bcc4e, b66f6abd, 87454622, c5c9ccc2, 516cb8f2, d7c41d52, 185a6d69, 52bde156, b7de8202, 2cc87185, ea2f3f0d |
| 流程复盘（2026-11-08） | 无人值守在回合级失效 | 阶段机自走，但包边界以「要我继续吗？」收尾，违反 HR1；状态脊 last_verdict 长期停在包 1，违反 HR4；子代理 500 轮上限未按 HR5 作有界停顿处置。修复：本状态脊新增 driver_contract 与 next_action；每包验收前跑 workspace-guard --check；报告只作陈述，不作确认门 |
| 异常（子代理状态污染） | 已安全收拢 | 子代理误跑 40 次 requirements 脚手架，生成 `087`–`126` 的 40 个分支与同名 spec 目录；主线 086 未受影响。处理：`126` 的合法提交 `d7c41d52` 已 fast-forward 合入 086；40 个目录移入 `/var/tmp/086-spurious-specs-20261107/`（可逆）；40 个分支清单存 `/var/tmp/086-spurious-branches.txt` 后删除 |
| 异常（零回归） | 已修复 | `common.sh` 的发布清单漏了 `git_repo_root`/`git_current_branch`/`is_git_repo`，使 `check-prerequisites.sh --paths-only` 输出空路径；已补入并复测（94 契约测试绿，路径输出正常） |


## U5 stall report (2026-11-08)

- **What was found**: SC-003 cannot reach 0 under the current spec. The full contained run (606 s, 751 candidates) reports 488 violations; 453 are under `tests/**` — pytest modules that cannot meaningfully carry `--help/--version`, and the declared-exception register only accepts `skills/external/<skill>/` scripts. The remaining 35 are separable corrections (out-of-scope `src/specify_cli/**`, historical `.specify/specs/*/notes/**`, mirror inheritance, ~9 real script gaps).
- **Why it is heavy**: this is a scope decision, not a fix. Option 1 (pytest-module exemption by run semantics) makes SC-003 reachable; options 2/3 are absurd or require a requirements amendment.
- **Intermediate artifacts** (all locatable): `test-evidence/closure-check.json`, `verification.md`, `SC-001/002/004-012` evidence, `checkpoints/07-implement.md`, commits `e75e10a4` / `90996f8f`.
- **Options**: (1) ratify the pytest-module exemption and resume T080/T081/T083/T086/T087 + the 35 corrections; (2) narrow SC-003 by requirements amendment; (3) stop at Blocked with the current evidence.

## Closure note (2026-11-08)

- The T086 suite first hung on `.specify/scripts/bash/check-prerequisites.sh`: the bash backfill had left the
  original entry block inside `main`, so every successful run re-entered `main`. The same duplicate was present in
  eight command scripts (check-prerequisites, collect-history, create-new-plan/skill/tools, detect-feature-context,
  refresh-tools, research-project); all were fixed and the mirrors re-projected (`48ccccd7`).
- Per the user's explicit instruction, the closure proceeds without the `/speckit.review` stage; this deviation is
  recorded here and is carried into the feature record (Dogfooding deviation logging).
