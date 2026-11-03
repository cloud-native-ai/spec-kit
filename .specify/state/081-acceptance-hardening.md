# Line State — 081-acceptance-hardening

<!-- loop-state:begin -->
spine_state: running
run_id: r20261103T043000Z-081b
slice: 081b
stage: implement
stage_started_at: 1793684686
stage_deadline_epoch: 1793690086
stage_base_commit: 8a4e7c7c
attempt: 3
retry_limit: 2
last_verdict: implement 081b part 3/3 HALTED @8a4e7c7c (T011 smoke 0/0; T010 checker exits 2 on annotated Contract/Source row cells; T012 blocked by T010; third defect: declared_dependency_files scans arbitrary backticks and makes 081 its own dependency); repair dispatched
<!-- plan-fence: decomposition=auto@plan-entry; test-budget=baseline@implement-start + closure@post-review; fast-lane=not-adopted -->
<!-- loop-state:end -->

<!-- test-budget:begin -->
{"seq": 1, "slot": "baseline", "stage": "implement", "purpose": "081b implement-start baseline (pre-081b tree; 081a final run)", "trigger": "081b implement start", "at": "2026-11-03T04:30Z", "command": "bash scripts/bash/run-tests.sh --names-out .specify/specs/081-acceptance-hardening/baseline-failed.txt -q", "selection_basis": "full-suite", "rc": 1, "passed": 7025, "failed": 39, "skipped": 7, "failed_names_path": ".specify/specs/081-acceptance-hardening/baseline-failed.txt", "evidence_ptr": ".specify/specs/081-acceptance-hardening/test-evidence/closure-final-run.txt"}
<!-- test-budget:end -->

- line_id: `081-acceptance-hardening`
- run_id: `r20261102T225758Z-081a`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，主工作区；feature branch 由 requirements 阶段创建）`
- base_sha: `cb841d90`
- trunk: `master`
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`）
- **执行拓扑**：本地（宿主原生子代理）
- **终态权威文档**：用户本轮需求（更严格验收：Phase 1–4；`Implemented` 增加基本 smoke test；`review` 增加对实现与各阶段产物本身的审查）+ 目标仓 `.specify/memory/constitution.md` + `.specify/instructions.md` + 现有 `templates/`、`shared/`、`skills/`、`scripts/`
- **特性切片**：Feature 081「Stricter Acceptance & Artifact Review」，按四个用户故事组织：
  - **US1（P1）** 验收状态机与 closure gate：final-path SC、`Blocked` 状态、Implemented 基本 smoke test、closure-acceptance-check
  - **US2（P1）** 运行时栈/依赖所有权 + 执行前提/继承 blocker + pre-analyze
  - **US3（P1）** review 实现与产物质量审查 + driver 合并门
  - **US4（P2）** 词表/注册表/迁移审计/文档/副本同步
  - 若 plan 入口 decomposition-check 判 `split-required`，按 081a–081d 切片后逐片重走 requirements。
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链
- **拆解开关**：`decomposition=auto`
- **测试预算**：implement 起点一次全量基线、review 后 closure；中间定向集
- **类别四元组**：`flow_class=execution`；`source=default`；`marker=未声明·按默认`；`error=-`

## U1 断点探测（2026-11-02 22:58 UTC）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `master` |
| 工作树 | 干净（`git status --porcelain` 无输出） |
| 最近提交 | `cb841d90`（080 post-fix full-suite comparison） |
| spec 目录 | 最高 `080-humanize-run-output`；无 081 / acceptance / closure 相关 spec |
| Feature 注册表 | 无 081；026 的零 pass 结项是本次改进的直接证据 |
| 治理 | constitution v1.15.0；instructions 含 Two Hats / One Source / Fast Fail / Token Efficiency / Directory Governance |
| 结论 | **断点 = requirements**；新建 Feature 081 |

## 阶段记录

| 阶段 | 状态 | 证据 |
|------|------|------|
| requirements | done（U4 PASS，2026-11-02 23:08 UTC） | `11289d54` + `d400a1e6`；validate-requirements ok（0 error/0 warning）；decomposition proceed（25/30）；pre-analyze pass（2 条 expected advisories，已在证据中处置）；wrap-up 见下 |

## Wrap-up 记账（requirements）

