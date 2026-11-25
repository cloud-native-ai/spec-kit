# Analyze Repair Record — 107-decision-governance（round 2，2026-11-26）

- **Stage**: analyze（round-2 gate FAIL 后的修复轮）· **Line**: `decision-governance` · **Branch**: `107-decision-governance` · 单写者
- **Dispatch**: SDD Analyze-Repair Executor（round 2）。不派发子代理、不写状态脊、不实现、不 push。
- **Input**: `test-evidence/analyze-domain-w{1,2,3}-r2.jsonl` 中 validator 确认的 2 条 HIGH：**R2-W1-01 / R2-W1-02**（R2-W2-01 同源，见 § 1 末）。
- **Scope**: 仅上述触发项的最小一致修复及相邻指针；其余 round-2 发现（R2-W1-03…W1-06、R2-W2-02…W2-06、R2-W3-01…W3-06）不在本轮触发范围，维持 analyze 报告归属（见 § 5）。
- **Gate captures**: `analyze-repair2-validate-requirements.txt`、`analyze-repair2-pre-analyze-{requirements,plan,tasks}.txt`、`analyze-repair2-validate-tasks.txt`、`analyze-repair2-decomposition.txt`、`analyze-repair2-readings.txt`（均在本目录）。

## 1. Finding → Change → Evidence（2/2 fixed）

| Finding | Sev | Disposition | 改动（文件:位置） | 证据 |
|---------|-----|-------------|-------------------|------|
| R2-W1-01 | HIGH | **fixed** — 记录文法改为**分层封闭**：基础层 10 字段（每条记录必填）+ 条件层三族（同名族 `same_name_conflict`/`resource_locator`；取代族 `superseded_by`；传递族 `dispatched_at`/`acknowledged_at`/`implemented_at`），两层之外无顶格字段；Field Ownership 表逐层枚举（10 基础 + 8 条件 + 1 维度行），回传项 `acknowledgement` / `implementation_receipt` 以「条件层：传递族（回传项）」两行登记为非记录字段 | `requirements.md` FR-014（分层文法本体）、FR-002（两层全部字段）、FR-015/Edge Case（`superseded` 标记由 `superseded_by` 在场表达）、FR-016（按适用层重建）、FR-022（M-01 新表述）、§ Decision Record Field Ownership（(closed) → (closed at each layer)，新增 Layer 列，19 行）、§ Enforcement Boundary M-01/M-02、§ Key Entities、§ Clarifications 2026-11-26 第二轮（3 条裁决）；`contracts/archive-and-audit.contract.md` C-202；`contracts/enforcement-boundary.contract.md` C-401 M-01/M-02；`data-model.md` E2（Layer 列 16 行 + field-closure 权威段 + I-03）、E1 一句；`tasks.md` T023/T026/T029、DoD-4、US3 Goal/Independent Test、Phase 5 Checkpoint；`checklists/decision-governance-2026-11-26.md` CHK011/CHK014；`research.md` R-1(6)/R-2/Open questions(a)；`quickstart.md` Scenario 1 | `analyze-repair2-readings.txt`：base 10 / 同名 2 / 取代 1 / 传递 3（+回传项 2）/ 维度 1，表行合计 19；FR-014 基础枚举 10 项；data-model E2 16 行；`analyze-repair2-validate-requirements.txt`（0/0） |
| R2-W1-02 | HIGH | **fixed** — 时点义务按**适用层与 [[STR-007]] 相位**条件在场：`created_at` 每条必填；传递族三时点仅传递决策携带，各按 `dispatched` / `acknowledged` / `implemented`·`diverged` 相位追加，未到相位不设占位（撤销 `not-yet` 字面量，单一表示、无二义）；`blocked` 按已达相位判；非传递记录只带 `created_at` 且 `transmission_status` 取 `not-transmitted`；M-01、Field Ownership 表、data-model E2、C-202、SC-005 同步按相位判 | 与 R2-W1-01 同一编辑面（FR-014 传递族、Field Ownership 传递族三行、M-01 行、data-model E2 三时点行与 closure 段、C-202、SC-005/US3 适用层读数、research/quickstart/tasks 对应句） | 同上；stale sweep（`四个时点必须齐全` / `four timestamps` / `ten mandatory fields` / `three conditional fields`）在 live artifacts 零命中（见 readings） |

**同源收口（不重分类，仅披露）**：`R2-W2-01`（data-model E2 的字段闭包声明与其表不一致：14 行中三个时间点与 `transmission_status` 未归类、同名对不在表）是触发项同一次缺陷在 plan 投影面的表现；本轮触发指令要求「align … data-model.md E2 and the contracts that restate the record shape」，该矛盾已随同一编辑消除。它未被计入本轮 2 条触发，也不登记为第 3 条修复。

**连带收口（披露）**：`R2-W1-03(b)`（`transmission_status` 闭集取值无 M 承接）——相位判定要可判定，守卫必须能识别状态值，故 M-01 转红条件新增「[[STR-007]] 值域外」；该发现在本轮关闭，但 `R2-W1-03(a)`（确认在场无 M 承接）未动，仍在 analyze 报告名下。

