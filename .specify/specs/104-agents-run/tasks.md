# Tasks: /speckit.agents run — 显式 run 子命令与 superagent/subagent 架构自动应用（Agents Run）

**Requirement ID**: 104
**Requirement Key**: `104-agents-run`
**Related Feature**: 019 Agents Command（`.specify/features.md`；本阶段维持 `Implemented`，无状态迁移权）
**Input**: Design documents from `.specify/specs/104-agents-run/`
**Prerequisites**: plan.md（技术路线 / Mirror Obligations / Structure Decision）、requirements.md（24 FR / 7 SC / 8 STR / A-1…A-14）、research.md（B-01…B-13 / R-01…R-10）、data-model.md（E1–E9 / INV-01…INV-12）、contracts/ ×3（**35 条款**：command 10 / dispatch 12 / docs 13）、quickstart.md（S-0…S-7）、feature-ref.md

**Tests Mode**: ON（Constitution Principle IV "Test-First & Contract-Driven Implementation" 是测试强制原则；同条下的 **Template-only features** 子句把本特性的测试形态固定为**结构性契约测试**——对模板、技能文本、参考文档的内容 / 标题 / 字面量 / 镜像一致性断言，而非单元或集成运行时测试。五支新测试模块一律红先；两处例外按 migration/regression 例外处置：`tests/contract/test_agents_run_multi_child_edges.py` 守的是既有只读引擎行为，`tests/contract/test_agents_run_scope_contract.py` 守的是变更集包含性——二者的红形分别是引擎报告违例与变更集出现禁止路径，不是文件缺位。）

**Tests**: 红先证据的唯一落点是 `.specify/specs/104-agents-run/notes/red-first-evidence.md`（每支测试一条：命令、真实输出、退出码）。失败 nodeid 名集的捕获与比较形式归 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，本文件只给路径与命令，不复述比较形式。测试执行唯一入口是 `bash scripts/bash/run-tests.sh`，任何任务行 MUST NOT 写解释器级测试命令。

**Organization**: 按用户故事组织——US1（一次显式 run 派发 + 角色自动应用，P1）、US2（同一 superagent 下多次 run 可区分，P1）、US3（边界与治理不越线，P2）、US4（文档同源，P2）、US5（失败与半成品被诚实报告，P3）。MVP = **US1 + US2**：两条故事同为 P1，且用户原话同时包含「显式 run 自动应用架构」与「一个 superagent 下多次 run 启动多个子代理」——只有 US1 时后者这半承诺缺席；两故事的检查点各自独立可测。Foundational 阶段整段省略：本特性无阻塞性基础设施——两处 authored 源、六个文档面与一个路由场景各自只依赖已存在的 owner 文档与只读引擎，没有共享件先于用户故事落地。

## Definition of Done (DoD)

