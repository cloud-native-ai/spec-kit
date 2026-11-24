# Tasks: /speckit.team view — 团队结构与状态只读呈现（Team View）

**Requirement ID**: 103
**Requirement Key**: 103-team-view
**Related Feature**: 027 Team Management（`.specify/features/027-team-management.md`）— 本特性是同一 `/speckit.team` 命令面的第四模式（只读 `view`）。tasks 阶段按 Feature Integration Protocol 复查 Feature 列表：任务分解未暴露新 Feature、未使既有 Feature 失效；027 状态保持 `Implemented`，不回退（no-status-regression）。
**Input**: Design documents from `.specify/specs/103-team-view/`
**Prerequisites**: `requirements.md`（21 FR / 7 SC / 4 Shared Strings / Clarifications 2026-11-24 / RS-001…RS-005）、`plan.md`（Constitution Check 23/23 Pass、Decision Tensions N/A、Execution Premises EP-001…EP-003 全 verified、Mirror Obligations 3 行、Inherited Blockers = none）、`research.md`（B-01…B-20 / R-01…R-14 / U-01…U-04）、`data-model.md`（E1–E9 / INV-01…INV-14 / FR-021 Fixture Map）、`contracts/`（`team-view-command.contract.md` C-01…C-12、`view-team-skill.contract.md` C-13…C-23、`team-view-program.contract.md` C-24…C-38，共 38 条款）、`quickstart.md`（S-0…S-6）、`feature-ref.md`（Feature 027 绑定 + 19 路径交付面）

**Tests Mode**: ON — `.specify/constitution.md` Principle IV「Test-First & Contract-Driven Implementation」是 test-mandating 原则（"Write or update tests BEFORE implementing new behavior (Red-Green-Refactor)"、"Critical flows MUST have automated regression coverage"）；本特性交付可执行运行时（确定性只读程序 + 四份测试文件 + 一个 fixture 模块），因此 Principle IV 的 template-only 特例不适用——不得用结构契约断言代替程序行为测试。

**Tests**: MANDATORY。红先证据落在 `.specify/specs/103-team-view/notes/red-first-evidence.md`；实现读数落在 `.specify/specs/103-team-view/test-evidence/`。所有测试只经唯一入口 `scripts/bash/run-tests.sh`；本文件不写解释器级测试命令（FR-021）。

**Organization**: 四条用户故事（US1 P1 / US2 P1 / US3 P2 / US4 P3）各一阶段，按 `requirements.md` 优先级排序；共享 fixture 构建模块作为 Foundational 阻塞前置；技能、命令模板与文档按 doc-feature 分类法「author-section → mirror-parity → render-verify」成对落行（镜像/副本只经生成器）。

**Row count and ID shape**: 44 task rows, `T001`…`T044`, one ID per row, no gaps, contiguous in execution order.

## Definition of Done (DoD)

- DoD-1: **FR lane 完整** — FR-001…FR-021 每条都被至少一个任务行按 `pre-analyze-check.py` 认可的形态引用（`- [ ] T<NNN>` 行内出现该 id；表格单元或散文不算），其中 `in-scope` 行 RS-005 点名的 FR-014 / FR-021 逐条在行内被引用。Check: `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/103-team-view --stage tasks --repo .` 的 summary 中 `errors=0`。
- DoD-2: **SC lane 有传感器** — SC-001…SC-007 每条都有具名任务行与证据路径；`**Path**: final` 的判据（SC-001 / SC-002）必须拿到 `pass` 读数并在 `verification.md` 带 smoke 三字段，`supporting` 判据（SC-003…SC-007）按真实读数如实取值，取不到时记 `not-evaluated` 与原因。
- DoD-3: **三份契约 38 条款各有守卫** — 每条 `C-NN` 由其 pinning test 文件断言（命令接线 C-01…C-12 → `tests/contract/test_team_view_command.py`；技能 C-13…C-23 → 命令接线 + 集成 + 程序契约三面；程序 C-24…C-38 → `tests/contract/test_team_view_program_contract.py` + `tests/integration/test_team_view_program.py`），fixture 形态覆盖 data-model § FR-021 Fixture Map 全表。
- DoD-4: **只读可判定** — 一次 view 前后 fixture 工作树 path+sha256 快照一致（新增/修改/删除 0），无 run line 登记、无席位派发、无引擎写动作调用（测试断言 + 源码只读扫描，INV-01、C-24、C-36）。
- DoD-5: **镜像与副本是生成的** — `scripts/`、`skills/internal/`、`shared/` 三对与四个 per-tool 副本全部经生成器产出（`sync-mirrors.py` / `regen-command-copies.py`），`--check` 相对 T003 记录的基线无新增漂移；`.specify/**` 未手改（C-12、C-23、FR-019）。
- DoD-6: **零新增机制与依赖** — 无第二团队存储/缓存/快照/registry；`goal-utils.py` 与 `pyproject.toml` 零改动；无第三方 import；程序不声明 `--target`；不调用 `run-checks`（RS-004、INV-14、FR-019、A-5）。
- DoD-7: **文档同步与漂移校正** — `docs/reference/commands/team.md` 四模式 + `## View Mode` 小节 + 两处 run 模式漂移校正；两个具名文件的模式表各 4 行且 `[[STR-004]]` 实时出现 0 次（SC-005、C-07、C-08、C-10）。
- DoD-8: **范围与纪律** — 完整变更集 ⊆ `feature-ref.md` § Delivery surface（含其第 19 项 probe 注册面）；既有脏文件不提交不还原；不 push；probe registry 经 `--validate` 与 `--reconcile` 双绿。

**DoD Status**: pending

## Completion Gate

