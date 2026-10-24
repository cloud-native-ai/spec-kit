# Tasks: 执行/表达二元分类与文档型门禁（Execution/Expression Classes & Document-Form Gates）— Feature 069 / Slice 069a

**Requirement ID**: 069a（Feature 069 的切片；不新建 Feature ID、不新增注册行）
**Requirement Key**: `069a-flow-classification-docs-gates`
**Branch**: `069-execution-expression-sdd`
**Related Feature**: Feature 069 执行/表达二元分类与文档型 SDD 同构，状态 Planned（切片复用同一注册行）
**Input**: Design documents from `.specify/specs/069a-flow-classification-docs-gates/`
**Prerequisites**: plan.md（含 § Minimal Designated Wiring W1–W4）、requirements.md（27 FR / 8 SC）、research.md（R1–R14）、data-model.md（E1–E10）、contracts/ ×4（50 条款：flow-class-ledger 15 / expression-gate-operators 15 / doc-consistency-checker 10 / compatibility-distribution 10）、quickstart.md（6 场景）、feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" 为测试强制原则——纯函数/工具须有单测、关键流程须有自动化回归、集成/契约测试覆盖跨面接口；且 principle VII 的 Workflow Gates 标注 NON-NEGOTIABLE。本切片交付可执行运行时（两个 stdlib 引擎 + 4 个接线点），非 template-only，故 template-only 的 Partial 豁免不适用。8 支新测试（6 契约 + 2 单元）一律红先：先跑出失败、把命令/真实输出/退出码写入 `notes/red-first-evidence.md`，再进入对应实现行。)

**Tests**: 红先证据的落点是 `.specify/specs/069a-flow-classification-docs-gates/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）；失败测试名基线的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。测试解释器只有 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（见 § Environment Prerequisites）。

**Organization**: 按用户故事组织：US1（P1 分类本体与查表）与 US2（P1 文档型门禁与最小接线）共同构成 MVP——只有分类而无读取点的门禁与只有门禁而无分类读取的实现都各是一半机制；US3（P2 防滥用与兼容）在 US2 的接线面之上钉住「类别不得成为跳过阶段的开关」与 062/067/068 的字节不变。Setup 冻结改前基线与条款覆盖基线；无 Foundational 阶段（US1 与 US2 写目标不重叠，唯一共享前提已由 Setup 落盘，见 § Dependencies）；Polish 收口文档同步、镜像、全量核验、SC 证据与特性登记回填。

## Definition of Done (DoD)

- DoD-1: 全部任务行行为 `[X]`；若有 `[~]`，理由逐条记录在 `.specify/specs/069a-flow-classification-docs-gates/verification.md` 的 `deferred_tasks=`。
- DoD-2: 两份 owner 文档与两个引擎按契约交付——`shared/definitions/flow-class-definitions.md`（判据/两取值/边界例/78 行台账/类中立封闭清单/命名空间/变更记录）、`shared/workflow/expression-gates.md`（六面 + 8 阶段算子表 + 调用点表 + 阻断级别 + 证据语法 + 三项基线协议）、`scripts/python/flow-class-check.py`（check/lookup）、`scripts/python/doc-consistency-check.py`（verify 四面）。
- DoD-3: 四份契约共 50 条款（flow-class-ledger C-1…C-15、expression-gate-operators C-1…C-15、doc-consistency-checker C-1…C-10、compatibility-distribution C-1…C-10）每条恰被一个任务行 `[green:]` 认领，`account-clause-coverage.py` 报告 claimed = 50。
- DoD-4: 8 支新测试（`test_flow_class_ledger` / `test_flow_class_correctness` / `test_expression_gates_doc` / `test_doc_consistency_checker` / `test_expression_gate_wiring` / `test_expression_compatibility` / `test_flow_class_check` / `test_doc_consistency_rules`）全绿；相对 `notes/test-baseline-contract.txt` 零**新增**失败 nodeid（既有 31 红不修、不掩盖）。
- DoD-5: plan.md § Mirror Obligations 逐行落地：7 个源文件与其 `.specify/` 镜像同字节，8 个每工具命令副本由 `regen-command-copies.py` 重生成，`sync-mirrors.py --check` 相对改前基线零新增差异；零手改镜像、零手写副本。
- DoD-6: 接线封闭且不越界：除 W1/W2 两个命令模板、W3/W4 两个技能与 `shared/workflow/feedback-step.md` 的一行指针外，其余 25 个模板与 49 个技能内容哈希不变；062 / 067 / 068 的 `requirements.md` 字节不变；结构面 `violations` 相对基线（`broken-link` 2 + `note-frontmatter` 1）零新增。
- DoD-7: 零新增 `/speckit.*` 命令、零新增项目侧存储或读取点；未刷新项目无调用点，刷新后接线与载荷同包到位（兼容分发的两种稳定状态成立）。
- DoD-8: `verification.md` 逐条列出 `- **SC-001**` … `- **SC-008**` 的状态、命令、输出摘要与证据指针；无来源的量记 `not-evaluated` + reason，不记 0、不记达成。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/069a-flow-classification-docs-gates/tasks.md` exit 0（0 error；warning 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/069a-flow-classification-docs-gates --stage tasks --repo .` 输出含 `decision=pass` 且 errors=0。
- GATE-3: 分解规模合法 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/069a-flow-classification-docs-gates/requirements.md --tasks .specify/specs/069a-flow-classification-docs-gates/tasks.md` 结论为 `proceed`。
- GATE-4: 测试零新增失败 — check: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider` 的失败 nodeid 排序后与 `notes/test-baseline-contract.txt` 名单 `comm -13` 为空（名字级，非计数级）。
- GATE-5: 镜像与副本零漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0，且与 `notes/pre-change-measurements.md` 的改前基线比较零新增差异。
- GATE-6: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069a-flow-classification-docs-gates` 输出 claimed = 50 且 uncovered beyond baseline = 0。
- GATE-7: 结构面零新增违规 — check: `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` 的 `violations` 计数与 kind 集合相对基线零新增。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/069a-flow-classification-docs-gates/tasks.md` 返回 0。
- GATE-9: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-8]\*\*' .specify/specs/069a-flow-classification-docs-gates/verification.md` 返回 8。

## Environment Prerequisites

<!-- 本节的探测结论是单一落点：任何任务行只引用本节，不复述环境判定。 -->

