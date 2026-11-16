# Tasks: 长任务 line 登记与 status 可见性（Line Registry Registration）

**Requirement ID**: 102
**Requirement Key**: 102-line-registry-registration
**Related Feature**: 088 Speckit 框架可视化（Speckit Framework Visualization）— slice 行 102（`.specify/features/088-speckit-visualization.md`）
**Input**: Design documents from `.specify/specs/102-line-registry-registration/`
**Prerequisites**: `requirements.md`（23 FR / 9 SC / 9 shared strings / Clarifications A-14…A-24 / RS-001…RS-006）、`plan.md`（Constitution Check 23/23 Pass、Decision Tensions T-001…T-002、Execution Premises EP-001…EP-005 全 verified、Mirror Obligations 7 行、Inherited Blockers = none）、`research.md`（R-01…R-13 / U-1…U-5 / 基线测量）、`data-model.md`（E1–E8 / INV-01…INV-12）、`contracts/`（`line-run.contract.md` 19 条款 / `line-registration-scan.contract.md` 17 条款 / `wiring-surfaces.contract.md` 16 条款）、`quickstart.md`（S-1…S-7，S-7 已实跑）、`feature-ref.md`（24 路径交付面）

**Tests Mode**: ON — `.specify/constitution.md` Principle IV「Test-First & Contract-Driven Implementation」是 test-mandating 原则（"Write or update tests BEFORE implementing new behavior (Red-Green-Refactor)"、"Critical flows MUST have automated regression coverage"、"Acceptance scenarios from specifications become automated tests"）；本特性交付**可执行运行时**（bash 包装器 + Python 扫描器），因此 Principle VII 的 template-only gate（line 267）不适用，不得按「结构契约测试」代替行为测试。

**Tests**: MANDATORY。红先证据落在 `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md`；实现读数落在 `.specify/specs/102-line-registry-registration/test-evidence/`。本特性无迁移/回归型测试（没有需要先改消费者才能转绿的既有套件），故每个测试行都在其实现行之前，真红先成立。

**Organization**: 按 `requirements.md` 的四条用户故事（US1 P1 / US2 P1 / US3 P2 / US4 P2）切分阶段；每条故事是一个可独立验证的增量。Foundational 阶段**省略**——本特性没有阻塞所有故事的共享前置（四个交付面互不阻塞，镜像写入各自跟随作者编辑）。阶段编号从 Setup 起连续。

**Row count and ID shape**: 57 task rows, `T001`…`T057`, one ID per row, no gaps, contiguous in execution order.

## Definition of Done (DoD)

- DoD-1: **FR lane 完整** — FR-001…FR-023 每条都被至少一个任务行按 `pre-analyze-check.py` 认可的形态引用（`- [ ] T<NNN>` 行内出现该 id；表格单元或散文不算），其中 runtime `in-scope` 行 RS-006 点名的 FR-003 / FR-006 / FR-007 / FR-011 逐条在行内被引用。Check: `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/102-line-registry-registration --stage tasks --repo /cws_data/cloud-native-ai/spec-kit` 的 summary 中 `errors=0`。
- DoD-2: **SC lane 有传感器** — SC-001…SC-009 每条都有具名任务行与证据路径；`**Path**: final` 的判据（SC-001 / SC-002 / SC-003）必须拿到 `pass` 读数，`supporting` 判据按 `verification.md` 如实取值，取不到时记 `not-evaluated` 与原因。
- DoD-3: **包装器生命周期可判定** — 成功 / 失败 / SIGKILL / 登记失败 / 双失败五形态各有子进程退出码、stderr 文本与 registry 条目断言（SC-003 / SC-004），且全部只经 `line-registry.py` 写 registry。
- DoD-4: **扫描器有牙且引用单一 owner** — fixture 正反两腿都断言；活仓库声明根读数为 0 违规并落盘；四个判据常量是唯一机器可读 owner，判据成员在其它面只按路径引用。
- DoD-5: **四个接线面只给指针** — owner § 九 判据、status 命令一句、常驻 bullet、run-team 三处步骤均由路径定位；任删一处则守卫测试转红（`notes/red-first-evidence.md` 记录注入读数）。
- DoD-6: **镜像与副本是生成的** — 每个改动文件的镜像/副本以生成器产出，`sync-mirrors.py --check` 相对基线**无新增**漂移，`regen-command-copies.py --check` rc 0；未手写 `.specify/` 运行时副本。
- DoD-7: **范围克制** — 变更文件集 ⊆ `feature-ref.md` 交付面；既有未跟踪 `.specify/scripts/line-registry.py` 与 `.specify/scripts/stage-runner.sh` 未提交未还原；无 push。
- DoD-8: **本阶段裁决全部披露** — `[green:]` 标签的省略、Foundational 阶段的省略、环境前提小节保留、红先与注入复查的满足方式写在 § Notes，不折进绿里。

**DoD Status**: pending

## Completion Gate

