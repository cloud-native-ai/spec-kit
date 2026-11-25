# Tasks: Runtime Store Layout — 运行期存储迁出 `.specify/memory/`

**Requirement ID**: 105
**Requirement Key**: `105-runtime-store-layout`
**Related Feature**: 024 Specification Workspace Versioning（`.specify/features.md` 行 105；本阶段维持 `Planned`，无状态迁移权）
**Input**: Design documents from `.specify/specs/105-runtime-store-layout/`
**Prerequisites**: plan.md（技术路线 / Mirror Obligations / Work Packages ×15 / Structure Decision / § Backward-Incompatible Change Inventory BC01…BC18）、requirements.md（27 FR / 9 SC / 6 STR / A-1…A-16 / 17 行 Store Inventory）、research.md（R-1…R-13 实测）、data-model.md（E-1…E-10 / I-1…I-10）、contracts/ ×4（C-1…C-8 / M-1…M-10 / P-1…P-6 / L-1…L-8）、quickstart.md（S-0…S-8）、feature-ref.md（FR→WP 27/27、SC→证据 9/9）

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则；本特性交付引擎、迁移 CLI 与契约测试，测试形态为 contract / integration / unit 运行时测试，而非模板结构测试。plan.md § Test-First Coverage 为 SC-001…SC-009 逐条定义红先夹具与变异转红断言。migration/regression 例外共两处：US6 的残留 / 符号链接 / 只读 / 半迁移断言守的是 WP08 已交付的执行器行为，按 `.specify/skills/internal/create-tasks/SKILL.md` § Task Generation Rules 的 migration/regression 例外置于执行器实现之后，红能力由变异演练证明，不冒充红先；T042 的 FR-027/SC-009 清点守卫守的是已落盘的 plan 清点与 T016 已交付的迁移行为，按同一例外以变异演练证明红能力。）

