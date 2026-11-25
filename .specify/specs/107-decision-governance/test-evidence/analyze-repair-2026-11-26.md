# Analyze Repair Record — 107-decision-governance（round 1，2026-11-26）

- **Stage**: analyze（gate FAIL 后的修复轮；一轮为限）· **Line**: `decision-governance` · **Branch**: `107-decision-governance` · 单写者
- **Dispatch**: SDD Analyze-Repair Executor（round 1）。不派发子代理、不写状态脊、不实现、不 push。
- **Input**: `test-evidence/analyze-domain-w{1,2,3}.jsonl` 中 validator 确认的 5 条 HIGH：**W1-01 / W1-02 / W2-01 / W2-02 / W3-01**。
- **Scope**: 仅上述 5 条 HIGH 的最小一致修复及相邻指针；其余 MEDIUM/LOW（W1-03…W1-06、W2-03…W2-06、W3-02…W3-06）不在本轮触发范围，维持 analyze 报告归属（见 § 5）。
- **Gate captures**: `analyze-repair-validate-requirements.txt`、`analyze-repair-pre-analyze-{requirements,plan,tasks}.txt`、`analyze-repair-validate-tasks.txt`、`analyze-repair-decomposition.txt`、`analyze-repair-readings.txt`（均在本目录）。

## 1. Finding → Change → Evidence（5/5 fixed）

| Finding | Sev | Disposition | 改动（文件:位置） | 证据 |
|---------|-----|-------------|-------------------|------|
| W1-01 | HIGH | **fixed** — 新增机器规则 **M-09**（evidence 指针可解析），封闭 M 表扩为 M-01…M-09；折叠进 M-01 的读法被拒并记录理由 | `requirements.md` FR-016（M-09 指针）、FR-022（M-09 枚举 + M-04 新式记录范围）、§ Enforcement Boundary（新增 M-09 行）、SC-005（指针破坏 → M-09，`decision_id` 不可解析 → M-04）、SC-005 Source（M-09 输出）、§ Clarifications 2026-11-26（裁决记录）；`contracts/enforcement-boundary.contract.md` C-401（nine rules + M-09 行）；`checklists/decision-governance-2026-11-26.md` CHK017/CHK025/头部与 Notes 计数；`plan.md` Summary/Scale、`research.md` R-3/R-8、`tasks.md` Prerequisites/DoD-3/T003/T040/Measured Premises 计数、`feature-ref.md`、`.specify/features/107-decision-governance.md` | `analyze-repair-readings.txt`（M rows: 9）；`analyze-repair-validate-requirements.txt`（0/0）；`analyze-repair-validate-tasks.txt`（PASS 0/0） |
| W1-02 | HIGH | **fixed** — 区分「决策记录（类别看持有者）」与「传递/实施回执（非第二条记录）」：P-09 类列改为随被传递记录的类别，义务明确不含第二条记录；FR-018 增类别一致性；A-4 增「传递不改变类别」 | `requirements.md` A-4、§ Decision Producer Inventory P-09 行、FR-014（一条决策项恰一条记录，回执只更新状态与审计链）、FR-018（`decision_class` 与被传递记录一致）、§ Clarifications 2026-11-26；`data-model.md` E4（类别从源记录复制）与 E6（回执不是第二条记录）；`checklists/decision-governance-2026-11-26.md` CHK037（改写为已调和形态） | 同上 |
| W2-01 | HIGH | **fixed** — C-502 验收读数由「文件级空 diff」重述为**行级包含**：既有记录路径 `git diff --numstat` 删除列 = 0 且 `--diff-filter=D` 为空，追加与新增文件允许且属预期；contract/plan/quickstart/requirements 同读法 | `contracts/migration-and-compat.contract.md` C-502；`plan.md` EP-006（证据重述）、BC-01/BC-05（`--numstat` 零删除读数）；`quickstart.md` Scenario 5（命令、执行读数、M-09 映射）；`requirements.md` SC-009 正文与 Measurement Source、US6 Independent Test；`tasks.md` GATE-7 与 § Notes 补 `--numstat` 读法 | `analyze-repair-readings.txt`：`3 0 .specify/register.md`；checkpoints 与 `plan.md` 均为新增文件、删除列 `0`；`--diff-filter=D` 空 |
| W2-02 | HIGH | **fixed** — 新式记录定义收紧为「`^### D-\d{3}` 标题 **且** 携带 C-201 记录字段文法」；id 形态本身永不使记录成为新式（`D-001` 等 register 行仍是 legacy）；M-04 只判新式记录 | `contracts/archive-and-audit.contract.md` C-206（精确定义 + 完整 legacy 清单）、C-204（映射 M-09）；`requirements.md` FR-022 M-04 与 § Enforcement Boundary M-04 行；`research.md` M-10 与 R-2；`plan.md` BC-01/BC-03；`data-model.md` I-13；`tasks.md` T024/T029（判别式含 `D-001`） | 同上 |
| W3-01 | HIGH | **fixed** — 收口产物所有权拆分：crew 写 `test-evidence/verification-input.md`；`verification.md` 由 spec 侧派生、对 crew 保持禁止 | `tasks.md` T056（改写）、DoD-1/DoD-8、Task State Sigil、§ Path Conventions 证据落点、Phase 9 Checkpoint；`handoff.md` § Task Reference 与 § Territory 禁止面注记；`.specify/teams/107-decision-governance/team.md` § Dynamic Structure（crew 可写输入 / `verification.md` 派生）；`plan.md` § Documentation 树的 `verification.md` 注记 | `analyze-repair-validate-tasks.txt`；`analyze-repair-pre-analyze-tasks.txt` |

