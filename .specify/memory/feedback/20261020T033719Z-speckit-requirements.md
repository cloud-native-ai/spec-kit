---
id: "20261020T033719Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "064-subagent-concurrency-requirements-20261020"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "064-subagent-concurrency"
partial: false
created: "2026-10-20T03:37:19Z"
summary: "为 Feature 064 创建 requirements.md 与质量检查单：读取 brief、宪法、sdd-loop-driver/run-agent 机制文档与 063 在途契约，写出 5 个用户故事、68 条 FR、10 条 SC、4 条 Shared Strings；validator 首轮 1 处 Shared Strings 反向引用失败（SC-003 未以 [[STR-002]] "
---

## Review
为 Feature 064 创建 requirements.md 与质量检查单：读取 brief、宪法、sdd-loop-driver/run-agent 机制文档与 063 在途契约，写出 5 个用户故事、68 条 FR、10 条 SC、4 条 Shared Strings；validator 首轮 1 处 Shared Strings 反向引用失败（SC-003 未以 [[STR-002]] 引用）已修复，最终 0 error / 0 warning；显式记录 063 provisional CLI-profile 重叠与 061 CAPABILITY_MATRIX 边界，交由 analyze/plan 裁决。脚手架脚本因其无条件 git checkout -b 与既有 064 分支冲突，按等价手工搭建并留痕。

## Optimization Points
- # Feedback points — 064 requirements run (2026-10-20)
- 1. **`create-new-requirements.sh` cannot reuse an existing feature branch.** The script unconditionally runs `git checkout -b "$BRANCH_NAME"`; when the orchestrator has already created and checked out the feature branch (normal for sdd-loop-driver stage dispatch), the script fails with "branch already exists" before creating the spec directory or the template. Proposed fix: detect an existing target branch (or an already-checked-out branch) and skip creation, or add a `--reuse-branch` / `--no-branch-create` mode while preserving the existing no-clobber guard. Evidence: this run started on `064-subagent-concurrency`; the scaffold script's branch step was incompatible, so the spec dir/template were reproduced equivalently by hand and disclosed in the stage report.
- 2. **Requirements template has no optional slot for cross-feature in-flight overlap.** Feature 064 must record that Feature 063's in-flight branch provisionally carries the same CLI-profile scope and hand the per-clause disposition to analyze/plan. The template's open-ended structure allows a new section, but every such run reinvents the shape. Proposed fix: add an optional "Cross-Feature Overlap" section (or guideline snippet) in the requirements template/guidelines with the record-only, no-dual-owner, analyze/plan-reconciliation wording. Evidence: this run added `## 跨特性重叠与边界` manually.
