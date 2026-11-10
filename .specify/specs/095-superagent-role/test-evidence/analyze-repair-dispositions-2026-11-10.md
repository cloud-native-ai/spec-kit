# Analyze Repair Dispositions — 095-superagent-role（2026-11-10）

- **Stage**: analyze 修复轮（上游 requirements/plan/tasks 修复后重过 analyze 门，一轮为限）· **Line**: `095-superagent-role` · 单写者
- **Input**: `test-evidence/analyze-merged-2026-11-10.md`（2 CRITICAL / 12 HIGH / 32 MEDIUM / 8 LOW）+ `analyze-findings-W{1,2,3}.md`
- **Scope of this round**: 逐条处置 **CRITICAL 2 + HIGH 12**（下表 §1，全部 `fixed`）；MEDIUM/LOW 择要修复（§2），其余维持 analyze 报告归属、不阻断（analyze round 2 重报）。无 `accepted-risk`、无 `not-applicable`、无静默丢条。
- **Touched artifacts**: `requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/role-edge-engine.contract.md`、`contracts/status-digest-role-view.contract.md`、`contracts/harness-landing.contract.md`、`.specify/features/095-superagent-role.md`、`.specify/features.md`（095 行描述）；证据：本文件 + `test-evidence/analyze-repair-gates-2026-11-10.txt`。

## 1. CRITICAL / HIGH 逐条处置（14/14）

| Finding | Sev | Disposition | 改动文件:行 | 一句话理由 |
|---------|-----|-------------|-------------|------------|
| W1-01 | C | fixed | `requirements.md:139`（FR-013） | 删去 attribution 五取值枚举，改为 owner 指针（`.specify/skills/sdd-loop-driver/references/watch-model.md` § 11 归属层），宪法 XIV 的枚举副本被移除；clarify 记录（Q「重试与旧结果如何区分？」）原文只写「按既有 attribution 取值识别」，本就不含枚举，无需同步。 |
| W1-02 | C | fixed | `.specify/features/095-superagent-role.md:16`（`## Implementation Notes`）、`:55`（`## Related Files`） | 补齐宪法 Feature Documentation Requirements 要求的两个 MUST 节，内容为已知实现约束（其余细节按阶段落笔）。 |
| W1-03 | H | fixed | `requirements.md:125`（FR-002）、`:197`（Key Entities）、`:210`（SC-001） | 统一为「角色是 `{subagent, superagent}` 集合，`dual-role` 只是两角色同时具备的集合形态机读标记、不是第三个取值」；三处互斥写法收敛到同一形态。 |
| W1-04 | H | fixed | `requirements.md:128`（FR-005）、`:39`（US1 AS3）、`:210`（SC-001）、`tasks.md:116`（US1 IT） | 第四类违例定义为 `depth-inconsistent`（声明深度 ≠ 计算最短距离，或环使深度不可解析；非深度上限规则），US1 AS3 / SC-001 / US1 IT 全部补齐为四类。 |
| W1-05 | H | fixed | `requirements.md:128`（FR-005）、`data-model.md:40`（§ 2.1 注）、`:71`（§ 5 谓词） | 「角色声明」指名载体：team 映射行 `role` 列或 stage envelope `role_edge` 声明中的**显式 `superagent` 断言**；违例可机判。 |
| W1-06 | H | fixed | `requirements.md:147`（FR-018）、`tasks.md:147`（T020） | 自检从「只匹配 `role-transition` 子串」改为「标识 + 九项 item-id 句柄逐项匹配」，缺任一项即阻断；与 SC-002 的逐项阻断一致。 |
| W2-01 | H | fixed | `plan.md:36`（D-8）、`contracts/role-edge-engine.contract.md:18`（C-1 Importable interface）、`contracts/status-digest-role-view.contract.md:5`（C-1）、`tasks.md:130`（T016）、`:193`（T034）、`:198`（T036） | 定死可导入纯函数签名 `read_carrier_inputs(...)` + `evaluate_role_model(inputs)`（`exec-quant` 同款 importlib 装载）；digest 每次运行各调一次，三族角色边与 legacy 条目共享**一次载体物化**，不再声称「只读 registry entries 就能建三族边」。 |
| W2-02 | H | fixed | `data-model.md:11`（§ 1）、`:23`（§ 2 `dispatch_duty`）、`:71`（§ 5）、`plan.md:34`（D-6）、`requirements.md:128`（FR-005）、`tasks.md:122`（T011 变异(c)） | `dual-role` 声明 = 已授予派发职责（授权事实，不是 superagent 主张）；`unbacked-role-claim` 只罚「显式 `superagent` 断言且无父边」，已授权未派发不再被误判。 |
| W2-03 | H | fixed | `plan.md:38`（D-10）、`:209`（Phase 0 #5）、`:156`（Mirror 行）、`:225`（P5）、`contracts/harness-landing.contract.md:17`（C-1）、`tasks.md:220`（T042）、`:222`（T044） | 更正「无 section-count pin」的失实表述；实测 pin `TPL_EXPECTED=35 / LIVE_EXPECTED=36`（`test_fast_fail_discipline.py:751-752`）已登记同提交 +1 义务并补任务行 T042（含 T044 复跑该 pin 测试）。 |
| W3-01 | H | fixed | `tasks.md:19`（DoD-3）、`:237`（T050） | 单位与计数以 `plan.md` § Mirror Obligations 表为唯一 owner（10 个 source 行覆盖 12 个文件），任务侧改为指针 + 逐行映射表述，删除手写「11 行」。 |
| W3-02 | H | fixed | `tasks.md:129`（T015 补 FR-013/FR-015）、`:201`（T039 补 FR-012/FR-014）、`:216`（T041 补 FR-011/FR-016） | FR-011…FR-016 六者各获得真实落点：T015 承担 attempt/stale 语义与既有载体状态派生（FR-013/015），T039 承担有界等待与恢复授权重验证（FR-012/014），T041 承担「汇报/授权 owner 不复制 + 无第二通道」（FR-011/016）；逐 FR 引用数现均为 1。 |
| W3-03 | H | fixed | `tasks.md:240`（T053） | T053 由「只记录结果」改为**实际运行** smoke 命令并把 stdout/退出码写进 `test-evidence/smoke-six-modules.txt`，`smoke_exit_code=<measured>`——GATE-4/DoD-6 的证据文件有了生产者。 |
| X-01 | H | fixed | `requirements.md:177`（FR-036）、`plan.md:195`（Inherited #4） | 完成门判据统一为唯一一条：**相对 implement 起点全量基线零新增失败**；基线既存红须逐条点名且声明不属于本特性写域，不再要求字面「全绿」；gate GATE-1/T051 原已用同一判据，三处一致。 |
| X-02 | H | fixed | `requirements.md:129`（FR-006）、`contracts/role-edge-engine.contract.md:45`（C-4） | 两种机器行为按来源分离：**记录侧**无法解析 = `dangling-parent` 违例（exit 1）；**query 参数**无法解析 = 具名输入错误（exit 2）——requirements 与契约两侧同步为同一行为。 |