**未处置（显式维持，属下一轮/既有归属）**：W1-03（decision-backed 派发的识别标记）、W1-04（五要素上行是否扩展）、W1-05（无人值守 blocked 姿态的 FR 锚点）、W1-06（跨载体同号语义与密度单位）、W2-03（确认/回执缺项的 M 承接）、W2-04（十个必填字段 vs 十三条非条件行）、W2-05（M-08 触发输入）、W2-06（R-3 的 three actions 笔误）、W3-02（writeback 记录无任务行）、W3-03（`[P]` 闭集漏 T018）、W3-04（territory 两份副本）、W3-05（C-102 四面对表述）、W3-06（GATE-8 不匹配 `[~]`）。其中 W2-03/W2-04 与 M 表相邻，但不在本轮 5-HIGH 触发内，未顺手改动。

## 2. PLAN-EDIT（plan-owned 变更逐条声明）

- `PLAN-EDIT: .specify/specs/107-decision-governance/plan.md — M 规则计数 8→9（M-01…M-09）随 W1-01 对齐（Summary / Scale/Scope）；W2-01 重述 EP-006 与 BC-01/BC-05 的零改写读数为行级包含；W2-02 收紧 BC-01 新式记录定义、BC-03 标注 D-001 为 legacy register 行；W3-01 注记 verification.md 派生来源; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/enforcement-boundary.contract.md — C-401 增补 M-09 规则行（唯一判定器 + 转红条件 + 逆向样本 fixtures/m09/*），M-04 转红范围收窄为新式记录; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/archive-and-audit.contract.md — C-204 标注 M-09 判定；C-206 精确定义新式记录（标题 + 字段文法）并把 D-001/D-001-a/D-098-01/D-102-01 归为 legacy register 行; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/migration-and-compat.contract.md — C-502 验收读数由文件级空 diff 重述为行级包含（--numstat 删除列 0 + --diff-filter=D 空；追加与新增文件允许）; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/quickstart.md — Scenario 5 改为 --numstat 行级包含命令与实测读数，指针破坏映射 M-09; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/research.md — M-10/R-2 判别式补「id 形态单凭 D-001 不判新式」；R-3 records 动作增 M-09；R-8 计数 M-01…M-09; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/data-model.md — E4 补 decision_class 从源记录复制（传递不改类别）；E6 补回执非第二条记录；I-13 判别式精确化; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/feature-ref.md — checker 行 M-01…M-09（计数对齐）; classification=minor`

