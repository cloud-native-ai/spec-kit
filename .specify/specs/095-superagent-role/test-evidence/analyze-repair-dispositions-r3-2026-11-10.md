# Analyze Repair Dispositions — r3（095-superagent-role，2026-11-10）

- **Stage**: analyze 门自主修复轮（round-2 报告 0C / 4H；用户授权续环，修复后直接续跑 analyze，不等待用户）· **Line**: `095-superagent-role` · 单写者
- **Input**: `test-evidence/analyze-merged-round2-2026-11-10.md`（44 行；0C / 4H / 28M / 12L）+ `analyze-findings-round2-W{1,2,3}.md`
- **Scope of this round**: 逐条处置 **HIGH 4/4**（下表 §1，全部 `confirm → fixed`；无 `reject`、无 `accepted-risk`、无静默丢条）。round-2 的 MEDIUM/LOW（含 X2-01/02/03）**不属本修复轮授权范围**，按 analyze 报告的归属指针留待各自 owner / 后续轮，**不视为已关闭**（§4 显式披露）。
- **Touched artifacts**: `requirements.md`、`data-model.md`、`plan.md`、`tasks.md`、`contracts/role-edge-engine.contract.md`、`contracts/role-transition-payload.contract.md`、`.specify/features/095-superagent-role.md`；证据：本文件 + `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`。
- **单一设计裁定（本修复轮，自行裁决并记录）**: 「已授予派发职责」的独立声明值复用既有 `dispatch_duty` 字段（取值 `granted` / `not-granted`，该字段已存在于 `data-model.md` § 2 与引擎契约 C-3 输出键集），不新造机器 token；代价是下行角色字段块由六项扩为**七项**（`role_declaration` 与 `dispatch_duty` 分离），全篇计数已机械同步。备选（新 token 如 `dispatch-granted`）被拒：会与既有 `dispatch_duty` 形成第二套授予词汇（XIV 重复）。

## 1. HIGH 逐条处置（4/4）

| Finding | Sev | 处置 | 改动文件:行 | 一句话理由 |
|---------|-----|------|-------------|------------|
| W1-30 | H | confirm → fixed | `requirements.md:128`（FR-005）、`:197`（Key Entities）、`:210`（SC-001）；`data-model.md:13`（§1 验证）、`:22-23`（§2 两字段）、`:35-40`（§2.1(a) 表+注）、`:71`（§5）、`:76-88`（§6）；`contracts/role-transition-payload.contract.md:7`（C-1）、`:54-57`（C-11）、`:67`（C-13）；`plan.md:34`（D-6）、`:37`（D-9）；`tasks.md:101`（T005）、`:122-123`（T011/T012）、`:129`（T015）、`:140-147`（US2 目标/IT/T019/T020）、`:152-155`（T022/T023/T025）、`:178`（T032）、`:296`（并行示例）；`.specify/features/095-superagent-role.md:20`、`:49` | `dual-role` 收敛为**单一语义**：只作角色集**输出**中「两角色同时具备」的机读标记（[[STR-002]]），任何载体声明字段 MUST NOT 取该值；「已授予派发职责」改由独立的 `dispatch_duty` 声明字段承载。FR-005 弃用字面量、改引 [[STR-002]] 并声明字段作用域；Key Entities / SC-001 同步。 |
| W1-31 | H | confirm → fixed | `requirements.md:218`（SC-009）、`:231`（SC-009 Source）、`tasks.md:223`（T045 绿断言改基线比对）、`:225`（US5 checkpoint「全绿」表述）；复核未改：`:177`（FR-036，判据 owner）、`plan.md:195`（Inherited #4）、`tasks.md:31`（GATE-1） | SC-009 与 FR-036 统一为**同一完成门判据**：四类既有治理契约测试「相对 implement 起点全量失败名单基线零新增失败」，基线既有红逐条点名并声明不属本特性写域，MUST NOT 声称「全绿」；SC-009 Source 补基线比对读数；tasks 侧 T045 与 US5 checkpoint 的「全绿」表述同步改为基线比对（同句扇出扫全）。三处完成门（SC-009 / plan Inherited #4 / GATE-1）复读确认同判据，后二者无改动。 |
| W1-32 | H | confirm → fixed | `requirements.md:29`（US1 故事叙述）、`:223`（SC-001 Source）；全篇复扫 `三类` = 0 | W1-04 的修复扇出扫全：US1 故事示例与 SC-001 Source 均改为**四类违例**（含 `depth-inconsistent`），与 FR-005 / US1 AS3 / SC-001 一致；机械复扫确认无其他「三类」残留。 |
| W2-13 | H | confirm → fixed | `data-model.md:22`（§2 `role_declaration` 值域）、`:37-40`（§2.1(a) 表行与注）、`:71`（§5 谓词）、`:82-83`（§6 字段）；`contracts/role-edge-engine.contract.md:65`（C-9）；`tasks.md:122`（T011 严格输入与变异声明） | 载体声明域改为 `subagent \| superagent`（三处同步），`superagent` 成为**已知合法值**——`unbacked-role-claim` 由此**可达**，且 C-9 显式规定该取值由 C-5 判红（exit 1）、**永不**落 malformed（exit 2），消除「不可达」与「同一行双判」两种失效；`dispatch_duty` 值域 `granted \| not-granted` 同条声明。 |