- run-determination: `.specify/memory/session/20261102T230741Z-run-determination-speckit-requirements-r20261102t225758z-081.md`
- feedback: `.specify/memory/feedback/20261102T230745Z-speckit-requirements.md`
- exec-quant: `.specify/memory/exec-quant/records/20261102T230745070375Z-da352ef1.json`
- 说明：子代理未在回传中执行 Wrap-up；驱动者在 U4 补跑三步（符合 stage-prompts § Independent Verification 的 `WRAPUP-DEFERRED` 补跑规则），并将指针写回本节。

## U4 独立校验记录（requirements）

- 哨兵：`REQUIREMENTS-DONE`（回传最后一行）
- 产物：`requirements.md`（25 FR / 9 SC / 17 STR，2 条 final-path SC）、`checklists/requirements.md`、`test-evidence/` 四项
- 提交：`11289d54`（阶段产物）+ `d400a1e6`（驱动者纠正 pre-analyze 证据：终树扫描为 2 条 advisory，非 0；advisory 指向 plan 阶段才创建的 `shared/workflow/acceptance-hardening.md`）
- 纪律：未 push；`master` 仍在 `cb841d90`；未提交 `.specify/state` / `.specify/.tmp` / 运行时记录
- 独立复跑：validate-requirements ok；decomposition `proceed`（fr_count=25）；pre-analyze `pass`（errors=0，advisories=2）
- 结论：PASS，下一阶段 = clarify

## 阶段记录（续）

| 阶段 | 状态 | 证据 |
|------|------|------|
| clarify | done（U4 PASS，2026-11-02 23:16 UTC） | `0c79e9c7`；Feature 081 绑定（`features.md` 76=76、详情 Draft）；A1–A13 处置；runtime stack 3 `signed-contract` + 1 `in-scope`；review 组合四段 + ARC；validator ok；overlap clear |

## Wrap-up 记账（clarify）

- run-determination: `.specify/memory/session/20261102T231641Z-run-determination-speckit-clarify-r20261102t225758z-081.md`（驱动者补跑）
- feedback: `.specify/memory/feedback/20261102T231649Z-speckit-clarify.md`
- exec-quant: `.specify/memory/exec-quant/records/20261102T231649041217Z-bf63d603.json`

## U4 独立校验记录（clarify）

- 哨兵：`CLARIFY-DONE`
- 产物：`requirements.md`（268 行；FR 25 / SC 9 / STR 17 不变）、`features.md`（081 行 + Total 76=76）、`features/081.md`（Draft）、`test-evidence/clarify-*`
- 提交：`0c79e9c7`（仅 clarify 产物；未 push；`master` 仍在 `cb841d90`）
- 独立复跑：validate-requirements `status: ok`；overlap-check `decision=clear`
- 关键裁决：A3 review 四段 + ARC（owner 文本改写归 plan/implement）；A4 `Path` 行内且为最后 token；A6 线状态 7→8 + 八项处置；A11 本仓不可核验 026，只以内联重述为准；A12 不新增第三套严重度，方法论载体由 plan 定；A13 plan 两表与 tasks 环境前提不叠位
- 结论：PASS，下一阶段 = plan

## 阶段记录（plan）

| 阶段 | 状态 | 证据 |
|------|------|------|
| plan | done（U4 PASS，driver completion；子代理 120-turn limit） | `ea058fae`；plan.md（18/18 Constitution、D1–D10、T-001..T-005）、data-model.md、5 contracts、quickstart.md、research.md、feature-ref.md；pre-analyze pass（65 planned-path advisories）；decision-tensions 6/6；两份 `--check` exit 0；baseline 39F/6970P/7S |

## Wrap-up 记账（plan）

- run-determination: `.specify/memory/session/20261102T234037Z-run-determination-speckit-plan-r20261102t225758z-081.md`（驱动者补跑）
- feedback: `.specify/memory/feedback/20261102T234040Z-speckit-plan.md`
- exec-quant: `.specify/memory/exec-quant/records/20261102T234040081493Z-d2bf1bce.json`

## U4 独立校验记录（plan）

