# Tasks: Review P1 Governance（评审 P1 治理）

**Requirement ID**: 063 (from branch `063-review-p1-governance`)
**Requirement Key**: `063-review-p1-governance`
**Related Feature**: Feature 063 Review P1 Governance（评审 P1 治理） (from `.specify/memory/features.md`，状态 Planned)
**Input**: Design documents from `.specify/specs/063-review-p1-governance/` — plan.md, requirements.md, research.md, data-model.md, contracts/ ×4（34 条款）, quickstart.md, feature-ref.md；权威评审报告 `.specify/specs/062-humanize-command/review.md`（证据，不编辑）
**Prerequisites**: plan.md (required), requirements.md (required), research.md, data-model.md, contracts/, quickstart.md, feature-ref.md, notes/ 冻结基线

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating（`.specify/memory/constitution.md` 确定性 grep 检出 MUST 级测试要求）；本特性包含可执行代码（三个引擎脚本的 args-manifest/缺参行为、抽取器双宽度实现），template-only 门不适用；每个机制先写契约测试/变异演练（红）再实现（FR-027/C-32），另按 engine-action 封闭集与镜像守卫的既有契约测试同批更新。

**Tests**: 契约测试 MANDATORY 且红先行（断言的路径/字面量尚未存在或行为未实现）。变异演练覆盖全部否定命题条款（"X MUST NOT 发生"）。名字级失败对比以冻结基线为准（零新增失败判据），既有失败不属本特性修复面。

**Organization**: Tasks are grouped by user story. 机制修复按 F1–F8 → US1–US6 组织：US1 = F1+F2（analyze 消费质量信号 + checklist 责任阶段）、US2 = F3（REC 持久化与所有权）、US3 = F4（编译 Wrap-up face 可执行）、US4 = F6（pass→证据绑定）、US5 = F7（冻结基线消费侧预检）、US6 = F5+F8（载体开放 + gate 逐字引用，P2）。跨切面义务 C-31..C-34 在 Polish 收口。无 Phase 2 Foundational（无阻断所有 story 的共享前置——各 story 的红测试随各自 phase 红先行，Setup 只承担改前证据冻结），依模板指引整节省略。

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]` (or `[~]` with a recorded deferral reason); zero `[ ]` / `[>]` rows remain.
- DoD-2: All 23 deliverables in `feature-ref.md` § Deliverable surface exist at their canonical paths and are listed with evidence in `verification.md`.
- DoD-3: All 34 contract clauses C-1..C-34 are claimed exactly once by a `[green:]` row, and every claimed check passes.
- DoD-4: 10 个契约测试文件全绿——7 新建（`tests/contract/test_review_p1_checklist_governance.py`、`test_review_p1_recheck_waiver.py`、`test_review_p1_review_loop.py`、`test_engine_face_contract.py`、`test_evidence_binding_contract.py`、`test_baseline_preflight_contract.py`、`test_premise_carrier_contract.py`）+ 3 扩展（`test_clause_forms.py`、`test_clause_coverage.py`、`test_probe_engine_action_sets.py`）。
- DoD-5: Name-level test comparison shows zero NEW failures vs `notes/baseline-failed-tests.txt`（63 名，2026-10-19 冻结）；既有失败不计数、基线不放宽不改写。
- DoD-6: `probe-utils.py --action compile-embeds --check` 零漂移且 `backlog.md` 第 89 行（2026-10-15）翻转 closed；本特性触碰的镜像对字节一致、`sync-mirrors.py --check` 相对 `notes/baseline-mirror-check.txt` 零 NEW drift；`regen-command-copies.py --check` 相对 `notes/baseline-regen-check.txt` 零 NEW drift；活动 `.specify/instructions.md` 含 `REC-` 枚举。
- DoD-7: `verification.md` lists SC-001..SC-014 with status and evidence paths; quickstart S1–S10 real runs recorded in `notes/quickstart-run.md`.
- DoD-8: `git diff -- .specify/specs/062-humanize-command/` 为空（062 制品零变更）；新增外部服务、网络调用、模型 API、第三方依赖、后台常驻进程数均为 0。

**DoD Status**: pending

## Completion Gate

- GATE-1: Zero NEW test failures by name — check: `bash scripts/bash/run-tests.sh --names-out /tmp/s63-gate1.txt` 后 `comm -13 .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt /tmp/s63-gate1.txt` 输出为空（比较形态 owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs；本文件只具名 feature 冻结名单，不复述其程序）。
- GATE-2: Per-tool copies clean — check: `python3 scripts/python/regen-command-copies.py --check` 相对 `notes/baseline-regen-check.txt` 零 NEW drift，且 analyze/review/implement 的四个 per-tool 副本含本次编辑。
- GATE-3: Touched mirrors byte-identical — check: `python3 scripts/python/sync-mirrors.py --check` 相对 `notes/baseline-mirror-check.txt` 零 NEW DIFF 行，且本特性触碰对（plan.md § Mirror Obligations 表所列源文件）逐一 `diff -q` exit 0。
- GATE-4: Compile face — check: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` 零漂移（相对 `notes/baseline-compile-check.txt` 零 NEW attribution）；`grep -n "2026-10-15" .specify/memory/feedback/backlog.md` 第 89 行行内状态段读作 `closed`。
- GATE-5: Contract tests green — check: `python3 -m pytest tests/contract/test_clause_forms.py tests/contract/test_clause_coverage.py tests/contract/test_review_p1_checklist_governance.py tests/contract/test_review_p1_recheck_waiver.py tests/contract/test_review_p1_review_loop.py tests/contract/test_probe_engine_action_sets.py tests/contract/test_engine_face_contract.py tests/contract/test_evidence_binding_contract.py tests/contract/test_baseline_preflight_contract.py tests/contract/test_premise_carrier_contract.py -q` exit 0。
- GATE-6: No open/claimed rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/063-review-p1-governance/tasks.md` 返回 0（`[~]` 行如有，列于 `verification.md` deferred_tasks）。
- GATE-7: Structural validity — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-review-p1-governance/tasks.md` exit 0（34 绿点、无 collision）；`python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-review-p1-governance/requirements.md` exit 0。
- GATE-8: 23 deliverables present — check: 对 `feature-ref.md` § Deliverable surface 每条路径 `test -e`，缺一即门失败。

## Environment Prerequisites

