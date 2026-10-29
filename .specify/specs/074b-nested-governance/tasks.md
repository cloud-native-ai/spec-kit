# Tasks: 外层消费、概念扩散与兼容安全（Nested Consumption, Diffusion & Compatibility）— Feature 074 / Slice 074b

**Requirement ID**: 074b（Feature 074 的第二个切片；不新建 Feature ID、不新增注册行）
**Requirement Key**: `074b-nested-governance`
**Branch**: `074b-nested-governance`
**Related Feature**: 074 Goal/Team/Agent 与 SDD 开发流程统一（切片复用同一注册行；本阶段状态天花板 `Planned`）
**Input**: Design documents from `.specify/specs/074b-nested-governance/`
**Prerequisites**: plan.md（技术路线、Mirror Obligations、Structure Decision）、requirements.md（8 FR / 2 SC / 7 STR；Parent Mapping；D-1/D-2/D-3）、research.md（RB1–RB10）、data-model.md（E1–E8 / V-1…V-12 / 2 状态机）、contracts/ ×3（**30 条款**：`compat-and-safety.md` 12 / `diffusion.md` 8 / `report-and-attribution.md` 10）、quickstart.md（S1–S7）、feature-ref.md（交付面 9 行 = 3 新 + 6 改）

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 为测试强制原则。本切片交付面是 markdown owner 的就地编辑 + 三份新契约套件 + 一份既有套件的超集改动，属 doc-feature 形态：所请求的"测试"恰是**结构性契约测试**（对制品的内容 / 标题 / 字面量 / 镜像一致性断言），而非单元或集成运行时测试——这与 Principle IV 的契约驱动要求同向，不构成豁免。三份新套件一律红先：先跑出失败，把命令、真实输出、退出码写入 `notes/red-first-evidence.md`，再进入对应实现行。既有套件的超集改动（T017）按 migration/regression 例外处置——它守的是 `074a` 已交付的行为，只能先有行为后有测试，故不做红先。）

