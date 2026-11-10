# Analyze Repair Dispositions — 098-suite-speed-optimizations（2026-11-10）

- **Stage**: analyze 门失败（Round 1 merged verdict FAIL：1 CRITICAL + 7 HIGH，全部 validated）后的上游修复轮；**一轮为限**。
- **输入**: `test-evidence/analyze-merged-2026-11-10.md`（§0 gate verdict + C/H 表 + validated 边界）、W1/W2/W3 原始 finding 文件。
- **权威**: 本特性 spec 全目录 + `.specify/constitution.md`（v1.19.0，§XX）+ `.specify/skills/internal/analyze-artifacts/`。
- **纪律**: 每条 C/H 先复核（confirm/reject），再做最小修复；CRITICAL 不降级，按宪法字面修正；修复在 requirements/contracts/tasks/plan 两侧同步。
- **结论**: 8/8 **confirm**、0 reject。全部修复落盘；门禁复跑见 `analyze-repair-gates-2026-11-10.txt`。

## 0. 处置汇总

| # | ID | 严重度 | 复核 | 修复落点 | 验证读数 |
|---|----|--------|------|----------|----------|
| 1 | W1-01 | CRITICAL | confirm | `requirements.md` §Overview、§FR-021；`plan.md` §Summary | FR-021/Overview 改为引用宪法 XX 指定的 owner（`test-execution-efficiency.md` §「不可采纳的提速手段」），不再重述清单；098 增量判据保留为可判定形态 |
| 2 | W1-02 | HIGH | confirm | `requirements.md` §SC-010 + §SC-010 Source；`quickstart.md` S-10；`tasks.md` T057 | SC-010 检测面覆盖装饰器 + 函数体内（`pytest.skip(`/`xfail(`、条件跳过、可重入重试循环）；扫描规则清单与零命中反空转输出入 Source |
| 3 | W1-08 | HIGH | confirm | `requirements.md` §FR-024、§Clarifications Q2、§SC-006；`data-model.md` E-1 | 排除数算式按档限定：fast=该次选择内成员数；caller=0；full=0 且回全局全量（须无调用方 `-m`） |
| 4 | W1-09 | HIGH | confirm | 同上（FR-024/Q2/SC-006） | 「`--full` 回到全量」限定为「无调用方 `-m`」；`--full` + 调用方 `-m` 时选择仍归调用方，收集集合不扩展回全局全量（FR-009） |
| 5 | W1-17 | HIGH | confirm | `requirements.md` §FR-016、§FR-017、§SC-008 + §SC-008 Source | FR-016 枚举三个 runner 文件；FR-017/SC-008 声明六文件闭集作用域，零计数断言可判定 |
| 6 | W1-21 | HIGH | confirm | `requirements.md` §FR-026、§A16；`tasks.md` T031 | 30 秒改为**声明内的共享缺省变更**（实测 5.0 → 30），不再声称「既有约定」；T031 断言 `timeout == 30`（enacted 值，对 5.0 红） |
| 7 | W3-01 | HIGH | confirm | 六份 `contracts/*.contract.md` + `plan.md`/`quickstart.md`/`feature-ref.md`/`tasks.md` | 68 条款全部重编号为 `C-001…`（md-bold-closed，6/6 文件可解析）；全部引用同步；tasks 补 68 条 `[green:]` 归属（一 clause 一 row） |
| 8 | W3-11 | HIGH | confirm | `tasks.md` DoD-7 / GATE-1 / Notes | 改为「两次预算槽全量 + closure 同树 `--full --serial` 验证运行（不占槽、不进度量，A14）」；plan 的「no third full run for measurement」经复核一致，未改 |

## 1. 逐条复核与修复细节

### W1-01（CRITICAL）— 宪法 XX 重述漂移 → confirm，按宪法字面修正

- **复核**: 重读宪法 §XX L431–439：判据 owner 是 `.specify/shared/guidelines/test-execution-efficiency.md`，且「consumers MUST reference it, do not restate it」；owner §「不可采纳的提速手段」含「声明不稳定 (declare flaky)」「重跑到绿 (retry until green)」等六类。原 FR-021 的封闭清单（重试至绿/随机丢参/skip/xfail/缩小参数化/放宽时限/无上限 worker）既重述又漏项（flaky），Overview L28 同为重述。**finding 成立，不可降级**。
- **修复**: FR-021 改为「以 owner 为唯一清单与判据，本条 MUST NOT 重述其条目」，只保留 098 特有增量：参数化条目减少、等待截止超过 FR-026 上限、worker 解析超出 runner 契约既有规则——三者均给出可判定形态；Overview 同步改为 owner 指针。
- **两侧同步**: `plan.md` §Summary 的同类重述句（"retry, dropped parameters, skip/xfail, …"）一并改为 owner 指针 + SC-010 检测增量，避免 plan 侧继续重述。
- **边界**: 未改宪法、未改 owner 文件；未在规格中复制 owner 清单。

### W1-02（HIGH）— SC-010 检测面窄于全称谓 → confirm