- pytest 解释器: **available（仅 profiles/.venv）** — probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --version` → `pytest 9.1.1`；本仓 `.venv/bin/python -m pytest --version` → `No module named pytest` @ 2026-10-24; affected: T004、T005、T006、T012、T013、T014、T015、T020、T021、T027、T029、T030、T034。
- git: **available** — probe: `git log -1 --format=%cs -- .specify/specs/069a-flow-classification-docs-gates/requirements.md` → `2026-10-24`（`as-of` 面的时钟来源与兼容面哈希比对均依赖它）@ 2026-10-24; affected: T020、T029、T030、T034。
- 容器 / 镜像仓库 / 集群 / 外网: **none** — 本切片的检查全为本地文件、`git` 与本地 pytest；无构建、无拉取、无网络 @ 2026-10-24; affected: none。
- humanize 命令形态基线: **Simple（实测）** — probe: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_humanize_command_surface.py -q` → `10 passed`；`templates/commands/humanize.md` 非表格行 40、无 `## Wrap-up`、`SKILL.md` 唯一一处、零 `flow-class-check` 引用 @ 2026-10-24; affected: T015、T024、T025、T026。
- 镜像漂移基线: **clean（判据 = 相对该基线零新增差异，不是绝对全绿）** — probe: `python3 scripts/python/sync-mirrors.py --check` → 六对 `ok`（`templates/` 22 files、`skills/external/` 396 files、`skills/internal/` 136 files、`agents/` 3 files、`scripts/` 109 files、`shared/` 51 files）+ 命令副本 `OK`，exit 0 @ 2026-10-24; affected: T026、T033、T034。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。
- **[Story]**: 用户故事标签（`[US1]`…`[US3]`），只在用户故事阶段的任务行出现；Setup 与 Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**：绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析。50 条款分区：flow-class-ledger C-1…C-3→T007、C-4…C-6→T009、C-7→T010、C-8→T011、C-9→T022、C-10/C-11→T027、C-12…C-15→T034；expression-gate-operators C-1→T016、C-2/C-3→T017、C-4…C-10→T018、C-11…C-15→T019；doc-consistency-checker C-1…C-4→T020、C-5…C-8→T021、C-9/C-10→T027；compatibility-distribution C-1…C-3→T030、C-4…C-10→T034。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`shared/workflow/feedback-step.md`、`scripts/python/flow-class-check.py`、`scripts/python/doc-consistency-check.py`、`templates/commands/docs.md`、`templates/commands/humanize.md`、`skills/external/create-docs/SKILL.md`、`skills/external/humanize/SKILL.md`、`tests/contract/`、`tests/unit/`。
- **生成面（禁止手改）**: `.specify/shared/`、`.specify/scripts/`、`.specify/skills/` 镜像（`sync-mirrors.py` 投影）与 8 个每工具命令副本（`.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/`，`regen-command-copies.py` 生成）。
- **证据落点（本特性）**: `.specify/specs/069a-flow-classification-docs-gates/` 下的 `notes/pre-change-measurements.md`、`notes/pre-change-file-hashes.txt`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`notes/expression-baseline.md`、`coverage-baseline.txt`、`verification.md`。
- **禁改面**: `.specify/specs/062-humanize-command/`、`.specify/specs/067-loop-efficiency-hardening/`、`.specify/specs/068-exec-quant-feedback-channel/`、`src/specify_cli/`、`AGENTS.md`、`.specify/instructions.md`；`.specify/specs/069-execution-expression-sdd/`（父规格零改动）。

## Measured Premises (re-measured at generation time 2026-10-24, HEAD `01275c5c`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 流程单元规模（台账分母） | `ls templates/commands/*.md \| wc -l`；`ls -d skills/external/*/ \| wc -l`；`ls -d skills/internal/*/ \| wc -l`；两层同名冲突 `comm -12` | 命令 27、external 14、internal 37 → 技能 51、合计 78；冲突输出为空 |
| 契约条款数（逐文件） | `grep -ohE '\*\*C-[0-9]+\*\*' .specify/specs/069a-flow-classification-docs-gates/contracts/*.md \| wc -l` | 50（flow-class-ledger 15、expression-gate-operators 15、doc-consistency-checker 10、compatibility-distribution 10），全部 `md-bold-closed` 形态 |
| FR / SC 计数 | `grep -cE '^\- \*\*FR-[0-9]+\*\*' requirements.md`；`grep -cE '^\- \*\*SC-[0-9]+\*\*' requirements.md` | 27 / 8 |
| 四个新目标文件当前状态 | 逐个 `test -e` | 四个全部 ABSENT（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`scripts/python/flow-class-check.py`、`scripts/python/doc-consistency-check.py`）；四个接线文件全部 EXISTS |
| notes/ 与覆盖基线 | `ls .specify/specs/069a-flow-classification-docs-gates/notes/`；`ls .../coverage-baseline.txt` | `parent-fr-mapping.md`、`test-baseline-contract.txt` 在盘；`coverage-baseline.txt` 缺失 |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | 六对 `ok` + 命令副本 `OK`，两次均 exit 0 |
| 结构面基线（非零） | `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` | exit 0，`violations=3`：`broken-link` 2（均在 `docs/concepts/overview.md`）+ `note-frontmatter` 1（`docs/notes/type-follows-stage-misclassification.md`） |
| 前序规格哈希（SC-008 分母） | `shasum -a 256` 三份 `requirements.md` | `987b24ea1f98…`（062）、`29e26b701ebe…`（067）、`ec20d5e28bd0…`（068） |
| 测试解释器与采集面 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest --version`；同解释器 `--collect-only -q tests/contract`；本仓 `.venv/bin/python -m pytest --version` | `pytest 9.1.1`；`4190 tests collected`；本仓 `.venv` → `No module named pytest` |
| 契约失败基线可解析性 | `pytest --collect-only -q tests/contract` 名单与 `notes/test-baseline-contract.txt` 的 31 条 node id 做 `comm -23` | 空输出——31 条冻结 node id 在当前树全部可解析（基线冻结于 `756b1f31`，当前 HEAD `01275c5c`，两者相差 2 个纯文档提交） |
| 8 个命令副本存在性 | 逐个 `test -e` 四个工具树 × docs/humanize | 8/8 EXISTS |
| humanize 命令模板形态（Simple 前提） | `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_humanize_command_surface.py -q`；非表格行计数脚本 | `10 passed`；非表格行 40（上限 120）、无 `## Wrap-up`、`SKILL.md` 唯一一处、零 `flow-class-check` 引用 @ 2026-10-24（checklist 修复轮复测） |

**Generation-time premise corrections（实测优先于派发提示）**

- 派发提示称「45 条 C-N 条款」；逐文件实测为 15 + 15 + 10 + 10 = **50**。本文件按实测 50 编排条款分区与 DoD-3；该差异属提示侧的继承前提偏差，按 Input Sanity「Inherited premises」重测并更正，不视为规格缺陷。
- 派发提示要求「只写 tasks 与必要记录」，故本阶段**不代跑** `coverage-baseline.txt` 的冻结与契约失败基线的重采（二者属 `/speckit.implement` 起点动作）；它们分别是 T002、T003 的冻结物，生成时实测状态如实记录在上表。

