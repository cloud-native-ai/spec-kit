# 099 — Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

**Feature ID**: 099
**Name**: Speckit Seal
**Description**: 按 review 结论封装 spec；`Sealed` 是 `Ready for Review` 之后的终态与归档准入状态；承载分片同名输出件的合并回写（split + merge-back）。
**Status**: Ready for Review
**Created**: 2026-11-10
**Last Updated**: 2026-11-11（100 plan：follow-up spec `100-seal-slice-archive` 经 `/speckit.plan` 产出 plan.md / research.md / data-model.md / 3 份契约（40 条款）/ quickstart.md / feature-ref.md；22 项 Constitution 全 Pass、6 条 decision-tension、11 条 Execution Premise 全 verified、Dependency set none、8 个工作包；plan 门禁 pre-analyze pass（errors=0）、validate-decision-tensions ok（6 records）、decomposition proceed、overlap adjudicated（099 绑定增量）；099 状态保持 `Ready for Review`；100 tasks：tasks.md 53 行 / 8 工作包 / 40 条款 `[green:]` 各认领一次，validate-tasks PASS 0/0、decomposition proceed 28/53、覆盖 claimed 40 / FR 28/28 / beyond-baseline 0；见 § Plan Notes 与 § Related Specifications/Requirements）

## Overview

框架的状态机在 `Ready for Review` 之后只有一条从未被任何程序执行的声明式出口（`→ Completed`），
归档入口也从不查询状态；拆分交付的 spec（069a/069b、074a/074b）从未把分片产物并回父级——074 的实测
状态是两片全部闭合（32/32、26/26）而父 `tasks.md` 仍挂 57 个 `[ ]`、父级没有 review 记录、父 requirements
缺 `**Path**` 标记使闭包引擎 exit 2。本特性新增 `/speckit.seal`：把「review 已完成、分片已并回、验收记录
齐备」固定为可判定的终态 `Sealed`，并让「只有 `Sealed` 可归档」成为唯一准入判据；同一条命令承载
split + merge 回写流程，所有同名输出件走同一条确定性流程，冲突显式呈现、不得静默择一。

## Latest Review

- **2026-11-11 `/speckit.review` round 2（四段 + ARC；`Implemented → Ready for Review` 合法并已应用）**：round-1 的 P0 F1 / P1 F2 / P1 F3 经 review-repair r1（`55dd6d61d`）修复并复核——4 个分片 P0/blocking 红先用例转绿，真实 074 重跑两次逐字节一致（exit 2、writes 0、引擎点名 `074b-nested-governance:F1`、47/47 分片 dated record 与两片文件哈希不变），supersede 认领保留（074 道 claimed=144、`074-*` 超基线 0）；seal 家族 137 passed、099 条款覆盖 45/45、镜像与命令副本零漂移、smoke 5/5 exit 0；当前 `code-review.md` 回执 485 / 5 / 480 / 0（changed / judged / skipped / gap），`report --summary --file` 返回 `gate=allow`（blocking 0；1 条 `important` 已答复且不阻断，P2 F9 留在 REC-099-5）；ARC `verdict=accept`，final_path pass 6 / total 6。四条件齐备，状态翻至 `Ready for Review`。遗留 P2：F4–F8、F10（见 `review.md` § 3）。
- **2026-11-11 `/speckit.review`（四段评审 + ARC；`Implemented → Ready for Review` 拒绝：`blocking-unresolved`）**：review.md 与 code-review.md 落盘；过程段 findings P0 1 / P1 2 / P2 7；代码段回执 451 / 29 / 422 / 0（changed / judged / skipped / gap），`report --summary --file` 返回 `gate=deny`（1 条 `blocking`：分片父级的 seal P0 判据只读父级指针视图，切片 review 的 P0 对 `p0-unresolved` 不可见）；实现段复核 P8b 修复可复现（seal 套件 133/133、两次 seal 运行逐字一致、47/47 分片 dated record 哈希不变、smoke 5/5）；ARC `verdict=accept`，final_path pass 6 / total 6，claimed `Implemented` 与记录一致。**状态保持 `Implemented`**：当前 `code-review.md` 含 blocking 条目，未attended 处置为 halt-and-report；P0 的修复或用户显式裁定后方可重跑 review。详见 `review.md` § 2.1 / § 3 F1。
- **2026-11-11 `/speckit.implement`（P9 收尾，`Planned → Implemented`）**：P1–P8b 已闭合（状态域七面、四动作引擎、074 真实回合约 blocked——FR-027(d)+B2 具名，合法）；P9 完成全量套件零新增（serial 定版 268 failed / 8415 passed / 2 skipped，相对 280 条实现入口基线 `comm -13` 为空、12 条基线红转绿；并行样本的 14 条基线外红逐条归因并修复 8 条 pin 漂移，`test-evidence/final-suite.txt`）、镜像与命令副本零漂移（`test-evidence/final-mirror-checks.txt`）、quickstart S-1…S-9 实跑（`notes/quickstart-run.md`，smoke 命令 exit 0）、`verification.md` SC-001…SC-009 全 `pass`（final 6/6，闭包判定 accept，前后两份 payload 在 `test-evidence/closure-verdict-099*.json`）、条款覆盖 45/45（`test-evidence/coverage-final.txt`）。**披露**：T050 延后 `[~]`——074 回合按 merge-back C-022 强制把父级 57 条拆前行的 green 认领转为引用记录，遗留 67 条 074 父契约未覆盖名（逐名归因，非本 spec 契约缺口）；T041 保留 P8 的历史延后记录。仍未 `Sealed`：`Ready for Review → Sealed` 属 `/speckit.seal`（review 完成后）。