非 plan-owned 的相邻改动（不属 PLAN-EDIT，逐条披露）：`requirements.md`（5 条修复本体 + § Clarifications 2026-11-26 三条裁决）、`tasks.md`、`checklists/decision-governance-2026-11-26.md`（CHK017/CHK025/CHK037 与计数，按 W1-01/W1-02 的「checklist note 一致性」要求）、`handoff.md`、`.specify/teams/107-decision-governance/team.md`、`.specify/features/107-decision-governance.md`（M-01…M-09 三处，生命周期状态未动）。

## 3. 门禁复跑（2026-11-25T16:20Z；逐字捕获见 § header 所列文件）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/107-decision-governance/requirements.md` | `status: ok`；六项全 pass；`scanned: 401 lines, 40 definition rows, 9 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage requirements --repo .` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 5 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/107-decision-governance/tasks.md` | `PASS — 0 error(s), 0 warning(s)`，rc=0 |
| 6 | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `decision=proceed`；fr_count=30 / task_count=56（ceiling 120/160），exit 0 |

- advisory 构成（tasks 阶段，127 条）：`external-clause` 48（BC-xx 外部命名空间，与 plan/tasks 修复轮同型）+ `missing-path` 79（implement 阶段才创建的交付路径，含新增的 `fixtures/m09/*` 与 `verification-input.md`）。较 checklist 阶段的 120 条增加 7 条，全部为上述 `missing-path` 预期项，无 error。
- 确定性计数（`analyze-repair-readings.txt`）：M 9 / B 6 / P 12 / BC 6 / 契约条款 38 / 清单条目 39。

## 4. 纪律与保全

- **单一真相**：M-09 只有一个定义点（requirements § Enforcement Boundary 与 owner page 的契约镜像，后者在实现期由 T040 写入）；requirements 与 enforcement 契约逐行一致（C-407 的表—守卫等价义务不变）。
- **封闭集**：M 表由 8 行扩为 9 行是**修订**而非泄漏；B 表、P 清单、BC 清单、STR 表均未加行。SC-005 的读数重新映射到 M-09，未新增 SC。
- **受保护面**：`.specify/register.md` 零改动；`T-NNN` 段落、检查点、其它规格、dated 报告（`analyze-domain-w*.jsonl` 等）均未改写；`.specify/features.md` 未改（107 行描述无 M 计数）。
- **in-passing corrections（披露）**：① `requirements.md` SC-009 正文/来源与 US6 Independent Test 同带「空 diff」读法（未列入 5 条 finding 的 locations），按 FR-028 的已记录意图（零改写 ≠ 零新增）一并对齐为行级包含；② `data-model.md` I-13 沿用「non-D-NNN forms」措辞，属 W2-02 同一判别式缺陷的相邻副本，一并对齐；③ `.specify/features/107-decision-governance.md` 的 M-01…M-08 三处摘要随 W1-01 对齐（状态行未动）。
- **workspace guard**：收口前以 `workspace-guard.py --snapshot` 记录并 `--check` 复核（见 § 6）。
- **push**：未 push、未联系远端。

## 5. 残余风险

1. 本轮只处置 5 条 HIGH；13 条 MEDIUM/LOW 仍在 analyze 报告名下（列表见 § 1 末段）。其中 **W2-03**（确认与回执缺项无 M 承接）与 **W2-04**（FR-014 十字段 vs data-model 十三条非条件行）与 M 表相邻，下一轮若要求全量处置应与 M-09 一并设计，避免再改表。
2. M-09 目前只存在于规格与契约；owner page（`shared/definitions/decision-definitions.md`）与检查器在实现期落（T040/T029 已含 M-09）。若实现漏落，C-407 表—守卫等价会在测试面转红。
3. **两个 base 并存**：requirements SC-009 使用 `fbab7a45c`（requirements 阶段基线），C-502/EP-006 使用 `08b59695c`（plan 阶段基线）。两者各自是阶段时点读数，本轮未统一（未列入 finding）；实现期的零改写测试须以 C-502 的 `08b59695c` 为准并在 review 复核。
4. checklist 的 CHK017/CHK025/CHK037 已改写为修复后形态；原始「缺口」表述保留在 `analyze-domain-w1.jsonl`（dated 证据），两处并存属预期。
5. `quickstart.md` Scenario 5 的读数是修复时点实测；实现/review 时按同一 `--numstat` 口径重测，数值会随合法追加变化，判据不变（删除列 0 + 无删除文件）。
