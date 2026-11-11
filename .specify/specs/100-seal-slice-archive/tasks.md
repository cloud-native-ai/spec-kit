# Tasks: /speckit.seal — 分片归档步骤（Seal Slice Archive）

**Requirement ID**: 100
**Requirement Key**: 100-seal-slice-archive
**Related Feature**: 099 Speckit Seal（bind；本特性不新建 Feature 行，099 状态保持 `Ready for Review`）
**Input**: Design documents from `.specify/specs/100-seal-slice-archive/`
**Prerequisites**: requirements.md（28 FR / 10 SC / 5 STR / 5 条 Clarifications）、plan.md（8 个工作包 P1–P8、6 条 decision-tension T-001…T-006、11 条 Execution Premise EP-001…EP-011 全 verified、Mirror Obligations）、research.md（R-01…R-14）、data-model.md（E1–E10、V1–V14）、contracts/（3 文件 40 条款：C-101…C-116 / C-201…C-212 / C-301…C-312）、quickstart.md（S-1…S-6）、feature-ref.md（FR 28/28、SC 10/10）

**Tests Mode**: ON — 宪法 Principle IV "Test-First & Contract-Driven Implementation" 是 test-mandating 原则（"Critical flows MUST have automated regression coverage" / "Integration/contract tests MUST cover cross-service communication and external APIs"）；requirements 与 plan 亦显式要求 Tests Mode ON。`flow_class = execution`（`flow-class-check.py --action lookup --unit-id "spec:100-seal-slice-archive"` 于 2026-11-11 实测 → `flow_class: execution`，source: declaration），无表达类门禁增量。交付面是混合形态：Python 引擎与契约/集成测试走运行时断言；纯函数/工具（路径形态分类谓词、C-034 摘要、三组闭环算术、schema 校验）MUST 另有 `tests/unit/` 单元测试（宪法 Principle IV）；prose 载体（命令模板、internal 技能、owner 页、命令参考）走结构契约测试（文件与夹具树断言）。

**Tests**: MANDATORY。全部测试经唯一入口 `bash scripts/bash/run-tests.sh` 运行；红先读数落 `.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md`，运行读数落同目录 `test-evidence/`。守护既有行为的行（迁移/回归例外）落在其消费对象之后并带显式 `[blockedBy:]`。

**Organization**: 按 requirements.md 的 4 条用户故事分组（US1 / US2 / US3 为 P1，US4 为 P2），前置 Setup（基线冻结）与 Foundational（动作集与 manifest-aware 发现，阻塞全部故事），尾置 Polish。阶段顺序服从 plan.md § Execution Model 的依赖链 `P1 ∥ P5 → P2 → P3 → P4 → P7` 且 `P4 → P7`、`P5 → P7`、`P6 → P7`：US4（P2）先于 US3（P1），因为 US3 的流程接线与真实回合消费 US4 的边界不变量（manifest-aware 发现、owner 登记），且 074 真实回合按定义是最后一步（099 同型先例：其 Phase 5 为 US4、Phase 6 为 US3）。

## Phase Map

| Phase | Purpose | Rows | Stories / criteria |
|-------|---------|------|--------------------|
| 1 Setup | 冻结四类对照物（改前测量、条款覆盖基线、证据落点） | T001–T003 | all |
| 2 Foundational | 动作集 4→6、CLI 表面、manifest-aware 分片发现 | T004–T009 | blocks US1–US4；FR-008、FR-019、FR-021 |
| 3 用户故事 1（P1） | `archive-plan` / `archive-apply` 核心：移动、清单、原子批次 | T010–T021 | US1；SC-001 / SC-002 |
| 4 用户故事 2（P1） | 载体分类、活引用改写、日期化保持、台账与闭环算术 | T022–T032 | US2；SC-003 / SC-006 / SC-007 / SC-008 |
| 5 用户故事 4（P2） | 边界不变量：回滚、并发、单一机制、owner 原地修订 | T033–T037 | US4；SC-005 / SC-009 / SC-010 |
| 6 用户故事 3（P1） | 流程固化、命令/技能面、阻断态与 074 真实回合 | T038–T045 | US3；SC-004（回合同时满足 US1 的真实验收 SC-001） |
| 7 Polish | 全量对照、镜像/副本、quickstart、记录收尾 | T046–T053 | SC-001…SC-010 的 Measurement Sources |

**MVP scope**: US1、US2、US3 均为 P1 且缺一不可独立成值——只移动不改引用会制造悬空指针（US2 缺失），只做引擎不进 `/speckit.seal` 流程则下一条拆分 spec 仍会重复残留（US3 缺失）。按模板 MVP 规则，MVP 覆盖**全部三条 P1 故事**（Phase 3–4 与 Phase 6）。US4（P2）约束实现形态而非新增用户能力，与 MVP 同批交付、排在其边界被引用的 US3 之前（Phase 5）。

### Work-package map（plan.md § Execution Model 的行级投影，每包一主题、≤16 行）

| 包 | 主题 | 任务行 | 行数 | 写域（文件级） | 验收锚 |
|----|------|--------|------|----------------|--------|
| Setup | 基线冻结与证据落点 | T001–T003 | 3 | `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt` | 四类对照物可比较 |
| P1 | 动作集 4→6 与 CLI 表面 | T004–T006, T041 | 4 | `scripts/python/seal-utils.py`、`tests/contract/test_seal_engine_contract.py`、`tests/contract/test_seal_boundaries.py` | 契约 C-101、C-115；命令名集合不变 |
| P2 | manifest-aware 分片发现 | T007–T008, T035 | 3 | `seal-utils.py`（发现段）、`tests/contract/test_seal_merge_plan.py`、`tests/integration/test_seal_074_round.py`、`tests/fixtures/seal-archive/archived-pair/` | 契约 C-112；归档后同一分片集 |
| P3 | `archive-plan`：前置 + 分类 + 清单 | T010–T012, T015–T016, T022–T031 | 15 | `seal-utils.py`（plan/分类/清单段）、契约测试 `test_seal_archive_plan.py` / `test_seal_archive_manifest.py` / `test_seal_merge_apply.py`、`tests/unit/test_seal_archive_classify.py`、`tests/unit/test_seal_archive_manifest_math.py`、`tests/unit/test_seal_archive_schema.py`、`tests/fixtures/seal-archive/` 6 套夹具 | 契约 C-102…C-104、C-201…C-212、C-301…C-311 |
| P4 | `archive-apply`：两阶段 + 移动 + 改写 + 原子恢复 | T013–T014, T017–T020 | 6 | `seal-utils.py`（apply 段）、`tests/contract/test_seal_archive_apply.py`、`tests/integration/test_seal_archive_idempotency.py`、`tests/integration/test_seal_archive_round.py` | 契约 C-105…C-109；重命名对、零纯删除、`already-archived` |
| P5 | owner 原地修订 | T036 | 1 | `shared/definitions/non-disposable-definitions.md`、`shared/definitions/framework-map.md`、099 三份契约的 6 条条款 | 契约 C-113；处置词表仍四值 |
| P6 | 命令面与技能面 | T039–T040 | 2 | `templates/commands/seal.md`、`skills/internal/seal-artifact/SKILL.md`、4 份 per-tool 副本（生成）、`docs/reference/commands/seal.md` | 契约 C-114；`regen`/`sync --check` 零新增漂移 |
| P7 | 074 真实回合 | T033, T038, T042–T044 | 5 | `.specify/specs/074-goal-team-sdd-unification/`、`.specify/register.md`、`.specify/features/074-goal-team-sdd-unification.md`、`shared/definitions/sdd-routing-definitions.md` + 镜像、`tests/contract/test_sdd_compat_containment.py`、`tests/contract/test_sdd_diffusion.py`、`tests/integration/test_seal_archive_rollback.py`、`tests/fixtures/seal-archive/blocked-pair/`、`test-evidence/074-archive-round.txt` | 契约 C-107、C-110；SC-001/SC-002/SC-010 |
| P8 | 收尾验证与记录 | T009, T021, T032, T034, T037, T045, T046–T053 | 14 | `tests/contract/test_seal_boundaries.py`、`tests/fixtures/seal-archive/concurrent/`、`notes/quickstart-run.md`、`test-evidence/**`、`verification.md`、`.specify/features.md` + 详情 | 契约 C-111、C-116、C-312；十项 SC 的 Measurement Sources 各有落点 |

