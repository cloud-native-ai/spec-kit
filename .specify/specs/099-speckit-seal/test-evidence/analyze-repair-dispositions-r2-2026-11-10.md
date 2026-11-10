# Analyze 修复轮 r2 — 处置记录（099-speckit-seal）

> 输入：`test-evidence/analyze-merged-r2-2026-11-10.md`（Round 2：0 CRITICAL / **1 HIGH（F-05）** / 5 MEDIUM / 1 LOW；F-05 为 `proposed`，是 r1 B-01 修复的残留实例）。
> 运行：`r20261110T121314Z-b099` · stage=analyze（修复回环 r2）· 四元组：flow_class=execution；source=declaration；marker=；error=-
> 纪律：分析报告 / checklist / research 是 dated record，**未修改**；本轮只处置 F-05 及其同类残留；MEDIUM 5 条与 LOW 1 条不在本轮范围（§6）。

## 1. 复核方法与计数

- 复核形态：**自证（self-verified）**。F-05 为 `proposed`（r2 独立复核波未派发）；本轮对报告锚点做修复前直读复测（file:line 原文逐字 + 缺陷类别可复现）→ `confirm`。
- 复核计数：**confirm 1 / reject 0 / downgrade 0**。严重度不变（HIGH）：F-05 承载 P8 的 SC-006 验收锚，旧口径会把合法第六类阻断读成不合规（封闭集声明，owner `shared/guidelines/closed-set-claims.md`）。
- 同类残留扫描（本轮的「全链」面）：短语面 `一一对应` / `恰好五项` / `仅五项` / `限于五项` / `只允许五项` / `恰五项` / `exactly five` / `one-to-one`，加语义面（`五项…对应/一致/相等`、`仅|只…五项`、`多出…不`）。扫描面 = spec 目录内 live 制品（排除 `test-evidence/`、`checklists/` 两个 dated-record 目录）+ 特性详情 `.specify/features/099-speckit-seal.md` + 注册表 `.specify/features.md`。结果见 §3。

## 2. F-05 锚点自证与修复

- 修复前原文复测（`plan.md:310`，P8 工作包「验收锚」列，逐字成立）：
  > `C-043；SC-006 逐项；阻断清单与 FR-027 五项一一对应`
- 缺陷成立依据：
  - 「与五项**一一对应**」是封闭清单声明（owner `shared/guidelines/closed-set-claims.md` § 处置），把合法阻断面收窄为恰好五项；
  - B-01 的 r1 修复已把 SC-006 / US3 / IT / FR-027 / C-043 / plan Summary / T-005 / quickstart S-7 / tasks DoD-6·T043·T044 统一为「五项是**下限** + 额外具名阻断逐条点名」（r2 复裁 7/7 关闭证据见 `analyze-merged-r2-2026-11-10.md` Rerun Delta）；
  - P8 是 074 回合的**派发与验收判读依据**——旧口径会让回合按错误标准验收，且与 SC-006 现文直接冲突（r2 §F-05，HIGH）。
- 修复（文本级回修，`plan.md:310` 的验收锚列）：
  > `C-043；SC-006 逐项；阻断清单逐条覆盖 FR-027 五项（下限），额外具名阻断逐条点名`
- 复核：新措辞与 `requirements.md:191`（SC-006）、`:162`（FR-027「五项是下限」）、C-043、`plan.md:31`/`:145`（T-005）、`quickstart.md:171`、`tasks.md:52/218/224/225` 的下限口径逐条一致。

## 3. 同类残留（全链扫描结果）

**发现并修复 1 处**（r2 的扫描面只覆盖 spec 目录，未覆盖特性详情文件）：

- `.specify/features/099-speckit-seal.md:39`（Key Changes 第 6 条，修复前原文）：
  > `终态二值（\`Sealed\` 或一一对应的具名阻断清单）。`
  修复后：
  > `终态二值（\`Sealed\` 或至少逐条覆盖五项、并逐条点名额外阻断的具名阻断清单）。`
  理由：注册表/详情是下游消费者读取的 live 摘要面，旧口径在同一缺陷类别下（封闭集声明），与 SC-006 冲突。

**判定为「非同类残留」（逐项留痕，不改动）**：

- `data-model.md:191`（E13 `item` = `FR-027(a)…(e) 五项之一`）：这是 FR-027 自身的条目定义域（a–e 即五项的**名称枚举**，不是验收口径）；额外具名阻断按 C-043 / T044 落 E3 `conflicts[]` / `dispositions[]` / 阻断态 stdout 捕获文件，不要求成为 E13 行——不构成封闭集声明。
- `contracts/records-and-boundaries.contract.md:131`（C-045 SC-006 取证形态「五项裁决逐条对照」）：下限取证描述，未排除额外条目；SC-006 全文的「额外阻断逐条点名」验收断言由该行引用的用例与回合记录承担。
- `.specify/features.md:102`（099 注册行）：无该缺陷类短语；行内 `R-01…R-20` 计数漂移属 §F-06/§G-01，范围外（§6）。
- `quickstart.md` / `tasks.md` / `feature-ref.md` / `research.md`：短语面与语义面均 0 命中（`research.md` 为 dated 实测记录，按纪律不改）。

