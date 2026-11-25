# Analyze Repair Record — 107-decision-governance（round 3，2026-11-26）

- **Stage**: analyze（round-3 gate FAIL 后的修复轮）· **Line**: `decision-governance` · **Branch**: `107-decision-governance` · 单写者
- **Dispatch**: SDD Analyze-Repair Executor（round 3）。不派发子代理、不写状态脊、不实现、不 push。
- **Input**: `test-evidence/analyze-domain-w{1,2,3}-r3.jsonl` 中 validator 确认的 2 条 HIGH：**R3-W1-01 / R3-W2-01**。
- **Scope**: 仅上述触发项的最小一致修复及相邻指针；其余 round-3 发现（R3-W1-02…W1-05、R3-W2-02…W2-06、W3 域）不在本轮触发范围，维持 analyze 报告归属（见 § 5）。
- **Gate captures**: `analyze-repair3-validate-requirements.txt`、`analyze-repair3-pre-analyze-{requirements,plan,tasks}.txt`、`analyze-repair3-validate-tasks.txt`、`analyze-repair3-decomposition.txt`、`analyze-repair3-readings.txt`、`workspace-analyze-repair3.json`（均在本目录）。

## 1. Finding → Change → Evidence（2/2 fixed）

| Finding | Sev | Disposition | 改动（文件:位置） | 证据 |
|---------|-----|-------------|-------------------|------|
| R3-W1-01 | HIGH | **fixed** — FR-025 由不可判定的「保持不变」改写为**五要件 containment claim**：①基线参照物 = requirements 阶段基线提交 `fbab7a45c`（记录于 `requirements-stage-2026-11-25.md`）；②比较单元 = 三个所有者产物的**全文逐字节比较**（`driver-completion-sentinels.yaml` 哨兵字面量 / `watch-model.md` watcher verdict 与退出码 / `efficiency-model.md` 两槽测试预算）；③允许差异集在无裁定时为空；④补集断言 = `git diff --quiet fbab7a45c..HEAD -- <三路径>` rc 0（`--numstat` 零行）；⑤裁定位置与形态 = 符合 FR-014 的 `D-NNN` 决策记录（落于改动面所属生产者的既有载体）或阶段检查点中的具名裁决，须具名被改字面量/行为、新值与理由。门控扫描同步具名基线（`scan-confirmation-gates-baseline.txt`，31 blocking / 0 violations，零新增命中） | `requirements.md` FR-025、SC-008、SC-008 Source、US5 场景 4、RS-005、§ Clarifications 第三轮；`contracts/enforcement-boundary.contract.md` C-405；`plan.md` § Technical Context Constraints；`tasks.md` DoD-6、Phase 7 Goal / Independent Test、T043、T054；`checklists/decision-governance-2026-11-26.md` CHK028/CHK029（引用文本同步并注 pass） | `analyze-repair3-readings.txt`：三路径 diff-quiet rc 0 / numstat 0 行；基线提交与三产物路径逐项在场 |
| R3-W2-01 | HIGH | **fixed** — 新式记录判别式明确为**最小合格形态**：`^### D-\d{3}` 标题 **且块内含 ≥1 条 C-201 字段行**（`- **<field>**: <value>`，基础层或条件层字段名）。低于阈值（无字段行的三位标题、一/两位标题、register 行）保持 `legacy`；达到阈值即新式，**块不完整不再逃逸**——缺基础层字段或条件族触发缺失由 M-01 转红（exit 1）。「既不新式也不 legacy」的块被消除；`D-001` 之类 register 行仍为 legacy（非标题） | `contracts/archive-and-audit.contract.md` C-206；`contracts/enforcement-boundary.contract.md` C-401 M-04 行；`requirements.md` FR-022 M-04、§ Enforcement Boundary M-04 行、§ Clarifications 第三轮；`research.md` M-10 / R-2；`plan.md` BC-01 / BC-03 / BC-05；`data-model.md` I-13；`tasks.md` T024（legacy 夹具增阈值双向样本）、T029 | `analyze-repair3-readings.txt`：live artifacts 中旧「field grammar」表述零残留（除 Clarifications 问题引文）；39 条一/两位标题 / 0 条三位标题的语料读数复测一致 |

**in-passing corrections（披露）**：① `checklists/decision-governance-2026-11-26.md` CHK028/CHK029 原引文引用旧 FR-025 措辞，已同步为新五要件形态并注 **pass**（仅引用文本与注记，未改条目数/维度计数）。② T043 原文把「five-item uplink」与哨兵/两槽并列在同一 `git diff` 断言中；五要素上行属 EP-002 的**结构性**保全（`superagent-definitions.md` 本特性会新增指针行，不能字节保全），已拆为两条读数：三产物 `git diff --quiet` 字节读数 + EP-002 字段计数声明。

## 2. PLAN-EDIT（plan-owned 变更逐条声明）

- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/archive-and-audit.contract.md — C-206 由「标题 + 记录字段文法」改写为最小合格形态（≥1 条 C-201 字段行即新式；不完整由 M-01 判缺字段；无字段行 = legacy）; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/contracts/enforcement-boundary.contract.md — C-401 M-04 行同步最小合格形态；C-405 由「保持不变」改写为具名基线 `fbab7a45c` + 三产物逐字节比较 + 空允许差异集 + 裁定形态; classification=substantive`
- `PLAN-EDIT: .specify/specs/107-decision-governance/plan.md — § Technical Context Constraints 增门控基线与三产物零漂移；BC-01/BC-03/BC-05 同步最小合格形态; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/research.md — M-10 与 R-2 的 legacy 判别式改为最小合格形态（≥1 字段行；不完整由 M-01 判）; classification=minor`
- `PLAN-EDIT: .specify/specs/107-decision-governance/data-model.md — I-13 的 new-form 定义改为最小合格形态; classification=minor`

非 plan-owned 的相邻改动（不属 PLAN-EDIT，逐条披露）：`requirements.md`（两条修复本体 + § Clarifications 第三轮两条裁决）、`tasks.md`（DoD-6、Phase 7 Goal/Independent Test、T024、T029、T043、T054）、`checklists/decision-governance-2026-11-26.md`（CHK028/CHK029）。`plan.md` 的 BC 行集合、M/B/P/BC/STR 行数、SC 与 FR 集合均未增删；`.specify/features/107-decision-governance.md`、`.specify/register.md`、`handoff.md`、`feature-ref.md`、`quickstart.md`、`team.md` 未改。

## 3. 门禁复跑（2026-11-25T17:59Z；逐字捕获见 § header）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/107-decision-governance/requirements.md` | `status: ok`；六项全 pass；`scanned: 421 lines, 40 definition rows, 9 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 skills/external/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/107-decision-governance --stage requirements --repo .` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=127 waived=0`，exit 0 |
| 5 | `python3 .specify/scripts/python/validate-tasks.py .specify/specs/107-decision-governance/tasks.md` | `PASS — 0 error(s), 0 warning(s)`，exit 0 |
| 6 | `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements …/requirements.md --tasks …/tasks.md` | `decision=proceed`；fr_count=30 / task_count=56（ceiling 120/160），exit 0 |

- advisory 构成与 round-2 基线一致：`external-clause` 48 + `missing-path` 79 = 127，无 error。修复过程中一度因 Clarifications 引文提及 `BC-01/BC-03` 增至 129，随即改为指针表述回落 127（见 readings）。
- 确定性计数（`analyze-repair3-readings.txt`）：M 9 / B 6 / P 12 / BC 6 / FR 30 / SC 10 / STR 9 / 契约条款 38 —— 与 round-2 完全一致，封闭集零增删。

## 4. 纪律与保全

- **单一真相**：FR-025 是保全 claim 的唯一需求定义点；C-405 与 SC-008 以指针口径抵达（基线名 + 三路径 + 读数命令），未另立取值域。新式记录判别式以 C-206 为契约定义点、FR-022 M-04 为需求定义点，其余面（M-10、BC、I-13、T024/T029）均为同步表述。
- **closed-set claims 五要件**：基线参照物（`fbab7a45c`）、比较单元（三产物全文逐字节）、允许差异集（默认空）、补集断言（三路径 rc 0 / 零 numstat 行）、未定义聚合词清零（「保持不变」不再承载验收语义）逐项在场；裁定记录位置与形态已具名。
- **封闭集**：M 9 / B 6 / P 12 / BC 6 / STR 9 / FR 30 / SC 10 / 契约 38 条款均未增行；本轮改动全部是既有行/段的修订或既有会话追加。
- **受保护面**：`.specify/register.md` 零改动；dated 记录（`analyze-domain-w*-r3.jsonl`、`analyze-repair-2026-11-26.md`、`analyze-repair2-2026-11-26.md`、各 checkpoints、既有 `T-NNN` 段、round-1/2 报告）均未改写；其它规格未触碰；三个保全产物相对 `fbab7a45c` 零 diff。
- **fast-fail**：未发现异常（无 ANOMALY 事项）；上述 in-passing corrections 与门禁回退均为披露项，非静默处置。
- **push**：未 push、未联系远端。

## 5. 残余风险

1. **最小合格形态的边界是刻意选择**：三位标题 + **零** C-201 字段行按定义是 `legacy`（不判）。这是「最小合格形态」的显式阈值而非漏洞——M-01 的缺字段转红条件对任何 ≥1 字段行的块都可触发；T024 已新增该阈值的双向夹具（零字段行 → legacy；仅一条字段行 → 新式且 M-01 红）。若后续希望「三位标题一律视为记录尝试」，须按 FR-025 的裁定形态改 C-206 与 M-04，不在本轮范围。
2. `R3-W1-02`（无人值守 human-interactive 的 blocked 姿态与多跳链不变量无 FR 锚点）、`R3-W1-03`（单可行选项未声明 forced 无 M/B 承接）、`R3-W1-04`（「决策 backed」识别基准）、`R3-W1-05`（P-03/P-10 的类别/义务措辞）、`R3-W2-02…W2-06`（transmission_status 追加 vs 改写、人的选择信号落位、forced 无语法槽、dense 语义、四落地面之一无名）与 W3 域发现仍在 analyze 报告名下，未动。
3. FR-025 的三产物全文比较比「两槽预算规则不变」更严（整文件而非 §2 抽取）：`efficiency-model.md` 未被本特性计划触碰，故当前成立；实现期若确需改动该文件的非 §2 部分，须先有 FR-025 裁定记录，这是刻意收紧而非误红。