## Key Changes

1. 新增命令 `/speckit.seal`：`templates/commands/seal.md` + internal 技能 `skills/internal/seal-artifact/` +
   确定性引擎 `scripts/python/seal-utils.py`（动作封闭集 `merge-plan` / `merge-apply` / `seal` / `archive-gate`；
   退出码 `0/1/2`；stdlib-only）。
2. 状态值域恰 +1：`Sealed`（`Ready for Review → Sealed` 的唯一 owner 是 `/speckit.seal`）；`Sealed` 为终态，
   唯一后向转移是携带证据的审计更正；`Ready for Review → Completed` 对新工作关闭，`Completed` 只留遗产。
3. 状态 owner 与消费面同批同步：`acceptance-hardening.md` § Feature Status（owner）、feature-details /
   feature-index 模板、feature-integration 协议、manage-features 词表、non-disposable 状态表、
   closure completion-claim 家族；消费面集合由静态检索派生并留 `test-evidence/` 证据。
4. 合并回写：15 项输出件封闭宇宙、动作四值（merge/create/keep/not-applicable）、编号重排（父映射复用 +
   分片独有按合并顺序追加）、引用改写、共享字符串对齐、冲突清单、`merge-manifest.json` 归属记录；
   57 行拆前记录按 non-disposable `supersede` 处置（原文保留 + 指针）。
5. 归档准入唯一 owner：`archive-gate` 只读查询；`/speckit.sanitize` 归档 lane、docs lane 与 manage-features
   归档指针在动手前查询，不自判。
6. 074 真实回合（首个验收）：split → merge-back → seal 全流程，五项实测输入缺陷逐条显式处置，
   终态二值（`Sealed` 或至少逐条覆盖五项、并逐条点名额外阻断的具名阻断清单）。

## Plan Notes

- **方案（planned 2026-11-10）**：`plan.md` + `research.md`（R-01…R-20，全部 file:line/实测）+ `data-model.md`
  （14 实体）+ `contracts/`（4 页 45 条款，C-001…C-045 全局连续）+ `quickstart.md`（9 走查，S-1 已实跑并粘贴
  真实输出）+ `feature-ref.md`（FR 28/28、SC 9/9）。
- **合规**：Constitution 22 项全 Pass；Complexity Tracking `N/A`；6 条承重裁决 T-001…T-006（散文合并边界 /
  `Sealed` 终态 / 编号重排 / 准入单 owner / 回合允许阻断 / 写面封闭）。