## Requirement Coverage Map

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T007、T008、T009 |
| FR-002 | T007 |
| FR-003 | T007 |
| FR-004 | T029 |
| FR-005 | T007、T012、T027 |
| FR-006 | T005、T007、T035 |
| FR-007 | T008、T009、T012 |
| FR-008 | T009 |
| FR-009 | T010、T012 |
| FR-010 | T011、T012 |
| FR-011 | T007、T030 |
| FR-012 | T019、T031 |
| FR-013 | T017、T018 |
| FR-014 | T019、T031 |
| FR-015 | T022、T024、T025、T027 |
| FR-016 | T010、T022、T024、T027 |
| FR-017 | T007、T034 |
| FR-018 | T016、T017 |
| FR-019 | T018、T020、T022 |
| FR-020 | T018、T020 |
| FR-021 | T018 |
| FR-022 | T018、T021 |
| FR-023 | T018、T019、T024、T025 |
| FR-024 | T018、T035 |
| FR-025 | T008、T019、T022、T023、T024、T025、T027 |
| FR-026 | T028、T030、T034 |
| FR-027 | T018、T034 |
| SC-001 | T005、T008、T009、T035 |
| SC-002 | T009、T010、T012、T027 |
| SC-003 | T031、T035 |
| SC-004 | T018、T035 |
| SC-005 | T018、T035 |
| SC-006 | T018、T035 |
| SC-007 | T014、T021、T027、T034 |
| SC-008 | T028、T030、T034、T035 |

T001 / T002 / T003（改前基线）、T004 / T005 / T006（分类侧红先测试：台账结构 / 分类正确性 / 引擎单测）、T013（门禁文档测试）、T015（接线测试）、T026 / T033（镜像与副本）、T032 / T036（文档与特性登记）是流程与镜像义务行，按设计不直接映射 FR/SC。`[[STR-001]]` / `[[STR-002]]` / `[[STR-003]]` / `[[STR-004]]` 一律按 requirements.md § Shared Strings 解析，实现与测试不得在 wiring 文本内内联类别字面量。

**Task Distribution**: Setup 3 · US1 9 · US2 15 · US3 4 · Polish 5 · 任务行合计 36。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结改前基线（镜像/副本、结构面、前序规格哈希、非接线文件哈希清单、条款覆盖、契约失败名单），让后续每个「相对基线零新增」判据都有日期化对照物；`notes/` 已就位，供红先取证与基线路由。

- [X] T001 捕获改前基线：创建/更新 `.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-measurements.md` 与机器清单 `notes/pre-change-file-hashes.txt`（74 行 `sha256␠␠<路径>`，覆盖 25 个非接线命令模板 + 49 个非接线技能源），逐项贴真实输出与捕获日期——`python3 scripts/python/sync-mirrors.py --check`（逐对）、`python3 scripts/python/regen-command-copies.py --check`、`python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .`（violations 计数与 kind 集合）、`shasum -a 256` 对 062/067/068 的 `requirements.md`、`git rev-parse HEAD` 与 `git status --short`；本行不写任何源文件。
- [X] T002 [P] 冻结条款覆盖基线：在仓库根运行 `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069a-flow-classification-docs-gates --freeze > .specify/specs/069a-flow-classification-docs-gates/coverage-baseline.txt`（脚本只打印、不写文件）；核对头部两行含 `frozen-from:` 与 `excluding 069a-flow-classification-docs-gates`，并确认基线正文**不含**本切片自己的条款名——`--freeze` 排除被核算的 spec 本身，本切片的 50 个条款只能被认领、不能被自己的基线豁免；冻结口径以该文件头部为唯一记录，不另写第二份清单。
- [X] T003 [P] 在实现起点重采契约套件名字级基线到 `notes/test-baseline-contract.txt`：保留文件头的判据行（zero NEW failing node ids against this list）并更新 HEAD / 日期 / 命令 / 结果四行，采集命令为 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider`；生成时已实测该文件 31 条 node id 在当前树全部可解析（`comm -23` 空输出），若重采后名单变化以新名单为准，并把差值记入 `notes/pre-change-measurements.md`。

**Checkpoint**: 六类基线落盘（镜像/副本、结构面、前序规格哈希、非接线文件哈希、条款覆盖、契约失败名单）；后续「零新增」判据全部有冻结对照物。

---

## Phase 2: User Story 1 - 对任一流程判定它属于执行还是表达，并得到两个人一致的答案 (Priority: P1) 🎯 MVP

**Goal**: 一份唯一所有者（判据 + 两取值 + 边界例 + 78 行逐流程台账 + 类中立封闭清单 + 命名空间消歧 + 变更记录）加一个只读解析引擎（`check` 机械对账、`lookup` 返回类别与默认标记），使分类可复现、可对账、可按单元查询，未声明者在消费点可见地按默认处理。

**Independent Test**: 在自构的临时仓库夹具上跑 `--action check`（用 `--repo` 指向夹具，零缺口 vs 删一行报 `missing`、删光清单报 `inventory-truncated`）与 `--action lookup`（已登记 vs 未登记 vs owner 不可解析三种返回），再跑 `test_flow_class_correctness.py` 的 ≥10 单元 oracle 比对（含变异断言）；独立于 US2 的门禁与接线即可交付「分类可查、缺口可报、判类可被证伪」的价值。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T004 [US1] 红先编写契约测试到 `tests/contract/test_flow_class_ledger.py`：台账 78 行且逐行类别键（[[STR-003]]）恰取二值之一、`/speckit.docs` 与 `/speckit.humanize` 登记为表达类首成员、未登记单元 `lookup` 返回默认类 + `[[STR-004]]` 标记且 `source=default`（不得呈现为已判定）、仓库内无第二份分类数据文件（表格/YAML/JSON/代码常量形态负向断言）、类中立清单封闭（枚举 + rationale + 与台账 `neutral: yes` 的子集关系）、§ 变更记录 行形态 `date | unit_id | before → after | basis | 依据`、`templates/commands/**` 与 `skills/**/SKILL.md` 零类别键赋值字面量（`[[STR-003]]`）；夹具全部自构，运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T005 [US1] 红先编写分类**正确性**测试到 `tests/contract/test_flow_class_correctness.py`：固定 fixture 含 ≥10 个流程单元（两类各 ≥3、未声明 ≥1、类中立 ≥1、混合 oracle ≥1），逐单元断言 `--action lookup` 的类别键（[[STR-003]]） / `source` / `basis` / `marker` 与测试内**独立书写**的 oracle 表相符（不得用被测实现生成期望）；再加一个**变异断言**——在临时副本中把某一单元的类别改错后重跑同一比对，比对 MUST 转红（改对后回绿），使 FR-006 / SC-001 可被机器证伪而不只是结构在场；运行红跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [ ] T006 [US1] 红先编写单元测试到 `tests/unit/test_flow_class_check.py`：台账行解析（列数不符 / 缺必选列 / 单元 id 形态非法 → `row-malformed`，解析器不猜列）、单元 id 归一化（命令 `/speckit.<stem>`、技能 `skill:<dir>`）、`inventory-truncated` 反空真下限（命令 27 / 技能 51）、`--repo` 指向缺 `skills/` 的树时不返回零缺口、退出码阶梯（check 0/1/2、lookup 0/2）、`lookup` 的 `owner-unparsable` 降级分支（默认类语义 + `marker` 为 null + `owner-unavailable`）与「未登记」路径的 `marker` 非空不变量（两标签互斥，FR-016）；运行红跑并写入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T007 [US1] 新建分类所有者 `shared/definitions/flow-class-definitions.md` 的判据与骨架章节：开头声明「唯一所有者 + 它拥有什么」；判据只回答一个问题（主交付物的验收由什么判定）并给出 [[STR-001]] / [[STR-002]] 二分；边界例至少覆盖「Markdown 架构文档 → 表达」「须生成并编译 SDK 的 OpenAPI 契约 → 执行」「站点构建通过不改变判定」三类且理由指向 oracle 而非扩展名；§ 命名空间 消歧类别键（[[STR-003]]）与既有 Agent Execution（指向 `.specify/memory/glossary.md`）；声明与复杂度轴正交（owner：`shared/workflow/feedback-step.md`）、所有权归框架且客户项目只可为自己新增流程声明类别；§ 变更记录 建空表（`date | unit_id | before → after | basis | 依据`）。 [blockedBy: T004,T006] [green: contracts/flow-class-ledger.md#C-1] [green: contracts/flow-class-ledger.md#C-2] [green: contracts/flow-class-ledger.md#C-3]
- [ ] T008 [US1] 在 `shared/definitions/flow-class-definitions.md` 补齐逐流程台账：一行一个流程单元，语法 `| <unit_id> | <类别键 [[STR-003]]> | <basis> | <neutral?> | <notes> |`，覆盖 27 个命令与 51 个技能共 78 行（命令 `/speckit.<stem>`、技能 `skill:<dir>`），`basis` 取 `behavior-oracle` / `reader-oracle` / `mixed-oracle`（`mixed-oracle` 行附父规格指针），`neutral: yes` 只标拟入类中立清单的技能；台账单元集与 `templates/commands/*.md` + `skills/{external,internal}/*/SKILL.md` 双向相等、零 `unknown` 行。 [blockedBy: T007]
- [ ] T009 [US1] 新建 `scripts/python/flow-class-check.py` 并实现 `--action check`：扫描命令与技能清单、解析所有者台账，八类 finding 各自独立报告（`missing` / `unknown` / `duplicate` / `dual-class` / `invalid-class` / `row-malformed` / `neutral-unlisted` / `inventory-truncated`），反空真下限取实测常量（命令 27 / 技能 51，低于即 `inventory-truncated`），`--repo` 默认取脚本自身解析的仓库根且客户项目缺 `skills/` 时报缺口而非静默通过，`--format json` 至少含 `action` / `findings[]` / `checked_at`（ISO-8601 Z），只读零写入，退出码 0/1/2。 [blockedBy: T008] [green: contracts/flow-class-ledger.md#C-4] [green: contracts/flow-class-ledger.md#C-5] [green: contracts/flow-class-ledger.md#C-6]
- [ ] T010 [US1] 在 `scripts/python/flow-class-check.py` 实现 `--action lookup --unit-id <id>`：已登记返回类别键（[[STR-003]]）+ `source=ledger` + `marker=null` + `basis`，未登记返回默认类 [[STR-001]] + `source=default` + `marker=[[STR-004]]` + `basis=null` 且退出码 0（不中断流程），单元 id 形态非法或所有者不可解析返回退出码 2、在 stderr 报 `owner-unparsable` 并保留默认类语义（`marker` 为 null，与「未登记」路径的标记互斥）、MUST NOT 静默切换门禁集；`neutral` 取类中立清单命中。 [blockedBy: T009] [green: contracts/flow-class-ledger.md#C-7]
- [ ] T011 [US1] 在 `shared/definitions/flow-class-definitions.md` 增补类中立封闭清单：每项 `unit_id | category ∈ {memory, feedback, evidence, session} | rationale`（一句话说明它为何没有自己的交付物），清单 ⊆ 台账且对应行 `neutral: yes`，清单外出现 `neutral: yes` 由检查器报 `neutral-unlisted`；明文写「类中立只豁免命令↔委托技能同类约束，不豁免任何门禁」。 [blockedBy: T010] [green: contracts/flow-class-ledger.md#C-8]
- [ ] T012 [US1] US1 定向转绿与取证：用 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract/test_flow_class_ledger.py tests/contract/test_flow_class_correctness.py tests/unit/test_flow_class_check.py -q -p no:cacheprovider` 跑到全绿（只读执行；正确性测试的变异断言同批转绿）并把绿证据追加 `notes/red-first-evidence.md`；另跑 `python3 scripts/python/flow-class-check.py --action check --format json`（期望 `units` = 78 且 `findings` 为空）与两次 `--action lookup`（`/speckit.docs`、一个未登记 id），贴真实输出。 [blockedBy: T011]