- **复核**: SC-010 原文只数「新增装饰器」，Source 也只写「装饰器与参数化计数」；函数体内 `pytest.skip()`、条件跳过、手写重跑至绿不在面内，无法支撑 FR-021 的禁止全称谓。finding 成立。
- **修复**: SC-010 的判据改为「AST + 文本双通道」扫描，显式命名四类形态：装饰器（skip/skipif/xfail/重试）、函数体内调用（`pytest.skip(`/`pytest.xfail(`）、条件跳过分支、含断言或被测调用的可重入重试至绿循环；参数化条目数做前后比较。SC-010 Source 增加「扫描规则清单 + 零命中时仍打印扫描范围（反空转）」。
- **两侧同步**: `quickstart.md` S-10 的 Proves 行扩写并指向 AST leg 与 `test-evidence/forbidden-shortcuts.txt`；`tasks.md` T057 的扫描描述同步为四类形态。

### W1-08 / W1-09（HIGH）— FR-024 披露算式未按档限定 → confirm

- **复核**: FR-024 原等式「披露排除数 = 本次选择内成员数」「`--full` 时回到全量」均未限档；FR-007/FR-009 已规定 caller 档 slow 成员被选中而非排除、`--full` + 调用方 `-m` 时选择仍归调用方。与 requirements 内部条款冲突，finder 成立。
- **修复**: FR-024 重写为按档断言：fast 档 = 该次选择内成员数；caller 档 = 0；full 档（无调用方 `-m`）= 0 且收集集合回全局全量；`--full` + 调用方 `-m` 时选择仍由调用方拥有、收集集合 MUST NOT 扩展回全局全量（引 FR-009）。
- **两侧同步**: Clarifications Q2 的同一未限定等式同步；SC-006 的守门证明句同步；`data-model.md` E-1 的 `excluded_slow` 字段规则改为「被本档从调用方选择中排除的 slow 成员（caller/full 档为 0）」，与 E-1 既有不变量一致（顺带消除 W2-10 LOW 的规则/不变量冲突）。
- **契约侧**: `tier-selection` C-003 原文已规定 caller 档 `excluded_slow=0`，无需改动；`slow-membership` C-007 的 fixture 断言本就无调用方 `-m`，语义与修复后 FR-024 一致。

### W1-17（HIGH）— SC-008 作用域未枚举 → confirm

- **复核**: FR-016 只写「runner 相关测试」，FR-017 反向引用该未定边界，SC-008 的「为零」断言不可判定。设计侧 `event-wait` C-001 已枚举六文件，需求文本未拥有。finder 成立。
- **修复**: FR-016 枚举三个 runner 文件（`test_sdd_loop_efficiency_runner.py`、`test_session_kill_reattach.py`、`test_line_envelope_contract.py`）；FR-017 把作用域定义为 FR-015 文件 + FR-016 三文件 + 两个显式并入的同缺陷类排序文件（`test_feedback_probe_cli.py`、`test_store_state_protocol.py`）；SC-008 与 Source 携带完整六文件闭集。
- **两侧同步**: 与 `event-wait` C-001 的枚举逐一对应（C-001 保持其按 FR 的标注形式）。

### W1-21（HIGH）— 30 秒「既有约定」与实测 5.0 秒矛盾 → confirm

- **复核**: `tests/fixtures/line_fixtures.py:396` 实测 `timeout: float = 5.0, interval: float = 0.05`；「086 runner 测试有 30 秒约定」无被引证据。finding 成立。
- **修复**: FR-026 与 A16 改写为「声明内的共享缺省行为变更」：当前缺省实测 5.0 秒，本特性显式调整为 30 秒 / ≤0.2 秒轮询；删除「与既有约定一致」的断言。
- **两侧同步**: `tasks.md` T031 的 red-first 断言由 `timeout <= 30` 改为 `timeout == 30`（enacted 值；对变更前的 5.0 必红）——顺带消除 W3-04 MEDIUM 的「断言先绿」缺陷；T037 的调整行不变；`data-model.md` E-5 的 `default 30` 为目标态，无需改动。

### W3-01（HIGH）— 条款 id 前缀形态不可解析 → confirm（plan-owned remedy 由本轮执行）