- GATE-1: 全量/定向套件零**新增**失败——按失败用例 id 名与入口基线做集合差，不用计数比较。Check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/102-line-registry-registration/final-failed.txt` 后 `comm -13 .specify/specs/102-line-registry-registration/baseline-failed.txt .specify/specs/102-line-registry-registration/final-failed.txt` 为空（读数在 T056）。
- GATE-2: 每条镜像义务成立——`python3 scripts/python/sync-mirrors.py --check` 只报基线已有的 5 条 `DIFF`（`skills/external/` 下）与 2 条 `ORPHAN`，本特性四对（`scripts/`、`shared/`、`skills/internal/`、`templates/`）行均为 `ok`；`python3 scripts/python/regen-command-copies.py --check` rc 0。
- GATE-3: 结构与 FR lane 静默——`python3 .specify/scripts/python/validate-tasks.py .specify/specs/102-line-registry-registration/tasks.md` exit 0，且 `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/102-line-registry-registration --stage tasks --repo /cws_data/cloud-native-ai/spec-kit` 的 `decision=pass`（errors=0）。
- GATE-4: 每条 `final` 路径成功判据为 `pass` **且**本特性的 smoke 记录在位——check: `verification.md` 中每个 `**Path**` 标记为 `final` 的判据都有 `SC-NNN_status=pass`，且 `smoke_command=`、`smoke_exit_code=0`、`smoke_evidence_path=`（路径存在且非空）三项齐备；任一 `final` 判据为 `blocked` / `deferred` / `fail` 即本门失败，除非有具名用户豁免。条件集 owner：`shared/workflow/acceptance-hardening.md` § Gates。
- GATE-5: 活仓库扫描读数在位——`python3 scripts/python/line-registration-scan.py` 退出 0、`violations: 0`、`owner-skipped: 1`，且该读数与根清单已写入 `test-evidence/line-registration-scan-live.txt`。
- GATE-6: 分发与文档一致——`python3 scripts/python/flow-class-check.py --action check` rc 0；`python3 scripts/python/doc-consistency-check.py` 不适用时以 `not-evaluated` 与原因记录，MUST NOT 记成通过。
- GATE-7: 脚本接口契约成立——`bash scripts/bash/line-run.sh --help`、`bash scripts/bash/line-run.sh --version`、`python3 scripts/python/line-registration-scan.py --help` 均退出 0 且 registry 目录零写入；三者各以一个未声明选项运行均非零退出且不执行任何被包装命令。

## Environment Prerequisites

探测日期 2026-11-16，工作区 `/cws_data/cloud-native-ai/spec-kit`。每一行都以此处判决为唯一落点；任何其它载体（阶段注记、`[~]` 注记、散文行）只写日期 + `(see § Environment Prerequisites)` 指针，不复述判决。

- POSIX `bash`（包装器本体与其子进程调用）：**available** — probe: `bash --version` → `GNU bash, version 5.1.16(1)-release` @ 2026-11-16；affects: US1 全部实现行与 T013 / T016 / T018。
- `git`（包装器身份 `git rev-parse --show-toplevel`；范围审计）：**available** — probe: `git --version` → `git version 2.34.1` @ 2026-11-16；affects: T010、T050。
- CPython `>=3.8`（扫描器与测试夹具，仅标准库）：**available** — probe: `python3 --version` → `Python 3.11.0rc1`（`pyproject.toml` 声明下限 `>=3.8`）@ 2026-11-16；affects: US2 全部实现行与 T048 / T056。
- `pytest` 运行器（经唯一入口 `scripts/bash/run-tests.sh`）：**available** — probe: `python3 -m pytest --version` → `pytest 9.0.3` @ 2026-11-16；affects: 每个测试执行行。
- 既有 registry 引擎与 digest 引擎：**available** — probe: `python3 skills/external/sdd-loop-driver/scripts/line-registry.py --version` 与 `python3 .specify/skills/sdd-loop-driver/scripts/line-registry.py --version` 均 → `line-registry.py 0.0.22` @ 2026-11-16；affects: US1 / US3 / US4。
- 外部服务 / 容器 / 集群 / 网络：**不需要**（本特性零联网、零容器、零远程调用）。
- `pytest-xdist` / 仓库虚拟环境：**unavailable（既有环境条件，非本阶段引入）** — probe: `ls -d .venv` → 不存在，`python3 -c "import xdist"` → `ModuleNotFoundError: No module named 'xdist'` @ 2026-11-16；后果实测：`bash scripts/bash/run-tests.sh <path> -q` 自判 `mode=serial reason=no-xdist` 却仍向 pytest 传 `-n0`，bare `python3` 不认 `-n` 而以 usage error 退出 4（`scripts/bash/run-tests.sh` 未被本特性修改，`git status` 为空）；affects: 每个测试执行行（T003、T013、T025、T037、T045、T048、T056）——实现入口必须**先让唯一入口可用**（为解释器提供 `pytest-xdist`，或提供可用的仓库虚拟环境），MUST NOT 改用裸测试 CLI 或 `-m` 模块入口绕过（FR-021）。 **2026-11-16 复测（checklist 阶段）**：`python3 -c "import xdist"` 通过（pytest-xdist 3.8.0；pytest 9.0.3），唯一入口已可用；该修复属环境侧，`pyproject.toml` 与 `scripts/bash/run-tests.sh` 均未改动，前文保留为生成时判决。

**A13 boundary**（owner：`shared/workflow/acceptance-hardening.md` § Gates —— 本节只是指针，不是第二条规则）：本小节只记**任务生成时的探测判决**，每条带探测命令与 ISO 日期。规划期的承重前提归 `plan.md` § Execution Premises（EP-001…EP-005），本文件不复述其取值。

## Format

每行一条、**单行不折行**，形如 `- [ ] T<NNN> [P?] [US<n>?] 动作 + 文件路径 + 验收 + (FR/SC 引用) + 依赖键`。占位符语义归 `templates/tasks-template.md` § Format，本文件不复述。

- `[P]` 只标在**写目标**与本阶段其它 `[P]` 行互不相交的行上（同一文件、同一镜像对都算冲突）；同一证据文件被两行追加时不得标 `[P]`。
- 依赖键只在存在具体前置时使用，取值为逗号分隔、必须是本文件已定义的任务 id；前向引用不写。
- 本文件**不使用** `[green: <contract>#<clause>]` 归属标签，理由见 § Notes N-1；条款级归属由各故事的测试行与 `contracts/` 条款一一对应承担，FR 级可追溯性由 DoD-1 的逐行引用承担。

## Premises measured at generation time (2026-11-16)

| 量 | 实测 | 复现命令 | 朴素形态的陷阱 |
|----|------|----------|----------------|
| 声明根内被判定文件数 | 158（`scripts/bash/` 16、`scripts/python/` 49、`skills/` 93） | 递归枚举三个根，只收常规文件且（`.sh`/`.bash`/`.py` 后缀或首行 `#!`），符号链接跳过 | 用 `find … \| wc -l` 不筛后缀会把 `.md` 散文算进来；按行计数与按文件计数在含 shebang 无后缀的文件上不同 |
| `[[STR-004]]` 活仓库命中 | 0 | `grep -rn -F 'terraform apply' scripts/bash scripts/python skills \| wc -l` | 把 `tests/` 或 `templates/` 纳入根就会把夹具样本判成产线违规 |
| `[[STR-005]]` 活仓库命中 | 4，全部是 `skills/external/*/references/*.md` | `grep -rn -F 'run-tests.sh --full' scripts/bash scripts/python skills` | 按行数 4 与按文件数 2 是两个量；按文件面规则这些 `.md` 不进判定，故违规面为 0 |
| 引擎身份 | 两个候选均 `line-registry.py 0.0.22` | 对两个候选各跑 `--version` | 只看仓库内运行时那一份会漏掉 framework 源优先的解析顺序 |
| 镜像基线 | 5 `DIFF`（`skills/external/`）+ 2 `ORPHAN`（`.specify/scripts/{line-registry.py,stage-runner.sh}`），rc 2 | `python3 scripts/python/sync-mirrors.py --check` | 把既有基线当成本特性漂移，或把 `--check` 非零当成不可继续 |
| 命令副本基线 | rc 0 | `python3 scripts/python/regen-command-copies.py --check` | — |
| flow-class 台账 | 91 unit / 0 finding / rc 0 | `python3 scripts/python/flow-class-check.py --action check` | — |
| 接线面编辑前读数 | `line-run.sh` / `Single source` 在四个面全部 0 命中 | 见 T005 的逐条 `grep -c` | `grep -c` 零命中时退出 1，不能据此中断链式命令 |
| 待建交付物 | `scripts/bash/line-run.sh` 与 `scripts/python/line-registration-scan.py` 都不存在 | 直接 `test -e` | 把它们当既有脚本会写出「扩展既有文件」的假前提 |
| 夹具根 | `.specify/.tmp/line-registry-registration/` 不存在；`.specify/.gitignore` 第 30 行匹配 `.tmp/` | `test -e` + `grep -n '\.tmp' .specify/.gitignore` | 用裸 `/tmp` 或未忽略目录作夹具根违反临时目录纪律 |

## Phase Map

| Phase | 用户故事 | 目的 | 行 |
|-------|----------|------|----|
| 1 Setup | — | 证据落点与五类基线（测量、条款覆盖、失败名单、分发、接线编辑前） | T001–T005 |
| 2 US1 (P1) | 包装器自动登记、运行期在 digest 可见 | 契约 + 行为测试先红，再实现 `line-run.sh`、镜像、quickstart 实跑 | T006–T018 |
| 3 US2 (P1) | 未登记的长任务立即变红 | 契约 + 活仓库测试先红，再实现扫描器、镜像、活根注入红腿 | T019–T027 |
| 4 US3 (P2) | 判据有唯一 owner，下游表面只给指针 | owner § 九 判据、status 一句、常驻 bullet、三处镜像/再生成 | T028–T038 |
| 5 US4 (P2) | 无人值守团队运行与 status 接线不依赖记忆 | run-team §5/§6/§7 接线 + 第二段守卫 | T039–T046 |
| 6 Polish | — | quickstart 补齐、digest 无回归、分发一致、范围与零机制审计、Feature 注册面、`verification.md`、收尾门禁 | T047–T057 |

---

## Phase 1: Setup — 证据落点与基线

**Purpose**: 在动手之前把后续所有读数行的对照面固定下来；没有基线的结论一律记 `not-evaluated`。

- [x] T001 建立本规格的证据落点并把生成时实测量写入 `notes/pre-change-measurements.md`：158 个被判定文件（`scripts/bash/` 16、`scripts/python/` 49、`skills/` 93）、`[[STR-004]]` 0 命中、`[[STR-005]]` 4 命中且全为 `.md`、两个引擎候选均 `line-registry.py 0.0.22`、镜像基线 5 DIFF + 2 ORPHAN、命令副本 rc 0、flow-class 91 单元、两份待建交付物当前不存在，每条附命令与采集日期（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/pre-change-measurements.md`
- [x] T002 [P] 冻结本特性的条款覆盖基线：`python3 scripts/python/account-clause-coverage.py --spec-dir .specify/specs/102-line-registry-registration --freeze > .specify/specs/102-line-registry-registration/coverage-baseline.txt`（脚本只打印、从不写入），作为收尾判决「覆盖面无退化」的对照面（FR-021）。write: `.specify/specs/102-line-registry-registration/coverage-baseline.txt`
- [x] T003 [P] 按唯一 owner（`skills/internal/implement-feature/SKILL.md` § Step 0 与 § Test runs）记录测试入口基线：`bash scripts/bash/run-tests.sh --names-out .specify/specs/102-line-registry-registration/baseline-failed.txt`，此后一切「零新增红」以 `comm -13` 名称级比较判定，不用计数比较（FR-021）。write: `.specify/specs/102-line-registry-registration/baseline-failed.txt`
- [x] T004 [P] 采集分发一致性基线到 `test-evidence/mirror-baseline.txt`：`sync-mirrors.py --check` 的 5 条 `DIFF` 与 2 条 `ORPHAN` 逐字落盘（rc 2 是既有基线，不是本特性漂移），并随行记录 `regen-command-copies.py --check`（rc 0）与 `flow-class-check.py --action check`（91 单元 / rc 0）读数（SC-006）。write: `.specify/specs/102-line-registry-registration/test-evidence/mirror-baseline.txt`
- [x] T005 [P] 复测四个接线面的编辑前基线并落盘 `test-evidence/wiring-pre-edit-baseline.txt`：对 `templates/instructions-template.md`、`.specify/instructions.md`、`skills/internal/run-team/SKILL.md` 各跑一条 `grep -c "line-run.sh"`，对 `templates/commands/status.md` 跑 `grep -c "Single source"`，四条都应为 0（零命中时 `grep -c` 退出 1，用 `;` 或 `|| true` 隔开，不得中断链），同时记录 `.specify/.gitignore` 的 `.tmp/` 行号作为 FR-015 夹具根前提（FR-017, FR-018, FR-019, FR-015）。write: `.specify/specs/102-line-registry-registration/test-evidence/wiring-pre-edit-baseline.txt`

**Checkpoint**: 五类基线与两处证据目录就位；后续每一行都能引用一条已落盘读数。

---

## Phase 2: User Story 1 — 后台批量脚本经包装器自动登记，运行期在 digest 里可见 (Priority: P1) 🎯 MVP

**Goal**: 把「登记」变成执行批处理命令的前置条件——`line-run.sh` 在命令启动前登记 line、跑完按结果关闭，被 SIGKILL 时保留 `active` 让 digest 仍能看到它。

**Independent Test**: 隔离 `$SPECIFY_LINE_REGISTRY_DIR` 下包住一个短命令，运行期读一次 digest 断言条目出现且 `state=active`，结束后读 registry 条目断言 `state=closed` 与 reason；再用 `kill -9` 模拟 SIGKILL 断言条目残留 `active` 且 digest 仍列出。

### Tests for User Story 1 (MANDATORY) ⚠️

- [x] T006 [P] [US1] 编写脚本接口契约测试 `tests/contract/test_line_run_contract.py`：`-h`/`--help`/`--version` 退出 0 且 registry 目录前后快照不变、未声明选项 / 缺值 / 缺裸 `--` / 空命令退出 2 且哨兵文件未出现、`--opt=value` 被拒、`--` 之后的 `-h` 属被包装命令，并静态断言包装器全文不含 `journal-utils.py`（契约 C-01…C-05、C-13、C-19）（FR-011, FR-003, FR-005）。write: `tests/contract/test_line_run_contract.py`
- [x] T007 [P] [US1] 编写包装器行为测试 `tests/integration/test_line_run_behavior.py`：隔离 registry 下 `-- true` → 条目 `state=closed`/`last_event=completed`/退出 0，`-- bash -c 'exit 7'` → 退出 7 且 reason `failed`，运行期 digest 列出该 line（被包装命令保持运行到采样完成，如 `bash -c 'sleep 2'`）、结束后渲染 `[[STR-006]]`，登记失败（registry 目录不可写）时哨兵证明命令未执行，非 git 仓库退出 4，双失败按 A-24 定优先级，SIGKILL 后条目残留 `active` 且 digest 仍列出（FR-004, FR-005, FR-006, FR-007, FR-008, FR-010）。write: `tests/integration/test_line_run_behavior.py`
- [x] T008 [US1] 在包装器实现之前先跑 T006 / T007 并把红读数写入 `notes/red-first-evidence.md`：逐条给出命令、真实输出与退出码（本特性无迁移型测试，两条都是真红先）（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T006,T007]

### Implementation for User Story 1

- [x] T009 [US1] 实现 `scripts/bash/line-run.sh` 的接口面：在 `source common.sh` 之前接入 `scripts/bash/script-interface.sh` 的 `define` / `guard`，声明 `--line-id <slug>`、`--run-id <id>`、`-h`/`--help`、`--version` 与裸 `--`，用法错误退出 2 且**不启动**任何子进程（FR-003, FR-011）。write: `scripts/bash/line-run.sh` [blockedBy: T008]
- [x] T010 [US1] 在 `scripts/bash/line-run.sh` 实现身份与引擎解析：`git rev-parse --show-toplevel` 同时作为 `--project-dir` 与 `--repo-root`（不是 `$PWD`），引擎按 A-17 的有序候选从脚本自身路径解析（`../..`，该级目录名为 `.specify` 时再上移一级），非 git 仓库或两个候选都不可读 → 退出 4 并具名两个候选路径，命令不执行（FR-004）。write: `scripts/bash/line-run.sh` [blockedBy: T009]
- [x] T011 [US1] 在 `scripts/bash/line-run.sh` 实现 register → 执行 → 关闭三段：以合成 id `<line-id>-<run-id>` 与 `state active` 登记（登记失败 fail-closed，命令不执行），`--` 之后的子进程继承 stdio/cwd/env 且退出码原样传播，按结果以 `completed` / `failed` 关闭，双失败按 A-24 决定退出码并把引擎载荷写 stderr，全程只有两个引擎事件（FR-004, FR-006, FR-007, FR-009）。write: `scripts/bash/line-run.sh` [blockedBy: T010]
- [x] T012 [US1] 在 `scripts/bash/line-run.sh` 落实残留与写入面约束：不装会在不可捕获信号上伪造关闭的 trap，被 SIGKILL 时条目保持 `active`；registry 根只按既有三级解析、不新增覆盖变量；全文不调用 `scripts/python/journal-utils.py`、不自行写 JSON、不读 digest 状态、不联网（FR-005, FR-008, FR-010）。write: `scripts/bash/line-run.sh` [blockedBy: T011]
- [x] T013 [US1] 经唯一入口转绿并记录读数：`bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py tests/integration/test_line_run_behavior.py -q --names-out .specify/specs/102-line-registry-registration/test-evidence/us1-failed.txt`，命令、rc、通过/失败数与耗时写入 `us1-wrapper-green.txt`（FR-021）。write: `.specify/specs/102-line-registry-registration/test-evidence/us1-wrapper-green.txt` [blockedBy: T012]
- [x] T014 [US1] 经生成器投影包装器镜像：`python3 scripts/python/sync-mirrors.py --write --only scripts`，使 `scripts/bash/line-run.sh` 落到 `.specify/scripts/bash/line-run.sh`；镜像不得手改（FR-003）。write: `.specify/scripts/bash/line-run.sh` [blockedBy: T013]
- [x] T015 [US1] 验证包装器镜像对：`python3 scripts/python/sync-mirrors.py --check` 的 `scripts/ == .specify/scripts/` 行为 `ok`（全量 `--check` 的 rc 2 只来自既有 5 DIFF / 2 ORPHAN 基线），`diff -q scripts/bash/line-run.sh .specify/scripts/bash/line-run.sh` 空输出，且既有基线未变，读数落盘（FR-003）。write: `.specify/specs/102-line-registry-registration/test-evidence/us1-mirror.txt` [blockedBy: T014]
- [x] T016 [US1] 实跑 `quickstart.md` S-1、S-2、S-3 并把真实输出（运行期 digest 表行、条目 JSON 字段、SIGKILL 后的 digest 读数）与清理步骤写入 `notes/quickstart-run.md`；scratch 根只用 `.specify/.tmp/line-registry-registration/`（SC-001）。write: `.specify/specs/102-line-registry-registration/notes/quickstart-run.md` [blockedBy: T015]
- [x] T017 [US1] 把 SC-001 / SC-003 / SC-004 的读数分别落到 `us1-sc-001.txt`、`us1-sc-003.txt`、`us1-sc-004.txt`：运行期 digest 行、registry 条目字段（`line_id` / `state` / `last_event` / `run_history`）、退出码矩阵与 journal 目录前后计数（0 新增）逐条粘贴，不写估计值（FR-005）。write: `.specify/specs/102-line-registry-registration/test-evidence/us1-sc-001.txt` [blockedBy: T016]
- [x] T018 [US1] 注入复查（守卫有牙）：临时把 `scripts/bash/line-run.sh` 的失败关闭 reason 改成 `completed`，观察 `tests/integration/test_line_run_behavior.py` 的失败路径腿转红；随后恢复原文件并确认 `git diff -- scripts/bash/line-run.sh` 为空，红/绿两次读数都写入 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T017]

**Checkpoint**: 包装器在隔离 registry 上完成登记→执行→关闭全程，SIGKILL 残留可观测，接口契约与行为测试全绿——US1 可独立演示。

---

## Phase 3: User Story 2 — 未登记的长任务在本仓立即变红，而不是永远绿 (Priority: P1)

**Goal**: 提供一个确定性只读扫描器，对命中长任务机械判据却未登记的脚本报违规；用 fixture 与活根注入两处证明它有牙。

**Independent Test**: 在 `.specify/.tmp/line-registry-registration/` 下生成含判据成员且未登记的脚本判退出 1，改成经包装器调用后判退出 0；对活仓库声明根运行为 0 违规并把读数落盘。

### Tests for User Story 2 (MANDATORY) ⚠️

- [x] T019 [P] [US2] 编写扫描器契约测试 `tests/contract/test_line_registration_scan.py`：`-h` 退出 0、未声明选项与缺值退出 2、缺失根/非目录根/仓外根退出 2、`.md` 不进判定、符号链接跳过、四个判据常量以 `import` 读取（不硬编码成员）、fixture 正例（含 `LONG_TASK_MARKERS` 成员且无合规调用 → exit 1）与反例（同一文件保留标记并新增合规调用 → exit 0）、自声明例（带头部标记 `SELF_DECLARATION_MARKER` 且无合规调用 → exit 1）、空根例（存在但零个被判定文件 → exit 2）、`owner-skipped` 计数、同树两次读数逐行一致（契约 C-01…C-17）（FR-002, FR-012, FR-014）。write: `tests/contract/test_line_registration_scan.py`
- [x] T020 [P] [US2] 编写活仓库读数测试 `tests/integration/test_line_registration_scan_live.py`：对声明默认根断言退出 0 且 `violations: 0`，并把读数（根清单、`scanned`、`violations`、`owner-skipped`）写入 `test-evidence/line-registration-scan-live.txt`；另以 `--root` 指向一个缺失目录断言退出 2 而不是干净（FR-013, FR-016）。write: `tests/integration/test_line_registration_scan_live.py`
- [x] T021 [US2] 在扫描器实现之前先跑 T019 / T020 并把红读数（命令、输出、退出码）写入 `notes/red-first-evidence.md`，使「扫描器存在前这两条测试不可能绿」成为可复核读数（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T019,T020]

### Implementation for User Story 2

- [x] T022 [US2] 实现 `scripts/python/line-registration-scan.py` 的判据常量与文件面：模块级 `LONG_TASK_MARKERS`、`SELF_DECLARATION_MARKER`、`COMPLIANT_INVOCATIONS`、`DEFAULT_SCAN_ROOTS` 四个常量是唯一机器可读 owner；遍历只收常规文件（符号链接跳过、不越出 repo root），被判定面为 `.sh`/`.bash`/`.py` 后缀或首行 shebang（FR-002, FR-013）。write: `scripts/python/line-registration-scan.py` [blockedBy: T021]
- [x] T023 [US2] 在 `scripts/python/line-registration-scan.py` 实现判定：命中 `LONG_TASK_MARKERS` 或自带 `SELF_DECLARATION_MARKER` 且不含任何 `COMPLIANT_INVOCATIONS` 成员 → 违规（自声明只是宣布「我是长任务」，不豁免登记）；按解析路径跳过扫描器自身并计入 `owner-skipped`（FR-002, FR-014）。write: `scripts/python/line-registration-scan.py` [blockedBy: T022]
- [x] T024 [US2] 在 `scripts/python/line-registration-scan.py` 实现接口面与读数：`--root` 可重复且替换默认根、`-h` 可用、未声明选项与缺值退出 2；逐违规输出 `<path>:<line>: criterion=<content-marker|self-declaration>` 与 `root:`/`scanned:`/`violations:`/`owner-skipped:` 汇总块，路径按字典序确定；退出码闭集 0/1/2 且 2 优先；全程只读、不派生进程、不联网（FR-012）。write: `scripts/python/line-registration-scan.py` [blockedBy: T023]
- [x] T025 [US2] 经唯一入口转绿并记录读数：`bash scripts/bash/run-tests.sh tests/contract/test_line_registration_scan.py tests/integration/test_line_registration_scan_live.py -q --names-out .specify/specs/102-line-registry-registration/test-evidence/us2-failed.txt`，rc、通过数与耗时写入 `us2-scanner-green.txt`（FR-021）。write: `.specify/specs/102-line-registry-registration/test-evidence/us2-scanner-green.txt` [blockedBy: T024]
- [x] T026 [US2] 投影并验证扫描器镜像：`python3 scripts/python/sync-mirrors.py --write --only scripts` 把 `scripts/python/line-registration-scan.py` 落到 `.specify/scripts/python/line-registration-scan.py`，随后 `python3 scripts/python/sync-mirrors.py --check --only scripts` 的 `scripts/ == .specify/scripts/` 行为 `ok`、`diff -q` 空输出；该 scoped `--check` 的 rc 2 只来自既有 2 条 ORPHAN（`.specify/scripts/{line-registry.py,stage-runner.sh}`）基线，不是本特性漂移（FR-012）。write: `.specify/scripts/python/line-registration-scan.py` [blockedBy: T025]
- [x] T027 [US2] 在既有可跟踪根上证明扫描有牙且可还原：临时新增 `scripts/bash/zz-scan-red-leg.sh`（含一个 `LONG_TASK_MARKERS` 成员且无合规调用）→ 扫描退出 1 并点名该文件；删除该文件后复扫退出 0；两次读数与 `git status --porcelain scripts/bash/` 的恢复证据写入 `us2-teeth.txt`；再做两次常量删除注入并各观察红、还原（删除 `COMPLIANT_INVOCATIONS` 一个成员 → fixture 合规腿转红；移除自声明识别 → 自声明腿转红），红/绿读数与还原证据同写入 `us2-teeth.txt`（SC-002）。write: `.specify/specs/102-line-registry-registration/test-evidence/us2-teeth.txt` [blockedBy: T026]

**Checkpoint**: 扫描器在 fixture 与活根两处都能红、都能绿，活仓库读数为 0 违规且已落盘——US2 可独立演示。

---

## Phase 4: User Story 3 — 判据有唯一 owner，下游表面只给指针 (Priority: P2)

**Goal**: owner 文档 § 九 拥有判据与判定边界（唯一承载点）；`status.md` 只声明 line 可见性以 registry 为唯一来源；常驻小节只有一句指针；除 owner 文档外的三处下游面都不复述阈值或机械字面量。

**Independent Test**: 阅读四个表面的文本与引用方向，并对「删掉常驻提醒」与「在 status.md 里复述判据」各做一次篡改注入，断言守卫测试各自转红。

### Tests for User Story 3 (MANDATORY) ⚠️

- [x] T028 [P] [US3] 编写接线契约测试 `tests/contract/test_line_registration_wiring.py` 的第一段（契约 C-01…C-09）：`shared/guidelines/reporting-obligations.md` § 九 含判据与判定边界并点名载体与引擎写入方、`templates/commands/status.md` 含逐字 `Single source` 句且无第二渲染面/进程发现逻辑、`templates/instructions-template.md` 在 `Exemptions and precedence` 之后恰有一条指针 bullet、`.specify/instructions.md` 同句恰好一次且四个符号链接解析到它；断言面收窄为**除 owner 文档外的三个下游面**（`templates/commands/status.md`、`templates/instructions-template.md`、`.specify/instructions.md`/符号链接）都不复述阈值与机械字面量——owner 文档 § 九 是唯一承载点（T030），不在此断言（FR-001, FR-018, FR-019）。write: `tests/contract/test_line_registration_wiring.py`
- [x] T029 [US3] 跑 T028 的第一段并记录红（四个面尚未编辑）到 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T028]

### Implementation for User Story 3

- [x] T030 [US3] 在 `shared/guidelines/reporting-obligations.md` § 九 追加长任务登记判据：预计超过 5 分钟或含后台批量 apply/verify 的运行 MUST 启动时登记、按阶段刷新、结束时关闭；未登记即不入 digest，`[[STR-006]]` 是准确结论而非漏报；同时声明 digest 的真实不变量（line 可见性唯一来源是 registry；存活探测仅限已登记 PID；绝不发现未登记进程）；阈值与判定边界在本文件拥有，**本行是该阈值与判定边界的唯一 owner 承载点**，下游三个面只按路径引用；载体是 `scripts/bash/line-run.sh`、registry 写入方是 `line-registry.py`（不是 `journal-utils.py`），§ 十一 的零新增机制禁令照旧（FR-001, FR-005）。write: `shared/guidelines/reporting-obligations.md` [blockedBy: T029]
- [x] T031 [US3] 投影 owner 文档镜像：`python3 scripts/python/sync-mirrors.py --write --only shared` 把 `shared/guidelines/reporting-obligations.md` 落到 `.specify/shared/guidelines/reporting-obligations.md`，以 `--check` 的 `shared/` 行 `ok` 与 `diff -q` 空输出验收（FR-001）。write: `.specify/shared/guidelines/reporting-obligations.md` [blockedBy: T030]
- [x] T032 [US3] 在 `templates/commands/status.md` 的 Delegation 段落加且只加一句逐字的 `Single source` 声明（line 可见性以 Line Registry 为唯一来源、存活探测仅限已登记 PID、绝不发现未登记进程、义务按路径引用 owner § 九），不新增渲染逻辑、不改动作集（FR-018）。write: `templates/commands/status.md` [blockedBy: T029]
- [x] T033 [US3] 经 `python3 scripts/python/regen-command-copies.py` 再生成四份 per-tool 命令副本（`.claude/commands/speckit.status.md`、`.github/prompts/speckit.status.prompt.md`、`.qoder/commands/speckit.status.md`、`.opencode/command/speckit.status.md`）并以 `--check` rc 0 验收，四个副本 `grep -c "Single source"` 各为 1（FR-018）。write: `.claude/commands/speckit.status.md` [blockedBy: T032]
- [x] T034 [US3] 在 `templates/instructions-template.md` 的 `## Progress Reporting Discipline` 内、`Exemptions and precedence` bullet 之后追加**恰好一条**指针 bullet（一句话 + `shared/guidelines/reporting-obligations.md` § 九 路径），不新建小节、不改其它 bullet、不含阈值与机械字面量（FR-019）。write: `templates/instructions-template.md` [blockedBy: T029]
- [x] T035 [US3] 投影模板镜像：`python3 scripts/python/sync-mirrors.py --write --only templates` 把该模板落到 `.specify/templates/instructions-template.md`，以 `--check` 的 `templates/` 行 `ok` 与 `diff -q` 空输出验收（FR-019）。write: `.specify/templates/instructions-template.md` [blockedBy: T034]
- [x] T036 [US3] 经 `/speckit.instructions` 的**小节级刷新**把该 bullet 带进 `.specify/instructions.md`：请求里显式点名 `## Progress Reporting Discipline` 小节，不得手改 live 文件，也不得只依赖 `bash scripts/bash/generate-instructions.sh`（后者按顶层级小节增量、其契约测试禁止修改既有小节，R-10 已实测）；随后验证 `AGENTS.md`、`CLAUDE.md`、`QODER.md`、`.github/copilot-instructions.md` 四个链接仍解析到该文件且内容显示该句（FR-019）。write: `.specify/instructions.md` [blockedBy: T035]
- [x] T037 [US3] 经唯一入口把第一段转绿：`bash scripts/bash/run-tests.sh tests/contract/test_line_registration_wiring.py -q`，读数（本行时点该文件只含 C-01…C-09 段）写入 `us3-wiring-green.txt`（FR-021）。write: `.specify/specs/102-line-registry-registration/test-evidence/us3-wiring-green.txt` [blockedBy: T031,T033,T036]
- [x] T038 [US3] 验证 status 命令面未被改动超出那一句：`python3 scripts/python/status-digest.py --help` 退出 0 且零 registry 写入、`git diff -- templates/commands/status.md` 只有新增的那一句、动作集与退出码闭集与 `[[STR-006]]` 渲染未变，读数落盘（FR-020）。write: `.specify/specs/102-line-registry-registration/test-evidence/us3-status-surface.txt` [blockedBy: T033]

**Checkpoint**: 四个表面各就各位、引用方向单向（下游只指路径），第一段守卫全绿——US3 可独立验证。

---

## Phase 5: User Story 4 — 无人值守团队运行与 status 接线不再依赖记忆 (Priority: P2)

**Goal**: 把登记义务写进 run-team 的执行步骤：运行前登记、编排中按步骤边界刷新、写报告前关闭并把 `line_id` 交给报告。

**Independent Test**: 守卫测试断言三处步骤存在且引擎路径被引用；删除任一处即转红；不修改 `create-team` 的 Report 契约文件。

### Tests for User Story 4 (MANDATORY) ⚠️

- [x] T039 [P] [US4] 在 `tests/contract/test_line_registration_wiring.py` 追加第二段（契约 C-10…C-13）断言：`skills/internal/run-team/SKILL.md` §5 顶部登记（两个引擎候选具名、登记失败在任何席位派发前 fail-closed）、§6 每个编排步骤边界一次 `update --last-event`、§7 写报告前关闭且 `line_id` 进报告正文、关闭失败须写明、`skills/internal/create-team` 的 Report 契约未被改、技能内无引擎参数表（FR-017）。write: `tests/contract/test_line_registration_wiring.py` [blockedBy: T037]
- [x] T040 [US4] 跑第二段并记录红（run-team 尚未接线）到 `notes/red-first-evidence.md`（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T039]

