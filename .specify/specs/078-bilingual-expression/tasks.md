# Tasks: 双语表述（Bilingual Expression）— 078

**Requirement ID**: 078
**Requirement Key**: `078-bilingual-expression`
**Branch**: `078-bilingual-expression`（本阶段禁止切换或新建分支；不 push）
**Related Feature**: Feature 078 — 双语表述（Bilingual Expression）, status `Planned`（tasks 阶段不推进状态机；`Planned → Implemented` 归 `/speckit.implement`，活状态只在 `.specify/memory/features.md` 的 078 行）
**Input**: Design documents from `.specify/specs/078-bilingual-expression/`
**Prerequisites**: `plan.md`（required，含 `## Document Structure` 四子节）、`requirements.md`（required；18 FR / 5 SC / 4 用户故事 / 3 Shared Strings）、`research.md`（R-1…R-12，三项基线冻结于 R-8）、`data-model.md`（E1…E7）、`contracts/`（4 份文件 / 35 条款，全部 `md-bold-closed`）、`quickstart.md`（S1–S8）、`feature-ref.md`

**Tests Mode**: ON — 宪法 Principle IV「Test-First & Contract-Driven Implementation」把测试定为先写后实现；本特性红先行起点 = 本次实测的红（`tests/contract/test_bilingual_expression.py`、检查器 [[STR-001]] 的实现载体、ambient 小节均不存在）。按 Principle VII 的 template-only 门复核：本特性的测试对象含真实可执行检查器（`scripts/python/bilingual-expression-check.py`），「Partial (justified)」路径按 plan § Constitution Check VII 的裁决**不存在**；owner 文档与 ambient 这类文档面由同一红先行测试文件内的**结构契约腿**（章节树逐字、owner 声明、枚举列表形态、ambient 摘要+指针形态）验证，不另立运行时测试，两层不互相替代。

**Tests**: 红先行只写一个测试文件 `tests/contract/test_bilingual_expression.py`（T002 一次写全各腿并随测试建立夹具 `tests/fixtures/bilingual/`），在未改动树上跑出记录在案的失败（重放命令 / 真实输出 / 退出码 / 失败计数四字段，落入 `notes/red-first-evidence.md`）；实现行按 `[green:]` 认领把对应契约条款转绿。迁移/回归例外不适用（无守卫既有行为的移植测试）。

