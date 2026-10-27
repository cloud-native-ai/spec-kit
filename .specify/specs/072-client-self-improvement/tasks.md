# Tasks: 客户项目的持续反馈与自我提升 (Client-Project Feedback & Self-Improvement) — 072

**Requirement ID**: 072
**Requirement Key**: `072-client-self-improvement`
**Branch**: `master`（本线未建分支；状态脊声明工作落在 master，见 requirements Assumptions A1）
**Related Feature**: Feature 072 — 客户项目的持续反馈与自我提升, status `Planned`（tasks 阶段不推进状态机；canonical 状态机无 tasks 侧取值，`Implemented` 属 `/speckit.implement`）
**Input**: Design documents from `.specify/specs/072-client-self-improvement/`
**Prerequisites**: `plan.md`（required）、`requirements.md`（required；29 FR / 7 SC / 6 user stories / 10 Shared Strings）、`research.md`（R1–R12）、`data-model.md`（E1–E10 / V1–V33）、`contracts/`（6 files, 62 clauses C-1…C-62）、`quickstart.md`（S1–S2 实跑，S3–S8 逐例豁免）、`feature-ref.md`

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" 是 test-mandating（NON-NEGOTIABLE），且本特性的两处引擎面（`git-delta-review.sh capture` / `feedback-utils.py client-metrics`）是纯确定性行为；模板/提示词/文档面由 Principle VII 的 template-only 门管辖，判据为结构契约测试（内容、路径、镜像一致性断言），两层都发。MVP 范围 = US1 + US2（采集与其"如实未采集"孪生共用同一解析器，缺一即半套机制）。

**Tests**: 五个新行为组（采集、武装态三值、打包排除、客户主体循环、度量即读即建）各一份契约测试，全部红先行——先在未改动的树上编写、跑出**记录在案的失败运行**（命令行、真实输出、退出码、失败计数，四字段落入 `.specify/specs/072-client-self-improvement/notes/red-first-evidence.md`），再实现。既有守护（071 六个套件、`test_expression_compatibility.py` C-5 冻结哈希、`test_review_p1_review_loop.py`、feedback/probe 契约族）MUST NOT 被删除/弱化，断言只增不减（C-61）；守护性复跑属迁移/回归例外，携带显式 `[blockedBy:]` 排在对应实现行之后，不作红先行声称。

**Organization**: 按 requirements.md 的六个用户故事分组（US1–US4 为 P1，US5–US6 为 P2）；Setup / Foundational / Polish 行无故事标签。62 条契约条款由 13 行以 `[green:]` 认领，每条款恰好一行，条款序号随行序升序（§ Clause Partition）。

## Definition of Done (DoD)