### Implementation for User Story 4

- [ ] T041 [US4] 在 `skills/internal/run-team/SKILL.md` §5 Present & Execute 顶部加登记步骤：按 A-18 的 run-id 生成规则（`r<UTC yyyymmdd>T<UTC hhmmss>Z-<4 位小写十六进制>`，必须匹配引擎 `RUN_ID_RE`；不得沿用裸 UTC 时间戳）生成 run-id，并以 A-18 的合成规则组成 `<team-slug>-<run-id>`，经引擎 `register` 登记为 `active`，登记失败在任何席位派发之前 fail-closed 停下；§2 五查判 `blocked` 时不登记，避免留下悬空 line；引擎动作与参数按其 `--help` 读取，技能内不复述参数表（FR-017）。write: `skills/internal/run-team/SKILL.md` [blockedBy: T040]
- [ ] T042 [US4] 在 `skills/internal/run-team/SKILL.md` §6 Orchestrate 指明：每个编排步骤边界调一次引擎 `update --last-event <step-label>` 刷新同一条 line，且不存在定时器、守护进程、心跳文件或第二 liveness 通道（FR-017）。write: `skills/internal/run-team/SKILL.md` [blockedBy: T041]
- [ ] T043 [US4] 在 `skills/internal/run-team/SKILL.md` §7 Report 写明：写报告之前经引擎关闭该 line，报告正文携带 composed `line_id`，关闭失败必须在报告中写明而不是吞掉（FR-017）。write: `skills/internal/run-team/SKILL.md` [blockedBy: T042]
- [ ] T044 [US4] 投影技能镜像：`python3 scripts/python/sync-mirrors.py --write --only skills/internal/run-team` 把 `skills/internal/run-team/SKILL.md` 落到 `.specify/skills/internal/run-team/SKILL.md`，以 `python3 scripts/python/sync-mirrors.py --check --only skills/internal/run-team` 验收：必须出现 `scope --only: skills/internal/run-team` 与 `ok    skills/internal/ == .specify/skills/internal/ (1 files, byte-identical)`、rc 0（2026-11-16 实测），且 `diff -q` 空输出。`--only` 只接受镜像对前缀（`skills/internal` / `skills/external`），`--only skills` 报 `error: --only prefix matches no mirror pair or regen surface: skills` 且 rc 2，禁止使用（FR-017）。write: `.specify/skills/internal/run-team/SKILL.md` [blockedBy: T043]
- [ ] T045 [US4] 经唯一入口把第二段转绿并做注入复查：`bash scripts/bash/run-tests.sh tests/contract/test_line_registration_wiring.py -q` 全绿，读数写入 `us4-wiring-green.txt`；再对 §5 / §6 / §7 各删一处、`templates/commands/status.md` 的 Single source 句与 `templates/instructions-template.md` 的指针 bullet 各删一次做注入（观察红、还原、含对应镜像/副本的 `git diff` 为空）（FR-021, SC-005）。write: `.specify/specs/102-line-registry-registration/test-evidence/us4-wiring-green.txt` [blockedBy: T044]
- [ ] T046 [US4] 把三处落点的定位读数写入 `us4-run-team-locators.txt`：`grep -n "line-registry.py" skills/internal/run-team/SKILL.md` 至少三处（登记 / update / 关闭）、`grep -n "line_id" skills/internal/run-team/SKILL.md` 命中 §7，并列出被引用的引擎动作（登记 / 刷新 / 关闭）（FR-017）。write: `.specify/specs/102-line-registry-registration/test-evidence/us4-run-team-locators.txt` [blockedBy: T045]

