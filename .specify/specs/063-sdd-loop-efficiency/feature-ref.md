# Feature Reference: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Feature ID**: 058 | **Feature Name**: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）
**Requirement**: `.specify/specs/063-sdd-loop-efficiency/requirements.md`（演化特性，2026-10-20 绑定；058 状态保持 `Implemented`，不回退）
**Status at plan time**: 058 = Implemented（扩展切片：只记录本特性规划，不改变状态）

## FR → 设计映射

| FR | 设计落点 | 契约 |
|----|----------|------|
| FR-001 快车道替代 checklist，保留 analyze/review | efficiency-model §1；dispatch-recipes Recipe 4 裁决点 | FL-01/02/07 |
| FR-002 仅显式启用（[[STR-006]]） | efficiency-model §1.1；stage-prompts 入口块 | FL-01/08 |
| FR-003 七项准入判据与冻结区间 | admission-check.py；efficiency-model §1.2；窄任务模式仅用于准入、宽模式仅作仓库记账 | FL-03/08 |
| FR-004 准入记录字段与跳过标记 | data-model E1；efficiency-model §1.3 | FL-04 |
| FR-005 下游发布与收口标记 | stage-prompts 条件块；efficiency-model §1.4 | FL-05 |
| FR-006 失败回退 | efficiency-model §1.5；dispatch-recipes Recipe 4 | FL-06 |
| FR-007 analyze 不削弱 | efficiency-model §1.6 | FL-07 |
| FR-008 review 不削弱 | efficiency-model §1.6 | FL-07 |
| FR-009 定义落点与契约钉住 | efficiency-model + test_sdd_loop_driver_efficiency.py | FL-09 |
| FR-010 自应用排除 | plan/feature-ref/收尾证据 | FL-10, DI-07 |
| FR-011 两个全量槽位、按线作用域 | efficiency-model §2；audit-test-budget.py；E2 合并来源 | TB-01/02/07 |
| FR-012 中间阶段与 review 定向 | stage-prompts 测试预算块；efficiency-model §2.3；快车道跳过记 [[STR-008]]；docs-only 缩减字段集 | TB-05/06 |
| FR-013 定向集选择规则 | efficiency-model §2.3 + TB-05 `targeted-set-v1` 固定程序；空集升级 | TB-05/06 |
| FR-014 测试证据字段与名称级差集 | data-model E2/E3；audit-test-budget.py；stage-status 行 | TB-04/06/07 |
| FR-015 回归发现与归因 | stage-prompts 收口块；feature 流程 | TB-04 |
| FR-016 槽外例外/槽内重跑 | efficiency-model §2.5；audit-test-budget.py | TB-08 |
| FR-017 台账与 unknown | data-model E2；audit-test-budget.py；`stages=N complete=N`；merge_source | TB-07 |
| FR-018 环境失败不消耗槽位 | efficiency-model §2.6；audit-test-budget.py | TB-09 |
| FR-019 编排层实现 | 全部测试预算内容落 stage-prompts + 状态脊 | TB-10 |
| FR-020 只小修约束 | efficiency-model §3；stage-prompts 条件块 | PC-01/02/04 |
| FR-021 实质改动显式异常回传 | stage-prompts 条件块（[[STR-005]]） | PC-04 |
| FR-022 U4 分类与两分支 | audit-plan-changes.py；efficiency-model §3.3；`approved_baseline_commit` 初始 = E4 `plan_commit`，re-baseline 后更新 | PC-03/05/06/10/11 |
| FR-023 analyze 修复路由不变 | efficiency-model §3.4 | PC-07 |
| FR-024 active 登记与收口报告 | data-model E4；efficiency-model §3.5 | PC-01/08 |
| FR-025 显式排除与设计代价 | efficiency-model §3.6；plan Complexity Tracking | PC-09 |
| FR-026 stream-json 默认 + raw stream | stage-runner.sh；dispatch-recipes Recipe 2 | PD-01/10 |
| FR-027 增量派生实时日志 | derive-live-log.py；efficiency-model §4.2 | PD-02 |
| FR-028 哨兵只认终止结果文本 | derive-live-log.py 收口；watch-model §3 | PD-03 |
| FR-029 watcher 只做可见性 | watch-model §3–§4（判定不变） | PD-04 |
| FR-030 降级与 [[STR-004]] | stage-runner.sh；efficiency-model §4.4 | PD-05 |
| FR-031 nohup 双拓扑 | dispatch-recipes Recipe 3/5；stage-prompts | PD-06 |
| FR-032 四件套、--once、重入 | watch-model §9；stage-prompts 重入程序 | PD-07 |
| FR-033 watcher 证据面与自测 | watch-target.sh（--raw-stream + 自测） | PD-08 |
| FR-034 长轮询、无 sleep 回合 | watch-model §4–§5（不变） | PD-09 |
| FR-035 证据保留、无新服务 | 产物命名与边界 | PD-09 |
| FR-036 确认门不变 | SKILL.md Boundary / DISPATCH | DI-01 |
| FR-037 独立校验不变 | stage-prompts U4 程序 | DI-02 |
| FR-038 卡死处置不变 | stage-prompts U5 程序；[[STR-007]] 三类场景行为基线（`ba2a18db` 冻结）；driver-stall-fixture 观测（exit_code 双字段、initial_retries=0） | DI-03 |
| FR-039 质量门不降低 | 契约与默认值（快车道默认关） | DI-04/08 |
| FR-040 交付面与镜像 | 交付清单；`sync-mirrors --only skills/external/sdd-loop-driver`（本对零 drift + 零 NEW drift；含 references/cli） | DI-05 |
| FR-041 契约测试 | 既有测试有意更新 + 新契约文件（含 CP） | DI-06 |
| FR-042 行为夹具 (a)–(e) | 测试落点见下表 | DI-06 |
| FR-043 编排层优先 | plan 结论：四项均在编排层 | DI-09 |
| FR-044 CLI 档案集合与落点 | references/cli/README + 五份档案；无档案先建骨架 | CP-01/05/10 |
| FR-045 七维内容与 known/unknown | references/cli/README schema；V-CP-1…V-CP-4 | CP-02/03/09 |
| FR-046 SKILL.md CLI Capability Profiles 节 | SKILL.md H2 [[STR-010]]；单一 owner = references/cli/ | CP-04 |
| FR-047 probe + feedback 观测点 | E8 CLI observations；feedback marker [[STR-009]]；最小 Probe Object | CP-05/06/07 |
| FR-048 不改变阶段行为 | CP-08；E6 当前阶段命令形态不变 | CP-08 |
| FR-049 交付、镜像与契约测试 | references/cli + docs + CP 契约 + 最小 Probe Object | CP-07/10, DI-05/06 |

