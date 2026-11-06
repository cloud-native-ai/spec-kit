# Line State — 084-harness-triple-structure

<!-- loop-state:begin -->
spine_state: done
run_id: r20261105T074027Z-084a
slice: 084
stage: closure
stage_started_at: 1793910800
stage_deadline_epoch: 1793916200
stage_base_commit: e22688da
attempt: 2
retry_limit: 2
last_verdict: Completed (user acceptance 2026-11-06). Closure GREEN: final suite 23F/7250P/4S, 0 new vs baseline, 2 mirror fixed; closure-acceptance-check accept; budget audit baseline:1 closure:1 (known stages=6 complete=0 audit limitation). Local master 3ffeb26e..e22688da, feature branch deleted, registry closed; acceptance committed; pushing gitlab/github/gitee master (origin upstream read-only, never pushed)
plan_constraint: active
plan_activated_at: 2026-11-05T08:22:55Z
plan_commit: 4b65517c
approved_baseline_commit: 4b65517c
<!-- plan-fence: decomposition=auto@plan-entry; test-budget=baseline@implement-start + closure@post-review; fast-lane=not-adopted -->
<!-- loop-state:end -->

<!-- test-budget:begin -->
{"seq": 1, "slot": "baseline", "stage": "implement", "purpose": "implement-start baseline (Part 1)", "trigger": "Part 1 start", "at": "2026-11-05T11:19:40Z", "command": "bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/baseline-failed.txt", "selection_basis": "full-suite", "rc": 1, "passed": 7151, "failed": 25, "skipped": 4, "failed_names_path": ".specify/specs/084-harness-triple-structure/baseline-failed.txt", "evidence_ptr": ".specify/specs/084-harness-triple-structure/test-evidence/baseline-full-suite-2026-11-05.txt", "comparison_set": ".specify/specs/084-harness-triple-structure/test-evidence/baseline-pre-existing-failed.txt (23 names; 2 mirror ids expected until T026)", "merge_source": "na", "merged_at": "na", "test_budget_after_baseline": "waived-by-user (2026-11-05) until the user authorized the final test budget; superseded by the seq=2 closure row"}
{"seq": 2, "slot": "closure", "stage": "closure", "purpose": "post-review closure full suite (in-slot rerun after closure regression fixes)", "trigger": "review passed + closure repair bd872308", "at": "2026-11-06T02:00:00Z", "command": "bash scripts/bash/run-tests.sh --names-out .specify/specs/084-harness-triple-structure/final-failed.txt", "selection_basis": "full-suite", "rc": 1, "passed": 7250, "failed": 23, "skipped": 4, "failed_names_path": ".specify/specs/084-harness-triple-structure/final-failed.txt", "evidence_ptr": ".specify/specs/084-harness-triple-structure/test-evidence/closure-full-suite-final-2026-11-06.log", "baseline_compare": "comm -13 baseline-failed.txt final-failed.txt -> 0 new; comm -23 -> 2 fixed (mirror ids)", "in_slot_rerun": "trigger=closure regression fixes; evidence=bd872308", "merge_source": "local-ff", "merged_at": "2026-11-06T02:01:18Z"}
<!-- test-budget:end -->

