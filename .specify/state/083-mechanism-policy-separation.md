# Line State — 083-mechanism-policy-separation

<!-- loop-state:begin -->
spine_state: done
run_id: r20261105T033420Z-082a
slice: main+skill-reference-grammar
stage: done
stage_started_at: 1793878143
stage_deadline_epoch: 1793888943
stage_base_commit: 6677b514
attempt: 1
retry_limit: 3
last_verdict: closure repair CLOSURE-DONE @6677b514 — full suite 16F/7280P/7S (771.89s), new=0, 8 fixed, C-57 absent (17→16); audit status=ok (baseline:1 closure:1 reruns=1, stages=6 complete=6); acceptance accept (final 8/8, smoke exit 0); line completed, local merge to master
<!-- plan-fence: decomposition=single-package@plan-D8; test-budget=baseline@implement-start + closure@post-review; plan_constraint=active@974db180; fast-lane=not-adopted -->
<!-- loop-state:end -->

<!-- test-budget:begin -->
{"seq": 1, "slot": "baseline", "stage": "implement", "purpose": "083 implement-start baseline", "trigger": "implement start", "at": "2026-11-05T15:07:02+0800", "selection_basis": "full-suite", "command": "env -u PYTHONPATH bash scripts/bash/run-tests.sh --names-out .specify/specs/083-mechanism-policy-separation/baseline-failed.txt -q", "rc": 1, "passed": 7157, "failed": 24, "skipped": 7, "failed_names_path": ".specify/specs/083-mechanism-policy-separation/baseline-failed.txt", "evidence_ptr": ".specify/specs/083-mechanism-policy-separation/test-evidence/implement-part1-baseline.txt", "captured_at": "2026-11-05T15:07:02+0800", "note": "24 pre-existing failures on the dispatched working tree (includes the known concurrent skill-reference effect tests/contract/test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes, fixed by T038; plus 083 budget-calibration drift and other pre-existing debt). Recorded, not hidden, not attributed to 083."}
{"seq": 2, "slot": "closure", "stage": "closure", "purpose": "post-review closure full-suite rerun and baseline name-level comparison", "trigger": "review passed", "at": "2026-11-05T19:27:34+0800", "command": "env -u PYTHONPATH bash scripts/bash/run-tests.sh --names-out .specify/specs/083-mechanism-policy-separation/final-failed.txt -q", "selection_basis": "full-suite", "rc": 1, "passed": 7279, "failed": 17, "skipped": 7, "failed_names_path": ".specify/specs/083-mechanism-policy-separation/final-failed.txt", "baseline_compare": "name-level diff vs baseline-failed.txt: comm -13 baseline-failed.txt final-failed.txt -> new=[\"tests/contract/test_client_guard_sweep.py::test_c57_shipped_text_adds_no_fresh_neutrality_violation\"]; comm -23 baseline-failed.txt final-failed.txt -> fixed=[\"tests/contract/test_coaching_run_contract.py::test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work\", \"tests/contract/test_coaching_wiring_contract.py::test_c1_eight_identity_coordinates_all_hold\", \"tests/contract/test_coaching_wiring_contract.py::test_c3_probe_compiled_face_is_zero_drift\", \"tests/contract/test_coaching_wiring_contract.py::test_c8_the_verification_surface_runs_green\", \"tests/contract/test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes\", \"tests/contract/test_ledger_reconciliation.py::test_real_tree_reconciles_clean_with_the_declared_coverage_numbers\", \"tests/contract/test_probe_nonentity_catalog.py::test_catalog_does_not_participate_in_registry_counts\", \"tests/contract/test_scripts_distribution_parity.py::TestScriptsDistributionParity::test_repo_has_no_orphan_or_drifted_scripts\"]", "evidence_ptr": ".specify/specs/083-mechanism-policy-separation/test-evidence/closure-final-run.txt", "note": "17 failed = 24 baseline names - 8 fixed + 1 new. The new failure is 083-attributable: commit 88be0714 (T039) put the literal 'Feature 083' into shipped text shared/definitions/framework-map.md line 28, which C-57's client-neutrality sweep reads as a fresh framework-runtime reference. Recorded, not fixed: the closure boundary hands new failures to the driver (U5); no repair and no rerun were performed."}
{"seq": 3, "slot": "in-slot-rerun", "stage": "closure", "purpose": "closure repair: remove the fresh 'Feature 083' neutrality reference from shipped shared/definitions/framework-map.md and re-measure the full suite once in the same closure slot", "trigger": "closure-repair C-57", "at": "2026-11-05T19:44:37+0800", "command": "env -u PYTHONPATH bash scripts/bash/run-tests.sh --names-out .specify/specs/083-mechanism-policy-separation/final-failed.txt -q", "selection_basis": "full-suite", "rc": 1, "passed": 7280, "failed": 16, "skipped": 7, "failed_names_path": ".specify/specs/083-mechanism-policy-separation/final-failed.txt", "baseline_compare": "name-level diff vs baseline-failed.txt: comm -13 -> new=[] (empty; every remaining failure is an E2-baseline name); comm -23 -> fixed=[\"tests/contract/test_coaching_run_contract.py::test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work\", \"tests/contract/test_coaching_wiring_contract.py::test_c1_eight_identity_coordinates_all_hold\", \"tests/contract/test_coaching_wiring_contract.py::test_c3_probe_compiled_face_is_zero_drift\", \"tests/contract/test_coaching_wiring_contract.py::test_c8_the_verification_surface_runs_green\", \"tests/contract/test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes\", \"tests/contract/test_ledger_reconciliation.py::test_real_tree_reconciles_clean_with_the_declared_coverage_numbers\", \"tests/contract/test_probe_nonentity_catalog.py::test_catalog_does_not_participate_in_registry_counts\", \"tests/contract/test_scripts_distribution_parity.py::TestScriptsDistributionParity::test_repo_has_no_orphan_or_drifted_scripts\"]. Arithmetic correction to the dispatched expectation: C-57 was never a baseline name, so it cannot appear in comm -23; its repair shows as absence from final-failed.txt relative to the seq=2 closure list (17 -> 16).", "evidence_ptr": ".specify/specs/083-mechanism-policy-separation/test-evidence/closure-final-rerun.txt", "note": "16 failed = 24 baseline names - 8 fixed; all 16 remaining names sit inside the E2 baseline set. The C-57 test passes in the targeted run (rc=0) and is absent from the rerun list. Full-suite runtime 771.89s."}
<!-- test-budget:end -->