**Organization**: 按 `requirements.md` 的四个用户故事分组（US1/US2 为 P1，US3/US4 为 P2）；Setup 与 Polish 行无故事标签。35 条契约条款由 T003/T007/T008/T009/T010/T011/T012/T013/T014/T015/T016/T017 共 12 行以 `[green:]` 认领，每条款恰好一行、同文件内条款序随行序递增（§ Clause Partition）。本特性无阻断全部故事的前置，Foundational 相位按模板指引省略——证据槽（T001）是唯一共享前置。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/078-bilingual-expression/verification.md` 的 `deferred_tasks=`。
- DoD-2: 35 条契约条款各被恰好一行 `[green:]` 认领；`python3 scripts/python/account-clause-coverage.py .specify/specs/078-bilingual-expression` 报 `status: ok`、claimed=35、beyond baseline=0、FR 车道 `FR uncovered: 0`（18/18）。
- DoD-3: `tests/contract/test_bilingual_expression.py` 红先行（`notes/red-first-evidence.md` 四字段齐全）并全绿；夹具三文件（合规 / 全角违规 / 同向违规）存在且被测试引用。
- DoD-4: 检查器只用标准库、只读扫描、无常驻进程；三动作 `scan`/`coverage`/`census`、退出码 0/1/2、finding 码封闭四值（`full-width-parens` / `same-language-bracket` / `missing-bilingual` / `coverage-missing`）；不并入 `doc-consistency-check.py`（T-002 的解耦裁决）、不绑定任何阶段门禁算子（FR-010）。
- DoD-5: 分发判据为「相对 plan 期基线无新增漂移」——`sync-mirrors.py --check` 本特性触碰的三对（shared / templates / scripts）相对 `test-evidence/plan-sync-mirrors-baseline.txt` 无新增 DIFF；`.specify/instructions.md` 与根 `AGENTS.md` 由 `generate-instructions.sh` 刷新产出（非手改），生成器 size report 留档；`scan-confirmation-gates.py --summary` 的 blocking 计数相对基线 27 不变。
- DoD-6: SC-001…SC-005 的 implement 期采证全部落 `test-evidence/`（E6 存量清单 / E7 关键词快照 / SC-003 pilot / SC-004 diff 审计 / 受控语料 census）；SC-002 的 review 面抽样复核与 SC-005 的真实词汇表实跑归 review 阶段，implement 期交付确定性抽样程序与受控语料证据，不预支 review 结论。
- DoD-7: `verification.md` 为 SC-001…SC-005 各记录一条状态行，词表归 `.specify/templates/verification-log-template.md`；Test-First 记 ON（本特性有真实可执行检查器为测试对象，不走宪法 VII 的 Partial 路径；owner 文档 / ambient 面由结构契约腿替代验证并写明）。
- DoD-8: 不新增 `/speckit.*` 命令、不引入运行时/服务/后台进程、不新增第三方依赖；Feature 078 在 tasks 阶段结束时保持 `Planned`；除 owner 文档、ambient 载体、检查器与其测试、登记文件与规格产物外，既有文档修改行数为 0（SC-004 审计）。
- DoD-9: plan 属主制品（`plan.md` / `research.md` / `data-model.md` / `contracts/*` / `quickstart.md` / `feature-ref.md`）不被重写；本阶段对 `checklists/requirements.md` 一行的改写属证据面误捕修复（G-tasks-evidence 实测 `grade-asof-unpaired`，与 requirements 阶段已记录的同类修复同形），已在本文件头与收尾声明，非 plan 属主制品。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 scripts/python/validate-tasks.py .specify/specs/078-bilingual-expression/tasks.md` 退出 0，0 error（WARN 逐条裁定）。
- GATE-2: 跨制品一致性 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/078-bilingual-expression --stage tasks --repo .` 报 `decision=pass`、`errors=0`；`missing-path` advisory 只允许命名本特性将新建的文件（[[STR-001]]、检查器、契约测试、夹具、`notes/*`、本阶段 `test-evidence/tasks*`）。
- GATE-3: 拆解尺度门 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/078-bilingual-expression/requirements.md --tasks .specify/specs/078-bilingual-expression/tasks.md` 报 `decision=proceed`、`task_count` ≤ 40。
- GATE-4: 条款覆盖 — check: `python3 scripts/python/account-clause-coverage.py .specify/specs/078-bilingual-expression` 报 `status: ok`、claimed=35、beyond baseline=0；非零 beyond-baseline 用认领修复，永不重冻结基线。
- GATE-5: 红先行留档且新测试转绿、既有守护无新增失败 — check（实现期，经 `python3 -m pytest`）：`tests/contract/test_bilingual_expression.py` 全绿，捕获与比较形式归 `/speckit.implement` step 6 的 `**Test runs**` bullet（此处引用不重述）。
- GATE-6: 镜像与确认门收口 — check: `python3 scripts/python/sync-mirrors.py --check` 相对 `test-evidence/plan-sync-mirrors-baseline.txt` 无新增 DIFF（本特性三对）；`python3 scripts/python/scan-confirmation-gates.py --summary` 的 blocking 计数 == 27（基线 `test-evidence/plan-scan-confirmation-gates.txt`）。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/078-bilingual-expression/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器、镜像、集群、注册表或特殊硬件依赖；全部工作为本地文件、本地 git、本地 pytest。

- Python（系统解释器）: **available** — probe: `python3 --version` → `Python 3.11.11` @ 2026-10-30；affected: T007（检查器）、全部测试行。要求 ≥3.8 且仅标准库，实测满足。
- pytest: **available** — probe: `python3 -m pytest --version` → `pytest 8.2.2`（系统解释器自带） @ 2026-10-30；affected: T002 及 GATE-5。处置：本线测试一律经 `python3 -m pytest` 运行（与 077 的 profiles venv 处置不同——本机系统解释器即具备 pytest，probe 实测，永不凭印象）。
- Git: **available** — probe: `git --version` → `git 2.43.5` @ 2026-10-30；affected: T014（diff 审计）、T008（基线比对）。
- 分发工具链: **available** — probe: `python3 scripts/python/sync-mirrors.py --check` → 退出码 0 @ 2026-10-30（本机系统解释器可直接运行，无 077 记录的 `httpx` 缺失问题）；affected: T008、T012。基线六对全 ok 的原始输出见 `test-evidence/plan-sync-mirrors-baseline.txt`。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 `[P]` 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US4]`；故事相位每行必有且仅有一个，Setup / Polish 行禁止出现。
- **[blockedBy: T002]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **[green: <contract>#<clause>]**: 本行是把该条款转绿的那一行；标签面定义归 `.specify/templates/tasks-template.md` § Format，机器校验归 `scripts/python/validate-tasks.py`，合同路径相对本文件目录解析。认领分区见 § Clause Partition，同一行内多条款按序递增书写。
- 每行给出具体文件路径与可执行验收；测试行写明它写入的证据槽，实现行写明它让哪一组断言转绿。

## Measured Premises（2026-10-30 生成时实测，HEAD `5a4dc5a4`，分支 `078-bilingual-expression`）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/078-bilingual-expression/requirements.md` | `18` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/078-bilingual-expression/requirements.md` | `5` |
| 用户故事数 | `grep -cE '^### User Story' .specify/specs/078-bilingual-expression/requirements.md` | `4` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/078-bilingual-expression/requirements.md` | `3` |
| 契约文件数 | `ls .specify/specs/078-bilingual-expression/contracts/*.md \| wc -l` | `4` |
| 契约条款定义 | `python3 scripts/python/clause_extract.py .specify/specs/078-bilingual-expression/contracts/*.md \| grep -c '^  C-'` | `35`（owner-document 9 + checker 12 + distribution 6 + measurement 8） |
| 条款计数陷阱形 | `grep -oh 'C-[0-9]\{2,3\}' .specify/specs/078-bilingual-expression/contracts/*.md \| wc -l` | `71` — 这是条款 id 的*提及*数（条款内互引与 [[STR]] 引用），不是定义数；单位是条款*定义*时正确答案是 `35`。两数并记，表明测量是有意取的而非碰巧 |
| 五个交付物路径不在树 | `ls shared/guidelines/bilingual-expression.md scripts/python/bilingual-expression-check.py tests/contract/test_bilingual_expression.py tests/fixtures/bilingual .specify/specs/078-bilingual-expression/notes` | 五行 `No such file or directory`（T003 / T007 / T002 创建；`notes/` 由 T001 创建；红先行起点即此实测红） |
| 生成器输入模板 | `grep -n 'TEMPLATE_FILE=' scripts/bash/generate-instructions.sh` | `TEMPLATE_FILE=".specify/templates/instructions-template.md"` — 生成器读运行时镜像，故 T012 刷新必须排在 T008 镜像同步之后（相位序已按此排列） |
| ambient 插入位置锚点 | `grep -n '^## Grounded Naming' templates/instructions-template.md` | 在场（plan Assumptions P2 登记插于其后的唯一锚点） |
| 确认门基线 | `tail -3 .specify/specs/078-bilingual-expression/test-evidence/plan-scan-confirmation-gates.txt` | blocking 27 / violations 0（T006 与 T012 的判据基线，原始输出留档于该文件） |
| 镜像基线 | `tail -2 .specify/specs/078-bilingual-expression/test-evidence/plan-sync-mirrors-baseline.txt` | 六对全 ok（2026-10-30 实测），T008 的「无新增漂移」判据基线 |
| coverage 基线 | `head -2 .specify/specs/078-bilingual-expression/coverage-baseline.txt` | plan 期已冻结（35 条 078 条款为 plan 期设计内红，本阶段认领后 beyond baseline 归零；不重冻结） |
| 任务行预算 | `grep -cE '^- \[ \] T[0-9]{3}' .specify/specs/078-bilingual-expression/tasks.md` | `19`（T001–T019）≤ 40 上限（`decomposition-check.py` 的 `TASK_CEILING = 40`） |
| 任务行预算陷阱形 | `grep -oE 'T[0-9]{3}' .specify/specs/078-bilingual-expression/tasks.md \| wc -l` | 远大于 19——这是任务标识的*提及*数（`[blockedBy:]`、认领表、覆盖表都在引用），不是定义数；单位是任务*行*时用行首锚定 `^- \[ \] T` 取数 |

## Clause Partition

35 条条款、4 份契约文件，每条款恰被一行认领，同文件内条款序随行序递增。认领的引擎是 `account-clause-coverage.py`（claimed 计数必须等于 35），本表只是声明。

| Contract file | Clauses | Claimed by | 行内条款带 |
|---|---|---|---|
| `contracts/owner-document.md` | C-001…C-009 | T003 | C-001…C-009 |
| `contracts/checker.md` | C-001…C-012 | T007 | C-001…C-012 |
| `contracts/distribution.md` | C-001…C-006 | T008 | C-001、C-002 |
| `contracts/distribution.md` | — | T012 | C-003…C-005 |
| `contracts/distribution.md` | — | T017 | C-006 |
| `contracts/measurement.md` | C-001…C-008 | T009 | C-001、C-002 |
| `contracts/measurement.md` | — | T010 | C-003 |
| `contracts/measurement.md` | — | T011 | C-004 |
| `contracts/measurement.md` | — | T013 | C-005 |
| `contracts/measurement.md` | — | T014 | C-006 |
| `contracts/measurement.md` | — | T015 | C-007 |
| `contracts/measurement.md` | — | T016 | C-008 |

**Partition check**: 9 + 12 + 6 + 8 = 35；12 个认领行，无条款落在两行，无行认领其相位之后才能转绿的条款带。distribution 的 C-003/C-004 虽在 T006（ambient 落笔）即事实转绿，但认领按执行-验证行 T012 归属（该行重跑模板侧中立性断言与确认门计数），以保持同文件条款序随行序递增（机器校验 `green-cross-phase`）——这是认领归属的声明，不是跳过验证。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T003 | FR-010 | T007 |
| FR-002 | T003, T007 | FR-011 | T012, T013 |
| FR-003 | T003, T007 | FR-012 | T006, T012 |
| FR-004 | T003, T007 | FR-013 | T003 |
| FR-005 | T003, T004, T015 | FR-014 | T017 |
| FR-006 | T003, T010 | FR-015 | T019 |
| FR-007 | T003, T007 | FR-016 | T010 |
| FR-008 | T006, T012 | FR-017 | T019 |
| FR-009 | T007 | FR-018 | T016 |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T009 |
| SC-002 | T010, T011 |
| SC-003 | T013 |
| SC-004 | T014 |
| SC-005 | T015（真实词汇表实跑归 review） |

**流程行**: T001（证据槽）、T018（quickstart 实跑取证）、T019（收尾门禁与 Feature 复核）为流程/取证行——T018 不认领契约条款但服务 SC-002/SC-003/SC-005 的复现，T019 承接 FR-015/FR-017 的零新增与登记复核。其余实现行各至少映射一条 FR 或 SC。

## Mirror Obligations

镜像对清单的属主是 `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`（六对）；范围登记见 `plan.md` § Mirror Obligations（本特性触碰 shared / templates / scripts 三对，命令副本面零触碰），本文件不复述其行内容。**T008 是唯一的同步与验证行**（`--write` 后 `--check`，逐对陈述相对 `test-evidence/plan-sync-mirrors-baseline.txt` 无新增漂移）；T012 的 instructions 刷新消费 T008 产出的 templates 镜像（生成器输入路径实测见 § Measured Premises），`.specify/instructions.md` 与根 `AGENTS.md` 由 `generate-instructions.sh` 产出、MUST NOT 手改；`tests/**` 与 `.specify/specs/078-bilingual-expression/**` 无任何镜像义务；`regen-command-copies.py --check` 相对基线无新增漂移（本特性不触碰 `templates/commands/**`）。

## Test Budget

- **本阶段（tasks）不运行任何测试套件**（docs-only 预算）：五个确定性门（`validate-tasks` / `pre-analyze-check --stage tasks` / `account-clause-coverage` / `decomposition-check --mode tasks` / `doc-consistency-check --faces evidence`）的输出留档 `test-evidence/tasks-*.txt`，全部测试断言留待实现阶段。
- **实现期基线（恰好一次）**: 实现开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获失败名基线；本文件任何行不得重捕获或刷新。
- **闭环节点**: review 之后由驱动者跑一次全量并按名比较；本特性任何行不得预支。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建好证据槽，红先行日志与测量前提都有固定落点

- [ ] T001 建立本特性证据槽并冻结实测前提：新建 `.specify/specs/078-bilingual-expression/notes/red-first-evidence.md`（头部点名 `tests/contract/test_bilingual_expression.py` 一个文件，并规定红先行记录四个字段——重放命令 / 真实输出 / 退出码 / 失败计数）、`notes/pre-change-measurements.md`（逐条粘贴本文件 § Measured Premises 的实测值与命令，带日期 2026-10-30）、`notes/quickstart-run.md`（头部列 S1–S8 八个场景及各自判据，真实输出留实现期粘贴）

**Checkpoint**: 证据槽就位；本特性无阻断全部故事的前置，故无 Foundational 相位。

---

## Phase 2: User Story 1 - 框架作者在核心概念的定义处写出双语形态，读者跨 context / 跨模型读到一致的语义锚点 (Priority: P1) 🎯 MVP

**Goal**: 让双语表述约定成文为唯一 owner 文档 [[STR-001]]：六组事实（方向规则、唯一形态、覆盖定义面封闭集、豁免面封闭集、一致性规则、迁移边界）+ 「定义处」可判定信号 S1…S4，任何作者按它即可自判一处定义行是否必须双语、形态是否合规。

**Independent Test**: 取任一 `shared/definitions/` 概念条目做改写演练（quickstart S1 的四步核对），owner 文档结构契约腿（章节树、owner 声明、四组枚举列表形态、信号清单、逐字形态与正则登记行）全绿即证明约定可执行、可教学。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写测试，确认它们失败，再实现**

- [ ] T002 [US1] 红先行编写 `tests/contract/test_bilingual_expression.py`（一次写全各腿，后续实现行只让对应腿转绿）并随测试建立夹具 `tests/fixtures/bilingual/compliant-definition.md`（zh 主语言、含 S3 加粗定义行的合规形态）、`tests/fixtures/bilingual/fullwidth-definition.md`（全角违规行）、`tests/fixtures/bilingual/same-language-definition.md`（en 主语言、括号内仍为英文的同向违规行）：腿清单 = owner 文档结构腿（plan Chapter Tree 九章逐字在场、头部 owner 声明逐字点名六组事实、`**Readers**`/`**Reading scenario**` 两行非空、四组枚举各为 `- ` 引导列表、S1…S4 信号清单、[[STR-002]]/[[STR-003]] 逐字形态与形态判定正则唯一登记行）、scan 夹具三腿（quickstart S2：`test_scan_compliant_fixture` 退出码 0 无 finding、`test_scan_fullwidth_fixture_red` 退出码 1 且 `file:line [full-width-parens]` 定位、`test_scan_same_language_fixture_red` 退出码 1 且码 `same-language-bracket`）、coverage 腿（S3：`test_coverage_action`，`coverage` 不接受 `--path`、覆盖面清单只读 owner 文档不内嵌副本）、census 腿（S8：`test_census_action`，复用词汇表表解析、中文侧逐字比对）、SC-001 关键词快照腿（S7：`test_sc001_keyword_snapshot`，关键词表由 owner 文档四组枚举程序派生不手写）、漂移守卫三腿（distribution C-006：(i) [[STR-001]]/[[STR-002]]/[[STR-003]] 三字字面量的唯一消费点；(ii) 镜像三面与框架源逐字一致、清单派生自 `sync-mirrors.py` 的 `MIRROR_PAIRS` 不硬编码；(iii) ambient 小节「摘要 + 指针」形态、四组枚举关键词在小节内零命中）、确定性抽样腿（measurement C-004：从检查器模块导入的行选择辅助 `sample_lines`，每隔 k 行取 1、k=⌈n/10⌉，钉其确定性）；在未改动树上跑出记录在案的失败运行（五个交付物路径不在树，实测见 § Measured Premises），四字段写入 `notes/red-first-evidence.md`

### Implementation for User Story 1

- [ ] T003 [US1] [blockedBy: T002] 落文 owner 文档 `shared/guidelines/bilingual-expression.md`：严格按 plan § Document Structure 的 Chapter Tree 九章（头部与 owner 声明 / 定义处与可判定信号 / 方向规则与唯一形态 / 覆盖定义面（封闭集）/ 豁免面（封闭集）/ 一致性与词汇表 / 迁移边界与存量差异 / 与相邻纪律的交界 / 检查器与守卫）；头部（前 40 非空行内）声明本文件是唯一 owner 并逐字点名六组事实，含非空 `**Readers**`/`**Reading scenario**` 两行（复用全局基准读者，不新建）；四组枚举（方向规则 / 覆盖定义面 / 豁免面 / 唯一形态字面量条款）各以 `- ` 列表成文；S1…S4 信号清单（S1 词汇表表体行、S2 章节标题行、S3 加粗引导定义行、S4 主语言声明行与 CJK/拉丁占比保守缺省）并声明「首次定义」语义判断不在机械范围；[[STR-002]]/[[STR-003]] 逐字形态与检查器形态正则的唯一登记行；混合主语言文档的判定信号与保守缺省；与 jargon 白名单、One Source Of Truth 的交界只给指针不重述；迁移边界声明「首次定义处仍需双语」并指针到 E6 不承载清单；检查器与守卫节只指针 `contracts/checker.md`；owner 文档结构腿全绿（测试文件见 T002） [green: contracts/owner-document.md#C-001] [green: contracts/owner-document.md#C-002] [green: contracts/owner-document.md#C-003] [green: contracts/owner-document.md#C-004] [green: contracts/owner-document.md#C-005] [green: contracts/owner-document.md#C-006] [green: contracts/owner-document.md#C-007] [green: contracts/owner-document.md#C-008] [green: contracts/owner-document.md#C-009]

**Checkpoint**: US1 独立可验——owner 文档在场、结构契约腿全绿；取任一概念条目按四步核对可自判合规（quickstart S1）。

---

## Phase 3: User Story 2 - 词汇表维护者登记新术语时，Canonical 直接采用双语形态 (Priority: P1)

**Goal**: 让 FR-005 的一致性判定可操作：A5 双语 Canonical 形态的登记演练跑通，census 的分母（词汇表全部双语 Canonical 词条）被程序枚举并冻结为 dated record，成为 SC-005 的测量输入。

**Independent Test**: 在临时根复制词汇表、登记一个虚构双语词条并用 owner 文档 § 一致性与词汇表 的判定规则核对「第二处定义与 Canonical 逐字一致」（requirements US2 验收场景的演练），输出留档、真词汇表零修改。

### Implementation for User Story 2

- [ ] T004 [P] [US2] [blockedBy: T003] FR-005 判定演练（受认可临时根 `.specify/.tmp/` 或 `mktemp -d`，不改真词汇表）：复制 `.specify/memory/glossary.md` 到临时根，按 A5 登记一个虚构词条（Canonical 取 `中文(English)` 双语形态、Variants 收集中文侧易混写、Origin/Status 按 `shared/workflow/glossary.md` 协议字段），随后用 owner 文档 § 一致性与词汇表 的判定规则演练两处定义的中文侧逐字一致性核对（一处一致、一处构造不一致并记录判定结果）；命令、真实输出、判定结论与拆卸步骤写入 `test-evidence/us2-glossary-drill.txt`；真词汇表 `.specify/memory/glossary.md` 保持零修改（SC-004 白名单外零改动）
- [ ] T005 [P] [US2] [blockedBy: T003] census 分母冻结：以 `scripts/python/glossary-utils.py` 的表解析模式（读取模式复用，不改其行为）程序枚举 `.specify/memory/glossary.md` 全部双语 Canonical 词条（Canonical 含半角括号双语形态的条目），输出词条清单 + 总数 + as-of 日期到 `test-evidence/us2-census-denominator.txt`（dated record，一文一件）；数值与 requirements 现状锚点 M-7（132/161）并记，差异即上报不静默采用；只读，真词汇表零修改

**Checkpoint**: US2 独立可验——演练判定流程跑通且留档，census 分母清单冻结（程序枚举，非手工计数）；两处证据均显示真词汇表零修改。

---

## Phase 4: User Story 3 - 下游项目经 `specify init` 获得约定的 ambient 摘要与指针 (Priority: P2)

**Goal**: 让约定的分发面成文：`templates/instructions-template.md` 新增 `## Bilingual Expression (双语表述)` ambient 小节（一句话摘要 + owner 路径指针），标题自身即约定的首个示范实例；模板中立性与确认门预算在本行自验，管道级实测（SC-003）在 Polish 的 T012/T013 收口。

**Independent Test**: 模板侧断言——小节标题逐字在场、四组枚举关键词在小节内零命中、无本仓专属路径或提交号、无阻断式确认句，且 `scan-confirmation-gates.py --summary` 的 blocking 计数 == 27 基线（requirements US3 验收场景的模板侧形态）。

### Implementation for User Story 3

- [ ] T006 [US3] 在 `templates/instructions-template.md` 的 `## Grounded Naming` 小节之后（plan Assumptions P2 的唯一锚点，不改动其他小节的文字）插入 `## Bilingual Expression (双语表述)` 小节：一句话摘要 + [[STR-001]] 框架源相对路径指针（零枚举复述、零本仓专属路径/提交号、零阻断式确认句），形态对照既有 `## One Source Of Truth` 小节惯例；本行自验并留档 `test-evidence/us3-ambient-template-check.txt`：① 小节标题逐字在场（grep 计数 = 1）；② 四组枚举关键词（派生自 T003 落文的 owner 文档列表项字面量）在小节内零命中；③ 本仓专属路径模式（`.specify/` 绝对路径形态、提交号形态）在小节内零命中；④ `python3 scripts/python/scan-confirmation-gates.py --summary` 的 blocking 计数 == 27（基线 `test-evidence/plan-scan-confirmation-gates.txt`）；本行不携带 `[green:]` 认领——distribution C-003/C-004 的认领归 T012（该行重跑同组断言并消费刷新产物，认领序与条款序保持一致，理由见 § Clause Partition 末段）

**Checkpoint**: US3 模板侧独立可验——ambient 小节在场且四组断言全过；下游生成管道实测（quickstart S4）在 T012/T013 完成，不阻塞本相位的模板侧结论。

---

## Phase 5: User Story 4 - 维护者运行确定性检查器，机械校验定义行形态与覆盖面 (Priority: P2)

**Goal**: 让机械守卫可用：`scripts/python/bilingual-expression-check.py` 三动作（scan / coverage / census）、退出码 0/1/2、finding 码封闭四值，只做契约钉死的三类机械判定，不判语义、不接线门禁、不并入 `doc-consistency-check.py`。

**Independent Test**: quickstart S2/S3/S8 三场景在夹具与受控语料上可红可绿（T002 已钉期望），本行让全部检查器腿转绿；构造一条全角违规行必报 `full-width-parens` 并定位行号。

### Implementation for User Story 4

- [ ] T007 [US4] [blockedBy: T002,T003] 实现 `scripts/python/bilingual-expression-check.py`（框架源；单文件、仅标准库、只读扫描、无第三方依赖）：三动作 CLI——`scan --path <file|dir> [--scope full|changed] [--json]`、`coverage`、`census`（coverage/census 不接受 `--path`，范围取 owner 文档覆盖面清单，脚本只读取不内嵌清单副本）；所有动作打印 JSON 摘要（`--json` 纯 JSON），finding 明细逐行 `file:line [code] message`；退出码封闭三段 0/1/2（无 findings / 有 findings / 用法错误），语义不随 finding 数量改变；不绑定任何阶段门禁算子；`scan` 跳过围栏代码块（``` / ~~~，按行线性跟踪、围栏任意列）与行内代码 span 内部，链接目标与图片语法的括号段同样豁免；`scan` 只判 S1…S4 信号行（S4 只用于主语言判定不单独产 finding）；判定 (a) 信号行缺半角紧贴双语形态 → `missing-bilingual`，形态常量逐字取 owner 文档 C-005 登记行；(b) 括号内词条脚本类与括号外相反 → `same-language-bracket`，主语言取 S4（声明优先、缺省 CJK/拉丁占比高者）；(c) `coverage` 核验覆盖面清单每面存在且非空、整面缺失 → `coverage-missing` 并输出缺失项清单；全角紧贴形态 → `full-width-parens`，码集封闭四值；`--scope changed` 只判调用方传入的改动路径并集（`git diff --name-only <base>..HEAD` ∪ `git status --porcelain`），`--scope full` 产出 E6 存量差异清单（dated record，append-only）；`census` 复用 `glossary-utils.py` 表解析模式读取 `.specify/memory/glossary.md` 全部双语 Canonical 词条，对覆盖面清单全量比对中文侧逐字一致、100% census 无抽样；MUST NOT 判语义、LLM MUST NOT 参与匹配计数；模块级暴露确定性行选择辅助 `sample_lines(lines)`（每隔 k 行取 1，k=⌈n/10⌉）供 review 面抽样（T011 消费、T002 已钉）；检查器全部测试腿转绿（测试文件与夹具见 T002） [green: contracts/checker.md#C-001] [green: contracts/checker.md#C-002] [green: contracts/checker.md#C-003] [green: contracts/checker.md#C-004] [green: contracts/checker.md#C-005] [green: contracts/checker.md#C-006] [green: contracts/checker.md#C-007] [green: contracts/checker.md#C-008] [green: contracts/checker.md#C-009] [green: contracts/checker.md#C-010] [green: contracts/checker.md#C-011] [green: contracts/checker.md#C-012]

**Checkpoint**: US4 独立可验——三动作在夹具上红绿可判（S2 两例违规各命中具名码与行号定位、合规例退出 0），coverage/census 行为符合契约，码集封闭四值。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: SC 采证、分发收口、漂移守卫、实跑留档与零新增机制复核

- [ ] T008 镜像同步与验证（唯一同步与验证行）：`python3 scripts/python/sync-mirrors.py --write` 产出全部 `.specify/` 副本（shared / templates / scripts 三对本特性触碰），再 `--check` 对六对逐对陈述相对 `test-evidence/plan-sync-mirrors-baseline.txt` 无新增漂移；`shared/guidelines/bilingual-expression.md`、`.specify/templates/instructions-template.md`、`scripts/python/bilingual-expression-check.py` 三件的镜像文件存在且与框架源逐字一致（不断言手改）；`.specify/` MUST NOT 手改；输出写入 `test-evidence/us8-distribution-after.txt` [green: contracts/distribution.md#C-001] [green: contracts/distribution.md#C-002]
- [ ] T009 [blockedBy: T003] SC-001 复制位置数 = 0 采证：程序派生关键词表（读取 owner 文档四组枚举的 `- ` 列表项取字面量，MUST NOT 手写）并在 `shared/`、`templates/`、`.specify/`（排除 `.specify/specs/` 与 `.specify/history/`）检索；命中行排除 (i) owner 文档自身（框架源与 `.specify/shared/` 镜像两路径）与 (ii) 含 [[STR-001]] 指针的「路径 + 锚」引用行后计数，期望 0；逐关键词命中清单与判定输出冻结为交付日快照（E7）写入 `test-evidence/us9-sc001-keyword-snapshot.txt`（review 阶段复用同一快照判定） [green: contracts/measurement.md#C-001] [green: contracts/measurement.md#C-002]
- [ ] T010 [blockedBy: T007,T008] SC-002 新写内容合规率采证与 E6 存量清单：`python3 scripts/python/bilingual-expression-check.py --action scan --scope changed --json`，输入 = 本特性全部提交相对 stage base `5a4dc5a4` 的改动路径并集（`git diff --name-only 5a4dc5a4..HEAD` ∪ `git status --porcelain`），分母 = 改动路径上的信号行数、分子 = 零 finding 的信号行，期望合规率 100%；同轮跑 `--scope full` 产出存量差异全量清单（E6，dated record）写入 `test-evidence/us10-sc002-changed-scope.txt` 与 `test-evidence/us10-e6-legacy-divergence.txt`（存量只清单化不批量改写，FR-016） [green: contracts/measurement.md#C-003]
- [ ] T011 [blockedBy: T010] review 面确定性抽样交付（measurement C-004 的 implement 侧）：对 T010 `--scope changed --json` 输出的信号行清单调用检查器模块的 `sample_lines`（每隔 k 行取 1，k=⌈n/10⌉；行数 < 10 时全量），把抽样行清单、参数与真实输出写入 `test-evidence/us11-review-sample.txt`，作为 review 阶段抽样复核的输入 artifact（复核分歧登记归 review 产物）；抽样选择由程序给出，MUST NOT 由评审自选 [green: contracts/measurement.md#C-004]
- [ ] T012 [blockedBy: T006,T008] instructions 刷新与 ambient 两态复核：`bash scripts/bash/generate-instructions.sh` 刷新 `.specify/instructions.md` 与根 `AGENTS.md`（生成器输入为 `.specify/templates/` 镜像，故排在 T008 之后；两文件 MUST NOT 手改），捕获生成器 size report 原始输出到 `test-evidence/us12-instructions-refresh.txt`（模板 27,940 B / live 32,259 B 为 R-5 基线，超预算只报 warning 但报告必须留档）；重跑 T006 的同组断言于刷新产物：`.specify/instructions.md` 含逐字 `## Bilingual Expression (双语表述)` 小节、小节内四组枚举关键词零命中、含 [[STR-001]] 指针；再跑 `scan-confirmation-gates.py --summary` 确认 blocking 计数 == 27 [green: contracts/distribution.md#C-003] [green: contracts/distribution.md#C-004] [green: contracts/distribution.md#C-005]
- [ ] T013 [blockedBy: T012] SC-003 下游生成管道实测（implement 期一次）：在受认可临时根（`.specify/.tmp/` 或 `mktemp -d`）按 quickstart S4 的管道构造下游树（`.specify/templates/instructions-template.md` 与 `.specify/scripts/` 载荷），以框架源脚本绝对路径运行 `generate-instructions.sh`，断言产物含逐字 ambient 小节标题、小节内四组枚举关键词零命中且含 [[STR-001]] 指针（「摘要 + 指针」形态）；命令、真实输出、产物检查结果与拆卸步骤写入 `test-evidence/us13-sc003-pilot.txt`（pilot 必须拆除） [green: contracts/measurement.md#C-005]
- [ ] T014 SC-004 追溯重写 = 0 审计：`git diff --stat 5a4dc5a4..HEAD` 全量文件清单对照白名单——允许改动：[[STR-001]]（框架源 + 镜像）、`templates/instructions-template.md`（+ 镜像与生成产物 `.specify/instructions.md`、根 `AGENTS.md`）、检查器与其镜像、契约测试与夹具、登记文件（`features.md`、`features/078.md`、`register.md`）、规格产物（`.specify/specs/078-bilingual-expression/`）；白名单外既有文档的修改行数必须为 0；原始输出与逐文件判定写入 `test-evidence/us14-sc004-diff-audit.txt` [green: contracts/measurement.md#C-006]
- [ ] T015 [blockedBy: T007] 受控语料 census 端到端采证（SC-005 的 implement 侧）：在临时根构造受控语料（复制 owner 文档覆盖面清单所指的定义面样本 + T004 演练词汇表），运行 `--action census`，断言退出码 0（受控语料内不一致处数 0）且中文侧比对逐字执行；真实词汇表的 census 实跑归 review 阶段（quickstart S8），本行不预支；命令、真实输出与拆卸写入 `test-evidence/us15-census-controlled.txt` [green: contracts/measurement.md#C-007]
- [ ] T016 [blockedBy: T003,T007] ID 登记完整性复核：核对 `.specify/memory/register.md` 的 078 登记行（T-001…T-004、078-C-clauses 命名空间行，plan 期已 coin）指针形态合规（编号 → 一行含义 → 权威路径 → 状态，MUST NOT 复述决策正文），且本特性新产出未 coin 任何未登记 durable identifier；核对结果写入 `test-evidence/us16-register-check.txt` [green: contracts/measurement.md#C-008]
- [ ] T017 [blockedBy: T003,T006,T007,T008,T012] 漂移守卫全绿确认：`python3 -m pytest tests/contract/test_bilingual_expression.py -q` 全绿，逐腿确认漂移守卫三腿(i/ii/iii)转绿——[[STR-001]]/[[STR-002]]/[[STR-003]] 唯一消费点、镜像三面逐字一致（清单派生自 `MIRROR_PAIRS`）、ambient「摘要 + 指针」形态；原始输出写入 `test-evidence/us17-drift-guard-green.txt` [green: contracts/distribution.md#C-006]
- [ ] T018 实跑 `quickstart.md` 的 S1–S8 八个场景（S1 四步核对 / S2 三例判定 / S3 覆盖面 / S4 下游生成 / S5 镜像漂移 / S6 结构面 / S7 关键词扫描 / S8 census），把每条命令的真实输出与拆卸步骤贴入 `.specify/specs/078-bilingual-expression/notes/quickstart-run.md`；S4/S8 的临时目录必须清除，`git status --ignored` 不得把它们当新增；不改写 plan 属主的 `quickstart.md`
- [ ] T019 收尾门禁留档与 Feature 复核：把 `validate-tasks.py`、`decomposition-check.py --mode tasks`、`pre-analyze-check.py --stage tasks`、`account-clause-coverage.py`、`doc-consistency-check.py --faces evidence` 五条命令的真实输出写入 `test-evidence/tasks-*.txt`；按 Feature Integration Protocol 复核 Feature 列表——本任务拆解未暴露新 Feature、未使既有 Feature 失效，`.specify/memory/features.md` 的 078 行保持 `Planned` 不改；复核「零新命令 / 零运行时 / 零第三方依赖」前后集合差；并只为本特性产物建立提交（不 push，不夹带既有脏文件）

**Checkpoint**: 全部 SC 有 implement 期采证；镜像与生成产物收口；漂移守卫全绿；八场景实跑有据。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始。
- **US1 (Phase 2)**: 依赖 Setup 的证据槽（T002 写 `notes/red-first-evidence.md`）；本特性 MVP。
- **US2 (Phase 3)**: 依赖 US1 的 owner 文档（演练与分母冻结都读其 § 一致性与词汇表）。
- **US3 (Phase 4)**: 无写集依赖（只改 `templates/instructions-template.md`），按故事优先级排在 US2 之后；管道级实测依赖 Polish 的同步与刷新（T008/T012/T013）。
- **US4 (Phase 5)**: 依赖 US1 的 owner 文档（覆盖面清单、形态常量、信号清单的唯一登记处）与 T002 的测试文件。
- **Polish (Phase 6)**: 依赖 US1–US4 全部源改动完成（T008 镜像同步必须最后跑；T012 刷新依赖 T008 的 templates 镜像，实测前提见 § Measured Premises）。

### User Story Dependencies

- **US1 (P1)**: 无跨故事依赖——owner 文档自成闭环，MVP 即它（US2 是验证演练不增产品面，US1 单独交付即可独立验收）。
- **US2 (P1)**: 消费 US1 的 owner 文档规则；与 US3 写集不相交。
- **US3 (P2)**: 只改模板文件，与 US2/US4 无写集交集；生成管道实测的依赖在 Polish 收口。
- **US4 (P2)**: 消费 US1 的 owner 文档（清单与常量）与 T002 的测试/夹具。

### Within Each User Story

- 测试先行（T002 一次写全），且必须先在未改动树上跑出记录在案的失败
- 同一文件的多行按 `[blockedBy:]` 串行；条款认领随行序递增
- 实现行让对应测试腿转绿后才进入下一行

### Parallel Opportunities

- T004 与 T005 为仅有的 `[P]` 对：写目标分别是 `test-evidence/us2-glossary-drill.txt` 与 `test-evidence/us2-census-denominator.txt`，无依赖交集（都只读词汇表与 owner 文档）。
- 无其它行级并行：单一红先行日志、单一检查器文件、单一同步行都是天然串行点；故事层 US2 与 US3 写集不相交，多 agent 下可同时开工，但本线按相位序执行。

---

## Parallel Example: Within US2 only

```bash
# T004 与 T005 可并行（不同写目标，共同前置 T003）：
Task: "FR-005 判定演练（test-evidence/us2-glossary-drill.txt）"
Task: "census 分母冻结（test-evidence/us2-census-denominator.txt）"

# 其余全部按 T001 → US1 → US2 → US3 → US4 → Polish 顺序执行
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = US1（owner 文档）**。模板 MVP 规则：多个 P1 故事只有合起来才构成可独立验收的增量时 MVP 才覆盖全部 P1——本线 US2 是对 owner 文档规则的验证演练（不产生新产品面），US1 单独交付即「约定成文、可自判合规」的完整增量，故 MVP = US1。US3/US4 为 P2，按序跟进。

1. 完成 Phase 1：证据槽
2. 完成 US1（T002–T003）→ **STOP and VALIDATE**：owner 文档结构腿全绿，四步核对演练可自判（quickstart S1）
3. 完成 US2（T004–T005）→ **STOP and VALIDATE**：演练判定与分母冻结留档，真词汇表零修改
4. 完成 US3（T006）→ 模板侧断言留档
5. 完成 US4（T007）→ 三动作红绿可判
6. Polish（T008–T019）收口

### Incremental Delivery

1. US1 → 双语约定第一次有成文的唯一 owner，作者可自判
2. US2 → FR-005 一致性判定第一次可操作、可测量
3. US3 → 分发面（ambient 摘要 + 指针）第一次成文
4. US4 → 机械守卫第一次可红可绿（三类机械判定 + 四值码）
5. Polish → SC 采证、镜像收口、漂移守卫与实跑证据

---

## Notes

- `[green:]` 认领的是「把该条款转绿的那一行」；认领分区由 `account-clause-coverage.py` 计数（必须等于 35），WARN 不靠删标签消音。
- 红先行记录必须含四个字段（重放命令、真实输出、退出码、失败计数）；只写「已执行」不算记录。
- distribution 的 C-003/C-004 在 T006 落笔即事实转绿，但认领归 T012（重跑同组断言的消费行），以保证同文件条款序随行序递增——见 § Clause Partition 末段。
- SC-002 的 review 面抽样复核与 SC-005 的真实词汇表 census 归 review 阶段；implement 期交付程序（`sample_lines`、census 动作）与受控语料证据，不预支 review 结论。
- 每个检查点的判定只看退出码、标签计数与差异行枚举，不靠阅读正文。
- **Deferral discipline**: 无法在本轮运行的行标 `[~]` 并在 `verification.md` 记 `deferred_tasks=`，不留 `[ ]` 挂着。