**Checkpoint**: 三处步骤与报告字段义务就位、第二段守卫全绿——US4 可独立验证。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 补齐 quickstart、digest 无回归、分发一致、范围与零机制审计、注册面与收尾产物。

- [ ] T047 补齐 quickstart 的可执行场景：实跑 S-4（fixture 正反两腿）、S-5（活仓库读数）、S-6（三处 grep 定位），把真实输出与清理步骤追加到 `notes/quickstart-run.md`（FR-015, FR-016, FR-018）。write: `.specify/specs/102-line-registry-registration/notes/quickstart-run.md` [blockedBy: T027,T046]
- [ ] T048 跑既有 digest 套件（`tests/contract/test_status_digest.py`、`tests/contract/test_status_digest_roles.py`、`tests/unit/test_status_digest_unit.py`）经唯一入口，记录 pass 数与 `comm -13` 名称级零新增红，并断言 `scripts/python/status-digest.py` 零改动（FR-020, SC-007）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-digest-regression.txt`
- [ ] T049 分发一致性收尾并在 `polish-distribution.txt` 记录：`sync-mirrors.py --check` 只报基线的 5 DIFF / 2 ORPHAN（本特性四对镜像全 `ok`）、`regen-command-copies.py --check` rc 0、`flow-class-check.py --action check` rc 0、`doc-consistency-check.py` 不适用时记 `not-evaluated` 与原因（MUST NOT 记成通过）（SC-006）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-distribution.txt` [blockedBy: T044]
- [ ] T050 范围克制审计（本行在唯一提交 T057 之前执行，故 `git diff` 必须与未跟踪清单合并，否则全部新文件不可见）：完整变更集 = `git diff --name-only "$(git merge-base master HEAD)" -- <交付面路径>` ∪ `git ls-files -o --exclude-standard -- <同一交付面路径>`，其中 `<交付面路径>` = `scripts/ shared/ skills/ templates/ tests/ .claude/ .github/ .qoder/ .opencode/ .specify/scripts/ .specify/shared/ .specify/skills/ .specify/templates/ .specify/specs/102-line-registry-registration/ .specify/features.md .specify/features/088-speckit-visualization.md .specify/instructions.md`；该集合减去既有未跟踪 `.specify/scripts/line-registry.py` 与 `.specify/scripts/stage-runner.sh` 后 MUST ⊆ `feature-ref.md` § Delivery surface 的 24 路径；另 `git status --porcelain` 显示两份既有脚本仍为未跟踪（未提交未还原），`git log master..HEAD --oneline` 只含本特性提交且无 push 产物，读数逐行落盘（FR-023, SC-009）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-scope.txt`
- [ ] T051 零新增机制审计：静态确认没有调度器、定时器、守护进程、心跳文件、第二 registry、第二状态脊或台账被引入（对包装器与扫描器全文 grep，`git diff --name-only` 不含 `pyproject.toml`），第三方依赖零新增（FR-022）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-zero-machinery.txt`
- [ ] T052 按 Feature Integration Protocol 更新注册面：在 `.specify/features.md` 的 102 行备注追加本次 tasks 阶段说明（测试模式、行数、门禁读数），父行 088 保持 `Completed` 不回退，并在 `.specify/features/088-speckit-visualization.md` 追加本切片的 tasks 阶段说明。write: `.specify/features.md`, `.specify/features/088-speckit-visualization.md`
- [ ] T053 写 `verification.md`：SC-001…SC-009 逐条状态与证据路径；`**Path**: final` 的判据（SC-001 / SC-002 / SC-003）必须 `pass` 且带 `smoke_command=` / `smoke_exit_code=0` / `smoke_evidence_path=`，SC-008 的复述检查按 `shared/guidelines/user-facing-comprehension.md` 的基准读者执行，做不到时记 `not-evaluated` 与原因（SC-008）。write: `.specify/specs/102-line-registry-registration/verification.md` [blockedBy: T047,T048]
- [ ] T054 收尾门禁三件套并把 rc 与摘要写入 `polish-gates.txt`：① `python3 .specify/scripts/python/validate-tasks.py .specify/specs/102-line-registry-registration/tasks.md` → rc 0；② `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/102-line-registry-registration --stage tasks --repo /cws_data/cloud-native-ai/spec-kit` → rc 0 且 `decision=pass`、`errors=0`；③ `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/102-line-registry-registration/requirements.md --tasks .specify/specs/102-line-registry-registration/tasks.md` → rc 0 且 JSON 的 `"decision": "proceed"`（该工具必填 `--requirements`，且只以 JSON 输出 `"decision": "proceed"`，字面量 `decision=proceed` 不会出现；2026-11-16 实测 `fr_count=23 / task_count=57`）；三条都 MUST 记录 rc 与原始输出首行，任一非预期即停下上送显式异常行，不得改写判据迁就读数（FR-021）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-gates.txt`
- [ ] T055 红先证据完整性复核：逐条核对 `notes/red-first-evidence.md` 的每个红点都有命令、真实输出与退出码，且对应测试在实现后转绿；缺任一者补齐读数，不得用「跑一遍是绿的」代替（FR-021）。write: `.specify/specs/102-line-registry-registration/notes/red-first-evidence.md` [blockedBy: T045]
- [ ] T056 一次跑齐本特性新增测试与既有 digest 守卫：`bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py tests/contract/test_line_registration_scan.py tests/contract/test_line_registration_wiring.py tests/integration/test_line_run_behavior.py tests/integration/test_line_registration_scan_live.py tests/contract/test_status_digest.py tests/contract/test_status_digest_roles.py tests/unit/test_status_digest_unit.py -q --names-out .specify/specs/102-line-registry-registration/final-failed.txt`，记录 rc、通过/失败与耗时作为收尾定向读数（FR-021）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-targeted-suite.txt` [blockedBy: T055]
- [ ] T057 只提交本特性产物：按显式路径 `git add`（framework 源、镜像、五份测试、四个文本面、本 spec 目录产物与 Feature 注册面），不 `git add -A`，两份既有未跟踪脚本不提交不还原，不 push；提交信息按 `templates/commit-template.md` 的单行形态（FR-023）。write: `.specify/specs/102-line-registry-registration/test-evidence/polish-commit.txt` [blockedBy: T056]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无前置，可立即开始；T002–T005 之间互不依赖（不同落点）。
- **US1 (Phase 2)**: 依赖 Setup 的基线落点；内部严格按「测试 → 红 → 实现 → 绿 → 镜像 → 实跑 → 证据 → 注入复查」推进。
- **US2 (Phase 3)**: 与 US1 无硬依赖（扫描器的合规调用检测是文本匹配，不要求包装器先存在），但按优先级顺序执行。
- **US3 (Phase 4)**: 与 US1 / US2 无硬依赖；是「判据 + 指针」的文本面。
- **US4 (Phase 5)**: 依赖 US3 的守卫测试文件存在（第二段追加到同一文件），除此之外独立。
- **Polish (Phase 6)**: 依赖全部故事完成；T057（提交）必须是最后一行。

