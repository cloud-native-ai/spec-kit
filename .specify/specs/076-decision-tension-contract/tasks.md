# Tasks: 决策反题与反指标契约（Decision Tension Record） — 076

**Requirement ID**: 076
**Requirement Key**: `076-decision-tension-contract`
**Branch**: `076-decision-tension-contract`（本阶段禁止切换或新建分支）
**Related Feature**: Feature 076 — 决策反题与反指标契约（Decision Tension Record）, status `Planned`（tasks 阶段不推进状态机；`Implemented` 属 `/speckit.implement`）
**Input**: Design documents from `.specify/specs/076-decision-tension-contract/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required；26 FR / 8 SC / 5 用户故事 / 4 Shared Strings）、`research.md`（R-1…R-11）、`data-model.md`（E1–E8 / R1–R6 / 6 条状态迁移）、`contracts/`（8 份文件 / 34 条条款）、`quickstart.md`（S1–S5）、`feature-ref.md`

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」要求先写测试再实现，本特性三个新契约测试文件全部红先行。同时按 Principle VII 的 **template-only 门**：本特性的规范面（owner、模板章节、检测通道、ADR 槽位、术语、闭合面、镜像）没有可跑运行的运行时，它们的"测试"是**结构契约测试**——章节存在与标题序列相邻、指针路径可解析、字段名逐字、镜像逐字节、三棵分发面零命中、与基线提交 `ac63fe8c` 的差异行枚举。两层都发，且不互相替代。

**Tests**: 新行为组（`validate-decision-tensions.py` 与 `validate-falsification-quartet.py` 两个确定性校验器、模板锚点、分析通道、四元组 owner）各自先在未改动树上跑出**记录在案的失败**（重放命令 / 真实输出 / 退出码 / 失败计数，四字段落入 `notes/red-first-evidence.md`）再实现。术语与闭合面两个切片属**实现后守卫**（对已完成树的前后差异断言，不是新行为），按迁移/回归例外排在所有源改动之后，携带显式 `[blockedBy:]`，不作红先行声称。

**Organization**: 按 `requirements.md` 的五个用户故事分组（US1–US3 为 P1，US4–US5 为 P2）；Setup 与 Polish 行无故事标签。34 条契约条款由 15 行以 `[green:]` 认领，每条款恰好一行、同文件内条款序随行序递增（§ Clause Partition）。本特性无阻断全部故事的前置，Foundational 相位按模板指引省略——owner 文档是 US1 的首个交付物，US2 / US4 / US5 只按路径引用它。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/076-decision-tension-contract/verification.md` 的 `deferred_tasks=`。
- DoD-2: 34 条契约条款各被恰好一行 `[green:]` 认领；`python3 scripts/python/account-clause-coverage.py .specify/specs/076-decision-tension-contract` 报 `status: ok`、claimed=34、beyond baseline=0、FR lane 26/26。
- DoD-3: 三个契约测试文件全部红先行（`notes/red-first-evidence.md` 每组一条四字段记录）并转绿；术语与闭合面两个守卫切片在源改动完成后落地，被破坏时变红。
- DoD-4: 两个新校验器只用标准库、只读、无常驻进程，退出码 0/1/2；封闭六标签与封闭六拒收原因逐字实现，不给模型留语义打分口。
- DoD-5: `requirements.md` FR-025 表所列镜像对（行数以该表为准）相对 plan 基线无新增漂移，`regen-command-copies.py --check` 仍为 OK 且无新增副本；`templates/commands/**` 未被触及。
- DoD-6: 三棵分发面的内部别名命中 0（且 A3 清单仍在，检查不空转）；`detection-and-severity.md` 与 `critique-and-self-critique.md` 相对基线 `ac63fe8c` 只增不改。
- DoD-7: `verification.md` 为 SC-001…SC-008 各记录一条状态行，词表归 `.specify/templates/verification-log-template.md`。
- DoD-8: 不 push、不手改 `.specify/` 运行时副本；不新增 `/speckit.*` 命令、存储、台账、调度器、评分器、模型调用或第三方依赖；Feature 076 状态保持 `Planned`。
- DoD-9: plan 属主制品（`plan.md` / `requirements.md` / `research.md` / `data-model.md` / `contracts/*` / `quickstart.md` / `feature-ref.md`）不被重写；确需修订时先行声明 `PLAN-EDIT: <path> — <reason>；分类=minor|substantive`，substantive 必须停止并回传异常行。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/076-decision-tension-contract/tasks.md` 退出 0，0 error / 0 warning。
- GATE-2: 跨制品一致性 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/076-decision-tension-contract --stage tasks --repo .` 报 `decision=pass`、`errors=0`；`tasks.md` 的 `missing-path` advisory 只允许命名本特性将新建的文件（`shared/guidelines/decision-tension.md`、两个 `scripts/python/validate-*.py`、三个 `tests/contract/test_*.py`），任何其它路径的 advisory 是缺陷；`requirements.md` / `plan.md` / `contracts/` / `checklists/` 的 advisory 是 plan 阶段既有的待建文件清单，随实现完成而自然清零，不是本阶段回归。
- GATE-3: 拆解尺度门 — check: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/076-decision-tension-contract/requirements.md --tasks .specify/specs/076-decision-tension-contract/tasks.md` 报 `decision=proceed`、`task_count` ≤ 40。
- GATE-4: 条款覆盖 — check: `python3 scripts/python/account-clause-coverage.py .specify/specs/076-decision-tension-contract` 报 `status: ok`、claimed=34、beyond baseline=0；非零 beyond-baseline 用认领修复，永不重冻结基线。
- GATE-5: 新组转绿且守护无新增失败 — check: `python3 -m pytest -q tests/contract/test_decision_tension_contract.py tests/contract/test_decision_tension_validator.py tests/contract/test_falsification_quartet_validator.py` 全绿，且五个既有守护套件（`test_closed_set_claims.py`、`test_self_improvement_conformance.py`、`test_validation_carrier_contract.py`、`test_user_facing_comprehension_doc.py`、`test_validate_tasks_parallel_safety.py`）的失败名集合相对 `test-evidence/targeted-tests-baseline.txt` 无新增（捕获与比较形式归 `/speckit.implement` step 6 的 `**Test runs**` bullet，此处引用不重述）。
- GATE-6: 镜像无新增漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 对 `test-evidence/sync-mirrors-check.txt` 基线无新增 DIFF。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/076-decision-tension-contract/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器、镜像、集群、注册表或特殊硬件依赖；全部工作为本地文件、本地 git、本地 pytest。

- Python（系统解释器）: **available** — probe: `python3 --version` → `Python 3.9.6` @ 2026-10-29；affected: T007、T008、T015、T018、T022、T024（两个校验器只要求 ≥3.8 与标准库）。
- pytest: **partial** — probe: `.venv/bin/python -m pytest --version` → `No module named pytest`（仓库自带 venv 是 Python 3.14.6 但未装 pytest）；`/Users/liuqiming.lqm/project/profiles/.venv/bin/python3 -m pytest --version` → `pytest 9.1.1` @ 2026-10-29。affected: 全部测试行（T002、T003、T009、T012、T013、T017、T019、T021、T023、T025）。处置：测试一律经 profiles venv 的 `python -m pytest` 运行，与 plan 期定向基线同解释器。
- Git: **available** — probe: `git --version` → `git 2.54.0 (Apple Git-157)` @ 2026-10-29；affected: T021、T022、T025（对基线提交 `ac63fe8c` 取差异）。
- 镜像工具链: **available** — probe: `python3 scripts/python/sync-mirrors.py --check` → 六对全 `ok`、`regen-command-copies.py --check` → OK @ 2026-10-29（原始输出见 `test-evidence/sync-mirrors-check.txt`）；affected: T024。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 `[P]` 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US5]`；故事相位每行必有且仅有一个，Setup / Polish 行禁止出现。
- **[blockedBy: T004,T006]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **[green: <contract>#<clause>]**: 本行是把该条款转绿的那一行；标签面定义归 `.specify/templates/tasks-template.md` § Format，机器校验归 `scripts/python/validate-tasks.py`，合同路径相对本文件目录解析。认领分区见 § Clause Partition。
- 每行给出具体文件路径与可执行验收；测试行写明它写入的证据槽，实现行写明它让哪一组断言转绿。

## Measured Premises（2026-10-29 生成时实测，HEAD `412b4245`，分支 `076-decision-tension-contract`）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/076-decision-tension-contract/requirements.md` | `26` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/076-decision-tension-contract/requirements.md` | `8` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/076-decision-tension-contract/requirements.md` | `5` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/076-decision-tension-contract/requirements.md` | `4` |
| 测量来源条目 | `grep -cE '^- \*\*SC-[0-9]{3} Source\*\*' .specify/specs/076-decision-tension-contract/requirements.md` | `8` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/076-decision-tension-contract/contracts/*.md` | 8 份文件全 `form=md-bold-closed`；owner 8 + anchor 3 + measurement 3 + channel 5 + quartet 5 + adr 2 + validator 4 + mirrors 4 = `34` |
| 条款计数陷阱形 | `grep -oh 'C-[0-9]\{1,2\}' .specify/specs/076-decision-tension-contract/contracts/*.md \| wc -l` | `88` — 这是*提及*数（条款内互引 + 各契约的 Traceability 表），不是定义数；单位是条款*定义*时正确答案是 `34`。两数并记，表明测量是有意取的而非碰巧 |
| 三个新测试文件不在树 | `ls tests/contract/test_decision_tension_contract.py tests/contract/test_decision_tension_validator.py tests/contract/test_falsification_quartet_validator.py` | 三行 `No such file or directory`（T002 / T003 / T012 创建；069–075 无同名文件） |
| owner 与两个校验器不在树 | `ls shared/guidelines/decision-tension.md scripts/python/validate-decision-tensions.py scripts/python/validate-falsification-quartet.py` | 三行 `No such file or directory`（T004 / T007 / T015 创建） |
| `notes/` 证据槽不在树 | `ls -d .specify/specs/076-decision-tension-contract/notes` | `No such file or directory`（T001 创建；同目录已有 `test-evidence/`） |
| 模板标题序 | `grep -n '^## ' templates/plan-template.md` | Summary(9) / Technical Context(13) / Constitution Check(31) / Project Structure(62) / Complexity Tracking(152) / Phase 1(162)——`## Constitution Check` 与 `## Project Structure` 当前**相邻**，新章节插入后须三行相邻 |
| ADR 模板标题序 | `grep -n '^## ' docs/decisions/template.md` | Context(7) / Decision(11) / Alternatives(15) / Consequences(19)——槽位落 `## Alternatives` |
| 检测通道现状 | `grep -n 'The seven passes\|^### [A-I]\.' skills/internal/analyze-artifacts/references/detection-and-severity.md` | `## The seven passes`(39) + A–G 七小节；`skills/internal/analyze-artifacts/SKILL.md` 第 103 行「Seven passes … plus one checklist pass (H)」——新通道字母取 `I`，计数行两处各改一处 |
| Git 快照 | `git rev-parse HEAD`; `git branch --show-current` | `412b4245b461f9643d8bcff13fababb86e035ae7`；`076-decision-tension-contract` |
| 行数预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/076-decision-tension-contract/tasks.md` | `27` 个任务行（T001–T027）≤ 40 上限 |
| 行数预算陷阱形（同一测量的朴素变体） | `grep -cE 'T[0-9]{3}' .specify/specs/076-decision-tension-contract/tasks.md`；`grep -oE 'T[0-9]{3}' .specify/specs/076-decision-tension-contract/tasks.md \| wc -l` | `81` 行 / `202` 次 — 这是任务标识的*提及*数（`[blockedBy:]`、覆盖表、认领表都在引用），不是定义数；单位是任务*行*时正确答案是 `27`，故用行首锚定 `^- \[ \] T` 取数 |

## Clause Partition

34 条条款、8 份契约文件，每条款恰被一行认领，同文件内条款序随行序递增。认领的引擎是 `account-clause-coverage.py`（claimed 计数必须等于 34），本表只是声明。

| Contract file | Clauses | Claimed by | 行内条款带 |
|---|---|---|---|
| `contracts/decision-tension-owner.md` | C-1…C-8 | T004 | C-1…C-4 |
| `contracts/decision-tension-owner.md` | — | T006 | C-5…C-8 |
| `contracts/plan-template-anchor.md` | C-1…C-3 | T005 | C-1…C-3 |
| `contracts/validator.md` | C-1…C-4 | T007 | C-1…C-3 |
| `contracts/validator.md` | — | T008 | C-4 |
| `contracts/measurement-binding.md` | C-1…C-3 | T008 | C-1…C-3 |
| `contracts/analyze-channel.md` | C-1…C-5 | T010 | C-1…C-4 |
| `contracts/analyze-channel.md` | — | T011 | C-5 |
| `contracts/falsification-quartet.md` | C-1…C-5 | T014 | C-1、C-2 |
| `contracts/falsification-quartet.md` | — | T015 | C-3、C-4 |
| `contracts/falsification-quartet.md` | — | T016 | C-5 |
| `contracts/adr-reference.md` | C-1…C-2 | T020 | C-1、C-2 |
| `contracts/mirrors-and-scope.md` | C-1…C-4 | T022 | C-1 |
| `contracts/mirrors-and-scope.md` | — | T023 | C-2 |
| `contracts/mirrors-and-scope.md` | — | T024 | C-3 |
| `contracts/mirrors-and-scope.md` | — | T025 | C-4 |

**Partition check**: 8 + 3 + 4 + 3 + 5 + 5 + 2 + 4 = 34；15 个认领行，无条款落在两行，无行认领其相位之后才能转绿的条款带。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T002, T004 | FR-014 | T009, T011, T021, T025 |
| FR-002 | T002, T004, T007 | FR-015 | T019, T020 |
| FR-003 | T002, T004 | FR-016 | T003, T007, T008, T018 |
| FR-004 | T002, T004, T008 | FR-017 | T003, T008 |
| FR-005 | T002, T006, T017 | FR-018 | T022 |
| FR-006 | T002, T006, T017 | FR-019 | T013, T014 |
| FR-007 | T002, T006 | FR-020 | T013, T014 |
| FR-008 | T002, T005 | FR-021 | T012, T015 |
| FR-009 | T002, T005 | FR-022 | T013, T015 |
| FR-010 | T008, T019 | FR-023 | T013, T016 |
| FR-011 | T009, T010, T018 | FR-024 | T021, T023 |
| FR-012 | T009, T010 | FR-025 | T024 |
| FR-013 | T007, T009, T010 | FR-026 | T021, T025 |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T003, T008 |
| SC-002 | T009, T010, T026 |
| SC-003 | T017, T018, T026 |
| SC-004 | T012, T015 |
| SC-005 | T022 |
| SC-006 | T019, T020 |
| SC-007 | T023 |
| SC-008 | T025 |

**流程行与执行/取证行**: T001（证据槽）、T027（Feature 集成复核）为流程行，不承接任何 FR 或 SC——不是漏映射，故不在上两表出现；T026 为执行/取证行——不认领 FR，但产出 SC-002 / SC-003 的报告快照，故出现在 SC 两表。其余 25 行各至少映射一条需求（FR 或 SC）。

## Mirror Obligations

镜像对清单的属主是 `requirements.md` FR-025 的表（行数以该表为准，本文件不复述行数），本文件不复述其行内容。落地形态：源编辑分散在 T004 / T006（owner）、T005（模板）、T010 / T011（分析通道两文件）、T014（批评 owner）、T016（SI-3C 指针形核验）、T015（四元组校验器）、T007 / T008（张力校验器）；**T024 是唯一的同步与验证行**（`sync-mirrors.py --write` 后 `--check`，逐对陈述无新增漂移）。`templates/commands/**` 全程不触，命令副本面为空。`docs/decisions/template.md` 与 `tests/**` 无镜像。

## Test Budget

- **本阶段（tasks）不运行任何测试套件**（docs-only 预算）：四个确定性门（validate-tasks / decomposition-check / pre-analyze-check / account-clause-coverage）的输出留档 `test-evidence/`，全部测试断言留待实现阶段。
- **实现期基线（恰好一次）**: 实现开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获失败名基线；本文件任何行不得重捕获或刷新（重捕获会把回归网变成移动靶）。
- **闭环节点**: review 之后由驱动者跑一次全量并按名比较；本特性任何行不得预支。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建好证据槽，后续每个红先行行与守卫行都有固定落点

- [ ] T001 建立本特性证据槽：新建 `notes/red-first-evidence.md`（头部点名 `tests/contract/test_decision_tension_contract.py`、`tests/contract/test_decision_tension_validator.py`、`tests/contract/test_falsification_quartet_validator.py` 三个文件，并规定每组红先行记录四个字段——重放命令、真实输出、退出码、失败计数）、`notes/pre-change-measurements.md`（逐条粘贴 plan 期已冻结的基线：`test-evidence/sync-mirrors-check.txt` 的六对 `ok`、`test-evidence/terminology-aliases-baseline.txt` 的五个别名各 0、`test-evidence/targeted-tests-baseline.txt` 的 `70 passed`，每条带命令与日期 2026-10-29）、`notes/quickstart-run.md`（头部列 S1–S5 五个场景及各自判据，真实输出留实现期粘贴）

**Checkpoint**: 证据槽就位；本相位无阻断全部故事的前置，故无 Foundational 相位。

---

## Phase 2: User Story 1 - 承重决策留下可判定的反题、代价与重开条件 (Priority: P1) — MVP

**Goal**: 写出唯一 owner 与计划模板落点，并用一个确定性校验器把「记录成立不成立」变成退出码。

**Independent Test**: 准备一个含 1 条承重决策的夹具计划并按模板填写，运行 `python3 scripts/python/validate-decision-tensions.py --spec <fixture-dir>` 得到退出码 0；随后逐个删字段、把 `expected_sacrifice` 写成 `none`、写入不可判定措辞，校验器逐例返回 1。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写测试，确认它们失败，再实现**

- [ ] T002 [US1] 红先行编写 `tests/contract/test_decision_tension_contract.py` 的场景 A（owner 与模板锚点）：owner 开篇声明拥有面与「消费者以路径引用、不复述判据表」的义务、六字段封闭集加 `tension_id` 的 `T-NNN` 唯一按序形态、四条可采纳判据、拒绝清单首条为字面 `expected_sacrifice: none`（值为空按同一条判）、**拒绝形态的判定者分工**（机械三项由校验器判、语义两项由两位复核者按同一判据判且必须得到同一 verdict）、承重四类触发与 Trivial 不触发、复杂度门控指向 `shared/guidelines/task-complexity-rubric.md`、四个相邻 owner 各以路径引用、无第二定义点且不引入载体；模板侧断言 `templates/plan-template.md` 的 `^## ` 标题序列三行相邻、`### T-NNN` 承载规则、`N/A` 加四类触发逐条说明、指针路径可解析、未逐行复制 owner 表；在未改动树上跑出记录在案的失败运行（命令行 / 真实输出 / 退出码 / 失败计数写入 `notes/red-first-evidence.md`）
- [ ] T003 [US1] 红先行编写 `tests/contract/test_decision_tension_validator.py`：CLI 契约（`python3 scripts/python/validate-decision-tensions.py --spec <spec-dir> [--json]` 读 `plan.md` 与 `requirements.md`，退出码 0/1/2）、封闭六标签 `dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` / `dtr-rejected-form` / `expected-sacrifice-unmapped` 与「同记录同标签只报一条」、跨标签优先级三条（章节缺失时只报 `dtr-section-missing` 并抑制 `dtr-anchor`；字段标签缺失时只报 `dtr-record-incomplete` 并抑制 `expected-sacrifice-unmapped`；值为空——`expected_sacrifice` 留空、任一极点缺失或留空——或 `expected_sacrifice` 恰为 `none` 时只报 `dtr-rejected-form`，抑制 `dtr-record-incomplete` 与 `expected-sacrifice-unmapped`）、人读 `status` 行加每标签 `[label] pass|fail (count)` 与 `--json` 六字段 `spec` / `status` / `checks` / `errors` / `warnings` / `scanned`；夹具在 `tmp_path` 内以字面量构造（一个合规计划 + 六个反向输入：删去任一字段——六字段逐一各一例、把 `expected_sacrifice` 写成字面 `none`、不可判定措辞、重复 `tension_id`、`tension_id` 跳号（如 `T-001` 后接 `T-003`）、指向不存在的测量来源）；跑出记录在案的失败运行

### Implementation for User Story 1

- [ ] T004 [US1] [blockedBy: T002] 新建 `shared/guidelines/decision-tension.md` 的开篇与判据段：开头逐项声明本文件拥有六字段记录形态、可采纳判据、拒绝形态、承重门槛、相邻 owner 边界与记录标识形态，并写明一切消费者以路径引用而不复述；随后写出封闭六字段（`decision` / `antithesis` / `binding_constraints` 含 `pole_a` 与 `pole_b` / `discriminating_evidence` / `expected_sacrifice` / `revision_trigger`）与 `tension_id` 形态、四条可采纳判据（单句点名一极；反题为可独立采纳的具名方案并给出至少一条「在什么条件下更优」；双极非空且被选方案不同时满足；判别性证据一位复核者可执行且结果二值）、封闭拒绝清单（首条字面 `expected_sacrifice: none`，值为空按同一条判；另含空极点、不可执行或非二值证据、稻草人反题、以「要平衡」「综合考虑」「视情况而定」代替取舍），并写出**拒绝形态的判定者分工**：机械可判三项（`none` 或空代价、空极点、命中措辞清单）归校验器，语义两项（稻草人、证据不可执行或非二值）归两位复核者按同一判据判定且必须得到同一 verdict [green: contracts/decision-tension-owner.md#C-1] [green: contracts/decision-tension-owner.md#C-2] [green: contracts/decision-tension-owner.md#C-3] [green: contracts/decision-tension-owner.md#C-4]
- [ ] T005 [US1] [blockedBy: T004] 在 `templates/plan-template.md` 的 `## Constitution Check` 之后、`## Project Structure` 之前插入 `## Decision Tensions`：内容只有一条指向 `shared/guidelines/decision-tension.md` 的指针加字段名清单，写明每条记录以 `### T-NNN` 子节承载、无承重决策时写 `N/A` 并逐条说明四类触发均不成立（不得删除或留空），且不复述 owner 的可采纳判据表、拒绝清单或门槛表；`.specify/templates/plan-template.md` 由 `sync-mirrors.py` 产出，不手改 [green: contracts/plan-template-anchor.md#C-1] [green: contracts/plan-template-anchor.md#C-2] [green: contracts/plan-template-anchor.md#C-3]
- [ ] T006 [US1] [blockedBy: T004] 续写 `shared/guidelines/decision-tension.md` 的门槛与边界段：承重四类触发（不可逆 / 跨团队 / 高爆炸半径 / 与宪法原则相关）任一成立即承重，不满足任一触发的决策不得被要求写记录、缺记录不得判缺陷；复杂度门控引用 `shared/guidelines/task-complexity-rubric.md` 的分级并声明 Trivial 按定义不含承重决策、分级与承重判据冲突时按该 rubric 的 tie-break 取较高一级且以承重判据为准；声明与 `shared/definitions/derivation-definitions.md` § Contradiction Handling、`/speckit.clarify` 与访谈账本、`shared/guidelines/fast-fail.md`、`shared/guidelines/critique-and-self-critique.md` 四个相邻机制的分工并各以路径引用，限定自己只承接方向已选定之后的技术取舍；消费者清单写成「路径 + 引用方式」指针形，全文不引入台账、调度器、评分器或运行时 [green: contracts/decision-tension-owner.md#C-5] [green: contracts/decision-tension-owner.md#C-6] [green: contracts/decision-tension-owner.md#C-7] [green: contracts/decision-tension-owner.md#C-8]
- [ ] T007 [US1] [blockedBy: T003] 新建 `scripts/python/validate-decision-tensions.py` 的骨架与四条结构检查：只用标准库、只读、无常驻进程，参数 `--spec <spec-dir>` 与 `--json`，读 `<spec-dir>/plan.md` 与 `<spec-dir>/requirements.md`（缺任一、不可解码或无内容行 → 退出码 2）；实现 `dtr-anchor`（`^## ` 序列三行相邻）、`dtr-section-missing`（章节缺失）、`dtr-record-incomplete`（六个字段标签齐备；`decision` / `antithesis` / `discriminating_evidence` / `revision_trigger` 留空仍判本标签，只有 `expected_sacrifice` 留空或字面 `none`、`pole_a` / `pole_b` 行缺失或留空归 `dtr-rejected-form`，见 T008）、`dtr-tension-id`（`T-NNN` 形态、唯一、按序递增）；输出 `status` 行 + 每标签 `[label] pass|fail (count)` + findings，`--json` 输出六字段；导出记录索引函数供 ADR 断链检查复用 [green: contracts/validator.md#C-1] [green: contracts/validator.md#C-2] [green: contracts/validator.md#C-3]
- [ ] T008 [US1] [blockedBy: T007] 在 `scripts/python/validate-decision-tensions.py` 内实现 `expected_sacrifice` 解析与拒绝形态：封闭形态 `<SC-NNN> Source <↓|↑>`，标识必须解析到 `requirements.md` § `### Measurement Sources & Collection Methods` 中 `**SC-NNN Source**` 起头的条目，方向缺失或越出两值、值中出现第二个 `SC-NNN`、无 `Source` 连接词一律判 `expected-sacrifice-unmapped`，不回落人工阅读；字段标签缺失时只报 `dtr-record-incomplete` 且不再执行映射判定；值为空（`expected_sacrifice` 留空、任一极点缺失或留空）或 `expected_sacrifice` 恰为 `none` 时只报 `dtr-rejected-form`，抑制 `dtr-record-incomplete` 与 `expected-sacrifice-unmapped`；实现不可判定措辞与空极点的拒绝形态，使六个反向输入各自单独命中一个标签（章节缺失类另判跨标签优先级）、`tests/contract/test_decision_tension_validator.py` 转绿 [green: contracts/measurement-binding.md#C-1] [green: contracts/measurement-binding.md#C-2] [green: contracts/measurement-binding.md#C-3] [green: contracts/validator.md#C-4]

**Checkpoint**: US1 独立可验——夹具计划一条记录经校验器返回 0，六个反向输入各返回 1（删除一类逐字段各一次）；模板与 owner 的结构断言全绿。

---

## Phase 3: User Story 2 - 分析阶段拦住不成立的张力记录 (Priority: P1)

**Goal**: 把「记录成立不成立」接进 `/speckit.analyze` 的检测面，三类缺陷各判 HIGH 且无降级档。

**Independent Test**: 四个夹具（合规 / 缺章节 / 六字段不全 / 代价不可映射）各命中一次，判定只读报告里的严重度与条目计数。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T009 [US2] [blockedBy: T008] 红先行编写 `tests/contract/test_decision_tension_contract.py` 的场景 B（分析结构通道）：通道只判 `REQUIREMENTS_DIR` 下的 `plan.md` 一份工件、不打开其他特性目录、范围内历史计划不豁免而范围外不产生发现；三类缺陷各判 HIGH 且取值只有 HIGH 与 0、无 advisory 或降级档；`requirements.md` 无测量来源节时按记录数机械分叉；严重度取 `.specify/shared/workflow/objective-analysis-gate.md` 的传播面判据且每条发现首字段写传播面；可机械判定部分消费 `scripts/python/validate-decision-tensions.py` 的 verdict；落点在 `skills/internal/analyze-artifacts/references/detection-and-severity.md` 且只增不改，`skills/internal/analyze-artifacts/SKILL.md` 第 5 步的通道枚举随之更新；四个夹具在 `tmp_path` 构造；跑出记录在案的失败运行

### Implementation for User Story 2

- [ ] T010 [US2] [blockedBy: T009] 在 `skills/internal/analyze-artifacts/references/detection-and-severity.md` 的既有 A–G 之后新增结构通道小节：判定对象只有本轮 `plan.md` 一份，`requirements.md` 只作映射参照；三类缺陷（缺章节或裸 `N/A`、六字段不全含单极约束、代价无法解析）各判 HIGH 且不设 advisory 或降级档；严重度按既有传播面判据、每条发现首字段写「计划 → 任务 / 实现」；可机械判定部分消费校验器 verdict，不交模型语义打分；`.specify/skills/internal/analyze-artifacts/` 同名副本由 `sync-mirrors.py` 产出，不手改 [green: contracts/analyze-channel.md#C-1] [green: contracts/analyze-channel.md#C-2] [green: contracts/analyze-channel.md#C-3] [green: contracts/analyze-channel.md#C-4]
- [ ] T011 [US2] [blockedBy: T010] 注册新通道并钉住允许差异集：把 `skills/internal/analyze-artifacts/references/detection-and-severity.md` 的 `## The seven passes` 计数标题改为八条通道、新通道字母取 `I`（`H` 已被 checklist 通道占用），同步 `skills/internal/analyze-artifacts/SKILL.md` 第 5 步的通道枚举句；在场景 B 的契约测试里把该文件的允许差异集声明为「新增通道小节 + 该计数标题行」，`SKILL.md` 的枚举更新声明为闭合面之外的指针更新 [green: contracts/analyze-channel.md#C-5]

**Checkpoint**: US2 独立可验——四个夹具的 HIGH 计数分别为 0 / 1 / 1 / 1，且通道只判一份工件。

---

## Phase 4: User Story 3 - 证伪尝试必须真的跑过，而且能变红 (Priority: P1)

**Goal**: 把「一句话加 verdict」升级为封闭四元组，判决交确定性脚本，接收方不得反向覆盖。

**Independent Test**: 一个合规载荷被接收；封闭六拒收原因码各一例全部被拒收（另有四个 `missing-field` 附加样本），每条具名给出原因码与缺失字段或失败的那半条件，判决由脚本退出码输出。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T012 [US3] 红先行编写 `tests/contract/test_falsification_quartet_validator.py`：一个合规载荷被接收（退出码 0）；封闭六拒收原因码各一例被拒收并具名给出原因 `missing-field` / `empty-field` / `exit-code-not-integer` / `observation-not-raw` / `tautology` / `input-unreadable`，拒收率 6/6；四字段各缺一的四例作为 `missing-field` 的附加样本（同一原因码，不参与 6/6 计数）；`tautology` 一例按 FR-021 的机械形状构造（缺 `red:` 标记、或 `red:` 之后无反引号跨度）；另加一个**双 `red:`** 定点夹具，断言「以第一次出现的 `red:` 切分」得到确定 verdict（构造为：首次切分之前有反引号跨度、首次切分之后有反引号跨度，故被接收；若按后一次切分则信号半为空、会变成 `tautology`——夹具断言切分点唯一，该例独立于原因码矩阵、不进入上述十一次运行的计数）；退出码 0/1/2 三值各有一次运行，原因码矩阵共十一次运行；载荷在 `tmp_path` 内以字面量构造；跑出记录在案的失败运行
- [ ] T013 [US3] 红先行编写 `tests/contract/test_decision_tension_contract.py` 的场景 C（四元组 owner 与 SI-3C 指针）：`shared/guidelines/critique-and-self-critique.md` 定义封闭四元组 `attempt` / `exit_code` / `observation` / `would_go_red_if`、各字段可判定语义（`observation` 以字面 `raw:` 起头作为「非转述」的机械代理、`would_go_red_if` 同时给出被改坏的具名输入与具名红色信号）、既有「一句话证伪尝试」段落逐字保留且新小节声明四元组即产出形态、**小节披露两处已披露限制**（`raw:` 标记可被伪造；`red:` 信号的真实性——输入改坏了却不会变红——不可证）**及各自处置**（由复核者发现、只记非阻断注记、不进程序判决）、载体不变（不新增台账 / 存储 / probe / 评分）、`shared/workflow/self-improvement-workflow.md` § SI-3C 只保留步骤摘要与指针且无第二份字段定义；跑出记录在案的失败运行

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T013] 改写 `shared/guidelines/critique-and-self-critique.md`：在既有「输出形态：每个提案一条证伪尝试」段之后新增四元组小节（四个字面键各出现一次、值取键后同行或缩进续行、`raw:` 代理、`red:` 分隔的两半形状、反空真两半条件、扩展须走 owner 修订），声明四元组是产出形态，并**披露两处限制及其处置**——`raw:` 标记可被伪造、`red:` 信号的真实性不可证，两处均由复核者发现、只作非阻断注记、不进程序判决；既有段落逐字保留，不改写、不删除；`.specify/shared/guidelines/critique-and-self-critique.md` 由 `sync-mirrors.py` 产出，不手改 [green: contracts/falsification-quartet.md#C-1] [green: contracts/falsification-quartet.md#C-2]
- [ ] T015 [US3] [blockedBy: T012,T014] 新建 `scripts/python/validate-falsification-quartet.py`：调用 `python3 scripts/python/validate-falsification-quartet.py <payload.md> [--json]`，退出码 0 接收 / 1 拒收 / 2 载荷不可读（按拒收处置，原因 `input-unreadable`）；判四个字面键各出现一次、`exit_code` 为整数、`observation` 值以 `raw:` 起头、`would_go_red_if` 按机械形状判两半（切分点取**第一次**出现的字面 `red:`，后续 `red:` 不移动切分点；切分点之前至少一个反引号跨度＝被改坏的具名输入；切分点之后至少一个反引号跨度＝断言名 / 检查标签 / 非零退出码），缺标记或缺任一 span 即 `tautology`；拒收原因取封闭六值并具名指出缺哪个字段或哪半条件；只用标准库、只读、不重放 `attempt` 也不判其可重放性（故不设 `attempt-not-replayable`）、不新增台账或存储 [green: contracts/falsification-quartet.md#C-3] [green: contracts/falsification-quartet.md#C-4]
- [ ] T016 [US3] [blockedBy: T015] 核验 `shared/workflow/self-improvement-workflow.md` § SI-3C 仍为**指针形**并留证：读该步，确认它只有步骤摘要加指向 `shared/guidelines/critique-and-self-critique.md` 的指针、没有四元组字段清单或拒收规则的复述（现状实测已如此，本行不是改写行）；若 T014 之后出现了复述则删去该复述再留证。证据写入 `notes/red-first-evidence.md` 的对应组（命令、输出、退出码、判定）与 `verification.md`；`.specify/shared/workflow/self-improvement-workflow.md` 只在确有复述时才改，且改动由 `sync-mirrors.py` 产出副本 [green: contracts/falsification-quartet.md#C-5]

**Checkpoint**: US3 独立可验——一个合规载荷接收、六个拒收原因码各拒收一次（加四个 `missing-field` 附加样本）、`raw:` 与 `red:` 两处形状各判一次。

---

## Phase 5: User Story 4 - 非承重决策不被仪式拖累 (Priority: P2)

**Goal**: 让门控可解释——trivial 计划零记录零发现，补入一条不可逆决策就必须出现发现。

**Independent Test**: trivial 夹具（`N/A` 加逐条说明）零记录、退出 0；同一夹具补入一条不可逆决策后复跑恰出现一条 `dtr-section-missing`。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T017 [US4] [blockedBy: T006,T008] 红先行编写 `tests/contract/test_decision_tension_contract.py` 的场景 D（非承重不触发与门控可达性），拆成三个独立子场景、每次运行只断言一个变体：**D-1 基线**——trivial 夹具写 `N/A` 并逐条说明四类触发均不成立 → 校验器退出 0、记录条数 0（这一次运行即 SC-003 的第一份快照）；同一夹具写裸 `N/A`（无逐条说明）→ 退出 1 且命中 `dtr-section-missing`——该裸 `N/A` 运行是 **SC-003 三次运行之外的附加断言**，只钉 `N/A` 判据，不产快照、不计入 SC-003。**D-2 删章节**——同一夹具补入一条不可逆决策（回滚需要迁移）并**移除**该合规 `N/A` 章节 → 复跑恰一条 `dtr-section-missing`（在 SC-003 的三连跑内，「恰 1 条 HIGH」只在此步可达；`dtr-anchor` 被抑制不叠加）。**D-3 补记录**——在同一位置写入一条合规 `### T-001` 记录以替换 `N/A` → 复跑 0 条 HIGH（修复路径成立）；SC-003 只取三份快照——合规 `N/A` → 0、删章节 → 1、补合规记录 → 0，三个子场景各运行一次并各留一份 analyze 报告快照到 `notes/analyze-sc003/`（D-1 / D-2 / D-3 各一份），SC-003 的 HIGH 计数只读这三份快照；`requirements.md` 无 `### Measurement Sources & Collection Methods` 时按记录数机械分叉（≥1 条记录则逐条 `expected-sacrifice-unmapped`，合规 `N/A` 零记录则零发现）；复杂度与承重判据冲突时以 rubric tie-break 取较高一级；跑出记录在案的失败运行

### Implementation for User Story 4

- [ ] T018 [US4] [blockedBy: T017] 在 `scripts/python/validate-decision-tensions.py` 内实现 `N/A` 判据与测量来源缺失的机械分叉：`N/A` 必须伴随四类触发逐条「均不成立」的说明，否则计入 `dtr-section-missing`；`requirements.md` 缺测量来源节时，计划含 ≥1 条记录则每条 `expected_sacrifice` 判解析失败，合规 `N/A`（零记录）则不执行映射判定、零发现；不引入 advisory 或降级档，使场景 D 转绿

**Checkpoint**: US4 独立可验——同一夹具三次运行（合规 `N/A` / 删章节 / 补合规记录）的记录数与发现数即可判定，「恰 1 条 HIGH」只在删章节那一次出现，不需读正文。

---

## Phase 6: User Story 5 - 计划、ADR 与测量来源互相可达 (Priority: P2)

**Goal**: 事后的 ADR 只按 `tension_id` 引用计划里的记录，断链是错误而不是提示。

**Independent Test**: ADR 模板含引用位；抽查夹具计划中每条记录的预期代价都解析到一条已声明的测量来源；指向不存在记录的引用被判断链错误。

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T019 [US5] [blockedBy: T008] 红先行编写 `tests/contract/test_decision_tension_contract.py` 的场景 E（ADR 引用位与断链）：`docs/decisions/template.md` 的 `## Alternatives` 含 `tension_id` 引用位、以 `T-NNN` 指向同一特性计划记录且不复制字段内容、无承重记录时须写「无承重张力记录」加判定结论、指向不存在记录的引用经校验器的记录索引函数被判断链错误（夹具对：一份计划 + 一条不可解析的 `tension_id`）；同一夹具计划中每条记录的 `expected_sacrifice` 均可解析到一条已声明测量来源；跑出记录在案的失败运行

### Implementation for User Story 5

- [ ] T020 [US5] [blockedBy: T019] 改写 `docs/decisions/template.md` 的 `## Alternatives`：增加 `tension_id` 引用位（`T-NNN` 指向同一特性计划中的记录、不复制任何字段内容），并写明无承重张力记录时须显式写「无承重张力记录」及判定结论而非留空；断链判定复用 `scripts/python/validate-decision-tensions.py` 的记录索引函数，不新写第二个解析器；`docs/` 不在镜像对内，本文件无副本 [green: contracts/adr-reference.md#C-1] [green: contracts/adr-reference.md#C-2]

**Checkpoint**: US5 独立可验——三处（计划记录 / ADR 引用 / 测量来源）各自只是引用，断链报错。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 术语与闭合面的前后守卫、镜像收尾、零新增机制判定与实跑留档

- [ ] T021 [blockedBy: T016,T020] 在 `tests/contract/test_decision_tension_contract.py` 追加两个**实现后守卫**切片（非红先行，属迁移/回归例外）：场景 F 术语——`shared/`、`templates/`、`skills/` 三棵分发面零命中 A3 五个内部别名，且正控断言 `requirements.md` § Assumptions A3 的别名清单仍存在（清单被改名或清空不得让零命中检查空转）；白名单只有 A3 本节与 `.specify/memory/features/076.md` § 附两处、均在分发面之外，owner 正文不在白名单内；场景 G 闭合面——`detection-and-severity.md` 与 `critique-and-self-critique.md` 相对基线提交 `ac63fe8c` 的差异行逐条枚举并落在声明的允许差异集内、集合外删除或改写行数为 0、拒绝形态 / 边界声明 / 消费者清单条目数不小于基线
- [ ] T022 [blockedBy: T021] 零新增机制的前后集合差：采集 `/speckit.*` 命令清单（`templates/commands/` 与各工具副本目录的并集）、依赖清单与进程清单在基线 `ac63fe8c` 与当前树的两份快照，差异必须落在空集，把两份快照与差异输出写入 `test-evidence/scope-set-difference.txt` [green: contracts/mirrors-and-scope.md#C-1]
- [ ] T023 [blockedBy: T021] 复测术语合规并留档：对 `shared/`、`templates/`、`skills/` 三棵树逐个别名 grep，把计数与正控输出写入 `test-evidence/terminology-counts-after.txt`，判据为五个别名各 0 且 A3 清单仍在（白名单只有 A3 与 Feature 详情 § 附两处，均在分发面之外），与 `test-evidence/terminology-aliases-baseline.txt` 的改动前计数相同 [green: contracts/mirrors-and-scope.md#C-2]
- [ ] T024 [blockedBy: T021] 镜像收尾：跑 `python3 scripts/python/sync-mirrors.py --write` 产出全部 `.specify/` 副本后再跑 `--check`，对 `requirements.md` FR-025 表所列全部镜像对（行数以该表为准）逐对陈述相对 plan 基线 `test-evidence/sync-mirrors-check.txt` 无新增漂移；`python3 scripts/python/regen-command-copies.py --check` 仍为 OK 且无新增副本；输出写入 `test-evidence/sync-mirrors-check-after.txt` [green: contracts/mirrors-and-scope.md#C-3]
- [ ] T025 [blockedBy: T024] 闭合面不回退的最终判定：用场景 G 的差异行枚举对 `detection-and-severity.md` 与 `critique-and-self-critique.md` 逐文件比对基线 `ac63fe8c`，允许差异集只含新增段落与新增通道逼出的计数行，集合外删除或改写行数为 0、集合内结构不变量可解析，条目计数比较结果写入 `test-evidence/closed-set-delta.txt` [green: contracts/mirrors-and-scope.md#C-4]
- [ ] T026 [blockedBy: T025] 实跑 `quickstart.md` 的 S1–S5 五个场景（S1 首条记录与校验、S2 六个反向输入、S3 分析三类缺陷、S4 四元组接收与六类拒收、S5 镜像与术语），把每条命令的真实输出与拆卸步骤贴入 `notes/quickstart-run.md`；S3 的四个夹具各留一份 analyze 报告快照（SC-002），并按 T017 的 D-1（合规 `N/A` 那一次；裸 `N/A` 的附加断言不产快照）/ D-2 / D-3 三次运行各留一份报告快照（SC-003：三次运行各一份）；不改写 plan 属主的 `quickstart.md`
- [ ] T027 [blockedBy: T026] Feature 集成复核：更新 `.specify/memory/features/076.md` 记录本特性的设计落点与实现期留痕，复核 `.specify/memory/features.md` 的 076 行无需变更（本阶段未发现新特性、无行失效），状态保持 `Planned` 不推进

**Checkpoint**: 全部 SC 有证据；镜像与闭合面无新增漂移；零新增机制。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **US1 (Phase 2)**: 依赖 Setup 的证据槽；本特性的 MVP。
- **US2 (Phase 3)**: 依赖 US1 的校验器（通道消费其 verdict）与 owner（字段判据）。
- **US3 (Phase 4)**: 除证据槽外不依赖 US1——四元组与张力记录是两条独立交付面。
- **US4 (Phase 5)**: 依赖 US1 的 owner 门槛段与校验器骨架。
- **US5 (Phase 6)**: 依赖 US1 的记录索引函数。
- **Polish (Phase 7)**: 依赖 US1–US5 全部源改动完成（镜像同步必须最后跑）。

### User Story Dependencies

- **US1 (P1)**: 无跨故事依赖——owner、模板、校验器三者自成闭环。
- **US2 (P1)**: 消费 US1 的校验器输出与 owner 判据，`[blockedBy: T008]`。
- **US3 (P1)**: 与 US1 无关；只与自身两条实现行串行。
- **US4 (P2)**: 消费 US1 的门槛段与校验器，`[blockedBy: T006,T008]`。
- **US5 (P2)**: 消费 US1 的记录索引函数，`[blockedBy: T008]`。

### Within Each User Story

- 测试先行，且必须先在未改动树上跑出记录在案的失败
- 同一文件的多行按 `[blockedBy:]` 串行；条款认领随行序递增
- 实现行让对应测试组转绿后才进入下一行

### Parallel Opportunities

- **本文件没有 `[P]` 行，这是测量结论而不是省略**：所有测试行都向同一个 `notes/red-first-evidence.md` 追加记录（红先行日志是单写点），所有实现行要么改同一个文件（owner 两段、校验器两段），要么需要前一行已落盘才能让断言通过（模板的指针路径必须解析到已存在的 owner）。把它们标成并行会声明一个写集与依赖图都不支持的并行度。
- 可并行的只有故事层：US1 与 US3 写不同文件、无相互依赖，多 agent 下可同时开工；两者仍串行在证据日志上（每次追加一行），故不体现为 `[P]` 标签。
- US2 / US4 / US5 因 `[blockedBy:]` 无法与 US1 并行：它们消费校验器输出或 owner 判据。

---

## Parallel Example: Story-level only

```bash
# 双 agent 场景（可选）：证据日志按「一次追加一行」串行，两故事写集不相交
Agent A: "US1 — T002 → T004 → T005 → T006 → T003 → T007 → T008"
Agent B: "US3 — T012 → T013 → T014 → T015 → T016"

# 单 agent 场景：按 T001 → US1 → US2 → US3 → US4 → US5 → Polish 顺序执行
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = US1**（P1 且独自构成可独立验收的增量：owner 定义形态、模板给出落点、校验器给出退出码；三者缺一即半套机制）。US2 在没有 US1 时没有判定对象，故不并入 MVP。

1. 完成 Phase 1：证据槽
2. 完成 US1（T002–T008）→ **STOP and VALIDATE**：夹具计划一条记录返回 0，六个反向输入各返回 1
3. 再推进 US2 / US3（可交换顺序），随后 US4 / US5
4. 最后 Polish

### Incremental Delivery

1. US1 → 计划作者第一次能写出被判定的记录
2. US2 → 分析阶段开始拦不成立的记录
3. US3 → 改进提案的证伪尝试变成可判定四元组（与 US1/US2 无耦合，可提前交付）
4. US4 → 门控可解释，trivial 任务不被仪式拖累
5. US5 → 三处互相可达，断链报错
6. Polish → 术语、闭合面、镜像、零新增机制与实跑证据

---

## Notes

- `[P]` 本文件未使用：测试行共享单一红先行日志，实现行共享文件或存在真实先后依赖（理由见 § Parallel Opportunities）。
- `[green:]` 认领的是「把该条款转绿的那一行」；认领分区由 `account-clause-coverage.py` 计数（必须等于 34），WARN 不靠删标签消音。
- 红先行记录必须含四个字段（重放命令、真实输出、退出码、失败计数）；只写「已执行」不算记录。
- 守卫切片（术语、闭合面）在源改动完成后落地，属迁移/回归例外，不作红先行声称。
- 每个检查点的判定只看退出码、标签计数与差异行枚举，不靠阅读正文。
- **Deferral discipline**: 无法在本轮运行的行标 `[~]` 并在 `verification.md` 记 `deferred_tasks=`，不留 `[ ]` 挂着。