## SC → 验证映射

| SC | 验证方式 | 证据落点 |
|----|----------|----------|
| SC-001 | admission-check 对中型/缺件夹具；契约钉字段完整性 | 单测 + `test_fl_04` |
| SC-002 | 中型夹具录取、大夹具/判据失败拒绝（自动脚本）；阶段序列由编排演练 trace 证明（当前固定夹具集为 1 个中型 + 1 个大型；trace 在 verification.md 如实标注） | 单测 + `test_fl_02_admission_point_and_sequence_policy` + verification.md trace |
| SC-003 | 台账审计：两槽位、槽外例外可见 | `test_audit_test_budget.py` + trace |
| SC-004 | 集成回归注入：baseline → 注入失败 → final `comm -13` 非空 | `test_sdd_loop_efficiency_regression.py` |
| SC-005 | E3 字段完整性；授权跳过记 [[STR-008]] 且不入分母；`not-run-docs-only` 按缩减字段集判完整；缺 stage-status 行计入分母；审计输出 `stages=N complete=N`；缺证据报 unknown | 单测 + `test_tb_06/07` |
| SC-006 | plan 改动分类；未声明/实质 → 门失败；无静默重审；requirements 变更后按 PC-11 re-anchor | `test_audit_plan_changes.py` + `test_pc_*` + trace |
| SC-007 | 事件→派生行延迟 ≤120s（无事件区间不适用）；无伪造行；无独立 sleep 回合 | `test_derive_live_log.py` + 契约 PD-02/PD-09 |
| SC-008 | 脱离存活 + `--once` 接管不重派：存活/降级由集成测试自动证明；新会话接管由 trace 证明 | `test_sdd_loop_efficiency_runner.py` + trace |
| SC-009 | 非终止/终止/派生失败三类哨兵用例 | 单测 + self-test |
| SC-010 | 确认门/独立校验条款测试；卡死处置以 [[STR-007]] 行为基线（`ba2a18db`）录制并由驱动侧可执行夹具（initial_retries=0、exit_code 双字段、反转录）在收口归一化重放比较，零差异为通过；名称级基线不得冒充行为基线 | 契约测试 + driver-stall-fixture + verification.md（自动夹具/录制 trace 如实标注） |
| SC-011 | 不支持 stream-json 的 stub CLI → 降级标记、无伪 DONE | runner 集成测试 |
| SC-012 | 全量名称级基线（implement 起点冻结）与改动后名称级差集为空；本对镜像零 drift，全部镜像对相对冻结基线零 NEW drift（既有 DIFF 作为已披露例外）；既有契约绿或有意更新 | `run-tests.sh --names-out` + `sync-mirrors.py --check` |
| SC-013 | 本特性运行 trace 检索 checklist/analyze/review 产物；快车道记录数 0 | verification.md + `test_fl_10` |
| SC-014 | 100% 派发有档案与 U2 查档记录；五份档案在位、known/unknown 显式；无档案派发 0 | `test_cli_profile_record.py` + CP 契约 + E6 记录 |
| SC-015 | 100% 观测事件有档案 provenance 与一条 `[[STR-009]]<cli>` 反馈；standalone 仍更新档案并报告；无证据 known 为 0 | `test_cp_03/06/07` + feedback `--contains` |
| SC-016 | 档案更新导致的哨兵/判定/退出码/确认门/deadline 变化为 0；契约钉住 H2/五档案/七维/marker/最小 Probe Object；compile-embeds 与本对镜像零漂移 | `test_cp_04/08/10` + `probe-utils.py` + `sync-mirrors.py` |

