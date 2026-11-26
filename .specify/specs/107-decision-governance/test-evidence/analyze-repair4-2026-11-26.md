# Analyze Repair Record — 107-decision-governance（round 4，final，2026-11-26）

- **Stage**: analyze（round-4 增量复检后的修复轮）· **Line**: `decision-governance` · **Branch**: `107-decision-governance` · 单写者
- **Dispatch**: SDD Analyze-Repair Executor（round 4, final）。不派发子代理、不写状态脊、不实现、不 push。
- **Input**: `test-evidence/analyze-incremental-r4.jsonl` 中 validator 确认的 **R4-01（HIGH）** 与同面的 **R4-02 / R4-03（MEDIUM）**。
- **Scope**: 仅上述三项的最小一致修复及相邻指针；R4-04（low，判别式字段名归属）与 R4-05（low，SC-008 覆盖矩阵缺 T043/T054）不在本轮触发范围，维持 analyze 报告归属（见 § 5）。
- **Gate captures**: `analyze-repair4-validate-requirements.txt`、`analyze-repair4-pre-analyze-{requirements,plan,tasks}.txt`、`analyze-repair4-validate-tasks.txt`、`analyze-repair4-decomposition.txt`、`analyze-repair4-readings.txt`、`workspace-analyze-repair4.json`（均在本目录）。

## 0. 选定读法（两选一，取推荐支）

**R4-01 统一为「允许差异集恒为空 + 裁定 = 重定基线」**：允许差异集**无条件为空集（∅）**，与是否存在裁定无关；一条记录在案的裁定不扩宽差异集，而是把**有效基线**更新为被裁定改动后的状态，此后补集断言照原样适用于新基线。集合之内无成员，故结构不变量一侧**空真**（显式声明为 vacuous，而非豁免）。另一支（裁定授权具名差异集 + 集合内结构不变量）被拒：它把「裁定」变成第二种验收形态，需为每个裁定再发明不变量，且与 C-405 的既有读法相反。

## 1. Finding → Change → Evidence（3/3 fixed）

| Finding | Sev | Disposition | 改动（文件:位置） | 证据 |
|---------|-----|-------------|-------------------|------|
| R4-01 | HIGH | **fixed** — FR-025 ② 由「允许差异集在无裁定时为空（暗示裁定可使其非空）」统一为 **恒为空集（∅）**，裁定改为**重定基线（re-baseline）**：基线参照物改写为**有效基线**（缺省 `fbab7a45c`，仅由记录在案的重定基线裁定更新为「引入该裁定记录的同一提交」）；读数 = `git diff --quiet <有效基线>..HEAD -- <三路径>` rc 0（`--numstat` 零行）；补集断言照原样适用于新基线；集合之内空真、不承载豁免。C-405、SC-008、SC-008 Source、US5 场景 4 与 CHK028 同步为同一读法 | `requirements.md` FR-025、SC-008、SC-008 Source、US5 场景 4、§ Clarifications 第四轮；`contracts/enforcement-boundary.contract.md` C-405；`checklists/decision-governance-2026-11-26.md` CHK028（问题文本 + pass 注记续期） | `analyze-repair4-readings.txt` § R4-01：`恒为空集（∅），与是否存在裁定无关` / `重定基线` 逐面在场；`unconditionally empty` 于 C-405；三路径 diff-quiet rc 0、numstat 0 行 |
| R4-02 | MEDIUM | **fixed** — 裁定两形态收敛为**唯一形态**：符合 FR-014 与 FR-015 的 `D-NNN` 决策记录（编号与登记语义按 FR-015），载体为阶段检查点 `<spec-dir>/checkpoints/<NN>-<stage>.md`（生产者 P-04，清单内可满足）；裁定 MUST 与被执行裁定的改动**同提交落盘**，逐一具名被改字面量/行为、新值与理由，并钉定后继基线为引入该裁定记录的同一提交。「改动面所属生产者载体」支（对三受保护产物不可满足）与「不要求 FR-014/015 合规的具名裁决」支一并删除 | `requirements.md` FR-025（裁定形态（唯一））、§ Clarifications 第四轮；`contracts/enforcement-boundary.contract.md` C-405 | `analyze-repair4-readings.txt` § R4-02：live 两面形态残留 0（排除日期性 Clarifications）；`裁定形态（唯一）` 1 处 |
| R4-03 | MEDIUM | **fixed** — 无裁定的受保护产物改动获得封闭承接行 **B-07**（保全裁定充分性）：承接面 `/speckit.analyze` + `/speckit.review` 产物段，不声称机器覆盖；FR-025 的缺陷措辞改由 B-07 承接。封闭 B 表扩为 B-01…B-07（先例：第二轮新增 M-09），FR-023、§ Enforcement Boundary、C-402、tasks / plan / checklist / feature detail 的 B 名单指针全量同步 | `requirements.md` FR-023、§ Enforcement Boundary 表、FR-025；`contracts/enforcement-boundary.contract.md` C-402；`contracts/text-and-options.contract.md` 条款指针；`tasks.md`（Prerequisites、DoD-3、Phase 7 Independent Test、T039/T040/T041）；`plan.md`（Scale/Scope + 3 指针行）；`checklists/decision-governance-2026-11-26.md`（CHK026、头部/页脚计数注记）；`.specify/features/107-decision-governance.md`（4 处 B 名单） | `analyze-repair4-readings.txt` § R4-03：B rows 7；`^| B-07` 1 行；C-402 `seven behavior rules`；B-01…B-07 指针 sweep |