- Python / pytest: **available** — probe: `python3 --version` → `Python 3.11.11`; `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-19；affected: 全部自动化检查（所有 phase）。
- cws-lib-bash (`CWS_LIB_BASH_HOME`): **resolvable** — probe: `bash scripts/bash/run-tests.sh --names-out .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt` @ 2026-10-19 → `63 failed, 3954 passed`（0:02:43，exit 0），名字集与 plan 阶段冻结逐一相等（`git diff` 于该文件为空，集合相等而非仅计数相等）；affected: T001、GATE-1、T046。若运行环境丢失该依赖，按 062 先例记 blocked/degraded verdict，MUST NOT 放宽或改写基线。
- 外部环境依赖: **none** — 本特性全部检查为本地 pytest 与仓库内脚本；无容器/镜像仓库/实集群/网络调用需求（生成期判定 2026-10-19）；affected: none。
- 仓库内既有漂移基线（数值 owner = T001 落盘的三个 baseline 文件 + § measured premises，此处只记探测日期与受影响行）: sync-mirrors 既有 DIFF 集、regen copies 状态、compile-embeds 单元/漂移状态 @ 2026-10-19；affected: T001、T044、T045、GATE-2..GATE-4 (see § Environment Prerequisites 的 per-row 数值引用，双要件合规形态)。

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- **[blockedBy: T001,T002]** (optional): explicit dependency tag — this task MUST NOT start until every listed task is `[X]`. Machine-checkable alternative to prose like "depends on T012"; prefer it whenever a dependency exists. Tasks without the tag follow phase order only.
- **[green: <contract>#<clause>]** (optional, repeatable): green-point attribution tag — this row is the one that turns that contract clause green. A row may declare zero or more; a row declaring none keeps exactly the plain form above, so the tag is purely additive. The contract path resolves relative to this tasks.md's own directory first and the repository root second. Keep the tag on the task row: the one-line-per-task rule is owned by `.specify/templates/commands/tasks.md` § "One line per task (mechanical-validation contract)" and is machine-enforced, so a tag folded onto a continuation line is a format error. `scripts/python/validate-tasks.py` parses the tag and reports: a contract path or clause id that does not resolve → `green-dangling` (**ERROR**); claims on one contract whose clause order runs backwards against the row order → `green-cross-phase` (WARN, an earlier row cannot leave that contract green at its own phase); one clause claimed by two rows → `green-clause-collision` (WARN); one test path claimed green at two different points by two rows → `green-path-divergence` (WARN). Partition a contract's clauses across the rows that own them so each clause is claimed exactly once, and never silence a WARN by deleting the tag — that removes the evidence of the conflict without removing the conflict.
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Task has not been completed. A run is NOT complete while any `[ ]` remains.
- `- [>]` — **Claimed / in progress**. Used only in multi-agent runs. Single-agent runs may skip this state.
- `- [X]` — **Closed**. Task has been fully executed and verified.
- `- [~]` — **Deferred**. Reasons must be recorded in `verification.md` under `deferred_tasks=`.

## Path Conventions

- Framework source（编辑面）: `shared/`、`templates/`、`skills/`、`scripts/`、`tests/`（两顶帽子：全部机制修复落源侧，FR-026/C-31）。
- Runtime mirrors（生成面，不手改）: `.specify/skills/`、`.specify/shared/`、`.specify/templates/`（sync-mirrors）、四 per-tool 命令副本（regen）、`.specify/instructions.md`（generate-instructions.sh）、编译 `## Wrap-up` 面（compile-embeds）。
- Feature evidence: `.specify/specs/063-review-p1-governance/`（`notes/`、`verification.md`、`coverage-baseline.txt`）。
- 062 制品: `.specify/specs/062-humanize-command/` 只读证据（FR-029/C-34）。

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze the pre-change side of every diff/drift premise and record the environment verdict before any artifact is written.

- [X] T001 捕获改前侧证据：逐项实跑并写入 `.specify/specs/063-review-p1-governance/notes/pre-change-measurements.md`（命令、日期、真实输出）——`python3 scripts/python/regen-command-copies.py --check`（落盘 `notes/baseline-regen-check.txt`）、`python3 scripts/python/sync-mirrors.py --check`（落盘 `notes/baseline-mirror-check.txt`）、`python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check`（落盘 `notes/baseline-compile-check.txt`）、062 覆盖通道 dark 实测与 `find .specify/specs -name coverage-baseline.txt` 清点、`.specify/memory/register.md` 的 `REC-` 行数清点、`.specify/memory/feedback/backlog.md` 第 89 行状态快照；`notes/baseline-failed-tests.txt`（63 名）与 `coverage-baseline.txt` 已于本 tasks 生成阶段重冻/首冻（2026-10-19，见 § measured premises），本行只引用不重跑；环境判据一律指向本文件 § Environment Prerequisites，不在此复述。

**Checkpoint**: pre-change measurements exist; every later "diff against pre-change" premise has a dated baseline.

---

## Phase 2: User Story 1 - 分析阶段看见已写下的质量信号 (Priority: P1) 🎯 MVP

**Goal**: 框架维护者写在检查单里的 `Gap` 与混用全/半角括号的契约引用组，在下一次 `/speckit.analyze` 即被消费——`Gap` 升格或确定性处置、覆盖核算成为固定步骤、`coverage-baseline.txt` 由 tasks 冻结、已回答条目走 append-only recheck 不再必然 waiver。

**Independent Test**: 在 fixture 中放入带未勾选 `Gap` 的 checklist 与混宽契约集，运行 analyze 与覆盖核算；断言 `Gap` 被升格/处置、双宽度单一总数、baseline-missing 可见呈现、recheck 回答免 waiver（quickstart S1–S4）。

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T002 [US1] 扩展 `tests/contract/test_clause_forms.py`：新增双宽度引用组确定性自测样本（≥1 全角组、≥1 同宽度一层嵌套组、≥1 跨宽度畸形组、1 个 ASCII-only 语料在双宽度实现下总数不变样本），并断言 owner 正文 § 4 rule 2 对定界字符集与同宽度嵌套规则的字面声明存在（per `shared/definitions/contract-clause-definitions.md`，C-1/C-2 钉；不并行：该只读断言对象由 T006 写入）；当前树先红，red 输出由 T005 统一落盘 per `notes/red-first-evidence.md`。
- [X] T003 [P] [US1] 扩展 `tests/contract/test_clause_coverage.py`：钉 analyze 固定步骤接线（技能与命令面以只读方式接入覆盖核算引擎 per `scripts/python/account-clause-coverage.py`，无 `--freeze`）、tasks 冻结义务（[[STR-002]] 经 `--freeze` 产出、无契约集 feature 显式 skip 不伪造空基线）、双侧同一路径形（`<spec-dir>/coverage-baseline.txt` 即 `--baseline` 缺省）、baseline-missing 作为阶段可见问题呈现（C-5/C-6/C-7 钉）；当前树先红，red 输出由 T005 统一落盘 per `notes/red-first-evidence.md`。
- [X] T004 [P] [US1] 新建两个互不重叠的钉文件：`tests/contract/test_review_p1_checklist_governance.py` 钉 `checklists/*.md` 装载行（load table 含 item text、checked state、tags）与 `[Gap]` 未勾选项升格/处置的确定性标记形态（自由散文不满足、「未勾选+未升格+未处置」计数可观察且为 0）（C-3/C-4 钉）；`tests/contract/test_review_p1_recheck_waiver.py` 钉 append-only recheck 形态（每轮新文件、回答引用 requirement 行、原 checklist 不原地刷新）、implement 豁免门第三分支（已回答条目不计未完成）与 waiver 四段格式缺一即不合规（C-8/C-9/C-10 钉）；当前树先红，red 输出由 T005 统一落盘 per `notes/red-first-evidence.md`。
- [X] T005 [US1] [blockedBy: T002,T003,T004] 运行上述四个测试文件确认按预期红（失败原因为制品缺失而非断言写错），把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 1