## 行为夹具落点（FR-042）

| 夹具 | 测试 |
|------|------|
| (a) 中型夹具走快车道、跳过 checklist、analyze/review 执行 | admission 单测 + 录制 trace（S7） |
| (b) 槽外全量无例外被检出 | `test_audit_test_budget.py::test_out_of_slot_without_exception_fails` |
| (c) 下游实质 plan 改动被 U4 抓获 | `test_audit_plan_changes.py::test_undeclared_plan_change_flagged` + PC-06 契约 |
| (d) 驱动中途退出不中断脱离阶段且重入可核验 | `test_sdd_loop_efficiency_runner.py::test_local_nohup_survives_parent_exit` |
| (e) implement 起点后注入回归被最终全量发现 | `test_sdd_loop_efficiency_regression.py::test_injected_regression_found_by_name_diff` |

SC-010 的驱动侧卡死夹具不在 FR-042(a)–(e) 之列：它由 `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` 提供（stub runner + 真实 watcher + 文档化 U4/U5 程序），基线录制与收口归一化重放见 `verification.md`；`initial_retries=0`、`exit_code={watcher,runner}`，禁止判定表转录。

## 交付面清单

```text
skills/external/sdd-loop-driver/SKILL.md                          # 新增 Efficiency Optimizations 与 CLI Capability Profiles 两节 + References/脚本清单
skills/external/sdd-loop-driver/references/efficiency-model.md    # 新增：四项优化唯一 owner
skills/external/sdd-loop-driver/references/dispatch-recipes.md    # runner/admission/budget/plan 接线
skills/external/sdd-loop-driver/references/stage-prompts.md       # 条件提示词块（快车道/预算/plan/PLAN-EDIT/state_spine_path）
skills/external/sdd-loop-driver/references/watch-model.md         # 进度/降级/raw 证据；判定不变
skills/external/sdd-loop-driver/references/cli/README.md          # 新增：CLI 档案 schema 与观测程序 owner
skills/external/sdd-loop-driver/references/cli/qodercli.md        # 新增：qodercli 已知能力/缺陷
skills/external/sdd-loop-driver/references/cli/claude.md          # 新增：骨架（known/unknown）
skills/external/sdd-loop-driver/references/cli/codex.md           # 新增：骨架（known/unknown）
skills/external/sdd-loop-driver/references/cli/opencode.md        # 新增：骨架（known/unknown）
skills/external/sdd-loop-driver/references/cli/hermes.md          # 新增：骨架（known/unknown）
skills/external/sdd-loop-driver/scripts/stage-runner.sh           # 新增：参数化 runner
skills/external/sdd-loop-driver/scripts/derive-live-log.py        # 新增：stream-json 派生
skills/external/sdd-loop-driver/scripts/admission-check.py        # 新增：快车道准入
skills/external/sdd-loop-driver/scripts/audit-test-budget.py      # 新增：预算台账审计
skills/external/sdd-loop-driver/scripts/audit-plan-changes.py     # 新增：plan 改动机械判定
skills/external/sdd-loop-driver/scripts/watch-target.sh           # 扩：--raw-stream、自测修正
docs/reference/skills/sdd-loop-driver.md                          # 用户文档页
tests/contract/test_sdd_loop_driver_skill.py                      # 有意更新：H2 集合 + C-4
tests/contract/test_sdd_loop_driver_efficiency.py                 # 新增：FL/TB/PC/PD/DI/CP 条款
tests/unit/test_admission_check.py                                # 新增
tests/unit/test_derive_live_log.py                                # 新增
tests/unit/test_audit_test_budget.py                              # 新增
tests/unit/test_audit_plan_changes.py                             # 新增
tests/unit/test_cli_profile_record.py                             # 新增（CLI 档案 schema/观测/marker）
tests/integration/test_sdd_loop_efficiency_runner.py              # 新增（脱离存活/降级）
tests/integration/test_sdd_loop_efficiency_regression.py          # 新增（名称级回归）
tests/fixtures/sdd_loop_efficiency/                               # 新增夹具（spec/stream/stub-cli/repo）
tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py        # 新增（驱动侧卡死观测夹具）
.specify/memory/features/058.md                                   # 扩展规划记录（状态不变）
.specify/memory/features.md                                       # Last Updated 注记（状态不变）
```