## 2. MEDIUM / LOW 择要修复（非强制项；其余维持 analyze 报告归属，不阻断）

| Finding | Sev | Disposition | 改动文件:行 | 理由（择要） |
|---------|-----|-------------|-------------|--------------|
| W1-11 | M | fixed | `requirements.md:146`（FR-017） | 「MUST 至少包含」→「MUST 恰好包含（封闭清单，不得增项）」，消除超集/封闭二义。 |
| W1-24 | M | fixed | `requirements.md:182`（FR-038） | 把 Clarifications 声称的补句落入正文：每行须记录**切片机制主张**；`not-observed` 须附**未观测理由**。 |
| W1-27 | L | fixed | `requirements.md:239-241`（Shared Strings） | 补 Consumed by：STR-002←FR-005、STR-003←FR-034、STR-004←FR-004/FR-034。 |
| W2-04 | M | fixed | `data-model.md:23`（`dispatch_duty`）、`:62-63`（§ 4） | 引擎输出键集与契约 C-3 对齐：data-model 增 `dispatch_duty`/`sources`；`state/last_activity/age/stale` 明确为 digest 视图字段而非引擎输出。 |
| W2-06 | M | fixed | `data-model.md:26`（§ 2 `conflicts`）、`contracts/role-edge-engine.contract.md:39`（C-3）、`plan.md:33`（D-5） | 冲突行形状统一：`conflicts` 为顶层行并携带所属边身份（`parent/child/attempt`），多边报告可归属；plan 措辞随之对齐。 |
| W2-08 | M | fixed | `contracts/role-edge-engine.contract.md:30`（C-2）、`plan.md:32`（D-4） | 枚举 required（state/teams/logs，缺失→2）与 optional（registry，cross-check，缺失记入 `inputs`、不致命）根。 |
| W2-09 | M | fixed | `contracts/status-digest-role-view.contract.md:13`（C-2）、`:30`（C-6） | 合并集按来源类型定 schema：line 行保留既有键名并新增三字段；非 line 行用 `id`/`last_activity` 并在无源字段处显式 `null`；两类字段族不混行。 |
| W2-10 | M | fixed | `.specify/features/095-superagent-role.md:10`、`.specify/features.md:102` | 注册表两处按 plan D-2/D-6 收敛：独立引擎 `role-edge-check.py` + 四类封闭违例（不再是「引擎动作」「三类违例」）。 |
| W2-11 | L | fixed | `contracts/role-edge-engine.contract.md:16`（C-1）、`plan.md:31`（D-3） | registry 默认解析链改为指向 owner `line-registry.py`（不再复制链路）。 |
| W3-04 | M | fixed | `tasks.md:116`（US1 IT） | 「三类」→「四类」违例夹具，与 T013/T015 及 requirements 对齐。 |
| W3-05 | M | fixed | `tasks.md:263`（User Story Dependencies） | US2 与 US1 的关系按 `blockedBy` 图重写（T028 只读引用 T005 owner 页，不依赖 US1 产物）。 |
| W3-07 | M | fixed | `tasks.md:200`（T038）、`:222`（T044） | 命名为 evidence 落盘文件（`status-digest-roles-readings.txt` / `instructions-budget.txt`），与同文件其它转绿行一致。 |
| X-03 | M | fixed | `plan.md:33`（D-5） | 根/父身份解析顺序单一 owner = `data-model.md` § 3（label → line id → run_id → literal root → dangling），plan D-5 改为指针。 |

