# Tasks: General Best Practices — 四分类封闭集模块与渐进积累（随框架分发）

**Requirement ID**: 111
**Requirement Key**: `111-general-best-practices`
**Related Feature**: 111 General Best Practices（通用最佳实践）——新独立 Feature（无父切片）；本阶段按 stage brief 对 `.specify/features.md` 与 `.specify/features/111-*.md` 零编辑，索引行与详情文件由后续特性登记阶段落地（FR-009 的唯一例外）
**Input**: Design documents from `.specify/specs/111-general-best-practices/`
**Prerequisites**: plan.md（Technical Context / Mirror Obligations / Execution Premises EP-001…EP-005 / research § Re-measure list 1–6）、requirements.md（9 FR / 7 SC / 7 STR / A-1…A-21 / US1…US3）、research.md（M1–M11 / R-1–R-10）、data-model.md（E1–E11 / INV-01…INV-12 / T1–T3）、contracts/ ×4（24 条款：manifest C-101…C-106 / entry-shape C-201…C-205 / accumulation C-301…C-306 / distribution-guard C-401…C-407）、quickstart.md（S-0…S-8）、feature-ref.md

**Tests Mode**: ON（宪法 Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则；本特性为 doc-feature 形态——交付面是五份 Markdown 内容文档、一行框架地图登记与一个结构契约守卫，因此测试形态是 `tests/contract/test_general_best_practices.py` 的结构契约断言（红先、六腿 a–f），而非运行时 unit / integration 测试；镜像字节一致由既有参数化套件 `tests/contract/test_mirror_parity_suite.py` 唯一裁决，守卫不复制比较逻辑。）

**Tests**: 红先证据的唯一落点 `.specify/specs/111-general-best-practices/notes/red-first-evidence.md`（每条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 `/speckit.implement` 的 `**Test runs**` owner（本文件只引用，不复述其路径与 flag）。测试唯一入口 `scripts/bash/run-tests.sh`；interpreter 固定在 § Environment Prerequisites。

**Organization**: 按用户故事组织——US1（遇到开发摩擦时读到规范做法：清单封闭集、四个 owner 文件、首条种子；P1）、US2（经既有引擎渐进积累新条目：观察 / 晋升 / 来源追溯的指针声明与无第二机制；P1）、US3（下游项目经 init 收到模块并可在框架地图找到：地图登记行、镜像再生成与零漂移、init 分发证明；P2）。US1 独立构成最小可交付增量（MVP）；US2 是紧随其后的 P1 增量（同一清单的积累机制段）；US3 依赖前两者完成的内容面才可登记、镜像与分发。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/111-general-best-practices/test-evidence/verification-input.md` 的 `deferred_tasks=`（`verification.md` 由 spec 侧从该输入派生）。
- DoD-2: 交付面齐备——`shared/best-practices/` 顶层恰为五文档（清单 `README.md` + 四个 owner 文件，含三处「尚无条目」占位与首条种子）、`shared/definitions/framework-map.md` 恰一行登记、`tests/contract/test_general_best_practices.py` 一个守卫、`.specify/shared/` 镜像由 `sync-mirrors.py` 写模式再生成；`src/`、`templates/`、`.specify/instructions.md`、`.specify/.gitignore`、`.specify/glossary.md`、`.specify/features.md` 与决策治理面零改动；变更路径集按 FR-009（单一 owner，本行只引用；GATE-7 只消费）判定。
- DoD-3: 覆盖如实记账——FR 9/9、SC 7/7 以 § Requirement Coverage Map 为权威；4 份契约共 24 条款由 § Clause Coverage & Green Partition 逐条恰好认领一次；`validate-tasks.py` 零 ERROR，WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`。
- DoD-4: 红先证据完整——守卫在模块落地前经唯一入口执行并失败（命令、真实输出、退出码记录在 `notes/red-first-evidence.md`）；模块、地图行与镜像落地后同一守卫全六腿转绿（记录在 `notes/us3-green.txt`）。
- DoD-5: 适配与零残留——模块五文档中 `ai-harness` / `.ah/` / `/ah.` 出现数 = 0、归属声明为 Feature 111、被引仓内路径全部存在，由守卫的模块读取前导断言钉住（FR-008 / SC-005）。
- DoD-6: 分发与镜像——`sync-mirrors.py --check` 相对入口基线零 NEW 漂移（`shared/` 对报告 122 文件字节一致，见 § Measured Premises 的陷阱形）、既有参数化镜像套件零新增红、init 分发三项证据（代码路径引用 + 既有 init 集成测试 + `.specify/.tmp/` 内只读演练恰五文档）记录在 `test-evidence/init-distribution-proof.txt`，且 `git diff --numstat 0419adae5..HEAD -- src/` 零行。
- DoD-7: 验收证据——`.specify/specs/111-general-best-practices/test-evidence/verification-input.md` 逐条记录 SC-001…SC-007 的状态、命令、值与证据指针；`final` 路径判据 SC-001…SC-006 记 `pass`，且一条 smoke 记录齐备（`smoke_command=`、`smoke_exit_code=0`、存在且非空的 `smoke_evidence_path=`）；`verification.md` 由 spec 侧从该输入派生（crew MUST NOT 直接写）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/111-general-best-practices/tasks.md` exit 0（0 error；WARN 逐条裁定并记录在 `test-evidence/tasks-validator.txt`）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/111-general-best-practices --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: FR / SC / 条款覆盖 — check: 本文件 § Requirement Coverage Map 为 9/9 与 7/7，§ Clause Coverage & Green Partition 的 24 条款逐条恰认领一次；`validate-tasks.py` 的 `green-dangling` / `green-clause-collision` / `green-cross-phase` / `green-path-divergence` 零 ERROR。
- GATE-4: final 路径成功判据 + smoke 记录 — check: `verification.md`（spec 侧从 `test-evidence/verification-input.md` 派生）中 `**Path**` 为 `final` 的 SC-001…SC-006 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 镜像收敛 — check: `python3 scripts/python/sync-mirrors.py --check` exit 0 且 `shared/` 对报告 `122 files, byte-identical`（117 基线 + 5 新文档）；`tests/contract/test_mirror_parity_suite.py` 经唯一入口零失败。
- GATE-6: 守卫与分发证明 — check: `bash scripts/bash/run-tests.sh tests/contract/test_general_best_practices.py` exit 0（全六腿 a–f）；`test-evidence/init-distribution-proof.txt` 三项证据齐备；`git diff --numstat 0419adae5..HEAD -- src/` 输出为空。
- GATE-7: 边界封闭 — check: `git diff --name-only 0419adae5..HEAD` 减去 FR-009 声明集后，残余仅限 `.specify/{session,feedback,exec-quant}/` 且记录体含特性 key `111-general-best-practices` 或 run id `r20261127T071500Z-111a`（A-20 残余判定程序）；读数记录在 `test-evidence/containment.txt`。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/111-general-best-practices/tasks.md` 返回 0。