**Checkpoint**: US1 独立可验收——台账 78 行零缺口、未登记单元带默认标记、类中立封闭、`check` / `lookup` 的面与退出码符合契约、≥10 单元 oracle 比对与变异断言能证伪分类；MVP 前半就位。

---

## Phase 3: User Story 2 - 文档型特性走完整 SDD，但面对的是文档型门禁 (Priority: P1) 🎯 MVP

**Goal**: 一份门禁 owner（六面各指单一既有 owner、8 阶段算子表、调用点表、阻断级别、读者声明形态、证据等级与 as-of 语法、构建非充分、事实唯一性修复方向、评审读者基准、三项基线协议、算子去重）+ 一个事实一致性检查器（reader / evidence / duplicate 三面 + count 委派）+ 四个最小接线点（W1/W2 命令模板、W3/W4 技能）与命令副本重生成，使门禁真正被入口执行而不是只落在文档里。

**Independent Test**: 在自构夹具（含三类 SC-007 注入）上跑 `doc-consistency-check.py --action verify`，核对三类注入各被报出、排除项零误报、计数字段显式；再对两个模板与两个技能跑接线断言（A1–A7）与 8 个副本内容断言，独立于 US3 的兼容面即可交付「门禁可执行 + 接线封闭」。

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T013 [US2] 红先编写契约测试到 `tests/contract/test_expression_gates_doc.py`：六面**恰好 6**（多于 6 或少于 6 均失败）且每面恰一个 face id 与一个可解析 `owner_pointer`（路径 + 章节锚）、逐阶段算子表覆盖 8 阶段且行数 ≥ 8、调用点表覆盖 W1–W4 且 docs 行含 `doc-consistency-check.py --action verify`、W2 行声明「不读取类别」、W4 行含该流程唯一的 `--action lookup`、humanize 算子行不含 `structure-links-build` 与需求清晰度且不被表述为六面子集、六面各 ≥ 1 blocking 且读者声明缺失为阻断、证据等级封闭三值 + `source` 必填（含 `source-missing`）与 `YYYY-MM-DD` as-of 成组规则在场、结构面「零新增」与 `not-applicable` 明文在场、三项基线来源表在场、全文与台账无「表达类可跳过/缩短/改判阶段」表述；运行红跑并写入 `notes/red-first-evidence.md`。
- [ ] T014 [US2] 红先编写 `tests/contract/test_doc_consistency_checker.py` 与 `tests/unit/test_doc_consistency_rules.py`：三面规则在夹具上红/绿、SC-007 三类注入（引用改 owner 原文副本 / `as-of` 改旧 / 派生计数手打）各被报出一次且漏报 = 0、排除项（`notes/`、`review.md`、`verification.md`、fence 内行、表格分隔行、纯链接行、短行、纯日期/版本行）零误报、计数面委派不可用时 `count_check.status=not-run` 显式且 `--strict` 下计失败、归一化与相似度阈值边界（完全相等 ≥ 24 字符 / ratio ≥ 0.90 且 ≥ 40 字符）、`--spec-dir` 与 `--path` 双缺 → 退出码 2；运行红跑并写入 `notes/red-first-evidence.md`。
- [ ] T015 [US2] 红先编写契约测试到 `tests/contract/test_expression_gate_wiring.py`（A1–A7）：W1 接线小节含 `flow-class-check.py` / `--action lookup` / `"/speckit.docs"` / 两个 owner 路径 / `doc-consistency-check.py` 且位于 `## Outline` 之后 `## Wrap-up` 之前；W2 小节**只含**两个 owner 路径，且不得出现 `flow-class-check.py` / `--action lookup` / `--unit-id` / `doc-consistency-check.py` / `feedback-utils.py` / `probe-utils.py` 任一（命令保持 Simple、零脚本调用），全文仅一处 `SKILL.md`、无 `## Wrap-up`、非表格行数 ≤ 120（行数上限，不是字符长度）；W3/W4 技能含门禁 owner 引用，`create-docs` 含 checker，`humanize` 含 `flow-class-check.py` / `--action lookup` / `"/speckit.humanize"` 且保留 `Stage 6 — 保真自检` 段与 `diff_protected.py` 引用；接线文本剔除 owner 路径后无独立 `expression` / `execution` 词与归属断言、全文无类别键赋值形态（正则键名取 `[[STR-003]]`）与「unit id ‖ 类别取值」台账样式行；其余 25 个模板与 49 个技能零引用（接线封闭）；8 个命令副本中 docs 副本各含 lookup 与 owner 指针、humanize 副本各含两个 owner 指针且不含 `flow-class-check.py`；062 / 067 / 068 的 `requirements.md` sha256 与冻结值一致。