### User Story Dependencies

- **US1 (P1)** 与 **US2 (P1)** 各自独立可测，合起来构成 MVP（缺一即「判据只有一半牙齿」：没有包装器则登记仍靠记忆，没有扫描器则判据只是措辞）。
- **US3 (P2)** / **US4 (P2)** 都独立于 US1/US2 的运行时行为，但引用同一 owner 路径；四个面路径不一致即视为缺陷。

### Within Each User Story

- 测试先写、先观察红，再实现；实现后经唯一入口转绿；随后镜像与实跑读数。
- 镜像写入永远跟随作者编辑，且只经生成器。

### Parallel Opportunities

- Setup 的 T002 / T003 / T004 / T005 四行可并行（四个不同落点）。
- US1 的 T006 / T007 可并行（两份不同测试文件）；实现链 T009→T013 与证据链 T014→T018 串行。
- US2 的 T019 / T020 可并行；实现链 T022→T027 串行。
- US3 / US4 的守卫是同一文件的两段，因此串行（T028 → T039）。
- 跨故事：若有多人，US3 与 US1/US2 可并行（写领地互不相交），US4 需等 US3 的守卫文件落地。

## Parallel Example: Setup 与 US1 测试腿

```bash
# Setup 的四个不同落点可同时开始
Bash: "冻结条款覆盖基线"        # write: coverage-baseline.txt
Bash: "记录测试入口失败名单基线"  # write: baseline-failed.txt
Bash: "采集分发一致性基线"        # write: test-evidence/mirror-baseline.txt
Bash: "复测接线面编辑前读数"      # write: test-evidence/wiring-pre-edit-baseline.txt

# US1 的两份测试文件互不相干
Bash: "编写 line-run 契约测试"    # write: tests/contract/test_line_run_contract.py
Bash: "编写 line-run 行为测试"    # write: tests/integration/test_line_run_behavior.py
```