## Environment Prerequisites

- CPython `>=3.8`: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-27；affected: 全部实现行与测试行。
- pytest: **available** — probe: `/usr/local/bin/python3 -c 'import pytest,sys; print(pytest.__version__, sys.version.split()[0])'` → `8.4.2 3.11.11` @ 2026-11-27；约束：PATH 上的 `python3` import no pytest（probe 输出 `ModuleNotFoundError: No module named 'pytest'`），因此全部测试行 MUST 经唯一入口 `scripts/bash/run-tests.sh` 并传入 `SPECKIT_PYTHON=/usr/local/bin/python3`；affected: 全部测试行。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-27；affected: 唯一测试入口、镜像引擎、基线对象与包含性读数。
- `specify` CLI 资源解析: **source-run available / installed 不可用** — probe: `specify --version` → `framework commit: fed513bcc… (embedded)`（全局安装在 `/home/agent/.local/lib/python3.11/site-packages/` 且自带打包 `shared/`，看不到本工作树模块）；`PYTHONPATH=<worktree>/src /usr/local/bin/python3 -c 'import specify_cli; specify_cli.main()' --version` → `framework commit: 1638077e4… (git)`；一次 `.specify/.tmp/` 内只读演练 `init --here --ai qoder --script sh --no-git` rc 0（`.specify/shared/` 已拷贝、`best-practices/` 缺席 = 实现前应有的读数）@ 2026-11-27；affected: 仅 T014 的 init 演练行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git`、本地 pytest、既有只读引擎与一次本地 init 拷贝，无构建、无拉取、无网络、无守护进程 @ 2026-11-27；affected: none。

**A13 boundary**（owner: `shared/workflow/acceptance-hardening.md` § Gates — 本注为指针，不是第二规则）：本节只记录任务生成期的探针结论（探测命令 + ISO 日期）；规划期承重前提归 `plan.md` § Execution Premises，依赖特性继承记录归 `plan.md` § Inherited Blockers。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标逐行不同、无未完成依赖）。本文件的 `[P]` 只出现在 T006 / T007：写目标分别为三个占位 owner 文件与 `programming-tools.md`，对 `README.md` 与只读源只作引用；其余行因共享同一清单、同一地图、同一镜像面或同一证据 sink 而按行序串行。
- **[Story]**: 用户故事标签（`[US1]`…`[US3]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零故事标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是该条款在本特性重新转绿的那一行；契约路径相对本文件目录解析。**24 条款分区**：manifest C-101…C-103 → T008、C-104…C-106 → T010；entry-shape C-201…C-205 → T008；accumulation C-301…C-306 → T010；distribution-guard C-401…C-402 → T013、C-403…C-405 → T015、C-406…C-407 → T019（C-406 的包含性窗口与 C-407 的三证据包在收口行一并读定）。测试编写行不携带 `[green:]`，验证行只以 `run` 治理词引用测试路径，故无 `green-path-divergence`。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `test-evidence/verification-input.md` 的 `deferred_tasks=`、由 spec 侧派生进 `verification.md`，并在行内加 `<!-- deferred: <reason> -->`）。

## Path Conventions

- **编辑面（框架源）**: `shared/best-practices/README.md`、`shared/best-practices/programming-languages.md`、`shared/best-practices/system-interfaces.md`、`shared/best-practices/programming-frameworks.md`、`shared/best-practices/programming-tools.md`、`shared/definitions/framework-map.md`（恰一行）、`tests/contract/test_general_best_practices.py`。
- **生成面（MUST NOT 手改）**: `.specify/shared/best-practices/**`（五文档镜像）、`.specify/shared/definitions/framework-map.md`（由 `sync-mirrors.py` 写模式再生成）。
- **证据落点（本特性）**: `.specify/specs/111-general-best-practices/notes/{red-first-evidence.md, pre-change-measurements.md, quickstart-run.md, us1-green.txt, us2-green.txt, us3-green.txt}`、`test-evidence/{init-distribution-proof.txt, us1-names.txt, us2-names.txt, us3-names.txt, mirror-parity-names.txt, targeted-names.txt, targeted-set.txt, full-names.txt, full-suite.txt, containment.txt, verification-input.md, tasks-validator.txt, tasks-pre-analyze.txt, decomposition-tasks.txt}`、`coverage-baseline.txt`。
- **只读面（零修改）**: `.specify/specs/111-general-best-practices/{requirements.md, plan.md, data-model.md, contracts/, research.md, quickstart.md, feature-ref.md}`（plan / requirements-owned；如需实质变更按 stage 规则回抛 `ANOMALY`）；`.specify/instructions.md`、`templates/`、`src/`、`.specify/.gitignore`、`.specify/glossary.md`、`.specify/features.md`、`.specify/features/**`、`shared/definitions/decision-definitions.md` 与其检查器、`.specify/register.md` 与 state spine。
- **只读源（移植输入）**: `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/`（ai-harness 087 已定稿内容；其规格与契约条款 id 不复用）。