- line_id: `083-mechanism-policy-separation`
- run_id: `r20261105T033420Z-082a`
- project_dir: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- repo_root: `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`
- worktree: `none（本地拓扑，主工作区；feature branch 由 requirements 阶段创建）`
- base_sha: `3ffeb26e`
- trunk: `master`
- topology: `local`（宿主原生子代理；不启动 qodercli）
- state: `running`

## U0 入口声明

- **目标项目**：spec-kit 框架源码仓（本地 `/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`；cwd 向上命中合法 `.specify/`）
- **执行拓扑**：本地（宿主原生子代理；阶段派发不启动 qodercli）
- **终态权威文档**：用户本轮入口描述 + `.specify/memory/constitution.md`（v1.15.0）+ `.specify/instructions.md` + 现有元技能 SKILL（`skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md`）+ `.specify/shared/definitions/` 与 `shared/guidelines/` 既有 owner 文档；本特性 spec 落地后以 spec 目录为准
- **特性切片**：新建特性（暂名 083 `mechanism-policy-separation`）。原则：**机制/策略分离（能力/职责分开）**——
  - 「机制/能力」层：逻辑、算法、步骤 → 归档在 skills 目录（技能定义本体与其 references/scripts）；
  - 「策略/职责」层：配置、输入、输出 → 归档在具体运行环境（用户指定目录、当前工作目录、`.specify` 等）；
  - 命令或技能执行时必须同时具备两层信息；不明确时提示用户提供；
  - 该原则落入**元技能/元命令**（操作其他命令与技能的流程，如 `skills/external/create-skills`、`skills/external/improve-skills` 及其同族）的作者与改进流程中，**不回溯改造**当前项目已加载的全部技能。
- **断点**：U1 探测 → `requirements`
- **阶段计划**：`requirements → clarify → plan → tasks → checklist → analyze → implement → review → closure → 合并`
- **快车道**：入口未声明 `fast-lane=opt-in` → 完整链
- **拆解开关**：`decomposition=auto`
- **测试预算**：implement 起点一次全量基线、review 后 closure；中间阶段定向集
- **类别四元组**：`flow_class=execution`；`source=declaration`；`marker=null`；`error=-`（requirements 声明行已落地；每次派发前重新解析）

## U1 断点探测（2026-11-05 11:34 +08）

| 探测项 | 实测 |
|--------|------|
| 当前分支 | `master` |
| 工作树 | 干净（`git status --porcelain` 无输出） |
| 最近提交 | `3ffeb26e`（081 final acceptance / branch retire） |
| spec 目录 | 最高 `081-acceptance-hardening`；无 083 / mechanism-policy 相关 spec |
| Feature 注册表 | 最高 081（Completed）；无 083 相关行 |
| 治理 | constitution v1.15.0（18 principles）；instructions 含 Two Hats / One Source / Fast Fail / Directory Governance |
| SDD 分流裁决 | `verdict: sdd`（`sdd-capability-or-contract-change`；nature=feature / traceability=required / blast=cross-cutting / reversible） |
| 结论 | **断点 = requirements**；新建特性 083 |

## 派发前置检查（Preflight，本地拓扑）

| # | 检查 | 结论 |
|---|------|------|
| ① | SSH 连通性 | `n/a` — 本地拓扑跳过 |
| ② | 非 root 运行用户 | `ok` — uid=501 |
| ③ | 子代理 CLI 可用性 | `n/a` — 本地原生子代理，不启动外部 CLI |
| ④ | 大语言模型配置（已解析） | `ok` — `execution-config.py --action resolve --agent sdd-requirements-executor` exit 0，`config_id=e1c83cb996590535`，`mode=native` |
| ⑤ | spec-kit 框架可用性 | `ok` — `.specify/` 与 `constitution.md` 在位 |

## 阶段记录

| 阶段 | 状态 | 证据 |
|------|------|------|
| requirements | dispatched（2026-11-05 11:34 +08） | 本地原生子代理（SDD Requirements Executor）；提示词三段骨架 + 类别四元组 + 测试预算块 |
| requirements | retry 1（2026-11-05 11:37 +08） | attempt 1 在 run-turn-budget 40 处停住（无哨兵；已产出 requirements.md 197 行；validator 2 error / 2 warning）；原因 = 实例预算 40 偏紧；修复 = 改用 SDD Executor（run-turn-budget 120）做完成收尾，不重做规格 |
| requirements | done（U4 PASS，2026-11-05 11:42 +08） | `88f8da14` + `66962d1b`；requirements.md 211 行（18 FR / 5 SC / 3 STR / A1–A10 / C1–C8 / Runtime Stack 5 行）；validator ok；pre-analyze pass（0 error / 3 expected advisory）；decomposition proceed（18/30）；flow-class declaration |

## U4 独立校验记录（requirements）