- [X] T006 [P] [US1] [blockedBy: T005] 实现 C-1+C-2：在 `shared/definitions/contract-clause-definitions.md` § 4 rule 2 增加规范性定界字符集句（开组 `(` 或 `（`、对应闭组 `)` 或 `）`、嵌套 MUST 同宽度匹配、跨宽度/不配对 = 畸形组由检查器报告且不得静默计为引用或 mention）；`scripts/python/clause_extract.py` 的 `parentheticals()` 按同一字符集实现双宽度 + 同宽度一层嵌套（既有深度语义保持），畸形组作为独立结果输出（既非引用亦非 mention）。
- [X] T007 [P] [US1] [blockedBy: T005] 实现 C-3+C-4+C-5：`skills/internal/analyze-artifacts/SKILL.md` § 2 装载表增加 `checklists/*.md` 行，检测遍增加 checklist 遍（未勾选 `[Gap]` 条目升格为 finding 或给出确定性 disposition 标记，报告使「未勾选+未升格+未处置」计数可观察且为 0），工作流增加固定步骤只读调用覆盖核算（per `scripts/python/account-clause-coverage.py`，`--spec <spec-dir>` 无 `--freeze`），`status: baseline-missing` 作为阶段可见问题与 remedy（重跑 `/speckit.tasks`）呈现，无契约集 feature 记录显式 skip 及理由；`templates/commands/analyze.md` § Delegation Inputs 具名 checklist 面与覆盖核算步骤。
- [X] T008 [P] [US1] [blockedBy: T005] 实现 C-6：`skills/internal/create-tasks/SKILL.md` § Runtime-evidence landing points 增加覆盖基线冻结义务——含契约集的 feature 经覆盖核算引擎冻结路径（per `scripts/python/account-clause-coverage.py` 的 `--freeze`，引擎缺省路径与 `BASELINE_NAME`）产出 [[STR-002]]，时机与既有 re-freeze timing 一致（每 feature 第一次全树核算，非首次全绿）；无契约集 feature 显式 skip 并说明理由，不伪造空基线。
- [X] T009 [P] [US1] [blockedBy: T005] 实现 C-8：`skills/internal/create-checklist/SKILL.md` § 5 Generate 声明 recheck 形态——答案落每轮一个 append-only recheck 文件（`checklists/recheck-<date>-<topic>.md`），每个已回答条目引用它所回答的 requirement 行，原 checklist MUST NOT 原地刷新、未勾选行保留为历史（061 REC-C5 落点）。
- [X] T010 [P] [US1] [blockedBy: T005] 实现 C-9+C-10：`skills/internal/implement-feature/SKILL.md` § Step 2 — Checklist exemption gate 增加第三分支（后续阶段已按 recheck 记录回答的条目计为已回答、不计未完成、无需 waiver，门只对真正未解决条目触发）与 waiver 四段格式（`Scope`/`Basis`/`Disposition`/`Closed`，`Closed` 说明是什么解决了它；缺任一段不合规、不得当作已关闭证据）（061 REC-C6 落点）。

### Verification for User Story 1