- GATE-1: 定向测试集零**新增**失败——按失败用例 id 名与 implement 入口基线做集合差，不用计数比较。Check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/103-team-view/final-failed.txt tests/unit/test_team_view_parsers.py tests/contract/test_team_view_command.py tests/contract/test_team_view_program_contract.py tests/integration/test_team_view_program.py -q` 后 `comm -13 <implement 入口基线名单> .specify/specs/103-team-view/final-failed.txt` 为空；基线名单的路径与采集形态归 `/speckit.implement` 的 `**Test runs**` bullet（`skills/internal/implement-feature/SKILL.md`），本文件不复述、不另立第二路径。
- GATE-2: 每条镜像义务成立——`python3 scripts/python/sync-mirrors.py --check` 中本特性三对（`scripts/ == .specify/scripts/`、`skills/internal/ == .specify/skills/internal/`、`shared/ == .specify/shared/`）行均为 `ok` 且相对 T003 基线无新增漂移；`python3 scripts/python/regen-command-copies.py --check` rc 0。
- GATE-3: 结构与 FR lane 静默——`python3 .specify/scripts/python/validate-tasks.py .specify/specs/103-team-view/tasks.md` exit 0；`python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/103-team-view --stage tasks --repo .` 的 `decision=pass`（errors=0）；`python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/103-team-view/requirements.md --tasks .specify/specs/103-team-view/tasks.md` 的 JSON `"decision": "proceed"`。
- GATE-4: 每条 `final` 路径成功判据为 `pass` **且**本特性的 smoke 记录在位——check: `verification.md` 中每个 `**Path**` 标记为 `final` 的判据都有 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（路径存在且非空）三项齐备；任一 `final` 判据为 `blocked` / `deferred` / `fail` 即本门失败，除非有具名用户豁免。条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates（本行只携带检查，不复述阈值）。
- GATE-5: 只读证明在位——`tests/integration/test_team_view_program.py::test_view_leaves_tree_byte_identical`（或实现期最终名）在定向集中为 pass，且 `verification.md` 引用其快照读数（SC-002、INV-01）。

## Environment Prerequisites

探测日期 2026-11-24，工作区 `/storage/project/cloud-native-ai/spec-kit`。每一行都以此处判决为唯一落点；任何其它载体（阶段注记、`[~]` 注记、散文行）只写日期 + `(see § Environment Prerequisites)` 指针，不复述判决。

- CPython `>=3.8`（程序与 fixture 模块，仅标准库）：**available** — probe: `python3 --version` → `Python 3.11.11`；`pyproject.toml` 声明下限 `requires-python = ">=3.8"` @ 2026-11-24；affects: 全部程序实现行与测试行。
- POSIX `bash`（唯一测试入口）：**available** — probe: `bash --version | head -1` → `GNU bash, version 4.4.20(1)-release` @ 2026-11-24；affects: 每个测试执行行。
- `pytest` + `pytest-xdist`（经唯一入口 `scripts/bash/run-tests.sh` 的并行默认）：**available** — probe: `python3 -m pytest --version` → `pytest 8.4.2`；`python3 -c "import xdist; print(xdist.__version__)"` → `3.8.0` @ 2026-11-24；affects: 每个测试执行行。
- `git`（范围审计与提交）：**available** — probe: `git --version` → `git version 2.43.5` @ 2026-11-24；affects: T040、T044。
- 既有确定性工具链（覆盖会计 / 任务结构校验 / 阶段门禁 / probe 引擎 / 镜像生成器）：**available** — probe: `--version` 各返回 `0.0.22`（`account-clause-coverage.py`、`validate-tasks.py`、`pre-analyze-check.py`、`probe-utils.py`），`sync-mirrors.py --check` 与 `regen-command-copies.py --check` rc 0 @ 2026-11-24；affects: T002、T003、T015、T030、T039、T043。
- 既有 `goal-utils.py` 引擎只读动作面：**available** — probe: `python3 scripts/python/goal-utils.py --version` → `goal-utils.py 0.0.22` @ 2026-11-24；affects: T011、T012（`binding` / `list` / `targets --list` 三个读动作）。
- 容器 / 集群 / 网络 / 特殊硬件：**不需要**（本特性零联网、零容器、零远程调用、零席位派发）。

**A13 boundary**（owner：`shared/workflow/acceptance-hardening.md` § Gates —— 本节只是指针，不是第二条规则）：本小节只记**任务生成时的探测判决**，每条带探测命令与 ISO 日期。规划期的承重前提归 `plan.md` § Execution Premises（EP-001…EP-003），本文件不复述其取值；同名事实只在本节出现一次。

## Format

每行一条、**单行不折行**，形如 `- [ ] T<NNN> [P?] [US<n>?] 动作 + 文件路径 + 验收 + (FR/SC 引用) + 依赖键`。占位符语义归 `templates/tasks-template.md` § Format，本文件不复述。

- `[P]` 只标在**写目标**与本阶段其它 `[P]` 行互不相交的行上（同一文件、同一镜像对都算冲突）；同一证据文件被两行追加时不得标 `[P]`。
- 依赖键只在存在具体前置时使用，取值为逗号分隔、必须是本文件已定义的**更早**任务 id；前向引用不写。
- 本文件**不使用** `[green: <contract>#<clause>]` 归属标签，理由见 § Notes N-1；条款级归属由「契约文件 ↔ pinning test 文件」一一对应承担，FR 级可追溯性由 DoD-1 的逐行引用承担。
- 需要落盘证据的行以 `write: <path>` 结尾标注主写目标；`write:` 之外引用的路径默认是读面或工具路径。

## Premises measured at generation time (2026-11-24)

| 量 | 实测 | 复现命令 | 朴素形态的陷阱 |
|----|------|----------|----------------|
| 团队档案规模 | 20 个团队目录 / 20 份 `team.md` | `ls -d .specify/teams/*/ \| wc -l` 与 `ls .specify/teams/*/team.md \| wc -l` | 把 `.work/` 或临时目录纳入根会多算；本仓当前两者一致 |
| 运行报告 | 46 个 `runs/*.md`，其中 41 个匹配契约名 `*-report.md`、5 个为契约外文件名（`-seat-result.md`、`-verification.md`、`-progress-snapshot.md` 等） | `ls .specify/teams/*/runs/*.md \| wc -l` 与 `ls .specify/teams/*/runs/*-report.md \| wc -l` | 只数 `*-report.md` 会得 41 并把 5 个非契约名当成不存在；E5 的 `unrecognized` 分支正是为它们准备的 |
| 台账 | 5 份 `items.jsonl`（含 1 份零行文件 `viz-skill-arena`） | `ls .specify/teams/*/items.jsonl \| wc -l` | 零行文件是「存在但为空」，不是「缺失」（B-04） |
| 持续运营脊柱 | 3 份 `constraints.md` | `ls .specify/teams/*/constraints.md \| wc -l` | — |
| 陈旧字面量 | `exactly three modes` 在 6 个文件各 1 次：模板、文档、四个 per-tool 副本 | `grep -c 'exactly three modes' <file>` | `grep -c` 零命中时退出 1，链式命令需 `\|\| true`；按文件数 6 与按总出现数 6 在此相同，别处未必 |
| argument-hint | 模板当前 0 命中；`templates/commands/anchor.md`（7 模式）与 `goal.md`（4 模式）是兄弟先例 | `grep -c 'argument-hint' templates/commands/team.md` | 把 anchor 的 hint 形态照抄到 team 会漏 `--target` |
| 待建交付物 | `scripts/python/team-view.py`、`skills/internal/view-team/`、5 份 tests 路径全部不存在 | `test -e <path>` | 把它们当既有文件会写出「扩展既有文件」的假前提 |
| docs 漂移字面量 | 三个假断言各 1 次（`never executes before you confirm` / `Only then does orchestration run` / `Declining stops without executing`）；run 委派单元格为带反引号的 `create-team` (execution path) | `grep -c -F <literal> docs/reference/commands/team.md` | 按 `-F 'create-team (execution path)'` 会因反引号漏配；按 `create-team` 搜会同时命中多处合法引用 |
| 引擎与运行时 | `goal-utils.py 0.0.22`；CPython 3.11.11（pyproject 下限 `>=3.8`）；pytest 8.4.2 + xdist 3.8.0；bash 4.4.20；git 2.43.5 | 各 `--version` 探针 | 用等值 pin（`startswith("0.0.22")`）会在合法升级时误红；pin 用下限语义 |
| 分发基线 | `sync-mirrors.py --check` rc 0（五对镜像 + 六投影 + 副本全 ok）；`regen-command-copies.py --check` rc 0；`probe-utils.py --action compile-embeds --check` → `85 units, zero drift`；`probes --validate` rc 0；`probes --reconcile` → zero-gap（129 internal objects / 86 embeds） | 各命令原样 | 把「改动前 rc 0」当「改动后依然 rc 0」是没读；改动后只许与 T003 基线比较 |
| 示例团队 | `.specify/teams/cws-workspace-cluster/`（含 runs/、台账外脊柱）与 `.specify/teams/086-efficient-test-execution/` 存在 | `test -d <path>` | — |

## Phase Map

| Phase | 用户故事 | 目的 | 行 |
|-------|----------|------|----|
| 1 Setup | — | 证据落点与四类生成时基线（测量、条款覆盖、分发） | T001–T003 |
| 2 Foundational | — | 共享 fixture 构建模块（tmp_path 团队树 + 只读快照 oracle） | T004 |
| 3 US1 (P1) | 单团队六组信息 | 程序红→绿、技能、命令入口、probe 注册、双镜像 | T005–T019 |
| 4 US2 (P1) | 无 slug 概览 | 概览红→绿、envelope 键、镜像复同步 | T020–T025 |
| 5 US3 (P2) | 只读边界与路由不串线 | 路由/默认/歧义接线 + 文档四模式与漂移校正 + 副本再生成 | T026–T031 |
| 6 US4 (P3) | 错误路径可行动导航 | 未知 slug / 空档案 / 损坏定义红→绿、镜像复同步 | T032–T036 |
| 7 Polish | — | quickstart 实跑、定向总跑、分发与范围审计、`verification.md`、收尾门禁、提交 | T037–T044 |

---

## Phase 1: Setup — 证据落点与生成时基线

**Purpose**: 在动手前把后续所有读数行的对照面固定下来；没有基线的结论一律记 `not-evaluated`。

- [X] T001 建立本规格的证据落点，并把本文件 § Premises 的生成时复测（20 团队 / 46 份 `runs/*.md` 与 41 份 `*-report.md` 两读数、5 台账含 1 零行、3 脊柱、6 文件各 1 次陈旧字面量、模板 argument-hint 0 命中、7 个待建交付物全 absent、三个 docs 假断言各 1 次、`goal-utils.py 0.0.22`、CPython 3.11.11 / pytest 8.4.2 + xdist 3.8.0 / bash 4.4.20、镜像与副本基线 rc 0、compile-embeds 85 units zero drift、probe validate rc 0 与 reconcile zero-gap、两个示例团队存在、既有脏文件清单）逐条带命令与采集日期写入 `notes/pre-change-measurements.md`；同时建立 `notes/` 与 `test-evidence/` 两个目录（FR-021）。write: `.specify/specs/103-team-view/notes/pre-change-measurements.md`
- [X] T002 [P] 冻结本特性的条款覆盖基线：`python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/103-team-view --freeze > .specify/specs/103-team-view/coverage-baseline.txt`，记录 38 条款所在的三份契约与「claimed=0（本文件不用 `[green:]`，理由见 N-1）」的裁决，作为收尾判决「覆盖面无退化」的对照面（FR-021）。write: `.specify/specs/103-team-view/coverage-baseline.txt`
- [X] T003 [P] 采集分发一致性基线到 `test-evidence/mirror-baseline.txt`：`python3 scripts/python/sync-mirrors.py --check`（rc 0，五对镜像 + 六投影 + per-tool 副本全 ok）与 `python3 scripts/python/regen-command-copies.py --check`（rc 0）逐字落盘；同文件记录 `python3 scripts/python/probe-utils.py --action compile-embeds --check`（`85 units, zero drift`）、`probe-utils.py --action probes --validate`（rc 0）与 `--action probes --reconcile`（zero-gap，129 internal objects / 86 embeds）三项读数（FR-019；C-22）。write: `.specify/specs/103-team-view/test-evidence/mirror-baseline.txt`

**Checkpoint**: 测量、覆盖、分发三类基线与两份证据目录就位；后续每一行都能引用一条已落盘读数。

---

## Phase 2: Foundational — 共享测试底座

**Purpose**: 所有用户故事的测试都依赖同一个 fixture 构建模块与只读 oracle；先把它落地，四条故事才能各自红→绿。本阶段只此一项，故无并行行。

- [X] T004 编写 fixture 构建模块 `tests/fixtures/team_view_fixtures.py`：暴露 `build_team(root, slug, *, frontmatter=<dict|raw text>, body=<str|None>, reports=((name, text), …), items_lines=(json line | raw, …), spine=(filename, …), corrupt=None) -> Path` 与 `snapshot(root) -> {relative_path: sha256}` 两个 helper；所有团队树建在 pytest `tmp_path` 下，绝不写 `.specify/teams/`（R-13；FR-021；SC-002 的 oracle 面）。write: `tests/fixtures/team_view_fixtures.py`

**Checkpoint**: fixture 模块可被后续四份测试文件 import，且只读快照 helper 就位。

---

## Phase 3: User Story 1 — 一次查看看懂一个团队的全部结构与状态 (Priority: P1) 🎯 MVP

**Goal**: 交付 `team-view.py` 的单团队六组呈现（身份与绑定 / 静态结构 / 动态结构 / 持久化清单 / 最近运行状态 / 归档层引用）、只读技能 `view-team` 与 `/speckit.team view` 入口；缺失三态显式标注，一次运行后工作树零变更。

**Independent Test**: 在含完整定义、运行报告与台账的 fixture 团队上执行一次 view，断言六组信息各自出现且成员/报告覆盖数等于 fixture 实际数；同一 fixture 查看前后 path+sha256 快照一致（SC-001 / SC-002）。

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T005 [US1] 编写解析单元测试 `tests/unit/test_team_view_parsers.py`：frontmatter 封闭子集（标量 / 行内列表 / 有界嵌套 map / `members` 的 block sequence of maps；子集外形态 → 该事实 `不可读`/`形态异常`，不猜值）、`## Static Structure` 表解析（缺列或重复必需列 → `不可读`）、报告段提取（`## Result Summary` / `## Verification` / `## Nested SDD Runs` 的 anomalies 值 / `**Target 指派**` 行）、台账聚合（IL-2 末事件定态、同 `ts` 按文件序、坏行计数、非终态项）；经 import 读取程序的纯函数，不启动子进程（C-32、C-33、C-35；FR-009, FR-011, FR-012, FR-015）。write: `tests/unit/test_team_view_parsers.py`
- [X] T006 [US1] 编写程序接口契约测试 `tests/contract/test_team_view_program_contract.py` 的第一段：`-h`/`--help`/`--version` 退出 0 且运行前后工作树零写、未声明选项（含 `--target`）退出 2、多余位置参数退出 2、非法 `--scope` 与无 slug `auto` 退出 2、`anchor`/`goals` 明确 not-applicable 退出 2、退出码闭集 0/2/3/4/5、源码或行为上不调用 `run-checks`、`--json` 顶层键集（`tool`/`version`/`mode`/`repo_root`/`scope`/`as_of`/`overview`/`team`/`errors`/`degraded`）（C-24、C-26、C-27、C-28、C-29；FR-005, FR-014；INV-14；A-5, A-7）；测试名 `test_undeclared_target_option_rejected` 在位（quickstart S-5 的钉）。write: `tests/contract/test_team_view_program_contract.py`
- [X] T007 [P] [US1] 编写接线契约测试 `tests/contract/test_team_view_command.py` 的第一段：模板 frontmatter 的 `description` 含 view、`short-description` 含四模式、`argument-hint` 逐字 [[STR-003]]；模式表恰好四行且顺序 create/modify/run/view、view 行识别意图组与委派 `view-team`；[[STR-004]] 0 次；`### View Mode` 小节陈述只读边界、委派路径 `.specify/skills/internal/view-team/SKILL.md`、无 slug=概览、精确 slug、未知 slug=[[STR-001]]+create 建议、损坏定义点名路径、`--target` 模式/参数冲突、五查与 `blocked` 归 run-team、固定提取在 `scripts/python/team-view.py`；测试名 `test_view_target_conflict_declared` 在位（C-01、C-02、C-03、C-06、C-11；FR-001, FR-002, FR-003, FR-004）。write: `tests/contract/test_team_view_command.py`
- [X] T008 [P] [US1] 编写集成测试 `tests/integration/test_team_view_program.py` 的第一段：完整团队六组标题按序出现且成员行/报告名全覆盖（SC-001）、最小团队三处 `缺失` 且无编造零值、遗留 `goal_slug` 披露 legacy、缺失 `anchor_slug` 披露 inferred、archived 正常呈现、台账坏行计数不中断、正文矩阵与 frontmatter 名册差异并列、>20 报告截断并报省略数、`as-of:` 行来自文件时间、`--json` 与默认渲染同源；只读快照前后一致（SC-002）；全部经 `--repo-root` 指向 tmp fixture（C-29、C-30、C-31、C-33、C-34；FR-004, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-015, FR-016, FR-020；SC-006；INV-01、INV-03、INV-07、INV-08、INV-10、INV-12、INV-13）；测试名 `test_single_team_renders_six_groups` 与 `test_view_leaves_tree_byte_identical` 在位。write: `tests/integration/test_team_view_program.py`
- [X] T009 [US1] 在实现之前先跑 T005–T008 并把红读数（命令、真实输出、退出码；被测文件尚不存在 → 逐条真红）写入 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/103-team-view/notes/red-first-evidence.md` [blockedBy: T005,T006,T007,T008]

### Implementation for User Story 1

- [X] T010 [US1] 实现 `scripts/python/team-view.py` 的接口与身份面：经 `scripts/python/script_interface_cli.py` 的 `configure_parser` / `VersionAction` / `version_text` 装配 `-h`/`--help`/`--version`（零副作用）；`--repo-root` 缺省按程序自身解析路径中的字面 `.specify` 组件自定位（两顶帽子规则，`shared/definitions/dogfooding-definitions.md` § 2.1）；`--scope` 闭集处理（`teams` 服务、`auto` 仅单 slug 且身份可解析、`anchor`/`goals` 与无 slug `auto` 具名拒绝退出 2）；退出码闭集 0/2/3/4/5（C-26、C-27、C-28；FR-005；R-08、R-09）。write: `scripts/python/team-view.py` [blockedBy: T009]
- [X] T011 [US1] 在 `scripts/python/team-view.py` 实现定义事实与静态/动态结构：封闭子集 frontmatter 解析器（C-35）；E2（name/slug/description、lifecycle 缺省按 owner 读作 active、binding 经引擎 `binding team <slug> --json` 只读取得、anchor 身份 declared/legacy/inferred 披露、`handoff_ref`、`其它声明键`）；E3（正文矩阵逐行、frontmatter `members`、`seats`/`stage_seats`、`roster_delta` 两侧并列、Type 只来自正文矩阵）；E4（pattern、`config` 全部声明键逐条呈现、schema 命名可选键 `已声明`/`未声明（默认值见 create-mode.md § Schema notes）`、`focus_target`）（C-25、C-36；FR-008, FR-009, FR-010, FR-020；RS-004、A-18、R-10）。write: `scripts/python/team-view.py` [blockedBy: T010]
- [X] T012 [US1] 在 `scripts/python/team-view.py` 实现持久化清单、最新报告有界摘要与归档层引用：E5（团队目录、`runs/` 全部文件名逆时序 + 总数 + 最新 20 + 省略数与 `未识别` 名单、`items.jsonl` 存在性/行数/按状态计数/坏行/非终态、三件脊柱文件存在性、summary 送达位置按声明）；E6（最新报告 Outcome、`**Target 指派**` 行、Result Summary 与 Verification 的有界摘录（10 行或 800 字符先到者，截断标记 `…（截断）`）、Nested SDD Runs 的 anomalies 值、未记录不渲染成「无异常」）；E7（engine `list --json` 与 `targets <anchor> --list --json` 的锚点身份/lifecycle/判据数/Target 列表，悬空标 `悬空（dangling）` + 原因，不复制 objective 或判据正文）（C-25、C-32、C-33、C-36；FR-011, FR-012, FR-013；R-05、R-06、R-07；RS-004）。write: `scripts/python/team-view.py` [blockedBy: T011]
- [X] T013 [US1] 在 `scripts/python/team-view.py` 实现默认渲染与 `--json` 包络：六组标题 `## 1. 身份与绑定` … `## 6. 其他归档层引用` 按 FR-008…FR-013 顺序、标签词汇取 data-model § Rendering Line Types 的封闭集（`缺失`/`为空`/`不可读`/`未记录` 绝不互相替代、缺失不渲染 `0`）、`as-of: <max_file_mtime_utc>（文件时间；非实时探测）`、E9 envelope 键集与渲染同源派生（C-29、C-30、C-34；FR-014, FR-016；A-5、INV-03、INV-09）。write: `scripts/python/team-view.py` [blockedBy: T012]
- [X] T014 [US1] 编写 `skills/internal/view-team/SKILL.md`：Input Contract（`view [team-slug]`、精确 slug、`--scope`/`--spec-dir` 透传、`--target` 冲突前置拒绝）、一次委派、逐字完整呈现（六组不删/不并/不改序，不加第二格式）、无条件只读、不是 run 预览、错误导航闭集（exit 0/2/3/4/5 的逐行动作）、措辞义务与边界（不承接 create/modify/run、不服务单代理）；末尾以 `python3 scripts/python/probe-utils.py --action compile-embeds` 生成 `## Wrap-up` 且 `--check` rc 0（C-13…C-22；FR-003）。write: `skills/internal/view-team/SKILL.md` [blockedBy: T009]
- [X] T015 [US1] 在 `shared/definitions/probe-definitions.md` § Objects 注册新技能的 wrap-up 探针对象：按既有 `skill-*-wrapup` 同形加入 `skill-view-team-wrapup | skill-wrapup | skill:view-team | wrap-up`，以 `python3 scripts/python/sync-mirrors.py --write --only shared` 投影到 `.specify/shared/definitions/probe-definitions.md`；验收 `probe-utils.py --action probes --validate` rc 0 且 `probe-utils.py --action probes --reconcile` 仍 zero-gap（否则新技能的 compile 嵌入会报 `embed without probe object`）（C-22；FR-019）。write: `shared/definitions/probe-definitions.md` [blockedBy: T014]
- [X] T016 [US1] 在 `templates/commands/team.md` 落地 view 入口（author-section）：frontmatter `description` 改为四个团队操作含 view、`short-description` 列四模式、新增 `argument-hint` 逐字 `[[STR-003]]` 的值；模式表加第四行（view 意图组 → `view-team`）；新增 `### View Mode` 小节，按 C-06 的五个要点委派到 `.specify/skills/internal/view-team/SKILL.md`，模板不内联呈现逻辑、不枚举六组字段（C-01、C-02、C-06；FR-001, FR-003, FR-004）。write: `templates/commands/team.md` [blockedBy: T009]
- [X] T017 [US1] 经唯一入口把 US1 转绿并记录读数：`bash scripts/bash/run-tests.sh tests/unit/test_team_view_parsers.py tests/contract/test_team_view_program_contract.py tests/contract/test_team_view_command.py tests/integration/test_team_view_program.py -q --names-out .specify/specs/103-team-view/test-evidence/us1-failed.txt`，命令、rc、通过/失败数与耗时写入 `us1-green.txt`（FR-021）。write: `.specify/specs/103-team-view/test-evidence/us1-green.txt` [blockedBy: T013,T014,T016]
- [X] T018 [US1] 投影程序镜像并验证：`python3 scripts/python/sync-mirrors.py --write --only scripts` 把 `scripts/python/team-view.py` 落到 `.specify/scripts/python/team-view.py`；`python3 scripts/python/sync-mirrors.py --check --only scripts` 的 `scripts/ == .specify/scripts/` 行为 `ok`，`diff -q` 空输出；镜像不得手改，读数落盘（FR-019）。write: `.specify/scripts/python/team-view.py` [blockedBy: T017]
- [X] T019 [US1] 投影技能镜像并验证：`python3 scripts/python/sync-mirrors.py --write --only skills/internal` 把 `skills/internal/view-team/SKILL.md` 落到 `.specify/skills/internal/view-team/SKILL.md`；`--check --only skills/internal` 的 `skills/internal/ == .specify/skills/internal/` 行为 `ok`，`diff -rq` 空输出（C-23；FR-019）。write: `.specify/skills/internal/view-team/SKILL.md` [blockedBy: T014]

**Checkpoint**: 单团队 view 在 fixture 上六组齐全、三态诚实、只读可证；技能与命令入口就位，双镜像与 probe 注册同步——US1 可独立演示（MVP 前半）。

---

## Phase 4: User Story 2 — 不记得 slug 时先看全部团队 (Priority: P1)

**Goal**: 无 slug 的 view 输出按 slug 升序的全团队概览（每行含 slug / 名称 / pattern / lifecycle / 绑定锚点身份 / 更新日期 / 最近运行日期），档案为空时显式输出 [[STR-002]]。

**Independent Test**: 在含两个可读团队的 fixture 上执行无参数 view，断言两行且顺序确定；在空档案 fixture 上执行，断言 [[STR-002]] 且 exit 0。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T020 [P] [US2] 追加概览集成测试段到 `tests/integration/test_team_view_program.py`：两团队 fixture 每团队一行且 slug 升序、列覆盖七个字段、无运行团队 `最近运行: 未记录`、空档案输出 [[STR-002]] 且 exit 0；使用 T004 的 builder 与 snapshot helper（C-29、C-31、C-32；FR-007；INV-04）。write: `tests/integration/test_team_view_program.py` [blockedBy: T017]
- [ ] T021 [P] [US2] 追加概览 envelope 断言到 `tests/contract/test_team_view_program_contract.py`：`--json` 的 `mode=overview`、`overview.rows[].slug` 升序、`overview.total` / `overview.corrupt_total` 键在位（C-29；FR-007；E9）。write: `tests/contract/test_team_view_program_contract.py` [blockedBy: T017]
- [ ] T022 [US2] 先跑 T020 / T021 并把红读数（概览尚未实现）写入 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/103-team-view/notes/red-first-evidence.md` [blockedBy: T020,T021]

### Implementation for User Story 2

- [ ] T023 [US2] 在 `scripts/python/team-view.py` 实现概览模式：扫描 `.specify/teams/*/` 的目录名作为排序键，每目录一行 E8（名称/pattern/lifecycle 缺省读 active/绑定锚点身份含 legacy 与 inferred 披露/updated/最新报告文件名时间戳或 `未记录`），空档案输出 [[STR-002]] 且 exit 0；概览不调用引擎读动作（R-04；C-31、C-32；FR-007）。write: `scripts/python/team-view.py` [blockedBy: T022]
- [ ] T024 [US2] 经唯一入口转绿并记录读数：`bash scripts/bash/run-tests.sh tests/contract/test_team_view_program_contract.py tests/integration/test_team_view_program.py -q --names-out .specify/specs/103-team-view/test-evidence/us2-failed.txt`，rc 与读数写入 `us2-green.txt`（FR-021）。write: `.specify/specs/103-team-view/test-evidence/us2-green.txt` [blockedBy: T023]
- [ ] T025 [US2] 复同步程序镜像并验证：`python3 scripts/python/sync-mirrors.py --write --only scripts` 后 `--check --only scripts` 为 `ok`、`diff -q` 空输出（FR-019）。write: `.specify/scripts/python/team-view.py` [blockedBy: T024]

**Checkpoint**: 无 slug 的概览在 fixture 上确定排序、空档案显式声明——US2 可独立验证（MVP 后半）。

---

## Phase 5: User Story 3 — 查看就是查看：只读边界与路由不串线 (Priority: P2)

**Goal**: 查看类意图稳定落到 view、create/modify/run 意图 0 条落到 view、歧义输入只报四项能力不执行任何模式；`docs/reference/commands/team.md` 同步四模式并在同一变更中校正两处 run 模式陈述漂移。

**Independent Test**: 路由样例集经命令接线逐条断言（view 命中率 100%、非查看意图落 view 0 条、歧义执行模式 0 条）；两个具名文件各 4 个模式且 [[STR-004]] 实时出现 0 次（SC-003 / SC-005）。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T026 [US3] 追加路由与文档断言段到 `tests/contract/test_team_view_command.py`：C-09 七条路由样例的确定性代理断言（每条样例的特征 token 出现在其期望模式的表行、view 特征 token 不出现在 create/modify/run 行）、C-04 三条不变量（create/modify/run 不落 view、歧义非空输入只报四项能力且不执行、`--target` 视为模式/参数冲突）、C-05 默认行为能力摘要四模式、C-07 文档四模式 + `## View Mode` 小节 + Companion Skills 含 `view-team`、C-08 两处漂移与三个假断言字面量各 0 次、C-10 两文件四模式且 [[STR-004]] 0 次、C-12 不存在 `.specify/templates/commands/` 镜像；测试名 `test_view_target_conflict_declared` 与路由样例逐条覆盖（FR-002, FR-017；SC-003, SC-005；C-04、C-05、C-07、C-08、C-09、C-10、C-12）。write: `tests/contract/test_team_view_command.py` [blockedBy: T017]
- [ ] T027 [US3] 先跑 T026 并把红读数（路由流、默认行为与文档尚未同步）写入 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/103-team-view/notes/red-first-evidence.md` [blockedBy: T026]

### Implementation for User Story 3

- [ ] T028 [US3] 在 `templates/commands/team.md` 补路由（author-section）：Routing flow 首步模式分类加入 `view`、新增 view → `view-team` 的委派步与 `--target` 冲突步；Default Behavior 第 3 步能力摘要列出 create/modify/run/view 四模式（默认行为仍是信息序列，不得变成隐式 view 执行）；Ambiguous 能力清单加 view 一项并保持「不猜」契约（C-04、C-05；FR-001, FR-002）。write: `templates/commands/team.md` [blockedBy: T027]
- [ ] T029 [US3] 同步 `docs/reference/commands/team.md`（author-section）：开头段与 When to Use 改为四模式、Syntax 与四行模式表加入 view、run 委派单元格改为 `run-team`、新增 `## View Mode` 小节（只读 / 无 slug 概览 / 精确 slug / `team not found` + create 建议 / 损坏定义点名路径 / 不是 run 预览的边界）、Companion Skills 加 `view-team`；同一变更内校正两处 run 模式漂移——run 委派对象改为 `run-team` 技能、预览改为「披露而非阻断门禁」，删除三个假断言字面量（C-07、C-08；FR-017；SC-005）。write: `docs/reference/commands/team.md` [blockedBy: T027]
- [ ] T030 [US3] 经生成器再生成四个 per-tool 命令副本：`python3 scripts/python/regen-command-copies.py --write` 产出 `.claude/commands/speckit.team.md`、`.github/prompts/speckit.team.prompt.md`、`.qoder/commands/speckit.team.md`、`.opencode/command/speckit.team.md`，随后 `--check` rc 0；四个副本各含 `view` 且 [[STR-004]] 0 次，副本不得手改（C-12；FR-001, FR-017）。write: `.claude/commands/speckit.team.md`, `.github/prompts/speckit.team.prompt.md`, `.qoder/commands/speckit.team.md`, `.opencode/command/speckit.team.md` [blockedBy: T028]
- [ ] T031 [US3] 经唯一入口把接线契约转绿并记录 SC-005 复算读数：`bash scripts/bash/run-tests.sh tests/contract/test_team_view_command.py -q` 全绿（该文件此时含 C-01/C-02/C-03/C-06 段与 C-04…C-12 段）；对两个具名文件以程序统计模式数与 [[STR-004]] 出现数（各 4 / 各 0）写入 `us3-green.txt`（FR-021；SC-003, SC-005）。write: `.specify/specs/103-team-view/test-evidence/us3-green.txt` [blockedBy: T029,T030]

**Checkpoint**: 四模式接线与文档一致、路由样例全绿、陈旧字面量清零——US3 可独立验证。

---

## Phase 6: User Story 4 — 团队不存在时给出可行动的导航 (Priority: P3)

**Goal**: 未知 slug 输出 [[STR-001]] + 有界可用清单（超 20 报省略数）+ create 建议（exit 3）；空档案同时输出 [[STR-002]]；目录存在而 `team.md` 缺失/不可解析时报「定义损坏」并点名路径（exit 4），绝不与「不存在」互换，概览中损坏行照常列出并标注。

**Independent Test**: 对不存在的 slug 执行 view，断言错误字面量与建议；对「目录存在但 team.md 缺失」和「frontmatter 不可解析」两个损坏变体执行 view，断言报告的是损坏而非不存在（SC-004）。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T032 [US4] 追加错误路径集成测试段到 `tests/integration/test_team_view_program.py`：未知 slug（非空档案）→ [[STR-001]] + 可用 slug 清单（>20 条时含省略计数）+ create 建议 + exit 3；未知 slug（空档案）→ [[STR-001]] + [[STR-002]] + create 建议；损坏定义（目录在而 `team.md` 缺失）→ `定义损坏` + 精确路径 + 不含 `team not found` + 无六组正文 + exit 4；第二变体（frontmatter 不可解析）同 exit 4；概览包含损坏行且标 `定义损坏`、整体仍 exit 0；near-miss slug 不匹配任何团队（精确匹配，INV-05）；测试名 `test_unknown_slug_reports_not_found`、`test_corrupt_definition_is_not_not_found`、`test_overview_lists_every_team_sorted` 在位（FR-006, FR-015；SC-004；C-28、C-31；INV-05、INV-06）。write: `tests/integration/test_team_view_program.py` [blockedBy: T025]
- [ ] T033 [US4] 先跑 T032 并把红读数写入 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/103-team-view/notes/red-first-evidence.md` [blockedBy: T032]

### Implementation for User Story 4

- [ ] T034 [US4] 在 `scripts/python/team-view.py` 实现错误分类与导航：slug 解析只做精确目录匹配；not-found 路径输出 [[STR-001]]、可用 slug 有界清单（20 + 省略计数）、create 建议与 exit 3，空档案路径叠加 [[STR-002]]；损坏分类按文件系统判定（目录在而 `team.md` 缺失/不可读/不可解析）→ 单团队 exit 4 且点名路径、概览行标 `定义损坏` 且不跳过（R-11；C-28、C-31、C-36；FR-006, FR-015；SC-004）。write: `scripts/python/team-view.py` [blockedBy: T033]
- [ ] T035 [US4] 经唯一入口转绿并记录读数：`bash scripts/bash/run-tests.sh tests/integration/test_team_view_program.py -q --names-out .specify/specs/103-team-view/test-evidence/us4-failed.txt`，rc 与读数写入 `us4-green.txt`（FR-021；SC-004）。write: `.specify/specs/103-team-view/test-evidence/us4-green.txt` [blockedBy: T034]
- [ ] T036 [US4] 复同步程序镜像并验证：`python3 scripts/python/sync-mirrors.py --write --only scripts` 后 `--check --only scripts` 为 `ok`、`diff -q` 空输出（FR-019）。write: `.specify/scripts/python/team-view.py` [blockedBy: T035]

**Checkpoint**: 三条错误路径与概览损坏行均可行动、可区分——US4 可独立验证。

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: quickstart 实跑、定向总跑、分发与范围审计、Feature 注册面、`verification.md`、收尾门禁与提交。

- [ ] T037 实跑 quickstart 的可执行场景并把真实输出追加到 `notes/quickstart-run.md`：S-0 的引擎三个读动作复测（`binding` / `list` / `targets --list`，exit 0）、S-1 单团队六组、S-2 概览、S-3 未知 slug、S-4 损坏定义、S-5 `--target` 冲突（程序面 exit 2）；每场景附前提、命令原文、完整输出与清理（fixture 均在 `.specify/.tmp/` 或 tmp 树；不写 `.specify/teams/`）；S-6 以只读测试 id 引用，不重跑即不伪造读数（SC-001, SC-002, SC-006）。write: `.specify/specs/103-team-view/notes/quickstart-run.md` [blockedBy: T036]
- [ ] T038 定向测试总跑并记录收尾读数：`bash scripts/bash/run-tests.sh --names-out .specify/specs/103-team-view/final-failed.txt tests/unit/test_team_view_parsers.py tests/contract/test_team_view_command.py tests/contract/test_team_view_program_contract.py tests/integration/test_team_view_program.py -q`，记录 rc、通过/失败数与耗时；与 implement 入口基线名单做 `comm -13` 名称级比较，零新增红（GATE-1；FR-021；SC-007）。write: `.specify/specs/103-team-view/test-evidence/polish-targeted-suite.txt` [blockedBy: T037]
- [ ] T039 分发一致性收尾并落盘：`python3 scripts/python/sync-mirrors.py --check`（本特性三对全 `ok`，且相对 T003 基线无新增漂移）、`python3 scripts/python/regen-command-copies.py --check` rc 0、`python3 scripts/python/probe-utils.py --action compile-embeds --check` rc 0、`probe-utils.py --action probes --validate` 与 `--reconcile` 均 rc 0、`python3 scripts/python/flow-class-check.py --action check` rc 0；`doc-consistency-check.py` 不适用时记 `not-evaluated` 与原因（MUST NOT 记成通过）（GATE-2；FR-019；C-22）。write: `.specify/specs/103-team-view/test-evidence/polish-distribution.txt` [blockedBy: T036]
- [ ] T040 范围审计：完整变更集 = `git diff --name-only "$(git merge-base master HEAD)"` ∪ `git ls-files -o --exclude-standard`，限定到交付面路径（`scripts/ skills/ shared/ templates/ tests/ docs/reference/commands/ .claude/ .github/ .qoder/ .opencode/ .specify/scripts/ .specify/skills/ .specify/shared/ .specify/specs/103-team-view/ .specify/features.md .specify/features/027-team-management.md`）后 MUST ⊆ `feature-ref.md` § Delivery surface（19 路径）；基线期已存在的脏/未跟踪文件（coaching-skills 两文件、run-determination 会话记录、exec-quant 记录、观察者 agent、feedback 记录等，清单见 `notes/pre-change-measurements.md`）不提交不还原；`git log master..HEAD --oneline` 只含本特性提交且无 push 产物；读数逐行落盘（FR-019）。write: `.specify/specs/103-team-view/test-evidence/polish-scope.txt` [blockedBy: T038]
- [ ] T041 零新增机制与依赖审计：对 `scripts/python/team-view.py` 与 `skills/internal/view-team/SKILL.md` 全文 grep 确认无 cache / snapshot / scheduler / daemon / heartbeat / 第二 registry / 第二团队存储、无 `run-checks` 调用、无第三方 import（仅标准库 + `script_interface_cli`）；`git diff --name-only ...` 不含 `pyproject.toml` 与 `scripts/python/goal-utils.py`；程序未声明 `--target`（RS-004、INV-14、FR-019、A-5）。write: `.specify/specs/103-team-view/test-evidence/polish-zero-machinery.txt` [blockedBy: T038]
- [ ] T042 写 `verification.md`：SC-001…SC-007 逐条状态与证据路径；`**Path**: final` 的 SC-001 / SC-002 必须 `pass` 且带 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（路径存在且非空）；SC-003…SC-007 按 supporting 如实取值，取不到记 `not-evaluated` 与原因（GATE-4、GATE-5；SC-001…SC-007）。write: `.specify/specs/103-team-view/verification.md` [blockedBy: T037,T038]
- [ ] T043 收尾门禁三件套并把 rc 与原始输出首行写入 `polish-gates.txt`：① `python3 .specify/scripts/python/validate-tasks.py .specify/specs/103-team-view/tasks.md` → rc 0；② `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/103-team-view --stage tasks --repo .` → rc 0 且 `decision=pass`、`errors=0`；③ `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/103-team-view/requirements.md --tasks .specify/specs/103-team-view/tasks.md` → rc 0 且 JSON 的 `"decision": "proceed"`；任一非预期即停下上送显式异常行，不得改写判据迁就读数（GATE-3；FR-021）。write: `.specify/specs/103-team-view/test-evidence/polish-gates.txt` [blockedBy: T042]
- [ ] T044 只提交本特性产物：按显式路径 `git add`（程序与镜像、技能与镜像、probe 注册面与镜像、命令模板与四个副本、docs 页、fixture 模块与四份测试、本 spec 目录产物与 Feature 注册面、证据目录），不 `git add -A`；既有脏文件不提交不还原；不 push；提交信息按 `templates/commit-template.md` 的单行形态，读数落盘（FR-019）。write: `.specify/specs/103-team-view/test-evidence/polish-commit.txt` [blockedBy: T043]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无前置，可立即开始；T002 / T003 与 T001 落在三个不同文件。
- **Foundational (Phase 2)**: 依赖 Setup 的落点；并被全部用户故事的测试行依赖。
- **US1 (Phase 3)**: 依赖 Foundational；内部严格按「测试 → 红 → 实现 → 技能/注册/接线 → 绿 → 双镜像」推进。
- **US2 (Phase 4)**: 依赖 US1 的程序面（同一文件扩展）；测试段追加到 US1 的两个测试文件。
- **US3 (Phase 5)**: 依赖 US1 的测试文件与命令模板；文档与副本跟随模板。
- **US4 (Phase 6)**: 依赖 US2 的程序与镜像面；测试段追加到同一集成文件。
- **Polish (Phase 7)**: 依赖全部故事完成；T044（提交）必须是最后一行。

### User Story Dependencies

- **US1 (P1)** 与 **US2 (P1)** 合起来构成 MVP：单团队呈现与全团队概览是同一 `view` 模式的两条主路径——缺概览则命令的默认入口不成立，缺单团队则核心价值不在。
- **US3 (P2)** 独立于程序行为（接线与文档），但引用同一 owner 路径；文档与模板不一致即视为缺陷。
- **US4 (P3)** 独立于 US3；其测试只依赖 US2 之后的程序面。

### Within Each User Story

- 测试先写、先观察红，再实现；实现后经唯一入口转绿；随后镜像/副本与读数。
- 同一文件（`scripts/python/team-view.py`、两个测试文件、模板）跨行修改时严格串行，依赖键显式声明。
- 镜像与副本只经生成器写入，且永远跟随作者编辑。

### Parallel Opportunities

- Setup 的 T002 / T003 可并行（两个不同证据文件）。
- US1 的 T007 / T008 可并行（两份不同测试文件）；实现链 T010→T013 串行；T014 技能与 T016 模板在测试红之后可分别推进，但本表按单执行体顺序排列。
- US2 的 T020 / T021 可并行（两份不同测试文件）。
- 跨故事：US3 的文档行与 US1/US2 的程序行写领地不相交；US4 必须等 US2 的程序面稳定。

---

## Parallel Example: Setup 与 US2 测试腿

```bash
# Setup：两个证据落点互不相干
Bash: "冻结条款覆盖基线"          # write: coverage-baseline.txt
Bash: "采集分发一致性基线"        # write: test-evidence/mirror-baseline.txt

# US2：两份测试文件互不相干
Bash: "追加概览集成测试段"        # write: tests/integration/test_team_view_program.py
Bash: "追加概览 envelope 断言"    # write: tests/contract/test_team_view_program_contract.py
```

---

## Implementation Strategy

### MVP First

**MVP 范围 = US1 + US2**（两条同为 P1，且只有合起来才构成完整可用的 `view` 入口：无 slug 默认概览 + 单团队六组细节）。T001–T019 完成 US1 后即按其 Independent Test 验证；T020–T025 完成 US2 后 STOP AND VALIDATE 一次 MVP，再进入 P2。

1. 完成 Setup：测量、覆盖、分发三类基线落盘。
2. 完成 Foundational：fixture 模块可 import。
3. 完成 US1：程序六组 + 技能 + probe 注册 + 入口 + 双镜像绿。
4. 完成 US2：概览与 envelope 键绿，镜像复同步。
5. **STOP and VALIDATE**：按两条 P1 故事的 Independent Test 独立验证。
6. 继续 US3 → US4 → Polish。

### Incremental Delivery

1. Setup + Foundational 完成 → 后续每条结论都有对照面。
2. US1 完成 → `/speckit.team view <slug>` 完整呈现六组，只读可证。
3. US2 完成 → `/speckit.team view` 给出全团队概览（MVP 收口）。
4. US3 完成 → 路由不串线、文档四模式、两处漂移校正。
5. US4 完成 → 三条错误路径可行动、损坏与不存在严格区分。
6. Polish 完成 → quickstart 实跑、分发一致、范围克制、`verification.md` 就位。

---

## Notes

- **N-1 `[green:]` 标签的省略（本阶段裁决）**: 三份契约的条款为 `md-bold-closed` 形态（`**C-NN**` 行首），`clause_extract.py` 可全部解析（12 + 11 + 15 = 38）；但条款的绿色时点跨三条故事（C-01/C-02/C-03/C-06 在 US1、C-04/C-05/C-07…C-12 在 US3、C-13…C-23 的文本面在 US1 而行为面在 US1/US2/US4），逐条打标会制造 `green-cross-phase` / `green-path-divergence` 噪声（与 101 N-4、102 N-1 同形）。故本文件不打标签：条款级归属由「契约文件 ↔ pinning test 文件」一一对应承担，FR 级由 DoD-1 的逐行引用承担，覆盖基线仍由 T002 冻结（claimed=0 的理由即本条）。
- **N-2 同一测试文件跨故事追加（append-only 增长）**: `tests/integration/test_team_view_program.py` 由 US1（六组/三态/遗留/归档/坏行/截断/只读）、US2（概览）、US4（错误路径）三段追加组成；`tests/contract/test_team_view_program_contract.py` 由 US1（接口与退出码）与 US2（overview 键）两段组成；每次追加行以「该文件当前全部段为绿」验收，不声明「文件从此冻结」——这不是两个验证行对同一固定状态各自宣称，而是同一文件的顺序生长。
- **N-3 Foundational 阶段只含一项**: 四份测试文件都 import 同一个 fixture 模块与快照 helper；没有它则四故事的测试都无法编写（R-13），因此按模板保留 Foundational 而且只有一行。除它之外没有阻塞四故事的共享前置（镜像各跟随作者编辑）。
- **N-4 probe registry 注册面（计划交付面的补齐）**: 契约 C-22 要求新技能的 `## Wrap-up` 由 `compile-embeds` 生成，而 `probe-utils.py --action probes --reconcile` 的「embed 无对象」检查要求该技能在 `shared/definitions/probe-definitions.md` § Objects 有一行 `skill:view-team` 对象；`feature-ref.md` 的交付面原先漏列该 pair（源 + `.specify/shared/` 镜像）。本阶段以 minor 级 PLAN-EDIT 将其补为第 19 项（引用完整性修补，非新能力），T015 是它的实现行。
- **N-5 概览与损坏定义的分工**: US2 只承诺可读团队的概览与空档案；「损坏行照常列出并标 `定义损坏`」属 FR-006 的错误路径语义，随 US2 的 `overview.total` / `corrupt_total` 键先落 envelope 契约（T021），完整行为在 US4 转绿（T032/T034）——避免把同一行为在两个故事里各实现一次。
- **N-6 只读证明的形态**: 只读 oracle 是 path+sha256 快照（T004 的 `snapshot`），断言在 T008（US1）与 T032 的概览/错误路径变体上执行；计划里的 `test_view_leaves_tree_byte_identical` 是实现期最终测试名，GATE-5 以最终名为准。源码层「无写动作」由 T041 的静态审计补充，不用静态扫描替代行为快照。
- **N-7 本阶段未改 plan-owned 语义**: 除 N-4 记录的 feature-ref 第 19 项补齐（minor）外，`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` 均未修改；`plan_constraint=active` 下本轮的 PLAN-EDIT 仅此一条。
- **N-8 测试入口纪律**: 所有测试行只写 `scripts/bash/run-tests.sh` 入口；本阶段自身是 docs-only（`tasks.md` + 注册面注记 + 证据），按 E3 记 `not-run-docs-only`，不跑任何测试——实现的测试义务由 T005–T044 承担。
