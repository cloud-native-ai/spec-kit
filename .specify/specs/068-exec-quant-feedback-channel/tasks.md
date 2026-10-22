# Tasks: 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel）— 068

**Requirement ID**: 068
**Requirement Key**: `068-exec-quant-feedback-channel`
**Branch**: `068-exec-quant-feedback-channel`（单写线，trunk master）
**Related Feature**: Feature 068 执行量化数据反馈回传与汇总（Exec-Quant Feedback Channel），状态 Planned
**Input**: Design documents from `.specify/specs/068-exec-quant-feedback-channel/`
**Prerequisites**: plan.md（required）、requirements.md（required，19 FR / 6 SC）、research.md（D1–D14）、data-model.md（E1–E8）、contracts/ ×4（31 条款 C-1…C-31）、quickstart.md（场景 0–5）、feature-ref.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating — unit tests for pure functions/utilities and contract/regression coverage for critical flows; this feature ships executable runtime Python in two engines (`feedback-utils.py` / `exec-quant.py`), so the template-only gate does not apply. Red-first evidence is mandatory for US1/US2/US3 new-behavior tests; US4 is a regression net and uses the migration/regression exception of `create-tasks` (guard tests land after the behavior they exercise, with explicit `[blockedBy:]`) — each such row says so explicitly.)

**Tests**: 每支新测试先以未实现状态跑出失败并把命令、真实输出、退出码写入 `notes/red-first-evidence.md`（引用门行时逐字引用该行 id + 名称 + 检查命令，不裸引 id）。失败测试名基线按其 owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 捕获与比较；预算槽位与槽位纪律见 § Test Budget (E2/E3/closure)——本文件不复述其比较形式。

**Organization**: 按用户故事组织：US1（P1 打包腿）与 US2（P1 接收腿）共同构成 MVP；US3（P2 汇总腿）消费 US2 落地的聚合层数据；US4（P2 边界腿）与前三条并行守护安全边界与非回归。Setup 冻结改前基线与 E2 全量基线；无 Foundational 阶段（三腿互不阻塞：US1/US2 同文件不同函数、US3 只读聚合层可对夹具开发，见 § Dependencies）；Polish 收口文档/镜像/quickstart/SC 证据/Completion Gate。

## Definition of Done (DoD)

- DoD-1: 所有任务行行为 `[X]`（如有 `[~]`，理由记录在 `.specify/specs/068-exec-quant-feedback-channel/verification.md` 的 `deferred_tasks=`）。
- DoD-2: 三腿按契约交付：`scripts/python/feedback-utils.py` 的 package 载荷扩展（C-1…C-9）与新动作 `ingest-exec-quant`（C-10…C-17），`scripts/python/exec-quant.py` 新动作 `aggregate`（C-18…C-23）；既有引擎动作语义零变化（C-26）。
- DoD-3: contracts/ 的 31 条规范条款（package-layout C-1…C-9、intake-contract C-10…C-17、aggregate-contract C-18…C-23、compatibility-security C-24…C-31）每条恰有一个任务行 `[green:]` 认领，且 `account-clause-coverage.py` 报告 claimed=31。
- DoD-4: 新增测试全绿（3 支契约 + 2 支单元 + 1 支集成 + 1 支边界兼容，见各 Phase 测试行）；FR-018/SC-006 名字级比对相对 `test-evidence/log-baseline-pre-impl.txt`（3 failed / 544 passed，24 文件定向集）零 NEW failing nodeid；E2 全量基线 `baseline-failed.txt` 的 closure 比对在 review/closure 槽执行（§ Test Budget）。
- DoD-5: plan.md § Mirror Obligations 表逐行落地：先源后镜像（`sync-mirrors.py --write` / `regen-command-copies.py`），相对 T001 既有漂移基线零 NEW drift，零手改镜像；既有基线内 DIFF 随同步消失不算回归。
- DoD-6: `.specify/specs/068-exec-quant-feedback-channel/verification.md` 以 `- **SC-001**:` … `- **SC-006**:` 列出六条成功标准的状态、命令、输出与证据指针。
- DoD-7: 边界零违例：打包产物、聚合层、汇总产物凭据型值扫描零命中；三腿零网络、零自动传输；exec-quant 记录零条混入 feedback store；零新增阻断式确认门。

**DoD Status**: pending

## Completion Gate

- GATE-1: 任务文件结构合法 — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/068-exec-quant-feedback-channel/tasks.md` exit 0。
- GATE-2: 跨产物一致 — check: `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/068-exec-quant-feedback-channel --stage tasks --repo .` 输出含 `decision=pass` 且 errors=0。
- GATE-3: 分解规模合法 — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/068-exec-quant-feedback-channel/requirements.md --tasks .specify/specs/068-exec-quant-feedback-channel/tasks.md` 结论为 proceed。
- GATE-4: FR-018/SC-006 定向零回归 — check: `bash scripts/bash/run-tests.sh` 按快速启动场景 4 的 24 文件集重跑，失败 nodeid 排序后与 `test-evidence/log-baseline-pre-impl.txt` 的名单 `comm -13` 逐名比对零新增（名字级，非计数级）。
- GATE-5: 镜像零 NEW drift — check: `python3 scripts/python/sync-mirrors.py --check` 相对 T001 记录的既有基线零 NEW DIFF，且 plan.md § Mirror Obligations 各对 `cmp` 逐对一致。
- GATE-6: 无未完成任务 — check: `grep -cE '^- \[[ >]\]' .specify/specs/068-exec-quant-feedback-channel/tasks.md` 返回 0。
- GATE-7: 条款覆盖完整 — check: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/068-exec-quant-feedback-channel` exit 0，输出 claimed clauses 31 / FR uncovered 0 / uncovered beyond baseline 0。
- GATE-8: SC 证据齐备 — check: `grep -cE '^- \*\*SC-00[1-6]\*\*' .specify/specs/068-exec-quant-feedback-channel/verification.md` 返回 6。
- GATE-9: 测试预算账本合规 — check: `python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine $SPINE --spec-dir .specify/specs/068-exec-quant-feedback-channel --stage-check implement`；implement 期判据 = 输出 `slots=baseline:1 closure:0` 且唯一 error 为 `review: stage evidence file missing`（review 证据由 review 阶段落盘，属预期未来阶段）；最终 closure 审计在 review 后以 `--stage-check closure` 要求 exit 0。

## Environment Prerequisites

- Python 3 + pytest: **available** — probe: `python3 --version` → `Python 3.11.11`；`python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-22; affected: T003、T004、T005、T009、T010、T011、T015、T016、T019、T020、T022、T023、T024 及全部 GATE 测试命令。
- 外部环境（容器/镜像仓库/集群/网络）: **none** — 三腿为纯本地文件操作、零网络（C-24/FR-016）；全部检查为本地文件、`git` 与本地 pytest @ 2026-10-22; affected: none。
- 镜像漂移既有基线: **pre-existing DIFF（判据 = 相对该基线零 NEW drift）** — probe: `python3 scripts/python/sync-mirrors.py --check` @ 2026-10-22: `scripts` 对含 `.specify/scripts/python/feedback-utils.py` 1 行既有 DIFF（镜像侧 f265cfbd 的 docstring 路径前缀更新，plan.md 已更正记录）；`skills/internal` 对含 manage-feedback 3 文件既有 DIFF；`shared` 对含 `feedback-step.md` 既有 DIFF；`templates` 对 clean（`ok … 22 files`）；`scripts` 对的 `exec-quant.py` 零 DIFF。逐对完整名单由 T001 落盘 `notes/pre-change-measurements.md`，其余行只引用该落点（见 § Environment Prerequisites 单一落点规则）。
- 样例客户项目存储（只读参考）: **available** — probe: `ls /storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant/records/ | wc -l` → `7`（schema v2）、`scores/` 空目录 @ 2026-10-22; affected: US1/US2 测试的双形态夹具设计参照；测试一律用自构夹具，不读写该真实存储。