- 哨兵：子代理在 120-turn limit 处停止，**未返回 `PLAN-DONE`**；按部分产物 + 驱动者补完处置（显式异常，不冒充子代理完成）
- 产物：plan.md、data-model.md、contracts/（5 份）、quickstart.md、research.md、feature-ref.md、`baseline-failed.txt`、test-evidence 五项
- 提交：`ea058fae`（仅 plan 产物；未 push；`master` 仍在 `cb841d90`）
- 驱动者补完：实跑全量基线 `39 failed / 6970 passed / 7 skipped in 596.80s`，把 EP-009 证据从“空文件 + 未落日志”纠正为真实结果；追加最终树 gate 证据；提交 plan 集
- 独立复跑：validate-requirements ok；validate-decision-tensions 6/6；pre-analyze plan pass（65 advisories，全部为 plan 阶段计划交付物）；regen/sync `--check` exit 0
- 关键设计：D5 载体 = 新内部技能 `review-feature-quality`（产物段 + 实现段）；D8 runner = `.venv` 修复后 pytest 9.2.0 / CPython 3.14.6；D10 = 自然任务 ≈52 > 40 → 081a–081d 切片
- 结论：plan PASS（带子代理 turn-limit 异常披露）；下一阶段 = tasks（仅 081a）

## 阶段记录（tasks）

| 阶段 | 状态 | 证据 |
|------|------|------|
| tasks | done（U4 PASS，2026-11-02 23:46 UTC） | `00d3ab3f` + `05024cb2`（GATE-6 自纠）+ `3cf66d68`（GW-15 状态校正）；tasks.md 20 任务（081a）；decomposition `proceed` 20/40；pre-analyze pass（81 planned-path advisories）；validate-tasks 0/0 |

## Wrap-up 记账（tasks）

- run-determination: `.specify/memory/session/20261102T234434Z-run-determination-speckit-tasks-r20261102t225758z-081a.md`（子代理已执行）
- feedback: `.specify/memory/feedback/20261102T234441Z-speckit-tasks.md`
- exec-quant: `.specify/memory/exec-quant/records/20261102T234438301426Z-b85fa0e2.json`

## U4 独立校验记录（tasks）

- 哨兵：`TASKS-DONE`
- 产物：`tasks.md`（20 任务；`## Slice Boundary` 明写“081a 后特性是 `Blocked`，不是 `Implemented`”）、4 份 tasks 证据
- 提交：`00d3ab3f`（tasks）、`05024cb2`（GATE-6 自纠：T020 播种后 checker 应 exit 1 而非 exit 2）、`3cf66d68`（驱动者校正 GW-15：Feature 081 `Draft → Planned`）
- 纪律：未 push；只提交 tasks 产物；`master` 仍在 `cb841d90`
- 独立复跑：decomposition `proceed`（task_count=20 ≤40）；pre-analyze `pass`（81 advisories，全部为 planned paths）；registry 76=76；`test_registry_completeness.py` 3 passed
- 子代理异常：GW-15（plan 阶段应把 Feature 081 从 Draft 升 Planned）未落；驱动者在 tasks U4 捕获并以 `3cf66d68` 校正，未静默放过
- 结论：PASS，下一阶段 = checklist

## 阶段记录（checklist）

| 阶段 | 状态 | 证据 |
|------|------|------|
| checklist | done（U4 PASS，2026-11-02 23:52 UTC） | `f83fb4ba` + `67054707`；`checklists/acceptance-2026-11-03.md` 39 项 = 28 PASS / 11 FAIL；`test-evidence/checklist-probes.txt` P1–P11 |

## Wrap-up 记账（checklist）

- run-determination: `.specify/memory/session/20261102T235210Z-run-determination-speckit-checklist-r20261102t225758z-081a.md`（驱动者补跑）
- feedback: `.specify/memory/feedback/20261102T235215Z-speckit-checklist.md`
- exec-quant: `.specify/memory/exec-quant/records/20261102T235210695451Z-7d99aa32.json`

## U4 独立校验记录（checklist）

- 哨兵：`CHECKLIST-DONE`
- 产物：`checklists/acceptance-2026-11-03.md`（39 项，逐项 PASS/FAIL + path:line）、`test-evidence/checklist-probes.txt`（11 条只读探针）
- 提交：`f83fb4ba` + `67054707`（仅 checklist 产物；未 push；`master` 仍在 `cb841d90`）
- 结论：checklist 为质量信号，11 FAIL 交下一步处置；按“明确缺口先修复复跑、残余交 analyze”的策略，先派 checklist-fix 修 8 项明确缺口（CHK004/005/008/024/025/027/035/036），CHK012/017/021 三项语义未决留 analyze 裁决
- 子代理披露：同作者检测降级（无 subagent 工具），rows 已标 `Detection disclosure`；未把未评估写成 0

## 阶段记录（checklist-fix）

