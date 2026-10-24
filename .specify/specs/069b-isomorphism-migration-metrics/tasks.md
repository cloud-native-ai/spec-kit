# Tasks: 同构映射、迁移兼容与度量仪器（Isomorphism Map, Migration Compatibility & Measurement Instruments）— Feature 069 / Slice 069b

**Requirement ID**: 069b（Feature 069 的第二个切片；不新建 Feature ID、不新增注册行）
**Requirement Key**: `069b-isomorphism-migration-metrics`
**Branch**: `069b-isomorphism-migration-metrics`
**Related Feature**: Feature 069 执行/表达二元分类与文档型 SDD 同构，状态 Planned（切片复用同一注册行；`069a = Implemented` / `069b = 进行中`）
**Input**: Design documents from `.specify/specs/069b-isomorphism-migration-metrics/`
**Prerequisites**: plan.md（技术路线、Mirror Obligations、Test Strategy 基线）、requirements.md（14 FR / 5 SC / 3 STR）、research.md（R1–R15）、data-model.md（E1–E10）、contracts/ ×4（51 条款：`isomorphism-map.md` 14 / `ledger-reconciler.md` 16 / `migration-distribution.md` 11 / `measurement-instruments.md` 10）、quickstart.md（7 场景）、feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 为测试强制原则——纯函数/工具 MUST 有单测、集成/契约测试 MUST 覆盖跨面接口；本切片交付可执行引擎扩展与 owner 文档章节，含运行时判定代码，非 template-only，故 Principle IV 的 Partial 豁免不适用。8 个新测试文件（6 契约 + 2 单元）一律红先：先跑出失败并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`，再进入对应实现行。)

**Tests**: 红先证据的落点是 `.specify/specs/069b-isomorphism-migration-metrics/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败测试名基线的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。测试解释器只有 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（见 § Environment Prerequisites）。

**Organization**: 按用户故事组织——US1（同构映射与四类边界成为可核对结构）、US2（未刷新项目行为不变、刷新后载荷同包到达、名字级零新增失败）、US3（台账对账、委托核验、六面指针与三项度量仪器可机械核对）。三个故事在 requirements 中同为 **Priority P2**（沿用父标签，不重排）：US1 是切片头号交付物、可独立演示，故 MVP = US1；US2 与 US3 各自独立可测，按 § Dependencies 的串行理由排在其后。Setup 冻结改前基线与条款覆盖基线；无 Foundational 阶段（三个故事写目标不重叠，唯一共享前提已在 Setup 落盘，见 § Dependencies）；Polish 收口镜像与副本、文档同步、全量回归、SC 证据与特性登记。

## Definition of Done (DoD)

- DoD-1: 全部任务行行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/069b-isomorphism-migration-metrics/verification.md` 的 `deferred_tasks=`。
- DoD-2: 两个编辑面按契约交付——`shared/definitions/flow-class-definitions.md`（同构映射 8 行 × 3 面 = 24 格、每行强制门禁与强制状态、四类不可同构边界、台账版本声明、P1–P4 指针收敛）与 `scripts/python/flow-class-check.py`（新增 `isomorphism` / `delegation` / `faces` 三动作，扩展 `check` 的 `ledger-truncated` / `coverage` / `red_kind`）；`--action lookup` 输出字段、降级标签与退出码，以及 069a 的八个 finding kind 全部不变。
- DoD-3: 4 份契约共 51 条款（14 + 16 + 11 + 10）每条恰被一个任务行 `[green:]` 认领一次，`account-clause-coverage.py` 报告 claimed = 51；条款认领顺序在每个契约内单调递增。
- DoD-4: 8 支新测试（`test_isomorphism_map` / `test_ledger_reconciliation` / `test_delegation_classes` / `test_expression_faces` / `test_migration_distribution` / `test_measurement_instruments` / `test_isomorphism_checker` / `test_reconciler_extensions`）全绿；相对 `notes/test-baseline-contract.txt` 零**新增**失败 nodeid（既有红不修、不掩盖；计数与名单的唯一所有者是该文件，本文件不重述数字）。
- DoD-5: plan.md § Mirror Obligations 逐行落地——`shared/definitions/flow-class-definitions.md` 与 `scripts/python/flow-class-check.py` 各自的 `.specify/` 镜像同字节，`sync-mirrors.py --check` 相对改前基线零新增差异，`regen-command-copies.py --check` 继续 `OK`（证明 `templates/commands/` 零改动）；零手改镜像、零手写副本。
- DoD-6: 零新增 `/speckit.*` 命令、零新增门禁面、零项目侧类别存储或读取点、零新采集器；三个新动作与 `check` 未被登记为任何命令模板或技能的调用点（`shared/workflow/expression-gates.md` § 调用点表零改动）。
- DoD-7: `verification.md` 逐条列 `- **SC-001**` … `- **SC-005**` 的状态、命令、输出摘要与证据指针；无来源的量记 `not-evaluated` + reason，不记 0、不记达成；`not-evaluated` 不得出现在 SC 状态位（SC 状态取 `verification-log-template.md` 的五值词表）。
- DoD-8: 三个客户项目快照按事先冻结样本跑测，`comm -13` 为空，或按契约记 `not-evaluated` + reason；原始项目与其工作树零修改（`git archive` 只读）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/069b-isomorphism-migration-metrics/tasks.md` exit 0（0 error / 0 warning）。
- GATE-2: 跨产物一致 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/069b-isomorphism-migration-metrics --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定并记录）。
- GATE-3: 分解规模合法 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/069b-isomorphism-migration-metrics/requirements.md --tasks .specify/specs/069b-isomorphism-migration-metrics/tasks.md` 结论为 `proceed`（task rows ≤ 40）。
- GATE-4: 测试零新增失败 — check: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract tests/unit -q --tb=no -p no:cacheprovider` 的失败 nodeid 排序后与 `notes/test-baseline-contract.txt` 做 `comm -13` 为空（名字级，非计数级）。
- GATE-5: 镜像与副本零漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0，且与 `notes/pre-change-measurements.md` 的改前基线比较零新增差异。
- GATE-6: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics` 输出 claimed = 51 且 uncovered beyond baseline = 0。
- GATE-7: 结构面零新增违规 — check: `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` 的 `violations` 计数与 kind 集合相对改前基线零新增。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/069b-isomorphism-migration-metrics/tasks.md` 返回 0。
- GATE-9: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-5]\*\*' .specify/specs/069b-isomorphism-migration-metrics/verification.md` 返回 5。

## Environment Prerequisites

<!-- 本节的探测结论是单一落点：任何任务行只引用本节，不复述环境判定。 -->