**不触碰**：`templates/commands/*`、`skills/internal/{create-plan,create-tasks,implement-feature,analyze-artifacts,review-sdd-process}/*`、watch-target 判定状态机/退出码、任何 `/speckit.*` 命令模板、probe Handler/HandlerBinding 与编译 Wrap-up 面。唯一注册表改动 = 新增最小 Probe Object 行 `skill-sdd-loop-driver-wrapup`（`skill-wrapup` / `skill:sdd-loop-driver` / `wrap-up`）；不新增 Probe Class、Handler 或 Binding。

**基线证据制品**：`notes/stall-behavior-baseline.json`（[[STR-007]]）由实现期录制，属 SC-010 证据，不计入上方 31 项交付面计数。CLI 档案属交付面内的技能文档，不计为新的运行时制品。

## 基线记录（2026-10-20 实测）

- **既有契约**：`tests/contract/test_sdd_loop_driver_skill.py` = 21 passed / 2 failed（文件共 23 个测试函数）；失败为 C-12 与 C-18（镜像漂移），本特性以源→镜像同步修复。
- **镜像**：`sync-mirrors.py --check --only skills/external` 退出码 2，68 个 DIFF 跨 12 个技能目录；本特性拥有的 sdd-loop-driver 占 3 个（SKILL.md、references/dispatch-recipes.md、references/watch-model.md），其余 11 个目录的完整清单见 `research.md` B-2——该清单即镜像冻结基线，零 NEW drift 以它为比较对象。
- **卡死行为基线（SC-010）**：冻结提交 `ba2a18db`；实现首个行为面提交之前录制 `notes/stall-behavior-baseline.json`（[[STR-007]]），覆盖超时 / 重试上限 / 伪完成三类处置元组；本 plan 期该基线尚不存在，由实现期录制，收口以同一组夹具归一化重放比较。名称级测试失败基线只服务 SC-012。
- **watcher 自测**：12 passed / 4 failed（macOS：无 `/proc` 的 pid-reuse、zombie；`sleep 3` 时序的 manifest；`pgrep -c` 平台差异）。本特性扩展自测时一并修正为跨平台或显式跳过。
- **规格校验**：`validate-requirements.py` = exit 0；plan-repair-2 的 requirements delta 后实测 382 lines / 65 definition rows / 10 shared strings（requirements-repair 第 2 轮为 313 / 56 / 8；plan 初测为 301 / 56 / 6，作历史对照）。
- **测试运行器**：`run-tests.sh --names-out` 探针 = 7 passed、名单 0 行；全量名称级基线在 implement 起点按本特性预算规则捕获。
- **Python**：`python3` 3.9.6（系统）、`python` 3.14.6（pytest）；新脚本按 ≥3.8 编写。
- **CLI 可用性（2026-10-20 实测）**：`qodercli` 1.1.73 在 PATH，`--print` / `--output-format` / session 子命令可用；`codex` 与 `opencode` 在 PATH；`claude` / `hermes` 未在 PATH。档案骨架对未验证项标 `unknown`，实现期由 `--help` 与版本探测填充。
- **probe 注册表（2026-10-20 实测）**：`probe-utils.py --action probes --validate` exit 0；`--action compile-embeds --check` 74 units zero drift；`--action probes --reconcile` 报 `embed without probe object: skill:sdd-loop-driver` 与 `skill:sdd-project-setup` 两个既有缺口。本特性用最小 Object 修复前者，后者保留为既有例外并披露。
- **需求方报告的基线**：一次特性运行全量 6 次、checklist 约 8 分钟——来自 brief 的 dated record，本 plan 未复测，不据此宣称提速百分比。

## 显式排除（Out of Scope）

- 框架命令内部（implement/review/analyze/plan 等）的硬执行；plan 约束仅为编排层纪律。
- 大型特性快车道、快车道设为缺省、跳过 analyze/review/独立校验。
- 改变哨兵字面量、watcher 判定状态机或既有退出码。
- 新增常驻服务、守护进程、外部依赖、模型 API 或网络传输。
- 自动 push、自动合并远程分支、自动外传反馈或运行数据。
- 预算外自动追加全量运行（槽外必须显式例外）。
- 重新设计阶段命令内部测试策略。

## 自应用声明

063 自身走完整阶段链：`checklist`、`analyze`、`review` 均必经；本特性运行 MUST NOT 产生快车道记录。该声明在 requirements FR-010、本 plan、并将在 verification.md 的收尾证据中再次核验（SC-013）。CLI 档案机制从实现完成后的后续派发生效；本次运行对 qodercli 的观测只能作为 `qodercli.md` 的 dated 种子证据，MUST NOT 以档案更新改变本运行任何阶段的命令或判定。