包定义与依赖边归 plan.md § Execution Model 所有；本表只记行号投影，不复制其依赖规则。行数以 `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/100-seal-slice-archive/requirements.md --tasks .specify/specs/100-seal-slice-archive/tasks.md` 的 `task_count` 为准（本文件 53 行；见 § Generation Measurements）。

> **依赖边注（与 plan § Execution Model 对齐）**：P8 的逐阶段检查点行（T009 / T021 / T032 / T034 / T037）按其阶段顺序执行，不等待 P7；T045 是唯一例外——它依赖 P7 的 T044；`P7 → P8` 只约束 T045 与收尾行 T046–T053。P7 的 T033 / T038 只依赖 P4 行（T017/T019 与 T018），不等待 P5/P6；`P5 → P7` / `P6 → P7` 只约束真实回合行 T042–T044。

## Generation Measurements（2026-11-11 本阶段实测；含陷阱形态）

| 读数 | 复现命令 | 实测输出 | 陷阱形态（朴素写法为何给出不同答案） |
|---|---|---|---|
| 条款定义 40（16 / 12 / 12） | `grep -cE '^\*\*C-[0-9]{3}\*\*' .specify/specs/100-seal-slice-archive/contracts/*.md` | archive-actions 16；archive-manifest 12；reference-classification 12 | `grep -c 'C-'` 会连正文交叉引用一起数，给出 30 / 16 / 17（合计 63）——条款只按定义行计；`clause_extract.clause_citations()` 同样返回 16 / 12 / 12 |
| FR 定义 28 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/100-seal-slice-archive/requirements.md` | 28 | 按 `FR-` 子串计数会连引用与 `Runtime Stack` 表一起数 |
| 命令基线 31 | `ls templates/commands/*.md \| wc -l` | 31 | `find templates/commands -name '*.md'` 会把将来嵌套子目录的文件也算进来 |
| 镜像对基线 | `python3 scripts/python/sync-mirrors.py --check` | exit 2，唯一 `DIFF` = `.specify/templates/gitignore-specify-template`（既有、非本特性写面） | 把「exit 0」当判据会误判为红；本特性判据是「触及的镜像对零新增漂移」 |
| 命令副本基线 | `python3 scripts/python/regen-command-copies.py --check` | `OK: all per-tool command copies match the source templates.`（exit 0） | — |
| 引擎现值（实现前） | `python3 scripts/python/seal-utils.py --help` | `--action {merge-plan,merge-apply,seal,archive-gate}` | 实现后应为六值；测试行按六动作断言，不按此读数断言 |
| 074 触发前提 | 解析 `.specify/specs/074-goal-team-sdd-unification/merge-manifest.json` | `merge.status=merged`、`conflicts=[]`、`slices` 2 行 | 文件数与哈希由运行期探针产生，测试 MUST NOT 写死（clarify Q3；requirements SC-001） |
| 任务行数 53 / 包数 8 | 上引 `decomposition-check.py --mode tasks` | `proceed`（fr_count=28 / task_count=53；ceiling 120 / 160） | `grep -c '^- \['` 会同时命中 Format 图例之外的行；任务行只按 `^- \[[ xX>~]\] T[0-9]{3}` 计 |

## Definition of Done (DoD)

- DoD-1: **条款认领** — 40 条契约条款每条恰被一个任务行 `[green:]` 认领一次，各契约内认领随行序单调；`account-clause-coverage.py` 报 claimed 40、FR 28/28、uncovered beyond baseline 0（T052 读数）。Check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/100-seal-slice-archive/tasks.md` 0 error / 0 warning 且 `test-evidence/coverage-final.txt` 记录上述三项。
- DoD-2: **FR/SC 追溯** — FR-001…FR-028 与 SC-001…SC-010 每条至少被一个任务行在行内逐字引用（§ FR → row trace / § SC → row trace）。
- DoD-3: **引擎契约** — 动作集封闭六值、只读/写划分 3/3、退出码封闭 `0/1/2`、`--help`/`--version` 零副作用、未声明选项 exit 2（C-101、C-115）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py tests/unit/test_seal_archive_classify.py tests/unit/test_seal_archive_manifest_math.py tests/unit/test_seal_archive_schema.py -q` 全绿。
- DoD-4: **零丢失与纯移动** — 074 归档前后文件数、逐文件 sha256、相对路径集合相等；`git diff --name-status -M HEAD`（比较基 = apply 前提交）在被移动分片路径集上全为重命名对、零纯删除，清单 A 与活引用载体 M 按声明集合断言、全局零 D（C-106、C-204…C-207、SC-001）。Check: T043 读数 + `bash scripts/bash/run-tests.sh tests/integration/test_seal_archive_round.py -q` 全绿。
- DoD-5: **引用 fail closed** — 活引用全部直接解析、日期化载体原字节且经清单映射解析、未解析 = 0、封闭集外命中 `unclassified-reference` 阻断（C-305…C-307、SC-003）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py -q` 全绿。
- DoD-6: **幂等与确定性** — 重跑 apply `already-archived` 零 diff、两次 `archive-plan` 逐字节一致、排序键只取声明字段（C-105、C-109、C-208、SC-002/SC-006）。Check: `bash scripts/bash/run-tests.sh tests/integration/test_seal_archive_idempotency.py -q` 全绿。
- DoD-7: **074 回合** — 两片落 `slices/`、`archive-manifest.json` 可复核、注册状态与封装结论不变、重跑可复现（FR-025、FR-026、SC-001）。Check: `test-evidence/074-archive-round.txt` 存在且含零丢失读数与两次运行对照。
- DoD-8: **边界与单一机制** — 无删除 / push / 注册表状态写（`.specify/state/**` 运行期更新按 FR-017 单独允许）/ goal-team 写 / `.specify/archive/` 写 / 父 spec 的 `seal.md` 回执字节不变（`templates/commands/seal.md` 命令模板与 `docs/reference/commands/seal.md` 命令参考是编辑目标，不在此禁列）；无第二套处置词表、第二归档引擎或共享聚合；owner 原地修订在位（C-110…C-113、C-312、SC-005/SC-009）。Check: `bash scripts/bash/run-tests.sh tests/contract/test_seal_boundaries.py tests/integration/test_seal_archive_rollback.py -q` 全绿。
- DoD-9: **镜像与副本生成** — `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 相对 T001 基线零新增漂移（plan § Mirror Obligations）。Check: GATE-2。
- DoD-10: **final 判据全 pass 且有 smoke 记录** — `verification.md` 每条 SC 一行状态，`**Path**: final` 判据均为 `pass`，smoke 三键齐备（GATE-4）。

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量套件相对实现入口基线零**新增**失败 — 基线名单由 `/speckit.implement` step 6 的 `**Test runs**` 拥有（`--names-out` 捕获、`comm -13` 比对）；本流程只消费该基线、不另立第二路径。Check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/100-seal-slice-archive/test-evidence/final-failed.txt` 后与基线名单做 `comm -13`，新增名单为空。
- GATE-2: plan.md § Mirror Obligations 的每一对源/镜像与全部 per-tool 命令副本零**新增**漂移（T001 基线：唯一既有 `DIFF` = `.specify/templates/gitignore-specify-template`，非本特性写面）。Check: `python3 scripts/python/sync-mirrors.py --check` 的 `DIFF` 集与 T001 记录逐条相等，且 `python3 scripts/python/regen-command-copies.py --check` exit 0。
- GATE-3: 无遗留 `[ ]` / `[>]` 任务行。Check: `grep -cE '^- \[[ >]\] T[0-9]{3} ' .specify/specs/100-seal-slice-archive/tasks.md` 返回 0。
- GATE-4: 每条 `final` 路径成功判据为 `pass` **且** smoke 记录存在。Check: `.specify/specs/100-seal-slice-archive/verification.md` 中每条 `**Path**` 读 `final` 的判据有 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（存在且非空的路径）三键齐备；`blocked`/`deferred`/`fail` 的 final 判据除非有具名用户豁免否则不通过。条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates——本行只承载检查，不复制 schema。
- GATE-5: 结构校验器干净。Check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/100-seal-slice-archive/tasks.md` exit 0 且 0 error。
- GATE-6: 条款覆盖与回合证据齐备。Check: `python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/100-seal-slice-archive` 报 claimed 40、FR 28/28、uncovered beyond baseline 0；`test -s .specify/specs/100-seal-slice-archive/test-evidence/074-archive-round.txt` 且其中含零丢失读数。

## Environment Prerequisites

Probed 2026-11-11 in this worktree（`100-seal-slice-archive` @ `90bab87ee`）。每条依赖这些裁决的任务行引用本节、不复述结论；implement 入口须重新探测，不跨运行缓存。

- CPython 解释器（引擎与全部测试）：**available** — probe: `python3 --version` @ 2026-11-11 → `Python 3.11.11`；`pyproject.toml` 声明 `requires-python >=3.8`；受影响：全部引擎与测试行。
- `pytest`：**available** — probe: `python3 -c "import pytest; print(pytest.__version__)"` @ 2026-11-11 → `8.4.2`；受影响：全部测试行与 GATE-1。
- 唯一测试入口 `scripts/bash/run-tests.sh`：**available** — probe: `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q` @ 2026-11-11 → `31 passed in 6.62s`；受影响：全部 `bash scripts/bash/run-tests.sh` 行。
- `git`（`git mv` / `status --porcelain` / `diff --name-status -M`）：**available** — probe: `git --version` @ 2026-11-11 → `git version 2.43.5`；`git rev-parse --is-inside-work-tree` → `true`；受影响：T043 的钉住提交与批次提交、`dirty-spec-tree` 与纯移动判定；非 git 工作树按 exit 2（`not-a-git-tree`）。
- 外部服务 / 网络 / 容器运行时 / 守护进程：**not required** — 引擎 stdlib-only，全部夹具树在 sanctioned 临时根（`.specify/shared/guidelines/temp-directory-discipline.md`）下本地构建。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可并行——不同**写**目标、且不依赖同阶段未完成行。
- **[Story]**: `US1`…`US4`，仅用户故事阶段携带；Setup / Foundational / Polish 阶段零 `[US` 标记。
- **[blockedBy: Txxx,Tyyy]**: 显式依赖；被列出的任务未 `[X]` 前本行不得开始。无标签的行只服从阶段顺序。
- **[green: <contract>#<clause>]**: 绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析；40 条款分区（每条款恰一行）：见各任务行的标签，`validate-tasks.py` 的 `green-dangling` / `green-cross-phase` / `green-clause-collision` / `green-path-divergence` 四项检查负责机验。标签定义 owner：`.specify/templates/tasks-template.md` § Format。
- 一行一条任务，精确写路径；禁止换行续写（单行契约由 `validate-tasks.py` 机验）。
- **Task State Sigil**: `- [ ]` open · `- [>]` claimed（多代理件）· `- [X]` closed · `- [~]` deferred；`[~]` 原因记入 `verification.md` 的 `deferred_tasks=`。

## Path Conventions

两顶帽子（plan.md § Structure Decision、§ Mirror Obligations）：`scripts/`、`shared/`、`skills/`、`templates/`、`tests/` 是**框架源**；`.specify/scripts/`、`.specify/shared/`、`.specify/skills/` 是 `scripts/python/sync-mirrors.py` 生成的运行时投影，绝不手改；命令模板经 `scripts/python/regen-command-copies.py` 投影到 `.claude/commands/`、`.github/prompts/`、`.opencode/command/`、`.qoder/commands/` 四份副本（`.specify/templates/commands/` 已退役）。`<parent>/slices/` 是父 spec 内的**数据**目录。全部路径为仓库根相对路径。

## FR → row trace

| FR | 任务行 |
|----|--------|
| FR-001 | T010、T015、T018、T038、T042、T043、T045 |
| FR-002 | T011、T017、T036、T043 |
| FR-003 | T013、T017、T018 |
| FR-004 | T011、T016、T018、T043 |
| FR-005 | T012、T016、T020、T028、T029、T031 |
| FR-006 | T010、T015 |
| FR-007 | T010、T011、T015 |
| FR-008 | T004、T005、T006、T009、T041 |
| FR-009 | T013、T015、T019 |
| FR-010 | T013、T014、T017、T044 |
| FR-011 | T033、T048 |
| FR-012 | T022、T023、T024、T032 |
| FR-013 | T025、T026 |
| FR-014 | T022、T025、T026 |
| FR-015 | T023、T025、T029 |
| FR-016 | T026、T027 |
| FR-017 | T022、T026、T032 |
| FR-018 | T030 |
| FR-019 | T007、T008、T009、T035 |
| FR-020 | T034、T036、T037 |
| FR-021 | T005、T039、T040、T045、T047 |
| FR-022 | T039、T040、T048 |
| FR-023 | T036 |
| FR-024 | T003、T021、T046、T049、T050、T052 |
| FR-025 | T042、T043 |
| FR-026 | T044 |
| FR-027 | T034、T053 |
| FR-028 | T006、T019、T024、T034 |

## SC → row trace

| SC | 任务行 | 首红模块（C-116；偏差见 Notes 1） |
|----|--------|---------------------------|
| SC-001 | T018、T043 | `tests/integration/test_seal_archive_round.py` |
| SC-002 | T014、T020、T044 | `tests/integration/test_seal_archive_idempotency.py` + `tests/contract/test_seal_archive_apply.py` |
| SC-003 | T023 | `tests/contract/test_seal_archive_plan.py` |
| SC-004 | T038、T041、T045 | `tests/integration/test_seal_archive_round.py`（阻断态）+ `tests/contract/test_seal_engine_contract.py` |
| SC-005 | T034、T037 | `tests/contract/test_seal_boundaries.py` |
| SC-006 | T020、T028 | `tests/integration/test_seal_archive_idempotency.py` |
| SC-007 | T012、T027 | `tests/contract/test_seal_archive_manifest.py`（T012 写红先算术/删行变异用例，T027 实现并转绿） |
| SC-008 | T013、T026 | `tests/contract/test_seal_archive_apply.py`（runtime 夹具；T013 写 apply 骨架，T026 追加 runtime 存在/缺席用例） |
| SC-009 | T034、T053 | `tests/contract/test_seal_boundaries.py` + 并发夹具 |
| SC-010 | T033 | `tests/integration/test_seal_archive_rollback.py`（见 § Notes 裁定 1） |

> **流程行（无 FR/SC 归属）**: T001（改前基线捕获）、T002（证据落点骨架）、T051（Feature 注册表收尾）按 `feature-integration.md` § Core Protocol 与 Setup 职责执行，不进入 FR→row / SC→row 表；T003 归 FR-024。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结四类对照物（改前测量、条款覆盖基线、运行时证据落点），使后续「零新增」判据全部有对照物。

- [X] T001 捕获改前基线：创建 `.specify/specs/100-seal-slice-archive/notes/pre-change-measurements.md`，逐项贴真实输出与捕获日期——`python3 scripts/python/sync-mirrors.py --check`（`DIFF` 集逐行）、`python3 scripts/python/regen-command-copies.py --check`、`ls templates/commands/*.md | wc -l`、`git rev-parse HEAD`、`git status --short`、seal 测试文件清单（`ls tests/contract/test_seal_*.py tests/integration/test_seal_*.py`）；本行不写任何源文件。 [P]
- [X] T002 创建其余运行时证据落点 `.specify/specs/100-seal-slice-archive/notes/red-first-evidence.md` 与 `.specify/specs/100-seal-slice-archive/notes/quickstart-run.md` 的标题骨架（Foundational 起的红先行与 quickstart 行已有地方可写）。 [P]
- [X] T003 冻结条款覆盖基线：`python3 scripts/python/account-clause-coverage.py .specify/specs/100-seal-slice-archive --freeze > .specify/specs/100-seal-slice-archive/coverage-baseline.txt`（脚本只打印、不写文件），核对头部含 `frozen-from:` 且正文**不含**本 spec 的 40 条 `C-N` 名——基线排除被核算 spec 自身，本 spec 条款只能被任务行认领、不能被自己的基线豁免（FR-024）。 [blockedBy: T001]

**Checkpoint**: 四类分母落盘（镜像/副本、命令面、名字级测试基线、条款覆盖），后续零新增判据均有冻结对照物。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 动作集 4→6 与 manifest-aware 分片发现。四条用户故事的每一个面都经由这两个引擎能力，故先于任何用户故事。

**⚠️ CRITICAL**: 本阶段完成前，任何用户故事行不得开始。

- [X] T004 红先扩写 `tests/contract/test_seal_engine_contract.py` 的动作集 pin 到六值（`ACTIONS` / `READ_ONLY_ACTIONS` / `WRITE_ACTIONS` 三元组、C-001 的 HANDLERS 与 argparse `choices` 断言、`--help` 动作标签）；运行 `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q` 并把红输出与退出码记入 `notes/red-first-evidence.md`（FR-008）。
- [X] T005 在 `scripts/python/seal-utils.py` 实现封闭六动作集：`ACTIONS`、`READ_ONLY_ACTIONS`（新增 `archive-plan`）、`WRITE_ACTIONS`（新增 `archive-apply`）、`HANDLERS` 两行（先指向 `_pending`）、`--action` choices 与帮助文本；`DECLARED_OPTIONS` 零新增；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认本对零新增漂移（FR-008、FR-021）。 [green: contracts/archive-actions.contract.md#C-101] [blockedBy: T004]
- [X] T006 扩写 `tests/contract/test_seal_boundaries.py` 的动作表审计：六动作封闭、只读/写划分恰 3/3、无破坏性动作、无调度器/守护进程构造；运行该文件全绿并把读数记入 `test-evidence/foundational-checks.txt`（FR-008、FR-028）。 [P] [blockedBy: T005]
- [ ] T007 建夹具 `tests/fixtures/seal-archive/archived-pair/`（父 spec + `slices/` 下两片 + `archive-manifest.json`）并在 `tests/contract/test_seal_merge_plan.py` 写红先测试：清单存在时分片集与顺序不变、`slices/` 不被读成新候选、清单不可解析或与合并清单/树不一致时以 exit 2（`archive-manifest-invalid` / `archive-drift`）拒绝（FR-019）。 [P] [blockedBy: T005]
- [ ] T008 在 `scripts/python/seal-utils.py` 实现 manifest-aware 分片发现：`_discover_slices` / `_derive_order` / `_merge_state` 先读 `archive-manifest.json` 并校验其 `slices[]` 与合并清单及目录树一致，缺席才回退同级扫描，绝不把 `slices/**` 读成新分片候选；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认本对零新增漂移（FR-019）。 [blockedBy: T007]
- [ ] T009 Foundational 检查点：运行 `bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py tests/contract/test_seal_boundaries.py tests/contract/test_seal_merge_plan.py tests/integration/test_seal_merge_determinism.py -q`，把命令、完整输出与退出码记入 `test-evidence/foundational-checks.txt`（FR-008、FR-019）。 [blockedBy: T005,T006,T008]

**Checkpoint**: 引擎的六动作面与归档后分片发现就位；US1–US4 的行可以开始。

---

## Phase 3: User Story 1 - 把已交付分片归档进父 spec 的 slices/，零丢失 (Priority: P1) 🎯 MVP

**Goal**: 对一条 merge-apply 已完成的拆分 spec 运行归档：分片整体 `git mv` 进 `<parent>/slices/<原分片目录名>/`，分片内容字节不变，父 spec 根落一份 `archive-manifest.json`，重跑收敛为 `already-archived`。

**Independent Test**: 在 `tests/fixtures/seal-archive/clean-pair/` 的回放树上执行 plan → apply → 重跑：两片只存在于 `slices/` 下、文件数与逐文件 sha256 不变、`git diff --name-status -M <pinned_commit>`（比较基 = apply 前提交）在被移动分片路径集上全为重命名对、清单/活引用载体按 A/M 集合断言、清单存在且可复核；重跑 apply 得 `already-archived` 且零 diff。**074 树的真实验收**由 US3 阶段的 T042–T044 执行（plan § Execution Model 的 `P4 → P7` 依赖边），其读数同样满足本故事的验收。

**Checkpoint**: 本故事独立可测——夹具回放树上的移动、清单、幂等三面全部可单独验证。

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T010 [US1] 写红先契约测试 `tests/contract/test_seal_archive_plan.py`：五条件合取且逐条点名**全部**未满足项；`verdict`/`outcome` 封闭集与 `0/1/2` 退出域；`not-applicable` 带依据；同片双侧 `destination-exists`（exit 1）与跨片不自洽 `partial-archive`/`slice-missing`（exit 2）分层；拒绝零写盘；封装阻断的 spec 仍可 plan（FR-001、FR-006、FR-007）。 [P] [blockedBy: T005]
- [ ] T011 [US1] 建夹具 `tests/fixtures/seal-archive/clean-pair/`（两片在源、合并清单 `merged`、无外部引用）与 `tests/fixtures/seal-archive/empty/`（无分片、`merge.status: not-applicable` 带 `basis`）（FR-002、FR-004、FR-007）。 [P] [blockedBy: T005]
- [ ] T012 [US1] 写红先契约测试 `tests/contract/test_seal_archive_manifest.py`：顶层/逐片/`checks` 键集等于封闭集（逐片恰七字段，`slices` 按 `order`、`files` 按 `path` 排序）；序列化 `indent=2, sort_keys=True, ensure_ascii=False`；`digest` 按 099 C-034 算法；无墙钟/绝对路径/`..` 字段；同输入两次 plan 逐字节一致；三组闭环算术复算与删行变异转红（SC-007 首红宿主）（FR-005、FR-016）。 [P] [blockedBy: T005]
- [ ] T013 [US1] 写红先契约测试 `tests/contract/test_seal_archive_apply.py`：纯移动（在被移动分片路径集上 `git diff --name-status -M <pinned_commit>` 全为 `R`、零 `D`；清单 A 与活引用载体 M 按声明集合断言）、只读阶段重算与 plan 一致（规范化计划 JSON 的 sha256 相等）、`already-archived`、拒绝零持久化、非 git 树 exit 2（FR-003、FR-009、FR-010、SC-008）。 [P] [blockedBy: T005]
- [ ] T014 [US1] 写红先集成测试 `tests/integration/test_seal_archive_idempotency.py`：第二次 apply 得 `already-archived` 且相对重跑前零新增 diff、plan 零待移动/零未解析、注入内容变异使哈希检查转红（FR-010、SC-002）。 [P] [blockedBy: T005]

### Implementation for User Story 1

- [ ] T015 [US1] 在 `scripts/python/seal-utils.py` 实现 `archive-plan` 前置与结论：从 `merge-manifest.json` 与 `git status --porcelain` 读取 C-102 合取并逐条点名全部未满足项；`verdict`/`outcome` 封闭集与三值退出码；`not-applicable` 带 `basis`；拒绝与错误零持久化（FR-001、FR-006、FR-007、FR-009）。 [green: contracts/archive-actions.contract.md#C-102] [green: contracts/archive-actions.contract.md#C-103] [green: contracts/archive-actions.contract.md#C-104] [blockedBy: T010,T005]
- [ ] T016 [US1] 在 `archive-plan` 内实现归档清单候选：封闭顶层键集、逐片条目恰含 `slug`/`from`/`to`/`order`/`file_count`/`files[{path,sha256}]`/`merged_into_pointer`（`slices` 按 `order` 升序、`files` 按 `path` 升序）、`pinned_commit`、按 C-207 逐字段路径基准与 C-034 `digest`；写入侧与读取侧共用同一校验函数（FR-004、FR-005）。 [green: contracts/archive-manifest.contract.md#C-201] [green: contracts/archive-manifest.contract.md#C-202] [green: contracts/archive-manifest.contract.md#C-203] [blockedBy: T012,T015]
- [ ] T017 [US1] 实现 `archive-apply` 核心写批次：只读阶段重算与 plan 相同；`git mv` 每个分片目录到 `<parent>/slices/<slug>`；写 `archive-manifest.json`；只改父 `merge-manifest.json` 的路径形态值并重算摘要（前后值记入清单）；重跑读清单走 `already-archived`（FR-002、FR-003、FR-010）。 [green: contracts/archive-actions.contract.md#C-105] [green: contracts/archive-actions.contract.md#C-106] [blockedBy: T016,T013]
- [ ] T018 [US1] 写夹具回放测试 `tests/integration/test_seal_archive_round.py`：把 `clean-pair` 复制成临时 git 树，按 merge-apply → 提交 merge 批次 → archive-plan → archive-apply → seal（阻断态）顺序执行，断言分片落在 `slices/`、文件数/逐文件 sha256/相对路径集合不变、全为重命名对、清单可复核、封装阻断不阻断归档也不改变阻断清单（FR-001、FR-003、FR-004、SC-001）。 [green: contracts/archive-actions.contract.md#C-107] [blockedBy: T017,T011]
- [ ] T019 [US1] 实现 `archive-apply` 的两阶段原子性：只读重算门；写入按批次执行；任一步失败按原字节恢复已移动目录与已改写文件并以 exit 2（`write-failed`）结束；拒绝路径零持久化（FR-009、FR-028）。 [green: contracts/archive-actions.contract.md#C-108] [blockedBy: T018]
- [ ] T020 [US1] 补齐确定性面（扩写 `tests/integration/test_seal_archive_idempotency.py`）：两次 `archive-plan` 逐字节一致（sha256 对照）、排序键只取声明字段、apply 重跑零 diff、把排序改为返回时刻或目录枚举顺序时测试转红（FR-005、SC-002、SC-006）。 [green: contracts/archive-actions.contract.md#C-109] [blockedBy: T019,T014]
- [ ] T021 [US1] US1 检查点：运行 `bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py tests/contract/test_seal_archive_apply.py tests/integration/test_seal_archive_idempotency.py tests/integration/test_seal_archive_round.py -q`，把读数记入 `test-evidence/us1-checkpoint.txt`（FR-024）。 [blockedBy: T020]

---

## Phase 4: User Story 2 - 归档后所有引用仍然可解析（活引用改写，历史记录只映射） (Priority: P1)

**Goal**: 归档 apply 在同一批次内把全部活引用改写为归档路径、日期化记录保持原字节并只经清单 `from → to` 映射解析；apply 前报告的未解析数为 0 才写入，封闭集外命中即阻断。

**Independent Test**: 用干净版 `tests/fixtures/seal-archive/reference-matrix/` 运行 plan/apply：活引用全部改写、日期化载体哈希前后一致且经映射可解析；再用 `tests/fixtures/seal-archive/reference-matrix-unclassified/` 断言未分类载体让 apply 拒绝；再注入一条指向旧路径的活引用、或移除一个映射，断言转红。

**Checkpoint**: 本故事独立可测——分类、改写、台账三面在 reference-matrix 夹具上单独验证。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T022 [US2] 建夹具 `tests/fixtures/seal-archive/reference-matrix/`（live：register/glossary/instructions/父正式文档/contracts/shared 源与镜像/tests 构造行；dated：memory/history/features.md/分片内部/notes/test-evidence/checklists；另含一份父级 `seal.md` 以断言不被改写）、`reference-matrix-unclassified/`（在干净版上外加一条 unclassified 载体）、`partial-pair/`（一片在目标一片在源）与 `runtime-present/`（含 `.specify/state/` 记录）（FR-012、FR-014、FR-017）。 [P] [blockedBy: T005]
- [ ] T023 [US2] 在 `tests/contract/test_seal_archive_plan.py` 追加红先分类测试：干净 reference-matrix（live/dated）、reference-matrix-unclassified、partial-pair 三类夹具；注入一条指向旧路径的活引用、或从清单移除一个 `from → to` 映射时检查转红（FR-012、FR-015、SC-003）。 [blockedBy: T022,T015,T010]

### Implementation for User Story 2

- [ ] T024 [US2] 实现载体名册与分类引擎：封闭扫描根、F1/F2/F3 引用形态（F1 最长匹配优先、裸 slug 永不计为引用）、混合载体的 H2 章节谓词、`live-rewrite` / `dated-preserved` 二值互斥、封闭集外命中即 `unclassified-reference` 阻断；判定只依据路径、行前缀或章节边界；并写红先单元测试 `tests/unit/test_seal_archive_classify.py` 覆盖路径形态分类谓词（F1/F2/F3、F1-F2/F1-F3 重叠、裸 slug、identity 字面量、H2 章节）；父级 `seal.md` 不属 live 载体，MUST NOT 被改写（夹具断言字节不变）（FR-012）。 [green: contracts/reference-classification.contract.md#C-301] [green: contracts/reference-classification.contract.md#C-302] [green: contracts/reference-classification.contract.md#C-303] [green: contracts/reference-classification.contract.md#C-304] [green: contracts/reference-classification.contract.md#C-305] [green: contracts/reference-classification.contract.md#C-306] [blockedBy: T023]
- [ ] T025 [US2] 实现改写引擎：F1/F2/F3 确定性前缀替换；逐条记 `before`/`after`/`carrier`/`line`；日期化载体运行前后 sha256 相等（否则 exit 2 并按原字节恢复）；未解析数按唯一定义计算并在大于 0 时拒绝（FR-013、FR-014、FR-015）。 [green: contracts/reference-classification.contract.md#C-307] [green: contracts/reference-classification.contract.md#C-308] [blockedBy: T024]
- [ ] T026 [US2] 实现引用台账与运行期载体：`references.rows[]` 封闭字段与二值 `kind`；`references.runtime[]` 每载体一条 `runtime-updated`/`absent`（附原因，缺席不阻断、更新不进版本库、不改任何 spine 读数）；`shared/**` 源与 `.specify/shared/**` 镜像同批改写成同一文本（不一致 → `2` `mirror-copy`）；`tests/**` 的 F3 构造行改写、identity 常量不动；并扩写 `tests/contract/test_seal_archive_apply.py` 的 runtime 存在/缺席两类用例与「缺席改阻断」变异（SC-008 首红宿主，使用 `runtime-present/` 夹具）（FR-013、FR-016、FR-017、SC-008）。 [green: contracts/archive-manifest.contract.md#C-204] [green: contracts/archive-manifest.contract.md#C-205] [green: contracts/reference-classification.contract.md#C-309] [green: contracts/reference-classification.contract.md#C-310] [green: contracts/reference-classification.contract.md#C-311] [blockedBy: T025]
- [ ] T027 [US2] 补齐 `checks` 与摘要记账：`preconditions`（`merge_status`/`open_conflicts`/`slices_closed`/`dirty_spec_tree`/`side_presence` 按 C-206 类型）/`moved_files`/`live_rewrite`/`dated_preserved`/`unclassified`/`unresolved_before`/`unresolved_after`/`runtime_carriers`/`files_match` 键集封闭；三组闭环算术成立；`digest` 覆盖完整文档；`pinned_commit` 为 apply 前 `git rev-parse HEAD`；无墙钟/运行主机/随机 id/绝对路径字段；并写红先单元测试 `tests/unit/test_seal_archive_manifest_math.py` 覆盖 C-034 摘要与三组闭环算术；各路径字段按 C-207 的逐字段基准（FR-016、SC-007）。 [green: contracts/archive-manifest.contract.md#C-206] [green: contracts/archive-manifest.contract.md#C-207] [blockedBy: T026]
- [ ] T028 [US2] 清单确定性收口：带完整台账的两次 plan 逐字节一致；排序键只取声明字段（路径、行号、`order`、`slug`）；成功 apply 后重跑零 diff（FR-005、SC-006）。 [green: contracts/archive-manifest.contract.md#C-208] [blockedBy: T027]
- [ ] T029 [US2] 实现唯一校验器与唯一解析通道：plan / apply / 归档后发现共用同一 schema 校验函数，未知或缺失字段 exit 2；清单是「旧路径 → 归档路径」的唯一映射（不建缓存索引或派生映射文件）；并写红先单元测试 `tests/unit/test_seal_archive_schema.py` 覆盖 schema 校验函数的未知/缺失字段拒绝（FR-005、FR-015）。 [green: contracts/archive-manifest.contract.md#C-209] [green: contracts/archive-manifest.contract.md#C-210] [blockedBy: T028]
- [ ] T030 [US2] 实现并钉住父 `merge-manifest.json` 的路径字段修订：对清单全文模式扫描枚举匹配 `.specify/specs/<任一分片 slug>[/…]` 形态的字符串值（匹配集合 = 允许差异集，不手写字段清单），匹配集合之外的值逐字节不变；合并结论（`merge`）/`checks` 计数/冲突/ID 映射/顺序/`retention` 不变，摘要按 C-034 重算并在归档清单记前后值；扩写 `tests/contract/test_seal_merge_apply.py`（FR-018）。 [green: contracts/archive-manifest.contract.md#C-211] [blockedBy: T029]
- [ ] T031 [US2] 实现 schema 版本纪律：`schema_version` 从 `1` 起且本特性只写 `1`；更高版本或未知字段在读取侧 exit 2（`archive-manifest-invalid`）；字段集增删改只走契约页修订；扩写 `tests/contract/test_seal_archive_manifest.py`（FR-005）。 [green: contracts/archive-manifest.contract.md#C-212] [blockedBy: T030]
- [ ] T032 [US2] US2 检查点：运行分类 + 清单 + merge-apply 套件，把 `reference-matrix` 上的 `live-rewrite` / `dated-preserved` / `unclassified` / 未解析四项计数记入 `test-evidence/us2-checkpoint.txt`（FR-012、FR-017）。 [blockedBy: T031,T022]

---

## Phase 5: User Story 4 - 归档有明确边界：不是退休、不改状态、可回滚 (Priority: P2)

**Goal**: 归档只在父 spec 的 `slices/` 子树内移动文件；不查询 `archive-gate`、不写 `.specify/archive/`、不改注册状态/`seal.md`/合并结论；回滚按文档步骤恢复到归档前的逐字节状态。

**Independent Test**: 静态审计引擎写面白名单与动作表；对夹具执行归档后按文档步骤回滚并断言逐字节一致；注入一次删除或一次状态写入，断言静态审计转红；两个夹具 spec 并发归档写入不同清单路径。

**Checkpoint**: 本故事独立可测——回滚、并发、单一机制、owner 修订四面均有独立断言。

- [ ] T033 [US4] 写回滚任务 `tests/integration/test_seal_archive_rollback.py`：在夹具上 apply 后按契约 C-110 与 quickstart S-6 的步骤逐字执行（逆 `git mv` → `git restore --source=<pinned_commit> --staged --worktree` → 移除清单 → 运行期逆写），断言 `git diff --exit-code <pinned_commit> -- <parent> <slices> <live carriers>` 为空且 `references.rows[]` 逐行核对成立；跳过任一步骤时断言转红（FR-011、SC-010）。 [green: contracts/archive-actions.contract.md#C-110] [blockedBy: T019,T017]
- [ ] T034 [US4] 写单一机制与并发静态审计（扩写 `tests/contract/test_seal_boundaries.py`）：每父 spec 一份清单、`tests/fixtures/seal-archive/concurrent/` 两个夹具 spec 并发归档写入不同路径、同一 spec 由「后到者读清单 → `already-archived` / `archive-drift`」收敛且无锁文件；写面白名单以数据表表达（移动仅 `archive-apply` 且目标限 `<parent>/slices/`），并审计引擎外部命令白名单（只允许 `git mv` / `status` / `diff` / `rev-parse`；`push` 缺席），注入删除、注册表状态写入或 `git push` 时转红；把一份清单复制成共享聚合时测试转红；解析无缓存索引/第二份映射表（FR-020、FR-027、FR-028、SC-005、SC-009）。 [green: contracts/archive-actions.contract.md#C-111] [green: contracts/reference-classification.contract.md#C-312] [blockedBy: T017]
- [ ] T035 [US4] 写归档后等价性测试（扩写 `tests/integration/test_seal_074_round.py`）：归档后 merge-plan 报告同一分片集且零待移动、merge-apply exit 0 且零写入、seal 的 P0 / `blocking` / 闭合判定与归档前一致；`slices/**` 不被读成新分片候选；清单缺席时回退同级扫描（FR-019）。 [green: contracts/archive-actions.contract.md#C-112] [blockedBy: T008,T034]
- [ ] T036 [US4] 原地修订既有 owner：`shared/definitions/non-disposable-definitions.md` § Disposition Set 的 `archive` 目的地扩为封闭二形（退休 `.specify/archive/` 或所属父 spec 的 `slices/`）且 § Disposal Pathways 记分片处置记录 = 父 `archive-manifest.json`；`shared/definitions/framework-map.md` 的 Feature specs 行登记 `slices/` 语义；099 `seal-engine.contract.md` C-001/C-008、`merge-back.contract.md` C-019/C-023、`records-and-boundaries.contract.md` C-035/C-036 原地修订；随后 `python3 scripts/python/sync-mirrors.py --write` 并确认零新增漂移（FR-002、FR-020、FR-023）。 [green: contracts/archive-actions.contract.md#C-113] [P] [blockedBy: T005]
- [ ] T037 [US4] US4 检查点：运行 boundaries/rollback/074_round 套件，抓取归档前后状态面快照（注册表行、详情状态、父 spec 的 `seal.md` 回执缺失或存在时字节不变（命令模板/命令参考不在此列）、合并结论/计数/冲突）存入 `test-evidence/us4-checkpoint.txt`，断言除路径字段、摘要、归档清单与被移动目录外零变化（FR-020、SC-005）。 [blockedBy: T033,T034,T035,T036]

---

## Phase 6: User Story 3 - 归档步骤固化在 /speckit.seal 流程中，blocked 状态也能执行 (Priority: P1)

**Goal**: `/speckit.seal` 在 merge-apply 成功并提交 merge 批次之后自动进入归档阶段（先预览后 apply，再提交 archive 批次，最后才做封装判定）；`Sealed` 与具名阻断两种终态都可归档；命令名集合与 `COMMAND_BASELINE`（31）不变；074 真实回合完成归档。

**Independent Test**: 对封装阻断的夹具运行 `/speckit.seal` 全流程，归档照常执行；对 merge-apply 被拒绝的夹具，归档不启动；074 真实树上执行归档并断言零丢失、状态与封装结论不变、重跑 `already-archived`。

**Checkpoint**: 本故事独立可测——阻断态夹具、merge 拒绝夹具与 074 真实回合三面各自可验证。

- [ ] T038 [US3] 建夹具 `tests/fixtures/seal-archive/blocked-pair/`（合并完成、封装阻断具名）并在 `tests/integration/test_seal_archive_round.py` 追加阻断态测试：封装阻断仍归档、阻断清单与归档清单互不覆盖、merge-apply 被拒绝的夹具不启动归档（FR-001、SC-004）。本行只追加用例、不认领新绿点（该文件的绿点归 T018 的 C-107）。 [P] [blockedBy: T018]
- [ ] T039 [US3] 在 `templates/commands/seal.md` 与 `skills/internal/seal-artifact/SKILL.md` 落归档阶段：merge-apply 成功并提交 merge 批次之后 → archive-plan（预览）→ archive-apply（写入）→ 提交 archive 批次 → seal 判定；说明封装阻断不阻断归档、拒绝语义与报告原样转述纪律，技能不得在引擎判定之外给出结论（FR-021、FR-022）。 [blockedBy: T035,T036]
- [ ] T040 [US3] 更新 `docs/reference/commands/seal.md`（可执行的归档走查 + 可执行的恢复走查，即 C-114 的「各给出」），用 `python3 scripts/python/regen-command-copies.py` 生成四份逐工具副本、`python3 scripts/python/sync-mirrors.py --write` 投影技能，并运行 `bash scripts/bash/run-tests.sh tests/contract/test_migration_distribution.py -q` 的 `COMMAND_BASELINE` 对照（31；`ls templates/commands/*.md | wc -l` 于 2026-11-11 实测 31）与两条 `--check` 零新增漂移（FR-021、FR-022）。 [green: contracts/archive-actions.contract.md#C-114] [blockedBy: T039]
- [X] T041 [US3] 六动作 CLI 一致性测试（扩写 `tests/contract/test_seal_engine_contract.py`）：`--help` 列出六个动作、`--version` 一行身份零副作用、未声明选项 exit 2、无 `--force`/`--no-verify`/`--waive` 一类旁路；把读数记入 `test-evidence/us3-checkpoint.txt`（FR-008、SC-004）。 [green: contracts/archive-actions.contract.md#C-115] [P] [blockedBy: T005]
- [ ] T042 [US3] 074 真实回合 · 预览：运行 `python3 scripts/python/seal-utils.py --action archive-plan --spec-dir .specify/specs/074-goal-team-sdd-unification --repo . --json`，把完整负载（`would-archive`、移动对、台账计数、未解析 0、未分类 0）贴入 `test-evidence/074-archive-round.txt`（FR-001、FR-025）。 [blockedBy: T040,T041,T032]
- [ ] T043 [US3] 074 真实回合 · 执行并提交 archive 批次：运行 `--action archive-apply`；断言 074a/074b 落在 `.specify/specs/074-goal-team-sdd-unification/slices/` 下、文件数与逐文件 sha256 及相对路径集合与归档前一致（运行期探针，不写死计数）、`git diff --name-status -M HEAD` 在被移动分片路径集上全为重命名对（清单 A 与活引用载体 M 按声明集合断言）、`archive-manifest.json` 可复核、注册状态与封装结论不变；按显式路径提交 archive 批次（父 spec 树、`.specify/register.md`、`.specify/features/074-goal-team-sdd-unification.md` 活区、`shared/definitions/sdd-routing-definitions.md` 与镜像、`tests/contract/test_sdd_compat_containment.py`、`tests/contract/test_sdd_diffusion.py`、归档清单）（FR-002、FR-004、FR-025、SC-001）。 [blockedBy: T042]
- [ ] T044 [US3] 074 回合可复现：重跑 archive-plan（`already-archived` 结论、零待移动、零未解析）与 archive-apply（`already-archived`、零 diff）；重跑 seal 并断言阻断清单与归档前逐条一致；把读数追加到 `test-evidence/074-archive-round.txt`（FR-010、FR-026、SC-002）。 [blockedBy: T043]
- [ ] T045 [US3] US3 检查点：运行阻断态 + 命令面 + 回合套件（`tests/integration/test_seal_archive_round.py`、`tests/contract/test_seal_engine_contract.py`、`tests/contract/test_migration_distribution.py`），把读数记入 `test-evidence/us3-checkpoint.txt`（FR-001、FR-021、SC-004）。 [blockedBy: T044,T038,T041]

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 全量对照、镜像/副本终检、quickstart 实跑、记录收尾——跨全部故事的收口面。

- [ ] T046 全量套件零新增失败（GATE-1）：`bash scripts/bash/run-tests.sh --names-out .specify/specs/100-seal-slice-archive/test-evidence/final-failed.txt`，与实现入口基线名单（owner：`/speckit.implement` step 6 的 `**Test runs**`）做 `comm -13`，新增名单为空；读数存 `test-evidence/final-suite.txt`（FR-024）。 [P] [blockedBy: T045]
- [ ] T047 镜像与副本终检（GATE-2）：`python3 scripts/python/sync-mirrors.py --check` 相对 T001 基线零新增漂移（唯一既有 `DIFF` 仍是 `.specify/templates/gitignore-specify-template`）、`python3 scripts/python/regen-command-copies.py --check` exit 0；读数存 `test-evidence/final-mirrors.txt`（FR-021）。 [P] [blockedBy: T045]
- [ ] T048 quickstart 实跑：按 `quickstart.md` S-2…S-6 在夹具树与已归档的 074 树上执行 plan / apply / 重跑 / 阻断态 / 回滚走查，把真实输出与 teardown 贴入 `notes/quickstart-run.md`（FR-011、FR-022）。 [P] [blockedBy: T045]
- [ ] T049 SC → 首红模块追溯：产出 `test-evidence/sc-trace.txt`，逐条给出 SC-001…SC-010 的测试模块、红先读数与变异取证；只有措辞变化的检查不计为取证（FR-024）。 [green: contracts/archive-actions.contract.md#C-116] [blockedBy: T046]
- [ ] T050 落 `verification.md`：SC-001…SC-010 每条一行状态（`**Path**` 标记）、smoke 三键（`smoke_command` / `smoke_exit_code=0` / 证据路径）、`deferred_tasks=`；条件集按 `shared/workflow/acceptance-hardening.md` § Gates（FR-024、GATE-4）。 [blockedBy: T049]
- [ ] T051 Feature 注册表收尾：向 `.specify/features.md` 099 行与 `.specify/features/099-speckit-seal.md` 追加 2026-11-11 tasks 阶段叙述（不新建 Feature 行、状态保持 `Ready for Review`），并复核 Feature 列表（无新增 / 合并 / 失效）。 [P] [blockedBy: T045]
- [ ] T052 条款覆盖终局：`python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/100-seal-slice-archive` 对照 T003 冻结基线，确认 claimed 40、FR 28/28、uncovered beyond baseline 0；读数存 `test-evidence/coverage-final.txt`（FR-024）。 [blockedBy: T003,T049]
- [ ] T053 结构与重复机制审计：`ls templates/commands/*.md | wc -l` 仍为 31；仓库无**本特性新增的**第二套处置词表、第二归档引擎、第二份按 spec 清单或调度器（基线中既有的 sanitize 五值词表与 non-disposable 四值词表按原样保留）；读数存 `test-evidence/structure-audit.txt`（FR-027、SC-009）。 [P] [blockedBy: T045]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup（Phase 1）**: 无依赖，立即开始。
- **Foundational（Phase 2）**: 依赖 Setup；阻塞全部用户故事。
- **User Stories（Phase 3–6）**: 依赖 Foundational。同优先级 P1 的三条故事按实现依赖排序——US1（引擎核心）→ US2（引用面）→ US4（边界不变量）→ US3（流程接线与真实回合，最后）。
- **Polish（Phase 7）**: 依赖全部故事完成。

### User Story Dependencies

- **US1（P1）**: Foundational 后可开始；无故事内跨依赖。
- **US2（P1）**: 依赖 US1 的 plan/apply 骨架（T015–T017）；其分类/改写/台账行按 `[blockedBy:]` 串行进入同一引擎文件。
- **US4（P2）**: 依赖 US1 的 apply（T017、T019）与 Foundational 的发现（T008）；先于 US3，因为 US3 的流程接线消费其边界不变量（契约 C-112、C-113）。
- **US3（P1）**: 依赖 US2（T032）、US4（T035、T036）与命令面自身行；074 真实回合（T042–T044）按定义最后执行。

### Within Each User Story

- 红先测试行先于把它转绿的实现行；同一测试文件只由一个认领行持有绿点（其余写入行无 `[green:]`）。
- 同一引擎文件 `scripts/python/seal-utils.py` 的行按 `[blockedBy:]` 串行（写域相交），不标 `[P]`。
- 迁移/回归例外：守护既有行为的断言（如 `test_seal_boundaries.py` 的动作表审计）落在其消费对象之后并带显式 `[blockedBy:]`。

### Parallel Opportunities

- Setup 的 T001 与 T002 两行 `[P]` 并行；T003 在 T001 之后冻结基线。
- Foundational 的 T006 与 T007 `[P]` 并行（不同文件）；T008 随后。
- US1 的 T010–T014 五个测试/夹具行 `[P]` 并行（五个不同文件/目录）；实现行 T015 起串行。
- US2 的 T022 夹具行 `[P]`；实现行串行。
- US4 的 T033、T034、T036 `[P]` 并行（三个不同写域：回滚测试、边界测试、owner 文档）；T035 依赖 T034。
- US3 的 T038 与 T041 `[P]`；T039 起串行。
- Polish 的 T046、T047、T048、T051、T053 `[P]` 并行（五个不同证据/记录文件）。

## Parallel Example: User Story 1

```bash
# 五个测试/夹具行可同时启动（不同写目标）：
T010 -> tests/contract/test_seal_archive_plan.py
T011 -> tests/fixtures/seal-archive/clean-pair/ 与 empty/
T012 -> tests/contract/test_seal_archive_manifest.py
T013 -> tests/contract/test_seal_archive_apply.py
T014 -> tests/integration/test_seal_archive_idempotency.py
# 实现行随后按 blockedBy 串行进入同一引擎文件：
T015 -> T016 -> T017 -> T018 -> T019 -> T020 -> T021
```

```bash
# 全部测试经唯一入口（并行默认）：
bash scripts/bash/run-tests.sh tests/contract/test_seal_archive_plan.py tests/contract/test_seal_archive_manifest.py -q
```

## Implementation Strategy

### MVP First

1. Phase 1 Setup：冻结对照物。
2. Phase 2 Foundational：动作集与发现就位。
3. Phase 3 US1 + Phase 4 US2 + Phase 6 US3（三条 P1 故事共同构成 MVP；Phase 5 US4 的边界约束与 MVP 同批交付、先行落地）。
4. **STOP and VALIDATE**：按每条故事的 Checkpoint 独立验证；074 真实回合是最终验收。

### Incremental Delivery

1. Foundational 完成 → 引擎可接受六动作与归档后树。
2. US1 完成 → 夹具回放树上的归档零丢失、幂等可演示。
3. US2 完成 → 引用面 fail closed 可演示。
4. US4 完成 → 回滚与单一机制可审计。
5. US3 完成 → `/speckit.seal` 流程固化，074 真实回合产出入库。
6. Polish 完成 → 全量对照与记录齐备。

## Notes

1. **回滚测试文件裁定**：契约 C-116 的 SC-010 首红模块写作 `tests/integration/test_seal_archive_round.py`（含 rollback）。本阶段把回滚断言落在**独立文件** `tests/integration/test_seal_archive_rollback.py`（T033），理由是 `green-path-divergence`：同一测试路径被两个认领行（T018 的 C-107 与回滚行的 C-110）以不同绿点写入不可满足。round 文件继续承载回放/阻断态用例（T018 认领、T038 仅追加），回滚配方在独立文件执行；SC-010 的取证不变。
2. **074 真实回合的相位归属**：US1 的 Independent Test 提到「对 074 执行归档」；plan § Execution Model 的 `P4 → P7` / `P5 → P7` / `P6 → P7` 边要求回合晚于 apply、owner 修订与命令面，故真实回合行（T042–T044）落在 US3 阶段（其阻断态场景即 US3 验收场景 1）。US1 阶段保留夹具回放（T018）作独立可测面，两者共用同一引擎断言。
3. **夹具回放 vs 真实回合**：T018 在临时 git 树上复制 `clean-pair` 回放；T042–T044 才写入 `.specify/specs/074-goal-team-sdd-unification/` 真实树。测试 MUST NOT 写死 074 的文件数或哈希（clarify Q3），只在运行期比较归档前后相等。
4. **story 相位顺序**：US4（P2）先于 US3（P1）——plan 的依赖链要求 US3 的流程接线在边界不变量（C-112、C-113）之后；099 有同型先例（Phase 5 = US4、Phase 6 = US3）。
5. **运行期载体缺席**：本 worktree 无 `.specify/state/`，074 回合的 3 个运行期载体全部记 `absent`（不阻断）；主仓环境下为 2 更新 + 1 缺席。算术两种环境都成立（契约 C-309）。
6. **既有镜像漂移不修**：`.specify/templates/gitignore-specify-template` 的既有 `DIFF` 早于本特性且不在写面，按「不修、不掩」记录；本特性判据是触及的镜像对零新增漂移。