**Tests**: 红先证据的唯一落点是 `.specify/specs/105-runtime-store-layout/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。测试执行唯一入口是 `bash scripts/bash/run-tests.sh`；interpreter 选择固定在 § Environment Prerequisites，任务行不写解释器级测试命令。

**Organization**: 按用户故事组织——US1（布局语义、墓碑与全新初始化，P1）、US2（既有项目升级零丢失、并存拒绝、幂等，P1）、US3（临时记忆与上下文注入行为不变，P1）、US4（tools 记录与生成清单同域、忽略与跟踪各归其位，P2）、US5（本仓 dogfood 与活引用 / 镜像零漂移，P2）、US6（半迁移与不可迁移状态被诚实报告，P3）。US1 + US2 + US3 共同构成 MVP：三条同为 P1，且「只改布局不迁移」只是一次改名、「迁移却不保记忆/注入」会打断用户明令保留的两个机制——三者检查点各自独立可测。Foundational 阶段承载所有故事的共同前置：单一机器声明与引擎根常量。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/105-runtime-store-layout/verification.md` 的 `deferred_tasks=`。
- DoD-2: 交付面 = 1 份机器声明（`shared/declarations/facts/runtime-store-layout.yaml` + `shared/declarations/contract.yaml` 注册）+ 1 份封闭的向后不兼容变更清点（`plan.md` § Backward-Incompatible Change Inventory，BC01…BC18）及其机器守卫 + 14 个顶层存储根 + 1 条墓碑行 + `specify migrate` 第六维 `store-layout` + 包内种子 `seed/` + 8 支新测试模块 + 1 支 fixture builders + 活引用 / 忽略 / 镜像 / 副本更新；零新增第三方依赖、零新增存储引擎 / 注册表 / 调度器 / 第二注入机制。
- DoD-3: 契约覆盖如实记账——4 份契约共 32 条款（C 8 / M 10 / P 6 / L 8）；其中 `store-layout.contract.md` 的 8 条 C 条款是机器可判定形式，8 条各被一个任务行 `[green:]` 认领一次（C-1→T003、C-2/C-3→T007、C-4→T023、C-5→T030、C-6→T032、C-7→T038、C-8→T040；认领行序与条款序号单调一致，零 green-cross-phase WARN；C-7 的绿点落在验收证据包 T038，因为全新初始化的机器绿由 SC-005 实测读数收口）；M / P / L 共 24 条以条款号引用但不具 `[green:]` 形态（`clause_extract.py` 对这三份文件返回 `form=md-none`；M-10（FR-027/SC-009 闭包）同样如此，这是计划期条款号的既有事实，不是本阶段可修复项）。`account-clause-coverage.py --spec-dir .specify/specs/105-runtime-store-layout` 报 `claimed clauses: 8` 且 `clause-uncovered` beyond baseline = 0；其 `fr-uncovered` 车道只读机器可判定条款的 citation group，读数 6/27（FR-027 不落在任何 C 条款 citation group 中）是 md-none 结构的既有事实——FR 覆盖的权威判据是本文件的 Requirement Coverage Map（27/27）加 `pre-analyze-check.py --stage tasks` 的 `runtime-stack-row` 行级校验 errors=0，不把会计器的 FR 车道冒充通过。
- DoD-4: 8 支新测试模块（`test_runtime_store_layout.py`（含 FR-027/SC-009 清点守卫 `test_backward_incompatible_inventory_is_closed`）、`test_store_layout_live_refs.py`、`test_tools_domain.py`、`test_store_layout_migration_us1_us2.py`、`test_store_layout_migration_us3_us6.py`、`test_memory_preservation.py`、`test_dispatch_injection_paths.py`、`test_init_new_layout.py`）与按 L-3 更新的既有测试全绿；全量套件相对 implement 入口的名字级失败基线零**新增**失败（既有红逐条点名、不声称全绿）。
- DoD-5: plan.md § Mirror Obligations 逐行落地——触及的源文件镜像已再生成且逐字节一致；`sync-mirrors.py --check` 的漂移成员集相对 450-DIFF 基线**无新增成员**（scope 同步可顺带治愈成员，按成员集差值记录）；`regen-command-copies.py --check` exit 0；零手改镜像 / 副本。
- DoD-6: 活引用封闭成立——按 L-5 的四文件允许集（墓碑行、退役根声明、anchor 迁移引擎、遗留残留扫描器）与三类产物面逐类比较，实测 = 声明（双向），类外零出现；四个变异演练（清单搬入未列文件 / 未列行）逐项转红并复原，读数落 `test-evidence/mutation-drill.md`。
- DoD-7: dogfood 完成——`.specify/memory/` 不再存在；受跟踪条目全部位于新顶层存储；每个存储的迁移回执为 v2 逐 run 一文一件；`git log --follow` 可追溯被移动条目；本仓无引擎重建退役根。
- DoD-8: `verification.md` 逐条记录 SC-001…SC-009 的状态、命令与证据指针；`final` 路径的 SC-001…SC-005 与 SC-009 记 `pass` 并带 smoke 记录（`smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=` 存在且非空）；dated record（`docs/reference/history/**`、`docs/decisions/**`、`.specify/specs/**`、`.specify/archive/**` 与记录型存储内既有条目）逐字未改。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/105-runtime-store-layout/tasks.md` exit 0（0 error；WARN 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `/usr/local/bin/python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/105-runtime-store-layout --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: 条款与 FR 覆盖 — check: `/usr/local/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/105-runtime-store-layout` 输出 `claimed clauses: 8` 且 `clause-uncovered` 的 beyond-baseline 为 0；`pre-analyze-check.py --stage tasks` 的 `runtime-stack-row` errors=0（每个 in-scope 运行时行的 FR 集至少被一个任务行引用）；本文件 Requirement Coverage Map 为 27/27。会计器的 `fr-uncovered` 车道按 6/27 如实报告（三份契约 `form=md-none` 的结构事实），不作通过判据。
- GATE-4: final-path 成功判据 + smoke 记录 — check: `verification.md` 中 `**Path**` 为 `final` 的 SC-001…SC-005 与 SC-009 全部 `pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-5: 全量套件零新增失败 — check: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --names-out <failed-list-file>` 的失败名集相对 implement 入口基线做 `comm -13` 为空（既有红逐条点名）。
- GATE-6: 镜像与副本干净 — check: `python3 scripts/python/sync-mirrors.py --check` 的漂移成员集相对 `test-evidence/sync-mirrors-baseline.txt` 无新增成员；`python3 scripts/python/regen-command-copies.py --check` exit 0；触及镜像对 `cmp` 空输出。
- GATE-7: 活引用封闭 + 退役根缺失 — check: `bash scripts/bash/run-tests.sh tests/contract/test_store_layout_live_refs.py -q` exit 0 且 `test ! -e .specify/memory`。
- GATE-8: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/105-runtime-store-layout/tasks.md` 返回 0。

## Environment Prerequisites

- CPython: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-25；约束：`python3` 解析到 profile venv（无 pytest），全部测试行 MUST 以 `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …` 经唯一入口执行；affected: 全部测试与引擎行。
- pytest / typer: **available** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2`；`/usr/local/bin/python3 -c "import typer; print(typer.__version__)"` → `0.19.2` @ 2026-11-25；affected: 全部测试行、`regen-command-copies.py`。
- bash / git: **available** — probe: `bash --version` → `4.4.20(1)-release`；`git --version` → `2.43.5` @ 2026-11-25；affected: 测试入口、迁移与证据行。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git` 与本地 pytest，无构建、无拉取、无网络、无守护进程 @ 2026-11-25；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本文件的 `[P]` 只出现在写目标逐行不同的行：Foundational 的 T004 / T005，US1 的 T007，US5 的 T026 / T027 / T028 / T029。US3 的 T017 / T018 共用 `notes/red-first-evidence.md` 这一追加 sink，按行序串行故零 `[P]`（同 104 先例）。T008 不标 `[P]`（2026-11-25 裁定）：其写目标（`seed/`、`pyproject.toml`、`src/specify_cli/__init__.py`）与 T007（`shared/definitions/framework-map.md`）实际不相交，但 T007 的墓碑引文内含 `.specify/session/`、`.specify/knowledge/`、`.specify/memory/` 三个字面量，`validate-tasks.py` 的写目标分类器将它们计入写目标并与 T008 的行内目标重叠；按行序串行以保持零 parallel-safe WARN。
- **[Story]**: 用户故事标签（`[US1]`…`[US6]`），只出现在用户故事阶段的任务行；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领。本特性 `[green:]` 只用于 `contracts/store-layout.contract.md` 的机器可判定条款（C-1…C-8）：C-1→T003、C-2/C-3→T007、C-4→T023、C-5→T030、C-6→T032、C-7→T038、C-8→T040。认领行序与条款序号单调一致，零 green-cross-phase WARN；C-7 的绿点落在验收证据包 T038（全新初始化的机器绿由 SC-005 实测读数收口，US1 的 T009 只做测试转绿与取证，不冒充最终绿点）。M / P / L 条款只以条款号引用（含 M-10）。分区结果由 `validate-tasks.py` 的四项 green 检查与 `account-clause-coverage.py` 共同核对。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `shared/`、`skills/`、`scripts/`、`src/`、`templates/`、`agents/`、`pyproject.toml`、包内种子 `seed/`。
- **生成面（MUST NOT 手改）**: `.specify/shared/**`、`.specify/skills/**`、`.specify/scripts/**`、`.specify/templates/**`、`.specify/agents/templates/**`（由 `sync-mirrors.py` 投影）；`.github/prompts/`、`.claude/commands/`、`.qoder/commands/`、`.opencode/command/`（由 `regen-command-copies.py` 生成）；`.specify/instructions.md`（由 instructions 生成器产出）。
- **证据落点（本特性）**: `.specify/specs/105-runtime-store-layout/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`（本阶段已冻结）、`test-evidence/mutation-drill.md`、`test-evidence/acceptance-105.md`、`verification.md`。
- **只读面（零修改）**: `docs/reference/history/**`、`docs/decisions/**`、`.specify/archive/**`、其他规格的 `.specify/specs/**`、记录型存储内既有条目；`docs/archive/**`、`docs/static/**`、`docs/notes/**` 按 L-4 的 dated 类扩展不改写。
- **plan-owned 面（仅小修）**: `plan.md`、`data-model.md`、`contracts/**`、`quickstart.md`、`research.md`、`feature-ref.md`。

## Measured Premises (re-measured at generation time 2026-11-25, HEAD `464ef0f04`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/105-runtime-store-layout/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **27 / 9 / 6**（2026-11-25 addendum 复测：FR-027、SC-009 已加入，既有 ID 未重编号） |
| 契约条款数（逐文件） | `grep -cE '^## [CMPL]-[0-9]+' .specify/specs/105-runtime-store-layout/contracts/*.md` | store-layout **8**（C-1…C-8）/ migrate **10**（M-1…M-10）/ memory **6**（P-1…P-6）/ live-refs **8**（L-1…L-8）；合计 **32**。**陷阱形**：`grep -c 'C-'` 会把正文引用一起算入，计量单位是行首 `##` 条款定义行 |
| 机器可判定条款形式 | `/usr/local/bin/python3 .specify/scripts/python/clause_extract.py .specify/specs/105-runtime-store-layout/contracts/*.md` | 仅 `store-layout.contract.md` 为 `form=md-heading clauses=8`；其余三份 `form=md-none clauses=0`（M / P / L 前缀不属 clause-syntax owner 的 C- 形式；新增 M-10 不改变该形式） |
| 计划工作包计数 | `grep -cE '^\| WP[0-9]+' .specify/specs/105-runtime-store-layout/plan.md` | **15**（WP01…WP15）；FR-027/SC-009 由 WP12/WP15 承载，未新增 WP |
| 不兼容变更清点计数 | `grep -cE '^\| BC[0-9]+' .specify/specs/105-runtime-store-layout/plan.md` | **18**（BC01…BC18：14 迁移 + 容器 + `draft` + 种子命名空间 + 维度集扩展） |
| quickstart 场景数 | `grep -c '^## Scenario' .specify/specs/105-runtime-store-layout/quickstart.md` | **9**（S-0…S-8） |
| 9 个新文件当前状态 | 逐个 `test -e`（3 个 contract 测试 + 5 个 integration 测试 + 1 个 fixture builders） | 9/9 **ABSENT**（红先的前提） |
| 编辑目标与守卫在位 | 逐个 `test -e`（`src/specify_cli/__init__.py`、`shared/declarations/{contract.yaml,facts/memory-types.yaml,facts/non-disposable-review-surface.yaml,exclusions/no-machine-fact.yaml}`、`shared/definitions/framework-map.md`、`scripts/python/*` 17 个引擎 + `scripts/bash/create-new-tools.sh`、`templates/commands/migrate.md`、三份 ignore 模板、`.specify/.gitignore`、`pyproject.toml`、`memory/` 包内种子、`.specify/instructions.md`、`.specify/glossary.md`、`tests/contract/test_migrate_engine_contract.py`、`tests/unit/test_migrate_planner.py`） | 21/21 **OK**；`.specify/tools/` **ABSENT**（生成清单尚未生成）；包内种子 `memory/` 4 条目（`constitution.md`、`features.md`、`session/`、`knowledge/`） |
| 基线存储清点 | `git ls-tree -d 23938f22e:.specify/memory`；`git ls-tree -r --name-only 23938f22e .specify/memory \| wc -l` | **12** 个子目录（coaching evidence exec-quant feedback housekeeping knowledge renumber retention session todo tools trigger）；基线受跟踪路径 **2,963**；当前工作树 `git ls-files .specify/memory \| wc -l` = **2,975**（plan/research 记 2,971 是当时快照，属 dated 读数） |
| 测试活引用载体数 | `grep -rl '\.specify/memory' tests/ \| wc -l` | **92**（research R-2.5 计划期记 89——实现时 MUST 重新执行本命令并按 L-3 分类全部命中，不得把任一计数当契约） |
| 镜像与副本基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | `sync-mirrors` rc **2**、**450 DIFF**、0 MISS / 0 ORPHAN；`regen` rc **0**（`OK: all per-tool command copies match the source templates.`） |
| 忽略规则现状 | `git check-ignore -v .specify/memory/sanitize/findings.json .specify/memory/trigger/telemetry.jsonl .specify/tools/system.json` | `.specify/.gitignore:23:memory/sanitize/`、`:27:memory/trigger/telemetry.jsonl`、`:16:tools/`（三处均需在同一变更内改到新路径 / 收窄） |
| 条款覆盖基线 | `/usr/local/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/105-runtime-store-layout --freeze > .specify/specs/105-runtime-store-layout/coverage-baseline.txt` | 已冻结：**787** 行、`base-sha: 464ef0f045c4`、`files: 322 (parsed 214 + named 108)` |
| 条款覆盖改后读数（生成时） | `/usr/local/bin/python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/105-runtime-store-layout` | `claimed clauses 8`；`clause-uncovered pass (785) — 0 beyond the frozen baseline`；`coverage-baseline-delta pass (0)`；`fr-uncovered fail (21) — 6 of 27 FRs cited from citation groups`（三份契约 `form=md-none` 的结构事实，FR-027 不落在任何 C 条款 citation group；按 DoD-3 / GATE-3 如实报告、不作通过判据）；FR universe **27**（2026-11-25 addendum 复测） |
| flow-class 判定 | `python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:105-runtime-store-layout"` | `flow_class: execution`、`source: declaration`、rc **0** |

## Requirement Coverage Map

| FR | 承载任务行 | SC | 承载任务行 |
|----|------------|----|------------|
| FR-001 | T002、T003、T007 | SC-001 | T002、T007、T009、T032、T033、T038 |
| FR-002 | T003、T012、T013 | SC-002 | T017、T020、T038 |
| FR-003 | T003、T012、T022 | SC-003 | T018、T020、T038 |
| FR-004 | T007、T013、T032 | SC-004 | T011、T016、T035、T036、T038 |
| FR-005 | T003、T007 | SC-005 | T006、T009、T038 |
| FR-006 | T019、T020 | SC-006 | T025、T032、T038 |
| FR-007 | T017、T019、T020 | SC-007 | T031、T032、T038 |
| FR-008 | T018、T019、T020 | SC-008 | T021、T024、T038 |
| FR-009 | T026、T028、T030 | | |
| FR-010 | T018、T020 | | |
| FR-011 | T018、T019、T020 | | |
| FR-012 | T018、T040 | | |
| FR-013 | T012、T015 | | |
| FR-014 | T013 | | |
| FR-015 | T012、T014 | | |
| FR-016 | T014、T033 | | |
| FR-017 | T008、T009 | | |
| FR-018 | T004、T005、T026 | | |
| FR-019 | T008 | | |
| FR-020 | T023 | | |
| FR-021 | T007、T030 | | |
| FR-022 | T031 | | |
| FR-023 | T028、T029、T040 | | |
| FR-024 | T002、T011、T017、T018、T021、T025、T035 | | |
| FR-025 | T002、T019 | | |
| FR-026 | T020、T033、T037、T039 | | |
| FR-027 | T016、T042、T043 | SC-009 | T016、T042、T043 |

**SC 路径读数**：SC-001…SC-005 与 SC-009 为 `final`；SC-006…SC-008 为 `supporting`（owner：`requirements.md` § Success Criteria）。supporting 判据按其实测基线报告，不冒充 final 门禁。

## Work Package → Task Map (15/15 preserved)

| WP | 任务行 | WP | 任务行 |
|----|--------|----|--------|
| WP01 | T002、T003、T007 | WP09 | T015 |
| WP02 | T004、T005 | WP10 | T026、T027、T028、T030 |
| WP03 | T017、T018、T019、T020 | WP11 | T031、T032 |
| WP04 | T021、T022、T024 | WP12 | T002、T011、T017、T018、T021、T025、T032、T035、T042 |
| WP05 | T006、T008、T009 | WP13 | T010、T034、T035 |
| WP06 | T021、T023、T024 | WP14 | T033 |
| WP07 | T010、T011、T012、T016 | WP15 | T037、T038、T039、T040、T041、T043 |
| WP08 | T013、T014、T016 | | |

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结后续「零丢失、零新增漂移、行为保持」判据的对照物——implement 起点的可比较分母。

- [X] T001 捕获 implement 起点基线并创建证据落点：创建 `.specify/specs/105-runtime-store-layout/notes/`，把 `git rev-parse --short HEAD`、`git status --short`、`git ls-tree -d 23938f22e:.specify/memory`（期望 12）、`git ls-files .specify/memory | wc -l`、`grep -rl '\.specify/memory' tests/ | wc -l`、`python3 scripts/python/sync-mirrors.py --check`（期望 rc 2 / 450 DIFF）、`python3 scripts/python/regen-command-copies.py --check`（期望 rc 0）与 `account-clause-coverage.py --freeze` 的重采读数连同命令、真实输出和日期写入 `.specify/specs/105-runtime-store-layout/notes/pre-change-measurements.md`；全量套件名字级基线按 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 在 implement Step 0 捕获，本行只留指针、不复述比较形式；本行不写任何产品文件。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 单一机器声明与引擎根常量——所有用户故事的共同前置；声明缺失时消费者只允许 `owner-unavailable` 降级，不得持有第二份根清单。

**⚠️ CRITICAL**: US1–US6 的引擎、迁移、记忆、工具与镜像工作都以本阶段为前置。

- [X] T002 [blockedBy: T001] 红先编写 `tests/contract/test_runtime_store_layout.py`：per `contracts/store-layout.contract.md` C-1/C-3/C-5/C-6 与 plan § Test-First Coverage 写具名函数 `test_inventory_is_closed`（基线 12 子目录 + 引擎按需 `sanitize`、`migrate/receipts` + 遗留 `draft` / `git-workflow.md` + 容器本身，各恰一次处置）、`test_declaration_equals_inventory_and_consumer_sets`（声明成员 = 需求清点表 = 代码消费者集）、`test_framework_map_rows_and_tombstone`（14 行 + 墓碑行）、`test_repo_has_no_retired_root`（dogfood 前红）、`test_mirror_member_set`（相对 450-DIFF 基线无新增成员）、`test_two_writers_distinct_paths`（每个新存储的两写入者模拟，FR-025）；作者时断言必须失败；以唯一入口跑并写入 `notes/red-first-evidence.md`。
- [X] T003 [blockedBy: T002] 创建 `shared/declarations/facts/runtime-store-layout.yaml`（kind `mapping`：14 个 store 的 `{lifecycle, owner, content_class, non_content, seeded}`、`retired_container: .specify/memory`、`legacy_non_store: [git-workflow.md]`、`legacy_retired: [draft]`、`consumers`、`former_carriers`；路径只作投影）并在 `shared/declarations/contract.yaml` 注册后才允许消费者读取；MUST NOT 写入 `.specify/glossary.md` 的 Runtime Store 词条（A-16 确认门前只留 run 证据）。 [green: contracts/store-layout.contract.md#C-1]
- [X] T004 [P] [blockedBy: T003] 把单存储引擎的根常量更新到 `.specify/<store>/`：`scripts/python/memory-utils.py`、`feedback-utils.py`、`evidence-utils.py`、`exec-quant.py`、`run-determination.py`、`trigger-utils.py`、`probe-utils.py`、`record-retention.py`、`role-edge-check.py`、`anchor-layout-migrate.py`（后者保留 legacy anchor reader 语境）；条目格式、写入协议与消费语义零修改（FR-025）。
- [X] T005 [P] [blockedBy: T003] 把跨存储枚举消费者改为经 `scripts/python/declaration_reader.py` 读声明：`scripts/python/sanitize-utils.py`、`renumber-utils.py`、`seal-utils.py`、`concurrency-check.py`、`non-disposable-check.py`；同步 `shared/declarations/facts/non-disposable-review-surface.yaml` 的成员集（自有闭集，守卫断言与声明相等）与 `shared/declarations/exclusions/no-machine-fact.yaml` 注释；声明缺失时只用 reader 的 `absent_label`，不得发明回退清单。

---

## Phase 3: User Story 1 - 打开 `.specify/` 就能看懂每个存储属于谁、memory 只意味着记忆 (Priority: P1) 🎯 MVP

**Goal**: 14 个顶层存储各有唯一 owner 与生命周期行；退役根只以墓碑行存在；全新初始化种出两个记忆存储且不创建旧根；本仓「旧根不存在」由 US5 的 dogfood 收口。

**Independent Test**: `tests/contract/test_runtime_store_layout.py` 的清单 / 声明 / 地图 / 墓碑函数与 `tests/integration/test_init_new_layout.py` 全绿（允许残余：`test_repo_has_no_retired_root` 与 `test_mirror_member_set` 待 US5）；`find <fresh>/.specify -maxdepth 1` 只出现新存储。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T006 [US1] [blockedBy: T001] 红先编写 `tests/integration/test_init_new_layout.py`：空目录夹具上 `specify init --here --ai qoder --script sh --no-git` 后断言 `.specify/session/` 与 `.specify/knowledge/` 存在、`.specify/memory/` 不存在、其余存储懒创建、核心资产清单为新两项、锚点仍在 `.specify/` 根；以唯一入口跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [X] T007 [P] [US1] [blockedBy: T003] 在 `shared/definitions/framework-map.md` 为 14 个顶层存储各写一行（owner / 生命周期 / 内容类别，指针到 owner 文档而非复述规则），并把 `.specify/memory/` 写成唯一墓碑行（A-2 措辞：历史 catch-all 桶；已退役；agent 语境记忆由 `.specify/session/` 与 `.specify/knowledge/` 承载；任何引擎 MUST NOT 视其为活存储）。 [green: contracts/store-layout.contract.md#C-2] [green: contracts/store-layout.contract.md#C-3]
- [X] T008 [US1] [blockedBy: T003] 落地包内种子与 init 播种：包内 `memory/` 改名为 `seed/`（保留两个锚点与 `session/`、`knowledge/` 占位）；`pyproject.toml` force-include 同步；`src/specify_cli/__init__.py` 的 `copy_local_templates` 播种 `.specify/session/` + `.specify/knowledge/` 且不创建 `.specify/memory/`、`_CORE_SPECIFY_ASSETS` 以两记忆 tier 替换 `.specify/memory` 项、`rewrite_paths()` 移除通用 `memory` 段与 `memory/<anchor>` 特例、`migrate_placeholder_dir()` 指向种子目录、`features_dir` 注释修正；检测到旧内容时原地保留并指向 `specify migrate`（C-7，FR-013 执行者裁定；FR-017、FR-019）。
- [X] T009 [US1] [blockedBy: T006,T007,T008] US1 转绿与取证：以唯一入口运行 `tests/integration/test_init_new_layout.py` 与运行 `tests/contract/test_runtime_store_layout.py`——清单 / 声明 / 地图 / 墓碑函数全绿，允许残余失败只限 `test_repo_has_no_retired_root` 与 `test_mirror_member_set`（待 US5）；逐函数结果与 init 树清单写入 `notes/red-first-evidence.md`（FR-017）；C-7 的 `[green:]` 归 T038（全新初始化的最终绿以 SC-005 实测读数收口）。

**Checkpoint**: US1 独立可验——声明、地图、墓碑与全新初始化成立；旧根缺失与镜像读数的收口在 US5 的 dogfood / 再生成之后。

---

## Phase 4: User Story 2 - 既有客户项目升级不丢数据，冲突时大声拒绝 (Priority: P1) 🎯 MVP

**Goal**: 仅旧布局的内容零丢失地移到新根（逐字节一致）；旧新并存确定性命名为 `dual-content` 并点名两侧；重跑为幂等 no-op；dry-run 全程零写入；回执逐 run 一文一件（v2）。

**Independent Test**: `tests/integration/test_store_layout_migration_us1_us2.py` 的三形态夹具（legacy / seeded-legacy / dual / rerun）全绿；`specify migrate` dry-run 后 `git status` 无新增写入。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T010 [US2] [blockedBy: T003] 编写 `tests/fixtures/store-layout-105/builders.py`：由声明构建 `build_legacy`（每个 store 至少一条权威条目 + `.gitkeep` + 一件生成物，无新根）、`build_seeded_legacy`（legacy 后跑 `specify init`）、`build_dual`（同一 store 两侧权威内容）、`build_rerun`（成功后重跑）；夹具在 `tmp_path` 或 `.specify/.tmp/` 生成，不写历史快照。
- [X] T011 [US2] [blockedBy: T010] 红先编写 `tests/integration/test_store_layout_migration_us1_us2.py`：dry-run 零写入（sentinel 目录 + `git status` 对比）；`--apply` 逐字节移动（`diff -r`）；旧根移除；回执 v2 每 run 一文一件；`build_dual` 拒绝并点名两侧路径与修复入口且两侧哈希不变；`build_rerun` 为 `clean`、零移动、不重建旧根；以唯一入口跑并把红读数写入 `notes/red-first-evidence.md`。

### Implementation for User Story 2

- [X] T012 [US2] [blockedBy: T003,T004,T005] 规划器：在 `src/specify_cli/__init__.py` 的 `MIGRATE_DIMENSIONS` 末尾追加 `store-layout`（原五 token 保持有序前缀），实现 M-2 状态判定表与 M-3「仅权威条目计冲突」谓词（生成物 / 占位不计入；新侧同路径条目保留、不覆盖、不删除；旧侧重复项按 M-3 记录路径+摘要后作废移除；本 run 自身回执不算新侧内容）、M-2 rule 9 / M-4 step 5 的容器遍历终态（未认领路径一律 `unknown-residue`、容器保留、结局 `blocked`）、M-9 结局映射；把两个 097 维度 pin 测试（`tests/contract/test_migrate_engine_contract.py`、`tests/unit/test_migrate_planner.py`）改为「前缀相等 + 六 token 全集」守卫，097 的 dated E-8 不改写。
- [X] T013 [US2] [blockedBy: T012] 执行器核心：每个 archive item 先写 `entries[]` manifest（relpath / class / digest / from→to / status）再逐条 `shutil.move`，不向 `.specify/archive/migrate/` 复制字节；digest 复核、`left-in-place` 报告、`recover[]` 逆序恢复行、容器空残留移除；回执 v2（`receiptVersion=2`、`storeLayout` 摘要、逐 run `O_EXCL`）；幂等重跑 no-op（M-4 / M-6；FR-014、FR-016）。
- [X] T014 [US2] [blockedBy: T013] 执行器失败面：`symlink-source` / `symlink-target`、`path-collision:<relpath>`、`permission-denied`、`unknown-residue`（逐个列出并保留）、`no-recovery-path` → `blocked`；OSError / digest 失配 → `failed` + `aborted`，已移动条目保留并按回执续跑；MUST NOT 静默跳过任何 refuse / blocked 项（M-5 / M-6；FR-014、FR-015、FR-016）。
- [X] T015 [US2] [blockedBy: T014] 迁移命令面：`templates/commands/migrate.md` 增加第六维与回执存储文案；`docs/reference/commands/migrate.md` 同步维度 / 回执 / 恢复字段；编辑模板后以 `scripts/python/regen-command-copies.py` 再生成四份逐工具副本（`.github/prompts/`、`.claude/commands/`、`.qoder/commands/`、`.opencode/command/`），MUST NOT 手改副本。
- [X] T016 [US2] [blockedBy: T011,T012,T013,T014,T015] US2 转绿与取证：以唯一入口跑 `tests/integration/test_store_layout_migration_us1_us2.py`、`tests/contract/test_migrate_engine_contract.py`、`tests/unit/test_migrate_planner.py`；在同一夹具上记录 dry-run 零写入、逐字节比较、dual 拒绝与 rerun no-op 的读数（含结局 token 与回执路径）写入 `notes/red-first-evidence.md`。

**Checkpoint**: US2 独立可验——三形态迁移安全成立；第六维复用既有 plan → apply → archive-first → 回执结构，未新建第二迁移引擎。

---

## Phase 5: User Story 3 - 临时记忆与上下文注入在新路径下行为不变 (Priority: P1) 🎯 MVP

**Goal**: `record` / `recall` / `list` / `prune` / `reindex` 与 `--scope all` 语义不变；两个 tier 的写入落在 `.specify/session/` 与 `.specify/knowledge/`；`run-determination` 判定记录仍经记忆引擎落 session；派发载荷七字段 / 四项注入 / 五要素不变，注入来源只解析到两个记忆存储；运行期存储文本不被记忆召回。

**Independent Test**: `tests/integration/test_memory_preservation.py` 与 `tests/integration/test_dispatch_injection_paths.py` 全绿；反向夹具证明 feedback / exec-quant 中的 token 不被记忆召回。

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T017 [US3] [blockedBy: T003] 红先编写 `tests/integration/test_memory_preservation.py`：session 与 knowledge 各一次 record→recall（条目文件落在新根、内容一致、upsert-by-slug 保留）；`prune` 的年龄 / 数量界与 `reindex` 的既有语义；`run-determination.py --action determine` 经 memory 引擎落 `.specify/session/` 且 `--action history` 可检索、schema 键与迁移前相等；以唯一入口跑并把红读数写入 `notes/red-first-evidence.md`。
- [X] T018 [US3] [blockedBy: T003] 红先编写 `tests/integration/test_dispatch_injection_paths.py`：派发夹具（child 声明 `memory-recall` + 预置 session 条目）断言七字段下行 / 四项注入 / 五要素上行齐备、注入的全部记忆引用解析到 `.specify/session/` 或 `.specify/knowledge/`、无第二注入源；反向夹具把唯一 token 只写入 feedback 与 exec-quant，`--action recall` 不返回该 token；结构断言无新载荷字段、无新检索来源（P-3 / P-4）；以唯一入口跑并把红读数写入 `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [X] T019 [US3] [blockedBy: T003,T004] 记忆面接线：`scripts/python/memory-utils.py` 经 `declaration_reader.py` 解析两个 tier 根（scope 名与动作闭集不变）；`skills/internal/memory-record/SKILL.md` 与 `skills/internal/memory-recall/SKILL.md` 的路径与检索边界文本更新到新根；`scripts/python/run-determination.py` 的持久化适配器路径说明更新；`shared/declarations/facts/memory-types.yaml` 的路径注记更新；MUST NOT 改名 scope、MUST NOT 增加动作或第二记忆源（FR-006、FR-007、FR-011）。
- [X] T020 [US3] [blockedBy: T017,T018,T019] US3 转绿与取证：以唯一入口跑 `tests/integration/test_memory_preservation.py` 与 `tests/integration/test_dispatch_injection_paths.py`；把 record→recall 往返、determination 持久化与召回、注入来源路径清单、反向 token 不返回四组读数写入 `notes/red-first-evidence.md`（FR-008、FR-010、FR-012）。

**Checkpoint**: US3 独立可验——用户点名的「临时记忆系统」与「super agent→sub agent 动态注入」在新根上行为一致，且记忆边界可反向验证。

---

## Phase 6: User Story 4 - Tool 记录与生成清单一处共存，受跟踪与忽略各归其位 (Priority: P2)

**Goal**: `.specify/tools/` 同时容纳受跟踪的 `<name>.md` 记录与被忽略的 `{system,shell,project}.json` 清单；`.specify/.gitignore` 的 `tools/` 全目录忽略收窄为 `tools/*.json`；`sanitize/` 与 `trigger/telemetry.jsonl` 规则改到新路径；框架模板与已安装副本逐字节一致；claude / codex ignore 模板放行新存储根。

**Independent Test**: `tests/contract/test_tools_domain.py` 与更新后的 `tests/contract/test_specify_gitignore_template.py` 全绿；`git check-ignore -v` 只命中生成物、`git ls-files .specify/tools` 只列记录。

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T021 [US4] [blockedBy: T001] 编写 `tests/contract/test_tools_domain.py` 并扩展 `tests/contract/test_specify_gitignore_template.py`：`.specify/tools/` 下 `*.md` 被跟踪、`*.json` 被忽略、同基名 `X.md` / `X.json` 可共存且互不覆盖；`templates/gitignore-specify-template` 与 `.specify/.gitignore` 逐字节一致并含 `tools/*.json`、`sanitize/`、`trigger/telemetry.jsonl`；claude / codex 模板含新存储根放行行；以唯一入口跑并把红读数写入 `notes/red-first-evidence.md`。

### Implementation for User Story 4

- [X] T022 [US4] [blockedBy: T003,T005] tools 域实现：`scripts/python/tools-utils.py` 与 `skills-utils.py` 的记录路径改到 `.specify/tools/`；`scripts/bash/create-new-tools.sh` 与 `shared/definitions/tool-definitions.md` 同步；`scripts/python/sanitize-utils.py` 移除已反转语义的 `legacy-tools-registry` 检查并把 MATERIAL_ROOTS 的 legacy registry 项改为 tools 域（M-7）；定义记录仍受跟踪、清单仍由原 owner 生成。
- [X] T023 [US4] [blockedBy: T022] 忽略面：`templates/gitignore-specify-template` 与 `.specify/.gitignore` 同变更更新（`tools/` → `tools/*.json`、`memory/sanitize/` → `sanitize/`、`memory/trigger/telemetry.jsonl` → `trigger/telemetry.jsonl`、注释里的 `memory/tools/` → `.specify/tools/`）且逐字节一致；`templates/claudeignore-template` 与 `templates/codexignore-template` 的 `!.specify/memory/` 放行改为 14 个新存储根的放行集。 [green: contracts/store-layout.contract.md#C-4]
- [X] T024 [US4] [blockedBy: T021,T022,T023] US4 转绿与取证：以唯一入口跑 `tests/contract/test_tools_domain.py` 与 `tests/contract/test_specify_gitignore_template.py`；在夹具上执行 `git check-ignore -v`、`git ls-files .specify/tools` 与 `cmp` 模板 / 已安装副本，读数写入 `notes/red-first-evidence.md`。

**Checkpoint**: US4 独立可验——唯一「记录 vs 生成物」混居目录的忽略与跟踪各归其位，模板与副本一致。

---

## Phase 7: User Story 5 - 仓库自身（dogfood）完成迁移且镜像零漂移 (Priority: P2)

**Goal**: 本仓的活引用面全部指向新根（允许集之外零 `.specify/memory/`）；镜像与逐工具副本同变更再生成且相对基线无新增漂移；本仓用同一 `specify migrate --apply` 完成 dogfood，旧根消失、`git log --follow` 可追溯、回执 v2 逐 run 留存。

**Independent Test**: `tests/contract/test_store_layout_live_refs.py` 与 `tests/contract/test_runtime_store_layout.py::test_repo_has_no_retired_root` 全绿；`test ! -e .specify/memory`；`sync-mirrors --check` 无新增漂移成员、`regen --check` rc 0。

### Tests for User Story 5 (MANDATORY) ⚠️

- [X] T025 [US5] [blockedBy: T003] 红先编写 `tests/contract/test_store_layout_live_refs.py`：按 `contracts/live-reference-migration.contract.md` L-5 计算三类产物面的旧根字面量出现文件集并与声明的四文件允许集双向相等；逐允许文件断言命中行满足其 allowed-line 规则；测试内允许集字面量与契约表相等（钉住副本）；声明四个变异演练（搬入未列文件 / 未列行，各双向）在 `test-evidence/mutation-drill.md` 留位；以唯一入口跑并把红读数写入 `notes/red-first-evidence.md`。

### Implementation for User Story 5

- [X] T026 [P] [US5] [blockedBy: T005,T015,T022] 框架源活引用重写：`shared/**`（R-2.1 的 22 文件：definitions / workflow / guidelines / patterns / declarations）、`skills/**`（38 文件 + 2 个 `mechanism-inventory.py`）、`agents/sdd-debt-governor.agent.md` 与 `scripts/**` 的剩余活字面量按 L-1 机械映射重写；墓碑行、退役根声明、`anchor-layout-migrate.py` 与 `sanitize-utils.py` 的 legacy 语境保持原样；dated record 零改写（FR-018）。
- [X] T027 [P] [US5] [blockedBy: T015,T022] 模板活引用重写：`templates/commands/{tools,todo,sanitize,review,migrate,interview,instructions,improve,feedback}.md`、`templates/instructions-template.md`、`templates/tools.md` 按 L-1 更新，保留 T015 已落的第六维与回执文案；不手改任何逐工具副本。
- [X] T028 [P] [US5] [blockedBy: T015,T022] 现行文档重写：`docs/**` 的 19 个活页面（R-2.3）逐路径更新；`docs/reference/skills/memory.md` 重写为两个顶层 tier 并声明 memory 只是系统名；`docs/concepts/spec-driven.md` 的陈旧 feature-registry 位置修为 `.specify/features/`；`docs/reference/history/**`、`docs/decisions/**`、`docs/archive/**`、`docs/static/**`、`docs/notes/**` 零改写。
- [X] T029 [P] [US5] [blockedBy: T003] 测试活引用分类与更新：重新执行 `grep -rl '\.specify/memory' tests/`（当前读数 92，不得当契约），按 L-3 / R-2.5 逐文件分类——live-target 改到新根、legacy-fixture 保留并限定在 `tests/fixtures/migrate-097/`、`tests/fixtures/store-layout-105/`、anchor-layout / sanitize-legacy / upgrade-end-state 的显式集合、stale 修复到现行权威路径；`tests/fixtures/migrate-097/` 的布局前提同步更新；新守卫文件与 `tests/contract/test_runtime_store_layout.py` 属于声明的 guard 集合，不算 stale 载体。
- [X] T030 [US5] [blockedBy: T027] 运行期指南：由生成器从 `templates/instructions-template.md` 再生成 `.specify/instructions.md`（不手改）；手工更新 `.specify/glossary.md` 的七个活条目（`Memory Layer`、`Session(消歧)`、`三捕获机制`、`自省报告`、`Evaluation Form`、`Renumber Lane`、`Coaching Run`）到新路径；A-16 的 Runtime Store 词条仍只留 run 证据、不写入 glossary（FR-009）。 [green: contracts/store-layout.contract.md#C-5]
- [X] T031 [US5] [blockedBy: T026,T027,T028,T029,T030] 再生成镜像与命令副本：`python3 scripts/python/sync-mirrors.py --write` 收敛本特性触及的 scope 后 `--write --check` 复核；`python3 scripts/python/regen-command-copies.py` 再生成全部逐工具副本并 `--check` rc 0；断言触及镜像对逐字节一致、`sync-mirrors --check` 的漂移成员集相对 450-DIFF 基线无新增成员（scope 治愈按差值记录）；MUST NOT 手改镜像面（FR-022）。
- [X] T032 [US5] [blockedBy: T031] 守卫收口：以唯一入口运行 `tests/contract/test_store_layout_live_refs.py` 与运行 `tests/contract/test_runtime_store_layout.py`——声明 = 清点 = 消费者集、地图 / 墓碑、镜像成员集与「本仓无退役根」全部成立；逐函数结果与允许集读数写入 `notes/red-first-evidence.md`。 [green: contracts/store-layout.contract.md#C-6]
- [X] T033 [US5] [blockedBy: T031,T024] dogfood：以 `PYTHONPATH=src /usr/local/bin/python3 -c "from specify_cli import main; main()" migrate --workspace . --apply` 迁移本仓；断言每个 store 的 manifest 与回执（v2、逐 run 一文一件）在位、`.specify/memory/` 不存在、受跟踪条目全部在新根、`git log --follow` 可追溯、二次 apply 为 `clean` 零移动；把命令、真实输出、回执路径与 `git log --follow` 摘录写入 `test-evidence/dogfood.txt`。

**Checkpoint**: US5 独立可验——本仓与框架源同时收敛；活引用允许集双向相等、镜像无新增漂移、旧根消失。

---

## Phase 8: User Story 6 - 半迁移与不可迁移状态被诚实报告，不被当作成功 (Priority: P3)

**Goal**: 旧位置未知残留、符号链接、只读目标与迁移中断四类状态都以点名路径的拒绝或续跑收束；不猜、不合并、不清空、不以「新建空存储」冒充成功。

**Independent Test**: `tests/integration/test_store_layout_migration_us3_us6.py` 的 residue / symlink / readonly / partial 四夹具读数；两个变异演练使对应断言转红。

> 本阶段是 migration/regression 例外：断言守的是 T014 已交付的执行器行为，故置于实现之后；红能力由变异演练证明，不冒充红先。

- [X] T034 [US6] [blockedBy: T010,T014] 扩展 `tests/fixtures/store-layout-105/builders.py`：新增 `build_residue`（legacy + `draft/` + stray `git-workflow.md`）、`build_symlink`（一个 store 符号链接）、`build_readonly`（目标父目录只读；root 运行记平台事实并跳过）、`build_partial`（中断 apply：回执 `running`、半数条目已移、digest 一致）。
- [X] T035 [US6] [blockedBy: T034,T014] 编写 `tests/integration/test_store_layout_migration_us3_us6.py`：residue 夹具上 store items 收敛、容器保留、每个残留路径被列出且零删除；symlink 夹具拒绝并点名路径、链接未动；readonly 夹具 `permission-denied` 且无部分成功；partial 夹具续跑只移余量、无重复条目、已移条目无第二份 archive 记录；每个断言配对一条变异说明（删冲突检查 / 删残留列举 / 重移已移条目），以唯一入口跑并记录读数。
- [X] T036 [US6] [blockedBy: T035] US6 转绿与变异演练：执行两个变异（① 删除 `dual-content` 冲突检查 → US2 dual 断言转红；② 取消 `unknown-residue` 列举 → residue 断言转红），逐项复原并转绿；红 / 绿读数写入 `test-evidence/mutation-drill.md`，与 T025 的活引用演练合并呈现。

**Checkpoint**: US6 独立可验——最坏结局（「迁移成功但数据消失」）被排除，失败形态可复现、可点名、可续跑。

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实跑、逐 SC 的验收证据包、非目标审计与最终门禁——跨故事、不可提前的收尾面；FR-027/SC-009 的清点守卫与证据（2026-11-25 用户追加要求）在本阶段追加，不新增 WP。

- [X] T037 [blockedBy: T033,T036] quickstart 实跑记录：执行 `quickstart.md` S-0 的三条基线命令与 S-7 的 dogfood 复核命令并贴真实输出；S-1…S-6、S-8 是 route-b 场景，逐条指向其钉住测试并声明该读法；落盘 `notes/quickstart-run.md`（含 teardown：只删除 `.specify/.tmp/quickstart-105/` 自建目录）（FR-026）。
- [X] T038 [blockedBy: T037] 验收证据包：写 `test-evidence/acceptance-105.md` 逐条记录 SC-001…SC-008 的状态、测量命令、真实输出与证据指针（SC-001 的基线 `git ls-tree` 与迁移后 `test ! -d`、SC-004 的三形态读数、SC-006 的允许集双向读数、SC-007 的成员集差值、SC-008 的 `git check-ignore` 夹具）；final / supporting 路径标注与 `requirements.md` 一致；SC-009 行由 T043 追加（C-7 的机器绿以本行记录的 SC-005 实测读数收口）。 [green: contracts/store-layout.contract.md#C-7]
- [X] T039 [blockedBy: T038] `verification.md`：写逐 SC 状态行（SC-001…SC-005 `pass`，SC-006…SC-008 按实测 supporting 读数；SC-009 的 final pass 行与 smoke 记录由 T043 追加）、`smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（指向存在的证据文件）与 `deferred_tasks=`（无 `[~]` 时为空）；不伪造未测读数。
- [X] T040 [blockedBy: T032,T033] 非目标与零第二机制审计：断言零新增存储引擎 / 注册表 / 调度器 / 第二上下文注入机制、零新增第三方依赖（`pyproject.toml` 未新增 runtime 依赖）、条目格式与写入协议不变（055 协议）、`draft/` 无新家、`git-workflow.md` 未改写；把命令、真实输出与结论写入 `test-evidence/non-goals-audit.md`。 [green: contracts/store-layout.contract.md#C-8]
> FR-027/SC-009 与 plan § Backward-Incompatible Change Inventory 是 2026-11-25 的用户追加要求（记录见 `requirements.md` § Clarifications 末节）：T042 / T043 以新 ID 追加、既有任务不重编号；最终门禁 T041 排在其后执行，以覆盖新增守卫与证据。
- [X] T042 [blockedBy: T016] FR-027/SC-009 清点守卫（migration/regression 例外）：在 `tests/contract/test_runtime_store_layout.py` 增加 `test_backward_incompatible_inventory_is_closed`——按 plan § Backward-Incompatible Change Inventory 断言（a）Store Inventory 中处置为 relocate / retire / retired-container 的行各被恰好一条 BC 行引用（集合 {#1…#15, #17}）；（b）每行 behavior ∈ 闭集 `migrate:relocate` / `migrate:container-pass` / `migrate:refuse:<M-5 token>` / `compatibility-bridge` / `no-workspace-object`，且 refuse token 存在于 M-5 表；（c）每行证据指针解析到存在的测试路径、证据文件或任务 ID；（d）禁用词 `manual` / `docs-only` / `fallback` / `runtime-fallback` / `todo` 零出现；执行变异演练（删一行 / 把一条 behavior 改为禁用词）使测试转红并复原，读数写入 `notes/red-first-evidence.md`。
- [X] T043 [blockedBy: T042,T038,T039] SC-009 验收证据：把 T016 / T035 的迁移读数（每个 store 的 dry-run 零写入、`--apply` 逐字节移动、dual / residue 拒绝）与 T042 的守卫输出汇总为 `test-evidence/acceptance-105.md` 的 SC-009 行，并向 `verification.md` 追加 `SC-009` 的 final pass 行及 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（指向存在的证据文件）；不伪造未测读数。
- [X] T041 [blockedBy: T039,T040,T043] 最终门禁：以 `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh --names-out <failed-list-file>` 跑全量套件并与 implement 入口基线做 `comm -13`（既有红逐条点名、零新增）；`sync-mirrors.py --check` 成员集对比、`regen-command-copies.py --check`、`test_store_layout_live_refs.py`、`test_runtime_store_layout.py`（含 BC 清点守卫）、`test ! -e .specify/memory` 与 `grep -cE '^- \[[ >]\]' tasks.md` 逐项复验；命令与读数写入 `notes/red-first-evidence.md`。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖——T001 先落基线。
- **Foundational (Phase 2)**: 依赖 Setup；声明与引擎根常量完成后才允许任何故事的实现行；T004 / T005 可并行。
- **User Stories (Phase 3–8)**: 均依赖 Foundational；按 P1（US1 → US2 → US3）→ P2（US4 → US5）→ P3（US6）推进；跨故事的显式依赖由 `[blockedBy:]` 承载，不靠阶段顺序猜测。
- **Polish (Phase 9)**: 依赖全部用户故事与 dogfood 完成（镜像 / 副本再生成与全量套件必须在全部源编辑之后）。FR-027/SC-009 追加行把收尾顺序固定为 T038 → T039 → T042 → T043 → T041：T042 依赖 US2 的 T016，T043 依赖 T042 / T038 / T039，最终门禁 T041 在 T043 之后执行。

### User Story Dependencies

- **US1 (P1)**: Foundational 后即可开始；交付声明投影（地图 / 墓碑）与全新初始化。
- **US2 (P1)**: 依赖 US1 的声明（T003）与引擎根（T004/T005）；其夹具与测试不依赖 US3/US4。
- **US3 (P1)**: 依赖 US1 的声明与 T004 的引擎常量；与 US2 无写目标冲突（测试与引擎文件不同）。
- **US4 (P2)**: 依赖声明与 T005；其忽略面（T023）不触碰 US2 的迁移引擎。
- **US5 (P2)**: 依赖 US1–US4 的全部源编辑（T005 / T015 / T022）后再做活引用与镜像；dogfood（T033）必须在镜像再生成（T031）与 ignore 更新（T023）之后。
- **US6 (P3)**: 只依赖 T010 / T014 的夹具与执行器；测试为回归守卫（migration/regression 例外）。

### Within Each User Story

- 新行为测试先写并确认失败 → 实现 → 转绿取证；US6 的回归守卫按例外置于实现之后，红能力由变异演练证明。
- 同一文件的多行严格按行序串行：`src/specify_cli/__init__.py`（T008 → T012 → T013 → T014）、`shared/definitions/framework-map.md`（T007）、`scripts/python/sanitize-utils.py`（T005 → T022 → T026）、`tests/fixtures/store-layout-105/builders.py`（T010 → T034）、`tests/contract/test_runtime_store_layout.py`（T002 → T042）。
- 每个故事以 `**Checkpoint**` 收口，独立可验后再进入下一故事。

### Parallel Opportunities

- **Foundational**: T004（单存储引擎组）与 T005（跨存储消费者组）写目标逐文件不同，可并行。
- **US1**: T007（framework map）与 T008（seed / init）写目标不同，可并行。
- **US5**: T026（shared / skills / agents / scripts）、T027（templates）、T028（docs）、T029（tests）写目标互不相交，可并行；T030 依赖 T027，T031 依赖四者全部完成。
- 其余阶段零 `[P]`：同一 CLI 文件、共享证据 sink 或同一镜像面按行序串行。

---

## Parallel Example: User Story 5

```text
# T015 / T022 / T005 完成后，四个活引用面可同时开工：
Task: "共享源 / 技能 / agents / scripts 活引用重写（T026）"
Task: "模板活引用重写（T027）"
Task: "现行文档重写（T028）"
Task: "测试活引用分类与更新（T029）"

# 四者全部完成后：
Task: "运行期指南再生成与 glossary 更新（T030）→ 镜像 / 副本再生成（T031）→ 守卫收口（T032）→ dogfood（T033）"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 + US2 + US3**——三条同为 P1，且缺一不可：US1 只交付布局语义会让既有项目无处可去；US2 只交付迁移会失去「memory 只意味着记忆」的命名目标；US3 缺失则用户明令保留的临时记忆与动态注入在路径迁移中断裂。三者检查点各自独立可测，合起来构成可演示的最小增量。

1. 完成 Phase 1（Setup）与 Phase 2（Foundational）。
2. 完成 US1（声明投影 / 墓碑 / 全新初始化）→ 检查点验证（允许旧根缺失待 US5）。
3. 完成 US2（三形态迁移）→ 检查点验证。
4. 完成 US3（记忆 / 注入保持）→ 检查点验证（MVP 到此可演示）。
5. 依次完成 US4（tools / ignore）→ US5（活引用 / 镜像 / dogfood）→ US6（失败面守卫）。
6. Polish：quickstart 实跑 → 验收证据包 → verification → 非目标审计 → 最终门禁。

### Incremental Delivery

每一故事结束时其检查点独立可验、不破坏前序故事；镜像与逐工具副本只在全部源编辑完成后一次性再生成（T031）；dogfood（T033）是唯一的本仓数据搬迁点，成功后不再回写旧根。

---

## Notes

- [P] 任务 = 不同写目标、无未完成依赖；共享 sink（`notes/red-first-evidence.md`）不算并行面。
- Story 标签只用于用户故事阶段行，便于按故事追踪；Setup / Foundational / Polish 零 `[US` 标记。
- 契约条款分区：8 条机器可判定 C 条款各被一行 `[green:]` 认领；M / P / L 共 24 条以条款号引用（理由见 DoD-3），不声称机器可判定的全覆盖。
- FR-027/SC-009 的清点守卫（T042）按 migration/regression 例外以变异演练证明红能力，与 US6 同一纪律；它守的是 plan 的封闭清点与 T016 已交付的迁移行为，不冒充红先。
- 既有守卫的名字级基线由 `/speckit.implement` 的 Step 0 重采（owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs），本文件不复述比较形式。
- dated record 的旧路径提及是历史事实，不是活引用；活引用守卫的允许集是封闭的四文件，任何新增必须修订 `contracts/live-reference-migration.contract.md` L-5 与本文件 T025 的钉住副本。
- plan-owned 面无任务行主动编辑；若实现中确需小修，按 DoD-3 的同一披露纪律逐项声明；实质性改动停线回抛。