- 哨兵：`REQUIREMENTS-DONE`（回传最后一行）
- 产物：`requirements.md`（211 行；18 FR / 5 SC / 3 STR；A1–A10；C1–C8；§ Runtime Stack & Dependency Ownership 5 行）、`checklists/requirements.md`、`test-evidence/{validate-requirements.txt,flow-class-lookup.txt,requirements-u4-gates.txt,requirements-stage-status.jsonl}`
- 提交：`88f8da14`（阶段主体）+ `66962d1b`（U4 门修复与证据刷新）
- 纪律：未 push；`.specify/state/`、`.specify/.tmp/` 与运行时记录未进入阶段提交；`Related Feature` 保持 `Need clarification`
- 独立复跑：`validate-requirements.py` status ok（0 error / 0 warning，211 行）；`pre-analyze-check.py --stage requirements` decision=pass（errors=0，advisories=3 预期）；`decomposition-check.py --mode plan` decision=proceed（fr_count=18 / ceiling 30）；`flow-class-check.py --action lookup` exit 0（source=declaration）
- 驱动侧纠正（disclosed）：① 补 § Runtime Stack & Dependency Ownership（5 行，RS-001…RS-005）——缺失时 pre-analyze exit 2；② SC 定义行全角冒号改 ASCII——否则 checker 识别 0 条 SC 并产生 31 条 dangling-id。两处均为单读法纠正，已写入 checklist Notes 与 stage-status。
- 结论：PASS，下一阶段 = clarify

## Wrap-up 记账（requirements）

- run-determination: `.specify/memory/session/20261105T034151Z-run-determination-speckit-requirements-r20261105t033420z-082.md`
- feedback: `.specify/memory/feedback/20261105T034201Z-speckit-requirements.md`
- exec-quant: `.specify/memory/exec-quant/records/20261105T034151386780Z-daca16a4.json`
- 说明：执行子代理未在回传中执行 Wrap-up；驱动者在 U4 补跑三步（stage-prompts § Independent Verification 的补跑规则）。

## 框架观察（requirements）

- **现象**：`pre-analyze-check.py --stage requirements` 强制要求 `requirements.md` 含 § Runtime Stack & Dependency Ownership，但 `create-requirements` 技能与 `templates/requirements-template.md` 未提及该表；新特性按默认流程生成规格必然门失败（exit 2）。**框架位置**：`skills/internal/create-requirements/SKILL.md` / `templates/requirements-template.md`。**对驱动的影响**：本次需驱动侧补表并重跑门。
- **现象**：checker 识别 SC 定义行要求 ASCII 冒号；规格正文使用中文全角 `：` 时静默得到 0 条 SC，进而把清单中的 SC 引用全部判为 dangling-id。**框架位置**：`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`（SC 定义正则）。**对驱动的影响**：一次 U4 门失败与 31 条级联错误。
- **现象**：`audit-test-budget.py` 按 `*.jsonl` 文件名 stem 取阶段名，`requirements-stage-status.jsonl` 被读成非 E3 阶段而跳过。**框架位置**：`skills/external/sdd-loop-driver/scripts/audit-test-budget.py`。**对驱动的影响**：requirements 的 E3 行不进入分母（审计本就不含 requirements 阶段），但命名约定缺 owner 裁定。
- **现象**：`sdd-requirements-executor` 实例的 `run-turn-budget: 40` 对完整规格偏紧，attempt 1 在 Shared Strings 修复处耗尽。**框架位置**：`.specify/agents/instances/sdd-requirements-executor.agent.md`。**对驱动的影响**：需要以 120 回合的 SDD Executor 做完成 pass。

## 阶段记录（clarify）

| 阶段 | 状态 | 证据 |
|------|------|------|
| clarify | done（U4 PASS，2026-11-05 11:45 +08） | `aaee504c`；Feature 083 绑定（`features.md` 77=77、`features/083.md` Draft）；A1–A10 / C1–C8 裁决（C1 谓词逐字保留：create-skills/improve-skills/merge-skills 纳入，coaching-skills/run-skills 排除并写理由，`/speckit.skills` 为命令面）；validator ok；overlap clear；pre-analyze pass（0 error / 7 expected advisory） |

## U4 独立校验记录（clarify）

- 哨兵：`CLARIFY-DONE`（回传最后一行）
- 产物：`requirements.md`（225 行；Related Feature 绑定 083；`## Clarifications` Session 2026-11-05）、`features.md`（083 行 + Total 77=77）、`features/083.md`（Draft）、`test-evidence/clarify-gates.txt`、E3 clarify 行
- 提交：`aaee504c`（仅 clarify 产物；未 push；state spine 未提交）
- 独立复跑：`validate-requirements.py` status ok（225 行 / 0 error / 0 warning）；`overlap-check.py` `decision=clear`（checked=1 / overlaps=0）；`pre-analyze-check.py --stage requirements` `decision=pass`（errors=0 / advisories=7 预期：owner 文档尚未创建 + 类路径占位）
- 结论：PASS，下一阶段 = plan

## Wrap-up 记账（clarify）

- run-determination: `.specify/memory/session/20261105T034532Z-run-determination-speckit-clarify-r20261105t033420z-082.md`
- feedback: `.specify/memory/feedback/20261105T034532Z-speckit-clarify.md`
- exec-quant: `.specify/memory/exec-quant/records/20261105T034532226069Z-96d1a028.json`
- 说明：执行子代理未在回传中执行 Wrap-up；驱动者在 U4 补跑三步。

## 阶段记录（plan）

| 阶段 | 状态 | 证据 |
|------|------|------|
| plan | attempt 1（2026-11-05 11:50 +08） | 120 回合预算耗尽；已产出 research.md / data-model.md / contracts×3 / quickstart.md / feature-ref.md，未产 plan.md |
| plan | done（U4 PASS，2026-11-05 12:11 +08） | `58d3dc5b`；plan.md 367 行（18 原则 Constitution Check、D1–D10、T-001–T-003、EP-001–EP-006、Inherited Blockers 零行、Measurement Plan）；pre-analyze pass（0 error / 50 expected advisory）；validator ok |

## U4 独立校验记录（plan）

- 哨兵：`PLAN-DONE`（回传最后一行；两条 ANOMALY 行随后，已按下述 U5 程序处置）
- 产物：`plan.md`、`research.md`、`data-model.md`、`contracts/{owner-document,skill-wiring,guard-and-measurement}.contract.md`、`quickstart.md`、`feature-ref.md`、`test-evidence/plan2026-11-05-{plan-gates,baseline,stage-status}.…`
- 提交：`58d3dc5b`（11 files / +1625；仅 spec 目录 plan 产物；未 push；`requirements.md`、`features.md`、`features/083.md`、`.specify/state/` 未改动）
- 独立复跑：`pre-analyze-check.py --stage plan` decision=pass（errors=0，advisories=50 条均为 implement 期才创建的文件路径）；`validate-requirements.py` status ok（225 行 / 0 error / 0 warning）
- 结论：PASS；**但下一阶段派发前触发了 U5 停线**（见下）