- **执行前提**：EP-001…EP-012 全部 `verified`；Inherited Blockers `Dependency set: none`（074 是验收目标而非依赖）。
- **执行形态**：9 个工作包、每包 ≤16 行；依赖边 P1 ∥ P2 → P3 → P4 → P5 → P6 ∥ P7-tests → P8 → P9；
  探索波次 requested=4 / effective=4。
- **follow-up 100 tasks（2026-11-11）**：`100-seal-slice-archive/tasks.md` 落盘——53 行（Setup 3 / Foundational 6 /
  US1 12 / US2 11 / US4 5 / US3 8 / Polish 8）、8 个工作包（每包 ≤16 行）、40 条契约条款各被一个任务行
  `[green:]` 认领一次且各契约内随行序单调；Tests Mode ON（宪法 IV）；阶段顺序 F → US1 → US2 → US4 → US3 → Polish
  （服从 plan 的 P1 ∥ P5 → P2 → P3 → P4 → P7 依赖链，099 同型先例）。门禁：`validate-tasks.py` PASS（0 error /
  0 warning）；`decomposition-check.py --mode tasks` proceed（fr_count=28 / task_count=53）；条款覆盖
  claimed 40 / FR 28/28 / uncovered beyond baseline 0（`coverage-baseline.txt` 冻结于 base-sha `90bab87ee3b9`）；
  `concurrency-check.py coverage --stage tasks` pass（covered-by-default）；读数见
  `.specify/specs/100-seal-slice-archive/test-evidence/tasks-stage-checks.txt`。状态保持 `Ready for Review`。
- **阶段门读数**：`test-evidence/plan-stage-checks.txt`（validate-decision-tensions、pre-analyze `--stage plan`、
  decomposition `--mode plan`、mirror/regen 零基线、074 闭包 exit 2、测试入口 32 passed）。

## Related Files

- `.specify/specs/099-speckit-seal/requirements.md`、`plan.md`、`research.md`、`data-model.md`、`contracts/`、
  `quickstart.md`、`feature-ref.md`
- `templates/commands/seal.md`、`skills/internal/seal-artifact/SKILL.md`、`scripts/python/seal-utils.py`（实现阶段落地）
- `shared/workflow/acceptance-hardening.md`、`shared/workflow/feature-integration.md`、
  `shared/definitions/non-disposable-definitions.md`、`shared/definitions/flow-class-definitions.md`、
  `shared/definitions/probe-definitions.md`
- `templates/feature-details-template.md`、`templates/feature-index-template.md`、
  `skills/internal/manage-features/SKILL.md`、`skills/internal/sanitize-materials/SKILL.md`
- `.specify/specs/074-goal-team-sdd-unification/`（074 回合产物）

## Related Specifications/Requirements

- `.specify/specs/099-speckit-seal/requirements.md` — 本 Feature 的主规格（seal 与 merge-back）。
- `.specify/specs/100-seal-slice-archive/requirements.md` — follow-up 规格（2026-11-11 `/speckit.clarify` Mode A 绑定；不新建命令/引擎）。绑定理由：它承接 099 C-019 明确延后的「分片承载物后续处置」复核，把归档步骤固化进既有 `/speckit.seal` 三件产物，并原地扩展 C-001 动作集、C-008 写面与 C-035 边界；099 状态保持 `Ready for Review`。
- `.specify/specs/100-seal-slice-archive/plan.md`（+ `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`）— 2026-11-11 `/speckit.plan` 产出的设计产物面；动作集四→六、归档清单 schema、载体分类与解析定义、074 回合计划。本 Feature 的契约条款在同批实现变更中原地修订（C-001 / C-008 / C-019 / C-023 / C-035 / C-036）。

## Future Evolution Suggestions

- 若回合证明散文合并的窄解释（T-001）不可用，按重开条件评估「经声明的语义合并步骤」。
- 归档准入查询若被 lane 高频调用，评估声明式事实文件缓存（owner 仍唯一，T-004 重开条件）。