**修复后复扫**：live 链 0 命中（`ZERO-LIVE-HITS`，证据 `analyze-repair-gates-r2-2026-11-10.txt` §7）；dated record（`test-evidence/`、`checklists/`）内的旧措辞按纪律保留不动，且 §7 的扫描面已显式排除。

## 4. 修复面清单

| 制品 | 变更点 |
|------|--------|
| `.specify/specs/099-speckit-seal/plan.md` | P8 验收锚（:310）：五项口径 → 「逐条覆盖（下限）+ 额外具名阻断逐条点名」 |
| `.specify/features/099-speckit-seal.md` | Key Changes 第 6 条（:39）：终态口径回显同步 |
| 本记录 + `analyze-repair-gates-r2-2026-11-10.txt` | 处置记录与门禁/扫描证据 |

**未改动**：`requirements.md`、`contracts/`、`data-model.md`、`quickstart.md`、`tasks.md`、`feature-ref.md`（r1 已同步，本轮复核一致）；`checklists/*`、`research.md`、`test-evidence/*` 既有文件（dated records）；`.specify/features.md`（注册行属 G-01/F-06 的 `manage-features` 刷新面）。

## 5. 门禁复跑

证据文件：`test-evidence/analyze-repair-gates-r2-2026-11-10.txt`（全量 stdout 捕获）。摘要：

| 门禁 | 结果 |
|------|------|
| `validate-requirements.py` | exit 0；6 检查项全 pass（251 行 / 37 定义行 / 3 共享字符串；0 error / 0 warning） |
| `pre-analyze-check.py --repo . --stage requirements` | `decision=pass`，errors=0，advisories=101 |
| `pre-analyze-check.py --repo . --stage plan` | `decision=pass`，errors=0，advisories=101 |
| `pre-analyze-check.py --repo . --stage tasks` | `decision=pass`，errors=0，advisories=101 |
| `decomposition-check.py --mode tasks` | exit 0；`decision=proceed`（FR 28 / tasks 51，均在 ceiling 内） |
| `validate-tasks.py`（支撑） | PASS，0 error / 0 warning |
| `validate-decision-tensions.py --spec … --json`（支撑） | exit 0；6 记录、六标签全 pass、`channel.high=0` |
| `clause_extract.py` 引用组重放（支撑） | exit 0；45 条款（13/14/10/8），C-001…C-045 全局连续——与 r2 读数一致（契约未改动） |
| F-05 短语复扫（本轮专用） | **hits: 0（ZERO-LIVE-HITS）**；修复锚点逐字读数见 gates §8 |

## 6. 范围外残留（不在本轮处置）

- MEDIUM 5 条：C-01（审计更正证据最小形态）、C-02（review「当前集合」派生规则）、F-03（dirty 判定范围措辞）、E-02（`coverage-baseline.txt` 缺席 → 条款差量仍不可判）、G-01（注册表阶段注记陈旧，由 `manage-features` reconcile 刷新）。
- LOW 1 条：F-06（`plan.md:62`/`:169`、`feature-ref.md:115` 的 research 计数漂移，随 G-01 一并改）。
- **E-02 仍是 analyze 覆盖步骤复跑的既定前提**：本轮未改条款宇宙；`baseline-missing`（exit 2）应继续读作「不可判」，MUST NOT 读作回归或通过。
- 观察（非 finding，交 close-out 处置）：`.specify/register.md` 目前没有 099 的 findings 登记行（F-01…F-06@099 / B-01@099 等）。r1 修复轮与各 close-out 均未登记；本轮按先例与任务范围不扩面，留痕供收口时按 ID Register 纪律补登。

## 7. Fast-fail 与异常声明

- 本轮**无 fast-fail 异常**：F-05 的修复由锚点直读复测与已记录的 owner 规则（SC-006 / C-043 的 B-01 口径、`closed-set-claims.md`）推出，无「以假设完成修复」的决策。
- **顺带修正（correction-in-passing，已披露）**：首轮短语扫描用 `grep -v 'test-evidence/'` 做内容级排除，P8 行自身含 `test-evidence/074-round-*.txt` 字样而被误滤，形成假阴性；改为**路径前缀排除**后复扫，恰好由此发现 §3 的 feature-detail 残留。该修正只影响扫描方法、不影响制品；扫描面定义已在 gates §7 显式留痕（教训：修复验证的排除条件必须作用在路径域，不能作用在内容域——否则被扫描行自身的路径字样会命中排除式）。
- 无其他可修补的「顺带修正」事项遗留。

## 8. 提交

- 单一修复提交，commit message：`099 analyze repair r2`。内容 = `plan.md` + `.specify/features/099-speckit-seal.md` + 本处置记录 + 门禁证据文件。
