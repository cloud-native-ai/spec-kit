# Tasks: 项目文档的 SDD 接入（特性级类别与文档型阶段门禁） — 077

**Requirement ID**: 077
**Requirement Key**: `077-doc-sdd-integration`
**Branch**: `077-doc-sdd-integration`（本阶段禁止切换或新建分支；不 push）
**Related Feature**: Feature 077 — 项目文档的 SDD 接入（特性级类别与文档型阶段门禁）, status `Planned`（tasks 阶段不推进状态机；`Planned → Implemented` 归 `/speckit.implement`，活状态只在 `.specify/memory/features.md` 的 077 行）
**Input**: Design documents from `.specify/specs/077-doc-sdd-integration/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required；25 FR / 8 SC / 4 用户故事 / 6 Shared Strings）、`research.md`（R-1…R-13）、`data-model.md`（E1–E9 + 校验规则汇总，行数以该文件为准）、`contracts/`（6 份文件 / 77 条款，全部 `md-bold-closed`）、`quickstart.md`（S1–S7）、`feature-ref.md`

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」把测试定为先写后实现；本特性五个新测试文件全部红先行（起点是本次实测的三处红：`spec:` 键退出码 2、`--action structure` 退出码 2、七模板零命中）。同时按 Principle VII 的 **template-only 门**：交付面（七份命令模板、两份 owner、驱动 references、两个既有引擎）没有可跑的运行时，它们的「测试」是**结构契约测试**——子节计数与逐字文本、剥离后与基线提交字节相同、退出码与记录字段、码集封闭、正文卫生。两层都发，且不互相替代。

**Tests**: 五组红先行各写一个文件并在未改动树上跑出**记录在案的失败**（重放命令 / 真实输出 / 退出码 / 失败计数四字段，落入 `notes/red-first-evidence.md`）：`tests/unit/test_flow_class_spec_key.py`（`spec:` 键族）、`tests/contract/test_flow_class_spec_declaration.py`（声明行与四码）、`tests/contract/test_stage_class_wiring.py`（七模板接线 + execution 零变化反向守卫）、`tests/contract/test_document_structure_gate.py`（`--action structure`）、`tests/contract/test_docs_gate_driver.py`（驱动载荷 / U4 / 槽位）。既有闭合集守卫 `tests/contract/test_expression_gate_wiring.py` 的名册修订属**实现后守卫**（迁移/回归例外），排在七模板接线之后，携带显式 `[blockedBy:]`，不作红先行声称。

**Organization**: 按 `requirements.md` 的四个用户故事分组（US1–US3 为 P1，US4 为 P2）；Setup 与 Polish 行无故事标签。77 条契约条款由 19 行以 `[green:]` 认领，每条款恰好一行、同文件内条款序随行序递增（§ Clause Partition）。本特性无阻断全部故事的前置，Foundational 相位按模板指引省略——证据槽（T001）是唯一共享前置。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/077-doc-sdd-integration/verification.md` 的 `deferred_tasks=`。
- DoD-2: 77 条契约条款各被恰好一行 `[green:]` 认领；`python3 scripts/python/account-clause-coverage.py .specify/specs/077-doc-sdd-integration` 报 `status: ok`、claimed=77、beyond baseline=0、FR 车道 `FR uncovered: 0`（25/25）。
- DoD-3: 五个新测试文件全部红先行（`notes/red-first-evidence.md` 每组四字段记录）并转绿；execution 零变化反向守卫同时断言「子节存在」与「剥离后与基线提交 `c1cd4600` 逐字相同」，不得在无接线时空转。
- DoD-4: 两个引擎扩展只用标准库、只读、无常驻进程，退出码 0/1/2（另有一个退出码 0 的 advisory 码 `declaration-absent`，不阻断、不计缺陷）；`doc-consistency-check.py --faces` 仍为四面，六面 owner 的封闭集不变（不新增第七个门禁面）。
- DoD-5: 分发判据是「相对改动前基线零新增漂移」——`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均不再出现新增 DIFF；`templates/commands/**` 不入 templates 镜像对，只经 per-tool 命令副本分发。
- DoD-6: 七个阶段模板按 `research.md` R-9 的剥离算法（起点＝子节标题行，终点＝其后第一个 `^#{1,3} ` 行前一行；块末恰一个空行）删去接线子节后，与基线提交 `c1cd4600` 的同名文件 **SHA-256 相等**，且同时断言子节在场（防空绿）；哈希以 2026-10-30 实测值钉入测试常量，见 § Measured Premises。
- DoD-7: `verification.md` 为 SC-001…SC-008 各记录一条状态行，词表归 `.specify/templates/verification-log-template.md`；表达类 implement 的 Test-First 按宪法 VII 的 template-only 条款记 `Partial (justified)` 并写明替代验证是四项文档门禁输出。
- DoD-8: 不新增 `/speckit.*` 命令、不引入运行时调度器 / 评分器 / 常驻服务、不新增第三方依赖；Feature 077 在 tasks 阶段结束时保持 `Planned`（`Implemented` 由 `/speckit.implement` 拥有）。
- DoD-9: plan 属主制品（`plan.md` / `requirements.md` / `research.md` / `data-model.md` / `contracts/*` / `quickstart.md` / `feature-ref.md`）不被重写；确需修订时先行声明 `PLAN-EDIT: <path> — <reason>；分类=minor|substantive`，substantive 必须停止并回传异常行。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 scripts/python/validate-tasks.py .specify/specs/077-doc-sdd-integration/tasks.md` 退出 0，0 error / 0 warning（含四条 green-* 判定）。
- GATE-2: 跨制品一致性 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/077-doc-sdd-integration --stage tasks --repo .` 报 `decision=pass`、`errors=0`；`missing-path` advisory 只允许命名本特性将新建的文件（`notes/*`、五个测试文件）、plan 期既有的待建清单，以及 quickstart 场景临时目录（`.specify/.tmp/**`——S6 的夹具目录，已由 `.specify/.gitignore` 覆盖、不落仓库，故不可能存在于树上）；任何其它路径的 advisory 是缺陷。
- GATE-3: 拆解尺度门 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/077-doc-sdd-integration/requirements.md --tasks .specify/specs/077-doc-sdd-integration/tasks.md` 报 `decision=proceed`、`task_count` ≤ 40。
- GATE-4: 条款覆盖 — check: `python3 scripts/python/account-clause-coverage.py .specify/specs/077-doc-sdd-integration` 报 `status: ok`、claimed=77、beyond baseline=0；非零 beyond-baseline 用认领修复，永不重冻结基线。
- GATE-5: 新组转绿且既有守卫无新增失败 — check（实现期，经 profiles venv 的 `python -m pytest -q`）：五个新测试文件全绿，`tests/contract/test_expression_gate_wiring.py` 全绿，且既有守护套件失败名集合相对 `test-evidence/plan-targeted-tests-baseline.txt` 无新增（捕获与比较形式归 `/speckit.implement` step 6 的 `**Test runs**` bullet，此处引用不重述）。
- GATE-6: 镜像无新增漂移 — check: `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对 `test-evidence/plan-sync-mirrors-baseline.txt` / `test-evidence/plan-regen-command-copies-baseline.txt` 无新增 DIFF。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/077-doc-sdd-integration/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器、镜像、集群、注册表或特殊硬件依赖；全部工作为本地文件、本地 git、本地 pytest。

- Python（系统解释器）: **available** — probe: `python3 --version` → `Python 3.14.6` @ 2026-10-30；affected: T004/T005/T007/T014/T015（两个引擎扩展）与四个确定性门（只要求 ≥3.8 与标准库）。
- pytest: **partial** — probe: `.venv/bin/python -m pytest --version` → `No module named pytest`（仓库自带 venv 是 Python 3.14.6 但未装 pytest）；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest --version` → `pytest 9.1.1` @ 2026-10-30。affected: 全部测试行（T002、T003、T009、T013、T016，以及 T012 的名册修订复核）。处置：测试一律经 profiles venv 的 `python -m pytest` 运行，与 plan 期定向基线同解释器。
- Git: **available** — probe: `git --version` → `git 2.54.0 (Apple Git-157)` @ 2026-10-30；affected: T009（对基线提交 `c1cd4600` 取剥离后的逐字比对基准）、T025（对基线取 owner 文档的 diff）。
- 分发工具链: **partial** — probe: `python3 scripts/python/sync-mirrors.py --check` → `ModuleNotFoundError: No module named 'httpx'`（系统解释器缺依赖，六对校验未完整执行）；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --check` → 六对全 `ok`、退出码 0，`.../regen-command-copies.py --check` → `OK`、退出码 0 @ 2026-10-30。affected: T022、T023。处置：分发命令一律经 profiles venv；系统解释器的 `ModuleNotFoundError` 不得读作漂移，也不得据此判定镜像失败。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 `[P]` 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US4]`；故事相位每行必有且仅有一个，Setup / Polish 行禁止出现。
- **[blockedBy: T004,T006]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **[green: <contract>#<clause>]**: 本行是把该条款转绿的那一行；标签面定义归 `.specify/templates/tasks-template.md` § Format，机器校验归 `scripts/python/validate-tasks.py`，合同路径相对本文件目录解析。认领分区见 § Clause Partition，同一行内多条款按序递增书写。
- 每行给出具体文件路径与可执行验收；测试行写明它写入的证据槽，实现行写明它让哪一组断言转绿。

## Measured Premises（2026-10-30 生成时实测，HEAD `06c31b1d`，分支 `077-doc-sdd-integration`）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/077-doc-sdd-integration/requirements.md` | `25` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/077-doc-sdd-integration/requirements.md` | `8` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/077-doc-sdd-integration/requirements.md` | `4` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/077-doc-sdd-integration/requirements.md` | `6` |
| 契约文件数 | `ls .specify/specs/077-doc-sdd-integration/contracts/*.md \| wc -l` | `6` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/077-doc-sdd-integration/contracts/*.md \| grep -c '^  C-'` | `77`（13 + 12 + 13 + 19 + 11 + 9） |
| 条款计数陷阱形 | `grep -oh 'C-[0-9]\{2,3\}' .specify/specs/077-doc-sdd-integration/contracts/*.md \| wc -l` | `85` — 这是条款 id 的*提及*数（条款内互引），不是定义数；单位是条款*定义*时正确答案是 `77`。两数并记，表明测量是有意取的而非碰巧 |
| 命令模板数 / 技能数 | `ls templates/commands/*.md \| wc -l`；`ls skills/external/*/SKILL.md skills/internal/*/SKILL.md \| wc -l` | `27` / `52`（069a 闭合集守卫的分母断言值） |
| 七模板三类 token 命中数 | `for f in requirements clarify plan tasks checklist analyze implement; do grep -c -E 'flow_class\|flow-class\|expression' templates/commands/$f.md; done` | 七个各 `0`；正控 `docs.md` = `3`、`humanize.md` = `2` |
| `spec:` 键现状 | `python3 scripts/python/flow-class-check.py --action lookup --unit-id "spec:077-doc-sdd-integration"` | stderr `invalid unit id …: expected /speckit.<stem> or skill:<dir>` + `flow_class: execution` / `source: default` / `marker: null`，退出码 **2** |
| `--action structure` 现状 | `python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/077-doc-sdd-integration` | `argument --action: invalid choice: 'structure' (choose from 'verify')`，退出码 **2** |
| 台账现状 | `python3 scripts/python/flow-class-check.py --action check` | `79 unit(s) scanned, 0 finding(s)`；`ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39`，退出码 0 |
| 分发基线 | `/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --check`；`… regen-command-copies.py --check` | 六对全 `ok`（templates 22 / skills-external 406 / skills-internal 136 / agents 3 / scripts 117 / shared 60），退出码 0；`OK: all per-tool command copies match the source templates.`，退出码 0 |
| 定向测试基线 | `tail -1 .specify/specs/077-doc-sdd-integration/test-evidence/plan-targeted-tests-baseline.txt` | `1015 passed in 27.64s`（14 个既有测试文件，退出码 0） |
| 基线提交的七模板 SHA-256 | `for f in requirements clarify plan tasks checklist analyze implement; do git show "c1cd4600:templates/commands/$f.md" \| shasum -a 256; done` | requirements `31d0e1b43079a35f87c35029053ecee8557b75a282a5949079e2f90c6701a82b` / clarify `baf687495d7f5bee1befbb61941aa348085148fe047c15360222e0ecab95cb92` / plan `1833be4a713f7b9cc80f6953303428469e095f9f3efb9472dff225ec835f485c` / tasks `205fa17fe0050ad1002f344783bb4239a5c70ef12144745e6883b45997d0c93d` / checklist `54ca213e7c102af6eb8c173854863c1d19de34364001df31825fb7ccea387d8e` / analyze `31dc261d9bf76243e4a50af62909dbb0c07fd7aa555ebf6acc0970c2eff8151b` / implement `86974490811efa04008f955a44b60e2e739a36ea2bd83b6fe90e1af4c4d2eda9`（T009 把这七个值钉进测试常量） |
| 七模板与基线是否同字节 | `for f in …; do git hash-object templates/commands/$f.md; git rev-parse c1cd4600:templates/commands/$f.md; done` | 七个 `SAME`（clarity/plan/tasks/checklist/analyze/implement 与 requirements 的 blob 均相等）——接线前它们与基线逐字相同，剥离判据有可复算的起点 |
| 五个新测试文件不在树 | `ls tests/unit/test_flow_class_spec_key.py tests/contract/test_flow_class_spec_declaration.py tests/contract/test_stage_class_wiring.py tests/contract/test_document_structure_gate.py tests/contract/test_docs_gate_driver.py` | 五行 `No such file or directory`（T002 / T003 / T009 / T013 / T016 创建） |
| `notes/` 证据槽不在树 | `ls -d .specify/specs/077-doc-sdd-integration/notes` | `No such file or directory`（T001 创建；同目录已有 `test-evidence/`） |
| 任务行预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/077-doc-sdd-integration/tasks.md` | `28`（T001–T028；T028 是 analyze 修复轮为 FR-013 产出侧新增的那一行，不认领条款）≤ 40 上限（`decomposition-check.py` 的 `TASK_CEILING = 40`） |
| 任务行预算陷阱形 | `grep -oE 'T[0-9]{3}' .specify/specs/077-doc-sdd-integration/tasks.md \| wc -l` | 远大于 28——这是任务标识的*提及*数（`[blockedBy:]`、覆盖表、认领表都在引用），不是定义数；单位是任务*行*时用行首锚定 `^- \[ \] T` 取数 |

## Clause Partition

77 条条款、6 份契约文件，每条款恰被一行认领，同文件内条款序随行序递增。认领的引擎是 `account-clause-coverage.py`（claimed 计数必须等于 77），本表只是声明。

| Contract file | Clauses | Claimed by | 行内条款带 |
|---|---|---|---|
| `contracts/class-declaration.md` | C-001…C-013 | T005 | C-001、C-002 |
| `contracts/class-declaration.md` | — | T006 | C-003 |
| `contracts/class-declaration.md` | — | T007 | C-004…C-010 |
| `contracts/class-declaration.md` | — | T010 | C-011、C-012、C-013 |
| `contracts/class-resolution.md` | C-001…C-012 | T004 | C-001…C-004 |
| `contracts/class-resolution.md` | — | T007 | C-005…C-009 |
| `contracts/class-resolution.md` | — | T008 | C-010 |
| `contracts/class-resolution.md` | — | T010 | C-011、C-012 |
| `contracts/stage-wiring.md` | C-001…C-013 | T010 | C-001…C-011 |
| `contracts/stage-wiring.md` | — | T011 | C-012 |
| `contracts/stage-wiring.md` | — | T012 | C-013 |
| `contracts/document-structure.md` | C-001…C-019 | T014 | C-001…C-010 |
| `contracts/document-structure.md` | — | T015 | C-011…C-016 |
| `contracts/document-structure.md` | — | T018 | C-017…C-019 |
| `contracts/driver-integration.md` | C-001…C-011 | T017 | C-001…C-005 |
| `contracts/driver-integration.md` | — | T019 | C-006…C-008 |
| `contracts/driver-integration.md` | — | T020 | C-009、C-010 |
| `contracts/driver-integration.md` | — | T024 | C-011 |
| `contracts/invariants-and-distribution.md` | C-001…C-009 | T021 | C-001…C-003 |
| `contracts/invariants-and-distribution.md` | — | T022 | C-004、C-005 |
| `contracts/invariants-and-distribution.md` | — | T023 | C-006 |
| `contracts/invariants-and-distribution.md` | — | T024 | C-007、C-008 |
| `contracts/invariants-and-distribution.md` | — | T025 | C-009 |

**Partition check**: 13 + 12 + 13 + 19 + 11 + 9 = 77；19 个认领行，无条款落在两行，无行认领其相位之后才能转绿的条款带。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T005, T007 | FR-014 | T014, T015 |
| FR-002 | T007, T008 | FR-015 | T015 |
| FR-003 | T004, T007 | FR-016 | T015 |
| FR-004 | T005, T007 | FR-017 | T018 |
| FR-005 | T007 | FR-018 | T017 |
| FR-006 | T010, T017 | FR-019 | T017 |
| FR-007 | T004, T010 | FR-020 | T019 |
| FR-008 | T009, T010 | FR-021 | T020 |
| FR-009 | T004, T010 | FR-022 | T021 |
| FR-010 | T010, T011 | FR-023 | T011, T021 |
| FR-011 | T009, T010 | FR-024 | T022, T023 |
| FR-012 | T009, T010 | FR-025 | T024 |
| FR-013 | T014, T028 | — | — |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T003, T004, T007 |
| SC-002 | T009, T023 |
| SC-003 | T010, T018 |
| SC-004 | T014, T015 |
| SC-005 | T017, T019 |
| SC-006 | T021 |
| SC-007 | T022, T023 |
| SC-008 | T020, T024 |

**流程行与执行/取证行**: T001（证据槽）与 T027（收尾门禁留档）为流程行，不承接任何 FR 或 SC——不是漏映射；T026 为实跑取证行——不认领 FR，但产出 `notes/quickstart-run.md` 的七场景快照，服务 SC-002 / SC-004 / SC-007 的复现。其余 25 行各至少映射一条需求（FR 或 SC）——T028 是 FR-013 产出侧的那一行，它不认领任何契约条款（77 条款的认领行仍是 19 行，见 § Clause Partition）。

## Mirror Obligations

镜像对清单的属主是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对）；范围登记见 `plan.md` § Mirror Obligations，本文件不复述其行内容。落地形态：源编辑分散在 T006（requirements 模板）、T028（plan 模板结构骨架）、T011（两份 owner）、T010 / T004 / T007 / T008（七模板与引擎）、T014 / T015（结构动作）、T017 / T018 / T019 / T020（驱动三文件）；**T022 是唯一的同步与验证行**（`--write` 后 `--check`，逐对陈述无新增漂移），T023 负责「未刷新 / 已刷新」两态证据。`templates/commands/**` 不在 templates 镜像对内，只经 `regen-command-copies.py` 产出 per-tool 副本——**套数以该脚本实际产出的目标目录为准**（注册表最多六个，本仓当前四个），本文件不写死套数；`tests/**` 与 `.specify/specs/077-doc-sdd-integration/**` 无任何镜像义务。

## Test Budget

- **本阶段（tasks）不运行任何测试套件**（docs-only 预算）：四个确定性门（`validate-tasks` / `decomposition-check` / `pre-analyze-check` / `account-clause-coverage`）的输出留档 `test-evidence/tasks-*.txt`，全部测试断言留待实现阶段。
- **实现期基线（恰好一次）**: 实现开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获失败名基线；本文件任何行不得重捕获或刷新（重捕获会把回归网变成移动靶）。
- **闭环节点**: review 之后由驱动者跑一次全量并按名比较；本特性任何行不得预支。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建好证据槽，后续每个红先行行与守卫行都有固定落点

- [ ] T001 建立本特性证据槽并冻结实测前提：新建 `.specify/specs/077-doc-sdd-integration/notes/red-first-evidence.md`（头部点名 `tests/unit/test_flow_class_spec_key.py`、`tests/contract/test_flow_class_spec_declaration.py`、`tests/contract/test_stage_class_wiring.py`、`tests/contract/test_document_structure_gate.py`、`tests/contract/test_docs_gate_driver.py` 五个文件，并规定每组红先行记录四个字段——重放命令 / 真实输出 / 退出码 / 失败计数）、`notes/pre-change-measurements.md`（逐条粘贴本文件 § Measured Premises 的实测值与命令，带日期 2026-10-30）、`notes/quickstart-run.md`（头部列 S1–S7 七个场景及各自判据，真实输出留实现期粘贴）

**Checkpoint**: 证据槽就位；本相位无阻断全部故事的前置，故无 Foundational 相位。

---

## Phase 2: User Story 1 - 一条特性线声明自己的类别，任何阶段都能在判定前读到它 (Priority: P1) 🎯 MVP

**Goal**: 让类别有一个**只由作者判定、只在规格头部出现一次、由既有唯一引擎解析**的载体，并把「已声明 / 未声明 / 取值越界 / 形态错误」四种结果做成只读退出码与记录字段即可判定的形态。

**Independent Test**: 三个夹具规格（声明 `expression`、不写该字段、写一个非法值）各跑一次 `--action lookup --unit-id "spec:<name>"`，只读退出码与记录字段即可判定（依次为已声明 / 未声明带默认标记 / 阻断错误），且 `feature:077` 与裸目录名仍退出 2。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写测试，确认它们失败，再实现**

- [ ] T002 [US1] 红先行编写 `tests/unit/test_flow_class_spec_key.py`：键文法 `^spec:[a-z0-9][a-z0-9-]*$`（裸目录名、`feature:077`、含 `/` 的路径形一律退出码 2 且不返回类别）、解析位置（`<repo>/.specify/specs/<name>/requirements.md`；`--repo` 指向 `.specify` 自身时退化为 `<repo>/specs/<name>`；spec 目录不存在 → 退出码 2）、记录与单元键逐字段同形（九字段，含 `error`；`unit_id` 取键原文、`source` ∈ {`declaration`, `default`}、`basis` 恒 `null`、`neutral` 恒 `false`）、三段退出码 0/1/2 各自的输入类别、owner 解析先于键族（把 owner 路径指向不存在的位置时任何键都走退出码 2 与同一降级标签）、`spec:` 声明不出现在逐流程台账；夹具在 `tmp_path` 内以字面量构造；在未改动树上跑出记录在案的失败运行（现状 `spec:` 键退出码 2，实测见 `test-evidence/plan-resolution-baseline.txt`），四字段写入 `notes/red-first-evidence.md`
- [ ] T003 [US1] 红先行编写 `tests/contract/test_flow_class_spec_declaration.py`：声明行逐字文法（`**Flow Class**:` + 半角冒号 + 一个空格 + 取值，行尾无尾随空白，字段名与取值大小写敏感）、位置在 `## Related Feature` 之前、四码各一例（`invalid-class`；`declaration-malformed` 的全角冒号 / 字段名大小写变体 / 尾随空白 / 行内附加注释四形各一次；`declaration-duplicate` 不论两次取值是否相同；`declaration-misplaced`）全部归退出码 1 且 stderr 具名文件、行号与取值、`templates/requirements-template.md` 的字段行位置（`**Status**:` 之后、`**Input**:` 之前）与占位形态（不得预填类别、不得携带判据句）、单一真源（`.specify/memory/features.md` 无类别列、`.specify/memory/features/077.md` 不存取值）；跑出记录在案的失败运行并四字段留档

### Implementation for User Story 1

- [ ] T004 [US1] [blockedBy: T002] 扩展 `scripts/python/flow-class-check.py` 的 `--action lookup` 键族：新增 `spec:<spec 目录名>` 解析（basename 文法、spec 目录不存在 → 退出码 2）、同形九字段记录与 `source`/`basis`/`neutral`/`error` 取值、`--repo` 两顶帽子下的解析位置；特性线声明不进逐流程台账；只用标准库、只读、不新增第二个解析函数或脚本入口；`tests/unit/test_flow_class_spec_key.py` 的键族与记录组转绿 [green: contracts/class-resolution.md#C-001] [green: contracts/class-resolution.md#C-002] [green: contracts/class-resolution.md#C-003] [green: contracts/class-resolution.md#C-004]
- [ ] T005 [US1] [blockedBy: T004] 在 `scripts/python/flow-class-check.py` 内解析声明行：只在 `## Related Feature` 之前的头部区取行、按逐字文法与封闭二值判定；合法声明返回 `source: declaration` 与声明值；全文无该字段返回 `execution` + `source: default` + 069 登记的默认标记；类别只由作者写在字段里，脚本 MUST NOT 从路径、文件名、扩展名、内容或提交信息推断；**存量线**无该字段时另可附 advisory 码 `declaration-absent`（`error.label`，退出码 0、不计缺陷、不进判定集合），且必须与 `owner-unavailable` 降级互斥 [green: contracts/class-declaration.md#C-001] [green: contracts/class-declaration.md#C-002]
- [ ] T006 [US1] [blockedBy: T003] 在 `templates/requirements-template.md` 的 `**Status**:` 行之后、`**Input**:` 行之前插入一行 `**Flow Class**: `（占位形态，由作者替换；MUST NOT 预填某个类别），并加一行注释说明取值只由作者判定、索引与详情不复制该值；模板 MUST NOT 携带判据句、取值定义或「如何判定」说明；`.specify/templates/requirements-template.md` 由 `sync-mirrors.py` 产出，不手改 [green: contracts/class-declaration.md#C-003]
- [ ] T007 [US1] [blockedBy: T005,T006] 在 `scripts/python/flow-class-check.py` 内实现声明形态发现与阻断：`declaration-duplicate`（全文第二行，判定只读行数、不读两次取值是否一致）、`declaration-misplaced`（唯一一行位于 `## Related Feature` 之后）、`declaration-malformed`（字段在场而形态不合规范，MUST NOT 落成「无该行」）、`invalid-class`（取值越界）；四码全部归退出码 1 且与退出码 2 不合并，stderr 形如 `<code>: <repo 相对路径>:<行号> carries '<值或形态摘要>', <判据一句话>`；退出码 1 的记录写 `flow_class: null` + `source: declaration`（MUST NOT 写 `execution` + `default`）；`source: declaration` 与默认标记互斥、`flow_class: null` 与 `source: default` 互斥；`declaration-absent` 只在 owner 与引擎都可用时产生（与 `owner-unavailable` 互斥）；owner 解析先于键文法是**本特性的登记变更**（FR-011 豁免①），实现时 MUST NOT 悄悄改回旧顺序；同时给 `tests/contract/test_flow_class_spec_declaration.py` 追加单一真源测试腿（索引无类别列、详情不存取值），并让该声明面板全绿、键族测试里的声明组断言一并转绿（see `tests/unit/test_flow_class_spec_key.py`） [green: contracts/class-declaration.md#C-004] [green: contracts/class-declaration.md#C-005] [green: contracts/class-declaration.md#C-006] [green: contracts/class-declaration.md#C-007] [green: contracts/class-declaration.md#C-008] [green: contracts/class-declaration.md#C-009] [green: contracts/class-declaration.md#C-010] [green: contracts/class-resolution.md#C-005] [green: contracts/class-resolution.md#C-006] [green: contracts/class-resolution.md#C-007] [green: contracts/class-resolution.md#C-008] [green: contracts/class-resolution.md#C-009]
- [ ] T008 [US1] [blockedBy: T007] 单一真源与台账边界收口：在 `.specify/memory/features/077.md` 只加一条指向声明行的指针（不复制取值），复核 `.specify/memory/features.md` 无类别列；跑 `python3 scripts/python/flow-class-check.py --action check` 断言台账仍 `ledger_rows=79 matched=79 inventory_units=79 gaps=0`（`spec:` 键不进台账，写入即产生 `unknown` 发现）；把命令、真实输出与退出码写入 `test-evidence/tasks-ledger-boundary.txt` [green: contracts/class-resolution.md#C-010]

**Checkpoint**: US1 独立可验——三个夹具规格各跑一次解析即得三种不同结论（表达式 / 未声明带标记 / 阻断），`feature:077` 与裸目录名仍退出 2，台账行集未变。

---

## Phase 3: User Story 2 - 表达类走完整八阶段但门禁换成语义上能证伪文档的算子；执行类一点没变 (Priority: P1)

**Goal**: 把「类别可查」变成「类别被七个阶段命令真正读取」，并把执行类的零行为变化做成可复算的字节判据。

**Independent Test**: 两条仅类别不同的夹具线跑同一模板，输出差异完全由声明解释；七个模板剥离接线子节后与基线提交 `c1cd4600` 逐字相同；模板全文 grep 不出现任何特性号或路径白名单。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T009 [US2] 红先行编写 `tests/contract/test_stage_class_wiring.py`：七个模板各恰一个接线子节（标题逐字取 `research.md` R-9 登记的唯一字面量）、子节内恰一次 `flow-class-check.py --action lookup --unit-id "spec:<spec 目录名>"`、两条 owner 指针（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`）、两分支句、降级可见句与**退出码 1 的停止句**（作者输入错误时本阶段停下并以阶段协议异常行形态收尾，MUST NOT 落入「既有门禁集逐字不变」那支）、禁止项（`G-` 算子 id / 六面 face 表 / `flow_class=` 与 `flow_class:` 赋值形 / 按特性号或路径的允许列表）、`clarify` 在内且 `docs.md` / `humanize.md` 不变、per-tool 命令副本携带子节；**execution 零变化反向守卫**：按 R-9 的剥离算法（起点＝标题行，终点＝其后第一个 `^#{1,3} ` 行前一行，不额外增删空行；块末 MUST 恰一个空行，否则判形态违规）删除子节后，七个模板 MUST 与基线提交 `c1cd4600` 的同名文件逐字相同（SHA-256 常量在编写时以 `git show c1cd4600:<path> | shasum -a 256` 实测钉入，值见 § Measured Premises），并**同时断言子节存在**，否则守卫在无接线时空转；跑出记录在案的失败运行并四字段留档

### Implementation for User Story 2

- [ ] T010 [US2] [blockedBy: T009] 在 `templates/commands/requirements.md`、`templates/commands/clarify.md`、`templates/commands/plan.md`、`templates/commands/tasks.md`、`templates/commands/checklist.md`、`templates/commands/analyze.md`、`templates/commands/implement.md` 各插入恰一个子节（标题逐字取 `research.md` R-9 登记的字面量，位于 `## User Input` 之后、下一个 `## ` 之前，独占一个块且块末恰一个空行以支持剥离）：一次 lookup + 两条 owner 指针 + 两分支句（表达类按阶段算子表执行本阶段登记的行；其余既有门禁集逐字不变）+ 降级可见句（`owner-unavailable` 时显示标签并保持既有门禁集，不中断、不转绿、不切换门禁集）+ **退出码 1 停止句**（作者输入错误时本阶段停下、以阶段协议异常行形态收尾并点名文件行号，MUST NOT 按「既有门禁集逐字不变」继续）；`requirements` 子节另写读取时点（声明行写入之后、`validate-requirements.py` 之前）与 re-baseline 句（门禁通过后改行须记 re-baseline 并重跑 requirements 门禁集，不得静默翻转）；六个非 requirements 阶段的读取点为阶段入口；子节内禁止 `G-` 算子 id、face id 表、类别赋值形与任何白名单，分支句用「表达类 / 执行类」语义词；委派技能不再读一次；只改框架源，`.specify/` 与 per-tool 命令副本不手改（副本由 `regen-command-copies.py` 产出，套数以它实际产出的目标目录为准） [green: contracts/stage-wiring.md#C-001] [green: contracts/stage-wiring.md#C-002] [green: contracts/stage-wiring.md#C-003] [green: contracts/stage-wiring.md#C-004] [green: contracts/stage-wiring.md#C-005] [green: contracts/stage-wiring.md#C-006] [green: contracts/stage-wiring.md#C-007] [green: contracts/stage-wiring.md#C-008] [green: contracts/stage-wiring.md#C-009] [green: contracts/stage-wiring.md#C-010] [green: contracts/stage-wiring.md#C-011] [green: contracts/class-declaration.md#C-011] [green: contracts/class-declaration.md#C-012] [green: contracts/class-declaration.md#C-013] [green: contracts/class-resolution.md#C-011] [green: contracts/class-resolution.md#C-012]
- [ ] T011 [US2] [blockedBy: T010] 两份 owner 的类条件追加（只增不改）：`shared/definitions/flow-class-definitions.md` 增特性线声明面与 `spec:` 键的消费方指针；`shared/workflow/expression-gates.md` 增特性线调用点行（六面封闭集与阶段算子表一行不动）；两份文件的既有条款零改写、零删除；`.specify/shared/` 同名副本由 `sync-mirrors.py` 产出，不手改 [green: contracts/stage-wiring.md#C-012]
- [ ] T012 [US2] [blockedBy: T010] 修订既有闭合集守卫 `tests/contract/test_expression_gate_wiring.py`：把七个阶段模板并入已接线名册（`test_a6_wiring_set_is_closed` 的跳过集合），`test_a6_wiring_inventory_matches_the_frozen_denominator` 的分母断言保持不变（27 模板 / 52 技能）；MUST NOT 删除该断言，MUST NOT 把它放宽成「任一面板可接线」 [green: contracts/stage-wiring.md#C-013]

**Checkpoint**: US2 独立可验——七个模板各出现一次 lookup 且剥离后与基线逐字相同；两条仅类别不同的夹具线输出差异完全由声明解释；执行类零新增阻断检查、零新增必填章节。

---

## Phase 4: User Story 3 - 表达类的 plan 产出可核对的文档结构，implement 按结构落文并过四面门禁 (Priority: P1)

**Goal**: 把「文档像代码一样严密」落成能红能绿的判定：plan 的四项结构由既有检查器的新动作校验，implement 的落文与计划两向比对。

**Independent Test**: 一个合规 plan 夹具通过；四个负向夹具（缺章节树、缺基准读者行、证据条目缺 source、同一事实两个 owner）各自转红；两个落文夹具各转红（计划外顶层章节 → `chapter-unexpected`；结构/链接/构建零新增违规而证据面缺 `source` → 该次门禁仍 fail，「结构绿而内容红」）；执行类/未声明主体输出 `not-applicable` 而不是「0 违规通过」。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T013 [US3] 红先行编写 `tests/contract/test_document_structure_gate.py`（**一次写全两组腿**，后续两行只让各自的一部分转绿）：`--action structure` 的 CLI 契约（`--spec-dir` 指定判定对象；缺省只做 plan 侧并标 `two-way: not-run`；**两向比对复用既有 `--path`** 作落文输入，不新增参数）、`--faces` 四面取值集与 `parse_faces` 不变（不新增第七面）、表达类 → 四子节与**四族**码检查（含 `document-structure-missing` 与 `subsection-missing` 两个缺节码）、执行类或未声明 → `status: not-applicable` 且打印 `class=` / `source=` 与非空伴生量（被检查文件数，MUST NOT 呈现为「0 违规通过」）、列名常量由检查器持有且测试从常量读取（不手抄）、章节树四语法码、两向比对的 `chapter-missing` / `chapter-unexpected`、证据面的 `evidence-unlisted` 与四个既有证据码复用、owner 面三码与既有 `duplicate` 机械下限、基线子集判据与 `--freeze` 只打印不写文件、**四个负向夹具各自转红**（缺章节树 / 缺基准读者行 / 证据条目缺 `source` / 同一事实两个 owner）、同一份 `plan.md` 重跑得同一违规集且 finding 顺序稳定；夹具在 `tmp_path` 内以字面量构造；跑出记录在案的失败运行（现状 `--action structure` 退出码 2）并四字段留档

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T013] 扩展 `scripts/python/doc-consistency-check.py` 的新动作 `--action structure`（`--action` 取值从 `("verify",)` 扩为 `("verify","structure")`，`--faces` 与四面解析路径一律不动）：主体是 `--spec-dir` 下的 `plan.md`（plan 侧），类别经 `scripts/python/flow-class-check.py --action lookup --unit-id "spec:<dir>"` 的同一条解析入口取得（不新建第二解析函数）；解析四子节（`## Document Structure` 与四个三级标题）、三张表的列名以常量声明并按列名匹配（不猜列位）、结构语法族码 `document-structure-missing` / `subsection-missing`（`name=` 取缺失子节的登记字面量，取值域为四个）/ `parent-unknown` / `chapter-duplicate` / `chapter-purpose-missing` / `chapter-boundary-missing`；**落文输入复用既有 `--path`**（不新增参数）：不给 `--path` 时只出 plan 侧结论并标 `two-way: not-run`，给了才做两向比对；表达类有 finding 或 `status: fail` → 退出码 1，输入错误 → 2，合格 → 0；重跑同一份 `plan.md` 得同一违规集；结构门禁测试的四子节与语法码组转绿（测试文件见 T013） [green: contracts/document-structure.md#C-001] [green: contracts/document-structure.md#C-002] [green: contracts/document-structure.md#C-003] [green: contracts/document-structure.md#C-004] [green: contracts/document-structure.md#C-005] [green: contracts/document-structure.md#C-006] [green: contracts/document-structure.md#C-007] [green: contracts/document-structure.md#C-008] [green: contracts/document-structure.md#C-009] [green: contracts/document-structure.md#C-010]
- [ ] T015 [US3] [blockedBy: T014] 在 `scripts/python/doc-consistency-check.py` 内补齐结构与逻辑的两向比对与两族码（两向比对只在给了 `--path` 时执行，未给则输出 `two-way: not-run` 且不计入任何 `passed` 面）：章节两向比对只产出 `chapter-missing`（落文缺计划中的节）与 `chapter-unexpected`（落文出现计划外**顶层**章节；非顶层不因本条转红）两个具名码、判定只读章节标题与计划表；证据面 `evidence-unlisted` 与复用既有 `grade-invalid` / `as-of-malformed` / `source-missing` / `grade-asof-unpaired`（不自造同义码）；owner 面 `owner-duplicate` / `owner-path-missing` / `owner-anchor-missing`；正文重复手写沿用既有 `duplicate` 面的机械下限（归一化后全等且长度 ≥ 24 字符，或相似度 ≥ 0.90 且长度 ≥ 40 字符），MUST NOT 自建第二套阈值；基线落在 `<spec-dir>/structure-baseline.txt`，判据是「当前违规集 ⊆ 基线集」按 `文件 + 违规码 + 节名` 三元组比对，基线缺失读作空集（绝对判定）而非豁免，`--freeze` 只打印、脚本自身不写文件；结构门禁测试的余下断言组全绿（测试文件见 T013） [green: contracts/document-structure.md#C-011] [green: contracts/document-structure.md#C-012] [green: contracts/document-structure.md#C-013] [green: contracts/document-structure.md#C-014] [green: contracts/document-structure.md#C-015] [green: contracts/document-structure.md#C-016]

**Checkpoint**: US3 独立可验——一个合规 plan 夹具退出 0，四个负向夹具各命中一个具名码，两个落文夹具各转红，执行类主体输出 `not-applicable` 且不呈现为通过。

---

## Phase 5: User Story 4 - sdd-loop-driver 能无人值守驱动表达类特性，而不是按代码型默认放行 (Priority: P2)

**Goal**: 让驱动把「这条线是哪一类」写进每次派发的提示词，并在 U4 把门禁证据列为放行前置；两槽位测试预算在表达类下装两次文档门禁，时点与审计不变。

**Independent Test**: 一条表达类线的 implement 记录具备哨兵与产物但缺门禁证据，U4 判未完成；状态脊里两个文档门禁槽位各出现一次且时点正确，缺一个时既有审计报违规而不是静默通过。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T016 [US4] 红先行编写 `tests/contract/test_docs_gate_driver.py`：派发载荷**四元组**（`flow_class=` / `source=` / `marker=` / `error=`）在第①段、本地原生与远端 CLI 同规、缺任一键即派发构造缺陷且 U4 不放行、子代理不得推断或补默认；U4 四项 blocking（(a) 算子表登记的 blocking 行各有结果记录且无 `not-evaluated`——计数分母只取算子表，implement 为 1 行；(b) 证据文件存在且非空，**不做哈希比对**；(c) 载荷类别与当场解析值一致，且 `error` 位非 `-` 时走 `owner-unavailable` 分支；(d) `stage-status` 行在场）；两槽位内容（`selection_basis=docs-gate-full`、`command` 记文档门禁命令串、`rc` 为逐命令非零优先的聚合值、`passed` 只数 `pass`、`not-applicable` 单列并由「总数 − (passed+failed) = not-applicable 条数」约束、closure 的 `baseline_compare` 为算子 id 名称级差集、`evidence_ptr` 承载逐面原因、未运行不写槽位行不记 0）；阶段序列、哨兵字面量、watcher 判定、快车道判据与 analyze/review 调用率不变；跑出记录在案的失败运行（驱动技能与 references 对类别零命中）并四字段留档

### Implementation for User Story 4

- [ ] T017 [US4] [blockedBy: T016] 改写 `skills/external/sdd-loop-driver/references/stage-prompts.md`：第①段增类别**四元组**（`flow_class=<值>`、`source=<declaration|default>`、`marker=<默认标记或空>`、`error=<E3 码或 ->`，本地与远端同规，提示词是唯一载体；`error` 位用于把「机制降级」与「作者未声明」分开）；取值唯一来源是该线 `requirements.md` 的声明行，经同一解析入口在**每次阶段派发前**解析一次，状态脊中的类别行只作带日期的观测、重入时重新解析并与观测比对（不一致记 re-baseline）；`## Independent Verification（独立校验程序，U4）` 增补四项全部 blocking 的校验（(a) 本阶段**在算子表中登记的 blocking 行**各有一条结果记录且无 `not-evaluated`（计数分母只取算子表：implement 为 1 行 `G-implement-structure`，四个 CLI 面不各自算算子）；(b) 证据文件存在且非空——**不做哈希比对、不新增记账字段**（既有哈希绑定只约束 `verification.md` 的 SC 样本行，且其 owner 明写非 `pass` 不承担绑定义务），verdict 只由 (a) 读记录；(c) 载荷类别与 U4 当场解析值一致，且 `error` 位非 `-` 时走 `owner-unavailable` 分支（记降级观测、保持既有门禁集、不按表达类四项校验、也不当作「作者未声明」放行）；(d) 本阶段 `stage-status` 行在场），哨兵与产物具备而门禁证据缺失判未完成、不派发下一阶段 [green: contracts/driver-integration.md#C-001] [green: contracts/driver-integration.md#C-002] [green: contracts/driver-integration.md#C-003] [green: contracts/driver-integration.md#C-004] [green: contracts/driver-integration.md#C-005]
- [ ] T018 [US4] [blockedBy: T015,T017] 在 `skills/external/sdd-loop-driver/references/stage-prompts.md` 的 implement 段与 U4 段写清 implement 侧证据面：表达类 implement 按章节树落文并通过以下 blocking 判定：① 门禁输出的四面 `reader` / `evidence` / `duplicate` / `count`（取值集归 `doc-consistency-check.py` 的 `FACES`，落文文档的读者声明仍按「前 40 个非空行」窗口判）；② 结构子步（章节树语法 + 两向比对，复用 `--path` 作落文输入）；③ 站点层存在时的构建算子；任一面/子步 `not-evaluated` 不计为通过——并写明「四面指 CLI 输出面、不是算子表的四行，U4(a) 的计数分母取算子表」这一读法；四面结果与结构子步落在同一份门禁输出文件（`<spec-dir>/test-evidence/`）并作为该阶段 SC 证据的唯一来源——`verification.md` 的 `SC-NNN_value=` 记逐面 `面=verdict` 摘要、证据记录沿用既有四键（`sample_id` / `evidence_path` / `evidence_sha256` / `verdict`），某面 `not-evaluated` → 该 SC 记 `unknown` 并点名面与原因、MUST NOT 记 `pass`；结构面通过不得被援引为内容正确性证据（只是必要条件），implement 的 Test-First MAY 按宪法 VII 的 template-only 条款判 `Partial (justified)` 且 justification 写明替代验证是四项文档门禁输出 [green: contracts/document-structure.md#C-017] [green: contracts/document-structure.md#C-018] [green: contracts/document-structure.md#C-019]
- [ ] T019 [US4] [blockedBy: T016] 改写 `skills/external/sdd-loop-driver/references/efficiency-model.md` §2 的槽位内容分支（时点、槽位数、槽位顺序、closure 名称级差集与审计判定一律不动）：表达类两槽位换为两个文档门禁槽位——`selection_basis=docs-gate-full`，`command` 记该次文档门禁命令串（一次四面调用 `--action verify --faces reader,evidence,duplicate,count` + 结构子步 `--action structure --spec-dir … --path …`，站点层存在时加构建算子），`rc` 记该串的**聚合退出码**（逐命令非零优先，逐命令原始 rc 落 `evidence_ptr` 指向的输出），`passed` 只记 verdict = `pass` 的 blocking 算子数，`failed` 记 verdict ∈ {`fail`, `not-evaluated`} 的算子数，**`not-applicable` 单列**（不计 `passed`、不计 `failed`，条数由「算子总数 − (passed+failed)」等式约束、逐面原因写进 `evidence_ptr`），closure 的 `baseline_compare` 是算子 id 集合的名称级差集、`failed_names_path` 指失败算子 id 名单、逐面 `not-evaluated` 原因写进 `evidence_ptr` 指向的门禁输出（不并入 `passed`、不以 0 表示未运行）；槽位不得静默跳过、未运行不得写槽位行；非槽位阶段的定向集记录义务不因类别免除（仅文档改动亦须留 `stage-status` 行）；`audit-test-budget.py` 不改 [green: contracts/driver-integration.md#C-006] [green: contracts/driver-integration.md#C-007] [green: contracts/driver-integration.md#C-008]
- [ ] T020 [US4] [blockedBy: T019] 在 `skills/external/sdd-loop-driver/SKILL.md` 写类别感知落点：`## Hard Requirements` 增一条类别分支（派发载荷必须携带类别**四元组**（含 `error` 位），缺失即派发构造缺陷；U4 对表达类校验门禁证据，`error` 位非 `-` 时走 `owner-unavailable` 分支），并加一条指向 `references/stage-prompts.md` 与 `references/efficiency-model.md` 的指针；同时声明驱动 MUST NOT 因类别改变阶段序列、哨兵字面量、watcher 判定与退出码、卡死处置、快车道判据或 analyze / review 调用率——类别只改变两件事：用哪套算子证明同一不变量、预算槽位里装什么；analyze 与 review 的调用率保持 100%，任何以「本线属表达类」为由跳过或缩短阶段的请求被拒；`.specify/skills/sdd-loop-driver/` 同名副本由 `sync-mirrors.py` 产出，不手改 [green: contracts/driver-integration.md#C-009] [green: contracts/driver-integration.md#C-010]

**Checkpoint**: US4 独立可验——缺门禁证据的 implement 记录被 U4 判未完成；两个文档门禁槽位在状态脊围栏中各一次且时点正确；阶段序列与 analyze/review 调用率不变。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 零新增机制的前后集合差、分发两态等价、069 不变量复核与实跑留档

- [ ] T021 零新增机制的前后集合差：对比基线提交 `c1cd4600` 与当前树的 `/speckit.*` 命令清单（`templates/commands/*.md` 与各工具副本目录的并集）、依赖清单与进程清单，差异必须落在空集；同时复核 `python3 scripts/python/doc-consistency-check.py --faces` 仍为四面、六面 owner 的封闭集不变、`--faces` 的解析器未被扩面；**再跑一次 `python3 skills/external/sdd-loop-driver/scripts/scan-confirmation-gates.py --summary`**，把 `blocking confirmation gates` 计数与改动前的读数逐字对照，两次 MUST 相等（FR-022 的确认门条款；既有 25% 总量守卫对 +1 不转红，所以必须直接读计数）；把两份快照、扫描器两次读数与差异输出写入 `test-evidence/tasks-scope-set-difference.txt` [green: contracts/invariants-and-distribution.md#C-001] [green: contracts/invariants-and-distribution.md#C-002] [green: contracts/invariants-and-distribution.md#C-003]
- [ ] T022 镜像与命令副本收尾（唯一同步与验证行）：经 profiles venv 跑 `/Users/liuqiming.lqm/project/profiles/.venv/bin/python scripts/python/sync-mirrors.py --write` 产出全部 `.specify/` 副本，再跑 `--check` 对六对逐对陈述相对 `test-evidence/plan-sync-mirrors-baseline.txt` 无新增漂移；跑 `… regen-command-copies.py --write` 后 `--check`，对 `regen-command-copies.py` 实际产出的每个 per-tool 副本（套数以脚本实测为准，本仓当前四个）陈述相对 `test-evidence/plan-regen-command-copies-baseline.txt` 无新增漂移；`.specify/` 与副本 MUST NOT 手改，`templates/commands/**` 不进 templates 镜像对；输出写入 `test-evidence/tasks-distribution-after.txt` [green: contracts/invariants-and-distribution.md#C-004] [green: contracts/invariants-and-distribution.md#C-005]
- [ ] T023 分发两态等价取证：以基线提交 `c1cd4600` 的命令副本为「未刷新」一侧、以 T022 产出的副本为「已刷新」一侧，逐模板断言差异只出现在「是否含接线子节」这一点上——未刷新副本的七个模板不出现 `flow-class-check.py` 与两条 owner 指针，已刷新副本各出现一次；两侧计数与差异写进 `test-evidence/tasks-distribution-two-state.txt`（服务 SC-007）[green: contracts/invariants-and-distribution.md#C-006]
- [ ] T024 069 不变量复核与 Feature 集成：复核八阶段集合不变、门禁数量不降、P0/P1 定义不动、analyze 与 review 调用率 100%（读 `shared/workflow/expression-gates.md` § 阶段不变量，不回写）；更新 `.specify/memory/features/077.md` 记录本特性的设计落点、实现期留痕与承接边（承接关系只记在 077 侧，MUST NOT 反向写入 069 详情文件），并复核 `.specify/memory/features.md` 的 077 行状态由实现阶段推进、tasks 阶段不改；069 与 069a/069b 的正文与状态零改动 [green: contracts/invariants-and-distribution.md#C-007] [green: contracts/invariants-and-distribution.md#C-008] [green: contracts/driver-integration.md#C-011]
- [ ] T025 两份 owner 的类条件追加取证：对基线提交 `c1cd4600` 取 `shared/definitions/flow-class-definitions.md` 与 `shared/workflow/expression-gates.md` 的 diff，断言差异行只有新增（既有条款零删除、零改写），且 `flow-class-check.py --action check` 的台账仍为 79 行量级、`gaps=0`（新增 `spec:` 键不进台账）；命令、diff 摘要与计数写入 `test-evidence/tasks-owner-append-delta.txt` [green: contracts/invariants-and-distribution.md#C-009]
- [ ] T026 实跑 `quickstart.md` 的 S1–S7 七个场景（S1 本线解析 / S2 三例判定 / S3 结构门禁 / S4 七模板接线存在性 / S5 分发漂移 / S6 两槽位审计 / S7 清理），把每条命令的真实输出与拆卸步骤贴入 `.specify/specs/077-doc-sdd-integration/notes/quickstart-run.md`；S7 的临时目录与 `.specify/.tmp/` 夹具必须清除，`git status --ignored` 不得把它们当新增；不改写 plan 属主的 `quickstart.md`
- [ ] T027 收尾门禁留档：把 `validate-tasks.py`、`decomposition-check.py --mode tasks`、`pre-analyze-check.py --stage tasks`、`account-clause-coverage.py` 四条命令的真实输出写入 `test-evidence/tasks-*.txt`，并只为本特性产物建立提交（不 push，不夹带既有脏文件）
- [ ] T028 在 `templates/plan-template.md` 增 `## Document Structure` 章节骨架（FR-013 的**产出侧**，即「可达一侧」）：四个三级子节标题逐字取 requirements § Shared Strings 的 [[STR-003]]…[[STR-006]]，三张表带固定表头列（章节树 4 列；基准读者两行 `**Readers**:` / `**Reading scenario**:`；证据清单 4 列；事实 owner 清单 3 列），并写明「表达类 MUST 产出该章节、执行类 MUST NOT 被要求产出」（后者保证执行类零新增必填章节，FR-011）；骨架之外一律以 `[[STR-NNN]]` 引用、不重抄字面量；`.specify/templates/plan-template.md` 由 `sync-mirrors.py` 产出，不手改；验收 = T009 的剥离守卫与 T013 的结构测试在同一树上通过（该文件属 templates 镜像对，不进 per-tool 命令副本面）

**Checkpoint**: 全部分发面零新增漂移；零新增机制；069 不变量未削弱；七场景实跑有据。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **US1 (Phase 2)**: 依赖 Setup 的证据槽；本特性 MVP 的第一块。
- **US2 (Phase 3)**: 依赖 US1 的解析引擎（接线子节调用它）与 requirements 模板字段。
- **US3 (Phase 4)**: 只依赖 US1 的解析入口（结构动作按类别解析），与 US2 的模板接线互不阻塞。
- **US4 (Phase 5)**: 依赖 US3 的结构码集（U4 校验算子结果时引用）与 US2 的接线子节语义。
- **Polish (Phase 6)**: 依赖 US1–US4 全部源改动完成（镜像同步必须最后跑）。

### User Story Dependencies

- **US1 (P1)**: 无跨故事依赖——字段、引擎、单一真源三者自成闭环。
- **US2 (P1)**: 消费 US1 的 `spec:` 键解析；`[blockedBy: T009]` 之外按故事顺序串行。
- **US3 (P1)**: 与 US2 无写集交集（`scripts/python/` vs `templates/commands/`），可并行开工；两者的共同前置只有 US1 的解析入口。
- **US4 (P2)**: 消费 US3 的码集与 US2 的子节语义，排在两者之后。

### Within Each User Story

- 测试先行，且必须先在未改动树上跑出记录在案的失败
- 同一文件的多行按 `[blockedBy:]` 串行；条款认领随行序递增
- 实现行让对应测试组转绿后才进入下一行

### Parallel Opportunities

- **本文件没有 `[P]` 行，这是测量结论而不是省略**：所有测试行都向同一个 `notes/red-first-evidence.md` 追加记录（红先行日志是单写点），实现行要么改同一个文件（引擎四段、结构动作两段、驱动三份 references 依次），要么需要前一行已落盘才能让断言通过（模板的 owner 指针必须解析到已存在的 owner；剥离守卫必须等子节落盘才可复算）。
- 可并行的只有故事层：US2 与 US3 写集不相交（模板 vs 脚本）、相互不消费对方的产物，多 agent 下可同时开工；两者仍串行在证据日志上（每次追加一行），故不体现为 `[P]` 标签。
- US1 与 US4 因 `[blockedBy:]` 无法并行：US4 消费 US1–US3 的引擎与码集。

---

## Parallel Example: Story-level only

```bash
# 双 agent 场景（可选）：证据日志按「一次追加一行」串行，两故事写集不相交
Agent A: "US2 — T009 → T010 → T011 → T012"
Agent B: "US3 — T013 → T014 → T015"

# 单 agent 场景：按 T001 → US1 → US2 → US3 → US4 → Polish 顺序执行
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = US1 + US2 + US3（三个 P1 故事）**。判据是模板的 MVP 规则：只有一个 P1 故事时它即 MVP；当多个 P1 故事**只有合起来**才构成可独立验收的增量时，MVP 覆盖全部 P1。这里正是后者——US1 单独交付的是一个没有消费者读取的标签（半套机制），US2 单独交付的是读一个不存在的声明，US3 单独交付的是一个没有编排入口的结构校验器；三者合起来才第一次让「表达类特性线跑文档门禁」成立。US4 是驱动侧接入，排在其后。

1. 完成 Phase 1：证据槽
2. 完成 US1（T002–T008）→ **STOP and VALIDATE**：三个夹具规格各跑一次解析得三种不同结论，台账行集未变
3. 完成 US2（T009–T012）→ **STOP and VALIDATE**：七模板各一次 lookup，剥离后与基线逐字相同，闭合集守卫复绿
4. 完成 US3（T013–T015）→ **STOP and VALIDATE**：五个结构夹具（1 合规 + 4 负向）与一个 implement 结构夹具各按其判据转绿 / 转红
5. 再推进 US4，最后 Polish

### Incremental Delivery

1. US1 → 规格作者第一次能声明类别并只读退出码判定
2. US2 → 七个阶段命令第一次按类别跑不同算子集，执行类零变化可复算
3. US3 → 「文档结构与逻辑」变成能红能绿的判定
4. US4 → 无人值守驱动第一次能驱动表达类线并拦下缺证据的阶段
5. Polish → 分发、零新增机制、069 不变量与实跑证据

---

## Notes

- `[P]` 本文件未使用：测试行共享单一红先行日志，实现行共享文件或存在真实先后依赖（理由见 § Parallel Opportunities）。
- `[green:]` 认领的是「把该条款转绿的那一行」；认领分区由 `account-clause-coverage.py` 计数（必须等于 77），WARN 不靠删标签消音。
- 红先行记录必须含四个字段（重放命令、真实输出、退出码、失败计数）；只写「已执行」不算记录。
- 名册修订（T012）、分发两态（T023）、owner 追加取证（T025）属实现后守卫，不作红先行声称。
- 每个检查点的判定只看退出码、标签计数与差异行枚举，不靠阅读正文。
- **Deferral discipline**: 无法在本轮运行的行标 `[~]` 并在 `verification.md` 记 `deferred_tasks=`，不留 `[ ]` 挂着。