### Implementation for User Story 2

- [ ] T016 [US2] 新建 `shared/workflow/expression-gates.md` 的六面清单（**封闭集，恰好 6**）：六面（需求清晰度、读者/目的/边界、证据分级与 as-of、结构/链接/构建、事实一致性、评审）各登记且仅登记一个 face id 与一个 `owner_pointer`——`requirements-clarity` → `scripts/python/validate-requirements.py` + `shared/guidelines/requirements-guidelines.md`；`reader-purpose` → `shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议；`evidence-asof` → 本文件新增面；`structure-links-build` → `skills/external/create-docs/SKILL.md` § Desired-State Baseline + `skills/external/create-docs/scripts/docs-utils.py`；`fact-consistency` → `shared/guidelines/one-source-of-truth.md`；`review` → `skills/internal/review-sdd-process/SKILL.md` + `templates/review-template.md`；明文写「面数 = 6，新增面须由后续特性修订本 owner」；声明新增面之外不复述这些 owner 的判据句。 [blockedBy: T013] [green: contracts/expression-gate-operators.md#C-1]
- [ ] T017 [US2] 在 `shared/workflow/expression-gates.md` 增补逐阶段算子表与阻断级别：8 阶段（requirements → clarify → plan → tasks → checklist → analyze → implement → review）各至少一行「阶段 | 执行算子 | 对应面 | 阻断级别」且行数 ≥ 8；六面各至少一个 `blocking` 算子、需求清晰度/事实一致性/评审三面必有 blocking、读者声明缺失为阻断；写入「不得把表达类读作更宽松通道 / 不得把既有 P0/P1 降为 advisory」的负向条款；humanize 调用点只执行最小算子集且 MUST NOT 被写成六面的子集或精简版。 [blockedBy: T016] [green: contracts/expression-gate-operators.md#C-2] [green: contracts/expression-gate-operators.md#C-3]
- [ ] T018 [US2] 在 `shared/workflow/expression-gates.md` 增补规则面：读者声明两行形态（前 40 个非空行内 `**Readers**:` / `**Reading scenario**:`，缺失或空值即 `reader-declaration-missing` 阻断，沿用基准读者不新建第二套）；证据等级封闭三值（实测 / 推断 / 引用）+ `YYYY-MM-DD` as-of + **来源必填**的三件套成组规则（`实测`/`推断` 的 source 是可复算命令或退出状态，`引用` 的 source 是引文出处；缺来源即 `source-missing` 阻断）+ 对象边界（不重定义 `shared/workflow/evidence-step.md` 七态、不并入 `shared/guidelines/single-run-evidence.md`）；结构/链接/构建通过只是必要条件、判据写「零新增违规」、站点层缺席记 `not-applicable`；同一事实唯一 owner、≥2 处手写即缺陷、修复方向是改为引用、派生计数由制品导出且手工计数交由既有计数判定，并承认机械检测下限（完全相等 ≥24 字符 / 相似度 ≥0.90 且 ≥40 字符）；评审按读者基准（判定者 = 人工评审者或受委托的评审代理，判定对象 = 读者理解与事实相符）且在 analyze 与 review 两阶段在场；三项基线（门禁调用次数 / 人工确认次数 / requirements→analyze 墙钟）的来源命令表、「开工前 = requirements 首次提交」与「无来源记 null」规则、单阶段确认 ≤3；算子去重规则（同一产物变更同算子只跑一次、不继承代码型算子、去重不减面数与阻断级别）。 [blockedBy: T017] [green: contracts/expression-gate-operators.md#C-4] [green: contracts/expression-gate-operators.md#C-5] [green: contracts/expression-gate-operators.md#C-6] [green: contracts/expression-gate-operators.md#C-7] [green: contracts/expression-gate-operators.md#C-8] [green: contracts/expression-gate-operators.md#C-9] [green: contracts/expression-gate-operators.md#C-10]
- [ ] T019 [US2] 在 `shared/workflow/expression-gates.md` 增补不变量与调用点表：阶段完整性由既有阶段记录判定、类别 MUST NOT 参与、analyze 与 review 调用率 100%、以表达类为由跳过/缩短/改判的请求被明文拒绝且无例外；首批成员 `/speckit.docs` 与 `/speckit.humanize` 只补强不削弱（humanize 命令保持 Simple）；与复杂度轴正交（`shared/workflow/feedback-step.md` 只加一行指针，不改其判据段落）；调用点表四行（W1 `/speckit.docs`、W3 `skill:create-docs`、W2 `/speckit.humanize`、W4 `skill:humanize`）给出时点 / 类别读取 / 执行算子 / 阻断——W2 行声明「不读取（只给 owner 指针）」、W4 行承载该流程唯一的 lookup，docs 行覆盖六面、humanize 行登记 `062-*` 最小集且不含六面全集；调用时机与降级（lookup 先于判定且同一产物变更只读一次、`source: default` 原样显示标记、owner 或引擎缺席显示 `owner-unavailable` 并保持既有门禁、技能被独立调用时仍按其调用点行读取、命令与技能重叠时复用一次执行、不改判定阈值/阶段集合/P0-P1）。 [blockedBy: T018] [green: contracts/expression-gate-operators.md#C-11] [green: contracts/expression-gate-operators.md#C-12] [green: contracts/expression-gate-operators.md#C-13] [green: contracts/expression-gate-operators.md#C-14] [green: contracts/expression-gate-operators.md#C-15]
- [ ] T020 [US2] 新建 `scripts/python/doc-consistency-check.py` 并实现命令面与 `reader` / `evidence` 两面：`--action verify` + `--spec-dir` / `--path`（至少给一个，双缺退出码 2）+ `--faces`（缺省 `reader,evidence,duplicate,count`，未知面名退出码 2）+ `--strict` / `--format` / `--json-out`；S1 形式产物集合、S2 显式文档、S3 判据 owner 路径常量，排除项写成实现常量闭集；`reader` 面前 40 非空行两行声明、`--path` 缺省时输出 `not-applicable`；`evidence` 面 `grade-asof-unpaired` / `as-of-malformed` / `as-of-stale`（时钟取 `git log -1 --format=%cs -- <path>`，非 git 或无提交历史输出 `not-evaluated` + reason）/ `grade-invalid` / `source-missing`（有等级或 as-of 但 source 缺失/为空）五条 blocking 规则；只读、不写除 `--json-out` 外的任何文件。 [blockedBy: T014] [green: contracts/doc-consistency-checker.md#C-1] [green: contracts/doc-consistency-checker.md#C-2] [green: contracts/doc-consistency-checker.md#C-3] [green: contracts/doc-consistency-checker.md#C-4]
- [ ] T021 [US2] 在 `scripts/python/doc-consistency-check.py` 实现 `duplicate` / `count` 两面与输出契约：归一化（去列表/引用前缀、压连续空白、去行尾标点、ASCII 大小写折叠）与命中条件（完全相等且 ≥ 24 字符，或 `difflib.SequenceMatcher` ratio ≥ 0.90 且 ≥ 40 字符），跨 ≥ 2 个不同文件才报、同文件内重复不报，`path/line` 取字典序首处 + `counterpart` 取第二处 + `fix_direction` 恒为「改为对唯一 owner 的引用」；`count` 面委派 `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py`（`--spec-dir --stage <plan|tasks> --json-out`）并把 count 类 finding 映射为 `count-mismatch`，委派目标缺席或返回码 2 时输出 `count_check.status=not-run` + reason；JSON 输出 schema（`action` / `checked_at` / `scope` / `faces` / `findings[]` / `count_check`）；退出码 0/1/2 且不得 0 退出同时带 finding、`--strict` 把 `not-evaluated` 升级为 1。 [blockedBy: T020] [green: contracts/doc-consistency-checker.md#C-5] [green: contracts/doc-consistency-checker.md#C-6] [green: contracts/doc-consistency-checker.md#C-7] [green: contracts/doc-consistency-checker.md#C-8]
- [ ] T022 [US2] 接线 W1：在 `templates/commands/docs.md` 的 `## Outline` 内、`### 技能输入` 之前新增一个 `###` 小节（不改既有 `## ` 顶级章节序列）：① 判定前执行一次 `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs"`；② 指针到 `shared/definitions/flow-class-definitions.md` 与 `shared/workflow/expression-gates.md`，并按门禁 owner 的 `/speckit.docs` 调用点行执行文档型算子（含 `doc-consistency-check.py --action verify`）；③ 降级可见：`source: default` 原样显示 `marker`，脚本缺席或退出码 2 显示 `owner-unavailable` 并保持既有门禁、不中断、不静默切换门禁集；小节内禁类别字面量与归属断言、禁判据或算子表副本。 [blockedBy: T010,T019,T021] [green: contracts/flow-class-ledger.md#C-9]
- [ ] T023 [US2] 接线 W3：在 `skills/external/create-docs/SKILL.md` 的 `### Reconcile Loop` R6 verify 与 `### Authoring Flow` R6 验证两处各补同一句（`### Desired-State Baseline` 是结构/链接/构建面的既有 owner，不向其加内容）：指针到 `shared/workflow/expression-gates.md`，并写明「当调用方已解析为文档型算子集时，对受触文档执行 `doc-consistency-check.py --action verify`；owner 或引擎缺席时显式跳过」；不得复制门禁规则、不得把 checker 变成无条件硬依赖、不得断言类别归属。 [blockedBy: T022]
- [ ] T024 [US2] 接线 W2：在 `templates/commands/humanize.md` 的 `## Outline` 内、委派段之前新增一个 `###` 小节——**只**给两个 owner 指针（`shared/definitions/flow-class-definitions.md` + `shared/workflow/expression-gates.md`），并写明「类别读取与最小算子集执行由委派技能的 Stage 6 承担」（不写该技能路径，全文 `SKILL.md` 仍只能出现一次）；MUST NOT 出现 lookup / `flow-class-check.py` / `--unit-id` / 任何脚本调用（命令保持 Simple）、禁 `doc-consistency-check.py`、`## Wrap-up`、六面算子表与类别归属断言；非表格行**数**仍 ≤ 120（行数上限，不是字符长度）。 [blockedBy: T023]
- [ ] T025 [US2] 接线 W4：在 `skills/external/humanize/SKILL.md` 的 `### Stage 6 — 保真自检（交付前）` 段首增补——① 判定前执行一次 `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.humanize"`（该流程**唯一**的类别读取，同一次运行只读一次）；② 一句 owner 指针（本技能参与的门禁算子集登记在门禁 owner 的 humanize 调用点；执行细则仍以本文件 Non-negotiables 与 Stage 6 为准）；③ owner/引擎缺席时显式降级（`owner-unavailable` 或默认标记），不中断改写；不得复制算子表、不得断言类别归属、不改 062 的默认输出与报告契约、不回指命令模板路径。 [blockedBy: T010,T024]
- [ ] T026 [US2] 重生成每工具命令副本并核零漂移：`python3 scripts/python/regen-command-copies.py` 后 `python3 scripts/python/regen-command-copies.py --check` 必须 `OK`，并逐副本确认 `.claude/commands/speckit.docs.md`、`.github/prompts/speckit.docs.prompt.md`、`.opencode/command/speckit.docs.md`、`.qoder/commands/speckit.docs.md` 各含 `flow-class-check.py` 与 `expression-gates.md`，`.claude/commands/speckit.humanize.md`、`.github/prompts/speckit.humanize.prompt.md`、`.opencode/command/speckit.humanize.md`、`.qoder/commands/speckit.humanize.md` 各含 `flow-class-definitions.md` 与 `expression-gates.md` 且**不含** `flow-class-check.py`（与其源模板一致）；副本属生成物，MUST NOT 手写。 [blockedBy: T025]
- [ ] T027 [US2] US2 定向转绿与取证：运行 `tests/contract/test_expression_gates_doc.py`、`tests/contract/test_doc_consistency_checker.py`、`tests/unit/test_doc_consistency_rules.py`、`tests/contract/test_expression_gate_wiring.py` 至全绿（只读执行），绿证据追加 `notes/red-first-evidence.md`；并实测两条降级面：`--repo` 指向无 `skills/` 的临时空树跑 `flow-class-check.py --action check`（期望非零退出且报缺口）、对无台账的临时所有者跑 `--action lookup`（期望默认类语义 + `marker` 为 null + `owner-unparsable`，两标签互斥）；把两条真实输出一并留证。 [blockedBy: T026] [green: contracts/flow-class-ledger.md#C-10] [green: contracts/flow-class-ledger.md#C-11] [green: contracts/doc-consistency-checker.md#C-9] [green: contracts/doc-consistency-checker.md#C-10]

**Checkpoint**: US2 独立可验收——六面与阶段算子表结构完整、检查器三面在夹具上按 SC-007 命中、四个接线点就位且接线封闭、8 个副本含接线；与 US1 合并即 MVP：分类可查 + 门禁可执行。

---

## Phase 4: User Story 3 - 分类不能被当作跳过 analyze/review 的开关 (Priority: P2)

**Goal**: 把「表达类所以可以轻一点」这条读法挡在机制层面——类别与复杂度轴显式正交、阶段完整性与调用率判定不读类别、任何以类别为由跳过/缩短/改判的请求被明文拒绝；同时钉住前序三特性只被引用不被改写、零新命令、零项目侧存储、接线面封闭。

**Independent Test**: 读两个 owner 文档与四个接线点，机械检索「跳过/缩短/改判」表述（唯一命中必须是拒绝规则本身）、确认阶段完整性段落零类别键（[[STR-003]]）读取、确认 `templates/commands/` 文件集与 062/067/068 的 `requirements.md` 字节不变——不需要 US2 的运行时夹具即可独立核对。

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [ ] T028 [US3] 红先编写契约测试到 `tests/contract/test_expression_compatibility.py`：`templates/commands/` 文件集 = 27 个名字集合不变、`skills/{external,internal}/*/SKILL.md` = 51 个名字集合不变；`notes/pre-change-file-hashes.txt` 里 25 个非接线模板 + 49 个非接线技能 sha256 全部不变；062 / 067 / 068 的 `requirements.md` sha256 与冻结值一致；`src/specify_cli/`、`AGENTS.md`、`.specify/instructions.md` 相对基线哈希零改动；零新增命令；仓库内零新增项目侧存储路径（`.specify/memory/` 下无分类数据文件）；接线封闭集之外零引擎/owner 引用；`.specify/` 镜像与源同字节；运行红跑并写入 `notes/red-first-evidence.md`。 [blockedBy: T001]

### Implementation for User Story 3

- [ ] T029 [US3] 在 `shared/workflow/feedback-step.md` 增补一行正交指针（既有复杂度判据与红线段落零改动）：声明复杂度轴决定 wrap-up 面有无、类别轴决定门禁算子集、两轴不互相推导，判据与台账归 `shared/definitions/flow-class-definitions.md`；该文件不得复制判据或台账。 [blockedBy: T007]
- [ ] T030 [US3] 兼容面转绿并取证：运行 `tests/contract/test_expression_compatibility.py` 至全绿（只读执行），绿证据追加 `notes/red-first-evidence.md`；另实测「未刷新项目」形态——`git show <改前 HEAD>:templates/commands/docs.md` 与同法 humanize 模板不含 `flow-class-check.py`（零调用点、行为与接线前逐字一致），并核对 `pyproject.toml` 的 `force-include` 与 `src/hatch_build.py` 覆盖四类载荷（`shared/`、`scripts/`、`templates/`、`skills/`）以证同包原子性；`<改前 HEAD>` 取 `notes/pre-change-measurements.md` 记录值。 [blockedBy: T028] [green: contracts/compatibility-distribution.md#C-1] [green: contracts/compatibility-distribution.md#C-2] [green: contracts/compatibility-distribution.md#C-3]
- [ ] T031 [US3] 防滥用审计（只读核对并留证）：① 在 `shared/definitions/flow-class-definitions.md` 与 `shared/workflow/expression-gates.md` 检索「跳过 / 缩短 / skip / exempt」类表述，确认唯一命中是拒绝规则本身且不带例外；② 确认阶段完整性判定段落不出现类别键（[[STR-003]]）读取（命中即判缺陷）；③ 确认 analyze 与 review 调用率 100% 的明文在场；④ 用 `grep -c` 记录两个命令模板的类别赋值字面量为 0；把四条命令与真实输出写入 `notes/red-first-evidence.md` 的防滥用小节。 [blockedBy: T030]

**Checkpoint**: US3 独立可验收——正交声明与阶段不变量在读面上无漏洞、前序三规格字节不变、零新命令与零项目侧存储成立、接线面封闭可机械核对。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 收口文档同步、镜像与副本、全量回归、SC 证据与特性登记；不改任何实现语义。

- [ ] T032 [P] 文档同步评估与补齐：按 `.specify/shared/workflow/docs-step.md` § Evaluation procedure 判断 `docs/reference/commands/docs.md` 与 `docs/reference/commands/humanize.md` 是否因接线而失真，失真时只补一行指针（不复制判据或算子表）；随后跑 `python3 skills/external/create-docs/scripts/docs-utils.py --action validate --root .` 核对 `violations` 计数与 kind 集合相对 T001 基线零新增；结论写入 `verification.md` 的 docs-sync 小节。
- [ ] T033 [P] 镜像同步与逐对核验：`python3 scripts/python/sync-mirrors.py --write --only shared --only scripts --only skills` 后 `python3 scripts/python/sync-mirrors.py --check` 相对 T001 基线零新增差异；用 `cmp` 逐对核对 7 个源文件与其 `.specify/` 镜像同字节（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、`shared/workflow/feedback-step.md`、`scripts/python/flow-class-check.py`、`scripts/python/doc-consistency-check.py`、`skills/external/create-docs/SKILL.md`、`skills/external/humanize/SKILL.md`）；禁止手改镜像。
- [ ] T034 全量收口核验：① 全量契约套件 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider` 的失败 nodeid 排序后与 `notes/test-baseline-contract.txt` 做 `comm -13`，零新增；② `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069a-flow-classification-docs-gates` 报告 claimed = 50 且 uncovered beyond baseline = 0；③ 重跑 quickstart 场景 1/2/3/4/6 并把真实输出贴 `notes/quickstart-run.md`；④ 复核 `flow-class-check.py --action check` 在本仓为零 finding、在无 `skills/` 的临时目录报 `inventory-truncated`（客户项目形态），并复核 `--action check` 零文件写入；⑤ 确认除 W1/W2 两个模板、W3/W4 两个技能与 `shared/workflow/feedback-step.md` 外零源文件改动。 [blockedBy: T033] [green: contracts/compatibility-distribution.md#C-4] [green: contracts/compatibility-distribution.md#C-5] [green: contracts/compatibility-distribution.md#C-6] [green: contracts/compatibility-distribution.md#C-7] [green: contracts/compatibility-distribution.md#C-8] [green: contracts/compatibility-distribution.md#C-9] [green: contracts/compatibility-distribution.md#C-10] [green: contracts/flow-class-ledger.md#C-12] [green: contracts/flow-class-ledger.md#C-13] [green: contracts/flow-class-ledger.md#C-14] [green: contracts/flow-class-ledger.md#C-15]
- [ ] T035 逐 SC 落 `verification.md` 与三项基线记录：`- **SC-001**` … `- **SC-008**` 各带状态、命令、输出摘要与证据指针；SC-001 先记 `test_flow_class_correctness.py` 的机械核验结果（≥10 单元 oracle 比对 + 变异断言），再记两名独立判定者的复现演练（隔离结论后逐条比对）或写明未执行的 reason（不得记达成）；SC-003 / SC-004 / SC-005 / SC-006 在真实样本不足时记 `not-evaluated` + reason（不记 0、不记达标）；SC-007 记三类注入的命中与漏报集合；SC-008 记三份前序规格的 sha256 复算值；同时落 `notes/expression-baseline.md`（三项基线冻结值 + `compared_at`，无来源记 null）。 [blockedBy: T034]
- [ ] T036 回填特性登记：在 `.specify/memory/features/069.md` § Related Specifications/Requirements 追加 `tasks.md` 指针与本切片任务规模（36 任务行），确认 `.specify/memory/features.md` 的 069 行零新增、零删除、状态仍为 Planned（Implemented 转移属 `/speckit.implement`）。 [blockedBy: T035]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始——但它是后续所有「相对基线零新增」判据的分母。
- **User Story 1 (Phase 2)**: 依赖 Setup 的基线落盘；故事内部严格 TDD（红 → 实现 → 转绿）。
- **User Story 2 (Phase 3)**: 依赖 Setup；`T022`（W1）显式依赖 `T010`（lookup 引擎）、`T019`（调用点表）与 `T021`（checker），因此 US2 在 US1 之后自然串行。
- **User Story 3 (Phase 4)**: 依赖 US2 的接线面存在（`T028` 依赖 Setup 的哈希清单；`T030` / `T031` 以 US2 的落盘为核对对象）。
- **Polish (Phase 5)**: 依赖全部故事完成；`T034` 依赖 `T033`（镜像先同步再全量核验）。

**本特性无 Foundational 阶段**：US1 与 US2 的写目标不重叠（分类侧 = owner + 台账 + `flow-class-check.py`；门禁侧 = gates owner + `doc-consistency-check.py` + 四个接线点），唯一共享前提（基线与哈希清单）已在 Setup 落盘；按模板规则整段省略并顺延阶段编号，避免留空章节。

### Within Each User Story

- 测试行先写并确认红，再进入实现行；转绿行在该故事末尾统一取证。
- US1：owner 判据骨架 → 台账 → 引擎 `check` → 引擎 `lookup` → 类中立清单 → 转绿（含正确性测试的 oracle 比对与变异断言）。
- US2：三支红测试 → 门禁 owner 四段（面 → 阶段表 → 规则 → 不变量与调用点）→ 检查器两面 → 接线 W1/W3/W2/W4 → 副本重生成 → 转绿。
- US3：红测试 → 正交指针 → 兼容转绿 → 防滥用审计。

### Parallel Opportunities

- Setup：`T002`（覆盖基线）与 `T003`（契约失败基线重采）可并行；`T001` 先落盘以免与二者抢同一文件。
- US1 内部：`T004`、`T005` 与 `T006` 写不同测试文件，可并行；`T007` 起为串行（同一 owner 文件与同一引擎文件）。
- US2 内部：`T013`、`T014`、`T015` 三支红测试写不同文件，可并行；`T020` / `T021` 串行同一引擎文件；四个接线点串行（`T022`→`T023`→`T024`→`T025`），因其后续断言相互依赖。
- Polish：`T032`（docs）与 `T033`（镜像）可并行；`T034` 之后 `T035`、`T036` 串行。

## Parallel Example: Phase 1 Setup

```bash
# 两支基线互不写同一文件，可同时开：
python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/069a-flow-classification-docs-gates --freeze > .specify/specs/069a-flow-classification-docs-gates/coverage-baseline.txt
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider
```

## Implementation Strategy

### MVP First

MVP 覆盖 **US1 + US2 两个 P1 故事**：分类若无读取点就只是文档，门禁若无分类读取就只是另一份文档，二者合并才构成一个可独立演示的增量（「查得出类别、跑得动文档型门禁、接线封闭」）。

1. 完成 Phase 1（基线与哈希清单），确认六类分母就位。
2. 完成 US1（Phase 2）→ 跑 Checkpoint：台账零缺口、未登记带标记、`check`/`lookup` 面与退出码合规。
3. 完成 US2（Phase 3）→ 跑 Checkpoint：六面与阶段表结构完整、检查器在 SC-007 三类注入上命中、四个接线点与 8 个副本就位。
4. **STOP and VALIDATE**：以 quickstart 场景 1/2/4 人工复核 MVP。
5. 完成 US3（Phase 4）→ 防滥用与兼容面独立核验。
6. 完成 Polish（Phase 5）→ 文档、镜像、全量回归、SC 证据、特性登记。

### Incremental Delivery

1. Setup → 基线可对照（无用户可见行为）。
2. US1 → 交付「分类可查、缺口可报」。
3. US2 → 交付「文档型门禁可执行 + 最小接线」。
4. US3 → 交付「类别不可作为跳过开关 + 兼容不回归」。
5. Polish → 交付可验收证据链（SC 逐条 + 全量零新增失败）。

---

## Notes

- `[P]` 行 = 写目标不同且无未完成依赖；同一文件的连续增补一律串行（owner 与引擎文件均如此）。
- 所有「相对基线零新增」判据的分母都在 § Measured Premises 与 T001 落盘的 `notes/pre-change-measurements.md`；任务行只引用，不复述基线值。
- 接线文本（两个模板与两个技能）MUST NOT 出现类别字面量、类别归属断言、判据或算子表副本——类别只能由 `flow-class-check.py --action lookup` 的运行结果给出；这是 A4 断言与 FR-015 的同一件事。
- 结构面判据是「零**新增**违规」（基线已有 `broken-link` 2 + `note-frontmatter` 1）；写成「全绿」会与既有债冲突，本切片不修也不掩盖他特性的登记债。
- 契约套件判据是「零**新增**失败 nodeid」（基线 31 红）；`pytest` 只存在于 `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`，不得假设 `python3 -m pytest` 可用。
- 062 / 067 / 068 只被引用不被改写；`069b` 的同构映射、迁移机制与度量仪器不在本切片，任何任务行都不得把它们预置进调用点表。
- 提交纪律：只提交本特性产物（显式路径），不夹带运行期记录与他命令的未提交工件；本 tasks 阶段不 push。