- line_id: `084-harness-triple-structure`
- run_id: `r20261105T074027Z-084a`
- project_dir: `/storage/project/cloud-native-ai/spec-kit`
- repo_root: `/storage/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，主工作区；特性分支由 requirements 阶段创建 084-harness-triple-structure）`
- base_sha: `3ffeb26e`
- trunk: `master`
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/storage/project/cloud-native-ai/spec-kit`）
- **执行拓扑**：本地（宿主原生子代理）
- **终态权威文档**：用户本轮需求（"在所有涉及到 harness 的流程中，需要使用 markdown + yaml + script 的三重结构来实现，之前主要使用 markdown + script 的两层结构"）+ 目标仓 `.specify/memory/constitution.md` + `.specify/instructions.md` + `.specify/shared/guidelines/better-harness.md` + 现有 `templates/`、`shared/`、`skills/`、`scripts/`、`src/`
- **特性切片**：Feature 084 `084-harness-triple-structure`——把 harness 相关流程的载体从 `markdown + script` 两层结构升级为 `markdown + yaml + script` 三层结构；具体「harness 流程」边界、YAML 层职责与迁移范围由 requirements/clarify 阶段定义
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链
- **拆解开关**：`decomposition=auto`
- **测试预算**：implement 起点一次全量基线、review 后 closure；中间定向集
- **类别四元组（requirements 派发）**：`flow_class=null`；`source=default`；`marker=`；`error=owner-unavailable`（spec 目录与 requirements.md 尚不存在，引擎按 class-resolution C-003 退出码 2；requirements 阶段自身写入 `**Flow Class**` 声明行后再解析）

## U1 断点探测（2026-11-05 07:40 UTC）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `master` |
| 工作树 | 干净（会话开始快照） |
| 最近提交 | `3ffeb26e`（081 final acceptance；081 已合并并删除特性分支） |
| spec 目录 | 最高 `081-acceptance-hardening`；无 082/083/084 目录 |
| Feature 注册表 | 无 084（`grep -nE "^\| 08[0-4]"` 仅命中 081 行） |
| 治理 | constitution v1.15.0；instructions 含 Two Hats / One Source / Fast Fail / Token Efficiency / Directory Governance / Better Harness |
| 结论 | **断点 = requirements**；新建 Feature 084，分支 `084-harness-triple-structure` |

## 阶段记录

| 阶段 | 状态 | 证据 |
|------|------|------|
| requirements | attempt 1 FAILED（turn budget 40，scaffold only）；attempt 2 dispatched（SDD Executor，120 turns） | 分支 `084-harness-triple-structure` 已建；`.specify/specs/084-harness-triple-structure/requirements.md` 为未填充模板；无提交 |
| requirements | DONE（attempt 2） | `requirements.md`（19 FR + 6 SC + 14 STR）、`checklists/requirements.md`、`test-evidence/{validate-requirements.txt,flow-class-lookup.txt,stage-status.md}`；提交 `a94c3945`；checker `status: ok` 0 error / 0 warning；`flow_class=execution source=declaration`；下一阶段 `clarify` |
| requirements U4 | PASS（2026-11-05 07:53 UTC） | `cd446a6e`（驱动者修复：补 § Runtime Stack & Dependency Ownership + 刷新证据）；decomposition `proceed`（19/30）；pre-analyze `pass`（errors=0，advisories=12 均为计划路径）；validate-requirements `ok`（250 行） |
| clarify | DONE（Mode A，零提问） | `171c2ff8`；A1–A10 全裁定（ratified 7 / revised 2 / A10 后半 superseded）；A8 拆为 Path in-scope + 标签集不迁（N7）；Feature 084 绑定（`features.md` 77=77，`features/084.md` Draft） |
| clarify U4 | PASS（2026-11-05 08:03 UTC） | overlap `clear`；pre-analyze requirements `pass`（errors=0，advisories=15 均为计划路径）；validate `ok`（282 行）；flow-class `execution/source=declaration`；feedback 带 feature 字段 |
| plan | attempt 1 FAILED（turn budget 120，产物已落盘未提交）；attempt 2 有界补完 DONE | `4b65517c`；plan.md / data-model.md / contracts×5 / quickstart.md / research.md / feature-ref.md；Feature 状态 Draft → Planned；pre-analyze plan pass、decomposition proceed、decision-tensions ok |
| plan U4 | PASS（2026-11-05 08:22 UTC） | 驱动者独立复跑三门前置一致；`requirements.md` 相对 `171c2ff8` 零改动（无 PLAN-EDIT）；`plan_constraint=active` 自 `4b65517c` 生效 |
| tasks | DONE | `5dc5919a` + `8ed70a87`；tasks.md（31 行，全部 `[ ]`；Setup 2 / Foundational 5 / US1 3 / US2 7 / US3 2 / US4 4 / Polish 8；Traceability 31 行；Tests Mode ON）；两条 ANOMALY 已披露 |
| tasks U4 | PASS（带 2 条待 analyze 裁决的异常） | validate-tasks `PASS 0/0`；decomposition tasks `proceed`（31/40）；plan-owned 零 diff；commit `5dc5919a`；`[green:]` 为可选面，未启用不构成门禁缺口 |
| checklist | DONE | `checklists/layer-criteria-2026-11-05.md`（38 条，CHK001–CHK038，100% 可追溯）、`test-evidence/{checklist-self-check.txt,flow-class-lookup-checklist.txt,stage-status.md}`；提交 `9abb10fb`；自检 `status: ok`；`flow_class=execution source=declaration`；`stage-status` 记 `not-run-docs-only`（`stage_base=8ed70a87`）；requirements/tasks/plan-owned 零 diff（无 PLAN-EDIT）；3 条 ANOMALY 交 analyze |
| checklist U4 | PASS（带 3 条待 analyze 裁决的异常） | 新增清单文件存在且未覆盖既有 `requirements.md` 清单；冻结面零 diff；commit `9abb10fb`；checklist 门判据（新增清单文件）成立 |
| analyze | DONE / gate NOT GREEN（round 1） | `test-evidence/analyze-report-2026-11-05.md`；1 CRITICAL + 2 HIGH + 10 MEDIUM + 4 LOW；4 个只读验证器 3 confirm / 1 downgrade / 0 reject；`git status` 前后一致；无提交（只读） |
| analyze 回环 1 | requirements 修复 DONE `fd84ed63`；plan 修复 DONE `9284c789`；tasks 修复 DONE `2b18485e` | 10 条 requirements findings + F-02/F-07/C-01 + F-05/E-01/F-09/G-01 全处置；四道确定性门全绿 |
| analyze round 2 | **NOT GREEN**（CRITICAL 0 / HIGH 2） | `test-evidence/analyze-report-round2-2026-11-05.md`；R2-01 已机械修复 `43dcf30e`（单测 `test_c2_no_project_side_classification_store` 1 passed）；R2-02 未决（8 条 `engine side=none` 行）；R2-03 MEDIUM（tasks banner 旧前提）、R2-04 LOW（commit message 拼写）；回环预算用尽 |
| U5 停线 | stalled / reentry-required | 状态脊本文件；Registry `state=stalled`；不合并、不 push、不进入 implement |
| 用户裁定 | **路径 A**（2026-11-05） | 重开 plan：8 条 `engine side=none` 事实移出 in-scope / 改判 `no-machine-fact`，同步 C-044/C-045、T015/T016 与范围表；回环预算由用户显式重置，修复后跑 analyze round 3 |
| plan reopen（路径 A） | DONE | `ba141671`；8 条无引擎事实移出（C-044 14→7、C-045 8→7）；新增 § Facts outside the roster（8 行 unit 级排除记录）；T015 只留 ARC、T016 去 `history-categories`；范围表 3 行 excluded + 2 行 in-scope（D2 列订正）；gates 全绿（clause 59 不变） |
| R2-03 修复 | DONE | `b1b19e93`；tasks banner 改为「58 条款已重编号、`[green:]` 可选未使用、0/19 非解析失败」；validate-tasks PASS |
| analyze round 3 | **GATE GREEN**（CRITICAL 0 / HIGH 0 / MEDIUM 3 / LOW 2） | `test-evidence/analyze-report-round3-2026-11-05.md`；R2-01 / R2-02 / R2-03 全闭环；覆盖率车道非 blocking 判断维持；证据提交 `9657885f` |
| implement Part 1 | DONE（attempt 2 有界补完） | T001-T007 `[X]`；`e3e0af68` + `72044bb3` + `fa7ce0f1` + `8ed7bedb`（reader + checker）；契约模块 22/22；E3 行在 `stage-status.md` § implement Part 1 |
| implement Part 1 U4 | PASS @3ad6a85c | E2 baseline 25F/7151P/4S（比较集 23 names）；定向集 2330P/16F（其中 2 条 mirror 待 T026，1 条 test_c57 已修 `3ad6a85c`）；无全量重跑；plan-owned 零 diff |
| implement Part 2 | attempt 1 PARTIAL（120 回合停在 T012）；拆为 Part 2a（T008-T012）+ Part 2b（T013-T014） | 批 1 facts 已写盘（feedback/evidence/flow-class 共 8 个）；`feedback-utils.py` / `evidence-utils.py` / `flow-class-check.py` / carriers 已改未提交；flow-class 仍有 shadow 常量，T010 读数缺失 |
| implement Part 2a | DONE | `16dcbdf2`；T008-T012 `[X]`；8 个批 1 facts + 4 个引擎 + carriers；`test_harness_triple_structure.py` 47/47；US1 读数 `test-evidence/us1-single-definition-point.txt`；E3 行在 `stage-status.md` § implement Part 2a |
| implement Part 2b | DONE（partial，@8ebee054） | T013 Path 迁移 + `expression-gate-faces` / `expression-stage-operator-table` facts + operator-table 声明列读取；contract 50/50；081 77/77 且两个测试文件零 diff；4 条 `driver-*` facts 与 T013/T014 勾选未完成 |
| implement Part 2c | DONE | `5bf3a7d2`；两条 driver facts + `loop-state.py` 读取点；T013 `[X]`；定向 449P/13F（10 基线 + 3 镜像类，镜像归 T026） |
| Path carrier 纠正 | DONE | `f64cde10`；`create-requirements/SKILL.md` 从 `former_carriers` 移出（从未重述 + 069a 冻结），`third-layer-missing` 清除；`PLAN-EDIT: contracts/migration-batches.contract.md — row 9 carrier annotation；分类=minor` |
| implement Part 2d | DONE | `3f4d9b1b`；两条 driver facts + 引擎读取 + 证据；`new_failures=0`（10 基线 loop-state + 3 镜像类） |
| T014 收口 | DONE @1da7a88d | 用户测试豁免下勾选；`dispatch-recipes.md` 的测试钉住字面量按 One Source of Truth 允许重复记录；不再运行 `test_c5` |
| implement Part 3 | DONE @98288d45 | T015-T019 `[X]`；ARC + 批 3 facts + 8 条排除行；T017-T019 读数 `waived-by-user`；无 pytest |
| implement Part 4/5 | DONE @1e4ca01e（测试豁免） | T020-T031 `[X]`；US4 排除记录、`--triple-structure` opt-in、docs/CHANGELOG、镜像投影（6 对 ok）；T021-T023/T027-T031 测试型读数 `waived-by-user`；verification.md 落盘；Feature 状态 `Blocked` |

## 最终状态（2026-11-05，用户测试豁免）

- **用户指令**：2026-11-05 明确「后续步骤略过所有的测试」。此后未运行任何 pytest/全量/定向套件/smoke/scratch-tree 证明；仅保留秒级的声明/镜像读数。测试型 SC 证据统一记 `waived-by-user`，未记 `pass`。
- **实现**：31/31 任务 `[X]`；提交链至 `1e4ca01e`；声明层 `shared/declarations/`（23 条声明 + 12 条排除行）、共享读取入口、`harness-triple-check.py`、批 1/2/3 迁移、`--triple-structure` opt-in、docs 指针页、CHANGELOG、镜像六对投影。
- **特性状态**：`Blocked`（`features.md` 与 `features/084.md`）。原因有二，**测试豁免不是唯一原因**：
  1. `verification.md`：SC-001/SC-002（final）`blocked`——测试型腿按用户指令 waived；smoke 未运行；
  2. 独立于测试：`coverage` 在最终树上仍报 **58 个 `unclassified-candidate:`**，T020 的排除名册只覆盖其中一部分；`SC-001(ii)` 的零未分类条件不成立。剩余分类/迁移没有任务行认领，需后续切片。
- **未执行**：不 push、不合并；review/closure 未跑（其证据面依赖被豁免的测试与未完成的分类）。
- **下一步（需用户裁定）**：① 为 58 个未分类候选新增一个迁移/分类切片（plan reopen），完成后再按用户允许的测试预算复跑 final 读数；② 若接受 `Blocked` 作为本切片终态，保留分支与证据，不合并；③ 若要求合并，需先决定是否放宽 SC-001/SC-002 的验收口径（不推荐，属状态机例外）。

### 分类切片结果（路径 A，2026-11-05）

- **58 → 0**：`coverage` 现报 `candidates 83 / in-scope 13 / excluded 70 / unclassified 0 / pending 0 / findings 0`，exit 0；`verify` exit 0、0 findings、锚点 0 失败、无重复 unit。处置分布：`no-harness-asset` 30 行、`no-machine-fact` 28 行；排除行总数 70（12 + 58），行未重排。
- **T032**：已加入 tasks.md 并勾 `[X]`（32/32 任务，`validate-tasks` PASS）；plan § Facts outside the roster 加了一句判决，不复制 58 行清单。
- **SC-001**：四腿（确定性、零未分类、无孤立声明、双向消费者一致性）均由秒级读数成立 → `pass`；证据 `test-evidence/t032-classification-readings-2026-11-05.txt`。
- **SC-002（final）仍 `blocked`**：残余面（复用的 `duplicate` 面）与契约模块均为测试型读数，按用户测试豁免未跑；smoke 未运行。**Feature 状态保持 `Blocked`**。
- **提交**：`94d9db33`（分类）+ `e185da6c`（镜像投影 + SC-001 pass）；未 push、未合并。
- **待用户决定**：是否现在运行 final 测试预算（SC-002 的契约模块/残余读数 + smoke），或接受 `Blocked` 终态。未获许可前不再运行任何测试。

### final 测试预算（用户授权，2026-11-05）

- 契约模块：`tests/contract/test_harness_triple_structure.py` → **68 passed**（`test-evidence/final-contract-module.txt`）。
- 残余 `duplicate` 面：`doc-consistency-check.py --action verify --faces duplicate --spec-dir …` → **pass / 0 findings**（`test-evidence/final-duplicate-face.txt`）。
- smoke：`harness-triple-check.py --action coverage` 两次 → exit 0、逐字节一致（`smoke-run1/2-2026-11-05.txt`）。
- SC-001 / SC-002 两条 final 路径均 `pass`；`verification.md` 更新；Feature 状态 `Blocked → Implemented`（提交 `03a19487`）。
- 下一步：`/speckit.review` 四段 + ARC；若通过 → `Ready for Review`；closure 全量在 review 之后由驱动执行。

### review round 1 → 修复 → round 2（2026-11-05）

- **round 1 结论**：3 P0（implement 未走 checker 翻转 / smoke 不可机读 / features 行双状态）+ 7 P1 + 6 P2；代码段 2 条 blocking（`flow-class-classes` 三个引擎内联副本；`success-criterion-path-values` 的 `final` 成员在分支处重写）；ARC `block`（`smoke_record_pass=false`）。Feature 未翻状态。
- **修复 `e0453f9e`**：smoke 记录三字段机读化（`smoke_exit_code=0`、单一路径存在、新增 `smoke_comparison`）；features 084 行单一状态；SC-004 改 70 行；`notes_feature_status=Implemented`；baseline_commit 改 `9657885f`；`pre-analyze-check.py` / `validate-requirements.py` 经声明读 `flow-class-classes`（consumers 同步）；`closure-acceptance-check.py` / `validate-requirements.py` 用 `PASS_PATH = PATH_VALUES[0]` 取代分支字面量；verification 模板加 `smoke_comparison` 槽位；DoD `green-with-void`。
- **读数**：`closure-acceptance-check` → `verdict: accept`（四条件全 true、final 2/2 pass、smoke pass）；定向测试 **219 passed / 2 baseline failures**（`test_e_a_stale_pin…`、`test_c22…`，均在 23-name 基线集内），无新增。
- **round 2**：重跑四段 + ARC；若 blocking 归零 → `Ready for Review`；closure 全量仍在 review 之后。
- **round 2 结果**：P0 全关、ARC `accept`；仍剩 1 条代码 blocking（`closure-acceptance-check.py:227` 的 `flow-class-classes` 内联副本未点名）。修复 `e1f59096`：closure 引擎经 `_declared_flow_classes()` 读取声明并把该引擎加入 consumers；`verify` 现 `31/31` + `16/16`、findings 0；`smoke_comparison` 进入 `SMOKE_FIELDS` 被解析并在 JSON 输出；`notes/quickstart-run.md` 以 `waived-by-user` 落盘；定向测试 168 passed。`closure-acceptance-check` 仍 `accept`（smoke comparison 已读）。
- **round 3**：重跑四段 + ARC；预期 blocking 0 → `Ready for Review`。
- **round 3 结果**：round 2 的 blocking 已关，但同一提交引入回归——`_declared_flow_classes()` 缺 `declaration_reader is None` 守卫，退化树 import 崩溃；`test_gate_wiring_081.py` 2 条新红。修复 `2d8576b5`：补守卫 + FR-012 兼容值 `("execution","expression")`（带标签）；该文件 22 passed；closure `accept`；关键定向集 241 passed / 2 baseline。round 4 重跑。
- **round 4**：预期 blocking 0 → `Ready for Review`；剩余 P1（head-failed.txt 待 closure 全量、REC-084-10/12 记录）不阻断翻转。
- **round 4 结果**：**GREEN @2d3b968e**。代码段 `blocking 0 / important 2 / suggestion 4`，`gate=allow`；ARC `accept`；两模块 45 passed；14 文件集 358 passed / 2 baseline failures（`test_e_a_stale_pin…`、`test_c5…`，均在基线）；Feature 状态已翻到 `Ready for Review`（`features.md` / `features/084.md` / `verification.md:134`）。round 3 的旧记录已归档为 `review-r3.md` / `code-review-20261105T163841Z.md`，未丢历史。**脊注**：round 4 attempt 1 虽在 120 回合处停止，但留下了完整的未提交产物；attempt 2 独立复测后提交，故「no work」的旧记录已按事实更正。

## closure 全量（slot 2）——RED（2026-11-06）

- **读数**：`bash scripts/bash/run-tests.sh --names-out …/final-failed.txt` → `55 failed / 7180 passed / 4 skipped / 38 errors`（331.65 s，rc 1）；证据 `test-evidence/closure-full-suite-2026-11-06.log`、`final-failed.txt`。
- **对基线（25 names）**：新增 **32** 条、修复 **2** 条（两条 mirror）。**合入门禁不通过**；未 merge、未 push。
- **五簇归因**（代表测试 → 直接原因 → 修复方向）：
  1. **probe/compile 嵌入漂移**（`test_compile_embeds`×4、`test_compile_reconcile_guards`×7、`test_compile_propagation_order`、`test_engine_face_contract`×5、`test_handler_registry`、`test_phase2_bindings`×3、`test_run_skills_wiring`、`test_coaching_wiring_contract`×3 等）：`pre-analyze-check.py` / `sdd-loop-driver/SKILL.md` 的迁移改动未重编译 probe 嵌入；`test_compiled_form_contract` 直接 `JSONDecodeError`。**修复**：运行 `probe-utils.py --action compile-embeds` 重新生成编译面并提交。
  2. **中性化守卫 C-57**：`shared/declarations/exclusions/no-machine-fact.yaml`、`shared/definitions/probe-definitions.md`、`shared/workflow/expression-gates.md`、`pre-analyze-check.py` 含 `Feature 084` / `.specify/specs/084-` 等框架运行时引用。**修复**：改写为特性中立措辞。
  3. **exec-quant 测试 setup**（38 个 ERROR 全部来自同一 setup）：`test_exec_quant_dispatch.py:41` 断言源码含字面量 `SCHEMA_VERSION = 2`，而批 3 迁移已改为声明读取。**修复**：把该测试改为读 `quant-record-schema` 声明（或断言派生值），属迁移的配套测试适配。
  4. **069 不变量的两处治理冲突**：`test_flow_class_ledger::test_no_second_classification_data_file` 把 `flow-class-ledger-columns.yaml` 判为「第二份分类数据源」；`test_expression_compatibility::test_c5_non_wiring_files_keep_their_frozen_hashes` 因 `sdd-loop-driver/SKILL.md` 等冻结文件被改动而红。**修复**：需裁定——把声明层登记为新的单一 owner（改 069 测试/记录）或回退对应迁移。
  5. **计数/基线类与字面量钉住**：`test_docs_gate_driver`（SKILL.md 的八阶段链字面量被指针化）、`test_clause_forms`、`test_confirmation_gates_sweep`、`test_fast_fail_discipline`、`test_neutrality_budget`、`test_proactive_trigger_section`、`test_token_efficiency_discipline` 等；多为新文件触发既有扫描总数或测试钉住的字面量。**修复**：恢复测试钉住的字面量（One Source of Truth 允许的「测试钉住字面量」重复）或按 owner 规则更新基线。
- **状态**：Feature 仍为 `Ready for Review`（review 已过），但 **closure/merge 门禁 RED**；线路 `stalled`，等用户决定修复切片或止步。

## 用户裁定（2026-11-05）：路径 A——分类切片

用户选择 **A**：为 58 个未分类候选新增分类/迁移切片（plan reopen），完成后再谈 final 读数。线路已从 `blocked` 恢复 active；测试豁免仍生效（不跑 pytest/全量/定向/smoke；仅允许秒级 coverage/verify）。本切片的成功判据：`harness-triple-check --action coverage` 的 `unclassified` 归零、`exclusion-anchor-unresolvable` 归零；SC-001(ii) 的覆盖条件可重新读取。

## Part 2a 异常处置（记录）

- **US1 `verify` 聚合 exit 1**：unit `shared/workflow/feedback-step.md` 自身 `state: complete`、0 条 finding 点名它；exit 1 来自批次 2/3 尚未迁移与排除层尚未落地的 80 个候选单元。US1 的独立验收按**单元级**读数成立；聚合 verify 的 0 期望留到 T027/T028 在完整层上重读，**不改引擎语义、不改任务原文**。
- **11 条 mirror-class new failures**：`.specify/` 镜像未投影，T026 拥有；closure 全量读数按「镜像类」整类解释，不得读成本段回归。

## Implement 分段计划（≤8 任务/段）

| Part | 任务 | 范围 |
|------|------|------|
| 1 | T001–T007（7） | Setup + Foundational：基线读数、声明层、共享读取入口、checker、red-first 测试模块 |
| 2 | T008–T014（7） | US1 + US2 前半（批 1 迁移 + 批 2 的 gate-shaped 集合） |
| 3 | T015–T019（5） | US2 后半（ARC + 排除记录）+ US3 |
| 4 | T020–T023（4） | US4（非 harness 流程不受影响） |
| 5 | T024–T031（8） | Polish：镜像/分发/文档/CHANGELOG、feature-level readings、verification.md、状态翻转 |

- **测试预算**：Part 1 起点一次全量基线（E2 slot=baseline），implement 内不再跑第二次全量；中间验证用 targeted-set-v1 + E3 stage-status；closure 全量在 review 之后由驱动执行。
- **非阻断残余（analyze round 3）**：F-10（`no-machine-fact.yaml` 8 条 vs T020 另写 2 条，总 10）、F-11（`history-categories` 排除锚点读数不可复现，排除本身成立）、F-12（banner 对 `0/19` 归因的措辞）、F-13（ARC 单元格 over-claim 11 vs 7）、F-14（`ARC verdict mapping` 非 kebab-case slug）。可随 implement 的对应文件触碰顺手订正，不另开 analyze 轮。

## U5 停线上送（四要素）

### 1. 发现了什么

`/speckit.analyze` round 2 判 **CRITICAL 0 / HIGH 2**，质量门未通过；按「同一门最多回环一轮」规则，回环预算已用尽，线路停在上送点。

- **R2-01（HIGH，已修复）**：tasks 修复提交 `2b18485e` 在 `.specify/memory/features/084.md:31` 的状态记录里写了 `flow_class: execution`，触发 069 既有契约测试 `tests/contract/test_expression_compatibility.py::test_c2_no_project_side_classification_store`（项目侧不得存分类数据）。已在报告后机械改词为「类别读取结果：`execution`（由 requirements 声明行解析）」并提交 `43dcf30e`；单测复跑 1 passed。该修复发生在 round 2 报告之后，报告中的 R2-01 为当时读数。
- **R2-02（HIGH，未决）**：`contracts/migration-batches.contract.md` C-044/C-045 的 **8 条 `engine side = none`** 行仍留在 in-scope，并写明「读取点在迁移时（C-047 step 3）才产生」；这与 `requirements.md` FR-006(i) 的「必须存在判决型引擎消费者」判据、FR-011 的范围，以及 `tasks.md` T015 末句「prose-only 且无消费者者留在原处、记为 out of scope」冲突。三种工件给出三种指令。

### 2. 为何吃重

- R2-02 不是措辞问题，而是**范围语义的二选一**，且两条修复路径都越过 analyze 的写权限：
  - **路径 A（plan reopen，substantive）**：把这 8 行移出 in-scope / 改判排除（`no-machine-fact` 或 `by-owner-decree`），保留「有引擎读取点」的 6 条批 2 行；需同步 tasks T015/T016 与范围表。
  - **路径 B（requirements 语义改动）**：保留 roster，把 FR-006(i) 改为「迁移后必须产生读取点」的判据，并替换 T015 末句；这会改变 A2 已收窄的判据（analyze 认为这正是 A2 移除的「自我证成」形态，风险更高）。
- 质量门规则规定第二轮 analyze 仍有 HIGH → 停线上送；不得自行开第三轮。

### 3. 已产生的中间产物逐项可定位

- **分支 / HEAD**：`084-harness-triple-structure` @ `d23490c3`（未 push）。
- **提交链**：`a94c3945` requirements → `cd446a6e` 运行时栈修复 → `171c2ff8` clarify + Feature 绑定 → `4b65517c` plan → `5dc5919a` + `8ed70a87` tasks → `9abb10fb` checklist → `6ac4c2d3` analyze round 1 证据 → `fd84ed63` requirements 回环修复 → `9284c789` plan 回环修复 → `2b18485e` tasks 回环修复 → `43dcf30e` R2-01 修复 → `d23490c3` analyze round 2 证据。
- **报告**：`test-evidence/analyze-report-2026-11-05.md`（round 1）、`analyze-report-round2-2026-11-05.md`（round 2）、`analyze-round2-targeted-run.txt`（定向集实跑：3 failed / 295 passed，其中 1 条 R2-01 已修复，2 条环境性）。
- **范围冲突证据**：`contracts/migration-batches.contract.md` C-044/C-045 的 `none` 行；`requirements.md` FR-006(i)/FR-011；`tasks.md` T015 末句。
- **确定性门**：`pre-analyze --stage requirements` pass、`pre-analyze --stage plan` pass（errors=0，advisories=82）；`validate-requirements` / `validate-tasks` / `validate-decision-tensions` ok；`decomposition --mode tasks` proceed（31/40）；`clause_extract` 五份 59 条 `md-bold-closed`；`coverage-baseline.txt` 513 names；覆盖率车道 `status=uncovered`（59 beyond baseline / 0/19 FR claimed，analyze 判非 blocking，因 `[green:]` 可选且 § Traceability 19/19）。
- **状态脊**：本文件（`.specify/state/084-harness-triple-structure.md`）。
- **Feature 记录**：`.specify/memory/features.md`（084 行，Total 77=77）、`.specify/memory/features/084.md`（Planned）。

### 4. 路径 A 执行结果（2026-11-05）

- **提交**：`ba141671`（plan reopen）+ `b1b19e93`（R2-03 机械订正）。
- **8 条事实移出**：C-044 由 14 行缩为 7 行（保留 `expression-gate-faces`、`expression-stage-operator-table`、`ARC verdict mapping`、4 条 `driver-*`）；C-045 由 8 行缩为 7 行（去 `history-categories`）。新增 § Facts outside the roster，按**单元**落 8 行 `no-machine-fact` 排除记录（2 analyze + 1 self-improvement + 5 improve）；`review-segment-sequence` 与 `history-categories` 所在单元因分别还持有 ARC / `history-manifest-schema` 的 in-scope 事实，单元保持 in-scope、各 0 条排除行（避免「既声明又排除」）。
- **T015/T016**：T015 只迁移 `ARC verdict mapping` 并写 7 条批 2 排除行；T016 去 `history-categories`、写 1 条批 3 排除行；任务总数仍 31。
- **范围表**：requirements § Initial Scope Adjudication 3 行改判 excluded、2 行保持 in-scope 并在 D2 列写明留下的那条事实；FR/SC/编号/类别/Path 未动。
- **门禁**：validate-requirements / validate-tasks / decision-tensions ok；decomposition plan+tasks proceed；pre-analyze plan pass（advisories 84）；clause_extract 59；guard pytest 16 passed；081 冻结面零 diff。

### 5. 用户裁定（2026-11-05）

用户选择 **路径 A**：把 C-044/C-045 的 8 条 `engine side=none` 行移出 in-scope / 改判排除（`no-machine-fact`），同步 tasks T015/T016 与范围表；回环预算显式重置，修复后运行 analyze round 3。R2-01 已在 `43dcf30e` 修复；R2-03/R2-04 保持非阻断。

### 5. 可选处置

1. **路径 A（推荐）**：授权一次 plan reopen（substantive），把 C-044/C-045 的 8 条 `none` 行移出 in-scope / 改判排除，同步 tasks T015/T016，然后重置回环预算并重跑 analyze。
2. **路径 B**：授权 requirements 语义改动（FR-006(i) 改为迁移后判据 + 替换 T015 末句），然后重跑 analyze；风险是 A2 的收窄被反转。
3. **带病进入 implement（不推荐）**：把 R2-02 记为本线已知风险并继续；会违反 FR-006(i) 的 in-scope 正当性，且 analyze 门未绿。
4. **缩小范围/重新切片**：把 8 条 `none` 行留到后续特性，本特性只交付有引擎读取点的批次；需重走 requirements/plan/tasks。

> 非阻断残余：R2-03（tasks banner 仍用旧 `DS/HC/SR/MB/DM` 解释 `[green:]` 未启用；前提已被 `9284c789` 证伪）建议随下一次 tasks 触碰顺手订正；R2-04（`2b18485e` message 把 `DM` 写成 `DN`）为 message-only，不改写历史。框架观察：`pre-analyze-check.py` 的 `CLAUSE_DEF` 只认 2–4 字母前缀，规范 `C-001` 抽不到；`audit-test-budget.py` 不读 `stage-status.md` 的 E3 行（全线一致 `stages=6 complete=0`）。

## Analyze 回环（round 1 → 修复 → round 2，最多一轮）

- **判据**：quality-gate 规则——analyze 的 CRITICAL/HIGH 必须回上游修复后重过该门；同一门最多回环一轮，第二轮仍有 CRITICAL/HIGH 则停线上送。
- **F-01（CRITICAL，requirements）**：「既有门禁脚本」封闭集四处、三种成员。修复：在 requirements 内发布一次 owner 枚举，FR-019 / N5 / SC-006 / SC-006 Source 只引用；区分「不得重判 / 不得改动」侧与「零新增失败 / 零测试文件 diff」侧。
- **F-02（HIGH，plan）**：五份契约条款 ID `DS/HC/SR/MB/DM` 不可被 `clause_extract.py` 解析。修复：重编号为 `C-001…C-059` 并同步全部引用；属 substantive plan 变更，由驱动显式重开 plan 修复（PLAN CONSTRAINT 的显式 reopen）。
- **F-03（HIGH，requirements）**：FR-009 / SC-005 / SC-006 的「基线」无指称。修复：在每条断言内点名参照物（T001 采集 → `notes/pre-change-measurements.md`；plan EP-003 的 `171c2ff8`），不在判据内重新推导基线。
- **顺手收口（MEDIUM/LOW）**：F-04 / F-06 / C-02 / C-03 / C-04 / C-05 / C-06 / F-08（requirements）；F-07 / C-01（plan）；F-05 / E-01 / F-09（tasks）；G-01（feature detail）。
- **回环预算**：requirements → plan → tasks 各一次有界修复，然后 analyze round 2；不再开第二轮回环。
- **requirements 修复结果（2026-11-05）**：`fd84ed63`；F-01 / F-03 / F-06 / F-04 / C-02 / C-03 / C-04 / C-05 / C-06 / F-08 全处置；`validate-requirements` exit 0（282 行）；`decomposition --mode plan` proceed；`pre-analyze --stage requirements` 仍有 5 条 `dangling-id: FR-023`（F-05，tasks-owned，待 tasks 修复后复跑）。
- **plan 修复结果（2026-11-05）**：`9284c789`；五份契约 59 条款 → `C-001…C-059`，`clause_extract` 五份全 `md-bold-closed`、合计 59；规范性文件旧 ID 零残留；F-07 读数订正（38 / 35 / 39 三读数 + 逐字五名）、C-01 批 2/3 engine side 补列；`validate-requirements` / `validate-decision-tensions` / `decomposition` 全绿；`pre-analyze --stage plan` 仍只剩 F-05 的 5 条 FR-023。
- **待 analyze round 2 裁决的新增风险（plan 修复披露）**：批 2 的 14 条事实中有 6 条今天在 `.py`/`.sh` 无引擎侧副本（`analyze-severity-values`、analysis finding-channel 集、`review-segment-sequence`、`self-improvement-stage-sequence`、track-to-executor mapping、`improvement-track-values` / changed-asset-category mapping），已按授权写 `none` 并给理由；需判定这些行是「迁移期才产生读取点」还是「不应 in-scope」。另：`pre-analyze-check.py` 的 `CLAUSE_DEF` 只认 2–4 字母前缀，规范 `C-001` 抽不到（框架侧覆盖缺口，未改）。
- **tasks 修复结果（2026-11-05）**：`2b18485e`；F-05（FR-023 → FR-011/FR-018，tasks + checklist 零残留）、E-01（`coverage-baseline.txt` 冻结：513 names / 248 files / base-sha 9284c789）、F-09（T005/T006 加 FR-008）、G-01（features/084 阶段记录 + checklist 路径 + `§ MB-01` → `C-042`）；`pre-analyze requirements` pass、`pre-analyze plan` pass、`validate-tasks` PASS、`decomposition tasks` proceed。
- **analyze round 2 的剩余读数**：`account-clause-coverage` 仍为 `status=uncovered`（59 条本特性条款超出基线、`0/19 FRs cited from citation groups`），原因是 tasks 未使用可选的 `[green:]` 归因标签；需裁决这是否构成 blocking。`pre-analyze` 的 `summary.clauses=0` 是 `CLAUSE_DEF` 前缀识别缺口，非本特性契约不可解析。

## U5 重试记录（requirements）

- **发现**：SDD Requirements Executor 在 40 回合上限处停止，未返回 `REQUIREMENTS-DONE`；仅创建 spec 目录、分支与模板骨架。
- **根因归类**：子代理能力/预算——该 agent 定义 `maxTurns: 40`，本次跨切面需求的阅读面超出预算。
- **处置**：按 U5 重试（attempt 2），改用 `SDD Executor`（`maxTurns: 120`）；提示词收紧为「先写作后探索」并附研究摘要；不修改 agent 定义（避免与 084 无关的框架源变更）。
- **保留证据**：分支名、spec 目录、模板文件均在；无中间提交需要回退。

### plan（attempt 1 → attempt 2）

- **发现**：SDD Executor 在 120 回合上限处停止，未返回 `PLAN-DONE`；全部 plan 产物已写盘并 `git add`，但未提交、未记账。
- **根因归类**：子代理能力/预算——plan 的阅读面（requirements + 宪法 + 模板 + 研究）与写作面（5 契约 + 5 设计文档）超出 120 回合。
- **处置**：attempt 2 为**有界补完**（不重写设计）：核对 staged 清单、复跑三门、提交、Wrap-up、哨兵。未修改 agent 定义。
- **保留证据**：staged 产物、`test-evidence/plan-readings.txt`、驱动者独立门禁读数；attempt 1 的 token/耗时无来源，如实记 `not_evaluated`。

## Wrap-up 记账

（待各阶段 U4 回填）

- **clarify**：Run Determination → `.specify/memory/session/20261105T080146Z-run-determination-speckit-clarify-r20261105t074027z-084a.md`；Exec Quant → `.specify/memory/exec-quant/records/20261105T080159336037Z-7f8a3419.json`；Feedback → `.specify/memory/feedback/20261105T080203Z-speckit-clarify.md`（带 feature/feature_id；`count_since_submission=246`，`should_prompt=true`，非阻断）。
- **plan（attempt 2）**：Run Determination → `.specify/memory/session/20261105T082004Z-run-determination-speckit-plan-r20261105t074027z-084a.md`（带 feature/feature_id；elapsed `not_comparable`，artifact_correctness `not_evaluated/no_baseline`）；Exec Quant → `.specify/memory/exec-quant/records/20261105T082009374970Z-a1347a99.json`（引擎无 feature 参数）；Feedback → `.specify/memory/feedback/20261105T082017Z-speckit-plan.md`（带 feature/feature_id；`count_since_submission=247`，`should_prompt=true`，非阻断）。
- **tasks**：Run Determination → `.specify/memory/session/20261105T083523Z-run-determination-speckit-tasks-r20261105t074027z-084a.md`；Exec Quant → `.specify/memory/exec-quant/records/20261105T083525969720Z-0c4b8437.json`；Feedback → `.specify/memory/feedback/20261105T083530Z-speckit-tasks.md`（带 feature/feature_id；`count_since_submission=248`，`should_prompt=true`，非阻断）。
- **checklist**：Run Determination → `.specify/memory/session/20261105T084306Z-run-determination-speckit-checklist-r20261105t074027z-084a.md`；Exec Quant → `.specify/memory/exec-quant/records/20261105T084309278446Z-6ee2f63f.json`；Feedback → `.specify/memory/feedback/20261105T084312Z-speckit-checklist.md`（带 feature/feature_id；`count_since_submission=249`，`should_prompt=true`，非阻断）。
- **analyze（round 3）**：Run Determination → `.specify/memory/session/20261105T111722Z-run-determination-speckit-analyze-r20261105t074027z-084a-r3.md`；Exec Quant → `.specify/memory/exec-quant/records/20261105T111724911488Z-17c66632.json`；Feedback → `.specify/memory/feedback/20261105T111730Z-speckit-analyze.md`（带 feature/feature_id；`count_since_submission=253`，`should_prompt=true`，非阻断）。
- **analyze（round 1）**：Run Determination → `.specify/memory/session/20261105T085413Z-run-determination-speckit-analyze-r20261105t074027z-084a.md`；Exec Quant → `.specify/memory/exec-quant/records/20261105T085419852858Z-eb6daa1e.json`；Feedback → `.specify/memory/feedback/20261105T085423Z-speckit-analyze.md`（带 feature/feature_id；`count_since_submission=250`，`should_prompt=true`，非阻断）。
- **requirements（attempt 2）**：Run Determination → `.specify/memory/session/20261105T075127Z-run-determination-speckit-requirements-r20261105t074027z-084.md`（四量均 `not_evaluated`，findings=4，clean=false——session 文件未由编排者提供，token/耗时无来源，如实记 `source_unavailable`）；Exec Quant → `.specify/memory/exec-quant/records/20261105T075132768628Z-cf37e921.json`；Feedback Record → `.specify/memory/feedback/20261105T075137Z-speckit-requirements.md`（`count_since_submission=245`，`should_prompt=true`，非阻断提示，零自动传输）；Threshold Notice：已提示，未处置；Token Reflection 与 Docs Sync Eval 结论见本阶段回传正文。三者均未纳入本阶段提交（记忆层记录，非特性产物），由驱动按需处置。

## U4 独立校验记录

### requirements（PASS，2026-11-05 07:53 UTC）

- **哨兵**：回传最后一行 `REQUIREMENTS-DONE`。
- **产物**：`requirements.md`（19 FR / 6 SC / 14 STR，含强制 § Runtime Stack & Dependency Ownership 三行：RS-001 CPython signed-contract / RS-002 pytest signed-contract / RS-003 `specify init` in-scope）、`checklists/requirements.md`、`test-evidence/` 三件；提交 `a94c3945` + 驱动者修复 `cd446a6e`。
- **纪律**：未 push；只提交本特性产物；运行时记录（session / feedback / exec-quant）与状态脊未提交；无脏文件还原。
- **记账**：session / feedback / exec-quant 三件存在；feedback 条目已补 `feature: 084-harness-triple-structure` / `feature_id: 084`（驱动者纠正，原条目缺该两字段）。
- **确定性门**：`decomposition-check --mode plan` → `proceed`（fr_count=19 ≤ 30）；`pre-analyze-check --stage requirements` 首次 exit 2（缺强制运行时栈节），驱动者补节后复跑 `decision=pass`（errors=0，advisories=12 全为未创建的计划交付路径）。
- **结论**：PASS；下一阶段 = clarify。

### clarify（PASS，2026-11-05 08:03 UTC）

- **哨兵**：回传最后一行 `CLARIFY-DONE`；回传披露 4 条（A8 拆分、features.md 既有孤行、run-determination 参数疏漏、081a session 记录被 engine settle），均非阻塞。
- **产物**：`requirements.md`（A1–A10 写回；A8 拆为 A8(a) Path in-scope / A8(b) 标签集不迁；FR-006 (i) 收窄；FR-018 增补 acceptance-hardening；SC-006 纳入 closure 脚本；新增 N7）、`checklists/requirements.md`、`features.md`（084 行 + Total 77）、`features/084.md`（Draft）、`features/081.md`（反向指针）、`test-evidence/` 五件；提交 `171c2ff8`（10 文件 / +313 −25）。
- **纪律**：未 push；只提交本特性产物；既有脏行（features.md 孤立 `|`）未改动；运行时记录未提交。
- **记账**：session / feedback / exec-quant 三件存在，feedback 带 `feature: 084-harness-triple-structure` / `feature_id: 084`。
- **确定性门**：`overlap-check` → `decision=clear`（checked=1，overlaps=0）；`pre-analyze --stage requirements` → `pass`（errors=0，15 advisories 全为计划路径）；`validate-requirements` → `ok`（282 行、25 定义行、14 STR）；`flow-class lookup` → `execution / source=declaration`。
- **A8 复核**：拆分结论有仓内证据（三处 Path 实体 + 被测试钉住的标签集 + 081 测试断言），且以 N7 记录不迁理由，不违反「一个候选单元恰一条处置记录」；接受。
- **结论**：PASS；下一阶段 = plan。

### plan（PASS，2026-11-05 08:22 UTC）

- **哨兵**：回传最后一行 `PLAN-DONE`（attempt 2 有界补完；attempt 1 在 120 回合处无哨兵，已按 U5 记录）。
- **产物**：`plan.md`（427 行：18/18 Constitution Check、4 条 Decision Tensions、Execution Premises EP-001…EP-007、Inherited Blockers、D1–D13、Mirror Obligations、Document Structure）、`data-model.md`（E-1…E-10 + 6 组夹具）、`contracts/`×5（59 条款）、`quickstart.md`（S1…S8）、`research.md`（R1–R10）、`feature-ref.md`；Feature 状态 Draft → Planned；提交 `4b65517c`（17 文件 / +1509 −5）。
- **纪律**：未 push；`requirements.md` 相对 `171c2ff8` 零改动（`git diff` 为空，无 PLAN-EDIT）；只提交本特性产物与注册表状态行；既有脏文件未动；scratch 已清理。
- **记账**：session / feedback / exec-quant 三件存在；run-determination 与 feedback 带 feature 084；exec-quant 引擎无 feature 参数（闭域仅 unit-id/run-id），按引擎能力如实记录，feature 归属由前两者承载。
- **确定性门**：pre-analyze plan `pass`（errors=0，advisories=51 全为交付前路径）；decomposition plan `proceed`（fr_count=19 ≤ 30）；validate-decision-tensions `ok`（6/6，4 records）；validate-requirements `ok`。
- **约束激活**：`plan_constraint=active`，`plan_commit=4b65517c`，`approved_baseline_commit=4b65517c`；下游 tasks/checklist/analyze/implement/review 携带只小修块。
- **结论**：PASS；下一阶段 = tasks。

### tasks（PASS with disclosed anomalies，2026-11-05 08:38 UTC）

- **哨兵**：回传最后一行 `TASKS-DONE`；同时携带 2 条 `ANOMALY:`（见下）。
- **产物**：`tasks.md`（252 行，31 任务全 `[ ]`；四故事 + Setup/Foundational/Polish；31 行 Traceability；DoD 8 行；Completion Gate 7 行；Tests Mode ON 并引用原则 IV）；`test-evidence/` 三件；提交 `5dc5919a` + `8ed70a87`。
- **纪律**：未 push；plan-owned 产物相对 `4b65517c` 零 diff（`git diff` 为空）；未勾选任何任务；既有脏文件未动。
- **记账**：session / feedback / exec-quant 三件存在；feedback 带 feature 084；exec-quant 按引擎闭域记录。
- **确定性门**：`validate-tasks` PASS（0 error / 0 warning）；`decomposition --mode tasks` → `proceed`（fr 19 ≤ 30，task 31 ≤ 40）。
- **`[green:]` 判读**：tasks 模板明写该标签为 optional；未启用不构成 tasks 阶段门禁缺口。但契约条款不可被 `clause_extract.py` 解析是 plan-owned 事实，转入 analyze 裁决。
- **结论**：PASS；异常不伪完成，交由 analyze 裁决（见下节）。

### checklist（PASS with disclosed anomalies，2026-11-05 08:43 UTC）

- **哨兵**：回传最后一行 `CHECKLIST-DONE`；同时携带 3 条 `ANOMALY:`（FR-023 越界引用、Shared Strings 占位符自述矛盾、既有门禁脚本四种口径）。
- **产物**：`checklists/layer-criteria-2026-11-05.md`（38 条，八组；100% 可追溯；未覆盖 requirements 阶段清单）；`test-evidence/checklist-self-check.txt`（268 行自检，可重跑）、`flow-class-lookup-checklist.txt`、`stage-status.md`；提交 `9abb10fb`（4 文件 / +405）。
- **纪律**：未 push；requirements / tasks / plan-owned 相对 `8ed70a87` 零 diff；既有清单未覆盖；无 PLAN-EDIT。
- **记账**：session / feedback / exec-quant 三件存在；feedback 带 feature 084；exec-quant 按引擎闭域。
- **方法学**：执行拓扑无子代理派发能力，缺口发现按 objective-analysis-gate 规则 7 走单上下文受限直读并在清单 Note 明示；建议 analyze 复核未命中缺口。
- **结论**：PASS；3 条异常交 analyze 裁决。

## 待 analyze 裁决的异常（tasks + checklist 阶段披露）

1. **契约条款 ID 方案与条款语法不兼容**：五份契约使用 `DS-01` / `HC-…` / `SR-…` / `MB-…` / `DM-…` 编号，而条款语法 owner `scripts/python/clause_extract.py` 只识别 `C-\d+`；驱动者独立复跑五份均得 `form=md-none, clauses=0`（与 081 的 `C-001` 形态不同）。tasks 阶段未启用可选 `[green:]` 归因面，改把条款分区落在 `tasks.md` § Traceability。**待裁决**：是否要求 plan 把五份契约改为 `C-\d+` 并同步 plan/tasks 引用（substantive，受 PLAN CONSTRAINT 约束）。
2. **MB-03 / MB-04 引擎侧路径精度不足**：`migration-batches.contract.md` 的批 2/3 只给 fact slug 与 carrier 侧（部分给引擎侧），不像 MB-01 有逐行 `engine side` 列；T014–T016 因此要求实施者用可执行 `grep` 现场定位并记录订正。**待裁决**：是否回填引擎侧列（plan-owned substantive）或接受实施期定位。
3. **`tasks.md` 引用 `FR-023`（2 处）但 `requirements.md` 只定义 `FR-001..FR-019`**：是规格缺一组需求，还是任务引用越界？需在「改任务」与「改需求」之间裁定（checklist CHK037）。
4. **`requirements.md` § Shared Strings 占位符自述矛盾**：原文称「一条无占位符（`STR-013` 只有一个 `<unit>`）」，实测六条原因模板每条都带占位符（四条一个、`STR-011` 两个、`STR-013` 一个）；SC-003 要求逐字判定，该 owner 文本需修订（checklist CHK011）。
5. **「既有门禁脚本」封闭集在 `requirements.md` 内四种口径**：FR-010 列五个（含 `doc-consistency-check.py`，正文却写「四个面」）、FR-019 写「四个」、N5 列四个、SC-006 列五个（含 `closure-acceptance-check.py`）、SC-006 Source 又写「四个」。修平属需求正文 substantive 改动（checklist CHK021）。

## 类别观测与 re-baseline

- requirements 派发载荷：`flow_class=null; source=default; marker=; error=owner-unavailable`（解析时 spec 输入缺失，符合 class-resolution C-003）。
- requirements U4 当场解析：`flow_class=execution; flow_type=-; source=declaration; marker=null; error=null`。
- 处置：这是「输入缺失 → 声明已写入」的预期迁移，不是类别翻转；记录为 re-baseline 观测，clarify 起载荷使用 `flow_class=execution; source=declaration; marker=; error=-`。

## 驱动者纠正记录

1. **补写 § Runtime Stack & Dependency Ownership**：`pre-analyze-check --stage requirements` exit 2 的直接原因；三行内容由本特性 FR（FR-009/FR-013/FR-016/FR-019）与仓内事实（`pyproject.toml`、`scripts/bash/run-tests.sh`、`src/specify_cli/__init__.py`、实测版本）导出；修复提交 `cd446a6e`。
2. **刷新证据**：`validate-requirements.txt` 重跑为 250 行；checklist 计数同步 240→250；stage-status 补记驱动者 U4 复跑。
3. **补 feedback feature 字段**：`20261105T075137Z-speckit-requirements.md` 增补 `feature` / `feature_id`，满足 U4 记账条件。

## 框架观察

1. **现象**：`shared/workflow/expression-gates.md` § 阶段算子表把 `pre-analyze-check.py` 写成 `scripts/python/` 路径，但实际位于 `skills/external/sdd-loop-driver/scripts/`（子代理在 requirements 阶段发现）。**框架位置**：`shared/workflow/expression-gates.md` 的引擎路径引用。**对驱动的影响**：若按 owner 文档路径调用会得到文件不存在；本次按真实路径运行。建议后续在 owner 文档修正并加路径解析守卫。
2. **现象**：`SDD Requirements Executor` 的 `maxTurns: 40` 对跨切面需求不足，首次派发仅完成模板骨架即耗尽。**框架位置**：`.qoder/agents/sdd-requirements-executor.agent.md`（与 `agents/sdd-executor.agent.md` 的 120 预算不一致）。**对驱动的影响**：浪费一次派发并触发 U5 重试；建议统一 requirements 执行器的预算或按阶段动态设定。
3. **现象**：requirements 阶段未自动运行 `pre-analyze-check` 与 `decomposition-check`，而驱动 U4 必须运行；子代理在 stage-status 中把两者登记为「未运行」。**框架位置**：`templates/commands/requirements.md` 的确定性门接线。**对驱动的影响**：门禁缺口靠驱动 U4 兜底；若驱动省略则漏检（本次即抓出缺失的运行时栈节）。
4. **现象**：clarify 阶段调用 run-determination 时，把既有 tracked 记录 `session/20261102T231648Z-run-determination-speckit-clarify-r20261102t225758z-081a.md` 的 satisfaction 轴 settle 了（文件现为 modified 未提交）。**框架位置**：`scripts/python/run-determination.py` 的跨记录 settle 行为。**对驱动的影响**：运行记录写入面外溢到上一特性的记录；U6 归档时须按运行记录处置，且下一轮需确认是否应禁止跨 run_id 的 settle。
5. **现象**：clarify 的 `overlap-check` 输出 `note: current feature has no declaration artifact`——本特性尚未实现声明层，检查器如实降级为 clear。**框架位置**：`overlap-check.py` 的输入面。**对驱动的影响**：在声明层落地后的复跑（plan/tasks/implement）才具备完整重叠判定能力，不能把本次 clear 读作终态。
6. **现象**：plan 阶段 `exec-quant.py --action collect` 的参数域不含 `--feature` / `--feature-id`，与派发简报要求的记账参数不一致。**框架位置**：`scripts/python/exec-quant.py` 的 `args-manifest` 闭域（`required=[--unit-id]`、`source=[--run-id]`）。**对驱动的影响**：feature 归属只能由 run-determination 与 feedback 承载；驱动的记账核验须按引擎真实参数域判定，不能把缺 feature 记成记账缺口。
7. **现象**：plan 产出的五份契约使用 `DS/HC/SR/MB/DM` 前缀条款 ID，`clause_extract.py` 只识别 `C-\d+`，五份均 `form=md-none, clauses=0`。**框架位置**：plan 模板的契约条款编号约定与 `scripts/python/clause_extract.py` 的语法 owner 未显式钉住前缀集合。**对驱动的影响**：可选 `[green:]` 归因面失效；tasks 阶段改用 § Traceability，需 analyze 裁决是否回改 plan。
8. **现象**：plan 的 `migration-batches.contract.md` 批 2/3 未给逐行引擎侧路径，MB-01 有、MB-03/04 无。**框架位置**：plan 的迁移契约完整性。**对驱动的影响**：tasks 只能要求实施期 `grep` 定位，增加实现不确定性；需 analyze 裁决是否回填。
9. **现象**：checklist 阶段在无子代理派发能力的拓扑下按 `objective-analysis-gate.md` 规则 7 降级为单上下文直读，缺口发现不构成覆盖性主张。**框架位置**：`shared/workflow/objective-analysis-gate.md` 与本地拓扑的兼容面。**对驱动的影响**：分析类阶段的质量上限受宿主能力约束；analyze 应复核 checklist 的未命中缺口。
