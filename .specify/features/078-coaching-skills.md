# Feature Detail: Coaching Skills（教练技能）

**Feature ID**: 078  
**Name**: Coaching Skills（教练技能）  
**Description**: Coach a Trainee through real work in its own carrier with prior expectations, observed execution, deviation analysis, and improvement plans.
**Status**: Blocked
**Created**: 2026-10-30  
**Last Updated**: 2026-11-22

## Overview

`coaching-skills` now executes the Trainee in its own declared carrier: the coach writes result-correctness and process-efficiency expectations first, records the Trainee's real execution without replacing it with a coach-created subagent workflow, compares expected and actual behavior, and hands the improvement plan to `improve-skills`. Command-side `speckit.` prefixes are stripped only in the command list; skill names are not rewritten through that namespace.

Execution remains primary. Optimization starts only after the real work finishes, and missing observation evidence is disclosed rather than fabricated.

## Latest Review

2026-11-22 audit correction: the new carrier-observation model is present, but the two directed contract modules currently report **12 failed / 21 passed** because they still assert the retired dispatch model. The latest prefix fix exists in framework source but not in the installed coaching mirror. These facts falsify the previous `Implemented` claim, so the index and this detail land `Blocked` under the canonical Implemented → Blocked audit-correction exception. Evidence command: `PYTHONDONTWRITEBYTECODE=1 bash scripts/bash/run-tests.sh tests/contract/test_coaching_run_contract.py tests/contract/test_coaching_dispatch_contract.py -q -p no:cacheprovider`; result: **12 failed, 21 passed**. Complete raw stream: `.specify/.tmp/feature-reconcile-20261122/state/raw-feature-audit-H-audit.jsonl`; semantic comparison: `skills/external/coaching-skills/` versus `.specify/skills/coaching-skills/`.

- 2026-10-30 `/speckit.implement`（4 段）：31/31 任务完成；162 passed / 0 failed（定向集），四冻结基线转绿；quickstart 场景 1–5 实跑（含真实教练闭环与 teardown）；新增行门 0 命中；SC-001/SC-005 因运行由脚本化 one-shot runner 驱动、观测全为 `self-report`，按 review F4 记为 `partial`（宿主原生派发通道未实测）。

- 2026-10-30 `/speckit.requirements`：29 FR / 9 SC / 17 Shared Strings；`validate-requirements.py` 0 error；`decomposition-check.py --mode plan` → `proceed`（29 ≤ 30）；`pre-analyze-check.py --stage requirements` → `pass`（1 条已知 advisory：目标技能路径实现前不存在）。
- 2026-10-30 `/speckit.clarify`（Mode A）：同作者条件下由 2 个 fresh-context 只读子代理分域覆盖扫描；24 条发现，20 条由既有 owner 事实裁决就地修正，4 条写回问答（Feature 绑定 / `<work>` 第二位置参数与双上下文独立性 / 观测通道 / 运行目录与四文件）。规格自查全绿。
- 2026-10-30 `/speckit.plan`：`plan.md`（18 条宪法原则逐行 Pass，`Complexity Tracking` N/A）+ `data-model.md`（8 实体 / 4 状态机）+ `contracts/`（5 份：run / expectation / observation / dispatch-payload / identity-and-wiring）+ `quickstart.md`（5 场景）+ `feature-ref.md` 落盘；两条承重决策记为 T-001（冻结基线用退役路径登记承接改名）与 T-002（优化在教练会话内联调用 improve-skills）。状态 Draft → Planned。`pre-analyze-check.py --stage plan` 结果见 `.specify/specs/078-coaching-skills/test-evidence/`。
- 2026-10-30 `/speckit.checklist`：新增需求质量清单 `checklists/coaching-loop-2026-10-30.md`（36 项，按运行输入 / 预期质量 / 观测 / 载荷 / 改名兼容等主题分组；只判断题面质量，不执行产品）。自查证据见 `.specify/specs/078-coaching-skills/test-evidence/checklist-*.txt`。
- 2026-10-30 `/speckit.tasks`（analyze 回环第 1 轮修复后）：`tasks.md` 31 行（T001–T031），38 条契约条款由 16 行 `[green:]` 认领；`validate-tasks.py` PASS（0 error / 0 warning）；`decomposition-check.py --mode tasks` → `proceed`（fr_count=29 / 30，task_count=31 / 40）；`pre-analyze-check.py --stage tasks` → `pass`（errors=0，52 条 advisory 全为本特性计划新建路径）。