- DoD-1: 全部任务行为 `[X]`；若出现 `[~]`，其理由逐条记录在 `.specify/specs/104-agents-run/verification.md` 的 `deferred_tasks=`。
- DoD-2: 交付面 = 2 处 authored 源（`templates/commands/agents.md`、`skills/internal/run-agent/SKILL.md`）+ 6 个文档面（`docs/reference/commands/agents.md`、`docs/reference/agents/command-and-skills.md`、`overview.md`、`design.md`、`docs/tutorials/installation.md`、`quickstart.md`）+ 1 个路由场景 + 5 支新测试模块 + 由生成器产出的 4 份逐工具命令副本与 1 份技能镜像；零新增 `/speckit.*` 命令、零新增技能、零新增脚本、零新增 store。
- DoD-3: 3 份契约共 35 条款（10 + 12 + 13）每条恰被一个任务行 `[green:]` 认领一次；`account-clause-coverage.py` 报告 `claimed clauses = 35`、`FR 24 / 24`、`uncovered beyond baseline = 0`；每份契约内认领顺序单调递增（唯一例外 C-06 已在生成报告里裁定并记录）。
- DoD-4: 5 支新测试全绿；4 支既有守卫（`tests/contract/test_run_skills_wiring.py`、`tests/contract/test_team_command_routing.py`、`tests/contract/test_role_transition_payload.py`、`tests/contract/test_fast_fail_discipline.py`）相对 implement 入口的名字级失败基线零**新增**失败（既有红逐条点名、不声称全绿）。
- DoD-5: plan.md § Mirror Obligations 逐行落地——4 份逐工具副本含 `run <agent-name> [task]`；`skills/internal/run-agent/SKILL.md` 与其 `.specify/skills/internal/` 投影 `diff -q` 空输出；`sync-mirrors.py --check` 与 `regen-command-copies.py --check` exit 0；零手改镜像 / 副本。
- DoD-6: C-34 的陈旧字面量封闭集在七个命名文件中出现数为 0；`docs/reference/commands/agents.md` 的 `^# /speckit.agents` 计数 = 1（改前 3）。
- DoD-7: 行为类条款（FR-023 清单）以真源文本（已被契约测试钉住的指针部分）+ 评审 + SC-006 变异演练取证；测试与文档 MUST NOT 声称契约测试覆盖运行期行为。
- DoD-8: `verification.md` 逐条记录 SC-001…SC-007 的状态、命令与证据指针；final-path 的 SC-001 记 `pass` 并带 smoke 记录。
- DoD-9: plan_constraint 全趟遵守——plan-owned 面（`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md`）的任何改动只能是行级小修，逐项在 `verification.md` 声明 `PLAN-EDIT: <path> — <理由>；分类=minor`；任何实质性改动停线回抛。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/104-agents-run/tasks.md` exit 0（0 error；WARN 逐条裁定并记录）。
- GATE-2: 跨产物一致 — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/104-agents-run --stage tasks --repo .` 输出 `decision=pass` 且 errors=0（advisory 逐条裁定）。
- GATE-3: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` 输出 `claimed clauses = 35`、FR uncovered = 0、`uncovered beyond baseline = 0`，exit 0。
- GATE-4: 五支新测试 + 四支既有守卫零新增失败 — check: `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py tests/contract/test_agents_run_docs_contract.py tests/contract/test_agents_run_skill_wiring.py tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_scope_contract.py tests/contract/test_run_skills_wiring.py tests/contract/test_team_command_routing.py tests/contract/test_role_transition_payload.py tests/contract/test_fast_fail_discipline.py --names-out <failed-list-file>` 的失败名集相对 implement 入口基线做 `comm -13` 为空。
- GATE-5: 镜像与副本零漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0，且 `diff -q skills/internal/run-agent/SKILL.md .specify/skills/internal/run-agent/SKILL.md` 空输出。
- GATE-6: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/104-agents-run/tasks.md` 返回 0。
- GATE-7: final-path 成功判据 + smoke 记录 — check: `verification.md` 中 `**Path**` 为 `final` 的 SC（本特性 = SC-001）记 `SC-001_status=pass`，且 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`（存在且非空）齐备（条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates）。
- GATE-8: 陈旧字面量封闭集为空 — check: `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py -q` exit 0——该模块的 C-34 函数逐行断言封闭谓词表的**全部行**（谓词表的唯一 owner 是 `contracts/agents-run-docs.contract.md` § C-34，本行不复述谓词集）；MUST NOT 以任何子集 grep 的绿色冒充零集证据。

## Environment Prerequisites

- CPython: **available** — probe: `python3 --version` → `Python 3.11.11` @ 2026-11-24；affected: 全部 python 引擎行。
- pytest（经唯一入口）: **available** — probe: `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-11-24；affected: 全部测试行（一律经 `bash scripts/bash/run-tests.sh`）。
- git（`rev-parse` / `status` / `diff`）: **available** — probe: `git rev-parse --short HEAD` → `a02705a3c`；`git status --short` 可读 @ 2026-11-24；affected: T001、T014、T029、T030。
- 容器运行时 / 镜像仓库 / 活集群 / 外网: **none** — 本特性全部检查为本地文件、`git` 与本地 pytest，无构建、无拉取、无网络、无守护进程 @ 2026-11-24；affected: none。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。本文件的 `[P]` 只出现在 US4 的文档编辑行（T017 / T018 / T019 / T020 / T022，逐行写彼此不同的文档或场景文件）；US1 的两条红先行共用 `notes/red-first-evidence.md` 这一追加落点，故整段零 `[P]`（共享 sink 即同写目标，按行序串行，不靠删路径消警）。
- **[Story]**: 用户故事标签（`[US1]`…`[US5]`），只出现在用户故事阶段的任务行；Setup / Polish 阶段零 `[US` 标记。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行。仅阶段顺序关系时不写。
- **[green: <contract>#<clause>]**: 绿点认领——本行是使该条款转绿的那一行；契约路径相对本文件目录解析。**35 条款分区**：`agents-run-command.contract.md` C-01…C-05、C-08、C-10→T004/T005/T009，C-06→T017，C-07→T005，C-09→T027；`agents-run-dispatch.contract.md` C-11→T006，C-12…C-14→T007，C-15→T008，C-16/C-17→T011，C-18…C-21→T013，C-22→T015；`agents-run-docs.contract.md` C-23…C-28→T017，C-29→T018，C-30→T019，C-31→T020，C-32→T021，C-33→T022，C-34→T023，C-35→T030。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径与全部标签），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **框架源（编辑面）**: `templates/commands/`、`skills/internal/`、`docs/reference/`、`docs/tutorials/`、`tests/scenarios/`、`tests/contract/`。
- **生成面（MUST NOT 手改）**: 四份逐工具命令副本（`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`，由 `regen-command-copies.py` 生成）；`.specify/skills/internal/`（由 `sync-mirrors.py` 投影）。
- **证据落点（本特性）**: `.specify/specs/104-agents-run/` 下的 `notes/pre-change-measurements.md`、`notes/red-first-evidence.md`、`notes/quickstart-run.md`、`coverage-baseline.txt`（本阶段已冻结）、`test-evidence/mutation-drill.md`、`test-evidence/behavior-class-evidence.md`、`verification.md`。
- **只读面（零修改）**: `scripts/python/role-edge-check.py`、`scripts/python/execution-config.py`、`scripts/python/exec-quant.py`、`scripts/python/status-digest.py`、`skills/internal/create-team/scripts/dispatch.sh`、`shared/definitions/superagent-definitions.md`、`shared/definitions/subagent-definitions.md`；`docs/reference/history/`（dated record 不改写）。
- **plan-owned 面（仅小修）**: `plan.md`、`data-model.md`、`contracts/**`、`quickstart.md`、`research.md`、`feature-ref.md`。

## Measured Premises (re-measured at generation time 2026-11-24, HEAD `a02705a3c`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 需求条目计数（FR / SC / STR） | `grep -cE '^\- \*\*FR-[0-9]+\*\*:' .specify/specs/104-agents-run/requirements.md`；同法 `SC-`；`grep -cE '^\| \`STR-[0-9]+\`' …/requirements.md` | **24 / 7 / 8** |
| 契约条款数（逐文件 + 合计） | `grep -cE '^\*\*C-[0-9]+\*\*' .specify/specs/104-agents-run/contracts/*.md`；合计 `grep -ohE '^\*\*C-[0-9]+\*\*' …/contracts/*.md \| wc -l` | command **10** / dispatch **12** / docs **13**；合计 **35**，ids 连续 C-01…C-35。**陷阱形**：`grep -c 'C-'` 会把正文里的条款引用一起算入，计量单位是行首加粗的条款定义行 |
| 5 个新测试文件当前状态 | 逐个 `test -e tests/contract/test_agents_run_{command_contract,docs_contract,skill_wiring,multi_child_edges,scope_contract}.py` | 5/5 **ABSENT**（红先的前提） |
| 编辑目标与守卫在位 | 逐个 `test -e`（2 处 authored 源 + 6 个文档面 + 1 个路由场景 + 4 支既有守卫） | 13/13 **OK** |
| 命令参考三副本 | `grep -nE '^# /speckit.agents' docs/reference/commands/agents.md` | **3** 处（`:1` / `:114` / `:205`）；copy 1 = 现行面，copy 2/3 = 旧子集 |
| 陈旧字面量（改前，C-34 的 Before 列） | `grep -Fc '<literal>'` 逐文件 | STR-005 **4**（commands 2 / command-and-skills 1 / scenario 1）；STR-006 **2**（commands）；STR-007 **2**（installation 1 / quickstart 1）；STR-008 **2**（commands）。**陷阱形**：`grep -c` 数的是命中行数，不是命中次数，跨行重复须逐文件重数 |
| `argument-hint` 现状 | `grep -c 'argument-hint' templates/commands/agents.md`；兄弟形 `grep -n 'argument-hint' templates/commands/team.md templates/commands/goal.md templates/commands/anchor.md` | **0**（本文件无此键）；兄弟形 `team.md:4` / `goal.md:4` / `anchor.md:4` |
| run-agent 缺项 | `grep -c 'parent_identity\|child_label\|role_declaration\|return_channel\|depth_position\|authority_ref' skills/internal/run-agent/SKILL.md` | **0**（七字段名一个都不在技能文本中，故红先成立） |
| 镜像与副本基线 | `python3 scripts/python/sync-mirrors.py --check`；`python3 scripts/python/regen-command-copies.py --check` | `sync-mirrors` exit **0**（六对 `ok`，末行 `ok shared/ == .specify/shared/ (114 files, byte-identical)`）；`regen-command-copies` 输出 `OK: all per-tool command copies match the source templates.`，exit **0** |
| flow-class 基线 | `python3 .specify/scripts/python/flow-class-check.py --action check` | `92 unit(s) scanned, 0 finding(s)`；`coverage: ledger_rows=92 matched=92 inventory_units=92 gaps=0 parse_errors=0 floor=39` |
| 条款覆盖基线 | `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run --freeze > .specify/specs/104-agents-run/coverage-baseline.txt`；随后 `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` | 基线已冻结：787 行、`base-sha: a02705a3c66e`、`files: 319 (parsed 211 + named 108)`；改后核算 `status: ok`、exit **0**：`claimed clauses 35`、`FR claimed: 24`、`FR uncovered: 0`、`clause-uncovered pass (785) — 0 beyond the frozen baseline`、`coverage-baseline-delta pass (0)`；唯一告警为语料级既有事实 `clause-unparsable (108)`（107 个 `md-none` 命名文件 + 1 个 parse-doubt），非本特性引入 |
| 任务行数 | `grep -cE '^- \[[ xX>~]\] T[0-9]+' .specify/specs/104-agents-run/tasks.md` | **33**（< 40，无需分裂） |

## Test Budget Record (targeted-set-v1, `stage_base=a02705a3c`)

**E3 stage-status row（恰一条，`not-run-docs-only`）** — `stage=tasks`、`row_type=stage-status`、`status=not-run-docs-only`、`selection_basis=targeted-set-v1：本阶段的变更全部是文档型——本任务清单、其证据行、本阶段冻结的条款覆盖基线与 Feature 019 登记注记；未触碰任何可执行面、测试面或引擎面，定向集为空集且无测试可跑`、`changed_paths[]=.specify/specs/104-agents-run/{tasks.md,coverage-baseline.txt,test-evidence/tasks.jsonl}` + `.specify/features.md` + `.specify/features/019-agents-command.md`、`evidence_ptr=.specify/specs/104-agents-run/test-evidence/tasks.jsonl`。运行字段（命令 / 退出码 / 计数 / 用时 / 失败名集）不适用，MUST NOT 报 `unknown`。

**条款覆盖改后读数（生成时实测）**：`account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` → `status: ok`、exit 0；`claimed clauses 35`、`FR claimed: 24`、`FR uncovered: 0`、`uncovered beyond baseline: 0`；唯一告警 `clause-unparsable (108)` 是语料级既有事实（107 个 `md-none` 命名文件 + 1 个 parse-doubt），不随本特性变化。三个此前未被契约引用的 FR（FR-013 / FR-021 / FR-024）已以**引用级小修**并入既有条款的引用括号，逐条声明见下。

**Plan edits（plan_constraint 声明，全部为 minor）**：
- `PLAN-EDIT: contracts/agents-run-dispatch.contract.md` — C-19 引用括号补 `FR-013`（同一 Instance 多次执行彼此隔离），C-22 引用括号补 `FR-021`（不新增 glossary 词条）；仅引用级补全，不改条款正文；分类=minor
- `PLAN-EDIT: contracts/agents-run-docs.contract.md` — C-35 引用括号补 `FR-024`（唯一测试入口 / 零新增失败）；仅引用级补全，不改条款正文；分类=minor

## Requirement Coverage Map

| FR | 承载任务行 | SC | 承载任务行 |
|----|------------|----|------------|
| FR-001 | T004、T005、T017、T027 | SC-001 | T002、T004、T005、T009、T017、T023 |
| FR-002 | T004、T009 | SC-002 | T010、T012 |
| FR-003 | T004 | SC-003 | T003、T009、T032 |
| FR-004 | T005 | SC-004 | T016、T023 |
| FR-005 | T024、T025 | SC-005 | T014、T029 |
| FR-006 | T006、T013 | SC-006 | T030 |
| FR-007 | T006 | SC-007 | T032 |
| FR-008 | T007 | — | — |
| FR-009 | T007 | — | — |
| FR-010 | T008 | — | — |
| FR-011 | T011、T012 | — | — |
| FR-012 | T011 | — | — |
| FR-013 | T006、T009 | — | — |
| FR-014 | T004、T013 | — | — |
| FR-015 | T013、T014、T029 | — | — |
| FR-016 | T013 | — | — |
| FR-017 | T013 | — | — |
| FR-018 | T017 | — | — |
| FR-019 | T018 | — | — |
| FR-020 | T019、T020、T021、T022 | — | — |
| FR-021 | T014、T029 | — | — |
| FR-022 | T002、T003、T016、T024、T027、T028、T032 | — | — |
| FR-023 | T031 | — | — |
| FR-024 | T032 | — | — |

**SC-002 的判定面**：T010 交付同父 + 双 label 夹具上的引擎读数（2 条子代边、深度 1、违例集空）与 label 变异腿；T012 把该读数与重试腿结果记为证据。二者合起来才是「两次 run 产生两条独立边 + 重试即新尝试」的完整读法。
**SC-006 的判定面**：T030 的四个变异各自点名其钉住检查（C-01 / C-02 / C-12 / C-23），红/绿读数落 `test-evidence/mutation-drill.md`。

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结后续「零新增 / 包含性 / 字面量前后对照」判据的对照物——implement 起点的可比较分母。

- [X] T001 捕获 implement 起点基线并创建证据落点：写 `.specify/specs/104-agents-run/notes/pre-change-measurements.md`（命令 + 真实输出 + 捕获日期），逐项贴 `git rev-parse --short HEAD`、`git status --short`、`python3 scripts/python/sync-mirrors.py --check`、`python3 scripts/python/regen-command-copies.py --check`、`grep -cE '^# /speckit.agents' docs/reference/commands/agents.md`（期望 3）、C-34 表全部谓词（owner 表逐行）的改前计数、`grep -c 'argument-hint' templates/commands/agents.md`（期望 0）、五个新增测试文件的缺位普查（逐个 `test -e`）、`python3 .specify/scripts/python/flow-class-check.py --action check`；本行同时创建 `notes/` 落点，不写任何产品文件。

---

## Phase 3: User Story 1 - 一条显式 run 命令把任务派发给子代理，当前 session 自动是 superagent (Priority: P1) 🎯 MVP

**Goal**: `run <agent-name> [task]` 在三个面（模板 `argument-hint`、技能输入契约、命令参考 Syntax）逐字固定；派发面接线 095 的角色协议——呈现披露角色关系、七字段下行、四项既有注入、五要素上行；当前 session 无需任何开关即成为该边的 superagent。

**Independent Test**: `tests/contract/test_agents_run_command_contract.py` 与 `tests/contract/test_agents_run_skill_wiring.py` 的 US1 面全绿（C-01…C-05、C-07、C-08、C-10、C-11…C-15），允许残余失败只限 C-06 / C-09 / C-16…C-22 对应函数；`notes/red-first-evidence.md` 记录红→绿两次实跑。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写测试并确认失败，再进入实现行**

- [X] T002 [US1] [blockedBy: T001] 红先编写 `tests/contract/test_agents_run_command_contract.py`：per `contracts/agents-run-command.contract.md` 的 C-01…C-10 每条一个具名测试函数（模板 frontmatter `argument-hint` 精确等于 STR-001；三技能委派表与 run 行输入 `run <agent-name> [task]`；显式动词优先 / 团队意图不得被 run 承接 / 歧义报三能力；缺 agent 名停止；无参行为不变；三面语法逐字一致；C-08 的 7 条路由样例逐条代理断言；四份逐工具副本含 `run <agent-name> [task]`；三条错误字符串在位且各自为停止路径）；作者时断言必须失败；以 `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q` 实跑并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`。
- [X] T003 [US1] [blockedBy: T002] 红先编写 `tests/contract/test_agents_run_skill_wiring.py`：per `contracts/agents-run-dispatch.contract.md` 的 C-11…C-22 每条一个具名测试函数（呈现三要素与 owner 指针；七字段下行逐项在场；四项注入按 owner 指针；`role-transition` 标识 + 九个 item-id slug 与既有短语 `nine item-id slugs` / `identifier alone is insufficient` / `payload-construction defect` 保留；五要素上行与 incomplete 规则；child label 约定与重试即新尝试；三载体可见性指针；SDD 探针适用条件；单单元边界句逐字保留 + 读数三元组；反嵌套红线；角色只由边决定；零第二机制与行为类诚实标签）；红跑同一入口并把命令、真实输出、退出码追加 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [X] T004 [US1] [blockedBy: T002,T003] 编辑 `templates/commands/agents.md`：frontmatter 增加 `argument-hint: "[create|refine|run] [agent-name] [task]"`（STR-001 逐字，兄弟形参见 `templates/commands/team.md`）；User Input 段补显式动词优先与「显式 run 无 agent 名 → 输出 STR-003 + 三能力清单 + 用法，零派发、不从上下文推断、不落入无参列举」；Delegation 段补「多代理 / 团队意图 MUST NOT 被本命令承接，指向 `/speckit.team`」并保留既有团队重定向句；三技能委派表与 run 行输入 `run <agent-name> [task]` 原样保留；运行 `tests/contract/test_agents_run_command_contract.py`（唯一入口，`-q`）确认 C-01…C-05 对应函数转绿。 [green: contracts/agents-run-command.contract.md#C-01] [green: contracts/agents-run-command.contract.md#C-02] [green: contracts/agents-run-command.contract.md#C-03] [green: contracts/agents-run-command.contract.md#C-04] [green: contracts/agents-run-command.contract.md#C-05]
- [X] T005 [US1] [blockedBy: T002,T003] 编辑 `skills/internal/run-agent/SKILL.md` § Input Contract：加入 STR-001 语法逐字（`[create|refine|run] [agent-name] [task]`）与 `missing task` 停止路径（STR-004：呈现解析后的 agent 名 / 层 / 描述并请求任务，不派发空简报、不落入无参列举）；运行 `tests/contract/test_agents_run_skill_wiring.py`（唯一入口，`-q`）确认 C-07 与 C-06 的技能面断言通过（docs 面仍红属预期）。 [green: contracts/agents-run-command.contract.md#C-07]
- [X] T006 [US1] [blockedBy: T005] 编辑 `skills/internal/run-agent/SKILL.md` § Run Mode 的 Present 步：在既有配置披露旁补第二组披露——本 session 是该边的 superagent（根）、child label、回传通道；按指针指向 `superagent-definitions.md` owner（不复述规则文本），保持 disclosure-not-gate（用户可在派发前叫停）；角色只由派发边决定（FR-006）。 [green: contracts/agents-run-dispatch.contract.md#C-11]
- [X] T007 [US1] [blockedBy: T006] 编辑 `skills/internal/run-agent/SKILL.md` § Dispatch：七字段下行逐项点名（`parent_identity` / `child_label` / `role_declaration` / `dispatch_duty` / `depth_position` / `authority_ref` / `return_channel`）并按指针指向 `superagent-definitions.md` § The super↔sub Protocol（语义不复述）；四项既有注入（快速失败子句逐字、并发义务、汇报义务、re-anchoring 锚摘要）按各自 owner 指针携带（FR-008 / FR-009）；保留 `role-transition` 标识 + 九个 item-id slug 的逐项自检与既有短语；反嵌套红线按指针保留。 [green: contracts/agents-run-dispatch.contract.md#C-12] [green: contracts/agents-run-dispatch.contract.md#C-13] [green: contracts/agents-run-dispatch.contract.md#C-14]
- [X] T008 [US1] [blockedBy: T007] 编辑 `skills/internal/run-agent/SKILL.md` § Report 步：五要素上行按 `superagent-definitions.md` § The super↔sub Protocol 指针要求——结果或交付物路径、证据指针、显式异常行（无异常写「未发现异常」）、并发读数三元组、返回执行体身份；缺任一项判 incomplete，父侧 MUST NOT 消费结论、MUST NOT 代填缺失字段。 [green: contracts/agents-run-dispatch.contract.md#C-15]
- [X] T009 [US1] [blockedBy: T004,T005,T006,T007,T008] US1 转绿与取证：运行 `tests/contract/test_agents_run_command_contract.py` 与运行 `tests/contract/test_agents_run_skill_wiring.py`（唯一入口，`-q`）——允许的残余失败只限 C-06（docs 面）、C-09（副本面）与 C-16…C-22（US2 / US3 面）对应函数，其余任何失败即缺陷；逐函数通过 / 失败名单与命令写入 `notes/red-first-evidence.md`；本行认领 C-08（路由样例集）与 C-10（三条错误字符串各自停止）——二者在本行实跑中首次全绿。 [green: contracts/agents-run-command.contract.md#C-08] [green: contracts/agents-run-command.contract.md#C-10]

**Checkpoint**: US1 独立可验——模板 / 技能输入 / 呈现 / 载荷 / 回传五段接线与路由样例全部转绿；C-06 只差 docs 面，副本面留待再生成。

---

## Phase 4: User Story 2 - 同一 superagent 下多次 run 启动多个子代理，彼此可区分 (Priority: P1)

**Goal**: 每次 run = 一条独立边 = 一个子代；child label 复用既有 dispatch label 约定，重试即新尝试、旧产物保留；多子代只经既有三载体可见。

**Independent Test**: `tests/contract/test_agents_run_multi_child_edges.py` 以同一 parent + 两个 child label 的夹具跑只读 `role-edge-check.py`，报告 2 条子代边、深度 1、零违例；`test_agents_run_skill_wiring.py` 的 C-16 / C-17 函数绿。

- [ ] T010 [US2] 编写 `tests/contract/test_agents_run_multi_child_edges.py`：在 pytest `tmp_path` 构造同一 parent + 两个 child label 的派发记录夹具（记录形态 `unit_type=agent` / `unit_id=agent:<parent>` / `run_id=<label>`）与对应 artifact triplet（`<label>.live.log` / `<label>.jsonl` / `<label>.status`），以只读方式运行 `scripts/python/role-edge-check.py --action report`，断言 2 条子代边、深度 1、零违例；变异腿：把两个 label 压成同一个时断言报告不再呈现两条独立边（红形演示）、重试即新 label 且旧 triplet 保留、旧尝试迟到返回按 `watch-model.md` § 11 归因且不被当作当前结果；本模块守既有引擎行为（migration/regression 例外，无红先步骤），跑一次并把真实输出写入 `notes/red-first-evidence.md`。
- [ ] T011 [US2] [blockedBy: T008,T010] 编辑 `skills/internal/run-agent/SKILL.md` § Dispatch / Report：落 child label 约定（`dispatch.sh <label>` 的 label 原样作为该次派发 `run_id`，调用 `exec-quant.py --action collect-dispatch --run-id <label>`；external triplet 以 `<label>.live.log` / `<label>.jsonl` / `<label>.status` 命名；每次 run 新 label、重试即新尝试、旧尝试产物保留、迟到返回不消费；零新增 label 生成器 / 子代清单 / registry）与三载体可见性指针（artifact triplet、`exec-quant` 派发记录、既有只读 `status-digest.py` 角色视图 `parent` / `roles` / `role_set_marker` / `depth`）。 [green: contracts/agents-run-dispatch.contract.md#C-16] [green: contracts/agents-run-dispatch.contract.md#C-17]
- [ ] T012 [US2] [blockedBy: T010,T011] US2 转绿与取证：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_skill_wiring.py -q` — 两子代边 / 深度 1 / 零违例与 label 变异腿通过，C-16 / C-17 对应函数绿（C-18…C-22 仍红属预期）；SC-002 读数（边数、深度、违例集、重试腿结果）写入 `notes/red-first-evidence.md`。

**Checkpoint**: US2 独立可验——多子代身份与可见性由既有引擎与既有载体证明，零新增清单 / registry。

---

## Phase 5: User Story 3 - 边界与治理不越线：单代理、SDD 条件、零第二机制 (Priority: P2)

**Goal**: run 仍是单代理操作；SDD 授权探针只在载荷指派 / 点名 SDD 驱动时适用，普通 run 不因缺 team / seat 被阻断；角色只由边决定；零新增持久化根 / registry / 渲染器 / 调度器 / 队列。

**Independent Test**: `tests/contract/test_agents_run_scope_contract.py` 与 `test_agents_run_skill_wiring.py` 的 C-18…C-22 函数全绿；结构审计命令的读数与 T001 基线比较为零新增。

- [ ] T013 [US3] [blockedBy: T011] 编辑 `skills/internal/run-agent/SKILL.md`：派发前探针段写清适用条件——调用 `sdd-route.py --action authorize` 只在载荷指派 / 点名 SDD 驱动时运行，谓词 per `subagent-definitions.md` § Dispatch-Time Governance Obligation 收窄；普通 run MUST NOT 调用探针、MUST NOT 因缺 team / seat 被阻断；既有拒绝形态（失败的一半 / 解析值 / 两个来源路径 / seat slug）原样保留；补团队参数冲突的选项处置——`--target` / `--scope` / `--spec-dir`（团队参数封闭集，owner `templates/commands/team.md`）与任何未列入的 `--` 选项一律输出具名冲突句 `team parameter not accepted by run: <option>` 并指向 `/speckit.team`，不静默丢弃、不改写为团队运行（requirements § Edge Cases / FR-002）；补「角色只由边决定」陈述（无激活开关、角色实体、第四类分类或第二份定义，owner 指针）与单单元边界（既有句 `**Scope boundary**: Run mode executes a **single** agent on a **single** task.` 逐字保留、一次 run 不扇出、多次 run 是多次命令运行、读数三元组以 `single-unit` 具名、无区间记 `not_evaluated`，MUST NOT 记 0 或估算）；反嵌套红线按既有指针保留。 [green: contracts/agents-run-dispatch.contract.md#C-18] [green: contracts/agents-run-dispatch.contract.md#C-19] [green: contracts/agents-run-dispatch.contract.md#C-20] [green: contracts/agents-run-dispatch.contract.md#C-21]
- [ ] T014 [US3] [blockedBy: T001] 编写 `tests/contract/test_agents_run_scope_contract.py`：变更集包含性（SC-005）——以 `notes/pre-change-measurements.md` 记录的 implement 起点为 base，读取 `git diff <base>..HEAD --name-status` 并限定到 SC-005 的五类产品面根（命令模板 / 技能 / 文档 / 测试 / 再生成副本与镜像，逐根路径以 SC-005 为准），在该比较单元内按产物类断言允许集闭包与补集为空——流程 / 证据 / 登记路径（`.specify/specs/104-agents-run/**`、`.specify/features.md`、`.specify/features/019-agents-command.md`、`.specify/memory/**`、`.specify/state/**`）在比较单元之外、MUST NOT 进入补集断言；结构负向面——零新增持久化根 / registry / 渲染器 / 调度器 / 队列、零新增 `/speckit.*` 命令与零新增技能、零新增 glossary 词条、零新增 flow-class / probe 单元行；行为类诚实标签——测试文本 MUST NOT 声称覆盖行为类条款；本模块是包含性守卫（红形 = 变更集出现禁止路径，由夹具腿演示），无红先步骤。
- [ ] T015 [US3] [blockedBy: T013,T014] US3 转绿与取证：运行 `tests/contract/test_agents_run_scope_contract.py` 与运行 `tests/contract/test_agents_run_skill_wiring.py`（唯一入口，`-q`）——C-18…C-21 对应函数绿、scope 模块绿；结构审计命令（`python3 .specify/scripts/python/flow-class-check.py --action check` 的单元数与发现数、对 `.specify/state/` 只读比对文件名集相对 T001 基线 `comm -13` 为空、对 `.specify/memory/` 同法）与真实输出追加 `notes/red-first-evidence.md`；本行认领 C-22（零第二机制与行为类诚实标签在技能文本与测试文本上同时成立）。 [green: contracts/agents-run-dispatch.contract.md#C-22]

**Checkpoint**: US3 独立可验——探针条件、单单元读数与零第二机制由文本断言 + 结构审计共同判定。

---

## Phase 6: User Story 4 - 一个语法、一处真源：文档与发现性同步 (Priority: P2)

**Goal**: 三份参考面与教程给出同一套能力与语法（create / refine / run）；`docs/reference/commands/agents.md` 只有一份正文；七个命名文件中的陈旧字面量封闭集清零。

**Independent Test**: `tests/contract/test_agents_run_docs_contract.py` 全绿 + `test_agents_run_command_contract.py` 的 C-06 函数绿；标题计数 = 1、C-34 全表陈旧谓词 = 0、三面语法逐字一致。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T016 [US4] [blockedBy: T004] 红先编写 `tests/contract/test_agents_run_docs_contract.py`：per `contracts/agents-run-docs.contract.md` 的 C-23…C-34 每条一个具名测试函数（单副本计数；三能力描述并断言 STR-006 为 0；Syntax 块含 STR-001 与显式 run 行；意图表 run 行 + 三能力歧义句并断言 STR-005 为 0；三技能清单；无参小节与 STR-008 为 0；command-and-skills 三能力与 run-agent 小节；overview 能力行与技能计数；design 能力行 / 工作流 / 技能清单；教程命令表与 STR-007 为 0；路由场景三能力；C-34 全表谓词全零；只读 `docs/reference/history/` 未改）；红跑 `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py -q`（当前 `^# /speckit.agents` 计数 = 3，故红）并把命令、输出、退出码写入 `notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T017 [P] [US4] [blockedBy: T004,T016] 合并 `docs/reference/commands/agents.md` 为单份正文：保留 copy 1（`:1–113`）为基底，删除 copy 2（`:114–204`）与 copy 3（`:205–299`）；正文化为三能力描述并删除 STR-006；`## Syntax` 加 STR-001 逐字与显式 `/speckit.agents run <agent-name> [task]` 行并保留无参行与自然语言意图行；意图表加 run 行、歧义句列三能力并删 STR-005；`## Companion Skills` 列 create-agent / improve-agent / run-agent 三技能；无参小节改为列举 + 建议 + 三模式摘要并删 STR-008；per `templates/commands/agents.md` 校准措辞。 [green: contracts/agents-run-command.contract.md#C-06] [green: contracts/agents-run-docs.contract.md#C-23] [green: contracts/agents-run-docs.contract.md#C-24] [green: contracts/agents-run-docs.contract.md#C-25] [green: contracts/agents-run-docs.contract.md#C-26] [green: contracts/agents-run-docs.contract.md#C-27] [green: contracts/agents-run-docs.contract.md#C-28]
- [ ] T018 [P] [US4] [blockedBy: T004,T016] 编辑 `docs/reference/agents/command-and-skills.md`：描述句改为三能力（create / refine / run）并删除两能力陈述；意图路由表加 run 行；路由流覆盖 run；单代理技能清单两→三，并为 `run-agent` 增加一节（解析 → 呈现 → 派发 → external 收集 → 报告，按指针引用其输出契约，不复制规则）；per `templates/commands/agents.md` 与只读 `skills/internal/run-agent/SKILL.md` 校准。 [green: contracts/agents-run-docs.contract.md#C-29]
- [ ] T019 [P] [US4] [blockedBy: T004,T016] 编辑 `docs/reference/agents/overview.md`：命令能力陈述加 run；技能计数陈述两→三（正文句与导航行两处）；入口图的技能层加 `run-agent`。 [green: contracts/agents-run-docs.contract.md#C-30]
- [ ] T020 [P] [US4] [blockedBy: T004,T016] 编辑 `docs/reference/agents/design.md`：命令能力行加 run；单代理命令工作流加 run 步；单代理技能清单加 `run-agent`。 [green: contracts/agents-run-docs.contract.md#C-31]
- [ ] T021 [US4] [blockedBy: T004,T016] 编辑 `docs/tutorials/installation.md` 与 `docs/tutorials/quickstart.md`：命令表行含 create / refine / run；删除 STR-007 与 C-34 的陈旧无参谓词（「生成七个角色代理」一类及其同句式变体）；per `templates/commands/agents.md` 校准无参行为。 [green: contracts/agents-run-docs.contract.md#C-32]
- [ ] T022 [P] [US4] [blockedBy: T004,T016] 编辑 `tests/scenarios/agents-command/single-entry-routing-scenario.md`：单 Agent 范围改 create / refine / run；路由表加显式 run 样例（含 `run <agent-name> [task]` 与自然语言「运行代理」形态）；歧义期望改三能力并删 STR-005；per `templates/commands/agents.md`。 [green: contracts/agents-run-docs.contract.md#C-33]
- [ ] T023 [US4] [blockedBy: T017,T018,T019,T020,T021,T022] US4 转绿与取证：运行 `tests/contract/test_agents_run_docs_contract.py` 与运行 `tests/contract/test_agents_run_command_contract.py`（唯一入口，`-q`）全绿（C-06 三面一致在此收口）；把标题计数、C-34 全表封闭谓词计数与命令输出写入 `notes/red-first-evidence.md`；本行认领 C-34（陈旧字面量封闭集在七个命名文件中为 0）。 [green: contracts/agents-run-docs.contract.md#C-34]

**Checkpoint**: US4 独立可验——文档契约全绿，且命令契约的 C-06 三面一致收口。

---

## Phase 7: User Story 5 - 失败与半成品被诚实报告，不被当作成功 (Priority: P3)

**Goal**: 不存在 / 损坏 / 配置失败 / 子代失败 / 回传缺项五类路径各有可行动的错误与部分结果，不静默成功、不编造结果。

**Independent Test**: `test_agents_run_skill_wiring.py` 的错误路径函数全绿；缺异常行的回传夹具判 incomplete。

- [ ] T024 [US5] [blockedBy: T003] 在 `tests/contract/test_agents_run_skill_wiring.py` 追加 US5 错误路径断言（每条一个具名函数）：不存在 agent → STR-002 + 有界可用项提示（声明省略条数）+ create 建议且零派发；定义目录存在而定义文件缺失 / 不可读 → 「定义损坏 / 不可读」+ 点名路径，MUST NOT 与 not-found 混同；配置解析失败 → 停止派发并报引擎的字段 / 支持集消息、不手工拼参数；子代失败 / 超时 / 触轮次上限 → 报部分结果与失败原因；回传缺五要素任一项（含缺异常行）→ 判 incomplete、不消费结论、不代填；红跑同一入口（当前技能文本缺有界列表与损坏分支，故红）并把命令、真实输出、退出码追加 `notes/red-first-evidence.md`。
- [ ] T025 [US5] [blockedBy: T024] 编辑 `skills/internal/run-agent/SKILL.md` § Input Contract 的解析失败路径：not-found 分支补有界可用项提示（声明省略条数）与 create 建议、零派发；新增 corrupt 分支（定义目录存在而定义文件缺失 / 不可读 → 「定义损坏 / 不可读」+ 点名路径，MUST NOT 与 not-found 混同）；§ Report 保留部分结果与失败原因的上报读法（超时 / 轮次上限同读法）；措辞 per `data-model.md` E2 的规则。
- [ ] T026 [US5] [blockedBy: T024,T025] US5 转绿与取证：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_skill_wiring.py -q` — 错误路径函数与既有 C-11…C-22 函数全绿；逐函数结果与错误路径文本摘录写入 `notes/red-first-evidence.md`。

**Checkpoint**: US5 独立可验——五类失败路径的文本与断言成对在位。

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 再生成镜像与副本、结构面审计、变异演练、行为类取证与收口验证——跨故事、不可提前的收尾面。

- [ ] T027 [blockedBy: T023,T026] 再生成四份逐工具命令副本：`python3 scripts/python/regen-command-copies.py` 后 `--check` exit 0，并逐份断言含 `run <agent-name> [task]`（副本只投影正文，frontmatter `argument-hint` 不是副本面）；MUST NOT 手改副本。 [green: contracts/agents-run-command.contract.md#C-09]
- [ ] T028 [blockedBy: T026] 再生成技能镜像：`python3 scripts/python/sync-mirrors.py --write --only skills/internal` 后 `--check` exit 0；`diff -q skills/internal/run-agent/SKILL.md .specify/skills/internal/run-agent/SKILL.md` 空输出；零手改镜像。
- [ ] T029 [blockedBy: T027,T028] SC-005 变更集结构审计：以 implement 起点（T001 记录的 HEAD）为 base，`git diff <base>..HEAD --name-status` 限定到 SC-005 的五类产品面根后按产物类分组核对允许集闭包与补集为空（流程 / 证据 / 登记路径在比较单元之外，不进入补集断言；复跑 `bash scripts/bash/run-tests.sh tests/contract/test_agents_run_scope_contract.py -q` 佐证），并核对零新增持久化根 / registry / 渲染器 / 调度器 / 队列、零新增 glossary 词条；命令与真实输出写入 `notes/red-first-evidence.md`。
- [ ] T030 [blockedBy: T029] SC-006 变异演练 4/4（逐项红 / 绿实测并复原）：① 删除 `templates/commands/agents.md` 的 `argument-hint` → 运行 `tests/contract/test_agents_run_command_contract.py`（唯一入口，`-q`）转红（C-01）；② 删除模板 run 意图行 → 同模块转红（C-02）；③ 删除 `skills/internal/run-agent/SKILL.md` 的七字段下行指针 → 运行 `tests/contract/test_agents_run_skill_wiring.py`（唯一入口，`-q`）转红（C-12）；④ 复制出第二份命令参考正文 → 运行 `tests/contract/test_agents_run_docs_contract.py`（唯一入口，`-q`）转红（C-23）；逐项复原后各自转绿；红 / 绿读数写入 `test-evidence/mutation-drill.md`。 [green: contracts/agents-run-docs.contract.md#C-35]
- [ ] T031 [blockedBy: T030] 行为类条款取证记录（FR-023 / quickstart S-7）：在 `test-evidence/behavior-class-evidence.md` 逐条列出 C-11 / C-12 / C-13 / C-15 / C-16 / C-18 / C-19 的行为类半边与 FR-007 / FR-008 / FR-010 / FR-011 / FR-016 / FR-017，声明取证路线 = 真源文本（已被契约测试钉住的指针部分）+ 评审 + SC-006 变异演练读数，MUST NOT 声称契约测试覆盖运行期行为；引 `test-evidence/mutation-drill.md` 为证据指针。
- [ ] T032 [blockedBy: T030,T031] 收口验证：`bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py tests/contract/test_agents_run_docs_contract.py tests/contract/test_agents_run_skill_wiring.py tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_scope_contract.py tests/contract/test_run_skills_wiring.py tests/contract/test_team_command_routing.py tests/contract/test_role_transition_payload.py tests/contract/test_fast_fail_discipline.py --names-out <failed-list-file>` 一次执行；失败名集相对 implement 入口基线的 `comm -13` 为空（既有红逐条点名）；`python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/104-agents-run` exit 0（claimed clauses = 35 / FR 24 / 24 / beyond baseline = 0）；读数写入 `notes/red-first-evidence.md`。
- [ ] T033 [blockedBy: T032] quickstart 实跑记录：执行 `quickstart.md` S-0 的三条命令（flow-class lookup、`sync-mirrors.py --check`、`regen-command-copies.py --check`）并贴真实输出；S-1…S-7 是聊天指令、不能由 shell 执行，逐条指向其钉住测试并声明该读法；落盘 `notes/quickstart-run.md`（含 teardown：无临时资源需清理）。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖——T001 先落基线。
- **Foundational**: 整段省略（无阻塞性基础设施）。
- **User Stories (Phase 3–7)**: 均依赖 Setup；US1 与 US2 同优先级（P1）：US2 的两条实现行（T011）依赖 US1 的技能编辑（T008），故按 P1 内序执行；US3 依赖 US1 / US2 的技能面（T013 blockedBy T011）；US4 的文档测试与编辑依赖模板定稿（T004）；US5 依赖技能测试模块（T003）。
- **Polish (Phase 8)**: 依赖全部用户故事完成（镜像 / 副本再生成必须在全部源编辑之后）。

### User Story Dependencies

- **US1 (P1)**: Setup 之后即可开始；其余故事的路由 / 呈现 / 派发 / 回传接线由它交付。
- **US2 (P1)**: 与 US1 共同构成 MVP；其 label 规则落在 US1 已编辑的同一技能文件上（T011 blockedBy T008）。
- **US3 (P2)**: 依赖 US1/US2 的派发面文本（探针条件与单单元边界写在同一 Run Mode）。
- **US4 (P2)**: 文档面依赖模板定稿（T004），与 US2/US3 无写目标冲突。
- **US5 (P3)**: 只依赖 US1 的测试模块（T003），与 US4 无依赖。

### Within Each User Story

- 测试先写并确认失败 → 实现 → 转绿取证（migration/regression 例外的两行在文中已具名）。
- 同一技能文件的编辑行严格按行序串行（T005 → T006 → T007 → T008 → T011 → T013 → T025）。
- 每个故事以 `**Checkpoint**` 收口，独立可验后再进入下一故事。

### Parallel Opportunities

- **US4 的五个文档 / 场景编辑行（T017 / T018 / T019 / T020 / T022）可并行**：写目标逐行不同，且都已在 ready 状态（blockedBy T004 / T016 全部完成）；T021（两个教程文件）与 T023（转绿收口）不并行。
- 其余阶段零 `[P]`：红先行共用 `notes/red-first-evidence.md` 这一追加 sink；同一技能文件的多行编辑互相串行。

---

## Parallel Example: User Story 4

```text
# 模板定稿（T004）与文档契约红先行（T016）完成后，五个编辑面可同时开工：
Task: "合并 docs/reference/commands/agents.md 为单份正文（T017）"
Task: "编辑 docs/reference/agents/command-and-skills.md 为三能力（T018）"
Task: "编辑 docs/reference/agents/overview.md 能力行与技能计数（T019）"
Task: "编辑 docs/reference/agents/design.md 能力行 / 工作流 / 技能清单（T020）"
Task: "编辑 tests/scenarios/agents-command/single-entry-routing-scenario.md 为三能力（T022）"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: **US1 + US2**——两条 P1 故事共同兑现用户原话（显式 run + 架构自动应用 + 一个 superagent 下多次 run）；两故事检查点各自独立可测，但 US2 的 label 规则落在 US1 交付的同一派发段上，拆开交付会让「多次 run 可区分」这半承诺缺席。

1. 完成 Phase 1（Setup）与 US1 的红先行。
2. 完成 US1 的模板 / 技能输入 / 呈现 / 载荷 / 回传接线 → 检查点验证。
3. 完成 US2 的 label / 可见性接线 → 检查点验证（MVP 到此可演示）。
4. 依次完成 US3（边界）→ US4（文档）→ US5（失败路径）。
5. Polish：副本 / 镜像再生成 → 结构审计 → 变异演练 → 行为类取证 → 收口验证 → quickstart 记录。

### Incremental Delivery

每一故事结束时其检查点独立可验、不破坏前序故事；镜像与副本只在全部源编辑完成后一次性再生成（plan.md § Mirror Obligations 的两行分别由 T027 / T028 承载）。

---

## Notes

- [P] 任务 = 不同写目标、无未完成依赖；共享 sink（`notes/red-first-evidence.md`）不算并行面。
- Story 标签只用于用户故事阶段行，便于按故事追踪；Setup / Polish 零 `[US` 标记。
- 行为类条款（FR-023）不冒充契约测试覆盖；其取证路线是 T030 / T031 的记录，不是新增断言。
- 既有守卫的名字级基线由 `/speckit.implement` 的 Step 0 重采（owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs），本文件不复述比较形式。
- plan-owned 面无任务行主动编辑；若实现中确需小修，按 DoD-9 声明 `PLAN-EDIT:`；实质性改动停线回抛。

