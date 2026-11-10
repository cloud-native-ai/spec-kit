# 099 — Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

**Feature ID**: 099
**Name**: Speckit Seal
**Description**: 按 review 结论封装 spec；`Sealed` 是 `Ready for Review` 之后的终态与归档准入状态；承载分片同名输出件的合并回写（split + merge-back）。
**Status**: Implemented
**Created**: 2026-11-10
**Last Updated**: 2026-11-11

## Overview

框架的状态机在 `Ready for Review` 之后只有一条从未被任何程序执行的声明式出口（`→ Completed`），
归档入口也从不查询状态；拆分交付的 spec（069a/069b、074a/074b）从未把分片产物并回父级——074 的实测
状态是两片全部闭合（32/32、26/26）而父 `tasks.md` 仍挂 57 个 `[ ]`、父级没有 review 记录、父 requirements
缺 `**Path**` 标记使闭包引擎 exit 2。本特性新增 `/speckit.seal`：把「review 已完成、分片已并回、验收记录
齐备」固定为可判定的终态 `Sealed`，并让「只有 `Sealed` 可归档」成为唯一准入判据；同一条命令承载
split + merge 回写流程，所有同名输出件走同一条确定性流程，冲突显式呈现、不得静默择一。

## Latest Review

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

## Future Evolution Suggestions

- 若回合证明散文合并的窄解释（T-001）不可用，按重开条件评估「经声明的语义合并步骤」。
- 归档准入查询若被 lane 高频调用，评估声明式事实文件缓存（owner 仍唯一，T-004 重开条件）。