## Measured Premises (re-measured at generation time 2026-11-27, HEAD `1638077e4`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' .specify/specs/111-general-best-practices/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]{3}\`' …/requirements.md` | **9 / 7 / 7** |
| 契约条款数（逐文件） | `grep -cE '^\*\*C-[0-9]{3}\*\*' .specify/specs/111-general-best-practices/contracts/*.md` | manifest **6** / entry-shape **5** / accumulation **6** / distribution-guard **7**；合计 **24**。**陷阱形**：按正文引用计数（如 `grep -ohE '\bC-[0-9]{3}\b' … \| wc -l`）会把 C-104 行内引用的 C-301…C-305 等一并算入；计量单位是行首 `**C-NNN**` 定义行 |
| 源模块组成与适配点 | `wc -l /storage/project/cloud-native-ai/ai-harness/shared/best-practices/*.md`；`grep -nE 'ai-harness\|\.ah/\|/ah\.' …/*.md`；`grep -n 'Feature 0' …/README.md` | **5** 文档 / **61** 行（README 38 / tools 8 / 其余 5/5/5）；残留字面量 **2** 行（README:3 `ai-harness`、README:33 `.ah/`）+ 归属行 **1** 处（README:5 `Feature 040`）；`/ah.` 全模块 **0** 命中。**陷阱形**：`Feature 040` 行不属于 FR-008 的三字面量残留扫描，但属归属适配点，漏改会使 SC-005 的归属断言失败 |
| 目标缺席 | `ls shared/best-practices .specify/shared/best-practices tests/contract/test_general_best_practices.py` | 3/3 `No such file or directory`（移植无覆盖风险；红先前提成立） |
| 积累 owner 在位 | `python3 .specify/scripts/python/feedback-utils.py --help`；`ls -la shared/guidelines/knowledge-promotion.md .specify/shared/guidelines/knowledge-promotion.md` | 动作集含 `record`（`{record,status,list,dispose,…}`）；两处 `knowledge-promotion.md` 皆 4849 B |
| 镜像基线 | `python3 scripts/python/sync-mirrors.py --check` | rc **0**；`ok    shared/ == .specify/shared/ (117 files, byte-identical)`。**陷阱形**：模块落地后该行 MUST 读到 **122** 文件（117 + 5 新文档）；仍读 117 = 镜像未收入模块 |
| 框架地图现状 | `grep -c 'best-practices' shared/definitions/framework-map.md .specify/shared/definitions/framework-map.md .specify/instructions.md`；`grep -n '\.specify/shared/' shared/definitions/framework-map.md` | 三处 **0** 命中；地图唯一布局表中 `.specify/shared/` 兄弟行位于第 48–55 行区，Notes 单元带 `(framework source: shared/…)` 指针（A-19 的行形态据此） |
| 解释器与 pytest | `/usr/local/bin/python3 -c 'import pytest,sys; print(pytest.__version__, sys.version.split()[0])'`；`python3 -c 'import pytest'` | `8.4.2 3.11.11`；PATH 的 `python3` → `ModuleNotFoundError: No module named 'pytest'`（`SPECKIT_PYTHON` 覆写必需） |
| CLI 解析形态 | `specify --version`；`PYTHONPATH=$PWD/src /usr/local/bin/python3 -c 'import specify_cli; specify_cli.main()' --version`；一次 `.specify/.tmp/` 只读演练 | installed → `framework commit: fed513bcc… (embedded)`；source-run → `framework commit: 1638077e4… (git)`；演练 rc **0**（`shared/` 拷贝在场、`best-practices/` 缺席）。**陷阱形**：用全局 installed `specify` 跑演练永远看不到本工作树模块，分发证明必为假 |
| 基线对象与包含性 | `git cat-file -e 0419adae5`；`git diff --name-only 0419adae5..HEAD \| wc -l`；`git diff --name-only 0419adae5..HEAD` | 对象在位；**43** 路径 = 34 规格路径 + 3 session + 3 feedback + 3 exec-quant，全部 ∈ FR-009 声明集。**陷阱形**：计划期读数是 18——计数随阶段落地增长，不变量是「全部 ∈ 声明集」而非某个具体计数 |
| 证据落点 / 守卫 / 覆盖基线现状 | `test -d …/notes`；`test -e tests/contract/test_general_best_practices.py`；`test -e …/coverage-baseline.txt` | 三者 **ABSENT** → Setup 行创建前者，实现行创建后两者 |

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T005, T008 | FR-004 | T009, T010 | FR-007 | T004, T008, T010, T013, T015 |
| FR-002 | T006, T007, T008 | FR-005 | T011, T012, T015 | FR-008 | T005, T006, T007, T008 |
| FR-003 | T007, T008 | FR-006 | T007A, T012, T013, T014 | FR-009 | T019 |

| SC | Rows |
|----|------|
| SC-001 | T008 |
| SC-002 | T008 |
| SC-003 | T010 |
| SC-004 | T013, T014, T015 |
| SC-005 | T008, T015 |
| SC-006 | T019 |
| SC-007 | T004, T015, T017, T018 |

## Clause Coverage & Green Partition

24 条机器可判定条款逐条恰认领一次。测试编写行不携带 `[green:]`；认领落在各故事末尾的验证行与 Polish 收口行（运行测试、写证据），验证行只以 `run` 治理词引用测试路径，因此无 `green-path-divergence`、无 `green-clause-collision`，每份契约内认领序号随行序单调。