## Key Changes

1. 重命名 `think-skills` → `coaching-skills`，并同步八处身份坐标（目录、frontmatter `name`、`skill_id`/Canonical ID、unit id `skill:coaching-skills`、flow-class 行、probe 行与 probe id、`/speckit.skills` 路由行、description 触发词）。
2. 语义从「静态推演」升级为「预期 → 真实执行 → 观测 → 提升计划」的教练闭环，保留原推演流程作为预期阶段的产出机制。
3. 新增双上下文契约：教练与 Trainee 各自独立理解同一份 `<work>`，派发载荷只带 work 原文，禁止教练预消化（FR-029）。
4. 新增可观测记录契约：逐步骤记录动作/工具/产物/耗时/状态与来源（`host-event` / `self-report`），不可见步骤标 `observation-gap`，缺口计数只数步骤行。
5. 运行产物独立落盘：`.specify/memory/coaching/<run-id>/` 下 `expectation.md` / `observation.md` / `deviations.md` / `improvement-plan.md`；同一 Trainee 的优化禁止并发应用。

## Implementation Notes

- 旧目录名进入 `src/specify_cli/__init__.py` 的 `_OBSOLETE_SKILLS`，`specify init` 清理旧实体目录但保留用户自建的同名符号链接。
- 四个冻结基线测试（expression compatibility / migration distribution / skill layer visibility / run-skills wiring）必须显式更新并注明日期与理由，不得静默改计数。
- 派生面（`.specify` 镜像、命令副本、渲染后的宿主 agents、编译的 `## Wrap-up`、probe-map）只能由既有再生成入口产出。
- 门禁预算余量为 0：新增/改写的扫描面文案必须 0 命中 `BLOCKING_PATTERNS`，判定单位为 `git diff` 的新增行，基线读数记入测量证据。
- 历史记录（`.specify/specs/**`、`memory/evidence/**`、features 详情、reviews、eval-baseline、旧 unit id 的 run 记录）不改写；旧名只允许出现在 `_OBSOLETE_SKILLS` 与 dated record 中。

## Future Evolution Suggestions

- 支持对同一 Trainee 的多次教练运行做趋势对比（跨 run 的效率/正确性漂移）。
- 为「提升计划」增加与 `improve-skills` 执行结果回写的闭环校验（计划 vs 实际改进）。
- 评估把运行目录纳入 `/speckit.sanitize` 的保留期治理。

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/078-coaching-skills.md
- Spec: .specify/specs/078-coaching-skills/requirements.md
- Checklist: .specify/specs/078-coaching-skills/checklists/requirements.md；.specify/specs/078-coaching-skills/checklists/coaching-loop-2026-10-30.md

## Related Specifications/Requirements

- .specify/specs/078-coaching-skills/requirements.md（本 Feature 首个规格）
- Related Features: 057 命令技能化分解补全（modify 族边界：`create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` / `run-skills`）、013 Skills Command（`/speckit.skills` 路由面）、062 Humanize Command（新增 external 技能的近例）。
- 历史沿革：本技能由 `thought-experiment-verifier` → `think-skills` → `coaching-skills`；前两次更名记录见 `_OBSOLETE_SKILLS` 注释。

## Status Tracking

- **Draft**: requirements 已澄清，checker exit 0。
- **Planned**: plan.md + Phase 1 产物落盘，Constitution Check 无未证成 Fail。
- **Implemented**: previously recorded from 31/31 tasks and the earlier verification set; falsified for the current tree by the 2026-11-22 audit evidence above.
- **Blocked** (current): current directed contracts fail and the source/installed mirror semantics are not synchronized.
- **Ready for Review**: requires the contract and mirror gaps to be repaired and fresh review evidence produced.
- **Completed**: 最终验收。