- [X] T011 [US1] [blockedBy: T006] 运行 `tests/contract/test_clause_forms.py` 全绿（双宽度/嵌套/畸形/ASCII 不变样本 + owner 正文断言），通过输出记入 `verification.md`；认领 C-1、C-2。 [green: contracts/template-mechanisms.md#C-1] [green: contracts/template-mechanisms.md#C-2]
- [X] T012 [US1] [blockedBy: T007] 按 quickstart S3 形态在 fixture（一条 `[覆盖/安全, Gap]` 未勾选项 + 一条无 Gap 未勾选项）上演练 checklist 装载与 Gap 消费（升格/处置标记、「未勾选+未升格+未处置」=0、无 Gap 条目无新义务），运行 `tests/contract/test_review_p1_checklist_governance.py` 相关腿全绿，结果记入 `verification.md`；认领 C-3、C-4。 [green: contracts/template-mechanisms.md#C-3] [green: contracts/template-mechanisms.md#C-4]
- [X] T013 [US1] [blockedBy: T007,T008] 按 quickstart S1/S2 形态演练双宽度语料单一总数（fixture 契约集含全/半角与同宽度嵌套）与 analyze 覆盖 verdict（只读运行 + baseline-missing 可见呈现 + 无契约集显式 skip），运行 `tests/contract/test_clause_coverage.py` 全绿并核对 analyze 消费侧与 tasks 冻结侧命名的同一文件路径形，结果记入 `verification.md`；认领 C-5、C-6、C-7。 [green: contracts/template-mechanisms.md#C-5] [green: contracts/template-mechanisms.md#C-6] [green: contracts/template-mechanisms.md#C-7]
- [X] T014 [US1] [blockedBy: T009,T010] 按 quickstart S4 形态演练 recheck 回答（fixture：下游阶段已答条目 → 豁免门计为已回答、原 checklist `git diff` 为空、无需 waiver）与四段 waiver（真未解决条目产生合规 waiver；缺任一段判不合规），运行 `tests/contract/test_review_p1_recheck_waiver.py` 全绿，结果记入 `verification.md`；认领 C-8、C-9、C-10。 [green: contracts/template-mechanisms.md#C-8] [green: contracts/template-mechanisms.md#C-9] [green: contracts/template-mechanisms.md#C-10]

**Checkpoint**: US1 independently testable: 双宽度单一总数、Gap 首轮消费、覆盖基线冻结/接线、recheck 免 waiver 全部可独立验证（quickstart S1–S4）。

---

## Phase 3: User Story 2 - 评审建议成为可追踪的持久编号 (Priority: P1)

**Goal**: 评审产出的每条 `REC-` 在同一提交登记进 `register.md`，常驻指令层可发现该编号，全局建议有合法 feedback 入口，REC 目标 repo-relative 可解析，`/speckit.review` 拥有 `Implemented → Ready for Review` 转换。

**Independent Test**: fixture review 含 2–3 条 `REC-`，演练收尾：register 副本出现指针行且同提交、干净 clone 上目标可解析、入口点名存在、转换表含 review 行（quickstart S5）。

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T015 [P] [US2] 新建 `tests/contract/test_review_p1_review_loop.py`：钉 review Handoffs 具名所有者与同提交登记义务（[[STR-003]] 编号 → 一行含义 → 报告锚点 → 状态，行形态 owner 为 ID Register）、常驻指令层枚举句含 `REC-`、feedback Scope guard 保持 `scope: local` 且点名 A3 自省(Introspection) 合法入口、review 模板 § 5/Replacement Rule 3 的 repo-relative 主形态与 external 标记、状态机转换表 review 行 + checklist 行注记 + 「每命令恰一转换」不变式（C-11..C-15 钉）；当前树先红，red 输出由 T016 统一落盘 per `notes/red-first-evidence.md`。
- [X] T016 [US2] [blockedBy: T015] 运行 `tests/contract/test_review_p1_review_loop.py` 确认按预期红，把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 2

- [X] T017 [P] [US2] [blockedBy: T016] 实现 C-11：`templates/commands/review.md` § Handoffs "After" 以具名义务替换无所有者的 "Apply improvements to spec-kit templates/commands/scripts"——报告中每条 `REC-`（[[STR-003]]）在同一提交以既有指针行形态（per `.specify/memory/register.md`，编号 → 一行含义 → 报告锚点 → 状态）登记；行形态 owner 为 register，命令只拥有登记义务。
- [ ] T018 [P] [US2] [blockedBy: T016] 实现 C-12：`templates/instructions-template.md` § ID Register 枚举句加入 `REC-`；运行 `bash scripts/bash/generate-instructions.sh` 使活动 `.specify/instructions.md` 经生成器获得该行（MUST NOT 手改运行时副本），并以 `grep -n "REC-" .specify/instructions.md` 验证落位、`git diff` 于符号链接集为空。
- [X] T019 [P] [US2] [blockedBy: T016] 实现 C-13：`shared/workflow/feedback-step.md` § Scope guard 保持 wrap-up 条目 `scope: local` 规则，并点名全局 review 建议的既有合法入口——`/speckit.feedback` manage-feedback Path A digest § A3 自省(Introspection)（评审报告 "Mode 5 自省" 为历史名）；不新建 intake 存储、跟踪引擎或评分系统。
- [X] T020 [P] [US2] [blockedBy: T016] 实现 C-14：`templates/review-template.md` § 5 与 Replacement Rule 3 把 repo-relative 路径改为 REC 目标主形态（任意 checkout 可解析），绝对路径仅作括号补充；无 repo-relative 形态的外部目标标记 `external` 并给出理由；不回退到 061 的机器本地 absolute-only 形态。
- [X] T021 [P] [US2] [blockedBy: T016] 实现 C-15：`shared/workflow/feature-integration.md` § Status State Machine 在 checklist 行后增加 `| /speckit.review | Implemented → Ready for Review | review.md committed AND every deferred item resolved or waived |`，checklist 行注记「仅在其于 implement 之后运行时适用」，文档头部命令清单加入 `/speckit.review`；「每个命令恰好拥有一个转换」保持成立（E2 裁决落位）。

### Verification for User Story 2

- [ ] T022 [US2] [blockedBy: T017,T018,T019,T020,T021] 运行 `tests/contract/test_review_p1_review_loop.py` 全绿；按 quickstart S5 形态做 seed 演练（临时目录内 fixture review 含 2–3 条 `REC-` → register 副本指针行 + 同提交检查 + 干净 clone 上 repo-relative 目标解析演练 + 转换表行核对），结果记入 `verification.md`；认领 C-11、C-12、C-13、C-14、C-15。 [green: contracts/template-mechanisms.md#C-11] [green: contracts/template-mechanisms.md#C-12] [green: contracts/template-mechanisms.md#C-13] [green: contracts/template-mechanisms.md#C-14] [green: contracts/template-mechanisms.md#C-15]

**Checkpoint**: US2 independently testable: 登记义务、枚举、入口、目标形态、转换行全部可独立验证（quickstart S5）。

---

## Phase 4: User Story 3 - 编译后的 Wrap-up face 可按原文执行 (Priority: P1)

**Goal**: 任意 `/speckit.*` 命令的编译收尾面逐字可执行：渲染完整参数全集 + 源参数与占位约定，引擎缺参一次全列，幂等语义不动，全部单元重编译零漂移并关闭 backlog 2026-10-15 行。

**Independent Test**: 隔离工作区逐字执行编译 face 的引擎调用（一次成功、无缺参）；缺 ≥2 必填参数的 fixture 得到一次列全的错误；duplicate 键返回 duplicate 且不铸 run-id（quickstart S6；重编译收口在 T044）。

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T023 [P] [US3] 扩展 `tests/contract/test_probe_engine_action_sets.py`：`args-manifest` 加入三个 wrap-up 引擎（`scripts/python/run-determination.py`、`scripts/python/feedback-utils.py`、`scripts/python/exec-quant.py`）的 action 封闭集，并同步更新其 owner 契约（per `.specify/specs/056-probe-handler-system/contracts/engine-action-sets.md`，同批变更）（C-22 钉）；当前树先红，red 输出由 T025 统一落盘 per `notes/red-first-evidence.md`。
- [ ] T024 [P] [US3] 新建 `tests/contract/test_engine_face_contract.py`：钉渲染器行为（kind=engine handler 行渲染该 action 必填参数全集 + 源参数、run 域值尖括号占位、约定行由 registry 声明而非逐命令手写、拒收参数不渲染且渲染器无手写参数表）、缺 ≥2 必填参数一次全列（两引擎、输入错误退出码 2 保持）、幂等变异演练（`(unit_id, run_id)` 重复返回 `duplicate: true` 且引擎任何路径不铸造/派生/替换 run-id）（C-20/C-21/C-23/C-24 钉）；当前树先红，red 输出由 T025 统一落盘 per `notes/red-first-evidence.md`。
- [ ] T025 [US3] [blockedBy: T023,T024] 运行上述两个测试文件确认按预期红，把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 3

- [ ] T026 [US3] [blockedBy: T025] 实现 C-22+C-23：`scripts/python/run-determination.py`、`scripts/python/feedback-utils.py`、`scripts/python/exec-quant.py` 各暴露由自身 parser 派生的机器可读参数清单 action（`--action args-manifest`，输出 JSON `{action: {required: [...], source: [...]}}`，parser 为唯一真源、无手写副本）；同批把 `run-determination.py` 与 `feedback-utils.py` 的逐参单错校验替换为一次调用列出全部缺失必填参数的单个错误（`InputError`/`FeedbackError` 单报全列；输入错误退出码约定保持：两引擎均 2）。
- [ ] T027 [US3] [blockedBy: T026] 实现 C-20+C-21：`scripts/python/probe-utils.py` `--action compile-embeds` 渲染器在编译期从各 handler 的引擎取得 args manifest（无 manifest 的引擎/action 对响亮失败编译——fast-fail 面，不静默退回 unit-id-only 渲染），按占位约定渲染必填参数全集 + 源参数与 run 域占位值，渲染面仅在其引擎行含占位符时携带一行约定说明；占位约定（语法、代入规则「尖括号为本轮运行时值——代入后照抄执行」、渲染集合成员资格）声明进 `shared/definitions/probe-definitions.md` § Handler note（registry 拥有约定，非逐命令手写）。

### Verification for User Story 3

- [ ] T028 [US3] [blockedBy: T026,T027] 运行 `tests/contract/test_engine_face_contract.py` 与 `tests/contract/test_probe_engine_action_sets.py` 全绿（fixture manifest 渲染断言含拒收参数不渲染、缺 ≥2 参一次全列 fixture、duplicate/idempotency 变异；per quickstart S6 前提，全单元重编译收口在 T044），结果记入 `verification.md`；认领 C-20、C-21、C-22、C-23、C-24。 [green: contracts/engine-face-contract.md#C-20] [green: contracts/engine-face-contract.md#C-21] [green: contracts/engine-face-contract.md#C-22] [green: contracts/engine-face-contract.md#C-23] [green: contracts/engine-face-contract.md#C-24]

**Checkpoint**: US3 independently testable: 渲染契约、一次全列、幂等不变全部由契约测试钉住；全单元重编译与 backlog 收口在 Polish T044 闭合。

---

## Phase 5: User Story 4 - “声称 PASS”必须绑定到归档证据 (Priority: P1)

**Goal**: 验证记录中每个 `pass` 都有结构化证据行（sample id → 归档路径 → SHA-256 → verdict），由注册的 command-gate 机械检查；缺失/为空/不匹配判红，不再依赖执行者自披露。

**Independent Test**: fixture `verification.md` 四 `pass` 样本（证据齐全/缺失/为空/哈希不匹配）+ 非 pass 样本，运行证据绑定门检查：仅齐全者绿、三种反向各自判红并点名样本 id（quickstart S8）。

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T029 [P] [US4] 新建 `tests/contract/test_evidence_binding_contract.py`：钉验证日志模板证据段（位置：implement results 与 SC evaluation 之间；字段 `sample_id`/`evidence_path`/`evidence_sha256`/`verdict`；SHA-256 算法声明；`pass` 须完整证据行）、`gate-implement-evidence-binding`（[[STR-001]]）注册形态（`command-gate` 行 + `h-gate-evidence` HandlerBinding `@point:confirm-gate`，与既有 `gate-implement-checklist-waiver` 同形、复用 gate-probe 机制）与判红语义变异演练（缺失/为空/哈希不匹配三变异各自判红并点名样本 id 与原因、非 `pass` verdict 无绑定义务、无证据段的 `pass` = unverified 不得作为通过证据引用）（C-26/C-27/C-28 钉）；当前树先红，red 输出由 T030 统一落盘 per `notes/red-first-evidence.md`。
- [ ] T030 [US4] [blockedBy: T029] 运行 `tests/contract/test_evidence_binding_contract.py` 确认按预期红，把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 4

- [ ] T031 [P] [US4] [blockedBy: T030] 实现 C-26：`templates/verification-log-template.md` 在 `# -- /speckit.implement results --` 与 `# -- Success Criteria evaluation --` 之间增加结构化证据记录段（每 evaluation sample 一行：`sample_id` → 归档工件 repo-relative 路径 → 内容 SHA-256 → verdict），模板声明确定性哈希算法（对归档文件字节计算 SHA-256，`sha256sum` 兼容）与「`pass` verdict 必须有完整证据行」规则；既有段集与键值约定保持，新增段为增量。
- [ ] T032 [P] [US4] [blockedBy: T030] 实现 C-27：`shared/definitions/probe-definitions.md` 在既有 command-gate 行旁注册 `gate-implement-evidence-binding`（[[STR-001]]，class `command-gate`、unit `/speckit.implement`）并增加 `h-gate-evidence` HandlerBinding 行 `@point:confirm-gate`（与 `gate-implement-checklist-waiver` 同形；复用既有 gate-probe 机制、触发证据经 feedback 引擎 `--lifecycle-point` 记录，不新增子系统）；`skills/internal/implement-feature/SKILL.md` 在填充 `verification.md` 的验证日志步骤（Step 9）旁引用该 gate（技能无 per-feature GATE 编号，锚点为拥有被检证据的步骤）。

### Verification for User Story 4

- [ ] T033 [US4] [blockedBy: T031,T032] 按 quickstart S8 形态演练证据绑定门：fixture `verification.md`（四 `pass` 样本——证据存在且哈希匹配 / 归档文件缺失 / 空文件 / 哈希不匹配 + 一 `fail` verdict 样本 + 无证据段形态），运行 `tests/contract/test_evidence_binding_contract.py` 全绿，结果记入 `verification.md`；认领 C-26、C-27、C-28。 [green: contracts/evidence-baseline-contract.md#C-26] [green: contracts/evidence-baseline-contract.md#C-27] [green: contracts/evidence-baseline-contract.md#C-28]

**Checkpoint**: US4 independently testable: 证据段、gate 注册、判红语义全部可独立验证（quickstart S8）。

---

## Phase 6: User Story 5 - 冻结基线在消费侧被重新读懂 (Priority: P1)

**Goal**: `/speckit.implement` 开工前重新捕获每个冻结基线（集合目录派生），差异写回引用行并按 `git log` 归因四分类（含 `undecidable`），之后才允许漂移 verdict；命令面同职责。

**Independent Test**: fixture：冻结名单与树不一致 + 一个缺失基线文件，运行 implement 预检：数值重捕获写回、逐差异分类或显式 `undecidable`、缺失按首次捕获处理（quickstart S9）。

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T034 [P] [US5] 新建 `tests/contract/test_baseline_preflight_contract.py`：钉 implement 预检步骤文本（位于 Step 1 之前；重捕获集合由目录派生 glob（C-29 的两个 glob 根 + [[STR-002]]）而非手写条数；差异先写回引用行、任何漂移 verdict 之前按 `git log` provenance 四分类；`undecidable` 显式报告不猜测；缺失基线按首次捕获记录 provenance 而非零漂移）与命令面同职责文本（C-29/C-30 钉）；当前树先红，red 输出由 T035 统一落盘 per `notes/red-first-evidence.md`。
- [ ] T035 [US5] [blockedBy: T034] 运行 `tests/contract/test_baseline_preflight_contract.py` 确认按预期红，把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 5

- [ ] T036 [P] [US5] [blockedBy: T035] 实现 C-29：`skills/internal/implement-feature/SKILL.md` 在 Step 1 之前增加预检步骤——重新捕获该 feature 的每个冻结基线（集合按目录派生：`<spec-dir>/baseline-*` 与 `<spec-dir>/notes/baseline-*` 两个 glob 根 + [[STR-002]] 覆盖基线，不手写条数）；重捕获值不同时把新值写入引用它的行，并在任何漂移 verdict 之前用 `git log` provenance 把每处差异分类为 `upstream repair` / `inherited` / `attributable to this feature` / `undecidable`；`undecidable` 显式报告，不猜测；缺失基线文件按首次捕获处理并记录 provenance，不得当作零漂移。
- [ ] T037 [P] [US5] [blockedBy: T035] 实现 C-30：`templates/commands/implement.md` 在 Skill Delegation inputs（「follow its steps 1–9」之前）陈述与 C-29 相同的预检职责，使义务抵达仅读命令面的读者，不只在技能内部。

### Verification for User Story 5

- [ ] T038 [US5] [blockedBy: T036,T037] 按 quickstart S9 形态演练预检（fixture：冻结名单与树不一致 + 一个缺失基线文件 → 数值重捕获、引用行写回 diff、逐差异分类或显式 `undecidable`、缺失按首次捕获处理非零漂移），运行 `tests/contract/test_baseline_preflight_contract.py` 全绿，结果记入 `verification.md`；认领 C-29、C-30。 [green: contracts/evidence-baseline-contract.md#C-29] [green: contracts/evidence-baseline-contract.md#C-30]

**Checkpoint**: US5 independently testable: 预检、写回、四分类、命令面同职责全部可独立验证（quickstart S9）。

---

## Phase 7: User Story 6 - 陈旧前提与 gate 引用不再静默漂移 (Priority: P2)

**Goal**: 环境判据的复述无载体可逃逸（任何 assumption 或 decision 或自由散文行都受约束且带日期 + 指针双要件）；red-first note 逐字引用 gate 行，重编号产生可见不匹配。

**Independent Test**: seed 行无日期/无指针被载体规则标记直至双要件齐备（date-only 与 pointer-only 各自失败）；裸 gate id 引用的 note 在 gate 重编号 fixture 上产生可见不匹配（quickstart S7）。

### Tests for User Story 6 (MANDATORY) ⚠️

- [ ] T039 [P] [US6] 新建 `tests/contract/test_premise_carrier_contract.py`：钉载体清单开放（create-tasks SKILL item 2 的「MUST reference § Environment Prerequisites instead of restating verdicts」义务覆盖 per-phase prerequisites、`[~]` notes 与任何 assumption 或 decision 或自由散文行）、复述行双要件（ISO 日期 + `(see § Environment Prerequisites)` 指针，缺一不合规；tasks 模板 ACTION REQUIRED 同步扩展）、red-first note 逐字引用 gate 行（id + name + check command；裸 id 不可用；重编号产生可见不匹配）、re-freeze timing 指向 implement 消费侧步骤（C-16/C-17/C-18/C-19 钉）；当前树先红，red 输出由 T040 统一落盘 per `notes/red-first-evidence.md`。
- [ ] T040 [US6] [blockedBy: T039] 运行 `tests/contract/test_premise_carrier_contract.py` 确认按预期红，把命令、真实红输出与退出码粘贴进 `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md`。

### Implementation for User Story 6

- [ ] T041 [P] [US6] [blockedBy: T040] 实现 C-16+C-18+C-19（同一文件三节，一次写入）：`skills/internal/create-tasks/SKILL.md` § Environment probe rules item 2 以开放载体清单替换封闭枚举（义务覆盖任何 assumption 或 decision 或自由散文行）、§ Runtime-evidence landing points 的 red-first note 形态规则增加逐字引用 gate 行义务（id + name + check command；前向适用，062 的 note 实例不在本特性编辑范围）、§ Re-freeze timing 改为指向 implement 侧消费步骤（C-29 预检）并保留生产侧 re-capture 义务。
- [ ] T042 [P] [US6] [blockedBy: T040] 实现 C-17：`templates/tasks-template.md` § Environment Prerequisites 的 ACTION REQUIRED 注释增加：任何复述环境 verdict 的行（任何载体）MUST 携带 ISO 日期戳与 `(see § Environment Prerequisites)` 指针，两者同时要求、缺一不合规。

### Verification for User Story 6

- [ ] T043 [US6] [blockedBy: T041,T042] 按 quickstart S7 形态演练载体规则（seed 行无日期/无指针 → 被标记直至双要件齐备；date-only 与 pointer-only 各自失败；裸 gate id 引用在重编号 fixture 上产生可见不匹配），运行 `tests/contract/test_premise_carrier_contract.py` 全绿，结果记入 `verification.md`；认领 C-16、C-17、C-18、C-19。 [green: contracts/template-mechanisms.md#C-16] [green: contracts/template-mechanisms.md#C-17] [green: contracts/template-mechanisms.md#C-18] [green: contracts/template-mechanisms.md#C-19]

**Checkpoint**: US6 independently testable: 载体开放、双要件、逐字 gate 引用全部可独立验证（quickstart S7）。

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 收口 F4 的全单元重编译与 backlog 翻转、两顶帽子同步分发、全局回归对比、quickstart 端到端、跨切面证据与 Feature 状态推进。

- [ ] T044 [blockedBy: T027,T032] 实现 C-25：渲染器与注册表变更全部落位后（见 § Dependencies），运行 `python3 .specify/scripts/python/probe-utils.py --action compile-embeds` 重编译全部编译单元；`--action compile-embeds --check` 零漂移；适用处以 `--reconcile` 收口（固定次序 compile → regen → sync）；同一提交把 `.specify/memory/feedback/backlog.md` 第 89 行（2026-10-15 direct-fix 行）状态翻转为 `closed` 并附 `--check` 输出为证据；结果记入 `verification.md`；认领 C-25。 [green: contracts/engine-face-contract.md#C-25]
- [ ] T045 [blockedBy: T044] 实现 C-31（两顶帽子同步）：按固定次序运行 `python3 scripts/python/regen-command-copies.py`（analyze/review/implement 四副本刷新）、`bash scripts/bash/generate-instructions.sh`（终态确认）、`python3 scripts/python/sync-mirrors.py --write --only templates --only skills/internal --only shared --only scripts`（源→镜像落位，本特性触碰的既有漂移对随写清除）；随后以 `--check` 对照 T001 落盘基线（per `notes/baseline-mirror-check.txt` 与 `notes/baseline-regen-check.txt`，2026-10-19，见 § Environment Prerequisites）确认零 NEW 漂移且触碰对字节一致；结果记入 `verification.md`；认领 C-31。 [green: contracts/cross-cutting-constraints.md#C-31]
- [ ] T046 [blockedBy: T045] 实现 C-32：`bash scripts/bash/run-tests.sh --names-out /tmp/s63-after.txt` 后 `comm -13 .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt /tmp/s63-after.txt` 输出为空（零新增失败；既有失败不属本特性修复面，基线不放宽不改写）；盘点逐机制变异演练清单（每条否定命题条款都有证明守卫在对象被破坏时转红的演练）并记入 `verification.md`；清理 `/tmp/s63-after.txt`；认领 C-32。 [green: contracts/cross-cutting-constraints.md#C-32]
- [ ] T047 [blockedBy: T045] 按 `quickstart.md` 实跑 S1–S10 端到端（各场景含 teardown；S6 在隔离工作区逐字执行编译 face 引擎调用），把命令、真实输出与退出码记入 `.specify/specs/063-review-p1-governance/notes/quickstart-run.md`。
- [ ] T048 [blockedBy: T045] 实现 C-33：对照 `pyproject.toml` 依赖清单与改动面 diff、对源码变更做网络调用/外部服务/后台常驻检索，确认新增外部服务、网络调用、模型 API、第三方依赖、后台常驻进程数均为 0；结果记入 `verification.md`；认领 C-33。 [green: contracts/cross-cutting-constraints.md#C-33]
- [ ] T049 [blockedBy: T045] 实现 C-34：`git diff --stat -- .specify/specs/062-humanize-command/` 输出为空（062 四治理制品与 notes 实例零变更，FR-029）；结果记入 `verification.md`；认领 C-34。 [green: contracts/cross-cutting-constraints.md#C-34]
- [ ] T050 [blockedBy: T046,T047,T048,T049] SC 收口：在 `verification.md` 列出 SC-001..SC-014 状态与证据路径（度量来源 per requirements § Measurement Sources & Collection Methods）；运行 `python3 .specify/scripts/python/validate-requirements.py .specify/specs/063-review-p1-governance/requirements.md` 与 `python3 .specify/scripts/python/validate-tasks.py .specify/specs/063-review-p1-governance/tasks.md` 确认 exit 0、34 绿点无 collision。
- [ ] T051 [blockedBy: T050] 按 `.specify/shared/workflow/feature-integration.md` 将 Feature 063 从 `Planned` 推进到 `Implemented`：同步 `.specify/memory/features.md` 注册行与 `.specify/memory/features/063.md` 详情，记录本次实现证据路径（Pre-Status-Flip Gate 全过后才翻转）。

---

## Feature Integration Review

- 2026-10-19, tasks phase: `.specify/memory/features.md` registers Feature 063（status `Planned`，clarify 2026-10-19 绑定 + plan 2026-10-19 推进），`.specify/memory/features/063.md` 详情存在。本任务分解不暴露新 Feature、不使既有 Feature 失效（51 项任务全部落在 FR-001..FR-030 / C-1..C-34 范围内；无跨 Feature 归属争议——机制编辑全部位于本特性声明的 owner 文件）。T051 仅在全部 gate 通过后将状态推进 `Planned → Implemented`；本阶段状态保持 `Planned`。

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependency; runs first（改前证据冻结是后续全部相对判据的基线）。
- **US1 (Phase 2)**: depends on Setup; MVP 切片（F1+F2）。
- **US2 (Phase 3)**: depends on US1 仅按阶段顺序（无共享编辑文件）；独立可测。
- **US3 (Phase 4)**: depends on US1/US2 仅按阶段顺序；其编辑面（引擎脚本 + probe 渲染/注册表）与前者不相交。
- **US4 (Phase 5)**: `probe-definitions.md` 与 `skills/internal/implement-feature/SKILL.md` 被 US1 先编辑（T010），故按阶段顺序在 US1 之后；与 US3 的注册表编辑（T027）无冲突但 T044 的重编译必须等两者齐。
- **US5 (Phase 6)**: `skills/internal/implement-feature/SKILL.md` 与 `templates/commands/implement.md` 的编辑在 US1/US4 之后（阶段顺序保证）。
- **US6 (Phase 7)**: `skills/internal/create-tasks/SKILL.md` 被 US1（T008）先编辑（阶段顺序保证）。
- **Polish (Phase 8)**: T044 阻塞于 T027（渲染器/注册表）与 T032（gate 行）——注册表投影在两者之后才稳定；T045 阻塞于 T044（compile → regen → sync 固定次序）；T046–T049 阻塞于 T045（分发面落位后才能对最终态做回归/端到端/不变量判定）；T050 阻塞于四条收口行；T051 阻塞于 T050。

### User Story Dependencies

- **US1 (P1)**: MVP；不依赖其他 story 的行为。
- **US2 (P1)**: 独立（编辑面不相交）；独立 checkpoint 在 quickstart S5。
- **US3 (P1)**: 独立（编辑面不相交）；独立 checkpoint 在 quickstart S6 的 pytest 腿，全单元重编译腿在 Polish 收口。
- **US4 (P1)**: 独立（同文件编辑由阶段顺序串行）；独立 checkpoint 在 quickstart S8。
- **US5 (P1)**: 独立；独立 checkpoint 在 quickstart S9。
- **US6 (P2)**: 独立；独立 checkpoint 在 quickstart S7。

### Within Each User Story

- 测试 MUST 先写并确认红（失败原因为制品缺失），实现后转绿；red 证据在实现开始前落盘。
- 共享写入面（`verification.md`、`notes/red-first-evidence.md`）的行不标 `[P]`；`[P]` 仅用于互斥写目标。
- Story 完成才进入下一优先级；每个 story 的 checkpoint 可独立验证。

### Parallel Opportunities

- Phase 2: T003/T004（测试文件互斥——T004 一次写两个）与 T006–T010（五个实现写目标互斥：clause 定义 + 抽取器 / analyze 技能+命令面 / create-tasks 技能 / create-checklist 技能 / implement 技能）内部并行；T002 不并行（其只读断言对象由 T006 写入，以其行内「不并行」说明为准）；验证行 T011–T014 串行（共享 `verification.md`）。
- Phase 3: T017–T021（五个源文件互斥：review 命令面 / 指令模板+生成 / feedback-step / review 模板 / feature-integration）并行。
- Phase 4: T023/T024（两个测试文件互斥）并行；T026 → T027 串行（渲染器消费 manifest）。
- Phase 5: T031/T032（模板 vs 注册表+技能，互斥）并行。
- Phase 6: T036/T037（技能 vs 命令面，互斥）并行。
- Phase 7: T041/T042（create-tasks 技能 vs tasks 模板，互斥）并行。
- Phase 8: 串行为主（共享 `verification.md` 与 compile → regen → sync 固定次序）。

---

## Parallel Example: User Story 1

```bash
# Launch the disjoint red tests for US1 together (T002 is NOT parallel: its read-only
# assertion target is written by T006, per T002's own inline note):
Task: "扩展 tests/contract/test_clause_coverage.py（T003）"
Task: "新建 tests/contract/test_review_p1_checklist_governance.py + tests/contract/test_review_p1_recheck_waiver.py（T004）"

# Launch all US1 implementation edits together after T005 (disjoint write targets):
Task: "shared/definitions/contract-clause-definitions.md + scripts/python/clause_extract.py（T006）"
Task: "skills/internal/analyze-artifacts/SKILL.md + templates/commands/analyze.md（T007）"
Task: "skills/internal/create-tasks/SKILL.md（T008）"
Task: "skills/internal/create-checklist/SKILL.md（T009）"
Task: "skills/internal/implement-feature/SKILL.md（T010）"
```

---

## Implementation Strategy

### MVP First

**MVP scope rule**: MVP = **US1 单独**（加 Setup）。US1 的 checkpoint（analyze 首轮消费 Gap + 双宽度单一总数 + 覆盖基线接线 + recheck 免 waiver）独立可测且有独立价值——它 alone 修复「证据已写下却无阶段消费」这类失效中 analyze 侧的全部机制；US2–US6 各自是独立增量，不扩张 MVP。

1. Complete Phase 1 (Setup).
2. Complete US1 (Phase 2).
3. **STOP and VALIDATE**: run the US1 independent test（quickstart S1–S4 fixture 演练）and record the MVP checkpoint.
4. Continue with US2 → US3 → US4 → US5 → US6 → Polish.

### Incremental Delivery

1. Setup → 改前证据全部有日期基线。
2. US1 → analyze 看见质量信号（MVP！）。
3. US2 → 评审建议持久化。
4. US3 → 编译面逐字可执行（重编译在 Polish 收口）。
5. US4 → pass 绑定归档证据。
6. US5 → 冻结基线消费侧预检。
7. US6 → 载体开放 + gate 逐字引用。
8. Polish → 重编译收口、分发同步、全局回归、quickstart、SC 收口、Feature 状态。

### Parallel Team Strategy

- 单执行者为主：各 story 的编辑面互斥，理论可并行；但 `verification.md` 与固定次序（compile → regen → sync）把 Polish 串行化。
- 关键串行点：T026 → T027（manifest 先于渲染器）；T027/T032 → T044（注册表稳定后重编译）；T044 → T045 → T046..T049。

---

## Notes

### Clause partition (each clause claimed exactly once)

| Contract | Claiming row | Clauses |
|----------|--------------|---------|
| `contracts/template-mechanisms.md` | T011 (US1) | C-1, C-2 |
| `contracts/template-mechanisms.md` | T012 (US1) | C-3, C-4 |
| `contracts/template-mechanisms.md` | T013 (US1) | C-5, C-6, C-7 |
| `contracts/template-mechanisms.md` | T014 (US1) | C-8, C-9, C-10 |
| `contracts/template-mechanisms.md` | T022 (US2) | C-11..C-15 |
| `contracts/template-mechanisms.md` | T043 (US6) | C-16..C-19 |
| `contracts/engine-face-contract.md` | T028 (US3) | C-20..C-24 |
| `contracts/engine-face-contract.md` | T044 (Polish) | C-25 |
| `contracts/evidence-baseline-contract.md` | T033 (US4) | C-26, C-27, C-28 |
| `contracts/evidence-baseline-contract.md` | T038 (US5) | C-29, C-30 |
| `contracts/cross-cutting-constraints.md` | T045 (Polish) | C-31 |
| `contracts/cross-cutting-constraints.md` | T046 (Polish) | C-32 |
| `contracts/cross-cutting-constraints.md` | T048 (Polish) | C-33 |
| `contracts/cross-cutting-constraints.md` | T049 (Polish) | C-34 |

Total: 34 clauses, each claimed exactly once. 分区随行序使每份契约的条款序号单调递增；C-25 在 Polish 收口（全单元重编译须等全部注册表编辑落位，见 D-T2）；C-19 的编辑与 C-16/C-18 同文件同批（D-T1），其 story 归属不变（FR-024 → C-19，per `feature-ref.md` FR→clause map）。

### Assumptions and decisions

- **D-T1 (2026-10-19; C-19 同文件归并)**: FR-024/C-19（re-freeze timing 指向消费侧）的实现行放入 US6 的 T041，与 C-16/C-18 同为 `skills/internal/create-tasks/SKILL.md` 的三节一次写入（一文件一写入者；并保持 template-mechanisms.md 的条款认领序 15 → 16..19 单调）。story 归属不受影响：F7 的 traceability 以 `feature-ref.md` 的 FR-024 → C-19 为准。
- **D-T2 (2026-10-19; C-25 收口点)**: 全单元重编译 + backlog 翻转放 Polish（T044），不在 US3 内做——US4 的 gate 行（T032）同样改动注册表投影，US3 内重编译会被再次打破；C-25 的触发条件「渲染器/注册表变更落位后」以 T044 的 blockedBy（T027,T032）机械表达，backlog 翻转的「同一提交」义务写在行内。
- **D-T3 (2026-10-19; C-12 活动面时点)**: `generate-instructions.sh` 在 US2 内运行（T018）使 C-12 在其 story 内转绿；Polish T045 仅作终态再确认（生成器幂等）。
- **D-T4 (2026-10-19; owner-file 订正承继)**: 承 research D-9/D-10 的两处对码订正——C-18 的 red-first note 形态 owner 是 `skills/internal/create-tasks/SKILL.md`（FR-025 原文的条件指称无实指）；C-27 的技能侧锚点是 implement Step 9（技能无 per-feature GATE-8 编号）。两处均已回写契约条款，任务行按订正后 owner 落点。
- **D-T5 (2026-10-19; 生成期冻结记录)**: 本 tasks 生成阶段实际重冻/首冻两项测量——`notes/baseline-failed-tests.txt` 重捕获 63 名（`git diff` 与 plan 阶段冻结集合逐一相等，见 § measured premises）；`coverage-baseline.txt` 首冻（FR-004 首次全树核算，base-sha `bf88f2c63857`）。implement 开工时树若已前进，按 C-29 预检重捕获并把新值写回引用行（MUST NOT 沿用过期冻结值）。
- **D-T6 (2026-10-19; MVP)**: MVP = US1，依据 requirements § User Story 1 的 Why this priority（F1/F2 同根、直接决定 analyze 门可信度）。

### Measured premises (commands actually run at generation time, 2026-10-19)

- 条款普查: `clause_extract`（`**C-N**:` 声明形）→ `template-mechanisms.md 19 (C-1..C-19)`、`engine-face-contract.md 6 (C-20..C-25)`、`evidence-baseline-contract.md 5 (C-26..C-30)`、`cross-cutting-constraints.md 4 (C-31..C-34)`、`TOTAL 34`，四文件 form 均 `md-bold-closed`（陷阱：按「含 C- 数字样」计数会把 traceability 表与散文提及算进去；唯一合法计数单位是行首声明形）。
- FR / SC: `grep -cE '^\- \*\*FR-[0-9]{3}\*\*:' requirements.md` → `30`；同形 SC → `14`。
- 失败测试基线: `bash scripts/bash/run-tests.sh --names-out .specify/specs/063-review-p1-governance/notes/baseline-failed-tests.txt` → `63 failed, 3954 passed`（163.32s，exit 0）；`wc -l` → `63`；`sort -c` 通过；`git diff -- <该文件>` 为空（与 plan 阶段冻结**集合逐一相等**，非仅计数相等）。陷阱：名字级比较形态是排序后 `comm -13`（owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs）；`wc -l` 计数相等不蕴含集合相等，本代以 `git diff` 空证明集合相等。
- 镜像漂移: `python3 scripts/python/sync-mirrors.py --check` → **202 条既有 DIFF**（`grep -c '^DIFF'` 计数；含本特性触碰对 `shared/workflow/feature-integration.md`、`feedback-step.md`）；判据 = 零 NEW，触碰对经 T045 sync 清除。
- regen copies: `python3 scripts/python/regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.`
- compile face: `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` → `74 units, zero drift`（改前干净态；C-25 重编译后回到零漂移）。
- register: `grep -c "REC-" .specify/memory/register.md` → `0`（前向机制的起点事实）。
- backlog: `.specify/memory/feedback/backlog.md` 第 89 行实测为 `2026-10-15 | introspection-20261015T081832Z#F-01… | direct-fix | … | open(修复须同步全部编译单元重编译 + --reconcile 收口…) | —`，与 C-25 的翻转前提一致。
- 覆盖通道: `python3 .specify/scripts/python/account-clause-coverage.py --spec .specify/specs/063-review-p1-governance` → `FR universe: 30 / FR claimed: 30 / FR uncovered: 0`，`status: baseline-missing`（首冻前）；`find .specify/specs -name coverage-baseline.txt` → 冻结前仅 `053-machine-decidable-artifacts`。
- 覆盖基线首冻: `python3 .specify/scripts/python/account-clause-coverage.py .specify/specs/063-review-p1-governance --freeze > .specify/specs/063-review-p1-governance/coverage-baseline.txt` → exit 0，497 行，`base-sha bf88f2c63857`（语料排除 063 自身契约；陷阱：该文件比较须 `LC_ALL=C comm -13`——文件头自述 glibc collation 下 locale 差异会使 comm 误报全量 delta）。
- gate 注册形锚点: `shared/definitions/probe-definitions.md` L117 `| gate-implement-checklist-waiver | command-gate | /speckit.implement | … |`；`h-gate-evidence` 绑定行形 `| h-gate-evidence | @point:confirm-gate | <gate-id> | … |`（T032 按此同形落 [[STR-001]]）。
- 任务面: 51 任务行（Setup 1 · US1 13 · US2 8 · US3 6 · US4 5 · US5 5 · US6 5 · Polish 8），`[P]` 24 项，`[green:]` 34 处（= C-1..C-34 每条款恰一次）。

### Runtime-evidence landing points

- `.specify/specs/063-review-p1-governance/notes/red-first-evidence.md` — T005/T016/T025/T030/T035/T040 记录各自红命令、真实输出与退出码。
- `.specify/specs/063-review-p1-governance/notes/quickstart-run.md` — T047 记录 S1–S10 实跑与 teardown。
- `.specify/specs/063-review-p1-governance/notes/pre-change-measurements.md` — T001 记录每个 diff 前提的改前侧（命令 + 日期 + 真实输出）。
- `.specify/specs/063-review-p1-governance/verification.md` — 验证行 T011–T014、T022、T028、T033、T038、T043、T044–T050 记录行为、结构与 SC 证据。
- `.specify/specs/063-review-p1-governance/coverage-baseline.txt` — 本生成阶段首冻（2026-10-19）；生产侧冻结义务 owner 为 C-6（create-tasks SKILL，T008 落位），消费侧 owner 为 C-5/C-29。
- 失败测试基线的路径、捕获旗标与名字级比较形态 owner：`.specify/skills/internal/implement-feature/SKILL.md` § Test runs；本文件只具名 feature 冻结名单，不复述其程序。