## Wrap-up 记账（plan）

- run-determination: `.specify/memory/session/20261105T041200Z-run-determination-speckit-plan-r20261105t033420z-082.md`
- feedback: `.specify/memory/feedback/20261105T041200Z-speckit-plan.md`
- exec-quant: `.specify/memory/exec-quant/records/20261105T041200397349Z-a9009299.json`
- 说明：执行子代理未执行 Wrap-up；驱动者在 U4 补跑三步。

## 异常与停线（U5，2026-11-05 12:12 +08）

- **发现了什么**：本会话运行期间，主工作树出现 10 个未提交修改（`skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}/SKILL.md`、`skills/internal/run-skills/SKILL.md` 及其 `.specify/skills/` 镜像）和 2 个未跟踪文件（`shared/definitions/skill-reference-definitions.md`、`.specify/shared/definitions/skill-reference-definitions.md`），mtime 12:07–12:08。内容是一个**无关的并发特性**（技能引用语法与归一化），不是 083 的实现；两份 plan 基线读数（受污染树 / 干净树）已在 `test-evidence/plan2026-11-05-baseline.txt` 如实记录。
- **为何吃重**：这些路径正是 083 的 implement 阶段要修改的三份元技能与所在目录；若按主工作树继续，阶段提交会把未知的并发改动混入 083，或覆盖用户在进行中的工作；plan 的 SC-003 逐字节封闭集与实现基线也会被污染。
- **已产生的中间产物逐项可定位**：`88f8da14`（requirements 主体）、`66962d1b`（requirements 门修复）、`aaee504c`（clarify + Feature 083 绑定）、`58d3dc5b`（plan）；状态脊本条；spec 目录 `.specify/specs/083-mechanism-policy-separation/`；plan 门证据 `test-evidence/plan2026-11-05-plan-gates.txt`。
- **可选处置**：(a) 视为无关的进行中工作，保留原样，083 改在基于 `58d3dc5b` 的隔离 worktree 继续；(b) 用户确认这些改动属于本次工作，先提交或并入后再续；(c) 用户明确授权丢弃这些改动后原地继续；(d) 停线移交。
- **停线时状态**：`stalled` / `reentry-required`；未删除、未还原、未提交任何并发改动；等待用户裁定。

## 用户裁定（2026-11-05，scope change）

- **裁定**：将工作树中的并发改动「技能引用语法与归一化」（`shared/definitions/skill-reference-definitions.md` + `create-skills` / `improve-skills` / `merge-skills` / `coaching-skills` / `run-skills` 的引用归一化接线）**并入 083**，与机制/策略分离原则一起交付。
- **裁定者**：用户（AskUserQuestion，2026-11-05 12:13 +08）。
- **影响**：083 的范围从「机制/策略分离」扩为「元技能治理：机制/策略分离 + 技能引用归一化」。需要按 SDD 链重开 requirements → clarify → plan → tasks → checklist → analyze → implement → review；现有未提交改动**保留不丢弃**，作为该能力的实现输入；已完成的机制/策略分离 artifacts 不被推翻，只做增量扩展。
- **重入断点**：`requirements`（scope update），基线 `58d3dc5b`。
- **状态**：line resumed（running）。

## requirements scope update（2026-11-05，U4 PASS）

| 阶段 | 状态 | 证据 |
|------|------|------|
| requirements (scope update) | done（U4 PASS，2026-11-05 12:21 +08） | `518466db`；requirements.md 292 行（FR-001…FR-030 / SC-001…SC-009 / A11 / C9 / STR-004 / STR-005）；validator ok；pre-analyze pass（0 error / 52 expected advisory）；decomposition proceed（fr_count=30，ceiling 60 after calibration）；checklist 记录未闭合项（SC-006…009 载体待落、owner 文档归一化顺序矛盾、镜像 vs 源路径口径）交 clarify/plan |

- 增量关键点：新增 US5 / F 组 FR-019…FR-030 / SC-006…SC-009；Feature 名称扩为「元技能治理：机制/策略分离与技能引用归一化」；A11 记录用户并入裁定；C9 划清两个 owner（mechanism-policy-definitions vs skill-reference-definitions）；既有 083a 内容未删改。
- 待 clarify：① Feature 083 详情/索引改名；② owner 文档归一化顺序与接受形式表的矛盾（并发实现起点有缺陷，FR-021/FR-030/SC-006 已要求修正）；③ 五消费方引用镜像路径 vs 本规格引用源路径的口径；④ 30 FR 在预算校准后已落入 60 上限，plan 的 083a/083b 切片是否保留需重判。

## 预算校准（083，direct，2026-11-05）

- 用户追加指令：提高框架各卡点与 split 预算（1M context）。
- 路由：`direct` / `direct-conditions-all-hold`（definition-class 有界修正）。
- 变更：sdd-executor 120→400；requirements/setup 实例 40→200；framework-engineer 24→100；skill-verifier 12→40；structure-adjuster 15→50；role templates 10–25→40–100；stage timeout 90→180 min；retry 2→3；split ceilings 30/40→60/80；segment >20/>40 & ≤8→>40/>80 & ≤16；fast-lane band 8–30/10–40→8–60/10–80；`loop-state.py` retry default 2→3 并修正 spine 优先级；技能体积 5000-token 预算保持不变（刻意纪律 + WC-07 契约禁止上调）。
- 证据：`083-budget-calibration-tests.txt`（219 passed）、`083-loop-state-self-test.txt`（36 passed）、sync-mirrors --check 0、regen-command-copies --check 0。
- 状态：工作树未提交（用户未要求提交）；不影响 083 后续阶段的派发。