## Test Budget (E2 / E3 / closure)

- **E2 baseline 槽（implement 起点，恰好一次）**: 进入任何实现编辑之前，用 canonical runner 全量跑一次并把失败名单落 `<spec-dir>/baseline-failed.txt`（形态 = owner `.specify/skills/internal/implement-feature/SKILL.md` § Test runs 的 `--names-out` 形式）；由 T003 执行并在状态脊 test-budget 账本记 `slot=baseline`。环境性失败（如 `No module named pytest`）判 probe failure、不消耗槽位、不记空基线。除 closure 后的 in-slot rerun 外，implement 期间零第二次全量。
- **E3 stage-status（阶段定向证据）**: 中间阶段的定向跑（targeted-set-v1）以 stage-status 行落 `test-evidence/*.jsonl`（本阶段 tasks 已落 docs-only 记录 `test-evidence/tasks.jsonl`；implement 期间由 T009 / T015 / T020 追加定向行）；`test-evidence/` 永远不是账本源。
- **closure 槽（review 后）**: 全量重跑 + 失败名单与 `baseline-failed.txt` 的 `comm -13` 名字级比较 + `python3 skills/external/sdd-loop-driver/scripts/audit-test-budget.py --spine $SPINE --spec-dir .specify/specs/068-exec-quant-feedback-channel --stage-check closure`；该槽属 review/closure 阶段，implement MUST NOT 预先消耗。
- **plan 冻结定向基线 ≠ E2**: `test-evidence/log-baseline-pre-impl.txt`（3 failed / 544 passed，24 文件 feedback/exec-quant 定向集，2026-10-22 冻结）只服务 FR-018/SC-006 的名字级比对（T023、GATE-4），不是全量 E2 基线。

## Mirror Obligations（落点）