| 阶段 | 状态 | 证据 |
|------|------|------|
| checklist-fix | done（spec-only，2026-11-03 00:01 UTC） | `f8f481ec`；8 项 CHK 修复（004/005/008/024/025/027/035/036）+ 4 项 fast-fail 纠正；CHK012/017/021 留 analyze；tasks 20→21；validator ok；pre-analyze tasks pass 0/0 |

## U4 独立校验记录（checklist-fix）

- 哨兵：`CHECKLIST-FIX-DONE`
- 产物：`requirements.md`（270 行；FR 25/SC 9/STR 17 不变）、`plan.md`、`tasks.md`（21 任务）、`contracts/**`、`data-model.md`、`test-evidence/checklist-fix-report.md`
- 提交：`f8f481ec`（9 文件；未 push；`master` 仍在 `cb841d90`）
- 关键修复：CHK025 七原因唯一拼写；CHK005 GATE-5 断言恰好 `Blocked` + T020 写入 `Planned → Blocked`；CHK004 data-model 去重表；CHK024 补 `test_acceptance_schema_ownership.py` 载体；CHK036 集合级零新增失败；CHK008 五字段 `SC-NNN_` 前缀 + 非法行非空触发；CHK035 Step 8/9 对齐；CHK027 三份 mixed-path 夹具 + T021
- 独立复跑：validate-requirements `status: ok`；pre-analyze tasks `decision=pass errors=0 advisories=0`；tasks=21 ≤40
- 结论：PASS；下一阶段 = analyze（3 个语义 FAIL + 新一致性检查）

## 阶段记录（analyze）

| 阶段 | 状态 | 证据 |
|------|------|------|
| analyze | done（ANALYZE-DONE；gate fail C0/H3/M11/L6） | 报告见本阶段日志；3 HIGH = C-01（`in-scope` 义务无判据）、E-01（`smoke-mutation`/`execution-without-final` 无断言）、H-01（`inherited` 义务未定义）；3 个 checklist 语义 FAIL 全部 upgrade（CHK017→H-01 HIGH；CHK012→H-02 MEDIUM；CHK021→H-03 MEDIUM） |

## U4 独立校验记录（analyze）

- 哨兵：`ANALYZE-DONE`；只读，`git status` 无 tracked 变更，HEAD 仍 `f8f481ec`
- 验证波：3/3 confirm（首次派发 `sdk_worker_removed`/`claude` 不可解析，去 `QODER_AGENT_SDK_*`/`QODER_SESSION_TYPE` 后成功）；无 downgrade/reject
- 读数：checker 七原因/三退出码一致；镜像/副本 `--check` 双 exit 0；FR→task→SC 零缺失；18 条宪法无 Fail（XVII 行有延迟登记不一致，F-06 MEDIUM）
- 结论：gate fail（3 HIGH），按规则先做 spec-only analyze-fix，再 analyze-r2；不得带病进入 implement

## 阶段记录（analyze-fix）

| 阶段 | 状态 | 证据 |
|------|------|------|
| analyze-fix | done（spec-only，driver completion；子代理 120-turn limit） | `f9f6d4f3`；H-01/C-01/E-01 + B-01/E-02/E-03/F-01/F-02/F-04/F-05/F-08/H-02/H-03 + LOW 处置；报告 `test-evidence/analyze-fix-report.md`；validators ok；task_count 24 |

## U4 独立校验记录（analyze-fix）