## 阶段记录（clarify scope update，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| clarify (scope update) | done（U4 PASS，2026-11-05 14:03 +08） | `00641764`；requirements.md 318 行（FR-030 / SC-009 / STR-005；C11；7 条 scope-update 裁决）；Feature 083 改名（index 77=77）；validator ok；pre-analyze pass（0 error / 54 expected advisory）；overlap 见下 |

- 裁决：① 归一化顺序 = 形态判定 → 去空白/引号 → 剥 `skill:` 与一段 `@`/`/` 前缀（接受 `@/name`）→ 剥 `SKILL.md`/尾 `/` → name/path 通道 → 三值输出（命令面 / 技能标识 / 失败）；② 消费方引用源路径 `shared/definitions/skill-reference-definitions.md`（镜像仅由 sync-mirrors 生成）；③ 预算上调后 30 FR ≤ 60，切片前提消失，是否撤销 083a/083b 交 plan 更新重判。
- 残留待 plan：`speckit.skills` 与 `speckit.skills/SKILL.md` 的 NAME/PATH 分类冲突；name/path 通道集合未闭合；`run-skills`「名字可省扩展名」与名字通道不剥 `.md` 冲突（fixture R14）；形态判定步骤落点；SC-006…SC-009 尚无测试（仅 fixture）。

## Overlap adjudication（clarify U4，2026-11-05）

| 路径 | 唯一 owner | 另一方处置 | 时间 |
|------|-----------|-----------|------|
| `shared/workflow/glossary.md` | 029-glossary-mechanism（glossary 协议的历史 owner） | 083 只按协议新增一行词条，把它当共享注册表/只读协议，不作为交付面；plan 更新时从 feature-ref 交付声明中移除该引用 token | 2026-11-05 |
| `skills/external/create-skills/SKILL.md` | 083（当前活动写线） | 059/062/063 已 Completed，无并发写；083 可修改 | 2026-11-05 |
| `skills/external/improve-skills/SKILL.md` | 083（当前活动写线） | 059/062/063 已 Completed，无并发写；083 可修改 | 2026-11-05 |
| `skills/external/merge-skills/SKILL.md` | 083（当前活动写线） | 059/062/063 已 Completed，无并发写；083 可修改 | 2026-11-05 |

- **说明**：`overlap-check.py` 对**已完成**特性的实际历史交付面也计入比较（081 复跑同样报 29 条）。因此对“新特性修改既有共享文件”这一常态，checker 的 `clear` 不可达；本线按 §7.4 记录归属裁决，plan 更新阶段改写 feature-ref 的交付声明并复跑，若仍只剩上述历史重叠则按本裁决继续。
- **不变量**：无并发活动线写同一路径；MUST NOT 启动第二条写线写这些路径。

## 阶段记录（plan scope update，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| plan (scope update) | done（U4 PASS，2026-11-05 14:26 +08） | `d20ed616`；plan.md 元技能治理版（30 FR / 9 SC；D1–D14；4 contracts；11 test modules；single-package ≈36）；research / data-model / contracts / quickstart(14) / feature-ref 同步；pre-analyze pass（0 error / 99 expected advisory）；validator ok；decomposition proceed（30/60）；overlap 18 行历史已完成，已按裁决记录 |

- U4 说明：执行子代理在宿主 120 回合上限处停住（未发哨兵），但产物与门证据完整；驱动者独立复跑四门并提交。宿主注册已 render 为 400，但当前会话的 native agent 上限仍是 120——后续阶段按有界分段派发，直到新会话加载 400 注册。
- overlap：18 行 = `shared/workflow/glossary.md` 3 行（029/044/051；083 只按协议加一行，不作为交付面，但 feature-ref 为记录裁决仍点名它）+ `skills/internal/run-skills/SKILL.md` 4 行（057/059/062/063）+ 三份元技能各 3 行（059/062/063）+ `coaching-skills/SKILL.md` 2 行（078）；全部 completed，无并发写线。

## 阶段记录（tasks，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| tasks | done（U4 PASS，2026-11-05 14:34 +08） | `5e60c629`；tasks.md 52 行（US1–US5；单包；EP-001…EP-007；DoD-1…DoD-10；GATE-1…GATE-8）；pre-analyze pass（0 error / 123 expected advisory）；validate-tasks PASS；decomposition proceed（30/60、52/80） |

- U4 说明：执行子代理在本会话 120 回合内完成并提交；两条 ANOMALY 转 implement 义务：① green-point 归属缺失（四份 contracts 声明 md-none clause form，四个 green-* validator 在 tasks.md 上空绿）；② `account-clause-coverage.py` rc 2 baseline-missing（083 无 coverage-baseline.txt，0/30 FR 从 citation group 解析）。

## Wrap-up 记账（tasks）

- run-determination: `.specify/memory/session/20261105T063435Z-run-determination-speckit-tasks-r20261105t033420z-082a.md`
- feedback: `.specify/memory/feedback/20261105T063435Z-speckit-tasks.md`
- exec-quant: `.specify/memory/exec-quant/records/20261105T063435844961Z-07328654.json`

## 阶段记录（checklist，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| checklist | done（U4 PASS，2026-11-05 14:41 +08） | `32389f88`；`checklists/quality-scope-update.md` 89 项（CHK001–CHK089，14 节 A–M）；结构自检 PASS；G-checklist-duplicate pass（13 files）；validate-requirements ok；flow-class execution/declaration |

- U4 说明：清单项满足判定不在本门裁决（由 implement 的 checklist 豁免门接管）；本门只判产物存在与非空、项编号连续、维度覆盖。
- 披露：① 40 项软上限被有意超过（89 项；11 维度 + 11 风险面）；② objective-analysis 门触发并按门规则 7 降级为直接有界阅读（执行体无子代理派发工具）；③ 四条 medium 发现：guard-and-measurement 契约计数漂移（GM-04/GM-03/GM-12）、requirements line 306 自相矛盾、GM-12 断言字面差异、两条 implement 义务未变。交 analyze 复核。