- pytest 解释器: **available（仅 profiles/.venv）** — probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --version` → `pytest 9.1.1`；本仓 `.venv/bin/python -m pytest --version` → `No module named pytest` @ 2026-10-25; affected: T003、T009、T013、T014、T015、T016、T017、T018、T023、T026。
- git（`archive` / author date / `show`）: **available** — probe: `git log --diff-filter=A --format='%h %as' -- .specify/specs/069b-isomorphism-migration-metrics/requirements.md` → `f0df3d0b 2026-10-24` @ 2026-10-25（另测 `git log -1 --format=%as -- …requirements.md` → `2026-10-25`：它取最近一次触及，**不可**作首次提交仪器）; affected: T012、T013、T022。
- Go 工具链（`xuanji-cli` 快照套件）: **available** — probe: `go version` → `go version go1.27.2 darwin/arm64` @ 2026-10-25; affected: T012。
- `specify` CLI（快照刷新入口）: **available，但预装包不是本切片发行包** — probe: `which specify` → `/Users/liuqiming.lqm/project/profiles/.venv/bin/specify`；实测其包内 `specify_cli/shared/definitions/` 无 `flow-class-definitions.md`、`specify_cli/shared/workflow/` 无 `expression-gates.md` @ 2026-10-25; affected: T012（MUST 由本切片源码构建 wheel → `--target` 暂存 → 用 profiles venv 解释器 + `PYTHONPATH` 运行 `specify init`；预装包不可作刷新入口；构建 / 安装不可执行时按契约记 `not-evaluated`）。
- 三个客户项目快照: **present 且未刷新** — probe: 逐项目 `git -C <project> rev-parse --short HEAD` + `test -f <project>/.specify/shared/definitions/flow-class-definitions.md` → 三者 `owner=no`（详见 `notes/migration-samples.md` 冻结表） @ 2026-10-25; affected: T012。
- 容器 / 镜像仓库 / 集群 / 外网: **none** — 本切片的检查全为本地文件、`git` 与本地 pytest；无构建、无拉取、无网络 @ 2026-10-25; affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本切片只有 Setup 与 Polish 各两条满足该条件；用户故事内的红先行共用 `notes/red-first-evidence.md` 这一追加落点（共享 sink 即同写目标），故不标 `[P]`。
- **[Story]**: 用户故事标签（`[US1]`…`[US3]`），只在用户故事阶段的任务行出现；Setup 与 Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**：绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析。51 条款分区：`isomorphism-map.md` C-1…C-7→T006、C-8…C-12→T007、C-13…C-14→T008；`ledger-reconciler.md` C-1…C-7→T019、C-8…C-10→T020、C-11…C-13→T021、C-14…C-16→T023；`migration-distribution.md` C-1…C-5→T011、C-6…C-9→T012、C-10→T024、C-11→T029；`measurement-instruments.md` C-1…C-7→T022、C-8…C-10→T023。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `shared/definitions/flow-class-definitions.md`、`scripts/python/flow-class-check.py`、`tests/contract/`、`tests/unit/`。
- **生成面（禁止手改）**: `.specify/shared/` 与 `.specify/scripts/` 镜像（`sync-mirrors.py` 投影）、每工具命令副本（`regen-command-copies.py` 生成）。
- **证据落点（本特性）**: `.specify/specs/069b-isomorphism-migration-metrics/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`、`verification.md`，以及既有的 `notes/test-baseline-contract.txt`、`notes/expression-baseline.md`、`notes/migration-samples.md`。
- **禁改面**: `templates/commands/`、`skills/`、`shared/workflow/expression-gates.md`（六面与算子表 owner，069a 已交付）、`.specify/specs/069a-flow-classification-docs-gates/`、`.specify/specs/069-execution-expression-sdd/`（父规格）、`.specify/specs/062-humanize-command/`、`067-loop-efficiency-hardening/`、`068-exec-quant-feedback-channel/`、`src/specify_cli/`。
- **被否决备选（MUST NOT 创建）**: `shared/definitions/isomorphism-map.md` 是 research R1 明确否决的方案（会产生第二个分类 owner）；映射与边界的唯一载体是 `shared/definitions/flow-class-definitions.md`。`contracts/isomorphism-map.md` 是本切片的**契约文档**（形态与判据），不是映射副本，两者不可混淆。`pre-analyze-check.py` 对该路径的 2 条 `missing-path` advisory 是这条被否决备选的正常残留，**不靠创建文件消除**。

## Measured Premises (re-measured at generation time 2026-10-25, HEAD `02abd56c`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 流程单元规模（台账分母与 `LEDGER_FLOOR`） | `ls templates/commands/*.md \| wc -l`；`ls -d skills/external/*/ \| wc -l`；`ls -d skills/internal/*/ \| wc -l`；`comm -12 <(ls skills/external) <(ls skills/internal)` | 27 / 14 / 37 → 技能 51，合计 78；`comm -12` 空输出（零同名冲突） |
| 契约条款数（逐文件） | `grep -ohE '^\- \*\*C-[0-9]+\*\*' .specify/specs/069b-isomorphism-migration-metrics/contracts/*.md \| wc -l` | 51（`isomorphism-map` 14 / `ledger-reconciler` 16 / `migration-distribution` 11 / `measurement-instruments` 10），全部 `- **C-N**` 形态 |
| FR / SC / STR 计数 | `grep -cE '^\- \*\*FR-[0-9]+\*\*' .specify/specs/069b-isomorphism-migration-metrics/requirements.md`；同法 SC；`grep -cE '^\| \`STR-[0-9]+\`' …requirements.md` | 14 / 5 / 3 |
| 8 个新测试文件当前状态 | 逐个 `test -e`（`tests/contract/test_isomorphism_map.py` 等 8 个） | 8/8 ABSENT（红先的前提） |
| owner 两章节当前状态 | `grep -c '^## 同构映射' shared/definitions/flow-class-definitions.md`；同法 `^## 不可同构边界`；`grep -n '069b 承接'` | 0 / 0；`069b 承接` 命中 12 行（4 行正文/表内说明 + 8 行台账 `notes`），其中 `由 069b 承接` 3 行（`:19` `:35` `:88`） |
| 引擎动作集当前状态 | `grep -n 'choices=("check", "lookup")' scripts/python/flow-class-check.py` | 命中 `:665`——当前只有 `check` / `lookup`，三个新动作不存在 |
| 被否决备选路径 | `test -e shared/definitions/isomorphism-map.md` | ABSENT（MUST 保持 ABSENT） |
| 台账检查当前基线 | `python3 scripts/python/flow-class-check.py --action check --format json` | `units = 78`、`findings = []`、exit 0 |
| 镜像与命令副本基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | 六对 `ok`（`scripts/` 112 files、`shared/` 55 files 等）+ 命令副本 `OK`，两次均 exit 0 |
| 结构面基线（非零） | `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | exit 0，`violations = 3`：`broken-link` 2（`docs/concepts/overview.md`）+ `note-frontmatter` 1（`docs/notes/type-follows-stage-misclassification.md`） |
| 契约套件名字级基线 | `wc -l .specify/specs/069b-isomorphism-migration-metrics/notes/test-baseline-contract.txt` 与文件头判据行 | 文件在盘（冻结于 `f0df3d0b`，2026-10-25 采集）；**失败名单与计数以该文件为唯一所有者**，本文件不重述。文件头记录的命令只跑 `tests/contract`，而 GATE-4 / T026 比对 `tests/contract tests/unit`——2026-10-25 analyze 实测 unit 侧 0 失败（814 passed），当前两侧等价；T003 的重采命令已扩到两侧，重采后由该文件同时拥有两侧名单 |
| 覆盖基线当前状态 | `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics` | `status: ok`（基线已于 2026-10-25 analyze 前置修复时冻结，base-sha `9bfe53de`，495 条基线内、0 beyond-baseline）；`claimed clauses = 51`、`FR universe: 14 / FR claimed: 14 / FR uncovered: 0`；T002 在实现起点按 never-cache 规则重采，不与实现期台账抢同一份口径 |
| 前置门禁（tasks 之前）| `pre-analyze-check.py --stage requirements|plan`；`decomposition-check.py --mode plan` | `decision=pass` errors=0、advisories=10（8 条指向尚未创建的测试文件 + 2 条指向被否决备选路径）；`decision=proceed`（fr_count=14） |
| 三个客户快照 | 逐项目 `git -C <project> rev-parse --short HEAD` / `branch --show-current` / `test -f .specify/shared/definitions/flow-class-definitions.md` | `3f68b62@master`、`a0c476d@xuanji/develop`、`a2fad18@main`，三者 `owner=no`（与 `notes/migration-samples.md` 冻结值一致） |

**Generation-time premise corrections（实测优先于派发提示）**

- 派发提示称「7 支新测试（5 契约 + 2 单元）」；实测 plan.md §4 / feature-ref.md §4 一致列出 **8 个**测试文件（6 契约 + 2 单元：`test_isomorphism_map` / `test_ledger_reconciliation` / `test_delegation_classes` / `test_expression_faces` / `test_migration_distribution` / `test_measurement_instruments` + `test_isomorphism_checker` / `test_reconciler_extensions`）。本文件按实测 8 编排（T004、T005、T010、T014–T018），该差异属提示侧的继承前提偏差。
- 派发提示提到「若 plan 中存在 `isomorphism-map.md` 备选路径」；实测该路径在 plan（§ 门禁实跑）与 research（R1 § 被否方案）中均以**被否决备选**出现，唯一映射载体是 `shared/definitions/flow-class-definitions.md`。本文件在 § Path Conventions 与 T005 明确该否决，不新增第二份 map 文件，也不为消除 advisory 而创建它。
- plan.md § 门禁实跑粘贴的 `advisories=9` 与紧随其后的正文「10 条 advisory」不一致；本节实测 requirements 与 plan 两阶段均为 `advisories=10`（8 测试文件 + 2 被否决备选）。plan 属冻结的上游产物，本文件只记录差值、不改写。
- 派发提示称任务数上限 40；`decomposition-check.py` 的 `TASK_CEILING` 同为 40，本文件任务行合计 29。
- **2026-10-25 analyze 轮修正（三处，均为可测性缺陷，不是口径放宽）**：① **解析侧反空真下限** 由「期望行数 78」改为由清单侧 floor 推导的 `⌊(27+51)/2⌋ = 39`——78 会让「删一行」同时触发 `ledger-truncated`，使 SC-003 的两种注入都落 `parse-failure`（两红不可区分），并破 069a 的 `test_missing_ledger_row_reports_missing`（77 行，断言 `kinds ⊆ EIGHT_KINDS`，本切片不得改写该断言）；② **条款覆盖基线**在 analyze 阶段冻结（`coverage-baseline.txt`，`status: ok` / 0 beyond-baseline），T002 改为实现起点的重采行；③ **`wall_clock` 起点仪器**改为 `git log --diff-filter=A --format='%h %as' -- requirements.md`（实测 `f0df3d0b 2026-10-24`）——原 `git log -1 --format=%as` 取最近一次触及，2026-10-25 实测返回 `2026-10-25`。

## Requirement Coverage Map

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T004、T005、T006 |
| FR-002 | T005、T006 |
| FR-003 | T005、T007 |
| FR-004 | T007 |
| FR-005 | T005、T007 |
| FR-006 | T010、T011 |
| FR-007 | T010、T012 |
| FR-008 | T010、T011 |
| FR-009 | T005、T006、T019 |
| FR-010 | T014、T018、T019 |
| FR-011 | T014、T019 |
| FR-012 | T015、T020 |
| FR-013 | T016、T021 |
| FR-014 | T017、T022、T023 |
| SC-001 | T006、T007、T009 |
| SC-002 | T012、T013 |
| SC-003 | T019、T023 |
| SC-004 | T019、T027 |
| SC-005 | T021、T023 |

T001 / T002 / T003（改前基线与覆盖基线）、T008（`--action isomorphism` 动作本体，其契约归属由 `[green:]` 表达）、T024 / T025 / T026 / T028 / T029（镜像、文档、回归、登记与终局门禁）共 9 行是流程与证据行，按设计不直接映射 FR/SC；其余 20 行全部出现在上表（T020 / T021 既是引擎动作本体、也是 FR-012 / FR-013 的覆盖行；T013 / T023 是故事转绿取证行、同时承载 SC 覆盖）。`[[STR-001]]` / `[[STR-002]]` / `[[STR-003]]` 一律按 requirements.md § Shared Strings 解析（语义 owner 是父规格），实现与测试不得在引擎输出之外内联类别字面量作为键名。

**Task Distribution**: Setup 3 · US1 6 · US2 4 · US3 10 · Polish 6 · 任务行合计 29。

**Assumptions（本轮自行裁决并记录，`/speckit.clarify` 可推翻）**

- **A-1 069a 单元测试夹具的最小补齐**：新增 `ledger-version-missing` 后，069a 的 `tests/unit/test_flow_class_check.py` 夹具（`_render_owner` 生成的 owner 无 `**台账版本**`）会额外命中该 kind，从而破掉 `kinds <= set(EIGHT_KINDS)` 与 `set(kinds) == {"row-malformed"}` 两条既有断言。故 T019 **只给该夹具构建器补一行版本声明**（补的是新判据要求的输入），**不改任何断言、不改判据语义**；feature-ref §3「不修改 069a 的 8 个测试文件」按「不改其判据与断言」理解——不补这一行，契约 C-5 与既有测试无法同时成立。
- **A-2 共享证据 sink 与 `[P]`**：每个红先行都要写 `notes/red-first-evidence.md`，写入目标相同即不可并行；故用户故事内的红先行不标 `[P]`，`[P]` 只给写目标互斥的 Setup / Polish 行。
- **A-3 条款形态与前置解析器**：本切片契约用 `- **C-N**`（单数字）形态，`pre-analyze-check.py` 的 `CLAUSE_DEF` 只认两位数字，故其 `clauses` 计数为 0（不做条款级核对）；条款覆盖的唯一机器判据是 `account-clause-coverage.py` 与 `validate-tasks.py` 的 `[green:]` 四项检查。本文件不因此放宽任何判据，也不为零而改契约写法。
- **A-4 快照刷新的降级口径**：三个快照的套件命令原样取自 `notes/migration-samples.md`；若套件缺未跟踪文件无法启动、或 `specify init` 在本机不可执行，按 `migration-distribution.md` C-8 记 `not-evaluated` + reason，**不记 0 新增失败**，也不以手工拷贝冒充刷新。
- **A-5 上游产物冻结**：本阶段不修改 `requirements.md` / `plan.md` / `research.md` / `data-model.md` / `contracts/`；发现的 plan 内部口径差异（advisory 计数 9 vs 10）只记录不改写。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结改前基线（镜像与副本、结构面、契约套件失败名单）与条款覆盖基线，让后续每个「相对基线零新增」判据都有日期化对照物；`notes/` 已就位。

- [ ] T001 捕获改前基线：创建 `.specify/specs/069b-isomorphism-migration-metrics/notes/pre-change-measurements.md`，逐项贴真实输出与捕获日期——`python3 scripts/python/sync-mirrors.py --check`（六对逐对 + 命令副本）、`python3 scripts/python/regen-command-copies.py --check`、`python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .`（violations 计数与 kind 集合）、`git rev-parse HEAD`、`git status --short` 中本切片相关条目；本行不写任何源文件。
- [ ] T002 [P] 重采条款覆盖基线：基线已在 tasks 阶段的既有义务下冻结（`.specify/specs/069b-isomorphism-migration-metrics/coverage-baseline.txt`，2026-10-25，base-sha `9bfe53de`，495 条基线内 / 0 beyond-baseline）；本行按 never-cache 规则在实现起点**重采一次**，命令为 `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics --freeze > .specify/specs/069b-isomorphism-migration-metrics/coverage-baseline.txt`（脚本只打印、不写文件），核对头部含 `frozen-from:` 与 `excluding 069b-isomorphism-migration-metrics`，并确认基线正文**不含**本切片 51 条 `C-N` 名——`--freeze` 排除被核算 spec 本身，本切片条款只能被任务行认领、不能被自己的基线豁免。
- [ ] T003 [P] 在实现起点重采名字级基线到 `.specify/specs/069b-isomorphism-migration-metrics/notes/test-baseline-contract.txt`（保留判据行 `zero NEW failing node ids against this list`，更新 HEAD / 日期 / 命令 / 结果四行），命令为 `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-contract.txt tests/contract tests/unit -q --tb=no -p no:cacheprovider`（**两侧都采**，与 GATE-4 / T026 的比对范围一致）；把重采名单与文件内冻结名单的差值（若有）追加到 `notes/pre-change-measurements.md` 的基线小节。

**Checkpoint**: 三类分母落盘（镜像/副本、结构面、契约失败名单、条款覆盖）；后续「零新增」判据全部有冻结对照物。

---

## Phase 2: User Story 1 - 我能查到代码与文档在八个阶段上的对应关系，以及它们不可能同构的地方 (Priority: P2) 🎯 MVP

**Goal**: 把「同构」落成可逐行核对的结构——分类所有者文档内新增 8 行 × 3 面 = 24 格的同构映射（每行带强制门禁与强制状态，两者可被真实门禁结构证伪）与四类不可同构边界（每条绑到一个封闭 face id），并由一个只读引擎动作 `--action isomorphism` 机械判定「标注失真 / 口号行 / 边界未绑面 / 载体唯一 / 介质判据」。

**Independent Test**: 在真实树上跑 `python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json`（期望 `stages = 8`、`gates = 6`、`findings = []`、exit 0）；再在 `~/tmp` 的 owner 副本上逐条注入（写一个不存在的 face id → `gate-unknown`；把一个真实但在该阶段只有 advisory 的 face 写进 `强制门禁` → `annotation-false-enforced`；把有 blocking 算子的阶段标 `已声明未强制` → `annotation-false-unenforced`；既无 face 又无标注 → `slogan-row`；删边界 (c) → `boundary-missing`；边界 `门禁处理` 不写 face id → `boundary-unbound`），确认每种注入各自转红；独立于 US2/US3 即可交付「映射可逐行核对、失真可机械发现」。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T004 [US1] 红先编写单元测试到 `tests/unit/test_isomorphism_checker.py`：阶段名册从 `skills/external/sdd-loop-driver/scripts/loop-state.py` 的 `STAGE_ARTIFACTS` 顶层键解析（8 个键，不接受内置列表冒充）、格语法边界（缺 `↔` / 两个 `↔` / 任一侧 < 8 字符 → `cell-malformed`）、`(stage, face)` blocking 集合计算（advisory 不算强制、别阶段的 blocking 不替代本阶段）、载荷根分支（无 `templates/commands/` 且无可解析 `skills/{external,internal}/` → 退出码 2 + `framework-source-required`，零 findings、不判绿）；运行红跑（红形态 = 引擎无 `isomorphism` 动作），把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T005 [US1] 红先编写契约测试到 `tests/contract/test_isomorphism_map.py`：表头逐字 6 列、恰好 8 个数据行、24 格逐格 `代码型：… ↔ 文档型：…`；行首阶段集合等于名册键集；`强制状态` 取封闭两值且真实（`已强制` 点名的每个 `(阶段, face)` 在 `shared/workflow/expression-gates.md` § 阶段算子表存在 blocking 行；`已声明未强制` 的阶段无任何 blocking 行），两侧反例分别产出 `annotation-false-enforced` / `annotation-false-unenforced`，两者皆空 → `slogan-row`；边界 a–d 各恰好一次且 `门禁处理` 含 face id 与处理说明（`boundary-missing` / `boundary-unbound` / `boundary-malformed`）；载体唯一（仓库内无第二份映射表，且 `shared/definitions/isomorphism-map.md` MUST 保持不存在）；介质判据短语闭集命中即 `medium-axis-in-map`；owns 列表同时列出映射与边界两项；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T006 [US1] [blockedBy: T004,T005] 在 `shared/definitions/flow-class-definitions.md` 落 `## 同构映射（8 阶段 × 3 面）`：开篇 owns 列表加「同构映射」「不可同构边界」两项、删除 `:19` 的交接行、表前一段 legend 一次性声明三面含义（结构 = 实体 / 关系 / 边界；流程 = 阶段与门禁角色；逻辑 = 证据 / 契约 / 验收 / 版本 / 所有权）、6 列表头逐字、8 个数据行首格逐字取自名册、每行三格写成 `代码型：… ↔ 文档型：…`、`强制门禁` 与 `强制状态` 两列（本版 8 行均 `已强制`，点名的 face 各自在该阶段有 blocking 算子）；只引用门禁 owner 的 `(stage, face, blocking)` 三元组，不复制算子文本。 [green: contracts/isomorphism-map.md#C-1] [green: contracts/isomorphism-map.md#C-2] [green: contracts/isomorphism-map.md#C-3] [green: contracts/isomorphism-map.md#C-4] [green: contracts/isomorphism-map.md#C-5] [green: contracts/isomorphism-map.md#C-6] [green: contracts/isomorphism-map.md#C-7]
- [ ] T007 [US1] [blockedBy: T006] 在 `shared/definitions/flow-class-definitions.md` 落 `## 不可同构边界` 四行表（表头逐字 `| 边界 | 不可互换的判定面 | 为什么不能互换 | 门禁处理 |`，a 验收 oracle / b 验证算子 / c 失败可见性 / d 语义 oracle 缺失各一次），每行 `门禁处理` 含 ≥1 个封闭 face id 与处理方式；同批落实「主张必须落地」的机械下限（24 格两侧成对、`templates/commands/` 与 `skills/` 无「文档即代码」许可句、两张表无介质判据短语），并只读扫描 `shared/workflow/expression-gates.md` § 阶段算子表的「执行算子」列确认零命中代码型算子闭集（`pytest` / `--cov` / `go test` / `mvn test` / `npm test` / `jest`）。 [green: contracts/isomorphism-map.md#C-8] [green: contracts/isomorphism-map.md#C-9] [green: contracts/isomorphism-map.md#C-10] [green: contracts/isomorphism-map.md#C-11] [green: contracts/isomorphism-map.md#C-12]
- [ ] T008 [US1] [blockedBy: T007] 在 `scripts/python/flow-class-check.py` 新增 `--action isomorphism`：只读、零写入、路径由 `--repo` 或脚本自身位置解析（不依赖 cwd）；JSON 含 `action` / `checked_at` / `stages`（行数）/ `gates`（六面数）/ `findings[]`（每项含 `kind` / `stage` / `message`）；退出码 0 零 finding / 1 有 finding / 2 输入错误（owner 缺失、名册不可解析 `roster-unavailable`、门禁 owner 不可解析）；载荷根以 `framework-source-required` 退出 2 且零 findings；`--action lookup` 与 `--action check` 的既有行为零改动。 [green: contracts/isomorphism-map.md#C-13] [green: contracts/isomorphism-map.md#C-14]
- [ ] T009 [US1] [blockedBy: T008] US1 定向转绿与取证：用 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/unit/test_isomorphism_checker.py tests/contract/test_isomorphism_map.py -q -p no:cacheprovider` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；再在真实树跑 `python3 scripts/python/flow-class-check.py --action isomorphism --repo . --format json`（期望 `stages = 8`、`gates = 6`、`findings = []`、exit 0）与同命令 `--format text`，把两段真实输出与逐行核对记录贴入 `notes/quickstart-run.md` 的场景 1 / 场景 2 小节。

**Checkpoint**: US1 独立可验收——24 格齐全、8 行强制标注可被门禁算子表证伪、四类边界各绑 face、载体唯一、介质判据零命中；MVP 就位。

---

## Phase 3: User Story 2 - 升级后既有项目行为不变，且分类数据随既有分发路径到达 (Priority: P2)

**Goal**: 钉住兼容与分发的三条事实——未刷新项目零调用点因而行为零变化；刷新后 owner / 引擎 / 命令副本 / 技能四类载荷出自同一发行包；项目侧不新增任何类别存储或读取点（项目在自己的知识空间记录类别，框架不读取）。同时把 069a 留下的三处措辞/指针偏差收敛为指向已落盘条款，并在三个事先冻结的客户项目快照上按失败 nodeid 集合证明零新增失败。

**Independent Test**: 读 owner 文档确认无「由 069b 承接」的待办措辞、`mixed-oracle` 行指向已落盘条款；跑 `tests/contract/test_migration_distribution.py` 确认模板与技能文件名集合不变、四动作零调用点、分发路径在场、零项目侧类别存储、快照记录字段齐备；再按 `notes/migration-samples.md` 的程序跑三个快照，`comm -13` 为空或按契约记 `not-evaluated`。

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T010 [US2] 红先编写契约测试到 `tests/contract/test_migration_distribution.py`：`shared/definitions/flow-class-definitions.md` 不再保留「069b 承接」的交接/待办措辞、§ 所有权 一行收敛为「项目 MAY 在自己的知识空间记录类别，框架不读取、不改变门禁」、字面量登记处声明父规格 § Shared Strings 为语义 owner；`templates/commands/` 与 `skills/` 的文件名集合与改前一致（27 / 51）且全文零四动作调用；`pyproject.toml` 的 `[tool.hatch.build.targets.wheel.force-include]` 含 `shared` 与 `scripts`、`src/specify_cli/__init__.py` 的 shared 复制段在场、`src/hatch_build.py` 的 skills 阶段在场；仓库内零新增项目侧类别存储（`.specify/memory/` 下无类别数据文件）；`notes/migration-samples.md` 三行样本字段齐备（项目 / HEAD / 分支 / 脏文件数 / 载荷状态 / 套件命令）；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T011 [US2] [blockedBy: T010] 在 `shared/definitions/flow-class-definitions.md` 收敛 P1 / P3 / P4 三处指针：P4 的 10 处「069b 承接」（判据 `:35` 1 处、台账说明 `:95` 1 处、台账 `notes` 8 处）改为指向 `contracts/ledger-reconciler.md` C-7（只改指针，不改任何行的类别、`basis` 与判据正文）、P1 字面量登记处改为「父规格 § Shared Strings 是语义 owner，069a / 069b 的表是同源投影」、P3 § 所有权 一行改为「项目 MAY 在自己知识空间记录，框架不读取、不影响门禁」；P2 的 `:19` 交接行由 T006 删除，不在本行处理；同批实测四类载荷同一发行包（`pyproject.toml` 的 `shared` / `scripts` force-include、`src/specify_cli/__init__.py` shared 复制段、`src/hatch_build.py` skills 阶段），把四条命令的真实输出与「未刷新 = 零调用点」的检索结果写入 `notes/quickstart-run.md` 的场景 6 小节。 [green: contracts/migration-distribution.md#C-1] [green: contracts/migration-distribution.md#C-2] [green: contracts/migration-distribution.md#C-3] [green: contracts/migration-distribution.md#C-4] [green: contracts/migration-distribution.md#C-5]
- [ ] T012 [US2] [blockedBy: T011] 跑三个客户快照并按名字级判据取证：逐项目 `git -C <project> archive <HEAD> | tar -x -C ~/tmp/069b-snap-<n>` 建临时副本（原始项目与工作树零修改），刷新前按 `notes/migration-samples.md` 的套件命令采失败 nodeid 名集；随后由本切片源码构建 wheel 并暂存到 `~/tmp/069b-pkg`（`python3 -m pip wheel . --no-deps -w ~/tmp/069b-wheel --trusted-host yum.tbsite.net` → `python3 -m pip install --target ~/tmp/069b-pkg --no-deps --upgrade ~/tmp/069b-wheel/specify_cli-*.whl`），先断言 `~/tmp/069b-pkg/specify_cli/shared/definitions/flow-class-definitions.md` 与 `~/tmp/069b-pkg/specify_cli/scripts/python/flow-class-check.py` 在场，再用 `PYTHONPATH=~/tmp/069b-pkg /Users/liuqiming.lqm/project/profiles/.venv/bin/specify init . --here --force --ai <该项目既有 AI 工具> --no-git --ignore-agent-tools` 刷新、再采第二次名集，`comm -13 before after` MUST 为空；套件因缺未跟踪文件无法启动或 wheel 构建 / `specify init` 不可执行时记 `not-evaluated` + reason（不记 0 新增失败、不以人工 `cp` / 逐文件复制冒充刷新）；记录证据后清理临时副本，把三行结论写入 `notes/quickstart-run.md` 的场景 6 小节。 [green: contracts/migration-distribution.md#C-6] [green: contracts/migration-distribution.md#C-7] [green: contracts/migration-distribution.md#C-8] [green: contracts/migration-distribution.md#C-9]
- [ ] T013 [US2] [blockedBy: T012] US2 转绿与取证：跑 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_migration_distribution.py -q -p no:cacheprovider` 至全绿并把绿证据追加 `notes/red-first-evidence.md`；另只读复核未刷新形态——`git show f0df3d0b:templates/commands/docs.md` 与 `humanize.md` 均不含四动作任一，`python3 scripts/python/regen-command-copies.py --check` 输出 `OK`，两段真实输出贴 `notes/quickstart-run.md` 场景 6。

**Checkpoint**: US2 独立可验收——未刷新零调用点、刷新同包原子、项目侧零存储/零读取点、三快照名字级零新增失败（或按契约记 `not-evaluated`）。

---

## Phase 4: User Story 3 - 分类的落地形态与度量仪器可被机械核对，而不是靠自述 (Priority: P2)

**Goal**: 让「落地形态」与「度量」不靠自述——台账新增一次版本声明并由对账检查同时具备解析侧下限与覆盖率断言（「缺口」与「解析失败」两种红可区分）；委托关系由命令模板里的技能路径解析后与台账类别比对（不依赖人工清单，类中立清单封闭）；六面门禁每面恰一个 owner 指针且判据正文不搬家；三项基线只用既有四个通道，无样本记 `not-evaluated`。

**Independent Test**: 对台账做两次注入（删一行 → `red_kind = gap`；破坏表形 → `red_kind = parse-failure` 或 `owner-unavailable`），确认两红不同且静默绿为 0；对混合 oracle 单元确认台账 `flow_class = execution`；跑 `--action delegation` 确认 27 个模板的边全部 `same-class` / `neutral-exempt` 且在改类夹具上转红；跑 `--action faces` 确认 6/6 指针可解析、判据副本计数为 0；核对三项基线的四条来源命令都在既有通道内。

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T014 [US3] 红先编写契约测试到 `tests/contract/test_ledger_reconciliation.py`：`--action check` 的 `coverage` 块六字段与算术（`gaps = missing + unknown`、`parse_errors = row-malformed + ledger-truncated`）；`LEDGER_FLOOR` 反空真（`⌊(27+51)/2⌋ = 39`，由清单侧 floor 推导、不得取自被检查台账自身；解析出 0 行而清单非空 → `ledger-truncated`；删一行后 77 行 MUST NOT 触发 `ledger-truncated`、仍判 `gap`）；`red_kind` 优先级 `owner-unavailable > framework-source-required > parse-failure > gap > clean`；双注入两种红可区分（删一行 → `gap`；破坏表形 → `parse-failure` 或 `owner-unavailable`）；`mixed-oracle-class` 反例注入（`basis = mixed-oracle` 且 `flow_class = expression`）；`ledger-version-missing`（声明缺失）与声明重复（按 `row-malformed`）；夹具根含 27 个命令模板与 51 个技能目录；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T015 [US3] 红先编写契约测试到 `tests/contract/test_delegation_classes.py`：27 个模板逐条解析委托边（语法 `(?:\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md`、同模板同名去重）、全部边 `same-class` 或 `neutral-exempt`、零 finding；证伪夹具把一个技能改成反类 → `delegation-mismatch` 转红、把一条类中立边保留 → 仍绿；台账中不存在的技能 → `delegation-unknown-skill`；仓库出现 ≥3 行命令↔技能对照表 → `delegation-hand-list`；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T016 [US3] 红先编写契约测试到 `tests/contract/test_expression_faces.py`：六面表恰好 6 行、face id 唯一、每行一个 `owner_pointer` 格（格内 `+` 连接多路径仍算一个绑定）、每个路径在源码根或 `.specify/` 镜像可解析、带 `§ <anchor>` 时锚可匹配标题；三种注入（删一行 → `faces-count`、复制一行 → `faces-duplicate`、指针指向不存在路径 → `faces-unresolvable`）；六面之外出现 ≥3 face id 与 owner 路径成对表 → `faces-second-table`；`python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate` 在封闭主体集上 `findings = []`（不含 S3 比较集：9 条 owner 路径 / 6 个绑定格，尤其不含 `shared/workflow/expression-gates.md`）；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T017 [US3] 红先编写契约测试到 `tests/contract/test_measurement_instruments.py`：`notes/expression-baseline.md` 每行七字段（`quantity` / `frozen_value` / `frozen_at` / `frozen_commit` / `instrument` / `source_command` / `verdict`）齐备、`verdict ∈ {not-evaluated, measured}` 且不存在「达成 / 未达成」层；三项量共用同一起点（`requirements.md` 首次提交的 author date）与同一 `frozen_commit`；四个通道命令在既有脚本中存在（`exec-quant.py --action list-records`、`feedback-utils.py --action list`、`run-determination.py --action history`、`git log --diff-filter=A --format='%h %as'`）；仓库内无新采集器 / 第二份基线存储；`verification-log-template.md` 的 SC 词表仍为五值且与 `not-evaluated` 不互相顶替；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T018 [US3] 红先编写单元测试到 `tests/unit/test_reconciler_extensions.py`：`red_kind` 优先级裁决函数、coverage 数学边界（`matched` / `inventory_units` / `gaps` / `parse_errors` 组合与 `clean` 的充要条件）、委托语法正则与同模板去重、faces `owner_pointer` 的 `+` 拆分与 `§` 锚解析、`LEDGER_FLOOR` 由清单侧 floor 推导（`⌊(27+51)/2⌋ = 39`，不取自被检查台账，MUST NOT 成第三份手写单元计数）；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T019 [US3] [blockedBy: T014,T018] 台账版本声明 + 对账扩展：在 `shared/definitions/flow-class-definitions.md` § 逐流程台账 内声明**一次** `**台账版本**: 1（2026-10-25）` 并写明生效版本由该文档版本与既有 `## 变更记录` 共同承载、行级不设版本列；在 `scripts/python/flow-class-check.py --action check` 增量加 `ledger-truncated`（解析出行数 < 解析侧下限 39）、`coverage` 块（`ledger_rows` / `inventory_units` / `matched` / `gaps` / `parse_errors` / `floor`）、`red_kind`（优先级 `owner-unavailable > framework-source-required > parse-failure > gap > clean`）、`ledger-version-missing` 与 `mixed-oracle-class` 两个新 kind，文本输出在空集旁同时打印 `matched` 与 `inventory_units`；069a 的八个 kind、退出码阶梯、`lookup` 语义零改动；同批只给 `tests/unit/test_flow_class_check.py` 的 `_render_owner` 夹具补 `**台账版本**` 一行（按 A-1，只补输入、不改断言）。 [green: contracts/ledger-reconciler.md#C-1] [green: contracts/ledger-reconciler.md#C-2] [green: contracts/ledger-reconciler.md#C-3] [green: contracts/ledger-reconciler.md#C-4] [green: contracts/ledger-reconciler.md#C-5] [green: contracts/ledger-reconciler.md#C-6] [green: contracts/ledger-reconciler.md#C-7]
- [ ] T020 [US3] [blockedBy: T019] 在 `scripts/python/flow-class-check.py` 新增 `--action delegation`：从命令模板文本解析委托边（语法 `(?:\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md` → `skill:<name>`，同模板同名去重），每条边输出 `{command, skill, command_class, skill_class, verdict, source_line}`，`verdict ∈ {same-class, neutral-exempt, mismatch, unknown-skill}` 且按 C-8 的裁决顺序（`unknown-skill` → `neutral-exempt` → `same-class` / `mismatch`；清单成员一律 `neutral-exempt`，实测 6 条）；类中立豁免只取所有者 § 类中立清单（不复制清单副本），`mismatch` → `delegation-mismatch`、台账不存在的技能 → `delegation-unknown-skill`、仓库出现人工委托清单 → `delegation-hand-list`；模板未声明技能路径时不构成委托边、不产 finding；只读零写入。 [green: contracts/ledger-reconciler.md#C-8] [green: contracts/ledger-reconciler.md#C-9] [green: contracts/ledger-reconciler.md#C-10]
- [ ] T021 [US3] [blockedBy: T020] 在 `scripts/python/flow-class-check.py` 新增 `--action faces`：解析 `shared/workflow/expression-gates.md` § 六面 表（恰好 6 行、face id 唯一、每行一个 `owner_pointer` 格，`+` 连接仍算一个绑定），逐路径在源码根或 `.specify/` 镜像解析、带 `§ <anchor>` 时校验标题；违规记 `faces-count` / `faces-duplicate` / `faces-pointer-missing` / `faces-unresolvable`，六面之外 ≥3 face id 成对表记 `faces-second-table`；同批把判据副本计数接到既有 `doc-consistency-check.py` 的 duplicate 面（主体集封闭为 owner 文档与本 spec 的 formal artifacts，要求 `findings = 0`）；只读零写入。 [green: contracts/ledger-reconciler.md#C-11] [green: contracts/ledger-reconciler.md#C-12] [green: contracts/ledger-reconciler.md#C-13]
- [ ] T022 [US3] [blockedBy: T017] 三项基线按同口径复核并落盘 `.specify/specs/069b-isomorphism-migration-metrics/notes/expression-baseline.md`：逐条复算四个既有通道（`exec-quant.py --action list-records --since 2026-10-24 --format json`、`feedback-utils.py --action list --since 2026-10-24 --format json` + 逐条查 `lifecycle_point: gate-*`、`run-determination.py --action history --target /speckit.analyze --json`、`git log --diff-filter=A --format='%h %as' -- requirements.md`），保持 `gate_calls` 的过滤集合为事先冻结的 6 个检查类单元且归属判据为 `run_id` 含 `069b`、`confirmations` 两个分项分别记录、`wall_clock` 起点为 `2026-10-24`（首次提交 `f0df3d0b`，用 `--diff-filter=A` 取，不用 `git log -1`）；无样本的量记 `not-evaluated` + reason（不记 0、不记达成），并把「不可计部分」（脚本级检查不是 exec-quant 单元）与四条可复算命令留在记录内。 [green: contracts/measurement-instruments.md#C-1] [green: contracts/measurement-instruments.md#C-2] [green: contracts/measurement-instruments.md#C-3] [green: contracts/measurement-instruments.md#C-4] [green: contracts/measurement-instruments.md#C-5] [green: contracts/measurement-instruments.md#C-6] [green: contracts/measurement-instruments.md#C-7]
- [ ] T023 [US3] [blockedBy: T021,T022] US3 转绿与取证：用 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_ledger_reconciliation.py tests/contract/test_delegation_classes.py tests/contract/test_expression_faces.py tests/contract/test_measurement_instruments.py tests/unit/test_reconciler_extensions.py -q -p no:cacheprovider` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；再实测四件事——`--action check` 在真实树为零 finding 且在 `~/tmp` 的双注入副本上分别给出 `gap` 与 `parse-failure`（或 `owner-unavailable`，按 C-3 判据）；`--action delegation` 在真实树零 finding、在「改一个技能为反类」副本上转红；`--action faces` 报 `faces = 6` 且 `findings = []`；三个新动作在仅含 `.specify/` 载荷的临时根上均以 `framework-source-required` 退出 2。把四段真实输出贴入 `notes/quickstart-run.md` 的场景 3 / 4 / 5 小节。 [green: contracts/ledger-reconciler.md#C-14] [green: contracts/ledger-reconciler.md#C-15] [green: contracts/ledger-reconciler.md#C-16] [green: contracts/measurement-instruments.md#C-8] [green: contracts/measurement-instruments.md#C-9] [green: contracts/measurement-instruments.md#C-10]

**Checkpoint**: US3 独立可验收——台账缺口与解析失败两红可区分、混合 oracle 落类一致、委托边由模板解析且类中立封闭、六面 6/6 且判据不搬家、三项基线可复算且无样本不记零。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 收口镜像与命令副本、文档同步、全量回归、SC 证据与特性登记；不改任何实现语义。

- [ ] T024 [P] 镜像同步与逐对核验：跑 `python3 scripts/python/sync-mirrors.py --write --only shared --only scripts` 后 `python3 scripts/python/sync-mirrors.py --check`（相对 T001 基线零新增差异），用 `cmp` 逐对核对 `shared/definitions/flow-class-definitions.md` 与 `.specify/shared/definitions/flow-class-definitions.md`、`scripts/python/flow-class-check.py` 与 `.specify/scripts/python/flow-class-check.py` 同字节，并复核 `python3 scripts/python/regen-command-copies.py --check` 仍 `OK`（证明 `templates/commands/` 零改动）；禁止手改镜像。 [green: contracts/migration-distribution.md#C-10]
- [ ] T025 [P] 文档同步评估与结构面复核：按 `.specify/shared/workflow/docs-step.md` § Evaluation procedure 判断 `docs/reference/` 与 `docs/concepts/` 中涉及流程分类 / 门禁的页面是否因新增映射与边界而失真（失真时只补一行指向 owner 文档的指针，不复制映射表或判据），随后跑 `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` 核对 `violations` 计数与 kind 集合相对 T001 基线零新增，把结论与两段输出写入 `notes/quickstart-run.md` 的 docs-sync 小节。
- [ ] T026 全量回归与红先证据完整性：跑 `SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-after.txt tests/contract tests/unit -q --tb=no -p no:cacheprovider`，把失败 nodeid 排序后与 `notes/test-baseline-contract.txt` 的冻结名单做 `comm -13`（MUST 为空，判据是名字级不是条数级）；同时核对 `notes/red-first-evidence.md` 覆盖 8 支测试的红跑与转绿证据各一条，缺项补齐。 [blockedBy: T024]
- [ ] T027 逐 SC 落 `.specify/specs/069b-isomorphism-migration-metrics/verification.md`：`- **SC-001**` … `- **SC-005**` 各带状态（取 `verification-log-template.md` 五值词表）、命令、输出摘要与证据指针；SC-001 记 `--action isomorphism` 的零 finding 与逐行核对记录，SC-002 记三快照的 `comm -13` 结果（未取得样本时状态取词表内的 `unknown`、证据行写 `not-evaluated` + reason——`not-evaluated` MUST NOT 出现在状态位），SC-003 记双注入的 `red_kind` 与退出码，SC-004 记混合 oracle 样本清单与机器侧落类分布（两名独立判定者未执行时状态取 `unknown`、证据行写 `not-evaluated` + reason，不记达成），SC-005 记 6/6 owner 指针与 duplicate 面 `findings = 0`；另把 `notes/quickstart-run.md` 七个场景的完成情况与小节指针列入本文件。 [blockedBy: T026]
- [ ] T028 特性登记核对与补齐：确认 `.specify/memory/features/069.md` § Related Specifications 已有本切片 `tasks.md` 指针与任务规模、§ Status Tracking 已有「069b tasks」行（tasks 阶段已回填，缺则补），只需更新 `.specify/memory/features.md` 的 069 行 Last Updated 单元格——状态列 MUST 保持 `Planned`（`069a = Implemented` / `069b = 进行中`），`Implemented` 转移属 `/speckit.implement`。 [blockedBy: T027]
- [ ] T029 终局门禁复跑：依次跑 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/069b-isomorphism-migration-metrics/tasks.md`（0 error / 0 warning）、`python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/069b-isomorphism-migration-metrics --stage tasks --repo .`（errors=0，advisory 逐条裁定）、`python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/069b-isomorphism-migration-metrics/requirements.md --tasks .specify/specs/069b-isomorphism-migration-metrics/tasks.md`（`proceed`）、`python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics`（claimed = 51、uncovered beyond baseline = 0），并复核零新增 `/speckit.*` 命令与零新增门禁面（`templates/commands/` 27 个文件、`shared/workflow/expression-gates.md` 六面表零改动、调用点表零新增），把四段真实输出贴入 `verification.md` 的 gates 小节。 [green: contracts/migration-distribution.md#C-11] [blockedBy: T028]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始——它是后续所有「相对基线零新增」判据的分母。
- **User Story 1 (Phase 2)**: 依赖 Setup 的基线落盘；故事内部严格 TDD（红 → 实现 → 转绿）。
- **User Story 2 (Phase 3)**: 依赖 US1 对 owner 文档的章节落盘（`T011` 要在新增章节之后收敛指针，避免同一处被两次改写）；`T012` 的快照跑测以 `T011` 的载荷事实核对为前提。
- **User Story 3 (Phase 4)**: 依赖 US1 的引擎骨架（`T019`–`T021` 扩展的是同一文件 `scripts/python/flow-class-check.py`）；`T019` 的版本声明落在 owner 文档，故排在 US2 的指针收敛之后。
- **Polish (Phase 5)**: 依赖全部故事完成；`T026` 依赖 `T024`（镜像先同步再全量核验），`T027` 依赖 `T026`，`T029` 依赖 `T028`。

**本特性无 Foundational 阶段**：US1 / US2 / US3 的写目标不重叠（US1 = owner 文档映射与边界 + 引擎 `isomorphism`；US2 = owner 文档指针 + 快照证据；US3 = owner 文档版本声明 + 引擎 `check`/`delegation`/`faces` + 基线记录），唯一共享前提（基线与覆盖基线）已在 Setup 落盘；按模板规则整段省略并顺延阶段编号，避免留空章节。

### Within Each User Story

- 测试行先写并确认红，再进入实现行；转绿行在该故事末尾统一取证。
- US1：两支红测试 → owner 映射章节 → owner 边界章节 → 引擎 `--action isomorphism` → 转绿取证。
- US2：红测试 → owner 指针收敛与分发实测 → 三快照跑测 → 转绿取证。
- US3：五支红测试 → 台账版本声明与 `check` 扩展 → `--action delegation` → `--action faces` → 三项基线复核 → 转绿取证。

### Parallel Opportunities

- Setup：`T002`（覆盖基线，写 `coverage-baseline.txt`）与 `T003`（契约失败基线，写 `notes/test-baseline-contract.txt`）写目标互斥，可并行；`T001` 先落盘以免与二者抢同一节记录。
- US1 / US2 / US3 的红先行**不并行**：它们共用 `notes/red-first-evidence.md` 这一追加落点，同写目标即不可并行（A-2）。要并行取证时，必须先把该 sink 拆成每测试一份文件——本切片不为此新增落点。
- Polish：`T024`（镜像，写 `.specify/**`）与 `T025`（文档评估，写 `notes/quickstart-run.md`）写目标互斥，可并行；`T026` → `T027` → `T028` → `T029` 串行。

## Parallel Example: Phase 1 Setup

```bash
# 两支基线互不写同一文件，可同时开：
python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069b-isomorphism-migration-metrics --freeze > .specify/specs/069b-isomorphism-migration-metrics/coverage-baseline.txt
SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python bash scripts/bash/run-tests.sh --names-out ~/tmp/069b-names-contract.txt tests/contract -q --tb=no -p no:cacheprovider
```

## Implementation Strategy

### MVP First

MVP = **US1**：三个故事在 requirements 中同为 P2，而 US1 是切片头号交付物——24 格映射与四类边界一旦可被 `--action isomorphism` 逐行判定，本切片的核心主张（同构是可核对结构，不是比喻）就已可独立演示；US2 的兼容保证与 US3 的落地/度量仪器各自独立可测，随其后交付。

1. 完成 Phase 1（基线与覆盖基线），确认分母就位。
2. 完成 US1（Phase 2）→ 跑 Checkpoint：24 格齐全、8 行强制标注可被证伪、四类边界各绑 face、载体唯一。
3. **STOP and VALIDATE**：以 quickstart 场景 1 / 2（逐行核对与失真注入）人工复核 MVP。
4. 完成 US2（Phase 3）→ 兼容面独立核验（零调用点 + 三快照名字级零新增失败）。
5. 完成 US3（Phase 4）→ 对账/委托/六面/三项基线独立核验。
6. 完成 Polish（Phase 5）→ 镜像、文档、全量回归、SC 证据、特性登记与终局门禁。

### Incremental Delivery

1. Setup → 基线可对照（无用户可见行为）。
2. US1 → 交付「同构映射可逐行核对 + 标注失真转红」。
3. US2 → 交付「未刷新零变化 + 刷新原子到达 + 客户快照零新增失败」。
4. US3 → 交付「台账缺口与解析失败可区分 + 委托同类机械核验 + 六面指针 6/6 + 三项基线可复算」。
5. Polish → 交付可验收证据链（SC 逐条 + 全量零新增失败 + 终局门禁）。

---

## Notes

- `[P]` 行 = 写目标不同且无未完成依赖；同一文件的连续增补一律串行（owner 文档与引擎文件均如此，二者各被多个任务行按区段增补，故按区段顺序执行）。
- 「相对基线零新增」判据的分母都在 § Measured Premises 与 T001 落盘的 `notes/pre-change-measurements.md`；任务行只引用，不复述基线数值。
- 契约套件判据是「零**新增**失败 nodeid」（基线红名单 = `notes/test-baseline-contract.txt`，计数以该文件为准）；`pytest` 只存在于 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`，不得假设 `python3 -m pytest` 可用。
- 结构面判据是「零**新增**违规」（基线已有 `broken-link` 2 + `note-frontmatter` 1）；写成「全绿」会与既有债冲突，本切片不修也不掩盖他特性的登记债。
- 判据正文只在两个 owner 内（`shared/definitions/flow-class-definitions.md` 与 `shared/workflow/expression-gates.md`）：本切片的契约、测试与任务行一律引用，不复制判据句、算子表或面表；`shared/workflow/expression-gates.md` 本切片零改动。
- 被否决备选 `shared/definitions/isomorphism-map.md` MUST NOT 创建；`pre-analyze-check.py` 对它报 `missing-path` advisory 属预期残留（§ Path Conventions、T005）。
- 062 / 067 / 068 只被引用不被改写；069a 的规格与判据正文零改动（唯一触碰是 A-1 允许的 069a 单元测试夹具补一行输入）。
- 提交纪律：只提交本特性产物（显式路径），不夹带运行期记录（`.specify/memory/session/`、`exec-quant/records/`、`feedback/`）与他命令的未提交工件；本 tasks 阶段不 push。