**in-passing corrections（披露）**：① Field Ownership 原「options / chosen option」合并行拆为两行，使基础层表行与 FR-014 的 10 字段逐一对应；该行原挂的「承重决策的理据由 `T-NNN` 承载」说明移至 `rationale` 行（原位属误挂）。② `superseded` 标记统一由 `superseded_by` 在场表达，不为二值标记新增布尔字段。③ `data-model.md` E1 增一句：同名对归档时走 E2 的同名族。

## 2. PLAN-EDIT（plan-owned 变更逐条声明）

- `PLAN-EDIT: .specify/specs/107-decision-governance/data-model.md — E2 改为分层表（base 10 + 同名/取代/传递条件族，16 行），重写 field-closure 权威段，I-03 改为分层在场义务; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/archive-and-audit.contract.md — C-202 由「十个必填 + not-yet 占位」重写为分层闭包与相位时点（回传项非记录字段）; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/enforcement-boundary.contract.md — C-401 M-01 转红条件改为「基础层缺失/条件族触发缺失/类值域外/[[STR-007]] 值域外/时点形态或相位不符」，M-02 标注条件层同名族; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/transmission-and-implementation.contract.md — C-303/C-304 增确认与回执对 acknowledged_at/implemented_at 及状态相位的驱动义务（指针回 C-202）; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/research.md — R-1(6)/R-2/Open questions(a) 同步分层闭包与相位时点，删除 not-yet 占位读法; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/quickstart.md — Scenario 1 的记录书写步骤改为分层文法（base + 条件族；传递时点按相位追加）; classification=minor`

非 plan-owned 的相邻改动（不属 PLAN-EDIT，逐条披露）：`requirements.md`（两条修复本体 + § Clarifications 2026-11-26 第二轮三条裁决）、`tasks.md`（T023/T026/T029、DoD-4、US3、Phase 5 Checkpoint）、`checklists/decision-governance-2026-11-26.md`（CHK011/CHK014 改写为修复后形态）。`plan.md` 未触碰（其 M-01…M-09 计数与抽象表述仍成立）；`.specify/features/107-decision-governance.md`、`.specify/register.md`、`handoff.md`、`feature-ref.md`、`team.md` 未改。

## 3. 门禁复跑（2026-11-25T16:35Z；逐字捕获见 § header）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/107-decision-governance/requirements.md` | `status: ok`；六项全 pass；`scanned: 416 lines, 40 definition rows, 9 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage requirements --repo .` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 5 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/107-decision-governance/tasks.md` | `PASS — 0 error(s), 0 warning(s)`，exit 0 |
| 6 | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `decision=proceed`；fr_count=30 / task_count=56（ceiling 120/160），exit 0 |

- advisory 构成（tasks 阶段，127 条）：`external-clause` 48（BC-xx 外部命名空间，与修复轮前同型）+ `missing-path` 79（实现阶段才创建的交付路径），与本轮 round-1 基线同值，无 error。
- 确定性计数（`analyze-repair2-readings.txt`）：M 9 / B 6 / P 12 / BC 6 / 契约条款 38 / Field Ownership 19 行（10+8+1）/ data-model E2 16 行。

## 4. 纪律与保全

- **单一真相**：FR-014 是记录文法的唯一需求定义点（Field Ownership 是它的字段→所有者投影；data-model E2 与 C-202 以指针抵达，不另立取值域）。条件层按**触发族封闭**：同名族 / 取代族 / 传递族，每族成员逐一枚举；两层之外无顶格字段。
- **封闭集**：M 表 9 行、B 表 6 行、P 清单 12 行、BC 清单 6 行、STR 表 9 行、契约 38 条款均未增行；SC 未增删；本轮改动全部是既有行/段的修订。
- **受保护面**：`.specify/register.md` 零改动；dated 记录（`analyze-domain-w*-r2.jsonl`、`analyze-repair-2026-11-26.md`、各 checkpoints、既有 `T-NNN` 段）均未改写；其它规格未触碰。
- **fast-fail**：未发现异常（无 ANOMALY 事项）；上述 in-passing corrections 与同源/连带收口均为披露项，非静默处置。
- **push**：未 push、未联系远端。

## 5. 残余风险

1. `R2-W1-03(a)`（子代理回传的确认在场无 M 规则承接；M-05 只判回执在场与 `decision_id`）仍在 analyze 报告名下；本轮只关闭了 (b) 的状态值域。
2. `forced` / `other.path` / 人的选择信号被登记为 `options` / `chosen option` 的值形状成员（FR-014、Field Ownership），但 M-03 的转红条件枚举仍未点名「单可行选项未声明 `forced`」，而 tasks T018 独立测试期望该形态令 M-03 转红——实现期须二者取一：扩展 M-03 的转红条件（须同步 C-401 与 C-107 面）或在 T018 改判；不在本轮触发范围。
3. `R2-W1-05`（生产者清单的两个修订载体无优先级）、`R2-W2-02`（确认/张力副本/取代保留三条测试无 guard 名册行）、`R2-W2-03`（回执四成员的 M-05 承接）与其余 MEDIUM/LOW 未动。
4. 撤销 `not-yet` 占位后，记录一经写出即按事件追加时点；实现期若需要「已派发但未确认」的事前记录，应写 `transmission_status: dispatched` + `dispatched_at`，不得引入新的占位字面量（Clarifications 2026-11-26 第二轮）。