## Wrap-up 记账（checklist）

- run-determination: `.specify/memory/session/20261105T064151Z-run-determination-speckit-checklist-r20261105t033420z-082a.md`
- feedback: `.specify/memory/feedback/20261105T064151Z-speckit-checklist.md`
- exec-quant: `.specify/memory/exec-quant/records/20261105T064151381207Z-e872cc64.json`

## 阶段记录（analyze #1 + repair，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| analyze #1 | FAIL（CRITICAL 0 / HIGH 2 clusters；12 MEDIUM / 2 LOW） | 基线 `32389f88`；H-01 plan Decision Tensions 机器门（dtr-anchor + 4 expected_sacrifice）；H-02 coverage baseline 缺失；报告正文见 analyze #1 回传 |
| analyze repair | done（2026-11-05 14:56 +08） | `974db180`；H-01 锚点/SC 来源修复、H-02 baseline 冻结、M-01…M-12、L-01/L-02 修复；`validate-decision-tensions` 0 error/0 HIGH；coverage `clause-uncovered` pass；CL-01/02/03 记录；Feature 083 `Draft → Planned` |
| analyze #2 | dispatched（2026-11-05 14:56 +08） | `974db180`；只读复核 H-01/H-02 关闭与 MEDIUM 处置 |

- analyze #1 的关键发现：H-01（plan.md Decision Tensions 不是 Constitution Check 的直接后继；4 条 expected_sacrifice 缺 `SC-NNN Source ↓`）；H-02（`coverage-baseline.txt` 缺失，clause coverage 结构上为 0）。MEDIUM 包括 guard 契约计数漂移、requirements line 306、GM-12 字面形态、模块路由/扫描范围、data-model 陈旧模块名、plan SU-02 E-13、checklist H-pass 裁定、feature-ref 计数/状态；LOW 包括 plan D4/D5/D6 与 SC-005/quickstart S9 计数。
- repair 的裁定：CL-01（失败类数归 requirements FR-024 四类）；CL-02（checklist 项是问题项，满足判定归 implement 的 checklist 豁免门）；CL-03（contracts 的 `md-none` 条款形态使 accountant 的 FR citation groups 为 0；不伪造，FR 覆盖由 DR-001 + tasks 人工核验；`coverage-baseline` 已冻结）。

## 阶段记录（analyze #2，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| analyze #2 | PASS（CRITICAL 0 / HIGH 0 / MEDIUM 0；7 LOW 不阻塞） | `974db180`；H-01/H-02 CLOSED；验证波 3 workers（1 confirm LOW / 1 downgrade / 1 reject）；7 LOW：L-1 evidence reproducibility、L-2 plan 计数分解式、L-3 feature-ref 7=6+1、L-4 DR-001 GR-05→GR-06、L-5 T036 twelve→11/12、L-6 tasks L61 FR 锚、L-7 design notes；SC-005 path-marker 修复 @8778d2bb（validator 0 error / 0 warning） |

## Implement 分段计划（2026-11-05）

- 单包 52 任务，按 ≤16 任务/段；为避开会话 120-turn 上限，实际按 **8 任务/段**：Part 1 T001–T008；Part 2 T009–T016；Part 3 T017–T024；Part 4 T025–T032；Part 5 T033–T040；Part 6 T041–T048；Part 7 T049–T052 + 集成/门。
- 测试预算：Part 1 起点一次全量基线（`env -u PYTHONPATH bash scripts/bash/run-tests.sh --names-out <spec>/baseline-failed.txt`，E2 row 写 `test-budget` 围栏）；中间段定向集 E3；review 后 closure 全量。
- 并发隔离：`skills/external/{create-skills,improve-skills,merge-skills,coaching-skills}`、`skills/internal/run-skills`、`shared/definitions/skill-reference-definitions.md` 是本特性交付面（A11），不是脏文件；083 预算校准的 agent/driver 路径不是本阶段交付面，MUST NOT 提交。
- plan constraint active：plan-owned artifacts（plan.md / data-model.md / contracts/ / quickstart / research / feature-ref）只允许 minor 修复；任何触碰以 `PLAN-EDIT:` 声明。

## 阶段记录（implement Part 1，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 1 (T001–T008) | done（U4 PASS，2026-11-05 15:18 +08） | `bfc18fe5` + `59ca4d36`；T001–T008 `[x]`；E2 baseline 24F/7157P/7S（`baseline-failed.txt` / `implement-part1-baseline.txt`）；定向 governance 830 passed；`test_expression_compatibility` 1 failed（已知 T038 面）；无 PLAN-EDIT |

- U4 说明：执行子代理在 120 回合内完成本段；两提交只含 feature 路径 + tasks.md + 证据；083/state 未提交。`shared/definitions/{flow-class,probe}-definitions.md` 出现与本段无关的脏改动，未提交、未还原，留待收尾归档分类。
- 下一段：Part 2 T009–T016。

## 阶段记录（implement Part 2，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 2 (T009–T016) | done（U4 PASS，2026-11-05 15:30 +08） | `c768bb82` + `588668a9` + `44bc7804`；T009–T016 `[x]`；targeted 823 passed；red 11F/16P → green 26P；skill-shape delta 5403→5942 / 5722→6200（rc 10 前后一致，EP-003 例外）；redline rc 0；sync-mirrors --check rc 0；唯一红 `test_expression_compatibility::test_c5` 归 T038 |

- U4 说明：执行子代理在 120 回合的最终验证处触顶（未发 `PART2-DONE`），但两个 feature 提交 + tasks/证据完整；驱动提交 `44bc7804` 收口。无 PLAN-EDIT。
- 下一段：Part 3 T017–T024。

## 阶段记录（implement Part 3 attempt 1，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 3 attempt 1 (T017–T024) | INCOMPLETE（120-turn cap at T020） | T017 red（`implement-part3-t017-red.txt`）、T020 red（`implement-part3-t020-red.txt`）；`test_mechanism_policy_{skill_wiring,ownership,guard,decidability}.py` 已写但未提交；tasks T017–T024 仍未勾；无 Part 3 commit |