- **复核**: `clause_extract.py` 的形态集只认 `**C-\d+…**`；六份契约的 `**TS-01**`…`**IC-10**` 全部 `md-none`。修复前实测：`[fr-uncovered] fail (27) — 0 of 27`、六文件均在 named-unparseable 名单中。finding 成立。
- **修复（plan 侧）**: 六份契约的 68 条款全部重编号为 `C-001…C-0NN`（文件内唯一，沿用 086 契约为最近同族形态）；契约内对 086 条款的全部提及加 `086 ` 前缀以消除与新本地 id 的歧义；`plan.md` / `quickstart.md` / `feature-ref.md` / `tasks.md` 的全部引用同步（含裸 `C-00N` 引用补契约 stem）。
- **修复（tasks 侧）**: 删除原「Clause Attribution Deviation」节，代之以 `## Clause Attribution`：记录重编号事实、机器读数与 68 条 `[green:]` 归属分区表；任务行按「文件转绿行 + 完成时点更晚的迟到行」原则携带 68 条标签（一 clause 恰一 row）。
- **FR 车道补全**: 重编号后重跑核算发现 FR-010 与 FR-021 未被任何条款引用组引用（原 25/27）；按「条款确有该命题的部分投影」原则在两处既有条款的引用组内补引：`parallel-consistency` C-007 描述 closure 槽全量运行（补 FR-010），`event-wait` C-006 的「超时 MUST NOT 转 skip/xfail/重试」是禁止捷径的实例化（补 FR-021）。未新增条款，条款总数保持 68。
- **验证**: 六文件全部 `md-bold-closed`（16/9/12/11/10/10 = 68）；`[fr-uncovered] pass (0) — 27 of 27`；`validate-tasks.py` 0 error（3 条 green-cross-phase WARN 已逐条记录在 § Clause Attribution）；核算 `claimed clauses 68`。
- **残余观察（非本单修复项）**: driver 侧 `pre-analyze-check.py` 的条款正则 `[A-Z]{2,4}-\d{2}` 不匹配规范 `C-<n>`（单字母 + 三位数字），其 `clauses` 汇总读数由 68 变 0——该脚本对 086 等所有使用规范形态的 spec 同样读 0，属框架工具对该形态的既有盲区，不产生任何 finding；不在本特性契约面内，不改框架脚本。核算的 `status: baseline-missing` 属预期：冻结（T002）是 implement 起点义务，「先冻结会钉住坏基线」的顺序条件本轮已满足。

### W3-11（HIGH）— 「恰好两次全量运行」与 T061 实跑两次矛盾 → confirm

- **复核**: DoD-7/GATE-1/Notes 均称两次全量；T061 一条命令含 `--full --names-out` 与同树 `--full --serial` 验证运行 → 全量执行实为 3 次。requirements Q2/A14 已把串行验证运行置于槽预算之外且不受「为度量」禁令约束。finder 成立，缺陷在 tasks 计数措辞。
- **修复**: DoD-7 改为「两次**预算槽**全量 + closure 同树串行验证运行（不占槽、不进度量）」；GATE-1 的括注同步；Notes 的预算段同改并注明 A14。
- **plan 侧**: 复核 `plan.md` 的既有措辞（`no third full run for measurement`、`two-slot count/timing/order` 不变、`parallel-consistency` C-007 已声明验证运行不入台账）——与修复后任务措辞一致，**无需改动**。

## 2. 附带修正（由上述修复直接要求的同步，非独立 finding 处置）

| 落点 | 改动 | 触发 |
|------|------|------|
| `data-model.md` E-1 | `excluded_slow` 规则按档限定 | W1-08/W1-09 两侧同步（同时消除 W2-10 的规则/不变量冲突） |
| `plan.md` §Constitution Check XXI / Phase 1 summary / Risks R-2/R-5/R-8/R-10 | 条款引用随重编号更新 | W3-01 |
| `quickstart.md` S-1…S-13 的 Proves 行 | 条款引用补契约 stem | W3-01 |
| `tasks.md` T031 | `timeout <= 30` → `timeout == 30` | W1-21 的检测面同步（顺带消除 W3-04） |
| `tasks.md` T043 | `tests/conftest.py` 前加「read-only」限定词 | 消除 validate-tasks 的路径启发式误报（只读引用降级，非删除标签） |

## 3. 未处置（保持 open，按严重度不阻断）

- MEDIUM 37 条 / LOW 13 条（含 W3-02/W3-04/W2-10 已被上述同步顺带贴合者不进此处）不属本轮 C/H 范围，保持原状；W2-10 的字段规则冲突已随 E-1 同步消解。
- 三条 `validate-tasks` green-cross-phase WARN 为「完成时点晚于条款序」的结构性告知（T061 迟闭环、T041 守卫转绿、T025 先于 T027 的 C-005/C-006），已在 `tasks.md` § Clause Attribution 逐条记录，非错误。
- 核算 `status: baseline-missing`：冻结义务属 T002（implement 起点），本轮不再前置冻结。

## 4. Fast-Fail 声明

本轮无「决定型」异常需要上报；所有修复均为与已记录分析结论一致的就地修正。运行中发现的唯一计划外事实（FR-010/FR-021 在重编号后仍未被条款引用组覆盖）已按可核实的规则补引并记入 W3-01 处置。

## 5. 本轮触碰的制品

- 修改：`requirements.md`、`plan.md`、`quickstart.md`、`feature-ref.md`、`data-model.md`、`tasks.md`、`contracts/*.contract.md`（6）。
- 新增：`test-evidence/analyze-repair-dispositions-2026-11-10.md`（本文件）、`test-evidence/analyze-repair-gates-2026-11-10.txt`。
- 未触碰：`checklists/*`（dated record）、`research.md`（无缺失引用）、`checkpoints/*`（驱动侧记录）、`.specify/features.md` 与 086 详情文件（状态保持 `Ready for Review`）、`test-evidence/analyze-*` 既有记录（dated record）。