**Tests**: 红先证据的唯一落点是 `.specify/specs/074b-nested-governance/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。

**Organization**: 按用户故事组织——US1（外层消费并交接嵌套运行的结果，Priority P2 / 父 US4）、US2（SDD 概念扩散而不复制，Priority P3 / 父 US5）。两个故事在 `requirements.md` 中**不同优先级**，故 MVP = US1 单独（US2 的扩散面只有在 US1 的消费面存在后才产生价值——这是 requirements 的判定，不是本文件的重排）。Phase 4 是跨故事的兼容与安全面（本地 FR-006 / FR-007 / FR-008），不属任何一个用户故事的验收场景，故作为非故事阶段承载，行内零 `[US` 标记。Phase 5 Polish 收口镜像、结构面、回归、覆盖与登记。Foundational 阶段整段省略：本切片无阻塞性基础设施——五处编辑面各自只依赖已存在的 owner 文档与 `074a` 已交付的只读面，没有任何共享件先于用户故事落地。

## Definition of Done (DoD)

- DoD-1: 全部 26 行任务为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/074b-nested-governance/verification.md` 的 `deferred_tasks=`。
- DoD-2: 交付面按 `feature-ref.md` § 2 的 **9 行 = 3 新 + 6 改**落地——3 新 = `tests/contract/test_nested_run_report.py`、`tests/contract/test_sdd_diffusion.py`、`tests/contract/test_sdd_compat_containment.py`；6 改 = 5 个框架源文件（`skills/internal/create-team/SKILL.md`、`skills/internal/create-team/references/conceptual-model.md`、`skills/internal/run-agent/SKILL.md`、`templates/instructions-template.md`、`shared/guidelines/proactive-trigger.md`）+ 1 个既有测试文件（`tests/contract/test_sdd_invocation_governance.py`，超集方向）；加上由生成器产出的 `.specify/instructions.md`；零新增 `/speckit.*` 命令、零新增技能、零新增夹具（`tests/fixtures/nested_sdd.py` 原样复用）。
- DoD-3: 3 份契约共 30 条款（12 + 8 + 10）每条恰被一个任务行 `[green:]` 认领一次；`account-clause-coverage.py` 报告 `claimed clauses = 30`、`FR 8 / 8`、`uncovered beyond baseline = 0`；每个契约内认领顺序单调递增。
- DoD-4: 3 支新测试全绿；`tests/contract/test_sdd_invocation_governance.py` 改动后既有用例 propositions 不变（超集方向）；相对 T002 重采的名字级基线零**新增**失败 nodeid（既有红不修、不掩盖；名单与计数以 `test-evidence/targeted-set-v1-baseline.txt` 为唯一所有者，本文件不复述数字）。
- DoD-5: plan.md § Mirror Obligations 逐行落地——5 个被编辑源文件的 `.specify/` 投影 `cmp` 同字节；`sync-mirrors.py --check` 相对 T001 基线零新增差异；`regen-command-copies.py --check` 继续 `OK`（证明 `templates/commands/**` 零改动）；`generate-instructions.sh` 二次运行对 `.specify/instructions.md` 幂等；零手改镜像。
- DoD-6: 单一 owner 面成立——`## Nested SDD Runs` 段只在 `skills/internal/create-team/SKILL.md` § Report contract 落盘一次（`run-team` 继续按路径委派、零第二份陈述）；Stage 取值集逐字不变；SDD 阶段名册、分流输入集 / 取值域 / 裁决表 / 理由码词表、中性键取值一律只按路径抵达各自 owner；本切片零新增 registry、ledger、状态脊、ownership 模型、集成队列、确认门、调度器、守护进程或自动传输。
- DoD-7: `verification.md` 逐条列 `- **SC-001**` 与 `- **SC-002**` 的状态（只从 `.specify/templates/verification-log-template.md` 的封闭词表取值）、命令、输出摘要与证据指针；无来源的量记 `not-evaluated` + reason，不记 0、不记达成。
- DoD-8: 两项包含性声明按**用例 node-id 名字集**判定（post ⊇ pre 且共享 id 裁决不变），载体是 `test-evidence/compat-baseline-nodeids.txt` 的 7 个具名集合；**计数比较判不合规**——不得以条数或模块数替代。
- DoD-9: plan_constraint 全趟遵守——`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` 的任一改动只能是行级小修（错字 / 措辞 / 断链 / 格式 / 行级一致），逐项在 `verification.md` 声明 `PLAN-EDIT: <path> — <理由>；分类=minor`；任何实质性改动停线回抛，不静默重写。

**DoD Status**: green（`/speckit.implement` 收口时逐行测定，DoD-1…DoD-9 各自的实测面记录在 `verification.md` § DoD close 与 § Gates；无 void 行。父 074 的 `tasks.md` 仍留 57 行 `[ ]` 是父产物的切分前状态，已带实测披露在 Feature 074 记录中，不属本文件的 DoD 行）

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md` exit 0（0 error）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定并记录）。
- GATE-3: 分解规模合法 — check: `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/074b-nested-governance/requirements.md --tasks .specify/specs/074b-nested-governance/tasks.md` 结论为 `proceed`（task rows ≤ 40）。
- GATE-4: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance` 输出 `claimed clauses = 30`、`FR uncovered: 0`、`uncovered beyond baseline: 0`。
- GATE-5: 测试零新增失败 — check: `test-evidence/targeted-set-v1-baseline.txt` 记录的 19 文件定向套件 + 3 支新套件重跑后，失败 nodeid 排序与 T002 重采名单做 `comm -13` 为空（名字级，非计数级）。
- GATE-6: 镜像与副本零漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0，且与 `notes/pre-change-measurements.md` 的改前基线比较零新增差异。
- GATE-7: 零新增存储面 — check: `.specify/state/`、既有 line registry 目录与 `.specify/memory/` 的文件名集合，相对 `notes/pre-change-measurements.md` 的改前基线做 `comm -13` 为空。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/074b-nested-governance/tasks.md` 返回 0。
- GATE-9: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[12]\*\*' .specify/specs/074b-nested-governance/verification.md` 返回 2。

## Environment Prerequisites

<!-- 本节是环境判定的单一落点：任何任务行只引用本节，不复述结论。 -->

- pytest（`python3 -m pytest`）: **available** — probe: `python3 -m pytest --version` → `pytest 8.4.2`（平台 linux / Python 3.11.11）@ 2026-10-29；affected: T002、T004、T009、T010、T016、T019、T020、T023。
- git（`log` / `status` / `diff --stat` / `cmp` 所需的 HEAD 读取）: **available** — probe: `git rev-parse HEAD` → `ce9de5983`；`git status --short` 可读 @ 2026-10-29；affected: T001、T018、T021、T022、T024。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本切片全部检查为本地文件、`git` 与本地 pytest，无构建、无拉取、无网络、无守护进程 @ 2026-10-29；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本文件只有 Setup 的 T002 / T003 满足该条件（写目标分别是 `test-evidence/targeted-set-v1-baseline.txt` 与 `coverage-baseline.txt`）；用户故事内的红先行共用 `notes/red-first-evidence.md` 这一追加落点、三条转绿行共用 `notes/quickstart-run.md` 这一追加落点、T021 逐对核对时点名全部 5 个源文件、T024 点名 `.specify/state/` 与 `.specify/memory/` 两个目录——共享 sink 或共享点名面即同写目标，故这些段落零 `[P]`（按行序串行，不靠删路径消警）。
- **[Story]**: 用户故事标签（`[US1]` / `[US2]`），只出现在用户故事阶段的任务行；Setup / Compatibility & Safety / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**：绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析。**30 条款分区**：`compat-and-safety.md` C-1…C-2→T017、C-3…C-6→T018、C-7…C-12→T019；`diffusion.md` C-13…C-14→T011、C-15…C-17→T012、C-18→T013、C-19→T014、C-20→T015；`report-and-attribution.md` C-21…C-23→T005、C-24…C-26→T006、C-27…C-29→T007、C-30→T008。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `skills/internal/`、`templates/instructions-template.md`、`shared/guidelines/`、`tests/contract/`。
- **生成面（MUST NOT 手改）**: `.specify/instructions.md`（由 `scripts/bash/generate-instructions.sh` 生成）；`.specify/skills/`、`.specify/shared/`、`.specify/templates/`（`sync-mirrors.py` 投影）；每工具命令副本（`regen-command-copies.py` 生成，本切片零改动）。
- **证据落点（本切片）**: `.specify/specs/074b-nested-governance/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`、`test-evidence/targeted-set-v1-baseline.txt`、`test-evidence/compat-baseline-nodeids.txt`、`verification.md`。
- **禁改面**: `.specify/specs/074-goal-team-sdd-unification/**`（父 spec 与父设计，含其 `tasks.md`，只读）；`.specify/specs/074a-authorized-routing/**`（兄弟切片，已合入 master，只读）；`skills/external/sdd-loop-driver/**`、`shared/definitions/sdd-routing-definitions.md`、`scripts/python/sdd-route.py`、`shared/definitions/subagent-definitions.md`、`src/specify_cli/__init__.py`（四个前驱面与键集 owner，`feature-ref.md` § 2 明列为 not touched）；`agents/sdd-executor.agent.md`（叶子负向断言主体，只读）；`tests/fixtures/nested_sdd.py`（原样复用）；`templates/commands/**`；`.specify/memory/constitution.md`。
- **plan-owned 面（仅小修）**: `plan.md`、`data-model.md`、`contracts/**`、`quickstart.md`、`research.md`、`feature-ref.md`。

## Measured Premises (re-measured at generation time 2026-10-29, HEAD `ce9de5983`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' …/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **8 / 2 / 7** |
| 契约条款数（逐文件 + 合计） | `grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/074b-nested-governance/contracts/*.md`；合计 `grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md \| wc -l` | 12（compat-and-safety）/ 8（diffusion）/ 10（report-and-attribution）；合计 **30**，ids 连续 C-1…C-30。**陷阱形**：`grep -c 'C-'` 会把 `parent C-47` 一类来源标注一起算进去，计量单位是行首加粗的条款定义行 |
| 3 个新测试文件当前状态 | 逐个 `test -e` | 3/3 **ABSENT**（红先的前提） |
| 5 个编辑目标 + 叶子预设 + 复用夹具在位 | 逐个 `test -e` | 8/8 **OK**（`create-team/SKILL.md`、`create-team/references/conceptual-model.md`、`run-agent/SKILL.md`、`templates/instructions-template.md`、`shared/guidelines/proactive-trigger.md`、`tests/contract/test_sdd_invocation_governance.py`、`tests/fixtures/nested_sdd.py`、`agents/sdd-executor.agent.md`） |
| 叶子预设的 `sdd-invocation` 落盘处数 | `grep -c 'sdd-invocation' agents/sdd-executor.agent.md` | `0`。**陷阱形**：`grep -rn 'sdd-invocation' .` 会命中 074a/074b 设计文档里的说明文字，那是引用不是声明；计量单位是出厂预设定件 |
| 报告契约 owner 位点 | `grep -n '### Report contract' skills/internal/create-team/SKILL.md`；`grep -n 'Run Workspace, Reports' …` | `:53`（owner 段）/ `:49`（父段）；报告骨架块 `:57-63`。`run-team/SKILL.md:66` 仍按路径委派（零第二份陈述），且已携带 `"target_ref": "T-<nnn>"` |
| Stage bullet 位点 | `grep -n 'executor.*evaluator.*optimizer' skills/internal/create-team/references/conceptual-model.md` | `:10`（既有 Stage bullet，就地追加一句） |
| 编写基线位点 | `grep -n '^## Authoring Baseline' skills/internal/run-agent/SKILL.md` | `:171` |
| 触发纪律章节集 | `grep -c '^## ' shared/guidelines/proactive-trigger.md` | `10` 个 `## ` 段，`## Promotion & Safety Boundary` 起于 `:68`（交付的封闭集，本切片只在段内加一句，零新段） |
| 指令模板指针面当前落盘处数 | `grep -c 'sdd-routing\|sdd-invocation\|Nested SDD' templates/instructions-template.md` | `0`（模板与 live 均为 0，故指针面是新增而非改写） |
| 指令文件字节数（改前） | `wc -c templates/instructions-template.md .specify/instructions.md` | `34666` / `41948`——两文件都已超生成器 32,768 B 预算，故判据是**本节声明的字节上限 + 实测增量**，永不是"装得下预算" |
| 台账归因字段（既有） | `grep -n 'target_ref' skills/internal/create-team/references/summary-mapping.md` | `:100`（`target_ref`，局部形 `T-\d{3}`，缺省 = 归属 goal 整体）——本切片复用它，不新增字段 |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check` | exit 0；六对 `ok`：templates 22 / skills-external 406 / skills-internal 136 / agents 3 / scripts 114 / shared 59 |
| 命令副本基线 | `python3 scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.`，exit 0 |
| flow-class 基线 | `python3 .specify/scripts/python/flow-class-check.py --action check` | `79 unit(s) scanned, 0 finding(s)`；`coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0` |
| 包含性载体 | `awk` 按 `## S<n>` 段计 `^tests/` 行数；`grep -cE '^tests/[^ ]*::' …/compat-baseline-nodeids.txt` | **266 例 / 17 文件 / 7 集合**（S1 49、S2 25、S3 24、S4 40、S5 36、S6 54、S7 38），`stage_base=33269994a` |
| targeted-set-v1 基线（§ Test budget，不改） | `tail -5 test-evidence/targeted-set-v1-baseline.txt` | 19 文件 / `collected 290 items` / **1 failed, 289 passed**（34.27s），`rc=1`；唯一失败 `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`（gate total 27 vs 冻结 23），**既有红，不在本切片修复** |
| 条款覆盖改前状态 | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance` | `claimed clauses (this feature): 0`；`baseline: …/coverage-baseline.txt (0 names, MISSING)`；`FR claimed: 8 / uncovered: 0`；`status: baseline-missing`（exit 2）——本阶段冻结基线后必须转为 covered |
| 任务行数 | `grep -cE '^- \[[ xX>~]\] T[0-9]+' .specify/specs/074b-nested-governance/tasks.md` | **26**（< 40，无需分裂） |

## Test Budget Record (targeted-set-v1, `stage_base=tasks`)

**E3 stage-status row (targeted evidence)** — `stage=tasks`、`row_type=stage-status`、`status=ran`、`selection_basis=targeted-set-v1`（19 文件，`test-evidence/targeted-set-v1-baseline.txt`，本阶段**一次**重跑，无第二次全量）、`changed_paths[]=.specify/specs/074b-nested-governance/{tasks.md,coverage-baseline.txt,test-evidence/*}`、`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md`。运行六字段（命令 / 退出码 / 计数 / 用时 / 失败名集 / 基线指针）见该证据文件 § 4。

**Full-suite row (docs-only)** — `stage=tasks`、`row_type=stage-status`、`status=not-run-docs-only`、`selection_basis=no executable surface changed by this stage（本阶段只新增任务清单与证据 / 基线文件，未触碰任何被测试的 owner 或引擎）`、`changed_paths[]=.specify/specs/074b-nested-governance/** (markdown + txt only)`、`evidence_ptr=.specify/specs/074b-nested-governance/test-evidence/tasks-stage-checks.md`。运行六字段不适用，不记为 `unknown`。

## Requirement Coverage Map

| FR | 承载任务行 | SC | 承载任务行 |
|----|------------|----|------------|
| FR-001 | T006 | SC-001 | T018、T023 |
| FR-002 | T005、T007、T008 | SC-002 | T006、T009 |
| FR-003 | T011 | — | — |
| FR-004 | T012 | — | — |
| FR-005 | T013、T014、T015 | — | — |
| FR-006 | T017、T018 | — | — |
| FR-007 | T018、T019 | — | — |
| FR-008 | T019、T024 | — | — |

**SC-001 的判定面**：T018 交付 post ⊇ pre + 共享 id 裁决不变（7 集合 / 17 文件名字集）；T023 交付相对重采基线的零新增失败。二者合起来才是"变更后用例集为超集且每条变更前用例裁决不变"的完整读法——单看其一都是半个判据。
**SC-002 的判定面**：T006 落下"解析出的 Goal 字段集运行前后一致 + 归因只经既有台账引用"的义务文本；T009 用 `scripts/python/goal-utils.py` 的 `parse_goal` 在夹具 Goal 上实测字段集前后一致。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结后续"零新增"与"包含性"判据的全部对照物——改前测量、名字级测试基线、条款覆盖基线——使每一行判定都有可比较的落盘分母。

- [X] T001 捕获改前基线：创建 `.specify/specs/074b-nested-governance/notes/` 目录并写 `notes/pre-change-measurements.md`，逐项贴真实输出与捕获日期——`python3 scripts/python/sync-mirrors.py --check`（六对逐对）、`python3 scripts/python/regen-command-copies.py --check`、`git rev-parse HEAD`、`git status --short`、`wc -c templates/instructions-template.md .specify/instructions.md`、`grep -c 'sdd-invocation' agents/sdd-executor.agent.md`、`grep -n 'target_ref' skills/internal/create-team/references/summary-mapping.md`、`python3 .specify/scripts/python/flow-class-check.py --action check`，外加 9 行交付面的存在性普查（5 个编辑目标 + 1 个既有测试 + 1 个复用夹具 + 1 个叶子预设全部在位、3 个新测试文件全部缺位）与 `.specify/state/`、`.specify/memory/` 的当前文件名清单（GATE-7 的对照物）；本行不写任何产品文件。
- [X] T002 [P] 在实现起点按 never-cache 规则重采名字级测试基线：重跑 `.specify/specs/074b-nested-governance/test-evidence/targeted-set-v1-baseline.txt` 内记录的 19 个契约文件命令，把该文件的 `stage_base` / HEAD / 日期 / 命令 / 结果五行更新为本次真实值（该文件是这条 targeted-set-v1 基线的唯一所有者）；失败 nodeid 名单的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本行不复述比较形式，也不改选择理由行与"既有红"声明行。
- [X] T003 [P] 在本文件 30 条 `[green:]` 认领就位后冻结条款覆盖基线：`python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance --freeze > .specify/specs/074b-nested-governance/coverage-baseline.txt`（脚本只打印、不写文件）；核对头部含 `frozen-from:` 且正文**不含**本切片 30 条 `C-n` 名（`--freeze` 排除被核算 spec 本身，本切片条款只能被任务行认领、不能被自己的基线豁免），随后 `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance` 必须 exit 0。

**Checkpoint**: 三类分母落盘（镜像 / 副本 / 存储面文件名集、名字级失败名单、条款覆盖）；后续每一行的"零新增"与"包含性"判定都有冻结对照物。

---

## Phase 2: User Story 1 - 外层消费并交接嵌套运行的结果 (Priority: P2)（父 US4）

**Goal**: 团队运行报告强制承载 `## Nested SDD Runs` 段，逐次列出 outcome、工件与证据路径、分流裁决引用与异常；无嵌套调用时显式声明而非省略；被阻断或失败的嵌套运行永不被报成成功；Goal 不新增任何必填字段，归因只经团队 supervisor 在报告时追加的那一条既有 Target 引用台账条目。

**Independent Test**: 用 `tests/fixtures/nested_sdd.py`（`074a` 交付，原样复用）起一个夹具团队，跑一次到 review 的嵌套 SDD 运行；检查团队运行报告的嵌套段、证据路径、零 merge 零 push，并用 `goal-utils.py` 的 `parse_goal` 比对运行前后的 Goal 字段集完全一致、Target 归因只出现在台账的 `target_ref` 上。

- [X] T004 [US1] 红先编写契约测试到 `tests/contract/test_nested_run_report.py`：段标题字面量逐字等于 `"## Nested SDD Runs"` 且该字面量全仓只有报告契约一处落点；段对**每次运行**强制（有界 pattern 与 continuous 一律）；逐次列出 outcome（三值封闭集）+ artifact paths + evidence paths + routing-verdict reference + anomalies；无调用时显式声明"无嵌套 SDD 调用"且段不可省略（省略即判违约）；被阻断 / 失败不被改写成成功语气；路径以路径携带、不内联工件正文；既有必填段的名称与次序不变、新增段只在末尾追加；`## Verification` 与嵌套段并列（嵌套段证据不替代外层验证义务）；归因只经既有台账 `target_ref`、Goal 字段集前后一致、无新 Goal 字段；裁决引用缺记录时记 missing 且不得重算；运行红跑（红形态 = 报告契约无该段），把命令、真实输出、退出码写入 `.specify/specs/074b-nested-governance/notes/red-first-evidence.md`。
- [X] T005 [US1] [blockedBy: T004] 在 `skills/internal/create-team/SKILL.md` § Report contract（`:53`，骨架块 `:57-63`）追加**恰好一个**强制段：标题字面量 `## Nested SDD Runs`，逐次一行的五个字段（outcome 取 `completed` / `blocked` / `failed`、artifact paths、evidence paths、routing-verdict reference、anomalies），无调用时显式声明而非省略，且该段是既有必填段的**末尾追加**——既有段的名称、次序与内容义务逐字不变。 [green: contracts/report-and-attribution.md#C-21] [green: contracts/report-and-attribution.md#C-22] [green: contracts/report-and-attribution.md#C-23]
- [X] T006 [US1] [blockedBy: T005] 在同一 owner 段落归因边界：team supervisor 是段与全部 tracked 工件的唯一写者、嵌套运行不写任何 tracked 工件；报告时追加**恰好一条**台账条目，复用既有归因字段 `target_ref`（owner `skills/internal/create-team/references/summary-mapping.md` § 6.5，值形 `T-\d{3}`，由 `run-team/SKILL.md:66` 既有行承载），未声明 Target 的运行不发明占位 Target、其行不带归因字段；无新 Goal 字段、无 Goal→requirements 结构链接、无 Goal 定义写入；解析出的 Goal 字段集运行前后完全一致。 [green: contracts/report-and-attribution.md#C-24] [green: contracts/report-and-attribution.md#C-25] [green: contracts/report-and-attribution.md#C-26]
- [X] T007 [US1] [blockedBy: T006] 在同一 owner 段落三件读法：嵌套段与 `## Verification` 并列而非替代（嵌套运行的验证证据不解除外层运行的验证义务）；routing-verdict reference 是**引用**——指向 `074a` 在 Agent 执行证据里记录的那条裁决，段内不复制输入集 / 裁决表 / 理由码词表，记录不可定位时记 missing 且外层 MUST NOT 重算；handoff 的封闭字段集按引用读取，交接未携带的字段记 missing、不用调用方叙述补齐，`blocked` / `failed` 原样上抛。 [green: contracts/report-and-attribution.md#C-27] [green: contracts/report-and-attribution.md#C-28] [green: contracts/report-and-attribution.md#C-29]
- [X] T008 [US1] [blockedBy: T007] 单一 owner 审计：`grep -n 'Nested SDD Runs' skills/internal/create-team/SKILL.md skills/internal/run-team/SKILL.md skills/internal/run-agent/SKILL.md` 必须只在报告契约一处出现（`run-team/SKILL.md:66` 继续按路径委派、零第二份陈述），把命令与真实输出追加到 `notes/red-first-evidence.md` 的 single-owner 小节。 [green: contracts/report-and-attribution.md#C-30]
- [X] T009 [US1] [blockedBy: T008] US1 转绿与取证：`python3 -m pytest -q tests/contract/test_nested_run_report.py` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；用夹具团队实测把 quickstart 的 S2（段强制且空时显式声明）与 S3（归因后 Goal 字段集不变，`parse_goal` 前后比对）的命令、真实输出、退出码写入 `notes/quickstart-run.md`。

**Checkpoint**: US1 独立可验收——嵌套段强制存在且空时显式声明、逐次字段封闭、`blocked` / `failed` 不上色、归因只经既有台账且 Goal 字段集零变化；MVP 就位。

---

## Phase 3: User Story 2 - SDD 概念扩散而不被复制 (Priority: P3)（父 US5）

**Goal**: Goal / Team / Agent / 指令四类表面各获得推理 SDD 所需的最小词汇——团队报告能描述一次嵌套运行、Agent 定义能声明承载能力并写明三条职责、项目指令能指向分流规则、团队自身 Stage 维度与 SDD 阶段名册被显式消歧——而每一个事实都按路径抵达其既有 owner，零复制。

**Independent Test**: 跑 `tests/contract/test_sdd_diffusion.py`（检测重复阶段名册、无主枚举、职责陈述与声明不同时在场、指令面复述 owner 内容），并确认 team Stage 取值集逐字未变、出厂叶子预设立场未变。

- [X] T010 [US2] 红先编写契约测试到 `tests/contract/test_sdd_diffusion.py`：Stage 消歧句在场且 team Stage 取值集（`executor` / `evaluator` / `optimizer`）逐字不变、无名册形状枚举、名册 owner 仍唯一；承载声明与三条职责陈述**一起**读取（只有声明缺三条陈述判不合规，反之亦判不合规）；出厂叶子预设 `agents/sdd-executor.agent.md` 不声明 `sdd-invocation`（负向断言对制品而非对约定）；指令面恰一个指针段、反向计数审计为 0（查询集从**已落盘 owner** 提取实际短语，不用"我以为写了的短语"）；触发纪律的合取句只作指针且 `## ` 段集不变；每个 `[[STR-NNN]]` 引用解析到 `requirements.md` § Shared Strings 的一行；运行红跑（红形态 = 四个扩散面均未落盘），把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [X] T011 [US2] [blockedBy: T010] 在 `skills/internal/create-team/references/conceptual-model.md:10` 的既有 Stage bullet 就地追加消歧句：本 Stage 维度（`executor` / `evaluator` / `optimizer`）**不是** SDD 阶段名册，SDD 阶段名册仍归驱动所有；不重命名、不重载任何 team Stage 取值；作为既有 bullet 的句子追加，MUST NOT 新开顶层段；新增文本中不出现名册形状的枚举。 [green: contracts/diffusion.md#C-13] [green: contracts/diffusion.md#C-14]
- [X] T012 [US2] [blockedBy: T011] 在 `skills/internal/run-agent/SKILL.md` § Authoring Baseline（`:171`）既有 `sdd-invocation` 段之后落承载责任规则：声明 `allowed` 的定义 MUST 同时写明三件事——承载驱动、自身不执行阶段命令、止于 review；声明与正文 MUST 一起被读取；阶段执行者能力仍是叶子、MUST NOT 声明 `allowed`，该禁令对本仓出厂预设 `agents/sdd-executor.agent.md` 断言；取值域 / 缺省 / 不渲染三项只作指针指向键集 owner `src/specify_cli/__init__.py`（`NEUTRAL_AGENT_METADATA_KEYS`），不复述取值。 [green: contracts/diffusion.md#C-15] [green: contracts/diffusion.md#C-16] [green: contracts/diffusion.md#C-17]
- [X] T013 [US2] [blockedBy: T012] 在 `templates/instructions-template.md` 追加**恰好一个**附加式 `## ` 段作为指针级分流面：出现写留存变更时到 owner 路径执行裁决（`shared/definitions/sdd-routing-definitions.md` 与引擎 `scripts/python/sdd-route.py`）；段内 MUST NOT 出现输入集、封闭取值域、裁决表、理由码词表或第二条优先级表述；段内自声明本节字节上限（改前实测 live 41,948 B / template 34,666 B，判据是上限 + 增量，不是"装得下 32,768 B 预算"）。 [green: contracts/diffusion.md#C-18]
- [X] T014 [US2] [blockedBy: T013] 在 `shared/guidelines/proactive-trigger.md` § Promotion & Safety Boundary（`:68`；该文档的 `## ` 段集是交付的封闭集，共 10 段）内加**一句**：晋升为一次 SDD 运行 MUST 同时具备 SDD 类分流裁决与有效授权（`allowed`）；该合取由路由 owner 拥有、此处只作指针；MUST NOT 新开段、MUST NOT 新增任何可被门禁扫描的声明（gate total 不得移动）。 [green: contracts/diffusion.md#C-19]
- [X] T015 [US2] [blockedBy: T014] 运行 `bash scripts/bash/generate-instructions.sh` 把新段生成进 `.specify/instructions.md`，随即核验三件事：新 `## ` 段标题在 live 文件中在场；无既有段被改写（`git diff --stat` 只落在附加块上）；实测增量在 T013 声明的本段字节上限内；四个兼容指令符号链接（`AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md`）仍指向 live 文件、无需修复；live 文件 MUST NOT 手改。 [green: contracts/diffusion.md#C-20]
- [X] T016 [US2] [blockedBy: T015] US2 转绿与取证：`python3 -m pytest -q tests/contract/test_sdd_diffusion.py` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；把 quickstart 的 S4（Stage 消歧且零重命名）与 S5（指令指针恰一个附加段、经生成器再生）的命令、真实输出、退出码写入 `notes/quickstart-run.md`。

**Checkpoint**: US2 独立可验收——四类表面各有最小词汇、每个事实只按路径抵达 owner、team Stage 取值零重命名、出厂叶子仍不声明承载能力。

---

## Phase 4: Compatibility, Containment & Safety (cross-story)

**Purpose**: 兑现本地 FR-006 / FR-007 / FR-008 的三项义务——`forbidden` 缺省与派发前拒绝、四个前驱面的可加性、以及"不新增自动合并 / 推送 / 调度器 / 第二确认门 / 自动反馈传输"的安全负向面——并把两项包含性声明落成**可判定**的 node-id 名字集比较，而不是一句保证。

**⚠️ 本阶段零 `[US` 标记**：这些义务不属 US1 或 US2 的验收场景，它们是横跨两个故事的兼容与安全边界。

- [X] T017 以**超集方向**编辑 `tests/contract/test_sdd_invocation_governance.py`：新增"未声明即缺省"用例——Agent 定义或 Team 席位不携带 `sdd-invocation` 声明时解析为 `forbidden`，派发前探针拒绝任何点名 SDD 驱动的该类收件方派发；同时断言该缺失**不改变**该收件方派发的其他一切（其他键解析、payload 字段、失败消息形态不变，改动前未点名驱动的派发逐位保持既有行为）。既有用例的命题一条不改；本行按 migration/regression 例外处置（守的是 `074a` 已交付行为，只能先有行为后有测试），故绿即写、无红先步骤；改完先单独跑该文件确认既有 17 例仍绿、新增例全绿。 [green: contracts/compat-and-safety.md#C-1] [green: contracts/compat-and-safety.md#C-2]
- [X] T018 兑现两项包含性声明（载体 `test-evidence/compat-baseline-nodeids.txt`，7 个具名集合 / 17 文件 / 266 例，冻结于 `33269994a`）：用同一命令与同一文件清单做改后 `pytest --collect-only`，逐集合断言 post ⊇ pre 且共享 id 裁决不变（**计数比较判不合规**；pre \ post 非空即失败并列出被丢 id）；同时对四个前驱面做可加性审计——`git diff --stat` 覆盖 `skills/external/sdd-loop-driver/**`、070 阶段团队预设契约、064 线 / 工作树 / 归属契约、058 U0–U6 契约的 owner 必须为空 diff（本切片不触碰它们），任何既有键 / 段 / 入口形式 / 退出码含义的变化即是违约；把命令与真实输出写入 `notes/pre-change-measurements.md` 的 containment 小节。 [green: contracts/compat-and-safety.md#C-3] [green: contracts/compat-and-safety.md#C-4] [green: contracts/compat-and-safety.md#C-5] [green: contracts/compat-and-safety.md#C-6]
- [X] T019 红先编写契约测试到 `tests/contract/test_sdd_compat_containment.py`：四面可加性的结构负向断言（独立驱动入口的默认解析行为不变、嵌套形态仍是"先校验后拒绝"的独立入口；070 阶段团队预设的键 / 段 / 入口形式不变、工作包仍是唯一的运行内分解机制；064 线注册表字段 / 工作树形态 / 归属与集成队列接口不变；058 的 U0–U6 阶段语义、哨兵、独立验证、watcher 判定与退出码、卡死处置、测试预算规则不变）；安全负向面（无自动 merge / push、无调度器或守护进程、无自动 feedback 传输、无第二确认门、段内 outcome 是数据不构成集成授权）；零新增 `/speckit.*` 命令与零新增技能（flow-class 单元数与发现数不变）；零新增存储面（报告段是既有报告里的文本、归因行是既有台账的一条、指针面是既有文档的段、包含性载体是测试证据工件，无 registry / ledger / 状态脊 / ownership 模型 / 集成队列）；运行红跑（红形态 = 该文件不存在），把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。 [green: contracts/compat-and-safety.md#C-7] [green: contracts/compat-and-safety.md#C-8] [green: contracts/compat-and-safety.md#C-9] [green: contracts/compat-and-safety.md#C-10] [green: contracts/compat-and-safety.md#C-11] [green: contracts/compat-and-safety.md#C-12]
- [X] T020 [blockedBy: T019] 兼容阶段转绿与取证：`python3 -m pytest -q tests/contract/test_sdd_compat_containment.py tests/contract/test_sdd_invocation_governance.py` 跑到全绿并把绿证据追加 `notes/red-first-evidence.md`；把 quickstart S6 的**改后半**（改后集合同样可判定、逐集合超集比较的真实输出）接着 S6 改前半写入 `notes/quickstart-run.md`。

**Checkpoint**: 兼容与安全面独立可验收——缺省 `forbidden` 与派发前拒绝可判定、两个包含性声明以名字集比较兑现（不是计数）、四个前驱面零改动、安全负向面全部成立。

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: 收口镜像与再生面、结构面、回归、条款覆盖与登记。

- [X] T021 镜像同步与逐对核验：`python3 scripts/python/sync-mirrors.py --write --only templates --only skills --only shared` 后 `python3 scripts/python/sync-mirrors.py --check`（相对 T001 基线零新增差异），并用 `cmp` 逐对核对 5 个被编辑源文件与各自 `.specify/` 投影同字节——`skills/internal/create-team/SKILL.md`、`skills/internal/create-team/references/conceptual-model.md`、`skills/internal/run-agent/SKILL.md`、`shared/guidelines/proactive-trigger.md`、`templates/instructions-template.md`；`python3 scripts/python/regen-command-copies.py --check` 仍 `OK`（证明 `templates/commands/**` 零改动）；禁止手改镜像。
- [X] T022 refresh-verify（与 T021 共用同一证据落点，故按行序串行）：再跑一次 `bash scripts/bash/generate-instructions.sh`，确认 `.specify/instructions.md` 与首次生成逐字节相同（幂等），且 `ls -l AGENTS.md CLAUDE.md QODER.md .github/copilot-instructions.md` 四条兼容路径仍解析到该 live 文件；把两次运行与幂等比较的真实输出追加 `notes/quickstart-run.md` 的 refresh 小节。
- [X] T023 定向回归与分类诚实性：重跑 `test-evidence/targeted-set-v1-baseline.txt` 的 19 个既有契约文件 + 3 支新套件，把既有文件的失败 nodeid 排序后与 T002 重采名单做 `comm -13`（MUST 为空，判据是名字级不是条数级）；3 支新文件 MUST 全绿；唯一既有红 `test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged` MUST 保持红且**未移动**（gate total 仍 27），不对它作任何绿声明；同趟落审计职责——`/speckit.review` 是本切片的分类诚实性审计面，结论记入 review 证据而不回写裁决；结果与命令追加 `notes/pre-change-measurements.md` 的回归小节。
- [X] T024 结构面复核（与 T023 共用同一证据落点，故按行序串行）：(a) 零新增命令 / 技能——`ls templates/commands/*.md | wc -l`、`ls -d skills/external/*/ | wc -l`、`ls -d skills/internal/*/ | wc -l` 相对 T001 基线不变；(b) 零新增存储面——`.specify/state/` 与既有 line registry 目录、`.specify/memory/` 的文件名集合相对 T001 基线 `comm -13` 为空；(c) `python3 .specify/scripts/python/flow-class-check.py --action check` 仍为 `79 unit(s) / 0 finding(s)`；把命令与输出写入 `notes/quickstart-run.md` 的 structure 小节。
- [X] T025 覆盖、SC 证据与登记收口：`python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance` 必须 exit 0 且报 `claimed clauses = 30`、`FR 8 / 8`、`uncovered beyond baseline: 0`；把 SC-001 / SC-002 的状态（只从 `.specify/templates/verification-log-template.md` 的封闭词表取值）、命令、输出摘要与证据指针逐条写入 `.specify/specs/074b-nested-governance/verification.md`，并逐条声明本趟的 `PLAN-EDIT:`（若有）；同步把本切片的条目追加到 `.specify/memory/features/074.md` § Latest Review（状态列保持 `Planned`，`features.md` 的 074 行不新增行——`Implemented` 转移按 `.specify/shared/workflow/feature-integration.md` 判定，不在本行擅自推进）。
- [X] T026 终局门禁复跑：依次跑 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/074b-nested-governance/tasks.md`（0 error）、`python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/074b-nested-governance --stage tasks --repo .`（errors=0，advisory 逐条裁定）、`python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/074b-nested-governance/requirements.md --tasks .specify/specs/074b-nested-governance/tasks.md`（`proceed`）、`python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/074b-nested-governance`（30 / FR 8 / beyond baseline 0），把四段真实输出贴入 `verification.md` 的 gates 小节；若发现与冻结清单的结构漂移，按 rerun 契约追加新行而不重编号。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始；T002 / T003 互为 `[P]`（写目标不同）；T003 依赖本文件已声明的 `[green:]` 认领（即文件本身落盘）。
- **User Stories (Phase 2–3)**: 均依赖 Setup（证据落点就位）。US1（P2）先于 US2（P3）——这是 requirements 的优先级，也是价值顺序：扩散面只有在消费面存在后才产生价值。
- **Compatibility & Safety (Phase 4)**: 依赖 US1 与 US2 的编辑面落地（包含性比较与结构负向断言都针对改后的树）。
- **Polish (Phase 5)**: 依赖全部前序阶段完成。

### User Story Dependencies

- **US1 (P2)**: 依赖 Setup；不依赖 US2——报告段与归因面的 owner 是 `create-team`，Stage 消歧与指令指针在另一批 owner 上。
- **US2 (P3)**: 依赖 Setup；与 US1 零写目标重叠（5 个编辑面互不相交：`conceptual-model.md`、`run-agent/SKILL.md`、`instructions-template.md`、`proactive-trigger.md` 与 US1 的 `create-team/SKILL.md`）。
- **Phase 4**: 依赖 US1 + US2；T017 与 T019 写不同测试文件，T018 只写证据，三者彼此无写冲突，但按条款顺序（C-1…C-12 单调）串行排列。

### Within Each User Story

- 红先测试先写并跑红（命令 + 真实输出 + 退出码入 `notes/red-first-evidence.md`）→ 再实现 → 再转绿取证。
- 一个条款只由一个行认领；同一契约内认领顺序单调递增。
- 同一文件的多行（`skills/internal/create-team/SKILL.md`：T005 / T006 / T007 三行连续；`tests/contract/test_sdd_compat_containment.py` 只在 T019 落地）按行序串行，不加 `[P]`。
- T012 的 Stage bullet（`conceptual-model.md`）与 T013 / T014 的模板 / 指南是不同文件，但都服务于同一支测试文件，故仍按行序串行以保持"红先 → 逐面转绿"的可读顺序。

### Parallel Opportunities

- Phase 1：T002 与 T003 可并行（写目标不同：`test-evidence/targeted-set-v1-baseline.txt` 与 `coverage-baseline.txt`）。
- 其余阶段零 `[P]`：红先行共用 `notes/red-first-evidence.md` 这一追加落点，三条转绿行共用 `notes/quickstart-run.md` 这一追加落点，T021 逐对核对时点名全部 5 个源文件，T023 / T024 共用 `notes/pre-change-measurements.md` 与 `notes/quickstart-run.md`——同一文件即同写目标，按行序串行。

## Parallel Example: Phase 1

```bash
# 两条互不写同一文件的基线重采行可同时启动：
Task: "名字级测试基线重采（T002）"
Task: "条款覆盖基线冻结（T003）"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: MVP = **US1 单独**。本切片的两个用户故事在 requirements 中不同优先级（US1 = P2 / 父 US4，US2 = P3 / 父 US5），且 requirements 明确写了扩散面"只有在消费面存在后才交付价值"——因此 US1 的 checkpoint 就是一个独立有价值的增量：外层会读、会报、会归因，而 Goal 字段集零变化。US2 与 Phase 4 是同一交付的扩散与安全边界，不可裁掉，但不属 MVP 演示面。

1. Phase 1 Setup（冻结三类分母）
2. US1 → 按 Checkpoint 独立验收（MVP 完成，可演示）
3. US2 → 按 Checkpoint 独立验收
4. Phase 4 兼容与安全面 → 按 Checkpoint 独立验收
5. Phase 5 Polish（镜像、再生幂等、回归、结构面、覆盖与登记）

### Incremental Delivery

1. Setup → 每一行的判定都有冻结对照物
2. US1 → 一次嵌套运行的结果成为外层可读、可审计、可归因的制品，且 Goal 面零新增
3. US2 → 四类表面各获得最小词汇，事实仍只有一处落盘
4. Phase 4 → 两项包含性声明以名字集比较兑现，四个前驱面零改动，安全负向面成立
5. Polish → 零漂移、零新增存储面、SC 证据齐备

---

## Notes

- **plan_constraint（active since 2026-10-29T04:47Z，plan_commit = ce9de5983）**: 本切片的 plan-owned 面（`plan.md` / `data-model.md` / `contracts/**` / `quickstart.md` / `research.md` / `feature-ref.md`）只接受行级小修，逐项在 `verification.md` 声明 `PLAN-EDIT: <path> — <理由>；分类=minor`；实质性改动停线回抛，不静默重写。父设计与 `074a` 的全套产物全程只读。
- **测试预算**: 本切片使用 targeted-set-v1（`stage_base=tasks`），本阶段只跑**一次**；全量 baseline / closure 两个槽位归 implement 与 review 阶段，本文件不预占，且禁止在本阶段跑第二次全量。
- **陷阱形复核**: 「新增存储面为零」的计量单位是**文件名集合**（`comm -13`），不是行数或目录数；「`sdd-invocation` 已落盘处数」的计量单位是出厂预设定件，不是全仓 grep 命中（设计文档里的说明文字是引用，不是声明）；「条款数」的计量单位是行首加粗的条款定义行，不是全仓 `C-` 命中；「包含性」的计量单位是 node-id **名字集**，不是条数。
- **不复述面**: SDD 阶段名册、分流输入集 / 取值域 / 裁决表 / 理由码词表、中性键取值、门禁分类表、复杂度层级信号、五阶段语义与哨兵一律按路径抵达各自 owner，本文件与任何实现面 MUST NOT 复述。
- **零越界面**: 本切片不实现 `074a` 承接的父 `FR 001`–`FR 019` 与 `FR 025` 面，不改 `skills/external/sdd-loop-driver/**`、`shared/definitions/sdd-routing-definitions.md`、`scripts/python/sdd-route.py`、`shared/definitions/subagent-definitions.md`、`src/specify_cli/__init__.py`、`agents/sdd-executor.agent.md`、`templates/commands/**`；`run-team/SKILL.md` 只作单一 owner 审计的读取对象，不编辑。