真源 = plan.md § Mirror Obligations 表（逐文件权威清单）+ `scripts/python/sync-mirrors.py MIRROR_PAIRS`；本节只落任务行、不复述表。同步顺序 = 先框架源后镜像（C-31）：`sync-mirrors.py --write` 后以 `--check` 对照 T001 基线核零 NEW drift；`templates/commands/feedback.md` 走 `regen-command-copies.py` 逐工具副本再生成后逐副本 diff 含改动。落点行：T014（scripts 对，feedback-utils.py 两腿编辑收口）、T021（scripts 对，exec-quant.py）、T027（skills/internal 对 + shared 对 + 逐工具副本）。禁止手改 `.specify/` 镜像与逐工具副本。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 可与同阶段其它 `[P]` 行并行（写目标不同、无未完成依赖）。
- **[Story]**: 用户故事标签（`[US1]`…`[US4]`），仅用户故事阶段的任务行携带。
- **[blockedBy: T001,T002]**: 显式依赖标签；被列任务全部 `[X]` 前不得开始本行；仅有阶段顺序关系时省略。
- **[green: <contract>#<clause>]**: 绿点认领——本行是使该契约条款转绿的那一行；契约路径相对本文件目录解析（`contracts/<file>.md#C-<n>`）。31 条款分区：package-layout C-1/C-2→T006、C-3…C-7→T007、C-8/C-9→T008；intake C-10…C-12→T012、C-13…C-17→T013；aggregate C-18…C-20→T017、C-21…C-23→T018；compatibility-security C-24/C-25→T022、C-26→T023、C-27…C-30→T024、C-31→T027。每条恰一行认领，`validate-tasks.py` 四项 green 检查 + `account-clause-coverage.py` 核对。
- 每行必须单行完成（含文件路径），不得换行续写。

### Task State Sigil (REQUIRED)

- `- [ ]` — Open；`- [>]` — Claimed（多代理运行用）；`- [X]` — Closed；`- [~]` — Deferred（理由记录在 `verification.md` 的 `deferred_tasks=`）。

## Path Conventions

- **Framework source（编辑面）**: `scripts/python/feedback-utils.py`、`scripts/python/exec-quant.py`、`skills/internal/manage-feedback/`（SKILL.md + references/）、`templates/commands/feedback.md`、`shared/workflow/feedback-step.md`、`docs/reference/commands/feedback.md`、`docs/reference/skills/feedback.md`、`tests/contract/`、`tests/unit/`、`tests/integration/`。
- **Generated mirrors（生成面，禁止手改）**: `.specify/scripts/python/`、`.specify/skills/internal/manage-feedback/`、`.specify/shared/workflow/feedback-step.md`、逐工具命令副本（`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/`、Codex 对应副本）——只由 `sync-mirrors.py --write` / `regen-command-copies.py` 再生成。
- **Runtime derived store（运行时派生层）**: `.specify/memory/exec-quant/aggregated/`（接收信封 `aggregated/<source-slug>/records/` + 汇总 `aggregated/summaries/`）；按本仓 records/ 惯例随 git 跟踪，但 implement 的提交以显式路径只含特性产物，运行时记录按派发约束不入本特性提交。
- **Read-only isolation（禁改面）**: `feedback/feedback-20261022T062525Z.zip`（真实入站基线包，禁提交/禁改/禁删）、`.specify/memory/exec-quant/records/` 与 `.specify/memory/feedback/` 下的运行时记录（禁提交/禁改/禁删）、`.specify/specs/059-exec-quant-recording/`（059 制品零改写）、`/storage/project/cloud-native-tools/cws-lib-python/.specify/memory/exec-quant`（客户样例，只读参考）。
- **Evidence（本特性证据落点）**: `.specify/specs/068-exec-quant-feedback-channel/` 下的 `notes/`、`verification.md`、`coverage-baseline.txt`、`baseline-failed.txt`、`test-evidence/`。

## Measured Premises (re-measured at generation time 2026-10-22)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| 契约条款数（逐文件） | `python3 .specify/scripts/python/clause_extract.py .specify/specs/068-exec-quant-feedback-channel/contracts/<f>.md` 逐文件计数 | package-layout 9（C-1…C-9）、intake-contract 8（C-10…C-17）、aggregate-contract 6（C-18…C-23）、compatibility-security 8（C-24…C-31）；合计 31，全部 md-bold-closed 形态 |
| FR / SC 计数 | `grep -cE '^\- \*\*FR-[0-9]+\*\*' requirements.md`；`grep -cE '^\- \*\*SC-[0-9]+\*\*' requirements.md` | 19 / 6 |
| 打包腿锚点符号 | `grep -n 'def write_package\|def action_package\|_ACTIONS =\|No feedback entries to package' scripts/python/feedback-utils.py` | `write_package` :1098、早退 `"No feedback entries to package."` :1116、`action_package` :1201、`_ACTIONS` :1645（12 动作，无 intake 类） |
| 汇总腿锚点符号 | `grep -n '^ACTIONS\|def write_entry\|def read_entry_files\|def append_record_locked\|RECORD_SIZE_CAP_BYTES =\|def entry_filename\|def normalize_record_view' scripts/python/exec-quant.py` | `ACTIONS` :45（collect / list-records / score / collect-dispatch / args-manifest）、`RECORD_SIZE_CAP_BYTES` :89、`entry_filename` :215、`write_entry` :220、`read_entry_files` :238、`append_record_locked` :895、`normalize_record_view` :929 |
| pytest 解释器 | `python3 -m pytest --version` | `pytest 8.4.2`（无 `.venv/`；`SPECKIT_PYTHON` 无需设置） |
| 镜像既有漂移 | `python3 scripts/python/sync-mirrors.py --check` 逐对 | 见 § Environment Prerequisites（feedback-utils 镜像 1 行既有 DIFF / manage-feedback 3 文件 / feedback-step.md；templates 对与 exec-quant 对 clean） |
| 共享字符串锚点 | requirements.md § Shared Strings | `[[STR-001]]` = "speckit.exec-quant"、`[[STR-002]]` = "not_evaluated"（沿用 059/运行判定既有锚点，本特性零新造词表） |

`missing-path` 类 advisory 在实现前属预期（新增测试文件与 `aggregated/` 尚不存在）；`error` 必须为 0。

## Requirement Coverage Map

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T004、T005、T006、T007 |
| FR-002 | T004、T005、T006 |
| FR-003 | T004、T005、T007 |
| FR-004 | T005、T007 |
| FR-005 | T004、T005、T006、T007、T008 |
| FR-006 | T010、T011、T012 |
| FR-007 | T011、T013、T024 |
| FR-008 | T010、T011、T013、T019 |
| FR-009 | T011、T012、T019、T024 |
| FR-010 | T011、T013 |
| FR-011 | T016、T017、T020 |
| FR-012 | T011、T013、T017、T018 |
| FR-013 | T016、T018 |
| FR-014 | T016、T018、T022 |
| FR-015 | T022 |
| FR-016 | T022 |
| FR-017 | T023 |
| FR-018 | T003、T023 |
| FR-019 | T005、T008 |
| SC-001 | T005、T006、T007、T028 |
| SC-002 | T004、T005、T006、T028 |
| SC-003 | T011、T013、T019、T028 |
| SC-004 | T016、T017、T018、T020、T028 |
| SC-005 | T022、T023、T029 |
| SC-006 | T003、T023、T029、T030 |

T001（镜像/改前基线）、T002（覆盖基线冻结）、T014/T021/T027（镜像同步）、T025/T026（文档面）、T030（审计收口）是流程与镜像义务任务，按设计不直接映射 FR/SC。`[[STR-001]]`/`[[STR-002]]` 引用一律按 requirements.md § Shared Strings 解析，测试不得内联字面值（Pin Hygiene：字面值漂移时只改共享串行）。

**Task Distribution**: Setup 3 · 打包腿 6 · 接收腿 6 · 汇总腿 6 · 边界腿 3 · Polish 6 · 任务行合计 30。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 冻结改前基线（镜像漂移 / 条款覆盖 / E2 全量失败名单），让后续每个「相对基线零 NEW」判据都有日期化依据；`notes/` 目录就位供红先取证。

- [X] T001 捕获改前基线到 `.specify/specs/068-exec-quant-feedback-channel/notes/pre-change-measurements.md`：`python3 scripts/python/sync-mirrors.py --check` 的逐对既有 drift 名单（判据 = 相对该基线零 NEW drift，既有 DIFF 一律不归因本特性；基线概览单一落点见 § Environment Prerequisites，本行落盘逐对完整名单与捕获日期）、`git status --short` 与 `git rev-parse HEAD` 快照（覆盖 § Path Conventions 的编辑面与禁改面），并创建 `notes/` 目录供后续红先取证行写入。
- [X] T002 [P] 冻结契约覆盖基线：在仓库根运行 `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/068-exec-quant-feedback-channel --freeze > .specify/specs/068-exec-quant-feedback-channel/coverage-baseline.txt`（脚本只打印、不写文件），核对输出首行含 `frozen-from:` 且明示 excluding 068 自身、记录 `base-sha`；该文件留作后续覆盖核对的冻结侧。
- [X] T003 [P] 执行 E2 全量基线（implement 起点，恰好一次，§ Test Budget）：`bash scripts/bash/run-tests.sh --names-out .specify/specs/068-exec-quant-feedback-channel/baseline-failed.txt`（无其他过滤参数 = 全量；owner = `.specify/skills/internal/implement-feature/SKILL.md` § Test runs，失败名单比较形式以 owner 为准，本行只落命令与路径），在状态脊 test-budget 账本记 `slot=baseline` 行（命令、耗时、失败名单行数、日期）；MUST 先于任何实现编辑；`No module named pytest` 判 probe failure 不消耗槽位、不记空基线（§ Environment Prerequisites）。

**Checkpoint**: 三份基线落盘（镜像漂移 / 覆盖 / E2 失败名单）；全部「零 NEW」判据有冻结对照物。

---

## Phase 2: User Story 1 - 客户项目打包时量化数据随包收回 (Priority: P1) 🎯 MVP

**Goal**: `/speckit.feedback package` 产物 zip 含 exec-quant 一等载荷（全量包含 + 显式封顶 + 只读源存储），包级源项目身份、payload-manifest 与 MANIFEST 人读段同源声明，输出报告知情，feedback 条目为空时载荷独立成包（FR-019）。

**Independent Test**: 在含 exec-quant 记录的自构夹具项目里执行打包流程，核对 zip 内容、payload-manifest/MANIFEST 声明、源存储零改动与 FR-019 双向行为；独立于接收/汇总腿即可交付价值（数据已可被收回）。

> **本特性无 Foundational 阶段**：三腿互不阻塞——打包腿与接收腿各自扩展 `feedback-utils.py` 的不同动作面（先 US1 后 US2 串行落同一文件），汇总腿只读聚合层、可对夹具信封开发（US3 集成测试行对 US2 有显式 blockedBy），故按模板规则整段省略并顺延编号。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [X] T004 [US1] 红先编写单元测试到 `tests/unit/test_feedback_exec_quant_payload.py`：载荷采集语义（`records/*.json` 与遗留 `records.jsonl` 双形态并存全量纳入、`kind == [[STR-001]]` 过滤、不可解析条目计入 `skipped_unreadable`、遗留条目名 `legacy-records-L%04d.json` 行号自 1 起、`source_form_counts` 双计数）、排序键 `(collected_at 升序, 源文件名升序)` 确定性跨机可复现、封顶模块常量（1000 条 / 16 MiB）与触顶截断计数、包级身份解析（`**Project Name**:` 行 → 目录基名回退 → `identity_status: "unknown-project"`；`git rev-parse HEAD` 失败置 null 不重试）；夹具全部自构（§ Environment Prerequisites 的样例客户存储只读参考，不进测试）。运行红跑并把命令、真实输出、退出码、用例清单写入 `notes/red-first-evidence.md`。
- [X] T005 [US1] 红先编写契约测试到 `tests/contract/test_feedback_exec_quant_payload.py`：zip 内布局 `exec-quant/payload-manifest.json` + `exec-quant/records/*.json` 且载荷仅存在于该目录（记录源字节 verbatim、零重排零重编码零过滤字段）；payload-manifest 字段集与 data-model § E4 一致（`record_count == len(records/)`、`cap_records`/`cap_bytes`、`source_form_counts`、`skipped_unreadable`、`truncated_count`、`identity`、`collected_at_range`）；MANIFEST.md § Exec-Quant Payload 人读段与机器段同源渲染（空载荷段存在并声明「无量化数据」）；`--action package` 输出 text 与 `--format json` 双面可见载荷条数与降级计数；FR-019 双向（feedback 空 + 载荷 ≥1 → 仍产包且 `Entries: 0` 显式；双空 → 不产包且显式说明）；源存储只读断言（打包前后 exec-quant 存储与 feedback store 逐文件清点零差异）；`kind: external` 排除 / 时间过滤 / `--all` / `--include-introspection` 语义零变化；一切载荷降级 exit 0 非阻塞。运行红跑并写入 `notes/red-first-evidence.md`。

### Implementation for User Story 1

- [X] T006 [US1] 在 `scripts/python/feedback-utils.py` 实现载荷采集（package 流程扩展第一步）：扫描 `<workspace>/.specify/memory/exec-quant/` 的 `records/*.json` 与遗留 `records.jsonl`（两类并存全量纳入，扫描窗口 = 动作发起时刻快照）、`json.loads` 为 object 且 `kind == [[STR-001]]` 过滤、不可解析计入 `skipped_unreadable`、遗留流条目名 `legacy-records-L%04d.json`（行号自 1 起）并计入 `source_form_counts.records-dir`/`.legacy-jsonl`、排序键 `(collected_at 升序, 源文件名升序)`、模块常量 `MAX_PAYLOAD_RECORDS = 1000` 与 `MAX_PAYLOAD_BYTES = 16 MiB`（封顶值唯一规范落点 = contracts C-2，实现只落常量零第二定义）、触顶截断余量计入 `truncated_count`；源存储零改动零移动零删除（只读扫描）。 [blockedBy: T004,T005] [green: contracts/package-layout.md#C-1] [green: contracts/package-layout.md#C-2]
- [X] T007 [US1] 在 `scripts/python/feedback-utils.py` 实现包级身份与载荷落盘：`project_name` 读 `.specify/instructions.md` 的 `**Project Name**:` 行、失败回退 workspace 目录基名、再失败置空且 `identity_status: "unknown-project"`，`source_commit` 取 `git rev-parse HEAD`（失败置 null、不重试不阻塞，零绝对路径身份载体零新增凭据面）；zip 写入 `exec-quant/payload-manifest.json`（E4 字段全集）与 `exec-quant/records/<name>.json`（源文件字节原样拷贝）；MANIFEST.md § Exec-Quant Payload 人读段与 payload-manifest.json 由同一渲染函数产出（内容同源，空载荷段照写并声明「无量化数据」）；`--action package` 输出 text 与 `--format json` 双面报告载荷条数与降级计数。 [blockedBy: T006] [green: contracts/package-layout.md#C-3] [green: contracts/package-layout.md#C-4] [green: contracts/package-layout.md#C-5] [green: contracts/package-layout.md#C-6] [green: contracts/package-layout.md#C-7]
- [X] T008 [US1] 在 `scripts/python/feedback-utils.py` 修订 `write_package`/`action_package` 空条目早退（FR-019）：早退条件由「feedback 条目为空」改为「feedback 条目与载荷记录双空」（返回措辞覆盖两类数据），feedback 空 + 载荷 ≥1 照常产包且 `Entries: 0` 显式入 MANIFEST，双空不产包且输出显式说明；`kind: external` 排除、时间过滤、`--all`、`--include-introspection` 语义零变化；确认载荷采集一切降级（空存储/目录缺失、部分不可解析、截断、身份缺失）不使打包失败且打包腿零网络操作。 [blockedBy: T007] [green: contracts/package-layout.md#C-8] [green: contracts/package-layout.md#C-9]
- [X] T009 [US1] 打包腿定向转绿与取证：用 canonical runner 运行 `tests/unit/test_feedback_exec_quant_payload.py` 与 `tests/contract/test_feedback_exec_quant_payload.py` 至全绿，把绿证据（命令、输出摘要、退出码）追加到 `notes/red-first-evidence.md`，并向 `.specify/specs/068-exec-quant-feedback-channel/test-evidence/implement-stage-status.jsonl` 追加一行 targeted-set-v1 stage-status（selection_basis 注明本段 diff 仅打包腿测试与实现路径）；独立可用性核验 = 快速启动场景 1/4 对应断言全绿（US1 验收场景 1–4 的测试等价物）。 [blockedBy: T008]

**Checkpoint**: 打包腿独立可验收：夹具项目打包产出合法载荷包、MANIFEST/报告知情、源存储零改动、FR-019 双向成立；MVP 前半就位。

---

## Phase 3: User Story 2 - spec-kit 接收包并解出量化数据 (Priority: P1) 🎯 MVP

**Goal**: 既有入站包路径承接的引擎动作 `ingest-exec-quant --package <zip>` 把包内 `exec-quant/` 载荷解出到聚合层 `aggregated/<source-slug>/records/`、按包级身份归因、identity_key 幂等去重（flock 临界区）、损坏/无载荷显式降级非阻塞；feedback 面零触碰、零混入 feedback store、接收不自动汇总。

**Independent Test**: 用自构含载荷包执行接收动作，核对聚合层新增信封逐条归因、feedback store 零混入、同包二次接收零重复；再对无载荷等构包执行，核对零计数零写入 exit 0、行为与 068 之前零差异。

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [X] T010 [US2] 红先编写单元测试到 `tests/unit/test_feedback_intake_exec_quant.py`：identity_key 计算（五元组 `source_project ␟ unit_id ␟ unit_type ␟ run_id ␟ collected_at` 以 `\x1f` 连接并 sha256，64-hex 输出确定性；content_hash 为独立 canonical JSON sha256，不拼入 identity_key）、canonical JSON 序列化（sort_keys + ensure_ascii=False + 紧凑分隔符）、source-slug 生成（项目名 slug 化 `[a-z0-9-]` + 身份串短哈希 8 位；空身份 → 字面 `unknown-project` 确定性）、信封字段集与 data-model § E6 一致（`aggregation_envelope.*` + `record` verbatim 封存、未知字段零丢弃）；夹具自构。运行红跑并写入 `notes/red-first-evidence.md`。
- [X] T011 [US2] 红先编写契约测试到 `tests/contract/test_feedback_intake_exec_quant.py`：动作签名 `--action ingest-exec-quant --package <zip>`（必选）+ 既有 `--workspace-root` 旗标；载荷识别 = zip 成员路径前缀 `exec-quant/`，无前缀 → `record_count: 0`、exit 0、零存储写入零目录创建（无载荷既有包零差异，快速启动场景 5）；payload-manifest 不可读/缺失 → 成员仍逐条尝试 + `manifest_unreadable` 降级；身份缺失/`identity_status == "unknown-project"` → 落字面 `unknown-project` 组、不从路径或内容猜测；单条不可解析或 `kind != [[STR-001]]` → `skipped_unreadable` 非阻塞；同包二次接收 `ingested: 0` + `duplicates_skipped` 全量（幂等）；同 key 异 content_hash → keep-first + `identity_conflicts`；去重检查 + 写入在同一 flock 临界区（锁文件 `aggregated/.write.lock`，两流程并写零冲突）；信封 tmp+rename 原子写、文件名沿用 `entry_filename()` 形态与源名解耦；输出 JSON 键集（`record_count`/`ingested`/`duplicates_skipped`/`skipped_unreadable`/`identity_conflicts`/`groups_touched`/`manifest_unreadable`）与退出码（降级 exit 0；`--package` 缺失/非 zip/存储不可写 exit 2）；exec-quant 记录零条混入 `.specify/memory/feedback/`、feedback 条目/introspection/SUBMISSION-NOTES 零触碰；接收不触发 aggregate（`aggregated/summaries/` 零新增）。运行红跑并写入 `notes/red-first-evidence.md`。

### Implementation for User Story 2

- [X] T012 [US2] 在 `scripts/python/feedback-utils.py` 实现动作 `ingest-exec-quant` 骨架（注册 + 识别 + 归因）：注册进 `_ACTIONS`（feedback 面既有动作语义零变化）、`--package` 必选参数；按成员路径前缀 `exec-quant/` 识别载荷，无前缀返回零计数 exit 0；读 `payload-manifest.json`（不可读/缺失 → `manifest_unreadable` 且成员逐条尝试）；逐条 `json.loads` + `kind` 过滤 + `skipped_unreadable`；identity 取 manifest（缺失/unknown-project → 字面 `unknown-project` 分组，零猜测）；source-slug 生成与 `aggregated/<source-slug>/records/` 分组目录。 [blockedBy: T010,T011] [green: contracts/intake-contract.md#C-10] [green: contracts/intake-contract.md#C-11] [green: contracts/intake-contract.md#C-12]
- [X] T013 [US2] 在 `scripts/python/feedback-utils.py` 实现幂等写入路径：identity_key（T010 的五元组哈希，不含 content_hash）+ 独立 content_hash 比较 + 去重窗口（全聚合层既有信封 identity_key 集合）+ 同 key 异 hash keep-first + `identity_conflicts` 计数；去重检查与写入在单一 flock 临界区（沿用 `append_record_locked` 形态，锁文件 `aggregated/.write.lock`，tmp+rename 原子写）；信封按 data-model § E6 落盘（`record` 键封入源记录 verbatim、未知字段零丢弃、不改写不补齐）；`duplicates_skipped`/`ingested`/`groups_touched` 计数与退出码阶梯（降级 exit 0、整体不可执行 exit 2，与既有 `FeedbackError` 形态一致）；feedback store 零写入零判定；动作零触发 aggregate。 [blockedBy: T012] [green: contracts/intake-contract.md#C-13] [green: contracts/intake-contract.md#C-14] [green: contracts/intake-contract.md#C-15] [green: contracts/intake-contract.md#C-16] [green: contracts/intake-contract.md#C-17]
- [X] T014 [P] [US2] scripts 对镜像同步（feedback-utils.py 编辑收口点，§ Mirror Obligations）：`python3 scripts/python/sync-mirrors.py --write --only scripts` 后 `--check` 复查，`.specify/scripts/python/feedback-utils.py` 相对 T001 基线零 NEW drift（该对 1 行既有 DIFF 随字节同步消失属预期，不算回归；判据单一落点 = § Environment Prerequisites），并用 `cmp` 核对源/镜像字节一致；零手改镜像。 [blockedBy: T013]
- [X] T015 [P] [US2] 接收腿定向转绿与取证：用 canonical runner 运行 `tests/unit/test_feedback_intake_exec_quant.py` 与 `tests/contract/test_feedback_intake_exec_quant.py` 至全绿，绿证据追加 `notes/red-first-evidence.md`，并向 `test-evidence/implement-stage-status.jsonl` 追加 targeted-set-v1 stage-status 行（selection_basis 注明本段 diff 仅接收腿测试与实现路径）；独立可用性核验 = 快速启动场景 2/5 对应断言全绿。 [blockedBy: T013]

**Checkpoint**: 接收腿独立可验收：含载荷包解出归因幂等、无载荷包零差异、feedback 面零触碰；MVP（打包 + 接收）闭环就位，可独立演示「收回 → 解出」。

---

## Phase 4: User Story 3 - 跨项目量化汇总可在本地查看 (Priority: P2)

**Goal**: `exec-quant.py` 新显式动作 `aggregate` 只读聚合层，产出按源项目/单元维度的机器可读聚合视图（计数、质量量分布、未测覆盖率、`record_files` 可对账名单），stdout JSON 与 `aggregated/summaries/<id>.json` 不可变产物同构，零臆造、零网络、仅本地。

**Independent Test**: 构造含 ≥2 源项目的聚合层夹具后执行汇总动作，核对视图逐项可由 `record_files` 名单重放对账、未测字段显式计数、产物落盘形态与可重建性（重跑新文件数字一致）；独立于打包腿（夹具直供聚合层）。

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: 先写这些测试并确认其失败，再进入实现。**

- [X] T016 [P] [US3] 红先编写契约测试到 `tests/contract/test_exec_quant_aggregate.py`：动作注册（`ACTIONS` 元组追加 `aggregate` + ARG_MANIFEST 覆盖新旗标，`--action args-manifest` 契约自动生效）；消费面 = `aggregated/**/records/*.json` 信封且 MUST NOT 读本地 `records/`/`scores/`（负例：本地记录不进视图）；信封不可读（非 dict/缺 `record` 键）→ `skipped_unreadable` 非阻塞；本仓自身作为源项目与其他源同权呈现（分组零特判）；视图口径（`sources[]` 的 `record_count`/`units`/`quality{field: {evaluated, not_evaluated}}`/`coverage`/`record_files[]` + `totals` + `store_digest{record_files_total, identity_keys_total}`）；形态归一（`{value, provenance}` → evaluated、裸 `[[STR-002]]` 或缺失键 → not_evaluated、未知新字段按 not_evaluated 零硬编码）；零臆造（任一数字可由 `record_files` 名单重放核对、产物零填补值零外推）；产物落盘 `aggregated/summaries/<summary-id>.json`（append-only、旧文件零改写、`generated_at` + `store_digest`）；stdout JSON 与落盘产物同构；重复执行安全（重跑新文件、数字一致）；接收动作零自动触发（负例断言）。运行红跑并写入 `notes/red-first-evidence.md`。

### Implementation for User Story 3

- [X] T017 [US3] 在 `scripts/python/exec-quant.py` 实现动作 `aggregate` 消费与视图：`ACTIONS` 元组追加 `aggregate` 并注册 ARG_MANIFEST（argparse parser 保持旗标唯一事实源，既有 `--action args-manifest` 契约自动覆盖；零新校验器）；参数 `--workspace-root` + `--format {text,json}`（缺省 json，与既有 `list-records` 形态一致）；用既有 `read_entry_files` 读 `aggregated/**/records/*.json` 信封、不可读计 `skipped_unreadable`；按信封 `source_project` 分组（本仓为零特判一员）投影 `sources[]`/`units`/`quality`/`coverage`/`record_files[]` 与 `totals`；字段形态归一遵循既有 `normalize_record_view` 先例（只影响视图，不写源）。 [blockedBy: T016] [green: contracts/aggregate-contract.md#C-18] [green: contracts/aggregate-contract.md#C-19] [green: contracts/aggregate-contract.md#C-20]
- [X] T018 [US3] 在 `scripts/python/exec-quant.py` 实现汇总产物与边界：stdout JSON 与落盘产物同构双出；`aggregated/summaries/<summary-id>.json` 用 `entry_filename()` 形态按条落盘、append-only 旧文件零改写、含 `generated_at` 与 `store_digest`（信封文件总数 / identity_key 总数，支撑重跑重建核对）；零臆造（未测/缺失以 `[[STR-002]]` 显式计数呈现，零填补零外推零杜撰基线，不评估不打分不判阈值）；显式动作边界（MUST NOT 随接收自动执行；零网络零外发、产物仅落本仓 `aggregated/`）。 [blockedBy: T017] [green: contracts/aggregate-contract.md#C-21] [green: contracts/aggregate-contract.md#C-22] [green: contracts/aggregate-contract.md#C-23]
- [X] T019 [US3] 红先编写端到端集成测试到 `tests/integration/test_feedback_exec_quant_channel.py`（red-first 范围 = 汇总链；接收/打包环节属回归网，按 create-tasks 迁移/回归例外带显式 blockedBy 落于实现后）：自构客户存储 → package（含双形态存储 + 混合字段形态夹具）→ 人工投递 → ingest-exec-quant → aggregate 全链（≥2 源项目，其中一组落 `unknown-project`）；同包双收幂等（聚合层条目增量为零）；`record_files` 名单重放对账逐数字核对；凭据零出现与零网络断言（本测试内对产物与聚合层跑凭据型变量名扫描、命中 0）；无载荷等构包全链零差异。运行红跑（汇总相关用例必须红）并写入 `notes/red-first-evidence.md`。 [blockedBy: T013]
- [ ] T020 [US3] 汇总腿定向转绿与取证：用 canonical runner 运行 `tests/contract/test_exec_quant_aggregate.py` 与 `tests/integration/test_feedback_exec_quant_channel.py` 至全绿，绿证据追加 `notes/red-first-evidence.md`，并向 `test-evidence/implement-stage-status.jsonl` 追加 targeted-set-v1 stage-status 行（selection_basis 注明含集成链）；独立可用性核验 = 快速启动场景 3 对应断言全绿。 [blockedBy: T018,T019]
- [ ] T021 [P] [US3] scripts 对镜像同步（exec-quant.py 编辑收口点，§ Mirror Obligations）：`python3 scripts/python/sync-mirrors.py --write --only scripts` 后 `--check` 复查该对相对 T001 基线零 NEW drift，`cmp` 源/镜像字节一致；零手改镜像。 [blockedBy: T018]

**Checkpoint**: 汇总腿独立可验收：聚合层夹具 → 显式汇总 → 机器可读视图 + 不可变产物，数字全部可对账；三腿功能面齐备。

---

## Phase 5: User Story 4 - 通道升级不破坏既有边界与行为 (Priority: P2)

**Goal**: 既有安全边界（凭据零出现、零自动传输、存储分界）与既有行为（两引擎既有动作、既有测试套件）零回归；兼容容忍（v1/v2、双布局、混合字段形态）与「零新增确认门」有守卫测试；文档与镜像同步顺序合规。

**Independent Test**: 对含载荷产物与聚合层跑凭据扫描（命中 0）；跑既有 feedback/exec-quant 契约与集成套件并与冻结基线逐名比对零新增；对无载荷等构包核对零差异。独立于前三条的可执行性（守卫断言落在已实现行为上）。

> **US4 是回归网（regression net）**：本阶段测试守护的是 US1–US3 落地后的行为面，按 create-tasks「迁移/回归例外」以显式 `[blockedBy:]` 落于实现之后，不适用红先于实现；各行的守卫用例清单仍先写全、先评审，再运行。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T022 [US4] 编写边界守卫契约测试到 `tests/contract/test_exec_quant_channel_boundary.py`（回归网形态，护栏对象 = 三腿已实现行为）：三腿零网络断言（引擎源零网络 import/调用面审查 + 运行面观察，零守护进程零常驻连接零定时器）；凭据零出现（对自构打包产物、聚合层目录、汇总产物分别执行凭据型变量名/形态扫描，命中计数 = 0）；零自动传输子句拆分保留（打包手动触发 / 接收本地解出 / 汇总显式动作，零外发路径）；059 采集遮蔽与封顶不削弱（载荷只携带已遮载数据，`RECORD_SIZE_CAP_BYTES` 等既有常量零改动）。运行并把结果（含红转绿状态）写入 `notes/red-first-evidence.md`。 [blockedBy: T008,T013,T018] [green: contracts/compatibility-security.md#C-24] [green: contracts/compatibility-security.md#C-25]
- [ ] T023 [US4] 既有套件名字级回归（FR-018/SC-006）：用 canonical runner 按快速启动场景 4 的 24 文件 feedback/exec-quant 定向集重跑，失败 nodeid 排序后与冻结基线 `test-evidence/log-baseline-pre-impl.txt` 逐名比对（名字级、非计数级；新增通过的用例不算回归，新增失败必须逐名归因解释，既有 3 个镜像一致性失败的消失不算回归）；两引擎既有动作面清单（feedback 12 动作 / exec-quant 5 动作 + 新增）零语义变化核对。结果写入 `notes/red-first-evidence.md` 与 `verification.md` §SC-006 预备段。 [blockedBy: T008,T013,T018] [green: contracts/compatibility-security.md#C-26]
- [ ] T024 [P] [US4] 编写兼容守卫契约测试到 `tests/contract/test_exec_quant_channel_compat.py`（回归网形态）：无载荷等构包接收零差异（零计数 exit 0 零写入，`feedback/feedback-20261022T062525Z.zip` 为只读参照、测试用自构等构包不触碰真实包）；feedback 空 + 载荷空 → package 与 068 前一致（不产包显式说明）；版本/布局/形态容忍（逐条目录与遗留流、schema v1/v2、`{value, provenance}` 与裸 `[[STR-002]]` 三类并存全链可打包可接收可汇总；未知新字段原样保留进聚合层零丢弃；遗留单体流只读永不重写）；零新增阻断式确认门（三腿动作不在确认门清单、退出开关只能是非阻断可选参数）；存储分界（聚合层只存在于 `exec-quant/aggregated/`、两 store 清点口径互不引用、exec-quant 记录零条混入 feedback store）。运行并把结果写入 `notes/red-first-evidence.md`。 [blockedBy: T008,T013,T018] [green: contracts/compatibility-security.md#C-27] [green: contracts/compatibility-security.md#C-28] [green: contracts/compatibility-security.md#C-29] [green: contracts/compatibility-security.md#C-30]

**Checkpoint**: 边界零违例可验收：凭据扫描 0 命中、既有套件名字级零新增失败、容忍面与存储分界有守卫测试。

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 流程面与参考文档同步、镜像与逐工具副本收口、快速启动实跑取证、SC 证据矩阵、范围审计与 Completion Gate 复验。

- [ ] T025 [P] 更新流程面文档（先源后镜像，§ Mirror Obligations）：`skills/internal/manage-feedback/SKILL.md` 与 `references/path-a-digest.md`（A2 对每个入站 bundle 执行一次 `ingest-exec-quant --package <zip>` 的调用点 + 降级计数知情 + 汇总列为建议的显式后续步骤、不并入接收流程）、`references/path-b-and-probe.md`（package 载荷面：全量包含/封顶/降级计数知情）、`shared/workflow/feedback-step.md`（载荷随包后 wrap-up 的观察面）、`templates/commands/feedback.md`（技能引用行同步）；零新增命令、零新增确认门，059 制品零触碰。
- [ ] T026 更新参考文档：`docs/reference/commands/feedback.md`（三腿行为 + 引擎动作名 `ingest-exec-quant` / `aggregate` + 退出码与降级计数语义）、`docs/reference/skills/feedback.md`（Path A 载荷步骤）；文档取值与引擎 `--help`/动作面一致，引擎动作名以代码 `_ACTIONS`/`ACTIONS` 为准（代码先于文档）。 [blockedBy: T025]
- [ ] T027 镜像与逐工具副本收口（§ Mirror Obligations；本行只写镜像面，T025 已编辑的源只读 `shared/workflow/feedback-step.md` 与源只读 `templates/commands/feedback.md` 不在本行改写）：`python3 scripts/python/sync-mirrors.py --write --only skills/internal` 与 `--only shared` 后 `--check` 复查两对相对 T001 基线零 NEW drift；`python3 scripts/python/regen-command-copies.py` 再生成逐工具副本并 diff 逐副本含改动（`.specify/templates/commands/` 已退役、无该镜像）；镜像对 `.specify/shared/workflow/feedback-step.md` 同步后既有失败测试 `test_feedback_step_reference_form.py::test_owner_mirror_is_byte_identical` 预期转绿（基线失败消失不算回归）；全程零手改镜像与副本。 [blockedBy: T025] [green: contracts/compatibility-security.md#C-31]
- [ ] T028 快速启动实跑取证：执行 `quickstart.md` 可执行场景并留痕 `notes/quickstart-run.md`（真实命令、输出、退出码、teardown）：场景 0（route a 存储形态探测，含样例客户项目只读 `ls`）；场景 1–3/5 以测试已钉断言为核验形态（route b——在自构夹具上复跑 `package` / `ingest-exec-quant` / `aggregate` 命令行本身，记录 `--format json` 输出与 `aggregated/` 落盘清单；不触碰真实入站包与客户存储写面）；场景 4 由 T023 的定向重跑代表（引用其证据行，不重复执行）。 [blockedBy: T020,T027]
- [ ] T029 写 SC 证据矩阵到 `verification.md`：`- **SC-001**:` 至 `- **SC-006**:` 逐条列状态、命令、输出摘要与证据指针（SC-001/002 ← T005–T007+T028；SC-003 ← T011/T013/T019；SC-004 ← T016–T020；SC-005 ← T022；SC-006 ← T003 基线 + T023 比对 + closure 槽）；未测量量显式记 not-evaluated，零手填。 [blockedBy: T023,T028]
- [ ] T030 范围审计与 Completion Gate 复验（结果写 `verification.md` §T030）：`git status --short` 核对禁改面零命中（真实入站包、`.specify/memory/exec-quant/records/` 与 `.specify/memory/feedback/` 运行时记录、059 制品、镜像手改）；逐项复验 GATE-1…GATE-8（GATE-9 以 `--stage-check implement` 执行：baseline:1/closure:0 且唯一 error 为 review 证据缺失属预期；closure 审计在 review 后以 `--stage-check closure` 要求 exit 0）；`account-clause-coverage.py` 核对 claimed=31 且 FR 19/19、SC 6/6 有任务行映射；Feature 068 保持 `Planned`（生命周期推进属 implement 阶段，本阶段不写注册表）。 [blockedBy: T029]

**Checkpoint**: 文档/镜像/证据/审计全部收口；除 closure 槽外所有 GATE 可就地复验通过。

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: 无依赖，立即开始；T003（E2 全量基线）必须先于任何实现编辑（§ Test Budget 恰好一次纪律）。
- **打包腿 (Phase 2)**: 依赖 Setup；`feedback-utils.py` 的第一段编辑。
- **接收腿 (Phase 3)**: 依赖打包腿完成（同文件 `feedback-utils.py` 串行编辑，避免同文件并行写）；T014 镜像同步是 `feedback-utils.py` 的编辑收口点。
- **汇总腿 (Phase 4)**: T016–T018 只写 `exec-quant.py`、只依赖 T016；T019 集成测试依赖 T013（复用已实现的接收动作做全链）；T020/T021 收口。
- **边界腿 (Phase 5)**: 全部行依赖三腿实现（T008, T013, T018）——回归网形态（例外依据见阶段头注）。
- **Polish (Phase 6)**: T025 依赖全部功能与守卫测试就位；T026←T025；T027←T025（镜像同步在源编辑全部落地后）；T028←T020,T027（快速启动命令走 `.specify/` 镜像路径，须在镜像同步后实跑）；T029←T023,T028；T030←T029。

### User Story Dependencies

- **打包腿 (P1)**: 不依赖其他故事；独立测试 = 自构夹具打包 + zip/MANIFEST/源存储核对。
- **接收腿 (P1)**: 与打包腿构成 MVP；其测试用自构等构包，不依赖打包腿运行时（仅共享引擎文件，串行编辑）。
- **汇总腿 (P2)**: 功能实现独立（只写 `exec-quant.py`、对夹具信封开发）；端到端链路依赖接收腿。
- **边界腿 (P2)**: 守护三腿行为，结论独立于任何单腿的功能断言。

### Within Each User Story

- 测试（红先）→ 实现 → 定向转绿 + 取证；同文件实现行按编号顺序执行，不得并行。
- 红先测试行共享同一个 append-only 证据汇 `notes/red-first-evidence.md`：同故事内按 T004 → T005、T010 → T011 顺序执行，不并行（这也是这四行不标 `[P]` 的原因）；取证行 T015 与镜像同步行 T014 写目标互不相同，可并行。
- 三腿实现共两份引擎文件：`feedback-utils.py` 由 T006 → T007 → T008 → T012 → T013 串行；`exec-quant.py` 由 T017 → T018 串行。
- 镜像同步行（T014/T021/T027）永远对应「该源文件的最后一次编辑」之后；同步前不运行任何以 `.specify/` 镜像路径为对象的验收。
- 兼容性/边界测试行的用例清单先于运行评审（先写全、先评审、再运行），但其守卫对象决定它们带实现 blockedBy。

### Parallel Opportunities

- T001 / T002 / T003（写目标互不相同：pre-change-measurements.md / coverage-baseline.txt / baseline-failed.txt）。
- T014（scripts 对镜像同步）与 T015 之外无同阶段并行面——红先测试行共享证据汇，按序执行（见 § Within Each User Story）。
- T016（汇总契约测试）与 T012/T013 所在的接收腿跨阶段天然不并行（阶段顺序），但同阶段内 T019 可与 T017/T018 的早期编辑并行（T019 只写集成测试文件， blockedBy 仅 T013）。
- T021 / T020（镜像同步 vs 取证）；T024 与 T022/T023 写目标不同。
- T026（docs/）与 T027（镜像/副本）在 T025 完成后互不写冲突，可并行；T027 与 T025 之间由 `[blockedBy: T025]` 定序（源只读引用不构成并行对象）。

---

## Parallel Example

```bash
# Setup: 三份基线互不覆盖，可并行
Task: "T001 捕获改前镜像漂移基线到 notes/pre-change-measurements.md"
Task: "T002 冻结 coverage-baseline.txt"
Task: "T003 执行 E2 全量基线（--names-out baseline-failed.txt，恰好一次）"

# 打包腿: 红先测试共享证据汇，按 T004 → T005 顺序
Task: "T004 红先单元测试 tests/unit/test_feedback_exec_quant_payload.py"
Task: "T005 红先契约测试 tests/contract/test_feedback_exec_quant_payload.py"

# 接收腿收口: T013 完成后镜像同步与取证各一行
Task: "T014 sync-mirrors --write --only scripts + 复查"
Task: "T015 接收腿定向转绿 + E3 取证（与 T014 写目标不同，可并行）"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: 本特性两个 P1 故事只有合起来才是可独立演示的增量（打包腿没有接收腿时数据止步于一个 zip；接收腿没有打包腿时无包可解），故 MVP = 打包腿 + 接收腿（Phase 2 + Phase 3）。每个故事阶段有独立 Checkpoint（打包腿可独立验收「数据可被收回」，接收腿可独立验收「收回 → 解出」闭环）。

1. 完成 Phase 1（Setup：三份基线）。
2. 完成打包腿（红先测试 → 实现 → T009 转绿取证）。
3. 完成接收腿（同法）。
4. **STOP and VALIDATE**: 按 Phase 2/3 的 Checkpoint 独立验收 MVP（快速启动场景 1/2/5 断言），再进入 Phase 4。

### Incremental Delivery

1. Setup + 打包腿 → 载荷可入包（独立价值：客户侧可收回）。
2. + 接收腿 → 数据落聚合层（MVP 闭环：收回 → 解出）。
3. + 汇总腿 → 跨项目机器可读聚合视图（「分析和汇总」入口兑现）。
4. + 边界腿 → 凭据/网络/回归守卫零违例。
5. Polish → 文档/镜像/quickstart/SC 证据/Completion Gate 收口。

---

## Notes

- `[P]` 仅表示可并行，不表示可跳过依赖；带 `[blockedBy:]` 的行必须在被列任务全部 `[X]` 后开始。
- 契约条款使用规范 `C-1`…`C-31`（`clause_extract.py` 实测 31 条 md-bold-closed）；31 条由 `[green:]` 在 T006/T007/T008/T012/T013/T017/T018/T022/T023/T024/T027 完整分区认领，每条恰一行，由 `validate-tasks.py` 四项 green 检查与 `account-clause-coverage.py` 核对。
- `[[STR-001]]` / `[[STR-002]]` 一律按 requirements.md § Shared Strings 解析；测试与文档不得内联字面值。
- 三腿零网络、零自动传输、零新增确认门；源存储（客户 exec-quant store 与 feedback store）全程只读；遗留单体流只读回退永不重写。
- 聚合层 `.specify/memory/exec-quant/aggregated/` 是运行时派生层：实现与测试产生的信封/汇总按并发开发安全纪律按条落盘；本特性的 git 提交按 Artifact Commit 约定只含特性产物（tasks.md / 证据 / 文档 / 引擎 / 测试 / 镜像），运行时记录与真实入站包零提交。
- 禁改面（§ Path Conventions Read-only isolation）任何任务不得触碰；`.specify/specs/059-exec-quant-recording/` 零改写（FR 修订关系仅记录于 068 侧）。
- 测试用自构夹具，不读写真实入站包 `feedback/feedback-20261022T062525Z.zip` 与样例客户项目存储的写面。
- Feature 068 生命周期保持 `Planned`：tasks 阶段零注册表变更（Feature list review 已完成：零新增、零失效，`Total Features`=65 与实际行数一致）；`Planned → Implemented` 推进属 implement 阶段。
- 任何流程不 push、不合并、不删除分支；提交按 `.specify/shared/workflow/artifact-commit-step.md` 显式路径单行信息。