- DoD-1: 本文件每一行为 `[X]`，或 `[~]` 且原因记录在 `.specify/specs/072-client-self-improvement/verification.md` 的 `deferred_tasks=`。
- DoD-2: 62 条契约条款（C-1…C-62）每条款被恰好一行 `[green:]` 认领；`python3 scripts/python/account-clause-coverage.py .specify/specs/072-client-self-improvement` 报告 `status: ok`、claimed=62、beyond baseline=0、FR lane 29/29。
- DoD-3: 五个新契约测试组全部红先行（`notes/red-first-evidence.md` 每组一条四字段记录）并转绿；守护套件（071 六套件 161 测试、`test_expression_compatibility.py`、`test_review_p1_review_loop.py`、feedback/probe 族）相对 T002 基线无新增失败名、断言数只增不减。
- DoD-4: 071 闭合面逐字保留，唯一授权修订 = 非交互路径步骤枚举四步→五步（C-10，理由与代价写在修订处）；镜像对无新增漂移（判据对照 T001 测量）；探针注册面不被触碰。
- DoD-5: `verification.md` 为 SC-001…SC-007 各记录一条状态行，词表归 `.specify/templates/verification-log-template.md`。
- DoD-6: plan 约束激活期间，任何 plan 属主制品（plan.md / requirements.md / research.md / data-model.md / contracts/* / quickstart.md / feature-ref.md）不得重写；确需修订时先行声明 `PLAN-EDIT: <path> — <reason>；分类=minor|substantive`，substantive 必须停止并回传异常行，不得就地修平。
- DoD-7: 不 push、不 force、不手改运行时投影；不新增 `/speckit.*` 命令、引擎、存储、台账、评分、标识族、依赖、网络调用或常驻进程；零自动传输。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 scripts/python/validate-tasks.py .specify/specs/072-client-self-improvement/tasks.md` 退出 0。
- GATE-2: 跨制品一致性 — check: `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/072-client-self-improvement --stage tasks --repo .` 报告 `decision=pass`、`errors=0`；`missing-path` advisory 只允许命名五个计划测试文件与 `tests/fixtures/client_project.py`（实现前状态），任何其它路径的 advisory 是缺陷。
- GATE-3: 拆解尺度门 — check: `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/072-client-self-improvement/requirements.md --tasks .specify/specs/072-client-self-improvement/tasks.md` 报告 `decision=proceed`、task_count ≤ 40。
- GATE-4: 条款覆盖 — check: `python3 scripts/python/account-clause-coverage.py .specify/specs/072-client-self-improvement` 报告 `status: ok`、claimed=62、beyond baseline=0；非零 beyond-baseline 用认领修复，永不重冻结基线。
- GATE-5: 新组转绿且守护无新增失败 — check: `python3 -m pytest -q tests/contract/test_client_capture.py tests/contract/test_client_armed_state.py tests/contract/test_client_package_exclusion.py tests/contract/test_client_improve_loop.py tests/contract/test_client_metrics.py` 全绿，且守护套件失败名集合相对 `.specify/specs/072-client-self-improvement/baseline-failed.txt` 的 `comm -13` 为空（捕获形式与比较形式归 `/speckit.implement` step 6 `**Test runs**` bullet，此处引用不重述）。
- GATE-6: 镜像无新增漂移 — check: `python3 scripts/python/sync-mirrors.py --check` 除既录 loop-playbook.md 一处外无新 DIFF；`python3 scripts/python/regen-command-copies.py --check` 报告 OK。
- GATE-7: 无未完行 — check: `grep -cE '^- \[[ >]\]' .specify/specs/072-client-self-improvement/tasks.md` 返回 0。

## Environment Prerequisites

本特性无容器/镜像/集群/网络/特殊硬件依赖；全部工作为本地文件、本地 git、本地 pytest。渲染器 `delta` 与本特性无关（采集是文本面结论行；非交互路径在 071 已证明无渲染器可跑）。

- Python / pytest: **available** — probe: `python3 --version` → `Python 3.11.11`；`python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-27；affected: 全部测试与校验行。
- Shell / git: **available** — probe: `bash --version` → `GNU bash, 4.4.20(1)-release`；`git --version` → `git 2.43.5` @ 2026-10-27；affected: T003、T006、T027、T028。
- 反馈/探针引擎: **available** — probe: `feedback-utils.py --action list --kind external --format json` → `count: 0`（plan 阶段实测，quickstart S2）；`probe-utils.py --action probes --format json` → `available: True, external objects: 0, classes: 10`（quickstart S1）@ 2026-10-27；affected: T006、T010、T021。
- 镜像基线: **1 处既录漂移** — probe: `sync-mirrors.py --check` → 仅 `.specify/skills/improve-skills/references/loop-playbook.md` DIFF（plan § Mirror Obligations 既录）；`regen-command-copies.py --check` → OK @ 2026-10-27（HEAD 646e1bfe）；验收判据 = 无**新增**漂移。Affected: T027。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同相其它 [P] 行并行（写目标不同、无未完依赖）。
- **[Story]**: `[US1]`…`[US6]`；故事相位每行必有且仅有一个，Setup / Foundational / Polish 行禁止出现。
- **[blockedBy: Txxx,Tyyy]**: 所列行全部 `[X]` 前本行不得开工；`/speckit.implement` 按此拓扑排序。
- **[green: <contract>#<clause>]**: 本行是把该条款转绿的那一行；标签面定义归 `.specify/templates/tasks-template.md` § Format，机器校验归 `scripts/python/validate-tasks.py`；合同路径相对本文件目录解析。认领分区见 § Clause Partition。
- 每行给出具体文件路径与可执行验收（Test anchor / evidence），测试行写明它写入的证据槽。

## Clause Partition

62 条款、六份契约文件，每条款恰被一行认领，条款序随行序升序（每合同内前一行的条款序不大于后一行）。认领的引擎是 `account-clause-coverage.py`（claimed 计数必须等于 62），本表只是声明。

| Contract file | Clauses | Claimed by | 行内条款带 |
|---|---|---|---|
| `contracts/client-identity-and-armed-state.md` | C-1…C-9 | T009 | C-1…C-9 |
| `contracts/capture-step.md` | C-10…C-24 | T004 | C-10…C-16 |
| `contracts/capture-step.md` | — | T005 | C-17 |
| `contracts/capture-step.md` | — | T006 | C-18…C-24 |
| `contracts/digest-and-carriers.md` | C-25…C-32 | T013 | C-25…C-28 |
| `contracts/digest-and-carriers.md` | — | T014 | C-29…C-32 |
| `contracts/client-improvement-loop.md` | C-33…C-39 | T016 | C-33…C-39 |
| `contracts/cadence-and-metrics.md` | C-40…C-50 | T020 | C-40…C-45 |
| `contracts/cadence-and-metrics.md` | — | T021 | C-46…C-50 |
| `contracts/red-lines-and-surfaces.md` | C-51…C-62 | T023 | C-51, C-52 |
| `contracts/red-lines-and-surfaces.md` | — | T024 | C-53…C-57 |
| `contracts/red-lines-and-surfaces.md` | — | T025 | C-58, C-59 |
| `contracts/red-lines-and-surfaces.md` | — | T026 | C-60…C-62 |

**Partition check**: 9 + 15 + 8 + 7 + 11 + 12 = 62；无条款落在两行，无行认领其相位之后才能转绿的条款带。

## Measured Premises（2026-10-27 生成时实测，HEAD `646e1bfe`，工作树干净）

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR 定义行 | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/072-client-self-improvement/requirements.md` | `29` |
| SC 定义行 | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/072-client-self-improvement/requirements.md` | `7` |
| 用户故事 | `grep -cE '^### User Story' .specify/specs/072-client-self-improvement/requirements.md` | `6` |
| Shared Strings | `grep -cE '^\| .STR-[0-9]{3}.' .specify/specs/072-client-self-improvement/requirements.md` | `10` |
| 契约条款 | `python3 scripts/python/clause_extract.py .specify/specs/072-client-self-improvement/contracts/*.md` | 9 + 15 + 8 + 7 + 11 + 12 = `62`，六文件全 `form=md-bold-closed`（client-identity 9 / capture-step 15 / digest-and-carriers 8 / client-improvement-loop 7 / cadence-and-metrics 11 / red-lines-and-surfaces 12） |
| 条款计数陷阱形 | `grep -oh 'C-[0-9]\{1,2\}' .specify/specs/072-client-self-improvement/contracts/*.md \| wc -l` | `242` — 这是*提及*数（条款内互引 + Traceability 表），不是定义数；本测量的单位是条款*定义*，正确答案是 `62`。两数并记，表明测量是有意取的而非碰巧 |
| 五个新测试文件均不存在 | `ls tests/contract/ \| grep -E 'client_(capture\|armed_state\|package_exclusion\|metrics\|improve_loop)'` | 无输出、退出 1（T004/T009/T013/T016/T020 创建它们） |
| 夹具模块不存在 | `ls tests/fixtures/client_project.py` | `No such file or directory`（T003 创建；071 先例 `tests/fixtures/review_git_repo.py` 已存在） |
| 采集修订点现状 | `sed -n '67,83p' skills/internal/code-review/SKILL.md` | 标题为「非交互路径（Agent / CI：四步，不是三步）」、枚举四步（base / start / note / receipt+report）——T007 的唯一授权修订面；`wc -l git-delta-review.sh SKILL.md` = `1260` / `154` |
| 守护套件在树 | `grep -c "def test_" tests/contract/{review_code_composition,code_review_skill_contract,coverage_receipt,status_gate_owner,review_feedback_boundary,review_docs_isomorphism,expression_compatibility,review_p1_review_loop}.py` | `31+39+20+32+30+9 = 161`（071 六套件）+ `16`（expression-compat，含 C-5 冻结哈希）+ `10`（review-p1）；`ls tests/contract/ \| grep -cE '^test_feedback_\|^test_probe_'` = `18`（feedback/probe 族文件数） |
| 计划同步面缺口 | `ls docs/reference/commands/improve.md` | 不存在 — plan § Project Structure 把 `docs/reference/commands/{review,feedback,improve}.md` 列为同步面，`improve.md` 在树中缺失；T018 负责新建它（新文件，不违 plan），T012/T015 同步既有页 |
| 镜像基线 | `sync-mirrors.py --check` / `regen-command-copies.py --check` | 仅 `.specify/skills/improve-skills/references/loop-playbook.md` 一处 DIFF（plan 既录）+ `OK: all per-tool command copies match`；判据 = 无新增漂移 |
| 冻结覆盖基线 | `LC_ALL=C comm -13 <(grep -v '^#' coverage-baseline.txt) <(account-clause-coverage.py --freeze \| grep -v '^#')` | 正文名列表 delta = `0`（plan 阶段以 base-sha dce7790c 冻结，本阶段在 646e1bfe 复测，仅头部 `base-sha:` 行随 HEAD 移动）；**不重新冻结**——冻结时机归"每特性首次全树会计"（plan 阶段已发生），tasks 阶段只复核 |
| 既有预存失败 | plan.jsonl evidence_ptr | `test_clause_forms.py::test_the_four_md_md_forms_never_co_occur_in_one_file`（060 契约 md-bold-closed + md-heading 共现，最后触碰 e7c2ed0c，与本特性无关）——本阶段不修复，T026 的失败名比较须把它当预存项 |
| Git 快照 | `git rev-parse HEAD`; `git status --short` | `646e1bfe348cb56d30fb024d82a0316b33010bcb`（上一阶段收尾提交）；干净 |
| 行数预算 | 本文件任务行计数 | 29 行（T001–T029）≤ 40 上限 |

## Test Budget (E2 / E3 / closure)

- **E2 基线槽（implement 开始时恰好一次）**: T002 按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式捕获 `.specify/specs/072-client-self-improvement/baseline-failed.txt`；本文件其它行不得重捕获。
- **E3 定向证据行**: 实现阶段各验证行向 `.specify/specs/072-client-self-improvement/test-evidence/implement-stage-status.jsonl` 追加 `targeted-set-v1` 行（由实现期行负责，形态归 071 先例）。tasks 阶段自身为 docs-only，其 `not-run-docs-only` 行已记于 `test-evidence/tasks.jsonl`。
- **Closure 槽（review 之后）**: 驱动器的闭环节点跑一次全量并按名比较；本特性任何行不得预支。
- **本阶段不运行任何测试套件**（docs-only 预算）：确定性门（validate-tasks / decomposition-check / pre-analyze-check / account-clause-coverage）的退出码全部留档 `test-evidence/`，全部测试断言留待实现阶段。

## Mirror Obligations

权威 对表归 `plan.md` § Mirror Obligations（唯一属主）。落地形态：源编辑分散在 T007（code-review 技能）、T011（dogfooding 指南）、T014（manage-feedback 技能）、T017/T018（self-improvement 面）、T021（feedback-utils.py）；T027 是唯一的验证行（枚举每个镜像对并陈述"无新增漂移"判词）。探针注册面本特性不编辑（采集是代码段内部步骤，不是收尾面），故无 compile-embeds 再编译义务；若 T027 发现实现期意外触碰注册面，先按既有 compile → regen → sync 顺序补齐并把偏离记入异常。

## Requirement Coverage Map

每个 FR / SC 至少落在一行；无需求无行。

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T006, T009, T010, T023, T025 | FR-016 | T016, T017 |
| FR-002 | T009, T010 | FR-017 | T016, T017 |
| FR-003 | T009, T011 | FR-018 | T016 |
| FR-004 | T009, T013 | FR-019 | T006, T022, T023 |
| FR-005 | T004, T006, T007 | FR-020 | T020, T021 |
| FR-006 | T006, T009, T023, T025 | FR-021 | T020, T021 |
| FR-007 | T004, T005 | FR-022 | T020, T021, T022 |
| FR-008 | T004, T006 | FR-023 | T020, T021, T022 |
| FR-009 | T004, T006, T009, T010 | FR-024 | T023 |
| FR-010 | T013, T014 | FR-025 | T024, T026 |
| FR-011 | T013, T014 | FR-026 | T005, T006, T008, T015, T018, T024 |
| FR-012 | T013, T023 | FR-027 | T018, T024, T027 |
| FR-013 | T013, T014, T022 | FR-028 | T024 |
| FR-014 | T016, T017 | FR-029 | T003, T004, T009, T013, T016, T020, T025 |
| FR-015 | T016, T017, T019 | | |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T004, T005, T006 |
| SC-002 | T009, T010 |
| SC-003 | T013, T014, T025 |
| SC-004 | T016, T017, T018, T019 |
| SC-005 | T020, T021, T022 |
| SC-006 | T004, T009, T013, T016, T020（红先行记录）, T026（守护网） |
| SC-007 | T004（步骤枚举结构断言）, T024 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 建立证据槽并把实现期每个"红先行 / 无新增失败"声称所对照的日期化控制冻结下来。

- [X] T001 [P] 创建 `.specify/specs/072-client-self-improvement/notes/` 证据槽：`notes/red-first-evidence.md`（头部点名五个新契约测试文件，每条红先行记录四字段——命令行、真实输出、退出码、失败计数）与 `notes/pre-change-measurements.md`（日期化：python 3.11.11 / pytest 8.4.2 / bash 4.4.20 / git 2.43.5、`git rev-parse HEAD` = 646e1bfe、`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 结果、覆盖基线正文 comm delta = 0、守护套件 def 计数 161/16/10/18）。Test anchor: 两份 notes 存在且字段齐备；evidence: `notes/pre-change-measurements.md`。
- [X] T002 [P] 实现期开始时按 `templates/commands/implement.md` step 6 `**Test runs**` bullet 的捕获命令与名级比较形式，恰好一次捕获失败名基线到 `.specify/specs/072-client-self-improvement/baseline-failed.txt`（E2 槽）；本文件其它行不得重捕获或刷新（重捕获会把回归网变成移动靶）。Test anchor: 基线文件存在且名级比较锚定它；evidence: `baseline-failed.txt`。

**Checkpoint**: 两个日期化控制就位——实现期每个红/绿与无新增失败声称都有可复算的参照。

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 五个测试组共用的模拟客户项目夹具；没有它，客户侧行为无法在框架仓自测走到的另一分支上被执行（FR-029 点名这是最易被"全绿自测"欺骗处）。

- [ ] T003 新建 `tests/fixtures/client_project.py`：`make_client_project(tmp_path)` 返回临时 git 仓 + 最小安装 `.specify/` 运行时（既有引擎可按绝对路径调用、探针定义就位、`.specify/memory/feedback/` 存储目录存在），根级无 `templates`/`skills`/`shared`/`scripts`/`src/specify_cli` 五框架源目录；`make_framework_hat_twin(tmp_path)` 五目录齐备；两个工厂都暴露帽子判定入口，帽子谓词双向可证。Test anchor: 夹具两头分别得出 client / framework 帽判定（probe 注册表在夹具内可用、外部探针计数为零）；evidence: `tests/fixtures/client_project.py` + T009/T025 的引用。

**Checkpoint**: 夹具就绪——T004/T009/T013/T016/T020 全部依赖它，US1–US6 的实现才能开始。

---

## Phase 3: User Story 1 - 一次代码评审自动把发现送进客户项目自己的通道 (Priority: P1) — MVP

**Goal**: 合格评审运行恰好自动落一条指针形态客户条目（记录路径 + 适用性 + 六项按严重度计数 + 运行标识 + 客户单元），幂等、非阻塞、不搬正文。

**Independent Test**: 在武装好的客户夹具里造一个含代码 delta 的特性并跑一次非交互路径，按运行标识过滤外部条目恰有一条，六项计数与 `report --summary --format json` 逐项相等；重复采集条目数不变（SC-001）。

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T004 [P] [US1] 红先行编写 `tests/contract/test_client_capture.py` 并在未改动树上跑出记录在案的失败：非交互路径枚举为五步（结构断言，对四步现状即红）、`capture` 子命令面（C-11 参数形态）、触发合取与恰好一条（C-12）、框架帽不采集且披露不混入五值闭集（C-13）、适用性非 `run` 披露 `no-capture-object` 且零条目（C-14）、指针载荷封闭字段集且不含意见正文/逐文件清单/文件计数（C-15）、六项计数逐项抄录含零值（C-16）；失败运行四字段记入 `notes/red-first-evidence.md`。 [green: contracts/capture-step.md#C-10] [green: contracts/capture-step.md#C-11] [green: contracts/capture-step.md#C-12] [green: contracts/capture-step.md#C-13] [green: contracts/capture-step.md#C-14] [green: contracts/capture-step.md#C-15] [green: contracts/capture-step.md#C-16] Test anchor: 对未改动树 pytest 该文件非零退出、失败数 = 记录值，实现完成后同命令全绿；evidence: `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [ ] T005 [US1] [blockedBy: T004] 在 `skills/internal/code-review/scripts/git-delta-review.sh` 给 `report --summary` 增加可选 `--format json`：输出记录路径、六项按严重度计数（含零值）、blocking 计数、合入门禁判决；既有文本输出与退出码字母表（0 允许 / 1 拒绝 / 2 不可解析）逐字不动。 [green: contracts/capture-step.md#C-17] Test anchor: T004 中逐项计数相等断言转绿 + 071 既有 report 钉（`test_coverage_receipt.py` 等）不回归（T026 复核）；evidence: per `tests/contract/test_client_capture.py` 的钉住断言。
- [ ] T006 [US1] [blockedBy: T004,T005] 在同一脚本实现 `capture --review-file <record> --triage <value> [--unit <custom:owner/name>]` 子命令：帽子判定只读既有 owner 判据；运行标识取记录头日期戳（可用脚本既有运行时间戳环境变量覆写做确定性测试）；按 `(unit, run)` 幂等（引擎重复结果即答、非错误）；三条不变量（幂等 / 非阻断恒退出 0 / 不越权——不改记录、不改回执字段块、不触发传输）；汇总退出 1（门禁拒绝）照常采集、退出 2 或引擎拒绝写盘披露 `counts-unavailable`；每次运行恰好一行结论，状态符取自五值闭集后接具体细节，与适用性取值同屏可见；非采集情形零条目、不以"本次无发现"替代原因；披露只进运行收尾结论、不进过程报告代码段小节字段清单。 [green: contracts/capture-step.md#C-18] [green: contracts/capture-step.md#C-19] [green: contracts/capture-step.md#C-20] [green: contracts/capture-step.md#C-21] [green: contracts/capture-step.md#C-22] [green: contracts/capture-step.md#C-23] [green: contracts/capture-step.md#C-24] Test anchor: T004 行为断言全绿；evidence: per `tests/contract/test_client_capture.py` 的钉住断言。
- [ ] T007 [US1] [blockedBy: T006] 修订 `skills/internal/code-review/SKILL.md` § 非交互路径：四步 → 五步（基准解析、记录创建与轮转、意见落盘、回执与裁决、**客户采集**），修订处同写理由（采集所需输入在第四步之后才齐备）与代价（前序特性一处闭合枚举被改写一次）；补采集触发条件、指针形态、五值披露闭集与零条目规则。除该枚举外 071 技能面一字不动。 Test anchor: T004 的步骤枚举结构断言转绿；evidence: per `tests/contract/test_client_capture.py` 的钉住断言。
- [ ] T008 [US1] [blockedBy: T006] 更新 `templates/commands/review.md`：新增可选 `--client-unit` 参数（值语法 `custom:<owner>/<name>`，透传代码段；畸形值 = 具名 skip 行 + 零条目 + 不阻断评审）、非交互路径第五步指针、面向人结论的采集披露位；随后按镜像表跑 `regen-command-copies.py` 产出各工具副本。 Test anchor: T009 的模板断言 + T027 镜像无新增漂移；evidence: per `tests/contract/test_client_armed_state.py` 的钉住断言。

**Checkpoint**: US1 独立可验——武装客户夹具里一次评审自动落一条指针条目，重复采集不增、门禁拒绝不拦、计数逐项等于汇总命令。

---

## Phase 4: User Story 2 - 通道没准备好时如实说，绝不伪造 (Priority: P1) — MVP

**Goal**: 武装态是显式三值事实（已武装 / 未武装 / 歧义），解析一次全程复用；每种"没采集"都有具名披露与一次性指引，零条目、不阻断。

**Independent Test**: 未武装夹具跑评审——条目数不变、退出 0、输出含 `client-channel-unarmed`；两个外部探针不带单元——输出含 `client-unit-ambiguous` 不猜测；显式单元——披露写明采用显式指定（SC-002）。

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T009 [P] [US2] 红先行编写 `tests/contract/test_client_armed_state.py` 并记录失败运行：帽子判定只由既有 owner 判据承担、`feedback/` 不参与（C-1）；三值闭集与解析顺序（显式单元 > 唯一外部探针 > 其余）、一次解析全程复用（C-2）；探针对象存在是已武装必要条件、显式单元无探针对象归未武装且指引指向探针注入（C-3）；注册表不可用判未武装、**完全不调用 record 动作**、不写无 `kind`/`slice` 遗留条目、指引指向重初始化/升级 `.specify/`（C-4）；多探针未指定不猜不轮流不取最近使用（C-5）；`--client-unit` 字面量与 `custom:` 值语法、畸形值具名 skip 行（C-6）；`custom:` 单元命名与 `/speckit.*`/`skill:` 词族拒绝、Loop B 配方改写断言（C-7，落在 `test_dogfooding_practice.py` 的净增断言）；三字段作用域、无第四字段/新标识族（C-8）；武装态经探针引擎机读输出解析、注册表不被本特性修改（C-9）。 [green: contracts/client-identity-and-armed-state.md#C-1] [green: contracts/client-identity-and-armed-state.md#C-2] [green: contracts/client-identity-and-armed-state.md#C-3] [green: contracts/client-identity-and-armed-state.md#C-4] [green: contracts/client-identity-and-armed-state.md#C-5] [green: contracts/client-identity-and-armed-state.md#C-6] [green: contracts/client-identity-and-armed-state.md#C-7] [green: contracts/client-identity-and-armed-state.md#C-8] [green: contracts/client-identity-and-armed-state.md#C-9] Test anchor: 未改动树非零退出，四字段记入 `notes/red-first-evidence.md`；evidence: `notes/red-first-evidence.md`。

### Implementation for User Story 2

- [ ] T010 [US2] [blockedBy: T006,T009] 在 `capture` 子命令内补齐武装态解析分支（全特性唯一解析器，C-9/C-62）：调用方显式单元优先、仅消解歧义不豁免探针检查；唯一外部探针自动命中；零探针 / 显式单元无探针 / 注册表不可用三情形归未武装且**不发起 record 调用**；多探针未指定归歧义；畸形 `--client-unit` 值产出一条具名 skip 行（指名期望语法）后照常评审。 Test anchor: T009 全绿；evidence: per `tests/contract/test_client_armed_state.py` 的钉住断言。
- [ ] T011 [US2] [blockedBy: T009] 改写 `shared/guidelines/dogfooding.md` Loop B 配方那一行：`skill:<scenario-name>` → `custom:<owner>/<name>` 形态，同段写明理由（客户项目里 `skill:` 要么无探针对象被拒、要么解析为框架内部单元被上送），Loop B 其余说明一字不动；同步 `.specify/shared/` 镜像由 T027 统一产出。 Test anchor: T009 的配方断言（per `test_dogfooding_practice.py`）转绿；evidence: per `tests/contract/test_client_armed_state.py` 的钉住断言。
- [ ] T012 [US2] [blockedBy: T008] 更新 `docs/reference/commands/review.md` 与 `templates/commands/review.md` 对齐（`--client-unit`、第五步、结论披露；同步面）。 Test anchor: 两页与模板无相互矛盾的参数/步骤表述；evidence: `tests/contract/test_client_armed_state.py` 的模板断言 + T027。

**Checkpoint**: US2 独立可验——三种未采集情形各跑一次，条目数均不变、退出码均为 0、披露字面量逐名命中。

---

## Phase 5: User Story 3 - 客户发现就地消化，框架发现照旧上送 (Priority: P1)

**Goal**: 客户条目只走既有就地消化路径，每条恰好落到三种既有载体之一；打包侧无条件排除外部条目并报排除计数，无任何可绕过开关。

**Independent Test**: 夹具里各造一条外部与一条框架单元条目跑一次消化——两侧都被处置并各自呈报，外部条目得唯一载体；打包产物内无外部条目、报告排除计数与实际相等（SC-003）。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T013 [P] [US3] 红先行编写 `tests/contract/test_client_package_exclusion.py` 并记录失败运行：消化只走既有 Path A、无第二消费路径/清单/清理流，打包无条件排除 `kind: external` 且报告排除计数、无可绕过开关/参数/环境变量（C-25）；载体闭集恰三（todo Park 默认 / 新需求规格 / 改进循环主体）、无第四载体、一条目不指派两个（C-26）；载体边界只引用各自 owner、不复制其内容（C-27）；双向目标闭集（框架摩擦不得记客户单元、客户缺陷不得记框架侧、同一观察不双侧、单向精化规则保留且移动须呈报）（C-28）。 [green: contracts/digest-and-carriers.md#C-25] [green: contracts/digest-and-carriers.md#C-26] [green: contracts/digest-and-carriers.md#C-27] [green: contracts/digest-and-carriers.md#C-28] Test anchor: 未改动树非零退出、四字段入 `notes/red-first-evidence.md`；evidence: `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T014 [US3] [blockedBy: T013] 扩展 `skills/internal/manage-feedback/SKILL.md` 与 `skills/internal/manage-feedback/references/path-a-digest.md`：A4 载体指派（闭集三、默认 Park）、每条已消化外部条目在路由台账恰写一行具名唯一载体并列入消化呈报、无法决定的条目呈报 undecided 留给下次消化不静默丢弃（C-30）；呈报三项事实——本次帽子与武装态及解析方式、两侧各自条目数与处置结果、四条循环度量读数指针（C-29）；客户单元从注册表消失时既有条目保持可读不重写不删不重新归属、消化呈报把该单元解析失败列为具名发现（C-31）；两侧同会话各跑一次、一侧非空不得为缩短运行而静默丢弃（C-32）；原子清理语义原样、度量计算不并入清理动作。 [green: contracts/digest-and-carriers.md#C-29] [green: contracts/digest-and-carriers.md#C-30] [green: contracts/digest-and-carriers.md#C-31] [green: contracts/digest-and-carriers.md#C-32] Test anchor: T013 全绿；evidence: per `tests/contract/test_client_package_exclusion.py` 的钉住断言。
- [ ] T015 [US3] [blockedBy: T013] 更新 `templates/commands/feedback.md` 与 `docs/reference/commands/feedback.md`：客户侧消化/载体/度量呈报指针（既有打包与自省路径不动）。 Test anchor: 模板断言与 T027 镜像无新增漂移；evidence: per `tests/contract/test_client_package_exclusion.py` 的钉住断言。

**Checkpoint**: US3 独立可验——夹具内一次消化两侧呈报、外部条目恰一载体、打包产物零外部条目且排除计数相符。

---

## Phase 6: User Story 4 - 客户项目的改进循环复用同一套步骤 (Priority: P1)

**Goal**: 客户工件作为执行主体走既有 SI-0…SI-9；why 段对 `custom:` 主体如实披露"运行判定历史未评估"并改用客户通道观察，不发明来源、不伪造历史。

**Independent Test**: 对满足五条执行主体判据的客户工件跑循环——三段产物与干预台账落盘、报告"结果待定"且明写未评估披露；对无唯一可编辑定义的目标——停在 SI-0、工作树零变更（SC-004）。

### Tests for User Story 6-4 (MANDATORY) ⚠️

- [ ] T016 [P] [US4] 红先行编写 `tests/contract/test_client_improve_loop.py` 并记录失败运行：复用 SI-0…SI-9、无客户专用流程/技能/台账、执行主体五条判据无放宽（C-33）；why 段明写"运行判定历史未评估"且附引擎 fail-closed 原因原文（C-34）；观察源 = 该单元 `kind: external` 条目 + 既有证据车道、不发明来源字符串、不把"无历史"写成"过去正常"（C-35）；来源契约加宽归引擎 owner、本特性不造并行历史存储或第二观察引擎（C-36）；how 段走既有派发表与降级路径、不新增改进器、命令不直接改主体（C-37）；证伪尝试/唯一台账/硬上限/结果待定四约束逐字保留（C-38）；无唯一可编辑定义停在 SI-0、留观察给载体、零文件改动（C-39）。 [green: contracts/client-improvement-loop.md#C-33] [green: contracts/client-improvement-loop.md#C-34] [green: contracts/client-improvement-loop.md#C-35] [green: contracts/client-improvement-loop.md#C-36] [green: contracts/client-improvement-loop.md#C-37] [green: contracts/client-improvement-loop.md#C-38] [green: contracts/client-improvement-loop.md#C-39] Test anchor: 未改动树非零退出、四字段入 `notes/red-first-evidence.md`；evidence: `notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T017 [US4] [blockedBy: T016] 更新 `shared/workflow/self-improvement-workflow.md`：SI-1 增加按主体类型的观察源规则——`custom:` 主体的 why 段以客户通道条目与既有证据车道为观察源，并载明披露字面量"运行判定历史未评估"及其引擎原因形态；不触碰运行判定引擎的来源契约。 Test anchor: T016 全绿；evidence: per `tests/contract/test_client_improve_loop.py` 的钉住断言。
- [ ] T018 [US4] [blockedBy: T016] 更新 `skills/internal/self-improvement/SKILL.md`（why 段客户观察源规则）与 `templates/commands/improve.md`（`custom:` 主体路由的客户观察源指针），并**新建** `docs/reference/commands/improve.md`（plan 同步面，生成期实测缺失）；随后按镜像表同步 `.specify/skills/` 与各工具副本。 Test anchor: T016 的结构断言 + T027 镜像无新增漂移；evidence: per `tests/contract/test_client_improve_loop.py` 的钉住断言。
- [ ] T019 [US4] [blockedBy: T017,T018] 复核运行判定引擎 fail-closed 钉仍绿（`tests/contract/test_run_determination_engine.py` 对 `custom:` 主体返回 `persisted: false` + 原因，行号锚 :1393）并做一次范围扫描确认本特性未造任何并行历史存储/第二观察引擎。 Test anchor: 该既有测试不回归（属迁移/回归例外，显式 blockedBy 后置）；evidence: per `tests/contract/test_client_improve_loop.py` 的钉住断言。

**Checkpoint**: US4 独立可验——客户工件循环三段产物齐、披露诚实；模糊目标零改动停在主体解析。

---

## Phase 7: User Story 5 - 循环是否真的有效可以被判定 (Priority: P2)

**Goal**: 四条循环度量（捕获覆盖 / 进入回路 / 闭环 / 重复发现）即读即建、口径机械化、零分母报未评估，永不合成评分、永不成门禁。

**Independent Test**: 同一批记录两次呈报读数相同；任一分母清零后该指标显示"未评估"且带原因；呈报前后存储树无新增聚合/评分文件（SC-005）。

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T020 [P] [US5] 红先行编写 `tests/contract/test_client_metrics.py` 并记录失败运行："持续" = 每次合格运行采集 + 既有非阻塞阈值提示 + 显式触发，无任何调度器/常驻进程/定时器（C-40）；不回填历史、度量口径声明只覆盖武装之后的运行（C-41）；阈值协议与运行判定组合规则原样（两真才提示、非阻塞、位置与触发条件不变）（C-42）；四指标分子分母数据来源明确且全部派生自既有记录（C-43）；闭环只认 owner 文件变更证据、处置标记/carried-by/open-unverified 行语义不被当作闭环（C-44）；重复发现率按（文件,严重度）对粗代理抽取、呈报带代理标注、不表述为缺陷复现率（C-45）。 [green: contracts/cadence-and-metrics.md#C-40] [green: contracts/cadence-and-metrics.md#C-41] [green: contracts/cadence-and-metrics.md#C-42] [green: contracts/cadence-and-metrics.md#C-43] [green: contracts/cadence-and-metrics.md#C-44] [green: contracts/cadence-and-metrics.md#C-45] Test anchor: 未改动树非零退出、四字段入 `notes/red-first-evidence.md`；evidence: `notes/red-first-evidence.md`。

### Implementation for User Story 5

- [ ] T021 [US5] [blockedBy: T020] 在 `scripts/python/feedback-utils.py` 实现只读 `client-metrics` 动作（+ 选项形态以 C-47 为准、机读输出）：度量即读即建——不落盘聚合、不写任何既有存储分区、不新增目录/索引、无评分权重总分（C-46）；程序优先——派生由引擎完成、代理不得从原始 list 输出自行计算、动作无写点（C-47）；任一分母为零/缺数据该指标报 `not-evaluated` 带原因、永不报 0/100%、行不省略、代理标注随行、度量不影响任何判定（C-48）；捕获覆盖分母以通道武装时点为界（该单元首条外部条目的 created）、界外记录排除并在输出披露（C-49）；所指记录不可读的条目分子分母同排除、输出带排除计数与原因、不影响其它三指标（C-50）。 [green: contracts/cadence-and-metrics.md#C-46] [green: contracts/cadence-and-metrics.md#C-47] [green: contracts/cadence-and-metrics.md#C-48] [green: contracts/cadence-and-metrics.md#C-49] [green: contracts/cadence-and-metrics.md#C-50] Test anchor: T020 全绿；evidence: per `tests/contract/test_client_metrics.py` 的钉住断言。
- [ ] T022 [P] [US5] [blockedBy: T014,T021] 把四条度量读数接入消化呈报（反馈命令面，随 T014 的呈报三项事实落地）：度量只读呈报、不并入清理动作、不构成任何门禁/状态转换/阈值输入。 Test anchor: T014/T020 全绿；evidence: per `tests/contract/test_client_package_exclusion.py` 的钉住断言。

**Checkpoint**: US5 独立可验——夹具内四指标可复算、零分母报未评估、两次呈报读数一致、存储树无新增。

---

## Phase 8: User Story 6 - 两顶帽子各自干净：框架侧不被污染，客户侧不外流 (Priority: P2)

**Goal**: 审计者不问日志即可回答：框架库无客户缺陷、客户反馈不外流；前序特性的分类义务与打包排除在本特性里不被削弱。

**Independent Test**: 同一次含代码缺陷与框架摩擦的评审，两侧条目互不越界；打包产物内外部条目为零、排除计数相等；框架帽孪生夹具同一流程不产生任何外部条目（SC-003、SC-006、SC-007）。

- [ ] T023 [US6] [blockedBy: T006,T010] 红线扫描所有本特性触及面：四条反馈红线逐字保留且同等覆盖客户条目（目标闭集、完全可选不阻塞不催促、零自动传输唯一合法路径是手动投递、本地 workaround 价值）（C-51）；全特性无任何新增网络调用/外部服务/依赖/常驻进程（C-52）。 [green: contracts/red-lines-and-surfaces.md#C-51] [green: contracts/red-lines-and-surfaces.md#C-52] Test anchor: 扫描结论可复算（逐面 grep/结构断言）；evidence: `tests/contract/test_client_capture.py` 的传输否定断言。
- [ ] T024 [US6] [blockedBy: T008,T012,T015,T018,T022] 071 闭合面逐字断言：步骤枚举现为五步（唯一授权修订，修订处带理由与代价）、记录形态与轮转、回执退出码字母表与字段块、过程报告代码段小节封闭字段清单、评审单元收尾步骤集合、三单元普查——全部原样；无新增 `/speckit.*` 命令与命令行入口面（仅第五步子命令 + `--format json` + `--client-unit` 参数）；编辑面只有框架源、运行时投影全部经再生成/镜像产出；分发表新文案客户中立（无框架规格键/特性编号/登记表条目）且两条既有负向断言逐字保留、守护套件断言总数只增（C-53…C-57）。 [green: contracts/red-lines-and-surfaces.md#C-53] [green: contracts/red-lines-and-surfaces.md#C-54] [green: contracts/red-lines-and-surfaces.md#C-55] [green: contracts/red-lines-and-surfaces.md#C-56] [green: contracts/red-lines-and-surfaces.md#C-57] Test anchor: 逐处文本/结构断言全绿（071 既有钉 + 本行新增断言）；evidence: per `tests/contract/test_client_capture.py` 的钉住断言。
- [ ] T025 [US6] [blockedBy: T003,T010] 夹具双向验证：客户夹具内五组行为（采集/武装态/打包排除/客户循环/度量）全部在夹具里执行而非框架仓自测（C-58）；框架帽孪生夹具同一流程零外部条目新增，vendored 框架源的客户仓按帽子判据走框架分支并以 `skipped: <帽子依据句>` 披露、不混入五值闭集（C-59）。 [green: contracts/red-lines-and-surfaces.md#C-58] [green: contracts/red-lines-and-surfaces.md#C-59] Test anchor: T004/T009/T013/T016/T020 的夹具内运行 + 孪生断言；evidence: per `tests/contract/test_client_armed_state.py` 的钉住断言。
- [ ] T026 [US6] [blockedBy: T024,T025] 不重写历史：无任何既有评审报告/反馈条目被修改、无回填、遗留单体存储只读（C-60）；守护网只增不减——071 六套件（161 测试）、`test_expression_compatibility.py` C-5 冻结哈希、`test_review_p1_review_loop.py`、feedback/probe 契约族相对 T002 基线零新增失败名、断言数只增，任何无法避免的变更必须带书面兼容计划且在特性详情声明不为例外先例（C-61）；引擎有界新增恰两面——`capture` 子命令 + `--format json`（脚本）与只读 `client-metrics`（反馈引擎），无新引擎/存储/台账/评分/标识族（C-62）。 [green: contracts/red-lines-and-surfaces.md#C-60] [green: contracts/red-lines-and-surfaces.md#C-61] [green: contracts/red-lines-and-surfaces.md#C-62] Test anchor: 失败名 `comm -13` 为空 + 两面清单 grep 为空；evidence: `test-evidence/` 实现期留档。

**Checkpoint**: US6 独立可验——双向帽子各跑一次，框架侧零外部条目、客户侧零外流、守护断言只增。

---

## Phase 9: Polish & Cross-Cutting Concerns

- [ ] T027 [P] [blockedBy: T007,T011,T014,T017,T018,T021] 镜像收尾：`python3 scripts/python/sync-mirrors.py --write` 后 `--check`，判词 = 相对 T001 测量无**新增**漂移（loop-playbook.md 既录除外）；`python3 scripts/python/regen-command-copies.py --write` 后 `--check` 报告 OK；确认探针注册面未被触碰（否则先 compile → regen → sync 并把偏离记为异常）。 Test anchor: 两条 check 输出留档 `test-evidence/`；evidence: `test-evidence/` 实现期镜像输出。
- [ ] T028 [blockedBy: T025] 在客户夹具内实跑 quickstart S3–S8，把真实输出（含拆卸步骤）贴入 `.specify/specs/072-client-self-improvement/notes/quickstart-run.md`（固定落点）；**不**改写 plan 属主的 `quickstart.md`——若实现期认定必须更新其"未实现"豁免措辞，先行声明 `PLAN-EDIT: .specify/specs/072-client-self-improvement/quickstart.md — <reason>；分类=minor`，substantive 一律停止回传。 Test anchor: notes/quickstart-run.md 六场Scenario输出齐备；evidence: `notes/quickstart-run.md`。
- [ ] T029 [blockedBy: T026,T027,T028] 更新 `.specify/memory/features/072.md`（实现运行留痕；状态保持 `Planned` 直到 implement 零 `[ ]` 为止，不得提前推进）并复核 `.specify/memory/features.md` 072 行无需变更（本阶段未发现新特性、无行失效）。 Test anchor: 详情 Latest Review 增实现期记录、登记表 Total Features 不变；evidence: `.specify/memory/features/072.md`。

**Checkpoint**: 全部行 `[X]`、DoD 可翻绿、实现期证据各就其槽。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开工。
- **Foundational (Phase 2)**: 依赖 Setup（证据槽就位）；阻塞全部用户故事（夹具）。
- **User Stories (Phase 3–8)**: 都依赖 Foundational；彼此按行内 `[blockedBy:]` 细化；US1→US2 共享采集解析器，US3 依赖 US1 的条目形态，US5 依赖 US3 的消化台账口径，US6 是全局守护网，最后收口。
- **Polish (Phase 9)**: 依赖全部期望故事的完成。

### User Story Dependencies

- **User Story 1 (P1)**: Foundational 后即可开工，无其它故事依赖 — MVP。
- **User Story 2 (P1)**: Foundational 后即可开工；与 US1 共用采集解析器（T010 阻塞于 T006），与 US1 合为 MVP。
- **User Story 3 (P1)**: Foundational 后即可开工；载体台账口径被 US5 度量复用。
- **User Story 4 (P1)**: Foundational 后即可开工；只引用 US2 的 `custom:` 单元命名与 US3 的载体机制，不阻塞其开工。
- **User Story 5 (P2)**: 依赖 US3 的消化台账（闭环/进入回路口径）。
- **User Story 6 (P2)**: 依赖全部实现的行（守护网后置）。

### Within Each User Story

- 测试先写、先红、记录在案，再实现（Constitution IV）。
- 同一文件的多行编辑按 `[blockedBy:]` 串行（脚本：T005→T006→T010）。
- 故事完成后其 Checkpoint 独立可验，再开下一优先序。

### Parallel Opportunities

- T001 ∥ T002（Setup）；T004 ∥ T008（US1，测试文件 vs 命令模板）；T022（US5，反馈模板面）；T027（Polish，镜像验证）。T011/T015/T018 与故事内测试行构成写者-读者对，已由 [blockedBy:] 串行，不再标 [P]。
- 不同故事在夹具就绪后可由不同执行者并行；共享文件（`git-delta-review.sh`、`templates/commands/feedback.md`）的行按 blockedBy 串行。

---

## Parallel Example: User Story 1

```bash
# 夹具就绪（T003）后同时启动：
Task: "红先行编写 tests/contract/test_client_capture.py（T004）"
Task: "更新 templates/commands/review.md 参数与披露位（T008）"

# T005 绿后串行：
Task: "实现 report --summary --format json（T005）" → "实现 capture 子命令（T006）" → "SKILL 四步→五步（T007）"
```

---

## Implementation Strategy

### MVP First

1. 完成 Phase 1（Setup）与 Phase 2（Foundational，夹具——阻塞全部故事）。
2. 完成 MVP = US1 + US2：采集机制与其诚实失败孪生一起交付；任一单卖都是半套机制（无披露的采集会静默退化死信；无采集的披露无对象）。
3. **STOP and VALIDATE**：按 US1/US2 Checkpoint 各自独立验证（夹具内武装/未武装/歧义/显式四情形）。
4. 继续 US3 → US4 → US5 → US6（P2 收口），最后 Polish。

### Incremental Delivery

1. Setup + Foundational → 夹具就绪。
2. + US1/US2 → 采集通道可用且诚实（MVP）。
3. + US3 → 客户发现开始被消化、不外流。
4. + US4 → 客户工件可进改进循环。
5. + US5 → 循环有效性可复算。
6. + US6 → 双向帽子干净、守护网收口。

### Parallel Team Strategy

1. 全员先完成 Setup + Foundational。
2. Foundational 完成后：A=US1/US2 脚本对，B=US3/US4 技能面对，C=US5 引擎面；共享文件行用 blockedBy 串行。
3. US6 守护网与 Polish 最后由同一人收口（判词唯一出口）。

---

## Notes

- [P] = 写目标不同、无未完依赖；[Story] 标签只做追溯，不改变 blockedBy 拓扑。
- 红先行四字段（命令行、真实输出、退出码、失败计数）是 SC-006 的判定面，缺一即该组声称无效。
- 每行提交后或每逻辑组提交一次；任何 checkpoint 可停下来独立验证故事。
- 计划同步面缺口（`docs/reference/commands/improve.md` 缺失）由 T018 新建解决，属实现的新文件，不构成对 plan 的修订。
- 简报中"073/071 的六个套件"按 071 的六个套件落地（登记表中无 Feature 073；C-61 原文即"前序特性的六个新套件"）——记录此解读，实现期若发现第三个前序套件的守护义务另行列出。
- 拒用 `[~]` 之外的"先留着"：要么做完，要么显式移交并记原因。