- 哨兵：子代理在 120-turn limit 处停止，未返回 `ANALYZE-FIX-DONE`；驱动者按部分产物完成校验、补报告与提交（显式异常）
- 产物：requirements.md 270 行（FR 25/SC 9/STR 17 不变）、plan.md（43 源面，D1–D10 更新）、tasks.md（24 任务，T022/T023/T024 新增）、contracts/**、data-model.md、checklists/requirements.md（superseded note）
- 提交：`f9f6d4f3`（12 文件；未 push；`master` 仍在 `cb841d90`）
- 独立复跑：validate-requirements ok；validate-tasks 0/0；decision-tensions 6/6；pre-analyze tasks pass（114 planned-path advisories）；decomposition tasks `proceed` 24/40
- 关键闭合：FR-011 `inherited` 载体规则；FR-009/FR-012 `in-scope` 三项义务；T007 断言 `smoke-mutation`/`execution-without-final`；T022 集合级全量收口；T024 `manage-features` 词表；H-02 pin 失效判据；H-03 expected_artifacts
- 结论：PASS（带子代理 turn-limit 异常披露）；下一阶段 = analyze-r2

## 阶段记录（analyze-r2）

| 阶段 | 状态 | 证据 |
|------|------|------|
| analyze-r2 | PASS（driver-side recheck，2026-11-03 02:07 UTC） | 3 HIGH 逐条复核闭合（H-01 FR-011 载体规则；C-01 FR-009/FR-012/SC-005；E-01 T007 两夹具断言）；validators：requirements ok、tasks 0/0、decision-tensions 6/6、pre-analyze tasks pass（114 planned-path advisories）；task_count 24；无新增 C/H |

## U4 独立校验记录（analyze-r2）

- 方式：上一次 analyze-r2 子代理派发被用户拒绝，驱动者按 skill 允许的「主代理自身只读核验」完成；未重复同一子代理调用
- 结论：0 CRITICAL / 0 HIGH，gate pass；下一阶段 = implement（slice 081a，分 4 part）

## 阶段记录（implement part 1）

| 阶段 | 状态 | 证据 |
|------|------|------|
| implement part 1 | done（U4 PASS，2026-11-03 02:16 UTC） | `544c2cde`；T001–T006+T021；`shared/workflow/acceptance-hardening.md` 四节 + extension points；`scripts/python/closure-acceptance-check.py` CLI surface；7 套夹具（45 文件）；`src/specify_cli/__init__.py` resolver fallback；mirror 62/shared、119/scripts；targeted 7 passed |

## U4 独立校验记录（implement part 1）

- 哨兵：`PART1-DONE`
- 产物：owner doc、checker CLI、fixtures、resolver fallback、notes；commit `544c2cde`（52 文件/1897 行；未 push）
- 验证：`py_compile` 0；`--help` 0；缺 `--spec-dir` / 不存在路径 / 空 spec / 非法 `--waive` 均 exit 2；fixture sanity 0；mirror/regen `--check` 0；targeted 7 passed；`specify init` dev-checkout probe exit 0
- 异常（均 correction-class，已披露/修复）：`sync-mirrors` 写模式会顺带跑 `regen-command-copies`（无产物 delta）；一次性 `/tmp/081-bare-spec` 裸目录已删；T005 四节边界与 Path marker 归入 § Closure Verdict；SV-05 载体措辞按 owner→carrier 指针解释；fixture 6 文件 + smoke evidence 实际 45 文件
- 特征状态：`Planned`（未提前翻 `Blocked`/`Implemented`）
- 结论：PASS；下一阶段 = implement part 2（T007–T014）

## 阶段记录（implement part 2）

| 阶段 | 状态 | 证据 |
|------|------|------|
| implement part 2 | done（U4 PASS，driver completion；子代理 120-turn limit） | `c9dc8cec`；T007–T014；4 个 contract tests（T007/T010 红、T008/T009 绿）、path-marker、state-machine/verification/tasks 模板重写、GATE-4、per-tool copies；40+14+50 targeted passed；red-first evidence 记录真实红输出；mirror/regen 0 |

## U4 独立校验记录（implement part 2）

- 哨兵：子代理在 120-turn limit 处停止，未返回 `PART2-DONE`；驱动者补跑 mirror 同步、定向测试、任务收口与提交（显式异常）
- 提交：`c9dc8cec`（22 文件 / 1546 insertions；未 push；`master` 仍在 `cb841d90`）
- 测试：`test_requirements_checker.py` 40 passed；`test_acceptance_state_machine.py` 14 passed；`test_checker_form.py` + `test_measurement_instruments.py` 50 passed；`test_closure_acceptance_check.py` 11F/5P（T015 前红）；`test_gate_wiring_081.py` 7F/1P（T016 前红）
- 镜像/副本：`sync-mirrors.py --check` 0；`regen-command-copies.py --check` 0；`validate-tasks.py` 0/0；T007–T014 已标 `[X]`
- 特征状态：仍 `Planned`
- 结论：PASS（带子代理 turn-limit 异常披露；红测试为 tests-first 预期）；下一阶段 = implement part 3（T015–T018）

## 阶段记录（implement part 3）

| 阶段 | 状态 | 证据 |
|------|------|------|
| implement part 3 | done（U4 PASS，2026-11-03 02:43 UTC） | `da5e4480`；T015 完整 checker（16 passed）、T016 implement 调用点（8 passed）、T017 smoke（1 passed）、T018 mirrors/regen 0 + fixtures 登记；`smoke-081.txt` 记录三 sub-check；`test_status_gate_owner` 扩为六状态（含 Blocked） |

## U4 独立校验记录（implement part 3）

- 哨兵：`PART3-DONE`
- 提交：`da5e4480`（16 文件/1990 insertions；未 push；`master` 仍在 `cb841d90`）
- 独立复跑：closure checker + gate wiring + smoke = 25 passed；regen/sync `--check` 0；feature 仍 `Planned`
- 披露：子代理将 T015–T018 标 `[X]`（brief 说不改 tasks；上一 part 同样收行；GATE-3 要求收尾零开放）；`test_status_gate_owner` 的六状态修正是 F-02 预测的必改项，保留反 `cleared` 原意
- 结论：PASS；下一阶段 = implement part 4（T019–T024，收尾/Blocked/全量/覆盖/词表）

## 阶段记录（implement part 4）

| 阶段 | 状态 | 证据 |
|------|------|------|
| implement part 4 | done（slice 收尾 = `Blocked`，2026-11-03 11:31 UTC） | `26a3e43d`（T019/T023/T024 + first full-suite evidence）、`a2701a4f`（wiring card/pin fix）、`8ce0f006`（T024 deferred to 081d）、`b0609f37`（verification/Blocked）；T019/T020/T023 `[X]`，T022/T024 `[~]`；closure checker `block`/exit 1/`zero-final-path-pass`；feature `Blocked` |

## U4 独立校验记录（implement part 4）

- smoke 两次 exit 0/0；`smoke-081.txt` 三 sub-check 齐备
- `verification.md`：SC-001 `blocked`（1/3 call sites）、SC-002 `partial`、SC-004 `pass`，其余 deferred/partial；final-path 0 pass
- closure checker：`verdict=block`、exit 1、`zero-final-path-pass`、tasks closed=22/deferred=2/open=0、claimed_status=`Blocked`
- 全量：first closure-repair `43F/7018P`（4 pin drift，已修）；second `40F/7021P`（1 mirror parity，因并发提交 `90de4d7f` 在运行中改 coaching-skills）；clean run 在跑
- T022 延后（需 clean full-suite set）；T024 延后到 081d（WC-14 冻结 C-5 套件）；两者均记录 unblock
- 并发事件：`90de4d7f fix(coaching-skills)` 在 11:19:54 落到本分支，改 `skills/external/coaching-skills/references/prompt-templates.md` 与镜像；未回退、未覆盖；它是 second-run mirror flake 的直接原因，已写入 notes
- 结论：implement 阶段以 `Blocked` 收尾（**不是** `Implemented`）；下一阶段 = review

## T022 clean closure（2026-11-03 03:41 UTC）

- `bash scripts/bash/run-tests.sh --names-out .specify/.tmp/081a-head-failed-clean.txt -q` → `39 failed, 7023 passed, 7 skipped in 699.18s`; `head − baseline` = 0; `baseline − head` = 0; pins unchanged.
- T022 `[X]`; T024 remains `[~]` (081d). Test budget: baseline:1 closure:1 reruns:2 exceptions:0; E3 stages complete=5/6, only review pending.
- Feature stays `Blocked` (SC-001 blocked 1/3, SC-002 partial); closure checker `block`/exit 1.

## Review-fix + final closure（2026-11-03 04:06 UTC）

- Review: P0=1 (F2), P1=5 (F1/F3/F4/F5/F6), P2=9; carriers `review.md` + `code-review.md`; no `blocking` code entry.
- Review-fix `0277b00f`: F2 moved the 081 gate lines out of the 077 card and re-measured `tasks/implement` strip baselines; F4/F7 six-bucket `final_path` incl. `partial`; F1/F3/F5/F6 corrected; F8/F9/F10/F11/F15 fixed; F12/F13/F14 recorded.
- Targeted suite 152 passed; `regen/sync --check` 0; `validate-tasks` 0/0; closure checker `block` (final_path pass0/blocked1/partial1/unknown0; tasks 23 closed/1 deferred/0 open; claimed `Blocked`).
- Final post-review-fix full-suite: `39 failed / 7025 passed / 7 skipped`; `head−baseline` 0 new; `baseline−head` 0 fixed.
- Test-budget audit: baseline:1 closure:1 reruns:3 exceptions:0; E3 stages complete=6/6; status=ok.
- 081a is closed as **`Blocked`** (SC-001 1/3, SC-002 partial, T024 081d). Next slice = 081b.

## 081b 入口（Phase 2）

- **切片**：081b — runtime stack / Execution Premises / Inherited Blockers + 四类确定性发现（parent requirements FR-009…FR-012 / SC-005；plan § D4 + D10 081b 行）。
- **断点**：`tasks`（parent requirements/plan 已存在且覆盖 081b；081a tasks 归档在 `tasks-081a.md`；本轮生成新的 `tasks.md`）。
- **阶段计划**：`tasks → checklist → analyze → implement → review → closure`（requirements/clarify/plan 继承 parent 081）。
- **测试预算**：baseline = 081a final full-suite（39F / 7025P / 7S，`closure-final-run.txt`），closure = 081b review 后。
- **不做**：081c 的 review-feature-quality / 四段组合 / review 调用点；081d 的 manage-features / feature-index / audit / driver line-state / driver merge gate / coverage guard。
- **状态**：Feature 081 仍 `Blocked`；081b 的 supporting SC-005 可转 pass，但 final SC-001/SC-002 仍等 081c/081d。

## 081b tasks（2026-11-03 04:36 UTC）

- `tasks.md` 12 任务（081a 归档 `tasks-081a.md`）；FR-009…FR-012 covered；SC-005 precise partial；parent Feature 081 仍 `Blocked`。
- 门禁：decomposition `proceed` 12/40；pre-analyze `pass`（62 planned-path advisories）；validate-tasks 0/0。
- 提交 `8a949241`；下一阶段 = checklist。

## 081b checklist（2026-11-03 04:46 UTC）

- `checklists/081b-2026-11-03.md` 42 项：24 PASS / 18 FAIL；7 条 P1：CHK019（inherited 载体无解析语法/连接键）、CHK017（C-17 抽取集合与五条 partial 不相交 → 0 行静默绿）、CHK020（后续切片载体无合法处置值）、CHK018（载体三种读法）、CHK005（零行静默放行）、CHK004（义务 ②③ 判定时点）、CHK013（premise-ID 零载体）。
- 提交 `43b0e668`；下一阶段 = analyze（裁决 18 FAIL，修 tasks/plan 后再 implement）。

## 081b analyze（2026-11-03 05:02 UTC）

- 结果：C=0 / H=8 / M=12 / L=4，gate fail；8 HIGH 经独立只读波确认（9 派发 / 8 confirm / 1 downgrade / 0 reject）。
- 关键 HIGH：F-12 duty ②③ 时点；C-02 零行静默放行；E-05 premise-ID 零载体；F-13 C-17 抽取集与 `partial` 行不相交；B-02 载体三读法；C-03 载体无解析语法/连接键；F-14 `plan-template.md` 豁免清单；E-06 `signed-contract` 契约路径无列。
- 结论：不得带病 implement；先做 spec-only analyze-fix，再 analyze-r2。

## 081b analyze-fix + r2（2026-11-03 05:14 UTC）

- `ce4c0f11`：8 HIGH 全修 —— C-17 抽取纳入 `partial`/`deferred_tasks`；Carrier/Source row 语法 + join key；`Carrier slice`/`inherited-later`；`Contract`/`Premises` 两列；in-scope duty ①/②/③ 分阶段；zero-data-row = block；四发现 check 名/severity；FR-005 覆盖行；plan-template 第四豁免 + 零域字面量；expression-gates 算子修正；E-10 转 081d。
- 驱动者 r2：validate-requirements ok、validate-tasks 0/0、decision-tensions 6/6、pre-analyze tasks pass（67 planned-path advisories）；FR-009 表头 `Contract`/`Premises` 在盘；IB-004 `inherited-later`/`carrier_slice` 在盘；C-17 含 `partial`/`deferred_tasks`；无新增 C/H。
- 结论：analyze-r2 PASS；下一阶段 = implement 081b part 1/3（T001–T004）。

## implement 081b part 1（2026-11-03 05:22 UTC）

- `b29a8a4c`：五套夹具（premise/runtime-gap/runtime-zero-row/inherited-mutation/inherited-clean）、`notes/red-first-evidence-081b.md`、owner doc 三节（九列/五列/继承表 + Carrier 语法 + inherited-later）、plan-template 两骨架（零域字面量）；mirror/regen 0；feature 仍 `Blocked`。
- 披露：081a 的 `positive` 等夹具仍是七列旧形态；part 2 需升级为九列（或明确缺列不触发），否则 `positive` 接受与 `Premises` 义务冲突。

## implement 081b part 2（2026-11-03 05:38 UTC）

- `793aff9e`：T005–T009；`test_acceptance_premises.py`（132 targeted passed）、pre-analyze 四发现、closure checker 外部来源抽取（partial/deferred_tasks、carrier、inherited-later、zero-row、prose）、expression-gates 修正 + 守卫、081a 夹具九列升级；mirror/regen 0；feature 仍 `Blocked`。
- 披露：子代理在 T009 regen 处 120-turn 停止；驱动者补跑 checks、132 测试并提交。

## implement 081b part 3 halt（2026-11-03 05:44 UTC）

- T011 done（smoke 0/0，081a 证据保留）；T010 halted：checker exit 2 on 081's own `Contract` cells（annotated prose / two candidate paths）and `Source row` cells（`（第 N 行）` annotations violate grammar）；T012 blocked by T010.
- 第三缺陷：`declared_dependency_files()` 扫描 § Inherited Blockers 内任意反引号 `.md`，把本 spec 的 `verification.md` 当成第九个依赖，产生 9 条 `081:...` 自依赖行。
- 处置：不手写计数；先修 `Contract`/`Source row`/依赖声明三处（spec + checker），再重跑 T010/T012。
- 提交 `61b62006` + `8a4e7c7c`（证据/异常记录）；feature 仍 `Blocked`。

## 框架观察

- 026 的零 pass `Implemented` 不是单点事故：`Planned → Implemented` 的 DoD 只要求 tasks 收口 + SC 有状态行，不要求 final-path SC `pass`；review 门只要求 P0/P1=0，不检查验收现实；driver 合并门只看 review 通过 + 测试预算。
- 本特性要把“更严格验收”落到确定性门：final-path SC + `Blocked` 状态 + 基本 smoke test + closure-acceptance-check；运行时栈/依赖所有权与执行前提/继承 blocker 作为模板强制字段；review 增加实现与产物质量审查。
- 约束：Two Hats——框架源（`templates/`、`shared/`、`skills/`、`scripts/`）是改动落点，`.specify/` 镜像由同步生成，不手改；现有特性不追溯改状态，audit 只读。

## implement 081b part 4 / slice close（2026-11-03 06:10 UTC）

- 三缺陷修复（不手写计数）：`requirements.md` 的 `Contract` 单元格各留一条可解析路径，次级引用移入 Contract-cell note；`plan.md` 五条 `Source row` 还原为纯 locator（`（第 N 行）`移入 Evidence）；`closure-acceptance-check.py` 的依赖集改为只读 `**Dependency artifacts (declared, never implied)**` 块，自排除收窄到本 spec 的四个 canonical 文件；两个 `inherited-*` 夹具改为同一声明块形态（路径在 bullet 行）。mirror 已同步。
- closure checker（081 spec dir）：`verdict=block`、exit 1、`zero-final-path-pass`、`final_path pass=0 blocked=1 deferred=0 partial=1 fail=0 unknown=0 total=2`、tasks closed=12/deferred=0/open=0、`no_open_rows=true`、`smoke_record_pass=true`。payload `.specify/.tmp/081b-closure-verdict.json`，tracked copy `test-evidence/closure-verdict-081b.json`。
- T010：SC-005 → `partial`；读数 = 四发现 4/4（两个 producer）、`RS-004` 三义务 3/3、8/8 records（7 settled + 1 `inherited-later`，IB-004 → 081c）；接受摘要从 payload 复制（未手算）。SC-001 保持 `blocked`，SC-002 保持 `partial`。
- T011：part 3 已完成（smoke 0/0，`smoke-081a.txt` 保留）。
- T012：5 模块 `89 passed` exit 0，记录 `test-evidence/tasks-081b-slice-tests.txt`；全量基线对照留给 081d（FR-023）。
- 测试预算：baseline = 081a final full-suite（39F/7025P/7S）；081b 为切片，按 tasks.md 不做全量 closure run，T012 的 targeted 观测不冒充集合级对照。
- 12 个任务全部 `[X]`；feature 状态仍 **`Blocked`**（081b 不接调用点，SC-001/SC-002 不动）。下一阶段 = 081b review。