- 处置：按有界分段拆为 3A（T017–T021）与 3B（T022–T024）；已写模块作为起点，不推倒重写。

## U5 停线（implement Part 3A，2026-11-05）

- **发现了什么**：Part 3A 的 T020 `test_sc003_complement_is_byte_identical_to_the_baseline` 红：工作树里有 22 个比较单元内路径不在 `data-model.md` GM-03 允许集内——083 预算校准 18 条（`skills/external/sdd-loop-driver/` 8 + `skills/internal/create-agent/templates/` 8 + `create-team` 1 + `run-agent` 1）、并发 skill-reference/sdd-project-setup 4 条（`coaching-skills/data-model.md`、`coaching-skills/references/prompt-templates.md`、`sdd-project-setup` ×2）、新增 `skills/external/ssh-utils/` 4 条；另有 083 自身 T017–T021 的未提交产物（owner 文档 / 测试模块 / 证据）。
- **为何吃重**：SC-003 是 083 的逐字节封闭集声明，只能覆盖 083 的交付面。083、skill-reference 的额外改动、sdd-project-setup 与 ssh-utils 都不是 083。继续在共享工作树里跑，只有两种结果：把无关路径塞进 083 允许集（污染声明），或提交/覆盖用户工作（越权）。
- **已产生的中间产物**：`bfc18fe5` / `59ca4d36` / `c768bb82` / `588668a9` / `44bc7804`（T001–T016 已提交）；T017–T021 的模块与红/绿证据未提交（`test_mechanism_policy_{skill_wiring,ownership,guard,decidability}.py`、`implement-part3*`）；E2 基线 24F/7157P/7S；状态脊本条。
- **可选处置**：(a) 从 `44bc7804` 建隔离 worktree，把 083 的未提交 feature 文件复制进去继续，主工作树的 083/并发改动保持不动（推荐）；(b) 先提交 083 与其它并发改动，再按新基线重审 083 SC-003 允许集；(c) 把 guard 改为只比较 083 已提交树（plan 修改，需重审 SC-003 口径）；(d) 停线移交。
- **当前状态**：`stalled` / `reentry-required`；未删除、未还原、未提交任何无关改动。

## U5 解除（2026-11-05，用户裁定「直接收编并发的修改」）

- **裁定**：并发 ssh-utils 改造（已完成）直接提交；083 预算校准与 skill-reference 一起收编；然后继续 083。
- **提交**：`62d1ab5d feat(ssh-utils)`（26 files）；`1acb97c1 chore(framework): calibrate the checkpoint and split budgets`（69 files）；`afd8115a feat(083): adopt the skill-reference wiring ...`（32 files）；`02bef714 fix(083): absorb the concurrent coaching files and close the SC-003 guard`（8 files）。
- **吸收面**：GM-03 行 19–20（coaching data-model / prompt-templates）加入允许集（in-unit 10）；guard 的 `feature_commits` 只选提交信息含 `083` 的提交，083/ssh-utils 作为吸收线不判违规；`registered_allowed_set` 按 `是/否` 列解析。`PLAN-EDIT` 已在 `02bef714` 提交体声明（classification=minor）。
- **验证**：ssh-utils 定向 70 passed；六机制/策略模块 66 passed；guard 9/9；无新失败。

## 阶段记录（implement Part 3A，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 3A (T017–T021) | done（U4 PASS，2026-11-05 17:08 +08） | `afd8115a` + `02bef714`；T017–T021 `[x]`；六模块 66 passed；guard 9/9；吸收面 10 条；E2 仍 24F/7157P/7S（无新失败） |

- U4 说明：初次的 1 个失败（guard 对工作树全量比较）是环境/比较源问题，不是 083 代码缺陷；用户裁定收编并发后，guard 改为按 `083` 提交选择比较集，其余工作线为吸收面。无 083 代码回退。
- 下一段：Part 3B T022–T024。

## 阶段记录（implement Part 3B，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 3B (T022–T024) | done（U4 PASS，2026-11-05 17:16 +08） | `6550ed80` + `094b23f3`；T022–T024 `[x]`；矩阵 30/30；targeted 100 passed / 1 known T038 c5（E2 baseline-internal）；无新失败 |

- U4 说明：执行子代理在 120 回合的提交处触顶；T022 已单独提交，T023/T024 与证据由驱动收口提交。无 PLAN-EDIT。
- 下一段：Part 4 T025–T032。

## 阶段记录（implement Part 4 attempt 1，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 4 attempt 1 (T025–T032) | INCOMPLETE（120-turn cap at T025/GR-01） | `implement-part4-red.txt`；`test_skill_reference_{grammar,matrix,consumers,command_surface,failures}.py` 已写未提交；`shared/definitions/skill-reference-definitions.md` 头部 GR-01 修复未提交；T025–T032 未勾；无 Part 4 commit |

- 处置：拆为 4A（T025–T028）与 4B（T029–T032）；已写模块作为起点。

## 阶段记录（implement Part 4A，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 4A (T025–T028) | done（U4 PASS，2026-11-05 17:29 +08） | `ac25bd58`；T025–T028 `[x]`；五个引用侧模块 30 passed / 1 expected T027 red（T035）；机制/策略邻居 40 passed；GM-12 四类失败名的形态/判据原文口径在 `implement-part4a-gm12-predicate-check.txt` 披露 |

- U4 说明：T027 的 mirror-path 断言在 T035 前必然红；这是任务序依赖，不是伪完成（失败文本逐条点名文件/行号，转绿路径明确）。
- 下一段：Part 4B T029–T032。

## 阶段记录（implement Part 4B attempt 1，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 4B attempt 1 (T029–T032) | INCOMPLETE（120-turn cap at T029 red evidence） | `test_skill_reference_failures.py` 已修改未提交；T029–T032 未勾；无 Part 4B commit |