**未处置的 MEDIUM/LOW（显式维持）**：W1-07/08/09/10/12/13/14/15/16/17/18/19/20/21/22/23/25/26/28/29、W2-05/07/12、W3-06/08/09/10 —— 均非门禁项，按 analyze 合并报告的归属指针留待 implement/后续轮；本清单如实披露未逐条修复，不视为 `accepted-risk`（其不阻断 analyze 门）。

## 3. 门禁复跑（本修复轮写入；完整捕获见 `test-evidence/analyze-repair-gates-2026-11-10.txt`）

| # | 命令 | 读数 |
|---|------|------|
| 1 | `python3 scripts/python/validate-requirements.py .specify/specs/095-superagent-role/requirements.md` | `status: ok`；6 标签全 pass；`scanned: 288 lines, 48 definition rows, 6 shared strings`；**0 error / 0 warning**，exit 0 |
| 2 | `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/095-superagent-role --stage requirements --repo .` | `decision=pass errors=0 advisories=70 waived=0`（fr=38 / sc=10 / tasks=54 / files=12），exit 0 |
| 3 | 同上 `--stage plan` | `decision=pass errors=0 advisories=70 waived=0`，exit 0 |
| 4 | 同上 `--stage tasks` | `decision=pass errors=0 advisories=70 waived=0`，exit 0 |
| 5 | `python3 .specify/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/095-superagent-role/requirements.md --tasks .specify/specs/095-superagent-role/tasks.md` | `decision=proceed`；fr_count=38 / task_count=54（ceiling 120/160），exit 0 |

- advisory 构成说明：70 条均为 `missing-path`（implement 阶段才创建的交付路径，两个 `blockedBy` 模板占位 token 亦属格式节示例行）；与 plan 修复轮 `decision=pass / advisories=39` 同型，属预期。
- 附注（确定性读数，非门禁）：`account-clause-coverage.py --spec-dir …` 仍 `status: uncovered`、29 条子句超出冻结基线（本轮未新增契约子句——importable interface 折入既有 C-1，故 38 条子句数不变）；FR 契约引用组 lane 由 19 降为 18 uncovered。W3-06（覆盖率 lane 是否应成为门）仍属 MEDIUM，留待 owner 裁定。

## 4. 纪律说明

- 本修复轮为单写者：只改本特性产物与绑定 Feature 记录（095 行描述、详情文件）；未触碰其他特性、未 push、未提交既有脏文件（`checkpoints/` 为前序阶段遗留未跟踪，本轮不代提交）。
- 未运行测试套件（本修复轮只改规格/计划/任务/契约与记录，无产品代码变更；测试执行入口纪律保持 `scripts/bash/run-tests.sh`）。
- 异常：无；in-passing repair：无（全部改动即 §1/§2 所列处置）。假设（自行裁决并记录）：W2-01 选择「定死输入与纯函数签名」而非降级为文件投影——理由是 US4/SC-006 要求 digest 呈现每条执行体的父边，而 digest 现有读域（registry entries + triplets）不足以还原父边；一次物化 + 共享读取同时满足 FR-029 的单读约束。