| Contract | Clause | Pinning test / reading | Green point |
|----------|--------|------------------------|-------------|
| `contracts/manifest.contract.md` | C-101 | guard leg (a) — top-level file set exactly five | T008 |
| `contracts/manifest.contract.md` | C-102 | guard leg (a) — four categories, literal 封闭集 | T008 |
| `contracts/manifest.contract.md` | C-103 | guard leg (a) — sole table, 4 rows, 1 link each | T008 |
| `contracts/manifest.contract.md` | C-104 | guard leg (d) + manifest reading (readers/scope, entry shape, accumulation, seed pointer) | T010 |
| `contracts/manifest.contract.md` | C-105 | reading — owner files restate no scope; 内容 cells own it | T010 |
| `contracts/manifest.contract.md` | C-106 | reading — manifest carries the same-change trio sentence | T010 |
| `contracts/entry-shape.contract.md` | C-201 | guard leg (b) — entry shape bullets | T008 |
| `contracts/entry-shape.contract.md` | C-202 | guard leg (b) — H1 + accumulation blockquote | T008 |
| `contracts/entry-shape.contract.md` | C-203 | guard leg (b) — placeholder ⇔ zero entries | T008 |
| `contracts/entry-shape.contract.md` | C-204 | guard leg (c) — seed three facts + SSH extension, no source line | T008 |
| `contracts/entry-shape.contract.md` | C-205 | guard leg (b) — no semantic-truth claim, no frozen count | T008 |
| `contracts/accumulation.contract.md` | C-301 | guard leg (d) + manifest reading — marker + stem convention | T010 |
| `contracts/accumulation.contract.md` | C-302 | manifest reading — promotion only when general | T010 |
| `contracts/accumulation.contract.md` | C-303 | manifest reading — 来源 evidence + generality basis | T010 |
| `contracts/accumulation.contract.md` | C-304 | guard leg (d) — zero `best-practices*.py` under `scripts/python/` | T010 |
| `contracts/accumulation.contract.md` | C-305 | manifest reading — pointer-only, no restated owner rules | T010 |
| `contracts/accumulation.contract.md` | C-306 | manifest reading — red line (no hollow entries, no fabricated values) | T010 |
| `contracts/distribution-guard.contract.md` | C-401 | guard leg (e) + `git diff --numstat … -- src/` zero lines (T015/T019 readings) | T013 |
| `contracts/distribution-guard.contract.md` | C-402 | `sync-mirrors.py --check` 122-file reading + parity suite green | T013 |
| `contracts/distribution-guard.contract.md` | C-403 | guard leg (e) — one row in source and mirror, token triple | T015 |
| `contracts/distribution-guard.contract.md` | C-404 | guard full six-leg green through the runner | T015 |
| `contracts/distribution-guard.contract.md` | C-405 | guard module-read prelude — zero residue, cited paths exist | T015 |
| `contracts/distribution-guard.contract.md` | C-406 | containment reading (FR-009 set difference + A-20 residual predicate) | T019 |
| `contracts/distribution-guard.contract.md` | C-407 | init-proof package (three evidences) confirmed at closure | T019 |

## Feature Integration Review

- **Review performed at generation (2026-11-27)**: `.specify/features.md` 无 Feature 111 行、`.specify/features/111-*.md` 不存在（M1/M8 同读）；任务拆解不暴露新 Feature、不使任何既有 Feature 失效。tasks 阶段按 stage brief 对 `.specify/features.md` 与 `.specify/features/111-*.md` 零编辑；索引行、详情文件与 `Draft → Planned` 推进归后续特性登记阶段（FR-009 的唯一例外）。
- **Glossary**: 本特性不写 `.specify/glossary.md`——词汇候选（"best practice / 最佳实践"、"progressive accumulation / 渐进积累"）按 A-21 定格为提案文本、登记时点显式外置；FR-009 的声明集不含词表。
- **Deferrals**: 无任务被标记 `[~]`；注册表与词表属**范围外**（上述两条），不是延期的占位。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 先建立证据落点、冻结实现前的可执行基线，并把移植输入与运行时前提固定下来。