## 2. 附带修复（in-passing；同句/同扇出所及，均披露）

| 项 | 原级别 | 处置 | 改动文件:行 | 理由 |
|----|--------|------|-------------|------|
| W2-20 | LOW | fixed（顺带） | `plan.md:34`（D-6）；`tasks.md:122`（T011）、`:129`（T015） | D-6 原写「superagent assertion with no parent edge」方向相反（§5/C-5 谓词为「无一条以其为 parent 的出边」）；本轮因 W1-30/W2-13 必须重写该句，已一并改为 `no edge where it is the parent`。 |
| W1-20 | MEDIUM | fixed（顺带） | `requirements.md:168`（FR-030）；`.specify/features/095-superagent-role.md:49` | 映射表增加 `dispatch_duty` 列后，需求文本的 `label → 角色 → 工作区` 描述必须回写；同时补齐下游既有的 `parent` 列（原 W1-20 的缺口），统一为 `label → 角色 → 派发职责 → 工作区 → 父身份`。 |
| 六→七字段计数扇出 | —（W1-30/W2-13 的机械关联） | fixed（同轮） | `data-model.md:42`（§2.1(b)）、`:76`、`:88`；`contracts/role-transition-payload.contract.md:7/54/57/67`；`plan.md:37`；`tasks.md:140/142/146/147/152/155/296` | 下行角色字段块由六项扩为七项（新增独立 `dispatch_duty`）后，全篇 `six fields` / 「六字段」/「六个下行」出现点**机械扫全**；复扫残留 = 0（SO-2C 教训的应用）。 |

## 3. 门禁复跑（完整捕获见 `test-evidence/analyze-repair-gates-r3-2026-11-10.txt`）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 scripts/python/validate-requirements.py .specify/specs/095-superagent-role/requirements.md` | `status: ok`；6 标签全 pass；`scanned: 288 lines, 48 definition rows, 6 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/095-superagent-role --stage requirements --repo .` | `decision=pass errors=0 advisories=81 waived=0`（fr=38 / sc=10 / tasks=54 / files=12），exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=81 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=81 waived=0`，exit 0 |
| 5 | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/095-superagent-role/requirements.md --tasks .specify/specs/095-superagent-role/tasks.md` | `decision=proceed`；fr_count=38 / task_count=54（ceiling 120/160），exit 0 |

- **advisory 构成（逐条枚举核对，非门禁）**: 81 = 79 × `missing-path`（implement 阶段才创建的交付路径：`superagent-definitions.md`、`role-edge-check.py`、六个契约测试模块、夹具目录等）+ 2 × `blocked-by` 模板占位 token（`<行ID>`，tasks 格式节示例行）。全部属实现前预期，与 plan 修复轮 `advisories=39` 同型（本阶段 spec 文件数 12、检查面更全故计数更高）。新增 11 条相对 r1 的增量均为前述既有缺失路径的逐行重复计数，无新类别。
- **本修复轮不重冻覆盖率基线**（`account-clause-coverage.py` 不在本轮的判据内；其 `uncovered` 读数与 W3-06 的 MEDIUM 归属不变）。

## 4. 显式维持（不属本修复轮授权范围；不静默关闭）

- round-2 **MEDIUM/LOW 全部维持**：W1-07/08/09/10/12/13/14/15/16/17/18/19/21/22/23/25/26/28/29/33/34/35、W2-05/07/12/14/15/16/17/18/19、W3-06/08/09/10/11、X2-01/02/03 —— 非本修复轮授权项，按 analyze merged report §7 的归属指针留待 implement / 后续轮；**其中 W1-20 与 W2-20 因与 HIGH 同句/同扇出，已在本轮顺带修复（§2）**。
- **验证波**: 本修复不改 round-2 的「HIGH 为检测者提议值」状态；修复后的重过 analyze 由轮换以全新检测/验证视角裁决，本文件不冒充验证结论。

## 5. 纪律说明

- 单写者；只改本特性产物与绑定 Feature 记录；未触碰其他特性、未 push。
- **未运行测试套件**（本轮只改规格/计划/任务/契约文本，无产品代码变更；测试入口纪律保持 `scripts/bash/run-tests.sh`）。
- 既有脏文件未提交未还原；前序阶段遗留 `checkpoints/`（未跟踪）继续不代提交。
- 异常：无；in-passing repair：3 项（§2）。假设：仅 § 顶部「单一设计裁定」一条（`dispatch_duty` 复用而非新 token）。