**in-passing corrections（披露，非触发项）**：① `contracts/text-and-options.contract.md` 末行原引「B-01…B-06 行」，随 B 表扩行同步为 B-01…B-07（纯指针，无条款内容变化）；② `checklists/decision-governance-2026-11-26.md` 的头部计数与页脚「机械读数」行按既有惯例**追加注记**（`7 B（第四轮加入 B-07）`），不改写任何既有日期性读数；③ `.specify/features/107-decision-governance.md` 的 B 名单四处同步（承第一轮把 M-01…M-08 修为 M-01…M-09 的同型动作）。

## 2. PLAN-EDIT（plan-owned 变更逐条声明）

- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/enforcement-boundary.contract.md — C-405 由「基线恒为 fbab7a45c + 裁定为例外」改写为「有效基线缺省 fbab7a45c、仅由重定基线裁定更新 + 允许差异集无条件为空 + 集合内空真」并收敛裁定形态为唯一（FR-014/FR-015 checkpoint D-NNN，同提交）；C-402 由六条 B 规则扩为七条并登记 B-07 承接面; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/text-and-options.contract.md — 末行 B 名单指针 B-01…B-06 → B-01…B-07; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/plan.md — § Constraints 的 FR-025 保全约束改为有效基线读法；Scale/Scope 的 6 behavior rules → 7 (B-01…B-07)；analyze-artifacts 与 review 技能指针行 B 名单同步; classification=minor`

非 plan-owned 的相邻改动（不属 PLAN-EDIT，逐条披露）：`requirements.md`（三条修复本体 + § Clarifications 第四轮三条裁决）、`tasks.md`（Prerequisites、DoD-3、Phase 7 Independent Test、T039/T040/T041、T043/T054 读数改为有效基线口径）、`checklists/decision-governance-2026-11-26.md`（CHK026/CHK028 + 计数注记）、`.specify/features/107-decision-governance.md`（B 名单四处）。`plan.md` 的 BC 行集合、M/B/P/BC/STR 行数（B 由 6 扩为 7 是唯一增行）、SC 与 FR 集合均未增删；`.specify/register.md`、`handoff.md`、`feature-ref.md`、`quickstart.md`、`research.md`、`data-model.md`、`team.md`、`.specify/features.md` 未改。

## 3. 门禁复跑（2026-11-26T02:06–02:07Z；逐字捕获见 § header）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/107-decision-governance/requirements.md` | `status: ok`；六项全 pass；`scanned: 428 lines, 40 definition rows, 9 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage requirements --repo .` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 5 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/107-decision-governance/tasks.md` | `PASS — 0 error(s), 0 warning(s)`，exit 0 |
| 6 | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `decision=proceed`；fr_count=30 / task_count=56（ceiling 120/160），exit 0 |

- advisory 构成与 round-3 基线一致：`external-clause` 48 + `missing-path` 79 = 127，无 error。
- 确定性计数（`analyze-repair4-readings.txt`）：M 9 / **B 7** / P 12 / BC 6 / FR 30 / SC 10 / STR 9 / 契约条款 38 —— 唯一变化是 B 6→7（新增 B-07，显式封闭集扩行，非漂移）。

## 4. 纪律与保全

- **单一真相**：FR-025 是保全 claim 的唯一需求定义点；C-405、SC-008、SC-008 Source、US5 场景 4、T043/T054 均以指针口径抵达（有效基线名 + 三路径 + 读数命令），不另立取值域。裁定形态只定义在 FR-025，C-405 为同形镜像。
- **closed-set claims 五要件**：基线参照物（有效基线，缺省 `fbab7a45c`）、比较单元（三产物全文逐字节）、允许差异集（**恒为空集**，不随裁定变化）、补集断言与结构不变量（之外逐字节一致；之内无成员、空真）、未定义聚合词清零（「保持不变」「无裁定时为空」均不再承载验收语义）逐项在场；裁定路径不再是第二个 inside 集合。
- **封闭集**：M 9 / P 12 / BC 6 / FR 30 / SC 10 / STR 9 / 契约 38 条款未增删；B 6→7 为本轮唯一的封闭表扩行（B-07），承第二轮 M-09 先例并在 § Clarifications 第四轮记录。
- **受保护面**：`.specify/register.md` 零改动；日期性记录（`analyze-incremental-r4.jsonl`、`analyze-repair{,2,3}-2026-11-26.md`、round-1/2/3 Clarifications 会话、各 checkpoints、既有 `T-NNN` 段）均未改写；其它规格未触碰；三个保全产物相对 `fbab7a45c` 零 diff（rc 0 / numstat 0 行）。
- **fast-fail**：未发现异常（无 ANOMALY 事项）；§ 1 的 in-passing corrections 与 § 2 的 PLAN-EDIT 均为披露项，非静默处置。
- **push**：未 push、未联系远端。

## 5. 残余风险

1. **B 6 → 7 是刻意扩行**：它使 B 表、C-402、FR-023、tasks/plan/checklist/feature detail 的名单同步成为同批义务；若后续 analyze 轮认为应把它折进既有 B-05（理由充分性），须以同等级裁决改回，不在本轮范围。
2. **重定基线的同提交义务由 B-07 承接**：「裁定引入提交未同时承载被裁定改动」与「该提交三路径 diff 与所具名改动不符」不可可靠机器判定（需要语义比对），故按设计归评审；机器侧只判「三路径对有效基线零 diff」这一读数。
3. `R4-04`（C-206/C-401 判别式字段名指向 C-201 而非 C-202 的闭集）与 `R4-05`（SC-008 覆盖矩阵只有 T048/T050，未含产出保全读数的 T043/T054）仍在 analyze 报告名下，未动——二者均为 low，且本轮为 final 修复轮：若后续复检仍要收口，须另行派发。
4. FR-025 的裁定窗要求「裁定记录与改动同提交」；跨提交的「先裁定、后落地」形态按现文本不合法（会读到非零）。这是刻意的收紧（消除追溯追认），代价是裁定记录必须在落地提交里成文。