- 处置：改用宿主 `general-purpose` 原生子代理（无 120 上限）重派 T029–T032；已写失败测试作为起点。

## 阶段记录（implement Part 4B，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 4B (T029–T032) | done（U4 PASS，2026-11-05 17:43 +08） | `fa563b0e`；T029–T032 `[x]`；targeted 890 passed / 4 failed（全部 E2 baseline-internal：T027 mirror-path→T035、coaching run/wiring、expression c5→T038）；new_failures=[]；mirrors/regen --check rc 0；无 PLAN-EDIT |

- U4 说明：general-purpose 原生子代理完成了 4 个任务并提交；T029 的 owner 文本断言是 GR-06 文档侧加固；owner 文档上一 attempt 的未提交改动已恢复为 HEAD（净零差异），未提交。
- 下一段：Part 5 T033–T040（含 T035 源路径改写与 T038 冻结哈希登记）。

## 阶段记录（implement Part 5，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 5 (T033–T040) | done（U4 PASS，2026-11-05 17:53 +08） | `88be0714`；T033–T040 `[x]`；targeted 980 passed / 3 failed（E2 baseline-internal：coaching run c1、coaching wiring c1、test_shared_reference_rewrite 029 张力）；T027/T038 转绿；mirrors/regen --check rc 0；无 PLAN-EDIT |

- 披露：T035 实测 7 处镜像串（非 8）；T038 coaching 键不在 069a 冻结清单，改用 `_retired_skill_register` replacement markers；T039 `framework-map.md` 是镜像源，已改源；Feature 079 STR-001 白名单 +2 个 083 消费方（红→绿）；删除空根目录 `tmp/`。
- 下一段：Part 6 T041–T048。

## 阶段记录（implement Part 6，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 6 (T041–T048) | done（U4 PASS，2026-11-05 18:15 +08） | `28662977`；T041–T048 `[x]`；targeted 64 passed；SC-003 `compared=575 unit=575 complement=566 allowed_in_unit=10 frozen_mismatches=0`；SC-001 14/14；SC-005 13/14（supporting，T052 如实写）；SC-002 detection 2/2 / false positives 0/2（harness 前后未分离，证据 §7）；no new failures；no PLAN-EDIT |

- 披露：SC-005 13/14（supporting，非 closure 门）；SC-002 的 harness 供策略值导致前后检出不可分离（判据数字与 GM-09 基线腿成立）；`reading_line` 形状变化仅 T050 消费；`test_gm03_allowed_set_parses_to_eight_in_unit_rows` 名字与 10 的断言不符（历史命名，未改 id）。
- 下一段：Part 7 T049–T052 + 集成（最后一段）。

## 阶段记录（implement Part 7 / 收口，2026-11-05）

| 段 | 状态 | 证据 |
|----|------|------|
| Part 7 (T049–T052 + 集成) | done（U4 PASS，2026-11-05 18:35 +08） | `6785e8de`；T001–T052 全 `[x]`；verification.md（九 SC：8 pass / 1 partial SC-005 13/14）；status Planned → Implemented；GATE-1…7 pass；E2 24F/7157P/7S 未新增；无 PLAN-EDIT |

- 披露：GATE-4 门禁文字「rows 1–8」陈旧（实际 10 = rows 1–8 + 19–20）；24 条无 083 提交的并发工作线路径在 raw diff 中已归因；GATE-2 的临时输出改落受制裁 `.specify/.tmp/`；SC-002 harness 不分离前后检出；SC-005 supporting partial 不阻断 GATE-8。
- 下一阶段：review（四段 + ARC）。

## 阶段记录（review，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| review | done（U4 PASS，2026-11-05 19:13 +08） | `875be2c7`（P0/P1 修复）+ `9685b58a`（review.md 405 行 + code-review.md 1046 行 + status）；四段 + ARC；findings F1–F10；P0 无；P1 全部修复或 decision（029 源路径张力记为 decision / 框架建议）；SC-005 13/14 supporting partial；SC-002 harness 局限记录；status Implemented → Ready for Review |

- U4 说明：执行子代理在 150 回合的收尾处触顶（未发 REVIEW-DONE），但 review.md / code-review.md / status 与 P0/P1 修复完整；驱动提交 `9685b58a` 收口。review 的 P1 建议（矩阵从 owner 派生、baseline 标注并发脏集、029 引用形式）作为框架改进项记录，不阻断本特性。
- 下一阶段：closure（全量 + audit + acceptance）→ U6 本地合并。

## 阶段记录（closure attempt 1，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| closure attempt 1 | BLOCKED（2026-11-05 19:43 +08） | `12c7af0b`；full suite 17F/7279P/7S（729.13s）；new=`tests/contract/test_client_guard_sweep.py::test_c57_shipped_text_adds_no_fresh_neutrality_violation`（083 T039 在 shipped `shared/definitions/framework-map.md:28` 写入 `Feature 083`）；fixed=8；closure checker `accept`（final 8/8，smoke 0）；audit `status=fail`（baseline 行缺 purpose/trigger/at；E3 命名 `<stage>-...-stage-status.jsonl` → stages=6 complete=0） |

- 处置：closure repair（C-57 一行修复 + 账本字段/命名修复 + in-slot-rerun 全量）；不是第三槽。
- 下一：closure repair → U6 合并。

## 阶段记录（closure repair，2026-11-05）

| 阶段 | 状态 | 证据 |
|------|------|------|
| closure repair | CLOSURE-DONE（2026-11-05 19:57 +08） | `6677b514`；C-57 修复（framework-map 去掉 shipped `Feature 083`）；in-slot-rerun 全量 16F/7280P/7S（771.89s）；new=0；8 fixed；C-57 缺席（17→16）；audit status=ok（baseline:1 closure:1 reruns=1、stages=6 complete=6）；acceptance accept（final 8/8、smoke 0） |

- 披露：`comm -23` 只能列 8 条 baseline 修复（C-57 从不在 baseline）；plan 阶段选用 scope-update 终态证据行。
- 结论：closure 通过；U6 本地合并。