## Implementation Strategy

### MVP First

**MVP 范围 = US1 + US2**（两条同为 P1，且只有合起来才构成可独立验证的机制：包装器让登记顺手发生，扫描器让「未登记」立刻变红；缺任一条，判据都只剩一半牙齿）。

1. 完成 Phase 1（Setup）：基线全部落盘。
2. 完成 US1：包装器红→绿、镜像、quickstart S-1…S-3 实跑。
3. 完成 US2：扫描器红→绿、镜像、活根注入红腿。
4. **STOP and VALIDATE**：分别按两条故事的 Independent Test 独立验证，任一不通过不得进入 P2。
5. 继续 US3 → US4 → Polish。

### Incremental Delivery

1. Setup 完成 → 所有结论都有对照面。
2. US1 完成 → 一个批量脚本可以经包装器变为 digest 可见。
3. US2 完成 → 未登记的同类脚本在本仓立即变红。
4. US3 完成 → 判据有唯一 owner，下游只给指针；常驻提醒进入每个会话的第一屏。
5. US4 完成 → 无人值守团队运行自动携带登记义务。
6. Polish 完成 → 分发一致、范围克制、`verification.md` 就位。

## Notes

- **N-1 `[green:]` 标签的省略（本阶段裁决）**: 三条契约的条款以 `## C-NN` 标题形态声明，`clause_extract.py` 只把标题形态解析为可解析条款 id（`line-run` 11 个、扫描器 9 个、接线 5 个），而契约正文的非标题条款（如 `C-02`、`C-09`、`C-12`）不可解析。若逐条打标，会把一半条款排除在归属之外并制造 `green-cross-phase` 噪声，故本文件不打标签（与 101 的 N-4 同形）；条款级归属由「契约文件 ↔ 其守卫测试文件」的一一对应承担，FR 级由 DoD-1 承担。
- **N-2 Foundational 阶段的省略**: 本特性没有阻塞全部故事的共享前置（四个交付面互不阻塞，镜像跟随各自作者编辑），因此按模板规则省略 Phase 2/Foundational 并连续编号。
- **N-3 环境前提小节的保留**: 模板允许「无外部环境依赖时删除该小节」，但本特性的每一行都依赖本机 `bash` / `git` / CPython / pytest 的可判定存在；保留该小节作为这些探测判决的唯一落点，行内只写日期 + 指针。
- **N-4 红先与注入复查的形态**: 五份测试都是新行为测试，因此都是真红先（T008 / T021 / T029 / T040 记录红）。守卫在主体之后落地时（T018 / T045），以**注入复查**补足：改写主体让守卫必须转红、观察红、还原并证明 `git diff` 为空——这两条都是可复核的红，而不是「跑一遍是绿的」。
- **N-5 活根注入的纪律**: T027 会在既有可跟踪根内临时新增一个违规脚本；该行必须在同一次执行内删除它，并以 `git status --porcelain scripts/bash/` 的空读数作为恢复证据。留下该文件即把本特性自己变成扫描器的违规对象。
- **N-6 `templates/commands/status.md` 没有命令镜像**: 该镜像已退役（plan 的 Mirror Obligations 表已记录），副本只经 `regen-command-copies.py` 生成四套 per-tool 文件，因此 T033 的验收面是四份副本而不是镜像对。
- **N-7 本阶段未改 plan-owned 工件**: 本文件不修改任何 plan-owned 文件（`plan.md` / `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md`），`plan_constraint=active` 下本轮 PLAN-EDIT 计数为 0。
- **N-8 测试入口的环境条件（生成时实测，见 § Environment Prerequisites 最后一条）**: 本轮只做了一次运行器**可用性探测**（`bash scripts/bash/run-tests.sh tests/integration/test_two_line_isolation.py -q`，rc 4 / usage error），目的是确认下一阶段的测试入口能否工作，**不是**本阶段的选择集；本阶段仍按 docs-only 记 `not-run-docs-only`。该条件不影响本文件的分解正确性，但实现入口动手前必须先把它修掉，且修复方式只能是环境侧（提供 `pytest-xdist` 或可用虚拟环境），不得改成裸测试 CLI。