- [ ] T001 Create the evidence directory `.specify/specs/111-general-best-practices/notes/` with a `.gitkeep` so the red-first, pre-change and quickstart records have their fixed landing points (`notes/red-first-evidence.md`, `notes/pre-change-measurements.md`, `notes/quickstart-run.md`).
- [ ] T002 [blockedBy: T001] Freeze the contract coverage baseline with `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/111-general-best-practices --freeze > .specify/specs/111-general-best-practices/coverage-baseline.txt` and assert the frozen file is non-empty and its `frozen-from` header reads `excluding 111-general-best-practices`.
- [ ] T003 [blockedBy: T001] Capture the pre-change side of every diff premise in `.specify/specs/111-general-best-practices/notes/pre-change-measurements.md` with command, reading and date per row: the `sync-mirrors.py --check` baseline (`shared/` 117 files byte-identical, rc 0), the framework-map sibling `.specify/shared/` row block (lines 48–55) and its zero `best-practices` hits, the source module inventory (five documents / 61 lines; README:3 `ai-harness`, README:33 `.ah/`, README:5 `Feature 040`; zero `/ah.`), the source-run CLI reading (`framework commit: 1638077e4 (git)`), the `feedback-utils.py --help` `record` action and the two `knowledge-promotion.md` copies, `git cat-file -e 0419adae5` plus the live containment reading (43 paths at generation time, all inside FR-009's set), and the absence readings for the three target paths, `notes/` and `coverage-baseline.txt`.

**Checkpoint**: evidence landing points exist; every pre-change value is frozen before any edit; no executable surface changed yet.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 红先守卫——它钉住全部三个故事的形状、指针与登记断言，必须先于任何模块内容落地并转红。

**⚠️ CRITICAL**: 守卫未以红态存在之前，任何模块行不得开始。

- [ ] T004 [blockedBy: T001] Author the red-first structural guard `tests/contract/test_general_best_practices.py` (`pytestmark = pytest.mark.contract`) with one shared module-read prelude and six legs whose function names stay stable for later `-k` selections: `test_module_document_set_and_closed_category_table` (a: top-level file set exactly five documents; the manifest's sole table with three columns and four data rows, exactly one relative link per row, link-target set = the four owner files, literal 封闭集 present), `test_owner_files_placeholders_and_entry_shape` (b: one H1 per owner file + the accumulation blockquote; placeholder ⇔ zero entries; each entry carries `**实践**` and `**反例 / 证据**`, optional `**延伸**`, promoted entries add `**来源**`; never freeze the placeholder count; never claim semantic-truth judgement), `test_seed_entry_three_facts_and_ssh_extension` (c: default HTTPS; special-repo HTTP/SSH flagged with protocol and credential requirement; the `~/.git-credentials` HTTP-vs-HTTPS mismatch counter-example; the SSH extension; no fabricated 来源 line), `test_accumulation_pointer_chain_and_no_second_engine` (d: `feedback-utils.py --help` lists `record`; `knowledge-promotion.md` exists; the manifest contains `[best-practice]`; no `best-practices*.py` under `scripts/python/`), `test_framework_map_registration_rows_source_and_mirror` (e: exactly one row in `shared/definitions/framework-map.md` and one in `.specify/shared/definitions/framework-map.md`, each carrying `.specify/shared/best-practices/` and `Feature 111`), `test_relative_links_resolve` (f: every manifest ↔ owner-file relative link resolves); the prelude asserts zero `ai-harness` / `.ah/` / `/ah.` across the five documents and the existence of every cited repository path (at minimum `.specify/scripts/python/feedback-utils.py`, `shared/guidelines/knowledge-promotion.md`, `.specify/shared/best-practices/`, `tests/contract/test_general_best_practices.py`); run it through `scripts/bash/run-tests.sh` (SPECKIT_PYTHON per § Environment Prerequisites) and capture the failing output, command and exit code in `notes/red-first-evidence.md` (FR-007, FR-008; C-404).

**Checkpoint**: the guard exists and is red for the right reason (missing module), with its capture on record.

---

## Phase 3: User Story 1 - 遇到开发摩擦时读到规范做法 (Priority: P1) 🎯 MVP

**Goal**: `shared/best-practices/` 交付清单与四个分类 owner 文件——维护者从清单看到封闭四分类并逐行进入 owner 文件，在「编程工具」下直接读到 git clone 的默认口径与反例，三个空分类各有「尚无条目」占位与范围说明。

**Independent Test**: 守卫腿 (a)(b)(c)(f) 经唯一入口的选择运行转绿：5/5 文档、唯一表 4/4 行、4/4 链接可解析、3 占位 ⇔ 3 空分类 + 种子文件 1 条目 0 占位、种子三项事实 + SSH 延伸在场、零残留与引用路径存在。

### Verification for User Story 1

> 共享结构守卫已在 Foundational（T004）红先落地；本故事以 T008 运行其 (a)(b)(c)(f) 腿并记录绿点。

- [ ] T005 [US1] [blockedBy: T004] Author the manifest `shared/best-practices/README.md` by porting the settled source in substance (read-only `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/README.md`): title + module readers and scope (日常开发经典最佳实践库、渐进积累而非一次性清单) + the sole category table (three columns 模块/文件/内容; four data rows 编程语言 / 系统接口 / 编程框架 / 编程工具; exactly one relative link per row to the four owner files) + the 封闭集 change-process sentence (same-change trio: this manifest + the owner file + the guard) + the entry-shape declaration (标题 + 实践 + 反例/证据, optional 延伸; point at the entry-shape contract via its repo-resolvable path `.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md`) + the seed pointer to `programming-tools.md` § Git clone 的默认协议; adapt naming per FR-008 (`ai-harness` → `Spec Kit`, `.ah/` → `.specify/`, 归属 `Feature 040` → `Feature 111`); leave the accumulation section to T009 (FR-001, FR-008).
- [ ] T006 [P] [US1] [blockedBy: T005] Author the three placeholder owner files `shared/best-practices/programming-languages.md`, `shared/best-practices/system-interfaces.md` and `shared/best-practices/programming-frameworks.md` by porting the settled source in substance (read-only `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/`): each file exactly one H1 naming its category, a blockquote that 指向 `README.md` and carries the literal 积累机制 plus the entry-shape triple 标题 + 实践 + 反例/证据, and exactly one italic placeholder line containing 尚无条目 plus one scope sentence, with zero `## ` entries and no fabricated entries (FR-002; C-202, C-203).
- [ ] T007 [P] [US1] [blockedBy: T005] Author `shared/best-practices/programming-tools.md` seeded with the Git clone entry by porting the settled source in substance (read-only `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/programming-tools.md`): H1 + the blockquote that 指向 `README.md` with 积累机制 and the entry-shape triple + the heading `## Git clone 的默认协议` carrying `**实践**` (git clone URLs default to HTTPS; a special repository requiring HTTP or SSH MUST be flagged with its protocol and credential requirement), `**反例 / 证据**` (`~/.git-credentials` recorded HTTP credentials while the install flow cloned over HTTPS — the protocol mismatch broke the clone) and `**延伸**` (when an intranet service needs HTTPS authentication while SSH with a key works, prefer SSH or state the authentication requirement), with no `**来源**` bullet and no fabricated feedback id (seed exemption) (FR-003; C-204).
- [ ] T007A [US1] [blockedBy: T005, T006, T007] Regenerate the mirror with `python3 scripts/python/sync-mirrors.py` in write mode (never hand-edit) so `.specify/shared/best-practices/` carries the five US1 documents and every path the module cites — including the mirror directory the guard's module-read prelude asserts — exists before the US1 green run; the final fan-out after the accumulation section and the map row remains T012 (FR-006; C-402; A-24).
- [ ] T008 [US1] [blockedBy: T005, T006, T007, T007A] Run the US1 guard selection through the single entry (`bash scripts/bash/run-tests.sh -k "module_document_set or owner_files or seed_entry or relative_links" --names-out .specify/specs/111-general-best-practices/test-evidence/us1-names.txt tests/contract/test_general_best_practices.py`（只读）, SPECKIT_PYTHON per § Environment Prerequisites), confirm 5/5 documents, 4/4 table rows, 4/4 links, 3 placeholders ⇔ 3 empty categories with the seed file at 1 entry and 0 placeholders, the seed's three facts plus the SSH extension, and the prelude's zero-residue / cited-path readings; record the green reading with the SC-001, SC-002 and SC-005 evidence in `notes/us1-green.txt`. [green: contracts/manifest.contract.md#C-101] [green: contracts/manifest.contract.md#C-102] [green: contracts/manifest.contract.md#C-103] [green: contracts/entry-shape.contract.md#C-201] [green: contracts/entry-shape.contract.md#C-202] [green: contracts/entry-shape.contract.md#C-203] [green: contracts/entry-shape.contract.md#C-204] [green: contracts/entry-shape.contract.md#C-205]

**Checkpoint**: US1 独立可测——内容模块可读：封闭集表可逐行抵达 owner 文件，种子条目给出默认口径 + 提示义务 + 反例 + 延伸，空分类以占位诚实呈现。

---

## Phase 4: User Story 2 - 经既有引擎渐进积累新条目 (Priority: P1)

**Goal**: 清单以「引擎指针 + 自有规则」声明渐进积累——观察经既有 feedback 引擎落为带 `[best-practice]` 标记与分类 stem 的记录（`--review` 文本），证实通用后按清单「逐步积累机制」节拥有的晋升程序沉淀，知识记录义务按指针归既有 owner，晋升条目携带可回溯的 `**来源**`；全模块无第二引擎、存储、渲染器或索引。

**Independent Test**: 守卫腿 (d) 与清单读取共同成立：指针链 2/2 可解析（`feedback-utils.py --action record` 动作、`knowledge-promotion.md` 作为知识记录义务 owner 存在）、`[best-practice]` 在场、`scripts/python/` 下零 `best-practices*.py`；清单的「逐步积累机制」节拥有晋升程序与通用判据且不复述两个引擎所有者的取值；晋升 / 留痕 / 红线三要素在场。

### Verification for User Story 2

- [ ] T009 [US2] [blockedBy: T008] Add the 逐步积累机制 section to `shared/best-practices/README.md` by porting the settled source in substance (read-only `/storage/project/cloud-native-ai/ai-harness/shared/best-practices/README.md` § 逐步积累机制): observation recorded through `.specify/scripts/python/feedback-utils.py --action record` with the literal `[best-practice]` marker and exactly one owner-file stem (`programming-languages` / `system-interfaces` / `programming-frameworks` / `programming-tools`) in the record's `--review` text (record shape and remaining arguments stay with the engine's `--help`), the identity convention per A-17 (`/speckit.<command>`+`command` or `skill:<name>`+`skill` with the run's id, else `custom:best-practices/observation` + `--unit-type custom-unit` + `bp-<yyyy-mm-dd>-<slug>` with the probe system's external-probe prerequisite), the promotion procedure and generality criterion (recurrence or one explicit user correction) declared as the section's own rules (the manifest is their owner, A-22), the knowledge-recording obligation cited to `.specify/shared/guidelines/knowledge-promotion.md` by pointer, the promoted entry's `**来源**` bullet naming at least one of feedback entry id / ≥7-hex commit / quoted session utterance plus the generality basis, the red line (no hollow entries, no fabricated numbers or evidence; the existing module is mirrored to `.specify/shared/best-practices/` by `sync-mirrors.py` and MUST stay byte-identical), and wording that restates none of the owners' store-disposal rules, emphasis thresholds or enumerations; declare no second engine, store, renderer or index; keep the section's pointers valid for both source and mirror paths (FR-004; C-301…C-306).
- [ ] T010 [US2] [blockedBy: T009] Run the US2 guard selection through the single entry (`bash scripts/bash/run-tests.sh -k "accumulation_pointer" --names-out .specify/specs/111-general-best-practices/test-evidence/us2-names.txt tests/contract/test_general_best_practices.py`（只读）), confirm the pointer chain 2/2 resolves, `[best-practice]` present, zero `best-practices*.py` under `scripts/python/`, and read the manifest once for C-105 (owner files restate no scope — the 内容 cells own it) and C-106 (the same-change trio sentence); record the reading with the SC-003 evidence in `notes/us2-green.txt`. [green: contracts/manifest.contract.md#C-104] [green: contracts/manifest.contract.md#C-105] [green: contracts/manifest.contract.md#C-106] [green: contracts/accumulation.contract.md#C-301] [green: contracts/accumulation.contract.md#C-302] [green: contracts/accumulation.contract.md#C-303] [green: contracts/accumulation.contract.md#C-304] [green: contracts/accumulation.contract.md#C-305] [green: contracts/accumulation.contract.md#C-306]

**Checkpoint**: US2 独立可测——积累路径只以指针复用既有 feedback + memory 引擎，观察 / 晋升 / 留痕 / 红线四要素齐备，第二机制的可判定读数为 0。

---

## Phase 5: User Story 3 - 下游项目经 init 收到模块并可在框架地图找到 (Priority: P2)

**Goal**: 框架地图恰一行登记 `.specify/shared/best-practices/` 的含义与所有者；`.specify/shared/` 镜像由既有引擎再生成并零漂移；`specify init` 既有整目录拷贝把模块送到客户项目——三项证据（代码路径 + 既有集成测试 + 只读演练）齐备，零 CLI / 打包改动。

**Independent Test**: 守卫全六腿转绿（腿 (e) 在源与镜像各恰一行、双 token 在场）；`sync-mirrors.py --check` 对 `shared/` 报 122 文件字节一致且既有参数化套件零新增红；init 演练的 `.specify/shared/best-practices/` 恰为五文档；`git diff --numstat 0419adae5..HEAD -- src/` 零行。

### Verification for User Story 3

- [ ] T011 [US3] [blockedBy: T010] Add exactly one registration row to `shared/definitions/framework-map.md` inside its single layout table adjacent to the existing `.specify/shared/` rows (the block at lines 48–55, read-only reference), three columns: the Where cell is `.specify/shared/best-practices/`; the Notes cell carries 随框架分发的通用最佳实践内容模块, the literal `Feature 111`, a pointer to the module's `README.md` and the sibling-style source pointer `(framework source: shared/best-practices/)`; add no instructions pointer section and no second map (FR-005; C-403).
- [ ] T012 [US3] [blockedBy: T011] Regenerate the mirror by executing `python3 scripts/python/sync-mirrors.py` in write mode (never hand-edit): the single fan-out writes `.specify/shared/best-practices/` (the five documents) and the regenerated `.specify/shared/definitions/framework-map.md`, covering both rows of plan.md § Mirror Obligations (FR-005, FR-006; C-402).
- [ ] T013 [US3] [blockedBy: T012] Verify the mirror through its named adjudicators: `python3 scripts/python/sync-mirrors.py --check` exits 0 with the `shared/` pair reporting 122 files byte-identical (117 baseline + 5 new documents — a still-117 reading means the module did not reach the mirror), and run the existing parameterized suite through the single entry (`bash scripts/bash/run-tests.sh --names-out .specify/specs/111-general-best-practices/test-evidence/mirror-parity-names.txt tests/contract/test_mirror_parity_suite.py`（只读）); record both readings plus the per-row confirmation for the two Mirror Obligations rows in `notes/us3-green.txt` (FR-006; C-401, C-402). [green: contracts/distribution-guard.contract.md#C-401] [green: contracts/distribution-guard.contract.md#C-402]
- [ ] T014 [US3] [blockedBy: T012] Record the init-distribution proof in `test-evidence/init-distribution-proof.txt`: (1) the code-path citation of the wholesale `shared/` copy step in `src/specify_cli/__init__.py` (read-only; the `copy_tree_with_rewrite(resource_path / "shared", shared_dest)` block at ~lines 2743–2761); (2) the existing init integration test `tests/integration/test_init_new_layout.py` run through the single entry (it executes the same copy step from `PYTHONPATH=src`); (3) one read-only drill under `.specify/.tmp/`: in a fresh drill directory run the source-run CLI `PYTHONPATH=<worktree>/src /usr/local/bin/python3 -c 'import specify_cli; specify_cli.main()' init --here --ai qoder --script sh --no-git` (the globally installed `specify` reports `framework commit: fed513bcc… (embedded)` and ships its own packaged `shared/`, so it MUST NOT be used), then list the drill's `.specify/shared/best-practices/` and confirm exactly the five documents, and tear the drill down; record command, real output and exit codes (FR-006; C-407).
- [ ] T015 [US3] [blockedBy: T013, T014] Run the complete guard through the single entry (`bash scripts/bash/run-tests.sh --names-out .specify/specs/111-general-best-practices/test-evidence/us3-names.txt tests/contract/test_general_best_practices.py`（只读）), confirm all six legs (a)–(f) pass including the map-row leg's token pair (`.specify/shared/best-practices/` + `Feature 111`) in both the source and the mirror table, and confirm the init-proof package from T014 is complete; record the green reading with the SC-004 and SC-005 evidence in `notes/us3-green.txt`. [green: contracts/distribution-guard.contract.md#C-403] [green: contracts/distribution-guard.contract.md#C-404] [green: contracts/distribution-guard.contract.md#C-405]

**Checkpoint**: US3 独立可测——登记、镜像与分发三条通道全部以机器读数钉住，`src/` 零改动。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实录、定向集与全量套件收口、边界封闭与验收证据包。

- [ ] T016 [blockedBy: T015] Execute every scenario in `.specify/specs/111-general-best-practices/quickstart.md` exactly as written (S-0 readings re-taken; S-1…S-8 executed through their named pins) and record command, real output and exit status per scenario in `notes/quickstart-run.md`, teardown included.
- [ ] T017 [blockedBy: T015] Run the targeted set through the single entry (the guard `tests/contract/test_general_best_practices.py`, `tests/contract/test_mirror_parity_suite.py` and `tests/integration/test_init_new_layout.py`, all read-only) with `--names-out .specify/specs/111-general-best-practices/test-evidence/targeted-names.txt` and compare the failing-name list against the implement pre-flight baseline under the `/speckit.implement` § Test runs owner (path and flag owned there, not restated); record rc, counts and the zero-new-failure reading in `test-evidence/targeted-set.txt` (SC-007).
- [ ] T018 [blockedBy: T015] Run the full suite once through the single entry (`bash scripts/bash/run-tests.sh --full --names-out .specify/specs/111-general-best-practices/test-evidence/full-names.txt`), compare the failure-name set against the implement entry baseline by the owner's comparison form, and record rc, collected count, the failure-name set and the subset reading in `test-evidence/full-suite.txt` (SC-007).
- [ ] T019 [blockedBy: T016, T017, T018] Close the feature: take the containment reading (`git diff --name-only 0419adae5..HEAD` set difference against FR-009, with the A-20 residual body predicate — path-set difference first, then only `.specify/{session,feedback,exec-quant}/` residuals whose record body carries the feature key or the run id; record it in `test-evidence/containment.txt`), and assemble `test-evidence/verification-input.md` with one `SC-001_status`…`SC-007_status` row each (value, note, command, evidence pointer), the `final`-path criteria SC-001…SC-006 reading `pass`, and the single smoke record (`smoke_command=` the guard run through the single entry, `smoke_exit_code=0`, an existing non-empty `smoke_evidence_path=`); confirm the init-proof package and the containment reading together (FR-009; C-406, C-407). [green: contracts/distribution-guard.contract.md#C-406] [green: contracts/distribution-guard.contract.md#C-407]

**Checkpoint**: quickstart 全场景有实录；定向集零新增失败、全量集失败名 ⊆ 入口基线；包含性成立；`test-evidence/verification-input.md` 可被 spec 侧直接派生为 `verification.md` 供 review 消费。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，可立即开始。
- **Foundational (Phase 2)**: 依赖 Setup 的证据落点；守卫以红态先于一切模块内容存在，阻塞全部三个故事。
- **US1 (Phase 3)**: 依赖 Foundational；T005 → T006 / T007（[P] 对）→ T007A（写模式镜像先行建立）→ T008。
- **US2 (Phase 4)**: 依赖 US1 的验证（同一清单文件的积累机制段在其内容面之后追加）。
- **US3 (Phase 5)**: 依赖 US2（登记与镜像以完成的内容模块为对象）；T011 → T012 → T013 / T014 → T015。
- **Polish (Phase 6)**: 依赖 US3 完成。

### User Story Dependencies

- **US1（P1）**: Foundational 之后即可开始；产出五文档与种子；检查点独立可测（MVP）。
- **US2（P1）**: 依赖 US1 的清单与 owner 文件；检查点独立可测（指针链 + 无第二机制）。
- **US3（P2）**: 依赖 US1 / US2 的内容面（地图行、镜像与 init 证明都以模块为对象）；检查点独立可测（地图行 + 镜像零漂移 + init 三证据）。

### Within Each User Story

- 红先守卫在 Foundational 先行；每个故事的验证行以 `-k` 选择运行守卫并记录绿点，测试编写行不认领条款。
- 同一文件的编辑按行序串行（`README.md` 在 US1 / US2 各一次编辑；地图、镜像与证据 sink 都不并行写）。
- doc-feature 形态：作者（author-section）→ 镜像（US1 末尾 T007A 先行建立以满足前导存在性断言；US3 的 T012 统一再生成收口，mirror-parity）→ 渲染验证（守卫选择 / 全量运行，render-verify）→ 刷新验证（`sync-mirrors.py --check` + init 演练，refresh-verify）。

### Parallel Opportunities

- Setup 无 `[P]`（同一 notes 目录与同一证据面串行建立）。
- US1 的 T006 与 T007 可并行：写目标分别为三个占位 owner 文件与 `programming-tools.md`，对 `README.md` 与只读源只作引用。
- 其余行因共享同一清单、同一地图、同一镜像面或同一证据 sink 而按行序串行；本线为单执行体（`single-unit`）。

---

## Parallel Example: User Story 1

```bash
# Launch the two US1 authoring rows together (distinct write targets, distinct files):
Task: "Author the three placeholder owner files shared/best-practices/programming-languages.md, system-interfaces.md, programming-frameworks.md"
Task: "Author shared/best-practices/programming-tools.md seeded with the Git clone entry"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 only — it is the smallest same-priority set whose checkpoint is independently testable (5/5 documents, sole table 4/4 rows, 4/4 links, placeholder ⇔ zero entries, seed three facts + SSH extension) and it alone restores the module's reason for existing (the canonical default plus counter-example). US2 is the immediate second P1 increment (the accumulation section on the same manifest); US3 is the P2 distribution and registration closure.

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (the red-first guard).
3. Complete US1 (T005–T008).
4. **STOP and VALIDATE**: 用 US1 的独立测试标准验证（守卫 (a)(b)(c)(f) 选择运行转绿）。
5. Deliver US2, then US3, then Polish.

### Incremental Delivery

1. Setup → 证据落点与冻结基线就绪。
2. US1 → 内容模块可读（MVP）。
3. US2 → 积累机制以指针声明、无第二机制。
4. US3 → 地图登记、镜像零漂移与 init 分发证明。
5. Polish → quickstart 实录、定向集与全量收口、包含性与 `test-evidence/verification-input.md`。

### Parallel Team Strategy

单执行体（本线 `single-unit`）。若后续拆并行：仅 T006 / T007 可分组并行；清单、地图、镜像与 notes 汇总面永不由两个执行体同时写。

---

## Notes

- **PLAN-EDIT**: 无。本文件未改动任何 plan-owned 路径；contracts、quickstart、data-model、research、feature-ref 只被引用。实现期间如需对 plan-owned 路径做实质变更，按 stage 规则回抛 `ANOMALY`。
- **零新机制**: 所有引擎面零修改——观察按指针复用 `feedback-utils.py`，知识记录义务按指针归 `knowledge-promotion.md`，晋升程序与判据为清单自有规则（A-22）；`scripts/python/` 下 MUST NOT 出现 `best-practices*.py`；文本层第二机制声明归评审（SC-003）。
- **镜像单一裁决**: `.specify/shared/**` 只由 `sync-mirrors.py` 写模式再生成；字节一致唯一由既有 `tests/contract/test_mirror_parity_suite.py` 裁决，守卫不复制比较逻辑。
- **source-run CLI**: init 演练 MUST 使用 source-run 形态（`PYTHONPATH=<worktree>/src`）；全局 installed `specify` 自带打包 `shared/`（embedded commit 早于本线），用它演练会让分发证明失真。
- **测量陷阱**: 条款计数单位是行首 `**C-NNN**` 定义行（正文引用会高估）；镜像 `shared/` 计数 117 → 122（新增五文档），仍读 117 即镜像未收入模块；包含性计数随阶段增长（计划期 18 → 任务生成期 43），不变量是「全部 ∈ 声明集」而非具体计数；源模块的 `Feature 040` 归属行是第三个适配点。
- **测试预算**: 定向集（守卫 + 镜像参数化套件 + init 集成测试）+ 一次全量套件（SC-007），全部经唯一入口 `scripts/bash/run-tests.sh`；interpreter 固定在 § Environment Prerequisites。
- **词表 / 注册表**: 不写 `.specify/glossary.md`（A-21：提案文本定格、登记时点外置）与 `.specify/features.md` / `.specify/features/**`（FR-009：特性登记阶段为唯一例外）。